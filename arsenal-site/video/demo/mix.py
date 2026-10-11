"""Builds the soundtrack for one version of the demo and muxes it onto the silent render.

usage: python3 mix.py <tech|epic> <music.mp3> <vo_dir> <silent.mp4> <out.mp4>

- epic: the 60-second track is extended to the edit by repeating bar-aligned sections
  (seams picked by comparing bars: 16->1 and 19->12), and gets a filtered "breakdown"
  under the reveal so the drop lands on "One relationship".
- narration clips are placed at the beat-snapped times in cues-<version>.json
- music ducks under the voice; light sound effects follow the on-screen hits
"""
import json, os, subprocess, sys, tempfile
import numpy as np
import soundfile as sf

SR = 48000
HERE = os.path.dirname(os.path.abspath(__file__))
v, music_path, vo_dir, silent, out = sys.argv[1:6]
cues = json.load(open(os.path.join(HERE, f'cues-{v}.json')))
DUR = cues['dur']
tmp = tempfile.mkdtemp()


def load(path):
    wav = os.path.join(tmp, os.path.basename(path) + '.wav')
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', path, '-ar', str(SR), '-ac', '2', wav], check=True)
    x, _ = sf.read(wav, dtype='float32')
    return x


def lowpass(x, cutoff):
    a, b = os.path.join(tmp, 'lp_in.wav'), os.path.join(tmp, 'lp_out.wav'); sf.write(a, x, SR)
    subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', a, '-af', f'lowpass=f={cutoff},lowpass=f={cutoff}', b], check=True)
    return sf.read(b, dtype='float32')[0]


def env(n, pts):                     # piecewise-linear envelope from (time, value) points
    t = np.arange(n) / SR; p = np.array(pts)
    return np.interp(t, p[:, 0], p[:, 1]).astype(np.float32)[:, None]


# ───────── music ─────────
m = load(music_path)
if v == 'epic':
    b0, bar = cues['b0'], cues['bar']
    S = lambda b: int(round((b0 + b * bar) * SR))
    plan = [(None, 0), (0, 17), (1, 17), (1, 20), (12, 20), (12, 22), (22, None)]   # (from bar, to bar) half-open; None = track edge
    pieces, xf = [], int(.012 * SR)
    for a, b in plan:
        seg = m[(0 if a is None else S(a)):(len(m) if b is None else S(b))].copy()
        if pieces and len(seg) > xf:     # tiny crossfade at every seam
            ramp = np.linspace(0, 1, xf, dtype=np.float32)[:, None]
            pieces[-1][-xf:] = pieces[-1][-xf:] * (1 - ramp) + seg[:xf] * ramp; seg = seg[xf:]
        pieces.append(seg)
    m = np.concatenate(pieces)
    # breakdown under the reveal: filtered and lower, opening back up on the drop
    r0, r1 = cues['break_']
    filt = lowpass(m, 700)
    mixk = env(len(m), [(0, 0), (r0, 0), (r0 + 1.2, 1), (r1 - .5, 1), (r1, 0), (len(m) / SR, 0)])
    m = m * (1 - mixk) + filt * mixk * 0.8
n = int(DUR * SR)
m = np.pad(m, ((0, max(0, n - len(m))), (0, 0)))[:n]
m *= env(n, [(0, 1), (DUR - 2.5, 1), (DUR, 0)])

# ───────── narration ─────────
vo = np.zeros((n, 2), np.float32)
for key, t in cues['vo'].items():
    c = load(os.path.join(vo_dir, key + '.wav'))
    i = int(t * SR); j = min(n, i + len(c)); vo[i:j] += c[:j - i]
vo *= 1.0 / max(1e-6, np.abs(vo).max()) * 0.89

# duck the music under the voice: envelope at 100 Hz, fast attack, slow release (8-10 dB)
hop = SR // 100; frames = len(vo) // hop + 1
lvl = np.array([np.sqrt(np.mean(vo[i * hop:(i + 1) * hop, 0] ** 2)) if i * hop < len(vo) else 0 for i in range(frames)])
g, s_, sm = (lvl > 0.01).astype(float), 0.0, []
for x in g:
    s_ += (x - s_) * (0.5 if x > s_ else 0.03); sm.append(s_)
depth = 0.7 if v == 'epic' else 0.6        # the epic track is fuller, so it ducks deeper
duck = (1 - depth * np.interp(np.arange(n) / hop, np.arange(frames), sm)).astype(np.float32)[:, None]

# ───────── sound effects ─────────
rng = np.random.default_rng(7)
def tone(f0, f1, d, decay):
    t = np.arange(int(d * SR)) / SR; f = np.linspace(f0, f1, len(t)); ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) * np.exp(-t / decay)).astype(np.float32)
def noise(d, lo, hi, shape):
    x = rng.standard_normal(int(d * SR)).astype(np.float32); X = np.fft.rfft(x); fr = np.fft.rfftfreq(len(x), 1 / SR)
    X[(fr < lo) | (fr > hi)] = 0; x = np.fft.irfft(X, len(x)).astype(np.float32); x /= np.abs(x).max() + 1e-9
    return x * shape(np.linspace(0, 1, len(x))).astype(np.float32)
def add(*xs):
    L = max(len(x) for x in xs); return sum(np.pad(x, (0, L - len(x))) for x in xs)
SFX = {
    'whoosh': lambda: noise(.5, 500, 6000, lambda u: np.sin(np.pi * u) ** 2) * .18,
    'hit':    lambda: add(tone(90, 45, .45, .12) * .5, noise(.08, 1500, 9000, lambda u: (1 - u) ** 3) * .12),
    'pop':    lambda: tone(880, 1320, .09, .03) * .1,
    'click':  lambda: noise(.02, 2000, 9000, lambda u: (1 - u) ** 2) * .14,
    'riser':  lambda: add(noise(2.4, 300, 9000, lambda u: u ** 2.2) * .22, tone(200, 900, 2.4, 9) * np.linspace(0, .08, int(2.4 * SR)).astype(np.float32)),
    'boom':   lambda: add(tone(70, 32, 1.6, .5) * .6, noise(.4, 200, 4000, lambda u: (1 - u) ** 4) * .2),
}
fx = np.zeros(n, np.float32); last = {}
for e in json.load(open(silent.replace('.mp4', '.sfx.json'))):
    typ, t = e['type'], e['time']
    if t < 0 or t >= DUR or typ not in SFX: continue
    if t - last.get(typ, -9) < (.25 if typ in ('pop', 'click') else .4): continue     # keep it uncluttered
    last[typ] = t; c = SFX[typ](); i = int(t * SR); j = min(n, i + len(c)); fx[i:j] += c[:j - i]
fx = np.stack([fx, fx], 1)

mix = m * 0.72 * duck + vo + fx * 0.8
mix /= max(1.0, np.abs(mix).max() / 0.98)
wav = os.path.join(tmp, 'mix.wav'); sf.write(wav, mix, SR)
subprocess.run(['ffmpeg', '-v', 'error', '-y', '-i', silent, '-i', wav, '-af', 'loudnorm=I=-14:TP=-1.0:LRA=11', '-ar', '48000',
                '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k', '-shortest', '-movflags', '+faststart', out], check=True)
print('wrote', out)
