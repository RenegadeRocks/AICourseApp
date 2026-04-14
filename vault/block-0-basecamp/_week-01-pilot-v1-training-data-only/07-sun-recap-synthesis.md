---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 7
day_name: sun
session_slug: basecamp-part-2-vibe-coding
date_due: 2026-05-04
tags: [recap, synthesis, review, week-close, prompting, rag, vibe-coding]
sources: [anthropic-contextual-retrieval, karpathy-vibe-coding-tweet, anthropic-prompt-engineering, lewis-rag-2020]
last_verified: 2026-04-14
---

# Sunday Recap: Synthesizing the Week

> Sunday's job is not to learn new things. It's to compress what you've learned into a durable mental model, identify the gaps, and prepare next week's study. Budget 45 minutes.

## Why this matters (operator framing)

Compression is the learning. You read five lessons this week, ran code, sat through two live sessions. Without a synthesis pass, you walk into next week with five loosely connected islands of knowledge. With it, you walk in with a single coherent framework. The practitioners who compound fastest are the ones who do the Sunday recap — it takes 45 minutes and doubles retention.

## Prerequisites

- All five daily lessons completed, or at minimum the deep-dives (Tue, Wed, Fri)
- [[06-sat-vibe-coding-live-companion]] notes from the live session
- Code-lab run and notes jotted (even if it didn't fully work)

## Core content: the week in review

### The unified framework

This week gave you two sides of one coin:

**Side 1: Getting the right answer out of a model (prompting + RAG)**

The model doesn't "know" things in the way a human expert does — it predicts the most plausible next token. To get reliable, accurate outputs:
- You need precise instructions (system prompts, XML structure, few-shot examples)
- You need the right facts in context (RAG: retrieval → augmentation → generation)
- You need structured, testable outputs (JSON mode, tool use, evals)

**Side 2: Turning model output into shipped software (vibe coding)**

The model generates code you can run. To do this efficiently:
- You need a spec before you prompt (the single highest-leverage habit)
- You need to choose the right tool for the abstraction level (component, app, agent)
- You need version control and at least some review for anything user-facing

These aren't separate disciplines. A RAG pipeline built with vibe coding is where both skills meet: you spec the architecture (prompting discipline), build the retrieval system (RAG depth), and ship the demo (vibe coding speed).

### What the experts would say you missed

**Karpathy's likely critique**: You probably didn't look hard enough at the token-level behavior of your prompts. The difference between a prompt that works 70% of the time and one that works 95% of the time is often one or two carefully chosen tokens. Karpathy would want you to run the tokenizer on your prompts — literally count the tokens — before declaring them optimized.

**Seibel's likely critique**: Did you ship something? Not run a code-lab — *ship* something. A demo URL. A script someone else can run. If the answer is no, that's the gap. The week should have ended with something in front of a real user, even a friend, not just working on your local machine.

**Jason Liu's likely critique**: You don't have an eval harness. You built the RAG pipeline, it "seems to work," but you have no retrieval recall metric, no faithfulness score, no test set. Without that, you're flying blind. Build the eval before you build the next feature.

**Simon Willison's likely critique**: Did you run a security scanner on any code you shipped? Generated code is often insecure by default — unvalidated inputs, missing rate limits, SQL injection risks. One `bandit` run on a Python project takes 10 seconds.

### Concept map

```
WEEK 1 CONCEPTS
│
├── PROMPTING
│   ├── System prompts (the contract)
│   ├── XML tags (instruction/data separation)
│   ├── Chain-of-thought (reasoning before output)
│   ├── Few-shot examples (show, don't tell)
│   ├── Structured outputs / JSON mode
│   ├── Tool use (model → action → result loop)
│   └── Prompt injection (the attack you must understand)
│
├── RAG
│   ├── Chunk → Embed → Index → Retrieve → Augment → Generate
│   ├── Contextual enrichment (Anthropic Sep 2024)
│   ├── Hybrid search (dense + BM25)
│   ├── Reranking (cross-encoder second pass)
│   └── Evals (retrieval recall, faithfulness, groundedness)
│
└── VIBE CODING
    ├── Three modes (copilot / agentic / zero-review)
    ├── Tool landscape (Cursor, Claude Code, Bolt, Lovable, v0, Replit)
    ├── Spec-driven vs. prompt-driven
    ├── .cursorrules / .claude/ configs
    └── Security: always scan generated code before shipping
```

### The five most important things you should be able to do now

1. **Write a production-grade system prompt** — role, instructions, XML structure, few-shot examples, output format, anti-injection posture. From scratch, in 10 minutes.

2. **Build a working RAG pipeline** — chunk a document, embed with sentence-transformers, query with FAISS, augment a prompt, generate with Claude API. From scratch, in 60 minutes. (The code-lab is the evidence.)

3. **Apply contextual retrieval** — generate chunk context with a small LLM before indexing. Explain why it reduces retrieval failures by ~49%.

4. **Choose the right vibe coding tool** — given a scenario, pick Cursor vs. Claude Code vs. Bolt vs. Lovable vs. v0 vs. Replit and justify it.

5. **Write a one-page spec** — before opening any AI coding tool. This is the meta-skill that makes everything else faster.

## Weekly quiz (take cold before reviewing answers in 05-quiz.md)

Take this without opening any lesson files. That's the only signal that generalizes.

1. What is the primary advantage of contextual retrieval over naive chunking?
2. Why is XML tagging useful in Claude prompts?
3. What is BM25, and what does it complement in hybrid RAG search?
4. Name three failure modes of naive RAG that contextual retrieval addresses.
5. What does "prompt injection" mean, and what is one mitigation?
6. When should you use Claude Code instead of Bolt for a vibe coding task?
7. What is the "prefill trick" in Claude API and what does it guarantee?
8. Why is "retrieval recall" measured separately from "answer accuracy" in RAG evals?

_Don't look up the answers yet. Write them out. Then check against [[05-quiz]]._

## Flashcard session

Run through [[06-flashcards]] now. Target: 80% correct without looking. If you score below 80%, schedule a [[02-tue-prompting-deep-dive]] or [[03-wed-rag-deep-dive]] revisit for Monday.

## What surprised me this week

_(fill in after the live sessions)_

- From the prompting session:

- From the RAG session:

- From the vibe coding session:

- From running the code-lab:

## What I'd tell the me from last Monday

_(write 3 sentences as if to a past self. This is the highest-compression output of the week.)_

## Next week preview

Week 2 covers **Basecamp Part 3: MCPs & Voice Agents** (Sat 2026-05-09) and **Basecamp Part 4: Revisiting n8n & AI Agent Fundamentals** (Sun 2026-05-10).

The connection to this week: MCPs (Model Context Protocol) are the standardized tool-use layer — everything you learned about tool use and function calling in Tuesday's lesson is the foundation for MCP. Voice agents add a new modality but the same prompting discipline applies.

Pre-read for Monday: [[../week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/ (pending)]]

## Reflection questions

1. What single concept from this week do you feel least confident about? (Be honest — that's the one to revisit.)
2. The RAG + prompting combination is the foundation for every AI product you'll build this program. If you had to explain the relationship between the two to a client in 60 seconds, what would you say?
3. Karpathy and Seibel would disagree about how much time to spend understanding generated code. Where do *you* stand, and why?
4. What would you build if you had 4 hours this weekend with what you now know?
5. Write your "what I'd tell the me from last Monday" paragraph. Then read it. Is it specific enough to be useful next time you're confused?

## My take (reviewer lens)

The integration point the lessons don't fully surface: a well-built RAG pipeline *is* a prompting system. The retrieval step is just a dynamic few-shot injection — you're adding the right examples (retrieved chunks) to the right prompt at query time. Understanding this unification makes you faster at debugging both. When RAG answers are wrong, ask: "Is this a retrieval failure (wrong chunks) or a generation failure (right chunks, wrong answer)?" That question is answered by the same eval discipline that applies to any prompting system.

Karpathy would end the week by asking: did you actually *understand* what the model is doing when it processes your RAG context? It's predicting the next token, attending across a very long sequence. The reason chunk order matters (most important context first) is because attention degrades over long sequences — the "lost in the middle" phenomenon. If you don't know about "lost in the middle," add it to next week's reading list.

## Further reading

**Week-end essentials**
- Nelson Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," *arXiv:2307.03172*, Jul 2023 — <https://arxiv.org/abs/2307.03172>. Explains why context placement matters in long prompts.
- Anthropic, "Building effective agents," Dec 2024 — <https://www.anthropic.com/research/building-effective-agents>. Preview for next week's agent content.

**Optional extension**
- Chip Huyen, *AI Engineering* (O'Reilly, 2024) — Chapter on RAG evaluation metrics. The most systematic treatment in book form.

## Citations

[^1]: Anthropic, "Introducing Contextual Retrieval," *Anthropic News*, Sep 19, 2024, <https://www.anthropic.com/news/contextual-retrieval>.

[^2]: Andrej Karpathy, vibe coding tweet, *X*, Feb 2025, <https://x.com/karpathy/status/1886192184808149383>.

[^3]: Anthropic, "Prompt engineering overview," *Anthropic Documentation*, <https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview>, accessed 2026-04-14.

[^4]: Nelson Liu et al., "Lost in the Middle: How Language Models Use Long Contexts," *arXiv:2307.03172*, Jul 2023, <https://arxiv.org/abs/2307.03172>. Key finding: model performance degrades on information placed in the middle of long contexts.

[^5]: Chip Huyen, *AI Engineering*, O'Reilly Media, 2024. Chapter on RAG evaluation: precision, recall, and faithfulness metrics for production systems.

_last_verified: 2026-04-14_
