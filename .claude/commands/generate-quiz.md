---
description: Generate a fresh quiz for a week (or specific lesson). 10-15 questions, mixed format, answer key included.
argument-hint: <week-slug>   e.g. block-0-basecamp/week-01
---

# /generate-quiz $ARGUMENTS

Generate a quiz grounded ONLY in the content of the target week's lesson files.

1. Read all lesson files under `vault/$ARGUMENTS/` (skip `_week.md`,
   `00-overview.md`, existing quizzes).
2. Produce **10–15 questions** mixing:
   - 4–6 MCQs (4 options each, 1 correct, distractors plausible)
   - 3–5 short-answer (3–4 sentence answers)
   - 2–4 code-completion or debugging (runnable)
3. Target difficulty: **70–85 % expected score for someone who studied the
   week**. Too easy = useless. Too hard = discouraging.
4. Each question references the source lesson and citation:
   `_Source: 02-tue-tokenization-internals.md, [^3]_`.
5. Write to `vault/$ARGUMENTS/05-quiz.md` with:
   - Questions at the top (no answers)
   - `---` separator
   - Answer key + explanations below

Do **not** recycle questions that already exist in `05-quiz.md` — diff against
the file and generate net-new items if regenerating.
