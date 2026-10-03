import React from 'react';
import {AbsoluteFill, Sequence} from 'remotion';
import {SFX} from '../assets';
import {Background} from '../primitives/Background';
import {Center} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {KineticWord} from '../primitives/KineticWord';
import {useLayout} from '../primitives/layout';
import {Sfx} from '../primitives/Sfx';
import {SpeedLine} from '../primitives/SpeedLine';
import {F} from '../theme';
import {SceneProps} from './types';

// 1. "Anyone can drive fast." then a hard cut to "RACING IS HARD."
export const S01Hook: React.FC<SceneProps> = ({dur}) => {
  const {portrait} = useLayout();
  const split = Math.round(dur * 0.48);
  return (
    <AbsoluteFill>
      <Sequence durationInFrames={split}>
        <Background kind="black" />
        <SpeedLine delay={2} dur={26} y={portrait ? 0.6 : 0.64} tilt={-7} />
        <Center>
          <Headline text="Anyone can drive fast." font={F.hero} size={portrait ? 96 : 104} weight={300} delay={4} stagger={4} />
        </Center>
      </Sequence>
      <Sequence from={split}>
        <Background kind="black" />
        <Center style={{gap: 0}}>
          <KineticWord text="Racing" mode="track" size={portrait ? 150 : 170} />
          <KineticWord text="is hard." mode="slam" delay={5} size={portrait ? 190 : 230} color="#FF0000" />
        </Center>
      </Sequence>
      <Sfx file={SFX.rev} at={0} volume={0.55} />
      <Sfx file={SFX.whooshShort} at={split - 2} volume={0.5} />
    </AbsoluteFill>
  );
};
