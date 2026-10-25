"""Play-along video from book page 5: wombats / penguins / mantis shrimp.

Same shape as play1 and stands on its own. The claims and answers are copied
from the printed pages (assets/pages/q03.png and a03.png).
"""
from __future__ import annotations

from ..doodle import INK, Picture, Shape, Text, circle, curve, ellipse, heart, line, poly, rrect
from ..explainer import KEEP
from ..figures import page
from .play1 import CHIP, FOOTER, ROWS, claim, l_cta, l_hook, l_lock, number, stamp
from .reading import GREY, GREEN, RED, TEAL, note, tag

ID = "play3"
TIGHTEN = 0.2
FUR = (170, 130, 95)
POOP = (130, 90, 60)
SHRIMP = (90, 190, 160)
GLOVE = (220, 50, 50)


def wombat(cx, cy, s=1.0):
    return [
        Shape(ellipse(cx - 20 * s, cy + 20 * s, 95 * s, 65 * s), color=(110, 80, 55), fill=FUR, width=6,
              fill_offset=(0, 0)),
        Shape(circle(cx + 60 * s, cy - 30 * s, 48 * s), color=(110, 80, 55), fill=FUR, width=6, fill_offset=(0, 0)),
        Shape([circle(cx + 30 * s, cy - 72 * s, 14 * s, wobble=0.4), circle(cx + 88 * s, cy - 72 * s, 14 * s,
                                                                             wobble=0.4)],
              color=(110, 80, 55), fill=FUR, width=5, fill_offset=(0, 0)),
        Shape(ellipse(cx + 90 * s, cy - 20 * s, 18 * s, 13 * s, wobble=0.3), fill=INK, width=4, fill_offset=(0, 0)),
        Shape(circle(cx + 62 * s, cy - 40 * s, 6 * s, wobble=0.2), fill=INK, width=4, fill_offset=(0, 0)),
        Shape([rrect(cx - 150 * s + k * 34 * s, cy + 60 * s, cx - 122 * s + k * 34 * s, cy + 88 * s, r=3)
               for k in range(3)] + [rrect(cx - 133 * s, cy + 30 * s, cx - 105 * s, cy + 58 * s, r=3)],
              color=(90, 60, 40), fill=POOP, width=4, fill_offset=(0, 0)),
    ]


def penguin(cx, cy, s=1.0):
    return [
        Shape(ellipse(cx, cy + 15 * s, 40 * s, 58 * s), fill=(40, 44, 56), width=5, fill_offset=(0, 0)),
        Shape(ellipse(cx, cy + 24 * s, 26 * s, 44 * s), fill=(255, 255, 255), width=4, fill_offset=(0, 0)),
        Shape(circle(cx, cy - 52 * s, 28 * s), fill=(40, 44, 56), width=5, fill_offset=(0, 0)),
        Shape([circle(cx - 10 * s, cy - 56 * s, 6 * s, wobble=0.2), circle(cx + 10 * s, cy - 56 * s, 6 * s,
                                                                            wobble=0.2)],
              fill=(255, 255, 255), width=3, fill_offset=(0, 0)),
        Shape(poly([(cx - 10 * s, cy - 44 * s), (cx + 10 * s, cy - 44 * s), (cx, cy - 30 * s)], closed=True,
                   wobble=0.3), color=(230, 140, 30), fill=(240, 160, 40), width=4, fill_offset=(0, 0)),
        Shape([ellipse(cx - 16 * s, cy + 76 * s, 14 * s, 6 * s), ellipse(cx + 16 * s, cy + 76 * s, 14 * s, 6 * s)],
              color=(230, 140, 30), fill=(240, 160, 40), width=3, fill_offset=(0, 0)),
    ]


def penguins(cx, cy, s=1.0):
    return [*penguin(cx - 55 * s, cy, s), *penguin(cx + 55 * s, cy, s),
            Shape(heart(cx, cy - 105 * s, 18 * s), color=RED, fill=(250, 140, 150), width=4)]


def mantis_shrimp(cx, cy, s=1.0):
    segs = [Shape(ellipse(cx - 100 * s + k * 34 * s, cy + 10 * s - k * 4 * s, 26 * s, 22 * s, wobble=0.6),
                  color=(40, 120, 100), fill=SHRIMP, width=5, fill_offset=(0, 0)) for k in range(5)]
    return [
        *segs,
        Shape([line((cx + 40 * s, cy - 14 * s), (cx + 20 * s, cy - 70 * s)),
               line((cx + 50 * s, cy - 14 * s), (cx + 56 * s, cy - 74 * s))], color=(40, 120, 100), width=5),
        Shape([circle(cx + 20 * s, cy - 74 * s, 8 * s, wobble=0.3), circle(cx + 56 * s, cy - 78 * s, 8 * s,
                                                                            wobble=0.3)],
              color=(40, 120, 100), fill=(250, 200, 60), width=4, fill_offset=(0, 0)),
        Shape(line((cx + 60 * s, cy), (cx + 100 * s, cy - 6 * s)), color=(40, 120, 100), width=8),
        Shape(circle(cx + 122 * s, cy - 8 * s, 26 * s), color=(150, 30, 30), fill=GLOVE, width=5,
              fill_offset=(0, 0)),
        Shape([line((cx + 158 * s, cy - 30 * s), (cx + 182 * s, cy - 44 * s)),
               line((cx + 162 * s, cy - 6 * s), (cx + 190 * s, cy - 6 * s)),
               line((cx + 158 * s, cy + 16 * s), (cx + 182 * s, cy + 30 * s))], color=(240, 170, 30), width=5),
    ]


def l_one():
    y = ROWS[0]
    return [*number(1, y), *[w.at("wombats") if k == 0 else w for k, w in enumerate(wombat(270, y, 1.0))],
            claim("Wombats produce cube-shaped poop.", y)]


def l_two():
    y = ROWS[1]
    return [*number(2, y), *[p.at("penguins") if k == 0 else p for k, p in enumerate(penguins(265, y + 20, 0.95))],
            claim("Penguins mate for life and never take a second partner.", y, size=44)]


def l_three():
    y = ROWS[2]
    return [*number(3, y), *[m.at("mantis") if k == 0 else m for k, m in enumerate(mantis_shrimp(250, y + 10,
                                                                                                  0.95))],
            claim("A mantis shrimp can punch with the speed and force of a bullet.", y, size=42)]


def l_r1():
    y = ROWS[0]
    return [*number(1, y), *wombat(270, y, 1.0),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("Their intestines shape it into cubes.", (450, y + 30), size=44, max_width=580, anchor="lm")
            .at("intestines")]


def l_r2():
    y = ROWS[1]
    return [*number(2, y), *penguins(265, y + 20, 0.95),
            stamp("FAKE!", y, RED).at("fake").pop(),
            note("Many species switch partners between seasons.", (450, y + 40), size=44, max_width=580,
                 anchor="lm").at("switch")]


def l_r3():
    y = ROWS[2]
    return [*number(3, y), *mantis_shrimp(250, y + 10, 0.95),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("Fast as a bullet. It can shatter aquarium glass.", (450, y + 40), size=42, max_width=580,
                 anchor="lm").at("shatter")]


def l_page():
    return [
        tag("that was ONE page", (540, 360), size=70, color=TEAL).at("one").pop(),
        Picture(page("q03.png"), (320, 780), width=400, angle=-4, tape=True).at("page").focus(1.06),
        Picture(page("a03.png"), (770, 800), width=400, angle=4, tape=True).at("trick"),
    ]


SCRIPT = [
    ("Play this with your kid. Three facts, one is fake. Bet they beat you.", l_hook),
    ("One: Wombats produce cube-shaped poop.", l_one),
    ("Two: Penguins mate for life and never take a second partner.", l_two, KEEP),
    ("Three: A mantis shrimp can punch with the speed and force of a bullet.", l_three, KEEP),
    ("Lock in your guess. Three, two, one.", l_lock),
    ("Wombats? Real. Their intestines shape it into cubes as it moves through.", l_r1),
    ("Penguins? Fake! Many penguin species actually switch partners between seasons.", l_r2, KEEP),
    ("Mantis shrimp? Real. Their punch is as fast as a bullet, strong enough to shatter aquarium "
     "glass.", l_r3, KEEP),
    ("That was one page of Trick Trivia, a real-or-fake book for kids.", l_page),
    ("There are a hundred and twenty claims inside. Grab your copy on Amazon.", l_cta),
]

CAPTION = (
    "Play this with your kid: three facts, one is fake. Wombats produce cube-shaped poop. "
    "Penguins mate for life and never take a second partner. A mantis shrimp can punch with the "
    "speed and force of a bullet. Lock in your guess, then watch the reveal. That was one page of "
    "Trick Trivia, a real-or-fake book for kids with 120 claims inside. Grab your copy on Amazon. "
    "Comment your score out of 3!"
)
HASHTAGS = ["#realorfake", "#funfacts", "#kidsbooks", "#familygame", "#momtok", "#dadtok",
            "#didyouknow"]
