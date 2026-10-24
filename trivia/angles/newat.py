"""Angle: your kid gets one thing wrong and says "I'm so stupid."

Value first, and honest: arguing back ("you're so smart!") isn't believed and
keeps the focus on being smart. "You're not bad at it, you're new at it,"
then shrinking it to the one tricky part, turns a person into a problem; and
seeing a parent be wrong out loud makes it normal. The book is one game where
grown-ups get fooled, next to any game where grown-ups lose.
"""
from __future__ import annotations

import math

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, circle, curve, ellipse, line, poly, rrect
from ..explainer import KEEP
from ..figures import bubble, cover, kid
from .reading import BLUE, GOLD, GREEN, GREY, RED, TEAL, W, note, tag
from .school import speech
from .screens import crossed, game_box

ID = "newat"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“Sloths can hold their breath longer than dolphins.”"
SWEAT = (120, 180, 230)
SLOTH = (190, 160, 120)
DOLPHIN = (150, 180, 215)


def worksheet(cx, cy):
    return [Shape([rrect(cx - 130, cy - 160, cx + 130, cy + 160, r=8)] +
                  [line((cx - 100, cy - 100 + k * 55), (cx + 90 - (k % 2) * 40, cy - 100 + k * 55), wobble=0.8)
                   for k in range(5)], width=6, fill=(255, 255, 255), fill_offset=(0, 0))]


def drops(cx, cy):
    return Shape([ellipse(cx, cy, 10, 16, wobble=0.4), ellipse(cx + 34, cy + 30, 8, 13, wobble=0.4)],
                 color=SWEAT, fill=SWEAT, width=4, fill_offset=(0, 0))


def sprout(cx, cy):
    return [Shape(line((cx - 120, cy + 60), (cx + 120, cy + 60)), color=(130, 90, 60), width=8),
            Shape(curve([(cx, cy + 60), (cx - 6, cy), (cx, cy - 60)], wobble=0.6), color=GREEN, width=9),
            Shape([ellipse(cx - 40, cy - 40, 40, 18, rot=-25), ellipse(cx + 40, cy - 60, 40, 18, rot=25)],
                  color=GREEN, fill=(190, 234, 200), width=6, fill_offset=(0, 0))]


def tangle(cx, cy, r=150):
    pts = [(cx + r * math.cos(t * 2.3) * (0.4 + 0.6 * ((t * 7) % 5) / 5),
            cy + r * math.sin(t * 3.1) * (0.4 + 0.6 * ((t * 3) % 4) / 4)) for t in range(40)]
    return Shape(curve(pts, wobble=1.0, samples=6), color=GREY, width=6)


def sloth(cx, cy):
    return [Shape(line((cx - 170, cy - 120), (cx + 170, cy - 110)), color=(130, 90, 60), width=14),
            Shape([line((cx - 50, cy - 20), (cx - 70, cy - 118)), line((cx + 50, cy - 20), (cx + 70, cy - 114))],
                  color=SLOTH, width=16),
            Shape(ellipse(cx, cy + 30, 90, 70), color=(120, 90, 60), fill=SLOTH, width=7, fill_offset=(0, 0)),
            Shape(circle(cx, cy - 10, 52), color=(120, 90, 60), fill=(230, 210, 180), width=7,
                  fill_offset=(0, 0)),
            Shape([ellipse(cx - 20, cy - 14, 14, 9, rot=-20), ellipse(cx + 20, cy - 14, 14, 9, rot=20)],
                  color=(90, 60, 40), fill=(90, 60, 40), width=4, fill_offset=(0, 0)),
            Shape(curve([(cx - 14, cy + 14), (cx, cy + 22), (cx + 14, cy + 14)], wobble=0.3), width=5)]


def dolphin(cx, cy):
    body = [(cx - 160, cy + 10), (cx - 80, cy - 50), (cx + 40, cy - 60), (cx + 140, cy - 20),
            (cx + 170, cy), (cx + 120, cy + 20), (cx, cy + 40), (cx - 120, cy + 30)]
    return [Shape(poly(body, closed=True, wobble=1.0), color=(70, 100, 150), fill=DOLPHIN, width=7,
                  fill_offset=(0, 0)),
            Shape([poly([(cx - 10, cy - 55), (cx + 20, cy - 110), (cx + 40, cy - 58)], wobble=0.6),
                   poly([(cx - 150, cy + 10), (cx - 200, cy - 30), (cx - 190, cy + 20), (cx - 200, cy + 60),
                         (cx - 150, cy + 20)], wobble=0.6)], color=(70, 100, 150), width=7),
            Shape(circle(cx + 100, cy - 18, 7, wobble=0.2), fill=INK, width=4, fill_offset=(0, 0))]


# ------------------------------------------------------------------ boards

def l_hook():
    """Only the headline is there on frame one; the scene draws as it is said."""
    child = kid(300, 1060, 0.95, "bored", "down")
    child[0].at("kid")
    return [
        Text("“I'M SO STUPID.”", (540, 320), size=88, face=MARKER, color=RED).ready(),
        *child,
        *worksheet(760, 760),
        crossed(760, 700, 90).at("wrong"),
        drops(400, 790).at("stupid"),
        Text("?", (560, 600), size=150, face=MARKER, color=GREEN).at("what").focus(1.08).pop(),
    ]


def l_smart():
    cheer = speech(390, 520, 280, 96, (300, 780), "No, you're so SMART!", size=48)
    cheer[0].at("no")
    listener = kid(800, 1090, 0.75, "bored", "down")
    listener[0].at("feels")
    return [
        *kid(270, 1060, 0.95, "happy", "point"),
        *cheer,
        *listener,
        Shape(arrow((620, 590), (690, 420), bend=40, head=22), color=GREY, width=7).at("don't"),
        crossed(390, 520, 110).at("believe"),
        tag("focus stays on “smart”", (690, 340), size=48, color=GREY).at("focus"),
    ]


def l_new():
    return [
        tag("“BAD AT IT.”", (540, 360), size=80, color=GREY).at("bad"),
        Shape(line((310, 365), (770, 355)), color=RED, width=12),
        Text("“NEW AT IT.”", (540, 540), size=120, face=MARKER, color=TEAL).at("new").pop(),
    ]


def l_shrink():
    return [
        tangle(270, 820, 140),
        Shape(arrow((450, 820), (640, 820), head=26), color=TEAL, width=W).at("shrink"),
        Shape(curve([(780, 800), (820, 840), (790, 860), (770, 820), (810, 790)], wobble=0.6),
              color=GREY, width=6).at("one"),
        Shape(circle(795, 825, 70), color=RED, width=8),
        note("the tricky part", (795, 950), size=50).at("tricky"),
        tag("a problem, not a person", (540, 1110), size=60, color=TEAL).at("problem").pop(),
    ]


def l_me():
    oops = speech(420, 540, 290, 96, (320, 780), "Huh, I didn't know that!", size=48)
    oops[0].at("huh")
    child = kid(810, 1090, 0.75, "happy", "up")
    child[0].at("see")
    return [
        *kid(290, 1060, 0.95, "happy", "point"),
        *child,
        *oops,
        tag("out loud, often", (800, 720), size=50, color=TEAL).at("loud").pop(),
    ]


def l_sloth():
    child = kid(930, 1150, 0.5, "think", "chin")
    return [
        *child,
        tag("REAL OR FAKE?", (540, 330), size=64, color=GOLD),
        note("(they fool me all the time)", (540, 410), size=42, color=GREY).at("fool"),
        Shape(rrect(70, 460, 1010, 640, r=24), width=W, fill=(255, 255, 255), fill_offset=(0, 0)).at("like"),
        note(CLAIM, (540, 552), size=48, max_width=880),
        *[s.at("sloths") if k == 0 else s for k, s in enumerate(sloth(280, 880))],
        *[d.at("longer") if k == 0 else d for k, d in enumerate(dolphin(700, 900))],
        tag("REAL!", (480, 1130), size=110, color=GREEN).at("dolphins").focus(1.1).pop(),
    ]


def l_options():
    return [
        *kid(240, 1040, 0.95, "happy", "hold"),
        Picture(cover(), (240, 985), width=112, angle=-4).at("book"),
        note("Trick Trivia", (280, 650), size=42, color=GREY).at("trick"),
        Shape(arrow((330, 690), (305, 930), bend=-30, head=18), color=GREY, width=6),
        game_box(760, 500).at("game"),
        *[f.at("grown-ups") if k == 0 else f for k, f in enumerate(kid(760, 1010, 0.6, "happy", "up"))],
        tag("kid wins!", (760, 720), size=60, color=TEAL).at("lose").pop(),
    ]


def l_close():
    return [
        tag("NOT “BAD AT IT.”", (540, 480), size=80, color=GREY),
        Text("“NEW AT IT.”", (540, 680), size=120, face=MARKER, color=TEAL).focus(1.08).pop(),
    ]


SCRIPT = [
    ("Your kid gets one thing wrong and says, “I'm so stupid.” Don't argue with it. Here's what "
     "to say instead.", l_hook),
    ("“No, you're so smart!” feels kind. But they don't believe it, and it keeps the focus on "
     "being smart.", l_smart),
    ("Try: “You're not bad at it. You're new at it.”", l_new),
    ("Then shrink it: “What's the one part that's tricky?” Now it's a problem, not a person.",
     l_shrink, KEEP),
    ("And let them see you be wrong. Say “Huh, I didn't know that,” out loud, often.", l_me),
    ("One thing that does that for us is real-or-fake questions. They fool me all the time, and "
     "nobody's stupid. Like, “Sloths can hold their breath longer than dolphins.” Real.", l_sloth),
    ("We use a book called Trick Trivia, but any game where grown-ups lose works too.", l_options),
    ("Not bad at it. New at it.", l_close),
]

CAPTION = (
    "Your kid gets one thing wrong and says \"I'm so stupid.\" Don't argue with it. \"No, you're "
    "so smart!\" feels kind, but they don't believe it, and it keeps the focus on being smart. "
    "Try: \"You're not bad at it. You're new at it.\" Then shrink it: \"What's the one part "
    "that's tricky?\" Now it's a problem, not a person. And let them see you be wrong, out "
    "loud, often. Real-or-fake questions from Trick Trivia (it's on Amazon) fool me all the "
    "time, but any game where grown-ups lose works too. (Sloths really can hold their breath "
    "longer than dolphins.)"
)
HASHTAGS = ["#parentingtips", "#gentleparenting", "#growthmindset", "#momtok", "#dadtok",
            "#selfesteem", "#realorfake"]
