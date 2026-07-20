---
type: lesson
block: block-6-launch-monetization
week: week-17
session_slug: growth-hacking-referral-loops
day_of_cycle: 6
day_name: sat
date_due: 2026-09-12
tags:
  - build
  - growth-system
  - pmf-survey
  - re-engagement-sequence
  - growth-loop
  - referral-mechanic
  - k-factor
  - code-lab
sources:
  - firstround-superhuman-pmf-engine
  - reforge-growth-loops
  - getlaunchlist-kfactor-guide
  - voucherify-referral-fraud
  - andrewchen-shitty-clickthroughs
  - viralloops-dropbox-3900
  - amplitude-hidden-roi-winback
  - baincapital-elena-verna-plg
last_verified: 2026-07-17
word_count_target: 3600
---

# BUILD: assemble your product's growth system

## Why this matters

Five days of concepts converge here into one artifact you will actually own by
the end of today: a growth system for your product, with a measurable loop and
projections honest enough that you would show them to an investor without
flinching. This is the Block 6 capstone build. You will produce four connected
components (a feedback loop, a re-engagement sequence, one instrumented growth
loop, and a referral mechanic with real k-factor math and fraud guards) and use
the `code-lab/1` simulator to project the loop with saturation instead of the
fantasy straight line. The deliverable is not a deck. It is a spec plus numbers
you can defend.

## Prerequisites

- Every lesson this week: [[01-mon-the-feedback-engine|Mon]],
  [[02-tue-retargeting-and-re-engagement|Tue]],
  [[03-wed-growth-loops-vs-funnels|Wed]],
  [[04-thu-referral-and-virality-engineering|Thu]],
  [[05-fri-the-growth-system-and-honest-measurement|Fri]]. Today assembles them.
- The `code-lab/1` simulator (in this folder). You will run it against your own
  numbers. If you have not run it yet, do the README pass bar first.

## The build, in four components

You are building the system diagram from Friday, made concrete for your product.
Work through the four components in order, because each depends on the one before.

### Component 1 — The feedback loop (from Monday)

The engine that keeps your product worth spreading. Build the smallest honest
version:

1. **Instrument the Sean Ellis survey.** One question ("How would you feel if you
   could no longer use [product]?"), fired only at recently-active users who have
   hit core value, three options. Wire it so responses carry a `segment` tag
   (persona, plan, or use-case). Do not average blindly; you will segment.
2. **Tag one qualitative channel.** Pick your richest channel (support queue,
   cancel survey, or reviews) and add a problem-category tag to every item so
   "feelings" become counts. Run the `feedback_triage.py` pattern from Monday as
   a deterministic pre-pass before any LLM clustering.
3. **Wire the closing stage.** A place to record "shipped because users asked"
   and "declined because." This is what makes the loop compound and what fires
   Tuesday's highest-converting win-back trigger.

Run `pmf_analyzer.py` on your real (or best-estimate) survey data. The output you
need: your aggregate PMF score, your per-segment scores, and your
high-expectation segment. **This gates everything else.** If no segment clears
40%, today's honest deliverable is "go back to the product," and that is a real,
valuable result, not a failure.

### Component 2 — The re-engagement sequence (from Tuesday)

The system that plugs the leak. Specify:

1. **Lifecycle thresholds** matched to your product's natural cadence: when is a
   user new, active, dormant, churned? Write the exact day/behavior boundaries.
   Get this wrong and you nag active users.
2. **Two triggers, not a blast.** Pick the two highest-leverage triggers you can
   actually fire: almost always an approaching-dormancy nudge plus a
   you-asked-we-fixed message (which reuses Component 1's closing stage).
3. **The honesty guards, wired first.** A hard frequency cap, instant
   unsubscribe, cancellation as easy as signup. Use the `reengagement.py`
   structure from Tuesday where guards suppress *before* targeting decides. If you
   would be embarrassed to read the flow aloud in a deposition, redesign it.

### Component 3 — One instrumented growth loop (from Wednesday)

Not four loops. One. Choose your product's dominant loop (for most AI products
built in this course, it is either the collaboration/viral loop or the
output-as-marketing content loop). Then instrument it:

1. **Name the input, process, and output explicitly.** "Active user → shares a
   watermarked artifact → recipient clicks through and signs up." If you cannot
   write this sentence, you have a funnel, not a loop.
2. **Measure the handoffs.** Estimate each conversion step and feed them to
   `loop_efficiency()`. The tool returns your loop amplification and, more
   usefully, your weakest handoff, which is the one place to push.
3. **Instrument cycle time.** How many days for one full turn? This is co-equal
   with amplification and usually more improvable.

### Component 4 — The referral mechanic (from Thursday)

Only if Component 1 showed a real "very disappointed" core. If it did not, skip
this and note why; building referral below PMF is the week's cardinal sin.

If you did clear the bar:

1. **Four incentive decisions.** Double-sided (almost always), reward = more of
   your product if possible (Dropbox, not PayPal), ask at the moment of delight,
   and remove every step of friction.
2. **The k-factor math, honest.** Estimate refer-rate, invites-per-referrer, and
   invite-conversion; run `k_factor()`; read the regime honestly (you will almost
   certainly be below 1). Then run `project_viral()` with your addressable market
   so the projection saturates instead of running to infinity.
3. **Fraud guards.** At minimum: reward a retained action, not a signup. Add
   IP/device matching and velocity limits only if the fraud data later demands
   it (do not over-engineer a detector for fraud you do not have).

## Worked example: assembling it for the meeting-notes product

Here is the full assembly, end to end, using the `code-lab` tools. This is the
shape your own deliverable should take.

**Component 1 output** (from `pmf_analyzer.py`):

```
AGGREGATE (n=120): very=34%  somewhat=41%  not=25%  PMF=False
BY SEGMENT:
  team_manager  n=38  very=58%  PMF=True     <- high-expectation segment
  solo_user     n=52  very=21%  PMF=False
  student       n=30  very=27%  PMF=False
NEXT MOVE: Aggregate 34% < 40%, BUT segment 'team_manager' is at 58%.
           Focus on 'team_manager', fix fence-sitters' blockers, re-measure.
```

The aggregate is a mediocre 34%. Averaging would tell you to fix the product
broadly or worse, to grow harder. The segmentation tells the true story: team
managers love it (58%, well past PMF), while solo users and students do not. This
is the Superhuman situation exactly. The decision falls out of the data: **grow
into the team-manager segment**, protect what they love, and address the specific
blockers keeping team-manager fence-sitters from "very disappointed." Do not chase
solo users and students who were never going to love a team product.[^1]

**Component 3 output** (from `loop_efficiency()`), scoped to the team-manager
collaboration loop:

```
handoffs: produces_shared_note=0.65, invites_teammate=0.35, teammate_signs_up=0.72
amplification: 0.164 users-out per user-in
weakest handoff: invites_teammate (0.35)
lift invites 0.35->0.55 adds 0.094 to amplification (more than doubling it)
```

The weakest handoff is the invite step. The single highest-leverage change is not
better signup conversion (already 72%) or better output (already 65% share); it is
getting more team managers to actually invite a teammate. That points to a product
change: prompt the invite at the moment a shared note is created, when the value
is fresh. This is where the loop and the moment-of-delight referral timing
converge.

**Component 4 output** (from `k_factor()` and `project_viral()`), referral layered
on the team-manager segment:

```
k = k_factor(refer_rate=0.35, invites_per_referrer=2.5, invite_conversion=0.18) = 0.158
regime: "where most successful companies land"

project_viral(starting=800 team-managers, base_k=0.158, cycle=10 days,
              market=25_000, cycles=10):
  saturates around ~950 users; adds ~150 over the base, NOT a hockey stick.
```

Honest projection: a k of 0.158 on 800 team-manager accounts adds roughly 150
users through referral over ten cycles, then flattens as the segment saturates.
That is a real 15-to-20% amplification of your team-manager growth, not
transformational, and worth building *because* the segment already loves the
product. If Component 1 had shown no segment above 40%, this entire component would
be a fraud magnet on a leaky bucket, and the honest deliverable would have been to
delete it.

## The deliverable and its pass bar

Produce a one-page growth-system spec for your product containing:

1. **The input-metric tree** with the retention multiplier explicitly in the
   middle (Friday).
2. **Your PMF segmentation result** and the resulting grow-or-fix decision.
3. **The re-engagement sequence**: thresholds, two triggers, honesty guards.
4. **Your dominant loop**: input/process/output named, amplification and cycle
   time measured, weakest handoff identified.
5. **The referral math** (or an explicit note that you skipped it because you are
   below PMF), with a saturating `project_viral` projection, not a straight line.

**Pass bar:** a growth system with (a) at least one loop whose amplification and
cycle time you measured, (b) a saturating projection you would defend to an
investor, and (c) a stated stopping condition, the signal that would make you
abandon growth work and return to the product. If your PMF segmentation says "go
back to the product," passing today means *saying so with the data*, not building
a referral program anyway. Honesty is the pass condition.

## Common mistakes experts see

1. **Building the referral mechanic despite a sub-40% product.** The tools will
   compute a k for you regardless; your judgment must refuse to build on a leaky
   bucket. Component 1 gates Component 4.
2. **Averaging the PMF survey instead of segmenting.** A 34% aggregate hid a 58%
   core. The segment is the signal.[^1]
3. **Projecting a constant k.** Use `project_viral` with your real addressable
   market so the curve saturates. A straight-line projection is the classic
   growth-planning lie.[^2]
4. **Optimizing the strongest handoff.** The weakest handoff moves the loop most.
   Let `loop_efficiency` tell you where to push, not your gut.
5. **Re-engagement without honesty guards wired first.** If a targeting rule can
   override a frequency cap or an unsubscribe, you built a dark pattern. Guards
   come first in the code and in the design.[^3]
6. **Confusing the deliverable with a real system.** The spec is a plan; the
   system is instrumented and running. Ship the instrumentation this week, even
   if crude, so next week's numbers are real.

## Reflection questions

1. What did segmenting your PMF survey reveal that the aggregate hid? Did it
   change your grow-or-fix decision?
2. What is your dominant loop's weakest handoff, by measurement not intuition, and
   what is the cheapest product change to move it?
3. Run `project_viral` with your real addressable market. How far below your naive
   straight-line projection does the saturating curve land, and what does that do
   to your growth plan?
4. Is your re-engagement sequence one you would be proud to have read aloud in a
   deposition? Where is it closest to the line?
5. What is your stated stopping condition, and is it instrumented well enough that
   you would actually notice it and act?

## My take (reviewer lens)

**Michael Seibel** would want you to ship the crude version of all four components
this week rather than perfect one, because a running system that produces real
numbers next week beats an elegant spec that produces none. He is right. The
`code-lab` tools are deliberately tiny so you can wire estimates today and replace
them with real data next week, rather than waiting for a perfect analytics stack.
Ugly and instrumented beats polished and hypothetical.

**Boris Cherny** would flag that the referral fraud guards are the component most
likely to be over-built: teams reach for IP/device fingerprinting and risk
scoring on day one, ship false positives that block legitimate household users,
and burn a week on fraud they do not yet have. Start with rewarding a retained
action, which removes most of the incentive with none of the false-positive risk,
and add detection only when fraud data proves you need it.[^3]

**Elena Verna** would push on whether your "loop" is actually a loop or a
disguised funnel: the test is whether the output genuinely reinvests into the
input, and many teams draw a loop diagram around what is really a one-directional
acquisition step.[^4] If turning off paid spend would stop your loop cold, it was
never a loop. Run the "what happens when I stop?" test from Friday against your
Component 3 before you call it done.

## Further reading

**Must-read**

- Rahul Vohra, "How Superhuman Built an Engine to Find Product/Market Fit," for
  the segmentation-drives-the-decision logic that gates today's build.[^1]

**Recommended**

- Reforge, "Growth Loops are the New Funnels," for the loop-vs-funnel test to run
  against your Component 3.[^4]
- Viral Loops, "Dropbox Grew 3900% With a Simple Referral Program," for the
  product-as-reward pattern to copy in Component 4.[^5]

**Optional**

- Voucherify, "How to Combat Referral Abuse and Fraud," for the minimal fraud
  guards.[^3]

## Citations

[^1]: Rahul Vohra, "How Superhuman Built an Engine to Find Product/Market Fit,"
First Round Review. https://review.firstround.com/how-superhuman-built-an-engine-to-find-product-market-fit/
— segment the PMF survey; grow into the high-expectation segment. (search-verified
2026-07-17; fetch egress-blocked — liveness pass pending; corroborated by Reforge
summary.)
[^2]: Andrew Chen, "The Law of Shitty Clickthroughs" / "Braindump on viral loops."
https://andrewchen.com/the-law-of-shitty-clickthroughs/ — saturation lowers
effective k; constant-k projections mislead. (search-verified 2026-07-17.)
[^3]: Voucherify, "How to Combat Referral Abuse and Fraud."
https://www.voucherify.io/blog/blowing-the-whistle-how-to-combat-referral-abuse-and-fraud
— reward retained actions; add IP/device/velocity checks only as needed.
(search-verified 2026-07-17; corroborated by Buyapowa.)
[^4]: Brian Balfour et al. / Elena Verna, "Growth Loops are the New Funnels,"
Reforge. https://www.reforge.com/blog/growth-loops — the output-reinvests test for
a real loop vs a funnel. (search-verified 2026-07-17; corroborated by Verna via
Bain Capital Ventures.)
[^5]: Viral Loops, "Dropbox Grew 3900% With a Simple Referral Program."
https://viral-loops.com/blog/dropbox-grew-3900-simple-referral-program/ — give-and-get
product reward; k ≈ 0.5. (search-verified 2026-07-17; corroborated by First Round
k-factor glossary.)

_last_verified: 2026-07-17_
