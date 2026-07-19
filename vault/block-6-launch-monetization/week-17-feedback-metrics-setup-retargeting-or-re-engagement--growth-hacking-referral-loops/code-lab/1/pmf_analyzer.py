"""pmf_analyzer.py — the Sean Ellis PMF survey, done the Superhuman way.

The naive PMF score averages everyone. The Superhuman insight (Rahul Vohra, First
Round Review) is to SEGMENT: find the segment whose "very disappointed" share is
highest (your high-expectation customer), then work the "somewhat disappointed"
fence-sitters within it. This module computes both the aggregate score and the
per-segment scores, and flags the high-expectation segment.

Stdlib only. Run:  python pmf_analyzer.py
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass

VERY = "very_disappointed"
SOMEWHAT = "somewhat_disappointed"
NOT = "not_disappointed"
_VALID = {VERY, SOMEWHAT, NOT}

PMF_THRESHOLD = 0.40  # Sean Ellis: 40% "very disappointed" is the PMF rule of thumb


@dataclass(frozen=True)
class Response:
    user_id: str
    answer: str          # one of VERY / SOMEWHAT / NOT
    segment: str         # e.g. persona, plan, or use-case
    recently_active: bool  # only recently-active users count (don't survey dead signups)


@dataclass
class PmfScore:
    n: int
    very_pct: float
    somewhat_pct: float
    not_pct: float
    has_pmf: bool


def _score(responses: list[Response]) -> PmfScore:
    n = len(responses)
    if n == 0:
        return PmfScore(0, 0.0, 0.0, 0.0, False)
    counts = defaultdict(int)
    for r in responses:
        if r.answer not in _VALID:
            raise ValueError(f"invalid answer {r.answer!r}")
        counts[r.answer] += 1
    very = counts[VERY] / n
    return PmfScore(
        n=n,
        very_pct=very,
        somewhat_pct=counts[SOMEWHAT] / n,
        not_pct=counts[NOT] / n,
        has_pmf=very >= PMF_THRESHOLD,
    )


def analyze(responses: list[Response]) -> dict:
    """Return aggregate + per-segment PMF, filtered to recently-active users.

    Surveying users who haven't recently experienced the core value drags the
    score toward zero and teaches you nothing, so we drop them first.
    """
    active = [r for r in responses if r.recently_active]
    dropped = len(responses) - len(active)

    aggregate = _score(active)

    by_segment: dict[str, PmfScore] = {}
    buckets: dict[str, list[Response]] = defaultdict(list)
    for r in active:
        buckets[r.segment].append(r)
    for seg, rs in buckets.items():
        by_segment[seg] = _score(rs)

    # high-expectation customer = segment with the highest very-disappointed share
    # (require a minimum n so a segment of 1 doesn't win by noise)
    eligible = {s: sc for s, sc in by_segment.items() if sc.n >= 3}
    high_exp = max(eligible, key=lambda s: eligible[s].very_pct) if eligible else None

    return {
        "dropped_inactive": dropped,
        "aggregate": aggregate,
        "by_segment": by_segment,
        "high_expectation_segment": high_exp,
    }


def next_move(result: dict) -> str:
    """Superhuman-style recommendation from the analysis."""
    agg = result["aggregate"]
    high = result["high_expectation_segment"]
    if agg.n == 0:
        return "No recently-active responses. Survey users who just hit core value."
    if agg.has_pmf:
        return (
            f"Aggregate {agg.very_pct:.0%} >= 40%: you have PMF signal. "
            f"Protect what the fans love; grow into segment '{high}'."
        )
    if high and result["by_segment"][high].very_pct >= PMF_THRESHOLD:
        return (
            f"Aggregate {agg.very_pct:.0%} < 40%, BUT segment '{high}' is at "
            f"{result['by_segment'][high].very_pct:.0%}. Do the Superhuman play: "
            f"focus on '{high}', fix the fence-sitters' blockers, re-measure."
        )
    return (
        f"Aggregate {agg.very_pct:.0%} < 40% and no segment clears 40%. "
        f"Stop optimizing growth. Go back to the product (feedback engine)."
    )


def _demo() -> None:
    responses = [
        # power users (high expectation) — love it
        Response("p1", VERY, "power_user", True),
        Response("p2", VERY, "power_user", True),
        Response("p3", VERY, "power_user", True),
        Response("p4", SOMEWHAT, "power_user", True),
        # casual users — lukewarm
        Response("c1", SOMEWHAT, "casual", True),
        Response("c2", NOT, "casual", True),
        Response("c3", NOT, "casual", True),
        Response("c4", SOMEWHAT, "casual", True),
        # dead signups — correctly dropped
        Response("d1", NOT, "casual", False),
        Response("d2", NOT, "power_user", False),
    ]
    res = analyze(responses)
    agg = res["aggregate"]
    print(f"dropped inactive: {res['dropped_inactive']}")
    print(f"AGGREGATE (n={agg.n}): very={agg.very_pct:.0%} "
          f"somewhat={agg.somewhat_pct:.0%} not={agg.not_pct:.0%} PMF={agg.has_pmf}")
    print("BY SEGMENT:")
    for seg, sc in res["by_segment"].items():
        print(f"  {seg:12} n={sc.n} very={sc.very_pct:.0%} PMF={sc.has_pmf}")
    print(f"high-expectation segment: {res['high_expectation_segment']}")
    print("NEXT MOVE:", next_move(res))


if __name__ == "__main__":
    _demo()
