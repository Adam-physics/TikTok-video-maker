import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Background} from '../primitives/Background';
import {ConceptTag} from '../primitives/Bits';
import {Headline} from '../primitives/Headline';
import {useLayout} from '../primitives/layout';
import {PathGraph} from './S07Path';
import {SceneProps} from './types';

// B4 (concept). Scene 7's path, now with a "You are here" marker and a suggested next program.
export const B4Path: React.FC<SceneProps> = ({dur}) => {
  const {portrait, u} = useLayout();
  return (
    <AbsoluteFill>
      <Background kind="red" />
      <ConceptTag />
      <div style={{position: 'absolute', top: (portrait ? 150 : 90) * u, width: '100%', display: 'flex', justifyContent: 'center'}}>
        <Headline text="Your path, *personalized*." size={portrait ? 96 : 96} accentColor="#fff" />
      </div>
      <PathGraph dur={dur} youAreHere={0} suggest={1} startDelay={4} />
    </AbsoluteFill>
  );
};
