"""growth_sim.py — an honest growth-metrics simulator.

Covers the four numbers from Week 17:
  1. k-factor (viral coefficient)      -> k_factor()
  2. cycle time -> growth velocity     -> project_viral()
  3. retention curve + plateau         -> retention_curve(), plateau()
  4. loop efficiency / weakest handoff -> loop_efficiency()

Design principle: model SATURATION and DECAY, because a constant-k projection is
the single most common growth-planning lie (Andrew Chen, "Law of Shitty
Clickthroughs"). Every projection here bends down as the market fills.

Stdlib only. Run:  python growth_sim.py
"""
from __future__ import annotations

from dataclasses import dataclass


# ---------------------------------------------------------------------------
# 1. k-factor
# ---------------------------------------------------------------------------
def k_factor(refer_rate: float, invites_per_referrer: float, invite_conversion: float) -> float:
    """Viral coefficient.

    refer_rate:          share of users who ever send a referral (0..1)
    invites_per_referrer: average invites sent by those who refer
    invite_conversion:   share of invites that convert to a new user (0..1)

    k = effective_invites_per_user * invite_conversion
    """
    for name, v in (("refer_rate", refer_rate), ("invite_conversion", invite_conversion)):
        if not 0.0 <= v <= 1.0:
            raise ValueError(f"{name} must be in [0,1], got {v}")
    if invites_per_referrer < 0:
        raise ValueError("invites_per_referrer must be >= 0")
    effective_invites = refer_rate * invites_per_referrer
    return effective_invites * invite_conversion


def regime(k: float) -> str:
    """Human label for a k value (practitioner benchmarks)."""
    if k > 1.0:
        return "true-viral (rare, usually temporary)"
    if k >= 0.7:
        return "near-viral (very strong)"
    if k >= 0.3:
        return "moderate (amplifies other channels)"
    if k >= 0.15:
        return "where most successful companies land"
    return "sub-scale (referral is a minor lever here)"


# ---------------------------------------------------------------------------
# 2. viral projection with saturation + cycle time
# ---------------------------------------------------------------------------
@dataclass
class ViralResult:
    total_users: list[float]      # cumulative users at end of each cycle
    new_users: list[float]        # new users added each cycle
    days: list[float]             # elapsed days at end of each cycle
    effective_k: list[float]      # k after saturation, per cycle
    steady_state: float           # analytic cap if k<1 and no saturation


def project_viral(
    starting_users: float,
    base_k: float,
    cycle_time_days: float,
    addressable_market: float,
    cycles: int = 12,
) -> ViralResult:
    """Simulate viral growth with a saturating market.

    effective_k in a cycle shrinks as the market fills:
        effective_k = base_k * (1 - penetration)
    where penetration = current_users / addressable_market.

    This is why no real loop compounds forever: as you reach more of the market,
    fewer of the people your users invite are still un-signed-up.
    """
    if cycle_time_days <= 0:
        raise ValueError("cycle_time_days must be > 0")
    if addressable_market <= 0:
        raise ValueError("addressable_market must be > 0")

    total = float(starting_users)
    totals, news, days, eff_ks = [], [], [], []
    last_cohort = float(starting_users)

    for c in range(1, cycles + 1):
        penetration = min(total / addressable_market, 1.0)
        eff_k = base_k * (1.0 - penetration)
        added = last_cohort * eff_k
        # don't overshoot the market
        added = min(added, max(addressable_market - total, 0.0))
        total += added
        last_cohort = added
        totals.append(total)
        news.append(added)
        days.append(c * cycle_time_days)
        eff_ks.append(eff_k)

    # analytic steady state IF k<1 and market were infinite (sum of geometric series)
    steady = (
        starting_users / (1.0 - base_k) if base_k < 1.0 else float("inf")
    )
    return ViralResult(totals, news, days, eff_ks, steady)


def growth_velocity(base_k: float, cycle_time_days: float) -> float:
    """Rough growth velocity: amplification per day.

    Two programs with the same k but half the cycle time differ ~2x in velocity.
    Defined as base_k per cycle normalized to a 30-day month.
    """
    if cycle_time_days <= 0:
        raise ValueError("cycle_time_days must be > 0")
    cycles_per_month = 30.0 / cycle_time_days
    return base_k * cycles_per_month


# ---------------------------------------------------------------------------
# 3. retention curve + plateau
# ---------------------------------------------------------------------------
def retention_curve(
    day1: float, decay: float, plateau_floor: float, horizon: int = 30
) -> list[float]:
    """Generate a retention curve that decays toward a plateau.

    r(t) = plateau_floor + (day1 - plateau_floor) * exp(-decay * t)

    A healthy product's curve FLATTENS to a plateau > 0 (Reforge/Amplitude).
    A curve decaying toward 0 has no product/market fit no matter how high day-1.
    """
    import math

    if not 0.0 <= plateau_floor <= 1.0:
        raise ValueError("plateau_floor must be in [0,1]")
    if not 0.0 <= day1 <= 1.0:
        raise ValueError("day1 must be in [0,1]")
    return [
        plateau_floor + (day1 - plateau_floor) * math.exp(-decay * t)
        for t in range(horizon)
    ]


def plateau(curve: list[float], tail: int = 5) -> float:
    """Estimate the plateau as the mean of the last `tail` points."""
    if not curve:
        raise ValueError("empty curve")
    tail = min(tail, len(curve))
    return sum(curve[-tail:]) / tail


def has_pmf_shape(curve: list[float], min_plateau: float = 0.10) -> bool:
    """A curve has PMF shape if it flattens ABOVE a non-trivial floor.

    Heuristic: plateau >= min_plateau AND the curve is roughly flat at the tail
    (later points don't keep falling meaningfully).
    """
    p = plateau(curve)
    if p < min_plateau:
        return False
    tail = curve[-5:] if len(curve) >= 5 else curve
    # flat if the drop across the tail is small relative to the plateau
    drop = tail[0] - tail[-1]
    return drop <= 0.02


# ---------------------------------------------------------------------------
# 4. loop efficiency / weakest handoff
# ---------------------------------------------------------------------------
@dataclass
class LoopResult:
    amplification: float          # product of all handoff rates = users out per user in
    weakest_step: str
    weakest_rate: float


def loop_efficiency(handoffs: dict[str, float]) -> LoopResult:
    """Overall loop amplification and the weakest handoff.

    handoffs maps step-name -> conversion rate (0..1). The loop amplification is
    the product of all rates: how many new inputs one input produces per cycle.
    The weakest handoff is where one improvement moves the whole loop most.

    Example (collaboration loop):
        {"produces_output": 0.60, "invites": 0.40, "invitee_signs_up": 0.70}
    amplification = 0.60*0.40*0.70 = 0.168 ; weakest = invites (0.40)
    """
    if not handoffs:
        raise ValueError("need at least one handoff")
    for name, r in handoffs.items():
        if not 0.0 <= r <= 1.0:
            raise ValueError(f"handoff {name!r} rate must be in [0,1], got {r}")
    amp = 1.0
    for r in handoffs.values():
        amp *= r
    weakest_step = min(handoffs, key=handoffs.get)
    return LoopResult(amp, weakest_step, handoffs[weakest_step])


def marginal_lift(handoffs: dict[str, float], step: str, new_rate: float) -> float:
    """How much the loop amplification changes if one step improves to new_rate."""
    if step not in handoffs:
        raise KeyError(step)
    before = loop_efficiency(handoffs).amplification
    after = dict(handoffs)
    after[step] = new_rate
    return loop_efficiency(after).amplification - before


# ---------------------------------------------------------------------------
# demo
# ---------------------------------------------------------------------------
def _demo() -> None:
    print("=" * 64)
    print("1. k-FACTOR")
    k = k_factor(refer_rate=0.30, invites_per_referrer=3.0, invite_conversion=0.15)
    print(f"   k = {k:.3f}  -> {regime(k)}")
    k2 = k_factor(refer_rate=0.50, invites_per_referrer=3.0, invite_conversion=0.15)
    print(f"   lift refer_rate 30%->50%: k = {k2:.3f}  -> {regime(k2)}")

    print("=" * 64)
    print("2. VIRAL PROJECTION (with saturation)")
    res = project_viral(
        starting_users=1000, base_k=0.5, cycle_time_days=14,
        addressable_market=50_000, cycles=8,
    )
    for c, (tot, new, d, ek) in enumerate(
        zip(res.total_users, res.new_users, res.days, res.effective_k), start=1
    ):
        print(f"   cycle {c:>2} (day {d:>3.0f}): +{new:>7.0f}  total {tot:>8.0f}  eff_k {ek:.3f}")
    print(f"   naive steady-state cap (infinite market): {res.steady_state:.0f}")
    print(f"   velocity 14d cycle: {growth_velocity(0.5, 14):.3f}/mo"
          f"   |  7d cycle: {growth_velocity(0.5, 7):.3f}/mo (2x)")

    print("=" * 64)
    print("3. RETENTION CURVE")
    healthy = retention_curve(day1=0.60, decay=0.25, plateau_floor=0.22)
    leaky = retention_curve(day1=0.60, decay=0.20, plateau_floor=0.01)
    print(f"   healthy: plateau {plateau(healthy):.2f}  PMF-shape? {has_pmf_shape(healthy)}")
    print(f"   leaky:   plateau {plateau(leaky):.2f}  PMF-shape? {has_pmf_shape(leaky)}")

    print("=" * 64)
    print("4. LOOP EFFICIENCY")
    loop = {"produces_output": 0.60, "invites": 0.40, "invitee_signs_up": 0.70}
    lr = loop_efficiency(loop)
    print(f"   amplification: {lr.amplification:.3f} users-out per user-in")
    print(f"   weakest handoff: {lr.weakest_step} ({lr.weakest_rate:.2f})")
    lift = marginal_lift(loop, "invites", 0.60)
    print(f"   lift invites 0.40->0.60 adds {lift:.3f} to amplification")
    print("=" * 64)


if __name__ == "__main__":
    _demo()
