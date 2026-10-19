"""Real-sounding foley for the whiteboard videos: marker, eraser, tape, tap.

The marker, tape and tap samples in assets/sfx/ were generated once with
ElevenLabs' sound effects model; the eraser swish was cut from the reference
video the style is matched to. All are committed, so a render needs no key
and no network.
Each sample is level-matched by RMS, so the mix sets loudness in dB
relative to the narration rather than trusting whatever level a file has.

The look being matched (voice-only explainer doodles) uses no music and
only quiet, literal sounds of the drawing itself. Nothing cartoonish.
"""
from __future__ import annotations

import os
import subprocess

import numpy as np

from .render import ffmpeg_bin

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SFX = os.path.join(ROOT, "assets", "sfx")
SR = 48000

# Target RMS in dBFS before the final loudness pass. The narration sits
# around -20, so the marker is a texture you feel more than hear.
LEVELS = {"marker": -38.0, "eraser": -34.0, "tape": -30.0, "tap": -32.0}

_cache: dict[str, np.ndarray] = {}


def _load(name: str) -> np.ndarray:
    path = next(p for p in (os.path.join(SFX, f"{name}.{ext}") for ext in ("wav", "mp3"))
                if os.path.exists(p))
    raw = subprocess.run([ffmpeg_bin(), "-v", "error", "-i", path, "-f", "s16le", "-ac", "1",
                          "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    x = np.frombuffer(raw, dtype="<i2").astype(float) / 32768
    # Trim leading and trailing near-silence so cues land on the sound.
    loud = np.where(np.abs(x) > 0.1 * np.abs(x).max())[0]
    if len(loud):
        x = x[max(0, loud[0] - 200): loud[-1] + 2000]
    rms = np.sqrt(np.mean(x ** 2)) + 1e-9
    return x * (10 ** (LEVELS[name] / 20) / rms)


def sample(name: str) -> np.ndarray:
    if name not in _cache:
        _cache[name] = _load(name)
    return _cache[name]


def marker(duration: float, seed: int) -> np.ndarray:
    """A slice of real marker scribble as long as the stroke, faded at both ends."""
    src = sample("marker")
    n = min(int(duration * SR), len(src) - 1)
    start = np.random.default_rng(seed).integers(0, max(1, len(src) - n))
    out = src[start:start + n].copy()
    fade = min(int(0.04 * SR), n // 2)
    if fade:
        ramp = np.linspace(0, 1, fade)
        out[:fade] *= ramp
        out[-fade:] *= ramp[::-1]
    return out
