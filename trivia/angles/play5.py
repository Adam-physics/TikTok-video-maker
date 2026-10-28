"""Whiteboard play-along from book page 11 (ants / goats / crocodiles), challenge hook.

Tests a new hook, "Are you smarter than a kids' trivia book?", on the
whiteboard format. Claims and answers follow the printed pages (q06.png,
a06.png); the ending is a recommendation, not a pitch.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, circle, curve, ellipse, line, poly, rrect
from ..explainer import KEEP
from ..figures import cover, kid, page
from .play1 import CHIP, FOOTER, ROWS, claim, l_lock, number, stamp
from .reading import GOLD, GREEN, GREY, RED, TEAL, note, tag

ID = "play5"
TIGHTEN = 0.2
ANT = (190, 70, 40)
GOAT = (215, 175, 130)
CROC = (110, 170, 80)
BAND = (170, 80, 200)


def ant(cx, cy, s=1.0):
    legs = []
    for dx in (-30, 0, 30):
        legs += [line((cx + dx * s, cy + 10 * s), (cx + (dx - 20) * s, cy + 55 * s), wobble=0.6),
                 line((cx + dx * s, cy - 10 * s), (cx + (dx - 20) * s, cy - 55 * s), wobble=0.6)]
    return [
        Shape(legs, width=5),
        Shape([ellipse(cx - 70 * s, cy, 42 * s, 32 * s), ellipse(cx, cy, 28 * s, 22 * s),
               ellipse(cx + 58 * s, cy - 4 * s, 30 * s, 26 * s)], color=(110, 40, 20), fill=ANT, width=5,
              fill_offset=(0, 0)),
        Shape([curve([(cx + 70 * s, cy - 26 * s), (cx + 90 * s, cy - 70 * s), (cx + 110 * s, cy - 80 * s)]),
               curve([(cx + 80 * s, cy - 22 * s), (cx + 115 * s, cy - 55 * s), (cx + 135 * s, cy - 58 * s)])],
              width=5),
        Shape(circle(cx + 68 * s, cy - 8 * s, 6 * s, wobble=0.2), fill=INK, width=3, fill_offset=(0, 0)),
    ]


def goat(cx, cy, s=1.0):
    head = [(cx - 50 * s, cy - 60 * s), (cx + 50 * s, cy - 60 * s), (cx + 40 * s, cy + 30 * s),
            (cx + 18 * s, cy + 80 * s), (cx - 18 * s, cy + 80 * s), (cx - 40 * s, cy + 30 * s)]
    return [
        Shape([curve([(cx - 30 * s, cy - 60 * s), (cx - 60 * s, cy - 120 * s), (cx - 100 * s, cy - 110 * s)]),
               curve([(cx + 30 * s, cy - 60 * s), (cx + 60 * s, cy - 120 * s), (cx + 100 * s, cy - 110 * s)])],
              color=(120, 100, 80), width=12),
        Shape([ellipse(cx - 78 * s, cy - 30 * s, 34 * s, 14 * s, rot=20),
               ellipse(cx + 78 * s, cy - 30 * s, 34 * s, 14 * s, rot=-20)], color=(130, 95, 60), fill=GOAT,
              width=5, fill_offset=(0, 0)),
        Shape(poly(head, closed=True, wobble=1.0), color=(130, 95, 60), fill=GOAT, width=6, fill_offset=(0, 0)),
        Shape([ellipse(cx - 22 * s, cy - 20 * s, 16 * s, 12 * s), ellipse(cx + 22 * s, cy - 20 * s, 16 * s, 12 * s)],
              fill=(250, 220, 90), width=4, fill_offset=(0, 0)),
        # The rectangular pupils the claim is about.
        Shape([rrect(cx - 32 * s, cy - 24 * s, cx - 12 * s, cy - 16 * s, r=2),
               rrect(cx + 12 * s, cy - 24 * s, cx + 32 * s, cy - 16 * s, r=2)], fill=INK, width=3,
              fill_offset=(0, 0)),
        Shape(poly([(cx - 10 * s, cy + 80 * s), (cx, cy + 120 * s), (cx + 10 * s, cy + 80 * s)], wobble=0.4),
              color=(240, 240, 240), fill=(250, 250, 250), width=4, fill_offset=(0, 0)),
    ]


def croc(cx, cy, s=1.0, band=False):
    snout = [(cx - 120 * s, cy - 30 * s), (cx + 150 * s, cy - 10 * s), (cx + 160 * s, cy + 10 * s),
             (cx + 140 * s, cy + 24 * s), (cx - 120 * s, cy + 34 * s)]
    out = [
        Shape(poly(snout, closed=True, wobble=1.0), color=(60, 110, 40), fill=CROC, width=6, fill_offset=(0, 0)),
        Shape(line((cx - 110 * s, cy + 4 * s), (cx + 150 * s, cy + 8 * s)), color=(60, 110, 40), width=5),
        Shape(poly([(cx - 40 * s + k * 34 * s, cy + 6 * s) if j == 0 else (cx - 23 * s + k * 34 * s, cy + 22 * s)
                    for k in range(5) for j in (0, 1)], wobble=0.3), color=(250, 250, 250), width=4),
        Shape(ellipse(cx - 70 * s, cy - 44 * s, 26 * s, 20 * s), color=(60, 110, 40), fill=CROC, width=5,
              fill_offset=(0, 0)),
        Shape(circle(cx - 66 * s, cy - 46 * s, 8 * s, wobble=0.2), fill=INK, width=3, fill_offset=(0, 0)),
    ]
    if band:
        out.append(Shape([ellipse(cx + 70 * s, cy + 2 * s, 14 * s, 42 * s), ellipse(cx + 92 * s, cy + 2 * s,
                                                                                  14 * s, 40 * s)],
                         color=BAND, width=8))
    return out


# ------------------------------------------------------------------ boards

def l_hook():
    """The challenge is on the board from frame one; the rest draws as it is said."""
    grownup = kid(290, 1050, 0.95, "think", "chin")
    grownup[0].at("smarter")
    return [
        Text("ARE YOU SMARTER THAN A KIDS' TRIVIA BOOK?", (540, 380), size=84, face=MARKER, color=RED,
             max_width=980).ready(),
        *grownup,
        Text("VS", (540, 860), size=110, face=MARKER, color=GOLD).at("book").pop(),
        Picture(cover(), (790, 860), width=250, angle=5, tape=True).at("trivia"),
        tag("3 facts · 1 is fake", (540, 620), size=70, color=TEAL).at("three").pop(),
    ]


def l_one():
    y = ROWS[0]
    return [*number(1, y), *[a.at("ants") if k == 0 else a for k, a in enumerate(ant(270, y, 1.1))],
            claim("Ants never sleep. They're the only insect awake 24 hours a day.", y, size=42)]


def l_two():
    y = ROWS[1]
    return [*number(2, y), *[g.at("goats") if k == 0 else g for k, g in enumerate(goat(270, y + 10, 0.9))],
            claim("Goats have rectangular pupils that give them nearly 340-degree vision.", y, size=40)]


def l_three():
    y = ROWS[2]
    return [*number(3, y), *[c.at("rubber") if k == 0 else c for k, c in enumerate(croc(250, y, 1.0))],
            claim("A rubber band can hold a crocodile's mouth shut.", y, size=44)]


def l_r1():
    y = ROWS[0]
    return [*number(1, y), *ant(270, y, 1.1),
            stamp("FAKE!", y, RED).at("fake").pop(),
            note("Ants take hundreds of tiny micro-naps a day.", (450, y + 30), size=42, max_width=580,
                 anchor="lm").at("micro-naps"),
            Text("z z z", (200, y - 70), size=40, face=MARKER, color=GREY).at("hundreds")]


def l_r2():
    y = ROWS[1]
    return [*number(2, y), *goat(270, y + 10, 0.9),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("They see almost all the way around without moving their head.", (450, y + 45), size=38,
                 max_width=580, anchor="lm").at("see")]


def l_r3():
    y = ROWS[2]
    return [*number(3, y), *croc(250, y, 1.0),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("Huge bite, but the muscles that open the jaw are weak.", (450, y + 40), size=40, max_width=580,
                 anchor="lm").at("muscles"),
            Shape([ellipse(320, y + 2, 14, 42), ellipse(342, y + 2, 14, 40)],
                  color=(170, 80, 200), width=8).at("weak")]


def l_score():
    return [
        tag("how many did you get?", (540, 420), size=72, color=INK).at("how"),
        Text("0 · 1 · 2 · 3", (540, 640), size=130, face=MARKER, color=GOLD).pop(),
        tag("comment your score", (540, 860), size=64, color=TEAL).at("did").pop(),
    ]


def l_find():
    return [
        Picture(cover(), (540, 640), width=330, angle=-2, tape=True).at("one"),
        Picture(page("q06.png"), (190, 700), width=230, angle=-7).at("page"),
        Picture(page("a06.png"), (890, 700), width=230, angle=7),
        tag("where to find it:", (540, 975), size=50, color=GREY).at("book"),
        tag("search “Trick Trivia”", (540, 1060), size=60, color=TEAL).at("trivia").pop(),
        tag("on Amazon", (540, 1140), size=60, color=TEAL).at("kids").pop(),
    ]


SCRIPT = [
    ("Are you smarter than a kids' trivia book? Three facts, one is fake.", l_hook),
    ("One: Ants never sleep. They're the only insect that stays awake twenty-four hours a day.", l_one),
    ("Two: Goats have rectangular pupils that give them nearly three hundred and forty degree vision.", l_two,
     KEEP),
    ("Three: A rubber band can hold a crocodile's mouth shut.", l_three, KEEP),
    ("Lock in your guess. Three, two, one.", l_lock),
    ("Ants? Fake! Ants do sleep. They take hundreds of tiny micro-naps a day.", l_r1),
    ("Goats? Real. They can see almost all the way around without moving their head.", l_r2, KEEP),
    ("Crocodiles? Real. Their bite is huge, but the muscles that open the jaw are so weak a rubber "
     "band can hold it shut.", l_r3, KEEP),
    ("So how many did you get? Comment your score.", l_score),
    ("That was one page of a book called Trick Trivia, it's for kids, and it's on Amazon.", l_find),
]

CAPTION = (
    "Are you smarter than a kids' trivia book? Three facts, one is fake: ants never sleep, goats "
    "have rectangular pupils with nearly 340-degree vision, and a rubber band can hold a "
    "crocodile's mouth shut. Comment your score out of 3, then try it on your kid. It's from "
    "Trick Trivia, a real-or-fake book for kids, on Amazon."
)
HASHTAGS = ["#realorfake", "#trivia", "#funfacts", "#areyousmarter", "#momtok", "#dadtok",
            "#familygame"]
