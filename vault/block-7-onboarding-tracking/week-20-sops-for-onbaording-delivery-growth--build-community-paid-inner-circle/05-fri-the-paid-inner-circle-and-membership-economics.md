---
type: lesson
block: block-7-onboarding-tracking
week: week-20
session_slug: build-community-paid-inner-circle
day_of_cycle: 5
day_name: fri
date_due: 2026-10-02
tags:
  - paid-community
  - membership
  - unit-economics
  - churn
  - ltv
  - mrr
  - ghost-town
sources:
  - churnkey-membership-churn
  - communipass-reduce-churn
  - kourses-member-retention
  - eightx-ltv-cac
  - i4a-member-ltv
  - moneyinc-small-paid-community
  - spinks-business-of-belonging
  - schoolmaker-circle-pricing
last_verified: 2026-07-17
word_count_target: 5300
---

# The paid inner circle & membership economics

## Why this matters

A paid membership is the best business model most operators never build correctly:
recurring revenue, compounding retention, and a moat made of belonging. It is also
the model that punishes carelessness fastest, because churn is silent, compounding,
and fatal. A membership that loses 10% of members a month is dead in a way its
founder will not feel until the MRR chart bends and it is too late. Today you learn
to design a paid inner circle that people stay in: the membership model and its
value mix, tier and pricing design, and the unit economics (MRR, churn, LTV) that
determine whether it is a business or a treadmill. Most importantly, you learn the
one metric that warns you a community is dying while you can still save it, the
ghost-town early-warning signal you will build on Saturday.

## Prerequisites

- [[04-thu-building-community-the-compounding-moat|Thu]] — free vs paid, platform
  choice, and the cold-start problem the inner circle must survive.
- [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/04-thu-tiers-upsell-hooks-and-expansion-revenue|Week 16 · tiers, upsell, and expansion revenue]] — the
  pricing-and-tier logic we apply to memberships. We build on it, not re-teach it.
- [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/01-mon-product-analytics-for-ai-products|Week 14 · retention]] — retention curves and churn, the
  foundation of membership economics.

## Core content

### The inner-circle model: what people actually pay for

A paid inner circle is not "a Discord with a paywall." People do not pay monthly for
access to a chat room. They pay for a *bundle* whose parts reinforce each other, and
the strongest memberships combine three ingredients:

1. **Access.** To you, and to a smaller room of more serious peers. The paid
   community's core promise is higher signal, fewer tire-kickers, and proximity to
   the founder and to people operating at their level or above. Access is the
   ingredient a free community structurally cannot offer.
2. **Ongoing content and live interaction.** Regular value that gives members a
   reason to stay *this* month, not just a reason to have joined. Live calls,
   workshops, teardowns, Q&A. The recurring live element is what converts a
   one-time purchase into a recurring one.
3. **Belonging and identity.** The Spinks core from yesterday: a place where members
   create value for each other, have relationships and status, and would feel a loss
   if they left.[^1] This is the retention engine, because leaving means leaving
   people, not just canceling a subscription.

The economics evidence is unambiguous about why the mix matters: the strongest
hybrid memberships, combining community plus content plus live calls, can sustain
monthly retention above 96%, while static course-only memberships tend to retain
far less (roughly 88-92% monthly).[^2] The lesson is structural: a membership that
is just content is a course with a subscription button, and it churns as soon as
the member has consumed what they came for. A membership that is content *plus*
community *plus* live access churns slowly, because the reasons to stay compound.

### Retention is the whole game (and churn is the enemy)

Everything about membership economics reduces to one number: churn. In a recurring
model, retention is not one metric among many, it is the metric that determines
whether you have a business. Here is why, made quantitative.

The 2026 benchmarks for paid communities:

- Healthy monthly churn is below 5% (equivalently, monthly retention above 95%).
  Between 92% and 95% retention is solid. Below 90% retention (over 10% monthly
  churn) signals a real problem worth fixing before you spend another dollar on
  acquisition.[^3]
- Elite membership sites target 1-2% monthly churn or less.[^3]
- Healthy online paid communities typically retain 91-94% of members month over
  month; the best hybrids exceed 96%.[^2]

Now the reason churn is existential rather than annoying, through the LTV formula.
Average member lifetime in months is 1 divided by monthly churn rate. So:

- 5% monthly churn implies an average lifetime of 20 months.
- Cut churn to 2.5% and lifetime doubles to 40 months.[^4]

A halving of churn *doubles* how long each member stays and therefore doubles the
revenue each member is worth. There is no acquisition tactic that produces that kind
of leverage. This is why experienced membership operators say the same thing: a
dollar spent reducing churn is worth several dollars spent on acquisition, because
churn is the most sensitive input in the entire model. If your churn is above the
healthy band, fixing it is the single highest-return activity in your business, and
pouring acquisition into a high-churn membership is filling a leaky bucket faster.

### Membership unit economics: MRR, churn, LTV, CAC

You cannot manage a membership on gut feel. Four numbers, and the relationships
between them, tell you whether the business works. You will compute all of these in
Saturday's `code-lab/1/` model; here is what they mean.

**MRR (Monthly Recurring Revenue).** The predictable monthly revenue from
memberships: sum over your tiers of (members in tier x tier price). This is the
headline number, but it is a lagging one, it tells you where you are, not where you
are heading. Two more numbers tell you the trajectory.

**Churn rate.** The percentage of members who cancel in a month. Track it as a rate
(cancellations / members at start of month) and watch the trend, not just the level.
Rising churn is the earliest financial warning that value is slipping.

**LTV (Lifetime Value).** What a member is worth over their whole tenure. For a
subscription, the standard formula is:

```
LTV = (ARPU x gross_margin) / monthly_churn_rate
```

where ARPU is average revenue per user per month and gross margin is the fraction
left after the cost to serve.[^4] The membership-specific version, average member
tenure times monthly revenue (plus any non-dues revenue from events or upsells),
gives the same intuition: LTV rises when members pay more, cost less to serve, or
stay longer, and staying longer (lower churn) is the biggest lever.[^5]

**CAC (Customer Acquisition Cost) and the LTV:CAC ratio.** What it costs to acquire
a member, and the ratio of what they are worth to what they cost. The standard
healthy benchmark is LTV:CAC of at least 3:1.[^4] Below that, you are spending too
much to acquire members relative to what they are worth, which for a membership
almost always means churn is too high (crushing LTV) rather than acquisition being
too expensive. The ratio is a churn diagnostic in disguise.

The relationships to internalize:

- Churn is the most sensitive input. Small churn improvements produce large LTV
  improvements, because LTV divides by churn.[^4]
- MRR growth is a race between new MRR and churned MRR. A membership can show
  growing MRR while its churn is quietly worsening, until the two lines cross and
  MRR falls off a cliff. Net MRR movement (new + expansion − churn − contraction) is
  the honest number.
- Expansion beats acquisition. Upselling existing members to higher tiers (the Week
  16 expansion-revenue logic) grows MRR without acquisition cost and signals the
  opposite of churn: members going deeper, not leaving.

### Tier design for memberships

Apply the Week 16 tier logic to the membership. A well-designed membership usually
has two or three tiers, differentiated by *access and depth*, not by artificially
withholding basic value:

- **A core tier** with the community, the content, and the group live sessions. The
  bulk of members live here. Priced for accessibility and volume.
- **A high tier** (the true "inner circle") with direct access: smaller-group or
  one-to-one time with the founder, hands-on help, higher-touch. Priced for the few
  who want maximum proximity, and often where the margin is.
- **Optionally, an entry tier** or a free layer that funnels into the paid tiers
  (yesterday's free-community funnel).

The design principle from Week 16 carries directly: tiers should map to *how much
value a member gets*, so that a member naturally graduates upward as they get more
serious. The upgrade from core to inner circle is your expansion-revenue engine, and
it churns *down* less than new acquisition churns out, because an upgrading member is
demonstrating exactly the deepening commitment that predicts retention.

The pricing anchors, from the platform reality: the platform fee sets a floor on
viable pricing. As noted in yesterday's platform economics, higher-fee platforms
force higher member prices to break even (for many creator communities in the
$49-79/month range, a higher-fee platform forces pricing rooms at $99+/month just to
clear costs).[^6] Price the membership on the value and belonging, not the content
cost, but make sure the price clears your platform fees, payment processing, and
cost to serve with margin to spare.

### The ghost-town death, and its early warning

Here is the failure mode that kills paid communities, and the metric that catches it
in time. A community does not usually die from a mass exodus. It dies quietly: the
active core shrinks, posts get fewer replies, the founder gets busy and posts less,
new members arrive to a room that feels dead and leave without engaging, and one day
the founder looks up and it is a ghost town, at which point churn spikes and the MRR
chart bends. By the time churn shows up in the financials, the community has been
dying for months.

The problem with churn as your warning signal is that it is a *lagging* indicator:
by the time a member cancels, they disengaged weeks earlier. You need a *leading*
indicator, and the community gives you one. The ghost-town early-warning metric is
built on engagement, not revenue:

- **Active-member ratio.** The fraction of members who were active (posted,
  commented, or attended) in the last 7 days, divided by total members. This is the
  vitality of the room. Watch its *trend*, not just its level.
- **The active core's direction.** Per yesterday's participation reality, most
  members lurk, and that is fine. The signal is not the lurker percentage, it is
  whether the *active core is growing or shrinking* relative to total membership. A
  shrinking active-member ratio is the earliest sign of a community sliding toward
  ghost town, and it moves weeks before churn does.[^1]
- **New-member first-week activation.** The fraction of new members who engage in
  their first week, exactly the onboarding-activation logic from Tuesday, applied to
  community. New members who do not post or engage in week one are the ones who will
  silently churn, and a falling first-week activation rate means the room is no
  longer pulling newcomers in.

The Saturday `code-lab/1/` model turns this into a concrete early-warning flag: it
raises a ghost-town risk alert when the active-member ratio falls below a threshold
*or* declines for several consecutive periods, so you intervene (re-energize the
core, run an event, get the founder posting again) while the community is still
saveable. The financial metrics (MRR, churn, LTV) tell you the outcome; the
engagement metrics tell you the outcome *before it happens*. Watch both, and act on
the leading one.

> My take: the single most common cause of the ghost-town death is not a bad
> product, it is the founder losing interest. The community was alive because the
> founder was its most active member; the founder got busy, posted less, the energy
> left, and the members followed. If you are not prepared to be the community's
> engine for the long haul, or to hire someone whose actual job is to be that
> engine, do not charge people monthly for a room you will let go quiet.

### Delivering ongoing value: the reason to stay this month

Because members can cancel any month, a membership must deliver a reason to stay
*this* month, not coast on the reason they joined. The operators who sustain high
retention share a discipline: a predictable rhythm of fresh value. A recurring live
call members plan their month around. A regular new resource or teardown. A steady
cadence of the founder showing up. The membership churn research is consistent that
the strongest retention comes from the hybrid of community, content, and live
interaction precisely because live interaction is inherently recurring, you cannot
"finish" a live community the way you finish a course.[^2] The retention question to
ask constantly: if a member asked "why am I still paying for this?" on the 28th of
the month, what is the specific, recent answer? If you do not have one, that member
is a future cancellation.

## Worked example: unit economics of a small paid inner circle

Let us run the numbers on a realistic small paid community, the kind you could
launch from this week's build.

**Setup.** You launch a paid inner circle on Skool ($99/month platform cost, ~2.9%
transaction fee).[^6] Two tiers: Core at $50/month (community + monthly group call +
resource library) and Inner Circle at $200/month (everything in Core + a monthly
small-group call with you + async access). After three months you have 80 Core
members and 12 Inner Circle members.

**MRR.** (80 x $50) + (12 x $200) = $4,000 + $2,400 = **$6,400/month.**

**Churn scenario A (healthy).** Monthly churn of 4% (retention 96%, in the healthy
band). Average member lifetime = 1 / 0.04 = 25 months. With a blended ARPU of
$6,400 / 92 = ~$70/member/month and, say, a 90% gross margin (low cost to serve),
LTV = ($70 x 0.90) / 0.04 = **~$1,565 per member.** If your blended CAC to acquire a
member is $150, your LTV:CAC is ~10:1, well above the 3:1 healthy benchmark. This is
a real business, and the leverage is expansion (upgrading Core members to Inner
Circle) and holding churn.

**Churn scenario B (bleaky).** Same MRR today, but monthly churn of 10% (retention
90%, the danger line). Average lifetime = 1 / 0.10 = 10 months. LTV = ($70 x 0.90) /
0.10 = **~$626 per member,** less than half of scenario A, from the same revenue
today. At a $150 CAC your LTV:CAC is ~4:1, still passable, but the trajectory is the
problem: at 10% monthly churn you lose ~9 members a month and must acquire 9 just to
stand still. The MRR looks fine *now* and is quietly doomed, and the churn will not
alarm you until the growth stalls.

**What the early-warning metric would show.** In scenario B, weeks before the churn
shows up financially, the active-member ratio would be sliding: fewer of the 92
members posting each week, new members not activating in week one, the founder
posting less. The Saturday model flags this, giving you the window to intervene (run
an event, re-engage the core, ship fresh value) before the churn hits the MRR. The
whole point: the engagement metric is the smoke alarm; the churn metric is the fire.

You will run these exact calculations, and the ghost-town early-warning flag, on your
own numbers in `code-lab/1/` on [[06-sat-build-sop-library-and-community-launch|Saturday]].

## Common mistakes experts see

1. **Building a "Discord with a paywall."** People do not pay monthly for chat
   access. They pay for the access + content + belonging bundle; a membership missing
   the live and community elements churns like a finished course.[^2]
2. **Watching MRR while ignoring churn trend.** MRR can grow while churn worsens,
   until the lines cross and MRR falls off a cliff. Net MRR movement and churn trend
   are the honest numbers.
3. **Pouring acquisition into a high-churn membership.** Above ~10% monthly churn you
   are filling a leaky bucket. Fixing churn is the higher-return activity, because
   LTV divides by churn.[^3][^4]
4. **Pricing on content cost instead of value and belonging.** Price on the value and
   the belonging, but make sure it clears platform fees, processing, and cost to serve
   with real margin.[^6]
5. **Using churn as your only warning signal.** Churn is a lagging indicator; by the
   time a member cancels they disengaged weeks ago. Watch the active-member ratio and
   first-week activation, which lead churn by weeks.
6. **The founder disengaging.** The community was alive because you were its engine.
   If you stop showing up, the energy and then the members leave. Commit to being the
   engine, or fund someone who will be.

## Reflection questions

1. Is your planned membership a bundle of access + content + belonging, or is it
   really just gated content that will churn once consumed? Be honest about which.
2. At your target price and an assumed churn rate, what is your LTV? Now halve the
   churn: what does LTV become, and what does that tell you about where to spend
   effort?
3. What is the specific, recent answer to a member asking "why am I still paying for
   this?" on the 28th of the month? If you do not have one, what will you build to
   create one?
4. What would your ghost-town early-warning metric be, concretely, and at what
   threshold or trend would it trigger you to act? Would you actually notice it today?
5. Are you genuinely prepared to be the community's most active member for a year, or
   to pay someone to be? If not, should you be charging monthly at all?

## My take (reviewer lens)

**Chip Huyen** would insist that the early-warning metric be instrumented before
launch, not bolted on after churn appears: the whole value of a leading indicator is
lost if you start measuring engagement only once the community is already dying, so
the active-member ratio and first-week activation must be tracked from member one.
She would also warn against vanity engagement metrics (total messages, total members)
that go up while the *active core* shrinks; the ratio, and its trend, is the honest
signal.

**Michael Seibel** would push back on over-modeling a community that does not exist
yet: the unit economics are worth understanding, but a first-time community founder
should charge a simple price, get the first ten paying members, and learn what they
actually value before building an elaborate tier structure and financial model. He is
right that the numbers matter more for deciding *whether the model can work* than for
running a community you have not launched. Use the model to sanity-check, then go get
ten members.

**swyx** would flag the platform-dependence risk in the economics: your LTV
calculation assumes the platform's fees and terms stay put, and a fee change or policy
shift (the kind the 2026 platform shakeout has produced) can move your unit economics
overnight, which again argues for owning the direct member relationship off-platform
so a platform's economics cannot unilaterally break yours.

## Further reading

**Must-read**

- Churnkey, "Membership Churn: Benchmarks, Calculator and Best Practices," for the
  churn benchmarks and the LTV-churn relationship that govern the whole model.[^3]

**Recommended**

- Eightx on the LTV:CAC ratio and why churn is the most sensitive input.[^4]
- Communipass, "How to Reduce Churn in a Paid Community," for the retention tactics
  behind the numbers.[^7]

**Optional**

- MoneyInc's 2026 data on the profitability of small paid communities, for a reality
  check on realistic revenue.[^8]
- Back to [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/04-thu-tiers-upsell-hooks-and-expansion-revenue|Week 16 tiers]] for the tier and expansion-revenue
  logic applied here.

## Citations

[^1]: David Spinks, *The Business of Belonging*, Wiley.
https://www.wiley.com/en-us/The+Business+of+Belonging:+How+to+Make+Community+your+Competitive+Advantage-p-9781119766124
— members creating value for each other is the retention engine; belonging is what
makes leaving a loss. (Evergreen; corroborated by blinkist.com/en/books/the-business-of-belonging-en.)
[^2]: "Member Retention 2026: Strategies, Benchmarks, Formulas," Kourses.
https://kourses.com/member-retention/ — hybrid memberships (community + content +
live) can sustain >96% monthly retention; static course memberships retain ~88-92%.
(search-verified 2026-07-17; fetch egress-blocked — liveness pass pending;
corroborated by churnkey.co/blog/membership-churn/.)
[^3]: "Membership Churn: Benchmarks, Calculator and Best Practices," Churnkey.
https://churnkey.co/blog/membership-churn/ — healthy monthly churn <5%, over 10% is a
real problem; elite sites target 1-2%. (search-verified 2026-07-17; corroborated by
communipass.com/blog/how-to-reduce-churn-in-a-paid-community-... below.)
[^4]: "LTV:CAC Ratio: What It Is, Why 3:1 Matters," Eightx.
https://eightx.co/blog/ltv-cac-ratio-guide — LTV = (ARPU x gross margin) / monthly
churn; lifetime = 1/churn (5% → 20 months, 2.5% → 40 months); 3:1 benchmark; churn is
the most sensitive input. (search-verified 2026-07-17; corroborated by
metrichq.org/saas/lifetime-value-to-customer-acquisition-cost-ratio-ltvcac/.)
[^5]: "Calculating Member Lifetime Value," i4a.
https://www.i4a.com/blog/calculating-member-ltv/ — member LTV = annual dues x average
tenure, plus non-dues revenue; average tenure = 1 / annual churn. (search-verified
2026-07-17; corroborated by membership.quest LTV calculator.)
[^6]: "Skool vs Discord vs Circle 2026," Stickyhive.
https://stickyhive.ai/skool/vs-discord/ — platform fees set the pricing floor;
higher-fee platforms force $99+/mo pricing to break even; Skool $99/mo Pro + ~2.9%.
(search-verified 2026-07-17; corroborated by schoolmaker.com/blog/circle-so-pricing.)
[^7]: "How to Reduce Churn in a Paid Community: 12 Retention Strategies," Communipass.
https://communipass.com/blog/how-to-reduce-churn-in-a-paid-community-12-retention-strategies-that-actually-work-in-2026/
— retention tactics and the centrality of ongoing value. (search-verified 2026-07-17;
corroborated by kourses.com/member-retention/.)
[^8]: "How Profitable Is a Small Paid Membership Community in 2026?," MoneyInc.
https://moneyinc.com/how-profitable-is-a-small-paid-membership-community-in-2026/ —
realistic revenue data for small paid communities. (search-verified 2026-07-17;
corroborated by churnkey.co membership-churn benchmarks above.)

_last_verified: 2026-07-17_
