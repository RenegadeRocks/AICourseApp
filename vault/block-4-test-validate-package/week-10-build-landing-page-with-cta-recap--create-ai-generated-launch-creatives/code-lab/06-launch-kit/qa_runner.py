#!/usr/bin/env python3
"""Asset-QA checklist runner: the mechanical half of Thursday's QA gate.

Reads an asset manifest (qa_manifest.json), checks every asset against the
per-kind rules, and writes reports/qa_report.md. Exit code 0 = all pass,
1 = at least one failure, 2 = configuration error. No asset ships with an
open failure.

Checks (mechanical only; the judgment half stays human):
  - file exists; dimensions parsed from PNG/JPEG headers (stdlib, no Pillow)
  - per-kind dimension rules (OG must be exactly 1200x630) and size budgets
  - filename starts with the asset id
  - alt text present and non-trivial
  - archive record complete: prompt, tool, settings, license_basis
  - disclosure consistency: ai_generated + photorealistic_people => platform
    disclosure flag must be set
  - copy checks: banned unsubstantiated-claim phrases; every numeric claim
    (percentages, dollar amounts) must appear in the claims file

Usage:
    python qa_runner.py example/qa_manifest.json [--claims example/claims.json]
"""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path

# Per-kind mechanical rules. Mirrors brief_generator.ASSET_RULES; keep in sync.
RULES = {
    "hero": {"min_width": 1600, "max_kb": 400},
    "og": {"exact": (1200, 630), "max_kb": 300},
    "ad": {"allowed": [(1080, 1080), (1080, 1350)], "max_kb": 500},
    "social_cutdown": {},        # video: dimension checks out of scope here
    "video_storyboard": {},      # document asset
}

BANNED_PHRASES = [
    "100% accurate",
    "never hallucinates",
    "no hallucinations",
    "guaranteed results",
    "fully autonomous",       # unless you truly run unattended with no HITL
    "bank-grade",             # vibes, not a spec; state the actual control
    "world's first",          # substantiate or delete
    "revolutionary",
]

NUM_CLAIM_RE = re.compile(r"(\d+(?:\.\d+)?%|\$\d[\d,]*(?:\.\d+)?[km]?)",
                          re.IGNORECASE)


# ---------------------------------------------------------------- dimensions

def png_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 24 or data[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", data[16:24])
    return w, h


def jpeg_dimensions(data: bytes) -> tuple[int, int] | None:
    if len(data) < 4 or data[:2] != b"\xff\xd8":
        return None
    i = 2
    while i + 9 < len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        # SOF0..SOF15 minus DHT(C4)/DAC(CC)/RST etc. carry dimensions
        if 0xC0 <= marker <= 0xCF and marker not in (0xC4, 0xC8, 0xCC):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        seg_len = struct.unpack(">H", data[i + 2:i + 4])[0]
        i += 2 + seg_len
    return None


def image_dimensions(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    return png_dimensions(data) or jpeg_dimensions(data)


# ------------------------------------------------------------------- results

@dataclass
class AssetResult:
    asset_id: str
    passes: list[str] = field(default_factory=list)
    failures: list[str] = field(default_factory=list)

    def ok(self, msg: str) -> None:
        self.passes.append(msg)

    def fail(self, msg: str) -> None:
        self.failures.append(msg)

    @property
    def passed(self) -> bool:
        return not self.failures


# -------------------------------------------------------------------- checks

def check_file_and_dimensions(asset: dict, base: Path, r: AssetResult) -> None:
    kind = asset["kind"]
    rules = RULES.get(kind, {})
    file_rel = asset.get("file")
    if not file_rel:
        if kind in ("video_storyboard",):
            r.ok("document asset: no file dimension checks")
            return
        r.fail("no 'file' in manifest entry")
        return
    path = base / file_rel
    if not path.is_file():
        r.fail(f"file missing: {path}")
        return
    r.ok(f"file exists: {file_rel}")

    if not path.name.startswith(asset["id"]):
        r.fail(f"filename '{path.name}' does not start with id "
               f"'{asset['id']}'")
    else:
        r.ok("filename convention")

    size_kb = path.stat().st_size / 1024
    max_kb = rules.get("max_kb")
    if max_kb is not None:
        if size_kb > max_kb:
            r.fail(f"size {size_kb:.0f}KB exceeds budget {max_kb}KB")
        else:
            r.ok(f"size {size_kb:.0f}KB within {max_kb}KB budget")

    if path.suffix.lower() in (".png", ".jpg", ".jpeg"):
        dims = image_dimensions(path)
        if dims is None:
            r.fail("could not parse image dimensions (corrupt header?)")
            return
        w, h = dims
        if "exact" in rules and (w, h) != tuple(rules["exact"]):
            r.fail(f"dimensions {w}x{h}; must be exactly "
                   f"{rules['exact'][0]}x{rules['exact'][1]}")
        elif "allowed" in rules and (w, h) not in [tuple(a) for a in
                                                   rules["allowed"]]:
            r.fail(f"dimensions {w}x{h} not in allowed set {rules['allowed']}")
        elif "min_width" in rules and w < rules["min_width"]:
            r.fail(f"width {w} below minimum {rules['min_width']}")
        else:
            r.ok(f"dimensions {w}x{h}")


def check_alt_text(asset: dict, r: AssetResult) -> None:
    if asset["kind"] in ("video_storyboard",):
        return
    alt = (asset.get("alt_text") or "").strip()
    if len(alt) < 10:
        r.fail("alt text missing or under 10 chars")
    else:
        r.ok("alt text present")


def check_archive(asset: dict, r: AssetResult) -> None:
    archive = asset.get("archive") or {}
    required = ("prompt", "tool", "settings", "license_basis")
    missing = [k for k in required if not str(archive.get(k, "")).strip()]
    if asset.get("ai_generated", False):
        if missing:
            r.fail(f"archive record incomplete: missing {missing}")
        else:
            r.ok("archive record complete (prompt/tool/settings/license)")
    else:
        if not str(archive.get("license_basis", "")).strip():
            r.fail("non-AI asset still needs license_basis (photo/stock/own)")
        else:
            r.ok("license basis recorded")


def check_disclosure(asset: dict, r: AssetResult) -> None:
    if asset.get("ai_generated", False) and \
            asset.get("photorealistic_people", False):
        flags = asset.get("disclosure") or {}
        if not any(flags.values()):
            r.fail("AI-generated photorealistic people but no platform "
                   "disclosure flag set (Meta/YouTube rules)")
        else:
            r.ok("disclosure flags set for photorealistic AI content")
    else:
        r.ok("no platform disclosure triggered (verify policy at publish)")


def check_copy(asset: dict, base: Path, allowed_claims: list[str],
               r: AssetResult) -> None:
    copy_rel = asset.get("copy_file")
    if not copy_rel:
        return
    path = base / copy_rel
    if not path.is_file():
        r.fail(f"copy file missing: {path}")
        return
    text = path.read_text(encoding="utf-8")
    low = text.lower()

    hits = [p for p in BANNED_PHRASES if p in low]
    if hits:
        r.fail(f"banned phrases present: {hits}")
    else:
        r.ok("no banned unsubstantiated phrases")

    claims_found = NUM_CLAIM_RE.findall(text)
    allowed_blob = " ".join(allowed_claims).lower()
    unsubstantiated = [c for c in claims_found
                       if c.lower() not in allowed_blob]
    if unsubstantiated:
        r.fail(f"numeric claims not in substantiation file: "
               f"{unsubstantiated}")
    elif claims_found:
        r.ok(f"all numeric claims substantiated: {claims_found}")
    else:
        r.ok("no numeric claims in copy")


# --------------------------------------------------------------------- main

def run(manifest_path: Path, claims_path: Path | None) -> int:
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as e:
        print(f"ERROR: cannot read manifest: {e}", file=sys.stderr)
        return 2

    base = manifest_path.parent
    claims_file = claims_path or (base / manifest.get("claims_file",
                                                      "claims.json"))
    allowed_claims: list[str] = []
    if Path(claims_file).is_file():
        try:
            allowed_claims = json.loads(
                Path(claims_file).read_text(encoding="utf-8"))["claims"]
        except (OSError, json.JSONDecodeError, KeyError) as e:
            print(f"ERROR: bad claims file {claims_file}: {e}",
                  file=sys.stderr)
            return 2
    else:
        print(f"WARNING: no claims file at {claims_file}; every numeric "
              "claim will fail", file=sys.stderr)

    assets = manifest.get("assets", [])
    if not assets:
        print("ERROR: manifest has no assets", file=sys.stderr)
        return 2

    results: list[AssetResult] = []
    for asset in assets:
        if "id" not in asset or "kind" not in asset:
            print(f"ERROR: asset needs 'id' and 'kind': {asset}",
                  file=sys.stderr)
            return 2
        r = AssetResult(asset_id=asset["id"])
        check_file_and_dimensions(asset, base, r)
        check_alt_text(asset, r)
        check_archive(asset, r)
        check_disclosure(asset, r)
        check_copy(asset, base, allowed_claims, r)
        results.append(r)

    # ---- report
    failed = [r for r in results if not r.passed]
    lines = ["# Asset QA report", ""]
    lines.append(f"Manifest: `{manifest_path}` — {len(results)} asset(s), "
                 f"{len(failed)} failing")
    lines.append("")
    for r in results:
        status = "PASS" if r.passed else "FAIL"
        lines.append(f"## [{status}] {r.asset_id}")
        for m in r.failures:
            lines.append(f"- FAIL: {m}")
        for m in r.passes:
            lines.append(f"- ok: {m}")
        lines.append("")
    lines.append("_Mechanical gate only. Judgment checks (artifact scan, "
                 "slop test, brand feel, positioning) are run by a human "
                 "per asset._")

    report_dir = Path("reports")
    report_dir.mkdir(exist_ok=True)
    report_path = report_dir / "qa_report.md"
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    for r in results:
        status = "PASS" if r.passed else "FAIL"
        print(f"[{status}] {r.asset_id}"
              + ("" if r.passed else f" — {len(r.failures)} failure(s)"))
        for m in r.failures:
            print(f"    FAIL: {m}")
    print(f"\nReport: {report_path}")
    if failed:
        print(f"{len(failed)} asset(s) failing. No asset ships with an "
              "open failure.")
        return 1
    print("All assets pass the mechanical gate. Run the human judgment "
          "checks before publishing.")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest", help="path to qa_manifest.json")
    ap.add_argument("--claims", help="path to claims.json (overrides "
                                     "manifest's claims_file)")
    args = ap.parse_args(argv)
    return run(Path(args.manifest),
               Path(args.claims) if args.claims else None)


if __name__ == "__main__":
    raise SystemExit(main())
