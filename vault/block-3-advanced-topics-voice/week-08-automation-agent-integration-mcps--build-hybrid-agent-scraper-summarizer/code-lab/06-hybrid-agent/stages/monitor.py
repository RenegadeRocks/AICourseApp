"""Stage 8 — Record + alert. Makes silence loud.

Heartbeat + per-run metrics to run.log; a checker that alerts on the failures an
unwatched pipeline dies from: a run that silently stopped (absence of heartbeat),
a source that went quiet (layout drift), a keep-rate/cost anomaly, a contract
failure. See 05-fri Layer 3. An alert to a channel nobody reads is a log line —
route ALERT_WEBHOOK somewhere you actually look.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path


def write_run_log(run_dir: Path, metrics: dict) -> None:
    metrics["heartbeat_ts"] = time.time()
    (run_dir / "run.log").write_text(json.dumps(metrics, indent=2))


def send_alert(message: str) -> None:
    """Fire an alert. Falls back to stderr if no webhook configured — but a
    stderr alert in an unattended cron job is nobody's alert, so wire the
    webhook before going live."""
    url = os.environ.get("ALERT_WEBHOOK")
    if not url:
        print(f"[ALERT] {message}", file=sys.stderr)
        return
    try:
        import httpx
        httpx.post(url, json={"text": f":rotating_light: {message}"}, timeout=10.0)
    except Exception as e:  # never let alerting crash the pipeline
        print(f"[ALERT-FAILED] {message} ({e})", file=sys.stderr)


def check_metrics(metrics: dict, sources_cfg: list[dict], history: dict | None = None) -> list[str]:
    """Return a list of alert strings. `history` is optional prior-run metrics
    for keep-rate / cost anomaly comparison."""
    alerts = []

    # Zero-from-productive-source (layout drift, not a quiet day).
    expected = {s["name"]: s.get("expected_min_items", 1) for s in sources_cfg}
    for name, count in metrics.get("items_per_source", {}).items():
        if count == 0 and expected.get(name, 1) > 0:
            alerts.append(f"source '{name}' returned 0 items (expected >= {expected.get(name)}): likely layout drift")

    # Contract failures.
    if metrics.get("contract_failed"):
        alerts.append(f"brief FAILED contract/faithfulness and was not delivered: {metrics.get('contract_detail')}")

    # Cost anomaly (per-run ceiling breach or rolling spike).
    if metrics.get("budget_exceeded"):
        alerts.append(f"run hit its dollar ceiling and stopped: {metrics.get('spent_usd')}")

    if history:
        prev_keep = history.get("keep_rate")
        cur_keep = metrics.get("keep_rate")
        if prev_keep is not None and cur_keep is not None and abs(cur_keep - prev_keep) > 0.3:
            alerts.append(f"keep-rate shifted {prev_keep:.2f} -> {cur_keep:.2f}: content or model drift")

    return alerts


def check_heartbeat(run_dir: Path, max_age_seconds: int = 90000) -> list[str]:
    """Absence-of-heartbeat is itself an alert — catches the run that never
    happened (cron died, machine slept, token expired)."""
    log = run_dir / "run.log"
    if not log.exists():
        return [f"no run.log in {run_dir}: run may not have happened at all"]
    m = json.loads(log.read_text())
    age = time.time() - m.get("heartbeat_ts", 0)
    if age > max_age_seconds:
        return [f"heartbeat is {int(age)}s old (> {max_age_seconds}s): pipeline may be stalled"]
    return []


if __name__ == "__main__":
    # `python -m stages.monitor --check runs/<date>/run.log`
    if len(sys.argv) >= 3 and sys.argv[1] == "--check":
        run_dir = Path(sys.argv[2]).parent
        for a in check_heartbeat(run_dir):
            send_alert(a)
