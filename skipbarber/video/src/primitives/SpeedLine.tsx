import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame, Easing} from 'remotion';
import {C} from '../theme';
import {useLayout} from './layout';
import {clamp} from './motion';

// Thin red light line that sweeps across the frame with a glowing head (the opening shot and
// fast transitions). y is a fraction of frame height.
export const SpeedLine: React.FC<{delay?: number; dur?: number; y?: number; tilt?: number; thickness?: number}> = ({delay = 0, dur = 18, y = 0.5, tilt = -4, thickness = 3}) => {
  const f = useCurrentFrame();
  const {width, height, u} = useLayout();
  const p = interpolate(f, [delay, delay + dur], [0, 1], {...clamp, easing: Easing.bezier(0.7, 0, 0.2, 1)});
  const tail = interpolate(f, [delay + dur * 0.4, delay + dur * 1.6], [0, 1], {...clamp, easing: Easing.bezier(0.5, 0, 0.2, 1)});
  const L = width * 1.4;
  const head = -width * 0.2 + p * L;
  const start = -width * 0.2 + tail * L;
  if (f < delay) return null;
  return (
    <AbsoluteFill style={{transform: `rotate(${tilt}deg)`}}>
      <div
        style={{
          position: 'absolute', top: y * height, left: start, width: Math.max(0, head - start), height: thickness * u,
          background: `linear-gradient(90deg, rgba(255,0,0,0), ${C.red} 70%, #fff)`,
          boxShadow: `0 0 ${18 * u}px ${C.red}, 0 0 ${48 * u}px rgba(255,0,0,0.6)`,
        }}
      />
      <div style={{position: 'absolute', top: y * height - 9 * u, left: head - 9 * u, width: 18 * u, height: 18 * u, borderRadius: '50%', background: '#fff', boxShadow: `0 0 ${30 * u}px ${C.red}`, opacity: p < 1 ? 1 : 0}} />
    </AbsoluteFill>
  );
};

// A few-frame whip at a cut: horizontal smear of red light (Outrank-style transition punch).
export const CutFlash: React.FC<{len?: number}> = ({len = 7}) => {
  const f = useCurrentFrame();
  if (f > len) return null;
  const o = interpolate(f, [0, 1, len], [0.0, 0.9, 0], clamp);
  return (
    <AbsoluteFill style={{pointerEvents: 'none'}}>
      <AbsoluteFill style={{background: 'linear-gradient(90deg, rgba(255,0,0,0) 0%, rgba(255,40,40,0.55) 45%, rgba(255,255,255,0.7) 50%, rgba(255,40,40,0.55) 55%, rgba(255,0,0,0) 100%)', opacity: o, transform: `scaleY(${interpolate(f, [0, len], [0.05, 1.2], clamp)})`}} />
    </AbsoluteFill>
  );
};
