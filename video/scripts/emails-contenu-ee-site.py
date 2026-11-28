# Suite de la série Europe Échecs : tous les autres modèles actuels du site (extraction du 25 novembre 2026, 94 modèles),
# réécrits au design de la série. Exécuté par emails-contenu-ee.py. Les textes reprennent les modèles du site, sans rien ajouter :
# les variables du site sont gardées (en majuscules) et listées dans DEVELOPPEURS-EE.md. Doublons du site regroupés (voir EMAILS-EE.md).
S_COMPTE, S_DIFFERE, S_TOURNOIS, S_EVENEMENTS = "Compte · suite", "Jeu en différé", "Tournois en direct", "Événements et masterclasses"
S_FAIRPLAY, S_COMMU, S_SUPPORT, S_PREDI, S_PARRAIN = "Fair-play", "Communauté", "Support", "PrediChess", "Parrainage"
INFO_SITE = " · modèle actuel du site"

def lignes_partie():   # la partie en cours : joueurs et coups (une ligne par coup, à dupliquer)
    return ('<!-- COUPS : une ligne par coup -->' f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 22px;border:1px solid #e4e1d8;border-radius:12px">'
            f'<tr><td style="padding:12px 16px;font:bold 14px {SANS};color:{C["texte"]};border-bottom:1px solid #e4e1d8">[BLANCS] (Blancs) · [NOIRS] (Noirs)</td></tr>'
            f'<tr><td style="padding:10px 16px;font:15px/1.7 {SANS};color:{C["texte"]}">[LISTE_COUPS]</td></tr></table>')

def fiche_tournoi():   # caractéristiques d'un tournoi en différé
    return infos([("Type de jeu", "[TYPE_JEU]"), ("Matchs", "[TYPE_MATCHS]"), ("Cadence", "[CADENCE]"), ("Elo", "[ELO_MIN] – [ELO_MAX]"), ("Joueurs", "[NB_JOUEURS_MAX]")])

GMT = petit("Les horaires sont en heure de Paris sur la fiche du tournoi.")

# ---------- Compte · suite ----------
mail(id="65-bienvenue-compte", cat=S_COMPTE, marketing=False, quand="Après l'activation d'un compte créé par le joueur (account_welcome). Si connexion par un fournisseur externe, ajouter la phrase [PHRASE_FOURNISSEUR]" + INFO_SITE,
     objet="Bienvenue sur Europe Échecs !", pre="Votre compte est prêt : jouez, entraînez-vous, et découvrez nos vidéos, notre revue et nos livres.", sur="Bienvenue", titre="Bienvenue, | [PSEUDO] !",
     corps=[para("Bonjour [PSEUDO], votre compte est prêt. Vous pouvez commencer à jouer et à vous entraîner dès maintenant."),
            bouton("Jouer une partie", L("ZONE_DE_JEU")),
            liste(['<b>Nos vidéos</b>, pour progresser à votre rythme', '<b>Notre revue</b>, chaque mois', '<b>Nos livres</b>, sur boutique.echecs.com']),
            para(petit('Une question ? <a href="[LIEN_AIDE]" style="color:#6b6b66">Contactez-nous</a>.'))])
mail(id="66-suppression-demandee", cat=S_COMPTE, marketing=False, quand="À la demande de suppression d'un compte (deletion_request)" + INFO_SITE,
     objet="Demande de suppression de votre compte", pre="Vous avez jusqu'au [DATE_ANNULATION] pour l'annuler depuis « Mon compte ».", sur="Votre compte", titre="Suppression | demandée.",
     corps=[para("Bonjour, une demande de suppression du compte <b>[PSEUDO]</b> a été faite le [DATE_DEMANDE]."),
            infos([("Annulation possible jusqu'au", "[DATE_ANNULATION]"), ("Suppression définitive avant le", "[DATE_SUPPRESSION]")]),
            para("Passé ce délai, le compte et toutes ses données seront effacés. Si vous n'êtes pas à l'origine de cette demande, annulez-la tout de suite :"),
            bouton("Annuler la suppression", L("MON_COMPTE"))])
mail(id="67-suppression-annulee", cat=S_COMPTE, marketing=False, quand="Quand le joueur annule sa demande de suppression (deletion_request_cancel)" + INFO_SITE,
     objet="Votre compte est conservé", pre="La demande de suppression du compte [PSEUDO] est annulée.", sur="Votre compte", titre="Votre compte | est conservé.",
     corps=[para("Bonjour, comme vous l'avez demandé, la suppression du compte <b>[PSEUDO]</b> est annulée. Rien ne change pour vous."),
            bouton("Retourner sur Europe Échecs", L("ZONE_DE_JEU"))])
mail(id="68-compte-inactif-6-mois", cat=S_COMPTE, marketing=False, quand="Compte inutilisé depuis 6 mois, avant sa suppression (suppr_compte_avert1)" + INFO_SITE,
     objet="Votre compte [PSEUDO] va être supprimé le [DATE_SUPPRESSION]", pre="Il n'a pas été utilisé depuis 6 mois. Pour le garder, il suffit de vous reconnecter ou de renouveler votre abonnement.", sur="Votre compte", titre="On garde | votre compte ?",
     corps=[para("Bonjour, le compte <b>[PSEUDO]</b> n'a pas été utilisé depuis 6 mois. Il sera supprimé le <b>[DATE_SUPPRESSION]</b>."),
            para("Pour le conserver, renouvelez votre abonnement dès maintenant :"),
            bouton("Garder mon compte", L("ABONNEMENTS"))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")
mail(id="69-liste-des-comptes", cat=S_COMPTE, marketing=False, quand="Quand un joueur demande la liste de ses comptes, depuis l'oubli de mot de passe (renvoicomptesreset)" + INFO_SITE,
     objet="Vos comptes sur Europe Échecs", pre="Voici les comptes liés à votre adresse. Choisissez celui dont vous voulez changer le mot de passe.", sur="Vos comptes", titre="Vos comptes | Europe Échecs.",
     corps=[para("Bonjour, comme demandé, voici les comptes liés à votre adresse e-mail. Pour choisir un nouveau mot de passe, cliquez à côté du compte concerné :"),
            '<!-- COMPTE : une ligne par compte -->' + infos([("[PSEUDO_1]", '<a href="[LIEN_NOUVEAU_MDP_1]" style="color:#1f6fc0;font-weight:700">Nouveau mot de passe</a>'), ("[PSEUDO_2]", '<a href="[LIEN_NOUVEAU_MDP_2]" style="color:#1f6fc0;font-weight:700">Nouveau mot de passe</a>')]),
            para(petit("Vous n'avez rien demandé ? Ignorez cet e-mail : vos mots de passe ne changent pas."))])
mail(id="70-connexion-externe-dissociee", cat=S_COMPTE, marketing=False, quand="Quand le joueur dissocie son compte d'un fournisseur externe (account_provider_dissociated)" + INFO_SITE,
     objet="Votre compte n'est plus lié à [FOURNISSEUR]", pre="Désormais, connectez-vous avec votre pseudo et votre mot de passe.", sur="Votre compte", titre="Compte dissocié | de [FOURNISSEUR].",
     corps=[para("Bonjour, comme vous l'avez demandé, le compte <b>[PSEUDO]</b> n'est plus lié à <b>[FOURNISSEUR]</b>. Désormais, connectez-vous avec votre pseudo et votre mot de passe."),
            bouton("Choisir un mot de passe", "[LIEN_NOUVEAU_MDP]"),
            para(petit("Vous avez oublié votre mot de passe ? Le bouton ci-dessus vous permet d'en choisir un nouveau."))])
mail(id="71-consentement-a-jour", cat=S_COMPTE, marketing=False, quand="Quand les choix du joueur sur ses données personnelles doivent être mis à jour (consent_update_required)" + INFO_SITE,
     objet="Une mise à jour de vos préférences est nécessaire", pre="Une minute pour confirmer vos choix sur l'utilisation de vos données, et continuer à utiliser votre compte.", sur="Vos données", titre="Vos préférences | à confirmer.",
     corps=[para("Bonjour [PSEUDO], vos choix concernant l'utilisation de vos données personnelles doivent être mis à jour. C'est nécessaire pour continuer à utiliser pleinement votre compte et ses services."),
            bouton("Mettre à jour mes préférences", "[LIEN_CONSENTEMENT]")])
mail(id="72-compte-limite", cat=S_COMPTE, marketing=False, quand="Quand une limite est appliquée à un compte sur la zone de jeu (account_limitation_applied)" + INFO_SITE,
     objet="Une limite a été appliquée à votre compte", pre="Limite : [LIMITE]. Durée : [DUREE_LIMITE].", sur="Votre compte", titre="Une limite | sur votre compte.",
     corps=[para("Bonjour [PSEUDO], pour que la zone de jeu reste sûre et respectueuse pour tous, une limite a été appliquée à votre compte :"),
            infos([("Limite", "[LIMITE]"), ("Durée", "[DUREE_LIMITE]")]),
            para('Nous vous invitons à relire <a href="[LIEN_CHARTE]" style="color:#1f6fc0;font-weight:700">notre code de conduite</a>. Si vous pensez qu\'il s\'agit d\'une erreur, ou si vous avez une question, notre équipe vous répond :'),
            bouton("Contacter l'équipe", "[LIEN_AIDE]")],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="73-limite-levee", cat=S_COMPTE, marketing=False, quand="Quand la limite est levée (account_limitation_revoked)" + INFO_SITE,
     objet="La limite sur votre compte est levée", pre="Vous retrouvez l'accès complet à la zone de jeu.", sur="Votre compte", titre="Limite | levée.",
     corps=[para("Bonjour [PSEUDO], la limite appliquée à votre compte (<b>[LIMITE]</b>) est levée. Merci de contribuer à une zone de jeu agréable pour tous."),
            bouton("Jouer une partie", L("ZONE_DE_JEU"))])
mail(id="74-multicompte-invitation", cat=S_COMPTE, marketing=False, quand="Quand un gestionnaire invite un compte existant dans son offre multicompte (multiaccount_join_invite)" + INFO_SITE,
     objet="[GESTIONNAIRE] vous invite à rejoindre son offre multicompte", pre="En acceptant, vous profitez de tous les services de son abonnement. Invitation valable [JOURS_VALIDITE] jours.", sur="Offre multicompte", titre="Une invitation | de [GESTIONNAIRE].",
     corps=[para("Bonjour [PSEUDO], <b>[GESTIONNAIRE]</b> vous invite à rejoindre son offre multicompte. En acceptant, vous profiterez de tous les services de son abonnement."),
            bouton("Répondre à l'invitation", "[LIEN_INVITATION]"),
            para(petit("Cette invitation est valable [JOURS_VALIDITE] jours."))])
mail(id="75-multicompte-reponse", cat=S_COMPTE, marketing=False, quand="Au gestionnaire, quand l'invité accepte ou décline (multiaccount_join_invite_answer). [REPONSE] : « a accepté » ou « a décliné »" + INFO_SITE,
     objet="Offre multicompte : [INVITE] [REPONSE] votre invitation", pre="Retrouvez la gestion de votre offre multicompte dans « Mon compte ».", sur="Offre multicompte", titre="[INVITE] | [REPONSE] votre invitation.",
     corps=[para("Bonjour [PSEUDO], <b>[INVITE]</b> [REPONSE] votre invitation à rejoindre votre offre multicompte."),
            bouton("Gérer mon offre", "[LIEN_MULTICOMPTE]")])
mail(id="76-multicompte-detache", cat=S_COMPTE, marketing=False, quand="Quand le gestionnaire détache un compte de son offre (multiaccount_detached)" + INFO_SITE,
     objet="Votre compte ne fait plus partie de l'offre de [GESTIONNAIRE]", pre="Les services de cette offre ne sont plus accessibles. Votre compte reste ouvert.", sur="Offre multicompte", titre="Compte | détaché.",
     corps=[para("Bonjour [PSEUDO], <b>[GESTIONNAIRE]</b> a détaché votre compte de son offre multicompte. Les services de cette offre ne vous sont plus accessibles ; votre compte, lui, reste ouvert."),
            JEU_PLUS, INTEGRAL,
            bouton("Voir les formules", L("ABONNEMENTS"))])
mail(id="77-newsletter-inscription", cat=P_NEWS, marketing=False, quand="À l'inscription à la newsletter (newsletter_confirm)" + INFO_SITE,
     objet="Vous êtes inscrit à la newsletter Europe Échecs", pre="Les actualités des échecs à ne pas rater, chaque semaine.", sur="La newsletter", titre="Bienvenue | dans la newsletter !",
     corps=[para("Merci de votre inscription ! Vous recevrez la newsletter Europe Échecs <b>chaque semaine</b> : tournois, interviews, analyses et nouveautés du site."),
            bouton("Lire l'actualité", "https://www.europe-echecs.com")],
     sign="Bonne lecture,<br><b>La rédaction d'Europe Échecs</b>")
mail(id="78-newsletter-confirmer", cat=P_NEWS, marketing=False, quand="Pour mettre la liste de diffusion à jour : abonnés à la newsletter à reconfirmer (newsletter_consent_update_required_fr)" + INFO_SITE,
     objet="Newsletter Europe Échecs : confirmez votre inscription", pre="Un clic pour continuer à la recevoir. Sans réponse de votre part, vous ne la recevrez plus.", sur="La newsletter", titre="On continue | ensemble ?",
     corps=[para("Bonjour, vous recevez la newsletter Europe Échecs. Pour mettre notre liste à jour, confirmez que vous souhaitez continuer à la recevoir :"),
            bouton("Je continue à la recevoir", "[LIEN_CONFIRMER_NEWSLETTER]"),
            para(petit("Vous ne souhaitez plus la recevoir ? Ne faites rien."))],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")

# ---------- Jeu en différé ----------
mail(id="79-differe-coup-joue", cat=S_DIFFERE, marketing=False, quand="À chaque coup de l'adversaire dans une partie en différé (jeudiffcoupjoue)" + INFO_SITE,
     objet="[ADVERSAIRE] a joué : à vous !", pre="Votre partie commencée le [DATE_DEBUT] continue. Voyez la nouvelle position et jouez votre coup.", sur="Jeu en différé", titre="À vous | de jouer !",
     corps=[para("Bonjour [PSEUDO], <b>[ADVERSAIRE]</b> a joué un coup dans votre partie commencée le [DATE_DEBUT]."),
            '<a href="[LIEN_PARTIE]"><img src="[URL_IMAGE_POSITION]" width="300" alt="La nouvelle position" style="display:block;width:300px;max-width:100%;height:auto;border:0;border-radius:10px;margin:0 auto 18px"></a>',
            bouton("Jouer mon coup", "[LIEN_PARTIE]"), lignes_partie()])
mail(id="80-differe-partie-commencee", cat=S_DIFFERE, marketing=False, quand="Au début d'une partie en différé (jeudiffpartiedebut)" + INFO_SITE,
     objet="Partie en différé commencée contre [ADVERSAIRE]", pre="[BLANCS] contre [NOIRS], commencée le [DATE_DEBUT].", sur="Jeu en différé", titre="La partie | commence.",
     corps=[para("Bonjour [PSEUDO], une nouvelle partie en différé a commencé :"),
            infos([("Partie", "[BLANCS] – [NOIRS]"), ("Début", "[DATE_DEBUT]")]),
            bouton("Voir la partie", "[LIEN_PARTIE]")])
mail(id="81-differe-partie-terminee", cat=S_DIFFERE, marketing=False, quand="À la fin d'une partie en différé (jeudiffpartietermine)" + INFO_SITE,
     objet="Partie en différé terminée contre [ADVERSAIRE] : [RESULTAT]", pre="[BLANCS] – [NOIRS], [RESULTAT] ([RAISON_FIN]).", sur="Jeu en différé", titre="Partie | terminée.",
     corps=[para("Bonjour [PSEUDO], votre partie en différé est terminée :"),
            infos([("Partie", "[BLANCS] – [NOIRS]"), ("Résultat", "[RESULTAT] ([RAISON_FIN])"), ("Cadence", "[CADENCE]"), ("Début", "[DATE_DEBUT]")]),
            bouton("Revoir la partie", "[LIEN_PARTIE]"),
            para(petit('Partie de tournoi ? <a href="[LIEN_TOURNOI]" style="color:#6b6b66">Voir la fiche du tournoi</a>.'))])
mail(id="82-differe-invitation-tournoi", cat=S_DIFFERE, marketing=False, quand="Invitation à un tournoi privé en différé (jeudifftourninvit)" + INFO_SITE,
     objet="[ORGANISATEUR] vous invite à un tournoi en différé", pre="[CADENCE], [NB_JOUEURS_MAX] joueurs. Inscrivez-vous depuis la fiche du tournoi.", sur="Jeu en différé", titre="Une invitation | à un tournoi.",
     corps=[para("Bonjour [PSEUDO], <b>[ORGANISATEUR]</b> vous invite à son tournoi privé en différé :"),
            fiche_tournoi(), para("<b>Joueurs invités :</b> [LISTE_INVITES]"),
            bouton("M'inscrire au tournoi", "[LIEN_TOURNOI]")])
mail(id="83-differe-tournoi-commence", cat=S_DIFFERE, marketing=False, quand="Au démarrage d'un tournoi en différé (jeudifftourndebut)" + INFO_SITE,
     objet="Le tournoi en différé n° [ID_TOURNOI] commence", pre="Ses parties sont ajoutées à vos parties en cours.", sur="Jeu en différé", titre="Le tournoi | commence !",
     corps=[para("Bonjour [PSEUDO], le tournoi n° <b>[ID_TOURNOI]</b> auquel vous êtes inscrit démarre. Ses parties sont ajoutées à vos parties en cours."),
            fiche_tournoi(), para("<b>Participants :</b> [LISTE_PARTICIPANTS]"),
            bouton("Voir le tournoi", "[LIEN_TOURNOI]")])
mail(id="84-differe-tournoi-termine", cat=S_DIFFERE, marketing=False, quand="À la fin d'un tournoi en différé (jeudifftournfin)" + INFO_SITE,
     objet="Le tournoi en différé n° [ID_TOURNOI] est terminé", pre="Appariements, scores et parties : tout est sur la fiche du tournoi.", sur="Jeu en différé", titre="Tournoi | terminé.",
     corps=[para("Bonjour [PSEUDO], le tournoi n° <b>[ID_TOURNOI]</b> vient de se terminer. Appariements, scores et parties sont sur sa fiche."),
            fiche_tournoi(),
            bouton("Voir les résultats", "[LIEN_TOURNOI]")])
mail(id="85-differe-tournoi-annule", cat=S_DIFFERE, marketing=False, quand="Quand un tournoi en différé est annulé faute de participants (jeudifftournannul)" + INFO_SITE,
     objet="Le tournoi en différé n° [ID_TOURNOI] est annulé", pre="Il n'a pas réuni assez de participants. D'autres tournois vous attendent.", sur="Jeu en différé", titre="Tournoi | annulé.",
     corps=[para("Bonjour [PSEUDO], le tournoi n° <b>[ID_TOURNOI]</b> auquel vous étiez inscrit est annulé : il n'a pas réuni assez de participants."),
            fiche_tournoi(),
            bouton("Voir les autres tournois", "[LIEN_TOURNOIS_DIFFERE]")])

# ---------- Tournois en direct ----------
mail(id="86-tournoi-invitation", cat=S_TOURNOIS, marketing=False, quand="Invitation à un tournoi en direct (tourn_invitation)" + INFO_SITE,
     objet="[ORGANISATEUR] vous invite à son tournoi", pre="Découvrez le programme et donnez votre réponse en un clic.", sur="Tournoi", titre="Vous êtes | invité !",
     corps=[para("Bonjour [PSEUDO], <b>[ORGANISATEUR]</b> organise un tournoi et vous y invite. Découvrez le programme et donnez votre réponse :"),
            bouton("Voir l'invitation", "[LIEN_INVITATION_TOURNOI]")])
mail(id="87-tournoi-en-ligne", cat=S_TOURNOIS, marketing=False, quand="Quand un tournoi est mis en ligne : aux participants ; variante organisateur dans le guide (tourn_created)" + INFO_SITE,
     objet="Tournoi [NOM_TOURNOI] : votre participation est enregistrée", pre="Début le [DATE_DEBUT_TOURNOI]. Toutes les infos sont sur la fiche du tournoi.", sur="Tournoi", titre="Vous êtes | inscrit !",
     corps=[para("Bonjour [PSEUDO], le tournoi <b>[NOM_TOURNOI]</b>, organisé par [ORGANISATEUR], est en ligne. Votre participation est enregistrée."),
            infos([("Début", "[DATE_DEBUT_TOURNOI]")]), bouton("Voir le tournoi", "[LIEN_TOURNOI]"), para(GMT)])
mail(id="88-tournoi-demarre-bientot", cat=S_TOURNOIS, marketing=False, quand="Avant le début d'un tournoi (tourn_start)" + INFO_SITE,
     objet="Tournoi [NOM_TOURNOI] : début le [DATE_DEBUT_TOURNOI]", pre="Connectez-vous quelques minutes avant pour être prêt.", sur="Tournoi", titre="Le tournoi | approche.",
     corps=[billet("[NOM_TOURNOI]", [("Début", "[HEURE_DEBUT]"), ("Organisateur", "[ORGANISATEUR]")], jour="[JJ]", mois="[MOIS_COURT]"),
            bouton("Voir le tournoi", "[LIEN_TOURNOI]"), para(GMT)])
mail(id="89-tournoi-nouvelle-ronde", cat=S_TOURNOIS, marketing=False, quand="Au début de chaque ronde (tourn_startround)" + INFO_SITE,
     objet="Tournoi [NOM_TOURNOI] : la ronde [RONDE] commence", pre="Elle dure jusqu'au [DATE_FIN_RONDE]. Votre appariement et votre horaire sont sur la fiche.", sur="Tournoi · ronde [RONDE]", titre="Ronde [RONDE] : | c'est parti !",
     corps=[para("Bonjour [PSEUDO], la ronde <b>[RONDE]</b> du tournoi [NOM_TOURNOI] a commencé. Elle dure jusqu'au <b>[DATE_FIN_RONDE]</b>."),
            para("Votre appariement et votre horaire de jeu sont sur la fiche du tournoi. Pour les rondes de plus de 3 heures, vous pouvez y proposer un autre horaire."),
            bouton("Voir mon appariement", "[LIEN_TOURNOI]"), para(GMT)])
mail(id="90-tournoi-rappel-partie", cat=S_TOURNOIS, marketing=False, quand="Rappel avant une partie de tournoi (tourn_match_reminder)" + INFO_SITE,
     objet="Rappel : votre partie de la ronde [RONDE], le [DATE_PARTIE]", pre="Connectez-vous 5 à 10 minutes avant, par sécurité.", sur="Tournoi · ronde [RONDE]", titre="Votre partie | approche.",
     corps=[billet("Ronde [RONDE] · [NOM_TOURNOI]", [("Heure", "[HEURE_PARTIE]"), ("Où", "sur la zone de jeu, connecté à votre compte")], jour="[JJ]", mois="[MOIS_COURT]"),
            para("Par sécurité, connectez-vous 5 à 10 minutes avant le début."),
            bouton("Aller sur la zone de jeu", L("ZONE_DE_JEU")), para(GMT)])
mail(id="91-tournoi-horaire-propose", cat=S_TOURNOIS, marketing=False, quand="Quand l'adversaire propose un autre horaire (tourn_proposreceived)" + INFO_SITE,
     objet="Ronde [RONDE] : votre adversaire propose un autre horaire", pre="Acceptez, refusez ou proposez un autre horaire depuis la fiche du tournoi.", sur="Tournoi · ronde [RONDE]", titre="Un autre | horaire ?",
     corps=[para("Bonjour [PSEUDO], votre adversaire souhaite changer l'horaire de votre partie de la ronde [RONDE]. Vous pouvez accepter, refuser ou proposer un autre horaire."),
            bouton("Répondre", "[LIEN_TOURNOI]"), para(GMT)])
mail(id="92-tournoi-horaire-reponse", cat=S_TOURNOIS, marketing=False, quand="Réponse de l'adversaire à une proposition d'horaire : acceptée, refusée ou retirée (tourn_proposaccepted, tourn_proposdenied, tourn_proposdeleted). [REPONSE_HORAIRE] selon le cas" + INFO_SITE,
     objet="Ronde [RONDE] : horaire [REPONSE_HORAIRE_COURTE]", pre="[REPONSE_HORAIRE]", sur="Tournoi · ronde [RONDE]", titre="Horaire | [REPONSE_HORAIRE_COURTE].",
     corps=[para("Bonjour [PSEUDO], [REPONSE_HORAIRE]"),
            bouton("Voir la fiche du tournoi", "[LIEN_TOURNOI]"), para(GMT)])
mail(id="93-tournoi-partie-reprogrammee", cat=S_TOURNOIS, marketing=False, quand="Quand une partie est reprogrammée pour raison technique (tourn_match_reprog)" + INFO_SITE,
     objet="Ronde [RONDE] : votre partie est reprogrammée", pre="Nouvel horaire : [NOUVEL_HORAIRE] au lieu de [ANCIEN_HORAIRE].", sur="Tournoi · ronde [RONDE]", titre="Partie | reprogrammée.",
     corps=[para("Bonjour [PSEUDO], pour une raison technique, votre partie a été reprogrammée :"),
            infos([("Prévue le", "[ANCIEN_HORAIRE]"), ("Nouvel horaire", "[NOUVEL_HORAIRE]")]),
            para("Pour les rondes de plus de 3 heures, vous pouvez proposer un autre horaire depuis la fiche du tournoi."),
            bouton("Voir la fiche du tournoi", "[LIEN_TOURNOI]"), para(GMT)],
     sign="Avec nos excuses,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="94-tournoi-ronde-retardee", cat=S_TOURNOIS, marketing=False, quand="Quand une ronde démarre ou finit en retard (tourn_round_shifted, tourn_roundend_updat)" + INFO_SITE,
     objet="Ronde [RONDE] : nouvel horaire de fin", pre="La ronde se termine le [NOUVELLE_FIN] au lieu du [FIN_PREVUE].", sur="Tournoi · ronde [RONDE]", titre="La ronde [RONDE] | est décalée.",
     corps=[para("Bonjour [PSEUDO], la ronde <b>[RONDE]</b> est décalée ([RAISON_RETARD])."),
            infos([("Fin prévue", "[FIN_PREVUE]"), ("Nouvelle fin", "[NOUVELLE_FIN]")]),
            bouton("Voir la fiche du tournoi", "[LIEN_TOURNOI]"), para(GMT)],
     sign="Avec nos excuses,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="95-tournoi-appariement-manuel", cat=S_TOURNOIS, marketing=False, quand="À l'organisateur, quand l'appariement automatique est impossible (tourn_round_manualpairingrequired)" + INFO_SITE,
     objet="Ronde [RONDE] : appariement manuel nécessaire", pre="Les règles d'appariement ne peuvent pas être respectées automatiquement. Votre intervention est nécessaire.", sur="Votre tournoi", titre="Appariement | à faire.",
     corps=[para("Bonjour [PSEUDO], l'appariement automatique de la ronde <b>[RONDE]</b> de votre tournoi n'a pas pu être fait : les règles d'appariement ne peuvent pas être respectées dans la situation actuelle. Pour que le tournoi continue, faites l'appariement vous-même :"),
            bouton("Apparier la ronde [RONDE]", "[LIEN_TOURNOI]")])
mail(id="96-tournoi-termine", cat=S_TOURNOIS, marketing=False, quand="À la fin d'un tournoi en direct (tourn_end)" + INFO_SITE,
     objet="Tournoi [NOM_TOURNOI] : les résultats", pre="Classement, parties et résultats : tout est sur la fiche du tournoi.", sur="Tournoi", titre="Tournoi | terminé !",
     corps=[para("Bonjour [PSEUDO], le tournoi <b>[NOM_TOURNOI]</b>, organisé par [ORGANISATEUR], est terminé. Merci d'y avoir participé !"),
            bouton("Voir les résultats", "[LIEN_TOURNOI]")])
mail(id="97-tournoi-instructions", cat=S_TOURNOIS, marketing=False, quand="Quelques heures avant un événement-tournoi d'Europe Échecs (tourn_instructions)" + INFO_SITE,
     objet="[NOM_EVENEMENT] : les instructions", pre="Le [DATE_EVENEMENT], heure de Paris. Tout ce qu'il faut savoir pour bien jouer.", sur="Tournoi · instructions", titre="Prêt pour | le tournoi ?",
     corps=[billet("[NOM_EVENEMENT]", [("Heure", "[HEURE_EVENEMENT], heure de Paris"), ("Où", "la zone de jeu Europe Échecs")], jour="[JJ]", mois="[MOIS_COURT]"),
            para("Connectez-vous un peu avant pour vous familiariser avec la zone de jeu."),
            etapes([("Suivre le tournoi", "L'heure, la cadence et les rondes s'affichent sur la zone de jeu. À gauche, un compte à rebours annonce chaque ronde ; « l'œil » du tournoi donne les résultats, le classement et les parties en cours."),
                    ("Entre deux rondes", "Une partie « hors tournoi » peut être interrompue au début de la ronde suivante : vous seriez déclaré perdant. Gardez un œil sur les notifications."),
                    ("En cas de doute", "À la fin d'une partie, le point d'exclamation au coin de l'échiquier demande une vérification. Une triche avérée corrige résultat et classement en temps réel."),
                    ("Un problème ?", "Écrivez au joueur « EuropeEchecs » : œil du tournoi, pseudo de l'organisateur, puis « Parler »."),
                    ("Réglages utiles", "La roue crantée près de votre pseudo : échiquier, pièces, « Premove », vitesse d'animation (« Aucune » est la plus rapide), promotion automatique en Dame, tchat.")]),
            encadre("<b>Le premove :</b> jouez votre prochain coup à l'avance, pendant que l'adversaire réfléchit. Il part dès son coup, s'il est toujours légal, sans consommer votre temps. Jusqu'à 3 coups à l'avance ; clic droit pour annuler. Pratique quand le coup adverse est forcé, risqué s'il est inattendu."),
            bouton("Aller sur la zone de jeu", L("ZONE_DE_JEU"))],
     sign="Bon tournoi à toutes et à tous !<br><b>L'équipe d'Europe Échecs</b>")

# ---------- Événements, cours et masterclasses ----------
mail(id="98-evenement-en-attente", cat=S_EVENEMENTS, marketing=False, quand="Inscription à un événement en attente de validation (event_waiting)" + INFO_SITE,
     objet="[NOM_EVENEMENT] : inscription reçue", pre="Vous recevrez un e-mail dès sa validation par les organisateurs.", sur="Votre inscription", titre="Inscription | reçue !",
     corps=[para("Bonjour [PSEUDO], merci pour votre inscription à <b>[NOM_EVENEMENT]</b>. Vous recevrez un e-mail dès qu'elle sera validée par les organisateurs ; s'il nous manque une information, nous vous contacterons."),
            para("En attendant, découvrez la zone de jeu, si vous ne la connaissez pas encore :"),
            bouton("Découvrir la zone de jeu", L("ZONE_DE_JEU"))])
mail(id="99-evenement-valide", cat=S_EVENEMENTS, marketing=False, quand="Inscription à un événement validée (event_confirm)" + INFO_SITE,
     objet="[NOM_EVENEMENT] : votre inscription est validée", pre="Vous recevrez les instructions du tournoi quelques heures avant l'événement.", sur="Votre inscription", titre="C'est validé, | à bientôt !",
     corps=[para("Bonjour [PSEUDO], votre inscription à <b>[NOM_EVENEMENT]</b> est confirmée."),
            encadre("<b>Important :</b> quelques heures avant l'événement, vous recevrez un e-mail avec les instructions du tournoi."),
            para("D'ici là, découvrez la zone de jeu si vous ne la connaissez pas encore :"),
            bouton("Découvrir la zone de jeu", L("ZONE_DE_JEU"))],
     sign="À très bientôt !<br><b>L'équipe d'Europe Échecs</b>")
mail(id="100-evenement-refuse", cat=S_EVENEMENTS, marketing=False, quand="Inscription à un événement refusée (event_reject)" + INFO_SITE,
     objet="[NOM_EVENEMENT] : votre inscription n'a pas pu être validée", pre="Contactez-nous pour en savoir plus.", sur="Votre inscription", titre="Inscription | non validée.",
     corps=[para("Bonjour [PSEUDO], nous n'avons malheureusement pas pu valider votre inscription à <b>[NOM_EVENEMENT]</b>. Contactez-nous pour en savoir plus :"),
            bouton("Contacter l'équipe", "[LIEN_AIDE]")])
mail(id="101-cours-inscription", cat=S_EVENEMENTS, marketing=False, quand="Inscription à un cours ou un stage (course_confirmation)" + INFO_SITE,
     objet="Inscription confirmée : [NOM_COURS]", pre="Votre réservation est confirmée. Nous revenons vers vous très vite avec les détails pratiques.", sur="Votre inscription", titre="Inscription | confirmée !",
     corps=[para("Bonjour [PSEUDO], merci pour votre inscription à <b>[NOM_COURS]</b>[AVEC_ANIMATEUR] ! Votre réservation est confirmée, et nous revenons vers vous très vite avec les détails pratiques."),
            para(petit('Une question ? <a href="[LIEN_AIDE]" style="color:#6b6b66">Contactez-nous</a>.'))],
     sign="Merci de votre confiance, et à bientôt !<br><b>L'équipe d'Europe Échecs</b>")
mail(id="102-masterclass-inscription", cat=S_EVENEMENTS, marketing=False, quand="Inscription à une masterclass (masterclass_confirm)" + INFO_SITE,
     objet="Masterclass « [TITRE_MASTERCLASS] » : vous êtes inscrit", pre="Retrouvez la page de la masterclass pour la date et le lien.", sur="Masterclass", titre="Vous êtes | inscrit !",
     corps=[para("Bonjour [PSEUDO], votre inscription à la masterclass <b>« [TITRE_MASTERCLASS] »</b> est confirmée."),
            bouton("Voir la masterclass", "[LIEN_MASTERCLASS]")])
mail(id="103-masterclass-invitation", cat=S_EVENEMENTS, marketing=False, quand="Invitation gratuite à une masterclass, avec un code (masterclass_invit)" + INFO_SITE,
     objet="Votre invitation à la masterclass « [TITRE_MASTERCLASS] »", pre="Votre place est offerte : 3 étapes pour l'activer avec votre code.", sur="Masterclass", titre="Votre place | est offerte.",
     corps=[para("Bonjour [PSEUDO], vous êtes invité à la masterclass <b>« [TITRE_MASTERCLASS] »</b>. Pour activer votre place :"),
            etapes([("Ouvrez la page de la masterclass", "Cliquez sur « S'inscrire à cette Masterclass » : elle s'ajoute à votre panier."),
                    ("Saisissez votre code", "Dans « Vous disposez d'une réduction ? », entrez <b>[CODE_INVITATION]</b> : la masterclass devient gratuite."),
                    ("Terminez la commande", "Vous recevrez un e-mail de confirmation.")]),
            bouton("Activer ma place", "[LIEN_MASTERCLASS]")])

# ---------- Fair-play (8 modèles du site regroupés en 3) ----------
mail(id="104-fairplay-suite-signalement", cat=S_FAIRPLAY, marketing=False, quand="À l'auteur d'un signalement, une fois le dossier examiné. [CONCLUSION] selon le cas : infraction confirmée, non confirmée, doute, ou message de l'équipe (les 5 modèles fairplaycase_*_to_reporter)" + INFO_SITE,
     objet="Votre signalement de [SUSPECT] a été examiné", pre="Merci de votre vigilance. Voici notre conclusion.", sur="Fair-play", titre="Merci | de votre vigilance.",
     corps=[para("Bonjour [PSEUDO], merci de nous avoir signalé une possible violation des règles du fair-play par <b>[SUSPECT]</b>. Votre vigilance aide à garder la zone de jeu juste pour tous."),
            encadre("[CONCLUSION]"),
            '<!-- ACTIONS : seulement si des actions ont été prises -->' + liste(["[ACTION_1]", "[ACTION_2]"]),
            bouton("Voir le dossier", "[LIEN_DOSSIER]")],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="105-fairplay-adversaire", cat=S_FAIRPLAY, marketing=False, quand="Aux adversaires d'un joueur sanctionné ou en doute (les 3 modèles fairplaycase_*_to_third_party_player)" + INFO_SITE,
     objet="Fair-play : une décision concerne un de vos adversaires", pre="[SUSPECT] : [CONSTAT]. Vos parties et votre Elo ont pu être corrigés.", sur="Fair-play", titre="Une décision | sur un adversaire.",
     corps=[para("Bonjour [PSEUDO], pour que chaque partie soit équitable, nous contrôlons le respect du fair-play. <b>[SUSPECT]</b>, un de vos adversaires, est concerné : [CONSTAT]."),
            '<!-- ACTIONS : seulement si des actions ont été prises -->' + liste(["[ACTION_1]", "[ACTION_2]"]),
            bouton("Voir le détail", "[LIEN_DOSSIER]")],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="106-fairplay-avertissement", cat=S_FAIRPLAY, marketing=False, quand="Au joueur concerné par une infraction (fairplaycase_violation_to_suspect)" + INFO_SITE,
     objet="Fair-play : à propos de votre compte", pre="Une activité récente pose question. Consultez la page de votre dossier.", sur="Fair-play", titre="À propos | de votre compte.",
     corps=[para("Bonjour [PSEUDO], des activités récentes sur votre compte posent question quant au respect des règles du fair-play. Pour la communauté comme pour nous, l'équité de la zone de jeu est essentielle."),
            para("La situation et les éventuelles restrictions appliquées à votre compte sont détaillées ici. Merci d'en prendre connaissance :"),
            bouton("Voir mon dossier", "[LIEN_DOSSIER]")],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="107-probleme-traite", cat=S_FAIRPLAY, marketing=False, quand="Après le traitement d'un problème sur une ou plusieurs parties (problem_solved et problem_solved_user, identiques)" + INFO_SITE,
     objet="Un problème sur vos parties a été traité", pre="[PROBLEME] : voici la solution adoptée.", sur="Vos parties", titre="Problème | traité.",
     corps=[para("Bonjour [PSEUDO], nous avons traité un problème concernant les parties suivantes :"),
            '<!-- PARTIE : une ligne par partie -->' + infos([("[BLANCS_1] – [NOIRS_1]", "[DATE_PARTIE_1]")]),
            infos([("Problème", "[PROBLEME]"), ("Solution adoptée", "[SOLUTION]")]),
            para(petit('Une question ? <a href="[LIEN_AIDE]" style="color:#6b6b66">Contactez-nous</a>.'))])

# ---------- Communauté ----------
mail(id="108-message-d-un-joueur", cat=S_COMMU, marketing=False, quand="Quand un joueur écrit à un autre depuis le site (contactjoueursmsg)" + INFO_SITE,
     objet="[EXPEDITEUR_PSEUDO] vous a envoyé un message", pre="« [DEBUT_MESSAGE] »", sur="Un message", titre="Un message | de [EXPEDITEUR_PSEUDO].",
     corps=[para("Bonjour, <b>[EXPEDITEUR_PSEUDO]</b> vous a écrit depuis Europe Échecs :"),
            encadre("[MESSAGE]"),
            para(petit("Pour lui répondre, répondez simplement à cet e-mail."))])
mail(id="109-commentaire-non-valide", cat=S_COMMU, marketing=False, quand="Quand un commentaire d'article n'est pas validé (refuscommentaire)" + INFO_SITE,
     objet="Votre commentaire n'a pas été publié", pre="Sur l'article « [TITRE_ARTICLE] ». La charte de publication est en bas de chaque article.", sur="Vos commentaires", titre="Commentaire | non publié.",
     corps=[para("Bonjour, votre commentaire n'a pas été publié."),
            infos([("Article", "[TITRE_ARTICLE]"), ("Raison", "[RAISON_REFUS]")]),
            encadre("[COMMENTAIRE]"),
            para(petit("La charte de publication des commentaires est en bas de chaque article."))])
mail(id="110-battle-commence", cat=S_COMMU, marketing=False, quand="Au début d'une battle de puzzles (puzzlesbattledebut)" + INFO_SITE,
     objet="Battle de puzzles n° [ID_BATTLE] : c'est parti !", pre="[JOUEUR_1] contre [JOUEUR_2]. À vous de jouer !", sur="Battle de puzzles", titre="La battle | commence !",
     corps=[para("Bonjour [PSEUDO], la battle de puzzles n° <b>[ID_BATTLE]</b> a commencé :"),
            infos([("Joueurs", "[JOUEUR_1] – [JOUEUR_2]")]),
            bouton("Jouer", "[LIEN_BATTLE]")])
mail(id="111-battle-terminee", cat=S_COMMU, marketing=False, quand="À la fin d'une battle de puzzles (puzzlesbattlefin)" + INFO_SITE,
     objet="Battle de puzzles n° [ID_BATTLE] : le résultat", pre="[JOUEUR_1] contre [JOUEUR_2] : découvrez qui l'emporte.", sur="Battle de puzzles", titre="Battle | terminée.",
     corps=[para("Bonjour [PSEUDO], la battle de puzzles n° <b>[ID_BATTLE]</b> est terminée :"),
            infos([("Joueurs", "[JOUEUR_1] – [JOUEUR_2]")]),
            bouton("Voir le résultat", "[LIEN_BATTLE]")])

# ---------- Support ----------
mail(id="112-support-demande-recue", cat=S_SUPPORT, marketing=False, quand="À l'enregistrement d'une demande de support (supportdemenreg)" + INFO_SITE,
     objet="Votre demande est bien enregistrée", pre="Nous vous écrivons à chaque étape. Suivez-la et répondez depuis le lien.", sur="Support", titre="Demande | bien reçue.",
     corps=[para("Bonjour, votre demande a été transmise au service concerné. Nous vous écrirons à chaque étape de son traitement."),
            infos([("Date", "[DATE_DEMANDE]"), ("Objet", "[OBJET_DEMANDE]"), ("Votre message", "[EXPLICATION]")]),
            bouton("Suivre ma demande", "[LIEN_DEMANDE]")])
mail(id="113-support-reponse", cat=S_SUPPORT, marketing=False, quand="Quand le support a répondu (supportdemchgetat)" + INFO_SITE,
     objet="Réponse à votre demande : [OBJET_DEMANDE]", pre="Notre équipe a examiné votre demande. Lisez la réponse et poursuivez l'échange.", sur="Support", titre="Nous vous | avons répondu.",
     corps=[para("Bonjour, notre équipe a examiné votre demande. Sa réponse vous attend :"),
            bouton("Lire la réponse", "[LIEN_DEMANDE]"),
            infos([("Date", "[DATE_DEMANDE]"), ("Objet", "[OBJET_DEMANDE]"), ("Votre message", "[EXPLICATION]")])])
mail(id="114-message-de-l-equipe", cat=S_SUPPORT, marketing=False, quand="Message libre d'un administrateur (support_mail_direct ; mail_direct a le même usage)" + INFO_SITE,
     objet="[TITRE_MESSAGE]", pre="Un message de l'équipe d'Europe Échecs.", sur="Un message de l'équipe", titre="[TITRE_MESSAGE]",
     corps=[para("[CONTENU_MESSAGE]"),
            para(petit('Pour nous répondre, utilisez <a href="[LIEN_AIDE]" style="color:#6b6b66">le formulaire de contact</a> : les réponses à cet e-mail ne nous parviennent pas.'))])

# ---------- PrediChess ----------
mail(id="115-predichess-premier", cat=S_PREDI, marketing=False, quand="Au 1er du classement PrediChess d'un événement (predichess_prize_first)" + INFO_SITE,
     objet="PrediChess [EVENEMENT] : vous avez gagné !", pre="1re place : un sweat Europe Échecs vous attend. Il nous faut votre adresse, votre taille et votre couleur.", sur="PrediChess · [EVENEMENT]", titre="Félicitations, | [PSEUDO] !",
     corps=[para("Bravo [PSEUDO] : vous terminez <b>1<sup>er</sup></b> du classement PrediChess de [EVENEMENT], et vous gagnez <b>un sweat Europe Échecs</b> !"),
            para("Pour vous l'envoyer, il nous faut votre adresse postale, la couleur et la taille de votre choix :"),
            bouton("Envoyer mes informations", "[LIEN_AIDE]"),
            para(petit('Merci de ne pas répondre à cet e-mail : utilisez le formulaire de contact. <a href="https://boutique.echecs.com/25-sweats" style="color:#6b6b66">Voir les modèles</a>.'))],
     sign="Merci d'avoir joué, et profitez bien de votre cadeau !<br><b>L'équipe d'Europe Échecs</b>")
mail(id="116-predichess-classement", cat=S_PREDI, marketing=False, quand="Aux joueurs du top 4 (3 mois) et du top 20 (1 mois) PrediChess (predichess_prize_top4, predichess_prize_top20)" + INFO_SITE,
     objet="PrediChess [EVENEMENT] : vous êtes dans le top [RANG] !", pre="Vous gagnez [DUREE_OFFERTE] de Pack Intégral. Activez-le avec votre code cadeau.", sur="PrediChess · [EVENEMENT]", titre="Top [RANG], | bravo !",
     corps=[para("Bravo [PSEUDO] ! Grâce à votre classement au PrediChess de [EVENEMENT], vous gagnez <b>[DUREE_OFFERTE] de Pack Intégral</b> :"),
            liste(["<b>Des centaines de vidéos</b>, en streaming", "<b>Toutes nos leçons</b> pour progresser", "<b>La zone de jeu complète</b>, entraînement tactique compris", "<b>La revue Europe Échecs</b>, à lire en ligne"]),
            infos([("Votre code", "[CODE_CADEAU]")]),
            bouton("Activer mon Pack Intégral", "https://www.europe-echecs.com/activation"),
            para(petit("Une question ? Utilisez le formulaire de contact, plutôt que de répondre à cet e-mail."))],
     sign="Merci d'avoir joué, et profitez bien de votre abonnement !<br><b>L'équipe d'Europe Échecs</b>")

# ---------- Parrainage ----------
mail(id="117-parrainage-invitation", cat=S_PARRAIN, quand="Invitation envoyée par un parrain à un ami, puis rappel (sponsorship_invitation et sponsorship_remind_invitation, identiques)" + INFO_SITE,
     pourquoi="Vous recevez cet e-mail car [EMAIL_PARRAIN] vous a invité sur europe-echecs.com.",
     objet="[PRENOM_OU_EMAIL_PARRAIN] vous invite à jouer aux échecs", pre="Créez votre compte gratuit et défiez des joueurs du monde entier. Votre période d'essai est doublée.", sur="Invitation", titre="Une partie | d'échecs ?",
     corps=[para("Bonjour, <b>[EMAIL_PARRAIN]</b> vous invite à découvrir la zone de jeu d'Europe Échecs : défiez des joueurs du monde entier et progressez."),
            liste(["[AVANTAGE_1]", "[AVANTAGE_2]", "[AVANTAGE_3]"]),
            encadre("<b>Invité par un ami, votre période d'essai est doublée.</b> Et en jouant au moins [NB_PARTIES_PARRAINAGE] parties, vous offrez un bonus à votre parrain."),
            bouton("Créer mon compte gratuit", "[LIEN_INSCRIPTION]"),
            para(petit('Jouez aussi sur mobile : <a href="[LIEN_APP_IOS]" style="color:#6b6b66">iPhone</a> · <a href="[LIEN_APP_ANDROID]" style="color:#6b6b66">Android</a>.'))],
     sign="Soyez le bienvenu !<br><b>L'équipe d'Europe Échecs</b>")
mail(id="118-parrainage-ami-inscrit", cat=S_PARRAIN, marketing=False, quand="Au parrain, quand un ami invité crée son compte (sponsorship_create_account)" + INFO_SITE,
     objet="Votre ami a créé son compte", pre="Encore [NB_PARTIES_PARRAINAGE] parties jouées par lui, et votre parrainage est validé.", sur="Parrainage", titre="Votre ami | vous a rejoint !",
     corps=[para("Bonne nouvelle : votre ami <b>[EMAIL_FILLEUL]</b> a créé son compte. Pour que votre parrainage soit validé, il doit jouer au moins [NB_PARTIES_PARRAINAGE] parties. Encouragez-le !"),
            bouton("Mes parrainages", "[LIEN_PARRAINAGES]")])
mail(id="119-parrainage-valide", cat=S_PARRAIN, marketing=False, quand="Au parrain, quand un parrainage est validé ; avec bonus débloqué si un palier est atteint (sponsorship_activate_account et _level_up)" + INFO_SITE,
     objet="Parrainage validé : merci !", pre="Le parrainage de [EMAIL_FILLEUL] est validé. [ETAT_BONUS]", sur="Parrainage", titre="Parrainage | validé !",
     corps=[para("Félicitations : le parrainage de <b>[EMAIL_FILLEUL]</b> est validé."),
            encadre("[ETAT_BONUS]"),
            bouton("Inviter un autre ami", "[LIEN_PARRAINAGES]")])
mail(id="120-parrainage-ami-abonne", cat=S_PARRAIN, marketing=False, quand="Au parrain, quand un filleul s'abonne ; avec bonus si un palier est atteint (sponsorship_activate_subscription et _level_up)" + INFO_SITE,
     objet="Votre ami s'est abonné !", pre="[EMAIL_FILLEUL] vient de s'abonner. [ETAT_BONUS]", sur="Parrainage", titre="Votre ami | s'est abonné !",
     corps=[para("Félicitations : votre ami <b>[EMAIL_FILLEUL]</b> vient de s'abonner."),
            encadre("[ETAT_BONUS]"),
            bouton("Mes parrainages", "[LIEN_PARRAINAGES]")])
mail(id="121-parrainage-relancez", cat=S_PARRAIN, quand="Au parrain dont des invités n'ont pas activé leur compte (sponsorship_remind_sponsor_activation)" + INFO_SITE,
     objet="Vos amis n'ont pas encore activé leur compte", pre="Relancez-les : chaque parrainage validé prolonge votre abonnement.", sur="Parrainage", titre="Un petit | rappel ?",
     corps=[para("Certains des amis que vous avez invités n'ont pas encore activé leur compte. Relancez-les : chaque parrainage validé vous rapproche d'un bonus."),
            bouton("Relancer mes amis", "[LIEN_PARRAINAGES]")])
mail(id="122-parrainage-adresse-erreur", cat=S_PARRAIN, marketing=False, quand="Quand l'invitation n'a pas pu être envoyée (sponsorship_email_error)" + INFO_SITE,
     objet="Votre invitation n'a pas pu être envoyée à [EMAIL_FILLEUL]", pre="Vérifiez l'adresse dans « Mes parrainages » et corrigez-la si besoin.", sur="Parrainage", titre="Adresse | à vérifier.",
     corps=[para("Nous n'avons pas pu envoyer votre invitation à <b>[EMAIL_FILLEUL]</b>. Vérifiez l'adresse dans vos parrainages et corrigez-la si besoin :"),
            bouton("Vérifier l'adresse", "[LIEN_PARRAINAGES]")])

EXEMPLES.update({"ADVERSAIRE": "TourDeFrance", "BLANCS": "LéaDame", "NOIRS": "TourDeFrance", "DATE_DEBUT": "18/11/2026",
    "URL_IMAGE_POSITION": "img/probleme-exemple.jpg", "RESULTAT": "1-0", "RAISON_FIN": "abandon", "CADENCE": "1 coup en 3 jours",
    "ORGANISATEUR": "ClubEchecs75", "NOM_TOURNOI": "Open d'automne", "RONDE": "3", "ID_TOURNOI": "4521", "TYPE_JEU": "Standard", "TYPE_MATCHS": "Aller simple",
    "ELO_MIN": "1400", "ELO_MAX": "1800", "NB_JOUEURS_MAX": "8", "NOM_EVENEMENT": "Championnat en ligne des clubs", "SUSPECT": "JoueurX", "EXPEDITEUR_PSEUDO": "TourDeFrance",
    "TITRE_MASTERCLASS": "Les plans du milieu de partie", "EVENEMENT": "Championnat du monde 2026", "RANG": "20", "DUREE_OFFERTE": "1 mois",
    "EMAIL_PARRAIN": "lea@exemple.fr", "PRENOM_OU_EMAIL_PARRAIN": "Léa", "EMAIL_FILLEUL": "paul@exemple.fr", "FOURNISSEUR": "Google", "LIMITE": "tchat désactivé",
    "INVITE": "PaulCavalier", "REPONSE": "a accepté", "ID_BATTLE": "812", "JOUEUR_1": "LéaDame", "JOUEUR_2": "PaulCavalier", "NOM_COURS": "Stage d'hiver",
    "REPONSE_HORAIRE_COURTE": "accepté", "OBJET_DEMANDE": "Problème de connexion", "TITRE_MESSAGE": "Maintenance de la zone de jeu"})
for _k in ("DATE_ANNULATION", "DATE_DEMANDE", "DUREE_LIMITE", "JOURS_VALIDITE", "DATE_DEBUT_TOURNOI", "HEURE_DEBUT",
           "DATE_FIN_RONDE", "DATE_PARTIE", "HEURE_PARTIE", "REPONSE_HORAIRE", "ANCIEN_HORAIRE", "NOUVEL_HORAIRE", "RAISON_RETARD", "FIN_PREVUE", "NOUVELLE_FIN",
           "DATE_EVENEMENT", "HEURE_EVENEMENT", "AVEC_ANIMATEUR", "CODE_INVITATION", "CONCLUSION", "CONSTAT", "ACTION_1", "ACTION_2", "PROBLEME", "SOLUTION",
           "BLANCS_1", "NOIRS_1", "DATE_PARTIE_1", "MESSAGE", "DEBUT_MESSAGE", "TITRE_ARTICLE", "RAISON_REFUS", "COMMENTAIRE", "EXPLICATION", "CONTENU_MESSAGE",
           "AVANTAGE_1", "AVANTAGE_2", "AVANTAGE_3", "NB_PARTIES_PARRAINAGE", "ETAT_BONUS", "LISTE_INVITES", "LISTE_PARTICIPANTS", "PSEUDO_1", "PSEUDO_2", "LISTE_COUPS"):
    EXEMPLES[_k] = "[" + _k + "]"
EXEMPLES["JJ"] = "12"
LOGO_SITE = {S_COMPTE: "logo-blanc", S_DIFFERE: "logo-jaune", S_TOURNOIS: "logo", S_EVENEMENTS: "logo-jaune", S_FAIRPLAY: "logo-blanc", S_COMMU: "logo", S_SUPPORT: "logo-blanc", S_PREDI: "logo-jaune", S_PARRAIN: "logo-jaune"}
PIECE_SITE = {S_COMPTE: "K", S_DIFFERE: "N", S_TOURNOIS: "R", S_EVENEMENTS: "B", S_FAIRPLAY: "K", S_COMMU: "P", S_SUPPORT: "Q", S_PREDI: "B", S_PARRAIN: "P"}
