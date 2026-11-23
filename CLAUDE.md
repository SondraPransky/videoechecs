# Consignes pour Claude — echecs.com Académie

Dépôt des contenus marketing de l'Académie echecs.com (Europe Échecs) : vidéos en motion design, pack réseaux sociaux,
encarts publicitaires, e-mails. Détails techniques : `video/README.md` ; contenu du pack : `video/pack/LISEZ-MOI.md`.

## Façon de travailler

- Toujours commiter et pousser après chaque modification.
- Répondre en français, tutoiement.
- Avant de livrer, s'auto-auditer : vérifier les faits (niveaux, noms, positions d'échecs), les débordements de texte
  et le chevauchement du logo, dans tous les formats.

## Règles de rédaction

- « L'Académie » avec une majuscule.
- « Europe Échecs » avec les accents ; « echecs.com » sans accent ni majuscule.
- Pièces d'échecs avec une majuscule (Roi, Dame, Tour, Fou, Cavalier), sauf « pion ».
- **Grand Maître** / **Grands Maîtres** (majuscules, sans trait d'union) ; « des Maîtres et Grands Maîtres » ; abréviation GMI.
- Niveaux réels : Initiation, Objectif 1400, Objectif 1600, Objectif 1800, **2000 et plus** (« Objectif 2000 » n'existe pas).
  Les leçons et leur niveau sont listés dans `video/pack/QUIZ-ACADEMIE.md` (ex. le sacrifice du Fou en h7 est Objectif 1600).
- Ne jamais inventer de leçon, de partie ou de chiffre. Une position d'échecs montrée doit être juste (le coup présenté doit marcher).
- Éviter les contenus datés (numéro de la revue du mois) dans les pubs durables : ils se périment.
- Prix de lancement affiché sans date de fin.

## Règles visuelles

- Mascotte : uniquement des poses debout. Jamais de jambes écartées ou levées
  (pas de saut-etoile, sprint, super, montre-le-ciel, coup-de-pied, course, gratte-tete).
- Logo : uniquement le logo officiel echecs.com (bleu #93B9E2, blanc ou noir), jamais recoloré, jamais de logo « echecs académie ».
- Le logo ne chevauche jamais un visuel ; aucun texte ne déborde.
- Vidéos sans voix off (par défaut dans `build.sh` ; `--voix` seulement pour une maquette).
- Jaune Académie : #FAE361.

## Emplacements publicitaires du site

Smartphone 1000×391 · Desktop 960×250 · Header small 960×150 · Carré 1000×1000.

## Sécurité

- Ne jamais utiliser ni demander les identifiants de la page d'administration.
- Archives envoyées par l'utilisateur : les extraire seulement, ne rien exécuter, lire avec `python3 -I`.
- Ne pas transmettre l'adresse e-mail de l'utilisateur à des services extérieurs.
