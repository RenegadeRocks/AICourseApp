"""Scaffold vault/ folder tree from curriculum.json."""
from __future__ import annotations
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CURRICULUM = ROOT / "curriculum.json"
VAULT = ROOT / "vault"


def week_folder_name(block_id: str, week: dict) -> str:
    live = [s for s in week["sessions"] if s["kind"] == "live-session"]
    if not live:
        # Onboarding week etc.
        only = week["sessions"][0] if week["sessions"] else None
        label = only["slug"] if only else week["id"]
        return f"{week['id']}-{label}"[:80]
    # Combine slugs of live sessions for a descriptive folder name
    slugs = [s["slug"] for s in live]
    tag = "--".join(slugs)
    return f"{week['id']}-{tag}"[:120]


def main() -> None:
    data = json.loads(CURRICULUM.read_text(encoding="utf-8"))
    VAULT.mkdir(exist_ok=True)

    # Program-level dir
    prog_dir = VAULT / "00-program"
    prog_dir.mkdir(exist_ok=True)

    for block in data["blocks"]:
        bdir = VAULT / block["id"]
        bdir.mkdir(exist_ok=True)
        # Block README placeholder
        readme = bdir / "_block.md"
        if not readme.exists():
            readme.write_text(
                f"---\ntype: block\nid: {block['id']}\norder: {block['order']}\n"
                f"title: {block['title']!r}\n---\n\n# {block['title']}\n\n"
                f"{len(block['weeks'])} weeks.\n",
                encoding="utf-8",
            )
        for week in block["weeks"]:
            wdir = bdir / week_folder_name(block["id"], week)
            wdir.mkdir(exist_ok=True)
            # Per-week placeholder files (filled by generate-lesson later)
            (wdir / "_week.md").write_text(
                json_frontmatter_for_week(block, week), encoding="utf-8"
            )
            (wdir / "code-lab").mkdir(exist_ok=True)
            (wdir / "07-notebooklm-pack").mkdir(exist_ok=True)
    print(f"[ok] Scaffolded vault at {VAULT}")


def json_frontmatter_for_week(block: dict, week: dict) -> str:
    sessions_block = "\n".join(
        f"  - slug: {s['slug']}\n"
        f"    title: {s['title']!r}\n"
        f"    date: {s.get('date') or 'TBD'}\n"
        f"    kind: {s['kind']}"
        for s in week["sessions"]
    )
    return (
        f"---\ntype: week\nblock: {block['id']}\nweek: {week['id']}\n"
        f"title: {week['title']!r}\nlive_week_number: {week.get('live_week_number')}\n"
        f"sessions:\n{sessions_block}\n---\n\n"
        f"# {week['title']} — {block['title']}\n\n"
        f"_Auto-scaffolded. Run `/generate-lesson {block['id']}/{week['id']}` "
        f"to fill this week._\n"
    )


if __name__ == "__main__":
    main()
