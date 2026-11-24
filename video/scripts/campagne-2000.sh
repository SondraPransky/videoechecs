#!/usr/bin/env bash
# Campagne « Jusqu'à 2000 et plus » : une vidéo par thème (avis de Samuel), sans voix off, en 4 formats.
#   accroche-7  leçons Objectif 1800        accroche-8  passe le cap des 2000
#   accroche-9  des Grands Maîtres          accroche-10 ton tournoi décortiqué
# 16:9 rendue par build.sh, puis placée dans un cadre aux couleurs de la marque (titre, logo) pour le 9:16, le 4:5 et le 1:1.
# Sorties : validation/campagne-2000/media/<nom>-{16x9,story-9x16,feed-4x5,carre-1x1}.mp4
# Usage : bash scripts/campagne-2000.sh [7 8 9 10]
set -euo pipefail
cd "$(dirname "$0")/.."
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
M=validation/campagne-2000/media
ENC=(-c:v libx264 -preset medium -crf 23 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart)
declare -A NOM=([7]=lecons-1800 [8]=cap-des-2000 [9]=grands-maitres [10]=tournoi-decortique)
# Titres courts : ils doivent tenir à côté du logo dans les cadres 4:5 et carré
declare -A TITRE=([7]="Cap sur|l'Objectif 1800." [8]="Passe le cap|des 2000 !" [9]="Avec des|Grands Maîtres." [10]="Ton tournoi,|décortiqué.")
LISTE=("$@"); [ ${#LISTE[@]} -gt 0 ] || LISTE=(7 8 9 10)
for k in "${LISTE[@]}"; do
  n=${NOM[$k]}; src=build/echecs-academie-accroche-$k.mp4; c=build/_cadres/campagne-$k
  [ "${CADRES_SEULS:-0}" = 1 ] && [ -f "$src" ] || bash build.sh --edition "accroche-$k"   # CADRES_SEULS=1 : refait seulement les formats à partir de la vidéo déjà rendue
  mkdir -p "$c"
  node scripts/social.mjs "$c" --cadres "${TITRE[$k]}" >/dev/null
  "$FFMPEG" -y -loglevel error -i "$src" "${ENC[@]}" "$M/$n-16x9.mp4"
  for f in "vertical 656 story-9x16" "portrait 300 feed-4x5" "carre 236 carre-1x1"; do
    set -- $f
    "$FFMPEG" -y -loglevel error -loop 1 -i "$c/cadre-$1.png" -i "$src" -filter_complex \
      "[1:v]scale=1080:608:flags=lanczos[v];[0:v][v]overlay=0:$2:shortest=1,format=yuv420p[out]" \
      -map "[out]" -map 1:a "${ENC[@]}" -shortest "$M/$n-$3.mp4"
  done
  echo "accroche-$k ($n) : OK"
done
python3 scripts/timing.py --music-only >/dev/null   # remet src/timing.js sur la version longue
ls -la "$M"/*.mp4
