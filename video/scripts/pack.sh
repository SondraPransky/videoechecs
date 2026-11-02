#!/usr/bin/env bash
# Pack complet pour le community manager, dans build/pack/ puis build/pack-reseaux-echecs-com.zip :
#   videos/  une mini-vidéo par pan de l'académie (9:16, 4:5, 1:1, 16:9) + les vidéos générales
#   images/  visuels de src/visuels-data.js dans tous les formats, identité de profil, affiches
#   apercu.html, LISEZ-MOI.md, TEXTES-PUBLICATIONS.md
# Prérequis : la version longue, la courte et la boucle déjà rendues (build.sh). Option --skip-render :
# réutilise les mini-vidéos déjà rendues.
set -euo pipefail
cd "$(dirname "$0")/.."
FFMPEG=$(python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())')
SKIP_RENDER=0; [ "${1:-}" = --skip-render ] && SKIP_RENDER=1
PACK=build/pack
mkdir -p "$PACK/videos" "$PACK/_cadres"
ENC=(-c:v libx264 -preset medium -crf 21 -pix_fmt yuv420p -r 30 -c:a aac -b:a 160k -movflags +faststart)

# Vidéo 16:9 placée dans un cadre (PNG plein) : cadre, vidéo, ordonnée de la zone vidéo, sortie
cadre() {
  "$FFMPEG" -y -loglevel error -loop 1 -i "$1" -i "$2" -filter_complex \
    "[1:v]scale=1080:608:flags=lanczos[v];[0:v][v]overlay=0:$3:shortest=1,format=yuv420p[out]" \
    -map "[out]" -map 1:a "${ENC[@]}" -shortest "$4"
}
declinaisons() {   # source 16:9, dossier de sortie, préfixe, "Titre|suite"
  local src=$1 out=$2 nom=$3 titre=$4 c="$PACK/_cadres/$3"
  mkdir -p "$out" "$c"
  node scripts/social.mjs "$c" --cadres "$titre" >/dev/null
  cadre "$c/cadre-vertical.png" "$src" 656 "$out/$nom-9x16-reels-tiktok-stories.mp4"
  cadre "$c/cadre-portrait.png" "$src" 300 "$out/$nom-4x5-feed-instagram-facebook.mp4"
  cadre "$c/cadre-carre.png" "$src" 236 "$out/$nom-1x1-posts.mp4"
  "$FFMPEG" -y -loglevel error -i "$src" "${ENC[@]}" "$out/$nom-16x9-x-youtube-linkedin.mp4"
  echo "vidéos : $out"
}

# 1. Mini-vidéos par pan de l'académie
PANS=(
  "progression|Progresse|à ton rythme."
  "lecons|+200 leçons|interactives."
  "exercices|+2 000 exercices|à ton niveau."
  "videos|Tout le catalogue|vidéo inclus."
  "masterclasses|Masterclasses|avec des pros."
  "parties|Saisis, analyse,|partage."
  "revue|Toute la revue|en PGN interactif."
  "forum|Rejoins|la communauté."
  "tournois|Mesure-toi|aux autres joueurs."
)
n=1
for p in "${PANS[@]}"; do
  IFS='|' read -r pan t e <<< "$p"
  [ "$SKIP_RENDER" = 1 ] && [ -f "build/echecs-academie-pan-$pan.mp4" ] || bash build.sh --edition "pan-$pan"
  declinaisons "build/echecs-academie-pan-$pan.mp4" "$PACK/videos/$(printf %02d $n)-$pan" "$pan" "$t|$e"
  n=$((n + 1))
done

# 2. Vidéos générales : longue, courte (4 formats), boucle d'en-tête
G="$PACK/videos/00-general"
mkdir -p "$G"
cp build/echecs-academie-presentation.mp4 "$G/presentation-longue-16x9.mp4"
declinaisons build/echecs-academie-court.mp4 "$G" "presentation-courte" "Progresse|à ton rythme."
cp build/echecs-academie-boucle.mp4 "$G/boucle-entete-site-muette-1920x1080.mp4"
"$FFMPEG" -y -loglevel error -i build/echecs-academie-boucle.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset slow -crf 24 -pix_fmt yuv420p -an -movflags +faststart "$G/boucle-entete-site-muette-1280x720.mp4"

# 3. Images : visuels par sujet, identité, affiches générales
node scripts/pack.mjs
bash scripts/social.sh >/dev/null
mkdir -p "$PACK/images/00-general"
cp build/poster.jpg "$PACK/images/00-general/affiche-video-1920x1080.jpg"
for f in build/reseaux/*.jpg; do cp "$f" "$PACK/images/00-general/"; done

# 4. Textes, puis archive
cp pack/LISEZ-MOI.md pack/TEXTES-PUBLICATIONS.md "$PACK/"
rm -rf "$PACK/_cadres"
rm -f build/pack-reseaux-echecs-com.zip
(cd build && zip -qr pack-reseaux-echecs-com.zip pack -x 'pack/_captures/*')
du -sh "$PACK" build/pack-reseaux-echecs-com.zip
