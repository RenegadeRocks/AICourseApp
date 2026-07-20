"""The single audited chokepoint for every tool call, from every channel.

Thursday's guardrail, made concrete: reads are always allowed; writes are gated
behind ALLOW_WRITES *and* a per-call confirmation flag *and* hard caps. The
prompt is advisory; this wrapper is law. Every call — voice or WhatsApp — is
logged here, so the audit trail is channel-agnostic and complete.
"""
from __future__ import annotations

import os
import time
from typing import Any, Callable

from . import crm

ALLOW_WRITES = os.getenv("ALLOW_WRITES", "false").lower() == "true"

# Hard caps live in code, not in the prompt (Thursday, Layer 5).
MAX_WRITES_PER_CONVERSATION = 2
MAX_RESCHEDULES_PER_DAY = 50

# name -> (callable, is_write)
_REGISTRY: dict[str, tuple[Callable[..., dict], bool]] = {
    "lookup_appointment": (crm.lookup_appointment, False),
    "lookup_balance": (crm.lookup_balance, False),
    "reschedule_appointment": (crm.reschedule_appointment, True),
}

# crude in-process counters; a real deployment uses a store keyed on conversation id
_write_counts: dict[str, int] = {}


class GuardrailError(Exception):
    pass


def call_tool(
    name: str,
    args: dict[str, Any],
    *,
    conversation_id: str,
    channel: str,
    confirmed: bool = False,
    log: Callable[[dict], None] | None = None,
) -> dict:
    """Execute a tool through the guardrail. Returns the tool result dict.

    channel: "voice" | "whatsapp" (recorded for the per-channel audit).
    confirmed: must be True for write tools (set only after a confirmation-read).
    """
    if name not in _REGISTRY:
        raise GuardrailError(f"unknown tool: {name}")
    fn, is_write = _REGISTRY[name]

    if is_write:
        if not ALLOW_WRITES:
            raise GuardrailError("writes disabled (ALLOW_WRITES=false)")
        if not confirmed:
            # The agent must read back parameters and get explicit assent first.
            raise GuardrailError("write requires prior confirmation-read")
        used = _write_counts.get(conversation_id, 0)
        if used >= MAX_WRITES_PER_CONVERSATION:
            raise GuardrailError("per-conversation write cap reached")
        _write_counts[conversation_id] = used + 1

    t0 = time.time()
    result = fn(**args)
    dt_ms = int((time.time() - t0) * 1000)

    if log is not None:
        log(
            {
                "type": "tool_call",
                "ts": time.time(),
                "conversation_id": conversation_id,
                "channel": channel,
                "tool": name,
                "is_write": is_write,
                "confirmed": confirmed,
                "latency_ms": dt_ms,
                # NB: do not log raw PII args in production; redact per Thursday.
                "args_keys": sorted(args.keys()),
                "ok": result.get("ok", result.get("found", True)),
            }
        )
    return result
