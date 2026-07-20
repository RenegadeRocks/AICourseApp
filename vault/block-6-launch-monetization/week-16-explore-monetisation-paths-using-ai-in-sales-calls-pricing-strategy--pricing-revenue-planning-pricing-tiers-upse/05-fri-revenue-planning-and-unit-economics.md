---
type: lesson
block: block-6-launch-monetization
week: week-16
session_slug: pricing-revenue-planning-pricing-tiers-upsell-hooks
day_of_cycle: 5
day_name: fri
tags: [unit-economics, cac, ltv, payback-period, gross-margin, churn, revenue-model, rule-of-40, saas-metrics, profitability]
sources:
  - digitalapplied-unit-economics-2026
  - foundrycro-ltv-cac-2026
  - foundrycro-cac-payback-2026
  - optifai-ltv-2026
  - ltvcacbook-cac-2026
  - proven-saas-cac-payback-2026
  - bessemer-ai-pricing-playbook-2026
  - saasmag-ai-cogs-2026
  - anthropic-pricing-docs-2026
  - refresh-2026-07-master-report
last_verified: 2026-07-17
word_count_target: 5000
---

# Revenue planning & unit economics — the model that tells you if this is a business

## Why this matters

Every decision this week (model, price, sales motion, tiers) converges into one question: **does a customer make you more money than they cost, fast enough, at your real margin?** That's unit economics, and it's the difference between a business and an expensive hobby. Today you build the model every founder needs: CAC, LTV, payback period, and gross margin computed under *actual AI COGS*, plus the compounding damage of churn and the one decision that dominates a subscription business, whether to raise price, cut cost, or improve retention when the numbers are tight. This is pass-bar-able: by the end you have a maintainable revenue model that shows a path to profitability at your real inference cost, or an honest diagnosis of why it doesn't yet. Saturday turns this into a calculator you'll reuse for the life of the product.

## Prerequisites

- [[01-mon-monetization-models-for-ai-products|Monday]] (your COGS-per-action) and [[02-tue-pricing-strategy-value-metric-anchoring-packaging|Tuesday]] (your prices). Today combines them into economics.
- [[04-thu-tiers-upsell-hooks-and-expansion-revenue|Thursday]]: NRR and expansion. LTV depends directly on retention and expansion, so Thursday's ladder feeds today's model.
- [[05-fri-data-and-scale|b5w14 Friday]]: churn and cohort measurement — where the retention *numbers* you'll plug in come from.

## The five numbers, defined without hand-waving

**1. Gross margin.** Revenue minus cost of goods sold, as a percentage. For an AI product, COGS = inference + hosting + any third-party API/data + the variable support cost per customer. This is the number the whole week has been protecting. Traditional SaaS: 80–90%. AI-native: 50–60% per Bessemer and SaaS Mag.[^1][^2] **Every downstream metric depends on this**, because you can only "afford" a customer out of your *gross* profit, not your revenue.

**2. CAC (Customer Acquisition Cost).** Total sales + marketing spend in a period, divided by new customers acquired in that period. Includes ad spend, tools, and the *fraction of your own time* spent selling valued at your rate (founders systematically ignore this and flatter their CAC).

**3. LTV (Lifetime Value).** The gross profit a customer generates over their lifetime. The honest formula for a subscription business:
`LTV = (ARPA × gross margin %) / churn rate`
where ARPA is average revenue per account per month and churn is monthly logo/revenue churn. Note the two things founders get wrong: **use gross margin, not revenue** (a customer paying $199 at 55% margin is worth $109 of profit, not $199), and **use revenue churn net of expansion**. Thursday's NRR matters here, because expansion *extends* LTV. With NRR > 100%, LTV is technically unbounded by the simple formula, so cap the horizon (e.g., 24–36 months) for a sane number.

**4. LTV:CAC ratio.** LTV divided by CAC. The canonical health target is **≥ 3:1**; 2026 median across segments is ~3.2:1, top quartile 4:1–6:1, by segment Enterprise ~4.5:1 / Mid-market ~3.2:1 / SMB ~2.5:1.[^3][^4] Below 3:1 you're spending too much to acquire relative to value; *far above* 5:1 often means you're *under*-investing in growth (leaving customers un-acquired). Only ~44% of SaaS companies actually hit the textbook 3:1.[^3]

**5. CAC payback period.** Months to recover CAC from a customer's *gross* profit: `CAC / (ARPA × gross margin %)`. The healthy benchmark is generally **≤ 12 months**, top quartile sub-12, worst quartile 24+.[^5][^6] 2026 sources scatter widely (median cited anywhere from ~8.6 to ~18 months depending on segment and how strictly CAC is measured) — treat these as **directional, not precise**, and note the AI-specific twist: because your gross margin is lower (55% not 85%), the *same* CAC takes proportionally longer to pay back. A CAC that paid back in 8 months at 85% margin takes ~12 months at 55%. **Lower AI margins stretch payback**, which is the quiet tax the COGS line puts on your whole growth model.

## The AI-COGS thread that runs through all five

Here's the compounding point most SaaS-metrics guides written before 2024 miss: **lower gross margin degrades LTV, LTV:CAC, and payback simultaneously.** Watch it cascade with the same customer:

- Customer pays ARPA $199/month, churns at 3%/month.
- **At 85% margin (old SaaS):** LTV = (199 × 0.85) / 0.03 = **$5,638**. If CAC = $600, LTV:CAC = 9.4:1, payback = 600 / (199 × 0.85) = **3.5 months**.
- **At 55% margin (AI reality):** LTV = (199 × 0.55) / 0.03 = **$3,648**. Same CAC $600 → LTV:CAC = 6.1:1, payback = 600 / (199 × 0.55) = **5.5 months**.

Same price, same churn, same CAC, but the AI-COGS reality knocks 35% off LTV and stretches payback 57%. This is *the* reason the whole week obsessed over margin under real token COGS. And it's why Monday's COGS-shock test matters for the *business model*, not just the price: if a forced model migration to Opus/Fable drops your margin from 55% to 35%, re-run this cascade and watch LTV:CAC fall below the 3:1 line — your unit economics can break from a *cost* event you didn't control, with no change to price or churn.

The optimistic mirror (Monday's point again): the 2026 cheap-tier curve is falling, so margin can *improve* without any pricing change. Sonnet 5 resetting the agent cost floor, cheaper competitor tiers, open-weight options.[^7] A model that's marginal today at 45% margin can become healthy at 60% if inference costs keep dropping. That's a real bet, but build for the downside and bank the upside.

## Churn: the compounding damage

Churn doesn't subtract; it compounds. A 5% monthly churn rate means you lose ~46% of a cohort in a year (0.95^12 ≈ 0.54 retained). At 3% monthly, you retain ~69%. At 2%, ~78%. The difference between 5% and 2% monthly churn is the difference between a business that leaks half its customers a year and one that keeps three-quarters — and because LTV has churn in the *denominator*, halving churn roughly *doubles* LTV. This is why [[05-fri-data-and-scale|b5w14]] retention and [[04-thu-tiers-upsell-hooks-and-expansion-revenue|Thursday's]] expansion are not separate from unit economics, they *are* the unit economics. The single highest-leverage number in the model is usually churn, because it sits in the denominator of LTV and compounds over time.

The SMB trap (Thursday's segment gap, now in dollars): SMB products churn harder (~97% NRR vs enterprise 118%), so an SMB AI product fights *both* lower margin *and* higher churn (the two forces that most degrade LTV), which is why SMB AI products must be either very cheap to acquire (low CAC, product-led) or very sticky (high retention). A high-CAC, high-churn, low-margin SMB product is three strikes; the model will show you which strike is fixable.

## The stage-appropriate metrics

You don't need every metric at every stage; tracking the wrong ones early is procrastination.

- **Pre-revenue / first customers:** forget LTV:CAC (you have no reliable churn or CAC yet). Track *gross margin per customer* (is each sale profitable?) and *raw cash* (runway). Seibel's stage.
- **Early revenue (10–50 customers):** now CAC and payback become meaningful; churn is still noisy (small N — [[06-sat-validation-instrumentation|b2w03]] discipline applies, don't over-read a 2-customer churn month). Track gross margin, CAC payback, and *early cohort retention shape*.
- **Scaling (50+ customers, some months of history):** LTV:CAC, NRR, and the **Rule of 40** (growth rate % + profit margin % ≥ 40, a directional health check that balances growth against efficiency) become real. Now the model can guide capital allocation.

Track the metric your stage can actually measure. A precise LTV:CAC computed from 8 customers is a fiction with decimal places.

## The one decision: raise price, cut cost, or improve retention?

When unit economics are tight — payback too long, LTV:CAC below 3:1. You have exactly three levers, and choosing the right one is the core skill of revenue planning. Work them in this order:

**1. Improve retention first (usually highest leverage).** Churn is in the LTV denominator and compounds, so a retention improvement often moves the model more than an equivalent price increase, *and* it's the healthiest signal (customers staying = value delivered). If churn is your worst number, fix it before anything else — [[05-fri-data-and-scale|b5w14]] retention mechanics and [[04-thu-tiers-upsell-hooks-and-expansion-revenue|Thursday's]] expansion.

**2. Raise price second (fastest, most direct).** A price increase flows straight to gross profit at ~100% margin (it costs almost nothing to charge more), so it's the most *efficient* lever, the Price Intelligently 1%→11% leverage from [[02-tue-pricing-strategy-value-metric-anchoring-packaging|Tuesday]]. The risk is churn/conversion drag, so test it (Tuesday's discipline) and apply it to new customers first (grandfather existing — [[05-fri-pricing-the-package|b4w09]]). If you've never raised price, you're almost certainly underpriced.

**3. Cut COGS third (real but bounded).** Cheaper model tier for deterministic-adjacent work, prompt caching (up to ~90% savings on cached input), batch processing (~50% off), retrieval instead of long-context stuffing (the 8–82× cost argument from the July refresh).[^7] COGS cuts improve margin and therefore every downstream metric, but they're bounded (you can't get below the model's floor) and can trade against quality. Do them, but know they're a margin lever, not a growth lever.

**Which first?** Diagnose: if churn is high → retention. If churn is fine but LTV:CAC is low and nobody flinches at your price → raise price. If margin is the constraint (a COGS shock, or you're at 40% margin) → cut COGS *and* raise price. The model tells you which number is worst; fix that one.

## Worked example — Niche Radar's unit economics

Inputs (from the week, and reproduced by Saturday's calculator): blended ARPA $179/month (mostly Pro), gross margin 58.1% (Monday's hybrid at Sonnet-5-intro rates, including a loaded support line), monthly revenue churn 4% net of expansion (Thursday's ladder pulled NRR toward positive but SMB churn is real), CAC $220 (mostly your time + light ads, product-led).

- **LTV** = (179 × 0.581) / 0.04 = **$2,602** (cap at 36 months: 179 × 0.581 × 36 = $3,743, so the churn-based number governs — fine).
- **LTV:CAC** = 2,602 / 220 = **11.8:1**. Suspiciously high → you're *under*-investing in acquisition (product-led, low CAC). The model says: you can afford to spend more to grow, or raise price.
- **CAC payback** = 220 / (179 × 0.581) = **2.1 months**. Excellent, fast payback, room to invest.
- **The stress:** Sonnet-5 intro expires Sept 1, margin drops to 52.8%. LTV → $2,362, payback → 2.3 months. Survivable. Forced Opus migration → margin 42.0%, LTV → $1,881, payback → 2.9 months, LTV:CAC → 8.6:1. Still healthy — the hybrid floor did its job.
- **The diagnosis:** this business is *under-monetized and under-marketed*, not broken. The lever is (2) raise price and (1) spend on acquisition. The 11.8:1 ratio is money left on the table. Contrast a hypothetical where CAC were $1,500 (paid ads for a $39 SMB product): LTV:CAC = 1.7:1, payback 14 months — three strikes, and the model would say "your acquisition model is wrong for this ACV; go product-led or raise ACV."

The point of the model isn't the numbers; it's the *diagnosis*. It tells you which of the three levers to pull.

## Runnable experiment — build and stress your revenue model

Allow 2 hours. Saturday's `code-lab/06-monetization-model/` mechanizes this; today build it by hand or in a sheet.

**Step 1 — The five numbers (40 min).** For your product, compute gross margin (real COGS from Monday), CAC (include your own time), ARPA (your tier mix), churn (from [[05-fri-data-and-scale|b5w14]] or an honest estimate), and derive LTV, LTV:CAC, and payback. Use real numbers where you have them; label estimates as estimates.

**Step 2. The COGS-shock cascade (30 min).** Re-run LTV, LTV:CAC, and payback at three margins: current, post-Sept-1 (intro expiry, ~−5pts), and forced-Opus-migration (~−16pts). Note which metric crosses a health threshold (LTV:CAC < 3:1, payback > 12mo) first, and at what margin.

**Step 3 — The churn sensitivity (20 min).** Re-run LTV at your current churn, half your churn, and double it. Observe that halving churn ~doubles LTV. This tells you retention's leverage relative to price.

**Step 4, The diagnosis (30 min).** Write the one-paragraph diagnosis: which lever (retention / price / COGS) moves your worst number most, what you'd do first, and what would have to be true for the business to be profitable at scale. Include the customer count at which you break even on fixed costs.

**Pass bar:** a model showing LTV:CAC and CAC payback with all inputs sourced or honestly labeled; the COGS-shock cascade computed at three margins with the first-to-break metric identified; and a written diagnosis naming the single highest-leverage lever and a path to profitability (or an honest statement of why there isn't one yet and what would have to change). The model must survive the Sept-1 intro-expiry shock with LTV:CAC ≥ 3:1 and payback ≤ 12 months, or carry a written plan for the gap.

## Common mistakes experts see

- **Using revenue instead of gross margin in LTV.** A $199 customer at 55% margin is worth $109 of profit, not $199. Every AI-product LTV must be margin-based, or it's inflated ~2×.
- **Ignoring your own time in CAC.** Founder-sold customers look free until you value your hours. Include them, or your CAC is fiction and your LTV:CAC is a fantasy.
- **Computing precise metrics from tiny N.** LTV:CAC to two decimals from 8 customers. Track stage-appropriate metrics; early on, gross margin per customer and cash, not a false-precision ratio.
- **Treating churn as a subtraction, not a compounding denominator.** Churn sits in the LTV denominator and compounds monthly; it's usually the highest-leverage number. Model it as compounding.
- **No COGS-shock test on the business model.** A margin event (forced model migration) can break LTV:CAC with no change to price or churn. If you only stress the price and not the unit economics, you'll be surprised in production.
- **Pulling the price lever when churn is the problem.** Raising price on a leaky bucket accelerates the leak. Diagnose first: fix the worst number, and it's often retention.
- **Chasing LTV:CAC ever-higher.** A 12:1 ratio isn't a trophy; it's a signal you're under-investing in growth. Very high ratios mean spend more (or price more), not celebrate.

## Reflection questions

- What's your real gross margin, including support and at your *worst* plausible model tier? If you don't know it to within 10 points, you don't know if you have a business — what's the fastest way to find out?
- Halving your churn roughly doubles your LTV. What's the single change to your product or onboarding most likely to halve churn, and why aren't you doing it this week?
- Your LTV:CAC is either below 3 (a problem) or above 6 (also a signal). Which is it, and does it tell you to fix acquisition, fix retention, or spend *more*?
- If a forced model migration cut your margin by 16 points tomorrow, would your unit economics still work? At what margin does LTV:CAC cross 3:1, and how far is that from where you are?
- When the numbers get tight, which lever will you reach for by instinct — and is that the one the model says has the most leverage, or just the one that feels safest?

## My take (reviewer lens)

**Michael Seibel** would attack the whole apparatus for an early reader: "LTV:CAC from 12 customers is astrology with a spreadsheet. You don't have a lifetime, you don't have a stable CAC, and you're going to make decisions off decimal places that are pure noise. At your stage there are two numbers: is each sale profitable (gross margin), and how many months of cash do you have. Everything else is a metric you'll earn the right to compute at 100 customers." He's right, and the lesson concedes it explicitly in the stage-appropriate section, the reason we teach the full model anyway is so the reader recognizes the moment their N gets big enough to trust it, and doesn't build the muscle from scratch in a crisis. **Chip Huyen** would flag that the benchmark ranges (CAC payback 8.6 to 18 months, LTV:CAC medians) are wide, source-dependent, and partly marketing content from vendors selling the very metrics they benchmark — so quoting them as targets invites false precision; the honest move (which the lesson makes) is to label them directional and lean on the *cascade math* (which is just arithmetic and always true) rather than the benchmark numbers (which drift). **Boris Cherny** would point at Saturday's calculator before it's built: the danger of any unit-economics model is that it hard-codes a margin and a rate card, then quietly lies for six months as prices move. So the tool has to read a *date-stamped* rate card and force the user to confront the shock scenarios, not present one comfortable number. That's exactly why the code-lab is structured around a rate card with dates and a stress matrix, not a single output. All three converge: the model's value is the *diagnosis and the arithmetic*, not the precision — it tells you which lever to pull, and it must never let you forget that your COGS moves.

## Further reading

**Must-read**
- Foundry CRO, *LTV:CAC Ratio Benchmarks 2026* and *CAC Payback Benchmarks 2026*, the ratios, by segment, with calculators.[^3][^5]
- [[05-fri-data-and-scale|b5w14 Friday]] — churn and cohort measurement, where the retention inputs come from.

**Recommended**
- Digital Applied, *SaaS Unit Economics 2026: CAC, LTV & Payback Reference*. The definitions and 2026 numbers in one place.[^8]
- Bessemer, *The AI Pricing and Monetization Playbook* — why AI margins reshape all of the above.[^1]

**Optional**
- Optifai, *B2B SaaS LTV Benchmarks, 939 Companies* — segment-level LTV distributions.[^4]
- SaaS Mag, *The AI COGS Problem*. The margin-compression mechanism in detail.[^2]

## Citations

[^1]: Bessemer Venture Partners, *The AI Pricing and Monetization Playbook* (2026): AI-native gross margins 50–60% vs 80–90% SaaS; COGS as a first-class metric for AI products. https://www.bvp.com/atlas/the-ai-pricing-and-monetization-playbook (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: SaaS Mag, *The AI COGS Problem: SaaS Gross Margin Compression 2026*: corroborates the 50–60% band and the mechanism by which inference COGS degrades margins. https://www.saasmag.com/ai-cogs-saas-gross-margin-compression/ (search-verified 2026-07-17; fetch egress-blocked, liveness pass pending)

[^3]: Foundry CRO, *LTV:CAC Ratio Benchmarks 2026*: median ~3.2:1, top quartile 4:1–6:1, only ~44% of SaaS hit 3:1; the "too high means under-investing" caution. Corroborated by SaaShero, *Best LTV to CAC Ratio Benchmarks for B2B SaaS in 2026*, https://www.saashero.net/strategy/b2b-saas-ltv-cac-benchmarks/ . https://foundrycro.com/blog/ltv-cac-ratio-benchmarks-2026/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Optifai, *B2B SaaS LTV Benchmarks. 939 Companies by Segment & LTV:CAC Ratio*: segment ratios (Enterprise ~4.5:1, Mid-market ~3.2:1, SMB ~2.5:1). https://optif.ai/learn/questions/b2b-saas-ltv-benchmark/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Foundry CRO, *CAC Payback Benchmarks 2026*: healthy ≤12 months, top quartile sub-12, worst quartile 24+; segment and method variance. https://foundrycro.com/blog/cac-payback-benchmarks-2026/ (search-verified 2026-07-17; fetch egress-blocked, liveness pass pending)

[^6]: Proven SaaS, *CAC Payback Benchmarks 2026*: corroborating payback ranges and the widening of median payback in recent years. https://proven-saas.com/benchmarks/cac-payback-benchmarks (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^7]: COGS levers and the falling cheap-tier curve (prompt caching ~90% on cached input, batch ~50%, retrieval-vs-long-context 8–82× cheaper; Sonnet 5 resetting the agent cost floor): Anthropic pricing docs and this vault's `_refresh-2026-07-master-report.md` / landscape delta §1 & §7, URL-cited therein. https://platform.claude.com/docs/en/about-claude/pricing (search-verified 2026-07-17; fetch egress-blocked. Liveness pass pending)

[^8]: Digital Applied, *SaaS Unit Economics 2026: CAC, LTV & Payback Reference*: consolidated definitions and 2026 benchmark values. https://www.digitalapplied.com/blog/saas-unit-economics-2026-cac-ltv-payback-reference (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
