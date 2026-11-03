#!/usr/bin/env python3
"""Textes alternatifs (accessibilité) de toutes les images du pack : pack/TEXTES-ALTERNATIFS.md.
Lit le catalogue src/visuels-data.js (via node) ; les descriptions des captures et des poses sont ci-dessous."""
import json, re, subprocess, pathlib
ICI = pathlib.Path(__file__).resolve().parent.parent
js = 'global.window={};require("./src/visuels-data.js");require("./src/quiz-academie.js");console.log(JSON.stringify(window.VISUELS))'
VIS = json.loads(subprocess.check_output(["node", "-e", js], cwd=ICI))

CAPTURE = {
    "progression": "un échiquier en position de départ et le parcours de niveaux, de l'initiation à 2000 et plus",
    "progres": "une carte de module validé avec trois étoiles et une courbe de classement Elo qui monte",
    "lecons": "les quatre formats de leçon : vidéo, cours écrit, exercice et quiz",
    "exercices": "une carte d'exercice « mat en 1 » et une carte de quiz",
    "videos": "le lecteur vidéo de la Minute Finale et les cartes des auteurs d'Europe Échecs",
    "masterclasses": "une masterclass en direct : échiquier, caméra du coach et nombre de spectateurs",
    "parties": "un échiquier de partie importée et la fenêtre de partage avec d'autres membres",
    "revue": "la couverture du numéro 779 de la revue et la liste des articles en PGN",
    "forum": "la liste des sujets du forum avec des réponses de membres et de coachs",
    "tournois": "le classement en direct d'un tournoi en ligne",
}
POSE = {
    "niveau-superieur": "monte un escalier", "serie-reussie": "célèbre une série réussie", "idee": "a une idée",
    "bonne-reponse": "lève le poing, contente", "regarde": "regarde une vidéo", "lecon-terminee": "salue, leçon terminée",
    "reflexion": "réfléchit", "lecture": "lit", "serie-de-jours": "coche les jours d'une série", "victoire-tournoi": "fête une victoire",
    "saut-etoile": "saute de joie", "lit-assise": "lit, assise", "gratte-tete": "se gratte la tête", "hourra": "lève les bras de joie",
    "haussement": "hausse les épaules", "sprint": "court à toute vitesse", "reverence": "fait une révérence",
    "parapluie": "s'abrite sous un parapluie", "sieste": "fait la sieste", "champion": "brandit un trophée",
    "montre-le-ciel": "pointe une étoile du doigt", "pendule": "est à côté d'une pendule d'échecs", "message-recu": "reçoit une lettre",
    "coucou-autre-main": "fait coucou", "cafe": "boit un café", "discute": "discute, une bulle au-dessus de la tête",
    "drapeau": "plante un drapeau", "pancarte": "tient une pancarte", "blancs-ou-noirs": "tient un pion blanc et un pion noir",
    "yoga-arbre": "fait la posture de l'arbre", "oups": "se tient la tête, oups", "danse": "danse", "prof": "porte une toque de diplômé",
}
def txt(x): return re.sub(r"<[^>]+>|&#8239;", lambda m: "" if m.group(0).startswith("<") else " ", x or "").strip()
def mascotte(p): return f"La mascotte jaune d'echecs.com {POSE.get(p, 'est là')}." if p else ""
def phrase(*parts): return " ".join(p for p in parts if p)

def alt(v):
    t, e, s, k = txt(v.get("t")), txt(v.get("e")), txt(v.get("s")), txt(v.get("k"))
    tpl = v["tpl"]
    if tpl == "accroche": return phrase(f"echecs.com — {k} : « {t} {e} » {s}", f"Capture de l'académie : {CAPTURE.get(v.get('shot'), '')}.", mascotte(v.get("pose")))
    if tpl == "chiffre": return phrase(f"echecs.com : « {txt(v.get('n'))} {t} {e} »", s, mascotte(v.get("pose")))
    if tpl == "puzzle" and "solution" in v["id"]:
        return phrase(f"Solution du problème du jour : {t}, {e} {s}", "Échiquier : la Tour blanche monte de d1 à d8 et fait mat, le Roi noir en g8 étant bloqué par ses pions f7, g7 et h7.")
    if tpl == "puzzle":
        return phrase(f"Problème du jour : « {t} {e} » {s}", "Échiquier : Roi blanc g1, Tour blanche d1, pions blancs f2, g2, h2 ; Roi noir g8, Dame noire b2, pions noirs a7, f7, g7, h7.")
    if tpl == "quizpos":
        return phrase(f"echecs.com — {k} : {txt(v['q'])}", " ".join(f"{'ABCD'[i]} : {o}." for i, o in enumerate(v["opts"])),
                      "Avec la position sur l'échiquier." if v.get("pos") else "", f"Question tirée de la leçon « {v.get('lecon', '')} » de l'académie.")
    if tpl == "quiz":
        return phrase(f"echecs.com — {k} : {txt(v['q'])}", " ".join(f"{'ABC'[i]} : {o}." for i, o in enumerate(v["opts"])), s, mascotte(v.get("pose")))
    if tpl == "coach": return phrase(f"Nos coachs : portrait de {t}, {e.rstrip('.').lower()}.", s)
    if tpl == "revue": return phrase(f"La revue Europe Échecs : « {t} {e} » {s}", "Couverture du numéro 779 avec Sophie Milliet et Étienne Bacrot.")
    if tpl == "event": return phrase(f"Tournois en ligne echecs.com : « {t} {e} »", ", ".join(txt(f) for f in v["facts"]) + ".", mascotte(v.get("pose")))
    if tpl == "mascotte": return phrase(f"echecs.com — {k} : « {t} {e} »", mascotte(v.get("pose")))
    if tpl == "id-avatar": return "Logo echecs.com : le Cavalier et le nom echecs.com."
    if tpl == "id-ban": return phrase("Bannière echecs.com : « Progresse à ton rythme. » +200 leçons, +2 000 exercices, masterclasses, tournois, forum.", mascotte(v.get("pose")))
    if tpl == "id-hl": return f"Couverture de story à la une : {v['label']}."
    return ""

DOSSIER = {v["id"]: v["id"] for v in VIS}
out = ["# Textes alternatifs — images du pack", "",
       "Le texte alternatif décrit l'image aux personnes malvoyantes (lecteurs d'écran) et aide le référencement.",
       "Où le coller : Instagram et Facebook, « Paramètres avancés » puis « Texte alternatif » ; X, « Ajouter une description » ;",
       "LinkedIn, « Texte alternatif » sur l'image. Le même texte vaut pour tous les formats d'un visuel.", "",
       "## Visuels par sujet (`images/`)", ""]
for v in VIS:
    if v["tpl"].startswith("id-"): continue
    out += [f"**`{v['id']}/`**", f"> {alt(v)}", ""]
out += ["## Identité (`images/00-identite/`)", ""]
for v in VIS:
    if v["tpl"].startswith("id-"): out += [f"**`{v['id']}`**", f"> {alt(v)}", ""]

PUBS = {1: ("Tu enchaînes les parties, mais ton classement ne bouge pas ?", "une carte de classement Elo bloqué à 1 201, ± 0 en 3 mois",
            "Jouer ne suffit pas. Entraîne-toi avec méthode.", "une courbe Elo qui monte jusqu'à 1 412 et les modules Tactique, Finales et Ouvertures validés",
            "Un programme par niveau, de l'initiation à 2000+."),
        2: ("Tu joues beaucoup, mais tu n'as pas l'impression de progresser ?", "une carte avec 247 parties jouées ce mois-ci",
            "Joue moins, comprends plus.", "l'analyse d'une partie qui repère une erreur, puis des exercices ciblés sur le clouage",
            "Analyse tes parties, puis +2 000 exercices ciblés."),
        3: ("Tu as l'impression de stagner depuis quelque temps ?", "une barre de progression bloquée à 40 % de janvier à juin",
            "Pour passer un cap, apprends des meilleurs.", "les cartes des coachs en masterclass en direct : Fabien Libiszewski, Gata Kamsky, Sylvain Ravot et Marc Quenehen",
            "Maîtres et grands maîtres, en direct chaque semaine."),
        4: ("Tu regardes des vidéos d'échecs, mais tu ne progresses pas ?", "12 heures de vidéos regardées, classement inchangé",
            "Passe à l'action : chaque leçon se joue !", "une leçon vidéo de la Minute Finale qui devient un exercice « À toi de jouer », avec la bonne réponse",
            "Vidéo, cours, exercice, quiz : tu pratiques tout de suite."),
        5: ("Tu veux progresser aux échecs, mais tu ne sais pas par où commencer ?", "un panneau indicateur : Ouvertures, Tactique, Finales, Stratégie",
            "Suis le guide, étape par étape.", "un parcours de l'initiation à 2000 et plus, avec la mention « Tu es ici »",
            "Un parcours clair, du premier coup à 2000+.")}
out += ["## Publicités en images (`images/00-publicites/pub-N/`)", ""]
for n, (q, pv, st, sv, cap) in PUBS.items():
    out += [f"**`pub-{n}-1-question`**", f"> « {q} » La mascotte jaune d'echecs.com, perplexe, à côté d'{pv}.", "",
            f"**`pub-{n}-2-reponse`**", f"> Le déclic : « {st} » Illustration : {sv}. {cap}", "",
            f"**`pub-{n}-3-final`**", "> Logo echecs.com, « L'Académie » et bouton « Commencer maintenant ».", ""]
out += ["## Images générales (`images/00-general/`)", "",
        "> echecs.com : « Progresse à ton rythme. » L'Académie echecs.com : +200 leçons, +2 000 exercices, masterclasses, tournois et forum. La mascotte jaune d'echecs.com à côté d'un échiquier.", ""]
FAN_RE = re.compile(r"(?<![A-Za-zÀ-ÿ])([RDTFC])(?=[a-h1-8]?x?[a-h][1-8])")
def fan(s):   # notation figurine Unicode dans les textes : Cf3 → ♘f3
    return FAN_RE.sub(lambda m: {"R": "♔", "D": "♕", "T": "♖", "F": "♗", "C": "♘"}[m.group(1)] + "\u202f", s)   # espace fine insécable entre la figurine et la case
(ICI / "pack/TEXTES-ALTERNATIFS.md").write_text(fan("\n".join(out)))
print(len(out), "lignes")
