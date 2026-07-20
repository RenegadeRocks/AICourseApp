# Code-lab 06 — Launch-kit brief generator + asset-QA checklist runner

Companion to `06-sat-build-the-launch-kit.md`. Two small, dependency-free
Python tools that operationalize Thursday's creative pipeline:

- **`brief_generator.py`** — reads your launch-kit config (`launch_kit.json`:
  package facts, brand spec, positioning stance, asset requests) and emits one
  markdown **creative brief per asset** into `briefs/`. Each brief carries the
  brand constraints, drafted generation prompts, the predicted disclosure
  status, and the QA criteria the asset must later pass. Briefs are written
  *before* generation; that ordering is the pipeline's whole point.
- **`qa_runner.py`** — reads an asset manifest (`qa_manifest.json`) and runs
  Thursday's **mechanical QA gate** over the real files: dimensions (PNG/JPEG
  parsed with stdlib, no Pillow), file-size budgets, OG-image exactness
  (1200×630), alt text, archive-record completeness (prompt/tool/settings/
  license), AI-disclosure consistency, banned unsubstantiated-claim phrases,
  and a numeric-claims check against your substantiation file (`claims.json`).
  Exits non-zero if any asset fails: wire it into CI or a pre-publish hook.

The judgment half of the QA gate (artifact scan, slop test, brand-feel) stays
human on purpose; see the Saturday lesson's Layer 3.

## Setup

Python 3.10+. **No dependencies** (stdlib only) — `requirements.txt` is
intentionally empty. No API keys.

## Run the example end-to-end

```bash
cd code-lab/06-launch-kit
python make_fixtures.py            # generates sample PNG assets in example/assets/
python brief_generator.py example/launch_kit.json          # -> briefs/*.md
python qa_runner.py example/qa_manifest.json               # -> reports/qa_report.md, exit code
echo $?                            # 1: the example ships one deliberately failing asset
```

The example manifest includes one asset that fails on purpose (wrong OG
dimensions + an unsubstantiated "100% accurate" claim) so you can see the
report format. Fix it or remove it to see exit code 0.

## Adapt to your launch (Saturday, Milestone 2–3)

1. Copy `example/launch_kit.json` → `my/launch_kit.json`; replace package
   facts, palette, negative list, and the asset list with yours.
2. Generate briefs; take them to your Wednesday-selected tools; produce assets.
3. Copy `example/qa_manifest.json` → `my/qa_manifest.json`; point entries at
   your real files; fill the archive records honestly.
4. Put every substantiated claim (exact strings) in `my/claims.json` — this is
   Monday's substantiation file in machine-readable form.
5. `python qa_runner.py my/qa_manifest.json` until exit code 0. No asset ships
   with an open failure.

## Files

```
brief_generator.py     # config -> briefs/*.md
qa_runner.py           # manifest -> reports/qa_report.md + exit code
make_fixtures.py       # generates example PNG files (stdlib zlib/struct)
example/launch_kit.json
example/qa_manifest.json
example/claims.json
example/assets/        # copy files checked into repo; PNGs via make_fixtures.py
requirements.txt       # empty on purpose (stdlib only)
```
