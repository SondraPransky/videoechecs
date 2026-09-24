#!/usr/bin/env bash
# Chaîne complète : voix off → découpage des scènes → musique → rendu image par image → mixage → MP4.
# Options : --music-only (sans voix off), --skip-voice (garde voice/out), --skip-render (garde build/video-muette.mp4)
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
mkdir -p build
SKIP_VOICE=0; SKIP_RENDER=0; MUSIC_ONLY=0
for a in "$@"; do case "$a" in --skip-voice) SKIP_VOICE=1;; --skip-render) SKIP_RENDER=1;; --music-only) MUSIC_ONLY=1; SKIP_VOICE=1;; esac; done

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
if [ "$MUSIC_ONLY" = 1 ]; then python3 scripts/timing.py --music-only; else python3 scripts/timing.py; fi
python3 audio/music.py
[ "$MUSIC_ONLY" = 1 ] || python3 scripts/captions.py

# 3. Mixage : répliques placées selon build/timing.json, musique « pompée » par la voix
TOTAL=$(python3 -c "import json;print(json.load(open('build/timing.json'))['total'])")
if [ "$MUSIC_ONLY" = 1 ]; then
  "$FFMPEG" -y -loglevel error -i audio/music.wav -af loudnorm=I=-14:TP=-1.2:LRA=9 -ar 48000 -t "$TOTAL" build/mix.wav
else
inputs=(); filters=""; labels=""; i=0
while read -r id at; do
  inputs+=(-i "voice/out/$id.wav")
  filters+="[$i:a]aresample=48000,aformat=channel_layouts=mono,adelay=$(python3 -c "print(int($at*1000))")[v$i];"
  labels+="[v$i]"; i=$((i+1))
done < <(python3 -c "import json;[print(v['id'],v['at']) for v in json.load(open('build/timing.json'))['vo']]")
filters+="${labels}amix=inputs=$i:normalize=0,apad=whole_dur=$TOTAL,highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,volume=1.6,pan=stereo|c0=c0|c1=c0,asplit=2[vo][sc];"
filters+="[$i:a]volume=0.5[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=5:attack=15:release=300[duck];"
filters+="[duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-15:TP=-1.5:LRA=9[out]"
"$FFMPEG" -y -loglevel error "${inputs[@]}" -i audio/music.wav -filter_complex "$filters" -map "[out]" -ar 48000 -t "$TOTAL" build/mix.wav
fi

# 4. Rendu de l'image puis assemblage
[ "$SKIP_RENDER" = 1 ] && [ -f build/video-muette.mp4 ] || node render.mjs build/video-muette.mp4
"$FFMPEG" -y -loglevel error -i build/video-muette.mp4 -i build/mix.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart build/echecs-academie-presentation.mp4
"$FFMPEG" -y -loglevel error -sseof -2 -i build/video-muette.mp4 -frames:v 1 -q:v 2 build/poster.jpg
echo "OK → build/echecs-academie-presentation.mp4 (${TOTAL}s)"
