# Week 6 briefs — Beyond Prompt Engineering: Context Engineering + Advanced RAGs

Curriculum sessions: "Beyond Prompt Engineering – Context Engineering" +
"Advanced RAGs". July-2026 interpretation: context engineering is now the
named discipline (Anthropic's "effective context engineering" essay, Karpathy's
framing); "advanced RAG" means retrieval as one tool inside an agentic context
strategy, not a bigger vector database. The reader upgraded from prompt-writer
to context architect.

Day plan (researcher may sharpen titles; keep the arc):

- **01-mon — Context engineering: the discipline that replaced prompt golf.**
  Context as a finite budget under attention degradation (context rot; the
  1M-token era does NOT repeal it — verify current long-context benchmarks).
  System prompt altitude, tool-definition token costs, just-in-time vs
  pre-loaded context. Link back to b0w0 context-economics + new tokenizer.
- **02-tue — Memory & compaction architectures.** Compaction/summarization,
  structured note-taking (NOTES.md / to-do persistence), sub-agent context
  isolation, memory tools across vendors (Claude memory tool, ChatGPT memory,
  frameworks); when memory helps vs contaminates. CLAUDE.md as memory — link
  b0w0 wed, don't re-teach.
- **03-wed — Retrieval architectures beyond naive RAG.** Hybrid (BM25+dense),
  rerankers (current leaders — verify), late-interaction (ColBERT-family),
  multi-vector, GraphRAG and its 2026 verdict (where it wins/loses, cost),
  structured/SQL retrieval. Wikilink the CR ladder (b0w01) — do not re-teach.
- **04-thu — Agentic retrieval.** Retrieval as tool-use loop: query planning,
  iterative search, self-correction, citations/grounding; agentic RAG vs
  single-shot; deep-research patterns; when agentic retrieval is overkill
  (latency/cost math with current model pricing).
- **05-fri — Evaluating context strategies.** Retrieval evals beyond hit-rate
  (answerable-vs-not, citation faithfulness, context-precision); long-context
  evals (NoLiMa/RULER-class, current SOTA); ablation methodology: measure
  context-budget changes like an engineer. Link b2w04 sat eval discipline.
- **06-sat — BUILD: upgrade the Week-4 RAG agent to a context-engineered v2.**
  Take the b2w04 build; add hybrid+rerank, compaction, memory notes, agentic
  retrieval fallback; ablation-test each addition against the Week-4 baseline
  with the ≥90% judge-agreement discipline. Claude Code orchestrated;
  code-lab for the harness.
- **07-sun — Synthesis + quiz + flashcards.** Must be consistent with the
  week; no duplicate quiz items from earlier weeks' quizzes.

Controversies to engage (verify current state): does 1M-context kill RAG
(no — but the frontier position moved; get the July-2026 nuance right);
GraphRAG hype vs production reality; memory-as-moat vs memory-as-contamination;
"context engineering" as genuine discipline vs rebranded prompt engineering
(name skeptics).
