"""Pin the behavior of the Week 18 lead-gen calculator + planner.

Doubles as a compile check. Run:  python test_funnel_metrics.py
Expected final line:  OK — 14 tests passed
"""
from __future__ import annotations

import math

from funnel_metrics import (
    opt_in_rate, confirmation_rate, cpl, cac, blended_cac, ltv_cac_ratio,
    funnel_conversion, paid_test_decision, PaidTestRule,
)
from distribution_planner import (
    repurpose, plan_week, plan_campaign, FORMATS, DEFAULT_CADENCE,
)


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def run() -> None:
    n = 0

    # 1. opt-in rate basic + zero-visitor guard
    _assert(abs(opt_in_rate(1000, 5000) - 0.20) < 1e-9, "opt_in_rate 20%")
    _assert(opt_in_rate(0, 0) == 0.0, "opt_in_rate zero visitors -> 0")
    n += 1

    # 2. opt_ins > visitors raises
    try:
        opt_in_rate(10, 5)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    n += 1

    # 3. confirmation rate
    _assert(abs(confirmation_rate(720, 1000) - 0.72) < 1e-9, "confirmation 72%")
    n += 1

    # 4. CPL, and zero leads -> inf
    _assert(abs(cpl(1050, 168) - 6.25) < 1e-9, "cpl 6.25")
    _assert(cpl(100, 0) == float("inf"), "cpl zero leads -> inf")
    n += 1

    # 5. CAC, and zero customers -> inf
    _assert(abs(cac(1050, 9) - 116.666667) < 1e-4, "cac ~116.67")
    _assert(cac(500, 0) == float("inf"), "cac zero customers -> inf")
    n += 1

    # 6. blended CAC is attribution-free totals
    _assert(abs(blended_cac(4000, 40) - 100.0) < 1e-9, "blended cac 100")
    n += 1

    # 7. LTV:CAC ratio
    _assert(abs(ltv_cac_ratio(420, 117) - 3.5897) < 1e-3, "ltv:cac ~3.59")
    _assert(ltv_cac_ratio(420, 0) == float("inf"), "ltv:cac zero cac -> inf")
    n += 1

    # 8. funnel roll-up: overall = product of stages, weakest identified
    funnel = {"visitors": 5000, "opt_ins": 1000, "confirmed": 720,
              "trials": 180, "customers": 27}
    fr = funnel_conversion(funnel)
    _assert(abs(fr.overall - 27 / 5000) < 1e-9, "overall 27/5000")
    prod = 1.0
    for r in fr.stage_rates.values():
        prod *= r
    _assert(abs(prod - fr.overall) < 1e-9, "stage product == overall")
    n += 1

    # 9. funnel weakest handoff is trials->customers (27/180=0.15)
    _assert(fr.weakest_stage == "trials->customers", "weakest handoff")
    _assert(abs(fr.weakest_rate - 27 / 180) < 1e-9, "weakest rate 0.15")
    n += 1

    # 10. funnel rejects an increasing stage
    try:
        funnel_conversion({"a": 100, "b": 200})
        raise AssertionError("expected ValueError")
    except ValueError:
        pass
    n += 1

    # 11. paid-test rule validates ordering
    try:
        PaidTestRule(target_cac=150, scale_below=200, kill_above=120,
                     min_spend=1000)
        raise AssertionError("expected ValueError on bad ordering")
    except ValueError:
        pass
    n += 1

    rule = PaidTestRule(target_cac=150, scale_below=120, kill_above=200,
                        min_spend=1000, min_customers=5)

    # 12. winner scales; loser kills; middle keeps testing
    # loser: enough customers to pass the small-N guard, but CAC 2400/8=300 > kill
    _assert(paid_test_decision(1050, 9, rule).decision == "SCALE", "scale")
    _assert(paid_test_decision(2400, 8, rule).decision == "KILL", "kill")
    _assert(paid_test_decision(1050, 7, rule).decision == "KEEP_TESTING", "mid")
    n += 1

    # 13. small-N guard: great CAC but too few customers -> INSUFFICIENT_DATA
    r = paid_test_decision(1050, 4, rule)
    _assert(r.decision == "INSUFFICIENT_DATA", "small-N customers guard")
    _assert(paid_test_decision(300, 2, rule).decision == "INSUFFICIENT_DATA",
            "small-N spend guard")
    n += 1

    # 14. distribution planner: one idea -> all five expressions; plan sizing
    chain = repurpose("test idea", "https://x.com/m")
    _assert(set(chain.expressions.keys()) == set(FORMATS.keys()),
            "all formats produced")
    _assert(all("test idea" in v for v in chain.expressions.values()),
            "idea embedded in every expression")
    wp = plan_week(1, "idea one", "https://x.com/m")
    _assert(set(wp.schedule.keys()) == set(DEFAULT_CADENCE.keys()), "5-day week")
    plan = plan_campaign(["a", "b", "c"], "https://x.com/m")
    _assert(len(plan) == 3 and plan[2].week == 3, "3-week campaign")
    try:
        repurpose("", "https://x.com/m")
        raise AssertionError("expected ValueError on empty idea")
    except ValueError:
        pass
    n += 1

    print(f"OK — {n} tests passed")


if __name__ == "__main__":
    run()
