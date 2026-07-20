"""The shared brain: one FastAPI service, two surfaces.

  POST /tools        <- voice platform (Vapi/Retell) tool webhook
  GET/POST /wa/webhook <- WhatsApp Cloud API webhook (verify + messages)

Both surfaces route through brain.router and tools.gateway and append to the
same events.jsonl. That single event stream is what eval.py turns into
latency + containment + per-channel numbers.
"""
from __future__ import annotations

import json
import os
import time

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Response

from .router import HandoffState, route
from tools import gateway
from channels import whatsapp as wa

load_dotenv()
app = FastAPI(title="week7-brain")

EVENTS_PATH = os.getenv("EVENTS_PATH", "events.jsonl")
WA_TOKEN = os.getenv("WA_ACCESS_TOKEN", "")
WA_PHONE_ID = os.getenv("WA_PHONE_NUMBER_ID", "")
WA_VERIFY = os.getenv("WA_VERIFY_TOKEN", "changeme")
DG_KEY = os.getenv("DEEPGRAM_API_KEY") or None

# conversation_id -> (HandoffState, last_user_msg_ts)
_SESSIONS: dict[str, tuple[HandoffState, float]] = {}


def log_event(ev: dict) -> None:
    ev.setdefault("ts", time.time())
    with open(EVENTS_PATH, "a") as f:
        f.write(json.dumps(ev) + "\n")


def _handle(text: str, phone: str, conversation_id: str, channel: str) -> dict:
    """Channel-agnostic core: triage -> specialist -> tool. Returns
    {intent, tool_result, contained}. Adapters render the reply."""
    state, _ = _SESSIONS.get(conversation_id, (HandoffState(phone=phone), 0.0))
    if not state.phone:
        state.phone = phone

    prev_intent = state.intent
    state = route(text, state)

    # A barge-in correction ('actually it's billing') re-routes WITHOUT losing
    # sacred fields — this is the seam Wednesday warns about; test #3 hits it.
    tool_result: dict = {}
    if state.intent == "booking":
        tool_result = gateway.call_tool(
            "lookup_appointment", {"phone": phone},
            conversation_id=conversation_id, channel=channel, log=log_event)
    elif state.intent == "billing":
        tool_result = gateway.call_tool(
            "lookup_balance", {"phone": phone},
            conversation_id=conversation_id, channel=channel, log=log_event)

    # Re-ask detection: when a lookup against the sacred phone field fails,
    # BOTH adapters render the fallback that asks the user to re-supply "the
    # number on file". That is a re-ask of a sacred field the brain already
    # holds (router.HandoffState), so it counts against the target-0 metric
    # eval.py reports. Intent=unknown asks nothing, so it does not count.
    reask = (
        state.intent in ("booking", "billing")
        and bool(state.phone)
        and not tool_result.get("found", False)
    )

    # containment = handled without asking for a human
    contained = tool_result.get("found", False)

    log_event({
        "type": "turn",
        "conversation_id": conversation_id,
        "channel": channel,
        "intent": state.intent,
        "reroute": prev_intent != "unknown" and prev_intent != state.intent,
        "reask": reask,
        "contained": contained,
    })
    _SESSIONS[conversation_id] = (state, time.time())
    return {"intent": state.intent, "tool_result": tool_result, "contained": contained}


@app.post("/tools")
async def voice_tools(req: Request) -> dict:
    """Vapi/Retell call this when the squad invokes a tool. Payload shape varies
    by platform; SETUP.md shows the mapping. We read a normalized subset."""
    body = await req.json()
    # Normalize across platforms (SETUP.md documents each platform's real shape).
    text = body.get("message", {}).get("text") or body.get("transcript", "")
    phone = body.get("customer", {}).get("number") or body.get("from", "")
    conv = body.get("call", {}).get("id") or body.get("call_id", "voice-unknown")

    # first-audio latency is measured client-side by the platform; here we log the
    # tool round-trip so eval.py can attribute per-turn tool latency.
    out = _handle(text, phone, conv, channel="voice")
    # The squad's specialist speaks this; keep it to one masked sentence (Tue).
    tr = out["tool_result"]
    if out["intent"] == "booking" and tr.get("found"):
        say = f"Let me check — you're set for {tr['when']} with {tr['provider']}."
    elif out["intent"] == "billing" and tr.get("found"):
        say = (f"One moment — your balance is clear." if tr["balance_due"] == 0
               else f"One moment — your balance due is {tr['balance_due']:.0f} rupees.")
    else:
        say = "I couldn't find your record — what's the number on file?"
    return {"result": say, "intent": out["intent"], "contained": out["contained"]}


@app.get("/wa/webhook")
async def wa_verify(req: Request) -> Response:
    """Meta webhook handshake."""
    p = req.query_params
    if p.get("hub.mode") == "subscribe" and p.get("hub.verify_token") == WA_VERIFY:
        return Response(content=p.get("hub.challenge", ""), media_type="text/plain")
    return Response(status_code=403)


@app.post("/wa/webhook")
async def wa_incoming(req: Request) -> dict:
    body = await req.json()
    try:
        entry = body["entry"][0]["changes"][0]["value"]
        msg = entry["messages"][0]
    except (KeyError, IndexError):
        return {"status": "ignored"}  # status callbacks etc.

    phone = msg["from"]
    conv = f"wa-{phone}"
    # Meta sends the user-message timestamp as epoch seconds (string). This is
    # what starts/refreshes the 24h window; fall back to now for sandbox tools
    # that omit it.
    try:
        msg_ts = float(msg.get("timestamp", time.time()))
    except (TypeError, ValueError):
        msg_ts = time.time()

    if msg["type"] == "text":
        text = msg["text"]["body"]
    elif msg["type"] == "audio":
        # voice note: prefer Meta's transcription if present, else STT ourselves
        if "transcription" in msg.get("audio", {}):
            text = msg["audio"]["transcription"]
        else:
            text = await wa.fetch_media_text(msg["audio"]["id"], WA_TOKEN, DG_KEY)
        log_event({"type": "voice_note_stt", "conversation_id": conv,
                   "channel": "whatsapp"})
    else:
        text = "(unsupported message type)"

    out = _handle(text, phone, conv, channel="whatsapp")
    body_text, options = wa.render(out["intent"], out["tool_result"])

    # Adapter decides HOW to render: buttons if options exist (fewer billed
    # messages after Oct 1 — Friday, Layer 2), else plain text. Every send goes
    # through the adapter's 24h-window check; a closed window (e.g. a delayed
    # replay of an old webhook) is a logged, non-retried event, not a send.
    try:
        if options:
            await wa.send_buttons(phone, body_text, options, WA_TOKEN,
                                  WA_PHONE_ID, last_user_msg_ts=msg_ts)
        else:
            await wa.send_text(phone, body_text, WA_TOKEN, WA_PHONE_ID,
                               last_user_msg_ts=msg_ts)
    except wa.WindowClosedError as e:
        log_event({"type": "window_closed_block", "conversation_id": conv,
                   "channel": "whatsapp", "detail": str(e)})
        return {"status": "window_closed", "intent": out["intent"],
                "error": "24h window closed; template message required"}
    return {"status": "ok", "intent": out["intent"]}


@app.get("/health")
async def health() -> dict:
    return {"ok": True, "writes_enabled": gateway.ALLOW_WRITES}
