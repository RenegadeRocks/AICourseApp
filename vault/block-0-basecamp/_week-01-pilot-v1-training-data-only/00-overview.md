---
type: week-overview
block: block-0-basecamp
week: week-01
sessions:
  - slug: basecamp-part-1-prompting-rags
    date: 2026-05-02
    kind: live-session
  - slug: basecamp-part-2-vibe-coding
    date: 2026-05-03
    kind: live-session
last_verified: 2026-04-14
---

# Week 01 — Basecamp: Prompting & RAGs + Vibe Coding

> Two live sessions. Two of the highest-ROI skills in practical AI engineering.
> By Sunday night you will have built a working RAG pipeline from scratch and shipped
> your first vibe-coded prototype.

## The Week at a Glance

| Day | File | Topic | Est. Time |
|-----|------|--------|-----------|
| Mon | [[01-mon-prompting-rags-preread]] | Pre-read: what prompting & RAG actually solve | 35 min |
| Tue | [[02-tue-prompting-deep-dive]] | Deep-dive: CoT, few-shot, XML, tool use, structured outputs | 90 min |
| Wed | [[03-wed-rag-deep-dive]] | Deep-dive: naive → contextual retrieval → reranking → evals | 90 min + code-lab |
| Thu | [[04-thu-vibe-coding-preread]] | Pre-read: vibe coding origin, mental model, when to use | 35 min |
| Fri | [[05-fri-vibe-coding-tools]] | Deep-dive: Cursor, Claude Code, Bolt, Lovable, v0, Replit | 90 min |
| Sat | [[06-sat-vibe-coding-live-companion]] | Live-session companion: build alongside instructor | 30 min prep + 2 h live |
| Sun | [[07-sun-recap-synthesis]] | Recap, synthesis, reviewer lens, quiz | 45 min |

**Supplementary**
- [[05-quiz]] — 12 questions with answer key
- [[06-flashcards]] — 25 cards (Anki-ready)
- [[07-notebooklm-pack/README]] — drag-and-drop pack for NotebookLM

## Live Sessions This Week

| # | Title | Date & Time | Kind |
|---|-------|-------------|------|
| 1 | Basecamp Part 1: Prompting & RAGs | Sat 2026-05-02, 19:30 IST | Live |
| 2 | Basecamp Part 2: Vibe Coding | Sun 2026-05-03, 19:30 IST | Live |

## Why These Two Topics Together?

Prompting and RAG are **input-side engineering** — how you shape what goes into the model and what context surrounds it. Vibe coding is **output-side engineering** — how you turn model output into working software at speed. Together they describe the full stack of an AI practitioner who ships things rather than just demos them.

The order is intentional: understand how to speak to a model precisely (prompting), understand how to give it the right facts (RAG), then understand how to turn its output into real products (vibe coding).

## Code Lab

`code-lab/01-rag-from-scratch/` — Python RAG pipeline:
- Chunking → embedding (sentence-transformers) → FAISS retrieval → contextual enrichment → generation
- Runs locally with no paid API key required for the retrieval step; uses Anthropic API for generation
- See `README.md` for exact setup command

## Links

- [[00-program/index]] — program overview and master reading list
- [[00-program/how-to-study]] — the 7-day cycle protocol
- [[../week-02-basecamp-part-3-mcps-voice-agents--basecamp-part-4-revisiting-n8n-ai-agent-fundamentals/ (pending)]] — next week

_last_verified: 2026-04-14_
