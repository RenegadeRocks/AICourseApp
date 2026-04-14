---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 6
day_name: sat
session_slug: basecamp-part-2-vibe-coding
date_due: 2026-05-03
tags: [vibe-coding, live-session, build, companion, cursor, claude-code]
sources: [karpathy-vibe-coding-tweet, claude-code-docs, cursor-docs]
last_verified: 2026-04-14
---

# Saturday Live-Session Companion: Vibe Coding in Practice

> This is your in-session companion document. Open it alongside the live session.
> Use the blank sections to capture what the instructor builds. The build prompts below are your fallback if you fall behind — you can reconstruct the demo after the session.

## Why this matters (operator framing)

Live sessions are where theory meets the instructor's taste. Dileep will make judgment calls you won't find in documentation — which tool to reach for first, how to structure the spec, when to stop iterating and ship. These decisions live in the session, not the recording. Your job today: capture not just what was built but *why each decision was made*.

## Prerequisites

- [[05-fri-vibe-coding-tools]] — tool landscape deep-dive
- [[04-thu-vibe-coding-preread]] — vibe coding mental model
- Have at least one tool open and ready to type: Cursor, Claude Code (terminal), or Bolt.new
- API key set up (Anthropic API key for Claude Code; no key needed for Bolt)

## Pre-session checklist (complete before 7:30 PM IST)

- [ ] Cursor installed and logged in, or Claude Code installed (`npm install -g @anthropic-ai/claude-code`)
- [ ] Bolt.new open in a browser tab (no auth needed)
- [ ] Lovable account created if you want to follow along there
- [ ] A text file open for session notes
- [ ] This document open in Obsidian or your markdown reader

## Session structure (anticipated)

Based on the curriculum topic "Basecamp Part 2: Vibe Coding," the session will likely cover:

1. **Live demo — tool walkthrough** (Cursor or Claude Code)
2. **Build-along — a real mini-app** from spec to running demo
3. **Comparison** — at least two tools on the same task
4. **Q&A / live debugging** — where the real learning happens

## Build-along: capture zone

Use this section during the session. Fill in as Dileep builds.

### What is being built?

_(write here during session)_

### Spec used (capture the exact prompt/spec Dileep writes)

```
[capture the spec or prompt here]
```

### Tool chosen and why

_(capture the instructor's reasoning)_

### Key prompts issued

```
Prompt 1:

Prompt 2:

Prompt 3:
```

### Where it broke and how it was fixed

| Error / issue | Fix used | Lesson |
|---|---|---|
| | | |

### Final output

_(describe what was built, link to any deployed URL if shared)_

## Your parallel build

The best use of this session: build the same thing independently on your own machine, in parallel. When Dileep issues a prompt, you issue the same prompt. When his version breaks, try to predict the fix before he reveals it.

**Your prompts** (write them here):

```
[your prompt 1]

[your prompt 2]
```

**Differences between your output and the instructor's**:

_(note what diverged and why — different tool? different spec wording? different model?)_

## The reconstructed build (post-session)

After the session, if you have the recording, use this structured guide to reconstruct the demo from scratch. Doing it again solo — without following along — is where the learning solidifies.

### Suggested build: Customer FAQ Chatbot with RAG

If the instructor builds something different, use this as a solo extension exercise.

**Spec**:
```markdown
# Customer FAQ Chatbot Spec

## What it does
A web chat interface that answers questions about a product using a curated FAQ document.

## Features (ranked)
1. Text input + submit button + chat history display
2. FAQ document loaded on startup (can be a plain .txt or .md file)
3. Simple RAG: embed FAQ, retrieve top-2 chunks, generate answer with Claude
4. Clear conversation button

## Tech stack
- Frontend: React (use v0 to generate the chat UI component)
- Backend: Node.js or Python FastAPI
- Retrieval: in-memory (no DB needed for this prototype)
- LLM: Claude claude-haiku-4-5-20251001 (cheap, fast)
- No auth needed (local prototype)

## Success definition
I can type "What is your return policy?" and get an answer that references the FAQ.
```

**Build sequence**:
1. Generate the chat UI with v0 or Bolt
2. Add the Python/Node.js backend
3. Implement the RAG retrieval (use the code-lab as reference)
4. Connect frontend to backend
5. Test with 5 different questions

**Expected time**: 45–60 minutes if following Friday's patterns.

## Questions to ask during Q&A

Use these or adapt based on what was built:

1. "When the model gives a wrong answer, how do you debug whether it's a retrieval issue or a generation issue?"
2. "How do you handle the case where the model confidently answers from a retrieved chunk that's wrong or outdated?"
3. "What's your threshold for when you stop vibe coding and start reading the generated code?"
4. "How do you version-control a project where you're using Lovable or Bolt and the generation is non-deterministic?"
5. _(your own question based on this week's reading)_: ___

## Key quotes and decisions to capture

_(use this space during the session for anything the instructor says that sounds like a principle rather than a how-to. These are the highest-signal notes to keep.)_

> "..."

> "..."

> "..."

## Common mistakes experts see (live edition)

These often come up during live builds — watch for them:

- **Prompt too vague → model picks the wrong framework**: "build a web app" gets React from Bolt and Flask from Cursor because the tool defaults differ. Always specify the stack.
- **No error handling in generated code**: ask explicitly: "add try/except around every external call and log the error."
- **Generated env vars not configured**: generated code often references `process.env.API_KEY` without creating a `.env.example`. Always check.
- **CSS conflicts**: when stitching v0 components into a Bolt project, Tailwind class conflicts can silently break layouts. Verify visually.
- **CORS issues**: if the frontend and backend run on different ports, generated code rarely includes CORS headers. Fix: add `cors` middleware.

## Reflection questions

1. What was the highest-leverage decision Dileep made during the build? (Not the most impressive — the most *leveraged*.)
2. Where did the generated code surprise you (positively or negatively)?
3. Which part of the session would you want to rebuild with a different tool? Why?
4. If you were charging a client for this deliverable, what would you charge, and how long did it actually take?
5. What will you build tomorrow using what you learned today?

## My take (reviewer lens)

Karpathy would be watching the iteration speed. The question he asks is not "is the code good?" but "how many iterations did it take to get to working?" If it took 12 back-and-forth prompts to fix a bug that a good spec would have prevented, the spec was the bottleneck. Count your iterations — that metric reveals your spec quality better than anything else.

Seibel would be watching for the moment you get "good enough" and ship. The most common failure mode in live builds is over-polishing — spending the last 30 minutes of a session adding features nobody asked for instead of deploying the working version and getting feedback.

Boris Cherny would be watching the error recovery. The interesting part of any live build is when the model produces code that breaks — how do you diagnose it, what do you tell the model, and how quickly do you converge? That recovery loop is the actual skill being demonstrated.

## Further reading

**Session-specific**
- Claude Code docs — <https://docs.anthropic.com/en/docs/claude-code>
- Cursor agent mode — <https://docs.cursor.com/cmdk/overview>

**If you want more live build examples**
- Simon Willison's "TIL" posts — many document his live builds: <https://til.simonwillison.net>

## Citations

[^1]: Andrej Karpathy, "Vibe coding," *X*, Feb 2025, <https://x.com/karpathy/status/1886192184808149383>.

[^2]: Anthropic, "Claude Code," *Anthropic Documentation*, <https://docs.anthropic.com/en/docs/claude-code>, accessed 2026-04-14.

[^3]: Cursor, "Agent mode," *Cursor Documentation*, <https://docs.cursor.com/cmdk/overview>, accessed 2026-04-14.

_last_verified: 2026-04-14_
