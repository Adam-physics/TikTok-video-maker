"""Builds the timing sheet (cues-<track>.json) for each music version.
Sections sit on bar lines of that track; every narration line starts on a beat."""
import json, math, sys, os

HERE = os.path.dirname(os.path.abspath(__file__))
dur_vo = json.load(open(sys.argv[1]))          # seconds per narration clip

TRACKS = {
  # beat grid measured from the audio: first beat, beat length
  'tech': dict(b0=0.095, beat=0.58023, dur=147.6,
               sec=dict(hook=0, acc=6, fam=12, ins=17, loan=21, energy=25, mont=29, reveal=33, wheel=37, engine=42, proof=50, cta=53),
               hi=[[14.0, 76.7], [86.0, 131.0]], break_=None),
  'epic': dict(b0=0.445, beat=0.48780, dur=152.4,
               sec=dict(hook=0, acc=7, fam=14, ins=20, loan=25, energy=30, mont=34, reveal=39, wheel=44, engine=50, proof=60, cta=67),
               hi=[[1.0, 76.5], [86.3, 137.0]], break_=[76.54, 86.29]),
}

# narration: (clip, section, offset seconds into the section)
PLAN = [('h1','hook',1.0),('h2','hook',6.2),('h3','hook',12.4),
        ('a1','acc',.5),('a2','acc',4.3),('a3','acc',9.5),
        ('f1','fam',.4),('f2','fam',5.6),
        ('i1','ins',.4),('i2','ins',3.6),
        ('l1','loan',.4),('l2','loan',2.6),
        ('e1','energy',.4),('e2','energy',4.6),
        ('m1','mont',.2),('m2','mont',None),('m3','mont',None),('m4','mont',None),
        ('r1','reveal',.6),('r2','reveal',5.1),
        ('r3','wheel',1.2),('r4','wheel',10.0),
        ('g1','engine',1.0),('g2a','engine',None),('g2b','engine',None),('g2c','engine',None),('g2d','engine',None),('g3','engine',None),
        ('c1','cta',.5),('c2','cta',2.6),('c3','cta',None),('c4','cta',None)]

for name, T in TRACKS.items():
    beat, b0 = T['beat'], T['b0']; bar = beat * 4
    S = {k: round(b0 + v * bar if v else 0.0, 3) for k, v in T['sec'].items()}
    vo, prev_end = {}, 0.0
    for clip, sec, off in PLAN:
        if off is None:   # follow on from the previous line
            gap = {'g2b': 2, 'g2c': 2, 'g2d': 2}.get(clip)
            want = (vo[list(vo)[-1]] + gap * beat) if gap else prev_end + (0.9 if clip in ('g2a', 'g3', 'c3', 'c4') else 0.3)
        else:
            want = S[sec] + off
        k = math.ceil((want - b0) / beat - 0.08)
        t = b0 + k * beat
        while t < prev_end + 0.12: t += beat
        vo[clip] = round(t, 3); prev_end = t + dur_vo[clip]
    S['end'] = vo['c4']
    cues = dict(track=name, dur=T['dur'], beat=beat, b0=b0, bar=bar, hi=T['hi'], break_=T['break_'], sec=S, vo=vo, vodur=dur_vo)
    json.dump(cues, open(os.path.join(HERE, f'cues-{name}.json'), 'w'), indent=1)
    print(name, 'last line ends', round(prev_end, 1), 's of', T['dur'])
    print('  ', ' '.join(f"{k}:{v}" for k, v in vo.items()))
