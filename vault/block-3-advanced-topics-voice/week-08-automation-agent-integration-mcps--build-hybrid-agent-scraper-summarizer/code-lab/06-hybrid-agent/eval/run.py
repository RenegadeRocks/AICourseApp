"""The eval gate. `python -m eval.run --gate` exits non-zero if any golden set
fails at threshold — wire it so no prompt/model change ships without a green
gate. This is your model-drift defense (05-fri): model drift is invisible in a
single output and only shows against a fixed reference.

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

from eval.rubric import judge_agreement
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
        passed = run_relevance_gate(args.config, golden)
        # Extend here: run the synthesis rubric against frozen end-to-end snapshots.
        return 0 if passed else 1

    print("nothing to do — pass --gate or --validate-judge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
