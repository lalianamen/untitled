# Build timeline from VO durations, write final HTML, build the audio mix.
import json, os, subprocess, sys, shutil
import shutil
FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
SC = os.path.dirname(os.path.abspath(__file__))
MODE = "short" if "--short" in sys.argv else "full"
VODIR = f"{SC}/vo_short" if MODE == "short" else f"{SC}/vo"
SUF = "_short" if MODE == "short" else ""
D = json.load(open(f"{VODIR}/durations.json"))
ALL = ["hook","pain","dream","obstacle","solution","demo","proof","honest","cta"]
KEYS = {k: f"{i+1:02d}_{k}" for i, k in enumerate(ALL)}
ORDER = [k for k in ALL if k != "proof"] if MODE == "short" else ALL
LEAD = {k: 0.3 for k in ORDER}      # VO starts this long after the scene starts
LEAD["hook"] = 0.55; LEAD["solution"] = 0.6; LEAD["demo"] = 0.5
MIN = {"hook":5.6,"pain":9.0,"dream":5.0,"obstacle":7.0,"solution":9.0,"demo":5.8,"proof":6.8,"honest":7.8,"cta":4.0}
if MODE == "short":
    MIN = {"hook":5.4,"pain":6.6,"dream":4.2,"obstacle":4.6,"solution":8.0,"demo":5.4,"honest":8.0,"cta":3.6}
    TAIL_OVERRIDE = 0.3
TAIL = 0.3 if MODE == "short" else 0.4
scenes, t = {}, 0.0
vo_starts = {}
for k in ORDER:
    vo = D[KEYS[k]]["dur"]
    length = max(MIN[k], LEAD[k] + vo + TAIL)
    if k == "cta": length = LEAD[k] + vo + (2.4 if MODE == "short" else 2.8)  # hold the end card
    scenes[k] = [round(t, 3), round(t + length, 3)]
    vo_starts[k] = round(t + LEAD[k], 3)
    t += length
total = round(t, 3)
TL = {"total": total, "scenes": scenes, "mode": MODE}
print(json.dumps(TL, indent=1)); print("VO starts", vo_starts)

os.makedirs(f"{SC}/out", exist_ok=True)
shutil.copytree(f"{SC}/fonts", f"{SC}/out/fonts", dirs_exist_ok=True)
html = open(f"{SC}/promo_template.html", encoding="utf-8").read().replace("__TIMELINE__", json.dumps(TL))
open(f"{SC}/out/licena_promo_es{SUF}.html", "w", encoding="utf-8").write(html)
json.dump({"timeline": TL, "vo_starts": vo_starts}, open(f"{SC}/out/timeline{SUF}.json", "w"), indent=1)

if "--audio" in sys.argv:
    # voice track: each segment delayed to its start
    inputs, filters, labels = [], [], []
    for i, k in enumerate(ORDER):
        inputs += ["-i", f"{VODIR}/{KEYS[k]}.wav"]
        ms = int(vo_starts[k] * 1000)
        filters.append(f"[{i}:a]adelay={ms}|{ms},apad=whole_dur={total}[v{i}]")
        labels.append(f"[v{i}]")
    n = len(ORDER)
    inputs += ["-i", f"{SC}/music.wav"]
    fc = ";".join(filters) + ";" + "".join(labels) + f"amix=inputs={n}:normalize=0,volume=1.0,aformat=channel_layouts=stereo,asplit=2[vA][vB];"
    fc += (f"[{n}:a]atrim=0:{total},afade=t=out:st={total-2.5}:d=2.5,volume=0.42[mus];"
           f"[mus][vB]sidechaincompress=threshold=0.02:ratio=8:attack=40:release=500:makeup=1[musd];"
           f"[musd][vA]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=11[out]")
    cmd = [FF, "-y", "-loglevel", "warning"] + inputs + ["-filter_complex", fc, "-map", "[out]", "-ar", "48000", "-ac", "2", f"{SC}/out/audio{SUF}.wav"]
    subprocess.run(cmd, check=True)
    print("audio ok", total)
