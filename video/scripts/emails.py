#!/usr/bin/env python3
"""E-mails de suivi des abonnés de l'Académie echecs.com : HTML prêt à intégrer dans l'outil d'envoi maison.

Écrit build/pack/emails/ : un fichier HTML par e-mail (images en [URL_IMAGES]/…, variables entre crochets),
le dossier img/ à héberger, et build/_emails_apercu/ (mêmes e-mails avec les images locales, pour les captures).
Le catalogue (déclencheur, objet, pré-en-tête, variables) est dans pack/EMAILS.md.
Usage : python3 scripts/emails.py"""
import html, pathlib, re, shutil

ICI = pathlib.Path(__file__).resolve().parent.parent
PACK = ICI / "build/pack"
OUT = PACK / "emails"; APER = ICI / "build/_emails_apercu"
for d in (OUT, APER):
    shutil.rmtree(d, ignore_errors=True); (d / "img").mkdir(parents=True)

# Images utilisées (copiées dans img/, à héberger à l'adresse [URL_IMAGES])
IMG = {
    "logo": ICI.parent / "assets/brand/logo-echecs-com-blanc.png",
    "progression": PACK / "images/01-progression/01-progression-lien-1200x630.jpg",
    "etapes": PACK / "images/02-valide-chaque-etape/02-valide-chaque-etape-lien-1200x630.jpg",
    "lecons": PACK / "images/03-lecons/03-lecons-lien-1200x630.jpg",
    "exercices": PACK / "images/04-exercices/04-exercices-lien-1200x630.jpg",
    "videos": PACK / "images/05-videos/05-videos-lien-1200x630.jpg",
    "masterclasses": PACK / "images/06-masterclasses/06-masterclasses-lien-1200x630.jpg",
    "parties": PACK / "images/07-tes-parties/07-tes-parties-lien-1200x630.jpg",
    "revue": PACK / "images/08-revue/08-revue-lien-1200x630.jpg",
    "forum": PACK / "images/09-forum/09-forum-lien-1200x630.jpg",
    "tournois": PACK / "images/10-tournois/10-tournois-lien-1200x630.jpg",
    "dodo": PACK / "images/24-humeur-dodo/24-humeur-dodo-lien-1200x630.jpg",
    "bienvenue": PACK / "images/30-bienvenue/30-bienvenue-lien-1200x630.jpg",
    "objectif": PACK / "images/33-objectif-atteint/33-objectif-atteint-lien-1200x630.jpg",
    "oups": PACK / "images/37-oups/37-oups-lien-1200x630.jpg",
    "puzzle": PACK / "images/14-probleme-mat-en-1/14-probleme-mat-en-1-lien-1200x630.jpg",
}
BANDEAUX = sorted(f.name[6:-13] for f in (PACK / "images/00-emails").glob("email-*-1200x480.jpg"))
for b in BANDEAUX: IMG["b-" + b] = PACK / f"images/00-emails/email-{b}-1200x480.jpg"
from PIL import Image
for k, f in IMG.items():
    for d in (OUT, APER):
        if f.suffix == ".png": shutil.copy(f, d / "img" / (k + ".png")); continue
        if k.startswith("b-"): Image.open(f).convert("RGB").save(d / "img" / (k + ".jpg"), quality=86, optimize=True); continue   # en-tête dédié : tel quel
        im = Image.open(f).convert("RGB"); w, h = im.size   # sans le logo ni le bouton du visuel réseau (doublons dans un e-mail)
        im.crop((0, int(h * .14), w, int(h * .85))).save(d / "img" / (k + ".jpg"), quality=86, optimize=True)

for src, nom in ((ICI / "assets/captures/ee/hd/auth-kamsky.jpg", "coach-exemple.jpg"), (PACK / "images/00-emails/email-puzzle-1080x1080.jpg", "puzzle-exemple.jpg")):
    im = Image.open(src).convert("RGB"); im.thumbnail((600, 600)); im.save(APER / "img" / nom, quality=86)
C = {"em": "#2c4a6e", "fond": "#f1f0ea", "nuit": "#0f1420", "texte": "#1d1d1b", "gris": "#6b6b66", "jaune": "#fae361", "bleu": "#93b9e2", "vert": "#2f9e44", "carte": "#ffffff", "filet": "#e4e1d8"}
SERIF = "'Fraunces', Georgia, 'Times New Roman', serif"; SANS = "'Manrope', 'Helvetica Neue', Arial, sans-serif"
# Polices de l'Académie : Google Fonts dans les e-mails envoyés (Apple Mail, iOS, Outlook.com les affichent ; Gmail garde Georgia / Arial),
# fichiers locaux pour les aperçus.
FONTS_WEB = '<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,900;1,9..144,400&family=Manrope:wght@500;700;800&display=swap" rel="stylesheet"><!--<![endif]-->'
# Outlook sur PC (moteur Word) : il ne charge pas les polices web et prendrait Times New Roman ; on impose Arial et Georgia
FONTS_WEB += '<!--[if mso]><style>body,table,td,p,a,div,span,li{font-family:Arial,Helvetica,sans-serif !important} h1,h1 span{font-family:Georgia,serif !important}</style><![endif]-->'
NM = ICI / "node_modules/@fontsource"
FONTS_LOCAL = "<style>" + "".join(f'@font-face{{font-family:"{f}";font-weight:{w};font-style:{st};src:url("file://{NM}/{f.lower()}/files/{f.lower()}-latin-{w}-{st}.woff2") format("woff2")}}'
    for f, w, st in (("Fraunces", 900, "normal"), ("Fraunces", 400, "italic"), ("Manrope", 500, "normal"), ("Manrope", 700, "normal"), ("Manrope", 800, "normal"))) + "</style>"

def bouton(txt, lien):
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:28px 0 8px"><tr><td bgcolor="{C['jaune']}" style="border-radius:999px;background:{C['jaune']};mso-padding-alt:16px 28px">
<a href="{lien}" style="display:inline-block;padding:16px 28px;font-family:{SANS};font-weight:800;font-size:17px;color:#111111;text-decoration:none;border-radius:999px">{txt}&nbsp;&rarr;</a></td></tr></table>'''

def para(t): return f'<p style="margin:0 0 16px;font:16px/1.6 {SANS};color:{C["texte"]}">{t}</p>'
def encadre(t): return f'<div style="margin:24px 0;padding:18px 20px;background:{C["fond"]};border-left:5px solid {C["jaune"]};border-radius:8px;font:16px/1.55 {SANS};color:{C["texte"]}">{t}</div>'
def liste(items): return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 18px">' + "".join(
    f'<tr><td valign="top" style="padding:6px 12px 6px 0;font:bold 16px {SANS};color:{C["vert"]}">&#10003;</td><td style="padding:6px 0;font:16px/1.5 {SANS};color:{C["texte"]}">{i}</td></tr>' for i in items) + "</table>"
def infos(rows): return '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;background:' + C["fond"] + ';border-radius:12px">' + "".join(
    f'<tr><td style="padding:13px 18px;font-family:{SANS};font-weight:500;font-size:14px;color:{C["gris"]};{"" if i == len(rows) - 1 else "border-bottom:1px solid " + C["filet"] + ";"}width:42%">{k}</td>'
    f'<td style="padding:13px 18px;font-family:{SANS};font-weight:800;font-size:16px;color:{C["texte"]};{"" if i == len(rows) - 1 else "border-bottom:1px solid " + C["filet"] + ";"}">{v}</td></tr>' for i, (k, v) in enumerate(rows)) + "</table>"
def comparatif(rows):   # Gratuit / Abonné : la colonne abonné en jaune
    ok = f'<span style="color:{C["vert"]};font-weight:800">&#10003;</span>'; non = f'<span style="color:#b9b5aa">&mdash;</span>'
    cell = lambda v: ok if v is True else non if v is False else v
    th = lambda t, bg, col: f'<td align="center" style="padding:12px 8px;background:{bg};font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:{col};border-radius:10px 10px 0 0">{t}</td>'
    h = f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr><td></td>{th("Gratuit", C["fond"], C["gris"])}{th("Abonné", C["jaune"], "#111")}</tr>'
    for i, (k, g, a) in enumerate(rows):
        last = i == len(rows) - 1; bb = "" if last else f"border-bottom:1px solid {C['filet']};"
        h += (f'<tr><td style="padding:13px 10px 13px 0;font-family:{SANS};font-weight:700;font-size:14px;color:{C["texte"]};{bb}">{k}</td>'
              f'<td align="center" style="padding:13px 8px;background:{C["fond"]};font-family:{SANS};font-size:14px;color:{C["gris"]};{bb}{"border-radius:0 0 10px 10px;" if last else ""}">{cell(g)}</td>'
              f'<td align="center" style="padding:13px 8px;background:#fff6c2;font-family:{SANS};font-weight:800;font-size:14px;color:#111;{bb}{"border-radius:0 0 10px 10px;" if last else ""}">{cell(a)}</td></tr>')
    return h + "</table>"
def tuiles(items):   # chiffres clés : grandes valeurs en Fraunces, sur des tuiles crème
    w = 100 // len(items)
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate;border-spacing:8px 0"><tr>' + "".join(
        f'<td width="{w}%" valign="top" style="background:{C["fond"]};border-radius:14px;padding:18px 12px 16px;text-align:center">'
        f'<div style="font-family:{SERIF};font-weight:900;font-size:{30 if len(re.sub(r"<[^>]+>|&[a-z]+;", "x", v)) <= 6 else 20}px;line-height:1.1;color:{C["texte"]}">{v}</div>'
        f'<div style="margin-top:8px;font-family:{SANS};font-weight:700;font-size:12px;line-height:1.35;color:{C["gris"]}">{k}</div></td>' for v, k in items) + "</tr></table>")
def billet(titre, lignes, jour="[JOUR]", mois="[MOIS_COURT]"):   # événement : bloc calendrier nuit + détails
    det = "".join(f'<div style="margin-top:7px;font-family:{SANS};font-size:14px;color:{C["gris"]}"><b style="color:{C["texte"]};font-weight:800">{k}</b>&nbsp;&nbsp;{v}</div>' for k, v in lignes)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr>'
            f'<td width="88" valign="middle" align="center" style="background:{C["nuit"]};border-radius:14px 0 0 14px;padding:16px 6px">'
            f'<div style="font-family:{SERIF};font-weight:900;font-size:36px;line-height:1;color:{C["jaune"]}">{jour}</div>'
            f'<div style="margin-top:6px;font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:#f4f1ea">{mois}</div></td>'
            f'<td valign="middle" style="background:{C["fond"]};border-radius:0 14px 14px 0;padding:16px 18px">'
            f'<div style="font-family:{SERIF};font-weight:900;font-size:20px;line-height:1.25;color:{C["texte"]}">{titre}</div>{det}</td></tr></table>')
def recu(lignes, total_k, total_v):   # reçu : lignes fines, pointillés, total en gras
    rows = "".join(f'<tr><td style="padding:9px 0;font-family:{SANS};font-size:14px;color:{C["gris"]}">{k}</td><td align="right" style="padding:9px 0;font-family:{SANS};font-weight:700;font-size:14px;color:{C["texte"]}">{v}</td></tr>' for k, v in lignes)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border:1px solid {C["filet"]};border-radius:14px"><tr><td style="padding:16px 20px">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{rows}'
            f'<tr><td colspan="2" style="border-top:2px dashed {C["filet"]};font-size:0;line-height:0;padding-top:8px">&nbsp;</td></tr>'
            f'<tr><td style="font-family:{SANS};font-weight:800;font-size:16px;color:{C["texte"]}">{total_k}</td><td align="right" style="font-family:{SERIF};font-weight:900;font-size:30px;color:{C["texte"]}">{total_v}</td></tr></table></td></tr></table>')
def coach():   # le coach de la masterclass : photo ronde, nom et titre
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:0 0 20px"><tr><td width="72" valign="middle"><img src="[URL_PHOTO_COACH]" width="64" height="64" alt="[COACH]" style="display:block;width:64px;height:64px;border-radius:50%;border:3px solid {C["jaune"]};object-fit:cover"></td>'
            f'<td valign="middle" style="padding-left:12px"><div style="font-family:{SERIF};font-weight:900;font-size:20px;color:{C["texte"]}">[COACH]</div><div style="font-family:{SANS};font-size:14px;color:{C["gris"]}">[TITRE_COACH] · ton coach pour cette masterclass</div></td></tr></table>')
def podium(p1, p2, p3):
    col = lambda nom, rang, h, bg: (f'<td width="33%" valign="bottom" align="center" style="padding:0 4px"><div style="font-family:{SANS};font-weight:800;font-size:14px;line-height:1.3;color:{C["texte"]};margin-bottom:8px">{nom}</div>'
        f'<div style="background:{bg};border-radius:12px 12px 0 0;height:{h}px;line-height:{h}px;font-family:{SERIF};font-weight:900;font-size:30px;color:#111">{rang}</div></td>')
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0 8px"><tr>'
            + col(p2, "2", 70, "#dfe6ef") + col(p1, "1", 100, C["jaune"]) + col(p3, "3", 52, "#f0c9a0") + '</tr></table>')
def carte_prix(titre, prix, unite, barre, note, mis_en_avant=False, badge=""):
    b = f'<div style="display:inline-block;margin-bottom:10px;padding:4px 10px;border-radius:999px;background:#111;font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:{C["jaune"]}">{badge}</div><br>' if badge else ""
    return (f'<td valign="top" style="background:{"#fff6c2" if mis_en_avant else C["fond"]};border:2px solid {C["jaune"] if mis_en_avant else C["fond"]};border-radius:16px;padding:16px 12px" width="50%">{b}'
            f'<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{C["gris"]}">{titre}</div>'
            f'<div style="margin-top:8px;font-family:{SERIF};font-weight:900;font-size:32px;line-height:1;color:{C["texte"]};white-space:nowrap">{prix}</div>'
            f'<div style="margin-top:4px;font-family:{SANS};font-weight:700;font-size:14px;color:{C["gris"]}">{unite}</div>'
            f'<div style="margin-top:6px;font-family:{SANS};font-size:14px;color:{C["gris"]}"><s>{barre}</s></div>'
            f'<div style="margin-top:10px;font-family:{SANS};font-weight:700;font-size:14px;line-height:1.4;color:{C["texte"]}">{note}</div></td>')
def offre(intro=""):   # les deux formules au prix de lancement, l'annuelle mise en avant
    return ((para(intro) if intro else "") + '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate;border-spacing:6px 0;table-layout:fixed"><tr>'
            + carte_prix("Mensuel", "14,90&nbsp;€", "/mois", "19,90 €/mois", "Sans engagement")
            + carte_prix("Annuel", "150&nbsp;€", "/an", "179,90 €/an", "Soit 12,50 € par mois", True, "Le plus avantageux") + "</tr></table>"
            + f'<p style="margin:0 0 6px;font-family:{SANS};font-size:14px;color:{C["gris"]}">Prix de lancement, garanti tant que tu restes abonné.</p>')
def carte(img, titre, texte, lien, cta, src=None):
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 22px;border:1px solid {C['filet']};border-radius:12px;overflow:hidden">
<tr><td{' style="background:#f1f0ea;padding:18px 18px 0"' if src else ""}><img src="{src or "{IMG}/" + img + ".jpg"}" width="{500 if src else 536}" alt="" style="display:block;width:100%;height:auto;border:0;{"border-radius:10px;" if src else ""}"></td></tr>
<tr><td style="padding:18px 20px 20px"><div style="font:bold 20px/1.3 {SERIF};color:{C['texte']};margin:0 0 8px">{titre}</div>
<div style="font:16px/1.55 {SANS};color:{C['texte']};margin:0 0 12px">{texte}</div><a href="{lien}" style="font:bold 16px {SANS};color:#1f5fa8;text-decoration:none">{cta}&nbsp;&rarr;</a></td></tr></table>'''

DARK = """<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><style>
@media (prefers-color-scheme: dark) {
  body, [style*="background:#f1f0ea"] { background:#06080c !important; }
  [style*="background:#ffffff"] { background:#121a25 !important; }
  td[style*="background:#f1f0ea"], div[style*="background:#f1f0ea"] { background:#1b2533 !important; }
  [style*="color:#1d1d1b"] { color:#f4f1ea !important; } [style*="color:#6b6b66"] { color:#a9b4c2 !important; }
  [style*="color:#2c4a6e"] { color:#93b9e2 !important; } a[style*="color:#1f5fa8"] { color:#93b9e2 !important; }
  [style*="#e4e1d8"] { border-color:#2a3546 !important; }
  [style*="background:#fff6c2"] [style*="color:#1d1d1b"], [style*="background:#fae361"] [style*="color:#1d1d1b"] { color:#111111 !important; }
  [style*="background:#fff6c2"] [style*="color:#6b6b66"] { color:#4a4636 !important; }
}
</style>"""
def typo(h):   # espace insécable avant : ; ? ! » % et après «, entre un nombre et son unité ; seulement dans le texte, jamais dans les balises
    def t(x):
        x = re.sub(r" ([:;?!»%])", "\u00a0\\1", x); x = x.replace("« ", "«\u00a0")
        x = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", "’", x)   # apostrophe typographique
        x = re.sub(r"\b1(er|re)\b", r"1<sup>\1</sup>", x)
        x = re.sub(r"(\d) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)", "\\1\u00a0\\2", x)   # 18 novembre
        x = re.sub(r"\b(Objectif|n°|N°|Calcul Gagnant) (\d)", "\\1\u00a0\\2", x)   # Objectif 1400, n° 780
        x = re.sub(r"(\d) (h|min|€|s|jours?|leçons|exercices|points|ans?)\b", "\\1\u00a0\\2", x)
        x = re.sub(r"(\d\u00a0h) (\d)", "\\1\u00a0\\2", x)   # 20 h 30
        return re.sub(r"(\d) (\d{3})\b", "\\1\u00a0\\2", x)
    return "".join(p if p.startswith("<") else t(p) for p in re.split(r"(<[^>]+>)", h))
def page(e):
    pied = ("Tu reçois cet e-mail car tu as un compte sur echecs.com. "
            + ('<a href="[LIEN_PREFERENCES]" style="color:#6b6b66">Gérer mes e-mails</a> · <a href="[LIEN_DESINSCRIPTION]" style="color:#6b6b66">Se désinscrire</a>' if e.get("marketing", True)
               else "Cet e-mail concerne ton compte : il est envoyé même si tu as refusé les e-mails d'information."))
    hero = f'<tr><td><img src="{{IMG}}/{e["img"]}.jpg" width="600" alt="{html.escape(e.get("alt", ""))}" style="display:block;width:100%;height:auto;border:0"></td></tr>' if e.get("img") else ""
    if not e.get("img") and e.get("mascotte"):   # pas d'image : la mascotte, sur le fond nuit de l'en-tête
        hero = f'<tr><td align="center" style="background:{C["nuit"]};padding:4px 0 0"><img src="{{IMG}}/mascotte-{e["mascotte"]}.png" height="150" alt="" style="display:block;height:150px;width:auto;border:0;margin:6px auto 0"></td></tr>'
    t1, _, t2 = e["titre"].partition("|")
    titre = t1.strip() + (f'<br><span style="font-family:{SERIF};font-style:italic;font-weight:400;color:{C["em"]}">{t2.strip()}</span>' if t2 else "")
    corps = "".join(e["corps"])
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>{html.escape(e["objet"])}</title>{{FONTS}}{DARK}</head>
<body style="margin:0;padding:0;background:{C['fond']}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{html.escape(e["pre"])}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:{C['fond']}"><tr><td align="center" style="padding:24px 12px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="width:100%;max-width:600px;background:{C['carte']};border-radius:16px;overflow:hidden">
<tr><td style="background:{C['nuit']};padding:22px 32px"><img src="{{IMG}}/logo.png" width="170" alt="echecs.com" style="display:block;border:0;width:170px;height:auto"></td></tr>
{hero}
<tr><td style="padding:34px 32px 30px">
<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{C['em']};margin:0 0 14px">&mdash;&nbsp;{e['sur']}</div>
<h1 style="margin:0 0 22px;font-family:{SERIF};font-weight:900;font-size:32px;line-height:1.15;color:{C['texte']}">{titre}</h1>
{corps}
<p style="margin:26px 0 0;font:16px/1.6 {SANS};color:{C['texte']}">{e.get('sign', "À très vite sur l'échiquier,<br><b>L'équipe de l'Académie echecs.com</b>")}</p>
</td></tr>
<tr><td style="padding:22px 32px 6px;border-top:1px solid {C['filet']};font-family:{SANS};font-weight:700;font-size:14px;color:{C['texte']}">
<a href="[LIEN_ACADEMIE]" style="color:{C['texte']};text-decoration:none">L'Académie</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="[LIEN_MASTERCLASSES]" style="color:{C['texte']};text-decoration:none">Masterclasses</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="[LIEN_TOURNOIS]" style="color:{C['texte']};text-decoration:none">Tournois</a>&nbsp;&nbsp;·&nbsp;&nbsp;<a href="[LIEN_FORUM]" style="color:{C['texte']};text-decoration:none">Forum</a></td></tr>
<tr><td style="padding:4px 32px 0;font-family:{SANS};font-size:12px;color:{C['gris']}">Suis-nous : <a href="[LIEN_INSTAGRAM]" style="color:{C['gris']}">Instagram</a> · <a href="[LIEN_FACEBOOK]" style="color:{C['gris']}">Facebook</a> · <a href="[LIEN_YOUTUBE]" style="color:{C['gris']}">YouTube</a> · <a href="[LIEN_X]" style="color:{C['gris']}">X</a> · <a href="[LIEN_LINKEDIN]" style="color:{C['gris']}">LinkedIn</a></td></tr>
<tr><td style="padding:12px 32px 26px;font:12px/1.6 {SANS};color:{C['gris']}">{pied}<br>echecs.com · Europe Échecs · [ADRESSE_POSTALE]</td></tr>
</table></td></tr></table></body></html>'''

L = lambda nom: f"[LIEN_{nom}]"
OFFRE = "<b>14,90&nbsp;€/mois</b> au lieu de 19,90&nbsp;€, ou <b>150&nbsp;€/an</b> au lieu de 179,90&nbsp;€"
E = []
def mail(**k): E.append(k)

# ---------- 1. Compte ----------
mail(id="01-confirmation-adresse", cat="Compte", marketing=False, quand="À la création du compte (transactionnel)",
     objet="Confirme ton adresse e-mail", pre="Un clic, et ton compte echecs.com est prêt.", sur="Ton compte", titre="Plus qu'un clic, [PRENOM] !",
     corps=[para("Pour activer ton compte echecs.com, confirme simplement ton adresse e-mail."), bouton("Confirmer mon adresse", L("CONFIRMATION")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 48 heures. Tu n\'as pas créé de compte ? Ignore cet e-mail.</span>')])
mail(id="02-bienvenue-compte-gratuit", cat="Compte", quand="Juste après la confirmation de l'adresse", img="bienvenue", alt="La mascotte echecs.com souhaite la bienvenue",
     objet="Bienvenue sur echecs.com, [PRENOM] ♟️", pre="6 leçons offertes, le forum et le puzzle du jour t'attendent.", sur="Bienvenue", titre="Ton compte est prêt.",
     corps=[para("Bienvenue dans la communauté echecs.com ! Sans attendre et sans payer, tu as déjà accès à :"),
            liste(["<b>6 leçons</b> de l'Académie, pour découvrir la méthode", "<b>Le puzzle du jour</b>, un nouveau problème chaque matin", "<b>Le forum</b>, pour poser tes questions et partager tes parties"]),
            bouton("Ma première leçon", L("PREMIERE_LECON")),
            offre("Envie d'aller plus loin ? L'Académie complète : +200 leçons, +2 000 exercices, les masterclasses et la revue en PGN."), para('<a href="[LIEN_ABONNEMENT]" style="font-weight:800;color:#1f5fa8;text-decoration:none">Voir les formules&nbsp;&rarr;</a>')])
mail(id="03-mot-de-passe", cat="Compte", marketing=False, quand="Sur demande de réinitialisation (transactionnel)",
     objet="Réinitialise ton mot de passe", pre="Ce lien est valable 1 heure.", sur="Ton compte", titre="Nouveau mot de passe",
     corps=[para("[PRENOM], tu as demandé à changer ton mot de passe. Clique ci-dessous pour en choisir un nouveau."), bouton("Choisir mon mot de passe", L("MOT_DE_PASSE")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 1 heure. Si tu n\'es pas à l\'origine de cette demande, ignore cet e-mail : ton mot de passe ne change pas.</span>')])

# ---------- 2. Conversion du compte gratuit ----------
mail(id="04-gratuit-j3-lecons", cat="Compte gratuit → abonnement", quand="J+3 après la création du compte, si pas abonné", img="lecons", alt="Les leçons interactives de l'Académie",
     objet="Tes 6 leçons offertes t'attendent", pre="Vidéo, cours, exercice, quiz : tu as essayé ?", sur="Ta découverte", titre="Tu as essayé une leçon ?",
     corps=[para("[PRENOM], chaque leçon de l'Académie suit le même chemin : une <b>vidéo</b>, un <b>cours</b>, des <b>exercices</b> sur l'échiquier, puis un <b>quiz</b> pour valider. Tu as [NB_LECONS_GRATUITES_RESTANTES] leçons offertes à découvrir."),
            bouton("Reprendre mes leçons", L("LECONS")), para("Et chaque matin, un nouveau <b>puzzle du jour</b> t'attend pour garder la main.")])
mail(id="05-gratuit-j7-offre", cat="Compte gratuit → abonnement", quand="J+7 après la création du compte, si pas abonné", img="progression", alt="Le parcours de progression de l'Académie",
     objet="L'Académie complète à 14,90 €/mois", pre="Prix de lancement, sans engagement en mensuel.", sur="Offre de lancement", titre="Passe à l'Académie complète.",
     corps=[para("Tu as goûté à la méthode, [PRENOM]. Avec l'abonnement, tu débloques tout :"),
            liste(["+200 leçons interactives, de l'initiation à 2000+", "+2 000 exercices à ton niveau", "Les masterclasses en direct et leurs replays", "Tout le catalogue vidéo Europe Échecs et la revue en PGN", "Tes parties analysées, les tournois en ligne"]),
            offre(), bouton("Je m'abonne", L("ABONNEMENT"))])
mail(id="06-gratuit-j21-relance", cat="Compte gratuit → abonnement", quand="J+21 après la création du compte, si pas abonné et actif dans les 14 derniers jours", img="exercices", alt="Les exercices de l'Académie",
     objet="Tu hésites encore, [PRENOM] ?", pre="Ce que les abonnés ont en plus, en 30 secondes.", sur="Ta découverte", titre="Tu hésites encore ?",
     corps=[para("Tu utilises déjà le puzzle du jour et les leçons offertes. Voici ce que l'abonnement ajoute :"),
            comparatif([("Leçons", "6", "+200"), ("Exercices", "puzzle du jour", "+2 000"), ("Masterclasses", False, True), ("Revue en PGN", False, True), ("Tes parties analysées", False, True), ("Forum", True, True)]),
            offre("Toujours au prix de lancement :"), bouton("Choisir ma formule", L("ABONNEMENT"))])

# ---------- 3. Abonnement ----------
mail(id="07-confirmation-abonnement", cat="Abonnement", marketing=False, quand="Au paiement du premier abonnement (transactionnel)", img="objectif", alt="Objectif atteint",
     objet="Bienvenue dans l'Académie, [PRENOM] !", pre="Ton abonnement est actif : voici ton récapitulatif.", sur="Abonnement confirmé", titre="Tu fais partie de l'Académie.",
     corps=[para("Merci pour ta confiance ! Ton abonnement est actif dès maintenant."),
            recu([("Formule", "[FORMULE]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]"), ("Moyen de paiement", "[MOYEN_PAIEMENT]")], "Payé aujourd'hui", "[PRIX]"),
            bouton("Choisir mon parcours", L("PARCOURS")), para('<span style="color:#6b6b66;font-size:14px">Ta facture est disponible dans <a href="[LIEN_FACTURES]" style="color:#1f5fa8">ton espace</a>.</span>')])
mail(id="08-paiement-refuse", cat="Abonnement", marketing=False, quand="Échec d'un prélèvement (transactionnel), relance à J+3 si non réglé",
     objet="Ton paiement n'est pas passé", pre="Mets à jour ta carte pour garder l'accès à l'Académie.", sur="Paiement", titre="Ton paiement n'est pas passé.",
     corps=[para("[PRENOM], le paiement de ton abonnement du [DATE] n'a pas pu être effectué. Ça arrive : carte expirée, plafond atteint…"),
            para("Mets à jour ton moyen de paiement pour garder l'accès à tes leçons, tes exercices et les masterclasses."), bouton("Mettre à jour ma carte", L("PAIEMENT")),
            para('<span style="color:#6b6b66;font-size:14px">Sans régularisation, ton accès sera suspendu le [DATE_SUSPENSION]. Ta progression reste enregistrée.</span>')])
mail(id="09-paiement-recu", cat="Abonnement", marketing=False, quand="À chaque renouvellement réussi (transactionnel)",
     objet="Ton reçu echecs.com · [MOIS]", pre="Merci ! Ton abonnement continue.", sur="Reçu", titre="Merci, [PRENOM] !",
     corps=[para("Ton abonnement à l'Académie est renouvelé."), recu([("Formule", "[FORMULE]"), ("Date", "[DATE]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]")], "Montant", "[PRIX]"),
            bouton("Voir ma facture", L("FACTURES"))])

# ---------- 4. Démarrage de l'abonné ----------
mail(id="10-demarrage-j1-parcours", cat="Démarrage de l'abonné", quand="J+1 après l'abonnement", img="etapes", alt="Valide chaque étape",
     objet="Par où commencer ? Ton parcours en 3 étapes", pre="Initiation, 1400, 1600, 1800 : trouve ton niveau.", sur="Démarrage · 1/4", titre="Trouve ton niveau.",
     corps=[para("[PRENOM], l'Académie est organisée en parcours : <b>Initiation</b>, <b>Objectif 1400</b>, <b>1600</b>, <b>1800</b>, puis <b>2000 et +</b>."),
            liste(['Choisis le parcours qui correspond à ton niveau, ou <a href="[LIEN_TEST_PLACEMENT]" style="color:#1f5fa8">passe le test de placement</a> (5 minutes)', "Fais une leçon : vidéo, cours, exercices, quiz", "Valide le quiz pour débloquer la suivante"]),
            bouton("Choisir mon parcours", L("PARCOURS"))])
mail(id="11-demarrage-j3-exercices", cat="Démarrage de l'abonné", quand="J+3 après l'abonnement", img="exercices", alt="Les exercices de l'Académie",
     objet="10 minutes par jour suffisent", pre="+2 000 exercices, rangés par thème et par niveau.", sur="Démarrage · 2/4", titre="10 minutes par jour.",
     corps=[para("La régularité fait plus que les longues séances. Chaque jour, quelques exercices à ton niveau : mat en 1, fourchette, clouage, finales…"),
            para("Ta <b>série de jours</b> s'affiche sur ton tableau de bord : essaie de ne pas la casser !"), bouton("Faire mes exercices du jour", L("EXERCICES"))])
mail(id="12-demarrage-j6-masterclasses", cat="Démarrage de l'abonné", quand="J+6 après l'abonnement", img="masterclasses", alt="Les masterclasses en direct",
     objet="Les grands maîtres t'attendent", pre="Masterclasses en direct et replays, inclus dans ton abonnement.", sur="Démarrage · 3/4", titre="Apprends des meilleurs.",
     corps=[para("Gata Kamsky, Fabien Libiszewski, Sylvain Ravot, Marc Quenehen… Les masterclasses sont <b>incluses</b> dans ton abonnement, en direct et en replay."),
            para("Tu peux poser tes questions pendant le direct."), bouton("Voir les masterclasses", L("MASTERCLASSES"))])
mail(id="13-demarrage-j10-communaute", cat="Démarrage de l'abonné", quand="J+10 après l'abonnement", img="tournois", alt="Les tournois en ligne",
     objet="Joue, partage, mesure-toi", pre="Tournois en ligne, forum, tes parties analysées.", sur="Démarrage · 4/4", titre="Rejoins la communauté.",
     corps=[liste(["<b>Les tournois en ligne</b>, ouverts à tous les niveaux", "<b>Le forum</b>, pour poser tes questions aux coachs et aux autres membres", "<b>Tes parties</b> : saisis-les, analyse-les, partage-les en PGN"]),
            bouton("Voir le prochain tournoi", L("TOURNOIS"))])

# ---------- 5. Engagement ----------
mail(id="14-bilan-mensuel", cat="Engagement", quand="Le 1er de chaque mois, si au moins une activité dans le mois", img="progression", alt="La mascotte fête une victoire",
     objet="[PRENOM], ton mois d'échecs en chiffres", pre="[NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo !", sur="Ton bilan de [MOIS]", titre="Ton mois en chiffres.",
     corps=[tuiles([("[NB_LECONS]", "leçons terminées"), ("[NB_EXERCICES]", "exercices réussis ([TAUX_REUSSITE] %)"), ("[SERIE_MAX]&nbsp;j", "meilleure série")]),
            para("Ton thème le plus travaillé : <b>[THEME_FORT]</b>. À renforcer : <b>[THEME_FAIBLE]</b>."), bouton("Travailler [THEME_FAIBLE]", L("THEME_FAIBLE"))])
mail(id="15-objectif-atteint", cat="Engagement", quand="Quand l'abonné valide un module ou un parcours", img="objectif", alt="Objectif atteint",
     objet="Module validé : [MODULE] 🎉", pre="Une étape de plus vers ton objectif.", sur="Bravo", titre="Module validé !",
     corps=[para("[PRENOM], tu viens de valider <b>[MODULE]</b>. Tu as passé [NB_LECONS_MODULE] leçons et réussi [NB_EXERCICES_MODULE] exercices."),
            para("Prochaine étape : <b>[MODULE_SUIVANT]</b>."), bouton("Module suivant", L("MODULE_SUIVANT"))])
mail(id="16-serie-en-danger", cat="Engagement", quand="Le soir, si la série de jours (≥ 5 jours) va s'interrompre", img="exercices", alt="La série de jours",
     objet="Ta série de [SERIE] jours va s'arrêter ⏳", pre="Un exercice suffit pour la garder.", sur="Ta série", titre="Garde ta série !",
     corps=[para("[PRENOM], tu as joué [SERIE] jours d'affilée. Il te reste jusqu'à minuit pour la prolonger : <b>un seul exercice suffit</b>."), bouton("Faire un exercice", L("EXERCICE_DU_JOUR"))])
mail(id="17-inactif-7-jours", cat="Réactivation", quand="Abonné sans connexion depuis 7 jours", img="lecons", alt="Les leçons de l'Académie",
     objet="Ta prochaine leçon t'attend", pre="On reprend là où tu en étais ?", sur="On reprend ?", titre="On reprend là où tu en étais ?",
     corps=[para("[PRENOM], ta dernière leçon était <b>[DERNIERE_LECON]</b>. La suivante, <b>[LECON_SUIVANTE]</b>, prend environ [DUREE_LECON]."), bouton("Reprendre ma leçon", L("LECON_SUIVANTE"))])
mail(id="18-inactif-30-jours", cat="Réactivation", quand="Abonné sans connexion depuis 30 jours", img="dodo", alt="La mascotte qui dort",
     objet="Tu nous manques, [PRENOM]", pre="Voici ce qui est nouveau depuis ta dernière visite.", sur="Quoi de neuf", titre="Tu nous manques !",
     corps=[para("Depuis ta dernière visite, il s'est passé des choses dans l'Académie :"), liste(["[NOUVEAUTE_1]", "[NOUVEAUTE_2]", "[NOUVEAUTE_3]"]),
            para("Ton abonnement est toujours actif : profites-en !"), bouton("Revenir sur l'Académie", L("ACADEMIE"))])

# ---------- 6. Événements ----------
mail(id="19-annonce-masterclass", cat="Événements", quand="Dès qu'une masterclass est programmée (au moins 7 jours avant)", img="masterclasses", alt="Portrait du coach",
     objet="Masterclass en direct avec [COACH]", pre="[THEME], le [DATE] à [HEURE]. Pose tes questions !", sur="Nouvelle masterclass", titre="[THEME]",
     corps=[para("<b>[COACH]</b> ([TITRE_COACH]) te donne rendez-vous pour une masterclass en direct :"),
            billet("[THEME]", [("Heure", "[HEURE] · Paris"), ("Durée", "[DUREE]"), ("Niveau", "[NIVEAU]")]), coach(),
            para("[DESCRIPTION_MASTERCLASS]"), bouton("Voir la masterclass", L("MASTERCLASS")),
            para('<span style="color:#6b6b66;font-size:14px">Tu ne peux pas être là ? Le replay sera disponible dans l\'Académie.</span>')])
mail(id="20-rappel-masterclass", cat="Événements", quand="La veille, puis 1 heure avant (même modèle)", img="masterclasses", alt="Masterclass en direct",
     objet="[QUAND] : masterclass avec [COACH]", pre="[THEME], en direct à [HEURE].", sur="Rappel", titre="Rendez-vous à [HEURE] !",
     corps=[para("[PRENOM], la masterclass <b>[THEME]</b> avec <b>[COACH]</b> commence à <b>[HEURE]</b>. Prépare tes questions !"), bouton("Rejoindre le direct", L("DIRECT"))])
mail(id="21-replay-masterclass", cat="Événements", quand="Dès que le replay est en ligne", img="masterclasses", alt="Replay de masterclass",
     objet="Le replay est en ligne : [THEME]", pre="La masterclass de [COACH] en entier, et les positions en PGN.", sur="Replay disponible", titre="Tu l'as manquée ? Le replay est là.",
     corps=[para("La masterclass <b>[THEME]</b> avec <b>[COACH]</b> est disponible en replay."), encadre("<b>À retenir :</b> [RESUME_MASTERCLASS]"),
            bouton("Voir le replay", L("REPLAY")), para("Les positions étudiées sont aussi dans l'Académie, en PGN interactif.")])
mail(id="22-nouveau-cours", cat="Événements", quand="À la mise en ligne d'un nouveau cours ou d'un replay de cours", img="videos", alt="Nouveau cours en ligne",
     objet="Nouveau cours : [TITRE_COURS]", pre="[NB_LECONS_COURS] leçons, niveau [NIVEAU].", sur="Nouveau dans l'Académie", titre="[TITRE_COURS]",
     corps=[para("Un nouveau cours vient d'arriver dans l'Académie : <b>[TITRE_COURS]</b>, par [AUTEUR]."),
            tuiles([("[NB_LECONS_COURS]", "leçons"), ("[NIVEAU]", "niveau"), ("[DUREE]", "au total")]), para("[DESCRIPTION_COURS]"), bouton("Commencer le cours", L("COURS"))])
mail(id="23-annonce-tournoi", cat="Événements", quand="5 jours avant un tournoi, rappel le jour J (même modèle)", img="tournois", alt="Tournoi en ligne",
     objet="Tournoi : [NOM_TOURNOI] le [DATE]", pre="Cadence [CADENCE], ouvert à tous les niveaux.", sur="Tournoi en ligne", titre="[NOM_TOURNOI]",
     corps=[para("Mesure-toi aux autres membres de l'Académie !"), billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]"), ("Rondes", "[NB_RONDES]"), ("Niveau", "ouvert à tous")]),
            bouton("Je m'inscris", L("INSCRIPTION_TOURNOI"))])
mail(id="24-resultats-tournoi", cat="Événements", quand="Le lendemain du tournoi, aux participants", img="tournois", alt="Résultats du tournoi",
     objet="Résultats : [NOM_TOURNOI]", pre="Tu termines [PLACE]ᵉ sur [NB_JOUEURS] : bravo !", sur="Résultats", titre="Tu termines [PLACE]<sup>e</sup> !",
     corps=[para("[PRENOM], tu termines <b>[PLACE]<sup>e</sup> sur [NB_JOUEURS]</b> au <b>[NOM_TOURNOI]</b>, avec <b>[POINTS] points</b> sur [NB_RONDES]. Voici le podium :"),
            podium("[VAINQUEUR]", "[DEUXIEME]", "[TROISIEME]"), para("Revois tes parties : elles sont déjà dans ton espace, prêtes à être analysées."),
            bouton("Analyser mes parties", L("MES_PARTIES"))])
mail(id="25-sortie-revue", cat="Événements", quand="À la sortie de chaque numéro", img="revue", alt="La revue Europe Échecs",
     objet="Le n° [NUMERO] d'Europe Échecs est sorti", pre="Toutes les parties en PGN interactif dans l'Académie.", sur="La revue", titre="Le n° [NUMERO] est là.",
     corps=[para("Au sommaire de ce numéro :"), liste(["[SOMMAIRE_1]", "[SOMMAIRE_2]", "[SOMMAIRE_3]"]),
            para("Rejoue chaque partie commentée directement sur l'échiquier, en PGN interactif."), bouton("Lire le numéro", L("REVUE"))])

# ---------- 7. Lettre d'information (plusieurs nouvelles) ----------
mail(id="26-lettre-plusieurs-nouvelles", cat="Lettre d'information", quand="Toutes les 1 à 2 semaines, à tous les comptes (gratuits et abonnés)", img="progression", alt="Les nouvelles de l'Académie",
     objet="Cette semaine dans l'Académie : [TITRE_UNE]", pre="Masterclass, tournoi, nouveau cours et le puzzle de la semaine.", sur="Les nouvelles · [DATE]", titre="Cette semaine dans l'Académie",
     corps=[para("Bonjour [PRENOM], voici ce qui t'attend cette semaine."),
            carte("b-masterclass", "Masterclass : [THEME]", "Avec [COACH], en direct le [DATE] à [HEURE].", L("MASTERCLASS"), "Voir la masterclass"),
            carte("b-tournoi", "Tournoi : [NOM_TOURNOI]", "Le [DATE], cadence [CADENCE], ouvert à tous.", L("INSCRIPTION_TOURNOI"), "Je m'inscris"),
            carte("b-cours", "Nouveau cours : [TITRE_COURS]", "[NB_LECONS_COURS] leçons, niveau [NIVEAU].", L("COURS"), "Découvrir le cours"),
            carte("puzzle", "Le puzzle de la semaine", "[CONSIGNE_PUZZLE] Tu trouves ? La solution est en ligne.", L("PUZZLE"), "Voir la solution", src="[URL_IMAGE_PUZZLE]"),
            para('<span style="color:#6b6b66;font-size:14px">Les blocs sont indépendants : garde ceux qui ont une actualité et supprime les autres.</span>')])

# ---------- 8. Fin d'abonnement ----------
mail(id="27-renouvellement-annuel-j30", cat="Fin d'abonnement", marketing=False, quand="30 jours avant le renouvellement d'un abonnement annuel (obligatoire)",
     objet="Ton abonnement annuel se renouvelle le [DATE_RENOUVELLEMENT]", pre="Rien à faire si tu continues : voici le récapitulatif.", sur="Renouvellement", titre="Ton année d'Académie se termine bientôt.",
     corps=[para("[PRENOM], ton abonnement annuel se renouvellera automatiquement le <b>[DATE_RENOUVELLEMENT]</b> pour <b>[PRIX]</b>."),
            tuiles([("[NB_LECONS_ANNEE]", "leçons terminées cette année"), ("[NB_EXERCICES_ANNEE]", "exercices réussis")]),
            para("Rien à faire si tu continues. Tu peux modifier ou arrêter ton abonnement à tout moment avant cette date."), bouton("Gérer mon abonnement", L("ABONNEMENT_GERER"))])
mail(id="28-passage-annuel", cat="Fin d'abonnement", quand="Abonnés mensuels depuis 3 mois", img="progression", alt="Ta progression",
     objet="Près de 2 mois offerts en passant à l'annuel", pre="150 €/an au lieu de 12 × 14,90 € : tu économises.", sur="Ton abonnement", titre="Passe à l'annuel.",
     corps=[para("[PRENOM], ça fait 3 mois que tu progresses avec l'Académie. En passant à l'abonnement annuel, tu paies <b>150&nbsp;€ par an</b>, soit 12,50&nbsp;€ par mois au lieu de 14,90&nbsp;€."),
            ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr>' + carte_prix("Annuel", "150&nbsp;€", "/an", "12 × 14,90 € = 178,80 €", "Soit 12,50 € par mois. Ton tarif reste garanti tant que tu restes abonné.", True, "Près de 2 mois offerts") + "</tr></table>"), bouton("Passer à l'annuel", L("PASSAGE_ANNUEL"))])
mail(id="29-fin-abonnement-j7", cat="Fin d'abonnement", marketing=False, quand="7 jours avant la fin d'un abonnement résilié (fin de période payée)", img="oups", alt="La mascotte, surprise",
     objet="Ton accès à l'Académie se termine le [DATE_FIN]", pre="Ta progression reste enregistrée.", sur="Fin d'abonnement", titre="Plus que 7 jours d'accès.",
     corps=[para("[PRENOM], ton abonnement se termine le <b>[DATE_FIN]</b>. Après cette date, tu gardes ton compte gratuit (6 leçons, forum, puzzle du jour), et ta progression reste enregistrée."),
            para("Tu as changé d'avis ? Tu peux réactiver ton abonnement en un clic, au même tarif."), bouton("Réactiver", L("REACTIVATION"))])
mail(id="30-resiliation-confirmee", cat="Fin d'abonnement", marketing=False, quand="À la résiliation (transactionnel)",
     objet="Ta résiliation est confirmée", pre="Tu gardes l'accès jusqu'au [DATE_FIN].", sur="Résiliation", titre="C'est noté, [PRENOM].",
     corps=[para("Ta résiliation est enregistrée. Tu gardes l'accès complet à l'Académie jusqu'au <b>[DATE_FIN]</b>, puis ton compte repasse en gratuit."),
            para("Pour nous aider à nous améliorer, dis-nous en une question pourquoi tu pars :"), bouton("Répondre (30 secondes)", L("QUESTIONNAIRE_DEPART")),
            para('<span style="color:#6b6b66;font-size:14px">Ta progression, tes parties et tes statistiques restent enregistrées.</span>')])
mail(id="31-reconquete-j30", cat="Fin d'abonnement", quand="30 jours après la fin de l'abonnement", img="masterclasses", alt="Les nouveautés de l'Académie",
     objet="Ton premier mois à 9,90 € pour revenir", pre="Et tout ce qui a changé depuis ton départ.", sur="Quoi de neuf", titre="Reviens quand tu veux.",
     corps=[para("[PRENOM], l'Académie a continué d'avancer :"), liste(["[NOUVEAUTE_1]", "[NOUVEAUTE_2]", "[NOUVEAUTE_3]"]),
            ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr>' + carte_prix("Ton retour", "9,90&nbsp;€", "le 1er mois", "19,90 €/mois", "Puis 19,90 €/mois, sans engagement. Jusqu'au [DATE_FIN_OFFRE].", True, "Offre de retour") + "</tr></table>" + para("Ta progression t'attend là où tu l'as laissée.")), bouton("Revenir pour 9,90 €", L("REACTIVATION"))])
mail(id="32-anniversaire", cat="Engagement", quand="À la date anniversaire de l'abonnement", img="progression", alt="Anniversaire",
     objet="Déjà [DUREE_ABONNEMENT] dans l'Académie 🎉", pre="Merci, [PRENOM] ! Voici ton parcours.", sur="Anniversaire", titre="Joyeux anniversaire d'abonnement !",
     corps=[para("[PRENOM], ça fait <b>[DUREE_ABONNEMENT]</b> que tu t'entraînes avec nous. Merci !"),
            tuiles([("[NB_LECONS_TOTAL]", "leçons"), ("[NB_EXERCICES_TOTAL]", "exercices réussis"), ("[NB_MODULES]", "modules validés")]), bouton("Voir ma progression", L("PROGRESSION"))])


# ---------- 9. Compléments (compte, facturation, événements) ----------
mail(id="33-paiement-abandonne", cat="Compte gratuit → abonnement", quand="2 heures après une page de paiement ouverte sans paiement", 
     objet="Ton abonnement n'est pas finalisé", pre="Il ne manque qu'une étape.", sur="Abonnement", titre="Il ne manque qu'une étape.",
     corps=[para("[PRENOM], tu as commencé à t'abonner à l'Académie sans aller jusqu'au bout. Un souci avec le paiement ?"),
            recu([("Formule choisie", "[FORMULE]")], "Prix", "[PRIX]"), bouton("Finaliser mon abonnement", L("ABONNEMENT")),
            para('<span style="color:#6b6b66;font-size:14px">Une question ? Réponds simplement à cet e-mail.</span>')])
mail(id="34-changement-formule", cat="Abonnement", marketing=False, quand="Au passage du mensuel à l'annuel (ou l'inverse), transactionnel",
     objet="Ta nouvelle formule est enregistrée", pre="Voici ce qui change pour toi.", sur="Ton abonnement", titre="C'est enregistré.",
     corps=[para("[PRENOM], ton changement de formule est pris en compte."), recu([("Nouvelle formule", "[FORMULE]"), ("À partir du", "[DATE]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]")], "Nouveau prix", "[PRIX]"),
            bouton("Gérer mon abonnement", L("ABONNEMENT_GERER"))])
mail(id="35-carte-expire", cat="Abonnement", marketing=False, quand="30 jours avant l'expiration de la carte enregistrée (transactionnel)",
     objet="Ta carte bancaire expire bientôt", pre="Mets-la à jour pour éviter une interruption.", sur="Paiement", titre="Ta carte expire bientôt.",
     corps=[para("[PRENOM], la carte enregistrée pour ton abonnement (se terminant par [CARTE_4_CHIFFRES]) expire fin [MOIS_EXPIRATION]."),
            para("Mets-la à jour dès maintenant pour ne pas perdre l'accès à tes leçons."), bouton("Mettre à jour ma carte", L("PAIEMENT"))])
mail(id="36-inscription-tournoi", cat="Événements", marketing=False, quand="À l'inscription à un tournoi (transactionnel)", img="tournois", alt="Tournoi en ligne",
     objet="Inscription confirmée : [NOM_TOURNOI]", pre="Rendez-vous le [DATE] à [HEURE].", sur="Inscription confirmée", titre="C'est noté, à [HEURE] !",
     corps=[billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]")]),
            para("Connecte-toi 10 minutes avant le début : les appariements de la 1re ronde sont publiés à [HEURE]."), bouton("Voir le tournoi", L("TOURNOI")),
            para('<span style="color:#6b6b66;font-size:14px">Un empêchement ? <a href="[LIEN_DESINSCRIPTION_TOURNOI]" style="color:#1f5fa8">Libère ta place</a>.</span>')])
mail(id="37-masterclass-reportee", cat="Événements", marketing=False, quand="Si une masterclass annoncée est déplacée ou annulée (aux inscrits)",
     objet="Masterclass déplacée au [NOUVELLE_DATE]", pre="[THEME], avec [COACH] : la nouvelle date.", sur="Information", titre="La masterclass est déplacée.",
     corps=[para("[PRENOM], la masterclass <b>[THEME]</b> avec <b>[COACH]</b>, prévue le [DATE], est déplacée."),
            billet("[THEME]", [("Heure", "[HEURE] · Paris"), ("Avec", "[COACH]")], "[NOUVEAU_JOUR]", "[NOUVEAU_MOIS_COURT]"), para("Désolés pour ce changement. Si tu ne peux pas être là, le replay sera disponible comme d'habitude."),
            bouton("Voir la masterclass", L("MASTERCLASS"))])
mail(id="38-reponse-forum", cat="Engagement", quand="Quand quelqu'un répond à un sujet de l'abonné (au plus 1 par jour, regroupé)", img="forum", alt="Le forum de l'Académie",
     objet="[AUTEUR_REPONSE] t'a répondu sur le forum", pre="« [EXTRAIT_REPONSE] »", sur="Le forum", titre="Nouvelle réponse à ton sujet",
     corps=[para("<b>[AUTEUR_REPONSE]</b> a répondu à ton sujet « [TITRE_SUJET] » :"), encadre("« [EXTRAIT_REPONSE] »"), bouton("Lire et répondre", L("SUJET_FORUM"))])
mail(id="39-changement-tarif", cat="Abonnement", marketing=False, quand="Au moins 30 jours avant toute hausse de prix ou changement des conditions (obligatoire)",
     objet="Information importante sur ton abonnement", pre="Ce qui change le [DATE_EFFET], et tes options.", sur="Information", titre="Ce qui change pour ton abonnement",
     corps=[para("[PRENOM], à partir du <b>[DATE_EFFET]</b>, [CHANGEMENT]."), para("Si tu ne souhaites pas continuer, tu peux résilier à tout moment avant cette date, sans frais."),
            bouton("Gérer mon abonnement", L("ABONNEMENT_GERER")), para('<span style="color:#6b6b66;font-size:14px">Les conditions générales mises à jour sont <a href="[LIEN_CGV]" style="color:#1f5fa8">disponibles ici</a>.</span>')])
mail(id="40-suppression-compte", cat="Compte", marketing=False, quand="À la suppression du compte (transactionnel, dernier e-mail envoyé)",
     objet="Ton compte echecs.com est supprimé", pre="Tes données personnelles ont été effacées.", sur="Ton compte", titre="Au revoir, [PRENOM].",
     corps=[para("Ton compte echecs.com et tes données personnelles ont été supprimés, comme tu l'as demandé. Tu ne recevras plus d'e-mails de notre part."),
            para("Si tu changes d'avis, tu pourras toujours créer un nouveau compte : les 6 leçons, le forum et le puzzle du jour resteront gratuits."),
            para('<span style="color:#6b6b66;font-size:14px">Tu n\'es pas à l\'origine de cette demande ? Écris-nous vite à [EMAIL_CONTACT].</span>')],
     sign="Merci d'avoir joué avec nous,<br><b>L'équipe de l'Académie echecs.com</b>")

mail(id="41-parrainage", cat="Engagement", quand="À J+30 d'abonnement, puis après un module validé (au plus une fois par trimestre)", img="b-parrainage", alt="Invite un ami",
     objet="Invite un ami, et profitez-en tous les deux", pre="Ton ami reçoit [OFFRE_FILLEUL], toi [RECOMPENSE_PARRAIN].", sur="Parrainage", titre="Joue avec | tes amis.",
     corps=[para("[PRENOM], tu connais quelqu'un qui veut progresser aux échecs ? Partage ton lien : ton ami reçoit <b>[OFFRE_FILLEUL]</b>, et toi <b>[RECOMPENSE_PARRAIN]</b> dès qu'il s'abonne."),
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0"><tr><td align="center" style="border:2px dashed {C["jaune"]};border-radius:14px;background:#fff6c2;padding:18px">'
            f'<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:{C["gris"]}">Ton code</div>'
            f'<div style="margin-top:6px;font-family:{SANS};font-weight:800;font-size:30px;letter-spacing:.12em;color:#111">[CODE_PARRAINAGE]</div></td></tr></table>',
            bouton("Partager mon lien", L("PARRAINAGE")), para('<span style="color:#6b6b66;font-size:14px">Pas de limite : chaque ami abonné te rapporte [RECOMPENSE_PARRAIN].</span>')])
mail(id="42-filleul-abonne", cat="Engagement", quand="Quand un ami parrainé s'abonne", img="b-filleul", alt="Ton ami est arrivé",
     objet="[PRENOM_FILLEUL] a rejoint l'Académie grâce à toi 🎉", pre="Ta récompense : [RECOMPENSE_PARRAIN].", sur="Parrainage", titre="Merci | pour l'invitation !",
     corps=[para("<b>[PRENOM_FILLEUL]</b> vient de s'abonner à l'Académie avec ton code. Comme promis, tu reçois <b>[RECOMPENSE_PARRAIN]</b> : c'est déjà sur ton compte."),
            para("Défiez-vous sur l'échiquier : les tournois en ligne sont ouverts à tous les niveaux."), bouton("Voir le prochain tournoi", L("TOURNOIS"))])

# Titres en deux temps (« | » : la suite en italique bleu) et mascotte des e-mails sans image
TITRES = {
    "01-confirmation-adresse": "Plus qu'un clic, | [PRENOM] !", "02-bienvenue-compte-gratuit": "Ton compte | est prêt.",
    "03-mot-de-passe": "Nouveau | mot de passe.", "04-gratuit-j3-lecons": "Tu as essayé | une leçon ?", "05-gratuit-j7-offre": "Passe à | l'Académie complète.",
    "06-gratuit-j21-relance": "Tu hésites | encore ?", "07-confirmation-abonnement": "Tu fais partie | de l'Académie.", "08-paiement-refuse": "Ton paiement | n'est pas passé.",
    "09-paiement-recu": "Merci, | [PRENOM] !", "10-demarrage-j1-parcours": "Trouve | ton niveau.", "11-demarrage-j3-exercices": "10 minutes | par jour.",
    "12-demarrage-j6-masterclasses": "Apprends | des meilleurs.", "13-demarrage-j10-communaute": "Rejoins | la communauté.", "14-bilan-mensuel": "Ton mois | en chiffres.",
    "15-objectif-atteint": "Module validé. | Au suivant !", "16-serie-en-danger": "Garde | ta série !", "17-inactif-7-jours": "On reprend | là où tu en étais ?",
    "18-inactif-30-jours": "Tu nous | manques !", "21-replay-masterclass": "Tu l'as manquée ? | Le replay est là.", "24-resultats-tournoi": "Merci | d'avoir joué !",
    "25-sortie-revue": "Le n° [NUMERO] | est là.", "26-lettre-plusieurs-nouvelles": "Cette semaine | dans l'Académie.", "27-renouvellement-annuel-j30": "Ton année d'Académie | se termine bientôt.",
    "28-passage-annuel": "Passe | à l'annuel.", "29-fin-abonnement-j7": "Plus que 7 jours | d'accès.", "30-resiliation-confirmee": "C'est noté, | [PRENOM].",
    "31-reconquete-j30": "Reviens | quand tu veux.", "32-anniversaire": "Joyeux anniversaire | d'abonnement !", "33-paiement-abandonne": "Il ne manque | qu'une étape.",
    "34-changement-formule": "C'est | enregistré.", "35-carte-expire": "Ta carte | expire bientôt.", "36-inscription-tournoi": "C'est noté, | rendez-vous à [HEURE] !",
    "37-masterclass-reportee": "La masterclass | est déplacée.", "38-reponse-forum": "Nouvelle réponse | à ton sujet.", "39-changement-tarif": "Ce qui change | pour ton abonnement.",
    "40-suppression-compte": "Au revoir, | [PRENOM].", "20-rappel-masterclass": "Rendez-vous | à [HEURE] !", "19-annonce-masterclass": "Nouvelle | masterclass.", "23-annonce-tournoi": "À toi | de jouer !", "22-nouveau-cours": "Nouveau cours : | [TITRE_COURS]",
}
MASCOTTES = {"01-confirmation-adresse": "coucou", "03-mot-de-passe": "cherche", "08-paiement-refuse": "gratte-tete", "09-paiement-recu": "super",
             "30-resiliation-confirmee": "reverence", "33-paiement-abandonne": "gratte-tete", "34-changement-formule": "super", "35-carte-expire": "telephone",
             "37-masterclass-reportee": "pendule", "27-renouvellement-annuel-j30": "pendule", "39-changement-tarif": "pancarte", "40-suppression-compte": "coucou"}
ENTETES = {"02": "bienvenue", "04": "lecons", "05": "offre", "06": "hesites", "07": "abonne", "10": "parcours", "11": "exercices", "12": "masterclasses",
           "13": "communaute", "14": "bilan", "15": "module", "16": "serie", "17": "reprendre", "18": "manque", "19": "masterclass", "20": "masterclass",
           "21": "replay", "22": "cours", "23": "tournoi", "24": "resultats", "25": "revue", "26": "nouvelles", "28": "annuel", "29": "fin", "31": "retour",
           "32": "anniversaire", "36": "inscription", "38": "forum"}
for e in E:   # objet et pré-en-tête : apostrophe typographique aussi
    for k in ("objet", "pre"): e[k] = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", "’", e[k])
    if e["id"][:2] in ENTETES: e["img"] = "b-" + ENTETES[e["id"][:2]]
    e["titre"] = TITRES.get(e["id"], e["titre"])
    if e["id"] in MASCOTTES: e["mascotte"] = MASCOTTES[e["id"]]

MASC = sorted({e["mascotte"] for e in E if e.get("mascotte") and not e.get("img")})
if MASC:
    import subprocess
    subprocess.run(["node", str(ICI / "scripts/mascotte-png.mjs"), ",".join(MASC)], check=True, capture_output=True)
    for m in MASC:
        im = Image.open(ICI / f"build/_mascotte/{m}.png"); im = im.crop(im.getbbox())
        for d in (OUT, APER): im.save(d / "img" / f"mascotte-{m}.png", optimize=True)
# Valeurs d'exemple pour les aperçus (les fichiers livrés gardent les variables)
EXEMPLES = {"PRENOM": "Léa", "DATE": "18 novembre", "HEURE": "20 h 30", "JOUR": "18", "MOIS_COURT": "nov.", "NOUVEAU_JOUR": "25", "NOUVEAU_MOIS_COURT": "nov.",
    "NOUVELLE_DATE": "25 novembre", "THEME": "Les plans typiques du milieu de partie", "COACH": "Gata Kamsky", "TITRE_COACH": "GMI", "DUREE": "1 h 30", "DUREE_LECON": "15 min", "NIVEAU": "1400 à 1800",
    "DESCRIPTION_MASTERCLASS": "Comment choisir un plan à partir de la structure de pions, avec des parties commentées en direct.", "NOM_TOURNOI": "Blitz du samedi",
    "CADENCE": "3 min + 2 s", "NB_RONDES": "7", "PLACE": "4", "POINTS": "5", "NB_JOUEURS": "38", "VAINQUEUR": "Hugo M.", "DEUXIEME": "Camille R.", "TROISIEME": "Inès B.",
    "FORMULE": "Annuelle", "PRIX": "150,00 €", "DATE_PROCHAIN_PAIEMENT": "18 novembre 2027", "MOYEN_PAIEMENT": "Carte •••• 4242", "MOIS": "novembre",
    "NB_LECONS": "12", "NB_EXERCICES": "184", "TAUX_REUSSITE": "78", "SERIE_MAX": "9", "THEME_FORT": "les finales de Tours", "THEME_FAIBLE": "le clouage",
    "MODULE": "Objectif 1400 · Tactique", "MODULE_SUIVANT": "Objectif 1400 · Finales", "NB_LECONS_MODULE": "14", "NB_EXERCICES_MODULE": "96", "SERIE": "12",
    "DERNIERE_LECON": "La règle du carré", "LECON_SUIVANTE": "L'opposition", "TITRE_COURS": "Les finales de Tours", "AUTEUR": "Marc Quenehen", "NB_LECONS_COURS": "18",
    "DESCRIPTION_COURS": "Lucena, Philidor, la Tour active : tout ce qu'il faut savoir pour sauver ou gagner les finales les plus fréquentes.", "NUMERO": "780",
    "SOMMAIRE_1": "Le championnat de France décrypté", "SOMMAIRE_2": "Les secrets de la Caro-Kann", "SOMMAIRE_3": "Finales : la défense de Vancura",
    "NOUVEAUTE_1": "Un nouveau cours sur les finales de Tours", "NOUVEAUTE_2": "3 masterclasses en replay", "NOUVEAUTE_3": "Le n° 780 de la revue en PGN",
    "NB_LECONS_ANNEE": "86", "NB_EXERCICES_ANNEE": "1 240", "NB_LECONS_TOTAL": "86", "NB_EXERCICES_TOTAL": "1 240", "NB_MODULES": "5", "DUREE_ABONNEMENT": "1 an",
    "DATE_RENOUVELLEMENT": "18 décembre", "DATE_FIN": "30 novembre", "DATE_SUSPENSION": "25 novembre", "DATE_FIN_OFFRE": "15 décembre", "TITRE_UNE": "masterclass avec Gata Kamsky",
    "NB_LECONS_GRATUITES_RESTANTES": "4", "CARTE_4_CHIFFRES": "4242", "MOIS_EXPIRATION": "décembre", "AUTEUR_REPONSE": "Sylvain Ravot", "TITRE_SUJET": "Que jouer contre la Caro-Kann ?",
    "EXTRAIT_REPONSE": "Essaie la variante d'avance : 3.e5, avec un plan simple…", "DATE_EFFET": "1er février", "CHANGEMENT": "l'abonnement mensuel passera à 21,90 €",
    "EMAIL_CONTACT": "contact@echecs.com", "RESUME_MASTERCLASS": "choisis ton plan d'après la structure de pions, pas d'après la position des pièces.", "URL_PHOTO_COACH": "img/coach-exemple.jpg", "URL_IMAGE_PUZZLE": "img/puzzle-exemple.jpg",
    "CONSIGNE_PUZZLE": "Les Blancs jouent et font mat en 1.", "OFFRE_FILLEUL": "son premier mois à 9,90 €", "RECOMPENSE_PARRAIN": "un mois offert",
    "CODE_PARRAINAGE": "LEA-2026", "PRENOM_FILLEUL": "Thomas", "QUAND": "Demain", "ADRESSE_POSTALE": "Paris, France"}
def exemple(h):
    r = re.sub(r"\[([A-Z_0-9]+)\]", lambda m: EXEMPLES.get(m.group(1), m.group(0)) if not m.group(1).startswith("LIEN_") else "#", h)
    return r[:r.index("<body")] + typo(r[r.index("<body"):])
VARS = set()
for e in E:
    h = page(e)
    h = h[:h.index("<body")] + typo(h[h.index("<body"):])
    h = h.replace("<sup>", '<sup style="font-size:.7em;line-height:0;vertical-align:super">')   # exposants sans agrandir l'interligne
    VARS |= set(re.findall(r"\[[A-Z_0-9]+\]", h))
    (OUT / f"{e['id']}.html").write_text(h.replace("{IMG}", "[URL_IMAGES]").replace("{FONTS}", FONTS_WEB))
    # aperçu : la ligne de la boîte de réception (expéditeur, objet, pré-en-tête), comme sur un téléphone
    boite = (f'<div style="background:#ffffff;border-bottom:1px solid #e4e1d8;padding:14px 18px;font-family:{SANS}">'
             f'<div style="display:flex;align-items:center;gap:10px"><div style="width:34px;height:34px;border-radius:50%;background:#0f1420;color:#fae361;font:900 16px/34px {SERIF};text-align:center">é</div>'
             f'<div style="flex:1;min-width:0"><div style="font-weight:800;font-size:14px;color:#1d1d1b">Académie echecs.com <span style="float:right;font-weight:500;color:#6b6b66">09:41</span></div>'
             f'<div style="font-weight:700;font-size:14px;color:#1d1d1b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{e["objet"]}</div>'
             f'<div style="font-size:14px;color:#6b6b66;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{e["pre"]}</div></div></div></div>')
    ha = h.replace("{IMG}", "img").replace("{FONTS}", FONTS_LOCAL)
    ha = ha.replace('<body style="margin:0;padding:0;background:#f1f0ea">', '<body style="margin:0;padding:0;background:#f1f0ea">' + boite, 1)
    (APER / f"{e['id']}.html").write_text(exemple(ha))
print(len(E), "e-mails ·", len(VARS), "variables")

# Catalogue pour pack/EMAILS.md (section générée)
lignes = []
cat = None
ORDRE = list(dict.fromkeys(e["cat"] for e in E))
for e in sorted(E, key=lambda e: (ORDRE.index(e["cat"]), e["id"])):
    if e["cat"] != cat:
        cat = e["cat"]; lignes.append(f"\n### {cat}\n\n| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |\n|---|---|---|---|---|")
    lignes.append(f"| `{e['id']}.html` | {e['quand']} | {e['objet']} | {e['pre']} | {'Information (désinscription possible)' if e.get('marketing', True) else 'Compte (toujours envoyé)'} |")
(ICI / "build/_emails_catalogue.md").write_text("\n".join(lignes) + "\n")
(ICI / "build/_emails_variables.txt").write_text("\n".join(sorted(VARS)) + "\n")

# Met à jour le catalogue de pack/EMAILS.md (entre « ## Catalogue » et « ## Variables »)
doc = ICI / "pack/EMAILS.md"
if doc.exists():
    t = doc.read_text(); a, b = t.find("## Catalogue"), t.find("## Variables")
    if a >= 0 and b > a: doc.write_text(t[:a] + "## Catalogue\n" + "\n".join(lignes) + "\n\n" + t[b:])
