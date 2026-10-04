"""Render a landscape Amazon Sponsored video ad for one book.

The ad is a sequence of text beats on the left and the cover on the right.
Every frame is composed in Pillow and piped straight into ffmpeg, so motion
is exact per frame: text lines rise in on a stagger, the cover breathes and
bumps on each cut, and the star field drifts underneath.

Amazon autoplays these muted, so the words carry the whole pitch. The cover
is on screen from frame one: there is no black lead-in, and a shopper who
reads only the first second still sees which book this is.
"""
from __future__ import annotations

import math
import os
import re
import subprocess

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from trivia.render import ffmpeg_bin

from . import score

W, H, FPS = 1920, 1080, 30
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
F_HEAD = os.path.join(FONTS, "BarlowCondensed-ExtraBold.ttf")
F_CHIP = os.path.join(FONTS, "BarlowCondensed-Bold.ttf")
F_SUB = os.path.join(FONTS, "BarlowSemiCondensed-SemiBold.ttf")

TEXT_X = 130            # left edge of the text column
TEXT_W = 900            # widest a line may run
COVER_CX = 1440         # cover centre
COVER_H = 930
WHITE = (255, 255, 255)
INK = (14, 16, 22)

ENTER, STAGGER, EXIT = 0.42, 0.09, 0.24


def _ease(x: float) -> float:
    x = min(1.0, max(0.0, x))
    return 1 - (1 - x) ** 3


# --- background ------------------------------------------------------------

def sky(spec: dict) -> Image.Image:
    """A star field with soft nebula glows, oversized so it can drift."""
    bw, bh = int(W * 1.12), int(H * 1.12)
    rng = np.random.default_rng(3)
    base = np.array(spec["base"], float)
    img = np.ones((bh, bw, 3)) * base
    yy, xx = np.mgrid[0:bh, 0:bw]
    for i, colour in enumerate(spec["glow"]):
        cx, cy = rng.uniform(0.15, 0.95) * bw, rng.uniform(0.1, 0.9) * bh
        r = rng.uniform(0.28, 0.42) * bw
        g = np.exp(-(((xx - cx) ** 2 + (yy - cy) ** 2) / (2 * r * r)))
        img += g[..., None] * (np.array(colour, float) - base) * 0.42

    stars = Image.new("L", (bw, bh))
    d = ImageDraw.Draw(stars)
    for _ in range(1600):
        x, y = rng.uniform(0, bw), rng.uniform(0, bh)
        v = int(255 * rng.uniform(0.15, 1.0) ** 2.2)
        d.point((x, y), fill=v)
    big = Image.new("L", (bw, bh))
    d = ImageDraw.Draw(big)
    for _ in range(70):
        x, y, r = rng.uniform(0, bw), rng.uniform(0, bh), rng.uniform(1.2, 2.4)
        d.ellipse((x - r, y - r, x + r, y + r), fill=255)
    layer = (np.asarray(stars.filter(ImageFilter.GaussianBlur(0.6)), float) * 2.2
             + np.asarray(big.filter(ImageFilter.GaussianBlur(1.6)), float) * 0.9)
    img += layer[..., None] * np.array([0.9, 0.95, 1.0])

    # Darken the text side so white type always clears the stars.
    shade = np.clip(1 - 0.35 * (1 - xx / (bw * 0.62)), 0.65, 1.0)
    img *= shade[..., None]
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


# --- cover -----------------------------------------------------------------

def book(path: str) -> Image.Image:
    """The cover dressed as a paperback: spine crease, sheen, drop shadow."""
    cover = Image.open(path).convert("RGB")
    cw = round(cover.width * COVER_H / cover.height)
    cover = cover.resize((cw, COVER_H), Image.LANCZOS)
    arr = np.asarray(cover, float)
    x = np.arange(cw)[None, :, None]
    crease = 1 - 0.32 * np.exp(-((x - 14) ** 2) / 30) + 0.12 * np.exp(-((x - 26) ** 2) / 40)
    edge = 1 - 0.25 * np.exp(-x / 6)
    arr = np.clip(arr * crease * edge, 0, 255)
    cover = Image.fromarray(arr.astype(np.uint8))

    pad = 70
    out = Image.new("RGBA", (cw + pad * 2, COVER_H + pad * 2), (0, 0, 0, 0))
    shadow = Image.new("L", out.size, 0)
    ImageDraw.Draw(shadow).rounded_rectangle(
        (pad + 10, pad + 22, pad + cw + 10, pad + COVER_H + 22), 8, fill=190)
    shadow = shadow.filter(ImageFilter.GaussianBlur(26))
    out.paste((0, 0, 0, 255), (0, 0), shadow)
    mask = Image.new("L", (cw, COVER_H), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw - 1, COVER_H - 1), 6, fill=255)
    out.paste(cover, (pad, pad), mask)
    return out


def halo(colour: tuple, size: int = 1100) -> Image.Image:
    """A soft accent glow that sits behind the cover."""
    yy, xx = np.mgrid[0:size, 0:size] - size / 2
    a = np.exp(-(xx ** 2 + yy ** 2) / (2 * (size * 0.22) ** 2)) * 70
    rgba = np.zeros((size, size, 4), np.uint8)
    rgba[..., :3] = colour
    rgba[..., 3] = a.astype(np.uint8)
    return Image.fromarray(rgba)


# --- text ------------------------------------------------------------------

def _segments(line: str) -> list[tuple[str, bool]]:
    """Split `*accent*` markup into (text, is_accent) runs."""
    parts = re.split(r"(\*[^*]+\*)", line)
    return [(p.strip("*"), p.startswith("*")) for p in parts if p]


def _width(font: ImageFont.FreeTypeFont, line: str) -> float:
    return sum(font.getlength(t) for t, _ in _segments(line))


def _shadowed(img: Image.Image, blur: int = 10, alpha: float = 0.7) -> Image.Image:
    pad = blur * 3
    out = Image.new("RGBA", (img.width + pad * 2, img.height + pad * 2), (0, 0, 0, 0))
    a = img.getchannel("A").point(lambda v: int(v * alpha))
    sh = Image.new("L", out.size, 0)
    sh.paste(a, (pad, pad + 6))
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    out.paste((0, 0, 0, 255), (0, 0), sh)
    out.alpha_composite(img, (pad, pad))
    return out


def _line(text: str, font, accent) -> Image.Image:
    asc, desc = font.getmetrics()
    img = Image.new("RGBA", (math.ceil(_width(font, text)) + 4, asc + desc), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    x = 0.0
    for t, hot in _segments(text):
        d.text((x, 0), t, font=font, fill=accent if hot else WHITE)
        x += font.getlength(t)
    return _shadowed(img)


def _chip(text: str, accent) -> Image.Image:
    font = ImageFont.truetype(F_CHIP, 44)
    track = 3                             # a little tracking reads as a label
    tw = sum(font.getlength(ch) + track for ch in text) - track
    asc, desc = font.getmetrics()
    w, h = round(tw + 44), asc + desc + 12
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((0, 0, w - 1, h - 1), h // 2, fill=accent + (255,))
    x = 22.0
    for ch in text:
        d.text((x, 6), ch, font=font, fill=INK)
        x += font.getlength(ch) + track
    return _shadowed(img, 8, 0.5)


def _wrap(text: str, font, width: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if font.getlength(trial) > width and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    return lines + [cur] if cur else lines


def card(beat: dict, accent) -> list[tuple[Image.Image, int, int]]:
    """Lay out one beat as [(element image, top y)], vertically centred."""
    size = 168
    while size > 60:
        head = ImageFont.truetype(F_HEAD, size)
        if max(_width(head, l) for l in beat["lines"]) <= TEXT_W:
            break
        size -= 4
    # (image, padding baked in by the shadow, step to the next element)
    items: list[tuple[Image.Image, int, int]] = []
    if beat.get("chip"):
        chip = _chip(beat["chip"], accent)
        items.append((chip, 24, chip.height - 48 + 20))
    for line in beat["lines"]:
        items.append((_line(line, head, accent), 30, round(size * 0.93)))
    if beat.get("sub"):
        sub = ImageFont.truetype(F_SUB, 60)
        items[-1] = items[-1][:2] + (items[-1][2] + 22,)
        lines = [w for part in beat["sub"].split("\n") for w in _wrap(part, sub, TEXT_W)]
        for l in lines:
            items.append((_line(l, sub, accent), 30, 70))
    last_img, last_pad, _ = items[-1]
    total = sum(step for _, _, step in items[:-1]) + last_img.height - 2 * last_pad
    y = (H - total) // 2
    placed = []
    for img, pad, step in items:
        placed.append((img, y - pad, pad))
        y += step
    return placed


# --- assembly --------------------------------------------------------------

def render(spec: dict, out_dir: str) -> str:
    accent = tuple(spec.get("accent", [255, 230, 0]))
    beats = spec["beats"]
    starts, t = [], 0.0
    for b in beats:
        starts.append(t)
        t += b["dur"]
    total = t
    frames = round(total * FPS)

    bg = sky(spec.get("sky", {"base": [8, 14, 26], "glow": [[34, 92, 104]]}))
    cover = book(os.path.join(ROOT, spec["cover"]))
    glow = halo(accent)
    cards = [card(b, accent) for b in beats]

    os.makedirs(out_dir, exist_ok=True)
    wav = os.path.join(out_dir, f"{spec['id']}.wav")
    score.render(total, starts[1:], wav)
    mp4 = os.path.join(out_dir, f"{spec['id']}.mp4")

    cmd = [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-i", wav,
           "-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-crf", "16",
           "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", str(FPS),
           "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
           "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-ac", "2",
           "-shortest", "-movflags", "+faststart", mp4]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE)

    previews = {0, *(round((s + b["dur"] * 0.6) * FPS) for s, b in zip(starts, beats))}
    for f in range(frames):
        now = f / FPS
        frame = _frame(now, total, bg, cover, glow, cards, beats, starts)
        if f in previews:
            frame.save(os.path.join(out_dir, f"{spec['id']}-f{f:04d}.png"))
        proc.stdin.write(frame.tobytes())
    proc.stdin.close()
    if proc.wait():
        raise RuntimeError("ffmpeg failed")
    os.remove(wav)
    return mp4


def _frame(now, total, bg, cover, glow, cards, beats, starts) -> Image.Image:
    # Background: a slow push-in across the whole ad.
    z = now / total
    cw, ch = bg.width - (bg.width - W) * z, bg.height - (bg.height - H) * z
    x0, y0 = (bg.width - cw) * 0.5, (bg.height - ch) * 0.4
    frame = bg.resize((W, H), Image.BILINEAR, box=(x0, y0, x0 + cw, y0 + ch)).convert("RGBA")

    # Cover: breathes, bumps on every cut, settles in on frame one.
    bump = sum(0.022 * math.exp(-(now - s) * 7) for s in starts[1:] if now >= s)
    settle = 0.05 * (1 - _ease(now / 0.7))
    grow = 0.05 * _ease((now - starts[-1]) / beats[-1]["dur"]) if now >= starts[-1] else 0
    s = 1 + bump + settle + grow + 0.008 * math.sin(now * 1.6)
    cy = H / 2 + 7 * math.sin(now * 1.2)
    gs = 1 + 0.04 * math.sin(now * 2.0) + bump * 2
    g = glow.resize((round(glow.width * gs), round(glow.height * gs)), Image.BILINEAR)
    frame.alpha_composite(g, (round(COVER_CX - g.width / 2), round(cy - g.height / 2)))
    c = cover.resize((round(cover.width * s), round(cover.height * s)), Image.BICUBIC)
    frame.alpha_composite(c, (round(COVER_CX - c.width / 2), round(cy - c.height / 2)))

    # Text: each element rises in on a stagger and lifts out before the cut.
    for i, (elements, beat, start) in enumerate(zip(cards, beats, starts)):
        end = start + beat["dur"]
        lead_in = 0.3 if i == 0 else 0.0        # first frame already reads
        if now < start - lead_in or now > end:
            continue
        last = i == len(beats) - 1
        for k, (img, y, pad) in enumerate(elements):
            p = _ease((now - start + lead_in - k * STAGGER) / ENTER)
            if p <= 0:
                continue
            q = 0.0 if last else _ease((now - (end - EXIT)) / EXIT)
            alpha = p * (1 - q)
            if alpha <= 0.01:
                continue
            dy = (1 - p) * 56 - q * 34
            layer = img
            if alpha < 0.999:
                layer = img.copy()
                layer.putalpha(img.getchannel("A").point(lambda v, a=alpha: int(v * a)))
            frame.alpha_composite(layer, (TEXT_X - pad, round(y + dy)))
    return frame.convert("RGB")
