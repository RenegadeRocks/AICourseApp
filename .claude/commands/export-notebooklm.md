---
description: Build a NotebookLM-ready bundle for a week (or block). Clean markdown, no wiki-links, no frontmatter bleed.
argument-hint: <week-or-block-slug>
---

# /export-notebooklm $ARGUMENTS

Create a clean bundle of markdown files that NotebookLM can ingest to produce
audio overviews, mind maps, and explainer videos.

## Process

1. Determine scope:
   - If `$ARGUMENTS` matches a week folder → bundle that week.
   - If `$ARGUMENTS` matches a block folder → bundle all weeks in that block.
2. For each lesson file in scope:
   - Strip YAML frontmatter.
   - Resolve `[[wikilinks]]` to plain text references (`see lesson: <title>`).
   - Inline `![image](...)` references by copying images into the pack.
   - Keep footnote citations intact — NotebookLM handles them well.
3. Write to `vault/<scope>/07-notebooklm-pack/`:
   - `README.md` — instructions: "Open NotebookLM → Create new notebook → Upload all `.md` files in this folder."
   - One `.md` per lesson (clean).
   - A single `bundle.md` concatenating all lessons in cycle order for
     single-upload convenience.
4. Do **not** delete existing pack files; overwrite only files you regenerate.

## Known NotebookLM limits

- Free tier: up to 50 sources per notebook. A full block can exceed this —
  offer the user a "top N most important" trimmed bundle.
- NotebookLM handles markdown tables, code blocks, and inline links well.
- It ignores frontmatter-looking YAML at the top of files but can get
  confused by nested frontmatter — always strip before export.
