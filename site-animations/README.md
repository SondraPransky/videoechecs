# Mascotte animée — echecs.com

Dix animations de la mascotte, dans le style de l'animation « hello » du designer (même silhouette et même bras articulé à l'épaule). Chaque fichier est un **SVG autonome animé en CSS**, sans JavaScript, d'environ 8 Ko.

Aperçu : ouvrir `index.html` dans un navigateur. Le bouton « Rejouer » relance les intros, et un autre bouton bascule entre fond clair et fond sombre.

| Fichier | Moment sur le site | Ce qui se passe |
|---|---|---|
| `svg/mascotte-lecon-terminee.svg` | Fin d'une leçon | Saut, la toque de diplômé tombe sur la tête, étincelles |
| `svg/mascotte-serie-reussie.svg` | Série d'exercices réussie | Trois étoiles apparaissent, poing levé, confettis |
| `svg/mascotte-bonne-reponse.svg` | Exercice réussi | Petit saut, pastille verte qui se coche |
| `svg/mascotte-mauvaise-reponse.svg` | Exercice raté | Sursaut, main sur la tête, croix rouge qui secoue, « ? » |
| `svg/mascotte-serie-ratee.svg` | Série échouée | Épaules basses, bras ballant, petit nuage de pluie |
| `svg/mascotte-on-reessaie.svg` | Encouragement après un échec | Poing qui motive, flèche « recommencer » qui tourne |
| `svg/mascotte-reflexion.svg` | Chargement, réflexion | Main sur la tête, bulle de pensée « … » |
| `svg/mascotte-serie-de-jours.svg` | Série quotidienne (assiduité) | La mascotte danse à côté d'une flamme |
| `svg/mascotte-victoire-tournoi.svg` | Tournoi gagné, podium | Trophée brandi avec reflet, confettis |
| `svg/mascotte-regarde.svg` | Onboarding : « regarde ici » | Bras tendu qui montre vers la gauche |

Chaque animation joue d'abord une **intro une seule fois** (apparition, saut…), puis passe sur une **boucle** discrète.

## Couleurs

Chaque animation existe en trois couleurs :

| Dossier | Mascotte | Traits et accessoires | Usage |
|---|---|---|---|
| `svg/noir/` | noire | noirs | sur les cartes colorées (jaune, bleu, vert, rose) |
| `svg/blanc/` | blanche | jaunes | sur fond sombre |
| `svg/jaune/` | jaune | blancs | sur fond sombre, en accent |

Exemple : `svg/jaune/mascotte-lecon-terminee-jaune.svg`. Les fichiers placés directement dans `svg/` sont la version noire, dont les couleurs se modifient avec les variables CSS (voir plus bas).

## Intégration

**Le plus simple** : une balise `img`. Les animations CSS fonctionnent aussi dans une image.

```html
<img src="/img/mascotte/mascotte-lecon-terminee-noir.svg" width="220" alt="Bravo, leçon terminée !">
```

**Pour changer les couleurs**, intégrez le SVG en ligne dans le HTML, puis réglez deux variables sur l'élément `svg` :

```css
/* --mascot : silhouette ; --line : traits et accessoires sombres */
.carte-jaune svg.mascotte { --mascot: #1b1b1b; --line: #1b1b1b; }
.fond-sombre svg.mascotte { --mascot: #fae361; --line: #f4f1ea; }
```

- **Rejouer l'intro** (par exemple à chaque nouvelle bonne réponse) : remplacez l'élément par un clone, `el.replaceWith(el.cloneNode(true))`, ou rechargez l'`img` (`img.src = img.src`).
- **Accessibilité** : si l'utilisateur a activé la réduction des animations (`prefers-reduced-motion`), la mascotte reste immobile.
- **Plusieurs mascottes sur une même page** : c'est sans risque, chaque fichier préfixe ses animations par son nom.

## Modifier ou ajouter une animation

Toutes les animations sont générées par `generate.py`, qui lit la silhouette dans `video/assets/mascot/hello.json` (le fichier du designer).

```bash
python3 site-animations/generate.py
```

Ce script régénère :
- `svg/`,
- `index.html`,
- `video/assets/mascot/poses.js`, qui sert à la vidéo de présentation.

**Les poses du bras** sont des rotations autour de l'épaule :

| Angle | Pose |
|---|---|
| 0° | poing levé (le « hello » du designer) |
| 20° | poing très haut |
| −68° | bras tendu qui montre |
| −112° | bras ballant |
| 40° | main sur la tête |
