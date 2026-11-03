#!/usr/bin/env python3
"""Réponses des quiz pour les visuels « réponse » (story et carré du lendemain).
Lit les tableaux de réponses de pack/TEXTES-PUBLICATIONS.md et pack/QUIZ-ACADEMIE.md, écrit src/reponses.js :
window.REPONSES = { id: { r: indice de la bonne réponse, ex: "explication (HTML court)" } }.
Usage : python3 scripts/reponses.py"""
import json, re, pathlib
ICI = pathlib.Path(__file__).resolve().parent.parent
FIG = {"♔": "R", "♕": "D", "♖": "T", "♗": "F", "♘": "C"}
def lettres(s):   # ♘ f3 → Cf3 : la page remet les figurines elle-même
    return re.sub("([♔♕♖♗♘]) ?", lambda m: FIG[m.group(1)], s)
INTERJ = r"^(Bravo, c'est ça|Bravo|Exact|C'est ça|Bien vu|Parfait|Oui)\s*[!:]\s*"
rep = {}
for f in ("pack/TEXTES-PUBLICATIONS.md", "pack/QUIZ-ACADEMIE.md"):
    for ligne in (ICI / f).read_text().splitlines():
        m = re.match(r"\| `([0-9]{2}-[^/]+)/` [^|]*\|[^|]*\| \*\*([A-D]), (.+?)\*\*(.*?) \|", ligne)
        if not m: continue
        id_, lettre, gras, reste = m.groups()
        reste = re.sub(INTERJ, "", reste.strip().lstrip(".").strip()) if reste.strip().startswith((".", " ")) or reste.strip()[:1].isupper() else reste
        if not re.match(r"[a-h][1-8]", gras): gras = gras[0].upper() + gras[1:]   # pas de majuscule à une case (f7, a6)
        if reste[:1].islower() and not re.match(r"[a-h][1-8]", reste): reste = reste[0].upper() + reste[1:]
        ex = f"<b>{lettres(gras)}</b>" + ("" if reste.startswith((",", " :", ":", ".")) else " ") + lettres(re.sub(r"\*([^*]+)\*", r"<i>\1</i>", reste.strip() if not reste.startswith((",", " :", ":")) else reste))
        rep[id_] = {"r": "ABCD".index(lettre), "ex": ex.replace(" ,", ",")}
rep["16-quiz-carlsbad"] = {"r": 0, "ex": "<b>L'attaque de minorité.</b> Les Blancs avancent b4-b5 pour créer un pion faible chez les Noirs en c6. Le plan est expliqué pas à pas en Objectif 1600."}
(ICI / "src/reponses.js").write_text("// Généré par scripts/reponses.py : ne pas modifier à la main.\nwindow.REPONSES = " + json.dumps(rep, ensure_ascii=False, indent=1) + ";\n")
print(len(rep), "réponses")
