"""Génère les SVG animés de la mascotte echecs.com pour le site.

La mascotte est reconstruite à partir de l'animation « hello » du designer
(video/assets/mascot/hello.json) : un corps et un bras articulé à l'épaule.
Chaque animation est un SVG autonome animé en CSS (aucun script) :
- une intro jouée une fois (animation-fill-mode: both), puis une boucle ;
- couleur de la mascotte : variable CSS --mascot (défaut #1b1b1b), modifiable
  quand le SVG est intégré en ligne dans la page.

Usage : python3 site-animations/generate.py
Sorties : site-animations/svg/mascotte-*.svg, site-animations/index.html,
          video/assets/mascot/poses.js (réutilisé dans la vidéo).
"""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "site-animations")
LOTTIE = os.path.join(ROOT, "video", "assets", "mascot", "hello.json")

YELLOW, BLUE, GREEN, PINK, INK = "#fae361", "#93b9e2", "#6bdc7d", "#f06b8a", "#1b1b1b"
LINE = "var(--line)"  # traits et accessoires sombres (défaut #1b1b1b)
EASE_BACK = "cubic-bezier(.34,1.56,.64,1)"
EASE_OUT = "cubic-bezier(.16,1,.3,1)"
EASE_IN = "cubic-bezier(.7,0,.84,0)"
EASE_IO = "cubic-bezier(.65,0,.35,1)"
UP, DOWN, SOFT = "cubic-bezier(.33,1,.68,1)", "cubic-bezier(.32,0,.67,0)", "cubic-bezier(.45,0,.55,1)"


def jump(h, sq=1.07):
    """Keyframes d'un saut qui boucle sans à-coup (à utiliser avec un timing linéaire)."""
    return (f"0%{{transform:translateY(0) scale(1,1);animation-timing-function:{SOFT}}} "
            f"16%{{transform:translateY(0) scale({sq},{2 - sq - .04:.2f});animation-timing-function:{UP}}} "
            f"42%{{transform:translateY(-{h}px) scale(.97,1.04);animation-timing-function:{DOWN}}} "
            f"62%{{transform:translateY(0) scale({sq + .01:.2f},{2 - sq - .05:.2f});animation-timing-function:{UP}}} "
            f"76%{{transform:translateY(0) scale(.98,1.02);animation-timing-function:{SOFT}}} "
            f"90%,100%{{transform:translateY(0) scale(1,1)}}")


# ---------------------------------------------------------------- géométrie
def lottie_paths():
    d = json.load(open(LOTTIE))
    L = {l["ind"]: l for l in d["layers"]}

    def path(sh, off):
        v, i, o, c = sh["v"], sh["i"], sh["o"], sh["c"]
        P = lambda p: f"{p[0] + off[0]:.1f},{p[1] + off[1]:.1f}"
        s, n = "M" + P(v[0]), len(v)
        for k in range(n if c else n - 1):
            a, b = v[k], v[(k + 1) % n]
            s += f" C{P((a[0] + o[k][0], a[1] + o[k][1]))} {P((b[0] + i[(k + 1) % n][0], b[1] + i[(k + 1) % n][1]))} {P(b)}"
        return s + (" Z" if c else "")

    x = L[1]["ks"]["p"]["k"]            # null X : position des pieds
    body_off = (L[4]["ks"]["p"]["k"][0] + x[0] - 50, L[4]["ks"]["p"]["k"][1] + x[1] - 50)
    arm_l = L[3]["ks"]
    pivot = (arm_l["p"]["k"][0] + x[0] - 50, arm_l["p"]["k"][1] + x[1] - 50)
    arm_off = (-arm_l["a"]["k"][0], -arm_l["a"]["k"][1])
    body = " ".join(path(it["ks"]["k"], body_off) for it in L[4]["shapes"][0]["it"] if it["ty"] == "sh")
    arm = [path(it["ks"]["k"], arm_off) for it in L[3]["shapes"][0]["it"] if it["ty"] == "sh"][0]
    return body, arm, pivot, (x[0], x[1])


BODY, ARM, PIVOT, FEET = lottie_paths()
FIST = (-324, -413)        # centre du poing, repère de l'épaule, bras à 0°
HEAD_TOP = (722, 58)
VB = "-40 -330 1160 1420"   # marge au-dessus de la tête pour les accessoires


# ---------------------------------------------------------------- accessoires
def star(r=60, color=YELLOW):
    import math
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * .46
        pts.append(f"{rr * math.cos(a):.1f},{rr * math.sin(a):.1f}")
    return f'<polygon points="{" ".join(pts)}" fill="{color}" stroke="{LINE}" stroke-width="10" stroke-linejoin="round"/>'


def sparkle(s=1, color=YELLOW):
    return f'<path transform="scale({s})" d="M0,-40 C4,-10 10,-4 40,0 C10,4 4,10 0,40 C-4,10 -10,4 -40,0 C-10,-4 -4,-10 0,-40Z" fill="{color}"/>'


CAP = f'''<g><path d="M-150,-10 L0,-70 L150,-10 L0,50 Z" fill="{LINE}"/>
<path d="M-85,15 L-85,70 C-40,100 40,100 85,70 L85,15 L0,50 Z" fill="{LINE}"/>
<path d="M0,-10 C60,0 110,20 118,60 L118,120" fill="none" stroke="{YELLOW}" stroke-width="12" stroke-linecap="round"/>
<circle cx="118" cy="132" r="20" fill="{YELLOW}"/></g>'''

TROPHY = f'''<g><path d="M-95,-150 L95,-150 C95,-40 50,10 0,20 C-50,10 -95,-40 -95,-150 Z" fill="{YELLOW}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<path d="M-95,-125 C-160,-125 -160,-40 -70,-30 M95,-125 C160,-125 160,-40 70,-30" fill="none" stroke="{LINE}" stroke-width="14" stroke-linecap="round"/>
<rect x="-18" y="18" width="36" height="50" fill="{LINE}"/><rect x="-70" y="64" width="140" height="38" rx="8" fill="{LINE}"/>
<clipPath id="mascotte-trophy-cup"><path d="M-95,-150 L95,-150 C95,-40 50,10 0,20 C-50,10 -95,-40 -95,-150 Z"/></clipPath>
<g clip-path="url(#mascotte-trophy-cup)"><g class="shine"><rect x="-150" y="-170" width="40" height="220" fill="#fff" opacity=".7" transform="skewX(-18)"/></g></g></g>'''

CHECK = f'''<g><circle r="95" fill="{GREEN}" stroke="{LINE}" stroke-width="12"/>
<path class="tick" d="M-45,3 L-12,36 L48,-30" fill="none" stroke="{LINE}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="150" stroke-dashoffset="150"/></g>'''

CROSS = f'''<g><circle r="95" fill="{PINK}" stroke="{LINE}" stroke-width="12"/>
<path d="M-36,-36 L36,36 M36,-36 L-36,36" stroke="{LINE}" stroke-width="22" stroke-linecap="round"/></g>'''

CLOUD = f'''<g><path d="M-170,40 C-230,40 -230,-50 -160,-55 C-160,-130 -60,-150 -30,-90 C0,-160 120,-150 120,-70 C200,-80 220,40 150,40 Z" fill="{BLUE}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/></g>'''

RETRY = f'''<g><path d="M70,-50 A90,90 0 1 0 90,20" fill="none" stroke="{LINE}" stroke-width="24" stroke-linecap="round"/>
<path d="M40,-95 L100,-60 L45,-10 Z" fill="{LINE}" stroke="{LINE}" stroke-width="10" stroke-linejoin="round"/></g>'''

FLAME = f'''<g><path d="M0,40 C-80,40 -110,-30 -80,-90 C-70,-60 -50,-50 -40,-60 C-50,-130 0,-180 20,-230 C40,-160 110,-120 100,-40 C95,10 60,40 0,40 Z" fill="#ff8a3d" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<path d="M0,30 C-40,30 -55,-10 -40,-45 C-25,-30 -10,-30 -5,-45 C0,-80 20,-100 30,-120 C45,-80 70,-50 60,-10 C55,15 35,30 0,30 Z" fill="{YELLOW}"/></g>'''


BOOK = f'''<g><path d="M-125,-72 L0,-56 L125,-72 L125,82 L0,98 L-125,82 Z" fill="{BLUE}" stroke="{LINE}" stroke-width="10" stroke-linejoin="round"/>
<path d="M-112,-62 L-4,-47 L-4,86 L-112,71 Z" fill="#fff" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>
<path d="M112,-62 L4,-47 L4,86 L112,71 Z" fill="#fff" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/>
<path d="M-92,-30 L-24,-21 M-92,-2 L-24,7 M-92,26 L-40,33 M24,-21 L92,-30 M24,7 L92,-2 M24,33 L76,26" stroke="#b9c3cf" stroke-width="8" stroke-linecap="round"/>
<g class="pg"><path d="M4,-47 L112,-62 L112,71 L4,86 Z" fill="#f4f1ea" stroke="{LINE}" stroke-width="7" stroke-linejoin="round"/></g></g>'''

BULB = f'''<g><g class="rays">{"".join(f'<path d="M0,-150 L0,-190" transform="rotate({a})" stroke="{YELLOW}" stroke-width="16" stroke-linecap="round"/>' for a in range(-90, 91, 30))}</g>
<circle cy="-20" r="88" fill="{YELLOW}" stroke="{LINE}" stroke-width="12"/>
<path d="M-26,10 C-26,-30 26,-30 26,10 M0,-10 L0,62" fill="none" stroke="{LINE}" stroke-width="9" stroke-linecap="round"/>
<rect x="-44" y="60" width="88" height="56" rx="12" fill="{LINE}"/></g>'''


def g(origin, cls, inner):
    """Groupe animé dont l'origine de transformation est `origin` (repère du SVG)."""
    ox, oy = origin
    return f'<g transform="translate({ox:.1f} {oy:.1f})"><g class="{cls}">{inner}</g></g>'


def mascot(arm_inner="", head_inner=""):
    """Corps + bras articulé ; `arm_inner` est dessiné dans le repère de l'épaule."""
    fx, fy = FEET
    px, py = PIVOT
    arm = g(PIVOT, "arm", f'<path class="m" d="{ARM}"/>{arm_inner}')
    head = f'<g transform="translate({HEAD_TOP[0]} {HEAD_TOP[1]})">{head_inner}</g>' if head_inner else ""
    inner = (f'<g transform="translate({-fx:.1f} {-fy:.1f})"><path class="m" d="{BODY}" fill-rule="evenodd"/>'
             f'<circle class="m" cx="{px:.1f}" cy="{py:.1f}" r="46"/>{arm}{head}</g>')
    return g(FEET, "rig", inner)


def svg(name, title, css, body, shadow=True):
    sh = f'<ellipse class="shadow" cx="{FEET[0] - 40}" cy="{FEET[1] + 18}" rx="280" ry="26"/>' if shadow else ""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="{VB}" class="mascotte mascotte-{name}" role="img" aria-label="{title}">
<style>
.mascotte-{name} {{ --mascot: {INK}; --line: {INK}; }}
.mascotte-{name} .m {{ fill: var(--mascot); }}
.mascotte-{name} .shadow {{ fill: var(--mascot); opacity: .12; }}
.mascotte-{name} g {{ transform-box: view-box; transform-origin: 0 0; }}
{css}
@media (prefers-reduced-motion: reduce) {{ .mascotte-{name} * {{ animation: none !important; }} }}
</style>
{sh}{body}
</svg>'''


def css(name, rules):
    """rules : liste de (sélecteur, animation, keyframes) → CSS préfixé par l'animation."""
    out = []
    for sel, anim, frames in rules:
        out.append(f".mascotte-{name} {sel} {{ animation: {anim}; }}")
        for kname, kf in frames.items():
            out.append(f"@keyframes {kname} {{ {kf} }}")
    return "\n".join(out)


A = {}   # nom → (titre, usage, svg)

# 1. Leçon terminée : saut, la toque tombe sur la tête, étincelles --------------------
n = "lecon-terminee"
body = mascot(head_inner=g((10, -20), "cap", CAP)) + \
    "".join(g(p, f"sp sp{i}", sparkle(s)) for i, (p, s) in enumerate([((380, 120), 1.1), ((1010, 180), .8), ((320, 420), .7), ((1060, 470), 1)]))
A[n] = ("Leçon terminée", "Fin d'une leçon", svg(n, "Leçon terminée", css(n, [
    (".rig", f"{n}-jump 1.3s linear both, {n}-bob 2.4s ease-in-out 1.3s infinite", {
        f"{n}-jump": jump(150),
        f"{n}-bob": "0%,100%{transform:scale(1,1)} 50%{transform:translateY(-8px) scale(.99,1.01)}"}),
    (".arm", f"{n}-pump 1.3s {SOFT} both, {n}-wave .7s ease-in-out 1.3s infinite alternate", {
        f"{n}-pump": "0%{transform:rotate(-10deg)} 20%{transform:rotate(-24deg)} 45%{transform:rotate(22deg)} 70%{transform:rotate(-4deg)} 100%{transform:rotate(0)}",
        f"{n}-wave": "from{transform:rotate(0)} to{transform:rotate(-13deg)}"}),
    (".cap", f"{n}-cap 1.3s linear both, {n}-tilt 2.4s ease-in-out 1.3s infinite", {
        f"{n}-cap": (f"0%,30%{{transform:translateY(-420px) rotate(-40deg);opacity:0;animation-timing-function:{DOWN}}} "
                     f"34%{{opacity:1}} 62%{{transform:translateY(0) rotate(-14deg);animation-timing-function:{UP}}} "
                     f"74%{{transform:translateY(-36px) rotate(-8deg);animation-timing-function:{DOWN}}} "
                     f"86%,100%{{transform:translateY(0) rotate(-12deg);opacity:1}}"),
        f"{n}-tilt": "0%,100%{transform:rotate(-12deg)} 50%{transform:rotate(-8deg)}"}),
    (".sp", f"{n}-sp 2.4s {SOFT} .8s infinite backwards", {f"{n}-sp":
        "0%{transform:scale(0) rotate(-90deg)} 18%{transform:scale(1.1) rotate(0)} 36%{transform:scale(1) rotate(20deg)} 54%,100%{transform:scale(0) rotate(90deg)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .sp{i} {{ animation-delay: {.8 + i * .45:.2f}s; }}" for i in range(4)), body))

# 2. Série réussie : trois étoiles apparaissent, poing levé, confettis ----------------
n = "serie-reussie"
stars = "".join(g(p, f"st st{i}", star(r, YELLOW)) for i, (p, r) in enumerate([((420, -120), 85), ((730, -230), 110), ((1040, -120), 85)]))
conf = "".join(g((150 + (k * 97) % 900, -300), f"cf cf{k}", f'<rect x="-10" y="-16" width="20" height="32" rx="4" fill="{[YELLOW, BLUE, GREEN, PINK][k % 4]}"/>') for k in range(10))
body = conf + mascot() + stars
A[n] = ("Série réussie", "Série d'exercices réussie", svg(n, "Série réussie", css(n, [
    (".rig", f"{n}-hop 1.6s linear infinite", {f"{n}-hop": jump(90)}),
    (".arm", f"{n}-arm 1.6s {SOFT} infinite", {f"{n}-arm":
        "0%,100%{transform:rotate(-6deg)} 16%{transform:rotate(-14deg)} 42%{transform:rotate(24deg)} 62%{transform:rotate(4deg)}"}),
    (".st", f"{n}-star .6s {EASE_BACK} both, {n}-tw 1.6s ease-in-out .9s infinite", {
        f"{n}-star": "from{transform:scale(0) rotate(-180deg)} to{transform:scale(1) rotate(0)}",
        f"{n}-tw": "0%,100%{transform:scale(1) rotate(0)} 50%{transform:scale(1.1) rotate(8deg)}"}),
    (".cf", f"{n}-fall 2.4s linear infinite", {f"{n}-fall":
        "from{transform:translateY(0) rotate(0)} to{transform:translateY(1400px) rotate(720deg)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .st{i} {{ animation-delay: {.15 + i * .18:.2f}s, {.9 + i * .2:.2f}s; }}" for i in range(3))
  + "\n" + "\n".join(f".mascotte-{n} .cf{k} {{ animation-delay: -{(k * .37) % 2.4:.2f}s; animation-duration: {2.0 + (k % 3) * .35:.2f}s; }}" for k in range(10)), body))

# 3. Bonne réponse : geste « Yes ! », le poing ramené vers le bas, pastille cochée ----
n = "bonne-reponse"
body = mascot() + g((300, 30), "badge", CHECK)
A[n] = ("Bonne réponse", "Exercice réussi", svg(n, "Bonne réponse", css(n, [
    (".rig", f"{n}-spin 1.1s {SOFT} both, {n}-idle 2.4s ease-in-out 1.1s infinite", {
        f"{n}-spin": ("0%{transform:scale(1,1)} 12%{transform:scale(1.06,.92)} 28%{transform:translateY(-90px) scale(-1,1.04)} "
                      "44%{transform:translateY(-90px) scale(1,1.04)} 60%{transform:translateY(0) scale(1.07,.92)} 74%{transform:scale(.98,1.02)} 88%,100%{transform:scale(1,1)}"),
        f"{n}-idle": "0%,100%{transform:scale(1)} 50%{transform:translateY(-6px) scale(.99,1.01)}"}),
    (".arm", f"{n}-arm 1.1s {SOFT} both, {n}-wave .7s ease-in-out 1.1s infinite alternate", {
        f"{n}-arm": "0%{transform:rotate(-20deg)} 30%{transform:rotate(18deg)} 60%{transform:rotate(-50deg)} 100%{transform:rotate(-36deg)}",
        f"{n}-wave": "from{transform:rotate(-36deg)} to{transform:rotate(-26deg)}"}),
    (".badge", f"{n}-pop .5s {EASE_BACK} .35s both, {n}-pulse 2.4s ease-in-out 1s infinite", {
        f"{n}-pop": "from{transform:scale(0) rotate(-30deg)} to{transform:scale(1) rotate(0)}",
        f"{n}-pulse": "0%,100%{transform:scale(1)} 50%{transform:scale(1.06)}"}),
    (".tick", f"{n}-tick .4s ease-out .65s both", {f"{n}-tick": "to{stroke-dashoffset:0}"}),
]), body))

# 4. Mauvaise réponse : sursaut, le bras retombe, la mascotte secoue la tête ------------
n = "mauvaise-reponse"
qm = "".join(g(p, f"q q{i}", f'<text x="0" y="0" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="{s}" text-anchor="middle" fill="{LINE}">?</text>') for i, (p, s) in enumerate([((900, -40), 150), ((1030, 60), 110)]))
body = mascot() + g((300, 40), "badge", CROSS) + qm
A[n] = ("Mauvaise réponse", "Exercice raté", svg(n, "Mauvaise réponse", css(n, [
    (".rig", f"{n}-flinch .5s {UP} both, {n}-no 2.4s ease-in-out .5s infinite", {
        f"{n}-flinch": "0%{transform:scale(1)} 30%{transform:rotate(-6deg) scale(1.06,.9)} 70%{transform:rotate(2deg) scale(.98,1.02)} 100%{transform:rotate(0) scale(1)}",
        f"{n}-no": "0%,30%,100%{transform:rotate(0)} 5%{transform:rotate(-3deg)} 10%{transform:rotate(3deg)} 15%{transform:rotate(-2deg)} 20%{transform:rotate(1.5deg)} 25%{transform:rotate(0)}"}),
    (".arm", f"{n}-drop .5s {EASE_BACK} both, {n}-swing 1.2s ease-in-out .5s infinite alternate", {
        f"{n}-drop": "from{transform:rotate(0)} to{transform:rotate(-100deg)}",
        f"{n}-swing": "from{transform:rotate(-100deg)} to{transform:rotate(-90deg)}"}),
    (".badge", f"{n}-pop .4s {EASE_BACK} both, {n}-shake 2.4s ease-in-out .5s infinite", {
        f"{n}-pop": "from{transform:scale(0)} to{transform:scale(1)}",
        f"{n}-shake": "0%,40%,100%{transform:rotate(0)} 5%{transform:rotate(-14deg)} 10%{transform:rotate(12deg)} 15%{transform:rotate(-8deg)} 20%{transform:rotate(5deg)} 25%{transform:rotate(0)}"}),
    (".q", f"{n}-q 1.6s ease-in-out infinite backwards", {f"{n}-q":
        "0%{transform:translateY(20px) scale(.6);opacity:0} 30%{transform:translateY(0) scale(1);opacity:1} 70%{opacity:1} 100%{transform:translateY(-60px) scale(1.05);opacity:0}"}),
]) + f"\n.mascotte-{n} .q1 {{ animation-delay: .6s; }}", body))

# 5. Série ratée : épaules basses, petit nuage de pluie -----------------------------
n = "serie-ratee"
drops = "".join(g((x, 60), f"dr dr{i}", f'<path d="M0,-22 C12,-4 16,6 16,14 A16,16 0 0 1 -16,14 C-16,6 -12,-4 0,-22Z" fill="{BLUE}" stroke="{LINE}" stroke-width="7"/>') for i, x in enumerate([-120, -30, 60, 140]))
body = mascot() + g((740, -150), "cloud", CLOUD + drops)
A[n] = ("Série ratée", "Série d'exercices échouée", svg(n, "Série ratée", css(n, [
    (".rig", f"{n}-slump .8s {EASE_OUT} both, {n}-sigh 3s ease-in-out .8s infinite", {
        f"{n}-slump": "from{transform:scale(1) rotate(0)} to{transform:scale(1.03,.95) rotate(3deg)}",
        f"{n}-sigh": "0%,100%{transform:scale(1.03,.95) rotate(3deg)} 45%{transform:scale(1.01,.98) rotate(2deg)} 60%{transform:scale(1.04,.94) rotate(3.5deg)}"}),
    (".arm", f"{n}-drop .8s {EASE_OUT} both, {n}-swing 3s ease-in-out .8s infinite", {
        f"{n}-drop": "from{transform:rotate(0)} to{transform:rotate(-112deg)}",
        f"{n}-swing": "0%,100%{transform:rotate(-112deg)} 50%{transform:rotate(-106deg)}"}),
    (".cloud", f"{n}-cloud .6s {EASE_BACK} .3s both, {n}-float 3s ease-in-out .9s infinite", {
        f"{n}-cloud": "from{transform:translateY(-80px) scale(.3);opacity:0} to{transform:translateY(0) scale(1);opacity:1}",
        f"{n}-float": "0%,100%{transform:translateX(0)} 50%{transform:translateX(18px)}"}),
    (".dr", f"{n}-rain .9s {EASE_IN} infinite backwards", {f"{n}-rain":
        "0%{transform:translateY(0);opacity:0} 15%{opacity:1} 100%{transform:translateY(190px);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .dr{i} {{ animation-delay: {.9 + i * .23:.2f}s; }}" for i in range(4)), body))

# 7. Réflexion / chargement : main sur la tête, bulles de pensée --------------------
n = "reflexion"
dots = "".join(g((x, 0), f"dt dt{i}", f'<circle r="26" fill="{INK}"/>') for i, x in enumerate([-70, 0, 70]))
bubble = f'<circle cx="-200" cy="170" r="22" fill="#fff" stroke="{INK}" stroke-width="9"/><circle cx="-150" cy="110" r="34" fill="#fff" stroke="{INK}" stroke-width="9"/><ellipse rx="160" ry="95" fill="#fff" stroke="{INK}" stroke-width="10"/>' + dots
body = mascot() + g((930, -150), "bub", bubble)
A[n] = ("Réflexion", "Chargement, réflexion", svg(n, "Réflexion", css(n, [
    (".rig", f"{n}-sway 3s ease-in-out infinite", {f"{n}-sway": "0%,100%{transform:rotate(-1.5deg)} 50%{transform:rotate(1.5deg)}"}),
    (".arm", f"{n}-arm .6s {EASE_OUT} both, {n}-tap 1.5s ease-in-out .6s infinite", {
        f"{n}-arm": "from{transform:rotate(0)} to{transform:rotate(38deg)}",
        f"{n}-tap": "0%,100%{transform:rotate(38deg)} 50%{transform:rotate(33deg)}"}),
    (".bub", f"{n}-bub .5s {EASE_BACK} .3s both", {f"{n}-bub": "from{transform:scale(0);opacity:0} to{transform:scale(1);opacity:1}"}),
    (".dt", f"{n}-dot 1.2s ease-in-out infinite backwards", {f"{n}-dot": "0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-34px)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .dt{i} {{ animation-delay: {.8 + i * .18:.2f}s; }}" for i in range(3)), body))

# 8. Série de jours : la mascotte danse à côté de la flamme, le bras balance --------
n = "serie-de-jours"
body = g((960, 1020), "flame", FLAME) + mascot()
A[n] = ("Série de jours", "Série quotidienne, assiduité", svg(n, "Série de jours", css(n, [
    (".rig", f"{n}-dance 1.2s ease-in-out infinite", {f"{n}-dance":
        "0%,100%{transform:rotate(-4deg) scale(1.03,.96)} 25%{transform:translateY(-24px) rotate(0) scale(.99,1.02)} "
        "50%{transform:rotate(4deg) scale(1.03,.96)} 75%{transform:translateY(-24px) rotate(0) scale(.99,1.02)}"}),
    (".arm", f"{n}-swing 1.2s ease-in-out infinite", {f"{n}-swing":
        "0%,100%{transform:rotate(-104deg)} 50%{transform:rotate(-34deg)}"}),
    (".flame", f"{n}-pop .5s {EASE_BACK} both, {n}-flicker .3s ease-in-out .5s infinite alternate", {
        f"{n}-pop": "from{transform:scale(0)} to{transform:scale(1.2)}",
        f"{n}-flicker": "from{transform:scale(1.2,1.2) skewX(-4deg)} to{transform:scale(1.14,1.3) skewX(5deg)}"}),
]), body))

# 9. Victoire en tournoi : trophée brandi, reflet, confettis --------------------------
n = "victoire-tournoi"
trophy = g((FIST[0] + 10, FIST[1] - 60), "trophy", TROPHY)
conf = "".join(g((150 + (k * 113) % 950, -300), f"cf cf{k}", f'<rect x="-10" y="-16" width="20" height="32" rx="4" fill="{[YELLOW, BLUE, GREEN, PINK][k % 4]}"/>') for k in range(12))
body = conf + mascot(arm_inner=trophy)
A[n] = ("Victoire en tournoi", "Tournoi gagné, podium", svg(n, "Victoire en tournoi", css(n, [
    (".rig", f"{n}-hop 1.2s linear infinite", {f"{n}-hop": jump(70)}),
    (".arm", f"{n}-arm 1.2s {SOFT} infinite", {f"{n}-arm":
        "0%,100%{transform:rotate(6deg)} 16%{transform:rotate(2deg)} 42%{transform:rotate(22deg)} 62%{transform:rotate(8deg)}"}),
    (".trophy", f"{n}-trophy .6s {EASE_BACK} both", {f"{n}-trophy": "from{transform:scale(0) rotate(-40deg)} to{transform:scale(1) rotate(0)}"}),
    (".shine", f"{n}-shine 1.8s ease-in-out .6s infinite", {f"{n}-shine": "0%{transform:translateX(0)} 40%,100%{transform:translateX(300px)}"}),
    (".cf", f"{n}-fall 2.4s linear infinite", {f"{n}-fall": "from{transform:translateY(0) rotate(0)} to{transform:translateY(1400px) rotate(720deg)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .cf{k} {{ animation-delay: -{(k * .41) % 2.4:.2f}s; animation-duration: {2.0 + (k % 3) * .3:.2f}s; }}" for k in range(12)), body))

# 10. Regarde ! : bras tendu qui montre, pour l'onboarding -------------------------
n = "regarde"
body = mascot()
A[n] = ("Regarde !", "Onboarding, attirer l'attention", svg(n, "Regarde", css(n, [
    (".rig", f"{n}-lean .6s {EASE_OUT} both, {n}-bob 1.4s ease-in-out .6s infinite", {
        f"{n}-lean": "from{transform:rotate(0)} to{transform:rotate(-4deg)}",
        f"{n}-bob": "0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(-3deg) translateY(-10px)}"}),
    (".arm", f"{n}-point .6s {EASE_BACK} both, {n}-jab 1.4s ease-in-out .6s infinite", {
        f"{n}-point": "from{transform:rotate(0)} to{transform:rotate(-68deg)}",
        f"{n}-jab": "0%,100%{transform:rotate(-68deg)} 50%{transform:rotate(-62deg)}"}),
]), body))


# 11. Lecture : la mascotte lit un livre, les pages tournent -------------------------
n = "lecture"
body = mascot(arm_inner=g(FIST, "book", f'<g transform="rotate(22) scale(1.35)">{BOOK}</g>'))
A[n] = ("Lecture", "Leçon en cours, cours écrit", svg(n, "Lecture", css(n, [
    (".rig", f"{n}-read 2.4s ease-in-out infinite", {f"{n}-read":
        "0%,100%{transform:rotate(0) scale(1)} 50%{transform:rotate(-1.5deg) translateY(-6px) scale(.995,1.005)}"}),
    (".arm", f"{n}-hold .6s {EASE_BACK} both, {n}-bob 2.4s ease-in-out .6s infinite", {
        f"{n}-hold": "from{transform:rotate(-90deg)} to{transform:rotate(-22deg)}",
        f"{n}-bob": "0%,100%{transform:rotate(-22deg)} 50%{transform:rotate(-18deg)}"}),
    (".book", f"{n}-open .5s {EASE_BACK} .3s both", {f"{n}-open": "from{transform:scale(0)} to{transform:scale(1)}"}),
    (".pg", f"{n}-flip 2.4s {SOFT} .9s infinite backwards", {f"{n}-flip":
        "0%,45%{transform:scaleX(1)} 75%,100%{transform:scaleX(-1)}"}),
]), body))

# 12. Idée : une ampoule s'allume au-dessus de la tête ---------------------------------
n = "idee"
body = mascot() + g((720, -170), "bulb", f'<g transform="scale(1.35)">{BULB}</g>')
A[n] = ("Idée !", "Indice, astuce", svg(n, "Idée", css(n, [
    (".rig", f"{n}-hop .8s linear .15s both, {n}-idle 2.4s ease-in-out .95s infinite", {
        f"{n}-hop": jump(50),
        f"{n}-idle": "0%,100%{transform:scale(1)} 50%{transform:translateY(-6px) scale(.99,1.01)}"}),
    (".arm", f"{n}-arm 1.2s ease-in-out infinite alternate", {f"{n}-arm": "from{transform:rotate(-84deg)} to{transform:rotate(-76deg)}"}),
    (".bulb", f"{n}-pop .5s {EASE_BACK} .3s both, {n}-float 2.4s ease-in-out .8s infinite", {
        f"{n}-pop": "from{transform:scale(0) rotate(-20deg)} to{transform:scale(1) rotate(0)}",
        f"{n}-float": "0%,100%{transform:translateY(0)} 50%{transform:translateY(-14px)}"}),
    (".rays", f"{n}-glow .6s ease-in-out .8s infinite alternate backwards", {f"{n}-glow":
        "from{transform:scale(.85);opacity:.4} to{transform:scale(1.08);opacity:1}"}),
]), body))

# 13. Dodo : avachie, « Z z z » -------------------------------------------------------
n = "dodo"
zs = "".join(g(p, f"z z{i}", f'<text font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="{sz}" text-anchor="middle" fill="{LINE}">Z</text>') for i, (p, sz) in enumerate([((850, 0), 130), ((960, -120), 170), ((1060, -250), 210)]))
body = mascot() + zs
A[n] = ("Dodo", "Inactivité, « reviens vite »", svg(n, "Dodo", css(n, [
    (".rig", f"{n}-slump .8s {EASE_OUT} both, {n}-breathe 3s ease-in-out .8s infinite", {
        f"{n}-slump": "from{transform:rotate(0) scale(1)} to{transform:rotate(5deg) scale(1.03,.95)}",
        f"{n}-breathe": "0%,100%{transform:rotate(5deg) scale(1.03,.95)} 50%{transform:rotate(4deg) scale(1.01,.98)}"}),
    (".arm", f"{n}-drop .8s {EASE_OUT} both, {n}-sway 3s ease-in-out .8s infinite", {
        f"{n}-drop": "from{transform:rotate(0)} to{transform:rotate(-120deg)}",
        f"{n}-sway": "0%,100%{transform:rotate(-120deg)} 50%{transform:rotate(-116deg)}"}),
    (".z", f"{n}-z 2.4s ease-in-out infinite backwards", {f"{n}-z":
        "0%{transform:translate(0,30px) scale(.5);opacity:0} 25%{opacity:1} 100%{transform:translate(50px,-90px) scale(1);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .z{i} {{ animation-delay: {.8 + i * .8:.1f}s; }}" for i in range(3)), body))

# 14. Niveau supérieur : la mascotte gravit un escalier sans fin -----------------------
n = "niveau-superieur"
W_, H_ = 380, 150
pts = []
for k in range(4, -4, -1):
    x0, y0 = 400 - W_ * k, 1038 - H_ * k
    pts += [(x0, y0), (x0 + W_, y0)]
stair = "M" + " L".join(f"{x},{y}" for x, y in pts)
stairs = g((0, 0), "stairs", f'<path d="{stair}" fill="none" stroke="{LINE}" stroke-width="20" stroke-linejoin="round" stroke-linecap="round"/>'
           + "".join(f'<path d="M{400 - W_ * k + W_},{1038 - H_ * k} L{400 - W_ * k + W_},{1038 - H_ * k + H_}" stroke="{LINE}" stroke-width="16"/>' for k in range(0)))
arrows = "".join(g((1010, 300 + i * 150), f"up up{i}", f'<path d="M-40,20 L0,-20 L40,20" fill="none" stroke="{GREEN}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>') for i in range(3))
body = f'<g transform="translate(0 -250)">{stairs}{mascot()}</g>' + arrows
A[n] = ("Niveau supérieur", "Progression, nouveau niveau", svg(n, "Niveau supérieur", css(n, [
    (".rig", f"{n}-hop 1.4s linear infinite", {f"{n}-hop": jump(170)}),
    (".stairs", f"{n}-steps 1.4s linear infinite", {f"{n}-steps":
        f"0%,16%{{transform:translate(0,0);animation-timing-function:{SOFT}}} 62%,100%{{transform:translate({W_}px,{H_}px)}}"}),
    (".arm", f"{n}-bal 1.4s {SOFT} infinite", {f"{n}-bal":
        "0%,100%{transform:rotate(-40deg)} 16%{transform:rotate(-58deg)} 42%{transform:rotate(-12deg)} 62%{transform:rotate(-50deg)}"}),
    (".up", f"{n}-up 1.4s linear infinite backwards", {f"{n}-up":
        "0%{transform:translateY(60px);opacity:0} 30%{opacity:1} 100%{transform:translateY(-120px);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .up{i} {{ animation-delay: {i * .45:.2f}s; }}" for i in range(3)), body, shadow=False))


# ================================================================ nouvelles poses
# Accessoires tenus dans le poing (repère du bras : FIST = centre du poing à 0°)
PAWN = f'''<g><path d="M-48,-112 C-48,-88 -22,-80 -30,-60 C-48,-22 -74,0 -78,30 L78,30 C74,0 48,-22 30,-60 C22,-80 48,-88 48,-112 Z" fill="#fff" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<circle cy="-158" r="50" fill="#fff" stroke="{LINE}" stroke-width="12"/><rect x="-98" y="24" width="196" height="42" rx="14" fill="#fff" stroke="{LINE}" stroke-width="12"/>
<path d="M-24,-176 C-18,-192 -6,-198 6,-200" fill="none" stroke="{BLUE}" stroke-width="10" stroke-linecap="round"/></g>'''

LOUPE = f'''<g><rect x="-22" y="-120" width="44" height="150" rx="18" fill="{LINE}"/>
<circle cy="-230" r="110" fill="{BLUE}" fill-opacity=".45" stroke="{LINE}" stroke-width="22"/>
<path class="glint" d="M-60,-270 C-48,-300 -22,-318 8,-322" fill="none" stroke="#fff" stroke-width="16" stroke-linecap="round"/></g>'''

MEGA = f'''<g><path d="M-10,-40 L-250,-150 L-250,150 L-10,40 Z" fill="{YELLOW}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<rect x="-30" y="-48" width="60" height="96" rx="16" fill="{LINE}"/><ellipse cx="-250" rx="34" ry="150" fill="{PINK}" stroke="{LINE}" stroke-width="12"/>
<g class="waves">{"".join(f'<path class="wv wv{i}" d="M{-320 - i * 60},-{70 + i * 40} C{-360 - i * 70},-{30 + i * 20} {-360 - i * 70},{30 + i * 20} {-320 - i * 60},{70 + i * 40}" fill="none" stroke="{LINE}" stroke-width="14" stroke-linecap="round"/>' for i in range(3))}</g></g>'''

PHONE = f'''<g><rect x="-95" y="-330" width="190" height="320" rx="34" fill="{LINE}"/>
<rect x="-76" y="-300" width="152" height="250" rx="16" fill="#e4ecf6"/>
{"".join(f'<rect x="{-76 + (k % 4) * 38}" y="{-260 + (k // 4) * 38}" width="38" height="38" fill="{BLUE}"/>' for k in range(16) if (k + k // 4) % 2 == 0)}
<g class="notif"><circle cx="90" cy="-320" r="46" fill="{PINK}" stroke="{LINE}" stroke-width="10"/><path d="M90,-340 L90,-300" stroke="#fff" stroke-width="14" stroke-linecap="round"/></g></g>'''

HALTERE = f'''<g><rect x="-230" y="-18" width="460" height="36" rx="12" fill="{LINE}"/>
<rect x="-250" y="-90" width="60" height="180" rx="16" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/><rect x="-200" y="-65" width="40" height="130" rx="12" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/>
<rect x="190" y="-90" width="60" height="180" rx="16" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/><rect x="160" y="-65" width="40" height="130" rx="12" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/></g>'''

DRAPEAU = f'''<g><rect x="-12" y="-470" width="24" height="520" rx="12" fill="{LINE}"/><circle cy="-480" r="24" fill="{YELLOW}" stroke="{LINE}" stroke-width="8"/>
<g transform="translate(12 -450)"><g class="flag"><path d="M0,0 L300,0 L300,210 L0,210 Z" fill="#fff" stroke="{INK}" stroke-width="10"/>
{"".join(f'<rect x="{(k % 6) * 50}" y="{(k // 6) * 52.5}" width="50" height="52.5" fill="{INK}"/>' for k in range(24) if (k + k // 6) % 2 == 0)}</g></g></g>'''

PENDULE = f'''<g><rect x="-230" y="-150" width="460" height="190" rx="26" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/>
<circle cx="-110" cy="-55" r="62" fill="#fff" stroke="{LINE}" stroke-width="10"/><circle cx="110" cy="-55" r="62" fill="#fff" stroke="{LINE}" stroke-width="10"/>
<g transform="translate(-110 -55)"><path class="aig1" d="M0,0 L0,-46" stroke="{LINE}" stroke-width="10" stroke-linecap="round"/></g>
<g transform="translate(110 -55)"><path class="aig2" d="M0,0 L0,-46" stroke="{LINE}" stroke-width="10" stroke-linecap="round"/></g>
<g transform="translate(-110 -150)"><g class="btn1"><rect x="-50" y="-36" width="100" height="40" rx="12" fill="{YELLOW}" stroke="{LINE}" stroke-width="10"/></g></g>
<rect x="60" y="-178" width="100" height="32" rx="12" fill="{YELLOW}" stroke="{LINE}" stroke-width="10"/></g>'''

HEART = lambda c=PINK: f'<path d="M0,40 C-150,-50 -110,-170 -40,-150 C-15,-143 0,-120 0,-110 C0,-120 15,-143 40,-150 C110,-170 150,-50 0,40 Z" fill="{c}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>'

BULLE = f'''<g><path d="M-190,-110 C-190,-170 -150,-200 -90,-200 L150,-200 C200,-200 230,-170 230,-110 L230,0 C230,50 200,80 150,80 L-60,80 L-150,150 L-130,80 C-170,80 -190,50 -190,0 Z" fill="#fff" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<path class="l1" d="M-130,-120 L160,-120" stroke="{BLUE}" stroke-width="26" stroke-linecap="round"/><path class="l2" d="M-130,-50 L110,-50" stroke="{BLUE}" stroke-width="26" stroke-linecap="round"/><path class="l3" d="M-130,15 L40,15" stroke="{YELLOW}" stroke-width="26" stroke-linecap="round"/></g>'''

# 15. Coucou : grand signe de la main, petits traits de mouvement -------------------
n = "coucou"
traits = g(FIST, "tr", f'<path d="M-150,-60 C-170,-10 -170,40 -150,80 M-210,-90 C-240,-20 -240,60 -210,110" fill="none" stroke="{LINE}" stroke-width="14" stroke-linecap="round"/>')
body = mascot(arm_inner=traits)
A[n] = ("Coucou !", "Accueil, bonjour, bienvenue", svg(n, "Coucou", css(n, [
    (".rig", f"{n}-pop .6s {EASE_BACK} both, {n}-sway 1.6s ease-in-out .6s infinite", {
        f"{n}-pop": "from{transform:translateY(60px) scale(.9,1.08);opacity:0} to{transform:translateY(0) scale(1);opacity:1}",
        f"{n}-sway": "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(2deg) translateY(-6px)}"}),
    (".arm", f"{n}-wave .4s ease-in-out .3s infinite alternate", {f"{n}-wave": "from{transform:rotate(-24deg)} to{transform:rotate(14deg)}"}),
    (".tr", f"{n}-tr .4s ease-in-out .3s infinite alternate", {f"{n}-tr": "from{opacity:.2} to{opacity:1}"}),
]), body))

# 16. Course : penchée en avant, le bras pompe, traits de vitesse et poussière -------
n = "course"
vites = "".join(g((900 + i * 40, 300 + i * 190), f"vl vl{i}", f'<path d="M0,0 L{220 - i * 40},0" stroke="{LINE}" stroke-width="16" stroke-linecap="round"/>') for i in range(3))
poussiere = "".join(g((780 + i * 90, 1010), f"pu pu{i}", f'<circle r="{34 - i * 8}" fill="{LINE}" opacity=".18"/>') for i in range(3))
body = vites + poussiere + mascot()
A[n] = ("Course", "Défi chronométré, « vite ! », progression rapide", svg(n, "Course", css(n, [
    (".rig", f"{n}-run .44s ease-in-out infinite", {f"{n}-run":
        "0%,100%{transform:rotate(-9deg) translateY(0) scale(1.03,.96)} 50%{transform:rotate(-11deg) translateY(-46px) scale(.98,1.03)}"}),
    (".arm", f"{n}-pump .44s ease-in-out infinite", {f"{n}-pump": "0%,100%{transform:rotate(-88deg)} 50%{transform:rotate(-8deg)}"}),
    (".vl", f"{n}-vl .44s linear infinite", {f"{n}-vl": "from{transform:translateX(-60px);opacity:1} to{transform:translateX(120px);opacity:0}"}),
    (".pu", f"{n}-pu .88s ease-out infinite", {f"{n}-pu": "from{transform:translate(0,0) scale(.4);opacity:1} to{transform:translate(160px,-40px) scale(1.6);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .vl{i} {{ animation-delay: -{i * .15:.2f}s; }} .mascotte-{n} .pu{i} {{ animation-delay: -{i * .29:.2f}s; }}" for i in range(3)), body, shadow=True))

# 17. Salto : saut périlleux complet, étoiles à l'atterrissage ----------------------
n = "salto"
body = g((580, 560), "flip", f'<g transform="translate(-580 -560)">{mascot()}</g>') + \
    "".join(g(p, f"sp sp{i}", sparkle(s)) for i, (p, s) in enumerate([((300, 900), .9), ((960, 860), 1.1)]))
A[n] = ("Salto", "Grande victoire, record battu", svg(n, "Salto", css(n, [
    (".rig", f"{n}-jump 1.8s linear infinite", {f"{n}-jump": jump(320, 1.1)}),
    (".flip", f"{n}-flip 1.8s infinite", {f"{n}-flip":
        f"0%,22%{{transform:rotate(0);animation-timing-function:{EASE_IO}}} 58%,100%{{transform:rotate(-360deg)}}"}),
    (".arm", f"{n}-arm 1.8s {SOFT} infinite", {f"{n}-arm": "0%,100%{transform:rotate(0)} 20%{transform:rotate(-30deg)} 40%{transform:rotate(20deg)} 70%{transform:rotate(-10deg)}"}),
    (".sp", f"{n}-sp 1.8s {SOFT} infinite", {f"{n}-sp":
        "0%,58%{transform:scale(0) rotate(-90deg)} 68%{transform:scale(1.1) rotate(0)} 85%,100%{transform:scale(0) rotate(90deg)}"}),
]), body))

# 18. Surgit : la mascotte surgit du bas, salue, puis redescend (coin d'écran) ------
n = "surgit"
body = f'<clipPath id="mascotte-surgit-clip"><rect x="-40" y="-330" width="1160" height="1390"/></clipPath><g clip-path="url(#mascotte-surgit-clip)">{mascot()}</g>'
A[n] = ("Surgit", "Coin d'écran, astuce discrète, « je suis là »", svg(n, "Surgit", css(n, [
    (".rig", f"{n}-peek 4s infinite", {f"{n}-peek":
        f"0%{{transform:translateY(1000px);animation-timing-function:{EASE_BACK}}} 18%,70%{{transform:translateY(0)}} "
        f"74%{{transform:translateY(-30px);animation-timing-function:{EASE_IN}}} 90%,100%{{transform:translateY(1000px)}}"}),
    (".arm", f"{n}-wave 4s ease-in-out infinite", {f"{n}-wave":
        "0%,20%{transform:rotate(-90deg)} 28%{transform:rotate(-10deg)} 34%{transform:rotate(16deg)} 40%{transform:rotate(-14deg)} 46%{transform:rotate(16deg)} 52%,70%{transform:rotate(0)} 80%,100%{transform:rotate(-90deg)}"}),
]), body, shadow=False))

# 19. Pion brandi : la mascotte brandit un grand pion ------------------------------
n = "pion-brandi"
body = mascot(arm_inner=g((FIST[0] + 10, FIST[1] - 40), "piece", f'<g transform="scale(1.25)">{PAWN}</g>'))
A[n] = ("Pion brandi", "Débutant, « ton premier coup », promotion", svg(n, "Pion brandi", css(n, [
    (".rig", f"{n}-hop 1.4s linear infinite", {f"{n}-hop": jump(60)}),
    (".arm", f"{n}-arm 1.4s {SOFT} infinite", {f"{n}-arm": "0%,100%{transform:rotate(8deg)} 16%{transform:rotate(2deg)} 42%{transform:rotate(20deg)} 62%{transform:rotate(10deg)}"}),
    (".piece", f"{n}-pop .6s {EASE_BACK} both, {n}-wob 1.4s ease-in-out .6s infinite", {
        f"{n}-pop": "from{transform:scale(0) rotate(-40deg)} to{transform:scale(1) rotate(0)}",
        f"{n}-wob": "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(8deg)}"}),
]), body))

# 20. Loupe : analyse une partie à la loupe, la loupe balaie ------------------------
n = "loupe"
body = mascot(arm_inner=g(FIST, "lp", LOUPE))
A[n] = ("Loupe", "Analyse de partie, recherche", svg(n, "Loupe", css(n, [
    (".rig", f"{n}-lean .6s {EASE_OUT} both, {n}-peer 2.4s ease-in-out .6s infinite", {
        f"{n}-lean": "from{transform:rotate(0)} to{transform:rotate(-4deg)}",
        f"{n}-peer": "0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(-1deg) translateY(-8px)}"}),
    (".arm", f"{n}-arm .6s {EASE_BACK} both, {n}-scan 2.4s ease-in-out .6s infinite", {
        f"{n}-arm": "from{transform:rotate(-100deg)} to{transform:rotate(-14deg)}",
        f"{n}-scan": "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(4deg)}"}),
    (".glint", f"{n}-glint 2.4s ease-in-out infinite", {f"{n}-glint": "0%,40%,100%{opacity:.2} 55%{opacity:1}"}),
]), body))

# 21. Mégaphone : annonce, ondes sonores --------------------------------------------
n = "megaphone"
body = mascot(arm_inner=g(FIST, "mg", f'<g transform="rotate(52) scale(.8)">{MEGA}</g>'))
A[n] = ("Mégaphone", "Annonce, nouveauté, nouveau numéro", svg(n, "Mégaphone", css(n, [
    (".rig", f"{n}-shout .5s {EASE_BACK} both, {n}-pulse .8s ease-in-out .5s infinite alternate", {
        f"{n}-shout": "from{transform:scale(1,1)} 50%{transform:scale(1.06,.92)} to{transform:scale(1)}",
        f"{n}-pulse": "from{transform:scale(1)} to{transform:scale(1.02,.98) translateY(4px)}"}),
    (".arm", f"{n}-arm .5s {EASE_BACK} both", {f"{n}-arm": "from{transform:rotate(-100deg)} to{transform:rotate(4deg)}"}),
    (".wv", f"{n}-wv 1.2s ease-out infinite backwards", {f"{n}-wv": "0%{opacity:0;transform:translateX(30px)} 30%{opacity:1} 100%{opacity:0;transform:translateX(-60px)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .wv{i} {{ animation-delay: {.5 + i * .2:.1f}s; }}" for i in range(3)), body))

# 22. Téléphone : joue sur son téléphone, notification ------------------------------
n = "telephone"
body = mascot(arm_inner=g(FIST, "ph", f'<g transform="rotate(18) translate(0 60)">{PHONE}</g>'))
A[n] = ("Téléphone", "Application mobile, notification, partie en ligne", svg(n, "Téléphone", css(n, [
    (".rig", f"{n}-idle 2.4s ease-in-out infinite", {f"{n}-idle": "0%,100%{transform:rotate(0)} 50%{transform:rotate(-2deg) translateY(-6px)}"}),
    (".arm", f"{n}-arm .6s {EASE_BACK} both, {n}-hold 2.4s ease-in-out .6s infinite", {
        f"{n}-arm": "from{transform:rotate(-110deg)} to{transform:rotate(-18deg)}",
        f"{n}-hold": "0%,100%{transform:rotate(-18deg)} 50%{transform:rotate(-14deg)}"}),
    (".notif", f"{n}-notif 2.4s {EASE_BACK} .8s infinite backwards", {f"{n}-notif":
        "0%{transform:scale(0)} 15%{transform:scale(1.2)} 25%,80%{transform:scale(1)} 100%{transform:scale(0)}"}),
]), body))

# 23. Haltère : s'entraîne, soulève une haltère -------------------------------------
n = "haltere"
body = mascot(arm_inner=g(FIST, "hl", f'<g transform="rotate(-38) scale(1.15)">{HALTERE}</g>'))
A[n] = ("Haltère", "Entraînement, exercices du jour", svg(n, "Haltère", css(n, [
    (".rig", f"{n}-push 1.2s ease-in-out infinite", {f"{n}-push":
        "0%,100%{transform:scale(1.03,.96)} 50%{transform:translateY(-10px) scale(.99,1.02)}"}),
    (".arm", f"{n}-curl 1.2s ease-in-out infinite", {f"{n}-curl": "0%,100%{transform:rotate(-30deg)} 50%{transform:rotate(16deg)}"}),
]), body))

# 24. Drapeau à damier : objectif atteint, ligne d'arrivée -------------------------
n = "drapeau"
body = mascot(arm_inner=g(FIST, "dp", DRAPEAU))
A[n] = ("Drapeau à damier", "Objectif atteint, fin de parcours", svg(n, "Drapeau", css(n, [
    (".rig", f"{n}-hop 1.2s linear infinite", {f"{n}-hop": jump(50)}),
    (".arm", f"{n}-wave 1.2s ease-in-out infinite", {f"{n}-wave": "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(18deg)}"}),
    (".flag", f"{n}-flag .6s ease-in-out infinite alternate", {f"{n}-flag": "from{transform:skewY(-6deg) scaleX(1)} to{transform:skewY(6deg) scaleX(.94)}"}),
]), body))

# 25. Pendule : tape la pendule d'échecs, les aiguilles tournent --------------------
n = "pendule"
body = mascot() + g((230, 1030), "clock", f'<g transform="scale(.8)">{PENDULE}</g>')
A[n] = ("Pendule", "Blitz, tournoi, cadence", svg(n, "Pendule", css(n, [
    (".rig", f"{n}-lean .3s ease-in-out infinite alternate", {f"{n}-lean": "from{transform:rotate(-3deg)} to{transform:rotate(-6deg) scale(1.02,.98)}"}),
    (".arm", f"{n}-tap .6s ease-in-out infinite", {f"{n}-tap": "0%,100%{transform:rotate(-78deg)} 45%{transform:rotate(-88deg)}"}),
    (".btn1", f"{n}-btn .6s ease-in-out infinite", {f"{n}-btn": "0%,30%,100%{transform:translateY(0)} 45%{transform:translateY(18px)}"}),
    (".aig1", f"{n}-a1 1.2s steps(12) infinite", {f"{n}-a1": "from{transform:rotate(0)} to{transform:rotate(360deg)}"}),
    (".aig2", f"{n}-a2 4.8s steps(12) infinite", {f"{n}-a2": "from{transform:rotate(0)} to{transform:rotate(360deg)}"}),
]), body))

# 26. Discussion : bulle de chat, la mascotte parle avec la main ---------------------
n = "discussion"
body = mascot() + g((860, -110), "bl", BULLE)
A[n] = ("Discussion", "Forum, commentaires, communauté", svg(n, "Discussion", css(n, [
    (".rig", f"{n}-talk 1.6s ease-in-out infinite", {f"{n}-talk": "0%,100%{transform:rotate(0)} 25%{transform:rotate(2deg) translateY(-8px)} 75%{transform:rotate(-2deg)}"}),
    (".arm", f"{n}-gest .8s ease-in-out infinite alternate", {f"{n}-gest": "from{transform:rotate(-64deg)} to{transform:rotate(-30deg)}"}),
    (".bl", f"{n}-pop .5s {EASE_BACK} .2s both, {n}-float 2.4s ease-in-out .7s infinite", {
        f"{n}-pop": "from{transform:scale(0);opacity:0} to{transform:scale(1);opacity:1}",
        f"{n}-float": "0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)}"}),
    (".l1,.l2,.l3", f"{n}-type 2.4s ease-out .5s infinite backwards", {f"{n}-type": "0%{stroke-dasharray:0 400} 40%,100%{stroke-dasharray:400 0}"}),
]) + f"\n.mascotte-{n} .l2 {{ animation-delay: .8s; }} .mascotte-{n} .l3 {{ animation-delay: 1.1s; }}", body))

# 27. Cœur : merci, cœurs qui s'envolent -------------------------------------------
n = "coeur"
coeurs = "".join(g(p, f"hc hc{i}", f'<g transform="scale({s})">{HEART([PINK, YELLOW, PINK][i])}</g>') for i, (p, s) in enumerate([((300, 300), .8), ((200, 120), .55), ((420, 60), .5)]))
body = mascot(arm_inner=g((FIST[0], FIST[1] - 40), "hm", f'<g transform="scale(1.1)">{HEART()}</g>')) + coeurs
A[n] = ("Cœur", "Merci, communauté, Saint-Valentin", svg(n, "Cœur", css(n, [
    (".rig", f"{n}-sway 2s ease-in-out infinite", {f"{n}-sway": "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(2deg) translateY(-8px)}"}),
    (".arm", f"{n}-arm .6s {EASE_BACK} both, {n}-hold 2s ease-in-out .6s infinite", {
        f"{n}-arm": "from{transform:rotate(-90deg)} to{transform:rotate(-2deg)}",
        f"{n}-hold": "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(-8deg)}"}),
    (".hm", f"{n}-beat .8s ease-in-out infinite", {f"{n}-beat": "0%,100%{transform:scale(1)} 15%{transform:scale(1.18)} 30%{transform:scale(.96)} 45%{transform:scale(1.1)}"}),
    (".hc", f"{n}-fly 2.4s ease-out infinite backwards", {f"{n}-fly": "0%{transform:translate(0,40px) scale(.3);opacity:0} 20%{opacity:1} 100%{transform:translate(-60px,-260px) scale(1);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .hc{i} {{ animation-delay: {.4 + i * .7:.1f}s; }}" for i in range(3)), body))



# ---------------------------------------------------------------- deuxième lot
PARTY_HAT = f'''<g><path d="M-90,30 L0,-230 L90,30 Z" fill="{PINK}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<path d="M-62,-50 L58,-50 M-34,-130 L30,-130" stroke="{YELLOW}" stroke-width="20" stroke-linecap="round"/><circle cy="-240" r="30" fill="{YELLOW}" stroke="{LINE}" stroke-width="10"/></g>'''
BONNET = f'''<g><path d="M-120,10 C-120,-130 120,-130 120,10 Z" fill="{PINK}" stroke="{LINE}" stroke-width="12"/>
<rect x="-135" y="-10" width="270" height="60" rx="30" fill="#fff" stroke="{LINE}" stroke-width="12"/><circle cy="-120" r="44" fill="#fff" stroke="{LINE}" stroke-width="12"/></g>'''
CUP = f'''<g><path d="M-80,-170 L80,-170 L64,-20 C60,10 -60,10 -64,-20 Z" fill="#fff" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<path d="M78,-140 C140,-140 140,-60 70,-60" fill="none" stroke="{LINE}" stroke-width="14"/><rect x="-80" y="-120" width="160" height="30" fill="{BLUE}"/>
<g class="steam">{"".join(f'<path class="st st{i}" d="M{x},-200 C{x - 24},-240 {x + 24},-270 {x},-320" fill="none" stroke="{LINE}" stroke-width="10" stroke-linecap="round" opacity=".6"/>' for i, x in enumerate([-36, 0, 36]))}</g></g>'''
UMBRELLA = f'''<g><path d="M0,0 L0,-360" stroke="{LINE}" stroke-width="18" stroke-linecap="round"/><path d="M0,0 C0,40 -50,40 -50,0" fill="none" stroke="{LINE}" stroke-width="18" stroke-linecap="round"/>
<path d="M-330,-330 C-300,-560 300,-560 330,-330 C280,-370 220,-370 165,-330 C110,-370 55,-370 0,-330 C-55,-370 -110,-370 -165,-330 C-220,-370 -280,-370 -330,-330 Z" fill="{BLUE}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/></g>'''
CAPE = f'<path d="M560,450 C700,520 900,700 1080,960 C980,940 900,990 820,960 C760,860 680,760 600,700 Z" fill="{PINK}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>'
DISCO = f'''<g><path d="M0,-200 L0,-90" stroke="{LINE}" stroke-width="8"/><circle r="90" fill="#cfd8e3" stroke="{LINE}" stroke-width="10"/>
{"".join(f'<path d="M{-90 + k * 30},{-80 if k in (0, 6) else -90} L{-90 + k * 30},{80 if k in (0, 6) else 90}" stroke="#8a97a8" stroke-width="5"/>' for k in range(1, 6))}
<path d="M-88,-30 L88,-30 M-88,30 L88,30" stroke="#8a97a8" stroke-width="5"/><rect x="-50" y="-60" width="26" height="26" fill="#fff"/><rect x="30" y="0" width="26" height="26" fill="{YELLOW}"/></g>'''
SMALL_PIECE = lambda c: f'<g transform="scale(.42)"><circle cy="-158" r="50" fill="{c}" stroke="{LINE}" stroke-width="16"/><path d="M-48,-112 C-48,-88 -22,-80 -30,-60 C-48,-22 -74,0 -78,30 L78,30 C74,0 48,-22 30,-60 C22,-80 48,-88 48,-112 Z" fill="{c}" stroke="{LINE}" stroke-width="16"/><rect x="-98" y="24" width="196" height="42" rx="14" fill="{c}" stroke="{LINE}" stroke-width="16"/></g>'
SNOW = lambda: f'<path d="M0,-26 L0,26 M-22,-13 L22,13 M-22,13 L22,-13" stroke="#fff" stroke-width="8" stroke-linecap="round"/>'

def zz(positions, cls="z"):
    return "".join(g(p, f"{cls} {cls}{i}", f'<text font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="{sz}" text-anchor="middle" fill="{LINE}">Z</text>') for i, (p, sz) in enumerate(positions))

# 28. S'assoupir : la tête tombe doucement, sursaut, et ça recommence --------------
n = "assoupie"
body = mascot() + zz([((900, 60), 120), ((990, -60), 150)])
A[n] = ("S'assoupir", "Pause trop longue, « tu es toujours là ? »", svg(n, "S'assoupir", css(n, [
    (".rig", f"{n}-nod 3.6s infinite", {f"{n}-nod":
        f"0%{{transform:rotate(0);animation-timing-function:{EASE_IO}}} 60%{{transform:rotate(7deg) scale(1.02,.97);animation-timing-function:{EASE_IN}}} "
        f"68%{{transform:rotate(9deg) scale(1.02,.97)}} 72%{{transform:rotate(-3deg) translateY(-30px) scale(.97,1.04);animation-timing-function:{EASE_OUT}}} 84%,100%{{transform:rotate(0)}}"}),
    (".arm", f"{n}-arm 3.6s ease-in-out infinite", {f"{n}-arm": "0%{transform:rotate(-104deg)} 60%,68%{transform:rotate(-118deg)} 72%{transform:rotate(-40deg)} 84%,100%{transform:rotate(-104deg)}"}),
    (".z", f"{n}-z 3.6s ease-out infinite", {f"{n}-z": "0%,20%{opacity:0;transform:translate(0,30px) scale(.5)} 40%{opacity:1} 66%{opacity:1;transform:translate(40px,-60px) scale(1)} 70%,100%{opacity:0;transform:translate(40px,-60px) scale(1)}"}),
]) + f"\n.mascotte-{n} .z1 {{ animation-delay: .3s; }}", body))

# 29. Sieste : couchée sur un oreiller, sous une couverture, « Z z z » ------------------
n = "sieste"
LIT = (-530, -350, .78)   # couchée sur le dos : décalage x, y et échelle, rotation de 90° autour des pieds (tête à droite)
OREILLER = f'<rect x="720" y="770" width="350" height="140" rx="64" fill="#fff" stroke="{LINE}" stroke-width="12"/>'
COUVERTURE = (f'<path d="M10,740 C200,690 500,690 720,760 L720,1010 L10,1010 Z" fill="{BLUE}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>'
              f'<path d="M10,820 C200,775 500,775 720,835 M10,900 C200,858 500,858 720,912" fill="none" stroke="#fff" stroke-width="12" opacity=".7"/>'
              f'<path d="M-40,1010 L1120,1010" stroke="{LINE}" stroke-width="12" stroke-linecap="round" opacity=".25"/>')
couchee = g(FEET, "lie", f'<g transform="translate({LIT[0]} {LIT[1]}) rotate(90) scale({LIT[2]}) translate({-FEET[0]:.1f} {-FEET[1]:.1f})">{mascot()}</g>')
body = OREILLER + couchee + COUVERTURE + zz([((880, 600), 100), ((960, 470), 130), ((1050, 320), 160)])
A[n] = ("Sieste", "Inactivité longue, mode nuit, « reviens vite »", svg(n, "Sieste", css(n, [
    (".rig", f"{n}-breathe 3s ease-in-out infinite", {f"{n}-breathe": "0%,100%{transform:scale(1,1)} 50%{transform:scale(1.05,1)}"}),
    (".arm", f"{n}-arm 3s ease-in-out infinite", {f"{n}-arm": "0%,100%{transform:rotate(12deg)} 50%{transform:rotate(16deg)}"}),
    (".z", f"{n}-z 3s ease-in-out infinite backwards", {f"{n}-z": "0%{transform:translate(0,30px) scale(.5);opacity:0} 25%{opacity:1} 100%{transform:translate(40px,-90px) scale(1);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .z{i} {{ animation-delay: {i:.0f}s; }}" for i in range(3)), body, shadow=False))

# 29 bis. S'endort : bâille, pique du nez, se couche, dort, puis se relève ------------
n = "s-endort"
tombe = g(FEET, "fall", f'<g transform="translate({-FEET[0]:.1f} {-FEET[1]:.1f})">{mascot()}</g>')
body = g((0, 0), "bed", OREILLER) + tombe + g((0, 0), "bed2", COUVERTURE) + zz([((880, 600), 100), ((960, 470), 130), ((1050, 320), 160)])
lying = f"translate({LIT[0]}px,{LIT[1]}px) rotate(90deg) scale({LIT[2]})"
A[n] = ("S'endort", "Fin de journée, inactivité, « à demain ! »", svg(n, "S'endort", css(n, [
    (".fall", f"{n}-fall 7s infinite", {f"{n}-fall":
        f"0%,30%{{transform:none;animation-timing-function:{EASE_IN}}} 40%,88%{{transform:{lying};animation-timing-function:{EASE_BACK}}} 96%,100%{{transform:none}}"}),
    (".rig", f"{n}-nod 7s infinite", {f"{n}-nod":
        "0%,4%{transform:none} 12%{transform:rotate(6deg) scale(1.02,.97)} 15%{transform:rotate(-2deg) translateY(-20px)} 20%{transform:none} "
        "26%{transform:rotate(8deg) scale(1.02,.96)} 30%{transform:rotate(9deg)} 40%{transform:none} 44%,86%{transform:none} 64%{transform:scale(1.05,1)} 96%{transform:translateY(-30px)} 100%{transform:none}"}),
    (".arm", f"{n}-arm 7s ease-in-out infinite", {f"{n}-arm":
        "0%{transform:rotate(-100deg)} 6%{transform:rotate(24deg)} 10%{transform:rotate(-100deg)} 30%{transform:rotate(-118deg)} 40%,88%{transform:rotate(12deg)} 96%{transform:rotate(10deg)} 100%{transform:rotate(-100deg)}"}),
    (".bed,.bed2", f"{n}-bed 7s infinite", {f"{n}-bed": "0%,32%{opacity:0;transform:translateY(40px)} 40%,88%{opacity:1;transform:none} 94%,100%{opacity:0;transform:translateY(40px)}"}),
    (".z", f"{n}-z 7s ease-out infinite", {f"{n}-z":
        "0%,44%{opacity:0;transform:translate(0,30px) scale(.5)} 54%{opacity:1} 70%{opacity:0;transform:translate(40px,-90px) scale(1)} 71%,100%{opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .z{i} {{ animation-delay: {i * .5:.1f}s; }}" for i in range(3)), body, shadow=False))

# 30. Disco : bras en l'air, puis en bas, boule à facettes --------------------------
n = "disco"
rays = "".join(g((300, -150), f"ray ray{i}", f'<path d="M0,0 L{["-260", "-120", "60"][i]},420" stroke="{[YELLOW, PINK, BLUE][i]}" stroke-width="14" stroke-linecap="round" opacity=".7"/>') for i in range(3))
body = rays + g((300, -150), "ball", DISCO) + mascot()
A[n] = ("Disco", "Fête, week-end, bonne humeur", svg(n, "Disco", css(n, [
    (".rig", f"{n}-hips .8s ease-in-out infinite", {f"{n}-hips":
        "0%,100%{transform:rotate(-5deg) scale(1.02,.97)} 50%{transform:rotate(5deg) translateY(-30px) scale(.98,1.03)}"}),
    (".arm", f"{n}-point 1.6s steps(1) infinite", {f"{n}-point": "0%{transform:rotate(22deg)} 50%{transform:rotate(-96deg)}"}),
    (".ball", f"{n}-spin 2s linear infinite", {f"{n}-spin": "from{transform:rotate(-8deg)} 50%{transform:rotate(8deg)} to{transform:rotate(-8deg)}"}),
    (".ray", f"{n}-ray .8s ease-in-out infinite alternate", {f"{n}-ray": "from{opacity:.15} to{opacity:1}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .ray{i} {{ animation-delay: -{i * .27:.2f}s; }}" for i in range(3)), body))

# 31. Étirement : s'étire vers le ciel, puis se relâche -----------------------------
n = "etirement"
body = mascot() + "".join(g(p, f"sp sp{i}", sparkle(.7)) for i, p in enumerate([(200, -60), (480, -160)]))
A[n] = ("Étirement", "Début de séance, échauffement, bonjour", svg(n, "Étirement", css(n, [
    (".rig", f"{n}-stretch 3s ease-in-out infinite", {f"{n}-stretch":
        "0%,100%{transform:scale(1,1)} 35%,55%{transform:scale(.95,1.1) rotate(-3deg)} 70%{transform:scale(1.05,.94)}"}),
    (".arm", f"{n}-arm 3s ease-in-out infinite", {f"{n}-arm": "0%,100%{transform:rotate(-100deg)} 35%,55%{transform:rotate(26deg)} 70%{transform:rotate(-90deg)}"}),
    (".sp", f"{n}-sp 3s ease-in-out infinite", {f"{n}-sp": "0%,30%,60%,100%{transform:scale(0)} 45%{transform:scale(1) rotate(45deg)}"}),
]), body))

# 32. Toupie : se retourne d'un côté puis de l'autre en sautillant ------------------
n = "toupie"
body = mascot()
A[n] = ("Toupie", "Changement, « et maintenant ? », transition", svg(n, "Toupie", css(n, [
    (".rig", f"{n}-turn 2.4s ease-in-out infinite", {f"{n}-turn":
        "0%,30%{transform:scale(1,1)} 40%{transform:translateY(-120px) scale(0,1.03)} 50%,80%{transform:scale(-1,1)} 90%{transform:translateY(-120px) scale(0,1.03)} 100%{transform:scale(1,1)}"}),
    (".arm", f"{n}-arm 1.2s ease-in-out infinite alternate", {f"{n}-arm": "from{transform:rotate(-10deg)} to{transform:rotate(14deg)}"}),
]), body))

# 33. Marche : traverse le cadre d'un pas décidé -----------------------------------
n = "marche"
body = mascot()
A[n] = ("Marche", "Parcours, « en route ! », prochaine étape", svg(n, "Marche", css(n, [
    (".rig", f"{n}-walk 4s linear infinite, {n}-step .5s ease-in-out infinite", {
        f"{n}-walk": "from{translate:200px 0} to{translate:-200px 0}",
        f"{n}-step": "0%,100%{transform:rotate(-3deg) translateY(0)} 50%{transform:rotate(2deg) translateY(-26px)}"}),
    (".arm", f"{n}-swing .5s ease-in-out infinite alternate", {f"{n}-swing": "from{transform:rotate(-110deg)} to{transform:rotate(-60deg)}"}),
]), body))

# 34. Fête : chapeau pointu, bras qui s'agite, confettis ----------------------------
n = "fete"
conf = "".join(g((150 + (k * 101) % 900, -300), f"cf cf{k}", f'<rect x="-10" y="-16" width="20" height="32" rx="4" fill="{[YELLOW, BLUE, GREEN, PINK][k % 4]}"/>') for k in range(12))
body = conf + mascot(head_inner=g((-10, 10), "hat", f'<g transform="rotate(-18)">{PARTY_HAT}</g>'))
A[n] = ("Fête", "Anniversaire de l'académie, cap franchi, fêtes", svg(n, "Fête", css(n, [
    (".rig", f"{n}-hop 1s linear infinite", {f"{n}-hop": jump(80)}),
    (".arm", f"{n}-wave .5s ease-in-out infinite alternate", {f"{n}-wave": "from{transform:rotate(-20deg)} to{transform:rotate(20deg)}"}),
    (".hat", f"{n}-hat .5s ease-in-out infinite alternate", {f"{n}-hat": "from{transform:rotate(-6deg)} to{transform:rotate(6deg)}"}),
    (".cf", f"{n}-fall 2.4s linear infinite", {f"{n}-fall": "from{transform:translateY(0) rotate(0)} to{transform:translateY(1400px) rotate(720deg)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .cf{k} {{ animation-delay: -{(k * .37) % 2.4:.2f}s; }}" for k in range(12)), body))

# 35. Jonglage : trois pions tournent au-dessus de la main ---------------------------
n = "jongle"
orbit = g((0, 0), "orb", "".join(g((160 * __import__("math").cos(a), 160 * __import__("math").sin(a)), f"pc pc{i}", SMALL_PIECE(["#fff", YELLOW, "#fff"][i])) for i, a in enumerate([0, 2.094, 4.189])))
body = mascot(arm_inner=g((FIST[0] + 20, FIST[1] - 260), "jg", orbit))
A[n] = ("Jonglage", "Astuces, multitâche, « à toi de jouer »", svg(n, "Jonglage", css(n, [
    (".rig", f"{n}-bob .6s ease-in-out infinite alternate", {f"{n}-bob": "from{transform:scale(1.02,.98)} to{transform:translateY(-10px) scale(.99,1.01)}"}),
    (".arm", f"{n}-toss .6s ease-in-out infinite alternate", {f"{n}-toss": "from{transform:rotate(-6deg)} to{transform:rotate(10deg)}"}),
    (".orb", f"{n}-orb 1.8s linear infinite", {f"{n}-orb": "from{transform:rotate(0)} to{transform:rotate(360deg)}"}),
    (".pc", f"{n}-pc 1.8s linear infinite", {f"{n}-pc": "from{transform:rotate(0)} to{transform:rotate(-360deg)}"}),
]), body))

# 36. Super-héros : cape au vent, poing levé ----------------------------------------
n = "super-heros"
speed = "".join(g((150 + i * 120, 1000 - i * 20), f"vl vl{i}", f'<path d="M0,0 L0,-{160 - i * 30}" stroke="{LINE}" stroke-width="14" stroke-linecap="round" opacity=".5"/>') for i in range(3))
body = g((600, 450), "cape", f'<g transform="translate(-600 -450)">{CAPE}</g>') + speed + mascot()
A[n] = ("Super-héros", "Super-progrès, record, défi relevé", svg(n, "Super-héros", css(n, [
    (".rig", f"{n}-pose .6s {EASE_BACK} both, {n}-hover 2s ease-in-out .6s infinite", {
        f"{n}-pose": "from{transform:translateY(80px) scale(.9,1.08)} to{transform:translateY(0) scale(1)}",
        f"{n}-hover": "0%,100%{transform:translateY(0)} 50%{transform:translateY(-24px)}"}),
    (".arm", f"{n}-arm .6s {EASE_BACK} both", {f"{n}-arm": "from{transform:rotate(-90deg)} to{transform:rotate(20deg)}"}),
    (".cape", f"{n}-flap .5s ease-in-out infinite alternate", {f"{n}-flap": "from{transform:skewY(-4deg) scale(1,1)} to{transform:skewY(4deg) scale(1.06,.96)}"}),
    (".vl", f"{n}-vl .6s linear infinite", {f"{n}-vl": "from{transform:translateY(-40px);opacity:0} 30%{opacity:1} to{transform:translateY(120px);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .vl{i} {{ animation-delay: -{i * .2:.1f}s; }}" for i in range(3)), body))

# 37. Zen : flotte en méditation, ondes de calme ------------------------------------
n = "zen"
waves = "".join(g((620, 560), f"aw aw{i}", f'<circle r="420" fill="none" stroke="{BLUE}" stroke-width="10"/>') for i in range(3))
body = waves + mascot()
A[n] = ("Zen", "Concentration, avant un tournoi, respiration", svg(n, "Zen", css(n, [
    (".rig", f"{n}-float 4s ease-in-out infinite", {f"{n}-float": "0%,100%{transform:translateY(-40px)} 50%{transform:translateY(-90px)}"}),
    (".arm", f"{n}-arm 4s ease-in-out infinite", {f"{n}-arm": "0%,100%{transform:rotate(-124deg)} 50%{transform:rotate(-118deg)}"}),
    (".aw", f"{n}-aw 4s ease-out infinite backwards", {f"{n}-aw": "from{transform:scale(.4);opacity:.8} to{transform:scale(1.3);opacity:0}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .aw{i} {{ animation-delay: {i * 1.33:.2f}s; }}" for i in range(3)), body, shadow=True))

# 38. Café : une tasse fumante à la main --------------------------------------------
n = "cafe"
body = mascot(arm_inner=g(FIST, "cup", f'<g transform="rotate(22) translate(0 40)">{CUP}</g>'))
A[n] = ("Café", "Bonjour, révision du matin, pause", svg(n, "Café", css(n, [
    (".rig", f"{n}-idle 3s ease-in-out infinite", {f"{n}-idle": "0%,100%{transform:rotate(0)} 50%{transform:rotate(-2deg) translateY(-6px)}"}),
    (".arm", f"{n}-sip 3s ease-in-out infinite", {f"{n}-sip": "0%,100%{transform:rotate(-22deg)} 45%,60%{transform:rotate(-8deg)}"}),
    (".st", f"{n}-st 1.8s ease-in-out infinite backwards", {f"{n}-st": "0%{opacity:0;transform:translateY(20px)} 40%{opacity:.7} 100%{opacity:0;transform:translateY(-40px)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .st{i} {{ animation-delay: {i * .5:.1f}s; }}" for i in range(3)), body))

# 39. Parapluie : à l'abri sous la pluie -------------------------------------------
n = "parapluie"
drops = "".join(g((x, -320), f"dr dr{i}", f'<path d="M0,-22 C12,-4 16,6 16,14 A16,16 0 0 1 -16,14 C-16,6 -12,-4 0,-22Z" fill="{BLUE}" stroke="{LINE}" stroke-width="6"/>') for i, x in enumerate([-10, 120, 860, 980, 1080]))
body = drops + mascot(arm_inner=g(FIST, "um", f'<g transform="rotate(30) translate(0 40) scale(.85)">{UMBRELLA}</g>'))
A[n] = ("Parapluie", "Coup dur, défaite, « on reste à l'abri »", svg(n, "Parapluie", css(n, [
    (".rig", f"{n}-idle 2.4s ease-in-out infinite", {f"{n}-idle": "0%,100%{transform:rotate(0)} 50%{transform:rotate(1.5deg) translateY(-6px)}"}),
    (".arm", f"{n}-hold 2.4s ease-in-out infinite", {f"{n}-hold": "0%,100%{transform:rotate(-30deg)} 50%{transform:rotate(-24deg)}"}),
    (".dr", f"{n}-rain 1.1s linear infinite", {f"{n}-rain": "from{transform:translateY(0);opacity:1} to{transform:translateY(1300px);opacity:1}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .dr{i} {{ animation-delay: -{(i * .37) % 1.1:.2f}s; }}" for i in range(5)), body))

# 40. Bonnet : hiver, la neige tombe -------------------------------------------------
n = "bonnet"
flakes = "".join(g((60 + (k * 137) % 1040, -320), f"fl fl{k}", SNOW()) for k in range(9))
body = flakes + mascot(head_inner=g((0, 30), "bn", f'<g transform="rotate(-14)">{BONNET}</g>'))
A[n] = ("Bonnet d'hiver", "Hiver, fêtes de fin d'année, vacances", svg(n, "Bonnet", css(n, [
    (".rig", f"{n}-shiver .16s ease-in-out infinite alternate", {f"{n}-shiver": "from{transform:translateX(-3px)} to{transform:translateX(3px)}"}),
    (".arm", f"{n}-arm 2s ease-in-out infinite", {f"{n}-arm": "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(-16deg)}"}),
    (".fl", f"{n}-snow 4s linear infinite", {f"{n}-snow": "from{transform:translate(0,0) rotate(0)} to{transform:translate(60px,1400px) rotate(360deg)}"}),
]) + "\n" + "\n".join(f".mascotte-{n} .fl{k} {{ animation-delay: -{(k * .53) % 4:.2f}s; }}" for k in range(9)), body))


ENV = f'''<g><g class="lettre"><rect x="-120" y="-150" width="240" height="190" rx="10" fill="{YELLOW}" stroke="{LINE}" stroke-width="10"/>
<path d="M-80,-110 L80,-110 M-80,-70 L80,-70 M-80,-30 L40,-30" stroke="{LINE}" stroke-width="12" stroke-linecap="round"/></g>
<rect x="-160" y="-110" width="320" height="210" rx="16" fill="#fff" stroke="{LINE}" stroke-width="12"/>
<path d="M-160,95 L0,-10 L160,95" fill="none" stroke="{LINE}" stroke-width="10" stroke-linejoin="round"/>
<g transform="translate(0 -104)"><g class="rabat"><path d="M-156,0 L0,110 L156,0 Z" fill="#fff" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/></g></g></g>'''

# 41. Message reçu : une enveloppe arrive dans la main, s'ouvre, la lettre sort --------
n = "message-recu"
badge = g((165, -125), "notif", f'<circle r="44" fill="{PINK}" stroke="{LINE}" stroke-width="10"/><path d="M0,-20 L0,20" stroke="#fff" stroke-width="14" stroke-linecap="round"/>')
body = mascot(arm_inner=g((FIST[0] + 20, FIST[1] - 150), "env", f'<g transform="rotate(16)">{ENV}{badge}</g>'))
A[n] = ("Message reçu", "Nouveau message, notification, réponse d'un coach", svg(n, "Message reçu", css(n, [
    (".rig", f"{n}-hop .7s linear .3s both, {n}-idle 2.6s ease-in-out 1s infinite", {
        f"{n}-hop": jump(50), f"{n}-idle": "0%,100%{transform:scale(1)} 50%{transform:translateY(-6px) scale(.99,1.01)}"}),
    (".arm", f"{n}-catch .6s {EASE_BACK} both, {n}-hold 2.6s ease-in-out .6s infinite", {
        f"{n}-catch": "from{transform:rotate(-90deg)} to{transform:rotate(-4deg)}",
        f"{n}-hold": "0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(2deg)}"}),
    (".env", f"{n}-in .6s {EASE_BACK} .2s both", {f"{n}-in": "from{transform:translate(260px,-360px) rotate(40deg) scale(.4);opacity:0} to{transform:translate(0,0) rotate(0) scale(1);opacity:1}"}),
    (".rabat", f"{n}-open 2.6s ease-in-out 1s infinite backwards", {f"{n}-open": "0%,10%{transform:scaleY(1)} 25%,80%{transform:scaleY(-1)} 95%,100%{transform:scaleY(1)}"}),
    (".lettre", f"{n}-out 2.6s ease-in-out 1s infinite backwards", {f"{n}-out": "0%,20%{transform:translateY(60px)} 40%,75%{transform:translateY(-90px)} 90%,100%{transform:translateY(60px)}"}),
    (".notif", f"{n}-notif .4s {EASE_BACK} .8s both, {n}-pulse 1.3s ease-in-out 1.2s infinite", {
        f"{n}-notif": "from{transform:scale(0)} to{transform:scale(1)}",
        f"{n}-pulse": "0%,100%{transform:scale(1)} 50%{transform:scale(1.15)}"}),
]), body))

# 42. Envoi de mail : lance une enveloppe qui s'envole --------------------------------
n = "envoi-mail"
vol = g((240, 120), "vol", f'<g transform="scale(.75)">{ENV}</g>' + "".join(f'<path class="tr" d="M{200 + i * 40},{-40 + i * 50} L{320 + i * 40},{-40 + i * 50}" stroke="{LINE}" stroke-width="12" stroke-linecap="round"/>' for i in range(3)))
body = mascot() + vol
A[n] = ("Envoi de mail", "Newsletter, e-mail envoyé, invitation", svg(n, "Envoi de mail", css(n, [
    (".rig", f"{n}-throw 2.2s ease-in-out infinite", {f"{n}-throw":
        "0%,100%{transform:rotate(0)} 20%{transform:rotate(4deg) scale(1.03,.97)} 35%{transform:rotate(-5deg) translateY(-20px)} 55%{transform:rotate(0)}"}),
    (".arm", f"{n}-arm 2.2s ease-in-out infinite", {f"{n}-arm": "0%,100%{transform:rotate(-30deg)} 20%{transform:rotate(-70deg)} 35%{transform:rotate(18deg)} 60%{transform:rotate(0)}"}),
    (".vol", f"{n}-fly 2.2s infinite", {f"{n}-fly":
        f"0%,30%{{transform:translate(0,0) rotate(0) scale(.6);opacity:0}} 34%{{transform:translate(0,0) rotate(0) scale(.9);opacity:1;animation-timing-function:{EASE_OUT}}} "
        f"80%{{transform:translate(-160px,-330px) rotate(-18deg) scale(.7);opacity:1}} 92%,100%{{transform:translate(-200px,-400px) rotate(-24deg) scale(.4);opacity:0}}"}),
]), body))

# ================================================================ mascotte articulée
# La silhouette du designer est découpée (clipPath) en tête, buste et deux jambes ; le bras
# collé sur la hanche est remplacé par un second bras articulé, symétrique du premier.
# Chaque pièce pivote autour de son articulation : on peut enfin bouger les DEUX bras,
# les jambes, la tête et le buste.
NECK, HIP, HIP_L, HIP_R, SH2 = (650, 470), (625, 800), (548, 795), (706, 795), (762, 575)
CLIPS = {
    "tete": "380,-10 1010,-10 1010,486 380,486",
    "buste": "380,470 772,478 800,560 788,640 780,790 780,862 380,862",
    "jambeg": "360,760 628,760 628,1110 360,1110",
    "jambed": "628,760 786,760 786,930 840,1110 628,1110",
    "jambes": "360,800 786,800 786,930 840,1110 360,1110",   # jambes d'origine, quand elles ne bougent pas
}


# Jambe redessinée dans le style de la silhouette : cuisse pleine qui s'affine, pied tourné vers l'avant
LEG = ("M-72,-24 C-72,-72 72,-72 72,-24 C72,66 62,150 54,206 C50,232 38,244 14,244 L-100,244 "
       "C-136,244 -142,204 -108,194 L-62,182 C-68,112 -72,40 -72,-24 Z")
# Buste redessiné : reprend le contour gauche de la silhouette, bas arrondi, côté droit galbé
BUSTE = ("M592,470 C566,510 546,560 532,612 C508,700 486,770 476,820 C520,872 734,872 790,826 "
         "C806,740 810,640 794,566 C786,524 774,494 760,470 Z")


def piece(name, part, pivot):
    """Pièce de la silhouette dans le repère de son articulation."""
    px, py = pivot
    return f'<g transform="translate({-px} {-py})"><path class="m" d="{BODY}" fill-rule="evenodd" clip-path="url(#{name}-{part})"/></g>'


# Coude : le bras du designer est coupé au milieu de sa courbe (droite x + y = -385 dans le repère
# de l'épaule) ; l'avant-bras pivote autour du coude, une articulation ronde masque le raccord.
ELBOW = (-253, -132)   # centre du tube à la coupe (largeur mesurée : 120)
ARM_UP = "300,-685 -685,300 300,300"       # côté épaule
ARM_LOW = "300,-685 -685,300 -685,-685"    # côté poing


def bras(name, inner="", mirror=False):
    """Bras en deux segments : épaule > .fa / .fa2 (coude) ; `inner` est dans le repère de l'épaule."""
    fa = "fa2" if mirror else "fa"
    ex, ey = ELBOW
    if mirror and inner:
        inner = f'<g transform="scale(-1 1)">{inner}</g>'
    low = (f'<g transform="translate({ex} {ey})"><g class="{fa}"><g transform="translate({-ex} {-ey})">'
           f'<path class="m" d="{ARM}" clip-path="url(#{name}-avb)"/>{inner}<circle class="m" cx="{ex}" cy="{ey}" r="62"/></g></g></g>')
    seg = f'<path class="m" d="{ARM}" clip-path="url(#{name}-bra)"/>{low}'
    return f'<g transform="scale(-1 1)">{seg}</g>' if mirror else seg


def mascot2(name, arm_inner="", arm2_inner="", head_inner="", extra_back="", torso_inner="", jambes=True):
    """Mascotte articulée : .rig > .legl, .legr, .torso > (.arm2, buste, .head, .arm)."""
    defs = ("<defs>" + "".join(f'<clipPath id="{name}-{k}"><polygon points="{v}"/></clipPath>' for k, v in CLIPS.items())
            + f'<clipPath id="{name}-bra"><polygon points="{ARM_UP}"/></clipPath><clipPath id="{name}-avb"><polygon points="{ARM_LOW}"/></clipPath></defs>')
    if jambes:
        jl = g(HIP_L, "legl", f'<path class="m" d="{LEG}"/>')
        jr = g(HIP_R, "legr", f'<path class="m" d="{LEG}"/>')
    else:   # jambes du dessin original, fixes
        jl, jr = f'<path class="m" d="{BODY}" fill-rule="evenodd" clip-path="url(#{name}-jambes)"/>', ""
    arm2 = g(SH2, "arm2", bras(name, arm2_inner, mirror=True) + '<circle class="m" r="50"/>')
    head = g(NECK, "head", piece(name, "tete", NECK) + (f'<g transform="translate({HEAD_TOP[0] - NECK[0]} {HEAD_TOP[1] - NECK[1]})">{head_inner}</g>' if head_inner else ""))
    arm = g(PIVOT, "arm", bras(name, arm_inner))
    torso = g(HIP, "torso", f'<g transform="translate({-HIP[0]} {-HIP[1]})">{arm2}<path class="m" d="{BUSTE}"/>'
              f'<circle class="m" cx="{NECK[0]}" cy="{NECK[1] + 10}" r="70"/>{head}<circle class="m" cx="{PIVOT[0]:.1f}" cy="{PIVOT[1]:.1f}" r="46"/>{arm}{torso_inner}</g>')
    fx, fy = FEET
    return defs + extra_back + g(FEET, "rig", f'<g transform="translate({-fx:.1f} {-fy:.1f})">{jl}{jr}{torso}</g>')


# Pose de repos de la mascotte articulée : bras du fond posé sur la hanche
REPOS = ".arm2 { transform: rotate(150deg); } .arm { transform: rotate(-112deg); }"



def pose2(n, title, usage, rules, extra_css="", ombre=None, coudes=None, **kw):
    """Ajoute une animation de la mascotte articulée ; repos par défaut : bras le long du corps.
    Les avant-bras (.fa, .fa2) ont un léger mouvement propre, en retard sur le corps (inertie) ;
    `coudes` = (a, b) angles de flexion de repos ; `ombre` = (durée, keyframes) pour l'ombre au sol."""
    rules = rules + PLIS.get(n, [])
    # Jambes redessinées seulement si elles sont le sujet de la pose ; sinon, celles du dessin original
    if n in JAMBES_ORIGINE:
        rules = [r for r in rules if ".leg" not in r[0]]
    kw.setdefault("jambes", any(".leg" in r[0] for r in rules))
    coudes = coudes or REPOS_COUDES.get(n)
    ombre = ombre or OMBRES.get(n)
    ca, cb = coudes or (10, 10)
    base = (f".mascotte-{n} .arm2 {{ transform: rotate(104deg); }} .mascotte-{n} .arm {{ transform: rotate(-104deg); }} "
            f".mascotte-{n} .legl {{ transform: rotate(10deg); }} .mascotte-{n} .legr {{ transform: rotate(-10deg); }}\n"
            f".mascotte-{n} .fa {{ animation: {n}-fa 1.6s ease-in-out .15s infinite alternate; }} .mascotte-{n} .fa2 {{ animation: {n}-fb 1.6s ease-in-out .3s infinite alternate; }}\n"
            f"@keyframes {n}-fa {{ from{{transform:rotate({ca - 6}deg)}} to{{transform:rotate({ca + 8}deg)}} }} @keyframes {n}-fb {{ from{{transform:rotate({cb - 6}deg)}} to{{transform:rotate({cb + 8}deg)}} }}\n"
            f".mascotte-{n} .shadow {{ transform-box: fill-box; transform-origin: center; }}")
    if ombre:
        base += f"\n.mascotte-{n} .shadow {{ animation: {n}-sh {ombre[0]} infinite; }} @keyframes {n}-sh {{ {ombre[1]} }}"
    shadow = kw.pop("shadow", True)
    body = kw.pop("before", "") + mascot2(n, **kw) + kw.pop("after", "") if False else None
    A[n] = (title, usage, svg(n, title, base + "\n" + css(n, rules) + ("\n" + extra_css if extra_css else ""), BODY2(n, kw), shadow=shadow))


def BODY2(n, kw):
    before, after = kw.pop("before", ""), kw.pop("after", "")
    return before + mascot2(n, **kw) + after


def ombre_saut(d):
    """Ombre qui rétrécit et pâlit quand la mascotte est en l'air (même rythme que jump())."""
    return (d, f"0%,16%,62%,100%{{transform:scale(1);opacity:.12;animation-timing-function:{UP}}} 42%{{transform:scale(.55);opacity:.05;animation-timing-function:{DOWN}}}")


# ---------------------------------------------------------------- passe d'animation
# Poses où les jambes ne font que de petits mouvements : on garde les jambes du dessin original
JAMBES_ORIGINE = {"hourra", "champion", "porte-echiquier", "invite", "boxe", "etirement-lateral"}
# Coudes : flexion de repos par pose (front, fond) et mouvements dédiés ; ombre au sol par pose.
REPOS_COUDES = {"hourra": (-14, -14), "pancarte": (24, 24), "porte-echiquier": (24, 24), "champion": (20, 20),
                "promenade": (24, 24), "coucou-autre-main": (10, 30), "selfie": (10, 10)}
def _fa(n, sel, frames, d="1s", t="ease-in-out infinite"):
    return (sel, f"{n}-{sel[1:]}x {d} {t}", {f"{n}-{sel[1:]}x": frames})
PLIS = {
    "haussement": [_fa("haussement", ".fa", "0%,60%,100%{transform:rotate(10deg)} 20%,40%{transform:rotate(78deg)}", "1.6s"),
                   _fa("haussement", ".fa2", "0%,60%,100%{transform:rotate(10deg)} 20%,40%{transform:rotate(78deg)}", "1.6s")],
    "sprint": [_fa("sprint", ".fa", "0%,100%{transform:rotate(60deg)} 50%{transform:rotate(96deg)}", ".5s"),
               _fa("sprint", ".fa2", "0%,100%{transform:rotate(96deg)} 50%{transform:rotate(60deg)}", ".5s")],
    "promenade": [_fa("promenade", ".fa", "0%,100%{transform:rotate(30deg)} 50%{transform:rotate(6deg)}", ".9s"),
                  _fa("promenade", ".fa2", "0%,100%{transform:rotate(6deg)} 50%{transform:rotate(30deg)}", ".9s")],
    "danse": [_fa("danse", ".fa", "0%,100%{transform:rotate(0)} 25%,75%{transform:rotate(70deg)}", "1.6s"),
              _fa("danse", ".fa2", "0%,100%{transform:rotate(70deg)} 25%,75%{transform:rotate(0)}", "1.6s")],
    "prof": [_fa("prof", ".fa2", "from{transform:rotate(20deg)} to{transform:rotate(64deg)}", ".8s", "ease-in-out infinite alternate")],
    "discute": [_fa("discute", ".fa", "0%,100%{transform:rotate(50deg)} 50%{transform:rotate(0)}", "1.2s"),
                _fa("discute", ".fa2", "0%,100%{transform:rotate(0)} 50%{transform:rotate(56deg)}", "1.2s")],
    "karate": [_fa("karate", ".fa", "0%,30%,80%,100%{transform:rotate(96deg)} 42%,62%{transform:rotate(10deg)}", "1.4s"),
               _fa("karate", ".fa2", "0%,30%,80%,100%{transform:rotate(90deg)} 42%,62%{transform:rotate(20deg)}", "1.4s")],
    "saut-etoile": [_fa("saut-etoile", ".fa", "0%,100%{transform:rotate(30deg)} 50%{transform:rotate(-10deg)}", ".8s"),
                    _fa("saut-etoile", ".fa2", "0%,100%{transform:rotate(30deg)} 50%{transform:rotate(-10deg)}", ".8s")],
    "oups": [_fa("oups", ".fa", "from{transform:rotate(-30deg)} to{transform:rotate(60deg)}", ".3s", "linear infinite alternate-reverse"),
             _fa("oups", ".fa2", "from{transform:rotate(-30deg)} to{transform:rotate(60deg)}", ".3s", "linear infinite alternate")],
    "invite": [_fa("invite", ".fa2", "from{transform:rotate(0)} to{transform:rotate(80deg)}", ".5s", "ease-in-out infinite alternate")],
    "coucou-autre-main": [_fa("coucou-autre-main", ".fa2", "from{transform:rotate(-20deg)} to{transform:rotate(36deg)}", ".4s", "ease-in-out infinite alternate")],
    "equilibre": [_fa("equilibre", ".fa", "0%,100%{transform:rotate(-20deg)} 50%{transform:rotate(10deg)}", "2s"),
                  _fa("equilibre", ".fa2", "0%,100%{transform:rotate(10deg)} 50%{transform:rotate(-20deg)}", "2s")],
    "reverence": [_fa("reverence", ".fa2", "0%,15%,90%,100%{transform:rotate(10deg)} 40%,65%{transform:rotate(90deg)}", "2.4s")],
}
OMBRES = {k: ombre_saut(d) for k, d in {"hourra": "1.1s", "champion": "1.2s", "pancarte": "1.4s", "saute-obstacle": "1.4s"}.items()}
OMBRES["saut-etoile"] = (".8s", "0%,100%{transform:scale(1);opacity:.12} 50%{transform:scale(.6);opacity:.05}")
OMBRES["sprint"] = (".25s", "from{transform:scale(1)} to{transform:scale(.85)}")
OMBRES["tailleur"] = ("4s", "0%,100%{transform:scale(.9);opacity:.1} 50%{transform:scale(.7);opacity:.06}")

# 43. Hourra : les DEUX bras en l'air, saute de joie -------------------------------
pose2("hourra", "Hourra !", "Grande victoire, objectif atteint", [
    (".rig", "hourra-jump 1.1s linear infinite", {"hourra-jump": jump(130)}),
    (".arm", f"hourra-a 1.1s {SOFT} infinite", {"hourra-a": "0%,100%{transform:rotate(-4deg)} 42%{transform:rotate(16deg)}"}),
    (".arm2", f"hourra-b 1.1s {SOFT} infinite", {"hourra-b": "0%,100%{transform:rotate(4deg)} 42%{transform:rotate(-16deg)}"}),
    (".legl", f"hourra-l 1.1s {SOFT} infinite", {"hourra-l": "0%,16%,62%,100%{transform:rotate(0)} 42%{transform:rotate(22deg)}"}),
    (".legr", f"hourra-r 1.1s {SOFT} infinite", {"hourra-r": "0%,16%,62%,100%{transform:rotate(0)} 42%{transform:rotate(-22deg)}"}),
])

# 44. Saut en étoile : bras et jambes s'écartent en rythme ---------------------------
pose2("saut-etoile", "Saut en étoile", "Échauffement, énergie, bonne humeur", [
    (".rig", "etoile-j .8s ease-in-out infinite", {"etoile-j": "0%,100%{transform:translateY(0) scale(1.02,.98)} 50%{transform:translateY(-90px) scale(.98,1.02)}"}),
    (".arm", "etoile-a .8s ease-in-out infinite", {"etoile-a": "0%,100%{transform:rotate(-112deg)} 50%{transform:rotate(14deg)}"}),
    (".arm2", "etoile-b .8s ease-in-out infinite", {"etoile-b": "0%,100%{transform:rotate(112deg)} 50%{transform:rotate(-14deg)}"}),
    (".legl", "etoile-l .8s ease-in-out infinite", {"etoile-l": "0%,100%{transform:rotate(0)} 50%{transform:rotate(26deg)}"}),
    (".legr", "etoile-r .8s ease-in-out infinite", {"etoile-r": "0%,100%{transform:rotate(0)} 50%{transform:rotate(-26deg)}"}),
])

# 45. Haussement d'épaules : « je ne sais pas » -------------------------------------
qm2 = g((620, -140), "q", f'<text font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="190" text-anchor="middle" fill="{LINE}">?</text>')
pose2("haussement", "Haussement d'épaules", "« Je ne sais pas », question ouverte, sondage", [
    (".torso", "hauss-t 1.6s ease-in-out infinite", {"hauss-t": "0%,60%,100%{transform:translateY(0)} 20%,40%{transform:translateY(-34px)}"}),
    (".arm", "hauss-a 1.6s ease-in-out infinite", {"hauss-a": "0%,60%,100%{transform:rotate(-100deg)} 20%,40%{transform:rotate(-66deg)}"}),
    (".arm2", "hauss-b 1.6s ease-in-out infinite", {"hauss-b": "0%,60%,100%{transform:rotate(112deg)} 20%,40%{transform:rotate(102deg)}"}),
    (".head", "hauss-h 1.6s ease-in-out infinite", {"hauss-h": "0%,60%,100%{transform:rotate(0)} 20%,40%{transform:rotate(-12deg)}"}),
    (".q", "hauss-q 1.6s ease-in-out infinite", {"hauss-q": "0%,100%{opacity:0;transform:translateY(30px)} 25%,55%{opacity:1;transform:translateY(0)}"}),
], after=qm2)

# 46. Marche : les jambes avancent, les bras balancent en opposition ------------------
pose2("promenade", "Promenade", "Parcours, « en route », pas à pas", [
    (".rig", "prom-b .45s ease-in-out infinite alternate", {"prom-b": "from{transform:translateY(0)} to{transform:translateY(-22px)}"}),
    (".legl", "prom-l .9s ease-in-out infinite", {"prom-l": "0%,100%{transform:rotate(22deg)} 50%{transform:rotate(-20deg)}"}),
    (".legr", "prom-r .9s ease-in-out infinite", {"prom-r": "0%,100%{transform:rotate(-20deg)} 50%{transform:rotate(22deg)}"}),
    (".arm", "prom-a .9s ease-in-out infinite", {"prom-a": "0%,100%{transform:rotate(-140deg)} 50%{transform:rotate(-84deg)}"}),
    (".arm2", "prom-c .9s ease-in-out infinite", {"prom-c": "0%,100%{transform:rotate(84deg)} 50%{transform:rotate(140deg)}"}),
    (".torso", "prom-t .45s ease-in-out infinite alternate", {"prom-t": "from{transform:rotate(-3deg)} to{transform:rotate(-5deg)}"}),
])

# 47. Sprint : vraie course, grandes foulées, bras qui pompent -------------------------
vit2 = "".join(g((930 + i * 30, 320 + i * 200), f"vl vl{i}", f'<path d="M0,0 L{200 - i * 40},0" stroke="{LINE}" stroke-width="16" stroke-linecap="round"/>') for i in range(3))
pose2("sprint", "Sprint", "Défi chrono, blitz, « fonce ! »", [
    (".rig", "sprint-b .25s ease-in-out infinite alternate", {"sprint-b": "from{transform:translateY(0)} to{transform:translateY(-40px)}"}),
    (".torso", "sprint-t .5s ease-in-out infinite", {"sprint-t": "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(-17deg)}"}),
    (".legl", "sprint-l .5s ease-in-out infinite", {"sprint-l": "0%,100%{transform:rotate(48deg)} 50%{transform:rotate(-34deg)}"}),
    (".legr", "sprint-r .5s ease-in-out infinite", {"sprint-r": "0%,100%{transform:rotate(-34deg)} 50%{transform:rotate(48deg)}"}),
    (".arm", "sprint-a .5s ease-in-out infinite", {"sprint-a": "0%,100%{transform:rotate(-150deg)} 50%{transform:rotate(-40deg)}"}),
    (".arm2", "sprint-c .5s ease-in-out infinite", {"sprint-c": "0%,100%{transform:rotate(-40deg)} 50%{transform:rotate(124deg)}"}),
    (".vl", ".5s linear infinite sprint-v", {"sprint-v": "from{transform:translateX(-60px);opacity:1} to{transform:translateX(140px);opacity:0}"}),
], extra_css="\n".join(f".mascotte-sprint .vl{i} {{ animation-delay: -{i * .16:.2f}s; }}" for i in range(3)), before=vit2)

# 48. Coucou de l'autre main ----------------------------------------------------------
pose2("coucou-autre-main", "Coucou (autre main)", "Accueil, au revoir", [
    (".rig", "cam-s 1.6s ease-in-out infinite", {"cam-s": "0%,100%{transform:rotate(1deg)} 50%{transform:rotate(-1deg) translateY(-6px)}"}),
    (".arm2", "cam-w .4s ease-in-out infinite alternate", {"cam-w": "from{transform:rotate(4deg)} to{transform:rotate(-34deg)}"}),
    (".arm", "cam-a 1.6s ease-in-out infinite", {"cam-a": "0%,100%{transform:rotate(-118deg)} 50%{transform:rotate(-110deg)}"}),
    (".head", "cam-h 1.6s ease-in-out infinite", {"cam-h": "0%,100%{transform:rotate(6deg)} 50%{transform:rotate(9deg)}"}),
])

# 51. Cherche : main en visière, la tête tourne ----------------------------------------
pose2("cherche", "Cherche à l'horizon", "Recherche, « où est le bon coup ? », nouveautés à venir", [
    (".arm2", "che-b .6s ease-out both", {"che-b": "from{transform:rotate(112deg)} to{transform:rotate(-58deg)}"}),
    (".arm", "che-a 2.4s ease-in-out infinite", {"che-a": "0%,100%{transform:rotate(-120deg)} 50%{transform:rotate(-112deg)}"}),
    (".torso", "che-t 2.4s ease-in-out infinite", {"che-t": "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(5deg)}"}),
    (".rig", "che-r 2.4s ease-in-out infinite", {"che-r": "0%,100%{transform:translateY(0)} 25%,75%{transform:translateY(-14px)}"}),
])

# 52. Danse : bras et jambes alternés ------------------------------------------------------
pose2("danse", "Danse", "Fête, week-end, bonne nouvelle", [
    (".rig", "dan-r .8s ease-in-out infinite", {"dan-r": "0%,100%{transform:rotate(-4deg) translateY(0)} 50%{transform:rotate(4deg) translateY(-26px)}"}),
    (".arm", "dan-a 1.6s ease-in-out infinite", {"dan-a": "0%,100%{transform:rotate(10deg)} 50%{transform:rotate(-100deg)}"}),
    (".arm2", "dan-b 1.6s ease-in-out infinite", {"dan-b": "0%,100%{transform:rotate(126deg)} 50%{transform:rotate(-14deg)}"}),
    (".legl", "dan-l .8s ease-in-out infinite", {"dan-l": "0%,100%{transform:rotate(30deg)} 50%{transform:rotate(0)}"}),
    (".legr", "dan-m .8s ease-in-out infinite", {"dan-m": "0%,100%{transform:rotate(0)} 50%{transform:rotate(-30deg)}"}),
    (".head", "dan-h .4s ease-in-out infinite alternate", {"dan-h": "from{transform:rotate(-6deg)} to{transform:rotate(6deg)}"}),
])

# 54. Coup de pied : envoie un pion en l'air ------------------------------------------------
pion_vole = g((330, 960), "pv", f'<g transform="scale(.5)">{PAWN}</g>')
pose2("coup-de-pied", "Coup de pied", "Lancement, « c'est parti ! », défi", [
    (".legl", "cdp-l 1.6s infinite", {"cdp-l": f"0%,20%{{transform:rotate(-30deg);animation-timing-function:{EASE_IN}}} 32%{{transform:rotate(80deg);animation-timing-function:{EASE_OUT}}} 60%,100%{{transform:rotate(0)}}"}),
    (".torso", "cdp-t 1.6s ease-in-out infinite", {"cdp-t": "0%,20%{transform:rotate(4deg)} 32%{transform:rotate(10deg)} 60%,100%{transform:rotate(0)}"}),
    (".arm", "cdp-a 1.6s ease-in-out infinite", {"cdp-a": "0%,20%{transform:rotate(-80deg)} 32%{transform:rotate(-150deg)} 60%,100%{transform:rotate(-112deg)}"}),
    (".arm2", "cdp-b 1.6s ease-in-out infinite", {"cdp-b": "0%,20%{transform:rotate(130deg)} 32%{transform:rotate(40deg)} 60%,100%{transform:rotate(112deg)}"}),
    (".pv", "cdp-p 1.6s infinite", {"cdp-p": f"0%,30%{{transform:translate(0,0) rotate(0);opacity:1;animation-timing-function:{EASE_OUT}}} 70%{{transform:translate(-260px,-760px) rotate(-260deg);opacity:1}} 80%,100%{{transform:translate(-300px,-860px) rotate(-300deg);opacity:0}}"}),
], after=pion_vole)

# 55. Étirement latéral : bras en l'air, se penche d'un côté puis de l'autre -------------------
pose2("etirement-lateral", "Étirement latéral", "Échauffement, début de séance", [
    (".torso", "etl-t 3s ease-in-out infinite", {"etl-t": "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(14deg)}"}),
    (".arm", "etl-a 3s ease-in-out infinite", {"etl-a": "0%,100%{transform:rotate(30deg)} 50%{transform:rotate(14deg)}"}),
    (".arm2", "etl-b 3s ease-in-out infinite", {"etl-b": "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(-30deg)}"}),
    (".legl", "etl-l 3s ease-in-out infinite", {"etl-l": "0%,100%{transform:rotate(10deg)} 50%{transform:rotate(14deg)}"}),
    (".legr", "etl-r 3s ease-in-out infinite", {"etl-r": "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(-10deg)}"}),
])

# 56. Équilibre : sur une jambe, bras écartés, vacille un peu -----------------------------------
pose2("equilibre", "Équilibre", "Concentration, maîtrise, « tiens bon »", [
    (".rig", "equ-r 2s ease-in-out infinite", {"equ-r": "0%,100%{transform:rotate(-3deg)} 50%{transform:rotate(3deg)}"}),
    (".legr", "equ-l .6s ease-out both", {"equ-l": "from{transform:rotate(0)} to{transform:rotate(-72deg)}"}),
    (".arm", "equ-a 2s ease-in-out infinite", {"equ-a": "0%,100%{transform:rotate(-30deg)} 50%{transform:rotate(-40deg)}"}),
    (".arm2", "equ-b 2s ease-in-out infinite", {"equ-b": "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(6deg)}"}),
])

# 57. Révérence : s'incline pour remercier ---------------------------------------------------
pose2("reverence", "Révérence", "Merci, fin de cours, au revoir", [
    (".torso", "rev-t 2.4s infinite", {"rev-t": f"0%,15%{{transform:rotate(0);animation-timing-function:{EASE_IO}}} 40%,65%{{transform:rotate(-38deg);animation-timing-function:{EASE_IO}}} 90%,100%{{transform:rotate(0)}}"}),
    (".arm", "rev-a 2.4s ease-in-out infinite", {"rev-a": "0%,15%,90%,100%{transform:rotate(-112deg)} 40%,65%{transform:rotate(-150deg)}"}),
    (".arm2", "rev-b 2.4s ease-in-out infinite", {"rev-b": "0%,15%,90%,100%{transform:rotate(104deg)} 40%,65%{transform:rotate(4deg)}"}),
    (".head", "rev-h 2.4s ease-in-out infinite", {"rev-h": "0%,15%,90%,100%{transform:rotate(0)} 40%,65%{transform:rotate(-10deg)}"}),
])

# 58. Pouce levé (bras du fond tendu vers le haut, l'autre sur la hanche) -------------------
pose2("super", "Super !", "Validation, « bien joué », approbation", [
    (".rig", "sup-r .6s {0} both, sup-i 2s ease-in-out .6s infinite".format(EASE_BACK), {"sup-r": "from{transform:translateY(40px) scale(1.05,.92)} to{transform:none}", "sup-i": "0%,100%{transform:none} 50%{transform:translateY(-8px)}"}),
    (".arm2", f"sup-b .6s {EASE_BACK} both", {"sup-b": "from{transform:rotate(112deg)} to{transform:rotate(2deg)}"}),
    (".arm", "sup-a 2s ease-in-out infinite", {"sup-a": "0%,100%{transform:rotate(-120deg)} 50%{transform:rotate(-114deg)}"}),
    (".head", "sup-h 2s ease-in-out infinite", {"sup-h": "0%,100%{transform:rotate(4deg)} 50%{transform:rotate(-2deg)}"}),
], arm2_inner=g((324, -413), "spk", sparkle(1.2)))

# ---------------------------------------------------------------- mascotte articulée : variantes
def tilt(a, b, d="2s"):
    return f"{d} ease-in-out infinite alternate", {"from": f"transform:rotate({a}deg)", "to": f"transform:rotate({b}deg)"}


def anim(n, sel, name, dur, frames, timing="ease-in-out infinite"):
    return (sel, f"{n}-{name} {dur} {timing}", {f"{n}-{name}": frames})


PANCARTE = f'''<g><rect x="300" y="-300" width="780" height="390" rx="26" fill="#fff" stroke="{LINE}" stroke-width="14"/>
<path d="M380,-210 L1000,-210 M380,-120 L900,-120 M380,-30 L760,-30" stroke="{BLUE}" stroke-width="34" stroke-linecap="round"/></g>'''
PAWN_Y = PAWN.replace('fill="#fff"', f'fill="{YELLOW}"')
KING = (f'<g><path d="M-14,-250 L14,-250 L14,-226 L38,-226 L38,-200 L14,-200 L14,-176 L-14,-176 L-14,-200 L-38,-200 L-38,-226 L-14,-226 Z" fill="#fff" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>'
        + PAWN.replace('<circle cy="-158" r="50"', '<ellipse cy="-150" rx="58" ry="46"') + '</g>')
ECHIQUIER = (f'<g><path d="M372,-58 L1008,-58 L1046,-14 L334,-14 Z" fill="#e4ecf6" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>'
             + "".join(f'<path d="M{372 + k * 79.5},-58 L{372 + (k + 1) * 79.5},-58 L{334 + (k + 1) * 89},-14 L{334 + k * 89},-14 Z" fill="{BLUE}"/>' for k in range(0, 8, 2))
             + f'<path d="M372,-58 L1008,-58 L1046,-14 L334,-14 Z" fill="none" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>'
             + f'<rect x="334" y="-14" width="712" height="54" rx="12" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/>'
             + "".join(f'<rect x="{346 + k * 86.5}" y="-2" width="43" height="30" rx="4" fill="#e4ecf6"/>' for k in range(8))
             + g((500, -50), "pc1", f'<g transform="scale(.55)">{PAWN}</g>') + g((690, -50), "pc2", f'<g transform="scale(.62)">{KING}</g>')
             + g((880, -50), "pc3", f'<g transform="scale(.55)">{PAWN_Y if "PAWN_Y" in globals() else PAWN}</g>') + '</g>')
COUPE = f'''<g transform="translate(690 -40) scale(1.1)"><path d="M-95,-150 L95,-150 C95,-40 50,10 0,20 C-50,10 -95,-40 -95,-150 Z" fill="{YELLOW}" stroke="{LINE}" stroke-width="12" stroke-linejoin="round"/>
<path d="M-95,-125 C-160,-125 -160,-40 -70,-30 M95,-125 C160,-125 160,-40 70,-30" fill="none" stroke="{LINE}" stroke-width="14" stroke-linecap="round"/>
<rect x="-18" y="18" width="36" height="50" fill="{LINE}"/><rect x="-70" y="64" width="140" height="38" rx="8" fill="{LINE}"/></g>'''
PAWN_Y = PAWN.replace('fill="#fff"', f'fill="{YELLOW}"')

# 53. Assise par terre : jambes tendues devant, sur un coussin --------------------------
COUSSIN = f'<rect x="470" y="980" width="320" height="80" rx="40" fill="{BLUE}" stroke="{LINE}" stroke-width="12"/>'
pose2("assise", "Assise par terre", "Pause, lecture d'un cours, détente", [
    anim("assise", ".rig", "r", "3s", "0%,100%{transform:translateY(60px)} 50%{transform:translateY(64px) scale(1.01,.99)}"),
    anim("assise", ".legl", "l", ".7s", "from{transform:rotate(84deg)} to{transform:rotate(74deg)}", "ease-in-out infinite alternate"),
    anim("assise", ".legr", "m", ".7s", "from{transform:rotate(72deg)} to{transform:rotate(82deg)}", "ease-in-out infinite alternate"),
    anim("assise", ".arm", "a", "3s", "0%,100%{transform:rotate(-78deg)} 50%{transform:rotate(-72deg)}"),
    anim("assise", ".arm2", "b", "3s", "0%,100%{transform:rotate(-14deg)} 50%{transform:rotate(-24deg)}"),
    anim("assise", ".head", "h", "3s", "0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(5deg)}"),
], before=COUSSIN)

# 59. Se gratte la tête : « hmm… » -------------------------------------------------------
pose2("gratte-tete", "Se gratte la tête", "Réflexion, problème difficile, « hmm… »", [
    anim("gratte-tete", ".arm2", "b", ".25s", "from{transform:rotate(-24deg)} to{transform:rotate(-34deg)}", "ease-in-out infinite alternate"),
    anim("gratte-tete", ".arm", "a", "3s", "0%,100%{transform:rotate(-110deg)} 50%{transform:rotate(-104deg)}"),
    anim("gratte-tete", ".head", "h", "3s", "0%,100%{transform:rotate(-8deg)} 50%{transform:rotate(-12deg)}"),
    anim("gratte-tete", ".torso", "t", "3s", "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(1deg)}"),
], after=g((380, -60), "q", f'<text font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="150" text-anchor="middle" fill="{LINE}">?</text>'))

# 60. Pancarte : brandit une pancarte des deux mains ------------------------------------------
pose2("pancarte", "Pancarte", "Annonce, message, « à retenir » (texte à ajouter par-dessus)", [
    anim("pancarte", ".rig", "j", "1.4s", jump(40), "linear infinite"),
    anim("pancarte", ".arm", "a", "1.4s", "0%,100%{transform:rotate(14deg)} 50%{transform:rotate(10deg)}"),
    anim("pancarte", ".arm2", "b", "1.4s", "0%,100%{transform:rotate(-12deg)} 50%{transform:rotate(-8deg)}"),
    anim("pancarte", ".pc", "p", "1.4s", "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(2deg)}"),
], torso_inner=g((690, -100), "pc", f'<g transform="translate(-690 100)">{PANCARTE}</g>'))

# 61. Échiquier porté au-dessus de la tête ---------------------------------------------------
pose2("porte-echiquier", "Porte un échiquier", "Nouvelle fonctionnalité, partie en ligne, « on joue ? »", [
    anim("porte-echiquier", ".rig", "w", ".8s", "0%,100%{transform:rotate(-2deg) translateY(0)} 50%{transform:rotate(2deg) translateY(-14px)}"),
    anim("porte-echiquier", ".legl", "l", ".8s", "0%,100%{transform:rotate(14deg)} 50%{transform:rotate(-10deg)}"),
    anim("porte-echiquier", ".legr", "r", ".8s", "0%,100%{transform:rotate(-10deg)} 50%{transform:rotate(14deg)}"),
    anim("porte-echiquier", ".arm", "a", ".8s", "0%,100%{transform:rotate(16deg)} 50%{transform:rotate(12deg)}"),
    anim("porte-echiquier", ".arm2", "b", ".8s", "0%,100%{transform:rotate(-12deg)} 50%{transform:rotate(-16deg)}"),
], torso_inner=ECHIQUIER)

# 62. Champion : coupe brandie à deux mains --------------------------------------------------
conf2 = "".join(g((150 + (k * 113) % 950, -300), f"cf cf{k}", f'<rect x="-10" y="-16" width="20" height="32" rx="4" fill="{[YELLOW, BLUE, GREEN, PINK][k % 4]}"/>') for k in range(12))
pose2("champion", "Champion", "Tournoi gagné, podium, record", [
    anim("champion", ".rig", "j", "1.2s", jump(90), "linear infinite"),
    anim("champion", ".arm", "a", "1.2s", "0%,100%{transform:rotate(22deg)} 42%{transform:rotate(26deg)}"),
    anim("champion", ".arm2", "b", "1.2s", "0%,100%{transform:rotate(-6deg)} 42%{transform:rotate(-10deg)}"),
    anim("champion", ".legl", "l", "1.2s", "0%,16%,62%,100%{transform:rotate(0)} 42%{transform:rotate(18deg)}"),
    anim("champion", ".legr", "r", "1.2s", "0%,16%,62%,100%{transform:rotate(0)} 42%{transform:rotate(-18deg)}"),
    (".cf", "champion-f 2.4s linear infinite", {"champion-f": "from{transform:translateY(0) rotate(0)} to{transform:translateY(1400px) rotate(720deg)}"}),
], extra_css="\n".join(f".mascotte-champion .cf{k} {{ animation-delay: -{(k * .41) % 2.4:.2f}s; }}" for k in range(12)), torso_inner=COUPE, before=conf2)

# 63. Blancs ou Noirs ? un pion dans chaque main ---------------------------------------------
pose2("blancs-ou-noirs", "Blancs ou Noirs ?", "Choix, sondage, tirage au sort", [
    anim("blancs-ou-noirs", ".arm", "a", "1.6s", "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(-24deg)}"),
    anim("blancs-ou-noirs", ".arm2", "b", "1.6s", "0%,100%{transform:rotate(-24deg)} 50%{transform:rotate(-6deg)}"),
    anim("blancs-ou-noirs", ".head", "h", "1.6s", "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(6deg)}"),
    anim("blancs-ou-noirs", ".torso", "t", "1.6s", "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(2deg)}"),
], arm_inner=g((FIST[0], FIST[1] - 40), "p1", f'<g transform="scale(.8)">{PAWN}</g>'), arm2_inner=g((324, -453), "p2", f'<g transform="scale(.8)">{PAWN_Y}</g>'))

# 64. La roue : tourne sur elle-même, bras et jambes écartés -----------------------------------
n = "roue"
body = g((620, 560), "spin", f'<g transform="translate(-620 -560)">{mascot2(n)}</g>')
A[n] = ("La roue", "Énorme progrès, « on a tout retourné ! »", svg(n, "La roue",
    f".mascotte-{n} .arm {{ transform: rotate(4deg); }} .mascotte-{n} .arm2 {{ transform: rotate(-4deg); }} .mascotte-{n} .legl {{ transform: rotate(30deg); }} .mascotte-{n} .legr {{ transform: rotate(-30deg); }}\n"
    + css(n, [(".spin", f"{n}-s 2.4s {EASE_IO} infinite", {f"{n}-s": "0%,15%{transform:rotate(0) scale(.86)} 85%,100%{transform:rotate(-360deg) scale(.86)}"})]), body))

# 65. Oups ! trébuche, bras qui moulinent --------------------------------------------------
pose2("oups", "Oups !", "Erreur, bug, « pas de panique »", [
    anim("oups", ".torso", "t", "1.2s", f"0%,100%{{transform:rotate(-4deg)}} 30%{{transform:rotate(-26deg)}} 60%{{transform:rotate(-14deg)}}"),
    anim("oups", ".rig", "r", "1.2s", "0%,100%{transform:translateX(0)} 30%{transform:translateX(-40px) translateY(-20px)} 60%{transform:translateX(-20px)}"),
    anim("oups", ".arm", "a", ".3s", "from{transform:rotate(-30deg)} to{transform:rotate(30deg)}", "linear infinite alternate"),
    anim("oups", ".arm2", "b", ".3s", "from{transform:rotate(-60deg)} to{transform:rotate(10deg)}", "linear infinite alternate-reverse"),
    anim("oups", ".legr", "l", "1.2s", "0%,100%{transform:rotate(0)} 30%{transform:rotate(-46deg)} 60%{transform:rotate(-20deg)}"),
    anim("oups", ".legl", "m", "1.2s", "0%,100%{transform:rotate(0)} 30%{transform:rotate(14deg)}"),
], after=g((300, 120), "q", f'<text font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="170" text-anchor="middle" fill="{LINE}">!</text>'))

# 66. Tailleur : méditation en lévitation ---------------------------------------------------
waves2 = "".join(g((620, 620), f"aw aw{i}", f'<circle r="420" fill="none" stroke="{BLUE}" stroke-width="10"/>') for i in range(3))
pose2("tailleur", "En tailleur", "Concentration, calme avant un tournoi", [
    anim("tailleur", ".rig", "f", "4s", "0%,100%{transform:translateY(-10px)} 50%{transform:translateY(-70px)}"),
    anim("tailleur", ".legl", "l", "4s", "0%,100%{transform:rotate(84deg)} 50%{transform:rotate(80deg)}"),
    anim("tailleur", ".legr", "r", "4s", "0%,100%{transform:rotate(-84deg)} 50%{transform:rotate(-80deg)}"),
    anim("tailleur", ".arm", "a", "4s", "0%,100%{transform:rotate(-74deg)} 50%{transform:rotate(-70deg)}"),
    anim("tailleur", ".arm2", "b", "4s", "0%,100%{transform:rotate(104deg)} 50%{transform:rotate(100deg)}"),
    (".aw", "tailleur-w 4s ease-out infinite backwards", {"tailleur-w": "from{transform:scale(.4);opacity:.8} to{transform:scale(1.3);opacity:0}"}),
], extra_css="\n".join(f".mascotte-tailleur .aw{i} {{ animation-delay: {i * 1.33:.2f}s; }}" for i in range(3)), before=waves2)

# 67. Arbre (yoga) : sur une jambe, mains jointes au-dessus de la tête --------------------------
pose2("yoga-arbre", "Yoga : l'arbre", "Équilibre, bien-être, patience", [
    anim("yoga-arbre", ".rig", "r", "3s", "0%,100%{transform:rotate(-2deg)} 50%{transform:rotate(2deg)}"),
    (".legr", "yoga-arbre-l .8s ease-out both", {"yoga-arbre-l": "from{transform:rotate(0)} to{transform:rotate(-96deg)}"}),
    anim("yoga-arbre", ".arm", "a", "3s", "0%,100%{transform:rotate(28deg)} 50%{transform:rotate(24deg)}"),
    anim("yoga-arbre", ".arm2", "b", "3s", "0%,100%{transform:rotate(-30deg)} 50%{transform:rotate(-26deg)}"),
])

# 68. Karaté : coup de pied haut, garde ----------------------------------------------------
pose2("karate", "Karaté", "Attaque, combinaison tactique, « kiai ! »", [
    anim("karate", ".legl", "l", "1.4s", f"0%,30%{{transform:rotate(10deg)}} 42%,62%{{transform:rotate(96deg)}} 80%,100%{{transform:rotate(10deg)}}"),
    anim("karate", ".torso", "t", "1.4s", "0%,30%,80%,100%{transform:rotate(0)} 42%,62%{transform:rotate(16deg)}"),
    anim("karate", ".arm", "a", "1.4s", "0%,30%,80%,100%{transform:rotate(-60deg)} 42%,62%{transform:rotate(-100deg)}"),
    anim("karate", ".arm2", "b", "1.4s", "0%,30%,80%,100%{transform:rotate(-24deg)} 42%,62%{transform:rotate(112deg)}"),
    anim("karate", ".rig", "r", "1.4s", "0%,30%,80%,100%{transform:translateY(0)} 42%,62%{transform:translateY(-20px)}"),
])

# 69. Patine : glisse sur la glace, une jambe en arrière ---------------------------------------
traces = "".join(g((700 + i * 80, 1040), f"vl vl{i}", f'<path d="M0,0 L{160 - i * 30},0" stroke="{BLUE}" stroke-width="12" stroke-linecap="round"/>') for i in range(3))
pose2("patine", "Patine", "Fluidité, « ça glisse ! », hiver", [
    anim("patine", ".rig", "g", "2.4s", "0%,100%{transform:translateX(120px) rotate(-3deg)} 50%{transform:translateX(-120px) rotate(3deg)}"),
    anim("patine", ".torso", "t", "2.4s", "0%,100%{transform:rotate(-20deg)} 50%{transform:rotate(-14deg)}"),
    anim("patine", ".legr", "r", "2.4s", "0%,100%{transform:rotate(-56deg)} 50%{transform:rotate(-40deg)}"),
    anim("patine", ".legl", "l", "2.4s", "0%,100%{transform:rotate(8deg)} 50%{transform:rotate(14deg)}"),
    anim("patine", ".arm", "a", "2.4s", "0%,100%{transform:rotate(-56deg)} 50%{transform:rotate(-66deg)}"),
    anim("patine", ".arm2", "b", "2.4s", "0%,100%{transform:rotate(124deg)} 50%{transform:rotate(110deg)}"),
    (".vl", "patine-v 1.2s linear infinite", {"patine-v": "from{transform:translateX(0);opacity:1} to{transform:translateX(200px);opacity:0}"}),
], before=traces)

# 70. Saut d'obstacle : saute par-dessus un pion qui défile ------------------------------------
haie = g((1200, 1040), "haie", f'<g transform="scale(.7)">{PAWN}</g>')
pose2("saute-obstacle", "Saut d'obstacle", "Difficulté surmontée, niveau suivant", [
    anim("saute-obstacle", ".rig", "j", "1.4s", jump(260, 1.08), "linear infinite"),
    anim("saute-obstacle", ".legl", "l", "1.4s", "0%,16%,70%,100%{transform:rotate(0)} 42%{transform:rotate(60deg)}"),
    anim("saute-obstacle", ".legr", "r", "1.4s", "0%,16%,70%,100%{transform:rotate(0)} 42%{transform:rotate(-56deg)}"),
    anim("saute-obstacle", ".arm", "a", "1.4s", "0%,16%,70%,100%{transform:rotate(-104deg)} 42%{transform:rotate(-30deg)}"),
    anim("saute-obstacle", ".arm2", "b", "1.4s", "0%,16%,70%,100%{transform:rotate(104deg)} 42%{transform:rotate(-20deg)}"),
    (".haie", "saute-obstacle-h 1.4s linear infinite", {"saute-obstacle-h": "from{transform:translateX(0)} to{transform:translateX(-1300px)}"}),
], after=haie)

# 71. Selfie : téléphone tenu à bout de bras, l'autre main fait coucou ---------------------------
flash = g((1090, 60), "fl", f'<circle r="70" fill="#fff" opacity=".9"/>')
pose2("selfie", "Selfie", "Partage, réseaux sociaux, « montre ta partie »", [
    (".arm2", "selfie-b .6s ease-out both", {"selfie-b": "from{transform:rotate(104deg)} to{transform:rotate(-4deg)}"}),
    anim("selfie", ".arm", "a", ".4s", "from{transform:rotate(-10deg)} to{transform:rotate(14deg)}", "ease-in-out infinite alternate"),
    anim("selfie", ".head", "h", "2s", "0%,100%{transform:rotate(10deg)} 50%{transform:rotate(14deg)}"),
    (".fl", "selfie-f 2s ease-out infinite", {"selfie-f": "0%,70%{opacity:0;transform:scale(.3)} 75%{opacity:1;transform:scale(1.4)} 100%{opacity:0;transform:scale(2)}"}),
], arm2_inner=g((324, -413), "ph", f'<g transform="rotate(-20) translate(0 40) scale(.8)">{PHONE}</g>'), after=flash)

# 72. Montre le ciel : désigne quelque chose en haut, une étoile brille ---------------------------
etoile = g((960, -200), "st", star(90))
pose2("montre-le-ciel", "Montre le ciel", "Objectif, « vise haut », nouveauté à venir", [
    (".arm2", f"montre-le-ciel-b .6s {EASE_BACK} both", {"montre-le-ciel-b": "from{transform:rotate(104deg)} to{transform:rotate(4deg)}"}),
    anim("montre-le-ciel", ".arm", "a", "2s", "0%,100%{transform:rotate(-118deg)} 50%{transform:rotate(-112deg)}"),
    anim("montre-le-ciel", ".head", "h", "2s", "0%,100%{transform:rotate(14deg)} 50%{transform:rotate(18deg)}"),
    anim("montre-le-ciel", ".torso", "t", "2s", "0%,100%{transform:rotate(4deg)} 50%{transform:rotate(6deg)}"),
    (".st", f"montre-le-ciel-s .8s {EASE_BACK} .4s both, montre-le-ciel-tw 1.6s ease-in-out 1.2s infinite", {
        "montre-le-ciel-s": "from{transform:scale(0) rotate(-180deg)} to{transform:scale(1) rotate(0)}",
        "montre-le-ciel-tw": "0%,100%{transform:scale(1) rotate(0)} 50%{transform:scale(1.15) rotate(12deg)}"}),
], after=etoile)

# ---------------------------------------------------------------- poses pour la vidéo
# 73. Prof : toque sur la tête, montre du doigt, l'autre main explique ---------------------
pose2("prof", "Prof", "Cours, masterclass, explication", [
    anim("prof", ".arm", "a", "2.4s", "0%,100%{transform:rotate(-64deg)} 50%{transform:rotate(-56deg)}"),
    anim("prof", ".arm2", "b", ".8s", "from{transform:rotate(-40deg)} to{transform:rotate(-8deg)}", "ease-in-out infinite alternate"),
    anim("prof", ".head", "h", "2.4s", "0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(4deg)}"),
    anim("prof", ".torso", "t", "2.4s", "0%,100%{transform:rotate(-3deg)} 50%{transform:rotate(0)}"),
    (".cap", "prof-c 2.4s ease-in-out infinite", {"prof-c": "0%,100%{transform:rotate(-12deg)} 50%{transform:rotate(-6deg)}"}),
], head_inner=g((10, -20), "cap", CAP))

# 74. Lit assise : assise par terre, la revue ouverte sur les genoux -----------------------
pose2("lit-assise", "Lit assise", "Lecture d'un cours, revue, détente", [
    anim("lit-assise", ".rig", "r", "3s", "0%,100%{transform:translateY(60px)} 50%{transform:translateY(64px) scale(1.01,.99)}"),
    anim("lit-assise", ".legl", "l", "1.4s", "from{transform:rotate(80deg)} to{transform:rotate(72deg)}", "ease-in-out infinite alternate"),
    anim("lit-assise", ".legr", "m", "1.4s", "from{transform:rotate(70deg)} to{transform:rotate(78deg)}", "ease-in-out infinite alternate"),
    anim("lit-assise", ".arm", "a", "3s", "0%,100%{transform:rotate(-22deg)} 50%{transform:rotate(-16deg)}"),
    anim("lit-assise", ".arm2", "b", "3s", "0%,100%{transform:rotate(-30deg)} 50%{transform:rotate(-36deg)}"),
    anim("lit-assise", ".head", "h", "3s", "0%,100%{transform:rotate(-10deg)} 50%{transform:rotate(-6deg)}"),
    (".pg", "lit-assise-p 3s ease-in-out 1s infinite backwards", {"lit-assise-p": "0%,45%{transform:scaleX(1)} 75%,100%{transform:scaleX(-1)}"}),
], before=COUSSIN, arm_inner=g(FIST, "book", f'<g transform="rotate(26) translate(0 40) scale(1.2)">{BOOK}</g>'))

# 75. Discute : les deux bras gesticulent, une bulle s'écrit ------------------------------
pose2("discute", "Discute", "Forum, échange avec la communauté", [
    anim("discute", ".arm", "a", "1.2s", "0%,100%{transform:rotate(-70deg)} 50%{transform:rotate(-30deg)}"),
    anim("discute", ".arm2", "b", "1.2s", "0%,100%{transform:rotate(-20deg)} 50%{transform:rotate(-56deg)}"),
    anim("discute", ".head", "h", ".6s", "from{transform:rotate(-5deg)} to{transform:rotate(5deg)}", "ease-in-out infinite alternate"),
    anim("discute", ".rig", "r", "1.2s", "0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)}"),
    (".bl", "discute-pop .5s {0} .2s both, discute-float 2.4s ease-in-out .7s infinite".format(EASE_BACK), {
        "discute-pop": "from{transform:scale(0);opacity:0} to{transform:scale(1);opacity:1}",
        "discute-float": "0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)}"}),
    (".l1,.l2,.l3", "discute-type 2.4s ease-out .5s infinite backwards", {"discute-type": "0%{stroke-dasharray:0 400} 40%,100%{stroke-dasharray:400 0}"}),
], extra_css=".mascotte-discute .l2 { animation-delay: .8s; } .mascotte-discute .l3 { animation-delay: 1.1s; }", after=g((330, -150), "bl", f'<g transform="scale(-.9 .9)">{BULLE}</g>'.replace('<path class="l', '<path class="l')))

# 76. Invite : montre le bouton et fait « viens ! » de l'autre main --------------------------
pose2("invite", "Invite", "Appel à l'action, « rejoins-nous ! »", [
    (".arm", f"invite-a .6s {EASE_BACK} both, invite-j 1.2s ease-in-out .6s infinite", {
        "invite-a": "from{transform:rotate(-104deg)} to{transform:rotate(-70deg)}",
        "invite-j": "0%,100%{transform:rotate(-70deg)} 50%{transform:rotate(-62deg)}"}),
    anim("invite", ".arm2", "b", ".5s", "from{transform:rotate(-6deg)} to{transform:rotate(-40deg)}", "ease-in-out infinite alternate"),
    anim("invite", ".torso", "t", "1.2s", "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(-3deg)}"),
    anim("invite", ".rig", "r", "1.2s", "0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)}"),
    anim("invite", ".legl", "l", "1.2s", "0%,100%{transform:rotate(24deg)} 50%{transform:rotate(16deg)}"),
])

# 77. Muscles : montre ses biceps, gonfle le torse --------------------------------------
pose2("muscles", "Muscles", "Progrès, force, « tu deviens fort ! »", [
    anim("muscles", ".arm", "a", "1.2s", "0%,100%{transform:rotate(-52deg)} 50%{transform:rotate(-46deg)}"),
    anim("muscles", ".fa", "c", "1.2s", "0%,100%{transform:rotate(48deg)} 50%{transform:rotate(80deg)}"),
    anim("muscles", ".arm2", "b", "1.2s", "0%,100%{transform:rotate(122deg)} 50%{transform:rotate(118deg)}"),
    anim("muscles", ".fa2", "d", "1.2s", "0%,100%{transform:rotate(76deg)} 50%{transform:rotate(80deg)}"),
    anim("muscles", ".torso", "t", "1.2s", "0%,100%{transform:scale(1)} 50%{transform:scale(1.04,1.02) translateY(-10px)}"),
    anim("muscles", ".head", "h", "1.2s", "0%,100%{transform:rotate(-4deg)} 50%{transform:rotate(4deg)}"),
], after="".join(g(p, f"sp sp{i}", sparkle(.8)) for i, p in enumerate([(160, 420), (1000, 420)])),
   extra_css=".mascotte-muscles .sp { animation: muscles-sp 1.2s ease-in-out infinite; } @keyframes muscles-sp { 0%,100%{transform:scale(0)} 50%{transform:scale(1) rotate(45deg)} }")

# 78. Boxe : enchaîne les directs, en garde ---------------------------------------------
pose2("boxe", "Boxe", "Attaque, combinaison, « frappe fort »", [
    anim("boxe", ".arm", "a", ".8s", "0%,40%,100%{transform:rotate(-80deg)} 20%{transform:rotate(-62deg)}"),
    anim("boxe", ".fa", "c", ".8s", "0%,40%,100%{transform:rotate(100deg)} 20%{transform:rotate(-6deg)}"),
    anim("boxe", ".arm2", "b", ".8s", "0%,50%,90%,100%{transform:rotate(-30deg)} 70%{transform:rotate(-50deg)}"),
    anim("boxe", ".fa2", "d", ".8s", "0%,50%,90%,100%{transform:rotate(100deg)} 70%{transform:rotate(30deg)}"),
    anim("boxe", ".rig", "r", ".4s", "from{transform:translateY(0)} to{transform:translateY(-14px)}", "ease-in-out infinite alternate"),
    anim("boxe", ".torso", "t", ".8s", "0%,40%,100%{transform:rotate(-4deg)} 20%{transform:rotate(-12deg)} 70%{transform:rotate(-8deg)}"),
    anim("boxe", ".legl", "l", ".4s", "from{transform:rotate(22deg)} to{transform:rotate(16deg)}", "ease-in-out infinite alternate"),
    anim("boxe", ".legr", "m", ".4s", "from{transform:rotate(-26deg)} to{transform:rotate(-20deg)}", "ease-in-out infinite alternate"),
])

# 79. Menton : réfléchit, la main sous le menton (enfin possible grâce au coude) -----------
pose2("menton", "Main sous le menton", "Réflexion, problème du jour, « à ton avis ? »", [
    anim("menton", ".arm", "a", "3s", "0%,100%{transform:rotate(-64deg)} 50%{transform:rotate(-60deg)}"),
    anim("menton", ".fa", "c", "3s", "0%,100%{transform:rotate(84deg)} 50%{transform:rotate(80deg)}"),
    anim("menton", ".arm2", "b", "3s", "0%,100%{transform:rotate(104deg)} 50%{transform:rotate(100deg)}"),
    anim("menton", ".fa2", "d", "3s", "0%,100%{transform:rotate(60deg)} 50%{transform:rotate(66deg)}"),
    anim("menton", ".head", "h", "3s", "0%,100%{transform:rotate(-6deg)} 50%{transform:rotate(-10deg)}"),
], after=g((930, -120), "bub", f'<circle cx="-200" cy="170" r="22" fill="#fff" stroke="{INK}" stroke-width="9"/><circle cx="-150" cy="110" r="34" fill="#fff" stroke="{INK}" stroke-width="9"/><ellipse rx="160" ry="95" fill="#fff" stroke="{INK}" stroke-width="10"/>' + "".join(g((x, 0), f"dt dt{i}", f'<circle r="26" fill="{INK}"/>') for i, x in enumerate([-70, 0, 70]))),
   extra_css=".mascotte-menton .dt { animation: menton-dt 1.2s ease-in-out infinite backwards; } @keyframes menton-dt { 0%,60%,100%{transform:translateY(0)} 30%{transform:translateY(-34px)} } .mascotte-menton .dt1 { animation-delay: .18s; } .mascotte-menton .dt2 { animation-delay: .36s; }")

# ---------------------------------------------------------------- versions miroir
# Chaque animation existe aussi tournée vers la droite : tout le dessin est retourné
# autour de l'axe vertical du cadre, sauf les textes (« ? », « Z ») remis à l'endroit.
def miroir(name, s):
    head, rest = s.split("</style>\n", 1)
    body, tail = rest.rsplit("\n</svg>", 1)
    body = body.replace("<text ", '<text transform="scale(-1 1)" ')
    head = head.replace(f'class="mascotte mascotte-{name}"', f'class="mascotte mascotte-{name} mascotte-miroir"', 1)
    head = head.replace('aria-label="', 'aria-label="(miroir) ', 1)
    return head + "</style>\n" + f'<g transform="translate(1080 0) scale(-1 1)">{body}</g>' + "\n</svg>" + tail


for name in list(A):
    title, usage, s_ = A[name]
    A[name + "-miroir"] = (title + " (miroir)", usage + " — tournée vers la droite", miroir(name, s_))


# ---------------------------------------------------------------- sorties
# Trois déclinaisons : noir (sur les cartes colorées), blanc et jaune (sur fond sombre)
VARIANTS = {"noir": (INK, INK), "blanc": ("#ffffff", YELLOW), "jaune": (YELLOW, "#ffffff")}
os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
for name, (title, usage, s) in A.items():
    open(os.path.join(OUT, "svg", f"mascotte-{name}.svg"), "w", encoding="utf-8").write(s)
    for v, (m, l) in VARIANTS.items():
        os.makedirs(os.path.join(OUT, "svg", v), exist_ok=True)
        base = name.removesuffix("-miroir")
        base_rule = f".mascotte-{base} {{ --mascot: {INK}; --line: {INK}; }}"
        assert base_rule in s
        sv = s.replace(base_rule, f".mascotte.mascotte-{name}-{v} {{ --mascot: {m}; --line: {l}; }}")
        sv = sv.replace(f'class="mascotte mascotte-{base}', f'class="mascotte mascotte-{name}-{v} mascotte-{base}', 1)
        open(os.path.join(OUT, "svg", v, f"mascotte-{name}-{v}.svg"), "w", encoding="utf-8").write(sv)

# Galerie de prévisualisation : une ligne par animation, une colonne par couleur
rows = []
for name, (title, usage, s_) in A.items():
    cells = []
    for v, bg in (("noir", YELLOW), ("blanc", "#1f1f1f"), ("jaune", "#1f1f1f")):
        sv = open(os.path.join(OUT, "svg", v, f"mascotte-{name}-{v}.svg"), encoding="utf-8").read()
        cells.append(f'<figure style="background:{bg}"><div class="art">{sv}</div><code>svg/{v}/mascotte-{name}-{v}.svg</code></figure>')
    rows.append(f'<section><h2>{title}<span>{usage}</span></h2><div class="row">{"".join(cells)}</div></section>')
html = f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mascotte animée</title>
<style>
body {{ margin:0; background:#f1f0ea; color:#1b1b1b; font:16px/1.4 system-ui, sans-serif; }}
header, main {{ max-width:1100px; margin:auto; padding:24px 16px 0; }}
h1 {{ margin:0 0 6px; font-size:28px; }} header p {{ margin:0; color:#555; }}
button {{ font:inherit; margin-top:14px; padding:8px 14px; border-radius:999px; border:1px solid #1b1b1b; background:#fff; cursor:pointer; }}
section {{ margin:28px 0; }} h2 {{ font-size:20px; margin:0 0 10px; display:flex; gap:12px; align-items:baseline; flex-wrap:wrap; }} h2 span {{ font-size:14px; color:#555; font-weight:500; }}
.row {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:12px; }}
figure {{ margin:0; border-radius:20px; padding:12px; }} .art svg {{ width:100%; height:auto; display:block; }}
figure code {{ display:block; font-size:11px; color:#777; word-break:break-all; margin-top:6px; }}
@media (max-width:640px) {{ .row {{ grid-template-columns:1fr; }} }}
</style></head><body>
<header><h1>Mascotte echecs.com — animations</h1><p>{len(A)} animations ({len(A) // 2} poses, chacune aussi en miroir) × 3 couleurs (noir, blanc, jaune). SVG animés en CSS, sans script.</p>
<button onclick="document.querySelectorAll('.art').forEach(a=>a.innerHTML=a.innerHTML)">Rejouer les intros</button></header>
<main>{"".join(rows)}</main></body></html>'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)

# Pour la vidéo : SVG en chaînes JS
open(os.path.join(ROOT, "video", "assets", "mascot", "poses.js"), "w", encoding="utf-8").write(
    "// Généré par site-animations/generate.py\nwindow.MASCOT_POSES = " + json.dumps({k: v[2] for k, v in A.items()}, ensure_ascii=False) + ";\n")
print(len(A), "animations →", os.path.join(OUT, "svg"))
