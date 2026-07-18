"""Binary synthesis rubric (Hamel's discipline: pass/fail per criterion, not
arbitrary scores) plus the faithfulness judge validator.

Your day-one golden set is a HYPOTHESIS. After a week of shadow runs, rebuild it
from the failures you actually observed — "error analysis is all you need"
(Hamel & Shreya). See 05-fri Layer 1.
"""
from __future__ import annotations

import re

CITATION_RE = re.compile(r"\[(\d+)\]")


def score_brief(brief_md: str, kept: list[dict]) -> dict:
    """Binary criteria — each True/False. A brief passes only if ALL pass."""
    n = len(kept)
    cited = {int(m) for m in CITATION_RE.findall(brief_md)}
    criteria = {
        "has_citations": bool(cited),
        "no_fabricated_citations": all(1 <= c <= n for c in cited),
        "within_length": len(brief_md) <= 8000,
        "has_footer": "item" in brief_md.lower() and "brief" in brief_md.lower(),
        "min_items_present": n >= 1,
    }
    return {"pass": all(criteria.values()), "criteria": criteria}


def judge_agreement(judge_labels: list[bool], human_labels: list[bool]) -> float:
    """Fraction of items where the judge agrees with your hand labels. Clear your
    threshold (e.g. >=0.90) before you trust the judge to gate anything —
    an unvalidated judge is a second unreviewed model, not oversight."""
    if not human_labels:
        return 0.0
    agree = sum(1 for j, h in zip(judge_labels, human_labels) if j == h)
    return agree / len(human_labels)
