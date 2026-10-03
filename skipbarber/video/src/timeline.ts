// Central timeline. Every scene length is in beats, so retiming to a new track is one edit:
// set BPM (and OFFSET if the first downbeat is late) from the librosa beat map.
export const FPS = 30;
// Measured with librosa on "Sports Action Version 3" (analysis/music-track.json): 185.2 BPM in
// eighths, so 92.61 quarter-note BPM, first downbeat at 1.318s. One bar = 4 beats = 2.59s.
// Sections: groove from 1.3s, hats enter at beat 12 (9.09s), full energy at beat 16, breakdown at
// beat 32, build at beat 40, drop at beat 48 (32.42s), hard stop at beat 96 (63.52s).
export const BPM = 92.61;
export const OFFSET = 39.54; // frames before the first downbeat
export const BEAT = (FPS * 60) / BPM;

export type SceneId =
  | 'hook' | 'whatif' | 'counter' | 'logo' | 'series' | 'car' | 'path' | 'curriculum'
  | 'license' | 'tracks' | 'giftCareer' | 'cta' | 'end'
  | 'aiFinder' | 'aiCoach' | 'aiLaps' | 'aiPath' | 'partner';

export type Cut = {id: SceneId; beats: number; flash?: boolean};
export type Variant = 'A' | 'B' | 'V' | 'test';

const A: Cut[] = [
  {id: 'hook', beats: 4}, // pickup + bar 1
  {id: 'whatif', beats: 4},
  {id: 'counter', beats: 4},
  {id: 'logo', beats: 4, flash: true}, // hats enter
  {id: 'series', beats: 8, flash: true}, // full energy, one series per beat
  {id: 'car', beats: 8},
  {id: 'path', beats: 8}, // breakdown
  {id: 'curriculum', beats: 12}, // build; step 03 "Race." lands on the drop
  {id: 'license', beats: 6, flash: true},
  {id: 'tracks', beats: 10, flash: true},
  {id: 'giftCareer', beats: 12},
  {id: 'cta', beats: 8},
  {id: 'end', beats: 9}, // last bar, then one beat of tail after the music stops
];

const aiScenes: Cut[] = [
  {id: 'aiFinder', beats: 12},
  {id: 'aiCoach', beats: 12},
  {id: 'aiLaps', beats: 12},
  {id: 'aiPath', beats: 8},
];

const B: Cut[] = A.flatMap((c) => {
  if (c.id === 'license') return [c, ...aiScenes];
  if (c.id === 'cta') return [{id: 'partner', beats: 8} as Cut, c];
  return [c];
});

// Vertical social cutdown, about 41s.
const V: Cut[] = [
  {id: 'hook', beats: 4},
  {id: 'counter', beats: 4},
  {id: 'logo', beats: 4, flash: true},
  {id: 'series', beats: 8, flash: true},
  {id: 'car', beats: 7},
  {id: 'curriculum', beats: 9},
  {id: 'tracks', beats: 6, flash: true},
  {id: 'giftCareer', beats: 7},
  {id: 'cta', beats: 5},
  {id: 'end', beats: 7},
];

// 10 second style test: hook, what-if over a car, counter, logo as the hats come in.
const test: Cut[] = [
  {id: 'hook', beats: 4},
  {id: 'whatif', beats: 4},
  {id: 'counter', beats: 4},
  {id: 'logo', beats: 2, flash: true},
];

export const CUTS: Record<Variant, Cut[]> = {A, B, V, test};

export type Placed = Cut & {from: number; dur: number};

// Rounds each boundary to the nearest frame of the beat grid so drift never accumulates.
export const place = (v: Variant): Placed[] => {
  let beat = 0;
  // The first scene starts at frame 0 and also covers the pickup before the first downbeat.
  return CUTS[v].map((c, i) => {
    const from = i === 0 ? 0 : Math.round(OFFSET + beat * BEAT);
    beat += c.beats;
    const to = Math.round(OFFSET + beat * BEAT);
    return {...c, from, dur: to - from};
  });
};

export const totalFrames = (v: Variant) => {
  const p = place(v);
  const last = p[p.length - 1];
  return last.from + last.dur;
};

// Beat helper for in-scene timing: b(2) is two beats in frames.
export const b = (n: number) => Math.round(n * BEAT);

// Music edit per variant, as [fromBeat, toBeat] ranges of the source track laid end to end
// (null = track start or end). Cuts sit on bar lines, so the downbeat grid never slips.
export type Seg = [number | null, number | null];
export const MUSIC_EDIT: Record<Variant, Seg[]> = {
  A: [[null, null]],
  // B: after the license scene (beat 58) repeat beats 18 to 62 under the 44 AI beats, then
  // repeat beats 72 to 80 under the 8 partner beats before the CTA.
  B: [[null, 58], [18, 62], [58, 80], [72, 80], [80, null]],
  // V: first 32 beats, then jump to beat 68 so the cut ends on the track's real ending.
  V: [[null, 32], [68, null]],
  test: [[null, 14]],
};

export const beatTime = (beat: number) => OFFSET / FPS + (beat * 60) / BPM;
