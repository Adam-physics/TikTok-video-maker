import {useVideoConfig} from 'remotion';

// Sizes are authored for a 1080px short side, so u === 1 in both 1920x1080 and 1080x1920.
export const useLayout = () => {
  const {width, height, fps} = useVideoConfig();
  const portrait = height > width;
  const u = Math.min(width, height) / 1080;
  return {width, height, fps, portrait, u};
};
