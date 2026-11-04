#!/usr/bin/env python3
"""Version e-mail d'une miniature YouTube : 1072 × 603 px (le double des 536 px affichés dans l'e-mail), bouton lecture au centre, JPEG léger (≈ 100 Ko).
Le bouton est incrusté dans l'image : il s'affiche partout, Outlook compris (les superpositions en HTML n'y marchent pas).
Usage : python3 scripts/miniature-mail.py miniature-youtube.jpg|png sortie.jpg   (plusieurs paires possibles)"""
import sys
from PIL import Image, ImageDraw

def bouton(d):   # disque blanc légèrement translucide, triangle nuit, ombre douce
    n = 4; t = d * n; im = Image.new("RGBA", (t, t), (0, 0, 0, 0)); g = ImageDraw.Draw(im)
    g.ellipse((0, 0, t - 1, t - 1), fill=(255, 255, 255, 238)); r = t / 2
    g.polygon([(r - t * .13, r - t * .2), (r - t * .13, r + t * .2), (r + t * .22, r)], fill=(15, 20, 32, 255))
    return im.resize((d, d), Image.LANCZOS)

def miniature_mail(src, dst, largeur=1072):
    im = Image.open(src).convert("RGB")
    w, h = im.size; hh = round(largeur * 9 / 16)
    if abs(w / h - 16 / 9) > .01:   # recadre au 16:9 si besoin, au centre
        if w / h > 16 / 9: nw = round(h * 16 / 9); im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else: nh = round(w * 9 / 16); im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
    im = im.resize((largeur, hh), Image.LANCZOS)
    ombre = Image.new("RGBA", im.size, (0, 0, 0, 0)); d = round(largeur * .14)
    ImageDraw.Draw(ombre).ellipse(((largeur - d) // 2 - 6, (hh - d) // 2 - 2, (largeur + d) // 2 + 6, (hh + d) // 2 + 10), fill=(0, 0, 0, 70))
    im = Image.alpha_composite(im.convert("RGBA"), ombre)
    b = bouton(d); im.alpha_composite(b, ((largeur - d) // 2, (hh - d) // 2))
    im.convert("RGB").save(dst, quality=82, optimize=True, progressive=True)

if __name__ == "__main__":
    a = sys.argv[1:]
    for i in range(0, len(a), 2): miniature_mail(a[i], a[i + 1]); print("écrit", a[i + 1])
