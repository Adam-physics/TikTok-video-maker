import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {Background} from '../primitives/Background';
import {ConceptTag} from '../primitives/Bits';
import {FloatingCard} from '../primitives/FloatingCard';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp} from '../primitives/motion';
import {C, F} from '../theme';
import {SceneProps} from './types';

// B3 (concept). Post-session dashboard. Lap times are illustrative and labeled as such.
const LAPS = [2.172, 2.151, 2.139, 2.128, 2.117, 2.109, 2.101];
const NOTES = ['Carry more speed to the apex', 'Pick up the throttle earlier', 'Hit the same brake marker every lap'];
const fmt = (m: number) => {
  const s = m * 60;
  return `${Math.floor(s / 60)}:${(s % 60).toFixed(2).padStart(5, '0')}`;
};

export const B3Laps: React.FC<SceneProps> = ({dur}) => {
  const f = useCurrentFrame();
  const {portrait, u} = useLayout();
  const cw = portrait ? 820 : 640;
  const ch = 300;
  const draw = interpolate(f, [14, Math.min(60, dur - 20)], [0, 1], {...clamp, easing: Easing.bezier(0.5, 0, 0.2, 1)});
  const max = Math.max(...LAPS) + 0.01;
  const min = Math.min(...LAPS) - 0.01;
  // Faster laps plot higher, so the line climbs like Outrank's traffic chart.
  const up = LAPS.map((l, i) => [(i / (LAPS.length - 1)) * cw, ((l - min) / (max - min)) * ch]);
  const d = up.map(([x, y], i) => `${i ? 'L' : 'M'} ${x} ${y}`).join(' ');
  const len = up.slice(1).reduce((a, p, i) => a + Math.hypot(p[0] - up[i][0], p[1] - up[i][1]), 0);
  const shown = Math.min(LAPS.length - 1, Math.floor(draw * (LAPS.length - 1) + 0.001));
  return (
    <AbsoluteFill>
      <Background kind="white" />
      <ConceptTag />
      <div style={{position: 'absolute', top: (portrait ? 170 : 70) * u, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Headline text="Your laps, *analyzed*." color="#111" size={portrait ? 96 : 88} />
      </div>
      <AbsoluteFill style={{alignItems: 'center', justifyContent: 'center', paddingTop: 140 * u}}>
        <FloatingCard delay={4} tiltX={8} tiltY={-8} style={{display: 'flex', flexDirection: portrait ? 'column' : 'row', gap: 40 * u, padding: 40 * u}}>
          <div>
            <div style={{fontFamily: F.ui, fontSize: 20 * u, color: '#888', letterSpacing: '0.14em', textTransform: 'uppercase'}}>Best lap by session</div>
            <div style={{fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', fontSize: 72 * u, color: '#111', fontVariantNumeric: 'tabular-nums'}}>{fmt(LAPS[shown])}</div>
            <svg width={cw * u} height={(ch + 20) * u} viewBox={`-10 -10 ${cw + 20} ${ch + 20}`}>
              {[0, 1, 2, 3].map((g) => (
                <line key={g} x1={0} x2={cw} y1={(g * ch) / 3} y2={(g * ch) / 3} stroke={C.line} strokeWidth={2} />
              ))}
              <path d={d} stroke={C.red} strokeWidth={6} fill="none" strokeLinecap="round" strokeLinejoin="round" strokeDasharray={len} strokeDashoffset={len * (1 - draw)} />
              {up.map(([x, y], i) => (i <= shown ? <circle key={i} cx={x} cy={y} r={9} fill="#fff" stroke={C.red} strokeWidth={5} /> : null))}
            </svg>
            <div style={{fontFamily: F.ui, fontSize: 16 * u, color: '#aaa'}}>Illustrative data</div>
          </div>
          <div style={{display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 18 * u, width: (portrait ? cw : 420) * u}}>
            <div style={{fontFamily: F.ui, fontWeight: 700, fontSize: 20 * u, color: C.red, letterSpacing: '0.14em', textTransform: 'uppercase'}}>Coaching notes</div>
            {NOTES.map((n, i) => {
              const t = f - 34 - i * 8;
              return (
                <div key={n} style={{fontFamily: F.head, fontWeight: 700, fontSize: 30 * u, color: '#111', opacity: interpolate(t, [0, 6], [0, 1], clamp), transform: `translateX(${interpolate(t, [0, 8], [20, 0], clamp) * u}px)`, borderLeft: `${5 * u}px solid ${C.red}`, paddingLeft: 16 * u}}>
                  {n}
                </div>
              );
            })}
          </div>
        </FloatingCard>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
