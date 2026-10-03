import React from 'react';
import {AbsoluteFill} from 'remotion';
import {SFX} from '../assets';
import {Background} from '../primitives/Background';
import {Center} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {Logo} from '../primitives/Logo';
import {useLayout} from '../primitives/layout';
import {Sfx} from '../primitives/Sfx';
import {SpeedLine} from '../primitives/SpeedLine';
import {SceneProps} from './types';

// 4. Logo lockup on the drop. "Since 1975." (skipbarber.com: "In 1975, racing legend Skip Barber founded a school...")
export const S04Logo: React.FC<SceneProps> = () => {
  const {portrait, u} = useLayout();
  return (
    <AbsoluteFill>
      <Background kind="black" />
      <SpeedLine delay={0} dur={14} y={0.5} tilt={0} thickness={2} />
      <Center style={{gap: 40 * u}}>
        <Logo delay={2} width={portrait ? 680 : 620} />
        <Headline text="Since *1975*." size={portrait ? 64 : 58} weight={500} delay={16} stagger={4} />
      </Center>
      <Sfx file={SFX.whoosh} at={0} volume={0.5} />
    </AbsoluteFill>
  );
};
