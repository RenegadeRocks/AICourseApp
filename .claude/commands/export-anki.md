---
description: Convert 06-flashcards.md files into a .apkg Anki deck. Block-scoped or week-scoped.
argument-hint: <week-or-block-slug>
---

# /export-anki $ARGUMENTS

Run `python scripts/anki_export.py $ARGUMENTS` which:

1. Finds every `06-flashcards.md` in scope.
2. Parses the `Q:/A:/---` format.
3. Builds a single `.apkg` deck named `AI-Catalyst-<scope>.apkg`.
4. Writes it to `exports/anki/`.
5. Prints the absolute path so the user can drag it into Anki.

If `scripts/anki_export.py` doesn't yet exist, generate it using the
`genanki` library (pinned in `scripts/requirements.txt`). Keep card templates
simple — plain front/back. Use `hashlib.md5(front+back)` as the stable
`guid` so re-exports update existing cards rather than duplicating them.
