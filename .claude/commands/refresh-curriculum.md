---
description: Re-parse the curriculum xlsx, diff against curriculum.json, flag affected weeks for regeneration.
---

# /refresh-curriculum

When the upstream curriculum xlsx is updated, run this to pick up the
changes.

1. Run `python scripts/parse_xlsx.py` to re-parse the xlsx.
2. **Diff** the new `curriculum.json` against the previously committed version
   using `git diff HEAD -- curriculum.json`.
3. For each changed session (title changed, new session added, date changed):
   - Identify the affected week folder under `vault/`.
   - If session **title** changed: regenerate that week with
     `/generate-lesson <block>/<week>` (dispatch a subagent).
   - If session **date** changed: update `date_due:` frontmatter in each daily
     lesson for that week.
   - If new session added: regenerate the week.
4. For each unchanged session: leave content as-is.
5. Summarize the diff to the user before regenerating. Confirm before writing.
6. After regeneration, run `python scripts/scaffold_vault.py` to ensure any
   new folders exist.
7. Commit: `git commit -m "refresh: curriculum diff from xlsx"`
