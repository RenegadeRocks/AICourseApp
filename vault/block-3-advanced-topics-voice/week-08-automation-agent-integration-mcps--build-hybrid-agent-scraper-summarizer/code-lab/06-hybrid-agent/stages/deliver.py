"""Stage 7 — Deliver (deterministic). Holds the only write credential.

Idempotent by brief date/ID: a retry after a lost ack must not double-send
(02-tue). The content-reading models never touched this credential — privilege
separation breaks the trifecta by construction (02-tue L5).
"""
from __future__ import annotations

import os
from pathlib import Path


def _already_delivered(marker: Path) -> bool:
    return marker.exists()


def deliver(brief_md: str, brief_id: str, delivery_cfg: dict, run_dir: Path) -> dict:
    """Deliver once. `brief_id` (e.g. the run date) is the idempotency key."""
    marker = run_dir / "07-delivery.json"
    if _already_delivered(marker):
        return {"status": "skipped", "reason": "already delivered (idempotent)", "brief_id": brief_id}

    mode = delivery_cfg.get("mode", "file")

    if mode == "file":
        out = Path(delivery_cfg["file_path"])
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(brief_md)
        return {"status": "delivered", "mode": "file", "path": str(out), "brief_id": brief_id}

    if mode == "webhook":
        import httpx
        url = os.environ[delivery_cfg["webhook"]["url_env"]]
        resp = httpx.post(url, json={"text": brief_md}, timeout=15.0)
        resp.raise_for_status()  # send-fail is TRANSIENT; orchestrator bounds retries
        return {"status": "delivered", "mode": "webhook", "brief_id": brief_id}

    if mode == "email":
        # Wire smtplib here using delivery_cfg['email']; keys/credentials from env.
        # Left as a wiring exercise — see README. Must remain idempotent.
        raise NotImplementedError("wire SMTP delivery; keep it idempotent by brief_id")

    raise ValueError(f"unknown delivery mode '{mode}'")
