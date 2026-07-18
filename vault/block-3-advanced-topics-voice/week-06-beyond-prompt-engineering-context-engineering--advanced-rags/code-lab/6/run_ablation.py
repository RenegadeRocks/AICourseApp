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


def run_lane(lane: str, queries: list[dict], repeats: int, out: Path) -> None:
    import harness
    from judge import judge_one

    idx = harness.Indexes(harness.load_chunks())
    fn = harness.LANES[lane]
    est = len(queries) * repeats * (3 if lane in ("tiered", "v2_composed") else 1) * 0.02
    if est > 5 and input(f"Estimated >= ${est:.2f}. Continue? [y/N] ").lower() != "y":
        return

    per_query = []
    passes = 2 if lane == "memory" else 1  # memory is scored on the 2nd pass
    for q in queries:
        runs = []
        for _ in range(repeats):
            for p in range(passes):
                res = fn(q["query"], idx)
            ctx = "\n".join(f"[{c}] {idx.by_id[c]['text'][:400]}" for c in res.chunk_ids)
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

    agg = aggregate(lane, per_query)
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{lane}.json").write_text(
        json.dumps({"lane": lane, "aggregate": agg, "per_query": per_query},
                   indent=2), encoding="utf-8")
    print(json.dumps(agg, indent=2))


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
