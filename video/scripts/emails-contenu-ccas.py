# Contenu des e-mails des bénéficiaires des Activités Sociales de l'Énergie (CCAS) : plateforme d'échecs https://ccas.echecs.com/academy/
# Accès offert par le partenariat, sans abonnement ni paiement : aucune offre, aucun prix, aucune relance de paiement.
# Inclus : leçons et exercices, tournois en ligne, forum, cours en direct le lundi et le mercredi à 18 h 30 avec Éric et Florian.
# Exécuté par scripts/emails.py (python3 scripts/emails.py ccas), qui fournit les composants et le design.

# ---------- Réglages de la série ----------
C["em"] = "#0066cc"   # bleu du logo des Activités Sociales (surtitre, suite du titre)
EXPEDITEUR = "Europe Échecs · Activités Sociales"
AVATAR = '<img src="img/favicon.png" width="34" height="34" alt="" style="display:block;width:34px;height:34px;border-radius:50%;background:#ffffff">'
POURQUOI = "Tu reçois cet e-mail car tu as un compte sur la plateforme d'échecs des Activités Sociales de l'Énergie."
SIGNATURE = "À très vite sur l'échiquier,<br><b style=\"color:#0066cc\">Les Activités Sociales de l'Énergie</b><br><b>en partenariat avec Europe Échecs</b>"
ENTETE = f'''<tr><td class="m-pad" style="background:#fefefe;padding:24px 32px;border-bottom:1px solid {C['filet']}"><img src="{{IMG}}/logo.png" width="280" alt="activités sociales de l'énergie" style="display:block;border:0;width:280px;max-width:100%;height:auto"></td></tr>'''
LIENS_PIED = [("La plateforme", "[LIEN_PLATEFORME]"), ("Cours en direct", "[LIEN_COURS_DIRECT]"), ("Tournois", "[LIEN_TOURNOIS]"), ("Forum", "[LIEN_FORUM]")]
RESEAUX = []
MENTION = "Europe Échecs, en partenariat avec les Activités Sociales de l'Énergie · [ADRESSE_POSTALE]"
DOC = ICI / "pack/EMAILS-CCAS.md"
DIRECT = "le <b>lundi</b> et le <b>mercredi</b> à <b>18 h 30</b>, avec <b>Éric</b> et <b>Florian</b>"

# ---------- 1. Compte ----------
mail(id="01-confirmation-adresse", cat="Compte", marketing=False, quand="À la création du compte (transactionnel)",
     objet="Confirme ton adresse e-mail", pre="Un clic, et ton compte est prêt.", sur="Ton compte", titre="Plus qu'un clic, | [PSEUDO] !",
     corps=[para("Pour activer ton compte sur la plateforme d'échecs des Activités Sociales de l'Énergie, confirme simplement ton adresse e-mail."), bouton("Confirmer mon adresse", L("CONFIRMATION")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 48 heures. Tu n\'as pas créé de compte ? Ignore cet e-mail.</span>')])
mail(id="02-bienvenue", cat="Compte", quand="Juste après la confirmation de l'adresse", alt="La mascotte souhaite la bienvenue",
     objet="Bienvenue sur ta plateforme d'échecs, [PSEUDO] ♟️", pre="Parcours Initiation, cours en direct, tournois : tout est offert.", sur="Bienvenue", titre="Ton compte | est prêt.",
     corps=[para("Bienvenue ! Grâce au partenariat entre Europe Échecs et les Activités Sociales de l'Énergie, tout est <b>offert</b> :"),
            liste(["<b>Le parcours Initiation</b> : les leçons et les exercices pour bien démarrer", f"<b>Les cours en direct</b>, {DIRECT}", "<b>Les tournois en ligne</b>, ouverts à tous les niveaux", "<b>Le forum</b>, pour poser tes questions et partager tes parties"]),
            bouton("Ma première leçon", L("PREMIERE_LECON")),
            para('<span style="color:#6b6b66;font-size:14px">Aucun abonnement, aucun moyen de paiement : ton accès est inclus dans tes Activités Sociales.</span>')])
mail(id="03-mot-de-passe", cat="Compte", marketing=False, quand="Sur demande de réinitialisation (transactionnel)",
     objet="Réinitialise ton mot de passe", pre="Ce lien est valable 1 heure.", sur="Ton compte", titre="Nouveau | mot de passe.",
     corps=[para("[PSEUDO], tu as demandé à changer ton mot de passe. Clique ci-dessous pour en choisir un nouveau."), bouton("Choisir mon mot de passe", L("MOT_DE_PASSE")),
            para('<span style="color:#6b6b66;font-size:14px">Ce lien est valable 1 heure. Si tu n\'es pas à l\'origine de cette demande, ignore cet e-mail : ton mot de passe ne change pas.</span>')])

# ---------- 2. Démarrage ----------
mail(id="04-demarrage-j1-cours-direct", cat="Démarrage", quand="J+1 après l'inscription", alt="Les cours en direct",
     objet="Lundi et mercredi, 18 h 30 : les cours en direct", pre="Éric et Florian t'attendent, et tu peux poser tes questions.", sur="Cours en direct", titre="Les cours | en direct.",
     corps=[para(f"Deux fois par semaine, {DIRECT}, un cours en direct pour progresser ensemble."),
            liste(["Un thème à chaque cours : les débuts, la tactique, les mats, les finales, des parties commentées…", "En visioconférence : un clic sur le lien, et tu es dans le cours", "Tu poses tes questions en direct, à l'oral ou par écrit : une occasion à ne pas rater !", "Tu l'as manqué ? Le cours reste disponible en vidéo"]),
            bouton("Voir le prochain cours", L("COURS_DIRECT"))])
mail(id="05-demarrage-j3-exercices", cat="Démarrage", quand="J+3 après l'inscription", alt="Les exercices",
     objet="10 minutes par jour suffisent", pre="Des exercices rangés par thème, pour bien démarrer.", sur="Exercices", titre="10 minutes | par jour.",
     corps=[para("La régularité fait plus que les longues séances. Chaque jour, quelques exercices à ton niveau : mat en 1, fourchette, clouage, finales…"),
            para("Le bon rythme : <b>un peu chaque jour</b>, plutôt que beaucoup une fois par semaine."), bouton("Faire mes exercices du jour", L("EXERCICES"))])
mail(id="06-demarrage-j6-communaute", cat="Démarrage", quand="J+6 après l'inscription", alt="Joue, partage, mesure-toi",
     objet="Joue, partage, mesure-toi", pre="Tournois en ligne et forum : rejoins les autres joueurs.", sur="Communauté", titre="Rejoins | la communauté.",
     corps=[para("La plateforme est aussi une communauté de joueurs, unis pour progresser ensemble !"), liste(["<b>Les tournois en ligne</b>, ouverts à tous les niveaux", "<b>Le forum</b>, pour poser tes questions à Éric, à Florian et aux autres joueurs", "<b>Les cours en direct</b>, pour progresser ensemble le lundi et le mercredi"]),
            bouton("Voir le prochain tournoi", L("TOURNOIS"))])

# ---------- 3. Cours en direct ----------
mail(id="07-programme-de-la-semaine", cat="Cours en direct", quand="Chaque lundi vers 10 h, à tous (les deux cours de la semaine)", alt="Cours en direct, lundi et mercredi à 18 h 30",
     objet="Cette semaine : 2 cours en direct à 18 h 30", pre="Lundi : [THEME_LUNDI]. Mercredi : [THEME_MERCREDI].", sur="Cette semaine", titre="Tes deux cours | de la semaine.",
     corps=[para("[PSEUDO], voici le programme des cours en direct de cette semaine, en visioconférence :"),
            billet("[THEME_LUNDI]", [("Lundi", "18 h 30 · Paris"), ("Avec", "[ANIMATEUR_LUNDI]")], "[JOUR_LUNDI]", "[MOIS_COURT]"),
            billet("[THEME_MERCREDI]", [("Mercredi", "18 h 30 · Paris"), ("Avec", "[ANIMATEUR_MERCREDI]")], "[JOUR_MERCREDI]", "[MOIS_COURT]"),
            bouton("Rejoindre le cours", L("DIRECT")),
            para('<span style="color:#6b6b66;font-size:14px">Le même lien sert pour les deux cours : garde cet e-mail et connecte-toi quelques minutes avant 18 h 30 pour vérifier ton son. Tu ne peux pas être là ? Le cours sera disponible en vidéo jeudi.</span>')])
mail(id="08-cours-de-la-semaine", cat="Cours en direct", quand="Chaque semaine, le jeudi (cours du lundi et du mercredi)", alt="Les cours de la semaine",
     objet="Les cours de la semaine sont en vidéo 🎥", pre="Lundi : [THEME_LUNDI]. Mercredi : [THEME_MERCREDI].", sur="Cette semaine · [DATE_ENVOI]", titre="Les cours | de la semaine.",
     corps=[para("Bonjour [PSEUDO], voici les deux cours en direct de cette semaine, à revoir quand tu veux."),
            video("[URL_MINIATURE_LUNDI]", "[THEME_LUNDI]", "Lundi · avec [ANIMATEUR_LUNDI] · [DUREE_LUNDI]", L("COURS_LUNDI"), L("YOUTUBE_LUNDI")),
            video("[URL_MINIATURE_MERCREDI]", "[THEME_MERCREDI]", "Mercredi · avec [ANIMATEUR_MERCREDI] · [DUREE_MERCREDI]", L("COURS_MERCREDI"), L("YOUTUBE_MERCREDI")),
            encadre("<b>La semaine prochaine :</b> lundi, [THEME_PROCHAIN_LUNDI] ; mercredi, [THEME_PROCHAIN_MERCREDI]. Rendez-vous à 18 h 30 !"),
            bouton("Tous les cours en vidéo", L("COURS_VIDEOS"))])
mail(id="09-cours-deplace", cat="Cours en direct", marketing=False, quand="Si un cours est déplacé ou annulé (à tous les joueurs qui ont activé les rappels)",
     objet="Cours du [DATE] déplacé au [NOUVELLE_DATE]", pre="[THEME_COURS], avec [ANIMATEUR] : la nouvelle date.", sur="Information", titre="Le cours | est déplacé.",
     corps=[para("[PSEUDO], le cours <b>[THEME_COURS]</b> avec <b>[ANIMATEUR]</b>, prévu le [DATE], est déplacé."),
            billet("[THEME_COURS]", [("Heure", "[HEURE] · Paris"), ("Avec", "[ANIMATEUR]"), ("Où", "en visioconférence, même lien")], "[NOUVEAU_JOUR]", "[NOUVEAU_MOIS_COURT]"),
            para("Désolés pour ce changement. Le cours sera, comme toujours, disponible en vidéo."), bouton("Voir les prochains cours", L("COURS_DIRECT"))])

mail(id="26-pause-vacances", cat="Cours en direct", quand="Le dernier jour de cours avant une pause (vacances scolaires, été, fin d'année)", alt="Pause pendant les vacances",
     exemples={"DATE_DEBUT_PAUSE": "21 décembre", "DATE_FIN_PAUSE": "4 janvier", "DATE_REPRISE": "lundi 5 janvier"},
     objet="Pas de cours en direct jusqu'au [DATE_REPRISE] ☀️", pre="La plateforme reste ouverte : cours en vidéo, leçons, exercices.", sur="Vacances", titre="Reprise le | [DATE_REPRISE].",
     corps=[para("[PSEUDO], les cours en direct font une pause pendant les vacances :"),
            encadre("<b>Pas de cours du [DATE_DEBUT_PAUSE] au [DATE_FIN_PAUSE].</b><br>Reprise le <b>[DATE_REPRISE] à 18 h 30</b>, avec Éric et Florian."),
            para("Pendant ce temps, la plateforme reste ouverte :"),
            liste(["<b>Les cours en vidéo</b>, pour revoir ceux que tu as manqués", "<b>Le parcours Initiation</b> : quelques exercices par jour pour garder la main", "<b>Le forum</b>, pour échanger avec les autres joueurs"]),
            bouton("Revoir les cours en vidéo", L("COURS_VIDEOS"))],
     sign="Bonnes vacances !<br><b style=\"color:#0066cc\">Les Activités Sociales de l'Énergie</b><br><b>en partenariat avec Europe Échecs</b>")
mail(id="27-reprise-cours", cat="Cours en direct", quand="Le vendredi avant la reprise des cours en direct", alt="C'est reparti",
     exemples={"JOUR_LUNDI": "5", "JOUR_MERCREDI": "7", "MOIS_COURT": "janv.", "THEME_LUNDI": "Les mats élémentaires", "THEME_MERCREDI": "Le clouage"},
     objet="Les cours en direct reprennent lundi à 18 h 30 !", pre="Au programme : [THEME_LUNDI] avec [ANIMATEUR_LUNDI].", sur="Reprise des cours", titre="Rendez-vous lundi | à 18 h 30.",
     corps=[para("[PSEUDO], les vacances sont finies : les cours en direct reprennent la semaine prochaine, en visioconférence :"),
            billet("[THEME_LUNDI]", [("Lundi", "18 h 30 · Paris"), ("Avec", "[ANIMATEUR_LUNDI]")], "[JOUR_LUNDI]", "[MOIS_COURT]"),
            billet("[THEME_MERCREDI]", [("Mercredi", "18 h 30 · Paris"), ("Avec", "[ANIMATEUR_MERCREDI]")], "[JOUR_MERCREDI]", "[MOIS_COURT]"),
            bouton("Rejoindre le cours", L("DIRECT")),
            para('<span style="color:#6b6b66;font-size:14px">Pour te remettre dans le bain d\'ici là : une leçon du parcours Initiation, <b>[LECON_SUIVANTE]</b>, environ [DUREE_LECON].</span>')])

# ---------- 4. Tournois ----------
mail(id="10-annonce-tournoi", exemples={"DATE": "21 novembre", "JOUR": "21", "HEURE": "20 h"}, cat="Tournois", quand="5 jours avant un tournoi, rappel le jour J (même modèle)", alt="Tournoi en ligne",
     objet="Tournoi : [NOM_TOURNOI] le [DATE]", pre="Cadence [CADENCE], ouvert à tous les niveaux.", sur="Tournoi en ligne", titre="À toi | de jouer !",
     corps=[para("Mesure-toi aux autres joueurs de la plateforme et mets en pratique ce que tu as appris !"), billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]"), ("Rondes", "[NB_RONDES]"), ("Niveau", "ouvert à tous")]),
            bouton("Je m'inscris", L("INSCRIPTION_TOURNOI")), para('<span style="color:#6b6b66;font-size:14px">Gratuit, comme tout le reste : il suffit de t\'inscrire.</span>')])
mail(id="11-inscription-tournoi", exemples={"DATE": "21 novembre", "JOUR": "21", "HEURE": "20 h"}, cat="Tournois", marketing=False, quand="À l'inscription à un tournoi (transactionnel)", alt="Inscription confirmée",
     objet="Inscription confirmée : [NOM_TOURNOI]", pre="Rendez-vous le [DATE] à [HEURE].", sur="Inscription confirmée", titre="C'est noté, | rendez-vous à [HEURE] !",
     corps=[billet("[NOM_TOURNOI]", [("Heure", "[HEURE] · Paris"), ("Cadence", "[CADENCE]")]),
            para("Connecte-toi 10 minutes avant le début : les appariements de la 1re ronde sont publiés à [HEURE]."), bouton("Voir le tournoi", L("TOURNOI")),
            para('<span style="color:#6b6b66;font-size:14px">Un empêchement ? <a href="[LIEN_DESINSCRIPTION_TOURNOI]" style="color:#1f5fa8">Libère ta place</a>.</span>')])
mail(id="12-resultats-tournoi", cat="Tournois", quand="Le lendemain du tournoi, aux participants (ajouter « Analyser mes parties » quand les parties seront sauvegardées)", alt="Résultats du tournoi",
     objet="Résultats : [NOM_TOURNOI]", pre="Tu termines [PLACE]ᵉ sur [NB_JOUEURS] : bravo !", sur="Résultats", titre="Merci | d'avoir joué !",
     corps=[para("[PSEUDO], tu termines <b>[PLACE]<sup>e</sup> sur [NB_JOUEURS]</b> au <b>[NOM_TOURNOI]</b>, avec <b>[POINTS] points</b> sur [NB_RONDES]. Voici le podium :"),
            podium("[VAINQUEUR]", "[DEUXIEME]", "[TROISIEME]"), para("Bravo pour ta participation ! Le prochain tournoi est déjà au programme."),
            bouton("Voir le classement complet", L("CLASSEMENT")), para('<a href="[LIEN_TOURNOIS]" style="font-weight:800;color:#1f5fa8;text-decoration:none">Voir le prochain tournoi&nbsp;&rarr;</a>')])

# ---------- 5. Lettre de la semaine (plusieurs nouvelles) ----------
mail(id="13-lettre-de-la-semaine", exemples={"DATE": "21 novembre", "JOUR": "21", "HEURE": "20 h"}, cat="Lettre de la semaine", quand="Les semaines où il y a 2 ou 3 nouvelles (remplace alors l'e-mail 08)", alt="Les nouvelles de la semaine",
     objet="Cette semaine : [TITRE_UNE]", pre="Le cours en vidéo, le prochain tournoi et les résultats du dernier.", sur="Les nouvelles · [DATE]", titre="Cette semaine | sur la plateforme.",
     corps=[para("Bonjour [PSEUDO], voici ce qu'il ne fallait pas manquer cette semaine."),
            video("[URL_MINIATURE_LUNDI]", "Le cours : [THEME_LUNDI]", "Avec [ANIMATEUR_LUNDI] · [DUREE_LUNDI]", L("COURS_LUNDI"), L("YOUTUBE_LUNDI")),
            carte("b-tournoi", "Tournoi : [NOM_TOURNOI]", "Le [DATE] à [HEURE], cadence [CADENCE], ouvert à tous.", L("INSCRIPTION_TOURNOI"), "Je m'inscris"),
            carte("b-resultats", "Résultats : [NOM_TOURNOI_PRECEDENT]", "Bravo à [VAINQUEUR], [DEUXIEME] et [TROISIEME], sur le podium parmi [NB_JOUEURS] joueurs.", L("CLASSEMENT"), "Voir le classement"),
            para('<span style="color:#6b6b66;font-size:14px">Les blocs sont indépendants : garde ceux qui ont une actualité et supprime les autres.</span>')])

# ---------- 6. Engagement ----------
# Bilan du mois (actif, peu actif) : le 1er du mois ; sans activité : relance à 1 semaine (27), puis 3 semaines (17) et 6 semaines (18) ; à activer avec les statistiques
NOUV_MOIS = nouveautes("Ce mois-ci sur la plateforme", [("Cours en direct", "[NB_COURS_MOIS]"), ("Nouveaux exercices", "[NB_NOUVEAUX_EXERCICES_MOIS]"), ("Tournois organisés", "[NB_TOURNOIS_MOIS]")])
NOUV_CCAS = nouveautes("Cette semaine sur la plateforme", [("Cours en direct", "[NB_COURS_SEMAINE]"), ("Nouveaux exercices", "[NB_NOUVEAUX_EXERCICES]"), ("Tournois organisés", "[NB_TOURNOIS_SEMAINE]")])
mail(id="14-bilan-mois-actif", cat="Bilan du mois", quand="Le 1er du mois, si au moins 8 jours d'entraînement dans le mois écoulé (à activer avec les statistiques)", alt="Ton mois d'échecs",
     exemples={"NB_JOURS_ACTIFS": "15", "NB_COURS_SUIVIS": "7", "NB_LECONS": "22", "NB_EXERCICES": "318", "NB_PARTIES": "35", "SERIE": "9", "PROGRESSION_PARCOURS": "62"},
     objet="[PSEUDO], ton mois d'échecs en chiffres 🔥", pre="[NB_JOURS_ACTIFS] jours d'entraînement, [NB_LECONS] leçons, [NB_EXERCICES] exercices : bravo !", sur="Ton bilan de [MOIS]", titre="[NB_JOURS_ACTIFS] jours d'entraînement, | bravo !",
     corps=[para("[PSEUDO], voici ton bilan du mois :"),
            tuiles([("[NB_COURS_SUIVIS]", "Cours en direct"), ("[NB_LECONS]", "Leçons"), ("[NB_EXERCICES]", "Exercices réussis")]),
            tuiles([("[NB_PARTIES]", "Parties jouées"), ("[SERIE]", "Jours de série"), ("[TAUX_REUSSITE]&nbsp;%", "Réussite")]),
            progression("Parcours Initiation", "[PROGRESSION_PARCOURS]"),
            encadre("<b>La régularité paie !</b> Ton point fort ce mois-ci : <b>[THEME_FORT]</b>. À travailler : <b>[THEME_FAIBLE]</b>."),
            NOUV_MOIS, bouton("Continuer l'Initiation", L("PARCOURS"))])
mail(id="24-bilan-mois-peu-actif", cat="Bilan du mois", quand="Le 1er du mois, si 1 à 7 jours d'entraînement dans le mois écoulé (à activer avec les statistiques)", alt="Bon début, on continue ?",
     exemples={"NB_JOURS_ACTIFS": "4", "NB_LECONS": "6", "NB_EXERCICES": "52", "NB_PARTIES": "5", "PROGRESSION_PARCOURS": "34"},
     objet="[PSEUDO], ton mois d'échecs : on continue ?", pre="[NB_LECONS] leçons ce mois-ci. 10 minutes de plus par semaine, et ça change tout.", sur="Ton bilan de [MOIS]", titre="Chaque séance | compte !",
     corps=[para("Jours d'entraînement ce mois-ci : <b>[NB_JOURS_ACTIFS]</b>. Voici ton bilan :"),
            tuiles([("[NB_LECONS]", "Leçons"), ("[NB_EXERCICES]", "Exercices réussis"), ("[NB_PARTIES]", "Parties jouées")]),
            progression("Parcours Initiation", "[PROGRESSION_PARCOURS]"),
            encadre("<b>Le secret pour progresser :</b> 10 minutes, 3 fois par semaine. Ta prochaine leçon, <b>[LECON_SUIVANTE]</b>, prend environ [DUREE_LECON]. Et lundi à 18 h 30, rejoins le cours en direct !"),
            NOUV_MOIS, bouton("Reprendre ma leçon", L("LECON_SUIVANTE"))])
mail(id="25-inactif-1-semaine", cat="Réactivation", quand="Après 7 jours sans activité (une seule fois par période d'inactivité ; puis 17 à 3 semaines et 18 à 6 semaines ; à activer avec les statistiques)", alt="Ta place t'attend",
     exemples={"PROGRESSION_PARCOURS": "34"},
     objet="Ce que tu as manqué cette semaine 👀", pre="Cours en direct, nouveaux exercices, tournoi : ta place t'attend.", sur="On reprend ?", titre="Ta place | t'attend.",
     corps=[para("Pas d'échecs cette semaine ? Ça arrive à tout le monde. Voici ce qui s'est passé sur la plateforme :"),
            NOUV_CCAS,
            progression("Parcours Initiation", "[PROGRESSION_PARCOURS]"),
            encadre("<b>Pour repartir en douceur :</b> rejoins le cours en direct de lundi, à 18 h 30 avec [ANIMATEUR_LUNDI], ou fais une seule leçon, <b>[LECON_SUIVANTE]</b> (environ [DUREE_LECON])."),
            bouton("Faire une leçon", L("LECON_SUIVANTE")),
            para('<span style="color:#6b6b66;font-size:14px">Ton accès est toujours ouvert, et toujours offert.</span>')])
mail(id="15-serie-en-danger", cat="Engagement", quand="Le soir, si la série de jours (≥ 5 jours) va s'interrompre (au plus une fois toutes les 4 semaines par joueur ; à activer avec la série de jours)", alt="Ta série de jours",
     objet="Ta série de [SERIE] jours va s'arrêter ⏳", pre="Un exercice suffit pour la garder.", sur="Ta série", titre="Garde | ta série !",
     corps=[para("[PSEUDO], tu as joué [SERIE] jours d'affilée. Il te reste jusqu'à minuit pour la prolonger : <b>un seul exercice suffit</b>."), bouton("Faire un exercice", L("EXERCICE_DU_JOUR"))])
mail(id="16-reponse-forum", cat="Engagement", quand="Quand quelqu'un répond à un sujet du joueur (au plus 1 par jour, regroupé)", alt="Le forum",
     objet="[AUTEUR_REPONSE] t'a répondu sur le forum", pre="« [EXTRAIT_REPONSE] »", sur="Le forum", titre="Nouvelle réponse | à ton sujet.",
     corps=[para("<b>[AUTEUR_REPONSE]</b> a répondu à ton sujet « [TITRE_SUJET] » :"), encadre("« [EXTRAIT_REPONSE] »"), bouton("Lire et répondre", L("SUJET_FORUM"))])

# ---------- 7. Réactivation ----------
mail(id="17-inactif-3-semaines", cat="Réactivation", quand="Après 3 semaines sans activité (une seule fois par période d'inactivité ; le 25 est parti à 1 semaine)", alt="On reprend ensemble ?",
     objet="Ta progression t'attend, [PSEUDO]", pre="3 semaines sans échecs : on reprend avant de perdre le fil ?", sur="On reprend ?", titre="On reprend | là où tu en étais ?",
     corps=[para("[PSEUDO], 3 semaines sans échecs : c'est le bon moment pour reprendre, avant de perdre le fil."), para("Ta dernière leçon était <b>[DERNIERE_LECON]</b>. La suivante, <b>[LECON_SUIVANTE]</b>, prend environ [DUREE_LECON]."),
            bouton("Reprendre ma leçon", L("LECON_SUIVANTE")), para(f'<span style="color:#6b6b66;font-size:14px">Et pour reprendre en douceur, rejoins un cours en direct, {DIRECT}.</span>')])
mail(id="18-inactif-6-semaines", cat="Réactivation", quand="Après 6 semaines sans activité (une seule fois par période d'inactivité ; dernière relance)", alt="Tu nous manques",
     objet="Tu nous manques, [PSEUDO]", pre="Voici ce qui est nouveau depuis ta dernière visite.", sur="Quoi de neuf", titre="Tu nous | manques !",
     corps=[para("Depuis ta dernière visite, il s'est passé des choses sur la plateforme :"), liste(["[NOUVEAUTE_1]", "[NOUVEAUTE_2]", "[NOUVEAUTE_3]"]),
            para("Ton accès est toujours ouvert, et toujours offert : ce serait dommage d'arrêter ta progression maintenant !"), bouton("Revenir sur la plateforme", L("PLATEFORME"))])

# ---------- 8. Partenariat ----------
mail(id="19-echecs-en-famille", cat="Partenariat", quand="J+14 après l'inscription", alt="Les échecs en famille",
     objet="Et si tu jouais aux échecs en famille ?", pre="Tes ayants droit peuvent aussi créer leur compte, gratuitement.", sur="En famille", titre="Les échecs | en famille.",
     corps=[para("[PSEUDO], tes ayants droit (conjoint, enfants…) bénéficient eux aussi des Activités Sociales de l'Énergie : ils peuvent créer leur propre compte, gratuitement."),
            liste(["Chacun avance à son rythme dans le parcours Initiation", "Les cours en direct sont ouverts à tous les niveaux, même aux débutants", "Les tournois en ligne : de quoi organiser des défis à la maison"]),
            bouton("Partager le lien d'inscription", L("INSCRIPTION")),
            para('<span style="color:#6b6b66;font-size:14px">Le lien à transmettre : <a href="https://ccas.echecs.com/academy/" style="color:#1f5fa8">ccas.echecs.com/academy</a></span>')])
mail(id="20-questionnaire-satisfaction", cat="Partenariat", quand="J+30 après l'inscription (une seule fois)", alt="Ton avis compte",
     objet="2 minutes pour nous donner ton avis ?", pre="Ce qui te plaît, ce qui manque : on t'écoute.", sur="Ton avis", titre="Ton avis | compte.",
     corps=[para("[PSEUDO], cela fait un mois que tu as rejoint la plateforme. Pour l'améliorer avec les Activités Sociales de l'Énergie, on aimerait savoir ce que tu en penses."),
            liste(["5 questions, 2 minutes", "Leçons, cours en direct, tournois : dis-nous ce qui te sert le plus", "Tes réponses restent anonymes"]),
            bouton("Donner mon avis", L("QUESTIONNAIRE"))])
mail(id="21-bilan-annuel", cat="Partenariat", quand="Un an après l'inscription (à activer avec les statistiques)", alt="Un an ensemble",
     objet="[PSEUDO], ta première année d'échecs en chiffres", pre="[NB_LECONS_ANNEE] leçons, [NB_COURS_ANNEE] cours en direct : merci !", sur="Ton bilan de l'année", titre="Un an | ensemble !",
     corps=[para("Il y a un an, tu rejoignais la plateforme. Merci, et bravo : ta progression se poursuit ! Voici le bilan de ton année :"),
            tuiles([("[NB_LECONS_ANNEE]", "leçons terminées"), ("[NB_EXERCICES_ANNEE]", "exercices réussis"), ("[NB_COURS_ANNEE]", "cours en direct suivis")]),
            para("Tu as aussi joué <b>[NB_TOURNOIS_ANNEE] tournois</b>. Merci d'avoir fait vivre la plateforme, et rendez-vous lundi à 18 h 30 pour le prochain cours !"),
            bouton("Voir les prochains cours", L("COURS_DIRECT"))])

# ---------- 9. Compte (informations) ----------
mail(id="22-changement-acces", cat="Compte", marketing=False, quand="Au moins 30 jours avant tout changement de la plateforme ou des conditions d'accès",
     objet="Information importante sur ton accès", pre="Ce qui change le [DATE_EFFET].", sur="Information", titre="Ce qui change | pour ton accès.",
     corps=[para("[PSEUDO], à partir du <b>[DATE_EFFET]</b>, [CHANGEMENT]."), para("Ton compte et ta progression sont conservés."),
            bouton("En savoir plus", L("INFORMATION")), para('<span style="color:#6b6b66;font-size:14px">Une question ? Écris-nous à [EMAIL_CONTACT].</span>')])
mail(id="23-suppression-compte", cat="Compte", marketing=False, quand="À la suppression du compte (transactionnel, dernier e-mail envoyé)",
     objet="Ton compte est supprimé", pre="Tes données personnelles ont été effacées.", sur="Ton compte", titre="Au revoir, | [PSEUDO].",
     corps=[para("Ton compte et tes données personnelles ont été supprimés, comme tu l'as demandé. Tu ne recevras plus d'e-mails de notre part."),
            para("Si tu changes d'avis, tu pourras toujours créer un nouveau compte : l'accès reste offert par les Activités Sociales de l'Énergie."),
            para('<span style="color:#6b6b66;font-size:14px">Tu n\'es pas à l\'origine de cette demande ? Écris-nous vite à [EMAIL_CONTACT].</span>')],
     sign="<b style=\"color:#0066cc\">Les Activités Sociales de l'Énergie</b><br><b>en partenariat avec Europe Échecs</b>")

# Titres en deux temps : déjà dans chaque mail (« | »)
TITRES = {}
MASCOTTES = {}
ENTETES = {'01': 'confirme', '02': 'plateforme', '03': 'mot-de-passe', '04': 'direct', '05': 'exercices', '06': 'communaute', '07': 'direct', '08': 'semaine', '09': 'deplace', '10': 'tournoi', '11': 'inscription', '12': 'resultats', '13': 'nouvelles', '14': 'bilan', '15': 'serie', '16': 'forum', '17': 'reprendre', '18': 'manque', '19': 'famille', '20': 'avis', '21': 'un-an', '22': 'information', '23': 'aurevoir', '24': 'bilan-debut', '25': 'bilan-pause', '26': 'vacances', '27': 'reprise'}
EXEMPLES.update({"THEME_COURS": "Les principes des débuts", "ANIMATEUR": "Éric", "NIVEAU": "tous niveaux",
    "DESCRIPTION_COURS": "Développer ses pièces, contrôler le centre, roquer : les trois règles d'or des débuts, avec des parties d'exemple commentées en direct.",
    "THEME_LUNDI": "Les principes des débuts", "ANIMATEUR_LUNDI": "Éric", "DUREE_LUNDI": "1 h",
    "THEME_MERCREDI": "La fourchette de Cavalier", "ANIMATEUR_MERCREDI": "Florian", "DUREE_MERCREDI": "55 min",
    "URL_MINIATURE_LUNDI": "img/miniature-exemple.jpg", "URL_MINIATURE_MERCREDI": "img/miniature-exemple.jpg",
    "THEME_PROCHAIN_LUNDI": "le mat du couloir", "THEME_PROCHAIN_MERCREDI": "les finales de pions", "DATE": "18 novembre",
    "NOM_TOURNOI": "Blitz de novembre", "NOM_TOURNOI_PRECEDENT": "Rapide d'octobre", "TITRE_UNE": "le Blitz de novembre",
    "NB_COURS_SUIVIS": "6", "NB_COURS_ANNEE": "58", "NB_TOURNOIS_ANNEE": "11", "HEURE": "18 h 30",
    "NOUVEAUTE_1": "8 cours en direct à revoir en vidéo", "NOUVEAUTE_2": "De nouveaux exercices dans le parcours Initiation", "NOUVEAUTE_3": "Le Blitz de novembre, ouvert à tous",
    "CHANGEMENT": "les cours en direct du mercredi passeront à 19 h", "MOIS": "novembre", "PSEUDO": "LéaDame", "EMAIL_CONTACT": "europe@echecs.com",
    "THEME_FORT": "les mats élémentaires", "THEME_FAIBLE": "le clouage", "AUTEUR_REPONSE": "Florian", "TITRE_SUJET": "Comment mater avec Roi et Tour ?",
    "EXTRAIT_REPONSE": "Repousse le Roi adverse vers le bord avec ta Tour, puis rapproche ton Roi…", "DERNIERE_LECON": "Le mat du couloir", "LECON_SUIVANTE": "La fourchette",
    "VAINQUEUR": "Hugo M.", "NB_JOUEURS": "38", "SEMAINE": "du 9 au 15 nov.", "DATE_ENVOI": "19 novembre", "NB_COURS_MOIS": "8", "NB_NOUVEAUX_EXERCICES_MOIS": "45", "NB_TOURNOIS_MOIS": "4", "NB_JOURS_ACTIFS": "5", "NB_COURS_SUIVIS": "2", "NB_PARTIES": "14", "PROGRESSION_PARCOURS": "62", "NB_LECONS": "8", "NB_EXERCICES": "96", "NB_COURS_SEMAINE": "2", "NB_NOUVEAUX_EXERCICES": "12", "NB_TOURNOIS_SEMAINE": "1", "SERIE": "5", "JOUR_LUNDI": "16", "JOUR_MERCREDI": "18"})

# Titres : le bandeau donne l'accroche, le titre l'information concrète (jamais la même phrase deux fois)
TITRES.update({
    "01-confirmation-adresse": "Confirme | ton adresse e-mail.", "03-mot-de-passe": "Un lien, | valable 1 heure.", "05-demarrage-j3-exercices": "La régularité | avant tout.",
    "08-cours-de-la-semaine": "Tu les as manqués ? | Revois-les.", "13-lettre-de-la-semaine": "À la une : | [TITRE_UNE].", "15-serie-en-danger": "Un exercice | suffit.",
    "16-reponse-forum": "[AUTEUR_REPONSE] | t'a répondu.", "17-inactif-3-semaines": "Ta leçon | t'attend.", "18-inactif-6-semaines": "Il y a du nouveau | sur la plateforme.",
    "19-echecs-en-famille": "Invite | tes proches.", "20-questionnaire-satisfaction": "2 minutes | pour nous aider ?", "21-bilan-annuel": "Ta première année | en chiffres.",
    "22-changement-acces": "À partir du | [DATE_EFFET].", "23-suppression-compte": "Ton compte | est supprimé.",
    "24-bilan-mois-peu-actif": "Chaque séance | compte !", "25-inactif-1-semaine": "Une leçon | pour repartir ?",
})
for e in E:
    if e["id"] == "13-lettre-de-la-semaine": e["sur"] = "La lettre · [DATE_ENVOI]"
