import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {P, SFX} from '../assets';
import {Background} from '../primitives/Background';
import {Center, Eyebrow} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {KineticWord} from '../primitives/KineticWord';
import {useLayout} from '../primitives/layout';
import {clamp} from '../primitives/motion';
import {Photo} from '../primitives/Photo';
import {Sfx} from '../primitives/Sfx';
import {C, F} from '../theme';
import {SceneProps} from './types';

// 5. Alumni across Formula 1, IndyCar, IMSA and NASCAR. Sources: /Race-Series (Perez, Herta, Taylor),
// /testimonials (Ross Chastain). One series per beat, each over a photo flash.
const SERIES = [
  {name: 'Formula 1', photo: P.f4Pack},
  {name: 'IndyCar', photo: P.f4SideBySide},
  {name: 'IMSA', photo: P.gtPack},
  {name: 'NASCAR', photo: P.gtx},
];

export const S05Series: React.FC<SceneProps> = ({dur}) => {
  const f = useCurrentFrame();
  const {portrait, u} = useLayout();
  const unit = dur / 8; // 2 units intro, 4 words, 2 units summary
  const intro = Math.round(unit * 2);
  const wordLen = Math.round(unit);
  const outro = intro + wordLen * 4;
  return (
    <AbsoluteFill>
      <Background kind="red" />
      <Sequence durationInFrames={intro}>
        <Center>
          <Headline text="From our *classroom* to" size={portrait ? 96 : 110} delay={1} stagger={3} />
        </Center>
      </Sequence>
      {SERIES.map((s, i) => (
        <Sequence key={s.name} from={intro + i * wordLen} durationInFrames={wordLen}>
          <AbsoluteFill style={{background: '#000'}}>
            <Photo file={s.photo} dur={wordLen} from={1.18} to={1.08} driftX={3} darken={0.55} streaks />
            <Center>
              <KineticWord text={s.name} size={portrait ? 118 : 210} />
            </Center>
          </AbsoluteFill>
          <Sfx file={SFX.whooshShort} at={0} volume={0.35} />
        </Sequence>
      ))}
      <Sequence from={outro}>
        <Background kind="black" />
        <Center style={{gap: 26 * u}}>
          <Eyebrow text="Skip Barber alumni" />
          <div style={{display: 'flex', flexDirection: portrait ? 'column' : 'row', alignItems: 'center', gap: (portrait ? 10 : 46) * u}}>
            {SERIES.map((s, i) => (
              <div
                key={s.name}
                style={{
                  fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', textTransform: 'uppercase', color: i % 2 ? C.red : '#fff',
                  fontSize: (portrait ? 110 : 96) * u, letterSpacing: '-0.02em',
                  opacity: interpolate(f - outro - i * 2, [0, 5], [0, 1], clamp),
                  transform: `translateY(${interpolate(f - outro - i * 2, [0, 7], [30, 0], clamp) * u}px)`,
                }}
              >
                {s.name}
              </div>
            ))}
          </div>
        </Center>
      </Sequence>
    </AbsoluteFill>
  );
};
