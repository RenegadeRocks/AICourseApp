"""Pricing calculator + stress matrix for an agent package.

Usage:
    python pricing_calculator.py package.yaml [--customers 5 15 40]

Computes, per tier:
  - monthly COGS (inference at date-stamped rates, hosting slice, eval,
    delivery infra, support hours at loaded rate)
  - gross margin at the tier price
Then runs the Friday stress matrix:
  baseline / intro_expiry / flagship_migration / price_war / bad_month
and prints margin per tier per scenario, flagging cells under the pass bar.
"""

from __future__ import annotations

import argparse
import sys
from dataclasses import dataclass

import yaml

from models import DEFAULT_TOKENIZER_FACTOR, get_rate, run_cost

PASS_BAR_MARGIN = 0.70  # Friday's pass bar: >= 70% gross margin, fully loaded


@dataclass
class TierEconomics:
    name: str
    price: float
    cogs_inference: float
    cogs_support: float
    cogs_fixed: float

    @property
    def cogs_total(self) -> float:
        return self.cogs_inference + self.cogs_support + self.cogs_fixed

    @property
    def margin(self) -> float:
        if self.price <= 0:
            return float("-inf")
        return (self.price - self.cogs_total) / self.price


def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    for key in ("package", "economics", "tiers"):
        if key not in cfg:
            sys.exit(f"Config missing required top-level key: '{key}'")
    return cfg


def tier_economics(
    cfg: dict,
    tier: dict,
    model_tier: str | None = None,
    price_override: float | None = None,
    support_multiplier: float = 1.0,
) -> TierEconomics:
    eco = cfg["economics"]
    tier_key = model_tier or eco["model_tier"]
    factor = float(eco.get("tokenizer_factor", DEFAULT_TOKENIZER_FACTOR))
    scale = float(tier.get("run_scale", 1.0))

    per_run = run_cost(
        tier_key,
        int(eco["input_tokens_per_run"] * scale),
        int(eco["output_tokens_per_run"] * scale),
        tokenizer_factor=factor,
    )
    inference = per_run * int(eco["runs_per_month"])

    hosting = float(eco["hosting_usd_per_month_fleet"]) / max(
        1, int(eco["expected_fleet_size_for_hosting_split"])
    )
    fixed = (
        hosting
        + float(eco["eval_usd_per_month_per_niche_pack"])
        + float(eco["delivery_infra_usd_per_tenant"])
    )
    support = (
        float(eco["support_hours_per_customer_per_month"])
        * float(eco["loaded_support_rate_usd"])
        * support_multiplier
    )
    price = price_override if price_override is not None else float(tier["price_usd_month"])
    return TierEconomics(tier["name"], price, inference, support, fixed)


def fmt_money(x: float) -> str:
    return f"${x:,.2f}"


def print_baseline(cfg: dict, customer_counts: list[int]) -> None:
    eco = cfg["economics"]
    rate = get_rate(eco["model_tier"])
    print(f"\n=== {cfg['package']['name']} — baseline economics ===")
    print(f"Model tier: {rate.name} (rate verified {rate.rate_date})"
          + (f" — {rate.note}" if rate.note else ""))

    labor = cfg["package"].get("labor_line", {})
    if labor:
        line = float(labor["hours_per_month"]) * float(labor["loaded_hourly_rate_usd"])
        print(f"Labor-line anchor: {labor['description']} ≈ {fmt_money(line)}/month")

    header = f"{'Tier':<12}{'Price':>10}{'Inference':>12}{'Support':>10}{'Fixed':>9}{'COGS':>10}{'Margin':>9}"
    print("\n" + header)
    print("-" * len(header))
    tiers = [tier_economics(cfg, t) for t in cfg["tiers"]]
    for te in tiers:
        print(
            f"{te.name:<12}{fmt_money(te.price):>10}{fmt_money(te.cogs_inference):>12}"
            f"{fmt_money(te.cogs_support):>10}{fmt_money(te.cogs_fixed):>9}"
            f"{fmt_money(te.cogs_total):>10}{te.margin:>8.1%}"
        )

    print("\nRevenue at customer counts (assumes even spread across tiers):")
    for n in customer_counts:
        per_tier = n / len(tiers)
        rev = sum(te.price * per_tier for te in tiers)
        cogs = sum(te.cogs_total * per_tier for te in tiers)
        print(f"  {n:>3} customers: revenue {fmt_money(rev)}/mo, "
              f"gross profit {fmt_money(rev - cogs)}/mo")


def scenarios(cfg: dict) -> dict[str, list[TierEconomics]]:
    """Friday's stress matrix, one column per scenario."""
    out: dict[str, list[TierEconomics]] = {}
    out["baseline"] = [tier_economics(cfg, t) for t in cfg["tiers"]]
    # (i) Sonnet 5 intro expiry — same workload, standard rate
    out["intro_expiry"] = [
        tier_economics(cfg, t, model_tier="sonnet-5-standard") for t in cfg["tiers"]
    ]
    # (ii) forced migration to a flagship tier
    out["flagship_migration"] = [
        tier_economics(cfg, t, model_tier="fable-5") for t in cfg["tiers"]
    ]
    # (iii) price war — hold COGS, cut every price to 60%
    out["price_war_-40%"] = [
        tier_economics(cfg, t, price_override=float(t["price_usd_month"]) * 0.60)
        for t in cfg["tiers"]
    ]
    # (iv) bad month — support burden doubles (incidents, hand-holding)
    out["bad_month_2x_support"] = [
        tier_economics(cfg, t, support_multiplier=2.0) for t in cfg["tiers"]
    ]
    return out


def print_matrix(cfg: dict) -> None:
    matrix = scenarios(cfg)
    names = [t["name"] for t in cfg["tiers"]]
    col_w = max(len(k) for k in matrix) + 2

    print(f"\n=== Stress matrix (gross margin; pass bar ≥ {PASS_BAR_MARGIN:.0%}) ===")
    print(f"{'Scenario':<{col_w}}" + "".join(f"{n:>12}" for n in names))
    print("-" * (col_w + 12 * len(names)))
    failures = []
    for scen, tiers in matrix.items():
        row = f"{scen:<{col_w}}"
        for te in tiers:
            flag = "" if te.margin >= PASS_BAR_MARGIN else "*"
            row += f"{te.margin:>11.1%}{flag or ' '}"
            if flag:
                failures.append((scen, te.name, te.margin))
        print(row)
    if failures:
        print("\n* below pass bar — fix by repricing, cutting COGS (cheaper tier for")
        print("  deterministic-adjacent stages), or restructuring (caps, volume):")
        for scen, tier, m in failures:
            print(f"    - {tier} under '{scen}': {m:.1%}")
    else:
        print("\nAll cells clear the pass bar. Now double support hours and re-run.")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", help="path to package.yaml")
    ap.add_argument("--customers", nargs="+", type=int, default=[5, 15, 40])
    args = ap.parse_args()

    cfg = load_config(args.config)
    print_baseline(cfg, args.customers)
    print_matrix(cfg)


if __name__ == "__main__":
    main()
