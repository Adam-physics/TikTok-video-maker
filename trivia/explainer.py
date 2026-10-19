"""Whiteboard explainer engine: one script in, one narrated vertical video out.

A video is an *angle* module (see `trivia/angles/`) holding a SCRIPT: a list
of (narration line, scene builder) pairs. The narration is voiced in one
take; its word timings cut the scenes, pin drawings to spoken words, and
drive the captions.
"""
from __future__ import annotations

import os
import re
import subprocess
import wave

import numpy as np
from PIL import Image, ImageDraw

from . import audio, brand, voice
from .doodle import INK, font, paint_hand, paper
from .render import ffmpeg_bin

W, H, FPS = brand.WIDTH, brand.HEIGHT, brand.FPS
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TRANSITION = 0.30
CAPTION_Y = 1390
TAIL = 1.6              # hold on the last frame after the voice ends
CAPTION_FONT = os.path.join(ROOT, "assets", "fonts", "Montserrat-Black.ttf")
YELLOW = brand.YELLOW


# ------------------------------------------------------------------ timing

def _norm(w: str) -> str:
    return re.sub(r"[^\w-]", "", w.lower())


def timeline(script, words: list[dict]):
    """Split the narration's words into scenes and give each a duration."""
    scenes, i = [], 0
    counts = [len(text.split()) for text, _ in script]
    if len(words) != sum(counts):
        raise RuntimeError(f"narration has {len(words)} words, script has {sum(counts)}")
    starts = []
    for n in counts:
        starts.append(0.0 if i == 0 else words[i]["start"] - 0.12)
        i += n
    end = words[-1]["end"] + TAIL
    i = 0
    for k, ((text, build), n) in enumerate(zip(script, counts)):
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
    # The CapCut look viewers already read without thinking: heavy white
    # caps, thick black outline, the spoken word in yellow.
    f = font(CAPTION_FONT, 70)
    texts = [w["text"].strip('"\u201c\u201d').upper() for w in group]
    space = f.getlength(" ") + 16
    widths = [f.getlength(s) for s in texts]
    x = (W - sum(widths) - space * (len(texts) - 1)) / 2
    d = ImageDraw.Draw(img, "RGBA")
    for w, s, wd in zip(group, texts, widths):
        active = w["start"] - 0.03 <= t <= w["end"] + 0.05 or (
            w is group[-1] and t > w["end"])
        d.text((x, CAPTION_Y), s, font=f, fill=YELLOW if active else (255, 255, 255),
               anchor="lm", stroke_width=8, stroke_fill=INK)
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
        paint_hand(img, pen)
    return img


def render(angle, out_path: str) -> dict:
    cache = os.path.join(ROOT, "out", "explainer", angle.ID)
    os.makedirs(cache, exist_ok=True)
    text = " ".join(t for t, _ in angle.SCRIPT)
    vo_path, words = voice.synthesize(text, cache)
    scenes = timeline(angle.SCRIPT, words)
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


def stills(angle, out_dir: str) -> list[str]:
    """The last frame of every scene, for checking layout by eye."""
    text = " ".join(t for t, _ in angle.SCRIPT)
    scenes = timeline(angle.SCRIPT, voice.estimate(text))
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
