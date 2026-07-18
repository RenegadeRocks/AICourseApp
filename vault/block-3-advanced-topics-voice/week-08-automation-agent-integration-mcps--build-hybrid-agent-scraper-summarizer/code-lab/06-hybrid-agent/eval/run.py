"""The eval gate. `python -m eval.run --gate` runs (a) the relevance golden set
against your hand labels and (b) the binary synthesis rubric against every
checkpointed brief in runs/<date>/, and exits non-zero if either fails at
threshold — wire it so no prompt/model change ships without a green gate. This
is your model-drift defense (05-fri): model drift is invisible in a single
output and only shows against a fixed reference.

  python -m eval.run --gate --config config.yaml
  python -m eval.run --validate-judge eval/golden_relevance.jsonl
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml
from dotenv import load_dotenv

from eval.rubric import judge_agreement, score_brief
from stages import judge as judge_stage

load_dotenv()

RELEVANCE_THRESHOLD = 0.90  # judge/human agreement to pass the gate


def load_golden(path: str) -> list[dict]:
    """One JSON object per line: {title, summary, label} where label is
    true/false for keep/drop (your hand labels)."""
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def run_relevance_gate(config_path: str, golden_path: str) -> bool:
    cfg = yaml.safe_load(Path(config_path).read_text())
    golden = load_golden(golden_path)
    from anthropic import Anthropic
    client = Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    niche = cfg["niche"]["description"]
    threshold = cfg["niche"]["relevance_threshold"]

    judge_labels, human_labels = [], []
    for row in golden:
        item = {"title": row["title"], "summary": row.get("summary", ""), "url": row.get("url", "")}
        j = judge_stage.judge_item(client, cfg["budget"]["judge_model"], niche, item)
        judge_labels.append(bool(j["keep"]) and float(j["score"]) >= threshold)
        human_labels.append(bool(row["label"]))

    agreement = judge_agreement(judge_labels, human_labels)
    passed = agreement >= RELEVANCE_THRESHOLD
    print(f"relevance golden set: {agreement:.1%} agreement "
          f"({'PASS' if passed else 'FAIL'} at {RELEVANCE_THRESHOLD:.0%})")
    return passed


def run_synthesis_rubric(runs_dir: str = "runs") -> bool:
    """Score every checkpointed brief (runs/<date>/05-brief.md) with the binary
    synthesis rubric, against that run's kept items (04-judged.json). The
    checkpoints ARE the frozen snapshots: a rubric failure on a brief that
    previously shipped means the prompt, model, or rubric drifted. No snapshots
    yet is a skip, not a pass-by-default — the printout says so."""
    briefs = sorted(Path(runs_dir).glob("*/05-brief.md"))
    if not briefs:
        print("synthesis rubric: no runs/<date>/05-brief.md snapshots yet — "
              "SKIPPED (gate covered the relevance golden set only)")
        return True
    all_pass = True
    for bp in briefs:
        run_name = bp.parent.name
        try:
            judged = json.loads((bp.parent / "04-judged.json").read_text())
            kept = [it for it in judged if it.get("keep")]
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"synthesis rubric: {run_name}: FAIL (unreadable 04-judged.json — {e})")
            all_pass = False
            continue
        res = score_brief(bp.read_text(), kept)
        if res["pass"]:
            print(f"synthesis rubric: {run_name}: PASS")
        else:
            failed = [k for k, v in res["criteria"].items() if not v]
            print(f"synthesis rubric: {run_name}: FAIL ({', '.join(failed)})")
            all_pass = False
    return all_pass


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--gate", action="store_true")
    ap.add_argument("--validate-judge", default=None)
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--golden", default="eval/golden_relevance.jsonl")
    args = ap.parse_args()

    if args.validate_judge:
        ok = run_relevance_gate(args.config, args.validate_judge)
        print("judge validated" if ok else "judge below threshold — fix the rubric before gating")
        return 0 if ok else 1

    if args.gate:
        golden = args.golden if Path(args.golden).exists() else "eval/golden_relevance.example.jsonl"
        relevance_ok = run_relevance_gate(args.config, golden)
        rubric_ok = run_synthesis_rubric()
        passed = relevance_ok and rubric_ok
        print(f"gate: {'PASS' if passed else 'FAIL'} "
              f"(relevance {'ok' if relevance_ok else 'FAIL'}, "
              f"synthesis rubric {'ok' if rubric_ok else 'FAIL'})")
        return 0 if passed else 1

    print("nothing to do — pass --gate or --validate-judge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
