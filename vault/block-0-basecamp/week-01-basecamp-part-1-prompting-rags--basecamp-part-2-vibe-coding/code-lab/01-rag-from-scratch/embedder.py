"""
embedder.py — Sentence-transformer embedding wrapper.

Uses `all-MiniLM-L6-v2` by default — a fast, general-purpose English model
that produces 384-dimensional vectors. First run downloads ~80MB model.

Why this model:
- Widely benchmarked, well-maintained by sentence-transformers team
- Fast enough for local use (CPU, no GPU required)
- Good baseline for English text; switch to BAAI/bge-small-en-v1.5 for
  domain-specific tasks with slightly better quality

Reference:
  Reimers & Gurevych, "Sentence-BERT: Sentence Embeddings using Siamese
  BERT-Networks," EMNLP 2019, https://arxiv.org/abs/1908.10084
"""

from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Load the embedding model.

        Args:
            model_name: HuggingFace model name. Options:
                - "all-MiniLM-L6-v2" (fast, 384d, good general English)
                - "BAAI/bge-small-en-v1.5" (slightly better, same speed)
                - "all-mpnet-base-v2" (best quality, 768d, slower)
        """
        print(f"Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.embedding_dim = self.model.get_sentence_embedding_dimension()
        print(f"Model loaded. Embedding dimension: {self.embedding_dim}")

    def embed(self, texts: list[str], batch_size: int = 32, show_progress: bool = False) -> np.ndarray:
        """
        Embed a list of texts.

        Args:
            texts: List of strings to embed.
            batch_size: Number of texts to process per batch.
            show_progress: Show a progress bar (useful for large corpora).

        Returns:
            numpy array of shape (len(texts), embedding_dim), float32.
        """
        embeddings = self.model.encode(
            texts,
            batch_size=batch_size,
            show_progress_bar=show_progress,
            convert_to_numpy=True,
            normalize_embeddings=True,  # L2 normalize → cosine sim = dot product
        )
        return embeddings

    def embed_single(self, text: str) -> np.ndarray:
        """Embed a single text string. Returns shape (embedding_dim,)."""
        return self.embed([text])[0]


if __name__ == "__main__":
    embedder = Embedder()
    test_texts = [
        "What is the refund policy for annual plans?",
        "Annual plans have a 30-day refund window.",
        "The cat sat on the mat.",
    ]
    vecs = embedder.embed(test_texts)
    print(f"Embedded {len(test_texts)} texts → shape {vecs.shape}")

    # Cosine similarity (since embeddings are L2-normalized, dot product = cosine sim)
    q = vecs[0]
    sims = vecs @ q
    print(f"Similarity of query to doc 1: {sims[1]:.4f}")
    print(f"Similarity of query to doc 2 (irrelevant): {sims[2]:.4f}")
    # Expected: doc 1 much more similar than doc 2
