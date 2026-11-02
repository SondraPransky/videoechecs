# Vidéo de présentation — echecs.com Académie

Vidéo en motion design de 56,5 s (1920×1080, 30 i/s), en musique seule : électro-pop originale à 120 BPM, avec les coupes calées sur les temps, et des bruitages d'interface (clics, « pop », validations, notifications, compteurs, pièces posées). Elle présente la mascotte du site et de vraies captures de la plateforme et d'Europe Échecs.

Fichiers produits :
- `build/echecs-academie-presentation.mp4` : la vidéo finale ;
- `build/poster.jpg` : l'image d'affiche.

## Scénario

| # | Scène | Contenu | Mascotte |
|---|---|---|---|
| 1 | Pas à pas | « Les échecs, ça s'apprend. Pas à pas. Du premier coup à plus de 2000. » : 1.e4 e5 sur l'échiquier, puis le pion parcourt Initiation → Objectif 1400, 1600, 1800 → 2000 et + et devient dame | « hello » (animation du designer) |
| 2 | Leçons | +200 leçons, 4 formats (vidéo, cours, exercice, quiz) | Idée (ampoule) |
| 3 | Exercices et quiz | Exercice Objectif 1400, quiz Objectif 1600 | Bonne réponse (pirouette) |
| 4 | Mesure tes progrès | Barre de validation d'un module (Objectif 1400) qui se remplit, « Validé », 3 étoiles, courbe Elo qui monte de 1150 à 1480 | Série réussie |
| 5 | Vidéos Europe Échecs | Lecteur HD (Marc Quenehen), fiches auteurs en couleur (Nataf, De Labaca, Quenehen, Ravot), carrousel des séries | — |
| 6 | Masterclasses en direct | « Masterclasses avec des pros » : direct (échiquier, caméra de Sylvain Ravot, question du chat), fiches de Sylvain Ravot, Marc Quenehen, Fabien Libiszewski et Gata Kamsky | Leçon terminée (toque) |
| 7 | Tes parties | Saisie coup par coup en notation figurine, puis import d'un PGN, analyse dans le lecteur Europe Échecs recoloré et partage avec d'autres membres (6 s) | Réflexion |
| 8 | Revue Europe Échecs | Numéro du mois (n°779, octobre 2026) en PGN, leçons d'Igor Nataf et Romuald De Labaca, thèmes | Lecture (blanche) |
| 9 | Forum | « Progresse en communauté » : forum echecs.com (logo echecs.com), sujet « Comment contrer la Sicilienne ? » qui reçoit des réponses, bulles de coachs | Série de jours (blanche) |
| 10 | Tournois | 10'+5", « Toi » passe premier | Victoire en tournoi |
| 11 | Final | Logo, « Commencer maintenant », echecs.com/academie | Regarde ! (montre le bouton) |

Pour la version musique seule, les durées de scène sont fixées dans `scripts/timing.py` (`MUSIC_ONLY`). Avec une voix off, elles sont calculées à partir des répliques.

## Générer la vidéo

Prérequis : Node 18+, Python 3 et Chromium (Playwright), puis :

```bash
npm install
pip install piper-tts imageio-ffmpeg numpy scipy
```

La commande suivante enchaîne voix off, découpage, musique, rendu et mixage :

```bash
bash build.sh --music-only   # version actuelle, sans voix off
bash build.sh                # avec voix off
```

### Voix ElevenLabs

1. Il faut `ELEVENLABS_API_KEY` dans l'environnement.
2. Choisissez une voix :
   ```bash
   python3 voice/elevenlabs.py --list
   ```
   Cette commande liste les voix françaises masculines.
3. Exportez `ELEVENLABS_VOICE_ID=<id>` puis lancez `bash build.sh`.

Sans ces deux variables, `build.sh` utilise la voix libre Piper, qui sert de maquette.

## Modifier

- **Textes à l'écran, couleurs, animations** : `src/index.html`. La timeline GSAP est découpée par scène, en temps local.
- **Voix off** : `voice/script.txt`, une réplique par scène. Les réglages ElevenLabs sont dans `voice/elevenlabs.py`.
- **Musique** : `audio/music.py`, générée par code, donc libre de droits.
- **Bruitages** : chaque scène note ses sons dans la timeline avec `sfx(st, type, t)` ; `node render.mjs --sfx build/sfx.json` exporte leurs instants et `audio/sfx.py` les synthétise (libres de droits). Le niveau se règle avec `SFX_VOL` (0.28 par défaut, discret) : `SFX_VOL=0.2 bash build.sh --music-only --skip-render`.
- **Mascottes** : `assets/mascot/` contient le `hello` du designer (Lottie) et `poses.js`, généré par `site-animations/generate.py`.
- **Captures réelles de la plateforme** : `assets/captures/`. Les pièces d'échecs viennent du site : `assets/pieces/`.

Pour vérifier une scène sans tout rendre :

```bash
node render.mjs build/apercu --frames 5,20,38
```

Pour refaire seulement le mixage, sans nouveau rendu de l'image :

```bash
bash build.sh --skip-voice --skip-render
```

## Crédits photo

- Fabien Libiszewski : Wolfgang Jekel, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:London_Chess_Classic_2016_Day5-19_(31872281495).jpg), CC BY 2.0, recadrée.
- Gata Kamsky : Stefan64, [Wikimedia Commons](https://commons.wikimedia.org/wiki/File:GataKamsky24.jpg), CC BY-SA 3.0, recadrée.

## Déclinaisons et réseaux sociaux

| Fichier | Usage |
|---|---|
| `build/poster.jpg` | Affiche de la vidéo (image avant lecture), générée par `src/poster.html` |
| `build/echecs-academie-court.mp4` | Version courte de 30,5 s : Pas à pas, Leçons, Valide chaque étape, Masterclasses, Forum, Final |
| `build/echecs-academie-boucle.mp4` | Boucle muette de 14 s pour l'en-tête du site : Leçons, Exercices, Valide chaque étape |
| `build/reseaux/video-9x16-reels-tiktok-stories.mp4` | Version courte en 1080×1920 (Reels, TikTok, Stories, Shorts) |
| `build/reseaux/video-1x1-posts-instagram-x.mp4` | Version courte en 1080×1080 (posts Instagram, X, Facebook, LinkedIn) |
| `build/reseaux/video-16x9-x-youtube-linkedin.mp4` | Version courte en 1920×1080 (X, YouTube, LinkedIn) |
| `build/reseaux/boucle-entete-site-*.mp4` | Boucle muette en 1920×1080 et 1280×720 (plus légère) |
| `build/reseaux/instagram-post-1080x1080.jpg` | Post carré |
| `build/reseaux/story-reel-tiktok-1080x1920.jpg` | Story, couverture de Reel ou de TikTok |
| `build/reseaux/x-post-1600x900.jpg` | Image de post X |
| `build/reseaux/banniere-x-linkedin-1500x500.jpg` | Bannière de profil X ou LinkedIn |
| `build/reseaux/youtube-miniature-1280x720.jpg` | Miniature YouTube |
| `build/reseaux/partage-lien-1200x630.jpg` | Aperçu de lien (Open Graph : Facebook, LinkedIn, WhatsApp) |

Pour tout régénérer :

```bash
bash build.sh --music-only       # version longue + affiche
bash build.sh --edition court    # version courte
bash build.sh --edition boucle   # boucle muette
bash scripts/social.sh           # kit réseaux sociaux
```

Les scènes de chaque déclinaison sont définies dans `scripts/timing.py` (`EDITIONS`). Les visuels sont dans `src/social.html` (un format par `?fmt=`). Les vidéos 9:16 et 1:1 placent la vidéo 16:9 dans un cadre aux couleurs de la marque, avec le logo, l'accroche et l'appel à l'action.
