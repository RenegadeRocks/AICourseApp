---
type: review
block: block-2-ai-employees
week: week-05
phase: 2-multi-persona-review
reviewed: 2026-04-17
reviewers_rotated:
  - chip-huyen
  - jerry-liu
  - jason-liu
  - simon-willison
  - hamel-husain
  - boris-cherny
  - harrison-chase
  - lilian-weng
  - douwe-kiela
  - brandon-smock
  - andrej-karpathy
criteria:
  - l3-technical-depth
  - citation-quality
  - reviewer-lens-sharpness
  - operator-war-stories
  - controversy-engagement
  - cross-domain-applicability
  - runnable-experiment-quality
  - problem-set-rigor
  - block-2-thesis-fit
  - overall-l3-quality
---

# Week 5 — Phase 2 Multi-Persona Review

## Summary Table

Scale 1–10 per criterion.

| Lesson | L3 depth | Citations | Reviewer sharpness | War stories | Controversy | Cross-domain | Experiment | Problem set | Block-2 fit | Overall | **Avg** |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-mon — analyst replacement thesis | 9 | 9 | 9 | 9 | 9 | 8 | 8 | 9 | 10 | 9 | **8.9** |
| 02-tue — document understanding stack | 9 | 9 | 9 | 8 | 8 | 9 | 9 | 9 | 9 | 9 | **8.8** |
| 03-wed — data connectivity / MCP / governance | 9 | 9 | 9 | 8 | 8 | 9 | 9 | 9 | 9 | 9 | **8.8** |
| 04-thu — analytical reasoning + code offload | 10 | 9 | 10 | 8 | 9 | 8 | 9 | 9 | 9 | 9 | **9.0** |
| 05-fri — report generation patterns | 9 | 9 | 9 | 8 | 8 | 9 | 9 | 9 | 9 | 9 | **8.8** |
| 06-sat — build the generator | 9 | 9 | 9 | 8 | 8 | 9 | 9 | 9 | 10 | 9 | **8.9** |
| 07-sun — synthesis + quiz + flashcards + capstone | 9 | 9 | 8 | 7 | 8 | 9 | 9 | 9 | 10 | 9 | **8.7** |

**Week average: 8.84 / 10** (target ≥8.0 — comfortably met)

Flagged lessons (avg < 8.5): **0**. All seven lessons clear the bar.

---

## Per-Lesson Sections

### 01-mon — analyst-replacement thesis

**Strongest:** The four-category taxonomy (financial-close / CPM / competitive intel / operational reporting) with disclosed-number anchors per category is an exceptionally clean commercial-entry frame. Brex 70%/3x, Ramp $163M/208K-hrs, Vic.ai 97%, Puzzle Level-3 Governed Automation all carry URL + date + exact quote. Reviewer lens (McCardel, Husain, Moallemi, Orloff, Willison) is the sharpest on the week — each disagreement is specific, load-bearing, and tied to a named quote.

**Weakest:** Runnable experiment is mostly thinking work (deconstruct → vendor benchmark → position) with no code. Defensible for a Monday framing lesson, but "runnable" is slightly aspirational. Also the Hex $19.8M ARR / 162-person datapoint leans on Latka, a secondary source.

**Line-level fix targets:**
- Layer 3 Case 1 ("accounting teams to close their books three times faster") — already quoted cleanly; consider adding a cohort caveat ("Brex customer base, no disclosed N").
- Problem Set #2 asks 500 words on category death — tighten to 400; 500 invites padding.

**Rollup: 8.9**

---

### 02-tue — document understanding stack

**Strongest:** The five-archetype frame (Specialised OSS / Hosted gen-AI / Native multimodal / Cloud doc-AI / Academic) with win-and-lose conditions per archetype is teachable and durable. SCORE-Bench ranking-inversion finding is load-bearing and correctly attributed. Choice-level operator advice (cache-by-SHA-256, page routing, schema-first vs markdown-first, when-to-require-citations, eval-first, fallback path) is the kind of real engineering wisdom L3 is supposed to carry.

**Weakest:** Only one named operator anecdote with specific before/after numbers (FinanceBench → Patronus follow-up). The LlamaParse Uber 10-K war story and SCORE-Bench observation are more "citation than anecdote." The 5000–50000 pages crossover estimate is asserted without a source.

**Line-level fix targets:**
- Layer 3 Choice 1 — the "10x cost reduction from caching" claim should be caveated or cited.
- Archetype 2 Procycons numbers (ChrF++ 81 vs edit-similarity 88) are apples-to-oranges metrics — note this explicitly.

**Rollup: 8.8**

---

### 03-wed — data connectivity / MCP / governance

**Strongest:** The source-class × team-size decision matrix is the best single artifact in the week for operator use. Willison lethal-trifecta + rug-pull framing is correctly attributed and specifically dated (April 9, 2025). Governance ladder (view → RLS → Presidio → audit log) is ordered by leverage, not alphabetised. Regulatory surfaces (SOC 2 / GDPR / HIPAA / PCI) each cite the actual current standard version + date.

**Weakest:** The "over-scoped service-account that survived three audits" war story is generic rather than named. Vanta's role is referenced but not with a specific case study URL. The Ramp AI-token-spend case is used twice (Monday, here), minor double-counting.

**Line-level fix targets:**
- Layer 3 — "Vanta's public trust center and case studies have multiple variants" — cite one specific Vanta case URL or drop.
- The decision table explicitly says "Unstructured loader (schema drift)" under spreadsheets — Unstructured isn't really a spreadsheet loader; this is an odd juxtaposition.

**Rollup: 8.8**

---

### 04-thu — analytical reasoning + code-execution offload

**Strongest:** This is the best lesson of the week on pure L3 technical depth. Failure taxonomy (aggregation off-by-one / unit confusion / sign errors / hallucinated columns / rounding chains) is operationally actionable. PAL + FinanceBench + FinQA + Huang 2024 + S²R (ACL 2025) citation set is exactly right. The `units` enum in the tool schema is a load-bearing architectural insight that most tutorials miss. Reviewer lens is the sharpest: Karpathy (self-correction critique), Husain (eval rigor), Jerry Liu (specialised pipelines for finance), Jason Liu (typed DSL vs free-text code), Kiela (retrieval-grounding counter). Five distinct critics, five genuinely orthogonal disagreements.

**Weakest:** Some self-reported pilot numbers ("68% → 86% → 94%") are marked "on my own pilots" without a public dataset — fine for a practitioner voice, but an evaluator with a rigorous lens would ask for the corpus spec. Karpathy is invoked as a reviewer but his actual X posts aren't cited; it's plausible paraphrase, not a quote.

**Line-level fix targets:**
- Layer 4 — add a Karpathy X URL or reframe as "Karpathy-style skepticism" to avoid putting words in his mouth.
- "~68% → 86% → 94%" numbers need either "N=30, corpus=X" or an "indicative, not benchmarked" caveat.

**Rollup: 9.0** (highest of the week)

---

### 05-fri — report-generation patterns

**Strongest:** The three-pattern taxonomy (slot-fill / narrative-synthesis / chart-generating) with the composition-pattern most-shipped-systems-use observation is clean and teachable. The insight-vs-description gap is a genuinely original framing (description defaults, RLHF neutrality, voice homogenisation, same-voice-as-competitors). The rubric-as-editor's-brief example with the adversarial senior-editor critic prompt is concrete and copyable. Vega-Lite grounding with VegaChat + VL2NL + 2025 arxiv survey gives builders a reliability floor.

**Weakest:** The Packy McCormick position is referenced multiple times but without a specific URL — "Packy's refusal" is paraphrased. The "60% generic-phrase reduction" claim from the adversarial critic is self-reported without a dataset spec. The schema example, while good, could flag that OpenAI strict mode requires every property in `required` — it does, but this isn't explicit.

**Line-level fix targets:**
- Cite a specific Packy McCormick tweet/podcast where he states the refusal, or mark as paraphrase.
- Layer 2 "+60%" claim — add N or mark as illustrative.
- Q6 of problem set explicitly asks students to reproduce a Vega-Lite failure — excellent, keep.

**Rollup: 8.8**

---

### 06-sat — build the generator

**Strongest:** Framework decision (Claude Code vs LangGraph vs Pydantic AI vs CrewAI) is the clearest contemporary L3 decision guidance in the week, and the 50-reports-per-week migration trigger is specific enough to be defensible. The eight-stage pipeline with per-stage contracts and explicit fail-loud-vs-fallback calibration is the spine that ties the entire week together. Boris Cherny's five-parallel-sessions pattern as a named reviewer disagreement is exactly the right move — it's the insider counter to the LangGraph recommendation.

**Weakest:** Case 1 (Clippd, Dagster) and Case 3 (Fédération Wallonie-Bruxelles) are legitimate but thin on specifically AI-analyst-worker detail — they are orchestrator-migration stories, not analyst-worker stories. Case 2 (Brex/Ramp) is the third time these disclosed numbers have appeared in the week; saturation risk. Phase 5's "read the generated report as if you were the CEO" is solid but the 500-word writeup spec is soft.

**Line-level fix targets:**
- Case 1 Clippd — explicitly call out this is an orchestration case study, not a report-generator case study, to avoid the reader confusing the two.
- Add one specific AI-analyst-worker postmortem (even a public community post) to Case 2 to replace or supplement the third-time Brex/Ramp frame.

**Rollup: 8.9**

---

### 07-sun — synthesis + quiz + flashcards + capstone

**Strongest:** Six-stage pipeline frame (category → parse → connect → verify → generate → ship) with failure-per-stage is an excellent compression of the week. The 15-move mental-move table is a ship-ready operator asset. 20-quiz + 40-flashcard + 30-day capstone with week-by-week commitment is the most complete synthesis asset in any week shipped so far. The "reviewer lens — where you'd still lose points" section (Morgan Lewis EU/DORA, Hamel eval decay, Harrison Chase adapter layer, Packy voice-is-for-Packy, Chip Huyen eval freeze-decay) is a genuine surprise-and-delight addition.

**Weakest:** Length (~7050 words vs 3800 target) is justified by capstone + quiz + flashcards but some flashcards are overlapping (cards 29 and 8 cover similar territory). A couple of quiz answers (Q9, Q12) are worked examples that blur into "applied capstone" rather than "quiz." No fundamentally weak section, just redundancy at edges.

**Line-level fix targets:**
- Flashcard 29 ≈ flashcard 8 (eval stack gains vs evaluator-critic conditions) — dedupe or tighten.
- Q15 cost numbers ("$8–$15/run") — add "Opus 4.7 at 2026-04 pricing" timestamp.
- Capstone Week 4 "gate-lift criteria" — voice fidelity "≥ 4/5" threshold should cite the rubric not just a number.

**Rollup: 8.7**

---

## Week-Level Notes

### Arc coherence

Week 5's arc is the strongest of Block 2 Phase 1 so far. The six-stage pipeline (Mon taxonomy → Tue parse → Wed connect → Thu verify → Fri generate → Sat ship → Sun synth/capstone) is genuinely load-bearing across every lesson, and the Saturday build explicitly references every earlier lesson's output as a stage contract. The commercial framing (category 4 is the clean lane) from Monday is paid off in Saturday's cost-model and 30-day rollout. The FinanceBench / PAL / Huang / Willison / MCP citation set recurs across lessons without feeling repetitive — each reuse adds a different angle (Mon: market framing; Tue: parse-vs-retrieval diagnosis; Wed: governance; Thu: numerical reasoning; Fri: generation; Sat: ship).

### Duplication

Minor saturation on three citation clusters:
1. **Brex 70%/3x + Ramp $163M/208K** appears in Mon (primary), Wed (governance example), Sat (Case 2), Sun (recall). Four mentions is acceptable because each serves a different role (commercial / governance / operator case / recall), but watch for reader fatigue.
2. **Hex / McCardel "no AI data scientists"** appears in Mon, Fri, Sat, Sun. Again, four different roles — but the quote "AI without analysts produces confidently-wrong reports at rates that survive casual review but fail audit" is attributed to McCardel as a direct quote in the synthesis; verify the exact quote in the source blog.
3. **FinanceBench 81%** appears in Mon (framing), Tue (parsing root cause), Thu (numerical reasoning), Sat (cost justification), Sun (recall). Five mentions. Teaches the benchmark well — keep.

### Phase 3 priorities

**P0 (must do before ship):**
1. Thu — verify Karpathy X source or reframe the reviewer voice as "Karpathy-style skepticism" (paraphrase, not quote). Same for any "~68%/86%/94%" self-reported numbers — add corpus spec or indicative caveat.
2. Fri — verify Packy McCormick "uncanny valley" refusal with a specific URL, or mark as paraphrase from reported interviews.
3. Sun — verify the direct quote attributed to McCardel ("confidently-wrong reports…") matches the Hex blog verbatim; rephrase if paraphrased.

**P1 (should do):**
4. Wed — add one specific Vanta case URL for the over-scoped-account postmortem, or replace with a named public postmortem.
5. Sat — swap one of the Clippd / FWB cases for a real AI-analyst-worker postmortem (community write-up is fine).
6. Tue — the 5K–50K pages crossover number should either get a source or be marked as practitioner estimate.

**P2 (nice to have):**
7. Sun — flashcard dedup (29 vs 8, plus 2 other light overlaps).
8. Mon — Problem Set #2 tightening from 500 to 400 words to match elsewhere.
9. Fri — "+60% generic-phrase reduction" — add N or mark indicative.

### Voice and house style

Consistent across the seven files: critical-operator voice, named reviewer with specific disagreement per lesson, disclosed-number anchoring, explicit what-this-doesn't-cover. No L2-generalist drift detected. "Further reading" tiers (Must/Recommended/Optional) are uniformly applied. Citation footnote format is consistent.

### Block 2 thesis fit

Week 5 is the *canonical* back-office analyst-worker week and the commercial payoff for Weeks 3 (landing pages) and 4 (sales agent). It references Weeks 3/4 cleanly without re-teaching, and it sets up Block 3 (voice agents) on each Further Reading appendix. Block 2 thesis fit averages 9.3 across lessons — the highest criterion average in the week.

---

## Week average: 8.84 / 10

Week 5 is ship-ready pending the P0 and P1 citation cleanups above. No lesson is flagged as sub-threshold; all seven clear 8.5, four clear 8.8, one (Thu) reaches 9.0.
