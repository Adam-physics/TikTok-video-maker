"""Angle: "I'm bored." You've tried everything. Here's why it keeps coming back.

Value first, and honest: boredom is often the moment right before a kid
starts something on their own, and always filling it teaches them that fun
is handed to them. The fix is a starter, not an activity: one odd question
or one thing to figure out, then step back. The book is named once as one
kind of starter, next to free ones, and the close is back on the habit.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, circle, curve, ellipse, line, poly, rrect, star
from ..explainer import KEEP
from ..figures import bubble, cover, kid, magnifier
from .reading import BLUE, GOLD, GREEN, GREY, PALE_GOLD, RED, TEAL, W, lightbulb, note, tag
from .school import PINK, speech
from .screens import crossed

ID = "bored"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“Cats can't taste sweet things.”"
SKY = (200, 222, 250)
MINT = (206, 236, 214)
SAND = (240, 214, 170)


def todo(cx, cy):
    x0, y0 = cx - 120, cy - 95
    return [Shape([rrect(x0, y0, x0 + 240, y0 + 190, r=10)] +
                  [line((x0 + 30, y0 + 50 + k * 45), (x0 + 200 - (k % 2) * 40, y0 + 50 + k * 45), wobble=0.8)
                   for k in range(3)], width=6, fill=(255, 255, 255), fill_offset=(0, 0))]


def craft_kit(cx, cy):
    return [Shape([rrect(cx - 115, cy - 60, cx + 115, cy + 70, r=10),
                   line((cx - 115, cy - 20), (cx + 115, cy - 20))], width=7, fill=PINK, fill_offset=(0, 0)),
            Shape([circle(cx - 50, cy + 25, 22, wobble=0.5), circle(cx + 10, cy + 25, 22, wobble=0.5)],
                  color=BLUE, width=6),
            Shape(line((cx + 50, cy + 50), (cx + 95, cy)), color=GOLD, width=10)]


def tree(cx, cy, s=1.0):
    return [Shape([line((cx, cy + 90 * s), (cx, cy))], color=(130, 90, 60), width=12),
            Shape(circle(cx, cy - 30 * s, 70 * s), color=GREEN, fill=MINT, width=7, fill_offset=(0, 0))]


def gift(cx, cy, w=200, h=150):
    x0, y0 = cx - w / 2, cy - h / 2
    return Shape([rrect(x0, y0, x0 + w, y0 + h, r=8), line((cx, y0), (cx, y0 + h)),
                  line((x0, cy), (x0 + w, cy)),
                  curve([(cx, y0), (cx - 40, y0 - 40), (cx - 10, y0 - 30), (cx, y0)]),
                  curve([(cx, y0), (cx + 40, y0 - 40), (cx + 10, y0 - 30), (cx, y0)])],
                 width=7, fill=PALE_GOLD, fill_offset=(0, 0))


def couch(cx, cy):
    return Shape([rrect(cx - 200, cy - 70, cx + 200, cy + 40, r=24),
                  rrect(cx - 240, cy - 20, cx - 180, cy + 80, r=18),
                  rrect(cx + 180, cy - 20, cx + 240, cy + 80, r=18),
                  rrect(cx - 180, cy + 10, cx + 180, cy + 80, r=10),
                  line((cx - 170, cy + 80), (cx - 170, cy + 110)), line((cx + 170, cy + 80), (cx + 170, cy + 110))],
                 width=W, fill=SKY, fill_offset=(0, 0))


def tower(cx, base, n=6):
    fills = [PINK, PALE_GOLD, MINT, SKY]
    return [Shape(rrect(cx - 60 + (k % 2) * 8, base - (k + 1) * 62, cx + 60 + (k % 2) * 8, base - k * 62, r=6),
                  width=7, fill=fills[k % 4], fill_offset=(0, 0)) for k in range(n)]


def spark(cx, cy):
    flame = Shape(poly([(cx, cy - 150), (cx + 60, cy - 40), (cx + 45, cy + 30), (cx, cy + 50),
                        (cx - 45, cy + 30), (cx - 60, cy - 40)], closed=True, wobble=1.5),
                  color=(230, 110, 20), fill=(255, 200, 90), width=W, fill_offset=(0, 0))
    inner = Shape(poly([(cx, cy - 60), (cx + 22, cy), (cx, cy + 30), (cx - 22, cy)], closed=True, wobble=1.0),
                  color=RED, fill=(255, 150, 60), width=5, fill_offset=(0, 0))
    rays = Shape([line((cx - 110, cy - 110), (cx - 80, cy - 80)), line((cx + 110, cy - 110), (cx + 80, cy - 80)),
                  line((cx, cy - 200), (cx, cy - 175))], color=GOLD, width=8)
    return [flame, inner, rays]


def spoon(cx, cy):
    return Shape([ellipse(cx, cy - 60, 34, 50), line((cx, cy - 10), (cx, cy + 110))], width=8,
                 fill=(220, 224, 232), fill_offset=(0, 0))


# ------------------------------------------------------------------ boards

def l_hook():
    """Frame one is already the whole problem; the X's land as each is named."""
    return [
        Text("“I'M BORED.”", (540, 330), size=96, face=MARKER, color=RED).ready(),
        *[it.ready() for it in kid(290, 1060, 0.95, "bored", "down")],
        *[it.ready() for it in todo(790, 580)],
        *[it.ready() for it in craft_kit(790, 840)],
        *[it.ready() for it in tree(790, 1090, 0.9)],
        note("activity lists", (790, 700), size=40, color=GREY).ready(),
        note("craft kits", (790, 940), size=40, color=GREY).ready(),
        note("go outside", (790, 1195), size=40, color=GREY).ready(),
        crossed(790, 580).at("lists"),
        crossed(790, 840).at("kits"),
        crossed(790, 1075).at("outside"),
        Text("?", (300, 640), size=170, face=MARKER, color=GREEN).at("why").focus(1.08).pop(),
    ]


def l_why():
    cloud = Shape(ellipse(540, 900, 260, 120), color=GREY, width=7)
    return [
        tag("a problem?", (540, 340), size=64, color=GREY).at("problem"),
        Shape(line((370, 345), (710, 335)), color=RED, width=10),
        cloud.at("moment"),
        note("bored...", (540, 905), size=60, color=GREY),
        Shape(arrow((540, 760), (540, 640), head=24), color=GOLD, width=W).at("right"),
        *lightbulb(540, 520, r=56),
        tag("their own idea", (540, 1110), size=60, color=TEAL).at("own").focus(1.08).pop(),
    ]


def l_handed():
    return [
        *kid(280, 1050, 1.0, "happy", "hold"),
        gift(400, 900, 160, 120).at("jump"),
        Shape(arrow((510, 900), (680, 930), bend=-20, head=22), color=GREY, width=7),
        *kid(800, 1100, 0.75, "bored", "down"),
        tag("“fun gets handed to me”", (540, 360), size=56, color=RED).at("handed").focus(1.08).pop(),
    ]


def l_fix():
    return [
        tag("NOT AN ACTIVITY.", (540, 340), size=76, color=GREY).at("activity"),
        Shape(line((190, 345), (890, 335)), color=RED, width=10),
        tag("A STARTER.", (540, 470), size=100, color=TEAL).at("starter").focus(1.08).pop(),
        Text("?", (200, 760), size=170, face=MARKER, color=GOLD).at("weird"),
        note("weird question", (200, 900), size=40, color=GREY),
        *magnifier(540, 740, 70),
        note("figure it out", (540, 900), size=40, color=GREY).at("figure"),
        Shape(arrow((790, 760), (970, 760), head=24), color=TEAL, width=W).at("step"),
        note("step back", (880, 900), size=40, color=GREY),
    ]


def l_example():
    ask = speech(540, 360, 400, 100, (300, 560), "Can you build a tower taller than the couch?", size=44)
    return [
        *ask,
        couch(740, 1070),
        *[t.at("tower") if k == 0 else t for k, t in enumerate(tower(330, 1180, 7))],
        Shape(line((150, 1185), (1010, 1185)), color=GREY, width=4),
        tag("then walk away", (720, 760), size=56, color=TEAL).at("walk").pop(),
    ]


def l_game():
    return [
        Shape(rrect(90, 300, 990, 450, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        note(CLAIM, (540, 375), size=56).at("real-or-fake"),
        tag("REAL OR FAKE?", (540, 540), size=64, color=GOLD).pop(),
        *kid(330, 1060, 0.95, "think", "chin"),
        *magnifier(700, 820, 80),
        tag("go find out!", (720, 1060), size=60, color=TEAL).at("find").focus(1.08).pop(),
    ]


def l_options():
    return [
        *kid(250, 1040, 0.95, "happy", "hold"),
        Picture(cover(), (250, 985), width=112, angle=-4).at("book"),
        note("Trick Trivia", (290, 650), size=42, color=GREY).at("trick"),
        Shape(arrow((340, 690), (315, 930), bend=-30, head=18), color=GREY, width=6),
        Text("?", (720, 420), size=130, face=MARKER, color=GOLD).at("riddle"),
        note("a riddle", (720, 540), size=42, color=GREY),
        spoon(600, 760).at("weird"),
        note("a weird object", (600, 900), size=42, color=GREY),
        bubble(870, 760, 120, 70, (870, 860)).at("what"),
        Text("what if...?", (870, 762), size=36, face=MARKER, color=BLUE),
    ]


def l_close():
    return [
        tag("DON'T FILL IT.", (540, 340), size=80, color=GREY).at("bored"),
        *spark(540, 760),
        tag("SPARK IT.", (540, 1000), size=96, color=TEAL).at("spark").focus(1.08).pop(),
    ]


SCRIPT = [
    ("You've made activity lists. Bought craft kits. Sent them outside. Five minutes later, "
     "“I'm bored.” Here's why.", l_hook),
    ("Boredom isn't really the problem. It's often the moment right before a kid comes up "
     "with their own idea.", l_why),
    ("But if we always jump in with the next activity, they never get there. They learn that "
     "fun gets handed to them.", l_handed),
    ("So don't hand them an activity. Hand them a starter. One weird question, one thing to "
     "figure out, then step back.", l_fix),
    ("Like, “Can you build a tower taller than the couch?” Then walk away.", l_example),
    ("One starter that works for us is a real-or-fake question. I read one wild claim, and "
     "they go find out if it's true.", l_game),
    ("We use a book called Trick Trivia, but a riddle, a weird object, or a “what if” "
     "works just as well.", l_options),
    ("Next time they're bored, don't fill it. Spark it, and step back.", l_close),
]

CAPTION = (
    "You've made activity lists, bought craft kits, sent them outside, and five minutes later: "
    "\"I'm bored.\" Boredom isn't really the problem. It's often the moment right before a kid "
    "comes up with their own idea, and if we always jump in with the next activity, they "
    "never get there. So don't hand them an activity, hand them a starter: one weird question, "
    "one thing to figure out, then step back. We use Trick Trivia (it's on Amazon), but a "
    "riddle, a weird object or a \"what if\" works just as well. Don't fill it. Spark it."
)
HASHTAGS = ["#imbored", "#parentingtips", "#momtok", "#dadtok", "#kidsactivities",
            "#boredkids", "#realorfake"]
