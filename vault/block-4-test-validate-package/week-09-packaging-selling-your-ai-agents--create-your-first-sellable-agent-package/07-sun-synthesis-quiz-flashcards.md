---
type: lesson
block: block-4-test-validate-package
week: week-09
day_of_cycle: 7
day_name: sun
session_slug: create-your-first-sellable-agent-package
date_due: 2026-07-19
tags: [synthesis, quiz, flashcards, productization, packaging, pricing, distribution, review]
sources:
  - cheekypint-bret-taylor-2026
  - artisan-ava-2-launch-2026
  - anthropic-model-deprecations-docs
  - tropic-ai-credits
  - salesforce-isv-revshare
last_verified: 2026-07-17
---

# Week 9 Synthesis — a package is a promise engineered to repeat

## The one-sentence thesis of this week

A sellable agent package is a *scope-collapsed promise* — fixed buyer, fixed outcome, fixed price — backed by delivery engineering that makes customer #20 cost almost nothing, guarantees you can measure, channels chosen by evidence, and a price that survives the model market moving under it in both directions.

## The unifying frame: five documents, one truth

Everything this week produced is a projection of one config file:

- **Monday** decided *what* goes in the config: the build that survived the packageability rubric, with scope collapsed along four axes (input, output, integration, segment).
- **Tuesday** wrote the *promise* fields: outcome statement, inclusion/exclusion fences with routes, tier ladder, and a guarantee chosen by measurement-plus-volume (per-outcome, error-budget, or process).
- **Wednesday** wrote the *delivery* fields: tenancy planes, config-over-code, the golden build with upgrade trains, COGS at date-stamped rates, and maintenance priced against a real deprecation cadence.
- **Thursday** chose where the config gets *seen*: one controlled channel, one rented rail, both with CAC math and kill criteria — marketplaces as procurement rails, never demand springs.
- **Friday** attached the *number*: a value metric that passes the physics test (measurable, buyer-legible, volume-appropriate), anchored to the labor line, capped against surprise, grandfathered by window not by forgetfulness.
- **Saturday** compiled it all: `package.yaml` → calculator → six documents → the stranger test.

The week's deepest single lesson hides in the calculator's output: at productized-service scale, **support hours dominate COGS, not tokens**. The margin-protection technology is the exclusion fence and the runbook, which is why the "soft" documents are the hard engineering.

## Where each day's content goes forward

- Monday's spectrum reappears in Week 11 when you validate whether the *idea* deserves more product investment — the agency-vs-product fork is re-decided with evidence there.
- Tuesday's one-pager and tier sheet become Week 10's landing page and pricing section nearly verbatim.
- Wednesday's config schema is the substrate for every future package; the migration runbook fires for real at the next deprecation notice (calendar it).
- Thursday's channel triggers get their quarterly review; the 10-customer plan starts Monday.
- Friday's calculator gets re-run on September 1, when the Sonnet 5 intro rate expires and your baseline becomes the `intro_expiry` scenario.

## The week's key moves — the mental-move table

| Situation | The move | From |
|---|---|---|
| "Can you also add…?" | Route it: tier, add-on, or reasoned no — never an improvised yes | Tue |
| "Guarantee it works" | Choose Position A/B/C by measurement + volume; never accuracy adjectives | Tue |
| Second customer signs | Tenant YAML from intake; zero code edits; runbook clock starts | Wed |
| Deprecation email arrives | Migration stage: candidates → per-pack regression → COGS recompute → notice → staged rollout | Wed |
| "Are you on [marketplace]?" twice in a quarter | That rail just crossed from hope to channel; do the readiness audit | Thu |
| Choosing a price metric | Physics test: disputable? buyer-controlled? volume-sufficient? | Fri |
| Model price moves ±20%+ | Symmetric materiality band activates; date-stamped rate card is the evidence | Fri |
| Sales page feels weak | Add specificity (numbers, fences, provenance), never promises | Sat |

## 15 quiz questions

**Q1.** Name the four positions on the productization spectrum and the variable that changes most fundamentally between them.

**Q2.** Artisan's Ava 2.0 relaunch cut entry pricing from $2,500/month to what, and what delivery-engineering fact makes that price viable for Artisan but a trap for a first-time packager?

**Q3.** What are the four axes of scope collapse, and for each, give the "custom" and "packaged" version in one phrase?

**Q4.** The 2026 forward-deployed-engineering wave (AWS's $1B unit, etc.) is cited as evidence for which side of which controversy? State the strongest counter-position in one sentence.

**Q5.** In the Perspective AI heuristic, what deployment statistic signals "the problem is product, not go-to-market"?

**Q6.** Describe the three guarantee positions for probabilistic systems (A/B/C) and the decision variable that selects among them.

**Q7.** How does Sierra's pricing embed its guarantee? What happens commercially when Sierra's agent escalates to a human?

**Q8.** Which three things should *never* vary across tiers, and why does each poison the business if tiered?

**Q9.** Name the three planes of multi-tenant architecture and state which one is never shared and which one is always shared.

**Q10.** In H1 2026, Anthropic retired or noticed at least five model families. Give two entries from that ledger and state the minimum notice policy — then name the commercial product this fact justifies.

**Q11.** Compute: a run consumes 220K input + 18K output tokens on Sonnet 5 intro pricing ($2/$10 per M). What does one run cost, and roughly what per month at 22 runs? What single COGS line dwarfs this at productized-service scale?

**Q12.** What take rate does Salesforce charge ISVs on AgentExchange, and what did Anthropic's Claude Marketplace charge at launch? What does each platform's rate reveal about its business model?

**Q13.** Why did this course classify the GPT Store as a cautionary tale for package distribution? Name the three mechanisms by which marketplaces *do* convert when they convert.

**Q14.** State two quantitative pieces of evidence for the 2026 usage-based pricing backlash, and the four package-design rules derived from it.

**Q15.** Your Standard tier is $1,500/month; a customer demands $1,100. Per Friday's discounting discipline, what are the two acceptable responses, and what is the forbidden one?

## Answers

**A1.** Custom service → productized service → product → platform. The fundamental variable: marginal delivery cost (your hours per additional customer), falling from ~all of them to hosting-plus-support to a take rate on others' work.

**A2.** $250/month (May 2026, with $300 free credits, sub-10-minute self-serve onboarding). It works because no human at Artisan touches a $250 account — the price is downstream of self-serve delivery engineering; adopting the price without that engineering means founder-hours delivered at product prices.

**A3.** Input (any source → supported-source list), output (custom formats → one fixed-schema artifact), integration (any system → one or two named channels per tier), segment (anyone who pays → one niche whose customers configure alike).

**A4.** Evidence for "every deployment is a snowflake" (against productized packages). Counter: snowflake-ness is a function of integration surface and outcome ambiguity — you *choose* it when you choose scope; narrow, well-collapsed packages (Fin, Ava) demonstrably deploy without embedded engineers.

**A5.** More than 30–40% of deployments requiring significant forward-deployed effort.

**A6.** A: price the guarantee in (charge only on success; needs countable events and volume). B: engineer it (statistical SLOs, error budgets, drift clauses; needs a production eval harness and a sophisticated buyer). C: guarantee the process (delivery, instrumentation, remediation velocity, exit) while declining per-item accuracy numbers. Decision variable: measurement quality × event volume.

**A7.** The guarantee is the price: a pre-negotiated rate per autonomous resolution, and escalation to a human is free — failure costs the customer nothing, so accuracy disputes convert into billing arithmetic.

**A8.** Core output quality (a degraded Starter is your marketing, seen first), security/credential posture (uniform or breached), and metric definitions (forked definitions mean per-tenant billing code forever).

**A9.** Control plane (always shared — one codebase, one version), data plane (the real choice: shared-with-isolation default, physical isolation as a priced Enterprise variant), credential plane (never shared; per-tenant secrets namespaces resolved by reference at runtime).

**A10.** Any two of: Opus 3 retired Jan 5; Claude 3.5 generation retired Feb 19; Claude 3 Haiku retired Apr 20; Opus 4/Sonnet 4 notices Apr 14; Opus 4.1 notified Jun 5, retired Jun 15. Policy: ≥60 days' notice for publicly released models. Justified product: the maintenance contract (model migration + eval re-baseline as a billable line, ~15–25% of annual package value or bundled into Standard+).

**A11.** (0.22M × $2) + (0.018M × $10) = $0.44 + $0.18 = **$0.62/run**; ≈ **$13.60/month** at 22 runs. The dominating line: support hours at a loaded rate (e.g., 45 min at $150/h = $112.50 — ~8× the inference bill).

**A12.** Salesforce: 15% Percentage Net Revenue for ISVs (25% OEM). Anthropic: 0% at Claude Marketplace launch. Salesforce monetizes the distribution rail itself; Anthropic monetizes the tokens underneath and uses the marketplace to make Claude the enterprise default.

**A13.** Millions of listings produced near-zero documented builder revenue, and OpenAI itself pivoted its energy to the apps program (which still bars digital-goods monetization). The three converting mechanisms: budget capture (drawing down committed cloud/AI spend), procurement compression (pre-cleared security/contracts), and platform co-sell. All presuppose demand generated elsewhere.

**A14.** Evidence (any two): 78% of IT leaders report unexpected charges under consumption/AI pricing (Tropic); 90% of CIOs cite cost forecasting as their top AI challenge (Zenskar's CFO guide); the Copilot AI-credits developer backlash. Rules: bill in buyer-legible units (keep tokens/credits internal); every variable component gets a cap and an alert; prefer prepaid commitments; publish the floor, negotiate the ceiling.

**A15.** Acceptable: discount *duration* (e.g., two months free on annual prepay) or shrink the *package* (drop to Starter / remove a source pack). Forbidden: cutting the number itself — a repeated price in a talking niche becomes the real price.

## 30 flashcards

1. **Q:** Four positions on the productization spectrum? **A:** Custom service → productized service → product → platform.
2. **Q:** Scope collapse? **A:** Shrinking a build's promise along input/output/integration/segment axes until delivery repeats without rebuilds.
3. **Q:** The 2026 productized-retainer price band (agency guides, directional)? **A:** ~$1,500–$4,500/month per client.
4. **Q:** Artisan Ava 2.0 entry price and date? **A:** $250/month, May 2026 (10× cut from $2,500).
5. **Q:** Harvey's scale by early 2026? **A:** ~$190M ARR (Jan 2026), $11B valuation (Mar 2026), 100K+ lawyers.
6. **Q:** Sierra's pricing model? **A:** Pre-negotiated fee per autonomous resolution; escalation free; ~$150M+ ARR at $15.8B valuation (May 2026).
7. **Q:** FDE 30–40% heuristic? **A:** If >30–40% of deployments need significant forward-deployed effort, it's a product problem, not go-to-market.
8. **Q:** AWS's June 30, 2026 FDE announcement? **A:** $1B into a unit embedding engineers with customers.
9. **Q:** Outcome statement format? **A:** [Named buyer] gets [specific outcome] within [time], measured by [metric], or [consequence].
10. **Q:** Why is the exclusion list "the product"? **A:** It's the fence that stops N customers converting the package back into N custom engagements; every exclusion carries a reason and a route.
11. **Q:** Six tier variables worth moving? **A:** Volume of the value metric, integration surface, quality instrumentation (eval report), support/change velocity, commercial terms, exclusivity.
12. **Q:** Three never-tier variables? **A:** Core output quality, security posture, metric definitions.
13. **Q:** Fin's pricing anatomy? **A:** $0.99 per resolution; standalone base $49/month including 50 resolutions — floor pays for pipes, variable scales with value.
14. **Q:** Fin's 2026 corporate event? **A:** Salesforce agreed to acquire Fin (ex-Intercom) for ~$3.6B, June 15, 2026.
15. **Q:** Guarantee Position A / B / C? **A:** A: charge only on success; B: statistical SLOs + error budgets + drift clauses; C: process guarantees (delivery, instrumentation, remediation, exit) without per-item accuracy.
16. **Q:** MavenAGI's SLA rule? **A:** Don't put accuracy in a contract you can't measure consistently; run internal SLOs before customer promises.
17. **Q:** Model-change disclosure clause? **A:** Notify customers of material model swaps; re-run the golden set across every swap; results in the next eval report.
18. **Q:** Three tenancy planes? **A:** Control (always shared), data (isolation is the priced choice), credential (never shared; per-tenant secrets by reference).
19. **Q:** Config-over-code law? **A:** Customer difference lives in config; behavior lives in one versioned golden build with upgrade trains gated by per-niche regression.
20. **Q:** White-label economics (Stammer-class)? **A:** ~$197/month platform; agencies resell at $300–$500/month/agent + 3–5× usage markup.
21. **Q:** H1-2026 Anthropic deprecation ledger (any three)? **A:** Opus 3 (Jan 5), Claude 3.5 gen (Feb 19), Claude 3 Haiku (Apr 20), Opus 4/Sonnet 4 notices (Apr 14), Opus 4.1 (Jun 15); ≥60-day notice policy.
22. **Q:** Maintenance-contract split? **A:** Bundle fleet-wide platform work into base price; bill tenant-specific work (custom re-onboarding, customer-labeled re-baselines, pins) as maintenance.
23. **Q:** "Niche Radar" Standard-tier COGS shape? **A:** ~$13.60/month inference (Sonnet 5 intro) vs ~$112.50 support (45 min loaded) — support dominates.
24. **Q:** Sonnet 5 pricing timeline? **A:** $2/$10 per M intro through Aug 31, 2026; then $3/$15; new tokenizer ≈ +30% tokens per text.
25. **Q:** AgentExchange scale + take rate? **A:** ~14,000 listings after the April 2026 AppExchange/Slack merger; 15% ISV / 25% OEM revenue share.
26. **Q:** Claude Marketplace's launch model? **A:** March 6, 2026, limited preview; curated partners (Snowflake, GitLab, Harvey…); purchases against Anthropic spend commitments; zero take rate.
27. **Q:** Three mechanisms that make marketplaces convert? **A:** Budget capture, procurement compression, platform co-sell — all presuppose externally generated demand.
28. **Q:** Value-metric physics test? **A:** Measurable without dispute; buyer believes they control it; scales with value at your actual volume.
29. **Q:** Usage-backlash headline stats? **A:** 78% of IT leaders hit unexpected consumption charges (Tropic); 90% of CIOs rank cost forecasting their top AI challenge (Zenskar).
30. **Q:** Grandfathering rules? **A:** Date-stamp rate cards; grandfather by window (6–12 months), not forever; absorb inside a ±20% materiality band, pass through symmetrically outside it; never grandfather the metric.

## Where you'd still lose points (reviewer lens)

The week's honest gaps, named so the live session can attack them: (1) **No real buyer touched anything.** Every artifact passed Claude personas, not humans; Seibel's correction stands — the folder's first real test is Monday's ten sends. (2) **The revenue evidence for the middle of the market is directional**, drawn from agency guides and surveys rather than audited books; treat the $1.5K–$4.5K band as a hypothesis your niche must confirm. (3) **Support-hour estimates are the load-bearing guess** in every margin claim this week made; instrument your actual hours from customer #1 or the whole matrix is theater. (4) **The channel landscape is mid-shift** — AgentExchange's merger is three months old, Claude Marketplace is in preview, and the agent-as-buyer thesis (swyx's point) could reorder Thursday within a year. Re-verify before quoting any of it in a sales conversation past September.

## Further reading for the week's gaps

- Bret Taylor's outcome-pricing interviews — re-listen after your first three sales calls, not before.
- Anthropic's deprecation page + endoflife.date's Claude tracker — subscribe; your migration stage has a real trigger coming.
- Tropic's credit-pricing interrogation — the buyer-side questions to keep passing quarterly.

_last_verified: 2026-07-17_
