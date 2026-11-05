#!/usr/bin/env python3
"""E-mails de suivi des abonnés de l'Académie echecs.com : HTML prêt à intégrer dans l'outil d'envoi maison.

Écrit build/pack/emails/ : un fichier HTML par e-mail (images en [URL_IMAGES]/…, variables entre crochets),
le dossier img/ à héberger, et build/_emails_apercu/ (mêmes e-mails avec les images locales, pour les captures).
Le catalogue (déclencheur, objet, pré-en-tête, variables) est dans pack/EMAILS.md.
Deux séries : « abonnes » (par défaut) et « ccas » (bénéficiaires des Activités Sociales de l'Énergie, accès offert, sans paiement).
Le contenu de chaque série est dans scripts/emails-contenu-<série>.py ; ce fichier fournit le design et les composants.
Usage : python3 scripts/emails.py [abonnes|ccas]"""
import html, pathlib, re, shutil, sys
PROFIL = sys.argv[1] if len(sys.argv) > 1 else "abonnes"
SUF = "" if PROFIL == "abonnes" else "-" + PROFIL

ICI = pathlib.Path(__file__).resolve().parent.parent
PACK = ICI / "build/pack"
OUT = PACK / f"emails{SUF}"; APER = ICI / f"build/_emails{SUF}_apercu"; ART = ICI / f"build/_emails{SUF}_artefact"
shutil.rmtree(ART, ignore_errors=True); ART.mkdir(parents=True)
for d in (OUT, APER):
    shutil.rmtree(d, ignore_errors=True); (d / "img").mkdir(parents=True)

# Images utilisées (copiées dans img/, à héberger à l'adresse [URL_IMAGES])
IMG = {
    "logo": ICI.parent / ("assets/brand/ccas/logo-email-560.png" if PROFIL == "ccas" else "assets/brand/logo-echecs-com-blanc.png"),
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
# Miniature d'exemple pour les aperçus (vraie miniature de cours si présente, sinon l'échiquier du puzzle), bouton lecture incrusté
import importlib.util
_spec = importlib.util.spec_from_file_location("miniature_mail", ICI / "scripts/miniature-mail.py"); _mm = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mm)
_ex = ICI / "assets/exemples/miniature-cours-youtube.jpg"
if not _ex.exists():
    _m = Image.new("RGB", (1280, 720), (15, 20, 32)); _m.paste(Image.open(PACK / "images/00-emails/email-puzzle-1080x1080.jpg").convert("RGB").resize((620, 620), Image.LANCZOS), (330, 50))
    _ex = APER / "_miniature-source.jpg"; _m.save(_ex, quality=90)
_mm.miniature_mail(_ex, APER / "img/miniature-exemple.jpg")
if PROFIL == "ccas": shutil.copy(ICI.parent / "assets/brand/ccas/ccas-favicon-72.png", APER / "img/favicon.png")   # pastille de l'expéditeur (aperçus)
C = {"em": "#2c4a6e", "fond": "#f1f0ea", "nuit": "#0f1420", "texte": "#1d1d1b", "gris": "#6b6b66", "jaune": "#fae361", "bleu": "#93b9e2", "vert": "#2f9e44", "carte": "#ffffff", "filet": "#e4e1d8"}
SERIF = "'Fraunces', Georgia, 'Times New Roman', serif"; SANS = "'Manrope', 'Helvetica Neue', Arial, sans-serif"
# Polices de l'Académie : Google Fonts dans les e-mails envoyés (Apple Mail, iOS, Outlook.com les affichent ; Gmail garde Georgia / Arial),
# fichiers locaux pour les aperçus.
FONTS_WEB = '<!--[if !mso]><!--><link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,900;1,9..144,400&family=Manrope:wght@400;700;800&display=swap" rel="stylesheet"><!--<![endif]-->'
# Outlook sur PC (moteur Word) : il ne charge pas les polices web et prendrait Times New Roman ; on impose Arial et Georgia
FONTS_WEB += '<!--[if mso]><style>body,table,td,p,a,div,span,li{font-family:Arial,Helvetica,sans-serif !important} h1,h1 span{font-family:Georgia,serif !important}</style><![endif]-->'
NM = ICI / "node_modules/@fontsource"
FONTS_LOCAL = "<style>" + "".join(f'@font-face{{font-family:"{f}";font-weight:{w};font-style:{st};src:url("file://{NM}/{f.lower()}/files/{f.lower()}-latin-{w}-{st}.woff2") format("woff2")}}'
    for f, w, st in (("Fraunces", 900, "normal"), ("Fraunces", 400, "italic"), ("Manrope", 400, "normal"), ("Manrope", 700, "normal"), ("Manrope", 800, "normal"))) + "</style>"

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
            f'<div class="m-prix" style="margin-top:8px;font-family:{SERIF};font-weight:900;font-size:32px;line-height:1;color:{C["texte"]};white-space:nowrap">{prix}</div>'
            f'<div style="margin-top:4px;font-family:{SANS};font-weight:700;font-size:14px;color:{C["gris"]}">{unite}</div>'
            f'<div style="margin-top:6px;font-family:{SANS};font-size:14px;color:{C["gris"]}"><s>{barre}</s></div>'
            f'<div style="margin-top:10px;font-family:{SANS};font-weight:700;font-size:14px;line-height:1.4;color:{C["texte"]}">{note}</div></td>')
def offre(intro=""):   # les deux formules au prix de lancement, l'annuelle mise en avant
    return ((para(intro) if intro else "") + '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate;border-spacing:6px 0;table-layout:fixed"><tr>'
            + carte_prix("Mensuel", "14,90&nbsp;€", "/mois", "19,90 €/mois", "Sans engagement")
            + carte_prix("Annuel", "150&nbsp;€", "/an", "179,90 €/an", "Soit 12,50 € par mois", True, "Le plus avantageux") + "</tr></table>"
            + f'<p style="margin:0 0 6px;font-family:{SANS};font-size:14px;color:{C["gris"]}">Prix de lancement, garanti tant que ton abonnement reste actif.</p>')
def carte(img, titre, texte, lien, cta, src=None):
    return f'''<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 22px;border:1px solid {C['filet']};border-radius:12px;overflow:hidden">
<tr><td{' style="background:#f1f0ea;padding:18px 18px 0"' if src else ""}><img src="{src or "{IMG}/" + img + ".jpg"}" width="{500 if src else 536}" alt="" style="display:block;width:100%;height:auto;border:0;{"border-radius:10px;" if src else ""}"></td></tr>
<tr><td style="padding:18px 20px 20px"><div style="font:900 20px/1.3 {SERIF};color:{C['texte']};margin:0 0 8px">{titre}</div>
<div style="font:16px/1.55 {SANS};color:{C['texte']};margin:0 0 12px">{texte}</div><a href="{lien}" style="font:bold 16px {SANS};color:#1f5fa8;text-decoration:none">{cta}&nbsp;&rarr;</a></td></tr></table>'''

def video(miniature, titre, sous, lien_lecon, lien_youtube):   # cours filmé : miniature YouTube en entier (bouton lecture incrusté, scripts/miniature-mail.py), titre, liens
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 22px;border:1px solid {C["filet"]};border-radius:12px;overflow:hidden">'
            f'<tr><td style="background:{C["nuit"]}"><a href="{lien_youtube}"><img src="{miniature}" width="536" alt="Regarder la vidéo : {titre}" style="display:block;width:100%;height:auto;border:0"></a></td></tr>'
            f'<tr><td style="padding:16px 20px 18px"><div style="font:900 20px/1.3 {SERIF};color:{C["texte"]};margin:0 0 6px">{titre}</div>'
            f'<div style="font:14px/1.5 {SANS};color:{C["gris"]};margin:0 0 12px">{sous}</div>'
            f'<a href="{lien_lecon}" style="font:bold 16px {SANS};color:#1f5fa8;text-decoration:none">Revoir le cours&nbsp;&rarr;</a>'
            f'<span style="font:16px {SANS};color:{C["filet"]}">&nbsp;&nbsp;|&nbsp;&nbsp;</span>'
            f'<a href="{lien_youtube}" style="font:bold 16px {SANS};color:#1f5fa8;text-decoration:none">Sur YouTube&nbsp;&rarr;</a></td></tr></table>')

def progression(titre, pct):   # avancement dans un parcours : titre, pourcentage, barre jaune sur fond crème (pct = nombre de 0 à 100, ou variable)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:8px 0 24px"><tr>'
            f'<td style="font-family:{SANS};font-weight:800;font-size:14px;color:{C["texte"]};padding:0 0 8px">{titre}</td>'
            f'<td align="right" style="font-family:{SERIF};font-weight:900;font-size:20px;color:{C["texte"]};padding:0 0 8px;white-space:nowrap">{pct}&nbsp;%</td></tr>'
            f'<tr><td colspan="2" style="background:{C["fond"]};border-radius:999px;padding:3px">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="{pct}%" style="width:{pct}%"><tr><td height="12" bgcolor="{C["jaune"]}" style="height:12px;line-height:12px;font-size:0;background:{C["jaune"]};border-radius:999px">&nbsp;</td></tr></table>'
            f'</td></tr></table>')
def nouveautes(titre, items):   # ce qui s'est passé sur la plateforme : intitulé, puis « libellé : valeur » (accord toujours juste, quelle que soit la valeur)
    rows = "".join(f'<tr><td style="padding:9px 0;font-family:{SANS};font-size:16px;color:{C["texte"]};border-top:1px solid {C["filet"]}">{k}</td>'
                   f'<td align="right" style="padding:9px 0;font-family:{SERIF};font-weight:900;font-size:20px;color:{C["texte"]};border-top:1px solid {C["filet"]};white-space:nowrap">{v}</td></tr>' for k, v in items)
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr><td style="background:{C["fond"]};border-radius:14px;padding:16px 20px 8px">'
            f'<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:{C["em"]};margin:0 0 8px">{titre}</div>'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">{rows}</table></td></tr></table>')

DARK = """<meta name="color-scheme" content="light dark"><meta name="supported-color-schemes" content="light dark"><style>
@media (max-width: 480px) { .m-pad { padding-left:20px !important; padding-right:20px !important; } .m-out { padding-left:0 !important; padding-right:0 !important; padding-top:0 !important; } h1 { font-size:28px !important; } }
@media (max-width: 360px) { .m-prix { font-size:25px !important; } }
@media (prefers-color-scheme: dark) {
  body, [style*="background:#f1f0ea"] { background:#06080c !important; }
  [style*="background:#ffffff"] { background:#121a25 !important; }
  td[style*="background:#f1f0ea"], div[style*="background:#f1f0ea"] { background:#1b2533 !important; }
  [style*="color:#1d1d1b"] { color:#f4f1ea !important; } [style*="color:#6b6b66"] { color:#a9b4c2 !important; }
  [style*="color:#2c4a6e"] { color:#93b9e2 !important; } [style*="color:#0066cc"] { color:#7db8f5 !important; } a[style*="color:#1f5fa8"] { color:#93b9e2 !important; }
  [style*="#e4e1d8"] { border-color:#2a3546 !important; }
  td[style*="border-radius:14px 0 0 14px"] { background:#26324a !important; }
  [style*="background:#fff6c2"] [style*="color:#1d1d1b"], [style*="background:#fae361"] [style*="color:#1d1d1b"] { color:#111111 !important; }
  [style*="background:#fff6c2"] [style*="color:#6b6b66"] { color:#4a4636 !important; }
}
</style>"""
def typo(h):   # espace insécable avant : ; ? ! » % et après «, entre un nombre et son unité ; seulement dans le texte, jamais dans les balises
    def t(x):
        x = re.sub(r" ([:;?!»%])", "\u00a0\\1", x); x = x.replace("« ", "«\u00a0")
        x = re.sub(r"(?<=[A-Za-zÀ-ÿ])'(?=[A-Za-zÀ-ÿ])", "’", x)   # apostrophe typographique
        x = re.sub(r"\be-mail", "e\u2011mail", x)   # « e-mail » jamais coupé au trait d'union
        x = re.sub(r"\b1(er|re)\b", r"1<sup>\1</sup>", x)
        x = re.sub(r"(\d) (janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)", "\\1\u00a0\\2", x)   # 18 novembre
        x = re.sub(r"\b(Objectif|n°|N°|Calcul Gagnant) (\d)", "\\1\u00a0\\2", x)   # Objectif 1400, n° 780
        x = re.sub(r"(\d) (h|min|€|s|jours?|leçons|exercices|points|ans?)\b", "\\1\u00a0\\2", x)
        x = re.sub(r"(\d\u00a0h) (\d)", "\\1\u00a0\\2", x)   # 20 h 30
        return re.sub(r"(\d) (\d{3})\b", "\\1\u00a0\\2", x)
    return "".join(p if p.startswith("<") else t(p) for p in re.split(r"(<[^>]+>)", h))
# Réglages propres à la série (le fichier de contenu peut les changer)
EXPEDITEUR = "Académie echecs.com"
AVATAR = "é"   # pastille de l'expéditeur dans l'aperçu de la boîte de réception
POURQUOI = "Tu reçois cet e-mail car tu as un compte sur echecs.com."
SIGNATURE = "À très vite sur l'échiquier,<br><b>L'équipe de l'Académie echecs.com</b>"
ENTETE = f'''<tr><td class="m-pad" style="background:{C['nuit']};padding:22px 32px"><img src="{{IMG}}/logo.png" width="170" alt="echecs.com" style="display:block;border:0;width:170px;height:auto"></td></tr>'''
LIENS_PIED = [("L'Académie", "[LIEN_ACADEMIE]"), ("Masterclasses", "[LIEN_MASTERCLASSES]"), ("Tournois", "[LIEN_TOURNOIS]"), ("Forum", "[LIEN_FORUM]")]
RESEAUX = [("Instagram", "[LIEN_INSTAGRAM]"), ("Facebook", "[LIEN_FACEBOOK]"), ("YouTube", "[LIEN_YOUTUBE]"), ("X", "[LIEN_X]"), ("LinkedIn", "[LIEN_LINKEDIN]")]
MENTION = "echecs.com · Europe Échecs · [ADRESSE_POSTALE]"
DOC = ICI / "pack/EMAILS.md"
def page(e):
    pied = (POURQUOI + " "
            + ('<a href="[LIEN_PREFERENCES]" style="color:#6b6b66">Gérer mes e&#8209;mails</a> · <a href="[LIEN_DESINSCRIPTION]" style="color:#6b6b66">Se désinscrire</a>' if e.get("marketing", True)
               else "Cet e-mail concerne ton compte : il est envoyé même si tu as refusé les e-mails d'information."))
    hero = f'<tr><td><img src="{{IMG}}/{e["img"]}.jpg" width="600" alt="{html.escape(e.get("alt", ""))}" style="display:block;width:100%;height:auto;border:0"></td></tr>' if e.get("img") else ""
    if not e.get("img") and e.get("mascotte"):   # pas d'image : la mascotte, sur le fond nuit de l'en-tête
        hero = f'<tr><td align="center" style="background:{C["nuit"]};padding:4px 0 0"><img src="{{IMG}}/mascotte-{e["mascotte"]}.png" height="150" alt="" style="display:block;height:150px;width:auto;border:0;margin:6px auto 0"></td></tr>'
    t1, _, t2 = e["titre"].partition("|")
    # deux temps sur la même ligne (la suite en italique bleu) : retour à la ligne seulement s'il manque de place
    titre = t1.strip() + (f' <span style="font-family:{SERIF};font-style:italic;font-weight:400;color:{C["em"]}">{t2.strip()}</span>' if t2 else "")
    corps = "".join(e["corps"])
    return f'''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="x-apple-disable-message-reformatting">
<title>{html.escape(e["objet"])}</title>{{FONTS}}{DARK}</head>
<body style="margin:0;padding:0;background:{C['fond']}">
<div style="display:none;max-height:0;overflow:hidden;opacity:0">{html.escape(e["pre"])}&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;&#847;&zwnj;&nbsp;</div>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background:{C['fond']}"><tr><td class="m-out" align="center" style="padding:24px 12px">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="width:100%;max-width:600px;background:{C['carte']};border-radius:16px;overflow:hidden">
{ENTETE}
{hero}
<tr><td class="m-pad" style="padding:34px 32px 30px">
<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:{C['em']};margin:0 0 14px">&mdash;&nbsp;{e['sur']}</div>
<h1 style="margin:0 0 22px;font-family:{SERIF};font-weight:900;font-size:32px;line-height:1.15;color:{C['texte']}">{titre}</h1>
{corps}
<p style="margin:26px 0 0;font:16px/1.6 {SANS};color:{C['texte']}">{e.get('sign', SIGNATURE)}</p>
</td></tr>
<tr><td class="m-pad" style="padding:22px 32px 6px;border-top:1px solid {C['filet']};font-family:{SANS};font-weight:700;font-size:14px;color:{C['texte']}">
{"&nbsp;· ".join(f'<a href="{l}" style="color:{C['texte']};text-decoration:none">{t}</a>' for t, l in LIENS_PIED)}</td></tr>
{f'<tr><td class="m-pad" style="padding:4px 32px 0;font-family:{SANS};font-size:12px;color:{C["gris"]}">Suis-nous : ' + " · ".join(f'<a href="{l}" style="color:{C["gris"]}">{t}</a>' for t, l in RESEAUX) + '</td></tr>' if RESEAUX else ""}
<tr><td class="m-pad" style="padding:12px 32px 26px;font:12px/1.6 {SANS};color:{C['gris']}">{pied}<br>{MENTION}</td></tr>
</table></td></tr></table></body></html>'''

L = lambda nom: f"[LIEN_{nom}]"
E = []
def mail(**k): E.append(k)
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
# Contenu de la série (mails, TITRES, MASCOTTES, ENTETES ; peut compléter EXEMPLES et changer les réglages ci-dessus)
exec(compile((ICI / f"scripts/emails-contenu-{PROFIL}.py").read_text(), f"emails-contenu-{PROFIL}.py", "exec"))
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
def exemple(h, propres=None):   # propres : exemples propres à un e-mail (ex. les chiffres d'une semaine peu active)
    ex = {**EXEMPLES, **(propres or {})}
    r = re.sub(r"\[([A-Z_0-9]+)\]", lambda m: ex.get(m.group(1), m.group(0)) if not m.group(1).startswith("LIEN_") else "#", h)
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
             f'<div style="display:flex;align-items:center;gap:10px"><div style="width:34px;height:34px;border-radius:50%;background:#0f1420;color:#fae361;font:900 16px/34px {SERIF};text-align:center">{AVATAR}</div>'
             f'<div style="flex:1;min-width:0"><div style="font-weight:800;font-size:14px;color:#1d1d1b">{EXPEDITEUR} <span style="float:right;font-weight:500;color:#6b6b66">09:41</span></div>'
             f'<div style="font-weight:700;font-size:14px;color:#1d1d1b;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{e["objet"]}</div>'
             f'<div style="font-size:14px;color:#6b6b66;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">{e["pre"]}</div></div></div></div>')
    ha = h.replace("{IMG}", "img").replace("{FONTS}", FONTS_LOCAL)
    ha = ha.replace('<body style="margin:0;padding:0;background:#f1f0ea">', '<body style="margin:0;padding:0;background:#f1f0ea">' + boite, 1)
    (APER / f"{e['id']}.html").write_text(exemple(ha, e.get("exemples")))
    # version pour la page de validation des e-mails (polices en ligne, exemples, ligne de boîte de réception)
    hb = h.replace("{IMG}", "img").replace("{FONTS}", FONTS_WEB).replace('<body style="margin:0;padding:0;background:#f1f0ea">', '<body style="margin:0;padding:0;background:#f1f0ea">' + boite, 1)
    (ART / f"{e['id']}.html").write_text(exemple(hb, e.get("exemples")))
print(len(E), "e-mails ·", len(VARS), "variables")

# Catalogue pour pack/EMAILS.md (section générée)
lignes = []
cat = None
ORDRE = list(dict.fromkeys(e["cat"] for e in E))
for e in sorted(E, key=lambda e: (ORDRE.index(e["cat"]), e["id"])):
    if e["cat"] != cat:
        cat = e["cat"]; lignes.append(f"\n### {cat}\n\n| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |\n|---|---|---|---|---|")
    lignes.append(f"| `{e['id']}.html` | {e['quand']} | {e['objet']} | {e['pre']} | {'Information (désinscription possible)' if e.get('marketing', True) else 'Compte (toujours envoyé)'} |")
(ICI / f"build/_emails{SUF}_catalogue.md").write_text("\n".join(lignes) + "\n")
(ICI / f"build/_emails{SUF}_variables.txt").write_text("\n".join(sorted(VARS)) + "\n")

# Met à jour le catalogue de pack/EMAILS.md (entre « ## Catalogue » et « ## Variables »)
doc = DOC
if doc.exists():
    t = doc.read_text(); a, b = t.find("## Catalogue"), t.find("## Variables")
    if a >= 0 and b > a: doc.write_text(t[:a] + "## Catalogue\n" + "\n".join(lignes) + "\n\n" + t[b:])
shutil.copytree(APER / "img", ART / "img")
# img/ à héberger : seulement les images utilisées par les e-mails de la série
_ref = set()
for f in OUT.glob("*.html"): _ref |= set(re.findall(r"\[URL_IMAGES\]/([a-z0-9-]+\.(?:jpg|png))", f.read_text()))
for f in (OUT / "img").iterdir():
    if f.name not in _ref: f.unlink()
