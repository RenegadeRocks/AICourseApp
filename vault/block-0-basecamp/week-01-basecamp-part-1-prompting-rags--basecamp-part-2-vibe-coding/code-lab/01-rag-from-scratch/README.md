# Code Lab 01: RAG From Scratch

Build a working RAG pipeline from first principles:
chunking → embedding → FAISS indexing → contextual enrichment → retrieval → generation.

## What you'll learn

- How naive RAG works (and exactly where it breaks)
- How Anthropic's contextual retrieval enriches each chunk before indexing
- How to query with FAISS and pass context to Claude
- How retrieval quality degrades without contextual enrichment (the key experiment)

## Prerequisites

- Python 3.10+
- An Anthropic API key (for the generation step and contextual enrichment)
- The generation and enrichment steps call the Claude API — no other paid dependencies

## Setup

```bash
# 1. Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Download NLTK sentence tokenizer data (one-time)
python -c "import nltk; nltk.download('punkt_tab')"

# 4. Set your Anthropic API key
export ANTHROPIC_API_KEY="sk-ant-..."   # Windows: set ANTHROPIC_API_KEY=sk-ant-...

# 5. Run the demo
python rag_demo.py
```

## What the demo does

1. Loads a sample FAQ document (included in `sample_docs/`)
2. Splits it into overlapping chunks with sentence-aware boundaries
3. Generates a contextual description for each chunk using Claude Haiku (the contextual enrichment step)
4. Embeds all contextual chunks with `sentence-transformers/all-MiniLM-L6-v2`
5. Builds a FAISS index
6. Accepts a query, embeds it, retrieves top-3 chunks
7. Generates an answer with Claude using the retrieved context
8. Repeats the experiment WITHOUT contextual enrichment and compares retrieval

## Key experiment

After the basic demo runs, it automatically runs a comparison:

```
=== WITH contextual enrichment ===
Query: "What is the refund policy for annual plans?"
Retrieved chunk 1: [context-enriched chunk about refund policies]
...

=== WITHOUT contextual enrichment (naive) ===
Query: "What is the refund policy for annual plans?"
Retrieved chunk 1: [may be a different, less relevant chunk]
...
```

This demonstrates empirically why contextual retrieval matters. The difference should be visible in chunk relevance.

## File structure

```
01-rag-from-scratch/
├── README.md                  ← you are here
├── requirements.txt
├── rag_demo.py                ← main demo (run this)
├── chunker.py                 ← sentence-aware chunking with overlap
├── embedder.py                ← sentence-transformer wrapper
├── retriever.py               ← FAISS index build + query
├── contextual_enricher.py     ← calls Claude Haiku to enrich chunks
├── generator.py               ← calls Claude to generate final answer
└── sample_docs/
    └── acme_faq.txt           ← sample FAQ document (no API key needed to read)
```

## API key note

The `ANTHROPIC_API_KEY` environment variable is required for:
- Contextual enrichment (calls Claude Haiku once per chunk at index time)
- Answer generation (calls Claude claude-haiku-4-5-20251001 or claude-sonnet-4-6)

The embedding step (sentence-transformers) and FAISS retrieval run fully locally.

To run the demo WITHOUT an API key (retrieval only, no enrichment, no generation):
```bash
python rag_demo.py --no-api
```
This will show chunking and retrieval without calling Claude.

## Costs

A single demo run with the sample FAQ (~20 chunks):
- Contextual enrichment: ~20 × 200 tokens ≈ 4,000 tokens ≈ $0.001 (Haiku pricing)
- Answer generation: ~1,000 tokens ≈ $0.001
- Total per run: < $0.01
