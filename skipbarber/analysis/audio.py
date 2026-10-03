import librosa, numpy as np, json, sys
out={}
for name in ["byline-short","outrank","download-24"]:
    y,sr=librosa.load(f"../analysis/{name}.wav",sr=22050)
    tempo,beats=librosa.beat.beat_track(y=y,sr=sr,units="time")
    onset=librosa.onset.onset_strength(y=y,sr=sr)
    rms=librosa.feature.rms(y=y)[0]; t=librosa.times_like(rms,sr=sr)
    # per-second RMS in dB
    sec=[float(20*np.log10(np.mean(rms[(t>=s)&(t<s+1)])+1e-9)) for s in range(int(t[-1])+1)]
    # spectral flatness / centroid hint at voice: zero-crossing + harmonic ratio
    harm,perc=librosa.effects.hpss(y)
    cuts=[float(x) for x in open(f"../analysis/{name}-cuts.txt").read().split()]
    cuts2=[float(x) for x in open(f"../analysis/{name}-cuts-012.txt").read().split()]
    b=np.array(beats)
    def near(c): 
        d=np.abs(b-c).min() if len(b) else 9; return float(d)
    out[name]=dict(bpm=float(np.atleast_1d(tempo)[0]),n_beats=len(b),beat_period=float(np.median(np.diff(b))) if len(b)>1 else None,
        first_beats=[round(x,2) for x in b[:12].tolist()],
        rms_db_per_sec=[round(x,1) for x in sec],
        harm_perc_ratio=float(np.mean(harm**2)/ (np.mean(perc**2)+1e-12)),
        cuts_03=cuts, cuts_012=cuts2,
        cut_beat_offsets_012=[round(near(c),3) for c in cuts2])
    o=out[name]; d=np.diff([0]+cuts2+[len(y)/sr])
    o["avg_shot_012"]=float(np.mean(d)); o["median_shot_012"]=float(np.median(d))
    d3=np.diff([0]+cuts+[len(y)/sr]); o["avg_shot_03"]=float(np.mean(d3))
    o["pct_cuts_within_100ms_of_beat"]=float(np.mean(np.array(o["cut_beat_offsets_012"])<0.1)) if cuts2 else None
json.dump(out,open("../analysis/audio.json","w"),indent=1)
for k,v in out.items():
    print(k, {x:v[x] for x in ["bpm","beat_period","avg_shot_03","avg_shot_012","median_shot_012","pct_cuts_within_100ms_of_beat","harm_perc_ratio"]}, "cuts012:",len(v["cuts_012"]))
    print("  rms/sec:",v["rms_db_per_sec"])
