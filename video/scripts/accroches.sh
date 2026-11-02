#!/usr/bin/env bash
# Publicités : 5 versions de ~31 s qui commencent par une question-accroche (éditions accroche-1 à 5
# de scripts/timing.py), en 16:9 et en story 9:16. La partie commune (après l'accroche et la réponse)
# n'est rendue qu'une fois puis raccordée à chaque début. Sorties : build/accroches/ et build/pack/videos/00-accroches/.
set -euo pipefail
cd "$(dirname "$0")/.."
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
O=build/accroches; P=build/pack/videos/00-accroches
mkdir -p "$O" "$P" build/_acc
SFX_VOL=${SFX_VOL:-0.28}
COUPE=6.5   # fin de l'accroche et de la réponse (hook 4 s + sol 2,5 s)
ENC=(-c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart)
QUESTIONS=(
  "Vous enchaînez les parties,|mais votre classement ne bouge pas ?"
  "Vous jouez beaucoup,|mais vous n'avez pas l'impression de progresser ?"
  "Vous avez l'impression|de stagner depuis quelque temps ?"
  "Vous regardez des vidéos d'échecs,|mais ne progressez pas ?"
  "Vous voulez progresser aux échecs,|mais vous ne savez pas par où commencer ?"
)
for k in 1 2 3 4 5; do
  python3 scripts/timing.py --music-only --edition "accroche-$k" >/dev/null
  python3 audio/music.py
  node render.mjs --sfx build/sfx.json --edition "accroche-$k"
  python3 audio/sfx.py
  TOTAL=$(python3 -c "import json;print(json.load(open('build/timing.json'))['total'])")
  "$FFMPEG" -y -loglevel error -i audio/music.wav -i build/sfx.wav -filter_complex "[1:a]volume=$SFX_VOL[fx];[0:a][fx]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.2:LRA=9[out]" -map "[out]" -ar 48000 -t "$TOTAL" "build/_acc/mix-$k.wav"
  [ -f "build/_acc/tete-$k.mp4" ] || node render.mjs "build/_acc/tete-$k.mp4" --edition "accroche-$k" --to "$COUPE"
done
[ -f build/_acc/queue.mp4 ] || node render.mjs build/_acc/queue.mp4 --edition accroche-1 --from "$COUPE"
python3 scripts/timing.py --music-only >/dev/null   # remet build/timing.json sur la version longue

for k in 1 2 3 4 5; do
  printf "file 'tete-%s.mp4'\nfile 'queue.mp4'\n" "$k" > build/_acc/liste.txt
  "$FFMPEG" -y -loglevel error -f concat -safe 0 -i build/_acc/liste.txt -c copy "build/_acc/video-$k.mp4"
  "$FFMPEG" -y -loglevel error -i "build/_acc/video-$k.mp4" -i "build/_acc/mix-$k.wav" -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart "$O/accroche-$k-16x9.mp4"
  # Story 9:16 : la question en grand pendant l'accroche, puis la réponse, puis le titre habituel
  IFS='|' read -r qt qe <<< "${QUESTIONS[$((k - 1))]}"
  if [ $((k % 2)) = 1 ]; then st="Nous avons"; se="la solution !"; else st="Nous avons"; se="pensé à vous !"; fi
  node scripts/social.mjs "build/_acc/q$k" --cadres "$qt|$qe" --fs 64 >/dev/null
  node scripts/social.mjs "build/_acc/s$k" --cadres "$st|$se" --fs 92 >/dev/null
  node scripts/social.mjs "build/_acc/d" --cadres "Progresse|à ton rythme." >/dev/null
  "$FFMPEG" -y -loglevel error -loop 1 -i build/_acc/d/cadre-vertical.png -loop 1 -i "build/_acc/q$k/cadre-vertical.png" -loop 1 -i "build/_acc/s$k/cadre-vertical.png" -i "$O/accroche-$k-16x9.mp4" -filter_complex \
    "[0:v][1:v]overlay=0:0:enable='lt(t,4)'[a];[a][2:v]overlay=0:0:enable='between(t,4,$COUPE)'[b];[3:v]scale=1080:608:flags=lanczos[v];[b][v]overlay=0:656:shortest=1,format=yuv420p[out]" \
    -map "[out]" -map 3:a "${ENC[@]}" -shortest "$O/accroche-$k-story-9x16.mp4"
  cp "$O/accroche-$k-16x9.mp4" "$O/accroche-$k-story-9x16.mp4" "$P/"
  echo "accroche $k : OK"
done
ls -la "$O"
