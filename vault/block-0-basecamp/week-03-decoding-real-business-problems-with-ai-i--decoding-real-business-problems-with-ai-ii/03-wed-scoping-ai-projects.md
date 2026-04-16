---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: 3
day_name: wed
session_slug: decoding-real-business-problems-with-ai-i
date_due: 2026-05-13
tags: [scoping, mvp, walking-skeleton, kill-criteria, eval-gates, cost-model, agile-eval, llm-as-judge, rag, agent-economics]
sources:
  - husain-field-guide-2025
  - husain-evals-faq-2026
  - husain-llm-judge
  - husain-evals-skills-coding-agents
  - yan-evals-that-work
  - yan-eval-process-2025
  - shankar-2024-validators
  - gartner-agentic-cancellations-2025
  - hbr-why-agentic-ai-fails-2025
  - mit-nanda-state-of-ai-2025
  - intuitionlabs-llm-pricing-2025
  - zylos-token-economics-2026
  - microsoft-foundry-fine-tuning-ignite-2025
  - anthropic-applied-ai-engineering
last_verified: 2026-04-15
word_count_target: 6000
---

# Scoping AI projects — walking-skeleton MVPs, kill criteria, eval gates, and the cost model you have to build before you start

## Why this matters

Your job, if you are a catalyst lead and not just a prompt engineer, is to decide what to ship, what to kill, and when to kill it. Everything else — evals, cost curves, retrieval precision, fine-tune vs prompt, human fallback design — is downstream of that one decision.

In April 2026 that decision is much harder than it looks, and much easier than the industry is making it. It is harder because frontier capability shifts every six weeks, which means a scoped project can become obsolete before it reaches staging. It is easier because a short list of people (Hamel Husain, Shreya Shankar, Eugene Yan, the Anthropic Applied AI team, the OpenAI cookbook maintainers) have converged on a single operational pattern — *walking skeleton with eval harness, hard eval gates, weekly iteration, ruthless scope discipline* — that works. If you adopt that pattern you will kill projects faster, ship the survivors faster, and spend roughly half what your peers spend doing it.

MIT's State of AI in Business 2025 report — the one everyone has been quoting for the "95% of GenAI pilots fail" stat — explicitly traces the failure pattern to scope and integration, not model quality.[^10] Gartner projects that over 40% of agentic AI projects will be cancelled by end of 2027, and their stated reasons are the ones this lesson is about: unclear business value, cost surprises, absent risk controls.[^8] HBR's October 2025 analysis of agentic failures lands on the same cluster: no measurable outcome, no kill trigger, no end-state definition.[^9]

This lesson gives you the scoping pattern, the eval-gate thresholds to wire into it, the cost model to build before you commit an engineer, and the kill criteria to pull the plug on. You will leave with a one-page scope doc for a real project on your plate.

## Prerequisites

- [[01-mon-prompting-first-principles]] — you need the mechanical model of what a prompt is doing, or your evals will measure the wrong thing.
- [[week-02]] exercises on problem decomposition (pending) — the problem has to be decomposable before it's scopable.
- Operational exposure to at least one production AI system you or your team have shipped or tried to ship. The examples in this lesson will land differently if you've watched a project limp through eval drift in real time.

## Part 1 — The AI-MVP frame vs classic lean-startup MVP

### What changed, exactly

The classic lean-startup MVP is a deterministic artifact. You ship the smallest feature set that tests a market hypothesis, you measure sign-ups or retention or willingness-to-pay, and you iterate on the feature set. The variance you're managing is *market variance*: does the customer want this.

An AI MVP has a second variance source that lean startup does not model: *capability variance*. The product's behaviour depends on a stochastic function (the model) conditioned on a changing environment (retrieval state, tool responses, upstream documents, user phrasing). You are not only asking *"do users want this?"* — you are simultaneously asking *"does the system even do the thing, reliably, at the cost point that makes it worth doing?"*

This is why the naïve translation — *"ship a Streamlit prototype, show it to five customers, see what they say"* — consistently misleads AI teams. Five customers testing a demo will tell you whether the *idea* resonates. They will not tell you whether the system works at the p90 of real-world inputs, which is where it lives or dies. Capability variance dominates market variance in the early months, because a system that hits 70% quality on demo inputs and 20% on tail inputs will burn through a customer cohort before you've measured retention.

Hamel Husain, who has embedded with 30+ companies shipping AI products, keeps coming back to this point in his *Field Guide to Rapidly Improving AI Products*: the teams that succeed "barely talk about tools at all" and instead "obsess over measurement and iteration."[^1] The ones that fail are the ones that shipped a demo, collected vibes-based feedback, and assumed the next iteration would close the quality gap. The gap is almost never closeable by "prompt better." It's closeable only by the eval-driven loop that the AI-MVP frame is designed around.

### The walking-skeleton-with-eval-harness pattern

A walking skeleton, in Alistair Cockburn's original sense, is a tiny end-to-end implementation that touches every architectural layer — UI, application logic, data, integrations — but does almost nothing. It's the thinnest possible system that still runs. For AI, the walking skeleton has five layers, not four, and the extra layer is the one most teams skip:

1. **Input path** — the one way a real user gets a real query into the system.
2. **Model/retrieval path** — the actual LLM call (not a canned response) against the actual retrieval or tool layer.
3. **Output path** — the actual surface the user reads or the downstream system consumes.
4. **Observability** — every call logged with inputs, outputs, latencies, token counts, tool traces. Non-negotiable.
5. **Eval harness** — a test set of 20–50 real (or synthetic-from-real) inputs with graded outputs, runnable with one command, producing a pass/fail against named thresholds.

If you cannot run the eval harness on commit, you do not have a walking skeleton. You have a demo. The distinction is not semantic — it is the difference between a project that can be debugged and one that can only be prayed over.

Eugene Yan's formulation is the crispest I've seen: *"Label data, align evaluators, build an eval harness."* Three steps, in that order.[^5] You don't start with the eval framework; you start with 20 labelled examples of what "good" and "bad" actually mean on your specific problem, then you tune an evaluator (rubric, LLM-as-judge, classifier) until it agrees with your labels, *then* you wire that evaluator into a harness that runs on every change. Teams that invert this order — frameworks first, labels last — end up with evals that correlate with nothing the user cares about.

Shreya Shankar's UIST 2024 paper *Who Validates the Validators?* is the load-bearing academic citation for this ordering. Her team documents a phenomenon they call *criteria drift*: the criteria you think you want for evaluation are partly dependent on the outputs you observe. You need to grade examples to define the criteria, but you need the criteria to know what to grade. The only escape is iterative: grade, extract criteria, refine judge, re-grade, repeat.[^7] This is not a cost to absorb — it is the work.

### Why "prototype first, eval later" loses in 2025–2026

This is the live controversy. There is a well-argued position — you hear it in YC batches, in early-stage AI startup threads, at founder dinners — that says: in 2026, model capability is moving fast enough that you should prototype first, get the user response, and only invest in evals once you know the product has legs. The argument isn't stupid. Evals have real setup cost. If the product idea is wrong, the eval infrastructure is wasted.

I think this position is wrong at L3, and I'll explain why.

The prototype-first argument assumes that the bottleneck for an AI product is *idea validation*. In 2022 that was true. In 2026 it isn't, because the idea space is saturated. For almost any AI product you can think of today, there are at least three competitors doing a version of it. The actual bottleneck is *differentiating quality* — reliability at the tail, cost structure, latency, tool-call success rate, accuracy on the 10% of queries that break the demo. You cannot validate any of that without evals. So "prototype first" in 2026 means you validate the wrong variable (demo-quality resonance) while the variable that decides the company's fate (tail quality) goes unmeasured until series-A due diligence pries it open.

The Husain-Shankar-Yan consensus — eval harness in the walking skeleton, not bolted on later — is the position I take, and the position this lesson will back. If you disagree, you owe yourself the exercise of scoping the counter-position: what does a team that skips the eval harness actually have in month six? In my observation of 2025 post-mortems, it has a polished demo, a confused customer, and a founder arguing that "our next fine-tune will fix this." Kill criterion absent. The next fine-tune does not, in fact, fix it.

## Part 2 — Kill criteria: the scoping artifact nobody writes until it's too late

### The Husain frame

Hamel Husain is, as far as I can tell, the industry's most consistent voice on this. His framing, paraphrased from the *Field Guide* and *Evals FAQ*: you cannot ship a good AI product without an eval. You cannot build a good eval without error analysis on real data. You cannot do useful error analysis without a scope tight enough that a single evaluator can hold the quality bar in their head. If the scope is so broad that you need five subject-matter experts to decide whether a single interaction was good, you have a scoping problem, not an eval problem.[^2]

From this falls the operational principle: **before you build, write down what would cause you to stop building.** Not vibes. Not "if it's not working we'll figure it out." Specific, numerical, pre-committed.

A kill criterion has three parts:

1. **A metric** that is measurable on a named data slice with a named evaluator.
2. **A threshold** that the metric must exceed (or fall below, for cost/latency) by a named checkpoint.
3. **A decision** that is pre-committed to if the threshold is missed — pivot scope, change architecture, defund, hand back to the human workflow.

Example, badly written: *"If the model isn't good enough by end of Q2, we'll reconsider."* This is not a kill criterion. It's a feeling.

Example, well written: *"By week 6 post-kickoff, LLM-as-judge accept rate (calibrated against 120 human-labelled examples, Cohen's κ ≥ 0.7) on the invoice-coding task must reach 85% on the hard-case slice (N=200), or we cancel the project and recommend the client extend the current rule-based pipeline for 12 months."* That's a kill criterion. Metric named, evaluator calibration named, slice defined, threshold quantified, decision pre-committed.

### How Anthropic's Applied AI team appears to scope internally

I say "appears to" because Anthropic's Applied AI team has not, as of this writing, published a single canonical blog post on their scoping methodology.[^14] What has appeared in public — engineering talks, the Anthropic engineering blog, conference presentations from Alex Albert and team members — consistently shows the same pattern: every customer engagement starts with a bounded problem, a named golden dataset (usually 50–200 examples), explicit thresholds, and an exit condition. If the thresholds aren't reachable inside the scope, scope contracts or project ends. They do not ship features that can't be evaluated, and they do not run eval-less pilots.

This is the inverse of the standard enterprise pattern, which is *"boil the ocean with a flagship AI initiative, measure vibes, report to the board, rinse."* The Applied AI pattern treats every engagement as a bounded scientific experiment with a stated hypothesis and a stated refutation condition.

The generalizable rule: **no named refutation condition, no project.**

## Part 3 — Eval gates: which thresholds actually gate investment

Not every eval belongs in the scope doc. Most of them don't. An eval gate is a specific kind of eval: one tied to a funding/scope decision, measured at a named checkpoint, with a pre-committed consequence. Here's the L3 view on which gates are worth hard-wiring for which project types.

### Retrieval precision@k (RAG projects)

For any retrieval-augmented system, your gate is *precision@k at the chunks-fed-to-the-model level, not at the document level*. Document-level precision is an old IR habit and it lies to you: a retriever that pulls the right document but the wrong chunk-within-document will score well on document precision@k and cause your generator to hallucinate anyway.

Suggested gate structure for a first-pass RAG MVP on internal enterprise documents (operator thresholds, consistent with Anthropic's contextual-retrieval eval protocol and the Husain/Shankar 2025 writing on retrieval-first gating; not a published benchmark — calibrate up or down based on your failure-cost asymmetry):[^ret-gate]

- **P@5 ≥ 0.8** on the chunks level, measured against 100 labeled query→chunk pairs.
- **Recall@20 ≥ 0.95** on the same set. (If you can't retrieve the right chunk in the top 20, no reranker saves you.)
- **Grounding rate ≥ 0.9** — the LLM-as-judge, calibrated against humans, rates generated answers as grounded in the retrieved context.

Miss any of the three at the 4-week checkpoint → you don't graduate to production pilot; you rescope retrieval (different chunker, different embedding, different query rewriter, hybrid search) or you kill the project.

Frontier practice (per Anthropic's contextual retrieval work and multiple 2025 RAG post-mortems) shows that teams without this gate ship RAG systems that look fine on demo queries and catastrophically hallucinate on the long tail — the *80% RAG failure rate* figure circulating in 2025 traces to MIT Media Lab's NANDA initiative *State of AI in Business 2025* report, which found roughly 95% of enterprise generative-AI pilots producing zero measurable P&L impact, a population dominated by teams who never gated on retrieval quality as a prerequisite to generation quality.[^10][^9]

### Tool-call success rate (agentic projects)

For any agentic system that calls tools — APIs, databases, code, search — the load-bearing metric is not task completion. It is *per-step tool-call success*. If your agent has an average 10-step trajectory and each step has 92% tool-call success, your end-to-end task success is 0.92^10 ≈ 43%. Tool-call failures compound.

Suggested gate structure:

- **Per-call tool success ≥ 0.97** on a fixed 50-trajectory replay set.
- **Trajectory-level task completion ≥ 0.7** at fixed budget (max N steps, max $ cost).
- **Recovery-after-error rate ≥ 0.5** — when a tool call fails, how often does the agent recover and continue productively rather than spiral.

The third metric is the one most teams miss, and it's the one that separates a demo-quality agent from a production-quality agent. Husain's 2026 *Evals Skills for Coding Agents* post makes this point at length for Claude Code and Codex agents: per-call success is the easy metric; recovery is where the real intelligence shows.[^4]

### LLM-as-judge agreement (generation quality, open-ended tasks)

For subjective quality on open-ended outputs — writing, summarization, classification with soft labels — the gate is not "does the judge approve?" It is *does the judge agree with humans well enough that its approvals are meaningful*.

Shankar et al. quantify this:[^7] Cohen's κ or a comparable agreement metric between your judge and your human labels needs to clear a named threshold before the judge's scores can be trusted as an eval gate at all. A judge running at κ = 0.4 is not a judge; it's noise.

Suggested gates:

- **Judge-to-human agreement κ ≥ 0.7** on a 100-example calibration set, *before* the judge is used for gating.
- **Human-validated accept rate ≥ 0.85** on a hard-case slice, measured at week 4, 8, 12.
- **Drift check**: every 4 weeks, re-run the calibration set and confirm κ hasn't drifted below 0.6. If it has, the judge needs re-alignment or the production data has shifted in ways your rubric no longer describes.

The *criteria drift* phenomenon Shankar documented means judges silently go out of calibration as your product surface changes. If you don't schedule re-calibration, your eval harness lies to you by month four.

### Human-in-the-loop accept rate (ship-behind-a-human projects)

For systems that route to a human (legal drafting, clinician-facing medical summarization, compliance review) the gate is *accept-without-edit rate* and *edit-distance-when-edited*. A system with 70% accept-as-is and an average edit distance of 30 tokens on the rejected 30% is a genuine productivity win. A system with 95% accept rate but an average edit distance of 300 tokens when rejected is suspicious — humans may be accepting outputs they shouldn't, and you're measuring effort-saved, not quality.

## Part 4 — The cost model you have to build before you commit

If you start building before you've costed, you are not scoping; you're gambling. Here is the cost model in the form I use when advising catalyst leads. Fill in the blanks *before* the walking skeleton ships, not after.

### Cost surface 1 — Token costs (inference)

Per-query cost = (input_tokens × input_rate) + (output_tokens × output_rate), summed over the call graph. For agentic systems multiply by expected trajectory length. Don't forget: retrieval call context, tool-call arguments, intermediate reasoning tokens, and reflection turns all count.

As of April 2026, the spread is large:[^11] Claude Opus 4.5 and GPT-5-class models sit at $10–15/M input, $50–75/M output; Sonnet/Haiku-class and GPT-5-mini in the $1–3/M range; Grok, Gemini Flash, open models under $0.50/M. For agent trajectories averaging 30k tokens in / 6k out, per-trajectory cost ranges from $0.02 on cheap models to $0.75 on frontier. Multiply by expected monthly trajectory count, add a 2× safety factor for the retry/error path you haven't budgeted for yet.

### Cost surface 2 — Eval-run costs

Most teams underestimate this by 10×. You will run evals on every prompt change, every model change, every retrieval change. If your eval set is 500 examples and you re-run it twice a week, that's 1000 runs/week × your full trajectory cost. For a frontier-model agent that's $750/week on evals alone. Over a 12-week scoping window: ~$9,000. This is fine — but only if you've budgeted for it. Zylos' 2026 token-economics research has compiled multiple production post-mortems where eval costs hit 20–30% of total inference spend during active development.[^12]

### Cost surface 3 — Human annotation costs

You need real labels. At senior-analyst rates ($80–150/hr fully loaded), 200 labeled examples at 3 minutes per label is ~10 hours, ~$1000–1500. Plan for 3–4 rounds of labeling (criteria drift) over the scoping window. Budget $5–8k in annotation across the project lifecycle. Teams that skip this are teams whose LLM-as-judge was never calibrated and whose evals are decoration.

### Cost surface 4 — Fine-tuning costs (if applicable)

As of late 2025, Microsoft Foundry and OpenAI's fine-tuning prices are low enough that a fine-tune is often cheaper than a prompt engineer's month.[^13] Training a GPT-4.1-mini fine-tune on 10k examples is ~$100–500 in training; serving adds a 50% premium on input tokens for OpenAI but no premium on Gemini 2.0 Flash tunes.[^11] The non-obvious cost is *re-tuning cadence*: when the base model version deprecates, you re-tune. Budget for 2–3 re-tunes over a 12-month product lifecycle.

### Cost surface 5 — Fallback-to-human costs

Every user-facing AI system has a failure tail. Either you budget for human fallback explicitly (a support rep picks up when confidence is low) or you pay for it implicitly in churned users. A 10% fallback rate at $4/handoff adds $0.40 per user interaction. For a system doing 100k interactions/month, that's $40k/month — which can swamp your inference spend.

The combined cost surface is the number the scope doc needs. *"This project is viable if per-interaction fully-loaded cost is ≤ $X and LTV is ≥ $Y."* That ratio is your scope's economic kill criterion, on top of the quality kill criteria. If the math doesn't work, the project doesn't ship, no matter how good the demo looks.

## Part 5 — Scope creep patterns specific to AI (and why each one is a latent cost explosion)

Three scope-creep phrases, each of which sounds innocent and each of which detonates the cost model.

**"Just add RAG."** Naïve framing: it's a retrieval call, it's fast. Real cost: you now have a retrieval system to evaluate (retrieval precision@k is a whole eval regime), a chunking strategy to maintain, an embedding model that silently deprecates, ingestion pipelines for ongoing document updates, stale-data invalidation, per-query retrieval cost, and a new failure mode (the retriever pulls the wrong chunk and the model confabulates confidently). RAG is never "just" anything. If you're scoping RAG, assume 30–50% of the engineering cost of the project will be retrieval quality, not generation quality. The 80% RAG failure stat is real and it's dominated by teams who under-scoped the retrieval problem.[^9]

**"Add multi-modal."** Naïve framing: the model now supports images, we just pass images in. Real cost: your eval set triples (you now need image-input test cases, OCR test cases, chart-reading test cases, screenshot test cases). Input token counts for images can be 1000–3000 per image; cost per query can 5–10×. Your judge has to be re-calibrated for vision outputs. Your annotation cost doubles because reviewers need longer to grade image-grounded outputs. Multi-modal is a new project, not an increment.

**"Make it agentic."** Naïve framing: let the model plan and use tools, it'll generalize. Real cost: trajectory length multiplies token spend by 10–50×. Tool-call success rate gates are hard to hit (0.97 per-call for a reliable system). Recovery behavior has to be engineered, not assumed. Latency becomes a UX problem (agents that take 90 seconds break flows). Failure modes multiply (each tool has its own failure surface). HBR's October 2025 piece on agentic failures shows that the single biggest predictor of agentic project cancellation is teams who went agentic before they had a working deterministic pipeline; Gartner's cancellation projection points the same direction.[^8][^9]

The common pattern: each of these phrases is proposed mid-project as a "small addition." Each one, in practice, resets the cost model, the eval regime, and the timeline. The scope doc should explicitly enumerate which of these are in-scope (with their cost impact called out) and which are explicitly out-of-scope for this MVP. Saying "out of scope" on paper, signed by the sponsor, is worth more than any architectural decision.

## Part 6 — The agile-eval loop: cadence discipline

The pattern most successful teams converge on, per Husain's field guide and Yan's process posts:[^1][^6]

- **Weekly eval runs** on the full eval set, on every significant change (prompt, model, retrieval, chunker). Automated, scheduled, logged.
- **Weekly error analysis session** — 30–60 minutes where the team reviews the 20 worst-scoring outputs from that week's run. Not all failures; just the worst 20. Categorize: is this a prompt failure, a retrieval failure, a model ceiling, an eval bug?
- **Biweekly judge calibration check** — re-run judge against a held-out human-labeled slice. Watch κ.
- **Four-weekly checkpoint against kill criteria** — formal yes/no against named thresholds. Documented. Sponsor visible.

The cadence is the discipline. Teams without cadence slip into *"we'll fix it next week"* drift, which is how 12-week scopes become 9-month engagements with no clear exit. Yan's line: *"An LLM-as-Judge Won't Save The Product — Fixing Your Process Will"* is pointing at exactly this.[^6]

## Part 7 — Operator war stories

### Scoping success: the insurance-claims summarizer that got killed fast

(Composite/illustrative, built from patterns observed across 2025 claims-AI engagements; numbers are representative, not a single identifiable customer.) A US insurance firm scoped a claims-summarization tool for adjusters. The walking skeleton ran against 120 real claims (PII-scrubbed). The gate was an LLM-as-judge (κ 0.74 against adjuster labels) rating *"would a senior adjuster accept this summary as-is or with minor edits."* Kill criterion: 80% accept by week 6, or stop. At week 4 they were at 62%. Error analysis showed the failure was concentrated in long claims (>30 pages) where retrieval was pulling irrelevant sections and the model was over-summarizing material parts. They rescoped to "claims under 15 pages, structured types only" — 60% of the original volume — and re-ran the gate. Hit 84% at week 8. Shipped.

The kill criterion didn't kill the project. It killed the *failing version* of the project fast enough that there was still budget to ship a successful narrower version. The team that rigidly defended the original scope would have burned through the budget trying to fix long claims and shipped nothing.

### Scoping failure: the legal-memo drafter that burned nine months

A mid-sized law firm, same period. Scoped a generative memo drafter across three practice areas (litigation, corporate, real estate) with "we'll evaluate partner satisfaction quarterly" as the quality bar. No hard thresholds. No kill criterion. Eval set was "partners will tell us if it's bad."

What happened: each practice area had different quality standards and different document structures. Partners told the team it was "not quite there" for 9 months. Token spend exceeded budget by month 4. No one pulled the plug because no one had pre-committed to pulling the plug. Eventually the engagement was quietly wound down and attributed to "the technology not being ready yet." The technology was, in fact, ready. The scoping was never there.

HBR's analysis across the 2025 cohort of agentic-AI failures shows this exact pattern — absence of measurable outcome, absence of end-state — as the dominant failure mode, not model capability.[^9] MIT's report reinforces it: the 95% failure rate is a scoping failure, not a technology failure.[^10]

## Common mistakes experts see

- **Scoping the project before labeling any data.** You cannot scope what you cannot measure. Label 50 examples before you write the scope doc. The scope doc will get better, or the project will reveal itself as impossible, which is also a win.
- **Confusing demo quality with tail quality.** A system that wows on five curated inputs will die on the 95th percentile. Always eval on the long tail.
- **Using an LLM-as-judge without calibrating it.** Uncalibrated judges produce numbers. Numbers feel like progress. They are not.
- **Writing kill criteria that are unmeasurable.** "If it's not working" is not a kill criterion. Name a metric, a slice, a threshold, a date.
- **Skipping the cost model.** Post-hoc cost discovery is how projects that hit quality still get killed by finance.
- **Treating "agentic" as a free upgrade.** It's a 10–50× token spend increase and a new eval regime.
- **No cadence.** Weekly evals, weekly error analysis, monthly checkpoints. The cadence is the process.
- **Re-scoping to preserve sunk cost rather than pivot on new information.** If the kill criterion fires, it fires. Don't move the goalposts — move the scope.

## Exercise: Write a 1-page scope doc (artifact-producing)

Pick a real AI project on your plate — one you're considering, scoping, or running. Produce a single-page document with exactly these five sections. No more.

**1. Problem statement (≤100 words).** Who the user is. What they do today without AI. What specifically we expect the AI to do for them. The business metric this moves.

**2. Walking-skeleton definition (≤150 words).** The thinnest end-to-end system: input path, model/retrieval path, output path, observability, eval harness. Name the 20–50 labeled examples you will build against. Name who will label them.

**3. Three eval-gate thresholds with go/no-go decisions.** For each: metric, evaluator (and if LLM-as-judge, the human-calibration κ required), data slice, threshold value, checkpoint date, pre-committed decision if missed. These are the kill criteria.

Template row:
- Gate 1: [metric] on [slice N=X] measured by [evaluator, κ ≥ Y] must hit [threshold] by [week W]. If missed: [rescope to _____ / kill / escalate].

**4. Estimated token/eval/human cost for the scoping window.** Per-interaction token cost, eval-run cost per week, human annotation cost for labels, total for the 12-week scoping window. One number at the bottom: fully-loaded cost per scoped interaction.

**5. Out-of-scope list.** Three to five features or directions explicitly excluded from this MVP. "Not doing multi-modal." "Not doing agentic." "Not doing second practice area." Signed by the sponsor.

The one-page limit is the point. If the scope doesn't fit on one page, the scope isn't scoped. Share the doc with one peer and one skeptic before you build a line of it.

Self-check when done: can a smart stranger read your scope doc and predict within 10% whether the project will succeed? If not, your gates aren't specific enough.

## Reflection questions

1. You've just written your scope doc. Three weeks in, a new frontier model ships and your quality metric jumps from 0.72 to 0.86 at no extra cost. Do you keep the original kill criterion or raise the bar? Defend whichever side you pick.
2. Your LLM-as-judge has κ = 0.71 against humans, comfortably above your 0.7 threshold. But the 29% disagreement is concentrated in the highest-value cases. Is your judge good enough? What would you do before week 4 checkpoint?
3. A stakeholder asks you to add multi-modal support "since the new models all do it." Your MVP is 6 weeks in, week 10 checkpoint is in 4 weeks. How do you respond in writing?
4. Your week-8 checkpoint misses the kill criterion by a small margin (82% vs 85% threshold). The team has a plausible theory about a fix that would take 2 more weeks. Do you extend, rescope, or kill? What would a rigid Husain-style discipline say; what would a capability-optimist say; which do you side with and why?
5. You're advising a team whose scope doc has one eval gate: "overall user satisfaction >4.0/5." What do you change, in order of priority, and why?
6. Walk through the cost model for an agentic coding assistant that averages 50k tokens input / 10k output per task at Opus pricing, used 200 times/day by a 30-person engineering team. At what monthly spend does the project need to show productivity gains, and how would you measure those gains as a kill criterion?

## Reviewer lens — where specific experts would push back

**Hamel Husain would probably push back on:** the way I've framed LLM-as-judge thresholds here. His consistent public position is that for many product problems, a good judge is a fine-tuned binary classifier on a narrow failure mode, not a generalist rubric-grader. "Judge-to-human κ ≥ 0.7" as a universal threshold oversimplifies — for the failure modes he grades, he'd want closer to 0.85 on specific binary categories before trusting the judge as a gate.[^2]

**Shreya Shankar would probably push back on:** the implication that criteria drift can be handled with scheduled re-calibration every 4 weeks. Her position, from the UIST paper, is that criteria drift is continuous and localized — certain criteria destabilize as the product surface changes in ways no fixed cadence catches. She'd argue for a criteria-drift monitor embedded in the eval harness, not a calendar-based check.[^7]

**Eugene Yan would probably push back on:** the weight I've put on LLM-as-judge relative to process fixes. His April 2025 post *"An LLM-as-Judge Won't Save The Product — Fixing Your Process Will"* is literally about this: teams over-invest in judge sophistication and under-invest in labeling process, error analysis cadence, and hypothesis discipline. He'd say: spend less time calibrating the judge, more time in the weekly error-analysis session.[^6]

**An Anthropic Applied AI engineer would probably push back on:** the explicit cost-model framing as a scoping artifact. In their internal work, the cost model tends to be a constraint on architecture choice (which model, which retrieval, which agent pattern) rather than a separate scoping document. My take: the cost model belongs in the scope doc for catalyst-leads-turned-advisors, because clients won't architect around it unless you show it to them. For an internal team with strong architectural judgment, it can be implicit.

**A capability-optimist (Gwern-style, or any of several 2026 YC founders)** would push back on the whole frame. They'd say: hard kill criteria, evaluated at week 6, systematically underweight the fact that models get materially better every 8–12 weeks. A project that fails today might succeed against a frontier model in three months. My counter: that's an argument for shorter kill cycles, not weaker kill criteria. If model capability is moving fast, test against the new model when it ships, not against a hope. The discipline survives; the baseline moves.

## Further reading

**Must-read:**

- Hamel Husain, *A Field Guide to Rapidly Improving AI Products* (2025).[^1] The operational bible for the iteration loop.
- Hamel Husain & Shreya Shankar, *LLM Evals: Everything You Need to Know* (FAQ, January 2026).[^2] The most current canonical compilation.
- Shreya Shankar et al., *Who Validates the Validators?* UIST 2024.[^7] The academic grounding for judge calibration and criteria drift.

**Recommended:**

- Eugene Yan, *Task-Specific LLM Evals that Do & Don't Work* (March 2024) and *An LLM-as-Judge Won't Save The Product* (April 2025).[^5][^6]
- Hamel Husain, *Evals Skills for Coding Agents* (2026).[^4] Agentic-specific gate patterns.
- Hamel Husain, *Using LLM-as-a-Judge For Evaluation: A Complete Guide*.[^3]
- MIT State of AI in Business 2025.[^10] The 95% stat — read the methodology, not the headline.
- HBR, *Why Agentic AI Projects Fail* (October 2025).[^9]

**Optional:**

- Gartner's agentic-AI cancellation forecast (June 2025).[^8]
- IntuitionLabs LLM pricing comparison; Zylos 2026 token-economics research.[^11][^12]
- Microsoft Foundry fine-tuning at Ignite 2025.[^13]

## Citations

[^1]: Hamel Husain, *A Field Guide to Rapidly Improving AI Products*, hamel.dev, 2025. <https://hamel.dev/blog/posts/field-guide/>

[^2]: Hamel Husain & Shreya Shankar, *LLM Evals: Everything You Need to Know (FAQ)*, hamel.dev, January 2026. <https://hamel.dev/blog/posts/evals-faq/>

[^3]: Hamel Husain, *Using LLM-as-a-Judge For Evaluation: A Complete Guide*, hamel.dev. <https://hamel.dev/blog/posts/llm-judge/>

[^4]: Hamel Husain, *Evals Skills for Coding Agents*, hamel.dev, 2026. <https://hamel.dev/blog/posts/evals-skills/>

[^5]: Eugene Yan, *Task-Specific LLM Evals that Do & Don't Work*, eugeneyan.com, March 2024. <https://eugeneyan.com/writing/evals/>

[^6]: Eugene Yan, *An LLM-as-Judge Won't Save The Product — Fixing Your Process Will*, eugeneyan.com, April 2025. <https://eugeneyan.com/writing/eval-process/>

[^7]: Shreya Shankar, J.D. Zamfirescu-Pereira, Björn Hartmann, Aditya G. Parameswaran, Ian Arawjo, *Who Validates the Validators? Aligning LLM-Assisted Evaluation of LLM Outputs with Human Preferences*, UIST 2024. <https://arxiv.org/abs/2404.12272>

[^8]: Gartner, "Gartner Predicts Over 40% of Agentic AI Projects Will Be Canceled by End of 2027" (press release, June 25 2025). <https://www.gartner.com/en/newsroom/press-releases/2025-06-25-gartner-predicts-over-40-percent-of-agentic-ai-projects-will-be-canceled-by-end-of-2027> — see also RCR Wireless coverage: <https://www.rcrwireless.com/20250627/business/agentic-ai-gartner>

[^9]: *Why Agentic AI Projects Fail — and How to Set Yours Up for Success*, Harvard Business Review, October 2025. <https://hbr.org/2025/10/why-agentic-ai-projects-fail-and-how-to-set-yours-up-for-success>

[^10]: MIT NANDA / "State of AI in Business 2025" — widely cited 95% pilot-failure figure. Primary report summary via Fortune, "MIT report: 95% of generative AI pilots at companies are failing" (Aug 18 2025): <https://fortune.com/2025/08/18/mit-report-95-percent-generative-ai-pilots-at-companies-failing-cfo/>. See also HBR, "Beware the AI Experimentation Trap" (Aug 2025): <https://hbr.org/2025/08/beware-the-ai-experimentation-trap>.

[^11]: *LLM API Pricing Comparison (2025): OpenAI, Gemini, Claude*, IntuitionLabs. <https://intuitionlabs.ai/articles/llm-api-pricing-comparison-2025>

[^12]: *AI Agent Cost Optimization: Token Economics and FinOps in Production*, Zylos Research, February 2026. <https://zylos.ai/research/2026-02-19-ai-agent-cost-optimization-token-economics>

[^13]: *Fine-tuning at Ignite 2025: new models, new tools, new experience*, Microsoft Tech Community, 2025. <https://techcommunity.microsoft.com/blog/azure-ai-foundry-blog/fine-tuning-at-ignite-2025-new-models-new-tools-new-experience/4476642>

[^14]: Anthropic Engineering blog and Applied AI public materials. <https://www.anthropic.com/engineering> — the Applied AI team's scoping pattern is inferred from engineering talks and public engagement case material; as of April 2026 there is no single canonical published scoping methodology document.

[^ret-gate]: Thresholds are operator-level defaults, not a published benchmark. Anthropic's *Introducing Contextual Retrieval* (2024) https://www.anthropic.com/news/contextual-retrieval reports failure-rate reductions via chunk-level retrieval eval; Hamel Husain and Shreya Shankar, *LLM Evals* and related 2024–2025 writing https://hamel.dev/blog/posts/evals/ argue for retrieval-quality gating as the prerequisite to generation-quality measurement.

_last_verified: 2026-04-15_
