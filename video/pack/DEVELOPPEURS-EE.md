# Kit développeurs : e-mails du site europe-echecs.com

Site : https://www.europe-echecs.com/ (Europe Échecs : zone de jeu SimpleChess, Pack Jeu+, Pack Intégral, revue papier, cartes cadeaux).
Ce document dit ce que l'équipe technique doit brancher. Il va avec le kit `kit-developpeurs-ee.zip` :

```
kit-developpeurs-ee/
  DEVELOPPEURS-EE.md   ce document
  EMAILS-EE.md         catalogue des 31 e-mails : quand les envoyer, objet, pré-en-tête, tarifs, règles, décisions
  emails-ee/           31 e-mails en HTML, prêts à intégrer (une variable = [NOM_EN_MAJUSCULES])
  emails-ee/img/       les 3 logos utilisés par les e-mails, à héberger
  emails-ee/apercus/   aperçus remplis avec des exemples (téléphone, ordinateur, mode sombre) : le rendu attendu
  miniature-mail.py    prépare la miniature d'une vidéo pour l'e-mail 28 (1072 × 603, bouton lecture incrusté)
  marque/              logos Europe Échecs (bleu officiel, blanc, jaune) et pastille de l'expéditeur (72 px)
```

Priorités : **(1) avant la mise en service**, (2) au lancement des nouvelles formules, (3) dans le mois qui suit.
Les e-mails 01 à 17, 29 et 30 remplacent des modèles existants du site (correspondance dans `EMAILS-EE.md`) ; 18 à 28 et 31 sont nouveaux.

## 1. Intégration

1. **Héberger `emails-ee/img/`** et remplacer `[URL_IMAGES]` par son adresse dans les 31 fichiers.
2. **Variables** : chaque `[VARIABLE]` est remplacée par la donnée correspondante (§ 3). Aucune ne doit partir telle quelle : valeur par défaut ou pas d'envoi.
3. **Expéditeur** : « Europe Échecs » ; « Le service abonnement » signe les e-mails 10, 16, 29 et 30. Adresse de réponse lue par une personne.
4. **Délivrabilité (1)** : domaine d'envoi authentifié SPF, DKIM, DMARC ; en-têtes `List-Unsubscribe` et `List-Unsubscribe-Post`
   sur les e-mails d'information. La pastille `marque/ee-favicon-72.png` peut servir d'image d'expéditeur (BIMI) si le domaine le permet.
5. **Tests (1)** : chaque e-mail sur Gmail (web et appli), Apple Mail et iPhone (clair et sombre) et Outlook sur PC.
   La police Signika se charge depuis Google Fonts ; Outlook sur PC affiche Arial, sans casser la mise en page.
6. **Pied de page** : « Compte » (toujours envoyé) ou « Information » (lien de désinscription) est déjà réglé dans chaque fichier ; voir la colonne « Type » du catalogue.

## 2. Déclencheurs à brancher

| Événement du site | E-mails | Priorité |
|---|---|---|
| Création de compte (avec activation) | 01 | 1 |
| Compte créé par le gestionnaire d'une offre multicompte | 02 | 1 |
| Demande de nouveau mot de passe | 03 | 1 |
| Suppression du compte | 04 (dernier e-mail envoyé) | 1 |
| Première connexion à la zone de jeu SimpleChess | 05 | 2 |
| Après l'inscription, sans achat | 06 offre de bienvenue (code valable 48 h), puis 24 rappel 24 h plus tard si le code n'a pas servi | 2 |
| Compte créé lors d'un abonnement | 07 | 1 |
| Mise en place d'un abonnement au mois | 08 | 1 |
| Paiement d'une commande reçu | 09 | 1 |
| Échéance d'une formule 1 an ou 2 ans (renouvellement manuel) | 10 (1re relance), puis 29 (2e relance) si rien n'est renouvelé | 1 |
| Annulation d'un abonnement au mois | 11 | 1 |
| Lancement des nouvelles formules, une fois : abonnés Pack Jeu en cours / Pack Progresser en cours | 12 / 13 | 2 |
| Fin d'un ancien Pack Progresser / Pack Jeu | 14 / 15 | 2 |
| Fin d'un abonnement à la revue papier | 16 (1re relance), puis 30 (2e relance) | 1 |
| Achat d'un Pack cadeau | 17 | 1 |
| Échec d'un prélèvement mensuel | 18, puis 31 à J+3 si la carte n'est pas mise à jour | 1 |
| 30 jours avant l'expiration de la carte (formules au mois) | 19 | 2 |
| Chaque prélèvement mensuel | 20 | 1 |
| 30 jours après une fin d'abonnement ou une annulation | 21 | 3 |
| Abonné Pack Jeu+ depuis `[NB_SEMAINES]` semaines (délai à fixer) | 22 | 3 |
| 3e prélèvement mensuel | 23 | 3 |
| Compte gratuit sans connexion depuis 7 / 21 / 45 jours | 25 / 26 / 27 | 3 |
| Chaque semaine | 28 les vidéos de la semaine | 3 |

**Règles** : e-mails d'information seulement aux personnes qui ont accepté (case non pré-cochée) ; au plus 3 par semaine et par personne ;
25, 26 et 27 une seule fois par période d'inactivité ; 22 et 23 une seule fois par abonné ; 21 une seule fois par départ ; pas de 24 si le code a servi ;
après le 27 sans clic sur « Oui, je reste », plus d'e-mails d'information (les e-mails de compte restent envoyés). Heure de Paris, envois entre 8 h et 21 h.

## 3. Données nécessaires (variables)

| Source | Variables |
|---|---|
| Compte | `[PSEUDO]`, `[CODE_ACTIVATION]`, `[MOT_DE_PASSE]` (voir § 5), `[GESTIONNAIRE]` (pseudo du gestionnaire), `[SERVICES_MULTICOMPTE]`, `[DATE_SUPPRESSION]`, `[HEURE_SUPPRESSION]` (GMT) |
| Abonnement | `[SERVICE]` et `[PACK]` (nom de la formule, ex. « Pack Intégral »), `[DATE_FIN]`, `[MONTANT]`, `[MOIS]`, `[DATE_PROCHAIN_PAIEMENT]`, `[MOYEN_PAIEMENT]` (« Carte •••• 4242 »), `[CARTE_4_CHIFFRES]`, `[MOIS_EXPIRATION]`, `[DATE_SUSPENSION]` (fin de l'accès garanti après un paiement refusé) |
| Passage à l'année (23), selon la formule | Pack Jeu+ : `[PRIX_MENSUEL]` = « 4,90 € par mois », `[PRIX_ANNUEL]` = « 39,90 € pour 1 an », `[PRIX_2ANS]` = « 59,90 € », `[ECONOMIE]` = « 18,90 € ». Pack Intégral : « 11,90 € par mois », « 99,90 € pour 1 an », « 149,90 € », « 42,90 € » |
| Commande | `[NUMERO_COMMANDE]`, `[PRODUIT]`, `[QUANTITE]`, `[PRIX_LIGNE]` (une ligne par produit), `[FRAIS_PORT]` (ligne affichée seulement s'ils dépassent 0 €), `[TOTAL]` |
| Offres | `[CODE_PROMO]` (06 et 24), `[PRODUIT_CADEAU]`, `[CODE_CADEAU]` (17 : un bloc par code ; s'il y en a plusieurs, ajouter le bouton « Télécharger tous les codes » vers le PDF groupé), `[OFFRE_RETOUR]` (21 : retirer l'encadré s'il n'y a pas d'offre) |
| Revue | `[ECHEANCE]` (mois du dernier numéro, « janvier 2027 »), `[NUMERO_ABONNE]`, `[EMAIL_CONTACT]` (adresse du service abonnement, à fournir) |
| Saisie éditoriale | `[NOUVEAUTE_1..3]` (21, 26), `[DATE_ENVOI]`, et pour chaque vidéo de l'e-mail 28 : `[SERIE_n]`, `[TITRE_VIDEO_n]`, `[AUTEUR_n]`, `[JOUR_VIDEO_n]`, `[URL_MINIATURE_n]`, `[LIEN_VIDEO_n]` |
| Fixe | `[ADRESSE_POSTALE]` de l'éditeur (pied de page) |

**Liens** (`[LIEN_…]`) : `ACTIVATION`, `MOT_DE_PASSE`, `CONNEXION`, `MON_COMPTE`, `MES_SERVICES`, `MOYEN_PAIEMENT` (mise à jour de la carte), `ABONNEMENTS` (page des formules),
`ZONE_DE_JEU`, `ENTRAINEMENT_TACTIQUE`, `VIDEOS`, `VIDEO_1..3`, `REVUE`, `AIDE`, `CARTE_CADEAU_PDF`, `PREFERENCES`, `DESINSCRIPTION`, `RESTER_ABONNE` (27 : confirme l'envoi des e-mails).
Liens fixes déjà écrits : page des tarifs, tarifs de la revue, activation d'un code cadeau, boutique.echecs.com.
Ajouter `utm_source=email&utm_medium=email&utm_campaign=ee-<nom du fichier>`. Ces tableaux couvrent toutes les variables des 31 e-mails.

## 4. Miniatures des vidéos (e-mail 28)

Chaque semaine, passer la miniature de chaque vidéo (1280 × 720 ou 1000 × 563) dans le script, puis l'héberger :
`python3 miniature-mail.py video-1.jpg video-1-mail.jpg` (Python 3 et Pillow). L'image est ramenée à 1072 × 603 px, avec le bouton lecture au centre.

## 5. Points à trancher avant la mise en service

- **Mot de passe en clair (02, 07)** : les modèles actuels l'envoient dans l'e-mail ; il est conservé pour rester fidèle, mais il vaut mieux le remplacer par un lien « Choisir mon mot de passe » (comme le 03).
- **01** : version avec activation. Sans activation, retirer le bouton et la ligne du code ; connexion par un fournisseur externe : ajouter « Vous avez décidé de vous connecter avec votre compte [FOURNISSEUR]. Vous pouvez aussi vous connecter avec votre pseudo et un mot de passe. »
- **Tarif pack de la revue** (+ 60 € / + 50 €, 14, 15, 30) : à confirmer pour les formules au mois.
- **Délais** des relances 10 / 29 et 16 / 30, délai du 22, durée d'accès après un paiement refusé (18).
- **Tarifs** : écrits en clair dans les e-mails (relevés le 23 novembre 2026, tableau dans `EMAILS-EE.md`). Si un prix change, prévenir pour mettre les e-mails à jour.

## 6. Liste de contrôle avant la mise en service

- [ ] SPF, DKIM, DMARC et désinscription en un clic en place
- [ ] `emails-ee/img/` hébergé, `[URL_IMAGES]` remplacé
- [ ] Les e-mails de priorité 1 intégrés, variables reliées, testés sur Gmail, iPhone (clair et sombre) et Outlook
- [ ] Aucune variable ne part telle quelle (valeur par défaut ou pas d'envoi)
- [ ] Adresse postale de l'éditeur et adresse du service abonnement renseignées
