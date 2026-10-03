import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {useLayout} from './layout';
import {clamp, pop} from './motion';

export const Center: React.FC<{children: React.ReactNode; style?: React.CSSProperties}> = ({children, style}) => (
  <div style={{position: 'absolute', inset: 0, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', ...style}}>{children}</div>
);

// Pill CTA button that presses when clicked.
export const Pill: React.FC<{label: string; delay?: number; clickAt?: number; size?: number}> = ({label, delay = 0, clickAt, size = 40}) => {
  const f = useCurrentFrame();
  const {fps, u} = useLayout();
  const p = pop(f, fps, delay, 15, 200);
  const press = clickAt !== undefined ? interpolate(f, [clickAt - 2, clickAt, clickAt + 5], [1, 0.93, 1], clamp) : 1;
  const lit = clickAt !== undefined && f >= clickAt;
  return (
    <div
      style={{
        display: 'inline-flex', alignItems: 'center', gap: 16 * u,
        padding: `${size * 0.55 * u}px ${size * 1.1 * u}px`, borderRadius: 999,
        background: lit ? C.red : '#fff', color: lit ? '#fff' : C.red,
        fontFamily: F.ui, fontWeight: 700, fontSize: size * u, letterSpacing: '0.02em',
        transform: `scale(${interpolate(p, [0, 1], [0.6, 1]) * press})`, opacity: interpolate(p, [0, 0.3], [0, 1], clamp),
        boxShadow: lit ? `0 0 ${60 * u}px rgba(255,0,0,0.7)` : `0 ${20 * u}px ${60 * u}px rgba(0,0,0,0.4)`,
      }}
    >
      {label}
      <span style={{fontSize: size * 0.9 * u}}>&rarr;</span>
    </div>
  );
};

// Small chip, used for track names and spec tags.
export const Chip: React.FC<{label: string; delay?: number; dark?: boolean; size?: number}> = ({label, delay = 0, dark = true, size = 30}) => {
  const f = useCurrentFrame();
  const {fps, u} = useLayout();
  const p = pop(f, fps, delay, 12, 240);
  return (
    <div
      style={{
        padding: `${size * 0.45 * u}px ${size * 0.85 * u}px`, borderRadius: 999,
        background: dark ? 'rgba(10,10,10,0.72)' : '#fff', color: dark ? '#fff' : '#111',
        border: dark ? `1px solid rgba(255,255,255,0.22)` : `1px solid ${C.line}`,
        backdropFilter: 'blur(8px)', fontFamily: F.ui, fontWeight: 600, fontSize: size * u, whiteSpace: 'nowrap',
        transform: `scale(${interpolate(p, [0, 1], [0.4, 1])}) translateY(${interpolate(p, [0, 1], [20, 0])}px)`,
        opacity: interpolate(p, [0, 0.2], [0, 1], clamp),
      }}
    >
      <span style={{color: C.red, marginRight: 10 * u}}>&#9679;</span>
      {label}
    </div>
  );
};

// "Concept preview" tag for the Version B AI scenes.
export const ConceptTag: React.FC = () => {
  const {u} = useLayout();
  return (
    <div style={{position: 'absolute', top: 44 * u, right: 48 * u, padding: `${10 * u}px ${20 * u}px`, borderRadius: 999, border: '1.5px solid rgba(255,255,255,0.55)', background: 'rgba(0,0,0,0.45)', color: '#fff', fontFamily: F.ui, fontWeight: 600, fontSize: 22 * u, letterSpacing: '0.12em', textTransform: 'uppercase'}}>
      Concept preview
    </div>
  );
};

export const Eyebrow: React.FC<{text: string; color?: string; delay?: number}> = ({text, color = C.red, delay = 0}) => {
  const f = useCurrentFrame();
  const {u} = useLayout();
  return (
    <div style={{fontFamily: F.ui, fontWeight: 700, fontSize: 24 * u, letterSpacing: '0.22em', textTransform: 'uppercase', color, opacity: interpolate(f - delay, [0, 8], [0, 1], clamp)}}>{text}</div>
  );
};
