---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 4
day_name: thu
session_slug: create-your-first-sellable-agent-package
date_due: 2026-07-16
tags: [distribution, marketplaces, agentexchange, aws-marketplace, claude-marketplace, chatgpt-apps, take-rates, n8n-templates, resellers, co-sell, direct-sales, channel-economics]
sources:
  - salesforce-agentexchange-2025
  - appnigma-appexchange-2026
  - rapidclaw-agent-marketplaces-2026
  - salesforce-isv-revshare
  - aws-agents-tools-launch-2025
  - siliconangle-aws-agents-2026
  - siliconangle-claude-marketplace-2026
  - venturebeat-claude-marketplace-2026
  - techzine-claude-marketplace-2026
  - openai-apps-in-chatgpt
  - openai-app-submissions
  - wildnetedge-gpt-store-monetization
  - n8n-community-marketplace
  - futurumgroup-agentexchange-2026
last_verified: 2026-07-17
word_count_target: 4500
---

# Distribution surfaces for agent products in 2026 — marketplaces, take rates, and what actually drives installs

## Why this matters

A package nobody discovers is a hobby with a tier sheet. Distribution is where most first packages die, and 2026 has made the terrain genuinely confusing: four hyperscaler-class marketplaces launched or restructured within eighteen months, each pitching itself as *the* storefront for agents, while the first-generation storefront (the GPT Store) quietly demonstrated that three million listings and no revenue is a possible outcome. Today you map the real surfaces — enterprise marketplaces with their take rates and procurement rails, developer and template surfaces, the white-label reseller channel, and the direct motion you already know from Block 1 — and, more importantly, you learn to read the evidence on what produces *installs and revenue* versus what produces a logo on a listings page. You leave with a two-channel plan for your package and the math to defend it.

## Prerequisites

- Tuesday's tier sheet and Wednesday's delivery architecture: channels constrain both (a marketplace listing demands self-serve-ish onboarding; an enterprise co-sell motion demands the isolated-tenant tier).
- [[02-tue-outbound-mechanics-and-positioning|Block 1's outbound machinery]] and [[01-mon-where-ai-services-demand-lives|demand map]]. One-line recap: demand for AI work concentrates where a named operational pain meets a budget owner; nothing about marketplaces changes that — they only change who introduces you.
- [[03-wed-building-in-public|Block 1 Week 2's]] building-in-public discipline, which is about to become your cheapest working channel.

## Layer 1 — The 2026 marketplace map, with numbers

Four enterprise-grade surfaces matter, and they are running four different strategies. Learn the strategy before the listing form.

**Salesforce AgentExchange — the incumbent-ecosystem play.** Launched March 2025 as the "trusted marketplace for Agentforce," then made the center of gravity in April 2026 when Salesforce merged AppExchange, the Slack Marketplace, and the Agentforce ecosystem into a single unified AgentExchange, now listing on the order of 14,000 vetted agents, actions, and apps.[^1][^2][^3] Monetization is mature because it inherited two decades of AppExchange plumbing: component sales, subscriptions, and usage/outcome add-ons, with Salesforce's standard Percentage Net Revenue take — **15% for ISV apps, 25% for OEM bundles** that embed a Salesforce license.[^4] The strategic read: AgentExchange is not a discovery engine, it is a *procurement rail into Salesforce's installed base*. You list there when your buyer already lives in Salesforce and your package can present as an Agentforce-compatible component; you are paying 15 points for contract paper and security review the buyer's IT already trusts.

**AWS Marketplace's "AI Agents and Tools" category — the infrastructure play.** Launched at the July 2025 AWS Summit New York with 900+ listings from day one (Anthropic, Salesforce, IBM, PwC, Stripe, and a long startup tail), with search filters for MCP and A2A protocol support and one-click-ish deployment onto Bedrock AgentCore; by July 2026 AWS was calling agentic AI the fastest-growing category in AWS Marketplace history.[^5][^6] The mechanics that matter to you: listings can be SaaS/API-based (you host, AWS bills), and the buyer's spend can draw down committed AWS budgets — the same enterprise-budget-capture trick that made cloud marketplaces work, evidenced at scale by Salesforce itself reporting $2B+ in bookings through AWS Marketplace in two years.[^7] The read: AWS Marketplace converts *existing enterprise cloud budgets* into your revenue; it is paperwork-heavy up front and nearly free demand-side, because the "demand" is your own prospect preferring to buy you through a bill they already pay.

**Claude Marketplace — the no-take-rate curation play.** Anthropic launched it March 6, 2026, in limited preview: an enterprise catalog of Claude-powered products from launch partners Snowflake, GitLab, Harvey, Rogo, Replit, and Lovable, purchasable partly against a company's existing Anthropic spend commitments — and, pointedly, **Anthropic takes no cut**.[^8][^9][^10] The strategy is legible: Anthropic monetizes the tokens underneath, so the marketplace exists to make Claude the enterprise default, not to earn commission. For you today it is aspirational (limited preview, marquee partners), but it sets two precedents worth tracking: the zero-take-rate anchor other platforms must now argue against, and spend-commitment drawdown as the real buyer motivation.

**ChatGPT apps and the post-GPT-Store economy — the consumer-scale play, still unmonetized.** OpenAI replaced the GPT Store's center of gravity with apps in ChatGPT (Apps SDK, built on MCP), opened third-party submissions with an app directory rolling out from early 2026, and shipped early partners like Booking.com, Canva, Coursera, Figma, Spotify, and Zillow.[^11][^12] But monetization remains the tell: as of mid-2026, apps may link out to complete purchases for *physical goods only*; digital goods, subscriptions, and in-app services are not yet allowed, with agentic commerce (the OpenAI/Stripe Agentic Commerce Protocol) in beta.[^11][^13] And the GPT Store's own builder-payout program produced so little publicly documented builder revenue that even sympathetic guides describe it as unproven.[^13] The read: enormous audience, no rail yet for a B2B package to charge on. Watch it; do not bet your quarter on it.

**The smaller surfaces.** n8n's ecosystem (9,400+ community workflow templates by May 2026) monetizes indirectly: the official creator hub trades templates for visibility and affiliate revenue, while third-party marketplaces (n8nmarkets and peers) and Gumroad-style direct sales handle paid templates.[^14] Template listings are lead magnets more than products: the template demonstrates competence; the money is the package behind it. The same logic covers vertical directories (Slack's marketplace now folded into AgentExchange;[^2] WhatsApp-adjacent agent directories remain fragmented enough in mid-2026 that this course declines to name a canonical one, so treat any single directory's claims there with suspicion).

One structural note that spans all of these surfaces: the discovery metadata is converging on agent-readable standards. AWS's category filters listings by MCP and A2A protocol support;[^5] OpenAI's Apps SDK is built on MCP;[^11] and the MCP ecosystem's official registry (Block 3's territory) means a well-described MCP server is itself a tiny distribution surface, findable by tooling rather than by browsing. The practical implication for a package builder is cheap and asymmetric: publish clean machine-readable descriptions of what your package's tools do (an MCP manifest, an honest README schema, structured capability text on your own site) even before any marketplace listing. It costs an afternoon, it cannot hurt, and if the agent-mediated-procurement thesis plays out even partially, the packages with legible capability metadata get found first. If it does not play out, you have documentation. This is the rare distribution bet with no downside case.

### Take-rate economics in one table

| Surface | Take rate | What you're actually buying | Fits your package if… |
|---|---|---|---|
| AgentExchange (ISV) | 15% PNR (25% OEM)[^4] | Procurement trust + Salesforce installed base | Buyer lives in Salesforce; you can pass security review |
| AWS Marketplace agents category | Negotiated/listing fees; buyer draws down cloud commits[^5][^7] | Enterprise budget capture + co-sell | Enterprise buyers; you can handle AWS's listing process |
| Claude Marketplace | 0%[^10] | Curation halo + Anthropic spend drawdown | You're big enough to be curated (not yet — track it) |
| ChatGPT apps | N/A for digital services today[^11] | Audience, someday a rail | Consumer-adjacent, patient |
| n8n/template surfaces | Platform-dependent, often ~0 + affiliate[^14] | Lead generation via demonstrated competence | Your package has a teachable core workflow |
| White-label resellers (Wed) | Effectively 50–70% of end price | Someone else's sales force | Commodity agent shapes, volume over margin |
| Direct (Block 1 motion) | 0% | Your own time | Always; the question is only CAC per hour |

## Layer 2 — What actually drives installs: evidence over vibes

The uncomfortable evidence, assembled:

**Listings are not demand.** The GPT Store hosted millions of GPTs; documented builder revenue remains near-invisible, and OpenAI itself deprioritized the store's economy in favor of the apps program.[^11][^13] AgentExchange's ~14,000 listings sit atop the AppExchange power-law: two decades of that marketplace produced a small head of ISVs earning real revenue and a very long tail of logos.[^2][^3] A listing is a *credential*, not a channel.

**What converts, when marketplaces do work, is one of three mechanisms.** (1) **Budget capture**: the buyer wanted you anyway and the marketplace let them pay you out of a committed cloud/AI budget — the mechanism behind AWS Marketplace's numbers and Claude Marketplace's drawdown design.[^7][^10] (2) **Procurement compression**: security review, DPAs, and vendor onboarding pre-cleared by the platform; on AgentExchange this is most of what the 15% buys.[^4] (3) **Platform co-sell**: a platform seller carrying your listing into their account calls because it closes *their* gap. All three mechanisms share a property: **the demand originated outside the marketplace.** The marketplace is a rail, not a spring.

**Therefore the operator sequencing is fixed:** direct first, marketplace second. Your first ten customers come from the Block 1 motion — niche outbound, building in public, referrals from custom work — because ten direct customers teach you the objection map, the real onboarding cost, and the tier that actually sells, none of which a listing dashboard reports. List on a marketplace when (a) a specific prospect asks to buy you through one, or (b) your niche's buyers demonstrably start discovery there. Listing *before* product-channel fit costs listing-maintenance time and, worse, lets you mistake a credential for progress. Instrument the channel question the same way [[06-sat-validation-instrumentation|Week 3 Saturday]] instrumented landing pages: every install/inquiry gets a source, and monthly you compare CAC per channel in hours, not vibes.

## Layer 3 — The controversy: marketplace hope vs direct-sales reality

*Position A — marketplaces are the new app stores; being early is the land grab.* The platform case, argued by Salesforce's ecosystem leadership and sympathetic analysts (Futurum's read is that AgentExchange could cement Salesforce's agentic-platform lead[^3]): agent adoption is following the SaaS playbook at 5× speed; enterprises will default to buying agents where they already have contracts, budgets, and trust; early listers inherit category pages, badges, and co-sell attention before the categories crowd; and the 2026 numbers (14K listings, fastest-growing AWS category, four platforms investing simultaneously) show the channel forming in real time.[^2][^3][^5] Under Position A, a builder who waits is repeating the mistake of the SaaS founders who skipped AppExchange in 2008.

*Position B — for a small operator, marketplaces are where packages go to feel distributed.* The operator case: every mechanism in Layer 2 that makes marketplaces convert presupposes demand you generated elsewhere; take rates and listing maintenance are a tax on margins you haven't earned yet; the GPT Store is the controlled experiment in what pure-listing distribution yields (approximately nothing);[^13] and the platforms' own behavior tells you who marketplaces serve — AWS and Salesforce simultaneously built *forward-deployed engineering* and co-sell teams (Monday's lesson) because even they know listings don't deploy themselves. Michael Seibel's standing YC advice is Position B's spine: recruit your first users by hand, one by one, from the niche you know; anything that feels like scalable distribution before product-market fit is procrastination with a dashboard.

*The synthesis this course endorses:* both positions are right about different company sizes, and the crossover is legible. Marketplaces in 2026 are **procurement infrastructure maturing ahead of discovery infrastructure**. Use them as rails (when a real buyer wants one), collect them as credentials (when the listing cost is low), and never confuse them with a demand engine. Revisit quarterly: the moment two prospects in one quarter ask "are you on AgentExchange/AWS?", that channel has crossed from hope to rail *for your niche*, and the 15% becomes cheap.

## Layer 4 — Designing your two-channel plan

A first package gets exactly two channels: one you fully control, one you rent. More than two fragments your attention; fewer leaves you hostage.

**The controlled channel** is a Block 1 motion aimed at package buyers: niche outbound with the one-pager attached (the package makes outbound *easier* than services outbound, because the ask is "look at this priced thing," not "hire my judgment"); building-in-public in the niche's watering holes with artifacts the package produces (a redacted weekly brief is a better ad than any thread about AI); referral mechanics with teeth (a named discount for intros that convert, offered at the moment of a customer's first delighted message, not in a footer). Set a number: 30 qualified conversations in the niche in 30 days, tracked in the same CRM discipline Block 1 taught.

**The rented channel** is chosen by where your niche's buyers already pay or search. Decision shortcuts: buyers in Salesforce daily → AgentExchange candidacy (budget the security-review effort honestly); enterprise IT buyers with cloud commits → AWS Marketplace listing when deal #1 asks for it; technical/SMB operators → template-surface lead magnets (an n8n template or open MCP server that demonstrates the package's core trick, with the package as the "done for you" tier);[^14] commodity agent shape → reseller/white-label recruitment (Wednesday's economics in reverse: *you* supply the platform, agencies supply distribution).

For each channel, write the four numbers before committing: expected CAC (in hours and dollars), take rate or fee, time-to-first-customer, and the kill criterion (the date and threshold at which you stop). Channels without kill criteria become identity.

### Worked example: the Niche Radar two-channel plan

To make the four-number discipline concrete, here is the running example's plan, written the way yours should read when the experiment below is done.

**Controlled channel: founder-led outbound plus artifact-in-public, aimed at DTC skincare operators.** The buyer is a head of brand or founder at a $2M–$20M DTC skincare company; they congregate in two or three operator communities, a handful of newsletters, and each other's group chats. The motion: 10 personalized sends per week using the one-pager and one *redacted live brief* as the attachment (the artifact is the pitch; nobody has to imagine the product), plus one public post per week decomposing a real trend the Radar caught early, footer-attributed. Numbers: CAC estimated at 6 founder-hours per closed customer at a 5% send-to-close rate (30 conversations to close 1.5 customers in month one is the honest expectation, not the fantasy); take rate zero; time-to-first-customer 2–4 weeks; kill criterion: if 60 sends across 6 weeks produce zero demo calls, the *niche or the one-pager* is wrong, and the fix is Monday's segment choice, not more sends.

**Rented channel: template-surface lead magnet.** A free, genuinely useful n8n workflow ("competitor price-change monitor for one source, delivered to Slack") published to the community library and a third-party template marketplace, with the package as the named done-for-you tier in the template's README.[^14] Numbers: CAC near zero marginal (one weekend to build, one hour per month to maintain); no take rate on the package itself; time-to-first-customer unknowable in advance, honestly stated (templates are a compounding surface, not a faucet); kill criterion: if 90 days produce fewer than 100 template runs and zero package inquiries, retire the maintenance and leave it as a portfolio artifact.

**Explicitly deferred: AgentExchange and AWS Marketplace.** The buyer for a $750–$3,500/month niche package is not procuring through enterprise marketplaces, and the listing overhead (security review, billing integration) fails the CAC test at this price point. The written trigger for revisiting: a single Enterprise-tier prospect whose procurement asks for a marketplace rail, at which point the readiness audit is a deal task with a deal attached, which is the only time marketplace paperwork is ever cheap.

Notice the plan's shape: the controlled channel has weekly quotas and a six-week verdict date; the rented channel costs nearly nothing to hold open; the deferred channels have named triggers instead of guilt. That is what "distribution strategy" means at customer-count zero, and it fits on one page.

## Runnable experiment — channel teardown and the 10-customer plan

Allow 90–120 minutes. Output: a two-channel plan with math, plus a marketplace-readiness audit.

**Step 1 — Buyer-path research (30 min).** In Claude.ai (with web search) or by hand: for your niche, find where three real prospective buyers would encounter a product like yours. Evidence hunt: what do they already buy, through what rail? Any competitor listed on AgentExchange/AWS/template surfaces? What does their procurement plausibly require? Capture URLs, not impressions.

**Step 2 — Channel math (30 min).** Build the four-number table (CAC, take/fees, time-to-first-customer, kill criterion) for four candidate channels: your controlled motion plus three rented candidates. Force ranked honesty:

> *Rank these channels by expected customers-in-90-days per hour of my effort, for a package priced at [your tiers] in [your niche]. Argue against my favorite. Where am I confusing credential with channel?*

**Step 3 — The 10-customer plan (30 min).** Write the plan that gets 10 customers with **zero** marketplace installs: named sub-segments, the outbound artifact (one-pager + demo asset), weekly activity quotas, referral trigger. This plan is the control group your rented channel must beat to earn its keep.

**Step 4 — Marketplace-readiness audit (15 min).** For your top rented candidate, list its actual listing requirements (security questionnaire, billing integration, support SLAs, demo assets) and mark each ready/not-ready against Wednesday's delivery architecture.

**Pass bar:** the two chosen channels each have all four numbers filled with defensible arithmetic; the 10-customer plan contains ≥3 activities you can start Monday without anyone's approval; and the readiness audit yields a dated to-do list, not a mood.

## Problem set

1. **Take-rate breakeven.** At your Standard tier price, compute the annual revenue per customer you keep after (a) AgentExchange 15%, (b) a reseller keeping 60%, (c) direct. How many *extra* customers must each rented channel deliver per year to beat direct at your realistic close rate? Show the arithmetic.
2. **The budget-capture probe.** Draft the two-sentence email asking a real (or realistic) enterprise prospect whether buying through AWS Marketplace against their cloud commit would ease procurement. This question costs nothing and is the single highest-signal marketplace test that exists.
3. **Template-as-lead-magnet design.** Specify the free artifact (n8n template, open config, sample brief) that demonstrates your package's core trick without giving away the runbook, eval harness, or niche packs. Name precisely what the free version lacks and where the "upgrade to done-for-you" seam sits.
4. **Vanity-metric autopsy.** Find any public "we're on N marketplaces" announcement from an agent startup. List what evidence would distinguish real channel revenue from credentialing, and whether the announcement contains any of it.
5. **Quarterly re-read.** Write the three observable triggers that would flip your marketplace decision next quarter (e.g., "two inbound prospects mention it," "a direct competitor gets a category badge," "the platform opens self-serve billing for my shape"). Calendar the review.

## Reflection questions

- Your niche's buyers already trust certain rails with money. Are you choosing channels by where *they* pay, or by which platform's announcement impressed *you*?
- If Anthropic's zero-take-rate curation model wins, marketplaces become pure credibility layers and the money stays in direct relationships. What does your distribution look like in that world? What if Salesforce's 15%-rail model wins instead?
- What did the GPT Store's builders — three million of them — believe that turned out false, and which of your current beliefs rhymes with it?

## Common failure modes at scale

- **Listing as strategy.** Three marketplace listings, zero outbound conversations, "waiting for the channel to kick in." The channel is waiting for you to bring it demand.
- **Take-rate blindness.** Signing a 25% OEM-style deal at Starter-tier prices where COGS + take rate + support leaves single-digit margin. Run Wednesday's COGS math *per channel* before signing.
- **Building for the listing, not the buyer.** Spending a month on a platform's integration requirements for a marketplace your buyers never open. The readiness audit is done *after* the buyer-path evidence, never before.
- **Reseller romance.** Recruiting resellers before the runbook survives strangers (Wednesday's pass bar). A reseller amplifies your delivery quality, including its absence, under someone else's brand.
- **Channel thrash.** A new channel every three weeks, none reaching its kill-criterion date. The two-channel constraint exists because attention is your scarcest COGS.
- **Ignoring the procurement rail your deal is dying in.** The inverse failure: grinding a stalled enterprise deal through bespoke security review when the same buyer could sign in days via a marketplace contract you refused to set up. Rails are real; use them when a live deal asks.

## My take (reviewer lens)

**Ethan Mollick** would anchor this lesson in his adoption research: organizations don't adopt what's listed, they adopt what a specific internal champion has already smuggled in and proven — which means your true distribution surface is the *artifact an employee can forward*: the sample brief, the shared Slack channel, the free template. He'd argue Layer 4 undersells this: the lab-leak path (individual use → team envy → org purchase) has outperformed top-down channels in nearly every wave he's studied, and your package should be designed so its output is inherently forwardable. Fair, and it costs nothing: put the package's name and a one-line "made with" in the artifact footer. **swyx** would make the sharper 2026-native point: the interesting distribution shift isn't human marketplaces at all, it's that *agents are becoming the buyers* — MCP/A2A filters on AWS listings and the ACP commerce rails exist because discovery is starting to happen via agent-readable metadata, and the packages that win 2027 will be the ones whose capabilities are legible to a procurement agent, not just a procurement human. Speculative in degree, correct in direction; it argues for publishing clean, machine-readable capability descriptions early (cheap insurance). **Jerry Liu** would add the composability caveat: listing your package as a monolith undersells it — the same asset decomposed (an MCP tool, a workflow template, a data feed) can occupy three surfaces with three price points, and the RAG-era lesson applies: whoever owns the *interface* to the data owns the renewal. The synthesis of all three: distribution in 2026 rewards packages that leak useful, attributable artifacts at every layer — to humans, to teams, and increasingly to other agents.

## Further reading

**Must-read**

- Salesforce, AgentExchange launch release (March 2025) plus the April-2026 unification coverage — read both to see a marketplace strategy mid-execution.[^1][^2]
- AWS, *Introducing AI agents and tools in AWS Marketplace* (July 2025) and SiliconANGLE's July-2026 growth follow-up.[^5][^6]
- SiliconANGLE / VentureBeat on Claude Marketplace's zero-take-rate launch — the counter-model.[^8][^9]

**Recommended**

- OpenAI, *Introducing apps in ChatGPT and the new Apps SDK* + the developer-submissions post — the consumer surface and its monetization gap, primary-sourced.[^11][^12]
- Futurum, *Can AgentExchange Cement Salesforce's Lead in the Agentic AI Platform Race?* — the strongest Position-A argument.[^3]
- [[02-tue-outbound-mechanics-and-positioning|Block 1 Tuesday]] — the direct motion this lesson keeps pointing back to.

**Optional**

- RapidClaw, *AI Agent Marketplaces 2026* — a wide (if breathless) map of the enterprise-vs-developer marketplace split.[^15]
- n8n community threads on selling workflows — ground truth on template economics from working creators.[^14]

## Citations

[^1]: Salesforce, *Salesforce unveils AgentExchange trusted marketplace for Agentforce*, March 4, 2025 press release. https://www.salesforce.com/news/press-releases/2025/03/04/agentexchange-announcement/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Appnigma, *What Is the Salesforce AppExchange? The 2026 Guide (Partner Console, How It Works, AgentExchange Rebrand)*: April 2026 merger of AppExchange, Slack Marketplace, and the Agentforce ecosystem into unified AgentExchange. https://appnigma.ai/blogs/what-is-salesforce-appexchange-partner-console-2026/ ; listing-count corroboration (~14,000 vetted agents/apps) via https://rapidclaw.dev/blog/ai-agent-marketplace-guide-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Futurum Group, *Can AgentExchange Cement Salesforce's Lead in the Agentic AI Platform Race?*: analyst read on AgentExchange's ecosystem strategy and monetization models (components, subscriptions, usage/outcome add-ons). https://futurumgroup.com/insights/can-agentexchange-cement-salesforces-lead-in-the-agentic-ai-platform-race/ (search-verified 2026-07-17)

[^4]: Salesforce Developers, *How Is Revenue Shared in AppExchange Checkout?* (ISVforce Guide) and Salesforce Help, *Partner Program FAQ: AgentExchange ISV*: 15% ISV / 25% OEM Percentage Net Revenue; fixed-fee alternative; AgentExchange Marginal PNR program. https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/appexchange_checkout_rev_share.htm ; https://help.salesforce.com/s/articleView?id=000394757&language=en_US&type=1 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: AWS, *Introducing AI agents and tools in AWS Marketplace*, July 2025 (launch at AWS Summit New York; 900+ listings; MCP/A2A filters; Bedrock AgentCore deployment; SaaS/API listing mechanics). https://aws.amazon.com/about-aws/whats-new/2025/07/ai-agents-tools-aws-marketplace/ ; https://docs.aws.amazon.com/marketplace/latest/userguide/listing-saas-ai-agents.html (search-verified 2026-07-17)

[^6]: SiliconANGLE, *Enterprise agents drive AI growth in AWS Marketplace*, July 15, 2026 — agentic AI as the fastest-growing category in AWS Marketplace history. https://siliconangle.com/2026/07/15/aws-product-listing-service-enterprise-agents-ai-awsmarketplaceseries/ ; launch-scale corroboration via https://blog.tmcnet.com/blog/rich-tehrani/ai/aws-marketplace-launches-ai-agents-tools-category-with-900-solutions-for-enterprise-deployment.html (search-verified 2026-07-17)

[^7]: Salesforce, *Salesforce and AWS Deepen Collaboration… Agentforce 360 for AWS*: Salesforce surpassing $2B total bookings through AWS Marketplace in two years; budget-drawdown mechanics. https://www.salesforce.com/news/stories/agentforce-360-for-aws-announcement/ (search-verified 2026-07-17; single primary source for the $2B figure, vendor-disclosed)

[^8]: SiliconANGLE, *Anthropic launches Claude Marketplace with third-party cloud services*, March 6, 2026 — launch partners Snowflake, GitLab, Harvey, Rogo, Replit, Lovable; limited preview; purchases financeable against Anthropic spend commitments. https://siliconangle.com/2026/03/06/anthropic-launches-claude-marketplace-third-party-cloud-services/ (search-verified 2026-07-17)

[^9]: VentureBeat, *Anthropic launches Claude Marketplace, giving enterprises access to Claude-powered tools from Replit, GitLab, Harvey and more*, March 2026. https://venturebeat.com/technology/anthropic-launches-claude-marketplace-giving-enterprises-access-to-claude (search-verified 2026-07-17)

[^10]: Techzine, *Anthropic launches Claude-powered app marketplace without taking a cut*, March 2026 — the zero-take-rate model. https://www.techzine.eu/news/applications/139359/anthropic-launches-claude-powered-app-marketplace-without-taking-a-cut/ ; corroborated by https://openclawai.io/blog/claude-marketplace-anthropic-enterprise-procurement (search-verified 2026-07-17)

[^11]: OpenAI, *Introducing apps in ChatGPT and the new Apps SDK*: Apps SDK on MCP; availability rollout; monetization limited to link-outs for physical goods in the early phase; ACP (with Stripe) in beta. https://openai.com/index/introducing-apps-in-chatgpt/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^12]: OpenAI, *Developers can now submit apps to ChatGPT*: app directory and review rollout from early 2026; corroborated by VentureBeat, https://venturebeat.com/technology/openai-now-accepting-chatgpt-app-submissions-from-third-party-devs-launches . https://openai.com/index/developers-can-now-submit-apps-to-chatgpt/ (search-verified 2026-07-17)

[^13]: WildnetEdge, *GPT Store Monetization Guide* and *How Can You Monetize ChatGPT Apps? (The Reality Check)*: builder-payout program rolled out across major markets, but scarce public evidence of substantive builder revenue; digital-goods monetization not yet permitted in apps. https://www.wildnetedge.com/blogs/gpt-store-monetization-guide ; https://www.wildnetedge.com/blogs/chatgpt-app-monetization (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^14]: n8n Community, *Where can I sell my N8N workflow?* and related marketplace threads; n8nmarkets.com as the leading third-party template marketplace; ~9,400+ community templates by May 2026 per https://connectsafely.ai/articles/n8n-templates-workflow-automation-examples . https://community.n8n.io/t/where-can-i-sell-my-n8n-workflow-i-am-looking-for-marketplaces-not-the-creator-hub/212963 ; https://n8nmarkets.com/en/sell (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^15]: RapidClaw, *AI Agent Marketplaces 2026 [AgentExchange + Agentspace]*: the enterprise-vs-developer marketplace taxonomy; use for the map, verify any specific number independently. https://rapidclaw.dev/blog/ai-agent-marketplace-guide-2026 (search-verified 2026-07-17)

_last_verified: 2026-07-17_
