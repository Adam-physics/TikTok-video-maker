"""Angle: "how was school?" gets "fine." Try two truths and a lie instead.

Value first: a dinner-table trick any parent can use tonight, with the
reason it works. The book enters as the next step of that same game
(after a few nights, flip it: you read them something wild) rather than
as a pitch, and the ask stays soft: "It's on Amazon."
"""
from __future__ import annotations

from ..doodle import (INK, MARKER, Picture, Shape, Text, arrow, check, circle, curve, ellipse, line,
                      poly, rrect)
from ..explainer import KEEP
from ..figures import bubble, bumpy, cover, kid
from .reading import (BLUE, GOLD, GREEN, GREY, RED, TEAL, W, mini_card, note, small_book,
                      tag)

ID = "school"
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“Dolphins sleep with one eye open.”"
PINK = (252, 214, 222)


def speech(cx, cy, rx, ry, tail, text, size=46, color=INK):
    return [bubble(cx, cy, rx, ry, tail), note(text, (cx, cy + 4), size=size, color=color,
                                                max_width=rx * 1.7)]


def clock(cx, cy, r):
    ticks = [line((cx, cy - r + 14), (cx, cy - r + 34)), line((cx + r - 14, cy), (cx + r - 34, cy)),
             line((cx, cy + r - 14), (cx, cy + r - 34)), line((cx - r + 14, cy), (cx - r + 34, cy))]
    return [Shape(circle(cx, cy, r), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
            Shape(ticks, width=6),
            Shape([line((cx, cy), (cx, cy - r * 0.62)), line((cx, cy), (cx + r * 0.42, cy + r * 0.2))],
                  color=RED, width=10)]


def tray(cx, cy):
    return Shape([rrect(cx - 90, cy - 55, cx + 90, cy + 55, r=16), circle(cx - 42, cy, 26, wobble=0.6),
                  rrect(cx + 8, cy - 32, cx + 70, cy + 32, r=8)], width=6)


# ------------------------------------------------------------------ boards

def l_ask():
    reply = speech(800, 760, 120, 66, (790, 880), "fine.", size=52)
    reply[0].at("one")
    return [
        *kid(280, 1060, 1.0, "happy", "down"),
        *speech(360, 560, 240, 88, (300, 760), "How was school?", size=52),
        *kid(780, 1100, 0.75, "bored", "down"),
        *reply,
        tag("1 WORD.", (800, 600), size=56, color=RED).at("word"),
    ]


def l_three():
    return [
        *kid(250, 1080, 0.8, "happy", "point"),
        *speech(660, 420, 330, 80, (380, 860), "I sat with Maya at lunch", size=44),
        *speech(660, 640, 330, 80, (380, 870), "We had a fire drill", size=44),
        *speech(660, 860, 330, 80, (380, 880), "Mr. Lee fell asleep in class", size=40),
    ]


def l_guess():
    return [
        tag("which one is fake?", (660, 1090), size=54).at("guess"),
        Shape(ellipse(660, 860, 360, 108, sweep=400), color=RED, width=9).at("fake"),
        tag("?", (980, 700), size=110, color=GOLD),
    ]


def l_details():
    return [
        Shape(bumpy(540, 720, 220, 150, bumps=11, depth=0.07), width=W, fill=PINK, fill_offset=(0, 0)),
        Shape([line((540, 600), (530, 840)), line((420, 680), (480, 720)), line((620, 700), (680, 660))],
              width=6, color=(200, 120, 140)),
        tag("REAL DETAILS", (540, 960), size=60).at("details"),
        *speech(880, 440, 140, 62, (800, 560), "who said what", size=34),
        Shape(arrow((820, 520), (700, 610), bend=-20, head=22), color=BLUE, width=W).at("who"),
        tray(190, 450).at("lunch"),
        Shape(arrow((260, 520), (380, 610), bend=20, head=22), color=BLUE, width=W),
    ]


def l_game():
    return [
        tag("GAME", (330, 1120), size=70, color=GREEN).at("game"),
        Shape(check(480, 1112, 24), color=GREEN, width=10),
        tag("REPORT", (760, 1120), size=70, color=GREY).at("report"),
        Shape(line((640, 1122), (880, 1112)), color=RED, width=10),
    ]


def l_result():
    return [
        *clock(280, 640, 140),
        tag("2 MIN", (280, 850), size=64, color=RED).at("two"),
        Shape(rrect(500, 360, 980, 900, r=60), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        Shape([line((550, 430 + k * 64), (930 - (k % 3) * 60, 428 + k * 64), wobble=0.8)
               for k in range(7)], color=GREY, width=6).at("more"),
        *kid(760, 1150, 0.62, "happy", "point"),
        tag("vs. “fine.”", (280, 960), size=48, color=GREY).at("week"),
    ]


def l_flip():
    return [
        Text("FLIP IT", (540, 420), size=150, face=MARKER, color=INK).at("flip"),
        Shape(arrow((180, 560), (900, 560), bend=-90, head=28), color=TEAL, width=W),
        *kid(300, 1110, 1.0, "happy", "hold"),
        *small_book(300, 1045, w=150, h=90),
        *kid(780, 1140, 0.75, "think", "chin"),
        tag("real or fake?", (800, 880), size=50, color=BLUE).at("guess"),
    ]


def dolphin(cx, cy, s=1.0):
    """Side-on cartoon dolphin, asleep with its eye wide open."""
    body = [(-235, 12), (-200, -4), (-150, -52), (-40, -84), (10, -82), (150, -50), (232, -14),
            (300, -62), (284, 0), (300, 58), (226, 16), (100, 46), (-40, 56), (-150, 36),
            (-212, 22), (-235, 12)]
    fin = [(-10, -80), (40, -152), (70, -74)]
    flipper = [(-60, 46), (-20, 104), (10, 48)]
    P = lambda pts: [(cx + x * s, cy + y * s) for x, y in pts]
    fill = (206, 228, 246)
    return [
        Shape(poly(P(fin), closed=True, wobble=1.0), width=W, fill=fill, fill_offset=(0, 0)),
        Shape(curve(P(body), wobble=1.2, samples=10), width=W, fill=fill, fill_offset=(0, 0)),
        Shape(poly(P(flipper), closed=True, wobble=0.8), width=W, fill=fill, fill_offset=(0, 0)),
        Shape(curve(P([(-232, 14), (-190, 18), (-150, 10)]), wobble=0.5), width=6),     # mouth
        Shape(circle(cx - 140 * s, cy - 16 * s, 16 * s, wobble=0.3), width=6,
              fill=(255, 255, 255), fill_offset=(0, 0)),                               # eye, open
        Shape(circle(cx - 136 * s, cy - 14 * s, 7 * s, wobble=0.2), fill=INK, width=4),
        Shape(line((cx - 300 * s, cy + 150 * s), (cx + 330 * s, cy + 140 * s), wobble=2.5),
              color=BLUE, width=W),
    ]


def l_example():
    return [
        Shape(rrect(90, 290, 990, 470, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        note(CLAIM, (540, 380), size=52, max_width=860),
        *dolphin(500, 760, 1.15),
        note("z z z", (300, 560), size=58, color=GREY),
        tag("sounds fake...", (540, 1010), size=56, color=BLUE).at("sounds"),
        tag("REAL!", (540, 1140), size=100, color=GREEN).at("real"),
    ]


def l_book():
    return [
        Picture(cover(), (540, 590), width=310, angle=-3, tape=True).at("trick"),
        mini_card(215, 1000, w=250, h=130), mini_card(540, 1000, w=250, h=130),
        mini_card(865, 1000, w=250, h=130),
        Shape(check(215, 1010, 30), color=GREEN, width=11).at("three"),
        Shape([line((515, 980), (565, 1030)), line((565, 980), (515, 1030))], color=RED, width=11),
        tag("?", (865, 1010), size=64, color=GOLD),
        tag("on Amazon", (540, 1160), size=60).at("amazon"),
    ]


SCRIPT = [
    ("Ask your kid how school was, and you get one word. “Fine.”", l_ask),
    ("Try this instead. Tonight, ask them to tell you three things about their day. Two true, "
     "one made up.", l_three),
    ("Your job is to guess the fake one.", l_guess, KEEP),
    ("Here's why it works. To fool you, they have to remember real details: who said what, "
     "what happened at lunch.", l_details),
    ("And now it's a game they want to win, not a report.", l_game, KEEP),
    ("You'll hear more about their day in two minutes than you have all week.", l_result),
    ("After a few nights, flip it. You read them something wild, and they guess if it's real.",
     l_flip),
    (f"Like, {CLAIM} Sounds fake. It's real.", l_example),
    ("We pull ours from a book called Trick Trivia. Every page has three of these. "
     "It's on Amazon.", l_book),
]

CAPTION = (
    "Ask your kid \"how was school?\" and you get \"fine.\" Try this at dinner tonight: two "
    "truths and a lie about their day, and you guess the fake one. To fool you, they have to "
    "remember real details, so you hear way more than \"fine.\" After a few nights, flip it: "
    "read them something wild and let them guess. We pull ours from Trick Trivia, a book of "
    "real-or-fake claims. It's on Amazon."
)
HASHTAGS = ["#parentingtips", "#momtok", "#dadtok", "#dinnertable", "#familygames",
            "#kidsconversation", "#realorfake"]
