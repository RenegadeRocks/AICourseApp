---
type: lesson
block: block-7-onboarding-tracking
week: week-20
session_slug: build-community-paid-inner-circle
day_of_cycle: 6
day_name: sat
date_due: 2026-10-03
tags:
  - build
  - sop-library
  - community-launch
  - membership-economics
  - ghost-town
  - code-lab
sources:
  - gawande-checklist-manifesto
  - spp-scaling-framework
  - churnkey-membership-churn
  - stickyhive-skool-vs-discord
  - spinks-business-of-belonging
  - eightx-ltv-cac
  - digitalapplied-ttv-2026
  - arxiv-agent-s-sop
last_verified: 2026-07-17
word_count_target: 4200
---

# BUILD: your SOP library + paid-community launch plan

## Why this matters

Five days of concepts converge into two artifacts you will own by tonight: a
runnable SOP library that gets three of your core procedures out of your head, and
a complete paid-community launch plan a stranger could act on. This is the Block 7
capstone build. You will write three SOPs (onboarding, delivery, one growth), tag
which become agents, design a paid inner circle with tiers and pricing, plan the
first 30 members, and run your real numbers through the `code-lab/1/` model,
including the ghost-town early-warning metric that tells you if the community is
dying while you can still save it. The deliverable is not notes. It is a system
and a plan you could execute Monday.

## Prerequisites

- Every lesson this week:
  [[01-mon-sops-the-operating-system-of-a-scaling-business|Mon]],
  [[02-tue-onboarding-sops-the-first-30-days|Tue]],
  [[03-wed-delivery-and-growth-sops|Wed]],
  [[04-thu-building-community-the-compounding-moat|Thu]],
  [[05-fri-the-paid-inner-circle-and-membership-economics|Fri]]. Today assembles
  them.
- The `code-lab/1/` tools in this folder. Run the README pass bar first if you have
  not: `python sop_generator.py` and `python membership_model.py` should both run
  clean.

## The build, in five parts

Work through these in order. Each produces a concrete artifact; together they are
the systematized-business deliverable.

### Part 1 — Write three core SOPs (from Mon-Wed)

Pick the three procedures that matter most and write them in checklist form using
the `code-lab/1/sop_generator.py` structure. One from each category:

1. **Onboarding SOP.** Your "signed to activated" procedure, designed around
   time-to-first-value (Tuesday). Trigger, ordered steps, the first-value milestone
   and its target day, the definition of done (activation confirmed), and the day-3
   and day-7 flags.
2. **Delivery SOP.** The runbook for producing one unit of the thing you sell
   (Wednesday). Trigger, inputs, production checklist, and, non-negotiable, the
   quality-gate rubric with named failure modes.
3. **One growth SOP.** Your highest-leverage growth activity as a triggered
   procedure (Wednesday): content, outreach, or referral. Trigger, checklist,
   definition of good.

For each, build an `SOPSpec` and call `render_sop(spec)` to get clean checklist-form
Markdown. Set `frequency`, `judgment`, and `error_cost` honestly so the generator's
run-mode verdict is meaningful. Write for the least experienced person who will run
it, and include the A-grade example and failure modes, that is what separates a
usable SOP from a step list (Wednesday).[^1]

### Part 2 — Tag which SOPs become agents (from Wed)

Run each SOP through the SOP-to-agent rubric. The generator does this automatically
via `automation_recommendation(spec)`, labeling each **AGENT-CANDIDATE**,
**AGENT-ASSIST**, **HUMAN-IN-THE-LOOP**, or **HUMAN-RUN** based on frequency,
determinism, and cost of error. Read the verdicts and produce your two-column view:
which procedures graduate into automation (built with the
[[block-3-advanced-topics-voice/week-08-automation-agent-integration-mcps--build-hybrid-agent-scraper-summarizer/01-mon-the-automation-spectrum-in-2026|Week 8]]
patterns) and which stay human. For every agent candidate, note the extra
requirement from Monday and Wednesday: the agent-run SOP must be *stricter* than the
human one, with failure modes and stop conditions explicit, because the agent fills
ambiguity with a confident wrong guess.[^2]

### Part 3 — Design the paid inner circle (from Thu-Fri)

Specify the community as a product a stranger could evaluate:

1. **The value bundle.** Name the three ingredients concretely (Friday): the access
   (to you and to peers), the ongoing content and live element (what recurring value
   gives a reason to stay *this* month), and the belonging (the shared identity, the
   Spinks "members create value for each other" mechanic).[^3]
2. **Platform choice, on economics.** Pick Skool, Circle, Discord, or Slack based on
   your design and its real cost, not hype (Thursday). Write down the *real* monthly
   cost including the tier you will actually need and the transaction fees, not the
   sticker price.[^4]
3. **Tiers and pricing.** Two or three tiers differentiated by access and depth
   (Friday, applying the [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/04-thu-tiers-upsell-hooks-and-expansion-revenue|Week 16 tier logic]]).
   A core tier and an inner-circle tier at minimum. Price on value and belonging, but
   confirm it clears platform fees, processing, and cost to serve with margin.

### Part 4 — The first-30-members plan (from Thu)

The cold-start problem kills communities; solve it explicitly (Thursday):

1. **The seeding nucleus.** Who are the first 10-15 founding members you will
   personally recruit before opening the doors, and where do they come from (existing
   clients, audience, the free community)? An empty room repels; you launch with it
   already alive.
2. **The founder-as-engine commitment.** What will you personally post and do in the
   first 30 days to set the culture? Be specific: a daily post, a weekly live call, a
   response to every introduction. If you are not willing to be the engine, say so now,
   before you charge anyone.
3. **The first-interaction design.** The introductions thread, the weekly question,
   the first-week challenge, whatever gives every new member a low-friction reason to
   make their first post (their community "first-value" moment).

### Part 5 — Run your real numbers (code-lab)

Open `code-lab/1/membership_model.py` and plug in your own tiers, churn estimate,
gross margin, and CAC. Produce:

1. **Your MRR, ARPU, average member lifetime, LTV, and LTV:CAC** at a realistic
   churn assumption. Read the LTV:CAC against the 3:1 benchmark.[^5]
2. **The churn-sensitivity check.** Re-run with churn doubled and watch LTV roughly
   halve. State the churn level at which your LTV:CAC drops below 3:1. This is the
   line you cannot cross.
3. **The ghost-town early-warning wiring.** Decide what your active-member ratio and
   first-week-activation thresholds are, and confirm `ghost_town_warning` correctly
   flags a declining engagement history. This is the leading indicator you will watch
   weekly once you launch, because it moves before churn does.

## Worked example: assembling it for the AI-automation agency

The full assembly, using the tools, as a model for your own.

**SOPs (Parts 1-2).** Three `SOPSpec`s: "New client kickoff" (weekly, mixed
judgment, medium error cost → the generator returns AGENT-ASSIST: the CRM tag,
templated welcome, and project creation are agent-drafted, the kickoff stays human);
"Produce one monthly report" (monthly, deterministic → AGENT-ASSIST: agent pulls
metrics and drafts the narrative, human does analysis, recommendations, and the
quality gate); "Publish one weekly case study" (weekly growth SOP, mixed → human-run
with agent assist on the draft). Two-column view: the data pull, welcome sequence,
and first-draft generation graduate to agents; the kickoff, analysis,
recommendations, and every quality gate stay human.

**Community (Parts 3-4).** Paid inner circle on Skool ($99/mo Pro, ~2.9% fee).[^4]
Two tiers: Core at $50/mo (community + monthly group call + resource library),
Inner Circle at $200/mo (+ monthly small-group call with the founder + async
access). Value bundle: access to the founder and to a room of other automation
consultants, a recurring monthly live teardown, and the shared identity of "operators
building real AI automation businesses." First 30: seed 12 founding members from the
existing free Discord's most engaged people, founder posts daily and runs the first
live call in week one, introductions thread as the first-interaction hook.

**Numbers (Part 5).** From `membership_model.py` at 80 Core + 12 Inner Circle: MRR
$6,400, ARPU ~$70, and at 4% churn, average lifetime 25 months, LTV ~$1,565, LTV:CAC
~10:1 against a $150 CAC. Churn-sensitivity: at 10% churn, LTV falls to ~$626 (40% of
the healthy figure) from the same revenue today, and LTV:CAC drops toward 4:1, still
passing but on a doomed trajectory. Ghost-town check: a four-week engagement history
sliding from a 37% to a 17% active ratio flags `GHOST_TOWN_RISK` on three grounds
(below the ratio floor, below first-week activation, and three consecutive declines),
weeks before that decline would show up as churned MRR. That flag is the whole point:
it is the smoke alarm; the churn is the fire.

## The deliverable and its pass bar

Produce two artifacts:

- **A runnable SOP library:** three SOPs in checklist form (rendered via the
  generator), each with an owner, version, definition of done, failure modes, and a
  run-mode verdict, plus your two-column human/agent split.
- **A paid-community launch plan:** the value bundle, platform choice with real cost,
  tiers and pricing, the first-30-members seeding-and-engine plan, and your membership
  numbers (MRR, LTV, LTV:CAC, the churn danger line, and the ghost-town threshold) from
  the model.

**Pass bar:** (a) three SOPs a stranger could execute, at least one honestly tagged
as an agent candidate with its stricter failure modes noted; (b) a paid community a
stranger could join with a clear value promise, a defensible price that clears its
costs, and a concrete plan for the first 30 members that does not launch into an
empty room; and (c) membership numbers you would defend, including the churn level
that breaks your LTV:CAC and a ghost-town early-warning threshold you will actually
watch. If your numbers say the membership does not clear 3:1 at a realistic churn,
passing today means *saying so with the numbers* and redesigning the price, tiers, or
cost to serve, not launching a treadmill.

## Common mistakes experts see

1. **Writing SOPs as prose, not checklists.** The generator forces the checklist
   form; keep it. Imperative, verifiable, one line per step.[^1]
2. **Skipping the quality-gate rubric on the delivery SOP.** A delivery SOP with no
   quality gate systematizes mediocrity. Write the rubric and the failure modes.
3. **Tagging a judgment task as an agent candidate.** Read the generator's verdict,
   but sanity-check it: if the task is really judgment, keep it human regardless of
   frequency.[^2]
4. **Designing the community before choosing on economics, or vice versa.** Design the
   community you want, then pick the platform whose real cost fits. Do not let the
   platform's sticker price fool you.[^4]
5. **A launch plan with no seeding nucleus.** Launching to strangers into an empty
   room is the modal community death. Seed the founding cohort first.
6. **Modeling MRR without stress-testing churn.** MRR today hides a doomed
   trajectory. Run the churn-doubled case and find the LTV:CAC break line before you
   launch.[^5]

## Reflection questions

1. Which of your three SOPs was hardest to write, and does that difficulty reveal a
   part of your business that is pure founder-in-the-head knowledge?
2. What did the generator's run-mode verdicts tell you about how much of your delivery
   could actually run without you? Did any verdict surprise you?
3. At your realistic churn assumption, what is your LTV:CAC, and at what churn does it
   break 3:1? Is your current retention plan enough to stay on the right side of that
   line?
4. What is your ghost-town early-warning threshold, and how will you actually see the
   active-member ratio each week once you launch?
5. Are you genuinely willing to be the community's engine for the first 30 days and
   beyond? If your honest answer is no, what does that mean for whether you should
   launch a *paid* community at all?

## My take (reviewer lens)

**Michael Seibel** would want you to ship the ugly version of all of this rather than
perfect one piece: three rough-but-real SOPs and a community with ten paying founding
members beats a beautiful SOP library and a launch plan you never execute. He is
right, and the `code-lab` tools are deliberately tiny so you wire estimates today and
replace them with real numbers once you launch, rather than waiting for perfect data.
Ugly and launched beats polished and hypothetical.

**Boris Cherny** would flag the agent-candidate SOPs as the place most likely to
bite: the generator's verdict is a starting point, not a safety certificate, and an
under-specified SOP handed to an agent scales your mistakes. His correction is the
stricter-SOP discipline, spelled-out failure modes and explicit stop conditions on
every agent-run procedure, which is exactly why the generator asks for failure modes
and the pass bar requires them.

**Chip Huyen** would insist the ghost-town metric be instrumented from member one,
not bolted on after churn appears: a leading indicator is worthless if you start
watching it once the community is already dying. Wire the active-member-ratio tracking
into your launch, so week one has a baseline and week eight has a trend you can act on.

## Further reading

**Must-read**

- Re-read this week's [[05-fri-the-paid-inner-circle-and-membership-economics|Friday
  economics]] alongside the `code-lab/1/README.md` as you run your numbers.

**Recommended**

- SPP on delivery SOPs that capture "what good looks like," for the Part 1 quality
  bar.[^1]
- Churnkey's membership-churn benchmarks, for calibrating the churn assumption in your
  model.[^5]

**Optional**

- The 2026 Skool/Circle/Discord comparisons, to finalize your platform choice on real
  economics.[^4]

## Citations

[^1]: "Scaling Productized Services: 3-Pillar Quality Framework," SPP.
https://spp.co/blog/scaling-productized-services-framework/ — SOPs must capture what
good looks like, with an A-grade example and named failure modes. (search-verified
2026-07-17; fetch egress-blocked — liveness pass pending; corroborated by
manyrequests.com/blog/productized-service-guide.)
[^2]: "Agent-S: LLM Agentic workflow to automate Standard Operating Procedures,"
arXiv 2503.15520. https://arxiv.org/pdf/2503.15520 — structured SOPs improve agent
controllability; agents need explicit procedure and stop conditions. (search-verified
2026-07-17; corroborated by v7labs.com/automations/standard-operating-procedures-sops.)
[^3]: David Spinks, *The Business of Belonging*, Wiley.
https://www.wiley.com/en-us/The+Business+of+Belonging:+How+to+Make+Community+your+Competitive+Advantage-p-9781119766124
— the access + content + belonging value bundle; members create value for each other.
(Evergreen; corroborated by nityesh.com/book-review-business-of-belonging/.)
[^4]: "Skool vs Discord vs Circle 2026," Stickyhive.
https://stickyhive.ai/skool/vs-discord/ — Skool $99 Pro / ~2.9% fee; Circle $89/$199;
Discord free; platform fees set the pricing floor. (search-verified 2026-07-17;
corroborated by schoolmaker.com/blog/circle-so-pricing.)
[^5]: "Membership Churn: Benchmarks, Calculator and Best Practices," Churnkey.
https://churnkey.co/blog/membership-churn/ — healthy monthly churn <5%; LTV divides by
churn so small churn changes swing LTV hard; 3:1 LTV:CAC benchmark. (search-verified
2026-07-17; corroborated by eightx.co/blog/ltv-cac-ratio-guide.)

_last_verified: 2026-07-17_
