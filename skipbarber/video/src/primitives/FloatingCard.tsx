import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {useLayout} from './layout';
import {glide} from './motion';

// White UI card with a soft shadow and a slight 3D tilt that settles on a spring, then drifts.
export const FloatingCard: React.FC<{
  delay?: number;
  tiltX?: number;
  tiltY?: number;
  width?: number;
  dark?: boolean;
  style?: React.CSSProperties;
  children: React.ReactNode;
}> = ({delay = 0, tiltX = 14, tiltY = -10, width, dark = false, style, children}) => {
  const f = useCurrentFrame();
  const {fps, u} = useLayout();
  const p = glide(f, fps, delay);
  const drift = (f - delay) / fps;
  const rx = interpolate(p, [0, 1], [tiltX + 22, tiltX * 0.35]) + Math.sin(drift * 0.9) * 1.2;
  const ry = interpolate(p, [0, 1], [tiltY - 14, tiltY * 0.35]) + Math.cos(drift * 0.7) * 1.5;
  const y = interpolate(p, [0, 1], [140, 0]) + Math.sin(drift * 1.1) * 4;
  return (
    <div style={{perspective: 1800 * u, opacity: interpolate(p, [0, 0.25], [0, 1], {extrapolateRight: 'clamp'})}}>
      <div
        style={{
          width: width ? width * u : undefined,
          transform: `translateY(${y * u}px) rotateX(${rx}deg) rotateY(${ry}deg)`,
          background: dark ? 'rgba(20,20,22,0.92)' : '#FFFFFF',
          color: dark ? '#fff' : '#111',
          borderRadius: 28 * u,
          padding: 36 * u,
          boxShadow: dark
            ? `0 ${40 * u}px ${120 * u}px rgba(0,0,0,0.6), 0 0 0 1px rgba(255,255,255,0.08)`
            : `0 ${40 * u}px ${100 * u}px rgba(20,0,0,0.28), 0 ${6 * u}px ${18 * u}px rgba(0,0,0,0.10)`,
          ...style,
        }}
      >
        {children}
      </div>
    </div>
  );
};
