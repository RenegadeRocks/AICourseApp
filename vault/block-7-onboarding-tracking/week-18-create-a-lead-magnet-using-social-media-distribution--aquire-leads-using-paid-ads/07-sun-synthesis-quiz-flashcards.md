---
type: lesson
block: block-7-onboarding-tracking
week: week-18
session_slug: aquire-leads-using-paid-ads
day_of_cycle: 7
day_name: sun
date_due: 2026-09-20
tags:
  - synthesis
  - quiz
  - flashcards
  - lead-gen
  - paid-ads
last_verified: 2026-07-19
word_count_target: 3200
---

# Synthesis, quiz & flashcards

## The week in one arc

Week 18 built a demand-capture machine, in the only order that works.

A **lead magnet** ([[01-mon-lead-magnets-that-convert|Mon]]) is a trade: value
for an email, and in 2026 the buyer is skeptical and the seller pays a
deliverability tax on every low-intent signup. Win the trade with a specific
promise and a designed next step, ideally an AI-native tool built from a slice of
your product. Gate by intent, not by default.

An **opt-in funnel** ([[02-tue-opt-in-funnel-and-list-hygiene|Tue]]) captures the
trade and keeps it deliverable. In 2026 deliverability is a hard gate: SPF, DKIM,
DMARC, one-click unsubscribe, and a spam-complaint rate under 0.30%, enforced with
550 rejections. Measure opt-in rate, not subscriber count. Double opt-in filters
the abuse that paid traffic invites.

An **organic distribution engine** ([[03-wed-organic-distribution-engine|Wed]])
fills the funnel for free and compounds: content → magnet → list → content. Reuse
the *idea*, not the asset, across native formats. Respect the platform mechanics
(no in-body links on LinkedIn, the first hour decides reach) but optimize for the
durable thing: be specifically, un-swappably useful.

**Paid ads** ([[04-thu-paid-ads-honest-primer|Thu]]) amplify a funnel that
already converts; they do not create demand. Meta Advantage+ automates targeting
and creative, so your levers are the offer, the creative concepts, and a clean
conversion signal. Size the test to actually learn (~50 conversions/ad set/week),
or stay organic.

**Campaign measurement** ([[05-fri-campaign-mechanics-and-measurement|Fri]]) is
the discipline that turns spend into a decision. Attribution is broken (50-70%
loss), so run CAPI, reconcile against your own customer count, watch blended CAC,
and pre-register a CAC-based kill/scale rule read on your own numbers, not the
platform's modeled ROAS. AI creative is at parity, but only when it does not look
like AI.

**The build** ([[06-sat-build-the-lead-gen-engine|Sat]]) assembled all four into
a live engine, with `code-lab/1` computing the ratios so vanity totals cannot
fool you.

## The five ideas that generalize

1. **A lead is only worth capturing if you have a place to put it and a next step
   to send it to.** Magnet, funnel, and offer are one system.
2. **Optimize the ratio, not the total.** Opt-in rate, CAC, and funnel conversion
   diagnose; subscriber count and CTR flatter.
3. **Paid amplifies; it does not create.** Prove the funnel free, then scale it
   paid. Never run paid to discover if the funnel works.
4. **Pre-register the decision.** A CAC target and a kill/scale rule written
   before you spend is the only defense against sunk-cost and small-N panic.
5. **Reason from your own totals.** When attribution and arithmetic disagree,
   trust arithmetic: your DB knows how many customers you got.

## Quiz (15 questions)

Take it cold, no notes. Answers below.

1. **(Short answer)** What are the two halves most failed lead magnets are
   missing?

2. **(MCQ)** In 2026, which lead-magnet format tends to convert highest?
   a) a 50-page ebook  b) a generic webinar  c) an interactive tool
   (calculator/quiz/audit)  d) a newsletter signup box

3. **(Short answer)** State the gated-vs-ungated synthesis in one sentence.

4. **(MCQ)** A bulk sender's spam-complaint rate should stay below which
   threshold to avoid enforcement?
   a) 0.01%  b) 0.30%  c) 3.0%  d) 10%

5. **(Short answer)** Why does making it *easier* to unsubscribe *protect* your
   deliverability?

6. **(MCQ)** Which metric should you track instead of raw subscriber count?
   a) total emails sent  b) opt-in rate  c) follower count  d) impressions

7. **(Short answer)** In the content→magnet→list→content loop, what makes each
   turn cheaper than the last?

8. **(MCQ)** On LinkedIn in 2026, putting the magnet link in the post body
   typically does what?
   a) boosts reach ~60%  b) has no effect  c) cuts reach ~60%  d) is required by
   the algorithm

9. **(Short answer)** State the one rule that governs whether paid ads make sense.

10. **(MCQ)** Roughly what daily budget does meaningful Meta testing require in
    2026 to let the algorithm optimize?
    a) $1-5/day  b) $50-100/day  c) $500-1000/day  d) $5000/day

11. **(Short answer)** Why is CPL a leading indicator but CAC the truth?

12. **(MCQ)** In 2026, what share of many advertisers' conversions cannot be
    deterministically attributed?
    a) ~5%  b) ~20%  c) ~50-70%  d) ~99%

13. **(Short answer)** What is "blended CAC" and why can it not be distorted by
    attribution?

14. **(Code completion)** Given the pre-registered rule below, what does
    `paid_test_decision(spend=1050, customers=4, rule)` return, and why?
    ```python
    rule = PaidTestRule(target_cac=150, scale_below=120, kill_above=200,
                        min_spend=1000, min_customers=5)
    ```

15. **(Short answer)** The 2026 AI-creative study found AI ads perform best under
    what condition? What does that imply for your creative process?

## Answer key

1. **A specific promise** (a numbered, outcome-shaped offer that matches the ad/
   post) **and a designed next step** (a low-friction bridge from the magnet to
   the offer). Missing either turns the magnet into a cost center.
   ([[01-mon-lead-magnets-that-convert|Mon]])

2. **c) an interactive tool.** Interactive magnets outconvert static content by
   ~70%; quizzes ~40%, AI-adaptive quizzes ~47%. Ebooks convert at 4-8%.
   ([[01-mon-lead-magnets-that-convert|Mon]])

3. **Gate by intent, not by default:** ungate top-of-funnel content that builds
   reputation and travels on social; gate the high-utility bottom-of-funnel tool
   where the value exchange is obviously fair. ([[01-mon-lead-magnets-that-convert|Mon]])

4. **b) 0.30%.** At or above 0.30% you are in enforcement territory (Gmail);
   above 0.10% deserves attention. ([[02-tue-opt-in-funnel-and-list-hygiene|Tue]])

5. Because an easy unsubscribe diverts people from hitting "Report Spam."
   Complaints damage sender reputation; unsubscribes do not. Protecting the exit
   protects inbox placement for everyone who stays.
   ([[02-tue-opt-in-funnel-and-list-hygiene|Tue]])

6. **b) opt-in rate** (submissions ÷ visitors). The raw count always rises and
   diagnoses nothing. ([[02-tue-opt-in-funnel-and-list-hygiene|Tue]])

7. Each turn converts volatile borrowed attention (a post) into stable owned
   attention (a subscriber), and the list supplies sharper raw material (real
   questions, results, objections) for the next piece of content.
   ([[03-wed-organic-distribution-engine|Wed]])

8. **c) cuts reach ~60%.** Put the link in the first comment or profile instead.
   ([[03-wed-organic-distribution-engine|Wed]])

9. **Paid amplifies a working funnel; it does not create demand.** Ads on a
   funnel that does not convert buy a bigger broken thing.
   ([[04-thu-paid-ads-honest-primer|Thu]])

10. **b) $50-100/day,** enough to reach ~50 conversions/ad set/week and exit the
    learning phase. Meta's $1-5/day minimum keeps a campaign alive but does not
    let it optimize. ([[04-thu-paid-ads-honest-primer|Thu]])

11. CPL (spend ÷ leads) measures how cheaply you fill the list, but a cheap lead
    that never converts is not cheap. CAC (spend ÷ customers) measures the number
    your unit economics are actually built on.
    ([[05-fri-campaign-mechanics-and-measurement|Fri]])

12. **c) ~50-70%,** because ATT opt-in rates sit around 18-25% and ~75% of iOS
    conversions cannot be deterministically tied to a click.
    ([[05-fri-campaign-mechanics-and-measurement|Fri]])

13. Blended CAC = total sales-and-marketing spend ÷ total new customers, across
    all channels. Because it uses totals rather than per-channel attribution, no
    attribution model can distort it, so when platform ROAS and blended CAC
    disagree, trust blended. ([[05-fri-campaign-mechanics-and-measurement|Fri]])

14. Returns **`INSUFFICIENT_DATA`.** CAC is $262 (below the kill line), but only
    4 customers is below `min_customers=5`, so the rule refuses to decide on a
    sample too small to be meaningful. This is the small-N guardrail.
    ([[06-sat-build-the-lead-gen-engine|Sat]], `code-lab/1`)

15. AI ads performed best when they **did not look like AI** (avoiding the
    over-polished, hyper-saturated aesthetic; a real human face as a trust
    signal). Implication: use AI to *produce* creative at volume, but ruthlessly
    reject anything that reads as machine-made. The winning creative is
    AI-produced and human-feeling. ([[05-fri-campaign-mechanics-and-measurement|Fri]])

**Scoring:** 13-15 fluent, walk into the live session ready. 10-12 solid, review
the misses. Below 10, re-read the two weakest lessons before Monday and run
`code-lab/1` again.

## Flashcards (30)

1. **Q:** What is a lead magnet, in first principles? **A:** A trade: value given
   in exchange for an email and implied consent to contact.

2. **Q:** The two halves most failed magnets miss? **A:** A specific promise, and
   a designed next step.

3. **Q:** Why is a high opt-in rate not automatically good? **A:** It may attract
   tire-kickers who never convert and who raise your spam-complaint rate.

4. **Q:** Highest-pull, lowest-cost magnet for a technical founder? **A:** An
   AI-native tool (audit/calculator/agent) built from a slice of your product.

5. **Q:** Interactive vs static magnet conversion gap? **A:** Interactive
   outconverts static by roughly 70%.

6. **Q:** The gated-vs-ungated synthesis? **A:** Gate by intent, not by default;
   ungate top-of-funnel, gate high-utility bottom-of-funnel.

7. **Q:** Value-calibration rule for a magnet? **A:** Give away the what/why
   completely; sell the implementation (done-with/for-you).

8. **Q:** The four opt-in funnel stages? **A:** Traffic→page, page→submitted,
   submitted→confirmed, confirmed→engaged.

9. **Q:** 2026 email authentication requirements? **A:** SPF, DKIM, DMARC (p=none
   minimum, progressing to quarantine/reject).

10. **Q:** Spam-complaint-rate enforcement threshold? **A:** 0.30% (attention
    above 0.10%).

11. **Q:** Penalty for non-compliant bulk mail in 2026? **A:** Permanent 550
    rejections, not quiet spam-foldering.

12. **Q:** Why use double opt-in on paid/cold traffic? **A:** It filters the
    highest-abuse channel's dirty addresses before they hit your complaint rate.

13. **Q:** Why does an easy unsubscribe protect deliverability? **A:** It diverts
    people from "Report Spam"; complaints hurt reputation, unsubscribes do not.

14. **Q:** The four-email welcome sequence shape? **A:** Deliver instantly, quick
    win, story+proof, bridge to offer.

15. **Q:** Metric to track instead of subscriber count? **A:** Opt-in rate
    (submissions ÷ visitors).

16. **Q:** The distribution flywheel loop? **A:** Content → magnet → list →
    content.

17. **Q:** Unit of reuse in repurposing? **A:** The idea, not the asset; reshape
    per platform.

18. **Q:** LinkedIn 2026 top formats? **A:** Document carousels (~6.6% ER), native
    video, newsletters.

19. **Q:** Cost of an in-body link on LinkedIn? **A:** ~60% less reach; use first
    comment or profile.

20. **Q:** What decides LinkedIn reach in the first hour? **A:** Early engagement
    and dwell time (how long people actually read).

21. **Q:** Antidote to AI slop in content? **A:** Specificity, real numbers/
    decisions/opinions, not sincere tone. Un-swappable by a competitor.

22. **Q:** The one rule of paid ads? **A:** Paid amplifies a working funnel; it
    does not create demand.

23. **Q:** Three preconditions for running paid? **A:** Funnel converts, LTV
    supports paid CAC, you can measure it.

24. **Q:** What has Meta Advantage+ automated? **A:** Targeting, creative
    optimization, budget allocation, bidding; manual targeting is retiring.

25. **Q:** Minimum meaningful Meta test budget? **A:** ~$50-100/day, ~50
    conversions/ad set/week to exit learning.

26. **Q:** 2026 attribution loss for many advertisers? **A:** ~50-70%
    (ATT opt-in ~18-25%).

27. **Q:** What does CAPI do? **A:** Sends conversion events server-side,
    recovering ~15-25% of lost attribution and feeding the algorithm.

28. **Q:** Why trust blended CAC over platform ROAS? **A:** Blended uses totals,
    so no attribution model can distort it.

29. **Q:** How to scale a winning campaign? **A:** Gradually (~20-30% every few
    days), 70/30 scale-vs-test, watching for CAC creep. Never 5x overnight.

30. **Q:** The 2026 AI-creative finding? **A:** AI ads match human overall, and
    perform best when they do not look like AI; produce with AI, reject the
    machine aesthetic.

## What surprised me this week

Write three lines in `_week.md` under "What I'd tell the me from last Monday."
The most useful answer is usually about sequence: which component you were
tempted to build out of order (usually paid before the funnel converted), and
what the ratios told you that your gut did not.

## Next week

Block 7 continues with the client-facing machinery: async dashboards,
productized-service ops, and the SOPs that make delivery systematic. The leads
you can now capture need somewhere to land and something repeatable to receive.
See [[block-7-onboarding-tracking/week-19-build-async-client-dashboard-or-project-tracking-for-agency--productizing-your-service-community-market-research/00-overview|Week 19]] (pending).

_last_verified: 2026-07-19_
