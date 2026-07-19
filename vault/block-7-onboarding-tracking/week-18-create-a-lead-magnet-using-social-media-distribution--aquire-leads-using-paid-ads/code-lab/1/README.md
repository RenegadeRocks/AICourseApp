# Code-lab 1 — Lead-gen & paid-test calculator + distribution planner

Companion to **Week 18, Saturday** ([[../../06-sat-build-the-lead-gen-engine]]).
Two small, dependency-free tools that do this week's demand-capture math in
seconds and refuse to let you lie to yourself about it.

## What's here

| File | What it does |
|---|---|
| `funnel_metrics.py` | opt-in rate, confirmation rate, CPL, CAC, blended CAC, LTV:CAC, multi-stage funnel roll-up (with weakest handoff), and the **pre-registered paid-test decision rule** (SCALE / KILL / KEEP_TESTING / INSUFFICIENT_DATA) |
| `distribution_planner.py` | turns one anchor idea into five platform-native expressions and builds an N-week publishing plan (one idea per week, repurposed) |
| `test_funnel_metrics.py` | 14 assertions pinning the behavior; doubles as a compile check |

## Requirements

- **Python 3.10+** (uses `X | None` union syntax). No pip installs. Stdlib only.
  See `requirements.txt` (intentionally empty).

## Run it

```bash
cd code-lab/1

# run the tests (should print "OK — 14 tests passed")
python test_funnel_metrics.py

# see the calculator demo
python funnel_metrics.py

# see the distribution planner demo
python distribution_planner.py
```

## Pass bar

`python test_funnel_metrics.py` prints `OK — 14 tests passed`, and you can
explain each of these to a skeptic:

1. **Opt-in rate, not subscriber count.** The tool reports the *ratio*
   (submissions ÷ visitors) because the raw count always rises and diagnoses
   nothing (Week 18 Tue). Confirmation rate isolates double-opt-in friction.
2. **CPL is a leading indicator; CAC is the truth.** The demo shows a $6.25 CPL
   sitting on top of a $117 CAC. A cheap lead that never converts is not cheap.
   `blended_cac` is attribution-free by construction, so it survives 2026's
   broken attribution (Week 18 Fri).
3. **The funnel roll-up finds the weakest handoff.** In the demo the overall
   visitor→customer rate is 0.54%, and the weakest step is trials→customers
   (15%) — the one place a fix moves the whole funnel most.
4. **The paid-test rule refuses to decide on noise.** A great-looking CAC on
   only 4 customers returns `INSUFFICIENT_DATA`, not `SCALE`. The rule is
   **pre-registered** (target CAC, scale line, kill line, min spend, min
   customers) *before* you spend, which is the only defense against sunk-cost
   rationalization and small-N panic (Week 18 Fri).

## Use it on your own numbers

```python
from funnel_metrics import funnel_conversion, paid_test_decision, PaidTestRule

# your real funnel counts, largest first
funnel = {"visitors": 4000, "opt_ins": 900, "confirmed": 650,
          "trials": 140, "customers": 19}
print(funnel_conversion(funnel))   # find YOUR weakest handoff

# pre-register BEFORE you spend (target_cac from your LTV, B6W16)
rule = PaidTestRule(target_cac=150, scale_below=120, kill_above=200,
                    min_spend=1000, min_customers=5)
print(paid_test_decision(spend=1050, customers=9, rule=rule))
```

```python
from distribution_planner import plan_campaign

for wp in plan_campaign(
    ["your week-1 anchor idea", "your week-2 anchor idea"],
    "https://yoursite.com/your-magnet",
):
    print(wp.week, wp.anchor_idea)
```

## Honesty notes

- The CAC target, scale line, and kill line are **yours to set from your unit
  economics** (Week 16). The tool enforces the rule; it does not invent the
  numbers.
- The paid-test guard's `min_customers=5` is a floor for "don't decide on noise,"
  not a substitute for the Wilson-interval thinking in
  [[../../../../block-2-ai-employees/week-03-building-elegant-landing-pages--how-to-build-micro-prototypes/06-sat-validation-instrumentation]].
  More customers = a tighter estimate; five is the minimum to have a conversation.
- Format guidance in `distribution_planner.py` (carousel ER, link penalty) is a
  **2026 snapshot** and decays fast. Re-verify before betting a plan on it.
- No network, no API keys, no external services. Everything runs offline.
