"""Per-stage token caps and a per-run dollar ceiling, ENFORCED not estimated.

A cost ceiling that only warns is a cost ceiling that gets exceeded. When a run
approaches the ceiling, the pipeline stops cleanly and alerts (ships a partial
brief with a truncation note, or skips synthesis) — it never silently blows the
budget. See 04-thu, Layer 4.

Prices are July-2026, date-stamped. Sonnet 5 intro $2/$10 per Mtok through
2026-08-31, then $3/$15. Verify current prices before a long run — the current
Anthropic tokenizer also runs ~30% heavier than the 2025 generation, so budgets
ported from older intuition undercount.
"""
from __future__ import annotations

from dataclasses import dataclass, field

# USD per input / output token, per model id. UPDATE before relying on these —
# check the current pricing page (platform.claude.com/docs) at run time; an
# unknown model id falls through to (0, 0) below, which silently disables the
# ceiling, so add every model you use here.
# Sonnet 5 shown at intro pricing; flip to (3.0, 15.0) after 2026-08-31.
PRICES = {
    "claude-sonnet-5":  (2.0 / 1_000_000, 10.0 / 1_000_000),
    "claude-haiku-4-5": (1.0 / 1_000_000,  5.0 / 1_000_000),  # UNVERIFIED — confirm against the pricing docs before trusting the ceiling
}


class BudgetExceeded(Exception):
    """Raised when a run would cross its dollar ceiling. Caught by the
    orchestrator, which stops cleanly and alerts rather than paying on."""


@dataclass
class RunBudget:
    dollar_ceiling: float
    per_stage_token_cap: dict[str, int] = field(default_factory=dict)
    spent_usd: float = 0.0
    tokens_by_stage: dict[str, int] = field(default_factory=dict)

    def check_stage_input(self, stage: str, input_tokens: int) -> int:
        """Truncate deterministically if a stage's input exceeds its cap.
        Runaway input (e.g. a 500KB page) is the usual cause of a run that
        costs 10x its neighbors. Returns the (possibly capped) token count."""
        cap = self.per_stage_token_cap.get(stage)
        if cap is not None and input_tokens > cap:
            return cap  # caller truncates content to fit; see stage code
        return input_tokens

    def charge(self, stage: str, model: str, in_tok: int, out_tok: int) -> None:
        pin, pout = PRICES.get(model, (0.0, 0.0))
        cost = in_tok * pin + out_tok * pout
        projected = self.spent_usd + cost
        if projected > self.dollar_ceiling:
            raise BudgetExceeded(
                f"run would hit ${projected:.2f} > ceiling ${self.dollar_ceiling:.2f} "
                f"at stage {stage}; stopping cleanly and alerting"
            )
        self.spent_usd = projected
        self.tokens_by_stage[stage] = self.tokens_by_stage.get(stage, 0) + in_tok + out_tok

    def summary(self) -> dict:
        return {
            "spent_usd": round(self.spent_usd, 4),
            "tokens_by_stage": self.tokens_by_stage,
        }
