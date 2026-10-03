import React from 'react';
import {useCurrentFrame} from 'remotion';
import {C, F} from '../theme';
import {useLayout} from './layout';
import {clamp, ease} from './motion';
import {interpolate} from 'remotion';

// AccentHeadline: sans headline where words wrapped in *asterisks* become the italic serif
// accent (Byline's "Pick your *topic*." pattern). Words blur in one at a time.
export const Headline: React.FC<{
  text: string;
  size?: number;
  color?: string;
  accentColor?: string;
  delay?: number;
  stagger?: number;
  exitAt?: number; // frame at which words blur back out
  align?: 'center' | 'left';
  weight?: number;
  maxWidth?: number;
  lineHeight?: number;
  font?: string;
  shadow?: boolean; // soft dark halo for text over photos
}> = ({shadow = false, font = F.head, text, size = 104, color = C.white, accentColor = C.red, delay = 0, stagger = 3, exitAt, align = 'center', weight = 700, maxWidth, lineHeight = 1.08}) => {
  const f = useCurrentFrame();
  const {u, portrait} = useLayout();
  const lines = text.split('\n');
  let idx = 0;
  return (
    <div
      style={{
        fontFamily: font,
        fontWeight: weight,
        fontSize: size * u,
        color,
        lineHeight,
        letterSpacing: '-0.025em',
        textAlign: align,
        maxWidth: (maxWidth ?? (portrait ? 960 : 1600)) * u,
        textShadow: shadow ? `0 ${4 * u}px ${28 * u}px rgba(0,0,0,0.75), 0 0 ${60 * u}px rgba(0,0,0,0.5)` : undefined,
      }}
    >
      {lines.map((line, li) => (
        <div key={li}>
          {line.split(' ').map((raw, wi) => {
            const accent = raw.includes('*');
            const word = raw.replace(/\*/g, '');
            const i = idx++;
            const t = f - delay - i * stagger;
            let o = ease(t, [0, 9]);
            let blur = interpolate(t, [0, 9], [14, 0], clamp);
            let y = interpolate(t, [0, 10], [18, 0], clamp);
            if (exitAt !== undefined) {
              const e = f - exitAt - i * 1.5;
              o *= interpolate(e, [0, 7], [1, 0], clamp);
              blur += interpolate(e, [0, 7], [0, 14], clamp);
            }
            return (
              <span
                key={wi}
                style={{
                  display: 'inline-block',
                  marginRight: '0.24em',
                  opacity: o,
                  filter: `blur(${blur * u}px)`,
                  transform: `translateY(${y * u}px)`,
                  ...(accent
                    ? {fontFamily: F.accent, fontStyle: 'italic', fontWeight: 400, color: accentColor, fontSize: '1.14em', letterSpacing: '-0.01em'}
                    : {}),
                }}
              >
                {word}
              </span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
