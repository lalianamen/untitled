import asyncio, json, os, subprocess, sys
import edge_tts

import shutil
FF = os.environ.get("FFMPEG") or shutil.which("ffmpeg") or "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
VOICE = os.environ.get("VOICE", "es-US-AlonsoNeural")
RATE = os.environ.get("RATE", "+4%")
PROXY = os.environ.get("HTTPS_PROXY")

MODE = os.environ.get("MODE", "full")
FULL = [
  ("01_hook",     "¿Trabajas en aire acondicionado en California o Arizona, y todavía no tienes tu licencia de contratista?"),
  ("02_pain",     "Sin licencia, cualquier trabajo de mil dólares o más es ilegal. Sin permisos, sin cobrar en corte, y los contratos grandes se los lleva otro."),
  ("03_dream",    "Con tu licencia: tu propia empresa, tus precios, tus clientes."),
  ("04_obstacle", "Pero el examen de contratista es en inglés, dura horas, y está lleno de trampas."),
  ("05_solution", "LICENA es tu entrenador: quinientas preguntas de Law and Business, quinientas de Trade C veinte, preparación para Arizona, y una guía paso a paso hasta tu empresa."),
  ("06_demo",     "Practicas en inglés, como en el examen real, con explicación al instante."),
  ("07_proof",    "Basado en el libro oficial del C S L B dos mil veintiséis. Hecho por un contratista en Los Ángeles, no por una escuela."),
  ("08_honest",   "Nadie garantiza el cien por ciento. Pero con práctica real, tus chances de pasar a la primera suben de setenta y cinco, a más de noventa por ciento."),
  ("09_cta",      "Empieza hoy. El enlace está en la descripción."),
]
SHORT = [
  ("01_hook",     "¿Trabajas en aire acondicionado en California o Arizona, y todavía no tienes tu licencia de contratista?"),
  ("02_pain",     "Sin licencia, cualquier trabajo de mil dólares o más es ilegal, y los contratos grandes se los lleva otro."),
  ("03_dream",    "Con tu licencia: tu empresa, tus precios, tus clientes."),
  ("04_obstacle", "Pero el examen es en inglés, y está lleno de trampas."),
  ("05_solution", "LICENA es tu entrenador: mil preguntas estilo examen para California, preparación para Arizona, y una guía paso a paso hasta tu empresa."),
  ("06_demo",     "Practicas en inglés, como en el examen real, con explicación al instante."),
  ("08_honest",   "Hecho por un contratista, no por una escuela. Y con práctica real, tus chances de pasar a la primera suben de setenta y cinco, a más de noventa por ciento."),
  ("09_cta",      "Empieza hoy. El enlace está en la descripción."),
]
SEGMENTS = SHORT if MODE == "short" else FULL
VODIR = "vo_short" if MODE == "short" else "vo"
os.makedirs(VODIR, exist_ok=True)

def dur(path):
    out = subprocess.run([FF, "-i", path, "-f", "null", "-"], capture_output=True, text=True).stderr
    # parse last "time=HH:MM:SS.xx"
    import re
    m = re.findall(r"time=(\d+):(\d+):([\d.]+)", out)
    if not m: return None
    h, mi, s = m[-1]
    return int(h)*3600 + int(mi)*60 + float(s)

async def main():
    res = {}
    for name, text in SEGMENTS:
        mp3 = f"{VODIR}/{name}.mp3"
        wav = f"{VODIR}/{name}.wav"
        comm = edge_tts.Communicate(text, VOICE, rate=RATE, proxy=PROXY)
        await comm.save(mp3)
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", mp3, "-af", "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse,silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.08,areverse", "-ar", "48000", "-ac", "1", wav], check=True)
        d = dur(wav)
        res[name] = {"text": text, "dur": d}
        print(f"{name:14s} {d:6.2f}s  {text[:60]}")
    json.dump(res, open(f"{VODIR}/durations.json", "w"), ensure_ascii=False, indent=1)
    print("TOTAL", round(sum(v["dur"] for v in res.values()), 2))

asyncio.run(main())
