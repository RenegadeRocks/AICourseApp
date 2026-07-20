---
type: review
phase: 2
week: week-06
reviewer: multi-persona 13-lens
date: 2026-07-17
---

# Week 6 — Phase 2 Multi-Persona Review (+ surgical polish applied)

Scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0; the other ten personas = 0.8 (total 11.0). Reviewed cold against `quality-standard.md`, `.claude/block-3-briefs/_generator-base.md` (anti-slop + canonical-home map), and `week-06-briefs.md`.

Mechanical checks run this session: `python -m py_compile` on all three code-lab modules (pass, incl. after edits); `queries.example.jsonl` JSON-valid; **all 14 distinct wikilink targets resolve** to real vault files (verified by script + `find`); em-dash density recomputed per file; contrast-tic scan; WebSearch spot-checks (NoLiMa "11 models < 50% at 32K, GPT-4o 99.3→69.7" — confirmed against arXiv 2502.05167 abstract + two secondaries; Karpathy tweet Jun 25, 2025 — confirmed; Lütke post date shows Jun 18 *or* 19 depending on timezone — see verify list). WebFetch egress-blocked, so no liveness pass on URLs; the lessons already flag this per-citation, which is the correct hedge.

---

## 00-overview

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Thesis names the mechanism (advertised vs effective windows) up front; no benchmark numbers asserted that the dailies don't own. |
| Chip Huyen | 8 | "What configuration of tokens… and how do you know" is the right through-line; day table maps cleanly to deliverables. |
| Jerry Liu | 8 | Retrieval correctly framed as one tool inside a context strategy, matching the brief's arc. |
| Hamel Husain | 8 | Eval-threshold prerequisite (≥90% judge agreement) linked, not re-taught. |
| Simon Willison | 8 | No overclaims; the "naive conclusion is wrong" setup is earned by Monday. |
| Seibel | 9 | Short, sells the week in two paragraphs. |
| Boris Cherny | 8 | Correctly points at Claude Code patterns without teaching them here. |
| Cohort peer | 9 | "Prove each token pays rent" is a sellable sentence. |
| Mira Murati | 8 | Positions the skill commercially without hype. |
| swyx | 8 | Frames the rename debate as content, not marketing. |
| Ethan Mollick | 8 | Prereq honesty ("you have felt an agent degrade") is good pedagogy. |
| Lilian Weng | 8 | Terminology (compaction, isolation, JIT) used consistently with the dailies. |
| Jeremy Howard | 8 | No re-teaching; links carry the load. |

**Weighted average: 8.1**

---

## 01-mon — Context engineering: the successor discipline

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Attention-budget mechanism before benchmarks; his own caveat (context engineering as one slice of the software layer) is surfaced in the lens rather than hidden. |
| Chip Huyen | 8 | Window-composition table is operator-shaped and honestly labeled as estimate, not benchmark; cost framing concrete. |
| Jerry Liu | 8 | JIT-vs-preload tradeoff table is balanced; hybrid conclusion correct. |
| Hamel Husain | 8 | Lens admits "/context audit is not an eval" and defers to Friday — right call; Phase-3 ablation is honestly labeled a toy. |
| Simon Willison | 9 | Skeptics' case steelmanned with named sources; every fast-moving claim carries the egress-blocked hedge; primary-source discipline on the Karpathy/Lütke quotes. |
| Seibel | 7 | Layer 5 spends a lot of words adjudicating a noun; the lens itself concedes this. |
| Boris Cherny | 8 | Tool-definition tax and MCP on-demand loading accurate to current Claude Code behavior. |
| Cohort peer | 9 | Cross-domain examples (sales/legal/exec) make the budget sellable to non-engineers. |
| Mira Murati | 7 | Nothing on when to *change models* rather than change context; defensible scope. |
| swyx | 8 | "Harness engineering will contest the ground" is the right treadmill-awareness. |
| Ethan Mollick | 8 | Problem set has pass/fail bars, not vibes. |
| Lilian Weng | 8 | NoLiMa/RULER/Chroma triangulation is the correct evidence set; spot-checked numbers verified. |
| Jeremy Howard | 8 | His pushback (naming disputes inflate catalogs) is in the lens, answered honestly. |

**Weighted average: 8.1**

Notes: [^7] (awesomeagents.ai / ofox.ai leaderboard analyses) is the thinnest citation in the file and the lesson correctly labels its 30–60-point figure "indicative." Word count 4.3K vs the 5–6.5K L3 soft target — density is high, so acceptable under "density over length."

---

## 02-tue — Memory & compaction architectures

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Four-primitive decomposition is genuinely mechanistic; compaction-as-lossy-loss-function is the right frame. |
| Chip Huyen | 9 | 15×/90.2%/80%-variance economics stated with both edges; per-product vs per-customer memory case is real ops thinking. |
| Jerry Liu | 8 | "Memory system = write-policy × retrieval × placement" collapses vendor marketing correctly. |
| Hamel Husain | 8 | Experiment grades compaction against notes on the reader's own data; contamination red-team has measurable outcomes. |
| Simon Willison | 9 | His dossier argument rendered accurately in three parts with the wedding-ring/Half Moon Bay specifics; lens correctly says the injection threat deserves more than one reflection question. |
| Seibel | 7 | Long; the build-vs-buy answer arrives only in the lens. |
| Boris Cherny | 8 | Claude Code compaction stages correctly labeled reverse-engineered/indicative. |
| Cohort peer | 9 | Agency-with-five-clients example and "show the client their memory file" are directly usable. |
| Mira Murati | 7 | Vendor landscape is rent-only; no fine-tuned/learned-memory angle. |
| swyx | 8 | Moat-vs-contamination is the correct 2026 framing with the incentive problem named. |
| Ethan Mollick | 8 | Phase-3 contamination experiment is teachably cheap. |
| Lilian Weng | 8 | Her convergence critique is in the lens; taxonomy tidiness acknowledged. |
| Jeremy Howard | 8 | CLAUDE.md canonical home linked with one-line recap only — compliant. |

**Weighted average: 8.2**

Notes: "LoCoMo… small (81 QA pairs in its core set)" — the 81 figure is the one number in the file I could not corroborate this session; see verify list.

---

## 03-wed — Retrieval beyond naive RAG

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | MaxSim mechanism explained correctly; "interview question pays more than the deployment" is honest sizing. |
| Chip Huyen | 9 | Reranker-ROI-lives-in-window-savings (Case 1) is a genuinely non-obvious production insight. |
| Jerry Liu | 9 | Five-family map explicitly subordinated to Thursday's agentic loop; graph-as-a-lane case study is right-sized. |
| Hamel Husain | 7 | "Leaderboard ELO is not your corpus" is said, but the lesson still leans on one ELO board for the market map. |
| Simon Willison | 7 | License catch (zerank-2 CC-BY-NC) is exactly his kind of point, but the reranker-market citations are SEO-blog tier (bestaiweb.ai, futureagi) — weakest sourcing in the week. |
| Seibel | 8 | Graph-refusal memo problem is the ship-the-ugly-thing ethos as an artifact. |
| Boris Cherny | 8 | "One index format too many" consistency-liability point is the tooling truth. |
| Cohort peer | 9 | Three-corpora case studies (labeled composites) map to jobs readers actually have. |
| Mira Murati | 8 | Her fine-tuned-reranker pushback is present in the lens. |
| swyx | 8 | GraphRAG hype cycle handled with named cost multiples, not sneering. |
| Ethan Mollick | 8 | Two-question triage is teachable to non-engineers. |
| Lilian Weng | 8 | PLAID/ColBERT-v2 numbers match the papers. |
| Jeremy Howard | 8 | Contextual Retrieval ladder wikilinked, one-line recap only — compliant. |

**Weighted average: 8.1**

---

## 04-thu — Agentic retrieval

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 9 | Lens names `sufficient(evidence)` as the unsolved problem hiding in a function name — the sharpest self-critique in the week. |
| Chip Huyen | 9 | The refusal-arithmetic table is correct (checked: $0.018/$0.1125/query, $180 vs $1,125/day) and labeled illustrative. |
| Jerry Liu | 8 | "RAG is dead" resolved to the hybrid consensus with his own 2024 lineage cited. |
| Hamel Husain | 8 | Phase-3 2×2 with the validated-judge prerequisite enforced; stopping-behavior eval gap named in mistakes. |
| Simon Willison | 8 | Cherny quote honestly attributed "via secondary accounts"; over-reading-the-grep-result warned against. |
| Seibel | 8 | Help-desk rollback case is the do-the-boring-thing lesson with a user-behavior metric. |
| Boris Cherny | 9 | His position rendered with a real disagreement (simplicity vs tiered routing) and the honest note that it depends on traffic shape. |
| Cohort peer | 9 | Escalation-trigger engineering is the sellable skill; trace-autopsy problem is concrete. |
| Mira Murati | 7 | Search-R1 RL-policy line gestures at trained policies but stays surface. |
| swyx | 8 | Deep-research commoditization take is his actual position, correctly placed. |
| Ethan Mollick | 8 | "Novelty is not a routing policy" case study lands for org readers. |
| Lilian Weng | 8 | Loop decomposition (plan/reformulate/stop/ground) matches the agent literature. |
| Jeremy Howard | 8 | MCP tool-use canonical home linked, not re-taught — compliant. |

**Weighted average: 8.3**

Notes: [^1] and [^2] are secondary-source-only (medium.com/blog coverage of the podcast and the AAAI paper) — properly flagged in-line, but Phase 4 should try to land the primary Latent Space episode URL and the actual Amazon Science paper page.

---

## 05-fri — Evaluating context strategies

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | "Decorated randomness" and the prior/posterior framing of leaderboards are exactly right. |
| Chip Huyen | 9 | Her missing-monitoring-twin critique is in the lens and referenced forward by Saturday — the seam works. |
| Jerry Liu | 8 | Vendor-number translation layer (39%/94.5%/90.2% → your experiment) is the most reusable section of the week. |
| Hamel Husain | 9 | His error-analysis-first objection is stated *against the lesson's own ordering* and conceded — rare honesty; ≥90% bar enforced as prerequisite everywhere. |
| Simon Willison | 8 | Answerability slice and citation-faithfulness drift warning are the security-adjacent truths. |
| Seibel | 8 | Mollick's minimum-viable-eval concession stops the lesson from being rigor cosplay. |
| Boris Cherny | 8 | Judge-pinning and tokenizer-shift warnings are correct tooling hygiene. |
| Cohort peer | 8 | Panel-diagnosis drill (four signatures) is a genuinely good exercise. |
| Mira Murati | 7 | Nothing on eval transfer across model families beyond "re-measure." |
| swyx | 8 | Four-way decomposition (task/harness/judge/budget) is a durable meme. |
| Ethan Mollick | 9 | His adoption-reality critique is present and changes the advice. |
| Lilian Weng | 8 | Long-context eval method faithful to NoLiMa/RULER definitions. |
| Jeremy Howard | 8 | Deletion-rows discipline is the fast.ai-style pragmatism. |

**Weighted average: 8.3**

---

## 06-sat — BUILD: context-engineered RAG v2

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Layer-0 decisions (hand-rolled vs platform, pinning, harness placement) are the systems content most builds skip. |
| Chip Huyen | 8 | Cost ledger with the meta-question ("what did the evidence cost") is production-grade honesty. |
| Jerry Liu | 8 | Stage composition + interaction warning is methodologically right. |
| Hamel Husain | 9 | Pre-registered gates, rubber-stamp warning, holdout slice, "at least one row should fail" — his protocol executed. |
| Simon Willison | 8 | "A report that names its own blind spot is more credible" is the right epistemics. |
| Seibel | 9 | His ship-two-lanes-and-find-a-customer pushback is in the lens with the honest counter-case. |
| Boris Cherny | 9 | Harness-as-liability critique present with the intended retirement path (keep evals, let platform eat lanes). |
| Cohort peer | 9 | Judge-revalidation-first warning is the real Saturday failure mode. |
| Mira Murati | 7 | No fine-tuning lane even as a stretch goal. |
| swyx | 8 | Client one-pager stretch goal is the distribution insight. |
| Ethan Mollick | 8 | 3–5 hour scoping with stage timings is respectful of a solo operator. |
| Lilian Weng | 7 | Memory lane's measurement design has a flaw the lesson doesn't see (see unresolved concerns). |
| Jeremy Howard | 8 | Deletion row promoted to a first-class stage. |

**Weighted average: 8.2** (post-polish; the doc/code mismatches found below were fixed this session)

---

## 07-sun — Synthesis + quiz + flashcards

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Q15/A15 rewards reconstruction from mechanism, not citation recall. |
| Chip Huyen | 8 | Operator decision table is a keeper artifact; every row traces to a day. |
| Jerry Liu | 8 | Synthesis subordinates retrieval to context strategy exactly as the brief demanded. |
| Hamel Husain | 9 | Q13/A13 (spread vs margin) and A14 (why upgrades erode declining) are the discipline, tested. |
| Simon Willison | 8 | A6 compresses his argument correctly; open-questions section is honest about unsettled ground. |
| Seibel | 8 | Capstone option 2 (productized audit) is the commercial move. |
| Boris Cherny | 8 | Open question on platform eating the hand-rolled lanes is the right forward pointer. |
| Cohort peer | 9 | Quiz difficulty is calibrated: Q7 calc checked and correct ($46/day → $1,380/month). |
| Mira Murati | 7 | Capstones are all rent-the-frontier shapes. |
| swyx | 8 | "No MMLU for memory yet" is the accurate ecosystem read. |
| Ethan Mollick | 9 | 30-day capstone with pre-registered gate is behavior design, not content. |
| Lilian Weng | 8 | Flashcards 1–30 all check against the weekday lessons; no contradictions found. |
| Jeremy Howard | 8 | No duplicate territory with the Week-4 quiz (RAGAS/judge-bias correctly ceded). |

**Weighted average: 8.2**

Consistency audit (Sunday vs weekdays): all shared numbers identical across files — 90.2% / ~15× / ~80% variance; +39% / +29% / 84%; 94.5% / ~24%; 0.1% / 700×; 3–10× / 2–5×; 99.3→69.7; ≥85% NoLiMa threshold; $2/$10→$3/$15 Sonnet 5; zerank-2 ≈1638 / Cohere v4.0 Pro ≈1629; CC-BY-NC. Q7's inputs match Thursday's table exactly.

---

## code-lab/6 (README, requirements, run_ablation.py, harness.py, judge.py, queries.example.jsonl)

| Persona | Rating | One-line justification |
|---|---|---|
| Karpathy | 8 | Small, readable, trace-first; the RRF/BM25S/Chroma wiring is correct and minimal. |
| Chip Huyen | 8 | Cost estimate + confirmation gate above $5; pipeline vs measurement cost split. |
| Jerry Liu | 7 | `hybrid_tuned` maps to `lane_baseline` with the sweep promised in run_ablation but no sweep code present — doc overpromises (see concerns). |
| Hamel Husain | 8 | `judge.py --validate` implements the ≥90% bar with per-dimension breakdown — the discipline, shipped. |
| Simon Willison | 8 | Keys via env only; nothing persists outside results/ and the memory file; NOT_IN_CORPUS contract is inspectable. |
| Seibel | 9 | Teaching implementation that admits it ("not a product") — correct scope. |
| Boris Cherny | 8 | Pinned deps + lock-file instruction; model IDs env-sourced so they don't fossilize. |
| Cohort peer | 9 | README is genuinely runnable: data layout, commands, lane table. |
| Mira Murati | 7 | Embedder swap relegated to a note; fine for scope. |
| swyx | 8 | Lane taxonomy matches the lesson 1:1 post-polish. |
| Ethan Mollick | 8 | The confirmation prompt before spend is good default paternalism. |
| Lilian Weng | 7 | Memory-lane scoring design doesn't produce what the lesson claims (below). |
| Jeremy Howard | 8 | bm25s choice justified with a citation; chunking crude but honest. |

**Weighted average: 7.9**

---

## Overall Week 6: **8.2 / 10**

(File averages: 8.1, 8.1, 8.2, 8.1, 8.3, 8.3, 8.2, 8.2, 7.9.) Strongest: Thursday and Friday — live controversies with named positions, correct arithmetic, and reviewer lenses that genuinely disagree with the text. Weakest: code-lab (7.9) — solid teaching harness, but two doc/code promises exceeded the implementation (both now reconciled or logged). Anti-slop: contrast tics ≤2/file everywhere (Mon's two regex hits are a quoted essay title); em-dash density now ≤ ~12/1k in all files after trims; house tics within budget ("operator" 4× in Mon is the ceiling; "would push back" 2× total; "load-bearing" 2× total). Canonical homes: all four (MCP/trifecta, CR ladder, eval threshold, CLAUDE.md) wikilinked with one-line recaps — no re-teaching found. NANDA 95% not referenced (fine; not needed this week).

---

## Surgical fixes applied this session (Phase 3, done)

1. **01-mon Layer 2:** removed "Gemini 3.5 Flash" and "Kimi K3" from the 1M-window model list — Gemini 3.5 is on the master report's do-not-teach-as-fact list and K3's window is unverified; list now Sonnet 5 / Fable 5 / GPT-5.5, all verified in the binding lineup.
2. **01-mon Layer 2:** "$2–$10 per million input tokens" conflated input/output prices → "$2 per million input tokens at Sonnet 5 intro pricing ($3 after 2026-08-31)".
3. **run_ablation.py:** judge context was truncated to 400 chars/chunk while the generator saw full chunks — systematic false faithfulness failures; judge now sees the full generation context.
4. **harness.py `lane_tiered`:** README and lesson promise hard caps of 6 calls / 40K tokens / 30s, but only the call cap existed — token and wall-clock caps now enforced in the loop.
5. **harness.py `lane_v2_composed`:** pre-escalation model spend was dropped from usage when the lane escalated — now folded into the reported usage.
6. **06-sat Stage 4:** trigger description ("retrieval-confidence floor and judge-flagged insufficiency") didn't match the shipped code — reworded to the actual pair (generation-declared NOT_IN_CORPUS + retrieval-diversity floor).
7. **Em-dash overage:** trimmed 00-overview 12.8→10.0, 01-mon 12.3→11.9, 05-fri 12.4→12.1, 06-sat 13.7→11.6, 07-sun 13.2→11.4 per 1k words (comma/colon/paren substitutions only; no content changes).

All Python re-compiled clean after edits.

## Unresolved concerns (recommendations, not applied)

1. **Memory-lane measurement flaw (code-lab + 06-sat Stage 3).** The lesson says memory is scored "by running the regression set twice and comparing second-pass metrics," but (a) `lane_memory` never *writes* memory — only `lane_tiered` does — so unless tiered ran first, pass 2 ≡ pass 1; (b) run_ablation runs each *query* twice consecutively, not the set twice, and discards first-pass usage from cost. Fixing requires a design decision (seed memory from a tiered pre-pass, or score set-level pass deltas) — restructuring, so left for the author.
2. **`hybrid_tuned` sweep is vaporware:** README/run_ablation promise an RRF/k sweep; `LANES["hybrid_tuned"]` is just `lane_baseline`. Either implement the sweep or demote the lane to "manual: edit params" in the README.
3. **Word counts** run 2.7–4.3K vs the L3 5–6.5K soft target on every daily. Density is genuinely high and the brief says density over length, but Mon/Tue could absorb 500 more words each on the missing angles their own lenses name (injection threat model on Tue; model-routing on Mon).
4. **Wed's reranker-market sourcing** is the citation weak point of the week (agentset.ai ELO + SEO-tier roundups). The in-text hedges are correct; Phase 4 should prioritize primary vendor docs for the four models and the zerank-2 license.

## Phase 4 citation-verify list

1. Mon/Sun [^1]: Lütke post date — lesson says June 19, 2025; one secondary says June 18 (timezone split). Pin to the tweet's own timestamp.
2. Tue [^8]: LoCoMo "81 QA pairs in its core set" — could not corroborate this session; verify or soften to "small."
3. Tue [^7]: Axios ChatGPT-memory URL/date (2025/07/11) — verify the article exists with that framing.
4. Wed [^1]: Agentset ELO figures (≈1638 / ≈1629) and board freshness.
5. Wed [^3]: Jina-ColBERT-v2 "89 languages" and 0.521 BEIR average against the paper PDF.
6. Thu [^1]: land the primary Latent Space episode URL for the Cherny quote.
7. Thu/Fri [^2]/[^8]: the actual Amazon Science / AAAI 2026 paper page for the 94.5% / ~24% figures.
8. Wed [^7]: BIRD top entry "~81.95% (AskData + GPT-4o)" against the live leaderboard.
9. Mon/Thu/Sat [^8]/[^6]/[^5]: Sonnet 5 intro-pricing end date 2026-08-31 against the Anthropic pricing page.
10. Sat requirements.txt: `anthropic==0.116.0` / `chromadb==1.5.9` currency on PyPI.

---

_Review + surgical polish produced 2026-07-17. Files edited: 01-mon, 05-fri, 06-sat, 07-sun, 00-overview, code-lab/6/run_ablation.py, code-lab/6/harness.py. No git commits made._
