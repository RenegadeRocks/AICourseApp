---
type: lesson
block: block-7-onboarding-tracking
week: week-18
session_slug: aquire-leads-using-paid-ads
day_of_cycle: 6
day_name: sat
date_due: 2026-09-19
tags:
  - build
  - lead-magnet
  - opt-in-funnel
  - distribution-plan
  - paid-test
  - code-lab
sources:
  - digitalapplied-lead-magnet-benchmarks-2026
  - chronos-gmail-yahoo-2026
  - getryze-meta-minimum-budget-2026
  - dojoai-meta-attribution-2026
  - optimyzee-advantage-plus-2026
last_verified: 2026-07-17
word_count_target: 4000
---

# BUILD: the lead-gen engine + a disciplined paid test

## Why this matters

Five days of concepts converge into one artifact you will own by tonight: a
working demand-capture engine for your product, with a paid test disciplined
enough that it produces a decision instead of a bill. This is the Week 18
capstone. You will ship four connected components (an AI-native lead magnet, an
opt-in funnel with a welcome sequence, a two-week organic distribution plan, and
a minimum-viable paid-ads test with a pre-registered kill/scale rule) and use
`code-lab/1` to compute the ratios so you cannot fool yourself with vanity
totals. The deliverable is not a plan deck. It is a live magnet, a live funnel,
and a written decision rule you would defend to an investor.

## Prerequisites

- Every lesson this week: [[01-mon-lead-magnets-that-convert|Mon]],
  [[02-tue-opt-in-funnel-and-list-hygiene|Tue]],
  [[03-wed-organic-distribution-engine|Wed]],
  [[04-thu-paid-ads-honest-primer|Thu]],
  [[05-fri-campaign-mechanics-and-measurement|Fri]]. Today assembles them.
- The `code-lab/1` calculator (in this folder). Run its pass bar first if you
  have not: `python test_funnel_metrics.py` should print `OK — 14 tests passed`.
- Your unit economics from
  [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/05-fri-revenue-planning-and-unit-economics|B6W16]].
  You cannot set a CAC target without an LTV.

## The build, in four components

Work in order. Each component depends on the one before, and the gate is that
paid (Component 4) is not allowed until the funnel (Components 1-2) demonstrably
converts.

### Component 1 — The AI-native lead magnet (from Monday)

Build the smallest version that keeps a specific promise and delivers complete
value for a narrow scope.

1. **Write the promise first, with a number in it.** "Find the 3 meetings your
   team should kill this week" beats "meeting productivity guide." The promise is
   the headline of everything downstream, and promise/page match is the top
   conversion lever.[^1]
2. **Build the thin tool.** One input, one valuable output, using Claude Code and
   a slice of your existing product. Do not add edge cases. A reliable narrow
   tool beats an ambitious broken one, because a broken magnet destroys trust at
   the moment of the ask.
3. **Design the next step into the output.** The tool's result page ends with the
   single most logical action (start free, book a call, reply). The magnet's own
   output should make that step feel obvious, not bolted on.
4. **Eval it before it ships.** If the output is LLM-generated, run it on 20 real
   inputs and read every one. Count the outputs you would be embarrassed to send.
   If that count is above zero, the magnet is not ready.

**Gate:** ship a magnet where the promise is specific, the output is reliable on
20 test inputs, and the next step is designed in.

### Component 2 — The opt-in funnel + welcome sequence (from Tuesday)

Build the pipe and keep it deliverable.

1. **Wire authentication FIRST.** SPF, DKIM, DMARC on your sending domain, plus a
   one-click `List-Unsubscribe` header. Without these, 2026 bulk mail gets 550
   rejections, and the rest of this component is moot.[^2] Do the plumbing before
   the paint.
2. **Build the opt-in page** on the B4W10 mechanics, with the matched promise
   above the fold and the email captured at the "get your result" step.
3. **Choose double opt-in** if paid traffic will hit this funnel (it will), so
   the highest-abuse channel cannot pollute your complaint rate.
4. **Write the four-email welcome sequence:** deliver instantly, quick win, story
   + proof, bridge to offer. Value before the pitch, or the pitch draws
   complaints that breach the 0.30% ceiling.
5. **Schedule the hygiene:** a 60-90 day sunset rule and real-time email
   validation at capture.

**Gate:** a live funnel where a test signup receives the magnet, the welcome
sequence fires, and you can see the opt-in event in your own instrumentation.

### Component 3 — The two-week distribution plan (from Wednesday)

Fill the top of the funnel organically before you pay for traffic.

1. **Pick your anchor platform** (where your buyer is, from B1W02) and one or two
   repurposing outlets.
2. **Choose two anchor ideas,** one per week, each a slice of the magnet's value.
3. **Run `distribution_planner.py`** to expand each idea into five native
   expressions and a five-day schedule. Edit the briefs into real posts.
4. **Soft-point to the magnet:** value in the post, link in the comment or
   profile, so you do not eat the ~60% link-in-body reach penalty on LinkedIn.
5. **Instrument attribution:** tag opt-ins by source so you learn which content
   fills the list, not which gets likes.

**Gate:** a concrete two-week schedule with dated, drafted posts, each pointing
at the magnet, and a way to attribute opt-ins to each piece.

### Component 4 — The minimum-viable paid test (from Thursday + Friday)

Only after Components 1-3 show the funnel converts organically. If the funnel
does not convert on free traffic, paid will faithfully scale a broken thing, and
today's honest deliverable is "more organic first."

1. **Confirm the three preconditions:** funnel converts, LTV supports a paid CAC,
   you can measure. If any fails, stop here and note why.
2. **Pre-register the decision rule.** Using your LTV, set `target_cac`,
   `scale_below`, `kill_above`, `min_spend`, and `min_customers` in
   `PaidTestRule` *before you spend*. This is the whole discipline in one object.
3. **Size the test to learn.** Enough budget to give the platform's algorithm
   ~50 conversions/ad set/week and to reach `min_spend` with `min_customers`.
   If you cannot fund it to significance, you are not ready; do more organic.[^3]
4. **Wire CAPI** so conversion events fire server-side, recovering attribution
   and feeding the algorithm.[^4]
5. **Ship three distinct creative concepts** (not tweaks), each matched to the
   opt-in page, using AI to produce but rejecting anything that reads as
   machine-made.[^5]

**Gate:** a launched (or launch-ready) test with a written pre-registered rule,
CAPI live, and three concepts, where the go/no-go is arithmetic, not hope.

## Worked example: reading it with the calculator

Assemble the meeting-audit engine and read it honestly. This is the shape your
own deliverable should take.

**Funnel roll-up** (from `funnel_conversion`), two weeks in:

```
visitors->opt_ins      20.0%
opt_ins->confirmed     72.0%
confirmed->trials      25.0%
trials->customers      15.0%
overall visitors->customers: 0.54%
weakest handoff: trials->customers (15.0%)
```

The weakest handoff is trials→customers, not the opt-in. The single highest-
leverage fix is not more traffic or a higher opt-in rate; it is converting
trials to paid. That points at onboarding and the offer, which is next week's
Block 7 territory. Do not pour paid budget into the top of a funnel whose leak is
at the bottom.

**Paid-test reading** (from `paid_test_decision`), against the pre-registered
rule `target_cac=150, scale_below=120, kill_above=200, min_spend=1000,
min_customers=5`:

```
spend $1050, 9 customers, CAC $117 -> SCALE
  CAC 116.67 < scale line 120.00; raise budget ~20-30% every few days,
  hold 30% for new concepts
```

Note what drove the decision: your own customer count (9), not the platform's
modeled ROAS. Had the same spend produced a great-looking CAC on only 4
customers, the rule returns `INSUFFICIENT_DATA`, not `SCALE`, because four
customers is noise. The pre-registration is what stops you from scaling a fluke
or killing a winner on a bad afternoon.

## The deliverable and its pass bar

Produce a one-page lead-gen engine spec plus the live artifacts:

1. **The magnet:** live, specific promise, reliable output, designed next step.
2. **The funnel:** authenticated domain, opt-in page, double opt-in, four-email
   welcome sequence, hygiene scheduled.
3. **The distribution plan:** two weeks, one anchor idea each, five native
   expressions, opt-in attribution wired.
4. **The paid test:** three concepts, CAPI live, and the pre-registered
   `PaidTestRule` written down with numbers derived from your LTV.
5. **The calculator output:** your funnel roll-up (with weakest handoff) and, if
   you spent, your paid-test reading.

**Pass bar:** a lead engine with (a) a live magnet that produced at least one
real opt-in you can see in your instrumentation, (b) a measured opt-in rate (not
a subscriber count), and (c) a paid test with a pre-registered kill/scale rule
whose go/no-go is arithmetic. If your funnel does not yet convert on free
traffic, passing today means *saying so with the numbers* and staying organic,
not running paid anyway. Honesty is the pass condition.

## Common mistakes experts see

1. **Running paid before the funnel converts organically.** Component 4 is gated
   on Components 1-3 for a reason; paid amplifies, it does not create demand.
2. **Skipping authentication.** No SPF/DKIM/DMARC means 550 rejections and a dead
   funnel, whatever else you build.[^2]
3. **Measuring subscriber count instead of opt-in rate.** The count always rises;
   only the ratio tells you if the funnel is healthy.
4. **No pre-registered decision rule.** Deciding after you see results invites
   sunk-cost rationalization and noise-driven panic.[^3]
5. **Trusting platform ROAS over your own customer count.** Reconcile against
   your DB/billing; up to 40-60% of reported conversions can be modeled.[^4]
6. **Pouring paid into the wrong leak.** If the weakest handoff is
   trials→customers, more traffic does not help; fix the leak first.
7. **Shipping a broken or slop magnet.** A hallucinating tool or generic AI
   creative destroys trust at the exact moment of the ask.

## Reflection questions

1. What did your funnel roll-up reveal as the weakest handoff, and does it change
   where you would spend next (more traffic vs fixing conversion)?
2. Did your magnet produce a real opt-in you can see in your own
   instrumentation? If not, what is broken?
3. What are your pre-registered `target_cac`, `scale_below`, and `kill_above`,
   and what LTV number justifies them?
4. If your funnel does not convert on free traffic yet, are you disciplined
   enough to *not* run paid, and to say so with the numbers?
5. Does your best ad creative read as authentically human, or does it have the
   over-polished AI aesthetic that underperforms?
6. What is the one thing you will ship live tonight, however crude, so next
   week's numbers are real?

## My take (reviewer lens)

**Michael Seibel** would want you to ship the crude version of all four
components tonight rather than perfect one. A running funnel that produces real
opt-ins next week beats an elegant spec that produces none. The `code-lab` tools
are deliberately tiny so you can wire estimates today and replace them with real
data next week. Ugly and live beats polished and hypothetical.

**Chip Huyen** would insist the whole engine be instrumented as a system whose
ratios you watch over time, not spot-check once. Opt-in rate, confirmation rate,
CAC, and the funnel roll-up should be a small weekly dashboard, because the
failure mode is slow drift a one-time measurement misses. Trust your own totals
over the platform's model, and log everything yourself.

**Boris Cherny** would flag the two places founders quietly ship bugs tonight:
the email authentication (a mis-configured DMARC record silently tanks
deliverability) and the CAPI conversion pipeline (duplicate or mis-mapped events
corrupt the CAC you are about to trust). Test both end to end with known events
before you believe a single number. A measurement system you have not verified
lies with confidence.

## Further reading

**Must-read**

- This week's [[05-fri-campaign-mechanics-and-measurement|Friday lesson]] for the
  attribution and decision-rule discipline the paid test depends on.

**Recommended**

- get-ryze Meta minimum-budget guide for sizing the test to actually learn.[^3]
- DOJO AI Meta attribution 2026 for the CAPI setup.[^4]

**Optional**

- Digital Applied lead-magnet benchmarks for opt-in-rate targets by format.[^1]

## Citations

[^1]: Digital Applied, "Lead Magnet Conversion Benchmarks 2026" — promise/page
match is the top lever; opt-in-rate ranges by format.
https://www.digitalapplied.com/blog/lead-magnet-conversion-benchmarks-2026-b2b-data-reference
(search-verified 2026-07-17; corroborated by Amra & Elma; fetch egress-blocked —
liveness pass pending).
[^2]: Chronos Agency, "Gmail & Yahoo Sender Requirements 2026" — SPF/DKIM/DMARC
required, 550 rejections for non-compliant bulk mail, one-click unsubscribe.
https://chronos.agency/blog/gmail-yahoo-email-sender-requirements-2026/
(search-verified 2026-07-17; corroborated by Red Sift / PowerDMARC).
[^3]: get-ryze, "Meta Ads Minimum Budget 2026" — ~50 conversions/ad set/week to
exit learning; size the test to significance or do not run it.
https://www.get-ryze.ai/blog/meta-ads-minimum-budget-guide-starting-budget
(search-verified 2026-07-17; corroborated by Stackmatix).
[^4]: DOJO AI, "Meta Ads Attribution in 2026" — CAPI + pixel, reconcile against
your own customer count; 40-60% of reported conversions can be modeled.
https://www.dojoai.com/blog/meta-ads-attribution-2026-changes-fixes
(search-verified 2026-07-17; corroborated by Stackmatix / adlibrary).
[^5]: Optimyzee, "Meta Advantage+ Guide 2026" — feed the automated engine
distinct creative concepts; use AI to produce but keep it human-feeling.
https://www.optimyzee.com/blog/meta-advantage-plus-guide-2026 (search-verified
2026-07-17; corroborated by Digital Applied Meta AI ads guide).

_last_verified: 2026-07-17_
