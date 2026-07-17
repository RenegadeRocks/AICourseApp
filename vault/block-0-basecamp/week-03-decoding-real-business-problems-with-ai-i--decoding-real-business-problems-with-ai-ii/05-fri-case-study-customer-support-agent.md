---
type: lesson
block: block-0-basecamp
week: week-03
day_of_cycle: 5
day_name: fri
session_slug: decoding-real-business-problems-with-ai-ii
date_due: 2026-05-15
tags: [case-study, customer-support, ai-agents, klarna, intercom-fin, decagon, sierra, ada, forethought, unit-economics, deflection, resolution-rate, outcome-based-pricing, teardown]
sources:
  - openai-klarna-case-study-2024
  - klarna-ai-press-release-feb-2024
  - pragmatic-engineer-klarna-chatbot
  - bloomberg-klarna-hires-humans-may-2025
  - fortune-klarna-ai-humans-return-may-2025
  - techcrunch-klarna-vip-humans-jun-2025
  - cnbc-klarna-ai-workforce-40-percent
  - intercom-fin-pricing-resolution-page
  - intercom-fin-outcomes-help
  - ibbaka-intercom-fin-value-pricing
  - decagon-stripe-case-study
  - decagon-series-c-131m-2025
  - sierra-cnbc-4-5b-valuation-2024
  - sierra-techcrunch-10b-valuation-sep-2025
  - sierra-techcrunch-100m-arr-nov-2025
  - taylor-cheeky-pint-outcome-pricing
  - bvp-ada-cx-loops
  - fini-deflection-rate-trust
  - ada-containment-rate-alarm
  - a16z-outcome-pricing-dec-2024
  - teneo-ai-vs-live-agent-cost-2025
  - gartner-ai-cost-exceed-human-2030
  - cx-dive-klarna-reinvest-human
  - morgan-lewis-ai-healthcare-enforcement-2025
last_verified: 2026-07-17
word_count_target: 6000
---

# Case study teardown — customer support AI agents (Klarna, Intercom Fin, Decagon, Sierra): numbers, unit economics, where they break

## Why this matters

Support is the category where AI agents first met the P&L. Every vendor pitch that crosses your desk this year — whether it's a legal agent, a revenue-ops agent, an internal-IT agent — is retelling the customer-support story with the serial numbers filed off. "Deflection rate" becomes "automation rate." "Cost per resolution" becomes "cost per task." "$0.99 outcome-based pricing" becomes whatever you're willing to pay per draft contract, per reconciled invoice, per triaged ticket.

So if you are an AI-catalyst lead, treat the support category as the reference implementation for every other agent category you will evaluate. The vendors in it have been shipping to production for two years. They have posted real numbers, eaten real walk-backs, and pivoted real pricing models. You can read their pitch decks, their case studies, their Trustpilot reviews, and the CFO's earnings transcripts side by side. Nowhere else in enterprise AI do you get that density of ground truth.

This lesson is a teardown. By the end of it you will:

1. Know the architectural difference between Klarna's OpenAI-on-Zendesk approach, Intercom Fin's vertically integrated play, Decagon's enterprise orchestration layer, and Sierra's outcome-priced platform — and be able to explain why each one's business model follows from its architecture, not the other way around.
2. Have the numbers. Klarna's headline claims, Klarna's walk-back, Intercom's guaranteed-or-refund resolution math, Sierra's valuation-to-ARR multiple, Decagon's 60-80% deflection in shipped deployments, the $0.50 vs $6.00 per-interaction cost range, and Gartner's projection that GenAI cost per resolution could cross human offshore rates by 2030.
3. Be able to run a one-page teardown on any support-agent vendor in under 60 minutes, using a rubric tight enough that you could present it in a Monday procurement meeting without getting killed by an honest CFO.

This is the pattern you will reuse for every other AI vendor category you evaluate for the next three years. Support is just where the data is best.

## Prerequisites

- [[03-wed-scoping-ai-projects|Wednesday's scoping lesson]] and [[04-thu-pricing-ai-services|Thursday's pricing trilemma]] — this teardown runs the pipeline they built.
- A rough sense of how RAG and tool-use agents are architected (we covered this in [[../week-02-decoding-real-business-problems-with-ai-i--basecamp-part-3-agents-and-apis/01-mon-agent-architectures|Week 2 Monday]]).
- You do not need to have shipped a support bot yourself. You do need to have looked at a Zendesk or Intercom dashboard at some point in your career.

## The category map (why the architectures diverge)

Before the numbers, one piece of orientation. The public press treats "AI customer support" as one category with one benchmark. It is not. There are at least four distinct shapes the product can take, and a vendor's architecture predicts their pricing, their deflection ceiling, and where they will break.

**Shape 1 — Bring-your-own-LLM, bolted onto the existing helpdesk.** This is the Klarna pattern. Klarna did not buy a support-agent platform. They partnered with OpenAI, wrapped GPT-4 in a Zendesk integration, and deployed it behind their existing chat widget.[^1] The product is essentially: GPT + their knowledge base + their API (for refund lookups, order status, payment-plan changes) + their brand voice prompt. Fast to ship, lowest vendor margin to pay, highest in-house engineering load, and you own the entire eval problem.

**Shape 2 — Vertically integrated helpdesk + AI layer.** This is Fin — the company that *was* Intercom.[^8] Intercom already owned the messaging widget, the inbox, the help-center CMS, the workflow builder, and sold Fin as the AI layer sitting naturally on top of that stack; the pitch is that if your content is already in the help center and your routing rules already in the workflow engine, Fin will "just work" at 50–60% resolution with a few days of config, at $0.99 per resolution on top of the per-seat helpdesk fee.[^8][^9] Two 2026 developments reshape this shape: Intercom **renamed itself Fin** (May 2026) after its agent, and **Salesforce signed a definitive agreement to acquire Fin for ~$3.6B** (June 15, 2026, expected to close in Q4 of Salesforce's FY2027).[^25] The vertically-integrated-independent is being absorbed into a CRM platform's Agentforce stack — the single biggest support-agent consolidation event since this lesson was first written, and a live example of the week's "own the model, own the distribution, or get acquired" thesis.

**Shape 3 — Enterprise orchestration layer on top of whatever you already have.** This is Decagon.[^11] You keep Zendesk, Salesforce, Gladly, whatever. Decagon sits above, does the reasoning, calls your APIs, escalates when it can't. The selling point is "we are not a helpdesk, we are the brain." Pricing is custom enterprise contract with a reported $50K platform fee floor and roughly $0.99/conversation above that.[^11] Duolingo deflecting 80% of volume and Chime reducing contact-center opex by >60% are the poster-child numbers.[^11]

**Shape 4 — Outcome-priced platform with voice.** This is Sierra.[^13][^14] Bret Taylor's pitch, in one sentence: we price you per successfully resolved interaction, we escalate to humans for free, and we build the "agent" (their word for your AI support persona) as a product with a personality and SLAs, not as a chatbot.[^16] Sierra is where voice-native support is moving — ADT home security, Sonos Wi-Fi troubleshooting — because voice is where incumbents' old IVR stacks are weakest and where outcome-based pricing is easiest to measure.[^16]

**Shapes 5 and 6, for completeness.** Ada is the pre-LLM conversational-AI incumbent that rebuilt on top of a "Reasoning Engine" with multi-model orchestration and Playbook SOPs.[^17] Forethought is the multi-agent-collaboration pitch — several specialized agents cooperating on one ticket.[^17] Both are credible, both have reference logos, but neither has the headline 2024-2026 story that Klarna, Intercom, Decagon, or Sierra have, so we will touch them lightly.

The punchline: when a support-agent vendor shows you a deflection number, your first question is *"which shape are you?"* — because the deflection number means something different in each one. Klarna's 66% "handled" conversations included any chat the bot ever responded in. Intercom's 50–60% resolution is measured specifically as "conversation ends without human handoff and customer doesn't return within N hours on the same topic." Decagon's 80% for Duolingo is counted against incoming volume, which is not the same denominator. Sierra's outcome is only counted when the customer's stated intent is satisfied. Four different numerators, four different denominators, and vendors know this.

## Klarna: the headline numbers and the walk-back

Klarna is the most-studied support-agent deployment in the world, so let's put the full timeline on the table.

### February 2024 — the announcement

One month after global rollout, Klarna and OpenAI published the numbers that every AI slide deck of 2024 would copy:[^1][^2]

- **2.3 million conversations** handled in the first month
- **Two-thirds of Klarna's total customer service chat volume**
- **Equivalent to 700 full-time agents** in workload
- **CSAT parity** with human agents
- **25% drop in repeat inquiries** (Klarna's preferred proxy for resolution quality)
- Customer time-to-resolution fell from **~11 minutes to under 2 minutes**
- **24/7, 23 markets, 35+ languages**
- **$40M USD in projected 2024 profit improvement**

These are the numbers. They are real; Klarna's own Feb 2024 press release (https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/) is the primary source for the two-thirds / 700-FTE / $40M projection, and OpenAI's case study corroborates.[^1][^2] The "700 FTE" figure is not a headcount claim — it is a workload-equivalent — and Klarna had, in fact, laid off roughly 700 people in 2022 as a cost-cutting move unrelated to the bot launch two years later, which caused a large chunk of the internet to conflate two separate events.[^3]

The Pragmatic Engineer's April 2024 teardown was the first widely read skeptical read.[^3] Gergely Orosz's main observation: Klarna's bot is excellent at the high-volume, FAQ-shaped head of the distribution — "when is my refund?", "change my payment plan", "where is my order?" — which is exactly the long tail of L1 repetitive questions. It is not clear from the headline numbers how the bot handles the mid-tail (weird edge cases) or the tail (regulatory, fraud, hardship). The 25% drop in repeat inquiries is the most interesting number on the sheet because it is the only one that suggests quality, not throughput. But Klarna never published what fraction of conversations were "complex" by their internal taxonomy, and the CSAT-parity claim was on the combined pool, not on complexity-matched samples.

### May 2025 — the walk-back

Fourteen months later, Sebastian Siemiatkowski told Bloomberg that Klarna was **hiring human customer service agents again**, explicitly because over-reliance on AI had produced *"lower quality"* output.[^4][^5] The same CEO who had said "AI can perform all human jobs" now said:

> "From a brand perspective, a company perspective, I just think it's so critical that you are clear to your customer that there will always be a human if you want."[^4]

The new hiring model is telling. Klarna is piloting an "Uber-like" setup — remote workers in Sweden, choosing their own hours, paid starting at 400 SEK (~$41) per shift — recruiting students, rural populations, and passionate Klarna users.[^4] This is not a rollback to the pre-AI call center. It is a **hybrid architecture** in which the AI handles the head, humans handle the tail, and humans can be summoned on demand ("press 9 for a human") as a brand promise.

By June 2025, Siemiatkowski clarified the humans would be positioned as **VIP support** — a premium path, not a fallback.[^6] And by the time of Klarna's September 2025 US IPO (priced $40/share, $1.37B raised) and first post-IPO earnings (Q4 2025 revenue $1.082B, FY2025 $3.5B up 25%)[^7], the official narrative was that AI had helped Klarna shrink its workforce by 40% over three years, and that the human re-hiring was about premium service, not AI failure.[^7]

### The controversy: failure or maturity pivot?

Here is the live argument in the industry, and you should be able to hold both sides.

**Position A — AI fell short of hype.** Klarna's walk-back is prima facie evidence that pure-AI support does not work at scale, even when the vendor is OpenAI and the customer is a well-funded fintech with high-quality first-party data. Customer complaints rose. CSAT degradation on complex cases was hidden inside aggregate parity numbers. The "$40M profit improvement" claim was never independently audited. The repeat-inquiry metric Klarna chose was the most flattering one available; resolution-quality metrics that actually measure whether the customer's problem was solved (versus the bot ending the conversation) were never published. By this read, Klarna got caught in a hype cycle and had to quietly rebuild human capacity once churn and regulatory complaints started showing up. Fortune's May 2025 coverage framed it this way and cited a MIT/BCG survey finding that **most enterprise AI projects fail to deliver ROI**.[^5]

**Position B — hybrid was always the right endpoint; pure-AI was the learning phase.** On this read, Klarna ran the experiment precisely because no one else in fintech would. They found the deflection ceiling empirically (~66% of volume, dropping in complex segments). They learned which intents their bot could own cleanly and which it could not. They now have the best hybrid support stack in consumer fintech because they did the work in public. The fact that Siemiatkowski is now bringing humans back does not invalidate the $40M 2024 gain — it compounds it with a quality layer the market will pay more for. The correct endpoint for consumer support was always AI + human escalation + human-as-brand-promise; Klarna just got there first, publicly. Bret Taylor's outcome-based pricing model at Sierra explicitly builds in this shape — "when AI resolves, we charge; when human has to, it's free."[^16] If Sierra is right, Klarna's architecture post-2025 is what every consumer brand will look like in 2028.

**My take:** Position B is mostly right on the architecture question and mostly wrong on the narrative question. The hybrid endpoint was obvious to anyone who had shipped a support bot before 2022; Klarna's architects absolutely knew this going in. What happened between 2024 and 2025 was not a technical failure — it was a **communications and expectation-setting failure**. Siemiatkowski's "AI can perform all human jobs" framing, and the conflation of the 2022 layoffs with the 2024 bot launch, created a narrative the product could not back up at the promised quality. The walk-back was mostly a narrative walk-back. But the tail quality issue was real, and it is a leading indicator for every support-agent vendor that quotes you a deflection rate over 60%: the last 10 percentage points of that rate are where your brand lives.

## Intercom Fin: resolution-rate economics and the metric problem

Intercom Fin is the cleanest public pricing model in the category, which is why it is the easiest to reason about.[^8]

**The pricing mechanic.** Fin charges $0.99 per "resolution" — a resolution is counted when Fin responds to a customer question and the conversation ends without the customer reopening it or being escalated to a human within a defined window (typically 24 hours). Intercom's pages quote a claimed ~60% resolution rate across their customer base, and Intercom offers a **50% guaranteed resolution rate** — if Fin resolves fewer than 50% of conversations it touches in a period, Intercom credits back resolution fees for the shortfall.[^8][^9]

**The unit-economics math, honestly.** If your fully-loaded human agent handles ~$6 per interaction (a common North American figure for an in-house L1 agent, fully loaded with management, QA, tooling, training, benefits, real estate)[^21], and Fin resolves at $0.99 per resolution, the naive savings look like this:

Assume 10,000 monthly support conversations. Pre-AI: 10,000 × $6 = $60,000/mo. With Fin at 60% resolution: 6,000 × $0.99 (Fin) + 4,000 × $6 (escalated to humans) = $5,940 + $24,000 = $29,940/mo. Naive savings: ~50%.

But three costs do not appear in the vendor deck:

1. **Humans handling escalations are handling the harder tickets.** AHT on escalated tickets goes up, not down, because the bot has already absorbed the easy ones. Your $6 figure might become $9. Our savings drop from 50% to ~40%.
2. **Knowledge-base curation is not free.** Fin's resolution rate is a function of how well your help center is written, tagged, and kept current. Real shipped deployments report 0.5–2 FTEs of ongoing content operations per team of 20 human agents. Call it $6-8k/mo for a mid-sized deployment.
3. **Ongoing eval labor.** Someone has to read the transcripts, label resolutions as actually-resolved vs bot-terminated-the-conversation, and feed corrections back. Another 0.3–0.5 FTE.

Add those back and the first-year real savings on a 10K-volume account are typically in the 20–35% range, not 50%. That is still an attractive ROI, but it is "good enterprise-software deal," not "replaces your call center."

**The metric controversy.** Resolution rate is a politically convenient number because it is measurable by the vendor — they know when their bot responded and the conversation closed. It is not the same thing as whether the customer's problem was solved. Fini Labs and Ada have both publicly argued that deflection and containment rates **punish** good AI and reward bad AI, because a bot that terminates a conversation with "I'm sorry I can't help with that, is there anything else?" and the frustrated customer gives up gets counted as a successful resolution.[^18][^19] Ada specifically ran a "sounding the alarm on containment rate" piece arguing the industry needs new metrics.[^19]

**Practical fix:** if you are an AI-catalyst lead evaluating Intercom or any resolution-priced vendor, insist on three additional numbers in the contract: (a) **customer-return-within-7-days rate** on "resolved" conversations; (b) **post-resolution CSAT** on AI-resolved conversations specifically, separated from blended numbers; (c) **escalation-request rate**, measuring how often customers ask for a human mid-conversation even if they don't get one. If the vendor won't share (a), (b), or (c), you are paying for a metric the vendor controls the definition of.

## Decagon: enterprise positioning, and what 80% deflection actually looks like

Decagon's pitch is the opposite of Intercom Fin's: instead of "come into our helpdesk," it is "keep your stack, we are the orchestration brain."[^11] This is a more expensive, slower, higher-touch sell, and the logo list reflects it — Duolingo, Chime, Hertz, Notion, Rippling, Eventbrite, Substack, Riot Games, with Stripe as a reference integration partner.[^11][^12] Decagon's funding tells its own consolidation story: $131M at $1.5B (June 2025), then a **$250M Series D at $4.5B — a valuation triple in six months — in January 2026**, $481M raised in total, on 100+ enterprise customers signed in 2025.[^12] The category isn't just consolidating by acquisition (Fin→Salesforce); the independents that stay independent are raising at multi-billion valuations to do it.

**The shipped numbers:**
- **Duolingo: 80% deflection** of incoming support volume.[^11] This is the highest published deflection I have seen from a real enterprise deployment, and it is context-dependent — Duolingo's support is heavily long-tail-but-repeatable (language questions, subscription management, streak recovery) and they have an unusually engaged audience willing to self-serve.
- **Chime: 70% resolution across chat and voice; 60%+ reduction in contact-center operating costs; net promoter score roughly doubled.**[^11] Chime is interesting because it is a **regulated fintech**, and the deflection number being this high while NPS went up means either (a) Chime's implementation is genuinely best-in-class, or (b) the deflection denominator excludes regulated-domain tickets (fraud, disputes, KYC) that still route to humans. Almost certainly (b), and that is the right architecture.
- **Stripe API integration case: 167% increase in deflection for a subscription-based business; 65% cost reduction for another.**[^12]

**The pricing.** Decagon does not publish; industry reporting and procurement data suggest a $50K annual platform floor plus approximately $0.99/conversation with volume discounts.[^11][^decagon-pricing] That is structurally similar to Fin's $0.99/resolution but with a different denominator (conversation, not resolution) and a floor that keeps smaller customers out. This is classic enterprise gating.

**Where Decagon breaks:** the same places every orchestration-layer vendor breaks. (1) **CRM integration time** — the vendor deck says "2 weeks to go live," the reality is 8–16 weeks when you count data cleanup and API edge cases. (2) **Knowledge-base quality** — orchestration can't save bad content. (3) **Regulated-domain carve-outs** — the 80% number always has a footnote about which intents are excluded. (4) **Non-English quality cliff** — Decagon, like most US-built agents, performs best in English; Spanish, Portuguese, Japanese, and Arabic CSAT usually drops 5–15 points at parity deflection. This last one matters disproportionately for Hertz and other travel/hospitality deployments and rarely shows up in a published case study.

## Sierra: outcome-based pricing and the voice play

Sierra is the most ambitious architectural bet in the category. Bret Taylor — ex-Google Maps founder, ex-Facebook CTO, ex-Salesforce co-CEO, current OpenAI board chair — launched Sierra in late 2023. By October 2024 Sierra raised $175M at a $4.5B valuation.[^13] By September 2025 they had raised $350M at a $10B valuation, then in **May 2026 a $950M Series E at a $15.8B valuation** (led by Tiger Global and Google's GV).[^14] Revenue moved too: past **$150M ARR in eight quarters**, with ~$200M reported in 2026.[^15] Run the multiple honestly — at $15.8B on ~$200M ARR that's ~**79x** and falling as ARR compounds, down from the ~100x the earlier round implied. Still indefensible by any normal SaaS benchmark, and still defensible only if you believe they are building something categorically different.

**What's different architecturally:**

1. **Outcome-based pricing.** Sierra charges when the agent successfully resolves a customer's stated intent; escalation to a human is **free**.[^16] This is the most customer-aligned pricing in the category and the hardest to fake, because "resolution" is measured against the customer's own stated intent at the start of the conversation. It also means Sierra's revenue is a direct function of their model quality — a rare alignment.
2. **Agents as products, not features.** Sierra's sales motion is to help a customer design their agent — give it a name, personality, escalation policy, brand voice — as if hiring a product manager for a new product line. ADT's agent is a Sierra deployment; so is Sonos's. The agent is positioned to the end customer as a named entity, not "the chatbot."[^16]
3. **Voice-first in key verticals.** Sierra has invested heavily in voice, which is where outcome-based pricing works best (easy to measure "did the caller's problem get solved") and where the incumbent IVR stack is weakest.[^16]
4. **Enterprise-only GTM.** Sierra does not have a self-serve SKU. This is a deliberate choice to keep model and eval quality under the vendor's control and to prevent race-to-the-bottom pricing pressure from SMB.

**The controversy inside Sierra's model:** the outcome-based pricing only works if the vendor controls the definition of "outcome," and even in the most aligned case, there is a clear incentive for the vendor to make agents optimistic about when they have "resolved" something. Taylor has pushed back on this publicly, arguing that the enterprise buyer has perfect transparency into the transcripts and the definition is negotiated per customer.[^16] Fair enough — but that negotiation is where the real ARR leakage happens, and it is why Sierra's revenue multiple is eye-watering: investors are betting Taylor can hold the line on quality-defined outcomes at enterprise scale, and if he can, that ARR compounds.

## Unit economics at scale — the honest spreadsheet

Here is the honest view of AI support economics across vendors, based on shipped deployments in 2024–2025.

**Per-interaction cost ranges (fully-loaded, 2025):**[^21]
- AI routine inquiry: $0.30–$0.99 per resolution
- Human agent, North America in-house: $5–$8 per interaction
- Human agent, offshore (Philippines, India): $1.50–$3 per interaction
- Voice human agent (any geo): roughly 2x chat equivalent

**The Gartner warning that every vendor deck ignores.** In a **January 26, 2026 press release**, Gartner projected that **by 2030 the cost per resolution for GenAI customer service will exceed $3 — higher than many B2C offshore human agents** — driven by rising data-center costs, a vendor pivot from subsidized growth to profitability, and increasingly complex, token-hungry use cases.[^22] Gartner's blunt framing: "Full automation will be prohibitively expensive for most organizations; instead, leading organizations will use AI to drive customer engagement rather than to cut costs." A companion projection in the same release sharpens the point: **by 2030, 10% of Fortune 500 companies will *double* their customer-service spend** to use AI for engagement rather than deflection.[^22] The implication is that the durable moat is not cost arbitrage — it is speed, availability, consistency, and lifetime-value expansion. If you are making a 2027–2030 support strategy bet on "AI will always be cheaper than humans," you are betting against a trend line Gartner now has a dated, primary-sourced number for.

**Integration costs nobody puts in the deck:**
- CRM / helpdesk integration: $30K–$200K implementation, one-time
- Knowledge-base rebuild (if current content is not AI-ready): $50K–$500K, one-time
- Ongoing content ops: 0.5–2 FTE per 20 human-agent equivalent
- Ongoing eval labor: 0.3–0.8 FTE per deployed agent
- Human escalation design: $20K–$100K one-time, plus 10–20% of ticket volume routed to humans costing full human rate

If you model a mid-market deployment (10K conversations/month) honestly, the year-1 TCO is typically $350K–$700K all-in, with payback inside 12–18 months if your pre-AI support cost was $700K+/year. If your pre-AI support cost was under $400K/year, the math does not work and you should buy Fin or a simpler bot, not an enterprise orchestration layer.

## Where support agents break — the four patterns

Across all four vendors and dozens of public post-mortems in 2024–2025, failures cluster in the same four patterns.

**Pattern 1 — Long-tail policy questions.** "Can I return this if my receipt shows a different card than the one I have now?" "What happens to my payment plan if I dispute a merchant charge?" The bot has all the policy documents in its RAG, but the specific interaction of policies is not written down anywhere — it lives in the head of a tenured human agent. Bots hallucinate an answer that sounds right and is wrong. This is the single biggest source of regulatory complaint volume in consumer fintech.

**Pattern 2 — Regulated domains.** Healthcare, finance, insurance, and anything that touches fraud. Morgan Lewis's 2025 summary of DOJ and state AG enforcement activity against healthcare AI tools is required reading for anyone deploying support bots in those domains: Texas AG settlements over deceptive accuracy claims, DOJ subpoenas of pharmaceutical and digital-health companies over AI-assisted documentation, and hallucination-driven false claims exposure.[^23] If your bot handles a medication question and hallucinates, you have a regulatory event, not a CSAT event. The right architecture here is intent-classification-first: detect the regulated intent, route to a human immediately, never let the bot answer.

**Pattern 3 — Non-English quality.** Every vendor undersells this because they sell in English first. Spanish, Portuguese, Japanese, Arabic, and Hindi CSAT at parity deflection is typically 5–15 points lower than English, driven by (a) less training data, (b) help-center content translated rather than written natively, (c) cultural-register mismatches (formal vs informal you, honorifics). If you are deploying in 10+ languages, budget a per-language eval operation. Klarna's 35-language deployment is genuinely impressive on this axis, and also part of why quality was uneven.

**Pattern 4 — CSAT cliffs at handoff.** When the bot escalates to a human, the customer has often already explained their problem three times. The human now has to either re-ask or read the transcript quickly; neither option is graceful. Customers who reach a human after a bot failure have systematically lower CSAT than customers who reach a human first. This is why Sierra's "escalation is free" pricing reframes escalation as a feature rather than a failure — a design choice as much as a pricing one.

## Exercise: the one-page vendor teardown

Your artifact for this lesson is a **one-page teardown** of one support-agent vendor. You can pick from the list above (Klarna's approach, Fin, Decagon, Sierra, Ada, Forethought) or pick any vendor currently pitching you.

The rubric has four sections. Use exactly this structure so you can compare teardowns across vendors later.

```
VENDOR: _______
DATE: _______
REVIEWER: _______

1. ARCHITECTURE (which Shape 1-4 are they? what do they own, what do you own?)
   - Where is the LLM call made?
   - Who owns the knowledge base, the routing rules, the tools/APIs?
   - What's the integration shape with your existing helpdesk / CRM?
   - What are the 2-3 specific claims in their pitch deck that depend on this architecture being right?

2. PRICING & UNIT ECONOMICS
   - Published price model (per-resolution? per-conversation? per-seat? platform fee?)
   - Cost per interaction AT YOUR VOLUME (do the math, don't copy the brochure)
   - Hidden costs (integration $, KB rebuild $, ongoing content ops $, eval labor $)
   - Payback period at your current pre-AI cost base

3. SHIPPED EVIDENCE
   - Which public case studies are real (named customer, named metric, dated)?
   - What IS the denominator for each published number? (deflection of what? resolution of what?)
   - What is the resolution/CSAT when regulated or long-tail intents are INCLUDED, not excluded?
   - One specific failure mode you can find in public sources (Trustpilot, Reddit, earnings transcripts)

4. WHERE IT BREAKS IN YOUR CONTEXT
   - Top 3 intents you cannot afford to let the bot answer wrong
   - Your non-English volume and quality needs
   - Regulatory exposure specific to your industry
   - The specific contract clauses you'd demand (return-within-7-days rate, post-AI CSAT, escalation-on-request data)

ONE-PARAGRAPH RECOMMENDATION (buy / pilot / pass) with the specific condition under which you would change your mind.
```

Timebox: 60 minutes. Sources: vendor site, one independent review (eesel, Fini Labs, G2), one case study, one negative signal (Trustpilot, Reddit, a critical blog post), one earnings transcript or funding announcement. If you cannot find a negative signal in 10 minutes of searching, that itself is a signal — the vendor is either very new or very good at suppressing public failure data, and both cases should change your recommendation.

When you run this on Fin, your teardown should end up recommending pilot for a mid-market helpdesk customer with $400K–$2M annual support spend and a clean help center. When you run it on Sierra, it should recommend pass unless you are a consumer brand with $10M+ support spend, voice volume, and a willingness to sign an enterprise contract. When you run it on Decagon, it should recommend pilot only after you've done a realistic data-cleanup cost estimate. When you run it on Klarna's do-it-yourself pattern, it should recommend build only if you have an in-house ML platform team with at least 5 engineers and an appetite for owning eval permanently.

If your teardown does not end up at one of those four positions — or at a clear "neither, here's what we build instead" — you have not been hard enough on the numbers.

## Reviewer lens — where I disagree with the industry consensus

Five specific disagreements, since we don't do generic reviewer lenses in this course.

1. **"AI support will always be cheaper than humans" is already wrong at the margin, and will be more wrong by 2028.** Gartner's 2030 projection of $3+ per GenAI resolution is in the right direction.[^22] Model-inference cost is falling, but context-window inflation, guardrail stacks, compliance overhead, and eval labor are rising faster. The winning argument for AI support in 2028 will be speed, 24/7 availability, and consistency — not cost. Vendors pitching cost savings as the primary ROI are pitching a depreciating asset.

2. **"Resolution rate" should be replaced with "net-resolved rate minus 7-day return rate" in every procurement contract.** The industry knows this and won't lead with it. Insist on it.

3. **Klarna's walk-back was mostly narrative, not technical.** Every vendor deck that cites Klarna's $40M 2024 profit improvement without citing the May 2025 "lower quality" admission is lying by omission. Every Klarna-skeptic piece that treats the walk-back as a refutation of AI support is also wrong. The correct read is: the pure-AI phase was a learning phase; the hybrid is the durable architecture; Klarna's 2024 numbers are real *and* incomplete.[^4][^5]

4. **Sierra's valuation-to-ARR multiple is either a bubble signal or an architecture signal, and you should know which before you buy.** A ~79x ARR multiple for Sierra ($15.8B on ~$200M ARR, May 2026 — down from ~100x and falling as ARR compounds)[^15] is not defensible under normal SaaS benchmarks. It is only defensible if outcome-based pricing becomes the industry-wide shape and Sierra becomes the platform. If you're evaluating Sierra, you are implicitly betting on that macro thesis. Be clear with yourself that you are.

5. **The category is going to consolidate on hybrid, and the winners will be the vendors who price the human escalation as a feature instead of a failure.** Sierra's "escalation is free" is a leading indicator. Klarna's "human on demand as brand promise" is another. Fin's resolution-only billing prices the human escalation as vendor lost revenue — a laggard signal I predicted would age badly. The 2026 update partly arbitrates that: Fin didn't reprice, it got *acquired* (Salesforce, ~$3.6B, June 2026), folding its resolution-billed agent into Agentforce.[^25] Consolidation, not repricing, is how the pricing-model tension resolved for the vertically-integrated independent — which is its own lesson about what happens to a strong product with a contested pricing axis in a consolidating market: a platform buys the distribution and inherits the pricing question.

## Common mistakes operators make when evaluating this category

1. **Copying the vendor's denominator.** 80% of what? Resolution of what population? Ask, always.
2. **Not separating AI-CSAT from blended CSAT.** Blended numbers hide the quality cliff on the 20% of hard cases that define your brand.
3. **Skipping the non-English evaluation.** If you serve non-English markets, you are buying a different product than the one in the English demo.
4. **Underestimating knowledge-base work.** Vendors say "2 weeks to go live." Budget 8–16.
5. **Pricing against today's human-agent cost, not 2028's AI cost.** Gartner's $3+ projection is directional — plan the 3-year contract assuming per-resolution price floors rise, not fall.
6. **Treating the vendor's eval as your eval.** You need a held-out labeled test set your vendor does not see, refreshed quarterly. Non-negotiable.
7. **Ignoring regulatory intent routing.** If a bot ever answers a medication question or a fraud question directly, you have an enforcement event waiting to happen.[^23]

## Reflection — questions worth thinking through

None of these are Google-able.

1. For your specific company, which of the four architectural shapes fits — and what constraint in your current stack makes it fit? If you've ever talked to a vendor in this space, your past conversations will answer this quickly.
2. If Klarna's 2024 $40M profit number is real but the 2025 quality walk-back is also real, what specifically would you measure in the 10th week of a deployment to catch the same pattern before it costs you brand equity?
3. Who inside your company owns the definition of "resolution" today? If the vendor owns it, what are you doing about that?
4. For a regulated intent (fraud, medical, insurance), what is the correct architecture — bot-first with human fallback, human-first with bot assist, or bot-forbidden-always? Pick one and defend it with a specific failure mode.
5. If Gartner is right and GenAI resolution cost crosses human offshore cost by 2030, what is the durable ROI argument for your 2026 deployment? If you can't answer, your ROI model is fragile.

## Further reading

**Must-read**
- OpenAI case study: *Klarna's AI assistant does the work of 700 full-time agents* (February 2024)[^1]
- Pragmatic Engineer: *Klarna's AI chatbot: how revolutionary is it, really?*[^3]
- Bloomberg / Fortune / CX Dive coverage of Klarna's May 2025 walk-back[^4][^5][^24]
- Bret Taylor on the Cheeky Pint podcast: *AI agents, outcome-based pricing, and the OpenAI board*[^16]

**Recommended**
- Intercom Fin outcomes page and Ibbaka's value-vs-pricing analysis[^9][^10]
- Decagon's Stripe case study and 2025 Series C announcement[^11][^12]
- a16z December 2024 enterprise newsletter on outcome-based pricing[^20]
- Ada's "sounding the alarm on containment rate" post[^19]
- Fini Labs: *Trust Metrics for AI Customer Support*[^18]

**Optional**
- Morgan Lewis on AI healthcare enforcement 2025[^23]
- Teneo 2025 AI vs live agent cost comparison[^21]
- Gartner's 2030 AI cost-per-resolution projection[^22]

## Citations

[^1]: OpenAI. *Klarna's AI assistant does the work of 700 full-time agents.* https://openai.com/index/klarna/ (Feb 2024).
[^2]: Klarna press release. *Klarna AI assistant handles two-thirds of customer service chats in its first month.* https://www.klarna.com/international/press/klarna-ai-assistant-handles-two-thirds-of-customer-service-chats-in-its-first-month/ (Feb 2024).
[^3]: Orosz, Gergely. *Klarna's AI chatbot: how revolutionary is it, really?* Pragmatic Engineer. https://blog.pragmaticengineer.com/klarnas-ai-chatbot/ (Apr 2024).
[^4]: Bloomberg. *Klarna Turns From AI to Real Person Customer Service.* https://www.bloomberg.com/news/articles/2025-05-08/klarna-turns-from-ai-to-real-person-customer-service (May 8, 2025).
[^5]: Fortune. *Klarna plans to hire humans again, as new landmark survey reveals most AI projects fail to deliver.* https://fortune.com/2025/05/09/klarna-ai-humans-return-on-investment/ (May 9, 2025).
[^6]: TechCrunch. *Klarna CEO says company will use humans to offer VIP customer service.* https://techcrunch.com/2025/06/04/klarna-ceo-says-klarna-vip-humans/ (Jun 4, 2025).
[^7]: CNBC. *Klarna CEO says AI helped company shrink workforce by 40%.* https://www.cnbc.com/2025/05/14/klarna-ceo-says-ai-helped-company-shrink-workforce-by-40percent.html (May 14, 2025); S&P Global. *Klarna set for 26% revenue jump in first post-IPO earnings.* (Nov 2025).
[^8]: Intercom. *Fin AI Agent pricing.* https://www.intercom.com/pricing and https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes (accessed Apr 2026).
[^9]: Intercom help. *Fin AI Agent resolutions.* https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes (accessed Apr 2026).
[^10]: Ibbaka. *Comparing the Value Model and Pricing Model of Intercom's Fin AI Agent.* https://www.ibbaka.com/ibbaka-market-blog/comparing-the-value-model-and-pricing-model-of-intercoms-fin-ai-agent (2025).
[^11]: Stripe. *Decagon AI Decreases Costs for Customer Support Operations by 65%.* https://stripe.com/customers/decagon (2025); Decagon case studies at https://decagon.ai/resources/ai-customer-service-agent-capabilities.
[^12]: Decagon / Business Wire. *Decagon Raises $131M at $1.5B Valuation.* https://www.businesswire.com/news/home/20250623894798/ (Jun 23, 2025). Series D: *Decagon's Valuation Triples to $4.5 Billion* — $250M at $4.5B, Jan 28 2026, $481M total raised. https://www.businesswire.com/news/home/20260128580542/en/Decagons-Valuation-Triples-to-$4.5-Billion-as-it-Ushers-in-the-Age-of-AI-Concierge ; cross-ref Sacra https://sacra.com/c/decagon/. Verified 2026-07-17.
[^13]: CNBC. *Bret Taylor's AI startup Sierra raises funding at $4.5 billion valuation.* https://www.cnbc.com/2024/10/28/bret-taylors-ai-startup-sierra-valued-at-4point5-billion-in-funding.html (Oct 28, 2024).
[^14]: TechCrunch. *Bret Taylor's Sierra raises $350M at a $10B valuation.* https://techcrunch.com/2025/09/04/bret-taylors-sierra-raises-350m-at-a-10b-valuation/ (Sep 4, 2025). Series E: *Sierra raises $950M as the race to own enterprise AI gets serious* — $950M at $15.8B, led by Tiger Global and GV. https://techcrunch.com/2026/05/04/sierra-raises-950m-as-the-race-to-own-enterprise-ai-gets-serious/ (May 4, 2026). Verified 2026-07-17.
[^15]: Sierra ARR: past $150M ARR in eight quarters (per company, via TechCrunch May 2026 above), ~$200M reported in 2026; Sacra profile https://sacra.com/c/sierra/. The ~79x multiple in the text = $15.8B ÷ ~$200M ARR. Verified 2026-07-17.
[^16]: Taylor, Bret. *Cheeky Pint podcast: AI agents, outcome-based pricing, and the OpenAI board.* https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents (2025).
[^17]: Ada. https://www.ada.cx/ and BVP's *Ada: Architecting fanatical CX loops.* https://www.bvp.com/atlas/ada-architecting-fanatical-cx-loops-that-power-ai-agents (2025); Forethought. https://forethought.ai/ai-agent-for-customer-support (accessed Apr 2026).
[^18]: Fini Labs. *Trust Metrics for AI Customer Support: Why Deflection Rate Is Killing Your Customer Experience.* https://www.usefini.com/blog/trust-metrics-for-ai-customer-support (2025).
[^19]: Ada. *Why customer service leaders are sounding the alarm on containment rate.* https://www.ada.cx/blog/why-customer-service-leaders-are-sounding-the-alarm-on-containment-rate/ (2025).
[^20]: Andreessen Horowitz. *AI Is Driving A Shift Towards Outcome-Based Pricing — December 2024 Enterprise Newsletter.* https://a16z.com/newsletter/december-2024-enterprise-newsletter-ai-is-driving-a-shift-towards-outcome-based-pricing/ (Dec 2024).
[^21]: Teneo. *AI vs Live Agent Cost: The Complete 2025 Analysis and Comparison.* https://www.teneo.ai/blog/ai-vs-live-agent-cost-the-complete-2025-analysis-and-comparison-2 (2025). The $5–$8/interaction North American in-house live-agent figure appears in the "Cost per Live Agent Interaction" / "Hidden costs of live agents" comparison sections — fully-loaded figure including wages, benefits, QA, training, tooling, management overhead and real estate, consistent with other 2024–2025 industry analyses of onshore L1 agent TCO.
[^22]: Gartner press release, *Gartner Predicts GenAI Cost Per Resolution for Customer Service Will Exceed Offshore Human Agent Costs by 2030* (Jan 26, 2026). https://www.gartner.com/en/newsroom/press-releases/2026-01-26-gartner-predicts-genai-cost-per-resolution-for-customer-service-will-exceed-offshore-human-agent-costs-by-2030 — >$3 cost per GenAI resolution by 2030; "full automation will be prohibitively expensive for most organizations"; companion stat: by 2030, 10% of Fortune 500 will double customer-service spend to use AI for engagement. Supersedes the earlier CX Today secondary. Verified 2026-07-17.
[^23]: Morgan Lewis. *AI in Healthcare: Opportunities, Enforcement Risks and False Claims.* https://www.morganlewis.com/pubs/2025/07/ai-in-healthcare-opportunities-enforcement-risks-and-false-claims-and-the-need-for-ai-specific-compliance (Jul 2025).
[^24]: CX Dive. *Klarna changes its AI tune and again recruits humans for customer service.* https://www.customerexperiencedive.com/news/klarna-reinvests-human-talent-customer-service-AI-chatbot/747586/ (May 2025).
[^decagon-pricing]: Industry pricing reporting for Decagon's AI agent platform (Decagon does not publish a rate card). AgenticAIPricing.com, *Decagon AI pricing case study.* https://www.agenticaipricing.com/ — floor-plus-per-conversation structure referenced across 2025 procurement analyses; cross-check with Sacra, *Decagon* https://sacra.com/c/decagon/.
[^25]: Salesforce, *Salesforce Signs Definitive Agreement to Acquire Fin* (Jun 15, 2026, ~$3.6B, expected close Q4 FY2027). https://www.salesforce.com/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/ ; TechCrunch, *Salesforce acquires AI customer service platform Fin for $3.6B* https://techcrunch.com/2026/06/15/salesforce-acquires-ai-customer-service-platform-fin-for-3-6b/ ; Intercom renamed itself Fin in May 2026. Fin pricing unchanged at $0.99/resolution. Verified 2026-07-17.

_last_verified: 2026-07-17_
