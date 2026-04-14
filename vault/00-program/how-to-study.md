---
type: study-protocol
---

# How to Study — The Daily Ritual

> The live cohort gives you 2 hours per week with the instructor.
> This vault gives you 2+ hours every day with the world's best teachers on each topic.
> The goal: walk into every live session already fluent.

## The 7-Day Cycle (per live-class week)

Each live-class week has 2 live sessions (Sat + Sun). The vault expands this
into 7 daily lessons so that every live session is entered from mastery:

| Day | What | Target time | Output |
|---|---|---|---|
| **Mon** | Pre-read Session 1 | 30–45 min | Highlights + 3 questions to answer |
| **Tue** | Deep-dive Session 1A (concepts) | 60–90 min | Notes + code-lab run |
| **Wed** | Deep-dive Session 1B (tradeoffs + pitfalls) | 60–90 min | Reflection answers |
| **Thu** | Pre-read Session 2 | 30–45 min | Questions for office hours |
| **Fri** | Deep-dive Session 2A (concepts) | 60–90 min | Notes + code-lab run |
| **Sat** | Deep-dive Session 2B + LIVE session | 60–90 min + 2h live | — |
| **Sun** | Live session 2 + recap | 2h live + 30 min | Fill the "what surprised me" card |

**Sunday night habit**: flashcards review (10 min), mark week complete, generate fresh quiz:
`/generate-quiz <week-slug>`. Take it cold. If you score <80 %, schedule a
`/deepen-lesson` on the weakest topic for Monday.

## The Daily Ritual (applies every weekday)

1. **Open the app** (menu-bar / tray icon → localhost:3000). It shows *today's
   lesson* computed from the program schedule.
2. **Read actively**. Don't skim. At every bold claim, ask: "do I believe this?
   Could I explain it to a beginner? Could I argue against it?"
3. **Run the code** in `code-lab/`. Actually run it. Modify one thing. See what breaks.
4. **Answer the reflection questions** — type directly into the app; stored in
   `progress.db` with the lesson ID.
5. **Ask Claude Code anything you're unsure about**: `cd vault && claude` →
   `/chat-course "explain contextual chunk retrieval like I'm in week 2"`.
6. **Mark complete** → streak increments. Takes 2 seconds.

## The Weekly Ritual (Sunday night)

1. **Flashcard review** — Anki deck for the week (10 min).
2. **Quiz cold** — `/generate-quiz <week-slug>`, score yourself.
3. **Refresh curriculum** — `/refresh-curriculum` picks up any upstream changes
   from Outskill's Monday resource drop and regenerates affected lessons.
4. **Write a 3-line post-mortem** in the week's `_week.md` under "What I'd tell
   the me from last Monday".
5. **Generate next week's prep** — `/generate-lesson <next-week-slug>` runs
   overnight so Monday's pre-read is fresh.

## Five Rules That Prevent Fake Learning

1. **No passive reading.** If you can't restate the main point aloud in 30
   seconds without looking, go back.
2. **No code skipping.** Every code block gets typed, run, or modified.
3. **Cite or ignore.** If a claim isn't cited and you can't reproduce it, flag
   it with `> [!question]` in the lesson and ask Claude Code.
4. **Teach it out.** End every lesson by writing one paragraph in plain English,
   as if to a friend — store under "My Take" in the lesson file.
5. **Quiz cold, not warm.** Always take the weekly quiz without re-opening the
   lesson first. That's the only signal that actually generalizes.

## Tracking Your Streak

- **App**: streak counter visible on the home screen, green days on a 6-month
  calendar.
- **Git history**: your commits to `app/progress.db` (if synced) or
  `progress.json` tell the real story.
- **The 80 % rule**: if you miss two days in a row, start the week over. Not
  the daily lesson — the *week*. Discipline compounds.

## Office Hours Protocol

On Thursdays:

1. Open the office-hours lesson file for the current week.
2. Paste your top 3 questions from the week into it.
3. Ask them live. If not all asked, post in the cohort channel right after.
4. Log the instructor's answer in the file. That file becomes your longest-
   compounding asset — cohort-specific knowledge you can't get anywhere else.

## When You Fall Behind

- Don't binge. Binging breaks memory consolidation.
- Instead: **skip recap days**, not deep-dive days. Those are the cheapest to skip.
- Run `/deepen-lesson` only for topics you'll actually touch in your projects.
- The live sessions have recordings — watch at 1.5× if you must catch up.
