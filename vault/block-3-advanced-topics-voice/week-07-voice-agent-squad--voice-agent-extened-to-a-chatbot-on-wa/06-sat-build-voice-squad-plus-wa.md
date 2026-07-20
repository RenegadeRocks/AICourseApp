---
type: lesson
block: block-3-advanced-topics-voice
week: week-07
day_of_cycle: 6
day_name: sat
session_slug: voice-agent-extened-to-a-chatbot-on-wa
date_due: 2026-07-04
tags: [build-day, voice-agent-squad, whatsapp, vapi, retell, cloud-api, one-brain-many-channels, tool-calling, latency-measurement, containment, eval-harness, webhook-glue]
sources:
  - vapi-squads-docs-2026
  - retell-conversation-flow-2026
  - meta-audio-messages-docs
  - deepgram-flux-events-2026
  - anthropic-building-effective-agents-2024
  - hamel-husain-evals-faq-2026
  - twilio-conversationrelay-flux-2026
  - meta-service-message-pricing-2026
last_verified: 2026-07-17
word_count_target: 5000
---

# BUILD: the voice agent squad + WhatsApp extension — one brain, two surfaces, measured

## Why this matters

Today you ship the week, not describe it. By the end you will have a **triage → billing/booking voice squad** running on a real platform, making a real tool call with latency masking, plus the **same agent brain** answering WhatsApp text *and* voice notes, with a per-turn event stream you turn into latency and containment numbers. This is Block 3's first end-to-end voice production artifact, and Week 8's automation-hybrid week assumes it exists.

The delta that survives past the demo (the thing this build installs that a weekend hack skips) is the **seam between the channel-agnostic brain and the channel-specific adapters.** Mon–Fri argued for it; today you build it, and then you measure the two seams that break in practice (barge-in during a squad handoff; the same brain rendering differently per channel) so you have numbers, not vibes. The code is deliberately config-and-glue, per [[01-mon-the-2026-voice-stack|Monday's]] platform-vs-parts conclusion: you are the tech lead, Claude Code is the integration engineer, and the runnable Python is the shared brain in `code-lab/6/`.

## Prerequisites

- The whole week. Specifically: [[03-wed-the-voice-agent-squad|Wednesday's]] handoff-state schema, [[02-tue-conversation-engineering|Tuesday's]] five metrics + masking ladder, [[04-thu-voice-agent-trust-and-safety|Thursday's]] tool-guardrail gateway, [[05-fri-whatsapp-the-chatbot-extension|Friday's]] adapter contract.
- The running artifact you've built across the week (Mon vendor sheet → Tue conversation spec → Wed squad spec → Fri channel-extension spec). Today's build *is* those specs, executed.
- Accounts: one voice platform (Vapi or Retell; free trial credit), a Meta WhatsApp **test number** (free), ngrok. Total spend to complete: **$0**.
- [[06-sat-build-the-weekly-report-generator|Week 5 Sat]] and [[06-sat-rag-evaluation|Week 4 Sat]]: the build-day rhythm and the eval discipline; today reuses both.

## Layer 1 — The architecture you're about to type

One diagram, then the build. The **brain** (`code-lab/6/brain/` + `tools/`) is channel-agnostic: a FastAPI service exposing tools the voice platform calls by webhook, and a WhatsApp webhook that routes messages through the *same* tools. Two **surfaces** call it: the voice squad (Vapi/Retell) and the WA adapter. One **event stream** (`events.jsonl`) feeds `eval.py`.

```
   PSTN/web ─▶ Vapi/Retell squad ─┐ tool webhook
                                   ├─▶ brain (FastAPI): router + gateway + CRM
   WhatsApp ─▶ /wa/webhook  ───────┘         │
   (text + voice note)                       ▼
                                        events.jsonl ─▶ eval.py
```

Three design commitments the code enforces, each a Mon–Fri lesson made executable:

- **The router is shared** (`brain/router.py`): triage classifies, builds the typed `HandoffState`, and both channels consume it. Swap the keyword stub for a small-fast LLM later without touching the schema; Monday's "big model via tool call, never inline" holds.
- **Every tool call goes through one gateway** (`tools/gateway.py`): reads always allowed, writes dead until you implement Thursday's confirmation-read + hard caps. This is the audited chokepoint; a squad that lets any specialist hit the CRM directly has no audit trail and no kill switch.
- **The WA adapter owns channel physics** (`channels/whatsapp.py`): 24-hour window state, voice-note media fetch + STT, and per-channel rendering (a spoken sentence on voice becomes an interactive button message on WhatsApp, which is also, after October 1, a [[05-fri-whatsapp-the-chatbot-extension|cost lever]]).

## Layer 2 — Build phases (timed)

Treat this as a shipping diary. Full click-path is in `code-lab/6/SETUP.md`; the phases below are the tech-lead view.

**Phase 0: brain offline (10 min).** `uvicorn brain.app:app --port 8000`, then curl `/tools` with a fake transcript. You should get a booking reply referencing "Tue 14th, 3:00pm" *before any vendor is involved.* This proves router + gateway + fake CRM work in isolation. The discipline is: never debug the brain and the platform at the same time. If Phase 0 fails, it's Python; if a later phase fails, it's webhooks.

**Phase 1: the voice squad (45 min).** On Vapi: replace `<NGROK>` in `configs/squad.vapi.json`, POST it to `/squad`, attach the trial number. The config is three assistants (triage + booking + billing) with **silent** handoffs (same Cartesia voice, no re-greet) and one tool per specialist pointed at your `/tools` webhook. On Retell: create the conversation-flow agent from `configs/squad.retell.json` instead. Direct Claude Code to do the API calls and report back the squad ID; you review that the handoff destinations and tool URLs are right. Note what you're *not* doing: writing barge-in handling, retry logic, or telephony glue; the platform owns those, which is the whole reason [[01-mon-the-2026-voice-stack|Monday]] said start managed.

**Phase 2: three calls (20 min).** Place them deliberately:
1. *"What's my appointment?"* from +919000000001: clean triage→booking→tool→answer. Watch `events.jsonl`.
2. A multi-step booking; confirm the specialist never re-asks your name (re-ask rate 0).
3. **Interrupt during the handoff**: as triage hands to booking, say *"actually it's about my bill."* This is Wednesday's hardest seam. Grade by hand: did billing pick up cleanly, or did the agent ignore you / re-ask / lose the thread? This one test is worth more than the other two combined.

**Phase 3: the WhatsApp surface (30 min).** Wire the Cloud API test number's webhook to `/wa/webhook` with your verify token. Message it three ways: a text ("what's my balance"), a **voice note** (speak "reschedule my appointment"; the adapter uses Meta's transcription or your Deepgram key), and, if you can wait or simulate, an out-of-window re-engagement. Confirm the *same* `lookup_balance` logic answered all of them, and that the reply came back **rendered for WhatsApp** (interactive buttons, not a spoken sentence). This is one-brain/many-channels working: you added a channel without adding a bot.

**Phase 4: measure (20 min).** `python eval.py events.jsonl`. Read the five server-side numbers (tool latency p50/p95 per channel, re-ask count, reroute handling, per-intent containment, per-channel behavior delta). Then paste the platform dashboard's **first-audio p50/p95** for your three calls into your writeup; [[02-tue-conversation-engineering|Tuesday]] warned that first-audio is measured client-side by the platform, not your server; the eval script owns everything else. Grade the barge-in recovery. Write 400 words: what broke, what surprised you, what v2 changes.

## Layer 3 — What "done" looks like, and the three things that will break

**Done:** silent handoff with re-ask rate 0; one masked tool call from the specialist; barge-in-during-handoff handled; the same tool logic answers a WA text and a WA voice note with per-channel rendering; `eval.py` prints per-intent containment; every tool call went through the gateway.

**The three predictable breakages** (name them before they bite):

1. **The handoff barge-in (Phase 2, call 3).** The half-committed seam (audio landing on a session whose instructions are mid-swap) is where platforms differ most and where "it ignored me" lives. If Vapi's silent handoff drops your correction, that's the platform's atomicity behavior, and the fix is either an announced handoff (slower, but the seam is explicit) or restructuring so triage holds the call until intent is firmly set. Either way: you now have direct experience of Wednesday's theory.

2. **Per-channel rendering drift.** The same brain that says one crisp sentence on voice can dump a wall of text on WhatsApp if you let the model render freely. The adapter's `render()` function is the guardrail: it forces buttons and short bodies. If your WA replies look like voice transcripts, the rendering layer is too thin, which is exactly [[05-fri-whatsapp-the-chatbot-extension|Chip Huyen's Friday critique]]: one brain in the repo is not one brain in production behavior.

3. **Webhook payload shape.** Vapi and Retell nest the transcript/caller/call-id differently, and Meta's webhook is a deep `entry[0].changes[0].value.messages[0]`. The brain reads normalized subsets with fallbacks; if a call produces empty `events.jsonl`, it's almost always the payload path, not the logic. Debug with the platform's webhook-log viewer, not by re-reading `router.py`.

## Layer 4 — Grade it like Week 4, not like a demo

A demo that "worked" is not a shipped agent. Apply [[06-sat-rag-evaluation|Week 4's]] gate discipline to what you built:

- **Containment, per intent, not global.** Your `eval.py` breaks it down. A booking specialist at 90% and a billing specialist at 30% is a *healthier* signal than a flat 60%; it tells you exactly where to work (Tuesday). Don't report the average.
- **Containment paired with resolution.** The lab's `contained` flag is "found the record and answered", a proxy. For real deployment, add a resolution check (did the caller's actual goal complete?) or you'll ship the deflection trap [[05-fri-case-study-customer-support-agent|Week 3]] and [[02-tue-conversation-engineering|Tuesday]] both warned about.
- **The barge-in recovery is a labeled eval row.** Your hand-grade of Phase 2 call 3 is the first entry in an IHBench-style regression set. Save the transcript; it's the seed of the thing that catches your next handoff regression.
- **Log the handoff payload** (the gateway already logs tool calls; extend it to dump `HandoffState` at each handoff). When a specialist flounders, diff what it knew against what triage knew — [[03-wed-the-voice-agent-squad|Wednesday's Lilian Weng critique]] made concrete.

Hamel Husain's discipline applies verbatim: you don't write the full rubric before you have failures; you *generate* failures (the three deliberate calls), analyze them, and let the rubric grow from what actually broke.

## Common mistakes experts see

1. **Debugging brain and platform simultaneously.** Phase 0 exists to prevent this. Prove the brain offline first.
2. **Letting each specialist hit the CRM directly.** No gateway = no audit trail, no caps, no kill switch. Every tool call through `tools/gateway.py`, always.
3. **Skipping the barge-in call because the first two worked.** Call 3 is the one that teaches. The demo-happy path is not the lesson.
4. **Building a WA prompt separate from the voice prompt.** The moment you copy the system prompt into a "WhatsApp version," the drift clock starts. One brain; the adapter renders.
5. **Reporting global containment.** Averages hide the specialist that's failing. Per-intent or it's theater.
6. **Committing the `.env` or the sandbox token.** The 24h WA token and platform keys are secrets. `.env` is gitignored for a reason; check before you push.
7. **Flipping `ALLOW_WRITES=true` to "just test reschedule."** Writes are dead by design until you implement Thursday's confirmation-read. The one time you shortcut it is the one time an injected voice note reschedules a stranger's appointment.

## Reflection questions

1. Your Phase 2 call 3 (barge-in during handoff) either worked or didn't on your platform. Whichever happened, explain the mechanism, and design the one config change that would flip the outcome. What does that change cost you elsewhere?
2. The lab's `contained` flag is a proxy for real resolution. Write the concrete resolution check for the booking intent — what observable event proves the caller's goal completed?
3. You added WhatsApp without adding a bot. Name the single line of code that most makes that true, and the single design decision that would have made it false.
4. After October 1, 2026, your WA agent's per-contact cost scales with messages sent. Which function in the lab is your cost lever, and what one-line change to it halves message count without hurting UX?
5. If you had to expose this same brain on a third channel (SMS, or WhatsApp-native calls), what exactly do you write, and what do you reuse unchanged? The ratio of the two is the value of the architecture.

## My take (reviewer lens)

**Seibel** would time-box the whole thing: "This is a four-hour build with three real calls and three WhatsApp messages. If it takes you a day, you're gold-plating." Right: the phases are timed for exactly that pressure, and the trap is Phase 1 config fiddling. Ship the ugly working version, measure, iterate; the writeup matters more than a pretty squad graph.

**Boris Cherny** would inspect the config discipline: the squad is created *via API from a repo file*, not hand-edited in the console, so it diffs and rolls back, but the lab stops short of CI. His upgrade: a smoke test that recreates the squad and replays the three calls on every config change, so a triage-prompt tweak can't silently regress the handoff contract. That's the right v2, and it's the same fleet-management instinct from Wednesday.

**Hamel Husain** would police the eval claim: printing containment is not evaluating: the numbers are meaningless until the `contained` proxy is validated against what you'd actually call a resolved call, and until the barge-in grade is calibrated across more than one run. He'd say the build's real deliverable isn't the running agent, it's the three failure transcripts and the growing regression set; the agent is just what generates them. Correct, and it's why Layer 4 frames the day as failure-generation, not demo-completion.

## Further reading

**Must-read**
- `code-lab/6/README.md` + `SETUP.md`: the actual build; read both before starting.
- Vapi Squads docs / Retell conversation-flow docs: the platform primitives Phase 1 uses.[^1][^2]
- Meta audio-messages docs: the voice-note path in Phase 3.[^3]

**Recommended**
- Anthropic, *Building Effective Agents*: re-read the routing pattern as you build it.[^5]
- Hamel Husain, evals FAQ: failure-analysis-first, the discipline behind Layer 4.[^6]

**Optional**
- Twilio ConversationRelay + Flux: if you'd rather build the voice surface on Twilio than a managed platform, this is the path.[^7]
- Friday's service-message pricing analysis: re-run your per-contact P&L with the numbers your build now makes real.[^8]

## Citations

[^1]: Vapi, Squads + handoff docs, https://docs.vapi.ai/squads and https://docs.vapi.ai/squads/silent-handoffs — squad creation, silent handoffs, tool webhooks (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^2]: Retell, conversation-flow + multi-prompt docs, https://docs.retellai.com/build/single-multi-prompt/prompt-overview and https://www.retellai.com/blog/unlocking-complex-interactions-with-retell-ais-conversation-flow (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^3]: Meta for Developers, "Audio messages," https://developers.facebook.com/documentation/business-messaging/whatsapp/messages/audio-messages — voice-note media-id → download → transcription flow (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^4]: Deepgram Flux turn events (for the optional Twilio/ConversationRelay path), https://developers.deepgram.com/docs/flux/quickstart (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^5]: Anthropic, *Building Effective AI Agents* (December 2024), https://www.anthropic.com/research/building-effective-agents — routing/orchestration patterns (Tier-1, stable).

[^6]: Hamel Husain, LLM evals FAQ, https://hamel.dev/blog/posts/evals-faq/ — failure-analysis-first eval discipline (Tier-1, stable).

[^7]: Twilio, ConversationRelay + Flux, https://www.twilio.com/en-us/products/conversational-ai/conversationrelay and https://www.twilio.com/en-us/changelog/conversation-relay-now-supports-deepgram-flux---new-features (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

[^8]: WhatsApp service-message pricing change (2026-10-01), Meta developer docs + BSP analyses per [[05-fri-whatsapp-the-chatbot-extension|Friday]] citations (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending).

_last_verified: 2026-07-17_
