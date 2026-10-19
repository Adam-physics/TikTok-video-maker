"""Flat-cartoon texting skits: a character close-up cut against a phone screen.

The format the reference reels use is limited animation: the character
mostly holds a pose and only the eyes, brows and mouth change, while the
joke is carried by cuts between his face and the chat. That is cheap to
render well, so the craft goes into timing, expressions and a phone
screen that reads as real at a glance.

Everything is drawn at SS times the output size and shrunk, so flat shapes
keep clean edges.
"""
from __future__ import annotations

import math
import os
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import brand, foley
from .render import ffmpeg_bin

W, H, FPS = brand.WIDTH, brand.HEIGHT, brand.FPS
SS = 2
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
UI_FONT = "/usr/share/fonts/opentype/inter/Inter-Medium.otf"
UI_BOLD = "/usr/share/fonts/opentype/inter/Inter-SemiBold.otf"
TITLE_FONT = os.path.join(FONTS, "Montserrat-Black.ttf")
EMOJI_FONT = "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf"

INK = (8, 8, 10)
GREY = (200, 200, 202)          # the stickman's skin
NIGHT = (14, 26, 56)
BUBBLE_IN = (228, 228, 232)
BUBBLE_OUT = (22, 76, 108)      # dark teal, as the skit channels draw it
HAND = INK

_fonts: dict = {}


def font(path, size):
    key = (path, size)
    if key not in _fonts:
        _fonts[key] = ImageFont.truetype(path, size)
    return _fonts[key]


def S(*v):
    """Scale 1x layout coordinates to the supersampled canvas."""
    return [x * SS for x in v] if len(v) > 1 else v[0] * SS


def ease_out_back(u, c=1.7):
    u = min(max(u, 0.0), 1.0) - 1
    return 1 + (c + 1) * u ** 3 + c * u ** 2


def ease(u):
    u = min(max(u, 0.0), 1.0)
    return u * u * (3 - 2 * u)


# ------------------------------------------------------------------ text + emoji

def _is_emoji(ch):
    o = ord(ch)
    return o >= 0x1F000 or 0x2600 <= o <= 0x27BF or o in (0xFE0F, 0x200D)


def _runs(text):
    runs, cur, cur_e = [], "", None
    for ch in text:
        e = _is_emoji(ch)
        if cur and e != cur_e:
            runs.append((cur, cur_e))
            cur = ""
        cur, cur_e = cur + ch, e
    if cur:
        runs.append((cur, cur_e))
    return runs


_emoji_cache: dict = {}


def _emoji(ch, px):
    key = (ch, px)
    if key not in _emoji_cache:
        f = ImageFont.truetype(EMOJI_FONT, 109)
        im = Image.new("RGBA", (136, 128), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((0, 0), ch, font=f, embedded_color=True)
        im = im.crop(im.getbbox() or (0, 0, 1, 1))
        _emoji_cache[key] = im.resize((px, int(px * im.height / im.width)), Image.LANCZOS)
    return _emoji_cache[key]


def text_width(text, f):
    w = 0
    for run, is_e in _runs(text):
        if is_e:
            w += sum(int(f.size * 1.1) for c in run if c not in "️‍")
        else:
            w += f.getlength(run)
    return w


def draw_text(img, xy, text, f, fill, anchor="ls"):
    """Text with colour emoji inline; xy is the left baseline unless anchor='mm'."""
    x, y = xy
    if anchor == "mm":
        x -= text_width(text, f) / 2
        asc, desc = f.getmetrics()
        y += (asc - desc) / 2
    d = ImageDraw.Draw(img)
    for run, is_e in _runs(text):
        if is_e:
            for c in run:
                if c in "️‍":
                    continue
                em = _emoji(c, int(f.size * 1.05))
                img.alpha_composite(em, (int(x), int(y - f.size * 0.88)))
                x += f.size * 1.1
        else:
            d.text((x, y), run, font=f, fill=fill, anchor="ls")
            x += f.getlength(run)


def wrap(text, f, max_w):
    lines, cur = [], ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if text_width(trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = word
    lines.append(cur)
    return lines


# ------------------------------------------------------------------ character
#
# The round-head stickman many skit channels share: a big light-grey head
# with a heavy black outline and one hair curl, tube limbs, solid black
# oval eyes, little arched brows and a wavy mouth. The face sits toward
# whatever he is looking at, which is most of the acting.

def _tube(d, pts, w=24, o=7):
    """A limb: grey tube with a black outline."""
    pts = [tuple(S(*p)) for p in pts]
    d.line(pts, fill=INK, width=S(w + 2 * o), joint="curve")
    for p in (pts[0], pts[-1]):
        r = S(w / 2 + o)
        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=INK)
    d.line(pts, fill=GREY, width=S(w), joint="curve")
    for p in (pts[0], pts[-1]):
        r = S(w / 2)
        d.ellipse((p[0] - r, p[1] - r, p[0] + r, p[1] + r), fill=GREY)


def _phone_back(img, cx, cy, angle, buzz_dx=0.0):
    """The phone seen from behind, held up: blue-grey with a camera bump."""
    w, h = S(170), S(290)
    ph = Image.new("RGBA", (w + S(20), h + S(20)), (0, 0, 0, 0))
    pd = ImageDraw.Draw(ph)
    pd.rounded_rectangle((S(10), S(10), S(10) + w, S(10) + h), radius=S(26), fill=(104, 116, 146),
                         outline=INK, width=S(8))
    pd.rounded_rectangle((S(30), S(30), S(30) + S(64), S(30) + S(84)), radius=S(16), fill=(84, 94, 122))
    for k, (x, y) in enumerate(((48, 52), (76, 52), (48, 92))):
        pd.ellipse(S(x - 11, y - 11, x + 11, y + 11), fill=(235, 238, 245), outline=INK, width=S(3))
        pd.ellipse(S(x - 4, y - 4, x + 4, y + 4), fill=INK)
    ph = ph.rotate(angle, resample=Image.BICUBIC, expand=True)
    img.alpha_composite(ph, (int(S(cx + buzz_dx) - ph.width / 2), int(S(cy) - ph.height / 2)))


def _hand(d, cx, cy, angle, side):
    """A black silhouette hand: a palm and four short fingers wrapped round the phone."""
    a = math.radians(angle)
    d.ellipse(S(cx - 46, cy - 40, cx + 46, cy + 40), fill=INK)
    for k in range(4):
        off = -42 + k * 26
        fx = cx + side * 50 * math.cos(a) - off * math.sin(a)
        fy = cy + side * 50 * math.sin(a) + off * math.cos(a)
        d.line([tuple(S(cx, cy + off * 0.6)), tuple(S(fx, fy))], fill=INK, width=S(22))
        d.ellipse(S(fx - 11, fy - 11, fx + 11, fy + 11), fill=INK)


def stickman(img, t, mood, look="phone", buzz=0.0, blink=False, phone_up=False):
    d = ImageDraw.Draw(img)
    breathe = math.sin(t * 2.0) * 4
    hx, hy, r = 600, 760 + breathe, 250

    # body: a tube from under the head down into the blanket
    _tube(d, [(640, hy + 200), (655, 1700)], w=30)
    # far arm reaches the phone
    px, py, pa = (330, 1150, 18) if not phone_up else (420, 980, 8)
    jx = math.sin(t * 95) * 7 * buzz
    _tube(d, [(625, hy + 330), (520, 1360), (px + 40, py + 90)])
    _phone_back(img, px, py, pa, jx)
    _hand(d, px + 52 + jx, py + 95, pa, 1)
    _tube(d, [(660, hy + 330), (560, 1420), (px - 10, py + 150)])
    _hand(d, px - 50 + jx, py + 130, pa, -1)
    if buzz:
        for k in range(2):
            rr = 150 + k * 34
            d.arc(S(px - rr, py - rr, px + rr, py + rr), 200, 250, fill=(235, 240, 255), width=S(7))
            d.arc(S(px - rr, py - rr, px + rr, py + rr), 290, 340, fill=(235, 240, 255), width=S(7))

    # head
    d.ellipse(S(hx - r, hy - r, hx + r, hy + r), fill=GREY, outline=INK, width=S(11))
    d.arc(S(hx - 40, hy - r - 50, hx + 60, hy - r + 70), 160, 300, fill=INK, width=S(9))   # hair curl
    stick_face(img, hx, hy, mood, look, blink)


def stick_face(img, hx, hy, mood, look, blink):
    d = ImageDraw.Draw(img)
    # where the face sits on the head: toward the phone, or straight at us
    fx, fy = {"phone": (hx - 70, hy + 55), "camera": (hx - 10, hy + 20)}[look]
    big = mood == "shock"
    ex = 70
    erx, ery = (38, 64) if big else (28, 50)
    for side in (-1, 1):
        cx = fx + side * ex + (8 if side > 0 else 0)
        if blink:
            d.line([tuple(S(cx - 22, fy)), tuple(S(cx + 22, fy))], fill=INK, width=S(9))
            continue
        d.ellipse(S(cx - erx, fy - ery, cx + erx, fy + ery), fill=INK)
        if mood in ("bored", "smug"):                  # heavy upper lid
            lid = fy - ery * (0.05 if mood == "bored" else 0.2)
            d.rectangle(S(cx - erx - 4, fy - ery - 6, cx + erx + 4, lid), fill=GREY)
            d.line([tuple(S(cx - erx - 6, lid)), tuple(S(cx + erx + 6, lid))], fill=INK, width=S(8))
    # brows: small arcs
    for side in (-1, 1):
        cx = fx + side * ex + (8 if side > 0 else 0)
        lift = {"shock": -36, "smug": -14 if side > 0 else 6}.get(mood, 0)
        by = fy - 80 + lift
        d.arc(S(cx - 30, by - 14, cx + 30, by + 26), 205, 335, fill=INK, width=S(8))
    # mouth
    my = fy + 120
    if mood == "shock":
        d.ellipse(S(fx - 40, my - 30, fx + 44, my + 58), fill=(52, 22, 26), outline=INK, width=S(8))
    elif mood == "smug":
        d.line([tuple(S(fx - 60, my + 8)), tuple(S(fx, my + 10)), tuple(S(fx + 62, my - 16))],
               fill=INK, width=S(8), joint="curve")
    else:
        # the wavy "ugh" mouth with a little chin bump under it
        xs = np.linspace(-62, 62, 60)
        ys = my + 6 * np.sin(xs / 62 * 2 * np.pi) * (1 - (xs / 62) ** 2) - 18 * (np.abs(xs) / 62) ** 4
        d.line([tuple(S(fx + x, y)) for x, y in zip(xs, ys)], fill=INK, width=S(8), joint="curve")
        for side in (-1, 1):                                        # curled corners
            cx = fx + side * 62
            d.arc(S(cx - 14, my - 34, cx + 14, my - 8), 90 if side > 0 else 0,
                  180 if side > 0 else 90, fill=INK, width=S(7))
        d.arc(S(fx - 26, my + 10, fx + 22, my + 40), 20, 160, fill=INK, width=S(7))  # chin


def bedroom(img):
    """Flat night bedroom, no outlines: wall, headboard, pillow, blanket."""
    d = ImageDraw.Draw(img)
    d.rectangle(S(0, 0, W, H), fill=NIGHT)
    d.rectangle(S(0, 1030, W, 1250), fill=(30, 52, 98))                 # headboard
    d.rectangle(S(0, 1010, W, 1040), fill=(40, 66, 118))
    d.rounded_rectangle(S(-60, 1160, 1140, 1420), radius=S(120), fill=(66, 112, 176))   # pillow


def blanket(img):
    d = ImageDraw.Draw(img)
    pts = [(0, 1520)]
    for x in range(0, W + 1, 40):
        pts.append((x, 1500 + 34 * math.sin(x / 130) + 20 * math.sin(x / 47)))
    pts += [(W, H), (0, H)]
    d.polygon([tuple(S(*p)) for p in pts], fill=(78, 136, 204))
    pts2 = [(0, 1700)] + [(x, 1680 + 30 * math.sin(x / 110 + 1)) for x in range(0, W + 1, 40)] + [(W, H), (0, H)]
    d.polygon([tuple(S(*p)) for p in pts2], fill=(98, 156, 220))
    d.ellipse(S(-200, 1580, 520, 1780), fill=(176, 200, 238))              # sheet fold


# ------------------------------------------------------------------ phone

PX0, PY0, PX1, PY1 = 200, 300, 880, 1760          # phone body
SX0, SY0, SX1, SY1 = 222, 322, 858, 1738          # screen
KB_TOP = 1390                                     # keyboard top
INPUT_Y = 1310                                    # input bar centre


def phone_frame(img, contact, typed, cursor_on, msgs, t, typing_dots, kb_key):
    d = ImageDraw.Draw(img)
    d.rectangle(S(0, 0, W, H), fill=NIGHT)
    # the hand behind: a dark palm low on the left
    d.ellipse(S(40, 1240, 520, 2100), fill=HAND)
    d.rounded_rectangle(S(PX0, PY0, PX1, PY1), radius=S(90), fill=(14, 14, 18))
    d.rounded_rectangle(S(SX0, SY0, SX1, SY1), radius=S(72), fill=(255, 255, 255))

    # header
    d.ellipse(S(500, 360, 580, 440), fill=(180, 186, 200))
    draw_text(img, S(540, 400), contact[0], font(UI_BOLD, S(40)), (255, 255, 255), anchor="mm")
    draw_text(img, S(540, 478), contact, font(UI_FONT, S(28)), (20, 20, 24), anchor="mm")
    d.text(S(262, 410), "‹", font=font(UI_FONT, S(80)), fill=BUBBLE_OUT, anchor="lm")
    d.line([tuple(S(SX0, 510)), tuple(S(SX1, 510))], fill=(220, 220, 226), width=S(2))

    # messages, laid out bottom-up above the input bar
    chat = Image.new("RGBA", img.size, (0, 0, 0, 0))
    y = INPUT_Y - 70
    f = font(UI_FONT, S(40))
    if typing_dots is not None:
        y = _dots(chat, y, typing_dots)
    for m in reversed(msgs):
        y = _bubble(chat, y, m, t, f)
        if y < 520:
            break
    clip = Image.new("L", img.size, 0)
    ImageDraw.Draw(clip).rectangle(S(SX0, 512, SX1, INPUT_Y - 46), fill=255)
    img.paste(chat, (0, 0), Image.composite(chat.getchannel("A"), clip, clip))

    # input bar + keyboard
    d.rounded_rectangle(S(250, INPUT_Y - 38, 760, INPUT_Y + 38), radius=S(38), outline=(205, 205, 212),
                        width=S(3), fill=(255, 255, 255))
    fi = font(UI_FONT, S(34))
    if typed:
        draw_text(img, S(280, INPUT_Y + 12), typed, fi, (20, 20, 24))
        cx = 280 + text_width(typed, fi) / SS + 4
    else:
        d.text(S(280, INPUT_Y + 12), "Message", font=fi, fill=(170, 170, 178),
               anchor="ls")
        cx = 280
    if cursor_on:
        d.line([tuple(S(cx, INPUT_Y - 22)), tuple(S(cx, INPUT_Y + 22))], fill=BUBBLE_OUT, width=S(4))
    d.ellipse(S(774, INPUT_Y - 34, 842, INPUT_Y + 34),
              fill=BUBBLE_OUT if typed else (205, 205, 212))
    d.text(S(808, INPUT_Y + 2), "↑", font=font(UI_BOLD, S(44)), fill=(255, 255, 255), anchor="mm")
    _keyboard(img, kb_key)

    # thumb and fingers over the edges, like a real grip
    d.rounded_rectangle(S(90, 1600, 290, 1690), radius=S(45), fill=HAND)      # thumb on the edge
    for k in range(4):
        y0 = 900 + k * 150
        d.rounded_rectangle(S(842, y0, 960, y0 + 110), radius=S(55), fill=HAND)


def _keyboard(img, active):
    d = ImageDraw.Draw(img)
    d.rectangle(S(SX0, KB_TOP, SX1, SY1 - 60), fill=(209, 212, 219))
    d.rounded_rectangle(S(SX0, KB_TOP, SX1, SY1), radius=S(72), fill=(209, 212, 219))
    rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    kw, kh, gap = 52, 72, 8
    f = font(UI_FONT, S(30))
    for r, row in enumerate(rows):
        n = len(row)
        x0 = 540 - (n * kw + (n - 1) * gap) / 2
        y0 = KB_TOP + 18 + r * (kh + 14)
        for i, ch in enumerate(row):
            x = x0 + i * (kw + gap)
            on = ch == active
            d.rounded_rectangle(S(x, y0 - (16 if on else 0), x + kw, y0 + kh), radius=S(10),
                                fill=(255, 255, 255) if not on else (245, 245, 250))
            d.text(S(x + kw / 2, y0 + kh / 2 - (14 if on else 0)), ch, font=f, fill=(20, 20, 24),
                   anchor="mm")
    y0 = KB_TOP + 18 + 3 * (kh + 14)
    d.rounded_rectangle(S(330, y0, 750, y0 + kh), radius=S(10), fill=(255, 255, 255))


def _bubble(img, y_bottom, m, t, f):
    """Draw one message ending at y_bottom; return the y above it."""
    kind, at = m["kind"], m["at"]
    if t < at:
        return y_bottom
    u = (t - at) / 0.22
    sc = ease_out_back(u) if u < 1 else 1.0
    out = kind == "out"
    max_w = 450
    if kind == "img":
        im = m["image"]
        bw, bh = im.width / SS, im.height / SS
        layer = Image.new("RGBA", (S(int(bw) + 4), S(int(bh) + 4)), (0, 0, 0, 0))
        mask = Image.new("L", im.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle((0, 0, im.width, im.height), radius=S(28), fill=255)
        layer.paste(im, (0, 0), mask)
        _place(img, layer, (SX0 + 30, y_bottom - bh), sc, "left")
        return y_bottom - bh - 14
    lines = wrap(m["text"], f, S(max_w))
    lh = 52
    tw = max(text_width(ln, f) for ln in lines) / SS
    bw, bh = tw + 52, lh * len(lines) + 34
    layer = Image.new("RGBA", (S(int(bw) + 2), S(int(bh) + 2)), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle((0, 0, S(bw), S(bh)), radius=S(36), fill=BUBBLE_OUT if out else BUBBLE_IN)
    for i, ln in enumerate(lines):
        draw_text(layer, (S(26), S(17 + lh * i + 36)), ln, f,
                  (255, 255, 255) if out else (20, 20, 24))
    x = SX1 - 26 - bw if out else SX0 + 26
    _place(img, layer, (x, y_bottom - bh), sc, "right" if out else "left")
    return y_bottom - bh - 12


def _place(img, layer, xy, sc, side):
    x, y = xy
    if sc < 0.999:
        w0, h0 = layer.size
        layer = layer.resize((max(1, int(w0 * sc)), max(1, int(h0 * sc))), Image.BILINEAR)
        if side == "right":
            x += (w0 - layer.width) / SS
        y += (h0 - layer.height) / SS
    img.alpha_composite(layer, (int(S(x)), int(S(y))))


def _dots(img, y_bottom, phase):
    d = ImageDraw.Draw(img)
    bw, bh = 130, 74
    x = SX0 + 26
    d.rounded_rectangle(S(x, y_bottom - bh, x + bw, y_bottom), radius=S(36), fill=BUBBLE_IN)
    for k in range(3):
        a = 0.45 + 0.55 * max(0, math.sin(phase * 7 - k * 0.9))
        g = int(150 - 60 * a)
        cy = y_bottom - bh / 2 - 6 * a
        cx = x + 34 + k * 31
        d.ellipse(S(cx - 10, cy - 10, cx + 10, cy + 10), fill=(g, g, g + 6))
    return y_bottom - bh - 12


# ------------------------------------------------------------------ the skit

def answer_crop():
    """The polar-bear reveal panel from the book's answer page."""
    pg = Image.open(os.path.join(ROOT, "assets", "pages", "a01.png")).convert("RGBA")
    panel = pg.crop((58, 812, 1266, 1276))
    w = S(470)
    return panel.resize((w, int(panel.height * w / panel.width)), Image.LANCZOS)


CAPTION = "POV: you lose trivia to your 8-year-old \U0001F62D"
CONTACT = "Lily"

SHOTS = [                          # (kind, start, end, options)
    ("dad", 0.0, 2.0, {"mood": "bored", "buzz": (0.6, 1.3)}),
    ("phone", 2.0, 5.6, {}),
    ("dad", 5.6, 6.9, {"mood": "smug", "look": "camera"}),
    ("phone", 6.9, 10.4, {}),
    ("dad", 10.4, 12.5, {"mood": "neutral", "shock_at": 10.75}),
    ("phone", 12.5, 16.4, {}),
    ("end", 16.4, 19.0, {}),
]

MSGS = [
    {"kind": "in", "at": 2.25, "text": "dad"},
    {"kind": "in", "at": 2.65, "text": "polar bear fur isn't white"},
    {"kind": "out", "at": 4.85, "text": "yes it is \U0001F644"},
    {"kind": "img", "at": 8.05},
    {"kind": "in", "at": 8.95, "text": "page 2 \U0001F60F"},
    {"kind": "out", "at": 14.0, "text": "how do u know that"},
    {"kind": "in", "at": 15.5, "text": "it's in my trick trivia book \U0001F996"},
]

TYPING = [                          # (start, end, text, sent_at)
    (3.25, 4.55, "yes it is \U0001F644", 4.85),
    (12.75, 13.75, "how do u know that", 14.0),
]
DOTS = [(7.05, 8.0), (14.35, 15.45)]


def _typed(t):
    for a, b, text, sent in TYPING:
        if a <= t < sent:
            n = int(len(text) * min(1.0, (t - a) / (b - a)))
            return text[:n], (text[n - 1] if 0 < n <= len(text) and t < b else "")
    return "", ""


def _caption(img):
    f = font(TITLE_FONT, S(40))
    tw = text_width(CAPTION, f) / SS
    x0 = (W - tw) / 2 - 30
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(S(x0, 140, x0 + tw + 60, 222), radius=S(41), fill=(0, 0, 0, 255))
    draw_text(img, S(540, 183), CAPTION, f, (255, 255, 255), anchor="mm")


def _camera(img, zoom, cx=540, cy=900):
    if abs(zoom - 1) < 1e-3:
        return img
    w, h = img.size
    cw, ch = w / zoom, h / zoom
    x0 = min(max(S(cx) - cw / 2, 0), w - cw)
    y0 = min(max(S(cy) - ch / 2, 0), h - ch)
    return img.crop((int(x0), int(y0), int(x0 + cw), int(y0 + ch))).resize((w, h), Image.BILINEAR)


def frame(t, crop_img, cover):
    kind, a, b, opt = next(s for s in SHOTS if s[1] <= t < s[2]) if t < SHOTS[-1][2] else SHOTS[-1]
    img = Image.new("RGBA", (W * SS, H * SS), (*NIGHT, 255))
    lt = t - a
    if kind == "dad":
        bedroom(img)
        mood, look = opt.get("mood", "bored"), opt.get("look", "phone")
        zoom = 1.2 + 0.04 * ease(lt / (b - a))      # framed close, like the reference
        sh = opt.get("shock_at")
        if sh and t >= sh:
            mood, look = "shock", "camera"
            zoom = 1.24 + 0.14 * ease((t - sh) / 0.14)
        bz = opt.get("buzz")
        buzz = 1.0 if bz and bz[0] <= t < bz[1] else 0.0
        blink = (lt % 2.3) < 0.11 and mood != "shock"
        stickman(img, t, mood, look, buzz, blink)
        blanket(img)
        img = _camera(img, zoom, 540, 1000)
    elif kind == "phone":
        typed, key = _typed(t)
        dots = next((t for x, y in DOTS if x <= t < y), None)
        msgs = [m if m["kind"] != "img" else {**m, "image": crop_img} for m in MSGS]
        phone_frame(img, CONTACT, typed, (t * 2) % 1 < 0.5, msgs, t, dots, key)
        img = _camera(img, 1.0 + 0.03 * ease(lt / (b - a)), 540, 1000)
    else:
        img.paste((*NIGHT, 255), (0, 0, img.width, img.height))
        u = ease_out_back(lt / 0.35)
        cw = int(S(520) * u)
        if cw > 4:
            c = cover.resize((cw, int(cover.height * cw / cover.width)), Image.LANCZOS)
            img.alpha_composite(c, (img.width // 2 - c.width // 2, S(330) + (S(780) - c.height) // 2))
        d = ImageDraw.Draw(img)
        if lt > 0.4:
            d.text(S(540, 1310), "Trick Trivia: Real or Fake?", font=font(TITLE_FONT, S(60)),
                   fill=(255, 255, 255), anchor="mm")
        if lt > 0.7:
            d.rounded_rectangle(S(300, 1390, 780, 1490), radius=S(50), fill=brand.YELLOW)
            d.text(S(540, 1441), "Search it on Amazon", font=font(TITLE_FONT, S(38)),
                   fill=(20, 20, 24), anchor="mm")
    _caption(img)
    return img.reduce(SS).convert("RGB")


def mix(total, path):
    track = np.zeros(int(total * foley.SR) + foley.SR)
    rng = np.random.default_rng(2)
    hiss = np.convolve(rng.standard_normal(len(track)), np.ones(24) / 24, mode="same")
    track += hiss * (10 ** (-58 / 20) / (np.sqrt(np.mean(hiss ** 2)) + 1e-12))
    levels = {"msg_in": -24.0, "msg_out": -24.0, "typing": -30.0, "buzz": -26.0}
    foley.LEVELS.update(levels)

    def put(name, at, dur=None):
        s = foley.sample(name)
        if dur:
            s = s[:int(dur * foley.SR)].copy()
            fade = min(len(s) // 2, int(0.03 * foley.SR))
            s[-fade:] *= np.linspace(1, 0, fade)
        i = int(at * foley.SR)
        track[i:i + len(s)] += s[:len(track) - i]

    put("buzz", 0.6)
    for m in MSGS:
        put("msg_out" if m["kind"] == "out" else "msg_in", m["at"])
    for a, b, _, _ in TYPING:
        put("typing", a, b - a)
    peak = np.abs(track).max()
    if peak > 0.98:
        track *= 0.98 / peak
    pcm = (np.clip(track[:int(total * foley.SR)], -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(foley.SR)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())


def render(out_path):
    cache = os.path.join(ROOT, "out", "skit")
    os.makedirs(cache, exist_ok=True)
    total = SHOTS[-1][2]
    crop_img = answer_crop()
    cover = Image.open(os.path.join(ROOT, "assets", "cover.png")).convert("RGBA")
    video = os.path.join(cache, "video.mp4")
    enc = subprocess.Popen(
        [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error", "-f", "rawvideo",
         "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
         "-c:v", "libx264", "-preset", "slow", "-crf", "14", "-tune", "animation",
         "-pix_fmt", "yuv420p", video], stdin=subprocess.PIPE)
    for i in range(int(total * FPS)):
        enc.stdin.write(frame(i / FPS, crop_img, cover).tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg failed while encoding frames")
    wav = os.path.join(cache, "mix.wav")
    mix(total, wav)
    done = subprocess.run(
        [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error", "-i", video, "-i", wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
         "-ar", "48000", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart",
         out_path], capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr[-3000:])
    return out_path
