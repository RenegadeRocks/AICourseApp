#!/usr/bin/env python3
"""
personalizer.py — a COMPLIANT outreach-sequence personalizer.

Design principle (the whole point of this lab):
    It DRAFTS for human review. It does NOT send. Ever.

It renders a 3-touch sequence for each prospect from a template, runs every
draft through the compliance gates in compliance.py, and writes the passing
drafts to ./drafts/ marked "FOR HUMAN REVIEW — DO NOT SEND". A human then
reads, edits every specific, and sends by hand from their own client.

This encodes the 04-thu thesis: use AI for research and drafting-for-review,
never for blast-send. The --send flag exists only to refuse, loudly, and
explain why.

Usage:
    python personalizer.py --prospects prospects.sample.json \
        --template sequence_template.json --config config.json
    python personalizer.py ... --touch 1        # draft only the first touch
    python personalizer.py ... --send           # refuses, by design
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import compliance


def load_json(path: Path) -> dict | list:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def render(template_str: str, prospect: dict, config: dict) -> str:
    """Minimal, safe field substitution. Unknown fields render as empty string
    rather than raising, so a missing optional field never crashes a batch."""
    fields = {
        "first_name": prospect.get("first_name", ""),
        "name": prospect.get("name", ""),
        "company": prospect.get("company", ""),
        "role": prospect.get("role", ""),
        "signal": prospect.get("signal", ""),
        "sender_name": config.get("sender_name", ""),
        "product": config.get("product", ""),
        "outcome": config.get("outcome", ""),
        "sender_physical_address": config.get("sender_physical_address", ""),
        "unsubscribe_url": config.get("unsubscribe_url", ""),
    }

    class _Default(dict):
        def __missing__(self, key):  # noqa: D401
            return ""

    return template_str.format_map(_Default(fields))


def compliance_footer(config: dict) -> str:
    return (
        "\n\n--\n"
        f"{config.get('sender_name', '')}\n"
        f"{config.get('sender_physical_address', '')}\n"
        f"Not relevant? Opt out here and I won't contact you again: "
        f"{config.get('unsubscribe_url', '')}"
    )


def draft_for_prospect(prospect: dict, template: dict, config: dict,
                       only_touch: int | None) -> tuple[list[dict], list[compliance.Finding]]:
    drafts: list[dict] = []
    findings: list[compliance.Finding] = []

    pres = compliance.check_prospect(prospect, config)
    findings.extend(pres.findings)
    if not pres.ok:
        return drafts, findings  # blocked: do not draft anything for this prospect

    for touch in template["touches"]:
        n = touch["number"]
        if only_touch is not None and n != only_touch:
            continue
        subject = render(touch["subject"], prospect, config)
        body = render(touch["body"], prospect, config) + compliance_footer(config)

        gate = compliance.check_rendered_email(
            subject, body, is_first_touch=(n == 1), config=config)
        findings.extend(gate.findings)
        if not gate.ok:
            continue  # blocked draft is not written for review

        drafts.append({
            "touch": n,
            "send_after_days": touch.get("send_after_days", 0),
            "subject": subject,
            "body": body,
            "warnings": [f.message for f in gate.warnings],
        })
    return drafts, findings


def write_drafts(prospect: dict, drafts: list[dict], out_dir: Path) -> list[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    safe = "".join(c if c.isalnum() else "-" for c in prospect.get("name", "prospect")).strip("-")
    written: list[Path] = []
    for d in drafts:
        path = out_dir / f"{safe}__touch{d['touch']}.txt"
        header = (
            "=================================================================\n"
            "  DRAFT — FOR HUMAN REVIEW — DO NOT SEND AS-IS\n"
            "  Read every line. Verify the {signal} is true. Edit in your voice.\n"
            "  Then send by hand from your own email client.\n"
            "=================================================================\n"
        )
        meta = (
            f"To:      {prospect.get('name','')} <{prospect.get('email','')}>\n"
            f"Role:    {prospect.get('role','')} @ {prospect.get('company','')}\n"
            f"Region:  {prospect.get('region','')}\n"
            f"Send:    touch {d['touch']}, +{d['send_after_days']} days\n"
            f"Signal:  {prospect.get('signal','')}\n"
        )
        warn = ""
        if d["warnings"]:
            warn = "\nREVIEWER WARNINGS:\n" + "\n".join(f"  - {w}" for w in d["warnings"]) + "\n"
        content = (
            f"{header}\n{meta}{warn}\n"
            f"Subject: {d['subject']}\n\n{d['body']}\n"
        )
        path.write_text(content, encoding="utf-8")
        written.append(path)
    return written


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Compliant outreach personalizer (drafts, never sends)")
    parser.add_argument("--prospects", required=True, type=Path)
    parser.add_argument("--template", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--out", default=Path("drafts"), type=Path)
    parser.add_argument("--touch", type=int, default=None, choices=[1, 2, 3])
    parser.add_argument("--send", action="store_true", help="(refuses by design)")
    args = parser.parse_args(argv)

    if args.send:
        print(
            "REFUSED. This tool never sends.\n"
            "It drafts for human review because generic AI blast-send is the exact\n"
            "motion that burns domains, trips spam filters, and gets buyers to\n"
            "delete on sight (see 04-thu). Read every draft, edit every specific,\n"
            "and send by hand from your own client.",
            file=sys.stderr,
        )
        return 3

    try:
        prospects = load_json(args.prospects)
        template = load_json(args.template)
        config = load_json(args.config)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"error: could not load inputs: {exc}", file=sys.stderr)
        return 2

    if not isinstance(prospects, list):
        print("error: prospects file must be a JSON list", file=sys.stderr)
        return 2

    cfg_gate = compliance.check_config(config)
    for f in cfg_gate.findings:
        print(f"[config {f.level}] {f.code}: {f.message}", file=sys.stderr)
    if not cfg_gate.ok:
        print("\nConfig has blocking CAN-SPAM problems. Fix config.json first.", file=sys.stderr)
        return 1

    total_drafts = 0
    total_blocked = 0
    print(f"Personalizing {len(prospects)} prospect(s). Drafts -> {args.out}/  (nothing is sent)\n")
    for prospect in prospects:
        drafts, findings = draft_for_prospect(prospect, template, config, args.touch)
        blocks = [f for f in findings if f.level == "block"]
        warns = [f for f in findings if f.level == "warn"]
        name = prospect.get("name", "?")
        if blocks:
            total_blocked += 1
            print(f"  BLOCKED  {name}: " + "; ".join(f.code for f in blocks))
            for b in blocks:
                print(f"           - {b.message}")
            continue
        written = write_drafts(prospect, drafts, args.out)
        total_drafts += len(written)
        wnote = f"  ({len(warns)} warning(s))" if warns else ""
        print(f"  drafted  {name}: {len(written)} touch(es){wnote}")
        for w in warns:
            print(f"           ~ {w.message}")

    print(f"\nDone. {total_drafts} draft(s) written for review; "
          f"{total_blocked} prospect(s) blocked. Nothing was sent.")
    print("Next: open ./drafts/, read every line, edit every specific, send by hand.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
