import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Background} from '../primitives/Background';
import {Center} from '../primitives/Bits';
import {TachCounter} from '../primitives/Counter';
import {useLayout} from '../primitives/layout';
import {SceneProps} from './types';

// 3. Tach-style counter rolls to 400,000+ ("Over 400,000 Alumni", skipbarber.com home page).
export const S03Counter: React.FC<SceneProps> = ({dur}) => {
  const {portrait} = useLayout();
  return (
    <AbsoluteFill>
      <Background kind="black" />
      <Center>
        <TachCounter value={400000} label="Skip Barber alumni" start={3} dur={Math.min(52, dur - 18)} size={portrait ? 960 : 860} />
      </Center>
    </AbsoluteFill>
  );
};
