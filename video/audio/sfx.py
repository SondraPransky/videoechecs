"""Bruitages d'interface générés par code (libres de droits).

Lit build/sfx.json (instants exportés par `node render.mjs --sfx`) et écrit
build/sfx.wav (stéréo, 48 kHz) : clics, « pop », validations, notifications,
tic-tac des compteurs, pièces posées sur l'échiquier, frappe au clavier.
"""
import json
import os
import wave

import numpy as np
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SR = 48000
timing = json.load(open(os.path.join(ROOT, "build", "timing.json")))
events = json.load(open(os.path.join(ROOT, "build", "sfx.json")))
N = int(SR * (timing["total"] + 1))
L, R = np.zeros(N), np.zeros(N)
rng = np.random.default_rng(7)


def env(n, k):
    return np.exp(-np.arange(n) / SR * k)


def tone(f, dur, k, sweep=1.0):
    n = int(dur * SR)
    fr = f * sweep ** (np.arange(n) / n)
    return np.sin(2 * np.pi * np.cumsum(fr) / SR) * env(n, k)


def band(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)


def click(p):
    n = int(.03 * SR)
    return band(rng.standard_normal(n), 2500 * p, 7000) * env(n, 260) * .6 + tone(1800 * p, .03, 180) * .35


def key(p):
    n = int(.035 * SR)
    return band(rng.standard_normal(n), 1200 * p, 5000) * env(n, 200) * .5


def pop(p):
    return tone(820 * p, .09, 45, sweep=.45) * .8


def tick(p):
    return tone(2600 * p, .025, 220) * .5


def ding(p):
    a = tone(1318.5 * p, .9, 5.5) + .55 * tone(1975.5 * p, .9, 7)
    a[:int(.5 * SR)] += .2 * tone(2637 * p, .5, 10)
    return a * .45


def notif(p):
    a = tone(784 * p, .35, 9) * .5
    b = tone(1046.5 * p, .55, 6) * .5
    out = np.zeros(int(.7 * SR)); out[:len(a)] += a; i = int(.11 * SR); out[i:i + len(b)] += b
    return out


def move(p):
    n = int(.12 * SR)
    knock = tone(190 * p, .12, 38) * .8 + band(rng.standard_normal(n), 700 * p, 2400) * env(n, 90) * .5
    return knock


def whoosh(p):
    n = int(.45 * SR)
    t = np.arange(n) / n
    x = band(rng.standard_normal(n), 500 * p, 4000) * np.sin(np.pi * t) ** 2
    return x * .35


def shimmer(p):
    out = np.zeros(int(1.0 * SR))
    for k, f in enumerate([1568, 1975.5, 2349, 3136]):
        a = tone(f * p, .7, 7) * .22; i = int(k * .055 * SR); out[i:i + len(a)] += a
    return out


SYNTH = dict(click=click, key=key, pop=pop, tick=tick, ding=ding, notif=notif, move=move, whoosh=whoosh, shimmer=shimmer)
for k, e in enumerate(events):
    sig = SYNTH[e["type"]](e.get("p", 1)) * e.get("g", 1)
    i = int(e["t"] * SR)
    sig = sig[: max(0, N - i)]
    pan = .5 + .18 * np.sin(k * 1.7)  # léger placement stéréo, déterministe
    L[i:i + len(sig)] += sig * (1 - pan) * 2 * .5
    R[i:i + len(sig)] += sig * pan * 2 * .5

peak = max(np.abs(L).max(), np.abs(R).max(), 1e-9)
g = min(1.0, .9 / peak)
pcm = (np.stack([L, R], 1) * g * 32767).astype("<i2")
with wave.open(os.path.join(ROOT, "build", "sfx.wav"), "w") as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print(f"{len(events)} bruitages → build/sfx.wav")
