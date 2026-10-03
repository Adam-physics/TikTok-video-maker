import React from 'react';
import {Easing, interpolate, useCurrentFrame} from 'remotion';
import {useLayout} from './layout';
import {clamp} from './motion';

export type CursorKey = {f: number; x: number; y: number};

// Arrow cursor that eases between keyframes (in px of a 1080-short-side layout) and clicks
// with a ripple at each frame listed in `clicks`.
export const Cursor: React.FC<{path: CursorKey[]; clicks?: number[]; color?: string}> = ({path, clicks = [], color = '#111'}) => {
  const f = useCurrentFrame();
  const {u} = useLayout();
  const frames = path.map((k) => k.f);
  const opt = {...clamp, easing: Easing.bezier(0.65, 0, 0.35, 1)};
  const x = interpolate(f, frames, path.map((k) => k.x), opt);
  const y = interpolate(f, frames, path.map((k) => k.y), opt);
  const show = interpolate(f, [frames[0], frames[0] + 5], [0, 1], clamp);
  const press = clicks.reduce((acc, c) => acc * (1 - 0.18 * interpolate(f, [c - 2, c, c + 4], [0, 1, 0], clamp)), 1);
  return (
    <div style={{position: 'absolute', left: x * u, top: y * u, opacity: show, pointerEvents: 'none'}}>
      {clicks.map((c) => {
        const t = f - c;
        if (t < 0 || t > 18) return null;
        const r = interpolate(t, [0, 18], [6, 70], clamp) * u;
        return (
          <div
            key={c}
            style={{
              position: 'absolute', left: -r, top: -r, width: r * 2, height: r * 2, borderRadius: '50%',
              border: `${3 * u}px solid rgba(255,0,0,${interpolate(t, [0, 18], [0.8, 0], clamp)})`,
            }}
          />
        );
      })}
      <svg width={40 * u} height={48 * u} viewBox="0 0 20 24" style={{transform: `scale(${press})`, transformOrigin: '0 0', filter: 'drop-shadow(0 3px 6px rgba(0,0,0,0.35))'}}>
        <path d="M1 1 L1 19 L6 14.5 L9.5 22 L12.5 20.7 L9 13.3 L16 13.3 Z" fill={color} stroke="#fff" strokeWidth="1.6" strokeLinejoin="round" />
      </svg>
    </div>
  );
};
