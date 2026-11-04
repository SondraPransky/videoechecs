#!/usr/bin/env python3
"""Page de validation des e-mails, séparée de celle du pack (publicités, vidéos, visuels).
Chaque fiche affiche le vrai e-mail (HTML), en largeur téléphone, tablette ou ordinateur, avec les avis et la décision finale.
Lit build/_emails_artefact/ (généré par scripts/emails.py) et pack/EMAILS.md (catalogue).
Usage : python3 scripts/validation-emails.py DOSSIER_SORTIE   (le gabarit de page est validation/emails.html)"""
import json, re, shutil, sys, pathlib
ICI = pathlib.Path(__file__).resolve().parent.parent
OUT = pathlib.Path(sys.argv[1]); (OUT / "media").mkdir(parents=True, exist_ok=True)
SRC = ICI / "build/_emails_artefact"
shutil.rmtree(OUT / "emails", ignore_errors=True); shutil.copytree(SRC, OUT / "emails")
shutil.copy(ICI / "validation/emails.html", OUT / "index.html")
VERS = json.loads((ICI / "pack/validation-versions.json").read_text())

sections, cat = [], None
for l in (ICI / "pack/EMAILS.md").read_text().splitlines():
    if l.startswith("### "):
        cat = l[4:].strip(); sections.append({"id": re.sub(r"[^a-z0-9]+", "-", cat.lower().translate(str.maketrans("éèêàâçôîû", "eeeaacoiu"))).strip("-"), "titre": cat, "items": []}); continue
    m = re.match(r"\| `([0-9]{2}-[^`]+)\.html` \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", l)
    if not m or not sections: continue
    fid, quand, objet, pre, typ = m.groups()
    src = f"emails/{fid}.html"
    sections[-1]["items"].append({"id": "email-" + fid, "titre": f"{fid[:2]} · {objet}", "sous": f"{quand} · {typ}",
        "pre": pre, "v": VERS.get("email-" + fid, 1),
        "medias": [{"type": "html", "src": src, "w": 375, "label": "Téléphone"}, {"type": "html", "src": src, "w": 320, "label": "Petit téléphone"},
                   {"type": "html", "src": src, "w": 768, "label": "Tablette"}, {"type": "html", "src": src, "w": 1280, "label": "Ordinateur"}]})
sombre = sorted((ICI / "build/pack/emails/apercus/sombre").glob("*.jpg"))
if sombre:
    for f in sombre: shutil.copy(f, OUT / "media" / ("sombre-" + f.name))
    sections.append({"id": "mode-sombre", "titre": "Mode sombre", "items": [{"id": "email-mode-sombre", "titre": "Mode sombre · exemples",
        "sous": "Apple Mail, iPhone, Outlook.com en thème sombre (Gmail applique sa propre inversion)", "pre": "", "v": VERS.get("email-mode-sombre", 1),
        "medias": [{"type": "image", "src": "media/sombre-" + f.name, "label": "E-mail " + f.stem[:2]} for f in sombre]}]})
(OUT / "media/manifest.json").write_text(json.dumps({"sections": sections}, ensure_ascii=False))
print(len(sections), "rubriques,", sum(len(s["items"]) for s in sections), "fiches")
