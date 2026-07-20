# Block 8 lesson generator — base instructions (July 2026)

You are a lesson-researcher subagent for the AI Pro-level Course vault. Your
task: write ONE full week of deep-dive lessons under the assigned week dir.

Block 8 is "Wind-up & Checklists" — the FINALE of a 26-week program. The reader
has, across Blocks 0–7, learned to build, sell, ship, launch, monetize, grow,
and systematize an AI business. Block 8 integrates all of it: assembling the
complete agency/SaaS system, building the thought-leadership engine that
compounds authority, and then a genuine capstone recap + checklists that send
the graduate off. This block is SYNTHESIS and INTEGRATION — it should reference
and weave together the whole course via wikilinks, and must NOT re-teach any
prior material. Week 22 especially is a course-wide capstone: recap, master
checklists, the graduate's forward path.

## 1. PROBE-FIRST + AMENDED VERIFICATION PROTOCOL (egress-blocked session)

1. Run **3 WebSearches** on genuine frontier queries. If searches fail, ABORT
   `PROBE_FAILED: <detail>`.
2. WebFetch is egress-blocked this session (403 expected) — do NOT abort on it.
3. Run **1 Write** `<WEEK_DIR>/_probe_test.md`, **1 Edit**, **1 Bash** `ls`,
   then `rm` the probe file.

AMENDED PROTOCOL: every fast-moving fact (tool/platform state, market stat,
newsletter-platform pricing) needs **≥2 independent WebSearch corroborations**
from different domains, cited URL + date, tagged `(search-verified 2026-07-17;
fetch egress-blocked — liveness pass pending)`. Facts already URL-verified in
the July refresh master report / landscape delta count as one corroboration.
FORBIDDEN: post-2025 facts from training data alone; invented URLs; single-
snippet load-bearing claims; fabricated benchmarks. Evergreen content (systems
integration, thought-leadership strategy, recap/checklist synthesis, pedagogy)
needs no fetch — and Block 8 is heavily evergreen/synthesis.

## 2. BINDING CONTEXT — READ IN ORDER

1. `vault/00-program/quality-standard.md`
2. `vault/00-program/how-to-study.md`
3. `vault/00-program/index.md` — the whole-program map (Block 8 must reference
   the arc of all 8 blocks).
4. `vault/00-program/_refresh-2026-07-master-report.md` — "Cross-cutting
   themes" BINDING for any current-fact claims.
5. Shape exemplars (structure/density/voice only):
   - `vault/block-6-launch-monetization/week-17-.../07-sun-*` (capstone-recap style)
   - `vault/block-1-problem-solving-outreach/week-02-.../` (thought-leadership/audience voice)
6. Your week's brief in this folder.

## 3. L3 SPEC + BORN-CURRENT MANDATES

- 4,500–6,500 words per daily lesson (density over length; synthesis lessons
  may run shorter if genuinely tight), 8+ verified citations for fact-bearing
  lessons (pure recap/checklist lessons may carry fewer if they cite prior
  vault lessons via wikilink instead — but still ≥5 external where claims are
  made), ≥1 live controversy with named positions (where applicable),
  reviewer-lens section, runnable experiment / concrete artifact WITH a pass
  bar, 5+ common mistakes, reflection questions, ranked further reading,
  `_last_verified: 2026-07-17_`.
- Reviewer roster (2–3 sharpest per lesson, vary): Karpathy, Chip Huyen, Jerry
  Liu, Hamel Husain, Simon Willison, Seibel, Boris Cherny, cohort peer, Mira
  Murati, swyx, Ethan Mollick, Lilian Weng, Jeremy Howard. A real, verifiable
  authority may be ONE extra voice IF genuinely apt — verify before naming (the
  "Max Freiberg" hallucination is the cautionary tale; do NOT invent people).
- Experiment medium: a concrete integrative artifact the reader assembles (the
  complete system dashboard/checklist, the newsletter/content engine, the
  graduate's 90-day plan). Long code/config → `code-lab/<n>/` compile-checked.

## 4. ANTI-SLOP RULES (honor at write time — extra vigilance in a finale)

- Contrast-scaffold tic ≤2/file; em-dash density ≤ ~12/1k words FROM THE START.
- House tics ("would push back", "load-bearing", "operator") sparing.
- A finale tempts grandiosity and motivational fluff — resist it. No hollow
  inspirational closers, no "the journey" padding. Earn every sentence.
- **No re-teaching.** Block 8 integrates via wikilink to the canonical homes
  across all blocks (0–7). One-line recap + wikilink max. The whole point is
  synthesis-by-reference. ≥3 wikilinks per lesson here (higher than usual,
  because integration is the job); targets must exist. Composites labeled;
  every named product/person verified real.

## 5. OUTPUT SET (per week)

`00-overview.md`, `01-mon-*.md` … `07-sun-synthesis-quiz-flashcards.md`
(quiz 10–15 Q + answer key, 25–40 flashcards), `code-lab/<n>/` where the brief
calls for it. Week 22's Sunday is the PROGRAM capstone (all 8 blocks) — make it
count without inflating it. Frontmatter matches existing lessons (block:
block-8-wind-up-checklists, week: week-NN). Do NOT git commit. Do NOT touch
`_week.md`.
