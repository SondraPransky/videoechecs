#!/usr/bin/env bash
# Génère une piste WAV par réplique de script.txt avec Piper (voix fr_FR-tom-medium).
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p out models
BASE=https://huggingface.co/rhasspy/piper-voices/resolve/main/fr/fr_FR/tom/medium
for f in fr_FR-tom-medium.onnx fr_FR-tom-medium.onnx.json; do
  [ -f "models/$f" ] || curl -sSL -o "models/$f" "$BASE/$f"
done
while IFS='|' read -r id text; do
  [ -z "$id" ] && continue
  echo "$text" | python3 -m piper -m models/fr_FR-tom-medium.onnx --length-scale 1.08 --sentence-silence 0.35 -f "out/$id.wav" >/dev/null 2>&1
  printf '%s %s\n' "$id" "$(python3 -c "import wave,sys;w=wave.open('out/$id.wav');print(round(w.getnframes()/w.getframerate(),2))")"
done < script.txt
