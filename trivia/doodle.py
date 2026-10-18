"""A small whiteboard-doodle animation engine.

Everything on screen is an *item* that knows how long it takes to draw and
how to paint itself at any point in that draw. A scene is a list of items
laid out on one sheet of paper; the scheduler hands each item a start time,
either straight after the previous one or pinned to a spoken word (a `cue`),
so the pen lands a stamp on the exact syllable the narrator says it.

Two details sell the hand-drawn look and are worth keeping:

- **Line boil.** Every few frames each stroke is redrawn with a slightly
  different wobble, the way a flipbook drawn by hand never sits still.
- **The pen.** A marker rides the tip of whatever is being drawn, so the
  viewer watches the drawing happen rather than seeing it fade in.
"""
from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import brand

W, H = brand.WIDTH, brand.HEIGHT
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HAND = os.path.join(ROOT, "assets", "fonts", "PatrickHand-Regular.ttf")
MARKER = os.path.join(ROOT, "assets", "fonts", "PermanentMarker-Regular.ttf")

INK = (30, 30, 36)
PAPER = (253, 251, 244)

BOIL_EVERY = 4          # frames between wobble redraws (~7.5 per second)
BOIL_AMP = 1.7          # pixels
DRAW_SPEED = 2600.0     # pixels of line per second at natural pace
POP = 0.32              # seconds for pictures and stamps to pop in

_fonts: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def _ease_out_back(u: float) -> float:
    c = 1.9
    u = min(max(u, 0.0), 1.0) - 1
    return 1 + (c + 1) * u ** 3 + c * u ** 2


# ---------------------------------------------------------------- shapes
#
# Every constructor returns an (N, 2) float array of points along the path,
# already wobbled the way a hand draws it. Points are dense enough that a
# partial draw can stop anywhere without a visible jump.

def _rng(seed):
    return np.random.default_rng(abs(hash(seed)) % (2 ** 32))


def _wobble(pts: np.ndarray, amp: float = 2.4, seed=0) -> np.ndarray:
    """Low-frequency hand tremor: smooth, never jagged."""
    n = len(pts)
    rng = _rng(("wobble", seed, n))
    phase = rng.uniform(0, 2 * math.pi, 4)
    s = np.linspace(0, 1, n) * rng.uniform(2.0, 3.5)
    dx = amp * (np.sin(2 * math.pi * s + phase[0]) + 0.5 * np.sin(5.1 * s + phase[1]))
    dy = amp * (np.sin(2 * math.pi * s + phase[2]) + 0.5 * np.sin(4.3 * s + phase[3]))
    return pts + np.stack([dx, dy], axis=1)


def _densify(pts, step: float = 6.0) -> np.ndarray:
    pts = np.asarray(pts, dtype=float)
    out = [pts[0]]
    for a, b in zip(pts[:-1], pts[1:]):
        n = max(1, int(np.hypot(*(b - a)) / step))
        for k in range(1, n + 1):
            out.append(a + (b - a) * k / n)
    return np.array(out)


def line(p0, p1, wobble=1.5, seed=0):
    return _wobble(_densify([p0, p1]), wobble, seed=(seed, tuple(p0)))


def poly(points, closed=False, wobble=2.0, seed=0):
    pts = list(points) + ([points[0]] if closed else [])
    return _wobble(_densify(pts), wobble, seed=(seed, tuple(map(tuple, points))))


def ellipse(cx, cy, rx, ry, a0=-100.0, sweep=380.0, rot=0.0, wobble=2.4, seed=0):
    """A hand-drawn ellipse overshoots its start a little, like a real one."""
    n = max(24, int(abs(sweep) / 360 * 2 * math.pi * max(rx, ry) / 6))
    t = np.radians(a0 + np.linspace(0, sweep, n))
    x, y = rx * np.cos(t), ry * np.sin(t)
    r = math.radians(rot)
    pts = np.stack([cx + x * math.cos(r) - y * math.sin(r),
                    cy + x * math.sin(r) + y * math.cos(r)], axis=1)
    return _wobble(pts, wobble, seed=(seed, cx, cy, rx, ry))


def circle(cx, cy, r, **kw):
    return ellipse(cx, cy, r, r, **kw)


def arc(cx, cy, rx, ry, a0, a1, **kw):
    return ellipse(cx, cy, rx, ry, a0=a0, sweep=a1 - a0, **kw)


def curve(points, wobble=1.6, seed=0, samples=14):
    """Catmull-Rom spline through the given points."""
    p = np.asarray(points, dtype=float)
    p = np.vstack([p[0], p, p[-1]])
    out = []
    for i in range(1, len(p) - 2):
        p0, p1, p2, p3 = p[i - 1], p[i], p[i + 1], p[i + 2]
        for t in np.linspace(0, 1, samples, endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t
                              + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(p[-2])
    return _wobble(_densify(out, 5), wobble, seed=(seed, len(points)))


def rrect(x0, y0, x1, y1, r=28, wobble=2.0, seed=0):
    pts = []
    for cx, cy, a in ((x1 - r, y0 + r, -90), (x1 - r, y1 - r, 0),
                      (x0 + r, y1 - r, 90), (x0 + r, y0 + r, 180)):
        for t in np.radians(np.linspace(a, a + 90, 8)):
            pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    pts.append(pts[0])
    return _wobble(_densify(pts), wobble, seed=(seed, x0, y0, x1, y1))


def star(cx, cy, r_out, r_in=None, points=5, rot=-90, seed=0):
    r_in = r_in or r_out * 0.45
    pts = []
    for k in range(points * 2):
        r = r_out if k % 2 == 0 else r_in
        a = math.radians(rot + k * 180 / points)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return poly(pts, closed=True, wobble=1.2, seed=seed)


def heart(cx, cy, s, seed=0):
    t = np.linspace(0, 2 * math.pi, 90)
    x = 16 * np.sin(t) ** 3
    y = -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))
    pts = np.stack([cx + x * s / 16, cy + y * s / 16], axis=1)
    return _wobble(pts, 1.2, seed=(seed, cx, cy))


def check(cx, cy, s, seed=0):
    return poly([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.8)],
                wobble=1.0, seed=seed)


def arrow(p0, p1, bend=0.0, head=34, seed=0):
    """A curved arrow; returns two paths (shaft, head) drawn as one item."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    mid = (p0 + p1) / 2
    d = p1 - p0
    normal = np.array([-d[1], d[0]]) / (np.hypot(*d) + 1e-9)
    shaft = curve([p0, mid + normal * bend, p1], seed=seed)
    tang = shaft[-1] - shaft[-6]
    ang = math.atan2(tang[1], tang[0])
    tip = shaft[-1]
    left = tip + head * np.array([math.cos(ang + 2.6), math.sin(ang + 2.6)])
    right = tip + head * np.array([math.cos(ang - 2.6), math.sin(ang - 2.6)])
    return [shaft, poly([left, tip, right], wobble=0.8, seed=seed)]


# ---------------------------------------------------------------- items

class Item:
    duration = 0.5
    cue: str | None = None
    start = 0.0
    sound: str | None = None        # effect to fire when the item starts
    scribble = False                # draws with pen noise

    def at(self, cue: str, sound: str | None = None):
        self.cue = cue.lower()
        if sound:
            self.sound = sound
        return self

    def tip(self, t: float):
        """Pen position while drawing, or None."""
        return None

    def paint(self, img: Image.Image, t: float, boil: int) -> None:
        raise NotImplementedError


class Shape(Item):
    """One or more paths drawn in order, optionally filled once closed."""

    scribble = True

    def __init__(self, paths, color=INK, width=9, fill=None, speed=1.0,
                 fill_offset=(7, 6)):
        if isinstance(paths, np.ndarray):
            paths = [paths]
        self.paths = [np.asarray(p, float) for p in paths]
        self.color, self.width, self.fill = color, width, fill
        self.fill_offset = fill_offset
        self.lengths = [float(np.sum(np.hypot(*np.diff(p, axis=0).T))) for p in self.paths]
        self.total = sum(self.lengths) or 1.0
        self.duration = max(0.18, self.total / (DRAW_SPEED * speed))
        self.seed = int(self.total * 7) % 997

    def _boiled(self, p: np.ndarray, boil: int, k: int) -> np.ndarray:
        s = self.seed + k * 13
        dx = BOIL_AMP * np.sin(0.021 * p[:, 1] + 2.3 * boil + s)
        dy = BOIL_AMP * np.cos(0.019 * p[:, 0] + 1.9 * boil + s * 1.3)
        return p + np.stack([dx, dy], axis=1)

    def _progress(self, t):
        return min(max((t - self.start) / self.duration, 0.0), 1.0)

    def _partial(self, u):
        """Yield (index, points) of each path drawn so far at progress u."""
        budget = u * self.total
        for k, (p, length) in enumerate(zip(self.paths, self.lengths)):
            if budget <= 0:
                return
            if budget >= length:
                yield k, p
            else:
                seg = np.hypot(*np.diff(p, axis=0).T)
                cut = int(np.searchsorted(np.cumsum(seg), budget)) + 1
                yield k, p[:max(cut, 2)]
            budget -= length

    def tip(self, t):
        u = self._progress(t)
        if u <= 0 or u >= 1:
            return None
        last = None
        for _, pts in self._partial(u):
            last = pts[-1]
        return last

    def paint(self, img, t, boil):
        u = self._progress(t)
        if u <= 0:
            return
        draw = ImageDraw.Draw(img, "RGBA")
        if self.fill is not None and u >= 1:
            a = min(1.0, (t - self.start - self.duration) / 0.18)
            ox, oy = self.fill_offset
            for k, p in enumerate(self.paths):
                if len(p) > 2:
                    q = self._boiled(p, boil, k) + (ox, oy)
                    draw.polygon([tuple(x) for x in q], fill=(*self.fill, int(255 * a)))
        r = self.width / 2
        for k, pts in self._partial(u):
            q = self._boiled(pts, boil, k)
            draw.line([tuple(x) for x in q], fill=self.color, width=self.width, joint="curve")
            for end in (q[0], q[-1]):
                draw.ellipse([end[0] - r, end[1] - r, end[0] + r, end[1] + r], fill=self.color)


class Text(Item):
    """Handwritten text, revealed left to right one line at a time."""

    def __init__(self, text, xy, size=80, color=INK, face=HAND, anchor="mm",
                 max_width=940, stroke=0, stroke_color=INK, per_char=0.035, spacing=10):
        f = font(face, size)
        lines = self._wrap(text, f, max_width)
        probe = ImageDraw.Draw(Image.new("L", (1, 1)))
        boxes = [probe.textbbox((0, 0), ln, font=f, stroke_width=stroke) for ln in lines]
        lh = max(b[3] - b[1] for b in boxes) + spacing
        width = max(b[2] - b[0] for b in boxes) + 2 * stroke + 8
        height = lh * len(lines) + 2 * stroke + 8
        self.layer = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, 0))
        d = ImageDraw.Draw(self.layer)
        self.line_spans = []
        for i, (ln, b) in enumerate(zip(lines, boxes)):
            lw = b[2] - b[0]
            x = (width - lw) / 2 - b[0]
            y = i * lh - b[1] + stroke + 4
            d.text((x, y), ln, font=f, fill=color, stroke_width=stroke, stroke_fill=stroke_color)
            self.line_spans.append(((width - lw) / 2 - stroke, (width + lw) / 2 + stroke,
                                    i * lh, (i + 1) * lh + stroke * 2 + 8, len(ln)))
        x, y = xy
        ax, ay = anchor
        self.x = int(x - {"l": 0, "m": width / 2, "r": width}[ax])
        self.y = int(y - {"t": 0, "m": height / 2, "b": height}[ay])
        self.w, self.h = int(width), int(height)
        chars = sum(s[4] for s in self.line_spans)
        self.duration = max(0.25, chars * per_char)

    @staticmethod
    def _wrap(text, f, max_width):
        out = []
        for para in text.split("\n"):
            words, cur = para.split(), ""
            for w in words:
                trial = f"{cur} {w}".strip()
                if f.getlength(trial) <= max_width or not cur:
                    cur = trial
                else:
                    out.append(cur)
                    cur = w
            out.append(cur)
        return out

    def _reveal(self, t):
        """(line index, x reached) at time t."""
        chars = sum(s[4] for s in self.line_spans)
        done = min(max((t - self.start) / self.duration, 0.0), 1.0) * chars
        for i, (x0, x1, *_rest, n) in enumerate(self.line_spans):
            if done < n:
                return i, x0 + (x1 - x0) * done / max(n, 1)
            done -= n
        return len(self.line_spans), None

    def tip(self, t):
        if not (self.start < t < self.start + self.duration):
            return None
        i, x = self._reveal(t)
        if x is None:
            return None
        y0, y1 = self.line_spans[i][2], self.line_spans[i][3]
        return np.array([self.x + x, self.y + (y0 + y1) * 0.62])

    def paint(self, img, t, boil):
        if t <= self.start:
            return
        i, x = self._reveal(t)
        mask = Image.new("L", self.layer.size, 0)
        d = ImageDraw.Draw(mask)
        for k, (x0, x1, y0, y1, _) in enumerate(self.line_spans):
            if k < i:
                d.rectangle([0, y0, self.w, y1], fill=255)
            elif k == i and x is not None:
                d.rectangle([0, y0, x, y1], fill=255)
        layer = Image.new("RGBA", self.layer.size, (0, 0, 0, 0))
        layer.paste(self.layer, (0, 0), mask)
        jx, jy = (boil % 2), ((boil // 2) % 2)
        img.alpha_composite(layer, (self.x + jx, self.y + jy))


class Picture(Item):
    """An image that pops in with an overshoot: stamps, book pages."""

    def __init__(self, image: Image.Image, center, width=None, angle=0.0, shadow=True):
        im = image.convert("RGBA")
        if width:
            im = im.resize((int(width), int(im.height * width / im.width)), Image.LANCZOS)
        if shadow:
            pad = 24
            sh = Image.new("RGBA", (im.width + pad * 2, im.height + pad * 2), (0, 0, 0, 0))
            alpha = im.getchannel("A").point(lambda v: v * 0.28)
            blk = Image.new("RGBA", im.size, (0, 0, 0, 255))
            blk.putalpha(alpha)
            sh.alpha_composite(blk, (pad + 10, pad + 14))
            from PIL import ImageFilter
            sh = sh.filter(ImageFilter.GaussianBlur(9))
            sh.alpha_composite(im, (pad, pad))
            im = sh
        self.image = im.rotate(angle, resample=Image.BICUBIC, expand=True)
        self.center = center
        self.duration = POP

    def paint(self, img, t, boil):
        if t <= self.start:
            return
        u = (t - self.start) / self.duration
        s = _ease_out_back(u) if u < 1 else 1.0
        if s <= 0.02:
            return
        im = self.image
        if abs(s - 1) > 1e-3:
            im = im.resize((max(1, int(im.width * s)), max(1, int(im.height * s))), Image.BILINEAR)
        cx, cy = self.center
        img.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))


def stamp(text, color, size=150, angle=-8, face=MARKER) -> Image.Image:
    """A rubber-stamp word in a rough box, as a still to pop in."""
    f = font(face, size)
    probe = ImageDraw.Draw(Image.new("L", (1, 1)))
    b = probe.textbbox((0, 0), text, font=f)
    tw, th = b[2] - b[0], b[3] - b[1]
    pad = 40
    im = Image.new("RGBA", (tw + pad * 2, th + pad * 2), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([6, 6, im.width - 6, im.height - 6], radius=24,
                        outline=color, width=12, fill=(255, 255, 255, 235))
    d.text((pad - b[0], pad - b[1]), text, font=f, fill=color)
    return im.rotate(angle, resample=Image.BICUBIC, expand=True)


# ---------------------------------------------------------------- pen

def _pen_sprite() -> Image.Image:
    """A chunky marker held at an angle; its nib sits at the image origin."""
    im = Image.new("RGBA", (260, 260), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    # Body runs down-right from the nib at (0, 0).
    def rot(pts, a=math.radians(38)):
        return [(x * math.cos(a) - y * math.sin(a), x * math.sin(a) + y * math.cos(a))
                for x, y in pts]
    nib = rot([(0, 0), (22, -9), (22, 9)])
    body = rot([(22, -15), (210, -19), (210, 19), (22, 15)])
    cap = rot([(150, -20), (212, -20), (212, 20), (150, 20)])
    for shape, fill in ((body, (245, 245, 245, 255)), (cap, (*brand.ORANGE, 255)),
                        (nib, (*INK, 255))):
        d.polygon(shape, fill=fill, outline=(*INK, 255))
        d.line(shape + [shape[0]], fill=(*INK, 255), width=5)
    return im


_PEN = None


def paint_pen(img: Image.Image, xy) -> None:
    global _PEN
    if _PEN is None:
        _PEN = _pen_sprite()
    img.alpha_composite(_PEN, (int(xy[0]) - 2, int(xy[1]) - 2))


# ---------------------------------------------------------------- paper

def paper() -> Image.Image:
    """Off-white sheet with a faint grain, so flat colour never looks digital."""
    rng = np.random.default_rng(3)
    grain = rng.normal(0, 3.2, (H, W, 1))
    base = np.array(PAPER, dtype=float)[None, None, :] + grain
    yy, xx = np.mgrid[0:H, 0:W]
    vignette = ((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2
    base -= vignette[..., None] * 26
    return Image.fromarray(np.clip(base, 0, 255).astype("uint8")).convert("RGBA")
