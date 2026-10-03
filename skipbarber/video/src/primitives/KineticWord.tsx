import React from 'react';
import {interpolate, useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {useLayout} from './layout';
import {clamp, pop} from './motion';

// One word or short phrase with an Outrank-style entrance.
//  slam:  scales down from big with a motion-blur punch
//  track: letter spacing collapses from wide (Byline's "IS HARD.")
//  blur:  soft blur-in
export const KineticWord: React.FC<{
  text: string;
  mode?: 'slam' | 'track' | 'blur';
  delay?: number;
  size?: number;
  color?: string;
  italic?: boolean;
  weight?: number;
  font?: string;
  style?: React.CSSProperties;
}> = ({text, mode = 'slam', delay = 0, size = 180, color = C.white, italic = true, weight = 900, font = F.slam, style}) => {
  const f = useCurrentFrame();
  const {fps, u} = useLayout();
  const t = f - delay;
  const p = pop(f, fps, delay, 13, 260);
  let transform = '';
  let filter = '';
  let letterSpacing = '-0.02em';
  let opacity = interpolate(t, [0, 2], [0, 1], clamp);
  if (mode === 'slam') {
    const s = interpolate(p, [0, 1], [1.9, 1]);
    transform = `scale(${s}) skewX(${interpolate(p, [0, 1], [-12, 0])}deg)`;
    filter = `blur(${interpolate(t, [0, 5], [10, 0], clamp) * u}px)`;
  } else if (mode === 'track') {
    letterSpacing = `${interpolate(p, [0, 1], [0.9, 0.12])}em`;
    filter = `blur(${interpolate(t, [0, 8], [12, 0], clamp) * u}px)`;
    opacity = interpolate(t, [0, 6], [0, 1], clamp);
  } else {
    filter = `blur(${interpolate(t, [0, 10], [18, 0], clamp) * u}px)`;
    opacity = interpolate(t, [0, 10], [0, 1], clamp);
    transform = `translateY(${interpolate(t, [0, 12], [20, 0], clamp) * u}px)`;
  }
  if (t < 0) opacity = 0;
  return (
    <div
      style={{
        fontFamily: font,
        fontWeight: weight,
        fontStyle: italic ? 'italic' : 'normal',
        fontSize: size * u,
        color,
        lineHeight: 0.95,
        letterSpacing,
        textTransform: 'uppercase',
        whiteSpace: 'nowrap',
        transform,
        filter,
        opacity,
        ...style,
      }}
    >
      {text}
    </div>
  );
};
