---
type: lesson
block: block-0-basecamp
week: week-01
day_of_cycle: 4
day_name: thu
session_slug: basecamp-part-2-vibe-coding
date_due: 2026-04-30
tags: [vibe-coding, cursor, claude-code, lovable, bolt, v0, replit, orientation, pre-read]
sources: [karpathy-vibe-coding-tweet, cursor-docs, claude-code-docs]
last_verified: 2026-04-14
---

# Thursday Pre-read: What Vibe Coding Actually Is

## Why this matters (operator framing)

In February 2025, Andrej Karpathy coined the term "vibe coding" in a tweet that ricocheted through the developer community[^1]. He described a new mode of software development: you describe what you want in natural language, accept what the model generates with minimal inspection, run it, and tell the model what to fix. The point is not perfect code — the point is working software fast.

This matters for you not as a philosophical position but as a competitive skill. A solo AI practitioner who can ship a functional web app in an afternoon, a Chrome extension in an hour, or a data pipeline in a morning competes differently than one who can't write code without an IDE and a week of scaffolding. Vibe coding is not about replacing engineers — it is about turning ideas directly into artifacts.

## Prerequisites

- [[01-mon-prompting-rags-preread]] — the prompting foundation matters here: vibe coding is applied prompting
- [[02-tue-prompting-deep-dive]] — especially the section on structured specifications
- No prior programming experience required (but helpful). You will run code today and tomorrow.
- [[00-program/how-to-study]] — keep the 7-day cycle in mind: this is a 35-minute orientation, not a deep-dive

## Core content

### What Karpathy actually said

The original tweet (Feb 2025) reads: "There's a new kind of coding I call 'vibe coding', where you fully give in to the vibes, embrace exponentials, and forget that the code even exists. It's possible because the LLMs (e.g. Cursor Composer with Sonnet) are getting good enough. You can make apps surprisingly fast, the iterations are fast, and it's fun."[^1]

He continued: "I just ask for what I want and it mostly works. Sometimes when things get weird, I'll do 'git diff', but mostly I don't even look at the code."

This is a strong claim. The reaction split the developer community: some saw it as the democratization of software creation; others saw it as a recipe for unmaintainable, insecure, debt-laden systems. Both are partially right. The key is knowing *when* to apply it.

### The three modes of AI-assisted coding

Not all AI coding is vibe coding. There is a spectrum:

**1. Copilot mode (autocomplete)**: the AI suggests the next line or block of code while you're typing. GitHub Copilot, Cursor's standard autocomplete. You read every suggestion. Used for: speeding up known work in a familiar codebase.

**2. Agentic coding (spec-driven)**: you write a detailed specification, the AI writes a plan, and then implements it step by step — reading files, running tests, making decisions. Claude Code and Cursor's "agent" mode operate here. You review at checkpoints. Used for: substantial features in production codebases where correctness matters.

**3. Vibe coding (prompt-driven, zero-review)**: you describe what you want, the AI generates the entire app or feature, you run it, give feedback in natural language, iterate. You accept changes without reading them. Used for: prototypes, throwaway scripts, MVPs you plan to rewrite, demos.

The mistake is applying mode 3 to situations that require mode 2. The mistake is also applying mode 2 to situations where mode 3 is fine — wasting time reviewing code for a throwaway demo.

### The tool landscape as of Q1 2026

The vibe coding ecosystem moved fast in 2025–2026. Here is the rough state:

**Cursor** — IDE built on VS Code, best-in-class codebase context (reads your entire repo), agent mode with multi-file edits, excellent for mode 2 and 3 in existing codebases[^2].

**Claude Code** — Anthropic's terminal-based agentic coding tool, released 2025. Runs in your terminal, reads the file system, runs commands, edits files. Best for: existing projects, complex refactors, infrastructure tasks. Strong operator-style system prompt under the hood[^3].

**Bolt** (StackBlitz) — browser-based, spins up a full-stack app in a container. Best for: JavaScript/TypeScript frontends, quick prototypes, no local setup required[^4].

**Lovable** — natural language to full-stack web app, generates React + Supabase backend. Best for: non-developers who want a functional app with a database[^5].

**v0** (Vercel) — generates React UI components. Best for: frontend design prototyping, component generation[^6].

**Replit** (Replit Agent) — cloud IDE with AI that can spin up and deploy a full-stack app. Best for: collaborative hacking, quick deployment, non-local workflows[^7].

### The spec-driven vs. prompt-driven debate

Simon Willison (one of the most thoughtful practitioners on this) draws a sharp distinction between vibe coding and responsible AI-assisted development[^8]. His position: "LLM-assisted coding is fantastic. Vibe coding — fully giving up on understanding what you ship — is a liability waiting to happen."

His key heuristics:
- If the code will touch user data, don't vibe code it. Understand it.
- If it's a one-off script for your own use, vibe code away.
- Always run the security scanner on anything you ship (he uses `bandit` for Python).

This is not a rejection of the tools — it is a rejection of the zero-understanding mode. The spec-driven approach: write a clear spec first, use the AI to implement it, review the output at key decision points.

### Three questions to bring to Sunday's session

1. You want to build a "give me a weekly digest of my Gmail inbox" tool this weekend. Which tool (Cursor, Claude Code, Bolt, Lovable, v0, Replit) would you use, and why? What are the risks if you vibe code it without reading the implementation?

2. Karpathy says he doesn't even look at the code. Under what circumstances is that irresponsible? Under what circumstances is it totally fine?

3. Think of one real project you want to build during this program. Map it to mode 1, 2, or 3 from the spectrum above. Is it a prototype, an agentic feature, or an autocomplete-speed task?

## Worked example

No code lab today. Instead, do this 15-minute experiment:

1. Go to Bolt.new (or v0.dev if you prefer React components).
2. Type: "Build a simple task manager with a text input to add tasks, a list of tasks with checkboxes, and a clear-completed button."
3. Watch it generate the app. Run it.
4. Notice: where is the state stored? What happens if you refresh? What would break if you wanted to add user authentication?

This experiment surfaces the gap between "works in a demo" and "works as a product." That gap is the main topic of Friday's deep-dive.

## Common mistakes experts see

- **Vibe coding production systems**: customer-facing authentication, payment processing, and data pipelines should be understood, not vibed. The liability is real.
- **Not using git**: if you're not committing after each working state, you lose the ability to roll back when the model goes off the rails. Karpathy himself does `git diff` — don't skip it.
- **Over-relying on one tool**: Cursor for everything, Claude Code for everything. Each tool has a distinct strength. Learn the landscape.
- **Treating generated code as a black box**: even in vibe coding mode, skimming the generated structure (not every line) gives you the mental model to course-correct faster.
- **Not giving good specs**: "build an app" produces mediocre code. "Build a React app with a sidebar navigation, a main content area, and a settings modal" produces much better code. The quality of your natural language spec is the primary bottleneck.

## Reflection questions

1. What is the difference between vibe coding and using GitHub Copilot? Where would you draw the line?
2. Simon Willison would say vibe coding is fine for some use cases and dangerous for others. Where exactly is the line, and who gets to draw it?
3. For a solo AI practitioner (not a traditional engineer), what is the highest-ROI use of vibe coding skills?
4. Why does context length matter for vibe coding tools like Cursor and Claude Code?
5. If a client asks you to deliver a data pipeline that processes sensitive PII — would you vibe code it? What would your process look like instead?

## My take (reviewer lens)

Karpathy would say most people are still not moving fast enough. His vibe coding framing is partly a critique of the developer culture's attachment to craftsmanship when the product need is just "does it work." The iteration speed of modern tools means you can afford to throw away and rebuild what a previous generation would have agonized over.

Seibel would be blunter: "Ship it. If your startup is debating the code quality of your MVP, you've already lost." He'd put vibe coding in the same bucket as "do things that don't scale" — it's the right tool for the right stage, and the wrong tool for the wrong stage.

Boris Cherny (Claude Code's lead) would point out that the most valuable use of vibe coding tools is not writing new code from scratch but navigating and modifying existing large codebases — understanding codebase structure, doing targeted refactors, and answering "what does this function actually do?" at scale. That use case requires deeper tool integration (reading the repo, running tests, understanding dependencies) than most people realize.

## Further reading

**Must-read before Sunday**
- Karpathy, vibe coding tweet thread — <https://x.com/karpathy/status/1886192184808149383> (Feb 2025)
- Claude Code docs — <https://docs.anthropic.com/en/docs/claude-code>

**Recommended**
- Simon Willison, "Things I've learned about LLM-assisted coding" — <https://simonwillison.net> (search his blog, 2025 posts)
- Cursor documentation — <https://docs.cursor.com>

**Optional**
- Bolt.new — try it live: <https://bolt.new>
- v0 by Vercel — <https://v0.dev>

## Citations

[^1]: Andrej Karpathy, "Vibe coding tweet," *X (formerly Twitter)*, Feb 2025, <https://x.com/karpathy/status/1886192184808149383>. Original coinage of "vibe coding" and description of the zero-review iteration mode.

[^2]: Cursor, "Cursor Documentation," <https://docs.cursor.com>, accessed 2026-04-14. Overview of agent mode, Composer, and multi-file context.

[^3]: Anthropic, "Claude Code," *Anthropic Documentation*, <https://docs.anthropic.com/en/docs/claude-code>, accessed 2026-04-14. Terminal-based agentic coding tool documentation.

[^4]: StackBlitz, "Bolt.new," <https://bolt.new>, accessed 2026-04-14. Browser-based full-stack application generation.

[^5]: Lovable, "Lovable Documentation," <https://docs.lovable.dev>, accessed 2026-04-14. Natural language to React + Supabase application generation.

[^6]: Vercel, "v0 — Generative UI," <https://v0.dev>, accessed 2026-04-14. Component-level React UI generation.

[^7]: Replit, "Replit Agent," *Replit Documentation*, <https://docs.replit.com/replitai/agent>, accessed 2026-04-14.

[^8]: Simon Willison, "Thoughts on vibe coding and the responsibility of shipping," *simonwillison.net*, 2025, <https://simonwillison.net>. Distinction between LLM-assisted coding (responsible) and vibe coding (context-dependent); security scanner recommendation.

_last_verified: 2026-04-14_
