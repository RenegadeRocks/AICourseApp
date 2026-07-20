"""Retrieval lanes for the Week-6 ablation harness.

Lanes: baseline, hybrid_tuned, reranked, budgeted, memory, tiered, v2_composed.
Each lane is a function (query, ctx) -> LaneResult. Indexes are built once.

Deliberately small: every trace should be readable. This is a teaching
implementation, not a product.
"""

from __future__ import annotations

import json
import os
import re
import time
from dataclasses import dataclass, field
from pathlib import Path

import bm25s
import chromadb
from anthropic import Anthropic

DOCS_DIR = Path(os.environ.get("LAB_DOCS", "docs"))
CHUNK_TOKENS = 400  # approx, by whitespace words * 1.3
MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5")
MEMORY_FILE = Path("RETRIEVAL_MEMORY.md")

# Edit after your gates are decided (Saturday, Stage 5):
V2_STACK = {"rerank": True, "budget": True, "memory": False, "tiered": True}

client = Anthropic()


# ---------------------------------------------------------------- corpus

def load_chunks() -> list[dict]:
    """Split corpus files into ~CHUNK_TOKENS word chunks with ids."""
    chunks = []
    for f in sorted(DOCS_DIR.glob("**/*")):
        if f.suffix.lower() not in {".md", ".txt"}:
            continue
        words = f.read_text(encoding="utf-8", errors="ignore").split()
        step = int(CHUNK_TOKENS / 1.3)
        for i in range(0, max(len(words), 1), step):
            text = " ".join(words[i : i + step])
            if text.strip():
                chunks.append({"id": f"{f.name}::{i // step}", "text": text})
    if not chunks:
        raise SystemExit(f"No .md/.txt files found under {DOCS_DIR}/")
    return chunks


class Indexes:
    def __init__(self, chunks: list[dict]):
        self.chunks = chunks
        self.by_id = {c["id"]: c for c in chunks}
        texts = [c["text"] for c in chunks]
        self.bm25 = bm25s.BM25()
        self.bm25.index(bm25s.tokenize(texts, stopwords="en"))
        cdb = chromadb.PersistentClient(path=".chroma")
        self.col = cdb.get_or_create_collection("lab6")
        have = set(self.col.get()["ids"])
        missing = [c for c in chunks if c["id"] not in have]
        if missing:
            self.col.add(ids=[c["id"] for c in missing],
                         documents=[c["text"] for c in missing])

    def lexical(self, q: str, k: int) -> list[str]:
        idx, _ = self.bm25.retrieve(bm25s.tokenize(q, stopwords="en"), k=min(k, len(self.chunks)))
        return [self.chunks[i]["id"] for i in idx[0]]

    def dense(self, q: str, k: int) -> list[str]:
        res = self.col.query(query_texts=[q], n_results=min(k, len(self.chunks)))
        return res["ids"][0]

    def hybrid(self, q: str, k: int = 20, rrf_c: int = 60,
               k_lex: int = 50, k_dense: int = 50) -> list[str]:
        scores: dict[str, float] = {}
        for ranking in (self.lexical(q, k_lex), self.dense(q, k_dense)):
            for rank, cid in enumerate(ranking):
                scores[cid] = scores.get(cid, 0.0) + 1.0 / (rrf_c + rank + 1)
        return [cid for cid, _ in sorted(scores.items(), key=lambda x: -x[1])][:k]


# ---------------------------------------------------------------- model calls

@dataclass
class Usage:
    input_tokens: int = 0
    output_tokens: int = 0
    calls: int = 0

    def add(self, msg):
        self.input_tokens += msg.usage.input_tokens
        self.output_tokens += msg.usage.output_tokens
        self.calls += 1


def ask(system: str, user: str, usage: Usage, max_tokens: int = 900) -> str:
    msg = client.messages.create(model=MODEL, max_tokens=max_tokens,
                                 system=system,
                                 messages=[{"role": "user", "content": user}])
    usage.add(msg)
    return "".join(b.text for b in msg.content if b.type == "text")


GEN_SYSTEM = (
    "Answer strictly from the provided context chunks. Cite chunk ids inline "
    "like [id]. If the context does not contain the answer, reply exactly: "
    "NOT_IN_CORPUS, followed by one sentence on what is missing."
)


def generate(query: str, chunk_ids: list[str], idx: Indexes, usage: Usage) -> str:
    ctx = "\n\n".join(f"<chunk id='{cid}'>\n{idx.by_id[cid]['text']}\n</chunk>"
                      for cid in chunk_ids)
    return ask(GEN_SYSTEM, f"Context:\n{ctx}\n\nQuestion: {query}", usage)


# ---------------------------------------------------------------- helpers

def rerank(query: str, chunk_ids: list[str], idx: Indexes, top_n: int = 5) -> list[str]:
    """Cohere rerank over candidates. Requires COHERE_API_KEY."""
    import cohere  # optional dep
    co = cohere.ClientV2()
    model = os.environ.get("COHERE_RERANK_MODEL", "rerank-v3.5")  # set to current leader per Wed lesson
    docs = [idx.by_id[c]["text"] for c in chunk_ids]
    res = co.rerank(model=model, query=query, documents=docs, top_n=top_n)
    return [chunk_ids[r.index] for r in res.results]


def budget_filter(chunk_ids: list[str], idx: Indexes, max_words: int = 1200) -> list[str]:
    """Token-budget cap + crude near-duplicate suppression."""
    kept, seen_starts, words = [], set(), 0
    for cid in chunk_ids:
        text = idx.by_id[cid]["text"]
        start = " ".join(text.split()[:12]).lower()
        if start in seen_starts:
            continue
        w = len(text.split())
        if words + w > max_words and kept:
            break
        kept.append(cid); seen_starts.add(start); words += w
    return kept


def memory_vocab() -> str:
    if not MEMORY_FILE.exists():
        return ""
    text = MEMORY_FILE.read_text(encoding="utf-8")
    m = re.search(r"## Vocabulary\n(.*?)(\n## |\Z)", text, re.S)
    return m.group(1).strip() if m else ""


def memory_append(section: str, line: str) -> None:
    from datetime import date
    entry = f"- ({date.today().isoformat()}) {line}\n"
    text = MEMORY_FILE.read_text(encoding="utf-8") if MEMORY_FILE.exists() else \
        "# Retrieval memory\n\n## Vocabulary\n\n## Known gaps\n\n## Judge feedback\n"
    text = text.replace(f"## {section}\n", f"## {section}\n{entry}", 1)
    if len(text.splitlines()) <= 150:  # hard cap from the lesson
        MEMORY_FILE.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------- lanes

@dataclass
class LaneResult:
    answer: str
    chunk_ids: list[str]
    usage: Usage
    seconds: float
    escalated: bool = False
    trace: list = field(default_factory=list)


def _timed(fn):
    def wrap(query: str, idx: Indexes, **kw) -> LaneResult:
        t0 = time.time()
        res = fn(query, idx, **kw)
        res.seconds = time.time() - t0
        return res
    return wrap


@_timed
def lane_baseline(query: str, idx: Indexes, k: int = 5, **_) -> LaneResult:
    u = Usage()
    ids = idx.hybrid(query, k=k)
    return LaneResult(generate(query, ids, idx, u), ids, u, 0)


@_timed
def lane_reranked(query: str, idx: Indexes, **_) -> LaneResult:
    u = Usage()
    ids = rerank(query, idx.hybrid(query, k=50), idx, top_n=5)
    return LaneResult(generate(query, ids, idx, u), ids, u, 0)


@_timed
def lane_budgeted(query: str, idx: Indexes, **_) -> LaneResult:
    u = Usage()
    ids = budget_filter(idx.hybrid(query, k=20), idx)
    return LaneResult(generate(query, ids, idx, u), ids, u, 0)


@_timed
def lane_memory(query: str, idx: Indexes, **_) -> LaneResult:
    """Read RETRIEVAL_MEMORY.md to rewrite the query, answer, then WRITE what
    this pass learned back to the file (Tuesday's write-policy, minimally).
    The write is what makes run_ablation's second pass a real measurement:
    pass 1 records vocabulary/gaps, pass 2 retrieves with them."""
    u = Usage()
    vocab = memory_vocab()
    q = query
    if vocab:
        q = ask("Rewrite the search query using this corpus vocabulary map. "
                "Return only the rewritten query.\n" + vocab, query, u, max_tokens=100)
    ids = idx.hybrid(q, k=5)
    answer = generate(query, ids, idx, u)
    # Write policy, applied at end of turn: refusals become Known gaps;
    # otherwise harvest up to 3 query-term -> corpus-term mappings.
    if "NOT_IN_CORPUS" in answer:
        memory_append("Known gaps", query[:100])
    else:
        preview = "\n".join(idx.by_id[c]["text"][:300] for c in ids[:3])
        terms = ask(
            "From these corpus excerpts, list at most 3 corpus-specific terms "
            "or synonyms that would improve future searches for the question. "
            "One per line, formatted 'question-term -> corpus-term'. "
            "Reply NONE if none.",
            f"Question: {query}\nExcerpts:\n{preview}", u, max_tokens=100)
        for line in terms.splitlines():
            if "->" in line:
                memory_append("Vocabulary", line.strip("- ").strip()[:120])
    return LaneResult(answer, ids, u, 0)


AGENT_SYSTEM = (
    "You retrieve evidence to answer a question over a private corpus. "
    "Respond ONLY with JSON: {\"action\": \"search\", \"query\": \"...\"} to "
    "search again, or {\"action\": \"answer\"} when evidence is sufficient or "
    "clearly absent. Prefer short, broad queries first; use corpus vocabulary "
    "you observe in results."
)


@_timed
def lane_tiered(query: str, idx: Indexes, max_calls: int = 6,
                max_tokens_cap: int = 40_000, max_seconds: float = 30.0, **_) -> LaneResult:
    u = Usage()
    # fast lane
    ids = idx.hybrid(query, k=5)
    answer = generate(query, ids, idx, u)
    trigger = "NOT_IN_CORPUS" in answer or len(set(ids[:5])) < 3
    if not trigger:
        return LaneResult(answer, ids, u, 0, escalated=False)
    # agentic lane, hard-capped (calls / tokens / wall-clock)
    t0 = time.time()
    evidence: list[str] = []
    trace = []
    q = query
    for _ in range(max_calls):
        if u.input_tokens + u.output_tokens > max_tokens_cap or time.time() - t0 > max_seconds:
            break
        found = idx.hybrid(q, k=5)
        evidence = list(dict.fromkeys(evidence + found))[:12]
        preview = "\n".join(f"[{c}] {idx.by_id[c]['text'][:200]}" for c in found)
        step = ask(AGENT_SYSTEM,
                   f"Question: {query}\nSearched so far: {trace}\n"
                   f"Latest results:\n{preview}\nEvidence ids held: {evidence}",
                   u, max_tokens=150)
        trace.append({"query": q, "found": found, "decision": step[:200]})
        try:
            action = json.loads(step[step.index("{"): step.rindex("}") + 1])
        except ValueError:
            break
        if action.get("action") == "search" and action.get("query"):
            new_q = action["query"]
            if new_q != q:
                memory_append("Vocabulary", f"'{query[:60]}' -> '{new_q[:60]}'")
            q = new_q
        else:
            break
    ids = budget_filter(evidence, idx)
    answer = generate(query, ids, idx, u)
    if "NOT_IN_CORPUS" in answer:
        memory_append("Known gaps", query[:100])
    return LaneResult(answer, ids, u, 0, escalated=True, trace=trace)


@_timed
def lane_v2_composed(query: str, idx: Indexes, **_) -> LaneResult:
    u = Usage()
    q = query
    if V2_STACK["memory"] and (vocab := memory_vocab()):
        q = ask("Rewrite the search query using this corpus vocabulary map. "
                "Return only the rewritten query.\n" + vocab, query, u, max_tokens=100)
    ids = idx.hybrid(q, k=50 if V2_STACK["rerank"] else 20)
    if V2_STACK["rerank"]:
        ids = rerank(q, ids, idx, top_n=8)
    if V2_STACK["budget"]:
        ids = budget_filter(ids, idx)
    answer = generate(query, ids, idx, u)
    if V2_STACK["tiered"] and "NOT_IN_CORPUS" in answer:
        res = lane_tiered(query, idx)
        # fold the pre-escalation spend into the reported usage
        res.usage.input_tokens += u.input_tokens
        res.usage.output_tokens += u.output_tokens
        res.usage.calls += u.calls
        return res
    return LaneResult(answer, ids, u, 0)


def make_hybrid_lane(rrf_c: int, k_lex: int, k_dense: int):
    """A baseline-shaped lane with fixed hybrid-fusion params. run_ablation's
    --lane hybrid_tuned builds one of these per HYBRID_SWEEP_GRID combo."""
    @_timed
    def lane(query: str, idx: Indexes, k: int = 5, **_) -> LaneResult:
        u = Usage()
        ids = idx.hybrid(query, k=k, rrf_c=rrf_c, k_lex=k_lex, k_dense=k_dense)
        return LaneResult(generate(query, ids, idx, u), ids, u, 0)
    return lane


# Small, honest sweep: 2 RRF constants x 2 candidate depths = 4 combos.
# Widen only after a first sweep shows the metric moves at all.
HYBRID_SWEEP_GRID = [
    {"rrf_c": 20, "k_lex": 20, "k_dense": 20},
    {"rrf_c": 60, "k_lex": 20, "k_dense": 20},
    {"rrf_c": 20, "k_lex": 50, "k_dense": 50},
    {"rrf_c": 60, "k_lex": 50, "k_dense": 50},
]


LANES = {
    "baseline": lane_baseline,
    "hybrid_tuned": lane_baseline,  # default params; run_ablation sweeps HYBRID_SWEEP_GRID
    "reranked": lane_reranked,
    "budgeted": lane_budgeted,
    "memory": lane_memory,
    "tiered": lane_tiered,
    "v2_composed": lane_v2_composed,
}
