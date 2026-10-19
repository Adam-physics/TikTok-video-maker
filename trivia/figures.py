"""Stock pieces for whiteboard scenes: stick figures, props, the book.

Stick figures are the vocabulary of the doodle videos viewers already
know, so a parent reads "bored kid" or "shocked kid" in a quarter second.
Faces carry the emotion; bodies stay deliberately plain.
"""
from __future__ import annotations

import math
import os

import numpy as np
from PIL import Image

from . import brand
from .doodle import KALAM, INK, Shape, Text, arc, circle, curve, ellipse, font, line, poly

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RED, GREEN, BLUE = brand.RED, brand.GREEN, brand.BLUE
GREY = (120, 120, 128)


def _dot(x, y, r):
    return circle(x, y, r, wobble=0.3)


def face(cx, cy, s, mood):
    """Eyes and mouth for a head centred at (cx, cy) with radius 62*s."""
    eyes, mouth, fill = [], [], None
    ex, ey = 24 * s, -8 * s
    if mood == "bored":
        # Same plain dot eyes as every other figure; the flat, slightly
        # sagging mouth carries the boredom.
        eyes = [_dot(cx - ex, cy + ey, 6 * s), _dot(cx + ex, cy + ey, 6 * s)]
        mouth = [line((cx - 20 * s, cy + 28 * s), (cx + 20 * s, cy + 32 * s), wobble=0.4)]
    elif mood == "happy":
        eyes = [_dot(cx - ex, cy + ey, 6 * s), _dot(cx + ex, cy + ey, 6 * s)]
        mouth = [arc(cx, cy + 12 * s, 30 * s, 22 * s, 15, 165)]
    elif mood == "shock":
        eyes = [circle(cx - ex, cy + ey, 13 * s, wobble=0.5),
                circle(cx + ex, cy + ey, 13 * s, wobble=0.5),
                _dot(cx - ex, cy + ey, 4 * s), _dot(cx + ex, cy + ey, 4 * s)]
        mouth = [ellipse(cx, cy + 30 * s, 12 * s, 17 * s, wobble=0.5)]
        fill = INK
    elif mood == "think":
        eyes = [_dot(cx - ex + 6 * s, cy + ey - 6 * s, 6 * s),
                _dot(cx + ex + 6 * s, cy + ey - 6 * s, 6 * s)]
        mouth = [line((cx - 6 * s, cy + 28 * s), (cx + 20 * s, cy + 24 * s), wobble=0.4)]
    return [Shape(eyes, width=max(4, int(6 * s))),
            Shape(mouth, width=max(4, int(6 * s)), fill=fill, fill_offset=(0, 0))]


def kid(cx, cy, s=1.0, mood="happy", arms="down"):
    """A stick-figure kid standing with feet near cy + 190*s."""
    hx, hy, r = cx, cy - 200 * s, 62 * s
    neck, hips = (cx, hy + r), (cx, cy + 30 * s)
    sh = (cx, cy - 100 * s)
    poses = {
        "down": [[sh, (cx - 45 * s, cy - 30 * s), (cx - 60 * s, cy + 20 * s)],
                 [sh, (cx + 45 * s, cy - 30 * s), (cx + 60 * s, cy + 20 * s)]],
        "hold": [[sh, (cx - 60 * s, cy - 40 * s), (cx - 35 * s, cy - 70 * s)],
                 [sh, (cx + 60 * s, cy - 40 * s), (cx + 35 * s, cy - 70 * s)]],
        "chin": [[sh, (cx - 45 * s, cy - 30 * s), (cx - 60 * s, cy + 20 * s)],
                 [sh, (cx + 70 * s, cy - 70 * s), (cx + 22 * s, hy + r + 4 * s)]],
        "up": [[sh, (cx - 70 * s, cy - 170 * s), (cx - 95 * s, cy - 260 * s)],
               [sh, (cx + 70 * s, cy - 170 * s), (cx + 95 * s, cy - 260 * s)]],
        "point": [[sh, (cx - 45 * s, cy - 30 * s), (cx - 60 * s, cy + 20 * s)],
                  [sh, (cx + 70 * s, cy - 110 * s), (cx + 135 * s, cy - 130 * s)]],
    }
    body = [poly([neck, hips], wobble=1.0),
            poly([hips, (cx - 50 * s, cy + 190 * s)], wobble=1.0),
            poly([hips, (cx + 50 * s, cy + 190 * s)], wobble=1.0),
            *[poly(a, wobble=1.0) for a in poses[arms]]]
    hair = [curve([(cx - 34 * s, hy - r + 14 * s), (cx - 30 * s, hy - r - 12 * s),
                   (cx - 12 * s, hy - r - 20 * s)], wobble=0.6),
            curve([(cx - 8 * s, hy - r + 2 * s), (cx + 2 * s, hy - r - 24 * s),
                   (cx + 22 * s, hy - r - 26 * s)], wobble=0.6),
            curve([(cx + 18 * s, hy - r + 6 * s), (cx + 36 * s, hy - r - 12 * s),
                   (cx + 50 * s, hy - r - 6 * s)], wobble=0.6)]
    w = max(6, int(9 * s))
    return [Shape(circle(hx, hy, r), width=w),
            Shape(hair, width=w),
            *face(hx, hy, s, mood),
            Shape(body, width=w)]


def bubble(cx, cy, rx, ry, tail, seed=0):
    """A speech bubble with its tail pointing at `tail`."""
    t = np.radians(np.linspace(-95, 265, 90))
    pts = np.stack([cx + rx * np.cos(t), cy + ry * np.sin(t)], axis=1)
    ang = math.atan2(tail[1] - cy, tail[0] - cx)
    base = [(cx + rx * 0.85 * math.cos(ang + d), cy + ry * 0.85 * math.sin(ang + d))
            for d in (-0.22, 0.22)]
    return Shape([poly(pts, wobble=1.6, seed=seed), poly([base[0], tail, base[1]], wobble=0.8)],
                 width=8)


def magnifier(cx, cy, r, angle=45, seed=0):
    a = math.radians(angle)
    p0 = (cx + r * math.cos(a), cy + r * math.sin(a))
    p1 = (cx + r * 1.9 * math.cos(a), cy + r * 1.9 * math.sin(a))
    return [Shape(circle(cx, cy, r, seed=seed), width=10),
            Shape(line(p0, p1), width=22)]


def word_box(text, size, face=KALAM):
    """Centre x and width of each word of a single centred line."""
    f = font(face, size)
    x = 540 - f.getlength(text) / 2
    out = {}
    for w in text.split():
        out.setdefault(w.strip(".,!?\"'\u201c\u201d").lower(), (x + f.getlength(w) / 2, f.getlength(w)))
        x += f.getlength(w + " ")
    return out


def polar_bear(cx, cy, s=1.0):
    """Outline-only bear: white on white, the way the claim pictures it."""
    w = max(7, int(9 * s))
    return [
        Shape(ellipse(cx, cy + 150 * s, 170 * s, 105 * s), width=w, fill=(255, 255, 255)),
        Shape([circle(cx - 85 * s, cy - 92 * s, 34 * s), circle(cx + 85 * s, cy - 92 * s, 34 * s)],
              width=w, fill=(255, 255, 255)),
        Shape(circle(cx, cy, 118 * s), width=w, fill=(255, 255, 255)),
        Shape([_dot(cx - 40 * s, cy - 22 * s, 9 * s), _dot(cx + 40 * s, cy - 22 * s, 9 * s)],
              fill=INK, width=5),
        Shape(ellipse(cx, cy + 40 * s, 54 * s, 40 * s), width=w),
        Shape(ellipse(cx, cy + 20 * s, 20 * s, 13 * s, wobble=0.5), fill=INK, width=5),
        Shape([ellipse(cx - 90 * s, cy + 250 * s, 52 * s, 26 * s),
               ellipse(cx + 90 * s, cy + 250 * s, 52 * s, 26 * s)], width=w, fill=(255, 255, 255)),
    ]


def hollow_hair(p0, p1, r, color=BLUE):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = (p1 - p0) / np.hypot(*(p1 - p0))
    n = np.array([-d[1], d[0]]) * r
    ang = math.degrees(math.atan2(d[1], d[0]))
    return Shape([line(p0 + n, p1 + n), line(p0 - n, p1 - n),
                  ellipse(*p1, r * 0.42, r, rot=ang, wobble=0.6),
                  ellipse(*p1, r * 0.2, r * 0.55, rot=ang, wobble=0.4),
                  arc(*p0, r * 0.42, r, 90, 270, rot=ang, wobble=0.6)], color=color, width=7)


def bumpy(cx, cy, rx, ry, bumps=11, depth=0.09, seed=0):
    """A cloud or thought-bubble outline."""
    t = np.linspace(0, 2 * math.pi, 220)
    r = 1 + depth * np.abs(np.sin(t * bumps / 2))
    return poly(np.stack([cx + rx * r * np.cos(t), cy + ry * r * np.sin(t)], axis=1),
                wobble=1.6, seed=seed)


def cover() -> Image.Image:
    return Image.open(os.path.join(ROOT, "assets", "cover.png"))


def page(name) -> Image.Image:
    return Image.open(os.path.join(ROOT, "assets", "pages", name))


def label(text, xy, size=78, color=INK, **kw):
    return Text(text, xy, size=size, color=color, **kw)
