import React from 'react';
import {AbsoluteFill, Easing, interpolate, useCurrentFrame} from 'remotion';
import {Background} from '../primitives/Background';
import {FloatingCard} from '../primitives/FloatingCard';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp} from '../primitives/motion';
import {C, F} from '../theme';
import {SceneProps} from './types';

// 7. "Pick your path." Program copy from /programs.
export const PROGRAMS = [
  {name: 'One Day', full: 'Racing School', note: 'Classroom, then lead-follow laps on track.', tag: ''},
  {name: 'Three Day', full: 'Racing School', note: 'The path toward an SCCA or USAC racing license.', tag: 'Most popular'},
  {name: 'Two Day', full: 'Advanced Racing School', note: 'For Three Day graduates and experienced drivers.', tag: ''},
];

// Shared with the Version B "personalized path" scene.
export const PathGraph: React.FC<{dur: number; youAreHere?: number; suggest?: number; startDelay?: number}> = ({dur, youAreHere, suggest, startDelay = 10}) => {
  const f = useCurrentFrame();
  const {portrait, u, width, height} = useLayout();
  const W = width / u;
  const H = height / u;
  // Rising positions, like a chart climbing left to right (bottom to top in portrait).
  const pts = portrait
    ? [{x: W / 2, y: H * 0.8}, {x: W / 2, y: H * 0.56}, {x: W / 2, y: H * 0.32}]
    : [{x: W * 0.2, y: H * 0.8}, {x: W * 0.5, y: H * 0.69}, {x: W * 0.8, y: H * 0.58}];
  const draw = interpolate(f, [startDelay, startDelay + Math.min(40, dur * 0.4)], [0, 1], {...clamp, easing: Easing.bezier(0.6, 0, 0.2, 1)});
  const d = `M ${pts[0].x} ${pts[0].y} L ${pts[1].x} ${pts[1].y} L ${pts[2].x} ${pts[2].y}`;
  const len = pts.slice(1).reduce((a, p, i) => a + Math.hypot(p.x - pts[i].x, p.y - pts[i].y), 0);
  return (
    <AbsoluteFill>
      <svg width={width} height={height} viewBox={`0 0 ${W} ${H}`} style={{position: 'absolute'}}>
        <path d={d} stroke="rgba(255,255,255,0.18)" strokeWidth={4} fill="none" strokeDasharray="10 12" />
        <path d={d} stroke="#fff" strokeWidth={5} fill="none" strokeDasharray={len} strokeDashoffset={len * (1 - draw)} strokeLinecap="round" style={{filter: 'drop-shadow(0 0 10px rgba(255,255,255,0.7))'}} />
      </svg>
      {PROGRAMS.map((p, i) => {
        const at = i / 2;
        const lit = draw >= at - 0.001;
        const cardDelay = startDelay + Math.round(at * Math.min(40, dur * 0.4));
        const isHere = youAreHere === i;
        const isNext = suggest === i;
        return (
          <div key={p.name} style={{position: 'absolute', left: pts[i].x * u, top: pts[i].y * u, transform: 'translate(-50%, -50%)'}}>
            <div style={{position: 'absolute', left: '50%', top: '50%', width: 26 * u, height: 26 * u, marginLeft: -13 * u, marginTop: -13 * u, borderRadius: '50%', background: lit ? '#fff' : 'rgba(255,255,255,0.3)', boxShadow: lit ? `0 0 ${24 * u}px #fff` : 'none'}} />
            <div style={{position: 'absolute', left: portrait ? 60 * u : -200 * u, top: portrait ? -110 * u : -310 * u, width: (portrait ? 560 : 400) * u}}>
              <FloatingCard delay={cardDelay} tiltX={8} tiltY={portrait ? -6 : -4} width={portrait ? 560 : 400} style={{padding: 28 * u, outline: isNext ? `${4 * u}px solid ${C.red}` : 'none'}}>
                {p.tag || isNext ? (
                  <div style={{display: 'inline-block', marginBottom: 12 * u, padding: `${5 * u}px ${14 * u}px`, borderRadius: 999, background: C.red, color: '#fff', fontFamily: F.ui, fontWeight: 700, fontSize: 18 * u, letterSpacing: '0.06em', textTransform: 'uppercase'}}>
                    {isNext ? 'Suggested next' : p.tag}
                  </div>
                ) : null}
                <div style={{fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', fontSize: 50 * u, lineHeight: 1, letterSpacing: '-0.02em', textTransform: 'uppercase'}}>{p.name}</div>
                <div style={{fontFamily: F.head, fontWeight: 700, fontSize: 24 * u, color: '#444', marginTop: 6 * u}}>{p.full}</div>
                <div style={{fontFamily: F.ui, fontSize: 21 * u, color: '#666', marginTop: 12 * u, lineHeight: 1.35}}>{p.note}</div>
              </FloatingCard>
            </div>
            {isHere ? <YouAreHere delay={cardDelay + 12} /> : null}
          </div>
        );
      })}
    </AbsoluteFill>
  );
};

const YouAreHere: React.FC<{delay: number}> = ({delay}) => {
  const f = useCurrentFrame();
  const {u} = useLayout();
  const o = interpolate(f - delay, [0, 8], [0, 1], clamp);
  const ring = ((f - delay) % 30) / 30;
  return (
    <div style={{position: 'absolute', left: 0, top: 0, opacity: o}}>
      <div style={{position: 'absolute', left: -40 * u * (1 + ring), top: -40 * u * (1 + ring), width: 80 * u * (1 + ring), height: 80 * u * (1 + ring), borderRadius: '50%', border: `${3 * u}px solid ${C.red}`, opacity: 1 - ring}} />
      <div style={{position: 'absolute', left: -110 * u, top: 40 * u, width: 220 * u, textAlign: 'center', fontFamily: F.ui, fontWeight: 700, fontSize: 22 * u, color: '#fff', background: C.red, borderRadius: 999, padding: `${8 * u}px 0`}}>You are here</div>
    </div>
  );
};

export const S07Path: React.FC<SceneProps> = ({dur}) => {
  const {portrait, u} = useLayout();
  return (
    <AbsoluteFill>
      <Background kind="red" />
      <div style={{position: 'absolute', top: (portrait ? 150 : 90) * u, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Headline text="Pick your *path*." size={portrait ? 112 : 100} accentColor="#fff" delay={1} />
      </div>
      <PathGraph dur={dur} />
    </AbsoluteFill>
  );
};
