// Renders story.html to an MP4 frame by frame. Rendering is deterministic, so every run is identical.
// Usage: node render.js [out.mp4] [fps] [workers]   (serve arsenal-site/ on :8765 first)
const { spawn, execFileSync } = require('child_process');
const fs = require('fs'), os = require('os'), path = require('path');
const { chromium } = require(process.env.PW || 'playwright');

async function renderChunk(browser, file, from, to, fps) {
  const p = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('http://localhost:8765/video/story.html?render');
  await p.evaluate(() => window.storyReady);
  const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-c:v', 'mjpeg', '-framerate', String(fps), '-i', '-',
    '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', file], { stdio: ['pipe', 'inherit', 'inherit'] });
  for (let i = from; i < to; i++) {
    // JPEG at high quality straight from the canvas is far faster than a page screenshot
    const b64 = await p.evaluate(t => { renderAt(t); return document.getElementById('c').toDataURL('image/jpeg', .96).slice(23); }, i / fps);
    if (!ff.stdin.write(Buffer.from(b64, 'base64'))) await new Promise(r => ff.stdin.once('drain', r));
  }
  ff.stdin.end(); await new Promise(r => ff.on('close', r)); await p.close();
}

(async () => {
  const out = path.resolve(process.argv[2] || 'arsenal-story.mp4'), fps = +(process.argv[3] || 30), workers = +(process.argv[4] || 3);
  const browser = await chromium.launch();
  const probe = await browser.newPage(); await probe.goto('http://localhost:8765/video/story.html?render');
  const n = Math.round(await probe.evaluate(() => window.DURATION) * fps); await probe.close();
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'story-')), per = Math.ceil(n / workers), parts = [];
  const t0 = Date.now();
  await Promise.all(Array.from({ length: workers }, (_, w) => {
    const f = path.join(tmp, `part${w}.mp4`); parts.push(f);
    return renderChunk(browser, f, w * per, Math.min(n, (w + 1) * per), fps);
  }));
  await browser.close();
  fs.writeFileSync(path.join(tmp, 'list.txt'), parts.map(f => `file '${f}'`).join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', path.join(tmp, 'list.txt'), '-c', 'copy', '-movflags', '+faststart', out]);
  console.log(`wrote ${out}: ${n} frames in ${((Date.now() - t0) / 1000).toFixed(0)}s`);
})();
