# E-mails de suivi des abonnés — Académie echecs.com

32 e-mails prêts à intégrer dans l'outil d'envoi du site : **un fichier HTML par e-mail** dans `emails/`, les images à héberger
dans `emails/img/`, et un aperçu de chaque e-mail (largeur téléphone) dans `emails/apercus/`.
Tous en « tu », dans le style du pack (fond crème, en-tête nuit, bouton jaune), lisibles sur téléphone et dans les messageries
qui bloquent les images (les textes ne sont jamais dans les images).

## Le parcours d'un abonné

```
Création du compte ──► 01 Confirme ton adresse ──► 02 Bienvenue (compte gratuit : 6 leçons, forum, puzzle du jour)
        │                                              │
        │                     pas abonné après…  J+3 ──► 04 Tes leçons offertes
        │                                        J+7 ──► 05 L'Académie complète à 14,90 €
        │                         fin de promo − 3 j ──► 06 Plus que 3 jours
        ▼
Abonnement payé ──► 07 Confirmation + reçu ──► J+1 10 Ton parcours ──► J+3 11 Exercices ──► J+6 12 Masterclasses ──► J+10 13 Communauté
        │
        ├── chaque mois : 09 Reçu (renouvellement) · 14 Bilan du mois · 32 Anniversaire (chaque année)
        ├── en continu  : 15 Module validé · 16 Série en danger · 17 Inactif 7 j · 18 Inactif 30 j
        ├── à 3 mois    : 28 Passage à l'annuel (mensuels)
        ├── paiement    : 08 Paiement refusé (relance J+3)
        └── fin         : 27 Renouvellement annuel J-30 · 30 Résiliation confirmée · 29 Fin d'accès J-7 · 31 Reconquête J+30

Événements (à tous, selon l'actualité) : 19 Annonce de masterclass · 20 Rappel (veille / 1 h avant) · 21 Replay
                                        22 Nouveau cours / replay de cours · 23 Tournoi · 24 Résultats · 25 Revue
                                        26 Lettre d'information à plusieurs nouvelles (toutes les 1 à 2 semaines)
```

## Règles d'envoi

- **E-mails « Compte »** (confirmation, mot de passe, paiement, résiliation, renouvellement annuel) : envoyés à tous, même désinscrits
  des e-mails d'information. Pas de promotion dedans, hormis un rappel discret.
- **E-mails d'information** (tout le reste) : seulement aux personnes qui ont accepté de les recevoir, avec les liens
  `[LIEN_PREFERENCES]` et `[LIEN_DESINSCRIPTION]` (déjà dans le pied de page).
- **Pression** : au maximum 3 e-mails d'information par semaine et par personne. Si plusieurs tombent le même jour, garder le plus
  important (ordre : rappel de masterclass, tournoi, démarrage, lettre d'information) et regrouper le reste dans la lettre `26`.
- **Exclusions** : pas d'e-mail de conversion (04, 05, 06) aux abonnés ; pas de relance d'inactivité pendant les 5 premiers jours.
- **Heures conseillées** : 18 h-20 h en semaine, 9 h-11 h le week-end. Rappels de masterclass : la veille à 18 h et 1 h avant.
- **Expéditeur** : « Académie echecs.com », adresse de réponse lue par quelqu'un (les réponses aux e-mails sont un bon signal).

## Pages à créer sur le site (les e-mails y renvoient)

| Page | Obligatoire ? | Pourquoi |
|---|---|---|
| **Préférences e-mails et désinscription** (`[LIEN_PREFERENCES]`, `[LIEN_DESINSCRIPTION]`) | **Oui** | Tout e-mail d'information doit permettre de se désinscrire simplement, sans se connecter (RGPD). Idéalement : choisir par type (événements, lettre, conseils) plutôt que tout ou rien. |
| **Gestion de l'abonnement** (`[LIEN_ABONNEMENT_GERER]`, `[LIEN_PAIEMENT]`, `[LIEN_PASSAGE_ANNUEL]`) | **Oui** | En France, un abonnement souscrit en ligne doit pouvoir être résilié en ligne, en quelques clics (fonction « résilier mon abonnement »). On y change aussi sa carte et sa formule. |
| **Factures** (`[LIEN_FACTURES]`) | Oui, sous une forme ou une autre | Une facture doit être fournie à chaque paiement. À défaut de page, joindre la facture en PDF aux e-mails 07 et 09. |
| **Ajout à l'agenda** (fichier .ics) | Non | Confort pour les masterclasses. En attendant, les e-mails 19 et 26 renvoient vers la page de la masterclass. |
| **Questionnaire de départ** (`[LIEN_QUESTIONNAIRE_DEPART]`) | Non | Une seule question à choix (trop cher, pas le temps, niveau pas adapté…) : très utile pour les décisions suivantes. Un simple formulaire suffit. |

## Intégration

1. Héberger le dossier `emails/img/` et remplacer `[URL_IMAGES]` par son adresse.
2. Remplacer chaque variable `[NOM]` par la donnée correspondante (liste ci-dessous). Une variable sans valeur ne doit jamais partir telle quelle :
   prévoir une valeur par défaut ou ne pas envoyer.
3. Tester chaque e-mail sur Gmail (web et téléphone), Outlook et Apple Mail avant la première vraie campagne.
4. Ajouter aux liens les repères de suivi : `utm_source=email`, `utm_medium=email`, `utm_campaign=` le nom du fichier (ex. `05-gratuit-j7-offre`).

## Catalogue

### Compte

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `01-confirmation-adresse.html` | À la création du compte (transactionnel) | Confirme ton adresse e-mail | Un clic, et ton compte echecs.com est prêt. | Compte (toujours envoyé) |
| `02-bienvenue-compte-gratuit.html` | Juste après la confirmation de l'adresse | Bienvenue sur echecs.com, [PRENOM] ♟️ | 6 leçons offertes, le forum et le puzzle du jour t'attendent. | Information (désinscription possible) |
| `03-mot-de-passe.html` | Sur demande de réinitialisation (transactionnel) | Réinitialise ton mot de passe | Ce lien est valable 1 heure. | Compte (toujours envoyé) |

### Compte gratuit → abonnement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `04-gratuit-j3-lecons.html` | J+3 après la création du compte, si pas abonné | Tes 6 leçons offertes t'attendent | Vidéo, cours, exercice, quiz : tu as essayé ? | Information (désinscription possible) |
| `05-gratuit-j7-offre.html` | J+7 après la création du compte, si pas abonné | L'Académie complète à 14,90 €/mois | Offre de lancement jusqu'au [FIN_PROMO]. | Information (désinscription possible) |
| `06-gratuit-fin-promo.html` | 3 jours avant la fin de l'offre de lancement, si pas abonné | Plus que 3 jours pour l'offre de lancement | Après le [FIN_PROMO], l'Académie repasse à 19,90 €/mois. | Information (désinscription possible) |

### Abonnement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `07-confirmation-abonnement.html` | Au paiement du premier abonnement (transactionnel) | Bienvenue dans l'Académie, [PRENOM] ! | Ton abonnement est actif : voici ton récapitulatif. | Compte (toujours envoyé) |
| `08-paiement-refuse.html` | Échec d'un prélèvement (transactionnel), relance à J+3 si non réglé | Ton paiement n'est pas passé | Mets à jour ta carte pour garder l'accès à l'Académie. | Compte (toujours envoyé) |
| `09-paiement-recu.html` | À chaque renouvellement réussi (transactionnel) | Ton reçu echecs.com · [MOIS] | Merci ! Ton abonnement continue. | Compte (toujours envoyé) |

### Démarrage de l'abonné

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `10-demarrage-j1-parcours.html` | J+1 après l'abonnement | Par où commencer ? Ton parcours en 3 étapes | Initiation, 1400, 1600, 1800 : trouve ton niveau. | Information (désinscription possible) |
| `11-demarrage-j3-exercices.html` | J+3 après l'abonnement | 10 minutes par jour suffisent | +2 000 exercices, rangés par thème et par niveau. | Information (désinscription possible) |
| `12-demarrage-j6-masterclasses.html` | J+6 après l'abonnement | Les grands maîtres t'attendent | Masterclasses en direct et replays, inclus dans ton abonnement. | Information (désinscription possible) |
| `13-demarrage-j10-communaute.html` | J+10 après l'abonnement | Joue, partage, mesure-toi | Tournois en ligne, forum, tes parties analysées. | Information (désinscription possible) |

### Engagement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `14-bilan-mensuel.html` | Le 1er de chaque mois, si au moins une activité dans le mois | [PRENOM], ton mois d'échecs en chiffres | [NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo ! | Information (désinscription possible) |
| `15-objectif-atteint.html` | Quand l'abonné valide un module ou un parcours | Module validé : [MODULE] 🎉 | Une étape de plus vers ton objectif. | Information (désinscription possible) |
| `16-serie-en-danger.html` | Le soir, si la série de jours (≥ 5 jours) va s'interrompre | Ta série de [SERIE] jours va s'arrêter ⏳ | Un exercice suffit pour la garder. | Information (désinscription possible) |

### Réactivation

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `17-inactif-7-jours.html` | Abonné sans connexion depuis 7 jours | Ta prochaine leçon t'attend | On reprend là où tu t'es arrêté ? | Information (désinscription possible) |
| `18-inactif-30-jours.html` | Abonné sans connexion depuis 30 jours | Tu nous manques, [PRENOM] | Voici ce qui est nouveau depuis ta dernière visite. | Information (désinscription possible) |

### Événements

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `19-annonce-masterclass.html` | Dès qu'une masterclass est programmée (au moins 7 jours avant) | Masterclass : [THEME] avec [COACH] | En direct le [DATE] à [HEURE]. Pose tes questions ! | Information (désinscription possible) |
| `20-rappel-masterclass.html` | La veille, puis 1 heure avant (même modèle) | [QUAND] : masterclass avec [COACH] | [THEME], en direct à [HEURE]. | Information (désinscription possible) |
| `21-replay-masterclass.html` | Dès que le replay est en ligne | Le replay est en ligne : [THEME] | La masterclass de [COACH] en entier, et les positions en PGN. | Information (désinscription possible) |
| `22-nouveau-cours.html` | À la mise en ligne d'un nouveau cours ou d'un replay de cours | Nouveau cours : [TITRE_COURS] | [NB_LECONS_COURS] leçons, niveau [NIVEAU]. | Information (désinscription possible) |
| `23-annonce-tournoi.html` | 5 jours avant un tournoi, rappel le jour J (même modèle) | Tournoi : [NOM_TOURNOI] le [DATE] | Cadence [CADENCE], ouvert à tous les niveaux. | Information (désinscription possible) |
| `24-resultats-tournoi.html` | Le lendemain du tournoi, aux participants | Résultats : [NOM_TOURNOI] | Tu termines [PLACE]e sur [NB_JOUEURS] : bravo ! | Information (désinscription possible) |
| `25-sortie-revue.html` | À la sortie de chaque numéro | Le n°[NUMERO] d'Europe Échecs est sorti | Toutes les parties en PGN interactif dans l'Académie. | Information (désinscription possible) |

### Lettre d'information

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `26-lettre-plusieurs-nouvelles.html` | Toutes les 1 à 2 semaines, à tous les comptes (gratuits et abonnés) | Cette semaine dans l'Académie : [TITRE_UNE] | Masterclass, tournoi, nouveau cours et le puzzle de la semaine. | Information (désinscription possible) |

### Fin d'abonnement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `27-renouvellement-annuel-j30.html` | 30 jours avant le renouvellement d'un abonnement annuel (obligatoire) | Ton abonnement annuel se renouvelle le [DATE_RENOUVELLEMENT] | Rien à faire si tu continues : voici le récapitulatif. | Compte (toujours envoyé) |
| `28-passage-annuel.html` | Abonnés mensuels depuis 3 mois | Près de 2 mois offerts en passant à l'annuel | 150 €/an au lieu de 12 × 14,90 € : tu économises. | Information (désinscription possible) |
| `29-fin-abonnement-j7.html` | 7 jours avant la fin d'un abonnement résilié (fin de période payée) | Ton accès à l'Académie se termine le [DATE_FIN] | Ta progression reste enregistrée. | Compte (toujours envoyé) |
| `30-resiliation-confirmee.html` | À la résiliation (transactionnel) | Ta résiliation est confirmée | Tu gardes l'accès jusqu'au [DATE_FIN]. | Compte (toujours envoyé) |
| `31-reconquete-j30.html` | 30 jours après la fin de l'abonnement | Ton premier mois à 9,90 € pour revenir | Et tout ce qui a changé depuis ton départ. | Information (désinscription possible) |

### Engagement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `32-anniversaire.html` | À la date anniversaire de l'abonnement | Déjà [ANNEES] an(s) dans l'Académie 🎉 | Merci, [PRENOM] ! Voici ton parcours. | Information (désinscription possible) |

## Variables

**Liens** (adresse de la page correspondante sur le site) : `[LIEN_ABONNEMENT]`, `[LIEN_ABONNEMENT_GERER]`, `[LIEN_ACADEMIE]`, `[LIEN_CONFIRMATION]`, `[LIEN_COURS]`, `[LIEN_DESINSCRIPTION]`, `[LIEN_DIRECT]`, `[LIEN_EXERCICES]`, `[LIEN_EXERCICE_DU_JOUR]`, `[LIEN_FACTURES]`, `[LIEN_INSCRIPTION_TOURNOI]`, `[LIEN_LECONS]`, `[LIEN_LECON_SUIVANTE]`, `[LIEN_MASTERCLASSES]`, `[LIEN_MASTERCLASS]`, `[LIEN_MES_PARTIES]`, `[LIEN_MODULE_SUIVANT]`, `[LIEN_MOT_DE_PASSE]`, `[LIEN_PAIEMENT]`, `[LIEN_PARCOURS]`, `[LIEN_PASSAGE_ANNUEL]`, `[LIEN_PREFERENCES]`, `[LIEN_PREMIERE_LECON]`, `[LIEN_PROGRESSION]`, `[LIEN_PUZZLE]`, `[LIEN_QUESTIONNAIRE_DEPART]`, `[LIEN_REACTIVATION]`, `[LIEN_REPLAY]`, `[LIEN_REVUE]`, `[LIEN_TEST_PLACEMENT]`, `[LIEN_THEME_FAIBLE]`, `[LIEN_TOURNOIS]`.

| Variable | Contenu |
|---|---|
| `[ADRESSE_POSTALE]` | adresse de l'éditeur (obligatoire dans les e-mails d'information) |
| `[ANNEES]` |  |
| `[AUTEUR]` |  |
| `[CADENCE]` |  |
| `[COACH]` |  |
| `[DATE]` |  |
| `[DATE_FIN]` |  |
| `[DATE_FIN_OFFRE]` |  |
| `[DATE_PROCHAIN_PAIEMENT]` |  |
| `[DATE_RENOUVELLEMENT]` |  |
| `[DATE_SUSPENSION]` |  |
| `[DERNIERE_LECON]` |  |
| `[DESCRIPTION_COURS]` |  |
| `[DESCRIPTION_MASTERCLASS]` |  |
| `[DEUXIEME]` |  |
| `[DUREE]` |  |
| `[FIN_PROMO]` | date de fin de l'offre de lancement |
| `[FORMULE]` | « Mensuelle » ou « Annuelle » |
| `[HEURE]` |  |
| `[LECON_SUIVANTE]` |  |
| `[MODULE]` |  |
| `[MODULE_SUIVANT]` |  |
| `[MOIS]` |  |
| `[MOYEN_PAIEMENT]` |  |
| `[NB_EXERCICES]` |  |
| `[NB_EXERCICES_ANNEE]` |  |
| `[NB_EXERCICES_MODULE]` |  |
| `[NB_EXERCICES_TOTAL]` |  |
| `[NB_JOUEURS]` |  |
| `[NB_LECONS]` |  |
| `[NB_LECONS_ANNEE]` |  |
| `[NB_LECONS_COURS]` |  |
| `[NB_LECONS_GRATUITES_RESTANTES]` |  |
| `[NB_LECONS_MODULE]` |  |
| `[NB_LECONS_TOTAL]` |  |
| `[NB_MODULES]` |  |
| `[NB_RONDES]` |  |
| `[NIVEAU]` |  |
| `[NOM_TOURNOI]` |  |
| `[NOUVEAUTE_1]` | une nouveauté depuis la dernière visite (idem 2 et 3) |
| `[NOUVEAUTE_2]` |  |
| `[NOUVEAUTE_3]` |  |
| `[NUMERO]` |  |
| `[PLACE]` |  |
| `[POINTS]` |  |
| `[PRENOM]` | prénom de l'abonné (à défaut : « » vide et la phrase reste correcte) |
| `[PRIX]` | montant payé, ex. « 14,90 € » |
| `[QUAND]` | « Demain » ou « Dans 1 heure » (rappel de masterclass) |
| `[RESUME_MASTERCLASS]` |  |
| `[SERIE]` | nombre de jours d'affilée |
| `[SERIE_MAX]` |  |
| `[SOMMAIRE_1]` |  |
| `[SOMMAIRE_2]` |  |
| `[SOMMAIRE_3]` |  |
| `[TAUX_REUSSITE]` | pourcentage d'exercices réussis |
| `[THEME]` |  |
| `[THEME_FAIBLE]` | thème le moins réussi du mois |
| `[THEME_FORT]` | thème le plus réussi du mois (calculé par le site) |
| `[TITRE_COACH]` |  |
| `[TITRE_COURS]` |  |
| `[TITRE_UNE]` |  |
| `[TROISIEME]` |  |
| `[VAINQUEUR]` |  |
| `[URL_IMAGES]` | adresse où sont hébergées les images du dossier img/ (ex. https://echecs.com/mail/img) |

Les variables non décrites portent un nom explicite (dates, nombres, noms de coach, de tournoi, de cours…).
