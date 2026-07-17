# Vault SLOP + Repetition Audit — Blocks 0–2 (9 weeks, 63 daily lessons + overviews/reviews, ~430K words)

Audited 2026-07-17. Scope: `vault/block-0-basecamp`, `vault/block-1-problem-solving-outreach`, `vault/block-2-ai-employees`, excluding `_v2*` files and `_week-01-pilot-v1-training-data-only/`.

## Executive summary

**Classic AI slop is nearly absent.** Zero hits vault-wide for: delve, game-changer, "In a world where", "Here's the thing", "The best part", supercharge, elevate, tapestry, "testament to", "buckle up", "Let's dive" (all "dive" hits are the Karpathy video title, "Deep-dive" table labels, or citation titles). One "seamless", one "unleash". "Robust" (40 hits) is almost entirely technical (Sleeper Agents robustness). No hollow section closers ("In short," / "The takeaway?" — 1 hit total). No rhetorical-question padding (2 hits). No empty triads found — every three-item list checked resolves to concrete distinct items ("Agents, innovation, and transformation" ×7 is the real McKinsey report title in citations).

The vault's actual problems are different:
1. **A house-style signature that repeats at scale**: "would push back" ×172, "load-bearing" ×126, "operator/operator-grade" ×650, "actually" ×378, contrast scaffolds (~85). Individually fine; in aggregate they make every lesson sound like the same narrator.
2. **Uniformly high em-dash density** (lesson baseline 9–20 per 1000 words ≈ one em-dash per 60–100 words) with `_review.md` and overview files as extreme outliers (up to 52/1k).
3. **Real cross-week repetition**: the same benchmark numbers, war stories, and paper summaries re-taught (and re-quizzed) in later weeks instead of wikilinked. Wikilink discipline collapsed after Block 0 Week 3 — four weeks have zero wikilinks in lesson files.
4. **Slopsquatting: clean.** Every package, CLI, and product name checked is real or lineage-consistent. Two suspicious version claims web-verified real.

---

## Part 1 — Per-file slop scorecard

Columns: words / em-dash per 1k / contrast-scaffold hits (isn't-just + this-isn't + not-X—it's + not-because-but + the-real-X-is) / "would push back" / "load-bearing". Only daily lessons + notable support files shown; files not listed scored 0–1 on every axis.

| File | Words | Em/1k | Contrast | Push-back | Load-bearing |
|---|---|---|---|---|---|
| B0/W00 01-mon-mental-model-of-llms | 6157 | 15.8 | 2 | 4 | 1 |
| B0/W00 02-tue-ai-native-builder-stack | 7503 | 14.7 | 1 | 2 | 2 |
| B0/W00 03-wed-claude-md-memory-architecture | 6859 | **19.5** | 3 | 3 | 3 |
| B0/W00 07-sun-synthesis | 4461 | **19.7** | 0 | 1 | 0 |
| B0/W01 01-mon-prompting-first-principles | 7214 | 16.2 | 2 | 4 | 2 |
| B0/W01 02-tue-prompt-engineering-in-practice | 7539 | 14.1 | 6 | 3 | 2 |
| B0/W01 03-wed-rag-as-a-system | 8029 | 12.1 | 3 | 5 | 1 |
| B0/W01 06-sat-vibe-coding-part-2-discipline | 7447 | 12.8 | 4 | 4 | 2 |
| B0/W01 07-sun-synthesis | 7278 | **18.8** | 1 | 2 | 1 |
| B0/W02 03-wed-mcp-security | 6431 | 10.9 | 0 | **6** | 2 |
| B0/W03 00-overview | 631 | **31.7** | 0 | 0 | 0 |
| B0/W03 _review | 1379 | **52.2** | 0 | 0 | 1 |
| B0/W03 04-thu-pricing-ai-services | 6020 | 12.5 | 4 | 3 | 2 |
| B0/W03 06-sat-case-study-coding-agent | 6504 | **17.7** | 0 | 3 | 1 |
| B0/W03 07-sun-synthesis | 5807 | **18.3** | 0 | 1 | 0 |
| B1/W01 00-overview | 965 | **24.9** | 0 | 0 | 0 |
| B1/W01 _review | 3103 | **27.4** | 0 | 0 | 5 |
| B1/W01 05-fri-commercial-sow | 8621 | 10.3 | 2 | 3 | **6** |
| B1/W01 06-sat-selling-ai-objections | 8934 | 11.2 | 4 | 4 | 3 |
| B1/W01 07-sun-synthesis | 6748 | **19.0** | 0 | 1 | 1 |
| B1/W02 00-overview | 1030 | **27.2** | 0 | 0 | 0 |
| B1/W02 _review | 3863 | **25.9** | 0 | 1 | **9** |
| B1/W02 01-mon-why-brand-matters | 7856 | 15.5 | 3 | 3 | 2 |
| B1/W02 04-thu-niche-as-a-hypothesis | 7297 | 16.7 | 4 | 4 | 2 |
| B1/W02 05-fri-niche-validation | 7759 | 15.9 | 2 | 3 | **6** |
| B2/W03 02-tue-how-ai-code-gen-tools-work | 7408 | 17.0 | 1 | **6** | 2 |
| B2/W03 03-wed-design-system-literacy | 6940 | **18.2** | 1 | 4 | 1 |
| B2/W03 04-thu-micro-prototype-ladder | 7221 | 16.6 | 2 | **6** | 2 |
| B2/W03 05-fri-prototype-pipeline | 6607 | **20.4** | 0 | **7** | 3 |
| B2/W03 _review | 2919 | **22.3** | 0 | 0 | 3 |
| B2/W04 01-mon-what-a-sales-agent-is | 8676 | 14.1 | 3 | 4 | 3 |
| B2/W04 02-tue-agent-architectures | 7921 | 15.8 | 1 | **6** | 5 |
| B2/W04 05-fri-advanced-rag | 7764 | 14.7 | 1 | **6** | 2 |
| B2/W04 _review | 2548 | **21.6** | 0 | 0 | 5 |
| B2/W05 01-mon-analyst-replacement-thesis | 5114 | 9.6 | 2 | 3 | 1 |
| B2/W05 _review | 2182 | **23.8** | 1 | 0 | 2 |

**Em-dash verdict.** Baseline across all 63 lessons: 9–20 em-dashes per 1000 words — one per paragraph or more, everywhere. It never drops below ~8/1k in any lesson. Outliers to fix first: `B0/W03 _review.md` (52.2/1k), `B0/W03 00-overview.md` (31.7), `B1/W01 _review.md` (27.4), `B1/W02 00-overview.md` (27.2), `B1/W02 _review.md` (25.9), `B1/W01 00-overview.md` (24.9), `B2/W03 05-fri-prototype-pipeline.md` (20.4, highest daily lesson). The overview/review house style leans on em-dash appositives almost every sentence.

**Contrast-scaffold verdict.** ~85 hits total ≈ 1.3 per lesson — low for AI-generated text, and roughly half are substantive (quoted dialogue, real distinctions). The pure-tic instances are listed in the Top-20 below. Worst clusters: `B0/W01 02-tue` (6), `B0/W03 04-thu` (4), `B1/W01 06-sat` (4), `B1/W02 04-thu` (4), `B0/W01 06-sat` (4).

**House-style signature (the real "slop" of this vault).**
- "would push back" — 172 occurrences. Partly mandated by the quality-standard's reviewer-lens section, but it has leaked into body prose; six lessons use it 6–7 times each (`B2/W03 05-fri` ×7; `B2/W03 02-tue`, `B2/W03 04-thu`, `B2/W04 02-tue`, `B2/W04 05-fri`, `B0/W02 03-wed` ×6).
- "load-bearing" — 126 occurrences across 9 weeks (`B1/W02 _review` ×9, `B1/W02 05-fri` ×6, `B1/W01 05-fri` ×6). A distinctive word used ~14×/week stops being distinctive.
- "operator" / "operator-grade" / "operator-ready" — 650 occurrences. Core persona vocabulary, but at ~10 per lesson it is a verbal texture, not a word choice.
- "The honest answer/counter/read" — 23 occurrences.

---

## Part 2 — Cross-week repetition map

Wikilink counts in lesson files per week: B0/W00: 5, B0/W01: 0, B0/W02: 12, B0/W03: 8, B1/W01: 2, B1/W02: 0, B2/W03: 0, B2/W04: 2, B2/W05: 0. Four of nine weeks never link back to prior lessons; repetition below correlates directly with the zero-wikilink weeks.

| Item | Appears in | Verdict per recurrence |
|---|---|---|
| **Anthropic Contextual Retrieval benchmark** (5.7%→3.7%→2.9%→1.9%; 35/49/67% relative) | B0/W01 `03-wed-rag-as-a-system.md` (Part 4, "the methodology in full", full number ladder), B0/W01 `07-sun` (quiz Q7 + A16 + flashcard), B2/W04 `04-thu-rag-fundamentals.md` (Layer 1 "taken seriously", same full ladder + benchmark table), B2/W04 `05-fri` (citation), B2/W04 `07-sun` (quiz Q11 + flashcards 18–19 on the identical 49%/67% numbers) | **Redundant retelling.** W04 adds real value (cost math, Kiela critique, Rerank 3.5 row) but re-teaches and — worse — re-quizzes the exact same numbers already quizzed in W01. The W04 lesson acknowledges "Block 0 Week 1" once in prerequisites, with no wikilink. |
| **MIT NANDA "95% of GenAI pilots fail"** | B0/W00 `03-wed`, B0/W00 `05-fri`, B0/W03 `03-wed-scoping` + `07-sun` quiz, B1/W01 `03-wed` + `04-thu` + `06-sat` + `07-sun` quiz, B2/W03 `02-tue` + `07-sun` quiz | **Redundant.** Used in 8+ files across 4 weeks; B1/W01 uses it in three lessons of the same week (its own `_review.md` notes "same as Wed... consistent across Wed/Thu/Sat"). Only B1/W01 `04-thu` interrogates the figure ("research finding vs marketing artifact") — that treatment should be the single canonical one, linked elsewhere. |
| **Honeycomb Query Assistant** (Phillip Carter, binary judge, >90% agreement in 3 iterations) | B0/W01 `02-tue-prompt-engineering-in-practice.md` (full story + Husain caveat), B0/W01 `06-sat`, B2/W04 `06-sat-rag-evaluation.md` (told twice in the same file: line ~98 summary and line ~128 as "Story 2") | **Redundant retelling** in W04, including intra-file repetition. Same numbers, same arc. No link back to W01. |
| **Simon Willison "lethal trifecta"** | B0/W02 `03-wed-mcp-security.md` (canonical deep treatment — appropriate) + 5 other W02 files; brief callbacks in B0/W00 ×3, B0/W01 ×4, B0/W03 `02-tue` (one sentence — the right way); B2/W05 `03-wed-data-connectivity.md` re-explains the Gmail-MCP attack twice in one file (lines ~90 and ~174, near-identical wording) + `00-overview` + `07-sun` | **W05 is redundant re-teaching** — the same April 2025 Willison Gmail example fully retold twice in one lesson, no wikilink to the W02 security lesson. Block-0 callbacks are acceptable brevity. |
| **MCP launch intro** ("Anthropic released MCP Nov 25 2024, open spec, reference servers...") | B0/W02 `01-mon-mcp-as-a-protocol.md` (canonical), B2/W05 `03-wed-data-connectivity.md` line ~84 (full re-introduction paragraph + same citation) | **Concept re-explanation.** W05 re-teaches MCP-101 to an audience that had a full MCP week; should be one sentence + wikilink. |
| **Karpathy *Deep Dive into LLMs* + "lossy... document simulator" framing** | B0/W00 `01-mon` (quoted 3×) + `07-sun` (flashcard), B0/W01 `01-mon` + `07-sun` (flashcard with same quote) | **Borderline.** Back-to-back weeks assign the same video and flashcard the same quote. W01's re-use adds no new angle. |
| **Anthropic Sleeper Agents paper** | B0/W00 `01-mon` (4 mentions) + `07-sun` quiz, B0/W01 `01-mon` (2) + `07-sun` (6 — quiz + flashcards) | **Borderline-redundant.** Both consecutive Sunday quizzes test the same paper's same findings (persistence through SFT/RLHF, robustness scales with size, CoT makes deception more robust). |
| **Moffatt v. Air Canada (2024 BCCRT 149)** | B0/W00 `01-mon` (exercise P3 + reading + footnote), B0/W03 `02-tue` (teaching case) + `07-sun` + `_review` | **Partially additive.** W03 is the proper teaching home; W00 uses it as an exercise example. Acceptable, but W03 doesn't acknowledge W00 saw it. |
| **Pieter Levels / PhotoAI revenue arc** ($100K/mo Sep 2024; $132–138K MRR 2025) | B1/W02 `02-tue` ("Case 3") and `03-wed` ("Story 2" — same trajectory, same Indie Hackers citations) + `07-sun`; B2/W03 `04-thu` + `05-fri` (different angle: ship-fast/pretotyping) | **Redundant within B1/W02** — two adjacent lessons retell the same revenue story with the same sources. B2/W03 recurrences are additive (different lesson). |
| **METR RCT (developers 19% slower)** | B0/W03 only (`02-tue`, `06-sat`, `_review`, `07-sun`) | **Fine** — contained in one week. |
| **Klarna support-agent saga** | B0/W03 (7 files — its case-study week) + B1/W01 `04-thu` (brief) + B2/W05 `06-sat` (LangGraph-adopters list) | **Fine** — recurrences are brief and additive. |
| **Replit agent DB-deletion incident (SaaStr/Lemkin)** | Full retelling only in B0/W01 `06-sat`. Lemkin reappears in B1/W01 in a different role (SaaStr sales data). | **Fine.** |
| **McKinsey *State of AI 2025*** | B0/W03 ×2 lessons, B1/W01 ×2 lessons (citations/readings) | **Acceptable** — cited, not retold. |
| **Lost-in-the-middle (Liu, TACL 2024)** | B0/W00 `05-fri`, B0/W01 `03-wed` + `04-thu` + `07-sun`, B2/W04 `05-fri` (+RULER context) | **Mostly additive** (each week uses it for a different decision), but W04 re-cites without linking back. |

### Concept re-teach (the structural finding)

**RAG is taught twice at full length.** B0/W01 `03-wed-rag-as-a-system.md` (8,029 words) covers: embeddings vs BM25, hybrid, chunking (fixed/semantic/parent-child), Contextual Retrieval in full, reranking (Cohere/Voyage), context assembly, recall@k/faithfulness evals. B2/W04 then runs a three-day RAG arc — `04-thu-rag-fundamentals.md` (8,521 words: chunking, embeddings/MTEB, hybrid/RRF, reranking, Contextual Retrieval), `05-fri-advanced-rag.md`, `06-sat-rag-evaluation.md` — of which Thursday is ~70% overlap with W01 Wednesday at the topic level. The Thursday file's own prerequisites say "If you have read Block 0 Week 1... you qualify," then re-teach anyway. Advanced-RAG Friday and eval Saturday are largely new (GraphRAG, Self-RAG, RAGAS regression gates) — the fix is to compress Thursday to a delta-from-W01 lesson with wikilinks, not to delete the arc.

**MCP re-taught in miniature** in B2/W05 `03-wed-data-connectivity.md` (launch story, spec, clients, security — all previously a full week in B0/W02, zero wikilinks back).

---

## Part 3 — Slopsquatting sweep

Inventory method: all backticked spans, install/import lines, and versioned product names across the 3 blocks.

**Packages/CLIs — all real:** `@anthropic-ai/claude-code`, `@modelcontextprotocol/server-filesystem`, `n8n-nodes-mcp`, `langchain-mcp-adapters`, `mcp-remote`, `instructor`, `pydantic`, `nltk`, `bubblewrap`, `sandbox-exec`, `pnpm`, `npm ci`, `claude mcp add`, `git reflog` / `reset --keep` etc., Anthropic beta headers `code-execution-2025-08-25` and `structured-outputs-2025-11-13`, `claude-sonnet-4-6` model id, `gpt-realtime`, `v0-1.0-md`, Unstructured `hi_res`, LangGraph, Pydantic AI 1.0, RAGAS, MTEB, RULER, Pinecone/Qdrant/Weaviate/Supabase Vector/PGVector, PostHog/Clarity/Hotjar, LiveKit/ElevenLabs v3, WebContainer (Bolt), Figma Make, Vercel v0.

**Web-verified (2 checks used; budget then exhausted):**
- **Cohere Rerank 4** — REAL. Released Dec 11, 2025 (rerank-4-pro / rerank-4-fast, 32K context). Note an internal inconsistency, not a fabrication: B0/W01 `03-wed` names "Cohere Rerank 4" while B2/W04 `04-thu`'s benchmark table uses "Cohere Rerank 3.5" — both real models, but the two RAG lessons disagree on the current flagship.
- **GPT-5.3-Codex** — REAL (openai.com/index/introducing-gpt-5-3-codex; follows GPT-5.2-Codex).

**Lineage-consistent, unverified (post-Jan-2026 versions; no red flags):** Claude Opus 4.6/4.7, Claude Sonnet 4.6 (consistent with Opus 4.5/Sonnet 4.5 lineage and with this repo's own CLAUDE.md), Gemini 3.1 (Gemini 3 shipped Nov 2025), Replit Agent 4 (Agent 3 was Sep 2025), Claude Code v2.1, Cursor 2.0 + Composer (real, Oct 2025), Devin 2.0 (real, Apr 2025), jina-embeddings-v3 (real), Voyage rerank-2/rerank-2-lite (real), Tailwind v4 (real), MIT NANDA report (real, Aug 2025), Contextual AI "RAG 2.0" (real term), Unbounce Conversion Benchmark Report (real).

**Fabrication verdict: nothing flagged.** The vault's own hygiene helps — e.g., the 67k-token MCP anecdote in B0/W02 explicitly labels itself "composite social-media anecdote; treat the attribution as such."

---

## Ranked worst-offending passages vault-wide

An honest note: after filtering false positives, the vault does not contain 20 genuinely slop-afflicted passages of the classic kind. Ranked below are the 15 worst real offenders, ordered by fix-priority (structural repetition first, then verbal tics).

1. **B2/W04 `04-thu-rag-fundamentals.md`** Layer 1 — full re-teach of the Contextual Retrieval number ladder already taught in B0/W01 `03-wed`: "Let's open with the number everybody cites and read it carefully. Anthropic..." (5.7→2.9→1.9%, 35/49/67%). Biggest single redundancy in the vault.
2. **B2/W04 `07-sun`** quiz Q11 + flashcards 18–19 — re-quizzes "Contextual Retrieval headline number? → 49%... with rerank? → 67%", identical to B0/W01 `07-sun` Q7/A16/flashcard. Same student, same numbers, two graded weeks apart.
3. **B2/W05 `03-wed-data-connectivity.md`** lines ~90 and ~174 — the Willison Gmail-MCP "lethal trifecta" attack explained twice in the same lesson, and a third time in the week's overview + Sunday, all without a wikilink to B0/W02 `03-wed-mcp-security.md`.
4. **B2/W05 `03-wed-data-connectivity.md`** line ~84 — MCP re-introduced from scratch ("Anthropic released the Model Context Protocol on November 25, 2024, as an open specification...") one block after MCP week.
5. **B1/W01** MIT NANDA 95% in three lessons of one week (`03-wed`, `04-thu`, `06-sat`) plus the quiz — the week's own `_review.md` flags it ("same as Wed").
6. **B2/W04 `06-sat-rag-evaluation.md`** — Honeycomb ">90% judge-human agreement in three iterations" told at line ~98 and again at ~128 as "Story 2", a full retelling of B0/W01 `02-tue`'s centerpiece case.
7. **B1/W02 `02-tue` "Case 3" + `03-wed` "Story 2"** — Pieter Levels' PhotoAI $0→$132K MRR arc retold in adjacent lessons with the same two Indie Hackers citations.
8. **B0/W03 `_review.md`** — 52.2 em-dashes per 1000 words, the densest file in the vault; nearly every sentence contains an em-dash appositive.
9. **B0/W03 `00-overview.md`** (31.7/1k) and **B1/W01/W02 overviews + reviews** (24.9–27.4/1k) — the overview/review template's em-dash-appositive house style.
10. **B2/W03 `05-fri-prototype-pipeline.md`** — "would push back" ×7 in one lesson (plus 20.4 em/1k, highest of any daily lesson); the reviewer-lens verb has become the lesson's only way to introduce disagreement.
11. **B1/W02 `_review.md`** — "load-bearing" ×9 in a 3,863-word file; also 25.9 em/1k.
12. **B0/W01 `07-sun`** line ~450 — "analysis is not overhead — it's the product": pure contrast-scaffold tic in a synthesis summary.
13. **B0/W02 `06-sat`** line ~79 — "The biggest quality lift you can give a legacy ReAct agent today is not a better model — it's a better `observation` formatter" — the not-X-it's-Y scaffold carrying a real point, but the same syntactic move appears twice more in the same week (`_review` line ~172: "Not because it's bad — it's the most usable decision...").
14. **B0/W03 `04-thu-pricing-ai-services.md`** lines ~178 and ~301 — two not-X-it's-Y scaffolds in one lesson ("is not 'usage-based is bad' — it's that...", "not to hold the outcome price fixed — it's to...") on top of a "The real question..." opener.
15. **B0/W01 `01-mon` + `07-sun` vs B0/W00 `01-mon` + `07-sun`** — Karpathy "lossy, frozen, probabilistic document simulator" quote and Sleeper Agents findings assigned, taught, and flashcarded in both consecutive weeks with no delta.

### Recommended fixes (in priority order)
1. Rewrite B2/W04 `04-thu` as a delta lesson: keep cost math, Kiela critique, MTEB/RRF material; replace the re-taught ladder with a wikilink to B0/W01 `03-wed`. Purge duplicate quiz items from B2/W04 `07-sun`.
2. In B2/W05 `03-wed`, collapse both trifecta retellings and the MCP intro to one sentence each + wikilinks to B0/W02.
3. Declare one canonical home for MIT NANDA 95% (B1/W01 `04-thu`, which actually interrogates it) and reference it elsewhere.
4. De-duplicate PhotoAI (B1/W02) and Honeycomb (B2/W04 `06-sat` internal).
5. Style pass on `_review.md`/overview templates: halve em-dashes; cap "load-bearing" and "would push back" at ~2 per file; vary the reviewer-lens verb.
6. Restore wikilink discipline in the four zero-wikilink weeks (B0/W01, B1/W02, B2/W03, B2/W05).
