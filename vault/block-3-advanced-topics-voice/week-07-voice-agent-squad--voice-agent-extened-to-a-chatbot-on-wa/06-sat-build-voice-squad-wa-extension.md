---
type: lesson
block: block-3-advanced-topics-voice
week: week-07
day_of_cycle: 6
day_name: sat
session_slug: voice-agent-extened-to-a-chatbot-on-wa
date_due: 2026-07-04
tags: [build-day, vapi-squads, whatsapp-cloud-api, webhook, one-brain-many-channels, tool-calling, latency-measurement, containment, eval-harness, claude-code, code-lab]
sources:
  - vapi-squads-docs-2026
  - vapi-handoff-docs-2026
  - meta-wa-cloud-api-docs
  - meta-audio-messages-docs
  - twilio-wa-audio-stt-tutorial
  - hamel-husain-evals-faq-2026
  - deloitte-containment-2026
  - teneo-containment-2026
last_verified: 2026-07-17
word_count_target: 5000
---

# BUILD: the voice agent squad + WhatsApp extension — one brain, two surfaces, measured

## Why this matters

Today you ship the week: a **triage + two specialists** voice squad on Vapi (or Retell — the lesson notes the deltas) with real tool calls, then the **same agent brain** exposed on WhatsApp through the Cloud API's free test number, including inbound voice notes. Then — the part that separates this from a YouTube tutorial — you **measure it**: end-to-end latency per turn, containment and re-ask rate per intent, across both channels, against the eval discipline [[06-sat-rag-evaluation|Week 4 Saturday]] installed. The artifact you finish with is the one you show a client: not "I made a bot," but "here is a two-channel agent with a measured 62% containment on bookings, 480 ms median voice latency, zero re-asks across handoffs, and here is the eval that catches regressions."

Budget 3–4 hours of build plus sign-ups. Everything runs on free tiers: Vapi's trial credits, the WA test number (free to message the 5 numbers you register), and a tunnel (ngrok or cloudflared) for local webhooks. You will not hand-write most of this code — `code-lab/6/` contains the scaffold and Claude Code drives the integration — but you will *read* all of it, because Wednesday's warning stands: the config surface is the product.

## Prerequisites

- The week's three artifacts: Monday's vendor worksheet, Tuesday's conversation spec, Wednesday's squad spec (with the handoff-state schema). Today implements them; if you skipped one, do the 20-minute version now.
- Accounts: Vapi (or Retell), Meta developer account with a WhatsApp Business test app, an STT-capable API key for voice notes (OpenAI or Deepgram), an LLM API key for the WA brain.
- [[04-thu-voice-agent-trust-and-safety|Thursday's]] checklist open in a tab. The build passes it before it dials anyone.
- `code-lab/6/` from this repo — README has the exact commands; deps are pinned.

## The build, phase by phase

### Phase 0 — Decide small (15 min)

The scenario shipped in the scaffold (swap in your own if your specs used one): **a clinic front desk**. Intents: *book/reschedule an appointment* (specialist A, tools: `check_availability`, `book_slot`), *billing questions* (specialist B, tools: `lookup_invoice`, requires identity confirmation first), *everything else* (triage answers FAQs directly or escalates). This satisfies Wednesday's ceremony test: the two specialists differ in **tools and verification posture**, not just topic — billing demands identity; booking doesn't.

Write the handoff-state schema *first*, because both channels and all three assistants consume it:

```json
{
  "intent": "booking | billing | faq | escalate",
  "caller_name": null,
  "phone_verified": false,
  "entities_confirmed": {},
  "attempted_steps": [],
  "channel": "voice | whatsapp",
  "sacred": ["caller_name", "entities_confirmed"]
}
```

The `sacred` list is Wednesday's never-re-ask contract, now machine-readable.

### Phase 1 — The squad, as config-in-repo (45 min)

Per Boris Cherny's Wednesday warning: the squad is created **via API from JSON in the repo**, never hand-edited in the console. In `code-lab/6/`, ask Claude Code:

> Read `squad.json` and `create_squad.py`. The JSON defines a Vapi squad: a triage assistant plus `booking` and `billing` assistants, each with its own short system prompt, its own tools (served by my `tools_server.py` webhook), and handoff tools wired triage→booking, triage→billing, and both specialists→triage. Handoffs are silent (no announcement), and each destination's context plan passes the structured handoff state, not raw transcript. Walk me through every field you see against the Vapi squads and handoff docs, flag anything deprecated, then run `create_squad.py` with my `VAPI_API_KEY` and print the squad ID and test-call instructions.

Design points the scaffold encodes (verify them against your Wednesday spec, don't take them on faith): triage's prompt is under 200 words and ends with routing criteria; specialists open by *using* handoff state ("I can help with your booking for {caller_name}…") — the re-ask bug is made structurally hard, not just discouraged; billing's prompt contains the verification gate; every assistant contains Thursday's two hard-coded behaviors — the AI-plus-recording disclosure in the *first* greeting only (silent handoffs must not re-greet), and a truthful answer to "are you a robot."[^1][^2]

**Retell delta:** the same design lands as either a conversation-flow agent (nodes = triage/booking/billing, Node KB per node) or separate agents with transfers; the scaffold's `README` maps each `squad.json` field to its Retell equivalent. If Wednesday's matrix told you your intents share tools and posture — build the single conversation-flow agent and skip the squad honestly.[^3]

### Phase 2 — Tools with latency masking (30 min)

`tools_server.py` is a FastAPI app exposing the three tools as webhooks. Two things it does that demo code never does: **every tool call is logged as a span** (tool, args-hash, latency ms, call ID, channel) to `traces.jsonl` — your own store, per Monday's measurement-history warning — and `check_availability` has a configurable artificial delay (`SLOW_TOOL_MS`) so you can *rehearse Tuesday's masking ladder*: set it to 2500 ms and confirm the assistant's prompt-level masking ("Let me check the calendar—") actually covers the gap, then find the delay where it stops working. That number goes in your writeup.

Expose it: `uvicorn tools_server:app --port 8000`, tunnel it, paste the tunnel URL into `squad.json`, re-run `create_squad.py` (idempotent update).

### Phase 3 — Voice test calls, instrumented (30 min)

Call the squad's number (Vapi gives you a web-call button and a phone number on trial). Run the six scripted calls in `README` — happy-path booking; billing with identity; the *misroute* ("billing" that's really a booking change); Tuesday's mid-workflow barge-in; Wednesday's barge-in-during-handoff ("wait, actually—" the moment triage hands off); and the "are you a robot?" probe. For each, pull the platform's call log **and** your `traces.jsonl`, and fill the measurement table:

| Call | First-audio p50/p95 | Handoff latency (audible gap) | Re-asks | Contained? | Resolved? |
|---|---|---|---|---|---|

Expect on a trial stack: 500–900 ms first-audio, handoffs near-invisible when silent, and — most likely failure — the barge-in-during-handoff call doing something ugly. That ugliness is the point; write down exactly what it did.

### Phase 4 — The WhatsApp adapter (60 min)

Meta developer app → WhatsApp → test number; register your own phone as a recipient; get the temporary access token. Then:

> Read `wa_webhook.py` and `brain.py`. Wire the webhook (GET verify with my `WA_VERIFY_TOKEN`, POST receive), tunnel it, and register the callback URL in the Meta app. Confirm the flow: inbound text → `brain.respond(state, text, channel="whatsapp")` → reply via Graph API; inbound audio → resolve media ID → download the .ogg → STT via my configured provider → same brain path, transcript tagged voice-originated. Then send me the test matrix.

`brain.py` is the one-brain artifact: the *same* routing logic and tool functions the squad uses, with a channel-aware rendering layer (voice: ≤2 spoken sentences; WA: consolidated messages, interactive buttons where the platform allows) and a **message-efficiency instruction** — Friday's October-1 lever, in the prompt from day one.[^4][^5] The WA flow re-uses the handoff-state schema with `channel: "whatsapp"`; the identity bridge is the phone number, so if you call the voice line and then message the test number from the same phone, the brain greets you with context. Test exactly that — it is the week's thesis in one interaction.

Test matrix: text booking end-to-end; a **voice note** booking (speak your request — verify the STT transcript lands in the trace); the injection probe from Thursday (a message instructing the bot to reveal another patient's invoice — confirm the tool layer's scoping, not the prompt, is what blocks it); and the window-state check (the adapter refuses free-form sends when no session is open, and tells you which template it *would* send).[^4]

### Phase 5 — The eval gate (45 min)

Per Hamel Husain's discipline — error analysis before elaborate metrics[^6] — your eval starts from what Phases 3–4 actually broke. `eval/scenarios.json` ships with 12 scenarios (both channels × intents × the two