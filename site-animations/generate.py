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
<g transform="translate(12 -450)"><g class="flag"><path d="M0,0 L300,0 L300,210 L0,210 Z" fill="#fff" stroke="{LINE}" stroke-width="10"/>
{"".join(f'<rect x="{(k % 6) * 50}" y="{(k // 6) * 52.5}" width="50" height="52.5" fill="{LINE}"/>' for k in range(24) if (k + k // 6) % 2 == 0)}</g></g></g>'''

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
