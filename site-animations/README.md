# Mascotte animée — echecs.com

Treize animations de la mascotte, dans le style de l'animation « hello » du designer (même silhouette et même bras articulé à l'épaule). Chaque fichier est un **SVG autonome animé en CSS**, sans JavaScript, d'environ 8 Ko.

Aperçu : ouvrir `index.html` dans un navigateur. Le bouton « Rejouer » relance les intros, et un autre bouton bascule entre fond clair et fond sombre.

| Fichier | Moment sur le site | Ce qui se passe |
|---|---|---|
| `mascotte-lecon-terminee` | Fin d'une leçon | Saut, la toque de diplômé tombe sur la tête et y reste, étincelles |
| `mascotte-serie-reussie` | Série d'exercices réussie | Trois étoiles apparaissent, sauts poing levé, confettis |
| `mascotte-bonne-reponse` | Exercice réussi | Pirouette sautée, pastille verte qui se coche |
| `mascotte-mauvaise-reponse` | Exercice raté | Sursaut, le bras retombe, secoue la tête, croix rouge, « ? » |
| `mascotte-serie-ratee` | Série échouée | Épaules basses, bras ballant, petit nuage de pluie |
| `mascotte-reflexion` | Chargement, réflexion | Main sur la tête, bulle de pensée « … » |
| `mascotte-idee` | Indice, astuce | Petit saut, une ampoule s'allume au-dessus de la tête |
| `mascotte-lecture` | Leçon en cours, cours écrit | Lit un grand livre, les pages tournent |
| `mascotte-niveau-superieur` | Progression, nouveau niveau | Gravit un escalier sans fin, flèches vertes |
| `mascotte-serie-de-jours` | Série quotidienne (assiduité) | Danse à côté d'une flamme, le bras balance |
| `mascotte-victoire-tournoi` | Tournoi gagné, podium | Trophée brandi avec reflet, confettis |
| `mascotte-dodo` | Inactivité, « reviens vite » | Avachie, respire lentement, « Z z z » |
| `mascotte-regarde` | Onboarding : « regarde ici » | Bras tendu qui montre vers la gauche |

Le nom exact d'un fichier dépend de sa couleur, par exemple `svg/noir/mascotte-idee-noir.svg`.

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

**Les poses du bras** sont des rotations autour de l'épaule. Pour varier les attitudes, on joue aussi sur le corps (sauts, pirouette, danse, tête qui penche) et sur les accessoires (livre, ampoule, escalier, toque, trophée) :

| Angle | Pose |
|---|---|
| 0° | poing levé (le « hello » du designer) |
| 20° | poing très haut |
| −68° | bras tendu qui montre |
| −112° | bras ballant |
| 40° | main sur la tête |
