#!/usr/bin/env python3
"""note_synthesizer.py — interview-note synthesizer with for/against tagging.

Week 11, Block 4 (AI Pro-level Course). Pure stdlib; Python 3.10+.

Takes interview transcripts/notes (plain text or markdown) plus your registered
assumptions (from ledger.json) and produces evidence ATOMS: one claim per atom,
tagged with assumption id, direction (for/against/neutral), source class, and a
0-5 strength score with a verbatim quote.

Two modes:
  * Claude mode (default): shells out to the `claude` CLI (`claude -p`), same
    pattern as the course app's chat route. No API key needed on a subscription
    machine. The prompt instructs the model to prefer AGAINST when ambiguous
    (anti-sycophancy, per Thursday's lesson) and to quote verbatim.
  * --offline mode: heuristic keyword tagger. Deliberately dumb; exists so the
    pipeline runs anywhere and so you feel the difference labeling quality makes.

Anti-cherry-picking guarantees:
  * Refuses to emit a FOR atom without a verbatim quote.
  * Warns if any transcript produced zero AGAINST/NEUTRAL atoms
    (Wednesday's disconfirmation quota).
  * --audit N prints a random sample of FOR atoms for blind human re-tagging
    (Hamel's inter-annotator hygiene).

Usage (see README.md):
  python note_synthesizer.py --ledger ledger.json --notes interviews/ --out atoms.json
  python note_synthesizer.py --ledger ledger.json --notes interviews/P1.md \
      --source-class stated --offline --out atoms.json
  python note_synthesizer.py --audit 5 --atoms atoms.json
"""

from __future__ import annotations

import argparse
import json
import random
import re
import shutil
import subprocess
import sys
from pathlib import Path

DIRECTIONS = ("for", "against", "neutral")
SOURCE_CLASSES = ("desk", "synthetic", "stated", "behavioral", "paid")

CLAUDE_PROMPT = """You are an evidence auditor for a founder validating their own product idea.
The founder's motivated reasoning is the enemy: when a statement is ambiguous,
tag it AGAINST or NEUTRAL, never FOR. Compliments and hypothetical enthusiasm
("sounds great", "I'd totally use that") are strength 0 NEUTRAL by rule.

ASSUMPTIONS UNDER TEST (id: text · kill criterion):
{assumptions}

TRANSCRIPT (source id: {source_id}):
---
{transcript}
---

Extract evidence atoms. One atom = one specific claim, story, or commitment.
For each atom output an object with EXACTLY these keys:
  "assumption": one of the assumption ids above (skip material touching none),
  "direction": "for" | "against" | "neutral",
  "strength": integer 0-5
      (0 compliment/vague; 1 general opinion; 2 specific but undated/second-hand;
       3 dated specific past instance or working workaround;
       4 specific instance with named consequence, or abandoned paid workaround;
       5 currency: time scheduled, intro made, money moved or refused with reasons),
  "quote": verbatim quote from the transcript (required, <= 40 words),
  "source": "{source_id}"

Every atom needs its quote copied verbatim. Extract at least one AGAINST or
NEUTRAL atom if the transcript contains ANY hedge, objection, or contradiction.
Respond with ONLY a JSON array of atom objects, no prose, no code fences."""

# Heuristic vocab for --offline mode. Crude on purpose.
AGAINST_HINTS = re.compile(
    r"\b(but|however|wouldn'?t|don'?t need|stopped|turned it off|gave up|too "
    r"(?:expensive|slow|risky)|not (?:a|the) (?:problem|priority)|myself|"
    r"prefer to|fine as is|no budget)\b", re.I)
FOR_HINTS = re.compile(
    r"\b(last (?:week|month|thursday|friday|tuesday)|every (?:week|day|month)|"
    r"hours? (?:per|a|each)|missed|late|forgot|complained|cost (?:us|me)|"
    r"paid? for|hired|tried|workaround|spreadsheet|manually)\b", re.I)
CURRENCY_HINTS = re.compile(
    r"\b(intro(?:duce)?|pilot|pre-?order|deposit|sign(?:ed)? up|paid|invoice|"
    r"next (?:week|month) .{0,20}(?:call|meet))\b", re.I)
COMPLIMENT_HINTS = re.compile(
    r"\b(sounds (?:great|good|awesome)|love (?:it|that|this)|definitely (?:would|use)|"
    r"cool idea|i'?d totally)\b", re.I)


def load_assumptions(ledger_path: Path) -> list[dict]:
    ledger = json.loads(ledger_path.read_text(encoding="utf-8"))
    if not ledger.get("assumptions"):
        sys.exit("Ledger has no registered assumptions. Register them first (Monday's job).")
    return ledger["assumptions"]


def gather_note_files(notes_arg: str) -> list[Path]:
    p = Path(notes_arg)
    if p.is_dir():
        files = sorted(q for q in p.iterdir() if q.suffix.lower() in (".md", ".txt"))
    else:
        files = [p]
    if not files:
        sys.exit(f"No .md/.txt notes found at {notes_arg}")
    return files


def claude_extract(transcript: str, source_id: str, assumptions: list[dict],
                   model_flag: str | None) -> list[dict]:
    if shutil.which("claude") is None:
        sys.exit("`claude` CLI not on PATH. Install it, or re-run with --offline.")
    assumption_block = "\n".join(
        f'  {a["id"]}: {a["text"]} · kill: {a["kill_criterion"]}' for a in assumptions)
    prompt = CLAUDE_PROMPT.format(
        assumptions=assumption_block, transcript=transcript[:24000], source_id=source_id)
    cmd = ["claude", "-p", prompt]
    if model_flag:
        cmd += ["--model", model_flag]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
    except subprocess.TimeoutExpired:
        sys.exit("claude CLI timed out after 300s. Try a shorter transcript or --offline.")
    if out.returncode != 0:
        sys.exit(f"claude CLI failed: {out.stderr.strip()[:400]}")
    text = out.stdout.strip()
    match = re.search(r"\[.*\]", text, re.S)  # tolerate stray prose/fences
    if not match:
        sys.exit(f"Could not find a JSON array in claude output:\n{text[:400]}")
    try:
        atoms = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        sys.exit(f"claude output was not valid JSON ({e}). Re-run, or use --offline.")
    return atoms if isinstance(atoms, list) else []


def offline_extract(transcript: str, source_id: str, assumptions: list[dict]) -> list[dict]:
    """Sentence-level heuristic tagger. A floor, not a standard."""
    default_assumption = assumptions[0]["id"]
    atoms: list[dict] = []
    sentences = re.split(r"(?<=[.!?])\s+", transcript)
    for s in sentences:
        # normalize whitespace and strip markdown speaker prefixes like "**P3:**"
        s = " ".join(s.split()).strip()
        s = re.sub(r"^\*\*[^*]{1,20}\*\*:?\s*", "", s)
        if len(s) < 25:
            continue
        quote = s if len(s.split()) <= 40 else " ".join(s.split()[:40]) + "..."
        if COMPLIMENT_HINTS.search(s):
            atoms.append({"assumption": default_assumption, "direction": "neutral",
                          "strength": 0, "quote": quote, "source": source_id})
        elif CURRENCY_HINTS.search(s):
            atoms.append({"assumption": default_assumption, "direction": "for",
                          "strength": 5, "quote": quote, "source": source_id})
        elif AGAINST_HINTS.search(s):
            atoms.append({"assumption": default_assumption, "direction": "against",
                          "strength": 2, "quote": quote, "source": source_id})
        elif FOR_HINTS.search(s):
            atoms.append({"assumption": default_assumption, "direction": "for",
                          "strength": 3, "quote": quote, "source": source_id})
    return atoms


def validate_atoms(atoms: list[dict], source_class: str, valid_ids: set[str]) -> list[dict]:
    clean: list[dict] = []
    for atom in atoms:
        if atom.get("assumption") not in valid_ids:
            continue
        if atom.get("direction") not in DIRECTIONS:
            continue
        if not isinstance(atom.get("strength"), int) or not 0 <= atom["strength"] <= 5:
            continue
        if atom["direction"] == "for" and not str(atom.get("quote", "")).strip():
            continue  # no FOR without a verbatim quote — anti-cherry-picking rule
        atom["source_class"] = source_class
        clean.append(atom)
    return clean


def cmd_audit(atoms_path: Path, n: int) -> None:
    atoms = json.loads(atoms_path.read_text(encoding="utf-8"))
    fors = [a for a in atoms if a.get("direction") == "for"]
    if not fors:
        print("No FOR atoms to audit. (Suspicious in the other direction, honestly.)")
        return
    sample = random.sample(fors, min(n, len(fors)))
    print(f"BLIND AUDIT — re-tag these {len(sample)} FOR atoms yourself, "
          "without looking at the stored tags. Then compare.\n")
    for i, a in enumerate(sample, 1):
        print(f"{i}. [{a.get('source','?')}] \"{a.get('quote','')}\"")
        print("   your direction? your strength (0-5)?  "
              f"(stored: {a['direction']}/s{a['strength']}, "
              f"assumption {a.get('assumption')})\n")
    print("If your blind re-tags disagree on direction for >1 in 5, your tagging "
          "run is not decision-grade. Re-run with a stricter prompt or a peer.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--ledger", default="ledger.json", help="ledger with registered assumptions")
    ap.add_argument("--notes", help="transcript file or directory of .md/.txt files")
    ap.add_argument("--out", default="atoms.json", help="output atoms JSON")
    ap.add_argument("--source-class", default="stated", choices=SOURCE_CLASSES,
                    help="stated for human interviews; synthetic for simulated panels "
                         "(synthetic atoms carry weight 0.0 in the ledger, by rule)")
    ap.add_argument("--offline", action="store_true", help="heuristic mode, no claude CLI")
    ap.add_argument("--model", default=None, help="optional model for `claude --model`")
    ap.add_argument("--audit", type=int, metavar="N",
                    help="print N random FOR atoms from --atoms for blind re-tagging")
    ap.add_argument("--atoms", default="atoms.json", help="atoms file for --audit")
    args = ap.parse_args()

    if args.audit is not None:
        cmd_audit(Path(args.atoms), args.audit)
        return

    if not args.notes:
        ap.error("--notes is required (unless running --audit)")

    assumptions = load_assumptions(Path(args.ledger))
    valid_ids = {a["id"] for a in assumptions}
    files = gather_note_files(args.notes)

    all_atoms: list[dict] = []
    for f in files:
        transcript = f.read_text(encoding="utf-8")
        source_id = f.stem
        if args.offline:
            raw = offline_extract(transcript, source_id, assumptions)
        else:
            raw = claude_extract(transcript, source_id, assumptions, args.model)
        atoms = validate_atoms(raw, args.source_class, valid_ids)
        n_against = sum(1 for a in atoms if a["direction"] in ("against", "neutral"))
        flag = ""
        if atoms and n_against == 0:
            flag = "  ⚠ ZERO against/neutral atoms — disconfirmation quota unmet; re-read this one."
        print(f"{f.name}: {len(atoms)} atoms "
              f"({sum(1 for a in atoms if a['direction']=='for')} for / {n_against} against+neutral){flag}")
        all_atoms.extend(atoms)

    Path(args.out).write_text(json.dumps(all_atoms, indent=2, ensure_ascii=False),
                              encoding="utf-8")
    print(f"\nWrote {len(all_atoms)} atoms to {args.out}.")
    print(f"Import with: python evidence_ledger.py import-atoms --ledger {args.ledger} "
          f"--atoms {args.out}")
    if args.source_class == "synthetic":
        print("Reminder: synthetic atoms are design inputs, weight 0.0. "
              "They cannot trip or rescue kill criteria.")


if __name__ == "__main__":
    main()
