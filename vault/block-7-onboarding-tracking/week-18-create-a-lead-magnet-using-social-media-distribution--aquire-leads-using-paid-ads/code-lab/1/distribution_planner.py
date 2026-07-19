"""distribution_planner.py — one idea, many native expressions.

Turns a single anchor idea into a platform-native repurposing chain (Week 18
Wed): long-form anchor -> carousel -> short video -> text post -> email, each
pointing softly at the lead magnet. The unit of reuse is the IDEA, not the
asset, so each expression is reshaped for its platform rather than cross-posted.

Also builds an N-week distribution plan from a list of weekly anchor ideas, so
you leave Saturday with a concrete schedule instead of good intentions.

Stdlib only. Run:  python distribution_planner.py
"""
from __future__ import annotations

from dataclasses import dataclass


# Platform-native format guidance (Week 18 Wed; fast-moving — re-verify).
FORMATS: dict[str, str] = {
    "long_form_anchor": "canonical write-up (LinkedIn article / newsletter / "
                        "YouTube / blog); everything else is cut from this",
    "carousel": "6-10 slide PDF (LinkedIn document post; highest ER format); "
                "magnet link in first COMMENT, never post body (~60% reach hit)",
    "short_video": "30-60s, strong hook in first second, captions; cut for "
                   "Reels + Shorts + TikTok + LinkedIn video",
    "text_post": "single sharpest point + a question to drive dwell/early "
                 "engagement (first 60 min decides reach)",
    "email": "send to your list with your own take + a direct magnet link "
             "(owned channel, no algorithm tax)",
}


@dataclass
class RepurposeChain:
    idea: str
    magnet_url: str
    expressions: dict[str, str]


def repurpose(idea: str, magnet_url: str) -> RepurposeChain:
    """Expand one anchor idea into the five native expressions.

    Each expression is a short brief (what to make), not finished copy — the
    point is to force the idea through every format so one afternoon yields a
    week of native content that all points at the magnet.
    """
    if not idea.strip():
        raise ValueError("idea must be non-empty")
    if not magnet_url.strip():
        raise ValueError("magnet_url must be non-empty")
    exprs = {
        fmt: f"[{fmt}] {guide}  |  IDEA: {idea}  |  POINTS TO: {magnet_url}"
        for fmt, guide in FORMATS.items()
    }
    return RepurposeChain(idea, magnet_url, exprs)


@dataclass
class WeekPlan:
    week: int
    anchor_idea: str
    schedule: dict[str, str]     # weekday -> what to publish


# A default publish cadence mapping the five expressions across a work week.
DEFAULT_CADENCE = {
    "Mon": "carousel",
    "Tue": "short_video",
    "Wed": "text_post",
    "Thu": "email",
    "Fri": "long_form_anchor",
}


def plan_week(week_number: int, anchor_idea: str, magnet_url: str,
              cadence: dict[str, str] | None = None) -> WeekPlan:
    """Turn one anchor idea into a five-day publishing schedule."""
    cadence = cadence or DEFAULT_CADENCE
    chain = repurpose(anchor_idea, magnet_url)
    schedule = {}
    for day, fmt in cadence.items():
        if fmt not in chain.expressions:
            raise KeyError(f"unknown format {fmt!r} in cadence")
        schedule[day] = chain.expressions[fmt]
    return WeekPlan(week_number, anchor_idea, schedule)


def plan_campaign(anchor_ideas: list[str], magnet_url: str,
                  cadence: dict[str, str] | None = None) -> list[WeekPlan]:
    """Build a multi-week plan, one anchor idea per week.

    Discipline: one idea per week, repurposed five ways, beats five thin ideas.
    Later weeks should be seeded by what your list/audience replied to earlier —
    the content->magnet->list->content loop (Week 18 Wed).
    """
    if not anchor_ideas:
        raise ValueError("need at least one anchor idea")
    return [
        plan_week(i, idea, magnet_url, cadence)
        for i, idea in enumerate(anchor_ideas, start=1)
    ]


# ---------------------------------------------------------------------------
# demo
# ---------------------------------------------------------------------------
def _demo() -> None:
    magnet = "https://yoursite.com/meeting-audit"
    ideas = [
        "Your team loses double-digit hours a week to 3 recurring meetings you "
        "could kill",
        "The 25-minute meeting default that recovers ~3 hours a week",
    ]
    print("=" * 70)
    print("REPURPOSE ONE IDEA (five native expressions)")
    chain = repurpose(ideas[0], magnet)
    for fmt, brief in chain.expressions.items():
        print(f"  - {brief}")

    print("=" * 70)
    print("TWO-WEEK DISTRIBUTION PLAN (one anchor idea per week)")
    for wp in plan_campaign(ideas, magnet):
        print(f"\n  WEEK {wp.week}: {wp.anchor_idea}")
        for day, what in wp.schedule.items():
            fmt = what.split("]")[0].lstrip("[")
            print(f"    {day}: {fmt}")
    print("=" * 70)


if __name__ == "__main__":
    _demo()
