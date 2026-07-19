"""SOP-template generator.

Turns a structured task spec into a checklist-form Standard Operating Procedure
(Monday's SOP form: trigger + ordered checklist + definition of done + owner +
version), and recommends whether the procedure should be human-run or graduate
into an agent (Wednesday's SOP-to-agent rubric: frequency x determinism x cost
of error).

Pure standard library. Run:  python sop_generator.py
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from typing import Literal

Frequency = Literal["daily", "weekly", "monthly", "quarterly", "rare"]
Judgment = Literal["deterministic", "mixed", "judgment"]
ErrorCost = Literal["low", "medium", "high"]


@dataclass
class SOPSpec:
    """The minimum a runnable SOP needs to exist."""

    title: str
    trigger: str
    steps: list[str]
    definition_of_done: str
    owner: str
    inputs: list[str] = field(default_factory=list)
    failure_modes: list[str] = field(default_factory=list)
    a_grade_example: str = ""
    version: str = "1.0"
    last_reviewed: str = field(default_factory=lambda: date.today().isoformat())
    frequency: Frequency = "weekly"
    judgment: Judgment = "mixed"
    error_cost: ErrorCost = "medium"


# --- SOP-to-agent recommendation (Wednesday's rubric) -----------------------

def automation_recommendation(spec: SOPSpec) -> tuple[str, str]:
    """Return (verdict, reason) for whether this SOP should be agent-run.

    Rubric axes: frequency (payback), judgment (feasibility), error cost (safety).
    """
    freq_score = {"daily": 3, "weekly": 2, "monthly": 1, "quarterly": 0, "rare": 0}
    judgment_score = {"deterministic": 2, "mixed": 1, "judgment": 0}

    f = freq_score[spec.frequency]
    j = judgment_score[spec.judgment]

    if spec.judgment == "judgment":
        return ("HUMAN-RUN", "Judgment-defined task: an agent fills ambiguity with "
                "a confident wrong guess. Keep human.")
    if spec.error_cost == "high" and spec.judgment != "deterministic":
        return ("HUMAN-IN-THE-LOOP", "High cost of error with non-trivial judgment: "
                "agent may draft, human must gate before it ships.")
    if spec.judgment == "deterministic" and f >= 2:
        return ("AGENT-CANDIDATE", "Deterministic and high-frequency: strong "
                "automation payback. Write failure modes and stop conditions "
                "explicitly before handing to an agent.")
    if f + j >= 3:
        return ("AGENT-ASSIST", "Frequent and mostly rule-following: agent can "
                "produce the first draft, human keeps the judgment slice.")
    return ("HUMAN-RUN", "Low frequency or high judgment: automating it is not "
            "worth the build, or not safe. Keep human for now.")


# --- Renderer ---------------------------------------------------------------

def render_sop(spec: SOPSpec) -> str:
    """Render an SOPSpec as a checklist-form Markdown SOP."""
    verdict, reason = automation_recommendation(spec)
    lines: list[str] = []
    lines.append(f"# SOP: {spec.title}")
    lines.append("")
    lines.append(f"- **Owner:** {spec.owner}")
    lines.append(f"- **Version:** {spec.version}  |  **Last reviewed:** {spec.last_reviewed}")
    lines.append(f"- **Trigger:** {spec.trigger}")
    lines.append(f"- **Run mode:** {verdict} — {reason}")
    lines.append("")

    if spec.inputs:
        lines.append("## Inputs (have these before you start)")
        for item in spec.inputs:
            lines.append(f"- [ ] {item}")
        lines.append("")

    lines.append("## Procedure (checklist)")
    for i, step in enumerate(spec.steps, start=1):
        lines.append(f"- [ ] {i}. {step}")
    lines.append("")

    lines.append("## Definition of done")
    lines.append(spec.definition_of_done)
    lines.append("")

    if spec.a_grade_example:
        lines.append("## What an A-grade output looks like")
        lines.append(spec.a_grade_example)
        lines.append("")

    if spec.failure_modes:
        lines.append("## How this usually goes wrong (check for these)")
        for fm in spec.failure_modes:
            lines.append(f"- {fm}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def sop_from_dict(data: dict) -> SOPSpec:
    """Build an SOPSpec from a plain dict (e.g. parsed from JSON/YAML or an LLM)."""
    return SOPSpec(**data)


def _demo() -> None:
    onboarding = SOPSpec(
        title="New client kickoff",
        trigger="Client signs the contract",
        owner="Founder",
        inputs=["Signed contract confirmed in e-sign tool", "Client point-of-contact email"],
        steps=[
            "Add client to CRM with the 'active' tag",
            "Send welcome email from template W-1 (states first-value promise + intake form + kickoff link)",
            "Create client project in the tracker from template",
            "Provision the client dashboard",
            "Set a day-2 check that the intake form was submitted",
        ],
        definition_of_done=(
            "Client has booked the kickoff call AND submitted the intake form before day two, "
            "and can see live progress in their dashboard."
        ),
        a_grade_example="Welcome email out within 2 business hours; client booked kickoff same day; intake form complete.",
        failure_modes=[
            "Intake form sits unfilled and the kickoff call starts blind",
            "Welcome email delayed past the first day, so buyer's remorse sets in",
        ],
        frequency="weekly",
        judgment="mixed",
        error_cost="medium",
    )
    print(render_sop(onboarding))

    print("=" * 70)
    report = SOPSpec(
        title="Produce one monthly client report",
        trigger="First business day of the month",
        owner="Delivery lead",
        steps=[
            "Pull the month's metrics from connected sources",
            "Generate the narrative draft from metrics using the report template",
            "Add the 'what changed and why it matters' analysis",
            "Add recommended actions for next month",
        ],
        definition_of_done="Every number traces to a source; analysis is client-specific; recommendations are actionable; no hallucinated facts.",
        failure_modes=["AI-drafted analysis sounds insightful but is generic filler that would fit any client"],
        frequency="monthly",
        judgment="deterministic",
        error_cost="medium",
    )
    print(render_sop(report))


if __name__ == "__main__":
    _demo()
