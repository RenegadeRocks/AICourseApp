"""
chunker.py — Sentence-aware document chunking with configurable overlap.

Strategy: split on sentence boundaries (NLTK), then aggregate sentences into
chunks of approximately `max_tokens` words, with `overlap_sentences` sentences
of overlap between adjacent chunks.

This is better than fixed-character splitting because it never cuts a sentence
in the middle — which would produce incoherent embeddings.
"""

import nltk
from typing import Optional


def ensure_nltk_data() -> None:
    """Download NLTK punkt tokenizer if not already present."""
    try:
        nltk.data.find("tokenizers/punkt_tab")
    except LookupError:
        print("Downloading NLTK punkt_tab data (one-time)...")
        nltk.download("punkt_tab", quiet=True)


def chunk_text(
    text: str,
    max_words_per_chunk: int = 150,
    overlap_sentences: int = 2,
    document_title: Optional[str] = None,
) -> list[dict]:
    """
    Split text into overlapping chunks using sentence boundaries.

    Args:
        text: The full document text.
        max_words_per_chunk: Approximate maximum words per chunk (not tokens).
            150 words ≈ 200-250 tokens for English text.
        overlap_sentences: Number of sentences from the end of one chunk
            to prepend to the next chunk.
        document_title: Optional document title for metadata.

    Returns:
        List of dicts: {"chunk_id": int, "text": str, "word_count": int,
                        "document_title": str}
    """
    ensure_nltk_data()

    sentences = nltk.sent_tokenize(text)

    chunks = []
    current_sentences: list[str] = []
    current_word_count = 0
    chunk_id = 0

    for sentence in sentences:
        sentence_words = len(sentence.split())

        # If adding this sentence would exceed the limit AND we already have
        # content, finalise the current chunk.
        if current_word_count + sentence_words > max_words_per_chunk and current_sentences:
            chunk_text_str = " ".join(current_sentences)
            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "text": chunk_text_str,
                    "word_count": current_word_count,
                    "document_title": document_title or "Unknown",
                }
            )
            chunk_id += 1

            # Overlap: keep the last N sentences from the previous chunk
            overlap = current_sentences[-overlap_sentences:] if overlap_sentences > 0 else []
            current_sentences = overlap + [sentence]
            current_word_count = sum(len(s.split()) for s in current_sentences)
        else:
            current_sentences.append(sentence)
            current_word_count += sentence_words

    # Don't forget the last chunk
    if current_sentences:
        chunks.append(
            {
                "chunk_id": chunk_id,
                "text": " ".join(current_sentences),
                "word_count": current_word_count,
                "document_title": document_title or "Unknown",
            }
        )

    return chunks


def load_and_chunk_file(
    filepath: str,
    max_words_per_chunk: int = 150,
    overlap_sentences: int = 2,
) -> list[dict]:
    """Load a text file and chunk it."""
    with open(filepath, "r", encoding="utf-8") as f:
        text = f.read()

    # Use the filename stem as the document title
    import os
    title = os.path.splitext(os.path.basename(filepath))[0]

    return chunk_text(
        text,
        max_words_per_chunk=max_words_per_chunk,
        overlap_sentences=overlap_sentences,
        document_title=title,
    )


if __name__ == "__main__":
    # Quick test
    sample = """
    The quick brown fox jumps over the lazy dog. This is a second sentence about the fox.
    Here is a third sentence that talks about something else entirely. The dog was not amused.
    In the end, everyone went home happy. A new day began with fresh opportunities.
    """
    chunks = chunk_text(sample, max_words_per_chunk=20, overlap_sentences=1)
    for c in chunks:
        print(f"Chunk {c['chunk_id']} ({c['word_count']} words): {c['text'][:80]}...")
