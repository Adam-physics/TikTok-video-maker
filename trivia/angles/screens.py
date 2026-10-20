"""Angle: you've tried everything to get them off the screen. Here's why nothing worked.

Value first, and honest: screens win because they are short, fast and always
a surprise; most screen-free swaps are long, slow and predictable. So compete
on the same terms, and add the one thing a screen can't: a parent fully
playing. The book is named once as what this family uses, then immediately
followed by free alternatives, so the advice stands on its own.
"""
from __future__ import annotations

from ..doodle import (INK, MARKER, Picture, Shape, Text, arrow, check, circle, curve, ellipse, heart,
                      line, poly, rrect)
from ..explainer import KEEP
from ..figures import bubble, cover, kid
from .reading import BLUE, GOLD, GREEN, GREY, RED, TEAL, W, note, tag
from .school import speech

ID = "screens"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
GLOW = (190, 222, 255)


def tablet(cx, cy, w=200, h=280, lit=True):
    return [Shape(rrect(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2, r=22), width=W,
                  fill=(60, 66, 80), fill_offset=(0, 0)),
            Shape(rrect(cx - w / 2 + 16, cy - h / 2 + 16, cx + w / 2 - 16, cy + h / 2 - 30, r=8),
                  width=4, fill=GLOW if lit else (90, 96, 110), fill_offset=(0, 0))]


def game_box(cx, cy, w=230, h=150):
    x0, y0 = cx - w / 2, cy - h / 2
    return Shape([rrect(x0, y0, x0 + w, y0 + h, r=10), line((x0, y0 + 34), (x0 + w, y0 + 34)),
                  circle(cx, cy + 22, 26, wobble=0.6)], width=W, fill=(255, 238, 200),
                 fill_offset=(0, 0))


def lego(cx, cy):
    return Shape([rrect(cx - 80, cy - 34, cx + 80, cy + 40, r=6),
                  rrect(cx - 62, cy - 56, cx - 26, cy - 34, r=4),
                  rrect(cx - 18, cy - 56, cx + 18, cy - 34, r=4),
                  rrect(cx + 26, cy - 56, cx + 62, cy - 34, r=4)], width=W, fill=(255, 200, 196),
                 fill_offset=(0, 0))


def puzzle(cx, cy, s=70):
    pts = [(cx - s, cy - s), (cx - 18, cy - s), (cx - 22, cy - s - 30), (cx + 22, cy - s - 30),
           (cx + 18, cy - s), (cx + s, cy - s), (cx + s, cy - 18), (cx + s + 30, cy - 22),
           (cx + s + 30, cy + 22), (cx + s, cy + 18), (cx + s, cy + s), (cx - s, cy + s)]
    return Shape(poly(pts, closed=True, wobble=1.2), width=W, fill=(206, 230, 210), fill_offset=(0, 0))


def hourglass(cx, cy, s=60):
    return Shape([poly([(cx - s, cy - s * 1.3), (cx + s, cy - s * 1.3), (cx - s, cy + s * 1.3),
                        (cx + s, cy + s * 1.3)], closed=True, wobble=1.0)], width=W)


def phone(cx, cy):
    return [Shape(rrect(cx - 110, cy - 200, cx + 110, cy + 200, r=30), width=W,
                  fill=(60, 66, 80), fill_offset=(0, 0)),
            Shape(rrect(cx - 92, cy - 170, cx + 92, cy + 160, r=10), width=4, fill=GLOW,
                  fill_offset=(0, 0))]


def octopus(cx, cy, s=1.0):
    fill = (226, 206, 246)
    legs = []
    for k, dx in enumerate((-110, -66, -22, 22, 66, 110)):
        sway = 34 if k % 2 else -34
        legs.append(curve([(cx + dx * 0.6 * s, cy + 70 * s), (cx + dx * s + sway * s, cy + 170 * s),
                           (cx + dx * 1.2 * s, cy + 250 * s)], wobble=1.0))
    return [
        Shape(legs, color=(120, 80, 170), width=12),
        Shape(ellipse(cx, cy, 130 * s, 120 * s), width=W, fill=fill, fill_offset=(0, 0)),
        Shape([circle(cx - 44 * s, cy, 12 * s, wobble=0.3), circle(cx + 44 * s, cy, 12 * s, wobble=0.3)],
              fill=INK, width=4),
    ]


def card(cx, cy):
    return Shape([rrect(cx - 55, cy - 78, cx + 55, cy + 78, r=10), heart(cx, cy, 28)], width=6,
                 fill=(255, 255, 255), fill_offset=(0, 0))


def crossed(cx, cy, r=70):
    return Shape([line((cx - r, cy - r), (cx + r, cy + r)), line((cx + r, cy - r), (cx - r, cy + r))],
                 color=RED, width=12, speed=2.2)


# ------------------------------------------------------------------ boards

def l_hook():
    """Frame one is already the whole problem; the X's land as each is named."""
    return [
        Text("NOTHING WORKS", (540, 330), size=88, face=MARKER, color=RED).ready(),
        *[it.ready() for it in kid(300, 1060, 0.95, "bored", "hold")],
        *[it.ready() for it in tablet(300, 1000, 150, 110)],
        game_box(790, 480).ready(),
        lego(790, 720).ready(),
        puzzle(790, 960, 60).ready(),
        note("board games", (790, 595), size=40, color=GREY).ready(),
        note("Legos", (790, 805), size=40, color=GREY).ready(),
        note("puzzles", (790, 1075), size=40, color=GREY).ready(),
        crossed(790, 480).at("board"),
        crossed(790, 715).at("legos"),
        crossed(790, 960).at("puzzles"),
        Text("?", (520, 600), size=170, face=MARKER, color=GREEN).at("why").focus(1.08).pop(),
    ]


def l_why():
    return [
        tag("lazy?", (300, 330), size=56, color=GREY).at("lazy"),
        Shape(line((210, 335), (390, 325)), color=RED, width=9),
        *phone(290, 640),
        Shape([*arrow((240, 600), (240, 470), head=20), *arrow((340, 700), (340, 570), head=20)],
              color=BLUE, width=7).at("swipe"),
        tag("SHORT", (290, 920), size=62, color=GREEN).at("short").pop(),
        tag("FAST", (290, 1010), size=62, color=GREEN).at("fast").pop(),
        tag("SURPRISE!", (290, 1100), size=62, color=GREEN).at("surprise").focus(1.08).pop(),
    ]


def l_games():
    return [
        game_box(790, 600, w=260, h=170),
        hourglass(790, 330, 40).at("setup"),
        tag("LONG SETUP", (790, 920), size=54, color=GREY),
        tag("WAITING...", (790, 1010), size=54, color=GREY).at("waiting"),
        tag("PREDICTABLE", (790, 1100), size=54, color=GREY).at("know"),
    ]


def l_fix():
    return [
        tag("FIGHT IT WITH:", (540, 340), size=70, color=INK).at("fight"),
        Shape(check(300, 470, 26), color=GREEN, width=11).at("short"),
        note("short", (360, 470), size=66, anchor="lm"),
        Shape(check(300, 570, 26), color=GREEN, width=11).at("fast"),
        note("fast", (360, 570), size=66, anchor="lm"),
        Shape(check(300, 670, 26), color=GREEN, width=11).at("surprising"),
        note("surprising", (360, 670), size=66, anchor="lm"),
    ]


def l_you():
    return [
        *kid(360, 1110, 0.95, "happy", "point"),
        *kid(720, 1140, 0.72, "happy", "up"),
        Shape(heart(540, 830, 50), color=RED, fill=(250, 140, 150), width=7).at("you").focus(1.1),
        tag("+ YOU", (800, 760), size=70, color=TEAL).pop(),
    ]


def l_game():
    reading = speech(420, 500, 240, 86, (330, 790), "Real or fake...?", size=50)
    return [
        *kid(300, 1060, 0.95, "happy", "hold"),
        *reading,
        *kid(780, 1090, 0.75, "think", "chin"),
        bubble(800, 770, 120, 70, (790, 880)).at("guess"),
        Text("?!", (800, 772), size=64, face=MARKER, color=GOLD),
        tag("every answer = a surprise", (540, 330), size=50, color=TEAL).at("surprise").pop(),
    ]


def l_example():
    return [
        Shape(rrect(90, 290, 990, 450, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        note("“Octopuses have three hearts.”", (540, 370), size=58).at("octopuses"),
        *octopus(540, 720, 1.0),
        Shape([heart(400, 560, 34), heart(540, 520, 34), heart(680, 560, 34)], color=RED,
              fill=(250, 130, 140), width=6).at("three"),
        tag("REAL!", (540, 1110), size=120, color=GREEN).at("real").focus(1.12).pop(),
    ]


def l_options():
    return [
        *kid(260, 1040, 0.95, "happy", "hold"),
        Picture(cover(), (260, 985), width=112, angle=-4).at("book"),
        note("Trick Trivia", (300, 650), size=42, color=GREY).at("trick"),
        Shape(arrow((350, 690), (325, 930), bend=-30, head=18), color=GREY, width=6),
        note("anything short & surprising:", (720, 380), size=46, color=INK).at("anything"),
        Text("?", (580, 560), size=130, face=MARKER, color=GOLD).at("riddles"),
        note("riddles", (580, 680), size=44, color=GREY),
        card(760, 560).at("card"),
        note("card tricks", (760, 680), size=44, color=GREY),
        bubble(900, 860, 130, 70, (900, 950)).at("would-you-rather"),
        Text("this or that?", (900, 862), size=34, face=MARKER, color=BLUE),
        note("would you rather", (760, 990), size=44, color=GREY),
    ]


def l_close():
    return [
        *tablet(540, 520, 300, 200, lit=False),
        tag("(screen down)", (540, 680), size=44, color=GREY).at("take"),
        Text("OUT-SURPRISE IT.", (540, 900), size=84, face=MARKER, color=TEAL, max_width=1040)
        .at("out-surprise").focus(1.1).pop(),
    ]


SCRIPT = [
    ("You've tried taking the tablet away. Board games. Legos. Puzzles. Nothing beats the screen. "
     "Here's why.", l_hook),
    ("Screens aren't winning because your kid is lazy. They're winning because every swipe might "
     "be something new. Short, fast, and always a surprise.", l_why),
    ("Most board games are the opposite. Long setup, lots of waiting your turn, and you kind of "
     "know how it ends.", l_games, KEEP),
    ("So don't fight the screen with something slower. Fight it with the same three things: "
     "short, fast, and surprising.", l_fix),
    ("And add the one thing a screen can't: you, fully playing with them.", l_you, KEEP),
    ("One thing that works for us is real-or-fake questions. I read something wild, they guess, "
     "and every answer is a surprise.", l_game),
    ("Like, “Octopuses have three hearts.” Real.", l_example),
    ("We use a book called Trick Trivia, but anything short and surprising works. Riddles, card "
     "tricks, would-you-rather.", l_options),
    ("Next time, don't just take the screen away. Out-surprise it.", l_close),
]

CAPTION = (
    "You've tried taking the tablet away. Board games, Legos, puzzles. Nothing beats the screen. "
    "Here's why: screens aren't winning because your kid is lazy, they're winning because every "
    "swipe might be something new. Short, fast, always a surprise. Most board games are the "
    "opposite. So compete on the same terms (short, fast, surprising) and add the one thing a "
    "screen can't: you, fully playing with them. We use Trick Trivia (it's on Amazon), but "
    "riddles, card tricks and would-you-rather work too. Don't just take the screen away. "
    "Out-surprise it."
)
HASHTAGS = ["#screentime", "#parentingtips", "#momtok", "#dadtok", "#screenfreekids",
            "#kidsactivities", "#realorfake"]
