"""Calcule le découpage des scènes à partir des durées de la voix off.

Chaque scène dure au moins `min` secondes, et assez pour contenir sa réplique
(départ `lead` + durée + `tail`). Les coupes sont arrondies à la demi-seconde,
soit un temps à 120 BPM, pour tomber en rythme avec la musique.
Écrit build/timing.json (musique, mixage) et src/timing.js (animation).
"""
import json
import math
import os
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRID = 0.5  # un temps à 120 BPM

# Mode --music-only : pas de voix off, durées fixes (secondes, multiples d'un temps)
MUSIC_ONLY = {"s1": 3.5, "s2": 4.0, "s3": 6.0, "s4": 4.0, "s5": 4.0, "s6": 5.0, "s7": 4.0, "s8": 5.5}
music_only = "--music-only" in sys.argv

# (lead, min, tail) par scène
SCENES = [
    ("s1", 0.3, 4.0, 0.5),
    ("s2", 0.2, 4.5, 0.5),
    ("s3", 0.2, 7.0, 0.4),
    ("s4", 0.2, 4.5, 0.4),
    ("s5", 0.2, 4.0, 0.4),
    ("s6", 0.2, 4.0, 0.4),
    ("s7", 0.2, 4.5, 0.4),
    ("s8", 0.4, 6.5, 1.5),
]


def wav_dur(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


t = 0.0
scenes, vo = [], []
for i, (name, lead, mn, tail) in enumerate(SCENES, start=1):
    if music_only:
        d, dur = 0.0, MUSIC_ONLY[name]
    else:
        d = wav_dur(os.path.join(ROOT, "voice", "out", f"{i:02d}.wav"))
        dur = math.ceil(max(mn, lead + d + tail) / GRID) * GRID
    scenes.append({"id": name, "start": t, "dur": dur})
    vo.append({"id": f"{i:02d}", "at": round(t + lead, 3), "dur": round(d, 3)})
    t += dur

timing = {"total": t, "bpm": 120, "scenes": scenes, "vo": [] if music_only else vo}
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
with open(os.path.join(ROOT, "build", "timing.json"), "w") as f:
    json.dump(timing, f, indent=1)
with open(os.path.join(ROOT, "src", "timing.js"), "w") as f:
    f.write("// Généré par scripts/timing.py — ne pas modifier à la main.\nwindow.TIMING = " + json.dumps(timing) + ";\n")
for s in scenes:
    print(f'{s["id"]}  {s["start"]:5.1f} → {s["start"] + s["dur"]:5.1f}')
print("total", t)
