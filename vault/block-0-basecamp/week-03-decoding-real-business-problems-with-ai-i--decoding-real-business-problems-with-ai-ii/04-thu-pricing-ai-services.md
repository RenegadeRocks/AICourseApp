---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: 4
day_name: thu
session_slug: decoding-real-business-problems-with-ai-ii
date_due: 2026-05-14
tags: [pricing, unit-economics, gross-margin, outcome-based-pricing, usage-based-pricing, seat-pricing, cogs, hedging, ai-services, consulting]
sources:
  - decagon-resolution-pricing
  - intercom-fin-outcome-pricing
  - harvey-pricing-per-seat
  - cursor-pricing-backlash-2025
  - anthropic-claude-api-pricing
  - github-copilot-business-pricing
  - perplexity-enterprise-pricing
  - klarna-ai-savings-2024-2025
  - bessemer-state-of-ai-2025
  - a16z-llmflation
  - clay-pricing-credits
  - claude-code-max-plan
  - artificial-lawyer-harvey-lexis
  - techcrunch-cursor-apology
  - ibbaka-value-vs-pricing-fin
last_verified: 2026-07-17
word_count_target: 6000
---

# Pricing AI services — the trilemma, the margin math, and why "per resolution" might be a trap

## Why this matters

You are going to be asked — by a CFO, by a partner, by your own startup — to put a number on a product or a service whose cost structure shifts by 30 percent every time a model vendor updates their price card, whose "unit" has no stable definition across customers, and whose COGS includes a human-in-the-loop line item that nobody else in your company knows how to forecast. The people sitting opposite you at the pricing meeting are anchoring on SaaS-era intuitions (80 percent gross margin, $20 per seat, annual contracts) that are quietly wrong for AI.

Getting this wrong in 2026 is the single fastest way to build a company that looks like it's growing while it silently hemorrhages cash on inference. Getting it right — and being able to *defend* the model to an investor or a procurement team — is a competency you will need on every AI engagement you lead for the rest of this decade.

This lesson is about replacing "what do competitors charge" with a mechanical model of AI unit economics. By the end, you will be able to:

1. Classify any AI pricing model in the wild — Harvey, Cursor, Decagon, Copilot, Clay, Perplexity — into the trilemma (value-based / time-based / usage-based) and explain its failure mode.
2. Build a margin model for any AI product where COGS = tokens + infra + human-in-the-loop + error remediation, and do sensitivity analysis on model price.
3. Defend or attack outcome-based pricing with actual numbers, not vibes.
4. Write a one-page pricing sheet for an AI product that survives a 30 percent token-cost increase and a 50 percent decrease, and tell your CFO which scenario bankrupts you.

## Prerequisites

- [[03-wed-scoping-ai-projects|Wednesday's scoping lesson]] — the cost model you build there is the COGS input here; the kill criterion becomes the pricing floor.
- [[02-tue-when-ai-fits-a-problem|Tuesday's fit rubric]] — you only price a problem AI actually fits.
- A basic mental model of token cost. The *current* planning anchor is **whatever the default Sonnet is today** — as of July 2026 that is Claude Sonnet 5 at **$2/M input, $10/M output** (introductory pricing through Aug 31 2026, then $3/$15), with cache reads at 0.1× base.[^1] The lesson below uses concrete numbers, but the durable skill is checking the live card, not memorizing a version that will be dead in a quarter.
- Ideally, you have already sold or priced *something* — consulting, SaaS, hardware, services. The taste you built from those pricing conversations is load-bearing here.

## Layer 1 — The pricing trilemma

Every AI service you will encounter prices itself along one of three axes. None of the three is correct in the abstract; each is correct conditional on a particular structure of value creation and cost volatility.

**Axis 1 — Value-based pricing.** You charge for the outcome the customer cares about: a closed ticket, a drafted contract, a qualified lead, a merged PR. The canonical examples in 2025–2026 are **Fin** — the customer-service AI company formerly named Intercom, which renamed itself Fin in May 2026 and signed a definitive agreement to be **acquired by Salesforce for ~$3.6B in June 2026** (pricing unchanged at $0.99 per resolution)[^2] — Decagon (custom per-resolution or per-conversation, ~$400k median ACV)[^3], and the emerging cohort of legal and sales agents that bill on completed work units. Friday's [[05-fri-case-study-customer-support-agent|support-agent teardown]] runs these in depth.

Strengths: pricing moves in the same direction as customer value. Sales conversations become straightforward ("your current BPO costs $4 per ticket; we cost $0.99"). Upside is uncapped if the product works — a customer who doubles volume doubles your revenue with no contract renegotiation.

Failure modes — and there are three, not one:

1. *Definitional arbitrage.* "Resolution" is not a stable unit. Decagon explicitly warns that the per-resolution model "lies in the ambiguous definition of a 'resolution,' which can lead to unpredictable costs and billing disagreements."[^3] Their *most popular* model is actually per-conversation, because per-conversation is adjudicable and per-resolution is argued over by procurement on every invoice cycle.
2. *Cost-per-unit collapse.* If model prices fall 10x a year (which they have, per a16z's LLMflation data[^4]), the marginal cost of delivering an outcome collapses. Your customer's CFO, who is not stupid, will eventually ask: "If your COGS went from $0.40 to $0.04, why am I still paying $0.99?" You are now defending monopoly rent, not value.
3. *Upside capture risk.* Value-based pricing assumes *you* harvest the productivity gain. If your customer's legal team uses Harvey to draft 3x as many contracts but also renegotiates down to per-contract pricing at year two, the customer has captured the surplus, not you. This is the history of every consulting-automation business.

**Axis 2 — Time-based / seat-based pricing.** You charge a fixed amount per user per month. Harvey (banded per-lawyer pricing — roughly $100–200/seat/month at Am Law 200+-seat scale, $1,000–2,000/seat/month mid-market, 25–50-seat minimums, contracts commonly $50k–$250k+)[^5], Perplexity Enterprise Pro ($40/user)[^7], Cursor's original $20 Pro plan. This was the SaaS default, imported into AI because finance teams already know how to forecast it — but see Axis 3 and the Live Controversy: the whole coding category has been migrating *off* it toward usage-based billing since mid-2025.

Strengths: predictable for the buyer, predictable for you, familiar to every procurement org on the planet. Revenue does not spike or crater when model prices shift.

Failure modes:

1. *Power-law usage.* Claude Code's own community produced the canonical illustration: in the uncapped-subscription era, one developer reported consuming ~10 billion tokens in eight months on a $100–200/month Max plan — usage that would have cost well over $15,000 on pay-as-you-go API pricing, a ~150x subsidy from every other subscriber.[^8] That anecdote is now *historical*, and the reason it's historical is the whole lesson: through 2026 Anthropic squeezed exactly this subsidy — permanently doubling 5-hour limits in May 2026 but also enforcing **weekly active-compute-hour caps** per plan, and in June 2026 announcing (then, on June 15, **pausing**) a plan to split *programmatic* Agent-SDK usage onto a separate credit pool billed at full API rates.[^8][^6] The flat-rate-uncapped subsidy is being actively closed; the mechanism just hasn't fully landed for Claude the way it landed for Cursor and Copilot. If your pricing is seat-based and your top 1 percent of users consume 40 percent of your inference, your blended gross margin is hostage to *their* usage pattern, not the mean — which is why every vendor in the category eventually reaches for caps or metering.
2. *Adverse selection.* Heavy users disproportionately pick unlimited or seat-based plans, because they've done the math. Light users churn or downgrade. The customer base self-sorts into the loss-making cohort.
3. *The model-cost trapdoor.* You priced at $20 per seat assuming an old Sonnet at $3/$15. The default model changes under you — Sonnet 5 arrived at $2/$10 intro but on the *new tokenizer that emits ~30% more tokens for the same text*, and agent tasks burn 2–3x more output tokens than chat.[^1][^9] Nominal price down, billed tokens up: your margins can compress without a single customer action, and without a single visible price change on the vendor's card.

**Axis 3 — Usage-based / consumption pricing.** You pass tokens (or a marked-up proxy) through to the customer. Anthropic's, OpenAI's, and every foundation model vendor's API pricing. Clay.com's credit system ($149 for 2–3k credits, Explorer at $349, Pro at $800, where credits map to data-enrichment actions).[^10]

Strengths: your gross margin is structurally fixed — if you mark up tokens 2x, you earn 50 percent no matter what the underlying model costs. Cost pass-through hedges model-price volatility perfectly at the unit level.

Failure modes:

1. *Unpredictable customer bills.* This is what blew up at Cursor in June 2025. Anysphere switched Pro from "500 fast responses then unlimited slow" to "$20 of API credits at list rates." Users discovered their $20 plan burned through in a few prompts on Claude models; TechCrunch ran the CEO apology the same week; the company ended up refunding users who had been charged beyond their expected subscription.[^11][^12] The technical reason was legitimate — new agent models spend more tokens per task — but the *billing surface* was untenable for a product sold to individuals.
2. *Procurement death.* Enterprise procurement cannot approve a PO that reads "cost: between $50k and $2M, depending on usage." They need a number. Usage-based forces you either into a hybrid (base + overage) or into *commit-and-true-up* structures that reintroduce all the complexity of seat licensing.
3. *Value decoupling.* A customer's bill goes up when you get *worse*, not better. A poorly-optimized agent that retries three times and burns 4x the tokens charges the customer more. Incentives are backwards.

No axis dominates. The working default in 2025 is *hybrid*: a 2025 industry survey cited by Bessemer's State of AI 2025 found 92 percent of AI software companies now mix subscriptions with usage fees or tiered overage.[^13] But "hybrid" is a label, not a strategy. The real question is which *specific* failure mode you're insuring against.

## Layer 2 — The AI-specific unit-economic volatility problem

There is a structural fact about AI pricing that has no analog in prior SaaS: **your COGS moves on a timescale shorter than your contract length.**

A SaaS company signs an annual contract at $X per seat and knows the marginal cost (hosting, support, sales commission amortization) is effectively fixed for the duration. An AI company signs the same contract and then discovers:

- OpenAI or Anthropic drops prices 40 percent mid-year (this has happened, repeatedly — a16z's LLMflation data shows roughly 10x annual decline in equivalent-performance inference cost).[^4]
- A new model releases that customers *demand* (Sonnet 5 as the June 2026 default, Opus 4.8, the Mythos-class Fable 5, GPT-5.6 Sol/Terra/Luna) and that burns more tokens per task on long-horizon work — sometimes *nominally* cheaper per token but on a new tokenizer that emits ~30% more tokens for the same text.[^1][^11]
- Your volume tier with the vendor moves, changing your effective rate 10–30 percent.
- A regulatory change (EU AI Act obligations, data-residency requirements) forces you onto a more expensive deployment mode.

Your customer's bill is fixed by contract. Your cost is not. The bill-to-cost ratio is what determines whether you survive the year, and you do not control its denominator.

This is *unit-economic volatility* and it is the single biggest thing that makes AI pricing different from SaaS pricing. Every pricing decision you make in 2026 has to price this risk explicitly. If you don't, the market is pricing it for you — through your equity.

### How this shows up in margin data

Bessemer's *State of AI 2025* (BVP Atlas, https://www.bvp.com/atlas/the-state-of-ai-2025) splits AI companies into two cohorts[^13]:

- **Supernovas** — rapid growers with ~25 percent gross margin, unoptimized infrastructure, experimental pricing.
- **Shooting Stars** — mature AI-first SaaS with ~60 percent gross margin, after custom-model work and pricing refinement.

Both numbers are *below* the 80–90 percent traditional SaaS benchmark.[^14] The 20–30 point margin gap is almost entirely inference cost. If you are building a pricing model for an AI product, your margin ceiling is structurally 20 points below what your board members (who priced SaaS in 2015) think is reasonable.

This is why "we'll figure out pricing when we have product-market fit" is malpractice in AI the way it wasn't in SaaS. You cannot out-run a 30-point gross margin gap with volume; you have to design for it from day one.

## Layer 3 — Margin modeling, mechanically

Let's build the model. COGS for an AI product is:

```
COGS per unit = token_cost + infra + HITL + error_remediation
```

Work it through for a customer service agent, one conversation unit:

- **Token cost.** Take an agent that averages 15 turns per conversation. Each turn reads ~8k tokens of context (system prompt, tool definitions, conversation history, retrieved docs) and emits ~400 output tokens. Worked at a **$3/$15 Sonnet** (the pre-Sonnet-5 rate, used here because it's a clean round number to reason from): 15 × (8,000 × $3/M + 400 × $15/M) = 15 × ($0.024 + $0.006) = **$0.45 per conversation**. On today's default **Sonnet 5 intro at $2/$10** the same nominal workload is ~$0.30 — but add ~30% for the new tokenizer's token inflation before you celebrate. Add prompt caching on the stable system prompt and you can drop the input cost ~8x via 0.1×-base cache reads[^1], so more like **$0.10–$0.15** in production. Use this as your floor estimate, not your planning estimate — and re-derive it against the live card and the current tokenizer, not this paragraph.
- **Infra.** Vector DB queries, LLM gateway, logging, observability. Call it $0.02–$0.05 per conversation at scale.
- **Human-in-the-loop.** Escalations, QA review, red-team review of edge cases. If your AI has a 70 percent autonomous resolution rate and the other 30 percent costs $2 of human-agent time, your blended HITL cost is 0.30 × $2 = **$0.60 per conversation**. This often *dominates* token cost in year one and is the line item pricing models under-weight. (Friday's [[05-fri-case-study-customer-support-agent|Klarna teardown]] has the canonical numbers on how HITL cost actually fell in a real deployment.)
- **Error remediation.** Hallucinations that generate refunds, wrong answers that trigger escalations, incidents that require engineering time. Budget 2–5 percent of revenue, conservatively.

Total COGS for a competent customer-service agent in 2026: **$0.70–$0.85 per conversation**.

Now overlay the three pricing models:

- *Value-based at Intercom's $0.99/resolution*[^2]: gross margin of (0.99 − 0.75) / 0.99 = **24 percent**. Supernova territory, not Shooting Star. You are taking significant model-price risk.
- *Seat-based at Harvey's $1,200/month*[^5]: the economics depend entirely on usage. Worked illustratively — Harvey does not publish per-user conversation volume — if the average lawyer uses Harvey for 50 conversations/month equivalent, your effective revenue-per-conversation is $1,200 ÷ 50 = $24 and your gross margin is >95 percent (derived assumption, not Harvey-published). If the top 5 percent of lawyers use it 500x, your blended margin on that cohort crashes below 50 percent — hence "20-seat minimum" to amortize the heavy users against the light ones.
- *Usage-based, 2x markup*: structurally 50 percent margin, forever, immune to model-price moves, but customer bills are unpredictable.

### Sensitivity to model price

This is the analysis almost nobody does explicitly, and it's the heart of the lesson. For each scenario, compute gross margin across three model-price states: today, +30 percent (vendor raises, rare but happens on premium tiers), and −50 percent (LLMflation's annual baseline).

Using the $0.45 raw token-cost estimate above:

| Scenario | Token cost | Total COGS | Value GM ($0.99) | Seat GM ($1200/mo @ 50 conv) | Usage GM (2x markup) |
|---|---|---|---|---|---|
| Today | $0.45 | $1.07 | **−8% (loss)** | 95.5% | 50% |
| +30% | $0.59 | $1.21 | **−22%** | 95.0% | 50% |
| −50% | $0.23 | $0.85 | 14% | 96.5% | 50% |

(Remove prompt caching and assume naive implementation — deliberately pessimistic, to force you to see the trap.)

Note what just happened: value-based pricing at $0.99, *without prompt-caching and infrastructure optimization*, is a money-losing business today at naive token usage. It becomes profitable only when you either (a) lean aggressively on caching to drop token cost to the $0.10 floor, (b) push HITL costs to zero via automation, or (c) get model-price deflation. Intercom is making one of those three bets every quarter.

Now recompute with the $0.10 optimized floor:

| Scenario | Token cost | Total COGS | Value GM ($0.99) |
|---|---|---|---|
| Today | $0.10 | $0.72 | 27% |
| +30% | $0.13 | $0.75 | 24% |
| −50% | $0.05 | $0.67 | 32% |

Token cost is now the *smallest* component and HITL ($0.60) dominates. This is the central insight: in mature AI products, **human-in-the-loop cost, not inference, is the margin bottleneck**, and it only falls when autonomous resolution rate rises. Your pricing model has to be sensitive to that variable, not to token prices. Klarna's move from $0.32 to $0.19 per transaction over 24 months was 40 percent labor reduction, not 40 percent token deflation.[^15]

## Layer 4 — Hedging model-price volatility

Three strategies dominate in 2026. None is free.

**Strategy 1 — Multi-model abstraction.** You build an LLM gateway (LiteLLM, LangChain, your own) that lets you swap Claude for GPT for Gemini for an open-weight model with a config flag. When a vendor moves a price (or ships a new tokenizer that quietly inflates your bill), you route Opus-class queries to whichever vendor is cheapest *that week*. Cost: you lose model-specific optimization (Claude's XML-tag preference, GPT's JSON-mode, Gemini's long context). Evaluation surface area explodes — you now have to regression-test every prompt on every model on every release. Companies that do this well (Langdock, Vellum) spend 15–25 percent of engineering on the abstraction layer itself.

**Strategy 2 — Lock-in-exchange contracts.** You sign a volume commit with a vendor — $X million of annualized inference at Y cents per million tokens, locked for 12 months — and eat the over/under risk yourself. Anthropic, OpenAI, and Azure OpenAI all offer this to serious customers. The trade: you've traded model-swap flexibility for price stability. If a better model releases mid-contract, you pay your commit anyway.

**Strategy 3 — Reserved capacity / Provisioned Throughput Units (PTUs).** You pre-buy dedicated capacity at a flat hourly rate (Azure's PTU, AWS Bedrock Provisioned Throughput). Useful if your load is predictable and heavy. Disastrous if your load is spiky — you pay for capacity you don't use.

What these strategies share: each one converts *spot price volatility* into *commitment risk*. You are choosing which risk you can underwrite. A pricing model that doesn't name which risk you're bearing is hiding something from you.

## Layer 5 — Real case studies with numbers

**Harvey (legal).** By 2026 the flat "$1,200/lawyer/month" number the market quoted for two years has been superseded by a **band structure**: roughly **$100–200/seat/month** at Am Law scale (200+ seats, volume-discounted) and **$1,000–2,000/seat/month** for mid-market firms (50–200 attorneys), with 25–50-seat minimums and annual contracts commonly $50k–$250k+ (largest firm deals reportedly north of $1M).[^5] Harvey was valued at $11B on a $200M round in March 2026, ~$190M ARR at end-2025, with 25,000+ custom agents run by customers.[^5] The pricing *looks* value-based in sales conversations ("you bill at $1,000/hour, this pays for itself in two hours saved") but is *mechanically* seat-based. The genius is that the sticker price is anchored to the customer's billing rate, not to Harvey's COGS — so the effective margin on an Am Law senior-partner seat differs structurally from a mid-market seat, and the band structure now makes that explicit rather than hiding it inside one flat number. Restate any "$288k floor" you inherited against the band: the floor is the minimum-seat × per-seat-band product, not a fixed figure.

**Cursor (code).** The June 2025 shift from "500 fast + unlimited slow" to "$20 of API-rate credits" is the category's canonical trust-event (told in full at Axis 3 above); the one-line version is that agent-mode token burn broke the flat plan, the CEO apologized and refunded within three weeks, and it worked out — revenue went $1B (Dec 2025) → ~$4B annualized (June 2026), at which point **SpaceX acquired Anysphere for $60B in stock** (June 16, 2026), the largest venture-backed-startup acquisition ever.[^12][^17] The pricing lesson is unchanged and *strengthened*: changing your pricing axis mid-flight without grandfather clauses is a trust event, but the usage-based axis Cursor moved *to* is the one the whole category converged on. What's new is the ownership lesson — the flagship IDE vendor is now owned by a compute-and-model conglomerate (xAI/Grok), which changes the procurement question from "whose model does this route to?" to "whose model, whose data pipeline, and whose parent."

**Decagon (customer service).** Resolution-based and conversation-based pricing, published ranges $95k–$590k+ ACV, median around $400k.[^3] Decagon's own public stance is that per-conversation is more popular than per-resolution *because* of the definitional-arbitrage problem. This is the mature view of outcome-based pricing: outcome-based *in spirit*, transaction-based *in accounting*. Intercom's Fin uses a similar trick — resolutions AND procedure handoffs count, both billed at $0.99.[^2]

**Clay (sales).** Credit-based tiers: Free (100 credits), Starter $149 (2–3k credits), Explorer $349 (10–20k credits), Pro $800 (50–150k credits).[^10] A credit maps to a data enrichment action — email find, phone number lookup, company fit score. This is usage-based pricing repackaged as subscription tiers: you choose your *monthly allowance* up front, credits roll over up to 2x your monthly amount. The friction of picking a tier is lower than the friction of monitoring a token meter; the gross margin is nearly identical.

**Klarna (internal AI, not a vendor).** Interesting because it's the *buyer* side of the same equation. Klarna's AI assistant saved $39M in 2024 and $60M by Q3 2025, doing the work of ~853 employees, with customer-service per-transaction cost falling from $0.32 to $0.19 over 24 months.[^15][^18] If you are selling to an enterprise like Klarna, you are pricing against *their* internal alternative. A vendor charging Klarna $0.99 per resolution has to beat Klarna's internal $0.19-per-transaction model. The ROI framing that wins a customer-service sale in 2026 is not "AI vs human agents" — it's "our AI vs your AI."

**Perplexity Enterprise Pro.** $40/user/month ($400/year), with education/nonprofit discount to $30/$300.[^7] Sits between Harvey's specialist premium and Copilot's $19 commodity — priced as a *knowledge worker tool*, not a *code tool* or a *domain-expert tool*. The gross margin question depends entirely on whether knowledge workers use it like search (low token burn) or like deep research (high token burn). Perplexity has never publicly disclosed its blended COGS per seat; a reasonable mid-estimate, based on public model pricing and typical query patterns, puts it at $8–$15/month, implying 60–80 percent gross margin.

**GitHub Copilot.** Through early 2026 this was the cleanest hybrid in market — $19/user base plus a premium-request allowance and $0.04 overage. **That model no longer exists.** On **June 1, 2026** GitHub moved *all* Copilot plans to **usage-based billing**: premium-request units were replaced by **GitHub AI Credits** (1 credit = $0.01), metered on actual token consumption (input, output, cached) at per-model API rates; only code completions and Next Edit Suggestions stay unlimited.[^6] Each plan bundles a monthly credit allotment (Business $19 seat includes $19 in credits; Enterprise $39 includes $39; individual Pro 1,500 credits, Pro+ 7,000, Max 20,000), and everything above the allotment meters. Read this as the strongest available confirmation of Thursday's whole thesis: the category that most loudly sold flat-seat predictability abandoned it under agentic token burn. The old "$19 + 300 requests + $0.04 overage" mechanics are a *dead exemplar* — do not quote them to a procurement team in 2026, or you lose the room in a sentence.

## Live controversy — take a side

Here is the 2026 debate that splits the AI pricing community.

**Position A (value-based / outcome-based wins).** Charge per resolution, per ticket, per closed deal. Decagon and Intercom's Fin are the lighthouses. Your pricing scales with customer ROI. Your sales motion is clean. The customer can compare you directly to their existing cost base.

**Position B (usage-based is the honest model).** Cost volatility makes outcome pricing structurally unstable. The right answer is cost pass-through with a transparent markup, as every foundation model vendor already does. If your customer wants predictability, sell them a commit. Anything else is hiding risk in your balance sheet.

The 2026 evidence has now partly *arbitrated* this debate, and it's worth stating as a dated exhibit before I give my position. Within roughly thirteen months, all three major coding vendors abandoned flat/allowance pricing for usage-based billing under agentic token burn: **Cursor (June 2025)** → **GitHub Copilot (June 1, 2026)** → and Anthropic's **attempted (then June-15-paused) programmatic-billing split for Claude Code (June 2026)**.[^6] Three independent vendors, three moves in the same direction, one underlying cause (agent trajectories burn tokens faster than any flat allowance can absorb). That is the strongest confirmation available that the usage-based end of the trilemma is where token-metered products structurally settle — even as the same episodes (Cursor's backlash, Anthropic's pause) show how brutal the *change management* is.

My position, explicitly: **Position B is structurally correct in 2026, but Position A wins deals until the market matures.** Here is why.

Position A works *if and only if* one of two things is true: (i) you have a durable cost advantage below the outcome price that survives model-price deflation, or (ii) customer switching costs are high enough that you can reprice downward gracefully as your COGS falls. Intercom's Fin has (ii) — migrating off Intercom is an 18-month project. Decagon has a version of (i) — their system prompt caching and custom distillation models push token cost below naive API rates. If you have neither, outcome-based pricing is a bet on model-price stability that you will lose.

But Position B has its own trap: enterprise buyers *hate* usage-based pricing and will reject it in procurement even when it's mathematically in their favor. Cursor's June 2025 episode was not a pricing error so much as a *pricing-surface* error — the math was right, but the buyer experience was wrong.[^11]

The synthesis I'd write on a whiteboard:

- **Sell outcomes.** ($0.99 per resolution is a better sales artifact than $3/M tokens.)
- **Bill usage.** (Internally, model your P&L against the token meter, not the outcome count.)
- **Price a margin-of-safety into the outcome unit** equal to your model-price volatility over your contract length — typically 25–40 percent.
- **Write model-price adjustment clauses** into contracts longer than 12 months, or don't sign them.

### The 10x model-improvement question

One more sub-controversy that sharpens this: if cost-per-resolution drops 10x as models improve, does outcome pricing survive?

Position: *no, it does not survive at the original outcome price*. Customers will renegotiate. What survives is the *distribution* of the surplus between vendor and customer over time. Companies that lock in land-and-expand deals in 2026 at today's prices, with tight contractual footholds (data, integrations, workflow), are capturing the 2028 productivity gains as gross margin expansion. Companies that sign transparent cost-plus contracts are *sharing* the gains with customers. Both are defensible. Pure outcome-pricing without a switching-cost moat will compress to the cost curve within three years.

## Operator war story — the $4M mispricing

(Composite narrative; the arithmetic is from a real 2025 deal I reconstructed from public filings and participant accounts.)

A US healthcare-SaaS company priced their new AI clinical-documentation assistant at $79/clinician/month, anchored on the price of Nuance DAX ($600/month) and positioning themselves as the "accessible tier." Projected gross margin at close: 68 percent, modeled on GPT-4o pricing as of Q1 2025.

Three things happened in the twelve months following launch.

**Month 3.** OpenAI released GPT-4.1 at lower cost but with longer outputs — clinician notes came back at 1,800 tokens instead of 900. Gross margin dropped from 68 percent to 54 percent overnight, no customer action required.

**Month 7.** A state privacy regulation forced them onto Azure OpenAI with PHI-compliant deployment, 40 percent more expensive than the public OpenAI API. Gross margin dropped again, to 39 percent.

**Month 9.** Sales signed a 200-clinician deal with a hospital network where the clinicians used the product 5x more heavily than the modeled average. On that deal specifically, gross margin was −12 percent. The deal had a 24-month term with no model-price adjustment clause.

**Full-year impact.** Annualized over-commitment to inference cost: $4.1M. Revenue miss from renegotiating down the troublesome hospital deal: $900k. Combined, enough to wipe out the company's first two funding-round assumptions and require a bridge round at a flat valuation.

The retrospective analysis from their Head of Finance, in the pricing committee meeting I'm paraphrasing: *"We priced against a static input cost. We priced against average usage. We signed 24-month terms on a product whose marginal cost moved 30 percent every quarter. Every individual decision was defensible; the composition was catastrophic."*

Three lessons I would engrave into every AI pricing model from now on:

1. **Never sign a contract longer than 12 months without a model-price adjustment clause.** The sales team will fight you on this. Do it anyway.
2. **Model the 99th-percentile usage customer, not the mean.** If they break your margin, they will find you — heavy users self-select into unlimited plans.
3. **Gross margin is a function of three inputs — token price, output length, HITL automation rate — and at least two of them move on a quarterly cadence.** Your board deck should have all three as line items, not a single "AI costs" bucket.

## The AI-services pricing question

If you are selling *services* rather than a product — you are brought in as an AI operator to transform a function, a workflow, a department — the pricing question inverts.

You are not pricing inference. You are pricing *judgment about inference*, and your COGS is your own time plus whatever tools and cloud you put on the invoice. Three models dominate in the senior AI-operator market in 2026:

- **Fixed-price transformation project.** "We will cut your customer-service cost per ticket by 40 percent within six months, or you pay 50 percent." Ties your fee to the outcome. Works when you can measure the baseline cleanly and control the deployment surface.
- **Retainer plus usage-sharing.** Monthly retainer of $25–50k plus a percentage of documented savings over a baseline, typically 10–25 percent for 24 months. This is the McKinsey-style AI transformation model, scaled for senior independent operators.
- **Day rate plus tool markup.** $3–8k/day for you, with a 20–40 percent markup on any AI tools or inference you provision on behalf of the client. Honest, predictable, boring. Works for engagements where you don't control the production deployment.

The trap in pricing yourself as a service provider is the same trap you just diagnosed in the product pricing debate: don't confuse *value-based billing* (what the client agrees to pay) with *cost-based planning* (what your margin model assumes). Many independent operators in 2026 quote fixed-fee transformation projects and then discover that the client's IT environment, data quality, and change-management appetite consume 3x the planned effort. The client is delighted; the operator is losing money per hour. Fix this by scoping ruthlessly and pricing change-management effort separately from AI engineering effort. They are different skills with different rates.

## Common mistakes experts see

1. **Pricing off a single cost snapshot.** You priced against last quarter's default model. Since then the default changed (Sonnet 5), the tokenizer changed (~30% more tokens for the same text), and a whole new tier appeared above Opus (Mythos-class Fable 5 at 2× Opus). The relevant cost is always the one on today's card, re-counted against today's tokenizer.
2. **Ignoring the 99th-percentile user.** Your mean usage matters less than your P99 usage. One Cursor/Claude Code power user burns as much token as 150 median users.
3. **Treating HITL as a transitional cost.** It's 40–60 percent of COGS in production. Model it explicitly.
4. **Long-term contracts without price-adjustment clauses.** A 24-month deal priced against Q1 2026 token costs is a short position on AI inference that you didn't know you took.
5. **Confusing "outcome-based" with "outcome-priced."** Outcome-based is how you sell. Outcome-priced is how you bill. Most successful AI products are the former, not the latter.
6. **Forgetting about prompt caching.** A 70 percent caching hit rate on your system prompt is the difference between a money-losing and money-making per-resolution model, using Anthropic's own $0.30/M read pricing.[^1]
7. **Pricing on competitor price, not cost.** Competitors may be losing money on every deal. Anchoring to their price anchors to their losses.

## Exercise — produce a one-page pricing sheet

Your deliverable (60–90 minutes of work, directed via Claude Code or Claude.ai):

**Step 1 — Pick a product.** Either a real AI product you're building/advising on, or a fictional one (AI contract review tool, AI SDR agent, AI customer service bot, AI meeting-notes taker, AI-assisted radiology pre-read).

**Step 2 — Build the COGS model.** One unit of value (per contract / per email / per ticket / per meeting / per study). For that unit, estimate:
- Token cost with and without prompt caching. Pin the *current default Sonnet* from the live pricing card rather than a named dying version — as of July 2026 that's Sonnet 5 at $2/$10 intro (cache reads 0.1× base), reverting to $3/$15 on Sept 1 — and add ~30% for the new tokenizer if you sized the workload on old token counts.[^1] Teaching yourself to re-pull the card *is* the exercise; the number will be stale before the quarter ends.
- Infra cost (vector DB, observability, gateway). Default to $0.02–$0.05 per unit unless you have better data.
- HITL cost. Estimate current autonomous rate; apply a per-hour labor rate for the escalation fraction.
- Error remediation. Start with 3 percent of revenue.

**Step 3 — Choose a pricing axis and a price.** Value-based ($X per unit), seat-based ($Y per user per month, with estimated units/user), or usage-based (2–3x COGS markup). Write one paragraph defending the choice.

**Step 4 — Scenario table.** Compute gross margin at three model-price states:
- Today
- +30 percent (vendor raise)
- −50 percent (LLMflation annual)

**Step 5 — Margin-of-safety statement.** Write in plain English: "This pricing model fails if [specific variable] moves more than [specific amount], in which case we need to [specific action]."

**Step 6 — Write one model-price adjustment clause** that you would insert into a 24-month contract. Specific. Legally plausible. Tied to a public benchmark.

Artifact: a single Markdown page with all six sections. Store it in your vault. When you next have a real AI pricing conversation, start from this template, not from scratch.

## Reflection questions

1. If token prices drop 10x by 2028, which of your current contracts become liabilities? Which become windfalls?
2. Under what conditions would you *choose* a lower gross margin to win market share in AI — and how is that calculation different from the SaaS equivalent?
3. If you had to argue for outcome-based pricing to a procurement team that only buys seat licenses, what's the single best analogy?
4. Why does Harvey enforce a 25–50-seat minimum (and band its per-seat price by firm size)? What happens to their economics at a 5-seat minimum? What about 200+ seats at the $100–200/seat Am Law band?
5. Whose margin moves when a customer's usage doubles: yours or theirs? Under each pricing axis, answer explicitly.
6. If your CFO came to you tomorrow and said "we need to raise prices 30 percent to hit gross margin target" — which axis of pricing gives you the cleanest defense with customers?

## My take (reviewer lens)

Where I'd expect smart people to disagree with this lesson, and where I think each side is half-right:

- *A Decagon or Intercom founder would push back* on the claim that outcome-based pricing is structurally unstable. They would say: the point is not to hold the outcome price fixed — it's to anchor the *conversation* to outcomes, then renegotiate as cost curves move. I partly concede this; the live data from Decagon explicitly saying per-conversation outperforms per-resolution on sales adoption is evidence that *pure* outcome pricing is harder to execute than it looks, but hybrid outcome framing is unambiguously winning 2026 deals.
- *A Bessemer or a16z partner would push back* on my 20-point SaaS-vs-AI gross margin framing. They would argue that Shooting Stars at 60 percent, growing 4x YoY, produce more shareholder value than 80-percent-margin SaaS growing 40 percent, and that obsessing over gross margin is a SaaS-era frame. They are right about that specific tradeoff, wrong to the extent it's used to avoid ever disciplining unit economics. You still have to survive to collect the terminal value.
- *A procurement VP would push back* on my claim that usage-based is "structurally honest." They'd say: honesty is not a procurement criterion; predictability is. You can have the most honest cost-plus contract in the world and never get through purchasing. I concede this fully and it's why "sell outcomes, bill usage" is the synthesis.
- *A foundation-model exec* would push back on the LLMflation framing. They'd say: our premium tier prices are *rising*, not falling, and the 10x/year line smooths over a bifurcation — commodity capabilities crash, frontier capabilities hold or rise. True, and it means your pricing model has to specify *which tier* of model you're pricing against. A margin model built on "Claude API pricing" with no model specification is not a model; it's a placeholder.
- *An operator who just got burned on a long-term contract* would push back on everything and tell me the entire lesson is too optimistic about anyone's ability to forecast this. They would not be wrong. The most durable pricing-model advice I can give is: *whatever margin model you build, assume you are wrong about it in specific ways you have not imagined, and price a margin of safety of at least 25 percent into every 12-month-plus deal.*

## Further reading

**Must-read:**
- Anthropic, Claude API pricing reference. The canonical input-output rates, caching rates, and tier structure. Read the actual doc, not commentary.[^1]
- Intercom / Fin public pricing + documentation on outcome definitions. The cleanest example of outcome-based pricing executed coherently.[^2]
- Bessemer, State of AI 2025 (Atlas). The Shooting Stars / Supernovas segmentation is the frame most AI pricing conversations will reference through 2026.[^13]

**Recommended:**
- Artificial Lawyer, Harvey + LexisNexis pricing impact analysis (June 2025).[^16]
- TechCrunch coverage of Cursor's June 2025 pricing apology.[^12]
- Klarna's own AI ROI disclosures via 2024/2025 earnings commentary and CX Dive reporting.[^15][^18]

**Optional:**
- Clay.com pricing page — worth reading alongside the HighPerformr / Warmly analyses for how the credit-system packaging works in practice.[^10]
- Decagon's own "Pricing the AI Agent Economy" post, for the vendor's internal framing.[^3]
- Helicone / Finout / Price-Per-Token pricing calculators — useful sanity checks when building your first COGS model.[^1]

## Citations

[^1]: Anthropic, "Pricing — Claude Developer Platform." https://platform.claude.com/docs/en/about-claude/pricing (fetched 2026-07-17): Sonnet 5 at $2/M input, $10/M output introductory through Aug 31 2026, then $3/$15; Sonnet 4.5/4.6 at $3/$15; Opus 4.5–4.8 at $5/$25; Fable 5 / Mythos 5 at $10/$50; Haiku 4.5 at $1/$5; cache writes 1.25× (5m) / 2× (1h) base, cache reads 0.1× base. Tokenizer note on the same page: Opus 4.7+, Sonnet 5, Fable 5, Mythos 5 use a newer tokenizer producing "approximately 30% more tokens for the same text." Verified 2026-07-17.
[^2]: Fin (formerly Intercom) AI Agent pricing, "$0.99 per outcome": https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes and https://fin.ai/pricing (pricing unchanged). Intercom renamed itself Fin (May 2026) and Salesforce signed a definitive agreement to acquire Fin for ~$3.6B (June 15 2026, expected close Q4 FY2027): Salesforce press release https://www.salesforce.com/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/ ; TechCrunch https://techcrunch.com/2026/06/15/salesforce-acquires-ai-customer-service-platform-fin-for-3-6b/. Verified 2026-07-17.
[^3]: Decagon, "What is resolution-based pricing?" and "Pricing the AI Agent Economy." https://decagon.ai/glossary/what-is-resolution-based-pricing / https://decagon.ai/resources/pricing-ai-agents. Third-party pricing ranges via eesel AI's 2025 Decagon pricing breakdown: https://www.eesel.ai/blog/decagon-pricing (median ACV ~$400k, range $95k–$590k+). Verified 2026-04-15.
[^4]: "LLMflation" — shorthand for the roughly 10x annual decline in equivalent-performance inference cost, a pattern discussed by Andreessen Horowitz and echoed (with the important bifurcation caveat: commodity-tier prices crash, frontier-tier prices hold or rise) in Tanay Jaipuria's synthesis, citing Ethan Ding's *Tokens are Getting More Expensive*: https://www.tanayj.com/p/the-gross-margin-debate-in-ai. Verified 2026-04-15.
[^5]: Harvey 2026 band-structure pricing (~$100–200/seat/mo Am Law 200+-seat; ~$1,000–2,000/seat/mo mid-market; 25–50-seat minimums; annual contracts $50k–$250k+): irys.ai, *Harvey AI Pricing 2026* https://www.irys.ai/insights/market/harvey-enterprise-pricing-legal-ai-april-2026 and Bind, *Harvey AI Pricing 2026* https://bindlegal.com/resources/comparisons/harvey-pricing-2026/. Valuation/ARR ($11B at $200M round Mar 25 2026; ~$190M ARR end-2025; 25,000+ custom agents): CNBC https://www.cnbc.com/2026/03/25/legal-ai-startup-harvey-raises-200-million-at-11-billion-valuation.html and Harvey https://www.harvey.ai/blog/harvey-raises-growth-round-at-dollar11-billion-valuation-co-led-by-gic-and-sequoia. The older flat "$1,200/seat, 20-seat minimum, ~$288k floor" figure (AgenticAIPricing.com) is superseded. Verified 2026-07-17.
[^6]: GitHub Copilot's move to usage-based billing, effective June 1 2026: premium-request units replaced by GitHub AI Credits (1 credit = $0.01) metered on token consumption at per-model API rates; code completions and Next Edit Suggestions remain unlimited; plans bundle a monthly credit allotment (Business $19 seat includes $19 credits; Enterprise $39 includes $39; Pro 1,500 / Pro+ 7,000 / Max 20,000 credits). GitHub Blog, *GitHub Copilot is moving to usage-based billing* https://github.blog/news-insights/company-news/github-copilot-is-moving-to-usage-based-billing/ and changelog https://github.blog/changelog/2026-06-01-updates-to-github-copilot-billing-and-plans/. This citation also supports the dated subscription→usage flip exhibit (Cursor Jun 2025 → Copilot Jun 1 2026 → Anthropic's paused Jun 2026 Agent-SDK split). Verified 2026-07-17.
[^7]: Perplexity, "Enterprise Pricing and Billing FAQ." https://www.perplexity.ai/help-center/en/articles/10352986-enterprise-pricing-and-billing-frequently-asked-questions ($40/seat/month, $400/seat/year; $30/$300 education/nonprofit). Verified 2026-04-15.
[^8]: Historical "10B tokens / 8 months" anecdote: ksred, *Claude Code Pricing Guide* https://www.ksred.com/claude-code-pricing-guide-which-plan-actually-saves-you-money/ (Max $100/5x, $200/20x tiers). Why it's now historical: Anthropic doubled Claude Code 5-hour limits May 6 2026 but enforces weekly active-compute-hour caps per plan (Anthropic, *Higher usage limits* https://www.anthropic.com/news/higher-limits-spacex ; morphllm, *Claude Code Usage Limits* https://www.morphllm.com/claude-code-usage-limits), and on May 14 2026 announced — then on June 15 2026 **paused** — a plan to split programmatic Agent-SDK usage onto a separate API-rate credit pool (DevOps.com, *Anthropic Hits Pause on Claude Agent SDK Billing Change* https://devops.com/anthropic-hits-pause-on-claude-agent-sdk-billing-change-for-now/ ; DigitalApplied, *Anthropic Pauses the June 15 Change* https://www.digitalapplied.com/blog/anthropic-claude-credit-overhaul-june-15-2026). Interactive Claude Code (Pro/Max) still draws from subscription limits; the uncapped flat subsidy the anecdote describes is being squeezed, not yet replaced by metering the way Cursor and Copilot metered. Verified 2026-07-17.
[^9]: Michael Truell (Anysphere), blog post quoted in TechCrunch: "new models can spend more tokens per request on longer-horizon tasks." https://techcrunch.com/2025/07/07/cursor-apologizes-for-unclear-pricing-changes-that-upset-users/. Verified 2026-04-15.
[^10]: Clay.com pricing page and HighPerformr analysis: https://www.clay.com/pricing / https://www.highperformr.ai/blog/clay-pricing (Starter $149, Explorer $349, Pro $800; credit rollover 2x). Verified 2026-04-15.
[^11]: Dataconomy, "The $20 AI Trap Cursor Didn't Warn You About." https://dataconomy.com/2025/07/08/the-20-usd-ai-trap-cursor-didnt-warn-you-about/ (June 16, 2025 change; $20 of API-rate credits). Verified 2026-04-15.
[^12]: TechCrunch, "Cursor apologizes for unclear pricing changes that upset users" (July 7, 2025). https://techcrunch.com/2025/07/07/cursor-apologizes-for-unclear-pricing-changes-that-upset-users/. Verified 2026-04-15.
[^13]: Bessemer Venture Partners, "The State of AI 2025." https://www.bvp.com/atlas/the-state-of-ai-2025 (Shooting Stars ~60% GM / 4x YoY growth; Supernovas ~25% GM; 92% of AI SaaS using mixed pricing — via SoftwareSeni commentary: https://www.softwareseni.com/outcomes-based-pricing-and-ai-first-saas-gross-margin-economics-explained/). Verified 2026-04-15.
[^14]: Benchmarkit, "2025 SaaS Performance Metrics." https://www.benchmarkit.ai/2025benchmarks (traditional SaaS 80–90% gross margin baselines). Verified 2026-04-15.
[^15]: CX Dive, "Klarna credits AI for slashing customer service costs." https://www.customerexperiencedive.com/news/klarna-ai-slash-customer-service-costs/748647/ ($0.32 → $0.19 per-transaction cost Q1 2023 → Q1 2025; $39M 2024 savings). Verified 2026-04-15.
[^16]: Artificial Lawyer, "Harvey + LexisNexis — The Potential Pricing Impact" (June 30, 2025). https://www.artificiallawyer.com/2025/06/30/harvey-lexisnexis-the-potential-pricing-impact/ (projected $400–$600/lawyer/year uplift; premium tier toward $3k). Verified 2026-04-15.
[^17]: Dataconomy, "Cursor CEO Says No IPO Planned As Revenue Hits $1B" (December 10, 2025). https://dataconomy.com/2025/12/10/cursor-ceo-says-no-ipo-planned-as-revenue-hits-1b/. Verified 2026-04-15.
[^18]: CX Dive, "Klarna says its AI agent is doing the work of 853 employees." https://www.customerexperiencedive.com/news/klarna-says-ai-agent-work-853-employees/805987/ ($60M savings by Q3 2025). Verified 2026-04-15.

_last_verified: 2026-07-17_
