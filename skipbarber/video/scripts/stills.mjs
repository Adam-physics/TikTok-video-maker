// Renders review stills in one bundle. Usage: node scripts/stills.mjs <outDir> <Comp:frame> ...
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import path from 'path';
import fs from 'fs';

const [outDir, ...jobs] = process.argv.slice(2);
fs.mkdirSync(outDir, {recursive: true});
const browserExecutable = '/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell';
const serveUrl = await bundle({entryPoint: path.resolve('src/index.ts')});
const cache = {};
for (const job of jobs) {
  const [id, frameStr, name] = job.split(':');
  const frame = Number(frameStr);
  cache[id] ??= await selectComposition({serveUrl, id, browserExecutable});
  const output = path.join(outDir, `${name ?? `${id}-${frame}`}.png`);
  await renderStill({serveUrl, composition: cache[id], frame, output, browserExecutable});
  console.log('wrote', output);
}
