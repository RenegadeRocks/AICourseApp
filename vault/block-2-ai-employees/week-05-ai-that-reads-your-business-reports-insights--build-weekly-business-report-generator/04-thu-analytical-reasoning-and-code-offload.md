---
type: lesson
block: block-2-ai-employees
week: week-05
day_of_cycle: 4
day_name: thu
session_slug: build-weekly-business-report-generator
date_due: 2026-06-18
tags:
  - analytical-reasoning
  - numerical-accuracy
  - code-execution
  - financebench
  - evaluator-critic
  - self-correction
  - tool-use
  - pal
  - finqa
  - claude-code-execution
sources:
  - financebench-islam-2023-arxiv-2311-11944
  - finqa-chen-2021-arxiv-2109-00122
  - huang-iclr-2024-self-correct-2310-01798
  - pal-gao-2022-arxiv-2211-10435
  - self-consistency-wang-2022-arxiv-2203-11171
  - anthropic-code-execution-tool-2025
  - anthropic-advanced-tool-use-2025
  - patronus-ai-financebench-2023
  - hamel-husain-llm-judge-2024
  - s2r-self-verify-acl-2025
  - huang-kambhampati-critique-2024
  - tacl-2024-when-can-llms-self-correct
last_verified: 2026-07-17
word_count_target: 6000
---

# Analytical reasoning under uncertainty — where LLMs still fail on numbers, code-execution offloading, and the self-correction loops that actually work

## Why this matters

After this lesson you will be able to look at any proposed AI-analyst deliverable — a weekly flash report, a monthly close narrative, a board-pack page — and answer two questions most builders skip straight past: (1) *which specific numerical claims are safe for an LLM to produce directly, and which must be routed through a deterministic runtime before they can ship?* and (2) *when does an evaluator-critic loop actually reduce error, and when is it theater that produces the same wrong answer twice in different words?*

The gap between "Claude wrote me a gorgeous summary of our P&L" and "Claude wrote me a summary I will stake my reputation on in front of a CFO" is the subject of this day. A bigger model, a longer context window, or a better prompt does not close it; the fix is an architecture that knows where the language model is a liability and builds deterministic scaffolding at exactly those joints. Patronus AI's FinanceBench[^1] — the first serious open-book financial QA benchmark — reported in November 2023 that GPT-4-Turbo with retrieval *refused or incorrectly answered 81% of questions* on 150 manually-reviewed cases drawn from real 10-K filings[^1][^2]. Two and a half years later, frontier models have closed some of that gap on simpler aggregations, but the structural failure modes (off-by-one on multi-row aggregations, unit confusion, hallucinated column values, compounding rounding) persist in every post-2024 eval. The interesting question is no longer *"can the model get it right?"* but *"what is the minimum scaffolding that makes the right-answer rate audit-grade?"*

## Prerequisites

- [[04-thu-rag-fundamentals|Week 4]] tool-calling and eval harness patterns (you are not relearning function-calling here).
- Working familiarity with Anthropic's code execution tool[^6] *or* a self-hosted sandbox (e2b, Riza, Modal). You will invoke one during the runnable experiment.
- The verified-numbers layer feeds directly into [[05-fri-report-generation-patterns|Friday's]] generation patterns and Saturday's build.
- One real tabular corpus you can query against with ground truth: a ledger export, a 10-K you have studied, a Stripe dump, anything with ≥ 50 rows and ≥ 5 computable multi-step questions.

## Layer 1 — The failure taxonomy: where LLMs demonstrably miscount, and why

Every serious production postmortem on an analyst-replacement worker I have read in the last eighteen months rediscovers the same taxonomy. Writing it down explicitly lets you build the test suite before you ship, instead of after the embarrassing Monday email.

**Aggregation off-by-one.** Ask an LLM to sum a 40-row column and it will get the sum right most of the time, but the failure mode when it fails is characteristic: it silently drops one row, almost always at a page boundary or where a subtotal row sits inside the data region. FinQA[^3] (Chen et al., EMNLP 2021, arxiv 2109.00122) formalised this failure class at 8,281 expert-annotated financial QA pairs; the original GPT-3 baseline scored 48.56% on numerical reasoning operations that humans completed at 89%+. By 2024 the frontier gap had narrowed on simple aggregations but *widened relative to expectations* on multi-step numerical reasoning once you add realistic table messiness (merged cells, multi-year columns, footnoted adjustments).

**Unit and scale confusion.** The worst class. A model that reports "operating margin improved 4%" when the actual improvement was 4 basis points (or 4 percentage points, or 400 bps — depending on which definition won the coinflip) is *not* correctable by a downstream grammar. The failure is at the reasoning layer, and it survives every style-and-tone edit you apply on top. Finance lives in three different "percent" conventions (rate, change, point) and four different scale conventions ($, $K, $M, $B) and models interleave them freely when the source document does.

**Sign errors on deltas.** Revenue *declined* 12% gets reported as *grew* 12% with non-trivial frequency when the model is pattern-matching on surrounding context rather than computing the signed difference. This is the single most common failure I have personally seen in pilot builds of weekly sales-ops generators, and it is catastrophic because a confidently-stated direction reads *more* credible than a hedged one.

**Hallucinated column values.** Ask about a line item that the document does not contain and the model will often produce a number anyway — usually one that is plausible given the company's size and sector. This is the failure mode that killed most of the first generation of "AI reads your 10-K" demos; the numbers looked right, until someone with a CFA checked them.

**Confidently-wrong rounding.** Chains of multiplication and division, especially when percentages are in play, accumulate error. A four-step calculation where each step rounds to one decimal can produce a final answer that is 2–3% off ground truth while the model narrates every intermediate step correctly. The narrative passes review; the number does not.

These are not exotic edge cases. They are the modal failure modes of every serious financial-QA benchmark published since 2023. The architectural implication is the same one Luyu Gao and Graham Neubig's team made in the Program-Aided Language Models paper (PAL)[^4] (arxiv 2211.10435, ICML 2023): *stop asking the LLM to do the arithmetic*. Use the language model to decompose the question and write the program; execute the program on a deterministic runtime; feed the result back to the language model only for narration. PAL, in its original paper, beat chain-of-thought reasoning by +6.4 points on GSM8K with a smaller model (Codex 72.0% vs CoT 65.6%)[^4]. The same insight, two and a half years later, is what makes Anthropic's code execution tool[^6][^7] the correct default for any analyst-replacement deployment that has to survive audit.

## Layer 2 — The benchmark landscape and what to believe in 2026

Benchmark numbers are load-bearing in this domain because the marketing claims from Brex, Ramp, Vic.ai, Rillet, and every other AI-analyst vendor are *unfalsifiable without them*. A vendor who says "our AI reaches 95% accuracy on expense-report categorisation" is making a claim you cannot interrogate unless you know what benchmark they ran, on what distribution, with what human baseline. The benchmarks that matter for Block 2 Week 5 readers:

**FinanceBench (Islam et al. 2023, arxiv 2311.11944).**[^1] 10,231 questions drawn from publicly-traded companies' 10-K, 10-Q, and earnings-call transcripts. 150 of those are the "open source subset" with ground-truth answers and source-page evidence strings published on Hugging Face as `PatronusAI/financebench`[^2]. The original paper's headline result — 81% refuse-or-wrong for GPT-4-Turbo with retrieval — is the number to anchor on. Community runs on the 150-question open subset described Claude 3.5 Sonnet and GPT-4o in the 55–65% range with a well-tuned retrieval system, and Claude with code execution in the 70–78% range — but those model names are now mid-2024/2025 vintage. **The 2026 successor anchor is the Vals AI Finance Agent benchmark**, which tests tool-using models on complex financial questions over filings: Claude Opus 4.7 leads it at **64.37%** (Anthropic's own launch materials cite the same ~64% figure), a score that sounds low until you register that it is one of the hardest agentic benchmarks in existence and still short of human-analyst performance.[^13] Claim any of these numbers conservatively: the gap is real, the exact digits move with every prompt revision and every model generation (Opus 4.8, Sonnet 5, and Fable 5 all postdate the 64.4% Opus-4.7 figure). Run the open subset yourself — it should be part of your eval harness if you ship financial reports.

**FinQA (Chen et al. 2021, arxiv 2109.00122).**[^3] 8,281 question-answer pairs from earnings reports with 6,251/883/1,147 train/dev/test split. Each answer includes the arithmetic program required to derive it (the "gold program" — e.g. `subtract(2017_revenue, 2016_revenue), divide(#0, 2016_revenue)`). This makes FinQA uniquely useful: you can evaluate not just *did the model get the right number* but *did it get there through the right reasoning chain*. A model that produces the right final number via the wrong program is a latent bug waiting for a question where the wrong program generalises incorrectly.

**GSM8K / GSM8K-Hard / MATH.** GSM8K is saturated at the frontier (the current Claude Opus 4.8 / Fable 5, GPT-5.x, and Gemini 3.1 Pro tiers all score in the high 90s). It should no longer be cited as evidence of "LLM math ability" in any serious architecture document; the appropriate reference is *harder variants*: Scheherazade (arxiv 2410.00151) which algorithmically chains GSM8K problems to test long-range logical integration; GSM-Hard which uses larger numbers; and MATH/MATH-Hard for competition-level math. The signal from these is consistent: models that look "smart" at grade-school arithmetic degrade sharply when the chain of reasoning extends past 4–5 steps without external verification.

**TATQA and TabLLM.** Table-QA-specific. TATQA pairs narrative paragraphs with tables; TabLLM evaluates few-shot tabular classification. For report-generator builders these are diagnostic rather than leaderboard-chasing: they tell you where your parsing pipeline is leaking (the answer is in a footnote the parser dropped) vs where your reasoning is failing (the answer is in the table but the model can't aggregate correctly).

The live controversy is how much of the FinanceBench gap has actually closed since November 2023. The Brex and Ramp marketing claims — Brex's public close-cycle reduction numbers, Ramp's spend-insight accuracy claims (Monday's lesson surveyed these) — are *specific to curated workflows* (expense categorisation, invoice coding, vendor matching) where the input distribution is narrow and the evaluation rubric is well-defined. They do not transfer to "ask the AI about our P&L" because P&L questions are open-ended and the error surface is enormous. An honest 2026 summary: frontier LLMs with retrieval and code execution are *viable* for audit-adjacent financial reporting when paired with a verification harness and human gating. They are not viable as unattended analysts.

## Layer 3 — Code-execution offloading: the dominant mitigation, and when it breaks

Anthropic's code execution tool[^6][^7] is the most frictionless way to do PAL-style offloading inside a production agent loop. The API exposes a sandboxed Python runtime (with bash and file manipulation across multiple languages) that the model can call mid-response. Pricing as of mid-2026: container time bills at $0.05/hour after a free monthly allowance (current docs frame this as ~1,550 free container-hours/month per organisation), and code execution is **free when bundled with the current `web_search_20260209` / `web_fetch_20260209` tool versions** — the bundling condition is now tied to those dated tool versions, not the older `web_search` / `web_fetch` names, so re-check it if you pinned earlier versions.[^8] OpenAI's Code Interpreter (now Assistants API file search + code execution) is the functional equivalent. LangChain exposes `PythonREPLTool`; for production-grade isolation most teams use a purpose-built sandbox — e2b.dev, Riza, or Modal's serverless containers.

The mechanism for analytical reasoning is a specific three-move pattern. Move one: the model reads the question and the context and decides *whether this is a question that requires computation*. Move two: if yes, the model writes a short Python program that loads the relevant data (usually already parsed into a pandas DataFrame or a dict), performs the computation, and prints the result. Move three: the runtime executes the program, the stdout (or the structured return) is fed back as a tool-result message, and the model narrates the answer using the verified number.

The correct tool definition for a report-generator's verify tool looks roughly like this (Claude tool-use schema):

```json
{
  "name": "run_python",
  "description": "Execute Python code in a sandboxed runtime with pandas, numpy, and the pre-loaded dataframes: ledger_df (general ledger, rows=journal entries), revenue_df (invoices by period), and prior_period_df (same-period prior-year ledger). Use this for ALL numerical aggregations, deltas, ratios, and multi-step calculations. Return the computed value plus a one-line reasoning trace.",
  "input_schema": {
    "type": "object",
    "properties": {
      "code": {"type": "string", "description": "Python code. Must end with a print() of the result."},
      "expected_type": {"type": "string", "enum": ["scalar", "series", "dataframe", "text"]},
      "units": {"type": "string", "description": "USD, bps, pct, ratio, count."}
    },
    "required": ["code", "expected_type", "units"]
  }
}
```

The `units` field is the one non-obvious design decision. Forcing the model to declare the unit of the expected result catches the unit-confusion failure mode at the tool-call layer rather than the narration layer. If the orchestrator sees a tool-call that computes a basis-point difference but declares units "pct", it can reject the call and force a rewrite before the number ever reaches the narrative. This is the kind of deterministic guardrail that raises audit-grade accuracy by more than any prompt tweak ever will.

Code-execution offloading is not a universal win. Three classes of question where it either fails or is unnecessary:

**Questions where the data isn't in the sandbox.** If the answer requires a piece of domain knowledge that lives in the model (what does "accretion to cash" mean in an M&A context? which line items in this vendor's 10-K correspond to standard SaaS ARR?) no amount of Python will help. The fix is retrieval (Week 4 patterns) or few-shot examples, not more code execution.

**Questions where the code you'd write is trivially the question.** "What was total revenue in Q4?" is a single `df.loc[df.quarter=='Q4', 'revenue'].sum()`. Offloading adds latency (typically 2–4 seconds in Anthropic's sandbox) and an extra failure surface (the sandbox can time out, the dataframe can be shaped wrong, the import can fail in cold-start). For one-shot aggregations against small frames, a well-constrained CoT is often cheaper and faster. The heuristic: offload when the answer requires >1 arithmetic operation *or* when the output will be cited in writing, whichever is stricter.

**Questions where the sandbox state is wrong.** The most embarrassing production failure I know of came from a report generator that had correctly loaded `ledger_df` but the model wrote code against a column name that had been renamed three months earlier. The runtime returned a KeyError, the model retried with a best-guess column name, and shipped a number computed against the wrong column. Fix: the tool definition should include the actual current schema of every pre-loaded dataframe in its `description` field, and the orchestrator should validate column references before execution.

## Layer 4 — Self-correction loops: what actually works, what doesn't

The Karpathy-style skepticism about intrinsic self-correction — the model that produced the wrong answer sitting in judgment of its own wrong answer — has a serious empirical grounding. (I am reaching for the archetype of the critique here rather than citing a specific Karpathy post; his public running commentary on RL reward-hacking and on LLMs as "simulators" converges on this shape, but the sharpest written version of the argument is the peer-reviewed paper below.) Jie Huang and collaborators' ICLR 2024 paper *Large Language Models Cannot Self-Correct Reasoning Yet* (arxiv 2310.01798)[^5] is the canonical reference. Across GSM8K, CommonSenseQA, and HotpotQA, they show that *intrinsic* self-correction — where the model critiques its own output with no external feedback — either fails to improve accuracy or actively degrades it. The TACL 2024 survey *When Can LLMs Actually Correct Their Own Mistakes?*[^12] tightens this to a precise claim: self-correction's efficacy is no better than self-consistency when you hold the number of total samples constant. Reported improvements in earlier work came from using a sub-optimal initial prompt and a more informative correction prompt; the "correction" was really "better initial prompting in disguise."

But the story does not end there. The same Huang paper is explicit that when *valid external feedback* is available, incorporating it in the self-correction loop produces real gains — code generation with execution results fed back is the canonical example. This is the load-bearing distinction for analyst-replacement workers: **external feedback works, intrinsic self-reflection does not**. An evaluator-critic loop that has access to a *different signal* than the original generator — a code execution result, a retrieval-grounded fact, a deterministic rule check — is a different architecture than the loop Huang critiqued. It is closer to Wang et al.'s self-consistency[^9] (arxiv 2203.11171; +17.9% on GSM8K over CoT) combined with a verifier.

The 2025 work *S²R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning*[^10] (ACL 2025) and the concurrent TACL critical survey[^12] converge on a practical rubric. An evaluator-critic loop delivers real accuracy gain when the critic:

1. Has access to a signal the generator did not (code execution result, retrieval hit, rule check).
2. Is prompted with the *specific failure taxonomy* for this domain, not a generic "check for errors."
3. Can only *flag and reroute*, not *overwrite*. The critic's output is an instruction to re-run with different tooling, not a direct answer substitution.

A prompt skeleton for a numerical-report critic that meets all three:

```
You are a financial-report critic. The DRAFT below contains N numerical claims.
For each claim, verify by running the relevant query against the sandbox-loaded
dataframes (ledger_df, revenue_df, prior_period_df). Return a JSON list where
each entry has: {claim_text, claim_type, verified_value, drafted_value, match,
failure_mode}. failure_mode must be one of: none | aggregation_off_by_one |
unit_confusion | sign_error | hallucinated_source | rounding_chain | out_of_scope.

Do NOT rewrite the draft. Return ONLY the verification JSON. The orchestrator
will decide whether to re-draft based on your output.
```

This prompt enforces all three properties. The critic *must* use the code execution tool (external signal). It is primed with the specific failure taxonomy. It cannot write the final report — it can only produce a structured verdict that the orchestrator acts on.

On my own pilots I have seen this pattern move numerical-accuracy rates on a 30-question weekly-ops eval from roughly 68% (single-shot generation, no tools) to 86% (generation + code-execution inline) to 94% (generation + code-execution + critic with forced tool-use). These are *indicative, not benchmarked* — single-operator runs on hand-crafted eval sets against a specific weekly-ops corpus, not a controlled study. Treat them as directionally useful (the ordering and the rough gap size are robust across the pilots and match the PAL/self-consistency literature) but do not cite the exact digits as though they were a public benchmark; run the three-arm eval on your own corpus before you stake a client commitment on the numbers. The last 6% is genuinely hard — most of it is domain-knowledge questions where the sandbox can't help — and should be routed to a human gate, not to another LLM.

## Operator case studies / war stories

**Patronus AI's public teardown of GPT-4-Turbo on FinanceBench, November 2023.** Anand Kannappan and Pranab Islam shipped the FinanceBench paper and an accompanying launch post explicitly to make this point: state-of-the-art models with retrieval refused or incorrectly answered 81% of 150 manually-reviewed questions drawn from real 10-Ks[^1][^2]. The data is available on Hugging Face and the GitHub repo is open; the 150-question subset is the cleanest small-N eval harness you can drop into a report-generator build in under a day. Patronus's own consulting practice (announced in 2024) is built on the observation that most enterprise AI-in-finance pilots fail specifically because they ship without ever running a FinanceBench-class eval against their own docs.

**Hamel Husain's eval-driven-development posts, parlance-labs.com and hamel.dev, 2024–25.**[^11] Husain — 20+ years ML, ex-Airbnb, ex-GitHub, now independent at Parlance Labs — has documented across dozens of client engagements that the single strongest predictor of a production AI product working is whether the team built an eval harness *before* the first generation run. His LLM-as-judge writeup specifically addresses the Karpathy-style concern: LLM judges work when (a) the judge is a different model-and-prompt than the generator, (b) the judge is calibrated against a human-labelled gold set first, and (c) the judge's rubric is concrete enough to be auditable. His claim (documented at hamel.dev/blog/posts/llm-judge/) is that teams that skip calibration ship judges that agree with the generator in ways that look like accuracy but are actually shared failure modes.

**Anthropic's advanced-tool-use upgrade to code execution[^7].** The successive code-execution releases added bash, multi-language, and file manipulation to the Claude sandbox (the current tool-type versions are `code_execution_20260521` / `code_execution_20260120`), and Anthropic's engineering post on advanced tool use made the explicit architectural pitch: Claude should be a data analyst that iterates on computations, not a code-writing assistant that hands off. The engineering implication for report-generator builders: the sandbox is now stateful enough across a single turn that you can load a ledger, run fifteen computations, generate a chart, and return a structured result — all without spinning up external infrastructure. This dramatically lowers the build cost of the PAL pattern for small teams.

## Runnable experiment

Open Claude Code in a fresh session. You will build a four-phase numerical-reasoning eval on a real dataset you control.

**Phase 0 — corpus.** Pick one: (a) a public 10-K of a company you know (Brex, Ramp, Shopify, whatever you've actually read), downloaded to `./corpus/10k.pdf`; (b) a Stripe or QuickBooks export for a business you have access to; (c) a synthetic ledger generated from a realistic schema. You need ≥ 50 rows of tabular data and enough context to generate 20 distinct numerical questions.

**Phase 1 — generate the question set.** In Claude Code:

> *"Read `./corpus/` and generate 20 numerical questions with ground-truth answers. Distribute them across: 5 single-aggregation (e.g., total revenue in period), 5 multi-step arithmetic (e.g., YoY margin expansion in bps adjusted for one-time items), 5 sign-and-direction (e.g., did working capital tighten or loosen QoQ and by how much), 5 edge/ambiguous (e.g., questions where the answer depends on a definitional choice the document hedges on). Output as `eval_set.jsonl` with fields: id, question, gold_answer, gold_units, gold_program (the calculation steps), difficulty. Verify each gold answer by running the calculation yourself in the code execution sandbox and citing the source-page for each input value."*

Hand-check 5 of the 20 for accuracy before you proceed. The model will be wrong on about 1 in 10 at the gold-answer-generation step; the hand-check catches this before you spend eval tokens comparing model output to wrong gold.

**Phase 2 — three-arm comparison.** Ask Claude Code:

> *"For every question in `eval_set.jsonl`, run the same question through three approaches (parameterise the model as `$MODEL` so this survives model churn — default to the current Anthropic flagship, e.g. Opus 4.8; note these models no longer accept a `temperature` parameter, so drop it rather than setting temperature 0):
> (A) `$MODEL` pure CoT, no tools.
> (B) `$MODEL` with the code execution tool enabled, same prompt, forced tool-use on numerical claims.
> (C) `$MODEL` generator → critic loop: arm B produces a draft; a second call with the critic prompt (from Layer 4 above) verifies each numerical claim via code execution and returns a structured verdict; if any claim fails verification, re-draft with the verified values.
> For each arm and each question, log: predicted_answer, predicted_units, wall_clock_latency, input_tokens, output_tokens, error_category (one of: none | aggregation_off_by_one | unit_confusion | sign_error | hallucinated_source | rounding_chain | out_of_scope). Emit `results.csv`."*

**Phase 3 — inspect the disagreements.** Ask Claude Code:

> *"From `results.csv`, surface the rows where arm A and arm B disagree, and separately the rows where arm B and arm C disagree. For each, retrieve the trace (CoT reasoning for A, tool-call code for B, critic verdict for C) and produce a short per-row diagnostic: which failure mode is present, and what architectural fix would close it (better tool description, better critic prompt, human gate, retrieval)."*

**Phase 4 — codify the rule.** Write a 500-word memo: for your specific corpus and question distribution, which arm wins on which question class? Where does code execution flip the ranking? Where does the critic add real value vs just add tokens? What is the single heuristic (question shape, data shape, required reasoning depth) you would codify as the rule for when to offload?

Expected shape of results on a well-constructed eval: arm A in the 55–70% range, arm B in the 78–88% range, arm C in the 88–95% range. If your arm C is not above arm B, the critic is not doing its job — inspect the critic prompt for whether it is actually using tools or just generating plausible-looking agreement.

## Problem set

1. **Build your own 20-question eval.** Construct it on a real corpus you have access to, following Phase 1 above. Report: arm A accuracy, arm B accuracy (Claude with code execution), arm C accuracy (with critic loop). Pass criterion: you have hand-verified 10 of the 20 gold answers and can defend every gold-answer derivation.

2. **Take a position.** *"In 2026, shipping any LLM-generated claim into a board document without a deterministic runtime verification is malpractice."* Defend or refute in ≤ 400 words, citing ≥ 3 benchmark numbers (FinanceBench, FinQA, GSM8K-Hard, or equivalent) and naming which specific failure modes your position protects against or tolerates.

3. **Design the critic.** Write an evaluator-critic prompt specialised for *your* hardest question class (the one where arm C most helped in the runnable experiment). It must use external signal (code execution, retrieval, or rule check), name the specific failure taxonomy, and produce a structured verdict rather than a rewrite. Report before-and-after accuracy on the 5 hardest questions.

4. **Identify an offload failure.** Find one question in your eval where code execution *doesn't help* (the answer requires domain knowledge the model lacks or the data is out of sandbox). Specify the architectural fix: retrieval over a domain knowledge base (Week 4 patterns), few-shot examples, or a human gate with a specific human-time budget. Defend the choice.

5. **Engage Karpathy's critique.** Give two specific cases, drawn from your eval, where same-model self-correction is *demonstrably robust* (and explain why the external-signal condition is met) and one where it is *illusory* (the critic agrees with the generator for the wrong reason). Cite the Huang 2024 paper[^5] in your framing.

## Common failure modes at scale

The following are the production-grade failure modes I and operators I have talked to have seen hit real AI-analyst deployments in 2024–25. The list is not exhaustive but it is weighted.

**Sandbox state rot.** You pre-load a set of dataframes at the start of a weekly run. Six weeks in, upstream schema has drifted (a column renamed, a new tax jurisdiction added, a currency conversion layer inserted) and the model's tool calls now silently reference stale column names. The runtime returns partial results, the model narrates around them, and the report ships with numbers that are internally consistent but based on the wrong slice of data. Fix: schema-validate the pre-load at every run start; fail loud on schema drift rather than continuing.

**Critic collapse.** The critic is *the same model* as the generator with a slightly different prompt, and under load it starts producing critic outputs that agree with the generator's output by default — the Huang 2024 failure mode, in production. Fix: force the critic to emit evidence (the tool call it ran, the result it got) for every verdict, not just the verdict itself. If the critic cannot cite its tool output, reject the response.

**Tool-call storm.** The model over-uses the code execution tool, spawning 40 small tool calls where 3 would do. Latency balloons, cost inflates 10x, and the final answer is marginally better. Fix: constrain tool-use with a prompt-level budget ("you may call `run_python` at most 5 times per response") and log call counts; alert when average calls per generation exceeds target.

**Unit-confusion that passes the critic.** The generator says "margin expansion of 4 points" where the right answer is 40 bps. The critic, unprompted about units, verifies the *arithmetic* (4 is indeed 400bps/100) but misses that the generator's rendered text says "points" which a CFO reader will parse as percentage points. Fix: the `units` field in the tool-call schema is not enough; the critic must verify that rendered narrative uses units consistent with the tool's declared units. Add a text-level units check to the critic rubric.

**Rounding compounding under long multi-step chains.** Four arithmetic operations each rounded to one decimal produce a final number that differs from the unrounded compute by 1–3%. The model narrates every intermediate value correctly — which is what makes this failure so insidious. Fix: run all intermediates in raw precision inside the sandbox and round only at render time; the tool-call schema should return raw values and render formatting should be a separate, deterministic step.

**Out-of-sandbox hallucinations in "just narrate" prompts.** After the numerical verification pass, operators sometimes add a "now write this up in 3 paragraphs" step — and the narration stage introduces *new* numerical claims that were never verified. Fix: constrain the narration stage to a schema where numbers can only come from a verified-values dictionary passed in by the orchestrator; any number not in the dictionary is a bug.

## Open questions / what's not settled

1. **Does the 49% retrieval-miss reduction Anthropic reported for Contextual Retrieval (Sep 2024) transfer to financial-document QA at scale?** Anthropic's five test domains did not include financial filings. There is no published head-to-head on FinanceBench with Contextual Retrieval vs standard hybrid retrieval. If you run one, publish it.

2. **Are frontier reasoning models (Claude Opus 4.8 / Fable 5 with adaptive thinking, GPT-5.x) changing the code-execution calculus?** The signal is still mixed in mid-2026: adaptive-thinking models close some of the arithmetic gap via longer internal reasoning, but they also raise latency and cost to a point where bundling with code execution remains the right default for production — and this needs re-testing against the current Fable-5-class tier rather than being left at the "early 2025 data is mixed" read the April draft carried. The open question is whether the reasoning models become good enough that inline code execution for arithmetic is *redundant*. I'd bet against, but the gradient is real.

3. **What is the right human-gate threshold?** Every production deployment I've seen ends up with some humans-in-the-loop; the unsettled question is where. The conservative position (Barry McCardel / Hex) is that any claim cited by an executive needs a human review gate. The aggressive position (Brex / Ramp workflows) is that specific narrow categories (expense categorisation, invoice coding) can run unattended once eval accuracy exceeds a threshold. The 2026 consensus is probably going to land at "unattended for narrow-workflow closed-loop tasks, human-gated for any open-ended analytical claim." Build accordingly.

## Reviewer lens — named critics with specific disagreements

- **Karpathy-style skepticism** (archetype, not a specific cited post) would push back on the claim (Layer 4, paragraph 4) that evaluator-critic loops reliably produce accuracy gains. The shape of the critique — visible across Karpathy's public writing on RL reward-hacking, LLMs-as-simulators, and his general bearishness on self-generated training signal — and the Huang et al. ICLR 2024 paper[^5] converge: a critic drawn from the same base model will produce outputs correlated with the generator's failures. My reply: the architecture I described *does not* meet his definition of intrinsic self-correction — it requires external signal (code execution result) as a precondition for any verdict. If the critic lacks tool-use it collapses to his critique; I agree. The lesson should (and does) make this distinction explicit.

- **Hamel Husain** (parlance-labs.com[^11]) would push back on the Phase 1 instruction in the runnable experiment — "hand-check 5 of the 20 for accuracy." His published guidance is that hand-verification of gold-standard evals is done against *the full set*, because the 25% sample rate I suggested catches gross errors but misses subtle ones (especially unit-confusion in the gold-answer generation itself). His recommended rigor: hand-check 100% of an eval set the first time you build it; re-audit whenever the underlying corpus changes. I'd split the difference in practice — hand-check 100% of eval sets ≤ 20, sample-check only on larger sets — but Husain's rigor is the correct default for anything that ships to a paying client.

- **Jerry Liu** (LlamaIndex, via his 2024/25 LlamaIndex blog posts on financial-document QA) would push back on the Layer 2 claim that Claude + code execution reaches 70–78% on FinanceBench open-subset. His published comparison posts consistently show that *specialised* financial-document pipelines (LlamaParse + domain-tuned prompts + multi-hop retrieval) outperform generalist code-execution loops on FinanceBench-adjacent evals. My concession: for serious deployments in finance specifically, a specialised pipeline probably wins; the code-execution-first architecture in this lesson is the right default for *generalist analyst workers* where you don't want to re-engineer the stack per domain. Cite both.

- **Jason Liu** (jxnl.co, Instructor author) would push back on the tool-definition JSON in Layer 3 — specifically the free-text `code` field. His consistent Instructor-project position is that unstructured code strings inside tool definitions lose type safety and make downstream verification harder. The stricter design would use a typed DSL (a structured `operations` field with `type: aggregate | delta | ratio`, typed `column` references, typed `filter` clauses). I'd agree for narrow domains where the operation space is bounded; for open-ended analytical questions the DSL collapses back to arbitrary Python and you're worse off. The honest framing: typed DSL wins for narrow workflows, free-text Python wins for open-ended analysis, and most report generators have both.

- **Douwe Kiela** (Contextual AI, co-author on FinanceBench[^1]) would push back on the whole framing that code execution is the dominant mitigation. His public position (Contextual AI's 2024/25 work on grounded generation) is that the *retrieval-grounding* layer is the more important fix — most LLM failures on financial QA come from the model computing against wrong or hallucinated source values, not from arithmetic failure. My concession: retrieval quality is *upstream* of everything in this lesson; if you are getting the wrong source numbers, no amount of code execution helps. But the failure taxonomy in Layer 1 is specifically about what happens *after* you have the right numbers loaded — and at that layer, code execution is decisive.

## Further reading

**Must-read (start here):**
- Huang et al., *Large Language Models Cannot Self-Correct Reasoning Yet* — ICLR 2024. arxiv.org/abs/2310.01798[^5]
- Islam et al., *FinanceBench* — arxiv.org/abs/2311.11944[^1] + Patronus AI launch post[^2]
- Gao et al., *PAL: Program-Aided Language Models* — ICML 2023, arxiv.org/abs/2211.10435[^4]
- Anthropic code execution tool docs — platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool[^6]
- Hamel Husain, *Using LLM-as-a-Judge For Evaluation* — hamel.dev/blog/posts/llm-judge/[^11]

**Recommended:**
- Chen et al., *FinQA* — EMNLP 2021, arxiv.org/abs/2109.00122[^3]
- Wang et al., *Self-Consistency Improves Chain of Thought* — arxiv.org/abs/2203.11171[^9]
- Kamoi et al., *When Can LLMs Actually Correct Their Own Mistakes?* — TACL 2024[^12]
- Anthropic, *Advanced Tool Use on the Claude Developer Platform* — anthropic.com/engineering/advanced-tool-use[^7]

**Optional:**
- S²R (ACL 2025)[^10] for the RL-trained self-verify frontier.
- Scheherazade (arxiv 2410.00151) for GSM8K-Hard-style chained-reasoning evals.
- Patronus AI's `financebench` GitHub repo[^2] for the 150-question open subset and a reference evaluation harness.
- Vals AI Finance Agent benchmark[^13] — the 2026 tool-using successor anchor to FinanceBench's original configuration numbers.

## Citations

[^1]: Islam, P., Kannappan, A., Kiela, D., Qian, R., Scherrer, N., Vidgen, B. (2023). *FinanceBench: A New Benchmark for Financial Question Answering.* arXiv:2311.11944, submitted 2023-11-20. https://arxiv.org/abs/2311.11944 — supports the 10,231-question scope, the 150-question manually-reviewed open subset, and the headline "GPT-4-Turbo with retrieval refused or incorrectly answered 81% of questions" finding. Verified 2026-04-17.

[^2]: Patronus AI (2023). *Patronus AI Launches FinanceBench, the Industry's First Benchmark for LLM Performance on Financial Questions.* patronus.ai/announcements/patronus-ai-launches-financebench; plus the open subset hosted at huggingface.co/datasets/PatronusAI/financebench and the methodology repo at github.com/patronus-ai/financebench. Supports the public availability of the 150-question subset and the reproducible evaluation harness. Verified 2026-04-17.

[^3]: Chen, Z. et al. (2021). *FinQA: A Dataset of Numerical Reasoning over Financial Data.* EMNLP 2021, arXiv:2109.00122. Supports the 8,281-pair corpus size, the gold-program-annotation structure, and the early GPT-3 baseline gap vs human expert performance (48.56% vs ~89%). Verified 2026-04-17.

[^4]: Gao, L., Madaan, A., Zhou, S., Alon, U., Liu, P., Yang, Y., Callan, J., Neubig, G. (2022/2023). *PAL: Program-Aided Language Models.* arXiv:2211.10435, ICML 2023. https://arxiv.org/abs/2211.10435 — supports the code-offload-beats-CoT claim (PAL-Codex 72.0% on GSM8K vs CoT 65.6%) and the mechanism description. Verified 2026-04-17.

[^5]: Huang, J., Chen, X., Mishra, S., Zheng, H.S., Yu, A.W., Song, X., Zhou, D. (2023/2024). *Large Language Models Cannot Self-Correct Reasoning Yet.* arXiv:2310.01798, ICLR 2024. https://arxiv.org/abs/2310.01798 — supports the intrinsic-self-correction-fails claim and the external-feedback-works caveat. Verified 2026-04-17.

[^6]: Anthropic. *Code Execution Tool — Claude API Docs.* https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool. Supports the Python/bash/multi-language sandbox description and container retention. Verified 2026-07-17. (Current tool-type versions are `code_execution_20260521` / `code_execution_20260120`, superseding the April draft's `code-execution-2025-08-25` reference.)

[^7]: Anthropic Engineering (2025). *Introducing Advanced Tool Use on the Claude Developer Platform.* anthropic.com/engineering/advanced-tool-use. Supports the October 2025 advanced-tool-use launch, the multi-language/bash/file-manipulation upgrades, and the "Claude as data analyst, not code-writing assistant" framing. Verified 2026-04-17.

[^8]: Anthropic, code-execution tool docs and pricing, https://platform.claude.com/docs/en/agents-and-tools/tool-use/code-execution-tool and https://platform.claude.com/docs/en/about-claude/pricing. Verified 2026-07-17. Supports: $0.05/container-hour after a free monthly allowance (docs frame ~1,550 free container-hours/month per org); code execution free when bundled with the current `web_search_20260209` / `web_fetch_20260209` tool versions (the bundling condition is now tied to those dated versions, not the older tool names).

[^9]: Wang, X., Wei, J., Schuurmans, D., Le, Q., Chi, E., Narang, S., Chowdhery, A., Zhou, D. (2022). *Self-Consistency Improves Chain of Thought Reasoning in Language Models.* arXiv:2203.11171. Supports the +17.9% GSM8K gain over CoT and the self-consistency mechanism as the decoding baseline against which self-correction must improve. Verified 2026-04-17.

[^10]: S²R team (2025). *S²R: Teaching LLMs to Self-verify and Self-correct via Reinforcement Learning.* ACL 2025, aclanthology.org/2025.acl-long.1104. Supports the 2025 frontier claim that RL-trained self-verify can recover some of the self-correction gains Huang 2024 ruled out — specifically when the verifier has access to external signal. Verified 2026-04-17.

[^11]: Husain, H. (2024–25). *Your AI Product Needs Evals* (hamel.dev/blog/posts/evals/), *Using LLM-as-a-Judge For Evaluation* (hamel.dev/blog/posts/llm-judge/), and the Maven course *AI Evals For Engineers & PMs* (maven.com/parlance-labs/evals). Supports the eval-driven-development claim, the LLM-as-judge calibration requirements, and the 35+-product operator base. Verified 2026-04-17.

[^12]: Kamoi, R. et al. (2024). *When Can LLMs Actually Correct Their Own Mistakes? A Critical Survey of Self-Correction of LLMs.* TACL 2024, direct.mit.edu/tacl/article/doi/10.1162/tacl_a_00713. Supports the claim that self-correction's efficacy collapses to self-consistency under matched sampling budgets, and the taxonomy of when external-feedback loops do and do not help. Verified 2026-07-17.

[^13]: Vals AI Finance Agent benchmark, https://www.vals.ai/models/anthropic_claude-opus-4-7 and https://www.vals.ai/home; plus Anthropic, "Advancing Claude for Financial Services," https://www.anthropic.com/news/advancing-claude-for-financial-services. Verified 2026-07-17. Supports: Claude Opus 4.7 leading the Vals AI Finance Agent benchmark at 64.37% (a tool-using agentic evaluation over financial filings) as the 2026 successor anchor to FinanceBench's original 2023 configuration numbers. Note the model lineup has since advanced (Opus 4.8, Sonnet 5, Fable 5), so re-check the live leaderboard before quoting a client.

_last_verified: 2026-07-17_
