---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 7
day_name: sun
session_slug: advanced-rags
date_due: 2026-06-28
tags: [synthesis, quiz, flashcards, context-engineering, advanced-rag, capstone]
sources:
  - anthropic-effective-context-engineering-2025
  - chroma-context-rot-2025
  - anthropic-multi-agent-research-2025
  - simonwillison-memory-dossier-2025
  - microsoft-lazygraphrag-2024
  - cherny-latent-space-2025
last_verified: 2026-07-17
word_count_target: 4000
---

# Week 6 Synthesis — from prompt-writer to context architect

## The one-sentence thesis of this week

Every capability this week — memory, compaction, hybrid retrieval, rerankers, graphs, SQL, agentic loops — is a different answer to one budgeting question, *which tokens deserve the window for this step*, and the only trustworthy referee for any answer is an ablation you pre-registered and ran on your own corpus.

## The unifying frame: one budget, seven days

**Monday** named the discipline and its constraint. Context engineering is curating and maintaining the optimal token set at inference time (Anthropic's definition; Karpathy's "delicate art and science" framing[^1]), and the constraint is real: attention degrades with length in measured, non-uniform ways (Chroma's context rot, 18 models[^2]), and effective context lands far below advertised context on every model tested (NoLiMa's ≥85%-of-base-score definition; RULER's task-category finding that aggregation dies before retrieval does). The 1M-token era changes prices and options; it repeals nothing.

**Tuesday** managed the budget across time with four primitives — compaction (lossy, needs a loss-function you chose on purpose), structured notes (agent-curated durable state), sub-agent isolation (fresh windows bought with money: 90.2% better research at ~15× tokens[^3]), and cross-session memory (retrieval plus write-policy, wearing marketing). The controversy that organizes the vendor landscape: memory as moat vs memory as contamination, with Willison's dossier critique — control, staleness, context collapse — as the engineering case for legible, scoped, erasable memory.[^4]

**Wednesday** spent the budget well: five retrieval families (lexical, dense, late-interaction, structural, rerankers), a reranker market with new leaders worth re-checking per project, LazyGraphRAG collapsing GraphRAG's cost story (0.1% indexing cost, 700× cheaper global queries[^5]) without collapsing the triage — graphs only for genuinely structural questions — and text-to-SQL's benchmark-to-production cliff proving that the system around the model outscores the model.

**Thursday** put the model in charge of the loop: query planning, iterative reformulation, sufficiency judgment, grounded citation. The existence proof (Claude Code firing its vector database for grep-based agentic search[^6]) and the generalization evidence (agentic keyword search ≈94.5% of RAG faithfulness) both come with a vocabulary-structure caveat, and the whole pattern comes with an invoice — 3–10× tokens, 2–5× latency — that makes *tiered* the shippable default: fast lane for everything, escalation trigger, capped agentic lane.

**Friday** built the referee: the four-metric panel read jointly, the answerability slice most harnesses are missing, your own operating-budget probe instead of leaderboard trust, and ablation method — frozen baseline, one dial at a time, deletion rows, pre-registered gates, validated judge.

**Saturday** ran it. The deliverable was never the v2 pipeline; it was the evidence table that says which upgrades earned their complexity on your corpus, and the discipline to no-ship the ones that didn't.

## The operator's decision table

| Situation | Move | Why (day) |
|---|---|---|
| Agent degrades late in long runs | Audit window; clear stale tool results first | Tool results decay fastest (Tue) |
| "Just use the 1M window" | Probe your effective budget on your task shape | Advertised ≠ effective (Mon, Fri) |
| Right doc at rank 14 | Add a reranker over hybrid top-50 | Highest-leverage single addition (Wed) |
| "We need GraphRAG" | Two-question triage against logged queries | Most reaching for it shouldn't (Wed) |
| Data is tabular | SQL retrieval over a curated semantic layer | Stop embedding arithmetic (Wed) |
| Hard multi-hop queries, budget exists | Tiered agentic fallback, hard caps | Loop earns 3–10× only on hard lane (Thu) |
| Vendor cites +39% / 90.2% / 94.5% | Decompose: task, harness, judge, budget | Numbers transfer only as far as those match (Fri) |
| Five upgrades proposed | One dial per run; deletion rows too | Bundles destroy attribution (Fri, Sat) |
| Memory feature request | Scoped, inspectable, dated, erasable — or no | Contamination is the default (Tue) |

## Quiz — 15 questions

Mixed format. Closed book, per the [[00-program/how-to-study|study protocol]]. Answers below; no items duplicate the Week-4 quiz (which owns RAGAS mechanics and judge-bias questions).

**Q1 (MCQ).** Anthropic's definition of context engineering differs from prompt engineering primarily in that it: (a) requires longer prompts; (b) covers curating *all* tokens in the window across inference, not just instructions; (c) applies only to agents; (d) replaces retrieval with long context.

**Q2 (short).** NoLiMa defines a model's "effective length." State the definition and the design choice that makes NoLiMa harder than classic needle-in-a-haystack.

**Q3 (MCQ).** Chroma's context-rot report found: (a) only small models degrade with length; (b) degradation is uniform and predictable; (c) all 18 tested models degrade, non-uniformly, affected by distractors and haystack structure; (d) degradation disappears above 200K tokens.

**Q4 (short).** Your agent's window is dominated by tool results from 40 turns ago. Name the cheapest remediation from the compaction pipeline and why it targets tool results specifically.

**Q5 (MCQ).** Anthropic's memory tool stores data: (a) on Anthropic's servers, encrypted; (b) in the model's weights; (c) client-side, as files your application persists; (d) in a managed vector database.

**Q6 (short).** Give Willison's three engineering objections to dossier-style memory, and the one design property that answers most of them.

**Q7 (calc).** A tiered system serves 10K queries/day. The fast lane costs $0.018/query; the agentic lane $0.11. The escalation trigger promotes 15% of traffic, but a third of promotions are false (fast lane would have sufficed). What does the false-promotion leak cost per 30-day month, and what's the first lever you'd pull?

**Q8 (MCQ).** Sub-agent context isolation is a poor fit when: (a) the task is breadth-first research; (b) sub-tasks are independent; (c) workers need fine-grained shared state, e.g. debugging; (d) the corpus is multilingual.

**Q9 (short).** LazyGraphRAG cut GraphRAG's indexing cost to ~0.1% of the original. What did it move out of indexing, and where did that work go?

**Q10 (short).** Why does late interaction (ColBERT-family MaxSim) beat single-vector dense retrieval on identifier-heavy queries? One mechanistic sentence.

**Q11 (MCQ).** The enterprise text-to-SQL finding — ~33% bare model vs ~75% with a grounding/clarification system on the same schema — primarily teaches: (a) SQL generation is solved; (b) benchmarks understate models; (c) past a capability floor, the surrounding system determines production accuracy; (d) BIRD is obsolete.

**Q12 (short).** Claude Code dropped its vector index for agentic grep search. Name the corpus property that made that the right call for code, and a corpus where the same move would collapse recall.

**Q13 (MCQ).** Your ablation shows +2.1 mean correctness for the agentic lane with a ±4-point spread across repeats. Correct reading: (a) ship it; (b) no signal — the effect is inside noise; (c) increase temperature; (d) the judge is broken.

**Q14 (short).** What is an answerability slice, why must it be hand-labeled, and why does every upgrade from this week make it *more* necessary?

**Q15 (essay, 150 words).** A client says: "Fable-class models have 1M-token windows now — rip out the retrieval stack and stuff everything." Using at least three named results from this week, write the reply that neither surrenders nor strawmans the client.

### Answer key

**A1.** (b).

**A2.** Longest context at which the model retains ≥85% of its own short-context base score; NoLiMa minimizes lexical overlap between question and needle, forcing latent association instead of literal matching.

**A3.** (c).

**A4.** Microcompact-style clearing: replace old tool-result *content* with a cleared marker, keeping call structure. Tool results are recomputable (re-read the file if needed) and decay fastest, so clearing them loses the least information per token freed.

**A5.** (c).

**A6.** Loss of context control (hidden state → unpredictable behavior), staleness with no invalidation, and context collapse across life/work spheres. Legibility — memory as inspectable, editable, scoped artifacts — addresses all three.

**A7.** Promotions/day = 1,500; false = 500. Waste per false promotion ≈ $0.11 − $0.018 = $0.092 → ≈ $46/day ≈ **$1,380/month**. First lever: tighten the trigger's precision (it's a classifier — evaluate it like one), before touching caps or lane quality.

**A8.** (c).

**A9.** All LLM work (entity extraction, community pre-summarization) left indexing; the graph is built with NLP noun-phrase co-occurrence, and LLM effort is deferred to query time, spent lazily only on queries that arrive.

**A10.** MaxSim scores each query token against its best-matching document *token*, so a single discriminating identifier can dominate the score instead of being averaged away in one pooled chunk vector.

**A11.** (c).

**A12.** Code's vocabulary is exact and lexically greppable (identifiers, conventions), and live filesystem state beats snapshots. A paraphrase-heavy corpus (support tickets, contracts) breaks the assumption — user words don't match document words, which is what dense retrieval exists for.

**A13.** (b). Margins inside the repeat spread are noise; the Week-4 rule (<5-point pairwise margins = no signal) applies to your own harness too.

**A14.** A regression-set slice of queries whose answers are *not in the corpus*, scored on whether the system declines; hand-labeled because "not answerable" is a claim about the corpus a judge can't infer from an answer. Every upgrade this week (bigger windows, memory, agentic loops) increases the system's power to produce a confident answer, so the ability to decline erodes silently unless measured.

**A15.** Strong answers concede the real capability (1M windows exist and have deliberate uses — big single-shot analyses), then cite: context rot / NoLiMa-RULER (effective ≪ advertised; accuracy falls with stuffing), the cost-latency record (retrieval orders of magnitude cheaper and faster per query at volume; 8–25s TTFT on 500K-token prompts), and the 2026 hybrid consensus (retrieve tens of thousands of relevant tokens, reason with a long-window model), ideally offering the ablation harness as the arbiter: "we'll run your stuffed-window lane against retrieval on your queries and ship the winner."

## Flashcards — 30 cards

Format: Q → A. Import into Anki as-is. No overlap with Week-4's deck (RAGAS mechanics, judge biases).

1. Context engineering (Anthropic's definition)? → Strategies for curating and maintaining the optimal set of tokens in the window during inference — everything, not just instructions.
2. Karpathy's context-engineering phrase? → "The delicate art and science of filling the context window with just the right information for the next step."
3. Context rot? → Measured degradation of LLM performance as input length grows; non-uniform; all 18 models in Chroma's study affected.
4. NoLiMa's effective length? → Longest context retaining ≥85% of the model's short-context base score.
5. NoLiMa's key design choice? → Minimal lexical overlap between question and needle — forces latent association.
6. RULER's four task categories? → Retrieval, multi-hop tracing, aggregation, question answering.
7. Which RULER categories degrade first? → Aggregation and multi-hop tracing, long before simple retrieval.
8. Attention budget? → The finite usable attention a model has; every added token depletes it (Anthropic's framing of why rot happens).
9. System-prompt altitude? → The Goldilocks zone between hardcoded if-else logic and vague exhortation: specific heuristics, judgment left to the model.
10. Why are tool definitions a context tax? → Every registered schema is resident in every call; MCP-heavy setups can spend tens of thousands of tokens before the conversation starts.
11. Just-in-time context? → Keep lightweight identifiers (paths, queries) in the window; load content via tools at the moment of need.
12. The four survive-past-the-window primitives? → Compaction, structured note-taking, sub-agent isolation, cross-session memory.
13. Why clear old tool results first? → Recomputable and fastest-decaying: least information lost per token freed.
14. Claude Code compaction stages? → Snip → microcompact → context collapse → autocompact (escalating, LLM-last).
15. Anthropic context-editing headline numbers? → +39% agentic search (with memory tool), +29% editing alone, 84% token reduction on the 100-turn eval — internal evals.
16. Anthropic memory tool architecture? → Client-side file operations (CRUD) against a memory directory your app stores; persists across conversations.
17. Multi-agent research system numbers? → +90.2% over single-agent on internal eval; ~15× chat tokens; token spend explained ~80% of BrowseComp variance.
18. When do sub-agents fit poorly? → Tightly-coupled shared-state tasks (coding, debugging); coordination eats the isolation gains.
19. Willison's three memory objections? → Loss of context control, staleness without invalidation, context collapse across spheres.
20. Memory design rules for client work? → Scoped per client, inspectable, dated/invalidatable, erasable on request.
21. The five retrieval families? → Lexical, dense single-vector, late-interaction/multi-vector, structural (graph/SQL), rerankers (second stage).
22. Mid-2026 reranker top tier? → zerank-2 and Cohere Rerank v4.0 Pro at the top of the Agentset ELO board; Voyage rerank-2.5 and jina-reranker-v3 (latency pick) close behind; re-check per project.
23. zerank-2 license catch? → Open weights are CC-BY-NC — commercial use needs a paid contract.
24. MaxSim (late interaction)? → Each query token takes its best-matching document token embedding; sum the maxima. Token-level precision with precomputable documents.
25. PLAID's contribution? → Made ColBERT-class serving practical: centroid interaction + pruning, up to 7× GPU / 45× CPU faster search.
26. LazyGraphRAG's trick? → No LLM at indexing (noun-phrase co-occurrence graph); LLM effort deferred to query time — ~0.1% indexing cost, ~700× cheaper global queries.
27. GraphRAG triage (two questions)? → Do logged queries genuinely require relationship joins across documents? Has hybrid+rerank been *proven* to fail them?
28. Agentic RAG cost multipliers? → Roughly 3–10× tokens, 2–5× latency vs one-pass; earned on multi-hop/ambiguous/high-stakes only.
29. Tiered retrieval architecture? → Single-shot default; measured escalation trigger; capped agentic lane; cost mix becomes a business lever.
30. The Friday decomposition of any vendor eval number? → Task distribution × harness × judge × budget; it transfers only as far as those four match yours.

## Open questions — what's not settled this week

- **Sufficiency judgment.** No current model reliably knows when its evidence is complete; every production loop is bounded by dumb caps. Whether RL-trained search policies (Search-R1 lineage) fix this or just move the failure is open.
- **Where context management lives.** Platform features (context editing, memory APIs) are eating the hand-rolled versions this week taught. The mechanics knowledge stays valuable; the code may not. Watch which of Saturday's lanes the platform obsoletes first.
- **Long-context training vs retrieval investment.** If effective-context curves keep improving (they have, slowly), the knee of your operating budget moves annually, and with it every triage in this week. Re-probe per model generation.
- **Memory benchmarks.** LoCoMo-class evals are small and vendor-adjacent; the space has no MMLU yet. Treat all memory leaderboards as directional until an independent benchmark lands.

## Capstone — 30 days, one context-engineered system with receipts

Ship one of these within 30 days, solo or for a client:

1. **The upgrade with evidence** (default): take Saturday's v2 and its ablation report to production behind the tiered architecture, add the monitoring twin (per-lane panel metrics on live traffic, weekly), and after 30 days write the one-page "what production disagreed with the ablation about" memo. That memo is your strongest sales artifact for the next engagement.
2. **The context audit** (services move): productize Monday's audit + Friday's probe as a fixed-fee engagement — "we measure your agent's real context budget and cut your token bill" — with the deletion-row ablation as the deliverable. Anthropic's 84%-reduction result is the reference point that makes the pitch credible; your client's own table is what makes it true.
3. **The mini deep-research agent** (stretch): Thursday's loop over a client's private corpus with Tuesday's notes and Saturday's caps, evaluated on a 30-query gold set with an answerability slice. Do not attempt the multi-agent version until the single-agent version's evals plateau.

Whichever you pick: pre-register the success gate today, before the work starts. That habit is the week, compressed to a sentence.

## Citations

[^1]: Anthropic Engineering, *Effective context engineering for AI agents* (Sep 29, 2025), https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents ; Karpathy, https://x.com/karpathy/status/1937902205765607626 (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^2]: Chroma Research, *Context Rot* (Jul 2025), https://www.trychroma.com/research/context-rot (search-verified 2026-07-17)

[^3]: Anthropic Engineering, *How we built our multi-agent research system* (Jun 2025), https://www.anthropic.com/engineering/multi-agent-research-system (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^4]: Simon Willison, *I really don't like ChatGPT's new memory dossier* (May 21, 2025), https://simonwillison.net/2025/May/21/chatgpt-new-memory/ (search-verified 2026-07-17)

[^5]: Microsoft Research, *LazyGraphRAG sets a new standard for quality and cost* (Nov 2024), https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^6]: Boris Cherny / Latent Space (May 2025) via https://zerofilter.medium.com/why-claude-code-is-special-for-not-doing-rag-vector-search-agent-search-tool-calling-versus-41b9a6c0f4d9 and https://smartscope.blog/en/ai-development/practices/rag-debate-agentic-search-code-exploration/ (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
