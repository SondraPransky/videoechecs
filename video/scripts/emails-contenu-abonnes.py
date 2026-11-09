# Contenu des e-mails des abonnés de l'Académie echecs.com (exécuté par scripts/emails.py, qui fournit les composants)
OFFRE = "<b>14,90&nbsp;€/mois</b> au lieu de 19,90&nbsp;€, ou <b>150&nbsp;€/an</b> au lieu de 179,90&nbsp;€"

# ---------- 1. Compte ----------
mail(id="01-confirmation-adresse", cat="Compte", marketing=False, quand="À la création du compte (transactionnel)",
     objet="Confirme ton adresse e-mail", pre="Un clic, et ton compte echecs.com est prêt.", sur="Ton compte", titre="Plus qu'un clic, [PRENOM] !",
     corps=[para("Pour activer ton compte à l'Académie echecs.com, confirme simplement ton adresse e-mail."), bouton("Confirmer mon adresse", L("CONFIRMATION")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 48 heures. Tu n\'as pas créé de compte ? Ignore cet e-mail.</span>')])
mail(id="02-bienvenue-compte-gratuit", cat="Compte", quand="Juste après la confirmation de l'adresse", img="bienvenue", alt="La mascotte echecs.com souhaite la bienvenue",
     objet="Bienvenue sur echecs.com, [PRENOM] ♟️", pre="6 leçons offertes, le forum et le puzzle du jour t'attendent.", sur="Bienvenue", titre="Ton compte est prêt.",
     corps=[para("Bienvenue dans la communauté echecs.com ! Sans attendre et sans payer, tu as déjà accès à :"),
            liste(["<b>6 leçons</b> de l'Académie, pour découvrir la méthode", "<b>Le puzzle du jour</b>, un nouveau problème chaque matin", "<b>Le forum</b>, pour poser tes questions et partager tes parties", "<b>La zone de jeu</b>, pour jouer tes parties en ligne"]),
            bouton("Ma première leçon", L("PREMIERE_LECON")),
            offre("Envie d'aller plus loin ? L'Académie complète : +200 leçons, +2 000 exercices, les masterclasses et la revue en PGN."), para('<a href="[LIEN_ABONNEMENT]" style="font-weight:800;color:#1f5fa8;text-decoration:none">Voir les formules&nbsp;&rarr;</a>')])
mail(id="03-mot-de-passe", cat="Compte", marketing=False, quand="Sur demande de réinitialisation (transactionnel)",
     objet="Réinitialise ton mot de passe", pre="Ce lien est valable 1 heure.", sur="Ton compte", titre="Nouveau mot de passe",
     corps=[para("[PRENOM], tu as demandé à changer ton mot de passe. Clique ci-dessous pour en choisir un nouveau."), bouton("Choisir mon mot de passe", L("MOT_DE_PASSE")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 1 heure. Si tu n\'es pas à l\'origine de cette demande, ignore cet e-mail : ton mot de passe ne change pas.</span>')])

# ---------- 2. Conversion du compte gratuit ----------
mail(id="04-gratuit-j3-lecons", cat="Compte gratuit → abonnement", quand="J+3 après la création du compte, si pas abonné", img="lecons", alt="Les leçons interactives de l'Académie",
     objet="Tes 6 leçons offertes t'attendent", pre="Vidéo, cours, exercice, quiz : tu as essayé ?", sur="Ta découverte", titre="Tu as essayé une leçon ?",
     corps=[para("[PRENOM], chaque leçon de l'Académie suit le même chemin : une <b>vidéo</b>, un <b>cours</b>, des <b>exercices</b> sur l'échiquier, puis un <b>quiz</b> pour valider. Tu as 6 leçons offertes à découvrir."),
            bouton("Reprendre mes leçons", L("LECONS")), para("Et chaque matin, un nouveau <b>puzzle du jour</b> t'attend pour garder la main.")])
mail(id="05-gratuit-j7-offre", cat="Compte gratuit → abonnement", quand="J+7 après la création du compte, si pas abonné", img="progression", alt="Le parcours de progression de l'Académie",
     objet="On continue ? Des centaines de leçons t'attendent !", pre="Prix de lancement, sans engagement en mensuel.", sur="Offre de lancement", titre="Passe à l'Académie complète.",
     corps=[para("Tu as découvert la méthode de l'Académie, mais ce n'est que le début ! Envie d'aller plus loin, [PRENOM] ? Avec l'abonnement, tu débloques tout :"),
            liste(["+200 leçons interactives, de l'initiation à 2000+", "+2 000 exercices à ton niveau", "Les masterclasses en direct et leurs replays", "Tout le catalogue vidéos et la revue Europe Échecs", "Tes parties analysées, les tournois en ligne"]),
            offre(), bouton("Je m'abonne", L("ABONNEMENT"))])
mail(id="06-gratuit-j21-relance", cat="Compte gratuit → abonnement", quand="J+21 après la création du compte, si pas abonné et actif dans les 14 derniers jours", img="exercices", alt="Les exercices de l'Académie",
     objet="Tu n'as encore rien vu, [PRENOM] : il reste tant à découvrir !", pre="Ce que les abonnés ont en plus, en 30 secondes.", sur="Ta découverte", titre="Tu hésites encore ?",
     corps=[para("Tu utilises déjà le puzzle du jour et les leçons offertes. Voici ce que l'abonnement ajoute, <b>sans engagement</b> :"),
            comparatif([("Leçons", "6", "+200"), ("Exercices", "puzzle du jour", "+2 000"), ("Masterclasses", False, True), ("Revue en PGN", False, True), ("Tes parties analysées", False, True), ("Forum", True, True)]),
            offre("Toujours au prix de lancement :"), bouton("Choisir ma formule", L("ABONNEMENT"))])

mail(id="46-gratuit-nouveautes-trimestre", cat="Compte gratuit → abonnement",
     quand="Tous les 3 mois, aux comptes gratuits qui acceptent les e-mails d'information (après le 06 ; pas dans les 30 jours qui suivent 05, 06, 31 ou 33)",
     alt="Quoi de neuf à l'Académie ?",
     exemples={"TITRE_UNE": "Les finales de Tours, par Marc Quenehen", "DESCRIPTION_UNE": "Lucena, Philidor, la Tour active : 18 leçons pour sauver ou gagner les finales les plus fréquentes."},
     objet="Il y a du nouveau dans l'Académie, [PRENOM] !", pre="[NB_NOUVELLES_LECONS_TRIMESTRE] nouvelles leçons, des masterclasses, des tournois… et ton prix de lancement t'attend.",
     sur="Ton compte gratuit", titre="Du nouveau | [PERIODE] !",
     corps=[para("[PRENOM], ces 3 derniers mois, l'Académie s'est encore enrichie :"),
            nouveautes("Ces 3 derniers mois", [("Nouvelles leçons", "[NB_NOUVELLES_LECONS_TRIMESTRE]"), ("Masterclasses en direct", "[NB_MASTERCLASSES_TRIMESTRE]"), ("Cours en vidéo", "[NB_VIDEOS_TRIMESTRE]"), ("Tournois organisés", "[NB_TOURNOIS_TRIMESTRE]")]),
            carte("b-cours", "À la une : [TITRE_UNE]", "[DESCRIPTION_UNE]", L("UNE"), "Découvrir"),
            para("Avec ton compte gratuit, tu profites déjà de 6 leçons, du forum et du puzzle du jour. Avec l'abonnement, tu débloques tout :"),
            liste(["<b>+200 leçons</b> et <b>+2 000 exercices</b>, de l'initiation à 2000+", "<b>Les masterclasses</b> en direct et leurs replays", "<b>La revue Europe Échecs</b> en PGN et tes parties analysées"]),
            offre("Toujours au prix de lancement :"), bouton("Je m'abonne", L("ABONNEMENT")),
            para('<span style="color:#6b6b66;font-size:14px">Pas pour l\'instant ? Tes 6 leçons, le forum et le puzzle du jour restent gratuits, sans limite de temps.</span>')])

mail(id="47-gratuit-lecons-terminees", cat="Compte gratuit → abonnement", quand="Dès que la 6ᵉ leçon offerte est validée (une seule fois)", alt="6 leçons bouclées",
     objet="Bravo, tu as réussi les 6 leçons offertes de l'Académie 🎉", pre="La suite t'attend : [LECON_SUIVANTE] et +200 autres leçons.", sur="Ta découverte", titre="Et maintenant, | la suite ?",
     corps=[para("[PRENOM], tu as terminé les 6 leçons offertes de l'Académie : bravo, tu as pris le rythme ! Mais il te reste encore beaucoup à découvrir…"),
            tuiles([("6", "Leçons terminées"), ("[NB_EXERCICES]", "Exercices réussis"), ("[TAUX_REUSSITE]&nbsp;%", "Réussite")]),
            encadre("<b>🔒 Ta prochaine leçon : [LECON_SUIVANTE]</b><br>[DESCRIPTION_LECON_SUIVANTE]"),
            para("Avec l'abonnement, tu continues sans t'arrêter : <b>+200 leçons</b>, <b>+2 000 exercices</b>, les masterclasses et la revue en PGN."),
            offre("Au prix de lancement :"), bouton("Débloquer la suite", L("ABONNEMENT"))])
mail(id="48-gratuit-serie-puzzles", cat="Compte gratuit → abonnement", quand="Le lendemain du 7ᵉ jour de suite sur le puzzle du jour (une seule fois)", alt="7 puzzles d'affilée",
     objet="7 puzzles de suite : belle série, [PRENOM] 🔥", pre="Ta régularité paie. Et si tu passais à +2 000 exercices ?", sur="Ta série", titre="Une semaine | sans manquer un jour.",
     corps=[para("[PRENOM], tu as ouvert le puzzle du jour 7 jours de suite. C'est exactement comme ça qu'on progresse aux échecs."),
            tuiles([("7", "Jours de suite"), ("[NB_PUZZLES_REUSSIS]", "Puzzles réussis")]),
            para("Envie d'en faire plus ? Avec l'abonnement, des exercices à ton niveau sur chaque thème :"),
            liste(["<b>Mat en 1, 2 et 3</b>, fourchettes, clouages, enfilades", "<b>Les finales</b> essentielles, pas à pas", "<b>Ta progression</b> par thème, pour savoir quoi travailler"]),
            offre("Au prix de lancement :"), bouton("Débloquer les exercices", L("ABONNEMENT")),
            para('<span style="color:#6b6b66;font-size:14px">Et demain, le puzzle du jour t\'attend : garde ta série !</span>')])
mail(id="49-gratuit-extrait-masterclass", cat="Compte gratuit → abonnement", quand="Quand un extrait de masterclass est publié en libre accès sur YouTube (au plus 1 par trimestre, pas le même mois que le 46)", alt="Un extrait offert",
     objet="Cadeau : [DUREE_EXTRAIT] de masterclass avec [COACH] 🎁", pre="[THEME], en libre accès sur YouTube.", sur="Masterclass", titre="[DUREE_EXTRAIT] avec | [COACH].",
     corps=[para("[PRENOM], pour te faire découvrir les masterclasses de l'Académie, voici un extrait en libre accès :"),
            coach(), video("[URL_MINIATURE_EXTRAIT]", "[THEME]", "Extrait · [DUREE_EXTRAIT] · avec [COACH]", L("MASTERCLASSES"), L("YOUTUBE_EXTRAIT"), "Les masterclasses"),
            para("La masterclass complète, et toutes les autres, sont incluses dans l'abonnement : en direct, avec tes questions, et en replay quand tu veux."),
            offre("Au prix de lancement :"), bouton("Je m'abonne", L("ABONNEMENT"))])
mail(id="50-gratuit-tournoi-ouvert", cat="Compte gratuit → abonnement", quand="5 jours avant un tournoi ouvert à tous, aux comptes gratuits (les abonnés reçoivent le 23)", alt="Tournoi en ligne",
     exemples={"DATE": "21 novembre", "JOUR": "21", "HEURE": "20 h"},
     objet="Tournoi gratuit : [NOM_TOURNOI] le [DATE]", pre="Ouvert à tous les comptes, cadence [CADENCE].", sur="Tournoi ouvert à tous", titre="Ton compte gratuit | suffit pour jouer.",
     corps=[para("[PRENOM], le prochain tournoi en ligne est ouvert à tous les membres d'echecs.com, abonnés ou non :"),
            billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]"), ("Rondes", "[NB_RONDES]"), ("Niveau", "ouvert à tous")]),
            bouton("Je m'inscris", L("INSCRIPTION_TOURNOI")),
            para('<span style="color:#6b6b66;font-size:14px">Les abonnés retrouvent en plus leurs parties analysées après le tournoi. <a href="[LIEN_ABONNEMENT]" style="color:#1f5fa8">Voir les formules</a></span>')])
mail(id="51-gratuit-anniversaire-compte", cat="Compte gratuit → abonnement", quand="À la date anniversaire du compte gratuit (chaque année)", alt="Un an ensemble",
     objet="1 an avec echecs.com, [PRENOM] 🎉", pre="Ton année en chiffres : merci d'être là !", sur="Anniversaire", titre="Merci d'être là | depuis 1 an.",
     corps=[para("[PRENOM], ça fait 1 an que tu as créé ton compte echecs.com. Voici le bilan de ton année :"),
            tuiles([("[NB_PUZZLES_ANNEE]", "Puzzles résolus"), ("[NB_LECONS_GRATUITES_FAITES]", "Leçons offertes"), ("[NB_MESSAGES_FORUM]", "Messages au forum")]),
            para("Et si cette deuxième année était celle où tu passes un cap ? L'Académie complète t'accompagne de l'initiation à 2000+."),
            offre("Toujours au prix de lancement :"), bouton("Passer à l'Académie complète", L("ABONNEMENT"))])
mail(id="52-offrir-academie", cat="Saisonnier", quand="Fin novembre et mi-décembre, à tous les comptes qui acceptent les e-mails d'information (si la carte cadeau existe sur le site)", alt="Offre l'Académie",
     objet="Et si tu offrais l'Académie à Noël ? 🎁", pre="Un abonnement en cadeau, à imprimer ou à envoyer par e-mail.", sur="Idée cadeau", titre="Le cadeau | des joueurs d'échecs.",
     corps=[para("[PRENOM], un proche joue aux échecs, ou rêve de s'y mettre ? Offre-lui l'Académie :"),
            liste(["<b>Une carte cadeau</b> à imprimer ou à envoyer par e-mail, le jour de ton choix", "<b>L'accès complet</b> : +200 leçons, +2 000 exercices, les masterclasses, la revue en PGN", "<b>Activation en un clic</b>, sans moyen de paiement à fournir"]),
            encadre("<b>[DUREES_CADEAU]</b>, à partir de <b>[PRIX_CADEAU]</b>."),
            bouton("Offrir l'Académie", L("CADEAU"))])

# ---------- 3. Abonnement ----------
mail(id="07-confirmation-abonnement", cat="Abonnement", marketing=False, quand="Au paiement du premier abonnement (transactionnel)", img="objectif", alt="Objectif atteint",
     objet="Bienvenue dans l'Académie, [PRENOM] !", pre="Ton abonnement est actif : voici ton récapitulatif.", sur="Abonnement confirmé", titre="Tu fais partie de l'Académie.",
     corps=[para("Excellent choix pour progresser ! Merci pour ta confiance, ton abonnement est actif dès maintenant."),
            recu([("Formule", "[FORMULE]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]"), ("Moyen de paiement", "[MOYEN_PAIEMENT]")], "Payé aujourd'hui", "[PRIX]"),
            bouton("Choisir mon parcours", L("PARCOURS")), para('<span style="color:#6b6b66;font-size:14px">Ta facture est disponible dans <a href="[LIEN_FACTURES]" style="color:#1f5fa8">ton espace</a>.</span>')])
mail(id="08-paiement-refuse", cat="Abonnement", marketing=False, quand="Échec d'un prélèvement (transactionnel), relance à J+3 si non réglé",
     objet="Ton paiement n'est pas passé", pre="Mets à jour ta carte pour garder l'accès à l'Académie.", sur="Paiement", titre="Ton paiement n'est pas passé.",
     corps=[para("[PRENOM], le paiement de ton abonnement du [DATE] n'a pas pu être effectué. Ça arrive : carte expirée, plafond atteint…"),
            para("Mets à jour ton moyen de paiement pour garder l'accès à tes leçons, tes exercices et les masterclasses."), bouton("Mettre à jour ma carte", L("PAIEMENT")),
            para('<span style="color:#6b6b66;font-size:14px">Sans régularisation, ton accès sera suspendu le [DATE_SUSPENSION]. Ta progression reste enregistrée.</span>')])
mail(id="09-paiement-recu", cat="Abonnement", marketing=False, quand="À chaque renouvellement réussi (transactionnel)",
     objet="Ton reçu echecs.com · [MOIS]", pre="Merci ! Ton abonnement continue.", sur="Reçu", titre="Merci, [PRENOM] !",
     corps=[para("Ton abonnement à l'Académie est renouvelé. Tu vas pouvoir continuer à progresser !"), recu([("Formule", "[FORMULE]"), ("Date", "[DATE]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]")], "Montant", "[PRIX]"),
            bouton("Voir ma facture", L("FACTURES"))])

# ---------- 4. Démarrage de l'abonné ----------
mail(id="10-demarrage-j1-parcours", cat="Démarrage de l'abonné", quand="J+1 après l'abonnement", img="etapes", alt="Valide chaque étape",
     objet="Par où commencer ? Ton parcours en 3 étapes", pre="Initiation, 1400, 1600, 1800 : trouve ton niveau.", sur="Ton parcours", titre="Trouve ton niveau.",
     corps=[para("[PRENOM], l'Académie est organisée en parcours : <b>Initiation</b>, <b>Objectif 1400</b>, <b>1600</b>, <b>1800</b>, puis <b>2000 et +</b>."),
            liste(['Choisis le parcours qui correspond à ton niveau, ou <a href="[LIEN_TEST_PLACEMENT]" style="color:#1f5fa8">passe le test de placement</a> (5 minutes)', "Fais une leçon : vidéo, cours, exercices, quiz", "Valide le quiz pour débloquer la suivante"]),
            bouton("Choisir mon parcours", L("PARCOURS"))])
mail(id="11-demarrage-j3-exercices", cat="Démarrage de l'abonné", quand="J+3 après l'abonnement", img="exercices", alt="Les exercices de l'Académie",
     objet="10 minutes par jour suffisent", pre="+2 000 exercices, rangés par thème et par niveau.", sur="Exercices", titre="10 minutes par jour.",
     corps=[para("La régularité fait plus que les longues séances. Chaque jour, quelques exercices à ton niveau : mat en 1, fourchette, clouage, finales…"),
            para("Ta <b>série de jours</b> s'affiche sur ton tableau de bord : essaie de ne pas la casser !"), bouton("Faire mes exercices du jour", L("EXERCICES"))])
mail(id="12-demarrage-j6-masterclasses", cat="Démarrage de l'abonné", quand="J+6 après l'abonnement", img="masterclasses", alt="Les masterclasses en direct",
     objet="Les grands maîtres t'attendent", pre="Masterclasses en direct et replays, inclus dans ton abonnement.", sur="Masterclasses", titre="Apprends des meilleurs.",
     corps=[para("Gata Kamsky, Fabien Libiszewski, Sylvain Ravot, Marc Quenehen… Les masterclasses sont <b>incluses</b> dans ton abonnement, en direct et en replay."),
            para("Tu peux poser tes questions pendant le direct. Une occasion à ne pas rater !"), bouton("Voir les masterclasses", L("MASTERCLASSES"))])
mail(id="13-demarrage-j10-communaute", cat="Démarrage de l'abonné", quand="J+10 après l'abonnement", img="tournois", alt="Les tournois en ligne",
     objet="Joue, partage, mesure-toi", pre="Tournois en ligne, forum, tes parties analysées.", sur="Communauté", titre="Rejoins la communauté.",
     corps=[para("L'Académie est aussi une communauté de joueurs, unis pour progresser ensemble !"), liste(["<b>Les tournois en ligne</b>, ouverts à tous les niveaux", "<b>Le forum</b>, pour poser tes questions aux coachs et aux autres membres", "<b>Tes parties</b> : saisis-les, analyse-les, partage-les en PGN"]),
            bouton("Voir le prochain tournoi", L("TOURNOIS"))])

# ---------- 5. Engagement ----------
# Bilan du mois (actif, peu actif) : le 1er du mois ; sans activité : relance à 1 semaine (45), puis 3 semaines (17) et 6 semaines (18)
NOUV_MOIS = nouveautes("Ce mois-ci dans l'Académie", [("Nouvelles leçons", "[NB_NOUVELLES_LECONS_MOIS]"), ("Masterclasses et cours en vidéo", "[NB_VIDEOS_MOIS]"), ("Tournois organisés", "[NB_TOURNOIS_MOIS]")])
NOUV_ACA = nouveautes("Cette semaine dans l'Académie", [("Nouvelles leçons", "[NB_NOUVELLES_LECONS]"), ("Cours et masterclasses en vidéo", "[NB_VIDEOS_SEMAINE]"), ("Tournois organisés", "[NB_TOURNOIS_SEMAINE]")])
mail(id="14-bilan-mois-actif", cat="Bilan du mois", quand="Le 1er du mois, si au moins 8 jours d'entraînement dans le mois écoulé", alt="Ton mois d'échecs",
     exemples={"NB_JOURS_ACTIFS": "18", "NB_COURS_SUIVIS": "6", "NB_LECONS": "26", "NB_EXERCICES": "412", "NB_PARTIES": "47", "SERIE": "12", "PROGRESSION_PARCOURS": "62"},
     objet="[PRENOM], ton mois d'échecs en chiffres 🔥", pre="[NB_JOURS_ACTIFS] jours d'entraînement, [NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo !", sur="Ton bilan de [MOIS]", titre="[NB_JOURS_ACTIFS] jours d'entraînement, | bravo !",
     corps=[para("[PRENOM], voici ton bilan du mois :"),
            tuiles([("[NB_COURS_SUIVIS]", "Cours suivis"), ("[NB_LECONS]", "Leçons"), ("[NB_EXERCICES]", "Exercices réussis")]),
            tuiles([("[NB_PARTIES]", "Parties jouées"), ("[SERIE]", "Jours de série"), ("[TAUX_REUSSITE]&nbsp;%", "Réussite")]),
            progression("[PARCOURS]", "[PROGRESSION_PARCOURS]"),
            encadre("<b>La régularité paie !</b> Ton point fort ce mois-ci : <b>[THEME_FORT]</b>. À travailler : <b>[THEME_FAIBLE]</b>."),
            NOUV_MOIS, bouton("Continuer mon parcours", L("PARCOURS"))])
mail(id="44-bilan-mois-peu-actif", cat="Bilan du mois", quand="Le 1er du mois, si 1 à 7 jours d'entraînement dans le mois écoulé", alt="Bon début, on continue ?",
     exemples={"NB_JOURS_ACTIFS": "5", "NB_LECONS": "7", "NB_EXERCICES": "64", "NB_PARTIES": "6", "PROGRESSION_PARCOURS": "34"},
     objet="[PRENOM], ton mois d'échecs : on continue ?", pre="[NB_LECONS] leçons ce mois-ci. 10 minutes de plus par semaine, et ça change tout.", sur="Ton bilan de [MOIS]", titre="Chaque séance | compte !",
     corps=[para("Jours d'entraînement ce mois-ci : <b>[NB_JOURS_ACTIFS]</b>. Voici ton bilan :"),
            tuiles([("[NB_LECONS]", "Leçons"), ("[NB_EXERCICES]", "Exercices réussis"), ("[NB_PARTIES]", "Parties jouées")]),
            progression("[PARCOURS]", "[PROGRESSION_PARCOURS]"),
            encadre("<b>Le secret des joueurs qui progressent :</b> 10 minutes, 3 fois par semaine. Ta prochaine leçon, <b>[LECON_SUIVANTE]</b>, prend environ [DUREE_LECON]."),
            NOUV_MOIS, bouton("Reprendre ma leçon", L("LECON_SUIVANTE"))])
mail(id="45-inactif-1-semaine", cat="Réactivation", quand="Après 7 jours sans activité (une seule fois par période d'inactivité ; puis 17 à 3 semaines et 18 à 6 semaines)", alt="Ta place t'attend", exemples={"PROGRESSION_PARCOURS": "34"},
     objet="Ce que tu as manqué cette semaine 👀", pre="Nouvelles leçons, cours en vidéo, tournoi… et ta prochaine leçon t'attend.", sur="Ta semaine · [SEMAINE]", titre="Ta place | t'attend.",
     corps=[para("Pas d'échecs cette semaine ? Ça arrive à tout le monde. Voici ce qui s'est passé pendant ce temps :"),
            NOUV_ACA,
            progression("[PARCOURS]", "[PROGRESSION_PARCOURS]"),
            encadre("<b>Pour repartir :</b> une seule leçon, <b>[LECON_SUIVANTE]</b>, environ [DUREE_LECON]. Ta série redémarre dès aujourd'hui."),
            bouton("Faire une leçon", L("LECON_SUIVANTE")),
            para('<span style="color:#6b6b66;font-size:14px">Ton abonnement est actif : toute l\'Académie t\'attend, quand tu veux.</span>')])
mail(id="15-objectif-atteint", cat="Engagement", quand="Quand l'abonné valide un module ou un parcours", img="objectif", alt="Objectif atteint",
     objet="Module validé : [MODULE] 🎉", pre="Une étape de plus vers ton objectif.", sur="Bravo", titre="Module validé !",
     corps=[para("Bravo [PRENOM], tu viens de valider <b>[MODULE]</b>. Tu as passé [NB_LECONS_MODULE] leçons et réussi [NB_EXERCICES_MODULE] exercices."),
            para("Prochaine étape : <b>[MODULE_SUIVANT]</b>."), bouton("Module suivant", L("MODULE_SUIVANT"))])
mail(id="16-serie-en-danger", cat="Engagement", quand="Le soir, si la série de jours (≥ 5 jours) va s'interrompre (au plus une fois toutes les 4 semaines par joueur)", img="exercices", alt="La série de jours",
     objet="Ta série de [SERIE] jours va s'arrêter ⏳", pre="Un exercice suffit pour la garder.", sur="Ta série", titre="Garde ta série !",
     corps=[para("[PRENOM], tu as joué [SERIE] jours d'affilée. Il te reste jusqu'à minuit pour la prolonger : <b>un seul exercice suffit</b>."), bouton("Faire un exercice", L("EXERCICE_DU_JOUR"))])
mail(id="17-inactif-3-semaines", cat="Réactivation", quand="Après 3 semaines sans activité (une seule fois par période d'inactivité ; le 45 est parti à 1 semaine)", img="lecons", alt="Les leçons de l'Académie",
     objet="Ta progression t'attend, [PRENOM]", pre="3 semaines sans échecs : on reprend avant de perdre le fil ?", sur="On reprend ?", titre="On reprend là où tu en étais ?",
     corps=[para("[PRENOM], 3 semaines sans échecs : c'est le bon moment pour reprendre, avant de perdre le fil."),
            para("Ta dernière leçon était <b>[DERNIERE_LECON]</b>. La suivante, <b>[LECON_SUIVANTE]</b>, prend environ [DUREE_LECON]."), bouton("Reprendre ma leçon", L("LECON_SUIVANTE")),
            para('<span style="color:#6b6b66;font-size:14px">Peu de temps ? Quelques exercices par jour suffisent pour retrouver le rythme.</span>')])
mail(id="18-inactif-6-semaines", cat="Réactivation", quand="Après 6 semaines sans activité (une seule fois par période d'inactivité ; dernière relance)", img="dodo", alt="La mascotte qui dort",
     objet="Tu nous manques, [PRENOM]", pre="Voici ce qui est nouveau depuis ta dernière visite.", sur="Quoi de neuf", titre="Tu nous manques !",
     corps=[para("Depuis ta dernière visite, il s'est passé des choses dans l'Académie :"), liste(["[NOUVEAUTE_1]", "[NOUVEAUTE_2]", "[NOUVEAUTE_3]"]),
            para("Ton abonnement est toujours actif : profites-en, ce serait dommage d'arrêter ta progression maintenant !"), bouton("Revenir sur l'Académie", L("ACADEMIE"))])

# ---------- 6. Événements ----------
mail(id="19-annonce-masterclass", cat="Événements", quand="Dès qu'une masterclass est programmée (au moins 7 jours avant)", img="masterclasses", alt="Portrait du coach",
     objet="Masterclass en direct avec [COACH]", pre="[THEME], le [DATE] à [HEURE]. Pose tes questions !", sur="Nouvelle masterclass", titre="[THEME]",
     corps=[para("<b>[COACH]</b> ([TITRE_COACH]) te donne rendez-vous pour une masterclass en direct :"),
            billet("[THEME]", [("Heure", "[HEURE] · Paris"), ("Durée", "[DUREE]"), ("Niveau", "[NIVEAU]")]), coach(),
            para("[DESCRIPTION_MASTERCLASS]"), bouton("Voir la masterclass", L("MASTERCLASS")),
            para('<span style="color:#6b6b66;font-size:14px">Le lien du direct t\'arrivera par e-mail la veille de la masterclass. Tu ne peux pas être là ? Le replay sera disponible dans l\'Académie.</span>')])
mail(id="20-rappel-masterclass", cat="Événements", quand="La veille à 18 h (un seul rappel), avec le lien du direct", img="masterclasses", alt="Masterclass en direct",
     objet="Demain : masterclass avec [COACH]", pre="[THEME], en direct à [HEURE]. Ton lien est dans cet e-mail.", sur="Rappel", titre="Rendez-vous demain | à [HEURE] !",
     corps=[para("[PRENOM], la masterclass <b>[THEME]</b> avec <b>[COACH]</b> commence demain à <b>[HEURE]</b>. Voici ton lien pour rejoindre le direct : garde cet e-mail !"),
            bouton("Rejoindre le direct", L("DIRECT")),
            para('<span style="color:#6b6b66;font-size:14px">Prépare tes questions : tu pourras les poser pendant le direct.</span>')])
mail(id="21-replay-masterclass", cat="Événements", quand="Dès que le replay est en ligne", img="masterclasses", alt="Replay de masterclass",
     objet="Replay : [THEME]", pre="La masterclass de [COACH] en entier, et les positions en PGN.", sur="Replay disponible", titre="Tu l'as manquée ? Le replay est là.",
     corps=[para("La masterclass <b>[THEME]</b> avec <b>[COACH]</b> est disponible en replay."), coach(), encadre("<b>À retenir :</b> [RESUME_MASTERCLASS]"),
            bouton("Voir le replay", L("REPLAY")), para("Les positions étudiées sont aussi dans l'Académie, en PGN interactif.")])
mail(id="22-nouveau-cours", cat="Événements", quand="À la mise en ligne d'un nouveau cours ou d'un replay de cours", img="videos", alt="Nouveau cours en ligne",
     objet="Ton nouveau cours : [TITRE_COURS]", pre="[NB_LECONS_COURS] leçons, niveau [NIVEAU].", sur="Nouveau dans l'Académie", titre="[TITRE_COURS]",
     corps=[para("Un nouveau cours vient d'arriver dans l'Académie : <b>[TITRE_COURS]</b>, par [AUTEUR]."), coach("[AUTEUR]", "[TITRE_AUTEUR]", "[URL_PHOTO_AUTEUR]", "l'auteur de ce cours"),
            tuiles([("[NB_LECONS_COURS]", "leçons"), ("[NIVEAU]", "niveau"), ("[DUREE]", "au total")]), para("[DESCRIPTION_COURS]"), bouton("Commencer le cours", L("COURS"))])
mail(id="23-annonce-tournoi", cat="Événements", quand="5 jours avant un tournoi, rappel le jour J (même modèle)", img="tournois", alt="Tournoi en ligne",
     objet="Tournoi : [NOM_TOURNOI] le [DATE]", pre="Cadence [CADENCE], ouvert à tous les niveaux.", sur="Tournoi en ligne", titre="[NOM_TOURNOI]",
     corps=[para("Mesure-toi aux autres membres de l'Académie et mets en pratique ce que tu as appris !"), billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]"), ("Rondes", "[NB_RONDES]"), ("Niveau", "ouvert à tous")]),
            bouton("Je m'inscris", L("INSCRIPTION_TOURNOI"))])
mail(id="24-resultats-tournoi", cat="Événements", quand="Le lendemain du tournoi, aux participants", img="tournois", alt="Résultats du tournoi",
     objet="Résultats : [NOM_TOURNOI]", pre="Tu termines [PLACE]ᵉ sur [NB_JOUEURS] : bravo !", sur="Résultats", titre="Tu termines [PLACE]<sup>e</sup> !",
     corps=[para("[PRENOM], tu termines <b>[PLACE]<sup>e</sup> sur [NB_JOUEURS]</b> au <b>[NOM_TOURNOI]</b>, avec <b>[POINTS] points</b> sur [NB_RONDES]. Voici le podium :"),
            podium("[VAINQUEUR]", "[DEUXIEME]", "[TROISIEME]"), para("Revois tes parties : elles sont déjà dans ton espace, prêtes à être analysées."),
            bouton("Analyser mes parties", L("MES_PARTIES"))])
mail(id="25-sortie-revue", cat="Événements", quand="À la sortie de chaque numéro", img="revue", alt="La revue Europe Échecs",
     objet="Le n° [NUMERO] d'Europe Échecs est sorti", pre="Toutes les parties en PGN interactif dans l'Académie.", sur="La revue", titre="Le n° [NUMERO] est là.",
     corps=[para("Au sommaire de ce numéro :"), liste(["[SOMMAIRE_1]", "[SOMMAIRE_2]", "[SOMMAIRE_3]"]),
            para("Rejoue chaque partie commentée directement sur l'échiquier, en PGN interactif."), bouton("Lire le numéro", L("REVUE"))])

# ---------- 7. Lettre d'information (plusieurs nouvelles) ----------
mail(id="26-lettre-plusieurs-nouvelles", cat="Lettre d'information", quand="Toutes les 1 à 2 semaines, à tous les comptes (gratuits et abonnés)", img="progression", alt="Les nouvelles de l'Académie",
     objet="Cette semaine : [TITRE_UNE]", pre="Masterclass, tournoi, nouveau cours et le puzzle de la semaine.", sur="Les nouvelles · [DATE]", titre="Cette semaine dans l'Académie",
     corps=[para("Bonjour [PRENOM], voici ce qui t'attend cette semaine."),
            carte("b-masterclass", "Masterclass : [THEME]", "Avec [COACH], en direct le [DATE] à [HEURE].", L("MASTERCLASS"), "Voir la masterclass"),
            carte("b-tournoi", "Tournoi : [NOM_TOURNOI]", "Le [DATE_TOURNOI] à [HEURE_TOURNOI], cadence [CADENCE], ouvert à tous.", L("INSCRIPTION_TOURNOI"), "Je m'inscris"),
            carte("b-cours", "Nouveau cours : [TITRE_COURS]", "[NB_LECONS_COURS] leçons, niveau [NIVEAU].", L("COURS"), "Découvrir le cours"),
            carte("puzzle", "Le puzzle de la semaine", "[CONSIGNE_PUZZLE] Tu trouves ? La solution est en ligne.", L("PUZZLE"), "Voir la solution", src="[URL_IMAGE_PUZZLE]"),
            para('<span style="color:#6b6b66;font-size:14px">Les blocs sont indépendants : garde ceux qui ont une actualité et supprime les autres.</span>')])

# ---------- 8. Fin d'abonnement ----------
mail(id="27-renouvellement-annuel-j30", cat="Fin d'abonnement", marketing=False, quand="30 jours avant le renouvellement d'un abonnement annuel (obligatoire)",
     objet="Ton abonnement annuel se renouvelle le [DATE_RENOUVELLEMENT]", pre="Rien à faire si tu continues : voici le récapitulatif.", sur="Renouvellement", titre="Ton année d'Académie se termine bientôt.",
     corps=[para("[PRENOM], ton abonnement annuel se renouvellera automatiquement le <b>[DATE_RENOUVELLEMENT]</b> pour <b>[PRIX]</b>."),
            tuiles([("[NB_LECONS_ANNEE]", "leçons terminées cette année"), ("[NB_EXERCICES_ANNEE]", "exercices réussis")]),
            para("Rien à faire si tu continues. Tu peux modifier ou arrêter ton abonnement à tout moment avant cette date."), bouton("Gérer mon abonnement", L("ABONNEMENT_GERER"))])
mail(id="28-passage-annuel", cat="Fin d'abonnement", quand="Abonnés mensuels depuis 3 mois", img="progression", alt="Ta progression",
     objet="Près de 2 mois offerts en passant à l'annuel", pre="150 €/an au lieu de 12 × 14,90 € : tu économises.", sur="Ton abonnement", titre="Passe à l'annuel.",
     corps=[para("[PRENOM], ça fait 3 mois que tu progresses avec l'Académie. En passant à l'abonnement annuel, tu paies <b>150&nbsp;€ par an</b>, soit 12,50&nbsp;€ par mois au lieu de 14,90&nbsp;€."),
            ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr>' + carte_prix("Annuel", "150&nbsp;€", "/an", "12 × 14,90 € = 178,80 €", "Soit 12,50 € par mois. Ton tarif reste garanti tant que ton abonnement reste actif.", True, "Près de 2 mois offerts") + "</tr></table>"), bouton("Passer à l'annuel", L("PASSAGE_ANNUEL"))])
mail(id="29-fin-abonnement-j7", cat="Fin d'abonnement", marketing=False, quand="7 jours avant la fin d'un abonnement résilié (fin de période payée)", img="oups", alt="La mascotte, surprise",
     objet="Ton accès à l'Académie se termine le [DATE_FIN]", pre="Ta progression reste enregistrée.", sur="Fin d'abonnement", titre="Plus que 7 jours d'accès.",
     corps=[para("[PRENOM], ton abonnement se termine le <b>[DATE_FIN]</b>. Après cette date, tu gardes ton compte gratuit (6 leçons, forum, puzzle du jour), et ta progression reste enregistrée. Mais ce serait dommage de t'arrêter en si bon chemin !"),
            para("Tu as changé d'avis ? Tu peux réactiver ton abonnement en un clic, au même tarif."), bouton("Réactiver", L("REACTIVATION"))])
mail(id="30-resiliation-confirmee", cat="Fin d'abonnement", marketing=False, quand="À la résiliation (transactionnel)",
     objet="Ta résiliation est confirmée", pre="Tu gardes l'accès jusqu'au [DATE_FIN].", sur="Résiliation", titre="C'est noté, [PRENOM].",
     corps=[para("Ta résiliation est enregistrée. Tu gardes l'accès complet à l'Académie jusqu'au <b>[DATE_FIN]</b>, puis ton compte repasse en gratuit."),
            para("Pour nous aider à nous améliorer, dis-nous en une question pourquoi tu pars :"), bouton("Répondre (30 secondes)", L("QUESTIONNAIRE_DEPART")),
            para('<span style="color:#6b6b66;font-size:14px">Ta progression, tes parties et tes statistiques restent enregistrées.</span>')])
mail(id="31-reconquete-j30", cat="Fin d'abonnement", quand="30 jours après la fin de l'abonnement", img="masterclasses", alt="Les nouveautés de l'Académie",
     objet="Ton premier mois à 9,90 € pour revenir", pre="Et tout ce qui a changé depuis ton départ.", sur="Quoi de neuf", titre="Reviens quand tu veux.",
     corps=[para("[PRENOM], nous te proposons une offre à prix réduit pour revenir dans l'Académie ! Pendant ton absence, elle a continué d'avancer :"), liste(["[NOUVEAUTE_1]", "[NOUVEAUTE_2]", "[NOUVEAUTE_3]"]),
            ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0;border-collapse:separate"><tr>' + carte_prix("Ton retour", "9,90&nbsp;€", "le 1er mois", "19,90 €/mois", "Puis 19,90 €/mois, sans engagement.", True, "Offre de retour") + "</tr></table>" + para("Ta progression t'attend là où tu l'as laissée.")), bouton("Revenir pour 9,90 €", L("REACTIVATION"))])
mail(id="32-anniversaire", cat="Engagement", quand="À la date anniversaire de l'abonnement", img="progression", alt="Anniversaire",
     objet="Déjà [DUREE_ABONNEMENT] dans l'Académie 🎉", pre="Merci, [PRENOM] ! Voici ton parcours.", sur="Anniversaire", titre="Joyeux anniversaire d'abonnement !",
     corps=[para("[PRENOM], ça fait <b>[DUREE_ABONNEMENT]</b> que tu t'entraînes avec nous. Merci, et bravo : ta progression se poursuit !"),
            tuiles([("[NB_LECONS_TOTAL]", "leçons"), ("[NB_EXERCICES_TOTAL]", "exercices réussis"), ("[NB_MODULES]", "modules validés")]), bouton("Voir ma progression", L("PROGRESSION"))])


# ---------- 9. Compléments (compte, facturation, événements) ----------
mail(id="33-paiement-abandonne", cat="Compte gratuit → abonnement", quand="2 heures après une page de paiement ouverte sans paiement", 
     objet="Ton abonnement n'est pas finalisé", pre="Il ne manque qu'une étape.", sur="Abonnement", titre="Il ne manque qu'une étape.",
     corps=[para("[PRENOM], tu as commencé à t'abonner à l'Académie sans aller jusqu'au bout. Un souci avec le paiement ?"),
            recu([("Formule choisie", "[FORMULE]")], "Prix", "[PRIX]"), bouton("Finaliser mon abonnement", L("ABONNEMENT")),
            para('<span style="color:#6b6b66;font-size:14px">Une question ? Réponds simplement à cet e-mail.</span>')])
mail(id="34-changement-formule", cat="Abonnement", marketing=False, quand="Au passage du mensuel à l'annuel (ou l'inverse), transactionnel",
     objet="Ta nouvelle formule est enregistrée", pre="Voici ce qui change pour toi.", sur="Ton abonnement", titre="C'est enregistré.",
     corps=[para("[PRENOM], ton changement de formule est pris en compte."), recu([("Nouvelle formule", "[FORMULE]"), ("À partir du", "[DATE]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]")], "Nouveau prix", "[PRIX]"),
            bouton("Gérer mon abonnement", L("ABONNEMENT_GERER"))])
mail(id="35-carte-expire", cat="Abonnement", marketing=False, quand="30 jours avant l'expiration de la carte enregistrée (transactionnel)",
     objet="Ta carte bancaire expire bientôt", pre="Mets-la à jour pour éviter une interruption.", sur="Paiement", titre="Ta carte expire bientôt.",
     corps=[para("[PRENOM], la carte enregistrée pour ton abonnement (se terminant par [CARTE_4_CHIFFRES]) expire fin [MOIS_EXPIRATION]."),
            para("Mets-la à jour dès maintenant pour ne pas perdre l'accès à tes leçons."), bouton("Mettre à jour ma carte", L("PAIEMENT"))])
mail(id="36-inscription-tournoi", cat="Événements", marketing=False, quand="À l'inscription à un tournoi (transactionnel)", img="tournois", alt="Tournoi en ligne",
     objet="Inscription confirmée : [NOM_TOURNOI]", pre="Rendez-vous le [DATE] à [HEURE].", sur="Inscription confirmée", titre="C'est noté, à [HEURE] !",
     corps=[billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]")]),
            para("Connecte-toi 10 minutes avant le début : les appariements de la 1re ronde sont publiés à [HEURE]."), bouton("Voir le tournoi", L("TOURNOI")),
            para('<span style="color:#6b6b66;font-size:14px">Un empêchement ? <a href="[LIEN_DESINSCRIPTION_TOURNOI]" style="color:#1f5fa8">Libère ta place</a>.</span>')])
mail(id="37-masterclass-reportee", cat="Événements", marketing=False, quand="Si une masterclass annoncée est déplacée ou annulée (aux inscrits)",
     objet="Masterclass déplacée au [NOUVELLE_DATE]", pre="[THEME], avec [COACH] : la nouvelle date.", sur="Information", titre="La masterclass est déplacée.",
     corps=[para("[PRENOM], la masterclass <b>[THEME]</b> avec <b>[COACH]</b>, prévue le [DATE], est déplacée."),
            billet("[THEME]", [("Heure", "[HEURE] · Paris"), ("Avec", "[COACH]")], "[NOUVEAU_JOUR]", "[NOUVEAU_MOIS_COURT]"), para("Désolés pour ce changement. Si tu ne peux pas être là, le replay sera disponible comme d'habitude."),
            bouton("Voir la masterclass", L("MASTERCLASS"))])
mail(id="38-reponse-forum", cat="Engagement", quand="Quand quelqu'un répond à un sujet de l'abonné (au plus 1 par jour, regroupé)", img="forum", alt="Le forum de l'Académie",
     objet="[AUTEUR_REPONSE] t'a répondu sur le forum", pre="« [EXTRAIT_REPONSE] »", sur="Le forum", titre="Nouvelle réponse à ton sujet",
     corps=[para("<b>[AUTEUR_REPONSE]</b> a répondu à ton sujet « [TITRE_SUJET] » :"), encadre("« [EXTRAIT_REPONSE] »"), bouton("Lire et répondre", L("SUJET_FORUM"))])
mail(id="39-changement-tarif", cat="Abonnement", marketing=False, quand="Au moins 30 jours avant toute hausse de prix ou changement des conditions (obligatoire)",
     objet="Information importante sur ton abonnement", pre="Ce qui change le [DATE_EFFET], et tes options.", sur="Information", titre="Ce qui change pour ton abonnement",
     corps=[para("[PRENOM], à partir du <b>[DATE_EFFET]</b>, [CHANGEMENT]."), para("Si tu ne souhaites pas continuer, tu peux résilier à tout moment avant cette date, sans frais."),
            bouton("Gérer mon abonnement", L("ABONNEMENT_GERER")), para('<span style="color:#6b6b66;font-size:14px">Les conditions générales mises à jour sont <a href="[LIEN_CGV]" style="color:#1f5fa8">disponibles ici</a>.</span>')])
mail(id="40-suppression-compte", cat="Compte", marketing=False, quand="À la suppression du compte (transactionnel, dernier e-mail envoyé)",
     objet="Ton compte echecs.com est supprimé", pre="Tes données personnelles ont été effacées.", sur="Ton compte", titre="Au revoir, [PRENOM].",
     corps=[para("Ton compte echecs.com et tes données personnelles ont été supprimés, comme tu l'as demandé. Tu ne recevras plus d'e-mails de notre part."),
            para("Si tu changes d'avis, tu pourras toujours créer un nouveau compte : les 6 leçons, le forum et le puzzle du jour resteront gratuits."),
            para('<span style="color:#6b6b66;font-size:14px">Tu n\'es pas à l\'origine de cette demande ? Écris-nous vite à [EMAIL_CONTACT].</span>')],
     sign="<b>L'équipe echecs.com</b>")

mail(id="41-parrainage", cat="Engagement", quand="À J+30 d'abonnement, puis après un module validé (au plus une fois par trimestre)", img="b-parrainage", alt="Invite un ami",
     objet="Invite un ami, et profitez-en tous les deux", pre="Ton ami reçoit [OFFRE_FILLEUL], toi [RECOMPENSE_PARRAIN].", sur="Parrainage", titre="Joue avec | tes amis.",
     corps=[para("[PRENOM], tu connais quelqu'un qui veut progresser aux échecs ? Partage ton lien : ton ami reçoit <b>[OFFRE_FILLEUL]</b>, et toi <b>[RECOMPENSE_PARRAIN]</b> dès qu'il s'abonne."),
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:24px 0"><tr><td align="center" style="border:2px dashed {C["jaune"]};border-radius:14px;background:#fff6c2;padding:18px">'
            f'<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.14em;text-transform:uppercase;color:{C["gris"]}">Ton code</div>'
            f'<div style="margin-top:6px;font-family:{SANS};font-weight:800;font-size:30px;letter-spacing:.12em;color:#111">[CODE_PARRAINAGE]</div></td></tr></table>',
            bouton("Partager mon lien", L("PARRAINAGE")), para('<span style="color:#6b6b66;font-size:14px">Pas de limite : chaque ami abonné te rapporte [RECOMPENSE_PARRAIN].</span>')])
mail(id="42-filleul-abonne", cat="Engagement", quand="Quand un ami parrainé s'abonne", img="b-filleul", alt="Ton ami est arrivé",
     objet="[PRENOM_FILLEUL] a rejoint l'Académie grâce à toi 🎉", pre="Ta récompense : [RECOMPENSE_PARRAIN].", sur="Parrainage", titre="Merci | pour l'invitation !",
     corps=[para("<b>[PRENOM_FILLEUL]</b> vient de s'abonner à l'Académie avec ton code. Comme promis, tu reçois <b>[RECOMPENSE_PARRAIN]</b> : c'est déjà sur ton compte."),
            para("Défiez-vous sur l'échiquier : les tournois en ligne sont ouverts à tous les niveaux."), bouton("Voir le prochain tournoi", L("TOURNOIS"))])

# ---------- 10. Cours de la semaine ----------
mail(id="43-cours-de-la-semaine", cat="Événements", quand="Chaque semaine, le lendemain du dernier cours (jours des cours à fixer)", alt="Les cours de la semaine",
     objet="Les cours de la semaine sont en vidéo 🎥", pre="[JOUR_COURS_1] : [THEME_COURS_1]. [JOUR_COURS_2] : [THEME_COURS_2].", sur="Cette semaine · [DATE_ENVOI]", titre="Les cours | de la semaine.",
     corps=[para("Bonjour [PRENOM], voici les cours de cette semaine, à revoir quand tu veux."),
            video("[URL_MINIATURE_COURS_1]", "[THEME_COURS_1]", "[JOUR_COURS_1] · avec [ANIMATEUR_COURS_1] · [DUREE_COURS_1]", L("COURS_1"), L("YOUTUBE_COURS_1")),
            video("[URL_MINIATURE_COURS_2]", "[THEME_COURS_2]", "[JOUR_COURS_2] · avec [ANIMATEUR_COURS_2] · [DUREE_COURS_2]", L("COURS_2"), L("YOUTUBE_COURS_2")),
            encadre("<b>La semaine prochaine :</b> [PROGRAMME_SEMAINE_PROCHAINE]."),
            bouton("Tous les cours en vidéo", L("COURS_VIDEOS")),
            para('<span style="color:#6b6b66;font-size:14px">Un seul cours cette semaine ? Supprime le second bloc vidéo.</span>')])
EXEMPLES.update({"TITRE_AUTEUR": "MI", "URL_PHOTO_AUTEUR": "img/coach-exemple.jpg", "NB_NOUVELLES_LECONS_MOIS": "24", "NB_VIDEOS_MOIS": "11", "NB_TOURNOIS_MOIS": "4", "DESCRIPTION_LECON_SUIVANTE": "Le Roi et le pion contre le Roi : la règle du carré et l'opposition, pour gagner ta première finale.", "NB_PUZZLES_REUSSIS": "6", "DUREE_EXTRAIT": "12 min", "URL_MINIATURE_EXTRAIT": "img/miniature-exemple.jpg", "NB_PUZZLES_ANNEE": "214", "NB_LECONS_GRATUITES_FAITES": "6", "NB_MESSAGES_FORUM": "17", "DUREES_CADEAU": "3, 6 ou 12 mois", "PRIX_CADEAU": "44,70 €", "PERIODE": "cet automne", "NB_NOUVELLES_LECONS_TRIMESTRE": "24", "NB_MASTERCLASSES_TRIMESTRE": "6", "NB_VIDEOS_TRIMESTRE": "12", "NB_TOURNOIS_TRIMESTRE": "9", "DATE_ENVOI": "19 novembre", "DATE_TOURNOI": "21 novembre", "HEURE_TOURNOI": "20 h", "NOM_TOURNOI": "Blitz de novembre", "SEMAINE": "du 9 au 15 nov.", "NB_JOURS_ACTIFS": "5", "NB_COURS_SUIVIS": "2", "NB_PARTIES": "14", "PARCOURS": "Objectif 1400", "PROGRESSION_PARCOURS": "62",
    "NB_NOUVELLES_LECONS": "6", "NB_VIDEOS_SEMAINE": "3", "NB_TOURNOIS_SEMAINE": "1"})
EXEMPLES.update({"THEME_COURS_1": "Les principes des débuts", "JOUR_COURS_1": "Mardi", "ANIMATEUR_COURS_1": "Fabien Libiszewski", "DUREE_COURS_1": "1 h",
    "THEME_COURS_2": "La fourchette de Cavalier", "JOUR_COURS_2": "Jeudi", "ANIMATEUR_COURS_2": "Sylvain Ravot", "DUREE_COURS_2": "55 min",
    "URL_MINIATURE_COURS_1": "img/miniature-exemple.jpg", "URL_MINIATURE_COURS_2": "img/miniature-exemple.jpg",
    "PROGRAMME_SEMAINE_PROCHAINE": "mardi, le mat du couloir ; jeudi, les finales de pions"})

# Titres en deux temps (« | » : la suite en italique bleu) et mascotte des e-mails sans image
TITRES = {
    "01-confirmation-adresse": "Plus qu'un clic, | [PRENOM] !", "02-bienvenue-compte-gratuit": "Ton compte | est prêt.",
    "03-mot-de-passe": "Nouveau | mot de passe.", "04-gratuit-j3-lecons": "Tu as essayé | une leçon ?", "05-gratuit-j7-offre": "Passe à | l'Académie complète.",
    "06-gratuit-j21-relance": "Tu hésites | encore ?", "07-confirmation-abonnement": "Tu fais partie | de l'Académie.", "08-paiement-refuse": "Ton paiement | n'est pas passé.",
    "09-paiement-recu": "Merci, | [PRENOM] !", "10-demarrage-j1-parcours": "Trouve | ton niveau.", "11-demarrage-j3-exercices": "10 minutes | par jour.",
    "12-demarrage-j6-masterclasses": "Apprends | des meilleurs.", "13-demarrage-j10-communaute": "Rejoins | la communauté.",
    "15-objectif-atteint": "Module validé. | Au suivant !", "16-serie-en-danger": "Garde | ta série !", "17-inactif-7-jours": "On reprend | là où tu en étais ?",
    "18-inactif-30-jours": "Tu nous | manques !", "21-replay-masterclass": "Tu l'as manquée ? | Le replay est là.", "24-resultats-tournoi": "Merci | d'avoir joué !",
    "25-sortie-revue": "Le n° [NUMERO] | est là.", "26-lettre-plusieurs-nouvelles": "Cette semaine | dans l'Académie.", "27-renouvellement-annuel-j30": "Ton année d'Académie | se termine bientôt.",
    "28-passage-annuel": "Passe | à l'annuel.", "29-fin-abonnement-j7": "Plus que 7 jours | d'accès.", "30-resiliation-confirmee": "C'est noté, | [PRENOM].",
    "31-reconquete-j30": "Reviens | quand tu veux.", "32-anniversaire": "Joyeux anniversaire | d'abonnement !", "33-paiement-abandonne": "Il ne manque | qu'une étape.",
    "34-changement-formule": "C'est | enregistré.", "35-carte-expire": "Ta carte | expire bientôt.", "36-inscription-tournoi": "C'est noté, | rendez-vous à [HEURE] !",
    "37-masterclass-reportee": "La masterclass | est déplacée.", "38-reponse-forum": "Nouvelle réponse | à ton sujet.", "39-changement-tarif": "Ce qui change | pour ton abonnement.",
    "40-suppression-compte": "Au revoir, | [PRENOM].", "20-rappel-masterclass": "Rendez-vous | à [HEURE] !", "19-annonce-masterclass": "Nouvelle | masterclass.", "23-annonce-tournoi": "À toi | de jouer !", "22-nouveau-cours": "Nouveau cours : | [TITRE_COURS]",
}
MASCOTTES = {}
ENTETES = {"01": "confirme", "03": "mot-de-passe", "08": "paiement", "09": "merci", "27": "renouvellement", "30": "resiliation", "33": "etape", "34": "enregistre", "35": "carte", "37": "deplace", "39": "information", "40": "aurevoir", "02": "bienvenue", "04": "lecons", "05": "offre", "06": "hesites", "07": "abonne", "10": "parcours", "11": "exercices", "12": "masterclasses",
           "13": "communaute", "14": "bilan", "44": "bilan-debut", "45": "bilan-pause", "15": "module", "16": "serie", "17": "reprendre", "18": "manque", "19": "masterclass", "20": "masterclass",
           "21": "replay", "22": "cours", "23": "tournoi", "24": "resultats", "25": "revue", "26": "nouvelles", "28": "annuel", "29": "fin", "31": "retour",
           "32": "anniversaire", "36": "inscription", "38": "forum", "43": "semaine", "46": "trimestre", "47": "lecons-finies", "48": "puzzles", "49": "extrait-offert", "50": "tournoi", "51": "un-an", "52": "cadeau"}

# Titres : le bandeau donne l'accroche, le titre l'information concrète (jamais la même phrase deux fois)
TITRES.update({
    "01-confirmation-adresse": "Confirme | ton adresse e-mail.", "03-mot-de-passe": "Un lien, | valable 1 heure.",
    "05-gratuit-j7-offre": "Tout débloquer, | dès 14,90 €.", "08-paiement-refuse": "Mets ta carte | à jour.", "09-paiement-recu": "Ton paiement | est bien reçu.",
    "11-demarrage-j3-exercices": "La régularité | avant tout.", "15-objectif-atteint": "Au suivant, | [PRENOM] !", "16-serie-en-danger": "Un exercice | suffit.",
    "17-inactif-3-semaines": "Ta leçon | t'attend.", "18-inactif-6-semaines": "Il y a du nouveau | dans l'Académie.", "19-annonce-masterclass": "Avec [COACH], | le [DATE].",
    "21-replay-masterclass": "Tu l'as manquée ? | Revois-la.", "22-nouveau-cours": "[TITRE_COURS], | par [AUTEUR].", "26-lettre-plusieurs-nouvelles": "À la une : | [TITRE_UNE].",
    "27-renouvellement-annuel-j30": "Renouvellement | le [DATE_RENOUVELLEMENT].", "28-passage-annuel": "Économise | 28,80 € par an.",
    "29-fin-abonnement-j7": "Ton accès s'arrête | le [DATE_FIN].", "30-resiliation-confirmee": "Accès ouvert | jusqu'au [DATE_FIN].",
    "31-reconquete-j30": "On reprend | ta progression ?", "32-anniversaire": "[DUREE_ABONNEMENT] | à nos côtés.", "33-paiement-abandonne": "Ton abonnement | t'attend.",
    "34-changement-formule": "Ta nouvelle formule : | [FORMULE].", "35-carte-expire": "Mets-la à jour | en 1 minute.", "38-reponse-forum": "[AUTEUR_REPONSE] | t'a répondu.",
    "39-changement-tarif": "À partir du | [DATE_EFFET].", "40-suppression-compte": "Ton compte | est supprimé.", "43-cours-de-la-semaine": "Tu les as manqués ? | Revois-les.",
    "44-bilan-mois-peu-actif": "Chaque séance | compte !", "45-inactif-1-semaine": "Une leçon | pour repartir ?", "07-confirmation-abonnement": "Tu as rejoint | l'Académie.", "20-rappel-masterclass": "Rendez-vous demain | à [HEURE] !", "49-gratuit-extrait-masterclass": "Progresse avec | [COACH].",
})
for e in E:
    if e["id"] == "26-lettre-plusieurs-nouvelles": e["sur"] = "La lettre · [DATE_ENVOI]"
