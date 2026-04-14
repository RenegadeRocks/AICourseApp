"""
contextual_enricher.py — Anthropic-style contextual chunk enrichment.

Based on: Anthropic, "Introducing Contextual Retrieval," Sep 19, 2024,
https://www.anthropic.com/news/contextual-retrieval

For each chunk, we call Claude claude-haiku-4-5-20251001 to generate a 1-2 sentence description
of what the chunk covers and where it fits in the document. This description is
prepended to the chunk text before embedding.

Why it works:
  A chunk like "Refunds are available within 30 days" is ambiguous without context.
  After enrichment: "This passage from the ACME FAQ (Billing section) covers the
  refund window for annual billing plans. Refunds are available within 30 days."

  The enriched chunk retrieves correctly even when the query uses different vocabulary
  (e.g., "money back guarantee" vs "refund window").

Cost: ~200 input tokens + ~50 output tokens per chunk via Haiku.
  At Haiku pricing (as of early 2026): ~$0.0003 per chunk.
  A 50-chunk FAQ = ~$0.015 total. One-time at index time.
"""

import os
import anthropic


ENRICHMENT_PROMPT = """\
You are a document indexing assistant. Your job is to write a brief context sentence \
for a chunk of text so that the chunk can be retrieved accurately in isolation.

<document_title>{document_title}</document_title>

<full_document_excerpt>
{document_excerpt}
</full_document_excerpt>

<chunk>
{chunk_text}
</chunk>

Write 1-2 sentences describing:
1. What document this chunk comes from and what that document is about.
2. What specific topic or question this chunk addresses.

Be concise and specific. Do NOT include phrases like "This chunk" or "This passage" — \
start directly with the context. Do NOT repeat the chunk text verbatim.
"""


def enrich_chunk(
    chunk: dict,
    document_excerpt: str,
    client: anthropic.Anthropic,
    model: str = "claude-haiku-4-5-20251001",
) -> dict:
    """
    Enrich a single chunk with contextual description.

    Args:
        chunk: Chunk dict with "text", "document_title", "chunk_id".
        document_excerpt: First ~500 words of the full document (provides document-level context).
        client: Anthropic client instance.
        model: Model to use for enrichment (claude-haiku-4-5-20251001 recommended — cheap + fast).

    Returns:
        New chunk dict with "text" replaced by "context\n\n{original_text}"
        and "enriched": True added.
    """
    prompt = ENRICHMENT_PROMPT.format(
        document_title=chunk.get("document_title", "Unknown"),
        document_excerpt=document_excerpt[:1500],  # limit to ~400 tokens
        chunk_text=chunk["text"],
    )

    response = client.messages.create(
        model=model,
        max_tokens=128,
        messages=[{"role": "user", "content": prompt}],
    )

    context_sentence = response.content[0].text.strip()

    enriched_text = f"{context_sentence}\n\n{chunk['text']}"

    return {
        **chunk,
        "text": enriched_text,
        "original_text": chunk["text"],
        "context_sentence": context_sentence,
        "enriched": True,
    }


def enrich_all_chunks(
    chunks: list[dict],
    document_text: str,
    model: str = "claude-haiku-4-5-20251001",
) -> list[dict]:
    """
    Enrich all chunks with contextual descriptions.

    Args:
        chunks: List of chunk dicts from chunker.py.
        document_text: Full document text (used to extract an excerpt for context).
        model: Model for enrichment.

    Returns:
        List of enriched chunk dicts.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable not set. "
            "Set it with: export ANTHROPIC_API_KEY='sk-ant-...'"
        )

    client = anthropic.Anthropic(api_key=api_key)

    # Use the first 1500 characters as the document-level context
    document_excerpt = document_text[:1500]

    enriched_chunks = []
    for i, chunk in enumerate(chunks):
        print(f"  Enriching chunk {i + 1}/{len(chunks)} (chunk_id={chunk['chunk_id']})...")
        enriched = enrich_chunk(chunk, document_excerpt, client, model=model)
        enriched_chunks.append(enriched)

    return enriched_chunks


if __name__ == "__main__":
    # Quick test (requires ANTHROPIC_API_KEY)
    from chunker import load_and_chunk_file
    import pathlib

    sample_path = pathlib.Path(__file__).parent / "sample_docs" / "acme_faq.txt"
    chunks = load_and_chunk_file(str(sample_path))

    with open(sample_path, "r") as f:
        doc_text = f.read()

    # Test with just the first 3 chunks to keep cost minimal
    test_chunks = chunks[:3]
    print(f"Enriching {len(test_chunks)} test chunks...")
    enriched = enrich_all_chunks(test_chunks, doc_text)

    for c in enriched:
        print(f"\n--- Chunk {c['chunk_id']} ---")
        print(f"Context: {c['context_sentence']}")
        print(f"Original: {c['original_text'][:100]}...")
