"""Angle: lights off, and suddenly your kid wants to talk. Don't shut it down.

Value first, and honest: bedtime is often the first quiet, unhurried moment
of a kid's day, and the dark, side-by-side, no-eye-contact setup makes it
easier to bring up the big stuff. The fix is to plan for it: five minutes of
talk before lights out, opened with something easy. The book is named once
as one easy opener, next to free ones, and the close is back on the habit.
"""
from __future__ import annotations

import math

import numpy as np

from ..doodle import (INK, MARKER, Picture, Shape, Text, arc, arrow, check, circle, ellipse, heart, line, poly,
                      rrect, star)
from ..figures import bubble, cover, face, kid
from .reading import BLUE, GOLD, GREEN, GREY, PALE_GOLD, RED, TEAL, W, note, tag
from .school import PINK, clock, speech
from .screens import crossed

ID = "bedtime"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“Koalas sleep up to 22 hours a day.”"
SKY = (200, 222, 250)
NIGHT = (52, 64, 110)
KOALA = (176, 180, 190)


def moon(cx, cy, r):
    """A filled crescent, opening to the right."""
    t = np.radians(np.linspace(60, 300, 60))
    outer = np.stack([cx + r * np.cos(t), cy + r * np.sin(t)], axis=1)
    t2 = np.radians(np.linspace(300, 60, 60))
    ox = cx + r * 0.55
    rin = math.hypot(cx + r * math.cos(math.radians(60)) - ox, r * math.sin(math.radians(60)))
    inner = np.stack([ox + rin * np.cos(t2), cy + rin * np.sin(t2)], axis=1)
    inner = inner[inner[:, 0] <= cx + r * 0.6]
    return Shape(poly(np.concatenate([outer, inner]).tolist(), closed=True, wobble=0.8),
                 color=GOLD, fill=PALE_GOLD, width=7, fill_offset=(0, 0))


def window(cx, cy, w=240, h=260):
    x0, y0 = cx - w / 2, cy - h / 2
    return [Shape(rrect(x0, y0, x0 + w, y0 + h, r=10), width=W, fill=NIGHT, fill_offset=(0, 0)),
            moon(cx - 30, cy - 30, 52),
            Shape([star(cx + 70, cy - 80, 14, seed=1), star(cx + 60, cy + 70, 11, seed=2)],
                  color=GOLD, fill=GOLD, width=3),
            Shape([line((cx, y0), (cx, y0 + h)), line((x0, cy + 20), (x0 + w, cy + 20))], width=7)]


def sleepy(cx, cy, s):
    """Closed, content eyes for a head of radius 62*s."""
    ex, ey = 24 * s, -6 * s
    return [Shape([arc(cx - ex, cy + ey, 12 * s, 9 * s, 10, 170), arc(cx + ex, cy + ey, 12 * s, 9 * s, 10, 170),
                   arc(cx, cy + 16 * s, 16 * s, 10 * s, 20, 160)], width=max(4, int(6 * s)))]


def bed(cx, cy, w=600, heads=(("happy", 0),)):
    """A bed seen from the side; heads are (mood, x offset along the pillow)."""
    x0, x1 = cx - w / 2, cx + w / 2
    out = [
        Shape([rrect(x0 - 20, cy - 190, x0 + 30, cy + 130, r=12), rrect(x0, cy + 10, x1, cy + 90, r=10),
               line((x1 - 20, cy + 90), (x1 - 20, cy + 130))], width=W, fill=(230, 200, 160),
              fill_offset=(0, 0)),
        Shape(ellipse(x0 + 120, cy - 20, 90, 34), width=7, fill=(255, 255, 255), fill_offset=(0, 0)),
    ]
    s = 0.8
    for mood, dx in heads:
        hx, hy = x0 + 120 + dx, cy - 70
        out.append(Shape(circle(hx, hy, 62 * s), width=8, fill=(255, 255, 255), fill_offset=(0, 0)))
        out.extend(sleepy(hx, hy, s) if mood == "sleepy" else face(hx, hy, s, mood))
    blanket = [(x0 + 60 + 120 * (len(heads) > 1), cy + 10), (x0 + 200, cy - 40), (x1 - 60, cy - 50),
               (x1 + 10, cy + 20), (x1, cy + 40), (x0 + 60, cy + 40)]
    out.append(Shape(poly(blanket, closed=True, wobble=1.4), width=W, fill=SKY, fill_offset=(0, 0)))
    return out


def koala(cx, cy, s=1.0):
    return [
        Shape(line((cx - 240 * s, cy + 150 * s), (cx + 260 * s, cy + 40 * s)), color=(130, 90, 60), width=16),
        Shape(ellipse(cx + 10 * s, cy + 70 * s, 120 * s, 85 * s), width=W, fill=KOALA, fill_offset=(0, 0)),
        Shape([circle(cx - 95 * s, cy - 95 * s, 52 * s), circle(cx + 95 * s, cy - 95 * s, 52 * s)],
              width=W, fill=KOALA, fill_offset=(0, 0)),
        Shape(circle(cx, cy - 40 * s, 92 * s), width=W, fill=KOALA, fill_offset=(0, 0)),
        Shape(ellipse(cx, cy - 20 * s, 26 * s, 34 * s, wobble=0.6), fill=INK, width=5, fill_offset=(0, 0)),
        Shape([arc(cx - 46 * s, cy - 60 * s, 16 * s, 10 * s, 10, 170),
               arc(cx + 46 * s, cy - 60 * s, 16 * s, 10 * s, 10, 170)], width=6),
    ]


def lamp(cx, cy):
    return [Shape([line((cx, cy), (cx, cy - 120)),
                   rrect(cx - 50, cy - 6, cx + 50, cy + 10, r=6)], width=8),
            Shape(poly([(cx - 70, cy - 120), (cx + 70, cy - 120), (cx + 45, cy - 210), (cx - 45, cy - 210)],
                       closed=True, wobble=1.0), width=W, fill=PALE_GOLD, fill_offset=(0, 0))]


# ------------------------------------------------------------------ boards

def l_hook():
    """Frame one: the chatty kid in bed, the tired parent at the door."""
    chatter = speech(380, 520, 280, 110, (300, 700), "and also... and ALSO...", size=48)
    shh = speech(860, 690, 110, 70, (860, 800), "SHH!", size=52)
    return [
        Text("SUDDENLY CHATTY", (540, 320), size=84, face=MARKER, color=RED).ready(),
        *[it.ready() for it in bed(380, 960, 560, (("happy", 0),))],
        *[it.ready() for it in chatter],
        *[it.ready() for it in kid(860, 1060, 0.75, "bored", "down")],
        *[it.ready() for it in shh],
        crossed(860, 690, 80).at("shut"),
        Text("?", (620, 720), size=150, face=MARKER, color=GREEN).at("why").focus(1.08).pop(),
    ]


def l_quiet():
    return [
        tag("stalling?", (540, 330), size=64, color=GREY),
        Shape(line((390, 335), (690, 325)), color=RED, width=10),
        moon(540, 560, 110).at("quiet"),
        tag("first quiet moment all day", (540, 760), size=54, color=TEAL).pop(),
        Shape(check(300, 900, 24), color=GREEN, width=10).at("screens"),
        note("no screens", (360, 900), size=54, anchor="lm"),
        Shape(check(300, 1000, 24), color=GREEN, width=10).at("rushing"),
        note("no rushing", (360, 1000), size=54, anchor="lm"),
        Shape(heart(300, 1100, 26), color=RED, fill=(250, 140, 150), width=6).at("right"),
        note("you, right there", (360, 1100), size=54, anchor="lm"),
    ]


def l_side():
    return [
        *window(820, 470, 220, 240),
        *bed(440, 900, 640, (("sleepy", 0), ("happy", 130))),
        tag("side by side", (300, 330), size=58, color=TEAL).at("side"),
        tag("no eye contact", (300, 420), size=50, color=GREY).at("eye"),
        bubble(560, 1150, 230, 70, (560, 1000)).at("big").focus(1.08),
        Text("the big stuff", (560, 1152), size=50, face=MARKER, color=RED).pop(),
    ]


def l_plan():
    return [
        tag("PLAN FOR IT.", (540, 340), size=96, color=TEAL).at("plan").focus(1.08).pop(),
        *clock(540, 640, 130),
        tag("5 MINUTES", (540, 850), size=80, color=RED).at("five").pop(),
        note("just for talking", (540, 960), size=60).at("talking"),
        note("(before lights out)", (540, 1050), size=46, color=GREY),
    ]


def l_start():
    small = bubble(300, 520, 180, 70, (220, 640))
    big = bubble(620, 900, 330, 130, (480, 1080), seed=2)
    return [
        small.at("silly"),
        note("a silly question", (300, 522), size=42),
        Shape(arrow((420, 620), (520, 760), bend=20, head=22), color=GOLD, width=W).at("going"),
        big.at("real").focus(1.08),
        Text("the real stuff", (620, 900), size=66, face=MARKER, color=RED).pop(),
        Shape(heart(860, 760, 34), color=RED, fill=(250, 140, 150), width=6),
    ]


def l_game():
    return [
        tag("1 real-or-fake a night", (540, 320), size=56, color=TEAL).at("real-or-fake"),
        Shape(rrect(70, 390, 1010, 530, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        note(CLAIM, (540, 462), size=52).at("koalas"),
        *koala(540, 820, 1.0),
        Text("z z z", (800, 640), size=56, face=MARKER, color=GREY),
        tag("REAL!", (540, 1150), size=120, color=GREEN).at("real").focus(1.12).pop(),
    ]


def l_options():
    return [
        Shape(rrect(130, 1000, 450, 1180, r=10), width=W, fill=(230, 200, 160), fill_offset=(0, 0)),
        *lamp(200, 1000),
        Picture(cover(), (385, 925), width=115, angle=6).at("book"),
        note("Trick Trivia", (330, 700), size=44, color=GREY).at("trick"),
        Shape(arrow((350, 740), (380, 835), head=18), color=GREY, width=6),
        bubble(770, 460, 220, 90, (700, 600)).at("would-you-rather"),
        Text("would you rather...?", (770, 462), size=40, face=MARKER, color=BLUE),
        Shape(star(770, 760, 50, seed=5), color=GOLD, fill=GOLD, width=6).at("best"),
        note("“best part of your day?”", (770, 870), size=44),
        tag("all work!", (770, 1040), size=56, color=TEAL).at("works").pop(),
    ]


def l_close():
    return [
        tag("GIVE THEM 5 MINUTES", (540, 340), size=74, color=TEAL).at("five").focus(1.08).pop(),
        *window(540, 650, 300, 300),
        note("...and they'll stop stealing them after.", (540, 950), size=50, color=INK,
             max_width=900).at("lights"),
        Text("goodnight.", (540, 1120), size=70, face=MARKER, color=BLUE).at("stealing"),
    ]


SCRIPT = [
    ("Lights off, and suddenly your kid wants to talk about everything. Don't shut it down. "
     "Here's why.", l_hook),
    ("It feels like stalling. But for a lot of kids, bedtime is the first quiet moment all day. "
     "No screens, no rushing, and you're right there.", l_quiet),
    ("And it's dark, side by side, no eye contact. That's when it's easiest for kids to say the "
     "big stuff.", l_side),
    ("So instead of fighting it, plan for it. Give them five minutes before lights out that are "
     "just for talking.", l_plan),
    ("Start with something easy. One silly question gets them going, and the real stuff often "
     "comes after.", l_start),
    ("One thing that works for us is one real-or-fake question every night. Like, “Koalas sleep "
     "up to twenty-two hours a day.” Real.", l_game),
    ("We use a book called Trick Trivia, but would-you-rather or “best part of your day” works "
     "too.", l_options),
    ("Give them five minutes before lights out, and they'll stop stealing them after.", l_close),
]

CAPTION = (
    "Lights off, and suddenly your kid wants to talk about everything. Don't shut it down. For "
    "a lot of kids, bedtime is the first quiet moment all day: no screens, no rushing, and "
    "you're right there. And in the dark, side by side, it's easier to say the big stuff. So "
    "plan for it: five minutes before lights out that are just for talking. Start with "
    "something easy, like one real-or-fake question. We use Trick Trivia (it's on Amazon), but "
    "would-you-rather or \"best part of your day\" works too. Give them five minutes before "
    "lights out, and they'll stop stealing them after."
)
HASHTAGS = ["#bedtimeroutine", "#parentingtips", "#momtok", "#dadtok", "#gentleparenting",
            "#connection", "#realorfake"]
