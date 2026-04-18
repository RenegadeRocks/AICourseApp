---
type: review
block: block-2-ai-employees
week: week-04
phase: 2-multi-persona-review
reviewers:
  - karpathy (agent architecture)
  - huyen (ML systems/eval)
  - jerry-liu (llamaindex/rag)
  - jason-liu (instructor/rag)
  - willison (prompt injection/LLM pragmatics)
  - chase (langchain/langgraph)
  - cherny (claude code)
  - weng (agent loops)
  - kiela (retrieval quality)
  - hylak (sales eng)
reviewed_on: 2026-04-17
---

# Week 4 Multi-Persona Review — Sales Agent + RAG

## Summary table (per-lesson criterion scores + avg)

Criteria: (1) L3 technical depth, (2) Citation quality, (3) Reviewer-lens sharpness, (4) Operator war stories, (5) Controversy engagement, (6) Cross-domain, (7) Runnable experiment, (8) Problem set rigor, (9) Block 2 thesis fit, (10) Overall L3.

| Lesson | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Avg |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 01-mon what-a-sales-agent-is | 8.5 | 9.0 | 9.0 | 9.5 | 9.0 | 8.5 | 8.0 | 8.5 | 9.0 | 8.8 | **8.78** |
| 02-tue agent-architectures | 9.0 | 9.0 | 8.5 | 8.5 | 8.5 | 7.5 | 8.5 | 8.5 | 9.0 | 8.7 | **8.57** |
| 03-wed deliverability-compliance | 9.0 | 9.5 | 8.5 | 8.5 | 8.5 | 9.5 | 8.5 | 8.5 | 9.0 | 9.0 | **8.85** |
| 04-thu rag-fundamentals | 9.0 | 9.5 | 9.0 | 8.5 | 9.0 | 8.5 | 8.5 | 8.5 | 8.5 | 8.9 | **8.79** |
| 05-fri advanced-rag | 9.0 | 9.5 | 9.0 | 8.0 | 9.0 | 8.0 | 8.5 | 8.5 | 9.0 | 8.9 | **8.74** |
| 06-sat rag-evaluation | 9.0 | 9.0 | 8.5 | 9.0 | 8.5 | 8.0 | 8.5 | 8.5 | 9.5 | 9.0 | **8.75** |
| 07-sun synthesis | 8.0 | 8.5 | 7.5 | 7.5 | 7.5 | 8.0 | 7.5 | 8.5 | 9.5 | 8.2 | **8.07** |

**Week average: 8.65** — above the 8.0 target. Zero lessons flagged below 8.0.

---

## Per-lesson notes

### 01-mon — What a sales agent actually is (8.78)

**Strongest.** The 11x teardown is the best operator case study anywhere in the vault: named quotes (ZoomInfo, Airtable, anonymous former employee on "massaged the numbers"), dollar-level specificity ($14M stated / $3M real ARR, 70–80% churn), legal framing ("deceptive trade practices, trademark infringement"), and the layer-by-layer disclosure-gap architecture reading. The eight-layer pipeline scaffold is structurally load-bearing for the entire week. Cross-domain section (legal/healthcare/financial/consulting) genuinely shifts the binding-constraint per vertical rather than repeating the SaaS frame.

**Weakest.** Reviewer-lens section is strong but could name **Aman Hylak** (sales-eng pragmatics) and **Jason Bay** with more specific numeric disagreements — Farrokh/Cegelski and Orlob are cited but their counter-numbers (specific reply-rate thresholds they call BS on) are not quoted. Footnote [^9] (Stebbings / Latka $25M ARR) flagged by the author as secondary — that's honest but the citation could be demoted or verified via a primary 20VC clip.

**Line-level fix targets.**
- L88 (Stebbings claim): add "confidence: low — secondary source" tag inline.
- L233 (Farrokh/Cegelski reviewer paragraph): add one specific disputed number (e.g., their position on the 52% Outreach pipeline-lift figure treated as "marketing artifact").
- Consider one additional war story: a *named* agency that ran Artisan at volume and reported specific numbers — currently Artisan teardown leans on vendor-disclosed figures.

**Rollup: 8.78** — highest-scoring week-opener in Block 2 so far. Ship.

### 02-tue — Agent architectures (8.57)

**Strongest.** The τ-bench pass^8<25% framing is the single best quantitative anchor in the lesson — paired with the "think" tool 0.370→0.570 improvement, it gives the reader a reliability budget, not just architecture names. Six-tool JSON schema is production-grade: the `description` field usage (irreversibility, budget hints, order-of-operations clauses) teaches a mechanism that Anthropic's own docs under-emphasize. Cognition/Devin "enthusiastic interns" quote + Sierra's $100M ARR workflow-first architecture as paired counter-examples is the sharpest treatment of the autonomous-vs-workflow debate in Block 2.

**Weakest.** Cross-domain is the weakest of any Week-4 lesson (7.5) — the lesson stays inside "sales agent" framing and doesn't generalize the patterns to other verticals (unlike Monday's legal/healthcare treatment). Reviewer-lens is good but Boris Cherny's pushback is generic ("use tool_search_tool") — could quote his specific Anthropic blog line on programmatic tool calling. Lilian Weng's memory critique is acknowledged but the lesson doesn't actually add a memory-layer discussion as a fix.

**Line-level fix targets.**
- L203 (Sierra paragraph): add one named Sierra customer's specific guardrail example — WeightWatchers or Discord's policy-gate pattern — for operator grounding.
- L229–234 (reviewer lens — Weng): either add a short "memory layer for sales agents" paragraph or explicitly punt to Thursday's RAG lesson with a forward-ref.
- Problem 5 (τ-bench reproduce): specify expected pass^3 delta so students have a yardstick for "did I reproduce the finding."

**Rollup: 8.57** — strong architecture lesson, could tighten the cross-domain and reviewer depth.

### 03-wed — Deliverability and compliance (8.85)

**Strongest.** The single most *operator-ready* lesson of the week. DNS zone snippets with `-all` vs `~all` tradeoff, the SPF 10-lookup PermError failure mode, the 5-jurisdiction compliance matrix (CAN-SPAM / CCPA / GDPR 6(1)(f) / DPDP 2025 / CASL) with penalty dollar amounts — this is what every Block 1 graduate who has never shipped outbound needs before touching a send button. The ePrivacy per-country trap (DE/FR/IT/NL opt-in vs UK opt-out) is rare to see correctly stated in a non-legal outlet. Cross-domain score (9.5) justified because the lesson IS cross-domain by construction.

**Weakest.** Reviewer-lens is solid but Neil Kumaran and Marcel Becker's pushbacks are reasonable steelman-guesses rather than quoted disagreements — the Becker Mailgun interview has quotable lines the lesson could pull more directly. Jason Bay's "wrong level of the problem" pushback is sharp but not paired with one of his specific LinkedIn/podcast examples.

**Line-level fix targets.**
- L138 (warmup table): Marcel Becker's point is that engagement-per-recipient matters more than volume-curve — consider adding a Becker-approved column ("engagement target per recipient type") rather than the current uniform "goal engagement" row.
- L184–264 (compliance matrix): worth one worked example — take the Monday Artisan Ava draft through all five regimes and flag the three clauses that would block per regime.
- L353 (Amin pushback): "bull case more aggressively" — the lesson could actually steelman the bull case in a box, not just acknowledge Amin would want it.

**Rollup: 8.85** — highest score of the week. Quasi-lesson-of-record for 2026 outbound deliverability. Ship.

### 04-thu — RAG fundamentals (8.79)

**Strongest.** The $1.02/M doc tokens cost math with prompt-caching as the decisive enabler is the load-bearing operational insight most Contextual Retrieval summaries skip — the lesson is explicit that the economics flip 5–10× without caching. MTEB 2026 table with web-verified $/1M token columns is the best commercial-embedder snapshot in the vault. Hybrid-RRF treatment (k=60, OpenSearch 2.19 numbers, +1.4% nDCG@10 over sparse, +18% over BM25 alone on BEIR) is specific and reproducible. Domain-specific chunking (legal 256/25, medical SOAP-aware, financial hierarchical) gives the reader three distinct playbooks, not one.

**Weakest.** War stories section names the three corpora (legal 500K docs, medical clinical decision support, financial 10-K QA) but the specific firms and their telemetry are anonymized or referenced to academic papers rather than disclosed operator reports — this is honest but less sharp than Monday's 11x teardown. Jerry Liu reviewer pushback is well-framed but his specific hierarchical-chunking counterexample corpus is not named.

**Line-level fix targets.**
- L206–214 (war stories): if any of the three can be tied to a named vendor or firm publicly (Harvey, Casetext, Ironclad for legal), prefer that over anonymous framing.
- L274 (Kiela reviewer): add one specific quote from his RAG 2.0 DataCamp podcast on the jointly-trained ceiling — currently paraphrased.
- Benchmark table (L194–201): the latency deltas are marked "indicative estimates" — add a footnote pointer to the Saturday eval lesson for how a reader would actually measure on their own stack.

**Rollup: 8.79** — strongest pure-RAG teaching in Block 2 so far. Ship.

### 05-fri — Advanced RAG (8.74)

**Strongest.** The cost-per-correct-answer unifier is the sharpest analytical move of the week — it resolves the GraphRAG / long-context / RAG trilemma into one metric a CFO can argue against. The Chroma Context Rot finding (all 18 models get worse, coherent docs hurt, 200K-window model fails at 50K) is correctly treated as a *trajectory-changing* piece of evidence, not a footnote. The three-layer grounding check (structural → span match → entailment) is production-ready and maps to real regulated-domain audit processes.

**Weakest.** Operator war stories section is the weakest of the RAG three (8.0) — Harvey is cited at "high level," the Endex 10%→0% claim is from Anthropic's own launch marketing (not independent), LinkedIn case is loosely referenced ("referenced widely in the RAG community"). Cross-domain is fine but less concrete than Monday's. Problem 4 (reproduce Lost-in-the-Middle on Opus 4.7) is excellent but may be out of scope for a one-afternoon exercise on a 500K-token synthetic doc.

**Line-level fix targets.**
- L217–224 (war stories): Endex 10%→0% should be flagged as "from Anthropic's own launch post — treat as vendor disclosure, not independent eval." LinkedIn case should link to the specific engineering-blog post.
- L295 (Darren Edge reviewer): his pushback is that GraphRAG is a family — could name the three variants (full / Lazy / drift-aware) explicitly and which workload each fits.
- Problem 4: consider splitting into "quick version" (5 positions, 3 trials) vs "full version" (the current spec) so a busy reader still gets the methodological point.

**Rollup: 8.74** — cost-per-correct-answer is the best teaching move of the week. Ship.

### 06-sat — RAG evaluation (8.75)

**Strongest.** Hamel numbers laid bare (Nurture Boss 33%→95%, Honeycomb 70%→90% over three rubric iterations, the 15–20% agreement bump from example critiques) are the week's best *deploy-ready numbers*. RAGAS faithfulness failure modes (statement-extraction errors, judge permissiveness, confidently-wrong-factually-grounded) are stated precisely enough that a reader can diagnose them in their own output. The Zheng-aligned vs Hamel-aligned resolution ("start pairwise for breadth, layer narrow rubrics for specific failure modes — both, not either") is the pragmatically correct synthesis. Block 2 thesis fit (9.5) is the highest of the week — this lesson is *why* Block 2 exists: the moat is evals.

**Weakest.** Build-vs-buy table (LangSmith / Braintrust / Phoenix / Helicone / DeepEval) is fair but light on concrete dollar comparisons — Ankur Goyal's reviewer pushback correctly notes this. Position bias paper (arxiv 2406.07791) is cited for the "worst at close quality" finding but the specific numeric degradation is not quoted.

**Line-level fix targets.**
- L108–122 (build-vs-buy): add a 5-col cost-at-100-queries/day row under each option for the Problem 5 answer to key off.
- L86 (position bias): add the specific measured degradation (e.g., "up to X% swing when quality gap is <Y%") from the paper's Table 2/3.
- Problem 2 (LLM-judge reliability conditions): the rubric requires 3 post-2024 cites — should specify which two of 2411.15594 / 2406.07791 / 2410.02736 are substitutable vs required.

**Rollup: 8.75** — the capstone-before-synthesis lesson. Ship.

### 07-sun — Synthesis quiz + flashcards (8.07)

**Strongest.** Two-parallel-ladders frame (sales agent Mon–Wed / RAG Thu–Sat joined at Saturday's eval discipline) is the correct structural thesis of the week — it connects Week 4 to every subsequent Block 2 week. The mental-move table (13 moves with Apply/Do-NOT-apply columns) is the most useful takeaway artifact. Q20 (long-context-obsoletes-RAG defense) with both sides specified is a good capstone question. End-to-end runnable exercise commits the reader to a 4-hour / 40-hour milestone with named sunset criteria.

**Weakest.** Synthesis lessons in this vault have structurally lower scores than L3 weekday lessons because the surface area compresses depth (this is expected — not a content defect). Reviewer-lens section is weaker than weekday lessons (7.5) — Lilian Weng and Marta Domínguez are named but their specific quotes are inferred rather than cited. Operator war stories are absent by design (synthesis format). Some flashcards (#17, #27) are reasonable but could reach for more specific numbers rather than author+year.

**Line-level fix targets.**
- L171 (Q3 answer): the "defensible answer requires citing a specific disclosure" framing is correct pedagogy but thin — add one *known-good* answer as a reference (e.g., Clay's 10× OpenAI prospecting number) so the reader has a calibration anchor.
- Q12 answer (L224): lists "Gemini Text Embedding 004" as the best-performing CR embedder — cross-check this against Anthropic's original post, which uses OpenAI text-embedding-3-large or Voyage variants in their published table. If Gemini-004 is from a different source, tag it.
- Flashcards: consider adding 3–5 cards on the reviewer-lens pushbacks (e.g., "Kiela's RAG 2.0 critique of CR in one sentence?") since those are load-bearing for the week's thesis.

**Rollup: 8.07** — meets the 8.0 floor, expected compression for synthesis format. Ship with Q12 fact-check.

---

## Week-level notes

### Arc coherence

Strong. Monday defines the pipeline → Tuesday gives the architectural vocabulary (workflows-vs-autonomous, MCP, tool schemas) → Wednesday handles the production infrastructure layer sales can't skip → Thursday opens RAG with the same workflow-vocab discipline → Friday pushes RAG to the frontier → Saturday is the eval moat that closes both ladders → Sunday weaves the thesis. Each lesson has a working prerequisites block that references the prior day without re-teaching.

The **joint-at-the-top** (Saturday's eval applies to both ladders) is the week's load-bearing structural claim and it holds. The sales ladder ending at Wednesday and the RAG ladder starting at Thursday with no hand-off lesson is a minor discontinuity — Tuesday does some of the bridging (MCP connector + tool-use schema generalizes), but a reader who wants "what's my sales agent's RAG layer?" will need to synthesize it themselves from Tue + Thu. Acceptable.

### Duplication

Minimal. 11x scandal appears across Mon / Wed / synthesis but each time in a different analytical frame (Mon: disclosure-gap architecture; Wed: deliverability-collapse consequence; Sun: controversy anchor). Anthropic Building Effective Agents is cited in Tue / Sun — correctly load-bearing both times. Contextual Retrieval 49% number appears Thu / Fri / Sun — each time in a different use (Thu: primary teaching; Fri: as baseline for next-level; Sun: quiz). No lesson over-repeats its own earlier framing.

### Phase 3 priorities (polish targets)

1. **Mon L88 Stebbings citation:** downgrade or verify primary 20VC source — single highest-leverage citation fix.
2. **Sun Q12:** fact-check "Gemini Text Embedding 004" as best CR embedder against Anthropic's original post — synthesis quiz answers should not introduce unverified claims.
3. **Thu war stories:** if any of the three anonymized corpora can be tied to named, publicly-disclosed operator accounts (Harvey, Casetext, Bloomberg, etc.), upgrade — currently the weakest citation layer in an otherwise strong lesson.
4. **Tue cross-domain:** add one 100-word paragraph generalizing the 5 workflow patterns to a non-sales vertical (legal research agent, medical triage, or marketing ops) to lift the 7.5 cross-domain score.
5. **Sat build-vs-buy:** add concrete dollar numbers to the 5-platform comparison table at N=100 queries/day, 6 months — answers Goyal's reviewer pushback and makes Problem 5 gradeable.
6. **Wed reviewer-lens:** pull direct Becker Mailgun interview quotes rather than paraphrased pushback.

None of these are blocking. The week is ship-ready at current state; Phase 3 polish would lift the avg from 8.65 toward 8.8+.

### Flagged lesson count

**0 lessons flagged** (none below 8.0). Synthesis at 8.07 is the closest to the floor and is at expected synthesis-format compression.

---

_Reviewed: 2026-04-17 by rotated multi-persona panel (Karpathy / Huyen / Jerry Liu / Jason Liu / Willison / Chase / Cherny / Weng / Kiela / Hylak)._
