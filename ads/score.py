"""Music bed for the Amazon ads: a slow pad, a soft arpeggio, a whoosh per beat.

Synthesised for the same reason as the TikTok score -- nothing here carries
a licence anyone can claim. Most viewers will never hear it (Amazon autoplays
muted), so it only has to be pleasant and unobtrusive when someone unmutes.
"""
from __future__ import annotations

import wave

import numpy as np

from trivia.audio import SR, _mix, pluck, whoosh

# A minor -> F -> C -> G: wide, a little wistful, suits "the universe is strange".
CHORDS = [
    [110.00, 164.81, 220.00, 261.63],
    [87.31, 130.81, 174.61, 220.00],
    [130.81, 196.00, 261.63, 329.63],
    [98.00, 146.83, 196.00, 246.94],
]
ARP = [0, 2, 3, 2]
CHORD_LEN = 2.0        # seconds per chord
STEP = 0.25            # arpeggio eighths at 120 bpm


def _pad_note(freq: float, dur: float) -> np.ndarray:
    n = int(dur * SR)
    t = np.arange(n) / SR
    tone = sum(np.sin(2 * np.pi * freq * d * t) for d in (0.996, 1.0, 1.004)) / 3
    tone += 0.25 * np.sin(2 * np.pi * freq * 2 * t)
    env = np.minimum(1.0, t / 0.5) * np.minimum(1.0, (dur - t) / 0.6).clip(0, 1)
    return tone * env


def boom() -> np.ndarray:
    """A low hit with a falling pitch, for the cold open."""
    n = int(0.9 * SR)
    t = np.arange(n) / SR
    freq = 55 + 60 * np.exp(-t * 14)
    return np.sin(2 * np.pi * np.cumsum(freq) / SR) * np.exp(-t * 4.5)


def render(duration: float, cuts: list[float], path: str, hits: list[float] = ()) -> str:
    out = np.zeros(int(duration * SR) + SR)
    t = 0.0
    k = 0
    while t < duration:
        chord = CHORDS[k % len(CHORDS)]
        for f in chord:
            _mix(out, _pad_note(f, CHORD_LEN + 0.6) * 0.055, t)
        for s in range(int(CHORD_LEN / STEP)):
            note = chord[ARP[s % len(ARP)]] * 2
            _mix(out, pluck(note, 0.6, 6.0) * 0.06, t + s * STEP)
        t += CHORD_LEN
        k += 1

    _mix(out, boom() * 0.5, 0.0)
    for h in hits:                          # a stamp on the "it's real" beats
        _mix(out, boom() * 0.35, h)
    for c in cuts:
        _mix(out, whoosh(0.3) * 0.08, max(0.0, c - 0.15))

    out = out[:int(duration * SR)]
    fade = int(0.8 * SR)
    out[-fade:] *= np.linspace(1, 0, fade)
    out = np.tanh(out / max(1e-6, np.abs(out).max()) * 1.2) * 0.85
    pcm = (out * 32767).astype("<i2")
    with wave.open(path, "wb") as f:
        f.setnchannels(2)
        f.setsampwidth(2)
        f.setframerate(SR)
        f.writeframes(np.repeat(pcm[:, None], 2, axis=1).tobytes())
    return path
