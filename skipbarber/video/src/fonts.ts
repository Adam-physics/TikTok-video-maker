import '@fontsource/inter-tight/500.css';
import '@fontsource/inter-tight/700.css';
import '@fontsource/inter-tight/800.css';
import '@fontsource/inter-tight/900.css';
import '@fontsource/inter-tight/800-italic.css';
import '@fontsource/inter-tight/900-italic.css';
import '@fontsource/instrument-serif/400-italic.css';
import '@fontsource/source-sans-3/300.css';
import '@fontsource/source-sans-3/400.css';
import '@fontsource/inter/400.css';
import '@fontsource/inter/500.css';
import '@fontsource/inter/600.css';
import '@fontsource/inter/700.css';
import {continueRender, delayRender} from 'remotion';

const faces = [
  '500 40px "Inter Tight"', '700 40px "Inter Tight"', '800 40px "Inter Tight"', '900 40px "Inter Tight"',
  'italic 800 40px "Inter Tight"', 'italic 900 40px "Inter Tight"', 'italic 400 40px "Instrument Serif"',
  '300 40px "Source Sans 3"', '400 40px "Source Sans 3"',
  '400 40px Inter', '500 40px Inter', '600 40px Inter', '700 40px Inter',
];

if (typeof document !== 'undefined') {
  const handle = delayRender('fonts');
  Promise.all(faces.map((f) => document.fonts.load(f)))
    .then(() => document.fonts.ready)
    .then(() => continueRender(handle))
    .catch(() => continueRender(handle));
}
