"""Angle: you've tried everything to get them reading. Here's why it isn't working.

Value first, and honest: for many reluctant readers the problem is the size
of the ask, and assigned reading (with rewards attached) starts to feel like
a job. The fix is to shrink it to something they can finish in a minute and
let them pick. The book is named once as what this family uses, then
immediately followed by free alternatives, and the close is back on the habit.
"""
from __future__ import annotations

from ..doodle import INK, MARKER, Picture, Shape, Text, arrow, circle, curve, ellipse, line, poly, rrect, star
from ..explainer import KEEP
from ..figures import bubble, cover, kid, magnifier, word_box
from .reading import BLUE, GOLD, GREEN, GREY, PALE_GOLD, RED, TEAL, W, note, small_book, tag
from .school import PINK, clock, speech
from .screens import crossed

ID = "readers"
TIGHTEN = 0.2
CHIP = "FOR PARENTS OF KIDS 6–12"
FOOTER = "Trick Trivia: Real or Fake? · by Tom Hadley"
CLAIM = "“A shrimp's heart is in its head.”"
SKY = (200, 222, 250)
MINT = (206, 236, 214)


def book_stack(cx, cy):
    """Three closed books, slightly askew, bottom edge near cy + 75."""
    rows = [(-6, 250, SKY), (10, 220, PINK), (-2, 236, PALE_GOLD)]
    out = []
    for k, (dx, w, fill) in enumerate(rows):
        y = cy + 30 - k * 50
        out.append(Shape([rrect(cx + dx - w / 2, y - 22, cx + dx + w / 2, y + 22, r=6),
                          line((cx + dx - w / 2 + 24, y - 22), (cx + dx - w / 2 + 24, y + 22))],
                         width=7, fill=fill, fill_offset=(0, 0)))
    return out


def sticker_chart(cx, cy):
    x0, y0, x1, y1 = cx - 120, cy - 85, cx + 120, cy + 85
    grid = [line((x0, y0 + 56), (x1, y0 + 56)), line((x0, y0 + 113), (x1, y0 + 113)),
            line((x0 + 80, y0), (x0 + 80, y1)), line((x0 + 160, y0), (x0 + 160, y1))]
    return [Shape([rrect(x0, y0, x1, y1, r=10), *grid], width=6, fill=(255, 255, 255),
                  fill_offset=(0, 0)),
            Shape([star(x0 + 40, y0 + 28, 18, seed=1), star(x0 + 120, y0 + 28, 18, seed=2),
                   star(x0 + 40, y0 + 85, 18, seed=3)], color=GOLD, fill=GOLD, width=4)]


def comic(cx, cy, s=1.0):
    w, h = 200 * s, 200 * s
    x0, y0 = cx - w / 2, cy - h / 2
    return [Shape([rrect(x0, y0, x0 + w, y0 + h, r=8), line((x0, y0 + h * 0.48), (x0 + w, y0 + h * 0.48)),
                   line((cx, y0), (cx, y0 + h * 0.48))], width=7, fill=(255, 255, 255),
                  fill_offset=(0, 0)),
            Shape([circle(x0 + w * 0.25, y0 + h * 0.26, 18 * s, wobble=0.5),
                   circle(x0 + w * 0.75, y0 + h * 0.26, 18 * s, wobble=0.5)], width=5),
            Text("POW!", (cx, y0 + h * 0.74), size=int(52 * s), face=MARKER, color=RED)]


def big_book(cx, cy, w=330, h=600):
    x0, y0 = cx - w / 2, cy - h / 2
    return [Shape([rrect(x0, y0, x0 + w, y0 + h, r=12), line((x0 + 40, y0), (x0 + 40, y0 + h))],
                  width=W, fill=SKY, fill_offset=(0, 0)),
            Shape([line((x0 + w, y0 + 18), (x0 + w + 22, y0 + 34)),
                   line((x0 + w + 22, y0 + 34), (x0 + w + 22, y0 + h + 14)),
                   line((x0 + w + 22, y0 + h + 14), (x0 + 40, y0 + h + 14))], width=6),
            Text("CHAPTER", (cx + 20, y0 + 150), size=46, face=MARKER, color=INK),
            Text("BOOK", (cx + 20, y0 + 210), size=46, face=MARKER, color=INK)]


def baseball_card(cx, cy):
    return [Shape([rrect(cx - 62, cy - 86, cx + 62, cy + 86, r=10),
                   line((cx - 44, cy + 40), (cx + 44, cy + 40)), line((cx - 44, cy + 62), (cx + 20, cy + 62))],
                  width=6, fill=(255, 255, 255), fill_offset=(0, 0)),
            Shape([circle(cx, cy - 22, 36), curve([(cx - 22, cy - 46), (cx - 8, cy - 22), (cx - 22, cy + 2)]),
                   curve([(cx + 22, cy - 46), (cx + 8, cy - 22), (cx + 22, cy + 2)])],
                  color=RED, width=5)]


# ------------------------------------------------------------------ boards

def l_hook():
    """Frame one is already the whole problem; the X's land as each is named."""
    return [
        Text("STILL WON'T READ", (540, 330), size=84, face=MARKER, color=RED).ready(),
        *[it.ready() for it in kid(290, 1060, 0.95, "bored", "down")],
        *[it.ready() for it in book_stack(790, 520)],
        *[it.ready() for it in clock(790, 775, 72)],
        *[it.ready() for it in sticker_chart(790, 1020)],
        note("new books", (790, 625), size=40, color=GREY).ready(),
        note("reading time", (790, 885), size=40, color=GREY).ready(),
        note("rewards", (790, 1135), size=40, color=GREY).ready(),
        crossed(790, 505).at("books"),
        crossed(790, 775).at("reading"),
        crossed(790, 1020).at("rewards"),
        Text("?", (300, 640), size=170, face=MARKER, color=GREEN).at("why").focus(1.08).pop(),
    ]


def l_ask():
    return [
        tag("not the reading...", (540, 330), size=56, color=GREY).at("isn't"),
        tag("the SIZE of the ask", (540, 420), size=64, color=RED).at("size").pop(),
        *kid(250, 1000, 0.7, "shock", "up"),
        *big_book(690, 790),
        note("300 pages before anything good?", (540, 1220), size=46, color=INK,
             max_width=980).at("good").focus(1.06),
    ]


def l_chore():
    x0, y0 = 110, 450
    return [
        Shape([rrect(x0, y0, x0 + 440, y0 + 560, r=16)], width=W, fill=(255, 255, 255),
              fill_offset=(0, 0)),
        Shape(rrect(x0 + 150, y0 - 24, x0 + 290, y0 + 26, r=10), width=7, fill=GREY, fill_offset=(0, 0)),
        tag("CHORES", (x0 + 220, y0 + 90), size=52, color=INK),
        *[Shape(rrect(x0 + 40, y0 + 160 + k * 110, x0 + 90, y0 + 210 + k * 110, r=6), width=6)
          for k in range(3)],
        Shape(line((x0 + 50, y0 + 185), (x0 + 80, y0 + 200)), color=GREEN, width=8),
        note("dishes", (x0 + 120, y0 + 185), size=48, anchor="lm"),
        note("trash", (x0 + 120, y0 + 295), size=48, anchor="lm"),
        note("read 20 min", (x0 + 120, y0 + 405), size=48, anchor="lm", color=RED).at("chore"),
        Shape(ellipse(x0 + 240, y0 + 405, 200, 50, sweep=400), color=RED, width=7),
        Shape(star(800, 590, 70, seed=4), color=GOLD, fill=GOLD, width=6).at("rewards"),
        note("works for a day...", (800, 720), size=46, color=GREY).at("day"),
        Shape(arrow((800, 770), (800, 920), head=22), color=GREY, width=7).at("turn"),
        tag("= A JOB", (800, 1000), size=84, color=RED).at("job").focus(1.1).pop(),
    ]


def l_shrink():
    joke = speech(220, 920, 150, 80, (180, 1040), "Knock knock!", size=40)
    joke[0].at("joke")
    sentence = Shape(rrect(700, 850, 1010, 990, r=14), width=W, fill=PALE_GOLD, fill_offset=(0, 0))
    sentence.at("sentence")
    return [
        tag("SHRINK IT.", (540, 340), size=96, color=TEAL).at("shrink").focus(1.08).pop(),
        *clock(540, 590, 100),
        tag("1 MINUTE", (540, 740), size=56, color=RED).at("minute").pop(),
        *joke,
        *[c.at("comic") if k == 0 else c for k, c in enumerate(comic(540, 930, 0.9))],
        sentence,
        note("one wild sentence!", (855, 920), size=38, max_width=290),
        note("joke", (220, 1110), size=42, color=GREY),
        note("comic", (540, 1110), size=42, color=GREY),
        note("sentence", (855, 1110), size=42, color=GREY),
    ]


def l_choose():
    mine = small_book(230, 520, 230, 140)
    theirs = comic(820, 500, 1.0)
    return [
        *mine,
        note("your pick", (230, 650), size=46, color=GREY),
        *theirs,
        *kid(560, 1040, 0.9, "happy", "point"),
        tag("THEIR PICK", (820, 680), size=60, color=TEAL).at("their").focus(1.08).pop(),
        Shape(arrow((650, 840), (820, 740), bend=-20, head=22), color=TEAL, width=W),
        note("(even if it's not yours)", (540, 1260), size=44, color=GREY).at("you'd"),
    ]


def l_game():
    box = word_box(CLAIM, 56)
    hx, hw = box["head"]
    return [
        Shape(rrect(70, 300, 1010, 450, r=26), width=W, fill=(255, 255, 255), fill_offset=(0, 0)),
        note(CLAIM, (540, 375), size=56).at("real-or-fake"),
        tag("REAL OR FAKE?", (540, 540), size=64, color=GOLD).pop(),
        tag("one sentence", (300, 660), size=50, color=TEAL).at("sentence"),
        *magnifier(hx, 380, hw * 0.62, angle=60),
        *kid(720, 1050, 0.9, "think", "chin"),
        tag("read it closely", (300, 760), size=50, color=TEAL).at("closely").pop(),
        bubble(380, 950, 170, 80, (640, 900)).at("catch"),
        Text("the trick?", (380, 952), size=48, face=MARKER, color=RED),
    ]


def l_options():
    return [
        *kid(250, 1040, 0.95, "happy", "hold"),
        Picture(cover(), (250, 985), width=112, angle=-4).at("book"),
        note("Trick Trivia", (290, 650), size=42, color=GREY).at("trick"),
        Shape(arrow((340, 690), (315, 930), bend=-30, head=18), color=GREY, width=6),
        *small_book(770, 420, 210, 120),
        Text("HA!", (770, 325), size=44, face=MARKER, color=GOLD).at("joke"),
        note("joke books", (770, 530), size=42, color=GREY),
        *comic(660, 750, 0.75),
        note("comics", (660, 870), size=42, color=GREY).at("comics"),
        *baseball_card(880, 760),
        note("sports stats", (860, 880), size=42, color=GREY).at("sports"),
        tag("all count!", (760, 1040), size=56, color=TEAL).at("work").pop(),
    ]


def l_close():
    pot = Shape(poly([(450, 1010), (630, 1010), (600, 1150), (480, 1150)], closed=True, wobble=1.0),
                width=W, fill=(240, 190, 150), fill_offset=(0, 0))
    stem = Shape([curve([(540, 1010), (520, 860), (550, 700), (540, 560)], wobble=0.8),
                  curve([(536, 820), (470, 760), (420, 700)], wobble=0.8),
                  curve([(546, 760), (610, 700), (660, 650)], wobble=0.8)], color=GREEN, width=10)
    leaves = Shape([ellipse(600, 900, 46, 22), ellipse(480, 930, 46, 22)], color=GREEN,
                   fill=MINT, width=6, fill_offset=(0, 0))
    return [
        tag("START SMALL.", (540, 340), size=88, color=TEAL).at("start").focus(1.08).pop(),
        note("let them choose", (540, 430), size=50, color=GREY).at("choose"),
        pot, stem.at("grows"), leaves,
        *[b for xy in ((420, 650), (660, 600), (540, 520)) for b in small_book(*xy, 140, 86)],
        Shape([star(330, 560, 16, seed=7), star(760, 520, 16, seed=8)], color=GOLD, fill=GOLD, width=4),
    ]


SCRIPT = [
    ("You've bought the books. Set reading time. Even offered rewards. They still won't read. "
     "Here's why.", l_hook),
    ("For a lot of kids, the problem isn't reading. It's the size of the ask. A whole chapter "
     "book is a lot of work before anything good happens.", l_ask),
    ("And when reading is assigned, it feels like a chore. Rewards help for a day, but they can "
     "turn reading into a job.", l_chore),
    ("So shrink it. Start with something they can finish in one minute. A joke. A comic. One "
     "wild sentence.", l_shrink),
    ("And let them choose. Kids read more when it's their pick, even if it's not what you'd "
     "pick.", l_choose),
    ("One thing that works for us is real-or-fake questions. It's one sentence, and they have "
     "to read it closely to catch the trick.", l_game),
    ("We use a book called Trick Trivia, but joke books, comics and sports stats work too.",
     l_options),
    ("Start small, let them choose, and the reading grows from there.", l_close),
]

CAPTION = (
    "You've bought the books, set reading time, even offered rewards, and they still won't "
    "read. For a lot of kids the problem isn't reading, it's the size of the ask: a whole "
    "chapter book is a lot of work before anything good happens. And assigned reading with "
    "rewards attached starts to feel like a job. So shrink it: something they can finish in a "
    "minute (a joke, a comic, one wild sentence), and let them pick. We use Trick Trivia (it's "
    "on Amazon), but joke books, comics and sports stats work too. Start small, let them "
    "choose, and the reading grows from there."
)
HASHTAGS = ["#readingtips", "#reluctantreader", "#parentingtips", "#momtok", "#dadtok",
            "#kidsbooks", "#realorfake"]
