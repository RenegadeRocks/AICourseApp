---
type: review
phase: 2
week: week-18
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 18 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-7-briefs/_generator-base.md` (anti-slop + canonical-home map + amended verification protocol), and `week-18-briefs.md`.

**Mechanical checks run this session:** `python -m py_compile funnel_metrics.py distribution_planner.py test_funnel_metrics.py` — **clean**. `python test_funnel_metrics.py` prints **`OK — 14 tests passed`** as claimed. The demo reproduces the load-bearing rules exactly: paid-test decision returns **SCALE** at CAC $116.67 (< scale line 120), **INSUFFICIENT_DATA** on the small-N guard (4 customers < min 5 → CAC $262 not acted on; $300 spend < min_spend 1000 → held), **KILL** at CAC $300 (> 200), **KEEP_TESTING** at CAC $150; funnel roll-up 20%/72%/25%/15% → overall 0.54%, weakest handoff `trials->customers` (15%). All ten distinct cross-week wikilink targets resolve to real vault files (b1w02, b4w10 ×2, b6w15 ×2, b6w16, b6w17 ×2, b2w03, and the b7w19 forward link). The single `(pending)` marker (Sun → Week 19) was **upgraded** — Week 19 exists on disk. Em-dash density 1.8–5.4/1k across all eight files (Sat 5.4 the ceiling; well under ~12). Contrast-scaffold tics ≤2/file everywhere. Date normalization: the generator left **48** `search-verified 2026-07-19` / `last_verified: 2026-07-19` stamps across all eight lessons — **all normalized to 2026-07-17** this session for vault consistency (code-lab and `_week.md` carried none).

**Internal-consistency audit** (dailies vs Sunday vs quiz/flashcards vs code-lab, all reproduce identically): spam-complaint ceiling 0.30% (enforcement) / 0.10% (attention); 550-rejection regime; interactive ~70% lift, quizzes ~40%, AI-adaptive ~47%; ebooks 4–8%, webinars 6–12%, calculators 28–42%; LinkedIn carousel ~6.6% ER / video ~5.6% / in-body link ~60% reach penalty / first-60-min reach; Meta Advantage+ ~82% adoption / ~22% ROAS lift / ~25 conv-threshold; test budget $50–100/day, ~50 conv/ad-set/week, ~$1,500–3,000/mo; LinkedIn CPL $50–130 (median ~$75–110), Reddit CPL $15–40; attribution loss 50–70%, ATT opt-in 18–25%, 40–60% modeled, CAPI recovers 15–25%; scale ~20–30%, 70/30 split; the worked-example spine (spend $1,050, 168 confirmed, 9 customers, CPL $6.25, CAC $117, rule 150/120/200/1000/5) — **all consistent across every file where they appear**, and identical to the code-lab.

**NAME-VERIFICATION (required this week):** two named non-core authorities, both real; one attribution corrected.

- **Alex Hormozi — "$100M Leads" (Acquisition.com, 2023).** Real; founder of Acquisition.com; the book's lead-magnet framing ("a complete solution to a narrow problem"; give away the what/why, sell implementation) matches Mon's use. Corroborated ≥2 independent domains. **Verified, correctly attributed.**
- **Chris Walker — Refine Labs.** Real demand-gen figure, ungated-content advocate, founded Refine Labs (2019). Corroborated ≥2 domains (refinelabs.com, forbes.com, usergems.com, typeform.com). **However** the lesson called him "CEO of Refine Labs" — he **exited as CEO in July 2025** (Megan Bowen now leads). Stale title **corrected to "founder"** in both the body and citation [^5] this session. **Verified with fix.**

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "A lead is only worth capturing if you have a place to put it and a next step" is the real mechanism up front. |
| Chip Huyen | 8 | Day table maps each day to a concrete owned artifact. |
| Jerry Liu | 8 | Orders the four components correctly (magnet→funnel→organic→paid). |
| Hamel Husain | 8 | "Pre-register the kill/scale threshold before you spend" is a measured bar. |
| Simon Willison | 8 | Fast-moving claims deferred to dailies with stamps, not hyped here. |
| Seibel | 8 | Sells the week in two paragraphs; the ordering discipline is the point. |
| Boris Cherny | 7 | Points at code-lab/1 without over-explaining; light on tooling. |
| Cohort peer | 8 | "Most founders build a magnet with no funnel" lands for a first-timer. |
| Mira Murati | 7 | Commercial framing sound; no capability-frontier context. |
| swyx | 8 | The "sequence, in the right order" meta-point is the correct read. |
| Ethan Mollick | 8 | "What you will own by Sunday" is real behavior design. |
| Lilian Weng | 8 | Terminology (opt-in rate, CAC, incrementality) consistent with dailies. |
| Jeremy Howard | 8 | Build-on wikilinks (b1w02/b4w10/b6w15-17) carry the load. |

**Weighted average: 7.9**

---

## 01-mon — Lead magnets that actually convert in 2026

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "A lead magnet is a barter and the buyer is skeptical" is a first-principles reframe, not a slogan. |
| Chip Huyen | 8 | "Judge each magnet by the lead it earns, not the rate it posts" is the right objective. |
| Jerry Liu | 8 | The magnet spectrum is a spec (cost vs pull), not a listicle. |
| Hamel Husain | 9 | His "what's your eval on 20 real inputs" lens makes the magnet a product surface with a pass bar. |
| Simon Willison | 8 | Every benchmark carries a search-verified stamp and a hedge. |
| Seibel | 9 | His "ship the Google Doc first, don't build a magnet factory" pushback IS the reviewer lens. |
| Boris Cherny | 8 | "A broken tool is worse than no tool" is the concrete tooling caution. |
| Cohort peer | 8 | AI-native magnet framed as the cohort's unfair advantage, concretely. |
| Mira Murati | 7 | Light on frontier framing; defensible for the topic. |
| swyx | 8 | Gate-by-intent synthesis is the current 2026 read. |
| Ethan Mollick | 9 | His "the tool is not the moat; the insight and the list are" is the sharpest lens. |
| Lilian Weng | 8 | Format taxonomy consistent with Sunday's cards. |
| Jeremy Howard | 8 | b1w02/b4w10/b6w15 recapped one line, wikilinked, not re-taught. |

**Weighted average: 8.1**

---

## 02-tue — The opt-in funnel & list hygiene

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Providers outsource spam-fighting to your incentives" is the real model behind the rules. |
| Chip Huyen | 9 | Her "instrument the ratios as a weekly dashboard, not a spot-check" is the sharpest lens. |
| Jerry Liu | 8 | Four-stage funnel each with its own metric is a structured artifact. |
| Hamel Husain | 8 | Complaint-rate ceiling turned into a concrete list-hygiene bar. |
| Simon Willison | 8 | Uses provider bulk-sender guidance as primary; stamps on the fast-moving rules. |
| Seibel | 8 | His "50 subscribers with a Google Form first" pushback is bounded honestly. |
| Boris Cherny | 9 | His "plumbing before paint — DNS records are the gate, not email copy" is the reviewer lens. |
| Cohort peer | 8 | Double-vs-single opt-in tradeoff tied to the paid-traffic channel decision. |
| Mira Murati | 7 | Compliance-heavy; light on frontier, defensible. |
| swyx | 8 | Deliverability-as-reputation framing current. |
| Ethan Mollick | 8 | Sunset-the-unengaged framed as real behavior, not sentiment. |
| Lilian Weng | 8 | Consent taxonomy (GDPR/CAN-SPAM) consistent with the code-lab. |
| Jeremy Howard | 8 | b4w10/b6w15/b6w17 wikilinked, page mechanics explicitly not re-taught. |

**Weighted average: 8.1**

---

## 03-wed — The organic distribution engine

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Convert volatile borrowed attention into stable owned attention" is the real loop mechanic. |
| Chip Huyen | 8 | "Track the content-to-opt-in path, not likes" is a measurable discipline. |
| Jerry Liu | 8 | "The unit of reuse is the idea, not the asset" is the durable abstraction. |
| Hamel Husain | 8 | Repurposing chain is a concrete artifact with a per-format brief. |
| Simon Willison | 8 | Format stats explicitly flagged as a fast-decaying snapshot. |
| Seibel | 8 | "Anchor on one platform" is his concentrate-don't-spread instinct. |
| Boris Cherny | 7 | Link-in-comment discipline present; light on tooling otherwise. |
| Cohort peer | 8 | Two-week worked plan is directly copyable. |
| Mira Murati | 7 | Platform-mechanics-heavy; light on frontier. |
| swyx | 9 | His "build a searchable, ownable anchor (blog/YouTube), not rented feeds" is the sharpest lens and a real tension with the text. |
| Ethan Mollick | 8 | His "documenting has a selection problem — say nothing on empty days" adds honest nuance. |
| Lilian Weng | 8 | 6.6%/60%-penalty figures consistent with Sunday and the planner. |
| Jeremy Howard | 8 | His "be useful, algorithm rewards it" allergy to hacking is named and bounded. |

**Weighted average: 8.0**

---

## 04-thu — Paid ads: the honest primer

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Paid amplifies, it does not create" is the correct mechanism-level thesis. |
| Chip Huyen | 9 | Her "an ad system you can't measure is unobservable" makes measurement a precondition, not an afterthought. |
| Jerry Liu | 8 | Three-precondition gate is a spec, not a vibe. |
| Hamel Husain | 8 | "Size the test to significance or don't run it" is a bettable bar. |
| Simon Willison | 8 | Advantage+ figures stamped and hedged as platform-friendly aggregates. |
| Seibel | 8 | His "don't run ads until something works without them" is the reviewer lens. |
| Boris Cherny | 7 | Tooling risk deferred to Friday's CAPI where it belongs. |
| Cohort peer | 8 | Channel-choice heuristic (Google/Meta/LinkedIn/Reddit) is directly usable. |
| Mira Murati | 8 | The "manual targeting is being retired" automation-frontier read is apt here. |
| swyx | 9 | His "Advantage+-does-everything is partly Meta's own marketing; keep your own scoreboard" is the sharpest lens. |
| Ethan Mollick | 8 | Organic-vs-paid reframed as a risk/cash question, not dogma. |
| Lilian Weng | 8 | CPL/CAC/budget figures consistent with Friday and Sunday. |
| Jeremy Howard | 8 | b6w16 unit-economics gate wikilinked, not re-derived. |

**Weighted average: 8.1**

---

## 05-fri — Ad campaign mechanics & measurement

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Attribution is broken; arithmetic is not — reason from your own totals" is the real through-line. |
| Chip Huyen | 9 | Her "partially-observable system → build your own instrumentation" framing is the sharpest lens. |
| Jerry Liu | 8 | Metric ladder (CTR→CPL→CAC→ROAS→payback) ranked by closeness to money. |
| Hamel Husain | 9 | Small-N/Wilson discipline made executable: "kill on a rule, not a feeling." |
| Simon Willison | 8 | Attribution-loss numbers corroborated across domains, modeled-conversion caveat explicit. |
| Seibel | 8 | Pre-registration framed as the whole game, no bureaucracy. |
| Boris Cherny | 9 | His "CAPI is where founders ship duplicate/mis-mapped events — verify end to end" is the sharpest lens. |
| Cohort peer | 8 | The $5-CPL-looks-great-but-real-CAC-$117 worked read is the copyable payoff. |
| Mira Murati | 7 | Frontier-light; the AI-creative study carries the currency. |
| swyx | 8 | Blended-CAC-over-platform-ROAS is the correct skeptic's default. |
| Ethan Mollick | 8 | His "authenticity penalty is a moving 2026 snapshot" caveat is honest. |
| Lilian Weng | 8 | Attribution/ROAS/CAPI figures consistent with Sunday's cards. |
| Jeremy Howard | 8 | b2w03 Wilson + b4w10 instrumentation wikilinked, not re-taught. |

**Weighted average: 8.2**

---

## 06-sat — BUILD: the lead-gen engine + a disciplined paid test

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four gated components with paid hard-blocked on a converting funnel is the right build order. |
| Chip Huyen | 8 | "Instrument the engine as a system whose ratios you watch over time" ties to the calculator. |
| Jerry Liu | 8 | Each component has an explicit pass gate, not a to-do list. |
| Hamel Husain | 8 | "Eval the magnet on 20 inputs; count embarrassing outputs" is the pass bar. |
| Simon Willison | 8 | Calculator output shown verbatim; claims map to the code. |
| Seibel | 9 | His "ship the crude version of all four tonight, ugly-and-live beats polished-and-hypothetical" is the lens. |
| Boris Cherny | 9 | His "DMARC and CAPI are where founders quietly ship bugs — test both end to end" is the sharpest lens. |
| Cohort peer | 8 | "Honesty is the pass condition" (say-so-with-numbers if the funnel doesn't convert) is the discipline most builds skip. |
| Mira Murati | 7 | No model-choice stage; inherited, defensible. |
| swyx | 8 | The "weakest handoff is trials→customers, don't pour paid into the wrong leak" read is correct. |
| Ethan Mollick | 8 | The one-thing-live-tonight prompt is real behavior design. |
| Lilian Weng | 8 | PaidTestRule fields consistent with Fri and the code. |
| Jeremy Howard | 8 | Tiny deterministic tools; compile-checked; b6w16 wikilinked. |

**Weighted average: 8.1**

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Compresses to "optimize the ratio, not the total; paid amplifies; reason from your own totals" — the real spine. |
| Chip Huyen | 8 | Q11/Q13 force the CPL-vs-CAC and blended-CAC semantics, not recall. |
| Jerry Liu | 8 | "Five ideas that generalize" keep positions defensible. |
| Hamel Husain | 8 | Q14 forces the small-N guard's exact behavior (fixed this session). |
| Simon Willison | 8 | Answer key precise; figures trace to the stamped dailies. |
| Seibel | 8 | "What surprised me" post-mortem converts the week into a next action. |
| Boris Cherny | 8 | Q14 traces to the verified code-lab guardrail. |
| Cohort peer | 9 | 15-question quiz + 30 cards calibrated; cold-quiz instruction correct. |
| Mira Murati | 7 | Forward pointer commercial; no frontier note. |
| swyx | 8 | Blended-CAC card current. |
| Ethan Mollick | 8 | Scoring bands direct rereads to weakest days — real behavior design. |
| Lilian Weng | 8 | All 30 cards checked against weekday lessons; no contradictions. |
| Jeremy Howard | 8 | No duplicate territory with earlier quizzes; Week 19 link upgraded. |

**Weighted average: 8.0**

---

## code-lab/1 (README, requirements, funnel_metrics.py, distribution_planner.py, test_funnel_metrics.py)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Zero-dependency stdlib Python; every guard readable; the calculator IS the "measure ratios not totals" thesis. |
| Chip Huyen | 9 | Funnel roll-up surfaces the weakest handoff — the real observability payoff. |
| Jerry Liu | 8 | Functions map 1:1 to the Fri/Sat lesson claims; docstrings honest. |
| Hamel Husain | 9 | `py_compile` clean; 14 tests pin every guard incl. both small-N branches. |
| Simon Willison | 9 | Decision rule refuses to decide on noise; demo output reproduces the lesson numbers exactly. |
| Seibel | 8 | Tools deliberately tiny — wire estimates today, replace with real data next week. |
| Boris Cherny | 9 | Input validation (negatives, over-count, ordering, zero-denominator→inf) is comprehensive. |
| Cohort peer | 8 | README runnable top-to-bottom; the small-N guard teaches by refusing a fluke. |
| Mira Murati | 7 | No LLM backend; correctly left out of scope. |
| swyx | 8 | Stdlib-only, offline, deterministic; correct floor. |
| Ethan Mollick | 8 | PaidTestRule as a pre-registered object is behavior design in code. |
| Lilian Weng | 8 | Decision taxonomy (SCALE/KILL/KEEP_TESTING/INSUFFICIENT_DATA) consistent with the lessons. |
| Jeremy Howard | 9 | Small, deterministic, no network; compiles and passes clean. |

**Weighted average: 8.4**

---

## Overall Week 18: **8.1 / 10**

(File averages: 7.9, 8.1, 8.1, 8.0, 8.1, 8.2, 8.1, 8.0, code-lab 8.4.) Strongest: the code-lab and Friday — a lab that compiles clean, passes 14 tests, and reproduces the paid-test decision rule and small-N guard the week preaches, plus reviewer lenses that genuinely argue against the text (Boris on CAPI double-counting and DMARC bugs, Chip on unobservable ad systems, swyx on Advantage+ being Meta's own marketing, Seibel on shipping the crude version, Ethan on the tool-is-not-the-moat). Anti-slop: em-dash 1.8–5.4/1k (well under ~12); contrast-tics ≤2/file; house tics inside budget. Canonical homes (b1w02, b4w10, b6w15/16/17, b2w03) all wikilinked with one-line recaps — no re-teaching found. Both non-core names verified; Chris Walker's stale "CEO" title corrected to "founder."

---

## Surgical fixes applied this session (Phase 3, done)

1. **Date normalization (all 8 lessons):** 48 `2026-07-19` stamps (`last_verified`, `_last_verified`, and `search-verified` tags) → **`2026-07-17`** for vault consistency.
2. **01-mon (body + citation [^5]):** "CEO of Refine Labs" → "founder of Refine Labs" — Chris Walker exited as CEO in July 2025; "founder" is accurate as of 2026-07.
3. **07-sun Q14 answer:** corrected the arithmetic gloss "$262 (below the kill line)" — $1,050 ÷ 4 = $262.5 is **above** the $200 kill line; rewritten to "which would otherwise breach the kill line … you cannot even call it a loser yet," which is both correct and a sharper teaching point for the small-N guard.
4. **07-sun forward link:** `[[…week-19…/00-overview|Week 19]] (pending)` → `(pending)` removed; Week 19 exists on disk.

No git commits made.

## Unresolved concerns (recommendations, not applied)

1. **Fast-moving facts carry `search-verified 2026-07-17; fetch egress-blocked — liveness pass pending` stamps** per the amended protocol. A Phase-4 liveness pass should re-hit the live URLs for the load-bearing 2026 figures: Gmail/Yahoo bulk-sender rules (Chronos/Red Sift/PowerDMARC), lead-magnet benchmarks (Digital Applied/Prospeo/Amra&Elma), LinkedIn algorithm stats (Dataslayer/Hootsuite), Meta Advantage+ adoption/ROAS (Optimyzee/Pixis/Digital Applied), CPL benchmarks (Stackmatix/meet-lea/Benly), attribution loss + CAPI (DOJO AI/adlibrary), and the GenAI-ads study (Taboola/DMNews).
2. **Several 2026 practitioner sources are secondary/SEO-tier** (Digital Applied, Prospeo, Stackmatix, get-ryze, meet-lea, Benly, Optimyzee, DOJO AI, adlibrary, Leadgen Economy). Each load-bearing figure is corroborated across two domains and hedged directionally ("roughly," "on the order of," "typically"), and the strongest claims lean on primaries where possible (provider bulk-sender guidance; the Taboola/Columbia/Harvard/TUM/CMU study). Phase-4 could hunt stronger primaries for the LinkedIn 6.6%-ER figure and the Meta 22%-ROAS-lift aggregate, or keep the directional framing.
3. **The Taboola GenAI-ads study attribution** ("Columbia, Harvard, TU Munich, Carnegie Mellon") is corroborated only via Taboola's own press release and secondary coverage (DMNews) in this egress-blocked session. A Phase-4 pass should confirm the academic authorship and the ~0.76% vs ~0.65% CTR figures against a primary before treating them as more than directional.
4. **Lesson word counts run ~2,600–3,600 words** (below the base spec's 4,500–6,500 L3 target, though within `quality-standard.md`'s 2,000–4,000 core-lesson band). Density is high and prose is tight, so this reads as deliberate compression rather than laziness; flagged for awareness, not fixed — padding a tight lesson in review would degrade it.

---

_Review + surgical polish produced 2026-07-17. Files edited: all 8 lesson `.md` (date stamps), 01-mon (Chris Walker title), 07-sun (Q14 gloss + Week 19 link). No git commits made._
