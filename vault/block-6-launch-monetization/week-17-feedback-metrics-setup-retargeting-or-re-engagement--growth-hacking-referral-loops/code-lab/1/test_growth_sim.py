"""test_growth_sim.py — assertions that pin the simulator's behavior.

Run:  python test_growth_sim.py
Exits 0 and prints OK if all pass; raises AssertionError otherwise.
No test framework needed (stdlib only), so it doubles as a compile check.
"""
from __future__ import annotations

from growth_sim import (
    k_factor, regime, project_viral, growth_velocity,
    retention_curve, plateau, has_pmf_shape,
    loop_efficiency, marginal_lift,
)
from pmf_analyzer import Response, analyze, next_move, VERY, SOMEWHAT, NOT


def approx(a: float, b: float, tol: float = 1e-6) -> bool:
    return abs(a - b) <= tol


def test_k_factor():
    assert approx(k_factor(0.30, 3.0, 0.15), 0.135)
    assert approx(k_factor(1.0, 5.0, 0.20), 1.0)
    assert k_factor(0.50, 3.0, 0.15) > k_factor(0.30, 3.0, 0.15)
    for bad in [(-0.1, 1, 0.5), (0.5, 1, 1.1)]:
        try:
            k_factor(*bad)
            raise AssertionError("expected ValueError")
        except ValueError:
            pass


def test_regime():
    assert "true-viral" in regime(1.2)
    assert "near-viral" in regime(0.8)
    assert "moderate" in regime(0.5)
    assert "most successful" in regime(0.2)
    assert "sub-scale" in regime(0.05)


def test_saturation_lowers_effective_k():
    res = project_viral(1000, base_k=0.5, cycle_time_days=14,
                        addressable_market=50_000, cycles=8)
    # effective k must monotonically decrease as market fills
    for a, b in zip(res.effective_k, res.effective_k[1:]):
        assert b <= a + 1e-9, "effective_k should not rise as market saturates"
    # never exceed the market
    assert res.total_users[-1] <= 50_000 + 1e-6
    # steady-state cap for k<1 is starting/(1-k) = 1000/0.5 = 2000
    assert approx(res.steady_state, 2000.0)


def test_growth_velocity_cycle_time():
    # halving cycle time doubles velocity
    assert approx(growth_velocity(0.5, 7), 2 * growth_velocity(0.5, 14))


def test_retention_plateau():
    healthy = retention_curve(day1=0.60, decay=0.25, plateau_floor=0.22)
    leaky = retention_curve(day1=0.60, decay=0.20, plateau_floor=0.01)
    assert has_pmf_shape(healthy) is True
    assert has_pmf_shape(leaky) is False
    assert plateau(healthy) > plateau(leaky)


def test_loop_efficiency():
    loop = {"produces_output": 0.60, "invites": 0.40, "invitee_signs_up": 0.70}
    lr = loop_efficiency(loop)
    assert approx(lr.amplification, 0.60 * 0.40 * 0.70)
    assert lr.weakest_step == "invites"
    # improving the weakest step lifts amplification more than improving a strong one
    lift_weak = marginal_lift(loop, "invites", 0.60)
    lift_strong = marginal_lift(loop, "invitee_signs_up", 0.90)
    assert lift_weak > lift_strong


def test_pmf_segmentation():
    responses = [
        Response("p1", VERY, "power_user", True),
        Response("p2", VERY, "power_user", True),
        Response("p3", VERY, "power_user", True),
        Response("p4", SOMEWHAT, "power_user", True),
        Response("c1", SOMEWHAT, "casual", True),
        Response("c2", NOT, "casual", True),
        Response("c3", NOT, "casual", True),
        Response("d1", NOT, "casual", False),   # dropped
    ]
    res = analyze(responses)
    assert res["dropped_inactive"] == 1
    # aggregate over 7 active: 3 very / 7 = ~0.43 -> above threshold here
    assert res["aggregate"].n == 7
    # power_user is the high-expectation segment (3/4 very)
    assert res["high_expectation_segment"] == "power_user"
    assert res["by_segment"]["power_user"].very_pct == 0.75
    assert "power_user" in next_move(res)


def test_pmf_below_threshold_recommends_product():
    responses = [
        Response("c1", NOT, "casual", True),
        Response("c2", NOT, "casual", True),
        Response("c3", SOMEWHAT, "casual", True),
        Response("c4", NOT, "casual", True),
    ]
    res = analyze(responses)
    assert res["aggregate"].has_pmf is False
    assert "back to the product" in next_move(res)


def main():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for t in tests:
        t()
        print(f"  PASS {t.__name__}")
    print(f"OK — {len(tests)} tests passed")


if __name__ == "__main__":
    main()
