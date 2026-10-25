"""Angle: play a real page of the book, then see it.

The video is the product: three claims from one page of Trick Trivia, a
lock-in, the reveal with the book's own explanations, and then the real page
taped to the board. The claims and answers are copied from the printed page
(assets/pages/q02.png and a02.png), so nothing on screen goes beyond the book.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arc, circle, ellipse, line, poly, rrect, star
from ..explainer import KEEP
from ..figures import cover, kid, page
from .guess import snail
from .reading import BLUE, GOLD, GREEN, GREY, RED, TEAL, W, note, tag

ID = "play1"
TIGHTEN = 0.2
CHIP = "PLAY ALONG WITH YOUR KID"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
DOLPHIN = (150, 180, 215)
BAT = (120, 100, 130)
ROWS = (500, 790, 1080)


def dolphin(cx, cy, s=0.6):
    body = [(cx - 160 * s, cy + 10 * s), (cx - 80 * s, cy - 50 * s), (cx + 40 * s, cy - 60 * s),
            (cx + 140 * s, cy - 20 * s), (cx + 170 * s, cy), (cx + 120 * s, cy + 20 * s), (cx, cy + 40 * s),
            (cx - 120 * s, cy + 30 * s)]
    return [Shape(poly(body, closed=True, wobble=1.0), color=(70, 100, 150), fill=DOLPHIN, width=6,
                  fill_offset=(0, 0)),
            Shape([poly([(cx - 10 * s, cy - 55 * s), (cx + 20 * s, cy - 110 * s), (cx + 40 * s, cy - 58 * s)],
                        wobble=0.6),
                   poly([(cx - 150 * s, cy + 10 * s), (cx - 200 * s, cy - 30 * s), (cx - 190 * s, cy + 20 * s),
                         (cx - 200 * s, cy + 60 * s), (cx - 150 * s, cy + 20 * s)], wobble=0.6)],
                  color=(70, 100, 150), width=6),
            Shape([circle(cx + 100 * s, cy - 18 * s, 8 * s, wobble=0.2)], fill=INK, width=4, fill_offset=(0, 0)),
            Text("z z", (cx + 150 * s, cy - 110 * s), size=40, face=MARKER, color=GREY)]


def bat(cx, cy, s=1.0):
    left = [(cx - 30 * s, cy - 10 * s), (cx - 150 * s, cy - 60 * s), (cx - 130 * s, cy - 10 * s),
            (cx - 100 * s, cy + 10 * s), (cx - 70 * s, cy), (cx - 40 * s, cy + 25 * s)]
    right = [(x if i < 0 else 2 * cx - x, y) for i, (x, y) in enumerate(left)]
    return [Shape([poly(left, closed=True, wobble=0.8), poly(right, closed=True, wobble=0.8)], color=(70, 55, 80),
                  fill=BAT, width=6, fill_offset=(0, 0)),
            Shape([ellipse(cx, cy + 5 * s, 38 * s, 46 * s),
                   poly([(cx - 26 * s, cy - 30 * s), (cx - 34 * s, cy - 70 * s), (cx - 8 * s, cy - 40 * s)],
                        closed=True, wobble=0.4),
                   poly([(cx + 26 * s, cy - 30 * s), (cx + 34 * s, cy - 70 * s), (cx + 8 * s, cy - 40 * s)],
                        closed=True, wobble=0.4)], color=(70, 55, 80), fill=BAT, width=6, fill_offset=(0, 0)),
            Shape([rrect(cx - 30 * s, cy - 14 * s, cx - 4 * s, cy + 2 * s, r=4),
                   rrect(cx + 4 * s, cy - 14 * s, cx + 30 * s, cy + 2 * s, r=4)], fill=INK, width=4,
                  fill_offset=(0, 0))]


def number(n, y):
    return [Shape(circle(75, y, 40), width=7, fill=(255, 255, 255), fill_offset=(0, 0)),
            Text(str(n), (75, y + 4), size=54, face=MARKER, color=INK)]


def claim(text, y, size=48):
    return note(text, (450, y), size=size, max_width=580, anchor="lm")


def stamp(word, y, color):
    return tag(word, (450, y - 50), size=64, color=color, anchor="lm")


# ------------------------------------------------------------------ boards

def l_hook():
    """Only the headline is there on frame one; the rest draws as it is said."""
    child = kid(800, 1090, 0.75, "happy", "up")
    child[0].at("kid")
    return [
        Text("REAL OR FAKE?", (540, 330), size=110, face=MARKER, color=GOLD).ready(),
        *kid(300, 1060, 0.95, "think", "chin"),
        *child,
        tag("3 facts · 1 is fake", (540, 500), size=70, color=RED).at("three").pop(),
        Shape(star(800, 780, 46, seed=4), color=GOLD, fill=GOLD, width=5).at("beat"),
        tag("bet they win!", (800, 680), size=52, color=TEAL).pop(),
    ]


def l_one():
    y = ROWS[0]
    return [*number(1, y), *[d.at("dolphins") if k == 0 else d for k, d in enumerate(dolphin(290, y, 0.72))],
            claim("Dolphins sleep with one eye open.", y)]


def l_two():
    y = ROWS[1]
    return [*number(2, y), *[p.at("snail") if k == 0 else p for k, p in enumerate(snail(265, y + 40, 0.5))],
            claim("A snail can sleep for up to three years.", y)]


def l_three():
    y = ROWS[2]
    return [*number(3, y), *[b.at("bats") if k == 0 else b for k, b in enumerate(bat(270, y, 1.05))],
            claim("Bats are blind. (That's where “blind as a bat” comes from.)", y, size=44)]


def l_lock():
    return [
        Text("LOCK IN", (540, 380), size=110, face=MARKER, color=RED).at("lock").focus(1.06),
        Text("YOUR GUESS!", (540, 500), size=110, face=MARKER, color=RED).pop(),
        Text("3", (300, 760), size=180, face=MARKER, color=INK).at("three").pop(),
        Text("2", (540, 760), size=180, face=MARKER, color=INK).at("two").pop(),
        Text("1", (780, 760), size=180, face=MARKER, color=INK).at("one").pop(),
    ]


def l_r1():
    y = ROWS[0]
    return [*number(1, y), *dolphin(290, y, 0.72),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("They rest half their brain at a time.", (450, y + 30), size=44, max_width=580, anchor="lm").at("rest")]


def l_r2():
    y = ROWS[1]
    return [*number(2, y), *snail(265, y + 40, 0.5),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("They hibernate for years, waiting for rain.", (450, y + 30), size=44, max_width=580, anchor="lm")
            .at("hibernate")]


def l_r3():
    y = ROWS[2]
    waves = Shape([arc(330, y + 70, 30, 40, -50, 50), arc(330, y + 70, 55, 70, -50, 50), arc(330, y + 70, 80, 100, -50, 50)],
                  color=BLUE, width=6)
    return [*number(3, y), *bat(270, y, 1.05),
            stamp("FAKE!", y, RED).at("fake").pop(),
            note("Bats can see just fine.", (450, y + 20), size=46, max_width=580, anchor="lm").at("see"),
            waves.at("echolocation"),
            note("Echolocation is extra, not instead.", (450, y + 80), size=40, color=GREY, max_width=580, anchor="lm")
            .at("top")]


def l_page():
    return [
        tag("that was ONE page", (540, 360), size=70, color=TEAL).at("one").pop(),
        Picture(page("q02.png"), (320, 780), width=400, angle=-4, tape=True).at("page").focus(1.06),
        Picture(page("a02.png"), (770, 800), width=400, angle=4, tape=True).at("trick"),
    ]


def l_cta():
    return [
        Picture(cover(), (540, 700), width=400, angle=-2, tape=True),
        tag("120 claims inside", (540, 330), size=72, color=RED).at("hundred").pop(),
        tag("Grab your copy on Amazon", (540, 1110), size=60, color=TEAL).at("grab").focus(1.04).pop(),
    ]


SCRIPT = [
    ("Play this with your kid. Three facts, one is fake. Bet they beat you.", l_hook),
    ("One: Dolphins sleep with one eye open.", l_one),
    ("Two: A snail can sleep for up to three years.", l_two, KEEP),
    ("Three: Bats are blind. That's where “blind as a bat” comes from.", l_three, KEEP),
    ("Lock in your guess. Three, two, one.", l_lock),
    ("Dolphins? Real. They rest half their brain at a time.", l_r1),
    ("Snails? Real. They can hibernate for years, waiting for rain.", l_r2, KEEP),
    ("Bats? Fake! Bats can see just fine. They use echolocation on top of their eyes, not "
     "instead of them.", l_r3, KEEP),
    ("That was one page of Trick Trivia, a real-or-fake book for kids.", l_page),
    ("There are a hundred and twenty claims inside. Grab your copy on Amazon.", l_cta),
]

CAPTION = (
    "Play this with your kid: three facts, one is fake. Dolphins sleep with one eye open. A "
    "snail can sleep for up to three years. Bats are blind. Lock in your guess, then watch the "
    "reveal (almost everyone gets fooled by the last one). That was one page of Trick Trivia, "
    "a real-or-fake book for kids with 120 claims inside. Grab your copy on Amazon. Comment "
    "your score out of 3!"
)
HASHTAGS = ["#realorfake", "#funfacts", "#kidsbooks", "#familygame", "#momtok", "#dadtok",
            "#didyouknow"]
