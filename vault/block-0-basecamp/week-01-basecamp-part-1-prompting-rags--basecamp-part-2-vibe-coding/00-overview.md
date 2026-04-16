---
type: week-overview
block: block-0-basecamp
week: week-01
title: 'Week 1 — Prompting, RAG, Vibe Coding'
live_sessions:
  - '2026-05-02 — Basecamp Part 1: Prompting & RAGs'
  - '2026-05-03 — Basecamp Part 2: Vibe Coding'
study_window: 2026-04-27 to 2026-05-03
last_verified: 2026-04-15
---

# Week 1 — Prompting, RAG, and vibe coding, rebuilt from first principles

## The thesis of this week

Almost everything you will build this year — chat apps, agents, multi-tool workflows, research assistants, data pipelines with AI in the middle — is a combination of three primitives: **prompting, retrieval, and agentic loops with tool use**. The industry's folk wisdom about each of these is roughly 60% right and 40% wrong, and most builders plateau exactly at the 60% mark because they treat the three primitives as tricks instead of understanding them as mechanisms.

Week 1 is where we replace folk wisdom with a mechanical model of what's happening under the hood. Not because you will ever hand-code a transformer — you won't need to — but because when your agent fails at 2 a.m. and Claude Code can't tell you why, *you* need to know enough about the substrate to ask the right next question.

## Who this week is for

You have completed a generalist AI cohort. You ship things — utility apps, small automations, custom agents — by directing Claude Code or Codex, not by writing Python from scratch. You know what an API is, you've set up an MCP server or two, you can read JSON, and you've hit the point where "just write me a good prompt" stops being a sufficient instruction to your tools.

This week is about replacing *sufficient* with *precise*. Precise instructions compound over the next twenty-five weeks of the program.

## Shape of the week

Two paired deep-dives plus a synthesis day. Each day is ~90–120 minutes of reading plus ~30–60 minutes of hands-on work.

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | Prompting from first principles — what the model is actually doing when you prompt it | Deep-dive + experiment + problem set |
| Tue | Prompt engineering in practice — composition, evals, versioning | Deep-dive + build |
| Wed | RAG as a system — retrieval, rerank, context assembly, eval | Deep-dive + experiment |
| Thu | RAG failure modes and the 2025 long-context vs retrieval debate | Deep-dive + problem set |
| Fri | Vibe coding 1 — what Karpathy actually said, what Claude Code actually does | Deep-dive on agent mechanics |
| Sat | Vibe coding 2 — the discipline: eval-driven dev, trace inspection, guardrails | Deep-dive + build |
| Sun | Synthesis, quiz, flashcards | Review |

## Why these three topics belong together

Prompting, RAG, and agentic coding are usually taught as three disconnected tricks. They are not. They are three answers to one question: *"How do I make a frozen text-completion engine do useful work on problems it has never explicitly seen?"*

- **Prompting** answers it through *in-context conditioning*: put the task spec, examples, and structural scaffolding directly in the context window. Works when the task is specifiable and the needed knowledge already lives in the model's weights.
- **RAG** answers it through *in-context injection of retrieved knowledge*: fetch relevant external documents at query time and paste them into the prompt. Works when the needed knowledge is too large, too fresh, or too private to have been trained into the model.
- **Vibe coding / agents** answers it through *in-context iteration with tools*: let the model write, run, observe, and repair across many turns. Works when the task requires multi-step search, verification against a ground truth (tests, compilers, APIs), or exploration of a large action space.

All three run on the same substrate — next-token prediction conditioned on the context window. Understanding that substrate is the bedrock of this week. The wrappers differ by topic; the mechanism doesn't.

## What "L3 depth" means in this vault

Every deep-dive this week engages five things:

1. **At least one live controversy in the field.** The chain-of-thought faithfulness debate (Lanham 2023 and Turpin 2023 vs. the reasoning-model crowd)[^1][^2]; the long-context-vs-RAG argument (does a 1M-token window kill retrieval, or not?); the "is vibe coding responsible engineering?" tension between Karpathy's hedge and how the phrase is used in practice.
2. **At least three citations to research published after January 2024.** Frontier, not history.
3. **Runnable experiments that demonstrate a mechanism.** Some you run in Claude.ai with pen and paper. Some you direct Claude Code to execute and report on. All produce numbers you can see.
4. **Operator-level specifics with numbers.** Anthropic's Contextual Retrieval reducing top-20 retrieval failure from 5.7% to 2.9% (a 49% relative reduction)[^3]; Hamel Husain's eval-driven development discipline — binary LLM-as-judge, human-agreement calibration, systematic error analysis[^4]; Opus 4.5 hitting 80.9% on SWE-bench Verified while Sonnet 4.5 hits 77.2% at a 200K thinking budget[^5].
5. **A reviewer lens with named technical disagreements.** Each lesson names specific paragraphs that a Karpathy, a Chip Huyen, a Jason Liu, or a Boris Cherny would push back on, and what they'd specifically argue instead.

## How to study this week

Each day, in priority order if you're short on time:

1. **Run the experiment.** That's where the capability actually builds.
2. **Read the "Must-read" citations.** Usually three to five sources.
3. **Do the problem set.** Some are hands-on, some are "read a paper and take a position."
4. **Read the lesson prose.** It's scaffolding for the first three. If you only read the prose, you've skimmed the week, not learned it.

The mix of exercise modes is deliberate. Some problems want you in Claude.ai with pen and paper so you *feel* variance. Some want you to direct Claude Code to run something at scale. Some want you to read a paper and write down where you agree and disagree. The variety is not aesthetic; different kinds of understanding require different kinds of work.

## The Saturday and Sunday live sessions

The cohort has live sessions on 2026-05-02 and 2026-05-03. They are bonuses. The lessons in this vault are the primary instruction — each one is a standalone masterclass. If you miss the live session, nothing in the vault is incomplete.

## Citations

[^1]: Lanham, T., Chen, A., et al. (2023-07-17). *Measuring Faithfulness in Chain-of-Thought Reasoning.* Anthropic. https://arxiv.org/abs/2307.13702 — models show large across-task variance in how much they condition on their own CoT; faithfulness often *decreases* with scale.
[^2]: Turpin, M., Michael, J., Perez, E., Bowman, S. (2023, NeurIPS). *Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting.* https://arxiv.org/abs/2305.04388 — biasing features in prompts drop accuracy by up to 36% on BIG-Bench Hard while the model's reasoning trace never mentions the bias.
[^3]: Anthropic (2024-09-19). *Introducing Contextual Retrieval.* https://www.anthropic.com/news/contextual-retrieval — Contextual Embeddings + Contextual BM25 reduce top-20-chunk retrieval failure from 5.7% to 2.9% (49% relative reduction); with a reranker, 67%.
[^4]: Hamel Husain (2024). *Your AI Product Needs Evals.* https://hamel.dev/blog/posts/evals/ — eval-driven development framework: binary LLM-as-judge, human-agreement calibration, error analysis as systematic process.
[^5]: Anthropic (2025-09-29 / 2025-11-24). *Introducing Claude Sonnet 4.5 / Claude Opus 4.5.* https://www.anthropic.com/news/claude-sonnet-4-5, https://www.anthropic.com/news/claude-opus-4-5 — Sonnet 4.5: 77.2% SWE-bench Verified at 200K thinking budget (10-trial avg), 82.0% with parallel test-time compute. Opus 4.5: 80.9%, first model over 80%.
