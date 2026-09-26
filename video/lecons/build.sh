#!/usr/bin/env bash
# Leçon vidéo complète à partir de lecons/<nom>/lecon.mjs :
# texte → voix off → chronologie → bruitages et mixage → rendu image par image → MP4.
#
#   bash lecons/build.sh jobava                   # voix Piper (maquette gratuite)
#   bash lecons/build.sh jobava --eleven ID       # voix ElevenLabs (ID de voix)
#   bash lecons/build.sh jobava --clone ref.wav   # voix clonée (Chatterbox, voir voix.py)
#   options : --skip-render (garde la vidéo muette), --workers n (rendu parallèle, 4 par défaut)
set -euo pipefail
cd "$(dirname "$0")/.."
NAME=${1:?nom de la leçon}; shift
VOICE=(); SKIP_RENDER=0; WORKERS=4
while [ $# -gt 0 ]; do case "$1" in
  --eleven) VOICE+=(--eleven --voice "$2"); shift;;
  --clone) VOICE+=(--clone "$2"); shift;;
  --skip-render) SKIP_RENDER=1;;
  --workers) WORKERS=$2; shift;;
esac; shift; done
OUT=build/lecons/$NAME
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')

node lecons/build.mjs "$NAME" plan
python3 lecons/voix.py "$NAME" ${VOICE[@]+"${VOICE[@]}"}
node lecons/build.mjs "$NAME" timing
python3 lecons/mix.py "$NAME"
[ "$SKIP_RENDER" = 1 ] && [ -f "$OUT/video-muette.mp4" ] || \
  node render.mjs "$OUT/video-muette.mp4" --page "lecons/player.html?l=$NAME" --workers "$WORKERS" --crf 20
"$FFMPEG" -y -loglevel error -i "$OUT/video-muette.mp4" -i "$OUT/mix.wav" -c:v copy -c:a aac -b:a 160k -shortest -movflags +faststart "$OUT/lecon-$NAME.mp4"
"$FFMPEG" -y -loglevel error -ss 60 -i "$OUT/video-muette.mp4" -frames:v 1 -q:v 2 "$OUT/affiche.jpg"
echo "OK → $OUT/lecon-$NAME.mp4"
