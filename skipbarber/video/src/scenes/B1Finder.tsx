import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {SFX} from '../assets';
import {Background} from '../primitives/Background';
import {ConceptTag} from '../primitives/Bits';
import {FloatingCard} from '../primitives/FloatingCard';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp, pop} from '../primitives/motion';
import {Sfx} from '../primitives/Sfx';
import {C, F} from '../theme';
import {SceneProps} from './types';

// B1 (concept, not announced). AI Program Finder: three taps, one recommendation.
const QS = [
  {q: 'How much track experience do you have?', a: ['None yet', 'Some track days', 'I have raced'], pick: 0},
  {q: 'Which car calls to you?', a: ['GT', 'Formula', 'GTX'], pick: 1},
  {q: "What's the goal?", a: ['A gift', 'A license', 'A career'], pick: 1},
];

export const B1Finder: React.FC<SceneProps> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps, portrait, u} = useLayout();
  const step = Math.round((dur - 40) / 4);
  const taps = QS.map((_, i) => 22 + step * (i + 1) - 6);
  const resultAt = taps[2] + 10;
  const res = pop(f, fps, resultAt, 14, 180);
  return (
    <AbsoluteFill>
      <Background kind="white" />
      <ConceptTag />
      <div style={{position: 'absolute', top: (portrait ? 170 : 70) * u, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Headline text="Not sure where to *start*?" color="#111" size={portrait ? 92 : 84} />
      </div>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: (portrait ? 120 : 140) * u}}>
        <FloatingCard delay={6} tiltX={8} tiltY={-6} width={portrait ? 900 : 1000} style={{padding: 34 * u}}>
          <div style={{display: 'flex', alignItems: 'center', gap: 14 * u, marginBottom: 18 * u}}>
            <div style={{width: 40 * u, height: 40 * u, borderRadius: 12 * u, background: C.red, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 24 * u}}>&#10022;</div>
            <div style={{fontFamily: F.ui, fontWeight: 700, fontSize: 26 * u}}>AI Program Finder</div>
          </div>
          {QS.map((q, i) => {
            const t0 = 22 + step * i;
            const show = interpolate(f - t0, [0, 8], [0, 1], clamp);
            if (f < t0) return null;
            return (
              <div key={i} style={{opacity: show, transform: `translateY(${(1 - show) * 16 * u}px)`, marginTop: 14 * u}}>
                <div style={{fontFamily: F.ui, fontWeight: 600, fontSize: 25 * u, color: '#222'}}>{q.q}</div>
                <div style={{display: 'flex', gap: 12 * u, marginTop: 10 * u}}>
                  {q.a.map((a, k) => {
                    const on = k === q.pick && f >= taps[i];
                    return (
                      <div key={a} style={{padding: `${9 * u}px ${20 * u}px`, borderRadius: 999, fontFamily: F.ui, fontWeight: 600, fontSize: 21 * u, border: `2px solid ${on ? C.red : C.line}`, background: on ? C.red : '#fff', color: on ? '#fff' : '#333', transform: `scale(${on ? interpolate(f - taps[i], [0, 3, 7], [0.92, 1.06, 1], clamp) : 1})`}}>
                        {a}
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
          {f >= resultAt ? (
            <div style={{marginTop: 22 * u, padding: 22 * u, borderRadius: 18 * u, background: '#111', color: '#fff', transform: `scale(${interpolate(res, [0, 1], [0.85, 1])})`, opacity: interpolate(res, [0, 0.3], [0, 1], clamp)}}>
              <div style={{fontFamily: F.ui, fontSize: 18 * u, color: '#aaa', letterSpacing: '0.14em', textTransform: 'uppercase'}}>Recommended for you</div>
              <div style={{fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', fontSize: 44 * u, marginTop: 6 * u}}>THREE DAY RACING SCHOOL <span style={{color: C.red}}>/ FORMULA</span></div>
            </div>
          ) : null}
        </FloatingCard>
      </AbsoluteFill>
      {taps.map((t) => (
        <Sfx key={t} file={SFX.click} at={t} volume={0.6} />
      ))}
    </AbsoluteFill>
  );
};
