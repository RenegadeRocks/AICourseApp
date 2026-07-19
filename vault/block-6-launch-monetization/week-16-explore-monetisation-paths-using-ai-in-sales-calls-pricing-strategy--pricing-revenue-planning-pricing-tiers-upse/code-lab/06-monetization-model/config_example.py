"""Scenarios for the Week 16 monetization model.

Two scenarios ship:
  HEALTHY_SCENARIO       — Niche Radar's hybrid model (Mon-Fri worked example)
  THREE_STRIKES_SCENARIO — the deliberately-failing stress case: paid-ads CAC
                           on a $39 SMB product (low margin + high churn +
                           high CAC = the three strikes from Friday)

Copy this file, edit the numbers for YOUR product, and pass your dict to
run_report(). Token counts are measured on a new-tokenizer model, so the
model applies the ~+30% tokenizer_factor from rate_card.py by default.
"""

from __future__ import annotations

# --------------------------------------------------------------------------- #
# HEALTHY: Niche Radar hybrid (the week's running example)
# --------------------------------------------------------------------------- #
HEALTHY_SCENARIO = {
    "product": {"name": "Niche Radar (hybrid)"},
    "economics": {
        "model_tier": "sonnet-5-intro",        # current rate card key
        "tokenizer_factor": 1.30,
        "input_tokens_per_run": 45_000,        # scraped sources + context per brief
        "output_tokens_per_run": 3_000,        # the structured brief
        "runs_per_month_per_unit": 22,         # ~daily briefs per monitored niche
        "hosting_usd_per_customer": 3.00,      # infra slice per tenant
        "loaded_support_rate_usd": 90.00,      # your time, loaded, per hour
    },
    # Tokens/runs above reproduce Monday's per-brief math exactly ($0.156/run,
    # $3.43/niche/mo). `expected_units` is the *active* niche count a tier
    # customer actually monitors — always below the tier's niche cap (fence),
    # because real customers don't max their plan. Mix is Pro-heavy (Friday:
    # "mostly Pro") for ARPA ~$180. Support hours are loaded at $90/hr and are
    # the largest single COGS line at the higher tiers — which, with real token
    # COGS, lands every tier in the week's 50-60% AI-native margin band rather
    # than the 80-90% of classic SaaS.
    "tiers": [
        {
            "name": "Starter", "price": 39.0, "customers": 15,
            "expected_units": 2, "support_hours_per_month": 0.09,
            "fences": ["2 niches", "email", "basic-analysis"],
        },
        {
            "name": "Pro", "price": 199.0, "customers": 21,
            "expected_units": 6, "support_hours_per_month": 0.67,
            "fences": ["10 niches", "slack", "trend-analysis", "3-seats"],
        },
        {
            "name": "Team", "price": 599.0, "customers": 4,
            "expected_units": 17, "support_hours_per_month": 2.00,
            "fences": ["30 niches", "api", "custom-prompts", "unlimited-seats", "onboarding"],
        },
    ],
    "business": {
        "cac_usd": 220.0,                      # mostly founder time + light ads
        "monthly_revenue_churn": 0.04,         # net of expansion (Thursday's ladder)
        "ltv_horizon_months": 36,
    },
}

# --------------------------------------------------------------------------- #
# THREE STRIKES: the failing case (Friday's cautionary contrast)
# Paid-ads CAC on a cheap SMB product, forced onto a pricier model, churning
# hard. The model should show LTV:CAC well below 3 and a slow payback.
# --------------------------------------------------------------------------- #
THREE_STRIKES_SCENARIO = {
    "product": {"name": "Niche Radar (paid-ads, cheap-only)"},
    "economics": {
        "model_tier": "opus-4.8",              # over-provisioned model = high COGS
        "tokenizer_factor": 1.30,
        "input_tokens_per_run": 45_000,
        "output_tokens_per_run": 3_000,
        "runs_per_month_per_unit": 22,
        "hosting_usd_per_customer": 3.00,
        "loaded_support_rate_usd": 90.00,
    },
    "tiers": [
        {
            "name": "Solo", "price": 29.0, "customers": 60,
            "expected_units": 3, "support_hours_per_month": 0.20,
            "fences": ["niches", "email"],
        },
        {
            "name": "Plus", "price": 49.0, "customers": 10,
            "expected_units": 6, "support_hours_per_month": 0.30,
            "fences": ["niches", "email"],   # identical fence set to Solo -> audit warns
        },
    ],
    "business": {
        "cac_usd": 1_500.0,                    # paid acquisition on a cheap product
        "monthly_revenue_churn": 0.08,         # SMB churn, no expansion mechanics
        "ltv_horizon_months": 36,
    },
}
