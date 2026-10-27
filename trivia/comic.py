"""Full-screen comic shorts: the book's own pages, filmed like a feed video.

The whiteboard format reads as a slide in a feed of faces and full-bleed
footage. This format opens on a printed page that fills the screen, then
the camera moves panel to panel with a spotlight, stamps slam onto the
reveals, and the text is TikTok-style: a white hook box up top and bold
outlined captions. Nothing important sits under the app's own UI.

An angle module for this format provides:

    ID, Q, A                      page files in assets/pages (question, answer)
    SCRIPT = [(text, shot), ...]  one shot per narrated line
    CAPTION, HASHTAGS

A shot is a dict: {"view": "page"|"panel"|"lock"|"end", "page": "q"|"a",
"panel": 0..2, "box": hook text, "stamp": (word, cue), "count": [cues]}.
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import brand, foley, voice
from .render import ffmpeg_bin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W, H, FPS = brand.WIDTH, brand.HEIGHT, brand.FPS
BOLD = os.path.join(ROOT, "assets", "fonts", "Montserrat-Black.ttf")
TAIL = 0.35
MOVE = 0.45                    # camera move between shots
CY = 860                       # where the subject sits: clear of the captions
CAPTION_Y = 1440
BOX_Y = 250                    # top of the hook box, under TikTok's top menu
YELLOW = (255, 214, 64)

# Every claim page and every answer page shares one layout, so the panels are
# fixed fractions of the page (x0, y0, x1, y1).
PANELS = {
    "q": [(0.05, 0.245, 0.96, 0.465), (0.05, 0.47, 0.96, 0.69), (0.05, 0.69, 0.96, 0.908)],
    "a": [(0.035, 0.16, 0.945, 0.405), (0.035, 0.403, 0.945, 0.65), (0.035, 0.65, 0.945, 0.902)],
}
WHOLE = (0.0, 0.0, 1.0, 1.0)


def _font(size):
    return ImageFont.truetype(BOLD, size)


def _norm(w):
    return re.sub(r"[^\w-]", "", w.lower())


def _ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ pictures

class Pages:
    def __init__(self, q, a):
        load = lambda n: Image.open(os.path.join(ROOT, "assets", "pages", n)).convert("RGB")
        self.img = {"q": load(q), "a": load(a),
                    "cover": Image.open(os.path.join(ROOT, "assets", "cover.png")).convert("RGB")}
        self.bg = {k: self._backdrop(v) for k, v in self.img.items()}

    @staticmethod
    def _backdrop(img):
        """The page itself, blurred and dimmed, filling the whole frame."""
        s = max(W / img.width, H / img.height) * 1.1
        big = img.resize((int(img.width * s), int(img.height * s)), Image.BILINEAR)
        x, y = (big.width - W) // 2, (big.height - H) // 2
        big = big.crop((x, y, x + W, y + H)).filter(ImageFilter.GaussianBlur(36))
        return Image.blend(big, Image.new("RGB", (W, H), (0, 0, 0)), 0.45)


def view(pages, key, rect, zoom=1.0, shake=(0, 0)):
    """Frame showing `rect` of a page, fitted to the width, centred on CY."""
    img = pages.img[key]
    pw, ph = img.size
    rx0, ry0, rx1, ry1 = rect[0] * pw, rect[1] * ph, rect[2] * pw, rect[3] * ph
    fit = 1080 if rect != WHOLE else 1000          # panels run edge to edge
    s = min(fit / (rx1 - rx0), 1560 / (ry1 - ry0)) * zoom
    cx, cy = (rx0 + rx1) / 2, (ry0 + ry1) / 2
    frame = pages.bg[key].copy()
    # The part of the page that lands inside the frame.
    fx0, fy0 = cx - (W / 2 + shake[0]) / s, cy - (CY + shake[1]) / s
    fx1, fy1 = fx0 + W / s, fy0 + H / s
    sx0, sy0, sx1, sy1 = max(fx0, 0), max(fy0, 0), min(fx1, pw), min(fy1, ph)
    if sx1 <= sx0 or sy1 <= sy0:
        return frame, s, (0, 0)
    part = img.crop((int(sx0), int(sy0), int(math.ceil(sx1)), int(math.ceil(sy1))))
    dw, dh = int(round((sx1 - sx0) * s)), int(round((sy1 - sy0) * s))
    part = part.resize((max(dw, 1), max(dh, 1)), Image.BILINEAR)
    dx, dy = int(round((sx0 - fx0) * s)), int(round((sy0 - fy0) * s))
    # A soft shadow so the page sits on its backdrop rather than in it.
    sh = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sh).rectangle([dx + 10, dy + 18, dx + dw + 10, dy + dh + 18], fill=150)
    frame.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(18)))
    frame.paste(part, (dx, dy))
    to_frame = lambda x, y: ((x - fx0) * s, (y - fy0) * s)
    return frame, s, to_frame


def spotlight(frame, box, alpha):
    """Dim everything outside one panel."""
    if alpha <= 0:
        return frame
    mask = Image.new("L", (W, H), int(170 * alpha))
    ImageDraw.Draw(mask).rounded_rectangle(box, radius=26, fill=0)
    frame.paste((0, 0, 0), (0, 0), mask.filter(ImageFilter.GaussianBlur(4)))
    return frame


def hook_box(img, text, t_in, t):
    """TikTok-style white box with black bold text."""
    if t < t_in:
        return
    f = _font(56)
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if f.getlength(trial) > 880 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = trial
    lines.append(cur)
    lh = 70
    pop = min(1.0, (t - t_in) / 0.18)
    scale = 0.85 + 0.15 * _ease(pop) + 0.04 * math.sin(min(pop, 1) * math.pi)
    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    widths = [f.getlength(l) for l in lines]
    bw, bh = max(widths) + 56, lh * len(lines) + 34
    x0, y0 = (W - bw) / 2, BOX_Y
    d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=18, fill=(255, 255, 255, 255))
    for i, l in enumerate(lines):
        d.text((W / 2, y0 + 17 + lh * i + lh / 2), l, font=f, fill=(12, 12, 16), anchor="mm")
    if scale != 1.0:
        cx, cy = W / 2, y0 + bh / 2
        layer = layer.transform((W, H), Image.AFFINE, (1 / scale, 0, cx - cx / scale, 0, 1 / scale,
                                                       cy - cy / scale), Image.BILINEAR)
    img.paste(layer, (0, 0), layer)


def stamp(img, word, at, t, centre):
    """A tick or a cross slammed onto the panel's art (the page already prints the word)."""
    if t < at:
        return
    u = t - at
    k = min(1.0, u / 0.16)
    scale = 2.2 - 1.2 * _ease(k) + (0.08 * math.sin((u - 0.16) * 30) * math.exp(-(u - 0.16) * 9)
                                    if u > 0.16 else 0)
    real = word.startswith("REAL")
    color = (40, 165, 60) if real else (226, 40, 36)
    r = 120
    size = 2 * r + 40
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    c = size / 2
    d.ellipse([c - r, c - r, c + r, c + r], fill=(255, 255, 255, 255), outline=color, width=16)
    if real:
        d.line([(c - 62, c + 4), (c - 18, c + 50), (c + 66, c - 52)], fill=color, width=34, joint="curve")
    else:
        d.line([(c - 52, c - 52), (c + 52, c + 52)], fill=color, width=34)
        d.line([(c + 52, c - 52), (c - 52, c + 52)], fill=color, width=34)
    layer = layer.rotate(-8, resample=Image.BICUBIC)
    layer = layer.resize((max(1, int(size * scale)), max(1, int(size * scale))), Image.BILINEAR)
    if k < 1:
        layer.putalpha(layer.getchannel("A").point(lambda v: int(v * k)))
    img.paste(layer, (int(centre[0] - layer.width / 2), int(centre[1] - layer.height / 2)), layer)
    if u < 0.09:
        flash = Image.new("RGB", (W, H), (255, 255, 255))
        img.paste(Image.blend(img, flash, 0.35 * (1 - u / 0.09)), (0, 0))


def big_number(img, n, at, t, x):
    if t < at:
        return
    u = min(1.0, (t - at) / 0.15)
    f = _font(int(260 * (1.4 - 0.4 * _ease(u))))
    ImageDraw.Draw(img).text((x, 900), n, font=f, fill=(255, 255, 255), anchor="mm",
                             stroke_width=14, stroke_fill=(12, 12, 16))


def captions(img, words, t):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["text"][-1] in ".,!?:":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    group = None
    for g in groups:
        if g[0]["start"] - 0.05 <= t <= g[-1]["end"] + 0.2:
            group = g
    if not group:
        return
    f = _font(68)
    texts = [w["text"].strip('"“”') for w in group]
    space = f.getlength(" ")
    widths = [f.getlength(s) for s in texts]
    x = (W - 60 - sum(widths) - space * (len(texts) - 1)) / 2
    d = ImageDraw.Draw(img)
    for w, s, wd in zip(group, texts, widths):
        active = w["start"] - 0.03 <= t <= w["end"] + 0.05
        d.text((x, CAPTION_Y), s, font=f, fill=YELLOW if active else (255, 255, 255), anchor="ls",
               stroke_width=8, stroke_fill=(12, 12, 16))
        x += wd + space


def end_card(pages, t_in, t, lines):
    frame = pages.bg["cover"].copy()
    cov = pages.img["cover"]
    u = _ease(min(1.0, (t - t_in) / 0.4))
    w = int(600 + 50 * u)
    c = cov.resize((w, int(cov.height * w / cov.width)), Image.BILINEAR)
    sh = Image.new("L", (W, H), 0)
    x, y = (W - c.width) // 2, CY - c.height // 2 - 10
    ImageDraw.Draw(sh).rectangle([x + 12, y + 20, x + c.width + 12, y + c.height + 20], fill=170)
    frame.paste((0, 0, 0), (0, 0), sh.filter(ImageFilter.GaussianBlur(20)))
    frame.paste(c, (x, y))
    return frame


# ------------------------------------------------------------------ timing

def timeline(script, words):
    shots, i = [], 0
    for text, shot in script:
        n = len(text.split())
        ws = words[i:i + n]
        i += n
        shots.append(dict(shot, words=ws, t0=ws[0]["start"] if ws else 0.0))
    for k, s in enumerate(shots):
        s["t0"] = 0.0 if k == 0 else s["words"][0]["start"] - 0.08
        s["t1"] = (shots[k + 1]["words"][0]["start"] - 0.08) if k + 1 < len(shots) else \
            s["words"][-1]["end"] + TAIL
    return shots


def cue_time(shot, cue):
    for w in shot["words"]:
        if _norm(w["text"]).startswith(_norm(cue)):
            return w["start"] - 0.04
    raise ValueError(f"cue {cue!r} not found in: {' '.join(w['text'] for w in shot['words'])}")


def target(shot):
    if shot["view"] == "panel":
        return shot["page"], PANELS[shot["page"]][shot["panel"]]
    if shot["view"] == "end":
        return "cover", WHOLE
    return shot.get("page", "q"), WHOLE


def frame_at(pages, shots, k, t):
    shot = shots[k]
    lt = t - shot["t0"]
    key, rect = target(shot)
    zoom = 1.0 + 0.035 * (lt / max(shot["t1"] - shot["t0"], 0.1))   # slow push
    if k > 0 and lt < MOVE:
        pkey, prect = target(shots[k - 1])
        if pkey == key:
            u = _ease(lt / MOVE)
            rect = tuple(p + (c - p) * u for p, c in zip(prect, rect))
    shake = (0, 0)
    st = cue_time(shot, shot["stamp"][1]) if shot.get("stamp") else None
    if st is not None and 0 <= t - st < 0.3:
        a = 16 * math.exp(-(t - st) * 12)
        shake = (a * math.sin((t - st) * 90), a * math.cos((t - st) * 70))

    if shot["view"] == "end":
        img = end_card(pages, shot["t0"], t, None)
    else:
        img, s, to_frame = view(pages, key, rect, zoom, shake)
        if shot["view"] == "panel":
            px0, py0, px1, py1 = PANELS[key][shot["panel"]]
            pw, ph = pages.img[key].size
            a = to_frame(px0 * pw, py0 * ph)
            b = to_frame(px1 * pw, py1 * ph)
            fade = _ease(lt / 0.35) if k == 0 or shots[k - 1]["view"] != "panel" else 1.0
            img = spotlight(img, [a[0], a[1], b[0], b[1]], fade)
            if st is not None:
                stamp(img, shot["stamp"][0], st, t, (a[0] + (b[0] - a[0]) * 0.27, (a[1] + b[1]) / 2))
        if shot["view"] == "lock":
            dim = Image.new("RGB", (W, H), (0, 0, 0))
            img = Image.blend(img, dim, 0.5 * _ease(lt / 0.3))
    # A hard cut between pages gets a quick white flash, like a feed transition.
    if k > 0 and target(shots[k - 1])[0] != key and lt < 0.1:
        img = Image.blend(img, Image.new("RGB", (W, H), (255, 255, 255)), 0.6 * (1 - lt / 0.1))
    if shot.get("box"):
        hook_box(img, shot["box"], shot["t0"] + (0 if k == 0 else 0.1), t)
    for j, (n, cue) in enumerate(zip(("3", "2", "1"), shot.get("count", []))):
        big_number(img, n, cue_time(shot, cue), t, 270 + 270 * j)
    return img


# ------------------------------------------------------------------ output

def render(angle, out_path):
    # A re-cut of an existing video reuses its narration (no new voice credits).
    cache = os.path.join(ROOT, "out", "explainer", getattr(angle, "CACHE", angle.ID))
    os.makedirs(cache, exist_ok=True)
    text = " ".join(t for t, _ in angle.SCRIPT)
    vo_path, words = voice.synthesize(text, cache)
    if vo_path:
        vo_path, words = voice.tighten(vo_path, words, cache, cap=0.2)
    shots = timeline(angle.SCRIPT, words)
    total = shots[-1]["t1"]
    pages = Pages(angle.Q, angle.A)

    video = os.path.join(cache, "comic.mp4")
    enc = subprocess.Popen(
        [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264",
         "-preset", "slow", "-crf", "20", "-pix_fmt", "yuv420p", video], stdin=subprocess.PIPE)
    k = 0
    for f in range(int(round(total * FPS))):
        t = f / FPS
        while k + 1 < len(shots) and t >= shots[k + 1]["t0"]:
            k += 1
        img = frame_at(pages, shots, k, t)
        captions(img, shots[k]["words"], t)
        enc.stdin.write(img.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg failed while encoding frames")

    wav = os.path.join(cache, "comic.wav")
    _mix(shots, total, vo_path, wav)
    done = subprocess.run(
        [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error", "-i", video, "-i", wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
         "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
         out_path], capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr[-3000:])
    return {"path": out_path, "duration": total, "voiced": vo_path is not None}


def stills(angle, out_dir):
    text = " ".join(t for t, _ in angle.SCRIPT)
    shots = timeline(angle.SCRIPT, voice.estimate(text))
    pages = Pages(angle.Q, angle.A)
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for k, s in enumerate(shots):
        t = s["t1"] - 0.05
        img = frame_at(pages, shots, k, t)
        captions(img, s["words"], s["words"][-1]["end"])
        p = os.path.join(out_dir, f"shot-{k + 1:02d}.png")
        img.save(p)
        paths.append(p)
    return paths


def _put(track, sound, at):
    start = int(at * foley.SR)
    end = min(start + len(sound), len(track))
    if end > start >= 0:
        track[start:end] += sound[:end - start]


def _mix(shots, total, vo_path, path):
    rng = np.random.default_rng(1)
    hiss = np.convolve(rng.standard_normal(int(total * foley.SR) + foley.SR), np.ones(24) / 24, "same")
    track = hiss * (10 ** (-58 / 20) / (np.sqrt(np.mean(hiss ** 2)) + 1e-12))
    for s in shots:
        if s.get("stamp"):
            _put(track, foley.sample("tape"), cue_time(s, s["stamp"][1]))
        for cue in s.get("count", []):
            _put(track, foley.sample("tap"), cue_time(s, cue))
    if vo_path:
        raw = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", vo_path, "-f", "s16le", "-ac", "1",
                              "-ar", str(foley.SR), "-"], capture_output=True, check=True).stdout
        _put(track, np.frombuffer(raw, dtype="<i2").astype(float) / 32768, 0.0)
    track = track[:int(total * foley.SR)]
    peak = np.abs(track).max()
    if peak > 0.98:
        track *= 0.98 / peak
    pcm = (np.clip(track, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(foley.SR)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())
