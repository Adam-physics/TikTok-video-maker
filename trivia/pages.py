"""Cut a printed book page into its three panels.

A Trick Trivia page is three bordered cards stacked on a flat halftone
background, with the title lockup above them. Every card is outlined in
near-black and spans most of the page width, so the cards can be found by
looking for rows that are overwhelmingly dark: those rows are the card's
top and bottom rules, and a panel is the span between a pair of them.

Detection is a convenience, not a contract -- pass explicit bands in the
round file whenever a page does something unusual.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

DARK = 78              # luma at or below this counts as ink
LINE_COVERAGE = 0.50   # fraction of the width a row must ink to be a rule
MIN_PANEL_FRAC = 0.07  # a panel is at least this tall, as a page fraction
MAX_PANEL_FRAC = 0.45


def _dark_rows(img: Image.Image) -> np.ndarray:
    """Fraction of inked pixels per row, measured across the page interior."""
    grey = np.asarray(img.convert("L"), dtype=np.int16)
    x0 = int(grey.shape[1] * 0.06)
    interior = grey[:, x0:grey.shape[1] - x0]
    return (interior <= DARK).mean(axis=1)


def _rules(coverage: np.ndarray) -> list[tuple[int, int]]:
    """Collapse runs of inked rows into (start, end) rules."""
    hits = coverage >= LINE_COVERAGE
    runs, start = [], None
    for y, on in enumerate(hits):
        if on and start is None:
            start = y
        elif not on and start is not None:
            runs.append((start, y - 1))
            start = None
    if start is not None:
        runs.append((start, len(hits) - 1))
    return runs


def find_panels(path: str, expected: int = 3) -> list[tuple[int, int, int, int]]:
    """Return up to `expected` panel boxes as (left, top, right, bottom).

    Panels are ordered top to bottom. Raises if the page does not yield the
    expected count, so a bad crop fails loudly instead of shipping.
    """
    img = Image.open(path).convert("RGB")
    w, h = img.size
    rules = _rules(_dark_rows(img))

    lo, hi = MIN_PANEL_FRAC * h, MAX_PANEL_FRAC * h
    spans: list[tuple[int, int, int]] = []
    for (a_start, a_end), (b_start, b_end) in zip(rules, rules[1:]):
        height = b_end - a_start
        if lo <= height <= hi:
            spans.append((height, a_start, b_end))

    # Keep the tallest plausible spans, then restore reading order.
    spans.sort(reverse=True)
    chosen = sorted(spans[:expected], key=lambda s: s[1])
    if len(chosen) != expected:
        raise ValueError(
            f"{path}: found {len(chosen)} panel(s), expected {expected}. "
            "Run `python make.py calibrate <page>` and set explicit bands."
        )

    boxes = []
    for _, top, bottom in chosen:
        left, right = _horizontal_extent(img, top, bottom)
        boxes.append((left, top, right, bottom))
    return boxes


def _horizontal_extent(img: Image.Image, top: int, bottom: int) -> tuple[int, int]:
    """Trim a panel band to the card's own left and right rules."""
    grey = np.asarray(img.convert("L"), dtype=np.int16)[top:bottom + 1]
    inked = (grey <= DARK).mean(axis=0)
    cols = np.flatnonzero(inked >= 0.55)
    if cols.size < 2:
        return 0, img.size[0] - 1
    return int(cols[0]), int(cols[-1])


def crop_panels(path: str, bands=None, expected: int = 3) -> list[Image.Image]:
    """Crop a page into panel images, using explicit bands when given.

    `bands` is a list of (top, bottom) pairs as fractions of page height,
    which is how a round file overrides detection.
    """
    img = Image.open(path).convert("RGB")
    if bands:
        h, w = img.size[1], img.size[0]
        boxes = [(0, int(t * h), w - 1, int(b * h)) for t, b in bands]
    else:
        boxes = find_panels(path, expected)
    return [img.crop((l, t, r + 1, b + 1)) for l, t, r, b in boxes]


def crop_title(path: str) -> Image.Image:
    """Everything above the first panel: the book's own title lockup."""
    img = Image.open(path).convert("RGB")
    top = find_panels(path)[0][1]
    return img.crop((0, 0, img.size[0], max(top - 6, 1)))


def background_swatch(path: str, size: int = 96) -> Image.Image:
    """A clean tile of the page's halftone background.

    Sampled from the extreme corner, which the layout always leaves empty.
    """
    img = Image.open(path).convert("RGB")
    return img.crop((0, 0, size, size))


def calibrate(path: str, out_path: str) -> str:
    """Write a copy of the page with the detected panels outlined.

    This is the fast way to check a crop by eye before rendering 30 seconds
    of video around it.
    """
    img = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(img)
    for i, (l, t, r, b) in enumerate(find_panels(path), start=1):
        draw.rectangle((l, t, r, b), outline=(255, 0, 220), width=8)
        draw.text((l + 18, t + 14), f"panel {i}", fill=(255, 0, 220))
    img.save(out_path)
    return out_path
