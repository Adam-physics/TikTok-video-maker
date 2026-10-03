import React from 'react';
import {Img, interpolate, useCurrentFrame} from 'remotion';
import {has, LOGO, src} from '../assets';
import {C, F} from '../theme';
import {useLayout} from './layout';
import {clamp, pop} from './motion';

// Glowing logo lockup on black. Uses the real logo PNG when it is in public/logo, otherwise a
// clearly temporary type-only stand-in.
export const Logo: React.FC<{delay?: number; width?: number; glow?: boolean}> = ({delay = 0, width = 720, glow = true}) => {
  const f = useCurrentFrame();
  const {fps, u} = useLayout();
  const p = pop(f, fps, delay, 16, 140);
  const t = f - delay;
  const blur = interpolate(t, [0, 12], [24, 0], clamp);
  const sweep = interpolate(t, [6, 30], [-30, 130], clamp);
  const pulse = glow ? 0.55 + 0.25 * Math.sin(t / 9) : 0;
  return (
    <div style={{position: 'relative', width: width * u, opacity: interpolate(t, [0, 6], [0, 1], clamp), transform: `scale(${interpolate(p, [0, 1], [1.15, 1])})`, filter: `blur(${blur * u}px)`}}>
      {glow ? (
        <div style={{position: 'absolute', inset: '-25%', background: `radial-gradient(closest-side, rgba(255,0,0,${pulse * 0.55}), rgba(255,0,0,0))`}} />
      ) : null}
      {has(LOGO) ? (
        <Img src={src(LOGO)} style={{width: '100%', position: 'relative'}} />
      ) : (
        <div style={{position: 'relative', textAlign: 'center', fontFamily: F.slam, color: '#fff'}}>
          <div style={{display: 'flex', gap: 10 * u, justifyContent: 'center', marginBottom: 14 * u}}>
            {[0, 1, 2].map((i) => (
              <div key={i} style={{width: 90 * u, height: 12 * u, background: i === 1 ? '#fff' : C.red, transform: 'skewX(-24deg)'}} />
            ))}
          </div>
          <div style={{fontWeight: 900, fontStyle: 'italic', fontSize: 120 * (width / 720) * u, lineHeight: 0.9, letterSpacing: '-0.02em'}}>SKIP BARBER</div>
          <div style={{fontWeight: 700, fontSize: 34 * (width / 720) * u, letterSpacing: '0.42em', marginTop: 12 * u, color: '#ddd'}}>RACING SCHOOL</div>
          <div style={{fontFamily: F.ui, fontSize: 16 * u, color: '#777', marginTop: 10 * u}}>[placeholder until the logo file is supplied]</div>
        </div>
      )}
      <div style={{position: 'absolute', inset: 0, background: `linear-gradient(100deg, rgba(255,255,255,0) ${sweep - 12}%, rgba(255,255,255,0.35) ${sweep}%, rgba(255,255,255,0) ${sweep + 12}%)`, mixBlendMode: 'overlay'}} />
    </div>
  );
};
