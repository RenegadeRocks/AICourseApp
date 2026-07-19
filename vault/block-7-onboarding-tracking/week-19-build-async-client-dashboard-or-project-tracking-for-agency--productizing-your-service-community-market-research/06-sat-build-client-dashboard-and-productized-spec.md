---
type: lesson
block: block-7-onboarding-tracking
week: week-19
session_slug: build-client-dashboard-productized-spec
day_of_cycle: 6
day_name: sat
date_due: 2026-09-26
tags:
  - build
  - client-dashboard
  - productized-spec
  - community-research-plan
  - capacity-model
  - code-lab
sources:
  - supabase-rls-docs
  - manyrequests-productized-guide
  - reddit-responsible-builder-policy
  - assembly-client-portal
  - digitalapplied-ai-pricing-2026
last_verified: 2026-07-17
word_count_target: 2300
---

# BUILD: client dashboard + productized-service spec + community-research plan

## Why this matters

Five days of concepts converge into three artifacts you own by tonight: a working
client dashboard a real client could log into, a productized-service spec a
stranger could buy, and a community-research plan you could start Monday. This is
the Week 19 capstone. The deliverable is not notes; it is a running backend, a
buy-page-ready offer with an honest capacity model, and a listening plan with a
disconfirming question in it. Everything you build today is for *your* business,
not a hypothetical one.

## Prerequisites

- Every lesson this week:
  [[01-mon-the-async-client-dashboard|Mon]],
  [[02-tue-building-the-dashboard|Tue]],
  [[03-wed-productizing-your-service|Wed]],
  [[04-thu-delivery-systems-and-the-ai-augmented-team|Thu]],
  [[05-fri-community-driven-market-research|Fri]].
- The `code-lab/1` package in this folder. Run its README pass bar first: nine
  offline tests and the `seed.py` demo. You will adapt it to your own business.

## The build, in three artifacts

Work in order. Each depends on the one before: the dashboard makes your delivery
visible, the productized spec defines what you deliver, and the community plan
tells you what to productize next.

### Artifact 1 — The client dashboard (working, not a mockup)

Adapt `code-lab/1` to your business. You have two honest paths, and Monday's
build-vs-buy decision chooses between them:

**Path A (buy, then skip to the data):** if you decided to buy (the right default
for a handful of clients), stand up Assembly, ManyRequests, or SPP this morning,
create one real client, and populate the four Monday sections (Progress,
Deliverables, Metrics, Next steps). Your "build" today is the *configuration and
the retirement script*: the portal populated with a real client's real data, and
the message that converts that client's status meeting to the dashboard. Then
spend the rest of the day on Artifacts 2 and 3.

**Path B (build, to own it):** adapt the code-lab. Concretely:

1. **Model your data.** Replace the seed clients/projects/deliverables/metrics in
   `seed.py` with one real client and one real project of yours. Pick the *one
   metric* that client would log in to check (Tuesday's hardest question).
2. **Keep the isolation choke point.** Do not scatter tenant filters. The one rule:
   every read is scoped to the caller's `client_id`, failing closed. When you move
   to a real database, port this to Supabase RLS using the README's six-step map
   (enable RLS, JWT `client_id` claim, `USING` policy, index, test-from-SDK, guard
   the service key).[^1]
3. **Wire the read-only client view.** Mark internal deliverables
   `is_client_visible=False`. Confirm a client sees only their approved,
   client-visible work and their "blocked on you" list.
4. **Generate one grounded status summary.** Use `summary.py`. Keep the fact
   assembly deterministic; let the model only phrase it; keep it a *draft* you
   approve. Run offline first (no key), then optionally wire your Anthropic key
   with a cheap model.[^2]
5. **Skin it.** Client logo and brand color from the `client` row. That is v1
   white-labeling.

The pass condition for Artifact 1 is identical on both paths: **a real client
could log in and see their real project, and only theirs.**

### Artifact 2 — The productized-service spec

Take Wednesday's offer design and Thursday's capacity model and produce one spec a
stranger could buy. It has six parts:

1. **The repeatable outcome**, in the buyer's language (Friday's community research
   feeds this): not "AI consulting" but "we connect your support inbox to an AI
   triage-and-draft workflow so your team answers 3x faster."
2. **Fixed scope**: inclusions *and* exclusions. The exclusions hold the price.
3. **Published price and timeline**: one number, one duration, no custom quote.
   Anchor to the 2026 bands (retainers $1.5K–$10K/mo, unlimited $3K–$15K/mo,
   fixed-scope projects in between) then adjust for value.[^3]
4. **The delivery SOP outline**, each step annotated `code | llm | human`, so you
   can see your automation opportunity and your judgment moat at once.
5. **The honest capacity model**: run `pricing.py` with *your* numbers, including
   verification hours. It will refuse a model that prices AI verification at zero.
   Read off your client ceiling, revenue ceiling, and next lever.[^4]
6. **The buy-page description**: scope, price, timeline, included/excluded, and a
   call to action a stranger could act on without a call.

The pass condition: **a stranger could read the buy-page description and purchase
without talking to you, and your capacity model has honest verification hours in
it.**

### Artifact 3 — The community-research plan

Take Friday's listening plan and make it executable. Five parts:

1. **Named targets**: 3–5 communities across at least two platform types (a couple
   of subreddits, a Discord, a Slack, any paid community), where your buyer
   actually is.
2. **Listening questions**, at least three, at least one of which could
   *disconfirm* your offer. If your plan can only confirm you, it is research
   theater.
3. **A capture method**: the sheet (quote / problem / frequency / intent) and the
   AI-clustering step you will run monthly, remembering the model clusters what you
   captured and cannot fix a biased sample.
4. **A give-before-take reciprocity plan** with a timeline: what you will
   contribute, for how long, before you extract anything. This is also your first-
   customer acquisition.
5. **The hand-off to formal validation**: which findings become Week-11-style
   interview hypotheses and a smoke test. Community aims; interviews fire.

Stay inside Reddit's Responsible Builder Policy: manual human reading for your own
research is fine; automated commercial collection needs approval and the API
terms.[^5] The pass condition: **a plan you could start Monday that could kill your
offer, not just cheer for it.**

## Worked example: the full assembly

For the AI support-triage business, end to end, using the code-lab.

**Artifact 1 output** (from `seed.py`, adapted):

```
=== ACME dashboard (client-scoped) ===
visible deliverables: ['Triage workflow v1', 'Reply-draft workflow']
blocked on you: ['Reply-draft workflow']
metrics: [tickets deflected: 312/wk, median response: 3.2 min]

=== Isolation check ===
globex sees only: ['Data pipeline draft']
PASS: no cross-tenant leak; internal deliverable hidden from client

=== Grounded AI status summary (offline draft) ===
[draft/offline] Hi Acme Support, here is your update: work is on track.
Shipped since last update: Triage workflow v1. Results so far: tickets
deflected: 312 /wk; median response: 3.2 min. We are waiting on you for:
Reply-draft workflow.
```

The dashboard shows the client exactly the four sections, hides internal QA notes,
surfaces the "blocked on you" item (which quietly ends the "you never told me"
argument), and the AI drafted the weekly update from real facts, not vibes. Note
what the summary does *not* say: it never claims progress that is not in the data,
because the model only phrased facts the code assembled.

**Artifact 2 output** (from `pricing.py`):

```
offer: AI support-triage build @ $6,000
human hours/client: 12.5 (verification: 3.5)
max clients/period: 2.0   revenue ceiling: $12,000   gross margin: 99%
next lever: raise price (protect your hours) or push more low-judgment steps
            onto AI to shrink hours-per-client
```

The honest story: at $6K and 12.5 human hours per client (3.5 of them
verification), a solo operator with 25 real delivery hours a period tops out
around two concurrent builds. The 99% *gross* margin (revenue minus tooling) is
technically true and deeply misleading, because the binding constraint is your
own hours, not cash cost. That is the Thursday lesson made concrete: efficiency is
high, but capacity is the ceiling, and the model tells you the next lever is price
or more AI, not "hire," because verification is still only 28% of your hours.[^4]

**Artifact 3 output** (the listening plan, abbreviated):

```
targets:   r/CustomerService, r/SaaS, r/msp, one support-ops Discord,
           one B2B-support Slack
questions: (1) words for "our support is drowning"?
           (2) what have they tried and why did it disappoint?
           (3) DISCONFIRM: do they think AI support is garbage customers hate?
capture:   4 weeks, quote/problem/frequency/intent, monthly AI clustering
reciproc.: 4 weeks answering triage questions + one non-promo teardown, first
hand-off:  top 3 problems in top 3 phrases -> interviews + smoke-test page
```

Question 3 is the one that makes it research and not theater: if the communities
are full of "AI support is garbage," I want to find that now, before I build.

## The pass bar for today

You pass Week 19 if you have all three:

1. **A dashboard a real client could log into and see only their project.**
   Bought-and-configured or code-lab-adapted, both count. The isolation must be
   real: a second client cannot see the first's data.
2. **A productized offer a stranger could buy**, with a published price, fixed
   scope (inclusions and exclusions), an SOP outline, and a capacity model with
   honest verification hours.
3. **A community-research plan you could start Monday** with at least one
   disconfirming question and a give-before-take reciprocity plan.

If your dashboard leaks across tenants, your offer needs a call to complete, or
your research plan can only confirm you, you have not passed. Each failure points
at a specific lesson to revisit.

## Common mistakes experts see

1. **Building the dashboard when you should have bought it.** For a few clients,
   configure a bought portal and spend the day on the offer and the research plan.
   Building is a learning exercise, not a business necessity at this scale.
2. **Scattering tenant filters instead of one choke point.** One rule, enforced in
   one place (or in the database via RLS). Scattered filters are how leaks happen.[^1]
3. **An ungrounded AI summary.** If the model can write progress that is not in the
   data, it will eventually lie to a client. Assemble facts in code; let the model
   only phrase them; keep it a draft.[^2]
4. **A capacity model with zero verification hours.** The pricing module rejects
   it, and so should you. Verification is real cost; count it.[^4]
5. **A research plan that can only confirm your offer.** Add the disconfirming
   question or you are doing bias laundering, not research.[^5]
6. **Three half-built artifacts instead of three real ones.** Better a bought
   portal with one real client, a simple published offer, and a five-line research
   plan you will actually run, than three elegant specs you never ship.

## Reflection questions

1. Could a real client log in right now and see only their project? If not, what is
   the exact gap?
2. Would a stranger buy your offer from the page as written, or do they still need
   a call? What would remove the call?
3. What is your true client ceiling from the capacity model with honest
   verification hours, and which lever do you pull at the ceiling?
4. What is the one disconfirming question in your research plan, and are you
   willing to act if the answer is bad?
5. Which of the three artifacts is weakest, and which lesson does that send you
   back to?

## My take (reviewer lens)

**Michael Seibel** would judge the day by one test: did a real person interact
with a real artifact? A dashboard with one real client beats a schema diagram; a
published offer someone could buy beats a pricing theory; a research plan you start
Monday beats a framework. Ship the ugly, real version of all three rather than the
polished version of one. The code-lab is deliberately tiny so you can adapt it in
an afternoon and spend the rest of the day making the offer and the plan real.

**Boris Cherny** would inspect the isolation choke point and the AI-summary
grounding as the two places a demo hides a future incident. The dashboard that
leaks across tenants and the summary that hallucinates progress are both invisible
in a happy-path demo and catastrophic in production. His standard: prove the
failure modes are handled (cross-tenant read fails closed, summary mentions only
real deliverables) with a test, not a click-through. The code-lab's nine tests are
that proof; keep them green as you adapt.

**A cohort peer** who shipped last week would give the most useful nudge: the
three artifacts are one system, and the temptation is to over-invest in the
dashboard (it is the fun code) and under-invest in the offer and the research plan
(they are the business). The dashboard makes delivery visible, but the offer is
what someone buys and the research is what tells you what to build next. Balance
the day accordingly.

## Further reading

**Must-read**

- The `code-lab/1` README — the build spec, the pass bar, and the Supabase RLS
  production map. Read it before you adapt anything.

**Recommended**

- ManyRequests productized guide (Wednesday) — for the offer bands and the
  buy-without-a-call page structure.[^3]
- Supabase RLS docs (Tuesday) — for moving the isolation from the app choke point
  into the database.[^1]

**Optional**

- Reddit Responsible Builder Policy (Friday) — before you automate any community
  collection.[^5]

## Citations

[^1]: Supabase Docs, "Row Level Security."
https://supabase.com/docs/guides/database/postgres/row-level-security — the
production home for the tenant isolation this build demonstrates at the app layer.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending;
corroborated by MakerKit RLS best-practices.)
[^2]: The grounded-summary discipline (assemble facts in code, model only phrases,
draft-then-approve) applies the Week 13 reliability-of-magic pattern. See
[[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/04-thu-reliability-of-magic|Week 13 reliability]].
(evergreen principle; no fast-moving claim.)
[^3]: ManyRequests, "The Productized Service Guide [2026]."
https://www.manyrequests.com/blog/productized-service-guide — pricing bands and
buy-without-a-call structure. (search-verified 2026-07-17; corroborated by
Assembly productized guide.)
[^4]: DigitalApplied, "AI-Era Agency Pricing Models: A 2026 Decision Guide."
https://www.digitalapplied.com/blog/ai-agency-pricing-models-2026-decision-guide —
outcome pricing and the AI-cost-vs-verification-cost split behind the capacity
model. (search-verified 2026-07-17; corroborated by Vendasta AI-workforce margins.)
[^5]: Reddit, "Responsible Builder Policy," Reddit Help.
https://support.reddithelp.com/hc/en-us/articles/42728983564564-Responsible-Builder-Policy
— manual research use permitted; automated commercial collection needs approval.
(search-verified 2026-07-17; corroborated by Reddit Data API 2026 coverage.)

_last_verified: 2026-07-17_
