#!/usr/bin/env python3
"""Quiz des réseaux tirés des vrais quiz de l'académie (exports des modules, en JSON).
Usage : python3 -I scripts/quiz-academie.py DOSSIER_EXPORTS
Écrit src/quiz-academie.js (visuels ajoutés au catalogue) et pack/QUIZ-ACADEMIE.md (réponses et explications)."""
import json, glob, re, sys, pathlib
ICI = pathlib.Path(__file__).resolve().parent.parent
SRC = pathlib.Path(sys.argv[1])
NIV = {"course-1": "Initiation", "course-4": "Objectif 1400", "course-5": "Objectif 1600", "course-6": "Objectif 1800"}
# (leçon, début de la question, FEN facultative pour départager)
CHOIX = [
    ("echiquier-et-cases", "Combien de cases", None),
    ("echiquier-et-cases", "Comment sont appelées les lignes HORIZONTALES", None),
    ("l-echec-et-mat", "Les Blancs sont-ils échec et mat", "3k2r1"),
    ("le-roque", "Les Blancs peuvent-ils roquer", "r1b2rk1"),
    ("la-prise-en-passant", "Trait aux Blancs. Le dernier coup des Noirs", None),
    ("le-pat", "Trait aux Noirs - Mat ou Pat", "kN5R"),
    ("principes-d-ouverture", "Laquelle de ces pièces", None),
    ("creer-et-parer-une-menace", "Trait aux Blancs. Quel coup les Noirs menacent", "r4rk1/pppbqppp"),
    ("la-regle-du-carre", "Trait aux Noirs - Le Roi peut-il arrêter", "8/8/8/1P4k1"),
    ("les-pieges-d-ouverture", "Dans presque tous les pièges", None),
    ("la-scandinave", "Après 1.e4 d5 2.exd5 Qxd5", None),
    ("contrer-le-gambit-roi", "Face au gambit Roi", None),
    ("le-trebuchet", "Trait aux Blancs, étude de Walker", None),
    ("le-roi-cible-de-l-attaque", "Trait aux Blancs. Trois échecs", None),
    ("le-fegatello", "Trait aux Noirs. Les Blancs viennent de jouer 6.Nxf7", None),
    ("chercher-un-abri", "Où se trouve le talon d'Achille", None),
    ("le-sacrifice-de-fou-en-h7", "Un Cavalier adverse est en f6", None),
    ("la-triangulation", "Trait aux Noirs. C'est la position de départ", None),
    ("l-initiative", "Que veut dire avoir l'initiative", None),
    ("sauver-la-partie", "Trait aux Blancs. Après 1.Rb8+", None),
    ("la-defense-de-vancura", "Dans la défense de Vancura", None),
]
FR = {"K": "R", "Q": "D", "R": "T", "B": "F", "N": "C"}
def fr(s):   # notation française : Nf3 → Cf3, Qxd5 → Dxd5, Rb8+ → Tb8+ (seulement devant une case)
    return re.sub(r"(?<![A-Za-zÀ-ÿ])([KQRBN])(?=[a-h1-8]?x?[a-h][1-8])", lambda m: FR[m.group(1)], s or "")
def fen_pos(fen):
    pos, rows = {}, fen.split()[0].split("/")
    for r, row in enumerate(rows):
        f = 0
        for ch in row:
            if ch.isdigit(): f += int(ch); continue
            pos["abcdefgh"[f] + str(8 - r)] = ("w" if ch.isupper() else "b") + ch.upper()
            f += 1
    return pos
def slug(s): return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower().translate(str.maketrans("àâäéèêëîïôöùûüç’'", "aaaeeeeiioouuuc--")))).strip("-")

quiz = []
for f in sorted(glob.glob(str(SRC / "m*/*/*/quiz-*.json"))):
    p = pathlib.Path(f); les = p.parent.name; cours = p.parent.parent.name[:8]
    meta = json.loads((p.parent / "metadata.json").read_text())
    for q in json.loads(p.read_text())["questions"]:
        fen = (q.get("pgn") or "").split('"')[1] if "FEN" in (q.get("pgn") or "") else ""
        quiz.append(dict(les=les, titre=meta.get("title", ""), niv=NIV.get(cours, ""), q=q, fen=fen))
out, md = [], []
THEMES = ["ciel", "soleil", "menthe", "rose", "craie", "nuit"]
for n, (les, debut, fenk) in enumerate(CHOIX):
    c = [x for x in quiz if les in x["les"] and x["q"]["question"].replace("’", "'").startswith(debut.replace("’", "'")) and (not fenk or x["fen"].startswith(fenk))]
    assert c, (les, debut)
    x = c[0]; q = x["q"]; rep = q["answer"] - 1
    id_ = f"{65 + n}-academie-{slug(x['titre'])[:28].strip('-')}"
    v = {"id": id_, "tpl": "quizpos", "theme": THEMES[n % 6], "k": f"Quiz · {x['niv']}", "q": fr(q["question"]).replace("’", "'"),
         "opts": [fr(o).replace("’", "'") for o in q["choices"]], "s": "Réponds en commentaire !", "lecon": x["titre"]}
    if x["fen"]: v["pos"] = fen_pos(x["fen"])
    out.append(v)
    md.append(f"| `{id_}/` · {x['niv']} | {v['q']} | **{'ABCD'[rep]}, {v['opts'][rep]}.** {fr(q['choiceMessages'][rep]).replace('’', chr(39))} | {x['titre']} |")
js = "// Généré par scripts/quiz-academie.py à partir des quiz de l'académie : ne pas modifier à la main.\nwindow.VISUELS.push(\n" + \
     ",\n".join("  " + json.dumps(v, ensure_ascii=False) for v in out) + "\n);\n"
(ICI / "src/quiz-academie.js").write_text(js)
(ICI / "pack/QUIZ-ACADEMIE.md").write_text("# Quiz de l'académie pour les réseaux\n\n"
  "Questions reprises telles quelles des quiz des modules (Initiation, Objectif 1400, 1600 et 1800), avec leur position et leur explication.\n"
  "Publier la question, puis donner la réponse le lendemain (commentaire épinglé ou story), avec un renvoi vers la leçon.\n\n"
  "| Visuel | Question | Réponse et explication | Leçon de l'académie |\n|---|---|---|---|\n" + "\n".join(md) + "\n")
print(len(out), "quiz")
