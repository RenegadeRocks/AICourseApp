# CLAUDE.md — runbook for agents working in this repo

This is a personal study system for the **AI Pro-level Course** (Renegade
Rocks, instructed by Claude Opus 4.6/4.7). It's a hybrid:

- `vault/` — plain markdown, one file per lesson (the source of truth)
- `app/` — Next.js 15 reader at `http://localhost:3000`
- `scripts/` — Python utilities (curriculum parser, Anki/NotebookLM/EPUB exports)
- `.claude/commands/` — slash commands for lesson generation
- `curriculum.json` — parsed 9-block / 26-week schedule

Read `README.md` for the human-facing overview. This file is the
deterministic runbook for *you*.

---

## Run the app

```bash
cd app
npm install     # only if app/node_modules is missing
npm run dev     # run in background — it blocks until killed
```

Then tell the user: open `http://localhost:3000`. Today's lesson auto-routes
from the first uncompleted slot in the schedule.

**Always background the dev server** (e.g. `run_in_background: true` on
Bash). Foregrounding it will hang the session — Next.js doesn't exit.

If port 3000 is in use, prefer killing the prior dev server over changing
ports. The launchers and bookmarks assume 3000.

## What auto-initializes (don't try to set these up)

- **SQLite progress DB** — `app/src/lib/db.ts` calls `CREATE TABLE IF NOT
  EXISTS` on first request. File is `app/progress.db`, gitignored.
- **FlexSearch index** — built in-memory on first search request by
  walking `vault/`. No persisted index file.
- **Vault content** — already on disk under `vault/`. Don't regenerate.

## Run the app on a fresh machine

Same as above. The user needs Node.js 20+ and (optionally) the `claude`
CLI installed; everything else is in the repo. `better-sqlite3` compiles
natively during `npm install` — if that fails, the user is missing C++
build tools (Visual Studio Build Tools on Windows, Xcode CLT on Mac).

## Generate content (only when the user asks)

Lesson generation lives in `.claude/commands/`:

```
> /generate-lesson <block-id>/<week-id>
> /generate-quiz   <block-id>/<week-id>
> /generate-flashcards <block-id>/<week-id>
```

Before generating, **always read** `vault/00-program/quality-standard.md`
and the relevant brief in `.claude/block-N-briefs/`. Lessons are
standalone expert masterclasses (L3 spec): 5000-6500 words, 8+ web-verified
citations, named reviewer lens, controversies engaged. Word counts are
soft targets — longer is fine if tight.

Content pipeline (proven across Weeks 1-5): parallel generation →
multi-persona review → surgical polish → citation verification. Each phase
gets its own subagent dispatch. Reviewer roster as of July 2026: Karpathy,
Chip Huyen, Jerry Liu, Hamel Husain, Simon Willison, Seibel, Boris Cherny,
cohort peer + Mira Murati, swyx, Ethan Mollick, Lilian Weng, Jeremy Howard
(see `vault/00-program/_refresh-2026-07-master-report.md`).

## EPUB output (replaces the old Notion mirror)

The course's read-elsewhere output is a single Kindle-ready EPUB, not Notion.
After generating or refreshing content, rebuild it:

```
> /export-epub            # all blocks -> exports/ai-pro-level-course.epub
python scripts/export_epub.py [--block <block-dir-name>]
```

Send the resulting file to the user (they load it via Send-to-Kindle).
`exports/` is gitignored — the EPUB is a build artifact, regenerated from the
vault. Do not push course content to Notion.

## Chat feature

`/api/chat` shells out to the `claude` CLI (`spawn('claude', ['-p'])`).
No API key needed — runs on the user's Max subscription. If `claude` isn't
on PATH the chat route returns a friendly error; the rest of the app keeps
working.

## Don't

- Don't commit `app/progress.db` (per-machine state, gitignored).
- Don't commit `node_modules/`, `.next/`, or `.claude/*.lock` /
  `.claude/w*_*.json` (transient pipeline artifacts, gitignored).
- Don't generate placeholder content with fabricated citations. Every
  citation must resolve to a real URL — see `feedback_content_standards`
  memory if you have access.
- Don't add calendar dates back to the app surface. The schedule is
  slug-based (block / week-in-program / day-of-cycle) — see
  `app/src/lib/schedule.ts`. Calendar dates were intentionally removed.
- Don't refer to "AI Catalyst" or "Outskill" in user-facing copy. The
  brand is "AI Pro-level Course" by "Renegade Rocks". (The xlsx filename
  on disk still says "AI Catalyst C3" — that's the real filename, leave
  it alone.)

## Project conventions

- Pre-approved Bash commands live in `.claude/settings.local.json`
  (committed). `npm install`, `npx tsc`, `npx next`, and `python` won't
  prompt for permission.
- TypeScript is strict; Next.js typed routes are on. Dynamic `href`s need
  `as Route` casts — see existing pages for the pattern.
- Tailwind `grid-cols-N` only works for N ≤ 12. For wider grids use inline
  `style={{ gridTemplateColumns: ... }}` — see `app/src/app/progress/page.tsx`.
- Lesson titles fall back through: frontmatter `title` → first H1 in body
  → prettified slug. Don't add new fallbacks.
