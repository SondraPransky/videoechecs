# Leçons vidéo à partir d'un PGN

Ce dossier transforme une partie commentée en leçon vidéo avec voix off, au format 1920×1080 et 30 images par seconde.

La vidéo montre :
- un échiquier animé, avec flèches et cases colorées ;
- la liste des coups en notation figurine ;
- une carte « Idée clé » et un badge d'évaluation ;
- des quiz « À toi de jouer ! » avec compte à rebours ;
- des cartes de chapitre avec la mascotte ;
- des sous-titres, un bruit de pièce à chaque coup et un bilan final.

## Leçons

| Leçon | Source | Niveau | Durée |
|---|---|---|---|
| `jobava/` — Une petite idée contre le Jobava | PGN commenté de Romuald De Labaca (12/11/2024) | Objectif 1600-1800 | environ 13 min |

## Fabriquer une leçon

1. **Écrire `lecons/<nom>/lecon.mjs`.**
   - Chaque passage associe une réplique de la voix (`say`) et ce qui se passe sur l'échiquier : coups joués, flèches, cases, idée clé, quiz.
   - Le format est décrit en tête de `jobava/lecon.mjs`.
   - Les coups s'écrivent en notation anglaise (`Nf3`, `Bxc5`). Ils sont affichés en français (`Cf3`, `Fxc5`).
   - Dans le texte parlé, on écrit les coups comme on les dit : « Cavalier f3 », « Fou prend c5 ».
2. **Vérifier et relire.** La commande suivante vérifie la légalité de chaque coup et régénère `lecons/<nom>/script.md`, le texte complet à relire :
   ```bash
   node lecons/build.mjs <nom> plan
   ```
3. **Produire la vidéo.** Choisir l'une des deux voix :
   ```bash
   bash lecons/build.sh <nom>                    # voix Piper (maquette gratuite)
   bash lecons/build.sh <nom> --eleven <ID>      # voix ElevenLabs
   ```
   Le résultat est écrit dans `build/lecons/<nom>/` : `lecon-<nom>.mp4`, `sous-titres.vtt` et `affiche.jpg`.

Les voix sont mises en cache réplique par réplique. Si l'on corrige une phrase, seule celle-ci est réenregistrée. C'est important pour ElevenLabs, dont le quota est limité.

Pour vérifier quelques images sans tout rendre :

```bash
node render.mjs build/lecons/<nom>/apercu --page "lecons/player.html?l=<nom>" --frames 60,300,600
```

## Voix off

- **Piper**, voix `fr_FR-tom-medium` : gratuite et hors ligne. Elle sert de maquette.
- **ElevenLabs** : nettement plus naturelle, avec le modèle `eleven_flash_v2_5`, qui coûte 0,5 crédit par caractère. Une leçon de 13 minutes compte environ 10 500 caractères, soit environ 5 300 crédits. Elle tient donc dans l'offre gratuite de 10 000 crédits par mois.
- Pour lister les voix du compte : `python3 lecons/voix.py --voices`.
- ElevenLabs renvoie l'instant de chaque caractère lu. Les coups tombent alors exactement sur le mot prononcé. Avec Piper, cet instant est estimé.
- Avant la lecture, `e5` est transformé en `é5` pour éviter un « euh cinq ». Les autres corrections de prononciation se trouvent dans `SAY`, dans `voix.py`.

## Fichiers

- `build.mjs` : lit la leçon, vérifie les coups avec chess.js et calcule la chronologie calée sur la voix. Il produit aussi les sous-titres.
- `voix.py` : synthèse vocale, avec Piper ou ElevenLabs.
- `mix.py` : ajoute les bruitages synthétisés, libres de droits, et mixe le tout.
- `player.html` : la page rendue image par image par `../render.mjs`, avec les options `--page` et `--workers` pour le rendu parallèle.
