---
type: week-overview
block: block-3-advanced-topics-voice
week: week-07
title: 'Week 7 — Voice agent squad + the WhatsApp extension'
live_sessions:
  - '2026-07-04 — Voice Agent Squad'
  - '2026-07-05 — Voice Agent Extended to a Chatbot on WA'
study_window: 2026-06-29 to 2026-07-05
last_verified: 2026-07-17
---

# Week 7 — Voice agent squad + the WhatsApp extension

## The thesis of this week

[[04-thu-voice-agents-architecture|Week 2's voice lesson]] taught you to draw the pipeline on a napkin (VAD, endpointing, STT, LLM, TTS, transport) and to know where the 800-millisecond budget goes. This week you graduate from *architecture* to *production*: you will pick vendors with July-2026 numbers in hand, engineer the conversation itself (turn-taking, interruptions, latency masking), split one agent into a routed squad of specialists, keep the whole thing legal across three jurisdictions, and then extend the same agent brain to the channel where your likely first market actually lives: WhatsApp, with its 24-hour windows, per-message pricing, and half a billion Indian users.

The unifying claim: **a voice agent is not a model, it is a system with one brain and many surfaces.** The brain (prompt, tools, context, evals) is channel-agnostic. The surfaces (a phone call, a web widget, a WhatsApp thread, a WA voice note) each have their own physics, economics, and law. Teams that couple the brain to one surface rebuild everything for the second channel. Teams that separate them ship the second channel in a weekend. Saturday you prove it: a working triage-plus-specialists voice squad, then the same brain answering on WhatsApp, with latency and containment measured against the [[06-sat-rag-evaluation|Week 4 eval discipline]].

## Who this week is for

You ship agents (Block 2), you know context engineering and retrieval architecture (Week 6), and you understand the voice pipeline's components and failure modes (Week 2 Thursday, a required prerequisite; this week does not re-teach it). You are now making *vendor, architecture, and channel* decisions with real per-minute and per-message money attached, possibly for a client, possibly for your own product's first market.

## Shape of the week

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | The 2026 voice stack, vendor by vendor: S2S vs cascaded now, per-minute economics, platform vs parts | Deep-dive + vendor-selection worksheet |
| Tue | Conversation engineering: turn-taking, endpointing, interruptions, latency budgets, telephony vs web, what kills perceived quality | Deep-dive + instrumented experiment |
| Wed | The voice agent squad: triage → specialist handoff, squad topologies, shared context, when a squad is ceremony | Deep-dive + squad design exercise |
| Thu | Voice agent trust & safety: disclosure law (EU AI Act Art. 50, state laws, TCPA), voice cloning, audio injection, recording consent, PII | Deep-dive + compliance checklist |
| Fri | WhatsApp: the chatbot extension — Cloud API, per-message pricing (and the October 2026 change), 24-hour windows, voice notes, one brain / many channels | Deep-dive + channel economics model |
| Sat | BUILD: voice squad + WA extension — Vapi squad with tool calls, same brain on WA, measure latency + containment | Build day + `code-lab/6/` |
| Sun | Synthesis, quiz, flashcards | Review |

## Why these topics belong together

The curriculum's two live sessions ("Voice Agent Squad" and "Voice Agent Extended to a Chatbot on WA") are two halves of one production question: *how do you scale one working agent along two axes at once?* The squad scales it **across competence** (triage → billing specialist → booking specialist) without bloating a single prompt past reliability. The WhatsApp extension scales it **across channels** without duplicating the brain. Both scalings fail the same way (context lost at a seam), and both are governed by the same discipline: measure containment and resolution per intent, not vibes per demo. Mon/Tue give you the substrate facts and the conversation physics; Wed gives you the multi-agent architecture; Thu keeps you unbanned and unsued; Fri gives you the second channel; Sat composes all five.

## What "L3 depth" means this week

Every lesson engages: (1) a live controversy with named positions — speech-to-speech vs cascaded in production, Cognition's "don't build multi-agents" vs the platform-squad pattern, the human-disclosure debate, Meta charging for service messages while exempting its own AI agent; (2) July-2026 numbers verified this cycle — Realtime-2.1 token pricing, Flux per-minute rates, Vapi/Retell all-in economics, WA per-message rates and the October 1, 2026 change; (3) a runnable artifact per day (worksheet, instrumented run, squad spec, compliance checklist, channel P&L, working build); (4) reviewer lenses that rotate across Karpathy, Chip Huyen, Simon Willison, Seibel, Hamel Husain, Lilian Weng, Boris Cherny, swyx, and Ethan Mollick.

A verification note for this week: several vendor domains block direct fetches from this environment, so every fast-moving number carries at least two independent search corroborations and is tagged accordingly in the citations. Treat any single-source number as a lead, not a fact — the lessons flag which is which.

## How to study this week

Monday and Friday are pre-reads for the two live sessions; Tuesday, Wednesday, and Thursday are the deep dives; Saturday is the build (budget 3–4 hours plus platform sign-ups — Vapi/Retell free credits and the WA Cloud API test number both cost nothing to start). Do the Saturday build even if you skip an experiment mid-week: this is the block's first end-to-end voice production artifact, and Week 8's automation-hybrid week assumes it exists.

_last_verified: 2026-07-17_
