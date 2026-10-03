import {staticFile} from 'remotion';
import manifest from './manifest.json';

const have = new Set<string>(manifest as string[]);
export const has = (p: string) => have.has(p);
export const src = (p: string) => staticFile(p);

// Photo keys are the filenames from the research top picks (scrape/inventory.md).
export const P = {
  gtTrack: 'photos/mustang-gt-track-03.jpg',
  gtTrack2: 'photos/mustang-gt-track-05.jpg',
  gtLimeRock: 'photos/mustang-gt-limerock-02.jpg',
  f4Track: 'photos/f4-track-02.png',
  f4Cota: 'photos/f4-cota-04.jpg',
  sebringBanner: 'photos/track-sebring-banner.png',
  cockpit: 'photos/cockpit-driving-academy.jpg',
  classroom: 'photos/classroom-01.jpg',
  f4Braking: 'photos/f4-braking-zone-sebring.png',
  gtBraking: 'photos/mustang-gt-braking-01.png',
  gtPack: 'photos/mustang-gt-pack-01.png',
  f4Pack: 'photos/f4-pack-limerock-01.jpg',
  f4SideBySide: 'photos/f4-side-by-side-sebring.jpg',
  vir: 'photos/mustang-gt-vir-01.jpg',
  sonoma: 'photos/track-sonoma-startline.png',
  njmp: 'photos/track-njmp-aerial.png',
  cota: 'photos/track-cota-pitlane.jpg',
  student: 'photos/smiling-student-helmet.png',
  trophy: 'photos/driver-race-gear-trophy.png',
  champagne: 'photos/driver-race-gear-champagne.jpg',
  gtx: 'photos/gtx-stock-car-01.png',
  gtxClose: 'photos/gtx-stock-car-closeup.png',
  fleet: 'photos/fleet-shop-overhead.png',
} as const;

export const LOGO = 'logo/skipbarber-logo.png';
export const MUSIC = 'music/track.mp3';
export const SFX = {
  rev: 'sfx/engine-rev-1.mp3',
  rev2: 'sfx/engine-rev-2.mp3',
  whoosh: 'sfx/whoosh-1.mp3',
  whoosh2: 'sfx/whoosh-2.mp3',
  whooshShort: 'sfx/whoosh-3.mp3',
  click: 'sfx/click.mp3',
} as const;
