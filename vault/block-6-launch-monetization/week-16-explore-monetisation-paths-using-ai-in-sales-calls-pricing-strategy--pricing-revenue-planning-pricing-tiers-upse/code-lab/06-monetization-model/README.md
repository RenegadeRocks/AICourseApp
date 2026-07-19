# Week 16 code-lab — the monetization + unit-economics model

A single, reusable calculator that ties the whole week together: it prices a
tier ladder under **real token COGS**, blends it into **CAC / LTV / payback /
gross margin**, runs the **Monday/Friday COGS-shock stress matrix**, and audits
your tier ladder for margin, spacing, and fences. It ships with two scenarios —
a healthy hybrid model and a deliberately-failing "three strikes" case — so you
can see both a passing and a failing business before you plug in your own.

## Run it

```bash
# Python 3.10+ ; no third-party dependencies.
cd code-lab/06-monetization-model
python unit_economics.py
```

You'll get two full reports plus a one-line read-out for each. No API key, no
network — the rate card is a local, date-stamped table you maintain by hand.

## Files

| File | What it is |
|------|-----------|
| `rate_card.py` | Date-stamped model rates (Sonnet 5 intro/standard, Opus 4.8, Fable 5, Haiku 4.5), verified 2026-07-17, plus the ~+30% tokenizer factor and `run_cost()`. **Update this from the provider's pricing page before trusting any output.** |
| `unit_economics.py` | The model: per-tier COGS, blended margin, LTV/CAC/payback, the COGS-shock stress matrix, and the tier-designer audit. Run this file. |
| `config_example.py` | Two scenarios: `HEALTHY_SCENARIO` (Niche Radar hybrid) and `THREE_STRIKES_SCENARIO` (paid-ads CAC on a cheap SMB product on an over-provisioned model). Copy and edit for your product. |
| `requirements.txt` | Standard-library only; Python 3.10+ floor. |

## What each number means

- **Per-tier margin** — `(price - COGS) / price`, where COGS = inference (at the
  date-stamped rate × your token counts × tokenizer factor) + support hours ×
  loaded rate + hosting slice.
- **LTV** — `(ARPA × gross margin) / monthly churn`, capped at a horizon
  (default 36 months) so near-zero churn doesn't blow up to infinity. **Gross
  margin, not revenue** — this is the #1 AI-product LTV mistake (Friday).
- **LTV:CAC** — target ≥ 3:1. Far above ~6:1 signals *under*-investment in
  growth, not a trophy.
- **CAC payback** — `CAC / (ARPA × gross margin)`; target ≤ 12 months. Lower AI
  margins stretch payback vs old SaaS.
- **COGS-shock matrix** — recomputes everything at Sonnet-5-intro,
  Sonnet-5-standard (Sept-1 expiry), Opus 4.8, and Fable 5, and flags the first
  scenario to break a pass bar. This is the whole point: **a margin event you
  don't control can break your unit economics with no change to price or churn.**
- **Tier-designer audit** — warns on tiers below the 60% margin floor, ladder
  steps under ~2×, and adjacent tiers with identical fences (no upgrade path).

## The stress case (why it's here)

Running the bundled `THREE_STRIKES_SCENARIO` shows a business that is upside-down
before any shock: negative margins (an over-provisioned model on a $29–$49
product), an $1,500 paid-ads CAC that can never pay back, and a ladder the audit
flags on all three checks. It exists so you can recognize the shape of a broken
model instantly — and so the calculator is proven to *fail loudly* rather than
print a comfortable lie. The healthy scenario, by contrast, survives every shock
down to Fable 5 (margin 20%, LTV:CAC 3.2:1) — thin, but alive — which is exactly
what a floor-plus-variable hybrid is supposed to do.

## Make it yours

1. Open `rate_card.py`, confirm the rates against
   `https://platform.claude.com/docs/en/about-claude/pricing`, update dates.
2. Copy `config_example.py`, replace the product, token counts, tiers, and
   business inputs (CAC including *your own time*, real churn from your
   analytics).
3. `python unit_economics.py` after importing your scenario, or edit the
   `__main__` block to point at it.

**Pass bar (Saturday):** your model clears LTV:CAC ≥ 3:1 and payback ≤ 12 months
at the Sept-1 intro-expiry shock (sonnet-5-standard), or you carry a written plan
for the gap. If a plausible model migration takes any tier negative, that's a
floor problem — add or raise a subscription floor, don't ship the price.

_last_verified: 2026-07-17_
