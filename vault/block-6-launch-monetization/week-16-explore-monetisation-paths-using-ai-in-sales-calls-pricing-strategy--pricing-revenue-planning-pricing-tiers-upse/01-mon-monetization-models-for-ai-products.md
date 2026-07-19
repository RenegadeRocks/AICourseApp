---
type: lesson
block: block-6-launch-monetization
week: week-16
session_slug: explore-monetisation-paths-using-ai-in-sales-calls-pricing-strategy
day_of_cycle: 1
day_name: mon
tags: [monetization, pricing-models, usage-based, subscription, outcome-pricing, freemium, cogs, token-economics, gross-margin, hybrid-pricing]
sources:
  - bessemer-ai-pricing-playbook-2026
  - flexprice-hybrid-pricing-2026
  - flexprice-usage-based-2026
  - lago-ai-pricing-models-2026
  - monetizely-agentic-pricing-2026
  - monetizely-outcome-pitfalls-2026
  - forbes-parloa-outcome-myth-2026
  - saasmag-ai-cogs-2026
  - freemius-ai-app-pricing-2026
  - firstpagesage-freemium-2026
  - anthropic-pricing-docs-2026
  - refresh-2026-07-master-report
last_verified: 2026-07-17
word_count_target: 5000
---

# Monetization models for AI products in 2026 — the menu, the margin, and the model that fits your physics

## Why this matters

By Friday you will commit to *how* your launched product makes money, and that commitment is expensive to reverse. Change your logo, your copy, even your feature set, and customers barely notice. Change your pricing model — subscription to usage, seat to outcome — and you re-paper every contract, retrain every buyer, and rebuild your billing code. The model is load-bearing structure, not a coat of paint. Today you learn the full 2026 menu, why the arrival of a real token-COGS line quietly kills some models that worked fine in the free-inference era, and how to pick the one whose physics matches your product. You leave with a chosen model and the margin math that proves it survives your actual inference bill.

## Prerequisites

- [[05-fri-pricing-the-package|b4w09 Friday — Pricing the package]]: value metrics, the labor-line anchor, the usage-based backlash, and the outcome-pricing controversy for a *services* package. Today is the *product-company* version. One-line recap: choose a metric that is measurable, feels buyer-controlled, and scales with delivered value — then defend a floor above self-serve. Not re-taught here.
- [[04-thu-pricing-ai-services|b0w03 Thursday]]: the first pass at AI-services pricing and the "when AI fits a problem" filter.
- Your product's real token cost per core action. If you do not have this number, stop and instrument it. Pricing without COGS is astrology, and in 2026 the COGS moves.

## First principles: a price is a metric times a rate, and AI broke the metric

For thirty years of software, the dominant value metric was the **seat**. It worked because software *assisted a human*, so counting humans counted value, and, critically, a marginal seat cost the vendor almost nothing. Gross margins sat at 80–90% and nobody running a SaaS business thought hard about cost of goods sold.[^1]

Agents break both halves of that. First, the pitch of an agent is that it does work *without* a human in the seat, so pricing per seat invites the buyer to notice that your product means *fewer* seats — you are taxing the thing you eliminate. Bessemer's 2026 framing is blunt: "per-user products are for humans; consumption products are for agents."[^1] Second, and more importantly for your survival, **the marginal unit now costs real money.** An agent run consumes thousands of model calls on your COGS line whether the customer has five logins or five hundred. Bessemer and SaaS Mag independently put AI-native gross margins at 50–60%, not 80–90%.[^1][^2] That 30-point compression is the single fact that reorganizes the entire monetization menu.

So the design question is no longer just "what metric captures value?" (the [[05-fri-pricing-the-package|b4w09]] physics test) but a second question stacked on top: **"does this metric let me pass through, or at least hedge, a COGS line that moves under me?"** A model that looked great in the demo can bleed you at scale if it decouples your revenue from your token bill in the wrong direction.

## The 2026 menu, in ascending order of buyer-risk transfer

Here is the full menu. For each: the mechanic, who it fits, and the part most guides skip, what the token-COGS line does to it.

### 1. Flat subscription (per month, by feature/scope band)

The classic. One price, defined scope, predictable for both sides. Buyers love the forecastability; CFOs can budget it.[^3] The danger in an AI product is **usage variance inside a flat price**: a customer who runs your agent 10× the median is 10× your COGS at the same revenue. Flat pricing silently cross-subsidizes heavy users from light ones, which is fine at 85% margin and lethal at 55%. Flat works when usage is naturally bounded (a weekly report, a fixed number of monitored items) or when you fence each tier with an included-volume cap.

### 2. Per seat

Legacy metric, increasingly wrong for agents (see above). Still viable for *collaboration-shaped* AI products where multiple humans genuinely use the tool (an AI-assisted design tool, a shared writing surface). Dead for autonomous-agent products. If your product's whole story is "it works while you sleep," per-seat is a category error.

### 3. Usage-based (per run, per message, per 1K tokens, per credit)

You bill for consumption. This aligns revenue with COGS beautifully, every expensive action bills the customer — which is exactly why AI companies rushed to it: roughly 92% of AI software companies now use *some* usage component.[^4][^5] But pure usage has a well-documented 2026 problem: buyers hate the unpredictability. Enterprise buyers reject pure usage citing cost unpredictability and attribution as their top objections;[^3] the [[05-fri-pricing-the-package|b4w09]] backlash data (78% of IT leaders hitting surprise charges; credits nobody can define) is the canonical evidence. Usage aligns *your* incentives and misaligns the *buyer's* sense of control.

### 4. Credits (a usage abstraction)

Credits are usage in a costume: you sell a bucket of "credits" that map to actions at a rate you control. GitHub Copilot's June-2026 move is the reference implementation — Pro at $10/month with $10 of included AI Credits, Business $19 with $19, Enterprise $39 with $39.[^6] Credits give you a legible-ish unit and a prepaid cash-forward structure, but they inherit usage's forecastability problem *and* add an opacity problem: buyers cannot easily map a credit to a dollar of value. Use credits as an internal COGS meter, expose them to buyers only when the action-to-credit ratio is stable enough to explain in one sentence.

### 5. Per-outcome (per resolution, per booked meeting, per document delivered)

The buyer pays only when the AI produces a defined result; failure is free. Sierra's per-resolution model, Intercom Fin's $0.99-per-resolution, Salesforce's pay-per-resolution. All live at $100M+ ARR scale.[^7] This is the maximum risk transfer *from* buyer *to* you: you now carry both the COGS *and* the delivery risk. It is magnetic in a sales conversation ("you only pay when it works") and treacherous in operations. We return to whether it fits you in the controversy section — the short version is that it is a conditional technology, not a law.

### 6. Hybrid (a floor plus a variable component)

A base subscription that covers your fixed COGS and gives the CFO a forecastable floor, plus a metered or credit component that scales with heavy usage and passes through your variable COGS. This is where the market's center of gravity actually sits. Hybrid adoption in B2B software went from 27% to 41% in a single year, with ICONIQ projecting 48% in 2026; Stripe found 21% higher median growth for hybrid vs pure subscription or pure usage.[^8][^5] For most AI products with real, variable inference cost, **hybrid is the honest default**, it gives buyers a predictable floor and gives you a margin shield. This is the product-company echo of [[05-fri-pricing-the-package|b4w09]]'s floor-plus-variable conclusion.

### 7. Usage-based-with-floor / committed-use

A hybrid variant worth naming separately because it is where enterprise deals settle: a committed minimum spend (the floor, which you can forecast and which de-risks your revenue) with usage billed above it, often at a discount for the commitment. Even pure-outcome vendors quietly sell committed-volume contracts around their headline metric, because a CFO cannot forecast a per-resolution bill any better than a per-token one.[^3]

## The margin math, done for real

Abstractions are cheap. Let us price the running example — **Niche Radar**, the competitive-intelligence product you carried through Block 4: it monitors a customer's chosen competitors and sources and delivers a daily brief. Here is its actual COGS on the July-2026 rate card.

**Per-brief inference.** One brief run ingests scraped source text and context (~45K input tokens) and writes a structured brief (~3K output tokens). On **Claude Sonnet 5 intro pricing ($2 / $10 per M tokens, in effect through 2026-08-31, then $3 / $15)**,[^9] and applying the ~+30% new-tokenizer factor from the July refresh (so effective tokens ≈ 58.5K in / 3.9K out):[^12]

- Input: 58,500 / 1e6 × $2.00 = **$0.117**
- Output: 3,900 / 1e6 × $10.00 = **$0.039**
- **Per brief ≈ $0.156.** At 22 briefs/month: **≈ $3.43 inference per active niche.**

Add embeddings/retrieval, scraping infra, and a hosting slice: call fully-loaded variable COGS **≈ $6–8 per active niche per month**. Now price it three ways:

- **Flat $49/month, 1 niche.** COGS ~$7 → gross margin ~86%. Healthy — *until* a power user monitors 8 niches inside a "flat" plan. COGS jumps to ~$56, margin collapses to −14%. The flat price only survives with a per-plan niche cap.
- **Usage: $9 per niche/month.** COGS ~$7/niche → margin ~22%. Aligned with COGS but thin, and the buyer with 8 niches sees a bill that swings monthly. Legible unit (niches, which they chose) but low margin unless you mark up harder.
- **Hybrid: $39 base (2 niches included) + $15 per extra niche.** A 5-niche customer pays $39 + $45 = $84; COGS ~$35 → margin ~58%. Forecastable floor, scales with the legible unit, margin holds. This is the structure the physics wants.

Now the part that separates 2026 from 2024: **run the COGS shock.** On **September 1**, Sonnet 5 intro pricing expires and inference rises 50% ($2/$10 → $3/$15). If you were forced onto **Opus 4.8 ($5/$25)**, inference is ~2.5× the Sonnet-5-intro baseline; onto **Fable 5 ($10/$50)**, ~5×.[^9] Under the flat $49/1-niche plan at Opus rates, the single-niche COGS climbs toward $17 and margin falls from 86% to ~65%. Survivable. Under the naive usage plan at Fable rates, margin goes *negative*. The lesson is not "avoid usage." It is that **your model must degrade gracefully as COGS moves**, and a floor is the cheapest insurance you can buy. (Saturday's calculator runs this matrix for your product automatically.)

The optimistic mirror image is real too: in 2026 the cheap-tier curve is falling fast — Sonnet 5 reset the agent-cost floor, GPT-5.6 Terra shipped at ~2× cheaper than GPT-5.5, Gemini 3.5 Flash sits at $1.50/$9, and Kimi K3 put an open-weight frontier model in play.[^12] If your model has a floor and you are honest with customers, falling inference cost drops straight to your margin or funds a visible "we upgraded your model tier at no charge" retention gift. Betting on cheaper inference is, in 2026, one of the least crazy bets available — but you build for the shock and *enjoy* the windfall, never the reverse.

## Controversy 1 — Is outcome-based pricing the future, or a special case wearing a crown?

This is the loudest pricing debate of 2026, so you must be able to argue both sides.

**Position A — outcomes are the endgame.** The strongest version (Bret Taylor's, canonically covered in [[05-fri-pricing-the-package|b4w09]]): the atomic unit of AI productivity is a completed *process*, not a person, so you should price the completed process. Align price with delivered value and the whole "are we getting our money's worth" conversation evaporates. The receipts are real — Sierra, Fin at $0.99/resolution across 30,000+ customers, Salesforce shipping it natively, and a majority of agencies moving toward outcome engagements.[^7]

**Position B. Outcome pricing is the most expensive myth in enterprise AI.** Parloa's Forbes piece and a chorus of 2026 pricing-ops writers make the skeptic's case, and it is sharper than the hype admits.[^10][^11] Outcome pricing only functions where the outcome is (a) high-frequency, (b) crisply definable, (c) mostly attributable to *you* and not the customer's team or other tools, and (d) cheap to adjudicate. Break any condition and you get: **attribution fights** ("did your AI close the deal or did my rep?"), **measurement disputes** ("your AI didn't save that, our process change did"), **perverse incentives** (an agent paid per resolution learns to close tickets fast at the cost of satisfaction), and **revenue volatility you cannot hedge**.[^11] Customer-support resolutions meet all four conditions almost uniquely well, which is precisely why every famous outcome-pricing example is a support agent.

**The synthesis you should hold:** outcome pricing is a *conditional technology*. Run the four conditions against your product honestly. Support-shaped products: often yes. Monitor-and-brief products like Niche Radar, most content and analysis tools, anything low-frequency or multi-attribution: usually no — take hybrid-with-a-guarantee and revisit at 10× volume. But absorb Position A's *accounting posture* regardless: **track your outcome metric even when you don't bill on it**, because the renewal conversation ("this quarter we surfaced 43 actionable competitive moves, you acted on 11") is where outcome data pays whether or not it is on the invoice.

## Controversy 2 — Freemium vs free trial vs paid-only, when free burns GPU money

For a bits-only SaaS, a free tier costs a rounding error. For an AI product, **every free user runs real inference on your COGS line** — free is a marketing expense with a variable cost you cannot fully predict. So the freemium-vs-trial question, evergreen in SaaS, has extra teeth in 2026.

The data, from a January-2026 study of ~200 products and corroborating benchmark sets:[^13][^14]

- **Free trial (no credit card):** median ~14% free-to-paid conversion. **Free trial (credit card required):** median ~44% — but far fewer people start.
- **Freemium (self-serve free tier forever):** median ~4.5% conversion.
- **AI-native products convert slightly higher** than traditional SaaS (good ~6–8%, great ~15–20%).
- The counterintuitive full-funnel finding: freemium's *lower* conversion rate is offset by a *much higher* signup rate. Per 1,000 visitors, freemium yields ~90 signups → ~5 paying; a no-card trial yields ~45 signups → ~3.6 paying. Freemium can win on total customers *and* still lose you money if the 85 non-converting free users each burn $6/month of inference.

The AI-specific decision rule: **your free tier's COGS per user must be a marketing number you can afford at your conversion rate.** If freemium free users cost $6/month and convert at 4.5%, you are paying ~$127 in inference to acquire one paying customer through the free tier alone (before any other CAC). If that is below your other acquisition channels and your LTV supports it (Friday's math), freemium is a channel. If not, use a **time-boxed trial** (bounds the COGS exposure), a **usage-capped free tier** (free but hard-limited to N actions/month. The most common AI-native answer), or **paid-only with a money-back guarantee** (zero free COGS, higher friction). Most AI products in 2026 land on usage-capped free or a short trial, precisely because unbounded freemium on a GPU bill is how you fund your competitors' evaluations.

## Choosing your model: the decision procedure

Run these in order for your product:

1. **Is the value delivered to a human-in-a-seat, or to a process running autonomously?** Seat-shaped → per-seat is still defensible. Process-shaped → seats are a category error; go usage/hybrid/outcome.
2. **Is your core outcome high-frequency, crisply definable, mostly attributable to you, and cheap to adjudicate?** All four yes → outcome pricing is on the table. Any no → hybrid-with-guarantee, keep outcome as an *accounting* metric.
3. **Does usage vary widely across customers?** Yes → you need a variable component (hybrid or usage-with-floor) or flat pricing will cross-subsidize you into the ground. No (naturally bounded usage) → flat tiers with caps are the simplest honest model.
4. **Can your buyer forecast their bill within ±20% at the start of a quarter?** If not, add a floor, add caps-with-alerts, or move variable components to prepaid. The 2026 backlash is entirely about surprise, not cost.[^3]
5. **Does the model degrade gracefully under a 2–5× COGS shock?** Run the shock (Saturday's calculator). If a plausible model migration takes any tier negative, you have a floor problem, not a pricing problem.

For most readers with a single launched AI product and variable inference cost, this procedure lands on **hybrid: a subscription floor that covers fixed COGS plus a legible metered component**, with outcome data tracked but not billed. That is not a failure of imagination; it is where the market's evidence points.[^5][^8]

## Worked example — Niche Radar's chosen model

Running the procedure: value is delivered to a process (autonomous monitoring), not a seat → not per-seat. The core outcome ("a competitive move you acted on") fails the frequency and attribution conditions → outcome pricing becomes an accounting metric, not a bill. Usage varies widely (customers monitor 1–15 niches) → we need a variable component. Buyers must forecast → floor plus caps. Under a 5× COGS shock the hybrid holds at ~58% while naive usage goes negative → hybrid it is.

**Decision:** hybrid — **$39 base (2 niches, daily briefs, 30-day source history) + $15 per additional niche, capped per tier with an 80%-usage alert.** Outcome metric tracked and surfaced in a monthly value email, never invoiced. Free experience: a **usage-capped free tier** (1 niche, weekly brief, 7-day history) that bounds free COGS to ~$2/user/month, chosen over unbounded freemium after the COGS-per-free-user arithmetic above. Thursday designs this into a full three-tier ladder with upsell hooks; today you have the *model* and proof it survives the shock.

## Common mistakes experts see

- **Pricing the tokens instead of the job.** Cost-plus off your COGS ("it costs me $7, so $19 is fair") hands the labor-line surplus to the buyer unasked. COGS sets your *floor*; the value delivered sets the neighborhood. ([[05-fri-pricing-the-package|b4w09]] labor-line anchor.)
- **Flat pricing with uncapped usage.** The single most common AI margin killer: one flat price, no included-volume cap, and your heaviest user is your biggest loss. Cap every tier; alert at 80%.
- **Metric mimicry.** Adopting per-resolution pricing because Sierra is impressive, on a product that produces 12 low-frequency, multi-attribution outcomes a month. Run the four conditions before the philosophy.
- **Unbounded freemium on a GPU bill.** A free tier with no usage cap, funding your competitors' evaluations at your inference expense. Cap it or time-box it.
- **Building a model that only works at today's price.** No COGS-shock test. When Sonnet-5 intro pricing expires on September 1 or a capability need forces you to Opus/Fable, you discover the negative-margin tier in production. Test the shock before you ship the price.
- **Exposing your internal COGS meter as the buyer's unit.** Billing in "tokens" or opaque "credits" the buyer cannot map to value. Bill in the legible unit they chose (niches, briefs, resolutions); keep tokens internal.

## Reflection questions

- Name the single displaced dollar your product replaces, in one sentence. If you cannot, is your value diffuse, and which model handles diffuse value honestly (hint: not outcome pricing)?
- If your inference cost fell 80% next year, would you cut price, expand scope, or take margin? What does each choice signal to your niche, and which competitor does each invite?
- Where in your current draft could a customer be *surprised* by a bill? What would it cost you to make that surprise impossible, and is that cost less than one churned customer?
- Your free tier costs $X/user/month in inference and converts at Y%. Multiply it out: what are you actually paying to acquire one customer through free, and is that your cheapest channel or your most expensive?
- Which of the four outcome-pricing conditions does your core outcome fail? Could a product change make it pass — and would that change be worth it just to unlock outcome billing?

## My take (reviewer lens)

**Michael Seibel** would compress this entire lesson to one imperative: "You have a launched product and, probably, single-digit paying customers. Your monetization problem is not model selection. It is that not enough people have said yes. Pick hybrid, ship a price, and let ten real buyers' faces tell you if it's wrong. Every hour on the COGS-shock matrix before you have pricing feedback is procrastination dressed as rigor." He is 80% right, and the defense is narrow: the shock matrix exists not to perfect the number but to stop you shipping structures — uncapped flat, unbounded freemium — that are cheap to *set* and expensive to *unwind* once customers arrive. **Hamel Husain** would go after the "track outcomes even when you don't bill them" line: a metric with no money on it rots, because nobody audits a number that has no consequence. He is right, which is why the outcome metric here is wired into a monthly value email the customer actually receives, a consequence — not a dashboard nobody opens. **Chip Huyen** would push on the margin math: the ~+30% tokenizer factor and the rate card are *today's* numbers, and both will move; the honest move is to build the calculator to read a date-stamped rate card (Saturday does exactly this) rather than hard-coding a margin you'll quote for six months after it's false. All three converge on the real point: your pricing model is a live experiment, and today's job is to choose a structure that makes that experiment cheap to run and safe to be wrong in.

## Further reading

**Must-read**
- Bessemer, *The AI Pricing and Monetization Playbook* (2026). The margin-compression thesis and the seat-vs-consumption reframe, primary-sourced.[^1]
- [[05-fri-pricing-the-package|b4w09 Friday]] — value metrics, the labor-line anchor, the usage-based backlash, canonical.

**Recommended**
- Flexprice, *Hybrid Pricing: The Complete Guide for SaaS and AI Companies (2026)* — the hybrid-dominance data and structures.[^8]
- Forbes / Parloa, *Outcome-Based Pricing: The Most Expensive Myth in Enterprise AI*, the sharpest Position-B text.[^10]
- Lago, *7 AI Pricing Models: What Works, What Breaks* — a clean taxonomy with failure modes.[^4]

**Optional**
- Monetizely, *The 2026 Guide to SaaS, AI, and Agentic Pricing Models* — the hybrid-structures survey.[^5]
- First Page Sage, *SaaS Freemium Conversion Rates: 2026*. Freemium benchmark detail.[^14]

## Citations

[^1]: Bessemer Venture Partners, *The AI Pricing and Monetization Playbook* (2026): 50–60% AI-native gross margins vs 80–90% SaaS; "per-user products are for humans, consumption products are for agents"; the 2026 renewal-cliff argument. https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook ; PDF https://www.bvp.com/assets/uploads/2026/02/The_AI_pricing_playbook_for_founders_Bessemer_Venture_Partners_2026.pdf (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: SaaS Mag, *The AI COGS Problem: SaaS Gross Margin Compression 2026*: independent corroboration of the 50–60% AI gross-margin band and COGS-driven pricing shift. https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/ (search-verified 2026-07-17; fetch egress-blocked, liveness pass pending)

[^3]: Tropic (buyer-side) and Zenskar (CFO-side) on usage-pricing forecastability: 78% of IT leaders report unexpected charges under consumption/AI pricing; enterprise buyers reject pure usage citing unpredictability and attribution. Canonically treated in [[05-fri-pricing-the-package|b4w09]]; https://www.tropicapp.io/blog/what-is-a-credit-ai-pricing ; https://www.zenskar.com/blog/token-based-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Lago, *7 AI Pricing Models: What Works, What Breaks* (2026): taxonomy of AI pricing models with failure modes; usage aligns COGS but transfers unpredictability to buyers. https://getlago.com/blog/ai-pricing-models (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Monetizely, *The 2026 Guide to SaaS, AI, and Agentic Pricing Models*: ~92% of AI software companies use some usage component; hybrid as the surviving structure. https://www.getmonetizely.com/blogs/the-2026-guide-to-saas-ai-and-agentic-pricing-models ; corroborated by Bessemer playbook[^1] (search-verified 2026-07-17; fetch egress-blocked. Liveness pass pending)

[^6]: GitHub Copilot AI Credits pricing (June 2026): Pro $10/mo + $10 credits, Business $19 + $19, Enterprise $39 + $39. Also recorded in this vault's July-2026 master refresh (cross-cutting theme #2, counts as one corroboration). https://flexprice.io/blog/hybrid-pricing-guide (search-verified 2026-07-17)

[^7]: Outcome-pricing receipts (Sierra per-resolution; Intercom Fin $0.99/resolution at 30,000+ customers; Salesforce pay-per-resolution; agency shift to outcomes): canonically sourced in [[05-fri-pricing-the-package|b4w09]] (Bret Taylor / A Cheeky Pint; Intercom docs; Digital Applied 250-agency survey). https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents ; https://www.digitalapplied.com/blog/agentic-ai-adoption-survey-2026-250-agencies (search-verified 2026-07-17)

[^8]: Flexprice, *Hybrid Pricing: The Complete Guide for SaaS and AI Companies (2026)*: hybrid adoption 27%→41% in a year, ICONIQ projecting 48% for 2026; Stripe's 21%-higher-median-growth finding for hybrid. https://flexprice.io/blog/hybrid-pricing-guide ; corroborated by https://flexprice.io/blog/why-ai-companies-have-adopted-usage-based-pricing (search-verified 2026-07-17)

[^9]: Anthropic, *Pricing*, Claude Platform Docs (per M tokens): Sonnet 5 intro $2/$10 through 2026-08-31 then $3/$15; Opus 4.8 $5/$25; Fable 5 $10/$50; Haiku 4.5 $1/$5. Cross-checked against this vault's July-2026 master refresh (binding theme #1). https://platform.claude.com/docs/en/about-claude/pricing ; corroborated by https://www.finout.io/blog/anthropic-api-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^10]: Forbes / Parloa BrandVoice, *Outcome-Based Pricing: The Most Expensive Myth in Enterprise AI* (Jan 2026): the four-condition skeptic's case; attribution and adjudication costs. https://www.forbes.com/sites/parloa/2026/01/06/outcome-based-pricing-the-most-expensive-myth-in-enterprise-ai/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^11]: Monetizely, *Why Outcome-Based AI Pricing Models Are Gaining Traction (And Their Hidden Pitfalls)*: attribution complexity, measurement disputes, perverse incentives, multi-variable systems billed as single-variable. https://www.getmonetizely.com/articles/why-outcome-based-ai-pricing-models-are-gaining-traction-and-their-hidden-pitfalls (search-verified 2026-07-17; fetch egress-blocked, liveness pass pending)

[^12]: Model lineup, tokenizer, and cheap-tier curve (Sonnet 5 reset the agent cost floor; GPT-5.6 Terra ~2× cheaper than GPT-5.5; Gemini 3.5 Flash $1.50/$9; Kimi K3 open-weight frontier; new Anthropic tokenizer ~+30% tokens): this vault's `_refresh-2026-07-master-report.md` (binding theme #1) and `_refresh-2026-07-landscape-delta.md` §1, both URL-cited therein. (search-verified 2026-07-17)

[^13]: ChartMogul, *The SaaS Conversion Report* and Growthspree, *B2B SaaS Trial-to-Paid Conversion Rate Benchmarks 2026*: no-card trial median ~14%, card-required ~44%; the freemium-vs-trial full-funnel comparison (per-1,000-visitor signup and paid yields). https://chartmogul.com/reports/saas-conversion-report/ ; https://www.growthspreeofficial.com/blogs/b2b-saas-trial-to-paid-conversion-rate-benchmarks-2026-by-trial-type-acv-length-credit-card (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^14]: First Page Sage, *SaaS Freemium Conversion Rates: 2026* and Freemius, *AI app pricing models*: freemium median ~4.5%; AI-native products convert slightly higher; free-tier COGS as a marketing expense. https://firstpagesage.com/seo-blog/saas-freemium-conversion-rates/ ; https://freemius.com/blog/ai-app-pricing-model/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
