#!/usr/bin/env python3
"""Generate example PNG assets for the QA-runner demo (stdlib only).

Writes solid-color PNGs at controlled dimensions into example/assets/ so the
example manifest can be run end-to-end without any image tool installed:

  - hero_main.png       1920x1080  (passes hero rules)
  - og_card.png         1200x630   (passes og rules)
  - og_card_bad.png     1200x628   (deliberately fails the og exact check)
  - ad_proof_v01.png    1080x1080  (passes ad rules)

Usage:  python make_fixtures.py
"""

from __future__ import annotations

import struct
import zlib
from pathlib import Path


def solid_png(width: int, height: int, rgb: tuple[int, int, int]) -> bytes:
    """Minimal valid RGB PNG: signature + IHDR + IDAT + IEND."""

    def chunk(tag: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + tag + data
                + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF))

    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    row = b"\x00" + bytes(rgb) * width          # filter byte 0 + pixels
    raw = row * height
    idat = zlib.compress(raw, 6)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", idat)
            + chunk(b"IEND", b""))


FIXTURES = [
    ("hero_main.png", 1920, 1080, (15, 23, 42)),      # slate
    ("og_card.png", 1200, 630, (56, 189, 248)),       # sky
    ("og_card_bad.png", 1200, 628, (56, 189, 248)),   # wrong height on purpose
    ("ad_proof_v01.png", 1080, 1080, (248, 250, 252)),
]


def main() -> int:
    out = Path(__file__).parent / "example" / "assets"
    out.mkdir(parents=True, exist_ok=True)
    for name, w, h, rgb in FIXTURES:
        path = out / name
        path.write_bytes(solid_png(w, h, rgb))
        print(f"wrote {path} ({w}x{h}, {path.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
