---
type: review
phase: 2
week: week-22
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 22 — Phase 2 Multi-Persona Review (the PROGRAM capstone)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-8-briefs/_generator-base.md` (anti-slop + EXTRA finale anti-fluff vigilance + ≥3-wikilink integration mandate + no-re-teaching), `week-22-briefs.md`, and `vault/00-program/index.md` (the whole-program map the capstone must reflect). This is a pure SYNTHESIS/CAPSTONE week; it is judged on integration density, honesty of the send-off, and zero re-teaching, not net-new fact density.

## Mechanical checks run this session (Python 3.11)

- **`py_compile graduation_audit.py plan_generator.py reverify_scheduler.py` — clean.**
- **`graduation_audit.py`** reproduces the Tuesday worked example exactly: Idea 9 + Validated 8 + Built 8 + Launched 6 + Monetized 5 + Grown 3 + Systematized 2 = **41/70**, band **"Building"** (26–45). **Hand-check:** the seven stage subtotals sum to 41 and each stays ≤10; the band boundary logic (≤25 Early / ≤45 Building / ≤60 Launched / else Systematized) is correct. Gap ranking sorts by `(-blocks_revenue, score)` → #18 (rev5,0), #21 (rev5,1), #23 (rev5,1), #30 (rev4,0)… verified correct against the source.
- **`plan_generator.py`** emits a Building-stage 3-sprint plan with correctly computed 30-day windows (2026-10-20 → 2027-01-17) and the right highest-leverage action + seeded trap/no-list. `stage_from_audit` bands match the audit.
- **`reverify_scheduler.py`** half-life scheduler works: cadences (price/model 30d, benchmark 60d, platform/competitor 90d, principle never) applied correctly; demo flags **2 facts overdue** (Opus price 65d, LinkedIn 5d), sorts overdue-first, marks the principle DURABLE. Matches Saturday's prose ("two facts already overdue and stale") to the letter.
- All three demo comments in `06-sat` (`41/70`, "Building-stage 3-sprint", "two facts overdue") reproduce exactly.

**Internal consistency:** the one-sentence course thesis, the five through-lines (evidence-over-vibes, unit-economics, anti-slop, eval-gating, canonical-homes), and the 14 durable principles are stated identically wherever they recur (Mon, Wed, Sat, Sun synthesis + quiz + flashcards). The 35 checklist items in `graduation_audit.py` match Tuesday's prose item-for-item.

## Hard checks

- **Integration density / wikilinks:** **142 wikilinks across 8 files, ALL 142 resolve** (per-file: overview 7, Mon 44, Tue 33, Wed 21, Thu 6, Fri 11, Sat 7, Sun 13 — every lesson ≥3, mandate met with room). The master build checklist's per-item links were spot-checked semantically: each of the 35 points to the canonical week that actually teaches it (idea→b4w11, when-AI-fits→b0w03, evals→b2w04, unit-economics→b6w16, SOPs→b7w20, etc.). The only `(pending)` marker is the Week-21 `_week` scaffold link (Mon L79) — correct, Week 21's dailies are not generated.
- **Re-teaching:** none. Every prior concept is a one-line recap + wikilink to its canonical home. The whole week is synthesis-by-reference, exactly as the brief demands.
- **Thursday requirement:** confirmed — Thu teaches re-verification using THIS course's July-2026 refresh as the running worked example (Opus mispriced 3×, deprecated vulnerable server, tokenizer change, 430k words dated, eleven parallel reviewers, forbidden-facts rules). This is the spec's central Thursday mandate and it is fully honored.
- **Anti-fluff / finale discipline:** **passes cleanly.** The send-off (Sun) is earned, not a speech: it restates concrete standards (evidence over vibes, margin computed, a pass bar before shipping, one canonical home, a date on every fact) and closes with a concrete action callback ("go get one person to pay"). No "the journey" language, no hype, no hollow inspiration. Friday's "honest probabilities" section actively resists both doom and hype and states base rates plainly.
- **Anti-slop metrics:** em-dash density 8.3–11.8/1k — **all under the ~12 ceiling** (Thu 11.8, Tue/Sat 11.6 are the tops; runs hotter than Week 20 but within budget). Contrast-scaffold tic ≤2/file everywhere (Thu 2, Sat 2 at budget; four files at 0). House tics in budget.

## NAME + CLAIM VERIFICATION (≥2 corroborations)

- **Atul Gawande — *The Checklist Manifesto*** (expert failure = omission under pressure). Real surgeon/author; corroborated (atulgawande.com + NIH PMC, also verified in the Week-20 review). **Verified.**
- **Jason Lemkin / SaaStr** (gross-margin literacy as the business/hobby line). Real SaaStr founder; the quote is framed as "Jason Lemkin's blunt version" — attributed paraphrase, appropriate. **Verified.**
- **Tiago Forte / PARA** (organize by actionability, not topic; Projects/Areas/Resources/Archives). Corroborated across fortelabs.com + todoist + workflowy; introduced 2017, expanded in *Building a Second Brain* (2022). Lesson's characterization is accurate. **Verified.**
- **Paul Graham — "Do Things That Don't Scale"** (paulgraham.com/ds.html, 2013; recruit users by hand). Corroborated (paulgraham.com + Inc. + multiple). Fri [^1] matches exactly. **Verified.**
- **"YC says agencies are 10× SaaS":** NOT stated as fact. Wed frames it as "one camp, loud on X and in YC-adjacent circles, argues… far larger than SaaS," calls it "partly a fashion," and [^5] explicitly instructs "treat the '10× larger than SaaS' claim as a contested projection, not fact." Already correctly reframed as attributed opinion. **No fix needed.**
- **Startup survival base rates:** corroborated against BLS — ~50% of businesses fail within 5 years, ~65% within 10. Fri [^2] says "multi-year survival… well below half," attributed to BLS + standard venture stats, appropriately hedged. Accurate for the 10-year horizon and roughly-half at 5 years; the soft phrasing is defensible. **Verified (minor precision note below).**

No hallucinated authorities; the "Max Freiberg" failure mode is absent.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Becomes one thing you can hold in your hand" states the week's actual job. |
| Chip Huyen | 8 | Day table maps each day to one durable artifact. |
| Jerry Liu | 8 | Subordinates the week to a single operating system, not seven topics. |
| Hamel Husain | 8 | Pass bar ("a score you'd show a mentor") is checkable. |
| Simon Willison | 8 | The decay framing is stated plainly, no hype. |
| Seibel | 9 | Sells the week honestly in two paragraphs; "if a day explains from scratch, it failed." |
| Boris Cherny | 7 | Light on tooling; correct for an overview. |
| Cohort peer | 8 | "Restate the linked idea before you follow it" is usable recall practice. |
| Mira Murati | 7 | No frontier note; defensible for a recap overview. |
| swyx | 8 | Names the re-verification meta-skill as the week's secret. |
| Ethan Mollick | 8 | Frames the week as artifacts, not concepts — right behavior design. |
| Lilian Weng | 8 | Terminology consistent with the dailies. |
| Jeremy Howard | 8 | Prereq = the whole program, stated without inflation. |

**Weighted average: 8.0**

---

## 01-mon — The whole map

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | "Software 2.0" + canonical-homes-as-thinking-skill is a real model, and the lens defends the billing. |
| Chip Huyen | 8 | The compounds/evaporates split is an honest engineering distinction. |
| Jerry Liu | 9 | The 8 blocks recast as one pipeline (output→input) is a clean synthesis. |
| Hamel Husain | 8 | The eval-gating through-line is stated as measure-before-build. |
| Simon Willison | 8 | Fast facts carry search-verified stamps; no naked claims. |
| Seibel | 9 | His "a map is procrastination if it delays shipping" is the lens, and it's answered. |
| Boris Cherny | 8 | Canonical-homes tied to CLAUDE.md as memory architecture. |
| Cohort peer | 8 | "Draw your own map in one page" pass bar is directly doable. |
| Mira Murati | 7 | Light on capability frontier. |
| swyx | 8 | "Judgment is the compounding asset" is the right 2026 read. |
| Ethan Mollick | 9 | His adoption-not-capability finding is used correctly and the lens sharpens it. |
| Lilian Weng | 8 | Through-line taxonomy consistent with Sun's cards. |
| Jeremy Howard | 9 | 44 wikilinks, all resolve; recap-not-re-teach discipline exemplary. |

**Weighted average: 8.3**

---

## 02-tue — The master build checklist

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | 0/1/2 rubric with "done on vibes = 0" is a real bar, not a slogan. |
| Chip Huyen | 9 | Item 24 ("recompute per-unit cost against current prices") catches stale economics precisely. |
| Jerry Liu | 8 | Seven stages as a pipeline audit, each wikilinked to its home. |
| Hamel Husain | 9 | His "evals should cap Stage 3, not round" pushback IS the reviewer lens. |
| Simon Willison | 8 | Every fast fact stamped; the audit avoids hype. |
| Seibel | 8 | "Gaps are the deliverable, not the number" defuses score-gaming — his own worry, answered. |
| Boris Cherny | 8 | His "item 18 does too much in one checkbox" flag is honest and routed to Wed. |
| Cohort peer | 9 | The worked audit (41/70 → a concrete Friday plan) is copyable. |
| Mira Murati | 7 | No frontier; fine for an audit. |
| swyx | 8 | Value-metric + expansion-path items are the current monetization read. |
| Ethan Mollick | 8 | "Audit the reality, not the aspiration" is real behavior design. |
| Lilian Weng | 8 | 35 items match the code-lab item-for-item. |
| Jeremy Howard | 9 | 33 wikilinks, all resolve to the right canonical weeks. |

**Weighted average: 8.2**

---

## 03-wed — The durable principles

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | His "the test sorts rules, not intuition" pushback is the lens and it lands. |
| Chip Huyen | 9 | Her "simplicity-first can excuse never building the harder system" is the sharpest lens. |
| Jerry Liu | 8 | Principle/fashion durability test is a genuine sorting tool. |
| Hamel Husain | 8 | Eval-gating stated as "no eval, no ship." |
| Simon Willison | 9 | His "the trifecta is a config to avoid, not a risk to manage" is the lens; take his version. |
| Seibel | 8 | "Agency-vs-product is a false binary; the sequence is the answer" is honest. |
| Boris Cherny | 8 | Security-posture principle framed as durable threat model, not a CVE. |
| Cohort peer | 8 | "Classify your own ten habits" pass bar is actionable. |
| Mira Murati | 7 | Frontier light. |
| swyx | 8 | Agency-vs-SaaS controversy carries named positions, correctly hedged. |
| Ethan Mollick | 8 | Adoption-practice framing consistent. |
| Lilian Weng | 8 | 14 principles match Sun's flashcards. |
| Jeremy Howard | 8 | Controversy names camps rather than faking consensus. |

**Weighted average: 8.1**

---

## 04-thu — Staying current: re-verification

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Knowledge has a half-life" decay map is a real epistemic model. |
| Chip Huyen | 9 | The three-tier calibrated-trust ladder is a usable production discipline. |
| Jerry Liu | 8 | The minimal 5-step refresh loop scales the course's own process down cleanly. |
| Hamel Husain | 8 | "Two independent sources for anything load-bearing" is the right bar. |
| Simon Willison | 9 | His "distrust confident AI on fast-moving facts should be the headline" is the lens — and correct. |
| Seibel | 8 | The perpetual-learner warning is bounded, not preachy. |
| Boris Cherny | 8 | `_last_verified` as an operational habit, not decoration. |
| Cohort peer | 8 | "Audit one week of this course" pass bar is concrete. |
| Mira Murati | 8 | The forbidden-facts / training-cutoff caution touches the frontier honestly. |
| swyx | 9 | His "narrow verification diet + small exploration budget" pushback is the sharpest tension. |
| Ethan Mollick | 8 | Information-diet-as-behavior-design is on-model. |
| Lilian Weng | 8 | Decay taxonomy consistent with the scheduler cadences. |
| Jeremy Howard | 9 | His anti-firehose position is named and agreed with; uses the July refresh as the worked example exactly as briefed. |

**Weighted average: 8.3**

---

## 05-fri — The forward path: next 90 days

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Stage → single highest-leverage action is a clean decision rule. |
| Chip Huyen | 8 | "Validation-constrained vs capital-constrained" is the right raise test. |
| Jerry Liu | 8 | Three 30-day sprints with one falsifiable outcome each is a real structure. |
| Hamel Husain | 8 | "Study X is not an outcome; shipping is" applies eval discipline to the plan. |
| Simon Willison | 8 | Base rates stamped and hedged, not hyped. |
| Seibel | 9 | His "stages/no-lists risk planning theater; did someone pay this week" is the lens. |
| Boris Cherny | 8 | The no-list as an explicit constraint is sound. |
| Cohort peer | 9 | The worked Building-stage quarter is directly transplantable. |
| Mira Murati | 7 | Frontier light. |
| swyx | 8 | Agency-vs-SaaS "averages are irrelevant to you" is the right operator framing. |
| Ethan Mollick | 9 | His "distribution with agency, not one grim number" is used well. |
| Lilian Weng | 8 | Stage bands match the audit + generator. |
| Jeremy Howard | 8 | Anti-tutorial-hell stance consistent with Thu. |

**Weighted average: 8.1**

---

## 06-sat — BUILD: graduation artifact

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four-part artifact maps 1:1 to three zero-dependency tools; no gold-plating. |
| Chip Huyen | 8 | "If it could belong to another graduate, it isn't done" forces specificity. |
| Jerry Liu | 8 | The tools encode Tue/Fri/Thu as runnable frameworks, not vibes. |
| Hamel Husain | 8 | Each sprint gets a measurable pass bar — evals applied to the self. |
| Simon Willison | 9 | All three tools verified to run clean; demos reproduce the lessons exactly. |
| Seibel | 9 | His "a beautiful artifact can substitute for the action it points to" is the lens. |
| Boris Cherny | 9 | His "fail loudly, validate inputs, zero-dep so any machine runs it" is honored in the code. |
| Cohort peer | 8 | The checklist-weights-are-adjustable note serves a real services operator. |
| Mira Murati | 7 | No model-choice stage; inherited, defensible. |
| swyx | 8 | Persist-and-diff extension is the right compounding idea. |
| Ethan Mollick | 8 | "Put it in a calendar now" ties the artifact to a behavior. |
| Lilian Weng | 8 | Item taxonomy consistent across lesson and code. |
| Jeremy Howard | 9 | Small, deterministic, offline; compiles and runs clean. |

**Weighted average: 8.2**

---

## 07-sun — Program capstone: synthesis + quiz + flashcards + send-off

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Compresses the program to one durable sentence + the compounding asset (judgment). |
| Chip Huyen | 8 | Q5/Q14 force the "why durable" reasoning, not recall. |
| Jerry Liu | 8 | The one-arc synthesis is a clean whole-program compression. |
| Hamel Husain | 8 | Answer key precise; Q14 nails eval-gating = shipped-not-demoed. |
| Simon Willison | 9 | Q10 ("confident AI answer is a lead") is the single best epistemic question in the set. |
| Seibel | 9 | The send-off is action, not speech: "close the vault and go get one person to pay." |
| Boris Cherny | 8 | Trifecta card + security answers match Wed. |
| Cohort peer | 9 | 15 cross-block questions + 30 durable-core cards, cold-quiz instruction correct. |
| Mira Murati | 7 | Forward-looking note light on frontier. |
| swyx | 8 | The dated-claim / half-life framing is the right 2026 close. |
| Ethan Mollick | 9 | The send-off restates standards, not motivation — earned, honest. |
| Lilian Weng | 8 | All 30 cards checked against the weekday lessons; no contradictions. |
| Jeremy Howard | 8 | Quiz draws across all 8 blocks without re-teaching. |

**Weighted average: 8.2**

---

## code-lab/1 (README, requirements, graduation_audit.py, plan_generator.py, reverify_scheduler.py)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Zero-dependency stdlib; every band, cadence, and gap-sort readable — the simplicity is the point. |
| Chip Huyen | 8 | `blocks_revenue` gap ranking is a real prioritization signal with documented, tunable defaults. |
| Jerry Liu | 8 | The three tools map 1:1 to Tue/Fri/Thu; no scope creep. |
| Hamel Husain | 9 | `py_compile` clean; all three demos exercise the documented paths exactly. |
| Simon Willison | 9 | Numbers reproduce the lessons exactly: audit 41/70, 2 facts overdue, Building-stage windows correct. |
| Seibel | 8 | Tiny by design so a graduate replaces demo data with real numbers post-course. |
| Boris Cherny | 9 | Inputs validated (0/1/2, known stages/kinds raise); scheduler intentionally shows the seeded facts going stale. |
| Cohort peer | 8 | README runnable top-to-bottom; pass bar concrete. |
| Mira Murati | 7 | No LLM backend; correctly left as a manual judgment layer. |
| swyx | 8 | Std-lib only, offline, 3.10+ floor pinned. |
| Ethan Mollick | 8 | Each tool ends in a human decision (score, plan, cadence), not automation theater. |
| Lilian Weng | 8 | Item / Sprint / Fact taxonomies consistent with the lessons. |
| Jeremy Howard | 9 | Small, deterministic, no network; compiles and runs clean. |

**Weighted average: 8.4**

---

## Overall Week 22: **8.2 / 10**

(File averages: 8.0, 8.3, 8.2, 8.1, 8.3, 8.1, 8.2, 8.2, code-lab 8.4.) A genuinely strong capstone. Strongest: Monday's one-pipeline synthesis, Thursday's re-verification meta-skill taught through the course's own July-2026 refresh, the honest no-hype send-off, and a code-lab that compiles clean and reproduces every claimed number (41/70 audit, 2-overdue scheduler, Building-stage plan) exactly. The reviewer lenses argue against the text rather than nodding at it (Chip on simplicity-first as an excuse, Simon on the trifecta as a config to avoid and on distrusting confident AI, Seibel on planning theater and artifacts-as-substitute, Hamel on evals capping the Built score). Integration is the headline: 142 wikilinks, all resolve, ≥3 per lesson, per-item checklist links pointing to the correct canonical weeks — and zero re-teaching. The finale earns its close.

---

## Surgical fixes applied this session

**None required.** No date drift (all `last_verified: 2026-07-17`; all in-text dates 2026-07-17; `date_due` sequential Mon–Sun). No unresolved wikilinks, no unambiguous errors, no fabricated names, no over-claimed facts (the two flagged claims — "10× SaaS" and startup base rates — are already correctly hedged/attributed in the source text). Contrast-tics ≤2/file and em-dash density under the ceiling throughout. Editing anything here would be over-editing correct, well-hedged prose. No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Fast-moving facts carry `search-verified 2026-07-17; fetch egress-blocked — liveness pass pending` stamps** per the amended protocol. A Phase-4 liveness pass should re-hit live URLs for: 2026 model pricing (Opus 4.8 $5/$25, Sonnet 5 $2/$10→$3/$15, tokenizer delta), the EU AI Act 2 Aug 2026 applicability date, and the agency-vs-SaaS margin/opportunity figures (fluxio.dev, lootr.io, bartoszcruz.com — secondary/SEO-tier domains; each load-bearing figure is corroborated across two and hedged as a contested projection).
2. **Em-dash density runs hot** (Thu 11.8, Tue/Sat 11.6 per 1k) — under the ~12 ceiling but notably above Week 20's 2.9–5.0 band. Not a fix, but a Phase-4 polish could trim a handful in the three densest files for headroom.
3. **Base-rate precision (Fri [^2]):** BLS puts 5-year survival at ~50% (roughly half) and 10-year at ~35% (well below half); the lesson's "multi-year survival well below half" is accurate for the longer horizon and slightly pessimistic at 5 years. It is hedged and attributed, so left unfixed to avoid over-editing a correct, soft claim.
4. **Week 21 dailies are not generated** — Monday's link to `week-21/_week` is correctly marked `(pending)`. When Week 21's lessons land, this marker (and any back-links) should be upgraded, mirroring the Week-20 review's wikilink-upgrade step.

---

_Review produced 2026-07-17. No files edited (none needed). No git commits made._
