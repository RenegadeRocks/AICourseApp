"""system_map.py — build and validate a complete-system map.

Takes a JSON spec of your business subsystems and:
  1. validates that no subsystem is an "orphan" (missing a metric, owner,
     SOP, or a wikilink to the course week that built it),
  2. audits handoffs for dead-ends (a subsystem nothing flows into, or that
     flows into nothing),
  3. renders a one-page system map and a completion checklist.

Pure standard library. Python 3.10+.
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path


REQUIRED_FIELDS = ("metric", "owner", "sop", "built_in")


@dataclass
class Subsystem:
    name: str
    metric: str = ""
    owner: str = ""
    sop: str = ""
    built_in: str = ""          # wikilink to the course week that built it
    handoff_to: list[str] = field(default_factory=list)

    def missing(self) -> list[str]:
        """Return the required fields that are blank (what makes it an orphan)."""
        return [f for f in REQUIRED_FIELDS if not str(getattr(self, f)).strip()]


def load_system(path: str | Path) -> list[Subsystem]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    subs = [Subsystem(**row) for row in data["subsystems"]]
    _validate_handoff_targets(subs)
    return subs


def _validate_handoff_targets(subs: list[Subsystem]) -> None:
    names = {s.name for s in subs}
    for s in subs:
        for target in s.handoff_to:
            if target not in names:
                raise ValueError(
                    f"subsystem '{s.name}' hands off to unknown subsystem '{target}'"
                )


def find_orphans(subs: list[Subsystem]) -> dict[str, list[str]]:
    """Map subsystem name -> list of missing required fields. Empty == clean."""
    return {s.name: s.missing() for s in subs if s.missing()}


def find_handoff_gaps(subs: list[Subsystem]) -> dict[str, list[str]]:
    """Detect dead-ends: no outbound handoff, or nothing hands off into it."""
    inbound: dict[str, int] = {s.name: 0 for s in subs}
    for s in subs:
        for target in s.handoff_to:
            inbound[target] += 1
    gaps: dict[str, list[str]] = {}
    for s in subs:
        problems = []
        if not s.handoff_to:
            problems.append("no outbound handoff (dead end)")
        if inbound[s.name] == 0:
            problems.append("no inbound handoff (starved)")
        if problems:
            gaps[s.name] = problems
    return gaps


def render_map(subs: list[Subsystem]) -> str:
    lines = ["# Complete-System Map", ""]
    for s in subs:
        flow = " -> ".join(s.handoff_to) if s.handoff_to else "(none)"
        lines += [
            f"## {s.name}",
            f"- metric:   {s.metric or 'MISSING'}",
            f"- owner:    {s.owner or 'MISSING'}",
            f"- sop:      {s.sop or 'MISSING'}",
            f"- built in: {s.built_in or 'MISSING'}",
            f"- hands off to: {flow}",
            "",
        ]
    return "\n".join(lines)


def render_checklist(subs: list[Subsystem]) -> str:
    orphans = find_orphans(subs)
    gaps = find_handoff_gaps(subs)
    lines = ["# System Completeness Checklist", ""]
    for s in subs:
        clean = s.name not in orphans and s.name not in gaps
        box = "[x]" if clean else "[ ]"
        note = ""
        if s.name in orphans:
            note = f"  -> missing: {', '.join(orphans[s.name])}"
        elif s.name in gaps:
            note = f"  -> {'; '.join(gaps[s.name])}"
        lines.append(f"- {box} {s.name}{note}")
    passed = not orphans and not gaps
    lines += ["", f"PASS BAR: {'PASS — no orphan subsystems' if passed else 'FAIL — fix the boxes above'}"]
    return "\n".join(lines)


def report(path: str | Path) -> str:
    subs = load_system(path)
    return render_map(subs) + "\n\n" + render_checklist(subs)
