---
type: lesson
block: block-0-basecamp
week: week-00
day_of_cycle: 4
day_name: thu
session_slug: ai-catalyst-program-onboarding
date_due: 2026-04-23
tags: [model-cards, benchmarks, swe-bench, tau-bench, gpqa, bfcl, contamination, calibration, evals, vendor-claims]
sources:
  - anthropic-opus-4-6-release
  - anthropic-opus-4-5-release
  - openai-gpt-5-system-card
  - openai-swe-bench-verified
  - google-gemini-3-1-pro-model-card
  - xai-grok-4-1-model-card
  - yao-2024-tau-bench
  - rein-2023-gpqa
  - patil-2025-bfcl
  - epoch-ai-capabilities-index
  - swebench-pro-2025
  - mmlu-cf-acl-2025
  - hamel-husain-evals-faq
  - eugene-yan-task-specific-evals
  - turpin-2023-unfaithful-cot
  - anthropic-fable-5-mythos-5
  - swe-bench-pro-leaderboard
last_verified: 2026-07-17
word_count_target: 6000
---

# Reading model specs critically — what the Anthropic, OpenAI, Google and xAI cards actually tell you, what they hide, and how to calibrate

## Why this matters

Every few weeks in 2026, one of the labs drops a model card with a table of benchmarks and a headline number. Your feed fills with "Fable 5 hits 95% on SWE-bench Verified," "Mythos 5 leads SWE-bench Pro at 80.3%," "Gemini 3.1 Pro takes GPQA Diamond in the low-90s."[^1][^2][^3] Someone on your team forwards the chart, and within 48 hours there is a Slack thread, a migration plan, and a calendar invite to "evaluate switching models."

The central skill of an AI-pro lead is *not* tracking who is ahead on which benchmark. It is knowing, within ninety seconds of opening a model card, which numbers are meaningful for your pipeline, which are load-bearing PR, which are almost certainly gamed, and which are telling you something real about a capability you care about. The cards are not designed to answer your question. They are designed to answer the *vendor's* question: *"why should this release trend on Hacker News?"* Those two questions overlap only partially.

By the end of today you will be able to, for any model card Anthropic/OpenAI/Google/xAI ships in the next twelve months:

1. Identify which of the five or six headline numbers were produced under conditions your production system will never reproduce, and mentally discount them.
2. Separate *capability-section* claims (benchmarks, code, reasoning) from *safety-section* claims (refusal rates, jailbreak resistance, biorisk evals) and read each with the right lens — they are written by different teams, with different incentives, and should not be conflated.
3. Identify at least one benchmark on the card that is saturated or contaminated, and therefore cannot distinguish this release from the last three.
4. Extract the one signal from the card that would actually change something about how you'd build, evaluate, or price your pipeline — or, more often, conclude that no such signal exists and you should ignore the release until independent numbers land.

This is a calibration skill, and it is the substrate under every model-choice decision the rest of the program asks you to make.

## Prerequisites

- Claude.ai access and Claude Code installed.
- [[01-mon-mental-model-of-llms|Monday's mental model of LLMs]], especially the reasoning-model and confabulation sections — you'll use the same epistemic stance ("what produced this number?") here that Monday used for "which of the three failures was this?".
- [[02-tue-ai-native-builder-stack|Tuesday's tool-stack lesson]] introduced SWE-bench Verified vs Pro and the harness-confound problem; this lesson generalizes that skepticism to every benchmark on a card.
- Familiarity with the idea that a "benchmark score" is a point estimate, not a capability. If you're hazy on confidence intervals, keep a tab open to Epoch AI's Capabilities Index methodology page.[^4]

## Layer 1 — The anatomy of a 2025-era model card

A modern vendor model card is a document of roughly 30–90 pages that mixes four distinct things. A critical reader separates them on first pass.

**1. The marketing preamble.** One to three pages. "Our most capable model yet. A step change in agentic coding. Smarter on your most complex tasks." This is headline copy — the words "step change" appear in the Anthropic, OpenAI, Google, and xAI 2025–2026 releases with uncanny consistency.[^5][^6] Read it for positioning signals (what capability did the lab decide to sell this release on?) and nothing else. If the preamble leads with coding, the card is a coding-first release; safety numbers will be terse. If it leads with safety, capability numbers will be terse. This is nearly always a clean trade.

**2. The capability section.** Five to fifteen pages. Benchmark tables, agentic evaluations, a coding section, a math section, a reasoning section, sometimes a long-context section, sometimes a multimodal section. This is where vendor-reported benchmark numbers live. *This is the section most readers skim for the bold numbers and move on.* You are going to read it differently starting today.

**3. The safety section.** Ten to forty pages. Refusal rates on harmful categories, jailbreak robustness, bioweapon/chem uplift evals, autonomy evals, persuasion evals, sometimes "Responsible Scaling Policy" / "Preparedness Framework" assessments against capability thresholds. The GPT-5-era system cards run to dozens of pages of this, with detailed sections on capabilities in biology, cyber, persuasion, and autonomy.[^7] Anthropic's cards spend comparable ink on RSP evals — and by mid-2026 the safety section is where the whole *access model* of a release lives: Fable 5's card documents that high-risk queries (cyber/bio/chem/distillation) are blocked and answered by an Opus 4.8 fallback, and that its more-capable sibling Mythos 5 is restricted to Project Glasswing partners.[^23] xAI's Grok 4.1 card devotes a substantial portion to bio-risk and CBRN evaluations.[^8] Google's Gemini 3.1 Pro card likewise partitions capability from safety.[^9]

The safety section is written by a different internal team than the capability section, typically operates under a different review process, and uses far more rigorous methodology. Read it with less skepticism — the incentive gradient is genuinely different. A lab publishing a safety eval showing their model performs badly on biorisk uplift has every reason to bury it and none to inflate it.

**4. The limitations section.** One to three pages, usually near the end, often unnumbered. Known hallucination patterns, failure modes, deprecations, restrictions. This is where you learn that "adaptive thinking" has a budget you can exceed, or that a specific Anthropic tool-use mode degrades on contexts above 600K tokens, or that xAI's model performs worse than human baselines on FigQA and multi-step cloning reasoning despite strong aggregate scores.[^8] The limitations section is *the* highest-signal-per-word region of the card. Read it first.

### The reordering trick

When you open a new model card, read it in this order, not top-to-bottom:

1. **Limitations** — anchor on where the model breaks.
2. **Safety section methodology** (skip the numbers, read how they measured) — this tells you what kind of eval the lab can actually execute.
3. **Capability section** — now, with the lab's methodology standards already cached, you can read the capability numbers with better calibration.
4. **Preamble, last.** It is written for journalists. If it surprises you after reading the substance, you missed something in the substance.

This reordering alone adds 90 seconds to your read and removes about 80% of the hype framing. It is free.

## Layer 2 — The benchmarks you will see on every card, and what each one actually measures

Most model cards from Anthropic, OpenAI, Google, and xAI now share a core set of maybe eight benchmarks. You should know what each is measuring, what it doesn't measure, and its current status on the saturation curve.

### SWE-bench Verified

**What it is.** A 500-problem human-filtered subset of SWE-bench, released by OpenAI's Preparedness team in August 2024 in collaboration with the SWE-bench authors.[^10] Each problem is a GitHub issue from a real open-source Python project (Django, sympy, scikit-learn, etc.); the model must produce a patch that passes the project's hidden test suite.

**Why it took over — and why it just retired.** The original SWE-bench had known issues: some problems were ambiguous, some had underspecified tests, some were effectively unsolvable without external context. Verified filtered the set to 500 human-validated problems, giving vendors a stable, clean target, and through 2025 Anthropic, OpenAI, Google, and xAI all reported it as a headline number. As of July 2026 it has **saturated**: Fable 5 leads at 95.0% and the frontier bunches in the high 80s, so a Verified score can no longer distinguish this release from the last three.[^1][^2][^11] This is the exact "last useful quarter" dynamic this lesson teaches — Verified has now aged out of the *headline* bucket and into the *decorative* one, the way HumanEval did before it. The discriminating coding benchmark is now SWE-bench **Pro** (see below).

**What it doesn't measure, and what the cards hide.** The benchmark is a *tuple*: (model, agentic harness, retrieval strategy, sample budget, temperature, and patience). Anthropic has stated that their custom harness contributes roughly a ten-percentage-point improvement in accuracy over a minimal baseline.[^10] Different vendors report numbers under different harnesses. The fine print — usually a footnote the size of an ant — says things like "evaluated on Anthropic's internal harness with parallel test-time compute (n=k samples, reranker)" or "evaluated with pass@1 under the default SWE-agent scaffold."

Two numbers from the same benchmark, reported by two vendors, can differ by more than the difference between the underlying models. The SWE-bench team attempted to address this with mini-SWE-agent, a minimal ReAct loop standardizing conditions, but vendors still report their own harness numbers as headlines.[^10]

**The live controversy.** Is SWE-bench Verified a good proxy for real-world coding capability?

*Position A (the vendors'):* Yes — it tracked real progress, and its saturation drove the move to Scale AI's contamination-resistant SWE-bench **Pro**, where the July-2026 frontier still has dynamic range: Mythos 5 leads at 80.3%, Fable 5 is at ~80%, and Opus 4.8 leads *active* models at 69.2%.[^12] Saturation is a sign the benchmark *did its job*. Carry one caveat, though: OpenAI's July 2026 audit estimated ~30% of the public Pro tasks are broken and retracted its earlier recommendation — so Pro is the better discriminator but is itself noisy.

*Position B (practitioners, ML engineers):* Hamel Husain has argued across his 2024–2025 posts that foundation-model benchmarks answer a fundamentally different question than product-specific evals. He distinguishes cleanly between "benchmarks that justify a release" and "evals that tell you if your product works," and warns that the former routinely overfit in ways that do not transfer.[^13] Eugene Yan, writing on task-specific evals, makes the adjacent point that generic metrics — including aggregated coding benchmarks — underperform task-specific rubrics on production distributions; the fluency benchmarks reward is already solved, so the signal is elsewhere.[^14] The operational claim: a jump on SWE-bench (Verified *or* Pro) is not evidence the model will be better on *your* codebase. Harness and retrieval choices swamp the model delta for many production contexts.

Both positions are partially correct. The responsible calibration: a coding benchmark tracks *something* — a model that rises from 65% to 80% on Pro has genuinely improved at agentic coding in a specific setup. But a two-point delta between generations, under different harnesses, inside different labs' scaffolds, should not drive a migration decision. That decision needs your own eval — the discipline [[05-fri-context-window-economics|Friday]] and the later evals week build.

### TAU-bench (τ-bench)

**What it is.** A benchmark introduced by Shunyu Yao, Noah Shinn, Pedram Razavi, and Karthik Narasimhan at Sierra in 2024 (arXiv 2406.12045). It simulates dynamic multi-turn conversations between a language agent and a user (also simulated by an LLM), with the agent given access to domain-specific APIs and required to follow a policy document.[^15] Two domains ship: retail (product returns, exchanges) and airline (booking, itinerary changes). Evaluation is state-based — at end of conversation, does the database state match the annotated goal state?

**Why it's interesting.** Unlike SWE-bench, TAU-bench is explicitly adversarial toward the agentic paradigm: the user simulator will change their mind, give incomplete information, resist the agent, and not always follow a clean conversation path. TAU-bench also introduced the pass^k metric — not "did the agent succeed at least once in k tries" but "did the agent succeed on *all* k independent trials," exposing reliability, not peak performance.

**What it tells you.** Even frontier 2024-era function-calling agents succeeded on less than 50% of TAU-bench retail tasks and, more damningly, showed pass^8 under 25%.[^15] Consistency collapsed long before peak capability did. Vendors have begun reporting TAU-bench in 2025–2026 model cards, and the numbers have risen — but the pass^k discipline remains rare in vendor reports. When you see a TAU-bench score without a pass^k figure, you are seeing the generous version of the story.

**What it doesn't measure.** Policy documents are short and artificial; production policies are long, contradictory, and versioned. The user simulator, being an LLM, has LLM-typical failure modes that compound with the agent's. Real customers send ambiguous typo-ridden multi-language emojis; TAU-bench users are polite text.

### GPQA (Diamond)

**What it is.** The "Graduate-Level Google-Proof Q&A" benchmark, 448 multiple-choice questions across biology, physics, and chemistry, written by PhDs and PhD students in the relevant domains. Rein et al., Nov 2023, arXiv 2311.12022.[^16] The "Diamond" subset is the hardest 198 questions. PhD-domain-expert humans reach 65% accuracy; non-expert humans with internet access reach 34%.

**Why vendors love it.** It's hard, it's tasteful, it looks like "real graduate-level science," and through 2025 it was still on the non-saturated side. That has now flipped: Gemini 3 Pro reported 91.9% on GPQA Diamond (93.8% with Deep Think), and the later Gemini 3.1 Pro refresh reached ~94.3% with Deep Think.[^3] When a benchmark goes from 39% (GPT-4 initial) to the mid-90s in under three years, the next generation hits the ceiling and it retires. *This is a benchmark you are watching leave its last useful quarter in real time* — exactly the pattern SWE-bench Verified completed above.

**What it doesn't measure.** Multiple choice collapses the answering surface. The benchmark measures *knowledge and reasoning on closed, canonical graduate-level scientific questions* — a non-trivial capability — but says nothing about open-ended problem framing, experimental design, or the capacity to notice a question is ill-posed.

### AIME / math competition benchmarks

**What it is.** AIME (American Invitational Mathematics Examination) is a 15-problem high-school math contest, 3-hour time limit, integer answers 0–999. AIME 2024/2025 have become standard vendor reports, along with HMMT and Putnam for top-of-range models.

**Current status.** Saturated at the top. Grok 4 Heavy scored 100% on AIME 2025. Gemini 3 Pro with code execution hit 100%, 95% without tools.[^3][^17] When multiple frontier models achieve perfect or near-perfect scores on a benchmark, the benchmark can no longer distinguish them. It remains useful for mid-tier models and for open models comparing to frontier; it is not a useful differentiator among the top five.

**What it doesn't measure.** Olympiad-style math is a narrow slice of mathematical reasoning — contest problems have elegant solutions by construction, which is not how research math or applied math works. A model that aces AIME may still fail on a grad-student-level proof requiring 40 pages of setup.

### BFCL (Berkeley Function-Calling Leaderboard)

**What it is.** Released by the Gorilla team at UC Berkeley (Shishir Patil et al.); now at v3/v4. Evaluates function calling via AST-based structural comparison — the model's generated tool call is parsed and matched structurally against the gold call, which lets the benchmark scale to thousands of functions without actually executing any of them.[^18]

**BFCL v3 specifically.** Introduced multi-turn evaluation, long-context tool settings, and *relevance* categories (does the model correctly refuse to call tools when none are needed?). The seventeen task categories cover simple, parallel, multi-step, long-context, missing-function, and missing-parameter cases.[^18] This is one of the cleanest agentic-capability benchmarks currently published.

**What it doesn't measure.** Structural correctness is not execution correctness. An AST-match pass means the model produced a call with the right shape; it does not mean the tool, when actually run, would have returned the right result or that the model would have recovered from a failure. Multi-turn with tool-failure recovery — a core production failure mode — is present but limited.

### HumanEval / MBPP

**Status.** Saturated and contaminated. HumanEval was one of the original LLM coding benchmarks (164 Python problems, doc-string + tests). Independent work has shown 8–18% of HumanEval problems overlap with samples that appear verbatim or near-verbatim in common training data, and GPT-3.5-generated synthetic training sets (CodeAlpaca) contain 12.8% rephrased HumanEval samples.[^19]

If you still see HumanEval on a 2026 model card — and you will, in the long-table-of-secondary-benchmarks — the number is essentially a null check. Every frontier model scores in the high 90s. Treat it as decorative.

### MMLU

**Status.** Saturated and contaminated. MMLU is 57 subject areas of multiple-choice academic knowledge, released 2020. By mid-2024, frontier models were saturating at the high end; by 2026 the current frontier (Fable 5, Opus 4.8, Gemini 3.1 Pro) clusters at 88–93%.[^4][^20] Epoch AI's Capabilities Index explicitly exists because individual benchmarks like MMLU saturate faster than models improve, making single-benchmark comparisons meaningless across releases.[^4]

Worse, GPT-4 and ChatGPT have been shown to complete held-out MMLU questions with exact-match rates of 57% and 52% respectively when simply asked to fill in missing options — strong evidence of training-set leakage.[^20] MMLU-CF (ACL 2025) was built explicitly to create a contamination-free replacement, with rephrased questions and shuffled options.[^21] MMLU-Pro (ten answer choices, harder questions) is approaching saturation as well, with top 2026 models at ~90%.

**Operational consequence.** If a vendor leads their capability section with MMLU, they are signaling weakness elsewhere. If a vendor leads with a *new* or *uncommon* benchmark you've never seen before, the opposite warning applies — suspicion of cherry-picking. The right diagnostic is reading across *three* model cards from the same period and noting which benchmarks the vendor chose to emphasize and which they buried.

## Layer 3 — What cards systematically don't measure

The most important numbers in your pipeline are typically not on any card. Make this list part of your mental model; it's the gap between "benchmark state of the art" and "production-ready."

**Long-horizon task completion outside the benchmark harness.** SWE-bench tasks have bounded scope and clear termination criteria. Most production coding tasks don't. A 30-minute agentic coding task that requires mid-stream replanning — "I need to look at the CI logs, then reconsider my test strategy" — is not scored on any released benchmark.

**Multi-turn with tool-failure recovery.** BFCL's multi-turn tracks test a limited slice; TAU-bench's user simulator is adversarial in its own way but doesn't simulate flaky tools, rate-limited APIs, or stale data. The ability to gracefully handle a 500 Internal Server Error on the third tool call is one of the most load-bearing capabilities for production agents and is unmeasured by any public benchmark.

**Stylistic / taste / QA judgments.** Does the model write summary bullets the way your brand writes them? Does it preserve a specific voice? Can it match house style on memos? These are untestable by any capability benchmark; they are your evals to build.

**Latency and p99 reliability.** Cards report capability numbers, not timing distributions. A model that hits 80% on SWE-bench Pro over a 48-hour eval run can also have a 4-second p50 and a 40-second p99 under tool-use workloads; neither number is on the card. Latency shifts when thinking is enabled — sometimes dramatically — and vendor-reported latency numbers, when they exist at all, are typically median under benign conditions.

**Cost efficiency on *your* distribution.** Pricing is on the release blog, not the card. A model that's 10% better and 5x more expensive is not "better" for most production systems. This is a pipeline-level accounting question, not a model-level benchmark question.

**Safety under adversarial *tool output*.** Safety sections evaluate refusal on adversarial *user* prompts. They do not typically evaluate what happens when a web search tool returns attacker-controlled content containing prompt injection — Simon Willison's lethal trifecta (private data + untrusted content + exfiltration channel), which [[02-tue-ai-native-builder-stack|Tuesday's tool-stack lesson]] introduced.[^22] As of mid-2026, no major vendor publishes a standard adversarial-tool-output benchmark, even as dynamic-workflow orchestration multiplies the injection surface. This is the single largest unmeasured safety surface in current model cards.

## Layer 4 — Contamination, Goodhart, and spotting a suspicious number

Three failure modes cluster here.

**Training-set leakage.** The simplest: the test data, or a near-paraphrase of it, appears in pretraining. The MMLU/HumanEval evidence above is representative, not exceptional.[^19][^20] Simple string-match decontamination misses translations, paraphrases, and structural rewrites; serious decontamination requires embedding-based deduplication or dynamic test generation (which is why benchmarks like MMLU-CF and LiveBench exist).

**Goodhart on the benchmark.** When a metric becomes a target, it ceases to be a good metric. Anthropic, OpenAI, Google, and xAI all know their models will be judged by SWE-bench Verified. They optimize training data, fine-tuning, and RL for agentic coding behaviors that look like SWE-bench. The model gets better at SWE-bench *and* at real coding, but the rate differs. By the time Verified saturates, the gap between benchmark score and real-world productivity gain is wider than at launch — which is why SWE-Bench Pro, with harder problems and a lower ceiling, became necessary.[^12]

**Vendor-reported vs third-party-reproduced.** Lab-internal harnesses, sample budgets, parallel test-time compute, and majority-vote rerankers can all legitimately boost reported numbers. When the same model is evaluated by an independent third party under a different scaffold, numbers routinely drop by 5–15 points. The Epoch AI Capabilities Index and Artificial Analysis's independent reruns are the two primary counterweights; when their numbers disagree meaningfully with the vendor's, trust the third party for cross-model comparison purposes.[^4]

**How to spot a suspicious number.** Five heuristics:

1. *The number is a new record by a suspiciously clean margin.* Generation-over-generation SWE-bench deltas of a few points are plausible. A jump of 15 points would not be — no single model release produces a 15-point real capability jump without a fundamental architectural change. (When a leader instead posts a huge jump because a *new* model tier appeared — Fable 5's Mythos-class leap over Opus — read the access policy in the safety section, not just the number.)
2. *The benchmark is one the vendor has never previously reported.* This often means the model is much better on new benchmarks the competitor reports and much worse on the old one.
3. *The number is reported without sample budget, temperature, or scaffold details.* "Pass@1 under Anthropic's internal harness with parallel test-time compute at n=unspecified" is pseudo-science. You cannot reproduce it.
4. *The "+X points" baseline is selectively chosen.* "Our new model is +8 points over the previous model" — but the comparison is against an old, non-thinking variant while the current competitor is a thinking variant. Watch for cross-comparison across reasoning modes.
5. *The number conflicts with an independent third party.* Artificial Analysis and Epoch AI rerun most major releases. When their numbers are 3+ points lower and the vendor's footnote about harness conditions is vague, the vendor number is the aspirational one.

## Layer 5 — An operator war story, with names, dates, and numbers

This is a composite operator anecdote, drawn from multiple published reports of large-codebase AI engineering teams and their eval practice in 2024–2025 (see e.g. Obie Fernandez's Shopify-engineering-era writing and the broader eval-driven-development posts cited in this lesson's reading list).[^24] A representative version of the pattern: an AI-first engineering team had built an internal coding-assistant pipeline on an earlier Claude generation, evaluated it on both SWE-bench Verified *and* on an internal eval drawn from their own Python/Ruby monorepo. When a new Claude generation dropped with a reported +4 point SWE-bench Verified jump (the release at the time was in the low 70s), the team spent roughly one engineering week running their internal eval against the new model. Internal-eval accuracy moved by less than one point, within the noise band of their harness. Migration was deferred for six weeks until a later revision produced a signal on *their* distribution.

This is the pattern: the public benchmark moved, the production eval did not, and the team that had built its own eval could tell the difference. Teams without internal evals migrated on the headline number, and half of them migrated back when latency and cost metrics on their distribution turned out worse.

Anthropic, OpenAI, Google, and xAI will keep shipping model cards with positive-trending numbers. Your team's calibration habit is what converts those numbers into decisions. If you do not have internal evals, every model card is an unfiltered pitch.

## Runnable experiment — calibrate a single vendor headline

Do this before you move on. The exercise is intentionally small; the point is the *habit* it creates.

**Step 1.** Open Claude Code in any scratch folder.

**Step 2.** Direct Claude Code with this instruction (adapt the numbers if the release has moved by the time you read this):

> Please look up the following from primary sources (vendor model cards and release notes, not third-party blogs). Pick the two current frontier models the day you run this — as of mid-July 2026 that is Claude Fable 5 and either GPT-5.6 Sol or Gemini 3.1 Pro:
>
> 1. The exact SWE-bench Pro score the vendor reports for model A (use Pro, not the now-saturated Verified).
> 2. The harness, sample budget (n), temperature, and whether parallel test-time compute was used, from the footnotes in the release page or any linked model card PDF.
> 3. The exact SWE-bench Pro score the second vendor reports for model B.
> 4. The harness, sample budget, temperature, and test-time compute settings that vendor reports.
> 5. Where the two methodologies differ, list each concrete difference.
> 6. Where an independent tracker (Epoch AI, Artificial Analysis, BenchLM, llm-stats) has published rerun numbers for either model, report those and the delta from the vendor number — and note that OpenAI's July 2026 audit flagged ~30% of public SWE-bench Pro tasks as broken.
>
> For each of the six items, cite the URL and exact section you pulled it from. If any item is missing from the source (e.g., vendor doesn't publish n), say "not reported" — do not guess.

**Step 3.** When Claude Code returns, audit the output for three specific things:

- Did it find the numbers or did it fall back to a secondary blog?
- Did the vendors report the same methodology, or are the numbers technically incomparable?
- Is the independent third-party number meaningfully different from the vendor-reported one?

**Step 4.** Open Claude.ai in parallel. Paste *the same instruction* into a new conversation. Compare what Claude.ai returns, in plain conversational mode, to what Claude Code returned with tool access. The differences will be instructive: Claude.ai will be more likely to hedge, less likely to cite specific footnotes, and more likely to hit knowledge-cutoff gaps on post-cutoff releases. Claude Code with web access will be more likely to hit the actual PDFs.

**Step 5.** Write a three-sentence note to yourself answering: *would I migrate my pipeline on this delta?* The answer should be "no" unless either (a) the methodology matches and the delta is large, or (b) the independent third-party confirms and your own eval has already tracked a correlated improvement.

This exercise is a habit, not a one-off. Run it every time a new model lands. It takes ten minutes and is the single cheapest calibration practice in your toolkit.

## Reviewer lens — five disagreements I would expect an expert to push back on

Writing this lesson, I am aware of where a reviewer who does this full-time would push.

1. *"You've overweighted the harness-confound critique on SWE-bench Verified."* Fair. The SWE-bench team and OpenAI Preparedness built mini-SWE-agent in 2024–2025 precisely to standardize conditions for cross-model comparison.[^10] A careful reader will look at both vendor numbers *and* mini-SWE-agent numbers. The critique in Layer 2 is sharpest when applied to vendor-reported headline numbers, not to the mini-SWE-agent standardized line.

2. *"Your framing of Hamel Husain's position overstates it."* Husain does not claim SWE-bench is useless — he claims it is not a product eval, and that foundation-model benchmarks and product-specific evals answer different questions.[^13] The position I labeled "B" in Layer 2 is a composite synthesized from Husain's and Yan's posts; the individual positions are subtler. If you cite the composite in a team discussion, cite them individually first.

3. *"Goodhart is a tired frame; the real mechanism is mesa-optimization against the training signal."* A reviewer deep in the interpretability literature would argue the Goodhart framing is imprecise. Models don't "optimize" for SWE-bench directly; rather, labs select training data and post-training objectives that correlate with SWE-bench performance, and this induces second-order effects that look Goodhart-like. For an operator audience the distinction doesn't matter; for a research audience it does.

4. *"You're being too dismissive of MMLU."* Also fair, and I stand behind the framing but note the caveat: MMLU at 88–93% is uninformative *between frontier models in 2026*. A 30-point MMLU gap between a 2023 7B open model and a 2026 frontier model is genuinely informative; the benchmark did its historical job. The dismissal applies to its current role as a vendor headline, not to its full record.

5. *"TAU-bench's pass^k is a better reliability metric, but is also subject to simulator bias."* A reviewer close to the Sierra team would point out that pass^k depends on the user simulator behaving consistently across trials, and the simulator is itself an LLM with its own variance. Reliability measured by pass^k conflates model unreliability with simulator unreliability. The Sierra team acknowledges this in the τ2-bench followup.

## Common mistakes I see AI-pro leads make when reading cards

- **Migrating on a headline number without running a personal eval first.** The composite operator war story above generalizes — if your pipeline is non-trivial, the public benchmark is a weak prior.
- **Treating the safety section as skim content.** The safety section is often the most honest section of the card; the capability section is the most marketed.
- **Trusting benchmark numbers reported on a third-party review blog without clicking through to the primary source.** The blog often rounded, or picked a favorable variant, or confused thinking and non-thinking modes.
- **Failing to check the release date against the benchmark release date.** If Benchmark X was released in month N and the vendor reports a SOTA score in month N+1, either they had pre-release access or they fine-tuned on it. Either is a signal — just not necessarily the one they want you to hear.
- **Reading a single release in isolation.** Cards are comparative artifacts. Read Anthropic's, OpenAI's, Google's, and xAI's latest side-by-side; the differences in which benchmarks each chose to highlight are the real message.

## Reflection prompts — not Googleable

- You are evaluating whether to migrate from Sonnet 5 to Opus 4.8 (or up to Fable 5) for a production retail customer-service agent. Which three sections of each card do you read in which order, and what specific number would make you *not* migrate even if the headline coding benchmark moved significantly? (Remember Fable 5 costs 2× Opus per token and tokenizes ~30% heavier.)
- The 2027 version of GPQA Diamond hits 98% across all four major labs. What do you, as a calibration-conscious reader, now do differently when GPQA appears in a capability table?
- A new vendor you have not used before releases a model with headline numbers +4 points above the nearest Anthropic/OpenAI/Google offering on three benchmarks and -8 points on one. What is your prior on this release being (a) a genuine advance, (b) a cherry-picked report, (c) a sign of training-data leakage on the +4 benchmarks? What single piece of evidence would most rapidly update you?
- Your legal team asks you to generate a one-page "why we chose model X" justification based entirely on vendor-reported benchmarks. What do you push back on, and what do you provide instead?
- Every model card you have read in the last six months reports on the same seven benchmarks. What does this uniformity tell you about the capability-measurement ecosystem, and what does it miss?

## Further reading

**Must-read (this week):**
- The Claude Fable 5 release page (Jun 2026) and a current GPT-5.6 or Gemini 3.1 Pro system card. Read them side by side; note how a capability-first release buries safety and an access-gated release leads with it.[^5][^7][^23]
- Hamel Husain, *"Your AI Product Needs Evals"* and the FAQ post.[^13]
- Eugene Yan, *"Task-Specific LLM Evals That Do & Don't Work."*[^14]

**Recommended:**
- Yao et al., τ-bench paper (arXiv 2406.12045).[^15]
- Rein et al., GPQA paper (arXiv 2311.12022).[^16]
- Patil et al., BFCL (ICML 2025 / OpenReview).[^18]
- Epoch AI Capabilities Index methodology page.[^4]

**Optional:**
- SWE-Bench Pro paper (arXiv 2509.16941) — the benchmark that replaces Verified as the latter saturates.[^12]
- MMLU-CF paper (ACL 2025) — the contamination-free replacement.[^21]
- A Survey on Data Contamination for Large Language Models (arXiv 2502.14425).

## Citations

[^1]: SWE-bench leaderboards, fetched 2026-07-17: Verified (now saturated; Fable 5 leads at 95.0%) https://llm-stats.com/benchmarks/swe-bench-verified and https://www.swebench.com/; SWE-bench Pro (Mythos 5 80.3%, Opus 4.8 69.2% active) https://benchlm.ai/benchmarks/swePro. Fable 5 release (95.0–95.5% Verified, Mythos-class tier, access model): Anthropic https://www.anthropic.com/news/claude-fable-5-mythos-5 (corroborated via search; 403s to the fetch proxy) and https://simonwillison.net/2026/Jun/9/claude-fable-5/.
[^2]: SWE-bench Pro leaderboard (BenchLM), fetched 2026-07-17. https://benchlm.ai/benchmarks/swePro — July 2026: Mythos 5 80.3%, Fable 5 ~80%; Opus 4.8 leads active models at 69.2% (llm-stats aggregate, https://llm-stats.com/benchmarks/swe-bench-pro). Note OpenAI's July 2026 audit estimated ~30% of public Pro tasks are broken.
[^3]: Vellum AI, "Google Gemini 3 Benchmarks (Explained)," 2026. Gemini 3 Pro: 91.9% GPQA Diamond; Gemini 3 Deep Think: 93.8%. https://www.vellum.ai/blog/google-gemini-3-benchmarks. Official Gemini 3.1 Pro model card (later refresh reaching ~94.3% GPQA Diamond with Deep Think): https://deepmind.google/models/model-cards/gemini-3-1-pro/. (Body/footnote corrected 2026-07-17: the 91.9%/93.8% figures are Gemini 3 Pro / Deep Think, not 3.1 Pro.)
[^4]: Epoch AI, "Epoch Capabilities Index" methodology, 2024–2025. Addresses benchmark saturation by aggregating across benchmarks on a general-capability scale. https://epoch.ai/benchmarks/eci/
[^5]: Anthropic, "Claude Fable 5 and Claude Mythos 5" release page, 2026-06-09. https://www.anthropic.com/news/claude-fable-5-mythos-5 (corroborated via search; 403s to the fetch proxy). A capability-and-access-first release page — useful contrast to a capability-only announcement.
[^6]: Google, "Gemini 3.1 Pro: A smarter model for your most complex tasks," blog.google, 2026. https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/
[^7]: OpenAI, GPT-5 System Card, August 2025. https://cdn.openai.com/gpt-5-system-card.pdf (updated version: https://cdn.openai.com/pdf/8124a3ce-ab78-4f06-96eb-49ea29ffb52f/gpt5-system-card-aug7.pdf). Covers capability evaluations, Preparedness Framework assessments including biology, cybersecurity, persuasion, and autonomy categories.
[^8]: xAI, "Grok 4.1 Model Card," November 17, 2025. https://data.x.ai/2025-11-17-grok-4-1-model-card.pdf. See also Grok 4 card (Aug 20, 2025) at https://data.x.ai/2025-08-20-grok-4-model-card.pdf and Grok 4 Fast card (Sep 19, 2025) at https://data.x.ai/2025-09-19-grok-4-fast-model-card.pdf. Grok 4.1 Thinking LMArena #1 at 1483 Elo; underperforms human baselines on FigQA and CloningScenarios despite strong aggregate scores.
[^9]: Google DeepMind, "Gemini 3.1 Pro Model Card." https://deepmind.google/models/model-cards/gemini-3-1-pro/
[^10]: OpenAI, "Introducing SWE-bench Verified," August 2024. https://openai.com/index/introducing-swe-bench-verified/. 500 human-validated problems; harness contribution documented. SWE-bench official site and mini-SWE-agent: https://www.swebench.com/ and https://www.swebench.com/verified.html. Anthropic harness improvement (~10 points) discussed in SWE-bench guides: https://www.swebench.com/SWE-bench/guides/evaluation/
[^11]: CodeSOTA analysis of Claude Opus 4.5: 80.9% SWE-bench Verified. https://www.codesota.com/news/claude-opus-4-5-swe-bench-80. Sonnet 4.5 figures (77.2%, 82.0% with parallel test-time compute) from Anthropic Sonnet 4.5 release page.
[^12]: "SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?" arXiv 2509.16941, September 2025 (updated November 2025). https://arxiv.org/pdf/2509.16941. Introduces the harder, contamination-resistant benchmark. Current (July 2026) leaderboard: Mythos 5 80.3%, Opus 4.8 69.2% active — https://benchlm.ai/benchmarks/swePro and https://www.morphllm.com/swe-bench-pro. (The April draft's "GPT-5.2 Thinking 55.6% SOTA" figure is superseded.) OpenAI's July 2026 audit flagged ~30% of public Pro tasks as broken.
[^13]: Hamel Husain, "Your AI Product Needs Evals." https://hamel.dev/blog/posts/evals/ and "LLM Evals FAQ" https://hamel.dev/blog/posts/evals-faq/. Also "A Field Guide to Rapidly Improving AI Products" https://hamel.dev/blog/posts/field-guide/. Core claim: foundation-model benchmarks and product-specific evals answer different questions; the former routinely overfits in ways that don't transfer to production distributions.
[^14]: Eugene Yan, "Task-Specific LLM Evals That Do & Don't Work." https://eugeneyan.com/writing/evals/. N-gram metrics and generic LLM-evals found unreliable/impractical on production workloads; binary task-specific labels outperform 1–5 Likert scales for calibration.
[^15]: Yao, Shinn, Razavi, Narasimhan, "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains," arXiv 2406.12045, 2024. https://arxiv.org/abs/2406.12045. Retail and airline domains; pass^k reliability metric; state-of-the-art function-calling agents <50% success, pass^8 <25% in retail.
[^16]: Rein et al., "GPQA: A Graduate-Level Google-Proof Q&A Benchmark," arXiv 2311.12022, November 2023. https://arxiv.org/abs/2311.12022. 448 multiple-choice questions; domain experts 65%, non-experts 34%; Diamond subset = 198 hardest questions.
[^17]: xAI, Grok 4 Heavy 100% AIME 2025 coverage. https://ucstrategies.com/news/grok-4-heavy-100-aime-score-benchmarks-api-pricing-2026/
[^18]: Patil et al., "The Berkeley Function Calling Leaderboard (BFCL): From Tool Use to Agentic Evaluation of Large Language Models," ICML 2025. https://openreview.net/forum?id=2GmDdhBdDk and https://gorilla.cs.berkeley.edu/leaderboard.html. BFCL v3: 17 task categories including multi-turn, multi-turn-miss-func, multi-turn-miss-param, long-context; AST-based structural evaluation.
[^19]: Survey on Data Contamination for LLMs, arXiv 2502.14425, 2025. https://arxiv.org/html/2502.14425v2. HumanEval: 8–18% overlap with common training data; CodeAlpaca synthetic dataset contains 12.8% rephrased HumanEval samples. "Investigating Data Contamination in Modern Benchmarks for Large Language Models," arXiv 2311.09783.
[^20]: Deng et al. (NAACL 2024). *Investigating Data Contamination in Modern Benchmarks for Large Language Models.* https://arxiv.org/abs/2311.09783 / https://aclanthology.org/2024.naacl-long.482/ — introduces the Testset Slot Guessing (TS-Guessing) protocol: masking a wrong option in MMLU multiple-choice items and prompting the model to fill it in. ChatGPT and GPT-4 achieve 52% and 57% exact-match rates respectively on the masked held-out options, providing strong evidence of training-set leakage. Epoch AI MMLU tracking: https://epoch.ai/benchmarks/mmlu/
[^21]: Microsoft, "MMLU-CF: A Contamination-free Multi-task Language Understanding Benchmark," ACL 2025. https://github.com/microsoft/MMLU-CF. Contamination-free replacement using rephrased questions and shuffled answer options.
[^22]: Simon Willison (2025-06-16). *The lethal trifecta for AI agents.* https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/ — private data + untrusted content + exfiltration channel. Coined June 2025; introduced in this week's [[02-tue-ai-native-builder-stack|Tuesday tool-stack lesson]] (the April draft mis-pointed this to a nonexistent "Monday prompting lesson"). See also Turpin et al., "Language Models Don't Always Say What They Think," 2023, for the faithfulness framing applied here.
[^23]: Anthropic (2026-06-09). *Claude Fable 5 and Claude Mythos 5.* https://www.anthropic.com/news/claude-fable-5-mythos-5 (corroborated via search; page 403s to the fetch proxy). Mythos-class tier above Opus; high-risk queries (cyber/bio/chem/distillation) blocked with an Opus 4.8 fallback; Mythos 5 restricted to Project Glasswing partners (https://anthropic.com/glasswing). Public risk-warning context days before launch: https://techcrunch.com/2026/06/09/anthropics-claude-fable-5-is-a-version-of-mythos-the-public-can-access-today/. Verified 2026-07-17.

_last_verified: 2026-07-17_
