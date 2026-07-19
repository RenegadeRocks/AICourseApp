# Code-lab 1 — Growth-metrics simulator + PMF-survey analyzer

Companion to **Week 17, Saturday** ([[../../06-sat-build-the-growth-system]]). Two
small, dependency-free tools that let you do the growth math from this week in
seconds instead of quarters, and refuse to lie to you the way a naive spreadsheet
does.

## What's here

| File | What it does |
|---|---|
| `growth_sim.py` | k-factor, saturating viral projection, cycle-time velocity, retention curve + plateau, loop efficiency + weakest handoff |
| `pmf_analyzer.py` | Sean Ellis PMF survey scored the **Superhuman** way: aggregate + per-segment, drops dead signups, flags the high-expectation segment, recommends the next move |
| `test_growth_sim.py` | 8 assertions that pin the behavior; doubles as a compile check |

## Requirements

- **Python 3.10+** (uses `X | None` union syntax). No pip installs. Stdlib only.

## Run it

```bash
cd code-lab/1

# run the tests (should print "OK — 8 tests passed")
python test_growth_sim.py

# see the growth simulator demo
python growth_sim.py

# see the PMF analyzer demo
python pmf_analyzer.py
```

## Pass bar

`python test_growth_sim.py` prints `OK — 8 tests passed`, and you can explain
each of these four demo outputs to a skeptic:

1. **k-factor with saturation.** The default demo (`base_k=0.5`, market 50k) tops
   out near ~1,950 users, *not* infinity, because effective k decays as the market
   fills. A constant-k spreadsheet would project a hockey stick that never
   arrives. This is the whole point: **model saturation or you will overpromise.**
2. **Cycle time.** A 7-day cycle has exactly 2x the velocity of a 14-day cycle at
   the same k. Speeding the loop can beat growing it.
3. **Retention plateau.** The "healthy" curve flattens above a floor and reads as
   PMF-shape; the "leaky" curve decays toward zero and does not. Day-1 retention
   is identical in both — the plateau is the signal, not the intercept.
4. **PMF segmentation.** The demo aggregate is 38% (below the 40% line), but the
   `power_user` segment is at 75%. The tool tells you to do the Superhuman play:
   focus on that segment, not the mass average.

## Use it on your own product

Edit the `_demo()` inputs, or import the functions:

```python
from growth_sim import k_factor, regime, project_viral, loop_efficiency

k = k_factor(refer_rate=0.35, invites_per_referrer=2.5, invite_conversion=0.18)
print(k, regime(k))

loop = {"produces_output": 0.55, "invites": 0.30, "invitee_signs_up": 0.65}
print(loop_efficiency(loop))   # find YOUR weakest handoff
```

```python
from pmf_analyzer import Response, analyze, next_move, VERY, SOMEWHAT, NOT

rows = [Response("u1", VERY, "power_user", True), ...]  # your real survey rows
print(next_move(analyze(rows)))
```

## Honesty notes

- The k-factor benchmarks (`>1` true-viral, `0.15–0.25` typical) are practitioner
  figures from the Week 17 Thursday lesson, not laws. Use your own data.
- The retention curve here is a **generator** for reasoning about shape, not a
  fitter for your real cohort data. Feed real numbers before you trust a plateau.
- No network, no API keys, no external services. Everything runs offline.
