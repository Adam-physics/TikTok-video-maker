"""Narration: ElevenLabs text-to-speech with per-character timestamps.

The whole script is read in ONE request so the voice keeps its rhythm
across scene boundaries; the timestamps then say where each scene starts
and when each word is spoken, which drives both the cut points and the
burned-in captions. Results are cached by a hash of (text, voice, model),
so re-rendering after a visual tweak never spends credits twice.

Without a key the same word timings are *estimated* from a reading pace,
so the visuals can be developed and reviewed before any audio exists.

    ELEVENLABS_API_KEY   required for real narration
    ELEVENLABS_VOICE_ID  optional; defaults to Siren from the voice library
    ELEVENLABS_MODEL     optional; defaults to eleven_v4
"""
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import urllib.request

API = "https://api.elevenlabs.io/v1/text-to-speech/{voice}/with-timestamps"
DEFAULT_VOICE = "eXpIbVcVbLo8ZJQDlDnl"   # "Siren": natural, conversational, social-first
DEFAULT_MODEL = "eleven_v4"


def _words_from_alignment(al: dict) -> list[dict]:
    chars = al["characters"]
    starts = al["character_start_times_seconds"]
    ends = al["character_end_times_seconds"]
    words, cur = [], None
    for i, ch in enumerate(chars):
        if ch.isspace():
            if cur:
                words.append(cur)
                cur = None
            continue
        if cur is None:
            cur = {"text": "", "start": starts[i], "end": ends[i], "char": i}
        cur["text"] += ch
        cur["end"] = ends[i]
    if cur:
        words.append(cur)
    return words


def estimate(text: str) -> list[dict]:
    """Word timings for an unvoiced draft, at a brisk social-video pace."""
    t, words = 0.15, []
    for m in re.finditer(r"\S+", text):
        w = m.group()
        dur = 0.08 + 0.046 * len(re.sub(r"\W", "", w))
        words.append({"text": w, "start": t, "end": t + dur, "char": m.start()})
        t += dur + 0.04
        if w[-1] in ".!?":
            t += 0.26
        elif w[-1] in ",;:":
            t += 0.12
    return words


def synthesize(text: str, cache_dir: str) -> tuple[str | None, list[dict]]:
    """Return (mp3 path or None, word timings)."""
    key = os.environ.get("ELEVENLABS_API_KEY")
    if not key:
        return None, estimate(text)
    voice = os.environ.get("ELEVENLABS_VOICE_ID", DEFAULT_VOICE)
    model = os.environ.get("ELEVENLABS_MODEL", DEFAULT_MODEL)
    digest = hashlib.sha1(f"{voice}|{model}|{text}".encode()).hexdigest()[:12]
    os.makedirs(cache_dir, exist_ok=True)
    mp3 = os.path.join(cache_dir, f"vo-{digest}.mp3")
    meta = os.path.join(cache_dir, f"vo-{digest}.json")
    if os.path.exists(mp3) and os.path.exists(meta):
        with open(meta) as f:
            return mp3, json.load(f)

    # No voice_settings: library voices ship tuned by their creators.
    body = json.dumps({"text": text, "model_id": model}).encode()
    req = urllib.request.Request(
        API.format(voice=voice) + "?output_format=mp3_44100_128", data=body,
        headers={"xi-api-key": key, "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            data = json.load(r)
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"ElevenLabs {e.code}: {e.read().decode()[:600]}") from e

    with open(mp3, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))
    words = _words_from_alignment(data.get("alignment") or data["normalized_alignment"])
    with open(meta, "w") as f:
        json.dump(words, f)
    return mp3, words


def tighten(mp3: str, words: list[dict], cache_dir: str, cap: float = 0.2,
            floor_db: float = -42.0) -> tuple[str, list[dict]]:
    """Shorten every pause in the narration to at most `cap` seconds.

    Speeding the voice up changes how it sounds; cutting dead air does not.
    Silences are found in the audio itself (the alignment folds pauses into
    punctuation), the middle of each long one is removed, and the word
    timings are shifted to match so captions and cues stay in sync.
    """
    import subprocess

    import numpy as np

    from .render import ffmpeg_bin
    sr, hop = 48000, 480
    out = os.path.join(cache_dir, os.path.basename(mp3).replace(".mp3", f"-tight{int(cap * 100)}.wav"))
    raw = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", mp3, "-f", "s16le", "-ac", "1",
                          "-ar", str(sr), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype="<i2").astype(float) / 32768
    frames = len(x) // hop
    level = 20 * np.log10(np.sqrt((x[:frames * hop].reshape(frames, hop) ** 2).mean(1)) + 1e-9)
    quiet = level < floor_db

    cuts, start = [], None                      # (time the cut begins, seconds removed)
    for i, q in enumerate(list(quiet) + [False]):
        if q and start is None:
            start = i
        elif not q and start is not None:
            dur = (i - start) * hop / sr
            if dur > cap and start > 0:
                begin = start * hop / sr + cap / 2
                cuts.append((begin, dur - cap))
            start = None

    keep, last = [], 0
    for begin, removed in cuts:
        a, b = int(begin * sr), int((begin + removed) * sr)
        keep.append(x[last:a])
        last = b
    keep.append(x[last:])
    y = np.concatenate(keep)
    import wave
    with wave.open(out, "wb") as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sr)
        f.writeframes((np.clip(y, -1, 1) * 32767).astype("<i2").tobytes())

    def shift(t):
        moved = 0.0
        for begin, removed in cuts:
            if t >= begin + removed:
                moved += removed
            elif t > begin:
                return begin - moved
        return t - moved

    tight = [{**w, "start": shift(w["start"]), "end": shift(w["end"])} for w in words]
    return out, tight
