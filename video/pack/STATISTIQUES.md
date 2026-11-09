# Statistiques nécessaires pour les e-mails — Académie et CCAS

9 novembre 2026 · Europe Échecs

## À quoi sert ce document

Pour envoyer les bilans et les relances, la plateforme doit calculer **27 statistiques par joueur pour l'Académie** et **17 pour la CCAS**, plus quelques chiffres de la plateforme (nouveautés). Chaque statistique correspond à une variable des e-mails (`[NB_LECONS]`, `[SERIE]`…).

- Ce document s'adresse à l'équipe technique ; il complète les kits développeurs (`DEVELOPPEURS.md`, `DEVELOPPEURS-CCAS.md`).
- Les numéros entre parenthèses renvoient aux e-mails de chaque série.
- CCAS : les statistiques n'existent pas encore ; les e-mails qui en dépendent (bilans, relance à 1 semaine, série, bilan de l'année) partent quand elles arrivent.

## Académie echecs.com : statistiques par joueur

Les abonnés ont besoin de 23 statistiques, les comptes gratuits de 4 de plus. « Le mois » = le mois civil écoulé, calculé le 1er du mois.

**Abonnés**

| Variable | Ce que c'est | Période | E-mails |
| --- | --- | --- | --- |
| `[NB_JOURS_ACTIFS]` | Jours avec au moins une activité (leçon, exercice, partie, masterclass) | Le mois | 14, 44 |
| `[NB_COURS_SUIVIS]` | Masterclasses et cours suivis, en direct ou en replay | Le mois | 14 |
| `[NB_LECONS]` | Leçons terminées (quiz validé) | Le mois | 14, 44 |
| `[NB_EXERCICES]` | Exercices réussis | Le mois | 14, 44 |
| `[TAUX_REUSSITE]` | Exercices réussis ÷ exercices tentés, en %, arrondi à l'entier | Le mois | 14 |
| `[NB_PARTIES]` | Parties jouées (tournois et zone de jeu) | Le mois | 14, 44 |
| `[SERIE]` | Jours d'entraînement consécutifs jusqu'à aujourd'hui | En cours | 14, 16 |
| `[PARCOURS]` | Nom du parcours en cours (« Objectif 1400 ») | En cours | 14, 44, 45 |
| `[PROGRESSION_PARCOURS]` | Leçons validées ÷ leçons du parcours, nombre de 0 à 100 | En cours | 14, 44, 45 |
| `[THEME_FORT]` | Thème au meilleur taux de réussite (au moins 10 exercices) | Le mois | 14 |
| `[THEME_FAIBLE]` | Thème au plus faible taux de réussite (au moins 10 exercices) | Le mois | 14 |
| `[DERNIERE_LECON]` | Titre de la dernière leçon ouverte | En cours | 17 |
| `[LECON_SUIVANTE]` | Titre de la prochaine leçon du parcours | En cours | 17, 44, 45, 47 |
| `[DUREE_LECON]` | Durée estimée de cette leçon (« 15 min ») | En cours | 17, 44, 45 |
| `[MODULE]` | Module qui vient d'être validé | À l'événement | 15 |
| `[MODULE_SUIVANT]` | Module suivant du parcours | À l'événement | 15 |
| `[NB_LECONS_MODULE]` | Leçons du module validé | À l'événement | 15 |
| `[NB_EXERCICES_MODULE]` | Exercices réussis dans ce module | À l'événement | 15 |
| `[NB_LECONS_ANNEE]` | Leçons terminées | 12 derniers mois | 27 |
| `[NB_EXERCICES_ANNEE]` | Exercices réussis | 12 derniers mois | 27 |
| `[NB_LECONS_TOTAL]` | Leçons terminées | Depuis l'abonnement | 32 |
| `[NB_EXERCICES_TOTAL]` | Exercices réussis | Depuis l'abonnement | 32 |
| `[NB_MODULES]` | Modules validés | Depuis l'abonnement | 32 |

**Comptes gratuits**

| Variable | Ce que c'est | Période | E-mails |
| --- | --- | --- | --- |
| `[NB_PUZZLES_REUSSIS]` | Puzzles du jour réussis pendant la série de 7 jours | 7 derniers jours | 48 |
| `[NB_PUZZLES_ANNEE]` | Puzzles du jour résolus | Depuis la création du compte | 51 |
| `[NB_LECONS_GRATUITES_FAITES]` | Leçons offertes terminées (0 à 6) | Depuis la création du compte | 51 |
| `[NB_MESSAGES_FORUM]` | Messages publiés sur le forum | Depuis la création du compte | 51 |

L'e-mail 47 (« 6 leçons offertes ») réutilise `[NB_EXERCICES]` et `[TAUX_REUSSITE]`, calculés sur les leçons offertes.

## Académie : chiffres de la plateforme et déclencheurs

Les nouveautés sont les mêmes pour tous les joueurs : un seul calcul par période.

| Variable | Ce que c'est | Période | E-mails |
| --- | --- | --- | --- |
| `[NB_NOUVELLES_LECONS_MOIS]` | Leçons mises en ligne | Le mois | 14, 44 |
| `[NB_VIDEOS_MOIS]` | Masterclasses et cours mis en ligne en vidéo | Le mois | 14, 44 |
| `[NB_TOURNOIS_MOIS]` | Tournois organisés | Le mois | 14, 44 |
| `[NB_NOUVELLES_LECONS]` | Leçons mises en ligne | 7 derniers jours | 45 |
| `[NB_VIDEOS_SEMAINE]` | Cours et masterclasses mis en ligne en vidéo | 7 derniers jours | 45 |
| `[NB_TOURNOIS_SEMAINE]` | Tournois organisés | 7 derniers jours | 45 |
| `[NB_NOUVELLES_LECONS_TRIMESTRE]` | Leçons mises en ligne | 3 derniers mois | 46 |
| `[NB_MASTERCLASSES_TRIMESTRE]` | Masterclasses en direct | 3 derniers mois | 46 |
| `[NB_VIDEOS_TRIMESTRE]` | Cours mis en ligne en vidéo | 3 derniers mois | 46 |
| `[NB_TOURNOIS_TRIMESTRE]` | Tournois organisés | 3 derniers mois | 46 |

**Déclencheurs à suivre pour chaque joueur** (pas de variable dans le texte, mais nécessaires pour envoyer au bon moment) :

| Donnée | Sert à envoyer |
| --- | --- |
| Date de la dernière activité | 45 (7 jours), 17 (3 semaines), 18 (6 semaines) |
| Série en cours et activité du jour, le soir | 16 (série ≥ 5 jours sur le point de s'arrêter) |
| Date du dernier envoi du 16 | 16 (au plus une fois toutes les 4 semaines) |
| Validation d'un module | 15 |
| Nombre de leçons offertes terminées | 47 (à la 6ᵉ) |
| Jours de suite sur le puzzle du jour | 48 (au 7ᵉ jour) |
| Dates de création du compte et d'abonnement | 51, 32 (anniversaires) |

## Plateforme CCAS : statistiques par joueur et chiffres de la plateforme

La CCAS a besoin de 17 statistiques par joueur, sur le seul parcours Initiation. Les cours en direct du lundi et du mercredi remplacent les masterclasses.

**Par joueur**

| Variable | Ce que c'est | Période | E-mails |
| --- | --- | --- | --- |
| `[NB_JOURS_ACTIFS]` | Jours avec au moins une activité (leçon, exercice, partie, cours en direct) | Le mois | 14, 24 |
| `[NB_COURS_SUIVIS]` | Cours en direct suivis (présence à la visio ou vidéo regardée) | Le mois | 14 |
| `[NB_LECONS]` | Leçons terminées (quiz validé) | Le mois | 14, 24 |
| `[NB_EXERCICES]` | Exercices réussis | Le mois | 14, 24 |
| `[TAUX_REUSSITE]` | Exercices réussis ÷ exercices tentés, en %, arrondi à l'entier | Le mois | 14 |
| `[NB_PARTIES]` | Parties jouées | Le mois | 14, 24 |
| `[SERIE]` | Jours d'entraînement consécutifs jusqu'à aujourd'hui | En cours | 14, 15 |
| `[PROGRESSION_PARCOURS]` | Leçons validées ÷ leçons du parcours Initiation, nombre de 0 à 100 | En cours | 14, 24, 25 |
| `[THEME_FORT]` | Thème au meilleur taux de réussite (au moins 10 exercices) | Le mois | 14 |
| `[THEME_FAIBLE]` | Thème au plus faible taux de réussite (au moins 10 exercices) | Le mois | 14 |
| `[DERNIERE_LECON]` | Titre de la dernière leçon ouverte | En cours | 17 |
| `[LECON_SUIVANTE]` | Titre de la prochaine leçon du parcours | En cours | 17, 24, 25, 27 |
| `[DUREE_LECON]` | Durée estimée de cette leçon (« 15 min ») | En cours | 17, 24, 25, 27 |
| `[NB_LECONS_ANNEE]` | Leçons terminées | Depuis l'inscription (1 an) | 21 |
| `[NB_EXERCICES_ANNEE]` | Exercices réussis | Depuis l'inscription (1 an) | 21 |
| `[NB_COURS_ANNEE]` | Cours en direct suivis | Depuis l'inscription (1 an) | 21 |
| `[NB_TOURNOIS_ANNEE]` | Tournois joués | Depuis l'inscription (1 an) | 21 |

**Chiffres de la plateforme** (un seul calcul par période)

| Variable | Ce que c'est | Période | E-mails |
| --- | --- | --- | --- |
| `[NB_COURS_MOIS]` | Cours en direct donnés | Le mois | 14, 24 |
| `[NB_NOUVEAUX_EXERCICES_MOIS]` | Exercices ajoutés au parcours Initiation | Le mois | 14, 24 |
| `[NB_TOURNOIS_MOIS]` | Tournois organisés | Le mois | 14, 24 |
| `[NB_COURS_SEMAINE]` | Cours en direct donnés | 7 derniers jours | 25 |
| `[NB_NOUVEAUX_EXERCICES]` | Exercices ajoutés | 7 derniers jours | 25 |
| `[NB_TOURNOIS_SEMAINE]` | Tournois organisés | 7 derniers jours | 25 |

**Déclencheurs à suivre pour chaque joueur**

| Donnée | Sert à envoyer |
| --- | --- |
| Date de la dernière activité | 25 (7 jours), 17 (3 semaines), 18 (6 semaines) |
| Série en cours et activité du jour, le soir | 15 (série ≥ 5 jours sur le point de s'arrêter) |
| Date du dernier envoi du 15 | 15 (au plus une fois toutes les 4 semaines) |
| Date d'inscription | 19 (J+14), 20 (J+30), 21 (1 an) |

## Règles de calcul communes et priorités

Les mêmes définitions valent pour les deux plateformes, pour que les chiffres se comparent.

- **Jour d'entraînement** : un jour (heure de Paris) avec au moins une leçon ouverte, un exercice tenté, une partie jouée ou un cours suivi. La simple connexion ne compte pas.
- **Série** : jours d'entraînement consécutifs, remise à 0 après un jour sans activité.
- **Leçon terminée** : quiz de fin de leçon validé ; une leçon refaite ne compte qu'une fois par période.
- **Taux de réussite** : première tentative de chaque exercice seulement, sinon le taux monte artificiellement.
- **Thème fort ou faible** : seulement les thèmes avec au moins 10 exercices tentés dans le mois ; sinon, la phrase est retirée de l'e-mail.
- **Valeur nulle** : un compteur à 0 s'affiche « 0 » ; une variable impossible à calculer bloque l'envoi (jamais de crochets dans un e-mail).
- **Bilan du mois** : calculé la nuit du dernier jour du mois, envoyé le 1er ; actif à partir de 8 jours d'entraînement, peu actif de 1 à 7, rien à 0 (les relances d'inactivité prennent le relais).

**Priorités**

1. Date de la dernière activité et série : elles déclenchent les relances d'inactivité et la série en danger, les e-mails qui ramènent le plus de joueurs.
2. Compteurs du mois (jours, leçons, exercices, parties, cours) et progression dans le parcours : ils font les bilans du mois.
3. Thèmes forts et faibles, taux de réussite, chiffres annuels : ils enrichissent les bilans mais peuvent arriver plus tard.

**Durée des leçons (`[DUREE_LECON]`)** : elle n'existe pas pour toutes les leçons dans la base. Décision : on la calculera à partir des données utilisateurs.

- **Au lancement** : pas de durée saisie à la main. Quand la durée manque, le texte « environ [DUREE_LECON] » est retiré de l'e-mail (aucune valeur inventée).
- **Ensuite, à partir des données utilisateurs** : la plateforme enregistre, pour chaque leçon terminée, le temps réellement passé (début → fin). La durée estimée d'une leçon = la **médiane** de ces temps, arrondie à 5 minutes, recalculée chaque mois.
- **Seuil** : la durée n'est affichée qu'une fois la leçon terminée par au moins 30 personnes ; on écarte les sessions aberrantes (moins d'1 minute, ou onglet laissé ouvert plus de 2 heures).
- **À prévoir dès maintenant** : enregistrer l'heure de début et de fin de chaque leçon, sinon il n'y aura pas d'historique pour calculer la durée plus tard.

E-mails concernés : Académie 17, 44, 45 · CCAS 17, 24, 25, 27.
