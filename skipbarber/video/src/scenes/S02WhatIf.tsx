import React from 'react';
import {AbsoluteFill} from 'remotion';
import {P} from '../assets';
import {Center} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {Photo} from '../primitives/Photo';
import {SceneProps} from './types';

// 2. Words blur in over a panning-blur Mustang shot.
export const S02WhatIf: React.FC<SceneProps> = ({dur}) => {
  const {portrait} = useLayout();
  return (
    <AbsoluteFill style={{background: '#000'}}>
      <Photo file={P.gtTrack} dur={dur} from={1.12} to={1.24} driftX={-4} streaks darken={0.42} position={portrait ? '40% center' : 'center'} />
      <AbsoluteFill style={{background: 'radial-gradient(80% 70% at 50% 50%, rgba(0,0,0,0.35), rgba(0,0,0,0) 70%)'}} />
      <Center>
        <Headline shadow text={'What if you learned\nwhere *champions* learned?'} size={portrait ? 88 : 104} delay={2} stagger={4} />
      </Center>
    </AbsoluteFill>
  );
};
