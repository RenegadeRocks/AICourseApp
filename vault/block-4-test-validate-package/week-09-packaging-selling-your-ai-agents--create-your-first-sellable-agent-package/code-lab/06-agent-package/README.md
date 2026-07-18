# Code-lab 06 — Agent Package Toolkit

Two tools that turn Week 9's artifacts into numbers and documents:

1. **`pricing_calculator.py`** — models your package's COGS (tokens, hosting,
   support hours), computes gross margin per tier, and stress-tests pricing
   against 2026-shaped scenarios (Sonnet 5 intro expiry, flagship-tier
   migration, price war, outcome-rate bad month).
2. **`package_spec.py`** — reads your `package.yaml` and generates the
   Saturday deliverable set as markdown: one-pager, tier sheet, onboarding
   checklist, delivery runbook skeleton, eval-report template, and a demo
   script with your pricing sentence spelled out verbatim.

## Setup

```bash
cd code-lab/06-agent-package
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Python 3.10+ required. No API keys needed — this lab is deliberately
deterministic; the numbers come from your config, not from a model.

## Run

```bash
# 1. Copy the example config and edit every value marked CHANGE-ME
cp package.example.yaml package.yaml

# 2. Margin + stress matrix (prints to stdout)
python pricing_calculator.py package.yaml

# 3. Generate the package documents into ./out/
python package_spec.py package.yaml --out out/
```

## What to look at

- The **stress matrix**: any cell below 70% gross margin (fully loaded,
  including support hours) fails Friday's pass bar. Fix by repricing the
  tier, cutting COGS (cheaper model tier for deterministic-adjacent stages),
  or restructuring (caps, smaller included volume).
- The **rate card dates** in `models.py`. Prices are date-stamped on purpose:
  when you read this after 2026-08-31, Sonnet 5's intro rate is gone and the
  calculator's `--scenario intro_expiry` is your new baseline. Update the
  table from the provider's published pricing page before trusting any output.
- `out/one_pager.md` — if a stranger could not buy from this page, the gap is
  in your `package.yaml`, not in the generator.

## Files

| File | Purpose |
|---|---|
| `models.py` | Date-stamped model rate card + tokenizer factor |
| `pricing_calculator.py` | COGS, margin per tier, scenario stress matrix |
| `package_spec.py` | package.yaml → one-pager, tier sheet, checklist, runbook, eval-report template, demo script |
| `package.example.yaml` | Fully worked "Niche Radar" example config |
| `requirements.txt` | Pinned deps (PyYAML only) |

## Modify one thing (per the study protocol)

Change `support_hours_per_customer_per_month` in your `package.yaml` from the
optimistic number to double it, and re-run. Watch which tier's margin breaks
first. That tier is where your support fence (Tuesday's exclusion list) is
doing the most work.
