"""Stage 1 — Fetch. RSS-first, polite, conditional requests.

Honors the Wednesday scraping policy (03-wed): prefer the front door (RSS/API),
send a truthful User-Agent naming the bot + a contact URL, use conditional
requests so you don't re-fetch unchanged pages (Cloudflare measured >50% of AI
crawl traffic as wasteful re-fetches). Fetch failures classify TRANSIENT vs
PERMANENT per common/schema.py.
"""
from __future__ import annotations

import time
from typing import Any

import feedparser
import httpx

from common.schema import TransientError, PermanentError, classify_http_status

DEFAULT_UA = "niche-brief-bot/1.0 (+{contact})"


def fetch_source(source: dict, etag_cache: dict[str, str]) -> dict[str, Any]:
    """Return {name, access, status, items_raw|html, etag}. Raises TransientError
    / PermanentError so the orchestrator can retry or skip+alert."""
    name = source["name"]
    access = source["access"]
    url = source["url"]
    contact = source.get("contact_url", "https://example.invalid/bot")
    ua = DEFAULT_UA.format(contact=contact)

    if access == "rss":
        # feedparser handles conditional requests via etag/modified.
        parsed = feedparser.parse(url, etag=etag_cache.get(url), agent=ua)
        status = getattr(parsed, "status", 200)
        if status == 304:
            return {"name": name, "access": access, "status": 304, "items_raw": [], "etag": etag_cache.get(url)}
        if status >= 400:
            classify_http_status(status)  # raises
        return {
            "name": name,
            "access": access,
            "status": status,
            "items_raw": [dict(e) for e in parsed.entries],
            "etag": getattr(parsed, "etag", None),
        }

    if access in ("html", "api"):
        headers = {"User-Agent": ua}
        if url in etag_cache:
            headers["If-None-Match"] = etag_cache[url]
        try:
            resp = httpx.get(url, headers=headers, timeout=20.0, follow_redirects=True)
        except (httpx.TimeoutException, httpx.ConnectError) as e:
            raise TransientError(f"TRANSIENT: {name} connection/timeout — {e}")
        if resp.status_code == 304:
            return {"name": name, "access": access, "status": 304, "html": None, "etag": etag_cache.get(url)}
        if resp.status_code >= 400:
            classify_http_status(resp.status_code)  # raises
        return {
            "name": name,
            "access": access,
            "status": resp.status_code,
            "html": resp.text,
            "etag": resp.headers.get("ETag"),
        }

    if access == "firecrawl":
        # Optional: use firecrawl-py with change-tracking here. Left as a wiring
        # exercise; see README env var FIRECRAWL_API_KEY.
        raise PermanentError(
            f"PERMANENT: firecrawl access for {name} not wired — see README"
        )

    raise PermanentError(f"PERMANENT: unknown access mode '{access}' for {name}")


def fetch_all(sources: list[dict], etag_cache: dict[str, str], polite_delay: float = 1.0,
              retryer=None):
    """Fetch each source politely (jittered delay), collecting per-source results
    and per-source errors. A source that fails PERMANENT is skipped (its error
    recorded for the alert) so the run degrades to the sources that worked.

    TRANSIENT failures are retried PER SOURCE with backoff+jitter: pass the
    orchestrator's `transient_retry(cfg)` decorator as `retryer`. Retry must be
    per-source — decorating the whole batch would re-fetch sources that already
    succeeded. Only after retries exhaust is the source recorded as a TRANSIENT
    error and skipped for this run.

    Successful responses write their ETag back into `etag_cache` (keyed by URL)
    so the orchestrator can persist it and the next run's conditional requests
    actually get 304s.
    """
    fetch_one = retryer(fetch_source) if retryer else fetch_source
    results, errors = [], []
    for src in sources:
        try:
            res = fetch_one(src, etag_cache)
            results.append(res)
            if res.get("etag"):
                etag_cache[src["url"]] = res["etag"]
        except PermanentError as e:
            errors.append({"source": src["name"], "class": "PERMANENT", "detail": str(e)})
        except TransientError as e:
            # Retries (if any) are already exhausted at this point; record and
            # degrade to the sources that worked.
            errors.append({"source": src["name"], "class": "TRANSIENT", "detail": str(e)})
        time.sleep(polite_delay)  # be a good guest; jitter this in production
    return {"results": results, "errors": errors}
