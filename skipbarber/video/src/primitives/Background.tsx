import React from 'react';
import {AbsoluteFill, useCurrentFrame} from 'remotion';
import {C} from '../theme';

export type BgKind = 'black' | 'ink' | 'red' | 'white';

// Brand take on Byline's blue gradient: deep red bloom drifting on black.
export const Background: React.FC<{kind: BgKind}> = ({kind}) => {
  const f = useCurrentFrame();
  if (kind === 'white') {
    return (
      <AbsoluteFill style={{background: `radial-gradient(120% 90% at 50% 40%, #FFFFFF 0%, ${C.paper} 70%, #E9EBEF 100%)`}} />
    );
  }
  if (kind === 'red') {
    const x = 70 + Math.sin(f / 40) * 6;
    const y = 80 + Math.cos(f / 50) * 5;
    return (
      <AbsoluteFill
        style={{
          background: `radial-gradient(70% 80% at ${x}% ${y}%, #FF1A1A 0%, #B00000 28%, #3A0000 60%, #070000 100%)`,
        }}
      />
    );
  }
  const base = kind === 'ink' ? C.ink : C.black;
  return (
    <AbsoluteFill
      style={{background: `radial-gradient(90% 70% at 50% 110%, rgba(255,0,0,0.10) 0%, rgba(0,0,0,0) 60%), ${base}`}}
    />
  );
};
