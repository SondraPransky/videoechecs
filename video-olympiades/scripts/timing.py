"""Découpage des scènes de la vidéo « ronde 9 ».

Version musique seule : les durées sont fixes et multiples d'un temps à 120 BPM
(0,5 s), pour que les coupes tombent en rythme. Écrit build/timing.json (pour la
musique et le mixage), src/timing.js et src/contenu.js (pour l'animation).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRID = 0.5  # un temps à 120 BPM

# (scène, durée en secondes — multiple de GRID)
SCENES = [
    ("titre", 8.0),
    ("enbref", 10.0),
    ("match", 9.0),
    ("lagarde1", 22.0),
    ("lagarde2", 20.0),
    ("feminines", 18.0),
    ("gukesh", 12.0),
    ("classement", 12.0),
    ("final", 9.0),
]

for name, dur in SCENES:
    assert abs(dur / GRID - round(dur / GRID)) < 1e-9, f"{name} n'est pas un multiple de {GRID} s"

t = 0.0
scenes = []
for name, dur in SCENES:
    scenes.append({"id": name, "start": round(t, 3), "dur": dur})
    t += dur

timing = {"total": round(t, 3), "bpm": 120, "scenes": scenes, "vo": []}

os.makedirs(os.path.join(ROOT, "build"), exist_ok=True)
with open(os.path.join(ROOT, "build", "timing.json"), "w") as f:
    json.dump(timing, f, indent=1)
with open(os.path.join(ROOT, "src", "timing.js"), "w") as f:
    f.write("// Généré par scripts/timing.py — ne pas modifier à la main.\nwindow.TIMING = "
            + json.dumps(timing) + ";\n")

# Le contenu éditorial est embarqué en JS : la page est ouverte en file://, où un
# fetch() de fichier local est refusé par le navigateur.
with open(os.path.join(ROOT, "data", "contenu.json"), encoding="utf-8") as f:
    contenu = json.load(f)
with open(os.path.join(ROOT, "src", "contenu.js"), "w", encoding="utf-8") as f:
    f.write("// Généré par scripts/timing.py depuis data/contenu.json — ne pas modifier à la main.\n"
            "window.CONTENU = " + json.dumps(contenu, ensure_ascii=False) + ";\n")

for s in scenes:
    print(f'{s["id"]:11} {s["start"]:6.1f} → {s["start"] + s["dur"]:6.1f}')
print("total", timing["total"], "s")
