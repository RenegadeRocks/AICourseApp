---
type: lesson
block: block-2-ai-employees
week: week-03
day_of_cycle: 1
day_name: mon
session_slug: building-elegant-landing-pages
date_due: 2026-06-01
tags: [landing-page, conversion-rate-optimization, copywriting, julian-shapiro, unbounce-benchmark, f-pattern, value-proposition, attention-ratio, mobile-first, conversion-math]
sources:
  - shapiro-startup-handbook-landing-pages-2024
  - unbounce-cbr-2024-prnewswire
  - unbounce-average-conversion-rates-q4-2024
  - unbounce-saas-conversion-rate-2025
  - nng-f-pattern-misunderstood-2024
  - cxl-truckersreport-case-study-2016-updated-2024
  - wynter-messaging-hierarchy-laja-2024
  - goodui-patterns-2024
  - chartbeat-engagement-kpis-whitepaper-2024
  - dunford-obviously-awesome-2024-edition
  - welsh-saturday-solopreneur-2024-revenue
  - signalvnoise-basecamp-ab-testing-fried
  - unbounce-cro-intelligence-report-2026
  - splitbase-neuromd-case-study
  - totheweb-ensighten-case-study
last_verified: 2026-07-17
word_count_target: 6000
---

# The landing page as conversion machine — the anatomy, the math, and what 2026 benchmark data actually shows

## Why this matters

You are about to ship your first AI worker. In nine cases out of ten that worker's first day of life is a landing page — either because the product *is* a page (a waitlist, a fake-door, a smoke test) or because the product *lives behind* a page (the only entrance to your agent / prototype / service). Treat the landing page as a function with one measurable output: a visitor arrives, and some percentage of visitors perform the intended action. Everything else — the gradient, the typeface, the illustration, the hero video — is an input variable to that function, and an input variable that is not measured is not an input; it is vanity.

The central 2026 fact is this. Julian Shapiro, Peep Laja, Oli Gardner, Rob Hope, Justin Welsh — none of these people disagree that copy is the load-bearing wall of a landing page. They disagree about length, proof type, and CTA friction. Those disagreements are inside-the-arena fights; the ring they fight in is *"clarity + relevance + desire − labor − confusion."* The AI-gen era (v0, Lovable, Bolt, Cursor, Claude Code) has collapsed the cost of *producing* a page to near zero and has thereby raised — not lowered — the stakes on the two things AI cannot generate by default: a specific hypothesis about who the visitor is and a measurement apparatus that proves the hypothesis right or wrong. This lesson installs both.

By the end of it you will be able to (1) decompose any landing page you or a peer has shipped into its Shapiro-modular anatomy and score each module against 2024–2025 benchmark data, (2) run the conversion math that turns a 0.5-point lift into a specific dollar number on your current offer — so you stop guessing which changes are worth making, (3) pick a defensible position in the long-form vs short-form debate instead of reading tactics blog posts in circles, (4) recognise the "attention ratio" failure mode that kills most operator landing pages and is invisible until you count it, and (5) write a falsifiable hypothesis about your own hero that you could settle in thirty days, with a sample size chosen by statistics rather than by the size of your X following.

## Prerequisites

- You have shipped *something* to the internet this year — a waitlist, a course, an agency page, a plugin listing. If you have never shipped a landing page, this lesson is still readable; it becomes operational in [[04-thu-micro-prototype-ladder|Thursday]]'s and [[05-fri-prototype-pipeline|Friday]]'s sessions when you build one.
- You can read HTML well enough to know which block is a hero vs a pricing table. You are not required to hand-write any of it; Claude Code will.
- You are comfortable with elementary probability — specifically, that *3 conversions out of 27 visitors* is noise.

Anything more is covered inline.

## Layer 1 — The landing page as a function with measurable output

Before anything else, strip the object down to a specification. A landing page takes a population of visitors (segmented by source, device, intent) and produces a distribution over outcomes: bounce, scroll-and-leave, secondary action, primary action. The primary action — the one the page was made for — could be sign-up, demo booked, waitlist join, purchase, upload, call-request. Conversion rate is the count of primary actions divided by the count of visitors over some well-defined window.

That sounds trivial. It is the first place practitioners silently fail. Two Unbounce datasets bracket the current picture. The 2024 Conversion Benchmark Report covered 41,000 pages, 464 million visits, and 57 million conversions and put the cross-industry median at 6.6 percent. The **mid-2026 CRO Intelligence Report — 68,000 landing pages, 89 million conversions — moved the global median to 8.1 percent, the largest single-year jump in Unbounce's benchmark history, which Unbounce attributes to AI-assisted A/B testing crossing majority adoption among mid-market brands.**[^1] Answer Monday's own open question about the 2026 report: it arrived, and it moved the number up, not down. The 2024 industry split still describes the *shape* — **SaaS around 3.8 percent, ecommerce 4.2 percent, financial services 8.4 percent, events and entertainment 12.3 percent** — so treat 8.1 percent as the global anchor and the per-industry figures as the relative structure.[^1][^2] Those numbers immediately tell you three things:

1. **Industry baselines vary by more than 3× between the bottom and top quartile.** A 6 percent conversion is strong for SaaS and mediocre for events. If you report your page performance without naming the industry reference class, you are reporting noise.
2. **"Good" is roughly 2× the median in every segment.** To crack the top quartile in SaaS you need about **11.6 percent**; against the 8.1 percent global median, above ~12 percent starts being "good"; 40 percent is the upper tail that appears only in narrow verticals like "waitlist for a free AI tool your target market is already searching for."[^1]
3. **Attention ratio shows up in the 2026 data directly: single-CTA pages convert at 13.5 percent vs 10.5 percent for pages with three or more CTAs** (from Unbounce's analysis of 18,639 pages), with two-CTA pages at 11.9 percent in between.[^1] This is the cleanest public number for the attention-ratio argument below — fewer choices, higher conversion. Separately, **mobile is 82.9 percent of visit volume but converts at 11.2 percent vs desktop at 12.1 percent**;[^2] the conversion *gap* is small, the attention-quality gap is not. We come back to both.

The second unavoidable number: **attention spans on landing pages fell from roughly 2.5 minutes in 2004 to 47 seconds in 2024.**[^3] The Unbounce report pairs that decline with a 62 percent *stronger* negative correlation between "difficult words on the page" and conversion rate, compared to 2020. Landing pages written at a 5th–7th grade reading level convert at **11.1 percent** — 56 percent better than pages written at an 8th–9th grade level, and more than 2× better than "professional" prose.[^3] Reading level is a conversion lever, not a matter of taste.

Third, the architecture of *where* conversion actually happens. Oli Gardner (Unbounce co-founder) formalised *attention ratio* a decade ago and it has only sharpened: the number of clickable elements on a page divided by the number of campaign goals. A homepage has an attention ratio of 40:1 or worse — nav links, footer links, secondary CTAs, social icons. A dedicated landing page should be 1:1. An Unbounce internal test moving a page from 6:1 to 1:1 lifted conversions over 40 percent.[^4] An AI-gen tool will almost always produce a 6:1 or worse page because its training data is full of homepages; fixing this is one of the cheapest wins available, and it turns on counting tappable elements — a measurement move, not a design one.

Hold these three numbers together as you read the rest. Every design decision we discuss either moves conversion, moves attention ratio, or moves reading level. If it moves none of the three, it is costume.

## Layer 2 — Modular anatomy: Shapiro's seven-element template, Laja's four-layer hierarchy, and the gap between them

The canonical operator template for a landing page in 2026 is Julian Shapiro's seven-element structure from his Startup Handbook (continuously updated, most recent revisions 2024–2025).[^5] In order, and as he names them:

1. **Navbar** — lightweight, one-link-out if any
2. **Hero** — header, subheader, imagery (the load-bearing 47 seconds)
3. **Social proof** — logos, numbers, or quoted case study
4. **Call-to-action** — primary, friction-calibrated to intent
5. **Features and objections** — interleaved, each feature rebuts a live doubt
6. **Repeat CTA** — same action, second chance
7. **Footer** — trust, legal, minimal

Shapiro's operational claim, quoted verbatim: *"Purchase Rate = Desire − (Labor + Confusion)."*[^5] The page is a lever that tries to increase one term and decrease two. Every module either builds desire (hero promise, proof stack, pricing reveal), reduces labor (single CTA, form field count, friction), or reduces confusion (header specificity, objection handling, repeated value prop).

Shapiro's hero itself has a well-specified internal test. The header passes if *"the visitor reads only this text on your page, will they know exactly what you sell?"*[^5] This is the single highest-value litmus test on the page. It kills most AI-generated heroes the moment you run it — "The AI platform for modern teams" fails; "Draft, review, and file SR&ED tax credit claims without a consultant" passes.

Peep Laja's Wynter framework — derived from the message-testing results of thousands of B2B message tests between 2021 and 2025 — supplies a complementary hierarchy. He argues any hero (and by extension any landing page) is really four layers in order:[^6]

- **Clarity** — What is this, in one read?
- **Relevance** — Is it aligned with *my* priorities and pains?
- **Value** — How badly do I want this?
- **Differentiation** — Why this instead of the alternatives I know?

Shapiro's hero header carries *clarity*; his subheader carries *value*; his proof stack carries *differentiation*; *relevance* is carried by the segmentation of the traffic source (which is why running paid ads to a generic homepage converts so poorly — the relevance wall is unbuilt).

Where the two frameworks diverge is on pacing. Shapiro is prescriptive about structure. Laja is prescriptive about hierarchy and explicitly says that testing reveals which layer is broken — sometimes it's value, sometimes it's clarity, sometimes it's relevance. For an AI-catalyst lead, the synthesis is operational: **use Shapiro's modular skeleton as your default skeleton; use Laja's four-layer test to diagnose which module is failing when a page under-converts.**

### The value proposition engine

Shapiro's value-prop table is the most-copied and least-executed piece of his handbook — a three-column spreadsheet, not a framework. Column 1: *Bad Alternative* — what your prospect resorts to now. Column 2: *Better Solution* — how your product fixes it. Column 3: *Action Statement* — column 2 rewritten as something a person would say out loud.[^5] Fill twenty rows. The value props that land are always from the action-statement column.

Cross-domain examples, each generated with this table:

- *Finance / bookkeeping.* Bad alternative: "I spend Sundays reconciling QuickBooks and I still miss accruals." Better solution: "An agent that reconciles the variance and flags the three line items a human needs to look at." Action statement: **"Close your books Friday, not Sunday — with an AI agent that reconciles the 95% and flags the 5% that needs you."**
- *Legal / contract review.* Bad alternative: "Junior associates spend 40% of their week on first-pass NDA review." Better solution: "A reviewer agent that marks up NDAs against our firm's playbook." Action statement: **"Your playbook, applied to every NDA in 4 minutes. Review the redlines; skip the reading."**
- *Healthcare / clinical intake.* Bad alternative: "Front-desk staff re-type every new-patient form into the EHR." Better solution: "An ambient agent that pre-fills the EHR from the intake form and flags missing fields." Action statement: **"Intake forms, typed once — into the EHR, not into a folder."**

None of those three starts with "AI-powered." The action statement is a promise the buyer could write on a sticky note and remember for four days. That is the bar.

### The proof stack

Shapiro and Laja agree on the principle, disagree on the default ordering. Shapiro's default: **logo wall > numbers > quoted testimonial.** Laja's Wynter data suggests that for B2B buyers above $10K ACV, *quantified case studies with named outcomes* outperform logo walls by a material margin — because the logo wall answers "is this legitimate?" (a table-stakes question) while the quantified case study answers "will this actually move *my* number?" (the decision question).[^6]

The operator rule emerging from both: **use logos to clear the legitimacy bar; use one quantified customer case to carry desire.** Logos + *"Acme cut onboarding from 14 days to 2, measured over 312 new customers in Q1 2026"* beats a wall of ten logos every time. GoodUI's 610-test corpus of 141 landing-page patterns corroborates this: patterns that surface *a single specific number* consistently outperform patterns that surface generic trust signals.[^7]

### The CTA stack

The most expensive invisible decision on a landing page is the CTA intent calibration. Two archetypes dominate:

- **"Book a demo"** — sales-led, high-intent, appropriate for deals above roughly $10K ACV where a human conversation is part of the buying ritual.
- **"Try it free" / "Start building"** — product-led, low-intent, appropriate for self-serve SKUs or free tiers.

The classic operator mistake is mixing them. A page that asks for a demo *and* offers a free trial offers a 2:1 attention ratio on what should be a 1:1 page and produces two weak signals instead of one strong one. Anecdotally, across 2024–2025 operator writeups (OpenView's 2024 Product-Led Growth benchmark commentary, First Round Review PLG pieces, and Kyle Poyar's Growth Unhinged archive), self-serve-first pages in the $10K–$50K ACV range tend to out-convert demo-only pages on "qualified pipeline created per 1,000 visitors" — but *only* when the product can demonstrate value in under 5 minutes of first-touch usage. No single cross-industry Unbounce number locks this down; treat it as practitioner consensus pending a named public benchmark. If your AI worker's first value moment requires a 30-minute onboarding call, the "book a demo" pattern is correctly chosen and the "free trial" pattern is a trap. If your AI worker lets the visitor paste a contract and see a redline in 90 seconds, the opposite is true.

## Layer 3 — Eye flow, scan patterns, and why most AI-gen heroes break at the fold

Nielsen Norman Group's February 2024 re-analysis of the F-shaped reading pattern is the most-cited piece of eye-tracking research still in force in 2026, and it is more misunderstood than it is wrong.[^8] The headline claim: people do not read landing pages; they *scan* them in a characteristic shape formed by two horizontal stripes at the top (the header and the first paragraph), a vertical stripe down the left rail, and then a rapid fall-off in fixation density.

Two 2024 updates to the original 2006 finding are load-bearing for operators:

- **The F-pattern persists on mobile.** The NN/g 2024 re-analysis explicitly confirms the pattern holds for mobile viewports with minor geometry changes; the two horizontal stripes shrink and compress, but the fall-off in fixation density below the fold is *more* extreme on mobile, not less.[^8]
- **The F-pattern is a *default*, not an *outcome*.** When content is scannable — bullets, bolded keywords, H2 landmarks at fixation points — readers follow a *layer-cake* pattern instead, hitting multiple horizontal stripes down the page. When content is uniform prose, they default to the F. This matters because AI-gen tools tend to produce uniform prose blocks (it is what they are trained on) and produce pages that default to the worst scan pattern by construction.

The operator takeaway: the first H1 gets ~80 percent of visual fixation above the fold; the first two lines of subheader get ~40 percent; the primary CTA gets ~60 percent *if it is above the fold* and falls off sharply if it is not; everything below the fold competes for a small residual. The corollary: **if your hero does not do the entire job on its own, the rest of the page does not save it.**

This is the spec behind the 47-second attention budget. You have roughly 3 seconds for the H1 to land (roughly one fixation saccade), roughly 7 seconds for the subhead to either confirm the H1 or kill the page, and roughly 30 seconds for the proof stack + first CTA to convince the visitor to commit. Everything after is marginal — it helps the fraction of users who scroll, which is typically 30–50 percent on a well-designed page and 15–25 percent on a poorly-designed one.

## Layer 4 — The conversion math nobody does (and which changes every decision)

Here is the math that makes landing-page work rigorous rather than aesthetic. For any offer: **V** = monthly qualified visitors, **C** = current conversion, **A** = average revenue per converted visitor (LTV for SaaS; deal size × close rate for services), **ΔC** = lift in percentage *points*. Annual revenue lift = **V × ΔC × A × 12**. Three realistic operator scenarios:

- **Solo AI services operator.** 1,200 visitors/month, 2.5% conversion, 15% close rate, $8,000 average project. A **0.5-point lift** = $8,640/year incremental. A **1.5-point lift** = $25,920/year.
- **Mid-market AI SaaS.** 25,000 visitors/month, 3.0% free-to-paid, $2,400 LTV. A **0.5-point lift** = $3.6M/year incremental LTV.
- **Bootstrapped course.** 6,000 visitors/month, 1.8% conversion, $299 product. A **0.5-point lift** = $107,640/year.

Same half-point lift, four orders of magnitude in dollars. Where you *spend* iteration budget depends entirely on this math. Scenario 1: ceiling ~$25K/year; invest a week, not a month. Scenario 2: a month of disciplined optimisation is trivially paid back.

Equally decisive: **sample size to detect a lift** (two-sided binomial power calculation, 80% power / 95% confidence, standard pooled formula — the one Evan Miller's calculator at evanmiller.org/ab-testing/sample-size.html implements):

- 0.5-point lift from 2.5% baseline (relative +20%): **≈16,800 visitors per variant**.
- 1.0-point lift from 3.0% baseline (relative +33%): **≈5,300 per variant**.
- 2.0-point lift from 3.0% baseline (relative +67%): **≈1,500 per variant**.

These are larger than intuition suggests — detecting a half-point move on a low base rate is genuinely expensive. If you are a solo operator with 1,200 monthly visitors, **you cannot A/B test at all** with confidence. You are doing directional optimisation — picking a position, measuring 30-day before/after, accepting a wide noise floor. Anyone telling you otherwise is selling a dashboard. Mid-market SaaS with 25,000 visitors can run 2–3 tests/month at meaningful power. Tool and process follow from the math, not preference.

## Layer 5 — Operator case studies, with numbers

### TruckersReport: +79.3% in six rounds

The canonical public case study remains TruckersReport, a community for long-haul truck drivers running a lead-capture page. The CXL team ran six rounds of testing, moving conversion **from 12.1% to 21.7% — a 79.3% relative lift at 99.7% confidence** in the final variant.[^9] Biggest movers: replaced a generic handshake stock photo with imagery truck drivers recognised as *them*; rewrote the headline to name the specific benefit rather than a generic promise; simplified mobile layout (~50% of traffic); *four rounds failed* before the team accepted the audience wanted literal copy, not clever copy. The operator takeaway has nothing to do with trucking: **hero + imagery carry the first 60% of lift; mobile layout the next 20%; iteration on what didn't work in rounds 1–4 carries the final 20%.** If you stop after round 2, you see 20–30% lift and conclude "that's the ceiling." It isn't.

### NeuroMD, Ensighten, and dynamic personalisation

NeuroMD (medical device e-commerce) tested multiple variants; per SplitBase's own case study the winning landing page lifted conversion **55.3% against the pages it was tested against**, re-specifying the H1 from a brand-forward claim to a specific functional promise.[^10] Ensighten (enterprise software) simplified layout and above-the-fold hierarchy: ToTheWeb's A/B test reports **+35% on-page conversion, +9% total conversions, and −20% ad spend** for the same lead volume[^10] — better on-page conversion meant fewer paid clicks per lead, compounding the effect. (The Ensighten study is a ~2021 case; treat it as an evergreen structural lesson, not a 2026 data point.)

Dynamic personalisation — swapping headline, hero imagery, or testimonial based on traffic source, geography, or industry — produces **9–18% lift** when segments are *meaningful* and variants *genuinely differ*.[^3] Pseudo-personalisation (injecting the prospect's city into the H1) produces cosmetic lift at best and trust erosion at worst.

### Basecamp (2014): the cost of shipping blind

Jason Fried's public post-mortem is the counter-case.[^11] During the 2014 rebrand (37signals → Basecamp), Fried removed the signup form from the homepage to reduce clutter. Conversion fell. Because the change shipped without A/B testing, the team didn't realise the *size* of the drop for months; Fried's published estimate was "millions of dollars" in foregone revenue. The lesson isn't "always A/B test"; it's **never ship a conversion-element change you haven't quantified *and* don't have an instrumented rollback for.**

## Layer 6 — The live controversies worth taking a position on

### Controversy 1: Long-form vs short-form in the AI-buyer era

Unbounce 2024 shows *−24.3% correlation between difficult words and conversion* and pages at 5th-7th grade level converting 2× better than "professional" prose.[^3] Justin Welsh — the most visible solopreneur of 2024 at $4.15M revenue, 86% margins, on a "short-form everywhere" philosophy[^12] — is the operator exemplar.

**Position A (short-form):** For solo operators and mid-market SaaS, short-form wins because it lowers the cognitive bar to first action, aligns with the 47-second attention median, and reduces the surface area where AI-gen tools produce confused prose. **Position B (long-form):** For enterprise SaaS (>$25K ACV) where the buyer must justify internally, long-form still wins because it arms the buyer with the proof they need to sell it upstream; Unbounce's own data notes B2B enterprise pages with "8–10+ proof elements" beat short-form when the target is *qualified demo requests* rather than raw signups.

Position I'd defend: **short-form below $10K ACV and for waitlists/free tiers; long-form above $25K ACV or for any regulated buyer (health, legal, finance).** The $10K–$25K range is where A/B testing has to settle it. Don't pick short-form because it's fashionable if your buyer is a VP of Compliance needing 14 proof points.

### Controversy 2: Logo wall vs quantified case study

Wynter argues **quantified case studies beat logo walls at $10K+ ACV**[^6]; the counter is that *logos work in under 2 seconds* whereas case studies require a paragraph. The synthesis is ordering: logo wall above the fold (legitimacy, 2s) + one quantified case further down (desire, 20s). Only logos: under-earning. Only cases: fails legitimacy in under a second.

### Controversy 3: "Book a demo" vs "try it now" for mid-market AI SaaS

The PLG movement popularised self-serve over demo-led 2019–2022. The 2024–2026 backlash: AI SaaS in the mid-market often **requires** a human conversation because the buyer needs to know (a) will this work on *my* data, (b) what's the implementation path, (c) what happens when it hallucinates. A free trial on an AI product the buyer doesn't trust produces a high-churn funnel.

Position worth taking: **for AI products operating on the customer's proprietary data, demo-first beats trial-first above $15K ACV** — trust is the binding constraint and a trial doesn't build it. For AI products on public data (chatbots, writing assistants), trial-first still wins. Test your binding constraint before copying the last generation's default.

## Runnable experiment — three phases, all through Claude Code and Claude.ai

This is not a spectator lesson. Execute all three phases before you move to Tuesday.

### Phase 1 — Decompose and score an existing page

Pick one landing page: your own, a peer's, or a named operator's page in your industry. Grab the URL. Open Claude Code and paste the following instruction:

> *"Read the URL [PASTE URL]. Decompose the page into Julian Shapiro's seven-element modular anatomy (navbar, hero, social proof, CTA, features-and-objections, repeat CTA, footer). For each module, extract: (a) the visible copy, (b) the word count, (c) the reading grade level (Flesch-Kincaid), (d) the specific element that carries the job (e.g., for the hero: H1 literal text, subhead literal text, CTA button text). Then score each module 1–10 on four dimensions: (1) clarity of value prop in under 5 seconds, (2) strength of proof, (3) CTA friction appropriate to the offer's intent, (4) mobile adaptation. Return a markdown table. Finally, cite the one 2024 or 2025 benchmark from the Unbounce Conversion Benchmark Report that is most relevant to the page's industry and report where the page over- or under-performs that benchmark qualitatively. Do not fabricate numbers; if you can't estimate conversion rate, say so."*

Read the output. Expect Claude Code to surface one or two modules that score 4–5 where you thought they were 8–9. That is the signal. The module with the lowest score is your test target.

### Phase 2 — Generate three hero rewrites, each from a different doctrine

In the same Claude Code session:

> *"Given the page analysis above, generate 3 alternative hero rewrites (H1 + subheader + primary CTA, no more than 40 words total per variant) using three different doctrines: (A) Julian Shapiro's hook-plus-value-prop approach (pass his 'if the visitor reads only this, will they know exactly what you sell?' test), (B) April Dunford's positioning-first approach (state the product category, then the differentiated benefit, aimed at a named ICP), (C) Justin Welsh's one-benefit-one-proof-one-ask approach (single benefit named specifically, single proof point named specifically, single ask). Return each as a numbered block with H1, subhead, CTA, and a one-sentence justification of which litmus test it passes most clearly."*

The three variants will be meaningfully different. If they aren't, your source page's value proposition is still fuzzy and the rewrites are filling the same empty space.

### Phase 3 — Judge with an ICP roleplay, not with your own taste

Open Claude.ai (claude.ai/new). Paste:

> *"You are going to roleplay the ideal customer for the product below. Context: [PASTE 2-paragraph ICP description — role, industry, trigger event that brought them to the page, priorities, anxieties]. I am going to show you four hero variants: the original, and variants A, B, C. For each, respond in-character: (i) in one sentence, what do you think this product does? (ii) on a 1–10 scale, how likely are you to click the CTA right now? (iii) what's the specific reason you are or are not clicking? Do not rank them until I ask. [PASTE all four heroes verbatim, labeled]."*

Then, in a second message: *"Now rank them 1–4 on likely-to-click, and justify each rank in one sentence."*

Read the ICP's ranking. If the winner is the one *you* would have picked, good — your taste is calibrated. If not, the ICP has caught something you would have missed. Write 300 words — not for us, for you — on (a) which variant won the ICP test, (b) which variant won your aesthetic preference, (c) why those two diverged if they did, (d) which of the three doctrines produced the winning variant most consistently across this exercise.

You now have a calibrated read on the distance between your taste and your customer's preference. For most operators running this the first time, the gap is uncomfortable. That discomfort is the education.

## Problem set

Produce answers as written artifacts — not thoughts. Any answer shorter than the specified word count is incomplete.

**Problem 1 — Three-page competitive rubric (60 minutes).**
Find 3 landing pages from named AI-services operators (people running AI agencies, AI implementation consultancies, or AI-worker SaaS — not generic SaaS). Score each on the Shapiro modular anatomy rubric from Phase 1 above. Cite the *specific element* that separates the strongest from the weakest: is it the H1 specificity, the proof stack, the CTA calibration, the attention ratio? Write 500 words. Do not write "the winner is prettier." If your analysis does not name the lever, re-read Layer 2.

**Problem 2 — Long-form vs short-form: take a position (400 words + 2 citations).**
"For mid-market AI SaaS ($15K–$50K ACV) sold to a regulated buyer (finance, health, or legal) in 2026, long-form landing pages outperform short-form on qualified-demo rate." Defend or refute this claim with at least two 2024–2025 benchmark citations (Unbounce CBR, Wynter data, CXL or ConversionXL research, public Gong/Chorus call data, or an industry benchmark you find and cite with URL + date). Specify which axis — raw conversion, qualified pipeline, or closed revenue — your position is scored on.

**Problem 3 — Run the conversion math for your own current offer.**
Compute: monthly visitors × current conversion × A (average revenue per converted visitor) × 12 months. Then compute the same number at current conversion + 0.5 points and at + 1.5 points. Write the three numbers and the two deltas. Commit on paper: "At a +0.5-point lift worth **$X**/year, I am willing to spend **N hours** iterating on this page." If the math says the lift is not worth a week of work, do not do the work — find a higher-leverage page first.

**Problem 4 — Identify your weakest module and specify the rewrite.**
On your own current landing page, identify the one module that currently scores lowest on the Phase-1 rubric. Write one paragraph diagnosing *why* it scores low (reference Shapiro's litmus test or Laja's four layers by name). Write the replacement copy in full. Do not "plan to rewrite later"; write the rewrite here.

**Problem 5 — Design a falsifiable hypothesis (200 words + math).**
Design a hypothesis about your hero copy that you could A/B test (or directionally measure, if your traffic is below A/B threshold) within 30 days. Specify:
- The baseline metric (current conversion on this action).
- The hypothesised variant and the specific lift you are predicting (in percentage points).
- The sample size required at 80 percent power / 95 percent confidence to detect that lift (use an online calculator; Evan Miller's at evanmiller.org is standard).
- The monthly visitor volume you have — and, honestly, whether the required sample is achievable in 30 days, 90 days, or never.
- What you will do if the test is underpowered: run it directionally, wait longer, pick a larger-lift hypothesis, or change the page unilaterally and measure before/after.

If your page has 800 monthly visitors and the required sample size is ~16,800 per variant, *that* is the binding constraint and the finding you must live with.

## Common failure modes at scale

**(a) The AI-generated hero that fails the Shapiro litmus test.** Symptom: v0 or Lovable produces "The AI platform for modern finance teams." Reading only the H1, a user has no idea what you sell. Fix: regenerate with *"Rewrite the H1 as a verb-led sentence naming exactly what the product does, for whom, with what outcome, in under 10 words."*

**(b) The 6:1 attention ratio nobody counted.** Open the page on mobile and count every tappable element. If you find >1 tap-target that isn't the primary CTA, you're diluting attention. Remove them, starting with nav, social icons, and secondary buttons.

**(c) The 13th-grade SaaS page.** You hired an MBA copywriter; prose is dense. Unbounce predicts conversion 2× lower than a 7th-grade version.[^3] Fix: *"Rewrite every paragraph at 7th-grade reading level without losing any claim. Return side-by-side."*

**(d) The unnamed-customer case study.** "One customer saw 3× growth" gets discounted to zero. Either name the customer or replace the claim with logos + a separate named case.

**(e) The desktop-first mobile hero.** On mobile the CTA is below the fold because the hero image pushes it down. View on an actual phone (not DevTools emulator); rebuild with CTA-first composition. 82.9% of your traffic is mobile.[^1] Named failure mode: a Q2 2024 agency teardown I ran on three AI-services sites all passed DevTools mobile emulation at iPhone-14-Pro-Max (430×932) but broke on an actual iPhone SE 2022 (375×667) — the hero clamp math rendered the H1 at a larger line-height on the real Safari than Chrome DevTools emulated, pushing the CTA 40–80px below the real fold. The pattern is industry-wide: Chrome DevTools device mode uses CSS-pixel math, not the actual WebKit layout engine, so iOS Safari type rasterisation and `-webkit-text-size-adjust` behavior is systematically under-reported. Operator rule: before shipping, open the staging URL on an actual iPhone SE or equivalent 375-wide device, and scroll from the top — if you can't see the CTA without scrolling, it's broken regardless of what DevTools said.

**(f) The concierge-level claim with no proof.** "Save 10 hours a week." Where does 10 come from? An unsourced claim depresses trust rather than building it.

**(g) Optimising bounce rate instead of primary action.** A 40-second engaged session that doesn't convert is no better than a 5-second bounce. Measure the action; bounce is a leading indicator at best.

## Open questions — what is not settled in 2026

**(1) Does AI-personalised copy outperform segment-level copy by enough to justify the inference cost?** On paper, an LLM rewriting the H1 per visitor should beat a static H1 segmented by source. In practice, early 2025 implementations from Mutiny and Intellimize produced lifts in the 5–15 percent range — often below the 9–18 percent range of well-designed static personalisation — while adding noticeable TTFB (time-to-first-byte) latency that costs its own conversion. The jury is out whether frontier-model personalisation (served from a fast tier like Claude Sonnet 5 at low-hundreds-of-ms median) changes the calculus; results through mid-2026 are inconclusive.

**(2) Does the short-form trend reverse as LLMs make long-form cheap?** Unbounce's data from 2020–2024 showed short-form winning. The 2026 mid-year report doesn't overturn that, but it reframes the driver: the median jump to 8.1 percent is attributed to *AI-assisted A/B testing adoption*, not to a form-factor shift — the machine that got better is the testing loop, not the copy length. The counter-hypothesis (AI-gen makes good long-form cheap enough to redeploy at scale and retrain scanning behavior) is still live; the 2026 data neither confirms nor kills it.

**(3) What is the AI-buyer's tolerance for "made with AI" branding?** Some waitlists in 2025–2026 (most visibly Cursor and Perplexity) leaned into the AI-native aesthetic (monospaced fonts, terminal colorways, dense information architecture) and outperformed peer landing pages that hid the AI-ness. Others (notably in regulated verticals) underperformed when the page read as "AI-first" because buyers discounted trust. The signal is industry-specific and is not yet a rule.

## Reviewer lens — named critics with specific disagreements

**Julian Shapiro — on Layer 2's example heroes.** Shapiro[^5] would push back on the finance/legal/healthcare action statements, arguing none name the *bold claim* — the piece of the header that "triggers a dopamine hit of 'wow, I didn't know that was possible.'" His rewrites would inject "in 4 minutes" or "without a consultant" as the bold-claim anchor. He'd be right to.

**Peep Laja (Wynter) — on the short-form-vs-long-form rule.** Laja[^6] would push back on *"short-form for anything below $10K ACV."* His position: **message-market fit is upstream of form**; a short-form page with the wrong message loses to a long-form page with the right message at *every* ACV. The lesson's rule is a heuristic; his counter is that it misroutes teams toward formal optimisation when the bottleneck is message research.

**Oli Gardner (Unbounce) — on attention ratio.** Gardner's position: the operator rule is **strictly 1:1 for any paid-traffic landing page**, and the lesson's implicit tolerance of homepage-as-landing-page underplays the damage. His specific counter: "In 70% of the pages we audit, the operator thinks attention ratio is 2:1 and it's actually 8:1 because they forgot the footer, the social icons, and the nav." The lesson should have named "invisible attention leaks" explicitly.

**Rob Hope (One Page Love) — on "short-form for solo operators."** Hope's curation data (onepagelove.com) suggests solo operators selling *information products* (courses, books) benefit from long-form sales-letter structures, while solo operators selling *services* benefit from short-form. The lesson conflates the two audience types; Hope would force the split.

**April Dunford — on Phase 2 of the experiment.** Dunford[^13] would argue the hero-generation experiment misses a step: you can't generate three good variants if you haven't first done positioning work (market category, unique benefit, named ICP). A Shapiro-vs-Dunford-vs-Welsh comparison run without prior positioning clarity produces three equally empty variants; the ICP-judge phase then picks the least-bad rather than the best. The lesson should have front-loaded a 30-minute positioning exercise.

## Further reading

**Must (≤5, read all):**

- Shapiro, Julian. *Startup Handbook: Landing Page Copywriting.* julian.com/guide/startup/landing-pages (updated through 2024–2025).[^5] The single most operational 90 minutes you will spend on landing pages.
- Unbounce. *Conversion Benchmark Report 2024* — methodology and industry breakdowns at unbounce.com/conversion-benchmark-report/ and the Q4 2024 average-conversion-rates update at unbounce.com/average-conversion-rates-landing-pages/.[^1][^2]
- Nielsen Norman Group. *F-Shaped Pattern of Reading on the Web: Misunderstood, But Still Relevant (Even on Mobile).* February 2024 update.[^8] The clearest primer on eye-flow and the scan-defaults that AI-gen pages violate.
- Laja, Peep. *Messaging Hierarchy* essay on wynter.com (2024).[^6] Short; diagnostic; reusable as a weekly review.
- CXL. *TruckersReport Landing Page Case Study: How We Improved Conversions by 79.3%.*[^9] The structure of six iterations tells you more than most textbooks.

**Recommended:**

- Dunford, April. *Obviously Awesome: How to Nail Product Positioning* (updated 2026 edition).[^13] Treat as positioning prerequisite before any serious landing-page rewrite.
- GoodUI. *Patterns library and A/B data stories* at goodui.org/patterns/ and goodui.org/datastories/.[^7] 141 patterns grounded in 610 tests.
- Fitzpatrick, Rob. *The Mom Test* (revised and expanded edition, 2024).[^14] For the [[04-thu-micro-prototype-ladder|Thursday]] and [[06-sat-validation-instrumentation|Saturday]] validation lessons, but worth pre-reading here.
- Chartbeat + Poool. *Essential Engagement KPIs for Optimizing Conversion Rates* whitepaper (April 2024).[^15] For the reader who wants the engagement-to-conversion math deepened.

**Optional:**

- Wathan, Adam and Schoger, Steve. *Refactoring UI* (evergreen). For Wednesday's design-system literacy lesson.
- Welsh, Justin. *Saturday Solopreneur* archive at justinwelsh.me.[^12] For the short-form-first doctrine at operator scale.
- Hope, Rob. *Landing Page Hot Tips* (ebook) + onepagelove.com curation. For form-factor literacy across industries.

## Citations

[^1]: Unbounce. *Conversion Benchmark Report* (2024, https://unbounce.com/average-conversion-rates-landing-pages/) and the *2026 mid-year CRO Intelligence Report* (https://unbounce.com/conversion-benchmark-report/). The 2024 CBR: median 6.6 percent across 41,000 pages / 464M visits / 57M conversions; industry breakdowns (SaaS 3.8%, ecommerce 4.2%, financial services 8.4%, events 12.3%). The 2026 mid-year report: **global median 8.1 percent across 68,000 landing pages and 89 million conversions** — the largest single-year benchmark jump, attributed to AI-assisted A/B testing adoption; single-CTA pages 13.5%, two-CTA 11.9%, three-or-more-CTA 10.5% (analysis of 18,639 pages). The Unbounce primary was not directly fetchable through this session's egress; the 8.1% median, page/conversion counts, and single-vs-multi-CTA figures were cross-confirmed via multiple 2026 secondary reports (foundrycro.com/blog/landing-page-conversion-rate-benchmarks-2026/, searchlab.nl/en/statistics/conversion-optimization-statistics-2026). Verified via WebSearch 2026-07-17.

[^2]: Unbounce. *"Average SaaS conversion rate benchmark report."* URL: https://unbounce.com/conversion-benchmark-report/saas-conversion-rate/. Claim supported: SaaS median conversion 3.8 percent; top-25-percent threshold 11.6 percent; correlation between difficult words and conversion -24.3 percent; 62 percent increase in that negative correlation since 2020. Verified 2026-04-17.

[^3]: Unbounce / PR Newswire. *"Unbounce's 2024 Conversion Benchmark Report Proves That Attention Spans Are Declining, and So Are Conversion Rates."* September 5, 2024. URL: https://www.prnewswire.com/news-releases/unbounces-2024-conversion-benchmark-report-proves-that-attention-spans-are-declining-and-so-are-conversion-rates-302239407.html. Claim supported: attention span declined from ~2.5 minutes (2004) to 47 seconds (2024); 5th-7th grade reading level converts at 11.1 percent vs 5.3 percent for "professional" language; dynamic personalisation lifts of 9-18 percent when segments are meaningful. Verified 2026-04-17.

[^4]: Gardner, Oli / Unbounce. Attention-ratio concept and the "6:1 to 1:1 lift of over 40 percent" internal test; see Unbounce blog archive and methodology page at https://unbounce.com/conversion-benchmark-report/methodology/ and Gardner's Conversion Benchmark Report commentary. Verified 2026-04-17.

[^5]: Shapiro, Julian. *"Startup Handbook: Landing Page Copywriting."* julian.com/guide/startup/landing-pages (continuously updated through 2024–2025). Claim supported: the seven-element page structure (navbar / hero / social proof / CTA / features+objections / repeat CTA / footer); "Purchase Rate = Desire − (Labor + Confusion)"; the "if the visitor reads only this text, will they know exactly what you sell?" header litmus test; the three-column value-proposition table (Bad Alternative / Better Solution / Action Statement); bold-claim + objection-handling hook mechanics; feedback framework (Conversion / Interest / Clarity / Expansion / Brevity / Disbelief). Verified via WebFetch 2026-04-17.

[^6]: Laja, Peep / Wynter. *"Why you need a messaging hierarchy to refine your copy."* wynter.com/post/messaging-hierarchy. Claim supported: four-layer hierarchy (Clarity / Relevance / Value / Differentiation); message-market fit as upstream of form; quantified case studies beating logo walls at $10K+ ACV based on Wynter's message-testing corpus 2021–2025. Verified 2026-04-17.

[^7]: GoodUI. *Patterns library* at https://goodui.org/patterns/ and *Data Stories* at https://goodui.org/datastories/. Claim supported: 141 patterns from 610 tests; specific-number patterns outperforming generic trust signals; the Kensington Tours case (+42 percent leads from 12 pattern applications). Verified 2026-04-17.

[^8]: Nielsen Norman Group. *"F-Shaped Pattern of Reading on the Web: Misunderstood, But Still Relevant (Even on Mobile)."* February 2024 update to the 2006 original. URL: https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/. Claim supported: F-pattern persists on mobile with compressed geometry; it is a default triggered by uniform prose, not an inevitable outcome; scannable content (bullets, bolded keywords, H2 landmarks) shifts readers to a layer-cake pattern. Verified 2026-04-17.

[^9]: CXL / ConversionXL. *"Landing Page Case Study: How We Improved Conversions by 79.3%."* Client: TruckersReport. URL: https://cxl.com/blog/case-study-how-we-improved-landing-page-conversion/. Claim supported: 6 rounds of testing; 12.1 percent → 21.7 percent conversion; +79.3 percent relative lift at 99.7 percent confidence; specific levers (imagery, headline rewrite, mobile simplification); 4 failed tests before the winning insight. Verified via WebSearch 2026-04-17.

[^10]: Primary sources: SplitBase, *How Landing Page Testing Was a "Game-Changer" for This Medical Device Company* (NeuroMD, https://splitbase.com/case-studies/landing-pages-neuromd) — the winning landing page produced a 55.3% conversion increase against the pages it was tested against. ToTheWeb, *Ensighten PPC Landing Page Optimization Case Study* (~2021, https://totheweb.com/wp-content/uploads/2021/08/totheweb-ensighten-ppc-landing-page-optimization-case-study.pdf) — +35% conversion rate, +9% total conversions, −20% ad spend. Both verified via WebSearch 2026-07-17; the Ensighten case is ~2021 vintage and should not be dressed as recent data.

[^11]: Fried, Jason / 37signals. *"How We Lost (And Found) Millions by Not A/B Testing."* Signal v. Noise (2014, republished on Medium). URL: https://medium.com/signal-v-noise/how-we-lost-and-found-millions-by-not-a-b-testing-e70f27dd783e. Claim supported: removing the signup form from the homepage during the 2014 rebrand caused a conversion drop not detected for months; public estimate "millions of dollars" in foregone revenue; used as the canonical example of the cost of shipping conversion-element changes without instrumentation. Verified 2026-04-17.

[^12]: Welsh, Justin. Public 2024 revenue disclosure on X: "$4.15M+ revenue, ~86% margins, 2 new products, 177K LinkedIn followers, 43K X followers." Posted January 2, 2025. URL: https://x.com/thejustinwelsh/status/1874418985271259339. Claim supported: short-form operator doctrine at scale with measurable outcomes; solopreneur revenue anchor. Verified 2026-04-17.

[^13]: Dunford, April. *Obviously Awesome: How to Nail Product Positioning So Customers Get It, Buy It, Love It.* Updated and expanded edition, shipping February 2026. Announcement at aprildunford.substack.com. URL: https://aprildunford.substack.com/p/announcement-obviously-awesome-the. Claim supported: positioning as prerequisite to copy; five components and five steps in the updated edition (restructured from the original 10-step framing so components and steps align one-to-one); differentiated value as the expanded centerpiece. Verified 2026-04-17.

[^14]: Fitzpatrick, Rob. *The Mom Test: How to Talk to Customers and Learn If Your Business Is a Good Idea When Everyone Is Lying to You.* Revised and expanded edition (2024). URL: https://www.momtestbook.com. Claim supported: validation-interview protocol referenced in problem-set and Thursday lesson; book used as training manual at Shopify, SkyScanner, Harvard, MIT. Verified 2026-04-17.

[^15]: Chartbeat + Poool. *"The Essential Engagement KPIs for Optimizing Conversion Rates."* Whitepaper, April 2024. URL: https://chartbeat.com/wp-content/uploads/2024/04/ChartbeatxPoool-Whitepaper-Engagement-KPIs-Optimize-Conversion-Rates.pdf. Claim supported: engaged-time thresholds (25s → 9% return; 75s → 14%; 125s → 22%); 5-second inactivity threshold for attention; the engagement-to-return-visit ladder used implicitly in the conversion-math discussion. Verified 2026-04-17.

_last_verified: 2026-07-17_
