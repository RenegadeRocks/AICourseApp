---
type: week-overview
block: block-0-basecamp
week: week-01
title: "Week 1 — Basecamp: Prompting & RAGs + Vibe Coding"
sessions:
  - slug: basecamp-part-1-prompting-rags
    title: "Basecamp Part 1: Prompting & RAGs"
    date: 2026-05-02
  - slug: basecamp-part-2-vibe-coding
    title: "Basecamp Part 2: Vibe Coding"
    date: 2026-05-03
last_verified: 2026-04-15
---

# Week 1 — Basecamp: Prompting, RAGs, and Vibe Coding

Seven daily masterclasses across two tracks: three days on how prompting and retrieval work from first principles, three days on the "vibe coding" agentic paradigm and Claude Code, one day of synthesis.

## What you will be able to do by Sunday

1. Explain, in terms of attention mechanics and in-context learning, what every named prompting technique is doing to the next-token distribution — and predict where each one silently degrades.
2. Build a retrieval-augmented system from scratch: chunk, embed, hybrid-retrieve, rerank, ground, and evaluate. Articulate why each stage earns its keep using published benchmarks (Anthropic's Contextual Retrieval, 49% → 67% failure-rate reduction).[^1]
3. Operate Claude Code as an engineering surface: `CLAUDE.md` memory hierarchy, plan mode, subagents, hooks, MCP. Define the regime where "vibe coding" is a productivity multiplier vs. the regime where Karpathy himself calls it "not too bad for throwaway weekend projects."[^2]
4. Compose all three into a real system: prompt as program + retrieval as grounding + agent loop as execution.

## Daily map

| Day | Date | Lesson |
| --- | ---- | ------ |
| Mon | 2026-04-27 | [[01-mon-prompting-first-principles\|Prompting from first principles — mechanics, induction heads, CoT]] |
| Tue | 2026-04-28 | [[02-tue-advanced-prompting-patterns\|Advanced prompting — decomposition, self-consistency, tool use, evaluation]] (pending) |
| Wed | 2026-04-29 | [[03-wed-rag-end-to-end\|RAG end to end — chunking, hybrid retrieval, contextual retrieval, reranking]] (pending) |
| Thu | 2026-04-30 | [[04-thu-vibe-coding-origins-and-loops\|Vibe coding — origins, agent loops, why it works when it works]] (pending) |
| Fri | 2026-05-01 | [[05-fri-claude-code-deep-dive\|Claude Code deep dive — CLAUDE.md, plan mode, subagents, hooks, MCP]] (pending) |
| Sat | 2026-05-02 | [[06-sat-vibe-coding-in-anger\|Vibe coding in anger — real projects, hard limits, testing discipline]] (pending) |
| Sun | 2026-05-03 | [[07-sun-synthesis-and-review\|Synthesis — prompting + retrieval + agents as one system]] (pending) |

## Week deliverables

- A `prompts/` repo with ≥3 production-grade prompts (review, extract+cite, plan+execute) and a before/after evaluation table.
- A working local RAG demo in `code-lab/03/` that answers a question from a PDF of your choice, with grounded citations.
- A `CLAUDE.md`-driven toy project in `code-lab/05/` reproducible from voice or short text commands via Claude Code.
- A completed pass of the Sunday quiz and flashcards.

## Reading load (honest estimate)

- Core lessons: ~12 hours
- Code-lab time: ~4 hours
- Reference reading (linked inline): ~6 hours if you go deep, ~2 if you skim

## Key primary sources referenced this week

- Anthropic, *Prompt engineering overview* (Claude API docs).[^3]
- Anthropic, *Building effective agents* (Dec 2024).[^4]
- Anthropic, *Introducing Contextual Retrieval* (Sep 2024).[^1]
- Lewis et al. (2020), *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.*[^5]
- Olsson et al. (2022), *In-context Learning and Induction Heads.*[^6]
- Wei et al. (2022), *Chain-of-Thought Prompting.*[^7]
- Brown et al. (2020), *Language Models are Few-Shot Learners (GPT-3).*[^8]
- Andrej Karpathy (2025-02-02), *vibe coding* primary-source tweet.[^2]
- Andrej Karpathy (2025-02-05), *Deep Dive into LLMs like ChatGPT* (3h31m).[^9]

## Citations

[^1]: Anthropic (2024-09-19). *Introducing Contextual Retrieval.* https://www.anthropic.com/news/contextual-retrieval — "reduced the top-20-chunk retrieval failure rate by 49% (from 5.7% to 2.9%), and adding reranking further reduced the failure rate by 67% (to 1.9%)."
[^2]: Andrej Karpathy (2025-02-02). *"There's a new kind of coding I call 'vibe coding'"* [tweet]. https://x.com/karpathy/status/1886192184808149383 — "not too bad for throwaway weekend projects."
[^3]: Anthropic. *Prompt engineering overview.* Claude API Docs. https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
[^4]: Anthropic (2024-12-20). *Building effective agents.* https://www.anthropic.com/research/building-effective-agents — workflows (predefined orchestration) vs agents (dynamic self-direction); five workflow patterns.
[^5]: Lewis, P. et al. (2020). *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.* NeurIPS 2020. https://arxiv.org/abs/2005.11401
[^6]: Olsson, C., Elhage, N., Nanda, N., et al. (2022-09-24). *In-context Learning and Induction Heads.* https://transformer-circuits.pub/2022/in-context-learning-and-induction-heads/index.html
[^7]: Wei, J. et al. (2022). *Chain-of-Thought Prompting Elicits Reasoning in Large Language Models.* https://arxiv.org/abs/2201.11903
[^8]: Brown, T. et al. (2020). *Language Models are Few-Shot Learners.* https://arxiv.org/abs/2005.14165
[^9]: Andrej Karpathy (2025-02-05). *Deep Dive into LLMs like ChatGPT.* YouTube, 3h31m. https://x.com/karpathy/status/1887211193099825254
