---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: sat
day_name: sat
session_slug: decoding-real-business-problems-with-ai-ii
title: 'Case study teardown — coding agents as a business (Cursor, Claude Code, Devin, Copilot, Codex) under the four-step pipeline'
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
last_verified: 2026-07-17
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

- Monday–Friday of this week — [[01-mon-problem-discovery-frameworks|discovery]], [[02-tue-when-ai-fits-a-problem|fit]], [[03-wed-scoping-ai-projects|scoping]], [[04-thu-pricing-ai-services|pricing]], and Friday's [[05-fri-case-study-customer-support-agent|support-agent teardown]]. The four-step pipeline names below refer to the rubrics you built earlier in the week. Fine to read standalone, but the vocabulary assumes you've seen them.
- Claude Code and a Claude.ai account. One exercise has you direct Claude Code to read a SWE-bench-style issue and reason about it; another is a manual pricing comparison run in Claude.ai.
- No coding. Every exercise is directed-through-AI or analytical.

## Framing — what a "coding agent" actually is in 2026, under the hood

Strip the marketing. A coding agent, circa mid-2026, is a loop of four elements:

1. A frontier model (Claude Sonnet 5 / Opus 4.8 / the Mythos-class Fable 5, GPT-5.6 Sol/Terra/Luna, Gemini 3.5 Flash) doing the actual reasoning and token generation.
2. A scaffolding layer that shapes that model's behaviour — file reads, shell execution, edit application, retry logic, sub-agent dispatch, planning prompts.
3. A surface — an IDE integration (Cursor, Copilot), a terminal tool (Claude Code, Codex CLI), or a hosted async worker (Devin, Devin Desktop).
4. A monetization wrapper — subscription, seat pricing, usage metering, enterprise contract.

Every tool in this category is a different bet about which of those four layers captures the most value. Cursor bet on #3 — own the IDE (and, as of June 2026, is owned by SpaceX, which owns model and compute via xAI). Claude Code bet on #1+#2 — own the model and the scaffolding in terminal form. Copilot bet on #3+#4 — own the distribution inside GitHub and the enterprise procurement motion. Devin bet on a stronger version of #2+#3 — make the agent asynchronous, parallelizable, and remote, so a developer can delegate rather than pair. OpenAI Codex bet on #1+#3+#4 — its own frontier model, a surface inside ChatGPT desktop, and a distribution wedge that by mid-2026 reached beyond developers entirely. Those bets predict how each company prices, what its margin profile looks like, and where its moat either exists or doesn't. Hold that framing while we walk the pipeline.

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

**Job C (delegated tickets).** Contested fit. This is where all the interesting arguments live. The cost of a wrong autonomous PR is a broken build, a subtle bug merged to main, a two-day junior-engineer clean-up, or worse — a security issue, a deleted table, a shipped hallucination. By mid-2026 the reported number has migrated from **SWE-bench Verified** (which topped out above 80% and became contaminated — see the CTO pushback below) to **SWE-bench Pro**, where the best models sit materially lower: roughly high-50s to low-70s depending on which split you read (Scale's standardized public set puts frontier models around 59%, vendor-aggregate leaderboards put Opus 4.8 near 69%).[^12] Even taking the optimistic number, a ~30% failure rate on delegated tickets means roughly one in three PRs is wrong — a load that breaks code review if volume is high, and an error-mode the current scaffolding doesn't self-detect reliably. Fit verdict depends entirely on how well the organisation can catch the wrong slice before merge. Most can't.

**Job D (enterprise governance).** Fit is not about AI capability at all — it is about procurement, security, and integration. The question "is AI the right tool" has already been answered (yes, we're buying something); the question is *which vendor's enterprise product actually solves the CISO's problems.* The pipeline here is not discovery → fit → scoping → pricing in the original sense; it is compliance → integration → seat-governance → renewal.

Cross-job implication: a single vendor evaluation that tries to cover all four jobs simultaneously produces a rubric that can't distinguish between them. The first scoping move is almost always *"pick the one job we're going to actually measure."*

## Step 3 — Scoping: what does each vendor's current product actually do, with real numbers?

This is where the citations matter. Dates and URLs are in footnotes; I'll keep numbers in the prose.

**Cursor (Anysphere → SpaceX).** IDE fork of VS Code. Pro is $20/mo with unlimited Tab completions and $20 worth of premium-model credits; Business is $40/user/mo adding SSO, team controls, SOC 2; Ultra is $200/mo with ~20x the Pro credit pool.[^3] The June 2025 shift from request caps to model-API-priced credits is load-bearing — it means Cursor's gross margin on paid plans is capped by how much of the $20 their users burn in Claude / GPT API fees. ARR crossed $500M in June 2025, passed $1B by the November 2025 Series D, and reached **roughly $4B annualized (~$2.6B of it enterprise) by June 2026** — at which point **SpaceX exercised an option and agreed to acquire Anysphere for $60B in all-stock, the largest venture-backed-startup acquisition ever** (announced June 16, 2026, expected to close Q3 2026).[^4] This detonates the old "independent IDE startup" framing and inverts the concentration-risk story below: the flagship IDE is now owned by a conglomerate that also owns a frontier lab (xAI/Grok) and hyperscale compute (Colossus), and Cursor's coding data reportedly feeds Grok's training pipeline. The procurement question changes from "whose model does this route to?" to "whose model, whose data pipeline, whose parent." Net dollar retention has been reported above 170%. Cursor wins Jobs A and B; background-agent and multi-edit features push into Job C; enterprise (Job D) is newer and lighter than Copilot's, though the SpaceX balance sheet changes the calculus.

**Claude Code (Anthropic).** Terminal tool. Pricing rides on Claude subscriptions: Pro at $20/mo (insufficient for heavy use), Max 5x at $100/mo, Max 20x at $200/mo; or pay-as-you-go API at **Sonnet 5 $2/$10 intro (then $3/$15) and Opus 4.8 $5/$25 per million tokens** — note $15/$75 is *deprecated Opus 4.1* pricing, not current Opus, and the newer tokenizer emits ~30% more tokens for the same text.[^5] The real unit economics: across enterprise Claude Code deployments, Anthropic's cost guidance has indicated roughly $13 per active developer per active day, $150–$250 per active developer per month average, with 90% of users under $30/day.[^5] A widely-quoted developer anecdote — ~10 billion tokens over eight months that would have cost ~$15,000 on API but ran $1,600 flat on Max 20x — is now *historical*: through 2026 Anthropic doubled 5-hour limits (May 6) but enforces weekly active-compute-hour caps, and in June 2026 announced then **paused** (June 15) a plan to meter programmatic Agent-SDK usage at API rates.[^5] The uncapped flat subsidy that anecdote celebrated is being squeezed. Claude Code's default is now **Sonnet 5 with a 1M-token context**; it hit ~$1B annualized run-rate by November 2025 and ~$2.5B by February 2026.[^6] Claude Code wins Job B for AI-native operators and pushes hard into Job C through headless / non-interactive mode; Job A is not its game (no IDE); Job D is shipping but less mature than Copilot Enterprise.

**OpenAI Codex.** The entrant this teardown originally omitted, and by mid-2026 it cannot be. Codex surpassed **5 million weekly active users by June 2026** (up ~6x since the desktop app launched in February), with **roughly one in five users not a developer** — role-specific plugins target equity research, banking, sales, and design.[^codex] GPT-5.6 runs in Codex for Plus+ plans, and Codex lives inside the ChatGPT desktop app. OpenAI was named a **Leader in the 2026 Gartner Magic Quadrant for Enterprise AI Coding Agents** — a Gartner MQ *existing* for this category is itself a Job-D procurement data point. Codex is a Job-A/B/C play with OpenAI's distribution behind it; a four-vendor teardown that ignores it is a 2025 teardown. Related: GitHub **Agent HQ** repositions Copilot as a control plane for third-party agents (Anthropic, OpenAI, Google, Cognition, xAI running inside one surface), which complicates every vendor's "own the surface" story.

**GitHub Copilot (Microsoft).** The incumbent — and, as of **June 1, 2026, no longer flat-priced**. GitHub moved *all* Copilot plans to **usage-based billing**: premium-request units were replaced by **GitHub AI Credits** (1 credit = $0.01) metered on token consumption at per-model API rates, with only code completions and Next Edit Suggestions staying unlimited; each plan bundles a monthly credit allotment (Business $19 seat includes $19 in credits, Enterprise $39 includes $39) and meters above it.[^7] The old "$19 seat + 300 premium requests + $0.04 overage" mechanics are dead — do not quote them. Reported ~4.7M paid Copilot subscribers by January 2026 (up 75% YoY), ~20M all-time users; estimated ARR roughly $1B.[^8] Wins Job A by distribution and incumbency; Job D by integration into GitHub's existing enterprise procurement surface (the CISO has already approved GitHub), now extended by **Agent HQ** as a multi-agent control plane. Job B is contested — power users trade down to Cursor or Claude Code for depth. Job C is shipping later than Devin or Claude Code's async modes.

**Cognition Devin.** Asynchronous agent. Originally $500/mo for 250 ACUs (an ACU is roughly 15 minutes of Devin active work); in April 2025 relaunched as Devin 2.0 starting at $20/mo with pay-as-you-go at $2.25/ACU; enterprise custom-priced with VPC deployment.[^9] The framing of Devin as the under-adopted premium experiment that had to reprice is now badly out of date. Cognition **acquired Windsurf (IP, product, brand, most of the team) in July 2025**, raised a **$1B+ Series D at a $26B post-money valuation in May 2026** with ARR at **~$492M (up 13x from $37M a year earlier)**, and on **June 2, 2026 rebranded Windsurf as "Devin Desktop"** — an Agent Command Center that opens on a Kanban of running agents rather than an editor, shipping the open Agent Client Protocol (ACP).[^9][^cognition] Cognition also claims ~89% of its own committed code is now written by Devin. So Devin is a top-three player with both an async worker *and* an IDE surface, not a niche experiment. Devin still pitches Job C hardest — *"delegate the ticket and walk away"* — and the procurement question (Job D) remains the hard one: enterprise customers ask about liability for autonomous merges, audit trails on what Devin decided and why, and how to roll back a 50-PR burst that contained one data-loss bug.

**Unit economics sanity check.** Model inference is the largest variable cost for any of these. A realistic Job-B session — a developer chatting with a coding agent for a few hours — consumes on the order of a few million tokens of Sonnet-class inference once you account for file reads, conversation history, and tool-call loops (and ~30% more under the new tokenizer). At API price that's a few dollars. A Claude Code Max 20x subscriber at $200/mo who runs heavy costs Anthropic many multiples of what they pay — but Anthropic serves the inference itself, so the "loss" is compute-time on models Anthropic owns (and the new weekly caps are how Anthropic bounds it). Cursor at Pro $20/mo serving a user who burns their entire credit pool on Claude or GPT operates at essentially zero marginal gross profit on that user before fixed costs; Cursor's margin depends on under-consuming users plus Business/Ultra seats (and now on SpaceX/xAI potentially serving inference in-house). GitHub's June 2026 move to metered AI Credits directly addresses the flat-price margin bleed — heavy users now pay for their consumption instead of being cross-subsidized.

Scoping conclusion: **each vendor's price is tuned to its structural advantage.** Anthropic can price Claude Code against a model it owns. OpenAI can do the same with Codex. GitHub converted its distribution advantage into a metered floor once flat pricing bled margin. Cursor, having owned neither model nor distribution, priced up (Business/Ultra) — and then was acquired by a parent that owns both. Devin prices for the most valuable job if it works. Reading the pricing sheet still tells you the strategic position; in 2026 it also tells you who got acquired.

## Step 4 — Pricing: value-based, seat-based, or usage-based, and why it matters which

Thursday's frame: pricing choice encodes what the vendor believes they are selling. Three patterns across the four vendors.

**Seat + usage credit (Cursor Pro, Claude Code Max).** The seat says "this user has access"; the credit pool says "this much inference is included." Good for buyers whose AI usage is bursty and hard to predict per-person; good for vendors because average usage stays below the cap and the cap is a psychological commitment, not a literal ceiling. Failure mode: heavy users feel squeezed (see the June 2025 Cursor rollout backlash — the migration from request caps to credit pools was widely read as a de-facto price hike and caused retention complaints), light users pay for unused capacity.[^3]

**Pure usage / ACU (Devin 2.0, Claude Code API pay-as-you-go).** The buyer pays for exactly what the agent does. Good for finance teams that need to attribute cost to projects; good for vendors because it removes the unit-economic risk of heavy users. Failure mode: buyers cannot predict monthly spend, which blocks enterprise approval — Devin's original $500 ceiling was in part an attempt to give procurement a budgeting number.

**Seat + enterprise (Claude Code Enterprise, Cursor Business — and, until June 2026, Copilot Enterprise).** Flat per-seat pricing with usage fair-use, plus security and compliance features. Good for large organisations that want predictable per-developer cost and centralized control. This *was* Job D's natural pricing shape — but the failure mode named here (heavy users cross-subsidized by light users; economics break if the ratio inverts) is exactly what drove GitHub to convert Copilot to metered AI Credits on June 1, 2026. When the flat-seat shape's own failure mode bites hard enough, vendors reach for metering. Watch for the remaining flat-seat enterprise tiers to follow.

**The value-based pricing question nobody has solved well yet.** If a coding agent genuinely closes one Job-C ticket autonomously — a ticket that would have taken a mid-level engineer three hours — the value created is closer to $300 than to $9 (the cost of 4 ACUs on Devin). Why is no one capturing that value? Two reasons. First, verification: the agent can't prove it delivered the $300 of value because the PR still requires human review and sometimes the PR is wrong. Second, substitution risk: if one vendor prices at $300/ticket, a competitor at $50/ticket captures the market. The coding-agent category is in a classic race-to-the-bottom phase where capture-price is pinned to inference-cost-plus rather than value-created. Expect this to change — or to be forced to change — over the next 18 months.

## The live controversy — does AI actually make senior developers faster?

This is the single most contested empirical question in the coding-agent market right now. Know both sides.

**Position 1 — the optimistic / adoption-driven case.** Cursor, Claude Code, and Copilot publish self-reported productivity numbers from their user bases that consistently claim 25–55% acceleration on tasks. Cursor's retention and expansion numbers are consistent with users who believe they are faster with the tool. Boris Cherny, head of Claude Code at Anthropic, has said publicly that he writes 100% of his daily code through the tool — an extraordinary claim if true and not unusual among AI-native operators.[^10] The ambient vibe-coding discourse (Karpathy's original February 2025 tweet onward) assumes meaningful acceleration at least for exploratory and throwaway work.

**Position 2 — the measured / randomized-trial case.** In July 2025, METR published a randomized controlled trial: sixteen experienced open-source developers, each with roughly five years of prior experience on the repositories they were working in, completed 246 real tasks. Each task was randomly assigned either "AI allowed" (primarily Cursor Pro with Claude 3.5/3.7 Sonnet) or "AI disallowed." **Before the study, the developers forecast a 24% speedup from AI. After completing the study, they estimated AI had given them a 20% speedup. The measured reality was a 19% slowdown.** Developers took *longer* to complete tasks with AI tools than without. ML researchers and economists surveyed before the study predicted 38–39% speedups. Everyone was wrong in the same direction.[^11]

The METR finding is not a one-off. It is the best-designed trial we currently have on the question, and its result directly contradicts the self-reported productivity numbers.

**And the follow-up has now happened — with a stranger result than either camp expected.** METR's **February 24, 2026 update** reports that its attempted 2026 replication produced an *unreliable* signal, for a reason that is itself the punchline: **30–50% of developers declined to submit some tasks rather than do them without AI**, a selection effect that systematically removes the high-AI-uplift tasks from the control condition. In plain terms, the RCT methodology partially broke because *the control group increasingly refuses to exist* — developers won't work without AI anymore. METR's careful read is that it is "likely that developers are more sped up from AI tools now" in early 2026 than in early 2025, and its latest RCT of open-source developers on late-2025 agents found **small (~4–20%) productivity benefits** — but METR flags even that as weak evidence likely underestimating the true effect due to the selection problem, and is reworking the design (questionnaires, fixed-task experiments, developer-level randomization).[^11] So the honest 2026 statement is *not* "nobody has published a follow-up number" — someone has, it's METR itself, and the number moved from −19% toward a small positive while the methodology that produced the −19% started to buckle.

**Two positions, how to hold them.** The honest reading is that both positions are describing something real. The developers in METR's study *felt* faster even when they were slower — the subjective acceleration is real, the objective deliverable-throughput is not (on those tasks, with those tools at that time). The adoption and expansion numbers at Cursor and Claude Code are real too — people are willingly paying for something — but "willingness to pay" and "measurable throughput gain" are different variables. This is the same gap that shows up in every productivity-tool category (IDEs, code review tools, meeting software) where subjective felt-productivity leads measurable throughput by years or decades.

**Operator takeaway.** If you're briefing a client or a CTO on whether to deploy a coding agent, the honest answer in 2026 is: *expect real subjective improvement, expect measurable throughput improvement on well-scoped novel work where the agent isn't competing against existing context in the developer's head, and expect null-or-negative effects on tasks in mature codebases the developer already knows deeply.* The second category — new work — is most of the upside. The third category — old code the senior knows cold — is where the METR slowdown lives.

The follow-up empirical question — whether the gap closes as (a) models get better, (b) scaffolding gets better, and (c) developers get better at using the tools — now has partial 2026 evidence pointing toward "yes, somewhat," but wrapped in a measurement crisis: you can no longer cleanly run the control condition because senior developers refuse to code without AI. That refusal is itself the strongest real-world signal in the whole debate.

## Reviewer lens — named pushbacks from three specific positions

**Pushback 1. A skeptical enterprise CTO on SWE-bench.** The migration from Verified to Pro (referenced in the Job C fit discussion above) is exactly the CTO's point: the benchmark-to-production leap has three structural problems. First, **contamination**: any model trained on GitHub data after June 2024 has likely seen some subset of the 500 Verified problems including their solutions, and empirical work in 2025 showed direct solution-leakage in a large share of successful passes. SWE-bench Pro (Scale AI's response) has standardized-set scores running well below Verified on the same tier of models; that gap is the contamination and the harder task distribution.[^12] Second, **environment**: Verified tasks are single-repo Python issues with high-quality test coverage. A typical enterprise codebase is multi-language, multi-repo, has flaky tests or no tests, has undocumented business logic, and half the time you can't reproduce the bug locally. Third, **scoring**: "resolved" means the tests pass. In production, "resolved" means the tests pass *and* a senior reviewer believes the fix is correct *and* it doesn't break adjacent systems *and* it matches architectural constraints no one wrote down. Any headline benchmark number is a floor on production performance, not a ceiling. OpenAI has publicly de-emphasized Verified and shifted toward SWE-bench Pro partly for these reasons.[^12] The CTO's operational consequence: **discount any headline SWE-bench score by something like 20–30 points when predicting in-codebase performance, and budget for human review as if the agent's accuracy is 50–60%.**

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

**Problem 2 — Unit-economics reality check.** For a team of 20 developers, compute the monthly cost at: (a) Cursor Pro for all, (b) Cursor Business for all, (c) Claude Code Max 5x for all, (d) Copilot Enterprise for all, (e) Devin 2.0 Core for all, (f) a mixed stack of Copilot Enterprise for the full org + Claude Code Max 20x for the five heaviest users. Note the 2026 subtlety that is itself the lesson: **Copilot Enterprise is no longer a flat seat** — since June 1 2026 the $39 seat includes $39 of AI Credits and then meters token usage, so "seat cost" for (d) and (f) is a floor, not the bill. Estimate the metered overage for a heavy team, and notice how that changes the mixed-stack math versus the old flat-seat assumption. To identify the "heaviest 5" in practice: pull 30 days of per-seat token/request usage from the vendor admin dashboard (Anthropic Console usage tab, Cursor Business admin, or Copilot Enterprise admin analytics), sort by total tokens or active-day count, take the top 5; cross-check against Git commit or PR-volume logs to confirm usage correlates with output and isn't one power-user burning credits on a side project. Then ask: which is cheapest, and is cheapest the right frame? What breaks in option (f) that doesn't break in options (a)–(e)? (Hint: governance, integration, audit trail — the Job-D concerns from discovery.)

**Problem 3 — Take a position on METR.** Read *both* the METR July 2025 study *and* its February 24 2026 update (URLs in citations) — the update is now the more interesting document, because the 2026 replication partly broke when 30–50% of developers refused to work without AI. In 200 words, take a position on one of these: (i) the 19% slowdown generalizes and most AI-coding productivity claims are folk knowledge; (ii) the slowdown is specific to deep-context mature-codebase work and will not appear on greenfield or unfamiliar-codebase work; (iii) the slowdown was a transitional 2025 phenomenon and the 2026 evidence (small positive, weakened by selection effects) shows it shrinking. Your position must name one follow-up experiment that would falsify it — and must engage the control-group-refusal problem, which is the real methodological story of 2026.

**Problem 4 — Price a Job-C engagement.** You are advising a founder who wants to deploy an async coding agent (Devin or Claude Code headless) to close well-scoped bugs out of hours. The founder wants "$20,000/month of virtual-engineer throughput." Using public pricing, estimate: how many hours of agent work that buys, how many tickets that is at the current realistic pass rate, and what the implied cost per completed ticket is. Then argue for a pricing structure to sell this to the founder's customers. Seat-based? Per-ticket? Retainer?

**Problem 5 — Write the reviewer-lens email.** A client has just sent you a deck claiming their team is 40% more productive on Copilot based on self-reported survey data. Draft a one-screen reply that (a) doesn't insult the data, (b) names the METR contrast explicitly, (c) proposes a two-week pilot design that would produce a number you'd both trust. This is the measurement discipline from Pushback 2, made practical.

## Common failure modes in coding-agent procurement — specifics

1. **Evaluating on Job B, deploying for Job C.** Procurement team runs a month of Cursor in the IDE, everyone loves it, then buys Devin seats for async delegation. Completely different job, zero signal transfer.

2. **Trusting self-reported productivity numbers.** "Our team says they're 40% faster" is a belief, not a measurement. Run a two-sprint A/B on real tickets before signing enterprise contracts.

3. **Ignoring the model-layer concentration risk — now with an ownership twist.** Copilot and most agent wrappers route through OpenAI or Anthropic; if a provider changes pricing, rate limits, or terms — or the customer bans sending code to a third-party model — the stack breaks. The 2026 twist: after the SpaceX acquisition, **Cursor is owned by a conglomerate that also owns a frontier lab (xAI/Grok) and hyperscale compute**, and its coding data reportedly feeds Grok training. The old worry ("my IDE depends on someone else's model") inverts into a new one for some buyers ("my IDE's parent is a model competitor, and my code may train it"). Enterprise procurement increasingly demands VPC or on-prem options and explicit data-use terms, which only a subset of vendors offer.

4. **Buying on SWE-bench, measuring on production.** Discount the number. Measure in-codebase.

5. **Underestimating the review cost.** AI-generated PRs shift labour from writing to reviewing. A 20-developer team that triples PR volume without scaling review discipline creates a quality crisis in quarter two that is read as "the agent doesn't work" — when in fact the agent worked and the review process didn't.

6. **Buying Devin-style async for a team without ticket-scoping discipline.** If your engineering org doesn't write tickets well, the async agent will fail on ambiguous input and the seat cost will be wasted. The answer is sometimes "fix ticket-writing first, then evaluate async agents."

7. **Ignoring the Klarna-style reversal risk.** This week's [[05-fri-case-study-customer-support-agent|Friday lesson]] walked through Klarna's retreat from AI customer support after backlash.[^15] The analogous risk in coding is real: a loud failure — a subtle bug merged to main that costs $50K to clean up, a leaked secret from a Claude Code session, a regulatory breach — can trigger a months-long rollback of AI-coding adoption even if the aggregate numbers were positive. Plan for the tail.

## Open questions — what is not settled as of July 2026

1. **Does the METR slowdown shrink with model generation? — partly answered.** Sonnet 5, Opus 4.8, and the Mythos-class Fable 5 are meaningfully stronger than the Claude 3.5/3.7 models in METR's 2025 study. METR's Feb 2026 update did land on a small positive (~4–20%) on late-2025 agents — but with a broken control condition (30–50% of devs refusing to work without AI) that makes the point estimate weak evidence. The open part is now "how large, once you correct for the selection effect," not "has anyone looked."[^11]

2. **Will pricing stay inference-cost-plus, or move to value-based?** Current race-to-the-bottom on price reflects the fact that no vendor can reliably prove $300-of-value-per-ticket delivery. If one vendor solves verification (agent auto-grades its own PR with high calibration vs. human review), the market can re-price.

3. **Is there an enterprise-native winner, or does Copilot run the table on Job D?** Microsoft's distribution advantage in Job D is structural. Cursor and Anthropic are building enterprise tiers aggressively. The question is whether a CISO who has already approved GitHub will pay to approve a second vendor, and the answer depends on how much Job B outperformance the second vendor can demonstrate on audited benchmarks.

4. **Does the autonomous-agent model (Devin, Claude Code headless, Codex cloud) find its second act? — partly answered.** Devin 2.0's pricing reset from $500 to $20 was a correction, but Cognition's 2026 arc ($26B valuation, ~$492M ARR, Windsurf → Devin Desktop) shows the async-delegation bet is now a top-three business, not a failed experiment. Where the *pricing* settles — premium per-task-value, commodity usage, or absorption into IDE-native async modes and multi-agent control planes like GitHub Agent HQ — is the live open question for 2026–2027.

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
[^4]: ARR trajectory: TechCrunch (2025-06-05), *Cursor's Anysphere nabs $9.9B valuation, soars past $500M ARR* https://techcrunch.com/2025/06/05/cursors-anysphere-nabs-9-9b-valuation-soars-past-500m-arr/ ; ~$4B annualized (~$2.6B enterprise) by June 2026: Dealroom https://app.dealroom.co/news/note/cursor-tops-4b-annualized-revenue-june-2026. **SpaceX $60B all-stock acquisition (announced Jun 16 2026, option signed Apr 21 2026, expected close Q3 2026):** CNBC https://www.cnbc.com/2026/06/16/spacex-spcx-cursor-acquisition-ipo.html ; TechCrunch https://techcrunch.com/2026/06/16/spacex-to-acquire-cursor-for-60b-in-stock-days-after-blockbuster-ipo/. Verified 2026-07-17.
[^5]: Anthropic. *Claude API pricing* and *Claude Code — Manage costs effectively.* https://platform.claude.com/docs/en/about-claude/pricing and https://code.claude.com/docs/en/costs (fetched 2026-07-17): Sonnet 5 $2/$10 intro (then $3/$15), Opus 4.8 $5/$25 per million tokens; $15/$75 is *deprecated Opus 4.1*, not current Opus; Opus 4.7+/Sonnet 5/Fable 5 use a newer tokenizer (~30% more tokens for the same text). Enterprise averages ~$13/active-dev/day, $150–$250/active-dev/month. Weekly active-compute-hour caps + doubled 5-hour limits (May 6 2026): Anthropic, *Higher usage limits* https://www.anthropic.com/news/higher-limits-spacex. June 2026 Agent-SDK metering announced then paused (June 15): DevOps.com https://devops.com/anthropic-hits-pause-on-claude-agent-sdk-billing-change-for-now/. Verified 2026-07-17.
[^6]: The Meridiem (2026-01-22). *Claude Code hits inflection point as Anthropic shifts to product-led revenue.* https://www.themeridiem.com/ai-machine-learning/2026/1/22/claude-code-hits-inflection-point-as-anthropic-shifts-to-product-led-revenue — ~$1B ARR by November 2025, ~$2.5B by February 2026. Anthropic's overall run-rate trajectory has since re-anchored an order of magnitude higher: ~$19B (Mar 2026) → **~$47B run-rate disclosed May 2026** alongside the $65B Series H at a $965B valuation. Simon Willison, *Anthropic's run-rate revenue hits $47 billion* https://simonwillison.net/2026/May/29/anthropic/ ; VentureBeat, *Anthropic says it hit a $30 billion revenue run rate* https://venturebeat.com/technology/anthropic-says-it-hit-a-30-billion-revenue-run-rate-after-crazy-80x-growth. Verified 2026-07-17.
[^7]: GitHub Copilot moved all plans to **usage-based billing on June 1 2026** — premium-request units replaced by GitHub AI Credits (1 credit = $0.01) metered on token consumption at per-model API rates; code completions and Next Edit Suggestions stay unlimited; each plan bundles a monthly credit allotment (Business $19 seat = $19 credits; Enterprise $39 = $39). GitHub Blog, *GitHub Copilot is moving to usage-based billing* https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/ and changelog https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/. Agent HQ (multi-agent control plane) context: GitHub product materials, 2026. Verified 2026-07-17.
[^8]: Microsoft FY26 Q2 earnings (Jan 28 2026) — 15M paid Microsoft 365 Copilot seats (160% YoY), 4.7M GitHub Copilot subscribers (75% YoY). Primary: https://www.microsoft.com/en-us/investor/events/fy-2026/earnings-fy-2026-q2 ; see Directions on Microsoft's summary: https://www.directionsonmicrosoft.com/microsoft-claims-15-million-paid-m365-copilot-seats/ ; mid-2025 20M all-time GitHub Copilot user context: https://techcrunch.com/2025/07/30/github-copilot-crosses-20-million-all-time-users/
[^9]: Cognition (2025). *Devin pricing.* https://devin.ai/pricing/ — Core from $20/mo, $2.25/ACU pay-as-you-go; Team $500/mo / 250 ACUs; Enterprise custom. Context: VentureBeat (2025-04-03). *Devin 2.0 is here.* https://venturebeat.com/programming-development/devin-2-0-is-here-cognition-slashes-price-of-ai-software-engineer-to-20-per-month-from-500

[^cognition]: Cognition Series D and Windsurf/Devin Desktop: TechCrunch, *AI coding startup Cognition raises $1B at $25B pre-money valuation* (May 27 2026; $26B post-money, ARR ~$492M up 13x, ~89% of Cognition's own code by Devin) https://techcrunch.com/2026/05/27/ai-coding-startup-cognition-raises-1b-at-25b-pre-money-valuation/ ; Windsurf → Devin Desktop rebrand (Jun 2 2026, Agent Command Center, ACP): DigitalApplied https://www.digitalapplied.com/blog/windsurf-becomes-devin-desktop-ide-migration-2026 ; Windsurf acquired July 2025. Verified 2026-07-17.

[^codex]: OpenAI Codex 5M weekly users (~1 in 5 non-developers, June 2026): TechJack Solutions https://techjacksolutions.com/ai-brief/openai-codex-passes-5-million-weekly-users-and-1-in-5-arent/ ; Constellation Research https://www.constellationr.com/insights/news/openai-touts-broadening-codex-usage-5-million-weekly-active-users. 2026 Gartner Magic Quadrant for Enterprise AI Coding Agents (OpenAI a Leader alongside Anthropic Claude Code, GitHub Copilot, Cursor): OpenAI https://openai.com/index/gartner-2026-agentic-coding-leader/. Verified 2026-07-17.
[^10]: Lenny's Newsletter with Boris Cherny (2025–2026). *Head of Claude Code: What happens after coding is solved.* https://www.lennysnewsletter.com/p/head-of-claude-code — Cherny's public statements on Claude Code's scope, usage, and his own daily workflow.
[^11]: METR (2025-07-10). *Measuring the Impact of Early-2025 AI on Experienced Open-Source Developer Productivity.* https://metr.org/blog/2025-07-10-early-2025-ai-experienced-os-dev-study/ — RCT of 16 experienced OSS developers, 246 tasks, predicted 24% speedup, measured 19% slowdown. arXiv: https://arxiv.org/abs/2507.09089. **Follow-up: METR (2026-02-24). *We are Changing our Developer Productivity Experiment Design.* https://metr.org/blog/2026-02-24-uplift-update/** — the 2026 replication gave an unreliable signal because 30–50% of developers declined to submit tasks rather than work without AI (a selection effect removing high-uplift tasks); METR believes developers are likely more sped up now, and its latest RCT on late-2025 agents found small (~4–20%) benefits it calls weak evidence. Verified 2026-07-17.
[^12]: Scale AI. *SWE-Bench Pro: Can AI Agents Solve Long-Horizon Software Engineering Tasks?* leaderboard https://labs.scale.com/leaderboard/swe_bench_pro_public — frontier models on the standardized public set land around 59% (vs. 80%+ on Verified); the gap is contamination + harder task distribution. 2026 vendor-aggregate leaderboards report Opus 4.8 ~69% and Sonnet 5 higher on some splits — scores vary by methodology/split, so name the split when quoting: morphllm, *SWE-bench Pro Leaderboard 2026* https://www.morphllm.com/swe-bench-pro. Contamination argument: *The SWE-Bench Illusion* (arXiv 2506.12286). Verified 2026-07-17.
[^13]: Husain, H. (2025-03-24). *A Field Guide to Rapidly Improving AI Products.* https://hamel.dev/blog/posts/field-guide/ — measurement-first framing, binary LLM-as-judge, human-agreement calibration, systematic error analysis. Companion: *Your AI Product Needs Evals.* https://hamel.dev/blog/posts/evals/
[^14]: *The SWE-Bench Illusion: When State-of-the-Art LLMs Remember Instead of Reason* (2025). arXiv 2506.12286. https://arxiv.org/html/2506.12286v3 — memorization vs reasoning on SWE-bench; up to 76% file-path accuracy by memorization alone.
[^15]: Klarna reversal coverage (2025). CX Dive: https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/ and Entrepreneur: https://www.entrepreneur.com/business-news/klarna-ceo-reverses-course-by-hiring-more-humans-not-ai/491396 — used as the tail-risk analogy for a loud AI-adoption reversal.
[^16]: Cognition (2024). *SWE-bench technical report.* https://cognition.ai/blog/swe-bench-technical-report — Cognition's own methodology write-up. Critique coverage: 80.lv summary https://80.lv/articles/first-ai-software-engineer-creators-are-accused-of-lying

---

*Self-check against the L3 spec: engages ≥1 live controversy (the METR vs. adoption-numbers debate, now updated with METR's Feb 2026 control-group-refusal finding); post-2024 citations refreshed to July 2026 (SpaceX–Cursor $60B, Copilot usage-based flip Jun 2026, Cognition $26B / Devin Desktop, Codex 5M weekly users + Gartner MQ, Anthropic ~$47B run-rate, Opus 4.8/Sonnet 5 pricing, SWE-bench Pro); runnable experiment that demonstrates mechanism (SWE-bench-style loop felt on one real issue via Claude Code); operator numbers with sources (all pricing and ARR numbers cited and re-verified 2026-07-17); reviewer lens naming three specific pushbacks with named roles (skeptical CTO on contamination; Hamel Husain on measurement; Cognition founder rebuttal); domain variety (enterprise procurement, indie builder, async delegation, incumbent distribution); no "live session" framing, no fabricated URLs, experiment framed as illustrative.*
