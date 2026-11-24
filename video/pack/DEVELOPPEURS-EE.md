# Kit développeurs : e-mails du site europe-echecs.com

Site : https://www.europe-echecs.com/ (Europe Échecs : zone de jeu SimpleChess, Pack Jeu+, Pack Intégral, revue papier, cartes cadeaux).
Ce document dit ce que l'équipe technique doit brancher. Il va avec le kit `kit-developpeurs-ee.zip` :

```
kit-developpeurs-ee/
  DEVELOPPEURS-EE.md   ce document
  EMAILS-EE.md         catalogue des 32 e-mails : quand les envoyer, objet, pré-en-tête, tarifs, règles, décisions
  emails-ee/           32 e-mails en HTML, prêts à intégrer (une variable = [NOM_EN_MAJUSCULES])
  emails-ee/img/       les 3 logos utilisés par les e-mails, à héberger
  emails-ee/apercus/   aperçus remplis avec des exemples (téléphone, ordinateur, mode sombre) : le rendu attendu
  miniature-mail.py    prépare la miniature d'une vidéo pour l'e-mail 28 (1072 × 603, bouton lecture incrusté)
  marque/              logos Europe Échecs (bleu officiel, blanc, jaune) et pastille de l'expéditeur (72 px)
```

Priorités : **(1) avant la mise en service**, (2) au lancement des nouvelles formules, (3) dans le mois qui suit.
Les e-mails 01 à 17, 29 et 30 remplacent des modèles existants du site (correspondance dans `EMAILS-EE.md`) ; 18 à 28, 31 et 32 sont nouveaux.

## 1. Intégration

1. **Héberger `emails-ee/img/`** et remplacer `[URL_IMAGES]` par son adresse dans les 32 fichiers.
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
| Échéance d'une formule 1 an ou 2 ans (renouvellement manuel) | 10 à J-15, puis 29 à J-3 si rien n'est renouvelé | 1 |
| Formule 1 an ou 2 ans arrivée à échéance sans renouvellement | 32 à J+1 | 2 |
| Annulation d'un abonnement au mois | 11 | 1 |
| Lancement des nouvelles formules, une fois : abonnés Pack Jeu en cours / Pack Progresser en cours | 12 / 13 | 2 |
| Fin d'un ancien Pack Progresser / Pack Jeu | 14 / 15 | 2 |
| Fin prochaine d'un abonnement à la revue papier | 16 le 25, puis 30 le 8 du mois suivant si rien n'est renouvelé | 1 |
| Achat d'un Pack cadeau | 17 | 1 |
| Échec d'un prélèvement mensuel (accès suspendu tout de suite) | 18, puis 31 à J+3 si la carte n'est pas mise à jour | 1 |
| 30 jours avant l'expiration de la carte (formules au mois) | 19 | 2 |
| Chaque prélèvement mensuel | 20 | 1 |
| 30 jours après une fin d'abonnement ou une annulation | 21 | 3 |
| Abonné Pack Jeu+ depuis un délai à fixer (pas en place aujourd'hui) | 22 | 3 |
| 3e prélèvement mensuel | 23 | 3 |
| Compte gratuit sans connexion depuis 7 / 21 / 45 jours | 25 / 26 / 27 | 3 |
| Chaque semaine, après la Minute Finale du vendredi | 28 les vidéos de la semaine | 3 |

**Règles** : e-mails d'information seulement aux personnes qui ont accepté (case non pré-cochée) ; au plus 3 par semaine et par personne ;
25, 26 et 27 une seule fois par période d'inactivité ; 22 et 23 une seule fois par abonné ; 21 une seule fois par départ ; pas de 24 si le code a servi ;
après le 27 sans clic sur « Oui, je reste », plus d'e-mails d'information (les e-mails de compte restent envoyés). Heure de Paris, envois entre 8 h et 21 h.

## 3. Données nécessaires (variables)

| Source | Variables |
|---|---|
| Compte | `[PSEUDO]`, `[CODE_ACTIVATION]`, `[GESTIONNAIRE]` (pseudo du gestionnaire), `[SERVICES_MULTICOMPTE]`, `[DATE_SUPPRESSION]`, `[HEURE_SUPPRESSION]` (GMT) |
| Abonnement | `[SERVICE]` et `[PACK]` (nom de la formule, ex. « Pack Intégral »), `[DATE_FIN]`, `[MONTANT]`, `[MOIS]`, `[DATE_PROCHAIN_PAIEMENT]`, `[MOYEN_PAIEMENT]` (« Carte •••• 4242 »), `[CARTE_4_CHIFFRES]`, `[MOIS_EXPIRATION]` |
| Passage à l'année (23), selon la formule | Pack Jeu+ : `[PRIX_MENSUEL]` = « 4,90 € par mois », `[PRIX_ANNUEL]` = « 39,90 € pour 1 an », `[PRIX_2ANS]` = « 59,90 € », `[ECONOMIE]` = « 18,90 € ». Pack Intégral : « 11,90 € par mois », « 99,90 € pour 1 an », « 149,90 € », « 42,90 € » |
| Commande | `[NUMERO_COMMANDE]`, `[PRODUIT]`, `[QUANTITE]`, `[PRIX_LIGNE]` (une ligne par produit), `[FRAIS_PORT]` (ligne affichée seulement s'ils dépassent 0 €), `[TOTAL]` |
| Offres | `[CODE_PROMO]` (06 et 24), `[PRODUIT_CADEAU]`, `[CODE_CADEAU]` (17 : un bloc par code ; s'il y en a plusieurs, ajouter le bouton « Télécharger tous les codes » vers le PDF groupé) |
| Revue | `[ECHEANCE]` (mois du dernier numéro, « janvier 2027 »), `[NUMERO_ABONNE]` (le contact passe par `[LIEN_AIDE]`, la page d'aide) |
| Saisie éditoriale | `[NOUVEAUTE_1..3]` (21, 26), `[DATE_ENVOI]`, et pour chaque vidéo de l'e-mail 28 (1 La Minute Stratégie du lundi, 2 Coup de Légende du mardi, 3 Calcul Gagnant du mercredi, 4 La Minute Finale du vendredi ; série et jour déjà écrits) : `[TITRE_VIDEO_n]`, `[AUTEUR_n]`, `[URL_MINIATURE_n]`, `[LIEN_VIDEO_n]`. Les semaines avec une vidéo du dimanche (1 ou 2 par mois), ajouter une 5e carte sur le même modèle |

**Liens** (`[LIEN_…]`) : `ACTIVATION`, `MOT_DE_PASSE`, `CONNEXION`, `MES_SERVICES`, `MOYEN_PAIEMENT` (mise à jour de la carte), `ABONNEMENTS` (page des formules),
`ZONE_DE_JEU`, `ENTRAINEMENT_TACTIQUE`, `VIDEOS`, `VIDEO_1..4`, `REVUE`, `AIDE`, `CARTE_CADEAU_PDF`, `PREFERENCES`, `DESINSCRIPTION`, `RESTER_ABONNE` (27 : confirme l'envoi des e-mails).
Liens fixes déjà écrits : page des tarifs, tarifs de la revue, activation d'un code cadeau, boutique.echecs.com.
Ajouter `utm_source=email&utm_medium=email&utm_campaign=ee-<nom du fichier>`. Ces tableaux couvrent toutes les variables des 32 e-mails.

## 4. Miniatures des vidéos (e-mail 28)

Chaque semaine, passer la miniature de chaque vidéo (1280 × 720 ou 1000 × 563) dans le script, puis l'héberger :
`python3 miniature-mail.py video-1.jpg video-1-mail.jpg` (Python 3 et Pillow). L'image est ramenée à 1072 × 603 px, avec le bouton lecture au centre.

## 4 bis. E-mails envoyés depuis Mailjet (33, 34, 39 à 43)

Newsletter (33), promo boutique (34), Noël (39 à 41),
nouveau numéro de la revue (42) et problème de la semaine (43) ne partent pas du site mais de Mailjet. Fichiers prêts à coller : `emails-ee/mailjet/`.
Liens utiles relevés sur le site le 24 novembre 2026 : guide cadeaux (`https://www.europe-echecs.com/art/quel-cadeau-offrir-a-un-joueur-d-echecs-le-guide-2026-8904.html`),
packs cadeaux (`https://boutique.echecs.com/15-packs-cadeaux`), Pack Steinitz (`https://boutique.echecs.com/histoire/1144-pack-steinitz.html`),
revue papier + Pack Jeu+ (`https://boutique.echecs.com/pack-jeu/1341-revue-papier-pack-jeu-plus-france-1-an.html`), sweat-shirts (`https://boutique.echecs.com/25-sweats`).

1. Mailjet → Modèles → Créer un modèle → **Coder votre propre modèle (HTML)**, puis coller le fichier.
2. Remplacer `[URL_IMAGES]` (logo) par l'adresse où est hébergé `emails-ee/img/`, comme pour les autres e-mails.
3. Chaque envoi : remplacer les textes d'exemple (newsletter du 23 novembre, promo sweat-shirts du 4 novembre), puis
   `[URL_IMAGE_ARTICLE_n]` / `[URL_IMAGE_ENCART]` / `[URL_IMAGE_PRODUIT]` par l'adresse de l'image chargée dans Mailjet (550 px de large minimum, idéalement 1100 px),
   et `[LIEN_ARTICLE_n]` / `[LIEN_ENCART]` / `[LIEN_PRODUIT]` par les liens.
4. Newsletter : un article à la une, puis autant d'articles que nécessaire. Chaque bloc est repéré par un commentaire
   `<!-- ARTICLE n -->` : le dupliquer ou le supprimer. Un seul encart boutique au plus (`<!-- ENCART BOUTIQUE -->`), facultatif.
5. Pied : `[LIEN_ZONE_DE_JEU]`, `[LIEN_VIDEOS]`, `[LIEN_REVUE]`, `[LIEN_AIDE]` à remplacer une fois pour toutes par les adresses du site.
   La désinscription utilise la balise Mailjet `[[UNSUB_LINK_FR]]` : vérifier sur un envoi de test qu'elle est bien remplacée.
6. Objet et pré-en-tête : à saisir dans Mailjet à chaque envoi (exemples dans `EMAILS-EE.md`).

## 4 ter. E-mails 44 à 50 (envoyés par le site) : données à créer

Bilan du mois (44), cap franchi (45), panier abandonné (46), satisfaction à 30 jours (47), anniversaire (48), votre année (49), revue papier vers le web (50).
Les données ci-dessous sont à créer côté site si elles n'existent pas encore (par compte, sauf mention contraire).

| Donnée | Variable | E-mails |
|---|---|---|
| Parties jouées sur le mois / sur l'année | `[NB_PARTIES]` / `[NB_PARTIES_AN]` | 44 / 48, 49 |
| Variation Elo sur le mois, Elo actuel, meilleur Elo de l'année | `[VARIATION_ELO]`, `[ELO_ACTUEL]`, `[ELO_MAX]` | 44, 45, 49 |
| Exercices tactiques réussis sur le mois / sur l'année | `[NB_EXERCICES]` / `[NB_EXERCICES_AN]` | 44 / 48, 49 |
| Vidéos vues sur l'année | `[NB_VIDEOS_AN]` | 48 |
| Plus belle victoire (victoire contre l'adversaire le mieux classé) | `[MEILLEURE_VICTOIRE]` | 44, 49 |
| Cadence la plus jouée, mois le plus actif | `[CADENCE_PREFEREE]`, `[MOIS_ACTIF]` | 49 |
| Caps : 100ᵉ partie (puis 500, 1000), nouveau record Elo, record du mode challenge | `[CAP_FRANCHI]`, `[DETAIL_CAP]`, `[RECORD]`, `[DATE_CAP]` | 45 (un e-mail par semaine au plus) |
| Panier en cours : formule choisie, prix, date de sortie de la page de paiement, lien pour reprendre | `[SERVICE]`, `[PRIX]`, `[LIEN_PANIER]` | 46 |
| Note de satisfaction (0 à 10) et commentaire : chaque note est un lien `[LIEN_AVIS]?note=N` qui l'enregistre puis ouvre une page de commentaire | `[LIEN_AVIS]` | 47 |
| Date de début d'abonnement (anniversaire) | `[DATE_FIN]`, `[SERVICE]` | 48 |
| Abonnés à la revue papier sans abonnement web, date de début de l'abonnement revue | (segment) | 50 |
| Page à partager « Mon année » | `[LIEN_PARTAGE_ANNEE]` | 49 |

## 4 quater. Boutique : suivi de commande (51 à 57)

Envoyés par la boutique (boutique.echecs.com), à la place de ses e-mails actuels : commande confirmée (51), expédiée (52), livrée (53),
avis 10 jours après la livraison (54), remboursement (55), retour en stock (56), panier oublié (57). 51, 52, 53 et 55 sont des e-mails de commande (toujours envoyés) ;
54, 56 et 57 respectent le refus des e-mails d'information.

- Une ligne `<!-- PRODUIT n -->` par article commandé (vignette, nom, quantité, prix) : la dupliquer ou la supprimer.
- Si la boutique tourne sous PrestaShop (les adresses le laissent penser, à confirmer) : `[PRENOM_CLIENT]` = `{firstname}`, `[NUMERO_COMMANDE]` = `{order_name}`,
  `[TOTAL]` = `{total_paid}`, `[FRAIS_PORT]` = `{total_shipping}`, `[MODE_PAIEMENT]` = `{payment}`, `[ADRESSE_LIVRAISON]` = `{delivery_block_html}`,
  `[LIEN_SUIVI]` = `{followup}`, `[LIEN_COMMANDE]` = `{history_url}`. Les modèles correspondants : `order_conf`, `shipped`, `refund`, `order_canceled`.
- 54 (avis) et 57 (panier) demandent un module d'avis et un module de relance de panier ; 56 un module d'alerte de retour en stock (« Prévenez-moi »).

## 5. Points à trancher avant la mise en service

- **Mot de passe** : choisi par l'utilisateur à la création, il n'est plus dans aucun e-mail. À confirmer pour le 02 : comment le membre d'une offre multicompte choisit-il le sien ?
- **01** : version avec activation. Sans activation, retirer le bouton et la ligne du code ; connexion par un fournisseur externe : ajouter « Vous avez décidé de vous connecter avec votre compte [FOURNISSEUR]. Vous pouvez aussi vous connecter avec votre pseudo et un mot de passe. »
- **Tarif pack de la revue** (+ 60 € / + 50 €, 14, 15, 30) : à confirmer pour les formules au mois.
- **22** : à décider. **44 à 50** : données à créer (section 4 ter). **02** : comment le membre d'une offre multicompte choisit son mot de passe.
- **Tarifs** : écrits en clair dans les e-mails (relevés le 23 novembre 2026, tableau dans `EMAILS-EE.md`). Si un prix change, prévenir pour mettre les e-mails à jour.

## 6. Liste de contrôle avant la mise en service

- [ ] SPF, DKIM, DMARC et désinscription en un clic en place
- [ ] `emails-ee/img/` hébergé, `[URL_IMAGES]` remplacé
- [ ] Les e-mails de priorité 1 intégrés, variables reliées, testés sur Gmail, iPhone (clair et sombre) et Outlook
- [ ] Aucune variable ne part telle quelle (valeur par défaut ou pas d'envoi)
