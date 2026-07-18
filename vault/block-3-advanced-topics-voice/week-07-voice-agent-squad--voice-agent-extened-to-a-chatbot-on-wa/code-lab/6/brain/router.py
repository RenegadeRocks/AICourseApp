"""Intent -> specialist routing, shared by BOTH channels.

This is the 'brain' in one-brain/many-channels. Voice and WhatsApp both call
route() and both build the same handoff-state payload (Wednesday's typed
contract). The router itself knows nothing about audio, WhatsApp windows, or
latency masking — those are the adapters' jobs.

The classifier here is a keyword stub so the lab runs offline. In production
you replace classify() with a small-fast LLM call (Monday: never the big model
on the voice critical path). The handoff-state SCHEMA is the load-bearing part
and does not change when you swap the classifier.
"""
from __future__ import annotations

from dataclasses import dataclass, field, asdict
from typing import Literal

Intent = Literal["booking", "billing", "unknown"]


@dataclass
class HandoffState:
    """The typed cross-agent AND cross-channel contract (Wed + Fri).

    'sacred' fields are collected once and must NEVER be re-asked by a
    downstream specialist or a second channel. Re-ask rate is measured against
    exactly these.
    """
    intent: Intent = "unknown"
    phone: str = ""                      # sacred: identity, collected at entry
    name: str | None = None              # sacred once known
    entities_confirmed: dict = field(default_factory=dict)  # e.g. {"date": "Tue 14th"}
    identity_status: Literal["unverified", "identified", "verified"] = "unverified"
    attempted_steps: list[str] = field(default_factory=list)
    sentiment_flag: str | None = None

    def as_payload(self) -> dict:
        return asdict(self)


_BOOKING = {"book", "appointment", "reschedule", "cancel", "slot", "time", "date"}
_BILLING = {"bill", "balance", "invoice", "payment", "charge", "refund", "owe"}


def classify(text: str) -> Intent:
    t = text.lower()
    b = sum(w in t for w in _BOOKING)
    m = sum(w in t for w in _BILLING)
    if b == 0 and m == 0:
        return "unknown"
    return "booking" if b >= m else "billing"


def route(text: str, state: HandoffState) -> HandoffState:
    """Triage step: set intent on the shared state. Idempotent — re-running on a
    barge-in correction ('actually it's billing') updates intent WITHOUT
    dropping any sacred field already collected."""
    new_intent = classify(text)
    if new_intent != "unknown":
        state.intent = new_intent
    state.attempted_steps.append(f"triage:{new_intent}")
    return state
