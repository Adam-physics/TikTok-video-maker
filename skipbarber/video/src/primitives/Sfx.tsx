import React from 'react';
import {Audio, Sequence} from 'remotion';
import {has, src} from '../assets';

// Plays a sound effect at a frame offset, only if the file has been supplied.
export const Sfx: React.FC<{file: string; at?: number; volume?: number}> = ({file, at = 0, volume = 0.6}) =>
  has(file) ? (
    <Sequence from={at} layout="none">
      <Audio src={src(file)} volume={volume} />
    </Sequence>
  ) : null;
