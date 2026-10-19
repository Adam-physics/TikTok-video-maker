"""Whiteboard explainer engine: one script in, one narrated vertical video out.

A video is an *angle* module (see `trivia/angles/`) holding a SCRIPT: a list
of (narration line, scene builder) pairs, optionally with KEEP as a third
element to keep drawing on the same board instead of erasing it. The
narration is voiced in one take; its word timings cut the scenes, pin
drawings to spoken words, and drive the captions.

The look follows the explainer doodles that already perform on social:
soft paper, thin navy ink, a fixed audience label at the top, drawings that
build up across sentences until an eraser wipes the board, handwritten
captions with a highlighter on the spoken word, and no music.
"""
from __future__ import annotations

import os
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

from . import brand, foley, voice
from .doodle import INK, SS, eraser_sprite, font, paint_hand, paper
from .render import ffmpeg_bin

W, H, FPS = brand.WIDTH, brand.HEIGHT, brand.FPS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(ROOT, "assets", "fonts")
KEEP = "keep"           # third element of a SCRIPT entry: draw on the same board
ERASE = 0.45            # one quick left-to-right pass, as in the reference
TAIL = 1.6              # hold on the last frame after the voice ends
SHOW_HAND = False       # the reference style draws with no visible hand

CAPTION_Y = 1330
CAPTION_FONT = os.path.join(FONTS, "Kalam-Bold.ttf")
LABEL_FONT = os.path.join(FONTS, "PermanentMarker-Regular.ttf")
TEAL = (27, 128, 122)
HIGHLIGHT = (255, 214, 64, 150)


# ------------------------------------------------------------------ timing

def _norm(w: str) -> str:
    return re.sub(r"[^\w-]", "", w.lower())


def _entries(script):
    for entry in script:
        text, build, *flags = entry
        yield text, build, KEEP in flags


class Held:
    """An item carried over from the previous line: already fully drawn."""

    cue = None
    sound = None
    scribble = False
    duration = 0.0
    start = -1.0

    def __init__(self, item):
        self.item = item

    def tip(self, t):
        return None

    def paint(self, img, t, boil):
        self.item.paint(img, self.item.start + self.item.duration + 60, boil)


def timeline(script, words: list[dict]):
    """Split the narration's words into scenes and give each a duration."""
    entries = list(_entries(script))
    counts = [len(text.split()) for text, _, _ in entries]
    if len(words) != sum(counts):
        raise RuntimeError(f"narration has {len(words)} words, script has {sum(counts)}")
    starts, i = [], 0
    for n in counts:
        starts.append(0.0 if i == 0 else words[i]["start"] - 0.12)
        i += n
    end = words[-1]["end"] + TAIL
    scenes, i, board = [], 0, []
    for k, ((text, build, keep), n) in enumerate(zip(entries, counts)):
        t0 = starts[k]
        t1 = starts[k + 1] if k + 1 < len(starts) else end
        local = [{**w, "start": w["start"] - t0, "end": w["end"] - t0} for w in words[i:i + n]]
        keep = keep and k > 0
        new = build()
        held = [Held(it) for it in board] if keep else []
        board = (board if keep else []) + new
        scenes.append({"t0": t0, "duration": t1 - t0, "words": local, "items": held + new,
                       "new": new, "erase": k > 0 and not keep})
        i += n
    return scenes


def schedule(scene: dict) -> None:
    """Give every new item a start time inside the scene.

    Items pinned to a word split the scene into segments. Each segment is
    drawn between its own cue and the next one, sped up if it would not
    otherwise finish -- so a mark never lands on a drawing that is not
    there yet.
    """
    items, words, dur = scene["new"], scene["words"], scene["duration"]
    lead = ERASE + 0.05 if scene["erase"] else 0.05

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

def board(angle) -> Image.Image:
    """Paper plus everything that never changes: the audience label on top
    and the small line at the bottom."""
    img = paper()
    d = ImageDraw.Draw(img, "RGBA")
    chip = getattr(angle, "CHIP", None)
    if chip:
        f = font(LABEL_FONT, 40 * SS)
        w = f.getlength(chip) / SS
        x0, y0 = (W - w) / 2 - 26, 150
        d.rounded_rectangle([x0 * SS, y0 * SS, (x0 + w + 52) * SS, (y0 + 78) * SS],
                            radius=18 * SS, outline=TEAL, width=5 * SS)
        d.text((W / 2 * SS, (y0 + 41) * SS), chip, font=f, fill=TEAL, anchor="mm")
    foot = getattr(angle, "FOOTER", None)
    if foot:
        f = font(CAPTION_FONT, 30 * SS)
        d.text((W / 2 * SS, 1450 * SS), foot, font=f, fill=(140, 144, 152), anchor="mm")
    return img


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
    # Handwritten caption, with a highlighter swipe behind the spoken word.
    f = font(CAPTION_FONT, 72 * SS)
    texts = [w["text"].strip('"“”') for w in group]
    space = f.getlength(" ")
    widths = [f.getlength(s) for s in texts]
    x = (W * SS - sum(widths) - space * (len(texts) - 1)) / 2
    y = CAPTION_Y * SS
    k = SS
    d = ImageDraw.Draw(img, "RGBA")
    for w, s, wd in zip(group, texts, widths):
        active = w["start"] - 0.03 <= t <= w["end"] + 0.05 or (
            w is group[-1] and t > w["end"])
        if active:
            d.polygon([(x - 8 * k, y - 4 * k), (x + wd + 10 * k, y - 8 * k),
                       (x + wd + 6 * k, y + 34 * k), (x - 6 * k, y + 37 * k)], fill=HIGHLIGHT)
        d.text((x, y), s, font=f, fill=INK, anchor="ls")
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
    if SHOW_HAND and pen is not None:
        paint_hand(img, pen)
    return img


# The eraser makes one quick pass from left to right through the middle of
# the board, bobbing a little, and everything behind it is wiped clean: the
# same move as the reference video.
ERASE_TOP, ERASE_BOTTOM = 245, 1265      # between the label and the captions
_ERASER = None


def _erase(prev: Image.Image, fresh: Image.Image, u: float) -> Image.Image:
    global _ERASER
    if _ERASER is None:
        _ERASER = eraser_sprite()
    e = u * u * (3 - 2 * u)                         # ease in and out
    ex = (-0.12 + 1.26 * e) * W
    ey = 760 + 55 * np.sin(u * np.pi * 3)
    wipe = ex + 40                                  # the felt's trailing edge
    w, h = W * SS, H * SS
    col = np.clip((np.arange(w) / SS - wipe) / 24, 0, 1)   # soft vertical edge
    mask = np.full((h, w), 255, np.uint8)
    mask[ERASE_TOP * SS:ERASE_BOTTOM * SS, :] = (col * 255).astype(np.uint8)[None, :]
    out = fresh.copy()
    out.paste(prev, (0, 0), Image.fromarray(mask, "L"))
    if u < 1:
        out.alpha_composite(_ERASER, (int(ex * SS - _ERASER.width / 2),
                                      int(ey * SS - _ERASER.height / 2)))
    return out


def render(angle, out_path: str) -> dict:
    cache = os.path.join(ROOT, "out", "explainer", angle.ID)
    os.makedirs(cache, exist_ok=True)
    text = " ".join(t for t, *_ in angle.SCRIPT)
    vo_path, words = voice.synthesize(text, cache)
    scenes = timeline(angle.SCRIPT, words)
    for s in scenes:
        schedule(s)
    total = scenes[-1]["t0"] + scenes[-1]["duration"]

    base = board(angle)
    cmd = [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS),
           "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "14",
           "-tune", "animation",
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
        if s["erase"] and prev_last is not None and lt < ERASE + 0.05:
            img = _erase(prev_last, img, min(1.0, lt / ERASE))
        paint_caption(img, s["words"], lt)
        enc.stdin.write(img.reduce(SS).convert("RGB").tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError("ffmpeg failed while encoding frames")

    wav = os.path.join(cache, "mix.wav")
    mix(scenes, total, vo_path, wav)
    done = subprocess.run(
        [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error",
         "-i", os.path.join(cache, "video.mp4"), "-i", wav,
         "-map", "0:v", "-map", "1:a", "-c:v", "copy",
         # Social apps play back near -14 LUFS; quieter uploads sound weak.
         "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "48000",
         "-c:a", "aac", "-b:a", "192k",
         "-shortest", "-movflags", "+faststart", out_path],
        capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr[-3000:])
    return {"path": out_path, "duration": total, "voiced": vo_path is not None,
            "scenes": scenes}


# ------------------------------------------------------------------ sound

def _put(track: np.ndarray, sound: np.ndarray, at: float) -> None:
    start = int(at * foley.SR)
    end = min(start + len(sound), len(track))
    if end > start >= 0:
        track[start:end] += sound[:end - start]


def _read_voice(path: str) -> np.ndarray:
    raw = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", path, "-f", "s16le",
                          "-ac", "1", "-ar", str(foley.SR), "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, dtype="<i2").astype(float) / 32768


def mix(scenes, total, vo_path, path):
    """Voice, plus quiet foley for what is happening on the board. No music."""
    # A faint room tone under everything: pure digital silence between
    # sentences sounds like the audio cut out.
    rng = np.random.default_rng(1)
    hiss = np.convolve(rng.standard_normal(int(total * foley.SR) + foley.SR),
                       np.ones(24) / 24, mode="same")
    track = hiss * (10 ** (-56 / 20) / (np.sqrt(np.mean(hiss ** 2)) + 1e-12))
    for k, s in enumerate(scenes):
        if s["erase"]:
            _put(track, foley.sample("eraser"), s["t0"] + 0.08)
        for j, it in enumerate(s["new"]):
            at = s["t0"] + it.start
            if it.sound:
                _put(track, foley.sample(it.sound), at)
            if it.scribble and it.duration > 0.12:
                _put(track, foley.marker(it.duration, k * 100 + j), at)
    if vo_path:
        _put(track, _read_voice(vo_path), 0.0)
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
    return path


def stills(angle, out_dir: str) -> list[str]:
    """The last frame of every scene, for checking layout by eye."""
    text = " ".join(t for t, *_ in angle.SCRIPT)
    scenes = timeline(angle.SCRIPT, voice.estimate(text))
    base, paths = board(angle), []
    os.makedirs(out_dir, exist_ok=True)
    for k, s in enumerate(scenes):
        schedule(s)
        img = scene_frame(base, s, s["duration"] - 0.05, 0)
        paint_caption(img, s["words"], s["words"][-1]["end"])
        p = os.path.join(out_dir, f"scene-{k + 1:02d}.png")
        img.reduce(SS).convert("RGB").save(p)
        paths.append(p)
    return paths
