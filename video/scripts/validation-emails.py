#!/usr/bin/env python3
"""Page de validation des e-mails, séparée de celle du pack (publicités, vidéos, visuels).
Chaque fiche affiche le vrai e-mail (HTML), en largeur téléphone, tablette ou ordinateur, avec les avis et la décision finale.
Lit build/_emails_artefact/ (généré par scripts/emails.py) et pack/EMAILS.md (catalogue).
Usage : python3 scripts/validation-emails.py DOSSIER_SORTIE [abonnes|ccas]   (le gabarit de page est validation/emails.html)"""
import json, re, shutil, sys, pathlib
ICI = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]); (OUT / "media").mkdir(parents=True, exist_ok=True)
PROFIL = sys.argv[2] if len(sys.argv) > 2 else "abonnes"; SUF = "" if PROFIL == "abonnes" else "-" + PROFIL
SRC = ICI / f"build/_emails{SUF}_artefact"
DOC = ICI / ("pack/EMAILS.md" if PROFIL == "abonnes" else f"pack/EMAILS-{PROFIL.upper()}.md")
shutil.rmtree(OUT / "emails", ignore_errors=True); shutil.copytree(SRC, OUT / "emails")
# Version sombre de chaque e-mail (le bouton « Sombre » de la page) : les règles @media (prefers-color-scheme: dark) appliquées d'office,
# comme Apple Mail, l'iPhone ou Outlook.com en thème sombre
(OUT / "emails/sombre").mkdir()
for f in SRC.glob("*.html"):
    h = f.read_text().replace("@media (prefers-color-scheme: dark)", "@media all").replace('src="img/', 'src="../img/').replace('url(img/', 'url(../img/')
    (OUT / "emails/sombre" / f.name).write_text(h)
PRE = "email-" if PROFIL == "abonnes" else PROFIL + "-"
NB = len(list(SRC.glob("*.html")))
page = (ICI / "validation/emails.html").read_text().replace("{{NB}}", str(NB))
if PROFIL == "ccas":   # page des bénéficiaires des Activités Sociales de l'Énergie
    page = (page.replace("<title>E-mails de l’Académie</title>", "<title>E-mails CCAS</title>")
                .replace("<h1>Les e-mails de <em>l’Académie</em></h1>", "<h1>Les e-mails <em>CCAS</em></h1>")
                .replace("envoyés aux membres, de la création du compte à la fin d’abonnement", "envoyés aux bénéficiaires des Activités Sociales de l’Énergie (accès offert, sans abonnement ni paiement), de la création du compte au bilan de l’année")
                .replace("Léa, 18 nov., Gata Kamsky", "Léa, 18 nov., Éric et Florian"))
(OUT / "index.html").write_text(page)
VERS = json.loads((ICI / "pack/validation-versions.json").read_text())

sections, cat = [], None
for l in DOC.read_text().splitlines():
    if l.startswith("### "):
        cat = l[4:].strip(); sections.append({"id": re.sub(r"[^a-z0-9]+", "-", cat.lower().translate(str.maketrans("éèêàâçôîû", "eeeaacoiu"))).strip("-"), "titre": cat, "items": []}); continue
    m = re.match(r"\| `([0-9]{2}-[^`]+)\.html` \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", l)
    if not m or not sections: continue
    fid, quand, objet, pre, typ = m.groups()
    src = f"emails/{fid}.html"
    sections[-1]["items"].append({"id": PRE + fid, "titre": f"{fid[:2]} · {objet}", "sous": f"{quand} · {typ}",
        "pre": pre, "v": VERS.get(PRE + fid, 1),
        "medias": [{"type": "html", "src": src, "w": 375, "label": "Téléphone"}, {"type": "html", "src": src, "w": 320, "label": "Petit téléphone"},
                   {"type": "html", "src": src, "w": 768, "label": "Tablette"}, {"type": "html", "src": src, "w": 1280, "label": "Ordinateur"}]})
# Le mode sombre se voit sur chaque fiche (bouton Clair / Sombre) : plus de captures à part
for f in (OUT / "media").glob("sombre-*.jpg"): f.unlink()
(OUT / "media/manifest.json").write_text(json.dumps({"sections": sections}, ensure_ascii=False))
print(len(sections), "rubriques,", sum(len(s["items"]) for s in sections), "fiches")
