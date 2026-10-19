"""Angle: reading comprehension for the kid who says reading is boring.

The promise: your kid reads every word, carefully, without being told to.
The mechanism, shown rather than claimed: a claim is a puzzle, one word
can be the trick, so they read closely, think, guess, then check. That
loop repeated page after page IS reading comprehension practice, and to
the kid it is a game.
"""
from __future__ import annotations

from .. import brand
from ..doodle import (INK, MARKER, Picture, Shape, Text, arrow, circle, ellipse, line, poly,
                      rrect, stamp, star)
from ..figures import (GREEN, GREY, RED, bubble, bumpy, hollow_hair, kid, label, magnifier,
                       page, polar_bear, word_box)

ID = "reading"
CLAIM = "“A polar bear's fur is white.”"
YELLOW = brand.YELLOW


def s_bored():
    return [
        bubble(540, 390, 330, 105, (500, 545)),
        label("reading is BORING", (540, 392), size=82),
        *kid(540, 930, 1.35, "bored", "hold"),
        Shape(poly([(445, 800), (540, 818), (635, 800), (635, 868), (540, 886), (445, 868)],
                   closed=True), fill=(255, 255, 255), fill_offset=(0, 0), width=8),
        Shape(line((540, 818), (540, 886)), width=6),
        label("z z z", (790, 600), size=74, color=GREY),
    ]


def s_problem():
    return [
        label("it's not the reading...", (540, 380), size=80),
        Shape([poly([(150, 560), (540, 610), (540, 1000), (150, 950)], closed=True),
               poly([(540, 610), (930, 560), (930, 950), (540, 1000)], closed=True)],
              fill=(255, 255, 255), fill_offset=(0, 0)),
        Text("blah blah blah\nblah blah\nblah blah blah", (345, 785), size=50, color=GREY),
        Text("blah blah\nblah blah blah\nblah blah", (735, 785), size=50, color=GREY),
        label("there's nothing to\nfigure out", (540, 1135), size=80).at("nothing"),
    ]


def s_mystery():
    return [
        Text("a MYSTERY?", (540, 380), size=96, face=MARKER).at("mystery", "pop"),
        *kid(400, 1000, 1.3, "happy", "point"),
        *magnifier(640, 720, 92),
        Shape([poly([(660, 650), (690, 700)], wobble=0.4), poly([(640, 670), (660, 720)], wobble=0.4)],
              color=GREY, width=6),
        Shape([star(800, 560, 28, seed=1), star(860, 820, 20, seed=2)], color=INK, fill=YELLOW, width=6),
        label("every.\nsingle.\nword.", (840, 1050), size=80).at("every"),
    ]


def s_game():
    items = [Text("TRICK TRIVIA", (540, 360), size=96, face=MARKER, color=brand.ORANGE_DEEP,
                  stroke=3, stroke_color=INK).at("trick")]
    for k, y in enumerate((560, 760, 960)):
        items.append(Shape([rrect(130, y - 80, 950, y + 80, r=26),
                            line((175, y - 25), (560, y - 30), wobble=1.0),
                            line((175, y + 25), (500, y + 22), wobble=1.0),
                            rrect(620, y - 38, 760, y + 38, r=14),
                            rrect(790, y - 38, 930, y + 38, r=14)], width=7))
        items.append(Text("REAL", (690, y), size=46, face=MARKER, color=GREEN))
        items.append(Text("FAKE", (860, y), size=46, face=MARKER, color=RED))
    items += [
        label("3 claims a page", (540, 1135), size=80).at("three"),
        Shape(ellipse(690, 560, 86, 52), color=GREEN, width=9).at("real", "ding"),
        Shape(ellipse(860, 760, 86, 52), color=RED, width=9).at("fake", "pop"),
    ]
    return items


def s_claim():
    return [
        label(CLAIM, (540, 390), size=78, max_width=980),
        *polar_bear(470, 760, 1.05),
        bubble(835, 1070, 165, 78, (720, 1160)),
        label("sounds real...", (835, 1072), size=60).at("sounds"),
    ]


def s_think():
    words = word_box(CLAIM, 78)
    wx, ww = words["white"]
    return [
        label(CLAIM, (540, 390), size=78, max_width=980),
        Shape(ellipse(wx, 398, ww / 2 + 26, 54, sweep=400), color=RED, width=10).at("catch"),
        *kid(380, 1030, 1.25, "think", "chin"),
        Shape(arrow((wx + 40, 470), (770, 640), bend=-40), color=RED, width=8),
        label("is it REALLY\nwhite?", (790, 720), size=70, color=RED).at("slow"),
        label("hmm...", (640, 960), size=72).at("think"),
    ]


def s_answer():
    return [
        *kid(540, 1040, 1.25, "shock", "up"),
        Picture(stamp("FAKE!", RED, size=140, angle=-7), (540, 380)).at("fake", "buzz"),
        bubble(820, 650, 190, 80, (650, 760)),
        Text("NO WAY!", (820, 652), size=72, face=MARKER),
        hollow_hair((140, 760), (290, 640), 26).at("see-through"),
        label("see-through!", (225, 860), size=60, color=brand.BLUE),
    ]


def s_loop():
    return [
        Text("READ", (540, 470), size=84, face=MARKER).at("read"),
        Shape(arrow((650, 490), (840, 640), bend=-40), width=8),
        Text("THINK", (860, 725), size=84, face=MARKER).at("think"),
        Shape(arrow((860, 790), (660, 955), bend=-40), width=8),
        Text("GUESS", (540, 980), size=84, face=MARKER).at("guess"),
        Shape(arrow((420, 960), (220, 800), bend=-40), width=8),
        Text("CHECK", (220, 725), size=84, face=MARKER).at("check"),
        Shape(arrow((220, 650), (430, 490), bend=-40), width=8),
        Shape(bumpy(540, 725, 150, 66, bumps=9, depth=0.06), color=YELLOW, fill=YELLOW,
              fill_offset=(0, 0), width=4).at("comprehension"),
        label("reading\ncomprehension", (540, 725), size=50),
        label("(they think it's a game)", (540, 1160), size=70).at("playing"),
    ]


def s_cta():
    return [
        Picture(page("q01.png"), (540, 680), width=400, angle=-4).at("search", "pop"),
        Shape([rrect(120, 1050, 960, 1160, r=55), circle(190, 1102, 24, wobble=0.6),
               line((207, 1119), (228, 1140))], width=8),
        Text("Trick Trivia", (260, 1104), size=72, anchor="lm").at("trick"),
        label("on Amazon", (540, 1240), size=74).at("amazon", "ding"),
    ]


SCRIPT = [
    ("If your kid says reading is boring...", s_bored),
    ("it's usually not the reading. It's that there's nothing to figure out.", s_problem),
    ("Give a kid a mystery, and they'll read every single word.", s_mystery),
    ("That's the idea behind Trick Trivia. Every page has three wild claims, and your kid "
     "decides: real, or fake?", s_game),
    (f"Like this one. {CLAIM} Sounds real, right?", s_claim),
    ("But to catch the trick, they have to slow down, read every word, and think it through.",
     s_think),
    ("Then they check the answer. Fake! The hairs are actually see-through.", s_answer),
    ("Read, think, guess, check. Page after page. That's reading comprehension, and they "
     "think they're just playing.", s_loop),
    ("Search Trick Trivia on Amazon, and grab your copy today.", s_cta),
]

CAPTION = (
    "If your kid says reading is boring, it's usually not the reading. It's that there's "
    "nothing to figure out. Trick Trivia turns every page into a real-or-fake puzzle, so "
    "kids read every word closely, think it through, guess, and check. That's reading "
    "comprehension practice they think is a game. Search Trick Trivia on Amazon."
)
HASHTAGS = ["#readingcomprehension", "#reluctantreader", "#kidsbooks", "#momtok",
            "#homeschool", "#readingtips", "#parentingtips", "#realorfake"]
