"""Angle: fine all day at school, falls apart the second they get home.

Value first, and honest: after a day of rules, sitting still and holding in
big feelings, home is the first safe place to let go; therapists often call
it after-school restraint collapse. The fix is to skip the pickup questions,
snack and quiet first, then reconnect with something light. The book is one
light opener next to free ones; the close is back on the reassurance.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, circle, curve, ellipse, heart, line, poly, rrect
from ..figures import bubble, bumpy, cover, kid
from .reading import BLUE, GOLD, GREEN, GREY, PALE_GOLD, RED, TEAL, W, note, tag
from .school import PINK, clock, speech
from .screens import crossed

ID = "meltdown"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“A group of flamingos is called a flamboyance.”"
BRICK = (240, 200, 180)
CLOUD = (196, 200, 210)
ORANGE = (240, 140, 40)
FLAMINGO = (248, 160, 180)


def school(cx, cy):
    return [Shape([rrect(cx - 130, cy - 60, cx + 130, cy + 90, r=6),
                   poly([(cx - 150, cy - 60), (cx, cy - 150), (cx + 150, cy - 60)], wobble=1.0),
                   rrect(cx - 26, cy + 20, cx + 26, cy + 90, r=4)], width=W, fill=BRICK, fill_offset=(0, 0)),
            Shape([line((cx, cy - 150), (cx, cy - 220)),
                   poly([(cx, cy - 220), (cx + 50, cy - 205), (cx, cy - 190)], closed=True, wobble=0.5)],
                  color=RED, width=6)]


def house(cx, cy):
    return [Shape([rrect(cx - 110, cy - 50, cx + 110, cy + 90, r=6),
                   poly([(cx - 135, cy - 50), (cx, cy - 150), (cx + 135, cy - 50)], wobble=1.0),
                   rrect(cx - 24, cy + 20, cx + 24, cy + 90, r=4)], width=W, fill=PALE_GOLD, fill_offset=(0, 0)),
            Shape(rrect(cx + 40, cy - 20, cx + 85, cy + 20, r=4), width=6, fill=(200, 222, 250),
                  fill_offset=(0, 0))]


def storm(cx, cy, s=1.0):
    return [Shape(bumpy(cx, cy, 130 * s, 60 * s, bumps=9, depth=0.12), color=GREY, fill=CLOUD, width=7,
                  fill_offset=(0, 0)),
            Shape(poly([(cx + 10 * s, cy + 50 * s), (cx - 20 * s, cy + 110 * s), (cx + 10 * s, cy + 110 * s),
                        (cx - 15 * s, cy + 170 * s)], wobble=0.6), color=GOLD, width=8)]


def apple(cx, cy, r=55):
    return [Shape(circle(cx, cy, r), color=(170, 30, 40), fill=(226, 60, 70), width=7, fill_offset=(0, 0)),
            Shape(line((cx, cy - r + 6), (cx + 6, cy - r - 24)), color=(110, 80, 40), width=7),
            Shape(ellipse(cx + 26, cy - r - 12, 20, 10, rot=-20), color=GREEN, fill=(190, 234, 200), width=5,
                  fill_offset=(0, 0))]


def flamingo(cx, cy, s=1.0):
    return [Shape([line((cx - 6 * s, cy + 40 * s), (cx - 6 * s, cy + 190 * s)),
                   poly([(cx + 10 * s, cy + 40 * s), (cx + 10 * s, cy + 110 * s), (cx + 50 * s, cy + 90 * s)],
                        wobble=0.6)], color=(200, 90, 110), width=6),
            Shape(ellipse(cx, cy, 70 * s, 42 * s), color=(200, 90, 110), fill=FLAMINGO, width=7,
                  fill_offset=(0, 0)),
            Shape(curve([(cx + 50 * s, cy - 20 * s), (cx + 80 * s, cy - 90 * s), (cx + 50 * s, cy - 150 * s),
                         (cx + 70 * s, cy - 180 * s)], wobble=0.6), color=(200, 90, 110), width=9),
            Shape(circle(cx + 76 * s, cy - 186 * s, 18 * s, wobble=0.4), color=(200, 90, 110), fill=FLAMINGO,
                  width=6, fill_offset=(0, 0)),
            Shape(poly([(cx + 92 * s, cy - 192 * s), (cx + 118 * s, cy - 172 * s), (cx + 92 * s, cy - 178 * s)],
                       wobble=0.3), width=5)]


def car(cx, cy):
    return [Shape([rrect(cx - 120, cy - 30, cx + 120, cy + 40, r=16),
                   poly([(cx - 70, cy - 30), (cx - 40, cy - 80), (cx + 50, cy - 80), (cx + 80, cy - 30)],
                        wobble=0.8)], width=W, fill=(200, 222, 250), fill_offset=(0, 0)),
            Shape([circle(cx - 65, cy + 45, 24, wobble=0.4), circle(cx + 65, cy + 45, 24, wobble=0.4)],
                  fill=INK, width=6, fill_offset=(0, 0))]


def music(cx, cy):
    return Shape([circle(cx, cy, 14, wobble=0.3), line((cx + 13, cy), (cx + 13, cy - 60)),
                  circle(cx + 50, cy - 12, 14, wobble=0.3), line((cx + 63, cy - 12), (cx + 63, cy - 72)),
                  line((cx + 13, cy - 60), (cx + 63, cy - 72))], color=BLUE, fill=BLUE, width=6,
                 fill_offset=(0, 0))


def pillow(cx, cy):
    return Shape([rrect(cx - 220, cy - 70, cx + 220, cy + 70, r=60),
                  curve([(cx - 150, cy), (cx, cy + 14), (cx + 150, cy)], wobble=0.8)], width=W,
                 fill=(220, 232, 255), fill_offset=(0, 0))


# ------------------------------------------------------------------ boards

def l_hook():
    """Only the headline is there on frame one; the scene draws as it is said."""
    calm = kid(270, 1110, 0.6, "happy", "down")
    calm[0].at("together")
    home = house(800, 730)
    home[0].at("then")
    cloud = storm(800, 885, 0.65)
    cloud[0].at("apart")
    upset = kid(800, 1150, 0.55, "shock", "down")
    return [
        Text("AFTER-SCHOOL MELTDOWN", (540, 320), size=64, face=MARKER, color=RED, max_width=1040).ready(),
        *school(270, 730),
        *calm,
        *home,
        *cloud,
        *upset,
        tag("IT'S NOT YOU.", (540, 450), size=64, color=TEAL).at("it's").focus(1.06).pop(),
    ]


def l_pressure():
    bar = Shape(rrect(480, 420, 600, 920, r=20), width=W)
    levels = [(760, 920, GOLD, "rules", "rules"), (600, 760, ORANGE, "sitting", "sitting still"),
              (440, 600, RED, "feelings", "big feelings")]
    out = [bar]
    for y0, y1, color, cue, label in levels:
        out.append(Shape(rrect(488, y0, 592, y1 - 4, r=12), color=color, fill=color, width=4,
                         fill_offset=(0, 0)).at(cue))
        out.append(note(label, (440, (y0 + y1) / 2), size=48, anchor="rm"))
    return out + [
        *[h.at("home") if k == 0 else h for k, h in enumerate(house(840, 760))],
        Shape([line((540, 400), (540, 330)), line((480, 410), (430, 350)), line((600, 410), (650, 350))],
              color=RED, width=9).at("safe"),
        tag("safe to let go", (540, 1060), size=66, color=TEAL).pop(),
    ]


def l_safe():
    return [
        note("some experts call it", (540, 330), size=50, color=GREY),
        tag("RESTRAINT", (540, 440), size=84, color=RED).at("restraint"),
        tag("COLLAPSE", (540, 540), size=84, color=RED),
        Shape(heart(540, 760, 90, seed=2), color=RED, fill=(250, 140, 150), width=8).at("actually"),
        tag("= they feel safe with you", (540, 960), size=60, color=TEAL).at("safe").focus(1.08).pop(),
    ]


def l_pickup():
    ask = speech(540, 400, 330, 90, (420, 520), "How was school? What did you...?", size=42)
    return [
        *ask,
        crossed(540, 400, 110).at("questions"),
        *[a.at("snack") if k == 0 else a for k, a in enumerate(apple(230, 720))],
        note("snack", (230, 840), size=50),
        tag("shh...", (540, 720), size=70, color=BLUE).at("quiet"),
        note("quiet", (540, 840), size=50),
        *[c.at("twenty") if k == 0 else c for k, c in enumerate(clock(850, 720, 85))],
        note("20 min", (850, 840), size=50),
        tag("let them land", (540, 1010), size=64, color=TEAL).at("minutes").pop(),
    ]


def l_light():
    light = speech(430, 540, 230, 86, (330, 780), "Wanna hear something weird?", size=40)
    light[0].at("light")
    return [
        *kid(300, 1060, 0.95, "happy", "point"),
        *kid(780, 1090, 0.75, "happy", "down"),
        *light,
        note("“how was your day?”", (780, 780), size=40, color=GREY).at("not"),
        Shape(line((620, 785), (940, 775)), color=RED, width=9).at("how"),
    ]


def l_flamingo():
    flock = [flamingo(200, 860, 0.85), flamingo(400, 830, 0.95), flamingo(600, 870, 0.85)]
    flock[0][0].at("flamingos")
    return [
        *kid(880, 1110, 0.68, "think", "chin"),
        tag("REAL OR FAKE?", (540, 330), size=64, color=GOLD).at("real-or-fake"),
        Shape(rrect(70, 390, 1010, 590, r=24), width=W, fill=(255, 255, 255), fill_offset=(0, 0)).at("like"),
        note(CLAIM, (540, 490), size=50, max_width=880),
        *[it for f in flock for it in f],
        tag("REAL!", (420, 1150), size=110, color=GREEN).at("flamboyance").focus(1.1).pop(),
    ]


def l_options():
    return [
        Shape(rrect(110, 1000, 450, 1170, r=10), width=W, fill=(230, 200, 160), fill_offset=(0, 0)),
        *apple(180, 950, 40),
        Picture(cover(), (360, 925), width=112, angle=5).at("book"),
        note("Trick Trivia", (330, 700), size=44, color=GREY).at("trick"),
        Shape(arrow((350, 740), (360, 840), head=18), color=GREY, width=6),
        bubble(760, 420, 200, 76, (700, 530)).at("joke"),
        Text("knock knock!", (760, 422), size=44, face=MARKER, color=GOLD),
        *[c.at("song") if k == 0 else c for k, c in enumerate(car(740, 720))],
        music(860, 620),
        *[f.at("sitting") if k == 0 else f for k, f in enumerate(kid(700, 1000, 0.5, "happy", "down"))],
        *kid(820, 1010, 0.42, "happy", "down"),
        Shape(heart(760, 840, 22), color=RED, fill=(250, 140, 150), width=5),
    ]


def l_close():
    return [
        *storm(540, 390, 0.85),
        tag("it's the pressure coming out", (540, 590), size=56, color=GREY).at("pressure"),
        pillow(540, 770).at("coming"),
        tag("GIVE IT SOMEWHERE", (540, 920), size=70, color=TEAL).at("give").focus(1.06),
        tag("SOFT TO LAND.", (540, 1010), size=70, color=TEAL).pop(),
    ]


SCRIPT = [
    ("Your kid holds it together all day at school… then falls apart the second they get home. "
     "It's not you. Here's why.", l_hook),
    ("All day they're following rules, sitting still, and holding in big feelings. Home is the "
     "first place it's safe to let go.", l_pressure),
    ("Some experts call it after-school restraint collapse. It actually means they feel safe "
     "with you.", l_safe),
    ("So skip the questions at pickup. Snack first. Quiet first. Give them twenty minutes to "
     "land.", l_pickup),
    ("Then reconnect with something light, not “how was your day?”", l_light),
    ("One thing that works for us is one silly real-or-fake question over snack. Like, “A group "
     "of flamingos is called a flamboyance.” Real.", l_flamingo),
    ("We use a book called Trick Trivia, but a joke, a song in the car, or just sitting "
     "together works too.", l_options),
    ("The meltdown isn't the problem. It's the pressure coming out. Give it somewhere soft to "
     "land.", l_close),
]

CAPTION = (
    "Your kid holds it together all day at school, then falls apart the second they get home. "
    "It's not you. All day they're following rules, sitting still and holding in big feelings, "
    "and home is the first place it's safe to let go. Some experts call it after-school "
    "restraint collapse, and it actually means they feel safe with you. So skip the questions "
    "at pickup: snack first, quiet first, twenty minutes to land. Then reconnect with "
    "something light. We use a silly real-or-fake question from Trick Trivia (it's on Amazon), "
    "but a joke, a song in the car or just sitting together works too. Give it somewhere soft "
    "to land."
)
HASHTAGS = ["#afterschoolrestraintcollapse", "#parentingtips", "#gentleparenting", "#momtok",
            "#dadtok", "#meltdown", "#realorfake"]
