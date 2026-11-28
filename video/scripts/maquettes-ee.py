# Maquettes de trois pistes graphiques pour les e-mails Europe Échecs (rien n'est changé dans les e-mails livrés)
# Usage : python3 scripts/maquettes-ee.py <dossier de sortie>  (crée <dossier>/maquettes/ : actuel, compact, revue, diagramme)
import sys, re, shutil, pathlib
from PIL import Image, ImageDraw, ImageFont
V = pathlib.Path("/home/user/videoechecs/video"); S = pathlib.Path(sys.argv[1]); OUTM = S / "maquettes"
src = V / "scripts/emails.py"; g = {"__file__": str(src), "__name__": "maquette"}
sys.argv = ["emails.py", "ee"]; exec(compile(src.read_text(), str(src), "exec"), g)
if OUTM.exists(): shutil.rmtree(OUTM)
shutil.copytree(V / "build/_emails-ee_apercu/img", OUTM / "img")
E = {e["id"]: e for e in g["E"]}

# ---------- diagrammes générés (positions vérifiées) ----------
PIECES = V / "assets/pieces"
def diagramme(fen, nom, depuis=None, vers=None, cote=640):
    cl, fo, hl = (234, 240, 250), (143, 179, 224), (250, 227, 97)
    m = 36; case = (cote - m) // 8; W = case * 8 + m
    im = Image.new("RGB", (W, W + 0), (255, 255, 255)); d = ImageDraw.Draw(im)
    try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 22)
    except Exception: f = ImageFont.load_default()
    rangs = fen.split()[0].split("/")
    surl = {depuis, vers}
    for r in range(8):
        for c in range(8):
            sq = "abcdefgh"[c] + str(8 - r); x, y = m + c * case, r * case
            col = fo if (r + c) % 2 else cl
            if sq in surl: col = tuple(int(a * .45 + b * .55) for a, b in zip(col, hl))
            d.rectangle([x, y, x + case - 1, y + case - 1], fill=col)
    for r, ligne in enumerate(rangs):
        c = 0
        for ch in ligne:
            if ch.isdigit(): c += int(ch); continue
            p = Image.open(PIECES / f"{'w' if ch.isupper() else 'b'}{ch.upper()}.png").convert("RGBA").resize((case, case), Image.LANCZOS)
            im.paste(p, (m + c * case, r * case), p); c += 1
    for i in range(8):
        d.text((10, i * case + case // 2 - 12), str(8 - i), fill=(90, 100, 128), font=f)
    im2 = Image.new("RGB", (W, W + m), (255, 255, 255)); im2.paste(im, (0, 0)); d2 = ImageDraw.Draw(im2)
    for i in range(8): d2.text((m + i * case + case // 2 - 7, W + 4), "abcdefgh"[i], fill=(90, 100, 128), font=f)
    im2.save(OUTM / "img" / nom, quality=90)
# 79 : après 1.e4 e5 2.Cf3 Cc6 3.Fb5 a6 (partie espagnole), les Noirs viennent de jouer a7-a6
diagramme("r1bqkbnr/1ppp1ppp/p1n5/1B2p3/4P3/5N2/PPPP1PPP/RNBQK2R w KQkq - 0 4", "diag-79.jpg", "a7", "a6")
# 81 : le mat du berger, 1.e4 e5 2.Fc4 Cc6 3.Dh5 Cf6 4.Dxf7#
diagramme("r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4", "diag-81.jpg", "h5", "f7")

# ---------- rendu d'une variante ----------
BASE = {k: g[k] for k in ("ENTETE", "TITRE_SUR_NUIT", "DAMIER", "PIED_NUIT", "SERIF", "PIECE_RUBRIQUE")}
SERIF_REVUE = "'Merriweather', Georgia, 'Times New Roman', serif"
FONT_REVUE = '<link href="https://fonts.googleapis.com/css2?family=Merriweather:wght@400;700;900&display=swap" rel="stylesheet">'
def rendre(e, piste, apres=None):
    g.update(BASE)
    nuit = "#02263D"
    if piste == "compact":
        g["TITRE_SUR_NUIT"] = g["DAMIER"] = g["PIED_NUIT"] = False
        g["ENTETE"] = f'<tr><td class="m-pad" style="background:{nuit};padding:14px 32px"><img src="{{IMG}}/logo-blanc.png" width="104" alt="Europe Échecs" style="display:block;border:0;width:104px;height:auto"></td></tr><tr><td height="4" style="height:4px;background:#FFD30E;font-size:0;line-height:0">&nbsp;</td></tr>'
    elif piste == "revue":
        g["TITRE_SUR_NUIT"] = g["DAMIER"] = False; g["SERIF"] = SERIF_REVUE
        g["ENTETE"] = (f'<tr><td align="center" style="background:{nuit};padding:16px 32px"><img src="{{IMG}}/logo-blanc.png" width="120" alt="Europe Échecs" style="display:block;margin:0 auto;border:0;width:120px;height:auto"></td></tr>'
                       f'<tr><td align="center" style="padding:14px 32px 0;font:700 11px/1 Arial,sans-serif;letter-spacing:.32em;color:#5D6480;text-transform:uppercase">La revue des échecs depuis 1959</td></tr>'
                       f'<tr><td style="padding:12px 32px 0"><div style="border-top:3px solid {nuit};border-bottom:1px solid {nuit};height:3px;font-size:0;line-height:0">&nbsp;</div></td></tr>')
    h = g["page"](e)
    if piste == "revue":   # titres d'articles et chiffres en serif ; titre principal centré
        h = re.sub(r"(<h1 style=\"margin:0 0 22px;)", r'\1text-align:center;font-size:30px;', h).replace(">&mdash;&nbsp;", ">")
        h = h.replace('margin:0 0 14px">', 'margin:0 0 14px;text-align:center">', 1)
        h = re.sub(r"font:(bold|700|800|900) (1[89]|2\d|3\d)px/([\d.]+) 'Signika'[^;\"]*", lambda m: f"font:700 {m.group(2)}px/{m.group(3)} {SERIF_REVUE}", h)
        h = h.replace("{FONTS}", "{FONTS}" + FONT_REVUE)
    if apres: h = apres(h)
    h = h[:h.index("<body")] + g["typo"](h[h.index("<body"):])
    h = h.replace("<sup>", '<sup style="font-size:.7em;line-height:0;vertical-align:super">')
    hb = h.replace("{IMG}", "img").replace("{FONTS}", g["FONTS_WEB"])
    (OUTM / f"{piste}-{e['id']}.html").write_text(g["teinte"](g["exemple"](hb, e.get("exemples"))))

AVANT = {"79-differe-coup-joue", "81-differe-partie-terminee", "89-tournoi-nouvelle-ronde", "104-fairplay-suite-signalement", "112-support-demande-recue",
         "33-newsletter", "42-revue-nouveau-numero", "43-probleme-de-la-semaine", "28-videos-de-la-semaine"}
for i in AVANT: rendre(E[i], "actuel")
for i in ("79-differe-coup-joue", "89-tournoi-nouvelle-ronde", "104-fairplay-suite-signalement", "112-support-demande-recue"): rendre(E[i], "compact")
for i in ("33-newsletter", "42-revue-nouveau-numero", "43-probleme-de-la-semaine", "28-videos-de-la-semaine"): rendre(E[i], "revue")
# Piste 3 : diagramme de la vraie position (79 dans le gabarit actuel et dans le compact, 81 avec le mat)
img79 = lambda h: h.replace("[URL_IMAGE_POSITION]", "img/diag-79.jpg").replace("[LISTE_COUPS]", "1. e4 e5 2. Cf3 Cc6 3. Fb5 a6")
def img81(h):
    bloc = ('<img src="img/diag-81.jpg" width="320" alt="La position finale" style="display:block;width:320px;max-width:100%;height:auto;border:0;border-radius:10px;margin:0 auto 6px">'
            '<p style="margin:0 0 18px;text-align:center;font:14px/1.5 \'Signika\',Arial,sans-serif;color:#5D6480">Position finale : 4. Dxf7#</p>')
    return h.replace('<a href="[LIEN_PARTIE]" style', bloc + '<a href="[LIEN_PARTIE]" style', 1) if False else h.replace("<!-- APRES_INFOS -->", bloc)
rendre(E["79-differe-coup-joue"], "diagramme", img79)
rendre(E["79-differe-coup-joue"], "compact-diagramme", img79) if False else None
e81 = dict(E["81-differe-partie-terminee"]); e81["corps"] = list(e81["corps"]); e81["corps"].insert(1, "<!-- APRES_INFOS -->")
e81["exemples"] = {"RAISON_FIN": "échec et mat", "CADENCE": "1 coup en 3 jours"}
rendre(e81, "diagramme", img81)
g.update(BASE)
# compact + diagramme : la combinaison conseillée pour les notifications de jeu
def rendre_combo():
    e = E["79-differe-coup-joue"]; rendre(e, "compact", img79)
    p = OUTM / "compact-79-differe-coup-joue.html"; p.rename(OUTM / "combo-79-differe-coup-joue.html")
rendre_combo(); rendre(E["79-differe-coup-joue"], "compact")
print(sorted(f.name for f in OUTM.glob("*.html")))
