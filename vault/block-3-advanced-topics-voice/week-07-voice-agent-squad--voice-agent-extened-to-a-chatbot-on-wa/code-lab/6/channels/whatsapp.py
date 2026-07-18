"""The WhatsApp adapter (Friday's Layer 3, made concrete).

Owns the four channel-specific responsibilities the brain must NOT know about:
  1. 24-hour window state (free-form vs template-only)
  2. modality rendering (persistent text + interactive buttons, no latency crisis)
  3. identity bridge (WA number == the CRM key)
  4. media handling (voice note -> media id -> download -> STT -> transcript)

The brain gives this adapter an intent + a reply; the adapter decides HOW to put
it on WhatsApp.
"""
from __future__ import annotations

import os
import time
import httpx

GRAPH = "https://graph.facebook.com/v21.0"


def window_open(last_user_msg_ts: float | None) -> bool:
    """True if the 24-hour customer-service window is open. Outside it, only
    approved template messages may be sent (Friday, Layer 1). The adapter checks
    this before EVERY send; the brain never has to."""
    if last_user_msg_ts is None:
        return False
    return (time.time() - last_user_msg_ts) < 24 * 3600


async def fetch_media_text(media_id: str, token: str, deepgram_key: str | None) -> str:
    """Voice-note path: resolve the temporary URL, download the .ogg, transcribe.

    Media URLs expire fast — download promptly (Friday, mistake #7). If you have
    no Deepgram key, rely on Meta's user-side transcription instead (delivered in
    the webhook payload) and skip this call.
    """
    async with httpx.AsyncClient(timeout=30) as c:
        meta = (await c.get(f"{GRAPH}/{media_id}",
                            headers={"Authorization": f"Bearer {token}"})).json()
        url = meta["url"]
        audio = (await c.get(url, headers={"Authorization": f"Bearer {token}"})).content

    if not deepgram_key:
        # Caller should fall back to the webhook's transcription field.
        raise RuntimeError("no DEEPGRAM_API_KEY; use Meta user-side transcription")

    # Treat the transcript as UNTRUSTED input (Thursday: voice notes are an
    # injection surface just like live audio).
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            "https://api.deepgram.com/v1/listen?model=nova-3&smart_format=true",
            headers={"Authorization": f"Token {deepgram_key}",
                     "Content-Type": "audio/ogg"},
            content=audio,
        )
    j = r.json()
    return j["results"]["channels"][0]["alternatives"][0]["transcript"]


async def send_text(to: str, body: str, token: str, phone_number_id: str) -> dict:
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"{GRAPH}/{phone_number_id}/messages",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json={"messaging_product": "whatsapp", "to": to,
                  "type": "text", "text": {"body": body}},
        )
    return r.json()


async def send_buttons(to: str, body: str, options: list[str],
                       token: str, phone_number_id: str) -> dict:
    """Per-channel rendering: one interactive message replaces several clarifying
    turns. After Oct 1, 2026 this is also a COST lever (Friday, Layer 2) — fewer
    billed messages per contact."""
    buttons = [{"type": "reply", "reply": {"id": f"opt_{i}", "title": o[:20]}}
               for i, o in enumerate(options[:3])]
    async with httpx.AsyncClient(timeout=30) as c:
        r = await c.post(
            f"{GRAPH}/{phone_number_id}/messages",
            headers={"Authorization": f"Bearer {token}",
                     "Content-Type": "application/json"},
            json={"messaging_product": "whatsapp", "to": to,
                  "type": "interactive",
                  "interactive": {"type": "button",
                                  "body": {"text": body},
                                  "action": {"buttons": buttons}}},
        )
    return r.json()


def render(intent: str, tool_result: dict) -> tuple[str, list[str]]:
    """Channel-aware rendering of a brain reply for WhatsApp. Returns
    (body, button_options). The SAME tool_result rendered for voice would be a
    single spoken sentence with latency masking; here it's persistent text +
    buttons and there is no 800ms clock (Friday, Layer 3)."""
    if intent == "booking" and tool_result.get("found"):
        body = (f"Hi {tool_result['name']}, your next appointment is "
                f"{tool_result['when']} with {tool_result['provider']}. "
                f"What would you like to do?")
        return body, ["Confirm", "Reschedule", "Talk to a person"]
    if intent == "billing" and tool_result.get("found"):
        due = tool_result["balance_due"]
        if due == 0:
            return f"Hi {tool_result['name']}, your balance is clear. Anything else?", []
        return (f"Hi {tool_result['name']}, your balance due is ₹{due:.0f}.",
                ["Pay now", "Payment plan", "Talk to a person"])
    return "I couldn't find your record — can you share the number on file?", []
