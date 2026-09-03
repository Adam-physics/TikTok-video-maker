"""Compose 1080x1920 still frames from cropped book panels.

One scene per beat of the round. Motion, timing and sound are added later
in render.py -- these are just the frames. The background, the title lockup
and the panels all come out of the printed page, so a finished frame is
recognisably the book rather than a design that merely references it.

Two layout rules hold everywhere. Text is shrunk until it fits inside the
side margins, because a clipped word is worse than a small one. And the
block below the guess timer is centred in whatever space is left, so a
tall answer panel and a short claim panel both sit balanced without
per-page tuning.
"""
from __future__ import annotations

from PIL import Image, ImageDraw, ImageFilter, ImageFont

from . import brand

W, H = brand.WIDTH, brand.HEIGHT
TEXT_WIDTH = W - brand.SAFE_SIDE * 2

# The readable band, once TikTok's own chrome is discounted.
BAND_TOP = brand.SAFE_TOP
BAND_BOTTOM = H - brand.SAFE_BOTTOM

TITLE_GAP = 26      # between the lockup and the guess timer

# Vertical rhythm below the panel.
GAP_PANEL = 46
GAP_TEXT = 30


def tiled_background(swatch: Image.Image) -> Image.Image:
    """Fill the canvas with the page's own halftone ground."""
    bg = Image.new("RGB", (W, H))
    sw, sh = swatch.size
    for y in range(0, H, sh):
        for x in range(0, W, sw):
            bg.paste(swatch, (x, y))
    return bg


def _fit_width(img: Image.Image, width: int) -> Image.Image:
    scale = width / img.size[0]
    return img.resize((width, max(1, round(img.size[1] * scale))), Image.LANCZOS)


def _auto_font(draw, text: str, size: int, max_width: int = TEXT_WIDTH):
    """Largest bold face at or below `size` that keeps `text` inside the margins."""
    while size > 22:
        font = ImageFont.truetype(brand.FONT_BOLD, size)
        if draw.textlength(text, font=font) <= max_width:
            return font
        size -= 4
    return ImageFont.truetype(brand.FONT_BOLD, 22)


def _paste_with_shadow(base: Image.Image, art: Image.Image, xy: tuple[int, int]) -> None:
    """Drop the panel onto the ground with a soft shadow so it lifts off it."""
    x, y = xy
    pad = brand.PANEL_SHADOW * 3
    shadow = Image.new("RGBA", (art.size[0] + pad * 2, art.size[1] + pad * 2), (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (pad, pad + 8, pad + art.size[0], pad + art.size[1] + 8),
        radius=brand.PANEL_RADIUS, fill=(0, 0, 0, 130))
    shadow = shadow.filter(ImageFilter.GaussianBlur(brand.PANEL_SHADOW))
    base.paste(shadow, (x - pad, y - pad), shadow)
    base.paste(art, (x, y))


def _shout(draw, y, text, size, fill, stroke=10):
    font = _auto_font(draw, text, size)
    w = draw.textlength(text, font=font)
    draw.text(((W - w) / 2, y), text, font=font, fill=fill,
              stroke_width=stroke, stroke_fill=brand.INK)
    return font.size


def _pill(draw, y, text, size, fill):
    """A rounded chip -- used for the round counter."""
    font = _auto_font(draw, text, size)
    tw = draw.textlength(text, font=font)
    pad_x, pad_y = 34, 16
    height = font.size + pad_y * 2
    x0 = (W - (tw + pad_x * 2)) / 2
    draw.rounded_rectangle((x0, y, x0 + tw + pad_x * 2, y + height),
                           radius=height // 2, fill=fill,
                           outline=brand.INK, width=5)
    draw.text((x0 + pad_x, y + pad_y - 4), text, font=font, fill=brand.INK)
    return height


def timer_box(title, title_width: int = W) -> tuple[int, int, int, int]:
    """Where the guess timer sits, as (x, y, width, height).

    Claim and reveal pages crop to lockups of different heights, so the
    timer is placed under whichever one this scene uses rather than at a
    fixed offset. render.py animates the fill using the same box.
    """
    height = round(title.size[1] * title_width / title.size[0])
    return brand.TIMER_X, height + TITLE_GAP, brand.TIMER_W, brand.TIMER_H


def panel_scene(swatch, title, panel, counter=None, prompt=None, timer=False,
                title_width=W, panel_width=1044):
    """A claim or reveal frame: title lockup, hero panel, counter, nudge."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)

    # Flush to the top edge and full width, so the lockup's own halftone
    # bleeds off the frame instead of showing as a pasted rectangle.
    frame.paste(_fit_width(title, title_width), ((W - title_width) // 2, 0))

    x, y, tw, th = timer_box(title, title_width)
    header_bottom = y + th + 40
    # The timer itself -- groove and fill both -- is drawn by render.py as
    # an overlay, so the scene's slow push cannot drift one from the other.

    panel_img = _fit_width(panel, panel_width)
    counter_font = _auto_font(draw, counter or "", 44) if counter else None
    prompt_font = _auto_font(draw, prompt or "", 56) if prompt else None

    # Centre panel + counter + nudge in the space the header leaves behind.
    pill_height = counter_font.size + 32 if counter_font else 0
    stack = panel_img.size[1]
    if counter_font:
        stack += GAP_PANEL + pill_height
    if prompt_font:
        stack += GAP_TEXT + prompt_font.size
    y = header_bottom + max(0, (BAND_BOTTOM - header_bottom - stack) // 2)

    _paste_with_shadow(frame, panel_img, ((W - panel_width) // 2, y))
    y += panel_img.size[1]
    if counter:
        y += GAP_PANEL
        y += _pill(draw, y, counter, 44, brand.YELLOW)
    if prompt:
        y += GAP_TEXT
        _shout(draw, y, prompt, 56, (255, 255, 255))
    return frame


def shout_scene(swatch, lines, colour=(255, 255, 255)):
    """A full-bleed text beat -- the guess lock and other pauses."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)
    fonts = [_auto_font(draw, line, 116) for line in lines]
    total = sum(f.size for f in fonts) + 26 * (len(lines) - 1)
    y = (H - total) / 2
    for line, font in zip(lines, fonts):
        w = draw.textlength(line, font=font)
        draw.text(((W - w) / 2, y), line, font=font, fill=colour,
                  stroke_width=12, stroke_fill=brand.INK)
        y += font.size + 26
    return frame


def end_card(swatch, cover: Image.Image | None, headline, subline):
    """The diegetic close: the book as the answer key, not as an advert."""
    frame = tiled_background(swatch)
    draw = ImageDraw.Draw(frame)

    head_font = _auto_font(draw, headline, 88)
    sub_font = _auto_font(draw, subline, 62)
    art = _fit_width(cover, 620) if cover is not None else None

    stack = head_font.size + 48 + sub_font.size
    if art is not None:
        stack += art.size[1] + 48
    y = BAND_TOP + max(0, (BAND_BOTTOM - BAND_TOP - stack) // 2)

    y += _shout(draw, y, headline, 88, (255, 255, 255)) + 48
    if art is not None:
        _paste_with_shadow(frame, art, ((W - 620) // 2, y))
        y += art.size[1] + 48
    _shout(draw, y, subline, 62, brand.YELLOW)
    return frame
