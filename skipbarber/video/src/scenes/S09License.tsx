import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Background} from '../primitives/Background';
import {Center} from '../primitives/Bits';
import {FloatingCard} from '../primitives/FloatingCard';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp, pop} from '../primitives/motion';
import {C, F} from '../theme';
import {SceneProps} from './types';

// 9. Home page: "SCCA & USAC Licensed Racing School". /programs: the Three Day "places drivers on the
// path towards receiving a racing license with SCCA or USAC."
export const S09License: React.FC<SceneProps> = () => {
  const f = useCurrentFrame();
  const {fps, portrait, u} = useLayout();
  const stamp = pop(f, fps, 22, 10, 260);
  return (
    <AbsoluteFill>
      <Background kind="red" />
      <Center style={{gap: 56 * u}}>
        <Headline text="On the path to your *license*." size={portrait ? 96 : 96} accentColor="#fff" maxWidth={portrait ? 900 : 1600} />
        <FloatingCard delay={10} tiltX={12} tiltY={-12} width={portrait ? 820 : 760} style={{display: 'flex', alignItems: 'center', gap: 36 * u, padding: 44 * u}}>
          <svg width={150 * u} height={170 * u} viewBox="0 0 100 114" style={{flexShrink: 0, transform: `scale(${interpolate(stamp, [0, 1], [1.8, 1])}) rotate(${interpolate(stamp, [0, 1], [-20, 0])}deg)`, opacity: interpolate(f, [22, 25], [0, 1], clamp)}}>
            <path d="M50 2 L94 18 V54 C94 82 74 102 50 112 C26 102 6 82 6 54 V18 Z" fill={C.red} />
            <path d="M30 57 L45 72 L72 40" stroke="#fff" strokeWidth={10} fill="none" strokeLinecap="round" strokeLinejoin="round" />
          </svg>
          <div>
            <div style={{fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', fontSize: 84 * u, lineHeight: 0.95, letterSpacing: '-0.02em'}}>SCCA &amp; USAC</div>
            <div style={{fontFamily: F.head, fontWeight: 700, fontSize: 36 * u, color: '#333', marginTop: 10 * u}}>Licensed Racing School</div>
            <div style={{fontFamily: F.ui, fontSize: 22 * u, color: '#777', marginTop: 14 * u, lineHeight: 1.35}}>The Three Day puts you on the path to an SCCA or USAC racing license.</div>
          </div>
        </FloatingCard>
      </Center>
    </AbsoluteFill>
  );
};
