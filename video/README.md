# Vidéo de présentation — echecs.com Académie

Vidéo en motion design de 47 s (1920×1080, 30 i/s), en musique seule : électro-pop originale à 120 BPM, avec les coupes calées sur les temps. Elle présente la mascotte du site et de vraies captures de la plateforme et d'Europe Échecs.

Fichiers produits :
- `build/echecs-academie-presentation.mp4` : la vidéo finale ;
- `build/poster.jpg` : l'image d'affiche.

## Scénario

| # | Scène | Contenu | Mascotte |
|---|---|---|---|
| 1 | Pas à pas | L'échiquier se met en place, 1.e4 e5 | « hello » (animation du designer) |
| 2 | Progression | Débutant → Club, promotion en dame | Niveau supérieur (escalier) |
| 3 | Leçons | +200 leçons, 4 formats (vidéo, cours, exercice, quiz) | Lecture |
| 4 | Revue Europe Échecs | Numéro du mois en PGN, leçons d'Igor Nataf et Romuald De Labaca, thèmes | Leçon terminée |
| 5 | Vidéos Europe Échecs | Lecteur HD (Marc Quenehen), fiches auteurs en couleur (Nataf, De Labaca, Quenehen, Ravot), carrousel des séries | — |
| 6 | Cours en direct | MI & GMI | — |
| 7 | Tes parties | Partie rejouée en notation figurine, puis le lecteur PGN Europe Échecs recoloré aux couleurs de l'académie (import, bases, analyse) | Réflexion |
| 8 | Exercices et quiz | Exercice Objectif 1400, quiz Objectif 1600 | Bonne réponse (pirouette) |
| 9 | Tournois | 10'+5", « Toi » passe premier | Victoire en tournoi |
| 10 | Final | Logo, « Commencer maintenant », echecs.com/academie | Regarde ! (montre le bouton) |

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
