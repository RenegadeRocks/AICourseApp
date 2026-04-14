"""
rag_demo.py — Full RAG pipeline demo with contextual retrieval comparison.

Usage:
    python rag_demo.py              # Full demo (requires ANTHROPIC_API_KEY)
    python rag_demo.py --no-api     # Retrieval only, no Claude calls

What this demonstrates:
    1. Naive RAG (chunk → embed → retrieve)
    2. Contextual RAG (chunk → enrich with Claude → embed → retrieve)
    3. Side-by-side comparison showing retrieval quality improvement
    4. Answer generation from retrieved context

Based on:
    Anthropic, "Introducing Contextual Retrieval," Sep 2024
    https://www.anthropic.com/news/contextual-retrieval

    Lewis et al., "RAG for Knowledge-Intensive NLP Tasks," arXiv:2005.11401
    https://arxiv.org/abs/2005.11401
"""

import argparse
import os
import pathlib
import sys

from chunker import load_and_chunk_file
from embedder import Embedder
from retriever import VectorIndex

# Default document
SAMPLE_DOC = pathlib.Path(__file__).parent / "sample_docs" / "acme_faq.txt"

# Test queries — these are chosen to stress-test retrieval
TEST_QUERIES = [
    "What is the refund policy for annual plans?",
    "Does ACME support SSO and which identity providers?",
    "How many API requests per hour can I make on the Growth plan?",
    "Is customer data encrypted and where is it stored?",
]


def build_naive_index(chunks: list[dict], embedder: Embedder) -> VectorIndex:
    """Build a FAISS index using raw (unenriched) chunk text."""
    texts = [c["text"] for c in chunks]
    embeddings = embedder.embed(texts, show_progress=False)
    index = VectorIndex(embedding_dim=embedder.embedding_dim)
    index.add_chunks(chunks, embeddings)
    return index


def build_contextual_index(
    chunks: list[dict],
    document_text: str,
    embedder: Embedder,
) -> VectorIndex:
    """
    Build a FAISS index using contextually enriched chunks.
    Calls Claude Haiku once per chunk at index time.
    """
    from contextual_enricher import enrich_all_chunks

    print(f"\nEnriching {len(chunks)} chunks with Claude Haiku...")
    enriched_chunks = enrich_all_chunks(chunks, document_text)

    texts = [c["text"] for c in enriched_chunks]
    embeddings = embedder.embed(texts, show_progress=False)
    index = VectorIndex(embedding_dim=embedder.embedding_dim)
    index.add_chunks(enriched_chunks, embeddings)
    return index


def print_retrieval_results(query: str, results, label: str) -> None:
    """Pretty-print retrieval results."""
    print(f"\n{'='*60}")
    print(f"  {label}")
    print(f"  Query: {query}")
    print(f"{'='*60}")
    for i, r in enumerate(results, 1):
        # Show first 200 characters of the chunk text
        preview = r.text[:200].replace("\n", " ")
        if len(r.text) > 200:
            preview += "..."
        print(f"\n  [{i}] Score: {r.score:.4f}")
        print(f"      {preview}")


def run_comparison(
    query: str,
    naive_index: VectorIndex,
    contextual_index: VectorIndex,
    embedder: Embedder,
    k: int = 3,
) -> None:
    """Run the same query on both indexes and compare."""
    q_emb = embedder.embed_single(query)

    naive_results = naive_index.search(q_emb, k=k)
    print_retrieval_results(query, naive_results, "NAIVE RAG (no enrichment)")

    contextual_results = contextual_index.search(q_emb, k=k)
    print_retrieval_results(query, contextual_results, "CONTEXTUAL RAG (Anthropic method)")


def run_full_qa(
    query: str,
    contextual_index: VectorIndex,
    embedder: Embedder,
    k: int = 3,
) -> None:
    """Retrieve from contextual index and generate an answer with Claude."""
    from generator import generate_answer

    q_emb = embedder.embed_single(query)
    results = contextual_index.search(q_emb, k=k)

    print(f"\n{'='*60}")
    print(f"  ANSWER GENERATION")
    print(f"  Query: {query}")
    print(f"{'='*60}")

    result = generate_answer(query, results)
    print(f"\nAnswer:\n{result['answer']}")
    print(f"\n[{result['model']} | {result['input_tokens']} in / {result['output_tokens']} out tokens]")


def main():
    parser = argparse.ArgumentParser(description="RAG pipeline demo")
    parser.add_argument(
        "--no-api",
        action="store_true",
        help="Skip Claude API calls (no enrichment, no generation). Shows retrieval only.",
    )
    parser.add_argument(
        "--doc",
        type=str,
        default=str(SAMPLE_DOC),
        help="Path to the document to index.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=2,
        help="Number of chunks to retrieve (default: 2)",
    )
    args = parser.parse_args()

    if not args.no_api and not os.environ.get("ANTHROPIC_API_KEY"):
        print("ERROR: ANTHROPIC_API_KEY not set.")
        print("  Set it with: export ANTHROPIC_API_KEY='sk-ant-...'")
        print("  Or run with --no-api for retrieval-only mode (no Claude calls).")
        sys.exit(1)

    # --- Step 1: Load and chunk the document ---
    print(f"\n{'='*60}")
    print(f"  STEP 1: Loading and chunking {args.doc}")
    print(f"{'='*60}")
    chunks = load_and_chunk_file(args.doc, max_words_per_chunk=150, overlap_sentences=2)
    with open(args.doc, "r", encoding="utf-8") as f:
        document_text = f.read()
    print(f"Produced {len(chunks)} chunks from {len(document_text)} characters.")

    # --- Step 2: Load embedding model ---
    print(f"\n{'='*60}")
    print(f"  STEP 2: Loading embedding model")
    print(f"{'='*60}")
    embedder = Embedder("all-MiniLM-L6-v2")

    # --- Step 3: Build naive index ---
    print(f"\n{'='*60}")
    print(f"  STEP 3: Building NAIVE index (no enrichment)")
    print(f"{'='*60}")
    naive_index = build_naive_index(chunks, embedder)

    if args.no_api:
        # No-API mode: just demonstrate naive retrieval on a few queries
        print("\n[--no-api mode: showing naive retrieval only]\n")
        q_emb = embedder.embed_single(TEST_QUERIES[0])
        results = naive_index.search(q_emb, k=args.k)
        print_retrieval_results(TEST_QUERIES[0], results, "NAIVE RAG")
        print("\nRun without --no-api to see contextual enrichment comparison and answer generation.")
        return

    # --- Step 4: Build contextual index ---
    print(f"\n{'='*60}")
    print(f"  STEP 4: Building CONTEXTUAL index (Anthropic method)")
    print(f"{'='*60}")
    contextual_index = build_contextual_index(chunks, document_text, embedder)

    # --- Step 5: Comparison run ---
    print(f"\n{'#'*60}")
    print(f"  COMPARISON: NAIVE vs CONTEXTUAL RETRIEVAL")
    print(f"{'#'*60}")

    for query in TEST_QUERIES[:2]:  # compare first 2 queries to keep runtime short
        run_comparison(query, naive_index, contextual_index, embedder, k=args.k)

    # --- Step 6: Full QA with generation ---
    print(f"\n{'#'*60}")
    print(f"  FULL QA: CONTEXTUAL RETRIEVAL + GENERATION")
    print(f"{'#'*60}")

    for query in TEST_QUERIES[:2]:
        run_full_qa(query, contextual_index, embedder, k=args.k)

    # --- Step 7: Interactive mode ---
    print(f"\n{'='*60}")
    print("  INTERACTIVE MODE — type a question (or 'quit' to exit)")
    print(f"{'='*60}\n")

    while True:
        try:
            user_query = input("Your question: ").strip()
        except (KeyboardInterrupt, EOFError):
            break
        if not user_query or user_query.lower() in {"quit", "exit", "q"}:
            break
        run_full_qa(user_query, contextual_index, embedder, k=args.k)

    print("\nDone. Review the comparison above to see why contextual retrieval matters.")


if __name__ == "__main__":
    main()
