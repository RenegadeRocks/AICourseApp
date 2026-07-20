# Week 21 code-lab — complete-system map + content-engine planner

Two tools that produce the two Saturday artifacts:

1. **`system_map.py`** — validate your complete-system map. Flags any subsystem
   that is an *orphan* (missing a metric, owner, SOP, or a wikilink to the course
   week that built it) and any *handoff dead-end* (nothing flows in, or nothing
   flows out). Passing this is the week's pass bar for the system half.
2. **`content_engine.py`** — plan and measure the content engine: a cadence-based
   **calendar**, a one-pillar-to-many **repurposing matrix**, and the four
   **engine-health metrics** with pass/fail flags.

`planner.py` is the CLI that ties them together.

## Requirements

Python 3.10+. No third-party packages (see `requirements.txt`).

## Run

```bash
cd code-lab/1

# validate the example system map (should PASS — no orphans)
python planner.py system system.example.json

# plan + measure the example content engine
python planner.py engine engine.example.json

# run both
python planner.py all
```

## Make it yours

- Copy `system.example.json` and replace the three subsystems with your own.
  Every subsystem needs a `metric`, `owner`, `sop`, and `built_in` wikilink, plus
  a `handoff_to` list that forms a closed loop (demand -> delivery -> money ->
  demand). Delete any one field to watch the checklist flag it — that is the
  tool doing its job.
- Copy `engine.example.json` and set your real `start_date`, `cadence_days`
  (14 = biweekly, the sustainable default), your `pillars`, your channels, and
  your last 8 weeks of `metrics`. The health thresholds live in
  `content_engine.THRESHOLDS` and match the 2026 creator-newsletter baselines
  cited in the Thursday lesson.

## Files

| File | What it does |
|---|---|
| `system_map.py` | orphan + handoff validation, map + checklist rendering |
| `content_engine.py` | calendar, repurposing matrix, engine-health metrics |
| `planner.py` | CLI (`system` / `engine` / `all`) |
| `system.example.json` | a clean three-subsystem loop (passes) |
| `engine.example.json` | a biweekly engine with 4 pillars |

## Pass bar

- `python planner.py system <yours>` prints `PASS — no orphan subsystems`.
- `python planner.py engine <yours>` prints `STATUS: HEALTHY` (or names exactly
  which metric to investigate).
