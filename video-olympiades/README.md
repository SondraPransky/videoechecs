# Olympiades 2026, ronde 9 — résumé vidéo Europe Échecs

Résumé en motion design de 2 min (1920×1080, 30 i/s, musique seule) de l'article
d'Europe Échecs **« La France frôle l'exploit, belle journée pour l'Ouzbékistan »**
(Pierre Verdon, 25/09/2026) :
https://www.europe-echecs.com/art/olympiades-2026-ronde-9-10085.html

Fichiers produits :
- `build/olympiades-2026-ronde-9.mp4` : la vidéo ;
- `build/poster.jpg` : l'image d'affiche.

Marque : logo Europe Échecs (`../assets/brand/logo-europe-echecs.png`), en filigrane
puis en grand sur le plan final. Pas de mascotte : c'est un format actualité.

## Scénario

| # | Scène | Durée | Contenu |
|---|---|---|---|
| 1 | Titre | 8 s | « La France frôle l'exploit », Samarcande, crédit de l'article |
| 2 | En bref | 10 s | Ouzbékistan–États-Unis, Inde–Allemagne, Ouzbékistan 2–Pays-Bas, France–Chine |
| 3 | France 2–2 Chine | 9 s | Les quatre échiquiers, Elo, ouvertures, nombre de coups |
| 4 | Wei Yi – Lagarde (1) | 22 s | 22… Tf2 à 28… Dxd6 : l'échange dame contre deux tours |
| 5 | Wei Yi – Lagarde (2) | 20 s | 64. Td2 à 70… Rg5 : le piège et l'échec perpétuel, puis 82. Txf3 !! |
| 6 | Féminines | 18 s | France 2,5–1,5 Serbie, 17. Tb1 à 19. Df3 (Daulyte-Cornette – Injac) |
| 7 | Gukesh | 12 s | Donchenko – Gukesh, 51. Fe2 à 54… Dd2 |
| 8 | Classements | 12 s | Mixte et féminin après la ronde 9 |
| 9 | Final | 9 s | « Deux rondes à jouer », logo Europe Échecs |

## D'où viennent les données

- **Textes, scores, classements** : tous tirés de l'article (`data/contenu.json`).
  Pour le classement mixte, l'article cite l'Ouzbékistan en tête et l'Inde à un
  point ; les autres lignes (Ouzbékistan 2, Arménie, France 7e à 14) viennent du
  classement officiel sur chess-results.
- **Coups animés** : les PGN de la diffusion officielle (lichess, échiquiers 1 à 12)
  pour France–Chine et Donchenko–Gukesh. La partie Daulyte-Cornette – Injac est
  reconstruite depuis les coups donnés en entier dans l'article, et sa légalité est
  vérifiée par chess.js. Les coups cités par l'article correspondent tous au PGN,
  à une exception près : pour 70. l'article écrit Tg2+, le PGN donne Th2+. La
  vidéo anime le PGN.

## Générer la vidéo

Prérequis : Node 18+, Python 3 et Chromium (Playwright), puis :

```bash
npm install
pip install imageio-ffmpeg numpy scipy
bash build.sh
```

`build.sh` enchaîne : PGN → `src/parties.js` (coups résolus par chess.js),
découpage → `src/timing.js` et `src/contenu.js`, musique (`audio/music.py`, générée
par code, donc libre de droits), rendu image par image, puis assemblage.

## Modifier

- **Textes, légendes, fenêtres de coups** : `data/contenu.json`. Chaque scène de
  partie a `de` et `a` (indices de demi-coups, 0 = 1. blancs), `pas` (secondes par
  demi-coup) et ses `legendes` accrochées à un demi-coup (`ply`).
- **Durées des scènes** : `scripts/timing.py` (multiples de 0,5 s, un temps à 120 BPM).
- **Mise en page et animation** : `src/index.html`.

Pour vérifier quelques images sans tout rendre :

```bash
python3 scripts/timing.py && node scripts/parties.mjs
node render.mjs build/apercu --frames 3,22,35,58,78,93,105,116
```
