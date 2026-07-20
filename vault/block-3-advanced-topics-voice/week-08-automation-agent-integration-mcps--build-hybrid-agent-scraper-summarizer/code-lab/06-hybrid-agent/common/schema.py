"""Shared schemas and the TRANSIENT/PERMANENT error convention.

Every stage produces output conforming to a schema here, and every fallible
stage raises TransientError (retry with backoff) or PermanentError (skip/alert,
never retry the same input). This convention is taught in
02-tue-building-an-mcp-server.md and made load-bearing in
04-thu-hybrid-agent-design-pipeline-plus-judgment.md.
"""
from __future__ import annotations

import hashlib
import re


class PipelineError(Exception):
    """Base for classified pipeline failures."""


class TransientError(PipelineError):
    """5xx, timeout, 429, model overload — a second attempt might fix it.

    Retried with capped exponential backoff + jitter.
    """


class PermanentError(PipelineError):
    """4xx (except 429), auth failure, schema violation, ToS block, contract
    rejection — retrying the same input cannot help. Log, alert, degrade.
    """


# JSON Schema for one extracted item. Every source populates THIS shape so that
# dedup, judging, and synthesis stay source-agnostic. Fed to the Claude API as
# `output_format` so extraction output is grammar-guaranteed to conform.
ITEM_SCHEMA = {
    "type": "object",
    "properties": {
        "title": {"type": "string"},
        "url": {"type": "string"},
        "source": {"type": "string"},
        "published_at": {"type": ["string", "null"]},  # ISO 8601 or null
        "summary": {"type": "string"},
        "topics": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["title", "url", "source", "summary", "topics"],
    "additionalProperties": False,
}

# Relevance judge output schema (stage 4). Cheap tier, structured output.
JUDGMENT_SCHEMA = {
    "type": "object",
    "properties": {
        "keep": {"type": "boolean"},
        "score": {"type": "number"},           # 0..1
        "reason": {"type": "string"},
    },
    "required": ["keep", "score", "reason"],
    "additionalProperties": False,
}


def content_hash(url: str, title: str) -> str:
    """Stable identity for an item, shared by dedup and idempotent writes.

    Normalizes title (lowercase, collapse whitespace, strip punctuation) so
    trivial variants hash together. A re-run recognizes what it already saw.
    """
    norm_title = re.sub(r"[^\w\s]", "", title.lower())
    norm_title = re.sub(r"\s+", " ", norm_title).strip()
    key = f"{url.strip()}::{norm_title}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:16]


def classify_http_status(status: int) -> None:
    """Raise the right error class for an HTTP status. 429 is TRANSIENT (respect
    Retry-After upstream); other 4xx are PERMANENT; 5xx are TRANSIENT.
    """
    if status == 429 or 500 <= status < 600:
        raise TransientError(f"TRANSIENT: HTTP {status} — retry with backoff")
    if 400 <= status < 500:
        raise PermanentError(
            f"PERMANENT: HTTP {status} — do not retry; skip source and alert"
        )
