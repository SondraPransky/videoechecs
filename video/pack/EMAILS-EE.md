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
  boutons jaunes `#FFD30E` à texte marine, comme « Je m'abonne » sur le site ; pas de mascotte ni de bandeaux illustrés (ils appartiennent à l'Académie).
- **Logo décliné par rubrique** (forme officielle, seule la couleur change ; fichiers dans `assets/brand/europe-echecs/`) : blanc pour Compte et Revue,
  jaune `#FFD30E` pour Découverte, Nouvelles formules et Cadeaux, bleu officiel `#93B9E2` pour Abonnement. Trois images à héberger : `logo.png`, `logo-blanc.png`, `logo-jaune.png`.
- **Palette déclinée de la charte du site, avec les couleurs relevées sur la page des abonnements : jaune `#FFD30E`, bleu `#65AFFF`, marine `#02263D`** : surtitre et titre en blanc sur un bandeau marine sous le logo (surtitre et suite du titre en jaune),
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
| 10 Échéance de l'abonnement web, 1re relance | `relance1web` | 27, 29 |
| 29 Échéance de l'abonnement web, 2e relance | `relance2web`, réécrit : nouvel angle (formule 2 ans, formule au mois) | 27, 29 |
| 11 Abonnement annulé | `recurpmt_cancelled` | 30 |
| 12 Le Pack Jeu devient le Pack Jeu+ | texte fourni (nouvelles formules) | — |
| 13 Pack Progresser en cours | texte fourni (nouvelles formules) | — |
| 14 Fin du Pack Progresser | texte fourni (nouvelles formules) | — |
| 15 Fin du Pack Jeu | texte fourni (nouvelles formules) | — |
| 16 Échéance de la revue papier, 1re relance | `relance1ee` | — |
| 30 Échéance de la revue papier, 2e relance | `relance2ee`, réécrit : nouvel angle (tarif pack avec un Pack) | — |
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
- **Chaque relance apporte un angle nouveau** (méthode des relances de prospection) : jamais le même texte renvoyé. 10 puis 29 : renouveler, puis économiser avec 2 ans ou passer au mois ; 16 puis 30 : se réabonner, puis le tarif pack ; 25, 26, 27 : une partie, les nouveautés, puis « on continue ? » (dernier message, respecté : sans clic, plus d'e-mails d'information). Pour le 18, la relance à J+3 devrait aussi changer d'angle (par exemple rappeler ce que l'accès comprend).
- **Ouverture directe** : la raison de l'e-mail dès la première phrase (pas de « Bonne nouvelle : », « Rassurez-vous : », « Nous sommes ravis… »).
- **Pas de formule d'aide en fin d'e-mail** (« N'hésitez pas à nous contacter… ») : le lien « Aide » est dans le pied de page ; une demande précise si besoin (11 : « Pourquoi partez-vous ? »).
- **Boutons** : action + résultat, à la première personne (« Profiter de −25 % », « Me réabonner », « Choisir ma formule »).
- Longueur : 50 à 125 mots pour les e-mails transactionnels, jusqu'à 250 pour la découverte de la zone de jeu (05).

## Tarifs utilisés dans les e-mails

Relevés sur la page des abonnements du site (capture fournie le 23 novembre 2026). À mettre à jour ici et dans `scripts/emails-contenu-ee.py` si un prix change.

| Formule | 1 mois (renouvelé automatiquement, sans engagement) | 1 an (paiement unique, renouvellement manuel) | 2 ans (idem) | Avec la revue (tarif pack) |
|---|---|---|---|---|
| Pack Jeu+ · « Le plaisir de jouer et progresser » | 4,90 € | 39,90 € | 59,90 € | + 60 € |
| Pack Intégral · « Le choix des passionnés » | 11,90 € | 99,90 € | 149,90 € | + 50 € |
| Revue seule | | 79,95 € | | |

Calculs repris dans les e-mails : passer au Pack Intégral coûte 7 € de plus par mois (22) ; passer du mois à l'année fait économiser
18,90 € avec le Pack Jeu+ (12 × 4,90 = 58,80 €) et 42,90 € avec le Pack Intégral (12 × 11,90 = 142,80 €) (23 : `[PRIX_MENSUEL]`, `[PRIX_ANNUEL]`, `[PRIX_2ANS]`, `[ECONOMIE]` selon la formule).
Conséquences : seules les formules au mois sont prélevées automatiquement (18, 19, 20) ; les relances d'échéance (10) concernent les formules 1 an et 2 ans.
À confirmer : le tarif pack de la revue vaut-il aussi pour les formules au mois ?

## Propositions : les e-mails qui manquaient (18 à 28, à valider)

Rédigées d'après la liste de contrôle du cycle de vie. **Rien n'y est inventé** : les prix, délais, offres et nouveautés restent des variables
à remplir avant l'envoi. Dans les aperçus, ces variables restent visibles entre crochets.

| E-mail | Quand | À fournir avant l'envoi |
|---|---|---|
| 18 Paiement refusé | Échec d'un prélèvement mensuel, relance à J+3 | `[DATE_SUSPENSION]` : jusqu'à quand l'accès est garanti ; lien de mise à jour de la carte |
| 19 Carte bientôt expirée | 30 jours avant l'expiration de la carte | Rien de plus (données de paiement) |
| 20 Reçu de renouvellement | À chaque prélèvement d'une formule au mois | Le reçu ou la facture dans « Mon compte » |
| 21 Reconquête | 30 jours après une fin d'abonnement ou une annulation | Trois nouveautés du mois ; `[OFFRE_RETOUR]` ou retrait du bloc |
| 22 Pack Jeu+ → Pack Intégral | Abonnés Pack Jeu+, après `[NB_SEMAINES]` semaines | Le délai (prix intégrés) |
| 23 Mensuel → annuel | Au 3ᵉ prélèvement mensuel | Rien : valeurs par formule dans le tableau des tarifs |
| 24 Rappel de l'offre de bienvenue | 24 h après le 06, sans achat | Confirmer que les Packs Web 1 et 2 ans existent encore |
| 25 Gratuit inactif 7 jours | 7 jours sans connexion | Rien de plus |
| 26 Gratuit inactif 21 jours | 21 jours sans connexion | Trois nouveautés |
| 27 Gratuit inactif 45 jours | 45 jours sans connexion, dernière relance | Lien « Je reste » (`[LIEN_RESTER_ABONNE]`) ; sans clic, arrêt des e-mails d'information |
| 28 Les vidéos de la semaine | Chaque semaine | Titre, série, auteur, jour et miniature de chaque vidéo (exemples des aperçus : vraies séries du catalogue) |

Règles d'envoi proposées : 25, 26 et 27 une seule fois par période d'inactivité ; 22 et 23 une seule fois par abonné ; 21 une seule fois par départ ;
pas de 24 si le code a servi ; 28 remplace les relances 25 et 26 pour un compte qui l'ouvre.

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
| `10-abonnement-echeance.html` | Avant l'échéance d'un abonnement web de 1 ou 2 ans (paiement unique, renouvellement manuel), 1re relance (modèle relance1web ; la 2e est l'e-mail 29) | Votre abonnement Europe Échecs arrive à échéance | [PACK] jusqu’au [DATE_FIN] : renouvelez-le pour garder vos services sans interruption. | Information (désinscription possible) |
| `11-abonnement-annule.html` | À l'annulation d'un abonnement récurrent (modèle recurpmt_cancelled) | Annulation de votre abonnement [SERVICE] | Plus aucune facturation à partir d’aujourd’hui. Vous pouvez revenir quand vous voulez. | Compte (toujours envoyé) |
| `29-abonnement-echeance-relance-2.html` | 2e relance avant l'échéance d'un abonnement de 1 ou 2 ans, si l'abonnement n'est pas renouvelé (modèle relance2web, réécrit) | Votre abonnement s’arrête le [DATE_FIN] | Prolongez pour 2 ans et économisez jusqu’à 49,90 €, ou passez au mois, sans engagement. | Information (désinscription possible) |

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
| `16-revue-echeance.html` | Avant la fin d'un abonnement à la revue papier, 1re relance (modèle relance1ee ; la 2e est l'e-mail 30) | Votre abonnement à la revue Europe Échecs se termine | Votre dernier numéro arrive en [ECHEANCE]. Réabonnez-vous pour ne manquer aucun numéro. | Information (désinscription possible) |
| `30-revue-echeance-relance-2.html` | 2e relance avant la fin d'un abonnement à la revue papier, si rien n'est renouvelé (modèle relance2ee, réécrit) | Votre revue Europe Échecs pour 50 € de plus | Ajoutée à un Pack Intégral, la revue papier coûte 50 € au lieu de 79,95 €, avec la revue en ligne en prime. | Information (désinscription possible) |

### Cadeaux

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `17-carte-cadeau.html` | Après l'achat d'un Pack cadeau (modèle gift_code) | Votre carte cadeau Europe Échecs est prête | Le code à offrir, et la carte au format PDF à imprimer ou à envoyer. | Compte (toujours envoyé) |

### Propositions · paiement mensuel

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `18-paiement-refuse.html` | Échec d'un prélèvement mensuel, relance à J+3 si rien n'a changé (même modèle) · proposition, à valider | Le paiement de votre [SERVICE] n’a pas abouti | Mettez à jour votre carte avant le [DATE_SUSPENSION] pour garder votre accès sans interruption. | Compte (toujours envoyé) |
| `19-carte-bientot-expiree.html` | 30 jours avant l'expiration de la carte enregistrée (abonnements au mois) · proposition, à valider | Votre carte expire bientôt : pensez à la mettre à jour | La carte •••• [CARTE_4_CHIFFRES] expire fin [MOIS_EXPIRATION]. Une minute suffit pour la remplacer. | Compte (toujours envoyé) |
| `20-recu-renouvellement.html` | À chaque prélèvement d'une formule au mois (seule formule renouvelée automatiquement ; 1 an et 2 ans se renouvellent à la main) · proposition, à valider | Votre reçu Europe Échecs : [SERVICE], [MOIS] | Paiement de [MONTANT] reçu. Prochain prélèvement le [DATE_PROCHAIN_PAIEMENT]. | Compte (toujours envoyé) |

### Propositions · reconquête et montée en gamme

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `21-reconquete-j30.html` | 30 jours après une fin d'abonnement ou une annulation, une seule fois · proposition, à valider | Depuis votre départ, sur Europe Échecs | [NOUVEAUTE_1], et d’autres nouveautés. Votre compte vous attend, à l’année ou au mois. | Information (désinscription possible) |
| `22-jeu-plus-vers-integral.html` | Abonnés Pack Jeu+ actifs, après [NB_SEMAINES] semaines d'abonnement (délai à fixer), une seule fois · proposition, à valider | Le Pack Intégral : vidéos, leçons et revue en plus | Pour 7 € de plus par mois : vidéos à la demande, leçons, revue en ligne et plus de 4 nouvelles vidéos par semaine. | Information (désinscription possible) |
| `23-mensuel-vers-annuel.html` | Au 3ᵉ prélèvement d'un abonnement au mois, une seule fois · proposition, à valider | Passez à l’année : [ECONOMIE] d’économie sur votre [SERVICE] | Un seul paiement par an au lieu de douze, et le même accès à tout votre abonnement. | Information (désinscription possible) |

### Propositions · comptes gratuits

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `24-offre-bienvenue-rappel.html` | 24 h après l'e-mail 06, si aucun achat avec le code (fin de l'offre dans 24 h) · proposition, à valider | Plus que 24 heures pour votre −25 % | Votre code de bienvenue s’arrête demain, sur tous nos Packs Web 1 et 2 ans. | Information (désinscription possible) |
| `25-gratuit-inactif-7j.html` | Comptes gratuits, 7 jours sans connexion, une seule fois par période d'inactivité · proposition, à valider | [PSEUDO], une partie sur Europe Échecs ? | Choisissez votre cadence et la force de votre adversaire : la partie commence en un clic. | Information (désinscription possible) |
| `26-gratuit-inactif-21j.html` | Comptes gratuits, 21 jours sans connexion, une seule fois · proposition, à valider | Ce qui s’est passé sur Europe Échecs ces 3 semaines | [NOUVEAUTE_1], et ce qui vous attend sur la zone de jeu. | Information (désinscription possible) |
| `27-gratuit-inactif-45j.html` | Comptes gratuits, 45 jours sans connexion, dernière relance (ensuite, plus d'e-mails d'information) · proposition, à valider | On continue à vous écrire, [PSEUDO] ? | Dites-nous si nos e-mails vous intéressent encore. Sinon, nous arrêtons de vous écrire. | Information (désinscription possible) |
| `28-videos-de-la-semaine.html` | Chaque semaine, à tous les comptes qui l'acceptent (gratuits et abonnés) · proposition, à valider | Les vidéos de la semaine sur Europe Échecs | [SERIE_1], [SERIE_2], [SERIE_3] : les nouveautés de la semaine. | Information (désinscription possible) |

## Variables

La liste complète est générée dans `build/_emails-ee_variables.txt`.
