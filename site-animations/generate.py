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


# ---------------------------------------------------------------- sorties
# Trois déclinaisons : noir (sur les cartes colorées), blanc et jaune (sur fond sombre)
VARIANTS = {"noir": (INK, INK), "blanc": ("#ffffff", YELLOW), "jaune": (YELLOW, "#ffffff")}
os.makedirs(os.path.join(OUT, "svg"), exist_ok=True)
for name, (title, usage, s) in A.items():
    open(os.path.join(OUT, "svg", f"mascotte-{name}.svg"), "w", encoding="utf-8").write(s)
    for v, (m, l) in VARIANTS.items():
        os.makedirs(os.path.join(OUT, "svg", v), exist_ok=True)
        base_rule = f".mascotte-{name} {{ --mascot: {INK}; --line: {INK}; }}"
        assert base_rule in s
        sv = s.replace(base_rule, f".mascotte.mascotte-{name}-{v} {{ --mascot: {m}; --line: {l}; }}")
        sv = sv.replace(f'class="mascotte mascotte-{name}"', f'class="mascotte mascotte-{name} mascotte-{name}-{v}"')
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
<header><h1>Mascotte echecs.com — animations</h1><p>13 animations × 3 couleurs (noir, blanc, jaune). SVG animés en CSS, sans script.</p>
<button onclick="document.querySelectorAll('.art').forEach(a=>a.innerHTML=a.innerHTML)">Rejouer les intros</button></header>
<main>{"".join(rows)}</main></body></html>'''
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(html)

# Pour la vidéo : SVG en chaînes JS
open(os.path.join(ROOT, "video", "assets", "mascot", "poses.js"), "w", encoding="utf-8").write(
    "// Généré par site-animations/generate.py\nwindow.MASCOT_POSES = " + json.dumps({k: v[2] for k, v in A.items()}, ensure_ascii=False) + ";\n")
print(len(A), "animations →", os.path.join(OUT, "svg"))
