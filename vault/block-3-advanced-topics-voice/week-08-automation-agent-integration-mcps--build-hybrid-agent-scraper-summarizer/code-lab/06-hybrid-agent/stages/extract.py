"""Stage 2 — Extract. Every source -> the SAME Item schema.

Ladder (cheapest first, 03-wed Layer 5): RSS/API returns structured data (parse,
don't extract); stable HTML -> typed selectors; irregular prose -> schema-
constrained LLM extraction via the Claude API `output_format`, which GUARANTEES
conformant JSON (no almost-JSON-at-3am failures). A source yielding zero items
where it usually yields many is a drift signal surfaced to the monitor.
"""
from __future__ import annotations

from typing import Any

from selectolax.parser import HTMLParser

from common.schema import ITEM_SCHEMA, PermanentError


def _item(title, url, source, summary, published_at=None, topics=None) -> dict:
    return {
        "title": (title or "").strip(),
        "url": (url or "").strip(),
        "source": source,
        "published_at": published_at,
        "summary": (summary or "").strip(),
        "topics": topics or [],
    }


def extract_rss(fetched: dict) -> list[dict]:
    """RSS entries are already structured — parse into Item shape, no LLM."""
    out = []
    for e in fetched.get("items_raw", []):
        out.append(_item(
            title=e.get("title"),
            url=e.get("link"),
            source=fetched["name"],
            summary=e.get("summary") or e.get("description") or "",
            published_at=e.get("published") or e.get("updated"),
            topics=[t.get("term") for t in e.get("tags", []) if t.get("term")],
        ))
    return out


def extract_html_selectors(fetched: dict, item_selector: str) -> list[dict]:
    """Stable HTML -> typed selectors. Deterministic and cheap. Fill-rate on
    key fields is a drift signal (Thursday); the monitor watches it."""
    html = fetched.get("html")
    if not html:
        return []
    tree = HTMLParser(html)
    out = []
    for node in tree.css(item_selector):
        a = node.css_first("a")
        title = node.css_first("h1, h2, h3, .title")
        out.append(_item(
            title=title.text() if title else (a.text() if a else ""),
            url=a.attributes.get("href") if a else "",
            source=fetched["name"],
            summary=(node.css_first("p").text() if node.css_first("p") else ""),
        ))
    return out


def extract_prose_llm(client, model: str, text: str, source: str) -> list[dict]:
    """Irregular prose -> schema-constrained extraction. `output_format` makes
    the model's JSON grammar-guaranteed to match ITEM_SCHEMA (wrapped as an
    array). Cache-friendly: the compiled schema is cached ~24h by the API.

    Pseudocode-precise against the Anthropic SDK; verify param names against the
    current SDK before running (see README). Kept minimal on purpose.
    """
    resp = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{
            "role": "user",
            "content": (
                f"Extract news items from this content from source '{source}'. "
                f"Return a JSON array of items.\n\n{text[:20000]}"
            ),
        }],
        # output_format enforces the schema. Shape per Claude structured-outputs
        # docs; an array-of-items schema wraps ITEM_SCHEMA.
        output_format={
            "type": "json_schema",
            "schema": {"type": "array", "items": ITEM_SCHEMA},
        },
    )
    import json
    try:
        items = json.loads(resp.content[0].text)
    except (json.JSONDecodeError, IndexError) as e:
        # With output_format this should not happen; if it does it's a hard fault.
        raise PermanentError(f"PERMANENT: extraction returned non-conformant JSON — {e}")
    for it in items:
        it["source"] = source
    return items


def extract(fetched: dict, source_cfg: dict, client=None, model: str = "") -> list[dict]:
    access = fetched["access"]
    if fetched.get("status") == 304:
        return []  # not modified since last fetch — nothing new, not an error
    if access == "rss":
        return extract_rss(fetched)
    if access in ("html", "api"):
        sel = source_cfg.get("item_selector")
        if sel:
            return extract_html_selectors(fetched, sel)
        if client:  # fall back to LLM extraction over the raw HTML/text
            return extract_prose_llm(client, model, fetched.get("html", ""), fetched["name"])
        raise PermanentError(
            f"PERMANENT: {fetched['name']} needs item_selector or an LLM client"
        )
    raise PermanentError(f"PERMANENT: cannot extract access mode '{access}'")
