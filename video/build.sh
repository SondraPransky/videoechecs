#!/usr/bin/env bash
# Chaîne complète : voix off → musique → rendu image par image → mixage → MP4 final.
set -euo pipefail
cd "$(dirname "$0")"
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
mkdir -p build

[ -f voice/out/08.wav ] || bash voice/synth.sh
[ -f audio/music.wav ] || python3 audio/music.py

# Départ de chaque réplique (secondes), calé sur les scènes de src/index.html
declare -A AT=( [01]=0.8 [02]=7.5 [03]=15.0 [04]=25.6 [05]=32.6 [06]=39.6 [07]=46.0 [08]=53.3 )

inputs=(); filters=""; labels=""
i=0
for id in 01 02 03 04 05 06 07 08; do
  inputs+=(-i "voice/out/$id.wav")
  ms=$(python3 -c "print(int(${AT[$id]}*1000))")
  filters+="[$i:a]aresample=48000,aformat=channel_layouts=mono,adelay=${ms}[v$i];"
  labels+="[v$i]"
  i=$((i+1))
done
filters+="${labels}amix=inputs=8:normalize=0,apad=whole_dur=62,highpass=f=80,acompressor=threshold=-18dB:ratio=3:attack=5:release=120,volume=1.6,pan=stereo|c0=c0|c1=c0,asplit=2[vo][sc];"
filters+="[8:a]volume=0.42[mu];[mu][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[duck];"
filters+="[duck][vo]amix=inputs=2:normalize=0,loudnorm=I=-16:TP=-1.5:LRA=11[out]"
"$FFMPEG" -y -loglevel error "${inputs[@]}" -i audio/music.wav -filter_complex "$filters" -map "[out]" -ar 48000 -t 62 build/mix.wav

[ -f build/video-muette.mp4 ] || node render.mjs build/video-muette.mp4

"$FFMPEG" -y -loglevel error -i build/video-muette.mp4 -i build/mix.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart build/echecs-academie-presentation.mp4
"$FFMPEG" -y -loglevel error -ss 59 -i build/video-muette.mp4 -frames:v 1 -q:v 2 build/poster.jpg
echo "OK → build/echecs-academie-presentation.mp4"
