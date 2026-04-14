"""
Parse vault/**/06-flashcards.md and produce a .apkg Anki deck.

Usage:
  python scripts/anki_export.py <scope>
    <scope> = "all" | "<block-id>" | "<block-id>/<week-folder>"

Flashcard format inside 06-flashcards.md:
  Q: <front>
  A: <back>
  ---
  Q: ...
  A: ...

Multi-line answers allowed between Q: and the next --- separator.
"""
from __future__ import annotations
import hashlib
import re
import sys
from pathlib import Path

try:
    import genanki
except ImportError:
    sys.stderr.write("Install deps: pip install -r scripts/requirements.txt\n")
    raise

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"
OUT_DIR = ROOT / "exports" / "anki"


MODEL_ID = 1607392319
DECK_ROOT = "AI Catalyst C3"

MODEL = genanki.Model(
    MODEL_ID,
    "AIC Basic",
    fields=[{"name": "Front"}, {"name": "Back"}, {"name": "Source"}],
    templates=[
        {
            "name": "Card 1",
            "qfmt": "{{Front}}",
            "afmt": "{{FrontSide}}<hr id='answer'>{{Back}}<br><br><small>{{Source}}</small>",
        }
    ],
    css="""
    .card { font-family: -apple-system, sans-serif; font-size: 18px;
            text-align: left; color: #1a1a1a; background: #fafaf7; padding: 14px; }
    hr#answer { margin: 12px 0; border: none; border-top: 1px solid #bbb; }
    small { color: #888; }
    """,
)


def parse_flashcards(md: str) -> list[tuple[str, str]]:
    # Split on lines that are exactly --- (optionally whitespace).
    blocks = re.split(r"\n\s*---\s*\n", md)
    cards: list[tuple[str, str]] = []
    for blk in blocks:
        blk = blk.strip()
        if not blk:
            continue
        m = re.search(r"^Q:\s*(.*?)\n+A:\s*(.*)$", blk, re.DOTALL | re.MULTILINE)
        if not m:
            continue
        front = m.group(1).strip()
        back = m.group(2).strip()
        if front and back:
            cards.append((front, back))
    return cards


def stable_guid(front: str, back: str) -> str:
    return hashlib.md5(f"{front}||{back}".encode("utf-8")).hexdigest()


def collect_files(scope: str) -> list[Path]:
    if scope == "all":
        return sorted(VAULT.rglob("06-flashcards.md"))
    scope_path = VAULT / scope
    if scope_path.is_file():
        return [scope_path]
    if scope_path.is_dir():
        return sorted(scope_path.rglob("06-flashcards.md"))
    return []


def main() -> int:
    scope = sys.argv[1] if len(sys.argv) > 1 else "all"
    files = collect_files(scope)
    if not files:
        print(f"No flashcard files found for scope: {scope}")
        return 1
    deck_name = f"{DECK_ROOT}::{scope}" if scope != "all" else DECK_ROOT
    deck = genanki.Deck(
        int(hashlib.md5(deck_name.encode()).hexdigest()[:8], 16),
        deck_name,
    )
    total = 0
    for f in files:
        md = f.read_text(encoding="utf-8")
        source = str(f.relative_to(ROOT))
        for front, back in parse_flashcards(md):
            note = genanki.Note(
                model=MODEL,
                fields=[front, back.replace("\n", "<br>"), source],
                guid=stable_guid(front, back),
            )
            deck.add_note(note)
            total += 1
    if total == 0:
        print("No cards parsed.")
        return 1
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"AI-Catalyst-{scope.replace('/', '-')}.apkg"
    genanki.Package(deck).write_to_file(out)
    print(f"[ok] {total} cards -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
