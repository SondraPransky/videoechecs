#!/usr/bin/env python3
"""Prépare la page de validation du pack : aperçus allégés (images 800 px, vidéos 960 px) et manifest.json.
Usage : python3 scripts/validation.py DOSSIER_SORTIE   (lit build/pack/ ; versions des fiches dans pack/validation-versions.json)"""
import json, re, subprocess, sys, pathlib
from PIL import Image
ICI = pathlib.Path(__file__).resolve().parent.parent
PACK = ICI / "build/pack"
OUT = pathlib.Path(sys.argv[1]); MED = OUT / "media"; MED.mkdir(parents=True, exist_ok=True)
FF = subprocess.check_output(["python3", "-c", "import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())"]).decode().strip()
VERS = json.loads((ICI / "pack/validation-versions.json").read_text()) if (ICI / "pack/validation-versions.json").exists() else {}
def nb(f): return re.sub(r"[^a-z0-9.-]+", "-", str(f.relative_to(PACK)).lower())

def img(f):
    dst = MED / (nb(f).rsplit(".", 1)[0] + ".jpg")
    if not dst.exists() or dst.stat().st_mtime < f.stat().st_mtime:   # refait si la source a changé
        im = Image.open(f).convert("RGB"); im.thumbnail((800, 800) if im.height < 2 * im.width else (640, 9000)); im.save(dst, quality=80, optimize=True)   # e-mails : pleine hauteur
    w, h = Image.open(f).size
    return {"type": "image", "src": "media/" + dst.name, "w": w, "h": h}

def vid(f):
    dst = MED / nb(f)
    out = subprocess.run([FF, "-i", str(f)], capture_output=True, text=True).stderr
    m = re.search(r"Video:.*?(\d{3,4})x(\d{3,4})", out); w, h = int(m.group(1)), int(m.group(2))
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", out); dur = int(d.group(2)) * 60 + float(d.group(3))
    if not dst.exists() or dst.stat().st_mtime < f.stat().st_mtime:   # refait si la source a changé
        sc = "scale=960:-2" if w >= h else "scale=-2:960"
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(f), "-vf", sc, "-c:v", "libx264", "-preset", "medium", "-crf", "29",
                        "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(dst)], check=True)
    return {"type": "video", "src": "media/" + dst.name, "w": w, "h": h, "dur": round(dur, 1)}

ETIQ = [("reponse-story", "Réponse · story 9:16"), ("reponse-carre", "Réponse · carré"), ("story-9x16-jaune", "Story 9:16 · fond jaune"), ("9x16", "Vertical 9:16"), ("story-1080x1920", "Story 9:16"), ("story", "Story 9:16"),
        ("4x5", "Portrait 4:5"), ("feed", "Portrait 4:5"), ("portrait", "Portrait 4:5"), ("1x1", "Carré 1:1"), ("carre", "Carré 1:1"),
        ("16x9", "Paysage 16:9"), ("x-1600x900", "X 16:9"), ("lien-120", "Lien partagé"), ("pinterest", "Pinterest 2:3"),
        ("avatar", "Photo de profil"), ("banniere", "Bannière"), ("a-la-une", "Story à la une")]
def etiquette(f):
    n = f.name.lower(); lab = next((l for k, l in ETIQ if k in n), f.stem)
    if f.parent.name == "apercus": return "Aperçu sur téléphone"
    if f.parent.name == "sombre": return "Mode sombre · " + f.stem[:2]
    if f.parent.name == "ordinateur": return "Ordinateur · " + f.stem[:2]
    if "jaune" in n and "jaune" not in lab: lab += " · fond jaune"
    for k, l in [("facebook", "Facebook"), ("linkedin", "LinkedIn"), ("youtube", "YouTube"), ("-x-1500", "X")]:
        if k in n and "banniere" in n: lab = "Bannière " + l + (" · soleil" if "soleil" in n else "")
    if "avatar" in n: lab = "Photo de profil" + (" · soleil" if "soleil" in n else " · nuit")
    if n.startswith("carrousel-"): lab = "Diapo " + n.split("-portrait")[0].rsplit("-", 1)[1]
    if "a-la-une" in n: lab = "À la une · " + n.split("a-la-une-")[1].split("-")[0].capitalize()
    return lab
def media(files, kind):
    out = []
    for f in files:
        m = vid(f) if kind == "video" else img(f); m["label"] = etiquette(f); out.append(m)
    return out
def item(id_, titre, sous, files, kind):
    return {"id": id_, "titre": titre, "sous": sous, "v": VERS.get(id_, 1), "medias": media(files, kind)}

V, I = PACK / "videos", PACK / "images"
ORDRE_V = ["16x9", "4x5", "1x1", "9x16", "story-9x16.mp4", "story-9x16-jaune", "feed", "carre"]
def tri(fs, ordre):
    return sorted(fs, key=lambda f: 98 if "reponse" in f.name else next((i for i, k in enumerate(ordre) if k in f.name), 97))
S = []
S.append({"id": "motion", "titre": "Motion — version longue", "items": [
    item("motion-longue", "Présentation de l'académie", "56 s · 16:9 · YouTube, site, LinkedIn", [V / "00-general/presentation-longue-16x9.mp4"], "video")]})
S.append({"id": "generales", "titre": "Vidéos générales", "items": [
    item("video-courte", "Présentation courte", "30 s · 4 formats (le 9:16 est la nouvelle version verticale)",
         tri(list((V / "00-general").glob("presentation-courte-*.mp4")), ORDRE_V), "video"),
    item("video-boucle", "Boucle d'en-tête du site", "14 s · muette · se répète en fond", [V / "00-general/boucle-entete-site-muette-1920x1080.mp4"], "video")]})
QS = {1: "Tu enchaînes les parties…", 2: "Tu joues beaucoup…", 3: "Tu as l'impression de stagner…", 4: "Tu regardes des vidéos d'échecs…", 5: "Tu veux progresser…"}
S.append({"id": "pubs", "titre": "Publicités 16 s", "items": [
    item(f"pub-{q}", f"Pub {q} · {QS[q]}", "16 s · 5 formats", tri(list((V / "00-publicites").glob(f"pub-{q}-*.mp4")), ["story-9x16.mp4", "feed", "carre", "16x9", "jaune"]), "video") for q in QS]})
ORDRE_I = ["story-1080x1920.jpg", "portrait", "carre-1080x1080.jpg", "x-1600", "lien", "pinterest", "jaune"]
S.append({"id": "pubs-images", "titre": "Publicités en images", "items": [
    item(f"pub-images-{q}", f"Pub {q} en images", "3 vues (question, réponse, final), seules ou en carrousel",
         [f for vue in ("1-question", "2-reponse", "3-final") for f in tri([g for g in (I / f"00-publicites/pub-{q}").glob(f"pub-{q}-{vue}-*.jpg") if "jaune" not in g.name and ("story" in g.name or "carre" in g.name or "lien" in g.name)], ORDRE_I)], "image") for q in QS]})
for m in S[-1]["items"]:
    for x in m["medias"]: x["label"] = {"1-q": "Question", "2-r": "Réponse", "3-f": "Final"}[x["src"].split(f"pub-")[-1].split("-", 1)[1][:3]] + " · " + x["label"]
S.append({"id": "accroches", "titre": "Publicités 31 s (première version)", "items": [
    item(f"accroche-{q}", f"Accroche {q} · {QS[q]}", "31 s · 16:9 et story", tri(list((V / "00-accroches").glob(f"accroche-{q}-*.mp4")), ["16x9", "story"]), "video") for q in QS]})
th = sorted(d for d in V.iterdir() if d.is_dir() and re.match(r"\d\d-", d.name) and not d.name.startswith("00"))
S.append({"id": "themes", "titre": "Vidéos par thème", "items": [
    item("theme-" + d.name[3:], d.name[3:].replace("-", " ").capitalize(), "10 à 17 s · 4 formats", tri(list(d.glob("*.mp4")), ORDRE_V), "video") for d in th]})
vi = sorted(d for d in I.iterdir() if d.is_dir() and re.match(r"\d\d-", d.name) and not d.name.startswith("00"))
data = {v["id"]: v for v in json.loads(subprocess.check_output(["node", "-e", 'global.window={};require("./src/visuels-data.js");require("./src/quiz-academie.js");console.log(JSON.stringify(window.VISUELS))'], cwd=ICI))}
FAN_RE = re.compile(r"(?<![A-Za-zÀ-ÿ])([RDTFC])(?=[a-h1-8]?x?[a-h][1-8])")
def fan(s):   # notation figurine Unicode dans les textes : Cf3 → ♘f3
    return FAN_RE.sub(lambda m: {"R": "♔", "D": "♕", "T": "♖", "F": "♗", "C": "♘"}[m.group(1)] + "\u202f", s)   # espace fine insécable entre la figurine et la case
def titre_vis(d):
    v = data.get(d.name, {}); t = " ".join(x for x in (v.get("t"), v.get("e")) if x) or v.get("q", d.name)
    return fan(re.sub(r"<[^>]+>|&#8239;", "", t))
GARDE_Q = ("-carre-1080x1080.jpg", "-story-1080x1920.jpg", "reponse-story-1080x1920.jpg")   # quiz : carré, story + la réponse (limite de fichiers de la page)
GARDE = ("carre-1080x1080.jpg", "portrait-1080x1350.jpg", "story-1080x1920.jpg", "lien-1200x630.jpg")   # 4 formats par visuel (limite de fichiers de la page)
S.append({"id": "visuels", "titre": "Visuels", "items": [
    item("visuel-" + d.name, f"{d.name[:2]} · {titre_vis(d)}", (data.get(d.name, {}).get("k") or "") + " · 6 formats dans le pack, 4 ici", tri([f for f in d.glob("*.jpg") if f.name.endswith(GARDE)], ORDRE_I), "image") for d in vi if not d.name[3:].startswith(("quiz", "academie"))]})
S.append({"id": "quiz", "titre": "Quiz", "items": [
    item("visuel-" + d.name, f"{d.name[:2]} · {titre_vis(d)}", (data.get(d.name, {}).get("k") or "") + " · 6 formats + réponse (story, carré) dans le pack, 2 + réponse ici", tri([f for f in d.glob("*.jpg") if f.name.endswith(GARDE_Q) and not f.name.endswith(("reponse-carre-1080x1080.jpg",))], ORDRE_I), "image") for d in vi if d.name[3:].startswith(("quiz", "academie"))]})
CAR = sorted(d for d in I.iterdir() if d.is_dir() and d.name.startswith("carrousel-"))
S.append({"id": "carrousels", "titre": "Carrousels pédagogiques", "items": [
    item("carrousel-" + d.name.split("-", 2)[2], f"Carrousel {d.name.split('-')[1]} · {d.name.split('-', 2)[2].replace('-', ' ').capitalize()}", f"{len(list(d.glob('*.jpg')))} diapositives · portrait 4:5 · Instagram, LinkedIn, Facebook",
         sorted(d.glob("*.jpg"), key=lambda f: int(f.name.split("-portrait")[0].rsplit("-", 1)[1])), "image") for d in CAR]})
EM = PACK / "emails/apercus"
S.append({"id": "emails", "titre": "E-mails de suivi des abonnés", "items": [
    item("email-" + f.stem, f"{f.stem[:2]} · " + next((l.split("|")[3].strip() for l in (ICI / "pack/EMAILS.md").read_text().splitlines() if l.startswith(f"| `{f.stem}.html`")), f.stem),
         next((l.split("|")[2].strip() for l in (ICI / "pack/EMAILS.md").read_text().splitlines() if l.startswith(f"| `{f.stem}.html`")), ""), [f], "image") for f in sorted(EM.glob("*.jpg"))]})
if (EM / "sombre").exists():
    S[-1]["items"].append(item("email-ordinateur", "Sur ordinateur · exemples", "Gmail, Outlook.com, Apple Mail : colonne de 600 px centrée", sorted((EM / "ordinateur").glob("*.jpg")), "image"))
    S[-1]["items"].append(item("email-mode-sombre", "Mode sombre · exemples", "Apple Mail, iPhone, Outlook.com en thème sombre", sorted((EM / "sombre").glob("*.jpg")), "image"))
idt = I / "00-identite"
S.append({"id": "identite", "titre": "Identité des comptes", "items": [
    item("id-avatars", "Photos de profil", "nuit et soleil", sorted(idt.glob("avatar-*.jpg")), "image"),
    item("id-bannieres", "Bannières", "X, LinkedIn, Facebook, YouTube · nuit et soleil", sorted(idt.glob("banniere-*.jpg")), "image"),
    item("id-a-la-une", "Couvertures de stories à la une", "Instagram", sorted(idt.glob("a-la-une-*.jpg")), "image"),
    item("images-generales", "Images générales", "affiche de la vidéo, post, bannière, partage de lien", sorted((I / "00-general").glob("*.jpg")), "image")]})
(OUT / "media/manifest.json").write_text(json.dumps({"sections": S}, ensure_ascii=False))
print(sum(len(s["items"]) for s in S), "fiches,", sum(len(i["medias"]) for s in S for i in s["items"]), "aperçus")
