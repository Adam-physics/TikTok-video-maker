import React from 'react';
import {AbsoluteFill, interpolate, useCurrentFrame} from 'remotion';
import {Background} from '../primitives/Background';
import {Center} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {Logo} from '../primitives/Logo';
import {useLayout} from '../primitives/layout';
import {clamp} from '../primitives/motion';
import {C, F} from '../theme';
import {SceneProps} from './types';

// 13. End card. /VIR: "the world's largest racing school".
export const S13End: React.FC<SceneProps & {partnerTag?: boolean}> = ({dur, partnerTag}) => {
  const f = useCurrentFrame();
  const {portrait, u} = useLayout();
  const fade = interpolate(f, [dur - 20, dur], [1, 0], clamp);
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <AbsoluteFill style={{opacity: fade}}>
        <Background kind="black" />
        <Center style={{gap: 34 * u}}>
          <Logo delay={0} width={portrait ? 640 : 520} />
          <Headline text="The world's largest *racing school*." size={portrait ? 60 : 54} weight={500} delay={12} stagger={3} maxWidth={portrait ? 900 : 1500} />
          <div style={{fontFamily: F.head, fontWeight: 800, fontSize: (portrait ? 56 : 50) * u, color: '#fff', letterSpacing: '0.01em', opacity: interpolate(f, [26, 34], [0, 1], clamp)}}>
            skipbarber<span style={{color: C.red}}>.com</span>
          </div>
          {partnerTag ? (
            <div style={{fontFamily: F.ui, fontSize: 22 * u, color: '#8a8a8a', letterSpacing: '0.08em', opacity: interpolate(f, [36, 44], [0, 1], clamp)}}>AI by Arsenal Digital Holdings</div>
          ) : null}
        </Center>
      </AbsoluteFill>
    </AbsoluteFill>
  );
};
