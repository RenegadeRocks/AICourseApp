---
type: lesson
block: block-2-ai-employees
week: week-04
day_of_cycle: 5
day_name: fri
session_slug: building-comprehensive-rag-ai-agent
date_due: 2026-06-12
tags: [advanced-rag, graphrag, agentic-retrieval, self-rag, chain-of-rag, long-context, lost-in-the-middle, ruler, citations-api, leiden-community, cost-per-correct-answer]
sources:
  - edge-graphrag-arxiv-2404-16130-2024
  - microsoft-lazygraphrag-nov-2024
  - liu-lost-in-the-middle-tacl-2024
  - hsieh-ruler-arxiv-2404-06654-2024
  - google-gemini-1-5-tech-report-arxiv-2403-05530-2024
  - anthropic-1m-context-ga-mar-2026
  - asai-self-rag-arxiv-2310-11511-2023
  - wang-chain-of-rag-arxiv-2501-14342-2025
  - zhang-raft-arxiv-2403-10131-2024
  - anthropic-contextual-retrieval-sep-2024
  - anthropic-citations-api-jan-2025
  - chroma-context-rot-research-2025
  - kiela-contextual-ai-rag-2025
  - liu-llamaindex-long-context-rag-2024
  - husain-context-rot-notes-2025
  - kamradt-niah-github-2023
  - tang-multihop-rag-colm-2024
last_verified: 2026-07-17
word_count_target: 6000
---

# Advanced RAG — GraphRAG, agentic retrieval, the long-context question, and claim-level grounding

## Why this matters

Yesterday you built the retrieval stack: chunking, embeddings, hybrid search, reranking, and Anthropic's contextual retrieval preprocessing. That stack handles the problem of *"find me the three paragraphs that contain the answer to this specific question."* It is necessary and not sufficient. The four problems it does not solve are the ones that now eat most enterprise RAG deployments.

First, **global sensemaking.** A question like "what are the three recurring failure patterns across the last two years of incident reports?" is not retrievable by any single query — the answer is latent in the structure of the whole corpus. Second, **multi-hop reasoning.** A question like "of the customers who churned in Q3, which of them had filed a severity-1 ticket in the prior six months, and which account executive owned the relationship?" requires three retrievals stitched by logic, and a single top-k fetch returns garbage. Third, **when long-context obsoletes RAG.** By July 2026 a 1M-token context window is table stakes — Gemini 3 (Nov 2025) and Gemini 2.5 Pro both ship 1M, and Claude Fable 5, Opus 4.8, and Sonnet 5 are all at 1M standard;[^gem15][^claude1m] if your corpus fits in-window, why run a retriever at all? Fourth, **claim-level grounding.** A RAG system that answers "yes, the policy covers this" without pointing to the sentence it's inferring from is not deployable in legal, healthcare, insurance, or financial services. The retrieval-then-generation two-step is structurally unable to produce per-claim citations; the model invents a plausible sentence that happens to agree with the context.

By the end of this lesson you will be able to (1) explain what GraphRAG actually is — entity extraction, Leiden community detection, pre-generated community reports — and defend when its 10–100× ingestion cost is worth paying vs when LazyGraphRAG or plain contextual retrieval wins, (2) design an agentic-retrieval loop (Self-RAG or Chain-of-RAG) with defensible stop conditions, and know which operators argue it's a net loss vs a net win, (3) run a cost-per-correct-answer comparison across RAG, GraphRAG, and pure long-context on a real corpus and make a defensible routing decision, (4) wire Anthropic's Citations API into a RAG pipeline and understand why operator-level citation correctness ≠ claim-level grounding, (5) hold a rigorous position in the "long-context obsoletes RAG" debate with named primary sources on both sides.

This is the lesson where RAG stops being a pipeline you assemble and starts being an architecture you reason about with cost, latency, and correctness budgets — the frame every production-grade operator uses.

## Prerequisites

- Thursday's lesson on RAG fundamentals ([[04-thu-rag-fundamentals]]) — you know what chunking, hybrid BM25+dense retrieval, reranking, and Anthropic's contextual retrieval do, and you have a baseline pipeline you can modify.
- Tuesday's lesson on agent architectures ([[02-tue-agent-architectures]]) — you know the five patterns from Anthropic's *Building Effective Agents* post, and you can tell an evaluator-optimizer workflow from an autonomous agent loop.

If either is absent the lesson will still land, but the experiment section assumes both.

## Layer 1 — GraphRAG: what it actually is, and the 97% / 700× numbers in context

The Microsoft GraphRAG paper (*"From Local to Global: A Graph RAG Approach to Query-Focused Summarization,"* Edge, Trinh, Cheng, Bradley, Chao, Mody, Truitt, Metropolitansky, Ness, Larson; arxiv 2404.16130, first posted April 24, 2024, last revised February 19, 2025)[^graphrag] is the most-cited graph-retrieval paper of the cycle because it attacked a specific failure mode of vanilla RAG rather than trying to replace it wholesale. The failure mode: vanilla RAG — embed the chunks, vector-search against the query, stuff the top-k into the prompt — systematically loses on *global sensemaking* questions. "What are the top themes in this dataset?" has no local answer; every chunk is equally relevant or equally irrelevant to it. Top-k retrieval returns a handful of arbitrary paragraphs and the model confabulates a theme list from what it happens to see.

### The construction pipeline

GraphRAG's indexing pipeline runs four stages over a corpus before the first query ever arrives.

**Stage 1 — Entity and relationship extraction.** An LLM reads each source chunk and emits entities (people, orgs, products, places, concepts) and relationships between them, each with a short description. In the paper's configuration this is a single LLM call per chunk with a tuned prompt; at a 600-token chunk size over a 1M-token Podcast Transcripts corpus that's roughly 1,700 extraction calls per corpus.

**Stage 2 — Graph construction and summarization.** Entities and relationships are deduplicated and joined into a global knowledge graph. An LLM then generates element summaries for clusters of instances — "Barack Obama" mentions in campaign transcripts get summarized into one entity profile.

**Stage 3 — Community detection via Leiden.** The Leiden algorithm (Traag, Waltman, van Eck 2019 — the improved successor to Louvain community detection) partitions the graph into hierarchical communities. The Leiden algorithm is chosen specifically because it guarantees *well-connected* communities, avoiding the "badly connected community" pathology of Louvain. The paper reports using hierarchical Leiden at multiple resolution levels, producing a forest of communities-within-communities.[^graphrag]

**Stage 4 — Community report generation.** For every community at every level, the LLM writes a *community report* — a prose summary of what the community is about, its key entities, its internal structure. These reports are the new retrieval unit. A query asking "what are the top themes in this corpus?" doesn't fetch chunks; it fetches community reports, generates a partial answer per report, and map-reduces the partials.

The ingestion cost is the story. On a public 1M-token News Articles dataset in the paper, GraphRAG indexing ran roughly 610,000 input + 19,000 output tokens to build the graph and generate community summaries at the highest level, before any queries.[^graphrag] At Anthropic or OpenAI flagship rates this is tens of dollars for a 1M-token corpus — roughly 10–100× the cost of a pure embedding pipeline for the same corpus, which needs only the embedding-model cost (fractions of a cent per 1K tokens with text-embedding-3-small or voyage-3). The paper is candid about this. What graphs buy you is the ability to *answer a different class of question* — global sensemaking — at a structural cost multiplier; they are not a free quality lift on the questions vanilla RAG already handles.

### The result in numbers

Microsoft's benchmark on global sensemaking questions over two 1M-token corpora (Podcast Transcripts, News Articles) reports GraphRAG at Level 0 and Level 1 communities outperforming vanilla vector RAG on head-to-head preference scoring by margins of 70–80% on comprehensiveness and diversity of answers.[^graphrag] Separately, Microsoft's November 2024 follow-up blog reports that a tuned GraphRAG required between 26% and 97% fewer tokens at query time than the alternatives, with 97% fewer tokens for root-level global summaries relative to a baseline.[^lazygraph] That query-time number is the one to hold against the ingestion number: you spend 10–100× up front, you save 3–30× every time a user asks a global question. The break-even is a function of how many global queries the corpus will serve over its lifetime.

### LazyGraphRAG — the cost rebuttal to GraphRAG

On November 25, 2024, Microsoft Research released *LazyGraphRAG* — a retort to its own earlier system. LazyGraphRAG's construction cost is reported at **0.1% of full GraphRAG's** — a 1000× reduction — and identical to vector RAG.[^lazygraph] The mechanism: it doesn't pre-generate community summaries. It extracts concepts and their co-occurrences into a light graph at ingestion, then *at query time* it retrieves the relevant communities on the fly and summarizes them just-in-time using a cheap LLM. The paper claims LazyGraphRAG at 4% of GraphRAG's query cost outperforms GraphRAG Global Search on global queries *and* outperforms vanilla RAG on local queries.[^lazygraph]

Operator read: the original GraphRAG is a good fit only if (a) your corpus is relatively stable — you index once and query many times, (b) global sensemaking queries are a meaningful fraction of the workload, and (c) the up-front token cost is amortizable. LazyGraphRAG is the better default for exploratory workloads, streaming corpora, or pilots — because the ingestion cost is effectively free. A third-party *unbiased evaluation* paper (arxiv 2506.06331, Jun 2025, *"How Significant Are the Real Performance Gains? An Unbiased Evaluation Framework for GraphRAG"*) has challenged the transferability of GraphRAG's headline numbers: applying a bias-corrected framework, it found LightRAG's reported win rates on the Agriculture dataset (66.70% vs NaiveRAG, 56.38% vs MGRAG) collapse to 39.06% and 32.33%, with high tie rates shrinking the real gaps between methods.[^graphgains] Darren Edge's team would push back that those benchmarks were run with default untuned configurations, but the asymmetry of the evidence is now clear: GraphRAG's wins are domain-sensitive and smaller than first reported.

### Cross-domain: where GraphRAG earns its cost, and where it doesn't

Earns it: *legal/compliance archives* (cross-regulation queries like "which regulations touch data-residency across APAC and have overlapping enforcement bodies?" — no single chunk answers it; the graph's cross-regulation links do real work); *multi-year consulting research libraries* where recurring recommendation patterns are latent in structure; *biomedical literature* with dense entity-relationship structure. On the biomedical/knowledge-graph point, the most-cited number — knowledge-graph RAG at **86.31% on RobustQA vs 32.74–75.89% for vector-RAG baselines** — comes from **Writer's own RobustQA marketing benchmark**, not from Microsoft's LazyGraphRAG post; treat it as a vendor-disclosed figure on a vendor-run benchmark.[^writerkg]

Doesn't: *product-documentation RAG for SaaS support*, where users ask local questions ("how do I set up SSO?") and contextual-retrieval + rerank Pareto-dominates on cost and latency; *dynamic corpora* (news, email, messaging) where re-indexing is operationally painful and LazyGraphRAG is the honest choice; *moderate corpora that fit in a 1M window*, where the comparison shifts from "GraphRAG vs vector RAG" to "GraphRAG vs no retrieval at all" — Layer 3.

## Layer 2 — Agentic retrieval: Self-RAG, Chain-of-RAG, and the latency-cost-quality trilemma

Vanilla RAG retrieves once and generates once. Agentic retrieval lets the model *decide* to retrieve more, rewrite the query, or abstain. The two canonical papers to hold in your head:

### Self-RAG (Asai, Wu, Wang, Sil, Hajishirzi — arxiv 2310.11511, October 2023)

Self-RAG trains a single LM to emit *reflection tokens* during generation — special tokens that encode decisions: `[Retrieve]` (go fetch passages), `[IsRel]` (is the retrieved passage relevant?), `[IsSup]` (is the draft answer supported by the passage?), `[IsUse]` (is the draft useful to the user's query?).[^selfrag] At inference time the model reads its own reflection tokens and either proceeds with the current passage, triggers another retrieval with a rewritten query, or abstains. Self-RAG 7B and 13B outperformed ChatGPT and retrieval-augmented Llama2-chat on open-domain QA, reasoning, and fact-verification tasks at the time of publication, with particularly strong gains on citation accuracy for long-form generations.[^selfrag]

The architectural move is that *the retrieval policy is learned*, not hand-written. The cost is that you need a fine-tuned model with reflection-token training data. Most production teams don't train custom models; they approximate Self-RAG with a prompted workflow — an LLM asked to decide whether to retrieve, what to query, and whether to stop.

### Chain-of-Retrieval Augmented Generation (CoRAG — Wang et al., arxiv 2501.14342, January 2025)

CoRAG extends the iteration over retrieval more explicitly. The model generates a *chain* of (sub-query, retrieved-passages, intermediate-answer) triples, each step informed by the previous, until it produces a final answer. On multi-hop QA benchmarks CoRAG reports **>10 EM-score-point improvements** over strong single-shot baselines, and sets state-of-the-art on the KILT benchmark across a diverse range of knowledge-intensive tasks.[^corag] The training recipe uses rejection sampling over existing RAG datasets to generate intermediate retrieval chains, then fine-tunes with standard next-token prediction.

For practitioners who won't train a custom model, the essential CoRAG move can be approximated: *let the model plan a retrieval chain before executing the first query.* This is what Harrison Chase's LangGraph and Jason Liu's `instructor` library (used for schema-enforced step outputs) let you compose without training.

### RAFT — the adjacent idea

Retrieval-Augmented Fine-Tuning (Zhang, Patil, Jain, Shen, Zaharia, Stoica, Gonzalez — arxiv 2403.10131, March 2024)[^raft] is a different spin on the same theme: train the model on domain-specific (question, retrieved-docs, answer) triples where *some* of the retrieved docs are distractors, so the model learns to ignore them and to cite the right spans verbatim. RAFT is a preparation move, not a runtime move — worth knowing exists, rarely the right thing for a non-frontier operator to do themselves.

### Eugene Yan's counter: self-reflection often *hurts*

Eugene Yan's *Patterns for Building LLM-based Systems & Products*[^eugeneyan] includes a pragmatic warning that becomes more important the closer you get to production: self-reflection loops add latency, cost, and *sometimes hurt accuracy* because the model second-guesses correct answers into wrong ones. His 2024 writing on LLM patterns notes that narrow, task-specific prompts often outperform general self-reflective agents on the same task, because every extra loop is another opportunity to confabulate. The empirical reality: on benchmarks designed for multi-hop (MultiHop-RAG,[^multihoprag] HotpotQA, 2WikiMultiHopQA) the agentic loop wins by 5–15 points; on benchmarks designed for local QA it loses or ties while paying 2–5× the latency and cost.

### The latency math operators actually care about

A single-shot RAG query on a Claude Sonnet 5 generation call is typically 1.5–3 seconds end-to-end with a warm cache. A 3-hop agentic loop is 5–12 seconds. If your product is an interactive chat UI, the second number is user-hostile. If your product is an overnight batch job, the second number is invisible — the trade-off is a product decision, not a technical one. Named operators are split: Jerry Liu of LlamaIndex has argued in talks through 2024 that *small-to-big* retrieval (retrieve small precise chunks, then expand to surrounding context via document metadata) is the right middle ground, keeping latency down while recovering multi-hop gains for a subset of queries.[^jerryliu] Ben Hylak at Raindrop has argued publicly that agent UX degrades at any loop count >1 for interactive products, period, and that the right answer is to move the work to background pipelines. Both are right for different products.

### Cross-domain: when the loop earns its cost

- **Legal research.** "Find me three cases where a non-compete was ruled unenforceable in Delaware when the employee was terminated without cause." A three-hop loop (jurisdiction filter → outcome filter → cause filter) is the only way this works; a flat query fails.
- **M&A diligence.** "Across the target's last eight board decks, are there revenue numbers that contradict what was reported in the management presentation?" Requires retrieving across documents and cross-checking — classic multi-hop.
- **Insurance claims investigation.** "Did the policyholder make statements in earlier claim history inconsistent with the current claim?" Same shape.

### Cross-domain: when the loop is theater

- **Single-document question answering** (product docs, API references, a specific 10-K). The answer is local; one well-tuned retrieval call wins.
- **Interactive chat UIs** where the user can re-ask the question. Every second of latency trades against the user's willingness to wait; the product answer is often "single-shot + excellent reranking + citations."

## Layer 3 — Long-context vs RAG: the live frontier debate

This is the live frontier debate. Hold both sides.

### The context-window reality, as of July 2026

Gemini 1.5 Pro shipped with 1M tokens in production in February 2024 and a 2M-token variant later that year, the Google DeepMind technical report (Reid et al., arxiv 2403.05530, March 2024)[^gem15] reporting >99.7% recall on needle-in-a-haystack retrieval at 1M tokens and 99.2% at 10M tokens in internal evaluations. Gemini 3 (November 2025) and Gemini 2.5 Pro both ship 1M-token windows. Claude 3.5 and Claude 4 were originally 200K; Anthropic moved to 1M context GA over 2026, and the **current lineup — Claude Fable 5, Opus 4.8, and Sonnet 5 — all run 1M context by default**, with 128K max output.[^claude1m] The pricing is where the frontier moved: the widely-available frontier is **Opus 4.8 at $5/$25 per Mtok**, and the *capability* frontier is **Claude Fable 5 at $10/$50 per Mtok — 2× the price the older cost tables assumed** (Opus 4.7/4.8 sat at $5/$25). Sonnet 5 is the cheap-agentic default at $2/$10 intro (through Aug 31 2026), then $3/$15. Two things every cost table below has to absorb: Fable 5's 2× pricing, and the **new tokenizer** (introduced on Opus 4.7 and shared by Opus 4.8 / Sonnet 5 / Fable 5) that tokenizes the same text to **~30% more tokens** than pre-4.7 models — so a corpus that "fit" or "cost X" on an old tokenizer costs more now.[^claude1m]

The 2024–2025 framing was "long-context is close to obsoleting RAG." The 2026 framing has shifted, for reasons below — and the price and tokenizer changes *sharpen* the anti-long-context case rather than soften it.

### The pro-long-context position

The canonical pro-long-context argument, articulated by Sam Altman and others through 2024: "if you can just stuff the whole corpus into the prompt, retrieval becomes irrelevant — you're paying a retrieval cost to save the model from reading, when reading is what it's good at." Empirically, Gemini 1.5 Pro's near-perfect needle-in-a-haystack recall at 1M and 2M tokens[^gem15] is the strongest evidence for this position. Greg Kamradt's original needle-in-a-haystack benchmark[^niah] — the test that catalyzed the public discourse on long context — showed earlier models like GPT-4 128K degrading above 64K; the newer frontier models at 1M substantially fixed that problem.

Douwe Kiela (Contextual AI, the co-inventor of RAG in 2020) has publicly argued that the right architecture is *RAG plus long context*, not one or the other — use retrieval to narrow to a sensibly-sized window (say, 200K–500K tokens of relevant material), then let the model use its long-context capability to reason across that window.[^kiela] This is now a widely-held operator position.

### The anti-long-context position — Lost in the Middle, RULER, context rot

Three independent pieces of evidence complicate the pro-long-context story.

**Lost in the Middle (Liu et al., TACL 2024).**[^lim] Nelson F. Liu's team measured a 30%+ accuracy drop on multi-document question answering when the answer document moved from position 1 to position 10 in a 20-document context. The result forms a U shape — high at the edges, low in the middle — and persists even after randomizing document order and after instruction-tuning. The paper's headline finding was so robust it named the phenomenon. Follow-up work (*Found in the Middle*, Hsieh et al., ACL 2024, arxiv 2406.16008) proposed attention calibration methods that recover up to 15 percentage points of the lost middle — but only recover, not fix.

**RULER (Hsieh, Sun, Cheng, Santhanam, Wang, Ginsburg — arxiv 2404.06654, April 2024; NVIDIA).**[^ruler] RULER extends needle-in-a-haystack to 13 tasks across four categories (retrieval, multi-hop tracing, aggregation, QA) with configurable length and complexity. The headline finding from the 17 long-context models RULER evaluated: "despite achieving nearly perfect accuracy in the vanilla NIAH test, almost all models exhibit large performance drops as the context length increases," and only about half of the models claiming 32K+ could maintain satisfactory performance at 32K.[^ruler] Pure needle-in-a-haystack is a solved benchmark; RULER's multi-hop and aggregation tasks are not.

**Chroma's Context Rot research (July 2025, "Context Rot: How Increasing Input Tokens Impacts LLM Performance," Kelly Hong, Anton Troynikov, Jeff Huber).**[^chroma] Chroma evaluated 18 frontier models — GPT-4.1, Claude 4, Gemini 2.5, Qwen3, and others — and found every single one gets measurably worse as input length grows, even on tasks that should be simple. Their four key findings:

1. Model performance varies significantly with input length *even on simple tasks*.
2. Structural coherence of the haystack *hurts* performance — all 18 models performed better on shuffled haystacks than on logically coherent documents.
3. Distractors have non-uniform impact — lower semantic similarity between needle and question makes degradation faster.
4. A 200K-window model can exhibit significant degradation at 50K tokens, long before any claimed window limit.

Hamel Husain hosted Kelly Hong of Chroma on his blog; his write-up (P6 of his RAG series, "Context Rot")[^hamelrot] highlights the production implication: when models fail with longer contexts, GPT-class models tend to *confidently hallucinate* from distractor signals, while Claude-class models are more likely to abstain. Neither behavior is ideal, but they fail differently. Husain's summary line, from his July 2024 X post: *"I'm seeing lots of takes that RAG will become irrelevant bc of long context windows. Reasons I think this is BS — You often want to filter by metadata (dates, # of views, etc). Search/IR is critical in many applied scenarios."*[^hamelx]

### The cost side of the debate

The cost asymmetry is the decisive factor most casual discussions skip, and the July-2026 price sheet plus the new tokenizer make it starker than the 2025 version of this table. Consider a corpus that measured ~500K tokens on the pre-4.7 tokenizer. On the current tokenizer (Opus 4.7/4.8, Sonnet 5, Fable 5) the *same text* is **~650K tokens** — the ~30% inflation is not free, it multiplies the pure-long-context input bill.[^claude1m] Per single user question (assume a ~1K-token answer, which is ~1.3K tokens on the new tokenizer):

| Architecture | Input tokens/query (new tokenizer) | Cost/query — Opus 4.8 ($5/$25) | Cost/query — Fable 5 ($10/$50) |
|---|---|---|---|
| Vanilla RAG (top-20 chunks @ ~500 tok) | ~13K in + ~1.3K out | ~$0.10 | ~$0.20 |
| GraphRAG global search | ~19.5K report tok + out | ~$0.13 | ~$0.26 |
| Pure long-context (whole corpus in-window) | ~650K in + ~1.3K out | ~$3.28 | ~$6.57 |

Pure long-context runs **~30–50× the per-query cost** of retrieval-based approaches — and that multiplier holds on both the $5/$25 Opus 4.8 tier and the $10/$50 Fable 5 tier, because both the retrieval and the stuffing rows scale with the same price. For a SaaS support bot serving 10K queries/day on that corpus: vanilla RAG runs ~$1,000/day on Opus 4.8, pure long-context runs ~$32,800/day — a swing north of **$11M/year for a single workflow**, and roughly double that if you run the frontier Fable 5 tier. (An earlier draft of this lesson quoted "$250/day vs $500/day" here; that was arithmetically wrong by two orders of magnitude — 10K queries at $3.28 each is ~$32.8K/day, not $250.) Kiela's "RAG plus long context" framing exists because it's the only way to preserve long-context's reasoning win without paying the full-window cost on every query — and the new tokenizer only widens the gap.

### The cost-per-correct-answer unifier

The right metric across all these architectures is **cost per correct answer**: (total cost over N queries) / (number of queries answered correctly by a rubric-grounded LLM-judge). Accuracy alone hides the price of the wins; cost alone hides which architecture actually answers the question. Under the combined metric:

- Vanilla RAG on a local-QA workload beats everything on cost-per-correct-answer, often by 5–10×.
- GraphRAG on a global-sensemaking workload beats vanilla RAG by 2–3× on cost-per-correct-answer (it costs more per query but answers many more correctly).
- Pure long-context on either workload is rarely competitive on cost-per-correct-answer except when the corpus is small and static enough that retrieval cost is overkill, or when the query requires holistic reasoning that no retrieval decomposition captures.
- LazyGraphRAG is the default for pilot-stage workloads where ingestion cost must be ~free.

This is the metric you defend your architecture with in an executive conversation. It captures the real trade-off.

## Layer 4 — Citation grounding: Anthropic Citations API, Instructor, and why "Claude cited it" ≠ "Claude is correct"

Every RAG-driven product that touches a regulated domain — legal, healthcare, insurance, finance, compliance — needs claim-level citations: the exact sentence(s) the model used to support each output claim. Two common failure modes show why this is hard.

**Failure mode 1 — confabulated citations.** A prompted RAG pipeline tells the model "cite the source for each claim." The model obliges with plausible-looking citations that do not map to the retrieved passages. This was the dominant failure mode of RAG pipelines through 2024.

**Failure mode 2 — quote-drift.** The model cites a real retrieved passage, but the sentence it quotes is paraphrased or slightly reordered — technically wrong, operationally undetectable, legally fatal.

### Anthropic Citations API (launched January 23, 2025)

On January 23, 2025, Anthropic launched the Citations API feature.[^citations] The mechanism: developers pass source documents as structured content blocks in the request; Claude's output includes `citations` objects that point to the exact character or sentence spans in the source documents that ground each output claim. Anthropic's internal evaluations reported the built-in feature outperformed custom implementations with recall-accuracy gains up to 15%; early adopter Endex reported reducing source hallucinations and formatting issues from 10% to 0% and a 20% increase in references per response.[^citations] Pricing is standard token-based, but Anthropic does not charge output tokens for the quoted text itself.

Simon Willison's January 24, 2025 write-up[^simonwillison] notes the critical operator point: the citations feature solves *formatting* (you get structured pointers) and *quote-drift* (the quote matches a span in the source), but it does not solve *groundedness* (did the cited span actually support the claim?). That second problem is still an eval problem — it requires a judge that checks whether the claim is entailed by the cited span, not just whether the citation is well-formed.

### Instructor — the schema-enforced counterpart

Jason Liu's `instructor` library (built on Pydantic, 6M+ monthly downloads as of 2024–2025)[^jxnl] is the open-source approach to the same problem. You define a Pydantic schema that requires every output claim to carry a `source_span_id` and a verbatim `quote`, and `instructor` retries the model until the output validates. For non-Anthropic models or local open-weight models (Llama 3.3 70B, Qwen, Mistral), `instructor` + a retry loop is the default operator pattern.

### The three-layer grounding check (the operator pattern)

The production pattern used by teams that can't afford citation failures:

1. **Layer 1 — Structural.** Every claim must carry a structured citation (Anthropic Citations API, or instructor-enforced Pydantic schema). No claim without a citation is allowed to reach the user.
2. **Layer 2 — Span match.** The quoted text must match a verbatim substring of a retrieved passage (deterministic check, no LLM needed). Catches quote-drift.
3. **Layer 3 — Entailment.** An LLM-judge (Claude Opus 4.8, rubric-grounded, pairwise when possible — the judge should be at least as capable as the generator) checks whether each claim is entailed by its cited span. Catches plausible-but-unsupported claims.

Layers 1 and 2 are free and deterministic. Layer 3 is the one that costs real eval budget — but it's the one that catches the production failures that matter in regulated domains.

### Cross-domain: where this pipeline is load-bearing

- **Legal brief drafting.** Every factual claim must cite a specific case, statute, or contract clause. Missing citation = malpractice risk.
- **Insurance claims processing.** Every coverage determination must cite the policy section. Auditor-facing requirement.
- **Clinical decision support.** Every recommendation must cite the guideline. Required by FDA and most health systems.
- **Financial research.** Every earnings claim must cite the 10-K, 10-Q, or earnings transcript line. Required for analyst compliance.

## Operator case studies / war stories

**Case 1 — Harvey and legal research at scale (2024–2025).** Harvey, the legal AI platform used by Reed Smith, Nixon Peabody, and other Am Law 100 firms, ran into the global-sensemaking failure on its earliest workflows. A question like *"across our last five years of M&A precedent, which non-compete clauses survived challenge and why?"* could not be answered by top-k retrieval — no single memo contained the cross-matter pattern. The operator fix was a graph-style intermediate layer: extract clauses, outcomes, jurisdictions, and precedent relationships at ingestion; answer global questions against the graph, local questions against the raw documents. Disclosed publicly only at a high level in Harvey's 2024–2025 enterprise announcements, the architecture choice maps cleanly to the GraphRAG vs vanilla RAG divide.

**Case 2 — Endex and citation hallucinations dropping from 10% to 0% (January 2025).** As part of the Anthropic Citations API launch, Endex — a financial-research AI tool — reported that structured citation support dropped their hallucinated-source and formatting-error rate from 10% to 0% and increased references per response by 20%.[^citations] *(Source caveat: these numbers come from Anthropic's own January 2025 Citations API launch post and are vendor-disclosed, not independently audited — treat as a customer testimonial embedded in a product announcement, not an independent evaluation.)* The operator story here is that Endex had invested in a custom prompt-engineered citation layer that never cleared the 90% reliability bar; the native API beat their hand-built version on day one. This is the pattern: when a frontier lab ships a primitive for a specific problem, custom implementations of that primitive are usually obsoleted within a quarter.

**Case 3 — LinkedIn's GenAI customer support agent.** LinkedIn's 2024 engineering blog on scaling a GenAI customer-service agent (referenced widely in the RAG community) describes exactly the multi-hop-retrieval failure pattern: single-shot retrieval returned plausible but wrong answers for questions that required chaining across multiple help-center articles. Their fix was a pipeline closer to CoRAG in spirit — a retrieval plan generated by the LLM, executed in stages, with an evaluator checking each intermediate result. End-to-end latency went up 3×; resolution rate went up 40%. Depending on the product surface, that's either a huge win or a product-killing regression.

**Case 4 — Chroma's context-rot finding that reshaped a retail-pricing RAG deployment.** A retail operator running a pricing-rules RAG built for 200K Claude context shifted to pure long-context in mid-2025 and saw answer quality *drop* on questions where the relevant pricing rule was buried in the middle of a 120K-token rulebook. The Chroma Context Rot research[^chroma] diagnoses exactly this: performance degrades non-uniformly well before the claimed window limit, and document structure coherence actively hurts. The operator rolled back to RAG+contextual-retrieval and reported a ~15% jump in answer quality at 10% of the inference cost.

## Runnable experiment — cost-per-correct-answer across RAG, GraphRAG, and long-context

The goal: produce a three-column table showing cost-per-correct-answer across three architectures on a real corpus, for two query classes (local QA, global sensemaking). This is the experiment that qualifies you to have a defensible opinion in the long-context vs RAG debate.

**Phase 1 — Pick your corpus and query set.** Choose a corpus of 20–50 documents you actually have access to — enterprise product docs, a legal corpus, a set of case studies, your own internal research library. Write 20 queries: 10 *local* (answerable from a single document or passage) and 10 *global* (require synthesis across multiple documents). For each query, write the ground-truth correct answer or a rubric for what a correct answer looks like.

**Phase 2 — Run three pipelines.** Ask Claude Code:

> *"Given this corpus at [path] and these 20 queries at [path], run three retrieval architectures on each query and log the (latency, input-tokens, output-tokens, answer) tuple for every run:*
>
> *(a) My best baseline RAG from Thursday — whatever interventions won on that corpus: chunking, hybrid BM25+dense, reranker, contextual retrieval preprocessing.*
>
> *(b) Pure long-context — load the entire corpus into a single Claude Opus 4.8 context (or Fable 5 if you want the frontier tier) and answer each query with no retrieval. Log real token counts on the current tokenizer — do not estimate from an old model.*
>
> *(c) A minimal GraphRAG-style pipeline — extract entities and relationships per chunk with Claude, cluster into communities (a cheap approximation of Leiden using any clustering library), generate a community summary per cluster, and answer global queries by retrieving community summaries and local queries by retrieving raw chunks. Use `microsoft/graphrag` library defaults if available; otherwise approximate.*
>
> *Save all raw outputs with the query metadata."*

**Phase 3 — Grade with an LLM-judge.** Ask Claude Code:

> *"For each of the 60 (query, architecture, answer) triples, run an LLM-as-judge with Claude Opus 4.8 using this rubric: [supply your rubric]. Grade each answer 0/1 against the ground truth or rubric. Output a table: query_id × architecture × answer_grade × latency × total_tokens × dollar_cost (using current Anthropic pricing — Opus 4.8 $5/$25, Fable 5 $10/$50, Sonnet 5 $2/$10 intro; count tokens on the current tokenizer)."*

**Phase 4 — Compute cost-per-correct-answer per architecture per query class.** Ask Claude Code to produce a 3×2 table: architectures × {local, global}, cells containing (total cost) / (number of correct answers) for that architecture and query class.

**Phase 5 — Write a 500-word decision memo.** Which architecture wins on local, which on global, and what routing rule would you ship to production? Defend each branch. Name the query type where pure long-context beats retrieval if any. Name the query type where GraphRAG's construction cost is amortized.

**Expected observation.** On most small-to-medium enterprise corpora:

- Local queries: RAG wins on cost-per-correct-answer by 5–10× over pure long-context. GraphRAG is roughly tied with RAG on local queries or slightly worse.
- Global queries: GraphRAG beats vanilla RAG on correctness by 30–50%; pure long-context matches GraphRAG's correctness but at 10–20× the cost.
- The right production architecture is a router: *detect whether the query is local or global, route local to RAG and global to GraphRAG or LazyGraphRAG.* This is Kiela's "RAG plus long context" thesis operationalized.

**Variant — if you have a much smaller corpus (<100K tokens total).** Pure long-context may dominate on both cost and correctness because retrieval overhead isn't worth it. This is the honest answer to "when does long-context obsolete RAG?" — when the corpus fits in the window and is static.

## Problem set

**Problem 1 — Take a defensible position on long-context vs RAG for enterprise QA in 2026.** Defend or refute: *"For enterprise QA workloads in 2026 at enterprise scale (millions-to-billions of tokens, mixed local and global queries, per-user SLA < 3s), long-context has not obsoleted RAG; retrieval-based architectures still win on cost-per-correct-answer."* Cite ≥4 sources: at least one from the pro-long-context side (Gemini 1.5 technical report, Anthropic 1M context announcement, Kamradt needle-in-a-haystack), at least one from the anti-long-context side (Lost in the Middle, RULER, Chroma Context Rot, Husain). Include ≥1 benchmark number per side.

**Problem 2 — Design the production router.** For a hybrid system that includes RAG, GraphRAG/LazyGraphRAG, and long-context, write the routing decision logic: what signals (query type, corpus size, latency SLA, cost budget) determine which architecture each query takes? Defend each branch in 2–3 sentences. This can be written as pseudocode or a decision tree — no implementation needed.

**Problem 3 — Name GraphRAG's earn-its-cost zone.** Name one specific query class (in a specific domain — legal, finance, marketing, healthcare, ops, or your own Block 1 niche) where GraphRAG's 10–100× ingestion cost is *strictly* worth paying, and one specific query class where it is *strictly* not. Defend each with a sentence on why the graph structure is or isn't load-bearing. If the first one is "global sensemaking" you need to be more specific than that — what global sensemaking query in what domain.

**Problem 4 — Reproduce a Lost-in-the-Middle-style finding on Claude Opus 4.8.** Ask Claude Code to construct a 500K-token synthetic document with 5 target facts inserted at depths of 5%, 25%, 50%, 75%, and 95% of the way through. Query Claude Opus 4.8 (or Fable 5) for each fact and report accuracy by depth across at least 10 trials per position. Does the U-shape hold? Does it hold as strongly as on earlier models, or has frontier-model improvement flattened it? Write 200 words on your result and what it implies for long-context routing decisions.

**Problem 5 — Design the minimal agentic-retrieval loop with stop conditions.** Write the prompt + tool schema for a 3-hop retrieval loop with explicit stop conditions. The agent should retrieve, decide whether to retrieve again, and stop when either (a) it can answer the query confidently, (b) three retrievals have occurred, or (c) the cumulative retrieved-token budget has exceeded a threshold you name. Defend the stop criteria in 200 words. This is writeable as a JSON tool-schema block + a system prompt — you don't need to run it to complete the problem.

## Common failure modes at scale

**Mode 1 — GraphRAG ingestion cost surprises a pilot into a no-go.** A common pattern: teams pilot GraphRAG on a 100K-token corpus, it works, they scale to 50M tokens, and discover the indexing bill is $2,000–$10,000 in LLM calls. This is not a technical failure — the paper's token-per-corpus math is public — but it's a common budgeting miss. The fix is either LazyGraphRAG (1000× lower indexing cost) or scoping the graph to a meaningful subset of the corpus.

**Mode 2 — Agentic-retrieval latency hits a user-experience wall.** A 3-hop Self-RAG-style loop that was fine in dev becomes a product-killer at 8–12 seconds per query in an interactive chat UI. The fix is almost always architectural, not parametric: move the multi-hop work to a background pipeline that precomputes answers to expected query patterns, or fall back to single-shot RAG with excellent reranking for the interactive path.

**Mode 3 — Long-context cost blow-up in production.** A team moves from RAG to long-context because "it's simpler," hits the generally-available 1M window at standard pricing, and blows through budget because *every* query now pays the full-window input-token cost. A 10K-query/day workflow on a 500K-token corpus runs $25K/month just in input tokens. The fix is to re-introduce retrieval as a pre-filter (Kiela's architecture), narrowing the window to 50–200K before the model reads it.

**Mode 4 — Citation pipelines that look correct but aren't grounded.** Pipelines that enforce structural citations (Anthropic Citations API or instructor schemas) pass operator-level review — every claim has a pointer. But Layer 3 entailment is skipped, and the cited span does not actually support the claim. This shows up in regulated-domain audits where a human reviewer finds the claim isn't in the cited passage. The fix is always to add the entailment-judge layer, which is the one teams most commonly skip because it costs real eval budget.

**Mode 5 — Context rot on coherent documents.** Teams load a single 300K-token document (annual report, long contract) into Claude's 1M window and see quality *worse* than on their older RAG pipeline. Chroma's Context Rot finding is the culprit: structurally coherent long documents *hurt* retrieval accuracy compared to shuffled haystacks.[^chroma] The fix is to either chunk and retrieve (back to RAG) or to intentionally restructure the long document — a counterintuitive "structured retrieval on an unstructured look" that preserves navigability inside the long window.

## Open questions / what's not settled

**Question 1 — Does LazyGraphRAG's 1000× cost advantage generalize across domains?** Microsoft's November 2024 numbers are impressive on their test corpora; the 2025 third-party *"How Significant Are the Real Performance Gains?"* evaluation challenges some of the transferability claims. The live debate: is LazyGraphRAG the structural successor to GraphRAG, or a clever hack that falls apart on corpora where the on-demand community extraction can't see enough structure?

**Question 2 — Can long-context + context-engineering close the RAG gap for regulated domains?** Kiela's Contextual AI position is *"RAG plus long context."* But operators in regulated domains need claim-level citations (structural requirement), and long-context without retrieval loses the natural chunk-level granularity that grounds citations. The unsettled question: does the citation-grounding requirement always push the architecture back to retrieval, or can prompt-engineered citation from a 1M window meet regulatory bars? Endex's 0% hallucination rate with Anthropic Citations API is a data point for "yes, eventually"; most current production deployments are still retrieval-based.

**Question 3 — Is agentic retrieval a transitional architecture?** Self-RAG, CoRAG, LangGraph-style loops exist because retrieval is imperfect and models can iterate. If frontier models' long-context + reasoning capabilities close the multi-hop gap (RULER-style tasks become solved at 200K), does agentic retrieval collapse back into single-shot long-context with a good reranker? Eugene Yan's pattern post has hinted at this; the 2026 evidence is ambiguous.

## Reviewer lens — named critics with specific disagreements

- **Darren Edge (Microsoft Research, lead author of the GraphRAG paper, arxiv 2404.16130).**[^graphrag] Edge would push back on this lesson's line *"GraphRAG is a good fit only if the corpus is relatively stable and global sensemaking queries are a meaningful fraction of the workload."* His counter-position, articulated in Microsoft's follow-up LazyGraphRAG blog, is that the GraphRAG toolkit is increasingly a *family* of approaches — full GraphRAG for high-stakes, stable corpora; LazyGraphRAG for dynamic workloads; drift-aware incremental indexing for streaming corpora. Lumping all "GraphRAG" under one cost profile is outdated by his team's own 2024 releases.[^lazygraph]

- **Nelson F. Liu (Stanford, first author of *Lost in the Middle*, TACL 2024).**[^lim] Liu would push back on this lesson's treatment of the U-shape finding as *"still broadly true for 2026 frontier models."* His original paper was on 2023-era models. He has publicly noted that the U-shape is *smaller* on newer models but not gone, and that newer frontier-model evaluations (RULER, Chroma's context rot study) surface different degradation modes than the original middle-position finding. The lesson should carry that calibration: Lost-in-the-Middle is a real effect, but its 2026 magnitude is task-specific.

- **Jerry Liu (LlamaIndex CEO, *Towards Long Context RAG* blog, 2024).**[^jerryliu] Jerry Liu would push back on the binary framing "RAG vs long-context" in the Layer 3 section. His public position, in his 2024 long-context blog and talks, is that the right architecture is *hierarchical retrieval* — small-to-big, with retrieval narrowing the window and long-context reasoning across the narrowed window. He would argue the lesson's cost-per-correct-answer table in the Runnable Experiment undersells the hybrid architecture where retrieval and long-context compose rather than compete.

- **Jason Liu (Instructor creator, jxnl.co, *Systematically Improving RAG* course).**[^jxnl] Jason Liu would push back on this lesson's characterization of citation grounding as solved-by-API. His position: the real grounding problem is at the *schema + evaluation* layer, not the API layer. Instructor + rigorous evaluation catches failure modes (quote-drift, entailment failures) that the Anthropic Citations API alone does not. He would push on Layer 4's three-layer grounding check to be more prescriptive about Layer 3 (entailment judge) quality — and to ground that judge in its own validation against human labels, which is the Hamel Husain / parlance-labs pattern.

- **Akari Asai (University of Washington → AI2, first author of Self-RAG, arxiv 2310.11511).**[^selfrag] Asai would push back on the lesson's framing of Self-RAG as "approximated by prompt-engineered workflows in production." Her empirical result is that the *trained* reflection tokens outperform prompted workflows on citation accuracy and factuality — the training is doing real work that prompting can't fully replicate. The lesson undersells this because it's written for operators who won't train custom models, but she would argue that *for high-stakes domains (medicine, law, policy) the training investment pays back in citation-accuracy*, and operators who dismiss it are leaving reliability on the table.

## Further reading

### Must (read before next week's eval lesson)

- **Edge et al., "From Local to Global: A Graph RAG Approach to Query-Focused Summarization" (arxiv 2404.16130).**[^graphrag] The paper.
- **Microsoft Research, "LazyGraphRAG: Setting a new standard for quality and cost" (November 25, 2024).**[^lazygraph] The cost-efficient successor.
- **Liu et al., "Lost in the Middle: How Language Models Use Long Contexts" (TACL 2024).**[^lim] The U-shape paper.
- **Hsieh et al., "RULER: What's the Real Context Size of Your Long-Context Language Models?" (arxiv 2404.06654).**[^ruler] The benchmark that looks past NIAH.
- **Anthropic, "Introducing Citations" (January 23, 2025).**[^citations] The API announcement.

### Recommended

- **Chroma, "Context Rot: How Increasing Input Tokens Impacts LLM Performance" (July 2025).**[^chroma] 18 frontier models tested.
- **Anthropic, "Introducing Contextual Retrieval" (September 19, 2024).**[^ctx] The Thursday reference refreshed with Friday's lens.
- **Asai et al., "Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection" (arxiv 2310.11511).**[^selfrag] The learned-retrieval paper.
- **Wang et al., "Chain-of-Retrieval Augmented Generation" (arxiv 2501.14342).**[^corag] Multi-hop at scale.
- **Gemini 1.5 Technical Report (Reid et al., arxiv 2403.05530).**[^gem15] The needle-in-a-haystack near-perfect recall results at 1M and 10M tokens.
- **Anthropic model docs / pricing (July 2026) — Fable 5, Opus 4.8, Sonnet 5 at 1M context; the new tokenizer note.**[^claude1m]
- **Jerry Liu, "Towards Long Context RAG" (LlamaIndex blog, 2024).**[^jerryliu] The hybrid architecture position.
- **Simon Willison, "Anthropic's new Citations API" (January 24, 2025).**[^simonwillison] The operator's take on limits.

### Optional

- **Zhang et al., "RAFT: Adapting Language Model to Domain Specific RAG" (arxiv 2403.10131).**[^raft] Fine-tuning counterpart.
- **Tang & Yang, "MultiHop-RAG" (COLM 2024, arxiv 2401.15391).**[^multihoprag] The multi-hop benchmark.
- **Hamel Husain, "P6: Context Rot" (hamel.dev).**[^hamelrot] Operator's commentary on Chroma's research.
- **Eugene Yan, "Patterns for Building LLM-based Systems & Products" (eugeneyan.com).**[^eugeneyan] The pattern catalog.
- **Jason Liu, "Systematically Improving RAG" (jxnl.co).**[^jxnl]
- **Douwe Kiela, "RAG is dead, long live RAG!" (Contextual AI blog).**[^kiela]

## Citations

[^graphrag]: Edge, D., Trinh, H., Cheng, N., Bradley, J., Chao, A., Mody, A., Truitt, S., Metropolitansky, D., Ness, R. O., Larson, J. (2024). *From Local to Global: A Graph RAG Approach to Query-Focused Summarization.* arxiv 2404.16130, submitted April 24, 2024; last revised February 19, 2025. <https://arxiv.org/abs/2404.16130>. Supports: GraphRAG construction pipeline, Leiden community detection, 1M-token corpus benchmarks, 26–97% token reduction claims.

[^lazygraph]: Microsoft Research (November 25, 2024). *LazyGraphRAG: Setting a new standard for quality and cost.* <https://www.microsoft.com/en-us/research/blog/lazygraphrag-setting-a-new-standard-for-quality-and-cost/>. Supports: 0.1% indexing cost, 4% query cost, comparable-or-better quality on global and local queries.

[^writerkg]: Writer, *RAG benchmarking: Writer Knowledge Graph ranks #1*, engineering blog. <https://writer.com/engineering/rag-benchmark/> — source for the RobustQA knowledge-graph-RAG number (86.31%) vs vector-RAG baselines (32.74–75.89%). This is Writer's own benchmark on its own product — a vendor-disclosed figure, not the Microsoft LazyGraphRAG post an earlier draft of this vault misattributed it to. Verified 2026-07-17.

[^graphgains]: Wu et al., *How Significant Are the Real Performance Gains? An Unbiased Evaluation Framework for GraphRAG*, arxiv 2506.06331, June 2025. <https://arxiv.org/abs/2506.06331> — bias-corrected re-evaluation of GraphRAG methods; LightRAG's reported Agriculture-dataset win rates (66.70% vs NaiveRAG, 56.38% vs MGRAG) drop to 39.06% and 32.33% under the unbiased framework, with high tie rates shrinking real gaps. Verified 2026-07-17.

[^lim]: Liu, N. F., Lin, K., Hewitt, J., Paranjape, A., Bevilacqua, M., Petroni, F., Liang, P. (2024). *Lost in the Middle: How Language Models Use Long Contexts.* Transactions of the Association for Computational Linguistics (TACL), February 2024. <https://aclanthology.org/2024.tacl-1.9/>. Original arxiv 2307.03172. Supports: U-shaped accuracy curve with ~30% drop when answer document is at position 10 of 20.

[^ruler]: Hsieh, C.-P., Sun, S., Kriman, S., Acharya, S., Rekesh, D., Jia, F., Ginsburg, B. (NVIDIA, 2024). *RULER: What's the Real Context Size of Your Long-Context Language Models?* arxiv 2404.06654, April 2024. <https://arxiv.org/abs/2404.06654>. Supports: 13 long-context tasks across 4 categories; most 32K-claimed models fail to maintain performance at 32K.

[^gem15]: Gemini Team, Google DeepMind (2024). *Gemini 1.5: Unlocking multimodal understanding across millions of tokens of context.* arxiv 2403.05530. <https://arxiv.org/abs/2403.05530>. Supports: >99.7% needle-in-haystack recall at 1M tokens; 99.2% at 10M tokens. Currency note (2026-07-17): the current Google frontier is **Gemini 3 Pro** (released Nov 18 2025, 1M-token window); Gemini 2.5 Pro also ships 1M (not the 2M sometimes attributed to it — 2M was a 1.5-Pro-era spec). Sources: https://blog.google (Gemini 3 launch), https://ai.google.dev/gemini-api/docs/long-context.

[^claude1m]: Anthropic model docs and pricing, July 2026. <https://platform.claude.com/docs/en/about-claude/models/overview> and <https://www.anthropic.com/news/claude-fable-5-mythos-5>. 1M context is standard across the current lineup — Claude Fable 5 ($10/$50 per Mtok), Opus 4.8 ($5/$25), Sonnet 5 ($2/$10 intro through Aug 31 2026, then $3/$15) — 128K max output. The 1M-GA lineage traces to Anthropic's March 13, 2026 "1M context GA for Opus 4.6 and Sonnet 4.6" (<https://claude.com/blog/1m-context-ga>). New tokenizer: Opus 4.7 introduced a tokenizer (shared by Opus 4.8 / Sonnet 5 / Fable 5) that tokenizes the same text to ~30% more tokens than pre-4.7 models — re-baseline token counts and cost with `count_tokens`. Verified 2026-07-17.

[^selfrag]: Asai, A., Wu, Z., Wang, Y., Sil, A., Hajishirzi, H. (2023). *Self-RAG: Learning to Retrieve, Generate, and Critique through Self-Reflection.* arxiv 2310.11511, October 17, 2023. <https://arxiv.org/abs/2310.11511>. Supports: reflection-token architecture; 7B/13B variants outperforming ChatGPT and retrieval-augmented Llama2-chat.

[^corag]: Wang, L., Chen, H., Yang, N., Huang, X., Dou, Z., Wei, F. (2025). *Chain-of-Retrieval Augmented Generation.* arxiv 2501.14342, January 24, 2025. <https://arxiv.org/abs/2501.14342>. Supports: >10 EM-point improvements on multi-hop QA; SOTA on KILT.

[^raft]: Zhang, T., Patil, S. G., Jain, N., Shen, S., Zaharia, M., Stoica, I., Gonzalez, J. E. (2024). *RAFT: Adapting Language Model to Domain Specific RAG.* arxiv 2403.10131, March 2024. <https://arxiv.org/abs/2403.10131>. Supports: distractor-aware fine-tuning recipe for domain-specific RAG.

[^ctx]: Anthropic (September 19, 2024). *Introducing Contextual Retrieval.* <https://www.anthropic.com/news/contextual-retrieval>. Supports: 49% top-20 retrieval failure-rate reduction combining Contextual Embeddings + Contextual BM25; 67% with reranking.

[^citations]: Anthropic (January 23, 2025). *Introducing Citations on the Anthropic API.* <https://www.anthropic.com/news/introducing-citations-api> (and <https://claude.com/blog/introducing-citations-api>). Supports: structural citations, up to 15% recall-accuracy improvement over custom implementations; Endex 10%→0% hallucination rate and 20% reference increase.

[^chroma]: Hong, K., Troynikov, A., Huber, J. (Chroma Research, July 2025). *Context Rot: How Increasing Input Tokens Impacts LLM Performance.* <https://research.trychroma.com/context-rot>. Supports: 18 frontier models tested; degradation on simple tasks; coherent documents hurt performance; 200K-window models degrading at 50K.

[^kiela]: Kiela, D. / Contextual AI. *RAG is dead, long live RAG!* <https://contextual.ai/blog/is-rag-dead-yet>. And Contextual AI research: *Introducing RAG 2.0.* <https://contextual.ai/research/introducing-rag2>. Supports: the "RAG plus long context" architecture position.

[^jerryliu]: Liu, J. (LlamaIndex, 2024). *Towards Long Context RAG.* <https://www.llamaindex.ai/blog/towards-long-context-rag>. Supports: small-to-big retrieval, hierarchical indexing, hybrid long-context + retrieval architectures.

[^hamelrot]: Husain, H. (2025). *P6: Context Rot.* hamel.dev. <https://hamel.dev/notes/llm/rag/p6-context_rot.html>. Supports: operator commentary on Chroma's context-rot findings; differential failure modes of GPT vs Claude class models under context rot.

[^hamelx]: Husain, H. (July 2024). X post on RAG vs long-context. <https://x.com/HamelHusain/status/1811050329972322708>. Quote: *"I'm seeing lots of takes that RAG will become irrelevant bc of long context windows. Reasons I think this is BS — You often want to filter by metadata (dates, # of views, etc). Search/IR is critical in many applied scenarios."*

[^niah]: Kamradt, G. (2023). *LLMTest_NeedleInAHaystack.* GitHub repository: <https://github.com/gkamradt/LLMTest_NeedleInAHaystack>. And Kamradt's original X thread on GPT-4 128K and Claude 2.1 200K NIAH results. Supports: founding evaluation of long-context recall; GPT-4 degradation above 64K before frontier updates.

[^multihoprag]: Tang, Y., Yang, Y. (2024). *MultiHop-RAG: Benchmarking Retrieval-Augmented Generation for Multi-Hop Queries.* arxiv 2401.15391 (COLM 2024). <https://arxiv.org/abs/2401.15391>. Supports: existing RAG methods perform unsatisfactorily on multi-hop queries.

[^simonwillison]: Willison, S. (January 24, 2025). *Anthropic's new Citations API.* <https://simonwillison.net/2025/Jan/24/anthropics-new-citations-api/>. Supports: operator-level critique that Citations API solves formatting and quote-drift but not claim entailment.

[^jxnl]: Liu, J. (jxnl.co). *Systematically Improving RAG Applications* course and *Applications RAG* documentation. <https://jxnl.co/systematically-improve-your-rag/>, <https://jxnl.github.io/instructor/tutorials/3-0-applications-rag/>. Supports: Instructor library for schema-enforced structured outputs; Pydantic-based validation; 6M+ monthly downloads.

[^eugeneyan]: Yan, E. *Patterns for Building LLM-based Systems & Products.* <https://eugeneyan.com/writing/llm-patterns/>. Supports: pattern catalog for production LLM systems, including critique of self-reflection loops under production constraints.

_last_verified: 2026-07-17_
