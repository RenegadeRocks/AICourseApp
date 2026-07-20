"""Append-only per-run/per-stage checkpoint store with resume logic.

A checkpoint is durable state written between stages so a re-run RESUMES instead
of restarting. Critical for unattended pipelines because (a) runs fail partway,
(b) LLM stages are non-idempotent so re-running them changes the output and
re-pays, and (c) checkpoints are the audit trail for postmortems.

See 04-thu-hybrid-agent-design-pipeline-plus-judgment.md, Layer 2.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class CheckpointStore:
    def __init__(self, base: str, run_date: str):
        self.dir = Path(base) / run_date
        self.dir.mkdir(parents=True, exist_ok=True)

    def _path(self, stage_file: str) -> Path:
        return self.dir / stage_file

    def has(self, stage_file: str) -> bool:
        """True if a stage's checkpoint exists AND parses — a truncated write
        from a crash mid-flush must not be treated as valid."""
        p = self._path(stage_file)
        if not p.exists():
            return False
        try:
            json.loads(p.read_text())
            return True
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False

    def load(self, stage_file: str) -> Any:
        return json.loads(self._path(stage_file).read_text())

    def save(self, stage_file: str, data: Any) -> None:
        """Atomic write: temp file then rename, so a crash never leaves a
        half-written checkpoint that `has()` would accept."""
        p = self._path(stage_file)
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        tmp.replace(p)

    def save_text(self, stage_file: str, text: str) -> None:
        p = self._path(stage_file)
        tmp = p.with_suffix(p.suffix + ".tmp")
        tmp.write_text(text)
        tmp.replace(p)

    def run_or_resume(self, stage_file: str, fn, *, resume: bool):
        """Return the checkpointed output if resuming and it exists+validates;
        otherwise run `fn`, checkpoint its result, and return it.

        This is the whole resume story: judgment stages are reused on resume
        rather than re-invoked, which is both correctness (stable output) and
        cost (no double-pay) at once.
        """
        if resume and self.has(stage_file):
            return self.load(stage_file)
        result = fn()
        self.save(stage_file, result)
        return result
