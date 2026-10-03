# Skip Barber demo video (Remotion)

```bash
npm install
npm run studio                                   # live preview
npm run render -- src/index.ts DemoA ../out/skipbarber-demo-A-16x9.mp4
npm run render -- src/index.ts DemoB ../out/skipbarber-demo-B-16x9-Concept.mp4
npm run render -- src/index.ts DemoA9x16 ../out/skipbarber-demo-A-9x16.mp4
npm run render -- src/index.ts StyleTest ../out/style-test-10s.mp4
```

- Timing: `src/timeline.ts`. Scene lengths are in beats, so set `BPM`/`OFFSET` from the track's beat map and everything re-snaps.
- One file per scene in `src/scenes/`, shared pieces in `src/primitives/`.
- Assets go in `public/` with the names listed in `../scrape/inventory.md`. Anything missing renders as a labeled placeholder (or is silent, for audio), so the project always renders.
- `remotion.config.ts` points Remotion at the preinstalled Chromium in the cloud container; elsewhere Remotion uses its own.
