"""Cut a printed book page into its three panels.

A Trick Trivia page is three cards stacked on a flat halftone ground, with
the title lockup above them. The cards are found by looking for the ground
itself: the only rows that are almost entirely background are the seams
between cards, the breathing space under the title, and the margin below
the last card. Four such seams bound three panels.

Ink is not a usable signal here -- the illustrations are full-bleed and
frequently darker than the card outlines, and decorative bubbles overlap
the card edges. Background coverage is stable across every page tested,
including reveal pages whose underwater art is close in hue to the ground.

Detection is a convenience, not a contract: pass explicit bands in the
round file whenever a page does something unusual, and check any new page
with `python make.py calibrate` before rendering around it.
"""
from __future__ import annotations

import numpy as np
from PIL import Image, ImageDraw

BG_TOLERANCE = 190     # summed per-channel distance that still reads as ground
SEAM_COVERAGE = 0.55   # fraction of the row width that must be ground
EDGE_COVERAGE = 0.50   # looser, for the outer edges of the panel block
MIN_SEPARATION = 200   # px; stops one wide seam being counted twice
SEARCH_TOP, SEARCH_BOTTOM = 0.35, 0.75   # where interior seams can live


def _ground_profile(img: Image.Image) -> np.ndarray:
    """Per-row fraction of pixels matching the page's background colour."""
    a = np.asarray(img, dtype=np.int16)
    h, w = a.shape[:2]
    ring = np.concatenate([a[:30].reshape(-1, 3), a[-30:].reshape(-1, 3)])
    ground = np.median(ring, axis=0)
    matches = np.abs(a - ground).sum(axis=2) < BG_TOLERANCE
    return matches[:, int(w * 0.10):int(w * 0.90)].mean(axis=1)


def _seams(profile: np.ndarray, lo: int, hi: int, threshold: float):
    """Runs of mostly-background rows, strongest first."""
    runs, y = [], lo
    while y < hi:
        if profile[y] >= threshold:
            start = y
            while y < hi and profile[y] >= threshold:
                y += 1
            runs.append((float(profile[start:y].max()), start, y - 1))
        else:
            y += 1
    return sorted(runs, reverse=True)


def _interior_seams(profile: np.ndarray, h: int) -> list[tuple[int, int]]:
    """The two seams between the three cards."""
    lo, hi = int(h * SEARCH_TOP), int(h * SEARCH_BOTTOM)
    chosen: list[tuple[float, int, int]] = []
    for run in _seams(profile, lo, hi, SEAM_COVERAGE):
        if all(abs(run[1] - kept[1]) >= MIN_SEPARATION for kept in chosen):
            chosen.append(run)
        if len(chosen) == 2:
            break
    if len(chosen) != 2:
        raise ValueError("could not find the two seams between the three cards")
    return sorted((start, end) for _, start, end in chosen)


def _sustained_runs(profile, lo: int, hi: int, min_length: int = 4):
    """Background runs long enough to be real breathing space, not a light
    patch inside an illustration."""
    runs, y = [], lo
    while y < hi:
        if profile[y] >= SEAM_COVERAGE:
            start = y
            while y < hi and profile[y] >= SEAM_COVERAGE:
                y += 1
            if y - start >= min_length:
                runs.append((start, y - 1))
        else:
            y += 1
    return runs


def _block_edges(profile: np.ndarray, h: int, first: int, last: int) -> tuple[int, int]:
    """Top of the first card and bottom of the last, either side of the seams."""
    above = _sustained_runs(profile, int(h * 0.08), first)
    below = _sustained_runs(profile, last + 1, int(h * 0.97))
    top = above[-1][1] + 1 if above else int(h * 0.20)
    bottom = below[0][0] - 1 if below else int(h * 0.92)
    return top, bottom


def find_panels(path: str) -> list[tuple[int, int, int, int]]:
    """Return the three panel boxes as (left, top, right, bottom), top down."""
    img = Image.open(path).convert("RGB")
    h = img.size[1]
    profile = _ground_profile(img)
    (g1_start, g1_end), (g2_start, g2_end) = _interior_seams(profile, h)
    top, bottom = _block_edges(profile, h, g1_start, g2_end)

    bands = [(top, g1_start - 1), (g1_end + 1, g2_start - 1), (g2_end + 1, bottom)]
    bands[0] = (_trim_banner(bands), bands[0][1])

    boxes = []
    for band_top, band_bottom in bands:
        left, right = _horizontal_extent(img, band_top, band_bottom)
        boxes.append((left, band_top, right, band_bottom))
    return boxes


def _trim_banner(bands) -> int:
    """Pull the first band down off the page's strapline.

    On claim pages a banner ("CAN YOU SPOT THE TRUTH?") sits above the first
    card and inside its seam, which would make panel one taller than the two
    below it. When the first band runs noticeably long, trim the excess from
    its top so all three panels match.
    """
    (top, first_bottom), *rest = bands
    typical = sorted(b - t for t, b in rest)[len(rest) // 2]
    overshoot = (first_bottom - top) - typical
    return top + overshoot if overshoot > typical * 0.12 else top


def _horizontal_extent(img: Image.Image, top: int, bottom: int) -> tuple[int, int]:
    """Trim a band to the card's own left and right edges."""
    a = np.asarray(img, dtype=np.int16)
    ring = np.concatenate([a[:30].reshape(-1, 3), a[-30:].reshape(-1, 3)])
    ground = np.median(ring, axis=0)
    band = a[top:bottom + 1]
    on_card = (np.abs(band - ground).sum(axis=2) >= BG_TOLERANCE).mean(axis=0)
    cols = np.flatnonzero(on_card >= 0.55)
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
        boxes = find_panels(path)
    if len(boxes) != expected:
        raise ValueError(f"{path}: got {len(boxes)} panels, expected {expected}")
    return [img.crop((l, t, r + 1, b + 1)) for l, t, r, b in boxes]


def crop_title(path: str) -> Image.Image:
    """Everything above the first panel: the book's own title lockup."""
    img = Image.open(path).convert("RGB")
    top = find_panels(path)[0][1]
    return img.crop((0, 0, img.size[0], max(top - 6, 1)))


def _period(block: np.ndarray, axis: int, lo: int = 6, hi: int = 40) -> int:
    """The repeat length of the halftone along one axis.

    A swatch cut to a whole number of periods tiles without seams; a swatch
    of an arbitrary size leaves a visible grid across the finished frame.
    """
    limit = min(hi, block.shape[axis] // 2)
    if limit <= lo:
        return max(1, block.shape[axis])
    scores = []
    for step in range(lo, limit + 1):
        a, b = (block[:-step], block[step:]) if axis == 0 else \
               (block[:, :-step], block[:, step:])
        scores.append((float(np.abs(a - b).mean()), step))
    return min(scores)[1]


def background_swatch(path: str) -> Image.Image:
    """A seamlessly tileable piece of the page's halftone ground.

    The page corners are not empty -- a mascot and decorative stars sit in
    them -- so the swatch is cut from the widest band of pure ground on the
    page, then sized to a whole number of halftone periods. Tiling anything
    else leaves a visible grid across the finished frame.
    """
    img = Image.open(path).convert("RGB")
    profile = _ground_profile(img)
    bands, y, h = [], 0, img.size[1]
    while y < h:
        if profile[y] >= 0.99:
            start = y
            while y < h and profile[y] >= 0.99:
                y += 1
            bands.append((y - start, start, y - 1))
        else:
            y += 1
    if not bands:
        return img.crop((0, 0, 16, 16))

    _, top, bottom = max(bands)
    strip = np.asarray(img.crop((0, top, img.size[0], bottom + 1)), dtype=np.int16)
    px, py = _period(strip, 1), _period(strip, 0)
    return img.crop((0, top, px, top + py))


def calibrate(path: str, out_path: str) -> str:
    """Write a copy of the page with the detected panels outlined."""
    img = Image.open(path).convert("RGB")
    draw = ImageDraw.Draw(img)
    for i, (l, t, r, b) in enumerate(find_panels(path), start=1):
        draw.rectangle((l, t, r, b), outline=(255, 0, 220), width=8)
        draw.text((l + 18, t + 14), f"panel {i}", fill=(255, 0, 220))
    img.save(out_path)
    return out_path
