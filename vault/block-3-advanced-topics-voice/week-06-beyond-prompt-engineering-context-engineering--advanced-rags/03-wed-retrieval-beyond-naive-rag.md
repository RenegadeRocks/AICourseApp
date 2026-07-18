---
type: lesson
block: block-3-advanced-topics-voice
week: week-06
day_of_cycle: 3
day_name: wed
session_slug: beyond-prompt-engineering-context-engineering
date_due: 2026-06-24
tags: [retrieval, hybrid-search, rerankers, late-interaction, colbert, multi-vector, graphrag, lazygraphrag, text-to-sql, structured-retrieval, zerank, cohere-rerank, voyage, jina]
sources:
  - agentset-reranker-leaderboard-2026
  - zeroentropy-reranker-guide
  - jina-colbert-v2-arxiv
  - plaid-engine-paper
  - microsoft-lazygraphrag-2024
  - graphrag-2026-verdicts
  - bird-benchmark-2026
  - datost-text-to-sql-2026
  - anthropic-contextual-retrieval-2024
last_verified: 2026-07-17
word_count_target: 5500
---

# Retrieval beyond naive RAG — hybrid, rerankers, late interaction, graphs, and SQL

## Why this matters

Your Week-4 build already runs the 2025 default stack: chunking, embeddings, hybrid BM25+dense with reciprocal rank fusion, a reranker, and Contextual Retrieval preprocessing. Today is the map of everything past that default, because "advanced RAG" is where clients actually have money: the deployments that fail are rarely failing at the embedding step, they are failing because someone shipped cosine similarity against a problem that needed a reranker, a graph, or a SQL query. By tonight you can look at a retrieval problem and name, with reasons, which of five architecture families it belongs to — and, just as commercially important, recognize when a consultant is pitching GraphRAG at a problem a $200/month managed index would solve. The frame from Monday holds: retrieval is context engineering's supply chain. Every architecture below is just a different answer to "which 2,000 tokens deserve the window?"

## Prerequisites

- [[04-thu-rag-fundamentals|RAG fundamentals]] (Block 2 Week 4): chunking, embeddings, hybrid BM25+dense+RRF, cross-encoder reranking. Assumed cold.
- The Contextual Retrieval ladder (the 5.7%→2.9%→1.9% failure-rate numbers) lives in [[03-wed-rag-as-a-system|Block 0 Week 1]] and is not re-taught. One line: prepend chunk-situating context before embedding, stack with BM25 and reranking, and top-20 retrieval failures drop by up to 67%.[^9]
- [[05-fri-advanced-rag|Advanced RAG]] (Block 2 Week 4) introduced GraphRAG and agentic retrieval at survey level; today deepens the retrieval-architecture half, tomorrow the agentic half.

## Layer 1 — The five-family map

Every production retrieval system in 2026 is assembled from five families. Name them before tuning anything:

1. **Lexical.** BM25-class term matching. Exact identifiers, error codes, names, legal citations.
2. **Dense single-vector.** Embeddings + ANN search. Paraphrase and semantic similarity.
3. **Late-interaction / multi-vector.** Token-level embeddings scored at query time (ColBERT family). Precision closer to a cross-encoder at retrieval-scale cost.
4. **Structural.** Knowledge graphs (GraphRAG family) for relationship and corpus-global questions; SQL/text-to-SQL for tabular facts.
5. **Rerankers.** Cross-encoders applied to a candidate set from any of the above. Not a retriever; a second-stage referee.

The 2026 consensus architecture is boring and correct: **hybrid first stage (lexical + dense), reranker second stage, structural retrieval only where the question shape demands it, all increasingly orchestrated by an agent** (tomorrow's lesson).[^6] What changed since your Week-4 build is not the shape but the components: the reranker market has new leaders, late interaction became genuinely deployable, and GraphRAG got both radically cheaper and more honestly scoped.

## Layer 2 — Rerankers in mid-2026: the leaderboard moved

The reranker's job is unchanged: take the top 50–100 candidates from a cheap first stage, score each query–document pair with a model that attends to both jointly, return a sharpened top-k. What changed is who wins. As of this month, on Agentset's public reranker leaderboard (ELO-style, across domains), the top tier is: **ZeroEntropy's zerank-2** (~1638 ELO), **Cohere Rerank v4.0 Pro** (~1629), with **Voyage rerank-2.5** and **jina-reranker-v3** close behind; Jina's v3 is the latency pick (sub-200ms class), Voyage and Cohere sit around ~600ms in the same tests.[^1][^2]

Selection heuristics that survive contact with procurement:

- **Default commercial pick:** Cohere Rerank 4 Pro. Managed, multilingual, boring in the good way.[^2]
- **Latency-critical (voice agents next week!):** jina-reranker-v3.[^1]
- **Highest measured quality:** zerank-2, but read the license: the open weights are CC-BY-NC, so commercial use means a paid contract.[^1][^2]
- **Already on Voyage embeddings / MongoDB Atlas:** rerank-2.5 keeps one vendor surface.[^2]

Two disciplines matter more than the pick. First, *rerankers are the highest-leverage single addition* to a mediocre pipeline — they fix the "right document at rank 14" disease that hybrid first stages produce, and Anthropic's own Contextual Retrieval numbers already showed reranking supplying the last big drop in failure rate.[^9] Second, *leaderboard ELO is not your corpus*. The spread between the top four is small enough that your Saturday ablation, on your documents, is the only ranking that matters. Vendor-published win rates in this market have the same epistemics as mattress reviews.

## Layer 3 — Late interaction: the ColBERT family grows up

Single-vector retrieval compresses a whole chunk into one embedding: cheap, and lossy exactly when queries hinge on one token. Cross-encoders attend over the full query–document pair: accurate, and unusable as a first stage. **Late interaction** is the negotiated middle: embed every token of every document offline, embed the query's tokens at search time, score via MaxSim (each query token takes its best-matching document token; sum). You keep per-token precision while documents remain pre-computable.[^3]

Why this stopped being a research toy: the **PLAID** engine cut ColBERTv2 search latency by up to 7× on GPU and 45× on CPU via centroid interaction and pruning, making multi-vector serving operationally plausible;[^4] and **Jina-ColBERT-v2** (arXiv 2408.16672) delivered a production-grade open model: 89 languages, 8K-token length, Matryoshka-style controllable output dimensions to cut storage, and ~6.5% improvement over original ColBERTv2 on English BEIR (0.521 avg across 14 tasks).[^3] Qdrant, Vespa, and LanceDB all ship native multi-vector support, so the storage story (the historical objection: token-level vectors cost an order of magnitude more space) is now a tunable dial rather than a dealbreaker.

Where it earns its place: corpora where the query's discriminating signal is token-scale — code identifiers, part numbers, legal cites, biomedical entities — and where you want reranker-class precision *inside* the first stage instead of after it. Where it doesn't: small corpora (a reranker over hybrid top-50 gets you there cheaper) and teams without the ops appetite for a second index format. Honest sizing: most readers of this course should *know* this family and deploy it rarely; it is the right tool perhaps one engagement in ten, and the interview-question version ("why does MaxSim beat pooled cosine on identifier-heavy queries?") pays off more often than the deployment.

## Layer 4 — GraphRAG: the 2026 verdict

GraphRAG's pitch: extract entities and relations into a knowledge graph, cluster into communities, pre-summarize communities, and answer *corpus-global* questions ("what are the main themes across these 10,000 filings?" "how are these twelve counterparties connected?") that chunk retrieval structurally cannot see. Your Week-4 lesson introduced the mechanism; here is what eighteen months of production reality did to it.

**The cost story collapsed, in a good way.** Original 2024-era GraphRAG indexing was notoriously expensive (the community's shorthand horror story: five figures to index a large corpus). Microsoft's **LazyGraphRAG** (announced November 2024, since folded into the open-source GraphRAG line) deferred all LLM work out of indexing — NLP noun-phrase co-occurrence builds the graph; the LLM is spent lazily at query time — achieving answer quality comparable to GraphRAG global search at **0.1% of its indexing cost**, and comparable global-query quality at 700× lower query cost than full global search.[^5] The "$33,000 became $33" arc that practitioner write-ups describe is directionally real even if you should treat any single retelling's numbers as illustrative.[^6]

**The verdict, from people running it:** even at the new prices, graph-based RAG still costs multiples of vanilla RAG to operate (practitioner guides put it at roughly 6–8× to index and ~3× to run, stack-dependent), and the mid-2026 consensus among production writers is blunt: GraphRAG is the buzzword of the year and most teams reaching for it shouldn't — it wins when the problem is *genuinely structural* (multi-hop relationship queries, corpus-global synthesis, high-stakes cross-document reasoning in legal/financial/medical work) and loses everywhere a FAQ bot or single-fact lookup lives.[^6] The two-question triage that does most of the work: (1) Do your real user queries require joining facts across documents via named relationships? (2) Have you *proven* that hybrid+rerank fails them? A "no" on either means no graph. Run the triage against logged queries, not imagined ones; a week of production logs usually shows the multi-hop share is under 10%, and an agentic loop (tomorrow) often covers that residue by chaining ordinary retrievals.

## Layer 5 — Structured retrieval: when the answer is a row, stop embedding it

The most under-taught retrieval upgrade costs no new infrastructure: route questions about structured data to structured queries. Embedding a revenue table into prose chunks so a vector search can approximately rediscover arithmetic is a category error you already learned to avoid in the [[06-sat-build-the-weekly-report-generator|Week-5 build]] (verify numbers in code, never in prose). The retrieval-side corollary: **text-to-SQL is a retrieval architecture**, and its 2026 numbers deserve sober reading.

On **BIRD** — the benchmark that made text-to-SQL honest by using large, messy, real databases — the best 2026 pipelines reach the low 80s in execution accuracy (the leaderboard's top entries sit around 81–82%), against a human-expert reference of ~92–93%.[^7] But the number that should shape your architecture comes from the enterprise gap literature: vendors promise 85–90%, while *raw* model performance on real production schemas — hundreds of tables, cryptic column names, undocumented business logic — has been measured as low as the 10–31% range, and one documented system comparison shows the same frontier model scoring ~33% bare versus 75.2% wrapped in a grounding-and-clarification system.[^8] The lesson generalizes past SQL and is arguably the thesis of this whole week: **past a capability floor, the system around the model determines production accuracy more than the model does.** For your builds: text-to-SQL over a curated semantic layer (documented views, business definitions, few-shot query examples per table) is shippable; text-to-SQL straight at a raw warehouse is a demo.

Routing between families is itself the design act. The router can be rules (identifiers→lexical-heavy hybrid; aggregates→SQL; relationship phrasing→graph), a cheap classifier, or the agent itself deciding per query, which is precisely tomorrow's subject.

## Worked example / runnable experiment — reranker ablation on your corpus

Claude Code orchestration, 60–90 minutes, using your Week-4 corpus and regression set. (Long code belongs in Saturday's `code-lab/6/`; today's experiment needs none.)

**Phase 1 — establish the candidate gap.** Paste into Claude Code:

> Using my Week-4 retrieval pipeline and its regression set, run each query and record hit-rate@5 and hit-rate@20 for the hybrid first stage. Output a table plus the list of queries where the gold chunk lands in ranks 6–20.

That ranks-6–20 list is the reranker's addressable market. If it's empty, a reranker cannot help you (rare, and worth knowing in ten minutes instead of after an integration).

**Phase 2 — add one reranker.** Have Claude Code wire *one* API reranker (Cohere Rerank 4 Pro or Voyage rerank-2.5, whichever key you have; document the choice) over the hybrid top-50, then re-run: hit-rate@5 before/after, added latency per query, added cost per 1,000 queries at list prices.

**Phase 3 — decide like an operator.** One paragraph: given the measured lift, latency, and cost, does the reranker ship in Saturday's v2? A 2-point lift at 600ms may be wrong for a voice agent and right for a legal research tool. Write the sentence you'd say to a client to justify the line item.

**Phase 4 (optional) — graph triage.** Run the Layer-4 two-question triage against your actual regression queries and last week's real usage. Count the genuinely multi-hop queries. Most readers will find the count near zero, and that finding is the deliverable.

## Operator case studies — three corpora, three different right answers

**Case 1 — internal engineering wiki, ~3,000 pages.** Queries are vocabulary-aligned with documents (engineers wrote both). Hybrid first stage already put gold chunks in the top 10 for 92% of the regression set; the reranker's addressable market (ranks 6–20) was 11% of queries. Adding Cohere rerank lifted hit-rate@5 by 6 points for ~450ms and a per-query fee, and the team shipped it because their consumers were agents (Thursday's loop) whose downstream cost scales with retrieved-context size: concentrating relevance into 5 chunks instead of 10 paid for the reranker twice over in generation tokens. The lesson: reranker ROI often lives in the *window savings*, not the accuracy line.

**Case 2 — regulatory filings, cross-entity questions.** A financial-research team with genuine multi-hop traffic ("which portfolio companies share directors with the acquirer?") ran the triage honestly: 23% of logged queries required relationship joins, and hybrid+rerank demonstrably failed them. They deployed LazyGraphRAG-style indexing for the entity layer while keeping vanilla hybrid for the other 77%, routed by a cheap classifier. Cost multiple over vanilla: roughly 2× blended, not the 6–8× of a full-graph-everything build.[^6] The lesson: GraphRAG as a *lane*, never as the architecture.

**Case 3 — SaaS analytics assistant.** Users asked aggregate questions ("MRR by segment last quarter") at a corpus of dashboards and docs. The team spent six weeks tuning embeddings before admitting the answers lived in the warehouse. Text-to-SQL over a curated semantic layer (34 documented views, few-shot examples per view) took accuracy on the aggregate-question slice from effectively-zero to production-usable, consistent with the system-wrapping literature.[^8] The residual doc-question traffic kept plain hybrid retrieval. The lesson: the biggest retrieval upgrade of the year was a router and some SQL views.

(Case studies are composites of documented patterns, labeled as such; the numbers are illustrative of the published ranges, not client disclosures.)

## Problem set

1. **The family assignment.** Take 20 real queries from your corpus's logs (or write 20 honest ones). Assign each to the family that should serve it, with one clause of justification. Deliverable: the assignment table plus the *distribution*, which is your architecture argument in one row of percentages.
2. **Reranker ROI math.** Using your Phase-1/2 experiment numbers: compute the break-even query volume at which the reranker's accuracy lift justifies its fee and latency for (a) a human-facing search tool, (b) an agent consumer where retrieved tokens feed generation cost. Show both calculations; explain why they differ.
3. **The graph refusal memo.** A stakeholder returns from a conference demanding GraphRAG. Write the 250-word reply: the two-question triage, the logged-query evidence you would collect, the cost multiples, and the condition under which you would reverse yourself. Tone: collaborative, not smug. This memo ships more consulting value than most implementations.
4. **Late-interaction fit check.** For your corpus: estimate what fraction of queries hinge on token-scale identifiers. Describe the experiment (10 queries, MaxSim vs pooled-vector, judged) that would confirm it, and the storage multiple you would accept before saying no.
5. **Semantic-layer starter.** Pick three real tables (or exports) from any system you use. Write the semantic-layer documentation that would make text-to-SQL viable: view definition, business definitions of each metric, two example query pairs per view. This artifact is directly reusable in client work.

## Common mistakes experts see

- **Skipping the reranker to save latency, then paying in k.** Teams push k to 20 to compensate for a weak top-5, spending window tokens (Monday's budget!) to avoid a 300ms model call.
- **Buying the leaderboard, not the license.** zerank-2's weights are CC-BY-NC; "open" and "usable in your client's product" are different claims.[^1][^2]
- **GraphRAG as résumé-driven development.** The 2026 pattern: a quarter spent shipping a graph that answers questions nobody logged. Triage first.[^6]
- **Embedding tables.** If the answer is an aggregate, a filter, or a join, it belongs to SQL. Vector search over serialized rows is approximate arithmetic.
- **Testing text-to-SQL on the demo schema.** The benchmark-to-production cliff is the finding.[^8] Evaluate on your real schema with your real column names or you have evaluated nothing.
- **One index format too many.** Adding late interaction alongside dense + lexical + graph gives you four indexes to keep consistent. Every additional retrieval family is an ongoing consistency liability, not a one-time install.
- **Tuning retrieval without a regression set.** Any change you can't score is a vibe. (You built the set in Week 4; use it.)

## Reflection questions

1. For your own corpus: which two of the five families carry 90% of your queries, and what logged evidence supports that split?
2. MaxSim keeps per-token document vectors; a cross-encoder attends jointly over query and document. Explain, mechanically, one query class where the cross-encoder still wins and why the gap is irreducible.
3. LazyGraphRAG moved LLM spend from indexing to query time. For what usage profile (queries/day vs corpus churn rate) does that trade go *against* you?
4. Your client's counsel asks: "the reranker sees our documents at query time; what does that change in our data-processing agreement compared to embedding-time exposure?" Answer in three sentences.
5. Design the router prompt (or rule set) that decides hybrid vs SQL vs graph for an internal analytics assistant. Which misroute is cheapest, and how does that asymmetry shape your defaults?
6. The text-to-SQL 33%→75% system-wrapping result: name the two components of the wrapper you'd build first for your own warehouse, and the eval that proves each.

## My take (reviewer lens)

**Jerry Liu** would call the five-family map sound but static: the interesting 2026 work treats retrieval modules as *tools an agent composes per query*, not as an architecture chosen once — routing, query planning, and multi-step retrieval move the needle more than swapping rerankers, and he'd want today's taxonomy explicitly subordinated to tomorrow's loop (it is; the seam is deliberate). **Chip Huyen** would press on the missing production telemetry: this lesson chooses architectures by benchmark and triage, but real systems choose by monitoring — retrieval logs, per-family hit rates, drift on the query distribution — and a lesson that says "run the ablation once on Saturday" understates that the ablation must keep running in production. **Mira Murati** would push from the customization angle: the lesson treats rerankers and embedders as commodities you rent, but for a differentiated agency the winning move is often a small model *fine-tuned on your domain's relevance judgments*, which routinely beats general-purpose rerankers on-domain at a fraction of the serving cost; renting the frontier is the default, not the ceiling. All three critiques share a root: today's lesson is the parts catalog, and parts catalogs flatter the parts. Saturday is where the catalog meets your data, which is the only place any of these choices become true or false.

## Further reading

**Must-read**
- Agentset reranker leaderboard. Bookmark it; it updates.[^1]
- Microsoft Research, *LazyGraphRAG sets a new standard for quality and cost*.[^5] The 0.1%/700× post, primary source.
- Jina-ColBERT-v2 paper, §3 (architecture): the cleanest modern write-up of late interaction.[^3]

**Recommended**
- ZeroEntropy's reranker-selection guide (vendor, but unusually candid about tradeoffs).[^2]
- A 2026 GraphRAG practitioner verdict: Graffitecs' "when a knowledge graph actually pays off" is the most balanced short one.[^6]
- Datost, *How Accurate Is Text-to-SQL, Really?*: the benchmark-vs-production cliff with numbers.[^8]

**Optional**
- PLAID paper (SIGIR '22) for the engineering of multi-vector serving.[^4]
- BIRD leaderboard, to watch the low-80s ceiling move.[^7]

## Citations

[^1]: Agentset, *Best Rerankers for RAG — Leaderboard* (ELO-style, continuously updated): zerank-2 ≈1638, Cohere Rerank v4.0 Pro ≈1629; jina-reranker-v3 strongest sub-200ms option. https://agentset.ai/rerankers (search-verified 2026-07-17; corroborated by [^2]; fetch egress-blocked — liveness pass pending)

[^2]: Cross-vendor reranker comparisons, mid-2026: *How to Add Reranking… Cohere Rerank 4 Pro, Voyage rerank-2.5, zerank-2* (https://www.bestaiweb.ai/how-to-add-reranking-to-your-rag-pipeline-with-cohere-rerank-4-pro-voyage-rerank-2-5-and-zerank-2-in-2026/); FutureAGI, *Best Rerankers for RAG in 2026* (https://futureagi.com/blog/best-rerankers-for-rag-2026/); ZeroEntropy, *Ultimate Guide to Choosing the Best Reranking Model* (https://zeroentropy.dev/articles/ultimate-guide-to-choosing-the-best-reranking-model-in-2025/). zerank-2 open weights are CC-BY-NC. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^3]: Rohan Jha, Bo Wang, Michael Günther et al. (Jina AI), *Jina-ColBERT-v2: A General-Purpose Multilingual Late Interaction Retriever*, arXiv 2408.16672. 89 languages; 8192-token length; controllable output dims; +6.5% over ColBERTv2 on English; 0.521 avg across 14 BEIR tasks. https://arxiv.org/abs/2408.16672 ; model card: https://huggingface.co/jinaai/jina-colbert-v2 (search-verified 2026-07-17)

[^4]: Keshav Santhanam, Omar Khattab et al., *PLAID: An Efficient Engine for Late Interaction Retrieval*, CIKM 2022. Centroid interaction + pruning; up to 7× GPU / 45× CPU latency reduction for ColBERTv2. https://dl.acm.org/doi/abs/10.1145/3511808.3557325 (search-verified 2026-07-17)

[^5]: Microsoft Research blog, *LazyGraphRAG sets a new standard for quality and cost* (Nov 2024). Comparable quality to GraphRAG global search at 0.1% of indexing cost; >700× lower query cost for global queries; NLP noun-phrase graph construction, deferred LLM use. https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/ (search-verified 2026-07-17; corroborated by thestack.technology and dev.to coverage; fetch egress-blocked — liveness pass pending)

[^6]: 2026 GraphRAG production verdicts: Graffitecs, *RAG vs GraphRAG: when a knowledge graph actually pays off* (https://graffitecs.com/pages/insights/rag-vs-graphrag.html); Alexander Shereshevsky, *Graph RAG in 2026: A Practitioner's Guide* and *The GraphRAG Cost Cliff* (https://medium.com/graph-praxis/graph-rag-in-2026-a-practitioners-guide-to-what-actually-works-dca4962e7517 ; https://medium.com/graph-praxis/the-graphrag-cost-cliff-how-33-000-became-33-in-eighteen-months-be1b0fbe37e4); AI Learning Guides, *RAG in Production 2026* (https://ailearningguides.com/rag-production-patterns-2026/) — 6–8× indexing / ~3× operating cost multiples; "most teams reaching for it shouldn't." (search-verified 2026-07-17; cost multiples are practitioner estimates, flagged as such; fetch egress-blocked — liveness pass pending)

[^7]: BIRD benchmark state, 2026: best pipelines ~low-80s execution accuracy on test (top entry ~81.95%, AskData + GPT-4o); human expert ~92–93%. https://beancount.io/bean-labs/research-logs/2026/06/06/bird-benchmark-text-to-sql-real-database-gap ; https://datost.com/blog/text-to-sql-accuracy-benchmarks (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

[^8]: Enterprise text-to-SQL gap: Promethium, *Enterprise Text-to-SQL: What Accuracy Benchmarks Really Mean* (vendor 85–90% claims vs 10–31% measured on production schemas; https://promethium.ai/guides/enterprise-text-to-sql-accuracy-benchmarks-2/); Datost, *How Accurate Is Text-to-SQL, Really?* (same frontier model ~33% bare vs 75.2% system-wrapped; https://datost.com/blog/text-to-sql-accuracy-benchmarks). (search-verified 2026-07-17; the 75.2% figure is the vendor's own system — read as a directional system-vs-model claim; fetch egress-blocked — liveness pass pending)

[^9]: Anthropic, *Introducing Contextual Retrieval* (Sep 2024) — canonical numbers and method taught in [[03-wed-rag-as-a-system]]; up to 67% top-20 failure-rate reduction with contextual embeddings + BM25 + reranking. https://www.anthropic.com/news/contextual-retrieval (URL-verified in vault refresh 2026-07-17)

_last_verified: 2026-07-17_
