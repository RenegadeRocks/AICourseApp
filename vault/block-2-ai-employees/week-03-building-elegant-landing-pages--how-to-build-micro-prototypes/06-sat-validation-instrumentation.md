---
type: lesson
block: block-2-ai-employees
week: week-03
day_of_cycle: 6
day_name: sat
session_slug: how-to-build-micro-prototypes
date_due: 2026-06-06
tags: [validation, instrumentation, posthog, session-replay, ai-moderated-interviews, outset, listen-labs, strella, mom-test, binomial-ci, gdpr, ccpa]
sources:
  - outset-nestle-case-study-2025
  - outset-series-b-globenewswire-2025
  - listenlabs-series-b-prnewswire-2025
  - strella-series-a-venturebeat-2025
  - maze-interview-studies-launch-2024
  - nngroup-ai-interviewers-2024
  - pearson-ai-moderated-methodological-2025
  - posthog-gdpr-compliance-docs-2025
  - clarity-gdpr-consent-2025
  - loeb-session-replay-legal-risks-2025
  - wilmerhale-web-tracking-2024-review-2025
  - kohavi-trustworthy-experiments-2020
  - kohavi-neweconomies-ab-science-2024
  - wilson-ci-corplingstats-2024
  - evan-miller-sample-size-calc
  - posthog-best-practices-funnels-2025
  - amplitude-tracking-plan-2024
  - fitzpatrick-mom-test-rules
  - torres-producttalk-weekly-2024
  - julian-shapiro-startup-handbook-landing
last_verified: 2026-04-17
word_count_target: 6000
---

# Validation instrumentation — the measurement layer that decides whether your prototype actually validated anything

## Why this matters

You have shipped a prototype by Friday night. A landing page, a fake-door, a concierge scaffold — something live on the internet with traffic pointed at it. The week has taught you how to compose conversion copy, how to pick a code-gen tool, how to override AI taste defaults, how to position a hypothesis on the pretotyping ladder, how to run the whole pipeline in a workday. None of it matters if by Wednesday morning you cannot *read* the thing you shipped.

The single most common prototype failure in 2026 is not "the page looked wrong" or "the tool was bad." It is that the operator deployed a prototype with no instrumentation beyond a Google Analytics tag and a half-read funnel chart, ran a hundred visitors through it, watched twelve of them "convert," told themselves the hypothesis had validated, and burned the next quarter building the wrong thing. The entire discipline of validation instrumentation exists to prevent that story — to force a prototype to earn its "validated" label with a numerator, a denominator, a confidence interval, a qualitative tape, and an explicit sunset condition.

By the end you will be able to (1) design a compact event model for a prototype across four reader domains — B2B SaaS, ecommerce, creator platform, consulting leadgen — with verb+object naming, funnel steps, and health metrics that survive contact with messy small-N data, (2) pick between PostHog, Microsoft Clarity, Hotjar, and a bare web-analytics stack on a cost / insight / compliance tradeoff, (3) use an AI-moderated interview platform (Outset, Listen Labs, Strella, Maze) with a Mom-Test-hardened script that keeps the AI from collapsing into survey theater, (4) compute Wilson-score confidence intervals for 6/50, 12/100, 60/500 and explain why three observations with the same point estimate tell you very different things, (5) write a go / iterate / kill decision rule *before* data arrives, such that the decision is forced by data rather than argued out of it afterward, and (6) navigate the 2024–26 GDPR/CCPA landscape for session replay without triggering a wiretap class action on your own prototype.

The capability delta is precise. A sharp generalist ships a prototype and asks "did it work?" An AI-catalyst lead ships one and can say, before data arrives, *what observation will count as success, failure, or ambiguous, and what the next experiment is for each outcome*.

## Prerequisites

- A prototype live on the internet with at least an analytics snippet installed (from Friday's pipeline).
- Working vocabulary for funnel, cohort, event, property, session — the generalist-cohort level is enough.

## Layer 1 — The event model is the instrument, not the tool

The tool you pick — PostHog, Amplitude, Mixpanel, Clarity — is a distant second in importance to the event model you design before you pick it. A bad event model in the best tool produces unreadable data; a good event model in a mediocre tool produces clean signal. Start here.

### The compact taxonomy rule

PostHog's own best-practices documentation puts this bluntly: instrument the top 5–10 moments that map to your core user journey (acquisition → activation → adoption → retention → expansion), use verb-object naming, snake_case properties, and avoid PII in payloads.[^1] The same principle sits at the core of Amplitude's and Mixpanel's tracking-plan guidance: a tracking plan is a living document that specifies what events and properties exist and what they mean, and serves as the single source of truth an engineer or AI agent can instrument against.[^2][^3]

The bias for a first-prototype operator is always the same: over-instrument. Log every click, every scroll, every hover, every microinteraction, because "what if we need it later?" The predictable result is a dashboard that no one opens because it is thirty charts deep and none of them correspond to the question the prototype was meant to answer. Amplitude's specific warning — "only capture what you need and start small" — is the right posture.[^2] Eight events is plenty for a prototype. Twelve is the ceiling before reader fatigue sets in. If you have twenty, you have not been strict enough about what question the prototype is asking.

### The four-domain event model, concrete

Every reader of this vault comes from a different field. An event model written for one industry reads as alien to another, so four in parallel. Same skeleton: (a) *landed* event on page render, (b) one or two *qualified-intent* events that mark real engagement, (c) the primary *conversion* event, (d) a *confirming* event that distinguishes a real conversion from a fat-finger click, (e) two or three *health metrics* (bounce, time-on-page, scroll depth).

**B2B SaaS leadgen** (fake-door "AI contract-redline assistant" targeting Series A legal ops):
```
landing_page_viewed    { variant, utm_source, viewport_class }
hero_cta_clicked       { cta_label, time_to_click_sec }
pricing_section_viewed { scroll_depth_pct, dwell_sec }
demo_form_submitted    { email_domain_category, company_size_bucket }
calendar_slot_booked   { days_to_meeting }
```
Conversion: `demo_form_submitted`. Confirming: `calendar_slot_booked` — B2B demo forms are fat-finger- and bot-prone; a "submission" that never becomes a booking is noise at 30–50% of observed rate. The `email_domain_category` property (personal vs corporate vs disposable) is the property that distinguishes "validated the B2B hypothesis" from "converted gmail.com tire-kickers."

**Ecommerce pretotype** (limited-run artist-collab DTC candle, 200 units):
```
product_page_viewed    { product_sku, utm_source }
image_carousel_swiped  { max_image_index_reached }
add_to_cart            { product_sku, qty }
checkout_started       { cart_value }
order_confirmed        { order_id, order_value }
```
Conversion: `checkout_started`; confirming: `order_confirmed`. Shopify's baseline cart-abandonment sits at 65–80% — a `checkout_started` number without a `order_confirmed` number overstates real conversion by 3–5x.

**Creator platform waitlist** (newsletter-to-paid-course smoke test):
```
landing_viewed         { utm_source, referrer_category }
hero_video_played      { watch_pct }
waitlist_email_entered { email_hash, personal_or_work_email }
waitlist_confirmed     { confirm_latency_sec }
referral_link_clicked  { referrer_email_hash }
```
Conversion: `waitlist_email_entered`; confirming: `waitlist_confirmed` (the email-confirmation click — filters the 20–40% of address-only signups that never click through). `referral_link_clicked` is the event most creator pretotypes skip and the one that predicts whether the waitlist has organic energy or is an artifact of the launch tweet.

**Consulting leadgen** (fractional-CFO service microsite):
```
homepage_viewed        { utm_source }
case_study_viewed      { case_study_slug, dwell_sec }
intro_call_booked      { slot_offset_days }
intro_call_attended    { attendance_confirmed_by }
proposal_sent          { proposal_id }
```
Conversion: `intro_call_booked`; confirming: `intro_call_attended`. Intro-call no-show rates run 25–40%; a prototype that optimizes `intro_call_booked` without tracking attendance is optimizing for booking vanity.

Pattern across all four: *conversion alone is not enough*. The confirming event — requiring a second, costlier action — collapses fat-finger and bot noise and distinguishes real intent from survey-theater intent. Instrument both.

### Properties: what to attach, what not to attach

Properties are what turn an event from a counter into a pivotable object. Three rules.

**Attach what makes a cohort.** Variant label (for A/B splits), utm_source (for channel attribution), viewport class (mobile vs desktop splits matter — we know from Friday that 75%+ of 2026 traffic is mobile), bucketed firmographic where available (company_size_bucket rather than raw company name).

**Standardize once, propagate everywhere.** PostHog and Amplitude both warn that inconsistent naming is the single highest-leverage data-quality failure mode.[^1][^2] Decide `utm_source` vs `source` vs `channel` on day one, write it in the tracking plan, and have Claude Code enforce it on every new event it helps instrument. This is the kind of discipline that is cheap on day one and nearly impossible to retrofit on day ninety.

**Never attach PII.** Email addresses, raw IP, full names, exact coordinates — none of these belong in event properties. PostHog's GDPR guidance calls this out explicitly: because PostHog automatically captures data that *can* be personal data, the operator must provide a consensual mechanism and must redact at the property layer before it hits storage.[^4] Using an `email_hash` rather than a raw email keeps cohorting intact without creating a compliance surface you did not plan for.

## Layer 2 — Session replay — indispensable, invasive, and newly dangerous

Session replay is the tool that records a visitor's mouse movements, clicks, scrolls, and (depending on configuration) form inputs, and lets you play back the session as a video. For N<200 prototypes where your funnel numbers are too small for any statistical test, session replay is often the highest-information-density instrument you own. It is also the one most likely to get you sued in 2026.

### What replay tells you that a funnel cannot

At N=50 visitors and 6 conversions, your funnel chart is four bars of ambiguous height. Session replay gives you twenty-five two-minute videos. You watch the first five. You see three visitors bounce within four seconds (the hero failed), one visitor scroll to pricing, hover on the CTA, and leave (the pricing objection killed them), and one visitor engage fully and convert (the proof stack worked). The funnel says "12% conversion." The replay says "hero is broken for 60% of traffic, pricing is the second-order blocker, proof stack is fine." Those are completely different next-step recommendations. The funnel gives you a number; replay gives you a *diagnosis*.

This is why session-replay adoption among prototype-stage operators is near-universal in 2026. Microsoft Clarity is free and unlimited; PostHog offers 5,000 session recordings per month on the free tier with EU hosting;[^5] Hotjar and FullStory sit at the premium end with richer filtering. The market shape has been roughly stable since 2023.

### The 2024–2026 legal collapse around replay

Session replay is now the subject of the most active privacy-litigation wave in the US. WilmerHale's Feb 2025 year-in-review documents "various class action cases" filed in 2024 "challenging these practices under myriad legal theories on the grounds that the collection of this data, shared with third parties, is nonconsensual and an illegal breach of user privacy."[^6] Loeb & Loeb's July 2025 advisory is sharper: where session-replay captures visitor *communications* (chat, form inputs, search queries), plaintiffs allege violation of state wiretap laws.[^7] The theory: recording a user's inputs in real time and transmitting to a third-party vendor constitutes two-party recording of a one-party communication, triggering state wiretap liability in two-party-consent states (California chief among them) independent of any federal framework.

The regulatory layer tightened in parallel. Microsoft Clarity announced that from 31 October 2025, session recordings, funnels, and heatmaps "will be disabled for visitors in the EEA, UK, and Switzerland" unless explicit consent is implemented via the Clarity Consent API or an integrated CMP.[^8] PostHog masks all inputs and text by default, offers PostHog Cloud EU with IP capture disabled by default, and enters DPAs on request.[^4]

The 2026 operator checklist for session replay on a prototype:

1. **Consent banner before record** — if your traffic touches any EEA, UK, Swiss, or California visitor, explicit consent must be collected before the replay script fires. Scroll-as-consent banners are now CPPA-flagged as dark patterns.[^9]
2. **Mask inputs by default** — never record form-field content without a specific research need and an explicit consent surface.
3. **No recording on payment or auth pages** — PCI-adjacent and the fastest path to a demand letter.
4. **EU hosting if you have any EU traffic** — PostHog Cloud EU exists; the cost delta is minor, the compliance delta is massive.
5. **Document retention** — 30 days default. "We kept replays indefinitely" has been a plaintiff-bar gift in 2024–25 filings.

The live controversy: replay is either *indispensable* diagnostic (closes the gap between N=50 funnel ambiguity and actual diagnosis) or *surveillance-creep* (a wiretap 76% of sites deploy with inadequate consent, per the 2024 Global Privacy Enforcement Network review[^9]). Honest answer: both. The operators who get sued are the ones using replay as shipped by default, with no consent surface and no masking discipline.

## Layer 3 — AI-moderated interviews — the 2024–2026 category that actually ships

Separate from quantitative instrumentation is the qualitative layer: 1:1 conversations with actual humans who touched your prototype. The old rule — five interviews beats a hundred survey responses for prototype-stage feedback, because the research job at N<100 is pattern-discovery rather than effect-estimation — is unchanged. What changed in 2024–2026 is *who runs the interview*.

### The category, by the numbers

Four platforms anchor the AI-moderated-interview category in 2024–2026, each with verifiable customer disclosures:

- **Outset.ai** — $17M Series A (June 2025, 8VC lead) + $30M Series B (Dec 2025, Radical Ventures lead, M12/Microsoft participating), total $51M, 8x 2025 revenue growth.[^10] Disclosed customers: Microsoft, WeightWatchers, Away, Nestlé, HubSpot, Uber. The Nestlé deployment is the deepest public case: 100+ concepts, 7+ brands, 5+ countries, "10x" the participant count of traditional qual (benchmarked at 20–30 people), and Michael Widenmeyer (Nestlé Consumer Insights Sr Manager) disclosing "participants shared more than twice as much depth with the AI moderator" as with their next-best method.[^11]
- **Listen Labs** — $27M (Sequoia, 2025) + $69M Series B (Ribbit lead, 2025), $500M+ valuation.[^12] Disclosed: Microsoft, Sweetgreen, Perplexity, Robinhood, Canva, Chubbies. eWeek profile: "quietly interviewing customers for Microsoft."
- **Strella** — out of stealth Oct 2024, $14M Series A (Oct 2025, Bessemer lead).[^13] Disclosed: Amazon, Duolingo, Apollo GraphQL, Chobani. Ritual case study reports 24% revenue growth after AI-moderated pricing research. Brian Santiago (Apollo GraphQL): "Before Strella, studies took weeks. Now we get insights in a day."
- **Maze** — Interview Studies launched June 2024, AI transcripts/summaries/highlights on top of moderated or unmoderated video, with recruitment + scheduling + conferencing in one workflow.[^14] Positioning: AI-augmented human moderation rather than full AI moderation — which matters for the controversy below.

### The live controversy — genuine signal or survey theater?

Two positions, both held seriously.

**Position A — AI-moderated interviews produce better data at scale.** The disclosure evidence is loud. Nestlé's consumer-insights team on record that participants share "more than twice as much depth" with an AI moderator vs next-best method[^11] is a claim a $320B company put its Senior Manager's name on. Apollo GraphQL's Product Design Manager on record that Strella compresses weeks of research into hours[^13] is a throughput claim with a credibility structure — measurable and falsifiable by his own team. The theoretical case: participants feel less judged, face no time pressure, can talk at any hour, and are freed from social-desirability effects that distort human-moderated research. Aaron Cannon (Outset founder) has made this argument publicly across 2024–25.

**Position B — AI moderators collapse the exploratory interview into a structured survey.** Carl Pearson's May 2025 methodological critique is the sharpest articulation.[^15] AI-moderated interviews "collapse the exploratory sequential design into a single moment" — they simultaneously define what counts as a category of insight (should be generative) and count how many people fall into it (should be evaluative). The classifier prompts do both jobs at once; at scale, you count categories before defining them. NN/g's 2024 study, based on direct observation of AI-moderated interviews in production, reached a similar conclusion: AI interviewers "did not give participants a chance to weigh in"; rapport-building was absent; psychological nuance, body-language reading, and moment-to-moment adaptation were not present.[^16] NN/g's recommendation — "use them to supplement, not to replace" — is the diplomatic version of "not yet suitable for semistructured or in-depth discovery interviews."

Teresa Torres's weekly-interview discipline assumes human moderation because the exploratory work (pushing past three whys, sensing performance vs disclosure) is what AI currently cannot do.[^17] Rob Fitzpatrick's Mom Test is structurally *harder* for an AI interviewer, not easier, because every Mom Test rule is about *what the interviewer must not do in the moment* based on a signal only a human can currently read.[^18]

**Resolution for a prototype-stage operator.** Run AI-moderated interviews for the *structured-feedback* surface — "tell me what you expected, what confused you, what would stop you from using it" — where the question scope is defined in advance and reach matters. Run human-moderated interviews (yourself, five calls) for the *generative* surface — "tell me about the last time you dealt with [job]; what did you try, what did you switch away from, what almost made you give up." Mixing the two is a division of labor, not a hedge. Reach and consistency on the structured surface; depth and adaptation on the generative. Do not substitute one for the other.

### A Mom-Test-hardened AI interview script

Taking Fitzpatrick's three core rules[^18] and applying them as literal guardrails on an AI interviewer is the operational technique. A seven-question script that survives the Mom Test, for a concierge-stage prototype that claims to help a specific professional do a specific job faster:

1. **Past behavior, not future preference.** "Walk me through the last time you had to [the job the prototype helps with]. What day was it? What were you trying to accomplish?" *Bans: any variant of "would you use a tool that…"*
2. **What did you try first, second, third?** "What was the first thing you reached for? What were you doing before that stopped working?" *Bans: "what would you hope such a tool could do?"*
3. **Cost of the current approach.** "How long did the whole thing take? What did it cost you — in time, in dollars, in anything else?" *Bans: leading on "was it frustrating?"*
4. **The switch moment.** "Was there a moment in that process where you almost gave up? Almost switched to something different? What happened?"
5. **The actual competitive set.** "If [the thing you were using] disappeared tomorrow and you had to get [outcome] done, what would you reach for? Why that, not something else?"
6. **What would a 'great' outcome have looked like.** "If that had gone perfectly, how would you have known? What would you have been comparing against?" *This is the Ulwick outcome-probe, surfacing the metric the person was implicitly judging by.*
7. **Commitment ask, not hypothetical.** "If I built [the prototype], what would make you spend the next hour trying it? Not a year from now — this week. What would have to be true?" *The commitment question filters polite respondents from the ones who have real energy around the problem.*

The move that distinguishes a Mom-Test-hardened AI script from a survey-theater AI script is the refusal of hypotheticals in questions 1–5 and the substitution of commitment specificity in question 7. A script that opens with "would you be interested in a tool that…" has already lost — the respondent will say yes to be polite, the AI has no way to probe past the politeness, and you have collected 50 worthless "yes" responses that your funnel dashboard will count as "validation." The Mom Test rules are the *only* guardrails that make the AI-moderated mode produce useful data at the prototype stage, because without them the AI's inability to probe in the moment compounds with the respondent's instinct to please.

## Layer 4 — Small-N decision math — Wilson intervals and what they actually tell you

Now the part the spec demanded, in full. A prototype with 50 visitors and 6 conversions is 12%. A prototype with 100 visitors and 12 conversions is 12%. A prototype with 500 visitors and 60 conversions is 12%. All three have the same point estimate. None of them mean the same thing. The three Wilson-score 95% confidence intervals tell the real story.

### The Wilson score in two paragraphs

The binomial confidence interval of a proportion is the range within which, given *n* trials and *k* successes, the true underlying proportion plausibly sits at the 95% level. The classical normal-approximation interval (taught in every intro stats class) fails badly for small *n* or for proportions near 0 or 1 — it can produce zero-width intervals, overshoot negative probabilities, and generally misstates uncertainty.[^19] E.B. Wilson's 1927 interval remains the recommended general-use formula nearly a century later because it handles small *n* and skewed proportions cleanly, producing asymmetric intervals that never overshoot and remain stable from around n=10 upward.[^19][^20]

The Wilson-score 95% CI for a proportion *p̂ = k/n* is:

```
p_wilson = (k + z²/2) / (n + z²)
margin   = (z / (n + z²)) * sqrt(k(n-k)/n + z²/4)
CI       = [p_wilson - margin, p_wilson + margin]
```

where z = 1.96 for a 95% confidence level. You do not need to compute this by hand — ask Claude Code or use any reputable statistics calculator — but you need to understand what the output means.

### The three 12%-point-estimates, worked

**Case A — 6 / 50.** Wilson 95% CI = [5.6%, 24.2%]. Width ≈ 18.6 percentage points.

**Case B — 12 / 100.** Wilson 95% CI = [7.0%, 19.8%]. Width ≈ 12.8 percentage points.

**Case C — 60 / 500.** Wilson 95% CI = [9.4%, 15.2%]. Width ≈ 5.8 percentage points.

All three are "12%." The first says "the true conversion rate of this prototype, given the data, is plausibly anywhere from 5.6% to 24.2% — a 4x range." The second narrows that to roughly a 3x range. The third narrows it to a ~1.6x range. The inference differs completely.

**Case A (6/50) inference.** You have seen a 12% conversion rate. You have *not* excluded the hypothesis that the real rate is 6%, which in most B2B contexts would kill the project. You have also not excluded the hypothesis that it is 24%, which in most B2B contexts would be a clear green-light. The 6/50 result, by itself, tells you essentially nothing that could drive a go/no-go decision. The correct next action is almost always *more traffic* — not "ship it," not "kill it." If your decision threshold was 10%, you cannot tell from 6/50 whether you cleared it. If your decision threshold was 15%, you also cannot tell. The only decision 6/50 reliably supports is "run it to 200 visitors before reading again."

**Case B (12/100) inference.** Tighter, but not much. You have roughly excluded rates below 7% and above 20%. If your decision threshold was "kill below 5%," you can now kill or continue. If your threshold was "ship above 20%," you can make that call. If your threshold was somewhere in the middle — as almost all real thresholds are — you still cannot force the decision from this data alone, and more traffic or a qualitative supplement is the right next step.

**Case C (60/500) inference.** Now the interval is tight enough to drive a decision. You have excluded rates below 9.4% and above 15.2%. If your pre-registered threshold was "ship at 10% or better," this data ships it. If it was "kill below 8%," this data continues. If it was "ship above 18%," this data kills it. 500-visitor sample sizes are where prototype-stage A/B thinking starts to become tractable.

### The operator rule

Ronny Kohavi's treatment of this in *Trustworthy Online Controlled Experiments* is the canonical source, and his publicly circulated 2024 example drives the point home: a paper claimed a 55% lift for rounded buttons based on 919 visits, and three replications at 2,000x the sample size returned lift estimates of 0.16%, 0.29%, and 0.73%, *none* statistically significant.[^21][^22] The 55% original was artifact. Prototype-stage operators who are not aware of this failure mode routinely "validate" hypotheses at N=50 that would completely collapse at N=5,000.

The discipline the Kohavi frame installs, for prototype work:

- **Compute the interval before you interpret the point estimate.** Never quote a "12% conversion" without its CI width. The width is more diagnostic than the point.
- **Pre-register your thresholds.** Before you launch the prototype, write down: "I will ship if conversion ≥ X% with CI lower bound ≥ Y%. I will kill if CI upper bound ≤ Z%. I will iterate and gather more data if neither condition holds." This is what transforms a vanity dashboard into a decision instrument.
- **Do not run "A/B tests" at prototype scale.** A proper two-arm A/B test at 12% baseline trying to detect a 2-point lift requires, per Evan Miller's calculator at 95% confidence and 80% power, roughly 4,000–5,000 visitors per arm.[^23] A "solo operator with 100 visits A/B testing their hero copy" is not running an experiment in the Kohavi sense; they are collecting anecdotes with statistics theater on top.
- **At N<500, replay and interviews outweigh numbers.** Session replay plus five Mom-Test-hardened interviews will tell you more about a prototype at N=50 than any funnel chart. Save the quantitative rigor for when you have the traffic to deserve it.

## Layer 5 — The decision rule, pre-registered

Bringing it together: the prototype instrumentation brief for any reader field.

1. **State the hypothesis in one sentence with an explicit outcome metric.** Example for a B2B SaaS prototype: *"Among qualified Series A legal-ops leaders exposed to this landing page via LinkedIn Ads, ≥8% will submit a demo form with a corporate email domain within 14 days of launch."*
2. **State the decision rule.** Example: *"Ship if observed rate ≥ 8% AND Wilson 95% CI lower bound ≥ 5% AND ≥ 500 visitors reached. Kill if Wilson CI upper bound ≤ 4% at ≥ 500 visitors. Extend data collection if neither threshold is crossed at 500 visitors."*
3. **State the qualitative overlay.** Example: *"Independent of quantitative outcome, run 5 Mom-Test-hardened AI-moderated interviews (via Outset or Strella) with respondents matching the ICP. If ≥3 of 5 interviews surface a previously-unknown objection or unmet outcome, iterate on the copy regardless of quant result."*
4. **State the replay review ritual.** Example: *"Watch the first 10 session replays within 24 hours of launch. If ≥3 show bounces within 4 seconds on hero, freeze campaign until hero is rewritten."*
5. **State the compliance posture.** Example: *"Consent banner deployed via [CMP]. Clarity/PostHog masking on by default. EU hosting on. 30-day replay retention. No replay on payment/auth pages."*

The decision rule, pre-registered, is what makes validation instrumentation *validation* rather than confirmation-bias with a dashboard. The operators who ship and iterate productively in 2026 are the ones who wrote down their go / kill / iterate thresholds before the first visitor arrived. The ones who stall are the ones who wait for the data and then argue about what it means.

## Operator case studies — small-N decisions, well and badly made

**The Ritual pricing test (Strella, 2024–25).** Nutrition DTC brand Ritual used Strella's AI-moderated interviews to test price-point hypotheses before public commitment. Disclosed outcome: 24% revenue growth post-rollout.[^13] The structural move: AI-moderated interviews were used for *depth* on willingness-to-pay conversations (cost justification, perceived value tiers, substitute behaviors), feeding a bounded quantitative test. Strella's "thousands of interviews" at "90% time savings" is a throughput claim; Ritual's 24% growth is a consequence claim, and the consequence ran through interview → hypothesis → bounded quantitative test — not through AI-moderated A/B.

**The Nestlé concept validation (Outset, 2024–25).** Nestlé's 100-concepts × 7-brands × 5-countries deployment, disclosed by Michael Widenmeyer, is the largest public AI-moderated-research case as of early 2026.[^11] The structural move: Nestlé provided "concepts plus consumer target criteria," Outset ran interviews *and* analysis, explicit throughput "10x" traditional qual. This works because the research question — "which of 100 concepts resonates with which segment in which country" — is exactly the structured-feedback surface NN/g and Pearson flag as legitimate for AI moderation.[^15][^16] Nestlé is not using Outset to generate unknown insights; it is running a very large comparison of known concepts against known segments. Inside the frame where AI moderation currently works.

**The Listen Labs / Microsoft pattern.** Listen Labs' disclosed customer list (Microsoft, Sweetgreen, Perplexity, Robinhood) is enterprise-scale; eWeek profiled Listen as "quietly interviewing customers for Microsoft."[^12] The revealed preference — $500M+ valuation, $69M Series B, Sequoia-and-Ribbit backed — is that the enterprise CX-research market will replace significant human-moderated capacity with AI moderation at scale. But none of the disclosed customers are using Listen for prototype-stage solo-operator work; they use it for post-launch monitoring at volumes where structured-feedback mode fits. For a prototype-stage operator, the rule distilled from all three cases: use the AI-moderated layer for *reach* on structured questions; keep the generative work in your own hands.

## Runnable experiment — instrument yesterday's prototype

Run this against Friday's deployed prototype. Plan for a 3–4 hour session.

**Phase 1 — Event model, in Claude Code.** Open Claude Code in the prototype's repo. Ask: *"Given this prototype [paste the one-line hypothesis from Thursday and the deployed URL], design an 8-event event model following the compact-taxonomy rule. Name them verb-object, snake_case properties, include a conversion event and a confirming event, three health metrics. Output as a Markdown tracking-plan document and as a PostHog-ready JSON snippet of the capture calls. Flag any event that would require consent before firing."* Save the Markdown output to `code-lab/week-03/tracking-plan.md`.

**Phase 2 — Deploy instrumentation, in Claude Code.** Instruct: *"Using the tracking plan in `code-lab/week-03/tracking-plan.md`, instrument the deployed prototype. Add the PostHog snippet to the site with EU hosting enabled, masking on, IP capture off. Add a cookie consent banner that blocks the PostHog script until consent is granted. Output the diff of the HTML/Next.js changes. Deploy to Vercel. Verify the first event fires by sending a test visit and confirming it in the PostHog dashboard."*

**Phase 3 — Drive N≥50 visitors.** Use one of: LinkedIn Ads (B2B), Reddit organic in a relevant subreddit (creator / consumer), cold outreach to your Block 1 Week 1 ICP list (consulting / B2B), X organic from your warm audience. Target 50 unique sessions within 72 hours.

**Phase 4 — Wilson-interval decision, in Claude Code.** Ask: *"Given my current funnel [paste the numerator/denominator per step], compute the Wilson-score 95% CI for the conversion event. Interpret against my pre-registered thresholds [paste thresholds from Layer 5]. Recommend: ship, kill, iterate, or gather more data. Justify based on CI width."*

**Phase 5 — Session replay review.** Watch 10 replays manually. For each, note: bounce location, scroll depth reached, and the single highest-leverage friction point observed. In a 200-word summary, identify the modal friction mode.

**Phase 6 — AI-moderated interview round.** Sign up for the Outset, Strella, or Listen Labs trial (or use Maze's AI Moderator tier). Load the seven-question Mom-Test-hardened script from Layer 3. Recruit five respondents matching your ICP — either from your opt-in list, your network, or the platform's own participant pool. Run the interviews (asynchronously, 48-hour window). Review the AI-generated synthesis with skepticism: look specifically for questions where the AI failed to probe, participants who slipped into hypotheticals without being redirected, and categories the AI "discovered" that were actually asked by the script.

**Phase 7 — The decision memo.** Ask Claude Code: *"Given funnel data [paste], Wilson CI [paste], replay diagnosis [paste], and five interview transcripts [paste], write a go / kill / iterate memo against my pre-registered decision rule. For each evidence layer — quantitative, replay, qualitative — state whether it supports, opposes, or is inconclusive. Recommend next experiment."* Save to `code-lab/week-03/decision-memo.md`.

Expected observation pattern: at N=50 the quantitative layer is almost always inconclusive; the replay layer reveals a friction point you did not predict; the interview layer surfaces one objection invisible in both replay and funnel; and the memo ends either "iterate on the specific friction and retest" or "gather more data" — almost never "ship" and almost never "kill." Operators find this disappointing at first and liberating once internalized. A prototype does not have to close a decision on its first 50 visitors; designing instrumentation so it *doesn't* falsely close is the entire point.

## Problem set

1. **Event model across domains.** For one prototype you are currently running or considering (real, not hypothetical), design the compact event model per Layer 1 using the skeleton (landed → qualified-intent → conversion → confirming → health). Write the tracking plan as a Markdown table: event name, properties, firing condition, why it earns its place. Must not exceed 12 events. Explicitly identify your conversion event and your confirming event, and justify the split.

2. **Session replay compliance audit.** Pick the session-replay tool you intend to use (or are using). Against the five-item Layer 2 checklist, audit your current deployment. For each item, state: compliant, non-compliant, or not-applicable, and for each non-compliant item, specify the exact configuration change required. If you have EU/UK/CA traffic and no consent banner, flag this as a priority-0 remediation with a reasoned 30-day fix.

3. **Wilson-interval worked exercise.** Without using a calculator, estimate the Wilson 95% CI widths for these four observations: (a) 3 / 25, (b) 8 / 80, (c) 30 / 300, (d) 150 / 1500. Order them from widest CI to narrowest. Then compute the actual CIs with any tool. How close was your intuition to the numbers? Write 150 words on what your gut got right and wrong, and which of the four observations would support a go / kill decision if your threshold was "ship at ≥10% with CI lower bound ≥ 6%."

4. **The AI-moderated-interviews position paper.** Take a defensible written position on the live controversy: *"AI-moderated interviews produce useful signal at N=5 that would take 20+ human-moderated sessions to reach."* Defend or refute in 400 words, citing at least one source from Position A (Outset/Strella/Listen Labs customer disclosures) and one from Position B (NN/g 2024 study, Pearson 2025, Torres / Fitzpatrick methodological position). Your position must specify the *kind* of signal the claim applies to — generative vs evaluative, structured vs semi-structured. A position that answers "yes" or "no" without this scoping fails the rubric.

5. **The pre-registered decision rule.** For the prototype in problem 1, write the five-item decision rule per Layer 5. Share it with one peer before launch. Commit to not modifying it after data starts arriving. Thirty days later (or at end-of-experiment, whichever comes first), write a 300-word retrospective: did the rule force the decision, or did you argue your way around it? If you argued around it, what pressure specifically caused you to override the pre-registration — and how would you write the rule differently next time to absorb that pressure in advance?

## Common failure modes at scale

**The self-reported-conversion trap.** Ecommerce operators instrument `checkout_started` because it is easier than `order_confirmed`. Shopify's baseline cart-abandonment is 65–80% — `checkout_started` overstates real conversion by 3–5x. Operator sees 15% at prototype, ships, discovers real purchases are 3.8%. Fix: always pair conversion with a confirming event; report confirming rate externally.

**The dashboard-without-thresholds trap.** Operator deploys PostHog, wires 20 events, sees numbers, declares "validation" — never wrote down what would falsify. Motivated reasoning wins. Fix: pre-registered thresholds in writing before launch. No pre-registration, no post-hoc conclusion.

**The consent-banner-after-deployment trap.** Operator deploys replay without consent on a prototype that attracts EU traffic. Three months later, retrofits consent; first three months of data potentially unlawfully collected. At minimum a data-hygiene loss; at worst, per the 2024 class-action wave,[^6][^7] a liability surface. Fix: consent banner on day one, even for "just a test." Prototype vs production is operator fiction; to the regulator, both are users.

**The AI-moderated-interview-as-survey trap.** Operator runs 200 "interviews" on Outset that are actually 6-question preference surveys with open-text. Concludes concept validated. Post-launch discovers respondents said yes to be polite, never intended to buy, and the real struggle was orthogonal to what got asked. Fix: hardcode Mom Test rules into the script; supplement with five human-moderated generative interviews. Complementary, not substitutable.

**The A/B-test-at-N=100 trap.** Two hero headlines at N=100 per arm, 4-point lift observed, "copy A wins" — rolls out. At N=5000 per arm the lift is 0.2 points, not significant. The exact pattern Kohavi has documented.[^21][^22] Fix: either run to the MDE sample size (Evan Miller's calculator[^23]), or accept the prototype stage is a single-arm pre-registered test, not a comparative A/B.

## Open questions — what is not settled

**Does the AI-moderated-interview category remain useful when participants realize they are talking to AI?** The 2024–2026 wave of customer disclosures assumes participants treat the AI moderator roughly as they would a human-moderated session. As participant awareness of the mode increases — and NN/g's 2024 findings already show rapport-building is shallower[^16] — the depth-of-disclosure claim from Outset's Nestlé case may attenuate. No public longitudinal data yet resolves this.

**Do Wilson intervals and pre-registered thresholds transfer to non-binary conversion surfaces?** The math in Layer 4 is clean for binary outcomes (converted / didn't). Revenue-per-visitor, time-to-conversion, multi-step-funnel-completion, and open-ended prototype outcomes (did this user continue past day 7?) require different intervals and non-trivial power analyses. The prototype-stage operator literature on small-N non-binary outcomes is thin. Kohavi's treatment in *Trustworthy Online Controlled Experiments* remains the best reference for non-binary cases, but the operational synthesis for solo-operator scale is unwritten.

**Is session replay's legal exposure containable, or does the 2024–26 class-action wave kill it for SMB use?** The Loeb 2025 analysis[^7] describes a settled framework (wiretap theory, two-party consent states, consent-management remediation). The WilmerHale 2024 review[^6] describes an active litigation wave without a settled appellate answer. Whether the remediations (consent banners, EU hosting, masking) hold up to adversarial plaintiffs' bars in 2026 and 2027 is a real open question. A prototype-stage operator may reasonably choose to forgo session replay entirely as a compliance hedge — at the cost of the diagnostic leverage it provides.

## Reviewer lens — named critics, specific disagreements

- **Teresa Torres (producttalk.org) on Layer 3's division-of-labor.** Torres would push back on "run human-moderated interviews for the generative portion — yourself, five calls" by arguing the *weekly cadence* is the discipline, not just the generative/structured split. An operator running five human interviews once per prototype is still doing episodic discovery; Torres wants five per week, indefinitely, as the muscle.[^17]

- **Rob Fitzpatrick (momtestbook.com) on the Mom-Test-hardened AI script.** Fitzpatrick's position is that the Mom Test rules *cannot* be fully encoded as a script because the hard part is in-the-moment restraint — noticing the respondent has slipped into hypothetical mode and redirecting without leading. He would argue the "seven questions hardcoded into the AI" framing substitutes rule-following for judgment, precisely the failure mode he wrote the book to combat.[^18] Counter: the script is a floor for the structured-feedback surface where question-scope tightness mitigates the AI's adaptation gap.

- **Ronny Kohavi (exp-platform.com) on Layer 5's pre-registered decision rule.** Kohavi would argue the threshold is the surface; the deeper discipline is SRM checks, A/A tests, and pre-specified stopping rules that account for peeking. Layer 5's pre-registration is necessary but insufficient — without an SRM check or stopping rule, pre-registration is still gameable by unconsciously choosing when to "read" the data.[^21]

- **James Hawkins (PostHog) on the compact-taxonomy rule.** Hawkins prefers capturing broadly and cleaning at query time (PostHog's autocapture philosophy). He would push back on Layer 1's "eight events is plenty" by arguing the cost of adding events is low and the cost of *missing* an event you later need is high. Counter: autocapture produces the dashboard-without-thresholds trap for first-time operators; the discipline of naming the eight events that matter is the education.

- **Aaron Cannon (Outset) on the Position A/B framing.** Cannon would argue NN/g's 2024 findings reflect early-2024 capability, that the platforms have iterated significantly since, and that treating the critique as present-tense is already outdated by 2026.[^10][^11][^16]

## Further reading

**Must-read**

- Ron Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments* (Cambridge, 2020). Still the canonical text. Chapters on sample size, pre-registration, and pitfalls are load-bearing.[^21]
- PostHog, *Product analytics best practices* (docs, updated 2025). The compact-taxonomy rule lives here.[^1]
- Rob Fitzpatrick, *The Mom Test* (2013, ebook 2024 reissue). Short, operational, unavoidable for interview discipline.[^18]

**Recommended**

- NN/g, *AI-Moderated Interviews: If, When, and How to Use Them* (Nielsen Norman Group, 2024). The most rigorous third-party observational study of AI-moderation failure modes to date.[^16]
- Carl Pearson, *AI moderated interviews: methodological error amplified* (carljpearson.com, May 2025). The sharpest methodological critique.[^15]
- Loeb & Loeb, *Understanding Session Replay: Legal Risks and How to Mitigate Them* (July 2025). Practitioner-grade walk-through of wiretap theory in replay litigation.[^7]

**Optional**

- Wilson score interval explainer at corplingstats (May 2024) — for readers who want to see the continuity-correction variant of the math.[^20]
- Evan Miller's A/B sample size calculator for the moment you need to estimate what traffic you need.[^23]

## Citations

[^1]: PostHog, "Product analytics best practices." https://posthog.com/docs/product-analytics/best-practices — Claim: compact taxonomy, top 5–10 events, verb-object naming, avoid PII. Verified 2026-04-17.

[^2]: Amplitude, "A 5 Step Guide to Sustainable Analytics Instrumentation" and "Best Practices to Follow When Creating or Evolving Your Analytics Tracking." https://amplitude.com/blog/analytics-instrumentation and https://amplitude.com/blog/analytics-tracking-practices — Claim: tracking plan as living document, only capture what you need. Verified 2026-04-17.

[^3]: Mixpanel, "Events: Capture behaviors and actions." https://docs.mixpanel.com/docs/data-structure/events-and-properties — Claim: structured event-property schema, property-data-type discipline. Verified 2026-04-17.

[^4]: PostHog, "GDPR compliance" documentation. https://posthog.com/docs/privacy/gdpr-compliance — Claim: masking by default on session replay, PostHog Cloud EU with IP capture disabled by default, consent-mechanism requirement. Verified 2026-04-17.

[^5]: PostHog, "Introducing PostHog Cloud EU." https://posthog.com/blog/posthog-cloud-eu — Claim: free tier includes 1M events and 5,000 session replays/month, EU-hosted. Verified 2026-04-17.

[^6]: WilmerHale Privacy and Cybersecurity Law, "Year in Review: 2024 Web Tracking Litigation and Enforcement," 25 Feb 2025. https://www.wilmerhale.com/en/insights/blogs/wilmerhale-privacy-and-cybersecurity-law/20250225-year-in-review-2024-web-tracking-litigation-and-enforcement — Claim: 2024 saw "various class action cases" on web-tracking technology. Verified 2026-04-17.

[^7]: Loeb & Loeb, "Understanding Session Replay: Legal Risks and How to Mitigate Them," July 2025. https://www.loeb.com/en/insights/publications/2025/07/understanding-session-replay-legal-risks-and-how-to-mitigate-them — Claim: wiretap-theory liability for session replay capturing visitor communications. Verified 2026-04-17.

[^8]: Pandectes, "Microsoft Clarity and GDPR: What You Need to Know in 2025." https://pandectes.io/blog/microsoft-clarity-and-gdpr-what-you-need-to-know-in-2025/ — Claim: Microsoft Clarity requires explicit user consent before any tracking begins for EEA/UK/Swiss visitors under GDPR; operators must integrate a Consent Management Platform and the Clarity Consent API, which delays tracking until valid consent is obtained and allows users to withdraw consent at any time. Verified 2026-04-17.

[^9]: California Privacy Protection Agency, Enforcement Advisory (Sep 2024). https://cppa.ca.gov/announcements/2024/20240904.html and Global Privacy Enforcement Network review summary via Herbert Smith Freehills Kramer. https://www.hsfkramer.com/notes/data/2024-posts/Global-Privacy-Enforcement-Network-findings-around-dark-patterns — Claim: 76% of sites and apps reviewed use at least one possible dark pattern; CPPA dark-patterns-subvert-autonomy framing. Verified 2026-04-17.

[^10]: Outset.ai, "Outset Secures $30 Million Series B" press release via GlobeNewswire, 10 Dec 2025. https://www.globenewswire.com/news-release/2025/12/10/3203401/0/en/Outset-Secures-30-Million-Series-B-to-Launch-the-World-s-First-AI-Native-Customer-Experience-Management-Platform.html — Claim: $30M Series B (Radical Ventures lead, M12/Microsoft participating), 8x 2025 revenue growth, total funding $51M; customer list Microsoft/WeightWatchers/Away/Nestlé/HubSpot/Uber. Verified 2026-04-17.

[^11]: Outset.ai, "Nestle Uses AI to Accelerate Product Innovation." https://outset.ai/resources/stories/nestle-ai-research-accelerated-product-innovation — Claim: 100+ concepts tested, 7+ brands, 5+ countries, "10x" participant count vs traditional qual (benchmark 20–30 people); Widenmeyer statement on "more than twice as much depth." Verified 2026-04-17 via WebFetch.

[^12]: Listen Labs, Series B announcement via PRNewswire, 2025. https://www.prnewswire.com/news-releases/listen-labs-raises-69-million-series-b-to-bring-customer-voices-into-every-decision-302661000.html and founders' letter https://listenlabs.ai/founders-letter — Claim: $69M Series B, Ribbit-led, $500M+ valuation, customer list Microsoft/Sweetgreen/Perplexity/Robinhood/Canva/Chubbies. Verified 2026-04-17.

[^13]: Strella, Series A announcement via VentureBeat and PRNewswire, Oct 2025. https://venturebeat.com/technology/amazon-and-chobani-adopt-strellas-ai-interviews-for-customer-research-as and https://www.prnewswire.com/news-releases/strella-raises-14m-in-series-a-led-by-bessemer-venture-partners-to-re-design-customer-research-for-the-ai-era-302586024.html — Claim: $14M Series A Bessemer-led, October 2024 stealth exit; Amazon/Duolingo/Apollo GraphQL/Chobani customer list; Apollo GraphQL Santiago quote; Ritual 24% revenue growth case study. https://www.strella.io/blog/how-ritual-used-strellas-ai-moderated-interviews-to-optimize-pricing-and-drive-24-revenue-growth. Verified 2026-04-17.

[^14]: Maze, "Launches Interview Studies to Streamline Moderated User Research for Product Development," WebWire press release, June 2024. https://www.webwire.com/ViewPressRel.asp?aId=323224 and Maze Interview Studies product page https://maze.co/features/interview-studies/ — Claim: June 2024 launch of Interview Studies, recruitment + scheduling + conferencing + AI transcript/summary/highlights in a single workflow. Verified 2026-04-17.

[^15]: Carl J. Pearson, PhD, "AI moderated interviews: methodological error amplified." https://carljpearson.com/ai-moderated-interviews-methodological-error-amplified/ — Claim: AI-moderated interviews collapse exploratory sequential design; classifier prompts simultaneously define and count categories; counting categories before defining them. Published May 2025; verified 2026-04-17.

[^16]: Nielsen Norman Group, "AI-Moderated Interviews: If, When, and How to Use Them." https://www.nngroup.com/articles/ai-interviewers/ — Claim: AI interviewers do not give participants chance to weigh in; rapport-building absent; use to supplement not replace human moderation; not suited for semistructured in-depth discovery interviews. Published 2024; verified 2026-04-17.

[^17]: Teresa Torres, Product Talk. https://www.producttalk.org/ and https://www.userinterviews.com/blog/how-to-interview-customers-continuously-with-teresa-torres-of-product-talk — Claim: weekly interview cadence as core continuous-discovery rhythm. Verified 2026-04-17.

[^18]: Rob Fitzpatrick, *The Mom Test*. https://www.momtestbook.com — Claim: three rules (talk about their life, ask past specifics, avoid pitching); Simon & Schuster 2024 reissue. https://www.simonandschuster.com/books/The-Mom-Test/Rob-Fitzpatrick/9798893312577. Verified 2026-04-17.

[^19]: Wikipedia, "Binomial proportion confidence interval." https://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval — Claim: Wilson interval stable from n=10, handles small n and extreme proportions better than normal approximation. Verified 2026-04-17.

[^20]: corp.ling.stats, "Re-evaluating continuity correction for Wilson intervals," May 2024. https://corplingstats.wordpress.com/2024/05/19/re-evaluating-wilson-intervals/ — Claim: Wilson score produces stable result around n=10 with actual confidence ~0.95. Verified 2026-04-17.

[^21]: Ron Kohavi, Diane Tang, Ya Xu, *Trustworthy Online Controlled Experiments: A Practical Guide to A/B Testing* (Cambridge, 2020). https://www.cambridge.org/core/books/trustworthy-online-controlled-experiments/D97B26382EB0EB2DC2019A7A7B518F59 — Claim: sample-size discipline, pre-registration, pitfalls at small N. Verified 2026-04-17.

[^22]: neweconomies.co, "A/B Testing: The Science of Not Fooling Yourself," 2024. https://www.neweconomies.co/p/ab-testing-the-science-of-not-fooling — Claim: Kohavi 2024 example of 55%-lift paper at N=919 collapsing to 0.16%/0.29%/0.73% across three 1.9M-user replications. Verified 2026-04-17.

[^23]: Evan Miller, "Sample Size Calculator (Evan's Awesome A/B Tools)." https://www.evanmiller.org/ab-testing/sample-size.html — Claim: interactive sample-size calculator with MDE, baseline, power, significance parameters. Verified 2026-04-17.

[^24]: Julian Shapiro, "Startup Handbook: Landing Page Copywriting." https://www.julian.com/guide/startup/landing-pages and Demand Curve "above the fold" playbook https://www.demandcurve.com/playbooks/above-the-fold — Claim: copy-hierarchy framework and demand-test / smoke-test pattern for landing pages. Referenced for cross-week continuity with Monday's lesson. Verified 2026-04-17.
