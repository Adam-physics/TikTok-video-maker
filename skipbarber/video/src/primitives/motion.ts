import {Easing, interpolate, spring} from 'remotion';

export const clamp = {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'} as const;

// Snappy entrance, small overshoot. Used for most slams and card entrances.
export const pop = (frame: number, fps: number, delay = 0, damping = 14, stiffness = 180) =>
  spring({frame: frame - delay, fps, config: {damping, stiffness, mass: 0.8}});

// Calm entrance with no overshoot, for UI cards and headlines.
export const glide = (frame: number, fps: number, delay = 0) =>
  spring({frame: frame - delay, fps, config: {damping: 200, stiffness: 120}});

export const ease = (frame: number, range: [number, number], out: [number, number] = [0, 1]) =>
  interpolate(frame, range, out, {...clamp, easing: Easing.bezier(0.22, 1, 0.36, 1)});

// Fades everything out over the last n frames of a scene.
export const exitOpacity = (frame: number, dur: number, n = 6) =>
  interpolate(frame, [dur - n, dur], [1, 0], clamp);
