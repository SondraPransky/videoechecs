# Pack réseaux sociaux — echecs.com Académie

Tout ce qu'il faut pour animer les comptes de l'académie, dans le style du motion de présentation.
Ouvrir **apercu.html** dans un navigateur pour voir toutes les images d'un coup.

## Organisation

```
videos/
  00-publicites/     5 publicités de 15 s : une question, sa réponse, une musique par pub (story, 4:5, 16:9, story jaune)
  00-accroches/      première version : 5 publicités de 31 s qui reprennent le motion (16:9 et story 9:16)
  00-general/        présentation longue (56 s), présentation courte (30 s) en 4 formats, boucle muette d'en-tête de site
  01-progression/    une mini-vidéo par pan de l'académie (10 à 17 s), chacune en 4 formats
  02-lecons/ … 09-tournois/
images/
  00-identite/       photos de profil, bannières X / LinkedIn / Facebook / YouTube, couvertures de stories à la une
  00-general/        affiche de la vidéo et visuels généraux
  01-progression/ … 28-tournois-chaque-semaine/   un dossier par visuel, dans 6 formats
apercu.html          planche de toutes les images
TEXTES-PUBLICATIONS.md   textes prêts à publier, hashtags, calendrier type
```

## Quel format pour quel réseau

| Réseau | Vidéo | Image |
|---|---|---|
| Instagram — feed | `*-4x5-feed-instagram-facebook.mp4` (le plus visible) ou `*-1x1-posts.mp4` | `*-portrait-1080x1350.jpg` ou `*-carre-1080x1080.jpg` |
| Instagram — Reels, Stories | `*-9x16-reels-tiktok-stories.mp4` | `*-story-1080x1920.jpg` |
| Instagram — stories à la une | — | `00-identite/a-la-une-*.jpg` |
| TikTok | `*-9x16-reels-tiktok-stories.mp4` | `*-story-1080x1920.jpg` (carrousel photo) |
| Facebook — page | `*-4x5-feed-instagram-facebook.mp4` ou `*-1x1-posts.mp4` | `*-portrait-1080x1350.jpg`, `*-lien-1200x630.jpg` pour un lien |
| Facebook — couverture | — | `00-identite/banniere-facebook-1640x624.jpg` |
| X (Twitter) | `*-16x9-x-youtube-linkedin.mp4` | `*-x-1600x900.jpg` |
| X — bannière | — | `00-identite/banniere-x-1500x500.jpg` |
| LinkedIn | `*-1x1-posts.mp4` ou `*-16x9-x-youtube-linkedin.mp4` | `*-carre-1080x1080.jpg`, `*-lien-1200x630.jpg` |
| LinkedIn — bannière de page | — | `00-identite/banniere-linkedin-1584x396.jpg` |
| YouTube | `presentation-longue-16x9.mp4`, Shorts : `*-9x16-*.mp4` | miniature : `00-general/youtube-miniature-1280x720.jpg` |
| YouTube — bannière de chaîne | — | `00-identite/banniere-youtube-2560x1440.jpg` |
| Pinterest | — | `*-pinterest-1000x1500.jpg` |
| Site web | `boucle-entete-site-muette-*.mp4` (en-tête), `presentation-longue-16x9.mp4` | `affiche-video-1920x1080.jpg` (image avant lecture), `partage-lien-1200x630.jpg` (Open Graph) |
| Photo de profil, partout | — | `00-identite/avatar-*.jpg` (s'affiche en rond) |

## Publicités de 15 s (videos/00-publicites/)

Construites pour la pub, sans reprendre le motion : la question en très grand, « Nous avons la solution ! » (ou « pensé à vous ! »),
puis **une réponse propre à chaque question**, et l'appel final. Chaque pub a sa musique.

| Fichier | Question | Réponse montrée | Musique |
|---|---|---|---|
| `pub-1-*` | Vous enchaînez les parties, mais votre classement ne bouge pas ? | « Jouer ne suffit pas. Entraînez-vous avec méthode. » Courbe Elo qui monte, modules validés | électro-pop |
| `pub-2-*` | Vous jouez beaucoup, mais vous n'avez pas l'impression de progresser ? | « Jouez moins, comprenez plus. » Analyse de partie, erreur repérée, exercices ciblés | disco-funk |
| `pub-3-*` | Vous avez l'impression de stagner depuis quelque temps ? | « Pour passer un cap, apprenez des meilleurs. » Masterclasses en direct avec GM et MF | lo-fi puis hip-hop |
| `pub-4-*` | Vous regardez des vidéos d'échecs, mais ne progressez pas ? | « Ne regardez plus, jouez ! » La vidéo devient un exercice : à vous de jouer | trap cinématique |
| `pub-5-*` | Vous voulez progresser aux échecs, mais vous ne savez pas par où commencer ? | « Suivez le guide, étape par étape. » Le parcours de l'initiation à 2000+ | pop acoustique |

Formats : `*-story-9x16.mp4` (Stories et Reels Instagram, TikTok), `*-story-9x16-jaune.mp4` (même pub sur fond jaune, pour varier
ou tester), `*-feed-4x5.mp4` (fil Instagram et Facebook), `*-16x9.mp4` (YouTube, X, LinkedIn).
Conseil : lancer les 5 en test A/B avec le même budget, garder la question qui convertit le mieux, puis comparer fond noir et fond jaune.

## Première version : publicités de 31 s (videos/00-accroches/)

Cinq versions de 31 s : une question au spectateur, la réponse (« Nous avons la solution ! » ou « Nous avons pensé à vous ! Découvrez l'Académie Europe Échecs »), puis leçons, progression, masterclasses, forum et l'appel final.

| Fichier | Question |
|---|---|
| `accroche-1-*` | Vous enchaînez les parties, mais votre classement ne bouge pas ? |
| `accroche-2-*` | Vous jouez beaucoup, mais vous n'avez pas l'impression de progresser ? |
| `accroche-3-*` | Vous avez l'impression de stagner depuis quelque temps ? |
| `accroche-4-*` | Vous regardez des vidéos d'échecs, mais ne progressez pas ? |
| `accroche-5-*` | Vous voulez progresser aux échecs, mais vous ne savez pas par où commencer ? |

`*-story-9x16.mp4` pour les pubs Instagram (Stories, Reels), `*-16x9.mp4` pour YouTube, X, LinkedIn. En story, la question s'affiche en grand en haut de l'écran pendant l'accroche. Idéal pour un test A/B : même budget sur les 5 versions, puis garder celle qui convertit le mieux.

## Bon à savoir

- Toutes les vidéos se terminent par l'écran « Commencer maintenant · echecs.com/academie ».
- Musique et bruitages sont générés par code : libres de droits, utilisables partout.
- Sur TikTok et les Reels, l'interface de l'application recouvre le bas et le côté droit : le titre et le logo sont en haut exprès.
- Le pack se régénère après toute modification : `bash scripts/pack.sh` dans le dossier `video/` (voir le README).
- Photos de Fabien Libiszewski et Gata Kamsky : Wikimedia Commons (CC BY 2.0 / CC BY-SA 3.0), crédits dans le README du projet. Les remplacer par des portraits officiels si possible.
