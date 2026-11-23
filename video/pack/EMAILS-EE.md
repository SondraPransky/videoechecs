# E-mails du site europe-echecs.com — Europe Échecs

17 e-mails pour les membres de https://www.europe-echecs.com/ : **un fichier HTML par e-mail** dans `emails-ee/`, les images à héberger
dans `emails-ee/img/`. Même moteur et même mise en page que les e-mails de l'Académie echecs.com et de la CCAS
(`scripts/emails.py ee`, contenu dans `scripts/emails-contenu-ee.py`).

**Sources :**
- les modèles actuels du site, relevés le 22 novembre 2026 (`MAILS-EE-COMMUNS-ACADEMIE-2026-11-22.md` : les 13 modèles qui recoupent les e-mails de l'Académie, relances de la revue comprises) ;
- les 4 textes des nouvelles formules (passage au Pack Jeu+, Pack Progresser en cours, fin du Pack Progresser, fin du Pack Jeu).

Les textes sont réécrits dans le style des deux autres séries (titre en deux temps, boutons, encadrés, typographie française), **sans rien ajouter** :
aucun prix, délai, service ou chiffre qui ne figure pas dans les sources. Les fautes des modèles d'origine sont corrigées.

**Ce qui change par rapport à l'Académie echecs.com :**
- **Vouvoiement**, comme sur le site europe-echecs.com et dans ses modèles.
- **Marque** : logo officiel Europe Échecs (bleu `#93B9E2`, tiré de la planche `assets/brand/logos-reference.png`) sur l'en-tête marine `#191F38` du site ;
  boutons jaunes `#FAE361` à texte marine ; pas de mascotte ni de bandeaux illustrés (ils appartiennent à l'Académie).
- **Logo décliné par rubrique** (forme officielle, seule la couleur change ; fichiers dans `assets/brand/europe-echecs/`) : blanc pour Compte et Revue,
  jaune `#FAE361` pour Découverte, Nouvelles formules et Cadeaux, bleu officiel `#93B9E2` pour Abonnement. Trois images à héberger : `logo.png`, `logo-blanc.png`, `logo-jaune.png`.
- **Palette déclinée de la charte du site, avec le jaune Europe Échecs `#FAE361`** : surtitre et titre en blanc sur un bandeau marine sous le logo (surtitre et suite du titre en jaune),
  filet jaune de 4 px sous le bandeau, boutons et pastille du Pack Intégral en jaune, filets d'encadré jaunes ; le bleu reste pour le logo, les liens et le Pack Jeu+ ; fond et encadrés gris-bleu `#EDF1F8`, texte marine `#1A2140`, texte secondaire `#5D6480`, filets `#DFE4EE` ;
  Pack Jeu+ sur fond bleu clair `#E6F1FF`, Pack Intégral mis en avant sur fond marine avec sa pastille « Le choix des passionnés ».
  Les teintes crème de l'Académie sont remplacées partout (`REMAP` dans `scripts/emails-contenu-ee.py`), mode sombre compris.
- Expéditeur « Europe Échecs » ; signature « L'équipe d'Europe Échecs » ou « Le service abonnement » (relances), comme dans les modèles.
- Pied de page : Jouer · Vidéos · La revue · Livres (boutique.echecs.com) · Aide. Pas de liens vers les réseaux : ils ne figurent pas dans les modèles.

## Correspondance avec les modèles du site

| E-mail | Modèle EE d'origine | Équivalent Académie |
|---|---|---|
| 01 Activation du compte | `account_confirmation` | 01 + 02 |
| 02 Compte multicompte | `account_confirmation` (variante multicompte) | — |
| 03 Mot de passe | `resetpass` | 03 |
| 04 Suppression du compte | `deletion_request_perform` | 40 |
| 05 Découverte de la zone de jeu | `welcome_directplay` | 10, 11, 13 (partiel) |
| 06 Offre de bienvenue (-25 %, 48 h) | `welcome_subscription_48h` | 05, 06 (partiel) |
| 07 Bienvenue après abonnement | `welcome_subscription` | 07 (partiel) |
| 08 Abonnement mis en place | `recurpmt_created` | 07 |
| 09 Paiement reçu | `cmdpmtreceived` | 09 |
| 10 Échéance de l'abonnement web | `relance1web`, `relance2web` (identiques) | 27, 29 |
| 11 Abonnement annulé | `recurpmt_cancelled` | 30 |
| 12 Le Pack Jeu devient le Pack Jeu+ | texte fourni (nouvelles formules) | — |
| 13 Pack Progresser en cours | texte fourni (nouvelles formules) | — |
| 14 Fin du Pack Progresser | texte fourni (nouvelles formules) | — |
| 15 Fin du Pack Jeu | texte fourni (nouvelles formules) | — |
| 16 Échéance de la revue papier | `relance1ee`, `relance2ee` (identiques) | — |
| 17 Carte cadeau | `gift_code` | 52 (partiel) |

## Décisions et points à suivre

- **Mot de passe en clair (02, 07)** : les modèles actuels envoient le mot de passe dans l'e-mail ; il est conservé pour rester fidèle, mais il vaut mieux
  le remplacer par un lien « Choisir mon mot de passe » (comme le 03).
- **Objets** : les modèles d'origine utilisent « Bienvenue sur [nom du site] ! » pour trois e-mails différents ; 01 et 02 ont désormais leur propre objet.
- **01** : le modèle d'origine a plusieurs variantes (connexion par un fournisseur externe, mot de passe fourni, code d'activation) ; l'e-mail montre la
  version avec activation. Sans activation, retirer le bouton et la ligne du code ; avec un fournisseur externe, ajouter : « Vous avez décidé de vous
  connecter avec votre compte [FOURNISSEUR]. Vous pouvez aussi vous connecter avec votre pseudo et un mot de passe. »
- **05** : le modèle d'origine annonce « 1 e-mail par jour pendant x jours » et contient des commentaires techniques non terminés ; la phrase est retirée
  tant que la série n'est pas définie.
- **06** : le code est à saisir dans le panier, offre valable 48 heures après réception, -25 % sur les Packs Web 1 et 2 ans (selon le modèle). À vérifier :
  ces Packs existent-ils encore avec les nouvelles formules (Pack Jeu+, Pack Intégral) ?
- **10 et 16** : les délais des deux relances ne sont pas indiqués dans les modèles ; à fixer.
- **Paiement mensuel (10, 11)** : la relance d'échéance et l'annulation rappellent que le paiement au mois est possible (nouveauté annoncée avec le Pack Jeu+ et le Pack Intégral). À retirer si la relance concerne une formule sans paiement mensuel.
- **Prix** : aucun tarif n'est écrit dans les e-mails ; ils restent sur la page des abonnements. Dans les aperçus, les montants restent affichés comme variables.
- **[EMAIL_CONTACT]** : adresse du service abonnement de la revue, à renseigner.

## Règles de rédaction de la série

- **Un e-mail, une tâche** : un seul bouton principal ; pas de liens inutiles avant l'action attendue (01 : rien à cliquer avant l'activation).
- **Objet** de 35 à 55 caractères, clair avant d'être malin ; **pré-en-tête** de 60 à 95 caractères qui complète l'objet sans le répéter.
- **Ouverture directe** : la raison de l'e-mail dès la première phrase (pas de « Bonne nouvelle : », « Rassurez-vous : », « Nous sommes ravis… »).
- **Pas de formule d'aide en fin d'e-mail** (« N'hésitez pas à nous contacter… ») : le lien « Aide » est dans le pied de page ; une demande précise si besoin (11 : « Pourquoi partez-vous ? »).
- **Boutons** : action + résultat, à la première personne (« Profiter de −25 % », « Me réabonner », « Choisir ma formule »).
- Longueur : 50 à 125 mots pour les e-mails transactionnels, jusqu'à 250 pour la découverte de la zone de jeu (05).

## Audit du cycle de vie : e-mails qui manquent

Comparée à la liste de contrôle du cycle de vie (et aux 52 e-mails de l'Académie), la série Europe Échecs n'a pas encore :

| Manque | Quand | Pourquoi | Ce qu'il faut pour l'écrire |
|---|---|---|---|
| Paiement refusé (relance J+3) | Échec d'un prélèvement mensuel | Le paiement mensuel arrive : sans relance, les abonnés partent sans le vouloir | Le délai de suspension de l'accès |
| Carte bientôt expirée | 30 jours avant | Même raison, en prévention | Rien de plus |
| Reçu de renouvellement | À chaque prélèvement | Obligatoire en pratique pour le mensuel | Le format du reçu |
| Reconquête | 30 jours après une fin d'abonnement ou une annulation | Seul e-mail qui ramène un ancien abonné | Une offre de retour, si elle existe |
| Pack Jeu+ → Pack Intégral | Après quelques semaines d'usage du Pack Jeu+ | Montée en gamme vers la formule mise en avant | Les prix des deux formules |
| Mensuel → annuel | Au 3ᵉ mois de paiement mensuel | Fidélise et réduit les échecs de paiement | L'écart de prix entre les deux |
| Rappel de l'offre de bienvenue | 24 h avant la fin des 48 h (06) | Le rappel « dernières heures » convertit souvent autant que l'e-mail d'origine | Confirmer que les Packs Web 1 et 2 ans existent encore |
| Comptes gratuits inactifs | 7, 21 et 45 jours sans connexion | Rien ne relance un compte gratuit après le 05 et le 06 | Ce qui est nouveau sur le site (vidéos de la semaine, tournois) |
| Les vidéos de la semaine | Chaque semaine | Rendez-vous régulier, à l'image de l'e-mail 43 de l'Académie | Le programme réel des séries vidéo |

## Mesures

- **Taux de clic** (objectif 2 à 5 %) et **conversion** propre à chaque e-mail : activation (01), achat avec le code (06), renouvellement (10, 16), choix d'une formule (13 à 15), réabonnement (11).
- **Désinscriptions** sous 0,5 % par envoi.
- Le taux d'ouverture n'est qu'une tendance (faussé par Apple Mail depuis 2021) : à comparer d'un envoi à l'autre, jamais à une moyenne du marché.
- Premiers tests A/B, une variable à la fois : l'objet du 06 (offre en chiffre ou en avantage), le bouton des 14 et 15.

## Catalogue

### Compte

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `01-activation-compte.html` | À la création du compte, si une activation est nécessaire (modèle account_confirmation) | Bienvenue ! Activez votre compte Europe Échecs | Un clic pour activer votre compte : zone de jeu, vidéos, revue et livres vous attendent. | Compte (toujours envoyé) |
| `02-compte-multicompte.html` | À la création d'un compte par le gestionnaire d'une offre multicompte (modèle account_confirmation, variante multicompte) | Votre compte Europe Échecs est prêt | Créé par [GESTIONNAIRE] dans une offre multicompte : vos identifiants et vos services. | Compte (toujours envoyé) |
| `03-mot-de-passe.html` | Sur demande de réinitialisation (modèle resetpass) | Réinitialisez votre mot de passe Europe Échecs | Ce lien est valable 1 heure. Vous n’avez rien demandé ? Ignorez simplement cet e-mail. | Compte (toujours envoyé) |
| `04-suppression-compte.html` | Après la suppression du compte (modèle deletion_request_perform) | Suppression de votre compte Europe Échecs | Votre compte [PSEUDO] et ses données ont été supprimés, comme vous l’avez demandé. | Compte (toujours envoyé) |

### Découverte

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `05-decouverte-zone-de-jeu.html` | Après la première connexion à la zone de jeu SimpleChess (modèle welcome_directplay) | Zone de jeu : 7 fonctions à connaître dès maintenant | Cadences, tournois, analyse de vos parties, joueurs à suivre : le tour du propriétaire. | Information (désinscription possible) |
| `06-offre-de-bienvenue.html` | Offre de bienvenue après l'inscription, valable 48 h (modèle welcome_subscription_48h) | Votre offre de bienvenue : −25 % pendant 48 h | Sur tous nos Packs Web 1 et 2 ans, avec votre code personnel. L’offre s’arrête dans 48 heures. | Information (désinscription possible) |

### Abonnement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `07-bienvenue-abonnement.html` | À la création du compte lors d'un abonnement (modèle welcome_subscription) | Bienvenue ! Vos identifiants Europe Échecs | Merci pour votre abonnement. Voici de quoi vous connecter tout de suite. | Compte (toujours envoyé) |
| `08-abonnement-mis-en-place.html` | À la mise en place d'un abonnement à paiement récurrent (modèle recurpmt_created) | Mise en place de votre abonnement [SERVICE] | Votre abonnement récurrent est en place. Vous le gérez à tout moment depuis « Mon compte ». | Compte (toujours envoyé) |
| `09-paiement-recu.html` | À la réception d'un paiement de commande (modèle cmdpmtreceived) | Votre commande n° [NUMERO_COMMANDE] | Paiement reçu, commande traitée : le détail de votre commande. | Compte (toujours envoyé) |
| `10-abonnement-echeance.html` | Avant l'échéance d'un abonnement web, 1re et 2e relance (modèles relance1web et relance2web, identiques) | Votre abonnement Europe Échecs arrive à échéance | [PACK] jusqu’au [DATE_FIN] : renouvelez-le pour garder vos services sans interruption. | Information (désinscription possible) |
| `11-abonnement-annule.html` | À l'annulation d'un abonnement récurrent (modèle recurpmt_cancelled) | Annulation de votre abonnement [SERVICE] | Plus aucune facturation à partir d’aujourd’hui. Vous pouvez revenir quand vous voulez. | Compte (toujours envoyé) |

### Nouvelles formules

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `12-pack-jeu-devient-jeu-plus.html` | Une fois, aux abonnés du Pack Jeu en cours (passage gratuit au Pack Jeu+) | Votre Pack Jeu devient gratuitement le Pack Jeu+ | Sans rien payer de plus : l’entraînement tactique en illimité, avec des milliers d’exercices. | Compte (toujours envoyé) |
| `13-pack-progresser-en-cours.html` | Une fois, aux abonnés du Pack Progresser en cours | Votre Pack Progresser : ce qui change | Vous gardez les mêmes services jusqu’à la fin. Ensuite, deux nouvelles formules au choix. | Compte (toujours envoyé) |
| `14-pack-progresser-expire.html` | À l'échéance d'un abonnement Pack Progresser | Votre Pack Progresser est arrivé à échéance | Pack Jeu+ ou Pack Intégral, à l’année ou au mois : à vous de choisir. | Information (désinscription possible) |
| `15-pack-jeu-expire.html` | À l'échéance d'un abonnement Pack Jeu | Votre Pack Jeu est arrivé à échéance | Pack Jeu+ ou Pack Intégral, à l’année ou au mois : à vous de choisir. | Information (désinscription possible) |

### Revue

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `16-revue-echeance.html` | Avant la fin d'un abonnement à la revue papier, 1re et 2e relance (modèles relance1ee et relance2ee, identiques) | Votre abonnement à la revue Europe Échecs se termine | Votre dernier numéro arrive en [ECHEANCE]. Réabonnez-vous pour ne manquer aucun numéro. | Information (désinscription possible) |

### Cadeaux

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `17-carte-cadeau.html` | Après l'achat d'un Pack cadeau (modèle gift_code) | Votre carte cadeau Europe Échecs est prête | Le code à offrir, et la carte au format PDF à imprimer ou à envoyer. | Compte (toujours envoyé) |

## Variables

La liste complète est générée dans `build/_emails-ee_variables.txt`.
