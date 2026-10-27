"""Full-screen comic re-cut of book page 7 (sharks / butterflies / horses).

Same parent-voice narration as play4, so it reuses that recording.
"""
from .play4 import CAPTION, HASHTAGS, SCRIPT as _WHITEBOARD

ID = "comic7"
CACHE = "play4"
Q, A = "q04.png", "a04.png"

_SHOTS = [
    {"view": "page", "page": "q", "box": "POV: the dinner game my kid begs for every night"},
    {"view": "panel", "page": "q", "panel": 0},
    {"view": "panel", "page": "q", "panel": 1},
    {"view": "panel", "page": "q", "panel": 2},
    {"view": "lock", "page": "q", "box": "LOCK IN YOUR GUESS", "count": ["three", "two", "one"]},
    {"view": "panel", "page": "a", "panel": 0, "stamp": ("FAKE!", "fake")},
    {"view": "panel", "page": "a", "panel": 1, "stamp": ("REAL!", "real")},
    {"view": "panel", "page": "a", "panel": 2, "stamp": ("REAL!", "real")},
    {"view": "end", "box": "search “Trick Trivia” on Amazon"},
]
SCRIPT = [(entry[0], shot) for entry, shot in zip(_WHITEBOARD, _SHOTS)]
