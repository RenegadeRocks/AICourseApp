#!/usr/bin/env python3
"""
checklist.py — a dated launch-checklist runner.

Reads a launch plan (JSON) of dated, phased checklist items and prints a
go / no-go report. Blocking items that are not done fail the run (non-zero
exit), so "a stranger could execute the launch on a date" becomes a testable
gate rather than a vibe.

Usage:
    python checklist.py --plan launch_plan.json
    python checklist.py --plan launch_plan.json --phase launch-day
    python checklist.py --plan launch_plan.json --json     # machine-readable

Plan schema (see launch_plan.sample.json):
    {
      "product": "Triage Agent",
      "launch_date": "2026-08-29",
      "items": [
        {"id": "ph-first-comment", "phase": "T-7", "blocking": true,
         "done": false, "owner": "you",
         "text": "Maker first comment drafted, <30s read, limitation named"}
      ]
    }
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

PHASE_ORDER = ["T-7", "T-2", "T-0", "launch-day", "T+1", "T+14"]


def load_plan(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        plan = json.load(fh)
    if "items" not in plan or not isinstance(plan["items"], list):
        raise ValueError("plan must contain an 'items' list")
    return plan


def phase_key(phase: str) -> tuple[int, str]:
    return (PHASE_ORDER.index(phase) if phase in PHASE_ORDER else len(PHASE_ORDER), phase)


def evaluate(plan: dict, only_phase: str | None = None) -> dict:
    items = plan["items"]
    if only_phase:
        items = [i for i in items if i.get("phase") == only_phase]

    blocking_total = [i for i in items if i.get("blocking")]
    blocking_done = [i for i in blocking_total if i.get("done")]
    incomplete_blocking = [i for i in blocking_total if not i.get("done")]
    optional_incomplete = [
        i for i in items if not i.get("blocking") and not i.get("done")
    ]

    return {
        "product": plan.get("product", "(unnamed)"),
        "launch_date": plan.get("launch_date", "(no date)"),
        "total": len(items),
        "blocking_total": len(blocking_total),
        "blocking_done": len(blocking_done),
        "incomplete_blocking": incomplete_blocking,
        "optional_incomplete": optional_incomplete,
        "go": len(incomplete_blocking) == 0,
    }


def print_report(result: dict) -> None:
    print("=" * 64)
    print(f"  LAUNCH READINESS — {result['product']}")
    print(f"  Launch date: {result['launch_date']}")
    print("=" * 64)
    done = result["blocking_done"]
    total = result["blocking_total"]
    pct = (100 * done // total) if total else 100
    print(f"  Blocking items complete: {done}/{total}  ({pct}%)")
    print(f"  Total items in scope:    {result['total']}")
    print("-" * 64)

    if result["incomplete_blocking"]:
        print("  NO-GO. Incomplete BLOCKING items:")
        for i in sorted(result["incomplete_blocking"], key=lambda x: phase_key(x.get("phase", ""))):
            print(f"    [ ] ({i.get('phase','?'):>10}) {i['id']}: {i.get('text','')}")
    else:
        print("  GO. All blocking items complete.")

    if result["optional_incomplete"]:
        print("-" * 64)
        print("  Optional items still open (non-blocking):")
        for i in sorted(result["optional_incomplete"], key=lambda x: phase_key(x.get("phase", ""))):
            print(f"    ( ) ({i.get('phase','?'):>10}) {i['id']}: {i.get('text','')}")
    print("=" * 64)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Launch-checklist runner")
    parser.add_argument("--plan", required=True, type=Path)
    parser.add_argument("--phase", default=None, help="only evaluate one phase")
    parser.add_argument("--json", action="store_true", help="machine-readable output")
    args = parser.parse_args(argv)

    try:
        plan = load_plan(args.plan)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"error: could not load plan: {exc}", file=sys.stderr)
        return 2

    result = evaluate(plan, only_phase=args.phase)

    if args.json:
        serializable = {k: v for k, v in result.items()
                        if k not in ("incomplete_blocking", "optional_incomplete")}
        serializable["incomplete_blocking_ids"] = [i["id"] for i in result["incomplete_blocking"]]
        print(json.dumps(serializable, indent=2))
    else:
        print_report(result)

    return 0 if result["go"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
