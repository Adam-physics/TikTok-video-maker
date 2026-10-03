// Prints Comp:frame:name jobs at a fraction through every scene of a variant.
import {readFileSync} from 'fs';
const src = readFileSync(new URL('../src/timeline.ts', import.meta.url), 'utf8');
const bpm = Number(src.match(/BPM = ([\d.]+)/)[1]);
const BEAT = (30 * 60) / bpm;
const OFFSET = Number(src.match(/OFFSET = ([\d.]+)/)[1]);
const block = (name) => src.match(new RegExp(`const ${name}: Cut\\[\\] = \\[([\\s\\S]*?)\\];`))[1];
const parse = (txt) => [...txt.matchAll(/id: '(\w+)', beats: (\d+)/g)].map((m) => ({id: m[1], beats: +m[2]}));
const [variant, comp, frac = '0.7'] = process.argv.slice(2);
let cuts;
if (variant === 'B') {
  const A = parse(block('A')), ai = parse(block('aiScenes'));
  cuts = A.flatMap((c) => (c.id === 'license' ? [c, ...ai] : c.id === 'cta' ? [{id: 'partner', beats: 8}, c] : [c]));
} else cuts = parse(block(variant));
let beat = 0;
const out = [];
for (const c of cuts) {
  const from = beat === 0 ? 0 : Math.round(OFFSET + beat * BEAT);
  beat += c.beats;
  const to = Math.round(OFFSET + beat * BEAT);
  out.push(`${comp}:${Math.round(from + (to - from) * Number(frac))}:${comp}-${c.id}`);
}
console.log(out.join(' '));
