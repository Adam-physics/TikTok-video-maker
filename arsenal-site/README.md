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

The constellation is the Arsenal mark itself. The logo's facets sit on a triangular lattice, so each vertex is a star and each facet edge is a constellation line. Eleven named stars stand for the shared AI stack, the seven portfolio companies, Energy and Finance (the two feet of the A), and Health & Insurance (the violet tip).

- **Load:** the stars fly in and assemble the A, and the facet edges draw themselves.
- **Hover:** facets light up near the cursor, and nearby background stars wire themselves to the cursor.
- **Named stars:** hovering shows a card, and clicking jumps to that company or tab.
- **Click on empty sky:** sends a shockwave through the stars.
- **Ambient:** shooting stars, a light sweep across the facets, parallax by depth, and warp streaks on fast scroll.
- **Efficiency:** the animation pauses offscreen and calms down when the visitor prefers reduced motion.

## Before launch

- The product screens in "What We Build" are labelled *Illustrative*. Swap in real screenshots when they exist.
- The evidence bars are drawn for illustration. The numbers and their sources match the live site.
- Links to pages not rebuilt here (IR portal, contact, newsroom, vertical pages) point at the live site.
