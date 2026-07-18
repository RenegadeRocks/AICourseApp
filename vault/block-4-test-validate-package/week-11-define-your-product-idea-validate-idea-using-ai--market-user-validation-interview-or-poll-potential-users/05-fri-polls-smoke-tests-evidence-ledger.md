---
type: lesson
block: block-4-test-validate-package
week: week-11
day_of_cycle: 5
day_name: fri
session_slug: market-user-validation-interview-or-poll-potential-users
date_due: 2026-07-31
tags: [polls, survey-design, smoke-tests, fake-door, waitlist, pre-order, paid-pilot, evidence-ledger, decision-rules, wilson-intervals, usage-depth, agent-product-metrics]
sources:
  - pew-question-wording
  - waitlister-statistics
  - flowjam-waitlist-pages
  - userintuition-landing-tests
  - chameleon-fake-door
  - kromatic-fake-door
  - gascoigne-buffer-idea-to-customers
  - theforest-validation-experiments
  - andres-max-validate-2026
  - nyu-shipping-not-asking-2026
last_verified: 2026-07-17
word_count_target: 5300
---

# Polls, smoke tests, and the evidence ledger — quantitative validation with a pre-registered verdict

## Why this matters

Interviews gave you depth on a handful of humans; today adds breadth and, more importantly, *cost*. The evidence classes that decide build/pivot/kill are the ones where saying yes costs the sayer something: a click toward a price, an email into a waitlist, a card into a pre-order, money into a pilot. Today you learn to design polls that do not lead the witness, to climb the smoke-test ladder from waitlist to paid pilot in order of escalating evidence strength, and to aim the Week 10 launch page at a validation question instead of a launch vibe. Then everything converges into the week's central artifact: the **evidence ledger**, where every assumption from Monday meets every atom of evidence from the week, scored by class and direction, and a decision rule you wrote before the data arrived returns BUILD, PIVOT, or KILL. Saturday you run it; today you learn to build it honestly. This is also where the week's controversy gets its final round: if building is this cheap, why not skip the smoke test and ship? The answer turns out to be a claim about *instrumentation*, not effort.

## Prerequisites

- Monday's frozen decision rule; Wednesday's tagged atoms; Thursday's synthetic boundary memo.
- [[01-mon-landing-page-as-conversion-machine|Block 2 Week 3 Mon]] — landing-page conversion mechanics; and [[06-sat-validation-instrumentation|Block 2 Week 3 Sat]] — the canonical home for CI-stats discipline and Wilson intervals. One-line recap here; the derivation lives there.
- [[../week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/_week|Week 10]] — the launch page and creatives you will now repurpose as an instrument.

## Layer 1 — Polls that don't lead the witness

Surveys and polls are stated-preference instruments: cheap breadth, moderate bias, and useful mostly to *quantify* patterns interviews discovered, never to discover patterns. Four design rules carry most of the value:

1. **Behavior before attitude.** Open with what they did ("How did you handle [task] last week?" with concrete options), not what they think. The Pew Research Center's methodology work on question wording is the standard reference for how much answers move with framing: small wording shifts (e.g., "not allow" vs "forbid" framings) reliably move response distributions by double digits.[^1] If Pew's professionally neutral instruments wobble that much, your enthusiast-drafted survey starts contaminated; the fix is behavioral anchoring plus neutral framing plus randomized option order where your tool supports it.
2. **No idea exposure before the pain questions.** Same rule as Wednesday's interviews. The moment your concept appears, everything after it is a reaction to your framing.
3. **One decision per survey.** A survey exists to move one number in the ledger ("what share of the segment reports doing this weekly?" or "which of three pains ranks first?"). Ten-minute omnibus surveys produce fatigue noise and no decisions.
4. **Screen, then weight nothing by hand.** Two screening questions up front (role, frequency of the task) so your n counts the segment, not the internet. Distribution channels: the communities from Tuesday (with the same etiquette), your niche list, or paid panels; log the channel per response, because a poll of your own followers is a different instrument than a poll of strangers.

Willingness-to-pay questions deserve special suspicion: direct "what would you pay?" answers are famously inflated. If you need pricing signal from a survey at all, use ranged anchors (Van Westendorp-style price brackets) and treat the output as *hypothesis for the pre-order test*, not as evidence. Money questions get answered honestly only by money instruments, which is the ladder's job.

## Layer 2 — The smoke-test ladder

A smoke test markets the product before the product exists and measures who steps forward. The ladder, in ascending evidence strength (and ascending cost to you in effort and reputation):

**Rung 1 — Waitlist.** A page describing the wedge with an email capture. Cheapest, weakest: an email costs seconds and zero dollars. Interpreting rates: the median waitlist page converts visitors to signups at roughly 11%, against a ~6.6% all-industry landing-page median, with top pages exceeding 20%; treat these as directional priors from vendor-published data, not gospel.[^2][^3] A waitlist's real value is less its rate than its *reply behavior*: emailing the list a Mom-Test question ("what did you try last week for this?") and reading who answers turns rung 1 into a recruiting engine for rungs above.

**Rung 2 — Fake door.** The page presents the product as available: a "Start free pilot" or "Get it" CTA, with pricing visible; the click lands on "not yet, join the list." The click-through *past a price* is the signal, and it is stronger than a waitlist signup because the clicker believed they were committing to a next step. Two cautions from the practitioner literature: run it briefly and small (the trust cost of disappointed clickers is real, and the pattern is controversial enough that Chameleon's guide catalogs the risks alongside the method), and never fake-door an audience you cannot afford to mildly annoy, which for you means running it on cold traffic, not on your Block 1 niche relationships.[^4][^5]

**Rung 3 — Pre-order / deposit.** Money moves. A $5–50 refundable deposit or a discounted pre-order converts stated interest into revealed preference; benchmarks are thin and channel-dependent, but the practitioner consensus is blunt: pre-order conversion from cold B2B traffic above 1% is noteworthy, and consumer pre-orders from paid social run low single digits.[^6] The canonical origin story remains Buffer: Joel Gascoigne's two-page test (landing page → plans-and-pricing page → email capture) validated both demand and price willingness before the product existed, and went from idea to first paying customer in seven weeks.[^7]

**Rung 4 — Paid pilot.** The apex, and for B2B agent products usually the *only* rung that settles viability: a named customer, real workload, real money (even a nominal $200–500 pilot fee), defined success criteria. You already know how to structure and gate pilots commercially from [[04-thu-project-planning-phases-and-risk|Block 1 Week 1 Thu]]; the validation-week version compresses it to: one workflow, two weeks, pre-agreed "what would make you continue at full price?" A signed paid pilot is worth more than every other instrument this week combined; three refused pilot offers with reasons attached are worth nearly as much.

Choosing your rung: start at the highest rung your assets allow. You have interviews scheduled (pilot offers belong in Movement 5), a Week 10 page (fake-doorable in an afternoon), and a niche audience (waitlist-ready). The ladder is not a sequence to climb rung by rung; it is a menu ordered by evidence price. The Forest's ranked-experiment framing gets this right: pick the cheapest experiment that can *actually kill* the assumption in question, which for viability is almost never rung 1.[^8]

## Layer 3 — The instrument: your Week 10 page, re-aimed

Week 10 built you a landing page with a CTA and AI-generated creatives ([[../week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/_week|Week 10]]); Block 2 Week 3 taught the conversion mechanics behind it. Re-aiming it as a validation instrument means three changes:

1. **One variant per hypothesis.** The page states *one* wedge for *one* customer with *one* price posture. If Thursday's copy pre-screen left you with two live framings, run them as separate variants with split traffic, not as one page hedging both.
2. **Instrument the decision points, not the vanity points.** Events: qualified visit (past 10s), CTA click, price-page view, form submit, and (rung 3+) checkout start. Traffic source tagged per visit, because 50 visitors from your niche list and 50 from cold ads are different experiments sharing a URL.
3. **Pre-register the read.** Before traffic flows, write into the ledger: expected n, the metric, the threshold, and what above/below means. The stats discipline is canonical in [[06-sat-validation-instrumentation|Block 2 Week 3 Sat]] and imports in one sentence: small-n conversion rates are intervals, not points, so state every result as a Wilson 95% interval and act only on what the *interval* clears. Eight signups on 80 visitors is not "10%"; it is roughly [5%, 18%], and if your decision threshold sits inside that interval, the honest verdict is "collect more n," which your decision rule should have anticipated by setting minimum sample sizes.

Traffic: your niche channels first (free, warm, fast, biased-known), then a small paid budget ($50–150) for the cold read if the warm read passes. Do not buy traffic to rescue a failing warm read; that is paying to postpone the verdict.

## Layer 4 — The evidence ledger

The week's convergence artifact, and Saturday's code-lab build. Structure:

**Rows: assumptions** (from Monday, verbatim, with their kill criteria). **Attached to each row: evidence atoms** from every source this week. Each atom carries:

- `source_class`: `desk` | `synthetic` | `stated` (interviews, polls) | `behavioral` (smoke-test actions) | `paid` (deposits, pilots)
- `direction`: FOR | AGAINST | NEUTRAL
- `strength` 0–5 (within-class quality: a specific past instance with consequence beats a general opinion)
- `quote/metric`, `source id`, `date`, `channel` (warm/cold)

**Class weights, fixed in advance:** paid 5×, behavioral 3×, stated 1×, desk 0.5×, synthetic 0×. The exact multipliers are less important than three properties: they are written down before evidence arrives, money outweighs talk by a large margin, and synthetic is zero by Thursday's rule. The ledger then computes, per assumption, a weighted FOR and AGAINST mass and, crucially, displays the *strongest single AGAINST atom* alongside the totals, because averages hide the one interview that should be haunting you.

**The decision rule, formalized.** Monday's paragraph becomes explicit predicates, for example: BUILD requires desirability FOR-mass ≥ threshold with ≥2 behavioral-or-paid atoms AND no unrebutted strength-5 AGAINST AND viability's paid-pilot criterion met or in progress. PIVOT names its axis in advance (if desirability passes but the wedge assumption fails, pivot the wedge, keep the customer). KILL fires when any kill criterion trips. The tool evaluates the predicates mechanically and prints the verdict with its evidence trail; you retain override authority, but overrides must be written down with reasons, which is precisely the friction that makes them rare.

Why this much apparatus for a personal decision? Because Monday named the enemy: motivated reasoning does its best work in the synthesis step, where a mood becomes a memo. The ledger replaces the mood with arithmetic you rigged in advance to be hard to fool, the same move as pre-registration, now with a CLI.

## Layer 5 — Validation signals specific to agent products

Signups measure curiosity; agent products live or die on *delegation*. When your validation reaches pilot stage (this week for some readers, Week 12+ for most), the metrics that predict a real business:

- **Usage depth over usage breadth.** One user running the agent on their real workload three times a week beats forty signups. Depth = tasks delegated per active week, share of the target workflow actually routed through the agent, and unprompted return after the first failure.
- **The failure-response signal.** Every agent fails a task eventually; watch what the pilot user does next. Reporting the failure and asking for a fix is *positive* evidence (they want it to work); silent abandonment is the churn preview. Instrument for this explicitly: an in-product "flag this output" beats a satisfaction survey.
- **Escalation acceptance.** For fine-you're-fired workflows, whether users accept the agent's escalation/review loop (per the reliability patterns of [[05-fri-reliability-engineering-for-unattended-agents|Block 3 Week 8 Fri]]) tells you if the trust boundary from Wednesday's interviews sits where they said it did.
- **Would-they-pay-again.** At pilot end, the renewal conversation at full price is the only satisfaction metric with teeth.

Log these as `behavioral`/`paid` atoms like everything else; the ledger schema does not change, which is the point of building it generically.

## Layer 6 — The controversy, final round: smoke tests vs. just shipping

The ship-school's strongest form, aimed squarely at this lesson: a fake door is a worse product test than a real door, and in 2026 the real door costs a weekend, so smoke tests are a relic of expensive-build economics; ship the ugly real thing and measure actual usage, per Andrés Max's build-and-ship-in-two-weeks playbook.[^9] The reply is not to defend fake doors as products; it is that shipping-as-validation *without pre-registered instrumentation* answers only "did they come?" and cannot answer "why not?", and its silence is unreadable, which is NYU's discovery-school point.[^10] Resolved operationally: for software this simple, rungs 2 and 4 have nearly merged; the "smoke test" for an agent product in 2026 is often a *thin real pilot* (the agent running on one workflow for one customer) rather than a painted door. What survives from the ladder is not fakery but *ordering by evidence cost* and *pre-registration of the read*. Ship as early as you like; the ledger does not care whether the behavioral atoms came from a fake door or a real one, only that you wrote down, in advance, what the numbers would have to be.

## Worked example — the follow-up agent's Friday

Continuing the running example, the week's evidence converges. Interviews (n=6 by Friday): 5 of 6 described follow-up lag with consequence, unprompted (stated, FOR desirability, strength 4); 4 of 6 located the pain in CRM/task plumbing, not drafting (stated, AGAINST current wedge, strength 4); two intros volunteered (reputation currency, FOR); zero pilot acceptances *for the drafting wedge*, one "come back if it does the HubSpot part" (stated, AGAINST viability-as-drafted, strength 4). Smoke test: the Week 10 page re-aimed at the *revised* wedge ("your calls become CRM updates, tasks, and a draft you approve"), fake-door CTA at $200/month, warm traffic n=74: 9 price-page views, 4 form submits (behavioral, FOR revised wedge; Wilson interval on 4/74 ≈ [2%, 13%], threshold was 3% minimum, verdict: interval straddles, extend n). Ledger verdict under the pre-registered rule: desirability BUILD-grade for the *plumbing* wedge; original drafting wedge KILLED by its own criterion (0 of 10 pilot acceptances); decision: PIVOT the wedge, keep customer and problem, then re-run rung 3 with the pivoted page. That is a good week: the idea that dies was killed by a rule written before the evidence, and the survivor earned its next test.

## Runnable experiment — pre-register and light the fuse (90 min + traffic time)

**Step 1 (20 min).** Choose your rung (justify the choice against your riskiest untested assumption in one written sentence). Draft the page changes or pilot offer.

**Step 2 (20 min).** Pre-register in the ledger file: metric, minimum n, threshold, Wilson-interval read rule, run window (e.g., 7 days), and what each outcome maps to under Monday's decision rule. Commit before traffic.

**Step 3 (30 min).** Instrument events and traffic-source tagging on the Week 10 page (or send the pilot offer to the two warmest interviewees with a price in it).

**Step 4 (20 min).** Open the taps: post to your niche channels; queue the paid-traffic experiment only behind a warm-read pass.

**Pass bar:** (a) pre-registration committed before the first visitor, verifiable by timestamps; (b) the chosen rung can actually kill an assumption (a waitlist "test" of a viability assumption fails this clause); (c) every event that will be read has a threshold written for it; (d) at least one money-class instrument exists somewhere in your week (a pilot offer counts, even if refused; refusals with reasons are atoms too).

## Common mistakes experts see

1. **Surveys as discovery.** Polls quantify known patterns; they cannot find unknown ones. Discovery happened Wednesday; today is measurement.
2. **The leading poll.** "How excited would you be about an AI that saves you hours?" produces enthusiasm data about the question. Behavioral anchors or nothing.[^1]
3. **Point-estimate theater.** Announcing "12% conversion!" on n=50. State the interval; act on the interval. Canonical treatment in [[06-sat-validation-instrumentation|Block 2 Week 3 Sat]].
4. **Fake-dooring your warm network.** Cold traffic can be mildly annoyed; the niche relationships Block 1 built cannot. Choose traffic to match the rung's trust cost.[^4]
5. **Moving the threshold mid-read.** Four signups against a threshold of five becomes "well, four is basically five." The pre-registration commit exists to make this visible as the fraud-against-self it is.
6. **Waitlist numerology.** Comparing your rate against benchmark medians from different traffic mixes and CTAs. Benchmarks set priors; your pre-registered threshold, set against *your* channel, decides.[^2]
7. **Counting signups for an agent product.** Breadth metrics flatter; delegation depth decides. If your pilot dashboard has signups on top, redesign the dashboard.
8. **Skipping the refusal interviews.** A refused pre-order or pilot, plus one "what would have made this a yes?" question, is among the highest-density atoms available and costs one email.

## Open questions — what's not settled

**1. Are fake doors becoming untenable?** The trust economics of the painted door were always marginal, and two 2026 trends squeeze them further: buyers drowning in AI-generated launch noise have hair-trigger skepticism about vaporware, and the collapse of build costs weakens the method's founding excuse (that building first was too expensive). The practitioner literature already hedges hard on ethics and brand risk.[^4] The unresolved question is whether the fake door survives as a legitimate instrument at all, or shrinks to the narrow niche where the thin-real-pilot substitute is genuinely infeasible (hardware, regulated products, marketplaces needing simultaneous sides). This course's position, weakly held: prefer the thin real pilot wherever it costs under two weeks; use painted doors on cold traffic only, briefly, with a same-week "here's where we actually are" follow-up to everyone who clicked.

**2. Fixed pre-registration vs. adaptive experimentation.** The pre-registered fixed-n read this lesson teaches is the founder-grade version of a frequentist trial; the sophisticated alternative is sequential/adaptive testing (Bayesian updating, bandit allocation across variants) which reaches decisions faster on the same traffic and never "peeks" illegally because its math prices continuous looking. The reason this course still teaches fixed reads is not statistical superiority; it is that adaptive methods hand the founder more knobs mid-flight, and every knob is a rationalization surface. At what scale of traffic and organizational maturity the switch pays is unsettled; if you reach thousands of visitors per variant, learn the adaptive tooling and hold the pre-registration discipline around *what counts as a win*.

**3. Do class weights transfer across products?** Paid 5×, behavioral 3×, stated 1× encodes a B2B-agent-product theory of evidence. For consumer products with impulse dynamics, stated intent is even weaker; for enterprise deals with long committee cycles, a strength-5 stated atom from an economic buyer ("budget exists, Q4, I sign") may honestly outweigh a hundred behavioral clicks. The right weights are a function of sales motion, and no published calibration exists. Log your own: after three validated-then-launched ideas, your ledgers become a private dataset on which evidence classes predicted *your* market's revenue, which is a moat nobody's research agent can retrieve.

## Reflection questions

1. Your class weights put paid at 5× and stated at 1×. For *your* product and price point, is that ratio too aggressive or too timid? What evidence pattern would make you revise it, and why is revising it *after* seeing data forbidden?
2. Which rung frightens you more: the fake door (trust cost) or the pilot offer (rejection cost)? What does that asymmetry predict about which evidence you will unconsciously avoid collecting?
3. Construct a scenario where the warm read passes and the cold read fails. Three explanations, and the cheapest instrument that distinguishes them.
4. The worked example's pivot kept the customer and problem, changed the wedge. Under what evidence pattern would the correct pivot instead keep the wedge and change the customer? Does your decision rule distinguish these, or did you leave "pivot" unspecified?
5. For your idea, what is the thin-real-pilot version of rung 2 that makes the fake-door debate moot? What does it cost in days, and what does that number do to your smoke-test plan?
6. If your ledger returns KILL on Sunday, what specifically do you salvage: the customer relationships, the desk dossier, the instrument templates, the niche? Rank them, and notice what the ranking says about where validation value actually accrues.

## My take (reviewer lens)

**Michael Seibel** would enjoy watching the ladder collapse in Layer 6, because the collapse concedes his point: for software this cheap, the best smoke test is the product, and he would add that founders who love instrumentation sometimes ship the measurement and forget to ship the thing; his tiebreak is always "would a customer be mad if you took it away?", a question no fake door can answer. The lesson holds one line against him: pre-registration costs twenty minutes and is the only thing standing between a solo founder and a self-graded exam. **Hamel Husain** would approve the ledger as an eval harness for a business decision and then flag the weakest joint: the 0–5 strength scores are un-calibrated human judgments feeding a precise-looking arithmetic, classic garbage-in-formula-out risk; his fix would be an anchored rubric per strength level (this lesson gestures at one; Saturday's tool ships it as a config file you must edit) and a periodic blind re-score of a sample, the same inter-annotator hygiene he prescribed Wednesday. **Jerry Liu** would push on the ledger's data model rather than its philosophy: atoms-with-provenance across heterogeneous sources, weighted aggregation, and an auditable verdict is *exactly* the retrieval-and-synthesis shape his stack solves for documents, and he would ask why the tool stops at your own idea, since the same ledger pointed at a client's product decisions is a sellable artifact. That observation is Week 12's seed, and it is correct.

## Further reading

**Must-read**

- Pew Research Center, "Writing Survey Questions" (methods guide).[^1]
- Joel Gascoigne, "Idea to Paying Customers in 7 Weeks: How We Did It" (Buffer, 2011). The original two-page pricing smoke test, still the cleanest specimen.[^7]

**Recommended**

- The Forest, "10 Startup Validation Experiments — Ranked by Cost, Speed, and Signal Strength."[^8]
- Chameleon, "Fake Door Testing: How it Works, Benefits & Risks," read alongside Kromatic's Real Startup Book entry for the mechanics.[^4][^5]
- [[06-sat-validation-instrumentation|Block 2 Week 3 Sat]] — re-read the Wilson-interval worked cases before Saturday's sprint.

**Optional**

- Waitlister, "7 Waitlist & Product Launch Statistics (Backed by Data)," with Flowjam's examples as a cross-check; vendor data, use as priors only.[^2][^3]
- User Intuition, "Landing Page Tests: Measuring Demand Before Building."[^6]

## Citations

[^1]: Pew Research Center, "Writing Survey Questions" (methods). https://www.pewresearch.org/writing-survey-questions/ — question-wording and order effects, incl. the classic forbid/not-allow gap; behavioral-anchoring practice.

[^2]: Waitlister, "7 Waitlist & Product Launch Statistics (Backed by Data)." https://waitlister.me/growth-hub/blog/waitlist-and-launch-statistics — median waitlist page ~11% visitor→signup vs ~6.6% all-industry landing median; top pages >20%. Vendor-published aggregate; treated as a directional prior (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Flowjam, "Waitlist Landing Page Examples: 7 That Convert at 20% (2026)." https://www.flowjam.com/blog/waitlist-landing-page-examples-10-high-converting-pre-launch-designs-how-to-build-yours — corroborates the 2%-typical / 20%-excellent spread from a second vendor (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Chameleon, "Fake Door Testing - How it Works, Benefits & Risks." https://www.chameleon.io/blog/fake-door-testing — mechanics plus the trust-cost and ethics cautions (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Kromatic, "Fake Door Test: Validate Demand Before Building," *The Real Startup Book*. https://kromatic.com/real-startup-book/4-evaluative-market-experiment/fake-door-smoke-test/ — canonical experiment write-up; corroborates [^4] (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^6]: User Intuition, "Landing Page Tests: Measuring Demand Before Building." https://www.userintuition.ai/reference-guides/landing-page-tests-measuring-demand-before-building/ — B2B SaaS email-signup 8–15% on paid search, pre-order from cold B2B traffic >1% noteworthy, consumer pre-orders 1–3% from paid social; single-source benchmarks, used as priors with that caveat stated (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^7]: Joel Gascoigne, "Idea to Paying Customers in 7 Weeks: How We Did It," Buffer blog, 2011. https://buffer.com/resources/idea-to-paying-customers-in-7-weeks-how-we-did-it/ — the two-page (landing + pricing) validation sequence.

[^8]: The Forest / LaunchFolio, "Ep. 2: 10 Startup Validation Experiments — Ranked by Cost, Speed, and Signal Strength." https://www.theforest.ai/blog/ep-2-10-startup-validation-experiments-ranked-by-cost-speed-and-signal-strength — experiment selection by cost/speed/signal (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^9]: Andrés Max, "How to Validate a Startup Idea in 2026 (The Old Playbook Is Dead)." https://andresmax.com/validate-startup-idea/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^10]: NYU Entrepreneurship blog, "Shipping Is Not a Substitute for Asking," May 8, 2026. https://entrepreneur.nyu.edu/blog/2026/05/08/shipping-is-not-a-substitute-for-asking/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
