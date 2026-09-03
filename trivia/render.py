"""Assemble scene stills into a finished, upload-ready MP4.

Stills carry the layout; this module adds the things a still cannot do --
a slow push on every panel so nothing sits dead on screen, the guess timer
draining in real time, and the score.

Output is H.264 / AAC in a faststart MP4 at 1080x1920, which is what
TikTok ingests without re-encoding surprises.
"""
from __future__ import annotations

import os
import shutil
import subprocess

from . import brand


def ffmpeg_bin() -> str:
    """Prefer the repo-local static build so the tool needs no system install."""
    local = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                         "node_modules", "ffmpeg-static", "ffmpeg")
    if os.path.exists(local):
        return local
    found = shutil.which("ffmpeg")
    if not found:
        raise RuntimeError("ffmpeg not found -- run `npm install` in the repo root")
    return found


def _ts(t: float) -> str:
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def timer_track(scenes: list[dict], path: str) -> str:
    """An ASS overlay that drains a bar across each timed scene."""
    head = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {brand.WIDTH}
PlayResY: {brand.HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Groove,DejaVu Sans,40,&H00141410,&H00141410,&H00000000,-1,100,100,0,0,1,5,0,7,0,0,0,1
Style: Bar,DejaVu Sans,40,&H001AC7FF,&H00141410,&H00000000,-1,100,100,0,0,1,5,0,7,0,0,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events, t = [], 0.0
    for scene in scenes:
        dur = scene["duration"]
        if scene.get("timer"):
            x, y, w, h = scene["timer_box"]
            ms = int(dur * 1000)
            shape = rf"{{\p1}}m 0 0 l {w} 0 {w} {h} 0 {h}{{\p0}}"
            # Both halves are overlays. Baking the groove into the still
            # would let the scene's slow push drift it away from the fill,
            # which stays put because subtitles render after the zoom.
            groove = rf"{{\an7\pos({x},{y})}}"
            events.append(
                f"Dialogue: 0,{_ts(t)},{_ts(t + dur)},Groove,,0,0,0,,{groove}{shape}")
            fill = (rf"{{\an7\pos({x},{y})\clip({x},{y},{x + w},{y + h})"
                    rf"\t(0,{ms},\clip({x},{y},{x},{y + h}))}}")
            events.append(
                f"Dialogue: 1,{_ts(t)},{_ts(t + dur)},Bar,,0,0,0,,{fill}{shape}")
        t += dur
    with open(path, "w") as f:
        f.write(head + "\n".join(events) + "\n")
    return path


def _motion(index: int, duration: float) -> str:
    """Alternate a slow push in and out so consecutive panels differ."""
    frames = max(2, round(duration * brand.FPS))
    if index % 2 == 0:
        z = f"min(1+0.0009*on,1.10)"
    else:
        z = f"max(1.10-0.0009*on,1.0)"
    return (f"zoompan=z='{z}':d={frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
            f":s={brand.WIDTH}x{brand.HEIGHT}:fps={brand.FPS}"
            f",trim=duration={duration:.3f},setpts=PTS-STARTPTS")


def build(scenes: list[dict], audio_path: str, ass_path: str, out_path: str) -> str:
    """Render the round. `scenes` is [{png, duration, timer}] in order."""
    cmd = [ffmpeg_bin(), "-y", "-hide_banner", "-loglevel", "error"]
    for scene in scenes:
        cmd += ["-loop", "1", "-t", f"{scene['duration']:.3f}", "-i", scene["png"]]
    cmd += ["-i", audio_path]

    chains = [f"[{i}:v]{_motion(i, s['duration'])}[v{i}]"
              for i, s in enumerate(scenes)]
    joined = "".join(f"[v{i}]" for i in range(len(scenes)))
    graph = ";".join(chains)
    graph += f";{joined}concat=n={len(scenes)}:v=1:a=0[cat]"
    graph += f";[cat]subtitles='{ass_path}':fontsdir={brand.FONT_DIR}[vout]"

    cmd += [
        "-filter_complex", graph,
        "-map", "[vout]", "-map", f"{len(scenes)}:a",
        "-c:v", "libx264", "-preset", "medium", "-crf", "19",
        "-pix_fmt", "yuv420p", "-r", str(brand.FPS), "-g", str(brand.FPS * 2),
        "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2",
        "-shortest", "-movflags", "+faststart", out_path,
    ]
    done = subprocess.run(cmd, capture_output=True, text=True)
    if done.returncode:
        raise RuntimeError(done.stderr[-4000:])
    return out_path
