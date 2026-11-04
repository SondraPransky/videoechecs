# E-mails des bénéficiaires CCAS — plateforme d'échecs des Activités Sociales de l'Énergie

25 e-mails pour les joueurs de https://ccas.echecs.com/academy/ : **un fichier HTML par e-mail** dans `emails-ccas/`,
les images à héberger dans `emails-ccas/img/`. Même moteur et même design que les e-mails de l'Académie echecs.com
(`scripts/emails.py ccas`, contenu dans `scripts/emails-contenu-ccas.py`).

**Ce qui change par rapport à l'Académie echecs.com :**
- **Aucun abonnement, aucun paiement** : pas d'offre, de prix, de reçu ni de relance de paiement. L'accès est offert par le partenariat et n'a pas de fin prévue.
- **Marque** : logo des Activités Sociales de l'Énergie (CCAS) en en-tête, **pas de logo echecs.com**. Expéditeur « Europe Echecs · Activités Sociales » ;
  signature « L'équipe Europe Echecs, en partenariat avec les Activités Sociales de l'Énergie ». Pas de liens vers les réseaux d'echecs.com dans le pied de page.
- **Contenu** : leçons et exercices, tournois en ligne, forum, et **cours en direct le lundi et le mercredi à 18 h 30** avec Eric et Florian.
  Pas de masterclasses ni de revue.

## Le parcours d'un joueur

```
Création du compte ──► 01 Confirme ton adresse ──► 02 Bienvenue (tout est offert)
        │
        ▼
Démarrage : J+1 04 Ton parcours ──► J+2 05 Cours en direct ──► J+4 06 Exercices ──► J+7 07 Communauté
Partenariat : J+14 21 Les échecs en famille ──► J+30 22 Questionnaire de satisfaction ──► 1 an 23 Bilan de l'année
        │
        ├── cours en direct : 08 Rappel (lundi et mercredi, vers 16 h) · 09 Les cours de la semaine (jeudi, vidéos YouTube) · 10 Cours déplacé
        ├── tournois        : 11 Annonce (J-5 et jour J) · 12 Inscription confirmée · 13 Résultats
        ├── lettre          : 14 Lettre de la semaine (2 ou 3 nouvelles mélangées : cours en vidéo, tournoi, résultats ; remplace alors le 09)
        ├── en continu      : 15 Bilan du mois · 16 Module validé · 17 Série en danger · 18 Réponse sur le forum
        ├── réactivation    : 19 Inactif 7 j · 20 Inactif 30 j
        └── compte          : 24 Changement de la plateforme ou de l'accès (30 jours avant) · 25 Suppression du compte (RGPD)
```

## Design

Identique aux e-mails de l'Académie (voir `EMAILS.md`), sauf l'en-tête : bande blanche avec le logo des Activités Sociales de l'Énergie
(`img/logo.png`, tiré du fichier officiel `2022_logo_AS_CCAS_CMJN_ocean`), qui reste blanche en mode sombre pour garder le logo lisible.

**Bloc vidéo** (e-mails 09 et 14) : la miniature YouTube du cours (16:9, ex. `https://i.ytimg.com/vi/<id>/maxresdefault.jpg`) avec un bouton lecture,
cliquable vers YouTube ; en dessous, le thème, le jour, l'animateur, la durée, et deux liens : « Revoir le cours » (la leçon sur la plateforme) et « Sur YouTube ».

## Règles d'envoi

- **E-mails « Compte »** (01, 03, 10, 12, 24, 25) : envoyés à tous, même désinscrits des e-mails d'information.
- **E-mails d'information** (tout le reste) : seulement aux personnes qui ont accepté de les recevoir, avec `[LIEN_PREFERENCES]` et `[LIEN_DESINSCRIPTION]`.
- **Pression** : au maximum 3 e-mails d'information par semaine. Une semaine type : rappel lundi, rappel mercredi, cours de la semaine jeudi.
  Les semaines chargées, la lettre 14 remplace le 09 et regroupe le tournoi et les résultats.
- **Rappels de cours (08)** : seulement aux joueurs qui les ont activés (case à cocher dans les préférences), sinon c'est trop fréquent.
- **Pas de relance d'inactivité** pendant les 5 premiers jours.

## À confirmer

- La 2ᵉ étape de l'inscription (« Suivant » sur la page de création de compte) : si elle vérifie les droits CCAS, prévoir un e-mail « compte validé » ou « droits non reconnus ».
- Qui peut s'inscrire dans la famille (e-mail 21 : « les membres de ta famille qui bénéficient des Activités Sociales »).
- L'adresse de contact (`[EMAIL_CONTACT]`) et l'adresse postale de l'éditeur (`[ADRESSE_POSTALE]`).
- Les noms complets d'Eric et Florian, si on veut les afficher.

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
| `02-bienvenue.html` | Juste après la confirmation de l'adresse | Bienvenue sur ta plateforme d’échecs, [PRENOM] ♟️ | Leçons, exercices, cours en direct, tournois : tout est offert. | Information (désinscription possible) |
| `03-mot-de-passe.html` | Sur demande de réinitialisation (transactionnel) | Réinitialise ton mot de passe | Ce lien est valable 1 heure. | Compte (toujours envoyé) |
| `24-changement-acces.html` | Au moins 30 jours avant tout changement de la plateforme ou des conditions d'accès | Information importante sur ton accès | Ce qui change le [DATE_EFFET]. | Compte (toujours envoyé) |
| `25-suppression-compte.html` | À la suppression du compte (transactionnel, dernier e-mail envoyé) | Ton compte est supprimé | Tes données personnelles ont été effacées. | Compte (toujours envoyé) |

### Démarrage

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `04-demarrage-j1-parcours.html` | J+1 après l'inscription | Par où commencer ? Ton parcours en 3 étapes | De l’initiation au niveau confirmé : trouve ton niveau. | Information (désinscription possible) |
| `05-demarrage-j2-cours-direct.html` | J+2 après l'inscription | Lundi et mercredi, 18 h 30 : les cours en direct | Eric et Florian t’attendent, et tu peux poser tes questions. | Information (désinscription possible) |
| `06-demarrage-j4-exercices.html` | J+4 après l'inscription | 10 minutes par jour suffisent | Des exercices rangés par thème et par niveau. | Information (désinscription possible) |
| `07-demarrage-j7-communaute.html` | J+7 après l'inscription | Joue, partage, mesure-toi | Tournois en ligne et forum : rejoins les autres joueurs. | Information (désinscription possible) |

### Cours en direct

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `08-rappel-cours-direct.html` | Le lundi et le mercredi, vers 16 h (aux joueurs qui ont activé les rappels) | Ce soir 18 h 30 : [THEME_COURS] | Cours en direct avec [ANIMATEUR]. Prépare tes questions ! | Information (désinscription possible) |
| `09-cours-de-la-semaine.html` | Chaque semaine, le jeudi (cours du lundi et du mercredi) | Les cours de la semaine : [THEME_LUNDI], [THEME_MERCREDI] | Tu les as manqués ? Revois-les en vidéo. | Information (désinscription possible) |
| `10-cours-deplace.html` | Si un cours est déplacé ou annulé (à tous les joueurs qui ont activé les rappels) | Cours du [DATE] déplacé au [NOUVELLE_DATE] | [THEME_COURS], avec [ANIMATEUR] : la nouvelle date. | Compte (toujours envoyé) |

### Tournois

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `11-annonce-tournoi.html` | 5 jours avant un tournoi, rappel le jour J (même modèle) | Tournoi : [NOM_TOURNOI] le [DATE] | Cadence [CADENCE], ouvert à tous les niveaux. | Information (désinscription possible) |
| `12-inscription-tournoi.html` | À l'inscription à un tournoi (transactionnel) | Inscription confirmée : [NOM_TOURNOI] | Rendez-vous le [DATE] à [HEURE]. | Compte (toujours envoyé) |
| `13-resultats-tournoi.html` | Le lendemain du tournoi, aux participants | Résultats : [NOM_TOURNOI] | Tu termines [PLACE]ᵉ sur [NB_JOUEURS] : bravo ! | Information (désinscription possible) |

### Lettre de la semaine

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `14-lettre-de-la-semaine.html` | Les semaines où il y a 2 ou 3 nouvelles (remplace alors l'e-mail 09) | Cette semaine : [TITRE_UNE] | Le cours en vidéo, le prochain tournoi et les résultats du dernier. | Information (désinscription possible) |

### Engagement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `15-bilan-mensuel.html` | Le 1er de chaque mois, si au moins une activité dans le mois | [PRENOM], ton mois d’échecs en chiffres | [NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo ! | Information (désinscription possible) |
| `16-module-valide.html` | Quand le joueur valide un module ou un parcours | Module validé : [MODULE] 🎉 | Une étape de plus vers ton objectif. | Information (désinscription possible) |
| `17-serie-en-danger.html` | Le soir, si la série de jours (≥ 5 jours) va s'interrompre | Ta série de [SERIE] jours va s’arrêter ⏳ | Un exercice suffit pour la garder. | Information (désinscription possible) |
| `18-reponse-forum.html` | Quand quelqu'un répond à un sujet du joueur (au plus 1 par jour, regroupé) | [AUTEUR_REPONSE] t’a répondu sur le forum | « [EXTRAIT_REPONSE] » | Information (désinscription possible) |

### Réactivation

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `19-inactif-7-jours.html` | Sans connexion depuis 7 jours | Ta prochaine leçon t’attend | On reprend là où tu en étais ? | Information (désinscription possible) |
| `20-inactif-30-jours.html` | Sans connexion depuis 30 jours | Tu nous manques, [PRENOM] | Voici ce qui est nouveau depuis ta dernière visite. | Information (désinscription possible) |

### Partenariat

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `21-echecs-en-famille.html` | J+14 après l'inscription | Et si tu jouais aux échecs en famille ? | Tes proches bénéficiaires peuvent aussi créer leur compte. | Information (désinscription possible) |
| `22-questionnaire-satisfaction.html` | J+30 après l'inscription (une seule fois) | 2 minutes pour nous donner ton avis ? | Ce qui te plaît, ce qui manque : on t’écoute. | Information (désinscription possible) |
| `23-bilan-annuel.html` | Un an après l'inscription | [PRENOM], ta première année d’échecs en chiffres | [NB_LECONS_ANNEE] leçons, [NB_COURS_ANNEE] cours en direct : merci ! | Information (désinscription possible) |

## Variables

La liste complète est générée dans `build/_emails-ccas_variables.txt`.
