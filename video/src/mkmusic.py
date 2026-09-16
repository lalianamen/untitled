# Pure-Python ambient/upbeat music bed: pad chords + soft kick + bass + hats. Writes music.wav (48 kHz stereo).
import math, array, wave, random, sys
SR = 48000
DUR = float(sys.argv[1]) if len(sys.argv) > 1 else 62.0
BPM = 100.0
BEAT = 60.0 / BPM
BAR = 4 * BEAT
CHORD_LEN = 2 * BAR  # 4.8 s per chord
# A minor / F / C / G  (midi numbers), voiced low-mid
def f(m): return 440.0 * 2 ** ((m - 69) / 12)
CHORDS = [
  [57, 60, 64, 69],  # Am
  [53, 57, 60, 65],  # F
  [55, 60, 64, 67],  # C
  [55, 59, 62, 67],  # G
]
ROOTS = [45, 41, 48, 43]  # bass roots (A1, F1, C2, G1) -> +12 for audibility

N = int(SR * DUR)
random.seed(7)
out = array.array('h')
two_pi = 2 * math.pi

# precompute chord oscillator tables per chord (one period is not integer; do direct sin, but cache phases increments)
chord_freqs = []
for ch in CHORDS:
    fs = []
    for m in ch:
        base = f(m)
        fs.append((base * 0.9985, base * 1.0015, base * 2.0))  # detuned pair + octave partial
    chord_freqs.append(fs)
bass_freqs = [f(r + 12) for r in ROOTS]

def env_ad(t, a, d):  # attack/decay exponential
    if t < 0: return 0.0
    if t < a: return t / a
    return math.exp(-(t - a) / d)

# noise buffer for hats
prev_noise = 0.0
last_l = last_r = 0.0
for n in range(N):
    t = n / SR
    ci = int(t // CHORD_LEN) % len(CHORDS)
    tc = t - (t // CHORD_LEN) * CHORD_LEN  # time within chord
    # pad envelope: attack 0.5s, release last 0.4s
    if tc < 0.5: pe = tc / 0.5
    elif tc > CHORD_LEN - 0.4: pe = (CHORD_LEN - tc) / 0.4
    else: pe = 1.0
    lfo = 0.85 + 0.15 * math.sin(two_pi * 0.23 * t)
    pad = 0.0
    for (fa, fb, fo) in chord_freqs[ci]:
        pad += math.sin(two_pi * fa * t) + math.sin(two_pi * fb * t) + 0.25 * math.sin(two_pi * fo * t)
    pad *= pe * lfo / (len(chord_freqs[ci]) * 2.25)
    # global intro fade in / outro fade out
    g = 1.0
    if t < 1.5: g = t / 1.5
    if t > DUR - 2.5: g = max(0.0, (DUR - t) / 2.5)
    # rhythm section starts after first chord (4.8 s) for a build-up
    rhythm = 0.0 if t < CHORD_LEN else min(1.0, (t - CHORD_LEN) / 1.0)
    beat_pos = (t / BEAT)
    tb = (beat_pos - math.floor(beat_pos)) * BEAT  # time since beat
    # kick: pitch sweep 110 -> 45 Hz
    ke = env_ad(tb, 0.004, 0.11)
    kf = 45 + 65 * math.exp(-tb / 0.03)
    kick = math.sin(two_pi * kf * tb) * ke * 0.55
    # bass: on beats 1 and 3.5 of each bar
    bar_pos = (t / BAR) - math.floor(t / BAR)
    bt = None
    for hit in (0.0, 0.625, 0.75):
        if bar_pos >= hit: bt = (bar_pos - hit) * BAR
    be = env_ad(bt, 0.01, 0.35) if bt is not None else 0.0
    bass = (math.sin(two_pi * bass_freqs[ci] * t) + 0.3 * math.sin(two_pi * bass_freqs[ci] * 2 * t)) * be * 0.35
    # hats on 8ths (offbeat louder), short noise bursts, crude highpass via difference
    eighth = (t / (BEAT / 2)); te = (eighth - math.floor(eighth)) * (BEAT / 2)
    offbeat = int(math.floor(eighth)) % 2 == 1
    he = env_ad(te, 0.001, 0.025 if offbeat else 0.012) * (0.9 if offbeat else 0.45)
    nz = random.uniform(-1, 1)
    hat = (nz - prev_noise) * he * 0.10
    prev_noise = nz
    mix = pad * 0.42 + rhythm * (kick + bass + hat)
    mix *= g * 0.6
    # gentle stereo: pad wider via tiny delay-less phase trick (use sign-alternating detune) -> simple: pan pad slightly
    l = mix + pad * 0.05 * math.sin(two_pi * 0.11 * t)
    r = mix - pad * 0.05 * math.sin(two_pi * 0.11 * t)
    # soft clip
    l = math.tanh(l * 1.2); r = math.tanh(r * 1.2)
    out.append(int(max(-1, min(1, l)) * 32000)); out.append(int(max(-1, min(1, r)) * 32000))

with wave.open("music.wav", "wb") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes(out.tobytes())
print("wrote music.wav", DUR, "s")
