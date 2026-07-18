---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 6
day_name: sat
session_slug: create-your-first-sellable-agent-package
date_due: 2026-07-18
tags: [build-day, agent-package, one-pager, tier-sheet, onboarding, runbook, eval-report, pricing-calculator, demo-script, code-lab]
sources:
  - artisan-ava-2-launch-2026
  - intercom-fin-pricing-2026
  - cheekypint-bret-taylor-2026
  - anthropic-sonnet-5-pricing
  - anthropic-model-deprecations-docs
  - tropic-ai-credits
  - salesforce-isv-revshare
  - aws-agents-tools-launch-2025
  - mavenagi-ai-sla-glossary
last_verified: 2026-07-17
word_count_target: 5000
---

# Build day — your first sellable agent package, end to end, with the calculator to prove the margins

## Why this matters

Today you ship the package. Not the agent — you built that in Weeks 4–8 — but the *commercial artifact* that lets a stranger evaluate, buy, and receive it: a one-pager, a tier sheet, an onboarding checklist, a delivery runbook, an eval-report template, a stress-tested pricing model, and a five-minute demo script with the price said out loud. This is the week's thesis made physical: the difference between "I can build agents" and "I sell an agent package" is a folder of documents that all agree with each other. The pass bar is unambiguous: **a competent stranger, given this folder, could buy the package, and a competent peer, given this folder, could deliver customer #2.** Everything else is decoration.

The build is assembly, not invention. Monday chose the build and collapsed its scope. Tuesday drafted the promise. Wednesday engineered delivery. Thursday picked channels. Friday priced it. If any of those artifacts is missing, today's first hour is spent making its minimum version — the week was designed so that skipping a day surfaces here, not in front of a customer.

## Prerequisites

- Your Monday-through-Friday drafts (candidate + collapse lists, tier sheet, runbook skeleton, two-channel plan, chosen pricing structure).
- The [[06-sat-rag-evaluation|Week 4 eval harness]] or [[05-fri-reliability-engineering-for-unattended-agents|Week 8 golden-set]] machinery for your build — the eval-report template assumes one exists.
- A 3–4 hour uninterrupted block. Claude Code open. `code-lab/06-agent-package/` from this folder.

## The deliverable set, and the order to build it

Build in this order, because each artifact feeds the next:

```
package.yaml  →  pricing (calculator)  →  one-pager + tier sheet
     →  onboarding checklist + runbook  →  eval-report template  →  demo script
```

### Stage 1 — `package.yaml`: the single source of truth (45 min)

The code-lab's design principle is the week's Wednesday principle: **config over prose**. Every fact about your package — outcome statement, labor line, tiers, exclusions with routes, guarantees with consequences, onboarding steps with owners and clocks, runbook stages, the verbatim pricing sentence — lives in one YAML file, and every customer-facing document is *generated* from it. When the package changes (it will: tier prices, source counts, guarantee language), you change one file and regenerate, instead of discovering in month four that your one-pager promises 12 sources while your tier sheet says 10.

```bash
cd code-lab/06-agent-package
cp package.example.yaml package.yaml
# edit every CHANGE-ME; keep the structure
```

The example config is the week's running "Niche Radar" package, fully worked. Do not keep any example value you cannot personally defend: the point of the exercise collapses if your labor line is someone else's fiction. Fill the economics block from your real Week 4/5/8 telemetry where you have it (token counts per run measured on a current-tokenizer model), and from honest estimates where you don't — then mark estimates with a comment, because Stage 2 will show you which ones matter.

In Claude Code, the fastest honest path:

> *Here is my Tuesday tier sheet, Wednesday runbook skeleton, and Friday pricing choice [paste]. Populate package.yaml in this schema [paste example]. Flag every field where my drafts disagree with each other, and every field you had to invent — inventions become my TODO list, not silent defaults.*

The disagreement list is the real output. A package whose tier sheet, guarantee, and runbook disagree is three documents wearing a trench coat.

### Stage 2 — Run the pricing calculator, and believe it (30 min)

```bash
python pricing_calculator.py package.yaml
```

You get two tables: baseline economics per tier (inference, support, fixed, margin, with the labor-line anchor printed above them) and the Friday stress matrix (baseline / intro-expiry / flagship-migration / price-war / bad-month), with any cell under the 70% pass bar flagged.

Read the example package's output before your own, because it teaches the week's most counterintuitive numerical lesson. For "Niche Radar" Standard at $1,500: inference is **$13.64/month** at Sonnet 5 intro rates,[^4] support at a modest 45 min/month is **$112.50**, and the stress matrix barely moves under the August 31 intro expiry (91.1% → 90.7%) or even a forced flagship migration (→ 87.5%) — but the *bad-month, doubled-support* scenario breaks the Starter tier (68.0%, below bar). The margin risk in a productized-service package at your scale is not the token line everyone obsesses over; it is *your hours*, which is why Tuesday's exclusion fences and Wednesday's runbook are the actual margin-protection technology, and why the calculator prices support at a loaded rate instead of pretending founder time is free.

Now run yours. For every flagged cell, make one of the three moves (reprice, cut COGS, restructure) *in the YAML*, and re-run until the matrix clears. Then do the README's "modify one thing": double `support_hours_per_customer_per_month` and see what breaks. If nothing breaks, your support estimate was probably already padded; if Starter breaks (it usually does), write the sentence you will use to keep Starter customers inside the email-only support fence.

### Stage 3 — Generate and edit the document set (60 min)

```bash
python package_spec.py package.yaml --out out/
```

Six files land in `out/`. The generator gives you honest scaffolding; your hour goes into making three of them excellent:

**The one-pager** (`one_pager.md`). Generated structure: outcome statement → labor-line math → tiers → promises with consequence → exclusions with routes → onboarding terms. Edit for voice, not structure — the structure encodes the week (the exclusions section *on the sales page* is deliberate: buyers burned by agent-washing read "what this is not" as competence, and it pre-empts the scope-creep conversation before the first call). Test: hand it to someone who knows nothing about your week and ask them to tell you (a) what they'd get, (b) what it costs, (c) what happens when it fails. Three correct answers or keep editing.

**The delivery runbook** (`delivery_runbook.md`). The generator emits Wednesday's stages each with five empty fields: owner, inputs, procedure, failure mode + response, evidence of completion. Fill every field for at least the onboarding and monthly-operations stages today; the model-migration stage can carry Wednesday's fire-drill output pasted in. The forbidden phrase in a procedure field is "figure out." Where you catch yourself writing it, you have found either a missing tool or a missing decision, and it goes on the TODO list with a date.

**The eval-report template** (`eval_report_template.md`). Note the **provenance block** at the top — golden-set size, sampling method, refresh date, judge-alignment number. That block exists because an eval report without provenance is marketing with a table in it (Tuesday's reviewer lens, applied). Wire the template's metrics to your actual harness: if a row in the results table has no data source in your current instrumentation, either build the instrument this month or delete the row. A template that promises metrics you don't collect is a future incident report.

The other three (tier sheet, onboarding checklist, demo script) need only light editing if your YAML was honest.

To calibrate what "filled" means for a runbook stage, here is the monthly-operations stage of the running example, done:

> **Stage 6 — Monthly: eval report, COGS telemetry, config-change window.**
> *Owner:* you (delivery), until a contractor inherits this document.
> *Inputs:* the month's per-tenant token telemetry, eval harness results per niche pack, incident log, pending config-change requests.
> *Procedure:* (1) First business day: run the regression job per niche pack; export results into the eval-report template per Standard+ tenant. (2) Reconcile each tenant's token usage against its budget; flag any tenant over 80% for a cap conversation before it becomes an overage argument. (3) Fill the provenance block (set version, last refresh date, judge-alignment number) from the harness metadata, never from memory. (4) Send reports by the 5th; log send timestamps. (5) Process config changes in one batch inside the published window; regenerate affected tenant YAMLs; run per-tenant smoke delivery. (6) Update `pricing_notes.md` if any COGS line moved more than 10% month-over-month, and diagnose why.
> *Failure mode + response:* regression job fails or a metric breaches threshold → the Tuesday drift clause's clock starts; customer notification per disclosure policy; fix-forward before the next scheduled delivery.
> *Evidence it completed:* six report send-timestamps, telemetry reconciliation sheet, updated notes file, all dated in the ops log.

Notice the texture: named inputs, numbered steps, one explicit clock, one escalation path, and a paper trail. Every stage in your runbook should read like that by the time a contractor, or an agent, inherits it.

### Stage 4 — The demo script, rehearsed out loud (30 min)

The generated `demo_script.md` structures five minutes: pain in their words (30s) → the artifact with a clickable source link (60s) → one day in the customer's life (60s) → the eval report as trust evidence (60s) → **the pricing sentence, verbatim, then silence** (45s) → the close with a same-day next step (45s). Plus three rehearsed objection lines: the cheaper-tool objection (answered with Friday's defended-delta doctrine, not discounting[^1]), the guarantee objection (answered with measured promises, not adjectives[^8]), and the excluded-feature request (answered with the route, never an improvised yes).

Rehearse it out loud twice, timed. The pricing sentence gets rehearsed until it comes out flat and unhurried; Friday's cohort-peer lens was right that no spreadsheet builds this muscle. If you have a willing peer from the cohort, deliver it once over a call and collect exactly two notes: where they got bored, and whether they could repeat the price and what it buys.

### Stage 5 — The stranger test: assemble and audit (30 min)

Assemble the folder: `out/` documents + the stress-matrix output pasted into a `pricing_notes.md` + your two-channel plan from Thursday. Then run the pass-bar audit in a *fresh* Claude conversation (fresh matters: no context sympathy):

> *You are two people. First, a [niche] operations lead with budget who has never met me: reading only these documents, would you buy, and what stops you? List every question the documents fail to answer. Second, a competent AI engineer who has never seen this project: using only the runbook and config, walk me through delivering customer #2 — name the first step where you'd be stuck.*

**The pass bar, as a checklist:**

1. ☐ One-pager answers what/for-whom/how-much/what-if-it-fails without a call
2. ☐ Every tier's margin ≥70% across the stress matrix, support priced at loaded rate
3. ☐ Every guarantee names metric, cadence, and consequence; none is unmeasurable
4. ☐ Every exclusion has a route (tier, add-on, or no)
5. ☐ Onboarding checklist has owner + day for every step; time-to-first-value ≤ 3 days
6. ☐ Runbook's onboarding + monthly stages have zero "figure out" steps
7. ☐ Eval-report template's every metric maps to an existing instrument (or a dated TODO)
8. ☐ Model tier + rate date live in the config; migration stage exists with a rollback condition
9. ☐ Demo script rehearsed; pricing sentence delivered without flinch, twice
10. ☐ The stranger persona's "would you buy?" produced a yes, a conditional yes with named conditions, or a no whose reasons you can fix without rebuilding the agent

Eight of ten today is a pass with homework. Fewer means the gap is almost certainly in one of Monday/Tuesday/Friday, and the audit output tells you which day to redo tomorrow morning before the live session.

## Extending the calculator: make the scenarios yours

The shipped stress matrix covers the four 2026-shaped scenarios from Friday, but your package has risks the defaults cannot know. The `scenarios()` function in `pricing_calculator.py` is deliberately boring so you can extend it in five lines. Two extensions worth making today if they fit your shape:

**A volume-shock scenario** for customer-driven workloads (the voice-receptionist shape from Tuesday's transfer check, where calls arrive on the customer's schedule, not yours):

```python
# inside scenarios(), after the existing entries:
out["volume_2x"] = [
    tier_economics(cfg, {**t, "run_scale": float(t.get("run_scale", 1.0)) * 2.0})
    for t in cfg["tiers"]
]
```

**A churn scenario is the wrong instinct** (churn hits revenue, not tier margin, and this calculator models margin); the right second extension is a *fixed-cost shock*: triple `hosting_usd_per_month_fleet` and halve `expected_fleet_size_for_hosting_split` in a copied config to model the month where you have three customers and real infrastructure. Run it. The result usually argues for keeping infrastructure embarrassingly minimal until customer five, which is a conclusion worth having a printout of when the urge to "build the platform properly" strikes.

Two rules when extending: every scenario must correspond to an event you can name (a dated price change, a plausible customer behavior, a competitor move), and every scenario that fails the pass bar must produce a written response in `pricing_notes.md`, exactly like the shipped four. A stress matrix you cannot act on is a mood board with percentages.

While you are in the code, notice what the calculator deliberately does not model: discounts (Friday's rules forbid the interesting ones), taxes and payment fees (add ~3–4% if you want realism), and your own opportunity cost. The last one is the honest gap in every solo-operator margin model. If four hours of support at $150 "loaded rate" displaces four hours of selling that would have closed a $1,500/month customer, the true cost of those hours is not $600. The calculator prices your time at replacement cost; your calendar prices it at opportunity cost; when the two diverge badly, that is the signal to hire the first delivery contractor, and the runbook you wrote today is their onboarding document.

## What to bring to the live session tomorrow

The Sunday live session ("Create: Your First Sellable Agent Package") works best if you arrive with specific, disagreement-shaped material rather than a polished pitch. Bring:

1. **The one-pager, printed or shared**, plus the two hardest questions your stranger-persona audit produced. These are your office-hours questions, per the course's standing protocol.
2. **The stress matrix output**, with the cell that scared you highlighted, and your written response to it. Cohort comparison of *which tier breaks first* across different package shapes is the single highest-value fifteen minutes available tomorrow: scheduled-artifact packages break on support, conversational packages break on volume, and seeing both cures you of overfitting to your own shape.
3. **Your pricing sentence, rehearsed**, because the session's most useful ritual is saying it to a peer who is contractually obliged not to nod politely. Swap one-pagers with a cohort peer and each attempt to find the free-custom-work seam in the other's exclusion list. The seam a stranger finds in three minutes is the seam a customer will find in week three, when it is no longer free to fix.
4. **One honest unknown.** The week generated estimates (support hours, close rates, template-surface yield) that only contact with reality can settle. Name your biggest one out loud; the cohort's operators who are a few weeks ahead on their own packages are the best available data source for it, and asking is cheaper than finding out on your own book.

## What you have when you're done

A folder that is, functionally, a business: the same seven artifacts that Artisan's pricing page, Fin's outcome definitions, and Sierra's resolution contracts are the venture-scale versions of.[^1][^2][^3] Next week (Week 10, pending generation) builds the landing page and launch creatives *from* this folder — the one-pager becomes the page, the demo script becomes the video, the tier sheet becomes the pricing section. Week 11 validates the idea against real users before you over-invest. Nothing you made today is wasted even if the package pivots: the calculator, the config schema, and the runbook discipline transfer to every package you ever ship.

And one deliberate echo: you have now productized *yourself* through the same pipeline you productized the agent. Scope collapsed, promise written, delivery runbooked, price defended. The uncomfortable question Monday asked — "what does a package stop selling?" — has today's answer: nothing, if the package is the floor and your judgment is the Enterprise tier.

## Common failure modes on build day

- **Polishing the agent instead of the package.** The urge to refactor the pipeline "before it's sellable" is procrastination in an engineer costume. Today's artifacts sell the build you have; the buyer for whom it isn't good enough yet is a persona in your head, not a document in the folder.
- **Example-value laundering.** Shipping the Niche Radar labor line ($990) or token counts in *your* package because editing YAML felt like admin. Every number you didn't derive is a number a buyer's first hard question detonates.
- **The support-hours lie.** Entering 0.25 hours/month because you want the matrix green. The calculator prices founder time precisely because the fantasy of free support is how packages die at customer eight; enter what last month actually cost you.
- **Prose drift.** Editing the generated one-pager's *facts* (a price, a source count) instead of the YAML, so the documents immediately disagree again. Facts live in config; only voice lives in the editor.
- **Guarantee inflation at the last minute.** Adding "99.9%" or "money-back" during Stage 3 polish because the page felt weak. Weak pages are fixed with specificity, not with promises Tuesday's counsel persona never reviewed.
- **Skipping the out-loud rehearsal.** Reading the demo script silently and calling it rehearsed. The flinch on the pricing sentence is only audible out loud, and buyers hear it even on video calls.

## Reflection questions

- Which single artifact took you longest, and is that because it was hardest or because it was the one that made the business real?
- The stress matrix said support hours, not tokens, are your margin risk. What would have to be true of your runbook for support to *halve* instead of double as customers grow?
- If you had to hand this folder to a stranger and take 20% of revenue while they delivered, would the folder survive? What breaks first — and is that a document problem or a business problem?
- What in this package would you refuse to change even if the first three prospects all pushed on it? That refusal is your actual positioning.

## My take (reviewer lens)

**Jeremy Howard** would bless the pedagogy and flag the sequencing risk: a week that ends in a beautiful artifact can teach artifact-production instead of the underlying judgment, and the tell is a student who can regenerate the folder but cannot say *why* Starter breaks under doubled support in one sentence. His fix, which this lesson adopts: the calculator's example output is walked through *before* the student's own, precisely so the causal story (support dominates COGS at productized-service scale) is learned from a case, not memorized from a matrix. **Boris Cherny** would read the runbook stages with fleet eyes and note that everything here is designed for one operator and ten tenants — fine — but would insist the "evidence it completed" field is the one that scales: an operator who logs evidence per stage can hand the fleet to an agent (or an employee) later; one who doesn't has built a business only they can run, which was the disease this week claimed to cure. **Michael Seibel** gets the last word he has earned all week: "This is the best possible Saturday *if* Monday you send the one-pager to ten real humans. The folder is not the milestone. The first reply is." He is right, and Thursday's 10-customer plan is already sitting in the folder with activities that start without anyone's permission. Send it.

## Further reading

**Must-read**

- Your own `out/` folder, read cold tomorrow morning before the live session. Nothing on this list outranks it today.
- Artisan's pricing page and Fin's outcome documentation — the two best public specimens to diff your one-pager against: one self-serve flat-plus-credits, one base-plus-outcome.[^1][^2]

**Recommended**

- Bret Taylor on outcome pricing — re-listen *after* your matrix run; his volume conditions will land differently now.[^3]
- Anthropic's model-deprecation docs — calendar the check; your runbook's migration stage has a real trigger date coming.[^5]
- [[06-sat-build-the-weekly-report-generator|Week 5 Saturday]] and [[06-sat-build-the-hybrid-scraper-summarizer|Week 8 Saturday]] — the builds this package wraps; revisit their eval sections when wiring the report template.

**Optional**

- Tropic's credit-pricing interrogation — run it against your own tier sheet one more time as a buyer would.[^6]
- The AgentExchange ISV terms and AWS agents-category listing docs — when Thursday's triggers fire, these are the forms you'll fill.[^7][^9]

## Citations

[^1]: Artisan, *Artisan launches Ava 2.0* (May 2026): $250/month self-serve entry, credit-based usage; the anchor your one-pager's defended delta is written against. https://www.artisan.co/blog/artisan-launches-ava-2-0-the-first-autonomous-ai-bdr-now-self-serve ; https://www.artisan.co/pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending; canonical teardown in Week 4 Monday)

[^2]: Intercom, Fin pricing and outcome definitions ($0.99/outcome; $49 base incl. 50 resolutions standalone): the specimen for billable-event definition. https://www.intercom.com/help/en/articles/8205718-fin-ai-agent-outcomes ; https://www.dragapp.com/blog/intercom-pricing/ (search-verified 2026-07-17)

[^3]: Bret Taylor, *AI agents, outcome-based pricing, and the OpenAI board* (A Cheeky Pint / Sierra): outcome pricing's logic and its volume preconditions. https://cheekypint.substack.com/p/bret-taylor-of-sierra-on-ai-agents (search-verified 2026-07-17)

[^4]: Anthropic, *Pricing*, Claude Platform Docs: Sonnet 5 $2/$10 intro through 2026-08-31, then $3/$15; the calculator's rate card mirrors this with dates. https://platform.claude.com/docs/en/about-claude/pricing (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^5]: Anthropic, *Model deprecations*, Claude Platform Docs: ≥60-day retirement notices; the trigger for the runbook's migration stage. https://platform.claude.com/docs/en/about-claude/model-deprecations (search-verified 2026-07-17)

[^6]: Tropic, *What Is a Credit? Understanding AI Usage-Based Pricing*: the procurement interrogation your pricing must pass. https://www.tropicapp.io/blog/what-is-a-credit-ai-pricing (search-verified 2026-07-17)

[^7]: Salesforce Developers, AppExchange/AgentExchange revenue-share terms (15% ISV / 25% OEM PNR). https://developer.salesforce.com/docs/atlas.en-us.packagingGuide.meta/packagingGuide/appexchange_checkout_rev_share.htm (search-verified 2026-07-17)

[^8]: MavenAGI, *AI Service Level Agreement (SLA)*: measured guarantees only; the demo script's guarantee objection line paraphrases this discipline. https://www.mavenagi.com/glossary/ai-service-level-agreement (search-verified 2026-07-17)

[^9]: AWS, *Listing SaaS API-based AI agent products*, AWS Marketplace docs — the listing mechanics behind Thursday's readiness audit. https://docs.aws.amazon.com/marketplace/latest/userguide/listing-saas-ai-agents.html (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
