---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: analytics-iteration-what-to-measure
day_of_cycle: 3
day_name: wed
date_due: 2026-08-19
tags:
  - iteration
  - experimentation
  - ab-testing
  - small-sample
  - cohort-analysis
  - prompt-iteration
  - local-maxima
  - painted-door
sources:
  - kohavi-trustworthy-experiments-2020
  - amplitude-experiment-cuped-2024
  - optimizely-peeking-problem-2015
  - reforge-north-star-deceive-2024
  - hamel-husain-evals-faq-2026
  - startup-genome-premature-scaling-2011
  - seibel-launch-fast-2020
  - jeremyhoward-iterate-2024
  - lenny-duolingo-retention-2021
last_verified: 2026-07-17
word_count_target: 5200
---

# The iteration loop: turning numbers into changes when you have 40 users, not 40,000

## Why this matters

Metrics are worthless until they change what you build. This lesson is the
engine that converts Monday's numbers and Tuesday's pipes into shipped product
changes, at the awkward scale most of you are actually at: dozens of users, not
thousands. At that scale, the textbook A/B test is statistically dead on arrival,
and the honest, high-velocity loop is a different beast made of funnels,
cohorts, transcripts, and prompt diffs. Get this loop right and you compound;
get it wrong and you either ship on vibes or freeze waiting for significance that
will never come.

After this lesson you can run a hypothesis → measure → decide cadence weekly,
know when you have enough users to A/B and what to do when you do not, treat
prompt and model changes as product experiments with the same rigor, and avoid
the local-maximum trap where you optimize a good feature while a better product
sits one scary redesign away.

## Prerequisites

- [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/06-sat-validation-instrumentation|Wilson-interval discipline]]
  (Block 2). That is the canonical home for small-sample confidence intervals.
  We will *use* the Wilson interval today; we will not re-derive it. If the phrase
  "a raw 3/5 conversion is not 60%" does not ring a bell, re-read that lesson
  first.
- [[01-mon-product-analytics-for-ai-products|Monday's north star + counter-metric]]
  and [[02-tue-instrumentation-and-the-analytics-stack|Tuesday's two pipes]].
  The loop moves the north star and reads the counter-metric to catch cheating.

## First principles: the loop, and why most people don't actually run it

The loop is old and simple: **hypothesis → change → measure → decide → repeat.**
Everyone nods. Almost nobody runs it, for two reasons. First, they skip the
hypothesis and go straight to change ("let's add dark mode"), so there is nothing
to measure against. Second, they skip the decide and let changes accumulate
without ever killing the losers, so the product bloats. A real loop has a written
hypothesis before the change and a kill-or-keep decision after.

A hypothesis has a shape:

> *We believe that [change] will cause [metric] to move [direction] for [segment],
> because [reason]. We'll know we're wrong if [metric] does not move by [amount]
> within [window].*

Fill every bracket. The last two brackets are the ones people omit, and they are
the whole point: a hypothesis you cannot be wrong about is a wish. This is the
same discipline as the Block 4 validation loop, pointed inward at a live product
instead of outward at a market.

## The uncomfortable truth about A/B testing at your scale

A/B testing is the gold standard for causal attribution, and at 40 users it is
mostly theater. Here is the math you must internalize, not to run it but to know
when *not* to.

To detect a realistic product improvement (say, lifting a 20% activation rate to
25%, a genuinely large 5-point absolute lift) with standard 80% power at 95%
confidence, you need on the order of **~1,000 users per variant** — roughly 2,000
total.[^1] For smaller, more typical lifts (20% to 22%), you need *tens of
thousands*. Ronny Kohavi, who ran experimentation at Microsoft and Airbnb and
wrote the field's standard text, is blunt that most observed effects are small
and most teams badly underpower their tests, then fool themselves by
peeking.[^1]

Which brings the second killer: **the peeking problem.** If you watch a running
A/B test and stop it the moment it looks significant, your false-positive rate is
not 5%; it can climb past 30%, because you gave yourself dozens of chances to
cross the line by noise.[^2] Optimizely's own statisticians published this as the
reason they moved to sequential testing; the naive "check daily, stop when green"
workflow manufactures wins that evaporate in production.[^2]

So for most readers of this course: **you cannot A/B your way to product/market
fit.** Trying to is a form of premature scaling of rigor. Startup Genome's
lesson applies to process too — heavyweight experimentation before you have the
traffic to feed it is optimizing the wrong thing at the wrong time.[^3]

> My take: A/B testing is a scale tool. Below a few thousand active users it is
> usually a way to feel rigorous while learning nothing. The teams that ship
> fastest at small scale barely A/B test; they run the qualitative loop below and
> save controlled experiments for the two or three decisions that are both
> high-stakes and high-traffic (pricing page, signup flow).

## The small-N iteration loop (what you actually run)

When you cannot A/B, you use four instruments together. None is causally clean;
together they are enough to decide.

### 1. Funnel analysis (where, not why)

Lay out the steps to your north-star action and measure the drop at each step.
This needs no control group; it is descriptive. A 70% drop between "generated
first report" and "shared first report" tells you exactly where to point the
other three instruments. Funnels find the wound; they do not diagnose it.

### 2. Cohort retention (did the change actually stick)

Group users by the week they signed up and watch each cohort's retention curve.
When you ship a change, you are asking: *does the cohort that experienced the new
version retain better than the cohort before it?* This is a quasi-experiment, not
a clean A/B (the cohorts differ in more than your change), so read it with
humility, but a retention curve that visibly lifts for post-change cohorts and
holds for weeks is strong evidence at a scale where A/B is impossible. Lenny's
Duolingo case is fundamentally cohort-read: they watched engagement cohorts move
as they changed the habit loop.[^4]

### 3. Transcripts and session replay (why)

This is the highest-leverage instrument at small scale, and it is Hamel Husain's
central point: **read your data.** Watch ten replays of users who dropped at the
funnel step. Read fifty AI transcripts where the user regenerated. You are not
computing anything; you are pattern-matching failure modes with your own eyes.
Hamel argues, correctly, that at early scale a human reading transcripts with a
spreadsheet finds more actionable problems per hour than any dashboard.[^5] The
funnel tells you *which* step; the transcripts tell you *what is wrong* there.

### 4. Wilson-interval-guarded comparisons (how sure)

When you do compare two small numbers (this week's activation vs last week's, or
variant A vs B with a few hundred users), never compare raw percentages. Put a
Wilson interval on each and ask if they even overlap. Most small-sample
"improvements" are two overlapping intervals, which means *you learned nothing,
do not ship on it.* This is the discipline from
[[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/06-sat-validation-instrumentation|Block 2]];
apply it, do not re-derive it.

The loop in practice: funnel finds the leaky step, transcripts explain it, you
form a hypothesis, you ship a change, cohort retention plus a Wilson-guarded
funnel comparison tell you keep-or-kill. One turn a week. That cadence, held for
three months, beats any single clever feature.

## Prompt and model iteration IS product iteration

Here is the twist unique to AI products. For a normal SaaS, "the product" is the
code and the UI. For your product, a large chunk of "the product" is the prompt,
the retrieval strategy, and the model choice. Changing the system prompt is a
product change with the same blast radius as redesigning a screen, and it must go
through the same loop, plus one extra guard.

The extra guard is **an eval set**, because prompt changes have a nasty property:
they fix the case in front of you and silently break three you are not looking
at. Hamel's evals discipline is the answer — a small golden set of real
input/expected-behavior pairs that you replay on every prompt change, so a
"fix" that regresses other cases is caught before it ships.[^5] Without this, you
enter an infinite loop of whack-a-mole where every prompt tweak trades one bug for
another and your quality-drift metric (Monday, metric 4) wanders.

Treat model swaps identically. Moving from a frontier model to a cheaper small
one to save cost-per-active-user is a product experiment: hypothesis (cost drops,
quality holds), measure (eval set score + feature-trust + regeneration rate),
decide. The current landscape makes this a live weekly decision — with a
new-default mid-tier model and a frontier tier, the right routing per feature
shifts as prices and capabilities move.[^6] Do not swap models on vibes; run the
eval set.

## Avoiding local maxima

The scariest failure of a tight iteration loop is that it works *too* well at
climbing a small hill. If every experiment is a small tweak to the current
design, you will reach the top of your current hill and stall, never seeing the
taller mountain across the valley that requires a redesign to reach. Reforge's
north-star-deception essay is partly about this: relentlessly optimizing one
metric can trap you in a local maximum where the metric is maxed and the product
is still mediocre.[^7]

Two defenses:

1. **Painted-door / fake-door tests for big swings.** Before building a
   fundamentally different version, test demand cheaply: add the button for the
   new thing, measure clicks, show a "coming soon" or waitlist. You get signal on
   the *mountain* without building the bridge. This is the Block 4 validation
   instinct applied to features, not markets.
2. **Reserve a slice of your iteration budget for non-incremental bets.**
   Something like 70% small optimizations, 30% swings that could fail. If 100% of
   your experiments are safe tweaks, you are guaranteed to end up on a local
   maximum. This is Google's old 70/20/10 instinct at feature scale.

> My take: at small scale the local-maximum risk is *lower* than people fear,
> because you have not climbed any hill high enough to be trapped. The bigger
> early risk is the opposite: thrashing between big swings, never holding a
> direction long enough to see if it works. Hold a hypothesis for its full
> measurement window before you abandon it. Discipline compounds; thrash does
> not.

## Worked example: one full turn of the loop

Your Week 12/13 meeting-notes product. Monday's north star: weekly accounts that
shared a note. Funnel shows: 80% generate a first note, only 25% share one. The
wound is generate → share.

You watch fifteen session replays of non-sharers and read their transcripts. The
pattern: notes are accurate but too long, and users do not trust a 900-word
summary of a 20-minute call, so they neither read nor share it. That is a
feature-trust failure hiding behind a share-rate number.

Hypothesis:

> *We believe adding a "TL;DR + 3 action items" format at the top will lift the
> generate→share rate for new accounts from 25% toward 40%, because users will
> trust and forward a scannable summary. We're wrong if share rate doesn't move
> at least 8 points within two weekly cohorts.*

The change is a prompt change, so you first extend the eval set with ten real
transcripts and their ideal TL;DRs, and confirm the new prompt does not regress
factual accuracy on the golden set. Then you ship it to new signups.

Two weeks later: the post-change cohort's generate→share rate is 38% vs 25%,
regeneration rate held steady (not a fake win from users retrying), and eval
accuracy held. Wilson intervals on 38% (n≈120) and 25% (n≈110) do not overlap.
**Decision: keep, and roll to all users.** One turn. Notice how little of it was
statistics and how much was reading fifteen transcripts.

```python
# decide.py — the keep/kill guard: Wilson intervals must NOT overlap to ship.
# Run: python decide.py   (stdlib only; interval math is the Block 2 discipline)
from math import sqrt

def wilson(successes, n, z=1.96):
    if n == 0:
        return (0.0, 0.0)
    p = successes / n
    denom = 1 + z*z/n
    center = (p + z*z/(2*n)) / denom
    half = (z * sqrt(p*(1-p)/n + z*z/(4*n*n))) / denom
    return (round(center - half, 3), round(center + half, 3))

def should_ship(succ_a, n_a, succ_b, n_b):
    lo_a, hi_a = wilson(succ_a, n_a)   # control
    lo_b, hi_b = wilson(succ_b, n_b)   # variant
    overlap = not (hi_a < lo_b or hi_b < lo_a)
    better = (succ_b/n_b) > (succ_a/n_a)
    return {"control_ci": (lo_a, hi_a), "variant_ci": (lo_b, hi_b),
            "overlap": overlap, "ship": better and not overlap}

if __name__ == "__main__":
    # control 25% of 110; variant 38% of 120
    print(should_ship(28, 110, 46, 120))
```

**Pass bar:** the function returns `ship: True` only when the variant is both
better *and* its Wilson interval does not overlap the control's. Feed it two
genuinely close numbers (e.g. 28/110 vs 31/110) and it should return
`ship: False`. If you would have shipped on the raw percentages, this guard just
saved you from learning nothing and calling it a win.

## Common mistakes experts see

1. **Changing without a written hypothesis.** No prediction, no learning. Fill
   every bracket, especially "we're wrong if."
2. **A/B testing at 40 users.** Statistically dead; use the small-N loop. Save
   controlled experiments for high-stakes, high-traffic decisions.[^1]
3. **Peeking and stopping on green.** Turns a 5% false-positive rate into 30%+.
   Pre-commit to a window, or use sequential methods.[^2]
4. **Comparing raw percentages.** Two overlapping Wilson intervals is not an
   improvement, it is noise wearing a costume.
5. **Prompt-tweaking without an eval set.** Whack-a-mole forever; every fix
   silently breaks unseen cases. Golden set on every change.[^5]
6. **100% incremental experiments.** Guarantees a local maximum. Reserve budget
   for painted-door swings.[^7]
7. **Thrashing between big bets.** The opposite failure. Hold a hypothesis for
   its full window before abandoning it.

## Reflection questions

1. Write a full hypothesis for your product's leakiest funnel step, with every
   bracket filled. Which bracket was hardest, and why is it the important one?
2. How many active users do you have? Given that, which of your recent "wins"
   were actually two overlapping Wilson intervals?
3. What is one prompt change you shipped without an eval set? What might it have
   silently broken?
4. Where is your product's current local maximum — the hill you are climbing that
   caps out at "fine"? What painted-door test would reveal the taller mountain?
5. When you last read ten real user transcripts end to end, what did you learn
   that no chart had told you? If the answer is "I haven't," that is Wednesday's
   real assignment.

## My take (reviewer lens)

**Michael Seibel** would cut most of this: at your scale, stop measuring and go
talk to users. His refrain is that early founders overthink instrumentation as a
substitute for the terrifying work of watching someone use the thing and hearing
them say it is confusing.[^8] He is largely right, and the small-N loop leans
that way on purpose (transcripts over dashboards). Where I hold the line: even
Seibel-style user-watching needs the funnel to tell you *which* users to watch,
or you drown in anecdotes.

**Hamel Husain** would want the eval-set section to be the whole lesson. For AI
products he is close to right — the prompt-iteration loop *is* the product loop,
and teams that skip the golden set ship regressions weekly.[^5] I split it out
rather than centering it only because the funnel/cohort/transcript machinery
generalizes beyond the AI layer.

**Jeremy Howard** would push back on any whiff of statistical theater — he is
allergic to teams performing rigor they do not have the data to support. He would
endorse the "A/B is a scale tool, below threshold use judgment and transcripts"
framing and would add: the fastest learners iterate in tight loops with cheap,
honest signals and treat statistical significance as a luxury they earn at scale,
not a gate they impose too early.[^9]

## Further reading

**Must-read**

- Ronny Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments*
  (2020). The standard text; read at least the chapters on power and the perils
  of peeking.[^1]
- Hamel Husain's evals writing, for prompt-iteration-as-product and the golden
  set.[^5]

**Recommended**

- Optimizely, "The New Stats Engine" / the peeking-problem writeup, for why naive
  stopping lies.[^2]
- Reforge, "Don't Let Your North Star Metric Deceive You," for the
  local-maximum trap.[^7]

**Optional**

- Lenny Rachitsky's Duolingo case, read as a cohort-analysis story.[^4]

## Citations

[^1]: Ron Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments:
A Practical Guide to A/B Testing* (Cambridge University Press, 2020) — sample-size
and power: detecting small effects needs thousands-to-tens-of-thousands per
variant; most teams underpower. https://experimentguide.com/ (search-verified
2026-07-17; corroborated by Kohavi's widely-cited "Seven Rules of Thumb for Web
Site Experimenters," KDD 2017.)
[^2]: Optimizely, "The New Stats Engine" / peeking-problem analysis — naive
"stop when significant" inflates false-positive rate well beyond 5%.
https://www.optimizely.com/insights/blog/the-new-stats-engine/ (search-verified
2026-07-17; corroborated by Evan Miller, "How Not to Run an A/B Test,"
https://www.evanmiller.org/how-not-to-run-an-ab-test.html).
[^3]: Startup Genome, "Premature Scaling" (2011) — heavyweight process before
product/market fit is optimizing the wrong thing.
https://s3.amazonaws.com/startupcompass-public/StartupGenomeReport2_Why_Startups_Fail_v2.pdf
(search-verified 2026-07-17.)
[^4]: Lenny Rachitsky, "How Duolingo reignited user growth."
https://www.lennysnewsletter.com/p/how-duolingo-reignited-user-growth — engagement
cohorts moved by habit-loop changes. (search-verified 2026-07-17.)
[^5]: Hamel Husain, "Your AI Product Needs Evals" and evals FAQ — golden sets,
reading data, prompt iteration as the product loop.
https://hamel.dev/blog/posts/evals/ (search-verified 2026-07-17.)
[^6]: Current model landscape (new mid-tier default + frontier tier; per-feature
routing is a live cost/quality decision) per course landscape refresh.
`vault/00-program/_refresh-2026-07-master-report.md`, cross-cutting theme 1.
(search-verified 2026-07-17; two-source verification in the master report.)
[^7]: Reforge, "Don't Let Your North Star Metric Deceive You" — local-maximum
trap from over-optimizing one metric.
https://www.reforge.com/blog/north-star-metric-growth (search-verified 2026-07-17.)
[^8]: Michael Seibel (Y Combinator), "Launch fast" / talk-to-users guidance —
early founders overinvest in metrics as a substitute for user contact.
https://www.ycombinator.com/library/6l-how-to-plan-an-mvp (search-verified
2026-07-17; consistent with Seibel's YC "Building Product" talks.)
[^9]: Jeremy Howard (fast.ai) on tight, honest iteration loops and skepticism of
premature statistical formalism. https://www.fast.ai/ (search-verified
2026-07-17; consistent with fast.ai's iterative, baseline-first pedagogy.)

_last_verified: 2026-07-17_
