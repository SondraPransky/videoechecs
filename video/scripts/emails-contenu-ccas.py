# Contenu des e-mails des bénéficiaires des Activités Sociales de l'Énergie (CCAS) : plateforme d'échecs https://ccas.echecs.com/academy/
# Accès offert par le partenariat, sans abonnement ni paiement : aucune offre, aucun prix, aucune relance de paiement.
# Inclus : leçons et exercices, tournois en ligne, forum, cours en direct le lundi et le mercredi à 18 h 30 avec Eric et Florian.
# Exécuté par scripts/emails.py (python3 scripts/emails.py ccas), qui fournit les composants et le design.

# ---------- Réglages de la série ----------
EXPEDITEUR = "Europe Echecs · Activités Sociales"
AVATAR = "EE"
POURQUOI = "Tu reçois cet e-mail car tu as un compte sur la plateforme d'échecs des Activités Sociales de l'Énergie."
SIGNATURE = "À très vite sur l'échiquier,<br><b>L'équipe Europe Echecs</b><br><span style=\"color:#6b6b66;font-size:14px\">en partenariat avec les Activités Sociales de l'Énergie</span>"
ENTETE = f'''<tr><td class="m-pad" style="background:#fefefe;padding:18px 32px;border-bottom:1px solid {C['filet']}"><img src="{{IMG}}/logo.png" width="200" alt="Activités Sociales de l'Énergie · CCAS" style="display:block;border:0;width:200px;height:auto"></td></tr>'''
LIENS_PIED = [("La plateforme", "[LIEN_PLATEFORME]"), ("Cours en direct", "[LIEN_COURS_DIRECT]"), ("Tournois", "[LIEN_TOURNOIS]"), ("Forum", "[LIEN_FORUM]")]
RESEAUX = []
MENTION = "Europe Echecs, en partenariat avec les Activités Sociales de l'Énergie · [ADRESSE_POSTALE]"
DOC = ICI / "pack/EMAILS-CCAS.md"
DIRECT = "le <b>lundi</b> et le <b>mercredi</b> à <b>18 h 30</b>, avec <b>Eric</b> et <b>Florian</b>"

# ---------- 1. Compte ----------
mail(id="01-confirmation-adresse", cat="Compte", marketing=False, quand="À la création du compte (transactionnel)",
     objet="Confirme ton adresse e-mail", pre="Un clic, et ton compte est prêt.", sur="Ton compte", titre="Plus qu'un clic, | [PRENOM] !",
     corps=[para("Pour activer ton compte sur la plateforme d'échecs des Activités Sociales de l'Énergie, confirme simplement ton adresse e-mail."), bouton("Confirmer mon adresse", L("CONFIRMATION")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 48 heures. Tu n\'as pas créé de compte ? Ignore cet e-mail.</span>')])
mail(id="02-bienvenue", cat="Compte", quand="Juste après la confirmation de l'adresse", alt="La mascotte souhaite la bienvenue",
     objet="Bienvenue sur ta plateforme d'échecs, [PRENOM] ♟️", pre="Leçons, exercices, cours en direct, tournois : tout est offert.", sur="Bienvenue", titre="Ton compte | est prêt.",
     corps=[para("Bienvenue ! Grâce au partenariat entre Europe Echecs et les Activités Sociales de l'Énergie, tout est <b>offert</b> :"),
            liste(["<b>Les leçons et les exercices</b>, de l'initiation au niveau confirmé", f"<b>Les cours en direct</b>, {DIRECT}", "<b>Les tournois en ligne</b>, ouverts à tous les niveaux", "<b>Le forum</b>, pour poser tes questions et partager tes parties"]),
            bouton("Ma première leçon", L("PREMIERE_LECON")),
            para('<span style="color:#6b6b66;font-size:14px">Aucun abonnement, aucun moyen de paiement : ton accès est inclus dans tes Activités Sociales.</span>')])
mail(id="03-mot-de-passe", cat="Compte", marketing=False, quand="Sur demande de réinitialisation (transactionnel)",
     objet="Réinitialise ton mot de passe", pre="Ce lien est valable 1 heure.", sur="Ton compte", titre="Nouveau | mot de passe.",
     corps=[para("[PRENOM], tu as demandé à changer ton mot de passe. Clique ci-dessous pour en choisir un nouveau."), bouton("Choisir mon mot de passe", L("MOT_DE_PASSE")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 1 heure. Si tu n\'es pas à l\'origine de cette demande, ignore cet e-mail : ton mot de passe ne change pas.</span>')])

# ---------- 2. Démarrage ----------
mail(id="04-demarrage-j1-parcours", cat="Démarrage", quand="J+1 après l'inscription", alt="Ton parcours commence ici",
     objet="Par où commencer ? Ton parcours en 3 étapes", pre="De l'initiation au niveau confirmé : trouve ton niveau.", sur="Démarrage · 1/4", titre="Trouve | ton niveau.",
     corps=[para("[PRENOM], les leçons sont organisées en parcours : <b>Initiation</b>, <b>Objectif 1400</b>, <b>1600</b>, <b>1800</b>, puis <b>2000 et +</b>."),
            liste(['Choisis le parcours qui correspond à ton niveau, ou <a href="[LIEN_TEST_PLACEMENT]" style="color:#1f5fa8">passe le test de placement</a> (5 minutes)', "Fais une leçon : vidéo, cours, exercices, quiz", "Valide le quiz pour débloquer la suivante"]),
            bouton("Choisir mon parcours", L("PARCOURS"))])
mail(id="05-demarrage-j2-cours-direct", cat="Démarrage", quand="J+2 après l'inscription", alt="Les cours en direct",
     objet="Lundi et mercredi, 18 h 30 : les cours en direct", pre="Eric et Florian t'attendent, et tu peux poser tes questions.", sur="Démarrage · 2/4", titre="Les cours | en direct.",
     corps=[para(f"Deux fois par semaine, {DIRECT}, un cours en direct pour progresser ensemble."),
            liste(["Un thème à chaque cours : ouvertures, tactique, finales, parties commentées…", "Tu poses tes questions pendant le direct", "Tu l'as manqué ? Le cours reste disponible en vidéo"]),
            bouton("Voir le prochain cours", L("COURS_DIRECT"))])
mail(id="06-demarrage-j4-exercices", cat="Démarrage", quand="J+4 après l'inscription", alt="Les exercices",
     objet="10 minutes par jour suffisent", pre="Des exercices rangés par thème et par niveau.", sur="Démarrage · 3/4", titre="10 minutes | par jour.",
     corps=[para("La régularité fait plus que les longues séances. Chaque jour, quelques exercices à ton niveau : mat en 1, fourchette, clouage, finales…"),
            para("Ta <b>série de jours</b> s'affiche sur ton tableau de bord : essaie de ne pas la casser !"), bouton("Faire mes exercices du jour", L("EXERCICES"))])
mail(id="07-demarrage-j7-communaute", cat="Démarrage", quand="J+7 après l'inscription", alt="Joue, partage, mesure-toi",
     objet="Joue, partage, mesure-toi", pre="Tournois en ligne et forum : rejoins les autres joueurs.", sur="Démarrage · 4/4", titre="Rejoins | la communauté.",
     corps=[liste(["<b>Les tournois en ligne</b>, ouverts à tous les niveaux", "<b>Le forum</b>, pour poser tes questions à Eric, à Florian et aux autres joueurs", "<b>Tes parties</b> : rejoue-les et analyse-les"]),
            bouton("Voir le prochain tournoi", L("TOURNOIS"))])

# ---------- 3. Cours en direct ----------
mail(id="08-rappel-cours-direct", cat="Cours en direct", quand="Le lundi et le mercredi, vers 16 h (aux joueurs qui ont activé les rappels)", alt="Cours en direct à 18 h 30",
     objet="Ce soir 18 h 30 : [THEME_COURS]", pre="Cours en direct avec [ANIMATEUR]. Prépare tes questions !", sur="Rappel", titre="Rendez-vous | à 18 h 30 !",
     corps=[billet("[THEME_COURS]", [("Heure", "18 h 30 · Paris"), ("Avec", "[ANIMATEUR]"), ("Niveau", "[NIVEAU]")]),
            para("[DESCRIPTION_COURS]"), bouton("Rejoindre le direct", L("DIRECT")),
            para('<span style="color:#6b6b66;font-size:14px">Tu ne peux pas être là ? Le cours sera disponible en vidéo dans la semaine.</span>')])
mail(id="09-cours-de-la-semaine", cat="Cours en direct", quand="Chaque semaine, le jeudi (cours du lundi et du mercredi)", alt="Les cours de la semaine",
     objet="Les cours de la semaine : [THEME_LUNDI], [THEME_MERCREDI]", pre="Tu les as manqués ? Revois-les en vidéo.", sur="Cette semaine · [DATE]", titre="Les cours | de la semaine.",
     corps=[para("Bonjour [PRENOM], voici les deux cours en direct de cette semaine, à revoir quand tu veux."),
            video("[URL_MINIATURE_LUNDI]", "[THEME_LUNDI]", "Lundi · avec [ANIMATEUR_LUNDI] · [DUREE_LUNDI]", L("COURS_LUNDI"), L("YOUTUBE_LUNDI")),
            video("[URL_MINIATURE_MERCREDI]", "[THEME_MERCREDI]", "Mercredi · avec [ANIMATEUR_MERCREDI] · [DUREE_MERCREDI]", L("COURS_MERCREDI"), L("YOUTUBE_MERCREDI")),
            encadre("<b>La semaine prochaine :</b> lundi, [THEME_PROCHAIN_LUNDI] ; mercredi, [THEME_PROCHAIN_MERCREDI]. Rendez-vous à 18 h 30 !"),
            bouton("Tous les cours en vidéo", L("COURS_VIDEOS"))])
mail(id="10-cours-deplace", cat="Cours en direct", marketing=False, quand="Si un cours est déplacé ou annulé (à tous les joueurs qui ont activé les rappels)",
     objet="Cours du [DATE] déplacé au [NOUVELLE_DATE]", pre="[THEME_COURS], avec [ANIMATEUR] : la nouvelle date.", sur="Information", titre="Le cours | est déplacé.",
     corps=[para("[PRENOM], le cours <b>[THEME_COURS]</b> avec <b>[ANIMATEUR]</b>, prévu le [DATE], est déplacé."),
            billet("[THEME_COURS]", [("Heure", "[HEURE] · Paris"), ("Avec", "[ANIMATEUR]")], "[NOUVEAU_JOUR]", "[NOUVEAU_MOIS_COURT]"),
            para("Désolés pour ce changement. Le cours sera, comme toujours, disponible en vidéo."), bouton("Voir les prochains cours", L("COURS_DIRECT"))])

# ---------- 4. Tournois ----------
mail(id="11-annonce-tournoi", cat="Tournois", quand="5 jours avant un tournoi, rappel le jour J (même modèle)", alt="Tournoi en ligne",
     objet="Tournoi : [NOM_TOURNOI] le [DATE]", pre="Cadence [CADENCE], ouvert à tous les niveaux.", sur="Tournoi en ligne", titre="À toi | de jouer !",
     corps=[para("Mesure-toi aux autres joueurs de la plateforme !"), billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]"), ("Rondes", "[NB_RONDES]"), ("Niveau", "ouvert à tous")]),
            bouton("Je m'inscris", L("INSCRIPTION_TOURNOI")), para('<span style="color:#6b6b66;font-size:14px">Gratuit, comme tout le reste : il suffit de t\'inscrire.</span>')])
mail(id="12-inscription-tournoi", cat="Tournois", marketing=False, quand="À l'inscription à un tournoi (transactionnel)", alt="Inscription confirmée",
     objet="Inscription confirmée : [NOM_TOURNOI]", pre="Rendez-vous le [DATE] à [HEURE].", sur="Inscription confirmée", titre="C'est noté, | rendez-vous à [HEURE] !",
     corps=[billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]")]),
            para("Connecte-toi 10 minutes avant le début : les appariements de la 1re ronde sont publiés à [HEURE]."), bouton("Voir le tournoi", L("TOURNOI")),
            para('<span style="color:#6b6b66;font-size:14px">Un empêchement ? <a href="[LIEN_DESINSCRIPTION_TOURNOI]" style="color:#1f5fa8">Libère ta place</a>.</span>')])
mail(id="13-resultats-tournoi", cat="Tournois", quand="Le lendemain du tournoi, aux participants", alt="Résultats du tournoi",
     objet="Résultats : [NOM_TOURNOI]", pre="Tu termines [PLACE]ᵉ sur [NB_JOUEURS] : bravo !", sur="Résultats", titre="Merci | d'avoir joué !",
     corps=[para("[PRENOM], tu termines <b>[PLACE]<sup>e</sup> sur [NB_JOUEURS]</b> au <b>[NOM_TOURNOI]</b>, avec <b>[POINTS] points</b> sur [NB_RONDES]. Voici le podium :"),
            podium("[VAINQUEUR]", "[DEUXIEME]", "[TROISIEME]"), para("Revois tes parties : elles sont déjà dans ton espace, prêtes à être analysées."),
            bouton("Analyser mes parties", L("MES_PARTIES")), para('<a href="[LIEN_CLASSEMENT]" style="font-weight:800;color:#1f5fa8;text-decoration:none">Voir le classement complet&nbsp;&rarr;</a>')])

# ---------- 5. Lettre de la semaine (plusieurs nouvelles) ----------
mail(id="14-lettre-de-la-semaine", cat="Lettre de la semaine", quand="Les semaines où il y a 2 ou 3 nouvelles (remplace alors l'e-mail 09)", alt="Les nouvelles de la semaine",
     objet="Cette semaine : [TITRE_UNE]", pre="Le cours en vidéo, le prochain tournoi et les résultats du dernier.", sur="Les nouvelles · [DATE]", titre="Cette semaine | sur la plateforme.",
     corps=[para("Bonjour [PRENOM], voici ce qu'il ne fallait pas manquer cette semaine."),
            video("[URL_MINIATURE_LUNDI]", "Le cours : [THEME_LUNDI]", "Avec [ANIMATEUR_LUNDI] · [DUREE_LUNDI]", L("COURS_LUNDI"), L("YOUTUBE_LUNDI")),
            carte("b-tournoi", "Tournoi : [NOM_TOURNOI]", "Le [DATE] à [HEURE], cadence [CADENCE], ouvert à tous.", L("INSCRIPTION_TOURNOI"), "Je m'inscris"),
            carte("b-resultats", "Résultats : [NOM_TOURNOI_PRECEDENT]", "Bravo à [VAINQUEUR], [DEUXIEME] et [TROISIEME], sur le podium parmi [NB_JOUEURS] joueurs.", L("CLASSEMENT"), "Voir le classement"),
            para('<span style="color:#6b6b66;font-size:14px">Les blocs sont indépendants : garde ceux qui ont une actualité et supprime les autres.</span>')])

# ---------- 6. Engagement ----------
mail(id="15-bilan-mensuel", cat="Engagement", quand="Le 1er de chaque mois, si au moins une activité dans le mois", alt="Ton mois d'échecs",
     objet="[PRENOM], ton mois d'échecs en chiffres", pre="[NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo !", sur="Ton bilan de [MOIS]", titre="Ton mois | en chiffres.",
     corps=[tuiles([("[NB_LECONS]", "leçons terminées"), ("[NB_EXERCICES]", "exercices réussis ([TAUX_REUSSITE] %)"), ("[NB_COURS_SUIVIS]", "cours en direct suivis")]),
            para("Ton thème le plus travaillé : <b>[THEME_FORT]</b>. À renforcer : <b>[THEME_FAIBLE]</b>."), bouton("Travailler [THEME_FAIBLE]", L("THEME_FAIBLE"))])
mail(id="16-module-valide", cat="Engagement", quand="Quand le joueur valide un module ou un parcours", alt="Module validé",
     objet="Module validé : [MODULE] 🎉", pre="Une étape de plus vers ton objectif.", sur="Bravo", titre="Module validé. | Au suivant !",
     corps=[para("[PRENOM], tu viens de valider <b>[MODULE]</b>. Tu as passé [NB_LECONS_MODULE] leçons et réussi [NB_EXERCICES_MODULE] exercices."),
            para("Prochaine étape : <b>[MODULE_SUIVANT]</b>."), bouton("Module suivant", L("MODULE_SUIVANT"))])
mail(id="17-serie-en-danger", cat="Engagement", quand="Le soir, si la série de jours (≥ 5 jours) va s'interrompre", alt="Ta série de jours",
     objet="Ta série de [SERIE] jours va s'arrêter ⏳", pre="Un exercice suffit pour la garder.", sur="Ta série", titre="Garde | ta série !",
     corps=[para("[PRENOM], tu as joué [SERIE] jours d'affilée. Il te reste jusqu'à minuit pour la prolonger : <b>un seul exercice suffit</b>."), bouton("Faire un exercice", L("EXERCICE_DU_JOUR"))])
mail(id="18-reponse-forum", cat="Engagement", quand="Quand quelqu'un répond à un sujet du joueur (au plus 1 par jour, regroupé)", alt="Le forum",
     objet="[AUTEUR_REPONSE] t'a répondu sur le forum", pre="« [EXTRAIT_REPONSE] »", sur="Le forum", titre="Nouvelle réponse | à ton sujet.",
     corps=[para("<b>[AUTEUR_REPONSE]</b> a répondu à ton sujet « [TITRE_SUJET] » :"), encadre("« [EXTRAIT_REPONSE] »"), bouton("Lire et répondre", L("SUJET_FORUM"))])

# ---------- 7. Réactivation ----------
mail(id="19-inactif-7-jours", cat="Réactivation", quand="Sans connexion depuis 7 jours", alt="On reprend ensemble ?",
     objet="Ta prochaine leçon t'attend", pre="On reprend là où tu en étais ?", sur="On reprend ?", titre="On reprend | là où tu en étais ?",
     corps=[para("[PRENOM], ta dernière leçon était <b>[DERNIERE_LECON]</b>. La suivante, <b>[LECON_SUIVANTE]</b>, prend environ [DUREE_LECON]."),
            bouton("Reprendre ma leçon", L("LECON_SUIVANTE")), para(f'<span style="color:#6b6b66;font-size:14px">Et pour reprendre en douceur, rejoins un cours en direct, {DIRECT}.</span>')])
mail(id="20-inactif-30-jours", cat="Réactivation", quand="Sans connexion depuis 30 jours", alt="Tu nous manques",
     objet="Tu nous manques, [PRENOM]", pre="Voici ce qui est nouveau depuis ta dernière visite.", sur="Quoi de neuf", titre="Tu nous | manques !",
     corps=[para("Depuis ta dernière visite, il s'est passé des choses sur la plateforme :"), liste(["[NOUVEAUTE_1]", "[NOUVEAUTE_2]", "[NOUVEAUTE_3]"]),
            para("Ton accès est toujours ouvert, et toujours offert : reviens quand tu veux."), bouton("Revenir sur la plateforme", L("PLATEFORME"))])

# ---------- 8. Partenariat ----------
mail(id="21-echecs-en-famille", cat="Partenariat", quand="J+14 après l'inscription", alt="Les échecs en famille",
     objet="Et si tu jouais aux échecs en famille ?", pre="Tes proches bénéficiaires peuvent aussi créer leur compte.", sur="En famille", titre="Les échecs | en famille.",
     corps=[para("[PRENOM], les membres de ta famille qui bénéficient des Activités Sociales de l'Énergie peuvent, eux aussi, créer leur compte gratuitement."),
            liste(["Chacun avance à son rythme, avec son propre parcours", "Les cours en direct sont ouverts à tous les niveaux, même aux débutants", "Les tournois en ligne : de quoi organiser des défis à la maison"]),
            bouton("Partager le lien d'inscription", L("INSCRIPTION")),
            para('<span style="color:#6b6b66;font-size:14px">Le lien à transmettre : <a href="https://ccas.echecs.com/academy/" style="color:#1f5fa8">ccas.echecs.com/academy</a></span>')])
mail(id="22-questionnaire-satisfaction", cat="Partenariat", quand="J+30 après l'inscription (une seule fois)", alt="Ton avis compte",
     objet="2 minutes pour nous donner ton avis ?", pre="Ce qui te plaît, ce qui manque : on t'écoute.", sur="Ton avis", titre="Ton avis | compte.",
     corps=[para("[PRENOM], cela fait un mois que tu as rejoint la plateforme. Pour l'améliorer avec les Activités Sociales de l'Énergie, on aimerait savoir ce que tu en penses."),
            liste(["5 questions, 2 minutes", "Leçons, cours en direct, tournois : dis-nous ce qui te sert le plus", "Tes réponses restent anonymes"]),
            bouton("Donner mon avis", L("QUESTIONNAIRE"))])
mail(id="23-bilan-annuel", cat="Partenariat", quand="Un an après l'inscription", alt="Un an ensemble",
     objet="[PRENOM], ta première année d'échecs en chiffres", pre="[NB_LECONS_ANNEE] leçons, [NB_COURS_ANNEE] cours en direct : merci !", sur="Ton bilan de l'année", titre="Un an | ensemble !",
     corps=[para("Il y a un an, tu rejoignais la plateforme. Voici ton année :"),
            tuiles([("[NB_LECONS_ANNEE]", "leçons terminées"), ("[NB_EXERCICES_ANNEE]", "exercices réussis"), ("[NB_COURS_ANNEE]", "cours en direct suivis")]),
            para("Tu as validé <b>[NB_MODULES] modules</b> et joué <b>[NB_TOURNOIS_ANNEE] tournois</b>. Prochain objectif : <b>[MODULE_SUIVANT]</b>."),
            bouton("Continuer mon parcours", L("PARCOURS"))])

# ---------- 9. Compte (informations) ----------
mail(id="24-changement-acces", cat="Compte", marketing=False, quand="Au moins 30 jours avant tout changement de la plateforme ou des conditions d'accès",
     objet="Information importante sur ton accès", pre="Ce qui change le [DATE_EFFET].", sur="Information", titre="Ce qui change | pour ton accès.",
     corps=[para("[PRENOM], à partir du <b>[DATE_EFFET]</b>, [CHANGEMENT]."), para("Ton compte, ta progression et tes parties sont conservés."),
            bouton("En savoir plus", L("INFORMATION")), para('<span style="color:#6b6b66;font-size:14px">Une question ? Écris-nous à [EMAIL_CONTACT].</span>')])
mail(id="25-suppression-compte", cat="Compte", marketing=False, quand="À la suppression du compte (transactionnel, dernier e-mail envoyé)",
     objet="Ton compte est supprimé", pre="Tes données personnelles ont été effacées.", sur="Ton compte", titre="Au revoir, | [PRENOM].",
     corps=[para("Ton compte et tes données personnelles ont été supprimés, comme tu l'as demandé. Tu ne recevras plus d'e-mails de notre part."),
            para("Si tu changes d'avis, tu pourras toujours créer un nouveau compte : l'accès reste offert par les Activités Sociales de l'Énergie."),
            para('<span style="color:#6b6b66;font-size:14px">Tu n\'es pas à l\'origine de cette demande ? Écris-nous vite à [EMAIL_CONTACT].</span>')])

# Titres en deux temps : déjà dans chaque mail (« | »)
TITRES = {}
MASCOTTES = {"01-confirmation-adresse": "coucou", "03-mot-de-passe": "cherche", "10-cours-deplace": "pendule",
             "24-changement-acces": "pancarte", "25-suppression-compte": "coucou"}
ENTETES = {"02": "plateforme", "04": "parcours", "05": "direct", "06": "exercices", "07": "communaute", "08": "direct", "09": "semaine",
           "11": "tournoi", "12": "inscription", "13": "resultats", "14": "nouvelles", "15": "bilan", "16": "module", "17": "serie", "18": "forum",
           "19": "reprendre", "20": "manque", "21": "famille", "22": "avis", "23": "un-an"}
EXEMPLES.update({"THEME_COURS": "Les débuts ouverts : les principes", "ANIMATEUR": "Eric", "NIVEAU": "tous niveaux",
    "DESCRIPTION_COURS": "Développer ses pièces, contrôler le centre, roquer : les trois règles d'or des débuts, avec des parties d'exemple commentées en direct.",
    "THEME_LUNDI": "Les débuts ouverts : les principes", "ANIMATEUR_LUNDI": "Eric", "DUREE_LUNDI": "1 h",
    "THEME_MERCREDI": "La fourchette de Cavalier", "ANIMATEUR_MERCREDI": "Florian", "DUREE_MERCREDI": "55 min",
    "URL_MINIATURE_LUNDI": "img/miniature-exemple.jpg", "URL_MINIATURE_MERCREDI": "img/miniature-exemple.jpg",
    "THEME_PROCHAIN_LUNDI": "le mat du couloir", "THEME_PROCHAIN_MERCREDI": "les finales de pions", "DATE": "18 novembre",
    "NOM_TOURNOI": "Blitz du samedi", "NOM_TOURNOI_PRECEDENT": "Rapide du mercredi", "TITRE_UNE": "le Blitz du samedi",
    "NB_COURS_SUIVIS": "6", "NB_COURS_ANNEE": "58", "NB_TOURNOIS_ANNEE": "11", "HEURE": "18 h 30",
    "NOUVEAUTE_1": "8 cours en direct à revoir en vidéo", "NOUVEAUTE_2": "Un nouveau module sur les finales de Tours", "NOUVEAUTE_3": "Le Blitz du samedi, ouvert à tous",
    "CHANGEMENT": "les cours en direct du mercredi passeront à 19 h", "MOIS": "novembre"})
