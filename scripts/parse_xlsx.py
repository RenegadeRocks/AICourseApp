"""
Parse 'AI Pro-level Course - Tentative Schedule.xlsx' into curriculum.json.

Output schema:
{
  "program": {
    "name": "AI Pro-level Course",
    "start_date": "2026-04-18",
    "end_date": "2026-10-22",
    "session_time_ist": "19:30",
    "source_file": "AI Pro-level Course - Tentative Schedule.xlsx",
    "parsed_at": "ISO-8601"
  },
  "blocks": [
    {
      "id": "block-0-basecamp",
      "title": "Basecamp & Revision",
      "order": 0,
      "weeks": [
        {
          "id": "week-01",
          "title": "Week 1",
          "live_week_number": 1,
          "sessions": [
            {"slug": "basecamp-part-1-prompting-and-rags",
             "title": "Basecamp Part 1: Prompting & RAGs",
             "date": "2026-05-02",
             "kind": "live-session"},
            ...
          ]
        }
      ]
    }
  ]
}
"""
from __future__ import annotations
import json
import re
import sys
from datetime import date, datetime, time
from pathlib import Path
from typing import Iterable

import openpyxl

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "AI Pro-level Course - Tentative Schedule.xlsx"
OUT = ROOT / "curriculum.json"

BLOCK_ORDER = [
    ("block-0-basecamp", "Basecamp & Revision", ["Basecamp"]),
    ("block-1-problem-solving-outreach", "Problem Solving with AI & Outreach",
     ["Problem Solving with AI & Outreach"]),
    ("block-2-ai-employees", "AI Employees / Interns that work for you",
     ["AI Employees / Interns that work for you"]),
    ("block-3-advanced-topics-voice", "Advanced Topics & Voice Agents",
     ["Advanced Topics & Voice Agents"]),
    ("block-4-test-validate-package", "Test, Validate & Package your Ideas",
     ["Test, Validate & Package your Ideas"]),
    ("block-5-product-building-principles", "Product Building Principles",
     ["Block 5 -", "Product Building Principles"]),
    ("block-6-launch-monetization", "Launch & Monetization",
     ["Block 6 -", "Launch & Monetization"]),
    ("block-7-onboarding-tracking", "Onboarding & Tracking",
     ["Block 7 -", "Onboarding & Tracking"]),
    ("block-8-wind-up-checklists", "Wind-up & Checklists",
     ["Block 8 -", "Wind-up & Checklists"]),
]


def slugify(s: str) -> str:
    s = s.lower()
    s = re.sub(r"[\u2013\u2014\u2018\u2019\u201c\u201d]", "-", s)
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[-\s]+", "-", s).strip("-")
    return s[:80]


def classify_kind(title: str) -> str:
    t = title.lower()
    if "office hours" in t:
        return "office-hours"
    if "release of session resources" in t:
        return "resource-drop"
    if "onboarding" in t and "client" not in t:
        return "onboarding"
    if "demo day" in t or "immersion" in t:
        return "special"
    return "live-session"


def normalize_block_label(raw: str) -> str:
    if not raw:
        return ""
    return re.sub(r"\s+", " ", raw).strip().strip("-").strip()


def resolve_block(label: str) -> tuple[str, str, int] | None:
    norm = normalize_block_label(label)
    if not norm:
        return None
    for i, (bid, btitle, aliases) in enumerate(BLOCK_ORDER):
        for alias in aliases:
            alias_norm = normalize_block_label(alias)
            if alias_norm and alias_norm.lower() in norm.lower():
                return bid, btitle, i
    return None


def main() -> int:
    if not XLSX.exists():
        print(f"ERROR: {XLSX} not found", file=sys.stderr)
        return 1

    wb = openpyxl.load_workbook(XLSX, data_only=True)
    ws = wb["Program Schedule"]

    blocks: dict[str, dict] = {}
    current_block: dict | None = None
    current_week: dict | None = None
    pending_block_label = ""

    for row in ws.iter_rows(values_only=True):
        if not any(c not in (None, "") for c in row):
            pending_block_label = ""
            continue

        col_a = (row[0] or "").strip() if isinstance(row[0], str) else ""
        col_b = (row[1] or "").strip() if isinstance(row[1], str) else ""
        col_c = (row[2] or "").strip() if isinstance(row[2], str) else ""
        col_d = row[3]

        # Header rows / instructions — skip anything with "Week" as literal header
        if col_b.lower() == "week" and col_c.lower().startswith("details"):
            continue

        # If col_a carries a block name (Basecamp / "Problem Solving..." etc.) set it
        if col_a:
            # Could be a multi-line label; combine with pending
            pending_block_label = (pending_block_label + " " + col_a).strip()
            resolved = resolve_block(pending_block_label)
            if resolved:
                bid, btitle, border = resolved
                if bid not in blocks:
                    blocks[bid] = {
                        "id": bid,
                        "title": btitle,
                        "order": border,
                        "weeks": [],
                    }
                current_block = blocks[bid]
                pending_block_label = ""

        # Row with only a block label fragment (e.g. "Block 5 -") on its own line
        # — captured by pending_block_label above; if no session data in row, continue.
        if col_a and not col_b and not col_c:
            continue

        # Week marker
        if col_b.lower().startswith("week"):
            week_num_match = re.search(r"(\d+)", col_b)
            week_num = int(week_num_match.group(1)) if week_num_match else None
            if current_block is None:
                # Default to basecamp if we see a week before a block
                current_block = blocks.setdefault(
                    "block-0-basecamp",
                    {"id": "block-0-basecamp", "title": "Basecamp & Revision",
                     "order": 0, "weeks": []},
                )
            week_id = f"week-{week_num:02d}" if week_num is not None else slugify(col_b)
            current_week = {
                "id": week_id,
                "title": col_b,
                "live_week_number": week_num,
                "sessions": [],
            }
            current_block["weeks"].append(current_week)

        # Session row
        if col_c:
            if current_week is None:
                # skip stray rows
                continue
            title = col_c
            session_date = None
            if isinstance(col_d, (datetime, date)):
                session_date = (col_d.date() if isinstance(col_d, datetime) else col_d).isoformat()
            session = {
                "slug": slugify(title),
                "title": title,
                "date": session_date,
                "kind": classify_kind(title),
            }
            current_week["sessions"].append(session)

    # Sort & finalize
    ordered = sorted(blocks.values(), key=lambda b: b["order"])

    # Compute program start / end
    all_dates = [
        s["date"] for b in ordered for w in b["weeks"] for s in w["sessions"]
        if s.get("date")
    ]
    start = min(all_dates) if all_dates else None
    end = max(all_dates) if all_dates else None

    out = {
        "program": {
            "name": "AI Pro-level Course",
            "instructor": "Dileep (Outskill)",
            "start_date": start,
            "end_date": end,
            "session_time_ist": "19:30",
            "office_hours_day": "Thursday",
            "core_session_days": ["Saturday", "Sunday"],
            "resource_drop_day": "Monday",
            "source_file": XLSX.name,
            "parsed_at": datetime.utcnow().isoformat() + "Z",
        },
        "blocks": ordered,
    }

    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    # Summary
    total_weeks = sum(len(b["weeks"]) for b in ordered)
    total_sessions = sum(len(w["sessions"]) for b in ordered for w in b["weeks"])
    live_sessions = sum(
        1 for b in ordered for w in b["weeks"] for s in w["sessions"]
        if s["kind"] == "live-session"
    )
    print(f"[ok] Wrote {OUT}")
    print(f"     Blocks: {len(ordered)}  Weeks: {total_weeks}  "
          f"Sessions: {total_sessions}  Live: {live_sessions}")
    print(f"     Program: {start} -> {end}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
