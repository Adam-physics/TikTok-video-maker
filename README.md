# Trick Trivia — TikTok short generator

Turns a page pair from *Trick Trivia! Real or Fake?* into an upload-ready
vertical video. One command in, one MP4 plus its caption out.

```bash
npm install                       # fetches a static ffmpeg, no system install
pip install -r requirements.txt
python make.py rounds/round01.json
```

Output lands in `out/`: `round01.mp4` (1080x1920, H.264/AAC, faststart) and
`round01.txt` (caption and hashtags to paste at upload).

## Why it looks like the book

Nothing about the brand is re-created in code. The halftone background, the
title lockup and the three claim panels are all **cropped out of the printed
page**, so a frame is the book rather than a design that references it. The
answer pages already carry their own `REAL!` / `FAKE!` stamps, so a reveal
needs nothing drawn over it.

That is also the marketing argument: a viewer who plays three rounds has
used the product. The book is the obvious next step, not a pitch.

## Adding a round

Drop the two page scans in `assets/pages/`, then check the crop by eye
before rendering half a minute of video around it:

```bash
python make.py calibrate assets/pages/q07.png
# writes assets/derived/calibration-q07.png with the panels outlined
```

Panels are found automatically by looking for the cards' near-black rules.
If a page defeats the detector, set `question_bands` / `answer_bands` in the
round file as `[[top, bottom], ...]` fractions of page height.

Then a round file:

```json
{
  "id": "round07",
  "question_page": "assets/pages/q07.png",
  "answer_page": "assets/pages/a07.png",
  "cover": "assets/cover.png",
  "answers": ["real", "fake", "real"],
  "prompt": "COMMENT YOUR GUESS",
  "endcard": {"headline": "207 MORE INSIDE", "subline": "link in bio"},
  "caption": "...",
  "hashtags": ["#realorfake", "#funfacts"]
}
```

`answers` drives the reveal sound — a chime for real, a honk for fake — so
getting it wrong is audible.

## Beat sheet

| Beat | Length | Purpose |
|---|---|---|
| Claim 1–3 | 4.4s each | Guess timer drains; two ticks push a decision before the cut |
| Lock in | 1.3s | The pause that makes people commit in the comments |
| Reveal 1–3 | 3.6s each | Payoff, with the printed stamp |
| End card | 2.6s | The book as the answer key |

About 28 seconds, which is long enough to guess and short enough that a
finished watch still counts as one. Adjust in `trivia/brand.py`.

## Design decisions worth keeping

**Silent by default.** No narration. Reading the claim *is* the game, and a
robot voice reading it aloud spoils the pace. Free TTS is not good enough to
put next to this artwork, so the score is synthesised instead: `trivia/audio.py`
writes its own marimba bed and effects with numpy. Nothing here carries a
licence that can strike a monetised account later, and the bed sits at
-21 dB mean so narration can be added later without a remix.

**Layout adapts, text never clips.** Type shrinks until it fits the side
margins, and the block under the timer is centred in whatever room the
header leaves — so a wordy answer panel and a short claim panel both sit
balanced with no per-page tuning.

**TikTok's chrome is respected.** `SAFE_BOTTOM` keeps the caption, the
handle and the button rail from covering anything that has to be read.

## Layout

```
make.py             CLI: render a round, or calibrate a page crop
trivia/brand.py     canvas, palette, safe area, beat lengths
trivia/pages.py     find and crop panels, title and background from a page
trivia/scenes.py    compose 1080x1920 stills
trivia/audio.py     procedural score and effects -> WAV
trivia/render.py    ffmpeg assembly: motion, guess timer, mux
tools/              synthetic test pages; delete once real scans are in
```

## How panels are found

Ink is not a usable signal on these pages: the illustrations are full-bleed
and often darker than the card outlines, and decorative bubbles overlap the
card edges. Instead the detector looks for the **ground** — the only rows
that are almost entirely background are the seams between cards, the space
under the title, and the margin below the last card. Four seams bound three
panels. This holds even on reveal pages whose underwater art is close in
hue to the blue page ground.

Two consequences worth knowing:

- The background swatch is cut from the **widest band of pure ground**, not
  from a corner — the corners hold the mascot and decorative stars. It is
  then sized to a whole number of halftone periods, so the tiled canvas
  shows no grid.
- The claim-page strapline ("CAN YOU SPOT THE TRUTH?") sits above the first
  card and inside its seam. It is trimmed off panel one and left in the
  title lockup, where it belongs, so all three panels come out the same
  height.

`tools/make_test_pages.py` regenerates stand-in pages matching the real
geometry, for testing the pipeline without touching the artwork.

## Carousels (Photo Mode)

```bash
python make.py carousel rounds/round01.json
# -> out/round01-carousel/slide-01.jpg … slide-07.jpg + caption.txt
```

Seven slides: a hook claim, two more claims, three reveals, the close.
`order` in the round file puts the claim most adults get wrong on slide one.

### Why carousels, and the rules the layout follows

Photo Mode is scored on swipe-through, saves, comments and completion, not
watch time — every swipe is an active signal, and the format is currently
pushed harder than video and less crowded. A real-or-fake page is already a
swipe structure: claim, swipe, reveal.

Rules from the research, baked into `trivia/carousel.py`:

- **1080×1920.** Critical text centre-middle. Nothing that must be read in
  the bottom 350px or right 64px, where TikTok's UI sits.
- **Slide one is the thumbnail.** If it does not earn a swipe, the other
  slides do not exist. It carries the visual hook (the panel) and the text
  hook (the line above it), and they must say the same thing.
- **Five to seven slides.** Engagement drops after seven.
- **Nudge the swipe.** "swipe →" on early slides measurably lifts
  swipe-through. Each slide closes the loop the last one opened and opens
  the next.
- **The last slide asks for an action.** Completion plus a comment is the
  strongest pair of signals a post gets — hence "Comment your score".
- **Caption ≥200 characters, keyword-rich.** TikTok indexes captions for
  search. Three to eight niche hashtags; never `#fyp`.
- **Rotate slide one every one to two weeks.** Audience fatigue is fast.

### Kallaway's hook model, applied

Hook priority is **visual → written → spoken**, because eyes comprehend
before ears do. A carousel has no spoken hook, so it is the purest case:
the picture and the on-screen line carry everything. His three-step
formula — *context lean-in* (what is this, why care), *scroll-stop
interjection* (a contrasting claim), *contrarian snapback* (the turn) —
maps onto slide one, slide one's chip, and the reveal. Keep on-screen
hooks under seven words and specific.

### At post time (things the files cannot do for you)

- **Add a trending sound in the app.** Photo Mode without audio gets
  ~70% less reach. Lo-fi and sped-up tracks currently outperform library
  music on carousel placements.
- Paste `caption.txt` as the caption.
- Post the video *and* the carousel for the same round; they reach
  differently.

## Still to do

- `assets/cover.png` — goes on the video end card and the carousel close.
- `reviews` in the round file: `[{"name": "…", "quote": "…"}]` — the close
  slide renders up to three as review cards.
- More page scans: the close fans every page in `assets/pages`, and five
  distinct pages read as a real book where four cycles.

## Page naming

Pages pair up as question then answer, in printed order:

| File | Book page | Contents |
|---|---|---|
| `assets/pages/q01.png` | 1 | flamingo / polar bear / octopus — claims |
| `assets/pages/a01.png` | 2 | the same three, revealed |
| `assets/pages/q02.png` | 3 | dolphin / snail / bat — claims |
| `assets/pages/a02.png` | 4 | the same three, revealed |

Upload the highest-resolution originals you have. The panels get scaled up
to fill a 1080-wide frame, so a print-resolution source stays crisp where a
screenshot will not.
