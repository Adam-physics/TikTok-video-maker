"""Play-along video from book page 7: sharks / butterflies / horses, in a parent's voice.

The narration is a parent sharing the game their kid asks for at dinner, and the
ending is a recommendation ("it's called Trick Trivia, it's on Amazon"), not a
pitch. Claims and answers are copied from the printed pages (q04.png, a04.png).
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arc, circle, curve, ellipse, line, poly, rrect
from ..explainer import KEEP
from ..figures import cover, kid, page
from .play1 import CHIP, FOOTER, ROWS, claim, l_lock, number, stamp
from .reading import BLUE, GOLD, GREEN, GREY, RED, TEAL, note, tag
from .reading import W

ID = "play4"
TIGHTEN = 0.2
SHARK = (150, 170, 195)
WING = (245, 160, 50)
HORSE = (160, 110, 70)


def shark(cx, cy, s=1.0):
    body = [(cx - 150 * s, cy), (cx - 60 * s, cy - 40 * s), (cx + 60 * s, cy - 40 * s), (cx + 140 * s, cy - 6 * s),
            (cx + 150 * s, cy + 8 * s), (cx + 60 * s, cy + 34 * s), (cx - 60 * s, cy + 30 * s)]
    return [
        Shape(poly(body, closed=True, wobble=1.0), color=(80, 95, 125), fill=SHARK, width=6, fill_offset=(0, 0)),
        Shape([poly([(cx - 10 * s, cy - 38 * s), (cx + 20 * s, cy - 100 * s), (cx + 40 * s, cy - 40 * s)],
                    wobble=0.6),
               poly([(cx - 145 * s, cy), (cx - 195 * s, cy - 50 * s), (cx - 180 * s, cy + 4 * s),
                     (cx - 195 * s, cy + 50 * s), (cx - 145 * s, cy + 10 * s)], wobble=0.6)],
              color=(80, 95, 125), fill=SHARK, width=6, fill_offset=(0, 0)),
        Shape(circle(cx + 95 * s, cy - 10 * s, 9 * s, wobble=0.2), fill=INK, width=4, fill_offset=(0, 0)),
        Shape(poly([(cx + 70 * s, cy + 18 * s), (cx + 90 * s, cy + 12 * s), (cx + 110 * s, cy + 18 * s),
                    (cx + 130 * s, cy + 12 * s)], wobble=0.4), width=4),
    ]


def butterfly(cx, cy, s=1.0):
    return [
        Shape([ellipse(cx - 50 * s, cy - 30 * s, 50 * s, 42 * s, rot=-20), ellipse(cx + 50 * s, cy - 30 * s, 50 * s,
                                                                                   42 * s, rot=20),
               ellipse(cx - 40 * s, cy + 30 * s, 34 * s, 28 * s, rot=20), ellipse(cx + 40 * s, cy + 30 * s, 34 * s,
                                                                                  28 * s, rot=-20)],
              color=(150, 80, 20), fill=WING, width=5, fill_offset=(0, 0)),
        Shape(ellipse(cx, cy, 10 * s, 52 * s), fill=INK, width=4, fill_offset=(0, 0)),
        Shape([curve([(cx - 4 * s, cy - 50 * s), (cx - 20 * s, cy - 80 * s), (cx - 30 * s, cy - 86 * s)]),
               curve([(cx + 4 * s, cy - 50 * s), (cx + 20 * s, cy - 80 * s), (cx + 30 * s, cy - 86 * s)])], width=4),
        Shape([line((cx - 6 * s, cy + 40 * s), (cx - 24 * s, cy + 76 * s)),
               line((cx + 6 * s, cy + 40 * s), (cx + 24 * s, cy + 76 * s))], width=4),
    ]


def horse(cx, cy, s=1.0):
    head = [(cx - 70 * s, cy - 90 * s), (cx - 30 * s, cy - 120 * s), (cx + 20 * s, cy - 90 * s),
            (cx + 100 * s, cy - 10 * s), (cx + 110 * s, cy + 30 * s), (cx + 70 * s, cy + 50 * s),
            (cx - 20 * s, cy + 10 * s), (cx - 70 * s, cy + 90 * s), (cx - 110 * s, cy + 90 * s),
            (cx - 100 * s, cy - 20 * s)]
    return [
        Shape(poly(head, closed=True, wobble=1.0), color=(100, 65, 40), fill=HORSE, width=6, fill_offset=(0, 0)),
        Shape([poly([(cx - 50 * s, cy - 100 * s), (cx - 40 * s, cy - 150 * s), (cx - 20 * s, cy - 105 * s)],
                    closed=True, wobble=0.4)], color=(100, 65, 40), fill=HORSE, width=5, fill_offset=(0, 0)),
        Shape(curve([(cx - 70 * s, cy - 100 * s), (cx - 120 * s, cy - 40 * s), (cx - 130 * s, cy + 40 * s)],
                    wobble=0.8), color=(70, 45, 30), width=12),
        Shape(circle(cx + 10 * s, cy - 60 * s, 8 * s, wobble=0.2), fill=INK, width=4, fill_offset=(0, 0)),
        Shape(ellipse(cx + 92 * s, cy + 10 * s, 7 * s, 5 * s, wobble=0.2), fill=INK, width=3, fill_offset=(0, 0)),
    ]


def puffs(cx, cy, s=1.0):
    return Shape([circle(cx, cy, 14 * s, wobble=0.6), circle(cx + 26 * s, cy - 8 * s, 18 * s, wobble=0.6),
                  circle(cx + 56 * s, cy - 2 * s, 14 * s, wobble=0.6)], color=GREY, width=4)


def table(dy=-130):
    """The dinner table, lifted clear of the captions."""
    return [Shape(rrect(110, 1050 + dy, 970, 1200 + dy, r=14), width=W, fill=(255, 255, 255),
                  fill_offset=(0, 0)),
            Shape([line((330, 1095 + dy), (322, 1195 + dy)), line((540, 1095 + dy), (540, 1195 + dy)),
                   line((750, 1095 + dy), (758, 1195 + dy))], color=GREY, width=5),
            Shape([ellipse(450, 1044 + dy, 64, 14, wobble=0.6), ellipse(680, 1044 + dy, 64, 14, wobble=0.6)],
                  width=6)]


# ------------------------------------------------------------------ boards

def l_hook():
    """Only the headline is there on frame one; dinner draws in as it is said."""
    child = kid(760, 880, 0.75, "happy", "up")
    child[0].at("kid")
    return [
        Text("REAL OR FAKE?", (540, 330), size=110, face=MARKER, color=GOLD).ready(),
        *kid(300, 860, 0.95, "think", "chin"),
        *child,
        *[t.at("dinner") if k == 0 else t for k, t in enumerate(table())],
        tag("3 facts · 1 is fake", (540, 470), size=70, color=RED).at("three").pop(),
    ]


def l_one():
    y = ROWS[0]
    return [*number(1, y), *[f.at("sharks") if k == 0 else f for k, f in enumerate(shark(280, y, 0.8))],
            claim("Sharks are the only fish that can blink.", y)]


def l_two():
    y = ROWS[1]
    return [*number(2, y), *[b.at("butterfly") if k == 0 else b for k, b in enumerate(butterfly(270, y, 1.0))],
            claim("A butterfly can taste with its feet.", y)]


def l_three():
    y = ROWS[2]
    return [*number(3, y), *[h.at("horse") if k == 0 else h for k, h in enumerate(horse(260, y, 0.85))],
            claim("A horse cannot breathe through its mouth.", y)]


def l_r1():
    y = ROWS[0]
    return [*number(1, y), *shark(280, y, 0.8),
            stamp("FAKE!", y, RED).at("fake").pop(),
            note("Sharks don't blink at all.", (450, y + 25), size=44, max_width=580, anchor="lm").at("blink"),
            note("Some have an eye membrane. Not the same thing.", (450, y + 110), size=36, color=GREY,
                 max_width=580, anchor="lm").at("membrane")]


def l_r2():
    y = ROWS[1]
    return [*number(2, y), *butterfly(270, y, 1.0),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("Sensors on their feet taste the leaf.", (450, y + 30), size=44, max_width=580, anchor="lm")
            .at("sensors")]


def l_r3():
    y = ROWS[2]
    return [*number(3, y), *horse(260, y, 0.85),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("They can only breathe through their nose.", (450, y + 30), size=44, max_width=580,
                 anchor="lm").at("only"),
            puffs(355, y + 25, 1.0)]


def l_find():
    return [
        Picture(cover(), (540, 640), width=330, angle=-2, tape=True).at("book"),
        Picture(page("q04.png"), (190, 700), width=230, angle=-7).at("trivia"),
        Picture(page("a04.png"), (890, 700), width=230, angle=7),
        tag("where to find it:", (540, 975), size=50, color=GREY).at("every"),
        tag("search “Trick Trivia”", (540, 1060), size=60, color=TEAL).at("page").pop(),
        tag("on Amazon", (540, 1140), size=60, color=TEAL).pop(),
    ]


SCRIPT = [
    ("Okay, this is the game my kid begs to play at dinner. Three facts, one is fake.", l_hook),
    ("One: Sharks are the only fish that can blink.", l_one),
    ("Two: A butterfly can taste with its feet.", l_two, KEEP),
    ("Three: A horse cannot breathe through its mouth.", l_three, KEEP),
    ("Lock in your guess. Three, two, one.", l_lock),
    ("Sharks? Fake! Sharks don't blink at all. Some have a membrane that covers the eye, but "
     "that's not the same thing.", l_r1),
    ("Butterflies? Real. Sensors on their feet taste whether a leaf is good for their eggs.", l_r2,
     KEEP),
    ("Horses? Real. They can only breathe through their nose.", l_r3, KEEP),
    ("It's a book called Trick Trivia, and every page is like this. It's on Amazon.", l_find),
]

CAPTION = (
    "This is the game my kid begs to play at dinner. Three facts, one is fake: sharks are the "
    "only fish that can blink, a butterfly can taste with its feet, and a horse can't breathe "
    "through its mouth. Did you get it? It's a book called Trick Trivia, every page is like "
    "this, and it's on Amazon if you want it for your own dinner table."
)
HASHTAGS = ["#realorfake", "#funfacts", "#familygame", "#dinnertable", "#momtok", "#dadtok",
            "#screenfreekids"]
