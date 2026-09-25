#!/usr/bin/env bash
# Chaîne complète : parties (PGN → JS) → découpage des scènes → musique → rendu
# image par image → mixage → MP4.
# Options : --skip-render (garde build/video-muette.mp4)
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
mkdir -p build
SKIP_RENDER=0
for a in "$@"; do case "$a" in --skip-render) SKIP_RENDER=1;; esac; done

# 1. Les coups animés sont résolus une fois pour toutes depuis les PGN
node scripts/parties.mjs

# 2. Découpage des scènes, puis musique calée sur le découpage
python3 scripts/timing.py
python3 audio/music.py

# 3. Musique seule : pas de voix off, donc pas de mixage à faire
TOTAL=$(python3 -c "import json;print(json.load(open('build/timing.json'))['total'])")
"$FFMPEG" -y -loglevel error -i audio/music.wav -af loudnorm=I=-14:TP=-1.2:LRA=9 \
  -ar 48000 -t "$TOTAL" build/mix.wav

# 4. Rendu de l'image puis assemblage
[ "$SKIP_RENDER" = 1 ] && [ -f build/video-muette.mp4 ] || node render.mjs build/video-muette.mp4
"$FFMPEG" -y -loglevel error -i build/video-muette.mp4 -i build/mix.wav \
  -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart \
  build/olympiades-2026-ronde-9.mp4
"$FFMPEG" -y -loglevel error -sseof -2 -i build/video-muette.mp4 -frames:v 1 -q:v 2 build/poster.jpg
echo "OK → build/olympiades-2026-ronde-9.mp4 (${TOTAL}s)"
