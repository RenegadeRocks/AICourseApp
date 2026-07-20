# code-lab/1 — Graduation-audit tool

Three small, dependency-free tools that produce your Week 22 graduation
artifact: a scored self-audit, a dated 90-day plan, and a re-verification
schedule. Together they turn the recap week into something you actually run.

## Requirements

- Python 3.10+ (uses `X | Y` unions and `list[...]` generics). No third-party
  packages. See `requirements.txt`.

## Run it

```bash
# from this directory
python graduation_audit.py      # scores the 35-item checklist -> total, band, ranked gaps
python plan_generator.py        # turns your stage + top gap into a 3-sprint 90-day plan
python reverify_scheduler.py    # shows what to re-verify and what is already stale
```

Optional compile check (should print nothing and exit 0):

```bash
python -m py_compile graduation_audit.py plan_generator.py reverify_scheduler.py
```

## What each tool does

### `graduation_audit.py`
Encodes the 35-item master build checklist from
[[02-tue-the-master-build-checklist|Tuesday]] across seven stages. Call
`score(scores)` with a dict mapping item id (1–35) to `0/1/2`. Returns a total
out of 70, a stage band, per-stage totals, and a **gap list ranked by how much
revenue each gap blocks** (biggest blocker first). The demo scores the Tuesday
worked example (a "Building"-stage business at 41/70).

Use it: score your real business honestly, read the band, and take the top gap
straight into the plan generator.

### `plan_generator.py`
Takes an audit `Result` (or a stage name) and a start date and produces a
three-sprint, 90-day plan scaffold keyed to your stage, from
[[05-fri-the-forward-path-next-90-days|Friday]]. It fills in the stage's single
highest-leverage action and the trap most likely to eat your quarter, and leaves
blanks for the falsifiable outcome, weekly leading indicator, and no-list you
must supply. Dates are computed as three 30-day windows from your start date.

Use it: run it with your real stage and your #1 gap, then fill the blanks by
hand. The tool supplies structure; you supply judgment.

### `reverify_scheduler.py`
Implements [[04-thu-staying-current-re-verification|Thursday's]]
re-verification practice. Register each decaying fact your business rests on as
a `Fact(name, kind, source, last_verified)`. `kind` maps to a cadence: `price`
and `model` every 30 days, `benchmark` every 60, `platform` and `competitor`
every 90, `principle` never (durable). The report sorts **overdue facts first**
and labels anything past its cadence "assume stale — verify before acting."

Use it: list your ten decaying facts, run the report monthly, and re-verify
whatever it flags against the primary source — never against memory or a single
snippet.

## Pass bar

You finish Saturday with: (1) a real audit total out of 70 and a written gap
list, (2) a dated three-sprint 90-day plan with one falsifiable outcome per
sprint, and (3) a re-verification schedule listing at least your top decaying
facts with their next-due dates. All three printed, dated, and saved.

## Note

These tools encode judgment frameworks, not truths. The checklist weights, the
stage actions, and the cadences are defaults from the Week 22 lessons — adjust
them to your business, and re-verify the model/price facts in
`reverify_scheduler.py`'s demo before quoting them (they carry a
`last_verified` of 2026-07-17).
