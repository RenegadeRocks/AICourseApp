---
type: lesson
block: block-6-launch-monetization
week: week-17
session_slug: growth-hacking-referral-loops
day_of_cycle: 5
day_name: fri
date_due: 2026-09-11
tags:
  - growth-system
  - north-star-metric
  - input-metrics
  - vanity-metrics
  - retention-first
  - growth-theater
  - sustainable-growth
  - leaky-bucket
sources:
  - reforge-growth-loops
  - baincapital-elena-verna-plg
  - measuringu-nps-discredited
  - andrewchen-shitty-clickthroughs
  - firstround-superhuman-pmf-engine
  - devto-growth-hacking-2025
  - amplitude-hidden-roi-winback
  - reforge-north-star-metrics
last_verified: 2026-07-17
word_count_target: 3700
---

# The growth system: loops, lifecycle, feedback, and honest measurement

## Why this matters

You now have four pieces from this week: a feedback engine (Monday), a
re-engagement system (Tuesday), a loop framework (Wednesday), and referral math
(Thursday). A pile of pieces is not a system. This lesson assembles them into one
coherent growth machine and, more importantly, teaches you to measure it in a way
that will not lie to you. The failure mode this lesson prevents is the most common
and most seductive in all of growth: **growth theater**, where the dashboard is
green, the vanity metrics climb, and the business is quietly dying underneath. By
the end you can draw your own input-metric tree, tell a real growth signal from a
cosmetic one, apply the retention-first principle that makes every other lever
worth pulling, and, crucially, know when to stop optimizing growth and go back to
fixing the product.

## Prerequisites

- [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/01-mon-product-analytics-for-ai-products|Product analytics for AI products]]
  (Block 5). The north-star metric and the retention curve are defined there.
  This lesson builds the input-metric tree *below* the north star and connects it
  to the growth machinery.
- [[03-wed-growth-loops-vs-funnels|Growth loops vs funnels]] and
  [[04-thu-referral-and-virality-engineering|Referral engineering]] (this week).
  The loop and its math are the moving parts of the system we assemble today.

## First principles: a growth system is loops governed by retention

The whole week reduces to one architecture. Your product has a north-star metric
(the retained, valued action from Week 14). Below it sits an input-metric tree:
the handful of levers that, when moved, move the north star. Around it run the
loops (Wednesday) that reinvest output into input. Feeding the loops is the
feedback engine (Monday) that keeps the product worth spreading, and the lifecycle
system (Tuesday) that plugs the leaks. And underneath all of it, non-negotiable,
is retention, because every loop multiplies retention: a loop that pours users
into a leaky bucket just makes the leak louder.

That last point is the spine of the lesson, so state it plainly:
**growth without retention is a leaky bucket, and every growth lever multiplies
whatever retention you already have.** A referral program on a product with 20%
retention refers users who churn. A viral loop on a product nobody keeps spreads
churned users. This is why Monday came before Thursday, and why this whole block
followed Block 5's retention work rather than preceding it. Retention is the
multiplier; growth is the multiplicand. Optimize the multiplicand while the
multiplier is broken and you get a bigger version of nothing.

## The input-metric tree

Your north star is a lagging, aggregate number. You cannot pull a lever labeled
"north star." You pull levers below it. The input-metric tree makes the causal
chain explicit so your team works on causes, not symptoms.

Take the AI meeting-notes north star from Week 14: **weekly accounts that shared
or exported a note.** Its input tree:

```
North star: weekly accounts that shared/exported a note
├── New activated accounts        (acquisition × activation)
│   ├── new signups               ← acquisition loops (content, viral, paid)
│   └── activation rate           ← onboarding, time-to-first-value
├── Retained active accounts      (the multiplier)
│   ├── week-over-week retention  ← product quality, feedback engine
│   └── reactivated accounts      ← lifecycle win-back (Tuesday)
└── Share/export rate per account (the value-realization step)
    ├── output quality            ← feedback engine (Monday)
    └── share friction            ← loop design (Wednesday)
```

Every leaf is something a person can own and move this week. The tree does two
jobs. First, it stops arguments: instead of debating "how do we grow," you ask
"which leaf is weakest," which is answerable with data. Second, it exposes the
retention multiplier sitting in the middle of the tree, so a team tempted to pour
effort into the acquisition leaves can see that a leak in the retention branch
poisons everything downstream. Reforge's north-star and loop work is built on
exactly this decomposition: the north star up top, the loops and input metrics
below.[^1][^2]

## Vanity metrics and growth theater

Growth theater is the art of looking like you are growing while you are not. Its
props are vanity metrics: numbers that only go up, that do not require value
delivered, and that survive even as the business dies. Cumulative signups. Total
registered users. Page views. "Impressions." App downloads. Every one of these can
climb while your retention curve flatlines at zero.

The tell, from Week 14, is durable: **a healthy metric can go down.** If a number
can only increase, it cannot warn you, and a metric that cannot warn you is a prop,
not an instrument. Cumulative signups is the most reassuring lie in your
dashboard. The honest version of every vanity metric is its weekly, decrementable
cousin: not total users but weekly active accounts, not cumulative signups but
this week's activated accounts net of churn.

The 2026 growth literature has, notably, converged on this. The consensus reframe
of growth hacking is precisely a rejection of vanity metrics in favor of
retention, cohort curves, and LTV: what died is the exploit-and-vanity version,
what remains is the experiment-led, retention-anchored discipline.[^3][^4] Even the
growth-hacking industry now says the quiet part: chasing vanity metrics is the
thing that discredited the field.

Three specific theater patterns to name and refuse:

- **The cumulative chart.** Any "all-time total" going up and to the right. It is
  designed to reassure investors and yourself. Replace with weekly actives.
- **The unsustainable spike.** A growth hack (a viral gimmick, a Product Hunt
  spike, a paid blitz) that produces a number with no loop behind it. It decays,
  per the Law of Shitty Clickthroughs, and leaves nothing compounding.[^5]
- **The gamed north star.** A north star with no counter-metric, optimized until
  the number rises without value. From Week 14: pair every north star with a
  counter-metric that catches the cheat.

## Sustainable vs mercenary growth

There is a real strategic fork here, and you should choose consciously.
**Mercenary growth** buys numbers: paid blitzes, cash referral bounties, aggressive
re-engagement, growth hacks. It works, fast, and it stops the moment you stop
paying, and it often attracts users who never wanted the product. **Sustainable
growth** builds loops that compound: content that keeps attracting, referral from
genuine love, a product that gets more valuable as more people use it. It is slower
to start and it keeps working after you stop pushing.

The trap is that mercenary growth looks better on a quarterly chart, so
under pressure teams default to it, and then wonder why the growth evaporates when
the budget does. Elena Verna's framing captures the discipline: loops are the
engine, the one-off tactics are turbo boosts, and a business running on turbo
boosts alone has no engine.[^2] Mercenary tactics have a place, as fuel to ignite a
loop or bridge a gap, but a growth strategy that is *only* mercenary is renting
growth, not building it.

> My take: the honest test for any growth tactic is "what happens when I stop?" If
> the answer is "growth stops immediately," you have a funnel or a hack, and that
> is fine as long as you know it and are not fooling yourself that you built a
> machine. If the answer is "growth keeps compounding for a while," you have a
> loop. Most founders cannot answer this question about their own growth, which is
> the real diagnosis.

## When to stop optimizing growth and go back to the product

This is the lesson's sharpest and least-taught point. Growth optimization has a
precondition: a product worth growing. There is a specific signal that you should
stop tuning loops and go back to product, and it is your PMF evidence from Monday.
If your Sean Ellis "very disappointed" score is well below 40%, or your retention
curve decays toward zero instead of flattening into a plateau, **more growth is the
wrong investment**, because you would be accelerating users into a product that
does not hold them. Superhuman's whole story was recognizing this: at 22% PMF,
Rahul Vohra did not build a referral program, he spent a year fixing the product
until the score hit 58%, and *then* growth was worth pursuing.[^6]

So the decision rule: before you invest in any growth loop, check the multiplier.

- **Retention curve flattening at a healthy plateau + PMF above ~40%** → build
  growth loops; the machine is worth feeding.
- **Retention decaying toward zero, or PMF well below 40%** → stop, go back to the
  feedback engine and the product. Growth spend now is wasted.
- **In between (plateau low but non-zero, PMF 25 to 40%)** → the Superhuman play:
  segment, find your high-expectation core, fix the fence-sitters' blockers,
  re-measure. Grow into the segment that already loves it, not the whole market.

This is the anti-hype heart of the week. The growth-hacking industry sells the
loops; the discipline is knowing when you have not earned the right to build them
yet.

## Worked example: assembling and stress-testing the system

Put the pieces together for the meeting-notes product and pressure-test each
connection.

| Piece | Concrete instance | Health check |
|---|---|---|
| North star | Weekly accounts that shared/exported a note | Can it go down? Yes. Good. |
| Counter-metric | Edit-heaviness + regeneration rate | Catches "shared but bad" |
| Dominant loop | Collaboration (invite teammates to shared notes) | k and cycle time instrumented? |
| Feedback engine | Sean Ellis survey + tagged support | PMF core identified? |
| Lifecycle | Approaching-dormancy + you-asked-we-fixed triggers | Frequency-capped, honest? |
| Retention multiplier | W-o-W retention of activated accounts | Plateau or decay? |

Now stress-test the connections, because a system fails at its joints:

1. **Does the loop feed a leaky bucket?** If retention is decaying, the
   collaboration loop is spreading churners. Fix retention first.
2. **Does the feedback engine actually change the roadmap?** If tagged support
   tickets never become shipped fixes, the "you-asked-we-fixed" trigger has
   nothing to fire and the loop is decorative.
3. **Is any metric in the tree a vanity prop?** If your team's headline number is
   cumulative signups, replace it before it lulls you.
4. **What happens if you stop all paid spend tomorrow?** If growth goes to zero,
   your "system" is a funnel wearing a loop costume.

**Pass bar:** you can draw your own product's input-metric tree with the retention
multiplier explicitly in the middle, name one vanity metric you will stop
reporting, and state the one condition under which you would stop optimizing growth
and go back to the product. If you cannot name that stopping condition, you do not
yet have a growth *system*, you have a set of tactics.

## Common mistakes experts see

1. **Optimizing growth on top of broken retention.** Every loop multiplies
   retention; multiply a leak and you get a louder leak. Check the multiplier
   before feeding the loops.
2. **Reporting cumulative vanity metrics.** If it can only go up, it cannot warn
   you. Switch to weekly, decrementable numbers.[^3]
3. **A north star with no counter-metric.** You will optimize against yourself.
   Pair every north star with a guardrail.
4. **Confusing a spike for a system.** Unsustainable hacks decay and leave nothing
   compounding.[^5] Ask what happens when you stop.
5. **Growing the whole market when only a segment loves you.** The Superhuman
   correction: grow into your high-expectation core, not the mass you have not
   won.[^6]
6. **Never defining the stopping condition.** Not knowing when to abandon growth
   optimization for product work is how teams pour a year into loops on a product
   below PMF.

## Reflection questions

1. Draw your input-metric tree. Where exactly does the retention multiplier sit,
   and what happens to every leaf below it if that branch leaks?
2. Name one metric you currently report that can only go up. What is its honest,
   decrementable replacement?
3. Apply the "what happens when I stop?" test to your single biggest growth
   activity right now. Loop or funnel? Are you sure?
4. What is your product's specific stopping condition, the signal that would make
   you halt growth work and return to the product? Is that signal instrumented?
5. Sustainable or mercenary: honestly categorize your current growth. If it is
   mercenary, what is the loop you would build to replace it, and what is stopping
   you?

## My take (reviewer lens)

**Michael Seibel** would applaud the stopping-condition section and push it
further: for most early-stage founders the answer is almost always "go back to the
product," because almost nobody has earned the right to optimize growth yet, and
the growth-system diagram can become an elaborate way to avoid the uncomfortable
truth that not enough people love the thing. He is right that the bias should be
strongly toward product work early. Use the input-metric tree to *find* the leak,
then go fix it, rather than admiring the tree.

**Andrew Chen** would note that even a well-built system decays, so "assemble the
system" is not a finish line: the loops erode via saturation and habituation, and a
system that compounded last quarter can stall this quarter with no change on your
part.[^5] Fair. The system is a living thing that needs continuous work against
decay, not a machine you build once. Budget for maintenance, not just
construction.

**Chip Huyen** would add the measurement rigor the growth world routinely skips:
most claimed growth "wins" are not measured against a holdout, so teams credit a
campaign for users who would have converted anyway (the same selection effect that
inflates win-back numbers from Tuesday). Before you declare any lever a success,
compare it to a control group. Without incrementality measurement, the whole
input-metric tree is decorated with numbers you cannot trust.

## Further reading

**Must-read**

- Reforge, "Growth Loops are the New Funnels" (system view) plus their north-star
  work (the input-metric tree). The two together are the architecture.[^1][^2]

**Recommended**

- Rahul Vohra, "How Superhuman Built an Engine to Find Product/Market Fit," for
  the stopping-condition discipline in practice.[^6]
- Andrew Chen, "The Law of Shitty Clickthroughs," for why the system needs
  continuous maintenance.[^5]

**Optional**

- DEV/Synergist, "Growth Hacking in 2025: What Actually Moves the Needle," for the
  industry's own turn against vanity metrics.[^3]

## Citations

[^1]: Brian Balfour et al., "Growth Loops are the New Funnels," Reforge Blog.
https://www.reforge.com/blog/growth-loops — loops as the system-level view; north
star fed by input metrics and loops. (search-verified 2026-07-17; fetch
egress-blocked — liveness pass pending; corroborated by Aakash Gupta's growth-loops
guide.)
[^2]: Elena Verna, growth-model menu and Racecar framework (loops=engine,
tactics=turbo boosts, funnels=fuel), via Bain Capital Ventures.
https://baincapitalventures.com/insight/plg-expert-elena-verna-breaks-down-the-new-b2b-growth-standard/
— sustainable loops vs one-off tactics. (search-verified 2026-07-17; corroborated
by her newsletter elenaverna.com.)
[^3]: DEV/Synergist, "Growth Hacking in 2025: What Actually Moves the Needle."
https://dev.to/synergistdigitalmedia/growth-hacking-in-2025-what-actually-moves-the-needle-and-what-just-sounds-cool-276
— industry reframe rejecting vanity metrics for retention/cohort/LTV.
(search-verified 2026-07-17; corroborated by Venture Lab 2026 trends piece.)
[^4]: Venture Lab, "15 Growth Hacking Trends in 2026 (What's Replacing Old
Playbooks)." https://venture-lab.org/2026/growth-hacking-trends-2026/ — vanity-metric
rejection; retention-anchored discipline. (search-verified 2026-07-17.)
[^5]: Andrew Chen, "The Law of Shitty Clickthroughs."
https://andrewchen.com/the-law-of-shitty-clickthroughs/ — channels and loops decay;
spikes leave nothing compounding. (search-verified 2026-07-17; corroborated by his
Substack.)
[^6]: Rahul Vohra, "How Superhuman Built an Engine to Find Product/Market Fit,"
First Round Review. https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/
— fixed product at 22% PMF before pursuing growth; grew into high-expectation
segment. (search-verified 2026-07-17; corroborated by Reforge summary.)

_last_verified: 2026-07-17_
