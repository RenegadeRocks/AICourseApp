"""
generator.py — Answer generation using retrieved context and Claude.

The generation step is where RAG connects to the LLM:
  1. Assemble the retrieved chunks into a context block
  2. Build a prompt with the context + user question
  3. Call Claude to generate a grounded answer

Key design choices:
  - "Answer only from the context" instruction prevents hallucination from
    parametric memory when the context is sufficient.
  - Explicit "I don't know" path when context is insufficient — prevents
    confident hallucination on out-of-scope questions.
  - Citations are requested so the answer is auditable.
"""

import os
import anthropic
from retriever import RetrievedChunk


GENERATION_SYSTEM_PROMPT = """\
You are a helpful customer support assistant for ACME SaaS Platform.

<instructions>
Answer the user's question based ONLY on the information in the provided context.
- If the answer is clearly in the context, answer directly and cite the relevant part.
- If the context does not contain enough information to answer the question, say:
  "I don't have enough information in the knowledge base to answer that. Please contact support@acme.com."
- Do not make up information or draw on knowledge outside the provided context.
- Keep answers concise: 2-4 sentences unless a longer answer is genuinely required.
- Quote or paraphrase specific numbers, dates, and policy terms from the context.
</instructions>
"""

GENERATION_HUMAN_TEMPLATE = """\
<context>
{context_block}
</context>

<question>
{question}
</question>

Answer the question using only the information in the context above.
"""


def format_context(retrieved_chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks into a context block for the prompt."""
    context_parts = []
    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"[Source {i} — {chunk.document_title}, relevance score: {chunk.score:.3f}]\n"
            f"{chunk.text}"
        )
    return "\n\n---\n\n".join(context_parts)


def generate_answer(
    question: str,
    retrieved_chunks: list[RetrievedChunk],
    model: str = "claude-haiku-4-5-20251001",
    max_tokens: int = 512,
) -> dict:
    """
    Generate an answer from retrieved chunks.

    Args:
        question: The user's question.
        retrieved_chunks: List of RetrievedChunk from the retriever.
        model: Claude model to use for generation.
        max_tokens: Maximum output tokens.

    Returns:
        Dict with "answer" (str), "model" (str), "chunks_used" (int),
        and "input_tokens" (int, from the API response usage).
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    context_block = format_context(retrieved_chunks)
    human_message = GENERATION_HUMAN_TEMPLATE.format(
        context_block=context_block,
        question=question,
    )

    response = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=GENERATION_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": human_message}],
    )

    answer = response.content[0].text.strip()

    return {
        "answer": answer,
        "model": model,
        "chunks_used": len(retrieved_chunks),
        "input_tokens": response.usage.input_tokens,
        "output_tokens": response.usage.output_tokens,
    }


if __name__ == "__main__":
    # Standalone test (requires ANTHROPIC_API_KEY)
    mock_chunks = [
        RetrievedChunk(
            chunk_id=0,
            text="For annual plans, we offer a prorated refund for the remaining months if you cancel within the first 30 days of the annual billing period. After 30 days on an annual plan, no refunds are issued, but you retain access until the end of the paid period.",
            document_title="ACME FAQ",
            score=0.92,
        )
    ]

    result = generate_answer(
        question="Can I get a refund if I cancel my annual plan after 2 weeks?",
        retrieved_chunks=mock_chunks,
    )
    print(f"Answer: {result['answer']}")
    print(f"Tokens used: {result['input_tokens']} in / {result['output_tokens']} out")
