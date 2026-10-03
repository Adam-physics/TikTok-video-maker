import React from 'react';
import {Composition} from 'remotion';
import {Demo} from './Demo';
import {FPS, totalFrames} from './timeline';

export const Root: React.FC = () => (
  <>
    <Composition id="DemoA" component={Demo} defaultProps={{variant: 'A' as const}} durationInFrames={totalFrames('A')} fps={FPS} width={1920} height={1080} />
    <Composition id="DemoB" component={Demo} defaultProps={{variant: 'B' as const}} durationInFrames={totalFrames('B')} fps={FPS} width={1920} height={1080} />
    <Composition id="DemoA9x16" component={Demo} defaultProps={{variant: 'V' as const}} durationInFrames={totalFrames('V')} fps={FPS} width={1080} height={1920} />
    <Composition id="StyleTest" component={Demo} defaultProps={{variant: 'test' as const}} durationInFrames={totalFrames('test')} fps={FPS} width={1920} height={1080} />
  </>
);
