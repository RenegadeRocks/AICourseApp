---
type: review
phase: 2
week: week-17
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 17 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-6-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-17-briefs.md`.

Mechanical checks run this session: `python -m py_compile` on all three code-lab files (clean); `python test_growth_sim.py` → **`OK — 8 tests passed`**; `python growth_sim.py` and `python pmf_analyzer.py` both run and reproduce every number the lessons quote. Hand-checked the k-factor math: `k_factor(0.30, 3.0, 0.15) = 0.135`, the 50%-refer lift `= 0.225`, Saturday's `k_factor(0.35, 2.5, 0.18) = 0.158`, loop amplification `0.65·0.35·0.72 = 0.164` with weakest handoff `invites_teammate` and marginal lift `0.094` — all reproduce exactly. Saturating projection caps at ~1,946 (README's "~1,950"), never infinity — the anti-hockey-stick point the code exists to make. All cross-block wikilink targets resolve to real files (b4w11 interviews, b5w14 mon+wed, b4w10 fri, b3w08 wed, b5w13 sat); all intra-week links resolve. Em-dash density 2.7–4.6/1k across all eight files (far under the ~12 bar). Contrast-scaffold tics within budget on spot-check. Internal-consistency audit across dailies/Sunday/code-lab: Sean Ellis 40% line, Superhuman 22%→32%→58%, Dropbox k 0.24→0.56 (≈0.5) / invites 1.2→2.8 / 100k→4M / "3900%", PayPal $20+$20→$10→$5 / $60–70M / 7–10% daily, reactivation 5–10x (hedged), Klaviyo ~10% win-back, k-regime bands (>1 / 0.7–1.0 / 0.3–0.7 / 0.15–0.25), Privacy Sandbox retired Oct 17 2025, FTC click-to-cancel vacated (8th Cir. July 2025) + March 11 2026 ANPRM + Uber UberOne — all reproduce identically. Canonical homes (b4w11 validation, b5w14 analytics, b4w10 instrumentation, b3w08 consent, b5w13 shareable artifact) are recap-plus-wikilink, never re-taught.

**NAME-VERIFICATION (required this week):** both non-core growth authorities are real, correctly spelled, and correctly attributed — no "Max Freiberg" repeat.

- **Andrew Chen** — General Partner at Andreessen Horowitz (a16z), author of *The Cold Start Problem: How to Start and Scale Network Effects* (Harper Business, 2021), former head of rider growth at Uber. Corroborated ≥2 independent domains (a16z.com/author/andrew-chen, a16z.com/books/the-cold-start-problem, amazon.com, penguin.co.uk, goodreads.com). Week 17 cites him for the "Law of Shitty Clickthroughs" and viral-loop saturation — both are genuinely his (andrewchen.com / his Substack). Attribution accurate. **Verified.**
- **Elena Verna** — Head of Growth at Lovable as of 2026, previously growth leadership at SurveyMonkey, Miro, Amplitude, and Dropbox. Corroborated ≥2 independent domains (linkedin.com/in/elenaverna, lennysnewsletter.com "The new AI growth playbook for 2026", stripe.com/sessions/2026, growthtalent.org). The fast-moving current-title claim ("now Head of Growth at Lovable, formerly Amplitude/Miro/SurveyMonkey/Dropbox") is **confirmed accurate**, not merely plausible — no softening required. The Racecar framing (loops=engine, tactics=turbo, funnels=fuel) is correctly hers. **Verified.**

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Launch is a spike, price is a number, neither compounds" is the real mechanism, not a slogan. |
| Chip Huyen | 8 | Day table maps to concrete deliverables; through-line subordinates growth to retention. |
| Jerry Liu | 8 | Correctly frames the week as the layer on top of measurement, not new measurement. |
| Hamel Husain | 8 | "What you can do by Sunday" is behavioral and checkable. |
| Simon Willison | 8 | FTC/dark-pattern line named up front, not hyped. |
| Seibel | 8 | Sells the week honestly in two paragraphs; leaky-bucket closer is right operating advice. |
| Boris Cherny | 7 | Light on tooling, appropriate for an overview. |
| Cohort peer | 8 | Ties Weeks 15/16/17 into one arc cleanly. |
| Mira Murati | 8 | Commercial framing without hype. |
| swyx | 8 | Loop-vs-funnel thesis stated crisply. |
| Ethan Mollick | 8 | Study-order and expectations framing is real behavior design. |
| Lilian Weng | 8 | Terminology consistent with the dailies. |
| Jeremy Howard | 8 | Prereq wikilinks (b4/b5) carry the load. |

**Weighted average: 7.9**

---

## 01-mon — The feedback engine

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Feedback is ore, not the roadmap" is the honest mechanism; four-stage smelting is real. |
| Chip Huyen | 8 | Evidence-weight prioritization (distinct users, segment) beats volume; correct. |
| Jerry Liu | 8 | LLM review-mining framed as a pre-pass to verify, not ground truth. |
| Hamel Husain | 9 | His lens is in the text: one human reading 50 tickets; code is deliberately a pre-pass to reading. |
| Simon Willison | 8 | NPS critique cited to peer-reviewed sources, not vibes. |
| Seibel | 9 | His "call ten users, skip the pipeline" pushback is the reviewer lens, conceded and bounded. |
| Boris Cherny | 8 | `feedback_triage.py` is a defensible deterministic tagger with a clear pass bar. |
| Cohort peer | 8 | Superhuman segmentation made concrete and copyable. |
| Mira Murati | 8 | Trust-is-contextual note apt for AI products. |
| swyx | 8 | Close-the-loop as compounding investment is the right framing. |
| Ethan Mollick | 8 | His quality-drift caveat is in the lens and tied to Week 14. |
| Lilian Weng | 8 | Sean Ellis wording/thresholds consistent with Sunday and the code. |
| Jeremy Howard | 8 | b4w11/b5w14 recapped + wikilinked, not re-taught. |

**Weighted average: 8.2**

---

## 02-tue — Retargeting & re-engagement

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Lifecycle states as the mechanism; trigger-over-calendar is the real lever. |
| Chip Huyen | 9 | His selection-effect lens ("reactivation retains better is not causal — measure incrementality") is the sharpest voice this week. |
| Jerry Liu | 8 | Trigger taxonomy ranked by power, not listed flat. |
| Hamel Husain | 8 | `reengagement.py` pass bar forces guards-before-targeting; measurable. |
| Simon Willison | 9 | His lens on the privacy/consent surface (behavioral data into a prompt) is precise and in-text. |
| Seibel | 8 | "Don't build this until you have a dormant pool" pushback conceded and bounded. |
| Boris Cherny | 8 | Honesty guards wired as suppress-only is a clean implementation rule. |
| Cohort peer | 8 | Cancel-survey-as-truth is directly actionable. |
| Mira Murati | 8 | Ethics line drawn on stakes, not moralizing. |
| swyx | 8 | Post-cookie retargeting reality current and correctly de-hyped. |
| Ethan Mollick | 8 | "Walk your cancel flow as a hostile regulator" is good behavior design. |
| Lilian Weng | 8 | Four lifecycle states consistent with Sunday's cards. |
| Jeremy Howard | 8 | Cookie/FTC facts hedged and dual-sourced per protocol. |

**Weighted average: 8.3**

---

## 03-wed — Growth loops vs funnels

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Reinvestment as the addition-vs-multiplication mechanism is the correct core. |
| Chip Huyen | 9 | His cost-per-loop-cycle / inference-bill pushback is the non-obvious AI-specific lens. |
| Jerry Liu | 8 | Four loop families with a "run one" discipline, not a taxonomy dump. |
| Hamel Husain | 8 | Three loop numbers (amplification/cycle-time/weakest-handoff) are measurable. |
| Simon Willison | 8 | Output-as-marketing claims bounded ("watermarking mediocre output spreads mediocrity"). |
| Seibel | 8 | "Build the share button and watch, don't draw the diagram" is the reviewer lens. |
| Boris Cherny | 7 | Instrumentation described but not wired here (it lands in Saturday's code-lab). |
| Cohort peer | 8 | Loop-mapping table for the meeting-notes product is concrete. |
| Mira Murati | 8 | AI-native loop framed on genuine novelty, not gimmick. |
| swyx | 8 | Balfour/Verna framing current and correctly attributed. |
| Ethan Mollick | 8 | Weakest-handoff worked example teaches the one-place-to-push lesson. |
| Lilian Weng | 8 | Law-of-Shitty-Clickthroughs decay consistent with Thursday/Friday. |
| Jeremy Howard | 8 | b5w13/b5w14 wikilinked, not re-taught. |

**Weighted average: 8.1**

---

## 04-thu — Referral & virality engineering

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | k = invites × conversion with the honesty in the inputs is the right mechanism. |
| Chip Huyen | 8 | Saturation-lowers-k stated as a hard constraint on projections. |
| Jerry Liu | 8 | Dropbox/PayPal read for what they teach, not the mythology. |
| Hamel Husain | 9 | Worked k example with an explicit pass bar (write your three inputs, state the regime). |
| Simon Willison | 8 | Fraud-guard section names real attacks and real mitigations. |
| Seibel | 9 | "Do enough people love this to tell a friend unprompted?" is the reviewer lens and the gate. |
| Boris Cherny | 9 | His over-engineering-the-fraud-detector pushback (household IP/NAT false positives) is precise. |
| Cohort peer | 8 | Four incentive decisions are a copyable checklist. |
| Mira Murati | 8 | Controversy resolved conditionally, not tribally. |
| swyx | 8 | Named-positions controversy with real 2026 sources on both sides. |
| Ethan Mollick | 8 | Reflection Q5 forces you to take a side with your own math. |
| Lilian Weng | 8 | k-regimes and Dropbox ≈0.5 consistent with code and Sunday. |
| Jeremy Howard | 8 | Benchmark figures flagged as rules of thumb, not laws. |

**Weighted average: 8.3**

---

## 05-fri — The growth system & honest measurement

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Retention-as-multiplier, growth-as-multiplicand is the correct architecture. |
| Chip Huyen | 9 | His holdout/incrementality pushback recurs and is the measurement rigor growth skips. |
| Jerry Liu | 8 | Input-metric tree with retention explicitly in the middle is the right decomposition. |
| Hamel Husain | 8 | Stress-test-the-joints checklist is blunt and actionable. |
| Simon Willison | 8 | Vanity-metric tell ("a healthy metric can go down") is a clean instrument test. |
| Seibel | 9 | "Almost nobody has earned the right to optimize growth" is the reviewer lens, pushed further. |
| Boris Cherny | 7 | Less tooling surface here; appropriate for a synthesis lesson. |
| Cohort peer | 8 | Sustainable-vs-mercenary fork stated as a conscious choice. |
| Mira Murati | 8 | Stopping-condition decision rule is genuinely strategic. |
| swyx | 8 | Verna's Racecar framing correctly reused. |
| Ethan Mollick | 8 | "What happens when I stop?" is a memorable diagnostic. |
| Lilian Weng | 8 | North-star/counter-metric vocabulary consistent with Week 14 and Sunday. |
| Jeremy Howard | 8 | Growth-hacking-2026 reframe dual-sourced. |

**Weighted average: 8.2**

---

## 06-sat — BUILD: assemble your growth system

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four components built in dependency order; Component 1 gates Component 4. |
| Chip Huyen | 8 | PMF-gates-referral logic is the honest unit-economics discipline. |
| Jerry Liu | 8 | Worked assembly uses the actual code-lab tools end to end. |
| Hamel Husain | 9 | Pass bar is measurable and honesty is the pass condition ("go back to the product" is a passing result). |
| Simon Willison | 8 | Guards-first re-engagement carried into the build spec. |
| Seibel | 9 | "Ship the crude version of all four, not a perfect one" is the reviewer lens. |
| Boris Cherny | 8 | His fraud-guard over-build warning restated with the retained-action fix. |
| Cohort peer | 8 | One-page deliverable is a real artifact, not a deck. |
| Mira Murati | 7 | Model-choice absent; inherited from earlier days, defensible. |
| swyx | 8 | code-lab tool calls (`k_factor`/`project_viral`/`loop_efficiency`) match the module. |
| Ethan Mollick | 8 | Reflection questions convert the build into scheduled decisions. |
| Lilian Weng | 8 | Component numbers (34% aggregate / 58% segment example) internally coherent. |
| Jeremy Howard | 8 | Saturating projection taught as the correction to the straight-line lie. |

**Weighted average: 8.2**

---

## 07-sun — Synthesis + quiz + flashcards + Block 6 capstone

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | One-sentence-per-day compression is accurate; quiz rewards applying rules. |
| Chip Huyen | 8 | Q4/A4 and the incrementality flashcard carry the selection-effect discipline. |
| Jerry Liu | 8 | Capstone "sequence and a stack" framing is the right synthesis of the block. |
| Hamel Husain | 8 | Answer key precise; scoring bands direct rereads. |
| Simon Willison | 8 | Q6/Q14 (cookies, FTC) answers match the dailies exactly. |
| Seibel | 8 | His capstone lens ("more talking to users, less growth engineering") is the honest close. |
| Boris Cherny | 8 | Q11 weakest-handoff answer traces to the code and Wednesday. |
| Cohort peer | 8 | 15-question quiz + 32 flashcards well calibrated; cold-quiz instruction correct. |
| Mira Murati | 7 | Forward pointers commercial; no capability-frontier note. |
| swyx | 8 | k-regime and Dropbox cards current and consistent. |
| Ethan Mollick | 8 | Jeremy-Howard lens ("benchmarks are hypotheses") is the right meta-lesson. |
| Lilian Weng | 8 | All flashcards checked against weekday lessons; no contradictions. |
| Jeremy Howard | 8 | No duplicate territory with earlier weeks; builds on the block. |

**Weighted average: 8.0**

---

## code-lab/1 (README, requirements.txt, growth_sim.py, pmf_analyzer.py, test_growth_sim.py)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Zero-dependency stdlib; the saturating projection loop is readable and models the real mechanism. |
| Chip Huyen | 8 | Effective-k decay and steady-state cap make the anti-hockey-stick point quantitatively. |
| Jerry Liu | 8 | Each function maps to a specific Week 17 concept; import path shown for own-data use. |
| Hamel Husain | 9 | `test_growth_sim.py` exits 0 with 8 passing assertions; doubles as a compile check. |
| Simon Willison | 9 | No network, no keys, offline; input ranges validated with `ValueError` guards. |
| Seibel | 8 | Tiny enough to wire estimates today and replace with real data next week. |
| Boris Cherny | 8 | `X | None` union pins Python 3.10+; README states it. |
| Cohort peer | 8 | README pass bar is runnable top to bottom and its four outputs reproduce. |
| Mira Murati | 7 | Single deterministic model of growth; no stochastic variance, defensible for teaching. |
| swyx | 8 | pmf_analyzer segments the survey the Superhuman way, matching Monday. |
| Ethan Mollick | 8 | Demo outputs tie directly to Saturday's decision rule. |
| Lilian Weng | 8 | k-regime bands in `regime()` match the Thursday lesson exactly. |
| Jeremy Howard | 9 | Small, deterministic, honest about which numbers are rules of thumb. |

**Weighted average: 8.3**

---

## Overall Week 17: **8.2 / 10**

(File averages: 7.9, 8.2, 8.3, 8.1, 8.2, 8.2, 8.0, code-lab 8.3.) Strongest: Tuesday, Thursday, and the code-lab — reviewer lenses that genuinely argue against the text (Chip on the reactivation selection-effect and cost-per-loop-cycle, Boris on over-built fraud detection, Seibel on earning the right to optimize growth) and a lab that runs, tests clean, and exists specifically to kill the constant-k projection lie. Anti-slop: em-dash 2.7–4.6/1k (well under ~12); house tics inside budget. Canonical homes all wikilinked with one-line recaps — no re-teaching found. Both non-core growth authorities (Andrew Chen, Elena Verna) verified real and correctly attributed, including Verna's fast-moving Lovable title.

---

## Surgical fixes applied this session (Phase 3, done)

1. **07-sun capstone, Week 15 link:** upgraded folder link `[[…week-15…|Week 15]] (pending)` → `[[…week-15…/00-overview|Week 15]]` and removed the `(pending)` marker (Week 15 now exists).
2. **07-sun capstone, Week 16 link:** upgraded folder link `[[…week-16…|Week 16]] (pending)` → `[[…week-16…/00-overview|Week 16]]` and removed the `(pending)` marker (Week 16 now exists).
3. **06-sat frontmatter:** `last_verified: 2026-09-12` → `2026-07-17` (had accidentally copied the `date_due` value; the end-of-file stamp was already correct at 2026-07-17 and every other file's frontmatter reads 2026-07-17).

No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Word counts run under the L3 4,500–6,500 soft target** on every daily (Mon ~3.2K, Tue ~3.0K, Wed ~2.8K, Thu ~3.2K, Fri ~2.6K; Sat ~2.1K and Sun ~3.3K have lower intrinsic targets). Density is high and the brief says density over length, so this is a soft miss, not a defect. Wed (Boris's instrumentation) and Fri (Chip's incrementality/holdout mechanics) could each absorb ~400–600 words without padding.
2. **Fast-moving facts carry `search-verified … fetch egress-blocked — liveness pass pending` stamps** per the amended protocol. A Phase-4 liveness pass should re-hit the live URLs for: Privacy Sandbox Oct-2025 retirement, the FTC March-11-2026 ANPRM + Uber UberOne complaint, Klaviyo 2025 win-back benchmark, and Verna's current Lovable title (confirmed live this session, but it will drift).
3. **Several benchmark citations are practitioner/SEO-tier** (Stackmatix, Formbricks, Eightx, Finsi, getlaunchlist, viral-loops, Consenteo, Segwise). Each load-bearing figure is hedged in-text as directional and dual-sourced, which is the correct mitigation; Phase 4 could hunt a stronger primary for the 5–10x reactivation figure and the Klaviyo ~10% number specifically.
4. **06-sat Component 1 worked example uses a 34%-aggregate / 58%-segment scenario** that differs from the `pmf_analyzer.py` demo (38% / 75%). Both are internally correct and clearly presented as separate illustrations (the lesson's is the meeting-notes narrative; the code's is the module demo), so this is not a consistency defect — but a Phase-4 pass could align them to reduce reader friction.

---

_Review + surgical polish produced 2026-07-17. Files edited: 07-sun-synthesis-quiz-flashcards.md, 06-sat-build-the-growth-system.md. No git commits made._
