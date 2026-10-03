import React from 'react';
import {AbsoluteFill, Audio, interpolate, Sequence} from 'remotion';
import {has, MUSIC, SFX, src} from './assets';
import './fonts';
import {Sfx} from './primitives/Sfx';
import {CutFlash} from './primitives/SpeedLine';
import {B1Finder} from './scenes/B1Finder';
import {B2Coach} from './scenes/B2Coach';
import {B3Laps} from './scenes/B3Laps';
import {B4Path} from './scenes/B4Path';
import {BPartner} from './scenes/BPartner';
import {S01Hook} from './scenes/S01Hook';
import {S02WhatIf} from './scenes/S02WhatIf';
import {S03Counter} from './scenes/S03Counter';
import {S04Logo} from './scenes/S04Logo';
import {S05Series} from './scenes/S05Series';
import {S06Car} from './scenes/S06Car';
import {S07Path} from './scenes/S07Path';
import {S08Curriculum} from './scenes/S08Curriculum';
import {S09License} from './scenes/S09License';
import {S10Tracks} from './scenes/S10Tracks';
import {S11GiftCareer} from './scenes/S11GiftCareer';
import {S12Cta} from './scenes/S12Cta';
import {S13End} from './scenes/S13End';
import {SceneProps} from './scenes/types';
import {beatTime, FPS, MUSIC_EDIT, place, SceneId, totalFrames, Variant} from './timeline';

const SCENES: Record<SceneId, React.FC<SceneProps & {partnerTag?: boolean}>> = {
  hook: S01Hook, whatif: S02WhatIf, counter: S03Counter, logo: S04Logo, series: S05Series, car: S06Car,
  path: S07Path, curriculum: S08Curriculum, license: S09License, tracks: S10Tracks, giftCareer: S11GiftCareer,
  cta: S12Cta, end: S13End, aiFinder: B1Finder, aiCoach: B2Coach, aiLaps: B3Laps, aiPath: B4Path, partner: BPartner,
};

export const Demo: React.FC<{variant: Variant}> = ({variant}) => {
  const total = totalFrames(variant);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {place(variant).map((s) => {
        const Scene = SCENES[s.id];
        return (
          <Sequence key={`${s.id}-${s.from}`} from={s.from} durationInFrames={s.dur} name={s.id}>
            <Scene dur={s.dur} partnerTag={variant === 'B'} />
            {s.flash ? <CutFlash /> : null}
            {s.flash ? <Sfx file={SFX.whoosh} volume={0.4} /> : null}
          </Sequence>
        );
      })}
      {has(MUSIC) ? <Music variant={variant} total={total} /> : null}
    </AbsoluteFill>
  );
};

const TRACK_FRAMES = Math.floor(67.78 * FPS);
const MUSIC_VOL = 0.85;

// Lays the source track out as the variant's bar-aligned edit list. Each join gets a 2 frame
// dip so the splice never clicks; the last segment fades only if the video ends before the music.
const Music: React.FC<{variant: Variant; total: number}> = ({variant, total}) => {
  let at = 0;
  const segs = MUSIC_EDIT[variant].map(([a, b], i, all) => {
    const from = a === null ? 0 : Math.round(beatTime(a) * FPS);
    const to = b === null ? TRACK_FRAMES : Math.round(beatTime(b) * FPS);
    const len = Math.min(to - from, total - at);
    const seg = {from, len, at, first: i === 0, last: i === all.length - 1};
    at += to - from;
    return seg;
  });
  return (
    <>
      {segs.filter((s) => s.len > 0).map((s) => (
        <Sequence key={s.at} from={s.at} durationInFrames={s.len} layout="none">
          <Audio
            src={src(MUSIC)}
            trimBefore={s.from}
            durationInFrames={s.len}
            volume={(f) => {
              const inRamp = s.first ? 1 : interpolate(f, [0, 2], [0.2, 1], {extrapolateRight: 'clamp'});
              const endsEarly = s.at + s.len >= total && s.from + s.len < TRACK_FRAMES - 2;
              const outRamp = endsEarly
                ? interpolate(f, [s.len - 12, s.len], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})
                : s.last ? 1 : interpolate(f, [s.len - 2, s.len], [1, 0.2], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
              return MUSIC_VOL * inRamp * outRamp;
            }}
          />
        </Sequence>
      ))}
    </>
  );
};
