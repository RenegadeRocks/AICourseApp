"""Turn events.jsonl into the Week-4-discipline metrics (Tuesday's five + squad).

Usage:  python eval.py events.jsonl

Computes:
  - tool-call latency p50/p95 (per channel)
  - re-ask rate (should be 0 — sacred fields never re-asked)
  - reroute rate (barge-in corrections handled)
  - per-intent containment
  - per-channel behavior delta (does the same brain behave consistently?)

Note: first-audio latency is measured client-side by the voice PLATFORM, not
here — paste those three numbers from the platform dashboard into the printed
report by hand. This script owns everything the brain can see server-side.
"""
from __future__ import annotations

import json
import sys
from collections import defaultdict
from statistics import median


def pct(values: list[float], p: float) -> float:
    if not values:
        return 0.0
    s = sorted(values)
    k = min(len(s) - 1, int(round((p / 100) * (len(s) - 1))))
    return s[k]


def main(path: str) -> None:
    turns: list[dict] = []
    tool_calls: list[dict] = []
    with open(path) as f:
        for line in f:
            ev = json.loads(line)
            if ev["type"] == "turn":
                turns.append(ev)
            elif ev["type"] == "tool_call":
                tool_calls.append(ev)

    print("=" * 56)
    print("WEEK 7 BUILD — server-side metrics")
    print("=" * 56)

    # tool latency by channel
    by_ch: dict[str, list[float]] = defaultdict(list)
    for tc in tool_calls:
        by_ch[tc["channel"]].append(tc["latency_ms"])
    print("\nTool round-trip latency (ms):")
    for ch, lat in by_ch.items():
        print(f"  {ch:9s} p50={median(lat):.0f}  p95={pct(lat,95):.0f}  n={len(lat)}")

    # re-ask + reroute
    reasks = sum(t.get("reask", False) for t in turns)
    reroutes = sum(t.get("reroute", False) for t in turns)
    print(f"\nRe-ask events (target 0): {reasks}")
    print(f"Reroute (barge-in correction) events handled: {reroutes}")

    # per-intent containment
    cont: dict[str, list[bool]] = defaultdict(list)
    for t in turns:
        cont[t["intent"]].append(bool(t.get("contained")))
    print("\nPer-intent containment:")
    for intent, xs in cont.items():
        rate = 100 * sum(xs) / len(xs) if xs else 0
        print(f"  {intent:9s} {rate:5.1f}%  (n={len(xs)})")

    # per-channel behavior delta
    ch_intents: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for t in turns:
        ch_intents[t["channel"]][t["intent"]] += 1
    print("\nPer-channel intent distribution (consistency check):")
    for ch, dist in ch_intents.items():
        print(f"  {ch:9s} {dict(dist)}")

    print("\nReminder: paste platform-side first-audio p50/p95 for the 3 voice")
    print("calls here, and grade the barge-in-during-handoff recovery by hand.")
    print("=" * 56)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "events.jsonl")
