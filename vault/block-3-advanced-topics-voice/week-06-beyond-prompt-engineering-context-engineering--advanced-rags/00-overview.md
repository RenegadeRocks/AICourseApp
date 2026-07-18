---
type: week-overview
block: block-3-advanced-topics-voice
week: week-06
title: 'Week 6 — Beyond prompt engineering: context engineering + advanced RAGs'
live_sessions:
  - '2026-06-27 — Beyond Prompt Engineering: Context Engineering'
  - '2026-06-28 — Advanced RAGs'
study_window: 2026-06-22 to 2026-06-28
last_verified: 2026-07-17
---

# Week 6 — The context architect: budgets, memory, retrieval, and the evals that referee them

## The thesis of this week

In June 2025 Tobi Lütke and Andrej Karpathy renamed the job. Not "prompt engineering," the wording of one instruction, but **context engineering**: "the delicate art and science of filling the context window with just the right information for the next step."[Karpathy, June 2025] Anthropic's September 2025 engineering essay made it a named discipline with named techniques: context as a finite, degrading resource; system-prompt altitude; token-efficient tools; just-in-time retrieval; compaction; structured note-taking; sub-agent isolation. By mid-2026, with every frontier lab shipping 1M-token windows, the naive conclusion is that none of this matters anymore. The naive conclusion is wrong, and this week teaches you exactly why, with the benchmarks (NoLiMa, RULER, Chroma's context-rot research) that measure the gap between *advertised* and *effective* context.

The second half of the week applies the same discipline to retrieval. "Advanced RAG" in 2026 does not mean a bigger vector database. It means retrieval as one tool inside an agentic context strategy: hybrid lexical+dense with a reranker, late-interaction models where they pay, GraphRAG only where the problem is genuinely structural, SQL where the data is tabular, and an agentic loop that plans queries, inspects results, and re-searches. Then Friday and Saturday make it falsifiable: you measure every context decision like an engineer, and you upgrade your Week-4 RAG build to a context-engineered v2 with an ablation harness that proves which additions earned their complexity.

## Who this week is for

You shipped the Block 2 builds: a RAG pipeline with an eval harness ([[04-thu-rag-fundamentals|Week 4]]) and a report generator ([[06-sat-build-the-weekly-report-generator|Week 5]]). You can direct Claude Code, you know what hit-rate@k and LLM-as-judge mean, and you have felt at least one agent degrade as its context filled. This week turns that felt experience into an engineering discipline you can sell: the difference between "we prompt the model well" and "we control every token the model sees, and we can prove each one pays rent."

## Shape of the week

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | Context engineering: the finite-budget discipline — context rot, advertised vs effective windows, system-prompt altitude, tool-token costs, just-in-time context | Deep-dive + context-audit experiment |
| Tue | Memory and compaction architectures — compaction, structured notes, sub-agent isolation, memory tools across vendors, when memory contaminates | Deep-dive + memory-tool experiment |
| Wed | Retrieval beyond naive RAG — hybrid+rerank (current leaderboard), late interaction, GraphRAG's 2026 verdict, structured/SQL retrieval | Deep-dive + reranker ablation |
| Thu | Agentic retrieval — retrieval as a tool-use loop, query planning, deep-research patterns, the cost math for when agents are overkill | Deep-dive + agentic-vs-single-shot experiment |
| Fri | Evaluating context strategies — beyond hit-rate, long-context evals, ablation methodology | Deep-dive + eval-design problem set |
| Sat | BUILD: upgrade the Week-4 RAG agent to context-engineered v2, with an ablation harness | Full build, `code-lab/6/` |
| Sun | Synthesis + 15-question quiz + 30 flashcards + capstone | Review + ship plan |

## Why these topics belong together

Monday names the budget. Tuesday manages the budget over time. Wednesday and Thursday spend the budget well (what to retrieve, and who decides). Friday referees every choice with evals. Saturday makes you prove it on your own corpus. The through-line is a single question asked seven ways: **what configuration of tokens most improves the next model call, and how do you know?**

## Prerequisites from earlier weeks

Context economics and the new-tokenizer cost math live in [[05-fri-context-window-economics|Block 0 Week 0]]. The Contextual Retrieval ladder lives in [[03-wed-rag-as-a-system|Block 0 Week 1]]. The eval-threshold discipline (≥90% judge–human agreement before you trust a judge) lives in [[06-sat-rag-evaluation|Block 2 Week 4]]. This week links to all three and re-teaches none of them.

The cohort's live sessions are 2026-06-27 and 2026-06-28. As always: the vault lessons are the primary instruction; the live sessions are the bonus.

_last_verified: 2026-07-17_
