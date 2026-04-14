---
type: quality-standard
---

# Lesson Quality Standard

Every lesson `.md` in this vault must satisfy every rule below.

## 1. Primary-source citations (non-negotiable)

- **5–12 citations per lesson**, drawn from the tiered list in
  [index](index.md#master-reading-list).
- Every non-trivial claim has an inline footnote `[^1]` with:
  - URL
  - Author name
  - Publication / video / paper title
  - Timestamp (for videos) or page (for books/papers)
- Tier-1 sources (Karpathy, Anthropic docs, fast.ai, YC, original papers) must
  appear in every lesson. Secondary sources (blogs, tutorials) supplement,
  never replace.
- **If a claim can't be cited to a Tier-1 source**, write it as an opinion
  labeled clearly: `> My take: …`

## 2. Required sections (enforced template)

```
---
type: lesson
block: <block-id>
week: <week-id>
session_slug: <session-slug>
day_of_cycle: <1-7>
date_due: YYYY-MM-DD
tags: [...]
sources: [...]            # bibliographic list
---

# <Title>

## Why this matters (operator framing)
What will you build, sell, or decide with this? In 3–5 sentences.

## Prerequisites
[[links]] to earlier lessons or external primers.

## Core content
First principles → mechanics → tradeoffs → production pitfalls.
Use headings, not walls of prose.

## Worked example
One concrete scenario. Code that runs. See `code-lab/<n>/`.

## Common mistakes experts see
List 5+ with a one-liner each.

## Reflection questions
5–10 questions. The answers should not be Googleable.

## My take (reviewer lens)
What would Karpathy / Seibel / Boris push back on here? Write it.

## Further reading
Ranked: **Must-read** / Recommended / Optional.

## Citations
[^1]: …
[^2]: …
```

## 3. Currency rule

- Lessons covering fast-moving topics (model releases, tool pricing, library
  APIs) must be regenerated within 7 days of the live session.
- Every lesson ends with a `_last_verified: YYYY-MM-DD` stamp.
- `/refresh-curriculum` diffs the xlsx and flags weeks whose official topic
  text has changed; those get regenerated.

## 4. Runnable code

- Every code block marked with a language runs as-is.
- Dependencies pinned: `code-lab/<n>/requirements.txt` or `package.json`.
- Include a `README.md` in each `code-lab/<n>/` with the exact command to run.
- If the code requires an API key, document which env var in the README, but
  never commit the key.

## 5. Reviewer lens

Every lesson closes with "My take" — a one-paragraph critical response to the
lesson itself. Questions it answers:

- Where would Karpathy say "wait, that's not quite right"?
- Where would Michael Seibel say "you're overthinking, just do the ugly thing"?
- Where would Boris Cherny point out a tooling pitfall?

This trains taste, not just knowledge.

## 6. Length

- **Core lesson**: 2000–4000 words. Shorter is lazy; longer is padded.
- **Exercises**: 300–800 words with 3–5 graduated problems.
- **Quiz**: 10–15 questions, mix of MCQ / short-answer / code-completion.
- **Flashcards**: 15–30 cards covering key concepts, terms, and tradeoffs.

## 7. Internal linking

- Every lesson links to at least 2 other vault lessons via `[[wikilinks]]`.
- No dead links. Scaffolded files are placeholders — link to the folder and
  mark the link with `(pending)` if the target isn't generated yet.
