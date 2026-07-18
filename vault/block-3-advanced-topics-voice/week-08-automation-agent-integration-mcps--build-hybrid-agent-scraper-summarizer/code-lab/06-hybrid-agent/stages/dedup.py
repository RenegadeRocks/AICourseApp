"""Stage 3 — Dedup. Content-hash exact dupes; similarity threshold near-dupes.

Mostly deterministic. The near-duplicate adjudication (same story, two outlets)
is the whisker of judgment in an otherwise deterministic stage. Keeps the
highest-quality instance and records dropped-duplicate provenance so a
postmortem can see what was merged.
"""
from __future__ import annotations

from common.schema import content_hash

try:
    from rapidfuzz import fuzz
    _HAVE_FUZZ = True
except ImportError:            # near-dup detection degrades gracefully to exact
    _HAVE_FUZZ = False


def _quality(item: dict) -> int:
    """Cheap heuristic to pick the survivor among duplicates: longer summary +
    has a published date wins. Replace with your own signal if you have one."""
    return len(item.get("summary", "")) + (10 if item.get("published_at") else 0)


def dedup(items: list[dict], near_threshold: int = 88) -> dict:
    """Return {kept: [...], dropped: [{hash, kept_url, reason}]}."""
    by_hash: dict[str, dict] = {}
    dropped = []

    # Pass 1: exact dedup by content hash.
    for it in items:
        h = content_hash(it["url"], it["title"])
        it["_hash"] = h
        if h in by_hash:
            incumbent = by_hash[h]
            winner, loser = (it, incumbent) if _quality(it) > _quality(incumbent) else (incumbent, it)
            by_hash[h] = winner
            dropped.append({"hash": h, "kept_url": winner["url"], "reason": "exact-duplicate"})
        else:
            by_hash[h] = it

    kept = list(by_hash.values())
    if not _HAVE_FUZZ:
        return {"kept": kept, "dropped": dropped}

    # Pass 2: near-duplicate suppression on titles (same story, different outlet).
    survivors: list[dict] = []
    for it in kept:
        dup_of = None
        for s in survivors:
            if fuzz.token_sort_ratio(it["title"], s["title"]) >= near_threshold:
                dup_of = s
                break
        if dup_of is None:
            survivors.append(it)
        else:
            if _quality(it) > _quality(dup_of):
                survivors[survivors.index(dup_of)] = it
            dropped.append({"hash": it["_hash"], "kept_url": dup_of["url"], "reason": "near-duplicate"})
    return {"kept": survivors, "dropped": dropped}
