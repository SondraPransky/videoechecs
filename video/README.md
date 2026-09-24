# Vidéo de présentation — echecs.com Académie

Vidéo motion design de 62 s (1920×1080, 30 i/s), voix off masculine en français, musique originale.
Le fichier final est `build/echecs-academie-presentation.mp4`, avec son image d'affiche `build/poster.jpg` et ses sous-titres `build/sous-titres.vtt`.

## Scénario

| # | Temps | Scène | Voix off |
|---|---|---|---|
| 1 | 0–7 s | L'échiquier se met en place, 1.e4 e5 | « Les échecs, ça s'apprend. Pas à pas. » |
| 2 | 7–14,5 s | Parcours Débutant → Club, le pion est promu en dame | « Du tout premier coup jusqu'au niveau club… » |
| 3 | 14,5–25 s | +200 leçons, 4 formats (vidéo, cours écrit, exercice, quiz), captures réelles | « Plus de deux cents leçons interactives… » |
| 4 | 25–32 s | Cours en direct, MI & GMI | « Des cours en direct, avec des Maîtres Internationaux… » |
| 5 | 32–39 s | Partie rejouée et annotée, barre d'évaluation | « Enregistrez vos parties, et analysez-les… » |
| 6 | 39–45,5 s | +2 000 exercices, capture réelle du problème du jour | « Entraînez-vous avec plus de deux mille exercices. » |
| 7 | 45,5–52,5 s | Tournoi 10'+5", pendule, classement | « Et mesurez-vous aux autres joueurs… » |
| 8 | 52,5–62 s | Logo echecs.com, « Commencer maintenant », echecs.com/academie | « echecs.com. L'académie d'échecs. Commencez maintenant. » |

## Modifier puis relancer le rendu

Prérequis : Node 18+, Python 3, Chromium (Playwright), puis :

```bash
npm install
pip install piper-tts imageio-ffmpeg numpy
```

- **Textes à l'écran, couleurs, timing** : `src/index.html`. Les couleurs sont dans `:root` et la timeline GSAP est en bas du fichier, découpée par scène.
- **Voix off** : `voice/script.txt`, une réplique par ligne. Supprimez `voice/out/` pour la régénérer. Les départs de chaque réplique sont dans `build.sh` (`AT`).
- **Musique** : `audio/music.py`, générée par code, donc libre de droits.
- **Captures réelles de la plateforme** : `assets/captures/`. Les pièces d'échecs viennent du site : `assets/pieces/`.

```bash
rm -f build/video-muette.mp4   # forcer un nouveau rendu de l'image
bash build.sh                  # voix → musique → rendu → mixage → MP4
node render.mjs build/apercu --frames 5,20,59   # images fixes pour vérifier une scène
```

Pour intégrer une voix enregistrée par un comédien, remplacez les fichiers `voice/out/NN.wav` en gardant les mêmes noms, puis relancez `bash build.sh`.
