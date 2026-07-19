# Week 15 code-lab — the launch runner

Two small, dependency-free tools that turn Saturday's launch plan from a vibe
into something a stranger could execute on a date:

1. **`checklist.py`** — a dated launch-checklist runner. Loads your plan,
   prints a GO / NO-GO report, and *fails* (non-zero exit) if any blocking item
   is incomplete. This is the pass-bar gate: no blocking item open → no launch.
2. **`personalizer.py`** — a **compliant** outreach-sequence personalizer. It
   renders a 3-touch sequence for each prospect, runs every draft through the
   compliance gates in `compliance.py`, and writes passing drafts to `./drafts/`
   marked **FOR HUMAN REVIEW — DO NOT SEND**. It never sends. The `--send` flag
   exists only to refuse and explain why.

The design encodes the week's thesis: **use AI for research and
drafting-for-review, never for blast-send** (see `04-thu`), and **never ask for
upvotes or automate outreach** (see `02-tue`, `04-thu`). The tools make the
compliant motion the path of least resistance.

## Requirements

Python 3.10+. No third-party packages (standard library only). Nothing to
`pip install` — see `requirements.txt`.

## Run it

```bash
cd code-lab/06-launch-runner

# 1) Launch readiness — expect a NO-GO on the sample (some blocking items are
#    intentionally not done). Exit code is 1 when blocking items are open.
python checklist.py --plan launch_plan.sample.json

# only the launch-day phase
python checklist.py --plan launch_plan.sample.json --phase launch-day

# machine-readable
python checklist.py --plan launch_plan.sample.json --json

# 2) Draft the outreach sequence (writes to ./drafts/, sends NOTHING).
python personalizer.py \
  --prospects prospects.sample.json \
  --template sequence_template.json \
  --config config.json

# draft only touch 1
python personalizer.py --prospects prospects.sample.json \
  --template sequence_template.json --config config.json --touch 1

# prove the tool refuses to send
python personalizer.py --prospects prospects.sample.json \
  --template sequence_template.json --config config.json --send   # exits 3, sends nothing
```

## What the sample is engineered to teach

The sample `prospects.sample.json` contains four prospects that exercise every
gate:

- **Priya (US, strong signal)** → drafts cleanly.
- **Tom (EU, strong signal)** → drafts only because `config.lia_documented` is
  `true`. Set it to `false` and Tom is **BLOCKED** (`GDPR_EU_NO_LIA`) — the tool
  refuses to draft EU outreach without a documented Legitimate Interest
  Assessment.
- **Dana (empty signal)** → **BLOCKED** (`NO_SIGNAL`). Precision over volume: a
  prospect with no real, specific reason to be contacted is cut, not templated.
- **Sam ("please upvote our launch…")** → **BLOCKED** (`UPVOTE_ASK`): the
  prospect *has* a signal string, so it renders into the draft, and the
  rendered-email gate catches the prohibited vote solicitation before any draft
  is written. Asking for votes is prohibited (`02-tue`).

Every draft carries the CAN-SPAM footer (physical address + opt-out) injected
from `config.json`; remove either and the config gate blocks the whole run.

## Pass bar (Saturday)

You have passed when:

1. `checklist.py` on **your own** launch plan returns **GO** (exit 0) — every
   blocking item genuinely done — for a real launch date.
2. `personalizer.py` drafts a clean 3-touch sequence for **your own** 20-prospect
   list, with **zero** `NO_SIGNAL` blocks (every prospect has a real signal) and
   zero `AI_TELL` warnings you did not consciously accept.
3. You open `./drafts/`, read every line, and can point to the specific human
   edit each draft still needs before a person could send it. If a draft looks
   send-ready without edits, your `{signal}` was generic — fix the list.

## Files

| File | Role |
|---|---|
| `checklist.py` | launch-readiness gate (GO/NO-GO, non-zero exit on NO-GO) |
| `personalizer.py` | compliant draft generator (never sends) |
| `compliance.py` | shared CAN-SPAM / GDPR / no-upvote / anti-slop gates |
| `config.json` | your sender identity, CAN-SPAM footer, LIA flag |
| `sequence_template.json` | the 3-touch template ({signal} is human-verified) |
| `prospects.sample.json` | four prospects that exercise every gate |
| `launch_plan.sample.json` | a dated, phased launch checklist |

## Extending it safely

If you wire an LLM into `personalizer.py` to draft the `{signal}` opener from
research, keep two invariants: (1) the output still goes to `./drafts/` for
human review, never to a sender; (2) `compliance.check_rendered_email` still
runs on every rendered draft. The moment a pipeline sends without a human
reading every word, you have built the slop machine the week warns against.
