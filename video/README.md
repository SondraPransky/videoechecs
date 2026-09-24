# Vidéo de présentation — echecs.com Académie

Vidéo en motion design d'environ 40 s (1920×1080, 30 i/s), avec voix off masculine au tutoiement, musique électro-pop originale à 120 BPM et la mascotte du site.

Fichiers produits :
- `build/echecs-academie-presentation.mp4` : la vidéo finale ;
- `build/poster.jpg` : l'image d'affiche ;
- `build/sous-titres.vtt` : les sous-titres.

## Scénario

La durée de chaque scène est **calculée à partir de la voix off** (`scripts/timing.py`). Les coupes tombent sur les temps de la musique.

| # | Scène | Voix off | Mascotte |
|---|---|---|---|
| 1 | L'échiquier se met en place, 1.e4 e5 | « Les échecs, ça s'apprend. Pas à pas. » | « hello » (animation du designer) |
| 2 | Parcours Débutant → Club, promotion en dame | « Du premier coup jusqu'au niveau club… » | — |
| 3 | +200 leçons, 4 formats, captures réelles | « Plus de deux cents leçons interactives… » | Leçon terminée |
| 4 | Cours en direct, MI & GMI | « Des cours en direct avec des Maîtres Internationaux… » | — |
| 5 | Partie rejouée et annotée | « Enregistre tes parties. Analyse chaque coup. » | Réflexion |
| 6 | +2 000 exercices, problème du jour | « Plus de deux mille exercices pour progresser. » | Bonne réponse |
| 7 | Tournoi 10'+5", « Toi » passe premier | « Et des tournois en ligne pour te mesurer aux autres. » | Victoire en tournoi |
| 8 | Logo, « Commencer maintenant », echecs.com/academie | « echecs.com. L'académie d'échecs. Commence maintenant ! » | Regarde ! (montre le bouton) |

## Générer la vidéo

Prérequis : Node 18+, Python 3 et Chromium (Playwright), puis :

```bash
npm install
pip install piper-tts imageio-ffmpeg numpy scipy
```

La commande suivante enchaîne voix off, découpage, musique, rendu et mixage :

```bash
bash build.sh
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
