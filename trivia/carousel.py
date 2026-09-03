"""Compose a TikTok Photo Mode carousel from a page pair.

Why carousels: the algorithm scores them on swipe-through, saves and
completion rather than watch time, and every swipe is an active signal.
A real-or-fake page is already a swipe structure -- claim, swipe, reveal.

Layout rules baked in here, from the research in the README:

- 1080x1920, critical text centre-middle, nothing that must be read in the
  bottom 350px or right 64px where TikTok's UI sits.
- Slide 1 is the thumbnail. Kallaway's ordering -- visual hook first, text
  hook second, spoken hook a distant third -- means a carousel is the
  purest form: there is no spoken hook, so the picture and the on-screen
  line carry everything, and they must say the same thing.
- Every slide closes the loop the last one opened and opens a new one.
  A "swipe" nudge on early slides measurably lifts swipe-through.
- Five to seven slides. Engagement falls off after seven.
- The last slide drives an action (a comment, a profile visit) because
  completion plus a comment is the strongest pair of signals a post gets.
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import brand
from .scenes import (BAND_BOTTOM, TITLE_GAP, W, H, _auto_font, _fit_width,
                     _paste_with_shadow, tiled_background)

UI_BOTTOM = 350     # TikTok caption, handle and sound bar
UI_RIGHT = 64       # like / comment / share rail
SAFE_W = W - brand.SAFE_SIDE - UI_RIGHT - 24


def _wrap(draw, text, font, max_width):
    words, lines, line = text.split(), [], ""
    for word in words:
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= max_width:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def _hook_block(draw, y, text, size=96, fill=(255, 255, 255)):
    """Big on-screen hook, wrapped to at most two lines, stroked for contrast."""
    font = ImageFont.truetype(brand.FONT_BOLD, size)
    lines = _wrap(draw, text, font, SAFE_W)
    while len(lines) > 2 and size > 56:
        size -= 6
        font = ImageFont.truetype(brand.FONT_BOLD, size)
        lines = _wrap(draw, text, font, SAFE_W)
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((W - UI_RIGHT - w) / 2, y), line, font=font, fill=fill,
                  stroke_width=12, stroke_fill=brand.INK)
        y += font.size + 14
    return y


def _chip(draw, y, text, fill=brand.YELLOW, size=44):
    font = _auto_font(draw, text, size, SAFE_W)
    tw = draw.textlength(text, font=font)
    pad_x, pad_y = 36, 18
    height = font.size + pad_y * 2
    x0 = (W - UI_RIGHT - (tw + pad_x * 2)) / 2
    draw.rounded_rectangle((x0, y, x0 + tw + pad_x * 2, y + height),
                           radius=height // 2, fill=fill,
                           outline=brand.INK, width=5)
    draw.text((x0 + pad_x, y + pad_y - 4), text, font=font, fill=brand.INK)
    return y + height


def claim_slide(swatch, title, panel, hook=None, chip=None, panel_width=1044):
    """A claim or reveal slide: lockup, optional hook, hero panel, nudge."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    frame.paste(_fit_width(title, W), (0, 0))
    y = round(title.size[1] * W / title.size[0]) + TITLE_GAP + 10

    panel_img = _fit_width(panel, panel_width)
    limit = H - UI_BOTTOM - 40
    # Hook sits above the panel so it is read first; the panel is the
    # visual hook and the line on top of it is the text hook.
    if hook:
        y = _hook_block(draw, y + 20, hook) + 30
    # Centre the panel (and chip) in what is left.
    stack = panel_img.size[1] + (110 if chip else 0)
    y += max(0, (limit - y - stack) // 2)
    _paste_with_shadow(frame, panel_img, ((W - panel_width) // 2, y))
    y += panel_img.size[1] + 40
    if chip:
        _chip(draw, y, chip)
    return frame


def page_fan(pages_imgs, width=520, spread=9, offset=26):
    """A fanned stack of real pages -- the interior, shown as volume.

    Each page is rotated a little more than the last and shifted right, so
    the stack reads as a thick book rather than one flat sheet. Pages
    repeat if fewer than five are supplied.
    """
    if not pages_imgs:
        return None
    seq = (pages_imgs * 5)[:5]
    thumbs = [_fit_width(p, width) for p in seq]
    ph = thumbs[0].size[1]
    pad = 140
    canvas = Image.new("RGBA", (width + pad * 2 + offset * 5, ph + pad * 2), (0, 0, 0, 0))
    n = len(thumbs)
    for i, thumb in enumerate(thumbs):
        angle = -spread * (n - 1) / 2 + spread * i
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        shadow = Image.new("RGBA", thumb.size, (0, 0, 0, 120))
        shadow = shadow.rotate(angle, expand=True, resample=Image.BICUBIC)
        page = thumb.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
        x = pad + i * offset + (width - page.size[0]) // 2
        y = pad + (ph - page.size[1]) // 2
        layer.paste(shadow, (x + 6, y + 14), shadow)
        layer = layer.filter(ImageFilter.GaussianBlur(10))
        canvas.alpha_composite(layer)
        canvas.alpha_composite(page, (x, y))
    return canvas


def cta_slide(swatch, cover, headline, reviews, cta, interior=None):
    """The close: volume, proof, action. Nothing here is a feature list.

    `interior` is a list of page images. They are fanned behind the cover
    (or in its place) so the slide shows the inside of the book even before
    a cover file exists.
    """
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    y = 120
    y = _hook_block(draw, y, headline, size=88) + 10

    fan = page_fan(interior or [])
    if fan is not None:
        fx = (W - UI_RIGHT - fan.size[0]) // 2
        frame.paste(fan, (fx, y - 60), fan)
        y += fan.size[1] - 150
    if cover is not None:
        art = _fit_width(cover, 520)
        cy = y - (fan.size[1] // 2 + 40 if fan is not None else 0)
        _paste_with_shadow(frame, art, ((W - UI_RIGHT - 520) // 2, cy))
        y = cy + art.size[1] + 44

    star_font = ImageFont.truetype(brand.FONT_BOLD, 40)
    quote_font = ImageFont.truetype(brand.FONT_BOLD, 38)
    for review in reviews[:3]:
        box_w = SAFE_W
        x0 = (W - UI_RIGHT - box_w) / 2
        lines = _wrap(draw, f"“{review['quote']}”", quote_font, box_w - 60)[:2]
        box_h = 34 + star_font.size + 10 + len(lines) * (quote_font.size + 8) + 26
        if y + box_h > H - UI_BOTTOM - 120:
            break
        draw.rounded_rectangle((x0, y, x0 + box_w, y + box_h), radius=24,
                               fill=brand.PAPER, outline=brand.INK, width=5)
        stars = "★" * 5
        draw.text((x0 + 30, y + 26), stars, font=star_font, fill=(255, 160, 0))
        name = review.get("name", "")
        if name:
            nw = draw.textlength(name, font=star_font)
            draw.text((x0 + box_w - 30 - nw, y + 26), name, font=star_font,
                      fill=brand.INK)
        ty = y + 34 + star_font.size + 10
        for line in lines:
            draw.text((x0 + 30, ty), line, font=quote_font, fill=brand.INK)
            ty += quote_font.size + 8
        y += box_h + 22

    _chip(draw, H - UI_BOTTOM - 100, cta, size=46)
    return frame


def export(frames: list[Image.Image], out_dir: str, quality: int = 88) -> list[str]:
    """Write slides as JPEGs, in swipe order, sized for fast loading."""
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, frame in enumerate(frames, start=1):
        path = os.path.join(out_dir, f"slide-{i:02d}.jpg")
        frame.convert("RGB").save(path, "JPEG", quality=quality, optimize=True)
        paths.append(path)
    return paths
