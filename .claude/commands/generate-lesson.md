---
description: Deep-research generator for a week's daily lessons. Takes a week slug, writes all 7 daily lesson files + exercises + code-lab + quiz + flashcards + citations.
argument-hint: <block-id>/<week-id>   e.g. block-0-basecamp/week-01
---

# /generate-lesson $ARGUMENTS

You are generating **world-class study material** for the AI Catalyst C3 program.
Quality bar: Andrej Karpathy, Boris Cherny, Chip Huyen, Michael Seibel,
Lenny Rachitsky — operator-grade, cited, runnable, honest.

## Step 1 — Load context

1. Read `curriculum.json` to find the target week. The argument format is
   `<block-id>/<week-id>` (e.g. `block-0-basecamp/week-01`).
2. Read `vault/00-program/index.md`, `how-to-study.md`, and
   `quality-standard.md` — **you must obey the quality standard**.
3. Read the existing `_week.md` in the target week folder — it has the
   authoritative session list parsed from the xlsx.
4. Check which files already exist in the week folder. **Do not overwrite**
   existing lesson files unless the user explicitly said "regenerate".

## Step 2 — Research deeply

For the week's topics, gather material from **Tier-1 sources only** for the
backbone. Use web search aggressively.

Tier-1 sources (ranked by domain relevance):

- **Foundations / ML / tokenization / transformers**: Karpathy (Zero-to-Hero,
  nanoGPT, "Let's build GPT", "Let's build the GPT Tokenizer", "Deep Dive into
  LLMs"), Stanford CS224n/CS25/CS336, fast.ai, 3Blue1Brown NN series.
- **Prompting / LLM engineering**: Anthropic Cookbook + docs, OpenAI Cookbook,
  Simon Willison's blog, Hamel Husain, Eugene Yan, Chip Huyen (*AI Engineering*).
- **RAG**: Anthropic Contextual Retrieval, Jerry Liu (LlamaIndex), Jason Liu
  (<jxnl.co>), Wang et al. "Searching for Best Practices in RAG", Microsoft
  GraphRAG.
- **Agents**: Anthropic "Building effective agents" (Dec 2024), Lilian Weng
  "LLM Powered Autonomous Agents", LangGraph/CrewAI docs.
- **Claude Code / MCP**: Anthropic MCP spec + reference servers, Boris Cherny
  talks, official Claude Code docs.
- **Voice / Telephony**: VAPI docs, Twilio docs, WATI / AiSensy docs,
  ElevenLabs / Deepgram / Cartesia docs, Retell AI case studies.
- **n8n / Automation**: official n8n docs, community workflows, Zapier / Make
  guides.
- **YC / Sales / Pricing**: Paul Graham essays, YC Startup School library,
  Michael Seibel talks, Harj Taggar on sales, Jason Lemkin on SaaS pricing.
- **Product / GTM**: a16z AI Canon, First Round Review, Marty Cagan
  (*Inspired*), Lenny Rachitsky newsletter, April Dunford (*Obviously Awesome*).
- **Design**: Refactoring UI, Linear design principles, shadcn/ui patterns.
- **Papers**: Attention Is All You Need, RAG (Lewis et al.), Chinchilla,
  InstructGPT/RLHF, DPO, ReAct, Toolformer.

**Rule**: every factual claim cites a source. If you can't find a tier-1
source for a claim, either find one or mark it `> My take:` and argue it.

## Step 3 — Expand into 7 daily lessons

A live-class week has 2 live sessions (Sat + Sun). Expand it into **7 daily
lessons** following `how-to-study.md` (day-of-cycle 1..7 mapped to Mon..Sun):

1. **Mon** — Pre-read Session 1 (orientation, vocabulary, 3 questions)
2. **Tue** — Session 1 deep-dive A: concepts from first principles
3. **Wed** — Session 1 deep-dive B: tradeoffs, production pitfalls, worked example
4. **Thu** — Pre-read Session 2 (orientation for Sunday's live)
5. **Fri** — Session 2 deep-dive A: concepts
6. **Sat** — Session 2 deep-dive B + live-session companion notes
7. **Sun** — Week recap + synthesis + reviewer lens + quiz

For weeks with only 1 live session (e.g. Onboarding Week 0), compress to 3–5
days and mark the others as rest days.

## Step 4 — Write files

For each daily lesson, create:

- `<NN>-<day>-<topic-slug>.md` — the lesson itself (2000–4000 words). NN is
  `01` through `07`; `<day>` is `mon`/`tue`/.../`sun`.
- If the day needs runnable code, add `code-lab/<NN>/` with `README.md`,
  `requirements.txt` or `package.json`, and the source files.

At the end of the week also write:

- `05-quiz.md` — 10–15 questions (MCQ + short-answer + code-completion mix).
- `06-flashcards.md` — 15–30 Anki-ready cards (front/back format, one per line
  or separated by `---`).
- `07-notebooklm-pack/README.md` — instructions on dragging the pack into
  NotebookLM, plus a consolidated `lesson-bundle.md` with all 7 lessons
  inlined (no wiki-links, no frontmatter — NotebookLM-friendly).
- `00-overview.md` — 1-page week overview linking to each daily lesson with a
  one-line summary.

## Step 5 — Obey the lesson template

Each lesson file starts with YAML frontmatter:

```
---
type: lesson
block: <block-id>
week: <week-id>
day_of_cycle: <1-7>
day_name: <mon|tue|...|sun>
session_slug: <session-slug>
date_due: YYYY-MM-DD
tags: [...]
sources: [tier-1-source-keys]
last_verified: YYYY-MM-DD
---
```

Body structure (enforced):

1. `# <Title>` — short, active, specific.
2. `## Why this matters` — operator framing: what you'll build, sell, decide.
3. `## Prerequisites` — `[[links]]` to earlier vault lessons or primers.
4. `## Core content` — first principles → mechanics → tradeoffs → pitfalls.
5. `## Worked example` — runs, cites the code-lab folder.
6. `## Common mistakes experts see` — 5+ bullets.
7. `## Reflection questions` — 5–10, non-Googleable.
8. `## My take (reviewer lens)` — critical, specific, names names.
9. `## Further reading` — Must-read / Recommended / Optional.
10. `## Citations` — `[^N]:` footnotes.

## Step 6 — Verify before finishing

Run through this checklist for every file:

- [ ] ≥5 citations, all with URL + author + timestamp/page
- [ ] ≥2 tier-1 sources
- [ ] Code in `code-lab/` actually runs (trace it mentally step-by-step)
- [ ] 2+ `[[wikilinks]]` to other vault lessons
- [ ] `My take` section is specific, not generic
- [ ] `last_verified` stamp = today's date
- [ ] File length 2000–4000 words (lesson); 300–800 (exercises)

## Step 7 — Commit

After writing all files, stage and commit with:

```
git add vault/$ARGUMENTS/
git commit -m "lesson: generate $ARGUMENTS"
```

## Parallelism

If generating an entire block, dispatch **one subagent per week** using the
`Agent` tool with `subagent_type: "general-purpose"`. Each subagent gets a
self-contained prompt naming the week slug and pointing at this command file.
They write to disjoint folders → safe to run in parallel.
