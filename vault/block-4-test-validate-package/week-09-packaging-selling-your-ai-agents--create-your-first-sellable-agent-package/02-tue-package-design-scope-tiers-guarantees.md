---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 2
day_name: tue
session_slug: packaging-selling-your-ai-agents
date_due: 2026-07-14
tags: [package-design, tier-ladders, sla, guarantees, error-budgets, onboarding, inclusion-exclusion, eval-report, outcome-definition, probabilistic-systems]
sources:
  - intercom-fin-pricing-2026
  - dragapp-intercom-pricing-2026
  - salesforce-fin-acquisition-2026
  - techcrunch-fin-acquisition-2026
  - cheekypint-bret-taylor-2026
  - cxmtoday-agentforce-help-agent
  - mavenagi-ai-sla-glossary
  - aipedals-llm-agent-slas-2026
  - buildmvpfast-agent-sla-2026
  - artisan-ava-2-launch-2026
  - quickchat-pricing-models-2026
last_verified: 2026-07-17
word_count_target: 5200
---

# Package design — outcome, scope fences, tier ladders, and how to guarantee a probabilistic system

## Why this matters

Yesterday you chose what to package. Today you write the promise, and the promise is the product. A buyer evaluating a package never sees your architecture; they see an outcome statement, a list of what is included, a tier grid, and a guarantee. Those four artifacts decide your close rate, your support burden, and whether month six finds you profitable or drowning in "quick exceptions." The hard part is the last artifact: your system is probabilistic, and buyers are trained by two decades of SaaS to expect guarantees. In 2026 the market has produced real answers — Fin charges $0.99 only per resolution, Sierra charges only when the agent succeeds and escalation is free, enterprise SLA practice has shifted from binary accuracy promises to error budgets and drift clauses — and today you learn to write a guarantee in that family that you can honor at your scale. By tonight you will have a drafted tier sheet and guarantee language for your Monday candidate, both stress-tested by an adversarial buyer.

## Prerequisites

- Monday's chosen package candidate with its four scope-collapse lists (input, output, integration, segment).
- [[06-sat-rag-evaluation|Week 4 Saturday's]] eval harness pattern: golden set, LLM-judge with human alignment, regression thresholds. Today turns that machinery into a *sales document*.
- [[05-fri-commercial-sow-for-ai-projects|Block 1 Friday's]] drift-SLA anatomy (metric, threshold, cadence, remediation ladder) and its refusal conditions. That lesson wrote SLAs for one bespoke client; today adapts the same skeleton for N package customers. One-line recap, not a re-teach: never sign a drift SLA on a metric you cannot measure or a distribution you don't control.

## Layer 1 — The outcome statement: one sentence, falsifiable, priced

A package begins with a sentence of the form: **[Named buyer] gets [specific outcome] within [time], measured by [metric], or [what happens]**.

Weak: "AI-powered market intelligence for your business." Strong: "DTC skincare brands get a daily competitor-and-trend brief in Slack by 7am, covering your 12 nominated sources, with every claim linked to its source; first brief live within 10 business days."

Four properties make the strong version work:

1. **Named buyer.** The segment collapse from Monday, surfaced. "DTC skincare brands" filters traffic and lets every later word assume context.
2. **Specific, schedulable outcome.** "Daily brief by 7am" is checkable by the customer without your help. Outcomes a buyer can self-verify generate trust; outcomes only you can measure generate disputes.
3. **A measurement the buyer understands.** "Every claim linked to its source" is a hallucination-containment promise translated into civilian language. You built the machinery in [[05-fri-reliability-engineering-for-unattended-agents|Week 8 Friday]]; the outcome statement is where that engineering becomes billable.
4. **A consequence.** Credit, fix-forward, or exit. A promise without a consequence is marketing; with one, it is a guarantee (Layer 4).

Two more, across build shapes, to calibrate the muscle. Report generator ([[06-sat-build-the-weekly-report-generator|Week 5]]): "Series-A SaaS finance teams get a board-ready weekly metrics narrative every Monday 8am, every number traceable to a warehouse query, first report in 5 business days; a missed Monday is a free month." Voice receptionist (Week 7): "Single-location dental clinics get every inbound call answered within 3 rings, appointments booked directly into [supported PMS], and anything clinical escalated to staff within 60 seconds; live in 7 days." Notice what all three share: a schedulable event the buyer witnesses without your help, a verification mechanism inside the product, and a consequence with a number in it. Notice also what none of them mention: models, agents, RAG, or AI. The buyer is purchasing the outcome; the machinery is your business, not theirs.

Write the outcome statement before the feature list, because everything that does not serve the sentence is a candidate for the exclusion list.

## Layer 2 — Inclusion/exclusion lists: the fence is the product

The inclusion list says what the package does. The **exclusion list is more important**: it is the legal and psychological fence that keeps N customers from turning your package back into N custom engagements.

Structure both lists in the same five categories, mirroring Monday's collapse axes plus support:

| Category | Include (example: "Niche Radar" brief) | Exclude explicitly |
|---|---|---|
| Inputs | Up to 12 web/RSS sources from the supported-source list; 3 changes/month | Paywalled sources; sources requiring login; social platforms blocked to crawlers; "just add this one API" |
| Outputs | One daily brief, fixed 5-section schema, ≤600 words, English | Custom formats; ad-hoc queries against the archive (that's the Standard tier); translations |
| Integrations | Slack webhook or email | CRM writes, Notion, custom webhooks (Enterprise); anything requiring credentials beyond a webhook URL |
| Quality & evals | Monthly eval report against the golden set; claim-level source links | Accuracy guarantees on individual claims; real-time correction SLAs |
| Support & change | 2 business-day email support; monthly config review call (Standard+) | Slack-channel-with-founder; same-day changes; strategy consulting |

Two disciplines make the fence hold. First, **write exclusions as sentences a salesperson can say out loud**: "We don't monitor LinkedIn — platforms that prohibit crawling stay off the list, which is also why our sources never get us blocked." Every exclusion should carry its reason; reasoned exclusions read as competence, bare ones as stinginess. Second, **route every exclusion somewhere**: to a higher tier, to a paid add-on, or to a named "not us, try X" answer. An exclusion with a route is a upsell; an exclusion without one is a leak where customers push.

The 2026 pricing-model literature converges on the same point from the vendor side: per-outcome and per-resolution products only function because "resolution" is tightly defined and everything else is out of scope or free-but-unbilled — Fin's public definition work on what counts as a billable "outcome" is a masterclass in fence-writing.[^1][^2]

## Layer 3 — Tier ladders: what actually varies between Starter, Standard, and Enterprise

Three tiers is the default for a reason: one anchor below, one above, most buyers in the middle. The design question is *which variables move across tiers*. For agent packages, six variables are worth moving; most first-time packagers move the wrong ones.

**Move these:**

1. **Volume of the value metric.** Sources monitored, briefs per day, conversations handled, runs per month. The cleanest tier variable because it maps to your COGS (Friday) and the buyer's size.
2. **Integration surface.** Starter: one delivery channel. Standard: two channels plus archive access. Enterprise: API access, SSO, custom webhooks. Integration surface is the strongest tier separator because it tracks both buyer sophistication and your delivery cost (Wednesday).
3. **Quality instrumentation.** This is the underused one: **the eval report as a tier deliverable.** Starter customers get the system; Standard customers get a monthly eval report (golden-set pass rate, drift trend, incident log) generated from the [[06-sat-rag-evaluation|Week 4 harness]]; Enterprise customers get quarterly re-baselining against their own labeled sample. You are selling your eval discipline as a product feature, which simultaneously justifies price and *forces you to keep the discipline alive*. No competitor selling vibes can match it, and buyers burned by 2024–25 agent-washing increasingly ask for exactly this evidence.
4. **Support and change velocity.** Response times, config-change allowances, review-call cadence.
5. **Commercial terms.** Month-to-month at Starter; annual with a break clause at Enterprise ([[05-fri-commercial-sow-for-ai-projects|Block 1's]] termination machinery, reused).
6. **Exclusivity.** For competitive-intelligence-shaped packages, "we serve one customer per competitive set" is an Enterprise line item worth real money and worth real thought — it caps your TAM per niche.

**Do not move these:** core output quality (a Starter customer receiving a worse-quality brief poisons word of mouth in a niche where everyone talks), security posture (credential handling is uniform or you will breach it), and honesty of the metric (never define "resolution" differently per tier).

A worked ladder for the running example:

| | Starter $750/mo | Standard $1,500/mo | Enterprise $3,500/mo |
|---|---|---|---|
| Sources | 6 | 12 | 25 + custom source onboarding |
| Delivery | Slack or email | Both + searchable archive | + API + custom webhook |
| Eval | Claim-level source links | + monthly eval report | + quarterly re-baseline on your labeled sample |
| Support | Email, 2 biz days | + monthly config call | + named contact, next-day changes |
| Terms | Monthly | Monthly | Annual, 60-day break clause |
| Exclusivity | — | — | One customer per competitive set |

Fin's own pricing anatomy is worth copying at the structural level: a modest platform base ($49/month including 50 resolutions in its standalone deployment) plus $0.99 per additional resolution.[^1][^2] The floor pays for the pipes; the variable scales with delivered value. Friday returns to the floor-plus-variable pattern quantitatively.

### Transfer check: the same ladder logic on a different build shape

The Niche Radar example is a scheduled-artifact package, and it is worth proving the ladder logic transfers to a conversational shape before you trust it. Take the Week 7 voice-agent build productized as a clinic receptionist package for dental groups. The value metric flips from sources to *handled calls*, and the tier variables re-derive themselves from the same six-item menu:

- **Volume:** Starter covers 300 handled calls/month, Standard 800, Enterprise 2,500, each with a cap-and-alert rather than silent overage billing (Friday explains why).
- **Integration surface:** Starter answers and takes structured messages delivered by email. Standard writes appointments into one named practice-management system from a supported list of two. Enterprise adds a second location, after-hours overflow routing, and a custom greeting flow. Notice the discipline: the supported-PMS list is the inclusion fence doing its job, because "can it write into our weird legacy system" is the request that would otherwise unravel the package into consulting.
- **Quality instrumentation:** Starter gets call recordings and transcripts. Standard adds the monthly eval report, here scored on a golden set of 40 synthetic and 10 consented-real calls: booking accuracy, escalation correctness, and a caller-experience rubric. Enterprise adds quarterly re-scoring against the clinic's own labeled calls.
- **Support and terms:** as before, response times and break clauses climb with price.

Two things transfer unchanged: the exclusion list carries the reasons ("we do not give clinical advice on calls; the agent escalates every symptom question to staff, which is also why your malpractice carrier will not mind us"), and the eval deliverable is the differentiation. One thing does not transfer: call volume is customer-driven rather than schedule-driven, so the COGS model needs a per-call distribution, not a fixed run count, and the guarantee needs a concurrency clause (what happens when four calls arrive at once). When you run Wednesday's COGS math, that difference is the whole exercise. If you can re-derive your tier ladder for a second build shape in under thirty minutes, you understand the method; if the second ladder feels like starting over, revisit which variables you tiered and why.

### Onboarding as part of the product

Custom services treat onboarding as pre-sales friction. Packages treat it as a *chapter of the product* with its own deliverable and sometimes its own price. Design it as a fixed checklist with owner and clock: source nomination (customer, day 1–2), config and credential setup (you, day 3–4), golden-set calibration run (you, day 5–7), acceptance review against the outcome statement (both, day 8–10). Two design rules. First, **time-to-first-value is the metric**: the customer should see a real (even if imperfect) brief by day 3, not day 10; agent products live or die on the first week's felt momentum. Second, **charge for onboarding when it carries real labor** — a $500–$1,500 one-time setup fee filters unserious buyers, funds the calibration work honestly, and (usefully) anchors the monthly fee as the *cheap* part. Waive it tactically for design partners in exchange for a case study, never silently.

## Layer 4 — Guarantees for probabilistic systems: the live controversy

Here is the problem in one line: buyers want "guarantee it works"; your system is a probability distribution. Signing a naive accuracy guarantee is signing up to be wrong for money. Refusing all guarantees loses deals to whoever lies better. The 2026 market has three coherent positions, and you need to pick one deliberately.

**Position A — price the guarantee in: charge only on success.** Bret Taylor's Sierra runs the purest version: a pre-negotiated rate per autonomous resolution, and if the agent escalates to a human, it is free.[^3] Salesforce's Agentforce Help Agent shipped the same shape in 2026: pay-per-resolution, with no charge when the customer requests human escalation or leaves negative feedback.[^4] And Fin's $0.99-per-resolution is the mass-market version, now heading into Salesforce itself via the ~$3.6B acquisition agreement signed June 15, 2026.[^5][^6] The elegance: the guarantee and the price are the same object. You never argue about accuracy because failure is free. The cost: you need volume for the statistics to pay you, you need airtight *resolution definitions* (Fin publishes and litigates theirs), and you carry all the performance risk — which a solo packager with eleven customers cannot diversify the way Sierra can across the Fortune 50.

**Position B — engineer the guarantee: SLOs, error budgets, drift clauses.** The enterprise-SLA practice literature for LLM agents has converged on a recognizable stack: acknowledge that 100% accuracy is mathematically off the table for probabilistic systems; commit to *statistical* service levels (e.g., ≥90% golden-set pass rate measured weekly over a rolling month) with error budgets rather than binary promises; add a drift clause obligating the vendor to retune if performance falls more than a stated margin (±5% is a commonly cited default) from the deployment baseline; and refuse to expose any customer-facing guarantee you have not first run internally as an SLO.[^7][^8][^9] This is [[05-fri-commercial-sow-for-ai-projects|Block 1 Friday's]] drift-SLA skeleton, generalized from one client to a fleet: same four components (metric, threshold, cadence, remediation ladder), but now the metric must be *identical across customers* so one golden set and one weekly job service every contract.

Because most readers will eventually graduate from Position C to Position B, here is what B looks like drafted for the running example, in package language rather than bespoke-contract language:

> *Quality service level (Standard and Enterprise tiers). We measure the package weekly against a versioned golden evaluation set for your niche pack (provenance disclosed in each monthly report). Committed level: a rolling four-week golden-set pass rate of at least 88%. Error budget: up to 3 individual failed items per week carry no consequence provided the rolling rate holds. Drift obligation: if the rolling rate falls more than 5 percentage points below your deployment baseline, we begin retuning within 2 business days at no charge and report progress weekly until restored. Exclusions: degradation caused by customer-side source changes outside the supported list, or by configuration changes you requested in writing. This service level does not promise correctness of any individual claim; the claim-level source links exist so you can verify anything that matters before acting on it.*

Read what that clause does. It names the metric and its provenance, so an audit has an object. It budgets errors, so one bad Tuesday does not breach the contract. It converts drift from an argument into a clock. It fences causes you do not control, which is the fleet version of Block 1's refusal conditions. And its last sentence sets the correctness expectation honestly instead of hiding it, which is the sentence most vendors are afraid to write and most buyers are relieved to read.

**Position C — refuse the accuracy guarantee; guarantee the process.** For low-volume, high-variance packages, the honest structure is: guarantee delivery (the brief arrives by 7am, 99% of weekdays), guarantee instrumentation (monthly eval report, incident disclosure within 48h), guarantee remediation velocity (failures diagnosed in 2 business days), and guarantee exit (cancel monthly, data handed back) — while explicitly declining to guarantee any per-item accuracy number. MavenAGI's SLA guidance says the quiet part plainly: if you cannot measure "agent accuracy" consistently, do not put it in a contract.[^8]

**How to choose.** The decision variable is *measurement plus volume*. Per-success pricing (A) needs a crisply countable success event and enough monthly events per customer that variance averages out; below roughly a few hundred billable events per customer per month, one bad week whipsaws your revenue and their trust. Error-budget SLAs (B) need your eval harness running in production with history, and a buyer sophisticated enough to read them. Process guarantees (C) fit everything else and are the right default for a first package: they are honorable, cheap to honor, and upgradeable to (B) once six months of eval history exists. What is *not* coherent is the common cop-out — vague marketing promises ("99% accurate!") with contractual silence. That is Position D: lying, with a lag.

One more 2026-specific clause belongs in every option: **model-change disclosure.** Your package runs on models that will be deprecated or repriced under you (Wednesday covers the 2026 deprecation wave in detail). Commit to notifying customers of model swaps that materially affect behavior, and to re-running the golden set across every swap with the results in the next eval report. It costs you a CI run and buys you the credibility every agent-washing vendor lacks.

## Runnable experiment — draft the tier sheet, then survive procurement

Allow 90 minutes. Output: a tier sheet and guarantee language that survived two adversarial reviews.

**Step 1 — Draft (30 min).** Using Monday's collapse lists, write for your candidate: the outcome statement (Layer 1 format), the five-category inclusion/exclusion table, a three-tier ladder moving at least four of the six tier variables, and a guarantee in whichever of Positions A/B/C you chose, with one sentence justifying the choice by measurement-plus-volume.

**Step 2 — Procurement attack (25 min).** In a fresh Claude.ai conversation:

> *You are a procurement manager at [named buyer type] evaluating this package. You are skeptical of AI vendors after two burned pilots. Produce: (1) the 8 hardest questions you would ask before signing, (2) every term on this sheet that is ambiguous enough to dispute at renewal, (3) the two guarantees you would demand that are missing, and (4) the tier you would actually buy, with the discount you would demand.*

**Step 3 — Counsel attack (20 min).** Second fresh conversation: paste only the guarantee language.

> *You are the vendor's (my) lawyer. For each promise, classify: (a) measurable and honorable as written, (b) measurable but under-specified (what's missing?), (c) unmeasurable — rewrite or delete. Flag any promise that becomes dishonorable at 20 customers even if honorable at 3.*

**Step 4 — Revise (15 min).** Fold in the findings. Mark each change with which attack produced it.

**Pass bar:** every inclusion is measurable; every guarantee names its metric, cadence, and consequence; the procurement persona finds no term it can turn into free custom work; and you can state, in one sentence each, why the two missing guarantees procurement demanded are excluded (or which tier now carries them, at what price).

## Problem set

1. **Resolution-definition drill.** Write Fin-grade definitions for your package's billable event and its non-billable neighbors. For the running example: what exactly counts as a "delivered brief" when 2 of 12 sources were unreachable that morning? Your answer must be executable by code, not judgment.
2. **The tier-inversion test.** For each tier variable you moved, verify the *delivery cost* actually rises with the price. Find the one variable in your ladder where Enterprise costs you barely more than Starter; that variable is margin — label it honestly and check a competitor couldn't undercut it trivially.
3. **Guarantee arithmetic.** Assume Position A pricing at $2 per successful run, 85% success rate, 200 runs/customer/month. Compute monthly revenue per customer, then recompute at 70% success during a bad model-swap month. What revenue volatility did you just sign up for, and at what customer count does it stop threatening rent?
4. **Exclusion-route audit.** Take your five most-likely customer requests that sit outside scope. Route each: tier upgrade, paid add-on, or "not us, try X." Any request without a route gets one now.
5. **Rewrite a real SLA.** Find any public AI-agent SLA or pricing page (Fin's and Agentforce's resolution definitions are searchable). Identify which of Positions A/B/C it takes, and rewrite its weakest clause to be measurable.

## Reflection questions

- Sierra can absorb a 15% resolution-rate dip across the Fortune 50; you cannot absorb it across nine customers. What, structurally, is your version of their diversification?
- Which promise in your tier sheet would you be most relieved to delete? That relief is information: is the promise unhonorable, or just unmeasured?
- If a customer never opens the monthly eval report, is it still worth producing? (Consider who else reads it: renewals, procurement, your own regression discipline.)

## Common failure modes at scale

- **Selling the inclusion list, negotiating the exclusion list.** The sheet says 12 sources; the founder grants 15 "just this once" on a closing call. At ten customers, "just this once" is your roadmap, unpriced.
- **Accuracy theater.** Quoting "95% accuracy" in marketing with no metric, denominator, or cadence. Sophisticated buyers now ask which golden set; unsophisticated ones remember the number at renewal when anything goes wrong.
- **Tiering on quality.** Making Starter subtly worse at the core job to force upgrades. In a tight niche, your Starter output *is* your marketing; degrade it and every prospect sees the degraded version first.
- **Guaranteeing an average, honoring an anecdote.** Your SLA says ≥90% monthly pass rate; your customer experiences Tuesday's one embarrassing miss forwarded to their CEO. Pair statistical guarantees with an incident-response promise, because incidents, not averages, are what customers feel.
- **Onboarding as improvisation.** No checklist, no clock, no acceptance step. Every improvised onboarding trains that customer to expect improvisation forever, and burns the hours your package price assumed you would not spend.
- **One guarantee for all tiers.** Giving Starter customers Enterprise-grade remediation promises because writing two versions felt fussy. Your cheapest customers become your most expensive.

## My take (reviewer lens)

**Hamel Husain** would sharpen Layer 3's eval-report move and then push on it: an eval report generated from a golden set the customer never sees is dangerously close to grading your own homework in public. His discipline says the report only earns trust if the golden set's provenance is disclosed (how sampled, how labeled, when last refreshed against production traces) and if error analysis on *real* customer traffic feeds it monthly — otherwise you are shipping the ritual of evals without the substance, prettier but not truer than "95% accurate." He is right, and Saturday's eval-report template includes a provenance block because of exactly this critique. **Boris Cherny's** fleet-scale lens attacks Layer 4 from the operations side: every guarantee is a *runbook obligation*, and the question that matters is not whether the clause reads well but what fires when the threshold breaches at 2am across eleven tenants — if your remediation ladder is "founder wakes up," Positions A and B are both fiction, and honest Position C is worth more than aspirational B. **The cohort peer** would say the uncomfortable simple thing: this lesson risks two days of artifact-polishing before anyone has said the price out loud to a human. Draft the tier sheet in 90 minutes, show it to one real prospect this week, and let their eyebrows — not Claude's personas — tell you which guarantee is missing. All three are corrections of degree, not direction: the artifacts matter because they compound, but only contact with buyers makes them true.

## Further reading

**Must-read**

- Bret Taylor on outcome-based pricing (A Cheeky Pint / Sierra, 2025–26) — Position A from its clearest practitioner.[^3]
- Intercom's Fin pricing and outcomes documentation — the best public specimen of billable-event definition work.[^1]
- AIPedals, *Service Level Agreements for LLM Agents (2025–2026)* — the error-budget/cognitive-reliability framing behind Position B.[^7]

**Recommended**

- MavenAGI, *AI Service Level Agreement (SLA)* glossary — "don't contract what you can't measure," from a vendor that must live by it.[^8]
- CXM Today on Agentforce Help Agent's pay-per-resolution launch — Position A going mass-market.[^4]
- [[05-fri-commercial-sow-for-ai-projects|Block 1 Friday]] — the drift-SLA skeleton this lesson generalizes.

**Optional**

- Quickchat AI, *AI Agent Pricing Models 2026* — a taxonomy of per-resolution vs per-conversation vs per-action definitions.[^10]
- BuildMVPFast, *AI Agent SLAs: Uptime, Accuracy, and Response Time Guarantees* — drift-clause templates.[^9]

## Citations

[^1]: Intercom, Fin pricing and outcome definitions — $0.99 per resolution/outcome; standalone "Fin for platforms" at $49/month including 50 resolutions. https://www.intercom.com/learning-center/ai-customer-service-agent-pricing-comparison ; https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Drag, *Intercom Pricing 2026: Seats, Fin AI Outcomes & the Real Total*: independent corroboration of the $0.99/outcome and base-fee structure. https://www.dragapp.com/blog/intercom-pricing/ ; see also https://www.getmacha.com/blog/intercom-fin-ai-agent-complete-guide (search-verified 2026-07-17)

[^3]: Bret Taylor, *AI agents, outcome-based pricing, and the OpenAI board* (A Cheeky Pint; mirrored by Sierra): pre-negotiated per-resolution rate, escalation free; outcome pricing as the successor to seats and tokens. https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents ; https://sierra.ai/resources/podcasts/bret-taylor-of-sierra-on-ai-agents-outcome-based-pricing-and-the-openai-board (search-verified 2026-07-17)

[^4]: CXM Today, *Salesforce Launches Pay-Per-Resolution Agentforce Help Agent*: charge only on autonomous start-to-finish resolution; no charge on human escalation or negative feedback. https://cxmtoday.com/news/salesforce-launches-pay-per-resolution-agentforce-help-agent/ ; corroborated by https://quickchat.ai/post/ai-agent-pricing-models (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Salesforce, *Salesforce Signs Definitive Agreement to Acquire Fin*, June 15, 2026 (~$3.6B all cash; ~76% autonomous resolution rate claimed; 30,000+ customers; close expected early 2027 pending approvals). https://www.salesforce.com/news/press-releases/2026/06/15/salesforce-signs-definitive-agreement-to-acquire-fin/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: TechCrunch, *Salesforce acquires AI customer service platform Fin for $3.6B*, June 15, 2026. https://techcrunch.com/2026/06/15/salesforce-acquires-ai-customer-service-platform-fin-for-3-6b/ ; also The Irish Times, https://www.irishtimes.com/business/2026/06/15/salesforce-to-buy-fin-formerly-intercom-for-36bn/ (search-verified 2026-07-17)

[^7]: AIPedals, *Service Level Agreements for LLM Agents (2025–2026)*: statistical confidence intervals and error budgets replacing binary guarantees; "cognitive reliability" beyond availability. https://www.aipedals.com/charms/service-level-agreements-for-llm-agents-2025-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: MavenAGI, *AI Service Level Agreement (SLA)*: accuracy, resolution-rate, hallucination-threshold and escalation metrics in AI SLAs; do not contract accuracy you cannot measure consistently; start with internal SLOs. https://www.mavenagi.com/glossary/ai-service-level-agreement (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^9]: BuildMVPFast, *AI Agent SLAs: Uptime, Accuracy, and Response Time Guarantees* (2026): drift clauses keeping accuracy within a stated margin (±5% cited) of deployment baseline, with retune obligations. https://www.buildmvpfast.com/blog/ai-agent-sla-uptime-accuracy-response-time-guarantee-2026 (search-verified 2026-07-17; single-source template details, attributed)

[^10]: Quickchat AI, *AI Agent Pricing Models 2026: Per-Resolution vs Per-Seat Compared*: definitional taxonomy of billable events across vendors. https://quickchat.ai/post/ai-agent-pricing-models (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
