# Reference analysis

How the numbers were made (all scripts and raw output are in `analysis/`):

- Cuts: `ffmpeg -vf "select='gt(scene,0.3)',showinfo"` (hard cuts), plus a second pass at `0.12` to catch soft motion-graphic changes. Results: `analysis/*-cuts.txt`, `analysis/*-cuts-012.txt`.
- Frames: 2 fps stills in `analysis/frames-*/`, 1 fps contact sheets in `analysis/*-sheet-*.jpg`.
- Audio: `analysis/audio.py` (librosa beat tracking, RMS per second, harmonic/percussive split). Raw output: `analysis/audio.json`.
- Voiceover check: modulation energy at syllable rate (3 to 6 Hz) in the 300 to 3400 Hz speech band, relative to 0.5 to 20 Hz.

## Numbers

| | Byline short | Outrank | Download 24 |
|---|---|---|---|
| Duration / format | 53.4s, 1920x1080, 30fps | 98.6s, 1280x720, 60fps | 128.6s, 1920x1080, 30fps |
| Tempo | 136 BPM (beat 0.44s) | 112 BPM (beat 0.53s) | 99 BPM (beat 0.60s) |
| Hard cuts (scene > 0.3) | 17 | 39 (about 15 of them inside 3 to 5 frame glitch bursts) | 2 |
| Avg shot length, hard cuts | 3.0s | 2.5s | about 43s (one continuous canvas) |
| How often the screen content changes | about every 1.5s (text swaps inside a shot) | about every 1.0s | about every 2 to 3s (camera moves between cards) |
| Hard cuts within 100ms of a beat | 94% (16 of 17) | most clean cuts land on a beat; the glitch bursts are fast transitions that straddle one | n/a |
| Voiceover | No, music only (mod ratio 1.19) | No, music only (1.26) | **Probably yes** (1.72, plus RMS that moves like speech). Worth a listen; it does not change the plan |

### Energy arc (RMS per second)

- **Byline:** Loud first second, then a deliberate dip to about -29 dB at 0:03 to 0:05 under "IS HARD." / "REALLY HARD" (the tension beat). It builds back to about -13 dB by 0:10 to 0:11, right as "Meet" and the logo reveal land. After that it pulses in 3 to 4 second phrases with small dips (-25 dB at 0:19, 0:32, 0:37, 0:42), each one followed by a new section. Final hit at about 0:49, fading to -37 dB on the end card.
- **Outrank:** Quieter intro (-20 dB) for 7 seconds, then the drop at about 0:08 to 0:09 ("are searching for" into the product question). Flat and loud (-12 dB) until 0:26. A breakdown from 0:26 to 0:40 (-21 to -25 dB) under the chart and calendar section. A second drop at about 0:41, which runs at full energy to 1:35, then a hard stop under the URL card.
- **Download 24:** Steady -16 to -18 dB throughout with no clear build. Background bed under narration.

Takeaway for Skip Barber: open with tension and a dip under "RACING IS HARD.", put the drop on the logo reveal (around 0:12 to 0:15), add one breakdown in the middle (pick your path / curriculum), build into a second drop for tracks and the gift/career payoff, and end on a clean hit.

## Style breakdown

### Text animation
- **Byline:** Mostly two-line headlines, centered, medium-weight geometric sans. One accent word per line, either in an electric-blue sans ("the *expert*", "*quote*") or an italic serif ("Pick your *topic*.", "We design *your cover*."). Words blur in one at a time (blur plus opacity, slight upward drift), about 3 to 4 frames apart. Exits blur out. The hook "IS HARD." uses wide letter spacing, then a white frame with a "REALLY HARD" stretched-perspective slam.
- **Outrank:** Same skeleton, faster and louder. Typewriter builds ("Getting traffic", "find the relevant KEYWOR..."), letter-by-letter bouncy "Meet!", stretched "IS HAAARD!", arrows converging on a single word ("spot"), stacked repeating highlight words ("hands-free. hands-free. hands-free.") with purple highlight boxes.
- Both: text holds just long enough to read once, usually 1 to 2 beats.

### Transitions
- Hard cuts on the beat for type cards (both).
- Byline: soft background swaps (black, then blue gradient, then white) with type carrying through. UI cards float in with a spring and a slight 3D tilt, then drift.
- Outrank: whip pans and 3 to 5 frame glitch/stretch bursts, zooms through a 3D tilted calendar, fast lateral slides of real UI screenshots, a circle wipe (purple dot expands, cursor clicks it).

### Color
- Byline: near-black navy (#05070F range), electric blue (#2F4BFF range) gradient with a soft light bloom bottom right, plain white for UI scenes. One accent color only.
- Outrank: pure black, white, one purple (#9B4DFF range) as both background flood and accent.
- Rule both follow: **three neutrals plus exactly one accent**. For Skip Barber that becomes black, white, a dark red-to-black gradient, and a red accent.

### Type
- A clean geometric sans for everything (Byline looks like a Gilroy/Satoshi style face, Outrank similar). An italic serif only for accent words (Byline). Big numbers in a heavy weight inside a thin ring meter ("667", then "1,019" honest Amazon reviews; Outrank "4,855" then "627,340").

### Product UI
- Byline: simplified white cards with soft shadow, a cursor clicking an option, a highlighted row, a voice-waveform pill. Never a full real screen.
- Outrank: real screens, cropped tight and tilted, with a cursor and typing.
- For Skip Barber there is no app to show, so the "product" is the booking decision: car picker, program path, day-by-day curriculum, license badge, track chips. These work as Byline-style simplified cards.

### Logo moment
- Both: a pill-shaped glowing logo on black, revealed letter by letter right after a "Meet!" beat, around 0:11 to 0:14, on the musical drop.

### Endings
- Byline: "Become the published *authority* in your field." then "Build your *quote* today." with a small pill CTA button, then logo plus tagline end card (about 4s hold).
- Outrank: three short lines ("Start ranking today.", "Outrank the competition.", "Start your FREE trial now."), a counter, then the URL alone on black for 3 seconds.

## What this means for the build

- **Pacing:** a new visual about every 1 to 1.5s, a hard cut about every 2.5 to 3s. That matches the brief's "0.8 to 2.5s per shot".
- **Tempo:** pick a royalty-free track in the **120 to 135 BPM** range, between Outrank's 112 and Byline's 136. At 128 BPM a beat is 14.06 frames at 30fps, so word slams can sit on a 14/14/14/15 frame grid. The real grid will come from librosa on the chosen track.
- **Cut placement:** snap every hard cut to a beat (Byline hits 94%), and put the logo reveal on the first drop.
- **Arc:** tension dip, then drop on the logo, a full-energy product section, a breakdown under the curriculum, a second drop for tracks and gift/career, then a clean final hit on the end card.
- **What neither reference has:** real photography. Alternate kinetic type and white UI cards with full-bleed, slowly moving car photos. Never let a still sit still.
