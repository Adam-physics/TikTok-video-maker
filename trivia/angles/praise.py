"""Angle: stop saying "good job." Here's what to say instead.

Value first, and honest: blanket praise is pleasant but tells a kid nothing,
and praise for being smart can make mistakes feel threatening. Asking "how
did you figure that out?" praises the part they control, the effort and the
strategy, and works even when they are wrong. The book is one source of
chances to ask, next to free ones; the close is back on the swap itself.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, check, circle, ellipse, line, rrect, star
from ..figures import bubble, cover, kid
from .reading import BLUE, GOLD, GREEN, GREY, PALE_GOLD, RED, TEAL, W, lightbulb, note, tag
from .school import speech
from .screens import crossed, lego, puzzle

ID = "praise"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“A day on Venus is longer than its year.”"
SWEAT = (120, 180, 230)


def sticker(cx, cy, r=110):
    return [Shape(star(cx, cy, r, seed=3), color=GOLD, fill=PALE_GOLD, width=8),
            Text("good job", (cx, cy + 12), size=34, face=MARKER, color=INK)]


def homework(cx, cy):
    return [Shape([rrect(cx - 85, cy - 110, cx + 85, cy + 110, r=8)] +
                  [line((cx - 60, cy - 60 + k * 36), (cx + 55 - (k % 2) * 30, cy - 60 + k * 36), wobble=0.8)
                   for k in range(4)], width=6, fill=(255, 255, 255), fill_offset=(0, 0)),
            Text("2+3=?", (cx, cy - 82), size=30, face=MARKER, color=BLUE)]


def drops(cx, cy):
    return Shape([ellipse(cx, cy, 10, 16, wobble=0.4), ellipse(cx + 34, cy + 30, 8, 13, wobble=0.4)],
                 color=SWEAT, fill=SWEAT, width=4, fill_offset=(0, 0))


# ------------------------------------------------------------------ boards

def l_hook():
    """Only the headline is there on frame one; the rest draws as it is said."""
    first = speech(330, 480, 170, 62, (260, 800), "GOOD JOB!", size=44)
    first[0].at("good")
    second = speech(600, 610, 170, 62, (330, 820), "GOOD JOB!", size=44)
    listener = kid(820, 1100, 0.75, "bored", "down")
    listener[0].at("barely")
    return [
        Text("“GOOD JOB!”", (540, 320), size=88, face=MARKER, color=RED).ready(),
        *kid(260, 1060, 0.95, "happy", "point"),
        *first,
        tag("×50", (860, 470), size=90, color=RED).at("fifty").pop(),
        *second,
        *listener,
        Text("?", (820, 760), size=140, face=MARKER, color=GREEN).at("what").focus(1.08).pop(),
    ]


def l_empty():
    return [
        *sticker(290, 500),
        note("not bad...", (290, 680), size=54, color=GREEN).at("bad"),
        bubble(720, 520, 250, 130, (620, 700)).at("empty"),
        Text("...", (720, 505), size=90, face=MARKER, color=GREY),
        tag("you're happy :)", (250, 1000), size=50, color=GOLD).at("happy"),
        tag("but WHAT did I", (730, 900), size=58, color=RED).at("not"),
        tag("do well?", (730, 990), size=58, color=RED).pop(),
    ]


def l_smart():
    return [
        *kid(470, 1040, 0.95, "shock", "down"),
        Shape(star(270, 560, 40, seed=2), color=GOLD, fill=GOLD, width=5).at("praise"),
        tag("SMART", (470, 560), size=80, color=GOLD).at("smart").pop(),
        Shape(rrect(700, 640, 980, 760, r=14), width=7, fill=(255, 255, 255), fill_offset=(0, 0)).at("wrong"),
        Text("2+2=5", (840, 700), size=56, face=MARKER, color=INK),
        crossed(840, 700, 60),
        drops(590, 780).at("scary"),
    ]


def l_swap():
    return [
        tag("“GOOD JOB”", (540, 350), size=76, color=GREY),
        Shape(line((330, 355), (750, 345)), color=RED, width=12).at("swap"),
        Shape(arrow((540, 420), (540, 540), head=26), color=TEAL, width=W).at("one"),
        Text("“How did you", (540, 650), size=92, face=MARKER, color=TEAL).at("how").focus(1.08),
        Text("figure that out?”", (540, 770), size=92, face=MARKER, color=TEAL).pop(),
        *kid(540, 1110, 0.72, "happy", "up"),
    ]


def l_control():
    talk = speech(330, 560, 200, 80, (300, 760), "First I tried...", size=42)
    talk[0].at("explain")
    return [
        *kid(300, 1060, 0.95, "happy", "point"),
        *talk,
        *[b.at("thinking") if k == 0 else b for k, b in enumerate(lightbulb(780, 470, r=52))],
        tag("what they control:", (720, 740), size=48, color=TEAL).at("control"),
        Shape(check(600, 850, 24), color=GREEN, width=10).at("effort"),
        note("effort", (650, 850), size=56, anchor="lm"),
        Shape(check(600, 950, 24), color=GREEN, width=10),
        note("strategy", (650, 950), size=56, anchor="lm"),
    ]


def l_wrong():
    ask = speech(400, 500, 300, 100, (300, 760), "Ooh, why did you think that?", size=46)
    ask[0].at("ooh")
    return [
        *kid(280, 1060, 0.95, "happy", "point"),
        *kid(800, 1090, 0.75, "think", "chin"),
        tag("WRONG", (820, 640), size=60, color=RED).at("wrong"),
        *ask,
        tag("still curious!", (820, 790), size=44, color=TEAL).at("think"),
    ]


def l_game():
    because = speech(620, 760, 220, 80, (430, 900), "because...", size=50)
    because[0].at("every")
    return [
        *kid(330, 1070, 0.95, "think", "chin"),
        Shape(rrect(60, 300, 1020, 450, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0))
        .at("real-or-fake"),
        note(CLAIM, (540, 375), size=50),
        tag("REAL OR FAKE?", (540, 530), size=60, color=GOLD).pop(),
        *because,
        tag("every guess = a reason", (680, 960), size=46, color=TEAL).at("comes"),
    ]


def l_options():
    return [
        *kid(240, 1040, 0.95, "happy", "hold"),
        Picture(cover(), (240, 985), width=112, angle=-4).at("book"),
        note("Trick Trivia", (280, 650), size=42, color=GREY).at("trick"),
        Shape(arrow((330, 690), (305, 930), bend=-30, head=18), color=GREY, width=6),
        puzzle(720, 470, 60).at("puzzles"),
        note("puzzles", (720, 580), size=42, color=GREY),
        lego(600, 800).at("lego"),
        note("Lego", (600, 890), size=42, color=GREY),
        *[h.at("homework") if k == 0 else h for k, h in enumerate(homework(880, 820))],
        note("homework", (880, 970), size=42, color=GREY),
    ]


def l_close():
    return [
        tag("LESS “GOOD JOB.”", (540, 420), size=80, color=GREY),
        tag("MORE:", (540, 600), size=80, color=TEAL).at("more"),
        Text("“How did you figure that out?”", (540, 760), size=70, face=MARKER, color=TEAL,
             max_width=980).focus(1.08).pop(),
        Shape(star(540, 980, 60, seed=9), color=GOLD, fill=GOLD, width=6),
    ]


SCRIPT = [
    ("You say “good job” fifty times a day. Your kid barely hears it anymore. Here's what to "
     "say instead.", l_hook),
    ("“Good job” isn't bad. It's just empty. It tells them you're happy, not what they did "
     "well.", l_empty),
    ("And when praise is always about being smart, being wrong starts to feel scary.", l_smart),
    ("So swap it for one question: “How did you figure that out?”", l_swap),
    ("Now they explain their thinking, and you're praising the part they control: the effort "
     "and the strategy.", l_control),
    ("It works even when they're wrong. “Ooh, why did you think that?”", l_wrong),
    ("One thing that gives us lots of chances to ask is real-or-fake questions. Every guess "
     "comes with a reason.", l_game),
    ("We use a book called Trick Trivia, but puzzles, Lego builds, even homework work too.",
     l_options),
    ("Less “good job.” More “how did you figure that out?”", l_close),
]

CAPTION = (
    "You say \"good job\" fifty times a day, and your kid barely hears it anymore. \"Good job\" "
    "isn't bad, it's just empty: it tells them you're happy, not what they did well. And when "
    "praise is always about being smart, being wrong starts to feel scary. So swap it for one "
    "question: \"How did you figure that out?\" Now they explain their thinking, and you're "
    "praising what they control, the effort and the strategy. It works even when they're "
    "wrong. We get lots of chances with real-or-fake questions from Trick Trivia (it's on "
    "Amazon), but puzzles, Lego and homework work too. Less \"good job.\" More \"how did you "
    "figure that out?\""
)
HASHTAGS = ["#parentingtips", "#gentleparenting", "#momtok", "#dadtok", "#growthmindset",
            "#positiveparenting", "#realorfake"]
