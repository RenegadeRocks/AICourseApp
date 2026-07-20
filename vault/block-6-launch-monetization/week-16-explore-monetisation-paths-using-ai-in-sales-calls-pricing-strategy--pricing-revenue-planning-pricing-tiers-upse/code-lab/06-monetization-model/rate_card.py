"""Date-stamped model rate card for the Week 16 monetization model.

Every rate below was search-verified 2026-07-17 against the provider's
published pricing (see Week 16 Monday/Friday citations, Anthropic pricing
docs). Rates are per MILLION tokens, USD.

UPDATE THIS TABLE from the provider's pricing page before trusting any
calculator output. That is the entire point of date-stamping: a hard-coded
margin quietly becomes a lie as prices move, and in 2026 they move often.

`tokenizer_factor` reflects the newer Anthropic tokenizer (Opus 4.7+,
Sonnet 5, Fable 5) producing ~30% more tokens for the same text than
pre-2026 estimates. If your per-run token counts were measured directly on a
new-tokenizer model, set the factor to 1.0 in your scenario.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ModelRate:
    name: str
    input_per_mtok: float
    output_per_mtok: float
    rate_date: str          # when this rate was verified
    note: str = ""


RATE_CARD: dict[str, ModelRate] = {
    "sonnet-5-intro": ModelRate(
        name="Claude Sonnet 5 (intro pricing)",
        input_per_mtok=2.00,
        output_per_mtok=10.00,
        rate_date="2026-07-17",
        note="Intro rate ends 2026-08-31; then $3/$15.",
    ),
    "sonnet-5-standard": ModelRate(
        name="Claude Sonnet 5 (standard, from 2026-09-01)",
        input_per_mtok=3.00,
        output_per_mtok=15.00,
        rate_date="2026-07-17",
        note="The Sept-1 intro-expiry shock scenario.",
    ),
    "opus-4.8": ModelRate(
        name="Claude Opus 4.8",
        input_per_mtok=5.00,
        output_per_mtok=25.00,
        rate_date="2026-07-17",
        note="The forced-capability-migration shock scenario.",
    ),
    "fable-5": ModelRate(
        name="Claude Fable 5 (Mythos-class tier)",
        input_per_mtok=10.00,
        output_per_mtok=50.00,
        rate_date="2026-07-17",
        note="2x Opus 4.8; the upward-shock ceiling scenario.",
    ),
    "haiku-4.5": ModelRate(
        name="Claude Haiku 4.5",
        input_per_mtok=1.00,
        output_per_mtok=5.00,
        rate_date="2026-07-17",
        note="The cheap-tier / COGS-cut lever.",
    ),
}

# ~+30% tokens for identical text on the new tokenizer vs pre-2026 estimates.
DEFAULT_TOKENIZER_FACTOR = 1.30


def get_rate(tier_key: str) -> ModelRate:
    try:
        return RATE_CARD[tier_key]
    except KeyError:
        known = ", ".join(sorted(RATE_CARD))
        raise SystemExit(
            f"Unknown model tier '{tier_key}'. Known tiers: {known}. "
            "Add new tiers to rate_card.py WITH a rate_date."
        )


def run_cost(
    tier_key: str,
    input_tokens: int,
    output_tokens: int,
    tokenizer_factor: float = 1.0,
) -> float:
    """USD cost of ONE model run at the named tier's published rate."""
    rate = get_rate(tier_key)
    eff_in = input_tokens * tokenizer_factor
    eff_out = output_tokens * tokenizer_factor
    return (eff_in / 1e6) * rate.input_per_mtok + (eff_out / 1e6) * rate.output_per_mtok
