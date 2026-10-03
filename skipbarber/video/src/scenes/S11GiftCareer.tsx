import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {P} from '../assets';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp} from '../primitives/motion';
import {Photo} from '../primitives/Photo';
import {SceneProps} from './types';

// 11. Home page: "whether you're looking for a one-of-a-kind gift or want to start your racing career"
// and "From one-day bucket-list experiences..."
export const S11GiftCareer: React.FC<SceneProps> = ({dur}) => {
  const f = useCurrentFrame();
  const {portrait, u} = useLayout();
  const half = Math.round(dur / 2);
  const k = interpolate(f, [half - 6, half + 6], [0, 1], {...clamp});
  const a = 64 - 28 * k; // share of the first panel, percent
  const panel = (file: string, share: number, lit: number, first: boolean): React.CSSProperties =>
    portrait
      ? {position: 'absolute', left: 0, right: 0, top: first ? 0 : `${100 - share}%`, height: `${share}%`, overflow: 'hidden', filter: `brightness(${0.45 + 0.55 * lit})`}
      : {position: 'absolute', top: 0, bottom: 0, left: first ? 0 : `${100 - share}%`, width: `${share}%`, overflow: 'hidden', filter: `brightness(${0.45 + 0.55 * lit})`};
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <div style={panel(P.student, a, 1 - k, true)}>
        <Photo file={P.student} dur={dur} from={1.05} to={1.15} driftX={-2} />
      </div>
      <div style={panel(P.trophy, 100 - a, k, false)}>
        <Photo file={P.trophy} dur={dur} from={1.05} to={1.15} driftX={2} />
      </div>
      <div style={{position: 'absolute', ...(portrait ? {left: 0, right: 0, top: `${a}%`, height: 6 * u} : {top: 0, bottom: 0, left: `${a}%`, width: 6 * u}), background: '#FF0000', transform: portrait ? 'translateY(-50%)' : 'translateX(-50%)', boxShadow: '0 0 30px #FF0000'}} />
      <AbsoluteFill style={{background: 'linear-gradient(0deg, rgba(0,0,0,0.75), rgba(0,0,0,0) 45%)'}} />
      <Sequence durationInFrames={half}>
        <div style={{position: 'absolute', left: (portrait ? 60 : 110) * u, bottom: (portrait ? 1020 : 110) * u}}>
          <Headline text="A bucket-list *gift*." size={portrait ? 100 : 110} align="left" delay={2} stagger={3} exitAt={half - 7} />
        </div>
      </Sequence>
      <Sequence from={half}>
        <div style={{position: 'absolute', right: (portrait ? 60 : 110) * u, bottom: (portrait ? 140 : 110) * u}}>
          <Headline text={'Or the start\nof a *career*.'} size={portrait ? 100 : 110} align={portrait ? 'left' : 'left'} delay={2} stagger={3} />
        </div>
      </Sequence>
    </AbsoluteFill>
  );
};
