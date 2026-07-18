---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 3
day_name: wed
session_slug: packaging-selling-your-ai-agents
date_due: 2026-07-15
tags: [multi-tenant, single-tenant, config-over-code, credential-management, white-label, hosting-economics, maintenance-contracts, model-deprecation, upgrade-trains, delivery-runbook]
sources:
  - anthropic-model-deprecations-docs
  - anthropic-deprecation-commitments
  - make-claude-deprecations-2026
  - endoflife-claude
  - anthropic-sonnet-5-pricing
  - finout-sonnet5-pricing-2026
  - techcrunch-sonnet5-2026
  - aimadetools-tokenizer-2026
  - stammer-white-label-2026
  - pickaxe-white-label-2026
  - trillet-white-label-voice-2026
  - aiforanything-deprecation-migration-2026
last_verified: 2026-07-17
word_count_target: 4500
---

# Delivery engineering — one build, many customers: tenancy, config-over-code, white-labeling, COGS, and the deprecation wave as a revenue line

## Why this matters

A package is a promise that customer #2 through #20 cost you engineering-almost-nothing to serve. That promise is won or lost in delivery architecture, decided this week, lived with for years. Today you make four decisions: how customers share (or don't share) infrastructure; where per-customer difference lives (config, never code); whether you build the serving layer or rent it white-label; and what your inference COGS actually are at July-2026 prices. Then the part almost every new packager skips: **maintenance as a product line**. In the first half of 2026 alone, Anthropic retired the entire Claude 3 and 3.5 generations and gave Opus 4.1 users a 60-day runway; every agent package in production had to migrate, re-baseline evals, and re-verify behavior — and the operators who had sold maintenance contracts got *paid* for that work while everyone else ate it as unbilled panic.[^1][^2][^3] By tonight you will have a delivery runbook skeleton and a maintenance offer with a price on it.

## Prerequisites

- Tuesday's tier sheet: tiers determine tenancy and integration surface, so the ladder must exist before the architecture.
- [[02-tue-mcp-integration-patterns-for-unattended-agents|Week 8 Tuesday]]: headless auth, least-privilege credentials, idempotency for unattended agents. Today scales those patterns from one deployment to N.
- [[05-fri-reliability-engineering-for-unattended-agents|Week 8 Friday]]: golden-set regression and drift metrics. The fleet version of that harness is today's upgrade-train gate.
- [[05-fri-commercial-sow-for-ai-projects|Block 1 Friday]] on two-directional token-cost pass-through. One-line recap: model prices now move both directions mid-contract; the clause that survives indexes to the named tier's published rate. Today's COGS math is what you feed that clause.

## Layer 1 — Tenancy: what customers share, and what sharing costs

"Multi-tenant vs single-tenant" sounds like an infrastructure choice; it is actually a *blast-radius and margin* choice. Separate three planes and decide each independently:

- **Control plane** — the orchestration code, schedulers, eval harness, dashboards. Always shared. One codebase, one deployment, versioned once. If you find yourself forking control-plane code per customer, you have already lost the packaging game; that fork is a second product you accidentally created.
- **Data plane** — customer inputs, outputs, archives, embeddings. The real decision. Shared-with-isolation (one database, tenant-ID on every row, enforced at the query layer) is the default for packages at your scale: cheapest to operate, one migration to run, one backup to verify. Physically-separate-per-tenant (separate DBs or projects) is what you sell when the *buyer's* compliance posture demands it, and it belongs on the Enterprise tier at an honest premium, because every isolated tenant is a standing operational obligation: its own migrations, monitoring, and 2am failure modes.
- **Credential plane** — API keys, webhooks, OAuth grants per customer. Never shared, never co-mingled, and never embedded in code or prompts. The pattern that scales is a per-tenant secrets namespace (one vault path or encrypted row per customer) that the control plane resolves at runtime by tenant ID. This is [[02-tue-mcp-integration-patterns-for-unattended-agents|Week 8's]] least-privilege discipline made multi-tenant: each customer's agent runs with *that customer's* scoped credentials, so a compromise or a bug in tenant A's context physically cannot exfiltrate tenant B's data. The lethal-trifecta logic from Block 0 gets worse with tenancy: an agent processing untrusted scraped content while holding a shared credential store is one prompt-injection away from a cross-customer breach that ends your business, not just an account.

Two sharing consequences to price in. **Noisy neighbors:** one customer's 25-source Enterprise config can starve the 7am delivery window for everyone if your scheduler is naive; per-tenant budgets and rate limits (compute, tokens, wall-clock) belong in the control plane from day one, because they are also your COGS enforcement (Layer 4). **Compliance asymmetry:** the moment one prospect says SOC 2, HIPAA, or "EU data residency," the answer is not to re-architect the fleet; it is a priced Enterprise variant on isolated infrastructure, or a polite referral. Do the arithmetic before agreeing: one isolated tenant frequently costs more operational attention than five pooled ones.

## Layer 2 — Config-over-code: the golden build and the upgrade train

The delivery-engineering law of packages: **customer difference lives in configuration; behavior lives in one versioned build.** Concretely:

```yaml
# tenants/acme-skincare.yaml — everything customer-specific, nothing else
tenant_id: acme-skincare
tier: standard
niche_pack: dtc-skincare        # selects prompt pack + golden set + source templates
sources:                         # from the supported-source list only
  - {type: rss, url: "https://...", label: "Beauty Independent"}
  - {type: web, url: "https://...", label: "Competitor A blog"}
delivery:
  channel: slack
  webhook_secret_ref: vault://tenants/acme-skincare/slack   # reference, never a value
  send_at: "07:00"
  timezone: "America/New_York"
model:
  tier: sonnet-5                 # named tier, date-stamped rates in models.py
  monthly_token_budget: 9_000_000
```

The rules that keep this honest:

1. **The config schema is the product boundary.** If a customer request cannot be expressed in the schema, it is not in the package (route it per Tuesday's exclusion discipline: tier, add-on, or no). Extending the *schema* is a product decision that ships to everyone; editing one tenant's behavior in code is drift back to snowflakes.
2. **Prompts are config, versioned like code.** A `niche_pack` bundles the prompt set, output schema, and golden eval set for a segment. Customer-specific prompt edits are the most tempting and most corrosive customization: within one niche, resist them almost absolutely; the correct response to "our brief should emphasize X" is a niche-pack parameter every tenant gets, or nothing.
3. **One golden build, explicit upgrade trains.** Version the whole serving artifact (`package v1.7.0 = code + prompt packs + model tier + eval baselines`). Upgrades roll as trains: canary on your own internal tenant, then a batch of consenting tenants, then the fleet, with the [[05-fri-reliability-engineering-for-unattended-agents|Week 8 Friday]] regression harness run *per niche pack* as the gate between stages. A tenant "pinned to the old version because they liked it" is a fork with a customer attached; contract for a bounded pin window (30–60 days), not an indefinite one — the deprecation wave below shows what indefinite pins cost.
4. **Onboarding is config generation.** Tuesday's onboarding checklist, mechanized: intake answers → tenant YAML → calibration run → acceptance. Saturday's code-lab ships a generator that does exactly this, because delivery speed at customer #7 is a function of how little thinking onboarding requires.

**What an upgrade train looks like in practice.** Concreteness helps, because "version the whole artifact" sounds abstract until you see a release. Suppose the current fleet runs `niche-radar v1.6.2` and you want to ship two changes: a better dedup prompt in the `dtc-skincare` pack, and a switch of the synthesis stage from Sonnet 5 to a cheaper tier for the extraction sub-step. The release process, end to end:

1. Cut `v1.7.0` as a branch: prompt-pack diff + model-tier change in the pack's config, nothing tenant-specific touched.
2. Run the per-pack regression: golden set for `dtc-skincare` against `v1.7.0`, compared to the recorded `v1.6.2` baseline. Gate: no metric drops more than its threshold; cost per run recorded alongside quality, because a cost improvement that costs two quality points is a decision, not a win.
3. Canary: your own internal tenant runs `v1.7.0` for three days of real deliveries.
4. Batch 1: two consenting tenants (your design partners, who traded early-access feedback for their discount) run it for a week; their eval reports note the version change per Tuesday's disclosure clause.
5. Fleet: everyone else moves; the changelog entry is two sentences a customer can read.
6. Rollback condition, written before step 3: any tenant's weekly pass rate drops below its floor, that tenant reverts to `v1.6.2` within one delivery cycle while you diagnose.

Total ceremony for a ten-tenant fleet: perhaps two hours of wall-clock attention across a week, almost all of it reading eval output. That is the correct amount. The point of the train is not process for its own sake; it is that every change to a fleet has a version number, a quality gate, and an undo.

## Layer 3 — Build vs white-label: renting the productization layer

You do not have to build the serving layer. A 2026 cottage industry exists to productize agents *for* agencies: Stammer AI and similar platforms provide the multi-tenant dashboard, client billing, sub-accounts, and branding under your domain for roughly $197/month, while agencies resell agents at $300–$500/month per client plus a 3–5× markup on usage;[^4][^5] adjacent stacks (Voiceflow's custom-quoted reseller plans, Synthflow, and the voice-focused wrappers) cover chat and voice variants.[^5][^6]

The decision is a control-vs-speed trade, and it is honest to take either side:

- **White-label wins** when your value is niche knowledge and distribution, the agent shape is commodity (support chat, receptionist, appointment voice), and time-to-revenue matters more than margin structure. You inherit tenancy, billing, and dashboards on day one.
- **Building wins** when the agent shape *is* your edge (your Week 8 pipeline is not on anyone's white-label menu), when eval instrumentation is your differentiator (Tuesday's eval-report tier does not exist on wrapper platforms), or when platform risk is intolerable: a white-label package inherits its platform's pricing changes, model choices, deprecation schedule, and existence. Every risk this course taught you to contract against with model vendors ([[05-fri-commercial-sow-for-ai-projects|Block 1]]), you now hold *uncontracted* against a much smaller company.
- **The hybrid** is often right: build the differentiated pipeline; rent commodity surfaces around it (billing via Stripe, dashboards via retool-class tools) rather than the whole serving layer.

The test: write down the three package features buyers cite when they choose you. If a white-label platform offers all three off the shelf, your edge is distribution, and you should rent. If none, build. If some, hybrid.

Run the numbers on a concrete case, because the intuition ("renting is expensive") is often wrong at small scale. A commodity receptionist-agent package sold at $400/month per client: on a Stammer-class platform at ~$197/month flat plus usage passed through with your 3–5× markup, ten clients gross roughly $4,000/month against perhaps $600 of platform-plus-usage cost, and your delivery labor is configuration inside someone else's dashboard.[^4][^5] Self-built, the same ten clients might carry $150/month of infrastructure instead of $600, but you now own the tenancy code, the telephony edge cases, the dashboard your clients log into, and every 2am failure; at a loaded $150/hour, the build-and-operate delta wipes out the margin difference for at least the first year. The white-label toll starts to bind at two boundaries: scale (at fifty clients the platform's per-client economics and your differentiation ceiling both pinch) and dependency (a platform price change or shutdown propagates to your whole book, and you hold no contractual machinery against it). Write the crossover arithmetic for your own package before deciding on vibes in either direction.

## Layer 4 — Hosting economics at July-2026 model prices

Packages die quietly from COGS nobody computed. The worked example below is the running "Niche Radar" Standard tier; Saturday's code-lab parameterizes all of it so you can run your own numbers.

**The per-run model.** One daily run per tenant: fetch/parse 12 sources (deterministic, ~free), then LLM stages (extract, dedup-judge, synthesize, critic) consuming roughly 220K input + 18K output tokens per run on realistic mid-2026 source volumes. On **Claude Sonnet 5 at intro pricing ($2/M input, $10/M output, in effect through August 31, 2026)**:[^7][^8]

- Input: 0.22M × $2 = $0.44; output: 0.018M × $10 = $0.18 → **$0.62/run**
- ~22 business-day runs/month → **$13.60/month** inference per tenant
- Add hosting slice (scheduler, DB, monitoring ~$40/month across, say, 10 tenants → $4), delivery infra ($1), eval regression runs ($2/month per niche pack, amortized): **all-in COGS ≈ $21/tenant/month** against a $1,500 price. Gross margin ≈ 98.6% on paper.

Now the three corrections that separate this course from a YouTube margin fantasy:

1. **The tokenizer correction.** Sonnet 5 (like Opus 4.7+) uses the newer tokenizer producing roughly 30% more tokens for the same text, so April-2026 token estimates understate July-2026 bills; the numbers above already assume post-change counts — if you ported an older estimate, multiply by ~1.3 before trusting it.[^8][^9]
2. **The date-stamp correction.** Intro pricing ends August 31, 2026: $3/$15 thereafter, a +50% COGS move on the same workload ($13.60 → ~$20.40/month inference).[^7][^8] Your pricing (Friday) must survive that step-change without a renegotiation, which is why the model tier and its rate-card date belong *in the config file*, not in your memory.
3. **The support correction — the real COGS.** At package scale, inference is rarely your biggest cost; *your hours* are. Two support tickets a month at a loaded $150/hour dwarfs $21 of inference. The margin case for packages was never "tokens are cheap"; it is "the runbook amortizes." Which means the runbook's quality is a line item on your P&L, and skimping on it is a COGS decision, not a documentation preference.

Sensitivity habit: recompute COGS at (a) standard pricing, (b) a forced upgrade to a flagship tier (Fable-5-class at $10/$50 doubles-plus the token line), (c) 2× source volume. If any scenario pushes tier COGS above ~30% of tier price, the tier is mispriced or the pipeline needs a cheaper model for its deterministic-adjacent stages.

## Layer 5 — Maintenance contracts: the deprecation wave as evidence and revenue

Here is the 2026 evidence that maintenance is a product, not an apology. Anthropic's deprecation ledger for the first half of 2026: Claude Opus 3 retired January 5; the Claude 3.5 generation retired February 19; Claude 3 Haiku retired April 20 (completing the Claude 3 family's retirement); Opus 4 and Sonnet 4 deprecation notices went out April 14; Opus 4.1 was notified June 5 and retired June 15 — with Anthropic's stated policy guaranteeing at least 60 days' notice for publicly released models, and (per its deprecation commitments) preserving Opus 3 access on request as the first model retired under the new process.[^1][^2][^10] The blast radius was ecosystem-wide: platforms like Make shipped dedicated migration documentation telling *their* customers which scenarios would break on June 15.[^3]

Read that ledger as a package operator and three facts fall out:

1. **Every deployed agent package has a hard dependency with a ~12–18 month half-life.** Migration is not an if. On the current cadence, a package sold in July 2026 will migrate models at least once during a 12-month contract.
2. **Migration is real, billable work.** A model swap on a probabilistic system is not a string change: it is re-running golden sets per niche pack, re-tuning prompts where behavior shifted, re-baselining drift thresholds, updating COGS math (new rates, possibly new tokenizer), and notifying customers per Tuesday's model-change disclosure clause. That is precisely the work your Week 4/8 eval infrastructure makes estimable: with a harness, a migration is a CI run plus targeted fixes; without one, it is archaeology.
3. **Therefore: sell it.** The maintenance line for an agent package, priced as 15–25% of the package's annual value or bundled into Standard+ tiers, covers: model migrations with eval re-baseline (the headline item, with the H1-2026 wave as your evidence when a buyer asks why); integration drift (source sites change markup, APIs version — [[03-wed-the-scraping-stack-legally-and-technically|Week 8 Wednesday's]] world guarantees this); monthly eval reports (Tuesday's deliverable); and security/patch currency. Buyers who balk get the honest counter-question: "When your model provider retires the model this runs on — and this year they did it to five model families in six months — who does that work, on whose clock?"

**The controversy, named.** *Is maintenance revenue rent-seeking?* Position A (buyer-skeptic): recurring "maintenance" on software the vendor controls is the oldest agency margin trick; if your package were engineered well, migrations would be your cost of doing business, amortized into the price like any SaaS vendor's platform work — Fin does not bill customers when Anthropic swaps models under it. Position B (operator-realist): that logic holds for true Position-3 products at four-digit customer counts, where migration cost per customer rounds to zero; at productized-service scale, per-tenant re-baselining and per-niche eval work is genuine marginal labor, and hiding it in the base price either inflates the price for customers who churn before a migration or bankrupts the vendor who guessed the cadence wrong. The synthesis this course endorses: bundle *fleet-wide* platform work (control-plane upgrades, shared model migration) into the base price, and bill *tenant-specific* work (custom-source re-onboarding, customer-labeled re-baselines, Enterprise pins) as maintenance. The line between the two is exactly the line between your control plane and your config files, which is one more reason Layer 2's separation is worth being strict about.

## Runnable experiment — the second-customer drill and the deprecation fire drill

Allow 2 hours. Output: a delivery runbook skeleton and a tested migration procedure.

**Part 1 — Second-customer drill (60 min).** In Claude Code, working from your actual Week 4/5/8 build:

> *Here is my pipeline code and my Tuesday tier sheet. Produce: (1) a tenant config schema (YAML) that captures everything customer-specific for this package — sources/inputs, delivery, tier, model tier with a rate-card date, budgets, credential references (never values); (2) a delivery runbook as a numbered checklist from "signed" to "acceptance," with owner and target duration per step; (3) the list of everything in my current code that would have to change per customer — each item is either moved into the config schema or flagged as a scope defect.*

Then do the honest audit: for each flagged item, decide config-schema extension, exclusion-list addition, or (worst case) code refactor, and write the decision into the runbook.

**Part 2 — Deprecation fire drill (45 min).** Simulate the June-15 scenario:

> *Assume the model tier this package runs on gets a 60-day retirement notice today. Write the migration runbook: candidate replacement tiers with current published rates; the golden-set regression procedure per niche pack with pass thresholds; prompt-adjustment loop if regression fails; COGS recomputation (include a tokenizer-change factor as a parameter); customer notification per my disclosure clause; rollback condition. Then estimate hours per stage.*

Sanity-check the hour estimates against your real Week 8 eval runtime, not optimism.

**Part 3 — Price it (15 min).** Using Part 2's hours at your loaded rate, price your maintenance line two ways: bundled (added to monthly tiers) and separate (annual maintenance fee). Note which tenant-specific items fall outside both.

**Pass bar:** a stranger with your skills could, from the runbook alone, deploy customer #2 in ≤1 working day; the migration runbook has no step that says "figure out"; and the maintenance price covers Part 2's labor at your rate with margin, stated as a number.

## Problem set

1. **Blast-radius map.** For your package, list the five worst cross-tenant failure modes (credential leak, noisy neighbor, shared-prompt regression, migration gone wrong fleet-wide, one tenant's source getting your crawler IP blocked for everyone). For each: which plane's isolation prevents or contains it?
2. **Config-schema completeness.** Take your two most different imagined customers in the niche. Write both tenant YAMLs. Anything you could not express is either a schema gap (fix) or scope creep (refuse) — classify each.
3. **White-label teardown.** Price your package delivered via a Stammer-class platform: platform fee, usage markup, your price. Compare 12-month profit vs self-built at your Layer-4 COGS, *including* an honest estimate of your build-and-operate hours. Where is the crossover customer count?
4. **The pin negotiation.** An Enterprise prospect demands an indefinite pin to the current model version "for stability." Write your 5-sentence response, including what you will contract for (bounded pin, extended regression evidence) and what you will not, and the surcharge for the bounded pin.
5. **Deprecation math.** Using the H1-2026 Anthropic ledger, estimate migrations per 24 months for a package pinned to (a) a flagship tier, (b) a workhorse tier like Sonnet. Which pin is actually the stability play, and what does that imply for your default config?

## Reflection questions

- Which line of your current build would embarrass you if customer #2 signed tomorrow? That line is the real state of your delivery engineering.
- If your white-label platform (or model vendor) 10×'d prices next quarter, what is your migration time? Is that number acceptable, or is it a risk you are being paid to hold — and are you charging for it?
- Maintenance revenue rewards you when models churn. Does that misalign you with your customer's interest in stability, and does your bundled-vs-billed split fix the misalignment or hide it?

## Common failure modes at scale

- **The founder-shaped control plane.** Delivery "runbook" steps that only work with your undocumented judgment in the loop. Test: hand the runbook to Claude Code and see how far it gets before asking you something.
- **Credentials in prompts, configs, or repos.** One tenant's webhook URL pasted into a prompt template that ships fleet-wide. Secrets are references resolved at runtime, everywhere, always.
- **Per-tenant prompt patches.** The fastest, most invisible fork. Three tenants with "small" prompt tweaks means your next model migration runs three regression campaigns instead of one.
- **COGS computed once, at signing.** Rates are date-stamped and your workload grows with customer usage. Recompute monthly from actual token telemetry (your per-tenant budgets double as the meter), or discover the margin erosion at tax time.
- **Isolated tenants sold at pooled prices.** Saying yes to "we need our own instance" for a 15% premium. The premium for physical isolation is structural (it buys ongoing operational attention), commonly 2–3×, not cosmetic.
- **Migration as a surprise.** No maintenance line, no disclosure clause, then a 60-day deprecation notice lands and the work is unbilled, rushed, and invisible to the customer until something regresses. The wave was the warning; the next one is scheduled.

## My take (reviewer lens)

**Chip Huyen** would endorse the config-over-code spine and then push where it hurts: config-over-code degrades into *config sprawl* — a 300-key YAML schema is a programming language without tests — and the real discipline is keeping the schema small enough that every key is exercised by the golden set. She would also note this lesson under-weights data flywheels: the archive of briefs and customer edits accumulating per niche is the actual long-term moat, and tenancy design should treat that corpus (with consent) as a first-class asset, not exhaust. **Simon Willison** would go straight to the credential plane and say the lesson is right but not paranoid enough: a multi-tenant agent that *scrapes untrusted web content* holding *any* tenant credential is the lethal trifecta with a subscription model, and he would want per-tenant egress allowlists and output sanitization named as hard requirements, not implied by "least privilege" — one poisoned source page attempting exfiltration through your Slack delivery is a plausible Tuesday. He is right; add both to the runbook. **Karpathy** would squint at the upgrade-train ceremony from the other direction: for a ten-tenant package, canary batches and version trains can be cosplay of Google-scale ops — the leverage is in the regression harness being *fast and trusted*, so a migration is one command plus honest eval reading; if the harness is good, most of the process dissolves, and if it is bad, no process saves you. All three converge on the same center of gravity: the eval harness is the delivery architecture; everything else is scheduling.

## Further reading

**Must-read**

- Anthropic, *Model deprecations* (platform docs) — the ledger and the ≥60-day policy; read it as an operator's actuarial table.[^1]
- Anthropic, *Commitments on model deprecation and preservation* — what the vendor now promises, and where the burden still lands on you.[^2]
- [[02-tue-mcp-integration-patterns-for-unattended-agents|Week 8 Tuesday]] — the credential patterns this lesson multiplies by N.

**Recommended**

- Make, *Anthropic Claude model deprecations on June 15, 2026* — a platform's migration notice as a specimen of what you owe your own customers.[^3]
- Finout, *Claude Sonnet 5 Pricing 2026* — the cost-neutral-launch analysis behind Layer 4's corrections.[^8]
- Pickaxe, *9 White-Label AI Tools for Agencies (2026)* — the rental landscape for Layer 3's decision.[^5]

**Optional**

- endoflife.date's Claude tracker — third-party deprecation monitoring worth wiring into your alerting.[^10]
- AI for Anything, *Claude Model Deprecations June 2026: Migration Guide* — a worked community migration.[^11]

## Citations

[^1]: Anthropic, *Model deprecations*, Claude Platform Docs: deprecation/retirement ledger and ≥60-day notice policy for publicly released models; email + docs notification commitment. https://platform.claude.com/docs/en/about-claude/model-deprecations (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Anthropic, *Commitments on model deprecation and preservation* and *An update on our model deprecation commitments for Claude Opus 3*: Opus 3 retired January 5, 2026 as the first model under the new process; post-retirement availability on request. https://www.anthropic.com/research/deprecation-commitments ; https://www.anthropic.com/research/deprecation-updates-opus-3 (search-verified 2026-07-17)

[^3]: Make Help Center, *Anthropic Claude model deprecations on June 15, 2026*: platform-level migration documentation for the Opus 4.1 (and related) retirements; Opus 4 / Sonnet 4 notices April 14, 2026; Opus 4.1 notified June 5, retired June 15, 2026. https://help.make.com/anthropic-claude-model-deprecations-on-june-15-2026 ; https://developers.make.com/white-label-documentation/release-notes/anthropic-claude-model-deprecations-on-june-15-2026 (search-verified 2026-07-17)

[^4]: Stammer AI — white-label chat/voice agents under agency branding incl. client dashboards; ~$197/month platform cost; agency resale norms $300–$500/month per agent plus 3–5× usage markup. https://stammer.ai/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Pickaxe, *9 White-Label AI Tools for Agencies (2026)*: independent corroboration of Stammer-class economics and the wrapper-platform landscape. https://pickaxe.co/post/white-label-ai-tools-for-agencies (search-verified 2026-07-17)

[^6]: Trillet, *Top 10 White Label Voice AI Platforms for Agencies in 2026* and WotNot, *11 Best White Label AI Voice Agent Platforms*: voice-side reseller landscape; Voiceflow reseller plans custom-quoted with less turnkey client-management infrastructure. https://trillet.ai/blogs/top-10-white-label-voice-ai-platforms-for-agencies-2026 ; https://wotnot.io/blog/white-label-ai-voice-agent (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^7]: Anthropic, *Pricing*, Claude Platform Docs: Sonnet 5 intro pricing $2/$10 per M tokens through August 31, 2026, then $3/$15; also cross-checked in this vault's July 2026 master refresh report (binding cross-cutting theme #1, counts as one corroboration). https://platform.claude.com/docs/en/about-claude/pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: Finout, *Claude Sonnet 5 Pricing 2026: The Hidden Costs — and Real Savings — Behind the "Cost-Neutral" Launch*: intro-vs-standard rates and the ~30% tokenizer inflation on effective cost; corroborated by TechCrunch, *Anthropic launches Claude Sonnet 5 as a cheaper way to run agents*, June 30, 2026, https://techcrunch.com/2026/06/30/anthropic-launches-claude-sonnet-5-as-a-cheaper-way-to-run-agents/ . https://www.finout.io/blog/claude-sonnet-5-pricing-2026-the-hidden-costs-and-real-savings-behind-the-cost-neutral-launch (search-verified 2026-07-17)

[^9]: AI Made Tools, *Claude Sonnet 5 Pricing Explained: The Tokenizer Catch Nobody Mentions*: ~30% more tokens for the same text on the new tokenizer; effective-cost math. https://www.aimadetools.com/blog/claude-sonnet-5-pricing-explained/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^10]: endoflife.date, *Anthropic Claude*: third-party model lifecycle tracker (Claude 3.5 generation retired February 19, 2026; Claude 3 Haiku April 20, 2026; family-level retirement view). https://endoflife.date/claude (search-verified 2026-07-17)

[^11]: AI for Anything, *Claude Model Deprecations June 2026: Complete Migration Guide for Developers*: community migration guide; useful as a template for your own customer-facing migration notes. https://aiforanything.io/blog/claude-model-deprecation-migration-guide-june-2026 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
