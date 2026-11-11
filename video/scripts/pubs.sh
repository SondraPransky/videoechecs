#!/usr/bin/env bash
# Publicités « v2 » de 16 s (src/pub.html) : question en grand, « Nous avons la solution ! »,
# la réponse propre à chaque question, l'appel final. Une musique différente par question (audio/pub_music.py) ;
# MUSIQUE=longue pour reprendre la musique de la vidéo longue (audio/music.py), calée sur les scènes de la pub.
# Formats : story 9:16, feed 4:5, carré 1:1 et 16:9 en thème nuit, plus une story en thème soleil (fond jaune).
# VARIANTES="carre:nuit" pour ne rendre que certains formats. Images fixes : node scripts/pub-images.mjs
# Sorties : build/pubs/ et build/pack/videos/00-publicites/. Usage : bash scripts/pubs.sh [numéros…]
set -euo pipefail
cd "$(dirname "$0")/.."
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
O=build/pubs; T=build/_pub; P=build/pack/videos/00-publicites
mkdir -p "$O" "$T" "$P"
SFX_VOL=${SFX_VOL:-0.3}
declare -A SIZE=([story]=1080x1920 [feed]=1080x1350 [carre]=1080x1080 [wide]=1920x1080)
declare -A NOM=([story]=story-9x16 [feed]=feed-4x5 [carre]=carre-1x1 [wide]=16x9)
NUMS=${*:-1 2 3 4 5}
for q in $NUMS; do
  DR=$([ "$q" = 1 ] && echo 1.2 || echo 0)   # pub 1 : « Nous avons la solution » plus long
  DUR=$(python3 -c "print(16 + $DR)")
  python3 -c "import json;d=$DR;json.dump({'total':16+d,'scenes':[{'id':'q','start':0},{'id':'r','start':3.9},{'id':'s','start':6.4+d},{'id':'c','start':12.6+d}]},open('$T/timing.json','w'))"
  if [ "${MUSIQUE:-styles}" = styles ]; then python3 audio/pub_music.py "$q" "$T/music-$q.wav" >/dev/null
  else TIMING_JSON="$T/timing.json" MUSIC_OUT="$T/music-$q.wav" python3 audio/music.py >/dev/null; fi
  node render.mjs --page pub.html --size 1080x1920 --query "q=$q" --sfx "$T/sfx-$q.json"
  TIMING_JSON="$T/timing.json" SFX_JSON="$T/sfx-$q.json" SFX_OUT="$T/sfx-$q.wav" python3 audio/sfx.py >/dev/null
  "$FFMPEG" -y -loglevel error -i "$T/music-$q.wav" -i "$T/sfx-$q.wav" -filter_complex \
    "[1:a]volume=$SFX_VOL[fx];[0:a][fx]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[out]" -map "[out]" -ar 48000 -t "$DUR" "$T/mix-$q.wav"
  for v in ${VARIANTES:-story:nuit feed:nuit carre:nuit wide:nuit story:soleil}; do
    fmt=${v%%:*}; th=${v##*:}
    nom="pub-$q-${NOM[$fmt]}$([ "$th" = soleil ] && echo -jaune || true).mp4"
    node render.mjs "$T/v.mp4" --page pub.html --size "${SIZE[$fmt]}" --query "q=$q&fmt=$fmt&theme=$th" >/dev/null
    "$FFMPEG" -y -loglevel error -i "$T/v.mp4" -i "$T/mix-$q.wav" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$O/$nom"
    cp "$O/$nom" "$P/"
    echo "$nom : OK"
  done
done
ls -la "$O"
