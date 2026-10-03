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
import {place, SceneId, totalFrames, Variant} from './timeline';

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
      {has(MUSIC) ? (
        <Audio src={src(MUSIC)} volume={(f) => interpolate(f, [0, 3, total - 45, total - 1], [0, 0.9, 0.9, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'})} />
      ) : null}
    </AbsoluteFill>
  );
};
