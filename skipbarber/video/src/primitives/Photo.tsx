import React from 'react';
import {AbsoluteFill, Img, interpolate, useCurrentFrame, useVideoConfig} from 'remotion';
import {has, src} from '../assets';
import {F} from '../theme';
import {clamp} from './motion';

// A photo that is never static: slow push-in plus a lateral drift, optional speed streaks.
// Missing files render as a labeled placeholder so layouts can be reviewed before assets arrive.
export const Photo: React.FC<{
  file: string;
  from?: number;
  to?: number;
  driftX?: number; // percent of width over the shot
  position?: string; // object-position
  streaks?: boolean;
  darken?: number; // 0..1
  dur?: number; // frames over which the push-in runs
  style?: React.CSSProperties;
}> = ({file, from = 1.06, to = 1.16, driftX = -2.5, position = 'center', streaks = false, darken = 0, dur = 150, style}) => {
  const f = useCurrentFrame();
  const t = interpolate(f, [0, dur], [0, 1], clamp);
  const s = interpolate(t, [0, 1], [from, to]);
  const x = interpolate(t, [0, 1], [0, driftX]);
  return (
    <AbsoluteFill style={{overflow: 'hidden', ...style}}>
      {has(file) ? (
        <Img
          src={src(file)}
          style={{width: '100%', height: '100%', objectFit: 'cover', objectPosition: position, transform: `scale(${s}) translateX(${x}%)`}}
        />
      ) : (
        <Placeholder label={file} s={s} />
      )}
      {streaks ? <Streaks /> : null}
      {darken > 0 ? <AbsoluteFill style={{background: `rgba(0,0,0,${darken})`}} /> : null}
    </AbsoluteFill>
  );
};

const Placeholder: React.FC<{label: string; s: number}> = ({label, s}) => (
  <AbsoluteFill
    style={{
      background: 'repeating-linear-gradient(115deg, #1b1b1f 0 38px, #232329 38px 76px)',
      transform: `scale(${s})`,
      alignItems: 'center',
      justifyContent: 'center',
    }}
  >
    <div style={{fontFamily: F.ui, fontSize: 26, color: '#9aa0aa', border: '2px dashed #555', padding: '14px 22px', borderRadius: 12, background: 'rgba(0,0,0,0.5)'}}>
      PHOTO: {label.replace('photos/', '')}
    </div>
  </AbsoluteFill>
);

// Horizontal light streaks moving left, sells speed on top of panning shots.
const Streaks: React.FC = () => {
  const f = useCurrentFrame();
  const {width, height} = useVideoConfig();
  const lines = Array.from({length: 14}, (_, i) => {
    const seed = Math.sin(i * 91.7) * 0.5 + 0.5;
    const y = ((i * 0.071 + seed * 0.3) % 1) * height;
    const len = 200 + seed * 500;
    const speed = 60 + seed * 70;
    const x = width - ((f * speed + seed * width * 3) % (width + len * 2));
    return (
      <div
        key={i}
        style={{
          position: 'absolute',
          left: x,
          top: y,
          width: len,
          height: 1 + seed * 2.5,
          background: 'linear-gradient(90deg, rgba(255,255,255,0), rgba(255,255,255,0.55), rgba(255,255,255,0))',
          opacity: 0.35 + seed * 0.35,
        }}
      />
    );
  });
  return <AbsoluteFill style={{mixBlendMode: 'screen'}}>{lines}</AbsoluteFill>;
};

// Photo inside a rounded frame, for cards.
export const Thumb: React.FC<{file: string; w: number; h: number; radius?: number; style?: React.CSSProperties}> = ({file, w, h, radius = 16, style}) => (
  <div style={{width: w, height: h, borderRadius: radius, overflow: 'hidden', position: 'relative', flexShrink: 0, ...style}}>
    <Photo file={file} from={1.02} to={1.1} driftX={-1.5} />
  </div>
);
