# Code-lab 6 — Voice agent squad + WhatsApp extension

The Saturday build for Week 7. You will assemble a **triage → 2-specialist voice
squad** on a managed platform (Vapi or Retell), give it one real tool call, then
expose the **same agent brain** on WhatsApp via the Cloud API, and measure
end-to-end latency + containment against the [[06-sat-rag-evaluation|Week 4]]
eval discipline.

This lab is deliberately **config-and-glue**, not a from-scratch voice stack —
that is the whole point of Monday's platform-vs-parts lesson. The runnable code
here is the **shared brain**: a small FastAPI service that (a) exposes tools the
voice platform calls via webhook, (b) receives WhatsApp messages and voice notes
and routes them through the *same* tool logic, and (c) logs a per-turn event
stream you can compute latency and containment from.

> You are the tech lead. Claude Code is the integration engineer. Direct it;
> review its output against this README; do not paste-and-pray.

## What you build

```
                 ┌─────────────────────────────┐
   PSTN / web ──▶│ Vapi or Retell squad         │
                 │  triage → billing / booking   │──┐  tool webhooks
                 └─────────────────────────────┘  │
                                                    ▼
   WhatsApp  ───▶  WA Cloud API webhook ───▶  ┌──────────────────┐
   (text + voice note)                        │  brain/ (FastAPI) │
                                              │  tools + router    │
                                              │  event logger      │
                                              └──────────────────┘
                                                    │
                                                    ▼
                                              events.jsonl  ──▶  eval.py
```

The brain is channel-agnostic. The voice platform and the WA adapter are two
surfaces calling the same `tools/` and writing the same `events.jsonl`.

## Prerequisites

- Python 3.11+
- A **Vapi** or **Retell** account (both have free trial credit — pick one).
- A **Meta developer** account with a WhatsApp **test number** (free sandbox).
- **ngrok** or Cloudflare Tunnel to expose your local webhook to the internet.
- Optional: a Deepgram key if you want to run voice-note STT locally instead of
  relying on Meta's user-side transcription.

No API keys are committed. See `.env.example`.

## Setup

```bash
cd code-lab/6
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # fill in your keys
uvicorn brain.app:app --reload --port 8000
# in a second terminal:
ngrok http 8000             # copy the https URL for platform + WA webhooks
```

Then wire the two surfaces (full walkthrough in `SETUP.md`):

1. **Voice squad** — create the squad via the platform API using
   `configs/squad.vapi.json` (or `configs/squad.retell.json`). Point its tool
   webhook at `https://<ngrok>/tools`. The config **is code** — keep it in the
   repo, push via API, never hand-edit the console (Wednesday's Boris-Cherny
   rule).
2. **WhatsApp** — set the Cloud API webhook to `https://<ngrok>/wa/webhook`,
   verify token from `.env`, subscribe to `messages`.

## Run the graded exercises

```bash
# 1. Voice: place 3 calls (short factual / multi-step booking / mid-call barge-in)
#    events land in events.jsonl

# 2. WhatsApp: send 3 messages (text / a voice note / an out-of-window re-engage)

# 3. Compute the numbers:
python eval.py events.jsonl
#   -> first-audio p50/p95, interruption split, re-ask rate,
#      per-intent containment, per-channel behavior delta
```

## What "done" looks like

- The squad hands off triage → specialist **silently** (same voice, no re-greet)
  and the specialist never re-asks anything triage collected (re-ask rate 0).
- One real tool call (`lookup_appointment` against the bundled fake CRM) fires
  from the specialist, latency-masked with an acknowledge-then-work utterance.
- A barge-in **during** the handoff is handled without the agent ignoring the
  correction (test #3 — this is the one that breaks).
- The **same** `lookup_appointment` logic answers a WhatsApp text and a WhatsApp
  voice note, with the brain's reply **rendered per channel** (spoken sentence
  vs interactive button message).
- `eval.py` prints per-intent containment and a per-channel behavior delta, and
  every tool call went through the single audited chokepoint in `tools/gateway.py`
  (Thursday's guardrail).

## Files

- `brain/app.py` — FastAPI: `/tools` (voice platform webhook), `/wa/webhook`
  (WhatsApp), event logging.
- `brain/router.py` — intent → specialist logic (shared by both channels).
- `tools/gateway.py` — the single audited chokepoint; caps + confirmation gates.
- `tools/crm.py` — a fake in-memory CRM so the lab runs with zero external data.
- `channels/whatsapp.py` — the WA adapter: window state, media/voice-note
  fetch + STT, per-channel rendering.
- `configs/squad.vapi.json`, `configs/squad.retell.json` — the squad as code.
- `eval.py` — computes the Week-4-style metrics from `events.jsonl`.
- `SETUP.md` — the click-path for both platforms and the WA sandbox.
- `.env.example` — every key the lab reads, documented, none committed.

## Cost

Platform trial credit + WA test-number sandbox = **$0** to complete the lab.
A production version of this exact design is modeled in Friday's lesson
(~$500–700/month for a WA-first clinic with voice escalation).

## Safety note

`tools/gateway.py` ships with transacting tools **disabled** (`ALLOW_WRITES=false`).
The lab only reads the fake CRM. Turning writes on is left as a deliberate,
commented step so you implement Thursday's confirmation-read + hard-cap guardrails
before any tool can change state.
