---
type: review
phase: 2
week: week-08
reviewer: multi-persona 13-lens (Karpathy / Chip Huyen / Jerry Liu / Hamel Husain / Simon Willison / Seibel / Boris Cherny / cohort peer / Mira Murati / swyx / Ethan Mollick / Lilian Weng / Jeremy Howard)
date: 2026-07-17
---

# Week 8 — Phase 2 Multi-Persona Review

Scoring scale 1–10. Weights: Karpathy / Hamel / Simon = 1.0 each; the other ten = 0.8 each (11.0 total weight). Reviewer did not write this week; judged cold against `quality-standard.md`, `_generator-base.md`, and `week-08-briefs.md`, with `block-0/week-02` lessons 01–02 read to verify no re-teaching.

## Hard checks (ran before scoring)

- **Code-lab compiles**: all 17 `.py` files pass `py_compile` (before and after fixes).
- **Internal consistency — cost math**: $0.45 intro / ~$0.68 post-Aug per run and ~$14–20/mo are arithmetically correct (150K in × $2/M + 15K out × $10/M) and identical across 01-mon, 06-sat, and code-lab README. Make credit math ($1.5–1.8/mo computed vs "~$2–7/mo" stated) is loose but hedged with "~" and plan-variability; acceptable.
- **Internal consistency — retry semantics**: 429=TRANSIENT, non-429 4xx/auth/schema/ToS=PERMANENT is identical across 02-tue, 04-thu, 06-sat, quiz Q9/A9, `common/schema.py`. Clean.
- **Internal consistency — stage names**: the 8-stage table (fetch/extract/dedup/relevance-judge/synthesize/validate/deliver/record+alert) matches across 04-thu, 06-sat, README, and code files (stage 8 = `monitor.py`, mapped explicitly in the README).
- **Found and fixed**: two real code-lab bugs and one lesson/code mismatch (see Surgical fixes).
- **No re-teaching**: 02-tue explicitly assumes b0w02 cold, recaps the trifecta in one line + wikilink, points the June-2025 auth revision at `[[01-mon-mcp-as-a-protocol]]`, and builds only the Nov-2025/RC *application* layer. Verified against b0w02 01-mon/02-tue — the RC coverage overlaps b0w02's refreshed survey paragraph but goes materially deeper (Tasks extension, serverless implications); acceptable. TRANSIENT/PERMANENT is recapped in one line + wikilink per the rule.
- **Wikilinks**: all 14 distinct targets resolve to existing vault files. Every lesson has ≥2 links to earlier lessons.
- **Quiz/flashcards vs lessons**: all 15 questions and 25 flashcards trace to taught content; answer key spot-checked correct (A3 allowlist, A5 RC statelessness, A7 Sept-15 defaults, A9 classification, A13 green≠success).
- **Anti-slop**: contrast-scaffold tic within ≤2/file everywhere except 07-sun (5× "The decision is not X but Y" — reduced to 2, see fixes). "load-bearing" 1×, "would push back" 1× across the week — fine. **Em-dash density is the week's systemic miss: 17–23/1k words in lesson bodies (cap ~12/1k), every file.** Not surgically fixable; flagged for Phase 3.
- **Citation hedging**: exemplary — every egress-blocked source is marked "search-verified; fetch egress-blocked — liveness pass pending," survey stats labeled survey-grade, the RC consistently framed as scheduled-not-shipped, EU AI Act dates framed as upcoming. One slip fixed: 03-wed [^so] claimed structured-outputs GA "across … Mythos 5 …" — Mythos 5 is restricted-access (Project Glasswing, per landscape delta) and the lesson body doesn't claim it; dropped from the citation.

---

## Per-file scores

### 01-mon — The automation spectrum in 2026 — **8.3**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 9 | Three-tier scheduling table is mechanism-first; jitter/expiry read as design signals, not trivia. |
| Hamel | 1.0 | 7 | Experiment "grade its answers" lacks a quantified pass bar; placement drill has no N or rubric. |
| Simon | 1.0 | 9 | `<routine-fire-payload>` untrusted-wrapping and allowlist-by-default read exactly right, credited to docs fetched live. |
| Chip Huyen | 0.8 | 9 | Cost tables date-stamped, intro-vs-post-Aug split, and the honest "cost doesn't discriminate at solo scale" conclusion. |
| Jerry Liu | 0.8 | 8 | Lane taxonomy fair to frameworks; LangGraph/LlamaIndex placed without strawmanning. |
| Seibel | 0.8 | 8 | Lesson pre-empts him in the reviewer lens and concedes "decide fast and ship." |
| Boris Cherny | 0.8 | 9 | Session-tier vs production-tier warning is his exact beat, made explicit. |
| Cohort peer | 0.8 | 9 | Placement drill (5 scenarios) is immediately reusable with clients. |
| Mira Murati | 0.8 | 8 | Platform-strategy reading of SAP/n8n and dynamic workflows is sharp. |
| swyx | 0.8 | 9 | "The model writes the workflow" trajectory call is the right meta-observation. |
| Mollick | 0.8 | 8 | Reflection questions genuinely non-Googleable. |
| Lilian Weng | 0.8 | 7 | Agent-autonomy framing thin here (deferred to Fri, defensible). |
| Howard | 0.8 | 8 | Migration-of-judgment-steps-to-heuristics is the practitioner's insight. |

### 02-tue — MCP integration patterns — **8.2**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 9 | Stateless-RC mechanics (`_meta`, no handshake, tasks-as-extension) explained causally, not as changelog. |
| Hamel | 1.0 | 7 | Experiment step 4's OWASP audit has no acceptance criterion; "grade its answer" again unquantified. |
| Simon | 1.0 | 9 | Reviewer lens *corrects the lesson's own* "breaks the trifecta by construction" overclaim via the `reason`-field seam — honest and right. |
| Chip Huyen | 0.8 | 9 | Idempotency section ("everything eventually runs twice") is the production paragraph of the week. |
| Jerry Liu | 0.8 | 8 | Two-tool asceticism vs framework-growth tension engaged both ways. |
| Seibel | 0.8 | 7 | Heaviest lesson of the week; peer-reviewer question deflates it only partially. |
| Boris | 0.8 | 9 | Service-identity/blast-radius discipline is exactly fleet-scale hygiene. |
| Peer | 0.8 | 9 | "Do I need CIMD for a personal digest?" answered honestly: no. |
| Mira | 0.8 | 8 | Spec-establishment vs security-research controversy has real named positions. |
| swyx | 0.8 | 8 | Pattern C (automation-as-MCP-server = product surface) is the ecosystem insight. |
| Mollick | 0.8 | 8 | Reflection Q5 (state the principle once) is good pedagogy. |
| Lilian | 0.8 | 8 | Privilege-separation-as-architecture aligns with her agent-safety writing. |
| Howard | 0.8 | 7 | Could use one more worked auth example end-to-end. |

### 03-wed — The scraping stack, legally and technically — **8.1**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 8 | Fetch/render/extract decomposition and the extraction ladder are clean mechanism. |
| Hamel | 1.0 | 7 | Policy exercise produces an artifact but no check on its quality. |
| Simon | 1.0 | 9 | Reviewer lens has him correcting the lesson's piety toward proportionate permission — his actual position, well used. |
| Chip | 0.8 | 8 | Cost-the-stack drill good; her maintenance-cost critique is in the lens but not the table (her own noted complaint). |
| Jerry | 0.8 | 8 | Schemas-not-regex tied back to `[[03-wed-rag-as-a-system]]` correctly. |
| Seibel | 0.8 | 8 | "For Saturday, RSS + requests" keeps it shippable. |
| Boris | 0.8 | 8 | Conditional-requests and door-closing-as-handled-event are the right ops instincts. |
| Peer | 0.8 | 9 | hiQ told straight (settled on contract!) is worth the lesson alone. |
| Mira | 0.8 | 8 | Publisher-side reviewer lens (license vs scrape) is a genuinely distinct third voice. |
| swyx | 0.8 | 9 | Content-Independence-Day framing is the correct 2026 reorganizing fact. |
| Mollick | 0.8 | 9 | Reflection Q5 (business case against cheating) is applied-ethics done right. |
| Lilian | 0.8 | 7 | Injection-via-scraped-content deferred to Tue/Thu; one pointer would help. |
| Howard | 0.8 | 8 | Practical ladder + honest disclaimer. |

### 04-thu — Hybrid agent design — **8.3**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 9 | "Nameable failure is fixable failure"; checkpoint/idempotency/non-idempotent-LLM reasoning is exact. |
| Hamel | 1.0 | 8 | Design-artifact experiment with gradeable outputs; drift detectors quantified (fill-rate, volume). |
| Simon | 1.0 | 8 | Not his beat, but validator-as-containment is security-correct. |
| Chip | 0.8 | 9 | Her lens's rolling-cost-monitor point is real and correctly conceded. |
| Jerry | 0.8 | 8 | Workflows-1.0 study-then-graduate posture is fair to frameworks. |
| Seibel | 0.8 | 8 | Lens concedes "spine + contract first, armor when earned." |
| Boris | 0.8 | 9 | Checkpoint store rules are the production discipline. |
| Peer | 0.8 | 8 | Stage table is directly reusable. |
| Mira | 0.8 | 8 | Output-contract framing scales to org level. |
| swyx | 0.8 | 8 | OTel GenAI conventions placed as graduation path, not cargo cult. |
| Lilian | 0.8 | 9 | Her lens (reflection as controlled stages 4a/4b, not ambient autonomy) is the best persona argument in the week. |
| Mollick | 0.8 | 8 | Reflection Q5 (readers notice before you) is the right fear. |
| Howard | 0.8 | 8 | Cheap-tier judging / expensive synthesis is the fast.ai instinct. |

### 05-fri — Reliability engineering — **8.4**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 8 | Golden-set-as-fixed-reference logic for model drift is exactly right. |
| Hamel | 1.0 | 9 | His lens catches the lesson's own sequencing error (error analysis before golden set) and the lesson concedes it — the FAQ discipline, correctly credited. |
| Simon | 1.0 | 9 | Hallucination-containment stack layered cheapest-first; honest "no stack makes it perfectly safe." |
| Chip | 0.8 | 9 | Rolling-weekly cost trend operationalizes her Thursday critique. |
| Jerry | 0.8 | 8 | Eval decomposition maps cleanly onto the pipeline stages. |
| Seibel | 0.8 | 8 | "You-as-the-eval-harness in week one" concession is the honest sequence. |
| Boris | 0.8 | 8 | Kill switch shaped after `CLAUDE_CODE_DISABLE_CRON` — right pattern, cited. |
| Peer | 0.8 | 8 | HITL/HOTL rule is applicable Monday morning. |
| Mira | 0.8 | 9 | Autonomy controversy has named positions on both sides (MIT TR vs OWASP/Singapore) without straw men. |
| swyx | 0.8 | 8 | Postmortem→golden-set flywheel is the durable meme. |
| Mollick | 0.8 | 9 | Reflection Q5 (grant the illusion argument fully) is excellent. |
| Lilian | 0.8 | 8 | Reversibility under-specification caught by the safety lens itself. |
| Howard | 0.8 | 8 | Binary-over-scores consistently enforced. |

### 06-sat — Build the hybrid scraper + summarizer — **7.8**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 7 | Milestones are right, but two code-lab guards were dead code as shipped (budget never charged; zero-item drift alert unreachable) — the lesson's chaos-test (e) and (a) would have failed. Fixed this phase. |
| Hamel | 1.0 | 8 | Eval gate is a real gate (`--gate` non-zero exit); day-one-set-as-hypothesis stated. |
| Simon | 1.0 | 8 | Privilege separation implemented (deliver holds the only credential); judge/synth prompts carry ignore-embedded-instructions lines. |
| Chip | 0.8 | 8 | Real-token-counts-into-client-table discipline; $2 ceiling default sane. |
| Jerry | 0.8 | 8 | Checkpoint-store-as-tool-surface consistent with Tue's Pattern B. |
| Seibel | 0.8 | 9 | Milestone 1 = one real brief in 40 minutes; "Milestone 2 alone is a real ship." |
| Boris | 0.8 | 8 | Laptop-cron mortality named in his lens; README carries the graduation path. |
| Peer | 0.8 | 9 | The sellable framing ($200 setup vs $2k/mo managed) is the course's promise kept. |
| Mira | 0.8 | 7 | Thinnest lesson of the week (2,674 words) — leans on the code-lab, which mostly earns it. |
| swyx | 0.8 | 8 | Template-across-niches resale framing is right. |
| Mollick | 0.8 | 8 | Reflection Q6 (the August-31 client email) is applied. |
| Lilian | 0.8 | 7 | No discussion of what the judge/synth models *shouldn't* see; covered elsewhere. |
| Howard | 0.8 | 8 | RSS-first, selectolax, feedparser: pragmatic stack, pinned. |

### 07-sun — Synthesis + quiz + flashcards — **8.1**

| Persona | W | Score | One-liner |
|---|---|---|---|
| Karpathy | 1.0 | 8 | 13-move table compresses the week without distortion. |
| Hamel | 1.0 | 8 | "Golden set = hypothesis wearing a gate's clothing" carried into the lose-points section. |
| Simon | 1.0 | 8 | Quiz A5/A13 keep RC and green-status framing honest. |
| Chip | 0.8 | 8 | Move 3 (post-intro pricing, tokenizer) preserved in compressed form. |
| Jerry | 0.8 | 8 | W6/W7/W8 composition recap does the block-capstone job the brief asked for. |
| Seibel | 0.8 | 8 | "If Saturday is still a design doc, you skipped the week" — correct closing note. |
| Boris | 0.8 | 8 | Move 2 (scheduler never the model) survives compression. |
| Peer | 0.8 | 9 | Flashcards atomic and testable; answer key teaches, not just grades. |
| Mira | 0.8 | 8 | Trust-decomposed thesis is the right unification. |
| swyx | 0.8 | 8 | — |
| Mollick | 0.8 | 9 | Mixed-format quiz with real distractors (A1's per-option rationale). |
| Lilian | 0.8 | 8 | Move 13 states the autonomy rule cleanly. |
| Howard | 0.8 | 8 | — |

**Overall Week 8: 8.2 / 10** (8.3, 8.2, 8.1, 8.3, 8.4, 7.8, 8.1). Weakest: 06-sat — not conceptually, but because two of its advertised guards were unreachable in the code-lab as generated (both fixed). Strongest: 05-fri, whose reviewer lenses genuinely argue against the lesson.

---

## Surgical fixes applied (this phase)

1. **`pipeline.py` + `_count_by_source`**: `items_per_source` now seeds every configured source at 0 — previously a zero-item source was *absent* from the counts, so the flagship "zero-from-productive-source" drift alert in `monitor.check_metrics` could never fire (chaos-test (a) would fail).
2. **Budget enforcement wired**: `RunBudget.charge()` was never called anywhere — `BudgetExceeded` (and the README's "enforces `run_dollar_ceiling` with a controlled stop") was unreachable dead code. `judge.judge_item/judge_all` and `synthesize.synthesize` now accept an optional `budget` and charge real `resp.usage` tokens; `pipeline.py` passes it. `eval/run.py`'s call sites unaffected (param optional).
3. **Brief-length consistency**: 01-mon promises a ~2,500-word brief; `synthesize` capped output at `max_tokens=2000` (~1,500 words, would truncate mid-brief) and the validator/rubric rejected briefs >8,000 chars (~1,300 words). Aligned: `max_tokens=4000`, `max_chars=20000` in `validate.py` and `rubric.py` (with keep-in-sync comments).
4. **`budget.py` price hedging**: Haiku 4.5 line now marked "UNVERIFIED — confirm against the pricing docs"; header notes that an unknown model id falls through to (0,0), which silently disables the ceiling.
5. **03-wed [^so]**: dropped "Mythos 5" from the structured-outputs GA model list (restricted-access model per the landscape delta; body never claimed it; unverifiable here).
6. **07-sun contrast-scaffold tic**: "The decision is not X but Y" reduced from 5 to 2 instances (Wed/Thu/Fri bullets rewritten; Mon/Tue retained).

All Python re-compiled clean after fixes.

## Phase 3 recommendations (not applied — larger than surgical)

1. **Em-dash density** (all files, 17–23/1k vs ~12/1k cap): a week-wide pass converting a third of em-dashes to periods/commas/colons. Highest-density: 02-tue and 06-sat bodies.
2. **Length vs L3 spec**: all six daily lessons run 3.5–4.4k words against the 5,000–6,500 soft target; 06-sat is 2,674. Density is genuinely high (no padding found), and the code-lab carries 06-sat — but if the L3 bar is enforced, 06-sat and 04-thu are the ones to deepen (e.g., a worked chaos-test transcript; a real cost table from an actual run).
3. **`fetch_all` swallows `TransientError`** per-source (records it, moves on), so the orchestrator's `transient_retry` on stage 1 never actually retries a transient source failure. Either re-raise when *all* sources fail, or move retry into `fetch_source`. Design decision — not unambiguous enough for a surgical edit.
4. **`etag_cache={}`** is constructed fresh each run and never persisted, so the conditional-request discipline the lessons emphasize is inert across runs. Persist it (e.g., `runs/etag-cache.json`).
5. **`extract_prose_llm`** uses a top-level *array* JSON schema in `output_format`; structured-outputs implementations commonly require an object root. The docstring hedges ("verify param names against the current SDK") — verify in Phase 4 and wrap in an object if needed.
6. **Hamel-lens gap in experiments** (Mon/Tue/Wed): "grade its answers" steps lack pass bars. Add N and thresholds as b0w02's review did for its Step 5.
7. **`eval/run.py`**: `--validate-judge` and `--gate` execute the same computation; differentiate (validate-judge should report per-item disagreements, not just the aggregate), and extend `--gate` to actually run `rubric.score_brief` against frozen snapshots (currently a TODO comment).

## Phase 4 citation-verify list (liveness pass once egress allows)

1. 01-mon [^5] n8n/SAP $5.2B, Joule Studio GA Q3 2026, 1,400+ enterprise customers.
2. 01-mon [^9] 88% / 41% / 33% / 26% / 64% / 70% failure-stat stack (Digital Applied + CIO.com) — heavily load-bearing across Mon/Fri/Sun.
3. 02-tue [^1] RC SEP numbers (2575, 2567, 1865, 2663, 2468, 2352) and the 12-month deprecation window.
4. 03-wed [^1][^3] Cloudflare Sept-15 mixed-use default block scope (new customers + new sites + existing free tier) and Search/Agent/Training taxonomy.
5. 03-wed [^4] Firecrawl tier prices and credits-don't-roll-over; [^6] Browserbase proxy $/GB.
6. 03-wed [^7] Playwright v1.61 (2026-06-29) and v1.59 agent-CLI claims.
7. 03-wed [^9] EU AI Act Aug-2 GPAI enforcement + €15M/3% figures; Hamburg natural-language-ToS question.
8. 03-wed [^12] Reddit v. Perplexity co-defendant list (Oxylabs/AWMProxy/SerpApi) and motion-to-dismiss status.
9. 04-thu/03-wed [^so]/[^2] structured-outputs GA model list, ~24h schema cache, citation-block 400 conflict.
10. 05-fri [^3] MIT TR April 16, 2026 URL and framing; [^6] NIST initiative Feb 17, 2026.
11. Code-lab `budget.py` Haiku 4.5 $1/$5 — confirm against the live pricing page before anyone trusts the ceiling.

---

_Review produced 2026-07-17. Six surgical fixes applied (listed above); no git commits made._
