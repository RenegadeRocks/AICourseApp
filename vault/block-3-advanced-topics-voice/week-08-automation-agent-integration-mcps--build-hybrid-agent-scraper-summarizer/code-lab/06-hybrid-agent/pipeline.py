"""Orchestrator — runs the eight stages with checkpoint/resume, TRANSIENT retry,
budget enforcement, and monitoring. This is the deterministic spine that decides
WHETHER runs happen and in what order; the model only acts INSIDE stages 4 and 5.

Usage:
  python pipeline.py --config config.yaml            # one run today
  python pipeline.py --config config.yaml --resume 2026-07-11
  python pipeline.py --config config.yaml --shadow   # deliver only to yourself

Kill switch: PIPELINE_ENABLED=false makes every run log-and-exit (05-fri L5).
"""
from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path

import yaml
from dotenv import load_dotenv
from tenacity import retry, stop_after_attempt, wait_exponential_jitter, retry_if_exception_type

from common.schema import TransientError, PermanentError
from common.checkpoint import CheckpointStore
from common.budget import RunBudget, BudgetExceeded
from stages import fetch, extract, dedup, judge, synthesize, validate, deliver, monitor

load_dotenv()


def _client():
    """Lazily construct the Anthropic client so `--help` and eval-only paths
    don't require a key."""
    from anthropic import Anthropic
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


def transient_retry(cfg):
    """Retry decorator for TRANSIENT-classified failures only. PERMANENT errors
    propagate immediately — retrying them wastes tokens and can get you blocked."""
    return retry(
        retry=retry_if_exception_type(TransientError),
        stop=stop_after_attempt(cfg["reliability"]["max_retries"]),
        wait=wait_exponential_jitter(initial=cfg["reliability"]["backoff_base_seconds"], max=60),
        reraise=True,
    )


def run(config_path: str, resume_date: str | None = None, shadow: bool = False) -> dict:
    cfg = yaml.safe_load(Path(config_path).read_text())

    # --- Kill switch, checked at the top of every run ----------------------
    if os.environ.get("PIPELINE_ENABLED", "true").lower() == "false":
        print("PIPELINE_ENABLED=false — kill switch active, exiting cleanly.")
        return {"status": "disabled"}

    date = resume_date or dt.date.today().isoformat()
    resume = resume_date is not None
    store = CheckpointStore("runs", date)
    run_dir = Path("runs") / date
    budget = RunBudget(
        dollar_ceiling=cfg["budget"]["run_dollar_ceiling"],
        per_stage_token_cap=cfg["budget"].get("per_stage_token_cap", {}),
    )
    niche = cfg["niche"]["description"]
    metrics: dict = {"date": date, "shadow": shadow}
    client = None  # constructed on first stage that needs it

    try:
        # Stage 1 — fetch (deterministic; TRANSIENT retried, PERMANENT skips source)
        @transient_retry(cfg)
        def _fetch():
            return fetch.fetch_all(cfg["sources"], etag_cache={})
        fetched = store.run_or_resume("01-fetch.json", _fetch, resume=resume)

        # Stage 2 — extract (each source -> Item schema)
        def _extract():
            nonlocal client
            all_items = []
            for res in fetched["results"]:
                src_cfg = next(s for s in cfg["sources"] if s["name"] == res["name"])
                if src_cfg.get("item_selector") is None and res["access"] in ("html", "api"):
                    client = client or _client()
                all_items.extend(extract.extract(res, src_cfg, client, cfg["budget"]["synth_model"]))
            return all_items
        items = store.run_or_resume("02-items.json", _extract, resume=resume)
        # Seed every configured source at 0 so the zero-from-productive-source
        # drift alert (stages/monitor.py) can actually fire — a source that
        # yielded nothing must appear in the counts, not be absent from them.
        metrics["items_per_source"] = _count_by_source(items, cfg["sources"])

        # Stage 3 — dedup (deterministic)
        deduped = store.run_or_resume("03-deduped.json", lambda: dedup.dedup(items), resume=resume)
        kept_pool = deduped["kept"]

        # Stage 4 — relevance judge (judgment; REUSED on resume, never re-judged)
        client = client or _client()

        @transient_retry(cfg)
        def _judge():
            return judge.judge_all(client, cfg["budget"]["judge_model"], niche,
                                   kept_pool, cfg["niche"]["relevance_threshold"],
                                   budget=budget)
        judged = store.run_or_resume("04-judged.json", _judge, resume=resume)
        kept = [it for it in judged if it.get("keep")]
        metrics["keep_rate"] = round(len(kept) / max(len(judged), 1), 3)

        # Stage 5 — synthesize (judgment; REUSED on resume)
        @transient_retry(cfg)
        def _synth():
            return {"brief": synthesize.synthesize(client, cfg["budget"]["synth_model"], niche, kept, date, budget=budget)}
        brief_md = store.run_or_resume("05-brief.json", _synth, resume=resume)["brief"]
        store.save_text("05-brief.md", brief_md)

        # Stage 6 — validate contract (deterministic gate; PERMANENT if it fails)
        try:
            vresult = validate.validate(brief_md, kept, client, cfg["budget"]["judge_model"])
            store.save("06-validation.json", vresult)
        except PermanentError as e:
            metrics["contract_failed"] = True
            metrics["contract_detail"] = str(e)
            raise

        # Stage 7 — deliver (idempotent; shadow overrides recipients to you)
        delivery_cfg = dict(cfg["delivery"])
        if shadow:
            delivery_cfg = {"mode": "file", "file_path": f"runs/{date}/shadow-brief.md"}
        dresult = deliver.deliver(brief_md, brief_id=date, delivery_cfg=delivery_cfg, run_dir=run_dir)
        store.save("07-delivery.json", dresult)
        metrics["delivery"] = dresult["status"]

    except BudgetExceeded as e:
        metrics["budget_exceeded"] = True
        metrics.update(budget.summary())
        monitor.send_alert(f"[{date}] budget stop: {e}")
    except PermanentError as e:
        monitor.send_alert(f"[{date}] PERMANENT failure: {e}")
    finally:
        # Stage 8 — always record + alert, even (especially) on failure paths
        metrics.update(budget.summary())
        monitor.write_run_log(run_dir, metrics)
        for a in monitor.check_metrics(metrics, cfg["sources"]):
            monitor.send_alert(f"[{date}] {a}")

    return metrics


def _count_by_source(items: list[dict], sources_cfg: list[dict]) -> dict:
    out: dict[str, int] = {s["name"]: 0 for s in sources_cfg}
    for it in items:
        out[it["source"]] = out.get(it["source"], 0) + 1
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--config", default="config.yaml")
    ap.add_argument("--resume", default=None, help="run date to resume, e.g. 2026-07-11")
    ap.add_argument("--shadow", action="store_true", help="deliver only to yourself")
    args = ap.parse_args()
    result = run(args.config, args.resume, args.shadow)
    print(result)
