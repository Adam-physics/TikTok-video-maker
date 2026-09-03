#!/usr/bin/env python3
"""Turn one Trick Trivia book page pair into an upload-ready short.

    python make.py rounds/round01.json      # render a round
    python make.py calibrate <page.png>     # check panel detection by eye

A round is three claims and their three reveals, cut straight from the
printed pages. The output is out/<id>.mp4 plus out/<id>.txt holding the
caption and hashtags, so the upload is copy, paste, post.
"""
from __future__ import annotations

import json
import os
import sys

from trivia import audio, brand, pages, render, scenes

ROOT = os.path.dirname(os.path.abspath(__file__))
DERIVED = os.path.join(ROOT, "assets", "derived")
OUT = os.path.join(ROOT, "out")


def _load(path: str) -> dict:
    with open(path) as f:
        round_spec = json.load(f)
    answers = round_spec.get("answers", [])
    if len(answers) != 3 or any(a not in ("real", "fake") for a in answers):
        raise ValueError('"answers" must be three entries of "real" or "fake"')
    return round_spec


def build_scenes(spec: dict) -> tuple[list[dict], list[tuple[float, str]]]:
    """Compose every frame of the round and log the sounds that go with it."""
    q_page = os.path.join(ROOT, spec["question_page"])
    a_page = os.path.join(ROOT, spec["answer_page"])

    q_panels = pages.crop_panels(q_page, spec.get("question_bands"))
    a_panels = pages.crop_panels(a_page, spec.get("answer_bands"))
    q_title, a_title = pages.crop_title(q_page), pages.crop_title(a_page)
    q_bg, a_bg = pages.background_swatch(q_page), pages.background_swatch(a_page)

    os.makedirs(DERIVED, exist_ok=True)
    frames: list[dict] = []
    sounds: list[tuple[float, str]] = []
    clock = 0.0

    def add(image, duration, timer=False):
        nonlocal clock
        path = os.path.join(DERIVED, f"{spec['id']}-{len(frames):02d}.png")
        image.save(path)
        frames.append({"png": path, "duration": duration, "timer": timer})
        sounds.append((clock, "whoosh"))
        return clock, duration

    # Claims. No title card first: the panel itself is the hook, and a
    # silent viewer starts reading on frame one.
    for i, panel in enumerate(q_panels):
        prompt = spec.get("prompt", "COMMENT YOUR GUESS") if i == 2 else None
        start, dur = add(
            scenes.panel_scene(q_bg, q_title, panel, counter=f"{i + 1} of 3",
                               prompt=prompt, timer=True),
            brand.T_CLAIM, timer=True)
        # Two ticks as the bar runs out, to push the guess before the cut.
        sounds += [(start + dur - 1.9, "tick"), (start + dur - 0.9, "tick")]
        clock += dur

    add(scenes.shout_scene(q_bg, spec.get("lock", ["LOCK IN", "YOUR GUESS!"])),
        brand.T_LOCK)
    clock += brand.T_LOCK

    # Reveals. The printed answer page already carries the REAL!/FAKE!
    # stamps, so the panel is the payoff -- nothing is drawn over it.
    for i, panel in enumerate(a_panels):
        start, dur = add(
            scenes.panel_scene(a_bg, a_title, panel, counter=f"{i + 1} of 3"),
            brand.T_ANSWER)
        sounds.append((start + 0.30, "ding" if spec["answers"][i] == "real" else "buzz"))
        clock += dur

    cover = None
    if spec.get("cover"):
        from PIL import Image
        cover = Image.open(os.path.join(ROOT, spec["cover"])).convert("RGB")
    card = spec.get("endcard", {})
    add(scenes.end_card(a_bg, cover,
                        card.get("headline", "ALL 210 ANSWERS"),
                        card.get("subline", "are in the book")),
        brand.T_ENDCARD)
    clock += brand.T_ENDCARD

    return frames, sounds


def render_round(spec_path: str) -> str:
    spec = _load(spec_path)
    frames, sounds = build_scenes(spec)
    duration = sum(f["duration"] for f in frames)

    os.makedirs(OUT, exist_ok=True)
    wav = audio.render(duration, sounds, os.path.join(DERIVED, f"{spec['id']}.wav"))
    ass = render.timer_track(frames, os.path.join(DERIVED, f"{spec['id']}.ass"))
    mp4 = render.build(frames, wav, ass, os.path.join(OUT, f"{spec['id']}.mp4"))

    notes = os.path.join(OUT, f"{spec['id']}.txt")
    with open(notes, "w") as f:
        f.write(spec.get("caption", "").strip() + "\n\n")
        f.write(" ".join(spec.get("hashtags", [])) + "\n")

    print(f"{mp4}  ({duration:.1f}s, {len(frames)} scenes)")
    print(f"{notes}  (caption + hashtags)")
    return mp4


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__)
        return 2
    if argv[1] == "calibrate":
        os.makedirs(DERIVED, exist_ok=True)
        page = argv[2]
        out = os.path.join(DERIVED, "calibration-" + os.path.basename(page))
        print(pages.calibrate(page, out))
        return 0
    render_round(argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
