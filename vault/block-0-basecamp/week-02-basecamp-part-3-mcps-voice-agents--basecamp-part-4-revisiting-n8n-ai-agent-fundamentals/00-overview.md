---
type: week-overview
block: block-0-basecamp
week: week-02
title: 'Week 2 — MCPs, voice agents, and the agent-engineering substrate'
live_sessions:
  - '2026-05-09 — Basecamp Part 3: MCPs & Voice Agents'
  - '2026-05-10 — Basecamp Part 4: Revisiting n8n & AI Agent Fundamentals'
study_window: 2026-05-04 to 2026-05-10
last_verified: 2026-07-17
---

# Week 2 — MCPs, voice agents, and the agent-engineering substrate

## The thesis of this week

Week 1 taught the core primitives — prompting, retrieval, agentic loops with tool use. Week 2 walks one floor down, to the **protocols and runtimes** that make those primitives composable across tools, teams, and product surfaces. Specifically: the **Model Context Protocol (MCP)** as the emerging standard for how models reach tools; **voice agents** as the most latency-sensitive, most adversarial deployment surface for everything Week 1 covered; and **n8n / workflow engines** as the low-code bridge most teams actually ship on.

By the end of the week you will be able to build an MCP server, argue specifically about MCP security (including the lethal-trifecta attack surface that MCP inherently expands), design a voice agent's latency budget from STT through TTS, and decide when n8n beats a LangGraph or custom-code approach for a given workflow.

## Who this week is for

You have finished Week 0 and Week 1. You can articulate why post-training is a thin coat of paint on a document simulator, you can name what SWE-bench Verified measures and what it hides, and you have a working mental model of prompting from mechanism. This week is for turning that foundation into **agent engineering** — the discipline of picking the right runtime for a given problem.

## Shape of the week

| Day | Topic | Shape |
|-----|-------|-------|
| Mon | MCP as a protocol — why a protocol, clients/servers/transports, resources/tools/prompts/sampling | Deep-dive + teardown |
| Tue | Building an MCP server — server surface, tool design, schema, auth, deployment | Deep-dive + build |
| Wed | MCP security — lethal trifecta through MCP tools, prompt injection via tool output, sandboxing, real incidents | Deep-dive + threat model exercise |
| Thu | Voice agents — STT/TTS, streaming, latency budget, turn-taking, interruption, emotion | Deep-dive + latency experiment |
| Fri | n8n for agent workflows — workflow engine shape, AI + MCP nodes, tradeoffs vs LangGraph / Temporal / custom | Deep-dive + build |
| Sat | Agent fundamentals revisited — ReAct deeper, planning vs execution, memory strategies, TAU-bench / BFCL evidence | Deep-dive + eval experiment |
| Sun | Synthesis, quiz, flashcards | Review |

## Why these topics belong together

MCP, voice, and n8n look like three unrelated tools. They are not. They are three different answers to the same question: *"How do I let a language model act in the world without writing a bespoke integration every time?"*

- **MCP** answers it via a standard protocol: one spec that Claude Code, Cursor, OpenAI desktop app, and others all implement, so a tool you build once runs everywhere. As of December 2025 MCP is no longer an Anthropic-led artifact — it was donated to the Linux Foundation's new Agentic AI Foundation, which now co-governs it alongside Google's A2A, Block's goose, and AGENTS.md.
- **Voice** answers it via a streaming, low-latency runtime: the agent loop has to close the turn fast enough that a human doesn't interrupt, which forces every other design decision.
- **n8n** answers it via a visual workflow engine: teams that cannot staff a Python engineer still need to ship automations, and n8n's AI + MCP nodes are where that happens in 2025–2026.

Understanding all three is what separates "can use an agent" from "can architect an agent product."

## What "L3 depth" means this week

Every deep-dive engages: (1) at least one live controversy — MCP security boundaries, voice-agent emotion benchmarks, workflow-vs-code tradeoffs; (2) at least three post-2024-01 citations — MCP spec releases, voice-stack benchmarks, TAU-bench / BFCL papers; (3) a runnable experiment via Claude Code or Claude.ai; (4) operator-level specifics with numbers; (5) a reviewer lens naming specific paragraphs a Willison, a Karpathy, a Huyen, a Liu, or an Anthropic security researcher would push back on.

## How to study this week

Same priority order as every other week: experiment first, Must-read citations second, problem set third, prose last. Saturday's live sessions on 2026-05-09 and 2026-05-10 are kickers, not the core — the vault lessons are.

_last_verified: 2026-07-17_
