"""Generates the narration clips in vo/ with the Kokoro voice model (via sherpa-onnx).

usage: python3 make_vo.py <kokoro-en-v0_19 dir> [speaker id, default 6 = "Michael"] [speed, default 1.05]
Model: https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/kokoro-en-v0_19.tar.bz2
Edit vo/lines.json to change the wording, then rerun this and build_cues.py."""
import json, os, sys
import numpy as np, sherpa_onnx, soundfile as sf

d = sys.argv[1].rstrip('/') + '/'; sid = int(sys.argv[2]) if len(sys.argv) > 2 else 6; speed = float(sys.argv[3]) if len(sys.argv) > 3 else 1.05
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'vo')
tts = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(model=d + 'model.onnx', voices=d + 'voices.bin', tokens=d + 'tokens.txt', data_dir=d + 'espeak-ng-data'), num_threads=4)))
durations = {}
for key, line in json.load(open(os.path.join(out, 'lines.json'))):
    a = tts.generate(line, sid=sid, speed=speed); x = np.array(a.samples)
    nz = np.where(np.abs(x) > 0.01)[0]; x = x[max(0, nz[0] - 240):nz[-1] + 2400]      # trim silence
    sf.write(os.path.join(out, key + '.wav'), x, a.sample_rate); durations[key] = round(len(x) / a.sample_rate, 3)
json.dump(durations, open(os.path.join(out, 'durations.json'), 'w'), indent=0)
print('total speech', round(sum(durations.values()), 1), 's')
