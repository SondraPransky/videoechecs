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
| 65 Bienvenue (compte créé par le joueur) | `account_welcome` | — |
| 66 Suppression demandée · 67 annulée | `deletion_request`, `deletion_request_cancel` | — |
| 68 Compte inactif depuis 6 mois | `suppr_compte_avert1` | — |
| 69 Liste de vos comptes | `renvoicomptesreset` | — |
| 70 Connexion externe dissociée | `account_provider_dissociated` | — |
| 71 Préférences de données à confirmer | `consent_update_required` | — |
| 72 Limite appliquée · 73 levée | `account_limitation_applied`, `account_limitation_revoked` | — |
| 74 Multicompte : invitation · 75 réponse · 76 compte détaché | `multiaccount_join_invite`, `multiaccount_join_invite_answer`, `multiaccount_detached` | — |
| 77 Inscription à la newsletter · 78 à reconfirmer | `newsletter_confirm`, `newsletter_consent_update_required_fr` | — |
| 79 à 85 Jeu en différé (coup joué, partie commencée, terminée, invitation, tournoi commencé, terminé, annulé) | `jeudiffcoupjoue`, `jeudiffpartiedebut`, `jeudiffpartietermine`, `jeudifftourninvit`, `jeudifftourndebut`, `jeudifftournfin`, `jeudifftournannul` | — |
| 86 à 90 Tournois (invitation, en ligne, début, nouvelle ronde, rappel) | `tourn_invitation`, `tourn_created`, `tourn_start`, `tourn_startround`, `tourn_match_reminder` | — |
| 91 Horaire proposé · 92 réponse (acceptée, refusée, retirée) | `tourn_proposreceived` · `tourn_proposaccepted`, `tourn_proposdenied`, `tourn_proposdeleted` (3 en 1) | — |
| 93 Partie reprogrammée · 94 ronde décalée | `tourn_match_reprog` · `tourn_round_shifted`, `tourn_roundend_updat` (2 en 1) | — |
| 95 Appariement manuel · 96 tournoi terminé · 97 instructions | `tourn_round_manualpairingrequired`, `tourn_end` (objet corrigé), `tourn_instructions` (raccourci) | — |
| 98 à 100 Événement : en attente, validé, refusé | `event_waiting`, `event_confirm` (sans l'ancienne branche Zoom), `event_reject` | — |
| 101 Cours · 102 masterclass · 103 invitation masterclass | `course_confirmation`, `masterclass_confirm`, `masterclass_invit` | — |
| 104 Fair-play : suite d'un signalement | les 5 `fairplaycase_*_to_reporter` (5 en 1) | — |
| 105 Fair-play : décision sur un adversaire | les 3 `fairplaycase_*_to_third_party_player` (3 en 1) | — |
| 106 Fair-play : avertissement | `fairplaycase_violation_to_suspect` | — |
| 107 Problème traité | `problem_solved`, `problem_solved_user` (identiques, 2 en 1) | — |
| 108 Message d'un joueur · 109 commentaire non publié | `contactjoueursmsg`, `refuscommentaire` | — |
| 110 Battle commence · 111 terminée | `puzzlesbattledebut`, `puzzlesbattlefin` | — |
| 112 Demande enregistrée · 113 réponse · 114 message de l'équipe | `supportdemenreg`, `supportdemchgetat`, `support_mail_direct` et `mail_direct` (2 en 1) | — |
| 115 PrediChess 1er · 116 top 4 et top 20 | `predichess_prize_first` · `predichess_prize_top4`, `predichess_prize_top20` (2 en 1) | — |
| 117 Parrainage : invitation et rappel | `sponsorship_invitation`, `sponsorship_remind_invitation` (identiques, 2 en 1) | — |
| 118 à 122 Parrainage : ami inscrit, validé, abonné, relancez, adresse en erreur | `sponsorship_create_account`, `sponsorship_activate_account` (+ `_level_up`), `sponsorship_activate_subscription` (+ `_level_up`), `sponsorship_remind_sponsor_activation`, `sponsorship_email_error` | — |

Non repris : `ccas_tournament_soon` (série CCAS), `questionnaire_satisfaction_fr` (remplacé par le 47), `cmdsent` (couvert par le 52), `welcome_subscription` envoyait le mot de passe en clair (supprimé dans le 07).

## Décisions et points à suivre

Réponses de l'équipe (23 novembre 2026), confirmées par Raph :

- **Mot de passe** : l'utilisateur le choisit à la création du compte ; il n'apparaît plus dans aucun e-mail (02 et 07 n'affichent que le pseudo).
  À confirmer pour le 02 (compte créé par un gestionnaire) : comment le membre choisit-il son mot de passe ?
- **Paiement refusé (18, 31)** : l'accès est bloqué tout de suite, sans délai de grâce. Le 18 l'annonce, le 31 (J+3) invite à le retrouver.
- **Relances** : packs web à J-15 (10, `relance1web`) et J-3 (29, `relance2web`) ; revue le 25 (16, `relance1ee`) puis le 8 du mois suivant (30, `relance2ee`).
- **Contact de la revue (16, 30)** : le support, par la page d'aide.
- **Éditeur (pied de page)** : IDEAL SAS, 114 quai Louis Blériot, 75016 Paris.
- **Vidéos de la semaine (28)** : lundi La Minute Stratégie, mardi Coup de Légende, mercredi Calcul Gagnant, vendredi La Minute Finale ;
  le dimanche, une ou deux vidéos par mois (les semaines concernées, ajouter une 5e carte identique). Envoi le dimanche après-midi.
- **Pack Jeu+ → Pack Intégral (22)** : pas en place aujourd'hui ; proposition à décider.
- **Reconquête (21)** : pas d'offre de retour pour l'instant ; l'encadré est retiré.
- **Abonnement expiré** : nouvel e-mail 32 à J+1 après la fin d'un abonnement de 1 ou 2 ans (avant la reconquête à J+30).
- **Objets** : les modèles d'origine utilisent « Bienvenue sur [nom du site] ! » pour trois e-mails différents ; 01 et 02 ont désormais leur propre objet.
- **01** : le modèle d'origine a plusieurs variantes (connexion par un fournisseur externe, mot de passe fourni, code d'activation) ; l'e-mail montre la
  version avec activation. Sans activation, retirer le bouton et la ligne du code ; avec un fournisseur externe, ajouter : « Vous avez décidé de vous
  connecter avec votre compte [FOURNISSEUR]. Vous pouvez aussi vous connecter avec votre pseudo et un mot de passe. »
- **05** : le modèle d'origine annonce « 1 e-mail par jour pendant x jours » et contient des commentaires techniques non terminés ; la phrase est retirée
  tant que la série n'est pas définie.
- **06** : le code est à saisir dans le panier, offre valable 48 heures après réception, -25 % sur les Packs Web 1 et 2 ans (selon le modèle). À vérifier :
  ces Packs existent-ils encore avec les nouvelles formules (Pack Jeu+, Pack Intégral) ?
- **Paiement mensuel (10, 11)** : la relance d'échéance et l'annulation rappellent que le paiement au mois est possible (nouveauté annoncée avec le Pack Jeu+ et le Pack Intégral). À retirer si la relance concerne une formule sans paiement mensuel.

## Règles de rédaction de la série

- **Un e-mail, une tâche** : un seul bouton principal ; pas de liens inutiles avant l'action attendue (01 : rien à cliquer avant l'activation).
- **Objet** de 35 à 55 caractères, clair avant d'être malin ; **pré-en-tête** de 60 à 95 caractères qui complète l'objet sans le répéter.
- **Chaque relance apporte un angle nouveau** (méthode des relances de prospection) : jamais le même texte renvoyé. 10 puis 29 : renouveler, puis économiser avec 2 ans ou passer au mois ; 16 puis 30 : se réabonner, puis le tarif pack ; 25, 26, 27 : une partie, les nouveautés, puis « on continue ? » (dernier message, respecté : sans clic, plus d'e-mails d'information). 18 puis 31 : un souci de paiement, puis la date de fin d'accès.
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
| 18 Paiement refusé | Échec d'un prélèvement mensuel : accès suspendu tout de suite (1er avis) | Lien de mise à jour de la carte |
| 31 Paiement refusé, 2e avis | J+3 après le 18, si la carte n'est pas à jour : « Retrouver mon accès », et les autres formules | Rien de plus |
| 19 Carte bientôt expirée | 30 jours avant l'expiration de la carte | Rien de plus (données de paiement) |
| 20 Reçu de renouvellement | À chaque prélèvement d'une formule au mois | Le reçu ou la facture dans « Mon compte » |
| 32 Abonnement expiré | J+1 après la fin d'un abonnement de 1 ou 2 ans non renouvelé | Rien de plus |
| 21 Reconquête | 30 jours après une fin d'abonnement ou une annulation | Trois nouveautés du mois (pas d'offre de retour pour l'instant) |
| 22 Pack Jeu+ → Pack Intégral | Pas en place aujourd'hui : abonnés Pack Jeu+, après un délai à fixer | La décision et le délai |
| 23 Mensuel → annuel | Au 3ᵉ prélèvement mensuel | Rien : valeurs par formule dans le tableau des tarifs |
| 24 Rappel de l'offre de bienvenue | 24 h après le 06, sans achat | Confirmer que les Packs Web 1 et 2 ans existent encore |
| 25 Gratuit inactif 7 jours | 7 jours sans connexion | Rien de plus |
| 26 Gratuit inactif 21 jours | 21 jours sans connexion | Trois nouveautés |
| 27 Gratuit inactif 45 jours | 45 jours sans connexion, dernière relance | Lien « Je reste » (`[LIEN_RESTER_ABONNE]`) ; sans clic, arrêt des e-mails d'information |
| 28 Les vidéos de la semaine | Chaque semaine, après la Minute Finale du vendredi | Titre, auteur et miniature de chaque vidéo (séries et jours fixés : lundi, mardi, mercredi, vendredi) |

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
| `02-compte-multicompte.html` | À la création d'un compte par le gestionnaire d'une offre multicompte (modèle account_confirmation, variante multicompte) | Votre compte Europe Échecs est prêt | Créé par [GESTIONNAIRE] dans une offre multicompte : votre pseudo et vos services. | Compte (toujours envoyé) |
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
| `07-bienvenue-abonnement.html` | À la création du compte lors d'un abonnement (modèle welcome_subscription) | Bienvenue ! Votre compte Europe Échecs est prêt | Merci pour votre abonnement. Connectez-vous avec le pseudo et le mot de passe que vous avez choisis. | Compte (toujours envoyé) |
| `08-abonnement-mis-en-place.html` | À la mise en place d'un abonnement à paiement récurrent (modèle recurpmt_created) | Mise en place de votre abonnement [SERVICE] | Votre abonnement récurrent est en place. Vous le gérez à tout moment depuis « Mon compte ». | Compte (toujours envoyé) |
| `09-paiement-recu.html` | À la réception d'un paiement de commande (modèle cmdpmtreceived) | Votre commande n° [NUMERO_COMMANDE] | Paiement reçu, commande traitée : le détail de votre commande. | Compte (toujours envoyé) |
| `10-abonnement-echeance.html` | Avant l'échéance d'un abonnement web de 1 ou 2 ans (paiement unique, renouvellement manuel), 1re relance à J-15 (modèle relance1web ; la 2e, à J-3, est l'e-mail 29) | Votre abonnement Europe Échecs arrive à échéance | [PACK] jusqu’au [DATE_FIN] : renouvelez-le pour garder vos services sans interruption. | Information (désinscription possible) |
| `11-abonnement-annule.html` | À l'annulation d'un abonnement récurrent (modèle recurpmt_cancelled) | Annulation de votre abonnement [SERVICE] | Plus aucune facturation à partir d’aujourd’hui. Vous pouvez revenir quand vous voulez. | Compte (toujours envoyé) |
| `29-abonnement-echeance-relance-2.html` | 2e relance à J-3 avant l'échéance d'un abonnement de 1 ou 2 ans, si l'abonnement n'est pas renouvelé (modèle relance2web, réécrit) | Votre abonnement s’arrête le [DATE_FIN] | Prolongez pour 2 ans et économisez jusqu’à 49,90 €, ou passez au mois, sans engagement. | Information (désinscription possible) |

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
| `16-revue-echeance.html` | Avant la fin d'un abonnement à la revue papier, 1re relance le 25 du mois (modèle relance1ee ; la 2e, le 8 du mois suivant, est l'e-mail 30) | Votre abonnement à la revue Europe Échecs se termine | Votre dernier numéro arrive en [ECHEANCE]. Réabonnez-vous pour ne manquer aucun numéro. | Information (désinscription possible) |
| `30-revue-echeance-relance-2.html` | 2e relance le 8 du mois qui suit la 1re (16, le 25), avant la fin d'un abonnement à la revue papier, si rien n'est renouvelé (modèle relance2ee, réécrit) | Votre revue Europe Échecs pour 50 € de plus | Ajoutée à un Pack Intégral, la revue papier coûte 50 € au lieu de 79,95 €, avec la revue en ligne en prime. | Information (désinscription possible) |

### Cadeaux

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `17-carte-cadeau.html` | Après l'achat d'un Pack cadeau (modèle gift_code) | Votre carte cadeau Europe Échecs est prête | Le code à offrir, et la carte au format PDF à imprimer ou à envoyer. | Compte (toujours envoyé) |

### Propositions · paiement mensuel

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `18-paiement-refuse.html` | Échec d'un prélèvement mensuel : l'accès est suspendu tout de suite (1er avis ; si rien n'a changé à J+3 : e-mail 31) · proposition, à valider | Votre accès [SERVICE] est suspendu | Le prélèvement de [MONTANT] n’a pas abouti. Mettez à jour votre carte pour retrouver votre accès. | Compte (toujours envoyé) |
| `19-carte-bientot-expiree.html` | 30 jours avant l'expiration de la carte enregistrée (abonnements au mois) · proposition, à valider | Votre carte expire bientôt : pensez à la mettre à jour | La carte •••• [CARTE_4_CHIFFRES] expire fin [MOIS_EXPIRATION]. Une minute suffit pour la remplacer. | Compte (toujours envoyé) |
| `20-recu-renouvellement.html` | À chaque prélèvement d'une formule au mois (seule formule renouvelée automatiquement ; 1 an et 2 ans se renouvellent à la main) · proposition, à valider | Votre reçu Europe Échecs : [SERVICE], [MOIS] | Paiement de [MONTANT] reçu. Prochain prélèvement le [DATE_PROCHAIN_PAIEMENT]. | Compte (toujours envoyé) |
| `31-paiement-refuse-relance.html` | J+3 après l'e-mail 18, si la carte n'a toujours pas été mise à jour (2e et dernier avis) · proposition, à valider | Votre accès [SERVICE] est toujours suspendu | Une minute pour mettre votre carte à jour, ou une autre formule dès 4,90 € par mois, sans engagement. | Compte (toujours envoyé) |

### Propositions · reconquête et montée en gamme

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `21-reconquete-j30.html` | 30 jours après une fin d'abonnement ou une annulation, une seule fois · proposition, à valider | Depuis votre départ, sur Europe Échecs | [NOUVEAUTE_1], et d’autres nouveautés. Votre compte vous attend, à l’année ou au mois. | Information (désinscription possible) |
| `22-jeu-plus-vers-integral.html` | Nouveau (pas en place aujourd'hui) : abonnés Pack Jeu+ actifs, après un délai à fixer, une seule fois · proposition, à valider | Le Pack Intégral : vidéos, leçons et revue en plus | Pour 7 € de plus par mois : vidéos à la demande, leçons, revue en ligne et plus de 4 nouvelles vidéos par semaine. | Information (désinscription possible) |
| `23-mensuel-vers-annuel.html` | Au 3ᵉ prélèvement d'un abonnement au mois, une seule fois · proposition, à valider | Passez à l’année : [ECONOMIE] d’économie sur votre [SERVICE] | Un seul paiement par an au lieu de douze, et le même accès à tout votre abonnement. | Information (désinscription possible) |
| `32-abonnement-expire.html` | J+1 après la fin d'un abonnement de 1 ou 2 ans non renouvelé (après les relances 10 et 29 ; puis 21 à J+30) · proposition, à valider | Votre [PACK] est arrivé à échéance | Votre abonnement s’est terminé le [DATE_FIN]. Reprenez en un clic, au mois dès 4,90 € ou pour 1 ou 2 ans. | Information (désinscription possible) |

### Propositions · comptes gratuits

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `24-offre-bienvenue-rappel.html` | 24 h après l'e-mail 06, si aucun achat avec le code (fin de l'offre dans 24 h) · proposition, à valider | Plus que 24 heures pour votre −25 % | Votre code de bienvenue s’arrête demain, sur tous nos Packs Web 1 et 2 ans. | Information (désinscription possible) |
| `25-gratuit-inactif-7j.html` | Comptes gratuits, 7 jours sans connexion, une seule fois par période d'inactivité · proposition, à valider | [PSEUDO], une partie sur Europe Échecs ? | Choisissez votre cadence et la force de votre adversaire : la partie commence en un clic. | Information (désinscription possible) |
| `26-gratuit-inactif-21j.html` | Comptes gratuits, 21 jours sans connexion, une seule fois · proposition, à valider | Ce qui s’est passé sur Europe Échecs ces 3 semaines | [NOUVEAUTE_1], et ce qui vous attend sur la zone de jeu. | Information (désinscription possible) |
| `27-gratuit-inactif-45j.html` | Comptes gratuits, 45 jours sans connexion, dernière relance (ensuite, plus d'e-mails d'information) · proposition, à valider | On continue à vous écrire, [PSEUDO] ? | Dites-nous si nos e-mails vous intéressent encore. Sinon, nous arrêtons de vous écrire. | Information (désinscription possible) |
| `28-videos-de-la-semaine.html` | Chaque dimanche après-midi (bilan de la semaine : lundi, mardi, mercredi, vendredi, et le dimanche quand il y a une vidéo), à tous les comptes qui l'acceptent · proposition, à valider | Les vidéos de la semaine sur Europe Échecs | Stratégie, légende, calcul et finale : vos quatre rendez-vous de la semaine, à voir quand vous voulez. | Information (désinscription possible) |

### Newsletter

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `33-newsletter.html` | Chaque semaine (aujourd'hui le lundi en fin d'après-midi), à tous les comptes qui acceptent les e-mails d'information. Un article à la une, puis autant d'articles que nécessaire, et au plus un encart boutique | [OBJET_NEWSLETTER] | [PRE_EN_TETE_NEWSLETTER] | Information (désinscription possible) |
| `77-newsletter-inscription.html` | À l'inscription à la newsletter (newsletter_confirm) · modèle actuel du site | Vous êtes inscrit à la newsletter Europe Échecs | Les actualités des échecs à ne pas rater, chaque semaine. | Compte (toujours envoyé) |
| `78-newsletter-confirmer.html` | Pour mettre la liste de diffusion à jour : abonnés à la newsletter à reconfirmer (newsletter_consent_update_required_fr) · modèle actuel du site | Newsletter Europe Échecs : confirmez votre inscription | Un clic pour continuer à la recevoir. Sans réponse de votre part, vous ne la recevrez plus. | Compte (toujours envoyé) |

### Boutique

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `34-promo-boutique.html` | Opération commerciale de la boutique (un produit ou une gamme), à tous les comptes qui acceptent les e-mails d'information | [OBJET_PROMO] | [PRE_EN_TETE_PROMO] | Information (désinscription possible) |

### Propositions · temps forts

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `39-noel-idees-cadeaux.html` | Début décembre, à tous les comptes qui acceptent les e-mails d'information · proposition, à valider · Mailjet | Vos idées cadeaux échecs pour Noël | Pour un passionné d’histoire, un joueur de club ou un fan : livres, revue, abonnements, vêtements et cartes cadeaux. | Information (désinscription possible) |
| `40-noel-derniere-livraison.html` | Le dernier jour de commande pour une livraison avant Noël (date à fixer avec la boutique), sauf à ceux qui ont commandé dans la semaine · proposition, à valider · Mailjet | Commandez aujourd’hui pour être livré avant Noël | Dernier jour pour recevoir livres et échiquiers avant le 25 décembre. Ensuite, il reste la carte cadeau. | Information (désinscription possible) |
| `41-noel-carte-cadeau.html` | Du 22 au 24 décembre, une seule fois, sauf à ceux qui ont acheté une carte cadeau · proposition, à valider · Mailjet | Un cadeau d’échecs, même le 24 décembre | La carte cadeau Europe Échecs arrive en PDF : prête à imprimer ou à envoyer, sans attendre la livraison. | Information (désinscription possible) |

### Propositions · rendez-vous réguliers

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `42-revue-nouveau-numero.html` | À la sortie de chaque numéro de la revue, aux abonnés qui ont la revue en ligne (Pack Intégral) ou papier · proposition, à valider · Mailjet | Le numéro [NUMERO_REVUE] de la revue est en ligne | [ACCROCHE_NUMERO] | Information (désinscription possible) |
| `43-probleme-de-la-semaine.html` | Chaque semaine (jour à fixer, pas le même que la newsletter), aux comptes gratuits qui acceptent les e-mails d'information. Varier les niveaux d'une semaine à l'autre · proposition, à valider · Mailjet | Le problème de la semaine : [CONSIGNE_COURTE] | Niveau [NIVEAU_PROBLEME]. Trouvez le coup, puis vérifiez la solution sur Europe Échecs. | Information (désinscription possible) |

### Propositions · vos chiffres

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `44-votre-mois.html` | Le 1er de chaque mois, aux comptes qui ont joué au moins une partie dans le mois, s'ils acceptent les e-mails d'information · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Votre mois de [MOIS_BILAN] sur Europe Échecs | [NB_PARTIES] parties, [VARIATION_ELO] points Elo et [NB_EXERCICES] exercices réussis. | Information (désinscription possible) |
| `45-cap-franchi.html` | Quand un joueur franchit un cap : 100ᵉ partie, nouveau record Elo, record battu en mode challenge (un seul e-mail par semaine au plus) · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Bravo [PSEUDO] : [CAP_FRANCHI] | Félicitations, [DETAIL_CAP]. On continue sur cette lancée ? | Information (désinscription possible) |
| `49-votre-annee.html` | Début janvier, aux comptes qui ont joué dans l'année, s'ils acceptent les e-mails d'information · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Votre année [ANNEE] sur Europe Échecs | [NB_PARTIES_AN] parties, votre meilleur Elo à [ELO_MAX] et votre plus belle victoire. | Information (désinscription possible) |

### Propositions · satisfaction et fidélité

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `46-panier-abandonne.html` | 1 heure après avoir quitté la page de paiement d'un abonnement sans payer, une seule fois par semaine · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Votre [SERVICE] vous attend | Il ne reste qu’une étape pour retrouver vos vidéos, leçons et entraînements. | Information (désinscription possible) |
| `47-satisfaction-30j.html` | 30 jours après le début d'un abonnement payant, une seule fois · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Un mois sur Europe Échecs : votre avis ? | Une question, un clic : vous recommanderiez Europe Échecs à un ami ? | Information (désinscription possible) |
| `48-anniversaire-abonnement.html` | Au 1er anniversaire d'un abonnement (puis chaque année), 30 jours avant l'échéance pour les formules de 1 an · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Un an avec vous, [PSEUDO] : merci ! | [NB_PARTIES_AN] parties, [NB_VIDEOS_AN] vidéos et [NB_EXERCICES_AN] exercices en un an. | Information (désinscription possible) |
| `50-revue-papier-vers-web.html` | Abonnés à la revue papier sans abonnement web, 2 mois après le début de l'abonnement, une seule fois · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md) | Votre revue, aussi en ligne et en vidéo | Les parties de la revue à rejouer coup par coup, plus de 4 vidéos par semaine et la zone de jeu premium. | Information (désinscription possible) |

### Boutique · suivi de commande

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `51-commande-confirmee.html` | Dès la commande payée sur la boutique · proposition, à valider · envoyé par la boutique | Commande n° [NUMERO_COMMANDE] confirmée, merci ! | Nous préparons votre colis. Livraison prévue autour du [DATE_LIVRAISON_ESTIMEE]. | Compte (toujours envoyé) |
| `52-commande-expediee.html` | Quand le colis est remis au transporteur, avec le numéro de suivi · proposition, à valider · envoyé par la boutique | Votre commande n° [NUMERO_COMMANDE] est en route | Colis remis à [TRANSPORTEUR] : suivez-le avec le numéro [NUMERO_SUIVI]. | Compte (toujours envoyé) |
| `53-commande-livree.html` | Quand le transporteur signale la livraison (ou 3 jours après l'expédition si le transporteur ne le signale pas) · proposition, à valider · envoyé par la boutique | Votre commande n° [NUMERO_COMMANDE] est arrivée | Tout est en ordre ? Un souci avec votre colis : nous sommes là pour vous aider. | Compte (toujours envoyé) |
| `54-avis-produit.html` | 10 jours après la livraison, une seule fois par commande, s'il accepte les e-mails d'information · proposition, à valider · envoyé par la boutique | [NOM_ARTICLE_1] : qu’en pensez-vous ? | Votre avis aide les autres joueurs à choisir. Une note suffit, un commentaire si vous voulez. | Information (désinscription possible) |
| `55-remboursement.html` | Quand un remboursement (total ou partiel) ou une annulation est validé · proposition, à valider · envoyé par la boutique | Remboursement de votre commande n° [NUMERO_COMMANDE] | [MONTANT_REMBOURSE] remboursés sur votre [MODE_PAIEMENT]. Ils apparaîtront sous quelques jours. | Compte (toujours envoyé) |
| `56-retour-en-stock.html` | Quand un produit épuisé revient en stock, à ceux qui ont demandé à être prévenus (une seule fois) · proposition, à valider · envoyé par la boutique | [NOM_ARTICLE_1] est de retour en stock | Vous avez demandé à être prévenu : il est de nouveau disponible sur la boutique. | Information (désinscription possible) |
| `57-panier-boutique.html` | 2 heures après un panier laissé sur la boutique par un client connecté, une seule fois par panier · proposition, à valider · envoyé par la boutique | Vous avez oublié quelque chose | [NOM_ARTICLE_1] vous attend dans votre panier. | Information (désinscription possible) |

### Propositions · bien démarrer

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `58-premiers-pas-tactique.html` | J+1 après la souscription d'un Pack Jeu+ ou d'un Pack Intégral, sauf s'il a déjà résolu un exercice · proposition, à valider | Votre premier défi tactique vous attend | Des milliers d’exercices en illimité et un mode challenge : battez votre premier record aujourd’hui. | Information (désinscription possible) |
| `59-premiers-pas-videos.html` | J+3 après la souscription d'un Pack Intégral, sauf s'il a déjà regardé une vidéo · proposition, à valider | Vos 4 rendez-vous vidéo de la semaine | Stratégie le lundi, légendes le mardi, calcul le mercredi, finales le vendredi : tout est dans votre Pack Intégral. | Information (désinscription possible) |
| `60-premiers-pas-revue.html` | J+7 après la souscription d'un Pack Intégral, sauf s'il a déjà ouvert la revue en ligne · proposition, à valider | Votre revue Europe Échecs est aussi en ligne | Le dernier numéro est inclus dans votre Pack Intégral, avec ses parties à rejouer coup par coup. | Information (désinscription possible) |
| `61-abonne-inactif.html` | Abonnés payants sans aucune vidéo, exercice ni partie depuis 21 jours, une seule fois par période d'inactivité · proposition, à valider | Ce que vous avez manqué ces 3 semaines | De nouvelles vidéos et de nouveaux exercices vous attendent dans votre [SERVICE]. | Information (désinscription possible) |

### Propositions · d'un produit à l'autre

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `62-livre-auteur-en-video.html` | 15 jours après la livraison d'un livre dont l'auteur a des vidéos sur Europe Échecs, à ceux qui n'ont pas le Pack Intégral · proposition, à valider | [AUTEUR_LIVRE] vous attend aussi en vidéo | L’auteur de votre livre présente [SERIE_AUTEUR] chaque semaine sur Europe Échecs. | Information (désinscription possible) |
| `63-choisir-ses-emails.html` | J+2 après la création d'un compte, une seule fois (et lien permanent dans le pied des e-mails d'information) · proposition, à valider | Choisissez ce que vous voulez recevoir | Actualités, vidéos, problème de la semaine, boutique : cochez ce qui vous intéresse, rien de plus. | Information (désinscription possible) |

### Compte · suite

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `65-bienvenue-compte.html` | Après l'activation d'un compte créé par le joueur (account_welcome). Si connexion par un fournisseur externe, ajouter la phrase [PHRASE_FOURNISSEUR] · modèle actuel du site | Bienvenue sur Europe Échecs ! | Votre compte est prêt : jouez, entraînez-vous, et découvrez nos vidéos, notre revue et nos livres. | Compte (toujours envoyé) |
| `66-suppression-demandee.html` | À la demande de suppression d'un compte (deletion_request) · modèle actuel du site | Demande de suppression de votre compte | Vous avez jusqu’au [DATE_ANNULATION] pour l’annuler depuis « Mon compte ». | Compte (toujours envoyé) |
| `67-suppression-annulee.html` | Quand le joueur annule sa demande de suppression (deletion_request_cancel) · modèle actuel du site | Votre compte est conservé | La demande de suppression du compte [PSEUDO] est annulée. | Compte (toujours envoyé) |
| `68-compte-inactif-6-mois.html` | Compte inutilisé depuis 6 mois, avant sa suppression (suppr_compte_avert1) · modèle actuel du site | Votre compte [PSEUDO] va être supprimé le [DATE_SUPPRESSION] | Il n’a pas été utilisé depuis 6 mois. Pour le garder, il suffit de vous reconnecter ou de renouveler votre abonnement. | Compte (toujours envoyé) |
| `69-liste-des-comptes.html` | Quand un joueur demande la liste de ses comptes, depuis l'oubli de mot de passe (renvoicomptesreset) · modèle actuel du site | Vos comptes sur Europe Échecs | Voici les comptes liés à votre adresse. Choisissez celui dont vous voulez changer le mot de passe. | Compte (toujours envoyé) |
| `70-connexion-externe-dissociee.html` | Quand le joueur dissocie son compte d'un fournisseur externe (account_provider_dissociated) · modèle actuel du site | Votre compte n’est plus lié à [FOURNISSEUR] | Désormais, connectez-vous avec votre pseudo et votre mot de passe. | Compte (toujours envoyé) |
| `71-consentement-a-jour.html` | Quand les choix du joueur sur ses données personnelles doivent être mis à jour (consent_update_required) · modèle actuel du site | Une mise à jour de vos préférences est nécessaire | Une minute pour confirmer vos choix sur l’utilisation de vos données, et continuer à utiliser votre compte. | Compte (toujours envoyé) |
| `72-compte-limite.html` | Quand une limite est appliquée à un compte sur la zone de jeu (account_limitation_applied) · modèle actuel du site | Une limite a été appliquée à votre compte | Limite : [LIMITE]. Durée : [DUREE_LIMITE]. | Compte (toujours envoyé) |
| `73-limite-levee.html` | Quand la limite est levée (account_limitation_revoked) · modèle actuel du site | La limite sur votre compte est levée | Vous retrouvez l’accès complet à la zone de jeu. | Compte (toujours envoyé) |
| `74-multicompte-invitation.html` | Quand un gestionnaire invite un compte existant dans son offre multicompte (multiaccount_join_invite) · modèle actuel du site | [GESTIONNAIRE] vous invite à rejoindre son offre multicompte | En acceptant, vous profitez de tous les services de son abonnement. Invitation valable [JOURS_VALIDITE] jours. | Compte (toujours envoyé) |
| `75-multicompte-reponse.html` | Au gestionnaire, quand l'invité accepte ou décline (multiaccount_join_invite_answer). [REPONSE] : « a accepté » ou « a décliné » · modèle actuel du site | Offre multicompte : [INVITE] [REPONSE] votre invitation | Retrouvez la gestion de votre offre multicompte dans « Mon compte ». | Compte (toujours envoyé) |
| `76-multicompte-detache.html` | Quand le gestionnaire détache un compte de son offre (multiaccount_detached) · modèle actuel du site | Votre compte ne fait plus partie de l’offre de [GESTIONNAIRE] | Les services de cette offre ne sont plus accessibles. Votre compte reste ouvert. | Compte (toujours envoyé) |

### Jeu en différé

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `79-differe-coup-joue.html` | À chaque coup de l'adversaire dans une partie en différé (jeudiffcoupjoue) · modèle actuel du site | [ADVERSAIRE] a joué : à vous ! | Votre partie commencée le [DATE_DEBUT] continue. Voyez la nouvelle position et jouez votre coup. | Compte (toujours envoyé) |
| `80-differe-partie-commencee.html` | Au début d'une partie en différé (jeudiffpartiedebut) · modèle actuel du site | Partie en différé commencée contre [ADVERSAIRE] | [BLANCS] contre [NOIRS], commencée le [DATE_DEBUT]. | Compte (toujours envoyé) |
| `81-differe-partie-terminee.html` | À la fin d'une partie en différé (jeudiffpartietermine) · modèle actuel du site | Partie en différé terminée contre [ADVERSAIRE] : [RESULTAT] | [BLANCS] – [NOIRS], [RESULTAT] ([RAISON_FIN]). | Compte (toujours envoyé) |
| `82-differe-invitation-tournoi.html` | Invitation à un tournoi privé en différé (jeudifftourninvit) · modèle actuel du site | [ORGANISATEUR] vous invite à un tournoi en différé | [CADENCE], [NB_JOUEURS_MAX] joueurs. Inscrivez-vous depuis la fiche du tournoi. | Compte (toujours envoyé) |
| `83-differe-tournoi-commence.html` | Au démarrage d'un tournoi en différé (jeudifftourndebut) · modèle actuel du site | Le tournoi en différé n° [ID_TOURNOI] commence | Ses parties sont ajoutées à vos parties en cours. | Compte (toujours envoyé) |
| `84-differe-tournoi-termine.html` | À la fin d'un tournoi en différé (jeudifftournfin) · modèle actuel du site | Le tournoi en différé n° [ID_TOURNOI] est terminé | Appariements, scores et parties : tout est sur la fiche du tournoi. | Compte (toujours envoyé) |
| `85-differe-tournoi-annule.html` | Quand un tournoi en différé est annulé faute de participants (jeudifftournannul) · modèle actuel du site | Le tournoi en différé n° [ID_TOURNOI] est annulé | Il n’a pas réuni assez de participants. D’autres tournois vous attendent. | Compte (toujours envoyé) |

### Tournois en direct

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `86-tournoi-invitation.html` | Invitation à un tournoi en direct (tourn_invitation) · modèle actuel du site | [ORGANISATEUR] vous invite à son tournoi | Découvrez le programme et donnez votre réponse en un clic. | Compte (toujours envoyé) |
| `87-tournoi-en-ligne.html` | Quand un tournoi est mis en ligne : aux participants ; variante organisateur dans le guide (tourn_created) · modèle actuel du site | Tournoi [NOM_TOURNOI] : votre participation est enregistrée | Début le [DATE_DEBUT_TOURNOI]. Toutes les infos sont sur la fiche du tournoi. | Compte (toujours envoyé) |
| `88-tournoi-demarre-bientot.html` | Avant le début d'un tournoi (tourn_start) · modèle actuel du site | Tournoi [NOM_TOURNOI] : début le [DATE_DEBUT_TOURNOI] | Connectez-vous quelques minutes avant pour être prêt. | Compte (toujours envoyé) |
| `89-tournoi-nouvelle-ronde.html` | Au début de chaque ronde (tourn_startround) · modèle actuel du site | Tournoi [NOM_TOURNOI] : la ronde [RONDE] commence | Elle dure jusqu’au [DATE_FIN_RONDE]. Votre appariement et votre horaire sont sur la fiche. | Compte (toujours envoyé) |
| `90-tournoi-rappel-partie.html` | Rappel avant une partie de tournoi (tourn_match_reminder) · modèle actuel du site | Rappel : votre partie de la ronde [RONDE], le [DATE_PARTIE] | Connectez-vous 5 à 10 minutes avant, par sécurité. | Compte (toujours envoyé) |
| `91-tournoi-horaire-propose.html` | Quand l'adversaire propose un autre horaire (tourn_proposreceived) · modèle actuel du site | Ronde [RONDE] : votre adversaire propose un autre horaire | Acceptez, refusez ou proposez un autre horaire depuis la fiche du tournoi. | Compte (toujours envoyé) |
| `92-tournoi-horaire-reponse.html` | Réponse de l'adversaire à une proposition d'horaire : acceptée, refusée ou retirée (tourn_proposaccepted, tourn_proposdenied, tourn_proposdeleted). [REPONSE_HORAIRE] selon le cas · modèle actuel du site | Ronde [RONDE] : horaire [REPONSE_HORAIRE_COURTE] | [REPONSE_HORAIRE] | Compte (toujours envoyé) |
| `93-tournoi-partie-reprogrammee.html` | Quand une partie est reprogrammée pour raison technique (tourn_match_reprog) · modèle actuel du site | Ronde [RONDE] : votre partie est reprogrammée | Nouvel horaire : [NOUVEL_HORAIRE] au lieu de [ANCIEN_HORAIRE]. | Compte (toujours envoyé) |
| `94-tournoi-ronde-retardee.html` | Quand une ronde démarre ou finit en retard (tourn_round_shifted, tourn_roundend_updat) · modèle actuel du site | Ronde [RONDE] : nouvel horaire de fin | La ronde se termine le [NOUVELLE_FIN] au lieu du [FIN_PREVUE]. | Compte (toujours envoyé) |
| `95-tournoi-appariement-manuel.html` | À l'organisateur, quand l'appariement automatique est impossible (tourn_round_manualpairingrequired) · modèle actuel du site | Ronde [RONDE] : appariement manuel nécessaire | Les règles d’appariement ne peuvent pas être respectées automatiquement. Votre intervention est nécessaire. | Compte (toujours envoyé) |
| `96-tournoi-termine.html` | À la fin d'un tournoi en direct (tourn_end) · modèle actuel du site | Tournoi [NOM_TOURNOI] : les résultats | Classement, parties et résultats : tout est sur la fiche du tournoi. | Compte (toujours envoyé) |
| `97-tournoi-instructions.html` | Quelques heures avant un événement-tournoi d'Europe Échecs (tourn_instructions) · modèle actuel du site | [NOM_EVENEMENT] : les instructions | Le [DATE_EVENEMENT], heure de Paris. Tout ce qu’il faut savoir pour bien jouer. | Compte (toujours envoyé) |

### Événements et masterclasses

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `100-evenement-refuse.html` | Inscription à un événement refusée (event_reject) · modèle actuel du site | [NOM_EVENEMENT] : votre inscription n’a pas pu être validée | Contactez-nous pour en savoir plus. | Compte (toujours envoyé) |
| `101-cours-inscription.html` | Inscription à un cours ou un stage (course_confirmation) · modèle actuel du site | Inscription confirmée : [NOM_COURS] | Votre réservation est confirmée. Nous revenons vers vous très vite avec les détails pratiques. | Compte (toujours envoyé) |
| `102-masterclass-inscription.html` | Inscription à une masterclass (masterclass_confirm) · modèle actuel du site | Masterclass « [TITRE_MASTERCLASS] » : vous êtes inscrit | Retrouvez la page de la masterclass pour la date et le lien. | Compte (toujours envoyé) |
| `103-masterclass-invitation.html` | Invitation gratuite à une masterclass, avec un code (masterclass_invit) · modèle actuel du site | Votre invitation à la masterclass « [TITRE_MASTERCLASS] » | Votre place est offerte : 3 étapes pour l’activer avec votre code. | Compte (toujours envoyé) |
| `98-evenement-en-attente.html` | Inscription à un événement en attente de validation (event_waiting) · modèle actuel du site | [NOM_EVENEMENT] : inscription reçue | Vous recevrez un e-mail dès sa validation par les organisateurs. | Compte (toujours envoyé) |
| `99-evenement-valide.html` | Inscription à un événement validée (event_confirm) · modèle actuel du site | [NOM_EVENEMENT] : votre inscription est validée | Vous recevrez les instructions du tournoi quelques heures avant l’événement. | Compte (toujours envoyé) |

### Fair-play

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `104-fairplay-suite-signalement.html` | À l'auteur d'un signalement, une fois le dossier examiné. [CONCLUSION] selon le cas : infraction confirmée, non confirmée, doute, ou message de l'équipe (les 5 modèles fairplaycase_*_to_reporter) · modèle actuel du site | Votre signalement de [SUSPECT] a été examiné | Merci de votre vigilance. Voici notre conclusion. | Compte (toujours envoyé) |
| `105-fairplay-adversaire.html` | Aux adversaires d'un joueur sanctionné ou en doute (les 3 modèles fairplaycase_*_to_third_party_player) · modèle actuel du site | Fair-play : une décision concerne un de vos adversaires | [SUSPECT] : [CONSTAT]. Vos parties et votre Elo ont pu être corrigés. | Compte (toujours envoyé) |
| `106-fairplay-avertissement.html` | Au joueur concerné par une infraction (fairplaycase_violation_to_suspect) · modèle actuel du site | Fair-play : à propos de votre compte | Une activité récente pose question. Consultez la page de votre dossier. | Compte (toujours envoyé) |
| `107-probleme-traite.html` | Après le traitement d'un problème sur une ou plusieurs parties (problem_solved et problem_solved_user, identiques) · modèle actuel du site | Un problème sur vos parties a été traité | [PROBLEME] : voici la solution adoptée. | Compte (toujours envoyé) |

### Communauté

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `108-message-d-un-joueur.html` | Quand un joueur écrit à un autre depuis le site (contactjoueursmsg) · modèle actuel du site | [EXPEDITEUR_PSEUDO] vous a envoyé un message | « [DEBUT_MESSAGE] » | Compte (toujours envoyé) |
| `109-commentaire-non-valide.html` | Quand un commentaire d'article n'est pas validé (refuscommentaire) · modèle actuel du site | Votre commentaire n’a pas été publié | Sur l’article « [TITRE_ARTICLE] ». La charte de publication est en bas de chaque article. | Compte (toujours envoyé) |
| `110-battle-commence.html` | Au début d'une battle de puzzles (puzzlesbattledebut) · modèle actuel du site | Battle de puzzles n° [ID_BATTLE] : c’est parti ! | [JOUEUR_1] contre [JOUEUR_2]. À vous de jouer ! | Compte (toujours envoyé) |
| `111-battle-terminee.html` | À la fin d'une battle de puzzles (puzzlesbattlefin) · modèle actuel du site | Battle de puzzles n° [ID_BATTLE] : le résultat | [JOUEUR_1] contre [JOUEUR_2] : découvrez qui l’emporte. | Compte (toujours envoyé) |

### Support

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `112-support-demande-recue.html` | À l'enregistrement d'une demande de support (supportdemenreg) · modèle actuel du site | Votre demande est bien enregistrée | Nous vous écrivons à chaque étape. Suivez-la et répondez depuis le lien. | Compte (toujours envoyé) |
| `113-support-reponse.html` | Quand le support a répondu (supportdemchgetat) · modèle actuel du site | Réponse à votre demande : [OBJET_DEMANDE] | Notre équipe a examiné votre demande. Lisez la réponse et poursuivez l’échange. | Compte (toujours envoyé) |
| `114-message-de-l-equipe.html` | Message libre d'un administrateur (support_mail_direct ; mail_direct a le même usage) · modèle actuel du site | [TITRE_MESSAGE] | Un message de l’équipe d’Europe Échecs. | Compte (toujours envoyé) |

### PrediChess

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `115-predichess-premier.html` | Au 1er du classement PrediChess d'un événement (predichess_prize_first) · modèle actuel du site | PrediChess [EVENEMENT] : vous avez gagné ! | 1re place : un sweat Europe Échecs vous attend. Il nous faut votre adresse, votre taille et votre couleur. | Compte (toujours envoyé) |
| `116-predichess-classement.html` | Aux joueurs du top 4 (3 mois) et du top 20 (1 mois) PrediChess (predichess_prize_top4, predichess_prize_top20) · modèle actuel du site | PrediChess [EVENEMENT] : vous êtes dans le top [RANG] ! | Vous gagnez [DUREE_OFFERTE] de Pack Intégral. Activez-le avec votre code cadeau. | Compte (toujours envoyé) |

### Parrainage

| Fichier | Quand l'envoyer | Objet | Pré-en-tête | Type |
|---|---|---|---|---|
| `117-parrainage-invitation.html` | Invitation envoyée par un parrain à un ami, puis rappel (sponsorship_invitation et sponsorship_remind_invitation, identiques) · modèle actuel du site | [PRENOM_OU_EMAIL_PARRAIN] vous invite à jouer aux échecs | Créez votre compte gratuit et défiez des joueurs du monde entier. Votre période d’essai est doublée. | Information (désinscription possible) |
| `118-parrainage-ami-inscrit.html` | Au parrain, quand un ami invité crée son compte (sponsorship_create_account) · modèle actuel du site | Votre ami a créé son compte | Après [NB_PARTIES_PARRAINAGE] parties jouées, votre parrainage sera validé. | Compte (toujours envoyé) |
| `119-parrainage-valide.html` | Au parrain, quand un parrainage est validé ; avec bonus débloqué si un palier est atteint (sponsorship_activate_account et _level_up) · modèle actuel du site | Parrainage validé : merci ! | Le parrainage de [EMAIL_FILLEUL] est validé. [ETAT_BONUS] | Compte (toujours envoyé) |
| `120-parrainage-ami-abonne.html` | Au parrain, quand un filleul s'abonne ; avec bonus si un palier est atteint (sponsorship_activate_subscription et _level_up) · modèle actuel du site | Votre ami s’est abonné ! | [EMAIL_FILLEUL] vient de s’abonner. [ETAT_BONUS] | Compte (toujours envoyé) |
| `121-parrainage-relancez.html` | Au parrain dont des invités n'ont pas activé leur compte (sponsorship_remind_sponsor_activation) · modèle actuel du site | Vos amis n’ont pas encore activé leur compte | Relancez-les : chaque parrainage validé prolonge votre abonnement. | Information (désinscription possible) |
| `122-parrainage-adresse-erreur.html` | Quand l'invitation n'a pas pu être envoyée (sponsorship_email_error) · modèle actuel du site | Votre invitation n’a pas pu être envoyée à [EMAIL_FILLEUL] | Vérifiez l’adresse dans « Mes parrainages » et corrigez-la si besoin. | Compte (toujours envoyé) |

## Variables

La liste complète est générée dans `build/_emails-ee_variables.txt`.
