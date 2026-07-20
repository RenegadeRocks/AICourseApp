"""Binary-rubric judge for the Week-6 ablation harness.

Dimensions (all binary, per Week-4 discipline):
  faithfulness      — every claim in the answer is supported by cited chunks
  answer_relevancy  — the answer addresses the question asked
  correctness       — the answer agrees with the gold answer
  answerability     — for answerable=False queries: did the system decline?

Validate before trusting: `python judge.py --validate labels.csv`
labels.csv columns: query_id,dimension,human_label (1/0)
Target: >=90% judge-human agreement (Block 2 Week 4 bar).
"""

from __future__ import annotations

import csv
import json
import os
import sys

from anthropic import Anthropic

JUDGE_MODEL = os.environ.get("ANTHROPIC_JUDGE_MODEL",
                             os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-5"))
client = Anthropic()

RUBRIC = """You are grading a retrieval-augmented answer. Grade each dimension
strictly 1 or 0. Think briefly, then output ONLY JSON:
{"faithfulness": 0|1, "answer_relevancy": 0|1, "correctness": 0|1, "critique": "<one sentence>"}

faithfulness=1 only if every factual claim in the answer is supported by the
provided context chunks (the [id] citations must point at supporting chunks).
answer_relevancy=1 only if the answer addresses the specific question.
correctness=1 only if the answer is consistent with the gold answer.
"""


def judge_one(query: str, answer: str, context: str, gold: str | None,
              answerable: bool) -> dict:
    if not answerable:
        declined = "NOT_IN_CORPUS" in answer
        return {"faithfulness": None, "answer_relevancy": None,
                "correctness": None, "answerability": 1 if declined else 0,
                "critique": "declined correctly" if declined else
                            "fabricated an answer to an unanswerable query"}
    msg = client.messages.create(
        model=JUDGE_MODEL, max_tokens=300, system=RUBRIC,
        messages=[{"role": "user", "content":
                   f"Question: {query}\n\nGold answer: {gold}\n\n"
                   f"Context chunks:\n{context}\n\nAnswer to grade:\n{answer}"}])
    text = "".join(b.text for b in msg.content if b.type == "text")
    try:
        out = json.loads(text[text.index("{"): text.rindex("}") + 1])
    except ValueError:
        out = {"faithfulness": 0, "answer_relevancy": 0, "correctness": 0,
               "critique": "judge output unparseable"}
    out["answerability"] = None
    out["_judge_usage"] = {"input": msg.usage.input_tokens,
                           "output": msg.usage.output_tokens}
    return out


def validate(labels_csv: str, results_json: str) -> None:
    """Compare judge verdicts against human labels; print agreement."""
    with open(results_json, encoding="utf-8") as f:
        rows = {r["id"]: r for r in json.load(f)["per_query"]}
    total = agree = 0
    by_dim: dict[str, list[int]] = {}
    with open(labels_csv, encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            r = rows.get(rec["query_id"])
            if not r:
                continue
            j = r["judge"].get(rec["dimension"])
            if j is None:
                continue
            hit = int(int(rec["human_label"]) == int(j))
            total += 1; agree += hit
            by_dim.setdefault(rec["dimension"], []).append(hit)
    if not total:
        sys.exit("No overlapping labels found.")
    print(f"Overall judge-human agreement: {agree}/{total} = {agree/total:.1%}")
    for dim, hits in sorted(by_dim.items()):
        print(f"  {dim:<18} {sum(hits)}/{len(hits)} = {sum(hits)/len(hits):.1%}")
    bar = 0.90
    verdict = "PASS" if agree / total >= bar else "FAIL — fix the rubric before running lanes"
    print(f"Week-4 bar (>=90%): {verdict}")


if __name__ == "__main__":
    if "--validate" in sys.argv:
        i = sys.argv.index("--validate")
        labels = sys.argv[i + 1]
        results = sys.argv[i + 2] if len(sys.argv) > i + 2 else "results/baseline.json"
        validate(labels, results)
    else:
        print(__doc__)
