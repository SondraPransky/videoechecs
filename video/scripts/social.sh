#!/usr/bin/env bash
# Kit réseaux sociaux dans build/reseaux/, à partir des vidéos déjà rendues :
#   bash build.sh --music-only ; bash build.sh --edition court ; bash build.sh --edition boucle ; bash scripts/social.sh
set -euo pipefail
cd "$(dirname "$0")/.."
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
O=build/reseaux
mkdir -p "$O"
COURT=build/echecs-academie-court.mp4
ENC=(-c:v libx264 -preset slow -crf 19 -pix_fmt yuv420p -r 30 -c:a aac -b:a 192k -movflags +faststart)

# 1. Images (affiche, post, story, bannière) et cadres des vidéos verticale et carrée
node scripts/social.mjs "$O"
node scripts/poster.mjs build/poster.jpg
"$FFMPEG" -y -loglevel error -i build/poster.jpg -vf scale=1600:900:flags=lanczos -q:v 2 "$O/x-post-1600x900.jpg"
"$FFMPEG" -y -loglevel error -i build/poster.jpg -vf scale=1280:720:flags=lanczos -q:v 2 "$O/youtube-miniature-1280x720.jpg"
"$FFMPEG" -y -loglevel error -i build/poster.jpg -vf "crop=1920:1005:0:38,scale=1200:630:flags=lanczos" -q:v 2 "$O/partage-lien-1200x630.jpg"

# 2. Vidéos de la version courte (~30 s)
cp "$COURT" "$O/video-16x9-x-youtube-linkedin.mp4"
"$FFMPEG" -y -loglevel error -loop 1 -i "$O/cadre-vertical.png" -i "$COURT" -filter_complex \
  "[1:v]scale=1080:608:flags=lanczos[v];[0:v][v]overlay=0:656:shortest=1,format=yuv420p[out]" \
  -map "[out]" -map 1:a "${ENC[@]}" -shortest "$O/video-9x16-reels-tiktok-stories.mp4"
"$FFMPEG" -y -loglevel error -loop 1 -i "$O/cadre-carre.png" -i "$COURT" -filter_complex \
  "[1:v]scale=1080:608:flags=lanczos[v];[0:v][v]overlay=0:236:shortest=1,format=yuv420p[out]" \
  -map "[out]" -map 1:a "${ENC[@]}" -shortest "$O/video-1x1-posts-instagram-x.mp4"

# 3. Boucle muette de l'en-tête du site (1920×1080 et 1280×720, plus légère)
cp build/echecs-academie-boucle.mp4 "$O/boucle-entete-site-1920x1080.mp4"
"$FFMPEG" -y -loglevel error -i build/echecs-academie-boucle.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -an -movflags +faststart "$O/boucle-entete-site-1280x720.mp4"
rm -f "$O/cadre-vertical.png" "$O/cadre-carre.png"
ls -la "$O"
