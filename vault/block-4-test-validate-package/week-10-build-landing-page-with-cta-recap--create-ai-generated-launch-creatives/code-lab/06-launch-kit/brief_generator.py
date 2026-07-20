#!/usr/bin/env python3
"""Creative-brief generator for a launch kit.

Reads a launch-kit config (package facts + brand spec + asset requests) and
emits one markdown creative brief per asset into briefs/. Briefs are written
BEFORE generation: constraints in, prompts drafted, QA criteria attached.

Usage:
    python brief_generator.py example/launch_kit.json [--out briefs]

Stdlib only. Deterministic: no model calls; the brief is a spec, and specs
should not be sampled.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import date
from pathlib import Path

# Per-kind mechanical requirements. Mirrored by qa_runner.RULES; keep in sync.
ASSET_RULES = {
    "hero": {
        "dimensions": "1920x1080 master; crops 16:9 and 4:5",
        "max_kb": 400,
        "notes": "No text in the generated image (type is set in the design "
                 "tool). Real product UI is composited, never generated.",
    },
    "og": {
        "dimensions": "1200x630 exactly",
        "max_kb": 300,
        "notes": "Must read at 240px-wide thumbnail: wordmark, one claim "
                 "(max ~7 words), one visual element.",
    },
    "ad": {
        "dimensions": "1080x1080 (feed) or 1080x1350 (vertical)",
        "max_kb": 500,
        "notes": "Claim text must be an exact string from the substantiation "
                 "file. Review platform default-on enhancements before launch.",
    },
    "social_cutdown": {
        "dimensions": "1080x1920 or 1080x1080, 15-30s",
        "max_kb": None,
        "notes": "Cut from the demo video's beats; captions burned in "
                 "(feeds autoplay muted).",
    },
    "video_storyboard": {
        "dimensions": "n/a (document)",
        "max_kb": None,
        "notes": "Four beats: pain artifact / real run / guardrail beat / "
                 "scoped claim + CTA. Screen capture of the real product; "
                 "generated footage is b-roll only.",
    },
}

HOOKS = {
    "pain": "Lead with the buyer's artifact of pain (the inbox, the queue, "
            "the spreadsheet), not a category statement.",
    "proof": "Lead with the strongest substantiated number and its scope.",
    "objection": "Lead with the uncomfortable question ('What happens when "
                 "it's wrong?') and answer it with the escalation design.",
}


def build_prompt_drafts(asset: dict, brand: dict) -> list[str]:
    """Draft 2-3 generation prompts that mechanically carry the brand spec."""
    palette = ", ".join(brand.get("palette", []))
    negatives = "; ".join(brand.get("negative_list", []))
    anchor = brand.get("style_anchor", "brand anchor set")
    subject = asset.get("subject", asset.get("purpose", "launch visual"))
    base = (
        f"{subject}. Style: {brand.get('aesthetic', 'clean, minimal')}, "
        f"consistent with {anchor}. Palette: {palette}. "
        f"Do NOT include: {negatives}."
    )
    return [
        base,
        base + " Wide negative space on the "
               f"{asset.get('copy_side', 'left')} for typesetting.",
        base + " Simplified composition, fewer elements, thumbnail-legible.",
    ]


def disclosure_prediction(asset: dict) -> str:
    if not asset.get("ai_generated", True):
        return "Not AI-generated: no disclosure required."
    if asset.get("photorealistic_people", False):
        return ("AI-generated WITH photorealistic people: Meta ad disclosure "
                "required; YouTube disclosure if used in video; verify current "
                "platform policy the week you publish.")
    return ("AI-generated, non-photorealistic: platform disclosure generally "
            "not triggered (verify current policy); record ai_generated=true "
            "in the archive either way.")


def render_brief(asset: dict, cfg: dict) -> str:
    brand = cfg["brand"]
    package = cfg["package"]
    kind = asset["kind"]
    rules = ASSET_RULES.get(kind, {})
    lines: list[str] = []
    add = lines.append

    add(f"# Creative brief — {asset['id']} ({kind})")
    add("")
    add(f"_Generated {date.today().isoformat()} by brief_generator.py. "
        "Write-then-generate: no asset production before this brief is read._")
    add("")
    add("## Purpose")
    add(asset.get("purpose", "(fill in: what this asset must accomplish)"))
    add("")
    add("## Package facts this asset may use")
    add(f"- Product: {package['name']} — {package['one_liner']}")
    add(f"- Scoped promise: {package['scoped_promise']}")
    add(f"- Substantiated claims available: see claims file "
        f"({cfg.get('claims_file', 'claims.json')}). Use exact strings only.")
    add("")
    if kind == "ad" and asset.get("hook") in HOOKS:
        add("## Hook")
        add(f"**{asset['hook']}** — {HOOKS[asset['hook']]}")
        add("")
    add("## Mechanical requirements")
    add(f"- Dimensions: {rules.get('dimensions', 'per manifest')}")
    if rules.get("max_kb"):
        add(f"- Max served size: {rules['max_kb']} KB")
    add(f"- Filename: `{asset['id']}` prefix, variant suffix (e.g. "
        f"`{asset['id']}_v03.png`)")
    add(f"- Notes: {rules.get('notes', '-')}")
    add("")
    add("## Brand constraints (non-negotiable)")
    add(f"- Positioning stance: {brand.get('stance', '(declare it)')}")
    add(f"- Palette: {', '.join(brand.get('palette', []))}")
    add(f"- Aesthetic: {brand.get('aesthetic', '-')} "
        f"(anchor: {brand.get('style_anchor', '-')})")
    add(f"- Never include: {'; '.join(brand.get('negative_list', []))}")
    add("- Type is set outside the model unless the tool is a text-rendering "
        "specialist.")
    add("")
    if kind not in ("video_storyboard", "social_cutdown"):
        add("## Prompt drafts (batch >= 12 candidates across these)")
        for i, p in enumerate(build_prompt_drafts(asset, brand), 1):
            add(f"{i}. {p}")
        add("")
    add("## Disclosure prediction")
    add(disclosure_prediction(asset))
    add("")
    add("## QA criteria (the gate this asset must pass)")
    add("- Mechanical: dimensions, size budget, filename, alt text, archive "
        "record (prompt/tool/settings/license), disclosure flag consistency, "
        "claims match substantiation file. (Automated: qa_runner.py)")
    add("- Judgment: artifact scan, brand-spec compliance, thumbnail "
        "legibility, slop test, claim test, positioning test. (Human, ~60s)")
    add("")
    add("## Selection rule")
    add("Kill off-brand candidates before judging beauty. If no candidate "
        "clears the brief, fix the brief and re-batch; never negotiate with "
        "a mediocre candidate.")
    add("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("config", help="path to launch_kit.json")
    ap.add_argument("--out", default="briefs", help="output directory")
    args = ap.parse_args(argv)

    cfg_path = Path(args.config)
    try:
        cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read config {cfg_path}: {e}", file=sys.stderr)
        return 2

    missing = [k for k in ("package", "brand", "assets") if k not in cfg]
    if missing:
        print(f"ERROR: config missing keys: {missing}", file=sys.stderr)
        return 2

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    written = []
    for asset in cfg["assets"]:
        if "id" not in asset or "kind" not in asset:
            print(f"ERROR: asset entry needs 'id' and 'kind': {asset}",
                  file=sys.stderr)
            return 2
        if asset["kind"] not in ASSET_RULES:
            print(f"WARNING: unknown kind '{asset['kind']}' for "
                  f"{asset['id']}; brief will lack kind rules",
                  file=sys.stderr)
        path = out_dir / f"{asset['id']}.md"
        path.write_text(render_brief(asset, cfg), encoding="utf-8")
        written.append(path)

    print(f"Wrote {len(written)} brief(s) to {out_dir}/:")
    for p in written:
        print(f"  - {p}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
