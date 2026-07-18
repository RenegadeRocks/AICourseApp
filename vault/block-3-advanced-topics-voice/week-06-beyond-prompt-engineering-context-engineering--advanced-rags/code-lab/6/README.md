# Code-lab 6 — Context-engineered RAG v2 ablation harness

Companion to `06-sat-build-context-engineered-rag-v2.md`. One harness, seven
lanes, one report. You bring: a corpus (directory of `.md`/`.txt` files) and a
regression set (`queries.jsonl`). The harness builds lexical + dense indexes,
runs each lane, judge-scores the panel (context precision proxy, faithfulness,
answer relevancy, answerability), tracks cost/latency, and emits
`results/ablation_report.md`.

## Setup

```bash
cd code-lab/6
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip freeze > requirements.lock                       # pin your actual solve
```

Environment variables (never commit keys):

| Var | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | yes | generation + judge |
| `ANTHROPIC_MODEL` | no | generator model ID (default `claude-sonnet-5`; check the current ID on the pricing docs before a long run) |
| `ANTHROPIC_JUDGE_MODEL` | no | judge model ID (default: same family, stronger tier if you have it; PIN this per Week-4 discipline) |
| `COHERE_API_KEY` | no | enables the reranker lane (`--lane reranked` and reranking inside `v2_composed`) |

## Data layout

```
code-lab/6/
  docs/                 # your corpus: .md / .txt files (you supply)
  queries.jsonl         # your regression set (see queries.example.jsonl)
  results/              # created by the harness
```

`queries.jsonl` — one JSON object per line:

```json
{"id": "q001", "query": "What is our refund window?", "gold_answer": "30 days from delivery.", "answerable": true}
{"id": "q090", "query": "What was our 2019 headcount?", "gold_answer": null, "answerable": false}
```

Include 15–20 `"answerable": false` queries (Friday's manual labeling step).

## Commands

```bash
python run_ablation.py --lane baseline    --queries queries.jsonl --out results/
python run_ablation.py --lane hybrid_tuned --queries queries.jsonl --out results/
python run_ablation.py --lane reranked    --queries queries.jsonl --out results/   # needs COHERE_API_KEY
python run_ablation.py --lane budgeted    --queries queries.jsonl --out results/
python run_ablation.py --lane memory      --queries queries.jsonl --out results/   # runs the set twice
python run_ablation.py --lane tiered      --queries queries.jsonl --out results/ --repeats 3
python run_ablation.py --lane v2_composed --queries queries.jsonl --out results/ --repeats 3
python run_ablation.py --report           --out results/           # merge rows -> ablation_report.md
```

Each lane writes `results/<lane>.json` (per-query traces + aggregates).
`--repeats N` reruns stochastic lanes and reports mean ± spread.

## Lanes

| Lane | What it changes vs baseline |
|---|---|
| `baseline` | Week-4 shape: hybrid BM25+dense (RRF), top-k chunks, single-shot generation |
| `hybrid_tuned` | sweeps RRF constant and per-retriever candidate depth (4-combo grid in `harness.HYBRID_SWEEP_GRID`), one judged results row per combo; pick the winner, then confirm on a held-out slice you never tuned on |
| `reranked` | Cohere rerank over hybrid top-50 → top-5 |
| `budgeted` | token-budget cap on retrieved context + near-duplicate suppression |
| `memory` | RETRIEVAL_MEMORY.md read + write: vocabulary injected into query rewriting, new vocab/gap notes written after each query; scored on a second pass over the set (pass-1 spend reported separately) |
| `tiered` | single-shot + escalation trigger + capped agentic loop (6 calls / 40K tokens / 30s) with evidence log |
| `v2_composed` | your gate-passing subset, composed (edit `V2_STACK` in `harness.py`) |

## Judge discipline (read before trusting any number)

The judge prompts in `judge.py` are binary-per-dimension rubrics. Before any
lane run, confirm your judge still clears the >=90% human-agreement bar from
Block 2 Week 4 (`python judge.py --validate labels.csv` compares judge output
against your hand labels). If it doesn't, fix the rubric first; a harness with
an unvalidated judge produces decorated randomness.

## Costs

A 100-query regression set through all seven lanes with `--repeats 3` on the
stochastic ones is on the order of a few hundred model calls for pipelines plus
about a thousand judge calls. At Sonnet-5-class prices that's typically single-
digit dollars; the report splits pipeline cost from measurement cost. The
harness prints a cost estimate and asks for confirmation before lanes that
exceed $5 estimated.

## Notes

- Dense retrieval uses Chroma's default local embedding function (no API key,
  runs on CPU). Swap in an API embedder in `harness.py` if your Week-4 index
  used one — comparisons are only valid if baseline and lanes share the
  embedder.
- The agentic lane is a deliberately small tool-use loop (search / read / stop)
  so you can read every trace. It is a teaching implementation, not a product.
- Nothing here persists outside `results/` and `RETRIEVAL_MEMORY.md`.
