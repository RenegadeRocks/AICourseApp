---
type: review
phase: 2
week: week-11
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 11 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-4-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-11-briefs.md`.

Mechanical checks run this session: `python -m py_compile` on both code-lab modules (pass, incl. after edits); full README quickstart executed offline against `sample_interviews/P3.md` — behavior matches the README exactly (8 atoms, 4 for / 4 against+neutral, all mapped to the first assumption as the offline mode warns; verdict prints; `wilson 4 74` → [2.1%, 13.1%] matching 06-sat's pass bar; synthetic atoms import at weight 0.0 and cannot trip the strength-5 check — verified in code and by run). **All 23 distinct wikilink targets resolve** to real vault files (verified by `find`), and the eight week-9/10 "(pending)" markers were upgraded — both weeks now exist in full. Em-dash density 1.8–8.9/1k (all under the ~12 cap); contrast tics ≤2/file except Fri (~4 by regex, mostly false positives on quoted material); house tics: "load-bearing" 2× total, "operator" 5× total, "would push back" 0×. WebSearch spot-checks (fetch egress-blocked this session too, so the per-citation hedges stay correct): Park et al. 2411.10109 (1,052 agents / 85% of own GSS test-retest / 2-hour interviews / reduced demographic bias) — confirmed via arXiv + Stanford HAI; Gui & Toubia 2312.15524 (~50% of aggregate treatment effects across 11 experiments; unblinding mitigation) — confirmed via arXiv + SSRN; "Lost in Simulation" 2601.17087 — real, ICLR 2026, "excessively cooperative," 9pp cross-LLM variance, miscalibration direction all confirmed; "Illusion of Intervention" 2605.20767 — real, but its claim is user-drift confounding + negative-control diagnostics, not the "sign flips" the draft asserted (fixed); Otter consolidated wiretap litigation (In re Otter.AI Privacy Litigation, 5:25-cv-06911) and Cruz v. Fireflies.AI BIPA suit — both confirmed; GummySearch shutdown over Reddit commercial-API licensing ($0.24/1k calls) — confirmed, incl. the date ambiguity Tue [^7] already hedges; NYU "Shipping Is Not a Substitute for Asking" (May 8, 2026, Rimalovski) — confirmed; Synthetic Users 85–92% vendor parity claim — confirmed as vendor-reported, which is exactly how the lesson treats it; ACM energy-HEMS study and MeasuringU review — both real. Internal corroborations checked against `_refresh-2026-07-landscape-delta.md`: $510B / $217B / 43%, Sonnet 5 $2/$10 intro through 2026-08-31, GPT-5.6 Terra, Gemini 3.5 Flash $1.50/$9 (Flash is released; only 3.5 **Pro** GA is on the do-not-teach list), Cowork 07-07 cross-platform, LinkedIn AI-outreach demotion — all match.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "AI on both sides of the validation table" is the correct one-line mechanism for the week. |
| Chip Huyen | 8 | Deliverables table maps 1:1 to the day files; time budget is honest. |
| Jerry Liu | 8 | Ledger positioned as the convergence artifact, not a gadget. |
| Hamel Husain | 8 | "Simulate to design; humans to decide" stated up front and owned by Thursday. |
| Simon Willison | 8 | The ~50%-treatment-effects line now states the claim precisely (post-polish). |
| Seibel | 9 | Sells the week in two paragraphs; "cut Tuesday, never Wednesday" is the right triage. |
| Boris Cherny | 8 | Tool expectations set correctly (stdlib, no keys). |
| Cohort peer | 9 | "Protect the decision from the person making it" is a keeper sentence. |
| Mira Murati | 8 | Commercial frame (validate before launch) without hype. |
| swyx | 8 | Block 4 loop composition earns the Sunday recap. |
| Ethan Mollick | 8 | Produces-by-Sunday list is behavioral, not aspirational. |
| Lilian Weng | 8 | Terminology consistent with the dailies (atoms, classes, kill criteria). |
| Jeremy Howard | 8 | Links carry the load; no re-teaching. |

**Weighted average: 8.1**

## 01-mon — Idea definition: from itch to falsifiable bet

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Bet-sentence schema and the "feasibility rarely binds in 2026" calibration are mechanism-first, with three honest exceptions. |
| Chip Huyen | 8 | Quantified assumption examples (6/10, ≥$300/mo, ≥90% at $0.40) are operator-shaped. |
| Jerry Liu | 8 | Assumption map correctly subordinates tools to the decision structure. |
| Hamel Husain | 9 | Pre-registration ported honestly, incl. the boundary ("makes the decision precommitted, not the study rigorous"). |
| Simon Willison | 8 | Ship-vs-discovery controversy has named positions on both sides, all search-verified; Substack "5 interviews" quoted as position, not fact. |
| Seibel | 8 | His objection is in the lens and answered by the time-box + shipped smoke test. |
| Boris Cherny | 8 | Commit-timestamp-as-receipt is the right tooling instinct. |
| Cohort peer | 9 | Escape-hatch inventory is the most usable idea in the file. |
| Mira Murati | 7 | Platform-risk treatment (open question 2) gestures without a decision aid. |
| swyx | 8 | "Wedge value concentrates where platforms don't go" is the durable heuristic. |
| Ethan Mollick | 8 | His demo-vs-dependable objection is in the lens and changes the advice. |
| Lilian Weng | 8 | 88% / $510B / pricing figures all trace to corroborated sources (canonical pointer fixed this session). |
| Jeremy Howard | 8 | Kill-criteria canonical (b0w03 Wed) linked, extended, not re-derived. |

**Weighted average: 8.1**

Notes: the 88% "canonical vault treatment" pointer named b0w03 Tue, which does not contain the stat; the canonical home is b3w08 Mon [^9]. Fixed in body + [^1].

## 02-tue — AI-assisted desk validation

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Five failure modes are mechanisms, not vibes; homogenization tied to real literature. |
| Chip Huyen | 9 | Error log as a first-class deliverable is the production habit worth the day. |
| Jerry Liu | 8 | Two-tool triangulation honestly weakened by its own Simon lens (shared index/substrate). |
| Hamel Husain | 8 | Pass bar includes "if all five verify, re-pick harder claims" — good calibration hygiene. |
| Simon Willison | 7 | Ironic weak point: the deep-research tool-comparison citations ([^1]–[^3]) are exactly the SEO-tier content Layer 6 warns about; hedged, but the thinnest sourcing of the week. |
| Seibel | 8 | Time-boxed to an afternoon with "it decided nothing, which is exactly its jurisdiction." |
| Boris Cherny | 8 | GummySearch platform-risk lesson is the correct tooling parable (verified). |
| Cohort peer | 8 | Worked example lands the bottom-up sizing reframe concretely. |
| Mira Murati | 7 | Nothing on paid/primary data sources beyond a mention. |
| swyx | 8 | "AI dossier is the commodity baseline, negative differentiation on insight" is the right ecosystem read. |
| Ethan Mollick | 8 | Verification protocol is teachable and time-costed. |
| Lilian Weng | 8 | Doshi & Hauser / 2501.19361 / Kleinberg & Raghavan triangulation is the correct evidence set. |
| Jeremy Howard | 8 | Tool-fossilization risk named in his own lens, with the vault's D+ precedent cited. |

**Weighted average: 7.9**

## 03-wed — Interviews that don't lie to you

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four agent-product probe families are a genuine extension of the Mom Test, not a rehash. |
| Chip Huyen | 8 | Recruiting-channel hierarchy with reply-rate expectations and real panel prices (corroborated). |
| Jerry Liu | 8 | Atom schema is a clean data model that Saturday's tool implements verbatim. |
| Hamel Husain | 9 | His inter-annotator critique appears in the lens *against the lesson's own solo protocol* and the tool ships the fix (`--audit`). |
| Simon Willison | 8 | Consent/lawsuit material verified (Otter consolidation, Cruz v. Fireflies BIPA); conservative protocol correctly above every proposed bar. |
| Seibel | 8 | His "hide from the currency close inside guide engineering" warning is the true failure mode. |
| Boris Cherny | 8 | No-autonomous-notetaker rule matches the live litigation fact pattern. |
| Cohort peer | 9 | "Send the three cold messages before you re-read anything" is the intervention that matters. |
| Mira Murati | 7 | AI-moderated-interview vendors named but not evaluated. |
| swyx | 8 | Saturation-within-the-wedge resolution of the how-many debate is defensible. |
| Ethan Mollick | 8 | Worked P3 atomization shows a flattering interview yielding pivot signal — the pedagogy works. |
| Lilian Weng | 8 | Disconfirmation quota + prefer-AGAINST rule are consistent with Thursday's sycophancy evidence. |
| Jeremy Howard | 8 | Consent-law geometry ceded to b3w07 Thu with a ported protocol only — compliant. |

**Weighted average: 8.1**

## 04-thu — Synthetic users: promise and peril (centerpiece)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Layer 4's four mechanisms let the reader predict untested failure cases — the rare generalizing move. |
| Chip Huyen | 8 | Three-way taxonomy (respondent / AI-moderated / system harness) dissolves most of the discourse confusion. |
| Jerry Liu | 8 | "Output checked by something other than the simulation" is the correct structural test for permitted uses. |
| Hamel Husain | 9 | Zero-weight rule + his own lens demanding the divergence audit become a standing instrument — dogma upgraded to dashboard. |
| Simon Willison | 9 | Both sides' citations are real and correctly characterized (spot-checked: Park, Gui & Toubia, Lost in Simulation, Kapania, NN/g, Illusion of Intervention, ACM HEMS, MeasuringU); vendor parity numbers labeled vendor-reported; the Park result read as "best pro evidence AND best argument cheap personas are hollow" is exactly right. |
| Seibel | 8 | Worked example (panel silent on the wedge-breaking insight) makes the abstract peril concrete. |
| Boris Cherny | 8 | Fresh-context-per-persona and shared-chat-bleed warnings are correct practice. |
| Cohort peer | 8 | Divergence audit is runnable in 90 minutes with the reader's own data. |
| Mira Murati | 8 | Interview-grounded-twin open question engages the strongest future counter-case with pre-written acceptance criteria. |
| swyx | 8 | Vendor-blur critique (parity on attitudinal replication marketed as discovery) is the honest industry read. |
| Ethan Mollick | 8 | His actual pro-simulation position is steelmanned in the lens and answered as decision-hygiene, not capability denial. |
| Lilian Weng | 8 | Her single-study/model-generation caveat is in the lens; "Illusion" claim now matches the paper (fixed). |
| Jeremy Howard | 8 | Weight-zero protocol internally consistent with Tuesday (desk 0.5 because human-generated; synthetic 0 because errors correlate with hope) and with the Sunday quiz (Q8, Q12, A9). |

**Weighted average: 8.3**

Consistency audit vs Tuesday and Sunday: sycophancy/homogenization mechanisms identical across Tue Layer 6, Thu Layers 3–4, Sun A9/A12 and flashcards 10, 12, 23–26; the feasibility partial exception (Layer 5) is the one seam the tool doesn't model — see unresolved concerns.

## 05-fri — Polls, smoke tests, and the evidence ledger

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Ladder-as-menu-priced-by-evidence-cost, and the Layer 6 concession that rungs 2 and 4 have nearly merged, is honest 2026 thinking. |
| Chip Huyen | 9 | Class weights with the three properties that matter (pre-written, money ≫ talk, synthetic 0) and the strongest-single-AGAINST display. |
| Jerry Liu | 9 | His lens correctly spots the ledger as a sellable retrieval-and-synthesis artifact — the Week 12 seed. |
| Hamel Husain | 8 | Un-calibrated 0–5 strengths named as the weakest joint in his own lens, with the rubric-config fix shipped Saturday. |
| Simon Willison | 7 | Waitlist/pre-order benchmarks are vendor-published and single-source-ish ([^2][^3][^6]); hedged as priors, but [^3]'s "2%-typical" note sits awkwardly beside the body's "11% median." |
| Seibel | 8 | Layer 6 concedes his point and holds exactly one line (pre-registration) against him — the right trade. |
| Boris Cherny | 8 | Pre-registration-commit-before-traffic is verifiable by timestamp; instrument-the-decision-points list is correct. |
| Cohort peer | 8 | Refusal-interviews mistake (#8) is the highest-value cheap habit in the file. |
| Mira Murati | 7 | Adaptive/sequential alternative named but not taught, defensible scope. |
| swyx | 8 | "Are fake doors becoming untenable" open question is the live 2026 debate, positioned weakly-held. |
| Ethan Mollick | 8 | Delegation-depth-over-signups is the agent-product metric that matters, per the brief. |
| Lilian Weng | 8 | Wilson discipline imported by link (b2w03 canonical), not re-derived — compliant; worked-example intervals check against the tool. |
| Jeremy Howard | 8 | Buffer specimen + Pew wording work are the right evergreen anchors. |

**Weighted average: 8.0**

## 06-sat — BUILD: run the validation sprint

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Layer 2's architecture notes (why the tool is shaped this way, what it deliberately doesn't automate) are the systems content. |
| Chip Huyen | 8 | Worked sprint ends with real numbers, an EXTEND clause firing, and a $150 total cost line. |
| Jerry Liu | 8 | Backfill-the-week step makes the ledger the week's single convergence point. |
| Hamel Husain | 9 | Audit loop + "compute the model-vs-human agreement rate and write it in the memo" is the course's eval thesis, enacted. |
| Simon Willison | 8 | "The tool makes self-deception visible, not impossible" is the honest security posture; doc claims match shipped code (verified by run; one gap fixed). |
| Seibel | 9 | His spreadsheet-and-honesty null hypothesis is quoted *and* granted status as a respectable alternative — rare. |
| Boris Cherny | 9 | His automation critique is in the lens with the correct "resisted for pedagogy, right for Week 12" answer; his offline-tagger complaint is accurate to the code. |
| Cohort peer | 9 | Timed session with a pass bar per artifact; "calendar or it isn't real." |
| Mira Murati | 7 | No stretch goal beyond the CLI (e.g., the standing-panel question from Thursday). |
| swyx | 8 | "When does the CLI deserve to become a product" closes the loop on the block's commercial frame. |
| Ethan Mollick | 9 | Witnessed-decision requirement is behavior design grounded in the week's own motivated-reasoning thesis. |
| Lilian Weng | 8 | Shankar et al. validator-validation citation is the right basis for `--audit`. |
| Jeremy Howard | 8 | GV Sprint borrowed for skeleton only; Bland sequencing linked, not re-taught. |

**Weighted average: 8.3**

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Q8 tests the structural property (downstream check exists or doesn't), not citation recall. |
| Chip Huyen | 8 | Block 4 loop (validate → package → launch → loop) is the right composition, with data paths in A15. |
| Jerry Liu | 8 | A15's two concrete data paths trace faithfully to the running example. |
| Hamel Husain | 9 | Q11/A11 (interval straddles → collect more n) and Q12/A12 (the weight asymmetry) test the discipline, not the trivia. |
| Simon Willison | 8 | A7's numbers verified against both papers; A4's GummySearch facts corroborated. |
| Seibel | 8 | "Ten humans who now know you do research before you sell" is the compounding asset, correctly last. |
| Boris Cherny | 8 | A14's override mechanics match the shipped tool. |
| Cohort peer | 9 | Quiz difficulty calibrated; Q11 arithmetic now matches the tool's own output (fixed 13.7→13.8). |
| Mira Murati | 7 | Capstone recap stays inside the course's own artifacts. |
| swyx | 8 | Flashcard 34 compresses the block into one loop with both gates named. |
| Ethan Mollick | 9 | Sunday-night ritual routes weak quiz scores into `/deepen-lesson` — closed loop. |
| Lilian Weng | 8 | All 34 flashcards check against the weekday lessons; no contradictions found. |
| Jeremy Howard | 8 | No duplicate territory with b0w03 or b2w03 quizzes. |

**Weighted average: 8.2**

Consistency audit (Sunday vs weekdays): shared numbers identical across files — 85% / 1,052 / 2h; ~50% / 11 experiments; 9pp; 85–92% vendor parity; $0.24/1k; 12 all-party states; weights 5/3/1/0.5/0; ladder order; 88%; $20/month default. Q11's interval now matches `wilson 6 90` exactly.

## code-lab/6 (README, requirements, evidence_ledger.py, note_synthesizer.py, sample_interviews/P3.md)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Small, readable, single-file tools; the weight/mass arithmetic is inspectable in one screen. |
| Chip Huyen | 8 | Verdict prints checks with PASS/FAIL and the pivot/kill clauses — decision-shaped output. |
| Jerry Liu | 8 | Atom schema matches Wednesday's lesson exactly; import validates directions/classes/strengths. |
| Hamel Husain | 9 | Strength rubric embedded in the ledger file, anti-sycophancy prompt clause, `--audit` blind sampler — the week's discipline, shipped. |
| Simon Willison | 8 | No keys read or stored; synthetic weight-0 enforced in scoring *and* excluded from the strength-5 tripwire; honest "you can defeat this in a text editor" note. |
| Seibel | 8 | Teaching implementation that admits it; quickstart runs in five minutes as claimed (verified). |
| Boris Cherny | 7 | Offline mode maps every atom to the first assumption silently at runtime (documented in README, but the run output itself doesn't warn); `claude -p` path untestable this session. |
| Cohort peer | 9 | README commands reproduce exactly; sample P3.md doubles as the Wednesday worked example. |
| Mira Murati | 7 | No JSON-schema validation of Claude-mode output beyond field checks; fine for scope. |
| swyx | 8 | The tool is one rename from the client-facing product Sat's open question 3 describes. |
| Ethan Mollick | 8 | Printed reminders at every synthetic touchpoint (now including import) are good default paternalism. |
| Lilian Weng | 8 | Wilson implementation checked against hand computation for 4/74, 6/90, 8/80 — correct. |
| Jeremy Howard | 8 | Stdlib-only with an intentionally empty requirements.txt — right dependency posture for a decision tool. |

**Weighted average: 8.0**

---

## Overall Week 11: **8.1 / 10**

(File averages: 8.1, 8.1, 7.9, 8.1, 8.3, 8.0, 8.3, 8.2, 8.0.) Strongest: Thursday and Saturday — the centerpiece controversy is engaged with verified evidence on both sides and then *compiled into the tooling*, which is the week's distinctive move. Weakest: Tuesday's and Friday's benchmark sourcing (SEO-tier comparison blogs, vendor waitlist stats) — both are hedged in-line as priors, which is the correct posture, but they are the thinnest citations. Anti-slop: clean across the board (em-dash max 8.9/1k, contrast tics within budget, house tics near zero). Canonical homes: all seven (b0w03 discovery + kill criteria, b1w01 discovery calls + pilots, b1w02 niche, b2w03 landing + Wilson, b2w04 evals, b3w07 consent, b3w08 scraping + reliability) wikilinked with one-line recaps — no re-teaching found; b0w03 Mon's JTBD material is referenced, never re-derived.

## Surgical fixes applied this session (Phase 3, done)

1. **Week 9/10 "(pending)" markers removed** — 8 occurrences across 00-overview (2), 01-mon, 02-tue, 05-fri (2), 07-sun (2). Both weeks now exist in full; targets verified.
2. **01-mon 88%-stat canonical pointer** (body + [^1]): pointed at b0w03 Tue, which does not contain the Anaconda/Forrester figure; now points at its real canonical home, b3w08 Mon.
3. **04-thu "Illusion of Intervention"** (Layer 3 + [^4]): the draft asserted the paper "demonstrates sign flips on realistic marketing questions"; the paper's verified claim is intervention-induced user-drift confounding that inflates/attenuates estimates, with negative-control outcomes as the diagnostic. Reworded to match; no strength lost.
4. **07-sun Q11/A11**: [3.1%, 13.7%] → [3.1%, 13.8%] to match the shipped `wilson` command's output for 6/90 (verified by run).
5. **00-overview**: "users whose enthusiasm replicates only about half of real human treatment effects" conflated the finding; now "users that replicate only about half of real human treatment effects."
6. **evidence_ledger.py `import-atoms`**: 06-sat claims "the tools print the reminder every time you touch them" for synthetic atoms, but the import path printed nothing; a weight-0.0 reminder now prints when any imported atom is synthetic. Re-compiled and re-run clean.

## Unresolved concerns (recommendations, not applied)

1. **Feasibility-exception seam (04-thu Layer 5 vs the tool).** Thursday permits simulated *load on your own system* as feasibility evidence, but the ledger zero-weights everything tagged `synthetic`, including feasibility atoms. In practice a system-test result should probably be logged as `behavioral` (the thing measured is your system), but no lesson says so explicitly. One sentence in Thu Layer 5 or the README would close it; left for the author since it is a design decision.
2. **Word counts** run 3.3–4.6K vs the L3 4.5–6.5K soft target on every daily (same pattern the Week 6 review accepted). Density is genuinely high; Tue and Fri could each absorb ~500 words on the gaps their own lenses name (a non-search triangulation leg; adaptive testing).
3. **Tue [^1]–[^3] / Fri [^2][^3][^6] sourcing** is the citation weak point: deep-research comparisons and waitlist benchmarks from SEO/vendor-tier sites. In-text hedges are correct; Phase 4 should try to land at least one primary or practitioner-grade source for each.
4. **Fri [^3] internal wobble**: body cites an ~11% median waitlist conversion; the footnote says Flowjam corroborates a "2%-typical / 20%-excellent spread." Both are vendor priors and the body says so, but the two framings should be reconciled when the liveness pass runs.

## Phase 4 citation-verify list (liveness pass, when egress opens)

1. Mon [^8]/[^9]: andresmax.com and the Traction Thinking Substack posts — confirm the pages exist with the quoted positions ("5 conversations then ship"; ">5 interviews is procrastination").
2. Tue [^1][^2][^3]: the three deep-research comparison pages — liveness + whether the tool-positioning claims still hold.
3. Tue [^12]/Fri [^6]: userintuition.ai reference guide (shared source) — liveness and the 8–15% / >1% / 1–3% benchmark set.
4. Wed [^3][^4][^5]: User Interviews $49/$98 pay-as-you-go and Respondent's 50%-of-incentive/$40-minimum pricing against the live pricing pages.
5. Wed [^9]: Basil AI's "12 all-party-consent states" list against recordinglaw.com's state table.
6. Thu [^1]: syntheticusers.com science-post URL and the 85–92% parity page.
7. Thu [^10]: ACM DOI 10.1145/3765611.3815484 resolves (confirmed via search this session; DOI itself unfetched).
8. Fri [^2][^3]: waitlister.me / flowjam benchmark pages — liveness + reconcile concern 4.
9. Sun/Mon: Sonnet 5 intro-pricing end date 2026-08-31 against the Anthropic pricing page.

---

_Review + surgical polish produced 2026-07-17 (session run 2026-07-18). Files edited: 00-overview, 01-mon, 02-tue (pending-marker only), 04-thu, 05-fri (pending-markers only), 07-sun, code-lab/6/evidence_ledger.py. No git commits made._
