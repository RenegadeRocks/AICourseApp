"""Stage 6 — Validate contract (deterministic gate). ONLY validated briefs ship.

The whole point of unattended operation is nobody reviews the output, so code
must. Two layers:
  1. Deterministic contract — every [n] citation resolves to a kept source URL;
     no fabricated sources; length + item-count in bounds. Certain, cheap.
  2. Faithfulness pass — a validated cheap judge scores each cited claim against
     its source (catches misrepresentation that citation-matching can't).
A failing brief is PERMANENT: alert, do not deliver. (05-fri Layer 4.)
"""
from __future__ import annotations

import re

from common.schema import PermanentError

CITATION_RE = re.compile(r"\[(\d+)\]")


def validate_contract(brief_md: str, kept: list[dict], min_items: int = 1,
                      max_chars: int = 20000) -> dict:  # ~2,500-word brief fits; tune per niche
    """Deterministic checks. Returns {ok, failures[]}. Never raises — the caller
    decides whether a failure is a hard stop for this run."""
    failures = []
    n = len(kept)

    cited = {int(m) for m in CITATION_RE.findall(brief_md)}
    # Every citation index must be within the numbered source list.
    bad = [c for c in cited if c < 1 or c > n]
    if bad:
        failures.append(f"fabricated/out-of-range citations: {sorted(bad)}")
    # A brief with zero citations is not grounded.
    if not cited:
        failures.append("no citations present — brief is ungrounded")
    if n < min_items:
        failures.append(f"too few kept items: {n} < {min_items}")
    if len(brief_md) > max_chars:
        failures.append(f"brief too long: {len(brief_md)} > {max_chars} chars")

    return {"ok": not failures, "failures": failures, "cited": sorted(cited)}


def faithfulness_check(client, model: str, brief_md: str, kept: list[dict],
                       threshold: float = 0.8) -> dict:
    """For each cited item, ask a validated cheap judge whether the brief's use
    of it is faithful. Returns {ok, per_source, min_score}. VALIDATE this judge
    against your own labels before trusting it (eval/run.py --validate-judge).
    """
    import json
    scores = []
    for i, it in enumerate(kept, start=1):
        if f"[{i}]" not in brief_md:
            continue  # not cited; nothing to check
        try:
            resp = client.messages.create(
                model=model,
                max_tokens=200,
                messages=[{
                    "role": "user",
                    "content": (
                        "Score 0..1 how faithfully the BRIEF represents the SOURCE. "
                        "1 = fully supported by the source; 0 = misrepresents or "
                        "adds unsupported claims. Return JSON {score, reason}.\n\n"
                        f"SOURCE [{i}] {it['title']}: {it.get('summary','')[:1200]}\n\n"
                        f"BRIEF:\n{brief_md[:4000]}"
                    ),
                }],
                output_format={"type": "json_schema", "schema": {
                    "type": "object",
                    "properties": {"score": {"type": "number"}, "reason": {"type": "string"}},
                    "required": ["score", "reason"], "additionalProperties": False,
                }},
            )
            r = json.loads(resp.content[0].text)
        except Exception as e:
            raise PermanentError(f"PERMANENT: faithfulness judge failed on [{i}] — {e}")
        scores.append({"source": i, "score": float(r["score"]), "reason": r["reason"]})
    min_score = min((s["score"] for s in scores), default=1.0)
    return {"ok": min_score >= threshold, "per_source": scores, "min_score": min_score}


def validate(brief_md: str, kept: list[dict], client=None, judge_model: str = "",
             faithfulness_threshold: float = 0.8) -> dict:
    """Full gate. Deterministic contract first (cheap), faithfulness second
    (costs judge tokens). Raises PermanentError if the brief must not ship."""
    contract = validate_contract(brief_md, kept)
    result = {"contract": contract}
    if not contract["ok"]:
        raise PermanentError(f"PERMANENT: brief failed contract — {contract['failures']}")
    if client:
        faith = faithfulness_check(client, judge_model, brief_md, kept, faithfulness_threshold)
        result["faithfulness"] = faith
        if not faith["ok"]:
            raise PermanentError(
                f"PERMANENT: brief failed faithfulness — min score {faith['min_score']:.2f}"
            )
    return result
