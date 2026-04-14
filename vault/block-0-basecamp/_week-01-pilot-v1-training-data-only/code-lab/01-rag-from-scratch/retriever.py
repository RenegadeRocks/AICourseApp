"""
retriever.py — FAISS-based vector index for chunk retrieval.

FAISS (Facebook AI Similarity Search) provides fast approximate nearest-neighbor
search. For small corpora (<10k chunks), we use IndexFlatIP (exact inner product
search on L2-normalized vectors = cosine similarity, no approximation).

For larger corpora, swap IndexFlatIP for IndexIVFFlat or IndexHNSW.

Reference:
  Johnson, Douze, Jégou, "Billion-scale similarity search with GPUs,"
  arXiv:1702.08734, https://arxiv.org/abs/1702.08734
"""

import faiss
import numpy as np
from dataclasses import dataclass


@dataclass
class RetrievedChunk:
    chunk_id: int
    text: str
    document_title: str
    score: float  # cosine similarity (higher = more relevant)


class VectorIndex:
    def __init__(self, embedding_dim: int):
        """
        Create an empty FAISS index.

        Args:
            embedding_dim: Dimensionality of the embeddings (must match embedder).
        """
        # IndexFlatIP = flat (exact) index, inner product (= cosine sim for
        # L2-normalized vectors). No training required.
        self.index = faiss.IndexFlatIP(embedding_dim)
        self.chunks: list[dict] = []  # parallel list to the FAISS index

    def add_chunks(self, chunks: list[dict], embeddings: np.ndarray) -> None:
        """
        Add chunks and their embeddings to the index.

        Args:
            chunks: List of chunk dicts (must have "text", "chunk_id", "document_title").
            embeddings: numpy array of shape (len(chunks), embedding_dim), float32, L2-normalized.
        """
        assert len(chunks) == embeddings.shape[0], (
            f"Mismatch: {len(chunks)} chunks but {embeddings.shape[0]} embeddings"
        )
        embeddings_f32 = embeddings.astype(np.float32)
        self.index.add(embeddings_f32)
        self.chunks.extend(chunks)
        print(f"Indexed {len(chunks)} chunks. Total in index: {self.index.ntotal}")

    def search(self, query_embedding: np.ndarray, k: int = 3) -> list[RetrievedChunk]:
        """
        Retrieve the top-k most similar chunks.

        Args:
            query_embedding: 1D numpy array of shape (embedding_dim,), L2-normalized.
            k: Number of results to return.

        Returns:
            List of RetrievedChunk objects, sorted by score descending.
        """
        k = min(k, self.index.ntotal)  # can't retrieve more than we have
        query_f32 = query_embedding.astype(np.float32).reshape(1, -1)
        scores, indices = self.index.search(query_f32, k)

        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue
            chunk = self.chunks[idx]
            results.append(
                RetrievedChunk(
                    chunk_id=chunk["chunk_id"],
                    text=chunk["text"],
                    document_title=chunk.get("document_title", "Unknown"),
                    score=float(score),
                )
            )
        return results

    def __len__(self) -> int:
        return self.index.ntotal


if __name__ == "__main__":
    # Minimal integration test
    from embedder import Embedder

    embedder = Embedder()
    texts = [
        "Refunds for annual plans are available within 30 days.",
        "We accept Visa, Mastercard, and PayPal.",
        "The cat sat on the mat.",
        "SSO is available on Enterprise plans via SAML 2.0.",
    ]
    chunks = [{"chunk_id": i, "text": t, "document_title": "Test"} for i, t in enumerate(texts)]
    embeddings = embedder.embed(texts)

    index = VectorIndex(embedding_dim=embedder.embedding_dim)
    index.add_chunks(chunks, embeddings)

    query = "What is the refund window for annual billing?"
    q_emb = embedder.embed_single(query)
    results = index.search(q_emb, k=2)

    print(f"\nQuery: {query}")
    for r in results:
        print(f"  [{r.score:.4f}] {r.text}")
