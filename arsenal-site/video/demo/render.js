// Renders demo.html to a silent MP4 and writes the list of on-screen sound cues next to it.
// Usage: node render.js <tech|epic> <out.mp4> [fps] [workers]   (serve arsenal-site/ on :8765 first)
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');
const { chromium } = require(process.env.PW || 'playwright');
const URL = v => `http://localhost:8765/video/demo/demo.html?render&v=${v}`;

async function chunk(browser, v, file, from, to, fps) {
  const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto(URL(v)); await p.evaluate(() => window.storyReady);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '17', '-pix_fmt', 'yuv420p', file], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = from; i < to; i++) {
    const b64 = await p.evaluate(t => { renderAt(t); return document.getElementById('c').toDataURL('image/jpeg', .95).slice(23); }, i / fps);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r));
  const events = await p.evaluate(() => Object.values(window.SFX_EVENTS)); await p.close(); return events;
}

(async () => {
  const v = process.argv[2], out = path.resolve(process.argv[3]), fps = +(process.argv[4] || 30), workers = +(process.argv[5] || 3);
  const browser = await chromium.launch();
  const probe = await browser.newPage(); await probe.goto(URL(v)); await probe.evaluate(() => window.storyReady);
  const n = Math.round(await probe.evaluate(() => window.DURATION) * fps); await probe.close();
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'demo-')), per = Math.ceil(n / workers), parts = [], t0 = Date.now();
  const evs = await Promise.all(Array.from({ length: workers }, (_, w) => { const f = path.join(tmp, `p${w}.mp4`); parts.push(f); return chunk(browser, v, f, w * per, Math.min(n, (w + 1) * per), fps); }));
  await browser.close();
  fs.writeFileSync(path.join(tmp, 'l.txt'), parts.map(f => `file '${f}'`).join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'l.txt'), '-c', 'copy', out]);
  const seen = {}; evs.flat().forEach(e => { seen[e.type + '@' + e.time] = e; });
  fs.writeFileSync(out.replace(/\.mp4$/, '.sfx.json'), JSON.stringify(Object.values(seen).sort((a, b) => a.time - b.time)));
  console.log(`wrote ${out}: ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})();
