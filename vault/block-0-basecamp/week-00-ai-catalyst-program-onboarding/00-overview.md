---
type: week-overview
block: block-0-basecamp
week: week-00
title: 'Week 0 — Basecamp: the AI-native builder''s substrate'
live_sessions:
  - 'Program Onboarding — AI Pro-level Course'
study_window: 2026-04-20 to 2026-04-26
last_verified: 2026-07-17
---

# Week 0 — Basecamp: the substrate every later week assumes

## The thesis of this week

The rest of the program — prompting, RAG, MCPs, voice agents, business problem decoding, fine-tuning, production ops — is built on a handful of assumptions about *what a language model is*, *how your tooling actually talks to it*, *what model-card numbers really mean*, *what a 1M-token context window does and does not buy you*, and *what git gives you when an agent writes code for you*. If any of those assumptions is shaky, the later weeks will land as tricks instead of as mechanisms.

Week 0 installs that substrate: six standalone L3 masterclasses, one per day Monday through Saturday, plus a Sunday synthesis. This is not orientation. Each lesson stands on its own and teaches the topic in full.

## Who this week is for

You finished a generalist AI cohort or fellowship. You ship utility apps, small automations, custom agents — by directing Claude Code, Codex, Cursor, or similar. You can read a model card without glazing over, but you haven't yet developed the reflex to ask *"what eval harness produced this number?"*. You can set up an MCP server but couldn't sketch why 1M-context Claude behaves differently from Gemini 3.1 Pro on long documents. You have enough surface-level fluency to be dangerous; this week converts that fluency into structural understanding.

## Shape of the week

Six paired deep-dives plus a synthesis day. Each day is ~90–120 minutes of reading plus ~30–60 minutes of hands-on work via Claude Code or Claude.ai.

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | Mental model of LLMs — what the model actually is, and how that shapes every downstream decision | Deep-dive + sampling experiment |
| Tue | The AI-native builder stack — Claude Code, Codex, Cursor, Aider, Cline, Replit Agent, Devin Desktop (ex-Windsurf) compared on the axes that matter | Deep-dive + head-to-head experiment |
| Wed | CLAUDE.md and the memory architecture — 4-tier hierarchy, auto-memory, skills, subagents as memory | Deep-dive + merge-order experiment |
| Thu | Reading model specs critically — what Anthropic / OpenAI / Google / xAI cards actually tell you, what they hide | Deep-dive + calibration experiment |
| Fri | Context window economics — 1M windows, lost-in-the-middle, prompt caching, real $ math | Deep-dive + cost experiment |
| Sat | Git worktrees and diff review — the AI builder's safety net when agents write your code | Deep-dive + recovery experiment |
| Sun | Synthesis, quiz, flashcards | Review |

## Why these six topics belong together

Each of the later twenty-five weeks lands an advanced technique (RAG, agents, fine-tuning, evals, production ops, monetization). Each one *assumes* the reader has internalized the six topics above. Week 0 front-loads those assumptions so the rest of the program can stop re-explaining them.

Mapped to what's coming:

- **Mental model of LLMs (Mon)** → underwrites Week 1's prompting-from-first-principles, Week 4's fine-tuning discussion, Week 13's reasoning-models deep-dive.
- **AI-native builder stack (Tue)** → underwrites every week you will ship something in Claude Code; the tool differences matter when you pick a stack for a client project in Weeks 19–22.
- **CLAUDE.md / memory (Wed)** → underwrites every session you run after today. Skills, subagents, hooks — all of Week 2's MCP content assumes you know where state lives.
- **Reading model specs (Thu)** → underwrites every model-choice decision in the program. You will be asked to pick a model for a pipeline a dozen times; picking by vibes instead of by benchmark-with-caveats is how AI projects die.
- **Context window economics (Fri)** → underwrites Week 1's RAG content (is retrieval obsolete or not?), Week 9's long-context agents, Week 14's cost optimization.
- **Git worktrees (Sat)** → underwrites every later week where an agent writes code you ship. Without a recovery protocol you are not running AI-directed development; you are doing AI-directed gambling.

## What "L3 depth" means in this vault

Every deep-dive this week engages five things:

1. **At least one live controversy in the field.** Are reasoning models qualitatively different or just sampled more (Mon)? Is SWE-bench Verified a good proxy for real coding ability (Tue / Thu)? Has the "long context kills RAG" argument held up through 2025 (Fri)? Commit-per-iteration vs commit-per-feature for AI-directed code (Sat)?
2. **At least three citations to research, posts, or docs published after January 2024.** Frontier, not history.
3. **Runnable experiments that demonstrate mechanism.** You will run them by directing Claude Code or Claude.ai — not by hand-coding Python. The experiments produce numbers you see on your screen.
4. **Operator-level specifics with numbers.** Concrete performance figures with benchmark names, baselines, and confidence intervals where published. "Fable 5 scores 95.0% on the now-saturated SWE-bench Verified but 80.0% on SWE-bench Pro" beats "Fable is good at coding."
5. **A reviewer lens with named technical disagreements.** Each lesson names specific paragraphs a Karpathy, a Chip Huyen, a Simon Willison, or a Hamel Husain would push back on, and what they would argue instead.

## How to study this week

Each day, in priority order when you're short on time:

1. **Run the experiment.** This is where capability compounds. If you read the prose without running the experiment, you skimmed the lesson.
2. **Read the Must-read citations.** Usually three to five per lesson.
3. **Do the problem set.** Some are hands-on, some require reading a paper and taking a position.
4. **Read the lesson prose.** It is scaffolding for the first three.

The program's weekly rhythm (captured in `vault/00-program/how-to-study.md`) assumes you finish Week 0 by Sunday 2026-04-26 — because Week 1 begins the same day with a Monday lesson on prompting from first principles that composes directly on Monday's mental model of LLMs from this week.

## The Saturday onboarding session

The cohort's onboarding session on Saturday 2026-04-18 is a kickoff: cohort norms, program map, expectations, the live-session rhythm. It is not a substitute for this week's lessons. If you miss the onboarding, nothing in the vault becomes inaccessible — each lesson here is a standalone masterclass. If you attend the onboarding, the vault remains where you actually build the substrate.

## Week 0 is permanent infrastructure

Treat these six lessons as reference material you will come back to. When a later week asks you to compare Sonnet 5 to Gemini 3.1 Pro on a long-context agent, you will re-open Friday's lesson. When a later week asks you to reason about why your CLAUDE.md instructions are being ignored by a nested subagent, you will re-open Wednesday's. Week 0 is the layer underneath every other week — and because it covers the fastest-moving layer of the stack (model names, prices, tool features), it is also the layer most in need of the re-verification habit the lessons themselves teach. Model facts in this vault carry a `_last_verified` stamp; distrust anything older than a quarter.
