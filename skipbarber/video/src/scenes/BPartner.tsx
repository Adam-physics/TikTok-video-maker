import React from 'react';
import {AbsoluteFill} from 'remotion';
import {Background} from '../primitives/Background';
import {Center, ConceptTag} from '../primitives/Bits';
import {FloatingCard} from '../primitives/FloatingCard';
import {useLayout} from '../primitives/layout';
import {F} from '../theme';
import {SceneProps} from './types';

// Placeholder slot for a possible partner pricing message. No partner is named on screen.
export const BPartner: React.FC<SceneProps> = () => {
  const {u} = useLayout();
  return (
    <AbsoluteFill>
      <Background kind="black" />
      <ConceptTag />
      <Center>
        <FloatingCard dark delay={2} tiltX={8} tiltY={-8} width={900} style={{border: `${3 * u}px dashed rgba(255,255,255,0.4)`, textAlign: 'center', padding: 60 * u}}>
          <div style={{fontFamily: F.slam, fontWeight: 900, fontStyle: 'italic', fontSize: 80 * u}}>[PARTNER OFFER]</div>
          <div style={{fontFamily: F.ui, fontSize: 26 * u, color: '#aaa', marginTop: 14 * u}}>Placeholder for a partner pricing message</div>
        </FloatingCard>
      </Center>
    </AbsoluteFill>
  );
};
