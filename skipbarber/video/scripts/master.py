"""Two-pass EBU R128 loudnorm to -14 LUFS / -1 dBTP. Video stream is copied untouched.
Usage: python3 scripts/master.py in.mp4 out.mp4"""
import json, re, subprocess, sys

src, dst = sys.argv[1], sys.argv[2]
target = 'I=-14:TP=-1:LRA=11'
p = subprocess.run(['ffmpeg', '-hide_banner', '-i', src, '-af', f'loudnorm={target}:print_format=json', '-f', 'null', '-'],
                   capture_output=True, text=True)
m = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', p.stderr)[-1])
af = (f"loudnorm={target}:measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
      f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true,aresample=48000")
subprocess.run(['ffmpeg', '-hide_banner', '-loglevel', 'error', '-y', '-i', src, '-c:v', 'copy', '-af', af,
                '-c:a', 'aac', '-b:a', '320k', '-movflags', '+faststart', dst], check=True)
q = subprocess.run(['ffmpeg', '-hide_banner', '-i', dst, '-af', 'loudnorm=print_format=json', '-f', 'null', '-'],
                   capture_output=True, text=True)
r = json.loads(re.findall(r'\{[^{}]*"input_i"[^{}]*\}', q.stderr)[-1])
print(f"{dst}: in {m['input_i']} LUFS -> out {r['input_i']} LUFS, true peak {r['input_tp']} dBTP")
