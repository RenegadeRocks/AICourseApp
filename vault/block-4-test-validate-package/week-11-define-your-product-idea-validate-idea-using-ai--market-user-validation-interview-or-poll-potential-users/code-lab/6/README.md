# Code-lab 6 — evidence ledger + interview-note synthesizer

Two stdlib-only Python tools that operationalize the week's discipline:
pre-registered assumptions, for/against-tagged evidence atoms, class-weighted
scoring with `synthetic` fixed at weight 0.0, and a mechanical build/pivot/kill
verdict.

## Requirements

- Python 3.10+ (no third-party packages; `requirements.txt` is intentionally empty).
- Optional: the `claude` CLI on PATH for LLM-assisted atom extraction
  (`note_synthesizer.py` default mode). No API key needed on a machine with a
  Claude subscription. Without it, use `--offline`.

## Quickstart (5 minutes, uses the bundled sample)

```bash
cd code-lab/6

# 1. Pre-register: fresh ledger + assumptions with kill criteria.
python evidence_ledger.py init --ledger ledger.json
python evidence_ledger.py add-assumption --ledger ledger.json \
  --id A1 --category desirability \
  --text "Principals lose 30+ min/meeting to follow-up admin, recurring weekly" \
  --kill "fewer than 3 of 10 interviewees cite a specific recent instance"
python evidence_ledger.py add-assumption --ledger ledger.json \
  --id A2 --category viability \
  --text "2 of first 10 will start a paid pilot at >= \$200/month" \
  --kill "0 pilot acceptances after 10 currency-close conversations"

# Commit ledger.json NOW — the commit timestamp is your pre-registration receipt.

# 2. Synthesize the sample interview into tagged atoms (offline heuristic mode).
python note_synthesizer.py --ledger ledger.json --notes sample_interviews/ \
  --source-class stated --offline --out atoms.json

# 3. Import, then add one behavioral atom from your smoke test by hand.
python evidence_ledger.py import-atoms --ledger ledger.json --atoms atoms.json
python evidence_ledger.py add-evidence --ledger ledger.json \
  --assumption A2 --direction for --source-class behavioral --strength 4 \
  --quote "4 of 74 warm visitors submitted the pilot-request form at \$200/mo" \
  --source smoke-test-v1 --channel warm

# 4. Read the verdict + report; sanity-check a conversion rate.
python evidence_ledger.py verdict --ledger ledger.json
python evidence_ledger.py report  --ledger ledger.json > report.md
python evidence_ledger.py wilson --successes 4 --trials 74
```

## Real use (Claude mode)

```bash
# Extract atoms from your real transcripts with Claude as the auditor
# (prompt is anti-sycophantic: ambiguous statements tag AGAINST/NEUTRAL).
python note_synthesizer.py --ledger ledger.json --notes validation/interviews/ \
  --source-class stated --out atoms.json

# Synthetic panels are allowed in, but carry weight 0.0 by rule (Thursday):
python note_synthesizer.py --ledger ledger.json --notes validation/synthetic/ \
  --source-class synthetic --out synthetic_atoms.json

# Blind-audit a random sample of FOR atoms before trusting a tagging run:
python note_synthesizer.py --audit 5 --atoms atoms.json
```

## Design notes

- **Weights** live in `ledger.json` (`paid` 5.0, `behavioral` 3.0, `stated` 1.0,
  `desk` 0.5, `synthetic` 0.0). Edit them at init if you must; edits after
  evidence exists belong in `overrides` with a reason.
- **The verdict is advice with an audit trail.** You can overrule it; the tool
  records overrides so Sunday-you can see what Friday-you rationalized.
- **`--offline` mode is deliberately crude** (keyword heuristics, everything
  mapped to your first assumption). It exists so the pipeline runs anywhere and
  so the quality gap between careless and careful labeling is something you
  *experience*, not read about.
- No API keys are read or stored. Claude mode shells out to your local `claude`
  CLI exactly like the course app's chat route does.

## Files

| File | Purpose |
|---|---|
| `evidence_ledger.py` | Pre-registered ledger: assumptions, atoms, weights, verdict, report, Wilson helper |
| `note_synthesizer.py` | Transcript → tagged evidence atoms (Claude or offline mode), blind-audit sampler |
| `sample_interviews/P3.md` | Sample transcript (the Wednesday worked example) for the quickstart |
| `requirements.txt` | Empty on purpose: stdlib only |
