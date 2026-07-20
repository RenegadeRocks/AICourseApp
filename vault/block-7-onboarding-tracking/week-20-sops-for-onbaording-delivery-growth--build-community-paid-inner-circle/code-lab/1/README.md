# code-lab/1 — SOP generator + membership economics model

Two small, dependency-free tools for Week 20's Saturday build. Together they
produce a runnable SOP and the numbers that tell you whether your paid community
is a business or a treadmill (and whether it is quietly dying).

## Requirements

- Python 3.10+ (uses `X | Y` unions and `list[...]` generics). No third-party
  packages. See `requirements.txt`.

## Run it

```bash
# from this directory
python sop_generator.py       # renders two example SOPs + agent/human verdicts
python membership_model.py    # prints unit economics + ghost-town warning demo
```

Optional compile check (should print nothing and exit 0):

```bash
python -m py_compile sop_generator.py membership_model.py
```

## What each tool does

### `sop_generator.py`
Turns a structured `SOPSpec` (title, trigger, ordered steps, definition of done,
owner, version, failure modes) into a checklist-form Markdown SOP, and runs the
Wednesday SOP-to-agent rubric to label each procedure **AGENT-CANDIDATE**,
**AGENT-ASSIST**, **HUMAN-IN-THE-LOOP**, or **HUMAN-RUN** based on frequency,
judgment, and cost of error.

Use it: build a `SOPSpec` for each of your three core SOPs (onboarding, delivery,
one growth), call `render_sop(spec)`, and read the run-mode verdict to decide
what graduates into automation.

### `membership_model.py`
Computes `mrr`, `arpu`, `avg_lifetime_months`, `ltv`, `ltv_cac_ratio`, and
`net_mrr_movement` from your tiers and churn assumptions, then
`ghost_town_warning(history)` raises a risk flag from a list of weekly
`EngagementSnapshot`s.

The ghost-town flag fires when the **active-member ratio** is below the floor,
OR it has declined for several consecutive periods, OR **new-member first-week
activation** is below the floor. Engagement leads churn by weeks, so this is the
smoke alarm; MRR/churn are the fire.

Use it: plug in your own tiers, churn estimate, gross margin, and CAC, then feed
real weekly engagement counts into `ghost_town_warning`.

## Pass bar (Saturday)

1. `python sop_generator.py` renders your three real SOPs (edit `_demo` or build
   specs in a REPL) with sensible run-mode verdicts.
2. `python membership_model.py` prints your membership's MRR, LTV, and LTV:CAC,
   and correctly flags a declining engagement history as `GHOST_TOWN_RISK`.
3. You can state, from the output, your break-even member count and the churn
   level at which your LTV:CAC drops below 3:1.

## Tuning

Thresholds live at the top of `membership_model.py`:
`ACTIVE_RATIO_FLOOR`, `FIRST_WEEK_ACTIVATION_FLOOR`, `DECLINE_PERIODS`. Adjust to
your community's baseline once you have a few weeks of real data — a niche
professional community runs hotter than a broad free one.
