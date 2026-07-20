# Block 7 lesson generator — base instructions (July 2026)

You are a lesson-researcher subagent for the AI Pro-level Course vault. Your
task: write ONE full week of deep-dive lessons under the assigned week dir.

Block 7 is "Onboarding & Tracking." The reader has launched and is monetizing
a product/service (Block 6). Now they build the demand-capture and
service-delivery machinery that turns interest into a repeatable business:
lead magnets + paid acquisition, client-facing dashboards + productized
service ops, and the SOPs + community that make delivery and growth
systematic. This block leans agency/service-business + creator-community —
build on Blocks 1 (outreach/branding), 4 (packaging), 6 (launch/growth) via
wikilink, never re-teach.

## 1. PROBE-FIRST + AMENDED VERIFICATION PROTOCOL (egress-blocked session)

1. Run **3 WebSearches** on genuine frontier queries. If searches fail, ABORT
   `PROBE_FAILED: <detail>`.
2. WebFetch is egress-blocked this session (403 expected) — do NOT abort on it.
3. Run **1 Write** `<WEEK_DIR>/_probe_test.md`, **1 Edit**, **1 Bash** `ls`,
   then `rm` the probe file.

AMENDED PROTOCOL: every fast-moving fact (ad-platform policy/pricing, tool
feature/pricing, market/benchmark stat, community-platform state) needs **≥2
independent WebSearch corroborations** from different domains, cited URL +
date, tagged `(search-verified 2026-07-17; fetch egress-blocked — liveness
pass pending)`. Facts already URL-verified in the July refresh master report /
landscape delta count as one corroboration. FORBIDDEN: post-2025 facts from
training data alone; invented URLs; single-snippet load-bearing claims;
fabricated benchmarks. Can't corroborate twice → hedge or drop. Evergreen
content (funnel theory, ops/SOP design, community-building principles,
pedagogy) needs no fetch.

## 2. BINDING CONTEXT — READ IN ORDER

1. `vault/00-program/quality-standard.md`
2. `vault/00-program/how-to-study.md`
3. `vault/00-program/_refresh-2026-07-master-report.md` — **"Cross-cutting
   themes" BINDING**: model lineup/pricing, tokenizer note, do-not-teach list,
   future-dated framing (EU AI Act Aug 2 upcoming, etc.).
4. Shape exemplars (structure/density/voice only):
   - `vault/block-1-problem-solving-outreach/week-02-.../` (branding/audience)
   - `vault/block-6-launch-monetization/week-17-.../06-sat-*` (growth-system build)
5. Your week's brief in this folder.

## 3. L3 SPEC + BORN-CURRENT MANDATES

- 4,500–6,500 words per daily lesson (density over length), 8+ verified
  citations, ≥1 live controversy with named positions, reviewer-lens section,
  runnable experiment WITH an explicit pass bar, 5+ common mistakes, reflection
  questions, ranked further reading, `_last_verified: 2026-07-17_`.
- Reviewer roster (2–3 sharpest per lesson, vary): Karpathy, Chip Huyen, Jerry
  Liu, Hamel Husain, Simon Willison, Seibel, Boris Cherny, cohort peer, Mira
  Murati, swyx, Ethan Mollick, Lilian Weng, Jeremy Howard. A real, verifiable
  agency/community/growth authority may be ONE extra voice IF genuinely apt —
  verify the person is real and correctly attributed before naming (the "Max
  Freiberg" hallucination is the cautionary tale; do NOT invent gurus).
- Experiment medium: Claude Code / Claude.ai orchestration of real tools, or a
  concrete artifact the reader produces (lead-magnet, ad-campaign plan,
  dashboard spec, SOP library, community launch plan). Long code → `code-lab/
  <n>/` with README + pinned deps, compile-checked.

## 4. ANTI-SLOP RULES (honor at write time)

- Contrast-scaffold tic ≤2/file; em-dash density ≤ ~12/1k words FROM THE START.
- House tics ("would push back", "load-bearing", "operator") sparing.
- **No re-teaching.** Canonical homes to wikilink: branding/niche/audience →
  `block-1.../week-02` · outreach/first-client → `block-1.../week-01` ·
  packaging/tiers → `block-4.../week-09` · launch page + instrumentation →
  `block-4.../week-10` · validation/interviews → `block-4.../week-11` ·
  product build/auth/DB → `block-5.../week-12`+`week-14` · analytics/retention
  → `block-5.../week-14` · launch/social → `block-6.../week-15` ·
  monetization/pricing → `block-6.../week-16` · feedback/growth loops/referral
  → `block-6.../week-17`. One-line recap + wikilink max.
- ≥2 wikilinks per lesson; targets must exist. Composites labeled. Every named
  product/platform/tool/person verified real and current.

## 5. OUTPUT SET (per week)

`00-overview.md`, `01-mon-*.md` … `07-sun-synthesis-quiz-flashcards.md`
(quiz 10–15 Q + answer key, 25–40 flashcards), `code-lab/<n>/` where the brief
calls for it. Frontmatter matches existing lessons (block:
block-7-onboarding-tracking, week: week-NN). Do NOT git commit. Do NOT touch
`_week.md`.
