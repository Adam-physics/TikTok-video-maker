import React from 'react';
import {Easing, interpolate, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {useLayout} from './layout';
import {clamp} from './motion';

// Tachometer-style ring counter (brand take on Byline's review ring). The needle sweeps
// into the redline as the number rolls up.
export const TachCounter: React.FC<{
  value: number;
  suffix?: string;
  label: string;
  start?: number;
  dur?: number;
  size?: number;
}> = ({value, suffix = '+', label, start = 0, dur = 50, size = 640}) => {
  const f = useCurrentFrame();
  const {u} = useLayout();
  const p = interpolate(f, [start, start + dur], [0, 1], {...clamp, easing: Easing.bezier(0.3, 0, 0.1, 1)});
  const appear = interpolate(f, [start - 8, start + 4], [0, 1], clamp);
  const a0 = 135;
  const sweep = 270;
  const ang = a0 + sweep * p * 0.93;
  const R = 470;
  const pt = (deg: number, r: number) => {
    const rad = (deg * Math.PI) / 180;
    return [540 + r * Math.cos(rad), 540 + r * Math.sin(rad)];
  };
  const arc = (from: number, to: number, r: number) => {
    const [x1, y1] = pt(from, r);
    const [x2, y2] = pt(to, r);
    return `M ${x1} ${y1} A ${r} ${r} 0 ${to - from > 180 ? 1 : 0} 1 ${x2} ${y2}`;
  };
  const ticks = Array.from({length: 41}, (_, i) => {
    const d = a0 + (sweep * i) / 40;
    const major = i % 5 === 0;
    const [x1, y1] = pt(d, R - 30);
    const [x2, y2] = pt(d, R - (major ? 74 : 52));
    const red = i >= 34;
    const lit = d <= ang;
    return <line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={red ? C.red : lit ? '#fff' : '#3a3a3a'} strokeWidth={major ? 6 : 3} strokeLinecap="round" />;
  });
  const n = Math.round(value * p);
  const done = p > 0.995;
  return (
    <div style={{position: 'relative', width: size * u, height: size * u, opacity: appear, transform: `scale(${interpolate(appear, [0, 1], [0.92, 1])})`}}>
      <svg viewBox="0 0 1080 1080" width="100%" height="100%">
        <defs>
          <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
            <feGaussianBlur stdDeviation="10" result="b" />
            <feMerge><feMergeNode in="b" /><feMergeNode in="SourceGraphic" /></feMerge>
          </filter>
        </defs>
        <path d={arc(a0, a0 + sweep, R)} stroke="#262626" strokeWidth={14} fill="none" strokeLinecap="round" />
        <path d={arc(a0, Math.max(a0 + 0.1, ang), R)} stroke={C.red} strokeWidth={14} fill="none" strokeLinecap="round" filter="url(#glow)" />
        {ticks}
      </svg>
      <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center'}}>
        <div style={{fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', fontSize: size * 0.135 * u, color: '#fff', letterSpacing: '-0.03em', fontVariantNumeric: 'tabular-nums'}}>
          {n.toLocaleString('en-US')}
          <span style={{color: C.red, opacity: done ? 1 : 0}}>{suffix}</span>
        </div>
        <div style={{fontFamily: F.ui, fontWeight: 500, fontSize: size * 0.036 * u, color: '#c9c9c9', marginTop: 6 * u, letterSpacing: '0.02em'}}>{label}</div>
      </div>
    </div>
  );
};
