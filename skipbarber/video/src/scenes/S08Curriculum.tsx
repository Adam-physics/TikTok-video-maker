import React from 'react';
import {AbsoluteFill, interpolate, Sequence, useCurrentFrame} from 'remotion';
import {P, SFX} from '../assets';
import {Eyebrow} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp, pop} from '../primitives/motion';
import {Photo} from '../primitives/Photo';
import {Sfx} from '../primitives/Sfx';
import {CutFlash} from '../primitives/SpeedLine';
import {C, F} from '../theme';
import {SceneProps} from './types';

// 8. What the Three Day teaches, quoted from /programs:
//  "learn the braking marks, turn-in points, and see the apex of the corner"
//  "our instructors analyze student's techniques, lines, brake and throttle application"
//  "passing exercises, practice race starts, and open-lapping"
const STEPS = [
  {head: '*Learn* the line.', photo: P.classroom, title: 'Classroom and lead-follow', items: ['Braking marks', 'Turn-in points', 'The apex']},
  {head: '*Find* your limit.', photo: P.gtBraking, title: 'Instructor feedback', items: ['Your lines', 'Brake application', 'Throttle application']},
  {head: '*Race*.', photo: P.f4SideBySide, title: 'Racecraft', items: ['Passing exercises', 'Practice race starts', 'Open lapping']},
];

const Step: React.FC<{i: number; len: number}> = ({i, len}) => {
  const f = useCurrentFrame();
  const {fps, portrait, u} = useLayout();
  const s = STEPS[i];
  const p = pop(f, fps, 2, 22, 150);
  const out = interpolate(f, [len - 7, len], [0, 1], clamp);
  // Card flies in from depth on the right and leaves to the left, like Outrank's 3D calendar.
  const rotY = interpolate(p, [0, 1], [-48, -18]) + out * -30;
  const tx = interpolate(p, [0, 1], [700, 0]) - out * 1400;
  const tz = interpolate(p, [0, 1], [-600, 0]);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Photo file={s.photo} dur={len} from={1.05} to={1.15} driftX={i % 2 ? 2 : -2} darken={0.3} />
      <AbsoluteFill style={{background: portrait ? 'linear-gradient(180deg, rgba(0,0,0,0.85) 0%, rgba(0,0,0,0.1) 45%, rgba(0,0,0,0.75) 100%)' : 'linear-gradient(90deg, rgba(0,0,0,0.88) 0%, rgba(0,0,0,0.55) 40%, rgba(0,0,0,0) 70%)'}} />
      <div style={{position: 'absolute', left: (portrait ? 70 : 120) * u, top: (portrait ? 200 : 0) * u, bottom: portrait ? undefined : 0, display: 'flex', flexDirection: 'column', justifyContent: 'center', gap: 22 * u}}>
        <Eyebrow text={`Three Day Racing School  0${i + 1}`} delay={2} />
        <Headline shadow text={s.head} size={portrait ? 120 : 132} align="left" delay={3} stagger={4} exitAt={len - 8} />
      </div>
      <div style={{position: 'absolute', right: portrait ? 70 * u : 140 * u, left: portrait ? 70 * u : undefined, justifyContent: 'center', bottom: portrait ? 300 * u : undefined, top: portrait ? undefined : 0, height: portrait ? undefined : '100%', display: 'flex', alignItems: 'center', perspective: 1600 * u}}>
        <div
          style={{
            width: (portrait ? 800 : 540) * u, background: '#fff', borderRadius: 26 * u, padding: 36 * u,
            transform: `translateX(${tx * u}px) translateZ(${tz * u}px) rotateY(${rotY}deg) rotateX(6deg)`,
            boxShadow: `0 ${40 * u}px ${120 * u}px rgba(0,0,0,0.55)`, opacity: interpolate(p, [0, 0.2], [0, 1], clamp),
          }}
        >
          <div style={{fontFamily: F.ui, fontWeight: 700, fontSize: 20 * u, color: C.red, letterSpacing: '0.16em', textTransform: 'uppercase'}}>{s.title}</div>
          {s.items.map((it, k) => {
            const t = f - 9 - k * 4;
            return (
              <div key={it} style={{display: 'flex', alignItems: 'center', gap: 18 * u, marginTop: 22 * u, opacity: interpolate(t, [0, 6], [0, 1], clamp), transform: `translateX(${interpolate(t, [0, 8], [24, 0], clamp) * u}px)`}}>
                <div style={{width: 34 * u, height: 34 * u, borderRadius: 10 * u, background: C.red, color: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 22 * u, fontFamily: F.ui, fontWeight: 700}}>&#10003;</div>
                <div style={{fontFamily: F.head, fontWeight: 700, fontSize: 36 * u, color: '#111', letterSpacing: '-0.01em'}}>{it}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const S08Curriculum: React.FC<SceneProps> = ({dur}) => {
  const len = Math.floor(dur / 3);
  return (
    <AbsoluteFill>
      {STEPS.map((_, i) => (
        <Sequence key={i} from={i * len} durationInFrames={i === 2 ? dur - 2 * len : len}>
          <Step i={i} len={i === 2 ? dur - 2 * len : len} />
          {i === 2 ? <CutFlash len={9} /> : null}
          <Sfx file={i === 2 ? SFX.whoosh : SFX.whoosh2} at={0} volume={i === 2 ? 0.5 : 0.35} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};
