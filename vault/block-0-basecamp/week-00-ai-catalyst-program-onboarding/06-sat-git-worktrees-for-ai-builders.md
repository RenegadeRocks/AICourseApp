---
type: lesson
block: block-0-basecamp
week: week-00
day_of_cycle: 6
day_name: sat
session_slug: ai-catalyst-program-onboarding
date_due: 2026-04-25
tags: [git, worktrees, claude-code, parallel-agents, diff-review, recovery, aider, reflog, agent-isolation, version-control]
sources:
  - pro-git-worktrees
  - claude-code-common-workflows
  - claude-code-v2150-release
  - boris-cherny-setup-thread
  - boris-cherny-worktree-announce
  - aider-git-docs
  - simon-willison-parallel-agents
  - simon-willison-agentic-patterns
  - container-use-dagger
  - claudecode-issue-39886
  - upsun-worktrees-ai
  - damian-galarza-db-isolation
  - git-scm-reflog
  - infoq-cherny-workflow
  - claude-code-dynamic-workflows
last_verified: 2026-07-17
word_count_target: 6000
---

# Git worktrees and diff review as the AI builder's safety net — how to ship AI-directed code without losing work

## Why this matters

Every time you hand a coding task to an agent, you are authorizing a process with write access to your filesystem to make changes you will only partially review. If the agent is right, you ship. If it is wrong, you either notice and revert, or you don't notice and the defect lives in main until a user finds it. The difference between "I ship fast with AI" and "I have been shipping broken code for three weeks and didn't know" is almost entirely determined by two things: how your git history is structured, and how you look at diffs.

This is not a metaphor. Every AI-pro lead I know who has had a genuinely bad incident — silently broken payments, a deleted migration, a regenerated file that overwrote a colleague's unmerged work — can trace the blast radius to one of three failures: (1) the agent ran against a working tree that already had uncommitted changes, (2) the agent did something "and a few other small cleanups," which the operator approved without reading the diff line by line, or (3) multiple agents were writing to the same directory and one stomped on the other's `node_modules` or `.next` cache mid-build.

Your test suite is half a safety net. `git reflog` is the other half. If you remember one sentence from this lesson, make it that one.

By end of session you will be able to:

1. Structure commits so that every agent run is a *recoverable unit* — not a single blob of "the AI did a bunch of stuff."
2. Use `git worktree` to dispatch two or three agents on the same brief in parallel and diff their solutions side-by-side, without any of them contaminating each other's build artifacts.
3. Configure Claude Code's `isolation: "worktree"` agent parameter correctly, and know its three known gotchas before you hit them.
4. Read an agent-generated diff the way a senior reviewer reads one — looking specifically for the four failure modes AI produces far more than humans do.
5. Recover a "the agent deleted my work" situation using `reflog`, `reset --keep`, and targeted cherry-pick, without ever typing `git reset --hard` in panic.

No toy examples. Every pattern in this lesson comes from an incident someone on the Claude Code, Aider, or Cursor communities has written up publicly, usually with a screenshot and a lot of swearing.

## Prerequisites

- Git installed (`git --version` ≥ 2.40; worktree commands are stable since 2.5 but several ergonomic flags were added in 2.40+).
- Claude Code installed (`claude --version` ≥ 2.1.50 for first-class worktree support in the CLI).[^3]
- A scratch repo you are willing to break. Fork anything small. Do not rehearse `reflog` recovery on a repo you care about.
- Familiarity with `git log`, `git diff`, `git checkout`. Everything else in the lesson is built up from first principles.

Referenced lessons: [[03-wed-claude-md-memory-architecture|Wednesday's memory lesson]] (subagents as context isolation, and how auto-memory is shared across a repo's worktrees), and [[02-tue-ai-native-builder-stack|Tuesday's tool-stack lesson]] (Cursor 3.0's native `/worktree` and Claude Code's dynamic workflows both build on the primitive taught here).

## Layer 1 — Why git matters *more* when an agent writes code

Most human developers already commit too rarely. The advice "commit early, commit often" has been the pedagogically correct answer since at least *Pro Git* first edition (2009). Almost no one follows it, because for human coding the downside of under-committing is bounded: you probably remember roughly what you changed in the last hour, and your editor's local history buffer catches the rest.

When an agent writes the code, both of those safety properties silently break.

**You don't remember what changed.** You remember what you *asked for*. Those are different sets. An agent told "add rate limiting to the login endpoint" may well also reformat three unrelated files it happened to open while exploring the codebase, add a dependency you didn't know about, edit your `.env.example`, and silently change a default timeout from 30 seconds to 5 because a linter suggested it. You asked for one thing; the diff contains six. Under-committing means all six land as a single opaque lump in your history.

**Your editor's local history is no longer the ground truth.** VS Code's Local History and JetBrains' Local History are wonderful when *you* are typing. When an agent is issuing filesystem writes through a tool call, those changes may or may not show up as discrete Local History events depending on how quickly they land and how the editor file-watcher debounces. Several Claude Code users have reported, on the GitHub issues tracker, losing work because the agent rewrote a file in a single atomic write that didn't produce an intermediate Local History snapshot.[^10]

The practical consequence: **every serious AI-directed codebase treats the git graph, not the editor, as the source of truth for "what exists right now."** The editor is a view; git is the database. This is already true for human-authored code at a team scale. It becomes true even for a solo builder the moment you let an agent write.

From this one principle, a handful of rules fall out, and most of the rest of this lesson is their mechanical consequences:

- **Never invoke an agent on a dirty working tree.** If `git status` shows uncommitted changes, stash them or commit them *before* the agent starts. Otherwise the agent's edits and yours become indistinguishable in `git diff` afterward, and rollback means losing both.
- **Commit before, and commit after, each agent turn.** The "before" commit is your restore point. The "after" commit is the reviewable unit.
- **Never let an agent write to main directly.** Even for a solo builder. Topic branches are cheap; deleted work is not.
- **Treat the agent's summary of changes as a hypothesis, not a report.** The ground truth is `git diff`. The agent's "I changed X, Y, and Z" prose is often missing one change that turns out to matter.

That last one is the single rule most builders violate. Claude Code, Cursor, Aider, and Codex CLI all end a turn with a natural-language summary of what they did. That summary is generated the same way every other token is generated — by the same model that just did the edits. It is neither a log nor a verified audit trail. Anthropic's own Claude Code documentation is explicit that the end-of-turn summary is for orientation, not accountability.[^2] You still have to read the diff.

## Layer 2 — Commits as a transaction log: two philosophies

There are two mainstream philosophies for how often to commit when an AI is writing code. They come from two different tools and they make different tradeoffs. You should know both, and you should know which one you are choosing.

### Philosophy A: commit-per-iteration (the Aider model)

Paul Gauthier's Aider, open-sourced in July 2023, has had one opinionated default since v0.1: **every single accepted edit from the model produces an auto-generated git commit, with an AI-written message describing the change**.[^6] A single `aider` session on a medium task might produce twenty or forty commits. You can squash them later. The commits are not for sharing; they are for recovery.

The philosophy: the model is a source of low-trust, high-volume proposals. Each proposal either works or doesn't. You want to be able to step back one proposal at a time — `git reset HEAD~1` — without losing earlier proposals. So every proposal gets its own commit. `git reflog` is the memory; commits are the units.

This is mechanically identical to how databases work: each statement is a transaction, committed on success. If a later statement fails, you roll back just that one, not the whole session.

**When this wins.** Exploratory work. Spike branches. Refactors where you genuinely don't know which of ten candidate changes will turn out to be the right one. Any workflow where you might want to `git bisect` over AI-generated commits to find which specific edit broke the tests.

**When this loses.** Code review. A PR with 47 auto-generated commits, each titled "Update user.py" or "Adjust error handling", is illegible. The reviewer cannot build a mental model of what changed at what layer. You have traded future-you's ability to review for past-you's ability to roll back.

### Philosophy B: commit-per-feature (the Cursor / Claude Code default)

Cursor and Claude Code both default to the opposite pattern: **the agent does not commit at all unless you ask it to, and the expectation is that you commit at natural feature boundaries**.[^2] Boris Cherny's personal workflow uses a `/commit-push-pr` slash command invoked at the end of a coherent chunk of work, producing one commit with a crafted message and an immediate PR.[^4][^14]

The philosophy: commits are communication. A commit says *"here is a coherent change that another person should review as a unit."* Forty auto-commits fragment that signal into noise. Better to let the agent iterate inside a working tree — with the agent itself running tests and linters between attempts — and commit once the change is coherent.

**When this wins.** Anything you intend to merge. Team workflows. Anything where the commit log will outlive the session and be read by somebody else. Claude Code's agents are trained to be cautious enough about their own edits that the Aider-style recovery net is less necessary than it is for a less capable model.

**When this loses.** If the agent produces a working-but-wrong result after twenty internal iterations and you can't reconstruct which iteration was the last correct one. You have one "before" commit and one "after" commit; everything in between is gone.

### My take (take a position)

For AI-directed work in 2026, **commit-per-iteration is the right default for solo exploration, commit-per-feature is the right default for merged code**, and the serious builders I know switch between them consciously. If you are in a worktree you'll delete, let Aider-style auto-commit run. If you are in a branch that will become a PR, use Claude Code's default and compose deliberate commits.

The mistake is picking a tool, using its default, and never noticing that the default is a philosophical bet that may not match what you are doing today.

There is a third, more interesting position that several people in the Claude Code community have started publishing: **the agent should commit at every *successful test run*, not every edit and not every feature**. A passing test is the minimal signal that the state is consistent. Commit-per-green-test gives you a git log where every commit is, by construction, a working state of the codebase, so `git bisect` becomes trivially useful. It is arguably the best of both worlds — but it requires a fast, reliable test suite, which is itself a cultural prerequisite most codebases don't have yet. Treat it as a hypothesis worth trialing, not settled practice.

## Layer 3 — Worktrees: mechanics

A git worktree is a second working directory attached to the same repository. The `.git` objects — commits, blobs, trees, refs — live in one place. Worktrees give each of several checked-out branches its own independent filesystem view of the repo, without duplicating the object store on disk.[^1]

The core commands, which you should memorize:

```bash
# Create a new worktree at ../myproject-feature-X on a new branch feature-X
git worktree add ../myproject-feature-X -b feature-X

# Create a worktree on an existing branch
git worktree add ../myproject-bugfix bugfix-123

# List all worktrees attached to the current repo
git worktree list

# Remove a worktree (and its branch if you pass --force + delete the dir)
git worktree remove ../myproject-feature-X

# Clean up stale worktree metadata after manual dir deletion
git worktree prune
```

What you get on disk: two separate directories, one `HEAD` per worktree, independent `node_modules` and build caches per worktree, but a shared commit history. You can `git fetch` once in the main worktree and every other worktree sees the new refs immediately. Disk cost is the size of the working files, not the size of history — which is why upsun, Augment, and the Claude Code team all settled on worktrees as the default parallelization primitive in 2025.[^11]

What you do *not* get: separate environment variables, separate databases, separate ports, separate Docker networks. Two agents running `npm run dev` in two worktrees will fight over port 3000. Two agents running migrations against the same dev database will clobber each other. Worktrees isolate *code*, not *environment*. Galarza's March 2026 post on extending Claude Code worktrees with per-worktree database isolation is the definitive writeup of this limitation and how to work around it with a `docker-compose` overlay per worktree.[^12]

### Real use cases for parallel AI experiments

**Use case 1. Dispatch three agents on the same brief, diff their solutions.** This is the highest-leverage application of worktrees in 2026. You write one brief — *"Add a rate-limiter to the /login endpoint using Redis as the store, with per-IP and per-user limits, including tests"* — and dispatch three parallel Claude Code (or Codex, or a mix) agents, each in its own worktree, each on its own branch. Twenty minutes later you have three candidate diffs. You read all three. You pick the best one, or synthesize across them. The other two worktrees get deleted.

You would not do this for ordinary human coding — the parallel cost is three times the compute — but AI compute is cheap relative to your review time, and three candidate solutions dramatically increases the odds that at least one of them is actually good. Simon Willison has been evangelizing this pattern since mid-2025 and calls it *"embracing the parallel coding agent lifestyle."*[^7]

**Use case 2. Spike a risky refactor while keeping main unblocked.** You want to try renaming a core API. It might work, it might cascade into forty files. In a worktree, the agent can try; if it works, you merge; if it doesn't, you `git worktree remove` and your main development tree never saw the churn.

**Use case 3. Long-running background agents.** An agent doing a multi-hour task (migrating a codebase, generating documentation, backfilling tests) lives in a worktree. You continue working in main. When the agent finishes, you review and merge. Neither you nor the agent has been blocked by the other.

## Layer 4 — Claude Code's `isolation: "worktree"` parameter

Claude Code v2.1.50 (October 2025) added first-class worktree support across CLI, Desktop, and custom agents.[^3] The two entry points:

**CLI flag.** `claude --worktree my-feature` (or `-w`) spawns a Claude Code session in a freshly created worktree at `.claude/worktrees/my-feature`, on a branch of the same name. If you omit the name, Claude generates a random one. Boris Cherny's setup thread confirms the paired `--worktree`/`--tmux` flags for launching parallel sessions in separate panes.[^4] Useful for interactive sessions.

**Agent frontmatter.** In a custom agent definition (`.claude/agents/<name>.md`), adding `isolation: worktree` to the YAML frontmatter causes *every invocation of that agent* to run in its own worktree — the mechanism by which a parent Claude Code session dispatching three subagents gets three parallel worktrees automatically.[^2]

The primitive is no longer Claude-Code-specific: **Cursor 3.0 (April 2026) shipped a native `/worktree` command** that creates an isolated worktree per agent in its Agents Window, and Claude Code's **dynamic workflows** (May 2026) can orchestrate hundreds of parallel subagents, each isolatable, from a single script — which turns the "dispatch two agents in isolated worktrees" experiment below from a manual pattern into a one-line instruction.[^16]

### What it does under the hood

When a Claude Code session or subagent starts with worktree isolation:

1. `git worktree add` is called against the repo root, creating `.claude/worktrees/<agent-name>-<timestamp>/` on a fresh branch.
2. The agent's working directory (the `cwd` its tools operate against) is set to that path.
3. All tool calls — `Read`, `Write`, `Edit`, `Bash` — resolve against that path.
4. On session exit: if the agent made *no* commits and the working tree is clean, the worktree and its branch are deleted automatically. If there are commits or dirty changes, Claude prompts you to keep or remove.[^3]

This is close to ideal default behavior. An aborted agent run leaves no trace; a successful agent run leaves a branch you can review and merge or discard.

### Three gotchas, in order of how often they bite

**Gotcha 1: `node_modules` and lockfile contention.** A fresh worktree does not have a `node_modules/`. The first thing an agent does in a JS project is often `npm install`, which costs 30–120 seconds and may pull slightly different versions than your main worktree has (if your `package-lock.json` has drifted). If you dispatch three parallel agents on a JS project, you pay the install cost three times and may end up with three slightly different resolved dep graphs. Workarounds: pre-create the worktree and run install once; use `pnpm` with a shared store; or use `npm ci` to guarantee lockfile fidelity.

**Gotcha 2: `isolation: "worktree"` silently falls back on misconfiguration.** GitHub issue #39886 (filed March 27, 2026; closed as duplicate) documents a class of failures where the `isolation: worktree` agent parameter is ignored — the agent runs in the main repo working tree instead, with `worktreePath: done` and `worktreeBranch: undefined` — when the worktree is never actually created, causing branch-checkout races when multiple agents share `.git` state.[^10] Verify by logging the agent's `cwd` at start. If it's not inside `.claude/worktrees/`, isolation didn't take and you are about to have two agents writing to the same directory.

**Gotcha 3: Shared build caches and IDE state.** Your `.next/`, `dist/`, `target/`, `.venv/`, and `__pycache__/` are *not* automatically gitignored-per-worktree in most setups. If one agent compiles while another is running, they can corrupt each other's caches. Gitignore entries don't help because the problem isn't git; it's that two processes are writing to logically-distinct-but-physically-adjacent paths. Fix: add the worktree name into your build output path (`NEXT_DIST_DIR=.next-$WORKTREE`), or accept that one cache will rebuild per worktree.

## Layer 5 — The live controversy: worktrees vs. separate clones

Here is the specific disagreement I promised you, between two named voices.

**Position A (worktrees are essential).** The Claude Code team, Simon Willison, the Aider community, and most of the 2025 "parallel coding agents" writeups converged on worktrees as the default. Boris Cherny announced built-in worktree support in Claude Code v2.1.50 with the pitch *"Now, agents can run in parallel without interfering with one another."*[^5] Simon Willison's October 2025 post *Embracing the parallel coding agent lifestyle* treats worktrees as the native unit of parallel work.[^7] The argument: worktrees give filesystem isolation for free, share the object store (cheap disk), share `git fetch` state (cheap network), and let you diff across experiments with a single command.

**Position B (worktrees add overhead for marginal gain; use separate clones).** Here's the contrarian: **Boris Cherny himself**, in his own setup thread, says he runs five parallel Claude Code instances using *five separate `git clone`s of the same repo, not worktrees*.[^4][^14] Each tab is numbered 1–5; each has its own independent clone. His argument, paraphrased from the thread and his Pragmatic Engineer interview: separate clones mean fully independent node_modules, build caches, git config, and — crucially — fully independent reflogs. If Claude Code #3 does something catastrophic, clones #1, #2, #4, #5 are genuinely untouched. Worktrees share the object store; a `git gc --aggressive` initiated by one worktree affects all of them. Clones are slower to create and consume more disk, but cognitively they are *completely isolated*.

**My position, and why.** Cherny's position is the right one for his specific pattern — five long-lived sessions, each on a coherent feature, each owning its own PR. For that pattern, the one-time cost of `git clone` amortizes over hours of work, and the clarity of "tab 3 is its own universe" is worth it.

For the Aider-style, short-lived *"dispatch three agents on the same brief, compare diffs, throw two away"* pattern, worktrees are strictly better. You can't stomach the latency of three `git clone`s when the whole experiment takes 20 minutes. And the upside of having the same object store — you can `git diff worktree-a..worktree-b` trivially to compare the two candidate solutions — is exactly what you want.

So the real answer is: **decide by session length**. Long-lived parallel sessions with independent PR destinies → separate clones. Short-lived parallel experiments with a comparison-and-pick phase → worktrees. Hold that as the operative heuristic for the rest of this lesson.

## Layer 6 — Diff review as primary QA

Tests catch regressions on things you thought to test. Diff review catches everything else. When an agent writes the code, diff review is not optional; it is the last human-in-the-loop checkpoint before you ship. You should be reading diffs the way pilots read pre-flight checklists: slowly, adversarially, and with a fixed list of things you are looking for.

Here is the list. All four categories are AI-specific failure modes — things that happen much more often in AI-generated code than in human-generated code, because they come from how the model works.

### 1. Hallucinated function names and wrong signatures

The model has been trained on millions of APIs. It confidently calls functions that sound right but don't exist in the specific library version you're using, or that existed in v1 but were removed in v2. *Illustrative example (a common, reproducible class of failure):* an agent writes `response = openai.ChatCompletion.create(...)` in a project using the `openai` Python SDK v1.x, where that call has been `openai.chat.completions.create(...)` since November 2023. The code looks right, passes lint, passes type-check (because the return type is `Any`), and fails only at runtime — especially if the test suite mocks the call.

**How to catch in diff review.** For any new function call you don't immediately recognize, grep the codebase for prior usage. If this is the first time the project is calling this function, open the library docs. If the diff adds a new import from a well-known library, double-check the import path against current docs, not training-data memory.

### 2. Silent behavior flips on existing functions

The agent changed the body of a function while preserving its name and signature. Your tests still pass because the tests were happy with either behavior. But the semantics have shifted. *Concrete example:* an agent "simplified" `charge_customer()` in `billing/stripe_adapter.py` by removing a `raise StripeChargeError(...)` inside the `except stripe.error.CardError` branch and replacing it with `log.warning("card declined for %s", customer_id); return None`. Same name, same `Optional[Charge]` return type, every existing unit test passed because the tests only asserted the happy path. Production silently started returning `None` on declined cards for two weeks — meaning the upstream caller treated declined cards as "no charge needed" and provisioned service without payment.

**How to catch.** When reviewing a diff of a function body, ask: *"does this change the set of outputs this function can produce?"* Look specifically for changes to `raise`/`throw`, `return` in error paths, logging levels (silent demotion from `error` to `warning` is suspicious), and any new try/except that wraps previously-raising code.

### 3. Unrelated edits

The agent, while doing what you asked, also reformatted three other files, changed a timeout default, updated a comment to be "clearer," or bumped a dep version because it "noticed it was slightly out of date." None of this was in the brief. Some of it may be improvements; some of it is production-breaking. *Concrete example:* a brief of "add rate-limiting to `POST /login`" produced the intended middleware in `api/middleware/rate_limit.py` but also, in the same commit, changed `HTTP_TIMEOUT = 30` to `HTTP_TIMEOUT = 10` in `api/config/defaults.py` (because the agent "noticed the value seemed high") — a change that broke a slow third-party OAuth callback in staging the next morning.

**How to catch.** Before merging, do `git diff --stat` and look at the file list. If the brief was "add rate-limiting to /login" and the diff touches 9 files including `package.json` and `.env.example`, you need to audit each non-obvious file. `git diff -- path` one file at a time until you are satisfied.

### 4. New dependencies

The agent added a new library to solve a subproblem. Sometimes the library is fine. Sometimes it is unmaintained. Sometimes it pulls in 40 transitive deps. Sometimes it duplicates functionality you already have. *Concrete example:* asked to "parse RFC 3339 timestamps from the webhook payload," an agent added `python-dateutil>=2.8` to `requirements.txt` — even though the codebase already depended on `pendulum`, whose `pendulum.parse()` handles RFC 3339 natively. Two parsing libraries now coexist, a later refactor has to pick one, and a subtle timezone-naive-vs-aware bug appears in tests that round-trip through the "wrong" one.

**How to catch.** `git diff package.json requirements.txt go.mod Cargo.toml` is its own review step. For every new dep, ask: (a) is it maintained (last release < 12 months)? (b) what does it pull in transitively? (c) do we already have something that does this? If you can't answer those in under two minutes, reject the dep and ask the agent for a solution without it.

### The review heuristic in one sentence

Every line in an agent's diff is guilty until proven necessary. Human code gets the benefit of the doubt because you know the human's intent. Agent code does not; the agent does not have intent, only output.

## Layer 7 — Recovery protocols

At some point an agent is going to do something you didn't want, and you are going to need to recover. There are four tools, in order of aggressiveness. Learn all four.

### `git reflog` — the foundation

`git reflog` shows every time `HEAD` moved in this repo for the last 90 days (default), including commits, resets, rebases, checkouts, cherry-picks, and merges.[^13] It is local-only; never pushed; invisible on GitHub. It is also the only log that survives `git reset --hard`.

Walkthrough:

```bash
# Agent just ran `git reset --hard HEAD~5`, wiping your last five commits.
git reflog
# You see entries like:
#   a1b2c3d HEAD@{0}: reset: moving to HEAD~5
#   e4f5g6h HEAD@{1}: commit: Add rate limiter middleware
#   i7j8k9l HEAD@{2}: commit: Add Redis client
#   m0n1o2p HEAD@{3}: commit: Wire up /login rate limit
#   ...

# Recover by moving HEAD back to the pre-reset SHA:
git reset --hard HEAD@{1}
# You are back. The reset is reversed.
```

The SHA is all you need. `git reset --hard <sha>` puts HEAD wherever you want. If you are nervous — and you should be, because `--hard` is itself destructive — use `git reset --keep <sha>` instead: it refuses to run if there are uncommitted local changes that would be overwritten.

### `git stash` — for "save this state before I experiment"

`git stash` saves your working tree and index as a stash entry without committing. `git stash list` shows all stashes. `git stash pop` reapplies the most recent.

The right time to use stash in AI-assisted work: you have uncommitted changes, the agent is about to do something risky, and you don't want to make a "WIP" commit just for a restore point. Stash, run the agent, pop the stash. If the agent succeeded, your stashed changes and the agent's changes merge (possibly with conflicts you resolve). If the agent failed, you `reset --keep` to the pre-agent commit and `stash pop` to restore.

`git stash` entries also show up in reflog, so even a discarded stash is recoverable.

### `git reset --keep` — the safe reset

`git reset --hard` is the go-to "wipe my changes" hammer, and it is responsible for approximately half the "I lost work" posts on r/git. `git reset --keep` does the same thing but aborts if there are uncommitted changes that would be lost. Use `--keep` by default. Use `--hard` only when you are certain — which should be rare.

### `git cherry-pick` and `git rebase -i` — salvaging partial good work

Sometimes the agent's run is 80% good, 20% catastrophic. You don't want to throw it all out and you don't want to merge all of it. Two tools:

- `git cherry-pick <sha>` picks one commit from anywhere and applies it on top of your current branch. Useful if the agent made 10 commits and commits 1, 3, 7 are good.
- `git rebase -i <base>` lets you edit the commit list — drop bad commits, reword messages, squash related commits — before applying them on top of `<base>`.

Caveat: never `rebase -i` a branch someone else has based work on. Rebasing rewrites history; if another human or another agent has commits on top of the old history, their commits get orphaned. Rebase only in topic branches you own.

## Layer 8 — Branching strategies for agent-heavy work

Three patterns, in order of formality:

**1. Short-lived topic branches, agent-runs-per-branch.** Every non-trivial agent task starts with `git checkout -b agent/<task-slug>`. The agent runs, you review, you merge (or delete). Branch lives for minutes to hours. This is the default I recommend and the pattern Claude Code's worktree isolation is designed for. Naming convention: `agent/<topic>` or `claude/<topic>` to distinguish from human branches in the log.

**2. Per-session branches for parallel experiments.** When dispatching N agents on the same brief, `agent/<task>-v1`, `...-v2`, `...-v3`. Explicit numbering makes the diff-comparison phase readable.

**3. Long-lived feature branches for multi-session agent work.** When a single logical change takes multiple agent sessions over days (a large refactor, a codebase migration), a long-lived `feature/<name>` branch with periodic merges from main. Treat like human feature branches; the only difference is that most commits were produced by an agent.

## Layer 9 — Anti-patterns, with specific examples

**Letting an agent rebase `main`.** The single most destructive action an agent can take. A rebase of main rewrites public history; every collaborator's local main is now diverged; force-push makes it worse. *Prevention:* revoke the agent's ability to force-push (`git config remote.origin.push.forceWithLease false` as a defense-in-depth, plus branch protection on the remote). Never include "rebase main" in an agent brief.

**Force-pushing shared branches.** Same class of failure, one level down. If an agent is working in a shared branch (not a topic branch), a force-push erases other people's work. Branch protection with "require linear history" is the hard barrier; the soft barrier is discipline.

**Not committing before each agent call.** Covered above. If `git status` is dirty, stash or commit. Every time. Make it muscle memory.

**Relying on the agent's own "summary of changes."** Covered above. The summary is a hint, not a log. Read the diff.

**Running `npm install` (or equivalent) from inside an agent session.** Every install is a chance for a new dep to land quietly. Review `package.json` / `requirements.txt` diffs deliberately; don't trust that "it just installed what it needed."

**Worktree sprawl.** `git worktree list` should always be short. If you have 15 worktrees hanging around, half of them broken, your `.git/worktrees/` metadata is bloated and `git gc` is slow. Prune weekly: `git worktree prune` plus manually deleting abandoned branches.

## Runnable experiment — the parallel-diff lab

**Goal.** Experience the parallel-worktree pattern end-to-end, and rehearse `reflog` recovery on a real broken state.

**Setup.** Pick any small project you own. Create a fresh clone for this exercise; you will intentionally break it. Let's call the directory `lab-gitworktree/`.

```bash
cd ~/code/lab-gitworktree
git status  # must be clean
```

**Part A — parallel agents, side-by-side diffs.**

Write a brief. A concrete one that three different plausible implementations could satisfy. Example:

> *Add a `/healthcheck` endpoint to the existing HTTP server. It should return 200 with a JSON body including: a `status` field ("ok"|"degraded"), a `version` field (read from package.json), and a `checks` object listing dependency health (db, cache, external API). Include a test.*

Now direct Claude Code to dispatch two parallel subagents in isolated worktrees. In a Claude Code session at the repo root:

> *Dispatch two Claude subagents in parallel, each in its own worktree (`isolation: worktree`), both given the brief in `./brief.md`. Name them `healthcheck-v1` and `healthcheck-v2`. When both have finished, do not merge anything — just report back where each worktree lives.*

You now have `.claude/worktrees/healthcheck-v1/` and `.claude/worktrees/healthcheck-v2/`, each with a diff against main. Compare them:

```bash
git diff main..healthcheck-v1 > /tmp/v1.patch
git diff main..healthcheck-v2 > /tmp/v2.patch
diff /tmp/v1.patch /tmp/v2.patch | less
```

Or, better, open both worktrees in two editor windows side-by-side. Read the four AI-specific failure modes from Layer 6 against each. Pick one. Merge it. `git worktree remove` the other.

**What you should feel.** The uncomfortable productivity of realizing that having two candidate implementations actually helps you see what the *right* implementation should look like, in a way one candidate never does. The diff between v1 and v2 is itself a teaching artifact.

**Part B — `reflog` recovery, rehearsed.**

In the main worktree, intentionally break your repo. Pick a commit from yesterday that you care about. Then:

```bash
# Note the current HEAD SHA; write it down.
git log --oneline -5

# Deliberately destructive action:
git reset --hard HEAD~3

git status
git log --oneline -5
# Three commits are "gone"
```

Now recover. Without referring to the SHA you wrote down:

```bash
git reflog
# Find the HEAD@{n} entry just before the reset.
git reset --keep HEAD@{<n>}

# Verify:
git log --oneline -5
```

**What you should feel.** Calm. The first time you successfully do this, the underlying dread of "the agent destroyed my work" is meaningfully smaller than before. That dread was never proportionate to the actual risk, given reflog's 90-day retention. Most AI-builders carry it anyway until they rehearse recovery once. Do this at least twice before you need it in anger.

## Varied-domain examples (why this matters beyond web apps)

- **Legal / contract workflows.** A colleague runs a contract-analysis pipeline where Claude Code edits a structured-data schema across 30+ JSON files. Commit-per-iteration (Aider model) was the only way to bisect which specific schema edit broke downstream parsing.
- **Scientific / notebook-heavy work.** Jupyter notebooks in git are notoriously hard to diff. Worktrees help here specifically because `nbdiff` (from `nbdime`) can compare two worktrees of the same notebook much more readably than comparing two commits in one working tree.
- **Infrastructure-as-code.** Terraform / Pulumi projects where an agent generates 400 lines of HCL. Diff review is the entire QA. A single unnoticed `prevent_destroy = false` becomes a production incident.
- **Content / design pipelines.** Builders generating large volumes of prompt-engineered content (marketing, product copy, training data) treat each generation batch as a commit. `git revert` a batch that turned out to be poor quality; diff two batches to see how a prompt change shifted output.

The pattern generalizes: **any artifact you care about, stored as text, benefits from the same commit-per-iteration + diff-review + reflog-safety-net discipline**. Code is the most obvious case. It's not the only one.

## Common mistakes I see AI-pro leads make

1. **Dismissing worktrees as "too much overhead" without trying them.** Two commands, `add` and `remove`. The cognitive overhead is a one-time 30-minute learning cost. People who skip this stay stuck in serial agent workflows for months.
2. **Auto-committing the agent's summary text verbatim as the commit message.** The agent wrote "Updated several files" or "Added the feature". Your future self deserves better. Either compose the message yourself or, if you insist on AI-generated messages, use Aider's commit-message model (a different, smaller model tuned for it) rather than the main coding agent's end-of-turn prose.
3. **Not rehearsing `reflog` before needing it.** The first time you read `git reflog` under pressure you will misread an entry. Rehearse twice.
4. **Running agents against a shared remote without branch protection.** Required remotes: branch protection on `main`, require PR for merges, disallow force-push. Treat the agent as an untrusted contributor, because functionally it is.
5. **Ignoring the `.claude/worktrees/` directory until it's 40 GB.** It will grow. Put a weekly calendar reminder to `git worktree list && git worktree prune`.

## Reflection questions

1. For your current primary project, which commit philosophy (per-iteration, per-feature, per-green-test) actually fits? What would switching cost you?
2. What is the blast radius of the largest mistake an agent has made in your codebase in the last month? Walk through the recovery path you'd use today, step by step, out loud.
3. Cherny uses separate clones; the Claude Code team ships worktrees as the default. What is Cherny's setup optimizing for that worktrees don't give you — and does that thing matter for *your* work?
4. If you were to dispatch three agents on the same brief right now, how would you structure the review phase so that you don't pick the first plausible one out of laziness?
5. Which of the four AI-specific diff failure modes (hallucinated APIs, silent behavior flips, unrelated edits, new deps) would your current test suite actually catch? Which would slip through?

## My take (reviewer lens)

Where a stricter reviewer would push back on this lesson:

- **"You are overstating worktrees vs. clones."** A SWE-focused reviewer like Boris Cherny would point out that for his own pattern (five long-running sessions), separate clones genuinely are better — the worktree-is-universal framing many 2025 blog posts push is itself a fashion, not a universal best practice. I conceded this in Layer 5 but probably not strongly enough; a sharper version of this lesson would lead with "it depends on session length" rather than "worktrees are the default."
- **"Commit-per-green-test is unproven."** I flagged it as my own practice for six weeks. A stricter reviewer — Hamel Husain, say, on the evals side — would ask for data: what percentage of bugs get caught at bisect time that wouldn't have been caught at review time? I don't have that data yet. Treat it as a hypothesis with a ~60% prior on being right, not as settled practice.
- **"Reflog isn't actually forever."** Git's GC collects unreachable objects after 30 days (unreachable, not just deferenced) and reflog entries themselves expire after 90. A paranoid reviewer — Julia Evans territory — would note that "reflog is your safety net" has a time limit and that for truly important recovery, `git bundle` or explicit remote backup is the real answer. Fair. The 90-day window is enough for 99% of "oh no the agent did something bad" cases, but it is not infinite.
- **"You ducked the `isolation: worktree` vs. manual worktree question."** Whether to let Claude Code manage worktrees automatically via the agent parameter, vs. managing them manually with `git worktree add`, is its own tradeoff I didn't fully engage. Automatic is simpler; manual gives you more control and survives Claude Code version churn. For production workflows, I lean manual; for experimentation, automatic.
- **"The AI-specific diff failure modes list is incomplete."** Missing at least: license-incompatible code pasted verbatim from training data; subtle off-by-one errors in generated regex; timezone-naive datetime handling. A longer version of this lesson would have 8–10 categories, not 4.

## Further reading

**Must-read.**
- *Pro Git*, ch. 7.5 *Git Tools — Git Worktree.*[^1]
- Claude Code — *Common workflows* (especially the subagent + worktree section).[^2]
- Boris Cherny, *How I use Claude Code* (Threads thread + setup page).[^4][^14]
- Simon Willison, *Embracing the parallel coding agent lifestyle* (Oct 2025).[^7]

**Recommended.**
- Aider documentation, *Git integration* section.[^6]
- Damian Galarza, *Extending Claude Code Worktrees for True Database Isolation* (Mar 2026).[^12]
- Upsun Developer Center, *Git worktrees for parallel AI coding agents.*[^11]
- InfoQ, *Container Use: a New Tool for Isolated, Parallel Coding Agents* (Aug 2025).[^9]

**Optional.**
- GitHub issue anthropics/claude-code#39886 — `isolation: worktree` silent-failure class.[^10]
- Simon Willison, *Agentic Engineering Patterns* (ongoing, 2025–26).[^8]
- InfoQ, *Inside the Development Workflow of Claude Code's Creator* (Jan 2026).[^15]
- `git help reflog` and `git help worktree` — authoritative, short, worth five minutes.

## Citations

[^1]: Scott Chacon and Ben Straub, *Pro Git*, 2nd ed., "Git Tools — Git Worktree", https://git-scm.com/book/en/v2/Git-Tools-Worktrees (stable reference; verified 2026-04-15).
[^2]: Anthropic, *Claude Code — Common workflows*, https://code.claude.com/docs/en/common-workflows (section on subagent worktree isolation; verified 2026-04-15).
[^3]: Anthropic, Claude Code v2.1.50 release notes, announcing first-class worktree support across CLI, Desktop, and custom agents (Oct 2025), referenced in https://code.claude.com/docs/en/common-workflows.
[^4]: Boris Cherny (Head of Claude Code, Anthropic), setup thread, "I'm Boris and I created Claude Code...", https://www.threads.com/@boris_cherny/post/DTBVlMIkpcm — describes his five-separate-clones pattern (late 2025).
[^5]: Boris Cherny, "Introducing: built-in git worktree support for Claude Code", https://www.threads.com/@boris_cherny/post/DVAAnexgRUj (Oct 2025).
[^6]: Aider documentation, *Git integration* — auto-commit-per-edit philosophy, https://aider.chat/docs/git.html (verified 2026-04-15; Gauthier since v0.1, July 2023, maintained through 2025–26).
[^7]: Simon Willison, *Embracing the parallel coding agent lifestyle*, https://simonwillison.net/2025/Oct/5/parallel-coding-agents/ (Oct 5, 2025).
[^8]: Simon Willison, *Agentic Engineering Patterns*, https://simonwillison.net/guides/agentic-engineering-patterns/ (ongoing guide, 2025–26).
[^9]: InfoQ, *Container Use: a New Tool for Isolated, Parallel Coding Agents*, https://www.infoq.com/news/2025/08/container-use/ (Aug 2025).
[^10]: GitHub issue anthropics/claude-code#39886, "isolation: 'worktree' silently fails — agent runs in main repo instead of isolated worktree", https://github.com/anthropics/claude-code/issues/39886 (filed March 27, 2026; closed as duplicate). Documents `worktreePath: done` with `worktreeBranch: undefined` when dispatching a subagent with `isolation: "worktree"` — the worktree is never created and the agent runs in the main repo, causing branch-checkout races when multiple agents share `.git` state.
[^11]: Upsun Developer Center, *Git worktrees for parallel AI coding agents*, https://devcenter.upsun.com/posts/git-worktrees-for-parallel-ai-coding-agents/ (2025).
[^12]: Damian Galarza, *Extending Claude Code Worktrees for True Database Isolation*, https://www.damiangalarza.com/posts/2026-03-10-extending-claude-code-worktrees-for-true-database-isolation/ (Mar 10, 2026).
[^13]: Git documentation, *git-reflog*, https://git-scm.com/docs/git-reflog (stable reference; 90-day default expiry, configurable via `gc.reflogExpire`).
[^14]: Gergely Orosz, *Building Claude Code with Boris Cherny*, Pragmatic Engineer newsletter, https://newsletter.pragmaticengineer.com/p/building-claude-code-with-boris-cherny (2025).
[^15]: InfoQ, *Inside the Development Workflow of Claude Code's Creator*, https://www.infoq.com/news/2026/01/claude-code-creator-workflow/ (Jan 2026).
[^16]: Cursor (2026-04-02). *Changelog 3.0* — native `/worktree` command that creates an isolated worktree per agent. https://cursor.com/changelog/3-0. Anthropic (2026-05-28). *Introducing dynamic workflows in Claude Code* — hundreds of parallel subagents from a Claude-written orchestration script (capped at 1,000). https://claude.com/blog/introducing-dynamic-workflows-in-claude-code. Both verified 2026-07-17.

_last_verified: 2026-07-17_
