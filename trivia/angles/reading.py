"""Angle: reading comprehension for the kid who says reading is boring.

The promise: your kid reads every word, carefully, without being told to.
The mechanism, shown rather than claimed: a claim is a puzzle, one word
can be the trick, so they read closely, think, guess, then check. That
loop repeated page after page IS reading comprehension practice, and to
the kid it is a game.

Boards build across lines (KEEP) and are erased between ideas, the way the
reference explainer doodles are paced.
"""
from __future__ import annotations

from ..doodle import (HAND, INK, MARKER, Picture, Shape, Text, arrow, check, circle, ellipse,
                      line, poly, rrect)
from ..explainer import KEEP
from ..figures import bumpy, cover, hollow_hair, kid, polar_bear, word_box

ID = "reading"
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“A polar bear's fur is white.”"

TEAL = (27, 128, 122)
BLUE = (48, 92, 172)
RED = (208, 62, 50)
GREEN = (46, 146, 78)
GOLD = (226, 168, 40)
PALE_GOLD = (252, 234, 178)
GREY = (150, 152, 160)
W = 7                   # line weight: thin, like a fine marker


def tag(text, xy, size=54, color=TEAL, **kw):
    return Text(text, xy, size=size, color=color, face=MARKER, **kw)


def note(text, xy, size=60, color=INK, **kw):
    return Text(text, xy, size=size, color=color, face=HAND, **kw)


def small_book(cx, cy, w=300, h=190):
    x0, x1 = cx - w / 2, cx + w / 2
    pages = Shape([poly([(x0, cy - h / 2 + 14), (cx, cy - h / 2 + 34), (cx, cy + h / 2 + 10),
                         (x0, cy + h / 2 - 10)], closed=True),
                   poly([(cx, cy - h / 2 + 34), (x1, cy - h / 2 + 14), (x1, cy + h / 2 - 10),
                         (cx, cy + h / 2 + 10)], closed=True)],
                  width=W, fill=(255, 255, 255), fill_offset=(0, 0))
    lines = Shape([line((x0 + 22, cy - 40 + k * 34), (cx - 22, cy - 26 + k * 34), wobble=0.8)
                   for k in range(4)]
                  + [line((cx + 22, cy - 26 + k * 34), (x1 - 22, cy - 40 + k * 34), wobble=0.8)
                     for k in range(4)], color=GREY, width=5)
    return [pages, lines]


def lightbulb(cx, cy, r=62):
    return [
        Shape([circle(cx, cy, r), rrect(cx - 28, cy + r - 4, cx + 28, cy + r + 34, r=8)],
              color=GOLD, fill=PALE_GOLD, fill_offset=(0, 0), width=W),
        Shape([line((cx - 22, cy + r + 50), (cx + 22, cy + r + 50))], color=GOLD, width=W),
        Shape([line((cx, cy - r - 24), (cx, cy - r - 54)),
               line((cx - r - 22, cy - 50), (cx - r - 46, cy - 72)),
               line((cx + r + 22, cy - 50), (cx + r + 46, cy - 72)),
               line((cx - r - 30, cy + 8), (cx - r - 62, cy + 8)),
               line((cx + r + 30, cy + 8), (cx + r + 62, cy + 8))], color=GOLD, width=W),
    ]


def mini_card(cx, cy, w=270, h=150):
    x0, y0 = cx - w / 2, cy - h / 2
    return Shape([rrect(x0, y0, x0 + w, y0 + h, r=18),
                  line((x0 + 26, y0 + 44), (x0 + w - 40, y0 + 40), wobble=0.8),
                  line((x0 + 26, y0 + 78), (x0 + w - 80, y0 + 76), wobble=0.8)], width=W)


# ------------------------------------------------------------------ boards

def l_bored():
    return [
        *kid(320, 940, 0.85, "bored", "hold"),
        Shape(poly([(262, 845), (320, 856), (378, 845), (378, 893), (320, 904), (262, 893)],
                   closed=True), fill=(255, 255, 255), fill_offset=(0, 0), width=W),
        tag("“READING IS BORING”", (600, 380), size=58, color=BLUE).at("reading"),
        Shape(arrow((470, 430), (365, 600), bend=30, head=26), color=BLUE, width=W),
        note("z z z", (440, 640), size=52, color=GREY),
    ]


def l_problem():
    return [
        *small_book(770, 760),
        tag("nothing to\nfigure out", (770, 990), size=56, color=RED).at("nothing"),
    ]


def l_mystery():
    return [
        *lightbulb(540, 400),
        Text("MYSTERY", (540, 720), size=170, face=MARKER, color=INK).at("mystery"),
        Shape(line((150, 830), (930, 822), wobble=1.0), color=TEAL, width=10),
        Shape([line((260, 834), (260, 880)), line((540, 828), (540, 880)),
               line((820, 824), (820, 880))], color=TEAL, width=6).at("every"),
        tag("EVERY", (260, 925)),
        tag("SINGLE", (540, 925)),
        tag("WORD", (820, 925)),
    ]


def l_book():
    return [
        Picture(cover(), (540, 560), width=300, angle=-3, tape=True).at("trick"),
        mini_card(215, 925), mini_card(540, 925), mini_card(865, 925),
        tag("3 wild claims a page", (540, 1130), size=52).at("three"),
        Shape(check(215, 940, 34), color=GREEN, width=12).at("real"),
        tag("REAL", (215, 1050), size=40, color=GREEN),
        Shape([line((510, 905), (570, 965)), line((570, 905), (510, 965))],
              color=RED, width=12).at("fake"),
        tag("FAKE", (540, 1050), size=40, color=RED),
        tag("?", (865, 940), size=70, color=GOLD).at("decides"),
    ]


def l_claim():
    return [
        Shape(rrect(90, 290, 990, 470, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        note(CLAIM, (540, 380), size=64),
        *polar_bear(300, 720, 0.62),
        tag("sounds real...", (760, 650), size=54, color=BLUE).at("sounds"),
        Shape(arrow((660, 690), (450, 760), bend=-30, head=24), color=BLUE, width=W),
    ]


def l_think():
    words = word_box(CLAIM, 64)
    wx, ww = words["white"]
    return [
        Shape(ellipse(wx, 386, ww / 2 + 24, 46, sweep=400), color=RED, width=8).at("catch"),
        tag("is it REALLY white?", (700, 540), size=48, color=RED).at("slow"),
        *kid(800, 1060, 0.75, "think", "chin"),
        note("hmm...", (930, 860), size=54).at("think"),
    ]


def l_answer():
    return [
        tag("FAKE!", (250, 545), size=84, color=RED).at("fake"),
        hollow_hair((470, 1060), (600, 960), 24, color=TEAL).at("hairs"),
        tag("see-through!", (500, 1150), size=50).at("see-through"),
    ]


def l_loop():
    return [
        tag("READ", (540, 420), size=80, color=INK).at("read"),
        Shape(arrow((650, 440), (850, 610), bend=-40, head=26), width=W),
        tag("THINK", (880, 700), size=80, color=INK).at("think"),
        Shape(arrow((880, 770), (660, 960), bend=-40, head=26), width=W),
        tag("GUESS", (540, 1000), size=80, color=INK).at("guess"),
        Shape(arrow((420, 980), (200, 790), bend=-40, head=26), width=W),
        tag("CHECK", (200, 700), size=80, color=INK).at("check"),
        Shape(arrow((200, 620), (420, 440), bend=-40, head=26), width=W),
        Shape(bumpy(540, 705, 140, 66, bumps=9, depth=0.06), color=GOLD, fill=PALE_GOLD,
              fill_offset=(0, 0), width=5).at("comprehension"),
        tag("READING\nCOMPREHENSION", (540, 707), size=33),
        note("(they think it's a game)", (540, 1160), size=62).at("playing"),
    ]


def l_cta():
    return [
        Shape([rrect(140, 330, 480, 1020, r=44), rrect(175, 400, 445, 940, r=12),
               line((280, 980), (340, 980))], width=W),
        Shape([rrect(195, 450, 425, 510, r=28), circle(225, 480, 13, wobble=0.4),
               line((234, 489), (246, 501))], width=5).at("search", "tap"),
        Text("Trick Trivia", (250, 481), size=36, face=HAND, anchor="lm"),
        *small_book(310, 660, w=200, h=130),
        Shape(rrect(200, 820, 420, 890, r=34), color=GOLD, fill=PALE_GOLD, fill_offset=(0, 0),
              width=W).at("grab", "tap"),
        Text("Add to Cart", (310, 856), size=38, face=HAND),
        Picture(cover(), (770, 600), width=290, angle=4, tape=True).at("trick"),
        tag("on Amazon", (770, 1000), size=60).at("amazon"),
        Shape(arrow((770, 950), (770, 860), bend=0, head=24), color=TEAL, width=W),
    ]


SCRIPT = [
    ("If your kid says reading is boring...", l_bored),
    ("it's usually not the reading. It's that there's nothing to figure out.", l_problem, KEEP),
    ("Give a kid a mystery, and they'll read every single word.", l_mystery),
    ("That's the idea behind Trick Trivia. Every page has three wild claims, and your kid "
     "decides: real, or fake?", l_book),
    (f"Like this one. {CLAIM} Sounds real, right?", l_claim),
    ("But to catch the trick, they have to slow down, read every word, and think it through.",
     l_think, KEEP),
    ("Then they check the answer. Fake! The hairs are actually see-through.", l_answer, KEEP),
    ("Read, think, guess, check. Page after page. That's reading comprehension, and they "
     "think they're just playing.", l_loop),
    ("Search Trick Trivia on Amazon, and grab your copy today.", l_cta),
]

CAPTION = (
    "If your kid says reading is boring, it's usually not the reading. It's that there's "
    "nothing to figure out. Trick Trivia turns every page into a real-or-fake puzzle, so "
    "kids read every word closely, think it through, guess, and check. That's reading "
    "comprehension practice they think is a game. Search Trick Trivia on Amazon."
)
HASHTAGS = ["#readingcomprehension", "#reluctantreader", "#kidsbooks", "#momtok",
            "#homeschool", "#readingtips", "#parentingtips", "#realorfake"]
