---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 4
day_name: thu
session_slug: basecamp-part-1-prompting-rags
date_due: 2026-04-30
tags: [rag, failure-modes, long-context, retrieval, benchmarks, agentic-rag, production, lost-in-middle, nolima, ruler, gemini, claude, gpt-4-1]
sources:
  - liu-2023-lost-in-middle
  - hsieh-2024-ruler-nvidia
  - nolima-2025-icml
  - gemini-1-5-paper-2024
  - llamaindex-long-context-rag-2024
  - llamaindex-rag-dead-agentic-2025
  - anthropic-contextual-retrieval-2024
  - anthropic-multi-agent-research-2025
  - databricks-long-context-rag-2024
  - factum-citation-hallucination-2026
last_verified: 2026-04-15
word_count_target: 6500
---

# RAG failure modes and the long-context debate — where retrieval breaks in production, and whether 1M-token windows fix it or just move the problem

## Why this matters

If you have shipped or designed a RAG system — a document chatbot, an internal knowledge base query tool, a research assistant — there is a ceiling you will hit that no amount of prompt tweaking clears: the system confidently gives wrong answers, retrieves the wrong chunks, ignores relevant material that was three paragraphs away from the retrieved chunk, or fabricates a citation that sounds completely plausible.

These are not random failures. They are *structural* failures with known mechanisms. And in 2024 and 2025, the field had a very public argument about whether the solution was to fix retrieval or to throw it away and just stuff your entire corpus into a 1M-token context window.

The "long-context kills RAG" crowd had a case. The "RAG is evolving, not dying" crowd also had a case. Both positions were held by smart people building real systems. This lesson makes you able to take a *position* on that argument, grounded in the benchmarks, the costs, and the failure modes on both sides — not just recite both views.

Specifically: after today you can walk into a product decision with a legal team (hundred-thousand-document corpus), a customer support engineering team (three years of ticket history), or a research organization (PubMed-scale literature) and give them a defensible answer for which architecture to reach for *first*, what will break when it does, and how to measure it.

## Prerequisites

- Wednesday's lesson (RAG as a system — chunking, embedding, retrieval, generation loop) or equivalent mental model. This lesson takes the pipeline as a known starting point and attacks its failure modes.
- Familiarity with what context windows are and what "tokens" means at the operational level.

---

## Part 1: A taxonomy of RAG failures — seven named failure modes, each with mechanism

Most practitioners think RAG failure = "bad retrieval." That is one failure among seven, and not always the most dangerous one. Here they are by mechanism.

### 1. Retrieval miss

The right chunk is not in the top-k results. The query embedding is too semantically distant from the chunk embedding, even though the chunk is the correct answer.

**Mechanism:** Embedding models compress meaning into high-dimensional vectors, but semantic compression is lossy. A query phrased as "What is our policy on contractor termination?" may not fire strongly against a chunk that says "The consultant engagement may be ended by either party per Section 4.2." Same meaning, different vocabulary — the cosine similarity is lower than a chunk about "employee termination procedures" that is technically wrong for contractors.

This is the **query-document mismatch** failure. It is exacerbated by asymmetric training data: most embedding models were trained on web text where queries and documents are written in similar registers. Legal, medical, and internal company language routinely violates this assumption.

Anthropic's Contextual Retrieval paper (September 2024) reports that context-blind chunking — chunks that omit their document-level context — causes retrieval failures in approximately 35–40% of queries on technical corpora.[^1] The fix they propose (prepending a short LLM-generated context blurb to each chunk before embedding) reduces top-20 retrieval failures by 49%, and by 67% when combined with a reranker. **But note the caveat buried in their methodology:** the eval corpus is five domains of moderate-size technical documents. The result almost certainly does not transfer directly to 100M-token legal archives, where document diversity and query specificity both increase dramatically, and where the cost of generating contextual blurbs at indexing time becomes non-trivial.

### 2. Chunk boundary loss

The answer spans two chunks. Neither chunk is independently sufficient, but together they would be. The retriever returns one and not the other.

**Mechanism:** Fixed-stride chunking (e.g., 512 tokens with 128-token overlap) is a heuristic that does not know where meaning breaks. A legal contract's key obligation may begin in the last 50 tokens of one chunk and conclude in the first 80 tokens of the next. The retriever scores each chunk against the query independently; the relevant sentence pair is never co-located in a single retrieved unit.

This failure is not solved by better embeddings. It is solved by better chunking — hierarchical structures (sentences nested inside paragraphs nested inside sections), sentence-window retrieval (retrieve the matching sentence, expand to its surrounding paragraph before passing to the generator), or document-level indexing with in-document search at generation time.

### 3. Distractor dominance

The retrieved top-k includes chunks that are superficially similar to the query but factually wrong or misleading for the specific question. The generator reconciles the contradiction incorrectly, usually by averaging or by deferring to the wrong chunk.

**Mechanism:** This is the inverse of retrieval miss. The embedding model fires on the wrong thing. The generator then has to reason across conflicting evidence under pressure to produce a coherent answer. Most generators will confabulate a synthesis rather than surface the contradiction explicitly. The output looks confident and is wrong.

This failure is particularly vicious in domains with version history — internal policy documents, legal codes with amendments, medical guidelines with updates. A query about "current policy on X" may retrieve three versions of the policy. The generator does not know which is current. It produces an answer that is a blend of all three.

### 4. Over-retrieval (noise floods context)

The top-k is too high. You retrieve 20 chunks trying to cover edge cases. But 14 of them are noise, and the generator's attention is now distributed across irrelevant material. Answer quality degrades.

This is the mechanism behind Liu et al.'s "Lost in the Middle" (2023, published in TACL 2024): performance on multi-document question answering is highest when the relevant document is at the beginning or end of the context window, and degrades significantly when it is in the middle — even with models explicitly designed for long contexts.[^2] The finding generalizes: more context is not always better context. Precision matters more than recall once you cross the "enough relevant signal" threshold.

The practical consequence: systems that default to top-20 retrieval trying to be safe are often outperformed by well-tuned top-5 retrieval. More chunks is not more information — it is more distraction.

### 5. Citation fabrication

The generator cites a source that does not exist or cites a real source for a claim it does not actually support.

This failure is often treated as a hallucination problem, separate from retrieval. It is not. It is a *grounding failure* at the generation stage: the model has the retrieved chunks in context, but it is not attending to them faithfully when generating the citation. Instead, it is pattern-completing to the expected output format of "answer + citation."

The numbers here are alarming and domain-specific. A 2025 study published in the *Journal of Empirical Legal Studies* found hallucination rates of 17% for Lexis+ AI, 33% for Westlaw AI-Assisted Research, and 43% for GPT-4 on legal research tasks — all of these are RAG-enabled systems.[^3] A 2025 paper on reference hallucination in commercial LLMs and deep research agents found that even search-grounded systems fabricate 3–13% of URLs cited.[^4] FACTUM (2026), a mechanistic study of citation hallucination in long-form RAG, found that 57% of citations in a RAG-optimized model showed unfaithful behavior — the cited source did not actually support the claim made.[^5]

The clean-corpus assumption that underlies most RAG evals ("if we give the model the right chunks, it will cite them correctly") breaks down in production because generators are not perfect copiers. They compress, paraphrase, and when paraphrasing fails, they hallucinate the citation anchor rather than admit they cannot ground the claim.

### 6. Freshness lag

The retrieval index reflects the state of your knowledge base at indexing time. If the corpus changes — new contracts filed, updated policies, revised drug interaction data — the index is stale until reindexed.

**Mechanism:** This is not a model failure. It is a systems failure. But it surfaces as a model failure when users ask queries that depend on recent updates. The more frequently your corpus changes and the higher the stakes of stale information (legal, regulatory, medical), the more critical your reindexing cadence becomes. Most production systems underinvest in this.

The operational fix is incremental indexing with clear freshness metadata, and routing queries about "current" or "latest" state through a freshness filter that boosts recently indexed chunks. The deeper fix is surfacing staleness risk explicitly in the generated answer: "This answer is based on documents indexed as of [date]."

### 7. Query-document mismatch (semantic register gap)

Covered partially under retrieval miss, but worth naming separately: the user writes a query in conversational language; the corpus is written in formal, domain-specific, or technical language. The embedding model was trained on a distribution that underrepresents either the query register or the document register.

**Production example:** Customer support logs are written in CRM shorthand ("cust reported 404 on /checkout per order #12345"). A user asking "why do customers get errors at checkout?" in natural language may not retrieve those logs effectively, even though they contain exactly the relevant information. The mismatch is not at the semantic level — it is at the register and format level.

Query rewriting (generating multiple query variants before retrieval) and HyDE (Hypothetical Document Embeddings — generate what the ideal answer document would look like, then embed that for retrieval) are the two most commonly deployed mitigations.[^6]

---

## Part 2: The benchmarks that settled (and unsettled) the debate

### NIAH and why it was misleading

Needle-in-a-Haystack (NIAH) became the standard long-context eval in 2023–2024. The setup: bury a specific sentence in a long document, ask the model to retrieve it. Gemini 1.5 Pro scored 99%+ recall at 1M tokens on this test.[^7] GPT-4o scored near-perfectly. Claude scored near-perfectly. The press release interpretation was: "Long-context models can use all their context. RAG is obsolete."

This interpretation was wrong, and two papers in 2024–2025 demonstrate exactly why.

### RULER (NVIDIA, April 2024)

Cheng-Ping Hsieh and colleagues at NVIDIA published RULER: *What's the Real Context Size of Your Long-Context Language Models?* (arXiv:2404.06654).[^8] RULER extends the vanilla NIAH test with harder variants:

- Multiple needles (retrieve 2, 3, or 4 sentences, not just one)
- Variable distractor types (semantically related distractors, not just random text)
- Multi-hop tracing (retrieve entity A's property, use it to find entity B)
- Aggregation tasks (find all instances of a pattern, count them)
- Question answering over retrieved content

Key finding: **models that score near-perfect on vanilla NIAH show large degradation on RULER tasks as sequence length increases.** Among models claiming 32K+ context, only half maintained satisfactory performance at 32K on RULER's harder tasks. Yi-34B, which claimed 200K context support, showed "large room for improvement" as length and task complexity increased. The conclusion: claimed context sizes are marketing numbers calibrated to vanilla NIAH. Real-task performance drops much earlier.

### NoLiMa (Adobe Research, February 2025 / ICML 2025)

*NoLiMa: Long-Context Evaluation Beyond Literal Matching* (arXiv:2502.05167) is the more pointed paper.[^9] The core insight: NIAH is gameable because the needle and the query share literal text overlap. A model can find "the secret code is 42901-B" by doing something that approximates keyword search on the attention pattern. It does not need to *understand* the needle; it just needs to *locate* the literal string.

NoLiMa constructs needle/query pairs with **minimal lexical overlap** — the model must infer a latent association to answer. For example, the needle might describe a historical figure's role without using their name, and the query asks about that person by name. The model cannot exploit literal matching; it must reason about the connection.

Results: **13 popular LLMs tested, all claiming 128K+ context support. At 32K tokens, 11 of 13 dropped below 50% of their short-context baseline.** GPT-4o, the top performer, fell from 99.3% accuracy at short contexts to 69.7% at longer ones. Models with chain-of-thought reasoning struggled equally.

The mechanism the authors identify: the attention mechanism, when scanning a long context, finds literal matches as shortcuts. When those shortcuts are absent, it must do actual semantic inference across distance — and this gets harder as the haystack grows, because the signal-to-noise ratio in the attention computation decreases. This is not a prompt engineering problem. It is a fundamental property of how transformers attend.

**What this means for the "just stuff the context" argument:** If your user queries are literal ("find the sentence about X"), NIAH-type recall stays high even at 1M tokens. If your queries require *reasoning* about the context — synthesis, comparison, multi-hop inference, "what does this imply about Y?" — NoLiMa predicts significant degradation at extended contexts. Most interesting enterprise queries are in the second category.

---

## Part 3: The long-context models — what they actually do and where they break

### Current specs (April 2026)

| Model | Max context | Notes |
|---|---|---|
| Claude Opus 4.6 | 1M tokens GA | $5/$25 per M tokens in/out; 78.3% MRCR v2 |
| Claude Sonnet 4.6 | 1M tokens GA | $3/$15 per M tokens in/out |
| Gemini 2.5 Pro | 1M tokens (2M forthcoming) | 99.7% recall at 1M on NIAH; 100% recall to 530K |
| GPT-4.1 | 1M tokens | $2/$8 per M tokens in/out; released April 2025 |

[^10] [^11] [^12]

All four models now support 1M tokens at standard pricing. This is a real milestone — twelve months ago, 1M context was a beta feature with a price multiplier. The question is not whether these models *can* hold 1M tokens. They can. The question is whether they *use* that context well on real tasks.

### What long-context models do well

**Single-document comprehension.** Ask Gemini 2.5 Pro or Claude Opus 4.6 to summarize, extract, or reason about a single 200-page document — it performs excellently. The full document is in context; there is no retrieval miss, no chunk boundary loss, no distractor. This is the use case where long context genuinely replaces RAG.

**Literal recall.** NIAH-style "find me the specific clause that says X" across a 500K-token contract. High recall, fast, no retrieval pipeline to maintain.

**Fixed corpus, infrequent queries.** If you have a stable corpus (e.g., a single company's legal framework, a product's technical spec) and query it rarely enough that per-query cost is acceptable, context-stuffing is simpler to build and maintain than a RAG pipeline.

### Where long-context models break

**Multi-hop inference at scale.** Exactly the NoLiMa result: when the answer requires chaining two or three pieces of information that are far apart in the context and have no literal text overlap, accuracy degrades sharply beyond 32K–64K tokens, even on frontier models.

**Over 32K practical performance.** The Databricks benchmark (November 2024, arXiv:2411.03538) tested 20+ models on real RAG datasets (Databricks DocsQA, FinanceBench, NaturalQuestions) with context lengths from 2K to 2M tokens.[^13] Key finding: most models' performance *decreases* after a context-length optimum that is far below their advertised limit. Llama-3.1-405B degraded after 32K tokens; GPT-4-0125-preview after 64K. Longer context at that point hurt answer quality.

**Freshness.** If you are stuffing the full corpus, updating requires re-ingesting the full corpus on every query or on every corpus change. That is operationally equivalent to maintaining no index at all — just reprocessing everything each time. For corpora that change daily (customer tickets, news, regulatory filings), this is impractical.

**Cost at scale.** This is the decisive argument in most production settings. See Part 4.

---

## Part 4: The cost argument — concrete numbers

This is not a theoretical tradeoff. Here are the numbers.

**Setup:** You have a corpus of 100K tokens (roughly 200 pages of dense text — a medium-size legal brief, a quarter of technical documentation, three months of customer support tickets). A user asks one question. Claude Sonnet 4.6 at $3/M input tokens.

| Approach | Input tokens | Cost per query |
|---|---|---|
| Context stuffing (full corpus) | ~100,000 | $0.30 |
| RAG, top-5 chunks (avg 500 tokens each) | ~2,500 + 200 system | $0.008 |
| RAG, top-20 chunks | ~10,000 + 200 | $0.031 |

That is a **37x cost difference** between context-stuffing and optimized RAG on a 100K-token corpus. The gap grows linearly with corpus size. At 1M tokens, the difference is $3.00 per query vs $0.008 — a **375x** difference.

For an internal chatbot serving 1,000 queries per day against a 1M-token corpus:

| Approach | Daily cost | Annual cost |
|---|---|---|
| Context stuffing (1M tokens/query) | $3,000 | $1.1M |
| Optimized RAG (top-5) | $8 | $2,920 |

The latency gap is equally stark. 1M-token context requests can exceed 20–30 seconds for the first token response on current infrastructure. A RAG pipeline retrieving 5 chunks and calling the API with a 2,500-token prompt runs in 1–3 seconds.

**The escape clause:** These numbers assume you are paying per-token via API. Some enterprise deployments license models at flat rates, which changes the math. Anthropic has moved toward flat-rate long-context pricing for enterprise tiers, which makes context-stuffing more attractive if you already have a license commitment.[^14] But at API rates — which is what most builders face — the cost argument for RAG remains strong.

**The hybrid point:** LlamaIndex's Jerry Liu, in the March 2024 "Towards Long Context RAG" post, argued that the right frame is not RAG-vs-long-context but *which architecture for which query type*.[^15] Simple factual lookups ("what does clause 4.2 say?") are well served by long-context stuffing if you can afford it. Complex synthesis queries ("compare the indemnification provisions across these 30 contracts") require agentic multi-step retrieval regardless of context window size, because no single retrieval pass surfaces everything relevant. This is the position that held up best as the field evolved through 2024–2025.

---

## Part 5: Agentic RAG — what it is, why it matters, where it breaks

By mid-2025, the dominant pattern at the frontier was neither naive RAG nor raw context-stuffing. It was **agentic RAG**: a multi-step process where the retrieval strategy is itself controlled by a reasoning agent.

LlamaIndex published "RAG is dead, long live agentic retrieval" (2025), marking the explicit end of naive top-k RAG as the production default.[^16] Anthropic published a detailed engineering post on their own multi-agent research system (June 2025), describing an orchestrator-worker architecture where a Lead Researcher agent directs subagents to perform targeted retrieval, synthesize partial results, and re-query when gaps are identified.[^17] The result: 90% reduction in research time for complex queries; 90.2% better than a single Opus 4 on internal benchmarks.

### What agentic RAG adds

**Query decomposition.** A complex user question is broken into sub-questions. Each sub-question retrieves independently. The generator synthesizes across all sub-results. This handles multi-hop queries that a single retrieval pass misses.

**Query rewriting.** Before retrieval, the agent generates 2–5 query variants (different phrasings, different keyword emphasis, a HyDE-style hypothetical answer). Each variant retrieves independently; results are merged. This directly attacks the query-document mismatch failure mode.

**Iterative refinement.** After a first retrieval+generation pass, the agent evaluates whether the answer is complete. If not, it formulates a follow-up query targeting the identified gap. This loop continues until confidence is high or a budget is exhausted.

**Tool-augmented retrieval.** The agent can call structured lookups (SQL queries, metadata filters, date-range filters) alongside semantic search, then combine results. This handles freshness lag better than pure semantic retrieval.

### Where agentic RAG breaks

Agentic RAG is not a free lunch. The survey paper (arXiv:2501.09136, January 2025) identifies the predictable failure modes of agentic retrieval systems.[^18] Three are critical:

**Planning failures.** The orchestrator agent misdiagnoses what is needed and issues irrelevant sub-queries. This is a direct descendant of the query-document mismatch failure, now at the orchestrator level instead of the retriever level. A bad planner compounds errors across multiple retrieval calls.

**Tool loop explosion.** Iterative refinement without a hard stop on retrieval iterations will loop indefinitely on hard questions. In Anthropic's engineering post, they describe designing explicit loop-termination criteria and budget limits as a primary engineering challenge. Without these, an agentic system can run $10 of retrieval+generation to answer a simple question.

**Latency compounding.** Each additional retrieval-and-synthesis loop adds latency. Three-hop agentic RAG can take 15–30 seconds for complex queries even with optimized chunking and fast models. This is comparable to or worse than context-stuffing latency for user-facing applications.

The practical implication: agentic RAG is appropriate for *asynchronous* research tasks (generate a report, analyze a corpus, prepare a briefing) but not for real-time user-facing applications where a user is waiting for a response.

---

## Part 6: The live debate — taking a position

The debate as it stood in 2024: Jerry Liu and the LlamaIndex position vs. the "just stuff the context" crowd, which included early Gemini 1.5 boosters and several YC companies who shipped context-stuffing products.

**The "stuff the context" argument (strongest version):** Retrieval introduces irreducible failure modes — retrieval miss, chunk boundary loss, distractor dominance — that context-stuffing avoids entirely. If the entire corpus fits in the context window and the model attends to it accurately, none of those failure modes apply. NIAH at 99%+ recall on 1M tokens proves the model can find things.

**The "RAG is not dead" rebuttal (strongest version):** NIAH is the wrong benchmark. NoLiMa and RULER show that real task performance degrades at 32K–64K tokens even on frontier models, far below the context limit. The "model can hold 1M tokens" claim is not the same as "model reasons accurately over 1M tokens." Cost at scale makes context-stuffing economically unviable for corpora that change or systems that see high query volume. And agentic RAG — when properly architected — outperforms naive context-stuffing on complex synthesis queries because it can target retrieval to exactly what is needed.

**My position:** Agentic RAG wins in 2025 and 2026 for almost all enterprise use cases. Context-stuffing is appropriate for exactly two narrow cases: (1) fixed, small-to-medium corpora (under ~100K tokens) where per-query cost is not a constraint and queries are primarily factual recall; (2) asynchronous one-shot analysis tasks where you want the model to reason over the entire document set at once. For everything else — large corpora, high query volume, complex synthesis, frequently-updated knowledge — the architecture is agentic RAG with dynamic multi-step retrieval, not context-stuffing.

The mechanism that drives this conclusion: the NoLiMa result is a fundamental attention property, not a prompt engineering gap. No instruction to "pay careful attention to the full context" overrides the fact that semantic inference over long distances degrades as context grows. Fixing this requires *retrieval* — bringing the relevant material close to the generation step — not just a bigger window.

---

## Runnable experiment

This experiment tests the core claim: that context-stuffing degrades on non-literal queries compared to targeted retrieval, even when the model has the full corpus in context.

**What you are testing:** Take a 100K-token corpus. Ask the same query using (a) full context stuffing and (b) chunked RAG with top-5 retrieval. Compare answer accuracy, latency, and cost.

**Step 1 — Set up the experiment.**

Direct Claude Code with this instruction:

> "I want to run a RAG vs context-stuffing comparison experiment. Please do the following:
> 
> First, download the full text of a public document set that totals approximately 100,000 tokens — for example, use the text of all 50 US state constitutions combined, or the full text of a major open-source project's documentation (your choice, but make sure you can cite the source). Save this as a single file called `corpus.txt` and tell me the exact token count using tiktoken.
> 
> Second, create a list of 10 test questions. Five should be 'literal recall' questions — questions where the answer is a specific phrase or fact that appears verbatim in the corpus. Five should be 'inference' questions — questions that require combining information from multiple sections or reasoning about what the corpus implies.
> 
> Show me the 10 questions before proceeding."

Review the questions. Confirm they represent both query types before continuing.

**Step 2 — Run the context-stuffing condition.**

> "Now, for each of the 10 questions, call Claude Sonnet 4.6 with the full corpus in context plus the question. Record: (1) the answer, (2) the time taken, (3) the approximate input token count. Save all results to a file called `results_stuffing.json`."

**Step 3 — Run the RAG condition.**

> "Now implement a simple RAG pipeline: chunk the corpus into 512-token chunks with 128-token overlap, embed each chunk using the `text-embedding-3-small` model from OpenAI, store the embeddings locally. For each of the 10 questions, retrieve the top-5 chunks by cosine similarity, then call Claude Sonnet 4.6 with only those chunks in context. Record: (1) the answer, (2) the time taken, (3) the approximate input token count. Save all results to `results_rag.json`."

**Step 4 — Score and compare.**

> "Compare `results_stuffing.json` and `results_rag.json`. For each question: (1) are the answers correct? Grade them yourself — I'll review your grades. (2) What was the latency difference? (3) What was the token count difference, and at $3/M input tokens, what was the cost difference per query? Summarize in a table."

**Expected observation:** On literal recall questions, both approaches should score similarly. On inference questions, you should see divergence — context-stuffing may score higher on some (because it has access to all context simultaneously) but lower on others (because the relevant material is buried and the model fails to synthesize across distance). Total cost for context-stuffing should be roughly 20–40x higher.

If you observe that context-stuffing beats RAG on inference questions, that is an important result. Note the corpus size (if it is under 32K tokens, context-stuffing may genuinely outperform on inference tasks at that scale — the degradation curve from NoLiMa only becomes decisive above ~32K). This is the kind of nuanced result that makes you a better architect.

**Variation to add:** Repeat with a query that requires combining information from two documents that are far apart in the corpus. This is the multi-hop case. Compare whether agentic RAG (query decomposition → two retrieval passes → synthesis) outperforms both naive approaches.

---

## Problem set

**Problem 1: Diagnose a production failure.**

You are advising a team that built an internal Q&A tool over a 200,000-token legal contract corpus. Users report that the tool often gives answers that are "mostly right but miss a key qualifier." The tool uses standard top-5 cosine retrieval, 512-token chunks with no overlap. What is the most likely failure mode? What is the second most likely? Propose two specific architectural changes, each targeting one failure mode, and describe what measurement you would use to confirm the fix worked. (Do not run code. Write your diagnosis and fix proposal as you would in a design doc.)

**Problem 2: Read NoLiMa and take a position.**

Read the abstract and Section 4 of NoLiMa (arXiv:2502.05167).[^9] The authors argue that performance degradation with context length "stems from the increased difficulty the attention mechanism faces in longer contexts when literal matches are absent." Write a one-paragraph response: do you agree this is a fundamental attention limitation, or could it be addressed by better training data or fine-tuning? Cite at least one other paper (RULER or the Databricks study) in your response to support or challenge the NoLiMa authors' mechanism claim.

**Problem 3: Cost model for a real use case.**

You are designing a RAG system for a law firm that has 3 million tokens of case precedents. Users will ask approximately 500 queries per day. Using the pricing numbers in Part 4 of this lesson, calculate: (a) the daily and annual cost of context-stuffing at full corpus, (b) the daily and annual cost of top-5 RAG, (c) at what query volume per day the break-even shifts if Anthropic offers a flat-rate enterprise license at $50,000/year for unlimited Claude Sonnet usage. Show your math. State which approach you would recommend and why, given that the queries are primarily "synthesis across multiple cases" (inference type, not literal recall).

**Problem 4: Design an agentic RAG for medical literature review.**

A research team needs to review 50,000 PubMed abstracts (roughly 25M tokens) to answer clinical questions like "what does the evidence say about treatment X for condition Y in patients over 65?" Design an agentic RAG architecture on paper. Specify: (a) how you would structure the index, (b) what the orchestrator agent's planning prompt would do, (c) how many retrieval hops you would budget, (d) how you would handle the citation fabrication failure mode to ensure every claim in the output traces to a real abstract. You do not need to write code. Write a one-page architecture spec.

**Problem 5: Challenge Anthropic's claim.**

Anthropic's Contextual Retrieval post claims a 49% reduction in retrieval failures (35% with Contextual Embeddings only, 67% with reranking).[^1] Read the methodology section of the post. Identify at least two limitations of their evaluation setup that might make the result not transfer to your use case. Then describe what you would change about their eval to make it a fair test for your specific domain.

---

## Common failure modes at scale

**The index maintenance gap.** Teams build the RAG pipeline, celebrate the demo quality, and deploy. Six months later, half the corpus has been updated, but the index has not been reindexed because "it's working." The tool starts giving stale answers. The failure is not noticed until a user catches a material error. Fix: treat index freshness as a system metric with alerts, not as a deployment task.

**Top-k fixed in config, never tuned.** Most deployed RAG systems use a default top-k of 5 or 10 from the initial scaffolding code. Top-k should be tuned per query type — lower for factual recall (reduce noise), higher for open-ended synthesis (increase coverage). No team that sets k once and never revisits it is operating at production quality.

**No eval on retrieval — only on generation.** Teams evaluate whether the generated answer is correct, but they never measure retrieval precision and recall independently. This means you cannot tell whether a wrong answer is a retrieval failure or a generation failure. The fix is a labeled "golden set" of query/chunk pairs that lets you score retrieval independently from generation. Hamel Husain's October 2024 writing on eval-driven development argues this separation is the single highest-leverage improvement in most production RAG pipelines.

**Embedding model mismatch.** The embedding model trained on web text gets deployed over legal, medical, or technical documents. The semantic space does not align. Retrieval miss rates are high. The team keeps tweaking prompt and top-k without diagnosing the root cause. The correct diagnosis requires running retrieval recall on a labeled set with the current embedding model and confirming the failure rate is above a threshold that warrants switching to a domain-fine-tuned embedding model.

**Context-stuffing for a corpus that grows.** A team ships a successful context-stuffing product on a 50K-token corpus. Users love it. They add more documents. At 200K tokens, latency becomes unacceptable. At 1M tokens, cost becomes unacceptable. The team now has to retrofit a RAG pipeline into an architecture that was designed without it. Building RAG in from the start — even if initially using a full-context shortcut for small corpora — is cheaper than retrofitting it later.

---

## Open questions — what is not settled

**1. Does reasoning-native architecture fix the NoLiMa problem?**

NoLiMa tested standard models. Several newer architectures (o3, Claude's extended thinking mode, Gemini's reasoning models) are explicitly designed for multi-step inference. It is not yet clear whether native reasoning chains allow these models to do reliable multi-hop inference at 500K+ tokens. The benchmark results from RULER and NoLiMa predate the current generation of reasoning models. This is an open empirical question.

**2. Is hybrid search (dense + sparse) always the right retrieval baseline?**

Anthropic's Contextual Retrieval post combines dense embedding with BM25 (keyword-based sparse retrieval) and reports 67% failure rate reduction with reranking. But BM25 assumes the query and the document share vocabulary — exactly the assumption that breaks in register mismatch cases. The right combination of retrieval signals is likely corpus-dependent, but there is no systematic study of which hybrid to use for which corpus type.

**3. Can retrieval-augmented fine-tuning (RAFT) replace architecture changes?**

RAFT (Zhang et al. 2024, *RAFT: Adapting Language Model to Domain Specific RAG*, arXiv 2403.10131 — https://arxiv.org/abs/2403.10131) fine-tunes the generator to be robust to distractors in the retrieved context. Preliminary results suggest it significantly reduces distractor dominance failure. But it requires fine-tuning access (not available to API-only users) and has not been benchmarked on the full taxonomy of RAG failures described in this lesson. Whether RAFT generalizes across failure modes or only addresses distractor robustness is unsettled.

---

## Reviewer lens

**Karpathy would push back on the cost table in Part 4.** Specifically: the numbers assume a query-by-query API pricing model, but Karpathy has argued (in his 2025 commentary on AI infrastructure) that the relevant comparison for serious products is total system cost including engineering time, maintenance, and reliability — not per-query API cost. A context-stuffing approach has near-zero retrieval infrastructure to maintain. A RAG pipeline with evaluation harnesses, index freshness monitoring, embedding model management, and reranking requires ongoing engineering. At small to medium scale, the engineering cost of RAG might exceed the API cost of context-stuffing. The lesson should be clearer that the cost comparison is API-cost-only and that total system cost tilts differently at different scales.

**Chip Huyen would push back on the experiment design in the Runnable Experiment section.** Specifically: the 10-question test set is N=10, which is statistically meaningless. Huyen's *AI Engineering* book argues that production eval sets need N≥100 with structured labeling to distinguish signal from noise. Running N=10 and drawing conclusions about which architecture is "better" is exactly the kind of premature evaluation that leads to wrong architectural decisions. The lesson should frame the runnable experiment as a *diagnostic* that reveals failure modes, not as a conclusive architectural comparison.

**The NoLiMa authors themselves would push back on the interpretation in Part 6.** They are careful to say performance degrades in their benchmark — they do not claim this is impossible to fix with architectural improvements. Characterizing the result as a "fundamental attention limitation" goes slightly beyond what they demonstrate. The attention mechanism in current transformer architectures makes this hard; it does not prove that next-generation attention mechanisms will have the same limitation. The lesson's "my position" section should acknowledge this caveat more explicitly.

**A legal engineer running production RAG would push back on the citation fabrication numbers.** The hallucination rates cited (17% Lexis, 33% Westlaw, 43% GPT-4) come from a study of specific task types in legal research. Legal research requires case citation with exact case names, docket numbers, and page references — a particularly unforgiving evaluation criterion. Citation quality in domains with less rigorous attribution standards (internal policy Q&A, customer support) is likely substantially better. The lesson correctly notes the domain-specificity of this problem but should foreground it more prominently to avoid alarming readers in non-legal applications.

---

## Further reading

**Must-read (read before building any RAG system in production):**

1. Liu et al., "Lost in the Middle" (2023, TACL 2024) — arXiv:2307.03172. Foundational evidence that generators do not attend uniformly to long context.
2. Hsieh et al., "RULER" (NVIDIA, 2024) — arXiv:2404.06654. The benchmark that broke the "NIAH = real performance" assumption.
3. Anthropic, "Contextual Retrieval" (September 2024) — anthropic.com/news/contextual-retrieval. The best documented operator-level fix for retrieval miss, with production numbers.

**Recommended:**

4. NoLiMa, arXiv:2502.05167 (ICML 2025) — Read Section 4 (results) and Section 5 (mechanism analysis). Skip the appendix unless you are building benchmarks.
5. Databricks, "Long Context RAG Performance of LLMs" (November 2024) — databricks.com/blog/long-context-rag-performance-llms. Real benchmark across 20 models; the per-model degradation curves are the most useful artifact.
6. Anthropic Engineering, "How we built our multi-agent research system" (June 2025) — anthropic.com/engineering/multi-agent-research-system. Operator war story with specifics from a team that actually ran this in production.

**Optional (for depth on specific topics):**

7. LlamaIndex, "Towards Long Context RAG" (March 2024) — llamaindex.ai/blog/towards-long-context-rag. Jerry Liu's framing of the architectural options; shows the debate in real time.
8. LlamaIndex, "RAG is dead, long live agentic retrieval" (2025) — llamaindex.ai/blog/rag-is-dead-long-live-agentic-retrieval. The updated position; read alongside the 2024 post to see how the field evolved.
9. arXiv:2501.09136, "Agentic Retrieval-Augmented Generation: A Survey" (January 2025). Taxonomy of agentic RAG architectures; useful if you are designing a multi-step retrieval system.

---

## Citations

[^1]: Anthropic, "Introducing Contextual Retrieval," September 19, 2024. https://www.anthropic.com/news/contextual-retrieval — Supports the claims about context-blind chunking causing ~35–40% retrieval failures, 49% reduction with Contextual Embeddings + BM25, 67% with reranking. Methodology caveat: evaluation corpus is five domains of moderate-size technical documents.

[^2]: Nelson F. Liu, Kevin Lin, John Hewitt, Ashwin Paranjape, Michele Bevilacqua, Fabio Petroni, Percy Liang, "Lost in the Middle: How Language Models Use Long Contexts," arXiv:2307.03172 (July 2023), published in TACL 2024. https://arxiv.org/abs/2307.03172 — Foundational finding that relevant information in the middle of long contexts degrades LLM performance significantly on multi-document QA.

[^3]: Journal of Empirical Legal Studies, 2025, "Legal RAG Hallucinations" (Stanford). https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf — Reports hallucination rates: 17% Lexis+ AI, 33% Westlaw AI-Assisted Research, 43% GPT-4 on legal research tasks.

[^4]: "Detecting and Correcting Reference Hallucinations in Commercial LLMs and Deep Research Agents," arXiv:2604.03173 (2025). https://arxiv.org/html/2604.03173v1 — Finds 3–13% URL fabrication rate in search-grounded systems.

[^5]: "FACTUM: Mechanistic Detection of Citation Hallucination in Long-Form RAG," arXiv:2601.05866 (January 2026). https://arxiv.org/abs/2601.05866 — Finds 57% of citations in a RAG-optimized model showed unfaithful behavior (cited source does not support the claim).

[^6]: Gao et al., "Precise Zero-Shot Dense Retrieval without Relevance Labels" (HyDE), 2022. Referenced in context of query-document mismatch mitigation strategies. For HyDE implementation context: https://arxiv.org/abs/2212.10496

[^7]: Google DeepMind, "Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context," arXiv:2403.05530 (2024). https://arxiv.org/abs/2403.05530 — Reports >99.7% NIAH recall at 1M tokens, near-perfect recall to 10M tokens for text. Also: https://blog.google/innovation-and-ai/products/google-gemini-next-generation-model-february-2024/

[^8]: Cheng-Ping Hsieh, Simeng Sun, Samuel Kriman, Shantanu Acharya, Dima Rekesh, Fei Jia, Yang Zhang, Boris Ginsburg (NVIDIA), "RULER: What's the Real Context Size of Your Long-Context Language Models?", arXiv:2404.06654 (April 2024). https://arxiv.org/abs/2404.06654 — Evaluates 17+ models on multi-task long-context benchmark; finds large degradation beyond claimed context sizes for all but a subset of tested models.

[^9]: Adobe Research, "NoLiMa: Long-Context Evaluation Beyond Literal Matching," arXiv:2502.05167 (February 2025), accepted ICML 2025. https://arxiv.org/abs/2502.05167 — 13 LLMs tested claiming 128K+ context; 11 of 13 drop below 50% of short-context baseline at 32K tokens when literal matching is removed. GPT-4o declines from 99.3% to 69.7%.

[^10]: Anthropic, "1M context is now generally available for Opus 4.6 and Sonnet 4.6." https://claude.com/blog/1m-context-ga — Confirms GA status, pricing ($5/$25 Opus 4.6, $3/$15 Sonnet 4.6 per M tokens), and MRCR v2 score 78.3% for Opus 4.6.

[^11]: Google, Gemini 2.5 Pro specs. https://ai.google.dev/gemini-api/docs/models — 1,048,576 token context window; 2M forthcoming; 100% recall to 530K tokens, 99.7% recall at 1M tokens.

[^12]: OpenAI, "Introducing GPT-4.1 in the API" (April 14, 2025). https://openai.com/index/gpt-4-1/ — 1M token context window; $2/$8 per M tokens in/out for full model.

[^13]: Jue Wang, Bhavnick Minhas, Purva Patel, Chirag Gokul, et al. (Databricks), "Long Context RAG Performance of LLMs," arXiv:2411.03538 (November 2024). https://www.databricks.com/blog/long-context-rag-performance-llms — Benchmarks 20+ models on DocsQA, FinanceBench, NaturalQuestions at 2K–2M token context; finds per-model performance peaks far below advertised context limits.

[^14]: MindStudio, "What Is Flat-Rate Long-Context Pricing? How Anthropic Changed the Economics of RAG." https://www.mindstudio.ai/blog/flat-rate-long-context-pricing-anthropic-claude — Discusses Anthropic's enterprise pricing model and its implications for context-stuffing economics.

[^15]: Jerry Liu / LlamaIndex, "Towards Long Context RAG" (March 1, 2024). https://www.llamaindex.ai/blog/towards-long-context-rag — Proposes that query type determines whether long-context or RAG is appropriate; introduces Small-to-Big Retrieval and Intelligent Routing architectures.

[^16]: LlamaIndex, "RAG is dead, long live agentic retrieval" (2025). https://www.llamaindex.ai/blog/rag-is-dead-long-live-agentic-retrieval — Declares naive top-k RAG insufficient; argues for agentic multi-knowledge-base retrieval as the production default.

[^17]: Anthropic Engineering, "How we built our multi-agent research system" (June 2025). https://www.anthropic.com/engineering/multi-agent-research-system — Orchestrator-worker architecture; 90% research time reduction; 90.2% improvement over single Opus 4 on internal benchmarks.

[^18]: Lim et al., "Agentic Retrieval-Augmented Generation: A Survey on Agentic RAG," arXiv:2501.09136 (January 2025). https://arxiv.org/abs/2501.09136 — Taxonomy of agentic RAG architectures; failure modes including planning failures, tool loop explosion, latency compounding.
