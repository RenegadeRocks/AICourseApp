---
type: lesson
block: block-8-wind-up-checklists
week: week-22
session_slug: final-thoughts-recap-checklists-1
day_of_cycle: 2
day_name: tue
date_due: 2026-10-13
tags:
  - capstone
  - checklist
  - audit
  - build
sources:
  - dunford-obviously-awesome
  - hamel-evals
  - cagan-inspired
  - anthropic-pricing-2026
  - saastr-pricing
last_verified: 2026-07-17
---

# The master build checklist

## Why this matters (operator framing)

A checklist is not a to-do list. It is a way to catch the step you skipped
because you were confident. Atul Gawande's argument for surgical checklists was
that experts fail not from ignorance but from omission under pressure, and the
same is true of solo builders shipping AI products.[^1] Today you get the
definitive end-to-end checklist for taking one idea from itch to systematized
business, and then you score your own business against it. The output is a
number and a shortlist of gaps. That shortlist is your Friday plan.

## Prerequisites

Everything, but especially the validation and monetization blocks. Each line
below links to its canonical home. If a line is unfamiliar, the fix is to reread
the link, not to reread this.

## How to use this

Score each item **0 / 1 / 2**:

- **0**: not done, or done on vibes with no evidence.
- **1**: done partially, or done once but not durable / not written down.
- **2**: done, evidenced, and repeatable without you improvising.

There are 35 items across seven stages, so the maximum is 70. Do not inflate
your scores; the point is to find gaps, and a flattering audit finds none. Total
at the end and read the band. Saturday's tool automates this scoring; today you
do it by hand so the gaps sting.

---

## Stage 1 — Idea (max 10)

The bet before you build. Skipping this stage is the most expensive mistake in
the course, because everything downstream inherits the error.

1. **The problem is a specific person's specific pain**, stated as a falsifiable
   bet, not a vague market. → [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/01-mon-idea-definition-from-itch-to-falsifiable-bet|idea as a falsifiable bet]]
2. **AI actually fits this problem**: you can articulate why a non-AI solution
   is worse, and you are not using AI because it is fashionable. → [[block-0-basecamp/week-03-decoding-real-business-problems-with-ai-i--decoding-real-business-problems-with-ai-ii/02-tue-when-ai-fits-a-problem|when AI fits a problem]]
3. **You have a niche, stated as a hypothesis** you could be wrong about, not a
   demographic. → [[block-1-problem-solving-outreach/week-02-importance-of-personal-branding--niche-discovery/04-thu-niche-as-a-hypothesis|niche as a hypothesis]]
4. **Positioning is explicit**: what you are, for whom, against what alternative.
   April Dunford's test: your best customers should recognize themselves in your
   first sentence.[^2] → [[block-1-problem-solving-outreach/week-02-importance-of-personal-branding--niche-discovery/04-thu-niche-as-a-hypothesis|positioning as hypothesis]]
5. **You know the unit of value** you will eventually charge for, even loosely. →
   [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/02-tue-pricing-strategy-value-metric-anchoring-packaging|value metric]]

## Stage 2 — Validated (max 10)

Evidence that someone other than you wants this. This stage separates the
surviving 5% from the pilots that die.

6. **You ran interviews designed not to flatter you**: no leading questions,
   past behavior over future intentions. → [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/03-wed-interviews-that-dont-lie-to-you|interviews that don't lie]]
7. **You treated any synthetic-user or AI-simulated feedback as a hypothesis
   generator, not evidence.** → [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/04-thu-synthetic-users-promise-and-peril|synthetic users]]
8. **You have a signal stronger than words**: a smoke test, a waitlist with
   real intent, a pre-payment, a signed pilot. → [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/05-fri-polls-smoke-tests-evidence-ledger|smoke tests and the evidence ledger]]
9. **You kept an evidence ledger**: decisions traced to the evidence that drove
   them, so you can tell what you know from what you hope. → [[block-4-test-validate-package/week-11-define-your-product-idea-validate-idea-using-ai--market-user-validation-interview-or-poll-potential-users/05-fri-polls-smoke-tests-evidence-ledger|the evidence ledger]]
10. **You defined a kill condition**: the evidence that would make you stop, and
    you would honor it.

## Stage 3 — Built (max 10)

The smallest thing that solves the validated problem, engineered well enough to
survive a real user.

11. **You built the smallest version up the prototype ladder**, not the full
    vision. → [[block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/04-thu-micro-prototype-ladder|the micro-prototype ladder]]
12. **The AI work has a real architecture**: retrieval, tools, and control flow
    are deliberate, not a single mega-prompt. → [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/02-tue-agent-architectures|agent architectures]]
13. **Context is engineered**, not stuffed — you manage what the model sees. →
    [[block-3-advanced-topics-voice/week-06-beyond-prompt-engineering-context-engineering--advanced-rags/01-mon-context-engineering-the-successor-discipline|context engineering]]
14. **You have evals**: a defined pass bar and a way to measure output quality
    before shipping. Hamel Husain's rule: your AI product needs evals, and vibes
    are not evals.[^3] → [[block-2-ai-employees/week-04-building-a-sales-agent--building-comprehensive-rag-ai-agent/06-sat-rag-evaluation|RAG evaluation]]
15. **Any code the AI generated was reviewed**, not merged on trust — the
    agentic-engineering discipline, not blind vibe-coding. → [[block-0-basecamp/week-01-basecamp-part-1-prompting-rags--basecamp-part-2-vibe-coding/06-sat-vibe-coding-part-2-discipline|vibe-coding discipline]]

## Stage 4 — Launched (max 10)

Getting it in front of people, on purpose, with instrumentation.

16. **The product has a UI/UX a stranger can use** without you narrating it. →
    [[block-5-product-building-principles/week-12-frontend-basic-uiux-design-principles--build-mvp-backend-connect-with-ai-workflows/01-mon-ui-ux-first-principles|UI/UX first principles]]
17. **Magic features are reliable**: the wow does not become a support ticket. →
    [[block-5-product-building-principles/week-13-making-your-product-feel-magic-with-ai--how-to-add-smart-features-that-wow-users/04-thu-reliability-of-magic|the reliability of magic]]
18. **Auth and security are real**: a paying user's data is protected, and you
    understand the lethal-trifecta risk in any agent that reads untrusted input.
    → [[block-5-product-building-principles/week-14-analytics-iteration-what-to-measure--scale-infra-auth-db-ui-polish/04-thu-auth-and-security-for-real-users|auth and security]]
19. **You launched on purpose**: a plan, not an accident, with a definition of
    what launch means for your stage. → [[block-6-launch-monetization/week-15-plan-product-hunt-social-strategy--publish-live-cold-outreach/01-mon-what-launch-means-in-2026|what launch means in 2026]]
20. **Outreach is not slop**: it complies with platform policy and reads like a
    human wrote it. → [[block-6-launch-monetization/week-15-plan-product-hunt-social-strategy--publish-live-cold-outreach/04-thu-cold-outreach-post-ai-slop|cold outreach post-AI-slop]]

## Stage 5 — Monetized (max 10)

Usage becomes revenue, and revenue clears cost.

21. **Pricing is anchored to a value metric**, not cost-plus or a round number. →
    [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/02-tue-pricing-strategy-value-metric-anchoring-packaging|pricing strategy]]
22. **You have tiers and an expansion path**: a way for a happy customer to pay
    you more. → [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/04-thu-tiers-upsell-hooks-and-expansion-revenue|tiers and expansion revenue]]
23. **Your margin is computed under real COGS**: current token prices, current
    tokenizer, inference plus overhead. Jason Lemkin's blunt version: if you do
    not know your gross margin, you do not have a business, you have a hobby.[^4]
    → [[block-6-launch-monetization/week-16-explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy--pricing-revenue-planning-pricing-tiers-upse/05-fri-revenue-planning-and-unit-economics|unit economics]]
24. **You can quote a real per-unit cost today**: recomputed against 2026 model
    prices, not the numbers you memorized months ago.[^5]
25. **Sales has a repeatable motion**: objections have answers, closes have a
    process. → [[block-1-problem-solving-outreach/week-01-getting-your-first-client--how-to-plan-scope-and-sell-ai-projects/06-sat-selling-ai-objections-and-closing|objections and closing]]

## Stage 6 — Grown (max 10)

Distribution that compounds, measured honestly.

26. **You have at least one growth loop**, not just a funnel you refill by hand.
    → [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/03-wed-growth-loops-vs-funnels|growth loops vs funnels]]
27. **A feedback engine turns usage into roadmap**, segmented so the loudest user
    does not set direction. → [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/01-mon-the-feedback-engine|the feedback engine]]
28. **You measure growth honestly**: no vanity metrics, and you know your
    stopping condition. → [[block-6-launch-monetization/week-17-feedback-metrics-setup-retargeting-or-re-engagement--growth-hacking-referral-loops/05-fri-the-growth-system-and-honest-measurement|honest measurement]]
29. **You have a lead-gen engine**: a magnet and an opt-in funnel that runs
    without you posting daily. → [[block-7-onboarding-tracking/week-18-create-a-lead-magnet-using-social-media-distribution--aquire-leads-using-paid-ads/01-mon-lead-magnets-that-convert|lead magnets]]
30. **If you run paid, you know your real payback**: CAC against margin, not
    revenue. → [[block-7-onboarding-tracking/week-18-create-a-lead-magnet-using-social-media-distribution--aquire-leads-using-paid-ads/04-thu-paid-ads-honest-primer|paid ads honest primer]]

## Stage 7 — Systematized (max 10)

The business runs without you being the bottleneck.

31. **Onboarding is an SOP**, not a heroic effort you repeat from memory each
    time. → [[block-7-onboarding-tracking/week-20-sops-for-onbaording-delivery-growth--build-community-paid-inner-circle/02-tue-onboarding-sops-the-first-30-days|onboarding SOPs]]
32. **Delivery is engineered so one build serves many customers.** → [[block-4-test-validate-package/week-09-packaging-selling-your-ai-agents--create-your-first-sellable-agent-package/03-wed-delivery-engineering-one-build-many-customers|one build, many customers]]
33. **You have a client dashboard or async tracking** so status is visible
    without a meeting. → [[block-7-onboarding-tracking/week-19-build-async-client-dashboard-or-project-tracking-for-agency--productizing-your-service-community-market-research/00-overview|the async client dashboard]]
34. **Community or an owned audience compounds** your distribution and retention.
    → [[block-7-onboarding-tracking/week-20-sops-for-onbaording-delivery-growth--build-community-paid-inner-circle/04-thu-building-community-the-compounding-moat|community as a moat]]
35. **Your prices, SOPs, and specs each live in one canonical place**: no
    contradictory copies. This is the fifth through-line from [[01-mon-the-whole-map|Monday]] applied to your own operation.

---

## Reading your score

- **0–25 — Early.** You have an idea and maybe a build. That is normal and fine.
  Your Friday plan is a validation-and-first-revenue plan. Do not systematize
  something no one has bought.
- **26–45 — Building.** You have a product and early money. Your gaps are
  usually in Stage 5 or 6: pricing on vibes, or growth with no loop. Fix the
  economics before the distribution.
- **46–60 — Launched and monetizing.** You have a business. Your gaps are usually
  Stage 7: it runs because you run it. Systematize before you scale, or scaling
  will break you.
- **61–70 — Systematized.** Rare and real. Your risk is now complacency and
  decay: the parts you scored 2 on may be quietly aging (Thursday). Re-audit
  quarterly.

The score is not a grade. A 30 who is honest is worth more than a 55 who
inflated. The gaps are the deliverable.

## Worked example

A solo builder audits her contract-review agent. Idea 9, Validated 8 (real
pilots, no written kill condition, so item 10 scores 1), Built 8, Launched 6 (no
real auth yet, item 18 scores 0), Monetized 5 (priced per seat with no margin
recomputation since spring, items 23 and 24 score 1 each), Grown 3, Systematized
2. Total 41 — "Building." The audit tells her exactly what to do next: write the
kill condition, ship auth, and recompute margin against current token prices
before she spends a rupee on growth. That is a Friday plan she can act on
tomorrow, not a vague "get more customers."

**Pass bar:** you have a total out of 70, a band, and a written list of every
item you scored 0 or 1, ranked by how much it blocks revenue.

## Common mistakes experts see

- **Auditing the aspiration, not the reality.** Score what exists, not what you
  intend to build.
- **Systematizing prematurely.** Building SOPs and dashboards for a product no
  one pays for is expensive procrastination.
- **Skipping Stage 2.** The most common 0s hide in "Validated," because building
  is more fun than validating.
- **Stale economics scored as 2.** A margin calculated on old prices is not
  "done." Item 24 exists to catch exactly this.
- **One flattering pass, never repeated.** This audit decays like everything
  else. An un-repeated audit is a snapshot of a business that no longer exists.

## Reflection questions

1. What is your total, and which stage holds most of your zeros?
2. Which single 0-or-1 item, if fixed, would unblock the most revenue?
3. Is anything you scored 2 actually running on months-old facts?
4. Where are you systematizing ahead of validating, and why?
5. If a mentor scored your business on this list, where would they be harsher
   than you were?

## My take (reviewer lens)

**Seibel** would like the checklist and distrust the score. His worry: a number
invites optimizing the number instead of the business. The mitigation is the
"gaps are the deliverable" framing — the total exists only to route you to the
worst gap, not to be maximized.

**Hamel Husain** would insist item 14 (evals) is under-weighted. In his view a
product without evals is not "Built," it is "demoed," and it should cap your
Stage 3 score. He has a point; if you scored Built high with no evals, treat
that as a red flag, not a rounding error.

**Boris Cherny** would flag that item 18's security line is doing a lot of work
in one checkbox. The lethal trifecta deserves its own audit for any agent that
touches untrusted input. He is right, and Wednesday's principles lesson gives it
the room this checklist cannot.

## Further reading

- **Must-read:** the linked canonical home for whichever stage holds your zeros.
  Reread it, then re-score that stage.
- **Recommended:** Atul Gawande, *The Checklist Manifesto* — why experts need
  checklists precisely because they are experts.[^1]
- **Optional:** April Dunford, *Obviously Awesome* — for sharpening item 4.[^2]

## Citations

[^1]: Atul Gawande, *The Checklist Manifesto: How to Get Things Right* (2009) — expert failure is dominated by omission, not ignorance; checklists catch skipped steps under pressure.
[^2]: April Dunford, *Obviously Awesome* (2019), aprildunford.com/obviously-awesome — positioning as the frame that makes your best customers recognize themselves immediately.
[^3]: Hamel Husain, "Your AI Product Needs Evals," hamel.dev/blog/posts/evals/ — vibes are not evals; define and measure a pass bar before shipping.
[^4]: Jason Lemkin, SaaStr, saastr.com — gross-margin literacy as the line between a business and a hobby; see also the unit-economics canonical home in Week 16.
[^5]: Anthropic, "Pricing," platform.claude.com/docs/en/about-claude/pricing — current per-Mtok rates (Opus 4.8 $5/$25, Sonnet 5 $2/$10 intro) and the updated tokenizer that changes per-unit cost. Corroborated by the July 2026 refresh master report. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
