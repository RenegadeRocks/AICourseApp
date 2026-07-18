---
type: week-overview
block: block-3-advanced-topics-voice
week: week-08
title: 'Week 8 — Unattended automation, MCP integration, and the hybrid scraper + summarizer'
live_sessions:
  - '2026-07-11 — Automation + Agent Integration (MCPs)'
  - '2026-07-12 — Build: Hybrid Agent (Scraper + Summarizer)'
study_window: 2026-07-06 to 2026-07-12
last_verified: 2026-07-17
---

# Week 8 — Unattended automation, MCP integration, and the hybrid scraper + summarizer

## The thesis of this week

Everything you have built so far ran with you watching. Week 8 removes you from the room. The subject is **unattended automation**: agents that run on schedules and triggers, integrate with real systems over MCP, pull data from a web that is actively fighting crawlers, and produce output nobody reviews before it ships. That last clause is the whole discipline. An agent whose output a human checks is a tool; an agent whose output goes straight to a customer, a channel, or a decision is a liability unless you have engineered the reliability in.

The capstone is the canonical hybrid: a **scraper + summarizer** that monitors sources in your niche, extracts structured items, dedups, synthesizes a cited daily brief, and delivers it on a schedule — with a golden-set eval harness and failure alerting, because in 2026 shipping the pipeline without the eval is shipping half the system.

## Who this week is for

You finished Blocks 0–2: you can build an MCP server ([[02-tue-building-an-mcp-server]]), you know the lethal trifecta ([[03-wed-mcp-security]]), you have run an eval harness against a RAG agent ([[06-sat-rag-evaluation]]), and you shipped the Week 5 report generator ([[06-sat-build-the-weekly-report-generator]]). Weeks 6 and 7 of this block (context engineering, voice) are referenced where built; where pending, links are marked.

## Shape of the week

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | The automation spectrum in 2026 — n8n 2.0 / Make / Zapier vs code-first (Claude Code Routines, Agent SDK, cron) vs platform-native; determinism-vs-judgment decision framework; total-cost math | Deep-dive + decision exercise |
| Tue | Integration patterns with MCP — headless auth (client credentials, CIMD), idempotency, webhook-in / MCP-out, the 2026-07-28 stateless RC, least-privilege for unattended agents | Deep-dive + teardown |
| Wed | The scraping stack, legally and technically — Playwright/Browserbase/Firecrawl, Cloudflare's crawler tolls and the Sept 15 default block, robots.txt/ToS/case law, ethical rules this course endorses | Deep-dive + policy exercise |
| Thu | Hybrid agent design — deterministic stages + LLM judgment stages, checkpointing, TRANSIENT/PERMANENT retries, output contracts via structured outputs, cost budgets, drift detection | Deep-dive + architecture exercise |
| Fri | Reliability engineering for unattended agents — golden-set regression, canaries, drift metrics, hallucination containment, kill switches, when to keep a human in the loop | Deep-dive + eval build |
| Sat | BUILD: the hybrid scraper + summarizer — scheduled, monitored, evaluated, delivered | Build day + `code-lab/06-hybrid-agent/` |
| Sun | Synthesis + quiz + flashcards + Block 3 capstone recap | Review |

## Why these topics belong together

The week is one system viewed from five angles. Monday picks the runtime. Tuesday wires it to the world safely. Wednesday secures the data supply against a web that now meters AI access — Cloudflare will block mixed-use AI crawlers by default on ad-carrying pages from September 15, 2026, and the legal ground under scraping is moving the same direction. Thursday shapes the pipeline so deterministic stages do everything determinism can do and the model only spends judgment where judgment pays. Friday makes it safe to walk away. Saturday you build the whole thing; Sunday you consolidate.

## What "L3 depth" means this week

Every deep-dive engages at least one live controversy with named positions (workflow tools vs agents; the scraping fight between Cloudflare/publishers and AI companies; how much autonomy unattended agents should get), carries 8+ web-verified citations current to July 2026, includes a runnable experiment orchestrated through Claude Code, and closes with a reviewer lens that argues against the lesson itself.

## How to study this week

Experiment first, Must-read citations second, prose last. Saturday's build is the week: budget 3+ hours for it and treat Friday's eval lesson as its prerequisite, not optional theory. Run the code-lab before the live session so your questions are about *your* failures, not hypothetical ones.

_last_verified: 2026-07-17_
