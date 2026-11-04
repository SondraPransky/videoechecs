#!/usr/bin/env bash
# Deux kits pour les équipes techniques :
#   build/kit-developpeurs-academie.zip : Académie echecs.com (e-mails des abonnés, fichiers du site)
#   build/kit-developpeurs-ccas.zip     : plateforme CCAS (e-mails des bénéficiaires des Activités Sociales de l'Énergie)
# Prérequis : python3 scripts/emails.py, python3 scripts/emails.py ccas, node scripts/emails-apercus.mjs [ccas], et le pack déjà générés.
set -euo pipefail
cd "$(dirname "$0")/.."
rm -rf build/kit-developpeurs build/kit-developpeurs.zip build/kit-developpeurs-academie build/kit-developpeurs-academie.zip build/kit-developpeurs-ccas build/kit-developpeurs-ccas.zip
# Académie echecs.com
K=build/kit-developpeurs-academie; mkdir -p "$K/site"
cp pack/DEVELOPPEURS.md pack/EMAILS.md scripts/miniature-mail.py "$K/"
cp -r build/pack/emails "$K/emails"
cp build/pack/videos/00-general/boucle-entete-site-muette-1920x1080.mp4 build/pack/videos/00-general/boucle-entete-site-muette-1280x720.mp4 "$K/site/"
cp build/pack/images/00-general/partage-lien-1200x630.jpg "$K/site/"
# Plateforme CCAS
C=build/kit-developpeurs-ccas; mkdir -p "$C/marque"
cp pack/DEVELOPPEURS-CCAS.md pack/EMAILS-CCAS.md scripts/miniature-mail.py "$C/"
cp -r build/pack/emails-ccas "$C/emails-ccas"
cp ../assets/brand/ccas/logo-activites-sociales-energie-web.svg ../assets/brand/ccas/ccas-favicon-*.png "$C/marque/"
(cd build && zip -qr kit-developpeurs-academie.zip kit-developpeurs-academie && zip -qr kit-developpeurs-ccas.zip kit-developpeurs-ccas)
du -sh build/kit-developpeurs-academie.zip build/kit-developpeurs-ccas.zip
