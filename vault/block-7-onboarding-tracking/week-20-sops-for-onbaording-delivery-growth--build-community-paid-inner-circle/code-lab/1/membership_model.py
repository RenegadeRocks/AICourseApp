"""Membership unit-economics + retention model with a ghost-town early warning.

Computes MRR, ARPU, average member lifetime, LTV, and the LTV:CAC ratio
(Friday's economics), and raises a ghost-town risk flag from a history of
engagement snapshots (the leading indicator that moves weeks before churn).

Formulas (Friday, [^4][^5]):
    ARPU                = MRR / total_members
    avg_lifetime_months = 1 / monthly_churn_rate
    LTV                 = (ARPU * gross_margin) / monthly_churn_rate
    LTV:CAC             = LTV / CAC   (>= 3 is the healthy benchmark)

Pure standard library. Run:  python membership_model.py
"""

from __future__ import annotations

from dataclasses import dataclass


# --- Unit economics ---------------------------------------------------------

@dataclass
class Tier:
    name: str
    price: float          # monthly price per member
    members: int


def mrr(tiers: list[Tier]) -> float:
    """Monthly recurring revenue: sum over tiers of price * members."""
    return sum(t.price * t.members for t in tiers)


def total_members(tiers: list[Tier]) -> int:
    return sum(t.members for t in tiers)


def arpu(tiers: list[Tier]) -> float:
    """Average revenue per user per month."""
    n = total_members(tiers)
    return mrr(tiers) / n if n else 0.0


def avg_lifetime_months(monthly_churn_rate: float) -> float:
    """Average member tenure in months = 1 / monthly churn."""
    if monthly_churn_rate <= 0:
        return float("inf")
    return 1.0 / monthly_churn_rate


def ltv(arpu_value: float, gross_margin: float, monthly_churn_rate: float) -> float:
    """Lifetime value = (ARPU * gross_margin) / monthly churn."""
    if monthly_churn_rate <= 0:
        return float("inf")
    return (arpu_value * gross_margin) / monthly_churn_rate


def ltv_cac_ratio(ltv_value: float, cac: float) -> float:
    if cac <= 0:
        return float("inf")
    return ltv_value / cac


def net_mrr_movement(new: float, expansion: float,
                     contraction: float, churned: float) -> float:
    """Honest MRR trajectory = new + expansion - contraction - churned."""
    return new + expansion - contraction - churned


# --- Ghost-town early warning (Friday's leading indicator) ------------------

@dataclass
class EngagementSnapshot:
    period: str            # e.g. "2026-W40"
    total_members: int
    active_7d: int         # members who posted/commented/attended in last 7 days
    new_members: int       # members who joined this period
    new_activated_7d: int  # of new_members, how many engaged in their first week

    def active_ratio(self) -> float:
        return self.active_7d / self.total_members if self.total_members else 0.0

    def first_week_activation(self) -> float:
        return self.new_activated_7d / self.new_members if self.new_members else 0.0


# thresholds (tune to your community; defaults are conservative)
ACTIVE_RATIO_FLOOR = 0.20        # fewer than 1 in 5 active weekly => risk
FIRST_WEEK_ACTIVATION_FLOOR = 0.30
DECLINE_PERIODS = 3              # consecutive falling periods => momentum risk


def ghost_town_warning(history: list[EngagementSnapshot]) -> dict:
    """Return a ghost-town risk assessment from a time-ordered engagement history.

    Fires when the active-member ratio is below the floor, OR has declined for
    DECLINE_PERIODS consecutive periods, OR new-member first-week activation is
    below the floor. Engagement leads churn by weeks, so this is the smoke alarm.
    """
    if not history:
        return {"status": "NO_DATA", "reasons": ["No engagement history supplied."]}

    latest = history[-1]
    reasons: list[str] = []

    ratio = latest.active_ratio()
    if ratio < ACTIVE_RATIO_FLOOR:
        reasons.append(
            f"Active-member ratio {ratio:.0%} is below the {ACTIVE_RATIO_FLOOR:.0%} floor."
        )

    fwa = latest.first_week_activation()
    if latest.new_members and fwa < FIRST_WEEK_ACTIVATION_FLOOR:
        reasons.append(
            f"New-member first-week activation {fwa:.0%} is below the "
            f"{FIRST_WEEK_ACTIVATION_FLOOR:.0%} floor: the room is not pulling newcomers in."
        )

    # momentum: is the active ratio falling for DECLINE_PERIODS in a row?
    if len(history) > DECLINE_PERIODS:
        window = history[-(DECLINE_PERIODS + 1):]
        ratios = [s.active_ratio() for s in window]
        declining = all(b < a for a, b in zip(ratios, ratios[1:]))
        if declining:
            reasons.append(
                f"Active-member ratio has declined for {DECLINE_PERIODS} consecutive "
                f"periods ({ratios[0]:.0%} -> {ratios[-1]:.0%}): trending toward ghost town."
            )

    status = "GHOST_TOWN_RISK" if reasons else "HEALTHY"
    return {
        "status": status,
        "active_ratio": round(ratio, 3),
        "first_week_activation": round(fwa, 3),
        "reasons": reasons or ["Active core is holding or growing; keep it up."],
    }


def _demo() -> None:
    tiers = [Tier("Core", 50.0, 80), Tier("Inner Circle", 200.0, 12)]
    monthly_churn = 0.04
    gross_margin = 0.90
    cac = 150.0

    m = mrr(tiers)
    a = arpu(tiers)
    life = avg_lifetime_months(monthly_churn)
    v = ltv(a, gross_margin, monthly_churn)
    ratio = ltv_cac_ratio(v, cac)

    print("=== MEMBERSHIP UNIT ECONOMICS ===")
    print(f"Members:        {total_members(tiers)}")
    print(f"MRR:            ${m:,.0f}/mo")
    print(f"ARPU:           ${a:,.2f}/member/mo")
    print(f"Monthly churn:  {monthly_churn:.0%}  ->  avg lifetime {life:.0f} months")
    print(f"LTV:            ${v:,.0f}/member")
    print(f"LTV:CAC:        {ratio:.1f}:1  (healthy >= 3:1)")

    print("\n--- Same MRR, churn doubled to 10% (the danger line) ---")
    bad_churn = 0.10
    v_bad = ltv(a, gross_margin, bad_churn)
    print(f"LTV falls to:   ${v_bad:,.0f}/member "
          f"({v_bad / v:.0%} of the healthy-churn LTV) from the same revenue today.")

    print("\n=== GHOST-TOWN EARLY WARNING ===")
    healthy_history = [
        EngagementSnapshot("W37", 70, 22, 8, 4),
        EngagementSnapshot("W38", 78, 26, 10, 5),
        EngagementSnapshot("W39", 85, 30, 9, 5),
        EngagementSnapshot("W40", 92, 34, 8, 4),
    ]
    print("Healthy community:", ghost_town_warning(healthy_history)["status"])
    for r in ghost_town_warning(healthy_history)["reasons"]:
        print("  -", r)

    dying_history = [
        EngagementSnapshot("W37", 92, 34, 8, 4),
        EngagementSnapshot("W38", 93, 28, 6, 2),
        EngagementSnapshot("W39", 94, 22, 5, 1),
        EngagementSnapshot("W40", 95, 16, 5, 1),
    ]
    result = ghost_town_warning(dying_history)
    print("\nDying community:", result["status"])
    for r in result["reasons"]:
        print("  -", r)


if __name__ == "__main__":
    _demo()
