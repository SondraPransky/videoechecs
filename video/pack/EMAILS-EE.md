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
  boutons bleus `#1F6FC0` à texte blanc, comme sur le site ; pas de mascotte ni de bandeaux illustrés (ils appartiennent à l'Académie).
- **Palette déclinée de la charte du site** : surtitre et titre en blanc sur un bandeau marine sous le logo (la suite du titre en bleu de marque `#58ACFF`),
  filet bleu de 4 px sous le bandeau ; fond et encadrés gris-bleu `#EDF1F8`, texte marine `#1A2140`, texte secondaire `#5D6480`, filets `#DFE4EE` ;
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
- **Prix** : aucun tarif n'est écrit dans les e-mails ; ils restent sur la page des abonnements. Dans les aperçus, les montants restent affichés comme variables.
- **[EMAIL_CONTACT]** : adresse du service abonnement de la revue, à renseigner.

## Catalogue

### Compte

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `01-activation-compte.html` | À la création du compte, si une activation est nécessaire (modèle account_confirmation) | Bienvenue ! Activez votre compte Europe Échecs | Un clic, et vous pouvez commencer à jouer. | Compte (toujours envoyé) |
| `02-compte-multicompte.html` | À la création d'un compte par le gestionnaire d'une offre multicompte (modèle account_confirmation, variante multicompte) | [GESTIONNAIRE] vous a créé un compte Europe Échecs | Vos identifiants et les services de votre offre. | Compte (toujours envoyé) |
| `03-mot-de-passe.html` | Sur demande de réinitialisation (modèle resetpass) | Réinitialisation de votre mot de passe Europe Échecs | Ce lien est valable 1 heure. | Compte (toujours envoyé) |
| `04-suppression-compte.html` | Après la suppression du compte (modèle deletion_request_perform) | Suppression de votre compte Europe Échecs | Votre compte et ses données ont été supprimés. | Compte (toujours envoyé) |

### Découverte

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `05-decouverte-zone-de-jeu.html` | Après la première connexion à la zone de jeu SimpleChess (modèle welcome_directplay) | Bienvenue sur la zone de jeu ! | Cadences, tournois, analyse : ce que vous pouvez y faire. | Information (désinscription possible) |
| `06-offre-de-bienvenue.html` | Offre de bienvenue après l'inscription, valable 48 h (modèle welcome_subscription_48h) | Votre offre de bienvenue : -25 % pendant 48 h | Sur tous nos Packs Web 1 et 2 ans, avec votre code. | Information (désinscription possible) |

### Abonnement

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `07-bienvenue-abonnement.html` | À la création du compte lors d'un abonnement (modèle welcome_subscription) | Bienvenue sur Europe Échecs ! | Vos identifiants de connexion. | Compte (toujours envoyé) |
| `08-abonnement-mis-en-place.html` | À la mise en place d'un abonnement à paiement récurrent (modèle recurpmt_created) | Mise en place de votre abonnement [SERVICE] | Votre abonnement récurrent est en place. | Compte (toujours envoyé) |
| `09-paiement-recu.html` | À la réception d'un paiement de commande (modèle cmdpmtreceived) | Votre commande n° [NUMERO_COMMANDE] | Paiement reçu : votre commande est traitée. | Compte (toujours envoyé) |
| `10-abonnement-echeance.html` | Avant l'échéance d'un abonnement web, 1re et 2e relance (modèles relance1web et relance2web, identiques) | Votre abonnement Europe Échecs arrive à échéance | [PACK] : jusqu’au [DATE_FIN]. | Information (désinscription possible) |
| `11-abonnement-annule.html` | À l'annulation d'un abonnement récurrent (modèle recurpmt_cancelled) | Annulation de votre abonnement [SERVICE] | Votre abonnement ne sera plus facturé. | Compte (toujours envoyé) |

### Nouvelles formules

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `12-pack-jeu-devient-jeu-plus.html` | Une fois, aux abonnés du Pack Jeu en cours (passage gratuit au Pack Jeu+) | Votre Pack Jeu devient gratuitement le Pack Jeu+ | L’entraînement tactique en illimité est inclus dès maintenant. | Compte (toujours envoyé) |
| `13-pack-progresser-en-cours.html` | Une fois, aux abonnés du Pack Progresser en cours | Votre Pack Progresser : ce qui change | Rien ne change avant la fin de votre abonnement. | Compte (toujours envoyé) |
| `14-pack-progresser-expire.html` | À l'échéance d'un abonnement Pack Progresser | Votre Pack Progresser est arrivé à échéance | Deux nouvelles formules pour continuer : Pack Jeu+ et Pack Intégral. | Information (désinscription possible) |
| `15-pack-jeu-expire.html` | À l'échéance d'un abonnement Pack Jeu | Votre Pack Jeu est arrivé à échéance | Deux nouvelles formules pour continuer : Pack Jeu+ et Pack Intégral. | Information (désinscription possible) |

### Revue

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `16-revue-echeance.html` | Avant la fin d'un abonnement à la revue papier, 1re et 2e relance (modèles relance1ee et relance2ee, identiques) | Votre abonnement au magazine Europe Échecs | Votre dernier numéro arrive en [ECHEANCE]. | Information (désinscription possible) |

### Cadeaux

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `17-carte-cadeau.html` | Après l'achat d'un Pack cadeau (modèle gift_code) | Votre commande cadeau | Votre code cadeau et la carte à imprimer. | Compte (toujours envoyé) |

## Variables

La liste complète est générée dans `build/_emails-ee_variables.txt`.
