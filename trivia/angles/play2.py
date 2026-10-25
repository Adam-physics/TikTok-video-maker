"""Play-along video from the flamingo / polar bear / octopus page.

Same shape as play1 but stands on its own. The claims and answers are copied from the printed
page (assets/pages/q01.png and a01.png).
"""
from __future__ import annotations

from ..doodle import Picture, Shape
from ..explainer import KEEP
from ..figures import hollow_hair, page, polar_bear
from .meltdown import flamingo
from .play1 import CHIP, FOOTER, ROWS, claim, l_cta, l_hook, l_lock, number, stamp
from .reading import BLUE, GREEN, GREY, RED, TEAL, note, tag
from .screens import octopus

ID = "play2"
TIGHTEN = 0.2


def l_one():
    y = ROWS[0]
    return [*number(1, y), *[f.at("flamingos") if k == 0 else f for k, f in enumerate(flamingo(250, y + 10, 0.55))],
            claim("A group of flamingos is called a flamboyance.", y)]


def l_two():
    y = ROWS[1]
    return [*number(2, y), *[b.at("polar") if k == 0 else b for k, b in enumerate(polar_bear(270, y - 55, 0.36))],
            claim("Polar bears have white fur.", y)]


def l_three():
    y = ROWS[2]
    return [*number(3, y), *[o.at("octopuses") if k == 0 else o for k, o in enumerate(octopus(270, y - 40, 0.48))],
            claim("Octopuses have three hearts and blue blood.", y)]


def l_r1():
    y = ROWS[0]
    return [*number(1, y), *flamingo(250, y + 10, 0.55),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("It's the official name.", (450, y + 30), size=44, max_width=580, anchor="lm").at("official")]


def l_r2():
    y = ROWS[1]
    return [*number(2, y), *polar_bear(270, y - 55, 0.36),
            stamp("FAKE!", y, RED).at("fake").pop(),
            note("The fur is see-through and hollow.", (450, y + 40), size=44, max_width=580, anchor="lm")
            .at("see-through"),
            hollow_hair((640, y + 120), (900, y + 108), 16, color=BLUE).at("hollow"),
            note("It just reflects the light.", (450, y + 170), size=40, color=GREY, max_width=580, anchor="lm")
            .at("reflects")]


def l_r3():
    y = ROWS[2]
    return [*number(3, y), *octopus(270, y - 40, 0.48),
            stamp("REAL!", y, GREEN).at("real").pop(),
            note("3 hearts. Blue blood (copper, not iron).", (450, y + 30), size=42, max_width=580,
                 anchor="lm").at("three")]


def l_page():
    return [
        tag("that was ONE page", (540, 360), size=70, color=TEAL).at("one").pop(),
        Picture(page("q01.png"), (320, 780), width=400, angle=-4, tape=True).at("page").focus(1.06),
        Picture(page("a01.png"), (770, 800), width=400, angle=4, tape=True).at("trick"),
    ]


SCRIPT = [
    ("Play this with your kid. Three facts, one is fake. Bet they beat you.", l_hook),
    ("One: A group of flamingos is called a flamboyance.", l_one),
    ("Two: Polar bears have white fur.", l_two, KEEP),
    ("Three: Octopuses have three hearts and blue blood.", l_three, KEEP),
    ("Lock in your guess. Three, two, one.", l_lock),
    ("Flamingos? Real. It's the official name.", l_r1),
    ("Polar bears? Fake! Their fur is actually see-through and hollow. It only looks white "
     "because it reflects the light.", l_r2, KEEP),
    ("Octopuses? Real. Three hearts, and blue blood, because it has copper instead of iron.",
     l_r3, KEEP),
    ("That was one page of Trick Trivia, a real-or-fake book for kids.", l_page),
    ("There are a hundred and twenty claims inside. Grab your copy on Amazon.", l_cta),
]

CAPTION = (
    "Play this with your kid: three facts, one is fake. A group of flamingos is called "
    "a flamboyance. Polar bears have white fur. Octopuses have three hearts and blue blood. "
    "Lock in your guess, then watch the reveal (the middle one gets almost everybody). That was "
    "one page of Trick Trivia, a real-or-fake book for kids with 120 claims inside. Grab your "
    "copy on Amazon. Comment your score out of 3!"
)
HASHTAGS = ["#realorfake", "#funfacts", "#kidsbooks", "#familygame", "#momtok", "#dadtok",
            "#didyouknow"]
