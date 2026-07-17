---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 3
day_name: wed
session_slug: basecamp-part-1-prompting-rags
date_due: 2026-04-29
tags: [rag, retrieval, embeddings, bm25, hybrid-retrieval, chunking, reranking, contextual-retrieval, context-assembly, rag-eval, ragas, long-context, needle-in-haystack, faithfulness, recall]
sources:
  - lewis-2020-rag-neurips
  - anthropic-contextual-retrieval-2024
  - liu-2024-inverted-thinking-rag
  - liu-2024-systematically-improving-rag
  - hsieh-2024-ruler-benchmark
  - nolima-2025-long-context
  - liu-2023-lost-in-middle
  - chroma-2025-context-rot
  - voyage-rerank-2-2024
  - cohere-rerank-4-2025
  - ragas-framework-2024
last_verified: 2026-07-17
word_count_target: 6500
---

# RAG as a system — retrieval, rerank, context assembly, and the evals that tell you if any of it is working

## Why this matters

Most practitioners who "use RAG" are actually using one stage of a four-stage system. They embed documents, store them in a vector database, retrieve the top-k nearest neighbors at query time, and shove the results into a prompt. Then they wonder why the system confidently answers questions with wrong information, or why it completely misses paragraphs that obviously contain the answer.

The gap between "I have a vector search" and "I have a working RAG system" is almost always a pipeline-design problem, not a model-capability problem. The model is usually fine. What's broken is: the chunks are sized wrong, the first-stage retrieval is missing lexical matches, there's no reranking pass to filter junk before the LLM sees it, the retrieved context is placed in the wrong position in the prompt, and there's no eval telling you any of this.

By the end of today you will be able to:

1. Diagnose a RAG failure at the correct stage — retrieval, rerank, context assembly, or generation — rather than reflexively iterating on the prompt.
2. Know when to use embeddings, BM25, or hybrid retrieval, and understand why Anthropic's Contextual Retrieval combines both to cut the top-20 failure rate from 5.7% to 2.9%.
3. Design a chunking strategy that matches your document type and query pattern, with awareness of the specific failure modes each strategy introduces.
4. Evaluate a RAG system quantitatively using recall@k, faithfulness, and answer-correctness — not "it seems to work when I test it."
5. Take a position on the live controversy: whether long-context models are making RAG architectures obsolete, or whether that argument misunderstands what the benchmarks are actually measuring.

This capability delta matters because anyone with an Anthropic or OpenAI API key can assemble a RAG pipeline from a tutorial. The ability to debug it, improve it systematically, and evaluate it honestly is not in the tutorial.

## Prerequisites

- [[01-mon-prompting-first-principles]] (prompting from first principles) or equivalent understanding of how a language model consumes its context. The eval discipline from [[02-tue-prompt-engineering-in-practice]] carries directly into Part 7 of this lesson.
- Familiarity with vector similarity as a concept — you don't need the math, but you should know that embeddings are high-dimensional vectors and that "closer in vector space = semantically similar."
- Claude.ai access and Claude Code installed in a working scratch folder. One of this lesson's experiments runs through Claude Code; one runs manually in Claude.ai. You do not write code by hand.

---

## Part 1 — Why RAG exists as a category

Language models have two kinds of memory: parametric and non-parametric.

Parametric memory is everything baked into the model's weights during training. When Claude tells you that the capital of France is Paris, it's drawing on weight-encoded knowledge that was compressed out of the pretraining corpus. Parametric memory is fast, cheap to query, and invisible — but it is frozen at training time, and it has no memory of documents that weren't in the training corpus.

Non-parametric memory is external — documents, databases, files, APIs — that are retrieved at inference time and placed into the context window. Lewis et al.'s 2020 NeurIPS paper coined this framing precisely: RAG combines "pre-trained parametric and non-parametric memory for language generation."[^1] At the time they were talking about Wikipedia indexes retrieved via dense passage retrieval and fed to BART. The architecture has generalized enormously since then, but the core insight has not changed.

There are five reasons a practitioner reaches for a RAG architecture rather than relying on parametric memory alone:

**Freshness.** A model trained in early 2024 cannot answer questions about events in late 2025 unless those events are in its context. You cannot retrain a frontier model every week. You can update a document index every night.

**Context-window cost.** Even with Claude at 200K tokens, loading an entire corpus into every request is prohibitively expensive and slow. A 100-document legal archive might run 600K tokens — fine for a single, expensive research query, completely non-viable for 10,000 daily support tickets. Retrieval gates which documents enter the context for any given query.

**Privacy and data residency.** Many organizations cannot feed entire databases to a frontier model. Retrieval lets you build an index over sensitive data without needing to ship every document to the LLM on every call — especially when combined with on-premise embedding infrastructure.

**Provenance and attribution.** A retrieved system can show the user exactly which paragraphs the answer came from. A parametric model cannot. This distinction matters enormously in legal, financial, medical, and regulatory applications where "what's your source?" is not a rhetorical question.

**Corpus scale.** The parametric memory of any model is a lossy compression of its training data. Facts that appear rarely in training are encoded weakly. For domain-specific corpora — niche regulatory texts, company-internal documentation, specialized scientific literature — retrieval outperforms parametric recall because the documents are present verbatim, not approximated through a compressed encoding.

None of this means RAG is always the right answer. For truly general Q&A across a broad and stable knowledge domain, a well-prompted frontier model with parametric memory often outperforms a poorly designed RAG system. The failure mode that gets teams in trouble: choosing RAG, then under-investing in retrieval quality while over-investing in the generation prompt.

---

## Part 2 — Embeddings vs BM25: the retrieval substrate

### Semantic search via embeddings

Embedding models convert text into dense vectors — typically 768, 1024, or 1536-dimensional arrays of floating-point numbers. The key property: semantically similar texts land nearby in vector space, and you measure "nearby" with cosine similarity.

If you embed the query "what is the refund policy for enterprise contracts?" and you've embedded every paragraph in your policy documentation, the vectors for paragraphs that discuss contract termination, SLA credits, and cancellation terms will score high, even if those paragraphs use completely different words than your query. This is the core win of embedding-based retrieval: it bridges the vocabulary gap between how a user asks a question and how a document answers it.

This works well until it doesn't. Embedding models are trained to capture semantic meaning, but they compress meaning into a fixed-size vector. That compression loses precision. If a user queries "Section 12.3(b)" or "error code E_AUTH_FAILED" or a product SKU, the embedding model has no good way to represent those identifiers semantically — they're arbitrary strings, not concepts. The retrieved results will be topically adjacent but often won't contain the specific term the user needs.

The other failure mode is false semantic similarity. A query about "the risks of a low-carbohydrate diet" will retrieve nutritional science documents — but may also retrieve diet-company marketing content that uses similar vocabulary with opposite intent. Embedding-based retrieval can't distinguish intent; it matches semantic surface.

### BM25: the lexical baseline you should not skip

BM25 (Best Matching 25) is a term-frequency-based scoring function. It scores documents for a query based on how often query terms appear in the document, normalized by document length and corpus frequency. It is, in essence, a sophisticated TF-IDF. It is fast, cheap, fully interpretable, and requires no GPU.

For a query like "Section 12.3(b) indemnification clause" or "VLOOKUP formula returning #REF! error," BM25 is often the better first-stage retriever. The user used the same words the document uses. Semantic interpolation is not only unnecessary — it actively adds noise by retrieving documents that discuss similar concepts but not the same terminology.

The empirical result: in Jason Liu's May 2024 comparison testing against large essay corpora, "full text search and embeddings basically performed the same, except full text search was about 10 times faster."[^2] For many production use cases, the incremental semantic lift from embeddings over BM25 is smaller than practitioners assume, and BM25's latency and cost advantages are much larger.

### Hybrid retrieval: why both beat either

The practical answer is not BM25 or embeddings. It's both, merged via Reciprocal Rank Fusion (RRF). RRF takes the ranked lists from each retrieval method and combines them by summing reciprocal ranks, so a document that appears at rank 3 in BM25 and rank 7 in semantic search outscores a document that only appears in one list.

The empirical argument for hybrid over either alone is not subtle. On Natural Questions (open-domain QA), BM25 passage recall was approximately 22%; dense retrieval reached approximately 49%; hybrid pipelines achieved up to 53%. On the BEIR benchmark suite (diverse retrieval tasks), BM25 nDCG@10 of 43.4 improved to over 52.6 via hybrid reranking.[^3] A sourcing caveat: those specific percentages come from a practitioner synthesis of the dense-passage-retrieval (Karpukhin et al. 2020) and BEIR literatures, not from one controlled study — treat the ordering (hybrid > dense > BM25 on vocabulary-gapped QA) as the robust finding and the exact numbers as illustrative.

Anthropic's Contextual Retrieval results show the same dynamic. Their hybrid of Contextual Embeddings plus Contextual BM25 reduces top-20 chunk failure rate from 5.7% to 2.9% — a 49% relative improvement — while Contextual Embeddings alone only reach 3.7% failure rate, a 35% improvement.[^4] The lexical signal is doing meaningful work even on top of semantically enriched embeddings. More on exactly what "contextual" means in Part 4.

---

## Part 3 — Chunking: the decision that sets the ceiling

Chunking is where most RAG systems are quietly broken. The failure rarely shows up in a demo. It shows up at scale, when edge cases accumulate.

### Why you chunk at all

A 200-page financial filing embedded as a single document is useless for retrieval. Cosine similarity between a query and a 150,000-token document collapses into meaninglessness — too much information is averaged into a single vector, and the signal for any specific query disappears in the noise. Chunking breaks documents into units that are small enough to be semantically coherent at the embedding level.

The tension: smaller chunks retrieve more precisely but give the LLM less context to reason from. Larger chunks preserve context but dilute the retrieval signal.

### Fixed-size chunking: fast, simple, and often wrong

The most common approach. Split at a fixed character or token count, with some overlap window. You can index ten million documents in an hour. The failure mode is that chunk boundaries slice across semantic units — a sentence is split mid-clause, a code snippet is severed from its docstring, a financial table is separated from the text that interprets it.

Jason Liu's January 2024 inversion analysis is useful here: *"If I wanted to build the worst RAG system, I would chunk all my documents at arbitrary fixed sizes and not think about whether the chunks are semantically coherent."*[^5] The key failure mode he identifies: the system retrieves the right document but the wrong chunk, so the answer is technically adjacent to the context but not present within it.

Fixed-size chunking is appropriate when your documents have a natural fixed-size structure (e.g., individual customer support tickets, short product descriptions, standardized regulatory filings with consistent paragraph lengths). It fails on long-form documents with heterogeneous structure: technical documentation, legal briefs, narrative research reports.

### Semantic chunking: principled but expensive

Semantic chunking embeds each sentence, compares adjacent sentence embeddings for similarity, and creates chunk boundaries at points of low similarity. You're splitting where the meaning shifts, not where a character count runs out.

A 2024 benchmark across multiple document types found semantic chunking can improve recall by up to 9% over fixed-size chunking. The cost: you must embed every sentence in the corpus at indexing time, which adds meaningful preprocessing overhead and cost, especially for large corpora that need to be re-indexed frequently. For a legal document archive that updates weekly with hundreds of new filings, the embedding cost of semantic chunking at sentence level is non-trivial.

The failure mode in semantic chunking is over-fragmentation. Documents with dense, high-similarity content — financial analysis, technical specifications — can produce very long chunks because the similarity threshold is never crossed. Those long chunks dilute the retrieval signal back toward the fixed-size problem.

### Parent-child (small-to-large) retrieval

This is the most underused design in production RAG systems, and it directly addresses the tension between retrieval precision and generation context.

The architecture: index small child chunks (e.g., individual paragraphs or 200-token segments) for retrieval. When a child chunk is retrieved, return its parent chunk (e.g., the full section it belongs to) to the LLM for generation.

The retrieval signal stays precise because you're matching against small, semantically tight units. The generation context stays rich because the LLM sees the full surrounding passage. A customer support query about a specific product error code retrieves the exact paragraph that mentions the code, but the LLM answers from the full troubleshooting section.

This pattern is particularly effective in:
- Legal document Q&A (retrieve specific clauses, but the LLM needs surrounding context for interpretation)
- Financial filings (retrieve specific line items, but the LLM needs the management discussion section for color)
- Technical documentation (retrieve the function signature, but the LLM needs the full usage example section)
- Research literature (retrieve the hypothesis sentence, but the LLM needs the methodology paragraph to understand what was actually measured)

The failure mode is metadata bookkeeping. Every child chunk needs a reliable parent pointer. When documents are updated, parent chunks can become stale while child chunks are re-indexed. In systems that don't carefully manage versioning, you end up with retrieved child chunks pointing to outdated parent documents.

### A critical evaluation caveat on chunking research

Most published chunking benchmarks test on English-language, moderately-structured documents. The NVIDIA 2024 benchmark that found page-level chunking winning with 0.648 accuracy was run across a specific mix of five document types. Generalizing "page-level chunking is the winner" to a corpus of dense legal text in multiple languages, or to a codebase where file-level chunking is the natural unit, requires empirical verification on your actual corpus, not transfer from a benchmark run on different documents. This is the discipline Jason Liu calls "understand your data first": segment the query types, then measure which chunking strategy serves each segment.[^6]

---

## Part 4 — Anthropic Contextual Retrieval: the methodology in full

Published September 19, 2024, Anthropic's Contextual Retrieval post describes an approach that addresses a specific failure mode in classic chunking: chunks that make sense in isolation but lose critical meaning when separated from their document context.[^4]

The concrete failure: you're building a RAG system over customer support documentation for a financial software product. A chunk reads: "The process described above applies to accounts opened before January 2023." Without the preceding paragraphs establishing what process is being described, this chunk is useless — or worse, actively misleading.

Contextual Retrieval's fix is to prepend each chunk with a short, LLM-generated contextual description before embedding it. The prompt is roughly: *"Here is the document. Here is a chunk from it. Write a short, document-aware summary that situates this chunk in context."* Claude Haiku is run over every chunk at indexing time to produce these summaries. The chunk that gets embedded becomes: *"[Context: This section describes the dividend reinvestment process for legacy accounts under the pre-2023 regulatory framework.] The process described above applies to accounts opened before January 2023."*

Two simultaneous benefits: the embedding now captures the semantic meaning of the chunk in its document context, not just the chunk in isolation. And the BM25 index now has richer lexical signal because the contextual prefix adds relevant terminology.

The evaluation results, as reported by Anthropic:

- Baseline top-20 failure rate (no contextual retrieval): **5.7%**
- Contextual Embeddings alone: **3.7%** (35% relative improvement)
- Contextual Embeddings + Contextual BM25: **2.9%** (49% relative improvement)
- Contextual Embeddings + Contextual BM25 + Reranking: **1.9%** (67% relative improvement)

These are striking numbers. But there is a specific critique that the post does not address, and any practitioner building a serious system should internalize it: the evaluation corpus consists of five domains of moderate-size technical documentation. That is not the same as a 100-million-token legal archive, or a codebase with complex cross-file dependencies, or a multi-year financial filing database where the definition of a term in 2019 is subtly different from its definition in 2024.

The contextual prefix approach works because the context window allows Claude to see the document and the chunk together. For very long documents — 50,000+ tokens — the context is still local (a few surrounding sections), not the full document. For documents where the relevant context is genuinely distributed across the full length, a locally-contextual prefix may be insufficient.

The prompt-caching optimization that Anthropic describes (caching the full document in context while running the chunk-contextualization prompt) reduces the cost of contextualizing large corpora significantly — Anthropic cites a cost range of $1–16 per million tokens depending on chunk size, with caching enabled. That cost still adds up at scale. For a 50-million-document news archive that needs daily re-indexing, contextual retrieval is an engineering decision, not a free upgrade.

Apply it confidently to: domain-specific knowledge bases of moderate size (company docs, product manuals, legal briefs up to a few thousand documents, research literature), when you control re-indexing cadence and can afford the upfront contextualization cost.

Verify before assuming it transfers to: massive, high-churn corpora; documents where critical context is distributed across thousands of tokens; multi-language corpora (the contextual prompt is in English; cross-lingual generalization is untested in the published results).

---

## Part 5 — Reranking: why the first-stage result is not the final answer

First-stage retrieval — whether BM25, embeddings, or hybrid — optimizes for speed. You are searching millions of documents in milliseconds. The models are bi-encoders: query and document are encoded independently, and similarity is a dot product or cosine computation against a pre-built index. This is fast and scalable, but it cannot model the interaction between a specific query and a specific document deeply.

Rerankers (cross-encoders) work differently. They take a query-document pair, concatenate them, and run a full transformer pass over the joint input. The model attends to how the query and document relate to each other — which parts of the document specifically answer which parts of the query, and where the document is irrelevant or contradictory to the query. This is richer reasoning, but it is O(N) in the number of candidates and cannot scale to millions of documents without a first-stage filter.

The two-stage architecture emerges from this tradeoff: first stage retrieves k=50 to 200 candidates fast; second stage reranks those candidates with a cross-encoder and returns top-5 to 20. The LLM then generates from those top-5 to 20. The first stage is optimizing recall. The second stage is optimizing precision.

### Cohere Rerank 4

Cohere's Rerank API is a mature commercial cross-encoder product. Rerank 4, released December 11, 2025, is the current flagship, shipped in two variants — rerank-4-pro (accuracy-first) and rerank-4-fast (latency-first) — with a 32K-token context window, four times Rerank 3.5's, plus support for 100+ languages and a self-learning mechanism that adapts relevance scoring to enterprise domains.[^13] The longer context matters for exactly the corpora where reranking earns its keep: legal and financial documents where the relevant passage plus its surrounding context exceeds the old 8K limits. Latency for Cohere's API reranking runs 150–400ms plus network on a candidate pool of 50 documents; for applications requiring sub-100ms end-to-end latency, deploy the fast variant on a pre-filtered candidate pool of 30–50, not 200.

### Voyage AI rerankers (now MongoDB)

Voyage AI — acquired by MongoDB in 2025 — is worth knowing specifically because Voyage rerankers are what Anthropic used in the Contextual Retrieval stack. The September 2024 generation, rerank-2, added an average 13.89% accuracy improvement on top of OpenAI's text-embedding-3-large across 93 retrieval datasets, with a 16K context window.[^7] The current generation, rerank-2.5 and rerank-2.5-lite (August 2025), doubles context to 32K and introduces instruction-following — you can steer relevance scoring with natural language ("prefer primary sources over commentary"), which MongoDB reports adds an average 11.48% accuracy on instruction-following retrieval datasets.[^14]

The practical question for a reranker choice: what is your candidate pool size, what is your latency budget, and do you need multi-language support or instruction-steered relevance? For most English-language production systems with 50–100 candidates and a few hundred milliseconds of budget, Cohere rerank-4-fast and Voyage rerank-2.5-lite are both solid. Head-to-head numbers between the two current flagships are mostly vendor-published (each claims wins on its own benchmark suite), so treat cross-vendor comparisons as marketing until you've measured on your own corpus.

---

## Part 6 — Context assembly: how retrieved content lands in the prompt

Retrieval gives you the right passages. Context assembly determines whether the LLM can actually use them.

### Placement and the lost-in-the-middle problem

Liu et al.'s 2023 paper "Lost in the Middle: How Language Models Use Long Contexts"[^8] — now published in Transactions of the Association for Computational Linguistics 2024 — documents a U-shaped performance curve in long-context models. When the relevant document is placed at the beginning or end of the context, accuracy is high. When it's placed in the middle of a long context, accuracy degrades significantly, even in models with explicit long-context support. The paper showed this effect across multi-document QA and key-value retrieval, finding that the models in their evaluation showed statistically significant degradation when relevant information was buried mid-context.

The operational implication for RAG context assembly: put the most relevant retrieved chunks at the beginning of the context block, or split between beginning and end, not buried in the middle. If you're assembling 10 retrieved chunks, don't place them in retrieval order. Reorder by relevance, front-loading the top results.

### Citation scaffolds

For attribution-sensitive applications — legal research, financial analysis, medical Q&A, any domain where "where does this come from?" is a compliance question — the context assembly step should include source metadata explicitly. A working pattern:

```
<sources>
  <source id="1">Document: Annual Report 2024, Section 7.2, Page 43</source>
  <source id="2">Document: Q4 Earnings Call Transcript, November 2024</source>
  <source id="3">Document: 10-K Filing, Risk Factors, Item 1A</source>
</sources>

<context>
  [1] Revenue from cloud services grew 34% year-over-year to $2.1B...
  [2] CFO stated during the call: "We expect margin compression to continue through H1..."
  [3] Material risk: concentration of revenue in three enterprise customers...
</context>

Answer the user's question. Cite sources using [1], [2], [3] notation.
```

Skip this scaffolding and LLMs will paraphrase retrieved content without attribution, and the provenance advantage of RAG over parametric memory is lost. More concretely: in a legal research application, an answer without a source citation is not an answer — it's a liability.

### Chunk deduplication and overlap management

A practical assembly problem: if you're using parent-child retrieval and multiple child chunks from the same parent are retrieved, you may end up sending the parent document twice or more. Context window tokens are not free. Deduplicate retrieved parents before assembly. Track which chunk IDs have already contributed a parent to the context.

---

## Part 7 — RAG evals: recall@k, faithfulness, and answer-correctness

Here is the failure mode that distinguishes teams who ship working RAG systems from teams who ship systems that seem to work: **not running an eval harness.**

"It seems to work in my testing" is not an eval. It's a bias-toward-success sampling of a space that contains many ways to fail. Jason Liu's June 2025 survey of teams who came to him with broken RAG systems found the same pattern repeatedly: no baseline measurement, no per-component diagnostic, no synthetic evaluation set. The teams had tuned their prompts extensively and their retrieval not at all.[^6]

### The three measures that matter

**Recall@k.** Of all the passages that contain relevant information for a given query, how many does your top-k retrieval find? This is a retrieval-stage metric. If recall@20 is 60%, your retrieval is losing 40% of relevant context before the LLM ever sees it. No amount of prompt tuning recovers context that was never retrieved.

To measure recall@k, you need a ground-truth set: query-answer pairs where you know which document passages contain the answer. You can build this with synthetic data generation: ask Claude to produce 50–100 questions that can only be answered from specific passages in your corpus, along with the passage IDs. Then run your retrieval and score how often those passage IDs appear in top-k.

**Faithfulness.** Given the retrieved context, does the LLM's response contain claims that are not supported by that context? Faithfulness measures hallucination relative to the retrieval, not relative to ground truth. A faithful response that cites wrong information because the retrieval was wrong is still faithful — the model stayed within its context. An unfaithful response manufactures claims that don't appear in the context at all.

The RAGAS framework (Retrieval Augmented Generation Assessment)[^9] measures faithfulness by decomposing the response into atomic claims and checking each claim against the retrieved context using an LLM judge. Faithfulness score = (claims supported by context) / (total claims in response).

**Answer-correctness.** Is the final answer right? This is the end-to-end metric that combines retrieval recall, faithfulness, and generation quality. RAGAS calculates answer correctness using F1 over factual overlap between the generated answer and a ground-truth answer, combining precision (facts in the answer that are correct) and recall (correct facts from ground truth that appear in the answer).

### The diagnostic stack

These three metrics compose into a diagnostic tree:

- Low recall@k + wrong answers = fix retrieval first. Prompt changes will not help.
- High recall@k + low faithfulness + wrong answers = the LLM is ignoring or hallucinating past the context. Check prompt structure, context placement, model temperature.
- High recall@k + high faithfulness + wrong answers = your retrieved passages don't contain the right answer. The retrieval is returning plausible but wrong documents. Check chunking granularity.
- High recall@k + high faithfulness + correct answers = the pipeline is working. Measure latency and cost; optimize for scale.

The team that runs these three metrics on 100 synthetic queries before launching has a fundamentally different debugging capability than the team that doesn't. The 100-query synthetic eval set is the minimum viable eval harness for a production RAG system.

---

## Part 8 — The live controversy: does long context make RAG obsolete?

This is the argument that has circulated since Gemini 1.5 Pro demonstrated near-perfect recall at 1 million tokens in early 2024. The logic: if you can fit your entire knowledge base into the context window, why bother with a retrieval system? Just load it all and let the model find what it needs.

The empirical case for long context is real. On the original Needle in a Haystack (NIAH) test — place a specific fact ("the best pizza in San Francisco is at...") in a document and ask the model to find it — Gemini 1.5 Pro achieves over 99.7% recall at 1 million tokens. Claude 3 Opus achieves over 99% at 1 million tokens. These are impressive numbers. If NIAH were the only relevant task, the argument "RAG is obsolete" would be defensible.

The problem is that NIAH is a lexical retrieval task dressed up as a long-context benchmark. The needle is retrieved because the exact query phrase matches the exact needle phrase. It is not reasoning over the context. It is Ctrl+F with attention.

### RULER and multi-hop degradation

Hsieh et al.'s RULER benchmark (NVIDIA, COLM 2024) was designed specifically to expose what NIAH misses.[^10] RULER introduces multi-hop tracing, aggregation tasks, and question answering that requires reasoning over multiple scattered locations in the context — not just finding one needle. The result: despite achieving near-perfect scores on vanilla NIAH, almost all models showed significant performance drops as context length increased on RULER's harder tasks. Only half of models claiming 32K-token context could maintain satisfactory performance at 32K on RULER's multi-hop and aggregation tasks.

### NoLiMa and the non-lexical gap

Adobe Research's NoLiMa benchmark (ICML 2025) went further.[^11] NoLiMa specifically minimizes lexical overlap between the query and the needle. The question and the relevant passage use different words — the model must infer the connection, not match tokens. Results: while LLMs perform well in short contexts (under 1K tokens), performance degrades significantly as context length increases. Of the 12 models evaluated — all claiming at least 128K context — 10 dropped below 50% of their strong short-length baseline at 32K tokens. Even GPT-4o dropped from 99.3% at short context to 69.7% at longer context.

The interpretation from the NoLiMa authors: performance drops stem from attention mechanisms facing increased difficulty with non-lexical retrieval in longer contexts. Adding chain-of-thought prompting did not reliably fix the problem.

### Context rot: the 2025 production finding

Chroma Research's July 2025 study "Context Rot"[^12] evaluated 18 LLMs, including Claude 4 and GPT-4.1, across tasks ranging from simple retrieval to text replication. They found non-uniform performance degradation as input length increases, even on tasks as simple as non-lexical retrieval, well before the context window is close to full. Three contributing mechanisms: the lost-in-the-middle effect, attention dilution from longer sequences, and distractor interference from semantically similar but irrelevant content.

### Taking a position

The debate re-erupted in January 2026, when a viral "RAG is DEAD" wave swept LinkedIn, Reddit, and Hacker News on the strength of 1M-token windows becoming table stakes. The wave resolved into a consensus worth stating precisely: **naive RAG is dead; sophisticated, agentic RAG is thriving.**[^15] Vanilla 2023-style RAG — chunk, embed, top-k, hope — is no longer a defensible production default. Retrieval itself is not going anywhere. Thursday's lesson ([[04-thu-rag-failure-modes-and-long-context-debate]]) takes this argument apart in full.

The correct position, supported by these results, is not "RAG is obsolete" and not "RAG always beats long context." It is:

Long context wins when: your corpus fits comfortably within the context window, your task requires reasoning across the full document rather than finding specific passages, you can afford the token cost per query, and the query pattern is stable enough that loading the full document is efficient.

RAG wins when: your corpus is too large for the context window (even at 1M tokens, a 10-million-document support archive doesn't fit), freshness requirements mean daily or hourly index updates, query patterns are sparse relative to corpus size (you don't need to read all 500 pages of the filing for every question about it), and multi-hop reasoning over large corpora must be reliable rather than "usually works."

The 2026 synthesis of the two: **use long context to reason over a bounded evidence set; use retrieval to decide what that evidence set should be.** The best production systems use a retrieval stage to narrow the candidate set, then a long-context model to reason over the narrowed context. Current frontier models are much better at long-context reasoning than their predecessors — which makes them better RAG *generation* models, not replacements for RAG retrieval.

The benchmark evidence (RULER, NoLiMa, Context Rot) consistently shows that the models claiming 1M-token context windows cannot reliably find and reason over non-lexical needles as context length grows. Production systems that rely on "just load everything" for multi-hop reasoning tasks will find this empirically.

---

## Runnable experiment — minimal RAG with and without contextual prefixes

This experiment has two parts. Part A runs via Claude Code. Part B is a manual comparison in Claude.ai.

### Part A — Build a minimal RAG and measure recall@k (Claude Code)

**Direct Claude Code with this instruction:**

> I need you to build a minimal RAG system over five documents and run a recall evaluation. Here are the documents to use:
>
> 1. A 500-word fictional "enterprise software pricing FAQ" covering topics: annual contracts, seat-based pricing, volume discounts, cancellation policy, renewal terms.
> 2. A 500-word fictional "employee onboarding policy" covering: probation period, equipment requisition, IT access, first-week schedule, manager assignment.
> 3. A 500-word fictional "product release notes" for a fictional SaaS tool, covering: version 2.4 features, known issues, deprecated APIs, upgrade instructions.
> 4. A 500-word fictional "customer support escalation runbook" covering: severity tiers, SLA times, escalation contacts, war room procedure, post-incident review.
> 5. A 500-word fictional "data retention and deletion policy" covering: retention schedules by data type, deletion workflows, legal hold procedures, audit log requirements.
>
> Generate these documents yourself. Then:
>
> 1. Chunk each document into 150-token fixed-size chunks with 30-token overlap.
> 2. Embed all chunks using a simple TF-IDF representation (since you can't call an external embedding API, use TF-IDF similarity as a proxy for semantic retrieval — it approximates BM25 behavior).
> 3. Generate 20 test questions from these documents (4 per document), where each question has a known answer that is contained in a specific chunk. Record the ground-truth chunk IDs.
> 4. For each question, retrieve top-5 chunks. Score recall@5: how often does the correct chunk appear in the top 5?
> 5. Now create a second version: for each chunk, prepend a one-sentence contextual description ("This chunk is from [document name] and covers [topic]"). Re-index. Re-run the same 20 questions. Report recall@5 again.
>
> Report: the 20 questions, the baseline recall@5, the contextual-prefix recall@5, and 3 questions where the prefix changed the result.

You're looking for two things: a concrete recall number showing the gap (expect 5–20 percentage points in favor of contextual prefixes), and specific examples of questions where the prefix made the difference — usually questions where the answer phrase is common across documents and the context disambiguates which document the question is about.

### Part B — Manual long-context vs. RAG comparison (Claude.ai)

Open Claude.ai. You'll run four separate conversations.

**Preparation:** Copy a real 5,000-word document you have access to — a company policy, a product specification, a research paper, a long email thread. This is your "corpus."

**Conversation 1 (long context, full document):** Paste the full document into Claude.ai and ask three questions — one where the answer is in the first quarter of the document, one where it's in the middle, and one where it's at the end.

**Conversation 2 (simulated RAG, manually retrieved):** Read the document yourself and find the 2–3 paragraphs that are most relevant to each question. Paste only those paragraphs into Claude.ai as "retrieved context," then ask the same three questions.

**What to observe:** For the first question (answer in the first quarter), both approaches should perform similarly. For the middle question, check whether the full-document version is actually using the correct paragraph or confabulating. For the end question, the full-document version may do fine if the ending paragraph gets recency attention, or may miss it.

This is not a controlled experiment. It's a calibration exercise — you're developing the sensory discrimination to distinguish "model answered from the right context" from "model answered from a plausible approximation." That discrimination is a skill that pays off when you're debugging a live RAG system.

---

## Problem set

**Problem 1 — Retrieval failure diagnosis (paper position required)**

You're building RAG over a 50,000-document legal case archive. A user queries "cases where the defendant argued statute of limitations under UCC 2-725." Your system has high retrieval recall@20 on general legal queries but low faithfulness. Read Anthropic's Contextual Retrieval post in full, then write a one-paragraph argument for whether contextual prefixes would help in this specific case, or whether the failure mode is elsewhere. Defend your position: is this a chunking problem, a faithfulness problem, or a retrieval signal problem? What would you measure first?

**Problem 2 — Chunking design on paper**

You are building a RAG system over a 3,000-document product documentation corpus. Documents range from 500-word API reference stubs to 15,000-word architectural guides. Query types: (a) "how do I authenticate with OAuth2?" — highly specific, low ambiguity; (b) "what are the tradeoffs between the synchronous and async API?" — requires synthesis across multiple sections; (c) "what changed in version 3.2?" — changelog lookup, specific version number. Design a chunking and retrieval strategy for this corpus. Do not pick one strategy for all three query types. Be specific: chunk sizes, overlap, whether parent-child applies, which retrieval method fits each query type.

**Problem 3 — NoLiMa result interpretation (requires reading the paper)**

Read the abstract and results section of NoLiMa (arxiv 2502.05167). The key finding is that models drop below 50% of their short-context baseline at 32K tokens for non-lexical retrieval. Your colleague argues: "This proves RAG is better than long context." Write a 200-word response that engages with what the result actually shows, what it doesn't show (it says nothing about generation quality given correct retrieval), and what additional experiment you would need to run to settle the "RAG vs long context" debate for a specific production use case.

**Problem 4 — Eval harness design for a specific domain**

You are the AI lead for a research intelligence firm that uses RAG to answer questions about pharmaceutical clinical trials from SEC filings and FDA submissions. Build an eval plan — not the code, the plan — that covers: (a) how you generate the synthetic query-answer ground-truth set, (b) which three RAGAS metrics you would prioritize and why, (c) one failure mode that RAGAS would not catch (think about medical claim hallucination where the retrieved context is technically correct but incomplete), and (d) how you'd catch that failure mode in production.

**Problem 5 — Production chunking failure post-mortem**

A team built a RAG system for a marketing agency's client intelligence database. The database has campaign briefs, creative strategy documents, brand guidelines, and competitive analysis reports. After launch, they found: high faithfulness scores but consistently wrong answers on questions about "brand voice" and "tone of voice guidelines." Their chunking is fixed-size at 400 tokens with 50-token overlap. Diagnose the failure mode. What is the most likely cause? What is your fix, and what metric tells you whether the fix worked?

---

## Common failure modes at scale

**Failure 1 — The "it works in the demo" gap.** Demo testing is selection-bias testing. You test the queries that inspired the system, not the queries users actually send. A customer support RAG system at a SaaS company showed 92% accuracy in demo testing and 61% accuracy against the first 1,000 production queries. The gap: product names had changed in recent releases, but the document index hadn't been updated. Keyword queries for the new product names returned nothing; the system fell back to semantic similarity and retrieved documents about the old product. Fix: measure lexical retrieval coverage (BM25 recall) separately from semantic recall; flag queries where both methods return below a confidence threshold.

**Failure 2 — Retrieval precision collapse under high corpus volume.** A legal research firm built RAG over 200,000 case documents. At corpus size 10,000, recall@10 was 81%. At 200,000, it fell to 58%, with no changes to chunking or retrieval. The cause: at 10,000 documents, the top-10 results were mostly relevant. At 200,000, the first-stage retrieval was returning 10 documents from a pool 20x larger, and the ranking signal was too noisy to maintain precision. Fix: add a reranker pass. With Cohere Rerank 4 on top of the first-stage results, recall@10 recovered to 74%. The remaining gap: some case law used archaic legal terminology not present in the embedding vocabulary. Fix (partial): hybrid retrieval with BM25 covering archaic terminology.

**Failure 3 — Context assembly order destroying generation quality.** A financial intelligence team found that their LLM was consistently citing the wrong source when multiple documents covered the same topic. The bug: retrieved chunks were assembled in retrieval rank order, so rank-1 was placed first. But their documents included both primary sources (10-K filings) and secondary sources (analyst reports). When an analyst report paraphrasing a 10-K ranked higher than the 10-K itself, the LLM cited the paraphrase, not the original. Fix: metadata-aware assembly. Primary sources always front-load; secondary sources are appended only when primary sources don't contain the answer.

**Failure 4 — Faithfulness gaming by the LLM.** A team was measuring faithfulness using RAGAS and saw scores above 0.9. Then a compliance officer reviewed 50 answers and flagged 12 as inaccurate. The problem: the LLM was generating answers that contained claims supported by the retrieved context, plus additional parametric-memory claims that were plausible extensions of the context. RAGAS was scoring the supported claims correctly, but the unsupported extensions were slipping through because they were adjacent to supported claims in the same sentence. Fix: decompose answers into atomic sentence-level claims before scoring faithfulness; don't score a claim as supported if it extends beyond what's explicitly stated in the context.

---

## Open questions — what's not settled

**1. At what corpus size does Contextual Retrieval's cost-benefit calculation break?** Anthropic's published evaluation covers moderate-size corpora. For a corpus that requires daily re-indexing of millions of documents, the cost of running Claude Haiku on every chunk to generate contextual prefixes is a real engineering decision. No published study has characterized the crossover point where the recall improvement from contextual prefixes no longer justifies the indexing cost relative to alternatives (better base embeddings, query expansion, or expanded reranking candidate sets).

**2. Does reranking quality degrade on domain-specific retrieval that's far from the reranker's training distribution?** Cohere Rerank 4 and Voyage rerank-2 are trained on broad retrieval benchmarks. For highly specialized corpora — cuneiform academic translations, genomics literature, niche regulatory frameworks — the reranker's relevance judgments may be poorly calibrated. The benchmark numbers (93 datasets for Voyage rerank-2) are broad but not universal. This is an empirical question for each new deployment domain, not a resolved one.

**3. How should RAG systems handle temporally conflicting retrieved documents?** If a RAG system retrieves a 2022 policy document and a 2024 policy update that contradicts it, and both are relevant to the query, the correct behavior is not obvious. A high-faithfulness LLM response stays within the retrieved context — but which document does it treat as authoritative? Current RAGAS metrics do not measure temporal consistency or conflict resolution. This is an open problem in production RAG design.

---

## Reviewer lens — specific technical disagreements with this lesson

**Disagreement 1 — The BM25 vs. embeddings empirical comparison is not clean.** This lesson cites Jason Liu's observation that "full text search and embeddings basically performed the same, except full text search was about 10 times faster" on his essay corpus.[^2] Liu himself acknowledges the corpus is his own writing, which has relatively consistent vocabulary and style. On corpora with high vocabulary mismatch between queries and documents (jargon-heavy technical docs, domain-specific abbreviations), embedding retrieval consistently outperforms BM25. Citing this number as a general result is a generalization the original text doesn't support. A more careful framing: for query-to-document vocabulary match, BM25 is competitive; for vocabulary gap, embeddings are necessary; for production systems, measure both.

**Disagreement 2 — The "Lost in the Middle" result is dated relative to current frontier models.** Liu et al. 2023 documented degradation in models available in 2023 — GPT-3.5, GPT-4, and Claude 2 variants. Anthropic and Google have trained subsequent models with explicit long-context attention modifications. The lesson applies the lost-in-the-middle heuristic as a current design constraint, which may be over-conservative for the current frontier generation (Claude Sonnet 5 / Fable 5, Gemini 3.x). The honest position: Context Rot (Chroma, July 2025) showed the phenomenon persisting well after the original 2023 study, but the degree of degradation is model-specific and no equivalent public study covers the mid-2026 frontier. Treat the context placement heuristic as a reasonable default, not an iron law — and measure it on your target model.

**Disagreement 3 — The RAGAS faithfulness metric has a documented gaming problem this lesson underplays.** The lesson's "common failure modes" section mentions faithfulness gaming, but the framing makes it sound like an edge case. In practice, RAGAS faithfulness scores are routinely inflated by LLMs that are trained to sound grounded. Hamel Husain, in his evaluation-driven development work with production teams, has consistently flagged RAGAS faithfulness as a weak signal that requires supplementation with LLM-as-judge on adversarial claim sets, not a number to be reported without qualification. A lesson teaching RAGAS as a primary eval framework should name this limitation more centrally, not in the failure modes section.

**Disagreement 4 — Contextual Retrieval's 67% improvement figure includes the reranking stage, which is a separate engineering decision.** The headline number most practitioners cite from Anthropic's post is "67% reduction in failure rate." That number requires adding a reranker after contextual retrieval. The isolated improvement from contextual retrieval (no reranker) is 49%. Teams who implement contextual prefixes without a reranker and expect 67% improvement are misreading the experimental design. This lesson states the numbers correctly but should make the experimental condition more prominent, not footnote it.

---

## Further reading

**Must-read (read before building your first production RAG system):**

- Anthropic, "Introducing Contextual Retrieval" (September 2024). The methodology, numbers, and prompt-caching optimization in one place. [https://www.anthropic.com/news/contextual-retrieval](https://www.anthropic.com/news/contextual-retrieval)
- Jason Liu, "Systematically Improving Your RAG" (May 2024). The 6-step diagnostic methodology — this is the operational companion to the theory in this lesson. [https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/](https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/)
- Hsieh et al., "RULER: What's the Real Context Size of Your Long-Context Language Models?" (NVIDIA / COLM 2024). Read Sections 1–3 and Table 2. This is the benchmark that exposes why NIAH scores are misleading. [https://arxiv.org/abs/2404.06654](https://arxiv.org/abs/2404.06654)

**Recommended:**

- NoLiMa, "Long-Context Evaluation Beyond Literal Matching" (Adobe Research / ICML 2025). Read the abstract and Figure 3 (performance by context length). [https://arxiv.org/abs/2502.05167](https://arxiv.org/abs/2502.05167)
- Chroma Research, "Context Rot" (July 2025). Empirical degradation across 18 models. Essential if you're deciding between RAG and long-context for a new system. [https://research.trychroma.com/context-rot](https://research.trychroma.com/context-rot)
- Jason Liu, "How to Build a Terrible RAG System" (January 2024). Read this for the anti-patterns. [https://jxnl.co/writing/2024/01/07/inverted-thinking-rag/](https://jxnl.co/writing/2024/01/07/inverted-thinking-rag/)
- Cohere, "Introducing Rerank 4" (December 2025). The current Cohere flagship: variants, 32K context, deployment options. [https://cohere.com/blog/rerank-4](https://cohere.com/blog/rerank-4)
- MongoDB / Voyage AI, "rerank-2.5 and rerank-2.5-lite: Instruction-Following Rerankers" (August 2025). The current Voyage generation and what instruction-steered relevance buys. [https://www.mongodb.com/company/blog/product-release-announcements/rerank-2-5-and-rerank-2-5-lite-instruction-following-rerankers](https://www.mongodb.com/company/blog/product-release-announcements/rerank-2-5-and-rerank-2-5-lite-instruction-following-rerankers)

**Optional (historical grounding):**

- Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" (NeurIPS 2020). The paper that named the paradigm. The specific architecture (BART + DPR) is dated, but the parametric/non-parametric framing is still the right mental model. [https://arxiv.org/abs/2005.11401](https://arxiv.org/abs/2005.11401)
- Liu et al., "Lost in the Middle" (Stanford / TACL 2024). The original documentation of context placement effects. Read Section 3 if you want the empirical tables. [https://arxiv.org/abs/2307.03172](https://arxiv.org/abs/2307.03172)

---

## Citations

[^1]: Lewis, P., Perez, E., Piktus, A., Petroni, F., Karpukhin, V., Goyal, N., ... & Kiela, D. (2020). Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks. *Advances in Neural Information Processing Systems 33 (NeurIPS 2020)*. https://arxiv.org/abs/2005.11401 — Supports: the parametric/non-parametric memory framing and the historical origin of RAG as a named paradigm.

[^2]: Liu, J. (2024, May 22). Systematically Improving Your RAG. *jxnl.co*. https://jxnl.co/writing/2024/05/22/systematically-improving-your-rag/ — Supports: the observation that full text search and embeddings performed comparably on essay corpora with BM25 being 10x faster. Liu's note: test on your own corpus before assuming which wins.

[^3]: Brenndoerfer, M. (2024). Hybrid Retrieval: Combining Sparse and Dense Methods for Effective Information Retrieval. *mbrenndoerfer.com*. https://mbrenndoerfer.com/writing/hybrid-retrieval-combining-sparse-dense-methods-effective-information-retrieval — Supports: Natural Questions BM25/dense/hybrid recall figures and BEIR nDCG@10 improvement from hybrid retrieval.

[^4]: Anthropic. (2024, September 19). Introducing Contextual Retrieval. *anthropic.com/news*. https://www.anthropic.com/news/contextual-retrieval — Supports: all four quantitative results (5.7% baseline, 3.7% embeddings only, 2.9% hybrid, 1.9% with reranking); methodology of LLM-generated contextual prefixes; prompt caching cost figures.

[^5]: Liu, J. (2024, January 7). How to Build a Terrible RAG System. *jxnl.co*. https://jxnl.co/writing/2024/01/07/inverted-thinking-rag/ — Supports: the inversion framing of RAG design anti-patterns; fixed-size chunking as the canonical wrong default.

[^6]: Liu, J. (2025, January 24). Systematically Improving RAG Applications. *jxnl.co*. https://jxnl.co/writing/2025/01/24/systematically-improving-rag-applications/ — Supports: the diagnosis pattern (understand query segments before choosing retrieval method); the observation that teams tune prompts while ignoring retrieval; the flywheel methodology from evaluation to improvement.

[^7]: Voyage AI. (2024, September 30). rerank-2 and rerank-2-lite: the next generation of Voyage multilingual rerankers. *blog.voyageai.com*. https://blog.voyageai.com/2024/09/30/rerank-2/ — Supports: Voyage rerank-2 accuracy improvement of 13.89% average across 93 retrieval datasets; 2.3x improvement vs. Cohere rerank-english-v3; 16K context window for rerank-2.

[^8]: Liu, N.F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., & Liang, P. (2024). Lost in the Middle: How Language Models Use Long Contexts. *Transactions of the Association for Computational Linguistics, 12*, 157–173. https://arxiv.org/abs/2307.03172 — Supports: U-shaped performance curve in long-context models; performance degradation when relevant information is in the middle of context; implications for context assembly ordering.

[^9]: Es, S., James, J., Anke, L.E., & Schockaert, S. (2023). RAGAS: Automated Evaluation of Retrieval Augmented Generation. *EACL 2024*. https://docs.ragas.io/en/stable/ — Supports: RAGAS faithfulness, answer correctness, and context recall metric definitions; the F1-based answer correctness calculation; the LLM-as-judge approach to faithfulness decomposition.

[^10]: Hsieh, C.P., Sun, S., Kriman, S., Acharya, S., Rekesh, D., Jia, F., Zhang, Y., & Ginsburg, B. (2024). RULER: What's the Real Context Size of Your Long-Context Language Models? *COLM 2024*. https://arxiv.org/abs/2404.06654 — Supports: multi-hop tracing and aggregation tasks exposing performance gaps beyond NIAH; only half of models claiming 32K context maintained satisfactory performance at 32K on RULER's harder tasks.

[^11]: Adobe Research. (2025, February). NoLiMa: Long-Context Evaluation Beyond Literal Matching. *ICML 2025*. https://arxiv.org/abs/2502.05167 — Supports: performance degradation on non-lexical retrieval at 32K tokens; 11 models dropping below 50% of short-context baseline; CoT prompting failing to close the gap; the attention-mechanism explanation for the degradation.

[^12]: Chroma Research. (2025, July). Context Rot: How Increasing Input Tokens Impacts LLM Performance. *research.trychroma.com*. https://research.trychroma.com/context-rot — Supports: context rot empirically confirmed in 2025 frontier models (Claude 4, GPT-4.1, Gemini 2.5); three contributing mechanisms (lost-in-the-middle, attention dilution, distractor interference); degradation observed before context window saturation.

[^13]: Cohere. (2025, December 11). Introducing Rerank 4. *cohere.com/blog*. https://cohere.com/blog/rerank-4 — Supports: Rerank 4 release date, rerank-4-pro / rerank-4-fast variants, 32K context window (4x Rerank 3.5), 100+ languages, self-learning relevance adaptation. See also https://venturebeat.com/ai/coheres-rerank-4-quadruples-the-context-window-to-cut-agent-errors-and-boost. Verified 2026-07-17.

[^14]: MongoDB / Voyage AI. (2025, August 11). rerank-2.5 and rerank-2.5-lite: Instruction-Following Rerankers. https://www.mongodb.com/company/blog/product-release-announcements/rerank-2-5-and-rerank-2-5-lite-instruction-following-rerankers — Supports: 32K context (2x rerank-2), first instruction-following rerankers, +11.48% average accuracy from instructions (rerank-2.5), accuracy gains over Cohere Rerank v3.5; MongoDB acquisition context. Verified 2026-07-17.

[^15]: byteiota. (2026). RAG vs Long Context 2026: Is Retrieval Really Dead? https://byteiota.com/rag-vs-long-context-2026-retrieval-debate/ — Supports: the January 2026 viral "RAG is dead" wave and the resolution into "naive RAG is dead; sophisticated/agentic RAG is thriving." See also LightOn, "RAG is Dead, Long Live RAG: Retrieval in the Age of Agents," https://lighton.ai/lighton-blogs/rag-is-dead-long-live-rag-retrieval-in-the-age-of-agents. Verified 2026-07-17.
