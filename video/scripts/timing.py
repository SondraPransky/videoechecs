"""Calcule le découpage des scènes.

Mode voix off (par défaut) : chaque scène dure au moins `min` secondes, et assez
pour contenir sa réplique (départ `lead` + durée + `tail`).
Mode --music-only : durées fixes (MUSIC_ONLY).
Les coupes sont arrondies à la demi-seconde, soit un temps à 120 BPM, pour tomber
en rythme avec la musique. Écrit build/timing.json (musique, mixage) et
src/timing.js (animation).
"""
import json
import math
import os
import sys
import wave

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRID = 0.5  # un temps à 120 BPM

# (scène, réplique de voice/script.txt ou None, lead, min, tail)
SCENES = [
    ("s1", "01", 0.3, 4.0, 0.5),
    ("s2", "02", 0.2, 4.5, 0.5),
    ("s3", "03", 0.2, 4.5, 0.4),
    ("revue", None, 0.2, 5.0, 0.4),
    ("videos", None, 0.2, 6.0, 0.4),
    ("s4", "04", 0.2, 4.5, 0.4),
    ("s5", "05", 0.2, 4.0, 0.4),
    ("s6", "06", 0.2, 4.5, 0.4),
    ("s7", "07", 0.2, 4.5, 0.4),
    ("s8", "08", 0.4, 6.5, 1.5),
]
# Mode --music-only : durées fixes (secondes, multiples d'un temps)
MUSIC_ONLY = {"s1": 3.5, "s2": 4.0, "s3": 4.0, "revue": 5.0, "videos": 6.0,
              "s4": 4.0, "s5": 7.0, "s6": 5.0, "s7": 4.0, "s8": 5.5}
music_only = "--music-only" in sys.argv


def wav_dur(path):
    with wave.open(path) as w:
        return w.getnframes() / w.getframerate()


t = 0.0
scenes, vo = [], []
for name, vo_id, lead, mn, tail in SCENES:
    if music_only:
        dur = MUSIC_ONLY[name]
    elif vo_id:
        d = wav_dur(os.path.join(ROOT, "voice", "out", f"{vo_id}.wav"))
        dur = math.ceil(max(mn, lead + d + tail) / GRID) * GRID
        vo.append({"id": vo_id, "at": round(t + lead, 3), "dur": round(d, 3)})
    else:
        dur = mn
    scenes.append({"id": name, "start": t, "dur": dur})
    t += dur

timing = {"total": t, "bpm": 120, "scenes": scenes, "vo": [] if music_only else vo}
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
with open(os.path.join(ROOT, "build", "timing.json"), "w") as f:
    json.dump(timing, f, indent=1)
with open(os.path.join(ROOT, "src", "timing.js"), "w") as f:
    f.write("// Généré par scripts/timing.py — ne pas modifier à la main.\nwindow.TIMING = " + json.dumps(timing) + ";\n")
for s in scenes:
    print(f'{s["id"]:7} {s["start"]:5.1f} → {s["start"] + s["dur"]:5.1f}')
print("total", t)
