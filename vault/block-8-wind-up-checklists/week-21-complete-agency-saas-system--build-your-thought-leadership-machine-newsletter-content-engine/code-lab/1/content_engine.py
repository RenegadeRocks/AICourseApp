"""content_engine.py — plan and measure the content engine.

Three tools:
  1. build_calendar()   — schedule pillar issues + atomized derivatives on a
                          sustainable cadence.
  2. repurposing_matrix() — turn one pillar into many platform-native assets.
  3. engine_health()    — compute the four health metrics with pass/fail flags.

Pure standard library. Python 3.10+.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path


# ---------------------------------------------------------------------------
# 1. Calendar
# ---------------------------------------------------------------------------

@dataclass
class CalendarEntry:
    day: date
    channel: str
    asset: str

    def as_row(self) -> str:
        return f"{self.day.isoformat()}  {self.channel:<12}  {self.asset}"


def build_calendar(
    start: date,
    cadence_days: int,
    pillars: list[str],
    derivative_channels: list[str],
) -> list[CalendarEntry]:
    """One pillar per cadence cycle; derivatives spread across the days after it.

    A biweekly cadence (cadence_days=14) with 4 derivative channels drops the
    pillar on day 0 of each cycle and one derivative on each following day.
    """
    if cadence_days <= 0:
        raise ValueError("cadence_days must be positive")
    if len(derivative_channels) >= cadence_days:
        raise ValueError(
            "too many derivative channels for the cadence: "
            f"{len(derivative_channels)} derivatives need > {cadence_days} days"
        )
    entries: list[CalendarEntry] = []
    for i, pillar in enumerate(pillars):
        cycle_start = start + timedelta(days=i * cadence_days)
        entries.append(CalendarEntry(cycle_start, "newsletter", f"PILLAR: {pillar}"))
        for j, channel in enumerate(derivative_channels, start=1):
            entries.append(
                CalendarEntry(cycle_start + timedelta(days=j), channel, f"from: {pillar}")
            )
    return entries


def render_calendar(entries: list[CalendarEntry]) -> str:
    lines = ["# Content Calendar", ""]
    lines += [e.as_row() for e in entries]
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 2. Repurposing matrix
# ---------------------------------------------------------------------------

def repurposing_matrix(pillars: list[str], channels: list[str]) -> list[list[str]]:
    """Rows = pillars, cols = channels; each cell is the derived asset label."""
    header = ["pillar \\ channel", *channels]
    rows = [header]
    for p in pillars:
        rows.append([p, *[f"{p[:18]}… -> {c}" for c in channels]])
    return rows


def render_matrix(matrix: list[list[str]]) -> str:
    widths = [max(len(row[c]) for row in matrix) for c in range(len(matrix[0]))]
    lines = ["# Repurposing Matrix", ""]
    for row in matrix:
        lines.append("  ".join(cell.ljust(widths[c]) for c, cell in enumerate(row)))
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# 3. Engine health
# ---------------------------------------------------------------------------

# Thresholds are 2026 creator-newsletter baselines (see 04-thu lesson).
THRESHOLDS = {
    "weekly_growth_rate": 0.0,   # net new subs must be positive
    "open_rate": 0.35,           # opted-in creator newsletters run 0.35-0.50
    "click_reply_rate": 0.02,    # engagement depth floor
    "downstream_conversion": 0.005,  # subs -> leads/calls/customers
}


@dataclass
class HealthMetric:
    name: str
    value: float
    threshold: float

    @property
    def ok(self) -> bool:
        return self.value >= self.threshold

    def as_row(self) -> str:
        flag = "OK  " if self.ok else "FLAG"
        return f"[{flag}] {self.name:<22} {self.value:>8.4f}  (>= {self.threshold})"


def engine_health(metrics: dict) -> list[HealthMetric]:
    """metrics keys: subs_start, subs_end, weeks, opens, sent, clicks_replies,
    downstream_conversions."""
    weeks = max(int(metrics["weeks"]), 1)
    subs_start = max(float(metrics["subs_start"]), 1.0)
    subs_end = float(metrics["subs_end"])
    sent = max(float(metrics["sent"]), 1.0)

    weekly_growth = ((subs_end - subs_start) / subs_start) / weeks
    open_rate = float(metrics["opens"]) / sent
    engagement = float(metrics["clicks_replies"]) / sent
    conversion = float(metrics["downstream_conversions"]) / subs_end

    return [
        HealthMetric("weekly_growth_rate", weekly_growth, THRESHOLDS["weekly_growth_rate"]),
        HealthMetric("open_rate", open_rate, THRESHOLDS["open_rate"]),
        HealthMetric("click_reply_rate", engagement, THRESHOLDS["click_reply_rate"]),
        HealthMetric("downstream_conversion", conversion, THRESHOLDS["downstream_conversion"]),
    ]


def render_health(metrics: list[HealthMetric]) -> str:
    lines = ["# Engine Health", ""]
    lines += [m.as_row() for m in metrics]
    flagged = [m.name for m in metrics if not m.ok]
    lines += ["", f"STATUS: {'HEALTHY' if not flagged else 'INVESTIGATE: ' + ', '.join(flagged)}"]
    return "\n".join(lines)


def load_engine(path: str | Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))
