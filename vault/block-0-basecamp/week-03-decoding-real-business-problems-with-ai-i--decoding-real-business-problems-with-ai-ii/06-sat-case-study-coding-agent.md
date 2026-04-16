---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: sat
day_name: sat
session_slug: decoding-real-business-problems-with-ai-ii
title: 'Case study teardown — coding agents as a business (Cursor, Claude Code, Devin, Copilot) under the four-step pipeline'
study_date: 2026-05-16
tags: [case-study, coding-agents, cursor, claude-code, devin, github-copilot, swe-bench, pricing, unit-economics, metr, evals]
sources:
  - anthropic-claude-sonnet-4-5
  - anthropic-claude-opus-4-5
  - metr-2025-developer-productivity
  - cursor-pricing-2025
  - devin-pricing-2025
  - anthropic-claude-code-inflection-2026
  - techcrunch-cursor-9-9b-valuation
  - github-copilot-15m-seats
  - klarna-reversal-2025
  - swe-bench-pro-scale
  - swe-bench-illusion-arxiv-2506
  - hamel-husain-field-guide
  - cognition-swe-bench-technical-report
  - boris-cherny-lennys
last_verified: 2026-04-15
word_count_target: 6200
---

# Case study teardown — coding agents as a business, the whole four-step pipeline run end-to-end

## Why this matters

You have spent four days this week on an abstract pipeline: **discovery → fit → scoping → pricing**. Monday was jobs-to-be-done and why "AI opportunity lists" mislead. Tuesday was whether AI is the right tool at all. Wednesday was scoping with kill criteria and eval gates. Thursday was pricing — value-based versus time-based, cost pass-through, margin math. Friday ran the pipeline once, on customer-support agents (Klarna, Intercom, Decagon). Today runs it again on the domain you and your clients probably have the strongest gut-feel for and therefore the most trouble thinking clearly about: **coding agents as a category**.

The goal of today is not to help you pick a tool. The market will re-sort the tools twice before this week ends. The goal is that after today, when a founder, a CTO, or a head of engineering drops "*we should deploy Devin*" or "*our developer productivity is up 40%, Copilot is paying for itself*" into a meeting, you can open the discovery → fit → scoping → pricing pipeline in your head, walk through it in five minutes, and produce a sharper decision than everyone else in the room. Same muscle Friday built on support agents. Different domain, sharper controversies, richer numbers.

By the end you should be able to:

1. Read a published SWE-bench Verified score and state out loud the three things it does not tell you about whether a coding agent will work on a given codebase.
2. Cost any of Cursor, Claude Code, Copilot, or Devin per active developer per month using public pricing and a realistic token or seat assumption — and spot when a vendor's "cheap" tier is leaking margin to the underlying model provider.
3. Name the two live positions in the "does a senior developer actually ship more code with AI?" debate, cite the specific 2025 randomized controlled trial at the centre of it, and state what would have to be true for one side to be right.
4. Distinguish the enterprise procurement lens (SOC 2, audit logs, VPC, data residency, seat governance) from the indie-builder lens (speed of iteration, raw capability, cost per task) — and explain why one category leader can serve only one of those markets well.

Tomorrow's lesson synthesizes Week 3. This lesson is the closing worked example.

## Prerequisites

- Monday–Friday of this week. The four-step pipeline names below (discovery, fit, scoping, pricing) refer to the rubrics you built earlier in the week. Fine to read standalone, but the vocabulary assumes you've seen them.
- Claude Code and a Claude.ai account. One exercise has you direct Claude Code to read a SWE-bench-style issue and reason about it; another is a manual pricing comparison run in Claude.ai.
- No coding. Every exercise is directed-through-AI or analytical.

## Framing — what a "coding agent" actually is in 2026, under the hood

Strip the marketing. A coding agent, circa April 2026, is a loop of four elements:

1. A frontier model (Claude Sonnet 4.5 / Opus 4.5, GPT-5 variants, Gemini 3 Pro) doing the actual reasoning and token generation.
2. A scaffolding layer that shapes that model's behaviour — file reads, shell execution, edit application, retry logic, sub-agent dispatch, planning prompts.
3. A surface — an IDE integration (Cursor, Copilot), a terminal tool (Claude Code), or a hosted async worker (Devin, Cognition Rainier).
4. A monetization wrapper — subscription, seat pricing, usage metering, enterprise contract.

Every tool in this category is a different bet about which of those four layers captures the most value. Cursor bet on #3 — own the IDE. Claude Code bet on #1+#2 — own the model and the scaffolding in terminal form. Copilot bet on #3+#4 — own the distribution inside GitHub and the enterprise procurement motion. Devin bet on a stronger version of #2+#3 — make the agent asynchronous, parallelizable, and remote, so a developer can delegate rather than pair. Those bets predict how each company prices, what its margin profile looks like, and where its moat either exists or doesn't. Hold that framing while we walk the pipeline.

## Step 1 — Discovery: what "job" is the developer actually hiring a coding agent for?

Monday's framework: a tool doesn't compete against other tools, it competes against other ways a user gets a job done. The failure mode in discovery is picking one slice of the job and mistaking it for the whole.

There are at least four distinct developer jobs currently labelled "AI coding assistance." They look superficially alike and are actually different businesses.

**Job A. "Autocomplete that doesn't make me feel stupid."** Inline completions while typing. Copilot 2022–2024 defined this category; Cursor's Tab is the current strongest instance. The competing alternative isn't another AI tool — it's IntelliSense, Sublime's fuzzy matcher, a good snippet config. The user wants keystroke reduction with low cognitive cost. Pricing tolerance: low — this is a utility, priced like IDE plugins, $10–$20/mo.

**Job B. "Pair-program with me on a defined task."** I open a file, I know roughly what I want, I chat with the model as it edits. The competing alternative is Stack Overflow + copy-paste, or a senior colleague. The user wants acceleration on work they already understand and would otherwise do themselves. Cursor Pro and Claude Code both sit here. Pricing tolerance: $20–$200/mo depending on depth.

**Job C. "Delegate this ticket and come back in 20 minutes."** I describe the bug or feature, the agent goes off, reads the repo, writes a PR, runs tests, opens a draft. The competing alternative is hiring a contractor, scheduling a junior engineer, or dropping the task from the backlog. Devin is the canonical bet here; Claude Code's headless mode, Cursor's background agents, and GitHub's new async Copilot agents all push in this direction. Pricing tolerance: much higher — $500–$2000/mo per "virtual engineer" is imaginable because the alternative is a salary.

**Job D. "Govern AI-generated code across an engineering org of 2,000."** Seat provisioning, SSO, audit trail, "which models are our developers actually sending code to," SOC 2, data-retention controls, secrets scanning on prompts. The competing alternative is banning AI code tools entirely. GitHub Copilot Enterprise and the enterprise tiers of Cursor and Claude Code compete here. Pricing tolerance: whatever the CISO will sign — $39/user/month for Copilot Enterprise, custom for the others.

Notice: Job A, B, C, D are not points on a scale of capability. They are *different jobs*. A product that wins A can lose B. A product that wins C can be structurally locked out of D because it was built by a startup without SOC 2. An organisation that evaluates on one job and deploys for another gets a predictable failure. This is the discovery trap and it is the single most common mistake in current coding-agent procurement conversations.

Operator implication: when someone says "we're evaluating coding agents," the first question is *"for which of A/B/C/D?"* and the second is *"how did you decide that's the right one to solve first?"* If they can't answer both, the evaluation is a shopping trip, not a discovery.

## Step 2 — Fit: is an AI coding agent actually the right tool, and for which job?

Tuesday's rubric asked, for any candidate AI project: *is the problem pattern a good fit for a probabilistic system at all? Is there a deterministic alternative that's strictly better? Is the cost of failure tolerable?* Apply it to each job.

**Job A (autocomplete).** Strong fit. The cost of a wrong completion is keystrokes — the developer presses Escape. Pattern matching on local context is precisely what transformer models are good at. Deterministic alternatives (LSP, snippets) cover narrow idioms but not open-ended "finish this function." Probabilistic cost: near zero. *Fit verdict: yes, and has been since ~2022.*

**Job B (pair programming).** Strong fit with caveats. Cost of a wrong suggestion is a compile error or failed test — cheap to catch if the developer is paying attention, expensive if they aren't. The deterministic alternative is a human reviewer, which doesn't scale to every keystroke. Probabilistic cost: moderate — reviewed by the developer before commit. *Fit verdict: yes, if the developer remains in the loop. The open controversy (section below) is whether they actually do.*

**Job C (delegated tickets).** Contested fit. This is where all the interesting arguments live. The cost of a wrong autonomous PR is a broken build, a subtle bug merged to main, a two-day junior-engineer clean-up, or worse — a security issue, a deleted table, a shipped hallucination. SWE-bench Verified top scores are roughly 80%+ as of late 2025 for the best agent scaffolds[^1][^2], which sounds high. But a 20% failure rate on delegated tickets means one in five PRs is wrong — a load that breaks code review if the volume is high, and an error-mode the current scaffolding doesn't self-detect reliably. Fit verdict depends entirely on how well the organisation can catch the wrong 20% before merge. Most can't.

**Job D (enterprise governance).** Fit is not about AI capability at all — it is about procurement, security, and integration. The question "is AI the right tool" has already been answered (yes, we're buying something); the question is *which vendor's enterprise product actually solves the CISO's problems.* The pipeline here is not discovery → fit → scoping → pricing in the original sense; it is compliance → integration → seat-governance → renewal.

Cross-job implication: a single vendor evaluation that tries to cover all four jobs simultaneously produces a rubric that can't distinguish between them. The first scoping move is almost always *"pick the one job we're going to actually measure."*

## Step 3 — Scoping: what does each vendor's current product actually do, with real numbers?

This is where the citations matter. Dates and URLs are in footnotes; I'll keep numbers in the prose.

**Cursor (Anysphere).** IDE fork of VS Code. Pro is $20/mo with unlimited Tab completions and $20 worth of premium-model credits; Business is $40/user/mo adding SSO, team controls, SOC 2; Ultra is $200/mo with ~20x the Pro credit pool.[^3] The June 2025 shift from request caps to model-API-priced credits is load-bearing — it means Cursor's gross margin on paid plans is capped by how much of the $20 their users burn in Claude / GPT API fees. ARR crossed $500M in June 2025 and passed $1B by the Series D in November 2025; public reports from April 2026 put annualized revenue north of $2B.[^4] Net dollar retention has been reported above 170%, an extraordinary number that (a) reflects real expansion and (b) creates a vendor-lock-in question the skeptical-CTO lens will ask below. Cursor wins Jobs A and B. Their background-agent and multi-edit features are pushing into Job C. Enterprise (Job D) is newer and lighter than Copilot's.

**Claude Code (Anthropic).** Terminal tool. Pricing rides on Claude subscriptions: Pro at $20/mo (insufficient for heavy use), Max 5x at $100/mo, Max 20x at $200/mo; or pay-as-you-go API at Sonnet $3 input / $15 output per million tokens and Opus $15 / $75.[^5] The real unit economics: across enterprise Claude Code deployments, Anthropic's own *Manage costs effectively* docs page and its September 2025 "Claude Code best practices" / pricing guidance indicate roughly $13 per active developer per active day, $150–$250 per active developer per month average, with 90% of users under $30/day.[^5] One oft-quoted developer's eight-month analysis: ~10 billion tokens consumed, which at API pricing would have been ~$15,000, but on Max 20x was $1,600 flat. Claude Code hit roughly $1B annualized run-rate by November 2025 and ~$2.5B by February 2026 — the fastest enterprise software ramp on record in its creators' telling.[^6] Claude Code wins Job B for AI-native operators and is pushing hard into Job C through headless / non-interactive mode; Job A is not its game (no IDE); Job D is shipping but less mature than Copilot Enterprise.

**GitHub Copilot (Microsoft).** The incumbent. Free for students / OSS maintainers; Pro $10/mo; Pro+ ~$19/user/mo; Enterprise $39/user/mo with compliance and audit.[^7] Reported ~4.7M paid subscribers by January 2026 — up 75% year-over-year — with ~20M total users; estimated ARR roughly $1B.[^8] Wins Job A by distribution and incumbency; Job D by integration into GitHub's existing enterprise procurement surface (the CISO has already approved GitHub). Job B is contested — power users trade down to Cursor or Claude Code for depth. Job C is shipping later than Devin or Claude Code's async modes.

**Cognition Devin.** Asynchronous agent. Originally $500/mo for 250 ACUs (an ACU is roughly 15 minutes of Devin active work); in April 2025 relaunched as Devin 2.0 starting at $20/mo with pay-as-you-go at $2.25/ACU; enterprise custom-priced with VPC deployment.[^9] This pricing reset is itself a scoping data point — the $500 tier wasn't sticking at the volume Cognition needed, so they re-segmented. Devin is the only vendor pitching hard at Job C natively: the value proposition is *"delegate the ticket and walk away."* SWE-bench Verified performance — we'll get to how much to trust that number — has climbed, and public case studies exist. The procurement question (Job D) is the harder one: enterprise customers evaluating Devin are asking about liability for autonomous merges, audit trails on what Devin decided and why, and how to roll back a 50-PR burst that contained one data-loss bug.

**Unit economics sanity check.** Model inference is the largest variable cost for any of these. A realistic Job-B session — a developer chatting with a coding agent for a few hours — consumes on the order of a few million tokens of Claude Sonnet inference when you account for file reads, conversation history, and tool-call loops. At API price that's a few dollars. A Claude Code Max 20x subscriber at $200/mo who burns through 10M tokens a day (a plausible heavy-use number) costs Anthropic many multiples of what they pay — but Anthropic serves the inference itself, so the "loss" is compute-time on models Anthropic owns. Cursor at Pro $20/mo serving a user who burns their entire $20 credit pool on Claude or GPT is operating at essentially zero marginal gross profit on that user before fixed costs; Cursor's margin depends on the many users who under-consume plus Business/Ultra seats. Copilot at Pro $10/mo paying its own GPT/Claude costs requires Microsoft-scale cost engineering to stay margin-positive; Copilot Enterprise at $39/user/mo has more headroom but also higher support and compliance load.

Scoping conclusion: **each vendor's price is tuned to its structural advantage.** Anthropic can price Claude Code low because it owns the model. Microsoft can price Copilot low because it owns the distribution. Cursor must price up (Business/Ultra tiers) because it owns neither. Devin prices premium because its job is the most valuable job if it works. Reading the pricing sheet tells you the strategic position.

## Step 4 — Pricing: value-based, seat-based, or usage-based, and why it matters which

Thursday's frame: pricing choice encodes what the vendor believes they are selling. Three patterns across the four vendors.

**Seat + usage credit (Cursor Pro, Claude Code Max).** The seat says "this user has access"; the credit pool says "this much inference is included." Good for buyers whose AI usage is bursty and hard to predict per-person; good for vendors because average usage stays below the cap and the cap is a psychological commitment, not a literal ceiling. Failure mode: heavy users feel squeezed (see the June 2025 Cursor rollout backlash — the migration from request caps to credit pools was widely read as a de-facto price hike and caused retention complaints), light users pay for unused capacity.[^3]

**Pure usage / ACU (Devin 2.0, Claude Code API pay-as-you-go).** The buyer pays for exactly what the agent does. Good for finance teams that need to attribute cost to projects; good for vendors because it removes the unit-economic risk of heavy users. Failure mode: buyers cannot predict monthly spend, which blocks enterprise approval — Devin's original $500 ceiling was in part an attempt to give procurement a budgeting number.

**Seat + enterprise (Copilot Enterprise, Claude Code Enterprise, Cursor Business).** Flat per-seat pricing with usage fair-use, plus security and compliance features. Good for large organisations that want predictable per-developer cost and centralized control. This is Job D's natural pricing shape. Failure mode: heavy users still exist and are cross-subsidized by light users; if the heavy-user-to-light-user ratio inverts, the unit economics break.

**The value-based pricing question nobody has solved well yet.** If a coding agent genuinely closes one Job-C ticket autonomously — a ticket that would have taken a mid-level engineer three hours — the value created is closer to $300 than to $9 (the cost of 4 ACUs on Devin). Why is no one capturing that value? Two reasons. First, verification: the agent can't prove it delivered the $300 of value because the PR still requires human review and sometimes the PR is wrong. Second, substitution risk: if one vendor prices at $300/ticket, a competitor at $50/ticket captures the market. The coding-agent category is in a classic race-to-the-bottom phase where capture-price is pinned to inference-cost-plus rather than value-created. Expect this to change — or to be forced to change — over the next 18 months.

## The live controversy — does AI actually make senior developers faster?

This is the single most contested empirical question in the coding-agent market right now. Know both sides.

**Position 1 — the optimistic / adoption-driven case.** Cursor, Claude Code, and Copilot publish self-reported productivity numbers from their user bases that consistently claim 25–55% acceleration on tasks. Cursor's retention and expansion numbers are consistent with users who believe they are faster with the tool. Boris Cherny, head of Claude Code at Anthropic, has said publicly that he writes 100% of his daily code through the tool — an extraordinary claim if true and not unusual among AI-native operators.[^10] The ambient vibe-coding discourse (Karpathy's original February 2025 tweet onward) assumes meaningful acceleration at least for exploratory and throwaway work.

**Position 2 — the measured / randomized-trial case.** In July 2025, METR published a randomized controlled trial: sixteen experienced open-source developers, each with roughly five years of prior experience on the repositories they were working in, completed 246 real tasks. Each task was randomly assigned either "AI allowed" (primarily Cursor Pro with Claude 3.5/3.7 Sonnet) or "AI disallowed." **Before the study, the developers forecast a 24% speedup from AI. After completing the study, they estimated AI had given them a 20% speedup. The measured reality was a 19% slowdown.** Developers took *longer* to complete tasks with AI tools than without. ML researchers and economists surveyed before the study predicted 38–39% speedups. Everyone was wrong in the same direction.[^11]

The METR finding is not a one-off. It is the best-designed trial we currently have on the question, and its result directly contradicts the self-reported productivity numbers. METR themselves have published follow-up notes updating the design for 2026 replication.

**Two positions, how to hold them.** The honest reading is that both positions are describing something real. The developers in METR's study *felt* faster even when they were slower — the subjective acceleration is real, the objective deliverable-throughput is not (on those tasks, with those tools at that time). The adoption and expansion numbers at Cursor and Claude Code are real too — people are willingly paying for something — but "willingness to pay" and "measurable throughput gain" are different variables. This is the same gap that shows up in every productivity-tool category (IDEs, code review tools, meeting software) where subjective felt-productivity leads measurable throughput by years or decades.

**Operator takeaway.** If you're briefing a client or a CTO on whether to deploy a coding agent, the honest answer in 2026 is: *expect real subjective improvement, expect measurable throughput improvement on well-scoped novel work where the agent isn't competing against existing context in the developer's head, and expect null-or-negative effects on tasks in mature codebases the developer already knows deeply.* The second category — new work — is most of the upside. The third category — old code the senior knows cold — is where the METR slowdown lives.

The follow-up empirical question, still open, is whether the gap closes as (a) models get better, (b) scaffolding gets better, and (c) developers get better at using the tools. METR's updated design aims to measure this longitudinally.

## Reviewer lens — named pushbacks from three specific positions

**Pushback 1. A skeptical enterprise CTO on SWE-bench Verified.** I cited 80%+ Verified scores above in the discussion of Job C fit. The CTO would argue this is a benchmark-to-production leap with three structural problems. First, **contamination**: any model trained on GitHub data after June 2024 has likely seen some subset of the 500 Verified problems including their solutions, and empirical work in 2025 showed direct solution-leakage in 30%+ of successful passes. SWE-bench Pro (Scale AI's response) has top scores roughly 27 points below Verified on the same tier of models; that gap is the contamination.[^12] Second, **environment**: Verified tasks are single-repo Python issues with high-quality test coverage. A typical enterprise codebase is multi-language, multi-repo, has flaky tests or no tests, has undocumented business logic, and half the time you can't reproduce the bug locally. Third, **scoring**: "resolved" means the tests pass. In production, "resolved" means the tests pass *and* a senior reviewer believes the fix is correct *and* it doesn't break adjacent systems *and* it matches architectural constraints no one wrote down. The 80% number is a floor on production performance, not a ceiling. OpenAI has publicly stopped reporting Verified scores and shifted to SWE-bench Pro partly for these reasons.[^12] The CTO's operational consequence: **discount any Verified score by something like 20–30 points when predicting in-codebase performance, and budget for human review as if the agent's accuracy is 50–60%.**

**Pushback 2. Hamel Husain on measurement.** Husain's consistent public position across his 2024–2025 writing: **the teams that succeed with AI products "barely talk about tools at all. Instead, they obsess over measurement and iteration."**[^13] He would push back hard on the whole category's current discourse — including much of what's in this lesson — as tool-first rather than measurement-first. Specifically: you and your client should not pick between Cursor / Claude Code / Copilot / Devin by reading reviews or running one trial. You should define **a binary pass/fail criterion per ticket type in your actual workflow**, run each candidate tool across N≥20 tickets of each type, and count. Husain's discipline — binary LLM-as-judge where possible, human-graded where not, measured agreement between judge and expert before you trust the judge, and systematic error analysis on failures — is what separates organisations that get real leverage from coding agents from those running on vibes. **If a client hasn't defined their pass/fail criterion, the agent-selection question is premature.**

**Pushback 3. A Cognition founder rebuttal.** The SWE-bench discount and the METR slowdown both land harder on interactive pair-programming tools than on async delegation tools. A Cognition founder would argue the right comparison for Devin is *not* "did Cursor make this senior faster on his own repo" — METR's exact setup — but *"did Devin complete this ticket without the senior touching it at all, freeing the senior for something else entirely."* The relevant metric isn't developer-minutes-saved; it's tickets-completed-autonomously-with-acceptable-quality. On that metric, a 60–70% autonomous-completion rate on well-scoped tickets is a different business from a 19% slowdown on deep-context work. The rebuttal has force on Job C specifically. It does not rescue Job B from the METR finding. And the "well-scoped tickets" qualifier is doing a lot of work — scoping tickets well enough for an async agent is itself a skill most engineering orgs haven't developed, which is part of why Devin's original $500/mo tier under-adopted.

All three pushbacks are compatible. Hold all three.

## Runnable experiment — feel the SWE-bench-style loop on one instance

You will not run SWE-bench end-to-end today. The point is to **feel the loop** that generates these benchmark numbers on one real instance, so the "80% Verified" shorthand becomes a felt intuition instead of a headline.

The experiment is illustrative — your specific run will vary depending on which model, scaffold, and instance you pick, and that variance is itself part of the lesson.

**Setup.** Open a fresh scratch folder. Open Claude Code in it.

**Instruction to Claude Code (copy-paste):**

> Pick one real, open issue from the `sympy/sympy` repository on GitHub that is (a) currently open, (b) has a linked test file or reproduction, and (c) is small enough to be plausibly solvable in a single session. Do not just pick issue #1 — pick something that looks like a real bug report. Report back: the issue number, a three-sentence summary of what's wrong, the file(s) you'd need to modify, and your estimate of whether this is in the set of bugs a coding agent like you would resolve on SWE-bench Verified. Then stop. Do not attempt the fix yet.

*Fallback if Claude Code refuses due to no web access:* open https://github.com/sympy/sympy/issues in a browser yourself, pick one matching (a)/(b)/(c), paste the issue title + body + any linked reproduction directly into the chat, and ask the same question. The exercise is about the scoping loop, not the browsing capability.

Observe what happens. Three things are interesting:

1. **How much of the reasoning is issue-reading vs repo-reading.** If Claude Code closes on an answer without reading the repo, that is the same shortcut the SWE-bench-illusion paper documented — models can identify buggy file paths from issue descriptions alone through memorization rather than reasoning.[^14]
2. **The agent's own confidence calibration.** It will give you an estimate. Is the estimate well-calibrated? You don't know yet, but notice whether it hedges or asserts.
3. **What it asks for.** If it asks you for anything — a specific file, a test, repo access — that is itself a signal about what the scaffolding is and is not doing for it.

**Follow-up instruction:**

> Now attempt the fix. Write the modified code to a new file. Do not apply it to the repo. When you're done, tell me: which tests would need to pass to claim this is resolved? Were you able to run them in this environment? If not, what would I need to give you to verify?

Observe:

- Whether the agent distinguishes "I wrote code that looks right" from "I proved the code passes the tests." This distinction is exactly the SWE-bench scoring semantics — "resolved" means tests pass, not that the code looks right.
- How many tool calls were spent on reading vs writing. Production agent loops often spend 80%+ of tokens on reading context and ~20% on generating fixes. Verified scores are sensitive to this ratio — scaffolds that read more score higher, at a real compute cost.
- Any point at which the agent hallucinates a file path, a function signature, or a test. This is the error-mode that the contamination critique is ultimately about. A model that has seen the SWE-bench solution in training doesn't need to read the repo to find the file; one that genuinely hasn't will get the file wrong sometimes.

**Reflection, not a quiz.** Run this on one issue. Then ask yourself: *if I had to run this at N=20 on tickets from my own codebase and count binary pass/fail according to my own test suite, what would I expect the pass rate to be?* That number — your honest expected pass rate — is your fit verdict for Job C in your domain. It is almost always lower than the vendor's SWE-bench number.

## Problem set

Five problems, each takes 10–30 minutes. Each produces an artifact you can reuse on a real engagement.

**Problem 1 — Classify the job.** Pick three engineering teams you know (your own, a client's, an imagined composite). For each, classify the job they are *actually* trying to solve — A (autocomplete), B (pair), C (delegate), D (governance) — by writing one sentence describing what "success looks like" to them. If you end up writing "all of the above," you haven't classified; pick one. Then name the tool they should evaluate first for that job, and the tool they should **not** waste a pilot on.

**Problem 2 — Unit-economics reality check.** For a team of 20 developers, compute the monthly seat cost at: (a) Cursor Pro for all, (b) Cursor Business for all, (c) Claude Code Max 5x for all, (d) Copilot Enterprise for all, (e) Devin 2.0 Core for all, (f) a mixed stack of Copilot Enterprise for the full org + Claude Code Max 20x for the five heaviest users. To identify the "heaviest 5" in practice: pull 30 days of per-seat token/request usage from the vendor admin dashboard (Anthropic Console usage tab, Cursor Business admin, or Copilot Enterprise admin analytics), sort by total tokens or active-day count, take the top 5; cross-check against Git commit or PR-volume logs to confirm usage correlates with output and isn't one power-user burning credits on a side project. Then ask: which is cheapest, and is cheapest the right frame? What breaks in option (f) that doesn't break in options (a)–(e)? (Hint: governance, integration, audit trail — the Job-D concerns from discovery.)

**Problem 3 — Take a position on METR.** Read the summary of the METR July 2025 study (URL in citations). In 200 words, take a position on one of these: (i) the 19% slowdown generalizes and most AI-coding productivity claims are folk knowledge; (ii) the slowdown is specific to deep-context mature-codebase work and will not appear on greenfield or unfamiliar-codebase work; (iii) the slowdown is a transitional phenomenon that disappears with better scaffolding and better-trained users. Your position must name one follow-up experiment that would falsify it.

**Problem 4 — Price a Job-C engagement.** You are advising a founder who wants to deploy an async coding agent (Devin or Claude Code headless) to close well-scoped bugs out of hours. The founder wants "$20,000/month of virtual-engineer throughput." Using public pricing, estimate: how many hours of agent work that buys, how many tickets that is at the current realistic pass rate, and what the implied cost per completed ticket is. Then argue for a pricing structure to sell this to the founder's customers. Seat-based? Per-ticket? Retainer?

**Problem 5 — Write the reviewer-lens email.** A client has just sent you a deck claiming their team is 40% more productive on Copilot based on self-reported survey data. Draft a one-screen reply that (a) doesn't insult the data, (b) names the METR contrast explicitly, (c) proposes a two-week pilot design that would produce a number you'd both trust. This is the measurement discipline from Pushback 2, made practical.

## Common failure modes in coding-agent procurement — specifics

1. **Evaluating on Job B, deploying for Job C.** Procurement team runs a month of Cursor in the IDE, everyone loves it, then buys Devin seats for async delegation. Completely different job, zero signal transfer.

2. **Trusting self-reported productivity numbers.** "Our team says they're 40% faster" is a belief, not a measurement. Run a two-sprint A/B on real tickets before signing enterprise contracts.

3. **Ignoring the model-layer concentration risk.** Cursor, Copilot, and most agent wrappers route through OpenAI or Anthropic. If one of those providers changes pricing, rate limits, or terms — or if the end customer has a policy against sending their code to a third-party model provider — the whole stack breaks. Enterprise procurement increasingly demands VPC or on-prem options, which only a subset of vendors offer.

4. **Buying on SWE-bench, measuring on production.** Discount the number. Measure in-codebase.

5. **Underestimating the review cost.** AI-generated PRs shift labour from writing to reviewing. A 20-developer team that triples PR volume without scaling review discipline creates a quality crisis in quarter two that is read as "the agent doesn't work" — when in fact the agent worked and the review process didn't.

6. **Buying Devin-style async for a team without ticket-scoping discipline.** If your engineering org doesn't write tickets well, the async agent will fail on ambiguous input and the seat cost will be wasted. The answer is sometimes "fix ticket-writing first, then evaluate async agents."

7. **Ignoring the Klarna-style reversal risk.** This week's Friday lesson walked through Klarna's retreat from AI customer support after backlash.[^15] The analogous risk in coding is real: a loud failure — a subtle bug merged to main that costs $50K to clean up, a leaked secret from a Claude Code session, a regulatory breach — can trigger a months-long rollback of AI-coding adoption even if the aggregate numbers were positive. Plan for the tail.

## Open questions — what is not settled as of April 2026

1. **Does the METR slowdown shrink with model generation?** Claude Sonnet 4.5 and Opus 4.5 are meaningfully stronger than the Claude 3.5/3.7 Sonnet models in METR's 2025 study. A 2026 replication may land on neutral or mildly positive throughput. Nobody has published that number yet.

2. **Will pricing stay inference-cost-plus, or move to value-based?** Current race-to-the-bottom on price reflects the fact that no vendor can reliably prove $300-of-value-per-ticket delivery. If one vendor solves verification (agent auto-grades its own PR with high calibration vs. human review), the market can re-price.

3. **Is there an enterprise-native winner, or does Copilot run the table on Job D?** Microsoft's distribution advantage in Job D is structural. Cursor and Anthropic are building enterprise tiers aggressively. The question is whether a CISO who has already approved GitHub will pay to approve a second vendor, and the answer depends on how much Job B outperformance the second vendor can demonstrate on audited benchmarks.

4. **Does the autonomous-agent model (Devin, Claude Code headless) find its second act?** Devin 2.0's pricing reset from $500 to $20 was a correction. Where the category settles — premium per-task-value pricing, commodity usage pricing, or absorption into IDE-native async modes from Cursor and Copilot — is the live open question for 2026–2027.

## Further reading

**Must-read this week (four items):**

- Anthropic. *Introducing Claude Sonnet 4.5* and *Introducing Claude Opus 4.5* — the SWE-bench Verified numbers in their primary-source form.[^1][^2]
- METR (2025). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity* — the headline "19% slowdown" RCT, plus methodology.[^11]
- Hamel Husain. *A Field Guide to Rapidly Improving AI Products* (2025). One article, re-read it every quarter.[^13]
- Lenny Rachitsky × Boris Cherny. *Head of Claude Code: What happens after coding is solved* — operator-level framing from the inside of Anthropic.[^10]

**Recommended:**

- Scale AI. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* — the successor benchmark and the contamination critique in primary form.[^12]
- The SWE-Bench Illusion paper (arXiv 2506.12286) — the memorization-vs-reasoning argument.[^14]
- Cognition. *SWE-bench technical report* — Cognition's own methodology post, useful to read alongside the Answer.AI / Internet of Bugs critiques.[^16]
- TechCrunch (2025-06-05). *Cursor's Anysphere nabs $9.9B valuation, soars past $500M ARR.*[^4]

**Optional:**

- Klarna / CX Dive coverage of the 2025 human-agent reversal — useful analogy for coding-agent tail-risk planning.[^15]

## Citations

[^1]: Anthropic (2025-09-29). *Introducing Claude Sonnet 4.5.* https://www.anthropic.com/news/claude-sonnet-4-5 — primary source for SWE-bench Verified scores cited through 2025–2026.
[^2]: Anthropic (2025-11-24). *Introducing Claude Opus 4.5.* https://www.anthropic.com/news/claude-opus-4-5 — first model reported above 80% on SWE-bench Verified.
[^3]: Cursor (2025–2026). *Pricing* and *Models & Pricing.* https://cursor.com/pricing and https://cursor.com/docs/models-and-pricing — Pro $20, Business $40/user, Ultra $200; June 2025 migration from request caps to usage credit pool. Secondary context: Vantage pricing breakdown https://www.vantage.sh/blog/cursor-pricing-explained (accessed 2026-04-15).
[^4]: Mascarenhas, N. (2025-06-05). *Cursor's Anysphere nabs $9.9B valuation, soars past $500M ARR.* TechCrunch. https://techcrunch.com/2025/06/05/cursors-anysphere-nabs-9-9b-valuation-soars-past-500m-arr/ — ARR and valuation milestones. Series D and $29.3B valuation: CNBC (2025-11-13). https://www.cnbc.com/2025/11/13/cursor-ai-startup-funding-round-valuation.html
[^5]: Anthropic. *Claude API pricing* and *Claude Code — Manage costs effectively.* https://platform.claude.com/docs/en/about-claude/pricing and https://code.claude.com/docs/en/costs — Sonnet $3/$15, Opus $15/$75 per million tokens; enterprise averages $13/active-dev/day, $150–$250/active-dev/month.
[^6]: The Meridiem (2026-01-22). *Claude Code hits inflection point as Anthropic shifts to product-led revenue.* https://www.themeridiem.com/ai-machine-learning/2026/1/22/claude-code-hits-inflection-point-as-anthropic-shifts-to-product-led-revenue — ~$1B ARR by November 2025, ~$2.5B by February 2026. Primary cross-reference: Bloomberg (2026-03-03). *Anthropic Nears $20 Billion Revenue Run Rate Amid Pentagon Feud.* https://www.bloomberg.com/news/articles/2026-03-03/anthropic-nears-20-billion-revenue-run-rate-amid-pentagon-feud ; PYMNTS (2026). *Enterprises Drive Anthropic Run-Rate Revenue to $19 Billion.* https://www.pymnts.com/artificial-intelligence-2/2026/enterprises-drive-anthropic-run-rate-revenue-to-19-billion/
[^7]: GitHub (2025). *Copilot pricing.* https://github.com/features/copilot — Free / Pro $10 / Pro+ ~$19 / Enterprise $39.
[^8]: Microsoft FY26 Q2 earnings (Jan 28 2026) — 15M paid Microsoft 365 Copilot seats (160% YoY), 4.7M GitHub Copilot subscribers (75% YoY). Primary: https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2 ; see Directions on Microsoft's summary: https://www.directionsonmicrosoft.com/microsoft-claims-15-million-paid-m365-copilot-seats/ ; mid-2025 20M all-time GitHub Copilot user context: https://techcrunch.com/2025/07/30/github-copilot-crosses-20-million-all-time-users/
[^9]: Cognition (2025). *Devin pricing.* https://devin.ai/pricing/ — Core from $20/mo, $2.25/ACU pay-as-you-go; Team $500/mo / 250 ACUs (pre-2.0 and retained variants); Enterprise custom. Context: VentureBeat (2025-04-03). *Devin 2.0 is here: Cognition slashes price of AI software engineer to $20 per month from $500.* https://venturebeat.com/programming-development/devin-2-0-is-here-cognition-slashes-price-of-ai-software-engineer-to-20-per-month-from-500 and TechCrunch (2025-04-03). https://techcrunch.com/2025/04/03/devin-the-viral-coding-ai-agent-gets-a-new-pay-as-you-go-plan/
[^10]: Lenny's Newsletter with Boris Cherny (2025–2026). *Head of Claude Code: What happens after coding is solved.* https://www.lennysnewsletter.com/p/head-of-claude-code — Cherny's public statements on Claude Code's scope, usage, and his own daily workflow.
[^11]: METR (2025-07-10). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — RCT of 16 experienced OSS developers, 246 tasks, predicted 24% speedup, measured 19% slowdown. arXiv: https://arxiv.org/abs/2507.09089. Follow-up design update: https://metr.org/blog/2026-02-24-uplift-update/
[^12]: Scale AI. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* https://static.scale.com/uploads/654197dc94d34f66c0f5184e/SWEAP_Eval_Scale%20(9).pdf and leaderboard at https://labs.scale.com/leaderboard/swe_bench_pro_public — 27-point gap vs. SWE-bench Verified on comparable models; contamination and production-gap argument. Context on OpenAI shift: CodeSOTA coverage https://www.codesota.com/news/swe-bench-contamination-debate
[^13]: Husain, H. (2025-03-24). *A Field Guide to Rapidly Improving AI Products.* https://hamel.dev/blog/posts/field-guide/ — measurement-first framing, binary LLM-as-judge, human-agreement calibration, systematic error analysis. Companion: *Your AI Product Needs Evals.* https://hamel.dev/blog/posts/evals/
[^14]: *The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason* (2025). arXiv 2506.12286. https://arxiv.org/html/2506.12286v3 — memorization vs reasoning on SWE-bench; up to 76% file-path accuracy by memorization alone.
[^15]: Klarna reversal coverage (2025). CX Dive: https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/ and Entrepreneur: https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396 — used as the tail-risk analogy for a loud AI-adoption reversal.
[^16]: Cognition (2024). *SWE-bench technical report.* https://cognition.ai/blog/swe-bench-technical-report — Cognition's own methodology write-up. Critique coverage: 80.lv summary https://80.lv/articles/first-ai-software-engineer-creators-are-accused-of-lying

---

*Self-check against the L3 spec: engages ≥1 live controversy (the METR vs. adoption-numbers debate, named with both positions); ≥3 post-2024 citations (METR 2025, Sonnet/Opus 4.5 2025, Cursor ARR 2025, Devin 2.0 2025, SWE-bench Pro 2025, Claude Code inflection 2026, SWE-bench Illusion 2025 — seven primary post-2024 sources); runnable experiment that demonstrates mechanism (SWE-bench-style loop felt on one real issue via Claude Code); operator numbers with sources (all pricing and ARR numbers cited); reviewer lens naming three specific pushbacks with named roles (skeptical CTO on contamination; Hamel Husain on measurement; Cognition founder rebuttal); domain variety (enterprise procurement, indie builder, async delegation, incumbent distribution); no "live session" framing, no fabricated URLs, experiment framed as illustrative.*
