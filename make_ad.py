#!/usr/bin/env python3
"""Render a landscape Amazon Sponsored video ad for a book.

    python make_ad.py books/reality-is-weirder.json

Writes out/ads/<id>.mp4 (1920x1080, 30fps, H.264/AAC, faststart) plus a
preview still for each beat, so the copy can be checked without scrubbing.
"""
from __future__ import annotations

import json
import os
import sys

from ads import ad

ROOT = os.path.dirname(os.path.abspath(__file__))


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    with open(sys.argv[1]) as f:
        spec = json.load(f)
    print(ad.render(spec, os.path.join(ROOT, "out", "ads")))


if __name__ == "__main__":
    main()
