---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 1
day_name: mon
session_slug: packaging-selling-your-ai-agents
date_due: 2026-07-13
tags: [productization, productized-services, agency-vs-product, scope-collapse, forward-deployed-engineer, vertical-ai, margin-economics, business-model, agent-packages]
sources:
  - harvey-11b-round-2026
  - sacra-harvey-2026
  - sierra-950m-series-e-2026
  - cheekypint-bret-taylor-2026
  - artisan-ava-2-launch-2026
  - taskip-agency-pricing-2026
  - digitalagencynetwork-ai-agency-pricing-2026
  - buildwithdew-productized-offers-2026
  - digitalapplied-agency-survey-2026
  - cnbc-aws-fde-2026
  - buildingagenticai-fde-2026
  - getperspective-fde-playbook-2026
  - techtarget-fde-2026
  - stammer-white-label-2026
last_verified: 2026-07-17
word_count_target: 4500
---

# From build to package — the productization spectrum, and where agent businesses actually sit in 2026

## Why this matters

You can build agents that work. That is now the table stakes, not the business. The business question this week answers is: *what do you sell, at what margin, to how many buyers, with how much of your own time in every delivery?* Get this wrong and you have built yourself a job with worse hours than the one AI was supposed to replace. Get it right and the build you finished in [[06-sat-build-the-hybrid-scraper-summarizer|Week 8]] becomes an asset that sells while you sleep, or at least while you build the next one. Today you learn the four-position spectrum every AI business sits on, the revenue evidence for where agent businesses actually cluster in mid-2026, the single move (scope collapse) that shifts a business rightward on the spectrum, and the live counter-argument: a multi-billion-dollar 2026 wave of *forward-deployed engineering* betting that agent deployments are snowflakes that resist packaging entirely. By Friday you will have priced a package; today you decide whether you have one.

## Prerequisites

- One working build from Weeks 4–8 that you could demo today: the [[01-mon-what-a-sales-agent-is|sales agent]], the [[06-sat-build-the-weekly-report-generator|report generator]], the voice squad, or the scraper-summarizer.
- The Block 1 selling machinery: [[05-fri-commercial-sow-for-ai-projects|SOWs, pass-through clauses, phase pricing]]. This lesson assumes it and does not re-teach it. Where Block 1 sold *your time shaped by a contract*, this week sells *an artifact shaped by a spec*.
- Honesty about your current revenue mechanics: for your last (or imagined next) client, how many hours of your labor does one delivery consume, and would delivery number five consume fewer?

## Layer 1 — The spectrum: four positions, four economic engines

Every AI business occupies a position on a spectrum with four canonical stops. The stops differ not by ambition but by *what the customer buys* and *what marginal delivery costs you*.

**Position 1 — Custom service.** The customer buys your judgment applied to their situation. Every engagement is scoped fresh ([[04-thu-project-planning-phases-and-risk|Block 1 Thursday's]] discovery-POC-pilot-production arc), priced fresh, and delivered fresh. Revenue scales linearly with your hours. Gross margins on paper look high (you are selling time you already own), but the *ceiling* is brutal: you cannot deliver engagement six while delivering engagement five. Everything in Block 1 lives here, deliberately: custom service is the fastest way to your first dollar and the best possible research program for what to productize. Its output is not just revenue; it is *pattern data* — which requests repeat, which deliverables get reused, which onboarding questions recur.

**Position 2 — Productized service.** The customer buys a named, fixed-scope, fixed-price outcome, delivered by you with a repeatable process. "The Niche Radar: a daily competitive brief for your market, in your Slack, $1,200/month, live in ten business days." Scope is closed. Price is public or semi-public. Delivery follows a runbook, not a proposal. Your hours per delivery fall with every customer because the process amortizes. The 2026 agency guides converge on a mid-market band for exactly this shape: roughly $1,500–$4,500/month per client for productized AI retainers, with B2B outbound packages at $1,500–$4,000/month and lighter local-business agents at $300–$1,500/month.[^6][^7] These are directional composites from agency-pricing surveys, not audited financials, but three independent guides land in the same band, which is what a market norm looks like from outside.

**Position 3 — Product.** The customer buys access to software; your marginal delivery cost approaches hosting plus support. Onboarding is self-serve or near-self-serve. The clean 2026 exhibit is Artisan's Ava 2.0: in May 2026 the AI-BDR vendor relaunched with self-serve onboarding in under ten minutes, $300 in free credits, no credit card required, and an entry price cut 10× from $2,500/month to $250/month.[^5] That price is only possible because delivery is fully productized: no human at Artisan touches a $250/month account. [[01-mon-what-a-sales-agent-is|Week 4 Monday]] is the canonical teardown of what that collapse did to the AI-SDR market; today's point is narrower: the $250 price *is* the productization, made visible as a number.

**Position 4 — Platform.** Other builders create value on your rails and you take a percentage. Salesforce's AgentExchange (Thursday's lesson) charges partners 15% of revenue for the privilege of distribution; a platform's customers are the sellers, not just the buyers.[^13] You will not build a platform this week. You should know the position exists because platforms set the take rates and default price anchors your package will live inside.

The spectrum is not a maturity ladder you must climb. It is a portfolio choice. Plenty of excellent businesses live permanently at Position 2; most readers of this course should aim there first, because Position 2 captures most of the margin improvement of a product with a fraction of the engineering and support surface.

### The economics that change at each step

Three variables move as you go right on the spectrum, and they move against each other:

1. **Marginal delivery cost** falls: from ~100% of your available hours (custom) to a runbook's worth of hours (productized service) to hosting-plus-support (product).
2. **Scope risk** transfers from the buyer to you. In a custom engagement, an ambiguous scope becomes a change order the buyer pays for ([[05-fri-commercial-sow-for-ai-projects|Block 1 Friday]]). In a package, an ambiguous scope becomes *your* unpaid support burden, multiplied by every customer who read the promise differently.
3. **Demand requirements** rise. A custom-services business is viable at three clients a year. A $250/month product needs hundreds of customers before it pays your rent, which means it needs distribution (Thursday) that a services business never had to solve.

The mistake this lesson exists to prevent: sliding right on the spectrum because products are higher status, before your demand and delivery engineering can support the move. The Artisan price is aspirational for Artisan's funders; for you, on customer one, it is a trap.

## Layer 2 — Where agent businesses actually sit in 2026, with revenue evidence

The instinct when packaging is to look at famous products. Look instead at the whole distribution, because the money is spread across all four positions and the evidence says the middle is thicker than the ends.

**The product end is real but capital-intensive.** Harvey, the legal-AI vertical product, reached roughly $190M ARR by January 2026 (up from ~$100M in August 2025) and raised at an $11B valuation in March 2026, serving 100,000+ lawyers across 1,300+ organizations.[^1][^2] Sierra, Bret Taylor's customer-service agent company, raised $950M at a $15.8B valuation in May 2026 with $150M+ ARR and 40%+ of the Fortune 50 as customers.[^3] Both are genuine products in the Position 3 sense. Both also carry deployment machinery a solo operator cannot copy: Sierra's platform-and-implementation commitment reportedly starts above $200K per year before per-outcome charges, which is to say the "product" ships wrapped in a services layer priced like enterprise consulting.[^4] The lesson from the top of the market is not "build a product." It is: even at $150M ARR, *agent products ship with heavy delivery scaffolding*, and someone charges for it.

**The productized-service middle is where operators like you live.** The 2026 agency-pricing literature — surveys and buyer guides rather than audited books — describes a recognizable shape: two-to-four-person shops running an offer suite of fixed-scope agent packages, $1,500–$4,500/month per client, reaching mid-five to low-six-figure annual revenue on a handful of retainers, with outlier operators documenting $50K/month and one widely-circulated solo case at $77K/month before restructuring around a team.[^6][^7][^8] Treat the outliers as existence proofs, not medians. The structural claim is better evidenced than the income claims: a 250-agency survey in 2026 found 56.8% of agencies selling or moving toward outcome-based engagements, which only works when the engagement is standardized enough that outcomes are comparable across clients — i.e., the middle of the market is productizing whether it uses the word or not.[^9]

**The white-label channel is a shortcut with a toll.** Platforms like Stammer AI exist specifically so agencies can resell chat and voice agents under their own brand: the platform costs the agency roughly $197/month, and agencies typically charge clients $300–$500/month per agent plus a 3–5× markup on usage.[^10] That is Position 2 economics built on someone else's Position 3 product. Wednesday's lesson takes the build-vs-white-label decision seriously; today, register that the *existence* of a rental productization layer proves the demand: hundreds of agencies are selling packaged agents right now without writing agent code at all.

**What is thin on the ground: verified solo product businesses.** The "$10K/month from my GPT" genre remains almost entirely unverified. OpenAI's GPT Store builder-payout program shipped, but public evidence of substantive builder revenue is scarce enough that even sympathetic 2026 guides describe monetization as unproven.[^11] When you cannot find revenue evidence for a position on the spectrum after honest searching, that absence is data. The verified money in 2026 agent-land is: venture-scale vertical products at the top, productized services and white-label resale in the middle, and custom services everywhere, forever.

## Layer 3 — Scope collapse: the productization move

If the week has one mechanical skill, it is this. A build becomes a package by *collapsing scope along four axes* until delivery is repeatable. Take the Week 8 scraper-summarizer as the running example.

**Axis 1 — Input collapse.** Custom: "we'll monitor whatever sources matter to you." Packaged: "we monitor up to 12 public web sources and 3 RSS feeds you nominate from our supported-source list." The supported-source list is the package. Every source type you support is an engineering surface you maintain against a web that actively resists crawling ([[03-wed-the-scraping-stack-legally-and-technically|Week 8 Wednesday]]); every source type you exclude is a support ticket you never receive.

**Axis 2 — Output collapse.** Custom: "reports shaped to your needs." Packaged: one output artifact with a fixed schema: a daily brief, ≤600 words, five sections, delivered to one Slack channel at a configured hour. Fixed outputs are what make the [[06-sat-rag-evaluation|eval harness]] reusable across customers, which is what makes your quality guarantee (Tuesday) affordable.

**Axis 3 — Integration collapse.** Custom: "we'll connect to your systems." Packaged: Slack or email delivery, period, at the starter tier. Each integration you admit to the package multiplies your credential-management, failure-mode, and support surface (Wednesday). The tier ladder exists partly to charge properly for integration surface: starter gets one delivery channel, enterprise gets the API.

**Axis 4 — Segment collapse.** Custom: anyone who pays. Packaged: one niche, so that customer five's configuration looks like customer two's. This is [[04-thu-niche-as-a-hypothesis|Block 1 Week 2's]] niche logic returning with an engineering payoff: niche homogeneity is not just a marketing choice, it is what makes one golden eval set, one onboarding checklist, and one supported-source list serve the whole customer base.

Scope collapse feels like giving up revenue. The arithmetic says otherwise. A custom engagement at $8K/month that consumes 30 hours/month of your labor nets you ~$267/hour with zero leverage. The same build collapsed into a $1,500/month package that consumes 2 hours/month per customer after onboarding nets $750/hour at four customers and climbs with each one, while the runbook, eval set, and onboarding materials appreciate instead of evaporating at contract end. The package is not the discount version of the service. It is the version where your best work stops being disposable.

### What packaging changes about margin, delivery, and support

Be precise about what you are signing up for, because packaging *worsens* two things while improving the third:

- **Margin (improves).** Services gross margins in AI work run decent-but-bounded because scope wobble eats them; packaged margins are structurally higher because delivery cost amortizes. Friday quantifies this with live model pricing; the preview is that a well-collapsed package on Sonnet-5-class inference carries software-like gross margins even at $1,500/month price points.
- **Delivery (changes kind).** You trade proposal-writing for runbook-writing. The runbook (Wednesday, and Saturday's build) is now a product asset with a version number. A delivery that deviates from the runbook is no longer "flexibility"; it is a defect in either the runbook or the sale.
- **Support (worsens, permanently).** Custom clients call you; package customers *expect a support function*. Every promise on the one-pager is a support liability multiplied by customer count. This is why inclusion/exclusion lists (Tuesday) are written defensively, and why "we'll just handle that manually for now" is the most expensive sentence in a young package business.

## Layer 4 — The fork, and the snowflake counter-argument

Every builder who can sell hits the same fork within a year: *agency or product?* Take more custom engagements at higher per-deal revenue, or bet the calendar on a package? The honest 2026 answer is that the market itself is split, and a great deal of new money just bet against packaging.

**The live controversy: productized agents vs "every deployment is a snowflake."**

*Position A — deployments are snowflakes, and the giants just priced that belief.* Between May and July 2026, the largest AI vendors committed enormous sums to forward-deployed engineering (FDE): embedding their own engineers inside customers to build, deploy, and operate agent systems, because "agentic AI does not ship itself." AWS alone announced a $1B investment in a new unit embedding engineers with customers on June 30, 2026 (CNBC), joining publicized FDE pushes at OpenAI, Anthropic, and Microsoft; one industry analysis tallies the combined 2026 commitments near $9B, and FDE job postings grew ~729% year over year (roughly 640 to 5,300+ active listings, April 2025 to April 2026).[^12][^14][^15] The FDE thesis in one sentence: a capable model plus an API does not become a working system; it must be fitted to the customer's data, permissions, workflows, and definitions of success, by an engineer inside the building. If the best-funded companies on earth believe enterprise agent deployments resist packaging, a solo operator claiming "fixed scope, fixed price, ten-day delivery" should at least explain why their corner of the market is different.

*Position B — the snowflake problem is a scoping failure, not a law of nature.* The counter comes from the productization playbooks themselves: Perspective AI's 2026 FDE guide argues that if more than 30–40% of your deployments require significant forward-deployed effort, "the problem is no longer go-to-market, it is product" — heavy per-customer fitting is a signal your scope is wrong, not that packaging is impossible.[^16] Artisan's $250 self-serve tier and Fin's $0.99-per-resolution product (Tuesday) are shipping proof that *narrow, well-collapsed* agent scopes deploy without embedded engineers. The synthesis this course endorses: snowflake-ness is mostly a function of *integration surface and outcome ambiguity*. Enterprise deployments touching bespoke ERPs with contested success metrics are snowflakes; a niche-collapsed monitor-and-brief package with one delivery channel and a golden eval set is not. You choose your position on the snowflake spectrum when you choose your scope. The FDE wave is not evidence that packaging fails; it is evidence about *which scopes* still require humans in the building, and those scopes are exactly the ones your package should exclude.

**How to actually take the fork.** Michael Seibel's standard YC counsel applies with unusual force here: do things that don't scale until the pattern is undeniable. The disciplined path is custom → productized, in that order: sell three-to-five custom engagements in one niche (Block 1), notice the 70% of work that repeated, collapse scope around that 70%, and sell the package to the next buyer *instead of* a proposal. The fork is rarely a single decision; it is a ratio you shift quarter by quarter, and the trap is not choosing wrong but drifting — running "packages" that are secretly custom engagements with a brochure, carrying product-level prices with services-level delivery costs.

## Runnable experiment — audit your builds for packageability

Allow 60–90 minutes. Output: a scored inventory and one chosen package candidate. This choice feeds every remaining day of the week.

**Step 1 — Inventory.** List every build you have from Weeks 4–8 (and any client work). For each, write one sentence: what goes in, what comes out, who pays.

**Step 2 — Score.** In Claude Code or Claude.ai, paste this rubric and your inventory:

> *Score each build 1–5 on six axes: (1) Input standardization — can the inputs be enumerated on a supported-list a customer picks from? (2) Output fixity — is the output one artifact with a fixed schema? (3) Integration surface — how few external systems must be touched per customer? (5 = one channel). (4) Segment homogeneity — would customer #5's configuration look like customer #2's inside one niche? (5) Eval maturity — does a golden set + regression harness exist today? (6) Demonstrated demand — has anyone paid, or asked to pay, for this or its obvious neighbor? For each score, demand one sentence of evidence; reject vibes. Then compute the total and flag the top build.*

**Step 3 — Interrogate the winner.** For the top-scoring build, have Claude draft the four scope collapses (input, output, integration, segment) as explicit lists: supported/excluded sources, fixed output schema, admitted integrations per tier, named niche. Then argue with it: every item on the "supported" lists must be something you could deliver to a second customer tomorrow without new engineering.

**Pass bar:** one build scoring ≥22/30, with all four collapse lists written and no "supported" item you cannot deliver today. If nothing scores ≥22, the correct output of this experiment is the sentence "I am not ready to package; my gap is X" — usually eval maturity or demand evidence — and X becomes this week's side quest, not a reason to skip the week.

## Problem set

1. **Spectrum placement.** Place five real businesses on the four-position spectrum: Harvey, Sierra, a Stammer-based white-label agency, your own current practice, and one AI business you follow. For each, name the evidence (what does marginal delivery cost them?) rather than the branding.
2. **Scope-collapse drill.** Take the Week 5 report generator and write its four collapse lists for a specific niche you know (e.g., Shopify DTC brands, regional logistics, dental groups). Which single axis was hardest to collapse? That axis is where your support costs would concentrate.
3. **Steelman the snowflake.** In ≤300 words, argue Position A (deployments are snowflakes) *for your own chosen package specifically*. Name the three customer-specific surfaces most likely to resist standardization. If you cannot name three, you have not looked hard enough; if you can name six, reconsider the package.
4. **The drift audit.** Write the three warning signs that would tell you, six months in, that your "package" has drifted back into custom services with a brochure. Make them measurable (e.g., "onboarding hours for customer N+1 exceed customer N's").
5. **Fork arithmetic.** Using your real (or honestly estimated) numbers: at what customer count does your package's monthly revenue exceed one custom engagement's, and at what customer count does *revenue per your hour* exceed it? Those are two different numbers; the second is the one that matters.

## Reflection questions

- Which of your skills does a package *stop* selling? (Custom work sells your judgment; packages sell your process. What happens to the judgment premium?)
- If Artisan-style self-serve pricing arrives in your niche at 1/10th your price, what exactly is the delta a buyer still pays you for? Write the sentence you would say on that sales call.
- The FDE wave means the biggest vendors are hiring people to do, inside enterprises, roughly what you do. Threat, validation, or exit path?

## Common failure modes at scale

- **Packaging before pattern.** Building the one-pager after one client (or zero). The package's scope should be extracted from repetition you have observed, not imagined. Seibel's correction: sell it manually, uncomfortably, several times first.
- **Scope collapse in the brochure only.** The pricing page says "12 sources"; the founder says yes to source 13 on the first sales call. One exception per customer and you are running unpriced custom services at package prices.
- **Copying Position-3 pricing with Position-2 delivery.** Charging $250/month because Artisan does, while your delivery still consumes founder-hours per customer per week. Artisan's price is downstream of self-serve engineering you have not built.
- **Confusing the demo with the product.** A build that demos well to you is not deliverable-by-runbook. The test is whether a competent stranger could deliver customer #2 from your written materials alone (Saturday's pass bar).
- **Niche promiscuity.** Selling the package into three unrelated niches "to see what sticks," which triples the eval sets, the supported-source lists, and the support vocabulary. Validate one niche to saturation first ([[05-fri-niche-validation-and-unit-economics|Block 1 Week 2 Friday]]).
- **Treating the FDE evidence as permission to stay custom forever.** "Everything's a snowflake" is also a comfortable excuse to never write the runbook. The 30–40% heuristic cuts both ways: if *fewer* than a third of your deliveries need real per-customer engineering, you are leaving package margins on the table.

## My take (reviewer lens)

**Michael Seibel** would push back on this lesson's tidy spectrum: "You don't have a productization problem, you have a customers problem. Nobody reading this has ten customers begging for the same thing yet. Go sell the ugly custom version five more times; the package will write itself from your invoices." He is right that the spectrum tempts premature abstraction, and the experiment's pass bar (demand evidence scored, not assumed) exists because of that critique. **swyx** would push on sequencing from the other side: in the 2026 AI-engineering zeitgeist, distribution compounds faster than delivery, so the scarce asset is not a runbook but an audience that trusts you in a niche; he would want Thursday's distribution material *before* Monday's packaging material, and he has a point this course resolves by making you draft channel plans mid-week rather than at the end. **Mira Murati's** lens lands differently: her Thinking Machines bet (open-weight Inkling plus Tinker fine-tuning) is that customization beats generality, which reads at first like the snowflake position — but it actually argues that *customization itself can be productized* when the customization surface is engineered deliberately. That is the strongest version of this lesson's thesis, and the lesson under-develops it: your package's config file (Wednesday) is a miniature Tinker, and the depth of what it can express is a product decision, not an accident.

## Further reading

**Must-read**

- Bret Taylor on AI agents, outcome-based pricing, and business models (A Cheeky Pint / Sierra podcast, 2025–26). The clearest articulation of "sell the process, not the seat" from someone doing it at scale.[^4]
- Perspective AI, *How to Build a Forward-Deployed Engineering Function: A 2026 Founder's Playbook*. Read it adversarially: every FDE task it lists is a candidate for your package's exclusion list.[^16]
- [[01-mon-what-a-sales-agent-is|Week 4 Monday]] — the Artisan/11x/Clay teardown this lesson builds on. Re-read Layer 4 (pricing after the collapse) with packaging eyes.

**Recommended**

- CNBC, *AWS puts $1 billion into new AI unit to embed engineers with customers* (June 30, 2026).[^12]
- Digital Applied, 250-agency survey on agentic engagements and outcome pricing (2026).[^9]
- Taskip / Digital Agency Network 2026 agency-pricing guides, for the productized-retainer band data.[^6][^7]

**Optional**

- Sacra's Harvey and Sierra revenue teardowns, for how analysts reconstruct private ARR.[^2]
- Stammer AI's public agency materials, as a specimen of white-label economics.[^10]

## Citations

[^1]: CNBC, *Legal AI startup Harvey valued at $11 billion in funding round*, March 25, 2026 ($200M round led by GIC and Sequoia; ~$11B valuation). https://www.cnbc.com/2026/03/25/legal-ai-startup-harvey-raises-200-million-at-11-billion-valuation.html ; corroborated by Harvey's own announcement, https://www.harvey.ai/blog/harvey-raises-at-dollar11-billion-valuation-to-scale-agents-across-law-firms-and-enterprises (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Sacra, *Harvey revenue, valuation & funding* (~$190M ARR by Jan 2026, up from ~$100M Aug 2025; 100,000+ lawyers, 1,300+ organizations). https://sacra.com/c/harvey/ ; corroborated by https://valueaddvc.com/blog/harvey-ai-valuation-revenue-2026-legal-ai-11b (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Sierra funding and scale — $950M raise at $15.8B valuation, May 2026; $150M+ ARR; 40%+ of Fortune 50 as customers. https://chatforest.com/reviews/sierra-ai-enterprise-agent-platform-bret-taylor-950m-series-e-2026/ ; corroborated by https://sacra.com/c/sierra/ and https://www.webpronews.com/bret-taylor-drives-ai-agent-innovation-with-10b-sierra-valuation/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Bret Taylor, *AI agents, outcome-based pricing, and the OpenAI board*, A Cheeky Pint podcast (also mirrored at sierra.ai/resources/podcasts): per-resolution pricing with free escalation; "the atomic unit of AI productivity is a process, not a person." https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents ; https://sierra.ai/resources/podcasts/bret-taylor-of-sierra-on-ai-agents-outcome-based-pricing-and-the-openai-board (search-verified 2026-07-17)

[^5]: Artisan, *Artisan launches Ava 2.0: the first autonomous AI BDR, now self-serve* (May 2026; $250/month entry, 10× cut from $2,500; $300 free credits; <10-minute self-serve onboarding). https://www.artisan.co/blog/artisan-launches-ava-2-0-the-first-autonomous-ai-bdr-now-self-serve ; corroborated by https://www.11x.ai/guides/artisan-pricing and https://tomba.io/blog/artisan-pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Taskip, *AI Automation Agency Pricing: 6 Proven Models for 2026* (productized retainer bands; outbound packages $1,500–$4,000/month). https://taskip.net/ai-automation-agency-pricing/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^7]: Digital Agency Network, *AI Agency Pricing Guide 2026* ($1,500–$4,500/month productized band; local agents $300–$1,500/month; content bundles $1,000–$2,000/month). https://digitalagencynetwork.com/ai-agency-pricing/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: Build with Dew, *Productized AI services: 7 offers buyers want in 2026* (offer-suite structure; $50K/month operator cases; solo $77K/month case, reported not audited). https://buildwithdew.com/blog/productized-ai-services-7-offers-buyers-want-2026 (search-verified 2026-07-17; treat income claims as existence proofs)

[^9]: Digital Applied, *Agentic AI adoption survey 2026 — 250 agencies* (56.8% of agencies selling or moving to outcome-based engagements). https://www.digitalapplied.com/blog/agentic-ai-adoption-survey-2026-250-agencies — also cited in this vault's July 2026 landscape delta (counts as one corroboration under the amended protocol).

[^10]: Stammer AI public positioning and agency economics (~$197/month platform; agencies charging $300–$500/month per agent plus 3–5× usage markup). https://stammer.ai/ ; corroborated by https://pickaxe.co/post/white-label-ai-tools-for-agencies (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^11]: OpenAI GPT Store / builder monetization state — builder payout program rolled out to major markets, but little public evidence of substantive builder revenue; apps monetization still limited (see Thursday's lesson). https://www.wildnetedge.com/blogs/gpt-store-monetization-guide ; https://www.snaplama.com/blog/how-to-create-chatgpt-apps-and-monetize-them-complete-2026-guide (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^12]: CNBC, *AWS puts $1 billion into new AI unit to embed engineers with customers, joining growing wave*, June 30, 2026. https://www.cnbc.com/2026/06/30/aws-amazon-ai-forward-deployed-engineers.html ; corroborated by AWS APN blog, https://aws.amazon.com/blogs/apn/introducing-forward-deployed-engineering-for-partners-winning-the-future-of-enterprise-ai/ (search-verified 2026-07-17)

[^13]: Salesforce ISV revenue-share terms for AgentExchange distribution (15% ISV / 25% OEM Percentage Net Revenue). https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/appexchange_checkout_rev_share.htm ; https://help.salesforce.com/s/articleView?id=000394757&language=en_US&type=1 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^14]: Building Agentic AI, *Forward Deployed Engineering: Why Agentic AI Doesn't Ship Itself* (aggregate ~$9B 2026 FDE commitments across Anthropic, OpenAI, AWS, Microsoft — aggregate figure single-source; treat as order-of-magnitude). https://buildingagenticai.com/blog/forward-deployed-engineering/ (search-verified 2026-07-17)

[^15]: TechTarget, *The rise of the AI forward-deployed engineer* and MarkTechPost, *What is a Forward Deployed Engineer* (FDE postings +729% YoY, ~643 → 5,300+ listings Apr 2025–Apr 2026). https://www.techtarget.com/searchenterpriseai/feature/The-rise-of-the-AI-forward-deployed-engineer ; https://www.marktechpost.com/2026/05/20/what-is-a-forward-deployed-engineer-the-ai-role-openai-anthropic-and-google-are-hiring-in-2026/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^16]: Perspective AI, *How to Build a Forward-Deployed Engineering Function: A 2026 Founder's Playbook* (the 30–40% FDE-effort threshold as a product-problem signal). https://getperspective.ai/blog/how-to-build-forward-deployed-engineering-function-founder-playbook-2026 (search-verified 2026-07-17; single-source heuristic, attributed)

_last_verified: 2026-07-17_
