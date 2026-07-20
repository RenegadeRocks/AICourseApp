"""funnel_metrics.py — an honest lead-gen & paid-test calculator.

Covers the Week 18 numbers:
  1. opt-in rate                 -> opt_in_rate()
  2. cost per lead (CPL)         -> cpl()
  3. customer acquisition cost   -> cac(), blended_cac()
  4. multi-stage funnel roll-up  -> funnel_conversion()
  5. the pre-registered paid-test decision rule -> paid_test_decision()

Design principle: measure ratios, not vanity totals, and force the paid-ads
go/no-go to be a PRE-REGISTERED rule read against a CAC target derived from LTV
(Week 18 Thu/Fri; unit economics from B6W16). The decision function refuses to
"decide" on a sample too small to be meaningful.

Stdlib only. Run:  python funnel_metrics.py
"""
from __future__ import annotations

from dataclasses import dataclass, field


# ---------------------------------------------------------------------------
# 1. opt-in rate
# ---------------------------------------------------------------------------
def opt_in_rate(opt_ins: int, visitors: int) -> float:
    """Opt-ins divided by opt-in-page visitors (0..1).

    This isolates offer/page quality from traffic volume. Track THIS, not raw
    subscriber count, which always rises and tells you nothing about health.
    """
    if visitors < 0 or opt_ins < 0:
        raise ValueError("counts must be >= 0")
    if visitors == 0:
        return 0.0
    if opt_ins > visitors:
        raise ValueError("opt_ins cannot exceed visitors")
    return opt_ins / visitors


def confirmation_rate(confirmed: int, submitted: int) -> float:
    """Confirmed (double opt-in) divided by submitted (0..1)."""
    if submitted < 0 or confirmed < 0:
        raise ValueError("counts must be >= 0")
    if submitted == 0:
        return 0.0
    if confirmed > submitted:
        raise ValueError("confirmed cannot exceed submitted")
    return confirmed / submitted


# ---------------------------------------------------------------------------
# 2. cost per lead
# ---------------------------------------------------------------------------
def cpl(spend: float, leads: int) -> float:
    """Cost per lead = spend / leads. Leading indicator, not the truth.

    A cheap lead that never becomes a customer is not cheap. Use CAC for the
    real decision.
    """
    if spend < 0:
        raise ValueError("spend must be >= 0")
    if leads < 0:
        raise ValueError("leads must be >= 0")
    if leads == 0:
        return float("inf")
    return spend / leads


# ---------------------------------------------------------------------------
# 3. customer acquisition cost
# ---------------------------------------------------------------------------
def cac(spend: float, customers: int) -> float:
    """Channel CAC = spend / customers acquired. The number that matters."""
    if spend < 0:
        raise ValueError("spend must be >= 0")
    if customers < 0:
        raise ValueError("customers must be >= 0")
    if customers == 0:
        return float("inf")
    return spend / customers


def blended_cac(total_sales_marketing_spend: float, total_new_customers: int) -> float:
    """Attribution-free CAC across ALL channels.

    Because it uses totals, no attribution model can distort it. When
    channel-level ROAS and blended CAC disagree, trust blended (Week 18 Fri).
    """
    return cac(total_sales_marketing_spend, total_new_customers)


def ltv_cac_ratio(ltv: float, customer_acquisition_cost: float) -> float:
    """LTV : CAC. Heuristic health line is >= 3.0 (see B6W16)."""
    if ltv < 0:
        raise ValueError("ltv must be >= 0")
    if customer_acquisition_cost <= 0:
        return float("inf")
    return ltv / customer_acquisition_cost


# ---------------------------------------------------------------------------
# 4. multi-stage funnel roll-up
# ---------------------------------------------------------------------------
@dataclass
class FunnelResult:
    stage_rates: dict[str, float]     # per-stage conversion (out/in)
    overall: float                    # product of all stage rates
    weakest_stage: str
    weakest_rate: float


def funnel_conversion(stages: dict[str, int]) -> FunnelResult:
    """Roll up an ordered funnel of absolute counts into stage rates.

    `stages` is an ORDERED dict of stage-name -> count reached at that stage,
    largest first, e.g.:
        {"visitors": 5000, "opt_ins": 1000, "confirmed": 720,
         "trials": 180, "customers": 27}

    Returns each stage-to-next rate, the overall visitor->final conversion, and
    the weakest handoff (where one improvement moves the whole funnel most).
    """
    if len(stages) < 2:
        raise ValueError("need at least two stages")
    names = list(stages.keys())
    counts = list(stages.values())
    for n, c in stages.items():
        if c < 0:
            raise ValueError(f"stage {n!r} count must be >= 0")
    rates: dict[str, float] = {}
    for i in range(len(names) - 1):
        top, bottom = counts[i], counts[i + 1]
        if bottom > top:
            raise ValueError(
                f"stage {names[i + 1]!r} ({bottom}) exceeds {names[i]!r} ({top})"
            )
        label = f"{names[i]}->{names[i + 1]}"
        rates[label] = (bottom / top) if top > 0 else 0.0
    overall = (counts[-1] / counts[0]) if counts[0] > 0 else 0.0
    weakest = min(rates, key=rates.get)
    return FunnelResult(rates, overall, weakest, rates[weakest])


# ---------------------------------------------------------------------------
# 5. the pre-registered paid-test decision rule
# ---------------------------------------------------------------------------
@dataclass
class PaidTestRule:
    """A PRE-REGISTERED decision rule. Fill this in BEFORE you spend."""
    target_cac: float           # CAC ceiling your LTV can sustain (from B6W16)
    scale_below: float          # scale if CAC < this
    kill_above: float           # kill if CAC > this
    min_spend: float            # don't decide before spending at least this
    min_customers: int = 5      # don't decide on fewer than this many customers

    def __post_init__(self) -> None:
        if not (self.scale_below <= self.target_cac <= self.kill_above):
            raise ValueError(
                "require scale_below <= target_cac <= kill_above"
            )
        if self.min_spend <= 0:
            raise ValueError("min_spend must be > 0")
        if self.min_customers < 1:
            raise ValueError("min_customers must be >= 1")


@dataclass
class PaidTestReading:
    decision: str               # "SCALE" | "KILL" | "KEEP_TESTING" | "INSUFFICIENT_DATA"
    cac: float
    reason: str
    details: dict[str, float] = field(default_factory=dict)


def paid_test_decision(
    spend: float, customers: int, rule: PaidTestRule
) -> PaidTestReading:
    """Apply a pre-registered rule to an in-flight paid test.

    The rule REFUSES to scale or kill on a sample too small to be meaningful:
    below min_spend OR below min_customers -> INSUFFICIENT_DATA. This is the
    guardrail against deciding on noise (Week 18 Fri small-N discipline).
    """
    c = cac(spend, customers)
    details = {
        "spend": spend,
        "customers": float(customers),
        "cac": c,
        "target_cac": rule.target_cac,
    }
    if spend < rule.min_spend or customers < rule.min_customers:
        return PaidTestReading(
            "INSUFFICIENT_DATA", c,
            f"spent {spend:.0f} (min {rule.min_spend:.0f}), "
            f"{customers} customers (min {rule.min_customers}); "
            "keep spending before deciding",
            details,
        )
    if c < rule.scale_below:
        return PaidTestReading(
            "SCALE", c,
            f"CAC {c:.2f} < scale line {rule.scale_below:.2f}; "
            "raise budget ~20-30% every few days, hold 30% for new concepts",
            details,
        )
    if c > rule.kill_above:
        return PaidTestReading(
            "KILL", c,
            f"CAC {c:.2f} > kill line {rule.kill_above:.2f} with no path down; "
            "stop, do not 'give it another week'",
            details,
        )
    return PaidTestReading(
        "KEEP_TESTING", c,
        f"CAC {c:.2f} between scale ({rule.scale_below:.2f}) and kill "
        f"({rule.kill_above:.2f}); iterate creative/offer toward target "
        f"{rule.target_cac:.2f}",
        details,
    )


# ---------------------------------------------------------------------------
# demo
# ---------------------------------------------------------------------------
def _demo() -> None:
    print("=" * 66)
    print("1. OPT-IN RATE (measure the ratio, not the raw count)")
    r = opt_in_rate(opt_ins=1000, visitors=5000)
    print(f"   1000 / 5000 visitors = {r:.1%} opt-in rate")
    print(f"   confirmation (double opt-in): {confirmation_rate(720, 1000):.1%}")

    print("=" * 66)
    print("2. CPL vs 3. CAC (leading indicator vs the truth)")
    print(f"   CPL: $1050 / 168 leads   = ${cpl(1050, 168):.2f}")
    print(f"   CAC: $1050 / 9 customers = ${cac(1050, 9):.2f}")
    print(f"   blended CAC: $4000 spend / 40 customers = ${blended_cac(4000, 40):.2f}")
    print(f"   LTV:CAC at LTV=$420, CAC=$117 -> {ltv_cac_ratio(420, 117):.2f}:1")

    print("=" * 66)
    print("4. FUNNEL ROLL-UP (find the weakest handoff)")
    funnel = {
        "visitors": 5000, "opt_ins": 1000, "confirmed": 720,
        "trials": 180, "customers": 27,
    }
    fr = funnel_conversion(funnel)
    for label, rate in fr.stage_rates.items():
        print(f"   {label:<22} {rate:.1%}")
    print(f"   overall visitors->customers: {fr.overall:.2%}")
    print(f"   weakest handoff: {fr.weakest_stage} ({fr.weakest_rate:.1%})")

    print("=" * 66)
    print("5. PAID-TEST DECISION (pre-registered rule, read on YOUR numbers)")
    rule = PaidTestRule(
        target_cac=150, scale_below=120, kill_above=200,
        min_spend=1000, min_customers=5,
    )
    for spend, custs, tag in [
        (1050, 9, "winner"),
        (1050, 4, "great CAC but only 4 customers"),
        (300, 2, "too early"),
        (2400, 8, "loser"),
        (1050, 7, "middle"),
    ]:
        reading = paid_test_decision(spend, custs, rule)
        cac_str = "inf" if reading.cac == float("inf") else f"${reading.cac:.0f}"
        print(f"   [{tag}] spend ${spend}, {custs} custs, CAC {cac_str} "
              f"-> {reading.decision}")
        print(f"        {reading.reason}")
    print("=" * 66)


if __name__ == "__main__":
    _demo()
