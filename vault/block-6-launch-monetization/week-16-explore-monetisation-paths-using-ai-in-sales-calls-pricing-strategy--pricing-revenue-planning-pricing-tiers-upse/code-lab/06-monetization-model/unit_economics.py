"""Unit-economics + revenue model for an AI product, under real token COGS.

Computes, from a scenario dict:
  - per-tier COGS (inference at a date-stamped rate, hosting slice, support)
    and gross margin at the tier price
  - blended gross margin across the tier customer mix
  - CAC, LTV (gross-margin based), LTV:CAC, and CAC payback period
  - a COGS-shock stress matrix across model tiers (the Monday/Friday shock)
  - a tier-designer audit: ladder spacing + a per-tier margin floor

Run the bundled example (Niche Radar) plus a deliberately-failing stress case:

    python unit_economics.py

Pure standard library. Edit scenarios in config_example.py or pass your own
dict to run_report().
"""

from __future__ import annotations

from dataclasses import dataclass

from rate_card import DEFAULT_TOKENIZER_FACTOR, get_rate, run_cost

# Health thresholds (Friday's pass bars). Directional, not gospel.
MIN_LTV_CAC = 3.0
MAX_PAYBACK_MONTHS = 12.0
MIN_TIER_MARGIN = 0.50          # per-tier gross-margin floor (AI-native band is 50-60%, per Bessemer/SaaS Mag; below 50% is the design finding)
MIN_LADDER_STEP = 2.0           # tiers should be >= ~2x apart to feel distinct


# --------------------------------------------------------------------------- #
# Tier economics
# --------------------------------------------------------------------------- #
@dataclass
class TierResult:
    name: str
    price: float
    customers: int
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


def tier_cogs(
    tier: dict,
    eco: dict,
    model_tier: str,
    support_multiplier: float = 1.0,
) -> tuple[float, float, float]:
    """Return (inference, support, fixed) monthly COGS for one customer on a tier."""
    factor = float(eco.get("tokenizer_factor", DEFAULT_TOKENIZER_FACTOR))
    per_run = run_cost(
        model_tier,
        int(eco["input_tokens_per_run"]),
        int(eco["output_tokens_per_run"]),
        tokenizer_factor=factor,
    )
    # A customer on this tier runs `runs_per_month` per active unit (niche),
    # across the tier's expected active units.
    runs = int(eco["runs_per_month_per_unit"]) * int(tier["expected_units"])
    inference = per_run * runs

    fixed = float(eco["hosting_usd_per_customer"])
    support = (
        float(tier["support_hours_per_month"])
        * float(eco["loaded_support_rate_usd"])
        * support_multiplier
    )
    return inference, support, fixed


def evaluate_tiers(
    cfg: dict,
    model_tier: str | None = None,
    support_multiplier: float = 1.0,
) -> list[TierResult]:
    eco = cfg["economics"]
    mt = model_tier or eco["model_tier"]
    out: list[TierResult] = []
    for t in cfg["tiers"]:
        inf, sup, fix = tier_cogs(t, eco, mt, support_multiplier)
        out.append(
            TierResult(
                name=t["name"],
                price=float(t["price"]),
                customers=int(t.get("customers", 0)),
                cogs_inference=inf,
                cogs_support=sup,
                cogs_fixed=fix,
            )
        )
    return out


# --------------------------------------------------------------------------- #
# Blended unit economics
# --------------------------------------------------------------------------- #
@dataclass
class UnitEconomics:
    arpa: float
    blended_margin: float
    cac: float
    monthly_churn: float
    ltv: float
    ltv_cac: float
    payback_months: float


def blended(tiers: list[TierResult]) -> tuple[float, float]:
    """Return (ARPA, blended gross margin) weighted by customer counts."""
    n = sum(t.customers for t in tiers)
    if n == 0:
        # Unweighted fallback so an empty book still returns sane numbers.
        arpa = sum(t.price for t in tiers) / len(tiers)
        cogs = sum(t.cogs_total for t in tiers) / len(tiers)
    else:
        arpa = sum(t.price * t.customers for t in tiers) / n
        cogs = sum(t.cogs_total * t.customers for t in tiers) / n
    margin = (arpa - cogs) / arpa if arpa > 0 else float("-inf")
    return arpa, margin


def unit_economics(cfg: dict, model_tier: str | None = None) -> UnitEconomics:
    tiers = evaluate_tiers(cfg, model_tier=model_tier)
    arpa, margin = blended(tiers)
    biz = cfg["business"]
    cac = float(biz["cac_usd"])
    churn = float(biz["monthly_revenue_churn"])
    gross_per_month = arpa * margin

    # LTV via the subscription formula, capped at an explicit horizon so that
    # near-zero churn (or NRR>100%) does not blow up to infinity.
    horizon = int(biz.get("ltv_horizon_months", 36))
    if churn <= 0:
        ltv = gross_per_month * horizon
    else:
        ltv = min(gross_per_month / churn, gross_per_month * horizon)

    ltv_cac = ltv / cac if cac > 0 else float("inf")
    payback = cac / gross_per_month if gross_per_month > 0 else float("inf")
    return UnitEconomics(arpa, margin, cac, churn, ltv, ltv_cac, payback)


# --------------------------------------------------------------------------- #
# Tier-designer audit
# --------------------------------------------------------------------------- #
def audit_ladder(cfg: dict) -> list[str]:
    warnings: list[str] = []
    tiers = evaluate_tiers(cfg)
    # Margin floor per tier.
    for t in tiers:
        if t.margin < MIN_TIER_MARGIN:
            warnings.append(
                f"Tier '{t.name}' margin {t.margin:.1%} is below the "
                f"{MIN_TIER_MARGIN:.0%} floor (COGS {t.cogs_total:.2f} vs price {t.price:.2f})."
            )
    # Ladder spacing.
    prices = [float(t["price"]) for t in cfg["tiers"]]
    for lo, hi, name_lo, name_hi in zip(
        prices, prices[1:], [t["name"] for t in cfg["tiers"]], [t["name"] for t in cfg["tiers"][1:]]
    ):
        if lo <= 0:
            continue
        step = hi / lo
        if step < MIN_LADDER_STEP:
            warnings.append(
                f"Ladder step '{name_lo}'->'{name_hi}' is {step:.1f}x "
                f"(< {MIN_LADDER_STEP:.0f}x): tiers may read as near-duplicates and stall buyers."
            )
    # Fence sanity: each tier must differ from the one below on >=1 named fence.
    for lo, hi in zip(cfg["tiers"], cfg["tiers"][1:]):
        if set(lo.get("fences", [])) == set(hi.get("fences", [])):
            warnings.append(
                f"Tiers '{lo['name']}' and '{hi['name']}' share identical fences: "
                "no clear upgrade path between them."
            )
    return warnings


# --------------------------------------------------------------------------- #
# Reporting
# --------------------------------------------------------------------------- #
def _money(x: float) -> str:
    return f"${x:,.2f}"


def run_report(cfg: dict) -> dict:
    """Print a full report and return the key numbers (for tests)."""
    eco = cfg["economics"]
    rate = get_rate(eco["model_tier"])
    print(f"\n{'=' * 68}")
    print(f" {cfg['product']['name']} — monetization & unit-economics model")
    print(f"{'=' * 68}")
    print(f" Model tier: {rate.name} (verified {rate.rate_date})"
          + (f" — {rate.note}" if rate.note else ""))

    # --- tier table ---
    tiers = evaluate_tiers(cfg)
    print("\n Per-tier economics (one customer):")
    header = f" {'Tier':<10}{'Price':>9}{'Cust':>6}{'Infer':>9}{'Supp':>9}{'Fixed':>8}{'COGS':>9}{'Margin':>9}"
    print(header)
    print(" " + "-" * (len(header) - 1))
    for t in tiers:
        print(f" {t.name:<10}{_money(t.price):>9}{t.customers:>6}"
              f"{_money(t.cogs_inference):>9}{_money(t.cogs_support):>9}"
              f"{_money(t.cogs_fixed):>8}{_money(t.cogs_total):>9}{t.margin:>8.1%}")

    # --- blended unit economics ---
    ue = unit_economics(cfg)
    print("\n Blended unit economics (weighted by customer mix):")
    print(f"   ARPA ................ {_money(ue.arpa)}/mo")
    print(f"   Gross margin ........ {ue.blended_margin:.1%}")
    print(f"   CAC ................. {_money(ue.cac)}")
    print(f"   Monthly rev churn ... {ue.monthly_churn:.1%}")
    print(f"   LTV (gross, capped) . {_money(ue.ltv)}")
    ltv_cac_ok = "OK" if ue.ltv_cac >= MIN_LTV_CAC else "LOW"
    pb_ok = "OK" if ue.payback_months <= MAX_PAYBACK_MONTHS else "SLOW"
    print(f"   LTV:CAC ............. {ue.ltv_cac:.1f}:1  [{ltv_cac_ok}]  (target >= {MIN_LTV_CAC:.0f}:1)")
    print(f"   CAC payback ......... {ue.payback_months:.1f} months  [{pb_ok}]  (target <= {MAX_PAYBACK_MONTHS:.0f})")

    # --- COGS-shock stress matrix ---
    print("\n COGS-shock stress matrix (blended margin / LTV:CAC / payback):")
    shock_tiers = ["sonnet-5-intro", "sonnet-5-standard", "opus-4.8", "fable-5"]
    print(f" {'Model tier':<26}{'Margin':>9}{'LTV:CAC':>10}{'Payback':>10}")
    print(" " + "-" * 54)
    first_break = None
    for mt in shock_tiers:
        ue_s = unit_economics(cfg, model_tier=mt)
        broke = ue_s.ltv_cac < MIN_LTV_CAC or ue_s.payback_months > MAX_PAYBACK_MONTHS
        flag = " *" if broke else ""
        if broke and first_break is None:
            first_break = mt
        name = get_rate(mt).name
        print(f" {name[:25]:<26}{ue_s.blended_margin:>8.1%}"
              f"{ue_s.ltv_cac:>9.1f}{ue_s.payback_months:>9.1f}{flag}")
    if first_break:
        print(f"\n * First shock to break a pass bar: {get_rate(first_break).name}")
    else:
        print("\n All shock scenarios clear both pass bars. Now double churn and re-run.")

    # --- tier-designer audit ---
    print("\n Tier-designer audit:")
    warns = audit_ladder(cfg)
    if not warns:
        print("   No issues: margins above floor, ladder well-spaced, fences distinct.")
    else:
        for w in warns:
            print(f"   ! {w}")

    return {
        "arpa": ue.arpa,
        "blended_margin": ue.blended_margin,
        "ltv": ue.ltv,
        "ltv_cac": ue.ltv_cac,
        "payback_months": ue.payback_months,
        "first_break": first_break,
        "warnings": warns,
    }


if __name__ == "__main__":
    from config_example import HEALTHY_SCENARIO, THREE_STRIKES_SCENARIO

    healthy = run_report(HEALTHY_SCENARIO)
    strikes = run_report(THREE_STRIKES_SCENARIO)

    print(f"\n{'=' * 68}")
    print(" READ-OUT")
    print(f"{'=' * 68}")
    print(f" Healthy (Niche Radar hybrid): LTV:CAC {healthy['ltv_cac']:.1f}:1, "
          f"payback {healthy['payback_months']:.1f}mo — under-monetized, room to invest.")
    print(f" Three-strikes (paid-ads on a $39 SMB product): LTV:CAC "
          f"{strikes['ltv_cac']:.1f}:1, payback {strikes['payback_months']:.1f}mo — "
          "acquisition model wrong for the ACV.")
