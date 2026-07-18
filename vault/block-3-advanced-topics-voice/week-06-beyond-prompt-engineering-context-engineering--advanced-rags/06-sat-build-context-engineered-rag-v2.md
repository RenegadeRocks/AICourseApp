---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 6
day_name: sat
session_slug: advanced-rags
date_due: 2026-06-27
tags: [build-day, ablation-harness, hybrid-search, reranking, compaction, memory, agentic-fallback, regression-gates, claude-code, code-lab]
sources:
  - anthropic-effective-context-engineering-2025
  - anthropic-context-management-2025
  - agentset-reranker-leaderboard-2026
  - bm25s-arxiv
  - hamel-field-guide-2025
  - marsdevs-agentic-rag-2026
  - anthropic-sonnet-5-pricing-2026
  - chroma-context-rot-2025
last_verified: 2026-07-17
word_count_target: 5000
---

# BUILD — upgrade the Week-4 RAG agent to a context-engineered v2, with proof

## Why this matters

Today you convert a week of concepts into a system and (the part that separates this build from every RAG tutorial on the internet) into an *evidence table*. The deliverable is not "my RAG got better." The deliverable is a filled ablation matrix showing, per intervention, what it cost and what it bought on your corpus, plus a v2 pipeline composed only of the interventions that cleared their pre-registered gates. That artifact is worth more than the pipeline itself: it is the thing you show a client to justify an architecture, the thing you re-run when a model swap lands, and the working demonstration that you practice context engineering as measurement rather than as vibes. Everything runs from Claude Code orchestrating the harness in `code-lab/6/`; plan for a 3–5 hour block.

## Prerequisites

- Your Week-4 baseline: corpus, pipeline, regression set, and a judge validated to the [[06-sat-rag-evaluation|≥90% agreement bar]]. If the judge was never validated, that is step zero today, not optional.
- Yesterday's `ABLATION_PLAN.md` with gates filled in *before* you run anything. No plan, no build — go do [[05-fri-evaluating-context-strategies|Friday's]] experiment first.
- `code-lab/6/` installed (README there; pinned deps; `ANTHROPIC_API_KEY` required, `COHERE_API_KEY` optional for the reranker lane).
- 15–20 hand-labeled *not-in-corpus* queries added to your regression set (Friday's manual step).

## Layer 0 — Three architecture decisions before you type anything

**Decision 1: hand-rolled lanes vs platform features.** Half of what the harness implements (context budgets, stale-result clearing, memory files) now exists as platform features: context editing and the memory tool on the Claude Developer Platform, compaction inside Claude Code.[^2] You are building the hand-rolled versions anyway, for two defensible reasons: the ablation requires *isolatable* interventions (a platform feature you cannot toggle per-lane cannot be attributed), and owning the mechanics once means you can evaluate platform features instead of believing them. Write this tradeoff down in your engineering memo; a client will eventually ask why you didn't "just use the built-in thing," and the answer ("we did, after we measured that it helped") is the whole brand of this course.

**Decision 2: which model, pinned how.** The harness reads the generator and judge models from env vars, and the correct discipline is: pin both for the entire ablation, record the IDs in the report header, and treat any model change as a new baseline, not a new row. The tempting mistake is upgrading the generator mid-ablation because a new checkpoint dropped; that converts your matrix into archaeology. Judge pinning matters even more: the Week-4 lesson documented score drift of several points across judge swaps with no pipeline change, and current-generation tokenizer changes make cross-generation swaps *more* shift-prone, not less.

**Decision 3: where the harness lives afterward.** Decide now: does `code-lab/6/` get copied into your project repo (where it can rot alongside the pipeline it measures) or does it live as a standalone eval repo that treats your pipeline as a black box over HTTP/CLI? For solo operators the copy is fine. For anything with a client attached, the standalone shape is worth the hour: it survives pipeline rewrites, and "our evals outlive our implementations" is a sentence that closes deals.

## The build, stage by stage

### Stage 0 — Freeze and re-score the baseline (30 min)

Pin everything: model ID, prompts, chunking, index contents, regression-set version. Then re-score the Week-4 baseline with today's *fuller* panel (the harness adds answerability and cost/latency columns your Week-4 harness may not have had). Do not skip the re-score even though "Week 4 already measured it": the panel changed, the model landscape changed since April, and a baseline measured under different instrumentation is not a baseline, it's a memory.

Run, from Claude Code:

> Run `python run_ablation.py --lane baseline --queries queries.jsonl --out results/` in code-lab/6, then summarize the baseline row: panel metrics, answerability on the unanswerable slice, mean cost/query, p50/p95.

Sanity checks before proceeding: answerability on the unanswerable slice should be imperfect (if it's 100%, your unanswerable queries are too easy); faithfulness below ~0.7 means fix generation before measuring retrieval upgrades — you'd be tuning the supply chain of a broken factory.

### Stage 1 — Hybrid retuning + reranker (45–60 min)

Your Week-4 pipeline already runs hybrid BM25+dense with RRF ([[04-thu-rag-fundamentals|not re-taught]]). The v2 work: (a) re-verify the fusion is actually earning its keep on the *current* regression set (the harness's `--lane hybrid_tuned` sweeps the RRF constant and k per retriever); (b) add the reranker lane over hybrid top-50, using whichever API you chose Wednesday (the harness ships Cohere wiring; swapping in Voyage is a ten-line change Claude Code will do on request).

Gate check, per your plan. The typical pattern on a few-hundred-document corpus: reranking buys its biggest wins on context *precision* (it concentrates relevance in the top 5, which shrinks the window you need, a context-budget win that compounds with every later stage), at 300–700ms and a per-query fee. If your measured lift is inside your noise band, the honest move is the one nobody makes: *don't ship it*, and write down why. An ablation harness that has never rejected an intervention is a rubber stamp.

### Stage 2 — Context-budget discipline: retrieval-side compaction (30–45 min)

Apply Monday and Tuesday to the pipeline itself. The `--lane budgeted` run enforces: retrieved context capped by *token budget* rather than chunk count (tight top-k after reranking); duplicate/near-duplicate chunk suppression; and stale-context hygiene in the agentic lane (older tool results cleared once superseded: the microcompact insight at pipeline scale, and the same shape as Anthropic's context-editing result, which was, remember, an 84% *deletion* that improved outcomes on their harness[^2]). Also run the **deletion row** from Monday's audit: whatever component had the worst signal-per-token (that MCP server, that bloated prompt section) gets a run without it.

This stage is where Chroma's finding becomes practical: fewer, better tokens frequently outscore more tokens, because the distractors you declined to include were going to tax attention.[^3] Expect small accuracy deltas and large cost deltas; the gate that matters here is usually cost-at-equal-quality.

### Stage 3 — Memory notes (30–45 min)

The v2 memory is deliberately modest and legible (Tuesday's position, enacted; the structured note-taking pattern from Anthropic's context-engineering essay[^8]): a single `RETRIEVAL_MEMORY.md` per corpus, schema'd as `## Vocabulary` (user-term → corpus-term mappings discovered during agentic runs), `## Known gaps` (queries the corpus cannot answer), and `## Judge feedback` (recurring failure notes). The agentic lane reads it before planning queries and appends to it after runs; the single-shot lane injects only the Vocabulary section into query rewriting. Caps: 150 lines, dated entries, gaps expire after 60 days (the invalidation rule you designed Tuesday).

Measure it honestly: memory helps *repeat* traffic, so the harness scores it by running the regression set twice and comparing second-pass metrics. If your regression set has no repeat-structure, expect ≈0 and say so; a null result recorded is a result, and it tells you memory belongs in your production loop (where traffic repeats) rather than in your eval headline.

### Stage 4 — Agentic fallback lane (45–60 min)

Wire Thursday's tiered architecture: single-shot answers everything; the escalation trigger (your Phase-4 design from Thursday — the harness ships two: a generation-declared insufficiency signal, NOT_IN_CORPUS, and a retrieval-diversity floor) promotes to the agentic lane; the loop carries hard caps (default: 6 tool calls, 40K tokens, 30s) and an evidence log that feeds the citation pass. Run `--lane tiered`.

Score three things separately, because they fail separately: hard-lane quality lift (the point of the lane), false-promotion rate on easy queries (the cost leak), and cap-hit rate (a high one means your caps are the de-facto stop condition — Thursday's "sufficiency judgment is unsolved" made concrete[^4]).

### Stage 5 — Compose v2, full re-score, and the verdict (45 min)

Compose only the gate-passing interventions, run `--lane v2_composed`, and compare against the sum-of-parts expectation. Interactions will show up (the reranker changes what the budget cap keeps; memory changes what the agent searches). Then write the two closing artifacts:

1. **The verdict table** — the harness emits `results/ablation_report.md`; annotate each row with ship/no-ship and one sentence of reasoning. This is the client-facing artifact.
2. **The 300-word engineering memo** — what surprised you, which vendor number failed to transfer to your corpus, and what the monitoring twin (Chip Huyen's critique from Friday) needs to watch in production.

A build that ships two of five interventions with evidence beats a build that ships five with none. That sentence is the week.

## The cost ledger — what today actually costs, and how to say so

Instrument the meta-question too: what did the *evidence* cost? A representative run (100-query regression set, seven lanes, `--repeats 3` on the two stochastic lanes, judge on everything) lands in the region of 1,500–2,500 model calls. At Sonnet-5-class prices that is typically single-digit dollars of API spend;[^5] the real cost is your 3–5 hours. Write both numbers in the report footer, because they are the answer to the two objections you will hear forever:

- *"Evals are expensive."* The counter is the ledger: the full matrix cost less than lunch, and the false-promotion leak it caught costs $1,000+/month at modest traffic (Thursday's arithmetic). Evals are only expensive when priced against not-measuring, which is free the way unvented gas leaks are free.
- *"We'll eval later."* The counter is the reuse curve: the harness's marginal cost per rerun approaches zero, and the reruns are scheduled (model swap, corpus growth, monthly regression). The first ablation buys an asset, not a report.

One honest caveat belongs in the same footer: today's evidence is offline evidence. The panel scores, the gates, the ablation table — all measured on a frozen regression set. Production traffic will disagree with it somewhere (Friday's Chip Huyen critique), and the monitoring twin exists to find where. A report that names its own blind spot is more credible to sophisticated buyers, not less.

## Stretch goals — if the matrix is done and it's not dinner yet

1. **The judge-swap sensitivity row.** Re-score the composed v2 with a different judge model (same rubric) and report the delta. If scores move more than 2–3 points, your gates need margins, and you have independently rediscovered why judges get pinned.
2. **The rot row.** Add a lane that retrieves top-20 *without* budget filtering, padding the window with plausible near-misses, and watch faithfulness. This is Monday's Phase-4 demo running inside your own harness, and it makes the context-budget gate self-justifying in one chart.
3. **The mini deep-research lane.** Chain the tiered lane's agentic mode with Tuesday's RETRIEVAL_MEMORY.md across the full regression set twice, and measure whether second-pass escalation *rate* drops (the memory teaching the fast lane, as in Thursday's middle case study). If it does, you have a learning system with receipts, which is a genuinely rare artifact to show a client.
4. **The client one-pager.** Convert `ablation_report.md` into a one-page client-facing version: three sentences of method, the table, ship/no-ship column, and the monitoring plan. Time-box to 30 minutes. The skill of compressing evidence without inflating it is the week's commercial payload.

## Common mistakes experts see

- **Gates edited after results.** The plan file is version-controlled for exactly this reason. A moved gate is a documented decision, not a silent edit.
- **Testing on the queries you tuned on.** If you iterated prompts against the regression set all afternoon, hold out a slice you never looked at for the final v2 score.
- **The rubber-stamp harness.** Every intervention passes because gates were set generously. Calibrate: at least one row should fail on a typical corpus, most often memory or (for low-rank-gap corpora) the reranker.
- **Judging the agentic lane once.** It's stochastic; the harness's `--repeats 3` exists for it. Report spread.
- **Cost accounting that omits the judge.** Eval tokens are real spend; the report separates pipeline cost from measurement cost so you don't bill measurement to the architecture.
- **Shipping v2 without deleting v1's dead weight.** The deletion row that passed its gate is a change too. Removals count as upgrades.
- **Calling it done.** The harness's value is amortized over reruns: model swap (the Sonnet-5-class intro pricing ends August 31 — someone will propose a swap[^5]), corpus growth, quarterly regression. Schedule the rerun before you close the laptop.

## Reflection questions

1. Which intervention had the largest gap between the week's cited numbers and your measured result? Diagnose the gap using Friday's four-way decomposition (task, harness, judge, budget).
2. Your false-promotion rate is 9% and each promotion costs 6× — write the actual dollars/month at your traffic and decide whether tightening the trigger is worth a week of your time.
3. If you could keep only *one* v2 intervention, which does your table say, and would the client agree given their latency SLA?
4. What would the ablation matrix look like for the Week-7 voice agent, where p95 latency budgets are an order of magnitude tighter? Which of today's winners survive?
5. Write the three-line cron job description for the monitoring twin: what re-runs, how often, and what pages you.

## My take (reviewer lens)

**Michael Seibel** would look at the five-stage plan and say most of you should ship Stage 1 and Stage 4 and go find a customer: the harness is beautiful, but a solo builder spending Saturday perfecting a memory lane that measures ≈0 is optimizing the demo, not the business — do the ugly two-lane version, charge for it, and let real traffic tell you which ablation to run next. He is right for week one of an engagement, and wrong the week a client asks "why should we trust it," which is when the evidence table closes the deal. **Boris Cherny** would push on tooling honesty: a custom harness in `code-lab/6/` is a liability you now maintain, and half of it (context editing, compaction, sub-agent budgets) is already productized at the platform layer — the lesson should say clearly that the harness is for *learning the mechanics and owning the evidence*, and that mature teams should let the platform do the context management and keep only the eval half. Agreed, and that is the intended trajectory: keep `run_ablation.py`, retire the hand-rolled lanes as the platform eats them. **A cohort peer** would flag the real Saturday risk: this build assumes your Week-4 judge still clears 90% agreement, and for most people it quietly doesn't after three months of corpus drift — budget the first hour for re-validation or the whole evidence table is decorated randomness (Friday's phrase, and it was aimed at today).

## Further reading

**Must-read**
- `code-lab/6/README.md` — setup, lanes, and the exact commands, before anything else.
- Hamel Husain's field guide, the regression-gate sections — today is that essay, executed.[^6]

**Recommended**
- Anthropic's context-management post — compare their reported eval framing with your report's framing.[^2]
- The Agentset reranker leaderboard, to sanity-check that your Stage-1 pick is still current before you wire it.[^1]

**Optional**
- BM25S paper (arXiv 2407.03618) — why the harness's lexical lane is fast enough to not think about.[^7]

## Citations

[^1]: Agentset reranker leaderboard (zerank-2 / Cohere Rerank v4.0 Pro / Voyage rerank-2.5 / jina-reranker-v3 top tier as of July 2026). https://agentset.ai/rerankers (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Anthropic, *Managing context on the Claude Developer Platform* (Sep 2025): context editing + memory tool; 84% token reduction / +39% combined on their agentic-search evals. https://claude.com/blog/context-management (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Chroma Research, *Context Rot* (Jul 2025) — distractor and haystack-structure effects; the mechanistic case for token budgets. https://www.trychroma.com/research/context-rot (search-verified 2026-07-17)

[^4]: Agentic-lane economics and stop-condition caveats: https://www.marsdevs.com/guides/agentic-rag-2026-guide (3–10× tokens, 2–5× latency) ; https://www.anthropic.com/engineering/multi-agent-research-system (token spend as quality driver; bounded budgets). (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Claude Sonnet 5 intro pricing $2/$10 through 2026-08-31, then $3/$15. https://www.anthropic.com/news/claude-sonnet-5 (vault landscape delta, URL-verified 2026-07-17); https://pricepertoken.com/pricing-page/model/anthropic-claude-sonnet-5 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (2025). https://hamel.dev/blog/posts/field-guide/ (URL-verified in vault refresh 2026-07-17)

[^7]: Xing Han Lù, *BM25S: Orders of magnitude faster lexical search via eager sparse scoring*, arXiv 2407.03618; repo https://github.com/xhluca/bm25s (search-verified 2026-07-17)

[^8]: Anthropic Engineering, *Effective context engineering for AI agents* (Sep 29, 2025), structured note-taking section. https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
