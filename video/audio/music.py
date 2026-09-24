"""Musique originale générée par code (libre de droits) pour la vidéo echecs.com.

Électro-pop énergique à 120 BPM (la mineur : Am – F – C – G). La structure suit
build/timing.json (généré par scripts/timing.py) : chaque changement de scène
tombe sur un temps et reçoit un impact, la montée finale mène au logo.
Sortie : audio/music.wav (stéréo, 48 kHz).
"""
import json
import os
import wave

import numpy as np
from scipy.signal import butter, sosfilt

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SR = 48000
BPM = 120
BEAT = 60 / BPM
BAR = 4 * BEAT
OUT = os.path.join(HERE, "music.wav")

timing = json.load(open(os.path.join(ROOT, "build", "timing.json")))
DURATION = timing["total"]
CUTS = [s["start"] for s in timing["scenes"]][1:]
T_DROP = timing["scenes"][1]["start"]      # le beat complet démarre à la scène 2
T_FINAL = timing["scenes"][-1]["start"]     # logo
T_RISE = T_FINAL - 2 * BAR / 2              # montée sur la mesure qui précède
N = int(SR * (DURATION + 0.5))
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(2026)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def add(buf, t, sig, g=1.0):
    i = int(t * SR)
    if i >= len(buf) or i + len(sig) <= 0:
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * g


def st(t, sig, g=1.0, pan=0.0):
    add(L, t, sig, g * (1 - max(0, pan)))
    add(R, t, sig, g * (1 + min(0, pan)))


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, kind, fs=SR, output="sos"), x)


def saw(freq, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((freq * t + phase) % 1.0) - 1


def env(n, a, d, s, r):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.interp(t, [0, a, a + d, max(a + d, dur - r), dur], [0, 1, s, s, 0])
    return e


# ------------------------------------------------------------------ instruments
def kick():
    n = int(.35 * SR)
    t = np.arange(n) / SR
    f = 48 + 160 * np.exp(-t * 35)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
    click = filt(rng.standard_normal(n), "highpass", 3000) * np.exp(-t * 400) * .3
    return np.tanh((body + click) * 1.6)


def clap():
    n = int(.25 * SR)
    t = np.arange(n) / SR
    x = filt(rng.standard_normal(n), "bandpass", [900, 3500])
    e = np.zeros(n)
    for k, dt in enumerate((0, .011, .022)):
        e += np.where(t >= dt, np.exp(-(t - dt) * (60 if k < 2 else 18)), 0)
    return x * e * .9


def hat(open_=False):
    n = int((.22 if open_ else .05) * SR)
    t = np.arange(n) / SR
    return filt(rng.standard_normal(n), "highpass", 8000) * np.exp(-t * (14 if open_ else 90))


def supersaw(notes, dur):
    n = int(dur * SR)
    x = np.zeros(n)
    for nn in notes:
        for det in (-.18, -.07, 0, .07, .18):
            x += saw(midi(nn) * 2 ** (det / 12), n, rng.random())
    x = filt(x, "lowpass", 3200) / (len(notes) * 5)
    return x * env(n, .01, .1, .8, .08)


def pluck(freq, dur=.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = saw(freq, n) * .6 + np.sin(2 * np.pi * freq * t)
    x = filt(x, "lowpass", 2500) * np.exp(-t * 14)
    return x


def bass(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * freq * t) + .35 * saw(freq, n)
    return filt(x, "lowpass", 700) * env(n, .005, .05, .85, .03)


def impact():
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 12)) / SR) * np.exp(-t * 3.5)
    noise = filt(rng.standard_normal(n), "lowpass", 5000) * np.exp(-t * 6) * .35
    return np.tanh((boom + noise) * 1.4)


def whoosh(dur=.5):
    n = int(dur * SR)
    x = rng.standard_normal(n)
    t = np.linspace(0, 1, n)
    y = np.zeros(n)
    step = 2048
    for i in range(0, n, step):
        fc = 500 + 7000 * t[i] ** 2
        y[i:i + step] = filt(x[i:i + step], "bandpass", [fc * .6, min(fc * 1.6, 20000)], 1)
    return y * t ** 2 * .5


# ------------------------------------------------------------------ arrangement
PROG = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]  # Am F C G
n_bars = int(np.ceil(DURATION / BAR)) + 1

# Sidechain : le kick « pompe » les accords et la basse
pump = np.ones(N)
for b in range(int(DURATION / BEAT) + 1):
    t0 = b * BEAT
    if t0 < T_DROP:
        continue
    i = int(t0 * SR)
    k = np.arange(int(BEAT * SR))
    seg = 1 - .75 * np.exp(-k / SR * 11)
    j = min(N, i + len(seg))
    pump[i:j] = np.minimum(pump[i:j], seg[: j - i])

chords = np.zeros(N)
bassline = np.zeros(N)
for b in range(n_bars):
    t0 = b * BAR
    if t0 >= DURATION:
        break
    root, notes = PROG[b % 4]
    add(chords, t0, supersaw([x - 12 for x in notes] + [notes[0]], BAR))
    if t0 >= T_DROP - .01:
        for e in range(8):   # basse en croches, octave sur les contretemps
            f = midi(root - 12 + (12 if e % 2 else 0))
            add(bassline, t0 + e * BEAT / 2, bass(f, BEAT / 2 * .9))

# Intro : accords filtrés qui s'ouvrent
intro_env = np.clip(np.arange(N) / SR / max(T_DROP, .1), 0, 1)
cut = filt(chords, "lowpass", 900)
chords_mix = np.where(np.arange(N) / SR < T_DROP, cut * (.4 + .6 * intro_env), chords * pump)
st(0, chords_mix, .55, -.1)
st(0, np.roll(chords_mix, int(.012 * SR)), .45, .1)
st(0, bassline * pump, .55)

# Arpège pluck en doubles-croches
t = 0.0
k = 0
pattern = [0, 1, 2, 1, 2, 3, 2, 1]
while t < DURATION - .1:
    b = int(t // BAR)
    root, notes = PROG[b % 4]
    tones = notes + [notes[0] + 12]
    nn = tones[pattern[k % 8]] + (12 if t >= timing["scenes"][3]["start"] and (k // 8) % 2 else 0)
    g = .14 if k % 4 == 0 else .09
    if T_RISE <= t < T_FINAL:
        g *= .5
    st(t, pluck(midi(nn)), g, .45 * np.sin(k * .9))
    t += BEAT / 4
    k += 1

# Batterie
nb = int(DURATION / BEAT) + 1
for b in range(nb):
    t0 = b * BEAT
    if t0 >= DURATION:
        break
    in_rise = T_RISE <= t0 < T_FINAL
    if t0 < T_DROP:
        if b % 2 == 0:
            st(t0, filt(kick(), "lowpass", 300), .45)   # kick étouffé dans l'intro
        continue
    if not in_rise:
        st(t0, kick(), .8)
        if b % 2 == 1:
            st(t0, clap(), .42)
        st(t0 + BEAT / 2, hat(True), .10, .2)
    st(t0, hat(), .07, -.3)
    st(t0 + BEAT / 4, hat(), .045, .3)
    st(t0 + BEAT * .75, hat(), .045, -.2)

# Roulement de caisse claire + montée avant le logo
n_roll = 16
for k in range(n_roll):
    tt = T_RISE + (T_FINAL - T_RISE) * k / n_roll
    st(tt, clap(), .12 + .3 * k / n_roll)
n = int((T_FINAL - T_RISE) * SR)
if n > 0:
    x = rng.standard_normal(n)
    tt = np.linspace(0, 1, n)
    riser = np.zeros(n)
    step = 2048
    for i in range(0, n, step):
        riser[i:i + step] = filt(x[i:i + step], "highpass", 300 + 6000 * tt[i] ** 2, 1)
    st(T_RISE, riser * tt ** 2, .35)

# Impacts et whooshes sur les coupes
for c in CUTS:
    if c == T_FINAL:
        continue
    st(c - .45, whoosh(.45), .5)
    st(c, impact(), .32)
st(T_FINAL, impact(), .75)
for nn in (45, 57, 64, 69, 72, 76):   # accord final tenu
    s = supersaw([nn], 3.0) * .9
    st(T_FINAL, filt(s, "lowpass", 5000) * np.exp(-np.arange(len(s)) / SR * .9), .5)


# ------------------------------------------------------------------ master
def room(x):
    y = x.copy()
    for d, g in ((.023, .35), (.031, .3), (.047, .25), (.089, .18), (.137, .12)):
        k = int(d * SR)
        y[k:] += x[:-k] * g
    return y


L = .8 * L + .2 * room(L)
R = .8 * R + .2 * room(R)
L, R = np.tanh(L * 1.3), np.tanh(R * 1.3)
nn = int(DURATION * SR)
L, R = L[:nn], R[:nn]
fade = np.clip((DURATION - np.arange(nn) / SR) / 1.2, 0, 1) * np.clip(np.arange(nn) / (SR * .05), 0, 1)
L, R = L * fade, R * fade
peak = max(np.abs(L).max(), np.abs(R).max())
data = (np.stack([L, R], 1) / peak * .9 * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("écrit", OUT, f"{DURATION:.1f}s, coupes :", CUTS)
