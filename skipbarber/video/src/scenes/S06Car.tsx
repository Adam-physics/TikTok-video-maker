import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {P, SFX} from '../assets';
import {Background} from '../primitives/Background';
import {Cursor} from '../primitives/Cursor';
import {FloatingCard} from '../primitives/FloatingCard';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {clamp, pop} from '../primitives/motion';
import {Thumb} from '../primitives/Photo';
import {Sfx} from '../primitives/Sfx';
import {C, F} from '../theme';
import {SceneProps} from './types';

// 6. "Pick your car." Specs quoted from /gt-car, /formula-car and /gtx.
const CARS = [
  {name: 'Skip Barber GT', sub: 'Built from a road-going Ford Mustang', photo: P.gtTrack2},
  {name: 'Skip Barber Formula', sub: 'Mygale FIA F4. 60 mph in under 4 seconds', photo: P.f4Track},
  {name: 'Skip Barber GTX', sub: 'Stock car. 700 hp Ilmor V8', photo: P.gtx},
];
const PICK = 1;

export const S06Car: React.FC<SceneProps> = ({dur}) => {
  const f = useCurrentFrame();
  const {fps, portrait, u, width, height} = useLayout();
  const clickAt = Math.round(dur * 0.58);
  const sel = pop(f, fps, clickAt, 14, 220);
  const cardW = portrait ? 860 : 520;
  const thumbH = portrait ? 250 : 300;
  // Cursor path, in 1080-short-side units.
  const W = width / u;
  const H = height / u;
  const target = portrait ? {x: W / 2 + 200, y: H * 0.5 + 60} : {x: W / 2 + 120, y: H * 0.58 + 40};
  return (
    <AbsoluteFill>
      <Background kind="white" />
      <div style={{position: 'absolute', top: (portrait ? 230 : 110) * u, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Headline text="Pick your *car*." color="#111" size={portrait ? 112 : 100} delay={1} stagger={3} />
      </div>
      <div
        style={{
          position: 'absolute', inset: 0, top: (portrait ? 220 : 170) * u, display: 'flex', flexDirection: portrait ? 'column' : 'row',
          alignItems: 'center', justifyContent: 'center', gap: (portrait ? 34 : 40) * u,
        }}
      >
        {CARS.map((c, i) => {
          const chosen = i === PICK;
          const dim = interpolate(sel, [0, 1], [1, chosen ? 1 : 0.45]);
          const grow = chosen ? interpolate(sel, [0, 1], [1, 1.05]) : interpolate(sel, [0, 1], [1, 0.97]);
          return (
            <div key={c.name} style={{opacity: dim, transform: `scale(${grow})`}}>
              <FloatingCard delay={8 + i * 4} tiltX={10} tiltY={(i - 1) * -8} width={cardW} style={{padding: 18 * u, outline: chosen && sel > 0.05 ? `${4 * u}px solid ${C.red}` : 'none', display: portrait ? 'flex' : 'block', gap: 24 * u, alignItems: 'center'}}>
                <Thumb file={c.photo} w={(portrait ? 330 : cardW - 36) * u} h={(portrait ? 220 : thumbH) * u} />
                <div style={{padding: `${(portrait ? 0 : 20) * u}px ${8 * u}px ${8 * u}px`}}>
                  <div style={{fontFamily: F.head, fontWeight: 800, fontSize: 38 * u, letterSpacing: '-0.02em'}}>{c.name}</div>
                  <div style={{fontFamily: F.ui, fontSize: 24 * u, color: '#555', marginTop: 8 * u, lineHeight: 1.3}}>{c.sub}</div>
                  {chosen ? (
                    <div style={{marginTop: 14 * u, display: 'inline-block', padding: `${6 * u}px ${16 * u}px`, borderRadius: 999, background: C.red, color: '#fff', fontFamily: F.ui, fontWeight: 700, fontSize: 20 * u, opacity: interpolate(sel, [0, 0.5], [0, 1], clamp), transform: `scale(${interpolate(sel, [0, 1], [0.6, 1])})`}}>
                      Selected &#10003;
                    </div>
                  ) : null}
                </div>
              </FloatingCard>
            </div>
          );
        })}
      </div>
      <Cursor
        path={[
          {f: clickAt - 26, x: W * 0.78, y: H * 0.95},
          {f: clickAt - 4, x: target.x, y: target.y},
          {f: dur, x: target.x + 30, y: target.y + 20},
        ]}
        clicks={[clickAt]}
      />
      <Sfx file={SFX.click} at={clickAt} volume={0.7} />
    </AbsoluteFill>
  );
};
