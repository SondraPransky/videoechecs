#!/usr/bin/env bash
# Présentation courte en vrai format vertical 9:16 (src/index.html?fmt=v, scènes recomposées pour le mobile),
# avec le son de la version courte. Remplace dans le pack l'ancienne version « 16:9 dans un cadre ».
# Prérequis : build/echecs-academie-court.mp4 (bash build.sh --edition court).
set -euo pipefail
cd "$(dirname "$0")/.."
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
OUT=build/echecs-academie-court-9x16.mp4
node render.mjs build/video-muette-court-9x16.mp4 --edition court --size 1080x1920 --query fmt=v
"$FFMPEG" -y -loglevel error -i build/video-muette-court-9x16.mp4 -i build/echecs-academie-court.mp4 -map 0:v -map 1:a \
  -c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p -r 30 -c:a copy -shortest -movflags +faststart "$OUT"
[ -d build/pack/videos/00-general ] && cp "$OUT" build/pack/videos/00-general/presentation-courte-9x16-reels-tiktok-stories.mp4
echo "OK → $OUT"
