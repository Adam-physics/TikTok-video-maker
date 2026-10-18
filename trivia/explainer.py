"""The parent-value doodle explainer: why a parent should buy Trick Trivia.

The book's audience on TikTok is the adult with the wallet, so the video
sells to them, in the order a parent decides:

1. Hook with a fact the parent gets wrong (polar bear fur). They play
   before they know it is an ad.
2. Name the feeling: the "NO WAY!" face. That is the product.
3. How it works in one breath.
4. The three reasons parents buy: screen-free, sneaky learning, anywhere.
5. Proof of substance (the real full-colour page), then the ask.

Doodles carry the argument; the only full-colour image is the book itself,
so it lands as the payoff rather than one more picture.
"""
from __future__ import annotations

import math
import os
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

from . import audio, brand, voice
from .doodle import (HAND, INK, MARKER, Picture, Shape, Text, arc, arrow, check, circle,
                     curve, ellipse, font, heart, line, paint_pen, paper, poly, rrect,
                     stamp, star)
from .render import ffmpeg_bin

W, H, FPS = brand.WIDTH, brand.HEIGHT, brand.FPS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSITION = 0.30
CAPTION_Y = 1395
TAIL = 1.4              # hold on the last frame after the voice ends

ORANGE, BLUE, GREEN, RED = brand.ORANGE_DEEP, brand.BLUE, brand.GREEN, brand.RED
YELLOW = brand.YELLOW
FUR, SKIN = (238, 243, 250), (255, 222, 190)


def headline(text, y=330, size=92, color=INK):
    return Text(text, (W / 2, y), size=size, color=color, face=MARKER)


def row(parts, y, size=110, face=MARKER, gap=26):
    """Several differently coloured words on one line, each its own item."""
    f = font(face, size)
    widths = [f.getlength(t) for t, _ in parts]
    x = (W - sum(widths) - gap * (len(parts) - 1)) / 2
    out = []
    for (t, c), w in zip(parts, widths):
        out.append(Text(t, (x, y), size=size, color=c, face=face, anchor="lm"))
        x += w + gap
    return out


def tube(p0, p1, r, seed=0):
    """A hollow hair: two walls and an open end you can see into."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = (p1 - p0) / np.hypot(*(p1 - p0))
    n = np.array([-d[1], d[0]]) * r
    ang = math.degrees(math.atan2(d[1], d[0]))
    return [line(p0 + n, p1 + n, seed=seed), line(p0 - n, p1 - n, seed=seed + 1),
            ellipse(*p1, r * 0.42, r, rot=ang, wobble=0.8, seed=seed),
            ellipse(*p1, r * 0.2, r * 0.55, rot=ang, wobble=0.5, seed=seed + 2),
            arc(*p0, r * 0.42, r, 90, 270, rot=ang, wobble=0.8, seed=seed)]


def snowflake(cx, cy, r, seed=0):
    return [line((cx + r * math.cos(a), cy + r * math.sin(a)),
                 (cx - r * math.cos(a), cy - r * math.sin(a)), wobble=0.6, seed=seed + k)
            for k, a in enumerate((0, math.pi / 3, 2 * math.pi / 3))]


def bumpy(cx, cy, rx, ry, bumps=11, depth=0.09, seed=0):
    t = np.linspace(0, 2 * math.pi, 220)
    r = 1 + depth * np.abs(np.sin(t * bumps / 2))
    pts = np.stack([cx + rx * r * np.cos(t), cy + ry * r * np.sin(t)], axis=1)
    return poly(pts, wobble=1.6, seed=seed)


def tilted_square(cx, cy, s, angle, seed=0):
    a = math.radians(angle)
    pts = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a))
           for x, y in ((-s, -s), (s, -s), (s, s), (-s, s))]
    return poly(pts, closed=True, wobble=1.0, seed=seed)


def crescent(cx, cy, r, seed=0):
    outer = [(cx + r * math.cos(a), cy + r * math.sin(a))
             for a in np.radians(np.linspace(55, 305, 40))]
    ix = cx + r * 0.55
    inner = [(ix + r * 0.8 * math.cos(a), cy + r * 0.8 * math.sin(a))
             for a in np.radians(np.linspace(262, 98, 30))]
    return poly(outer + inner, closed=True, wobble=1.0, seed=seed)


def pip(cx, cy, angle, dx, dy):
    a = math.radians(angle)
    return cx + dx * math.cos(a) - dy * math.sin(a), cy + dx * math.sin(a) + dy * math.cos(a)


def page(name):
    return Image.open(os.path.join(ROOT, "assets", "pages", name))


# ------------------------------------------------------------------ scenes
#
# Each scene: what the narrator says, and what the pen draws while they say
# it. `.at(word)` pins an item to the moment that word is spoken.

def s_hook():
    return [
        *row([("REAL", GREEN), ("or", INK), ("FAKE?", RED)], 340),
        Shape(ellipse(540, 935, 225, 140), fill=FUR),
        Shape([circle(425, 560, 46), circle(655, 560, 46)], fill=FUR),
        Shape(circle(540, 680, 160), fill=FUR),
        Shape([circle(485, 645, 12, wobble=0.5), circle(595, 645, 12, wobble=0.5)],
              fill=INK, width=6),
        Shape(ellipse(540, 735, 72, 52), fill=(250, 250, 252)),
        Shape(ellipse(540, 708, 26, 17), fill=INK, width=6),
        Shape(curve([(505, 758), (540, 774), (575, 758)])),
        Shape([ellipse(425, 1070, 70, 36), ellipse(655, 1070, 70, 36)], fill=FUR),
        Text("white fur?", (880, 815), size=74, color=BLUE).at("fur"),
        Shape(arrow((850, 865), (735, 935), bend=-25, head=26), color=BLUE, width=8),
        Text("?", (870, 560), size=230, color=RED, face=MARKER).at("white", "pop"),
    ]


def s_reveal():
    return [
        Picture(stamp("FAKE!", RED, size=150), (540, 360)).at("fake", "buzz"),
        Shape(circle(450, 780, 215), width=14, fill=(226, 240, 252)),
        Shape(line((610, 935), (780, 1110)), width=36),
        Shape(tube((320, 830), (550, 650), 28, seed=1), color=(70, 110, 160), width=7),
        Shape(tube((390, 915), (600, 755), 28, seed=5), color=(70, 110, 160), width=7),
        Shape(arc(450, 780, 170, 170, 200, 250), color=(255, 255, 255), width=10),
        Text("see-through", (840, 600), size=70, color=BLUE).at("see-through"),
        Shape(arrow((780, 645), (600, 690), bend=20), color=BLUE, width=8),
        Text("& hollow!", (850, 790), size=70, color=BLUE).at("hollow", "pop"),
        Shape(arrow((790, 830), (615, 790), bend=-20), color=BLUE, width=8),
        Shape(snowflake(880, 1010, 42, seed=3), color=(110, 160, 220), width=7).at("reflects"),
        Shape(snowflake(170, 1110, 32, seed=7), color=(110, 160, 220), width=7),
        Shape(snowflake(960, 1160, 26, seed=9), color=(110, 160, 220), width=7),
        Text("it reflects the snow", (540, 1215), size=72),
    ]


def s_noway():
    return [
        Shape(circle(540, 840, 225), fill=SKIN),
        Shape(poly([(318, 800), (322, 690), (372, 625), (418, 650), (450, 590), (500, 625),
                    (540, 575), (585, 620), (632, 588), (665, 640), (712, 628), (752, 700),
                    (762, 800), (705, 712), (620, 692), (540, 680), (455, 690), (380, 722)],
                   closed=True), fill=(120, 76, 44)),
        Shape([circle(462, 830, 54), circle(618, 830, 54)], fill=(255, 255, 255)),
        Shape([circle(466, 840, 20), circle(614, 840, 20)], fill=INK, width=6),
        Shape([curve([(410, 752), (460, 726), (510, 748)]),
               curve([(570, 748), (620, 726), (670, 752)])], width=10),
        Shape(ellipse(540, 965, 52, 66), fill=(150, 35, 45)),
        Shape([ellipse(400, 930, 34, 20), ellipse(680, 930, 34, 20)], fill=(255, 170, 160),
              width=4, color=(240, 150, 140)),
        Shape([line((270, 640), (230, 600)), line((250, 700), (195, 690)),
               line((810, 640), (850, 600)), line((830, 700), (885, 690))], width=8),
        Shape([rrect(560, 300, 1020, 470, r=60), poly([(640, 466), (620, 540), (700, 468)])],
              fill=(255, 255, 255), fill_offset=(0, 0)).at("no"),
        Text("NO WAY!", (790, 388), size=104, color=ORANGE, face=MARKER),
        Text("= Trick Trivia", (540, 1205), size=88, color=BLUE, face=MARKER).at("trick"),
    ]


def s_how():
    items = [headline("3 wild claims a page", 340, size=84).at("every")]
    xs = (205, 540, 875)
    for i, x in enumerate(xs):
        items.append(Shape(rrect(x - 148, 470, x + 148, 900, r=30), fill=(255, 246, 222)))
        items.append(Text("?", (x, 600), size=150, color=ORANGE, face=MARKER))
    items += [
        Shape(check(xs[0], 800, 52), color=GREEN, width=18).at("real", "ding"),
        Text("REAL", (xs[0], 980), size=76, color=GREEN, face=MARKER),
        Shape([line((xs[1] - 45, 760), (xs[1] + 45, 845)),
               line((xs[1] + 45, 760), (xs[1] - 45, 845))], color=RED, width=18).at("fake", "buzz"),
        Text("FAKE", (xs[1], 980), size=76, color=RED, face=MARKER),
        Shape(check(xs[2], 800, 52), color=GREEN, width=18).at("family", "ding"),
        Text("REAL", (xs[2], 980), size=76, color=GREEN, face=MARKER),
        Text("can your family tell?", (540, 1170), size=80).at("guess"),
    ]
    return items


def s_screens():
    return [
        headline("Screen-free fun", 340),
        Shape(rrect(130, 500, 480, 1060, r=40), fill=(70, 78, 96)),
        Shape(rrect(165, 545, 445, 990, r=14), fill=(150, 205, 255), fill_offset=(0, 0)),
        Shape(circle(305, 1025, 12)),
        Shape([poly([(560, 700), (770, 740), (770, 980), (560, 940)], closed=True),
               poly([(770, 740), (980, 700), (980, 940), (770, 980)], closed=True)],
              fill=(255, 255, 255), fill_offset=(0, 0)).at("actually"),
        Shape([line((600, 770), (730, 790)), line((600, 815), (730, 835)),
               line((600, 860), (700, 875)), line((810, 790), (940, 770)),
               line((810, 835), (940, 815)), line((810, 880), (910, 865))],
              color=(150, 150, 160), width=6),
        Shape([heart(700, 590, 42), heart(840, 560, 54)], color=RED, fill=(240, 80, 80),
              width=7).at("pick", "pop"),
        Text("they pick THIS", (775, 1080), size=74, color=BLUE),
        Shape([line((110, 520), (500, 1040)), line((500, 520), (110, 1040))],
              color=RED, width=24).at("tablet", "buzz"),
    ]


def s_learning():
    return [
        headline("Sneaky learning", 340),
        Shape(bumpy(520, 790, 290, 205, seed=2), fill=(255, 196, 206)),
        Shape([curve([(520, 610), (490, 690), (550, 770), (500, 860), (530, 960)]),
               curve([(330, 760), (390, 720), (430, 790)]),
               curve([(640, 700), (700, 740), (690, 820)]),
               curve([(360, 880), (420, 900), (450, 860)]),
               curve([(600, 900), (660, 930), (720, 880)])], width=7),
        Text("critical thinking", (290, 1100), size=70, color=BLUE).at("critical"),
        Shape([circle(890, 545, 64), rrect(860, 605, 920, 660, r=8)], fill=YELLOW).at("thinking", "ding"),
        Shape([line((890, 440), (890, 410)), line((975, 480), (1000, 460)),
               line((805, 480), (780, 460)), line((990, 560), (1020, 565))], width=7),
        Text("reading skills", (800, 1100), size=70, color=BLUE).at("reading"),
        Text("(they won't even notice)", (540, 1215), size=68).at("without"),
    ]


def s_anywhere():
    return [
        headline("Fun anywhere", 340),
        Shape([rrect(140, 520, 460, 620, r=26), poly([(200, 522), (245, 452), (370, 452), (410, 522)])],
              fill=(110, 170, 235)).at("car"),
        Shape([line((308, 455), (308, 520)), circle(215, 628, 34), circle(385, 628, 34)],
              fill=INK, width=8),
        Text("car rides", (720, 560), size=82),
        Shape(crescent(270, 830, 72), color=(200, 140, 10), fill=YELLOW,
              width=8).at("sleepovers"),
        Shape([star(380, 770, 26, seed=1), star(160, 900, 18, seed=2)], color=(220, 160, 20),
              fill=YELLOW, width=6),
        Text("sleepovers", (720, 830), size=82),
        Shape([tilted_square(230, 1080, 58, 10, seed=1), tilted_square(380, 1100, 50, -14, seed=2)],
              fill=(255, 255, 255)).at("game"),
        Shape([circle(*pip(230, 1080, 10, dx, dy), 7, wobble=0.3)
               for dx, dy in ((-28, -28), (0, 0), (28, 28))]
              + [circle(*pip(380, 1100, -14, dx, dy), 7, wobble=0.3)
                 for dx, dy in ((-24, -24), (24, -24), (-24, 24), (24, 24))],
              fill=INK, width=4),
        Text("game night", (720, 1095), size=82),
    ]


def s_inside():
    q = page("q01.png")
    return [
        headline("What's inside", 340),
        Picture(q, (310, 820), width=450, angle=4).at("120", "pop"),
        Shape([poly([(150, 470), (250, 450), (258, 495), (158, 515)], closed=True),
               poly([(400, 1160), (500, 1140), (508, 1185), (408, 1205)], closed=True)],
              color=(200, 170, 60), fill=(255, 220, 110), width=4),
        Shape(check(615, 590, 26), color=GREEN, width=12).at("120"),
        Text("120 real facts", (660, 590), size=66, anchor="lm", max_width=420),
        Shape(check(615, 730, 26), color=GREEN, width=12).at("10"),
        Text("10 wild rounds", (660, 730), size=66, anchor="lm", max_width=420),
        Shape(check(615, 870, 26), color=GREEN, width=12).at("printables"),
        Text("free printables", (660, 870), size=66, anchor="lm", max_width=420),
        Shape(check(615, 1010, 26), color=GREEN, width=12).at("online"),
        Text("online game", (660, 1010), size=66, anchor="lm", max_width=420),
    ]


def s_cta():
    return [
        Text("TRICK TRIVIA!", (540, 330), size=118, color=brand.ORANGE, face=MARKER,
             stroke=6, stroke_color=INK),
        Text("Real or Fake?", (540, 450), size=80),
        Picture(page("a01.png"), (650, 805), width=360, angle=-7),
        Picture(page("q01.png"), (420, 790), width=360, angle=6),
        Text("Grab it on Amazon", (540, 1160), size=84, color=BLUE, face=MARKER).at("amazon", "ding"),
        Text("link in bio", (540, 1255), size=70),
    ]


SCRIPT = [
    ("Real or fake? A polar bear's fur is white.", s_hook),
    ("Fake! It's see-through, and hollow. It just looks white because it reflects the snow.", s_reveal),
    ("Picture your kid's face finding that out. That \"no way!\" moment? That's Trick Trivia.", s_noway),
    ("Every page: three wild claims. Some real, some fake, and your whole family guesses.", s_how),
    ("It's screen-free fun they'll actually pick over the tablet.", s_screens),
    ("And it builds critical thinking and reading skills, without them noticing.", s_learning),
    ("Perfect for car rides, sleepovers, and family game night.", s_anywhere),
    ("120 verified facts, 10 wild rounds, free printables, and an online game.", s_inside),
    ("Grab Trick Trivia on Amazon, and let the \"no way!\" moments begin!", s_cta),
]


# ------------------------------------------------------------------ timing

def _norm(w: str) -> str:
    return re.sub(r"[^\w-]", "", w.lower())


def timeline(words: list[dict], voiced: bool):
    """Split the narration's words into scenes and give each a duration."""
    scenes, i, clock = [], 0, 0.0
    counts = [len(text.split()) for text, _ in SCRIPT]
    if len(words) != sum(counts):
        raise RuntimeError(f"narration has {len(words)} words, script has {sum(counts)}")
    starts = []
    for n in counts:
        starts.append(0.0 if i == 0 else words[i]["start"] - 0.12)
        i += n
    end = words[-1]["end"] + TAIL
    i = 0
    for k, ((text, build), n) in enumerate(zip(SCRIPT, counts)):
        t0 = starts[k]
        t1 = starts[k + 1] if k + 1 < len(starts) else end
        local = [{**w, "start": w["start"] - t0, "end": w["end"] - t0} for w in words[i:i + n]]
        scenes.append({"t0": t0, "duration": t1 - t0, "words": local, "items": build()})
        i += n
    return scenes


def schedule(scene: dict) -> None:
    """Give every item a start time inside the scene.

    Items pinned to a word split the scene into segments. Each segment is
    drawn between its own cue and the next one, sped up if it would not
    otherwise finish -- so a stamp never lands on a drawing that is not
    there yet.
    """
    items, words, dur = scene["items"], scene["words"], scene["duration"]
    lead = TRANSITION if scene["t0"] > 0 else 0.05

    cues, used = {}, 0
    for n, it in enumerate(items):
        if it.cue:
            for j in range(used, len(words)):
                if _norm(words[j]["text"]).startswith(_norm(it.cue)):
                    cues[n] = max(lead, words[j]["start"] - 0.06)
                    used = j + 1
                    break

    bounds = [0] + sorted(cues) + [len(items)]
    clock = lead
    for a, b in zip(bounds[:-1], bounds[1:]):
        if a == b:
            continue
        begin = max(clock, cues.get(a, clock))
        deadline = cues.get(b, dur - 0.35) - 0.05 if b < len(items) else dur - 0.35
        seg = items[a:b]
        natural = sum(it.duration for it in seg) + 0.04 * len(seg)
        room = deadline - begin
        if natural > room:
            squeeze = max(room, 0.12 * len(seg)) / natural
            for it in seg:
                it.duration = max(0.1, it.duration * squeeze)
        t = begin
        for it in seg:
            it.start = t
            t += it.duration + 0.04
        clock = t


# ------------------------------------------------------------------ frames

def _caption_groups(words):
    groups, cur = [], []
    for w in words:
        cur.append(w)
        if len(cur) == 3 or w["text"][-1] in ".,!?":
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    return groups


def paint_caption(img: Image.Image, words, t: float) -> None:
    group = None
    for g in _caption_groups(words):
        if g[0]["start"] - 0.05 <= t <= g[-1]["end"] + 0.25:
            group = g
    if not group:
        return
    f = font(MARKER, 70)
    texts = [w["text"].strip('"').upper() for w in group]
    space = f.getlength(" ")
    widths = [f.getlength(s) for s in texts]
    x = (W - sum(widths) - space * (len(texts) - 1)) / 2
    d = ImageDraw.Draw(img, "RGBA")
    for w, s, wd in zip(group, texts, widths):
        active = w["start"] - 0.03 <= t <= w["end"] + 0.05 or (
            w is group[-1] and t > w["end"])
        if active:
            d.rounded_rectangle([x - 12, CAPTION_Y - 48, x + wd + 12, CAPTION_Y + 46],
                                radius=16, fill=(*YELLOW, 235))
        d.text((x, CAPTION_Y), s, font=f, fill=INK, anchor="lm",
               stroke_width=0 if active else 3, stroke_fill=(255, 255, 255))
        x += wd + space


def scene_frame(base: Image.Image, scene: dict, t: float, frame: int) -> Image.Image:
    img = base.copy()
    boil = frame // 4
    pen = None
    for it in scene["items"]:
        it.paint(img, t, boil)
        tip = it.tip(t)
        if tip is not None:
            pen = tip
    if pen is not None:
        paint_pen(img, pen)
    return img


def render(out_path: str, words_override=None) -> dict:
    cache = os.path.join(ROOT, "out", "explainer")
    os.makedirs(cache, exist_ok=True)
    text = " ".join(t for t, _ in SCRIPT)
    vo_path, words = voice.synthesize(text, cache)
    scenes = timeline(words, voiced=vo_path is not None)
    for s in scenes:
        schedule(s)
    total = scenes[-1]["t0"] + scenes[-1]["duration"]

    base = paper()
    cmd = [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18",
           "-pix_fmt", "yuv420p", os.path.join(cache, "video.mp4")]
    enc = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n_frames = int(round(total * FPS))
    prev_last = None
    k = 0
    for f in range(n_frames):
        t = f / FPS
        while k + 1 < len(scenes) and t >= scenes[k + 1]["t0"]:
            prev_last = scene_frame(base, scenes[k], scenes[k]["duration"], f)
            k += 1
        s = scenes[k]
        lt = t - s["t0"]
        img = scene_frame(base, s, lt, f)
        if prev_last is not None and lt < TRANSITION:
            u = lt / TRANSITION
            e = 1 - (1 - u) ** 3
            frame_img = Image.new("RGBA", (W, H))
            frame_img.paste(prev_last, (int(-e * W), 0))
            frame_img.paste(img, (int(W - e * W), 0))
            img = frame_img
        paint_caption(img, s["words"], lt)
        enc.stdin.write(img.convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg failed while encoding frames")

    wav = os.path.join(cache, "mix.wav")
    mix(scenes, total, vo_path, wav)
    done = subprocess.run(
        [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error",
         "-i", os.path.join(cache, "video.mp4"), "-i", wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", out_path],
        capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr[-3000:])
    return {"path": out_path, "duration": total, "voiced": vo_path is not None,
            "scenes": scenes}


# ------------------------------------------------------------------ sound

def _pop() -> np.ndarray:
    n = int(0.12 * audio.SR)
    t = np.arange(n) / audio.SR
    f = 900 * np.exp(-t * 18) + 220
    return np.sin(2 * np.pi * np.cumsum(f) / audio.SR) * np.exp(-t * 30)


def _scribble(dur: float, seed: int) -> np.ndarray:
    """Marker-on-paper: filtered noise with a stroke rhythm."""
    n = int(dur * audio.SR)
    rng = np.random.default_rng(seed)
    x = rng.standard_normal(n)
    x = np.diff(np.concatenate([[0], x]))             # tilt toward hiss
    t = np.arange(n) / audio.SR
    am = 0.55 + 0.45 * np.sin(2 * np.pi * rng.uniform(5, 8) * t) ** 2
    fade = np.minimum(1, np.minimum(t, dur - t) / 0.03).clip(0, 1)
    return x * am * fade * 0.05


def _read_voice(path: str) -> np.ndarray:
    raw = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", path, "-f", "s16le",
                          "-ac", "1", "-ar", str(audio.SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<i2").astype(float) / 32768


def mix(scenes, total, vo_path, path):
    bed = audio._bed(total)[:int(total * audio.SR)]
    track = bed * (0.45 if vo_path else 1.0)
    effects = {"whoosh": audio.whoosh, "ding": audio.ding, "buzz": audio.buzz, "pop": _pop}
    for k, s in enumerate(scenes):
        if k:
            audio._mix(track, audio.whoosh() * 0.30, s["t0"])
        for j, it in enumerate(s["items"]):
            at = s["t0"] + it.start
            if it.sound:
                audio._mix(track, effects[it.sound]() * audio.SFX_GAIN, at)
            if it.scribble and it.duration > 0.12:
                audio._mix(track, _scribble(it.duration, k * 100 + j), at)
    if vo_path:
        audio._mix(track, _read_voice(vo_path), 0.0)
    peak = np.abs(track).max()
    if peak > 0.95:
        track = np.tanh(track / peak * 1.4) * 0.92
    pcm = (np.clip(track, -1, 1) * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(audio.SR)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())
    return path


def stills(out_dir: str) -> list[str]:
    """The last frame of every scene, for checking layout by eye."""
    text = " ".join(t for t, _ in SCRIPT)
    scenes = timeline(voice.estimate(text), voiced=False)
    base, paths = paper(), []
    os.makedirs(out_dir, exist_ok=True)
    for k, s in enumerate(scenes):
        schedule(s)
        img = scene_frame(base, s, s["duration"] - 0.05, 0)
        paint_caption(img, s["words"], s["words"][-1]["end"])
        p = os.path.join(out_dir, f"scene-{k + 1:02d}.png")
        img.convert("RGB").save(p)
        paths.append(p)
    return paths
