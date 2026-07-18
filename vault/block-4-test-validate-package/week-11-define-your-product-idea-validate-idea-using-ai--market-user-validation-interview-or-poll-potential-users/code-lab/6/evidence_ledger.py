#!/usr/bin/env python3
"""evidence_ledger.py — a pre-registered evidence ledger for build/pivot/kill decisions.

Week 11, Block 4 (AI Pro-level Course). Pure stdlib; Python 3.10+.

The ledger enforces three disciplines from the week:
  1. Assumptions and decision rules are registered BEFORE evidence (init locks them;
     changing them later is recorded as an override with a reason).
  2. Every evidence atom carries source_class, direction, strength, and provenance.
  3. Class weights are fixed in config; `synthetic` is weight 0.0 by rule
     (Thursday's lesson) and the tool refuses to let it satisfy kill criteria.

Usage (see README.md):
  python evidence_ledger.py init --ledger ledger.json
  python evidence_ledger.py add-assumption --ledger ledger.json \
      --id A1 --category desirability \
      --text "6/10 interviewees cite a specific recent instance" \
      --kill "fewer than 3 of 10 interviewees cite a specific instance"
  python evidence_ledger.py add-evidence --ledger ledger.json \
      --assumption A1 --direction for --source-class stated --strength 4 \
      --quote "Acme emailed asking where the follow-up was" \
      --source P3 --channel warm
  python evidence_ledger.py import-atoms --ledger ledger.json --atoms atoms.json
  python evidence_ledger.py verdict --ledger ledger.json
  python evidence_ledger.py report --ledger ledger.json > report.md
  python evidence_ledger.py wilson --successes 4 --trials 74
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path

SOURCE_CLASSES = ("desk", "synthetic", "stated", "behavioral", "paid")
DIRECTIONS = ("for", "against", "neutral")
CATEGORIES = ("desirability", "viability", "feasibility")

DEFAULT_WEIGHTS = {
    # Fixed in advance. Edit BEFORE gathering evidence, never after.
    "paid": 5.0,
    "behavioral": 3.0,
    "stated": 1.0,
    "desk": 0.5,
    "synthetic": 0.0,  # Thursday's rule: simulate to design, humans to decide.
}

DEFAULT_STRENGTH_RUBRIC = {
    # Anchors for the 0-5 strength score (Hamel's calibration critique, Fri lesson).
    "0": "Compliment, vague enthusiasm, or unanchored opinion. Scores zero by rule.",
    "1": "General opinion about the problem space, no specifics.",
    "2": "Specific claim without date/instance, or second-hand report.",
    "3": "One dated, specific past instance OR a working workaround described.",
    "4": "Specific instance WITH named consequence, or an abandoned paid workaround.",
    "5": "Currency: time commitment scheduled, intro made, money moved (or refused with reasons).",
}

DEFAULT_DECISION_RULE = {
    "build": {
        "min_for_mass_desirability": 12.0,
        "min_behavioral_or_paid_atoms": 2,
        "max_unrebutted_strength5_against": 0,
    },
    "pivot": "If desirability passes but a wedge/viability assumption fails its kill "
             "criterion, pivot the named axis (edit this text at init with your axis).",
    "kill": "Any assumption's kill criterion tripped by human-class evidence.",
}


def now_iso() -> str:
    return datetime.now().isoformat(timespec="seconds")


def wilson_interval(successes: int, trials: int, z: float = 1.96) -> tuple[float, float]:
    """Wilson score 95% CI for a proportion. Canonical derivation: Block 2 Week 3 Sat."""
    if trials == 0:
        return (0.0, 1.0)
    if successes < 0 or successes > trials:
        raise ValueError("successes must be between 0 and trials")
    p = successes / trials
    denom = 1 + z**2 / trials
    centre = p + z**2 / (2 * trials)
    margin = z * math.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2))
    return ((centre - margin) / denom, (centre + margin) / denom)


def load_ledger(path: Path) -> dict:
    if not path.exists():
        sys.exit(f"No ledger at {path}. Run `init` first.")
    return json.loads(path.read_text(encoding="utf-8"))


def save_ledger(path: Path, ledger: dict) -> None:
    path.write_text(json.dumps(ledger, indent=2, ensure_ascii=False), encoding="utf-8")


def cmd_init(args: argparse.Namespace) -> None:
    path = Path(args.ledger)
    if path.exists() and not args.force:
        sys.exit(f"{path} exists. A ledger is pre-registered; use --force only to start over.")
    ledger = {
        "created": now_iso(),
        "registered_on": str(date.today()),
        "weights": DEFAULT_WEIGHTS,
        "strength_rubric": DEFAULT_STRENGTH_RUBRIC,
        "decision_rule": DEFAULT_DECISION_RULE,
        "assumptions": [],
        "evidence": [],
        "overrides": [],
    }
    save_ledger(path, ledger)
    print(f"Initialized {path}.")
    print("EDIT weights/decision_rule NOW if you must, then commit the file.")
    print("The commit timestamp is your pre-registration receipt.")


def cmd_add_assumption(args: argparse.Namespace) -> None:
    path = Path(args.ledger)
    ledger = load_ledger(path)
    if args.category not in CATEGORIES:
        sys.exit(f"category must be one of {CATEGORIES}")
    if any(a["id"] == args.id for a in ledger["assumptions"]):
        sys.exit(f"Assumption {args.id} already exists.")
    if ledger["evidence"] and not args.reason:
        sys.exit("Evidence already exists. Adding assumptions now requires --reason "
                 "(recorded as an override).")
    assumption = {
        "id": args.id,
        "category": args.category,
        "text": args.text,
        "kill_criterion": args.kill,
        "added": now_iso(),
    }
    ledger["assumptions"].append(assumption)
    if args.reason:
        ledger["overrides"].append(
            {"when": now_iso(), "what": f"late assumption {args.id}", "reason": args.reason}
        )
    save_ledger(path, ledger)
    print(f"Registered {args.id} ({args.category}): {args.text}")


def cmd_add_evidence(args: argparse.Namespace) -> None:
    path = Path(args.ledger)
    ledger = load_ledger(path)
    if args.direction not in DIRECTIONS:
        sys.exit(f"direction must be one of {DIRECTIONS}")
    if args.source_class not in SOURCE_CLASSES:
        sys.exit(f"source-class must be one of {SOURCE_CLASSES}")
    if not 0 <= args.strength <= 5:
        sys.exit("strength must be 0-5 (see strength_rubric in the ledger).")
    if not any(a["id"] == args.assumption for a in ledger["assumptions"]):
        sys.exit(f"Unknown assumption {args.assumption}. Register it first.")
    atom = {
        "assumption": args.assumption,
        "direction": args.direction,
        "source_class": args.source_class,
        "strength": args.strength,
        "quote": args.quote,
        "source": args.source,
        "channel": args.channel,
        "added": now_iso(),
    }
    ledger["evidence"].append(atom)
    save_ledger(path, ledger)
    weight = ledger["weights"].get(args.source_class, 0.0)
    note = " (weight 0.0 — synthetic never decides)" if args.source_class == "synthetic" else ""
    print(f"Logged atom for {args.assumption}: {args.direction.upper()} "
          f"class={args.source_class} strength={args.strength}{note} weight={weight}")


def cmd_import_atoms(args: argparse.Namespace) -> None:
    """Import atoms produced by note_synthesizer.py (a JSON list)."""
    path = Path(args.ledger)
    ledger = load_ledger(path)
    atoms = json.loads(Path(args.atoms).read_text(encoding="utf-8"))
    known = {a["id"] for a in ledger["assumptions"]}
    imported, skipped = 0, 0
    for atom in atoms:
        if atom.get("assumption") not in known:
            skipped += 1
            continue
        atom.setdefault("added", now_iso())
        atom.setdefault("channel", "unknown")
        if (atom.get("direction") in DIRECTIONS
                and atom.get("source_class") in SOURCE_CLASSES
                and isinstance(atom.get("strength"), int)
                and 0 <= atom["strength"] <= 5):
            ledger["evidence"].append(atom)
            imported += 1
        else:
            skipped += 1
    save_ledger(path, ledger)
    print(f"Imported {imported} atoms; skipped {skipped} "
          f"(unknown assumption id or malformed fields).")


def assumption_masses(ledger: dict, assumption_id: str) -> dict:
    weights = ledger["weights"]
    atoms = [e for e in ledger["evidence"] if e["assumption"] == assumption_id]
    mass = {"for": 0.0, "against": 0.0, "neutral": 0.0}
    strongest_against = None
    human_against_s5 = 0
    behavioral_or_paid = 0
    for e in atoms:
        w = weights.get(e["source_class"], 0.0)
        mass[e["direction"]] += w * e["strength"]
        if e["direction"] == "against":
            if strongest_against is None or e["strength"] > strongest_against["strength"]:
                strongest_against = e
            if e["strength"] == 5 and e["source_class"] != "synthetic":
                human_against_s5 += 1
        if e["source_class"] in ("behavioral", "paid") and e["direction"] == "for":
            behavioral_or_paid += 1
    return {
        "atoms": len(atoms),
        "mass": mass,
        "strongest_against": strongest_against,
        "human_against_strength5": human_against_s5,
        "behavioral_or_paid_for": behavioral_or_paid,
    }


def cmd_verdict(args: argparse.Namespace) -> None:
    ledger = load_ledger(Path(args.ledger))
    rule = ledger["decision_rule"]["build"]
    print("=" * 62)
    print("EVIDENCE LEDGER VERDICT", now_iso())
    print("=" * 62)
    build_ok = True
    desirability_for = 0.0
    total_behavioral_or_paid = 0
    s5_against_total = 0
    for a in ledger["assumptions"]:
        m = assumption_masses(ledger, a["id"])
        print(f"\n[{a['id']}] ({a['category']}) {a['text']}")
        print(f"  atoms={m['atoms']}  FOR={m['mass']['for']:.1f}  "
              f"AGAINST={m['mass']['against']:.1f}  NEUTRAL={m['mass']['neutral']:.1f}")
        print(f"  kill criterion: {a['kill_criterion']}")
        if m["strongest_against"]:
            sa = m["strongest_against"]
            print(f"  strongest AGAINST (s{sa['strength']}, {sa['source_class']}, "
                  f"{sa['source']}): \"{sa['quote']}\"")
        if a["category"] == "desirability":
            desirability_for += m["mass"]["for"]
        total_behavioral_or_paid += m["behavioral_or_paid_for"]
        s5_against_total += m["human_against_strength5"]
    print("\n" + "-" * 62)
    checks = [
        ("desirability FOR-mass >= "
         f"{rule['min_for_mass_desirability']}", desirability_for >= rule["min_for_mass_desirability"]),
        (f"behavioral/paid FOR atoms >= {rule['min_behavioral_or_paid_atoms']}",
         total_behavioral_or_paid >= rule["min_behavioral_or_paid_atoms"]),
        (f"unrebutted strength-5 human AGAINST atoms <= "
         f"{rule['max_unrebutted_strength5_against']}",
         s5_against_total <= rule["max_unrebutted_strength5_against"]),
    ]
    for label, ok in checks:
        print(f"  [{'PASS' if ok else 'FAIL'}] {label}")
        build_ok = build_ok and ok
    print("-" * 62)
    if build_ok:
        print("VERDICT: BUILD-grade evidence under the pre-registered rule.")
    else:
        print("VERDICT: NOT build-grade. Consult the pivot/kill clauses:")
        print(f"  PIVOT: {ledger['decision_rule']['pivot']}")
        print(f"  KILL:  {ledger['decision_rule']['kill']}")
    print("Kill criteria are evaluated by YOU against human-class atoms only; "
          "synthetic atoms (weight 0.0) can never trip or rescue them.")
    if ledger["overrides"]:
        print(f"\nNOTE: {len(ledger['overrides'])} override(s) on record. "
              "Overrides are part of the verdict's audit trail:")
        for o in ledger["overrides"]:
            print(f"  - {o['when']}: {o['what']} — {o['reason']}")


def cmd_report(args: argparse.Namespace) -> None:
    ledger = load_ledger(Path(args.ledger))
    lines = ["# Evidence ledger report", "",
             f"Registered: {ledger['registered_on']}  ·  Generated: {now_iso()}", ""]
    lines += ["| Class | Weight |", "|---|---|"]
    for k, v in ledger["weights"].items():
        lines.append(f"| {k} | {v} |")
    for a in ledger["assumptions"]:
        m = assumption_masses(ledger, a["id"])
        lines += ["", f"## [{a['id']}] {a['text']}", "",
                  f"- Category: **{a['category']}** · Kill criterion: {a['kill_criterion']}",
                  f"- Weighted mass — FOR: **{m['mass']['for']:.1f}** · "
                  f"AGAINST: **{m['mass']['against']:.1f}** · NEUTRAL: {m['mass']['neutral']:.1f}",
                  "", "| Dir | Class | S | Source | Channel | Quote |", "|---|---|---|---|---|---|"]
        for e in ledger["evidence"]:
            if e["assumption"] == a["id"]:
                quote = " ".join(str(e["quote"]).split()).replace("|", "\\|")
                lines.append(f"| {e['direction'].upper()} | {e['source_class']} | "
                             f"{e['strength']} | {e['source']} | {e.get('channel','?')} | {quote} |")
    print("\n".join(lines))


def cmd_wilson(args: argparse.Namespace) -> None:
    lo, hi = wilson_interval(args.successes, args.trials)
    p = args.successes / args.trials if args.trials else 0.0
    print(f"{args.successes}/{args.trials} = {p:.1%}  ->  Wilson 95% CI [{lo:.1%}, {hi:.1%}]")
    print("Act on the interval, not the point. If your threshold sits inside "
          "the interval, the verdict is 'collect more n'.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("init", help="create a fresh ledger (pre-registration step)")
    p.add_argument("--ledger", default="ledger.json")
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("add-assumption", help="register an assumption + kill criterion")
    p.add_argument("--ledger", default="ledger.json")
    p.add_argument("--id", required=True)
    p.add_argument("--category", required=True, choices=CATEGORIES)
    p.add_argument("--text", required=True)
    p.add_argument("--kill", required=True, help="kill criterion, quantified")
    p.add_argument("--reason", help="required if evidence already exists (override)")
    p.set_defaults(func=cmd_add_assumption)

    p = sub.add_parser("add-evidence", help="log one evidence atom")
    p.add_argument("--ledger", default="ledger.json")
    p.add_argument("--assumption", required=True)
    p.add_argument("--direction", required=True, choices=DIRECTIONS)
    p.add_argument("--source-class", required=True, choices=SOURCE_CLASSES)
    p.add_argument("--strength", required=True, type=int)
    p.add_argument("--quote", required=True)
    p.add_argument("--source", required=True, help="e.g. P3, smoke-test-v2, dossier")
    p.add_argument("--channel", default="unknown", help="warm | cold | unknown")
    p.set_defaults(func=cmd_add_evidence)

    p = sub.add_parser("import-atoms", help="bulk import atoms from note_synthesizer.py")
    p.add_argument("--ledger", default="ledger.json")
    p.add_argument("--atoms", required=True)
    p.set_defaults(func=cmd_import_atoms)

    p = sub.add_parser("verdict", help="evaluate the pre-registered decision rule")
    p.add_argument("--ledger", default="ledger.json")
    p.set_defaults(func=cmd_verdict)

    p = sub.add_parser("report", help="render the full ledger as markdown (stdout)")
    p.add_argument("--ledger", default="ledger.json")
    p.set_defaults(func=cmd_report)

    p = sub.add_parser("wilson", help="Wilson 95% interval for k/n")
    p.add_argument("--successes", required=True, type=int)
    p.add_argument("--trials", required=True, type=int)
    p.set_defaults(func=cmd_wilson)

    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
