"""Compose a TikTok Photo Mode carousel from a page pair.

The sequence is a story, not a slideshow of the page:

  1  COVER    one line, one image, nothing else. It is a thumbnail; its
              only job is the first swipe.
  2-4 CLAIMS  the game, one claim per slide, each nudging the next swipe.
  5-7 REVEALS the payoff. The last one asks for a comment.
  8  TURN     the product appears: cover on a fan of real pages, and the
              three numbers that define it.
  9  PROOF    reviews, then the one action to take.

Layout rules from the research in the README: 1080x1920; critical text
centre-middle and clear of TikTok's UI (bottom 350px, right 64px); the
visual hook and the text hook on the cover must say the same thing; each
slide closes the loop the last one opened and opens the next.
"""
from __future__ import annotations

import os

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import brand
from .scenes import (TITLE_GAP, W, H, _auto_font, _fit_width,
                     _paste_with_shadow, tiled_background)

UI_BOTTOM = 350     # TikTok caption, handle and sound bar
UI_RIGHT = 64       # like / comment / share rail
SAFE_W = W - brand.SAFE_SIDE - UI_RIGHT - 24
CENTRE_X = (W - UI_RIGHT) // 2


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


def _block(draw, y, text, size, fill=(255, 255, 255), max_lines=2,
           stroke=12, gap=14, min_size=48):
    """Wrapped display text, shrunk until it fits `max_lines`. Returns bottom y."""
    font = ImageFont.truetype(brand.FONT_BOLD, size)
    lines = _wrap(draw, text, font, SAFE_W)
    while len(lines) > max_lines and size > min_size:
        size -= 6
        font = ImageFont.truetype(brand.FONT_BOLD, size)
        lines = _wrap(draw, text, font, SAFE_W)
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text((CENTRE_X - w / 2, y), line, font=font, fill=fill,
                  stroke_width=stroke, stroke_fill=brand.INK)
        y += font.size + gap
    return y


def _chip(draw, y, text, fill=brand.YELLOW, size=44):
    font = _auto_font(draw, text, size, SAFE_W)
    tw = draw.textlength(text, font=font)
    pad_x, pad_y = 36, 18
    height = font.size + pad_y * 2
    x0 = CENTRE_X - (tw + pad_x * 2) / 2
    draw.rounded_rectangle((x0, y, x0 + tw + pad_x * 2, y + height),
                           radius=height // 2, fill=fill,
                           outline=brand.INK, width=5)
    draw.text((x0 + pad_x, y + pad_y - 4), text, font=font, fill=brand.INK)
    return y + height


def _rounded(img: Image.Image, radius: int) -> Image.Image:
    mask = Image.new("L", img.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, *img.size), radius=radius, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out


def panel_art(panel: Image.Image, fraction: float = 0.46) -> Image.Image:
    """The illustration alone: the left part of a panel, before the bubble."""
    w, h = panel.size
    inset = 14
    return panel.crop((inset, inset, int(w * fraction), h - inset))


# --------------------------------------------------------------------------
# slides


def cover_slide(swatch, title, art, hook, chip):
    """One line, one image. The text hook and the visual hook agree."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    frame.paste(_fit_width(title, W), (0, 0))
    y = round(title.size[1] * W / title.size[0]) + 40

    y = _block(draw, y, hook, 124, max_lines=2, stroke=14, gap=6) + 30

    # Hero illustration, as large as the remaining band allows.
    limit = H - UI_BOTTOM - 130
    avail_h = limit - y
    art_w = min(SAFE_W, int(art.size[0] * avail_h / art.size[1]))
    hero = _rounded(_fit_width(art, art_w), 36)
    x = CENTRE_X - hero.size[0] // 2
    _paste_with_shadow(frame, hero.convert("RGB"), (x, y))
    frame.paste(hero, (x, y), hero)

    _chip(draw, H - UI_BOTTOM - 96, chip, size=48)
    return frame


def claim_slide(swatch, title, panel, chip=None, kicker=None, panel_width=1044):
    """A claim or reveal: lockup, kicker, hero panel, nudge."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    frame.paste(_fit_width(title, W), (0, 0))
    y = round(title.size[1] * W / title.size[0]) + TITLE_GAP + 10

    panel_img = _fit_width(panel, panel_width)
    limit = H - UI_BOTTOM - 40
    if kicker:
        y = _block(draw, y + 10, kicker, 72, max_lines=2) + 20
    stack = panel_img.size[1] + (110 if chip else 0)
    y += max(0, (limit - y - stack) // 2)
    _paste_with_shadow(frame, panel_img, ((W - panel_width) // 2, y))
    y += panel_img.size[1] + 40
    if chip:
        _chip(draw, y, chip)
    return frame


def page_fan(pages_imgs, width=470, spread=8, offset=30):
    """A fanned stack of real pages -- the interior, shown as volume."""
    if not pages_imgs:
        return None
    seq = (pages_imgs * 6)[:6]
    thumbs = [_fit_width(p, width) for p in seq]
    ph = thumbs[0].size[1]
    pad = 130
    canvas = Image.new("RGBA", (width + pad * 2 + offset * 6, ph + pad * 2), (0, 0, 0, 0))
    n = len(thumbs)
    for i, thumb in enumerate(thumbs):
        angle = -spread * (n - 1) / 2 + spread * i
        shadow = Image.new("RGBA", thumb.size, (0, 0, 0, 110))
        shadow = shadow.rotate(angle, expand=True, resample=Image.BICUBIC)
        page = thumb.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC)
        x = pad + i * offset + (width - page.size[0]) // 2
        y = pad + (ph - page.size[1]) // 2
        layer = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
        layer.paste(shadow, (x + 6, y + 14), shadow)
        canvas.alpha_composite(layer.filter(ImageFilter.GaussianBlur(10)))
        canvas.alpha_composite(page, (x, y))
    return canvas


def turn_slide(swatch, headline, interior, cover, stats):
    """The product appears: cover on a fan of real pages, three numbers."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    y = _block(draw, 110, headline, 96, max_lines=2) + 10

    fan = page_fan(interior or [])
    if fan is not None:
        fx = CENTRE_X - fan.size[0] // 2
        frame.paste(fan, (fx, y - 70), fan)
        body_bottom = y - 70 + fan.size[1] - 110
    else:
        body_bottom = y
    if cover is not None:
        art = _fit_width(cover, 500)
        cy = y + 20
        _paste_with_shadow(frame, art, (CENTRE_X - 250, cy))
        body_bottom = max(body_bottom, cy + art.size[1])

    # Three stats in a row, above the UI zone.
    font = ImageFont.truetype(brand.FONT_BOLD, 44)
    y = H - UI_BOTTOM - 110
    widths = [draw.textlength(s, font=font) + 64 for s in stats]
    gap = 22
    x = CENTRE_X - (sum(widths) + gap * (len(stats) - 1)) / 2
    for stat, w in zip(stats, widths):
        draw.rounded_rectangle((x, y, x + w, y + 84), radius=42,
                               fill=brand.YELLOW, outline=brand.INK, width=5)
        draw.text((x + 32, y + 16), stat, font=font, fill=brand.INK)
        x += w + gap
    return frame


def proof_slide(swatch, headline, reviews, cta):
    """Reviews, then the one action to take."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    y = _block(draw, 120, headline, 92, max_lines=2) + 30

    star_font = ImageFont.truetype(brand.FONT_BOLD, 40)
    quote_font = ImageFont.truetype(brand.FONT_BOLD, 40)
    box_w = SAFE_W
    x0 = CENTRE_X - box_w / 2
    for review in reviews[:3]:
        lines = _wrap(draw, f"“{review['quote']}”", quote_font, box_w - 60)[:3]
        box_h = 34 + star_font.size + 12 + len(lines) * (quote_font.size + 8) + 28
        if y + box_h > H - UI_BOTTOM - 150:
            break
        draw.rounded_rectangle((x0, y, x0 + box_w, y + box_h), radius=24,
                               fill=brand.PAPER, outline=brand.INK, width=5)
        draw.text((x0 + 30, y + 26), "★" * 5, font=star_font, fill=(255, 160, 0))
        name = review.get("name", "")
        if name:
            nw = draw.textlength(name, font=star_font)
            draw.text((x0 + box_w - 30 - nw, y + 26), name, font=star_font, fill=brand.INK)
        ty = y + 34 + star_font.size + 12
        for line in lines:
            draw.text((x0 + 30, ty), line, font=quote_font, fill=brand.INK)
            ty += quote_font.size + 8
        y += box_h + 22

    if not reviews:
        band_top, band_bottom = y, H - UI_BOTTOM - 150
        block_h = 110 + 6 + 56 * 2 + 14
        y = band_top + max(0, (band_bottom - band_top - block_h) // 2)
        y = _block(draw, y, "★★★★★", 110, fill=brand.YELLOW) + 6
        _block(draw, y, "Hundreds of 5-star reviews on Amazon", 56)

    _chip(draw, H - UI_BOTTOM - 96, cta, size=48)
    return frame


def export(frames: list[Image.Image], out_dir: str, quality: int = 88) -> list[str]:
    """Write slides as JPEGs, in swipe order."""
    os.makedirs(out_dir, exist_ok=True)
    paths = []
    for i, frame in enumerate(frames, start=1):
        path = os.path.join(out_dir, f"slide-{i:02d}.jpg")
        frame.convert("RGB").save(path, "JPEG", quality=quality, optimize=True)
        paths.append(path)
    return paths
