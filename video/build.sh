#!/usr/bin/env bash
# Chaîne complète : voix off → découpage des scènes → musique → rendu image par image → mixage → MP4.
# Options : --music-only (sans voix off), --skip-voice (garde voice/out), --skip-render (garde la vidéo muette déjà rendue),
#           --edition court|boucle (déclinaison en musique seule, voir scripts/timing.py ; la boucle est muette)
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
mkdir -p build
SKIP_VOICE=0; SKIP_RENDER=0; MUSIC_ONLY=0; EDITION=long
args=("$@")
for ((k = 0; k < ${#args[@]}; k++)); do case "${args[k]}" in
  --skip-voice) SKIP_VOICE=1;; --skip-render) SKIP_RENDER=1;; --music-only) MUSIC_ONLY=1; SKIP_VOICE=1;;
  --edition) EDITION="${args[k+1]}"; MUSIC_ONLY=1; SKIP_VOICE=1;;
esac; done
case "$EDITION" in
  long) OUT=build/echecs-academie-presentation.mp4; MUTE=build/video-muette.mp4;;
  *) OUT=build/echecs-academie-$EDITION.mp4; MUTE=build/video-muette-$EDITION.mp4;;
esac

# 1. Voix off : ElevenLabs si une clé est disponible, sinon Piper (voix libre, maquette)
if [ "$SKIP_VOICE" = 0 ]; then
  if [ -n "${ELEVENLABS_API_KEY:-}" ] && [ -n "${ELEVENLABS_VOICE_ID:-}" ]; then
    python3 voice/elevenlabs.py
  else
    echo "ELEVENLABS_API_KEY / ELEVENLABS_VOICE_ID absents : voix Piper."
    bash voice/synth.sh
  fi
fi

# 2. Découpage des scènes calé sur la voix, puis musique calée sur le découpage
if [ "$MUSIC_ONLY" = 1 ]; then python3 scripts/timing.py --music-only --edition "$EDITION"; else python3 scripts/timing.py; fi
TOTAL=$(python3 -c "import json;print(json.load(open('build/timing.json'))['total'])")

# Boucle de l'en-tête du site : muette, pas de musique ni de bruitage
if [ "$EDITION" = boucle ]; then
  [ "$SKIP_RENDER" = 1 ] && [ -f "$MUTE" ] || node render.mjs "$MUTE" --edition boucle
  "$FFMPEG" -y -loglevel error -i "$MUTE" -c:v libx264 -preset slow -crf 22 -pix_fmt yuv420p -an -movflags +faststart "$OUT"
  python3 scripts/timing.py --music-only >/dev/null   # remet build/timing.json sur la version longue
  echo "OK → $OUT (${TOTAL}s, muette)"
  exit 0
fi

python3 audio/music.py
# Bruitages d'interface : instants lus dans la timeline de src/index.html, puis synthèse
node render.mjs --sfx build/sfx.json --edition "$EDITION"
python3 audio/sfx.py
if [ "$MUSIC_ONLY" = 1 ]; then [ "$EDITION" != long ] || rm -f build/sous-titres.vtt; else python3 scripts/captions.py; fi

# 3. Mixage : répliques placées selon build/timing.json, musique « pompée » par la voix
SFX_VOL=${SFX_VOL:-0.28}  # niveau des bruitages par rapport à la musique
if [ "$MUSIC_ONLY" = 1 ]; then
  "$FFMPEG" -y -loglevel error -i audio/music.wav -i build/sfx.wav -filter_complex "[1:a]volume=$SFX_VOL[fx];[0:a][fx]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[out]" -map "[out]" -ar 48000 -t "$TOTAL" build/mix.wav
else
inputs=(); filters=""; labels=""; i=0
while read -r id at; do
  inputs+=(-i "voice/out/$id.wav")
  filters+="[$i:a]aresample=48000,aformat=channel_layouts=mono,adelay=$(python3 -c "print(int($at*1000))")[v$i];"
  labels+="[v$i]"; i=$((i+1))
done < <(python3 -c "import json;[print(v['id'],v['at']) for v in json.load(open('build/timing.json'))['vo']]")
filters+="${labels}amix=inputs=$i:normalize=0,apad=whole_dur=$TOTAL,highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,volume=1.6,pan=stereo|c0=c0|c1=c0,asplit=2[vo][sc];"
filters+="[$i:a]volume=0.5[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300[duck];"
filters+="[$((i+1)):a]volume=$SFX_VOL[fx];[duck][vo][fx]amix=inputs=3:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9[out]"
"$FFMPEG" -y -loglevel error "${inputs[@]}" -i audio/music.wav -i build/sfx.wav -filter_complex "$filters" -map "[out]" -ar 48000 -t "$TOTAL" build/mix.wav
fi
[ "$EDITION" = long ] || cp build/mix.wav "build/mix-$EDITION.wav"

# 4. Rendu de l'image puis assemblage
[ "$SKIP_RENDER" = 1 ] && [ -f "$MUTE" ] || node render.mjs "$MUTE" --edition "$EDITION"
"$FFMPEG" -y -loglevel error -i "$MUTE" -i build/mix.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$OUT"
# Affiche dédiée (src/poster.html) pour la version longue
[ "$EDITION" = long ] && node scripts/poster.mjs build/poster.jpg
[ "$EDITION" = long ] || python3 scripts/timing.py --music-only >/dev/null   # remet build/timing.json sur la version longue
echo "OK → $OUT (${TOTAL}s)"
