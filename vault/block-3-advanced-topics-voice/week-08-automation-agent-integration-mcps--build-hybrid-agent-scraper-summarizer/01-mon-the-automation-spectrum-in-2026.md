---
type: lesson
block: block-3-advanced-topics-voice
week: week-08
day_of_cycle: 1
day_name: mon
session_slug: automation-agent-integration-mcps
date_due: 2026-07-06
tags: [automation, unattended-agents, n8n, make, zapier, claude-code, routines, scheduled-tasks, agent-sdk, dynamic-workflows, determinism, cost-modeling]
sources:
  - claude-code-scheduled-tasks-docs
  - claude-code-routines-docs
  - anthropic-building-effective-agents-2024-12
  - n8n-pricing-2026
  - n8n-sap-investment-2026-05
  - make-ai-agents-ga-2026-02
  - zapier-pricing-2026
  - anthropic-opus-4-8-dynamic-workflows-2026-05
  - anthropic-sonnet-5-2026-06
  - refresh-2026-07-landscape-delta
last_verified: 2026-07-17
word_count_target: 5200
---

# The automation spectrum in 2026 — workflow tools, code-first agents, and platform-native scheduling, and how to pick without religion

## Why this matters

This week you will ship an automation that runs without you: a scraper + summarizer that wakes up on a schedule, does real work against real websites and real APIs, and delivers output nobody proofreads. Before you write a line of it, you have to make the single highest-leverage decision in the whole project: **what runtime does it run on?**

Get this wrong and everything downstream gets harder. Build a five-step deterministic pipeline as a free-roaming agent and you will spend Friday's reliability lesson debugging behavior that a workflow engine would have made impossible. Build a judgment-heavy synthesis task as an n8n graph and you will drown in brittle branches trying to encode taste as if-statements. The failure statistics are not subtle: the most-cited enterprise number of 2026 is that **88% of agent pilots never reach production**, and Forrester's decomposition attributes 41% of those failures to unclear success criteria and 26% to drift in evaluation coverage — problems that runtime choice either contains or amplifies.[^9]

By tonight you will be able to place any automation on a three-lane spectrum — visual workflow tools, code-first agents, platform-native scheduling — price a year of operation in each lane with July-2026 numbers, and defend the choice to a skeptical CTO in two minutes.

## Prerequisites

- [[05-fri-n8n-for-agent-workflows]] — the Week 2 n8n lesson. This lesson does not re-teach nodes, triggers, or the n8n editor; it re-prices and re-positions the category as of mid-2026.
- [[02-tue-when-ai-fits-a-problem]] — the determinism test from Block 0 applies at the *step* level today, not the project level.
- [[05-fri-context-window-economics]] — token cost math; we build on it.

## Layer 1 — The spectrum, drawn honestly

Every unattended automation in 2026 runs in one of three lanes. Most production systems worth studying straddle two.

### Lane 1: Visual workflow platforms (n8n, Make, Zapier)

The category grew up. n8n 2.0 shipped in January 2026 with native AI Agent nodes, out-of-the-box MCP node support, and multi-agent orchestration on one canvas — an AI Agent can now supervise multiple AI Agent Tool nodes in a single execution.[^4] In May 2026, SAP made a strategic investment at a **$5.2B valuation** (double its October 2025 mark) and is embedding n8n natively into Joule Studio as the orchestration layer of its "Autonomous Enterprise" platform, with GA planned for Q3 2026; n8n reports 1,400+ enterprise customers and 1.7M monthly active builders.[^5] Whatever you thought of "low-code" in 2024, this is no longer a hobbyist category — it is what a large fraction of enterprise automation actually runs on.

Make's next-generation AI Agents went GA on February 11, 2026: agents built, run, and debugged on the same canvas as scenarios, with credit-based pricing.[^6] Zapier completed its pivot from "Zaps" to an AI-orchestration bundle — Agents, Copilot, Tables, Interfaces, and **Zapier MCP** — still metered by tasks.[^7]

What the lane is genuinely good at: triggers and connectors (thousands of prebuilt integrations), visual auditability (a non-engineer can read the flow), hosted scheduling and retry semantics you don't have to build, and — since 2.x — bounded LLM judgment *inside* an otherwise deterministic graph.

What it is bad at: version control and code review (n8n workflows serialize to JSON you *can* diff, but most teams don't), eval harnesses (there is no native golden-set regression concept; you bolt it on), complex data transformation (you end up writing JavaScript in Function nodes anyway, now without a debugger), and any logic whose natural expression is a program.

### Lane 2: Code-first agents (Claude Agent SDK, LangGraph, custom pipelines)

The Claude Agent SDK — the library underneath Claude Code — exposes the full agent loop (context management, tool execution, permissions, subagents) as a programmable runtime.[^10] Pair it with any scheduler (cron, GitHub Actions `schedule:` triggers, a `node-cron` process) and you have unattended agents with the exact autonomy envelope you programmed. LangGraph 1.0 and LlamaIndex Workflows 1.0 occupy the same lane with graph- and event-driven idioms.

What the lane is good at: everything is code — versioned, reviewed, testable, eval-able. Checkpointing, retries, idempotency, and cost budgets are yours to design (Thursday's lesson) rather than whatever the platform ships. This is the lane where Friday's reliability discipline is actually implementable in full.

What it is bad at: you own the infrastructure. Connector breadth is your problem (MCP narrows this gap dramatically — Tuesday). And the blank page is seductive: teams write bespoke orchestration frameworks nobody needed. Anthropic's own guidance from "Building Effective Agents" remains the canonical caution — find the simplest solution, use workflows for well-defined tasks, and add agentic autonomy only when the task genuinely requires model-directed control flow.[^3]

### Lane 3: Platform-native scheduling (Claude Code's three tiers)

This lane barely existed in April 2026 and is the reason this lesson had to be re-researched rather than remembered. Claude Code now ships **three distinct scheduling surfaces**, and the differences are exactly the differences that matter for unattended operation:[^1][^2]

| | `/loop` (in-session) | Desktop scheduled tasks | **Routines** (cloud) |
|---|---|---|---|
| Runs on | Your machine, open session | Your machine | Anthropic-managed cloud |
| Machine must be on | Yes | Yes | **No** |
| Minimum interval | 1 minute | 1 minute | 1 hour |
| Persistence | Restored on `--resume` if unexpired; recurring tasks self-expire after 7 days | Survives restarts | Fully persistent |
| Permissions | Inherits session | Configurable per task | **None — runs autonomously** |
| Local file access | Yes | Yes | No (fresh clone of selected repos) |

The in-session tier is a polling tool: `/loop 5m check the deploy`, backed by `CronCreate`/`CronList`/`CronDelete` tools taking standard 5-field cron expressions, with deliberate jitter (recurring tasks fire up to 30 minutes late, or half the interval for sub-hourly jobs) and a hard 7-day expiry that bounds how long a forgotten loop can burn tokens.[^1] Read that design twice: Anthropic shipped *jitter and self-expiry as defaults*. That is a vendor telling you what goes wrong with unattended agents — thundering herds and zombie jobs — before you find out yourself.

**Routines** are the consequential one. A routine is a saved configuration — prompt, repositories, connectors, cloud environment — that fires on a schedule, an authenticated HTTP POST to a per-routine `/fire` endpoint, or a GitHub event, on Anthropic's infrastructure, with **no permission prompts at all** during a run.[^2] Available on Pro/Max/Team/Enterprise, in research preview, with a daily run cap. Three design details preview this whole week:

1. **Network egress is allowlisted by default.** The Default environment permits package registries and common dev domains; everything else fails with `403` and an `x-deny-reason: host_not_allowed` header. Least-privilege as the default posture, not an add-on.
2. **Trigger payloads arrive wrapped as untrusted data.** Text POSTed to `/fire` reaches the agent inside a `<routine-fire-payload>` block that labels it untrusted and instructs Claude not to follow instructions inside it unless the routine's own prompt opts in. That is a prompt-injection mitigation baked into the trigger surface — the lethal-trifecta lesson ([[03-wed-mcp-security]]) turned into product.
3. **A green run status means the infrastructure didn't fail, not that the task succeeded.** The docs say this explicitly. Anthropic is telling you that task-level success measurement — Friday's whole lesson — is *your* job.

Adjacent, for scale: Opus 4.8's **dynamic workflows** research preview (May 28, 2026) lets Claude write a JavaScript orchestration script that fans work across parallel subagents, capped at 16 concurrent and 1,000 total per run.[^8] It is a bulk-work tool (codebase migrations, mass analysis), not a scheduler — but it signals where platform-native orchestration is going: the model writes the workflow.

## Layer 2 — The decision framework: determinism vs judgment, per step

The wrong question is "should I use n8n or an agent?" The right question is asked per step: **can I write down, in advance, exactly what correct behavior is for this step?**

- If yes → the step is deterministic. Implement it as code or a workflow node. An LLM in this position adds cost, latency, and a failure mode (nondeterminism) while contributing nothing.
- If no — because the step requires reading, interpreting, ranking, or writing — it is a judgment step. That is where the model goes, wrapped in the tightest output contract you can write (Thursday).

Run the test over Saturday's build and the shape falls out immediately:

| Step | Deterministic? | Implementation |
|---|---|---|
| Fetch 5 sources on schedule | Yes | cron + HTTP client |
| Parse HTML → clean text | Yes | extraction library |
| Exact/near-duplicate detection | Mostly | hashing + similarity threshold |
| "Is this item relevant to my niche?" | No | LLM judgment, structured output |
| Cross-source synthesis into a brief | No | LLM judgment, cited |
| Delivery to email/file | Yes | code |

Two judgment steps out of six. The 2026 consensus architecture — deterministic spine, judgment islands — follows from this arithmetic, and the industry converged on it the hard way: the dominant published post-mortem pattern is teams that deployed agentic autonomy on tasks a flowchart could have handled, paying for nondeterminism they didn't need.[^9][^11] Anthropic said it before it was fashionable: "consistently, the most successful implementations weren't using complex frameworks... they were building with simple, composable patterns."[^3]

Three refinements the naive version of this test misses:

- **Judgment steps decay into deterministic ones.** Once your relevance classifier has seen 500 labeled examples, you may discover a cheap heuristic (source + keyword) that matches the LLM 95% of the time. The mature system migrates steps leftward over time. Budget for that migration; it is where unit costs collapse.
- **Deterministic steps hide judgment at the edges.** "Parse HTML" is deterministic until the site redesigns. The *detection* of that drift is a judgment problem (Thursday covers layout-drift detection). Deterministic code plus a judgment-based watchdog beats either alone.
- **The scheduler itself should never be the model.** Let an agent decide *what* to do inside a run; never let it decide *whether* runs happen. Schedules, triggers, and kill switches stay in boring infrastructure you can reason about at 3 a.m.

## Layer 3 — Total-cost math, July 2026 prices

Cost the same workload in all three lanes. Workload: the Saturday build — 1 run/day, 5 sources, ~40 candidate items/run, 2 judgment stages, a ~2,500-word cited brief out.

**Token cost per run (lane-independent floor).** On Sonnet 5 — the default agent workhorse at **$2/$10 per Mtok intro pricing through 2026-08-31, then $3/$15**[^12] — a run that processes ~150K input tokens (fetched content + prompts across stages) and produces ~15K output tokens costs about **$0.45 at intro pricing (~$0.68 after August 31)**. Per month: ~$14 intro, ~$20 after. Remember the tokenizer note from the master refresh: current Anthropic models tokenize ~30% heavier than the 2025 generation, so April-era per-token intuitions undercount.[^13] Date-stamp every cost table you show a client; this one is stamped 2026-07-17.

**Lane 1 — n8n.** Cloud Starter is $24/mo for 2,500 executions; one workflow run = one execution regardless of step count, so 30 runs/day fits the cheapest tier trivially. Self-hosted Community Edition is free with unlimited executions on a ~$5/mo VPS.[^4] Plus tokens (bring your own key): total **~$19–38/mo**. The hidden cost is engineering time at the edges: eval harness, version control, and complex extraction logic all fight the platform.

**Lane 2 — code-first.** Infrastructure ~$5/mo (VPS or free GitHub Actions minutes for a daily job) plus tokens: **~$19–25/mo**. The visible cost is build time — call it 2–4 focused days with Claude Code for pipeline + eval + alerting (Saturday compresses this). The payoff is that reliability engineering has somewhere to live.

**Lane 3 — Routines.** Draws down your existing Claude subscription usage (Pro/Max), subject to the daily routine cap, with metered overage available via usage credits.[^2] Marginal dollar cost: possibly zero if your subscription has headroom. The real constraints are the 1-hour minimum interval, no local filesystem, connector-only integrations, and research-preview status — the API surface ships under an `experimental-` beta header and may change.

**Make, for contrast:** an agent run on Make's built-in Small model consumes roughly 43–50 credits; at Core-plan rates (~$12/mo for 10,000 credits) a single daily agent run lands ~$2–7/mo but scales linearly and unforgivingly with frequency — 50 runs/day blows through plans that look cheap at demo volume.[^6] This is the generic workflow-platform trap: platform metering (tasks, credits, operations) is priced for *event plumbing*, and LLM-heavy workloads sit awkwardly on it.

The honest conclusion: **at solo-operator scale, cost does not discriminate between lanes — everything lands in tens of dollars a month.** The discriminating variables are reliability engineering (lane 2 wins), integration breadth and non-engineer legibility (lane 1 wins), and zero-infrastructure convenience (lane 3 wins). Cost only becomes the decider at volume, where per-execution platform metering crosses over VPS-flat pricing — do the crossover math per client, at post-August token prices, not intro ones.

## Layer 4 — The live controversy: "training wheels" vs "unreliable automations"

Two camps, both loud, both partly right.

**Camp A — "workflow tools are training wheels."** The code-first case: serious automations need code review, diffable history, test suites, and eval harnesses, and visual platforms obstruct all four. A JSON blob exported from a canvas is not a reviewable artifact; a workflow you can't regression-test is a workflow you can't safely change. The strongest evidence is what happens at the boundary: every nontrivial n8n deployment sprouts Function nodes full of JavaScript — code, but stripped of the tooling that makes code safe. On this view the platforms are prototyping surfaces, and SAP's embrace is the tell: enterprises buy legibility and governance optics, not engineering excellence.

**Camp B — "agents are unreliable automations."** The workflow-platform case, with 2026 receipts: enterprises that shipped agentic autonomy where determinism sufficed are overrepresented in the 88%-never-reach-production statistic, with evaluation gaps the top blocker named by 64% of leaders and non-deterministic outputs the number-one production-readiness barrier named by 70%.[^9] A Make agent whose every decision renders visibly on the canvas, wrapped by deterministic scenario steps, is *more* auditable than a Python agent whose reasoning lives in a log file nobody reads.[^6] Anthropic's own "simplest composable patterns" guidance is Camp B ammunition from a company that sells agents.[^3]

**Where this course lands** (opinion, labeled): the dichotomy mistakes a *surface* choice for an *engineering* choice. The properties that decide production success — determinism where possible, output contracts, golden-set evals, alerting — are achievable in either surface and defaulted in neither. Code-first makes them easier to build; platforms make them easier to skip. For this cohort, whose differentiation is engineering discipline, the build week is code-first via Claude Code — while using n8n or Make without embarrassment for connector-heavy, judgment-light client work where the platform's 1,000+ integrations are worth more than your pipeline elegance. Choosing a lane per project is the skill; loyalty to a lane is a cargo cult.

## Experiment — map, price, and schedule

**Part 1 (30 min): the placement drill.** Open Claude Code in a scratch directory and paste this:

> *I'm designing unattended automations. For each of the following, decompose into steps, mark each step DETERMINISTIC or JUDGMENT, then recommend one of: workflow platform (n8n/Make), code-first (Agent SDK + cron), or Claude Code Routines — with one sentence of justification and one failure mode of the recommended lane. (1) Nightly: pull yesterday's Stripe transactions, flag anomalies vs 90-day baseline, Slack a summary. (2) On each new PR: apply our review checklist and leave inline comments. (3) Hourly: watch 3 competitor pricing pages, alert on changes. (4) Weekly: read our support inbox, cluster complaints into themes, draft a report. (5) On webhook from our monitoring tool: triage the alert, correlate with recent commits, open a draft fix PR.*

Grade its answers against Layer 2. Items 2 and 5 should surface Routines' GitHub and API triggers specifically;[^2] item 3 should provoke a scraping-legality flag you'll be equipped to evaluate on Wednesday. Argue with anything you disagree with — the argument is the exercise.

**Pass bar:** ≥4 of the 5 lane recommendations match your own Layer-2 grading (a disagreement counts as a match only if you can defend it in two sentences citing a specific Layer-2 constraint). Hard requirements regardless of score: items 2 and 5 name Routines' GitHub/API triggers, and item 3 raises the legality flag. Miss either and the drill is a fail — reread Layer 2 and re-run.

**Part 2 (20 min): touch all three scheduling tiers.**

1. In a Claude Code session: `/loop 2m summarize what changed in this directory` — then ask *"what scheduled tasks do I have?"* and watch `CronList` return the job with its 8-character ID and jittered schedule. Delete it.
2. Run `/schedule` and walk the conversational flow for a daily 9 a.m. routine (you can cancel before saving if you don't want it live). Note what it asks for — repos, connectors, environment — versus what `/loop` asked for (nothing). That delta *is* the unattended-operation checklist.
3. Ask Claude Code: *"Compare /loop, Desktop scheduled tasks, and Routines for a daily scraper that needs to hit arbitrary websites and write local files. Which constraint kills which option?"* Correct answer: Routines' network allowlist and no-local-files posture both bite; local scheduling or a VPS wins for Saturday's build — which is exactly what the code-lab does.

**Pass bar:** all three tiers touched hands-on (CronList showed the job; /schedule flow walked to the save/cancel decision), and the step-3 answer names both killing constraints — the network allowlist *and* the no-local-files posture. Naming only one is a fail; it means the unattended-operation checklist hasn't landed.

**Part 3 (10 min): the cost table.** Have Claude Code produce the Layer 3 table for *your* niche's version of the Saturday build (your sources, your frequency), at both intro and post-August Sonnet 5 pricing. Keep the artifact; you will reuse it in the Saturday README and with clients.

**Pass bar:** recompute one row of the table by hand (tokens × price, per Layer 3's method) and match Claude's figure within 10%. The table must show both price regimes; a table quoting only intro pricing is an automatic fail — that's the "silent margin bomb" from the mistakes list below.

## Common mistakes experts see

- **Choosing the runtime by identity, not by workload.** "We're engineers, so n8n is beneath us" and "we're no-coders, so agents are scary" produce identical failure rates in opposite lanes.
- **Letting the model own the schedule.** Agents decide *within* runs; infrastructure decides *whether* runs happen. No exceptions survive contact with a 3 a.m. incident.
- **Pricing at intro rates.** Sonnet 5's $2/$10 ends 2026-08-31.[^12] Client quotes built on intro pricing are silent margin bombs.
- **Treating "the run went green" as success.** Routines' docs warn that green means the session exited without infrastructure error, nothing more.[^2] Task-level success is measured by evals, or it is not measured.
- **Ignoring platform metering at scale.** Tasks/credits pricing is linear in event volume; flat VPS pricing is not. Find the crossover before the client does.
- **Building bespoke orchestration on day one.** The Agent SDK, LangGraph, and n8n each embody years of retry/checkpoint/trigger lessons. Your handrolled framework embodies none, yet.
- **Forgetting the 7-day expiry and jitter exist.** Teams "lose" scheduled tasks that self-expired by design, then rebuild them on infrastructure without expiry — deleting the safety feature instead of learning from it.[^1]

## Reflection questions

1. Name a step in your planned Saturday build that you marked JUDGMENT today but that could plausibly migrate to DETERMINISTIC after 90 days of operation. What data would you need to have collected to make the migration safely?
2. Routines run with no permission prompts by network-allowlisted design; `/loop` inherits your session's permission state. For which of your automations is *neither* posture right, and what would the right one be?
3. Anthropic ships jitter and 7-day expiry as scheduling defaults. If you were designing the defaults for *your* client's automation platform, what failure are you most afraid of, and what default would encode that fear?
4. Construct a workload where Make's per-credit pricing beats self-hosted n8n *and* code-first on total cost of ownership. What had to be true about engineering time for the answer to come out that way?
5. The 88% pilot-failure statistic is quoted everywhere, usually without its decomposition. Which of Forrester's three failure causes (unclear success criteria, insufficient tool/data access, eval-coverage drift) does your runtime choice actually influence, and which does it merely relocate?
6. When SAP embeds n8n into Joule Studio at GA, what happens to the "training wheels" argument inside enterprises — and does that make the argument more true or less true for a solo builder selling to those enterprises?

## My take (reviewer lens)

**Michael Seibel** would attack the lesson's center of gravity: you spent five thousand words on runtime selection for a daily digest a motivated person ships in an afternoon on any of the three lanes. The 88% of pilots that die mostly die because nobody wanted the output badly enough, not because the scheduler was wrong. Ship the ugly cron job this week; earn the right to a runtime opinion with usage. He's right that the decision is reversible at this scale — and the lesson should say so plainly: **at one-run-a-day, you can migrate lanes in a weekend; decide fast and ship.**

**Chip Huyen** would push on the cost section's precision theater: per-run token math to the cent, while the dominant cost — engineering time to build and *maintain* the eval harness, which recurs every time a source or model changes — appears as an unpriced aside. Real automation TCO is maintenance-dominated, and the lesson's tables make the cheap part legible while the expensive part stays vibes. Fair. Thursday and Friday partially answer this; the honest fix is to track your own hours Saturday and put them in the table.

**Boris Cherny's** current public record is running agents at fleet scale, and from that vantage the tooling pitfall here is session-scoped thinking: `/loop` demos beautifully and then teams are shocked their automation died with the terminal. The spectrum table carries the warning, but he'd want it louder: *the demo tier and the production tier are different products that happen to share a brand.* Routines' no-prompt autonomy is likewise not a convenience feature — it's a permissions decision you're making implicitly. Making it explicitly is Tuesday's job.

## Further reading

**Must-read**

- Claude Code docs — "Automate work with routines" (fetched and verified this session).[^2]
- Anthropic — "Building Effective Agents" (Dec 2024). Still the best 20 minutes on workflow-vs-agent judgment.[^3]
- Claude Code docs — "Run prompts on a schedule" — read for the jitter/expiry design decisions, not just the syntax.[^1]

**Recommended**

- n8n blog — "Announcing SAP's strategic investment in n8n" (May 2026) — read as an enterprise-positioning artifact.[^5]
- Make — "Announcing the next generation of Make AI Agents" (Feb 2026).[^6]
- Anthropic — Claude Opus 4.8 announcement, dynamic workflows section (May 2026).[^8]

**Optional**

- Redis blog — "AI Agents vs Workflows: When to Use Each" — a clean vendor-neutral statement of the consensus.[^11]
- Zapier pricing page — study the task-metering model as a pricing-design case, whatever you think of the product.[^7]

## Citations

[^1]: Claude Code documentation. "Run prompts on a schedule." https://code.claude.com/docs/en/scheduled-tasks — fetched live 2026-07-17. `/loop`, `CronCreate`/`CronList`/`CronDelete`, 5-field cron, jitter rules (up to 30 min for recurring; half-interval for sub-hourly), 7-day expiry, 50-task session cap, session-scoped limitations, and the comparison table of cloud/Desktop/`/loop` tiers.

[^2]: Claude Code documentation. "Automate work with routines." https://code.claude.com/docs/en/routines — fetched live 2026-07-17. Research-preview status; schedule/API/GitHub triggers; per-routine `/fire` endpoint with bearer token under the `experimental-cc-routine-2026-04-01` beta header; `<routine-fire-payload>` untrusted-data wrapping; Default environment "Trusted" network allowlist with `403` / `x-deny-reason: host_not_allowed`; no permission prompts during runs; daily run caps and subscription usage draw-down; green-status caveat.

[^3]: Anthropic. "Building Effective Agents." https://www.anthropic.com/engineering/building-effective-agents — December 19, 2024. "Consistently, the most successful implementations weren't using complex frameworks... simple, composable patterns"; workflow-vs-agent definitions used throughout this lesson.

[^4]: n8n pricing and 2.x capabilities: https://n8n.io/pricing/ (Cloud Starter $24/mo / 2,500 executions; Pro $60 / 10,000; Business $800 / 40,000; one workflow run = one execution; free self-hosted Community Edition) corroborated by InstaPods "n8n Pricing 2026" https://instapods.com/blog/n8n-pricing/ and Automation Atlas https://automationatlas.io/answers/n8n-pricing-self-hosted-vs-cloud-2026/ ; n8n 2.0 AI Agent nodes / MCP node / multi-agent per Nodesify "n8n 2026 Updates" https://nodesify.com/blog/n8n-workflow-automation-guide-2026 and HatchWorks "n8n Guide 2026" https://hatchworks.com/blog/ai-agents/n8n-guide/ (search-verified 2026-07-17; fetch egress-blocked for these hosts — liveness pass pending).

[^5]: n8n blog. "Announcing SAP's strategic investment in n8n." https://blog.n8n.io/n8n-sap/ — May 12, 2026. $5.2B valuation (2x Oct 2025), embedding in SAP Joule Studio with GA planned Q3 2026, 1,400+ enterprise customers, 1.7M monthly active builders. Corroborated by PR Newswire https://www.prnewswire.com/news-releases/n8n-valuation-doubles-to-5-2bn-as-sap-makes-strategic-investment-and-plans-to-embed-the-ai-platform-into-joule-studio-302767227.html and The Next Web https://thenextweb.com/news/n8n-sap-joule-studio-workflow-automation (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: Make. "Announcing the next generation of Make AI Agents." https://www.make.com/en/blog/announcing-next-generation-make-ai-agents — GA February 11, 2026; agents on the same canvas as scenarios. Credit costs: Make Help Center "Credit usage for AI agents" https://help.make.com/credit-usage-for-ai-agents (~43–50 credits per agent run on built-in Small model; 1 credit/operation + token-based credits; BYO API key on paid plans), plan rates per Lindy "Make.com Pricing" https://www.lindy.ai/blog/make-com-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Zapier. Pricing page. https://zapier.com/pricing — task-metered tiers (Free 100 tasks/mo; Professional from $29.99/mo / 750 tasks; Team from $103.50/mo), AI Agents and Zapier MCP bundled across paid plans. Corroborated by Activepieces "Zapier Pricing Breakdown 2026" https://www.activepieces.com/blog/zapier-pricing and AIToolGrade review https://aitoolgrade.com/review/zapier.html (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: Anthropic. "Introducing Claude Opus 4.8." https://www.anthropic.com/news/claude-opus-4-8 — May 28, 2026. Dynamic workflows research preview: Claude writes a JavaScript orchestration script; runtime executes it in the background. Caps of 16 concurrent / 1,000 total subagents per run per MarkTechPost coverage https://www.marktechpost.com/2026/05/28/anthropic-ships-claude-opus-4-8-alongside-dynamic-workflows-and-cheaper-fast-mode-with-workflows-capped-at-1000-subagents/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Failure statistics: 88% of agent pilots never reach production (Anaconda/Forrester lineage), Forrester decomposition (41% unclear success criteria / 33% insufficient tool-data access / 26% eval-coverage drift), 64% naming evaluation/observability the top blocker, 70% naming non-deterministic outputs the #1 production-readiness barrier — Digital Applied, "AI Agent Adoption 2026: 120+ Enterprise Data Points," https://www.digitalapplied.com/blog/ai-agent-adoption-2026-enterprise-data-points , corroborated by CIO.com https://www.cio.com/article/3850763/88-of-ai-pilots-fail-to-reach-production-but-thats-not-all-on-it.html and AnAr Solutions https://anarsolutions.com/why-agentic-ai-pilots-fail-production/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending). Treat the decomposition percentages as survey-grade, not audit-grade.

[^10]: Anthropic. Claude Agent SDK overview. https://code.claude.com/docs/en/agent-sdk/overview — the runtime underlying Claude Code, exposed for custom agents; also verified in the July 2026 landscape delta (`vault/00-program/_refresh-2026-07-landscape-delta.md`, §4).

[^11]: Redis blog. "AI Agents vs Workflows: When to Use Each." https://redis.io/blog/agents-vs-workflows/ — workflows for known processes/stable inputs/high mistake-cost; agents where paths can't be pre-defined; hybrid as default (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^12]: Anthropic. "Claude Sonnet 5." https://www.anthropic.com/news/claude-sonnet-5 — June 30, 2026. Intro pricing $2/$10 per Mtok through 2026-08-31, then $3/$15; default model in Claude Code with 1M context. Verified in the July 2026 master refresh report (two-source) and landscape delta §1; corroborating coverage TechCrunch https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/ .

[^13]: Course master refresh report, `vault/00-program/_refresh-2026-07-master-report.md` (2026-07-17), cross-cutting theme 1: new tokenizer on Opus 4.7+/Sonnet 5/Fable 5 measures ~+30% tokens versus the prior generation — all per-token cost math must be restated against it.

_last_verified: 2026-07-17_
