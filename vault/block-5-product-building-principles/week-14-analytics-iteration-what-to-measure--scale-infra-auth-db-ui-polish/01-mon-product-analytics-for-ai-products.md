---
type: lesson
block: block-5-product-building-principles
week: week-14
session_slug: analytics-iteration-what-to-measure
day_of_cycle: 1
day_name: mon
date_due: 2026-08-17
tags:
  - product-analytics
  - north-star-metric
  - retention
  - activation
  - ai-metrics
  - containment-rate
  - cost-per-active-user
  - quality-drift
sources:
  - reforge-north-star-metrics-2024
  - reforge-north-star-deceive-2024
  - lenny-duolingo-retention-2021
  - startup-genome-premature-scaling-2011
  - digitalapplied-deflection-csat-2026
  - aerochat-deflection-vs-containment-2026
  - nextiva-ai-agent-metrics-2026
  - chip-huyen-ai-engineering-2025
  - amplitude-north-star-saas-2024
  - mollick-one-useful-thing-2026
last_verified: 2026-07-17
word_count_target: 5200
---

# Product analytics for AI products: what to measure when the product thinks

## Why this matters

By Friday of last block you knew how to instrument a launch: the spike, the
funnel, the day-one conversion numbers. That was a photograph. This week is the
movie. A launch tells you whether people will *try* your product. Analytics
tells you whether they will *keep using it*, whether the AI is earning their
trust or quietly bleeding it, and whether each active user costs you three cents
or three dollars in tokens. Those three questions decide whether you have a
business or an expensive hobby.

After this lesson you can pick a north-star metric you can defend to a skeptic,
read a retention curve without fooling yourself, and instrument the six
AI-specific numbers that predict churn before your revenue chart does. You will
also know which metrics are vanity, which are lies, and which one number you
should put on a screen you look at every morning.

## Prerequisites

- [[block-4-test-validate-package/week-10-build-landing-page-with-cta-recap--create-ai-generated-launch-creatives/05-fri-launch-day-instrumentation|Launch-day instrumentation]]
  (Block 4). That is the canonical home for launch funnels and event basics.
  This lesson assumes you already have *some* events firing and asks a different
  question: what do you look at on the boring Tuesday six weeks later?
- [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/06-sat-validation-instrumentation|Wilson-interval discipline]]
  (Block 2). When your sample is 40 users, a raw percentage lies. We will lean
  on that math on Wednesday; keep it in your pocket today.

## First principles: analytics exists to change a decision

A metric you will not act on is a distraction. Before you instrument anything,
finish this sentence: *"If this number goes down, I will \_\_\_\_."* If you
cannot fill the blank, do not track it on your dashboard. Put it in a warehouse
where it costs nothing to ignore.

This is the discipline that separates the two failure modes. The first is
**flying blind**: shipping features on vibes, never knowing if the magic AI
feature from Week 13 is used by 2% or 60% of users. The second, sneakier, is
**instrument-everything paralysis**: a dashboard with ninety tiles, none of
which has ever changed a decision, built because measuring feels like progress.
Startup Genome's analysis of 3,200 startups found the second failure mode has a
name and a body count: premature scaling, spending effort on infrastructure and
polish before nailing product/market fit, was the single largest cause of
startup death, implicated in roughly 70% of failures.[^1] A ninety-tile
dashboard is premature scaling of your attention.

So we build the smallest set of numbers that will actually move your hands.

## The metric hierarchy: vanity, then survival, then AI-specific

### Layer 0 — vanity metrics (know them, never optimize them)

Total signups. Page views. "Users." Cumulative anything. These go up and to the
right even when your product is dying, because they never decrement. A
cumulative signup chart is the most reassuring lie in your analytics tool. The
tell: a healthy metric can go *down*. If a number cannot fall, it cannot warn
you.

### Layer 1 — activation (the first promise kept)

Activation is the moment a new user first experiences the core value. Not
signup. Not "poked around." The specific action that correlates with them
coming back. Reforge popularized a clean three-step model for this: **Setup**
(the work to get ready), the **Aha moment** (first taste of value), and the
**Habit moment** (the behavior that predicts retention).[^2] Your job is to
define each one as a concrete, logged event for *your* product.

For an AI product the Aha is usually the first time the model does something the
user could not do alone, and *the user believes it*. That belief is the whole
game, and it is why AI activation is harder to instrument than SaaS activation.
A user can complete your onboarding checklist and still not trust the output.
Instrument the action, but watch the trust (Layer 2).

Concrete activation definitions from real products, for calibration:

- Duolingo's engagement work is the canonical case study: Lenny Rachitsky
  documented how Duolingo reignited growth by finding the right engagement
  metric (daily active users driven by a streak habit loop) and building the
  product around it rather than around raw installs.[^3]
- Slack's classic activation heuristic was 2,000 team messages sent. Facebook's
  was 7 friends in 10 days. These are not magic numbers; each team found the
  action that, once taken, made retention jump, then made onboarding a funnel
  toward it.

Your deliverable today: write one sentence. *"A user is activated when they
\_\_\_\_ within \_\_\_\_ of signup."* Fill both blanks with something you can log.

### Layer 2 — retention (the only number that tells the truth)

Retention is the health metric. Everything else is upstream of it or a proxy for
it. A product with great acquisition and bad retention is a bucket with a hole:
you can pour faster, but the water level tells the story.

Two things kill people here. First, **measuring the wrong retention**. There are
three flavors, and mixing them up produces confident nonsense:

- **N-day retention**: did the user come back on *exactly* day 7? Brutal, noisy
  for infrequent products. Good for daily-use apps (a language tutor), wrong for
  a product used monthly (an invoice generator).
- **Unbounded / "bracket" retention**: did the user come back *at all* in the
  window around day 7? More forgiving, better for weekly/monthly products.
- **Rolling retention**: did the user do anything on day 7 *or later*? Kindest
  of all, and the right lens for products with a naturally long cadence.

Pick the one that matches your product's natural frequency. A tax-prep AI used
once a year should not be graded on day-7 retention; that is malpractice with a
chart.

Second, **the curve shape matters more than any single point**. Reforge and
Amplitude both stress the same thing: a healthy product's retention curve
*flattens* into a plateau. A curve that decays toward zero has no product/market
fit no matter how high day-1 starts; a curve that flattens at even 15% has a
core of people who genuinely need the thing, and that core is your business.[^4]
The plateau, not the intercept, is the signal. Amplitude's SaaS retention work
frames the north star explicitly as the metric that captures *retained* value,
not momentary usage.[^5]

> My take: most indie builders stare at day-1 retention because it moves fast
> and feels controllable. It is the least informative point on the curve. Learn
> to read the plateau. If you only look at one chart each week, make it the
> retention curve for the last four weekly cohorts, overlaid.

### Layer 3 — the north-star metric

The north star is the single number that best captures delivered value, that the
whole team can rally behind, and that (this is the part people skip) *predicts
revenue without being revenue*. Reforge's framing: your north star should sit in
one of three families depending on your model — acquisition-led, retention-led,
or monetization-led — and for most AI products it should be retention-led,
because retention is where AI products actually die.[^2]

The famous trap has its own Reforge essay: **the north star that deceives
you**.[^6] The classic example is a metric you can inflate without creating
value. "Messages sent" looks like engagement until a confusing UI makes users
send three messages to accomplish one task; now your north star rewards your
own bad design. The defense is to pair every north-star candidate with a
counter-metric that catches the cheat. If north star is "reports generated,"
counter-metric is "reports generated per successful outcome" or "regeneration
rate" (below). A north star without a counter-metric is a target you will
eventually game against yourself.

Good north-star examples for AI products:

- Support-agent product: **weekly resolved conversations** (not "messages
  handled"), counter-metric containment quality.
- Writing product: **weekly documents the user kept and shipped** (not "drafts
  generated"), counter-metric regeneration rate.
- Analytics product: **weekly active accounts that reached an insight action**
  (exported, shared, or acted), not "queries run."

Notice the pattern: each north star is *retained, valued action*, weekly, per
account. Not cumulative, not vanity, not raw output.

## The six AI-specific metrics that predict churn

Here is where AI products diverge from ordinary SaaS. A normal app either works
or throws an error. An AI feature can run flawlessly, return a plausible answer,
and still be *wrong* or *distrusted*, and the user churns without ever filing a
bug. Your standard product analytics will not catch this. You need six extra
numbers.

### 1. Feature-trust rate

The share of AI outputs the user *accepts and acts on* versus dismisses, edits
heavily, or ignores. This is the truest measure of whether your magic feature is
magic. Instrument it with an explicit signal (accept / copy / ship / thumbs) or
an implicit one (did they use the output downstream, or delete it). Low
acceptance with high usage is a trust problem hiding inside a healthy-looking
engagement number.

### 2. Regeneration rate

How often users hit "regenerate" / "try again" on a single request. One
regeneration can be curiosity. A regeneration rate above roughly 30% on a
feature is a quality alarm: users are gambling for a better roll because the
first output was not good enough. Regeneration also directly multiplies your
token cost (metric 5), so it hits trust and margin at once.

### 3. Fallback / escalation rate (a.k.a. containment)

For any product with a human backstop, the containment rate is the share of
sessions the AI resolved *without* a human. Its cousin, deflection rate, counts
sessions that ended without escalation. These are not the same number, and
conflating them is a common way to lie to a board: containment measures whether
a ticket did not escalate; deflection measures whether it ended without a human,
which is a superset that includes users who simply gave up.[^7] Current
enterprise benchmarks put median tier-1 deflection around 41% in 2026, top
quartile near 59%, with agentic systems that take real backend actions reaching
70–85%.[^8] Nextiva's 2026 metric guide stresses pairing containment with a
resolution check, because a bot can show 90% deflection with only 40% of
problems actually solved.[^9]

The subtle trap: a *rising* containment rate can mean your AI got better, or it
can mean you made the "talk to a human" button harder to find. Always pair
containment with CSAT or a resolution signal. Deflection without satisfaction is
just abandonment you have relabeled.

### 4. Quality-drift (the metric that fires while you sleep)

Your model's output quality is not constant. It drifts, because the world drifts
(new slang, new products, new edge cases in your users' data) and because your
provider silently changes the model under you. Chip Huyen's *AI Engineering*
treats this as a first-class production concern: data distribution shift and
model degradation are the reason an eval that passed at launch fails in month
three, and the fix is continuous evaluation in production, not a one-time
test.[^10] Instrument a small, cheap, always-on quality signal: an LLM-as-judge
score on a sample of live outputs, or a golden-set replay run nightly. When the
number moves, you find out from your dashboard, not from a churn spike two months
later. We wire the mechanics of this on Tuesday.

### 5. Cost-per-active-user (the metric that decides your pricing)

Every AI feature has a token bill, and unlike SaaS your marginal cost per active
user is *not* near zero. You must know it per user and per feature, because it
sets your pricing floor. This number moved in 2026: the current-generation
Anthropic tokenizer produces roughly 30% more tokens for the same text than the
previous one, so a naive cost estimate carried over from last year understates
your bill by about a third.[^11] Model choice also swings it wildly — a task
routed to a small fast model versus a frontier model can differ 10× in cost for
a barely-perceptible quality change. Track cost-per-active-user weekly, broken
down by feature, and watch its ratio to revenue-per-active-user. If that ratio
climbs toward 1, you are running a token-reselling charity.

### 6. Time-to-value and its AI variant, time-to-trust

Standard time-to-value is minutes from signup to Aha. The AI variant is
minutes-or-interactions to *trust*: how many good outputs a user sees before
they stop double-checking every one. Products that shorten time-to-trust retain;
products where users never stop verifying churn, because at that point the AI is
adding work, not removing it. Ethan Mollick's adoption research keeps landing on
the same human truth: people extend trust to AI tools incrementally, through
repeated small wins, and a single confident wrong answer can reset the
counter.[^12] Instrument the streak of accepted outputs before disengagement.

## Choosing your north star: a worked selection

Say your Week 12/13 product is an AI meeting-notes assistant. Candidate north
stars:

| Candidate | Problem | Verdict |
|---|---|---|
| Total signups | Vanity, only goes up | Reject |
| Notes generated | Rewards volume, not value; gameable | Reject as north star, keep as input |
| Weekly accounts that *shared or exported* a note | Retained, valued action, weekly, per account | **North star** |
| Weekly active users | Doesn't require value delivered | Keep as a supporting input |

Counter-metric: regeneration rate + edit-heaviness (feature-trust). If shares go
up but edit-heaviness spikes, users are shipping notes they had to heavily fix,
and your "win" is fake.

Supporting inputs (the levers that move the north star): activation rate
(reached first shared note within 7 days), containment (meetings summarized
without a human correction), cost-per-active-user (margin guardrail).

That is the whole dashboard. Six-ish tiles. Each one, if it moves, changes what
you build next week.

## Worked example: instrument a north star and its counter-metric

You do not need a warehouse for this. The point today is the *definition*
discipline; Tuesday is the stack. Here is the smallest honest version, using a
plain event log you could send to any analytics tool or a Postgres table.

```python
# north_star.py — define events once, in code, so the definition can't drift.
# Run: python north_star.py  (pip install nothing; stdlib only)
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from collections import defaultdict

@dataclass(frozen=True)
class Event:
    account_id: str
    name: str            # 'signup' | 'note_generated' | 'note_shared' | 'note_regenerated'
    ts: datetime

# --- your ONE north-star definition, in code, testable ---
NORTH_STAR_EVENT = "note_shared"       # retained, valued action
ACTIVATION_WINDOW = timedelta(days=7)  # from signup

def weekly_north_star(events, week_start):
    """Distinct accounts that performed the valued action this week."""
    week_end = week_start + timedelta(days=7)
    accounts = {e.account_id for e in events
                if e.name == NORTH_STAR_EVENT and week_start <= e.ts < week_end}
    return len(accounts)

def activation_rate(events):
    """Share of signups that reached the valued action within the window."""
    signup_ts = {e.account_id: e.ts for e in events if e.name == "signup"}
    activated = 0
    for acct, ts in signup_ts.items():
        if any(e.account_id == acct and e.name == NORTH_STAR_EVENT
               and e.ts <= ts + ACTIVATION_WINDOW for e in events):
            activated += 1
    return activated / max(len(signup_ts), 1)

def regeneration_rate(events):
    """Counter-metric: regenerations per generated note. High => trust problem."""
    gen = sum(1 for e in events if e.name == "note_generated")
    regen = sum(1 for e in events if e.name == "note_regenerated")
    return regen / max(gen, 1)

if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    ev = [
        Event("acct_a", "signup", now - timedelta(days=6)),
        Event("acct_a", "note_generated", now - timedelta(days=5)),
        Event("acct_a", "note_shared", now - timedelta(days=5)),   # activated + north star
        Event("acct_b", "signup", now - timedelta(days=3)),
        Event("acct_b", "note_generated", now - timedelta(days=2)),
        Event("acct_b", "note_regenerated", now - timedelta(days=2)),  # trust wobble, no share
    ]
    week_start = now - timedelta(days=7)
    print("weekly north star (accounts shared):", weekly_north_star(ev, week_start))
    print("activation rate:", round(activation_rate(ev), 2))
    print("regeneration rate (counter):", round(regeneration_rate(ev), 2))
```

**Pass bar:** running this prints a north-star count of 1, activation 0.5,
regeneration 0.5, and — more important — you can point at the three function
bodies and defend each definition to someone trying to poke holes in it. If you
cannot defend a definition, that is the metric to fix before you build the
dashboard.

## Common mistakes experts see

1. **Optimizing a metric that can only go up.** Cumulative signups, total users,
   "all-time" anything. If it cannot decrement, it cannot warn you. Track the
   weekly, decrementable version.
2. **One retention definition for a product with mixed cadence.** Grading a
   monthly-use product on day-7 retention manufactures a crisis that is not
   real. Match the retention flavor to the natural frequency.
3. **A north star with no counter-metric.** You will eventually optimize against
   yourself. Every north star needs a paired guardrail that catches the cheat.
4. **Treating deflection as resolution.** A bot can end 90% of sessions without a
   human and solve 40% of problems.[^9] Containment and CSAT together, always.
5. **Ignoring cost-per-active-user until the bill scares you.** With the current
   tokenizer adding ~30% tokens,[^11] a margin you never measured can invert
   between two invoices. Track it weekly from day one, cheap.
6. **Measuring everything, deciding nothing.** Ninety tiles is premature scaling
   of attention.[^1] Six tiles you act on beats ninety you admire.

## Reflection questions

1. Write your activation sentence: "A user is activated when they \_\_\_\_ within
   \_\_\_\_ of signup." Could you log both blanks today? If not, what is missing?
2. What retention flavor (N-day, bracket, rolling) matches your product's natural
   frequency, and why is the other two wrong for you?
3. Name your north-star candidate and the exact way a user could inflate it
   without creating value. What counter-metric catches that?
4. Which of the six AI-specific metrics would move *first* if your model provider
   silently swapped the model under you? How would you notice within a day?
5. If cost-per-active-user rose 40% overnight, what would you do, and what would
   you need already instrumented to make that decision in an hour instead of a
   week?

## My take (reviewer lens)

**Chip Huyen** would push on quality-drift being underweighted here: in her
framing, continuous evaluation in production is not one of six metrics, it is the
spine, and treating it as a co-equal tile undersells how much silent model
degradation drives churn.[^10] Fair. I front-loaded it because indie builders
skip it entirely; she is right that at any real scale it graduates from tile to
system.

**Ethan Mollick** would note that trust is not a scalar you can fully capture in
an acceptance rate. His adoption research shows trust is contextual and
fragile — users trust the AI for drafting and distrust it for facts, in the same
session.[^12] So "feature-trust rate" aggregated across a product can hide two
opposite stories. Segment by feature or the number lies.

**Hamel Husain** would be blunter: most of this is procrastination if you have
not *looked at your data*. His refrain is that founders build dashboards to avoid
reading transcripts, and the highest-leverage analytics for an early AI product
is a human reading 50 real sessions with a spreadsheet open. The metrics tell you
*where* to look; they never tell you *what is wrong*. I agree, and Wednesday's
lesson leans hard into exactly that qualitative loop, because at 40 users the
transcript beats the chart every time.

## Further reading

**Must-read**

- Reforge, "How to Choose & Measure North Star Metrics" and "Don't Let Your
  North Star Metric Deceive You." The two-essay pair is the clearest treatment
  of the north-star trap.[^2][^6]
- Chip Huyen, *AI Engineering* (2025), the chapters on evaluation and
  production monitoring for the quality-drift discipline.[^10]

**Recommended**

- Lenny Rachitsky's Duolingo retention case study, for how one engagement metric
  reshaped a product.[^3]
- Nextiva's 2026 AI-agent metrics guide, for the containment/resolution
  pairing.[^9]

**Optional**

- Startup Genome, *Why Startups Fail: Premature Scaling* (2011). Old, still the
  best data on optimizing the wrong thing too early.[^1]

## Citations

[^1]: Startup Genome, "Startup Genome Report Extra: Premature Scaling" (2011).
https://s3.amazonaws.com/startupcompass-public/StartupGenomeReport2_Why_Startups_Fail_v2.pdf
— 70% of failed startups attributed to premature scaling; no prematurely-scaled
startup in the dataset passed 100k users. (search-verified 2026-07-17; fetch
egress-blocked — liveness pass pending; corroborated by Forbes,
https://www.forbes.com/sites/nathanfurr/2011/09/02/1-cause-of-startup-death-premature-scaling/)
[^2]: Reforge Blog, "How to Choose & Measure North Star Metrics: Acquisition,
Retention, & Monetization." https://www.reforge.com/blog/north-star-metrics —
three north-star families; Setup/Aha/Habit activation model. (search-verified
2026-07-17; corroborated by Amplitude north-star writeup below.)
[^3]: Lenny Rachitsky, "How Duolingo reignited user growth" (Lenny's Newsletter).
https://www.lennysnewsletter.com/p/how-duolingo-reignited-user-growth —
engagement-metric-led growth via streak habit loop. (search-verified 2026-07-17;
corroborated by Reforge north-star artifacts.)
[^4]: Reforge / Amplitude retention-curve guidance: a healthy retention curve
flattens to a plateau; the plateau, not the intercept, indicates product/market
fit. https://www.reforge.com/blog/north-star-metric-growth (search-verified
2026-07-17; corroborated by Amplitude below.)
[^5]: Amplitude, "North Star Metric: How a Top SaaS Provider Set Retention
Records." https://amplitude.com/blog/north-star-saas-provider — north star as
retained value. (search-verified 2026-07-17.)
[^6]: Reforge Blog, "Don't Let Your North Star Metric Deceive You."
https://www.reforge.com/blog/north-star-metric-growth — the gameable-north-star
trap and counter-metric defense. (search-verified 2026-07-17.)
[^7]: AeroChat, "Deflection Rate vs Containment Rate in AI Chatbots in 2026."
https://aerochat.ai/blog/deflection-rate-vs-containment-rate-in-ai-chatbots —
containment (did not escalate) is a subset of deflection (ended without a
human). (search-verified 2026-07-17; corroborated by digitalapplied below.)
[^8]: Digital Applied, "AI Customer Support Metrics: Deflection + CSAT
Framework" (2026).
https://www.digitalapplied.com/blog/ai-customer-support-metrics-deflection-csat-framework-2026
— median tier-1 deflection ~41.2%, top quartile 58.7%, agentic systems 70–85%.
(search-verified 2026-07-17; corroborated by AeroChat and Nextiva.)
[^9]: Nextiva, "AI Agent Performance Metrics: Key KPIs for 2026."
https://www.nextiva.com/blog/ai-agent-performance-metrics.html — 90% deflection
can coexist with 40% resolution; pair containment with resolution/CSAT.
(search-verified 2026-07-17.)
[^10]: Chip Huyen, *AI Engineering* (O'Reilly, 2025), evaluation & production
monitoring chapters — data distribution shift, model degradation, continuous
in-production evaluation. https://www.oreilly.com/library/view/ai-engineering/9781098166298/
(search-verified 2026-07-17; corroborated by her prior *Designing Machine
Learning Systems* monitoring chapter.)
[^11]: Anthropic tokenizer change (current-generation models, ~+30% tokens vs
prior generation) as recorded in the course landscape refresh; affects all
cost-per-active-user math. See `vault/00-program/_refresh-2026-07-master-report.md`
cross-cutting theme 1. (search-verified 2026-07-17; two-source verification
recorded in the master refresh report.)
[^12]: Ethan Mollick, *One Useful Thing* — incremental trust in AI tools; a
confident wrong answer resets accrued trust. https://www.oneusefulthing.org/
(search-verified 2026-07-17; consistent with his book *Co-Intelligence*.)

_last_verified: 2026-07-17_
