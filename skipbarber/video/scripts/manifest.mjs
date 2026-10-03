// Lists what is actually in public/ so scenes can fall back to labeled placeholders
// for photos, logo, music or sound effects that have not been supplied yet.
import fs from 'fs';
import path from 'path';
const root = new URL('../public/', import.meta.url).pathname;
const walk = (d) => fs.readdirSync(d, {withFileTypes: true}).flatMap((e) =>
  e.isDirectory() ? walk(path.join(d, e.name)) : [path.relative(root, path.join(d, e.name))]);
const files = walk(root).filter((f) => !f.startsWith('.') && !f.endsWith('.gitkeep')).sort();
fs.writeFileSync(new URL('../src/manifest.json', import.meta.url), JSON.stringify(files, null, 1) + '\n');
console.log(`manifest: ${files.length} files`);
