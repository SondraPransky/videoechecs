#!/usr/bin/env python3
"""Pack d'aperçus des e-mails CCAS à partager avec les Activités Sociales de l'Énergie (images seulement, pas de HTML).
Lit build/pack/emails-ccas/apercus/ (scripts/emails-apercus.mjs ccas) et le catalogue de pack/EMAILS-CCAS.md.
Écrit build/apercus-emails-ccas.zip : planche d'ensemble, PDF (un e-mail par page), images téléphone / ordinateur / mode sombre, LISEZ-MOI.
Usage : python3 scripts/pack-apercus-ccas.py"""
import pathlib, re, shutil, zipfile
from PIL import Image, ImageDraw, ImageFont
ICI = pathlib.Path(__file__).resolve().parent.parent
SRC = ICI / "build/pack/emails-ccas/apercus"
OUT = ICI / "build/apercus-emails-ccas"; shutil.rmtree(OUT, ignore_errors=True); (OUT / "telephone").mkdir(parents=True)
POLICE = ICI.parent / "assets/fonts/signika/signika-latin-variable.woff2"
def police(t):
    try: return ImageFont.truetype(str(POLICE), t)
    except Exception: return ImageFont.load_default()
# catalogue : rubrique, fichier, quand, objet (ordre du parcours)
cat, rub = [], None
for l in (ICI / "pack/EMAILS-CCAS.md").read_text().splitlines():
    if l.startswith("### "): rub = l[4:].strip(); continue
    m = re.match(r"\| `([0-9]{2}-[^`]+)\.html` \| (.*?) \| (.*?) \| (.*?) \| (.*?) \|$", l)
    if m and rub: cat.append((rub, m.group(1), m.group(2), m.group(3)))
# images téléphone, renommées dans l'ordre du parcours
import html as _h
def objet_exemple(f, objet):   # l'objet rempli avec les exemples (titre de l'aperçu), sans émoji (absent de la police)
    a = ICI / f"build/_emails-ccas_apercu/{f}.html"
    if a.exists(): objet = _h.unescape(re.search(r"<title>(.*?)</title>", a.read_text(), re.S).group(1))
    return re.sub(r"[\U0001F000-\U0001FFFF\u2600-\u27BF\uFE0F]", "", objet).strip()
imgs = []
for i, (rub, f, quand, objet) in enumerate(cat, 1):
    objet = objet_exemple(f, objet)
    src = SRC / f"{f}.jpg"
    if not src.exists(): continue
    dst = OUT / "telephone" / f"{i:02d}-{f[3:]}.jpg"; shutil.copy(src, dst); imgs.append((dst, rub, objet, quand))
for d in ("ordinateur", "sombre"):
    if (SRC / d).exists(): shutil.copytree(SRC / d, OUT / d)
# planche d'ensemble : le haut de chaque e-mail, 6 par ligne
W, H, col = 420, 760, 6
rows = (len(imgs) + col - 1) // col
pl = Image.new("RGB", (col * (W + 24) + 24, rows * (H + 70) + 110), "#f1f0ea"); dr = ImageDraw.Draw(pl)
dr.text((24, 28), "E-mails de la plateforme d'échecs des Activités Sociales de l'Énergie", font=police(40), fill="#1d1d1b")
for k, (p, rub, objet, quand) in enumerate(imgs):
    im = Image.open(p).convert("RGB"); im = im.resize((W, int(im.height * W / im.width))).crop((0, 0, W, H))
    x, y = 24 + (k % col) * (W + 24), 100 + (k // col) * (H + 70)
    pl.paste(im, (x, y)); dr.text((x, y + H + 10), f"{k + 1:02d} · {rub}", font=police(22), fill="#6b6b66")
pl.save(OUT / "00-planche.jpg", quality=82, optimize=True)
# PDF : une couverture, puis un e-mail par page
pages = []
cov = Image.new("RGB", (1240, 1754), "white"); dc = ImageDraw.Draw(cov)
logo = ICI.parent / "assets/brand/ccas/logo-email-560.png"
if logo.exists(): lg = Image.open(logo).convert("RGBA"); cov.paste(lg, (120, 160), lg)
dc.text((120, 320), "Les e-mails de la plateforme d'échecs", font=police(64), fill="#1d1d1b")
dc.text((120, 400), f"{len(imgs)} e-mails, du premier jour au bilan de l'année", font=police(40), fill="#0066cc")
y = 520
for k, (p, rub, objet, quand) in enumerate(imgs):
    dc.text((120, y), f"{k + 1:02d}  {objet}", font=police(26), fill="#1d1d1b"); y += 40
dc.text((120, 1660), "Europe Échecs · aperçus remplis avec des exemples (pseudo « LéaDame », dates fictives)", font=police(24), fill="#6b6b66")
pages.append(cov)
for k, (p, rub, objet, quand) in enumerate(imgs):
    im = Image.open(p).convert("RGB"); pg = Image.new("RGB", (1240, max(1754, im.height + 260)), "white"); d = ImageDraw.Draw(pg)
    d.text((80, 50), f"{k + 1:02d} · {rub}", font=police(30), fill="#0066cc"); d.text((80, 95), objet, font=police(38), fill="#1d1d1b")
    d.text((80, 150), f"Envoi : {quand}", font=police(24), fill="#6b6b66")
    pg.paste(im, ((1240 - im.width) // 2, 220)); pages.append(pg)
pages[0].save(OUT / "emails-ccas.pdf", save_all=True, append_images=pages[1:], resolution=150, quality=80)
# LISEZ-MOI
lignes = ["E-mails de la plateforme d'échecs des Activités Sociales de l'Énergie — aperçus", "",
          "00-planche.jpg      vue d'ensemble des e-mails", "emails-ccas.pdf     un e-mail par page, avec le moment de l'envoi",
          "telephone/          chaque e-mail sur téléphone, dans l'ordre du parcours", "ordinateur/         3 exemples sur ordinateur",
          "sombre/             3 exemples en mode sombre", "",
          "Les aperçus sont remplis avec des exemples (pseudo « LéaDame », dates et chiffres fictifs).", "", "Liste des e-mails :"]
lignes += [f"{k + 1:02d}  {objet}  —  {quand}" for k, (p, rub, objet, quand) in enumerate(imgs)]
(OUT / "LISEZ-MOI.txt").write_text("\n".join(lignes) + "\n")
z = ICI / "build/apercus-emails-ccas.zip"; z.unlink(missing_ok=True)
with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
    for f in sorted(OUT.rglob("*")):
        if f.is_file(): zf.write(f, "apercus-emails-ccas/" + str(f.relative_to(OUT)))
print(len(imgs), "e-mails ·", z, round(z.stat().st_size / 1e6, 1), "Mo")
