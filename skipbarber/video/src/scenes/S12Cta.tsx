import React from 'react';
import {AbsoluteFill} from 'remotion';
import {P, SFX} from '../assets';
import {Background} from '../primitives/Background';
import {Center, Pill} from '../primitives/Bits';
import {Cursor} from '../primitives/Cursor';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {Photo} from '../primitives/Photo';
import {Sfx} from '../primitives/Sfx';
import {SceneProps} from './types';

// 12. CTA. "Lock in your spot" is the site's own button copy ("LOCK IN YOUR SPOT!").
export const S12Cta: React.FC<SceneProps> = ({dur}) => {
  const {portrait, u, width, height} = useLayout();
  const clickAt = Math.round(dur * 0.62);
  const W = width / u;
  const H = height / u;
  const btn = {x: W / 2 + 40, y: H / 2 + (portrait ? 110 : 100)};
  return (
    <AbsoluteFill>
      <Background kind="black" />
      <Photo file={P.fleet} dur={dur} from={1.1} to={1.2} darken={0.78} />
      <Center style={{gap: 60 * u}}>
        <Headline text="Get on *track*." size={portrait ? 140 : 150} delay={1} stagger={4} />
        <Pill label="Lock in your spot" delay={12} clickAt={clickAt} size={portrait ? 44 : 40} />
      </Center>
      <Cursor color="#fff" path={[{f: clickAt - 24, x: W * 0.72, y: H * 0.86}, {f: clickAt - 3, x: btn.x, y: btn.y}, {f: dur, x: btn.x + 12, y: btn.y + 10}]} clicks={[clickAt]} />
      <Sfx file={SFX.click} at={clickAt} volume={0.7} />
    </AbsoluteFill>
  );
};
