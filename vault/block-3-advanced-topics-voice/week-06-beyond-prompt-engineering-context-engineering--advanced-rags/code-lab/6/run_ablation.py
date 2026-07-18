"""Run one lane (or the merged report) of the Week-6 ablation.

  python run_ablation.py --lane baseline --queries queries.jsonl --out results/
  python run_ablation.py --lane tiered   --queries queries.jsonl --out results/ --repeats 3
  python run_ablation.py --report --out results/

Costs: prints an estimate and asks for confirmation above $5.
Prices are read from env so they never fossilize in code:
  PRICE_IN / PRICE_OUT  — $ per Mtok for the generator (defaults 3 / 15,
  the post-intro Sonnet-5-class rate; check current pricing before big runs).
"""

from __future__ import annotations

import argparse
import json
import statistics
from pathlib import Path

import os

PRICE_IN = float(os.environ.get("PRICE_IN", "3"))
PRICE_OUT = float(os.environ.get("PRICE_OUT", "15"))


def load_queries(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def cost(usage: dict) -> float:
    return (usage["input_tokens"] * PRICE_IN + usage["output_tokens"] * PRICE_OUT) / 1e6


def _eval_queries(fn, queries: list[dict], repeats: int, idx) -> list[dict]:
    """Run every query through a lane `repeats` times and judge each run."""
    from judge import judge_one

    per_query = []
    for q in queries:
        runs = []
        for _ in range(repeats):
            res = fn(q["query"], idx)
            # Judge must see the same context the generator saw — truncating
            # here would produce false faithfulness failures.
            ctx = "\n".join(f"[{c}] {idx.by_id[c]['text']}" for c in res.chunk_ids)
            verdict = judge_one(q["query"], res.answer, ctx,
                                q.get("gold_answer"), q.get("answerable", True))
            runs.append({
                "answer": res.answer, "chunk_ids": res.chunk_ids,
                "escalated": res.escalated, "seconds": round(res.seconds, 2),
                "usage": {"input_tokens": res.usage.input_tokens,
                          "output_tokens": res.usage.output_tokens,
                          "calls": res.usage.calls},
                "judge": verdict, "trace": res.trace,
            })
        per_query.append({"id": q["id"], "answerable": q.get("answerable", True),
                          "judge": runs[0]["judge"], "runs": runs})
    return per_query


def run_lane(lane: str, queries: list[dict], repeats: int, out: Path) -> None:
    import harness

    idx = harness.Indexes(harness.load_chunks())
    out.mkdir(parents=True, exist_ok=True)

    if lane == "hybrid_tuned":
        # Sweep the RRF constant and per-retriever candidate depth: one full
        # judged run per grid combo, one results row per combo. Pick the
        # winner, then confirm it on a held-out slice you never tuned on.
        grid = harness.HYBRID_SWEEP_GRID
        est = len(queries) * repeats * len(grid) * 0.02
        if est > 5 and input(f"Estimated >= ${est:.2f}. Continue? [y/N] ").lower() != "y":
            return
        best = None
        for combo in grid:
            tag = f"c{combo['rrf_c']}-lex{combo['k_lex']}-dense{combo['k_dense']}"
            fn = harness.make_hybrid_lane(**combo)
            per_query = _eval_queries(fn, queries, repeats, idx)
            agg = aggregate(f"hybrid_tuned[{tag}]", per_query)
            (out / f"hybrid_tuned_{tag}.json").write_text(
                json.dumps({"lane": f"hybrid_tuned[{tag}]", "params": combo,
                            "aggregate": agg, "per_query": per_query},
                           indent=2), encoding="utf-8")
            print(json.dumps(agg, indent=2))
            score = agg.get("correctness") or agg.get("faithfulness") or 0
            if best is None or score > best[0]:
                best = (score, tag)
        print(f"Sweep winner (by correctness, ties unbroken): {best[1]} — "
              f"confirm on a held-out slice before shipping.")
        return

    fn = harness.LANES[lane]
    mult = 3 if lane in ("tiered", "v2_composed") else (2 if lane == "memory" else 1)
    est = len(queries) * repeats * mult * 0.02
    if est > 5 and input(f"Estimated >= ${est:.2f}. Continue? [y/N] ").lower() != "y":
        return

    first_pass = None
    if lane == "memory":
        # Memory is scored on the SECOND pass over the SET: pass 1 runs every
        # query once so the lane writes RETRIEVAL_MEMORY.md; the judged pass
        # below then retrieves with that memory. Pass-1 spend is reported
        # separately, not silently dropped.
        fp = {"input_tokens": 0, "output_tokens": 0, "calls": 0}
        for q in queries:
            res = fn(q["query"], idx)
            fp["input_tokens"] += res.usage.input_tokens
            fp["output_tokens"] += res.usage.output_tokens
            fp["calls"] += res.usage.calls
        first_pass = {"usage": fp, "cost": round(cost(fp), 5)}

    per_query = _eval_queries(fn, queries, repeats, idx)
    agg = aggregate(lane, per_query)
    payload = {"lane": lane, "aggregate": agg, "per_query": per_query}
    if first_pass is not None:
        payload["memory_first_pass"] = first_pass
    (out / f"{lane}.json").write_text(json.dumps(payload, indent=2),
                                      encoding="utf-8")
    print(json.dumps(agg, indent=2))
    if first_pass is not None:
        print(f"memory first (unjudged) pass cost: ${first_pass['cost']}")


def aggregate(lane: str, per_query: list[dict]) -> dict:
    def mean_dim(dim: str, answerable: bool) -> float | None:
        vals = [r["judge"][dim] for r in per_query
                if r["answerable"] is answerable and r["judge"].get(dim) is not None]
        return round(sum(vals) / len(vals), 3) if vals else None

    costs, secs, esc = [], [], 0
    for r in per_query:
        for run in r["runs"]:
            costs.append(cost(run["usage"]))
            secs.append(run["seconds"])
            esc += bool(run["escalated"])
    return {
        "lane": lane,
        "n_queries": len(per_query),
        "faithfulness": mean_dim("faithfulness", True),
        "answer_relevancy": mean_dim("answer_relevancy", True),
        "correctness": mean_dim("correctness", True),
        "answerability": mean_dim("answerability", False),
        "mean_cost_per_query": round(statistics.mean(costs), 5) if costs else None,
        "p50_seconds": round(statistics.median(secs), 2) if secs else None,
        "p95_seconds": round(sorted(secs)[int(0.95 * (len(secs) - 1))], 2) if secs else None,
        "spread_cost": round(statistics.pstdev(costs), 5) if len(costs) > 1 else 0,
        "escalation_rate": round(esc / max(len(per_query), 1), 3),
    }


def report(out: Path) -> None:
    rows = []
    for f in sorted(out.glob("*.json")):
        data = json.loads(f.read_text(encoding="utf-8"))
        rows.append(data["aggregate"])
    if not rows:
        raise SystemExit("No lane results in results/ yet.")
    cols = ["lane", "correctness", "faithfulness", "answer_relevancy",
            "answerability", "mean_cost_per_query", "p50_seconds",
            "p95_seconds", "escalation_rate"]
    lines = ["# Ablation report", "",
             "| " + " | ".join(cols) + " |",
             "|" + "---|" * len(cols)]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "—")) for c in cols) + " |")
    lines += ["", "Annotate each row: SHIP / NO-SHIP + one sentence.",
              "Gates live in ABLATION_PLAN.md — written before these runs."]
    (out / "ablation_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out/'ablation_report.md'}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--lane", choices=["baseline", "hybrid_tuned", "reranked",
                                       "budgeted", "memory", "tiered",
                                       "v2_composed"])
    ap.add_argument("--queries", default="queries.jsonl")
    ap.add_argument("--out", default="results/")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()

    if args.report:
        report(Path(args.out))
    elif args.lane:
        run_lane(args.lane, load_queries(args.queries), args.repeats, Path(args.out))
    else:
        ap.print_help()
