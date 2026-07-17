---
type: lesson
block: block-2-ai-employees
week: week-04
day_of_cycle: 6
day_name: sat
session_slug: building-comprehensive-rag-ai-agent
date_due: 2026-06-13
tags: [rag-evaluation, ragas, llm-as-judge, eval-driven-development, hamel-husain, mt-bench, observability, langsmith, braintrust, arize-phoenix, helicone, regression-gate]
sources:
  - hamel-your-ai-product-needs-evals-2024
  - hamel-field-guide-rapidly-improving-2025
  - hamel-evals-faq-2026
  - ragas-paper-es-shahul-2023
  - ragas-docs-faithfulness-2025
  - ragas-docs-context-precision-recall-2025
  - zheng-mt-bench-arxiv-2306-05685
  - llm-judge-survey-arxiv-2411-15594
  - position-bias-llm-judge-arxiv-2406-07791
  - justice-or-prejudice-arxiv-2410-02736
  - eugene-yan-llm-evaluators-2024
  - jxnl-systematically-improving-rag-2024
  - jxnl-lgtm-at-few-2024
  - braintrust-a16z-investing-2024
  - arize-phoenix-github-2024
  - langsmith-evaluation-docs-2025
  - helicone-ai-gateway-2025
  - deepeval-github-2025
  - mccardel-vanity-evals-linkedin-2025
  - anthropic-red-teaming-2024
last_verified: 2026-07-17
word_count_target: 6000
---

# RAG evaluation — RAGAS, LLM-as-judge, and why most RAG deployments are untested

## Why this matters

By the time you get here, you have a RAG pipeline. You chose a chunking strategy on Thursday, decided between long-context, GraphRAG, and agentic retrieval on Friday, and if you did the exercises you have a working answer-generator stood up against your own corpus. The failure you now need to recognize — and the one that kills 80% of RAG deployments below the waterline — is that you cannot tell whether any of it is working.

"Looks good" is not an evaluation. "The demo convinced the CEO" is not an evaluation. "We have a LangSmith dashboard" is not, in itself, an evaluation. An evaluation is a harness that (a) measures retrieval and generation as separable things, (b) converts human judgment into a repeatable rubric, (c) produces a number that moves up or down when you change the pipeline, and (d) blocks a deploy when a change regresses the number. If you don't have all four, you don't have evals — you have a dashboard, which is a different thing, and which Barry McCardel, the CEO of Hex, memorably labelled "vanity evals" in a widely shared 2025 LinkedIn post that caught the mood of the moment.[^1] The moment is this: every enterprise buyer of an AI system in 2026 has been burned at least once by a pilot that worked in the demo and shipped a 40% hallucination rate to production. The moat around a RAG deployment is no longer "we used Contextual Retrieval and hybrid search" — those are table stakes that Thursday and Friday taught. The moat is "we can prove, with a regression-gated harness, that this answer is 7% more faithful than last week's answer at the same latency and 2x less cost."

By the end of this lesson you will (1) decompose RAG eval into retrieval, generation, and end-to-end task success — and know which benchmarks belong to which layer, (2) be able to state, without cribbing from the docs, the exact formulas RAGAS uses for faithfulness, context precision, and context recall, and the failure modes practitioners have documented against each, (3) have a calibrated view on the LLM-as-judge controversy — where Lianmin Zheng et al.'s 80% human-agreement result holds, where the 2024 bias surveys show it breaks, and the pragmatic Hamel-Husain counter-move of narrow rubric-grounded judges getting >90% on specific tasks, (4) know what eval-driven development looks like when disclosed with numbers — the Nurture Boss 33% → 95% pass-rate jump, the Honeycomb three-iteration alignment to >90% judge-human agreement, the "15–20% higher agreement with example critiques" finding from Hamel's 2025 field guide — and (5) have a defensible build-vs-buy position across LangSmith, Braintrust, Arize Phoenix, and Helicone, plus a regression-gate rule you can paste into CI.

This is the moat. Everything else in Block 2 is commoditizing fast. Evals are what's left.

## Prerequisites

- Thursday's and Friday's RAG content ([[04-thu-rag-fundamentals]], [[05-fri-advanced-rag]]): you know what retrieval-augmented generation is, you have a mental model for hit-rate@k vs answer correctness, and you recognize that long-context and agentic retrieval are alternatives with their own cost profiles. If you skipped those, go back.
- Comfort reading a rubric and a JSON structure. You do not need to write Python — you direct Claude Code to build the harness — but you need to be able to read a failure-log row and tell whether the scoring rubric was the thing that went wrong.

## Layer 1 — Eval decomposition: retrieval, generation, end-to-end

Every RAG eval conversation goes sideways inside five minutes when someone asks "what's your accuracy number?" — because RAG is three systems in a trench coat, and a single number collapses three independent failure modes into a headline that cannot be debugged. The first move in any serious eval design is to decompose the number.

**Retrieval quality.** Did the retriever put the documents that contain the answer into the top-k window? This is a pure information-retrieval problem with a century of metric literature behind it. Hit-rate@k (does the relevant doc appear in the top k results) is the blunt instrument. Mean Reciprocal Rank (MRR) rewards the retriever for putting the relevant doc near the top rather than just anywhere in the window. Normalized Discounted Cumulative Gain (nDCG) extends that to graded relevance when "kind of relevant" is a real category. Jason Liu's February 2024 post *Stop using LGTM@Few as a metric* is the sharpest operator warning on this layer: teams that eyeball the top-5 retrieval window and decide "looks good to me at k=few" are running a metric with sample size 1 and no ground truth, and the number they get is a story about their Tuesday mood, not their retriever.[^2]

**Generation quality.** Given the retrieved context, did the model produce a faithful, relevant, complete answer? This is where faithfulness (does the answer only make claims supported by the context), answer relevance (does the answer actually address the question), and completeness (did it miss parts of the answer that the context supported) live. A retrieval pipeline can have hit-rate@5 of 0.95 and still generate wrong answers — the retriever brought the right passages, but the generator hallucinated a number or ignored the passage and answered from parametric memory. Conversely, a retriever can fail at 0.4 hit-rate@5 and the generator can still produce correct answers on easy queries that don't actually need retrieval. Tracking both independently is how you know which part of the pipeline to invest in.

**End-to-end task success.** Did the user get their job done? For a sales agent, this is "did the reply land an agreed meeting." For a RAG agent over product docs, it is "did the customer stop filing the ticket." This is the only metric the business cares about, and it is usually too noisy, too downstream, and too slow to use as the day-to-day iteration signal. You need the two upstream layers precisely so you can iterate on proxies that correlate with end-to-end success without having to wait for a meeting to get booked.

Eugene Yan's August 2024 *Evaluating the Effectiveness of LLM-Evaluators* post is the cleanest academic-grade treatment of the three layers — the piece argues (and supplies the receipts) that teams routinely conflate retrieval metrics with generation metrics and end up tuning the wrong knob for weeks.[^3] The operator move: keep the three numbers on three separate axes of your dashboard. When one moves, you know which part of the system to touch.

## Layer 2 — RAGAS: the metric math and where it breaks

The RAGAS framework, introduced by Shahul Es, Jithin James, and Luis Espinosa-Anke in their September 2023 arxiv paper *Ragas: Automated Evaluation of Retrieval Augmented Generation*,[^4] presented at EACL in March 2024, is the default "first eval harness" for RAG in 2026 because it is free, open-source, and opinionated — it picks a small set of metrics and tells you how to compute them. For an AI-catalyst lead, the value of knowing RAGAS is knowing to read the metric math, understand exactly what each number measures, and know the three places each metric lies to you — not to install it and trust the numbers.

**Pin your version before you follow any tutorial.** As of mid-2026 RAGAS is at **v0.3.x moving to v0.4**, and the repo has moved orgs to `github.com/vibrantlabsai/ragas` (formerly `explodinggradients`).[^ragasver] The v0.1→v0.2 migration renamed the metric imports (`faithfulness` → a `Faithfulness` class, plus `SingleTurnSample` / `EvaluationDataset` schemas and the deprecation of `ascore`), and v0.4 shifts to an experiment-based architecture — so any code you copy from a 2024 RAGAS tutorial will throw import errors against a current install. Pin the RAGAS version in your harness's `requirements.txt` and follow the migration guide for your target version, or you will spend an afternoon debugging renamed symbols instead of your retriever.

**Faithfulness.** RAGAS extracts the set of atomic claims from the generated answer (call it *S*) using an LLM decomposer, then asks a judge LLM, for each claim *s ∈ S*, whether *s* is supported by the retrieved context. Faithfulness = |supported claims| / |total claims|.[^5] A faithfulness of 1.0 means every atomic statement in the answer is grounded. The three failure modes practitioners have documented:

- *Statement extraction errors.* If the claim-decomposer misses a claim entirely, the unfaithful-but-unmeasured claim never enters the denominator. The RAGAS docs themselves acknowledge "the process of mapping statements can sometimes result in incorrect mappings, where occasionally irrelevant statements might be included, or relevant sentences might not be classified into any of the groups."[^5]
- *Judge permissiveness on partial support.* The judge LLM is asked a yes/no question about support. When the context contains a number like "$1.2 billion" and the answer says "over a billion," a permissive judge scores this as supported and a strict judge as unsupported. Neither is wrong; both will produce different faithfulness scores for the same pipeline. This is the metric gaming the Jason Liu and Jerry Liu camp have warned about — a tuned prompt to the judge can move faithfulness 5–10 points without any pipeline change.
- *Confidently wrong, factually grounded.* Faithfulness measures whether the answer is grounded in the retrieved context. It does not measure whether the retrieved context is *correct*. If your retriever returned a stale version of a policy document, the answer can be 1.0 faithful and 100% wrong. Faithfulness is a necessary but not sufficient condition for correctness — and a team that watches only faithfulness and sees it at 0.94 will ship a confidently wrong system.

**Context precision.** Of the chunks the retriever returned, which ones were actually relevant, and were the relevant ones ranked at the top? RAGAS's formula is Context Precision@K = (∑_{k=1}^{K} Precision@k × v_k) / (total relevant items in top K), where Precision@k = TP_k / (TP_k + FP_k) and v_k is a 0/1 relevance indicator at rank k.[^6] This is a version of the IR community's average precision; it rewards putting relevant chunks near the top. Failure mode: "relevant" is determined by an LLM judge comparing each chunk to the ground-truth answer. If your ground-truth answers are short and the retrieved chunks are long, the judge gets sloppy around "does this chunk support the answer" vs "does this chunk mention a word in the answer," and precision inflates.

**Context recall.** Of the information needed to answer the question (decomposed from the ground-truth answer into atomic claims), how much of it is actually in the retrieved context? RAGAS computes this as Context Recall = (claims in reference supported by retrieved context) / (total claims in reference).[^7] This is the cleanest of the three RAGAS metrics because it has a crisp denominator (the reference answer's claim count) and a crisp question per claim (is it in the retrieved chunks). Failure mode: requires ground-truth answers, which most teams don't have at scale; synthetic generation of ground-truth is itself a research problem and the synthetic-data-is-noisy tax applies.

**The build-vs-buy question RAGAS forces.** RAGAS is 200 lines of orchestration around "ask a judge LLM a series of questions with these specific prompts." It is useful as a baseline, and dangerous as a target. The Hamel Husain position, stated bluntly in his January 2026 *LLM Evals FAQ*, is that "generic evaluations waste time and create false confidence" — prefab metrics measure abstract qualities that are not tied to your specific product's failure modes.[^8] A team in the insurance domain where the dominant failure is "the model quotes a superseded 2022 schedule of benefits instead of the 2025 one" will not have that failure caught by a faithfulness metric — the stale document, once retrieved, makes the stale answer 1.0 faithful. RAGAS is the right place to start. It is the wrong place to stop. Every production RAG deployment with real skin in the game rolls its own metrics on top of (or replacing) RAGAS within the first two months.

## Layer 3 — LLM-as-judge: Zheng's 80%, the 2024 bias papers, and the Hamel counter

The single most important paper for understanding 2024–2026 RAG evaluation is Zheng et al.'s *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, arxiv 2306.05685, v4 revised December 24, 2023.[^9] The paper's load-bearing claim, quoted verbatim: "strong LLM judges like GPT-4 can match both controlled and crowdsourced human preferences well, achieving over 80% agreement, the same level of agreement between humans." That sentence gave the entire industry permission to use LLMs as the grading mechanism. Without it, every eval harness that scales beyond 100 examples would need human annotators, and RAG evaluation would be economically infeasible below Fortune-500 budgets.

The paper also named four biases the same study identified in LLM judges — *position bias* (the order you show candidates to the judge affects the judgment), *verbosity bias* (longer answers score higher, independent of content), *self-enhancement bias* (judges rate outputs from their own model family higher), and *limited reasoning ability* (the judge can be fooled by fluent wrongness when the question requires chained reasoning).[^9] Zheng's own mitigations included running pairwise comparisons in both orders and averaging, and using chain-of-thought prompts for the judge. These are still the baseline mitigations in 2026.

The 2024 arxiv literature then sharpened every part of this picture — mostly by showing that the 80% was a ceiling under ideal conditions and that real deployments land lower unless you design around the biases. The November 2024 survey *A Survey on LLM-as-a-Judge* (arxiv 2411.15594) catalogues the state of the art and its mitigations.[^10] The June 2024 paper *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge* (arxiv 2406.07791) demonstrated that position bias is not random — it varies significantly across judges and tasks, is weakly influenced by prompt length, and is *strongly* affected by the quality gap between the two candidates being compared.[^11] That last finding is the operator bomb: position bias is worst exactly when the two answers are closest in quality, which is exactly the regime where you care about the signal. The October 2024 *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge* paper (arxiv 2410.02736) identified twelve separate biases and proposed the CALM framework to quantify each.[^12] If you had to read exactly one post-Zheng paper before shipping an LLM-judge to production, it is this one.

So: 80% holds in the Zheng setup. It does not hold in 2026 real-world deployments unless you (a) randomize position, (b) control for verbosity by asking the judge to score on content rather than preference, and (c) validate the judge against human labels on a calibration set. The position that Hamel Husain stakes out — and this is the single most-cited operator claim in RAG eval circles in 2026 — is that a *narrow, rubric-grounded, task-specific* LLM-judge can achieve >90% agreement with domain experts, not by ignoring Zheng's biases but by constraining the evaluation surface so the biases have nowhere to express themselves. His Honeycomb query-assistant case study is the canonical example: three iterations of rubric refinement got LLM-judge agreement with a human expert above 90% on a specific task, and adding detailed example critiques to the judge prompt produced "15–20% higher agreement rates between human and LLM evaluations compared to prompts without example critiques."[^13] The trick is narrowness. A general-purpose "which answer is better" judge will hit Zheng's 80% ceiling and no higher. A judge that scores exactly "is this SQL query an accurate translation of the user's intent on a two-point scale, where a point is lost for each hallucinated column or mistaken join" can blow past 90% because the surface area for bias has been engineered out.

**The canonical bar for this week, stated once so the number stops drifting: ≥90% judge–human agreement.** That is Hamel's *published* Honeycomb figure — the empirically-reported point at which teams trusted the judge enough to gate deploys — and it is the number you should carry into Sunday's quiz and flashcards, not the 85% or 95% variants that circulate. Why not higher: pushing a narrow judge to "95%" is not a documented threshold and, at the calibration-set sizes anyone actually hand-labels (20–50 examples), the difference between 90% and 95% agreement is inside the sampling error — a 90%-vs-95% distinction on 20 labels is roughly ±13pp of noise, so it is a false precision. Why not lower: below ~90% the judge disagrees with the expert often enough that gating a deploy on it ships the judge's errors. Calibrate to ≥90% on a task-specific set of ≥20 hand-labeled examples, and treat that as *the* bar everywhere in this week.

This is the live controversy to stake a position on. Position A (Zheng-aligned): LLM-judges are fundamentally reliable enough for production gating, as long as you use pairwise comparison, randomize positions, and run on a held-out set. Position B (Hamel-aligned): LLM-judges are reliable *only* when the rubric is narrow and the judge has been calibrated against humans on a task-specific set of >50 examples; anything less and you are running a vibes-based eval dressed in statistics. The practical resolution most 2026 shops converge on: start with Zheng-style pairwise for breadth (does the new pipeline beat the old one, overall?), then layer Hamel-style narrow rubrics for the specific failure modes your error analysis surfaced. Both, not either.

## Layer 4 — Eval-driven development: Hamel's numbers, laid bare

The phrase "eval-driven development" has become a slogan, so let's ground it in the three specific pass-rate numbers that have come out of Hamel Husain's consulting work across 2024 and 2025. These are the numbers to anchor your own expectations against.

**Nurture Boss, 33% → 95% on date handling.** In Hamel's March 2025 *A Field Guide to Rapidly Improving AI Products*, the case of Jacob at Nurture Boss is walked through step-by-step.[^13] The team was building an AI assistant for the apartment-rental industry. Initial performance felt "okay" in demo. They built a simple viewer to examine conversations between their AI and users, annotated a few dozen, and discovered that the AI was failing 66% of the time when users said things like "let's schedule a tour two weeks from now" — relative date handling was broken. The team fixed that one failure mode with a combination of prompt edits and a small tool-use change. Post-fix, date handling success went from 33% to 95%. The generalizable pattern: error analysis on a small sample (dozens, not thousands) surfaced that the top three failure modes accounted for over 60% of all problems, and fixing those three moved the aggregate number materially. This is eval-driven development — the eval is not the end; the eval is the flashlight that shows you which 3 of 30 possible interventions is the one that matters.

**Honeycomb query assistant, three iterations to >90% judge-human agreement.** The Honeycomb internal AI that translates natural-language questions into query DSL was the testbed for Hamel's LLM-judge methodology. Initial agreement between the LLM-judge and the domain expert was below 70%. Three iterations of the rubric — adding example critiques, tightening the scoring criteria, removing ambiguous cases from the calibration set — pushed agreement above 90%.[^13] This matters because 90% agreement is the threshold at which teams started trusting the judge enough to let it gate deploys.

**Generic prefab metrics vs custom: the null result.** Hamel's January 2026 *LLM Evals FAQ* states plainly: "generic evaluations waste time and create false confidence."[^8] The teams who achieved the 10x iteration speed he cites are not the teams who adopted RAGAS and trusted it. They are the teams who built custom annotation tools, did error analysis on 20–50 real traces, and wrote judges that scored the specific failure modes surfaced. This is the part of eval-driven development that is hard to buy: no SaaS gives it to you because no SaaS knows your domain's failure modes.

**The pragmatic minimum eval set.** Hamel's guidance, consistent across the March 2024 *Your AI Product Needs Evals* piece[^14] and the 2025–2026 field guide and FAQ, is: start with 20–50 real user traces, hand-label them, write three metrics that score the specific failure patterns you see, build a unit-test-style assertion layer (Level 1 in his three-level hierarchy), then a human-plus-model judging layer (Level 2), and only then consider A/B testing in production (Level 3).[^14] The three-level structure matters because Level 1 is where you run on every commit (fast, cheap), Level 2 is where you run on every PR (slower, requires judge), and Level 3 is where you run after shipping (expensive, requires traffic). Most teams try to start at Level 2 and burn their budget on judge calls before they know what they're measuring.

**Regression-gate rule, concrete version — and the sample-size trap it must avoid.** The naive version of this rule is "block any deploy that drops the assertion pass-rate by >2 percentage points." That rule is *broken on a small regression set*, and the trap is worth stating explicitly because this lesson's own "Common failure modes" section (below) warns about it: a binary judgment measured on **N=30** carries roughly **±9pp at 95% CI**, so a 2pp move is pure noise — even on a 200-example set, 2pp is ~4 examples, still inside the sampling error. Gating on a bare point-threshold at those sizes ships noise as signal in both directions.

Two ways to fix it, pick one and pre-register it:

1. **Size the regression set to the delta you want to detect.** To reliably catch a real 5pp regression you want a set of ≥100 examples (±~5pp at 95% CI); to catch a 2–3pp regression you need ≥400. The 30-query set is a *fast smoke check* you run on every commit, not a deploy gate.
2. **Gate on a significance test, not a raw threshold.** Bootstrap a 95% confidence interval on the metric delta (or run a two-proportion test) and block the deploy only when the drop is statistically distinguishable from zero at your chosen N. This lets you keep a smaller set and still avoid gating on noise.

The concrete rule this week recommends: "block any deploy where a bootstrapped 95% CI on the Level-1 assertion pass-rate delta excludes zero on the *downside* (a statistically-real regression), evaluated on a ≥100-example regression set; the 30-query set gates nothing, it only flags candidates for a full run." The discipline that matters: every pipeline change that ships has gone through a gate that could have stopped it, the gate is pre-registered before the change runs, and the gate rule is aware of its own sample size rather than eyeballing a 2pp move on N=30.

## Layer 5 — Observability: LangSmith, Braintrust, Arize Phoenix, Helicone, build-vs-buy

Evals produce numbers on a regression set. Observability produces numbers on production traffic. Both are necessary; they are not the same thing. In 2026 there are four buy options and one build option worth knowing.

**LangSmith.** Harrison Chase's LangChain shipped LangSmith as the commercial observability + eval platform for LangChain-stack applications, and expanded it in 2024 to a standalone offering after LangChain's $20M Series A.[^15] LangSmith lets you create a Dataset (inputs + reference outputs), run your chain against it, score with built-in or custom evaluators, and catch regressions before deploy.[^15] The case for LangSmith: if your pipeline is already LangChain or LangGraph, the integration cost is near-zero and the traces are tagged automatically. The case against: you are locked into Harrison's opinionated schema, the custom-evaluator surface is less flexible than Braintrust's, and pricing above the free tier scales with trace volume.

**Braintrust.** Ankur Goyal's Braintrust raised $36M from a16z and is the highest-opinion platform in the space.[^16] The founder position, from Goyal's public interviews: evals are the new PRD, and teams who implement great evaluations move 10x faster than teams who don't. Braintrust combines prompt playground, dataset management, eval harness, CI/CD integration, and a proxy across OpenAI, Anthropic, Llama, and Mistral in one product.[^16] The pitch lands because Goyal previously built AI development platforms at Figma and Impira and has the scars to know what's actually needed. The case for Braintrust: tightest loop between "change a prompt, run evals, see the delta" in the category. The case against: commercial lock-in, and the 10x-faster number is self-reported marketing (treat as operator anecdote, not independent benchmark).

**Arize Phoenix.** Aparna Dhinakaran's Arize launched Phoenix in April 2023 as the open-source LLM observability library; it is fully self-hostable, OpenTelemetry-based, and vendor-agnostic with built-in integrations for the OpenAI Agents SDK, Claude Agent SDK, and LangGraph.[^17] The case for Phoenix: open-source, OTel, works with anything, deep roots in the traditional ML-observability tradition (Aparna's team came from Uber Michelangelo). The case against: less "opinionated eval harness" than Braintrust; more "put traces in, query them out." The mental model: Phoenix is your observability layer, you write your evals on top.

**Helicone.** Y Combinator W23, open-source LLM observability platform with an AI gateway and proxy model.[^18] Helicone sits in the request path, not as an SDK sidecar — you point your OpenAI/Anthropic client at Helicone's proxy URL and get caching, rate limiting, observability, and prompt management for free, at the cost of a hop. For a solo operator or small team on a budget, Helicone's free tier + self-host option is the cheapest way to get production-grade tracing without writing it yourself.

**DeepEval.** Open-source evaluation framework from Confident AI, Apache 2.0, designed to feel like Pytest for LLM apps.[^19] Fifty-plus research-backed metrics including faithfulness, answer relevancy, contextual precision and recall, hallucination, bias, toxicity. As of 2026 it shipped **DeepEval 4.0**, an *agent-native* eval workflow built for coding-agent loops — iterative patch → eval → retry inside Cursor, Claude Code, and Codex, with a terminal trace TUI — so the old framing of DeepEval as "just an eval library, not a platform" undersells its current shape.[^19] The case for DeepEval: you want evals living in your code repo next to your pipeline, driven from the same agent loop that writes the pipeline. The case against: you still need a place to put production traces, which DeepEval doesn't fully provide.

**The build option.** Write your own. For a sufficiently narrow production problem — say, a single RAG deployment for a single enterprise customer — a custom eval harness is a week of work and the Hamel position above applies: custom annotation tools make teams iterate 10x faster than off-the-shelf because nothing in a general platform matches the specificity of your failure modes.[^8]

**The operator decision tree in 2026.** If your stack is LangChain-or-LangGraph, start with LangSmith and a sidecar of custom assertions. If your stack is anything else and you want the fastest eval-iteration loop, go Braintrust. If open-source + self-host + OTel are non-negotiable, go Arize Phoenix. If you need a proxy that also observes, add Helicone in the request path. If you have a single narrow production use case and a domain expert on the team, build — you will be 10x faster than any platform and the eight hours of Claude Code work is less than a month of Braintrust seat licenses.

## Operator war stories — three, with numbers

**Story 1: The Nurture Boss relative-date fix (the full arc behind the Layer-4 number).** Team of three building an AI assistant for apartment-industry operators. Initial deploy felt "pretty good" in demo. Early user feedback was vague — "it sometimes messes up." The team built a minimal trace viewer (a single Streamlit page showing the user input, retrieved context, and model output for each conversation, with a free-text note field and a 1-bit "failed" toggle). They annotated 40 conversations in a single afternoon. The finding: 66% of conversations involving relative dates ("two weeks from now," "next Tuesday") produced wrong calendar outputs. Before the annotation sprint, the team had been debating whether to swap embedding models. After it, they spent two days fixing the date-handling prompt and tool call. Date handling success went from 33% to 95%. Time-to-insight: one afternoon. Cost: dollars. The punch line: until the trace viewer existed, the team literally could not see the failure pattern that was eating their retention.[^13]

**Story 2: The Honeycomb query-assistant three-iteration alignment (recapped, not re-told).** The Honeycomb natural-language-to-query-DSL judge is the canonical judge-calibration story, taught in full in [[02-tue-prompt-engineering-in-practice]] (Block 0 Week 1) and already summarized in Layer 3 above: an LLM-judge started at ~70% agreement with the domain expert, and three rubric iterations — refine the rubric, add good/bad example critiques (the +15–20pp jump), then drop ambiguous calibration examples — pushed it past the ≥90% bar at which the team trusted it to gate deploys.[^13] The single load-bearing move to carry forward: **the number that matters is judge–human agreement on a task-specific calibration set, and 90% is the trust threshold** — the same ≥90% bar Layer 3 fixed as canonical for this week.

**Story 3: The Anthropic frontier-red-team posture.** Anthropic's public writing on their Frontier Red Team program — on CBRN, cybersecurity, and autonomous-AI risks — is a different kind of eval story but worth knowing.[^20] The 2024 finding reported publicly: Claude's capability on Capture-The-Flag cybersecurity exercises moved from "high schooler level" to "undergraduate level" in a single year. The eval harness here is not RAGAS — it is an external red team of domain experts scoring model outputs against structured attack rubrics, iterated every major release. The cross-domain lesson for a RAG deployment: the expert-in-the-loop scoring loop that Anthropic runs on safety is the same structural loop that Hamel runs on product quality. The specifics differ; the shape doesn't. If your program has no domain experts looking at real traces on a rhythm, then whatever you've built is measuring activity, not quality.

## Cross-domain examples — where this lands for non-engineers

The vault reader might be a marketing ops lead, a healthcare claims analyst, a legal associate, a logistics planner, or a recruiting-ops director. RAG evaluation lands in all of those, differently.

- *Marketing ops RAG over brand guidelines.* Failure mode: the agent generates a social post that uses a deprecated brand voice. The faithfulness metric will score 1.0 because the post is "grounded" in some retrieved brand doc. The real eval you need is a rubric-grounded judge that scores "does this post match the *current* brand voice on these five dimensions, which a brand manager would recognize" — and a regression set of 30 posts approved by the brand manager last quarter.
- *Healthcare claims over policy docs.* Failure mode: the agent cites a 2022 coverage schedule for a plan that was re-issued in 2025. RAGAS's context-recall metric partly catches this if your reference answer is from 2025 and the retriever pulled 2022 docs — the 2022 claims won't support the 2025 answer. But only if your reference answer is actually current. Operator move: bake a date-freshness assertion into Level 1 — if any retrieved chunk has a doc-date > N days older than the query date on policy-change topics, flag.
- *Legal over case-law or contract clauses.* Faithfulness works better here than in most domains because claims are atomic and citations are concrete ("Section 4.2(a) states..."). The gap is completeness — did the answer miss the *also-relevant* clause that's two sections down? Jason Liu's *Systematically Improving Your RAG* discusses exactly this recall-focused problem pattern.[^21]
- *Logistics over operational runbooks.* Failure mode: the agent answers the literal question but misses the escalation path. Eval: "did the answer include the correct escalation contact for this severity level?" is a narrow, binary rubric item — exactly the kind that clears the week's ≥90% judge-agreement bar quickly with calibration.
- *Recruiting ops over candidate notes.* Failure mode: confidently-wrong attribution ("candidate X worked at Y for Z years" from a hallucinated parse). Mitigation: faithfulness at the claim level on structured extractions, with a zero-tolerance gate on factual-claim violations.

The pattern across all five: domain-specific rubric, narrow scope per metric, regression set built from historical ground-truth your domain expert can validate in an afternoon.

## Runnable experiment — the four-phase eval harness

You will direct Claude Code through the full loop. Do not hand-write any of this; this is an orchestration instruction, not a coding exercise.

**Phase 1 — Build the harness.** Paste into Claude Code:

> "Using my Thursday-Friday RAG pipeline as the baseline, build an eval harness with the following structure:
> (a) Two sets: a **30-query smoke-check set** (fast, runs on every commit) and a **≥100-query regression set** (the deploy gate — see Phase 3 for why 30 is too small to gate on), each with ground-truth answer spans, stored as YAML. If I don't supply them, generate synthetically from my corpus using Claude Opus 4.8 and flag every generated item as `synthetic: true` so I can hand-review and correct before use.
> (b) Implement the three RAGAS-style metrics — faithfulness, context precision, context recall — using Claude Opus 4.8 as the judge (the judge should be at least as capable as the pipeline's generator; pin the judge model so a later swap is a separate, recalibrated change). Save the exact judge prompts to a prompts/ directory so I can iterate them.
> (c) Implement a rubric-based pairwise LLM-as-judge that compares a new-pipeline answer against the baseline-pipeline answer on the same query, with position randomization and chain-of-thought prompting per Zheng et al.'s mitigations.
> (d) Output results as a pandas DataFrame and a markdown table, with one row per query and columns per metric, plus an aggregate row and a bootstrapped 95% CI on each aggregate.
> Run the harness on the baseline pipeline and show me the DataFrame."

**Phase 2 — Validate the judge.** Paste into Claude Code:

> "Take 20 rows from the Phase 1 output. I will now hand-label each — for each row, what's the correct answer, and would I score the pipeline's answer as Pass, Partial, or Fail on faithfulness and completeness? [paste your labels]. Compute the agreement rate between my labels and the judge's faithfulness scores. If agreement is <90%, propose three rubric edits (example critiques to add, ambiguous criteria to tighten, scoring scale to rescale) and re-run. Iterate until agreement >90% or I stop you after three iterations."

This is exactly the Hamel three-iteration loop on your own data. Expect the first pass to land 65–80%; expect the third pass, with example critiques and tightened criteria, to cross 90% for most narrow-scope rubrics.

**Phase 3 — Run the regression gate.** Paste into Claude Code:

> "Take each of the four interventions from Thursday-Friday (hybrid retrieval, reranker, contextual retrieval, agentic-retrieval loop) and re-run the full harness on the ≥100-query regression set. Produce a regression table: intervention × metric × delta from baseline × bootstrapped-95%-CI-on-the-delta × latency × cost. Then write a one-page Markdown 'Deploy decision memo' that for each intervention applies this gate: **block only if the bootstrapped 95% CI on any metric's delta excludes zero on the downside (a statistically-real regression), plus no more than 1.5× latency and 2× cost.** A raw 2pp point-drop is NOT a blocker on its own — on N=30 that is inside the ±9pp noise band, which is exactly why we gate on the ≥100-query set with a significance test, not a point threshold. If it passes, recommend ship; if not, specify the blocker and whether it's significant or noise."

**Phase 4 — Write the decision.** 400 words, in your own voice, on: which metric surprised you (moved when you didn't expect), which was noise (moved in ways that didn't correlate with your own intuition when you reviewed traces), which you trust most going forward, and where you'd invest the next eval-development hour. Keep this doc — you will return to it in Week 5's financial-document week.

Expected vs observed: on most corpora the reranker intervention will Pareto-improve (faithfulness up, context precision up, context recall flat or up, latency up). Contextual Retrieval will often improve on larger-context queries and hurt on tiny ones. The agentic-retrieval loop will improve on multi-hop queries and hurt on single-hop (the extra hops add latency and the judge can get confused by the iteration trace). If your observed doesn't match these priors, that is itself a finding — write it down.

## Problem set

1. **Design the minimum viable eval harness** for a real RAG deployment you care about (yours or a client's). Specify: the regression-set size (defend the number), the two Level-1 assertions and two Level-2 judge metrics, the regression-gate rule in CI form ("block deploy if X drops by Y"), and the one failure mode your error analysis surfaced that no generic metric would have caught. Pass: all five specified with one-sentence defenses. Fail: any missing or generic.

2. **Take a position with defense:** "In 2026, LLM-as-judge is reliable enough for production regression gates if and only if [your three conditions]." Cite at least three post-2024 papers or posts (Zheng v4 counts as 2023 but the methodology is in-scope; cite at least two of 2411.15594, 2406.07791, 2410.02736, plus one Hamel post). Two-page maximum; each condition must be defended with specific evidence, not vibes.

3. **Validate an LLM-judge on your own corpus.** Run the Phase-2 loop above on 20 real items from your domain. Report: initial agreement rate, the three rubric edits you made, final agreement rate. Pass: cross 90% by iteration 3. Fail: <90% at iteration 3 with no diagnosis of why (is the task too ambiguous? is the judge model too weak? is the rubric scoring the wrong thing?).

4. **Identify a gamble metric** in your current eval that has high variance and low correlation with user satisfaction. Name it. Explain its failure mode. Propose the replacement metric. Example: "We were tracking `length_of_answer_chars` as a proxy for thoroughness; variance was high and the correlation with user-reported satisfaction was r=0.08. Replacement: a rubric-grounded 'did this answer address all parts of the question' binary score, which tracks r=0.6 with reported satisfaction on our 200-query calibration set."

5. **Build-vs-buy defense, 300 words.** For a solo operator at N=100 queries per day in production, compare RAGAS + a custom judge vs DeepEval vs LangSmith vs Braintrust vs Arize Phoenix vs Helicone. Pick one. Defend with (a) your three most-common failure modes and which platform catches them most directly, (b) the dollar cost at N=100/day for six months, (c) the switching cost if you are wrong. No generic answers.

## Common failure modes at scale

- **The "our faithfulness is 0.94" trap.** Team watches only faithfulness, ships confidently-wrong answers because faithfulness only tests grounding, not correctness. Mitigation: pair faithfulness with a correctness check against ground truth on the regression set, and with a freshness-of-retrieved-docs assertion for time-sensitive domains.
- **Judge drift.** Judge model gets swapped (say Opus 4.7 to Opus 4.8, or Sonnet 4.6 to Sonnet 5) and scores move by 3–5 points on the same regression set with no pipeline change — and note that the current lineup's new tokenizer and re-tuned behavior make cross-generation judge swaps *more* likely to shift scores, not less. Mitigation: version-pin the judge in CI; treat a judge-model change as a separate PR that must be accompanied by a recalibration run against your human-labeled set.
- **Regression-set rot.** Your 30-query regression set was built in January; by June it's stale, the corpus has changed, four of the ground-truth answers are now wrong. Every pipeline change looks like a win against the stale set. Mitigation: quarterly re-validation of the regression set by a domain expert; a "set-age" field on each item.
- **Position bias at close quality.** Pairwise judge reports the new pipeline wins 53-47; you ship. The 6-point margin was entirely position bias — rerunning with swapped positions would have shown 49-51. Mitigation: always run pairwise in both orders and report the average; treat margins <5pp as "no signal."
- **Level-3 obsession.** Team spends three months building A/B testing infrastructure before ever running Level-1 assertions. Launches the A/B test with no pre-registered hypothesis and inconclusive results at N=10,000 users. Mitigation: Level 1 → Level 2 → Level 3 in that order, never out of order. Hamel's explicit rule.[^14]
- **Metric gaming via judge tuning.** Someone tunes the judge prompt for "strictness" to make the new pipeline look better. All numbers go up; user satisfaction doesn't move. Mitigation: judge prompt is versioned, any change requires recalibration against human labels on >20 examples, and the agreement rate is itself a tracked metric.
- **Small-N overconfidence.** N=30 regression set, pipeline moves 7 points, team ships. The real standard error on a 30-sample binary judgment is about 9 points at 95% CI. The "improvement" was noise. Mitigation: bootstrap confidence intervals on every metric; don't ship on non-significant deltas.

## Open questions — what's not settled

1. **Is it possible to train a judge that beats human agreement?** Some research in 2024–2025 (the long tail behind the Survey on LLM-as-a-Judge[^10]) argues that on narrow, structured tasks with fine-tuned judges, judge-human agreement can exceed human-human agreement on the same rubric (humans disagree with each other too, and a well-designed judge can be more consistent than the median human). Operator consequence: in domains where you can afford to fine-tune a judge, the eval-as-moat story gets stronger. Unsettled: whether this generalizes or is limited to narrow domains where consistency matters more than judgment.

2. **How much synthetic eval data is too much?** Hamel's 2026 FAQ recommends starting from real traces because synthetic data carries a known noise tax.[^8] But real-trace volumes are small for new products. The frontier: how to generate synthetic queries + ground-truth that correlate with production without smuggling in the biases of the generator model. Jason Liu's *RAG Playbook* (August 2024) discusses synthetic-question generation for retrieval eval specifically — useful but not settled.[^22]

3. **Does a regression gate at the aggregate level miss per-slice harms?** A pipeline change that raises aggregate faithfulness 3 points while silently dropping faithfulness on the insurance-claims slice by 15 points will pass an aggregate gate and ship a real regression to a specific customer segment. Slice-level gates solve this but multiply the number of gates. Unsettled consensus: how many slice-level gates before the gate set becomes un-maintainable, and what's the mechanism for triaging which slices deserve their own gate.

## Reviewer lens — named critics with specific disagreements

- **Hamel Husain ([hamel.dev](https://hamel.dev)) on Layer 2's treatment of RAGAS.** Husain's 2026 FAQ is blunter than this lesson on generic metrics: "generic evaluations waste time and create false confidence."[^8] He would push back on the framing that RAGAS is "the right place to start" — his line is that RAGAS is where teams *get stuck* and custom annotation tools + error analysis is where the real gains live. The lesson's concession ("RAGAS is the right place to start. It is the wrong place to stop") partially addresses this but Hamel would argue the lesson still overweights the metric math. His counter-position: skip RAGAS, go straight to 20 traces + a trace viewer + a custom rubric, and the team will be faster.

- **Jason Liu (jxnl.co) on the retrieval-eval section.** Liu's 2024 *Stop using LGTM@Few as a metric* post would push back on this lesson's Layer 1 treatment of retrieval-metric choice.[^2] His specific argument: the lesson gives hit-rate@k, MRR, and nDCG equal billing, but in practice most teams should be running recall@k-and-high-k alongside precision-at-top-k because the RAG generator can fix rank ordering within the retrieved window but cannot fix missing-document failures. He would want the lesson to state this as a priority rule, not present the three metrics as a menu.

- **Lianmin Zheng (arxiv 2306.05685) on the LLM-as-judge Layer 3 framing.** Zheng's own paper is careful to present the 80% number with caveats about domain and task.[^9] He would push back on the lesson's sharp "Position A vs Position B" split — his own position is not the strong pro-LLM-judge position the lesson attributes to Zheng-aligned practitioners. The lesson's resolution ("start with Zheng-style pairwise for breadth, then layer Hamel-style narrow rubrics") is closer to Zheng's actual 2024 follow-up writing than the paper's original framing suggests.

- **Shahul Es and Jithin James (RAGAS authors, arxiv 2309.15217) on the critiques of RAGAS.** The RAGAS authors would push back on the lesson's "failure modes" enumeration of faithfulness by pointing out that the metric is designed to be used alongside context precision and context recall, not alone, and that their own docs acknowledge the statement-extraction failure mode.[^4][^5] Their counter: the critique that "faithfulness can be 1.0 and the answer wrong if the retrieved context is wrong" is a feature, not a bug — faithfulness is explicitly a grounding metric, not a correctness metric, and conflating them is a user error the docs warn against.

- **Ankur Goyal (Braintrust) on the observability build-vs-buy section.** Goyal's position, from his public writing and podcast appearances, is that the 10x iteration-speed advantage of purpose-built eval platforms makes "build" the wrong call for 90% of teams.[^16] He would push back on the lesson's "build option" bullet — specifically, the framing that "the eight hours of Claude Code work is less than a month of Braintrust seat licenses" understates the ongoing maintenance, schema-evolution, and team-onboarding cost of a custom harness. His counter: the eight hours is build-cost one; the six months of maintenance is build-cost N, and N is where the math actually breaks.

## Further reading

**Must-read**
- Hamel Husain & Shreya Shankar, *Evals for AI Engineers* (O'Reilly) — the field's forthcoming book of record, publishing **October 31, 2026**; if your thesis is "evals are the moat," this is the canonical text to pre-order.[^evalsbook]
- Hamel Husain, *Your AI Product Needs Evals* (March 29, 2024).[^14] The foundational piece that named the movement.
- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (March 24, 2025).[^13] The numbers (Nurture Boss 33% → 95%, Honeycomb >90% agreement) come from here.
- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, arxiv 2306.05685 v4 (December 2023).[^9] The 80% claim, the four biases, the mitigation playbook.
- Shahul Es, Jithin James, Luis Espinosa-Anke, *Ragas: Automated Evaluation of Retrieval Augmented Generation*, arxiv 2309.15217 (September 2023, EACL 2024).[^4] The metric math, from the authors.

**Recommended**
- *A Survey on LLM-as-a-Judge*, arxiv 2411.15594 (November 2024).[^10]
- *Judging the Judges: A Systematic Study of Position Bias*, arxiv 2406.07791 (June 2024).[^11]
- Eugene Yan, *Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)* (August 2024).[^3]
- Jason Liu, *Systematically Improving Your RAG* (May 2024)[^21] and *The RAG Playbook* (August 2024).[^22]
- Hamel Husain, *LLM Evals FAQ* (January 15, 2026).[^8]

**Optional**
- *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge*, arxiv 2410.02736 (October 2024).[^12]
- Barry McCardel on "vanity evals," LinkedIn (April 2025).[^1]
- Braintrust a16z funding announcement + Ankur Goyal's *Latent Space* interview.[^16]
- Arize Phoenix GitHub + docs.[^17]
- LangSmith evaluation docs[^15], Helicone features page[^18], DeepEval GitHub[^19].

## Citations

[^1]: Barry McCardel, *I'm sorry, but those are vanity evals*, LinkedIn post (April 2025). Used as framing for the distinction between dashboards and evals. https://www.linkedin.com/posts/barrymccardel_im-sorry-but-those-are-vanity-evals-hex-activity-7317617617370763264-I_qo

[^2]: Jason Liu, *Stop using LGTM@Few as a metric (Better RAG)*, jxnl.co, February 5, 2024. On retrieval-eval discipline and why "looks good to me at k=few" is not a metric. https://jxnl.co/writing/2024/02/05/when-to-lgtm-at-k/

[^3]: Eugene Yan, *Evaluating the Effectiveness of LLM-Evaluators (aka LLM-as-Judge)*, eugeneyan.com, August 2024. Three-layer decomposition of RAG eval and LLM-judge reliability. https://eugeneyan.com/writing/llm-evaluators/

[^4]: Shahul Es, Jithin James, Luis Espinosa-Anke, Steven Schockaert, *Ragas: Automated Evaluation of Retrieval Augmented Generation*, arxiv 2309.15217, September 26, 2023; presented at EACL 2024. The original RAGAS paper with full metric derivations. https://arxiv.org/abs/2309.15217

[^5]: RAGAS official documentation, *Faithfulness metric*, docs.ragas.io (accessed April 2026). Exact formula and acknowledged failure modes. https://docs.ragas.io/en/latest/concepts/metrics/available_metrics/faithfulness/

[^6]: RAGAS official documentation, *Context Precision*, docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/ (accessed April 2026). Formula: Context Precision@K = (∑ Precision@k × v_k) / total relevant items in top K. https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_precision/

[^7]: RAGAS official documentation, *Context Recall*, docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/. Formula: (relevant contexts retrieved) / (total reference contexts); LLM-based variant uses claim coverage. https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/context_recall/

[^8]: Hamel Husain, *LLM Evals: Everything You Need to Know (LLM Evals FAQ)*, hamel.dev, January 15, 2026. Source for "generic evaluations waste time and create false confidence," the 20–50 trace guidance, the TPR/TNR framing, and the warning against chasing 100% pass rates. https://hamel.dev/blog/posts/evals-faq/

[^9]: Lianmin Zheng, Wei-Lin Chiang, Ying Sheng, Siyuan Zhuang, Zhanghao Wu, Yonghao Zhuang, Zi Lin, Zhuohan Li, Dacheng Li, Eric P. Xing, Hao Zhang, Joseph E. Gonzalez, Ion Stoica, *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, arxiv 2306.05685, v1 June 9, 2023; v4 December 24, 2023. The 80% human-agreement result and the four biases. https://arxiv.org/abs/2306.05685

[^10]: *A Survey on LLM-as-a-Judge*, arxiv 2411.15594, November 2024, v6 in 2025. Comprehensive catalogue of biases and mitigation strategies. https://arxiv.org/abs/2411.15594

[^11]: *Judging the Judges: A Systematic Study of Position Bias in LLM-as-a-Judge*, arxiv 2406.07791, June 2024. Position bias is strongest at close quality gaps — operator-critical finding. https://arxiv.org/abs/2406.07791

[^12]: *Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge*, arxiv 2410.02736, October 2024. Twelve bias taxonomy and the CALM quantification framework. https://arxiv.org/abs/2410.02736

[^13]: Hamel Husain, *A Field Guide to Rapidly Improving AI Products*, hamel.dev, March 24, 2025 (also published on O'Reilly Radar, April 15, 2025). Source for Nurture Boss 33% → 95% date-handling improvement, Honeycomb three-iteration >90% judge-human alignment, and the "15–20% higher agreement with example critiques" finding. https://hamel.dev/blog/posts/field-guide/

[^14]: Hamel Husain, *Your AI Product Needs Evals*, hamel.dev, March 29, 2024. The three-level hierarchy (Level 1 unit tests / Level 2 human+model eval / Level 3 A/B testing), the sample-size guidance, and the "pass rate is a product decision" framing. https://hamel.dev/blog/posts/evals/

[^15]: LangSmith Evaluation documentation, docs.langchain.com/langsmith/evaluation (accessed April 2026). Dataset + evaluator framework for regression-gating LangChain/LangGraph applications. https://docs.langchain.com/langsmith/evaluation

[^16]: *Production AI Engineering starts with Evals — with Ankur Goyal of Braintrust*, Latent Space interview, 2024; a16z *Investing in Braintrust* announcement (Martin Casado leading the Series A round), October 8 2024. Supports Braintrust's platform positioning — prompt management, real-time serving, model-API proxying, agentic-tool support — and the named-user roster including Notion, Stripe, Vercel, Airtable, Instacart, Zapier, Coda, and The Browser Company. The specific $36M Series A figure referenced elsewhere in the lesson comes from external funding-announcement coverage rather than the a16z post itself. https://www.latent.space/p/braintrust ; https://a16z.com/announcement/investing-in-braintrust/

[^17]: Arize Phoenix GitHub repository, github.com/Arize-ai/phoenix (launched April 2023; continuously updated through 2024–2026). Open-source OTel-based LLM observability with OpenAI Agents SDK, Claude Agent SDK, and LangGraph integrations. https://github.com/Arize-ai/phoenix

[^18]: Helicone AI Gateway and features documentation, helicone.ai (accessed April 2026). Proxy-model observability with caching, rate limiting, prompt management, and self-host option; YC W23. https://www.helicone.ai/

[^19]: DeepEval, confident-ai/deepeval GitHub repository (Apache 2.0). Pytest-style LLM eval framework with 50+ research-backed metrics. https://github.com/confident-ai/deepeval — **DeepEval 4.0 (2026)** adds an agent-native, coding-agent-driven eval workflow (patch → eval → retry loops for Cursor/Claude Code/Codex, terminal trace TUI); changelog https://deepeval.com/changelog/changelog-2026. Verified 2026-07-17.

[^ragasver]: RAGAS version and org state (mid-2026). Repo moved to `github.com/vibrantlabsai/ragas` (was `explodinggradients`): https://github.com/vibrantlabsai/ragas/releases. Current line v0.3.x → v0.4 (experiment-based architecture); v0.1→v0.2 renamed metric imports (`faithfulness` → `Faithfulness` class, `SingleTurnSample`/`EvaluationDataset` schema, `ascore` deprecated) — migration guide https://docs.ragas.io/en/stable/howtos/migrations/migrate_from_v01_to_v02/. Pin the version in `requirements.txt`. Verified 2026-07-17.

[^evalsbook]: Hamel Husain & Shreya Shankar, *Evals for AI Engineers: Systematically Measuring and Improving AI Applications* (O'Reilly). Publishes **October 31, 2026**. https://www.oreilly.com/library/view/evals-for-ai/9798341660717/ ; companion course https://maven.com/parlance-labs/evals. Verified 2026-07-17.

[^20]: Anthropic, *Progress from our Frontier Red Team*, anthropic.com/news (2024–2025). Expert-graded capability evals including the CTF "high schooler to undergraduate" cybersecurity progression. https://www.anthropic.com/news/strategic-warning-for-ai-risk-progress-and-insights-from-our-frontier-red-team

[^21]: Jason Liu, *Systematically Improving Your RAG*, jxnl.co, May 22, 2024. "The only 6 RAG evaluations you need," with recall-focused framing. https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/

[^22]: Jason Liu, *The RAG Playbook*, jxnl.co, August 19, 2024. Synthetic-question generation for retrieval eval, precision and recall decomposition. https://jxnl.co/writing/2024/08/19/rag-flywheel/

_last_verified: 2026-07-17_
