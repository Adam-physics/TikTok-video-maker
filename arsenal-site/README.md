# Arsenal Digital Holdings: homepage redesign

A static rebuild of the arsenalholdingscorp.com homepage. Open `index.html`, or serve the folder:

```bash
python3 -m http.server 8000   # then visit http://localhost:8000
```

There's no build step and no dependencies. Fonts come from Google Fonts.

| File | What it is |
| --- | --- |
| `index.html` | All page content, copied from the live site's home, about, energy, finance, health and partner pages |
| `styles.css` | Light and dark themes (follows the system setting), plus the night-sky hero and foundation band |
| `sky.js` | The hero star chart |
| `main.js` | Nav, scroll reveals, counters, the portfolio explorer, flywheel, sticky studio steps, foundation tabs, underwriting slider and deal builder |
| `assets/` | The official logo files from the live site. The dark version is the same SVG recoloured |

## The star chart

The constellation is the Arsenal mark itself. The logo's facets sit on a triangular lattice, so each vertex is a star and each facet edge is a constellation line. It's a pure brand moment: `named: false` in `main.js` turns off the earlier company-per-star labels and hover cards.

- **Load:** the stars fly in and assemble the A, and the facet edges draw themselves.
- **Hover:** facets light up near the cursor, and nearby background stars wire themselves to the cursor.
- **Click:** sends a shockwave through the stars.
- **Ambient:** shooting stars, a light sweep across the facets, parallax by depth, and warp streaks on fast scroll.
- **Efficiency:** the animation pauses offscreen and calms down when the visitor prefers reduced motion.

## Before launch

- The product screens in "What We Build" are labelled *Illustrative*. Swap in real screenshots when they exist.
- The evidence bars are drawn for illustration. The numbers and their sources match the live site.
- Links to pages not rebuilt here (IR portal, contact, newsroom, vertical pages) point at the live site.

## Demo video

The demo is a narrated product demo of Arsenal, cut in two versions, one to each music track:

- `video/arsenal-demo-tech-platforms.mp4`: about 2:28, to "Tech Platforms" (The Mountain, Pixabay).
- `video/arsenal-demo-epic-corporate.mp4`: about 2:32, to "Epic Corporate" (Paulyudin, Pixabay). This 60-second track is extended by repeating bar-aligned sections.

`video/SCRIPT.md` is the script. Everything under `video/demo/` is code, so wording, timing and visuals can all be changed and the video rebuilt.

| Step | Command | What it does |
|---|---|---|
| 1. Narration | `python3 make_vo.py <kokoro dir>` | Generates `vo/*.wav` from `vo/lines.json` with the Kokoro "Michael" voice, through sherpa-onnx |
| 2. Timing | `python3 build_cues.py vo/durations.json` | Puts each scene on a bar line and each narration line on a beat of the track (`cues-<track>.json`) |
| 3. Picture | `node render.js tech out/tech-silent.mp4` | Renders `demo.html?v=tech` frame by frame to a silent 1080p video and lists its sound cues. Serve `arsenal-site/` on port 8765 first |
| 4. Sound | `python3 mix.py tech <music.mp3> vo out/tech-silent.mp4 out/final.mp4` | Mixes the music (ducked under the voice), the narration and the sound effects, then normalizes loudness to -14 LUFS |

For a live preview, open `demo/demo.html?v=tech` (or `?v=epic`) in a browser served from this folder.

The music files aren't committed; they come from Pixabay under the Pixabay Content License. Product scenes are illustrative, so have counsel review the narration before any investor-facing use.

## Previous version

`arsenal-preview-v1.html` is a frozen single-file copy of the site before the constellation redesign. To restore that version completely:

```bash
git checkout 7b9e77f -- arsenal-site/index.html arsenal-site/styles.css arsenal-site/main.js arsenal-site/sky.js arsenal-site/arsenal-preview.html
```
