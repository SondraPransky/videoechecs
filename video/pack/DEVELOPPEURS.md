# Kit développeurs — lancement de l'Académie echecs.com

Ce document dit ce que l'équipe technique doit brancher pour le lancement. Il va avec le **kit développeurs** (`kit-developpeurs.zip`) :

```
kit-developpeurs/
  DEVELOPPEURS.md        ce document
  EMAILS.md              catalogue complet des 43 e-mails : quand les envoyer, objet, pré-en-tête, variables, règles
  emails/                43 e-mails en HTML, prêts à intégrer (une variable = [NOM_EN_MAJUSCULES])
  emails/img/            images des e-mails, à héberger (≈ 2,5 Mo)
  emails/apercus/        aperçus remplis avec des exemples (téléphone, ordinateur, mode sombre) : le rendu attendu
  EMAILS-CCAS.md         les 25 e-mails de la plateforme CCAS (ccas.echecs.com/academy) : accès offert, sans paiement, logo des Activités Sociales
  emails-ccas/           ces 25 e-mails en HTML, avec leurs images (img/) et leurs aperçus (apercus/)
  site/                  vidéo d'en-tête muette (boucle), image de partage du lien (Open Graph)
```

Priorités : **(1) obligatoire avant le lancement**, (2) au lancement, (3) dans le mois qui suit.

---

## 1. E-mails : intégration

1. **Héberger `emails/img/`** sur un domaine echecs.com (ex. `https://echecs.com/mail/img/`) et remplacer `[URL_IMAGES]` par cette adresse dans les 42 fichiers.
2. **Moteur de gabarits** : chaque `[VARIABLE]` est à remplacer par la donnée correspondante (liste au § 3). Aucune variable ne doit partir telle quelle :
   valeur par défaut ou pas d'envoi. Les textes et le HTML ne sont pas à retoucher (sinon nous redemander).
3. **Polices** : Fraunces et Manrope sont chargées depuis Google Fonts dans l'en-tête de chaque e-mail ; Outlook sur PC bascule sur Arial et Georgia (déjà prévu).
4. **Objet et pré-en-tête** : le pré-en-tête est déjà dans le HTML (texte masqué en tête du corps) ; l'objet est dans `EMAILS.md` (colonne « Objet »).
5. **Expéditeur** : « Académie echecs.com », adresse de réponse lue par une personne.
6. **Délivrabilité (1)** : domaine d'envoi authentifié **SPF, DKIM et DMARC** ; en-têtes **`List-Unsubscribe`** et **`List-Unsubscribe-Post: List-Unsubscribe=One-Click`**
   sur tous les e-mails d'information (exigé par Gmail et Yahoo pour les envois en nombre).
7. **Tests (1)** : envoyer chaque e-mail sur Gmail (web + appli), Apple Mail / iPhone et Outlook sur PC avant la première campagne.

## 2. Déclencheurs à brancher

Le détail de chaque e-mail (délai, condition) est dans `EMAILS.md`, section « Catalogue ». Les événements à émettre côté site :

| Événement du site | E-mails | Priorité |
|---|---|---|
| Création de compte | 01 confirmation d'adresse, puis 02 bienvenue | 1 |
| Demande de nouveau mot de passe | 03 | 1 |
| Compte gratuit sans abonnement à J+3, J+7, J+21 | 04, 05, 06 | 2 |
| Page de paiement ouverte sans paiement (2 h après) | 33 | 2 |
| Premier paiement d'abonnement | 07, puis la série de démarrage 10 (J+1), 11 (J+3), 12 (J+6), 13 (J+10) | 1 |
| Échec de prélèvement (+ relance à J+3) | 08 | 1 |
| Renouvellement réussi | 09 | 1 |
| Changement de formule | 34 | 1 |
| Carte bancaire qui expire dans 30 jours | 35 | 2 |
| Abonnement annuel : 30 jours avant le renouvellement | 27 | 1 (obligatoire) |
| Abonné mensuel depuis 3 mois | 28 | 3 |
| Résiliation demandée | 30, puis 29 sept jours avant la fin d'accès | 1 |
| Fin d'abonnement + 30 jours | 31 | 3 |
| Changement de prix ou de conditions (30 jours avant) | 39 | 1 (obligatoire) |
| Suppression du compte | 40 (dernier e-mail envoyé) | 1 |
| 1er du mois, si activité dans le mois | 14 bilan | 3 |
| Module validé | 15 | 2 |
| Série de jours (≥ 5) sur le point de s'arrêter, le soir | 16 | 3 |
| Abonné sans connexion depuis 7 / 30 jours | 17 / 18 | 2 |
| Date anniversaire d'abonnement | 32 | 3 |
| Masterclass programmée (≥ 7 jours avant), veille 18 h et 1 h avant, replay en ligne, report | 19, 20, 21, 37 | 2 |
| Nouveau cours en ligne | 22 | 2 |
| Tournoi programmé (5 jours avant, jour J), inscription, résultats le lendemain | 23, 36, 24 | 2 |
| Sortie d'un numéro de la revue | 25 | 2 |
| Lettre d'information (toutes les 1 à 2 semaines, envoyée à la main) | 26 | 2 |
| Réponse à un sujet du forum (au plus 1 par jour, regroupé) | 38 | 3 |
| Parrainage : J+30 d'abonnement / ami parrainé abonné | 41 / 42 | 3 (offre à définir) |

**Règles d'envoi à coder** : e-mails d'information seulement aux personnes qui ont accepté (case non pré-cochée) ; au plus **3 e-mails d'information par semaine** et par personne ;
pas d'e-mail de conversion (04, 05, 06, 33) aux abonnés ; pas de relance d'inactivité les 5 premiers jours ; heure de Paris ; envois entre 8 h et 21 h sauf rappels de masterclass.

## 3. Données nécessaires (variables)

| Source | Variables |
|---|---|
| Compte | `[PRENOM]`, `[EMAIL_CONTACT]`, `[ADRESSE_POSTALE]` (fixe) |
| Abonnement et paiement | `[FORMULE]`, `[PRIX]`, `[DATE]`, `[DATE_PROCHAIN_PAIEMENT]`, `[MOYEN_PAIEMENT]`, `[CARTE_4_CHIFFRES]`, `[MOIS_EXPIRATION]`, `[DATE_SUSPENSION]`, `[DATE_RENOUVELLEMENT]`, `[DATE_FIN]`, `[DATE_EFFET]`, `[CHANGEMENT]`, `[DUREE_ABONNEMENT]`, `[MOIS]` |
| Progression (statistiques de l'abonné) | `[NB_LECONS]`, `[NB_EXERCICES]`, `[TAUX_REUSSITE]`, `[SERIE]`, `[SERIE_MAX]`, `[THEME_FORT]`, `[THEME_FAIBLE]`, `[MODULE]`, `[MODULE_SUIVANT]`, `[NB_LECONS_MODULE]`, `[NB_EXERCICES_MODULE]`, `[DERNIERE_LECON]`, `[LECON_SUIVANTE]`, `[DUREE_LECON]`, `[NB_LECONS_GRATUITES_RESTANTES]`, `[NB_LECONS_ANNEE]`, `[NB_EXERCICES_ANNEE]`, `[NB_LECONS_TOTAL]`, `[NB_EXERCICES_TOTAL]`, `[NB_MODULES]` |
| Masterclass | `[THEME]`, `[COACH]`, `[TITRE_COACH]`, `[URL_PHOTO_COACH]` (carrée, ≥ 128 px), `[DATE]`, `[JOUR]`, `[MOIS_COURT]`, `[HEURE]`, `[DUREE]`, `[NIVEAU]`, `[DESCRIPTION_MASTERCLASS]`, `[RESUME_MASTERCLASS]`, `[QUAND]`, `[NOUVELLE_DATE]`, `[NOUVEAU_JOUR]`, `[NOUVEAU_MOIS_COURT]` |
| Tournoi | `[NOM_TOURNOI]`, `[DATE]`, `[JOUR]`, `[MOIS_COURT]`, `[HEURE]`, `[CADENCE]`, `[NB_RONDES]`, `[PLACE]`, `[POINTS]`, `[NB_JOUEURS]`, `[VAINQUEUR]`, `[DEUXIEME]`, `[TROISIEME]` |
| Cours, revue, forum | `[TITRE_COURS]`, `[AUTEUR]`, `[NB_LECONS_COURS]`, `[DESCRIPTION_COURS]`, `[NUMERO]`, `[SOMMAIRE_1..3]`, `[AUTEUR_REPONSE]`, `[TITRE_SUJET]`, `[EXTRAIT_REPONSE]` |
| Saisie éditoriale (lettre, réactivation) | `[TITRE_UNE]`, `[NOUVEAUTE_1..3]`, `[CONSIGNE_PUZZLE]`, `[URL_IMAGE_PUZZLE]`, `[DATE_FIN_OFFRE]` |
| Parrainage | `[CODE_PARRAINAGE]`, `[PRENOM_FILLEUL]`, `[OFFRE_FILLEUL]`, `[RECOMPENSE_PARRAIN]` |

**Liens** (`[LIEN_…]`, une adresse de page du site par variable) : la liste complète est dans `EMAILS.md`. Ajouter à chaque lien
`utm_source=email&utm_medium=email&utm_campaign=<nom du fichier>` (ex. `05-gratuit-j7-offre`).

## 4. Pages et fonctions à créer sur le site

| Page / fonction | Pourquoi | Priorité |
|---|---|---|
| **Préférences e-mails + désinscription en un clic** (sans connexion) | RGPD, et exigé par Gmail / Yahoo | 1 |
| **Gestion de l'abonnement** : changer de carte, de formule, **résilier en ligne** | Obligation légale (résiliation en quelques clics) | 1 |
| **Factures** téléchargeables (ou PDF joint aux e-mails 07 et 09) | Obligation de facturation | 1 |
| **Conditions générales de vente** à jour (prix, durée, résiliation, rétractation) | Obligatoire, lien dans l'e-mail 39 | 1 |
| **Compte gratuit** : 6 leçons, forum, puzzle du jour ; offre de lancement 14,90 €/mois, 150 €/an | Message de toutes les pubs | 1 |
| **Test de placement** relié à l'e-mail 10 (`[LIEN_TEST_PLACEMENT]`) | Démarrage des abonnés | 2 |
| **Image du puzzle du jour** : PNG carré 600 px de l'échiquier (`[URL_IMAGE_PUZZLE]`) | Lettre d'information | 2 |
| **Photos des coachs** à une adresse stable (`[URL_PHOTO_COACH]`) | E-mail 19 | 2 |
| **Questionnaire de départ** (une question à choix) | E-mail 30 | 3 |
| **Parrainage** : un code et un lien par abonné, suivi des filleuls, récompense | E-mails 41, 42 (offre à définir) | 3 |
| **Ajout à l'agenda** (.ics) pour les masterclasses | Confort | 3 |

## 5. Page d'arrivée `echecs.com/academie` et suivi (1)

- **Reprendre le message des pubs** : les 5 questions (« Tu enchaînes les parties… ? »), les 4 coachs, l'offre de lancement (14,90 €/mois au lieu de 19,90 €, 150 €/an au lieu de 179,90 €), le compte gratuit.
- **Conserver les paramètres UTM** jusqu'à l'inscription et au paiement (les enregistrer avec le compte) : c'est ce qui permet de savoir quelle pub et quel réseau amènent des abonnés.
- **Pixels** : Meta (Facebook / Instagram) et TikTok, avec les événements standard `CompleteRegistration` (compte créé), `InitiateCheckout` (page de paiement) et `Purchase` / `Subscribe` (avec la valeur et la devise).
  Idéalement aussi l'API de conversions côté serveur (Meta CAPI, TikTok Events API) pour ne pas perdre les mesures bloquées par les navigateurs.
- **Statistiques du site** (GA4 ou autre) : les mêmes événements, et un tableau par `utm_source`, `utm_campaign`, `utm_content`.
- **Bandeau de consentement** aux cookies avant de charger les pixels.
- **Partage du lien** (balises Open Graph) : image `site/partage-lien-1200x630.jpg`, titre « L'Académie echecs.com », description « Progresse à ton rythme : +200 leçons, +2 000 exercices, masterclasses, tournois. »
- **En-tête de page** : la boucle vidéo muette `site/boucle-entete-site-muette-1920x1080.mp4` (et sa version 1280×720 pour les petits écrans), en lecture automatique, muette, en boucle.

## 6. Liste de contrôle avant le lancement

- [ ] SPF, DKIM, DMARC et désinscription en un clic en place
- [ ] Les 43 e-mails intégrés, variables reliées, testés sur Gmail, iPhone et Outlook
- [ ] Déclencheurs priorité 1 branchés (compte, paiement, résiliation, renouvellement annuel, suppression)
- [ ] Pages préférences, gestion d'abonnement, factures, CGV en ligne
- [ ] Page d'arrivée avec l'offre, UTM conservés jusqu'au paiement, pixels Meta et TikTok, événements de conversion vérifiés
- [ ] Compte gratuit (6 leçons, forum, puzzle du jour) et prix de lancement actifs dans le paiement
