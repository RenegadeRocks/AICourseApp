#!/usr/bin/env python3
"""Build one EPUB 3 of every lesson in the vault, for Kindle (Send-to-Kindle).

Usage:
    python scripts/export_epub.py [--out exports/ai-pro-level-course.epub] [--block block-2]

Walks vault/, skipping underscore-prefixed files/dirs (archives, reviews,
refresh reports, pilot week). Structure: Block -> Week -> daily lessons.
EPUB 3 spec details: `mimetype` entry first and STORED; XHTML validated with
minidom before packaging; 1600x2560 cover.

Deps: markdown, Pillow (cover only — skipped gracefully if missing).
"""

from __future__ import annotations

import argparse
import html
import re
import sys
import uuid
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.dom import minidom

import markdown

ROOT = Path(__file__).resolve().parent.parent
VAULT = ROOT / "vault"

MD = markdown.Markdown(extensions=["extra", "sane_lists"], output_format="xhtml")

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
HTML_TAGS = {
    "a", "abbr", "b", "blockquote", "br", "code", "dd", "del", "div", "dl", "dt",
    "em", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "i", "img", "li", "nav", "ol",
    "p", "pre", "section", "span", "strong", "sub", "sup", "table", "tbody", "td",
    "th", "thead", "tr", "ul",
}
TAG_RE = re.compile(r"""<(/?)([a-zA-Z][a-zA-Z0-9-]*)((?:"[^"]*"|'[^']*'|[^>"'])*)(/?)>""")


def escape_pseudo_tags(body: str) -> str:
    # Prose placeholders like <city> or <example of X> read as tags to the XML
    # parser; escape anything that isn't a real XHTML tag.
    return TAG_RE.sub(
        lambda m: m.group(0) if m.group(2).lower() in HTML_TAGS else html.escape(m.group(0)),
        body,
    )
H1_RE = re.compile(r"^# (.+)$", re.MULTILINE)
WIKILINK_RE = re.compile(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]")

CSS = """
body { font-family: serif; line-height: 1.5; margin: 0 5%; }
h1, h2, h3 { font-family: sans-serif; line-height: 1.2; }
code { font-family: monospace; font-size: 0.9em; }
pre { white-space: pre-wrap; word-wrap: break-word; background: #f4f4f4;
      padding: 0.6em; font-size: 0.85em; }
table { border-collapse: collapse; font-size: 0.85em; }
th, td { border: 1px solid #999; padding: 0.3em 0.5em; }
blockquote { border-left: 3px solid #999; margin-left: 0; padding-left: 1em; }
.part-title { margin-top: 40%; text-align: center; }
.week-title { margin-top: 30%; text-align: center; }
"""


def prettify(slug: str) -> str:
    return re.sub(r"^\d+-", "", slug).replace("--", " / ").replace("-", " ").strip().title()


def lesson_title(text: str, path: Path) -> str:
    # Same fallback chain as the app: frontmatter title -> first H1 -> slug.
    fm = FRONTMATTER_RE.match(text)
    if fm:
        m = re.search(r"^title:\s*[\"']?(.+?)[\"']?\s*$", fm.group(1), re.MULTILINE)
        if m:
            return m.group(1)
    m = H1_RE.search(FRONTMATTER_RE.sub("", text))
    if m:
        return m.group(1).strip()
    return prettify(path.stem)


def collect(block_filter: str | None):
    """Return [(block_dir, [(week_dir, [lesson_path, ...]), ...]), ...]."""
    tree = []
    for block in sorted(VAULT.iterdir()):
        if not block.is_dir() or block.name.startswith("_") or block.name == "00-program":
            continue
        if block_filter and block.name != block_filter:
            continue
        weeks = []
        for week in sorted(block.iterdir()):
            if not week.is_dir() or week.name.startswith("_"):
                continue
            lessons = sorted(
                p for p in week.glob("*.md")
                if not p.name.startswith("_")
            )
            if lessons:
                weeks.append((week, lessons))
        if weeks:
            tree.append((block, weeks))
    return tree


def xhtml_page(title: str, body: str) -> str:
    doc = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops">\n'
        f"<head><title>{html.escape(title)}</title>"
        '<link rel="stylesheet" type="text/css" href="style.css"/></head>\n'
        f"<body>{body}</body>\n</html>\n"
    )
    minidom.parseString(doc)  # raises on invalid XML -> abort before packaging
    return doc


def convert_lesson(path: Path, href_map: dict[str, str]) -> tuple[str, str]:
    text = path.read_text(encoding="utf-8")
    title = lesson_title(text, path)
    text = FRONTMATTER_RE.sub("", text)

    def wikilink(m: re.Match) -> str:
        target = m.group(1).split("#")[0].strip()
        label = (m.group(2) or prettify(Path(target).stem)).strip()
        href = href_map.get(Path(target).stem)
        return f"[{label}]({href})" if href else f"*{label}*"

    text = WIKILINK_RE.sub(wikilink, text)
    MD.reset()
    body = MD.convert(text)
    # minidom chokes on bare & and named entities; markdown emits &amp; already,
    # but raw HTML passthrough in lessons may not. Fix the common offenders.
    body = re.sub(r"&(?!(?:[a-zA-Z]+|#\d+|#x[0-9a-fA-F]+);)", "&amp;", body)
    body = body.replace("&nbsp;", "&#160;")
    body = escape_pseudo_tags(body)
    return title, xhtml_page(title, body)


def make_cover(dest: Path) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        return False
    W, H = 1600, 2560
    img = Image.new("RGB", (W, H), (18, 24, 38))
    draw = ImageDraw.Draw(img)
    for i in range(H):  # subtle vertical gradient
        c = 18 + int(30 * i / H)
        draw.line([(0, i), (W, i)], fill=(c, c + 6, c + 20))
    font_dir = Path("/usr/share/fonts/truetype/dejavu")
    big = ImageFont.truetype(str(font_dir / "DejaVuSans-Bold.ttf"), 150)
    small = ImageFont.truetype(str(font_dir / "DejaVuSans.ttf"), 70)
    draw.line([(200, 700), (1400, 700)], fill=(212, 175, 55), width=8)
    for i, line in enumerate(["AI Pro-level", "Course"]):
        draw.text((W / 2, 950 + i * 210), line, font=big, fill=(240, 240, 240), anchor="mm")
    draw.line([(200, 1500), (1400, 1500)], fill=(212, 175, 55), width=8)
    draw.text((W / 2, 1700), "The Complete Lessons", font=small, fill=(200, 200, 205), anchor="mm")
    draw.text((W / 2, 2300), "Renegade Rocks", font=small, fill=(212, 175, 55), anchor="mm")
    img.save(dest, "PNG")
    return True


def build(out: Path, block_filter: str | None) -> None:
    tree = collect(block_filter)
    if not tree:
        sys.exit(f"no content found (block filter: {block_filter})")

    # Pass 1: assign hrefs so wikilinks can cross-reference chapters.
    href_map: dict[str, str] = {}
    chapters: list[tuple[str, Path, str]] = []  # (chapter_id, lesson_path, href)
    for bi, (block, weeks) in enumerate(tree):
        for wi, (week, lessons) in enumerate(weeks):
            for li, lesson in enumerate(lessons):
                cid = f"c{bi}_{wi}_{li}"
                href = f"{cid}.xhtml"
                href_map[lesson.stem] = href
                chapters.append((cid, lesson, href))

    # Pass 2: convert.
    docs: dict[str, str] = {}
    titles: dict[str, str] = {}
    for cid, lesson, href in chapters:
        title, doc = convert_lesson(lesson, href_map)
        docs[href] = doc
        titles[href] = title

    # Nav (nested Block -> Week -> Lesson) + part/week divider pages.
    nav_items, spine, extra_pages = [], [], {}
    for bi, (block, weeks) in enumerate(tree):
        bhref = f"part{bi}.xhtml"
        btitle = prettify(block.name)
        extra_pages[bhref] = xhtml_page(btitle, f'<h1 class="part-title">{html.escape(btitle)}</h1>')
        spine.append(bhref)
        week_lis = []
        for wi, (week, lessons) in enumerate(weeks):
            whref = f"part{bi}w{wi}.xhtml"
            wtitle = prettify(week.name)
            extra_pages[whref] = xhtml_page(wtitle, f'<h2 class="week-title">{html.escape(wtitle)}</h2>')
            spine.append(whref)
            lesson_lis = []
            for li, lesson in enumerate(lessons):
                href = f"c{bi}_{wi}_{li}.xhtml"
                spine.append(href)
                lesson_lis.append(f'<li><a href="{href}">{html.escape(titles[href])}</a></li>')
            week_lis.append(
                f'<li><a href="{whref}">{html.escape(wtitle)}</a><ol>{"".join(lesson_lis)}</ol></li>'
            )
        nav_items.append(
            f'<li><a href="{bhref}">{html.escape(btitle)}</a><ol>{"".join(week_lis)}</ol></li>'
        )

    nav = xhtml_page(
        "Contents",
        '<nav epub:type="toc" id="toc"><h1>Contents</h1><ol>' + "".join(nav_items) + "</ol></nav>",
    )

    book_id = f"urn:uuid:{uuid.uuid5(uuid.NAMESPACE_URL, 'renegade-rocks/ai-pro-level-course')}"
    modified = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    out.parent.mkdir(parents=True, exist_ok=True)
    cover_png = out.parent / "_cover.png"
    has_cover = make_cover(cover_png)

    manifest = ['<item id="nav" href="nav.xhtml" media-type="application/xhtml+xml" properties="nav"/>',
                '<item id="css" href="style.css" media-type="text/css"/>']
    if has_cover:
        manifest.append('<item id="cover-img" href="cover.png" media-type="image/png" properties="cover-image"/>')
    for href in spine:
        iid = href.replace(".xhtml", "")
        manifest.append(f'<item id="{iid}" href="{href}" media-type="application/xhtml+xml"/>')
    spine_xml = "".join(f'<itemref idref="{h.replace(".xhtml", "")}"/>' for h in spine)

    opf = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<package xmlns="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="bid">\n'
        '<metadata xmlns:dc="http://purl.org/dc/elements/1.1/">\n'
        f'<dc:identifier id="bid">{book_id}</dc:identifier>\n'
        "<dc:title>AI Pro-level Course — The Complete Lessons</dc:title>\n"
        "<dc:creator>Renegade Rocks</dc:creator>\n"
        "<dc:language>en</dc:language>\n"
        f'<meta property="dcterms:modified">{modified}</meta>\n'
        "</metadata>\n"
        f'<manifest>{"".join(manifest)}</manifest>\n'
        f"<spine>{spine_xml}</spine>\n"
        "</package>\n"
    )
    minidom.parseString(opf)

    container = (
        '<?xml version="1.0" encoding="utf-8"?>\n'
        '<container version="1.0" xmlns="urn:oasis:names:tc:opendocument:xmlns:container">\n'
        '<rootfiles><rootfile full-path="OEBPS/package.opf" media-type="application/oebps-package+xml"/></rootfiles>\n'
        "</container>\n"
    )

    with zipfile.ZipFile(out, "w") as z:
        z.writestr(zipfile.ZipInfo("mimetype"), "application/epub+zip", zipfile.ZIP_STORED)
        z.writestr("META-INF/container.xml", container, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/package.opf", opf, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/nav.xhtml", nav, zipfile.ZIP_DEFLATED)
        z.writestr("OEBPS/style.css", CSS, zipfile.ZIP_DEFLATED)
        if has_cover:
            z.write(cover_png, "OEBPS/cover.png", zipfile.ZIP_DEFLATED)
        for href, doc in {**extra_pages, **docs}.items():
            z.writestr(f"OEBPS/{href}", doc, zipfile.ZIP_DEFLATED)
    if has_cover:
        cover_png.unlink()

    n_lessons = len(chapters)
    print(f"wrote {out} — {n_lessons} lessons, {out.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="exports/ai-pro-level-course.epub")
    ap.add_argument("--block", default=None, help="limit to one block dir name, e.g. block-2-ai-employees")
    args = ap.parse_args()
    build(ROOT / args.out, args.block)
