import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Background} from '../primitives/Background';
import {ConceptTag} from '../primitives/Bits';
import {FloatingCard} from '../primitives/FloatingCard';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp} from '../primitives/motion';
import {C, F} from '../theme';
import {SceneProps} from './types';

// B2 (concept). An instructor "digital twin" answering by voice. The answer stays generic on purpose.
const ANSWER = 'Pick your brake marker, brake hard in a straight line, then ease off the pedal as you turn in.';

export const B2Coach: React.FC<SceneProps> = ({dur}) => {
  const f = useCurrentFrame();
  const {portrait, u} = useLayout();
  const askAt = 16;
  const ansAt = 40;
  const chars = Math.floor(interpolate(f, [ansAt, Math.min(dur - 12, ansAt + 70)], [0, ANSWER.length], clamp));
  const talking = f >= ansAt && chars < ANSWER.length;
  return (
    <AbsoluteFill>
      <Background kind="ink" />
      <ConceptTag />
      <div style={{position: 'absolute', top: (portrait ? 170 : 80) * u, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Headline text={'50 years of coaching.\nNow *always on*.'} size={portrait ? 88 : 80} />
      </div>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: (portrait ? 220 : 220) * u}}>
        <FloatingCard dark delay={6} tiltX={8} tiltY={8} width={portrait ? 900 : 980} style={{padding: 34 * u}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 18 * u}}>
            <div style={{width: 72 * u, height: 72 * u, borderRadius: '50%', background: `radial-gradient(circle at 35% 30%, #ff5a5a, ${C.redDeep})`, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: F.head, fontWeight: 800, fontSize: 26 * u}}>SB</div>
            <div>
              <div style={{fontFamily: F.ui, fontWeight: 700, fontSize: 26 * u}}>Skip Barber Coach</div>
              <div style={{fontFamily: F.ui, fontSize: 19 * u, color: '#999'}}>Digital twin, built from the Skip Barber curriculum</div>
            </div>
          </div>
          <div style={{marginTop: 24 * u, marginLeft: 'auto', maxWidth: '78%', padding: `${14 * u}px ${20 * u}px`, borderRadius: 18 * u, background: '#2a2a2e', fontFamily: F.ui, fontSize: 24 * u, opacity: interpolate(f - askAt, [0, 8], [0, 1], clamp)}}>
            Where should I brake into Turn 1 at VIR?
          </div>
          <div style={{display: 'flex', alignItems: 'center', gap: 4 * u, height: 60 * u, marginTop: 20 * u, opacity: f >= ansAt - 4 ? 1 : 0}}>
            {Array.from({length: 48}, (_, i) => {
              const h = talking ? 8 + Math.abs(Math.sin(f * 0.45 + i * 0.7) * Math.sin(f * 0.13 + i * 0.31)) * 50 : 6;
              return <div key={i} style={{width: 6 * u, height: h * u, borderRadius: 3 * u, background: i % 5 === 0 ? '#fff' : C.red}} />;
            })}
          </div>
          <div style={{fontFamily: F.ui, fontSize: 26 * u, lineHeight: 1.4, color: '#eee', marginTop: 10 * u, minHeight: 80 * u}}>{ANSWER.slice(0, chars)}</div>
        </FloatingCard>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
