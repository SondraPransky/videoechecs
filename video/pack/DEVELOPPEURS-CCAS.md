# Kit développeurs — e-mails de la plateforme d'échecs CCAS

Plateforme : https://ccas.echecs.com/academy/ — accès offert aux bénéficiaires des Activités Sociales de l'Énergie et à leurs ayants droit,
**sans abonnement ni paiement**. Ce document dit ce que l'équipe technique doit brancher. Il va avec le kit `kit-developpeurs-ccas.zip` :

```
kit-developpeurs-ccas/
  DEVELOPPEURS-CCAS.md   ce document
  EMAILS-CCAS.md         catalogue des 27 e-mails : quand les envoyer, objet, pré-en-tête, règles, décisions
  emails-ccas/           27 e-mails en HTML, prêts à intégrer (une variable = [NOM_EN_MAJUSCULES])
  emails-ccas/img/       images des e-mails, à héberger (≈ 1 Mo)
  emails-ccas/apercus/   aperçus remplis avec des exemples (téléphone, ordinateur, mode sombre) : le rendu attendu
  miniature-mail.py      prépare la miniature YouTube d'un cours pour les e-mails 08 et 13 (bouton lecture incrusté, 1072 × 603)
  marque/                logo web « activités sociales de l'énergie » (SVG) et favicon CCAS (32 à 144 px)
```

Priorités : **(1) obligatoire avant l'ouverture**, (2) à l'ouverture, (3) dans le mois qui suit.

## 1. Intégration

1. **Héberger `emails-ccas/img/`** et remplacer `[URL_IMAGES]` par son adresse dans les 27 fichiers.
2. **Variables** : chaque `[VARIABLE]` est remplacée par la donnée correspondante (§ 3). Aucune ne doit partir telle quelle : valeur par défaut ou pas d'envoi.
3. **Expéditeur** : « Europe Échecs · Activités Sociales », adresse de réponse lue par une personne. Contact affiché : europe@echecs.com.
4. **Délivrabilité (1)** : domaine d'envoi authentifié SPF, DKIM, DMARC ; en-têtes `List-Unsubscribe` et `List-Unsubscribe-Post` sur les e-mails d'information.
   Le favicon CCAS (`marque/`) peut servir d'image d'expéditeur (BIMI) si le domaine le permet.
5. **Tests (1)** : chaque e-mail sur Gmail (web + appli), Apple Mail / iPhone (clair et sombre) et Outlook sur PC.

## 2. Déclencheurs à brancher

| Événement de la plateforme | E-mails | Priorité |
|---|---|---|
| Création de compte | 01 confirmation d'adresse, puis 02 bienvenue | 1 |
| Demande de nouveau mot de passe | 03 | 1 |
| Après l'inscription : J+1, J+3, J+6 | 04 cours en direct, 05 exercices, 06 communauté | 2 |
| Chaque lundi vers 10 h | 07 programme de la semaine (les deux cours, lien de la visio) | 1 |
| Chaque jeudi (vidéos des cours en ligne) | 08 les cours de la semaine | 2 |
| Cours déplacé ou annulé | 09 | 1 |
| Tournoi (5 jours avant et jour J), inscription, résultats le lendemain | 10, 11, 12 | 2 |
| Semaine chargée : lettre à plusieurs nouvelles (remplace le 08) | 13 | 3 |
| Dimanche vers 18 h : bilan de la semaine selon les jours d'entraînement (≥ 3 / 1-2 / 0), avec les statistiques | 14 / 26 / 27 | 2 |
| Série de jours (≥ 5) sur le point de s'arrêter (avec la série de jours) | 15 | 3 |
| Réponse à un sujet du forum (au plus 1 par jour) | 16 | 3 |
| Sans connexion depuis 7 / 30 jours | 17 / 18 | 2 |
| J+14 / J+30 / 1 an après l'inscription | 19 famille / 20 questionnaire / 21 bilan de l'année | 3 |
| Changement de la plateforme ou de l'accès (30 jours avant) | 22 | 1 |
| Suppression du compte | 23 (dernier e-mail envoyé) | 1 |
| Étape 2 de l'inscription, **si elle contrôle les droits** : vérification à la main / refus | 24 / 25 | 1 si contrôle |

**Règles** : e-mails d'information seulement aux personnes qui ont accepté (case non pré-cochée) ; au plus 3 par semaine et par personne ;
pas de relance d'inactivité les 5 premiers jours ; heure de Paris, envois entre 8 h et 21 h.

## 3. Données nécessaires (variables)

| Source | Variables |
|---|---|
| Compte | `[PSEUDO]` (pas de prénom à l'inscription), `[EMAIL_CONTACT]` = europe@echecs.com, `[ADRESSE_POSTALE]` (fixe, à fournir) |
| Cours en direct | `[THEME_LUNDI]`, `[THEME_MERCREDI]`, `[ANIMATEUR_LUNDI]`, `[ANIMATEUR_MERCREDI]`, `[JOUR_LUNDI]`, `[JOUR_MERCREDI]`, `[MOIS_COURT]`, `[DUREE_LUNDI]`, `[DUREE_MERCREDI]`, `[URL_MINIATURE_LUNDI]`, `[URL_MINIATURE_MERCREDI]`, `[THEME_PROCHAIN_LUNDI]`, `[THEME_PROCHAIN_MERCREDI]`, `[THEME_COURS]`, `[ANIMATEUR]`, `[DATE]`, `[NOUVELLE_DATE]`, `[NOUVEAU_JOUR]`, `[NOUVEAU_MOIS_COURT]`, `[HEURE]` |
| Tournoi | `[NOM_TOURNOI]`, `[NOM_TOURNOI_PRECEDENT]`, `[DATE]`, `[JOUR]`, `[MOIS_COURT]`, `[HEURE]`, `[CADENCE]`, `[NB_RONDES]`, `[PLACE]`, `[POINTS]`, `[NB_JOUEURS]`, `[VAINQUEUR]`, `[DEUXIEME]`, `[TROISIEME]` |
| Statistiques (à venir) | `[SEMAINE]`, `[NB_JOURS_ACTIFS]`, `[NB_PARTIES]`, `[SERIE]`, `[PROGRESSION_PARCOURS]` (0 à 100), `[NB_COURS_SEMAINE]`, `[NB_NOUVEAUX_EXERCICES]`, `[NB_TOURNOIS_SEMAINE]`, `[NB_LECONS]`, `[NB_EXERCICES]`, `[TAUX_REUSSITE]`, `[NB_COURS_SUIVIS]`, `[THEME_FORT]`, `[THEME_FAIBLE]`, `[SERIE]`, `[DERNIERE_LECON]`, `[LECON_SUIVANTE]`, `[DUREE_LECON]`, `[NB_LECONS_ANNEE]`, `[NB_EXERCICES_ANNEE]`, `[NB_COURS_ANNEE]`, `[NB_TOURNOIS_ANNEE]`, `[MOIS]` |
| Forum | `[AUTEUR_REPONSE]`, `[TITRE_SUJET]`, `[EXTRAIT_REPONSE]` |
| Saisie éditoriale | `[TITRE_UNE]`, `[NOUVEAUTE_1..3]`, `[DATE_EFFET]`, `[CHANGEMENT]`, `[DELAI_VERIFICATION]` |

**Liens** (`[LIEN_…]`) : la liste complète est générée dans le catalogue (`EMAILS-CCAS.md`). `[LIEN_DIRECT]` = lien de la visioconférence (le même pour les deux cours),
`[LIEN_YOUTUBE_LUNDI]` / `[LIEN_YOUTUBE_MERCREDI]` = vidéos, `[LIEN_COURS_LUNDI]` / `[LIEN_COURS_MERCREDI]` = leçons sur la plateforme, `[LIEN_QUESTIONNAIRE]` = formulaire anonyme (Google Forms…).
Ajouter `utm_source=email&utm_medium=email&utm_campaign=ccas-<nom du fichier>`.

## 4. Miniatures des cours (e-mails 08 et 13)

Chaque semaine, passer les deux miniatures YouTube (1280 × 720) dans le script, puis les héberger :
`python3 miniature-mail.py lundi-4.png lundi-4-mail.jpg mercredi-4.png mercredi-4-mail.jpg` (Python 3 et Pillow). L'image est ramenée à 1072 × 603 px, avec le bouton lecture au centre (≈ 100 à 150 Ko).

## 5. Pages et fonctions

| Page / fonction | Pourquoi | Priorité |
|---|---|---|
| **Préférences e-mails + désinscription en un clic** (sans connexion) | RGPD, exigé par Gmail / Yahoo | 1 |
| **Page « Cours en direct »** : programme, lien de la visio, vidéos des cours passés | E-mails 04, 07, 08, 09 | 1 |
| **Statistiques, série de jours, parties sauvegardées** | E-mails 05, 12, 14, 15, 21, 26, 27 (à activer avec la fonction) | 3 |
| **Vérification des droits** à l'étape 2 de l'inscription, si prévue | E-mails 24, 25 | à décider |

## 6. Liste de contrôle avant l'ouverture

- [ ] SPF, DKIM, DMARC et désinscription en un clic en place
- [ ] Les e-mails de priorité 1 intégrés, variables reliées, testés sur Gmail, iPhone (clair et sombre) et Outlook
- [ ] Envoi du lundi (07) avec le lien de la visio, et du jeudi (08) avec les miniatures préparées
- [ ] Adresse postale de l'éditeur renseignée dans le pied de page
