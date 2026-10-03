import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {P} from '../assets';
import {Chip, Eyebrow} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {Photo} from '../primitives/Photo';
import {SceneProps} from './types';

// 10. Home page: "driving and racing schools at the finest tracks in America". Every track below
// has a school page on skipbarber.com. 2027 programs are on sale at VIR and Sonoma.
const TRACKS = ['VIRginia International Raceway', 'Sonoma Raceway', 'Sebring', 'Lime Rock Park', 'Circuit of the Americas', 'Laguna Seca', 'NJMP'];
const SHOTS = [P.vir, P.sonoma, P.cota];

export const S10Tracks: React.FC<SceneProps> = ({dur}) => {
  const {portrait, u} = useLayout();
  const len = Math.ceil(dur / SHOTS.length);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      {SHOTS.map((s, i) => (
        <Sequence key={s} from={i * len} durationInFrames={len}>
          <Photo file={s} dur={len} from={1.04} to={1.14} driftX={i % 2 ? 3 : -3} darken={0.25} />
        </Sequence>
      ))}
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.35) 50%, rgba(0,0,0,0.25) 100%)'}} />
      <div style={{position: 'absolute', left: (portrait ? 60 : 110) * u, right: (portrait ? 60 : 110) * u, bottom: (portrait ? 220 : 100) * u, display: 'flex', flexDirection: 'column', gap: 30 * u}}>
        <Eyebrow text="2027 programs on sale now at VIR and Sonoma" delay={Math.round(dur * 0.55)} color="#fff" />
        <Headline shadow text={'The finest tracks\nin *America*.'} size={portrait ? 112 : 120} align="left" delay={2} stagger={3} />
        <div style={{display: 'flex', flexWrap: 'wrap', gap: 14 * u, maxWidth: (portrait ? 960 : 1500) * u}}>
          {TRACKS.map((t, i) => (
            <Chip key={t} label={t} delay={12 + i * 4} size={portrait ? 30 : 28} />
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};
