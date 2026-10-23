"""Angle: your kid is confidently wrong. Don't correct them; ask how you could check.

Value first, and honest: a flat "no, that's wrong" ends the conversation and
hands over the answer, while "how could we check?" turns it into a small
mission they do the thinking for. Being wrong yourself, out loud, models it.
The book is one source of practice, next to any "did you know" from a show or
a friend, and the close is back on the line itself.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, circle, curve, ellipse, heart, line, poly, rrect
from ..figures import bubble, cover, kid, magnifier
from .reading import BLUE, GOLD, GREEN, GREY, PALE_GOLD, RED, TEAL, W, lightbulb, note, tag
from .school import speech
from .screens import crossed

ID = "check"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
BANANA = (255, 222, 90)
BERRY = (226, 60, 70)
BLUEBERRY = (70, 90, 170)


def beaker(cx, cy):
    return [Shape(poly([(cx - 30, cy - 100), (cx - 30, cy - 20), (cx - 90, cy + 90), (cx + 90, cy + 90),
                        (cx + 30, cy - 20), (cx + 30, cy - 100)], wobble=1.0), width=W),
            Shape(poly([(cx - 62, cy + 40), (cx + 62, cy + 40), (cx + 84, cy + 84), (cx - 84, cy + 84)],
                       closed=True, wobble=0.8), color=GREEN, fill=(190, 234, 200), width=5, fill_offset=(0, 0)),
            Shape([circle(cx - 10, cy - 10, 10, wobble=0.4), circle(cx + 14, cy - 50, 7, wobble=0.4)],
                  color=GREEN, width=5)]


def banana(cx, cy, s=1.0):
    top = [(cx - 150 * s, cy - 60 * s), (cx - 60 * s, cy + 30 * s), (cx + 70 * s, cy + 30 * s),
           (cx + 150 * s, cy - 50 * s)]
    bottom = [(cx + 150 * s, cy - 50 * s), (cx + 80 * s, cy + 80 * s), (cx - 60 * s, cy + 80 * s),
              (cx - 150 * s, cy - 60 * s)]
    return [Shape(poly(_spline(top) + _spline(bottom), closed=True, wobble=1.0), color=(190, 150, 30),
                  fill=BANANA, width=W, fill_offset=(0, 0)),
            Shape(line((cx - 150 * s, cy - 60 * s), (cx - 170 * s, cy - 80 * s)), color=(120, 90, 40), width=10)]


def _spline(pts):
    return [tuple(p) for p in curve(pts, wobble=0.0)]


def strawberry(cx, cy, s=1.0):
    return [Shape(heart(cx, cy, 52 * s, seed=2), color=(170, 30, 40), fill=BERRY, width=7),
            Shape([line((cx - 30 * s, cy - 50 * s), (cx, cy - 34 * s)), line((cx + 30 * s, cy - 50 * s), (cx, cy - 34 * s)),
                   line((cx, cy - 66 * s), (cx, cy - 34 * s))], color=GREEN, width=8)]


def blueberries(cx, cy):
    return Shape([circle(cx, cy, 26, wobble=0.5), circle(cx + 50, cy + 10, 24, wobble=0.5),
                  circle(cx + 22, cy - 38, 22, wobble=0.5)], color=(40, 50, 110), fill=BLUEBERRY, width=6,
                 fill_offset=(0, 0))


def tv(cx, cy):
    return [Shape([line((cx - 40, cy - 110), (cx, cy - 75)), line((cx + 40, cy - 115), (cx, cy - 75))], width=7),
            Shape(rrect(cx - 120, cy - 75, cx + 120, cy + 85, r=18), width=W, fill=(60, 66, 80), fill_offset=(0, 0)),
            Shape(rrect(cx - 98, cy - 55, cx + 98, cy + 65, r=8), width=4, fill=(190, 222, 255), fill_offset=(0, 0))]


# ------------------------------------------------------------------ boards

def l_hook():
    """Only the headline is there on frame one; the scene draws as it is said."""
    claim = speech(330, 500, 250, 90, (290, 800), "Sharks are mammals!", size=44)
    claim[0].at("says")
    parent = kid(820, 1080, 0.95, "bored", "down")
    parent[0].at("fact")
    no = speech(790, 660, 190, 76, (800, 790), "NO, that's wrong.", size=38)
    return [
        Text("CONFIDENTLY WRONG", (540, 320), size=80, face=MARKER, color=RED).ready(),
        *kid(290, 1060, 0.95, "happy", "point"),
        *claim,
        *parent,
        *no,
        crossed(790, 660, 85).at("correct"),
        Text("?", (550, 900), size=150, face=MARKER, color=GREEN).at("what").focus(1.08).pop(),
    ]


def l_shrink():
    bulb = lightbulb(780, 820, r=50)
    bulb[0].at("thinking")
    return [
        tag("“No, that's wrong.”", (540, 340), size=66, color=GREY),
        *kid(300, 1070, 0.95, "bored", "down"),
        bubble(360, 700, 90, 50, (310, 820)).at("stop"),
        Text("...", (360, 692), size=50, face=MARKER, color=GREY),
        tag("stop sharing", (760, 560), size=58, color=RED).at("sharing"),
        *bulb,
        crossed(780, 820, 80).at("because"),
        tag("answer handed over", (700, 1060), size=46, color=GREY).at("handed"),
    ]


def l_swap():
    return [
        tag("TRY THIS:", (540, 360), size=80, color=INK),
        Text("“Ooh, how could", (540, 600), size=96, face=MARKER, color=TEAL).at("ooh").focus(1.08),
        Text("we check?”", (540, 720), size=96, face=MARKER, color=TEAL).pop(),
        *kid(540, 1110, 0.72, "happy", "up"),
    ]


def l_mission():
    return [
        tag("A MISSION!", (540, 340), size=90, color=GOLD).at("mission").pop(),
        note("(not a correction)", (540, 440), size=46, color=GREY).at("correction"),
        *[m.at("look") if k == 0 else m for k, m in enumerate(magnifier(200, 760, 70))],
        note("look it up", (220, 960), size=46),
        *[f.at("together") if k == 0 else f for k, f in enumerate(kid(495, 840, 0.5, "happy", "down"))],
        *kid(605, 840, 0.5, "think", "chin"),
        note("ask someone", (550, 1010), size=46),
        *[b.at("someone") if k == 0 else b for k, b in enumerate(beaker(870, 790))],
        note("test it", (870, 960), size=46),
    ]


def l_wrong():
    oops = speech(390, 530, 230, 84, (300, 780), "I was wrong!", size=50)
    oops[0].at("wrong")
    child = kid(800, 1090, 0.75, "happy", "up")
    child[0].at("better")
    return [
        *kid(280, 1060, 0.95, "happy", "point"),
        *oops,
        *child,
        tag("say it out loud", (790, 690), size=44, color=GREY).at("say"),
        tag("checking > being sure", (540, 340), size=60, color=TEAL).at("checking").focus(1.06).pop(),
    ]


def l_banana():
    return [
        *kid(860, 1110, 0.7, "think", "chin"),
        tag("REAL OR FAKE?", (540, 330), size=64, color=GOLD).at("real-or-fake"),
        Shape(rrect(150, 400, 930, 520, r=24), width=W, fill=(255, 255, 255), fill_offset=(0, 0)).at("like"),
        note("“Bananas are berries.”", (540, 462), size=60),
        *[b.at("bananas") if k == 0 else b for k, b in enumerate(banana(330, 760, 0.9))],
        *[b.at("berries") if k == 0 else b for k, b in enumerate(strawberry(610, 750))],
        blueberries(730, 790),
        tag("fake?", (860, 880), size=50, color=GREY).at("fake"),
        tag("REAL!", (480, 1040), size=120, color=GREEN).at("check").focus(1.12).pop(),
    ]


def l_options():
    return [
        *kid(240, 1040, 0.95, "happy", "hold"),
        Picture(cover(), (240, 985), width=112, angle=-4).at("book"),
        note("Trick Trivia", (280, 650), size=42, color=GREY).at("trick"),
        Shape(arrow((330, 690), (305, 930), bend=-30, head=18), color=GREY, width=6),
        bubble(740, 420, 220, 80, (680, 540)).at("did"),
        Text("did you know...?", (740, 422), size=44, face=MARKER, color=BLUE),
        *[t.at("show") if k == 0 else t for k, t in enumerate(tv(660, 740))],
        note("a show", (660, 880), size=42, color=GREY),
        *[f.at("friend") if k == 0 else f for k, f in enumerate(kid(890, 1000, 0.6, "happy", "point"))],
        note("a friend", (890, 1150), size=42, color=GREY),
    ]


def l_close():
    return [
        tag("DON'T SAY “NO.”", (540, 400), size=84, color=GREY),
        tag("SAY:", (540, 580), size=84, color=TEAL).at("say"),
        Text("“How could we check?”", (540, 740), size=84, face=MARKER, color=TEAL,
             max_width=1000).at("how").focus(1.08).pop(),
        *magnifier(540, 960, 70),
    ]


SCRIPT = [
    ("Your kid says something totally wrong, like it's a fact. Don't correct them. Here's what "
     "to say instead.", l_hook),
    ("When we jump in with “No, that's wrong,” they hear: stop sharing. And they stop thinking, "
     "because we just handed them the answer.", l_shrink),
    ("So try this: “Ooh, how could we check?”", l_swap),
    ("Now it's a mission, not a correction. Look it up together, ask someone, or test it.",
     l_mission),
    ("And if you turn out to be wrong? Even better. Say it out loud. They learn that checking "
     "beats being sure.", l_wrong),
    ("One thing that gives us practice is real-or-fake questions. Like, “Bananas are berries.” "
     "Most kids say fake. Check it. It's real.", l_banana),
    ("We use a book called Trick Trivia, but any “did you know” from a show or a friend works "
     "too.", l_options),
    ("Next time they're confidently wrong, don't say no. Say, “How could we check?”", l_close),
]

CAPTION = (
    "Your kid says something totally wrong, like it's a fact. Don't correct them. When we jump "
    "in with \"no, that's wrong,\" they hear \"stop sharing,\" and they stop thinking because we "
    "just handed them the answer. Try this instead: \"Ooh, how could we check?\" Now it's a "
    "mission: look it up together, ask someone, or test it. And if you turn out to be wrong, "
    "say it out loud. They learn that checking beats being sure. We practice with real-or-fake "
    "questions from Trick Trivia (it's on Amazon), but any \"did you know\" from a show or a "
    "friend works too. (Bananas really are berries.)"
)
HASHTAGS = ["#parentingtips", "#gentleparenting", "#momtok", "#dadtok", "#criticalthinking",
            "#curiouskids", "#realorfake"]
