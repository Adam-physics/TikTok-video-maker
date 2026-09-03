"""Draw stand-in book pages that match the real page geometry.

The real pages are 3 bordered cards on a halftone ground, title lockup on
top. These fakes copy that layout so panel detection, composition, timing
and audio can all be validated before the real artwork is in the repo.
Delete this once assets/pages holds real scans -- it proves the pipeline,
it is not part of it.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from trivia import brand  # noqa: E402

PAGE = (1320, 2000)
CARD_X = (85, 1235)
CARDS = [(480, 920), (960, 1400), (1430, 1870)]

QUESTIONS = [
    ("A group of flamingos is called a flamboyance.", (196, 118, 168)),
    ("Polar bears have white fur.", (150, 196, 226)),
    ("Octopuses have three hearts and blue blood.", (120, 84, 176)),
]
ANSWERS = [
    ("REAL!", brand.GREEN, "Officially a flamboyance. Scientists named it."),
    ("FAKE!", brand.RED, "Polar bear fur is transparent and hollow."),
    ("REAL!", brand.GREEN, "Two hearts feed the gills, one feeds the body."),
]


def halftone(size, base, dot):
    img = Image.new("RGB", size, base)
    d = ImageDraw.Draw(img)
    for y in range(0, size[1], 14):
        for x in range((y // 14 % 2) * 7, size[0], 14):
            d.ellipse((x, y, x + 4, y + 4), fill=dot)
    return img


def wrap(draw, text, font, width):
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if draw.textlength(trial, font=font) <= width:
            line = trial
        else:
            lines.append(line)
            line = w
    if line:
        lines.append(line)
    return lines


def card(draw, box, art_colour, text, font, tail=None, tail_colour=None):
    l, t, r, b = box
    draw.rounded_rectangle((l, t, r, b), radius=30, fill=(252, 250, 244),
                           outline=brand.INK, width=9)
    art_w = int((r - l) * 0.44)
    draw.rounded_rectangle((l + 14, t + 14, l + art_w, b - 14), radius=22,
                           fill=art_colour)
    tx = l + art_w + 34
    lines = wrap(draw, text, font, r - tx - 30)
    y = t + 34
    if tail:
        draw.text((tx, y), tail, font=font, fill=tail_colour)
        y += 62
    for line in lines:
        draw.text((tx, y), line, font=font, fill=brand.INK)
        y += 46


def buttons(draw, box, font):
    l, t, r, b = box
    y = b - 96
    for label, colour, x in (("REAL", brand.GREEN, r - 470),
                             ("FAKE", brand.RED, r - 240)):
        draw.rounded_rectangle((x, y, x + 200, y + 74), radius=14,
                               fill=colour, outline=brand.INK, width=5)
        w = draw.textlength(label, font=font)
        draw.text((x + (200 - w) / 2, y + 18), label, font=font,
                  fill=(255, 255, 255))


def build(path, question_side):
    base = brand.ORANGE if question_side else brand.BLUE
    dot = brand.ORANGE_DEEP if question_side else brand.BLUE_DEEP
    img = halftone(PAGE, base, dot)
    draw = ImageDraw.Draw(img)
    title = ImageFont.truetype(brand.FONT_BOLD, 96)
    body = ImageFont.truetype(brand.FONT_BOLD, 38)
    small = ImageFont.truetype(brand.FONT_BOLD, 34)

    head = "TRICK TRIVIA!" if question_side else "THE TRUTH REVEALED!"
    w = draw.textlength(head, font=title)
    draw.text(((PAGE[0] - w) / 2, 150), head, font=title, fill=(255, 255, 255),
              stroke_width=10, stroke_fill=brand.INK)

    for i, (top, bottom) in enumerate(CARDS):
        box = (CARD_X[0], top, CARD_X[1], bottom)
        if question_side:
            text, colour = QUESTIONS[i]
            card(draw, box, colour, text, body)
            buttons(draw, box, small)
        else:
            stamp, stamp_colour, text = ANSWERS[i]
            card(draw, box, QUESTIONS[i][1], text, body, stamp, stamp_colour)
    img.save(path)
    return path


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "assets", "pages")
    os.makedirs(out, exist_ok=True)
    print(build(os.path.join(out, "test-q01.png"), True))
    print(build(os.path.join(out, "test-a01.png"), False))
