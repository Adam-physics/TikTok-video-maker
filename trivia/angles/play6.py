"""Dark-board play-along from book page 13 (sharks vs trees / owls / cats), short script.

Same shape as play5: challenge hook, short claims, one-line reveals, comment
bait, then "for more facts like this". Claims and answers follow the printed
pages (q07.png, a07.png).
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arc, circle, curve, ellipse, line, poly
from ..explainer import KEEP
from ..figures import cover, kid, page
from .bored import tree
from .play1 import CHIP, FOOTER, ROWS, claim, l_lock, number, stamp
from .play4 import shark
from .reading import GOLD, GREEN, GREY, RED, TEAL, note, tag

ID = "play6"
TIGHTEN = 0.2
OWL = (170, 120, 80)
CAT_COLORS = [(240, 160, 70), (150, 150, 160), (90, 90, 100)]


def owl(cx, cy, s=1.0):
    return [
        Shape(ellipse(cx, cy + 20 * s, 60 * s, 75 * s), color=(110, 75, 45), fill=OWL, width=6, fill_offset=(0, 0)),
        Shape([poly([(cx - 50 * s, cy - 30 * s), (cx - 60 * s, cy - 80 * s), (cx - 25 * s, cy - 50 * s)],
                    closed=True, wobble=0.4),
               poly([(cx + 50 * s, cy - 30 * s), (cx + 60 * s, cy - 80 * s), (cx + 25 * s, cy - 50 * s)],
                    closed=True, wobble=0.4)], color=(110, 75, 45), fill=OWL, width=5, fill_offset=(0, 0)),
        Shape([circle(cx - 24 * s, cy - 18 * s, 20 * s), circle(cx + 24 * s, cy - 18 * s, 20 * s)],
              color=(110, 75, 45), fill=(250, 210, 80), width=5, fill_offset=(0, 0)),
        Shape([circle(cx - 24 * s, cy - 18 * s, 7 * s, wobble=0.2), circle(cx + 24 * s, cy - 18 * s, 7 * s, wobble=0.2)],
              fill=INK, width=3, fill_offset=(0, 0)),
        Shape(poly([(cx - 8 * s, cy + 2 * s), (cx + 8 * s, cy + 2 * s), (cx, cy + 18 * s)], closed=True,
                   wobble=0.2), color=(200, 130, 30), fill=(240, 160, 40), width=3, fill_offset=(0, 0)),
    ]


def spin_arrow(cx, cy, r, sweep):
    """A curved arrow round the owl's head; `sweep` in degrees."""
    a0 = -90
    return Shape([arc(cx, cy, r, r * 0.45, a0, a0 + sweep, wobble=0.6)], color=TEAL, width=7)


def cat(cx, cy, s, color):
    return [
        Shape(circle(cx, cy, 34 * s), color=(60, 60, 60), fill=color, width=5, fill_offset=(0, 0)),
        Shape([poly([(cx - 30 * s, cy - 14 * s), (cx - 26 * s, cy - 48 * s), (cx - 8 * s, cy - 30 * s)],
                    closed=True, wobble=0.3),
               poly([(cx + 30 * s, cy - 14 * s), (cx + 26 * s, cy - 48 * s), (cx + 8 * s, cy - 30 * s)],
                    closed=True, wobble=0.3)], color=(60, 60, 60), fill=color, width=4, fill_offset=(0, 0)),
        Shape([circle(cx - 12 * s, cy - 4 * s, 4 * s, wobble=0.1), circle(cx + 12 * s, cy - 4 * s, 4 * s, wobble=0.1)],
              fill=INK, width=3, fill_offset=(0, 0)),
        Shape([line((cx - 6 * s, cy + 10 * s), (cx - 34 * s, cy + 6 * s)),
               line((cx + 6 * s, cy + 10 * s), (cx + 34 * s, cy + 6 * s))], width=3),
    ]


def cats(cx, cy):
    out = []
    for k, (dx, dy) in enumerate(((-75, 10), (0, -10), (75, 10))):
        out += cat(cx + dx, cy + dy, 1.0, CAT_COLORS[k])
    return out


# ------------------------------------------------------------------ boards

def l_hook():
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
    return [*number(1, y), *[f.at("sharks") if k == 0 else f for k, f in enumerate(shark(215, y + 10, 0.5))],
            *[t.at("older") if k == 0 else t for k, t in enumerate(tree(365, y - 5, 0.5))],
            claim("Sharks are older than trees.", y, size=50)]


def l_two():
    y = ROWS[1]
    return [*number(2, y), *[o.at("owls") if k == 0 else o for k, o in enumerate(owl(270, y + 5, 0.95))],
            spin_arrow(270, y - 95, 85, 340).at("full"),
            claim("Owls can turn their heads a full 360°.", y, size=48)]


def l_three():
    y = ROWS[2]
    return [*number(3, y), *[c.at("group") if k == 0 else c for k, c in enumerate(cats(270, y + 10))],
            claim("A group of cats is called a clowder.", y, size=48)]


def l_r1():
    y = ROWS[0]
    return [*number(1, y), *shark(215, y + 10, 0.5), *tree(365, y - 5, 0.5),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("450 vs. 350 million years.", (450, y + 35), size=44, max_width=580, anchor="lm").at("by")]


def l_r2():
    y = ROWS[1]
    return [*number(2, y), *owl(270, y + 5, 0.95), spin_arrow(270, y - 95, 85, 340),
            stamp("FAKE!", y, RED).at("fake").pop(),
            note("Only 270°.", (450, y + 35), size=48, max_width=580, anchor="lm").at("only"),
            Shape(line((180, y - 120), (360, y + 40)), color=RED, width=9)]


def l_r3():
    y = ROWS[2]
    return [*number(3, y), *cats(270, y + 10),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("And kittens? A kindle.", (450, y + 35), size=44, max_width=580, anchor="lm").at("kittens")]


def l_score():
    return [
        tag("how many did you get?", (540, 420), size=72, color=INK).at("how"),
        Text("0 · 1 · 2 · 3", (540, 640), size=130, face=MARKER, color=GOLD).pop(),
        tag("comment your score", (540, 860), size=64, color=TEAL).at("comment").pop(),
    ]


def l_find():
    return [
        Picture(cover(), (540, 640), width=330, angle=-2, tape=True).at("more"),
        Picture(page("q07.png"), (190, 700), width=230, angle=-7).at("facts"),
        Picture(page("a07.png"), (890, 700), width=230, angle=7),
        tag("where to find it:", (540, 975), size=50, color=GREY).at("like"),
        tag("search “Trick Trivia”", (540, 1060), size=60, color=TEAL).at("grab").pop(),
        tag("on Amazon", (540, 1140), size=60, color=TEAL).at("trick").pop(),
    ]


SCRIPT = [
    ("Are you smarter than a kids' trivia book? Three facts, one is fake.", l_hook),
    ("One: Sharks are older than trees.", l_one),
    ("Two: Owls can turn their heads a full three-sixty.", l_two, KEEP),
    ("Three: A group of cats is called a clowder.", l_three, KEEP),
    ("Lock in your guess. Three, two, one.", l_lock),
    ("Sharks? Real. By about a hundred million years.", l_r1),
    ("Owls? Fake! Only two-seventy.", l_r2, KEEP),
    ("Cats? Real. And a group of kittens is a kindle.", l_r3, KEEP),
    ("How many did you get? Comment your score.", l_score),
    ("For more facts like this, grab Trick Trivia on Amazon.", l_find),
]

CAPTION = (
    "Are you smarter than a kids' trivia book? 3 facts, 1 is fake: sharks are older than trees, "
    "owls can turn their heads a full 360, and a group of cats is called a clowder. Comment your "
    "score out of 3, then try it on your kid. For more facts like this, grab Trick Trivia on Amazon."
)
HASHTAGS = ["#realorfake", "#trivia", "#funfacts", "#momtok", "#dadtok", "#familygame", "#kidsbooks"]
