# E-mails Europe Échecs : bilan, audit et plan d'amélioration

Relu le 28 novembre 2026 : les 117 e-mails de `emails-ee/` (01 à 63 et 65 à 122), texte, objets, pré-en-têtes, rendu téléphone (clair et sombre)
et ordinateur. Ce document donne un avis, la liste de ce qu'il faut corriger, un plan sur 90 jours et des pistes graphiques.
**Rien n'est changé en profondeur pour l'instant** : seules les erreurs franches ont été corrigées (liste en fin de document).

## 0. Bilan de la reprise des modèles du site (25 novembre 2026)

Les 94 modèles de l'extraction qui n'avaient pas encore leur version ont été refaits : **58 nouveaux e-mails (65 à 122)**.
En regroupant les doublons du site, 94 modèles tiennent en 58. La série Europe Échecs compte maintenant **117 e-mails**.

- Page de validation (117 fiches) : https://claude.ai/artifact/RviFWXwnAD52PcX8Z1nhKv
- Correspondance modèle du site → nouvel e-mail : `EMAILS-EE.md` (tableau « Correspondance avec les modèles du site »).
- Ce qu'il faut brancher : `DEVELOPPEURS-EE.md` (section 4 quinquies pour 65 à 122).
- Contrôle : aucun débordement à 375 px, en clair comme en sombre. L'image des sweats a été retirée de l'e-mail du gagnant PrediChess (115) :
  elle affichait le « −10 % » de la promo du 4 novembre.

### Comparaison avec les 59 e-mails déjà faits

Ce qui se recoupe (à trancher) :
- **Accueil, trop d'e-mails d'un coup** : 01 (activation), 65 (bienvenue, compte créé par le joueur) et 05 (découverte de la zone de jeu) partent à quelques minutes d'écart,
  et le 63 (choisir ses e-mails) suit à J+2. Proposition : fusionner le 65 et le 05.
- **Préférences d'e-mails, trois e-mails proches** : 63 (choisir ses e-mails), 71 (préférences de données à confirmer) et 78 (newsletter à reconfirmer).
  Ils peuvent tous renvoyer vers la même page de préférences.
- **Inactivité** : les relances 25 à 27 (comptes gratuits) disent « dernière relance » à 45 jours, puis le 68 (compte supprimé après 6 mois) arrive plus tard.
  Ça se tient, puisque le 68 est un e-mail de compte, pas d'information. Mais le 68 dit « renouvelez votre abonnement », ce qui ne colle pas pour un compte gratuit.
- **Newsletter** : le modèle du site annonçait un envoi « du 1er au 5 du mois », alors que le 33 part chaque lundi. Le 77 dit « chaque semaine », comme le 33.
- **Parrainage (117)** : la « période d'essai doublée » vient du modèle actuel du site. Aucune période d'essai n'apparaît dans les formules ni dans les 59 autres e-mails :
  il faut confirmer qu'elle existe encore.
- **Pas repris** : `questionnaire_satisfaction_fr` (déjà couvert par le 47), `cmdsent` (couvert par le 52), `ccas_tournament_soon` (c'est la série CCAS).

Ce qui ne se recoupe pas : jeu en différé, tournois, événements, fair-play, support, PrediChess et parrainage sont tous des sujets nouveaux.

### Doublons du site regroupés

- relance1/relance2 web et revue : textes identiques, déjà remplacés par 10, 29, 16 et 30
- `relancepackprogresser` et `relanceoldpackjeu` : un seul texte
- fair-play : 8 modèles → 3 e-mails (104, 105, 106)
- horaires de tournoi : 3 réponses → 1 (92) ; ronde décalée : 2 → 1 (94)
- `problem_solved` et `_user`, invitation et rappel de parrainage, `mail_direct` et `support_mail_direct` : identiques deux à deux, un e-mail à chaque fois

### Erreurs corrigées dans les modèles actuels

- `tourn_end` avait pour objet « Invitation à rejoindre le tournoi »
- Horaires des tournois : en GMT sur le site, maintenant en heure de Paris
- « 1 email par jour pendant x jours », et des fautes : parmis, Dancs, il vous ait, a commencée, gène, compte à rebour, Faîtes,
  « aucune action est nécessaire », guillemet en trop dans `refuscommentaire`
- Signatures « L'équipe Simple Chess » et « Europe Echecs » sans accent, et « Cher membre » : le tout est remplacé
- `welcome_subscription` envoyait le mot de passe en clair (déjà supprimé dans le 07)

### À voir avec les développeurs

- **108 (message d'un joueur)** : on y répond en répondant à l'e-mail, ce qui dévoile l'adresse de l'expéditeur au destinataire. Il faudrait passer par une messagerie du site.
- **52 (commande expédiée)** : le modèle actuel du site passe par le site tiers parcelsapp.com pour le suivi. Mieux vaut le lien du transporteur.
- **103 (invitation masterclass)** : il faut entrer un code promo dans le panier, ce qui est lourd. Un lien d'inscription direct serait plus simple.
- **97 (instructions de tournoi)** : raccourci en 5 étapes. Le texte complet est mieux sur une page d'aide.

### Questions encore ouvertes

Date limite de commande pour Noël (40), mot de passe en multicompte (02), activation et connexion Google/Apple (01),
modules de la boutique (54, 56, 57) et page de préférences à créer (63).

## 1. En une minute

- **La base est solide.** Un seul moteur, une seule mise en page, des textes relus, aucune variable inventée, aucun débordement à 375 px, mode sombre testé.
  Les 94 modèles du site sont tous couverts, et 16 doublons du site disparaissent.
- **Le vrai risque n'est plus le texte, c'est la pression.** Un nouveau membre peut recevoir 5 à 7 e-mails en une semaine (01, 65, 05, 06, 24, 63, puis 58 s'il s'abonne),
  et un membre actif jusqu'à 4 e-mails d'information par semaine (33, 43, 28, plus une promo 34). Sans règle de pression commune, les désinscriptions monteront.
- **Trois chantiers d'abord** : (1) une règle de pression et de priorité entre e-mails, (2) une seule page de préférences pour 63, 71 et 78,
  (3) des objets et pré-en-têtes plus courts et moins répétitifs (40 objets sur 117 commencent par « Votre », 22 répètent « Europe Échecs », que l'expéditeur affiche déjà).

## 2. Ce qui marche bien (à garder)

- **Le titre en deux temps** (« À vous | de jouer ! ») et le bandeau marine : on reconnaît Europe Échecs d'un coup d'œil, chaque rubrique a sa couleur de logo et sa pièce.
- **Les e-mails de service sont nets** : une phrase qui dit ce qui se passe, un encadré de faits (date, montant, partie), un seul bouton. C'est ce qu'on attend d'un mail de compte ou de tournoi.
- **Les relances d'abonnement** (10, 29, 32, 21) ont une vraie logique de séquence : rappel, dernier jour, expiration, reconquête à J+30, avec un angle différent à chaque fois.
- **Les tarifs sont écrits en clair**, et le tarif revue + Pack est limité aux formules 1 et 2 ans, comme confirmé.
- **Aucune promesse inventée** : quand une donnée manque, elle reste en variable.

## 3. À corriger avant la mise en service

| Priorité | Problème | E-mails | Correction proposée |
|---|---|---|---|
| 1 | Trop d'e-mails à l'inscription | 01, 65, 05, 06, 24, 63 | Fusionner 65 et 05 (un seul « bienvenue + zone de jeu ») ; décaler 63 à J+5 ; pas plus d'un e-mail d'information par jour |
| 1 | Pas de règle de pression | tous les e-mails d'information | Au plus 3 e-mails d'information par semaine et par personne ; ordre de priorité : service > paiement > relance d'abonnement > premiers pas > bilans > newsletter > promo |
| 1 | Trois e-mails de préférences | 63, 71, 78 | Une seule page « Mes e-mails » (fréquence, sujets, pause de 30 jours) ; 71 et 78 y renvoient |
| 1 | 295 variables | tous | Une valeur par défaut pour chacune, ou pas d'envoi : aucune variable ne doit partir telle quelle (`_emails-ee_variables.txt` en donne la liste) |
| 2 | Heure en GMT sur le site | 04 et les tournois | Tout en heure de Paris (04 corrigé ici ; le site doit convertir l'heure) |
| 2 | Compte gratuit relancé pour « renouveler son abonnement » | 68 | Deux variantes : compte gratuit (« reconnectez-vous ») et ancien abonné (« renouvelez ») |
| 2 | Réponse qui dévoile l'adresse e-mail | 108 | Répondre par une messagerie sur le site, pas par e-mail |
| 2 | « Période d'essai doublée », « Jeu en Direct » | 117, 119, 120 | Vérifier que ce bonus de parrainage existe encore avec les formules actuelles, sinon réécrire |
| 2 | Suivi de colis par un site tiers | 52 | Lien direct du transporteur |
| 3 | « Ne répondez pas à cet e-mail » | 114, 115, 116 | Une adresse de réponse lue par quelqu'un : meilleure délivrabilité, moins de frustration |
| 3 | Masterclass offerte via un code promo dans le panier | 103 | Lien d'inscription direct, déjà validé |
| 3 | Accords au masculin (« inscrit », « invité », « le bienvenu ») | 77, 87, 102, 117 | Tournures neutres : « Inscription confirmée », « Bienvenue ! » |

## 4. Textes (copywriting)

**Diagnostic :** les textes ont déjà une voix (vouvoiement chaleureux, phrases courtes, vocabulaire des joueurs). On ne réécrit pas : on resserre.

- **Objets.** Retirer « Europe Échecs » quand l'expéditeur le dit déjà (01, 02, 03, 04, 10, 16, 17, 20, 28, 44, 49, 77, 78…). Varier les débuts :
  mettre en tête ce qui concerne le lecteur (le pseudo de l'adversaire, la date, le montant, le résultat), comme le font déjà le 79 (« TourDeFrance a joué : à vous ! ») et le 81.
- **Pré-en-têtes.** 15 dépassent 100 caractères et seront coupés sur téléphone (07, 22, 28, 30, 39, 40, 41, 50, 59, 68, 71, 74, 95, 115, 117). Viser 40 à 90 caractères, le fait le plus utile en premier.
- **Points d'exclamation.** Bien dans les titres de fête (bienvenue, victoire PrediChess, parrainage validé) ; à retirer des e-mails de service et de paiement.
- **Boutons.** Ils disent déjà ce qu'on obtient (« Jouer mon coup », « Activer mon Pack Intégral »). À garder : ne jamais revenir à « En savoir plus ».
- **Exemples d'objets à tester** (même promesse, sans rien inventer) :
  - 06 offre de bienvenue : « −25 % sur les Packs 1 et 2 ans, pendant 48 h » / « [PSEUDO], votre code de bienvenue : −25 % »
  - 10 échéance : « Votre [SERVICE] s'arrête le [DATE_FIN] » / « [PSEUDO], votre abonnement arrive à échéance »
  - 21 reconquête : « Ce qui a changé depuis votre départ » / « [PSEUDO], la zone de jeu vous attend »
  - 46 panier abandonné : « Votre [SERVICE] est resté dans le panier » / « Il ne manque qu'un clic pour votre [SERVICE] »
  - 57 panier boutique : « [NOM_ARTICLE_1] vous attend dans votre panier »

## 5. Graphisme : trois pistes (à choisir, rien n'est changé)

1. **Deux gabarits au lieu d'un.** Garder le bandeau marine pour les e-mails d'information et les grands moments ; créer un gabarit **compact** pour les
   notifications fréquentes (jeu en différé, tournois, fair-play, support : 79 à 114) : en-tête blanc de 60 px, logo bleu, pas de pièce ni de damier,
   le fait principal en première ligne. On lit tout sans faire défiler, et les e-mails marketing restent plus visibles par contraste.
2. **Gabarit « Revue » pour l'éditorial.** Newsletter, revue, problème de la semaine, vidéos de la semaine (33, 42, 43, 28) : titres en serif, filet fin,
   grande image d'article, comme une page de magazine. Ça rapproche les e-mails de la revue papier, l'actif le plus ancien de la marque (depuis 1959).
3. **Diagrammes générés.** Pour 79 (coup joué), 81 (partie terminée), 43 (problème) et 45 (cap franchi), une image de l'échiquier générée par le site
   avec la vraie position, plutôt qu'une image générique. C'est le visuel le plus « échecs » possible, et il est différent à chaque envoi.

**Maquettes** (actuel à gauche, puis la piste, sur 4 ou 5 e-mails chacune) : https://claude.ai/artifact/CRtoDDQT44ftdMP9tSZkeD — générées par `scripts/maquettes-ee.py`.
Recommandation : compact + diagramme pour le jeu en différé et les tournois, Revue pour l'éditorial, gabarit actuel pour tout le reste.

## 6. Plan sur 90 jours (AARRR)

**Objectif principal :** le nombre d'abonnés payants actifs (Pack Jeu+ ou Pack Intégral, au moins une connexion dans le mois).

| Semaines | Étape | Actions | Étape du parcours |
|---|---|---|---|
| 1–2 | Débloquer | Trancher les points ouverts (40 Noël, 02, 01, boutique, 117) ; fixer la règle de pression ; SPF, DKIM, DMARC, désinscription en un clic | toutes |
| 1–2 | Remplacer l'existant | Mettre en ligne les e-mails qui remplacent des modèles du site : 01 à 04, 07 à 11, 16, 17, 29, 30, 51 à 53, 65 à 122 | Activation, Rétention |
| 3–4 | Fondations | Page « Mes e-mails » (63, 71, 78) ; UTM sur tous les liens (`utm_source=email&utm_campaign=ee-<numéro>`) ; envois de test sur Gmail, iPhone et Outlook | toutes |
| 5–8 | Accélérer | Bienvenue et premiers pas (06, 24, 58 à 60, 63) ; paiement mensuel (18 à 20, 31) ; relances et reconquête (10, 29, 32, 21, 23) | Activation, Revenu |
| 9–12 | Faire durer | Bilans (44, 45, 49), anniversaire (48), satisfaction (47), boutique (54, 56, 57), parrainage relancé aux moments de satisfaction (45, 48, 53) | Rétention, Parrainage |
| 9–12 | Tester | Un test A/B d'objet par mois, sur les e-mails à fort volume (06, 10, 33) | Revenu |

**Mesures à suivre chaque semaine :**
- Activation : part des nouveaux abonnés qui font un exercice, regardent une vidéo ou ouvrent la revue dans les 7 jours (cohortes dont les 7 jours sont écoulés seulement).
- Revenu : taux de renouvellement après 10/29/32, taux de récupération des paiements refusés (18/31), ventes avec le code de bienvenue (06/24).
- Santé de la liste : désinscriptions sous 0,3 % par envoi, plaintes pour spam sous 0,1 %. Au-delà, on baisse la pression avant de toucher aux textes.

## 7. Nouvelles idées (à valider, aucune n'est faite)

- **Parrainage au bon moment** : un petit bloc « Invitez un ami » dans 45 (cap franchi), 48 (anniversaire) et 53 (commande livrée), là où le membre est content.
- **Clubs et entraîneurs** (offre multicompte) : une courte séquence pour les gestionnaires (bienvenue, comment inviter, bilan du groupe au mois) ;
  c'est aussi la seule cible où une prospection par e-mail aurait du sens (clubs, écoles), à faire depuis une adresse dédiée et avec une liste vérifiée.
- **Après une masterclass ou un tournoi d'Europe Échecs** : un e-mail de remerciement avec le replay ou les résultats, et la prochaine date.
- **Pause plutôt que désinscription** : sur la page « Mes e-mails », un bouton « Pause 30 jours », qui retient une partie de ceux qui partiraient.

Pas retenu : la partie du jour et le Black Friday (écartés), et la prospection par e-mail auprès des particuliers (non sollicitée, et contraire au RGPD).

## 8. Corrections faites pendant l'audit

- 04 : heure de la suppression en heure de Paris (au lieu de GMT).
- 33 (exemple de la newsletter) : « Grand Maître » avec les majuscules.
- 118 : pré-en-tête au neutre (« Après [NB_PARTIES_PARRAINAGE] parties jouées, votre parrainage sera validé »).
- 115 : image des sweats retirée (elle affichait le −10 % d'une promo passée) ; 77 : fréquence de la newsletter alignée sur le 33 (chaque semaine).
- Variable du parrainage renommée `[NB_PARTIES_PARRAINAGE]` (elle avait le même nom que celle du bilan mensuel 44).
- Balayage automatique des 117 e-mails : orthographe de la marque, tutoiement, majuscules des pièces et des titres, ponctuation française, mots répétés : rien d'autre à signaler.
