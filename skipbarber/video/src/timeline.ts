// Central timeline. Every scene length is in beats, so retiming to a new track is one edit:
// set BPM (and OFFSET if the first downbeat is late) from the librosa beat map.
export const FPS = 30;
export const BPM = 124; // estimate for "Sports Action Version 3"; replace with the measured value
export const OFFSET = 0; // frames before the first beat
export const BEAT = (FPS * 60) / BPM;

export type SceneId =
  | 'hook' | 'whatif' | 'counter' | 'logo' | 'series' | 'car' | 'path' | 'curriculum'
  | 'license' | 'tracks' | 'giftCareer' | 'cta' | 'end'
  | 'aiFinder' | 'aiCoach' | 'aiLaps' | 'aiPath' | 'partner';

export type Cut = {id: SceneId; beats: number; flash?: boolean};
export type Variant = 'A' | 'B' | 'V' | 'test';

const A: Cut[] = [
  {id: 'hook', beats: 8},
  {id: 'whatif', beats: 6},
  {id: 'counter', beats: 7},
  {id: 'logo', beats: 6, flash: true}, // lands on the drop, about 10s in
  {id: 'series', beats: 8, flash: true},
  {id: 'car', beats: 12},
  {id: 'path', beats: 12},
  {id: 'curriculum', beats: 16},
  {id: 'license', beats: 9, flash: true},
  {id: 'tracks', beats: 11, flash: true},
  {id: 'giftCareer', beats: 12},
  {id: 'cta', beats: 9},
  {id: 'end', beats: 12},
];

const aiScenes: Cut[] = [
  {id: 'aiFinder', beats: 13},
  {id: 'aiCoach', beats: 12},
  {id: 'aiLaps', beats: 11},
  {id: 'aiPath', beats: 9},
];

const B: Cut[] = A.flatMap((c) => {
  if (c.id === 'license') return [c, ...aiScenes];
  if (c.id === 'cta') return [{id: 'partner', beats: 6} as Cut, c];
  return [c];
});

// Vertical social cutdown, about 40s.
const V: Cut[] = [
  {id: 'hook', beats: 7},
  {id: 'counter', beats: 6},
  {id: 'logo', beats: 5, flash: true},
  {id: 'series', beats: 7, flash: true},
  {id: 'car', beats: 10},
  {id: 'curriculum', beats: 14},
  {id: 'tracks', beats: 9, flash: true},
  {id: 'giftCareer', beats: 10},
  {id: 'cta', beats: 7},
  {id: 'end', beats: 9},
];

// 10 second style test: hook, what-if over a car, counter, logo drop.
const test: Cut[] = [
  {id: 'hook', beats: 6},
  {id: 'whatif', beats: 5},
  {id: 'counter', beats: 5},
  {id: 'logo', beats: 5, flash: true},
];

export const CUTS: Record<Variant, Cut[]> = {A, B, V, test};

export type Placed = Cut & {from: number; dur: number};

// Rounds each boundary to the nearest frame of the beat grid so drift never accumulates.
export const place = (v: Variant): Placed[] => {
  let beat = 0;
  return CUTS[v].map((c) => {
    const from = Math.round(OFFSET + beat * BEAT);
    beat += c.beats;
    const to = Math.round(OFFSET + beat * BEAT);
    return {...c, from: from === OFFSET ? 0 : from, dur: to - (from === OFFSET ? 0 : from)};
  });
};

export const totalFrames = (v: Variant) => {
  const p = place(v);
  const last = p[p.length - 1];
  return last.from + last.dur;
};

// Beat helper for in-scene timing: b(2) is two beats in frames.
export const b = (n: number) => Math.round(n * BEAT);
