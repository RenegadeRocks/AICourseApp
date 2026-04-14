---
type: quiz
block: block-0-basecamp
week: week-01
question_count: 12
last_verified: 2026-04-14
---

# Week 01 Quiz — Prompting, RAG, and Vibe Coding

> Take this cold — no lesson files open. That's the only signal that generalizes.
> Aim for 80%+ before next Monday. Score below that = pick your weakest topic and run `/deepen-lesson`.

---

## Questions

### Section A: Prompting Mechanics (Q1–4)

**Q1 (MCQ)**: Which of the following BEST describes why XML tags improve Claude prompts?

A) They make the prompt look more professional  
B) They exploit how the tokenizer separates regions, reducing the risk that data overwrites instructions  
C) XML is a format Claude was specifically fine-tuned to produce  
D) They compress the prompt, reducing token usage  

**Q2 (Short answer)**: What is the "prefill trick" in the Claude API, and what specific output guarantee does it provide?

**Q3 (MCQ)**: You have a task where the model must count the number of times a condition appears in a 200-line CSV. Chain-of-thought prompting would:

A) Dramatically improve accuracy by letting the model reason step-by-step before counting  
B) Not help — CoT is only useful for natural language reasoning tasks, not token-level counting  
C) Hurt performance by using up context window with unnecessary reasoning  
D) Make no difference to accuracy but increase latency  

**Q4 (Short answer)**: A colleague reviews your system prompt and says "you repeated the key constraint twice — once at the top and once at the end. That's redundant." How do you respond?

---

### Section B: RAG Architecture (Q5–8)

**Q5 (MCQ)**: Anthropic's September 2024 contextual retrieval paper reported that contextual chunk enrichment + BM25 hybrid search reduced retrieval failures by approximately:

A) 15%  
B) 35%  
C) 49%  
D) 67%  

**Q6 (Code completion)**: The following Python code has a critical flaw for a production RAG system. Identify it and rewrite the relevant section.

```python
def retrieve(query: str, chunks: list[str], embedder, k: int = 3) -> list[str]:
    query_vec = embedder.encode(query)
    chunk_vecs = embedder.encode(chunks)
    scores = cosine_similarity([query_vec], chunk_vecs)[0]
    top_k_idx = scores.argsort()[-k:][::-1]
    return [chunks[i] for i in top_k_idx]
```

**Q7 (Short answer)**: Explain the difference between a bi-encoder and a cross-encoder in the context of RAG retrieval and reranking. Why can't you use a cross-encoder for first-stage retrieval at scale?

**Q8 (MCQ)**: Which of the following is the BEST definition of "faithfulness" in RAG evaluation?

A) The fraction of user questions that receive a non-empty answer  
B) The fraction of claims in the model's answer that are traceable to the retrieved context  
C) The fraction of relevant documents retrieved in the top-k results  
D) The similarity score between the query embedding and the top retrieved chunk  

---

### Section C: Vibe Coding (Q9–11)

**Q9 (MCQ)**: You need to add OAuth2 authentication to an existing FastAPI + PostgreSQL application. Which tool is the best primary choice?

A) Bolt.new — fastest way to generate authentication code  
B) v0 by Vercel — specialized in authentication component generation  
C) Cursor in agent mode — because it reads your existing codebase and modifies files across the project  
D) Lovable — because it handles auth natively with Supabase  

**Q10 (Short answer)**: Karpathy said he "doesn't even look at the code" in vibe coding. Simon Willison argues this is irresponsible for production code. Give a concrete example where Karpathy's approach is correct, and a concrete example where Willison's caution is essential.

**Q11 (Short answer)**: What is a `.cursorrules` file and what is its equivalent in Claude Code? What category of software engineering concept does this map to?

---

### Section D: Integration (Q12)

**Q12 (Scenario / long form)**: A client has 3,000 internal HR policy documents. They want employees to be able to ask questions and get accurate, cited answers. They've tried vanilla ChatGPT (hallucinations) and basic embedding search (wrong answers). Design a solution. Your answer must address:

1. Chunking strategy
2. Embedding model choice
3. Hybrid search approach
4. Contextual enrichment
5. Reranking decision (yes/no and why)
6. Evals you would implement
7. One risk you would flag to the client

---

## Answer Key

**Q1**: **B** — XML tags exploit tokenizer region separation, providing a structural signal that helps the model distinguish instruction from data, reducing prompt injection risk. Option A is wrong (aesthetics don't matter to a model). Option C is partially true in a loose sense but not the mechanistic reason. Option D is wrong (XML adds tokens, not reduces them).

**Q2**: The prefill trick involves passing `{"role": "assistant", "content": "{"}` as the last message in your API call. Claude will continue from the opening brace, *guaranteeing the output begins as a JSON object* — even if the model might otherwise add preamble like "Sure! Here is the JSON:". The guarantee is specifically about the opening character(s) of the output, not about the validity of the full JSON structure (you still need to validate the complete output).

**Q3**: **B** — CoT improves multi-step *reasoning* tasks. Counting occurrences in a CSV is a token-level pattern matching task that a model performs better with direct instruction than with reasoning steps. In fact, CoT often *hurts* on pure counting/extraction tasks because it introduces additional surface for the model to make arithmetic errors during the reasoning phase rather than focusing on the scan.

**Q4**: The repetition is intentional and has empirical backing. Language models don't "read" prompts sequentially and retain everything equally — attention is unevenly distributed, with stronger attention at the beginning and end of sequences. By placing the critical constraint at both positions, you increase the probability that the model attends to it during the token generation for the relevant output part. The correct response to the colleague is: "Test both versions on a 50-example benchmark. The double constraint will outperform the single one on adversarial inputs."

**Q5**: **C** — 49%. The exact Anthropic numbers: contextual enrichment alone = 35% fewer failures; contextual enrichment + BM25 = 49% fewer; + reranking = 67% fewer. The 67% answer (D) requires *all three* techniques combined.

**Q6**: The flaw is that `embedder.encode(chunks)` is called on the entire chunk list every time a query arrives. For a production system with thousands of chunks, this recomputes all chunk embeddings at query time, which is extremely slow. The fix: pre-compute and store chunk embeddings at index time, load them from the index at query time.

```python
# At index time (run once):
chunk_vecs = embedder.encode(chunks)
# Store chunk_vecs to disk or a FAISS index

# At query time (efficient):
def retrieve(query: str, chunk_vecs, chunks, embedder, k=3):
    query_vec = embedder.encode([query])[0]  # encode single query
    scores = cosine_similarity([query_vec], chunk_vecs)[0]
    top_k_idx = scores.argsort()[-k:][::-1]
    return [chunks[i] for i in top_k_idx]
```

**Q7**: A **bi-encoder** encodes the query and each document separately into embedding vectors, then computes similarity (cosine/dot product). It's fast because document embeddings are precomputed. A **cross-encoder** takes a (query, document) pair as joint input and produces a single relevance score — it's more accurate because it can model interactions between query tokens and document tokens, but it cannot precompute document representations (every query requires re-encoding every candidate document). At scale (millions of chunks), cross-encoding every document for every query is O(n) inference calls per query — computationally infeasible. Solution: bi-encoder for first-stage retrieval (fast, precomputed), cross-encoder for second-stage reranking (accurate, small candidate set of top-20).

**Q8**: **B** — Faithfulness measures whether claims in the answer are grounded in the context. Option C describes retrieval recall (a different metric). Option D describes similarity scoring (not an answer-level metric). Option A is answer coverage (also different).

**Q9**: **C** — Cursor in agent mode reads your existing FastAPI + PostgreSQL codebase, understands the current auth structure (or lack thereof), and modifies files across routes, middleware, and database schema coherently. Bolt generates a fresh app from scratch (doesn't integrate with existing). v0 generates UI components, not backend auth. Lovable generates Supabase apps (a different backend tech) and requires buying into its architecture.

**Q10**: Karpathy's approach is correct for: a Python script that scrapes a public website, formats the data as a CSV, and saves it locally — the stakes are low (personal use, no user data, easily deleted), the feedback loop is instant (run it and see), and reading every line would take longer than running and re-prompting. Willison's caution is essential for: an OAuth callback handler that stores user tokens in a database — a bug here could expose tokens, enable account takeover, or silently drop auth events in a way that's invisible until a security audit.

**Q11**: A `.cursorrules` file is a project-level configuration file in Cursor that contains standing instructions for every AI session in that project — framework, style guide, test requirements, forbidden patterns. Its Claude Code equivalent is the `.claude/` directory, specifically the `CLAUDE.md` or agent configuration files that persist instructions across sessions. The software engineering concept it maps to is an **operator-level system prompt** — persistent, project-wide constraints that sit above individual user instructions. It's analogous to a `eslint.config.js` for AI behavior: the "linter" is the model, and your rules define what "correct" behavior looks like.

**Q12 (Model answer)**:

1. **Chunking**: Use sentence-aware chunking at ~300–400 tokens with 50-token overlap (RecursiveCharacterTextSplitter). HR policies have section-based structure — also split at section headers as natural boundaries. Preserve the document title and section heading in each chunk's metadata.

2. **Embedding model**: `BAAI/bge-small-en-v1.5` (strong on domain-specific English, efficient) or `text-embedding-3-small` (OpenAI, if you're okay with the API dependency). Benchmark both on a 50-question HR QA test set before committing.

3. **Hybrid search**: Dense embedding search + BM25 lexical search, merged with Reciprocal Rank Fusion. HR policies use exact legal terminology (BM25 catches exact phrases); employee questions use natural language (embedding catches semantics). Both are needed.

4. **Contextual enrichment**: Before indexing, for each chunk, call a small LLM (Claude Haiku) with: "Given this document titled [title], section [section], briefly describe what this chunk covers in 1-2 sentences." Prepend that description to the chunk before embedding. One-time cost; pays back on every query.

5. **Reranking**: Yes, for this use case. HR queries are low-volume (< 1000/day for a company), so cross-encoder latency (~300ms) is acceptable. HR policy answers have real liability stakes — reducing retrieval error from 30% to 10% is worth it.

6. **Evals**: (a) Retrieval recall: 100-question labeled test set where the correct source document is known — target ≥85% correct chunk in top-3; (b) Faithfulness: LLM-as-judge scoring whether every claim in the answer appears in the context — target ≥90%; (c) Human spot-check: HR team reviews 20 answers per week, flags incorrect or misleading responses.

7. **Risk to flag**: Stale documents. If an HR policy is updated but the vector index isn't reindexed, employees will receive outdated policy information — a compliance risk. Implement document TTLs or a trigger-based reindex whenever source documents change.

---

_last_verified: 2026-04-14_
