---
description: Build one EPUB of all vault lessons for Kindle (Send-to-Kindle). Optionally block-scoped.
argument-hint: [block-slug]
---

# /export-epub $ARGUMENTS

Run `python scripts/export_epub.py` (add `--block $ARGUMENTS` if a block slug
was given) which:

1. Walks `vault/`, skipping underscore-prefixed files/dirs (archives,
   `_review.md`, `_refresh-*.md`, the pilot week) and `00-program/`.
2. Converts each lesson markdown to validated XHTML (frontmatter stripped,
   wikilinks become internal chapter links where the target lesson is in the
   book, plain italics otherwise).
3. Packages an EPUB 3 with nested Block → Week → Lesson TOC, a generated
   1600×2560 cover, `mimetype` entry first and stored (spec requirement).
4. Writes `exports/ai-pro-level-course.epub` and prints the path + size.

Deliver the resulting file to the user (it's their Kindle copy — they send it
via Send-to-Kindle). `exports/` is gitignored; the EPUB is regenerated from
the vault on demand, typically after new weeks are generated or lessons are
refreshed. The EPUB replaces the old Notion mirror as the read-elsewhere
output of this course.
