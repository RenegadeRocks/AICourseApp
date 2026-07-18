# Code-lab 06 — Hybrid scraper + summarizer

Companion to `06-sat-build-the-hybrid-scraper-summarizer.md`. A monitored,
scheduled agent that fetches your niche's sources (RSS-first, politely),
extracts a uniform `Item` schema, dedups, judges relevance (cheap tier),
synthesizes a **cited** daily brief (Sonnet-5-class), validates the brief as a
hard contract, delivers it, and writes metrics + heartbeat with failure alerts.
Plus a golden-set eval harness that **gates** prompt/model changes.

This is a *reference implementation you finish with Claude Code*, not a
paste-and-run product. The stage boundaries, checkpoint/resume, TRANSIENT/
PERMANENT retry classification, and eval gate are all here in skeleton form with
the load-bearing logic written; the source-specific extraction and the delivery
channel are yours to wire. Read the Saturday lesson's Layer 4 for the exact
Claude Code build prompts.

## Why it's shaped this way

- **Deterministic spine, two judgment islands** (relevance, synthesis) — see
  `04-thu-hybrid-agent-design-pipeline-plus-judgment.md`.
- **Checkpoint per stage** so a re-run resumes instead of restarting and never
  re-pays for (non-idempotent) LLM stages.
- **Every write is idempotent**; every fallible stage classifies failures
  TRANSIENT (backoff+jitter) vs PERMANENT (skip/alert, no retry).
- **Only validated briefs ship.** The validator is deterministic code; a brief
  that fabricates a source or fails faithfulness is a PERMANENT failure that
  alerts, not delivers.

## Setup

```bash
cd code-lab/06-hybrid-agent
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip freeze > requirements.lock                       # pin your actual solve
cp config.example.yaml config.yaml                   # then edit sources/schedule/budget
```

Environment variables (never commit keys — `.env` is gitignored):

| Var | Required | Purpose |
|---|---|---|
| `ANTHROPIC_API_KEY` | yes | synthesis + judging |
| `ANTHROPIC_SYNTH_MODEL` | no | synthesis model (default `claude-sonnet-5`; verify the current ID on the pricing docs before a long run) |
| `ANTHROPIC_JUDGE_MODEL` | no | relevance + faithfulness judge (default a Haiku-class tier; PIN it) |
| `PIPELINE_ENABLED` | no | kill switch — set `false` to make every run log-and-exit |
| `ALERT_WEBHOOK` | no | Slack/Discord/email-relay URL for failure alerts (stub logs if unset) |
| `FIRECRAWL_API_KEY` | no | enables the Firecrawl fetch/extract path for hard sources |

## Data & output layout

```
code-lab/06-hybrid-agent/
  config.yaml            # your sources, schedule, budget (you create from example)
  pipeline.py            # orchestrator: runs stages with checkpoint/resume
  stages/
    fetch.py             # stage 1 — RSS-first, polite, conditional requests
    extract.py           # stage 2 — uniform Item schema via structured outputs
    dedup.py             # stage 3 — content-hash + near-dup threshold
    judge.py             # stage 4 — relevance (cheap tier, structured output)
    synthesize.py        # stage 5 — cited brief, kept-items only
    validate.py          # stage 6 — deterministic contract + faithfulness gate
    deliver.py           # stage 7 — idempotent delivery (file/email/webhook)
    monitor.py           # stage 8 — heartbeat, metrics, alerts
  common/
    schema.py            # Item + brief JSON schemas, TRANSIENT/PERMANENT errors
    checkpoint.py        # append-only per-run/per-stage store, resume logic
    budget.py            # per-stage token caps + per-run dollar ceiling
  eval/
    run.py               # `python -m eval.run --gate` — ship gate
    rubric.py            # binary synthesis rubric + faithfulness judge
    golden_relevance.example.jsonl
  runs/                  # created at runtime; gitignored
  .env                   # your keys; gitignored
```

## Commands

```bash
# one manual run (writes runs/<date>/, delivers per config)
python pipeline.py --config config.yaml

# resume a crashed run without re-fetching/re-judging
python pipeline.py --config config.yaml --resume 2026-07-11

# shadow mode: produce the brief, deliver only to yourself
python pipeline.py --config config.yaml --shadow

# the eval gate — non-zero exit blocks a ship
python -m eval.run --gate --config config.yaml

# validate your judge against your own labels before trusting it
python -m eval.run --validate-judge eval/golden_relevance.jsonl

# read the last run's metrics and fire any due alerts
python -m stages.monitor --check runs/2026-07-11/run.log
```

## Stages

| Stage | Type | Checkpoint | Failure classes |
|---|---|---|---|
| 1 fetch | deterministic | `01-fetch.json` | 5xx/timeout/429 = TRANSIENT; 403/paywall/ToS = PERMANENT (skip source) |
| 2 extract | det. / judgment | `02-items.json` | malformed source = PERMANENT (quarantine item); zero-from-productive = drift alert |
| 3 dedup | deterministic | `03-deduped.json` | — |
| 4 relevance | judgment (cheap) | `04-judged.json` | model overload = TRANSIENT; reused on resume, never re-judged |
| 5 synthesize | judgment (Sonnet) | `05-brief.md/.json` | overload = TRANSIENT; reused on resume |
| 6 validate | deterministic | `06-validation.json` | contract/faithfulness fail = PERMANENT (alert, no ship) |
| 7 deliver | deterministic | `07-delivery.json` | idempotent by brief date/ID; send-fail = TRANSIENT (bounded) |
| 8 monitor | deterministic | `run.log` | absence-of-heartbeat is itself an alert |

## The eval gate (read before trusting any brief)

`eval/rubric.py` is binary-per-criterion (Hamel's discipline): cited claims,
no fabricated sources, sections present, length in bounds, no duplicated items,
faithfulness ≥ threshold. `eval/run.py --gate` runs the relevance golden set and
the synthesis rubric against frozen snapshots and **exits non-zero if anything
fails at threshold** — wire it into your change process so no prompt/model change
ships without a green gate. Your day-one golden set is a hypothesis; rebuild it
after a week of shadow runs from failures you actually observed.

**Validate the judge first.** An unvalidated LLM judge is a second unreviewed
model, not oversight. `--validate-judge` compares judge output to your hand
labels; clear your threshold (e.g. ≥90% agreement) before you gate on it.

## Costs

At Sonnet-5 intro pricing ($2/$10 per Mtok through 2026-08-31; then $3/$15),
a 5-source / ~40-item daily run is on the order of $0.45 (~$0.68 after Aug 31)
plus ~$5/mo infra. The pipeline prints a per-run token/dollar estimate and
enforces `config.yaml`'s `budget.run_dollar_ceiling` with a controlled stop.
Measure real token counts from the checkpoints and put them in your client's
cost table — at post-August prices, not intro ones.

## Going live safely

1. **Shadow** (`--shadow`) for several days; read every brief; log what's wrong.
2. **Canary** — deliver to you + a couple of tolerant users.
3. **Full** — only after clean days and a golden set rebuilt from real failures.
4. Document the schedule (cron/systemd timer) in this README — **do not commit a
   live crontab**. Local cron stops when the machine sleeps; graduate to a VPS +
   systemd timer, a managed cron, or Claude Code Routines (if all sources are
   connector-reachable) for durable operation.
5. The kill switch (`PIPELINE_ENABLED=false`) is line one of your incident
   runbook. Know where it is before the first scheduled run.

## Notes

- Honors your Wednesday scraping policy: RSS/API first, truthful User-Agent with
  contact URL, conditional requests, robots.txt respected, sources that block =
  handled PERMANENT events, not crashes.
- Nothing persists outside `runs/` and your configured delivery target.
- This is a teaching implementation. The judgment stages read the local
  checkpoint store directly; wrapping the finished pipeline as an MCP server
  (query briefs conversationally) is a documented stretch goal, not required.
