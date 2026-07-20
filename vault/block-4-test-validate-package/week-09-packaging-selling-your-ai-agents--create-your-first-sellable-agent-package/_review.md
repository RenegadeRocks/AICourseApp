---
type: review
phase: 2
week: week-09
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 9 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-4-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-09-briefs.md`.

Mechanical checks run this session: `python -m py_compile` on all three code-lab modules (pass, incl. after edits); `pricing_calculator.py` executed against `package.example.yaml` — **every number the lessons quote reproduces exactly** (baseline Standard 91.1%, intro-expiry 90.7%, flagship 87.5%, price-war 85.2%, doubled-support 83.6%, Starter 68.0% under doubled support, $28,750/mo at 15 customers); `package_spec.py` generates all six documents cleanly; **all 15 distinct wikilink targets resolve** to real vault files (verified by script); em-dash density and contrast-tic scans per file; WebSearch spot-checks on the four most load-bearing 2026 facts, each corroborated by ≥2 independent domains — Salesforce/Fin $3.6B on June 15, 2026 (salesforce.com press release + techcrunch.com + cnbc.com), AWS $1B FDE unit on June 30, 2026 (cnbc.com + techcrunch.com + aboutamazon.com), Artisan Ava 2.0 at $250/month self-serve May 2026 (artisan.co + tomba.io + producthunt.com), Claude Marketplace zero take rate March 6, 2026 (siliconangle.com + techzine.eu + venturebeat.com). WebFetch egress-blocked, so no liveness pass on URLs; the lessons flag this per-citation, which is the correct hedge. Canonical homes checked: b1w01 Friday does own the drift-SLA/pass-through machinery (14 + 25 mentions) and b2w04 Monday does own the Artisan teardown (24 mentions) — Week 9's one-line-recap-plus-wikilink treatment is compliant, no re-teaching found.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Scope collapse" named as the mechanism up front; no number asserted the dailies don't own. |
| Chip Huyen | 8 | Day table maps to concrete artifacts (tier sheet Tue, runbook Wed, pricing Fri); "five angles on one artifact" is the right frame. |
| Jerry Liu | 8 | Distribution correctly subordinated to the package, not the reverse. |
| Hamel Husain | 8 | Eval discipline and reliability named as prerequisites for guarantees, linked not re-taught. |
| Simon Willison | 8 | No overclaims; the 2026 surfaces are named, not hyped. |
| Seibel | 9 | Sells the week in two paragraphs; "draft artifacts as you go so Saturday is assembly" is the correct operating advice. |
| Boris Cherny | 8 | Points at Week 8 reliability as the substrate without teaching it. |
| Cohort peer | 9 | "The build you finished becomes an asset that sells while you sleep" is honest and motivating. |
| Mira Murati | 8 | Commercial positioning without hype. |
| swyx | 8 | Post-GPT-Store framing signals the week won't be marketplace-naive. |
| Ethan Mollick | 8 | "Do Monday's audit honestly; the week compounds on it" is good behavior design. |
| Lilian Weng | 8 | Terminology (tier ladder, scope collapse, upgrade train) consistent with the dailies. |
| Jeremy Howard | 8 | Links carry the Block 1 load. |

**Weighted average: 8.1**

---

## 01-mon — From build to package: the productization spectrum

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four-position spectrum decomposed by what marginal delivery costs, not by branding; scope-collapse axes are genuinely mechanistic. |
| Chip Huyen | 9 | The $267/hr vs $750/hr arithmetic and "support worsens permanently" are real ops economics; margins stated with both edges. |
| Jerry Liu | 8 | Platform position included only for take-rate context — correct restraint. |
| Hamel Husain | 8 | Packageability rubric demands one sentence of evidence per score, "reject vibes"; absence-of-evidence treated as data (solo GPT revenue). |
| Simon Willison | 9 | The FDE controversy is properly two-sided with named sources; single-source items ($9B aggregate, 30–40% heuristic) flagged in-line, exactly the amended protocol's discipline. |
| Seibel | 8 | His own correction (sell it manually five times first) is in the lens and the pass bar. |
| Boris Cherny | 8 | "Would delivery #5 consume fewer hours" is the right prerequisite honesty. |
| Cohort peer | 9 | Stammer white-label economics make Position 2 concrete for non-engineers. |
| Mira Murati | 8 | Her Thinking Machines lens ("customization itself can be productized") is the strongest reading of the thesis, and the lesson admits it under-develops it. |
| swyx | 8 | Distribution-before-packaging pushback surfaced and resolved honestly. |
| Ethan Mollick | 8 | The 60–90-min experiment has a real pass bar (≥22/30) and a dignified failure output. |
| Lilian Weng | 8 | Harvey/Sierra figures internally consistent with Sunday's cards. |
| Jeremy Howard | 8 | Block 1 SOW/niche homes wikilinked with one-line recaps — compliant. |

**Weighted average: 8.2**

Notes: [^14]'s ~$9B aggregate FDE figure and [^16]'s 30–40% heuristic are single-source; both carry in-line hedges ("order-of-magnitude," "attributed"), which is compliant. Contrast tics were 3 (one over budget); trimmed to 2 this session.

---

## 02-tue — Package design: scope, tiers, guarantees

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Guarantee and price are the same object" (Position A) is the correct mechanism-level read of Sierra/Fin. |
| Chip Huyen | 9 | Six tier variables with three never-tier variables is a real design system; the voice-agent transfer check proves the method isn't overfit to one shape. |
| Jerry Liu | 8 | Eval-report-as-tier-deliverable is the genuinely non-obvious productization of Week 4's machinery. |
| Hamel Husain | 9 | His golden-set-provenance critique is in the lens, conceded, and wired into Saturday's template — the seam works. |
| Simon Willison | 8 | The drafted Position-B clause is honest to the last sentence ("does not promise correctness of any individual claim"); Position D ("lying, with a lag") named. |
| Seibel | 8 | Cohort-peer lens carries his critique: show the tier sheet to one real prospect this week. |
| Boris Cherny | 9 | "Every guarantee is a runbook obligation; what fires at 2am across eleven tenants" is the operational truth most packaging content skips. |
| Cohort peer | 9 | Procurement-attack and counsel-attack prompts are directly runnable. |
| Mira Murati | 7 | Nothing on how guarantee posture shifts across model generations; defensible scope. |
| swyx | 8 | Fin/Agentforce/Sierra triangulation is current and correctly sequenced. |
| Ethan Mollick | 8 | Measurement-plus-volume as the decision variable is teachable and honest. |
| Lilian Weng | 8 | Error-budget/drift-clause stack matches the SLA literature cited. |
| Jeremy Howard | 8 | b1w01 drift-SLA skeleton recapped in one line and generalized, not re-taught — compliant. |

**Weighted average: 8.2**

---

## 03-wed — Delivery engineering: one build, many customers

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | His own lens argues against the lesson's ceremony ("canary trains can be cosplay; the harness is the architecture") — the sharpest self-critique of the week. |
| Chip Huyen | 9 | Config-sprawl warning plus the data-flywheel gap named in the lens; COGS worked with tokenizer and date-stamp corrections. |
| Jerry Liu | 8 | Three-plane tenancy decomposition collapses the multi-tenant debate correctly. |
| Hamel Husain | 8 | Per-niche-pack regression as the upgrade-train gate is his discipline deployed at fleet scale. |
| Simon Willison | 9 | Lethal-trifecta-with-a-subscription-model is exactly his threat model, and the lens correctly says the lesson isn't paranoid enough (egress allowlists, output sanitization). |
| Seibel | 8 | White-label crossover arithmetic ("renting is often right at small scale") resists the build-everything instinct. |
| Boris Cherny | 8 | "A tenant pinned to the old version is a fork with a customer attached" is the tooling truth. |
| Cohort peer | 9 | The worked v1.6.2→v1.7.0 release narrative makes upgrade trains concrete; maintenance-as-revenue framed with the buyer's counter-question scripted. |
| Mira Murati | 7 | Model-swap treatment is operational only; no capability-delta reasoning. |
| swyx | 8 | Deprecation-wave-as-evidence is the correct 2026-native argument for maintenance contracts. |
| Ethan Mollick | 8 | Fire-drill experiment with hour estimates sanity-checked against real eval runtime. |
| Lilian Weng | 8 | Rent-seeking controversy has two coherent positions and a synthesis with a principled line (control plane vs config). |
| Jeremy Howard | 8 | Week 8 credential/reliability homes linked, not re-taught — compliant. |

**Weighted average: 8.3**

Notes: the $13.60/$20.40 inference figures disagreed with the calculator's $13.64/$20.46 — fixed this session.

---

## 04-thu — Distribution surfaces for agent products in 2026

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "The demand originated outside the marketplace" is the mechanism under all three converting paths; the map explains strategies, not listings. |
| Chip Huyen | 8 | Take-rate table with "what you're actually buying" per surface is operator-shaped. |
| Jerry Liu | 9 | His decomposition caveat (one asset, three surfaces, whoever owns the interface owns the renewal) is a genuinely sharp addition. |
| Hamel Husain | 8 | "Instrument the channel question like Week 3 instrumented landing pages" — CAC in hours, kill criteria, no vibes. |
| Simon Willison | 8 | GPT-Store evidence handled honestly (absence as data); the WhatsApp-directory refusal to name a canonical source is the right epistemics. |
| Seibel | 9 | Position B is his actual argument, and the worked Niche Radar plan (60 sends / 6 weeks / kill criterion) executes it. |
| Boris Cherny | 8 | MCP-manifest-as-distribution is correctly priced as a no-downside afternoon. |
| Cohort peer | 9 | The two-channel plan with named triggers "instead of guilt" is directly copyable. |
| Mira Murati | 8 | Zero-take-rate strategy read (monetize tokens underneath) is the correct strategic decode. |
| swyx | 9 | Agents-as-buyers thesis labeled "speculative in degree, correct in direction" — precisely calibrated. |
| Ethan Mollick | 9 | Lab-leak adoption path (forwardable artifacts) present in the lens and folded into the plan. |
| Lilian Weng | 7 | Marketplace listing counts (14K) rest on secondary/SEO sources; hedged, but the thinnest evidence in the file. |
| Jeremy Howard | 8 | Block 1 outbound/demand-map homes recapped in one line each — compliant. |

**Weighted average: 8.3**

---

## 05-fri — Pricing the package

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | The three-question physics test is a real decision procedure; "a rounding error wearing a philosophy" correctly kills metric mimicry. |
| Chip Huyen | 9 | Three structures fully worked with the same COGS base; structure (b)'s honest cost ("prices below (a) for the median customer") is rare candor. |
| Jerry Liu | 8 | Hybrid floor-plus-variable default matches where the evidence points. |
| Hamel Husain | 9 | His tracked-not-billed-metrics-rot critique is in the lens *against the lesson's own synthesis* and changes the advice (wire outcomes to a consequence). |
| Simon Willison | 8 | Backlash evidence triangulated across buyer-side, finance-side, and vendor-repentance sources; asymmetric pass-through called out as a trust cost. |
| Seibel | 9 | His "say $1,500 out loud to ten buyers" cut is the lens's opening, with a narrow, honest defense of the matrix. |
| Boris Cherny | 8 | Never-grandfather-the-metric (billing forks as fork disease) is the correct invariant. |
| Cohort peer | 9 | The flinch-on-the-pricing-sentence observation is the thing experts skip; problem set 4's grandfathering ledger is a real drill. |
| Mira Murati | 7 | The "COGS falls 90%" reflection gestures at model-curve strategy but stays surface. |
| swyx | 8 | The $250-collapse and usage-backlash placed as anchors without doom. |
| Ethan Mollick | 8 | Stress-matrix pass bar (≥70% fully loaded, four numbers zero adjectives) is behavior design. |
| Lilian Weng | 8 | Structure (c)'s physics-test failure is argued, not asserted (adjudication incentive + volume variance). |
| Jeremy Howard | 8 | b2w04 Artisan and b1w01 pass-through kept canonical; one-line recaps only — compliant. |

**Weighted average: 8.2**

Notes: the "~54 analyst-hours/month" renewal figure contradicted the package's own labor line (16.5 h/month ≈ 50/quarter) — fixed this session in both spots plus the code-lab's pricing sentence. Scenario (iv)'s wording now matches what the calculator actually implements.

---

## 06-sat — BUILD: your first sellable agent package

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Config-as-single-source-of-truth with generated documents is the right architecture for the problem ("three documents wearing a trench coat"). |
| Chip Huyen | 9 | The support-dominates-COGS lesson walked through the example *before* the student's own numbers; opportunity-cost-vs-replacement-cost gap named. |
| Jerry Liu | 8 | Build order (yaml → calculator → documents) is dependency-correct. |
| Hamel Husain | 9 | Provenance block enforced; "a template that promises metrics you don't collect is a future incident report" is his discipline verbatim. |
| Simon Willison | 8 | Fresh-conversation stranger test ("no context sympathy") is methodologically right. |
| Seibel | 9 | Gets the last word he earned: "The folder is not the milestone. The first reply is." |
| Boris Cherny | 8 | Evidence-it-completed as the field that scales to handing the fleet to an agent — correct. |
| Cohort peer | 9 | Filled Stage-6 exemplar calibrates what "done" means; live-session bring-list is disagreement-shaped. |
| Mira Murati | 7 | No model-choice stage in the build; inherited from Wednesday, defensible. |
| swyx | 8 | Week 10 handoff (one-pager → page, script → video) is the distribution seam done right. |
| Ethan Mollick | 8 | Ten-item checklist with "eight of ten is a pass with homework" is honest calibration. |
| Lilian Weng | 8 | Extension guidance (every scenario must name an event; churn correctly rejected as out-of-model) shows the model's boundaries are understood. |
| Jeremy Howard | 9 | His artifact-production-vs-judgment risk is the lens's opening and the lesson's actual design principle. |

**Weighted average: 8.3**

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Q11 rewards recomputation from rates, not recall; the mental-move table compresses the week into decision procedures. |
| Chip Huyen | 8 | "Support hours dominate COGS" correctly elevated to the week's deepest lesson. |
| Jerry Liu | 8 | Synthesis keeps marketplaces subordinate to demand, matching Thursday. |
| Hamel Husain | 9 | "Where you'd still lose points" names the load-bearing guess (support hours) and the persona-not-human gap — rare honesty in a synthesis. |
| Simon Willison | 8 | A13/A14 compress the evidence correctly; re-verify-before-quoting-past-September warning is the right currency hygiene. |
| Seibel | 8 | "No real buyer touched anything" is gap #1, correctly. |
| Boris Cherny | 8 | A9's plane decomposition and A8's metric-fork answer match Wednesday exactly. |
| Cohort peer | 9 | Quiz difficulty calibrated; Q15's discount drill is the one students will actually face. |
| Mira Murati | 7 | Forward pointers are all commercial; no capability-frontier note. |
| swyx | 8 | Agent-as-buyer thesis carried into the gaps section with a re-verify date. |
| Ethan Mollick | 8 | "Where each day goes forward" converts content into scheduled behavior (Sept 1 re-run, quarterly channel review). |
| Lilian Weng | 8 | All 30 flashcards checked against the weekday lessons; no contradictions found post-fix. |
| Jeremy Howard | 8 | No duplicate territory with Block 1/2 quizzes; pricing questions build on, not repeat, b2w04. |

**Weighted average: 8.1**

Consistency audit (Sunday vs weekdays vs code-lab, all verified identical post-polish): tiers $750/$1,500/$3,500 with 6/12/25 sources; $0.62/run; $13.64/mo inference; $112.50 support; ~$133 loaded COGS; $990 labor line (16.5h × $60); stress margins 91.1/90.7/87.5/85.2/83.6 and Starter 68.0*; $28,750 rev / ~$26,700 GP at 15 customers; Artisan $250 (from $2,500, May 2026, $300 credits); Fin $0.99 + $49/50 resolutions; $3.6B Jun 15; Salesforce 15%/25%; Claude Marketplace 0% (Mar 6); Sonnet 5 $2/$10 → $3/$15 (Aug 31); deprecation ledger (Jan 5 / Feb 19 / Apr 14 / Apr 20 / Jun 5→15, ≥60-day policy); 78% / 90% / 56.8%; Stammer $197 + $300–500 + 3–5×; ~14,000 listings; AWS $1B (Jun 30); 30–40% FDE heuristic; ~50 analyst-hours/quarter. Q11's inputs match Wednesday's table exactly and the calculator reproduces them.

---

## code-lab/06-agent-package (README, requirements, models.py, pricing_calculator.py, package_spec.py, package.example.yaml)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Small, readable, deterministic; frozen dataclass rate card with a hard failure on unknown tiers is the right shape. |
| Chip Huyen | 9 | Date-stamped rates with the tokenizer factor as an explicit parameter; support at loaded rate is the honest default. |
| Jerry Liu | 8 | Generator's six documents map 1:1 to the Saturday deliverable set. |
| Hamel Husain | 8 | Eval-report template ships the provenance block and threshold columns; ±5pp drift row matches Tuesday's clause. |
| Simon Willison | 8 | No keys, no network, secrets-by-reference modeled in the example YAML ("reference, never a value"). |
| Seibel | 9 | Deliberately deterministic teaching tool that says so; "modify one thing" instruction is the study protocol done right. |
| Boris Cherny | 8 | `get_rate` failure message tells you to add a rate_date; PyYAML pinned; Python 3.10+ stated. |
| Cohort peer | 9 | README runnable top to bottom; example output genuinely teaches the support-dominates lesson. |
| Mira Murati | 7 | Rate card covers four tiers only; adding non-Anthropic tiers is left implicit. |
| swyx | 8 | Scenario names match Friday's narrative post-fix. |
| Ethan Mollick | 8 | "Any cell below 70% fails Friday's pass bar" ties code output to the lesson's decision rule. |
| Lilian Weng | 8 | Even-spread revenue assumption is stated in the output; margin-only scope acknowledged in Saturday's extension notes. |
| Jeremy Howard | 8 | int() truncation on scaled tokens is crude but harmless at these magnitudes. |

**Weighted average: 8.1**

---

## Overall Week 9: **8.2 / 10**

(File averages: 8.1, 8.2, 8.2, 8.3, 8.3, 8.2, 8.3, 8.1, 8.1.) Strongest: Wednesday and Thursday — reviewer lenses that genuinely argue against the text, and evidence assembled over vibes. The doc/code agreement is unusually good: every stress-matrix number quoted in three different lessons reproduces from the shipped calculator to the decimal. Anti-slop: em-dash density 8.9–11.4/1k across all files (under the ~12 bar, no trims needed); contrast tics ≤2/file after one Monday trim; house tics well inside budget ("would push back" 1× total, "load-bearing" 1× total, "operator" 4–6× in Mon/Wed/Thu/Sat — Thursday's 6 is the ceiling, mostly the legitimate "solo operator"). Canonical homes: all five (b1w01 SOW/pass-through, b1w02 niche/building-in-public, b2w03 instrumentation, b2w04 Artisan/eval, b3w08 reliability/credentials) wikilinked with one-line recaps — no re-teaching found against direct inspection of b1w01-fri and b2w04-mon. Quiz (15Q + key) and flashcards (30) all trace to weekday lessons.

---

## Surgical fixes applied this session (Phase 3, done)

1. **03-wed Layer 4:** inference figures "$13.60" and "$13.60 → ~$20.40" corrected to the calculator's actual **$13.64** and **$13.64 → ~$20.46** (0.62 × 22 = 13.64; 0.93 × 22 = 20.46).
2. **07-sun A11 + flashcard 23:** same $13.60 → $13.64 correction.
3. **05-fri Layers 2 & 4:** "~54 analyst-hours/month" contradicted the package's own labor line (16.5 h/month ≈ 50/quarter) → "~50 analyst-hours (this quarter)" in both renewal-conversation examples.
4. **package.example.yaml:** demo pricing sentence "fifty-four analyst-hours of monitoring" → "fifty analyst-hours of monitoring every quarter" (now consistent with the 16.5 h/mo labor line the eval-report template prints).
5. **code-lab README:** scenario list said "outcome-rate bad month" but the code implements a doubled-support bad month → README now says so; **05-fri experiment Step 2 (iv)** reworded to cover both readings and name which one the calculator ships.
6. **package_spec.py `eval_report`:** crashed with KeyError on configs without a `labor_line` (which `one_pager` treats as optional) → value-line basis now degrades to a fill-in placeholder.
7. **01-mon Axis 4:** contrast-tic count was 3 (budget ≤2) → one "not just a marketing choice" scaffold removed without content change.
8. **06-sat:** "Week 10, pending generation" upgraded — Weeks 10 and 11 now exist → wikilinked to `[[02-tue-the-launch-page-assembled|Week 10]]` and `[[01-mon-idea-definition-from-itch-to-falsifiable-bet|Week 11]]`; same upgrade applied to 07-sun's two forward pointers.

All Python re-compiled clean and both tools re-run successfully after edits; the no-labor-line path was exercised directly.

## Unresolved concerns (recommendations, not applied)

1. **Word counts run 3.9–4.4K** vs the L3 4,500–6,500 soft target on every daily. Density is genuinely high and the brief says density over length, but Tue and Fri could each absorb ~400 words on the gaps their own lenses name (guarantee posture across model swaps; model-curve pricing strategy).
2. **Middle-market revenue sourcing is the citation weak point** (Taskip / Digital Agency Network / Build with Dew are SEO-guide tier; the $77K solo case is uncorroborated). The in-text hedges ("directional composites, not audited financials," "existence proofs, not medians") are correct; Phase 4 should hunt stronger corroboration or downgrade the band to a range-of-ranges.
3. **Calculator hosting-split assumption:** per-tenant fixed cost always divides fleet hosting by `expected_fleet_size_for_hosting_split` (10), so the "5 customers" revenue line silently uses 10-tenant economics. Saturday's fixed-cost-shock extension addresses it, but a one-line README caveat (or an actual-fleet-size parameter) would be cleaner. Design decision — left for the author.
4. **Thursday's marketplace listing counts** (~14,000 AgentExchange; 9,400+ n8n templates) rest on secondary/SEO sources; both hedged in-line, but they are quoted in Sunday's flashcards, which hedge less.

## Phase 4 citation-verify list

1. Mon [^3]: Sierra $950M at $15.8B (May 2026) — current sourcing is chatforest/sacra/webpronews; land a primary (press release or tier-1 outlet).
2. Mon/Wed/Fri/Sat: Sonnet 5 intro-pricing end date 2026-08-31 against the live Anthropic pricing page (liveness pass).
3. Tue/Fri [^1]/[^2]: Fin standalone "$49/month including 50 resolutions" against the Intercom help doc.
4. Thu [^2]: AgentExchange ~14,000 listings and the April-2026 three-marketplace merger — find Salesforce primary.
5. Mon [^15]: FDE postings +729% YoY (~643 → 5,300+) against the TechTarget piece.
6. Mon [^1]: harvey.ai blog URL liveness for the $11B round corroboration.
7. Thu [^14]: n8n "9,400+ templates by May 2026" (connectsafely.ai is thin).
8. Fri [^3]/[^7]: Tropic 78% and Zenskar 90% figures against the actual posts.
9. Tue [^9]: BuildMVPFast ±5% drift-clause default (single-source, attributed — confirm or soften).
10. Wed [^10]: endoflife.date Claude retirement dates (Feb 19 / Apr 20) against the tracker.

---

_Review + surgical polish produced 2026-07-17. Files edited: 01-mon, 03-wed, 05-fri, 06-sat, 07-sun, code-lab/06-agent-package/README.md, package.example.yaml, package_spec.py. No git commits made._
