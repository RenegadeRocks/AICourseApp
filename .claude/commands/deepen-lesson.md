---
description: Add more rigor or a specific angle to an existing lesson without regenerating from scratch.
argument-hint: <lesson-path> <what-to-deepen>
---

# /deepen-lesson $ARGUMENTS

Extend an existing lesson in place.

1. Read the target lesson file in full.
2. Identify where the new content belongs — usually a new subsection under
   "Core content" or a new "Worked example 2".
3. Research from Tier-1 sources (see `generate-lesson` for list).
4. **Append, don't rewrite**. Preserve existing structure, citations, and
   user-added notes.
5. If the deepening introduces new code, add `code-lab/<N+1>/` without
   disturbing existing labs.
6. Update the lesson's `last_verified:` stamp and append a bullet to a
   `## Revisions` section at the bottom:
   `- YYYY-MM-DD: added section on <topic> via /deepen-lesson`.
7. Commit: `git commit -m "deepen: <file> — <what>"`
