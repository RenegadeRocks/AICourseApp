# Week 7 briefs — Voice Agent Squad + WhatsApp Chatbot Extension

Curriculum sessions: "Voice Agent squad" + "Voice agent Extended to a Chatbot
on WA". July-2026 interpretation: production voice agents on the current stack
(OpenAI Realtime-2, Cartesia Sonic 3.5, Deepgram Flux/Aura-2, ElevenLabs v3,
VAPI/Retell platforms — verify all current), multi-agent squads with routing/
handoff, and omnichannel extension to WhatsApp. b0w02 thu taught voice
*architecture* fundamentals — wikilink it; this week is the production build
course. Do not re-teach the latency-budget basics; deepen them.

Day plan:

- **01-mon — The 2026 voice stack, vendor by vendor.** Speech-to-speech vs
  cascaded (STT→LLM→TTS) in 2026: where each wins now; current latency/price
  table (verify every number); build-on-platform (VAPI/Retell) vs assemble-
  from-parts decision framework with real per-minute economics.
- **02-tue — Conversation engineering.** Turn-taking/endpointing (Flux-class
  models), interruption handling, backchanneling, latency budgets end-to-end,
  telephony (Twilio/SIP) vs web audio; failure modes that kill perceived
  quality and how to measure them.
- **03-wed — The voice agent squad.** Multi-agent voice: triage → specialist
  handoff, shared context across agents, squad topologies (router vs
  orchestrator), barge-in across handoffs, when a squad beats one bigger
  agent (and when it's ceremony — name the skeptic position). Tool-calling
  mid-call (bookings, lookups) with latency masking.
- **04-thu — Voice agent trust & safety.** Deepfake/voice-clone landscape and
  disclosure norms (verify current regulation: state AI-disclosure laws, EU AI
  Act Aug-2 applicability), prompt injection via audio, PII in transcripts,
  recording consent by jurisdiction (US one/two-party, India), guardrails for
  agents that can transact. Link b0w02 wed security + trifecta canonical.
- **05-fri — WhatsApp: the chatbot extension.** WA Business Platform in 2026
  (Cloud API — verify current pricing model: per-message categories, the
  2025-26 pricing changes), 24-hour session window + template messages,
  voice-note handling (STT on WA audio), one brain/many channels architecture:
  sharing the voice agent's context + tools with the WA text surface.
  India-market specifics (WA dominance) — the reader's likely first market.
- **06-sat — BUILD: voice agent squad + WA extension.** VAPI or Retell squad
  (triage + 2 specialists) with tool calls, then the same agent brain exposed
  on WA via Cloud API sandbox/Twilio; measure end-to-end latency + containment
  rate; eval per b2w04 sat discipline. code-lab for configs + webhook glue.
- **07-sun — Synthesis + quiz + flashcards.**

Controversies (verify current state): speech-to-speech vs cascaded for
production (positions moved in 2026); platform lock-in vs raw-stack control;
voice agents crossing the "don't pretend to be human" line — disclosure
debates; WA pricing changes squeezing chatbot economics.
