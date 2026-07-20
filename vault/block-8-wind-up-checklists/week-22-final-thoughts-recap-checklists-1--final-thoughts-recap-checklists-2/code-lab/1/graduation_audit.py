"""Graduation audit — master-checklist scorer.

Scores a graduate's business against the 35-item master build checklist from
Week 22 Tuesday, returns a total out of 70, a stage band, and a ranked gap list.

Pure standard library. Python 3.10+.

Run:  python graduation_audit.py          # demo with an example scoresheet
Use:  import graduation_audit as ga; ga.score(my_scores)
"""

from __future__ import annotations

from dataclasses import dataclass, field


# The 35 items, grouped by the seven stages. `blocks_revenue` is a coarse rank
# (higher = fixing this unblocks more revenue) used to sort the gap list.
@dataclass(frozen=True)
class Item:
    id: int
    stage: str
    text: str
    blocks_revenue: int  # 1 (low) .. 5 (high)


STAGES = [
    "Idea",
    "Validated",
    "Built",
    "Launched",
    "Monetized",
    "Grown",
    "Systematized",
]

CHECKLIST: list[Item] = [
    Item(1, "Idea", "Problem is a specific person's specific pain, stated as a falsifiable bet", 5),
    Item(2, "Idea", "AI actually fits this problem (non-AI solution is worse)", 5),
    Item(3, "Idea", "Niche stated as a hypothesis you could be wrong about", 3),
    Item(4, "Idea", "Positioning is explicit: what, for whom, against what alternative", 3),
    Item(5, "Idea", "You know the unit of value you will charge for", 4),
    Item(6, "Validated", "Ran interviews designed not to flatter you", 5),
    Item(7, "Validated", "Treated synthetic/AI feedback as hypothesis, not evidence", 2),
    Item(8, "Validated", "Have a signal stronger than words (smoke test, pre-pay, pilot)", 5),
    Item(9, "Validated", "Kept an evidence ledger", 3),
    Item(10, "Validated", "Defined a kill condition and would honor it", 3),
    Item(11, "Built", "Built the smallest version up the prototype ladder", 4),
    Item(12, "Built", "AI work has a real architecture (retrieval, tools, control flow)", 3),
    Item(13, "Built", "Context is engineered, not stuffed", 3),
    Item(14, "Built", "Have evals: a defined pass bar and a way to measure output", 5),
    Item(15, "Built", "AI-generated code was reviewed, not merged on trust", 4),
    Item(16, "Launched", "UI/UX a stranger can use without you narrating it", 4),
    Item(17, "Launched", "Magic features are reliable (wow does not become a ticket)", 3),
    Item(18, "Launched", "Auth and security are real; lethal-trifecta risk understood", 5),
    Item(19, "Launched", "Launched on purpose, with a plan for your stage", 3),
    Item(20, "Launched", "Outreach is not slop; complies with platform policy", 3),
    Item(21, "Monetized", "Pricing anchored to a value metric, not cost-plus", 5),
    Item(22, "Monetized", "Have tiers and an expansion path", 4),
    Item(23, "Monetized", "Margin computed under real COGS (current prices, tokenizer)", 5),
    Item(24, "Monetized", "Can quote a real per-unit cost today, recomputed recently", 4),
    Item(25, "Monetized", "Sales has a repeatable motion (objections, closes)", 4),
    Item(26, "Grown", "Have at least one growth loop, not just a hand-refilled funnel", 4),
    Item(27, "Grown", "Feedback engine turns usage into roadmap, segmented", 3),
    Item(28, "Grown", "Measure growth honestly; know your stopping condition", 3),
    Item(29, "Grown", "Have a lead-gen engine (magnet + opt-in funnel)", 4),
    Item(30, "Grown", "If paid: know real payback (CAC vs margin, not revenue)", 4),
    Item(31, "Systematized", "Onboarding is an SOP, not a heroic effort", 3),
    Item(32, "Systematized", "Delivery engineered so one build serves many customers", 4),
    Item(33, "Systematized", "Client dashboard / async tracking; status without a meeting", 2),
    Item(34, "Systematized", "Community or owned audience compounds distribution", 3),
    Item(35, "Systematized", "Prices, SOPs, specs each live in one canonical place", 3),
]

MAX_SCORE = len(CHECKLIST) * 2  # 70


@dataclass
class Result:
    total: int
    max_total: int
    band: str
    stage_totals: dict[str, int]
    gaps: list[tuple[Item, int]] = field(default_factory=list)


def band_for(total: int) -> str:
    if total <= 25:
        return "Early — validation & first revenue is the job. Do not systematize yet."
    if total <= 45:
        return "Building — fix economics (Stage 5/6) before distribution."
    if total <= 60:
        return "Launched & monetizing — systematize (Stage 7) before you scale."
    return "Systematized — rare. Guard against decay; re-audit quarterly."


def score(scores: dict[int, int]) -> Result:
    """`scores` maps item id -> 0/1/2. Missing ids are treated as 0."""
    for v in scores.values():
        if v not in (0, 1, 2):
            raise ValueError(f"scores must be 0, 1, or 2; got {v!r}")

    total = 0
    stage_totals = {s: 0 for s in STAGES}
    gaps: list[tuple[Item, int]] = []

    for item in CHECKLIST:
        v = scores.get(item.id, 0)
        total += v
        stage_totals[item.stage] += v
        if v < 2:
            gaps.append((item, v))

    # Rank gaps: biggest revenue blocker first, then lowest score first.
    gaps.sort(key=lambda pair: (-pair[0].blocks_revenue, pair[1]))

    return Result(
        total=total,
        max_total=MAX_SCORE,
        band=band_for(total),
        stage_totals=stage_totals,
        gaps=gaps,
    )


def render(result: Result) -> str:
    lines = [
        "=" * 60,
        f"MASTER CHECKLIST AUDIT   {result.total}/{result.max_total}",
        "=" * 60,
        f"Band: {result.band}",
        "",
        "Stage totals (max 10 each):",
    ]
    for stage in STAGES:
        lines.append(f"  {stage:<14} {result.stage_totals[stage]:>2}/10")
    lines += ["", "Top gaps to close (ranked by revenue blocked):"]
    for item, v in result.gaps[:8]:
        lines.append(f"  [{v}] #{item.id:<2} ({item.stage}) {item.text}")
    if len(result.gaps) > 8:
        lines.append(f"  ... and {len(result.gaps) - 8} more.")
    lines.append("")
    return "\n".join(lines)


def _demo() -> None:
    # An example "Building"-stage scoresheet (matches the Tuesday worked example).
    example = {
        1: 2, 2: 2, 3: 2, 4: 2, 5: 1,          # Idea = 9
        6: 2, 7: 2, 8: 2, 9: 1, 10: 1,          # Validated = 8
        11: 2, 12: 2, 13: 1, 14: 2, 15: 1,      # Built = 8
        16: 2, 17: 1, 18: 0, 19: 2, 20: 1,      # Launched = 6
        21: 1, 22: 1, 23: 1, 24: 1, 25: 1,      # Monetized = 5
        26: 1, 27: 1, 28: 0, 29: 1, 30: 0,      # Grown = 3
        31: 1, 32: 1, 33: 0, 34: 0, 35: 0,      # Systematized = 2
    }
    print(render(score(example)))


if __name__ == "__main__":
    _demo()
