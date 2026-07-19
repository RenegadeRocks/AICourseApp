"""90-day plan generator.

Turns an audit result (or a stage name) into a three-sprint, 90-day plan
scaffold keyed to the graduate's stage, from Week 22 Friday. It supplies the
structure and the stage's highest-leverage action; you supply the judgment and
the falsifiable outcomes.

Pure standard library. Python 3.10+.

Run:  python plan_generator.py
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

import graduation_audit as ga


STAGE_ORDER = ["Early", "Building", "Launched", "Scaling"]

# The single highest-leverage action per stage (Friday lesson).
HIGHEST_LEVERAGE = {
    "Early": "Get ONE person to pay (a payment or a paid pilot). Do things that don't scale.",
    "Building": "Make the revenue REPEATABLE: one channel, one pricing model, one delivery process.",
    "Launched": "Systematize yourself OUT of the bottleneck: SOPs + hand reproducible work to a person/agent.",
    "Scaling": "Pick the ONE growth loop with the best unit economics and pour into it.",
}

# The trap most associated with each stage, to seed the no-list.
STAGE_TRAP = {
    "Early": "Building more instead of selling. No-list: no new features until someone pays.",
    "Building": "One-off deals with no repeatable motion. No-list: no bespoke scope creep.",
    "Launched": "A job that looks like a business. No-list: no work you could have documented as an SOP.",
    "Scaling": "Diffusion across five channels. No-list: no second growth loop this quarter.",
}


def stage_from_audit(result: ga.Result) -> str:
    if result.total <= 25:
        return "Early"
    if result.total <= 45:
        return "Building"
    if result.total <= 60:
        return "Launched"
    return "Scaling"


@dataclass
class Sprint:
    number: int
    window: str
    theme: str
    prompt: str


def build_plan(stage: str, start: date, top_gap: str | None = None) -> list[Sprint]:
    if stage not in STAGE_ORDER:
        raise ValueError(f"unknown stage {stage!r}; expected one of {STAGE_ORDER}")

    def window(n: int) -> str:
        a = start + timedelta(days=30 * n)
        b = start + timedelta(days=30 * (n + 1) - 1)
        return f"{a.isoformat()} -> {b.isoformat()}"

    gap_line = top_gap or "your worst 0-or-1 item from the master-checklist audit"
    return [
        Sprint(
            1,
            window(0),
            "Close your worst gap",
            f"Make a 2 out of: {gap_line}. Write it as a falsifiable result, not 'improve'.",
        ),
        Sprint(
            2,
            window(1),
            "Highest-leverage action",
            HIGHEST_LEVERAGE[stage],
        ),
        Sprint(
            3,
            window(2),
            "Compound or correct",
            "If sprints 1-2 worked, build the loop/SOP that makes the gain repeatable. "
            "If not, run the honest post-mortem: bet wrong, execution wrong, or market wrong?",
        ),
    ]


def render_plan(stage: str, sprints: list[Sprint]) -> str:
    lines = [
        "=" * 60,
        f"90-DAY PLAN   stage: {stage}",
        "=" * 60,
        f"Highest-leverage action this quarter:\n  {HIGHEST_LEVERAGE[stage]}",
        f"Most likely trap:\n  {STAGE_TRAP[stage]}",
        "",
    ]
    for s in sprints:
        lines += [
            f"Sprint {s.number}  ({s.window})  — {s.theme}",
            f"  Outcome (make falsifiable): {s.prompt}",
            "  Weekly leading indicator: __________",
            "  No-list (one thing you will NOT do): __________",
            "",
        ]
    lines += [
        "Accountability:",
        "  Partner: __________   Public commitment: __________",
        "  End-of-sprint verdict is written (hit/miss + why), not felt.",
        "",
    ]
    return "\n".join(lines)


def _demo() -> None:
    # Reuse the Building-stage example from the audit demo.
    example = {i: 2 for i in range(1, 13)}
    example.update({13: 1, 14: 2, 15: 1, 18: 0, 21: 0, 23: 1})
    result = ga.score({**{i: 0 for i in range(1, 36)}, **example})
    stage = stage_from_audit(result)
    top_gap = "Pricing anchored to a value metric (#21), currently scored 0"
    plan = build_plan(stage, date(2026, 10, 20), top_gap=top_gap)
    print(render_plan(stage, plan))


if __name__ == "__main__":
    _demo()
