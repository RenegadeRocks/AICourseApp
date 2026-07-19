"""AI status-summary endpoint logic (Tuesday lesson).

The design rule from the lesson: assemble the FACTS deterministically in code,
and let the model only phrase them. That keeps the summary grounded and makes
it impossible for the model to invent progress that did not happen.

Two modes:
  * offline (default): a deterministic template. Runs and tests with no API key.
  * online: calls Anthropic if ANTHROPIC_API_KEY is set and ``use_llm=True``.

Either way the output is a DRAFT for operator approval, never auto-sent.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from store import DashboardStore


@dataclass
class SummaryFacts:
    """Deterministically assembled facts. The model never sees anything else."""

    client_name: str
    project_names: list[str]
    statuses: list[str]
    reasons: list[str]
    shipped: list[str]
    blocked_on_client: list[str]
    metric_lines: list[str]


def assemble_facts(store: DashboardStore, caller_client_id: str) -> SummaryFacts:
    """Pull a tenant-scoped, structured snapshot. Pure data, no prose."""
    view = store.client_view(caller_client_id)
    progress = view["progress"]
    return SummaryFacts(
        client_name=view["client"]["name"],
        project_names=[p["project"] for p in progress],
        statuses=[p["status"] for p in progress],
        reasons=[p["reason"] for p in progress if p["reason"]],
        shipped=[
            d["name"] for d in view["deliverables"] if d["status"] == "approved"
        ],
        blocked_on_client=view["blocked_on_you"],
        metric_lines=[
            f"{m['label']}: {m['value']:g}{(' ' + m['unit']) if m['unit'] else ''}"
            for m in view["metrics"]
        ],
    )


def render_offline(facts: SummaryFacts) -> str:
    """Deterministic template summary. This is also the test oracle/fallback."""
    parts: list[str] = []
    status_word = _dominant_status(facts.statuses)
    parts.append(
        f"Hi {facts.client_name}, here is your update: work is {status_word}."
    )
    if facts.shipped:
        parts.append("Shipped since last update: " + ", ".join(facts.shipped) + ".")
    if facts.metric_lines:
        parts.append("Results so far: " + "; ".join(facts.metric_lines) + ".")
    if facts.blocked_on_client:
        parts.append(
            "We are waiting on you for: " + ", ".join(facts.blocked_on_client) + "."
        )
    else:
        parts.append("Nothing is blocked on your side right now.")
    return " ".join(parts)


def render_llm(facts: SummaryFacts) -> str:
    """Call Anthropic to phrase the SAME facts. Requires ANTHROPIC_API_KEY.

    The prompt supplies only ``facts`` and forbids adding anything not given,
    so the model phrases but cannot invent. Imported lazily so offline use and
    tests never need the SDK installed.
    """
    import anthropic  # lazy: only needed in online mode

    client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
    grounding = (
        f"client={facts.client_name}; projects={facts.project_names}; "
        f"statuses={facts.statuses}; reasons={facts.reasons}; "
        f"shipped={facts.shipped}; blocked_on_client={facts.blocked_on_client}; "
        f"metrics={facts.metric_lines}"
    )
    prompt = (
        "Write a warm, concise (max 3 sentences) client status update using "
        "ONLY the facts below. Do not add any progress, metric, or claim not "
        "present in the facts. If a section is empty, omit it.\n\n"
        f"FACTS:\n{grounding}"
    )
    message = client.messages.create(
        model=os.environ.get("SUMMARY_MODEL", "claude-haiku-4-5"),
        max_tokens=250,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


def generate_summary(
    store: DashboardStore, caller_client_id: str, use_llm: bool = False
) -> dict:
    """Return a DRAFT summary (never auto-sent) plus the facts it was built from."""
    facts = assemble_facts(store, caller_client_id)
    online = use_llm and bool(os.environ.get("ANTHROPIC_API_KEY"))
    text = render_llm(facts) if online else render_offline(facts)
    return {
        "status": "draft",  # operator must approve before the client sees it
        "mode": "llm" if online else "offline",
        "summary": text,
        "grounded_on": facts.__dict__,
    }


def _dominant_status(statuses: list[str]) -> str:
    if not statuses:
        return "getting started"
    if "blocked" in statuses:
        return "partly blocked"
    if "at_risk" in statuses:
        return "at risk on part of the work"
    return "on track"
