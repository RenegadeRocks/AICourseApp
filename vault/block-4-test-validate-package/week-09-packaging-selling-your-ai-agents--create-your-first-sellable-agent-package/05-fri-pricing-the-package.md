---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 5
day_name: fri
session_slug: create-your-first-sellable-agent-package
date_due: 2026-07-17
tags: [pricing, value-metric, outcome-pricing, usage-based, credits, anchoring, labor-line, grandfathering, discounting, cogs, margin]
sources:
  - cheekypint-bret-taylor-2026
  - saastr-hubspot-resolution-2026
  - tropic-ai-credits
  - zenskar-token-pricing-cfo-2026
  - flexprice-usage-based-2026
  - revenera-prepaid-2026
  - gapvelocity-copilot-credits
  - bearlumen-ubp-trap
  - artisan-ava-2-launch-2026
  - intercom-fin-pricing-2026
  - digitalapplied-agency-survey-2026
  - anthropic-sonnet-5-pricing
  - getmonetizely-agentic-pricing-2026
last_verified: 2026-07-17
word_count_target: 4500
---

# Pricing the package — value metrics, the labor-line anchor, the $250 collapse, and surviving the usage-based backlash

## Why this matters

Price is the highest-leverage sentence in your package: it selects your customers, sets your support budget, and decides whether the Wednesday COGS math compounds into a business or a subsidy. And 2026 is a uniquely treacherous year to write that sentence. Entry anchors collapsed (Artisan's $250/month), outcome pricing went mainstream at the top (Sierra, Fin, Agentforce), the usage-based wave hit a measurable buyer backlash (78% of IT leaders reporting surprise charges), and your own COGS line moves twice this quarter (Sonnet 5's intro pricing expires August 31). Today you choose a value metric that fits your package's physics, anchor it against the labor line it replaces, structure it to survive model repricing in both directions, and stress-test the result numerically. Saturday's code-lab turns today's math into a calculator you will reuse for every package you ever ship.

## Prerequisites

- Wednesday's COGS numbers for your package (per-run token math, hosting slice, support estimate). Pricing without COGS is astrology.
- [[01-mon-what-a-sales-agent-is|Week 4 Monday]] — the canonical account of the Artisan Ava 2.0 price collapse and the "defend the floor above self-serve" doctrine. Today builds on it; it is not re-taught.
- [[05-fri-commercial-sow-for-ai-projects|Block 1 Friday]] — the canonical two-directional token-cost pass-through machinery. One-line recap: model prices now move up (Fable-class at 2× Opus) and down (Sonnet-class intro rates) mid-contract, and un-hedged flat pricing mis-serves someone either way.

## Layer 1 — Choosing the value metric: the physics test

Every price is a metric times a rate. The 2026 menu for agent packages, in ascending order of buyer-risk transfer:

1. **Flat tiers** (per month, by scope band) — the Tuesday ladder.
2. **Per seat** — legacy SaaS metric; increasingly wrong for agents, whose whole pitch is doing work without seats. Price per seat and you invite the buyer to notice the agent means *fewer* seats.
3. **Per unit of activity** (per run, per conversation, per 1K tokens, per "credit") — usage-based proper.
4. **Per unit of output** (per brief delivered, per qualified lead, per document processed).
5. **Per outcome** (per resolution, per booked meeting, per recovered invoice) — Sierra/Fin/Agentforce territory, where failure is free.[^1][^2]

Choose with a three-question physics test, applied to *your* package, not to the vendor you admire:

- **Can you measure it without dispute?** The metric must be computable by code both parties trust (Tuesday's resolution-definition drill). "Per insight" fails; "per daily brief delivered by 7am" passes; "per resolution" passes only with Fin-grade definitional work.[^2]
- **Does the buyer believe they control it?** Buyers revolt against metrics that feel like your throttle. Tokens and credits fail this test spectacularly — a credit is a proxy for variables the buyer can neither observe nor influence, and buyer-side literature now explicitly coaches procurement to distrust them.[^3]
- **Does it scale with value delivered, at your volume?** Outcome metrics need volume for the statistics to work (Tuesday's Layer 4). At 200 events/customer/month, per-outcome pricing is a business; at 22 briefs/month, it is a rounding error wearing a philosophy. Low-frequency, high-value packages price better as flat tiers with an outcome-shaped *guarantee* than as outcome-priced line items.

The honest default for a first productized-service package: **flat tiers on a scope metric (Layer 1 of value), plus a usage boundary (token/run budget) that protects your COGS, plus at most one outcome-flavored element** (a credit or free month triggered by missing the delivery SLO). This is also where the market's own center of gravity sits: the 2026 pricing literature converges on hybrid floor-plus-variable as the dominant surviving structure, precisely because it gives CFOs a forecastable floor and vendors a margin shield.[^4][^5]

## Layer 2 — Anchoring against the labor line

Your package's price has three possible reference frames, and you must choose the frame before the buyer chooses it for you:

- **Software frame**: "what does comparable SaaS cost?" → race to Artisan's $250.[^6]
- **Agency frame**: "what does an agency retainer cost?" → the $1,500–$4,500 productized band.
- **Labor frame**: "what does the human work cost that this replaces or augments?" → the only frame where agent economics shine honestly.

The labor frame is where the top of the market prices. Sierra's model works because every autonomous resolution displaces a $10–$20 human service interaction, and Sierra charges a slice of that spread.[^1] Your version, worked for the running "Niche Radar" example: a competent analyst spending 45 minutes each weekday assembling the same brief costs, at a loaded $60/hour, roughly $990/month. The Standard tier at $1,500/month is *more* than the labor line, which is fine: the package also buys coverage the analyst doesn't offer (no vacations, claim-level source links, the eval report), and that surplus is exactly what your differentiation section must argue. The sales-page arithmetic writes itself: state the labor line, state your price, and let the delta carry the "why us" burden. If your price is *below* the labor line, say so once, loudly, and resist the urge to price lower still: below a certain floor, B2B buyers read cheapness as risk, and [[01-mon-what-a-sales-agent-is|Week 4's]] post-collapse doctrine applies — the floor above self-serve is defended by named deltas (niche packs, eval reports, accountability), never by matching the self-serve price.

Two anchoring disciplines. **Anchor on the buyer's numbers, not yours**: during onboarding, capture the hours-per-week the package displaces, and reuse that number at renewal ("this quarter the Radar covered ~54 analyst-hours/month"). **Re-anchor at every scope change**: when a customer asks for source #13, quote the labor line of the addition, not just your incremental cost; scope creep priced at labor rates funds itself or stops.

## Layer 3 — The usage-based backlash, and building a CFO-safe structure

The 2026 evidence that pure usage pricing is in trouble is unusually consistent across buyer- and vendor-side sources: Tropic's procurement-side analysis reports 78% of IT leaders hitting unexpected charges under consumption/AI pricing and finds most finance leaders cannot define what a vendor's "credit" even measures;[^3] Zenskar's CFO-facing guide reports 90% of CIOs citing cost forecasting as their top AI-deployment challenge;[^7] developer-side anger at GitHub Copilot's 2026 move to usage-based AI Credits became its own genre of post;[^8] and vendor-side essays now openly describe the "usage-based pricing trap" and predict a partial swing back toward plans, prepaid commitments, and caps.[^5][^9] Even the pro-usage literature (Flexprice and peers) concedes the forecastability objection and prescribes floors and caps as table stakes.[^4]

Translate the backlash into four package-design rules:

1. **The buyer-facing metric must be legible.** Bill in briefs, conversations, sources, or resolutions — units the buyer can count on their fingers. Keep tokens and credits *internal* as your COGS meter (Wednesday's per-tenant budgets), never as the invoice line.
2. **Every variable component gets a cap and an alert.** "Usage above the tier's included volume pauses with a notification" beats "overage billed at…" for a first package: predictability is a feature you can afford to give because your COGS per unit is small; surprise is a churn event you cannot.
3. **Prepay beats surprise.** Annual or quarterly prepaid tiers with a modest discount move you cash-forward and move the buyer risk-forward, which both sides in the 2026 literature independently predict as the settling point.[^9]
4. **Publish the floor, negotiate the ceiling.** A public floor price (your Starter tier) does the Artisan-era work of signaling productization; ceilings (Enterprise) stay "talk to us" because isolated tenancy and exclusivity (Tuesday/Wednesday) genuinely vary.

## Layer 4 — The live controversy: is outcome pricing the future or a category error?

*Position A — outcomes are the endgame.* Bret Taylor's argument is the strongest version: the atomic unit of AI productivity is a *process*, not a person; selling seats made sense when software assisted humans, and selling outcomes is what selling completed processes looks like; align price with delivered value and the incentive conversation disappears.[^1] The 2026 receipts: Sierra's per-resolution model at $150M+ ARR, Fin's $0.99-per-resolution scaling to 30,000+ customers and a $3.6B acquisition, Salesforce shipping pay-per-resolution natively, and 56.8% of agencies reporting movement toward outcome-based engagements.[^1][^2][^10]

*Position B — outcome pricing is a special case masquerading as a law.* The skeptic's case, assembled from the pricing-operations literature and SaaStr's needling of HubSpot's per-resolution switch ("but does it really matter?"): outcome pricing only functions where the outcome is (a) high-frequency, (b) crisply definable, (c) mostly attributable to the vendor, and (d) cheap to adjudicate. Customer-support resolutions meet those four conditions almost uniquely well.[^11] Outside that pocket, "outcomes" degrade into negotiated definitions (whose "qualified lead"?), attribution fights (did the agent or the rep book the meeting?), and revenue volatility the vendor cannot hedge (Tuesday's guarantee arithmetic). Even inside the pocket, the buyer backlash logic applies in mirror image: a CFO cannot forecast a per-resolution bill any better than a per-token one, which is why every real outcome-priced vendor quietly sells committed-volume contracts around the headline metric.[^7][^11]

*The synthesis:* outcome pricing is a *conditional* technology. Run the four conditions against your package honestly. Support-agent shapes: often yes. Monitor-and-brief shapes, report generators, most Week-4-through-8 builds at your scale: usually no — take the flat-tier-plus-guarantee structure and revisit at 10× volume. What you must absorb from Position A either way is the *accounting posture*: track outcomes religiously even when you don't bill on them, because the renewal conversation ("54 analyst-hours covered, 96% delivery SLO, 3 incidents, all disclosed") is where outcome data pays regardless of the invoice format.

## Layer 5 — Grandfathering and the two-directional repricing problem

Your COGS will move at least twice in the next twelve months (Wednesday's deprecation ledger; the August 31 Sonnet-5 intro expiry is already calendared[^12]). Package pricing must metabolize this without renegotiating every customer. The machinery, building on [[05-fri-commercial-sow-for-ai-projects|Block 1's]] pass-through doctrine but adapted for *many* small customers instead of one large one:

- **Date-stamp the rate card.** Every tier sheet and every tenant config carries the model tier and its published rate as of a date (Wednesday's config schema does this structurally). This converts "prices went up" from an argument into a documented event.
- **Grandfather by window, not forever.** Standard practice that survives: existing customers keep their price for a defined window (6–12 months) after a public price change, then move to current pricing at renewal. Indefinite grandfathering feels generous and quietly builds a subsidized cohort whose COGS you eat at every model migration.
- **Absorb small, pass through large, in both directions.** Define a materiality band (±20% COGS movement is a workable default): inside the band you absorb (your margin exists to buffer noise); outside it, the contract's repricing clause activates — *symmetrically*, because 2026's curve moves down too, and a customer who watched Sonnet-class prices fall while your price held will do the arithmetic eventually. Passing savings through (or banking them visibly as "we upgraded your model tier at no charge") is a retention asset the spreadsheet never shows.
- **Never grandfather the metric.** Prices can hold; *definitions* cannot fork. If v2 of the package redefines the billable event or the tier boundaries, all tenants migrate to the new definitions even where their rate is grandfathered, or your billing code grows tenant-specific branches forever (Wednesday's fork disease, now in your invoices).

## Layer 6 — Discounting discipline, briefly and bluntly

Four rules cover a first package. (1) **Discount duration, never the metric**: two months free on annual prepay is recoverable; $1,100 instead of $1,500 "for you" reprices your product in one niche's group chat permanently. (2) **Design partners pay in evidence**: the early-customer discount (20–40%) is fine *when invoiced as a discount* against the real price and exchanged for named case-study rights, a logo, and a monthly feedback call with teeth. (3) **Every discount has an expiry event** written down: a date, a customer count ("first five"), or a milestone. (4) **The answer to "can you do better?" is a smaller package**, not a smaller price: drop to Starter, remove a source pack, shorten the support SLA. Price integrity is a compounding asset in a niche where buyers talk to each other, which, per your own segment-collapse decision Monday, they do.

## Layer 7 — The worked model: Niche Radar priced three ways

Numbers, so the experiment below has a template. COGS inputs from Wednesday: $0.62 inference per run at Sonnet 5 intro rates, 22 runs/month, ~$7/month fixed slice per tenant, support at 45 min/month loaded at $150/hour ($112.50). Fully loaded tenant COGS ≈ $133/month at Standard scope. Labor line: ~$990/month.

**Structure (a), flat three tiers ($750 / $1,500 / $3,500).** At 15 customers spread evenly: revenue $28,750/month, gross profit roughly $26,700, margins 83–96% by tier. Strengths: forecastable for both sides, trivially billable, the price sentence is speakable. Weakness: volume risk sits entirely with you; a customer running 3× the source volume inside a tier is margin leakage the caps must catch. This is why the tiers carry included-volume boundaries with pause-and-notify behavior rather than silent overages.

**Structure (b), hybrid floor plus usage.** $900/month platform floor (covers fixed COGS, support allocation, and the eval report) plus $30 per source per month beyond six, capped at the tier's ceiling with an alert at 80%. The same 12-source Standard customer pays $900 + $180 = $1,080; a 20-source near-Enterprise customer pays $1,320 before the Enterprise conversation triggers. Strengths: scales smoothly with the legible unit (sources, which the buyer chose and can count), and the floor is CFO-forecastable. Weakness: it re-opens a pricing conversation at every config change, and it prices *below* structure (a) for the median customer, which is a real cost of appearing fair. Choose (b) when your niche's customers vary widely in scope; choose (a) when the segment collapse worked and they don't.

**Structure (c), outcome-priced.** The billable event would be "actionable item surfaced that you acted on," at, say, $40 per acted-on item derived from the labor line. Run the physics test and watch it fail twice: measurement (who adjudicates "acted on"? the customer, with an incentive to under-report) and volume (a good month surfaces maybe 8–12 actionable items; one adjudication dispute swings 10% of revenue). The honest conversion of outcome thinking here is not the invoice but the guarantee and the renewal report: the delivery SLO credit (Tuesday) and the quarterly "hours covered, items acted on" artifact. Structure (c) is the right *accounting*, and the wrong *billing*, for this package. For a support-agent package the same test passes and (c) becomes viable; run the test, not the fashion.

**Decision for the running example: structure (a), with (b)'s alert mechanics inside the caps and (c)'s outcome data in the renewal artifact.** Stress outcomes from the Saturday calculator: baseline Standard margin 91.1%; intro-expiry 90.7%; flagship-migration 87.5%; price-war (−40% price) 85.2%; doubled-support 83.6%. Starter is the fragile tier (68.0% under doubled support), which is a design finding, not a footnote: Starter's fence (email-only support, six sources) is what makes its price honest, and the moment Starter customers routinely need calls, the correct move is raising Starter's price or tightening its scope, not absorbing quietly.

## Runnable experiment — price it three ways and stress-test the survivor

Allow 2 hours. Saturday's code-lab (`code-lab/06-agent-package/`) mechanizes this; today you can run it by hand or prototype in Claude Code.

**Step 1 — Three structures (40 min).** For your package, fully specify: (a) flat three-tier (Tuesday's ladder with today's Layer-3 caps and alerts); (b) hybrid (platform floor + legible usage component with included volume); (c) outcome-priced (billable event definition, rate derived from the labor line, committed-volume floor). For each: expected monthly revenue at 5 / 15 / 40 customers using honest volume assumptions.

**Step 2 — Stress matrix (40 min).** Run all three structures through four scenarios: (i) Sonnet-5 intro expiry (+50% inference COGS); (ii) forced migration to a flagship tier (+150% inference COGS); (iii) a price war (self-serve competitor at 1/5th your Standard price); (iv) an outcome-rate bad month (success rate −15%). For each cell: gross margin and required response (absorb / reprice / restructure). Claude Code prompt scaffold:

> *Build a small Python model: tiers, per-tier COGS (tokens/run, runs/month, rate card with dates, support hours at loaded rate), customer counts. Compute margin per tier per scenario. Print the matrix. Then argue: which structure degrades most gracefully, and which scenario kills each structure first?*

**Step 3 — Choose and defend (20 min).** Pick the structure you will actually ship. Write the five-sentence defense: metric and why it passes the physics test; the anchor frame and the labor line number; the cap/alert design; the grandfathering window and materiality band; the discount rules.

**Pass bar:** the chosen structure holds ≥70% gross margin (fully loaded, including support hours) in scenarios (i) and (iii), has a written response for (ii) and (iv) that does not involve emergency renegotiation, and the five-sentence defense contains four numbers and zero adjectives.

## Problem set

1. **Metric autopsies.** For each of Fin ($0.99/resolution), Artisan ($250/month + credits), and a Stammer-agency ($400/month/agent + usage markup): name the value metric, run the three-question physics test, and identify which question their pricing structure is engineered to survive.[^2][^6]
2. **The labor-line letter.** Write the four-sentence pricing paragraph for your package's sales page using the labor frame: the displaced work, its loaded cost, your price, the named surplus. No superlatives allowed; numbers only.
3. **Credit-scheme teardown.** Take any real credit-priced AI product you can find and answer Tropic's procurement questions against it: what does one credit measure, what moves the action-to-credit ratio, and could you forecast a quarter's bill within ±20%?[^3] Now confirm your own package would pass the same interrogation.
4. **Grandfathering ledger.** You have 12 customers: 5 at a legacy $1,200 rate, 7 at $1,500. The August 31 intro expiry lands (+50% inference COGS), and in October a competitor forces a Starter price *cut*. Write the ledger of who pays what through March, applying the window + materiality-band rules. Where does your margin trough, and is it survivable?
5. **The renewal artifact.** Draft the one-page quarterly value report (outcome data you track but don't bill on) for the running example. Which three numbers go in the first line, and which of them do you not yet instrument? That gap is homework for Saturday's build.

## Reflection questions

- Sierra prices on the customer-service spread because Bret Taylor could name the displaced dollar precisely. Can you name yours in one sentence? If not, is that a research gap or a sign your package's value is real but diffuse — and what pricing frame handles diffuse value honestly?
- The backlash data says buyers hate surprise more than they hate cost. Where in your current structure could a customer be surprised, and what would it cost you to make that impossible?
- If your model COGS fell 90% next year (plausible: watch the cheap-tier curve), would you cut prices, expand scope, or take margin? What does each choice signal to your niche, and which competitor does each choice invite?

## Common failure modes at scale

- **Pricing the tokens, not the job.** Cost-plus pricing off Wednesday's COGS ("it costs me $21, so $99 feels fair") ignores the $990 labor line and hands the surplus to the buyer unasked. COGS sets your floor; the labor line sets the neighborhood.
- **Metric mimicry.** Adopting per-resolution pricing because Sierra is impressive, at 20 events a month where one bad week is a 30% revenue swing. Run the volume condition before the philosophy.
- **The invisible overage cliff.** Shipping usage components without caps/alerts and discovering that your first churned customer is the one who got the surprise invoice. In 2026 this failure mode has its own survey literature; there is no excuse to re-derive it personally.[^3][^7]
- **Grandfathering by forgetfulness.** No date-stamped rate card, no window policy, and two years later a third of the book pays a price that predates two model migrations. The subsidy is real money; the awkward repricing email gets harder every quarter you delay it.
- **Discounting the metric under pressure.** One "$1,100 special" in a group-chat niche resets your real price to $1,100. Discount duration, scope, or onboarding — never the number that gets repeated.
- **Asymmetric pass-through.** A clause that passes cost *increases* through but stays silent on decreases. Buyers' counsel reads clauses too; the asymmetry costs trust worth more than the margin it protects — and [[05-fri-commercial-sow-for-ai-projects|Block 1]] already handed you the symmetric version.

## My take (reviewer lens)

**Michael Seibel** would cut through the taxonomy: "You have zero customers. Your pricing problem is not metric selection; it is that no one has said yes yet. Pick $1,500/month, say it out loud to ten real buyers, and let their faces price the product — every hour on the stress matrix before the first three yeses is procrastination." He is mostly right, and the defense is narrow: the stress matrix exists not to perfect the number but to stop you signing structures (uncapped usage, forever-grandfathering) that are expensive to *unwind* after the yeses arrive. **Hamel Husain** would attack Layer 4's synthesis from the measurement side: the lesson says "track outcomes even when you don't bill them," but tracked-not-billed metrics rot — nobody audits a number with no money on it — so either wire the outcome metric into a consequence (the SLO credit, the renewal report the customer actually receives) or admit it will decay into dashboard decoration. That critique is correct and is why the renewal artifact is a problem-set item, not a suggestion. **The cohort peer** would add the note the experts skip: the scariest moment is not choosing the metric, it is saying "fifteen hundred a month" to a human without flinching, and no spreadsheet builds that muscle — the Saturday demo script includes the pricing sentence *verbatim* for exactly this reason. All three agree on the underlying point: pricing is a live experiment run on real buyers, and today's structures exist to make that experiment cheap to run and safe to be wrong in.

## Further reading

**Must-read**

- Bret Taylor on outcome-based pricing (A Cheeky Pint / Sierra) — Position A, primary-sourced.[^1]
- Tropic, *What Is a Credit? Understanding AI Usage-Based Pricing* — the buyer-side interrogation your pricing must survive.[^3]
- [[01-mon-what-a-sales-agent-is|Week 4 Monday]], Layer 4 — the Artisan collapse and the defended floor, canonical.

**Recommended**

- SaaStr, *HubSpot Switching AI Pricing From Per Use to Per Resolution. But Does It Really Matter?* — the sharpest short Position-B text.[^11]
- Zenskar, *Token-Based Pricing for AI Products: The CFO's Guide 2026* — the forecastability problem from the finance seat.[^7]
- Monetizely, *The 2026 Guide to SaaS, AI, and Agentic Pricing Models* — the hybrid-structures survey behind Layer 1's default.[^4]

**Optional**

- Revenera, *Why Most AI Pricing Will (Eventually) Be Prepaid* — the prepaid-commitment prediction.[^9]
- GapVelocity on Copilot's AI-Credits billing change — a case study in metric-legibility failure at scale.[^8]
- Bear Lumen, *The Usage-Based Pricing Trap* — vendor-side repentance literature.[^5]

## Citations

[^1]: Bret Taylor, *AI agents, outcome-based pricing, and the OpenAI board*, A Cheeky Pint (mirrored at sierra.ai): per-resolution pricing with free escalation; "the atomic unit of AI productivity is a process, not a person"; the $10–$20 displaced-interaction spread. https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents ; https://sierra.ai/resources/podcasts/bret-taylor-of-sierra-on-ai-agents-outcome-based-pricing-and-the-openai-board (search-verified 2026-07-17)

[^2]: Intercom, Fin pricing / outcomes documentation ($0.99 per outcome; $49 base with 50 resolutions on the standalone deployment): the definitional work that makes outcome billing adjudicable. https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes ; corroborated by https://www.dragapp.com/blog/intercom-pricing/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Tropic, *What Is a Credit? Understanding AI Usage-Based Pricing*: 78% of IT leaders report unexpected charges under consumption/AI pricing; credits as opaque multi-variable proxies procurement cannot forecast. https://www.tropicapp.io/blog/what-is-a-credit-ai-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Monetizely, *The 2026 Guide to SaaS, AI, and Agentic Pricing Models* and Flexprice, *Why AI Companies Have Adopted Usage Based Pricing in 2026*: hybrid floor-plus-usage as the practically winning structure; floors/caps as table stakes. https://www.getmonetizely.com/blogs/the-2026-guide-to-saas-ai-and-agentic-pricing-models ; https://flexprice.io/blog/why-ai-companies-have-adopted-usage-based-pricing (search-verified 2026-07-17)

[^5]: Bear Lumen, *The Usage-Based Pricing Trap: Why AI Companies Are Moving Back to Plans*: vendor-side account of the swing back toward plans and caps. https://bearlumen.com/blog/usage-based-pricing-trap-ai-products (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Artisan, *Artisan launches Ava 2.0* (May 2026; $250/month entry, credit-based usage, $300 free credits): the entry-price anchor. https://www.artisan.co/blog/artisan-launches-ava-2-0-the-first-autonomous-ai-bdr-now-self-serve ; canonical treatment in this vault: Week 4 Monday (b2w04), verified 2026-07-17. (search-verified 2026-07-17)

[^7]: Zenskar, *Token-Based Pricing for AI Products: The CFO's Guide 2026*: 90% of CIOs cite cost forecasting as their top AI-deployment challenge; finance-side prescriptions for legible metrics. https://www.zenskar.com/blog/token-based-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: GapVelocity, *GitHub Copilot AI Credits Explained: The New Usage-based Billing…*: developer backlash to the June 2026 Copilot credits move as a metric-legibility case study; the Copilot usage-based shift is also recorded in this vault's July 2026 master refresh (cross-cutting theme #2, counts as one corroboration). https://www.gapvelocity.ai/blog/github-copilots-new-usage-based-billing-what-changed-why-developers-are-upset-and-what-it-means (search-verified 2026-07-17)

[^9]: Revenera, *Why Most AI Pricing Will (Eventually) Be Prepaid*: prepaid commitments as the predicted settling point between predictability and usage alignment. https://www.revenera.com/blog/software-monetization/why-most-ai-pricing-will-eventually-be-prepaid/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^10]: Digital Applied, 250-agency survey (56.8% of agencies selling or moving toward outcome-based engagements): also cited in this vault's July 2026 landscape delta (counts as one corroboration). https://www.digitalapplied.com/blog/agentic-ai-adoption-survey-2026-250-agencies

[^11]: SaaStr, *HubSpot Switching AI Pricing From Per Use to Per Resolution. But Does It Really Matter?*: the skeptical read on per-resolution's conditions; HubSpot Breeze's $0.50/resolution and $1.00/lead moves are canonically covered in Week 4 Monday (b2w04, verified 2026-07-17). https://www.saastr.com/hubspot-switching-ai-pricing-from-per-use-to-per-resolution-but-does-it-really-matter/ (search-verified 2026-07-17)

[^12]: Anthropic, *Pricing*, Claude Platform Docs: Sonnet 5 intro $2/$10 per M tokens through August 31, 2026, then $3/$15; cross-checked against this vault's July 2026 master refresh (binding theme #1). https://platform.claude.com/docs/en/about-claude/pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
