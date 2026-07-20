---
type: lesson
block: block-8-wind-up-checklists
week: week-22
session_slug: final-thoughts-recap-checklists-2
day_of_cycle: 6
day_name: sat
date_due: 2026-10-17
tags:
  - capstone
  - build
  - graduation-artifact
  - code-lab
sources:
  - gawande-checklist-manifesto
  - hamel-evals
  - anthropic-pricing-2026
  - forte-para-pkm
last_verified: 2026-07-17
---

# BUILD: your personalized graduation artifact

## Why this matters (operator framing)

Today the recap becomes an object you own. By the end of this build you will have
four things, all dated, all personal to your business: a scored self-audit, a
90-day plan, a durable-principles one-pager, and a re-verification schedule.
These are not keepsakes. They are the operating documents you will actually run
after the course ends, the first artifacts of a business that outlives the class. The code-lab turns three of them into runnable tools so
the scoring, the plan scaffold, and the re-verification cadence are computed, not
guessed. This is the last build of the program. Make it real, not tidy.

## Prerequisites

The whole week. Specifically [[02-tue-the-master-build-checklist|Tuesday's checklist]], [[03-wed-the-durable-principles|Wednesday's principles]], [[04-thu-staying-current-re-verification|Thursday's re-verification practice]], and [[05-fri-the-forward-path-next-90-days|Friday's 90-day plan]]. Today assembles them; it does not re-teach them.

## The artifact, four parts

**Part 1: the self-audit (a number and a gap list).** Score your real business
against the 35 items using `graduation_audit.py`. The tool returns a total out of
70, a stage band, and a gap list ranked by how much revenue each gap blocks. Do
not score the business you wish you had. The value is entirely in the honesty; a
flattering audit produces a useless plan.

**Part 2 — the 90-day plan (dated, falsifiable).** Feed your audit result and your
worst gap into `plan_generator.py`. It produces three 30-day sprints keyed to your
stage, with the stage's single highest-leverage action pre-filled and blanks for
the falsifiable outcome, weekly leading indicator, and no-list. You supply the
judgment. A plan without a date and a falsifiable outcome is a wish.

**Part 3 — the durable-principles one-pager.** From [[03-wed-the-durable-principles|Wednesday's 14]], write the ones your business most needs on the wall, in your own words, one line each. This is not a copy of the lesson. It is the five or six principles you personally violate or forget, phrased so a version of you at 11pm will actually obey them.

**Part 4 — the re-verification schedule.** List the decaying facts your business
rests on and register them in `reverify_scheduler.py`. It tells you what is due and
what is already stale. This is the part most graduates skip and most regret,
because it is the one that keeps the other three from silently going wrong.[^1]

## The code-lab

All three tools live in [`code-lab/1/`](code-lab/1/README.md). They are pure
standard library, Python 3.10+, no dependencies. Run them in order:

```bash
cd code-lab/1
python graduation_audit.py      # demo: scores the Tuesday example at 41/70
python plan_generator.py        # demo: a Building-stage 3-sprint plan
python reverify_scheduler.py    # demo: two facts already overdue and stale
```

Then replace the demo data with yours. For the audit, build a dict mapping each
item id (1–35) to your honest `0/1/2`:

```python
import graduation_audit as ga

my_scores = {
    1: 2, 2: 2, 3: 1, 4: 1, 5: 1,       # Idea
    6: 2, 7: 2, 8: 1, 9: 0, 10: 0,      # Validated
    # ... fill all 35 honestly ...
}
result = ga.score(my_scores)
print(ga.render(result))
```

Take `result` straight into the plan:

```python
import plan_generator as pg
from datetime import date

stage = pg.stage_from_audit(result)
top_gap = "the #1 item you scored 0-or-1 that most blocks revenue"
plan = pg.build_plan(stage, date.today(), top_gap=top_gap)
print(pg.render_plan(stage, plan))
```

And register your real decaying facts in the scheduler:

```python
import reverify_scheduler as rs
from datetime import date

facts = [
    rs.Fact("my model's price per Mtok", "price",
            "https://platform.claude.com/docs/en/about-claude/pricing", date(2026, 7, 17)),
    rs.Fact("my default model", "model",
            "vendor changelog url", date(2026, 7, 17)),
    # ... your ~10 decaying facts ...
]
print(rs.report(facts, date.today()))
```

The scheduler's cadences encode Thursday's decay map: prices and models every 30
days, platform and competitor facts every 90, benchmarks every 60, principles
never. Note the demo's `last_verified` dates are 2026-07-17, so the price and
platform facts already show as overdue when you run it later — which is precisely
the point.[^2]

## Pass bar

You finish today with all four parts, printed and dated:

1. A real audit total out of 70, a band, and a written gap list ranked by revenue
   blocked. Not the demo — yours.
2. A dated three-sprint 90-day plan with one falsifiable outcome per sprint, a
   weekly leading indicator, and a no-list per sprint. Hamel Husain's evals
   discipline applied to yourself: each sprint has a measurable pass bar.[^3]
3. A durable-principles one-pager in your own words: the five or six you most
   need.
4. A re-verification schedule with at least your top decaying facts and their
   next-due dates.

If any part is generic enough that it could belong to another graduate, it is not
done. The artifact is worthless in the abstract and valuable only about your
specific business.

## Extend it (optional)

- **Weight the checklist to your model.** The `blocks_revenue` ranks in
  `graduation_audit.py` are defaults. If you are a services business, security and
  delivery may block more revenue than growth loops; adjust the ranks and re-run.
- **Persist your audit.** Add a function that writes `result` to a dated JSON file
  so you can diff this quarter's audit against next quarter's. The delta is your
  progress signal.
- **Wire the scheduler to real dates.** Replace the demo facts with your inventory
  and set a monthly calendar reminder to run it. A scheduler you never run is a
  file, not a practice.[^4]

## Common mistakes experts see

- **Scoring the aspiration.** The audit is only useful if it hurts a little.
- **A plan with no date or no falsifiable outcome.** "Grow revenue" is not a
  sprint outcome; "10 paying pilots by 18 Nov" is.
- **Copying Wednesday's principles verbatim.** The one-pager works only in your own
  words, aimed at the principles you personally break.
- **Skipping Part 4.** The re-verification schedule is the part that protects the
  other three from decaying into fiction.
- **Building the tool instead of using it.** The extensions are optional. The
  deliverable is a scored, dated artifact about your business, not a nicer script.

## Reflection questions

1. What is your honest total, and did any stage score lower than you expected?
2. Which single gap did the tool rank as your biggest revenue blocker, and is it
   your Sprint 1 outcome?
3. How many decaying facts does your business actually rest on, and how many were
   you tracking before today?
4. Which durable principle made your one-pager because you personally keep
   breaking it?
5. When, concretely, will you next run the audit and the scheduler? Put it in a
   calendar now.

## My take (reviewer lens)

**Boris Cherny** would check that the tools fail loudly and are trivial to run.
They validate the `0/1/2` inputs and the stage names, and they have zero
dependencies precisely so a graduate on any machine can run them without a setup
yak-shave. His likely note: persist the audit to disk by default so the
quarter-over-quarter diff is automatic, not a manual extension. Reasonable — do
the extension if you will actually re-audit.

**Seibel** would warn that a beautiful artifact can become a substitute for the
uncomfortable action it points to. The audit is not the work; closing the top gap
is. If you spend Saturday perfecting the one-pager and Monday avoiding the sales
call it identified, the tool failed you. Ship the artifact fast, then act on it.

**A cohort peer** who has run a real business would push on the checklist weights:
for a pure-services operator, several "product" items barely apply, and forcing a
0 there distorts the band. Fair — the `blocks_revenue` ranks and even which items
count are meant to be adjusted to your model, not obeyed literally.

## Further reading

- **Must-read:** [`code-lab/1/README.md`](code-lab/1/README.md) — exact run
  commands and what each tool does.
- **Recommended:** [[02-tue-the-master-build-checklist|Tuesday's checklist]] — the
  source of the 35 items you are scoring.
- **Optional:** Atul Gawande, *The Checklist Manifesto* — why a scored checklist
  beats confident memory.

## Citations

[^1]: AI Pro-level Course, "July 2026 Content Refresh — Master Findings Report," internal, 2026-07-17 — the concrete demonstration that unversioned facts decay silently; see [[04-thu-staying-current-re-verification|Thursday]].
[^2]: Anthropic, "Pricing," platform.claude.com/docs/en/about-claude/pricing — the price facts seeded into the scheduler demo (Opus 4.8 $5/$25) carry `last_verified: 2026-07-17` and are intentionally shown going stale. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)
[^3]: Hamel Husain, "Your AI Product Needs Evals," hamel.dev/blog/posts/evals/ — define a measurable pass bar before you ship; applied here to each 90-day sprint.
[^4]: Personal knowledge management practice, 2026 — a system compounds only if you run it consistently rather than redesign it; run the scheduler on a fixed cadence. Reported across atlasworkspace.ai, Jul 2026. (search-verified 2026-07-17; fetch egress-blocked — liveness pass pending)

_last_verified: 2026-07-17_
