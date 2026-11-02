# Mascotte animée — echecs.com

Quarante-deux animations de la mascotte (et leurs 42 versions miroir, tournées vers la droite), dans le style de l'animation « hello » du designer (même silhouette et même bras articulé à l'épaule). Chaque fichier est un **SVG autonome animé en CSS**, sans JavaScript, d'environ 8 Ko.

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
| `mascotte-coucou` | Accueil, bienvenue | Grand signe de la main, traits de mouvement |
| `mascotte-course` | Défi chronométré, « vite ! » | Court penchée en avant, traits de vitesse, poussière |
| `mascotte-salto` | Grande victoire, record | Saut périlleux complet, étincelles à l'atterrissage |
| `mascotte-surgit` | Coin d'écran, astuce discrète | Surgit du bas, salue, redescend |
| `mascotte-pion-brandi` | Débutant, premier coup | Brandit un grand pion |
| `mascotte-loupe` | Analyse de partie, recherche | Balaie avec une loupe |
| `mascotte-megaphone` | Annonce, nouveauté | Crie dans un mégaphone, ondes sonores |
| `mascotte-telephone` | Application mobile, notification | Regarde son téléphone, pastille de notification |
| `mascotte-haltere` | Entraînement du jour | Soulève une haltère |
| `mascotte-drapeau` | Objectif atteint | Agite un drapeau à damier |
| `mascotte-pendule` | Blitz, cadence, tournoi | Tape la pendule d'échecs, les aiguilles tournent |
| `mascotte-discussion` | Forum, commentaires | Bulle de discussion qui s'écrit, parle avec la main |
| `mascotte-coeur` | Merci, communauté | Tient un cœur qui bat, cœurs qui s'envolent |
| `mascotte-assoupie` | « Tu es toujours là ? » | Pique du nez, sursaute, recommence |
| `mascotte-sieste` | Inactivité longue, mode nuit | Couchée sur un oreiller sous une couverture, « Z z z » |
| `mascotte-s-endort` | Fin de journée, « à demain » | Bâille, pique du nez, se couche, dort, se relève |
| `mascotte-disco` | Fête, week-end | Danse disco sous une boule à facettes |
| `mascotte-etirement` | Début de séance, échauffement | S'étire vers le ciel |
| `mascotte-toupie` | Transition, « et maintenant ? » | Se retourne d'un côté puis de l'autre |
| `mascotte-marche` | Parcours, prochaine étape | Traverse le cadre d'un pas décidé |
| `mascotte-fete` | Anniversaire, cap franchi | Chapeau pointu, confettis |
| `mascotte-jongle` | Astuces, multitâche | Jongle avec trois pions |
| `mascotte-super-heros` | Super-progrès, défi relevé | Cape au vent, poing levé |
| `mascotte-zen` | Concentration avant un tournoi | Flotte en méditation, ondes de calme |
| `mascotte-cafe` | Bonjour, révision du matin | Tasse fumante |
| `mascotte-parapluie` | Coup dur, défaite | À l'abri sous la pluie |
| `mascotte-bonnet` | Hiver, fêtes de fin d'année | Bonnet à pompon, la neige tombe |
| `mascotte-message-recu` | Nouveau message, notification | Attrape une enveloppe, elle s'ouvre, la lettre sort |
| `mascotte-envoi-mail` | Newsletter, e-mail envoyé | Lance une enveloppe qui s'envole |

Le nom exact d'un fichier dépend de sa couleur, par exemple `svg/noir/mascotte-idee-noir.svg`.

**Versions miroir** : chaque animation existe aussi tournée vers la droite, avec le suffixe `-miroir` (par exemple `svg/jaune/mascotte-coucou-miroir-jaune.svg`). Pratique pour qu'elle regarde vers le contenu, quel que soit le côté de la page où elle est placée.

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
