"""planner.py — CLI that runs the Week 21 build artifacts.

Usage:
    python planner.py system system.example.json
    python planner.py engine engine.example.json
    python planner.py all                      # runs both example files

Pure standard library. Python 3.10+.
"""
from __future__ import annotations

import argparse
from datetime import date

import content_engine as ce
import system_map as sm


def cmd_system(path: str) -> None:
    print(sm.report(path))


def cmd_engine(path: str) -> None:
    cfg = ce.load_engine(path)
    start = date.fromisoformat(cfg["start_date"])
    entries = ce.build_calendar(
        start=start,
        cadence_days=int(cfg["cadence_days"]),
        pillars=cfg["pillars"],
        derivative_channels=cfg["derivative_channels"],
    )
    matrix = ce.repurposing_matrix(cfg["pillars"], cfg["channels"])
    health = ce.engine_health(cfg["metrics"])
    print(ce.render_calendar(entries))
    print()
    print(ce.render_matrix(matrix))
    print()
    print(ce.render_health(health))


def main() -> None:
    parser = argparse.ArgumentParser(description="Week 21 complete-system + content-engine planner")
    sub = parser.add_subparsers(dest="command", required=True)

    p_sys = sub.add_parser("system", help="validate a system map JSON")
    p_sys.add_argument("path")

    p_eng = sub.add_parser("engine", help="plan + measure the content engine")
    p_eng.add_argument("path")

    sub.add_parser("all", help="run both example files")

    args = parser.parse_args()
    if args.command == "system":
        cmd_system(args.path)
    elif args.command == "engine":
        cmd_engine(args.path)
    elif args.command == "all":
        cmd_system("system.example.json")
        print("\n" + "=" * 60 + "\n")
        cmd_engine("engine.example.json")


if __name__ == "__main__":
    main()
