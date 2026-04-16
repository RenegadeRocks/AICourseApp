---
type: lesson
block: block-0-basecamp
week: week-00
day_of_cycle: 2
day_name: tue
session_slug: ai-catalyst-program-onboarding
date_due: 2026-04-21
tags: [ai-coding-tools, claude-code, codex-cli, cursor, aider, cline, roo-code, replit-agent, windsurf, swe-bench, mcp, agent-loop, tool-selection]
sources:
  - anthropic-opus-4-6-release
  - anthropic-claude-code-docs
  - anthropic-sub-agents
  - openai-codex-cli
  - openai-gpt-5-system-card
  - cursor-2-0-changelog
  - aider-leaderboards
  - cline-plan-act-docs
  - roo-code-modes
  - windsurf-cascade
  - replit-agent-4
  - swebench-verified-leaderboard
  - swebench-pro-scale
  - hamel-husain-evals-faq
  - simon-willison-trifecta
  - willison-inflection-2025
  - anthropic-sonnet-4-5
  - anthropic-opus-4-5
last_verified: 2026-04-15
word_count_target: 6000
---

# The AI-native builder stack — seven tools, six axes, one honest answer for which one to reach for Monday morning

## Why this matters

You are about to spend 26 weeks directing AI coding tools the way a technical founder directs a small team. The tool you pick is not a matter of taste. It shapes which bugs you can fix in a lunch hour, which refactors you will attempt at all, which production incidents you can triage from a phone, how much context you burn per feature, and — the part nobody writes down — which parts of your codebase silently become off-limits because your tool's permission model makes them too expensive to touch.

By Friday of Week 0 you need a working rig. By the end of this lesson you should be able to (a) explain the six axes on which AI coding tools actually differ, (b) name one specific failure mode of each of the seven tools we will cover, (c) read a SWE-bench Verified leaderboard number and say out loud what it does and does not tell you, and (d) run an honest head-to-head between Claude Code and one alternative on a real bug, measuring tool-calls, wall-time, and diff quality — not vibes.

This lesson is standalone. If you never attend a live session it still teaches the full topic. It is not a recap of "what is Cursor" — it assumes you have opened all seven tools at least briefly and now need an operator-grade comparison you can cite in a tech-selection memo.

## Prerequisites

- A working Claude Code install (any version ≥ the one shipped with Opus 4.6 in February 2026 is fine).[^1]
- One of: an active Cursor Pro trial, a Codex CLI install with an OpenAI key, or an Aider install with a Sonnet or GPT-5 key. You do not need all of them this week — you need one alternative to Claude Code so you can do the head-to-head experiment in Layer 6.
- A small repository with at least one real open bug. SWE-bench Lite instances work; a personal side project with a real ticket in its backlog works better, because the measurement is more honest when you know the code.
- [[01-mon-first-principles-of-ai-native-work]] from Monday, if you have it. This lesson composes with it but does not depend on it.

## Layer 1 — The six axes that actually separate these tools

The market-speak ("AI coding assistant", "autonomous agent", "AI-native IDE") is useless for picking between them. Strip it away. Every tool in this space is some specific choice along six axes, and once you see the axes you cannot unsee them.

**Axis 1. Agent loop shape.** Every coding tool is, under the hood, a loop of the form *(assemble context → model call → parse tool-use requests → execute tools → append results → repeat)*. What varies: who spawns what, whether the model plans before executing or interleaves, and how many tool calls per turn the loop is willing to spend before handing back to you. OpenAI's public teardown of the Codex CLI loop describes exactly this cycle — a Responses-API call that streams either a final message or a tool request, executes the tool locally, appends the result, and resubmits the expanded context until no more tool calls are emitted.[^2] Claude Code runs the structurally identical loop against Anthropic's Messages API, with three wrinkles that matter: (a) it can spawn *subagents* — isolated sub-loops with their own system prompts, tool permissions, and context windows, which report back a single summary to the parent loop[^3]; (b) it can fire *hooks* — shell commands before/after tool use, useful for enforcing policy or running tests[^4]; (c) it supports *adaptive thinking*, where the model decides mid-turn how many reasoning tokens to spend before emitting a tool call.[^1]

Cursor's Composer is a loop of a different shape. Until Cursor 2.0 (late 2025) it was mostly a single-pass "generate coordinated edits across these files" engine; the 2.0 changelog explicitly reframed Cursor as agent-first, with an Agent mode that plans multi-step work, executes terminal commands, and iterates — at which point the shape converges toward Claude Code's, with the key difference that Cursor's loop is embedded in an IDE rather than a terminal.[^5] Aider's loop is deliberately thin: a git-aware REPL that edits files, runs tests if you ask, and commits every change as a diff you can `git revert`. Cline and Roo Code run the loop inside VS Code, with Cline enforcing an explicit two-phase Plan/Act structure (you approve a plan before any file mutation happens) and Roo Code layering "modes" — role-scoped agents, like a planner or a reviewer — on top of the same core.[^6][^7] Replit Agent 3/4 runs the loop on Replit's hosted VM, which changes the sandboxing story entirely. Windsurf Cascade runs a local-VS-Code loop optimized for multi-file refactor planning rather than scaffolding new apps.[^8]

When you compare tools, the single most useful question is: *"how many tool calls does this thing burn to fix one bug, and how much of that budget does it spend reading code I already handed it?"* Token efficiency is almost entirely a function of loop design.

**Axis 2. Memory model.** Every tool has some answer to "how do you remember what to do in this repo tomorrow?" Claude Code's answer is the CLAUDE.md tier system: project-level `./CLAUDE.md`, user-level `~/.claude/CLAUDE.md`, and — for subagents — a `MEMORY.md` that is read into the subagent's system prompt at spawn time, capped at ~200 lines or 25KB.[^3][^9] Cursor's historical answer was `.cursorrules`; the modern answer is `AGENTS.md` at the repo root plus package-level `AGENTS.md` files that layer, plus `.mdc` rule files that are scoped to paths.[^10] Aider's answer is `CONVENTIONS.md`, a plain-text file you add with `/read-only` so it's pinned to every turn. Cline writes a `.clinerules` file and can persist task-level memory across sessions. Codex CLI has no durable project memory as of its April 2025 architecture; it takes a per-session system prompt and configuration lives in `~/.codex/config.toml`.[^11] Replit's memory is the Replit workspace itself — persistent VM state, files, and environment — which is the strongest form of memory in the set and also the most opaque to version control.

The operator lens: memory *is* portability. If you put your hard-won instructions into CLAUDE.md, moving to Cursor means translating them into AGENTS.md; moving to Cline means `.clinerules`. The tools mostly agree on the shape (plain-text markdown, layered by scope) but disagree on the file names — which means switching cost is real but non-catastrophic. A reasonable working pattern, followed by several of the practitioners Simon Willison cites in his 2025 state-of-AI retrospective, is to maintain one canonical `AGENTS.md` and symlink or copy to whatever the current tool expects.[^12]

**Axis 3. Tool surface.** This is the *set of actions the model can request*. Built-ins vary: Claude Code ships Read, Write, Edit, Bash, Glob, Grep, WebSearch, WebFetch, and a Task tool for spawning subagents. Codex CLI ships shell execution plus file IO against the working directory. Cursor's tools include file-edit, terminal, web-search, and IDE-specific affordances (selection, cursor position). Aider's "tools" are essentially git operations and file diffs. Cline and Roo Code expose file, terminal, browser-automation, and MCP. Extensibility then diverges dramatically: Claude Code, Codex CLI, Cline, and Roo Code all speak the Model Context Protocol natively, so you can attach any MCP server (Notion, Playwright, Postgres, Linear, Supabase, etc.) and the model can call it as a first-class tool. Cursor added MCP support in 2025. Replit and Windsurf are more closed — extensibility runs through their own plugin systems.

Practically: if you work in an ecosystem with a lot of third-party MCPs (which, by 2026, is most teams), "native MCP" is no longer a differentiator but "number of MCPs you can attach without plumbing" is. Claude Code leads here by volume of community-maintained MCPs; Codex CLI is close behind and growing quickly.[^11]

**Axis 4. Filesystem access and sandboxing.** Where can the loop read and write? What blocks it? This is where tools diverge most visibly to users, because the friction of *"this prompted me again"* is felt on every turn.

Claude Code defaults to prompting on every Bash invocation and every file write outside the working directory, with an allowlist (`.claude/settings.local.json` → `permissions.allow`) you build up over time. Hooks can tighten this further: `PreToolUse` hooks can run an arbitrary shell check before any tool fires and veto it.[^4] Codex CLI defaults to a lighter-touch model where the tool auto-approves shell commands unless they match a denylist, with a configurable sandbox mode. Cursor in agent mode runs against your workspace with terminal access and file writes; there is no per-command prompt — you see the diff before it applies and can accept or reject. Aider writes only to files you've `/add`ed, which is a different kind of sandbox — narrow by construction. Cline's Plan/Act mode is explicitly conservative: it generates a plan, you approve, it executes; file edits are always shown as diffs. Roo Code inherits this and adds role-scoped permission per mode. Replit's sandbox is the strongest in the set because it's a fresh VM you can burn down and rebuild; this is why Replit Agent can run commands and install packages without the hesitation appropriate on your laptop.[^13] Windsurf runs locally with human-in-the-loop approvals for multi-file edits.

The axis that actually matters for daily work is *how much friction does the approval model add per turn*, weighted by *how much damage the tool can do if you just say yes to everything*. Claude Code's default is the right prior for production repos; Replit's is the right prior for scaffolding from scratch; Aider's is the right prior if you want extreme narrowness.

**Axis 5. Model access.** Cursor is multi-model and lets you swap between GPT-5.3 Codex, Claude Sonnet 4.6, Gemini 3 Pro, and Cursor's own Composer model mid-session.[^14] Claude Code is Claude-only (Opus 4.6, Sonnet 4.6, Haiku 4.5). Codex CLI is OpenAI-only. Aider, Cline, Roo Code, and Windsurf are model-agnostic — you bring any key (Anthropic, OpenAI, Google, OpenRouter, local via Ollama). Replit Agent is controlled by Replit's model routing and changes under you.

If you have a strong prior about which model is best for a given task — and if you operate as an AI-catalyst lead you will — the Claude-only and OpenAI-only tools lock you to that frontier. That is usually fine; it stops being fine when the frontier moves, which it did between October 2025 (Anthropic's Sonnet 4.5) and February 2026 (Anthropic's Opus 4.6, after a three-month stretch where GPT-5 Codex led on several benchmarks).[^1][^15]

**Axis 6. Pricing and real-world cost per task.** Claude Code is priced three ways: Pro at $20/month (light use), Max 5x at $100/month, Max 20x at $200/month, or pay-as-you-go via Anthropic API at $5 input / $25 output per million tokens for Opus 4.6 (plus the 1M-context premium tier at $10/$37.50 above 200K).[^1][^16] Codex CLI is API-only (pay-as-you-go). Cursor is $20/month Pro with a credit-based overage system that has produced widely reported bill shocks — one team's annual $7,000 subscription depleted in a single day of heavy agentic use in 2026, per reporting compiled by morphllm's comparison study.[^17] Aider is free; you pay only the underlying model API. Cline and Roo Code are free; you pay the model. Windsurf is $15/month Pro. Replit is $25/month Core with additional agent-credit metering.

Independent measurements compiled through late 2025 and early 2026 suggest Claude Code uses roughly 4–5× fewer tokens than Cursor for identical tasks (Morph's 47-file benchmark landed at 4.2× for Aider-versus-Claude-Code; other shops report 5.5× for Claude-Code-versus-Cursor).[^17] The reason, consistent across reports: the *loop design*. Aider minimizes context by being narrow; Claude Code minimizes by using subagents and targeted Grep/Glob rather than file dumps; Cursor's Composer tends toward broader file inclusion because that is what the IDE UX rewards.

These six axes are not independent — memory interacts with loop design, sandboxing interacts with tool surface — but they are the only honest factorization I've found. Every tool teardown below uses them.

## Layer 2 — Per-tool teardown

Each teardown follows the same template: loop shape → memory → tool surface → sandbox → pricing → where it wins.

### Claude Code

Loop: terminal-native, turn-based, can spawn subagents via the Task tool. Adaptive thinking lets the model burn 1K–60K+ reasoning tokens per turn before emitting a tool call; in Opus 4.6 this is exposed as four explicit effort levels (low / medium / high / max).[^1] Plugins exist for VS Code and JetBrains that surface the loop inside an IDE without changing the underlying architecture — you get the same CLAUDE.md-driven loop, just with a panel instead of a terminal.

Memory: three-tier CLAUDE.md (user / project / local) plus per-subagent MEMORY.md read at spawn time (200 lines / 25KB cap).[^3][^9] This is the most layered memory model in the set.

Tool surface: Read / Write / Edit / Bash / Glob / Grep / WebSearch / WebFetch / Task (subagent spawn) built-in. MCP native; thousands of community MCPs. Hooks fire shell commands on `PreToolUse`, `PostToolUse`, `Stop`, and session boundaries.[^4]

Sandbox: permission prompt per Bash command and per file write outside CWD by default; `.claude/settings.local.json` allowlist grows with use; `PreToolUse` hooks can veto arbitrary commands. Worktree isolation is supported — you can run multiple Claude Code sessions in separate git worktrees without them interfering.

Pricing: $20 Pro, $100 Max 5x, $200 Max 20x, or API at $5/$25 per million tokens (Opus 4.6). The Max plan saves heavy users 90%+ versus API: Anthropic Max subscribers have reported large-multiple savings on sustained heavy usage versus API pay-as-you-go, though the exact numbers vary by usage pattern, model mix, and plan tier.[^16]

Where it wins: *long-horizon, repo-aware work*. Debugging that requires understanding conventions three directories away, multi-step refactors that touch 20 files, feature work where you need a plan, a critique, and a test loop in the same session. Opus 4.6's 80.8% on SWE-bench Verified and its explicit optimization for "agent teams" make it the default if you're building anything non-trivial.[^18][^1]

Where it loses: rapid scaffolding of brand-new projects from a spec (Replit wins), tight-loop refactors inside an IDE with live feedback (Cursor wins), extreme token frugality on narrow edits (Aider wins).

### Codex CLI (OpenAI / GPT-5)

Loop: Rust binary, terminal-native, structurally very similar to Claude Code — a Responses-API call streams either a final message or a tool request, local execution, append to context, loop until no more tool calls.[^2] Open-source (github.com/openai/codex) so you can read the loop directly.[^11]

Memory: per-session system prompt; `~/.codex/config.toml` for configuration; no durable per-project memory tier as rich as CLAUDE.md as of the April-2025 architecture. MCP servers can inject persistent context, which is the workaround most operators use.

Tool surface: shell, file IO, MCP (stdio and streaming-HTTP) configured in `config.toml` or via `codex mcp` subcommands.[^11] Smaller built-in set than Claude Code; parity comes via MCP.

Sandbox: configurable sandbox mode; lighter default approval than Claude Code's (auto-approves common shell commands). Denylist-based rather than allowlist-based by default.

Pricing: pay-as-you-go via the OpenAI API. GPT-5.3 Codex is the current flagship; GPT-5 itself reported 74.9% on SWE-bench Verified at release and 88% on Aider Polyglot.[^15][^19] (Caveat: like every SWE-bench Verified number, this reflects specific harness choices — a 477-task internal subset, particular tool/scaffold conditions, and OpenAI-chosen inference settings. Thursday's lesson teaches how to read these conditions critically before treating the number as comparable to another vendor's.) Costs depend on which GPT-5 tier you point it at.

Where it wins: teams already standardized on OpenAI billing; open-source loop you can fork; fastest iteration on loop-level research because the source is right there.

Where it loses: memory model is weaker out of the box; ecosystem of community MCPs is smaller than Claude Code's (closing, not closed); no equivalent of CLAUDE.md-style tiered project memory.

### Cursor (IDE + Composer + Agent mode)

Loop: until Cursor 2.0, a single-pass multi-file editor (Composer). From 2.0 (late 2025), agent-first with multi-step planning, terminal exec, and multi-file editing in one loop.[^5] Inline tab-complete coexists with agent mode, so the same surface handles both "complete this line" and "build this feature."

Memory: AGENTS.md at root, path-scoped `.mdc` rule files, legacy `.cursorrules` still supported.[^10] The layered model is similar to Claude Code's but file names differ.

Tool surface: file edit, terminal, web search, IDE-native (selection, cursor, buffer state). MCP support added in 2025. Multi-model — swap between GPT-5.3 Codex, Sonnet 4.6, Gemini 3 Pro, Composer-1 mid-session.[^14]

Sandbox: diffs previewed before apply; terminal commands shown before run; no per-Bash-command prompt by default.

Pricing: $20/month Pro with credit overages that have produced public bill shocks; Business/Enterprise tiers exist.[^17]

Where it wins: *tight refactor loops and "AI-first editor" workflows*. If 70% of your day is writing and editing code in an editor and you want ghost-text + multi-file agent in the same surface, Cursor remains the strongest single product. Multi-model access is the closer on "but which model is best?" arguments.

Where it loses: predictable agent-run cost ceilings (Cursor's pricing-update and overage patterns have repeatedly drawn user complaints in 2025–2026); the IDE coupling makes headless / CI-driven workflows awkward. On raw tokens-per-task Cursor is actually competitive — Morph's 3-tool benchmark clocks it at roughly parity with Aider and ~4.6× more efficient than Claude Code on the same 47-file task set[^17] — so the cost story here is about usage patterns and billing model, not per-task token count.

### Aider

Loop: thin, terminal-native, git-aware REPL. Every edit is a commit; `git revert` is your undo. Loop is deliberately narrow — a short turn, a focused edit, a test run if configured.

Memory: `CONVENTIONS.md` added via `/read-only` pins it to every turn. No deeper tier system.

Tool surface: file edit, git, test run. No native MCP support (as of the leaderboard-referenced versions).[^20] Bring-your-own-keys for any LLM.

Sandbox: narrow by construction — only files added to the session via `/add` are candidates for edit.

Pricing: free; pay underlying model API.

Where it wins: *surgical edits on tight token budgets* and *transparent commit-per-change workflows* that play nicely with human review. Aider's own benchmarks show it completing balanced-accuracy tasks in 257 seconds with 126K tokens — the best token-per-result ratio in Morph's comparison set.[^17] The Aider Polyglot benchmark itself is a useful eval: 225 Exercism exercises across C++, Go, Java, JavaScript, Python, and Rust, and GPT-5 scored 88% on it at release.[^19][^20]

Where it loses: long-horizon work (loop is too narrow); anything that benefits from subagents or a plan-critique-execute cycle.

### Cline and Roo Code (VS Code agentic extensions)

Loop: runs inside VS Code. Cline enforces Plan/Act — two explicit phases where Plan produces an approved plan and Act executes against it. Roo Code builds on the same base but introduces multiple *modes* (roles) — a Code mode, an Architect mode, a Debug mode, a custom mode you define — each with its own system prompt and tool subset.[^6][^7]

Memory: `.clinerules` (Cline), mode-specific prompts and memory (Roo Code). MCP-native in both; Cline ships an MCP marketplace for one-click installs, Roo requires manual MCP server configuration.[^6]

Tool surface: file, terminal, browser automation, MCP. Model-agnostic (bring any key).

Sandbox: human approval for every file mutation by default; Plan mode is the sandbox.

Pricing: free; pay underlying model.

Where it wins: *teams that want an open-source, model-agnostic agent inside an IDE they already use*. Cline's Plan/Act is, in my experience, the best explicit-plan UX in the set — easier to review than Cursor's implicit plans and safer than Codex CLI's light default. Roo Code's modes are the best starting point if you want to separate "architect" and "implementer" roles without building your own subagent plumbing.

Where it loses: no single provider pushing the product forward on the same cadence as Cursor or Claude Code; discoverability (the two tools are best-known among already-agentic operators).

### Replit Agent 3/4

Loop: runs on Replit's hosted VM. Agent 4 handles end-to-end app scaffolding — natural language → deployed, running app — with real-time collaboration and one-click deploy.[^13]

Memory: the Replit workspace itself. Persistent VM state, files, environment, database.

Tool surface: everything Replit exposes as a service — database, auth, hosting, deploys.

Sandbox: the VM is the sandbox. You can burn it down and rebuild. This is the strongest sandbox in the set.

Pricing: Replit Core $25/month + agent-credit metering.

Where it wins: *zero-to-deployed scaffolding* and *collaborative demos*. If your task is "I have a brief, I need a working app link by end of day," Replit is the fastest path. Also the right pick for non-technical operators on your team who need to prototype without local setup.

Where it loses: production engineering workflows; anything where you want local, version-controlled code you can move to a real repo; long-horizon debugging of existing systems (the VM state becomes a black box).

### Windsurf (Cascade)

Loop: VS-Code-fork IDE (acquired by Cognition in July 2025 after Google's $2.4B reverse-acquihire of Windsurf's CEO and co-founders left the remaining company, IP, and team available for sale).[^27] Cascade is a planning-first agent optimized for multi-file refactors with human-in-the-loop approvals on each step.[^8]

Memory: workspace-scoped memory; less layered than AGENTS.md.

Tool surface: file edit, terminal, MCP.

Sandbox: approval-per-step on multi-file edits.

Pricing: ~$15/month Pro.

Where it wins: *large-codebase refactor planning*. Cascade's planning output is explicitly structured around "here is the set of changes, here is the order, here is the diff per step" — easier to review than Cursor's plans for refactors that span 10+ files.

Where it loses: app scaffolding (Replit wins); general-purpose agentic coding (Claude Code wins); ecosystem (smaller MCP base, less community).

## Layer 3 — The comparison table

This is the table you actually want to keep open. Every column is one of the six axes.

| Tool | Loop shape | Memory | Tool surface | Sandbox | Model lock | Typical cost (heavy user) |
|---|---|---|---|---|---|---|
| Claude Code | CLI + IDE plugin, subagents, hooks, adaptive thinking[^1][^3] | CLAUDE.md × 3 tiers + subagent MEMORY.md[^9] | Read/Write/Edit/Bash/Glob/Grep/Web + MCP + hooks | Per-Bash prompts + allowlist + PreToolUse vetos[^4] | Claude-only | $100–200/mo Max; $130–260/mo API[^16] |
| Codex CLI | Terminal, Rust, open-source loop[^2][^11] | `config.toml`, no tiered project memory | Shell + file IO + MCP | Configurable sandbox, denylist default | OpenAI-only | API pay-as-you-go |
| Cursor | IDE, tab-complete + Composer + Agent mode[^5] | AGENTS.md + `.mdc` rules[^10] | File/terminal/web + MCP | Diff preview, no per-command prompt | Multi-model (GPT/Claude/Gemini)[^14] | $20 Pro + credit overages (can spike)[^17] |
| Aider | Terminal REPL, git-per-change[^20] | CONVENTIONS.md | Files + git + tests | Only `/add`ed files editable | Bring-your-own model | Model-API only (cheapest) |
| Cline | VS Code ext., Plan/Act[^6] | `.clinerules` | File/terminal/browser + MCP marketplace | Plan approval gates Act | Bring-your-own model | Model-API only |
| Roo Code | VS Code ext., multi-mode[^7] | Mode-scoped prompts | File/terminal/browser + MCP (manual) | Mode-scoped permissions | Bring-your-own model | Model-API only |
| Replit Agent | Hosted VM[^13] | Workspace state | Full Replit platform | VM sandbox (strongest) | Replit-controlled | $25/mo + agent credits |
| Windsurf | IDE, Cascade planning[^8] | Workspace memory | File/terminal + MCP | Step-by-step approvals | Multi-model | ~$15/mo |

## Layer 4 — The benchmark you will be cited at: SWE-bench Verified, and why it doesn't mean what you think

If you attend a tech-selection conversation this month, someone will cite SWE-bench Verified. You need a defensible position.

**What it is.** SWE-bench Verified is a 500-problem Python-only subset of SWE-bench, human-filtered by OpenAI in August 2024 to remove ambiguously specified tasks from the original SWE-bench. The harness checks whether a model-generated patch causes a repo's real test suite to pass.

**Where the frontier is, April 2026.** Per the aggregated leaderboard snapshots from swebench.com and third-party trackers through March–April 2026: Claude Opus 4.5 at 80.9%, Claude Opus 4.6 at 80.8%, Gemini 3.1 Pro at 80.6%, MiniMax M2.5 at 80.2%, GPT-5.2 at 80.0%, with a top Claude "Mythos Preview" entry at 93.9% reported on some third-party trackers.[^18][^21] Claude Sonnet 4.5 hit 77.2% at 200K thinking budget and 82.0% with parallel test-time compute as of its September 2025 release.[^22] GPT-5 at release in August 2025 reported 74.9% on Verified (using a fixed 477-task subset on OpenAI's internal infrastructure — not the 500-task public harness).[^15]

Aider Polyglot is the adjacent benchmark: 225 Exercism exercises across six languages. GPT-5 leads at 88%; Claude 3.7 Sonnet with extended thinking hit 93%+ via agentic wrappers like Refact.ai.[^20]

**Position A (the publishers): SWE-bench Verified is the best general-purpose coding eval we have.** Anthropic, OpenAI, and Google publish it as their headline coding number. The harness is reproducible; the tasks come from real PRs; the human filter addresses the original SWE-bench's ambiguity problem.

**Position B (the critics): the Verified numbers are contaminated and ceiling-bound.** Morph's September-2025 teardown of SWE-bench Pro versus Verified documents the gap: *"The best model scores 46% on Pro but 81% on Verified, because Verified is contaminated."*[^23] Scale AI's SWE-bench Pro was built specifically as a contamination-resistant alternative using strong-copyleft-licensed repos (GPL) as a legal deterrent to training-data inclusion. Top models on Pro cluster in the low-to-mid 20s versus 70%+ on Verified. Models are 3–6× more accurate at localizing bug locations on Verified than on held-out or decontaminated sets, with reported contamination rates of 8–10%. OpenAI's own internal audit (cited in Morph's analysis) found all frontier models contaminated on Verified and 59.4% of hard tasks with flawed tests — the reported conclusion being that OpenAI stopped reporting Verified scores.[^23]

Hamel Husain's position on evals — the single most influential working-operator position in the field through 2024–2025 — is not "SWE-bench is bad" but something sharper: *general-purpose benchmarks tell you almost nothing about whether a tool will work in your codebase, and the hours you spend arguing over leaderboard deltas are hours not spent building the domain-specific eval that actually predicts your production performance.*[^24] In his coding-agents eval piece he frames eval-building as the hard skill; the leaderboard is a rough prior at best.

**Operator synthesis.** Treat SWE-bench Verified numbers as a coarse filter — "is this tool in the top tier?" — and nothing more. Do not use a 1–2 percentage point delta as a tie-breaker. The decision-weight should be on your own eval on your own code. We will build one this week.

## Layer 5 — When each tool wins, with specific evidence

Four task shapes, seven tools, one honest ranking per shape.

**Task shape 1: scaffolding a new app from a brief.** *Replit Agent 4 > Cursor Agent mode > Claude Code > rest.* Replit wins because the VM sandbox means agent aggression is cheap — if the scaffold goes wrong you burn it down. The AIMultiple 2025 benchmark had Replit Agent producing a Todo app in ~5 minutes versus Windsurf's ~20, though both had quality issues on first-pass.[^13] Cursor Agent is a close second if you want the code local. Claude Code works but its default permission friction makes scaffolding slower than it needs to be — worth turning on auto-accept for greenfield sessions.

**Task shape 2: repo-aware refactor across 10+ files.** *Claude Code > Windsurf Cascade > Cursor Agent > rest.* Claude Code's subagents let you split "find all callers" from "rewrite the function" from "update the tests" into isolated contexts, each with its own MEMORY.md, with a parent loop reassembling results.[^3] Windsurf Cascade's step-by-step planning is the second-best explicit-planning UX in the set. Cursor Agent handles this well but the IDE coupling makes headless runs awkward.

**Task shape 3: hunt a production bug reported in a ticket.** *Claude Code (with hooks enforcing test-run-before-commit) > Cline Plan/Act > Aider > rest.* Claude Code's combination of adaptive thinking, Grep/Glob, and subagents maps cleanly onto "reproduce, isolate, fix, regress-test." Cline's Plan/Act is the right prior when you don't trust yourself to catch a wrong-turn plan (the approval gate saves you). Aider shines when the bug is local and you want every step to be a reviewable commit.

**Task shape 4: long-horizon feature build (a week or more).** *Claude Code (Opus 4.6 with agent teams) > Codex CLI > Cursor Agent > rest.* Opus 4.6's explicit optimization for "sustained agentic tasks" and its context compaction (automatic summarization during long-running tasks) are built for this shape.[^1] Codex CLI with a thoughtful MCP setup is competitive, at the cost of building your own memory layer. Cursor is workable but the credit-metering risk goes up the longer the session runs.[^17]

These rankings are informed priors, not hard rules. Your actual ranking depends on your codebase's language mix, test coverage, and repo size. Which is why the experiment in Layer 6 is the one you actually have to run.

## Layer 6 — The experiment: a real head-to-head on a real bug

This is the work that makes the rest of the lesson concrete. You will not conclude this week with a defensible tool choice unless you run it.

**Setup (15 min).** Pick a real bug. Options in order of preference:
1. A real ticket in a repo you own.
2. A SWE-bench Lite instance (smaller than Verified, faster to run): `sympy/sympy-20322` (a constant-folding edge case) is a reasonable mid-difficulty choice; `django/django-11099` is a good easier option. You can fetch any SWE-bench Lite instance from the SWE-bench GitHub.
3. A bug you planted yourself (off-by-one, null-check omission, wrong-boundary). Only use this if the first two are unavailable — you'll be biased about the fix.

**Rig (30 min).** You will run the same bug through two tools and measure three things. Tool A = Claude Code. Tool B = one of Cursor Agent, Codex CLI, or Aider — whichever you have set up.

Direct Claude Code, verbatim, with a prompt like:

> "Here is the bug report. Do not read more than necessary. Read the failing test first, then the implicated source. Propose a fix as a diff. Run the test. If it passes, commit. Do not touch files unrelated to the fix. Report back: tool-calls used, wall-time, and a one-paragraph summary."

For Cursor Agent, use Agent mode, paste the same prompt, accept the plan, let it run. For Codex CLI, run `codex` in the repo and paste the prompt. For Aider, `/add` the implicated files and paste the prompt.

**Measurements.**
1. *Tool-call count.* Claude Code's session transcript logs every tool call; Codex CLI's does too; Cursor surfaces them in the Agent panel; Aider reports per-turn. Count them.
2. *Wall-time.* Stopwatch from first prompt submission to successful test run. Exclude your own approval latency — what you want is the model-plus-tool-loop time.
3. *Diff quality.* Show the diff to a reviewer (a colleague, or a second Claude.ai session acting as code reviewer). Grade on: *minimal?* (no drive-by changes), *correct?* (test passes on the target and doesn't regress), *defensible?* (you'd accept this PR from a junior).

**What you're looking for.** If Claude Code takes 12 tool calls and 4 minutes and produces a 3-line correct fix, and Cursor Agent takes 28 tool calls and 9 minutes and produces a 15-line fix that refactors two unrelated files — which is a pattern I have seen more than once — Claude Code's loop design won on this shape. If the opposite happens — Cursor finishes in 2 minutes by spotting something Claude Code missed on a slow read — Cursor won on this shape. Either way you learn something your tech-selection memo needs.

**What to record in your Week 0 notes.** For each tool: tool-calls, wall-time, diff-quality grade, and one sentence on what the failure mode (if any) tells you about the loop. Do not extrapolate from one trial. Run three bugs across each tool over Tuesday–Thursday before you commit to a primary for Week 1.

## Common mistakes AI-catalyst leads still make when picking a tool

1. **Picking the tool with the highest SWE-bench number.** You now know why this is wrong in two ways: (a) Verified is contaminated, (b) general-purpose benchmarks don't predict your-codebase performance. Hamel's framing — *"build the eval that matters for your work, use the leaderboard as a coarse prior"* — is the operator move.[^24]

2. **Ignoring token-per-task cost until the bill arrives.** The 4–5× token-efficiency delta between Claude Code and Cursor on the same task compounds to meaningful dollars over a month of heavy use.[^17] If you are billing a client or running on a tight budget, measure this before you commit.

3. **Treating memory as an afterthought.** The CLAUDE.md you refine across a week is a moat. Moving to another tool means translating it. If you anticipate switching — or running more than one tool — keep a canonical `AGENTS.md` at the repo root and let tool-specific files (CLAUDE.md, .cursorrules, CONVENTIONS.md, .clinerules) symlink or copy from it.

4. **Accepting the default permission model without tuning it.** Claude Code's default prompts-every-Bash protects you; it also shreds your flow on greenfield work. Tune `.claude/settings.local.json` allowlist per-repo. Codex CLI's light default is dangerous on production repos; tighten the denylist. The five minutes of setup repay themselves within the first hour.

5. **Running the tool once and declaring a winner.** Sample size one is folklore. Run three tasks per tool with three different shapes (scaffold, refactor, bug-fix). The tool that wins two out of three on your shapes is your default; the others are situational.

6. **Forgetting the lethal trifecta when you connect MCPs.** The moment you attach an MCP that ingests external content (web browse, email, Linear tickets containing untrusted text) *and* your tool has a credential to something sensitive *and* has any outbound channel (PR creation, webhook call, file write to a watched directory) — you have the lethal trifecta Simon Willison has been writing about since 2022. Johann Rehberger's daily reports in August 2025 confirmed live prompt-injection vulnerabilities across ChatGPT, Codex, Claude Code, Cursor, Copilot, Devin, OpenHands, Jules, and Amp. No tool is exempt; defense is architectural.[^25]

7. **Measuring agent quality by watching it work instead of inspecting the diff.** The agent looks impressive. The diff is what ships. When you evaluate tools, disregard the interaction and read the diff.

## Open questions — what's genuinely unsettled as of April 2026

**Q1. Is the IDE-vs-CLI divide collapsing or sharpening?** Collapsing position: Cursor 2.0's agent-first reframing, Claude Code's JetBrains plugin, and the convergence of loop shapes suggest the same underlying loop will be packaged in both form factors and the "IDE versus CLI" question will become cosmetic. Sharpening position: the token-efficiency gap (Claude Code's 4–5× edge) and the headless / CI use-case (where IDE coupling is overhead, not feature) suggest CLI-native tools pull further ahead for operator workflows while IDE-native tools retain the pair-programming market. Both may be right for different users.

**Q2. Will MCP dominate or fragment?** Anthropic proposed MCP; Claude Code, Codex CLI, Cline, Roo Code, Cursor, and Windsurf all support it. If the protocol stays open and the community-MCP base keeps compounding, MCP becomes the UNIX-pipe of agentic coding. If a vendor ships a proprietary tool-use protocol that meaningfully beats MCP on a dimension that matters (streaming? type safety? permissioning?), the market fragments. Worth watching in 2026.

**Q3. Does "agent teams" win, or do single-agent loops stay dominant?** Opus 4.6's agent-teams feature explicitly bets that multi-agent collaboration — planner + implementer + reviewer, each with their own context — beats single-loop work on long-horizon tasks.[^1] Cognition's Devin, the original agent-teams product, has matured through 2025 updates but has not displaced single-agent loops as the default. Whether the 2026 generation of frontier models justifies agent-teams by default is an open empirical question.

## Reviewer lens — named technical disagreements

- **Hamel Husain, on Layer 4's SWE-bench treatment.** I've said *"treat SWE-bench Verified as a coarse filter"* and cited his evals writing. Husain would push harder: the framing *"coarse filter"* still implies the benchmark provides signal. In his *LLM Evals FAQ* and the *Evals Skills for Coding Agents* essay he argues that for anyone choosing a tool for a specific codebase, the leaderboard's predictive power is approximately zero above a baseline of "can write syntactically valid code," and the framing should be *"ignore the benchmark, build the eval."*[^24] My softer framing is a concession to operators who don't yet have time to build their own eval; Husain would call that an excuse.

- **Simon Willison, on Layer 2's MCP and tool-surface discussion.** I've listed MCP support as a straightforward positive feature. Willison — who has been the most consistent voice on agentic-coding security since 2022 — would flag the unpriced risk: *every MCP you attach is a new principal in the agent's trust graph, and most teams attach them with no threat model.*[^12][^25] His 2026 lethal-trifecta framing would read Layer 2 and add: *"the tool-surface axis should carry a security-surface-area column."* Fair pushback. The mitigation is architectural (taint tracking, outbound-HTTP gating, per-tool permissioning) and belongs in a Week 1 security lesson, not this one; I've named the risk and pointed the reader to his writing.

- **Boris Cherny, on the Claude Code teardown.** I've written that Claude Code's subagents, hooks, and MEMORY.md are differentiating strengths. Cherny — who works on Claude Code — would likely agree on the direction and push on the specifics: *how often do you actually use subagents in production?* Most operators don't reach for them until a task is long enough that a single context window starts thrashing, which is a minority of day-to-day work. The lesson implies subagents are a default feature; in practice they're a tool you reach for 10–20% of the time. I'll concede the point: the Layer-5 rankings should have called out when subagents actually pay off (task-shape 2 and 4) more explicitly, rather than implying they're always active.

- **Shreya Shankar / Jason Liu, on Layer 6's experiment design.** I've specified N=1 per tool per bug shape, moving to N=3 by Thursday. Shankar and Liu, who have both written extensively on eval rigor, would argue that N=3 with unknown variance between runs is not a measurement — it's three anecdotes. The honest answer is that the experiment is a *screening* experiment — cheap, fast, directional — not a power-calculated comparison. For a real tool-selection memo you'd want N≥10 per tool per shape with the variance reported. I've asked readers to do the cheap version because nobody has time for the rigorous one in Week 0; we build the rigorous version in Week 6 when we do evals properly.

- **An honest uncertainty.** I've asserted Claude Code uses 4–5× fewer tokens than Cursor for equivalent tasks, citing Morph's comparison study and other third-party reports.[^17] The studies I've cited are small-sample industry comparisons, not peer-reviewed or harness-controlled benchmarks; the number could shift meaningfully on different task shapes and tool configurations. Treat it as *"widely replicated across independent operator reports, directionally robust, not quantitatively precise."*

## Further reading

**Must-read this week:**

- Anthropic. *What's new in Claude 4.6.* Platform docs.[^1]
- Anthropic. *Create custom subagents* and the Claude Code documentation landing page.[^3][^4]
- Morph. *SWE-Bench Pro Leaderboard (2026): Why 46% Beats 81%.* Direct teardown of the contamination problem.[^23]
- Hamel Husain. *LLM Evals: Everything You Need to Know.* And *Evals Skills for Coding Agents.*[^24]

**Recommended (before Week 1 begins):**

- OpenAI. *Unrolling the Codex agent loop.* Read the loop diagram and re-read with Claude Code's loop in mind.[^2]
- Cursor. *Changelog 2.0: New Coding Model and Agent Interface.*[^5]
- Simon Willison. *An AI State of the Union* (Lenny's) and *The lethal trifecta.*[^12]
- Aider. *LLM Leaderboards.* Look at the Polyglot column specifically — it's a more honest coding eval than SWE-bench Verified in 2026.[^20]

**Optional:**

- Scale AI Labs. *SWE-Bench Pro Leaderboard (public dataset).*[^26]
- Cline. *Top 6 Claude Code Alternatives for Agentic Coding Workflows in 2025.* Opinionated teardown from a competitor — useful precisely because of the bias.[^6]

## Citations

[^1]: Anthropic (2026-02-05). *What's new in Claude 4.6.* Platform docs. https://platform.claude.com/docs/en/about-claude/models/whats-new-claude-4-6 — 1M token context in beta, 128K output tokens, four effort levels, agent teams in research preview, context compaction in beta, adaptive thinking. Pricing $5/$25 per million (premium $10/$37.50 above 200K prompts). Release context and "Anthropic releases Opus 4.6 with new 'agent teams'": https://techcrunch.com/2026/02/05/anthropic-releases-opus-4-6-with-new-agent-teams/
[^2]: OpenAI (2025). *Unrolling the Codex agent loop.* https://openai.com/index/unrolling-the-codex-agent-loop/ — request-response cycle using the Responses API, tool-call append-and-resubmit pattern, SSE streaming.
[^3]: Anthropic. *Create custom subagents.* Claude Code Docs. https://code.claude.com/docs/en/sub-agents — subagent isolation, per-subagent tool permissions, MEMORY.md read into system prompt (200-line / 25KB cap).
[^4]: Anthropic. *Claude Code documentation* and hooks reference. https://code.claude.com/docs/ — PreToolUse / PostToolUse / Stop hook events; `.claude/settings.local.json` permission model; see also practitioner teardowns: https://www.penligent.ai/hackinglabs/inside-claude-code-the-architecture-behind-tools-memory-hooks-and-mcp/ and https://alexop.dev/posts/understanding-claude-code-full-stack/
[^5]: Cursor (2025). *Changelog 2.0: New Coding Model and Agent Interface.* https://cursor.com/changelog/2-0 — agent-first reframing, Composer model, multi-file agent mode. See also Cursor's *Best practices for coding with agents*: https://cursor.com/blog/agent-best-practices
[^6]: Cline (2025). *Top 6 Claude Code Alternatives for Agentic Coding Workflows in 2025.* https://cline.bot/blog/top-6-claude-code-alternatives-for-agentic-coding-workflows-in-2025 — Plan/Act architecture, MCP marketplace, positioning versus Claude Code.
[^7]: Roo Code. GitHub repo and docs. https://github.com/RooCodeInc/Roo-Code — multi-mode architecture (Code / Architect / Debug / custom), mode-scoped prompts and tools.
[^8]: Taskade (2026). *Windsurf Review 2026: Cascade AI After Cognition.* https://www.taskade.com/blog/windsurf-review — Cascade planning-first architecture, step-by-step approvals, post-Cognition positioning.
[^9]: Alex Opalic (2025). *Claude Code Customization Guide: CLAUDE.md, Slash Commands, Skills, and Subagents.* https://alexop.dev/posts/claude-code-customization-guide-claudemd-skills-subagents/ — CLAUDE.md tier system (user / project / local), subagent MEMORY.md mechanics.
[^10]: Medium / Gopi (2025). *How to Orchestrate Cursor AI: AGENTS.md, Rules, and Autonomous Agent workflows.* https://medium.com/@gopikrish3004/how-i-made-cursor-autonomous-agents-md-and-the-art-of-ai-instruction-e8bdd7562442 — AGENTS.md layering, path-scoped `.mdc` rules, `.cursorrules` legacy.
[^11]: OpenAI Codex CLI. GitHub and docs. https://github.com/openai/codex and https://developers.openai.com/codex/cli — open-source Rust loop, MCP via `~/.codex/config.toml` and `codex mcp` subcommands, April-2025 launch.
[^12]: Simon Willison (2025-12). *An AI State of the Union* (Lenny's Newsletter podcast summary). https://www.lennysnewsletter.com/p/an-ai-state-of-the-union — November-2025 inflection point claim; canonical tag index for prompt-injection writing: https://simonwillison.net/tags/prompt-injection/ and the lethal trifecta essay: https://simonw.substack.com/p/the-lethal-trifecta-for-ai-agents
[^13]: Replit (2025–2026). *Replit vs Windsurf* product comparison page. https://replit.com/discover/replit-vs-windsurf — Agent 3/4 architecture, VM sandbox, deploy-as-coding-step. AIMultiple benchmark reference (~5 min Replit vs ~20 min Windsurf on Todo app): https://aimultiple.com/ai-code-editor
[^14]: Builder.io (2026). *Claude Code vs Cursor: What to Choose in 2026.* https://www.builder.io/blog/cursor-vs-claude-code — multi-model session switching (GPT-5.3 Codex, Sonnet 4.6, Gemini 3 Pro, Composer).
[^15]: OpenAI (2025-08). *Introducing GPT-5* and *GPT-5 System Card.* https://openai.com/index/introducing-gpt-5/ — 74.9% on SWE-bench Verified (477-task internal subset), 88% on Aider Polyglot at release. System card: https://cdn.openai.com/gpt-5-system-card.pdf
[^16]: Claude pricing and plan explainers. Claude Pricing: https://claude.com/pricing — Pro ($20/mo), Max 5x ($100/mo), Max 20x ($200/mo). API pricing: Opus 4.6 at $5/$25 per million, 1M-context premium at $10/$37.50 above 200K tokens.[^1] Cost-in-practice references: https://www.nxcode.io/resources/news/claude-code-pricing-2026-free-api-costs-max-plan and https://findskill.ai/blog/claude-code-subscription-pricing-guide/ (10-billion-token, $15K-vs-$800 case).
[^17]: Morph (2026). *Aider Uses 4.2x Fewer Tokens Than Claude Code (2026): 3-Tool Benchmark on 47 Files.* https://www.morphllm.com/comparisons/morph-vs-aider-diff — token-efficiency ratios across Claude Code, Cursor, Aider; $7,000-annual-in-a-day Cursor overage case.
[^18]: SWE-bench. *Leaderboards.* https://www.swebench.com/ and Verified-specific view: https://www.swebench.com/verified.html — April-2026 snapshot via third-party aggregators https://www.marc0.dev/en/leaderboard and https://benchlm.ai/benchmarks/sweVerified showing Opus 4.5 / Opus 4.6 / Gemini 3.1 Pro / MiniMax M2.5 / GPT-5.2 clustered 80.0–80.9%.
[^19]: Vellum AI (2025). *GPT-5 Benchmarks.* https://www.vellum.ai/blog/gpt-5-benchmarks — 74.9% SWE-bench Verified, 88% Aider Polyglot, debugging-larger-repos claim.
[^20]: Aider. *LLM Leaderboards.* https://aider.chat/docs/leaderboards/ — Polyglot benchmark (225 Exercism exercises, 6 languages). GPT-5 at 88%; Claude 3.7 Sonnet at 92.9% via Refact.ai agent (Simon Willison's writeup: https://simonwillison.net/2025/Feb/25/aider-polyglot-leaderboard/ and Refact.ai announcement https://refact.ai/blog/2025/refact-ai-agent-claude-3-7-sonnet-ranked-1-aider-polyglot/).
[^21]: BenchLM (2026). *SWE-bench Verified Benchmark 2026: 31 LLM scores.* https://benchlm.ai/benchmarks/sweVerified — April 2026 aggregated snapshot (Claude Mythos Preview 93.9%, GPT-5.3 Codex 85%, Claude Opus 4.5 80.9%). Third-party; reliability varies.
[^22]: Anthropic (2025-09-29). *Introducing Claude Sonnet 4.5.* https://www.anthropic.com/news/claude-sonnet-4-5 — 77.2% SWE-bench Verified at 200K thinking budget, 82.0% with parallel test-time compute. Opus 4.5 release (2025-11-24) at 80.9%: https://www.anthropic.com/news/claude-opus-4-5
[^23]: Morph (2026). *SWE-Bench Pro Leaderboard (2026): Why 46% Beats 81%.* https://www.morphllm.com/swe-bench-pro — contamination rates 8–10% on Verified, 3–6× bug-localization gap, GPL-license deterrent design on Pro, OpenAI's internal audit finding 59.4% of hard tasks with flawed tests.
[^24]: Hamel Husain (2024–2025). *LLM Evals: Everything You Need to Know.* https://hamel.dev/blog/posts/evals-faq/ and *Evals Skills for Coding Agents.* https://hamelhusain.substack.com/p/evals-skills-for-coding-agents — general-purpose benchmarks do not predict production performance; eval-building as the operator skill. Predecessor: *Your AI Product Needs Evals.* https://hamel.dev/blog/posts/evals/
[^25]: Simon Willison (2025). *New prompt injection papers: Agents Rule of Two and The Attacker Moves Second.* https://simonw.substack.com/p/new-prompt-injection-papers-agents and *Prompt injections as far as the eye can see.* https://simonw.substack.com/p/prompt-injections-as-far-as-the-eye — Johann Rehberger's August-2025 daily reports of prompt-injection vulnerabilities across ChatGPT, Codex, Claude Code, Cursor, Copilot, Devin, OpenHands, Google Jules, Amp.
[^26]: Scale AI Labs (2025–2026). *SWE-Bench Pro Leaderboard (Public Dataset).* https://labs.scale.com/leaderboard/swe_bench_pro_public — contamination-resistant benchmark design, 1,865 multi-language tasks across 41 repos, top models in low-to-mid 20s.
[^27]: Cognition (2025-07-14). *Cognition's acquisition of Windsurf.* https://cognition.ai/blog/windsurf — definitive agreement covering Windsurf IP, product, trademark, brand, and remaining team. Context: TechCrunch (2025-07-14) https://techcrunch.com/2025/07/14/cognition-maker-of-the-ai-coding-agent-devin-acquires-windsurf/ covering the 72-hour sequence after Google's $2.4B reverse-acquihire of CEO Varun Mohan and co-founders.
