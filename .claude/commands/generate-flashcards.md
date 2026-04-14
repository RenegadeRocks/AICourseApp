---
description: Generate Anki-ready flashcards (front/back) for a week. Atomic, testable, one concept per card.
argument-hint: <week-slug>
---

# /generate-flashcards $ARGUMENTS

Generate 15–30 flashcards from the week's lesson files.

## Rules

1. **Atomic** — one concept per card.
2. **Testable** — the front asks a question that has a specific correct answer,
   not "tell me everything about X".
3. **Cloze-friendly** — favor "What does {{c1::contextual retrieval}} add on top
   of BM25+embeddings?" style when it sharpens recall.
4. **Mix types**:
   - Definitions (term → meaning)
   - Tradeoffs (X vs Y → when to pick each)
   - Code patterns (what does this snippet do?)
   - Debugging (given symptom → likely root cause)
5. **No giveaways** — the front must not contain the answer.

## Output

Write to `vault/$ARGUMENTS/06-flashcards.md`:

```
---
type: flashcards
count: <N>
week: $ARGUMENTS
---

# Flashcards — <Week Title>

Q: …
A: …

---

Q: …
A: …
```

The `export-anki` command will parse this `Q:/A:/---` format into a `.apkg`
deck — keep formatting strict.
