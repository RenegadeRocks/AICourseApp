---
type: review
phase: 2
week: week-10
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 10 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-4-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-10-briefs.md`.

Mechanical checks run this session: `python -m py_compile` on all three code-lab modules (pass); `make_fixtures.py` → `brief_generator.py` (exit 0, 5 briefs) → `qa_runner.py` on the example manifest (**exit 1 with exactly the three advertised failures**: 1200×628 OG, "100% accurate" banned phrase, 100%/95% unsubstantiated) and **exit 0 after removing the deliberate failure** — README's exit-code claims verified by execution, not reading. All example JSON valid. **All 16 distinct wikilink targets resolve** to real, unambiguous vault basenames after one fix (below); the 44 "pending" strings in the week are all the amended-protocol "liveness pass pending" citation hedge — zero `(pending)` wikilinks remained to upgrade. Em-dash density 1.6–8.9/1k per file (budget ≤ ~12); contrast tics ≤2/file; "would push back" ≤1/file; "load-bearing" 2× total. WebSearch spot-checks: Sora two-stage shutdown (app 2026-04-26, API 2026-09-24, ~$1M/day vs ~$2.1M lifetime revenue) — confirmed against OpenAI Help Center + The Decoder + Futurum; Fin $0.99 pricing — confirmed, with a billing nuance found and folded into Monday's [^4] (see fixes). WebFetch egress-blocked; the lessons carry the correct per-citation hedge throughout.

**The b2w03 boundary check (brief-critical), quantified.** Read against all seven b2w03 lesson heading sets: Week 10 re-states b2w03 material in exactly one place, Tuesday Layer 1's seven-row recap table (~130 words, every row one line + canonical wikilink), plus one-line prerequisite recaps in Monday (~40 words) and Friday's "assumed wholesale" pointer to b2w03 Saturday. Total overlap ≈ 250 words of 25K (~1%), all explicitly labeled as recap with canonical homes linked. No re-teaching of Shapiro anatomy, Laja diagnosis, conversion math, attention ratio, design-system variables, Wilson intervals, or pre-registration mechanics — Friday *uses* pre-registered bands and small-n humility but defers their derivation to [[06-sat-validation-instrumentation]] every time. **Compliant, and cleanly so.** The new ground (agent-specific trust gap, proof hierarchy, eval-as-marketing, 2026 creative stack, launch instrumentation) is genuinely new relative to b2w03.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Eval report wearing a suit" is a real mechanism claim, and the dailies own the numbers it gestures at. |
| Chip Huyen | 8 | Day table maps to deliverables; the launch-as-experiment through-line is correct. |
| Jerry Liu | 8 | Positions the week as one artifact from five angles without overclaiming. |
| Hamel Husain | 8 | "Claims require evidence, launches are pre-registered experiments" is his discipline, stated up front. |
| Simon Willison | 8 | The three above-the-fold buyer questions are earned by Monday's survey evidence. |
| Seibel | 9 | Sells the week in two paragraphs; "not a re-run of Week 3" boundary declared. |
| Boris Cherny | 8 | Points at the code-lab without teaching it here. |
| Cohort peer | 9 | "If your marketing looks like unreviewed AI output, buyers infer your agent is" is a sellable sentence. |
| Mira Murati | 8 | Commercial framing without hype. |
| swyx | 8 | Slop-backlash-as-meta-signal is the right 2026 read. |
| Ethan Mollick | 8 | Prereq honesty about the Week 9 stand-in. |
| Lilian Weng | 8 | Terminology consistent with the dailies. |
| Jeremy Howard | 8 | Recap-in-one-table promise made and (verified) kept. |

**Weighted average: 8.1**

---

## 01-mon — Selling the invisible

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Trust-gap inversion (disqualifiers before value) is a real mechanism; proof hierarchy ordered by a principle (buyer-verifiability), not vibes. |
| Chip Huyen | 9 | Pricing-model menu states both edges (outcome pricing's revenue-inherits-variance cost); worked-math page rule is operator-real. |
| Jerry Liu | 8 | Scoped-claim pattern does three jobs and says which three. |
| Hamel Husain | 9 | Eval-report-as-marketing with methodology-or-it's-slop, plus his own lens attack on 40-example golden sets — the discipline, weaponized. |
| Simon Willison | 9 | FTC substantiation floor correctly sourced; CloneDesk single-source properly flagged in [^5] and (post-fix) no longer pluralized as "analyses" in-text. |
| Seibel | 8 | His ship-the-ugly-page-first pushback is in the lens with an honest synthesis. |
| Boris Cherny | 8 | Substantiation-file-as-artifact sets up Saturday's CI gate. |
| Cohort peer | 9 | The 55%-resolution reflection question is the uncomfortable one readers need. |
| Mira Murati | 7 | Pricing menu is rent-the-pattern; nothing on when model choice changes the cost floor. |
| swyx | 8 | "AI-powered is a disclosure, not a differentiator" is the correct 2026 positioning read. |
| Ethan Mollick | 8 | Pass bar routes failure to "run the eval first," not "write vaguer copy." |
| Lilian Weng | 8 | Survey triangulation (Okta/INFUSE/TrustRadius) is the right evidence shape. |
| Jeremy Howard | 8 | b2w03 boundary stated in the lesson itself; one-line recap only. |

**Weighted average: 8.3**

Notes: Fin billing nuance ($0.99 is per qualifying *outcome*, monthly minimum on standalone) surfaced by this session's WebSearch spot-check — now recorded in [^4]; body/quiz keep the marketing-level framing the lesson is explicitly analyzing, which is defensible now that the citation carries the fine print.

---

## 02-tue — The launch page, assembled

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Demo-rung decision rule is written in terms of measured p90, not courage — the correct variable. |
| Chip Huyen | 8 | Her own lens flags the single-publisher benchmark risk; framework axes vs numbers correctly separated. |
| Jerry Liu | 8 | Curated-input sandbox is the genuinely useful middle pattern, with its epistemic limit stated. |
| Hamel Husain | 9 | Pass bar's honest branch ("no evals yet, so video") enforces eval-before-ambition. |
| Simon Willison | 9 | Injection/abuse treatment of a public agent text box is exactly right, and his lens demands adversarial verification rather than spec assertion. |
| Seibel | 9 | CTA grid ends in "fix your evidence economics before launching" — the anti-theater quadrant. |
| Boris Cherny | 8 | Fallback-flag rehearsal is real ops discipline. |
| Cohort peer | 9 | Dispatch worked example (labeled composite) shows every decision with numbers that match the code-lab exactly. |
| Mira Murati | 7 | Navattic Agent Demos noted but the personalization-vs-proof question is left to a reflection. |
| swyx | 8 | Live-demo-as-credibility-signal counterargument is his actual position, honestly staged against Simon's. |
| Ethan Mollick | 8 | FTC fake-reviews rule turns the honesty argument into a compliance floor. |
| Lilian Weng | 8 | Demo-tool pricing triple-sourced with vendor-written bias noted. |
| Jeremy Howard | 8 | The recap table is the whole recap — brief's hardest constraint, met. |

**Weighted average: 8.3**

---

## 03-wed — The 2026 AI creative stack

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Capability/terms/perception three-way split is the right decomposition; "cost stopped being the constraint" is the honest 2026 read. |
| Chip Huyen | 8 | Stack-within-budget discipline with real prices; $30–50/month math checks. |
| Jerry Liu | 7 | Tool landscape leans on SEO-tier roundups (nomadlab, laozhang, getaiperks); hedged, but thinnest sourcing of the week. |
| Hamel Husain | 8 | "Hold percentages loosely, direction corroborated" applied to backlash surveys — correct posture. |
| Simon Willison | 8 | Copyright Part 2 rendered accurately (unprotectable raw gens, protectable arrangement, disclosure duty); license-trap layer is his kind of catch. |
| Seibel | 8 | Howard's minimalist-stack pushback keeps the lesson honest about first launches. |
| Boris Cherny | 8 | Export-discipline lesson from Sora is the tooling truth. |
| Cohort peer | 9 | Revenue-threshold clause applied to *client work* is the trap readers would actually hit. |
| Mira Murati | 8 | Her tuned-models-eat-prompt-discipline thesis is in the lens, correctly attributed as a bet. |
| swyx | 9 | Sora shutdown read as unit-economics lesson, not drama — verified figures, right conclusions. |
| Ethan Mollick | 9 | Slop = detectability + laziness, not assistance; his expertise-gap framing sharpens it in the lens. |
| Lilian Weng | 8 | Three positioning stances are mutually exclusive and decidable. |
| Jeremy Howard | 8 | b1w02 kept canonical for authenticity; this lesson only adds the 2026 evidence layer. |

**Weighted average: 8.1**

---

## 04-thu — Creative production pipeline

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Batch-and-select correctly framed as sampling with a human verifier; his own lens calls out process-worship risk. |
| Chip Huyen | 8 | Gate-failure logging ("three palette failures = one bad brief") is systems thinking applied to creative. |
| Jerry Liu | 8 | Six-stage pipeline with output contracts; brief-as-spec parallels the codegen discipline without re-teaching it. |
| Hamel Husain | 8 | His unmeasured-judgment-checks critique is in the lens and conceded as the week's thinnest discipline. |
| Simon Willison | 8 | Platform disclosure map appropriately hedged (LinkedIn reach figures explicitly labeled analytics-vendor estimates, not platform statements). |
| Seibel | 8 | "Never negotiate with a mediocre candidate" is the productivity delta, named. |
| Boris Cherny | 9 | Check-suite-not-checklist and the unmonitored last mile (served vs uploaded creative) — both real and both his. |
| Cohort peer | 8 | Guardrail beat (film the escalation) is the differentiator nobody ships. |
| Mira Murati | 7 | Andromeda treated as given; nothing on where creative models themselves are heading. |
| swyx | 8 | "Creative variety is the buying lever now" matches the 2026 practitioner consensus, labeled as such. |
| Ethan Mollick | 8 | EU AI Act Article 50 correctly future-framed (applicable 2026-08-02, 16 days out — date math checks). |
| Lilian Weng | 8 | C2PA status (v2.3, stripping weakness) accurate and appropriately deflated. |
| Jeremy Howard | 8 | Disclosure-as-cheap, non-disclosure-as-expensive is the pragmatist's compliance frame. |

**Weighted average: 8.0**

Notes: platform-policy claims (Meta labeling, YouTube disclosure) rest on secondary compliance-blog tier with 2–3 domain corroboration; Phase 4 should land the primary Meta/YouTube policy pages.

---

## 05-fri — Launch-day instrumentation

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | QAR's "must cost the visitor something" principle prevents the metric from optimizing itself into noise. |
| Chip Huyen | 9 | Her proxy-drift critique (demo-players ≠ buyers) is in the lens with the audit-to-revenue fix. |
| Jerry Liu | 8 | Event taxonomy is small, property-driven, and tool-agnostic. |
| Hamel Husain | 9 | Pre-registered bands + duration + no-peeking, with the day-6-motivated-reasoner failure named — the discipline transplanted correctly. |
| Simon Willison | 8 | Sandbox abuse instrumentation and replay-consent deferral to canon are the right calls. |
| Seibel | 9 | "The dashboard is mostly theater at your traffic level" concession is built into the plan's 90-minute budget. |
| Boris Cherny | 8 | Break-one-event verification ("instruments you haven't seen fail") is real engineering hygiene. |
| Cohort peer | 9 | Product Hunt sober read (credibility asset factory, one-day experiment) saves readers a week of hope. |
| Mira Murati | 7 | AI-assistant-mediated buying is noted in the lens but not instrumented beyond "protect the human channels." |
| swyx | 8 | Dark-funnel vs statistics-school fight staged with named positions (Walker vs Recast) and the sidestep argued, not assumed. |
| Ethan Mollick | 9 | "Collect the humans" — the launch-to-interview-pool bridge is the week's best behavioral design. |
| Lilian Weng | 8 | Small-n honesty (counts and stories over rate deltas) is statistically correct. |
| Jeremy Howard | 8 | b2w03 Saturday assumed wholesale by wikilink; zero re-derivation. |

**Weighted average: 8.3**

---

## 06-sat — BUILD: the launch kit

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Assembly, not invention" with the re-entry warning is the correct build-day frame. |
| Chip Huyen | 8 | Ship log with spend/hours by milestone makes launch two cheaper — ops learning loop. |
| Jerry Liu | 8 | Prompt template's "report the tappable count" turns a recap discipline into a build gate. |
| Hamel Husain | 9 | claims.json as literal CI gate, plus the stale-eval warning before T+14d — his program, shipped. |
| Simon Willison | 8 | Sandbox isolation verified *before* live, fallback rehearsed; matches Tuesday's threat model. |
| Seibel | 9 | Milestone clock + "prettier is not a milestone" + his own lens saying most readers should have shipped earlier. |
| Boris Cherny | 9 | Served-creative T+1 verification pass closes the last mile his Thursday lens opened. |
| Cohort peer | 9 | Checklist is genuinely runnable; unexplained-n/a rule prevents silent skips. |
| Mira Murati | 7 | No stretch goal beyond the static kit. |
| swyx | 8 | Launch-moment-vs-artifact-done separation (don't launch at 11pm) is distribution wisdom. |
| Ethan Mollick | 8 | Time boxes respect a solo operator's Saturday. |
| Lilian Weng | 8 | Milestone 4's deliberate-breakage test is proper instrument validation. |
| Jeremy Howard | 8 | 2.1K words is right for a build day; density, not padding. |

**Weighted average: 8.2**

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Q15 rewards applying the band logic to messy numbers, not recall. |
| Chip Huyen | 8 | Artifact-flow table (what goes where next) is a keeper; every row traces. |
| Jerry Liu | 8 | Mental-move table cites layer-level sources; all spot-checked rows resolve. |
| Hamel Husain | 9 | "Where you'd still lose points" names the week's three real weaknesses, including its own benchmark dependence. |
| Simon Willison | 8 | A8 states the FTC standard's actual phrasing; A10 compresses Part 2 correctly. |
| Seibel | 8 | Thesis-in-one-sentence passes the repeat-to-your-boss test. |
| Boris Cherny | 8 | A11's two operator habits are the right extraction from the Sora story. |
| Cohort peer | 9 | Quiz difficulty calibrated; Q15's "one call was a bad fit" detail forces judgment, not arithmetic. |
| Mira Murati | 7 | Synthesis stays inside the week's rent-the-stack frame. |
| swyx | 8 | A12's three-platform one-liners are accurate compressions of Thursday. |
| Ethan Mollick | 9 | The residual-weakness framing converts review into carried caution. |
| Lilian Weng | 8 | All 28 flashcards check against weekday lessons; no contradictions found. |
| Jeremy Howard | 8 | No duplicate territory with b2w03's quiz (anatomy/statistics ceded). |

**Weighted average: 8.2**

Consistency audit (Sunday + code-lab vs weekdays): all shared numbers identical everywhere checked — Fin $0.99; Zendesk ~$1.50/~$2.00; Okta 69/83/80%; Arcade ~$297.50, Storylane $40/$500, Navattic ~$500; opt-in ~14% (8–22) / opt-out ~44% (35–55); demo pages 1.5–4% / 8–15%; demo-vs-trial 55–75% vs 10–15%; Midjourney $10/$30/$60/$120 + $1M clause; ElevenLabs $6/$22/$99 + free-tier exclusion; Veo ~$0.15/s, Runway $12/$76, Kling ~$10; Sora $1M/day vs $2.1M, 3.3M→1.1M, Apr 26 / Sep 24; Screen Studio $29/mo, $89→$149; Meta 22%/12%, 8M advertisers; PostHog 1M/5,000, $0.00005/$0.005; PH 5–15K / 1–3K / <500, 1-in-10 featured; EU AI Act 2026-08-02; C2PA v2.3. Dispatch example (62% on 500-request set; Ridgeline 58% of 1,900; $1,200 + $0.40; 3 firms/6,100/14 weeks) matches `claims.json` and `launch_kit.json` string-for-string. Q15's 1.9% vs 0.5/3% bands → "continue" is correct.

---

## code-lab/06-launch-kit

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Small, readable, zero deps; hand-rolled PNG/JPEG header parsers are correct (verified against generated fixtures). |
| Chip Huyen | 8 | Mechanical/judgment split mirrors the lesson exactly; report format is actionable. |
| Jerry Liu | 8 | Brief generator is honestly deterministic ("specs should not be sampled"). |
| Hamel Husain | 8 | Deliberate-failure fixture teaches the report format; claims-file gate makes substantiation executable. |
| Simon Willison | 8 | No keys, no network, nothing persists outside briefs/ and reports/; banned-phrase list is a taste artifact in itself. |
| Seibel | 9 | Teaching tool that admits its scope; runnable in five minutes (verified). |
| Boris Cherny | 8 | Exit-code contract CI-ready; minor: reports/ lands in CWD, not beside the manifest. |
| Cohort peer | 9 | README commands reproduce exactly, including `echo $?` → 1. |
| Mira Murati | 7 | video/social_cutdown kinds are check-free stubs; acknowledged in comments. |
| swyx | 8 | The pipeline-as-product framing matches Wednesday's "demonstrative assistance" stance. |
| Ethan Mollick | 8 | Failure-first pedagogy (ship the broken example) is good teaching. |
| Lilian Weng | 7 | Claims matching is substring-in-blob: a short claim like "2%" would false-pass inside "62%"; RULES/ASSET_RULES sync is manual. |
| Jeremy Howard | 8 | stdlib-only constraint honored; requirements.txt empty on purpose and says why. |

**Weighted average: 8.0**

---

## Overall Week 10: **8.2 / 10**

(File averages: 8.1, 8.3, 8.3, 8.1, 8.0, 8.3, 8.2, 8.2, 8.0.) Strongest: Monday/Tuesday/Friday — the agent-specific conversion argument, the decision frameworks with honest benchmark hedging, and the instrumentation-to-decision bridge are genuinely new ground over b2w03. Weakest: Wednesday/Thursday's sourcing tier — the fast-moving tool/platform facts are corroborated across 2–3 domains each per the amended protocol, but many domains are SEO-adjacent roundups; the hedges are present and correct, the sources are just thin. Anti-slop: fully within budget on every metric measured. Canonical homes: all five (b1w01 SOW, b1w02 brand/niche, b2w03 landing/CI, b2w04 evals, b3w08 reliability) wikilinked with one-line recaps — no re-teaching found anywhere.

---

## Surgical fixes applied this session (Phase 3, done)

1. **05-fri:** `[[week-11-...]]` wikilink pointed at a *directory* (unresolvable as a vault file) → retargeted to `[[01-mon-idea-definition-from-itch-to-falsifiable-bet|Week 11]]`, which exists (weeks 6–11 all generated; this was the week's only unresolved link).
2. **01-mon Layer 3:** "independent analyses argue" overstated the single-source CloneDesk teardown → "one independent 2026 teardown argues" (hedge now matches the [^5] single-source flag).
3. **01-mon [^4]:** appended the Fin billing nuance found via this session's WebSearch spot-check (2+ independent corroborations): $0.99 is per qualifying *outcome* with a standalone-plan monthly minimum; "unresolved is free" labeled as marketing framing.
4. **01-mon [^11]:** Growthspree footnote was defined but never referenced in the body (orphaned) → anchored at Layer 5 item 8 (CTA/consideration), its natural home.
5. **01-mon:** trimmed the doubled "operator" tic in the Why-this-matters paragraph ("beat the operator with" → "beat the one with"); remaining instances are the term-of-art "solo operator" and within budget.

All Python re-compiled and re-run clean after review. No content files beyond 01-mon and 05-fri were edited.

## Unresolved concerns (recommendations, not applied)

1. **Word counts** run 3.5–4.3K per daily vs the brief's 4,500–6,500 soft target (frontmatter targets 4,700–5,200 also unmet). Density is high and the brief says density over length, so this is logged, not failed — but Wednesday and Thursday could each absorb ~500 words on the angles their own lenses name (Murati's tuned-brand-models trajectory; primary-source platform policy detail).
2. **qa_runner claims matching** is substring-in-concatenated-blob: a short numeric claim in copy (e.g. "2%") would false-pass if any allowed claim contains those characters (e.g. "62%"). Fix is a word-boundary match — behavior-changing, so left for the author.
3. **Wed/Thu source tier:** corroboration counts satisfy the amended protocol, but the domain quality (SEO roundups, compliance blogs) is the week's citation weak point. Hedges are in place; Phase 4 should upgrade to primary vendor/platform pages.
4. **Generated fixture PNGs** from running the code-lab example now sit untracked in `example/assets/` (the README's intended workflow generates them locally; they are not meant to be committed). Removal was blocked in this session's sandbox — either `rm example/assets/*.png` or gitignore them before any commit.

## Phase 4 citation-verify list

1. Mon [^4]: Fin pricing/benchmarks pages (`fin.ai`, `fin.ai/benchmarks`) — liveness + the standalone-minimum figure.
2. Mon [^5]: CloneDesk teardown URL liveness and whether its 45–53% band has been contested since.
3. Tue [^1]/[^2]: Arcade flat-$297.50 move and Storylane/Navattic tiers against the vendors' own pricing pages (currently vendor-blog sourced).
4. Wed [^3]: Veo 3.1 ~$0.15/s fast-mode rate against Google's API pricing page.
5. Wed [^12]: ContentGrip's 23.8%→10.2% Coca-Cola sentiment figures — single-analytics-source; verify or soften.
6. Thu [^3]: Meta's 22% ROAS / 12% CTR lift claims against Meta's own published materials and the Feb-2026 default-on change date.
7. Thu [^5]/[^6]: land primary Meta Transparency Center and YouTube Help pages for the disclosure rules.
8. Thu [^8]: C2PA v2.3 Feb-2026 date against c2pa.org.
9. Fri [^2]: PostHog free-tier allowances (1M/5,000) and overage rates against posthog.com/pricing.
10. Fri [^6]: Product Hunt band figures — founder-analysis tier; check against any PH-published data.

---

_Review + surgical polish produced 2026-07-17. Files edited: 01-mon, 05-fri, _review.md (this file). Code-lab executed but not modified. No git commits made._
