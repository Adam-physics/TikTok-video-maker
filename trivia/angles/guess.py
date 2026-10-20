"""Angle: make them guess before you tell them.

Value first: the pretesting effect, explained plainly. Kids who guess
before they are told remember the answer better, even when the guess is
wrong, because the guess makes them want the answer. The tip works with any
fact; the book is credited as where the family's facts come from, and the
video closes back on the habit, not the product.
"""
from __future__ import annotations

import math

import numpy as np

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, circle, ellipse, line, poly, rrect, star
from ..explainer import KEEP
from ..figures import bubble, bumpy, cover, kid
from .reading import BLUE, GOLD, GREEN, GREY, RED, TEAL, W, lightbulb, note, tag
from .school import PINK, speech, table

ID = "guess"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"


def snail(cx, cy, s=1.0):
    """A sleeping snail: spiral shell on a soft body."""
    t = np.linspace(0, 3.0 * 2 * math.pi, 160)
    r = 6 + 112 * t / t[-1]
    spiral = np.stack([cx + 20 * s + r * s * np.cos(t), cy - 70 * s + r * s * np.sin(t)], axis=1)
    body = [(cx - 190 * s, cy + 40 * s), (cx - 150 * s, cy - 10 * s), (cx - 60 * s, cy + 10 * s),
            (cx + 180 * s, cy + 20 * s), (cx + 210 * s, cy + 60 * s), (cx - 200 * s, cy + 62 * s)]
    shell_fill = (240, 214, 170)
    return [
        Shape(poly(body, closed=True, wobble=1.2), width=W, fill=(214, 226, 200), fill_offset=(0, 0)),
        Shape(circle(cx + 20 * s, cy - 70 * s, 140 * s), width=W, fill=shell_fill, fill_offset=(0, 0)),
        Shape(poly(spiral[::-1], wobble=0.6), color=(150, 110, 70), width=6),
        Shape([line((cx - 160 * s, cy), (cx - 185 * s, cy - 70 * s)),
               line((cx - 140 * s, cy - 4 * s), (cx - 140 * s, cy - 76 * s))], width=6),
        Shape([ellipse(cx - 188 * s, cy - 76 * s, 9 * s, 6 * s, wobble=0.2),
               ellipse(cx - 140 * s, cy - 82 * s, 9 * s, 6 * s, wobble=0.2)], width=6),
    ]


def calendar(cx, cy):
    return [
        Shape([rrect(cx - 110, cy - 100, cx + 110, cy + 110, r=16),
               line((cx - 110, cy - 50), (cx + 110, cy - 50))], width=W, fill=(255, 255, 255),
              fill_offset=(0, 0)),
        Shape([line((cx - 55, cy - 120), (cx - 55, cy - 80)), line((cx + 55, cy - 120), (cx + 55, cy - 80))],
              width=8),
        Text("3", (cx, cy + 10), size=96, face=MARKER, color=RED),
        Text("YEARS", (cx, cy + 82), size=38, face=MARKER, color=RED),
    ]


# ------------------------------------------------------------------ boards

def l_hook():
    """Frame one is a finished board: the parent explaining, the kid blank.
    The facts fly out on "gone"; the sticky note slaps on for the promise."""
    explain = speech(340, 540, 270, 92, (270, 800), "...and that's why the moon...", size=40)
    flying = [
        Shape(star(860, 840, 26, seed=3), color=GOLD, fill=GOLD, width=5),
        Text("2+2", (950, 930), size=46, face=MARKER, color=BLUE),
        Text("?", (880, 1010), size=70, face=MARKER, color=GREY),
        Shape([line((770, 900), (820, 880)), line((775, 930), (835, 935)), line((770, 960), (820, 985))],
              color=GREY, width=6),
    ]
    flying[0].at("gone")
    note_card = Shape(rrect(160, 1060, 900, 1200, r=14), color=(200, 160, 30), width=6,
                      fill=(255, 226, 120), fill_offset=(0, 0))
    note_card.at("stick").focus(1.06)
    return [
        Text("IN ONE EAR...", (540, 330), size=84, face=MARKER, color=RED).ready(),
        *[it.ready() for it in explain],
        *[it.ready() for it in kid(260, 1070, 0.95, "happy", "point")],
        *[it.ready() for it in kid(700, 1080, 0.75, "bored", "down")],
        tag("...OUT THE OTHER.", (760, 690), size=50, color=RED).at("later"),
        *flying,
        note_card,
        Text("MAKE IT STICK", (530, 1132), size=78, face=MARKER, color=INK).pop(),
    ]


def l_trick():
    tell = speech(430, 520, 270, 96, (330, 800), "The answer is...", size=56)
    tell[0].at("tell")
    return [
        *kid(300, 1050, 0.95, "happy", "down"),
        *tell,
        Shape([line((190, 430), (670, 615)), line((670, 430), (190, 615))], color=RED,
              width=16, speed=2.5).at("answer"),
        Text("GUESS", (820, 790), size=110, face=MARKER, color=GREEN).at("guess").focus(1.1).pop(),
        Text("FIRST", (820, 910), size=110, face=MARKER, color=GREEN).pop(),
    ]


def l_research():
    return [
        Shape(bumpy(540, 720, 220, 150, bumps=11, depth=0.07), width=W, fill=PINK, fill_offset=(0, 0)),
        Shape([line((540, 600), (530, 840)), line((420, 680), (480, 720)), line((620, 700), (680, 660))],
              width=6, color=(200, 120, 140)),
        tag("guess", (300, 470), size=56, color=GOLD).at("backwards"),
        Shape(arrow((360, 500), (430, 600), bend=20, head=22), color=GOLD, width=W),
    ]


def l_remember():
    return [
        tag("REMEMBERS BETTER", (540, 960), size=60).at("remember").focus(1.14).pop(),
        note("(even wrong guesses!)", (540, 1050), size=50, color=RED).at("wrong").pop(),
    ]


def l_why():
    return [
        *lightbulb(800, 430, r=52),
        Text("?", (545, 735), size=150, face=MARKER, color=GOLD).at("waiting").focus(1.2).pop(),
    ]


def l_ask():
    ask = speech(560, 400, 340, 86, (260, 860), "How long can a snail sleep?", size=46)
    ask[0].at("ask")
    return [*kid(240, 1070, 0.9, "happy", "point"), *ask]


def l_choices():
    return [
        *kid(880, 1110, 0.68, "think", "chin"),
        note("A)  a day", (560, 590), size=60, anchor="lm").at("day"),
        note("B)  a week", (560, 710), size=60, anchor="lm").at("week"),
        note("C)  3 years", (560, 830), size=60, anchor="lm").at("three").pop(),
    ]


def l_reveal():
    return [
        *snail(360, 760, 1.0),
        note("z z z", (230, 520), size=60, color=GREY),
        *calendar(820, 560),
        Shape(ellipse(820, 572, 150, 150, sweep=400), color=GREEN, width=9).at("three").focus(1.2),
        *kid(800, 1150, 0.62, "shock", "up"),
    ]


def l_sticks():
    return [
        bubble(470, 1020, 220, 74, (760, 1030)).at("wait").focus(1.16),
        Text("WAIT, WHAT?!", (470, 1022), size=50, face=MARKER, color=RED).pop(),
        tag("that's when it sticks", (470, 1150), size=46, color=TEAL).at("sticks"),
    ]


def l_book():
    """The family at the table; the book is a small prop with a credit."""
    return [
        *kid(300, 970, 1.0, "happy", "hold"),
        *kid(800, 1000, 0.8, "think", "chin"),
        *table(),
        Picture(cover(), (300, 915), width=118, angle=-4).at("book"),
        note("Trick Trivia", (560, 700), size=44, color=GREY).at("trick"),
        Shape(arrow((480, 790), (378, 880), bend=-20, head=20), color=GREY, width=6),
        bubble(800, 560, 200, 82, (800, 740)).at("real"),
        Text("real or fake?", (800, 565), size=38, face=MARKER, color=GOLD),
        note("(on Amazon)", (560, 752), size=36, color=GREY).at("amazon"),
    ]


def l_close():
    return [
        tag("GUESS FIRST.", (540, 330), size=80, color=GREEN).at("guess").focus(1.12).pop(),
        note("(the easiest learning trick there is)", (540, 410), size=40, color=GREY).at("easiest"),
    ]


SCRIPT = [
    ("You explain something to your kid… and five minutes later, it's gone. Here's how to "
     "make it stick.", l_hook),
    ("The trick: before you tell them the answer, make them guess first.", l_trick),
    ("It sounds backwards, but learning research keeps finding the same thing.", l_research),
    ("When kids guess before you tell them, they remember the real answer better. Even when "
     "their guess is wrong.", l_remember, KEEP),
    ("Why? A guess makes them care. Their brain is waiting for the answer.", l_why, KEEP),
    ("So next time you know a cool fact, don't just say it. Ask.", l_ask),
    ("“How long can a snail sleep? A day? A week? Three years?”", l_choices, KEEP),
    ("Let them pick. Then tell them. Three years. Watch their face.", l_reveal),
    ("That “wait, WHAT?” is the moment it sticks.", l_sticks, KEEP),
    ("We get a lot of ours from a book called Trick Trivia. Every claim is real or fake, so "
     "they have to guess first. It's on Amazon.", l_book),
    ("Book or no book, make them guess first. It's the easiest learning trick there is.",
     l_close, KEEP),
]

CAPTION = (
    "You explain something to your kid, and five minutes later it's gone. The fix: before you "
    "tell them the answer, make them guess first. Learning research keeps finding "
    "that a guess before the answer, even a wrong one, helps kids remember it better, because "
    "now they care what the answer is. Try it with any fact: \"How long can a snail sleep? A "
    "day, a week, or three years?\" (It's three years.) We get a lot of ours from Trick "
    "Trivia, a real-or-fake book (it's on Amazon). Book or no book, make them guess first."
)
HASHTAGS = ["#parentingtips", "#momtok", "#dadtok", "#learningtips", "#homeschool",
            "#kidsactivities", "#realorfake"]
