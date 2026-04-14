---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 1
day_name: mon
session_slug: basecamp-part-1-prompting-rags
date_due: 2026-04-27
tags: [prompting, rag, orientation, pre-read]
sources: [anthropic-prompt-engineering-overview, lewis-rag-2020, anthropic-contextual-retrieval]
last_verified: 2026-04-14
---

# Monday Pre-read: What Prompting and RAG Actually Solve

## Why this matters (operator framing)

Every AI product you build this program comes down to one question asked thousands of times a day: *how do you get a model to do the right thing, with the right information, reliably?* Prompting is the answer to the first half; RAG is the answer to the second. Neither is magic and neither requires a PhD. They are engineering disciplines with known best practices, measurable outcomes, and clear failure modes. By the end of this week you will be able to build a working RAG pipeline from scratch and write system prompts that hold up under adversarial input — skills that justify consulting fees on their own.

## Prerequisites

- Basic familiarity with what an LLM is (it predicts the next token)
- [[00-program/index]] — read the master reading list section on LLM Engineering and RAG
- [[00-program/how-to-study]] — understand the 7-day cycle before you start

## Core content

### The mental model: three problems, two tools

When an LLM gives a wrong answer, the cause is almost always one of three things:

1. **It didn't understand what you wanted** — instruction ambiguity, missing context, wrong format. *Fixed by better prompting.*
2. **It didn't have the right facts** — knowledge cutoff, private data, domain specifics not in training. *Fixed by RAG.*
3. **The model itself lacks capability** — needs to actually reason, count, or plan across many steps. *Fixed by CoT prompting, tool use, or a better model.*

Most practitioners confuse these. They try to fix problem 2 with fine-tuning (expensive), or problem 1 with RAG (irrelevant retrieval), or problem 3 with more elaborate prompts (ceiling hit). Getting the diagnosis right before picking the tool is the core skill.

### What prompting actually is

A prompt is not a magic spell. It is a specification: you are telling the model what role to play, what task to do, what constraints to respect, and what format the output should be in. Anthropic's prompt engineering documentation breaks this into four primitives[^1]:

- **System prompt** — persistent instructions the model always follows. This is where role, tone, tool descriptions, and hard rules live.
- **Human turn** — the user's actual request, which may include examples, data, and task-specific context.
- **Assistant prefill** — (Claude-specific) you can pre-fill the start of the assistant's response to steer format.
- **Tool results** — structured data returned to the model after a tool call, which it incorporates into its next response.

The most common beginner mistake is treating the system prompt as optional decoration. It is not — it is the contract between you and the model. Production systems spend more engineering effort on the system prompt than on any other part of the stack.

### What RAG actually is

RAG stands for Retrieval-Augmented Generation. The paper that named it — Lewis et al. 2020 — proposed combining a dense retrieval system with a generative model so the model's outputs are grounded in retrieved evidence rather than solely in parametric memory[^2].

In practice, a RAG pipeline has five steps:

1. **Index** — chunk your documents, embed each chunk, store in a vector database.
2. **Query** — embed the user's question.
3. **Retrieve** — find the k most semantically similar chunks.
4. **Augment** — stuff those chunks into the prompt as context.
5. **Generate** — the model answers based on the context.

This solves the knowledge problem cleanly: you can update the vector database without retraining the model, query private data without exposing it, and attribute answers to specific source documents.

The failure mode people don't talk about enough: garbage in, garbage out. If your chunking is bad, your retrieval is bad, and no amount of prompt engineering rescues it. Anthropic's September 2024 research on contextual retrieval showed that naive chunking loses ~35% of relevant chunks that could have been found with enriched context[^3].

### Three questions to bring to Saturday's session

Write your answers to these before the live session. They will anchor your learning:

1. Think of a real knowledge-intensive task you do today (answering customer questions, researching a topic, reviewing contracts). Which of the three failure modes above most often causes the AI to give a wrong answer?

2. If you had to explain RAG to a non-technical client in one sentence, what would you say? (Try it. It's harder than it looks.)

3. Karpathy's "Let's build GPT" video shows that a language model is fundamentally a next-token predictor trained on a loss function[^4]. How does that framing change how you think about why prompts work? (Hint: the model is optimizing for what a human *would say* next, not for "the truth".)

## Worked example

No code today — this is orientation. But do this:

Open Claude.ai (or your API playground). Write a system prompt that makes the model act as a legal contract reviewer. Give it a simple contract paragraph and ask it to identify three risks. Notice:
- How specific do you need to be before it gives useful output?
- What happens if you remove the system prompt entirely?
- What happens if you add "Think step by step" to your request?

This 10-minute experiment will surface the questions you want answered on Tuesday.

## Common mistakes experts see

- **Treating prompting as alchemy**: writing longer prompts hoping something sticks, with no hypothesis about what is actually failing.
- **Skipping evaluation**: writing a prompt that works on one example and shipping it. One example is not a benchmark.
- **Over-engineering before diagnosing**: building a complex multi-retrieval agentic RAG pipeline when the real issue is a vague user question.
- **Confusing fine-tuning with RAG**: fine-tuning teaches the model new *behaviors* and *styles*, not new *facts*. RAG is for facts. Both have their place but neither substitutes for the other.
- **Ignoring the retrieval quality**: spending 80% of time on the generation prompt and 20% on the retrieval that feeds it — then being surprised when answers are hallucinated.

## Reflection questions

1. In your own words: what is the difference between what a system prompt does and what a RAG context injection does?
2. Lewis et al. called their approach "open-domain question answering" in 2020. How has the scope of what RAG is used for evolved since then?
3. Why might a model give a confidently wrong answer even when the correct information is in the retrieved context?
4. What does "grounding" mean, and why is it the primary business value of RAG in enterprise settings?
5. A colleague says "we can just fine-tune the model on our company docs." When is this advice correct and when is it wrong?

## My take (reviewer lens)

Karpathy would insist you actually understand what a token is before you start writing prompts — because the whole point of techniques like XML tagging and structured prompting is to exploit how the model tokenizes and attends to input. If you think of a prompt as prose addressed to a person, you'll write worse prompts than if you understand you're specifying a probability distribution over the next token. Read or skim his tokenizer video before Tuesday.

Seibel would say: stop theorizing and start building. The fastest way to understand prompting is to break something — write an intentionally bad prompt, see what breaks, fix it. The fastest way to understand RAG is to build one from scratch (Wednesday's code-lab). Don't let the reading substitute for the doing.

## Further reading

**Must-read before Saturday**
- Anthropic prompt engineering overview — <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview> (15 min)
- Anthropic "Introducing Contextual Retrieval" — <https://www.anthropic.com/news/contextual-retrieval> (20 min, Sep 2024)

**Recommended**
- Lewis et al. "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks" — <https://arxiv.org/abs/2005.11401> (skim abstract + Section 2)
- Simon Willison "What I learned from six months of daily LLM use" — <https://simonwillison.net> (search his blog for this post, 2024)

**Optional**
- Karpathy "Let's build GPT" — <https://www.youtube.com/watch?v=kCc8FmEb1nY> (watch first 20 min for the next-token-prediction framing)

## Citations

[^1]: Anthropic, "Prompt engineering overview," *Anthropic Documentation*, <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>, accessed 2026-04-14.

[^2]: Patrick Lewis, Ethan Perez, et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks," *arXiv:2005.11401*, May 2020, <https://arxiv.org/abs/2005.11401>. See Section 2 (RAG model formulation).

[^3]: Anthropic, "Introducing Contextual Retrieval," *Anthropic News*, September 19, 2024, <https://www.anthropic.com/news/contextual-retrieval>. Key finding: naive chunking caused ~35% retrieval failure rate that contextual enrichment reduced significantly.

[^4]: Andrej Karpathy, "Let's build GPT: from scratch, in code, spelled out," *YouTube*, Jan 2023, <https://www.youtube.com/watch?v=kCc8FmEb1nY>, @ 0:00–12:00 (next-token prediction as the foundational objective).

_last_verified: 2026-04-14_
