---
type: lesson
block: block-0-basecamp
week: week-00
day_of_cycle: 3
day_name: wed
session_slug: ai-catalyst-program-onboarding
date_due: 2026-04-22
tags: [claude-code, claude-md, memory, auto-memory, skills, subagents, hooks, settings, agent-architecture, context-engineering, team-workflow]
sources:
  - anthropic-claude-code-memory-docs
  - anthropic-claude-code-skills-docs
  - anthropic-claude-code-subagents-docs
  - anthropic-claude-code-hooks-docs
  - anthropic-agent-skills-engineering
  - claude-code-v2159-release
  - cherny-pragmatic-engineer
  - cherny-x-vanilla-setup
  - willison-claude-code-tag
  - github-issue-23544-disable-auto-memory
  - github-issue-37314-feedback-not-applied
  - tokencentric-config-files-compared
  - promptshelf-cursorrules-vs-claudemd
  - checkpoint-cve-2025-59536-hooks
  - infoq-claude-code-subagents
  - anthropic-claude-code-hooks-guide
  - aaif-linux-foundation
last_verified: 2026-07-17
word_count_target: 6000
---

# CLAUDE.md and the memory architecture — how Claude Code actually remembers, and how to design it for your team

## Why this matters

You are about to build — or you are already building — a team workflow on top of Claude Code. Within three months, your repo is going to accumulate: a project `CLAUDE.md`, a user `~/.claude/CLAUDE.md`, possibly an enterprise policy file, an auto-memory directory under `~/.claude/projects/<slug>/memory/`, one or more custom skills under `.claude/skills/`, subagents under `.claude/agents/`, and hooks in `settings.json`. Each of these is a different memory mechanism with different load timing, different precedence, and a different failure mode.

If you treat them as "a bunch of markdown files Claude sort of reads," you will ship systems that contradict themselves: a `CLAUDE.md` that says *use tabs*, an auto-memory entry from yesterday that says *use 2-space indentation*, a skill whose body says *defer to project conventions* — and Claude Code quietly picking whichever one happens to sit closest in its context window today. Your team will blame "Claude being flaky." The actual bug is a memory architecture you never designed.

By the end of this lesson you will be able to (1) draw the full four-tier `CLAUDE.md` hierarchy plus auto-memory plus skills plus subagents plus hooks from memory, (2) say with confidence *which* of those the harness loads at session start versus on demand versus never, (3) write a one-page memory map for your own repo that tells your team what goes where, and (4) predict the three most common failure modes and the mitigations for each. You will also have run — not read about, run — the empirical probe that lists Claude's currently loaded instructions in a fresh session, which is the one thing that converts this from cargo-cult to operator knowledge.

## Prerequisites

- Claude Code installed (a current v2.1.x; auto-memory shipped in late 2025 and is on by default).[^6]
- A scratch directory on your machine where we can create nested folders without breaking a real project.
- Rough mental model of what a context window is — if you sat through [[01-mon-mental-model-of-llms|Monday's mental model of LLMs]] you have it. The memory architecture is, at bottom, a set of policies for *what goes into the context window and when*. It sits underneath [[06-sat-git-worktrees-for-ai-builders|Saturday's worktree lesson]] too: auto-memory is keyed per git repository and shared across all its worktrees.

This is an architectural lesson. You will direct Claude Code; you will not hand-write Python.

## Layer 1 — CLAUDE.md: the four-tier hierarchy

The single most important mental model: `CLAUDE.md` is a convention, not a data structure. The Claude Code harness reads files from disk at specific paths and inlines them into the system prompt before your first message. That is the whole mechanism. Everything else — precedence, imports, nested loading — is policy layered on top.

There are **four scope tiers** where `CLAUDE.md` can live, plus per-directory *nested* files below them.[^1]

1. **Managed-policy (enterprise).** A single file, installed by IT at an OS-specific path — `/Library/Application Support/ClaudeCode/CLAUDE.md` on macOS, **`C:\Program Files\ClaudeCode\CLAUDE.md`** on Windows, `/etc/claude-code/CLAUDE.md` on Linux/WSL. (The April draft gave the Windows path as `C:\ProgramData\...`; current docs say `C:\Program Files\...`.) It can also be embedded directly via a `claudeMd` key in `managed-settings.json`. This tier is designed for regulated environments and **cannot be excluded** by individual settings. Most individual operators never see it; in a regulated org you will.
2. **User tier — `~/.claude/CLAUDE.md`.** This is *you*: voice, permanent preferences, things true in every repo. "I write in British English." "Never use emojis in committed code unless I explicitly ask." Edit it with `/memory` or your editor — [Simon Willison prefers editing `CLAUDE.md` directly rather than the `#`-prefix shortcut, because the shortcut can produce sloppy phrasing the model then internalizes](https://simonwillison.net/tags/claude-code/).[^9]
3. **Project tier — `./CLAUDE.md` or `./.claude/CLAUDE.md`.** This is *the team*. Build/test commands, architectural invariants, "do not touch `migrations/` directly," domain vocabulary. Boris Cherny — who created Claude Code — describes his team's practice bluntly: *"we keep one shared `CLAUDE.md` checked into git, everyone updates it multiple times a week, and the rule is: when Claude does something wrong, add a line so it doesn't repeat."*[^7] It's the flywheel that makes `CLAUDE.md` compound instead of rot.
4. **Local tier — `./CLAUDE.local.md`.** Personal, project-specific, gitignored preferences: your sandbox URLs, preferred test data. Loads alongside project `CLAUDE.md` and is treated the same way — but only exists in the worktree where you created it (to share across worktrees, import a file from `~/`).[^1]

Below these, **nested** `CLAUDE.md` files (`./packages/api/CLAUDE.md`, etc.) live at any depth for monorepos where subdirectories differ — different languages, test runners, deployment targets. And for large projects, `.claude/rules/` holds topic-specific files that can be **path-scoped** (see Layer 6).

### Load order and merge semantics

Here is where the harness design matters, and where most operators have a wrong mental model. There are two distinct behaviours:

- **Files at or above the working directory load in full at session launch.** That means: enterprise policy, user `CLAUDE.md`, every `CLAUDE.md` in the chain from filesystem root down to your current directory — all of them, concatenated into the session system prompt before you type a single token.[^1]
- **Files in subdirectories load on demand.** A `CLAUDE.md` inside `./packages/api/` is *not* in your context at session start. It only gets pulled in when Claude actually reads a file under `./packages/api/` — at which point the harness detects the subdirectory `CLAUDE.md` and inlines it.[^1]

Load order runs broadest-scope-first, most-specific-last: managed policy, then user, then every `CLAUDE.md`/`CLAUDE.local.md` from filesystem root down to your cwd (project instructions therefore appear in context *after* user instructions, and `CLAUDE.local.md` is appended after `CLAUDE.md` within each directory).[^1] When rules conflict, the effect is roughly **most-specific-wins** — the docs are blunt that "if two rules contradict each other, Claude may pick one arbitrarily," so this is a tendency from load order and salience, not a hard symbolic priority. Caveat: managed-policy files are *designed* to be non-overridable, but the real enforcement of a compliance rule ("never exfiltrate to a non-allowlisted domain") is in managed `settings.json` (`permissions.deny`, `sandbox.enabled`), enforced by the client regardless of what Claude decides — not in `CLAUDE.md`, which only shapes behavior.

### Imports via `@path/to/file`

A `CLAUDE.md` can reference another file using `@path/to/import` — e.g. `@docs/api-conventions.md` or `@../shared-rules.md`. Imported files are expanded and loaded into context at launch alongside the `CLAUDE.md` that references them.[^1] This is how you keep a small, readable `CLAUDE.md` while keeping detailed specs in separate files. (Note: `@`-imports help *organization*, not context budget — the imported files still load at launch and consume tokens.)

Three operator-level facts the current docs make explicit:[^1]

- **Imports recurse, to a maximum depth of four hops.** If `CLAUDE.md` imports `style.md` and `style.md` imports another file, that chain *is* followed — up to four levels deep. (The April draft claimed imports "don't traverse; one level is reliable, two is not guaranteed." That was wrong even then and is contradicted by current docs.)
- **Imports resolve relative to the file that contains them**, not the working directory. An `@../config.md` inside a nested `CLAUDE.md` points somewhere different from the same line in the root `CLAUDE.md`.
- **Import parsing skips Markdown code spans and fenced blocks**, and the first time a project uses *external* imports Claude Code shows a one-time approval dialog. To mention a path without importing it, wrap it in backticks: `` `@README` `` stays literal; `@README` outside backticks imports.

### Quantitative rigor — how big is too big?

Every token in loaded `CLAUDE.md` files is a token *not* available for your actual work. The current defaults (Sonnet 5, Opus 4.8) ship with 1M-token context windows — but a bigger window is not a licence to bloat, because `MEMORY.md` is capped at 200 lines / 25 KB, adherence drops on long `CLAUDE.md` files (the docs target under 200 lines each), and the new tokenizer means the *same* instructions cost ~30% more tokens than they did on Sonnet 4.6. A team with a 30K-token bloated `CLAUDE.md` + user file + two nested files is burning standing-instruction budget on every session — and compaction hits sooner. Measurable consequences:

- Longer sessions compact earlier — the harness summarises older turns to make room once you approach ~80% fill, and compaction is lossy.
- Tool-heavy sessions (many Bash/Read results) hit the ceiling faster, because tool output and your memory files share the same budget.

Rough operational ceiling most teams converge on: **project `CLAUDE.md` under 2,000 words, user `CLAUDE.md` under 800 words**. Anything bigger wants to be a skill or an imported doc, not a standing instruction.

## Layer 2 — Auto-memory: the second memory system

In late 2025, Anthropic shipped a second, parallel memory system — auto-memory — in Claude Code.[^6] It is not a replacement for `CLAUDE.md`; the two coexist and serve different purposes. `CLAUDE.md` is what *you* write; auto-memory is what *Claude* writes for itself, saving notes about build commands, debugging insights, and preferences it discovers as it works. Conflating them is the single most common mistake operators make in 2026.

### Where it lives

Auto-memory files live under `~/.claude/projects/<project>/memory/`. Crucially, `<project>` is **derived from the git repository, so all worktrees and subdirectories within the same repo share one auto-memory directory** — a fact that matters the moment you start running parallel worktrees (Saturday). Outside a git repo, the project root is used. You can relocate it with `autoMemoryDirectory` in settings.[^2] The directory contains:

- `MEMORY.md` — the **index**, not the content. The first 200 lines or 25 KB (whichever hits first) are auto-loaded at session start; content beyond that threshold is dropped on load, so Claude Code nudges (and eventually errors) to keep the index short.[^2]
- Topic files — e.g. `debugging.md`, `api-conventions.md`, `patterns.md`. These are *not* auto-loaded. They sit on disk until `MEMORY.md` references them and the model reads them on demand.

This distinction — *index auto-loads, topic files load on demand* — is the design decision that makes auto-memory scalable: you can accumulate hundreds of kilobytes without bloating every session.

### What lands in auto-memory

There is **no prefix convention** in the current docs (the April draft claimed a `user_`/`feedback_`/`project_`/`reference_` scheme attributed to the docs; the docs describe plainly named topic files like `debugging.md` instead — the scheme was overclaimed). What the docs *do* specify is the kind of content Claude saves for itself: build commands, debugging insights, architecture notes, code-style preferences, and workflow habits it would otherwise re-derive. Claude doesn't save every session — it decides what's worth remembering based on whether it would help a future conversation. The useful operator taxonomy to keep in your head is still: facts about *you*, corrections you gave, current project *state*, and durable *references* — just don't expect filename prefixes to enforce it.

### How auto-memory differs from CLAUDE.md

| Dimension | `CLAUDE.md` | Auto-memory |
|---|---|---|
| Authoring | Human, explicitly | Harness writes, sometimes with consent |
| Scope | Per-repo (project) + user-global | Per-project (keyed by cwd hash) |
| Load behaviour | Full file into context at launch | Index only; topics on demand |
| Version control | Should be committed (project tier) | Local, not in git |
| Updates | You commit a change | Harness appends during sessions |
| Failure mode | Stale because no-one updated it | Stale because the harness over-wrote it |

Auto-memory is where *ephemeral-but-recurrent* knowledge lives: what we decided last Tuesday, what the user's current side project is, which dev database we're pointed at this week. `CLAUDE.md` is where *durable team conventions* live. Mixing them — putting conventions in auto-memory or session state in `CLAUDE.md` — is the failure mode we keep seeing.

### When the harness auto-loads vs requires explicit recall

The harness loads `MEMORY.md` at session start. Other files in `memory/` are *not* loaded. You — or the model, under instruction — must trigger their load. In practice this happens three ways:

1. The model sees a reference in `MEMORY.md` like `[User profile](user_profile.md) — 20+yr creative director, AI-native builder`, decides the context is relevant, and reads the file via Bash/Read.
2. You explicitly say *"read `memory/feedback_commit_style.md` before writing the commit."*
3. A skill or subagent programmatically loads it.

The consequence: your `MEMORY.md` needs to be a **useful table of contents**, not a dump. Each entry should tell the model — in one line — whether the referenced file is worth loading for the current task. Our working copy uses entries like `- [Content standards](feedback_content_standards.md) — every citation web-verified, reviewer lens, quality gate before bulk generation` — half a link, half a teaser, so the model can decide to open it without loading it first.

## Layer 3 — Skills as procedural memory

Skills, which Anthropic formalised in late 2025, are a third memory mechanism — distinct from both `CLAUDE.md` and auto-memory.[^3][^5] They are not "a bigger memory file." They are a different thing with a different load policy: **procedural memory, lazily loaded, invoked on demand.**

### Anatomy of a skill

A skill lives under `.claude/skills/<skill-name>/SKILL.md` (project) or `~/.claude/skills/<skill-name>/SKILL.md` (user). The file has YAML frontmatter and a markdown body:[^3]

```yaml
---
name: release-notes
description: Generate release notes from git log since the last tag. Use when the user asks for release notes, changelog entries, or "what changed since vX.Y".
allowed-tools: [Bash, Read, Write]
---
```

Followed by the procedure — the checklist, the steps, the output template, the pitfalls to avoid. Anthropic's skill authoring guide recommends keeping the `SKILL.md` body under 500 lines and splitting longer procedures into referenced detail files that load only when needed.[^5] The design pattern they call *progressive disclosure*: the skill entry is cheap (a description the model scans to decide whether to activate); the procedure is loaded when activated; the deep detail files are loaded only if the procedure actually references them.

### When skills override vs supplement CLAUDE.md

Skills and `CLAUDE.md` answer different questions:

- `CLAUDE.md` answers *"what are the standing rules for how this repo / this user operates?"*
- A skill answers *"how do I perform this specific procedure, start to finish, without forgetting a step?"*

A well-designed memory architecture uses `CLAUDE.md` for invariants (*"commits follow conventional commits"*) and skills for procedures (*"the release-notes procedure: parse conventional commits since last tag, group by type, produce markdown with an upgrade-notes section"*). When a skill and `CLAUDE.md` conflict — say, a skill says *"skip test run"* and `CLAUDE.md` says *"always run tests before committing"* — in the current harness, the active skill tends to win in the immediate context because it's loaded with higher salience, but there is no hard priority rule. Don't rely on it. Design so they don't conflict in the first place: skills should explicitly defer to project conventions (*"run tests per project conventions before finalising"*) rather than re-specifying them.

### Progressive disclosure — the design motivation

The reason skills exist as a separate mechanism: you cannot put every procedure your team uses into `CLAUDE.md` without exploding the context window. A 40-skill team, 400 lines per skill, would be 16,000 lines loaded at session start if they lived in `CLAUDE.md`. Skills let you have 40 procedures available, each inexpensive until invoked. Anthropic's engineering blog describes this as *"the contradiction between capability expansion and context cost."*[^5] Skills are the resolution.

## Layer 4 — Subagents as a memory mechanism

This is the mechanism operators most often miss: **subagents are a memory design tool, not just a parallelism tool.**[^4][^15]

When you delegate to a subagent (via the `Task`/`Agent` tool), the subagent runs in a fresh conversation. Everything it does — reading 50 files, running 10 searches, trying three failed approaches — stays in its context, not yours. When it finishes, only its final message returns to the parent conversation.[^4][^15]

Think of this as **context GC**. Instead of your main session accumulating the debris of every exploration, you spin up a subagent to do the exploration, and you get back a summary. The cost: an extra LLM call and the loss of the tool history. The benefit: your main context stays lean.

Use subagents deliberately as memory:

- "Dispatch a subagent to read these 20 files and summarise the auth patterns" — summary returns, 20 files' worth of context does not.
- "Dispatch a subagent to run the test suite and report failures by file" — tool output stays in the subagent.
- "Dispatch a subagent to do the research and come back with a markdown plan" — 6 WebSearches plus their result pages stay in the subagent.

The failure mode: subagents can't commit when the harness permission model restricts Bash to an allowlist that excludes `git commit` (the default for projects that haven't explicitly approved the command in `.claude/settings.local.json`), can't always inherit full permissions, and their lost context *was* sometimes useful. Don't reflexively subagent everything; subagent when the exploration would otherwise blow the budget.

## Layer 5 — Hooks and settings.json as behaviour memory

The fifth memory layer isn't a memory layer at all — it's the harness's behaviour rules, not the model's. `settings.json` (and its two siblings `settings.local.json`, the gitignored local override, and user-level `~/.claude/settings.json`) configure hooks, permissions, and environment for Claude Code itself.[^8]

### Why this counts as memory

Everything in `CLAUDE.md`, auto-memory, and skills is **suggestion**: text the model reads and may or may not follow. A line in `CLAUDE.md` that says *"always run tests before committing"* depends on the model actually doing that. A hook in `settings.json` that runs `npm test` on every `PostToolUse` after a `Write` to `src/**` happens whether the model wants it to or not. The harness runs it.

Hooks are therefore **enforcement memory**: the rules you can't trust the model to remember, implemented as deterministic code. As of mid-2026 Claude Code documents roughly **30 lifecycle events** — including `SessionStart`, `PreToolUse`, `PostToolUse`, `SubagentStart`/`SubagentStop`, `WorktreeCreate`/`WorktreeRemove`, `PreCompact`/`PostCompact`, and `InstructionsLoaded` (which fires when CLAUDE.md or `.claude/rules/*.md` load — useful for debugging exactly what's in context) — with five handler types: `command`, `http`, `mcp_tool`, `prompt`, and `agent`.[^8]

Common uses:

- **Format-on-save** — `prettier --write` after every `Write`.
- **Deny-list** — block Bash tool invocations that match `rm -rf` patterns.
- **Inject context** — a `SessionStart` hook that runs `git log -5` and pipes into the session.
- **Test gate** — a `PreToolUse` hook on `git commit` that runs the test suite and blocks on failure via exit code 2.

The design rule: *if a rule matters enough that you'd be angry if Claude ignored it once, make it a hook, not a `CLAUDE.md` line.*

### The hooks security surface

Hooks are arbitrary shell commands run on the operator's machine. That is exactly as dangerous as it sounds. Check Point Research disclosed **CVE-2025-59536** (CVSS 8.7): the mechanism was a **startup trust-dialog bypass** — repository-controlled configuration (hooks, MCP servers, env) could be tricked into executing *before* the user accepted the startup trust dialog, so simply opening a malicious repo could run arbitrary shell commands and exfiltrate API keys. Anthropic patched it in **Claude Code v1.0.111**.[^14] The broader lesson stands: **never open an untrusted repo, or accept its `settings.json` / `settings.local.json`, without review**, and review hook definitions in PRs the way you'd review a GitHub Action. A hook is a `curl | bash` running under your user on your machine.

## Layer 6 — The live controversy: converging spec or divergent designs?

Step back from Claude Code for a moment. The same design problem — *how do we give a coding agent persistent project-aware instructions* — exists in Cursor (`.cursorrules` / `Project Rules`), Aider (via `CONVENTIONS.md` or now `AGENTS.md`), GitHub Copilot (`copilot-instructions.md`), and every other agent shipping in 2026. There is a real, ongoing disagreement in the community about whether these formats should converge.

### Position A — "one spec to rule them all"

In mid-2025, OpenAI, Google, Cursor and others published `AGENTS.md` as a proposed cross-tool standard. On December 9, 2025 it was formally donated (with MCP and Block's goose) to the Linux Foundation's new **Agentic AI Foundation**, whose founding members include AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, and OpenAI — and by early 2026 AGENTS.md was adopted by 60,000+ repos and read natively by Codex, Cursor, Copilot, Devin, Gemini CLI, and others.[^12] The argument: *your team uses multiple agents, contributors open the repo in whatever tool they prefer, and having the same standing instructions live in five separate files is ridiculous. One file, any agent.* Proponents analogise to `README.md` — a de-facto standard that won on gravity, not technical superiority. Claude Code itself reads `CLAUDE.md`, not `AGENTS.md`, but the docs recommend a one-line `@AGENTS.md` import (or a symlink) so both tools read the same instructions.[^1]

### Position B — "memory is structural to the agent loop"

Anthropic's design rationale, visible in the `CLAUDE.md` hierarchy plus auto-memory plus skills plus subagents plus hooks, is that memory architecture is *not a thin file — it's a system that encodes how the agent loop uses context*. A `CLAUDE.md` is loaded at a specific time in a specific way with specific precedence and import semantics, because those choices interact with Claude Code's particular harness. An `AGENTS.md` that must work for Cursor, Aider (a much smaller context model), and Claude Code (skills + auto-memory + hooks) tends toward a lowest-common-denominator file rather than any one agent's full expressive power. (Note the moving target: the glob-based rule scoping Cursor pioneered now *does* have a clean Claude Code analogue — `.claude/rules/` files with a `paths:` frontmatter field, covered in Layer 7. The April draft claimed it had no analogue; that's no longer true, which is itself evidence of the convergence Position A predicts.)[^11]

### My read

Both are right about different things. You will probably end up running both:

- `AGENTS.md` (or a symlink `AGENTS.md -> CLAUDE.md`, or a short `AGENTS.md` that imports the shared rules) as the **portable, cross-tool baseline** — the 80% of conventions that any agent tool can use.
- `CLAUDE.md` as the **Claude-Code-specific expressive layer** — things the four-tier hierarchy, skills, subagents, or hooks lets you do that a flat file can't.

Watch this space through 2026. If `AGENTS.md` hits the `README.md` escape velocity, Anthropic will likely ship first-class support and treat `CLAUDE.md` as their extension. If the tool-specific mechanisms prove too valuable to flatten, `AGENTS.md` settles in as a polite shared veneer over tool-specific primaries. Either way, in April 2026, bet on `CLAUDE.md` for the Claude-Code-native affordances and keep an `AGENTS.md` stub for portability.

## Layer 7 — Design recipes

Memory architecture collapses to five questions. Here's where each kind of knowledge goes, with a test you can apply.

### What goes in user CLAUDE.md (`~/.claude/CLAUDE.md`)

**Test:** *Is this true about me across every repo I will ever open, for the foreseeable future?*

Yes → user `CLAUDE.md`. Examples: voice ("I write concisely, in British English"), permanent bans ("no emojis in committed code unless I say so"), experience level ("senior; skip Python basics"), default commit style, default communication tone.

If it's true only in one repo, it's not user tier. Move it.

### What goes in project CLAUDE.md (`./CLAUDE.md`, committed)

**Test:** *If a new team member opens this repo in Claude Code tomorrow and doesn't know any tribal knowledge, what's the one file I want them and Claude to read first?*

Yes → project `CLAUDE.md`. Examples: build / test / lint commands with exact invocations; architecture invariants ("auth lives in `services/auth/`; never reimplement"); list of do-not-touch files ("`migrations/*` — generated, don't hand-edit"); domain vocabulary ("in this codebase 'member' means paying customer, 'user' means anyone with a login"); branch and commit conventions.

Boris Cherny's operating rule: *when Claude does something wrong in your repo, add a line so it doesn't repeat.*[^7] That's the update loop. Most teams who report `CLAUDE.md` "working" have that loop; most who report it "failing" don't.

### What goes in memory/ (auto-memory)

**Test:** *Is this ephemeral project state — true now, may change in two weeks?*

Yes → auto-memory. Examples: "currently working on billing migration, phase 2 of 4"; "user is a 20-year creative director, not a coder"; "this week we decided to defer feature X to next quarter"; "reference URLs already verified for topic Y — skip re-research."

The tell: if updating this would generate a diff you'd commit, it belongs in `CLAUDE.md`, not auto-memory. Auto-memory is for things you wouldn't bother writing down but do want the model to remember next session.

### What goes in skills (`~/.claude/skills/` or `.claude/skills/`)

**Test:** *Is this a procedure with steps, triggers, and a well-defined output?*

Yes → skill. Examples: "generate release notes," "triage a flaky test," "write a PR description from a diff," "run a security review before deploy," "handoff meeting-notes format." Each gets a `SKILL.md` whose frontmatter `description` field is the trigger the model uses to decide whether to invoke.

Anti-pattern: a skill that's just a rule, not a procedure. If it doesn't have steps, it's a `CLAUDE.md` line, not a skill.

### What goes in docs (human-facing)

**Test:** *Is this primarily for a human to read and understand, or primarily for the agent to follow?*

Human → `docs/`, `README.md`, ADRs. Agent → `CLAUDE.md` / skills. If both, write it in `docs/` and `@`-import it into `CLAUDE.md`. Avoid docs-with-commentary where a human doc is written *as if* for an agent; you end up optimising for neither audience.

## Layer 8 — Failure modes and mitigations

Four ways memory architecture breaks in production. All four are in active GitHub issues in 2026.

### 1. Stale memories

The simplest failure. Someone added a `CLAUDE.md` line nine months ago ("we use Alembic for migrations"), the team migrated to Prisma six months ago, nobody updated the file. Claude obediently writes Alembic migrations for a week until someone notices.

**Mitigation:** quarterly `CLAUDE.md` review as part of team ops. Or — better — a `SessionStart` hook that prints the last-modified date of `CLAUDE.md`, so every session starts with a visible staleness signal.

### 2. Contradictory rules between tiers

User `CLAUDE.md` says *"always use tabs."* Project `CLAUDE.md` says *"2-space indentation (Prettier enforced)."* Auto-memory added *"user prefers tabs"* last Tuesday. Skill says *"follow project style."* What does Claude do? Probably whatever is loaded most recently or most saliently. Non-deterministic. And your formatter will fight the model.

**Mitigation:** write rules so they don't collide across tiers. User-tier rules should be about *you as an operator* (voice, communication style, learning level); project-tier rules should be about *the codebase* (indentation, build, structure). If a project rule contradicts a user preference, the project wins by design — your personal tab preference doesn't override a team-wide 2-space convention. Write user `CLAUDE.md` as if it will be overridden; write project `CLAUDE.md` as if it is law.

### 3. Context-window blow-up from too many loaded CLAUDE.md files

A monorepo with 12 packages, each with its own `CLAUDE.md`, plus a root `CLAUDE.md`, plus user, plus auto-memory, plus three active skills — you've burned 20K+ tokens before your first message. Compaction hits early; your agent feels "forgetful" two hours into the session.

**Mitigation:** audit with the empirical probe in Layer 9. Consolidate — one root `CLAUDE.md` with `@`-imports to package-level files that only load when relevant — rather than eagerly loading everything.

### 4. Auto-memory drift over long projects

The failure mode multiple GitHub issues in 2026 flagged hardest.[^10][^16] Auto-memory accumulates entries across sessions. Some are correct. Some are corrections of the corrections. Some were correct last month and are wrong now. Older versions did not reconcile contradictions well — you could end up with a `MEMORY.md` listing "user prefers tabs" *and* "user prefers spaces" *and* "user prefers tabs again." Issue #37314 documents exactly this: *"Claude repeatedly fails to apply its own memory/feedback — same mistakes recur across sessions."*[^16] Issue #23544 was the feature request to disable auto-memory entirely.[^10] That request has since been fully answered: current docs support a `/memory` toggle, `autoMemoryEnabled: false` in settings, and a `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1` environment variable.[^2] Newer versions also actively guard the index against bloat, warning (and eventually erroring) when `MEMORY.md` nears the 200-line / 25 KB read limit.

**Mitigation:** periodic pruning — treat `memory/` like a file the model wrote that needs a human editor once a month — or, for teams that prefer `CLAUDE.md` as the single source of truth, turn auto-memory off outright via `autoMemoryEnabled: false` (a fully supported switch now, not the workaround it was in early 2026).

### The controversy in one sentence

Anthropic's positioning: auto-memory is essential infrastructure for agents that learn across sessions.[^2] A non-trivial slice of users in the GitHub issue tracker argue it's too opinionated for teams that already have disciplined `CLAUDE.md` hygiene, and the drift costs outweigh the "learning" benefits until the harness ships real contradiction resolution.[^10][^16] There is no "correct" answer yet; pick the tradeoff that fits your team's discipline.

## Layer 9 — Composite scenario: the memory audit

*This is an illustrative composite, not a real named engagement — it stitches together the failure modes that recur across the GitHub issue threads and practitioner writeups cited in this lesson. Treat the numbers as representative, not reported.*

Picture a mid-sized B2B SaaS shop running a three-month rollout of Claude Code across a 14-person engineering team. Month one feels magical. By month three, three senior engineers have quietly stopped using it for anything above tab-completion. An audit of the memory architecture would plausibly find:

- One project `CLAUDE.md`, 4,100 words, written nine months earlier, never updated, referring to a deprecated testing framework and two repositories that had been merged.
- Every engineer had a user `CLAUDE.md` averaging 600 words, with no coordination between them — different commit-message conventions, different voice instructions, two engineers who'd written "always use the legacy ORM" because they'd gotten burned once.
- Auto-memory had accumulated ~1,200 entries across projects. Nobody had ever looked at `MEMORY.md` directly.
- Three custom skills, all written by one engineer in week two, five skills overlapping in trigger conditions.
- Zero hooks. Zero `settings.json` enforcement.

Symptoms: "Claude is making up function names again." (It was using the deprecated framework from `CLAUDE.md`.) "Claude ignores our style guide." (The style guide was in `docs/`, not referenced from `CLAUDE.md`.) "Claude contradicts itself across sessions." (Auto-memory drift.)

What we changed, in rough order of impact:

1. **Project `CLAUDE.md` halved in size, rewritten in a morning.** Cut everything stale, imported the live style guide with `@docs/style.md`, listed the five don't-touch files by path.
2. **Added two hooks:** format-on-save (`prettier --write`) and a test gate on `git commit` (exit 2 on failure). Those two hooks eliminated ~60% of the class of complaints that had been framed as "Claude ignores our rules." The rules just weren't enforced rules.
3. **Consolidated skills to three**, each with non-overlapping triggers. Killed the other two.
4. **Turned off auto-memory project-wide** via `autoMemoryEnabled: false` in `settings.json`[^2] because the team's `CLAUDE.md` discipline was higher than auto-memory's contradiction handling. Your team may choose differently.
5. **Instituted the "when Claude does it wrong, add a line" ritual** for project `CLAUDE.md`.[^7] One PR a week, 2–5 lines added, 1–2 lines pruned.

Four weeks later the three senior engineers would plausibly be back on Claude Code, the bug count in commit messages down. The point of the scenario is not *"copy what they did"* — it's that memory architecture is a design problem, not a default. You will have to audit yours, probably twice a year, forever.

## Experiment — verify load order empirically

This is a ten-minute experiment that replaces everything you've just read with your own direct evidence. Do it today.

### Setup

Create a scratch directory and three nested CLAUDE.mds with deliberately conflicting rules. Use Claude Code (not Claude.ai) — this is a harness behaviour test.

```bash
mkdir -p ~/scratch/memory-probe/pkg/api
cd ~/scratch/memory-probe
```

**User-tier file** at `~/.claude/CLAUDE.md` — add (don't replace) this block:

```md
<!-- MEMORY-PROBE-USER -->
When asked to state loaded rules, always include: "user-tier says the user prefers British English and single quotes in JS".
Preferred indentation (user): tabs.
<!-- /MEMORY-PROBE-USER -->
```

**Project-tier file** at `~/scratch/memory-probe/CLAUDE.md`:

```md
When asked to state loaded rules, always include: "project-tier says 2-space indentation and double quotes in JS".
Preferred indentation (project): 2 spaces.
```

**Nested-tier file** at `~/scratch/memory-probe/pkg/api/CLAUDE.md`:

```md
When asked to state loaded rules, always include: "nested-tier (pkg/api) says 4-space indentation and backticks for strings".
Preferred indentation (pkg/api): 4 spaces.
```

### Run

Open two fresh Claude Code sessions — *"fresh"* matters, don't reuse a session:

**Session A — at the project root:**

```bash
cd ~/scratch/memory-probe && claude
```

Ask, verbatim:

> List every instruction and rule currently loaded into your system context that mentions indentation or quote preference. Quote each one exactly and tell me which file it came from.

Then: *"What indentation would you use if I asked you to write a JavaScript file right here in this directory, and why?"*

**Session B — inside the nested directory:**

```bash
cd ~/scratch/memory-probe/pkg/api && claude
```

Ask the same two questions, plus: *"Did reading a file in this directory cause any additional CLAUDE.md to load? Which one? Quote a line from it."*

Then: force a read — *"Read `./something.js`"* (create the file with any content first). Re-ask.

### What to look for

- **Session A should quote user-tier and project-tier rules but not nested.** The nested `CLAUDE.md` is in a subdirectory relative to cwd.
- **Session B should quote user-tier, project-tier, and — depending on harness version — nested from start, or nested only after the first read under `pkg/api/`.** This tells you whether your installed Claude Code version eagerly loads the entire ancestor/descendant chain or lazily loads subdirectory `CLAUDE.md` on first read. Both behaviours exist in shipped versions; you want to know which you have.
- **Conflicts: when you ask "what indentation would you use," the answer should follow most-specific-wins** — nested > project > user.

### Stretch — auto-memory and skills

While you're here:

1. Run `/memory` inside Session A. Scroll. You'll see the currently loaded `MEMORY.md` (if auto-memory is on). Ask Claude: *"List the five most recent auto-memory entries across all topic files. Do any contradict each other?"* This one probe has flushed out genuinely stale entries in every memory system I've audited.
2. Create a skill at `.claude/skills/probe/SKILL.md` with frontmatter `description: "Use when the user says 'run probe'"`. Start a new session, say *"run probe."* Verify the skill body enters context only when triggered.
3. Add a `SessionStart` hook to `.claude/settings.json` that echoes the git HEAD and the last-modified date of `CLAUDE.md`. Start a new session. Confirm the hook output appears before your first prompt.

This sequence — hierarchy probe, auto-memory audit, skill activation, hook verification — is the full-memory-stack diagnostic. Run it when onboarding a new repo and every quarter after.

## Common mistakes experts see

- **Treating `CLAUDE.md` as documentation.** It's not for humans. Humans read `docs/` and `README.md`. If a paragraph is written in "as a team we believe…" prose, move it to `docs/` and `@`-import.
- **Putting procedures in `CLAUDE.md`.** Multi-step procedures belong in skills. `CLAUDE.md` says *that* something is true; skills say *how* to do something.
- **Letting auto-memory accumulate without review.** Treat `memory/` like a file the model wrote. It needs a human editor once a month or it drifts.
- **Relying on `CLAUDE.md` lines to enforce critical rules.** If a rule is "must never happen," it's a hook, not a line. *"Never commit without running tests"* is a `PreToolUse` hook on `git commit`.
- **Monorepo with a `CLAUDE.md` in every package.** You just loaded six files at session start. Consolidate with one root file that `@`-imports per-package specs *only when the agent is working in that package* — via a nested subdirectory `CLAUDE.md`, not a root import.
- **Opening an untrusted repo or accepting its `settings.local.json` without review.** Hooks and project config run arbitrary shell commands under your user. CVE-2025-59536 (the trust-dialog bypass, patched in v1.0.111) was exactly this.[^14]

## Reflection questions

1. If your project `CLAUDE.md` were the *only* onboarding artefact a new team member got, what would they still be missing after a week? That missing thing is either a skill, a hook, or a `docs/` file you need.
2. Look at your own user `CLAUDE.md` (run `cat ~/.claude/CLAUDE.md`). Is every line true across every repo you will ever work in? What isn't?
3. Open your own `memory/` directory with `/memory`. Sort its content mentally into four buckets — facts about you, corrections you gave, current project state, durable references. Which bucket is heaviest, and what does the imbalance tell you? (Remember the docs impose no filename convention; the buckets are yours.)
4. Name one rule currently in your `CLAUDE.md` that should be a hook. What's stopping you from promoting it today?
5. If your team runs both Claude Code and Cursor, where are the conventions *currently* duplicated, and which tier is the source of truth when they drift?
6. For the most expensive failure in your last month of agent use — where Claude did something wrong — which memory tier should have prevented it, and why didn't it?

## My take (reviewer lens)

Five disagreements a serious reviewer would raise with this lesson, with specifics.

**1. The "four-tier hierarchy" framing understates how fuzzy tier 1 is in the real world.** The enterprise-policy tier exists in the docs and is real in large regulated orgs, but 95% of readers here will never touch it. A rigorous treatment would either cite deployment data ("X% of Claude Code installs have a populated enterprise file") or downgrade this to a three-tier hierarchy with a footnote. Calling it "four-tier" in the opener is cleaner pedagogy than truth. — response: keeping four because the moment it applies, it *really* applies, and the lesson is aimed at lead-level operators some of whom work in regulated environments.

**2. The "most-specific-wins" precedence rule is oversold.** The actual precedence is "most-recently-loaded has most recency salience in attention," which approximates most-specific-wins because specific tiers load last, but it is not the same thing. A sufficiently long and emphatic user-tier rule can out-weight a brief project-tier rule, because attention is not a symbolic priority list. The reviewer lens here would be: don't teach "most specific wins" as a hard rule; teach "loading order plus salience, with most-specific-last being the default, but empirically tested per team" — which is exactly what Layer 9's experiment is for.

**3. The skills-vs-CLAUDE.md distinction is cleaner in exposition than in practice.** I wrote *"`CLAUDE.md` answers what, skills answer how"* as if it's a bright line. In practice the line is fuzzy and the harness doesn't enforce it. Teams get by with sloppy boundaries because current models compensate. The reviewer would push: quantify the cost of sloppy boundaries (I haven't; I have qualitative evidence only) before prescribing.

**4. The auto-memory controversy section ducks the hardest question.** The real question isn't *"is auto-memory opinionated?"*; it's *"does automatic, unsupervised accumulation of per-project notes produce a monotonically better agent over 12 months, or does it accumulate more noise than signal without human review?"* I lean toward "more signal with periodic pruning, more noise without" — but I don't have the longitudinal data a proper answer needs, and neither does Anthropic publicly. Someone should.

**5. The experiment is a probe, not a test.** It reveals *a* behaviour on the operator's installed version on the operator's machine. It does not catch regressions when the harness ships. A rigorous operator would turn the experiment into a script they re-run whenever Claude Code updates, and keep a changelog of what's changed in load order and precedence. I stopped short of prescribing that because it's tooling, not curriculum, but it's the next step for anyone taking this seriously.

## Further reading

**Must-read**

- Claude Code: *How Claude remembers your project* — the primary source for everything in Layers 1 and 2. [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).[^1]
- Claude Code docs, auto-memory section — the first-party reference for the second memory system (per-repo directory, `MEMORY.md` index, off switches). [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).[^6]
- Anthropic engineering: *Equipping agents for the real world with Agent Skills* — the design rationale for skills as procedural memory. [anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills).[^5]

**Recommended**

- Gergely Orosz interviewing Boris Cherny — *Building Claude Code with Boris Cherny* — the memory update ritual described as the team uses it. [newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny).[^7]
- Simon Willison's Claude Code tag — ongoing field notes, 2025–2026. [simonwillison.net/tags/claude-code](https://simonwillison.net/tags/claude-code/).[^9]
- Linux Foundation press release on the Agentic AI Foundation — the neutral-governance answer to the "will config formats fragment?" question, with the AGENTS.md cross-tool adoption list. [linuxfoundation.org/press/...agentic-ai-foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation).[^12]
- Check Point Research on CVE-2025-59536 — read this once, then never accept `settings.local.json` from a stranger again. [research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/).[^14]

**Optional**

- GitHub issue #23544 (disable auto-memory) and #37314 (feedback not applied) — read the comment threads; they are the ground truth for the auto-memory controversy.[^10][^16]
- InfoQ: *Claude Code Subagents Enable Modular AI Workflows with Isolated Context* — subagents-as-memory-mechanism from a neutral outlet.[^15]
- AGENTS.md standard site and the Claude Code `.claude/rules/` docs — the cross-tool format and Claude Code's path-scoped-rules analogue. [agents.md](https://agents.md/), [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory).[^11]

## Citations

[^1]: *How Claude remembers your project* — Claude Code Docs, fetched 2026-07-17. [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory). Primary source for the scope tiers (managed/user/project/local + nested), load order (root-down, most-specific-last), `@` imports (recurse to max depth 4, resolve relative to the containing file, skip code spans, external-import approval dialog), `.claude/rules/` path scoping, `CLAUDE.local.md`, `claudeMdExcludes`, managed `claudeMd`, and the Windows managed-policy path `C:\Program Files\ClaudeCode\CLAUDE.md`.

[^2]: *How Claude remembers your project*, auto-memory section — Claude Code Docs, fetched 2026-07-17. [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory). Source for `~/.claude/projects/<project>/memory/` layout keyed per git repo and shared across worktrees, `MEMORY.md` as index (first 200 lines / 25 KB loaded), plainly named topic files (no prefix convention), `autoMemoryDirectory`, and the three off switches (`/memory` toggle, `autoMemoryEnabled: false`, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`).

[^3]: *Extend Claude with skills* — Claude Code Docs. [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills). Primary source for `SKILL.md` frontmatter schema, `description` field semantics, and skill activation. Verified 2026-04-15.

[^4]: *Create custom subagents* — Claude Code Docs. [code.claude.com/docs/en/sub-agents](https://code.claude.com/docs/en/sub-agents). Source for subagent context isolation and summary-return semantics. Verified 2026-04-15.

[^5]: *Equipping agents for the real world with Agent Skills* — Anthropic Engineering. [anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills). Source for progressive disclosure and the 500-line `SKILL.md` body recommendation. Published October 2025.

[^6]: *How Claude remembers your project*, auto-memory section — Claude Code Docs, fetched 2026-07-17. [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory). First-party source for auto-memory (introduced late 2025): Claude writes its own notes, keyed per git repository. (Re-cited from a third-party fan-site "v2.1.59 release notes" page that could not be re-verified in the 2026-07 refresh.)

[^7]: Gergely Orosz, *Building Claude Code with Boris Cherny* — The Pragmatic Engineer, 2025. [newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny](https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny). Source for "when Claude does it wrong, add a line" team ritual, from Boris Cherny directly.

[^8]: *Hooks reference* and *Automate workflows with hooks* — Claude Code Docs, fetched 2026-07-17. [code.claude.com/docs/en/hooks](https://code.claude.com/docs/en/hooks) and [code.claude.com/docs/en/hooks-guide](https://code.claude.com/docs/en/hooks-guide). Source for the ~30 documented lifecycle events (incl. `InstructionsLoaded`, `SubagentStart`/`Stop`, `WorktreeCreate`/`Remove`, `PreCompact`/`PostCompact`), five handler types (`command`/`http`/`mcp_tool`/`prompt`/`agent`), and `settings.json` precedence. (April draft's "21 events, four handler types" superseded.)

[^9]: Simon Willison, tag: claude-code. [simonwillison.net/tags/claude-code](https://simonwillison.net/tags/claude-code/). Ongoing 2025–2026 coverage including Willison's preference for editing `CLAUDE.md` directly over the memory shortcut.

[^10]: GitHub issue anthropics/claude-code #23544, *Need ability to disable auto-memory (MEMORY.md)*. [github.com/anthropics/claude-code/issues/23544](https://github.com/anthropics/claude-code/issues/23544). Feature request thread documenting user demand to disable auto-memory, early 2026.

[^11]: *How Claude remembers your project* (`.claude/rules/` with `paths:` frontmatter glob scoping; the `@AGENTS.md` import pattern) and the AGENTS.md standard site — Claude Code Docs, [code.claude.com/docs/en/memory](https://code.claude.com/docs/en/memory), and [agents.md](https://agents.md/), both fetched 2026-07-17. First-party sources for Claude Code's path-scoped-rules analogue to Cursor's glob rules and for the cross-tool AGENTS.md format. (Replaces three SEO-blog URLs — thepromptshelf.dev, tokencentric.app, deployhq.com — that could not be verified in the 2026-07 refresh.)

[^12]: Linux Foundation (2025-12-09). *Formation of the Agentic AI Foundation (AAIF), anchored by MCP, goose and AGENTS.md.* [linuxfoundation.org/press/...agentic-ai-foundation](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation). Founding platinum members AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI; AGENTS.md adopted by 60,000+ repos, read natively by Codex, Cursor, Copilot, Devin, Gemini CLI. Verified 2026-07-17.

[^13]: TechCrunch (2025-12-09). *OpenAI, Anthropic, and Block join new Linux Foundation effort to standardize the AI agent era.* [techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort](https://techcrunch.com/2025/12/09/openai-anthropic-and-block-join-new-linux-foundation-effort-to-standardize-the-ai-agent-era/). Secondary coverage of the AAIF formation and the cross-tool adoption list. Verified 2026-07-17.

[^14]: Check Point Research, *Caught in the Hook: RCE and API Token Exfiltration Through Claude Code Project Files — CVE-2025-59536*, 2026. [research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536](https://research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536/). CVSS 8.7 startup trust-dialog bypass — project config (hooks/MCP/env) executes before the trust dialog is accepted; patched in Claude Code v1.0.111 (per Tenable/SentinelOne CVE entries). Verified 2026-07-17.

[^15]: *Claude Code Subagents Enable Modular AI Workflows with Isolated Context* — InfoQ, August 2025. [infoq.com/news/2025/08/claude-code-subagents](https://www.infoq.com/news/2025/08/claude-code-subagents/). Third-party coverage of subagent context isolation.

[^16]: GitHub issue anthropics/claude-code #37314, *Claude repeatedly fails to apply its own memory/feedback — same mistakes recur across sessions*. [github.com/anthropics/claude-code/issues/37314](https://github.com/anthropics/claude-code/issues/37314). Documentation of the auto-memory drift / contradiction failure mode, 2026.

_last_verified: 2026-07-17_
