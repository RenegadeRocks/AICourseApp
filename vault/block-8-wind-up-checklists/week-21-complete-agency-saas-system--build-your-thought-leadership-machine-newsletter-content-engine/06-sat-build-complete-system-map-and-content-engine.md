---
type: lesson
block: block-8-wind-up-checklists
week: week-21
session_slug: complete-agency-saas-system
day_of_cycle: 6
day_name: sat
date_due: 2026-10-10
tags:
  - build
  - system-map
  - content-engine
  - newsletter
  - code-lab
  - capstone-build
sources:
  - beehiiv-substack-ghost
  - storyteq-atomization
  - gawande-checklist-manifesto
  - hamel-evals
last_verified: 2026-07-17
---

# BUILD: the complete-system map + the content engine

## Why this matters

This is the week's payoff. Two artifacts, both real, both leaving this session
done. First, a one-page map of your entire business with no orphan subsystems —
every box has a metric, an owner, an SOP, and a wikilink to the course week that
built it. Second, a running content engine: a platform live, a POV as its spine,
a four-week calendar, one issue drafted in your own voice, and the measurement
loop wired up. When you finish, you can see your whole business on one page and
you have a compounding demand engine that runs on a schedule. The code in
`code-lab/1` generates and validates both.

## Prerequisites

- [[01-mon-the-complete-system-assembling-blocks-0-7|Mon · the complete system]] — the subsystems, handoffs, and dashboard you now formalize.
- [[04-thu-the-newsletter-and-content-engine|Thu · the content engine]] — the platform choice and pipeline you now stand up.
- [[05-fri-content-ops-and-the-ai-assisted-line|Fri · content ops]] — the quality bar every issue must pass.

## The build, part 1: the complete-system map

### Step 1: enumerate your subsystems

Use the three-subsystem cut from Monday: demand, delivery, money. For a simple
business that is exactly three boxes. If yours genuinely has more (a distinct
product subsystem, a separate community), add them, but resist inflation — most
readers have three. For each subsystem write four things:

- **The one metric** that tells you it is healthy (leads/week; time-to-first-
  value and retention; net revenue retention and runway).
- **The owner** — one name, even if the name is yours for now. Ownerless
  subsystems rot, exactly as ownerless SOPs do ([[block-7-onboarding-tracking/week-20-sops-for-onbaording-delivery-growth--build-community-paid-inner-circle/01-mon-sops-the-operating-system-of-a-scaling-business|B7W20]]).
- **The SOP** that runs it — a pointer to the runbook, not the runbook itself.
- **The `built_in` wikilink** — the exact course week that built this capability.
  This is the integration test: if you cannot name the week, you have a gap in
  your understanding, not just your map.

### Step 2: draw the handoffs as a closed loop

Add a `handoff_to` for each subsystem so value flows in a loop: demand hands off
to delivery, delivery to money, money back to demand (via the referral and
case-study loop from [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/04-thu-referral-and-virality-engineering|B6W17]]). A subsystem with no outbound handoff is a dead end; one with no inbound is starved. The validator flags both.

### Step 3: run the validator

Encode your map as JSON (copy `system.example.json`) and run:

```bash
cd code-lab/1
python planner.py system my-system.json
```

The tool prints your map and a completeness checklist. Any subsystem missing a
metric, owner, SOP, or `built_in` wikilink shows as an unchecked box with the
exact field named. Any handoff dead-end is flagged. The pass bar is literal:
`PASS — no orphan subsystems`. If you see `FAIL`, the tool has just told you the
precise gap in your business. Fix the map by fixing the business (or by honestly
recording that the SOP does not exist yet and belongs on your backlog).

This is the Gawande checklist principle applied to your whole company: the value
is not the beautiful document, it is that the checklist makes an omission
impossible to skip past.[^1]

## The build, part 2: the content engine

### Step 1: pick the platform and go live (30 min)

Decide in an hour, not three weeks. beehiiv or Ghost if you are building a
newsletter business and want to keep the platform fee; Substack if simplicity and
its discovery network matter more than the 10% cut while you start; Kit if you
want automations and a generous free tier.[^2] Sign up, connect your domain,
import the opt-in list you built in [[block-7-onboarding-tracking/week-18-create-a-lead-magnet-using-social-media-distribution--aquire-leads-using-paid-ads/02-tue-opt-in-funnel-and-list-hygiene|B7W18]]. Live means live: a real publication a stranger can subscribe to today.

### Step 2: set your POV as the spine (15 min)

Take the Level-3 POV you sharpened on [[03-wed-the-thought-leadership-thesis|Wednesday]] and make it the newsletter's reason to exist. Name the newsletter so the name signals the POV. Write the one-sentence promise a subscriber is opting into. This is the spine; every issue is a vertebra on it.

### Step 3: generate the calendar and repurposing matrix (20 min)

Fill in `engine.example.json` with your real cadence (14 days, biweekly, is the
sustainable default), your first four pillar ideas, and your channels. Run:

```bash
python planner.py engine my-engine.json
```

You get a dated content calendar (each pillar plus its atomized derivatives
across the following days) and a repurposing matrix (each pillar down the side,
each channel across the top). This is the one-pillar-many-assets loop from
[[04-thu-the-newsletter-and-content-engine|Thursday]] made concrete: you now know exactly what to publish, when, derived from what.[^3]

### Step 4: draft one issue, human-voiced (45 min)

Pick pillar one. Voice-memo the story, have AI structure it from your issue
template, then run the Friday human gate: strip the machine tells, inject the
specifics only you have, add the arguable point, read it aloud. Then run it
through your four-question quality rubric — the content eval from
[[05-fri-content-ops-and-the-ai-assisted-line|Friday]].[^4] It ships only if it passes all four. This is the issue you publish (or schedule) today.

### Step 5: wire up measurement (10 min)

Enter your baseline numbers (list size, opens, sent, clicks/replies, downstream
conversions) into the engine config and run it again. The health report shows the
four metrics with pass/fail flags and names any metric to investigate. Baseline
set. The engine now has a dashboard, and you apply the same leading/lagging
discipline as [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/01-mon-product-analytics-for-ai-products|B5W14]]: growth and open weekly, conversion monthly.

## Pass bar

You are done when both are true:

1. `python planner.py system my-system.json` prints `PASS — no orphan
   subsystems`, and every `built_in` field points to a real course week.
2. You have a publishable first newsletter issue, live or scheduled, that
   passes your four-question quality rubric, and a stranger reading it would not
   flag it as AI slop.

If either fails, you have a precise, named thing to fix, which is the entire
point of building the artifacts.

## Worked example: Priya's Saturday

Priya (the recurring law-firm-AI operator) runs both builds in an afternoon.

**System map.** Three subsystems. Encoding them surfaces exactly the gaps from
Monday: her money subsystem has no owner (she and her partner both assume the
other is watching invoicing), so the validator flags it. She fixes it by
assigning herself as owner and writing a one-line renewal-and-upsell SOP. She
also had no `handoff_to` from delivery back to demand — the missing referral loop
— so she adds the case-study SOP as the handoff. Now the map passes, and the two
biggest leaks in her business are closed as a side effect of making the map pass.

**Content engine.** beehiiv, live in fifteen minutes, list imported. "The
Retrieval Gate" as the name and spine. Four pillars from her idea inbox into the
planner; a biweekly calendar and repurposing matrix come out. She drafts issue
one (the hallucinated-citation story) through the human gate, runs the rubric,
passes, schedules it. Baseline metrics entered: the engine reports HEALTHY. In
one afternoon she has a validated business map and a running demand engine. The
week delivered exactly what it promised.

## Common mistakes experts see

1. **A map with orphan boxes.** A subsystem missing a metric, owner, or SOP is
   the tool telling you where your business is undefined. Do not fake the fields;
   fix the gap or record it on your backlog.
2. **`built_in` you cannot fill.** If you cannot name the week that built a
   capability, you have a knowledge gap. Go find the week; that is the
   integration the whole block is testing.
3. **A handoff loop that does not close.** If money does not hand back to demand,
   you have no referral loop and your machine is a line, not a flywheel.
4. **Over-optimizing the platform.** An hour, not three weeks. Shipping beats
   comparing.
5. **Shipping the AI draft to hit the deadline.** The one issue you draft today
   must pass the human gate and the rubric. A slop first issue teaches your new
   list to ignore you from message one.
6. **Skipping measurement.** An engine with no baseline cannot be improved. Ten
   minutes now saves you flying blind for months.

## Reflection questions

1. When your system map first ran, what did the validator flag? What did fixing
   that flag force you to change about the actual business, not just the JSON?
2. Which `built_in` wikilink was hardest to fill, and what does that say about
   where your understanding is thinnest?
3. Does your handoff loop close? If money does not flow back to demand, what is
   your plan to build the referral loop that closes it?
4. Read your first issue aloud one more time. Where does it still sound like a
   model, and are you shipping it anyway because you are tired?
5. What did your engine-health baseline reveal? Which metric will you watch
   first, and what number would trigger you to act?

## My take (reviewer lens)

**Boris Cherny**, whose current work is fleet-scale agent management, would treat
the system-map validator as the interesting artifact: it is a schema check on
your business, and the value is exactly that it fails loudly on missing fields.
His correction is to make the check *stricter* over time — add fields for "single
point of failure?" and "survives the next model release?" so the validator forces
the hard questions, not just the bookkeeping ones. A check that always passes is
a check that is not checking anything.

**Jerry Liu** would push on the repurposing matrix: the mechanical
one-pillar-to-many transformation is where AI genuinely helps, but the quality of
the derived assets is bounded by the retrieval-and-grounding quality of the
pillar. If the pillar is specific and well-sourced, the atomized pieces inherit
that; if it is thin, atomization multiplies the thinness across five channels.
His correction mirrors Thursday's: spend the effort on the pillar, let the
derivatives be mechanical.

**Michael Seibel** would ask the only question that matters: did you publish?
Not "did you build a lovely map" but "is there a live newsletter issue a stranger
can read." He would be ruthless about the failure mode where the reader spends
the afternoon perfecting the JSON and never hits publish. The map is
instrumentation; the published issue is the business. If you finish today with a
passing map and no live issue, you optimized the wrong artifact.

## Further reading

**Must-read**

- Re-read [[04-thu-the-newsletter-and-content-engine|Thursday]] and [[05-fri-content-ops-and-the-ai-assisted-line|Friday]] as you build — this session is their execution.

**Recommended**

- Atul Gawande, *The Checklist Manifesto* — the principle behind the system
  validator: make omissions impossible to skip.[^1]

**Optional**

- The 2026 platform fee comparisons, if you are still deciding where to publish.[^2]

## Citations

[^1]: Atul Gawande, *The Checklist Manifesto*.
https://atulgawande.com/book/the-checklist-manifesto/ — checklists make expert
omissions impossible to skip; the principle behind the system-map validator.
(Evergreen; corroborated by NIH PMC review
https://pmc.ncbi.nlm.nih.gov/articles/PMC4953332/.)
[^2]: "Newsletter Platform Fees Compared (2026)," That Marketing Buddy.
https://thatmarketingbuddy.com/blog/newsletter-platform-fees-compared — Substack
10% platform fee; beehiiv/Ghost 0% on paid plans; Kit ~3.5% bundled.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending;
corroborated by beehiiv.com/blog/substack-vs-ghost.)
[^3]: "Content Repurposing Strategy: The 2026 Framework," Tugan.ai.
https://www.tugan.ai/blog/content-repurposing-strategy — one pillar atomized into
many native assets across channels and time. (search-verified 2026-07-17;
corroborated by storyteq.com/blog/what-is-content-atomization-in-scalable-production.)
[^4]: Hamel Husain, "Your AI Product Needs Evals." https://hamel.dev/blog/posts/evals/
— the eval discipline behind the four-question content quality rubric.
(Evergreen; canonical.)

_last_verified: 2026-07-17_
