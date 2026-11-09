# E-mails des bénéficiaires CCAS — plateforme d'échecs des Activités Sociales de l'Énergie

27 e-mails pour les joueurs de https://ccas.echecs.com/academy/ : **un fichier HTML par e-mail** dans `emails-ccas/`,
les images à héberger dans `emails-ccas/img/`. Même moteur et même design que les e-mails de l'Académie echecs.com
(`scripts/emails.py ccas`, contenu dans `scripts/emails-contenu-ccas.py`).

**Ce qui change par rapport à l'Académie echecs.com :**
- **Aucun abonnement, aucun paiement** : pas d'offre, de prix, de reçu ni de relance de paiement. L'accès est offert par le partenariat et n'a pas de fin prévue.
- **Marque** : logo des Activités Sociales de l'Énergie (CCAS) en en-tête, **pas de logo echecs.com**. Expéditeur « Europe Échecs · Activités Sociales » ;
  signature « Les Activités Sociales de l'Énergie, en partenariat avec Europe Échecs ». Pas de liens vers les réseaux d'echecs.com dans le pied de page.
- **Contenu** : le **parcours Initiation** seulement (leçons et exercices), tournois en ligne, forum, et **cours en direct le lundi et le mercredi à 18 h 30** avec Éric et Florian, en visioconférence.
  Pas de masterclasses ni de revue.

## Le parcours d'un joueur

```
Création du compte ──► 01 Confirme ton adresse ──► 02 Bienvenue (tout est offert)
        │
        ▼
Démarrage : J+1 04 Cours en direct ──► J+3 05 Exercices ──► J+6 06 Communauté
Partenariat : J+14 19 Les échecs en famille ──► J+30 20 Questionnaire de satisfaction ──► 1 an 21 Bilan de l'année
        │
        ├── cours en direct : 07 Programme de la semaine (lundi, les deux cours) · 08 Les cours de la semaine (jeudi, vidéos YouTube) · 09 Cours déplacé · 26 Pause des vacances · 27 Reprise des cours
        ├── tournois        : 10 Annonce (J-5 et jour J) · 11 Inscription confirmée · 12 Résultats
        ├── lettre          : 13 Lettre de la semaine (2 ou 3 nouvelles mélangées : cours en vidéo, tournoi, résultats ; remplace alors le 08)
        ├── chaque mois     : 14 / 24 Bilan du mois (actif / peu actif, le 1er du mois)
        ├── en continu      : 15 Série en danger (1 fois par mois au plus) · 16 Réponse sur le forum
        ├── réactivation    : 25 après 1 semaine · 17 après 3 semaines · 18 après 6 semaines (chacun une seule fois)
        └── compte          : 22 Changement de la plateforme ou de l'accès (30 jours avant) · 23 Suppression du compte (RGPD)
```

## Design

Même mise en page que les e-mails de l'Académie (voir `EMAILS.md`), en **Signika** comme l'Académie et la plateforme CCAS, avec le bleu du logo (#0066cc) pour le surtitre et la suite des titres. L'en-tête : bande blanche avec le logo des Activités Sociales de l'Énergie
(`img/logo.png`, tiré du logo web officiel « activités sociales de l'énergie », bleu #0066cc, 280 px de large), qui reste blanche en mode sombre pour garder le logo lisible.
Le favicon CCAS (le soleil, `assets/brand/ccas/ccas-favicon-*.png`) peut servir d'image d'expéditeur (BIMI, avatar Gmail) si l'outil d'envoi le permet.

**Bloc vidéo** (e-mails 08 et 13) : la miniature YouTube du cours en entier (16:9, jamais recadrée), cliquable vers YouTube ; en dessous, le thème, le jour,
l'animateur, la durée, et deux liens : « Revoir le cours » (la leçon sur la plateforme) et « Sur YouTube ».
- **Image à fournir** (`[URL_MINIATURE_LUNDI]`, `[URL_MINIATURE_MERCREDI]`) : la miniature YouTube habituelle (1280 × 720), passée dans
  `scripts/miniature-mail.py` (inclus dans le kit) : `python3 miniature-mail.py lundi-4.png lundi-4-mail.jpg`. Le script la ramène à 1072 × 603 px
  (le double des 536 px affichés, net sur les écrans haute définition), incruste le bouton lecture au centre et la compresse (≈ 100 à 150 Ko).
- Le bouton est **dans l'image** : il s'affiche partout, Outlook compris. Pas besoin d'un autre format de miniature.

## Règles d'envoi

- **E-mails « Compte »** (01, 03, 09, 11, 22, 23) : envoyés à tous, même désinscrits des e-mails d'information.
- **E-mails d'information** (tout le reste) : seulement aux personnes qui ont accepté de les recevoir, avec `[LIEN_PREFERENCES]` et `[LIEN_DESINSCRIPTION]`.
- **Pression** : au maximum 3 e-mails d'information par semaine. Une semaine type : programme lundi (07), cours en vidéo jeudi (08).
  Les semaines chargées, la lettre 13 remplace le 08 et regroupe le tournoi et les résultats.
- **Pas de relance d'inactivité** pendant les 5 premiers jours.

## Décisions et points à suivre

- **Pseudo** : le formulaire d'inscription ne demande qu'un pseudo ; les e-mails interpellent le joueur avec `[PSEUDO]` (pas de prénom).
- **Cours en direct** : en visioconférence (Zoom, Teams…) ; `[LIEN_DIRECT]` est le lien de la visio, donné dans le rappel (07) et dans l'e-mail de report (09).
- **Contact** : `[EMAIL_CONTACT]` = europe@echecs.com.
- **Fonctions à venir** (les e-mails sont prêts, à activer quand la fonction existera) : statistiques (14, 24 bilan du mois ; 25 relance à 1 semaine ; 21 bilan de l'année),
  série de jours (15, et la mention dans 05), parties sauvegardées (à ajouter alors dans le 12 : « Analyser mes parties »).
- **Bilan du mois** (le 1er du mois) : actif (≥ 8 jours d'entraînement, 14) ou peu actif (1 à 7 jours, 24). Chiffres présentés comme des compteurs : l'accord est juste quelle que soit la valeur.
- **Inactivité** : 25 après 1 semaine sans activité, 17 après 3 semaines, 18 après 6 semaines ; chacun une seule fois par période d'inactivité.
- **Rappel des cours** : un seul e-mail par semaine, le lundi (07), avec les deux cours ; à tous les joueurs qui acceptent les e-mails d'information.
- **Famille** : les ayants droit (conjoint, enfants…) créent leur propre compte (e-mail 19).
- **Questionnaire** (20) : outil externe anonyme (Google Forms ou équivalent), `[LIEN_QUESTIONNAIRE]`.
- **Inscription** : l'étape 2 (« Suivant ») ne vérifie pas les droits CCAS ; pas d'e-mail de vérification.
- **À fournir** : l'adresse postale de l'éditeur (`[ADRESSE_POSTALE]`).

## Intégration

1. Héberger le dossier `emails-ccas/img/` et remplacer `[URL_IMAGES]` par son adresse.
2. Remplacer chaque variable `[NOM]` par la donnée correspondante. Une variable sans valeur ne doit jamais partir telle quelle.
3. Tester sur Gmail (web et téléphone), Outlook et Apple Mail avant la première vraie campagne.
4. Repères de suivi : `utm_source=email`, `utm_medium=email`, `utm_campaign=ccas-` suivi du nom du fichier.

## Catalogue

### Compte

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `01-confirmation-adresse.html` | À la création du compte (transactionnel) | Confirme ton adresse e-mail | Un clic, et ton compte est prêt. | Compte (toujours envoyé) |
| `02-bienvenue.html` | Juste après la confirmation de l'adresse | Bienvenue sur ta plateforme d’échecs, [PSEUDO] ♟️ | Parcours Initiation, cours en direct, tournois : tout est offert. | Information (désinscription possible) |
| `03-mot-de-passe.html` | Sur demande de réinitialisation (transactionnel) | Réinitialise ton mot de passe | Ce lien est valable 1 heure. | Compte (toujours envoyé) |
| `22-changement-acces.html` | Au moins 30 jours avant tout changement de la plateforme ou des conditions d'accès | Information importante sur ton accès | Ce qui change le [DATE_EFFET]. | Compte (toujours envoyé) |
| `23-suppression-compte.html` | À la suppression du compte (transactionnel, dernier e-mail envoyé) | Ton compte est supprimé | Tes données personnelles ont été effacées. | Compte (toujours envoyé) |

### Démarrage

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `04-demarrage-j1-cours-direct.html` | J+1 après l'inscription | Lundi et mercredi, 18 h 30 : les cours en direct | Éric et Florian t’attendent, et tu peux poser tes questions. | Information (désinscription possible) |
| `05-demarrage-j3-exercices.html` | J+3 après l'inscription | 10 minutes par jour suffisent | Des exercices rangés par thème, pour bien démarrer. | Information (désinscription possible) |
| `06-demarrage-j6-communaute.html` | J+6 après l'inscription | Joue, partage, mesure-toi | Tournois en ligne et forum : rejoins les autres joueurs. | Information (désinscription possible) |

### Cours en direct

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `07-programme-de-la-semaine.html` | Chaque lundi vers 10 h, à tous (les deux cours de la semaine) | Cette semaine : 2 cours en direct à 18 h 30 | Lundi : [THEME_LUNDI]. Mercredi : [THEME_MERCREDI]. | Information (désinscription possible) |
| `08-cours-de-la-semaine.html` | Chaque semaine, le jeudi (cours du lundi et du mercredi) | Les cours de la semaine sont en vidéo 🎥 | Lundi : [THEME_LUNDI]. Mercredi : [THEME_MERCREDI]. | Information (désinscription possible) |
| `09-cours-deplace.html` | Si un cours est déplacé ou annulé (à tous les joueurs qui ont activé les rappels) | Cours du [DATE] déplacé au [NOUVELLE_DATE] | [THEME_COURS], avec [ANIMATEUR] : la nouvelle date. | Compte (toujours envoyé) |
| `26-pause-vacances.html` | Le dernier jour de cours avant une pause (vacances scolaires, été, fin d'année) | Pas de cours en direct jusqu’au [DATE_REPRISE] ☀️ | La plateforme reste ouverte : cours en vidéo, leçons, exercices. | Information (désinscription possible) |
| `27-reprise-cours.html` | Le vendredi avant la reprise des cours en direct | Les cours en direct reprennent lundi à 18 h 30 ! | Au programme : [THEME_LUNDI] avec [ANIMATEUR_LUNDI]. | Information (désinscription possible) |

### Tournois

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `10-annonce-tournoi.html` | 5 jours avant un tournoi, rappel le jour J (même modèle) | Tournoi : [NOM_TOURNOI] le [DATE] | Cadence [CADENCE], ouvert à tous les niveaux. | Information (désinscription possible) |
| `11-inscription-tournoi.html` | À l'inscription à un tournoi (transactionnel) | Inscription confirmée : [NOM_TOURNOI] | Rendez-vous le [DATE] à [HEURE]. | Compte (toujours envoyé) |
| `12-resultats-tournoi.html` | Le lendemain du tournoi, aux participants (ajouter « Analyser mes parties » quand les parties seront sauvegardées) | Résultats : [NOM_TOURNOI] | Tu termines [PLACE]ᵉ sur [NB_JOUEURS] : bravo ! | Information (désinscription possible) |

### Lettre de la semaine

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `13-lettre-de-la-semaine.html` | Les semaines où il y a 2 ou 3 nouvelles (remplace alors l'e-mail 08) | Cette semaine : [TITRE_UNE] | Le cours en vidéo, le prochain tournoi et les résultats du dernier. | Information (désinscription possible) |

### Bilan du mois

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `14-bilan-mois-actif.html` | Le 1er du mois, si au moins 8 jours d'entraînement dans le mois écoulé (à activer avec les statistiques) | [PSEUDO], ton mois d’échecs en chiffres 🔥 | [NB_JOURS_ACTIFS] jours d’entraînement, [NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo ! | Information (désinscription possible) |
| `24-bilan-mois-peu-actif.html` | Le 1er du mois, si 1 à 7 jours d'entraînement dans le mois écoulé (à activer avec les statistiques) | [PSEUDO], ton mois d’échecs : on continue ? | [NB_LECONS] leçons ce mois-ci. 10 minutes de plus par semaine, et ça change tout. | Information (désinscription possible) |

### Réactivation

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `17-inactif-3-semaines.html` | Après 3 semaines sans activité (une seule fois par période d'inactivité ; le 25 est parti à 1 semaine) | Ta progression t’attend, [PSEUDO] | 3 semaines sans échecs : on reprend avant de perdre le fil ? | Information (désinscription possible) |
| `18-inactif-6-semaines.html` | Après 6 semaines sans activité (une seule fois par période d'inactivité ; dernière relance) | Tu nous manques, [PSEUDO] | Voici ce qui est nouveau depuis ta dernière visite. | Information (désinscription possible) |
| `25-inactif-1-semaine.html` | Après 7 jours sans activité (une seule fois par période d'inactivité ; puis 17 à 3 semaines et 18 à 6 semaines ; à activer avec les statistiques) | Ce que tu as manqué cette semaine 👀 | Cours en direct, nouveaux exercices, tournoi : ta place t’attend. | Information (désinscription possible) |

### Engagement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `15-serie-en-danger.html` | Le soir, si la série de jours (≥ 5 jours) va s'interrompre (au plus une fois toutes les 4 semaines par joueur ; à activer avec la série de jours) | Ta série de [SERIE] jours va s’arrêter ⏳ | Un exercice suffit pour la garder. | Information (désinscription possible) |
| `16-reponse-forum.html` | Quand quelqu'un répond à un sujet du joueur (au plus 1 par jour, regroupé) | [AUTEUR_REPONSE] t’a répondu sur le forum | « [EXTRAIT_REPONSE] » | Information (désinscription possible) |

### Partenariat

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `19-echecs-en-famille.html` | J+14 après l'inscription | Et si tu jouais aux échecs en famille ? | Tes ayants droit peuvent aussi créer leur compte, gratuitement. | Information (désinscription possible) |
| `20-questionnaire-satisfaction.html` | J+30 après l'inscription (une seule fois) | 2 minutes pour nous donner ton avis ? | Ce qui te plaît, ce qui manque : on t’écoute. | Information (désinscription possible) |
| `21-bilan-annuel.html` | Un an après l'inscription (à activer avec les statistiques) | [PSEUDO], ta première année d’échecs en chiffres | [NB_LECONS_ANNEE] leçons, [NB_COURS_ANNEE] cours en direct : merci ! | Information (désinscription possible) |

## Variables

La liste complète est générée dans `build/_emails-ccas_variables.txt`.
