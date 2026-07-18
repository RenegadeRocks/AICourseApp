"""Package-spec generator: package.yaml -> the Saturday deliverable set.

Usage:
    python package_spec.py package.yaml --out out/

Generates markdown files:
    one_pager.md            — the sales page a stranger could buy from
    tier_sheet.md           — the Tuesday ladder as a table
    onboarding_checklist.md — owner + clock per step
    delivery_runbook.md     — the Wednesday runbook skeleton
    eval_report_template.md — monthly report with a provenance block
    demo_script.md          — 5-minute script incl. the pricing sentence
"""

from __future__ import annotations

import argparse
import pathlib
import sys

import yaml

from models import get_rate


def load(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        cfg = yaml.safe_load(fh)
    for key in ("package", "economics", "tiers", "guarantee",
                "onboarding_checklist", "runbook_stages", "demo"):
        if key not in cfg:
            sys.exit(f"Config missing required key: '{key}'")
    return cfg


def labor_line_usd(cfg: dict) -> float | None:
    labor = cfg["package"].get("labor_line")
    if not labor:
        return None
    return float(labor["hours_per_month"]) * float(labor["loaded_hourly_rate_usd"])


def one_pager(cfg: dict) -> str:
    p = cfg["package"]
    g = cfg["guarantee"]
    lines = [f"# {p['name']}", ""]
    lines += [f"**For {p['niche']}.**", "", p["outcome_statement"].strip(), ""]

    line = labor_line_usd(cfg)
    if line is not None:
        cheapest = min(float(t["price_usd_month"]) for t in cfg["tiers"])
        lines += [
            "## The math",
            "",
            f"{cfg['package']['labor_line']['description']} costs roughly "
            f"${line:,.0f}/month in loaded time. {p['name']} starts at "
            f"${cheapest:,.0f}/month, never takes a vacation, and links every "
            "claim to its source.",
            "",
        ]

    lines += ["## What you get", ""]
    for t in cfg["tiers"]:
        lines.append(
            f"- **{t['name']}** (${float(t['price_usd_month']):,.0f}/mo): "
            f"{t['sources']} sources, {t['delivery']}; {t['eval_deliverable']}."
        )
    lines += ["", "## What we promise", ""]
    for promise in g["promises"]:
        lines.append(f"- {promise}")
    lines += ["", f"**If we miss:** {g['consequence']}", ""]

    if cfg.get("exclusions"):
        lines += ["## What this is not", ""]
        for ex in cfg["exclusions"]:
            lines.append(f"- {ex['item']} — {ex['route']}")
        lines.append("")

    eco = cfg["economics"]
    lines += [
        "## Getting started",
        "",
        f"One-time onboarding: ${float(eco['onboarding_fee_usd']):,.0f}. "
        "Live within 10 business days. Cancel monthly.",
    ]
    return "\n".join(lines) + "\n"


def tier_sheet(cfg: dict) -> str:
    tiers = cfg["tiers"]
    cols = ["name", "price_usd_month", "sources", "delivery",
            "eval_deliverable", "support", "terms"]
    heads = ["Tier", "Price/mo", "Sources", "Delivery", "Eval", "Support", "Terms"]
    lines = [f"# {cfg['package']['name']} — tier sheet", ""]
    lines.append("| " + " | ".join(heads) + " |")
    lines.append("|" + "---|" * len(heads))
    for t in tiers:
        row = []
        for c in cols:
            v = t[c]
            if c == "price_usd_month":
                v = f"${float(v):,.0f}"
            row.append(str(v))
        lines.append("| " + " | ".join(row) + " |")
    lines += ["", "_Prices date-stamped against the rate card in models.py; "
              "see grandfathering policy before quoting legacy customers._"]
    return "\n".join(lines) + "\n"


def onboarding(cfg: dict) -> str:
    lines = [f"# {cfg['package']['name']} — onboarding checklist", ""]
    lines.append("| # | Step | Owner | Day(s) | Done |")
    lines.append("|---|---|---|---|---|")
    for i, item in enumerate(cfg["onboarding_checklist"], 1):
        lines.append(f"| {i} | {item['step']} | {item['owner']} | {item['days']} | ☐ |")
    lines += ["", "Time-to-first-value target: DRAFT brief on the customer's "
              "screen by day 3. If a step slips, the runbook owner says so "
              "on the same day — silence is the only unacceptable status."]
    return "\n".join(lines) + "\n"


def runbook(cfg: dict) -> str:
    eco = cfg["economics"]
    rate = get_rate(eco["model_tier"])
    lines = [f"# {cfg['package']['name']} — delivery runbook (skeleton)", ""]
    lines += [f"Model tier: **{rate.name}** (rate verified {rate.rate_date}). "
              "Re-verify the rate card monthly and on every provider "
              "announcement.", ""]
    for i, stage in enumerate(cfg["runbook_stages"], 1):
        lines += [f"## Stage {i} — {stage}", "",
                  "- Owner:", "- Inputs:", "- Procedure (numbered, no 'figure out' steps):",
                  "- Failure mode + response:", "- Evidence it completed:", ""]
    return "\n".join(lines) + "\n"


def eval_report(cfg: dict) -> str:
    p = cfg["package"]
    return f"""# {p['name']} — monthly eval report — {{MONTH}}

**Customer:** {{TENANT}}    **Package version:** {{vX.Y.Z}}    **Model tier:** {{TIER (rate date)}}

## Golden-set provenance
- Set size / niche pack: {{N}} items, {{PACK}}
- How sampled: {{production traces / synthetic / customer-labeled}}
- Last refreshed against production: {{DATE}}
- Judge alignment check (human vs LLM-judge): {{X%}} on {{DATE}}

## Results
| Metric | This month | Last month | Threshold | Status |
|---|---|---|---|---|
| Delivery SLO (by 7:00, business days) | {{%}} | {{%}} | ≥99% | {{OK/BREACH}} |
| Golden-set pass rate | {{%}} | {{%}} | ≥{{T}}% | {{OK/BREACH}} |
| Claim-level source-link coverage | {{%}} | {{%}} | 100% | {{OK/BREACH}} |
| Drift vs deployment baseline | {{±pp}} | {{±pp}} | within ±5pp | {{OK/WATCH}} |

## Incidents ({{N}})
{{date — cause — customer impact — remediation — disclosed within 48h? }}

## Model/config changes this month
{{model swaps (golden set re-run results), prompt-pack version, source changes}}

## Value line
Coverage delivered: ~{{H}} analyst-hours equivalent this month
(basis: {p['labor_line']['description']}, {p['labor_line']['hours_per_month']}h/mo).
"""


def demo_script(cfg: dict) -> str:
    p = cfg["package"]
    d = cfg["demo"]
    return f"""# {p['name']} — {d['minutes']}-minute demo script

**0:00–0:30 — The pain, in their words.** "You currently find out about
competitor moves when a customer mentions them." One sentence, then stop.

**0:30–1:30 — Show the artifact, not the architecture.** Open a real (redacted)
brief from a live tenant. Point at one claim, click its source link. Say:
"Every claim does that."

**1:30–2:30 — The morning it lands.** Walk one day: 7am delivery, the two
items worth acting on, the config-change flow when they want a source swapped.

**2:30–3:30 — Trust, evidence-grade.** Show a monthly eval report. Golden-set
pass rate, drift line, incident log. Say: "You get this every month. Most
vendors won't show you theirs."

**3:30–4:15 — Price, verbatim, no flinch:**
> {d['pricing_sentence'].strip()}

Then be quiet. The silence is part of the script.

**4:15–5:00 — The close.** "Onboarding takes ten business days and starts
with you nominating sources — want me to send the intake form today?"

## Objection lines (rehearse out loud)
- "Cheaper tool exists" → "That's the self-serve tier of this market; you're
  paying for {p['niche']}-specific packs, the eval report, and a human who is
  accountable when a source breaks."
- "Can you guarantee accuracy?" → point at the promises list; explain what a
  measured guarantee is and why vendors who promise 99% without a golden set
  are guessing.
- "Can you add [excluded thing]?" → the route from the exclusions table,
  never an improvised yes.
"""


GENERATORS = {
    "one_pager.md": one_pager,
    "tier_sheet.md": tier_sheet,
    "onboarding_checklist.md": onboarding,
    "delivery_runbook.md": runbook,
    "eval_report_template.md": eval_report,
    "demo_script.md": demo_script,
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", help="path to package.yaml")
    ap.add_argument("--out", default="out", help="output directory")
    args = ap.parse_args()

    cfg = load(args.config)
    out = pathlib.Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    for fname, gen in GENERATORS.items():
        path = out / fname
        path.write_text(gen(cfg), encoding="utf-8")
        print(f"wrote {path}")
    print(f"\n{len(GENERATORS)} files in {out}/ — now read one_pager.md as a "
          "stranger. If you wouldn't buy, the gap is in package.yaml.")


if __name__ == "__main__":
    main()
