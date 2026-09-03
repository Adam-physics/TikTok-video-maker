"""Procedural score and sound effects, synthesised with numpy.

Written rather than sourced, because every free music library carries a
licence that can strike a monetised account later. Nothing here is
copyrightable by anyone else, and it costs nothing.

The bed sits deliberately low so a narration track can be dropped on top
later without a remix.
"""
from __future__ import annotations

import wave

import numpy as np

SR = 48000
BED_GAIN = 0.16      # leaves headroom for a future voiceover
SFX_GAIN = 0.42

# A minor pentatonic keeps every accidental pairing consonant, so the bed
# never needs hand-tuning per round length.
SCALE = [261.63, 311.13, 349.23, 392.00, 466.16, 523.25, 622.25, 698.46]


def _env(n: int, attack: int, decay: float) -> np.ndarray:
    t = np.arange(n) / SR
    env = np.exp(-decay * t)
    ramp = min(attack, n)
    env[:ramp] *= np.linspace(0.0, 1.0, ramp)
    return env


def pluck(freq: float, dur: float, decay: float = 5.5) -> np.ndarray:
    """A marimba-ish note: fundamental plus a quiet octave, fast decay."""
    n = int(dur * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * freq * t) + 0.28 * np.sin(4 * np.pi * freq * t)
    return body * _env(n, 96, decay)


def whoosh(dur: float = 0.34) -> np.ndarray:
    """Filtered noise sweep for a scene change."""
    n = int(dur * SR)
    noise = np.random.default_rng(7).standard_normal(n)
    # One-pole lowpass whose cutoff opens over the sweep.
    out = np.zeros(n)
    acc = 0.0
    for i in range(n):
        a = 0.02 + 0.28 * (i / n)
        acc += a * (noise[i] - acc)
        out[i] = acc
    return out * _env(n, 200, 7.0) * 3.2


def ding() -> np.ndarray:
    """Correct-answer chime -- a rising major third."""
    return np.concatenate([pluck(880, 0.16, 8), pluck(1108.7, 0.42, 5)])


def buzz() -> np.ndarray:
    """Wrong-answer honk. Detuned and short, so it reads as comic."""
    n = int(0.34 * SR)
    t = np.arange(n) / SR
    tone = np.sign(np.sin(2 * np.pi * 146.8 * t)) * 0.5
    tone += np.sign(np.sin(2 * np.pi * 155.6 * t)) * 0.3
    return tone * _env(n, 300, 6.0)


def tick() -> np.ndarray:
    return pluck(1560, 0.05, 40) * 0.5


def _bed(duration: float) -> np.ndarray:
    """A looping arpeggio for the whole round."""
    out = np.zeros(int(duration * SR) + SR)
    rng = np.random.default_rng(11)
    step, i, t = 0.30, 0, 0.0
    while t < duration:
        note = SCALE[[0, 2, 4, 2, 5, 4, 2, 0][i % 8]]
        if i % 8 == 0:                      # a bass note on the downbeat
            _mix(out, pluck(note / 2, 1.1, 2.2) * 0.7, t)
        _mix(out, pluck(note * (2 if rng.random() < 0.18 else 1), 0.7), t)
        t += step
        i += 1
    return out * BED_GAIN


def _mix(track: np.ndarray, sound: np.ndarray, at: float) -> None:
    start = int(at * SR)
    end = min(start + len(sound), len(track))
    if end > start:
        track[start:end] += sound[:end - start]


def render(duration: float, events: list[tuple[float, str]], path: str) -> str:
    """Write the finished stereo bed plus effects to a 16-bit WAV.

    `events` is (time_in_seconds, name) where name is one of the effect
    functions below. Unknown names raise rather than silently drop.
    """
    effects = {"whoosh": whoosh, "ding": ding, "buzz": buzz, "tick": tick}
    track = _bed(duration)
    for at, name in events:
        if name not in effects:
            raise KeyError(f"unknown sound effect {name!r}")
        _mix(track, effects[name]() * SFX_GAIN, at)

    track = track[:int(duration * SR)]
    peak = np.abs(track).max()
    if peak > 0.95:                          # soft-limit rather than clip
        track = np.tanh(track / peak * 1.4) * 0.92
    pcm = (np.clip(track, -1, 1) * 32767).astype("<i2")
    stereo = np.repeat(pcm[:, None], 2, axis=1).tobytes()

    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(stereo)
    return path
