---
type: flashcards
block: block-0-basecamp
week: week-01
card_count: 25
format: front/back separated by ---
last_verified: 2026-04-14
---

# Week 01 Flashcards — Prompting, RAG, Vibe Coding

> Import into Anki: use the "Basic" card type. Front = Q, Back = A.
> Review cold on Sunday night. Score below 80% = revisit the relevant deep-dive.

---

**Q: What are the four primitives of a Claude prompt?**
A: System prompt (operator instructions, persistent), Human turn (user request + context), Assistant prefill (optional: pre-fill the start of the response to control format), Tool results (structured data returned after a tool call).

---

**Q: What is XML tagging in prompts used for, and why does it work?**
A: XML tags demarcate different sections of a prompt (instructions, data, examples, format). They work because the tokenizer treats tagged regions as structurally distinct, reducing the risk that content in the data section overwrites instructions (prompt injection mitigation).

---

**Q: What is chain-of-thought (CoT) prompting?**
A: Prompting the model to reason step by step before producing a final answer. The zero-shot version: append "Let's think step by step." The few-shot version: provide worked examples that show the reasoning chain, not just the answer. Improves multi-step reasoning tasks; adds latency.

---

**Q: When should you NOT use chain-of-thought prompting?**
A: Classification tasks, simple extraction, sentiment analysis, or any task where the answer is a direct lookup — CoT adds latency and cost with no accuracy benefit, and can introduce arithmetic errors in pure counting/extraction tasks.

---

**Q: What is the "prefill trick" in the Claude API?**
A: Pass `{"role": "assistant", "content": "{"}` as the last message. Claude continues from the opening brace, guaranteeing the output starts as JSON — preventing preamble like "Sure! Here is the JSON:".

---

**Q: What is prompt injection, and name one mitigation?**
A: Prompt injection is when hostile content in the data portion of a prompt (user input, retrieved document, web scrape) overwrites the model's instructions. Mitigations: (1) XML tag separation of instructions and data, (2) sanitize user input before injecting into prompts, (3) place critical constraints at both the top and end of the system prompt.

---

**Q: Why do experts recommend placing the most important constraint at both the top and end of a system prompt?**
A: Attention is unevenly distributed in transformers — the model attends more strongly to tokens at the start and end of context. Placing a critical constraint at both positions increases the probability that the model attends to it during generation of the relevant output.

---

**Q: What is structured output / JSON mode, and why does it matter?**
A: Constraining the model's output to valid JSON matching a specific schema. Matters because downstream code that parses model output fails silently or throws exceptions on malformed JSON — production reliability requires structured output when the output feeds into code.

---

**Q: What are the 5 steps of a naive RAG pipeline?**
A: (1) Chunk documents into overlapping segments. (2) Embed each chunk with a sentence-transformer. (3) Index embeddings in a vector database (e.g., FAISS). (4) At query time: embed the question, retrieve top-k most similar chunks. (5) Augment the prompt with retrieved chunks and generate the answer.

---

**Q: What is the core problem naive RAG has with chunk isolation?**
A: A chunk may contain a key claim (e.g., "$2.3M revenue") but the qualifying context (e.g., "for Q3 EMEA") lives in an adjacent chunk. After chunking, the model retrieves the claim without the qualifier, leading to misleading or incomplete answers.

---

**Q: What is contextual retrieval (Anthropic, Sep 2024)?**
A: Before indexing a chunk, prepend a 1-2 sentence LLM-generated description of what the chunk covers and where it fits in the document. This gives each chunk enough stand-alone context to be retrieved accurately, even when the question uses different vocabulary.

---

**Q: What percentage improvement did Anthropic's full contextual retrieval stack (enrichment + BM25 + reranking) achieve over naive embedding-only RAG?**
A: 67% reduction in retrieval failures (versus naive embedding-only baseline).

---

**Q: What is BM25, and what role does it play in hybrid RAG search?**
A: BM25 (Best Match 25) is a classical information retrieval algorithm that scores documents by term frequency × inverse document frequency — exact keyword matching. In hybrid search, BM25 runs in parallel with dense embedding search and the results are merged (e.g., with Reciprocal Rank Fusion). BM25 catches exact phrase matches that embeddings miss.

---

**Q: What is the difference between a bi-encoder and a cross-encoder?**
A: Bi-encoder: encodes query and document separately, compares embeddings (fast, precomputable). Cross-encoder: encodes the (query, document) pair jointly, outputs a relevance score (more accurate, cannot precompute). Use bi-encoder for first-stage retrieval; cross-encoder for second-stage reranking over a small candidate set.

---

**Q: Name four RAG evaluation metrics.**
A: (1) Retrieval recall — does the correct chunk appear in top-k? (2) Answer correctness — is the final answer right? (3) Faithfulness — are all claims in the answer grounded in the context? (4) Groundedness / attribution — can every claim be traced to a specific passage?

---

**Q: What is RAGAS?**
A: An open-source Python library (arXiv:2309.15217) that automates RAG evaluation. It computes faithfulness, answer correctness, context precision, and context recall from the (question, answer, context) triple without requiring a human label for every example.

---

**Q: What is vibe coding (Karpathy, Feb 2025)?**
A: A mode of software development where you describe what you want in natural language, accept the model's generated code with minimal review, run it, and iterate by describing what to fix — fully trusting the model and moving fast. Coined by Andrej Karpathy on X/Twitter in February 2025.

---

**Q: Name the three modes of AI-assisted coding.**
A: (1) Copilot mode — autocomplete while typing, you read every suggestion. (2) Agentic coding (spec-driven) — model reads your repo, implements a plan, you review at checkpoints. (3) Vibe coding (prompt-driven, zero-review) — describe → generate → run → iterate, no code reading.

---

**Q: When is vibe coding irresponsible?**
A: When the code handles user data, authentication, payment processing, PII, or runs in a regulated environment. The generated code may contain unvalidated inputs, SQL injection, insecure cookie handling, or missing rate limits — risks that require human review.

---

**Q: What is a `.cursorrules` file?**
A: A project-level configuration file in Cursor that defines standing instructions for every AI session in that project: language, framework, code style, test requirements, forbidden patterns. Equivalent to an operator-level system prompt for the AI coding tool.

---

**Q: When would you choose Claude Code over Bolt for vibe coding?**
A: Choose Claude Code when: you have an existing codebase to modify, you need to run terminal commands (git, pip, docker), you're doing infrastructure work (CI/CD, cron jobs, environment setup), or you need multi-session refactors with context persistence. Bolt is better for greenfield JS/TS apps with no local setup.

---

**Q: What is the primary competitive advantage of Lovable over Bolt?**
A: Lovable generates a React frontend AND a Supabase backend (PostgreSQL + auth + storage) in one step, including row-level security policies. Bolt focuses on frontend JavaScript apps without native database/auth integration.

---

**Q: What is the "spec-first" discipline in vibe coding?**
A: Writing a one-page specification (what, who, features ranked, stack, constraints, success definition) before opening any AI coding tool. The spec replaces ambiguous natural language with a precise contract, dramatically improving output quality because the model spends its context budget on implementation rather than interpretation.

---

**Q: What is GraphRAG (Microsoft Research, 2024)?**
A: An extension of RAG that builds a knowledge graph from documents (entity extraction, community detection, LLM summarization), then combines graph traversal with vector search to answer multi-hop queries. Best for knowledge bases with complex entity relationships; operationally heavier than standard contextual retrieval.

---

**Q: What is the "lost in the middle" phenomenon in RAG and LLM prompting?**
A: Model performance on information placed in the middle of long contexts degrades significantly — the model attends strongly to content at the beginning and end of the context window but loses track of content buried in the middle. Implication: put the most important context (retrieved chunks) at the beginning of the augmented prompt, not the middle.

---

_last_verified: 2026-04-14_
