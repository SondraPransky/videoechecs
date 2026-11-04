#!/usr/bin/env bash
# Kit pour l'équipe technique : e-mails HTML + images, aperçus, documentation, fichiers du site.
# Sortie : build/kit-developpeurs.zip. Prérequis : scripts/emails.py et le pack déjà générés.
set -euo pipefail
cd "$(dirname "$0")/.."
K=build/kit-developpeurs; rm -rf "$K" build/kit-developpeurs.zip; mkdir -p "$K/site"
cp pack/DEVELOPPEURS.md pack/EMAILS.md pack/EMAILS-CCAS.md "$K/"
cp -r build/pack/emails "$K/emails"; cp -r build/pack/emails-ccas "$K/emails-ccas"   # e-mails de la plateforme CCAS (Activités Sociales de l'Énergie)
cp build/pack/videos/00-general/boucle-entete-site-muette-1920x1080.mp4 build/pack/videos/00-general/boucle-entete-site-muette-1280x720.mp4 "$K/site/"
cp build/pack/images/00-general/partage-lien-1200x630.jpg "$K/site/"
(cd build && zip -qr kit-developpeurs.zip kit-developpeurs)
du -sh build/kit-developpeurs.zip
