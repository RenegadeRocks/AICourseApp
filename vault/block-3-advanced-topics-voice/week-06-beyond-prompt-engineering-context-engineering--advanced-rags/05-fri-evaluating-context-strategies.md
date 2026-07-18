---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 5
day_name: fri
session_slug: advanced-rags
date_due: 2026-06-26
tags: [evals, retrieval-evals, context-precision, faithfulness, answerability, long-context-evals, nolima, ruler, ablation, judge-agreement, regression-gates]
sources:
  - ragas-metrics-2026
  - nolima-arxiv-2502-05167
  - ruler-arxiv-2404-06654
  - chroma-context-rot-2025
  - hamel-field-guide-2025
  - anthropic-context-management-2025
  - long-context-leaderboards-2026
  - anthropic-multi-agent-research-2025
last_verified: 2026-07-17
word_count_target: 5000
---

# Evaluating context strategies — measuring context-budget changes like an engineer

## Why this matters

This week handed you a dozen dials: trim the system prompt, clear stale tool results, add notes, add a reranker, escalate to an agentic loop. Every one of them can help, hurt, or do nothing on *your* workload, and the vendor numbers attached to each (39% here, 90.2% there, 94.5% somewhere else) were all measured on someone else's. The teams that compound are the ones that treat every context change the way a backend engineer treats a query-plan change: hypothesis, controlled comparison, regression gate. Today builds the measurement layer for context engineering specifically — the retrieval metrics beyond hit-rate, the answerability and faithfulness checks that catch what hit-rate can't, the long-context evals that tell you your model's *real* budget, and the ablation method Saturday's build runs. Without today, Saturday is a pile of plausible upgrades; with it, Saturday is evidence.

## Prerequisites

- [[06-sat-rag-evaluation|RAG evaluation]] from Block 2 Week 4 is the foundation and is not re-taught: RAGAS-style metric mechanics, LLM-as-judge biases and mitigations, and the eval-threshold discipline — **validate your judge to ≥90% agreement with human labels before trusting it** — all live there. Today assumes that harness exists and extends it.
- [[01-mon-context-engineering-the-successor-discipline|Monday]] for NoLiMa/RULER/context rot; [[04-thu-agentic-retrieval|Thursday]] for the tiered architecture we'll gate.

## Layer 1 — Beyond hit-rate: the metric panel for retrieval-in-context

Hit-rate@k answers one question: did a gold chunk land in the top k? Production failure analysis needs a panel, because systems fail in ways hit-rate scores as success. The now-standard core four, popularized by RAGAS and adopted across the 2026 tooling ecosystem, read as a diagnostic matrix:[^1]

| Metric | Question | Failure it catches |
|---|---|---|
| **Context precision** | Of what we retrieved, how much is relevant, and is the relevant material ranked high? | Window stuffed with noise → rot (Monday's tax, measured) |
| **Context recall** | Did we retrieve *everything* needed for the answer? | Partial answers that sound complete |
| **Faithfulness** | Is every claim in the answer supported by the retrieved context? | Fluent hallucination over correct retrieval |
| **Answer relevancy** | Does the answer address the question asked? | Correct, grounded, off-target responses |

Two panel-reading skills separate operators from tourists. First, **read them jointly**: high recall + low precision means your context is bloated (a compaction/reranking problem, not a retriever problem); high precision + low faithfulness means generation is the weak link; everything high + users unhappy means your regression set doesn't represent your traffic. Second, **know that three of the four are judge-computed**, which is why the Week-4 agreement bar is a prerequisite and not a footnote: a context-precision score from an unvalidated judge is a random number with a dashboard.

To the core four, add two that context engineering specifically demands:

**Answerability discipline.** Your regression set must contain queries whose answer is *not in the corpus* — a 10–20% slice is a reasonable start. Score whether the system says "I don't know / not in the sources" versus fabricating. This is a design pattern rather than a packaged metric (RAGAS-adjacent tooling covers pieces of it under noise-sensitivity/refusal labels), and it is the single highest-yield addition most Week-4 harnesses are missing: every architecture this week — bigger windows, memory, agentic loops — *increases* the system's ability to produce a confident answer, so the eval must check whether it also preserved the ability to decline.

**Citation faithfulness.** Stricter than faithfulness: does each cited source actually support the specific sentence citing it? Agentic systems (Thursday) assemble evidence across many steps, so decorative citations are the default failure, not the exception. Sample-audit by hand monthly even after the judge clears the bar; citation-checking is where judges drift quietest.

## Layer 2 — Knowing your real budget: long-context evals as engineering inputs

Monday used NoLiMa, RULER, and Chroma's context-rot report to kill the "1M tokens = free lunch" story.[^2][^3][^4] Today they become inputs to a number you will actually use: the **operating budget** for each model in your stack.

The method, distilled from how the benchmarks themselves define effective length (NoLiMa: longest context retaining ≥85% of the model's own short-context score[^2]; RULER: threshold-calibrated equivalent[^3]):

1. **Pick the task shape that matches your workload**, not the benchmark's. If your agent aggregates across a window (report generation), a needle test overstates your budget badly — RULER's core finding is that aggregation and multi-hop degrade long before simple retrieval does.[^3]
2. **Build a scaled probe set from your own data**: the same 20 tasks at 8K, 32K, 128K, 400K of realistic filler (your documents, not Paul Graham essays — Chroma showed haystack structure changes results[^4]).
3. **Find the knee.** Your operating budget is the largest size holding ≥90% of your small-context score, with margin below the knee.
4. **Re-measure on every model swap.** Rot curves differ by family;[^4] a model upgrade can silently move your knee in either direction, and (per the [[05-fri-context-window-economics|tokenizer note]]) the same documents may not even be the same token count across generations.

Public leaderboards tracking RULER/MRCR/LongBench-class results are useful for shortlisting models and for calibrating skepticism about advertised windows, and mid-2026 analyses continue to show large advertised-vs-effective divergence on multi-fact tasks past ~200K.[^5] But the leaderboard is the *prior*; your probe set is the *posterior*. Ship on the posterior.

## Layer 3 — Ablation methodology: one dial at a time, gates before feelings

The week's additions arrive as a bundle (hybrid! reranker! memory! agentic fallback!), and bundles are where learning goes to die: if v2 beats v1 after five simultaneous changes, you know nothing about which change earned its complexity, and complexity is a recurring cost — every component you keep is something that can drift, break, and demand maintenance. The ablation discipline, which Saturday's harness automates:

1. **Freeze the baseline.** Your Week-4 pipeline, pinned: model version, prompts, index, regression set. Score it fully (the Layer-1 panel + cost + latency). This row never changes.
2. **One intervention per run.** Baseline+reranker. Baseline+compaction. Baseline+memory. Not baseline+both.
3. **Then test the composition you'd actually ship.** Interactions are real — a reranker can shrink the context enough to change compaction behavior — so the final candidate is measured as a whole, *after* the per-dial attribution exists.
4. **Fixed seeds and repeated runs where the loop is stochastic.** Agentic lanes especially: run each query 3× and report spread. A 2-point mean gain inside a 5-point spread is noise wearing a suit. (Recall the pairwise-margin rule from Week 4: margins under ~5 points are "no signal.")
5. **Decide with a pre-written gate, not a post-hoc glance.** Before running: "reranker ships if faithfulness-weighted accuracy gains ≥3 points at ≤400ms added p50 and ≤20% added cost." Hamel Husain's field-guide observation, validated across his 3,000+ students and repeated all over this vault, is that teams who look at numbers *after* deciding what they hope to see ship their hopes.[^6]
6. **Log everything as a table you can re-sort.** Intervention × (panel metrics, answerability, cost/query, p50/p95, tokens). Saturday's harness emits exactly this.

One more discipline specific to context strategies: **ablate downward, too.** The cheapest win this week may be *removing* context — Monday's audit found components with terrible signal-per-token; the ablation table is where "delete the MCP server" gets to compete fairly with "add a reranker." Teams almost never run the deletion rows. Run the deletion rows. (Anthropic's own 84%-token-reduction result for context editing is, structurally, a deletion row that won.[^7])

## Layer 4 — What the vendor numbers would look like as your numbers

A worked translation, to make Layer 3 concrete. Take three claims you met this week and restate each as the experiment you'd run before believing it applies to you:

- **"Memory + context editing: +39% on agentic search."**[^7] Anthropic's eval is *agentic search tasks* in *their* harness. Your version: baseline vs +context-editing vs +memory vs +both, on your 20-query hard lane from Thursday, scored by your validated judge. Expect a smaller number; agentic search is the best case for context management because tool results dominate the window. If your workload is single-shot Q&A, the honest expected effect is ≈0, and measuring it saves you an integration.
- **"Agentic keyword search ≈94.5% of RAG faithfulness, no vector store."**[^8] Your version: the Thursday experiment's 2×2, with faithfulness (not just accuracy) as a scored column, and your corpus's vocabulary-overlap profile written down next to the result. The Amazon result transfers where lexical overlap is high; the whole point of running it yourself is to find out where you sit.
- **"Multi-agent beats single-agent by 90.2%."**[^9] Your version: almost certainly *don't* run it — the honest translation is "breadth-first research tasks with a 15× token budget," which most client workloads aren't. Knowing which vendor numbers *not* to chase is also eval literacy; the decision not to replicate is itself the output of reading the eval's task distribution against yours.

This is the general skill: every published eval number decomposes into (task distribution, harness, judge, budget), and it transfers to you exactly as far as those four match.

## Worked example / runnable experiment — pre-register Saturday

45–60 minutes, Claude Code, producing the one artifact Saturday requires: **the pre-registered ablation plan.**

> Read my Week-4 regression set and eval harness. Draft ABLATION_PLAN.md with: (1) the frozen baseline definition (model, prompts, index, set version); (2) the run matrix — baseline, +hybrid-tuning, +reranker, +compaction/context-editing, +memory-notes, +agentic-fallback, −[worst component from Monday's audit], and the composed v2; (3) for each row, the metric panel we'll record (context precision/recall, faithfulness, answer relevancy, answerability on the not-in-corpus slice, cost/query, p50/p95); (4) my ship gates per intervention, as inequalities, which I will now fill in BEFORE any run; (5) the judge-validation status: current agreement rate, date last validated, and whether the new not-in-corpus slice needs fresh human labels.

Then do the two manual steps that cannot be delegated: write the gate inequalities yourself (they encode your client's economics, not the model's opinion), and label 15–20 not-in-corpus queries by hand so the answerability metric has ground truth. If your judge has never been validated to the ≥90% bar, stop and do that first — it is the load-bearing prerequisite, and [[06-sat-rag-evaluation|Week 4's three-iteration loop]] gets most narrow rubrics there in an afternoon.

## Cross-domain examples — the same discipline in non-engineering clothes

- *Marketing team, brand-voice agent.* The "context strategy" is which brand documents load into the standing prompt. The ablation: three variants (full guidelines, one-page distillation, distillation plus five exemplar posts), judged against a rubric the brand manager pre-approved on 20 labeled posts. Teams that run this discover the one-pager usually wins, which is Monday's deletion lesson wearing lipstick.
- *Finance team, report assistant.* The answerability slice matters most here: a report generator that fabricates a number when the source table is missing is a fireable artifact. The unanswerable queries are cheap to construct (ask about periods before the data starts) and the gate is absolute: answerability failures block ship at any accuracy level.
- *Operations, SOP assistant.* Long-context probe in disguise: as the SOP corpus grew past a few hundred documents, "just put the manual in the prompt" quietly crossed the knee. The monthly probe (same 20 questions, growing corpus) is a ten-minute cron job and catches the degradation before the floor staff does.

The transferable move in every case: pre-approved rubric, labeled slice, pre-registered gate, and a probe that reruns on a schedule. None of it requires the stakeholder to know what a token is.

## Problem set

1. **Panel diagnosis drill.** For each of these signatures, name the most likely fault and the first fix: (a) precision 0.9 / recall 0.5; (b) recall 0.9 / faithfulness 0.6; (c) all four ≥0.85 but user complaints rising; (d) answerability 0.4 with everything else high. One sentence each; mechanism required, not vibes.
2. **Build the unanswerable slice.** Write 15 not-in-corpus queries for your actual corpus across three difficulty tiers: obviously absent, plausibly present, and adjacent-but-different (the corpus answers a *similar* question). Hand-label expected behavior for each. The third tier is where systems fail; if yours doesn't, your tier-3 queries are too easy.
3. **Operating-budget probe, executed.** Run the Layer-2 method at two sizes (your current typical context and 4× it) on 10 tasks. Report the delta and state your provisional knee. This is deliberately smaller than the full method; the point is to have *a* posterior before Saturday.
4. **Gate authorship.** Write ship-gates for all seven Saturday lanes as inequalities with units, including at least one cost gate and one latency gate derived from a real (or realistically imagined) client constraint. Trade them with a cohort peer and attack each other's for gameability: which gate can be passed by a change that makes the product worse?
5. **The vendor-number audit.** Find one eval claim in any AI product's current marketing. Decompose it (task, harness, judge, budget), write down what is undisclosed, and design the two-hour experiment that would test its transfer to your workload. Bonus: run it.

## Common mistakes experts see

- **Metrics without a validated judge.** Three of the core four are judge-scored. Unvalidated judge → decorated randomness.
- **No unanswerable slice.** The regression set only contains answerable queries, so the system's ability to decline is never measured — and every upgrade this week erodes it silently.
- **Bundled interventions.** Five changes, one number, zero attribution, permanent complexity.
- **Benchmarks as budgets.** Shipping at 400K context because a leaderboard said the model "supports" it. Your task shape sets your knee.[^3]
- **Post-hoc gates.** Deciding thresholds after seeing results converts evals into confirmation machinery.[^6]
- **Single runs of stochastic lanes.** One pass through an agentic loop is an anecdote; report spread or report nothing.
- **Never running deletion rows.** The ablation table only ever grows the system. The 84% result was a deletion.[^7]
- **Eval set drift.** The regression set fossilizes while traffic moves. Feed it monthly from real failures (the Week-4 discipline; still true).

## Reflection questions

1. Construct a concrete failure your system could have where all core-four metrics score well. What fifth measurement catches it?
2. Your context-precision score rose after adding the reranker, but answerability *fell*. Tell the mechanistic story of how that happens, and which gate should own it.
3. Why must the operating-budget probe use your documents as filler rather than generic text? Cite the specific Chroma finding that justifies the extra effort.[^4]
4. Write the gate inequality for the agentic fallback lane for a client whose SLA is p95 < 6s and whose margin per query is $0.04. What did you have to learn from Thursday's table to write it?
5. A vendor shows you a bar chart: their memory product, +31% on LoCoMo. Decompose the claim into (task distribution, harness, judge, budget) and write the one-paragraph email asking for what's missing.
6. When is it correct to ship a change that *fails* its pre-registered gate? Who signs off, and what happens to the gate afterward?

## My take (reviewer lens)

**Hamel Husain** would approve of the pre-registration spine but push hard on sequence: this lesson reaches for metrics before *error analysis*, and his consistent field finding is that teams who start by reading 50 real failure traces choose better metrics than teams who start from the RAGAS menu — the panel should be *derived from* your failure taxonomy, not adopted as a standard.[^6] He'd have you do Thursday's trace-reading before writing ABLATION_PLAN.md, and he'd be right about the order. **Ethan Mollick** would question the lesson's implicit population: rigorous ablation is what well-resourced teams do, but his adoption research keeps finding the real-world bottleneck is that most organizations run *zero* systematic evaluation — so the honest advice for a solo operator is a minimum viable version (frozen baseline, one gate, ten labeled queries) that actually happens, over an eight-row matrix that doesn't. The lesson gestures at this with the "manual steps" framing but could be blunter: half this rigor, actually executed, beats all of it planned. **Chip Huyen** would note the missing production half: everything here is offline evaluation, and context strategies drift *online* — compaction behavior changes with conversation-length distribution, memory quality changes as stores grow — so the ablation table needs a monitoring twin (per-lane metrics on live traffic) or Saturday's v2 will be re-fossilized by September. All three critiques converge usefully: evals are a loop through production, not a Friday.

## Further reading

**Must-read**
- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (2025) — re-read the error-analysis-first argument against today's metric-first framing and hold both.[^6]
- NoLiMa §5 + RULER §4 — read the *definitions* of effective length; you're about to compute your own.[^2][^3]

**Recommended**
- A current RAGAS metrics guide for the panel mechanics refresher.[^1]
- Chroma's context-rot report, haystack-structure section, before building your probe set.[^4]
- Anthropic's context-management post — as a model of how to report context-strategy evals (task, harness, delta, caveat).[^7]

**Optional**
- Long-context leaderboards for model shortlisting.[^5]
- Anthropic's multi-agent post, evals section — how they evaluated open-ended research quality.[^9]

## Citations

[^1]: RAGAS core-metric panel (faithfulness, answer relevancy, context precision, context recall) and 2026 ecosystem state: https://docs.ragas.io/ ; guides: https://qaskills.sh/blog/ragas-rag-evaluation-metrics-complete-guide ; https://futureagi.com/blog/rag-evaluation-metrics-2025/ ; https://atlan.com/know/how-to-evaluate-rag-systems-explained/ (search-verified 2026-07-17; metric mechanics taught canonically in [[06-sat-rag-evaluation]]; fetch egress-blocked — liveness pass pending)

[^2]: NoLiMa, arXiv 2502.05167 (ICML 2025): effective length = longest context retaining ≥85% of base score; 32K collapse results. https://arxiv.org/abs/2502.05167 (search-verified 2026-07-17)

[^3]: RULER, arXiv 2404.06654 (NVIDIA): 13 tasks / 4 categories; aggregation and multi-hop degrade before simple retrieval; threshold-calibrated effective length. https://arxiv.org/abs/2404.06654 (search-verified 2026-07-17)

[^4]: Chroma Research, *Context Rot* (Jul 2025): 18 models; degradation varies with needle-question similarity, distractors, haystack structure. https://www.trychroma.com/research/context-rot (search-verified 2026-07-17)

[^5]: Long-context leaderboards and mid-2026 analyses: https://awesomeagents.ai/leaderboards/long-context-benchmarks-leaderboard/ ; https://ofox.ai/blog/long-context-llm-benchmarks-200k-tokens-2026/ (advertised-vs-effective divergence past 200K; single-analysis figures — indicative). (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Hamel Husain, *A Field Guide to Rapidly Improving AI Products*, hamel.dev, March 2025 — error-analysis-first, judge validation, pre-committed criteria; the ≥90% agreement discipline as taught in [[06-sat-rag-evaluation]]. https://hamel.dev/blog/posts/field-guide/ (URL-verified in vault refresh 2026-07-17)

[^7]: Anthropic, *Managing context on the Claude Developer Platform* (Sep 2025): +39% (memory + context editing), +29% (editing alone), 84% token reduction on the 100-turn eval — internal evals, task-specific. https://claude.com/blog/context-management (search-verified 2026-07-17 across two queries; fetch egress-blocked — liveness pass pending)

[^8]: Amazon Science AAAI 2026 agentic-search result (~94.5% of RAG faithfulness, keyword-only), via https://www.startuphub.ai/ai-news/ai-research/2026/claude-code-benchmarking-semantic-search-vs-grep and https://buzzgrewal.medium.com/ai-agents-dont-need-vector-search-anymore-inside-the-agentic-search-stack-replacing-rag-in-2026-58efcabe4f6f (search-verified 2026-07-17; secondary coverage; fetch egress-blocked — liveness pass pending)

[^9]: Anthropic Engineering, *How we built our multi-agent research system* (Jun 2025): 90.2% internal-eval delta; ~15× tokens; task-distribution caveats in the post itself. https://www.anthropic.com/engineering/multi-agent-research-system (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
