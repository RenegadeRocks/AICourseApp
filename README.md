# AI Catalyst C3 — Personal Study System

A hybrid markdown-vault + local Next.js app for studying the **AI Catalyst C3**
cohort (Outskill, Apr 18 2026 → Oct 22 2026) at a Karpathy / YC / fast.ai
level of rigor.

## What you get

- **`vault/`** — an Obsidian-compatible markdown vault. Source of truth. Every
  week expands to 7 daily lessons, each cited, with runnable code labs.
- **`app/`** — a local Next.js 15 app at `http://localhost:3000` that routes
  by date to "today's lesson", tracks your streak, lets you search and chat
  with your vault, and exports to NotebookLM / Anki.
- **`.claude/commands/`** — slash commands you run inside Claude Code (uses
  your Claude Max subscription — zero API cost) to generate lessons,
  quizzes, flashcards, and NotebookLM bundles on demand.
- **`launchers/`** — menu-bar (macOS / SwiftBar) and system-tray (Windows /
  AutoHotkey) shortcuts so opening today's lesson is one click.
- **`scripts/`** — `parse_xlsx.py` (curriculum), `scaffold_vault.py` (folder
  tree), `anki_export.py` (`.apkg` decks), `notebooklm_export.py` (bundles).
- **`curriculum.json`** — canonical parsed schedule (9 blocks, 26 weeks, 50
  live sessions).

## Quick start

### 1. First-time setup (either machine)

```bash
# 1. Python deps (one-time)
pip install -r scripts/requirements.txt

# 2. Parse curriculum and scaffold vault (already run, idempotent)
python scripts/parse_xlsx.py
python scripts/scaffold_vault.py

# 3. App deps (one-time)
cd app
npm install
npm run build   # optional — proves it compiles
```

### 2. Generate study material (done inside Claude Code)

```bash
claude
# in the Claude Code REPL:
> /generate-lesson block-0-basecamp/week-01
> /generate-quiz   block-0-basecamp/week-01
> /generate-flashcards block-0-basecamp/week-01
```

You can also dispatch parallel subagents — see `.claude/agents/lesson-researcher.md`.

### 3. Daily study

```bash
cd app
npm run dev
# open http://localhost:3000 — today's lesson is auto-routed
```

Or click the menu-bar / tray launcher (see `launchers/README.md`).

### 4. Study-time queries & fresh quizzes

```bash
# in Claude Code, inside vault/
> /chat-course "compare naive vs contextual RAG"
> /generate-quiz block-0-basecamp/week-01
```

### 5. Exports when you want them

```bash
# NotebookLM bundle (for audio overview / mind map / video)
python scripts/notebooklm_export.py block-0-basecamp/week-01-basecamp-part-1-prompting-rags--basecamp-part-2-vibe-coding

# Anki deck
python scripts/anki_export.py block-0-basecamp
```

## Cross-machine sync

This repo is a git repo. Clone on both Mac and Windows. `progress.db`
(streaks) is **per-machine** (git-ignored). When generating content, commit
and push. When syncing completions, we can add a `progress.json` mirror if
you want shared streaks — defer until you actually feel the friction.

## Project layout

```
.
├── AI Catalyst C3 - Tentative Schedule.xlsx   — source of truth (upstream)
├── curriculum.json                             — parsed, versioned
├── vault/                                      — study material
│   ├── 00-program/                             — index, how-to-study, quality-standard
│   └── block-<N>-*/week-<N>-*/                 — daily lessons, code-lab, quiz, flashcards
├── app/                                        — Next.js 15 + Tailwind
├── launchers/                                  — Mac menu-bar + Windows tray
├── scripts/                                    — parse, scaffold, export
├── .claude/
│   ├── commands/                               — slash commands (generate-lesson, etc.)
│   └── agents/lesson-researcher.md             — subagent for parallel generation
└── exports/                                    — generated .apkg, NotebookLM packs
```

## Quality standard

Non-negotiable rules lessons must satisfy — see
[vault/00-program/quality-standard.md](vault/00-program/quality-standard.md).

## Principles

1. **Files outlive apps.** Content is plain markdown; the app is a reader.
2. **Claude Code is the intelligence layer.** Your Max subscription runs it —
   no API key anywhere in this repo.
3. **World-class or don't bother.** Every claim cites a Tier-1 source.
4. **Daily ritual, not binge.** 7-day cycle per live-class week.
5. **Reviewer lens.** Every lesson ends with "what would Karpathy / Seibel /
   Boris push back on?" That's where taste comes from.
