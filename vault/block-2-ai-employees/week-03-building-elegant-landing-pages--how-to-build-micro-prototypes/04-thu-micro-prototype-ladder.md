---
type: lesson
block: block-2-ai-employees
week: week-03
day_of_cycle: 4
day_name: thu
session_slug: how-to-build-micro-prototypes
date_due: 2026-06-04
tags: [pretotyping, micro-prototype, smoke-test, fake-door, concierge, wizard-of-oz, validation, savoia, torres, cagan, fitzpatrick, binomial-ci]
sources:
  - savoia-pretotype-it-10th-ed-2022
  - pretotyping-org-2024
  - torres-opportunity-solution-tree-producttalk-2023
  - torres-assumption-testing-course-2024
  - torres-ai-product-discovery-2025
  - cagan-svpg-product-validation-2024
  - cagan-svpg-biggest-risk-2024
  - fitzpatrick-mom-test-revised-2024
  - graham-do-things-that-dont-scale-2013
  - dropbox-mvp-explainer-video-2007
  - airbnb-cereal-yc-2008
  - zappos-wizard-of-oz-swinmurn
  - buffer-two-page-mvp-gascoigne-2010
  - superhuman-manual-onboarding-vohra
  - cppa-dark-pattern-advisory-2024
  - chameleon-fake-door-ethics-2024
  - learningloop-fake-door-testing-2024
  - measuringu-adjusted-wald-calculator
  - wikipedia-binomial-proportion-ci
  - lennys-superhuman-rahul-vohra-podcast
last_verified: 2026-04-17
word_count_target: 6000
---

# The micro-prototype ladder — pretotyping, smoke tests, fake-door, concierge, and which rung to start on

## Why this matters

You will ship a lot of AI prototypes in 2026. The tool stack is now cheap enough — Claude Code as orchestrator, v0/Lovable/Bolt for UI, n8n for glue, Vercel for hosting, PostHog for instrumentation — that a week's worth of hypothesis can become a deployed, trackable surface in four to eight hours. Tuesday and Wednesday taught you how to build one cleanly; Friday teaches you the pipeline end-to-end. Today's lesson is the question that sits upstream of all of that and silently decides whether any of the work matters: **which experiment, at which rung of the validation ladder, for which hypothesis?**

The capability delta you will have after internalizing this lesson, which a sharp AI-native generalist does not already have, is this: you will stop defaulting to "ship an MVP and see." You will be able to place any AI-product hypothesis on the six-rung ladder from Alberto Savoia's pretotyping framework[^1], name the rung it currently sits at, name the *next* cheaper-than-MVP experiment that would materially de-risk it, write a falsifiable hypothesis with a pre-committed success threshold and sample-size math, and — this is the one most operators miss — tell the difference between a "go" signal, a "no-go" signal, and an "ambiguous signal that demands a second round," without post-hoc rationalizing whichever direction you were already leaning. By the end you will also have a defensible position on two 2026-live controversies: whether fake-door testing is still ethical in a regulatory climate where the California Privacy Protection Agency is actively enforcing against dark-pattern deception[^2], and whether pretotyping's "demand validation" is real user validation or Marty Cagan's "not enough."[^3]

This is the rung-selection muscle. It is what separates operators who ship five 4-hour prototypes in a quarter and kill four of them decisively from operators who ship one 6-week MVP per quarter and cannot tell you whether it worked.

## Prerequisites

- You have a candidate product hypothesis — from your Block 1 Week 2 niche work or a fresh opportunity. If you do not have a specific one, pick an AI-workflow tool you've been tempted to build for your own industry; that will do.
- You are willing to run an experiment that costs <$200 and <8 hours *this week*, not "eventually." The ladder is worthless if you only read it.

## Layer 1 — The ladder, rung by rung

The framework here is Alberto Savoia's *pretotyping*, developed at Google and formalized in *Pretotype It* (2014, 10th Anniversary Edition 2022)[^1][^4]. Savoia's central bet, which has been absorbed by most modern product-discovery schools without attribution, is that *most ideas fail not because they were built badly but because they were the wrong ideas to build in the first place*. His response is to separate two questions that operators routinely collapse: **"can we build it?"** (the prototype question) from **"should we build it, and will anyone actually hire it?"** (the pretotype question). Pretotyping answers the second one before any prototyping begins.

Six rungs, cheapest to most expensive, each with a distinct operational signature. Know the mechanism of each rung before you start picking.

### Rung 1 — Pretotype on paper (the "skin in the game" test)

The cheapest rung. Before any artifact, before any landing page, the operator commits a specific week and a specific dollar amount of their own resources to the idea in a written pre-mortem. Savoia's test[^4]: would *you*, the would-be builder, commit a week of unpaid time and $X of your own money — not a VC's, not an employer's — to find out? If not, the idea has already failed the first rung. This sounds like journal-filler; it kills more ideas than any other rung, because the moment you write the number down the idea that seemed exciting yesterday reveals itself as an idea you would not personally fund.

Operational output: a one-paragraph statement of what you'd commit and why. If you cannot finish that paragraph, you skip building anything.

### Rung 2 — Smoke-test landing page (no product)

A single landing page that describes a product that does not exist, with a single conversion action (email signup, waitlist join, "notify me when it launches"). Drive ~50–500 visitors from a specific traffic source. Measure opt-in rate. Known canonically as the *Dropbox MVP*: Drew Houston's 2007 four-minute demo video, posted to Hacker News and Digg, pushed the beta waitlist from ~5,000 to 75,000 overnight.[^5] The product showed in the video — seamless multi-device sync — did not yet exist at scale; the video tested whether people would hire a product with that promise. The video was, in Savoia's vocabulary, a *Youtubeotype*: an artifact that surfaces "I want that" intensity before engineering begins.

Joel Gascoigne's Buffer took the same rung one step further in 2010 with a two-page refinement[^6]: page one described the product; page two showed pricing plans *before* the email capture. The second page tested not just demand but price-point resonance. Within four days of tweeting the link, Buffer had its first paying customer — because the pricing-click was itself the signal.

Operational output: signup rate, CTA-click-through rate, time-on-page, and — if Buffer-style pricing is on the page — pricing-tier distribution.

### Rung 3 — Fake-door / painted-door

The rung that causes the most 2026 debate. The operator adds a button, menu item, or feature card inside an *existing* product (or a mocked-up dashboard) that looks like it leads to a new feature but actually leads to a survey, a "coming soon" explanation, or a waitlist. Clicks measure *latent demand among existing users who already trust the brand*, which a cold-traffic smoke test cannot isolate.

The canonical case: Gmail's Priority Inbox in 2010, PM'd by Todd Jackson on the Gmail team[^7], reportedly used painted-door-style internal Labs probes before the feature shipped — though the exact mechanics were never fully disclosed. More operationally explicit is the ongoing GoodUI / Chameleon / ProdPad pattern library[^8][^9], which documents fake-door tests as a standard conversion-research discipline. *Critical 2026 constraint:* the California Privacy Protection Agency's Enforcement Advisory 2024-02 (September 4 2024) specifically names dark-pattern design as subject to civil penalties of up to $2,500 per violation and $7,500 for willful violations[^2]. Fake-door tests that do not immediately disclose ("thanks for your interest — this feature is in research, we'll tell you if we ship it") risk landing inside that enforcement surface. We come back to this in the controversy section.

Operational output: click-through rate on the nonfunctional element, delta vs. sibling features, follow-up survey response rate.

### Rung 4 — Concierge / Wizard of Oz

The operator delivers the promised outcome *manually* — behind a UI that makes it look automated — for a small number of real customers paying real money. The product is fully real to the user; what is fake is the automation. Nick Swinmurn's Zappos (1999) is the founding story: he photographed shoes at San Francisco mall stores, posted them on a website, and when an order came in, went back to the store, bought the pair, and shipped it personally[^10]. The customer got shoes; Nick got signal on whether online shoe commerce had a market, without warehouse capital. Later-stage concierge is Rahul Vohra's Superhuman, which ran *20 full-time humans* onboarding every new paying user with a 2-hour 1:1 session for roughly five years[^11][^12] — the signal being that the product's differentiated moment was the onboarded workflow, not the email client alone.

In 2026 for AI products, the concierge rung has a specific shape: *the "AI employee" is you, operating Claude Code or a structured prompt workflow, for real paying customers*. You take the client's input, run the workflow by hand in Claude.ai or via Claude Code, return the output, and measure satisfaction, willingness to pay, and what automatable patterns emerge. After N successful runs, the patterns that stabilized get coded.

Operational output: paid-customer count, NPS or satisfaction score, qualitative "jobs" transcripts, and a list of automatable sub-steps with confidence scores.

### Rung 5 — Painted-door feature inside an existing product

A partial-build variant of fake-door: the feature is *partially* real, but the riskiest path is stubbed. Useful when you already have a live product and an existing user base. The classic pattern is Airbnb's 2009 "we'll come take pro photos of your listing" offer[^13][^14]: Brian Chesky and Joe Gebbia literally rented a camera and went door-to-door in New York, photographing hosts' apartments. The "feature" (professional photography) was painted into the host dashboard; the backend was the two founders on a subway. Bookings on upgraded-photo listings were 2–3× the rest, which justified building the real feature later.

Operational output: same as concierge plus feature-engagement retention.

### Rung 6 — MVP

The rung most operators default to first. A real, shippable, minimum-feature product that genuinely delivers the core job. By the time you get here, the earlier rungs should have killed most of the bad hypotheses. Shipping an MVP as rung-one is the expensive path Paul Graham's "Do Things That Don't Scale" (2013)[^15] was written to prevent — and the pattern behind most of the failed hardware AI products Block 0 Week 3 covered (Humane Pin, Rabbit R1).

Operational output: retention curves, paid conversion, cohort behavior — the full product-analytics surface.

## Layer 2 — Which rung to start on

The common mistake is to start at the rung the operator is emotionally comfortable with. Engineers start at rung 6 because building is fun; marketers start at rung 2 because copy is fun; founders with consulting DNA start at rung 4 because that is literally how they are already working. None of those defaults is correct. The right rung is the one that *most cheaply disconfirms the riskiest current assumption*.

Teresa Torres's framing from her 2024 Assumption Testing course and 2025 AI-product-discovery work[^16][^17][^18] is the operational version: *break the idea into discrete assumptions (desirability, feasibility, viability, usability, ethical, trust), rank them by the risk they would kill the idea if false, then pick the smallest experiment that could disprove the top-ranked one*. Torres's rule: test the riskiest assumption, not the easiest one. The ladder is how the experiment instantiates; Torres's assumption ranking is how you pick the rung.

Concrete examples, mapped across three domains:

- **Enterprise AI SDR tool.** Riskiest assumption is almost never "can we build a tool that writes emails" (the capability exists, the question is calibration). It's usually "will sales leaders let an AI touch their CRM and send under a rep's signature?" That's a trust / viability question that a rung-2 smoke test cannot answer. The right rung is 3 or 4: a painted-door offer inside a Slack community of RevOps leaders, or a concierge where you personally ghost-write 50 emails for 5 named reps and measure reply-rate delta. Starting at rung 6 here burns six months.
- **Consumer AI-mediated journaling app.** Riskiest assumption is desirability: will someone consistently journal with an AI companion after novelty fades? That's a retention question, which no rung below 4 can truly answer. Concierge here looks like a Telegram / iMessage bot that *is* you behind a "journaling AI" mask for 20 users over 6 weeks. You measure week-4 and week-6 retention, not signup rate.
- **SaaS micro-tool for accountants (month-end variance reconciliation).** Riskiest assumption is probably viability: will they pay $X/month when their firm's existing spreadsheet, however painful, is free at the margin? A rung-2 Buffer-style two-page (description → pricing → signup) answers this in 48 hours without any product work. Rung 3 is also viable if you have access to an accounting-tools Slack where a "coming soon: automated variance explainer" card can be posted.

The cross-domain pattern: **desirability → rungs 2, 3**; **viability → rungs 2 (with pricing), 3**; **trust / ethical / social acceptability → rung 4**; **retention / habit formation → rung 4, 5**; **scale-economics and unit-cost → rung 6 only**. If an operator's answer to "which rung?" is rung 6, you should be suspicious that they haven't yet named the riskiest assumption.

## Layer 3 — Three operator case studies, one per rung

Three public cases, all with disclosed numbers, each on a different rung, each from a different field. Read them as templates for the shape of what "a rung well-climbed" looks like.

### Rung 2, SaaS — Buffer's two-page smoke test (2010)

Joel Gascoigne wrote up the Buffer validation pattern in a now-widely-cited blog post[^6][^19]. The structure: page one described what Buffer would do (schedule tweets); a single "plans and pricing" CTA led to page two, which listed three price tiers; clicking any plan went to page three, an email capture with "we're not ready yet, leave your email." The instrumentation was the page-flow itself. Within four days of posting the link on Twitter, Gascoigne had a first paying customer (he emailed back, took the payment manually via a Stripe-predecessor flow, and delivered the first Buffer feature hand-operated — notice the quiet rung-3-to-4 promotion *after* rung-2 signal). Buffer reached $2.5M ARR within a few years and remains a cited operator case for lean validation. **Rung signature:** pricing-tier clicks were the actionable signal; email captures without pricing-tier clicks were treated as noise. The layered CTA is what made the test diagnostic rather than merely directional.

### Rung 3, Enterprise — Gmail Priority Inbox (2010) and the painted-door lineage

The Gmail Priority Inbox case is frequently cited as a painted-door story, though the exact internal mechanics were never fully published by Todd Jackson or the Gmail team[^7][^20]. What is documented is that Gmail Labs was the painted-door *surface* for experimental features through 2009–2010: opt-in toggles that revealed whether users would even try a new inbox behavior before full engineering investment. The broader pattern — put a clickable path to a not-yet-real feature in front of existing users who already trust the brand — is the lineage that A/B Tasty, Optimizely, Contentful, and Amplitude all document as of 2024–2025[^21][^22][^23][^24]. **Rung signature:** existing-user click-through is the metric, and *the immediate post-click experience* is what determines whether the test is diagnostic or merely deceptive. The modern operator move — "thanks for your interest, this feature is being researched, here's a waitlist and a 3-question survey" — preserves the signal and stays inside ethics norms.

### Rung 4, Consumer (with enterprise overtones) — Superhuman's manual onboarding (2017–2022)

Rahul Vohra's published account of Superhuman on Lenny Rachitsky's podcast and First Round Review[^11][^12][^25] is unusually specific about the numbers. At peak, Superhuman had *dozens of full-time Onboarding Specialists*; each 1:1 session ran approximately 2 hours; Vohra himself personally onboarded hundreds of customers before hiring the first specialist; cumulatively the team onboarded "tens of thousands of paying customers" via manual 1:1. The cost looks absurd until you notice what it was testing: not "do people want a faster email client" (rung 2 would have answered that) but "is the *onboarded workflow* the product?" The concierge signal was that Superhuman's retention, NPS, and word-of-mouth collapsed without onboarding and stayed strong with it. The product team only started automating the onboarding after they had ~5 years of 1:1 tape to pattern-match against. **Rung signature:** the "manual" step *was* the product differentiator, which no cheaper rung could have revealed; automating too early would have shipped a worse product.

For a 2026 AI-product reader, the takeaway is sharper: if your AI product's differentiator is *the orchestration* (how Claude Code sequences six steps), concierge-rung validation where *you* operate the orchestration by hand for 10–20 real customers is the only way to learn which sequences stabilize into features and which were artifacts of you having intuition that Claude doesn't.

## Sample-size math — what you actually infer from N=50

This is the single most common failure mode at rungs 2 and 3: operators look at "6/50 visitors signed up — 12% conversion!" and either ship or kill based on it. Neither is warranted. A conversion of 6/50 has a *95% Wilson confidence interval* of roughly **5.6% to 23.8%** — meaning the true conversion rate could plausibly be as low as ~6% or as high as ~24%, an 18-percentage-point span that straddles nearly every threshold you might set. A single number at N=50 is a point estimate; the interval is the signal.

The math you should carry in your head (approximate Wilson score intervals, 95%, binomial proportion CI[^26][^27]):

| Conversions / N | Point rate | 95% CI (approx Wilson) | Operator read |
|---|---|---|---|
| 6 / 50 | 12% | ~5.6% – 24.2% | Ambiguous — run more |
| 3 / 50 | 6% | ~2.1% – 16.2% | Likely weak but cannot rule out 15% true rate |
| 12 / 100 | 12% | ~7.0% – 19.8% | Narrower but still ambiguous for A/B comparison |
| 60 / 500 | 12% | ~9.4% – 15.1% | Actionable — conversion in roughly this band |
| 10 / 50 | 20% | ~11.2% – 32.9% | Strong directional; likely level-up, not yet ship |
| 1 / 50 | 2% | ~0.4% – 10.5% | Almost certainly dead — but "almost" is doing work |

A few load-bearing implications:

**Sample-size math box — the go / no-go / ambiguous cuts at N=50.** Take a 10% conversion threshold as your "level up" bar and hold every read to the Wilson 95% interval. At N=50: observing **≥10/50 (≥20% observed)** puts the lower bound at ~11.2% — the whole interval clears 10%, so level up. Observing **≤1/50 (≤2% observed)** puts the upper bound at ~10.5% — the interval sits at or below the bar, so kill. **Everything from 2/50 to 9/50 straddles 10%** — for instance 2/50 → [1.1%, 13.5%] and 8/50 → [8.3%, 28.5%] — and must be read as "run to N=200 before deciding," never talked into a verdict. Watch the trap: 2/50 *looks* like a kill at 4% observed, but its Wilson upper bound is **13.5%**, which does not exclude a true 10% rate — 2/50 is ambiguous, not dead. The kill line at N=50 genuinely sits at ≤1/50 and the level-up line at ≥10/50; the band between them is wide precisely because 50 visitors carry little information. This is why operator rule 1 is: **pre-commit the threshold in writing before traffic starts, not after** — otherwise that wide ambiguous band gets retrospectively read as whichever direction you already wanted.

**Second load-bearing implication:** the adjusted Wald / Wilson interval is the right tool for N<150 landing-page tests. The standard Wald ("conversion ± 1.96 × √(p(1-p)/n)") gives nonsense bounds at small N — for 1/50 it produces a lower bound below zero. MeasuringU's adjusted-Wald calculator[^26] is the operator reference. For very small N (N<30, rung-4 concierge), use exact Clopper-Pearson or just accept you have qualitative data, not quantitative.

**Third:** you cannot meaningfully A/B test at N=50. If your hypothesis requires comparing two conversion rates (two headlines, two price points), you need roughly 5× the sample size to detect a 5-point lift at 80% power — often N≥300 per arm. This is why rung 2's job is "is there *any* pull?" not "which of two CTAs wins?" That second question belongs at rung 5 or 6 with real traffic.

**Fourth and most operationally useful:** the ambiguous zone is where real-operator discipline shows up. Operators who cannot tell their own bias from the signal will read 5/50 as "we're on something" and run a second rung-2 test with a more favorable traffic source until they get a "hit." The discipline is to pre-commit the threshold *and* the N-budget ("we'll run to 200 visitors; if we're still ambiguous, we demote to concierge or kill"), then execute.

## Runnable experiment — place and build your own rung

Four phases, designed to end with a deployed experiment by end of session.

**Phase 1 — Map the riskiest assumption and pick the rung (30 min).** Take one real product idea from your Block 1 Week 2 niche work. Open Claude Code and paste the hypothesis plus this instruction: *"Break this hypothesis into its discrete assumptions across Torres's categories: desirability, viability, feasibility, usability, ethical/trust. For each, score it 1–5 on (a) how risky it is if wrong and (b) how much evidence we already have. Output a ranked list with the top-3 riskiest-and-least-evidenced, and for each, name which rung of the pretotyping ladder (paper / smoke test / fake-door / concierge / painted-door-in-existing / MVP) would most cheaply disconfirm it, and why not the adjacent rungs."* Read the output critically. If Claude Code proposes rung 6 for the top risk, push back: "Name the cheapest rung that would still be diagnostic, even if less certain." You are looking for honest rung-selection, not "everything is an MVP."

**Phase 2 — Design the falsifiable experiment (30 min).** Ask Claude Code: *"Given this chosen rung and this assumption, design the cheapest valid experiment under 8 hours and $200 total. Specify: (a) the hypothesis in 'if we show X to audience Y, they will do Z at rate ≥ W%' form, (b) the deliverable (landing page / fake-door card / concierge workflow), (c) the traffic source and the exact N we will run to before deciding, (d) the pre-committed success threshold, kill threshold, and ambiguous-zone range using Wilson 95% CI math at the planned N, (e) the decision each outcome triggers — level up / iterate / kill, (f) the sunset date."* The output is your experiment spec. Write it down; timestamp it. This is the one document that must exist before you touch any tool.

**Phase 3 — Build it (2–4 hours).** Use the tool you chose on Tuesday. For rung 2: v0 or Lovable for the landing page, the pricing-tier-first Buffer pattern if viability is the riskiest question. For rung 3: build the fake-door card inside an existing Notion / Slack / landing surface, with an immediate "this feature is in research, here's a 3-question survey" post-click experience — the ethical disclosure that keeps you outside the CCPA-enforcement zone. For rung 4: skip the UI; set up a Telegram/email endpoint, write your Claude Code orchestration playbook, tell 5 target users you'll do the work for them personally at $X.

**Phase 4 — Write the 300-word go/no-go/ambiguous memo (30 min).** Before any traffic: *write the memo you would write at each of three outcomes.* "If we land at N=200 and we see ≥ X conversions, we will level up to rung Y by date Z. If we see ≤ A conversions, we kill. If we land in the ambiguous band (B to C conversions), the next decision is [second round? demote to concierge? interview 5 converters?]." Writing all three memos in advance is the single most durable discipline in the lesson. It removes the post-hoc rationalization that kills validation as a practice.

## Problem set

**Problem 1 — Place three public products on the ladder with disclosed numbers.** Take Dropbox's demo video (2007, beta list ~5,000 → 75,000 overnight after Hacker News posting)[^5], Superhuman's manual onboarding (2–hour 1:1s, tens of thousands of customers onboarded this way over ~5 years)[^11][^12], and one enterprise fake-door of your choosing (the 2024–2025 pattern libraries at GoodUI, Chameleon, or ProdPad have dozens of documented examples[^8][^9][^21]). For each: name the rung, the riskiest assumption it tested, the specific signal that justified level-up, and what each product shipped at the *next* rung.

**Problem 2 — Take a position on the fake-door 2026 ethics question.** Defend or refute, in ≤400 words: *"Fake-door testing that does not immediately disclose its test nature is an unacceptable dark pattern in 2026 and is legally exposed under the California Privacy Protection Agency's Enforcement Advisory 2024-02."*[^2] Your answer must cite the CPPA advisory's actual enforcement criteria and at least one of Chameleon, GoodUI, or Optimizely's published ethics guidance[^8][^9][^22], and must stake one of three positions: (a) fake-door is dead, replace with rung 2 or 4; (b) fake-door is fine if immediately disclosed post-click; (c) fake-door is fine undisclosed if no data is collected on the clicker. Name named operators on whichever side you land.

**Problem 3 — Write the falsifiable hypothesis for your own product with sample-size math.** In the format: *"If we show [artifact] to [audience sourced from channel] and run to N=[number], then [action] at rate ≥ [threshold]% will mean [decision]. At N=[number], the 95% Wilson CI for our threshold rate is [low]% to [high]%, so we will treat observed rates in [range] as ambiguous and run a second round to N=[larger] before deciding."* Include the channel, the exact N-budget, the decision each outcome triggers, and a kill date.

**Problem 4 — Design a concierge workflow where Claude Code operates the manual step.** Pick a rung-4 concierge version of your product where the "AI" is actually you driving Claude Code by hand for the first 10 customers. Specify: the client-facing promise, the hidden orchestration (what Claude Code does, what you do, what the client sees), the success metric per customer, and the automation criterion — *after how many successful runs, and what pattern-stability signal, does each sub-step get promoted from manual-with-Claude to fully-in-the-product?* Write it at the granularity of "step 3 — variance classifier — automate after 20 runs where human reclassification rate drops below 10%."

**Problem 5 — Identify your current skip-a-rung bias and commit to one demotion.** Pick a project you are currently building or thinking of building. Name the rung it is currently sitting at. Name the rung below it that a Torres-style assumption ranking would point to. Commit, in writing with a date, to running the cheaper rung *first* — even if it feels like going backwards. Most operators skip rungs upward toward MVP because building feels like progress; the demotion is the operator discipline.

## Common failure modes at scale

**1. "We validated it" at N=50 with no pre-committed threshold.** This is the single most common failure. An operator runs a smoke test, gets 7 signups out of 50, declares validation, ships, and six months later cannot explain why retention cratered. The fix is the pre-committed Wilson-CI threshold memo from Phase 4.

**2. Traffic-source contamination.** Smoke tests driven by friends-and-family, the operator's Twitter following, or a niche community the operator is already well-known in produce signal that does not generalize. A 20% conversion from 200 warm-network visitors is a different animal from 20% at cold paid-search traffic. Named operators who have published this failure mode include Pieter Levels (warm-network inflates early metrics) and the broader YC-library "Do Things That Don't Scale" lineage[^15]. The fix is to either test on the cold-traffic source you'll actually use at scale, or to explicitly name the warm source as a *ceiling* ("this rate is the best case").

**3. Fake-door without post-click disclosure, in a 2026 enforcement climate.** The CPPA's 2024-02 advisory makes the legal cost real, but the more durable cost is brand: users who feel tricked by a fake-door feature tell other users, and the trust cost compounds across all future rollouts. The fix is the "immediate post-click disclosure + survey" pattern. Chameleon's 2024 fake-door guide, the ProdPad glossary, and Amplitude's pattern docs all converge on this[^8][^9][^23].

**4. Concierge that never gets automated (the "consulting trap").** Rung 4 is a test, not a product. Operators who find the concierge profitable often stay there and miss that the *product* thesis was scale. Superhuman's team spent years at concierge, but they were explicitly *watching* for the patterns that would automate; most consulting-flavored AI tools in 2024–2025 stayed at concierge because the founder enjoyed the client work and never forced the automation question. The fix is a *pre-committed automation criterion per sub-step* — "we automate variance classification after 20 runs where the human reclassification rate drops below 10%." If you don't have that criterion in writing, you're probably running a consultancy.

**5. Skipping to rung 6 because "AI makes MVPs cheap."** The Block 0 Week 3 lesson's Humane Pin and Rabbit R1 case studies are the cautionary tale. 2026 AI tools do make MVPs cheaper, but "cheap to build" is not the same as "cheap to learn from if the hypothesis is wrong." An MVP that takes 4 hours and produces no validation signal is still more expensive than a rung-2 smoke test that takes 4 hours and tells you the demand isn't there.

**6. Confusing demand signal with user signal.** A smoke-test signup is a *demand* signal: someone was interested enough to convert. It is not yet *user* signal: that they would retain, pay, or derive ongoing value. This is Marty Cagan's critique of pretotyping in its extreme form[^3][^28] — we come back to it immediately.

## Open questions — live controversies in 2026

### Controversy 1 — Is fake-door testing ethical in 2026?

**Position A (the "it's fine with disclosure" camp):** Jakub Linowski's GoodUI pattern library[^8], Chameleon's fake-door guide[^9], ProdPad's glossary, Amplitude's experimentation docs[^23], and most product-ops teams hold that fake-door testing remains the single most efficient way to surface latent demand inside an existing user base, and that the ethical bar is satisfied by (a) no personal-data capture beyond what the user would have provided anyway, (b) immediate post-click transparency, and (c) honoring any follow-up commitments (survey, waitlist, notification). The conversion-research community treats it as a standard discipline and argues that the alternative — building features users don't click — is ethically worse because it burns team time on non-problems.

**Position B (the "dark pattern" camp):** The CPPA's Enforcement Advisory 2024-02 (September 2024)[^2], the EU Digital Services Act and Digital Markets Act enforcement trajectory, and a growing strand of 2024–2025 dark-pattern legal commentary argue that *any* UI element designed to produce user behavior the user would not have chosen under transparent conditions is a deceptive practice. Under this reading, a fake-door click is data exfiltrated from a misled user even if no PII is captured, and the downstream "trust erosion" cost is real. Teresa Torres[^16][^17] and the Product Talk school do not formally oppose fake-door but emphasize that *assumption testing* is better served by direct-interview and Wizard-of-Oz methods where the user is a willing participant, which sidesteps the ethics question entirely.

**My position:** fake-door testing is fine if two conditions hold: (i) the post-click experience immediately discloses the test, offers the user something real in return (a waitlist slot, a survey, the promise of early access), and collects no data the user wouldn't have given a plain "interested?" survey; (ii) the operator is prepared to defend the test publicly if asked by a user or a regulator. If either condition is shaky, demote to rung 2 (smoke test, transparent) or rung 4 (concierge, fully transparent and paying). The "undisclosed fake-door" variant is, in 2026, both legally exposed and strategically obsolete — rung 4 is cheaper to run in the Claude Code era than it was in 2014, and produces better signal.

### Controversy 2 — Is pretotyping "demand validation" real user validation, per Marty Cagan?

**Position A (Savoia, the pretotyping camp):** Savoia's canonical argument[^1][^4] is that *if no one will even click "I want that," there is nothing to validate further*. Pretotyping's job is to efficiently kill bad ideas, not to fully characterize the winning one. The follow-on rungs (concierge, painted-door) do the user-behavior validation. A smoke test is not trying to be user validation; it's a filter that determines whether user validation is worth running.

**Position B (Cagan, SVPG):** Cagan's 2024 SVPG writing[^3][^28] argues that demand tests — signups, click-throughs on landing pages — are a weak signal that conflates *curiosity* with *willingness to use a product in context*. His evidence base: a meaningful fraction of features that smoke-tested well shipped to negative retention because the smoke test measured a novelty reaction, not behavior change. Cagan's operational position is that the *minimum* bar for product validation is usability, feasibility, value, and viability assessed against a real user doing the real job with the real product or a high-fidelity facsimile — which pushes you to rung 4 or 5 as the *first* binding rung, not rung 2 or 3.

**My position:** Cagan is right that smoke tests are weak user signal and wrong to imply they are therefore not worth running. A smoke test is a cheap filter on the *portfolio* of ideas worth user-validating. Run rung 2 to decide which ideas make it to rung 4; don't skip rung 4 because rung 2 was promising; don't skip rung 2 because Cagan's bar is user validation. In practice, the Savoia ladder and the Cagan bar are complementary — the ladder tells you the cheapest rung for each assumption; the Cagan bar tells you *you are not done until you have passed rung 4 or 5 on value, usability, feasibility, viability*. Operators who treat rung 2 as sufficient are the Cagan critique's real target; operators who skip rung 2 because Cagan dismissed it miss the point of filtering the portfolio.

### Controversy 3 — Has the concierge rung changed shape in the Claude Code era?

Partially unresolved. The 2024–2025 pattern that a concierge service *is now a Claude Code orchestration operated by a founder* blurs Savoia's original distinction between "manual work behind a UI" and "automated work." If the founder is driving Claude Code, is that concierge (human-operated) or pretotyped automation (AI-operated)? Andrew Chen's 2024–2025 a16z writing[^29] on consumer AI suggests the "AI-in-the-loop concierge" is the dominant rung-4 shape for AI products now, because the founder can iterate the Claude workflow between customers in ways a purely manual concierge could not. The open question is whether this shortens the concierge phase (patterns stabilize faster when Claude is already capturing them) or lengthens it (founders over-trust Claude's outputs and automate prematurely). Public data is thin; the operator judgment is still being formed.

## Reviewer lens — named critics with specific disagreements

- **Alberto Savoia** (pretotyping founder)[^1][^4] would push back on the sentence *"Most operators skip rungs upward toward MVP because building feels like progress; the demotion is the operator discipline."* His argument: the deeper failure is skipping the *skin-in-the-game* rung-1 paper test. Operators who write the "would I personally commit a week and $500 to this?" paragraph kill 70–80% of their own ideas on paper before any rung-2 artifact exists, and the rung-demotion discipline is a second-order fix to a first-order failure. The lesson under-weights rung 1.
- **Teresa Torres** (Continuous Discovery Habits, Product Talk Academy)[^16][^17][^18] would push back on the controversy framing of *fake-door testing is fine if post-click-disclosed*. Her position: any test that relies on user surprise-and-disclose is a weaker signal than a direct Wizard-of-Oz or concierge test where the user is a willing participant. She would argue the lesson's go/no-go math privileges quantitative signal over the continuous-discovery rhythm (weekly interviews with 3–4 customers) that actually surfaces why a given rate was observed. The sample-size math section is correct, she'd say, but insufficient — it tells you *what* you saw, not *why*.
- **Marty Cagan** (SVPG)[^3][^28] would push back on the Layer 1 rung definitions. His line: rung 2 smoke tests are "demand validation," not product validation, and the lesson should be sharper about what each rung *cannot* answer. Specifically: a rung-2 win does not tell you value, usability, or viability — only whether a message resonates enough to produce a click. He would insist on naming the *minimum* rung at which Cagan's four-risk assessment actually holds (rung 4 at earliest, typically rung 5).
- **Rob Fitzpatrick** (*The Mom Test*, revised 2024)[^30] would push back on the Runnable Experiment Phase 4 memo-first protocol. His argument: the memo-first discipline correctly solves the post-hoc-rationalization problem at the *quantitative* layer but does nothing for the qualitative layer, where the Mom Test's three commandments (talk about their life not your idea, ask about specifics in the past not hypotheticals, talk less and listen more) are the binding constraint. The lesson should explicitly include a Mom-Test-audited interview script as a companion to any rung-2 or rung-3 test, because the most common failure at those rungs is misreading a click as "interest" when it was actually politeness.
- **Lenny Rachitsky** (*Lenny's Newsletter*)[^12][^31] would push back on the case-study selection. His argument: Dropbox's demo-video story has been over-cited to the point of mythologizing — it was as much a luck-of-the-Hacker-News-crowd moment as a reproducible method, and the signal-to-noise in "viral smoke test" is terrible. He'd insist on at least one boring, non-viral smoke-test case (Buffer is fair, but a B2B SaaS case with a paid-ads traffic source would be fairer) to prevent readers from inferring that rung 2 requires or even benefits from virality.
- **Andrew Chen** (a16z)[^29] would push back on the Controversy 3 framing. His position: the "AI-in-the-loop concierge" is not just a rung-4 variant — it is a genuinely new category of pretotype that deserves its own rung between 4 and 5, because the founder-operating-Claude-Code pattern has fundamentally different economics (lower marginal cost per run, higher pattern-capture rate) than pre-LLM manual concierge. The lesson treats it as a variant; Chen would argue it's a structural change in the ladder.

## Further reading

**Must-read (≤5)**

- Alberto Savoia, *Pretotype It — 10th Anniversary Edition* (2022), and pretotyping.org[^1][^4]. The source text.
- Teresa Torres, *Continuous Discovery Habits* (2021) + Product Talk's Opportunity Solution Tree and Assumption Testing articles[^16][^17]. The discipline that picks the rung.
- Marty Cagan, *Product Validation* and *The Biggest Risk* (SVPG, 2024)[^3][^28]. The critique of demand validation, stated at full strength.
- Paul Graham, *Do Things That Don't Scale* (2013)[^15]. Still the clearest case for rungs 3–4.
- Rob Fitzpatrick, *The Mom Test — Revised and Expanded Edition* (2024)[^30]. The qualitative companion to the sample-size math.

**Recommended**

- Joel Gascoigne, *How to successfully validate your idea with a Landing Page MVP* (Medium)[^6][^19]. The Buffer two-page canonical write-up.
- Lenny Rachitsky, *Superhuman's secret to success* podcast episode with Rahul Vohra[^12]. Concierge at scale with specific numbers.
- MeasuringU, adjusted-Wald calculator[^26]; Wikipedia, Binomial proportion confidence interval[^27]. The sample-size math.
- CPPA Enforcement Advisory 2024-02 (September 4 2024)[^2]. The dark-pattern enforcement context for fake-door ethics.
- Ryan Singer, *Shape Up* and *Shaping in Real Life* (2024–2025 updates)[^32]. The shaping discipline that sits alongside rung-picking.

**Optional**

- Nick Swinmurn / Zappos "Wizard of Oz" write-ups[^10][^33]. The canonical concierge.
- Airbnb cereal-and-photos YC-era story[^13][^14]. The canonical painted-door-in-existing-product.
- GoodUI, Chameleon, ProdPad fake-door pattern libraries[^8][^9]. The practitioner corpus.

## Citations

[^1]: Alberto Savoia, *Pretotype It: Make sure you are building The Right It before you build It right*, 10th Anniversary Edition, 2022; pretotyping.org. https://www.pretotyping.org/ — framework origin, six-rung ladder vocabulary, "YODa" (Your Own Data) rule.

[^2]: California Privacy Protection Agency, *Enforcement Advisory No. 2024-02*, September 4 2024 — dark-pattern enforcement under the CCPA; civil penalties up to $2,500 per violation and $7,500 for willful violations. https://cppa.ca.gov/pdf/enfadvisory202402.pdf

[^3]: Marty Cagan / Silicon Valley Product Group, *Product Validation*, 2024. https://www.svpg.com/product-validation/ — four-risk (value, viability, usability, feasibility) framework, critique of demand-only validation.

[^4]: Alberto Savoia, *Pretotype It* 2nd Edition PDF, hosted at pretotyping.org. https://www.pretotyping.org/uploads/1/4/0/9/14099067/pretotype_it_2nd_pretotype_edition-2.pdf — full framework text.

[^5]: Dropbox MVP explainer-video story: TechCrunch, *How DropBox Started As A Minimal Viable Product* (2011), Shortform synthesis, and corroborating 2025–2026 write-ups. The beta waitlist moved from ~5,000 to 75,000 overnight after the video was posted to Hacker News and Digg in late 2007 / early 2008. https://techcrunch.com/2011/10/19/dropbox-minimal-viable-product/ ; https://www.shortform.com/blog/dropbox-mvp-explainer-video/

[^6]: Joel Gascoigne, *How to successfully validate your idea with a Landing Page MVP*, Medium (written 2011, widely reprinted through 2024). https://medium.com/@joelgascoigne/how-to-successfully-validate-your-idea-with-a-landing-page-mvp-ef3c2d02dc51 — Buffer two-page-plus-pricing validation.

[^7]: Interview with Gmail PM Todd Jackson — TechCrunch (2008); Google System blog, *Gmail Priority Inbox* (August 2010). https://techcrunch.com/2008/06/05/interview-with-product-manager-todd-jackson-on-gmail-labs/ ; https://googlesystem.blogspot.com/2010/08/gmail-priority-inbox.html — Gmail Labs as painted-door surface; Priority Inbox context.

[^8]: GoodUI, *Patterns* library — Jakub Linowski. https://goodui.org/patterns/ — A/B-tested conversion patterns including fake-door variants, with operator ethics commentary.

[^9]: Chameleon, *Fake Door Testing: How It Works, Benefits & Risks* (2024). https://www.chameleon.io/blog/fake-door-testing — operational guide with the "disclose immediately post-click" ethics bar.

[^10]: Medium / Rocket Startup, *How Zappos Built a Product By Faking It*; WWD, *Zappos Milestone: Q&A With Nick Swinmurn*; related "doing things that don't scale" Zappos write-ups. https://medium.com/rocket-startup/how-zappos-built-a-product-by-faking-it-d3fd692a1fed ; https://wwd.com/footwear-news/shoe-industry-news/zappos-milestone-qa-with-nick-swinmurn-1237699700/ — Wizard-of-Oz concierge, 1999.

[^11]: First Round Review, *Superhuman's Onboarding Playbook* and *How Superhuman Built an Engine to Find Product/Market Fit*, 2018–2023 (with ongoing 2024–2025 citations). https://review.firstround.com/superhuman-onboarding-playbook/ ; https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/ — manual 1:1 onboarding at scale, ~2 hours per session.

[^12]: Lenny Rachitsky, *Superhuman's secret to success* podcast with Rahul Vohra. https://www.lennysnewsletter.com/p/superhumans-secret-to-success-rahul-vohra — Vohra discloses dozens of full-time Onboarding Specialists, tens of thousands of paying customers onboarded 1:1.

[^13]: Medium / Product Habits / Fortune 2023 / CNBC 2023, *Airbnb founder story — cereal, hosts, YC*. https://fortune.com/2023/04/19/airbnb-ceo-cereal-box-investors-changed-everything-billion-dollar-company/ ; https://producthabits.com/how-two-designers-created-airbnb-and-turned-it-into-a-30-billion-company/ — 2008–2009 chronology.

[^14]: Paul Graham / Y Combinator library — Airbnb founders going door-to-door in NY with a rented camera, photographing listings, documenting 2–3× booking lift. https://www.paulgraham.com/ds.html — *Do Things That Don't Scale*, 2013, Airbnb and Stripe "Collison installation" cases.

[^15]: Paul Graham, *Do Things That Don't Scale*, July 2013. https://www.paulgraham.com/ds.html — canonical essay on concierge and hand-recruitment rungs.

[^16]: Teresa Torres, *Opportunity Solution Trees: Visualize Your Discovery to Stay Aligned and Drive Outcomes*, producttalk.org (2023, with 2024–2025 Product Talk updates). https://www.producttalk.org/opportunity-solution-trees/ — outcome → opportunity → solution → assumption-test tree; "interview every 3–4 customers, revisit opportunity space monthly" cadence.

[^17]: Teresa Torres, *Assumption Testing* course, Product Talk Academy (2024). https://learn.producttalk.org/assumption-testing — Risky Assumption Test as a faster, less costly alternative to MVP; "test the riskiest assumption, not the easiest one."

[^18]: Teresa Torres on Aakash Gupta's podcast, *Step-by-Step Guide to AI Product Discovery* (2025). https://www.news.aakashg.com/p/teresa-torres-podcast — 2025 framing of continuous discovery for AI products.

[^19]: Buffer / The Launcher, *Idea to Paying Customers in 7 Weeks* and *The Two-Page Strategy That Launched Buffer*. https://buffer.com/resources/idea-to-paying-customers-in-7-weeks-how-we-did-it/ ; https://thelauncher.substack.com/p/from-0-to-paying-customers-the-two — Gascoigne's two-step validation, first paying customer within 4 days.

[^20]: The broader fake-door / painted-door lineage: Optimizely, *What is a painted door test? It's benefits and examples* (updated 2024). https://www.optimizely.com/optimization-glossary/painted-door-test/ ; A/B Tasty, *What is Fake Door Testing, aka Painted Door Test*. https://www.abtasty.com/glossary/fake-door-testing/

[^21]: ProdPad, *What is Fake Door Testing? Definition & Overview*. https://www.prodpad.com/glossary/fake-door-testing/ — product-management glossary with operator ethics notes.

[^22]: Contentful, *What's a painted door test, and why should you use one?* https://www.contentful.com/blog/painted-door-test/ — operator write-up.

[^23]: Amplitude, *What Is Fake Door Testing: Methods And Best Practices*. https://amplitude.com/explore/experiment/fake-door-testing — experimentation-platform pattern docs.

[^24]: LearningLoop, *Fake Door Testing: What It Is and How to Run One*. https://learningloop.io/plays/fake-door-testing — "be honest that it's a test as soon as the user would potentially feel misled" rule.

[^25]: Reforge, *How Superhuman's CEO Reverse-Engineered Product/Market Fit*. https://www.reforge.com/blog/brief-how-superhuman-s-ceo-reverse-engineered-product-market-fit — Sean Ellis PMF test applied to Superhuman; the "on-the-fence" segment methodology.

[^26]: MeasuringU, *Confidence Interval Calculator for a Completion Rate* (adjusted Wald). https://measuringu.com/calculators/wald/ — operator tool for small-N (N<150) conversion CIs.

[^27]: Wikipedia, *Binomial proportion confidence interval* — Wilson score interval, Clopper-Pearson exact interval, adjusted Wald. https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval

[^28]: Marty Cagan / SVPG, *The Biggest Risk*, 2024. https://www.svpg.com/the-biggest-risk/ — specific critique of "demand validation ≠ user validation" and the four-risk bar.

[^29]: Andrew Chen / a16z speedrun, 2024–2025 writing on consumer AI and viral loops. https://a16z.com/author/andrew-chen/ ; https://andrewchen.com/ — context for AI-in-the-loop concierge and user-acquisition math.

[^30]: Rob Fitzpatrick, *The Mom Test — Revised and Expanded Edition*, Simon & Schuster (2024). https://www.simonandschuster.com/books/The-Mom-Test/Rob-Fitzpatrick/9798893312577 — interview discipline; the three commandments (life not idea, past not hypothetical, listen more).

[^31]: Lenny Rachitsky, *Lenny's Newsletter*, ongoing validation and product teardowns, 2024–2026. https://www.lennysnewsletter.com/ — case-selection reference.

[^32]: Ryan Singer, *Shape Up* (2019) and *Shaping in Real Life* (2024–2025 update course). https://basecamp.com/shapeup/ ; https://www.ryansinger.co/ — shaping as the upstream discipline to rung picking; "appetite + scope" framing.

[^33]: AlexanderJarvis.com, *Zappos doing things that don't scale*. https://www.alexanderjarvis.com/zappos-doing-things-that-dont-scale/ — corroborating Swinmurn Wizard-of-Oz account with operational detail.

_last_verified: 2026-04-17_
