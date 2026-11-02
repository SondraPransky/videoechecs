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
    ("s3", "03", 0.2, 4.5, 0.4),
    ("s6", "06", 0.2, 4.5, 0.4),
    ("prog", None, 0.2, 5.0, 0.4),
    ("videos", None, 0.2, 6.0, 0.4),
    ("s4", "04", 0.2, 4.5, 0.4),
    ("s5", "05", 0.2, 4.0, 0.4),
    ("revue", None, 0.2, 5.0, 0.4),
    ("forum", None, 0.2, 5.0, 0.4),
    ("s7", "07", 0.2, 4.5, 0.4),
    ("s8", "08", 0.4, 6.5, 1.5),
]
# Mode --music-only : durées fixes (secondes, multiples d'un temps)
MUSIC_ONLY = {"hook": 4.0, "sol": 2.5, "s1": 6.0, "prog": 5.0, "s3": 4.0, "revue": 5.0, "videos": 6.0,
              "s4": 5.0, "s5": 6.0, "s6": 5.0, "forum": 5.0, "s7": 4.0, "s8": 5.5}
# Déclinaisons courtes (toujours en musique seule) : sous-ensembles de scènes
EDITIONS = {
    "court": ["s1", "s3", "prog", "s4", "forum", "s8"],   # ~30 s pour les réseaux
    "boucle": ["s3", "s6", "prog"],                       # boucle muette de l'en-tête du site
    # Pack réseaux : une mini-vidéo par pan de l'académie, toujours conclue par l'écran final
    "pan-progression": ["s1", "prog", "s8"],
    "pan-lecons": ["s3", "s8"],
    "pan-exercices": ["s6", "s8"],
    "pan-videos": ["videos", "s8"],
    "pan-masterclasses": ["s4", "s8"],
    "pan-parties": ["s5", "s8"],
    "pan-revue": ["revue", "s8"],
    "pan-forum": ["forum", "s8"],
    "pan-tournois": ["s7", "s8"],
    # Publicités : une question-accroche, la réponse, puis l'essentiel de l'académie (~31 s)
    **{f"accroche-{k}": ["hook", "sol", "s3", "prog", "s4", "forum", "s8"] for k in range(1, 6)},
}
music_only = "--music-only" in sys.argv
edition = sys.argv[sys.argv.index("--edition") + 1] if "--edition" in sys.argv else "long"


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

timings = {"long": {"total": t, "bpm": 120, "scenes": scenes, "vo": [] if music_only else vo}}
for name, ids in EDITIONS.items():
    t2, sc = 0.0, []
    for i in ids:
        sc.append({"id": i, "start": t2, "dur": MUSIC_ONLY[i]})
        t2 += MUSIC_ONLY[i]
    timings[name] = {"total": t2, "bpm": 120, "scenes": sc, "vo": []}
timing = timings[edition]
scenes, t = timing["scenes"], timing["total"]
os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
with open(os.path.join(ROOT, "build", "timing.json"), "w") as f:
    json.dump(timing, f, indent=1)
with open(os.path.join(ROOT, "src", "timing.js"), "w") as f:
    f.write("// Généré par scripts/timing.py — ne pas modifier à la main.\n"
            "// Déclinaison choisie par ?edition=court|boucle dans l'URL (par défaut : la vidéo longue).\n"
            "window.TIMINGS = " + json.dumps(timings) + ";\n"
            "window.TIMING = window.TIMINGS[new URLSearchParams(location.search).get(\"edition\") || \"long\"];\n")
for s in scenes:
    print(f'{s["id"]:7} {s["start"]:5.1f} → {s["start"] + s["dur"]:5.1f}')
print("total", t)
