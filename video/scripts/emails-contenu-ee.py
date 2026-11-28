# Contenu des e-mails du site europe-echecs.com (Europe Échecs) : compte, abonnements, nouvelles formules, revue papier, cartes cadeaux.
# Réécrits à partir des modèles actuels du site (relevé du 22 novembre 2026, voir pack/EMAILS-EE.md) et des 4 textes des nouvelles formules
# (Pack Jeu+, Pack Intégral, fin du Pack Jeu et du Pack Progresser). Vouvoiement, comme sur le site.
# Rien n'est ajouté aux sources : ni prix, ni délai, ni service qui n'y figure pas. Les prix restent des variables.
# Exécuté par scripts/emails.py (python3 scripts/emails.py ee), qui fournit les composants et le design.

# ---------- Réglages de la série ----------
C["em"] = "#1f6fc0"                 # bleu d'action du site (surtitre, suite du titre)
C["nuit"] = "#02263d"               # marine de la page des abonnements du site (en-tête, Pack Intégral)
C["bouton"] = "#ffd30e"; C["bouton_texte"] = "#02263d"   # boutons « Je m'abonne » du site : jaune, texte marine
C["jaune"] = "#ffd30e"              # jaune Europe Échecs (#FFD30E, relevé sur la page des abonnements) : filets d'encadré
C["clair"] = "#ffd30e"              # jaune : surtitre et suite du titre sur le bandeau marine, filet sous l'en-tête, pastille du Pack Intégral
TITRE_SUR_NUIT = True                # surtitre et titre dans le bandeau marine, sous le logo
# Palette déclinée de la charte du site (marine #191F38, bleu de marque #58ACFF, bleu d'action #1F6FC0, gris-bleu #6C7497) :
# les teintes crème de l'Académie deviennent des gris-bleus froids, partout (styles et règles du mode sombre)
REMAP = {"#f1f0ea": "#edf1f8",   # fond de page, encadrés, tuiles, tableaux
         "#1d1d1b": "#0b2235",   # texte : marine
         "#6b6b66": "#5d6480",   # texte secondaire : gris-bleu du site
         "#e4e1d8": "#dfe4ee",   # filets
         "#f4f1ea": "#eef1f7"}   # texte en mode sombre
DARK = DARK.replace("</style>", """@media (prefers-color-scheme: dark) {
  [style*="background:#e6f1ff"] { background:#1b2a44 !important; }
  [style*="border:1px solid #1d4563"] { border-color:#2b5a7d !important; }
  table[style*="background:#f1f0ea;border-radius:12px"] { background:#1b2533 !important; }
}
</style>""")
EXPEDITEUR = "Europe Échecs"
AVATAR = '<img src="img/favicon.png" width="34" height="34" alt="" style="display:block;width:34px;height:34px;border-radius:50%">'
POURQUOI = "Vous recevez cet e-mail car vous avez un compte sur europe-echecs.com."
PIED_COMPTE = "Cet e-mail concerne votre compte : il est envoyé même si vous avez refusé les e-mails d'information."
SUIS = "Suivez-nous"
SIGNATURE = "Bonnes parties sur Europe Échecs !<br><b>L'équipe d'Europe Échecs</b>"
ENTETE = f'''<tr><td class="m-pad" style="background:{C['nuit']};padding:22px 32px"><img src="{{IMG}}/logo.png" width="170" alt="Europe Échecs" style="display:block;border:0;width:170px;height:auto"></td></tr>'''
LIENS_PIED = [("Jouer", "[LIEN_ZONE_DE_JEU]"), ("Vidéos", "[LIEN_VIDEOS]"), ("La revue", "[LIEN_REVUE]"), ("Livres", "https://boutique.echecs.com"), ("Aide", "[LIEN_AIDE]")]
RESEAUX = []
MENTION = "IDEAL SAS · Europe Échecs · 114 quai Louis Blériot, 75016 Paris"
DOC = ICI / "pack/EMAILS-EE.md"
TARIFS = "https://www.europe-echecs.com/abonnement.html#table-rates-title"
TARIFS_REVUE = "https://www.europe-echecs.com/abonnement.html#price-revue"
petit = lambda t: f'<span style="color:#6b6b66;font-size:14px">{t}</span>'

def formule(nom, accroche, texte, prix="", phare=False):   # une formule : accroche et tarifs de la page des abonnements ; phare : sur fond marine, avec sa pastille
    if phare:
        return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 12px;border-collapse:separate"><tr>'
                f'<td bgcolor="{C["nuit"]}" style="background:{C["nuit"]};border:1px solid #1d4563;border-radius:14px;padding:18px 20px">'
                f'<div style="display:inline-block;margin:0 0 10px;padding:4px 10px;border-radius:999px;background:{C["clair"]};font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#0d1430">{accroche}</div>'
                f'<div style="font-family:{SERIF};font-weight:{GRAS};font-size:20px;line-height:1.25;color:#ffffff">{nom}</div>'
                f'<div style="margin-top:6px;font:16px/1.55 {SANS};color:#d3d8e6">{texte}</div>'
                + (f'<div style="margin-top:10px;font-family:{SANS};font-weight:800;font-size:14px;line-height:1.5;color:{C["clair"]}">{prix}</div>' if prix else "") + '</td></tr></table>')
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 12px;border-collapse:separate"><tr>'
            f'<td bgcolor="#e6f1ff" style="background:#e6f1ff;border-left:5px solid #65afff;border-radius:14px;padding:18px 20px">'
            f'<div style="font-family:{SERIF};font-weight:{GRAS};font-size:20px;line-height:1.25;color:{C["texte"]}">{nom}'
            + (f' <span style="font-weight:400;color:{C["em"]}">· {accroche}</span>' if accroche else "") + '</div>'
            f'<div style="margin-top:6px;font:16px/1.55 {SANS};color:{C["texte"]}">{texte}</div>'
            + (f'<div style="margin-top:10px;font-family:{SANS};font-weight:800;font-size:14px;line-height:1.5;color:{C["em"]}">{prix}</div>' if prix else "") + '</td></tr></table>')
JEU_PLUS = formule("Pack Jeu+", "Le plaisir de jouer et progresser", "Accédez à toutes les fonctionnalités premium de la zone de jeu et à la zone d'entraînement tactique en illimité. Idéal pour jouer et progresser chaque jour !", prix="4,90 € par mois, sans engagement · 39,90 € pour 1 an · 59,90 € pour 2 ans")
INTEGRAL = formule("Pack Intégral", "Le choix des passionnés", "Débloquez l'ensemble de nos contenus : vidéos à la demande, leçons, revue en ligne… et plus de 4 nouvelles vidéos chaque semaine pour continuer votre progression.", prix="11,90 € par mois, sans engagement · 99,90 € pour 1 an · 149,90 € pour 2 ans", phare=True)
def identifiants(): return infos([("Votre pseudo", "[PSEUDO]")])   # le mot de passe est choisi par l'utilisateur : jamais dans un e-mail

# ---------- 1. Compte ----------
mail(id="01-activation-compte", cat="Compte", marketing=False, quand="À la création du compte, si une activation est nécessaire (modèle account_confirmation)",
     objet="Bienvenue ! Activez votre compte Europe Échecs", pre="Un clic pour activer votre compte : zone de jeu, vidéos, revue et livres vous attendent.", sur="Votre compte", titre="Plus qu'un clic, | [PSEUDO] !",
     corps=[para("Votre compte Europe Échecs est créé. Il ne reste qu'une étape : l'activer."), bouton("Activer mon compte", L("ACTIVATION")),
            para(petit("Code d'activation à fournir si demandé : <b style='white-space:nowrap'>[CODE_ACTIVATION]</b>")),
            para("Une fois votre compte activé, tout Europe Échecs vous attend :"),
            liste(["<b>La zone de jeu</b>, pour jouer et vous entraîner", "<b>Nos vidéos</b>", "<b>Notre revue</b>", "<b>Nos livres</b>, sur boutique.echecs.com"])])
mail(id="02-compte-multicompte", cat="Compte", marketing=False, quand="À la création d'un compte par le gestionnaire d'une offre multicompte (modèle account_confirmation, variante multicompte)",
     objet="Votre compte Europe Échecs est prêt", pre="Créé par [GESTIONNAIRE] dans une offre multicompte : votre pseudo et vos services.", sur="Votre compte", titre="Bienvenue, | [PSEUDO] !",
     corps=[para("Votre compte a été créé par le gestionnaire <b>[GESTIONNAIRE]</b>, dans le cadre d'une offre multicompte dont il assure la gestion. Elle vous donne accès à : <b>[SERVICES_MULTICOMPTE]</b>."),
            identifiants(),
            bouton("Activer mon compte", L("ACTIVATION"))])
mail(id="03-mot-de-passe", cat="Compte", marketing=False, quand="Sur demande de réinitialisation (modèle resetpass)",
     objet="Réinitialisez votre mot de passe Europe Échecs", pre="Ce lien est valable 1 heure. Vous n'avez rien demandé ? Ignorez simplement cet e-mail.", sur="Votre compte", titre="Un nouveau | mot de passe.",
     corps=[para("À la suite de votre demande sur le site, voici un lien pour réinitialiser le mot de passe de votre pseudo <b>[PSEUDO]</b>."), bouton("Choisir mon mot de passe", L("MOT_DE_PASSE")),
            para(petit("Attention : ce lien n'est valable que pendant 1 heure. Si vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail : votre mot de passe ne change pas."))])
mail(id="04-suppression-compte", cat="Compte", marketing=False, quand="Après la suppression du compte (modèle deletion_request_perform)",
     objet="Suppression de votre compte Europe Échecs", pre="Votre compte [PSEUDO] et ses données ont été supprimés, comme vous l'avez demandé.", sur="Votre compte", titre="Votre compte | est supprimé.",
     corps=[para("Votre compte <b>[PSEUDO]</b> a bien été supprimé, ainsi que les données qui lui sont associées."),
            infos([("Date", "[DATE_SUPPRESSION]"), ("Heure", "[HEURE_SUPPRESSION] (heure de Paris)")])],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")

# ---------- 2. Découverte ----------
mail(id="05-decouverte-zone-de-jeu", cat="Découverte", quand="Après la première connexion à la zone de jeu SimpleChess (modèle welcome_directplay)",
     objet="Zone de jeu : 7 fonctions à connaître dès maintenant", pre="Cadences, tournois, analyse de vos parties, joueurs à suivre : le tour du propriétaire.", sur="Zone de jeu", titre="Bienvenue | dans la communauté.",
     corps=[para("Bonjour [PSEUDO] ! Vous avez effectué votre première connexion à notre zone de jeu SimpleChess : nous espérons que l'expérience vous a plu. Voici ce que vous pouvez y faire en tant que membre."),
            liste(["<b>Cadences et force de l'adversaire</b> : choisissez vos cadences et la force de votre adversaire. Gagner contre plus fort que vous rapporte plus de points.",
                   "<b>La discussion</b> : échangez en direct avec vos amis ou n'importe quel joueur, dans le respect de la charte de la zone de jeu.",
                   "<b>Vos listes de joueurs</b> : cliquez sur un pseudo pour l'ajouter à vos amis (une alerte signale son arrivée) ou à votre liste noire (il ne peut plus vous écrire ni vous défier).",
                   "<b>Les parties des plus forts</b> : observez les parties en cours, et retrouvez les 10 dernières parties de chaque joueur sur son profil.",
                   "<b>L'analyse</b> : à la fin de chaque partie, revoyez-la avec un regard critique ; vous pouvez aussi analyser celles que vous observez.",
                   "<b>Les tournois</b> : participez, ou créez votre petit tournoi et invitez vos amis.",
                   "<b>Votre connexion</b> : un rapport détaillé après chaque partie, si vous pensez avoir perdu à cause d'une coupure."]),
            bouton("Jouer une partie", L("ZONE_DE_JEU"))])
mail(id="06-offre-de-bienvenue", cat="Découverte", quand="Offre de bienvenue après l'inscription, valable 48 h (modèle welcome_subscription_48h)",
     objet="Votre offre de bienvenue : −25 % pendant 48 h", pre="Sur tous nos Packs Web 1 et 2 ans, avec votre code personnel. L'offre s'arrête dans 48 heures.", sur="Offre de bienvenue", titre="−25 % | pour bien commencer.",
     corps=[para("Bienvenue parmi nos joueurs, [PSEUDO] ! Pour découvrir nos services, voici un tarif de bienvenue :"),
            tuiles([("−25&nbsp;%", "sur tous nos Packs Web 1 et 2 ans"), ("48&nbsp;h", "pour en profiter")]),
            para("Saisissez ce code dans votre panier :"),
            infos([("Votre code", "[CODE_PROMO]")]),
            bouton("Profiter de −25 %", TARIFS),
            para(petit("Offre valable jusqu'à 48 heures après la réception de cet e-mail."))])

# ---------- 3. Abonnement ----------
mail(id="07-bienvenue-abonnement", cat="Abonnement", marketing=False, quand="À la création du compte lors d'un abonnement (modèle welcome_subscription)",
     objet="Bienvenue ! Votre compte Europe Échecs est prêt", pre="Merci pour votre abonnement. Connectez-vous avec le pseudo et le mot de passe que vous avez choisis.", sur="Bienvenue", titre="Bienvenue | parmi nous !",
     corps=[para("Merci pour votre abonnement ! Votre compte est prêt :"), identifiants(),
            bouton("Me connecter", L("CONNEXION")),
            para(petit("Mot de passe oublié ? Vous pouvez le réinitialiser depuis la page de connexion."))])
mail(id="08-abonnement-mis-en-place", cat="Abonnement", marketing=False, quand="À la mise en place d'un abonnement à paiement récurrent (modèle recurpmt_created)",
     objet="Mise en place de votre abonnement [SERVICE]", pre="Votre abonnement récurrent est en place. Vous le gérez à tout moment depuis « Mon compte ».", sur="Votre abonnement", titre="Votre abonnement | est en place.",
     corps=[para("Votre abonnement récurrent <b>[SERVICE]</b> a été mis en place avec succès pour votre compte <b>[PSEUDO]</b>."),
            para("La prise en compte de votre première mensualité peut demander quelques heures."),
            bouton("Gérer mon abonnement", L("MES_SERVICES")),
            para(petit("Vous pouvez gérer votre abonnement à tout moment dans la rubrique « Mon compte »."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="09-paiement-recu", cat="Abonnement", marketing=False, quand="À la réception d'un paiement de commande (modèle cmdpmtreceived)",
     objet="Votre commande n° [NUMERO_COMMANDE]", pre="Paiement reçu, commande traitée : le détail de votre commande.", sur="Commande n° [NUMERO_COMMANDE]", titre="Paiement reçu, | merci !",
     corps=[para("Nous avons bien reçu votre paiement de <b>[MONTANT]</b> pour la commande n° [NUMERO_COMMANDE], et nous vous en remercions. Votre commande a été traitée : si vous avez souscrit des services, ils sont activés."),
            recu([("[PRODUIT] · Qté [QUANTITE]", "[PRIX_LIGNE]"), ("Participation aux frais de port et d'emballage", "[FRAIS_PORT]")], "Total TTC", "[TOTAL]"),
            ],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="10-abonnement-echeance", cat="Abonnement", quand="Avant l'échéance d'un abonnement web de 1 ou 2 ans (paiement unique, renouvellement manuel), 1re relance à J-15 (modèle relance1web ; la 2e, à J-3, est l'e-mail 29)",
     objet="Votre abonnement Europe Échecs arrive à échéance", pre="[PACK] jusqu'au [DATE_FIN] : renouvelez-le pour garder vos services sans interruption.", sur="Votre abonnement", titre="Continuez | sans interruption.",
     corps=[para("Votre abonnement arrive bientôt à échéance (compte <b>[PSEUDO]</b>). Renouvelez-le, et continuez de profiter de vos services sans interruption !"),
            infos([("Formule", "[PACK]"), ("Fin de l'abonnement", "[DATE_FIN]")]),
            bouton("Renouveler mon abonnement", L("ABONNEMENTS")),
            para(petit("Nouveau : le paiement au mois, sans engagement, dès 4,90 € par mois (Pack Jeu+) ou 11,90 € par mois (Pack Intégral)."))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")
mail(id="11-abonnement-annule", cat="Abonnement", marketing=False, quand="À l'annulation d'un abonnement récurrent (modèle recurpmt_cancelled)",
     objet="Annulation de votre abonnement [SERVICE]", pre="Plus aucune facturation à partir d'aujourd'hui. Vous pouvez revenir quand vous voulez.", sur="Votre abonnement", titre="Votre abonnement | est annulé.",
     corps=[para("Votre abonnement <b>[SERVICE]</b> a été annulé pour votre compte <b>[PSEUDO]</b>. À partir d'aujourd'hui, il ne fera plus l'objet d'aucune facturation."),
            para("Vous pouvez vous réabonner à tout moment depuis la page des tarifs, à l'année, pour 2 ans, ou au mois sans engagement dès 4,90 €."), bouton("Me réabonner", TARIFS),
            para(petit("Pourquoi partez-vous ? Dites-le-nous en une ligne sur <a href=\"[LIEN_AIDE]\" style=\"color:#6b6b66\">la page d'aide</a> : vos réponses guident nos prochaines formules."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")

# ---------- 4. Nouvelles formules ----------
mail(id="12-pack-jeu-devient-jeu-plus", cat="Nouvelles formules", marketing=False, quand="Une fois, aux abonnés du Pack Jeu en cours (passage gratuit au Pack Jeu+)",
     objet="Votre Pack Jeu devient gratuitement le Pack Jeu+", pre="Sans rien payer de plus : l'entraînement tactique en illimité, avec des milliers d'exercices.", sur="Pack Jeu+", titre="Votre Pack Jeu | devient le Pack Jeu+.",
     corps=[para("Bonjour [PSEUDO], votre abonnement Pack Jeu évolue <b>gratuitement</b> vers le Pack Jeu+ !"),
            para("En plus de toutes les fonctionnalités premium de la zone de jeu, vous bénéficiez dès maintenant d'un accès illimité à notre module d'entraînement tactique :"),
            liste(["<b>Des milliers d'exercices</b>", "<b>Un mode challenge</b>, pour vous tester et tenter de battre votre record"]),
            bouton("Découvrir l'entraînement tactique", L("ENTRAINEMENT_TACTIQUE")),
            para("Le Pack Jeu+ remplace désormais le Pack Jeu. À la fin de votre abonnement, vous pourrez le prolonger pour 1 an (39,90 €), 2 ans (59,90 €) ou au mois, sans engagement (4,90 € par mois).")])
mail(id="13-pack-progresser-en-cours", cat="Nouvelles formules", marketing=False, quand="Une fois, aux abonnés du Pack Progresser en cours",
     objet="Votre Pack Progresser : ce qui change", pre="Vous gardez les mêmes services jusqu'à la fin. Ensuite, deux nouvelles formules au choix.", sur="Nouvelles formules", titre="Rien ne change | pour l'instant.",
     corps=[para("Bonjour [PSEUDO], merci pour votre fidélité ! Le Pack Progresser laisse la place à deux nouvelles offres, conçues à partir des réponses des joueurs que nous avons interrogés."),
            para("Jusqu'à la fin de votre abonnement, vous profitez des mêmes services. Ensuite, vous aurez le choix entre :"),
            JEU_PLUS, INTEGRAL,
            encadre("<b>Nouveauté :</b> vous pourrez opter pour le paiement au mois, sans engagement, dès 4,90 € par mois."),
            bouton("Découvrir les deux formules", L("ABONNEMENTS"))])
mail(id="14-pack-progresser-expire", cat="Nouvelles formules", quand="À l'échéance d'un abonnement Pack Progresser",
     objet="Votre Pack Progresser est arrivé à échéance", pre="Pack Jeu+ ou Pack Intégral, à l'année ou au mois : à vous de choisir.", sur="Nouvelles formules", titre="Choisissez | votre nouvelle formule.",
     corps=[para("Bonjour [PSEUDO], votre abonnement au Pack Progresser est arrivé à échéance. Elle laisse la place à deux nouvelles offres, conçues à partir des réponses des joueurs que nous avons interrogés."),
            para("Pour continuer à vivre votre passion sur Europe Échecs, choisissez :"),
            JEU_PLUS, INTEGRAL,
            encadre("<b>Nouveau :</b> payez au mois, sans engagement, dès 4,90 €. Et avec un Pack de 1 ou 2 ans, ajoutez la revue papier pour 60 € (Pack Jeu+) ou 50 € (Pack Intégral), au lieu de 79,95 € seule."),
            bouton("Choisir ma formule", L("ABONNEMENTS"))],
     sign="Merci de votre fidélité !<br><b>L'équipe d'Europe Échecs</b>")
mail(id="15-pack-jeu-expire", cat="Nouvelles formules", quand="À l'échéance d'un abonnement Pack Jeu",
     objet="Votre Pack Jeu est arrivé à échéance", pre="Pack Jeu+ ou Pack Intégral, à l'année ou au mois : à vous de choisir.", sur="Nouvelles formules", titre="Choisissez | votre nouvelle formule.",
     corps=[para("Bonjour [PSEUDO], votre abonnement au Pack Jeu est arrivé à échéance. Elle laisse la place à deux nouvelles offres, conçues à partir des réponses des joueurs que nous avons interrogés."),
            para("Pour continuer à vivre votre passion sur Europe Échecs, choisissez :"),
            JEU_PLUS, INTEGRAL,
            encadre("<b>Nouveau :</b> payez au mois, sans engagement, dès 4,90 €. Et avec un Pack de 1 ou 2 ans, ajoutez la revue papier pour 60 € (Pack Jeu+) ou 50 € (Pack Intégral), au lieu de 79,95 € seule."),
            bouton("Choisir ma formule", L("ABONNEMENTS"))],
     sign="Merci de votre fidélité !<br><b>L'équipe d'Europe Échecs</b>")

# ---------- 5. Revue ----------
mail(id="16-revue-echeance", cat="Revue", quand="Avant la fin d'un abonnement à la revue papier, 1re relance le 25 du mois (modèle relance1ee ; la 2e, le 8 du mois suivant, est l'e-mail 30)",
     objet="Votre abonnement à la revue Europe Échecs se termine", pre="Votre dernier numéro arrive en [ECHEANCE]. Réabonnez-vous pour ne manquer aucun numéro.", sur="La revue", titre="Votre dernier numéro | arrive en [ECHEANCE].",
     corps=[para("Bonjour [PSEUDO], votre abonnement à la revue <i>Europe Échecs</i> arrive à échéance en <b>[ECHEANCE]</b> : c'est ce mois-là que vous recevrez le dernier numéro de votre abonnement en cours."),
            para("Pour ne pas en interrompre l'envoi, réabonnez-vous dès maintenant :"),
            bouton("Me réabonner", TARIFS_REVUE),
            para(petit("Une question ? Contactez le support depuis <a href=\"[LIEN_AIDE]\" style=\"color:#6b6b66\">la page d'aide</a>, en indiquant votre numéro d'abonné ([NUMERO_ABONNE]). Si ce message a croisé votre règlement, merci de ne pas en tenir compte."))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")

# 2es relances : un nouvel angle plutôt que le même texte renvoyé (les modèles relance2web et relance2ee répétaient la 1re)
mail(id="29-abonnement-echeance-relance-2", cat="Abonnement", quand="2e relance à J-3 avant l'échéance d'un abonnement de 1 ou 2 ans, si l'abonnement n'est pas renouvelé (modèle relance2web, réécrit)",
     objet="Votre abonnement s'arrête le [DATE_FIN]", pre="Prolongez pour 2 ans et économisez jusqu'à 49,90 €, ou passez au mois, sans engagement.", sur="Votre abonnement", titre="Plus que 3 jours | avant l'échéance.",
     corps=[para("Bonjour [PSEUDO], votre <b>[PACK]</b> s'arrête le <b>[DATE_FIN]</b>. Si vous comptez continuer, la formule 2 ans revient moins cher que deux années séparées :"),
            infos([("Pack Jeu+, 2 ans", "59,90 € au lieu de 79,80 €"), ("Pack Intégral, 2 ans", "149,90 € au lieu de 199,80 €")]),
            bouton("Prolonger mon abonnement", L("ABONNEMENTS")),
            para(petit("Vous préférez ne pas vous engager ? La formule au mois est sans engagement : 4,90 € (Pack Jeu+) ou 11,90 € (Pack Intégral)."))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")
mail(id="30-revue-echeance-relance-2", cat="Revue", quand="2e relance le 8 du mois qui suit la 1re (16, le 25), avant la fin d'un abonnement à la revue papier, si rien n'est renouvelé (modèle relance2ee, réécrit)",
     objet="Votre revue Europe Échecs pour 50 € de plus", pre="Ajoutée à un Pack Intégral, la revue papier coûte 50 € au lieu de 79,95 €, avec la revue en ligne en prime.", sur="La revue", titre="La revue, | et bien plus.",
     corps=[para("Bonjour [PSEUDO], votre dernier numéro de la revue <i>Europe Échecs</i> arrive en <b>[ECHEANCE]</b>. Avant de vous réabonner, comparez :"),
            infos([("La revue seule", "79,95 €"), ("Avec un Pack Jeu+ 1 an", "39,90 € + 60 €"), ("Avec un Pack Intégral 1 an", "99,90 € + 50 €")]),
            para(petit("Le tarif revue + Pack est réservé aux formules de 1 ou 2 ans : il n'existe pas avec le paiement au mois.")),
            para("Avec le Pack Intégral, vous recevez la revue papier et vous profitez aussi de la revue en ligne, des vidéos à la demande et des leçons."),
            bouton("Choisir ma formule", TARIFS),
            para(petit("Vous préférez la revue seule ? <a href=\"" + TARIFS_REVUE + "\" style=\"color:#6b6b66\">Réabonnez-vous ici</a>. Si ce message a croisé votre règlement, merci de ne pas en tenir compte."))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")

# ---------- 6. Cadeaux ----------
mail(id="17-carte-cadeau", cat="Cadeaux", marketing=False, quand="Après l'achat d'un Pack cadeau (modèle gift_code)",
     objet="Votre carte cadeau Europe Échecs est prête", pre="Le code à offrir, et la carte au format PDF à imprimer ou à envoyer.", sur="Votre cadeau", titre="Votre cadeau | est prêt à offrir !",
     corps=[para("Bonjour [PSEUDO], merci d'avoir acheté l'un de nos Packs cadeaux. Voici votre code :"),
            infos([("[PRODUIT_CADEAU]", "[CODE_CADEAU]")]),
            bouton("Télécharger la carte cadeau", L("CARTE_CADEAU_PDF")),
            para("La carte cadeau au format PDF est prête à imprimer ou à envoyer. Pour la télécharger, connectez-vous avec le compte qui a servi à passer la commande."),
            para('Pour activer le code, rendez-vous sur <a href="https://www.europe-echecs.com/activer-mon-code-cadeau.html" style="color:#1f6fc0;font-weight:700">europe-echecs.com/activer-mon-code-cadeau</a>.'),
            para(petit(f'Le contenu de chaque Pack est détaillé sur notre <a href="{TARIFS}" style="color:#6b6b66">page des tarifs</a>.'))])

# ---------- 7. Propositions : e-mails qui manquent (à valider) ----------
# Rien n'est inventé : prix, délais, offre de retour et nouveautés restent des variables, à remplir avant l'envoi.
INFO_PROPOSITION = " · proposition, à valider"
P_PAIEMENT, P_FIDELITE, P_GRATUITS = "Propositions · paiement mensuel", "Propositions · reconquête et montée en gamme", "Propositions · comptes gratuits"

def video_semaine(n, serie="[SERIE_{n}]", jour="[JOUR_VIDEO_{n}]"):   # une vidéo de la semaine : miniature cliquable, série, jour, titre, auteur
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 18px;border:1px solid #e4e1d8;border-radius:12px;overflow:hidden">'
            f'<tr><td style="background:{C["nuit"]}"><a href="[LIEN_VIDEO_{n}]"><img src="[URL_MINIATURE_{n}]" width="536" alt="Regarder : [TITRE_VIDEO_{n}]" style="display:block;width:100%;height:auto;border:0"></a></td></tr>'
            f'<tr><td style="padding:14px 18px 16px"><div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{C["em"]}">{serie.format(n=n)} · {jour.format(n=n)}</div>'
            f'<div style="margin-top:6px;font:{GRAS} 18px/1.3 {SERIF};color:{C["texte"]}">[TITRE_VIDEO_{n}]</div>'
            f'<div style="margin-top:4px;font:14px/1.5 {SANS};color:{C["gris"]}">Avec [AUTEUR_{n}]</div></td></tr></table>')

# Paiement mensuel
mail(id="18-paiement-refuse", cat=P_PAIEMENT, marketing=False, quand="Échec d'un prélèvement mensuel : l'accès est suspendu tout de suite (1er avis ; si rien n'a changé à J+3 : e-mail 31)" + INFO_PROPOSITION,
     objet="Votre accès [SERVICE] est suspendu", pre="Le prélèvement de [MONTANT] n'a pas abouti. Mettez à jour votre carte pour retrouver votre accès.", sur="Votre abonnement", titre="Un souci | avec votre paiement.",
     corps=[para("Bonjour [PSEUDO], le prélèvement de <b>[MONTANT]</b> pour votre abonnement <b>[SERVICE]</b> n'a pas pu être effectué. Cela arrive par exemple avec une carte expirée ou un plafond atteint. En attendant, votre accès est suspendu."),
            infos([("Formule", "[SERVICE]"), ("Montant", "[MONTANT]"), ("Accès", "suspendu")]),
            bouton("Mettre à jour ma carte", L("MOYEN_PAIEMENT")),
            para(petit("Si c'est déjà fait, ne tenez pas compte de cet e-mail."))])
mail(id="19-carte-bientot-expiree", cat=P_PAIEMENT, marketing=False, quand="30 jours avant l'expiration de la carte enregistrée (abonnements au mois)" + INFO_PROPOSITION,
     objet="Votre carte expire bientôt : pensez à la mettre à jour", pre="La carte •••• [CARTE_4_CHIFFRES] expire fin [MOIS_EXPIRATION]. Une minute suffit pour la remplacer.", sur="Votre abonnement", titre="Votre carte | expire bientôt.",
     corps=[para("Bonjour [PSEUDO], la carte qui règle votre abonnement <b>[SERVICE]</b> expire à la fin du mois de <b>[MOIS_EXPIRATION]</b>. Remplacez-la dès maintenant pour que votre prochain paiement passe sans encombre."),
            infos([("Carte", "•••• [CARTE_4_CHIFFRES]"), ("Expire", "fin [MOIS_EXPIRATION]"), ("Prochain paiement", "[DATE_PROCHAIN_PAIEMENT]")]),
            bouton("Mettre à jour ma carte", L("MOYEN_PAIEMENT"))])
mail(id="20-recu-renouvellement", cat=P_PAIEMENT, marketing=False, quand="À chaque prélèvement d'une formule au mois (seule formule renouvelée automatiquement ; 1 an et 2 ans se renouvellent à la main)" + INFO_PROPOSITION,
     objet="Votre reçu Europe Échecs : [SERVICE], [MOIS]", pre="Paiement de [MONTANT] reçu. Prochain prélèvement le [DATE_PROCHAIN_PAIEMENT].", sur="Votre reçu", titre="Paiement reçu, | merci !",
     corps=[para("Bonjour [PSEUDO], votre abonnement <b>[SERVICE]</b> est renouvelé. Voici votre reçu."),
            recu([("[SERVICE] · [MOIS]", "[MONTANT]"), ("Moyen de paiement", "[MOYEN_PAIEMENT]"), ("Prochain prélèvement", "[DATE_PROCHAIN_PAIEMENT]")], "Total TTC", "[MONTANT]"),
            bouton("Gérer mon abonnement", L("MES_SERVICES")),
            para(petit("Facture téléchargeable dans « Mon compte ». Vous pouvez arrêter le renouvellement à tout moment."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")

mail(id="31-paiement-refuse-relance", cat=P_PAIEMENT, marketing=False, quand="J+3 après l'e-mail 18, si la carte n'a toujours pas été mise à jour (2e et dernier avis)" + INFO_PROPOSITION,
     objet="Votre accès [SERVICE] est toujours suspendu", pre="Une minute pour mettre votre carte à jour, ou une autre formule dès 4,90 € par mois, sans engagement.", sur="Votre abonnement", titre="Retrouvez | votre accès.",
     corps=[para("Bonjour [PSEUDO], le paiement de <b>[MONTANT]</b> pour votre <b>[SERVICE]</b> n'est toujours pas passé, et votre accès reste suspendu. Pour le retrouver, mettez simplement votre carte à jour."),
            bouton("Retrouver mon accès", L("MOYEN_PAIEMENT")),
            para(petit("Vous préférez changer de formule ? Toutes nos formules, au mois sans engagement dès 4,90 € ou pour 1 ou 2 ans, sont sur <a href=\"" + TARIFS + "\" style=\"color:#6b6b66\">la page des tarifs</a>. Si votre carte est déjà à jour, ne tenez pas compte de cet e-mail."))])

# Reconquête et montée en gamme
mail(id="32-abonnement-expire", cat=P_FIDELITE, quand="J+1 après la fin d'un abonnement de 1 ou 2 ans non renouvelé (après les relances 10 et 29 ; puis 21 à J+30)" + INFO_PROPOSITION,
     objet="Votre [PACK] est arrivé à échéance", pre="Votre abonnement s'est terminé le [DATE_FIN]. Reprenez en un clic, au mois dès 4,90 € ou pour 1 ou 2 ans.", sur="Votre abonnement", titre="On reprend | la partie ?",
     corps=[para("Bonjour [PSEUDO], votre <b>[PACK]</b> s'est terminé le <b>[DATE_FIN]</b>. Votre compte reste ouvert : renouvelez votre abonnement pour retrouver vos services."),
            JEU_PLUS, INTEGRAL,
            bouton("Renouveler mon abonnement", L("ABONNEMENTS"))])
mail(id="21-reconquete-j30", cat=P_FIDELITE, quand="30 jours après une fin d'abonnement ou une annulation, une seule fois" + INFO_PROPOSITION,
     objet="Depuis votre départ, sur Europe Échecs", pre="[NOUVEAUTE_1], et d'autres nouveautés. Votre compte vous attend, à l'année ou au mois.", sur="Quoi de neuf", titre="Ce que vous avez | manqué.",
     corps=[para("Bonjour [PSEUDO], votre abonnement s'est arrêté il y a un mois. Voici ce qui a changé depuis :"),
            nouveautes("Ce mois-ci sur Europe Échecs", [("[NOUVEAUTE_1]", ""), ("[NOUVEAUTE_2]", ""), ("[NOUVEAUTE_3]", "")]),
            JEU_PLUS, INTEGRAL,
            bouton("Revenir sur Europe Échecs", L("ABONNEMENTS")),
            para(petit("Le paiement au mois est désormais possible, sans engagement, dès 4,90 € par mois."))])
mail(id="22-jeu-plus-vers-integral", cat=P_FIDELITE, quand="Nouveau (pas en place aujourd'hui) : abonnés Pack Jeu+ actifs, après un délai à fixer, une seule fois" + INFO_PROPOSITION,
     objet="Le Pack Intégral : vidéos, leçons et revue en plus", pre="Pour 7 € de plus par mois : vidéos à la demande, leçons, revue en ligne et plus de 4 nouvelles vidéos par semaine.", sur="Pack Intégral", titre="Et si vous passiez | à l'Intégral ?",
     corps=[para("Bonjour [PSEUDO], avec le Pack Jeu+, vous jouez et vous vous entraînez. Le Pack Intégral garde tout cela, et ajoute le reste :"),
            INTEGRAL,
            para("Du Pack Jeu+ au Pack Intégral :"),
            infos([("Au mois", "4,90 € → 11,90 €"), ("Pour 1 an", "39,90 € → 99,90 €"), ("Pour 2 ans", "59,90 € → 149,90 €")]),
            bouton("Passer au Pack Intégral", L("ABONNEMENTS"))])
mail(id="23-mensuel-vers-annuel", cat=P_FIDELITE, quand="Au 3ᵉ prélèvement d'un abonnement au mois, une seule fois" + INFO_PROPOSITION,
     objet="Passez à l'année : [ECONOMIE] d'économie sur votre [SERVICE]", pre="Un seul paiement par an au lieu de douze, et le même accès à tout votre abonnement.", sur="Votre abonnement", titre="Passez | à l'année.",
     corps=[para("Bonjour [PSEUDO], cela fait trois mois que vous réglez votre abonnement <b>[SERVICE]</b> au mois. En passant à l'année, vous gardez exactement les mêmes services :"),
            infos([("Aujourd'hui, au mois", "[PRIX_MENSUEL]"), ("À l'année", "[PRIX_ANNUEL]")]),
            liste(["<b>[ECONOMIE] d'économie</b> sur un an", "<b>Un seul paiement</b>, sans renouvellement automatique : vous décidez à l'échéance", "Ou <b>2 ans</b> pour [PRIX_2ANS]"]),
            bouton("Passer à l'année", L("ABONNEMENTS"))])

# Offre de bienvenue
mail(id="24-offre-bienvenue-rappel", cat=P_GRATUITS, quand="24 h après l'e-mail 06, si aucun achat avec le code (fin de l'offre dans 24 h)" + INFO_PROPOSITION,
     objet="Plus que 24 heures pour votre −25 %", pre="Votre code de bienvenue s'arrête demain, sur tous nos Packs Web 1 et 2 ans.", sur="Offre de bienvenue", titre="Plus que | 24 heures.",
     corps=[para("Bonjour [PSEUDO], votre offre de bienvenue s'arrête demain. Il vous reste 24 heures pour profiter de <b>−25 %</b> sur tous nos Packs Web 1 et 2 ans."),
            infos([("Votre code", "[CODE_PROMO]")]),
            bouton("Profiter de −25 %", TARIFS),
            para(petit("Code à saisir dans votre panier. Offre valable jusqu'à 48 heures après la réception du premier e-mail."))])

# Comptes gratuits inactifs
mail(id="25-gratuit-inactif-7j", cat=P_GRATUITS, quand="Comptes gratuits, 7 jours sans connexion, une seule fois par période d'inactivité" + INFO_PROPOSITION,
     objet="[PSEUDO], une partie sur Europe Échecs ?", pre="Choisissez votre cadence et la force de votre adversaire : la partie commence en un clic.", sur="Zone de jeu", titre="Une partie, | [PSEUDO] ?",
     corps=[para("Une semaine sans partie : la zone de jeu vous attend. Choisissez votre cadence et la force de votre adversaire. Gagner contre plus fort que vous rapporte plus de points."),
            liste(["<b>Jouez</b> une partie à la cadence de votre choix", "<b>Observez</b> les parties de joueurs plus forts", "<b>Analysez</b> vos parties pour progresser"]),
            bouton("Jouer une partie", L("ZONE_DE_JEU"))])
mail(id="26-gratuit-inactif-21j", cat=P_GRATUITS, quand="Comptes gratuits, 21 jours sans connexion, une seule fois" + INFO_PROPOSITION,
     objet="Ce qui s'est passé sur Europe Échecs ces 3 semaines", pre="[NOUVEAUTE_1], et ce qui vous attend sur la zone de jeu.", sur="Quoi de neuf", titre="Trois semaines | de nouveautés.",
     corps=[para("Bonjour [PSEUDO], depuis votre dernière visite :"),
            nouveautes("Sur Europe Échecs", [("[NOUVEAUTE_1]", ""), ("[NOUVEAUTE_2]", ""), ("[NOUVEAUTE_3]", "")]),
            para("Et pour aller plus loin, le <b>Pack Jeu+</b> ouvre la zone d'entraînement tactique en illimité : des milliers d'exercices et un mode challenge pour battre votre record."),
            bouton("Revenir sur Europe Échecs", L("ZONE_DE_JEU"))])
mail(id="27-gratuit-inactif-45j", cat=P_GRATUITS, quand="Comptes gratuits, 45 jours sans connexion, dernière relance (ensuite, plus d'e-mails d'information)" + INFO_PROPOSITION,
     objet="On continue à vous écrire, [PSEUDO] ?", pre="Dites-nous si nos e-mails vous intéressent encore. Sinon, nous arrêtons de vous écrire.", sur="Vos e-mails", titre="On continue | à vous écrire ?",
     corps=[para("Bonjour [PSEUDO], votre dernière connexion remonte à plus d'un mois. Nous ne voulons pas encombrer votre boîte : si nos e-mails ne vous servent plus, nous arrêtons."),
            bouton("Oui, je reste", L("RESTER_ABONNE")),
            para(f'<a href="{L("DESINSCRIPTION")}" style="color:#1f6fc0;font-weight:700">Non merci, ne plus recevoir ces e-mails</a>'),
            para(petit("Votre compte reste ouvert dans tous les cas : vous pouvez revenir jouer quand vous voulez."))])
mail(id="28-videos-de-la-semaine", cat=P_GRATUITS, quand="Chaque dimanche après-midi (bilan de la semaine : lundi, mardi, mercredi, vendredi, et le dimanche quand il y a une vidéo), à tous les comptes qui l'acceptent" + INFO_PROPOSITION,
     objet="Les vidéos de la semaine sur Europe Échecs", pre="Stratégie, légende, calcul et finale : vos quatre rendez-vous de la semaine, à voir quand vous voulez.", sur="Cette semaine · [DATE_ENVOI]", titre="Les vidéos | de la semaine.",
     corps=[para("Bonjour [PSEUDO], voici les nouvelles vidéos de la semaine."),
            video_semaine(1, "La Minute Stratégie", "Lundi"), video_semaine(2, "Coup de Légende", "Mardi"),
            video_semaine(3, "Calcul Gagnant", "Mercredi"), video_semaine(4, "La Minute Finale", "Vendredi"),
            bouton("Voir toutes les vidéos", L("VIDEOS")),
            para(petit("Toutes les vidéos sont incluses dans le Pack Intégral."))])

# ---------- 8. Newsletter et boutique (e-mails envoyés aujourd'hui depuis Mailjet, remis au design de la série) ----------
P_NEWS, P_BOUTIQUE = "Newsletter", "Boutique"

def article(n, une=False):   # un article : image cliquable, titre, chapô, lien ; l'article à la une est plus grand
    return (f'<!-- ARTICLE {n} : bloc à dupliquer ou à supprimer -->' f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 {24 if une else 18}px;border:1px solid #e4e1d8;border-radius:12px;overflow:hidden">'
            f'<tr><td><a href="[LIEN_ARTICLE_{n}]"><img src="[URL_IMAGE_ARTICLE_{n}]" width="536" alt="" style="display:block;width:100%;height:auto;border:0"></a></td></tr>'
            f'<tr><td style="padding:{"18px 20px 22px" if une else "14px 18px 18px"}">' + (f'<div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{C["em"]};margin:0 0 6px">À la une</div>' if une else "")
            + f'<div style="font:{GRAS} {24 if une else 19}px/1.25 {SERIF};color:{C["texte"]}"><a href="[LIEN_ARTICLE_{n}]" style="color:{C["texte"]};text-decoration:none">[TITRE_ARTICLE_{n}]</a></div>'
            f'<div style="margin-top:8px;font:{16 if une else 15}px/1.55 {SANS};color:{C["gris"]}">[CHAPO_ARTICLE_{n}]</div>'
            f'<div style="margin-top:12px"><a href="[LIEN_ARTICLE_{n}]" style="font:bold 15px {SANS};color:#1f6fc0;text-decoration:none">Lire l\'article&nbsp;&rarr;</a></div></td></tr></table>')

def encart_boutique():   # l'encart commercial glissé dans la newsletter : fond jaune, image, texte court, bouton
    return ('<!-- ENCART BOUTIQUE : facultatif, un seul par newsletter -->' f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 18px;background:{C["jaune"]};border-radius:12px;overflow:hidden">'
            f'<tr><td><a href="[LIEN_ENCART]"><img src="[URL_IMAGE_ENCART]" width="536" alt="" style="display:block;width:100%;height:auto;border:0"></a></td></tr>'
            f'<tr><td style="padding:16px 20px 20px"><div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{C["nuit"]}">La boutique</div>'
            f'<div style="margin-top:6px;font:{GRAS} 19px/1.25 {SERIF};color:{C["nuit"]}">[TITRE_ENCART]</div>'
            f'<div style="margin-top:8px;font:15px/1.55 {SANS};color:{C["nuit"]}">[TEXTE_ENCART]</div>'
            f'<div style="margin-top:14px"><a href="[LIEN_ENCART]" style="display:inline-block;background:{C["nuit"]};color:#ffffff;font:bold 15px {SANS};text-decoration:none;padding:11px 20px;border-radius:999px">[BOUTON_ENCART]&nbsp;&rarr;</a></div></td></tr></table>')

mail(id="33-newsletter", cat=P_NEWS, mailjet=True, quand="Chaque semaine (aujourd'hui le lundi en fin d'après-midi), à tous les comptes qui acceptent les e-mails d'information. Un article à la une, puis autant d'articles que nécessaire, et au plus un encart boutique",
     objet="[OBJET_NEWSLETTER]", pre="[PRE_EN_TETE_NEWSLETTER]", sur="La newsletter · [DATE_ENVOI]", titre="Les actualités | à ne pas rater.",
     corps=[article(1, une=True), article(2), encart_boutique(), article(3), article(4), article(5),
            bouton("Toute l'actualité", "https://www.europe-echecs.com")],
     sign="Bonne lecture,<br><b>La rédaction d'Europe Échecs</b>")

mail(id="34-promo-boutique", cat=P_BOUTIQUE, mailjet=True, quand="Opération commerciale de la boutique (un produit ou une gamme), à tous les comptes qui acceptent les e-mails d'information",
     objet="[OBJET_PROMO]", pre="[PRE_EN_TETE_PROMO]", sur="La boutique Europe Échecs", titre="[TITRE_PROMO_1] | [TITRE_PROMO_2]",
     corps=['<a href="[LIEN_PRODUIT]"><img src="[URL_IMAGE_PRODUIT]" width="536" alt="[ALT_IMAGE_PRODUIT]" style="display:block;width:100%;height:auto;border:0;border-radius:12px;margin:0 0 22px"></a>',
            para("[TEXTE_PROMO]"),
            liste(["[ARGUMENT_1]", "[ARGUMENT_2]", "[ARGUMENT_3]", "[ARGUMENT_4]"]),
            bouton("[BOUTON_PROMO]", "[LIEN_PRODUIT]"),
            para(petit("[CONDITIONS_PROMO]"))],
     sign="À bientôt sur la boutique,<br><b>L'équipe d'Europe Échecs</b>")

from PIL import Image as _I
# Exemples : la newsletter du 23 novembre 2026 et l'e-mail sweat-shirts du 4 novembre 2026 (textes et images d'origine)
for _f in ("article-gukesh-sindarov", "article-firouzja", "article-black-friday", "article-carlsen", "article-maurizzi", "article-eingorn", "promo-sweat-shirts"):
    _im = _I.open(ICI / f"assets/captures/ee/newsletter/{_f}.jpg").convert("RGB"); _im.thumbnail((1100, 1100)); _im.save(APER / f"img/{_f}.jpg", quality=86)
EXEMPLES.update({
    "OBJET_NEWSLETTER": "J-1 avant le choc entre Gukesh et Sindarov !", "PRE_EN_TETE_NEWSLETTER": "Gukesh peut-il faire mentir les pronostics ? Et Firouzja gagne le Total Chess 2026.",
    "URL_IMAGE_ARTICLE_1": "img/article-gukesh-sindarov.jpg", "TITRE_ARTICLE_1": "Gukesh peut-il faire mentir les pronostics ?",
    "CHAPO_ARTICLE_1": "Le 24 novembre, à Genève, le champion du monde commencera la défense de son titre contre Javokhir Sindarov. Tous deux auront 20 ans au début du match : jamais deux joueurs aussi jeunes ne s'étaient affrontés pour la couronne mondiale ! Le match sera diffusé en direct sur Europe Échecs.",
    "URL_IMAGE_ARTICLE_2": "img/article-firouzja.jpg", "TITRE_ARTICLE_2": "Alireza Firouzja gagne le Total Chess 2026 devant Giri et Caruana",
    "CHAPO_ARTICLE_2": "Battu à l'aller par Anish Giri, le Français a remporté la manche retour vendredi 20 novembre à Budapest, puis obtenu la nulle avec les Noirs dans l'armageddon.",
    "URL_IMAGE_ENCART": "img/article-black-friday.jpg", "TITRE_ENCART": "Le Black Friday arrive vendredi !",
    "TEXTE_ENCART": "Livres, échiquiers, abonnements, vêtements : rendez-vous dès vendredi 27 novembre pour découvrir nos offres spéciales.", "BOUTON_ENCART": "Voir la boutique",
    "URL_IMAGE_ARTICLE_3": "img/article-carlsen.jpg", "TITRE_ARTICLE_3": "Magnus Carlsen en 11 coups d'éclat et polémiques",
    "CHAPO_ARTICLE_3": "Trois forfaits en deux jours au Total Chess, une saisine de la commission d'éthique de la FIDE : retour sur onze épisodes où le numéro un mondial a fait parler de lui.",
    "URL_IMAGE_ARTICLE_4": "img/article-maurizzi.jpg", "TITRE_ARTICLE_4": "« Ils me craignent peut-être un peu plus ! » Interview de Marc'Andria Maurizzi",
    "CHAPO_ARTICLE_4": "29 points Elo gagnés en deux tournois et le cap des 2650 franchi : il raconte à Jean-Michel Péchiné comment il a revu sa préparation, avec les 2700 en ligne de mire.",
    "URL_IMAGE_ARTICLE_5": "img/article-eingorn.jpg", "TITRE_ARTICLE_5": "Hommage à Viacheslav Eingorn",
    "CHAPO_ARTICLE_5": "Le Grand Maître d'Odessa aurait eu 70 ans ce 23 novembre. Georges Bertola lui rend hommage et nous invite à rejouer sa victoire contre Efim Geller, commentée par Eingorn lui-même.",
    "OBJET_PROMO": "Faites échec et mat au froid !", "PRE_EN_TETE_PROMO": "−10 % sur les sweat-shirts Europe Échecs : capuche, coton écologique et logo brodé.",
    "TITRE_PROMO_1": "Faites échec et mat", "TITRE_PROMO_2": "au froid !", "URL_IMAGE_PRODUIT": "img/promo-sweat-shirts.jpg", "ALT_IMAGE_PRODUIT": "−10 % sur les sweat-shirts Europe Échecs",
    "TEXTE_PROMO": "L'automne s'installe : les sweat-shirts Europe Échecs sont conçus pour vous garder au chaud tout en affichant votre passion pour le jeu. Pour aller au club, jouer un tournoi ou rester devant l'échiquier, c'est le moment de vous équiper !",
    "ARGUMENT_1": "<b>Capuche</b> et grande poche ventrale", "ARGUMENT_2": "<b>85 % de coton</b> écologique", "ARGUMENT_3": "<b>Logo Europe Échecs</b> brodé", "ARGUMENT_4": "<b>Plusieurs coloris</b> disponibles",
    "BOUTON_PROMO": "Profiter de −10 %", "LIEN_PRODUIT": "https://boutique.echecs.com/25-sweats", "CONDITIONS_PROMO": "−10 % sur les sweat-shirts, en ce moment sur la boutique Europe Échecs."})

# ---------- 9. Propositions : temps forts et rendez-vous réguliers (envoyés depuis Mailjet) ----------
# Prix, remises, dates et résultats restent des variables : rien n'est inventé.
P_TEMPS, P_RDV = "Propositions · temps forts", "Propositions · rendez-vous réguliers"
INFO_MJ = " · proposition, à valider · Mailjet"

def image(src, alt="", lien=None):
    i = f'<img src="{src}" width="536" alt="{alt}" style="display:block;width:100%;height:auto;border:0;border-radius:12px">'
    return f'<div style="margin:0 0 22px">{f"<a href=\"{lien}\">{i}</a>" if lien else i}</div>'

def idee(n):   # une idée cadeau : visuel à gauche, profil, produit, prix et lien à droite
    return (f'<!-- IDÉE CADEAU {n} -->' f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 14px;border:1px solid #e4e1d8;border-radius:12px;background:#ffffff"><tr>'
            f'<td width="128" valign="middle" style="padding:12px 0 12px 12px"><a href="[LIEN_PRODUIT_{n}]"><img src="[URL_IMAGE_PRODUIT_{n}]" width="116" alt="" style="display:block;width:116px;height:auto;border:0"></a></td>'
            f'<td valign="middle" style="padding:12px 16px"><div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{C["em"]}">[PROFIL_{n}]</div>'
            f'<div style="margin-top:4px;font:{GRAS} 17px/1.3 {SERIF};color:{C["texte"]}">[PRODUIT_{n}]</div>'
            f'<div style="margin-top:4px;font:15px/1.5 {SANS};color:{C["gris"]}">[PRIX_PRODUIT_{n}]</div>'
            f'<div style="margin-top:8px"><a href="[LIEN_PRODUIT_{n}]" style="font:bold 15px {SANS};color:#1f6fc0;text-decoration:none">Voir&nbsp;&rarr;</a></div></td></tr></table>')

def visuel_carte_cadeau(pack="Pack Intégral"):   # la carte cadeau dessinée : marine, logo jaune, code en pointillés
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:6px 0 22px"><tr><td align="center">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="340" style="width:100%;max-width:340px;background:{C["nuit"]};border-radius:16px;box-shadow:0 10px 26px rgba(2,38,61,.28)"><tr>'
            f'<td style="padding:20px 22px 22px;border-radius:16px;border:2px solid {C["jaune"]}">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%"><tr><td><img src="{{IMG}}/logo-jaune.png" width="104" alt="Europe Échecs" style="display:block;width:104px;height:auto;border:0"></td>'
            f'<td align="right" style="font-family:{SANS};font-weight:800;font-size:11px;letter-spacing:.16em;text-transform:uppercase;color:{C["jaune"]}">Carte cadeau</td></tr></table>'
            f'<div style="margin-top:26px;font:{GRAS} 26px/1.1 {SERIF};color:#ffffff">{pack}</div>'
            f'<div style="margin-top:6px;font:14px/1.4 {SANS};color:#c9d6e3">Vidéos, leçons, revue en ligne et zone de jeu premium</div>'
            f'<div style="margin-top:18px;padding:9px 12px;border:1px dashed #6f8aa3;border-radius:8px;font:bold 15px/1 {SANS};letter-spacing:.18em;color:#ffffff;text-align:center">XXXX-XXXX</div>'
            f'</td></tr></table></td></tr></table>')

def medaille():   # le cap franchi en grand, dans une pastille jaune
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:6px 0 24px"><tr><td align="center">'
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="160" height="160" style="width:160px;height:160px;background:{C["jaune"]};border-radius:50%;box-shadow:0 0 0 8px #fff4bf,0 10px 24px rgba(2,38,61,.2)"><tr>'
            f'<td align="center" valign="middle" style="border-radius:50%"><div style="font:{GRAS} 50px/1 {SERIF};color:{C["nuit"]}">[CHIFFRE_CAP]</div>'
            f'<div style="margin-top:6px;font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:{C["nuit"]}">[UNITE_CAP]</div></td></tr></table>'
            f'</td></tr></table>')

def bandeau_annee():   # ouverture du bilan annuel : l'année en très grand sur fond marine
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 8px;background:{C["nuit"]};border-radius:16px"><tr>'
            f'<td align="center" style="padding:26px 16px 24px"><div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.16em;text-transform:uppercase;color:#9fb3c8">Votre année aux échecs</div>'
            f'<div style="margin-top:8px;font:{GRAS} 64px/1 {SERIF};color:{C["jaune"]}">[ANNEE]</div>'
            f'<div style="margin-top:10px;font:15px/1.4 {SANS};color:#ffffff">[PSEUDO] · Elo [ELO_ACTUEL]</div></td></tr></table>')

CARTE_CADEAU = encadre("<b>La carte cadeau Europe Échecs</b><br>Pack Jeu+ ou Pack Intégral à offrir : la carte cadeau au format PDF est prête à imprimer ou à envoyer dès la commande. "
                       "La personne qui la reçoit active son code sur europe-echecs.com/activer-mon-code-cadeau.")

# Noël
mail(id="39-noel-idees-cadeaux", cat=P_TEMPS, mailjet=True, quand="Début décembre, à tous les comptes qui acceptent les e-mails d'information" + INFO_MJ,
     objet="Vos idées cadeaux échecs pour Noël", pre="Pour un passionné d'histoire, un joueur de club ou un fan : livres, revue, abonnements, vêtements et cartes cadeaux.", sur="Noël · idées cadeaux", titre="Des cadeaux | pour joueurs d'échecs.",
     corps=[para("Bonjour, vous cherchez un cadeau pour un joueur d'échecs ? Voici quelques idées, selon ce qu'il aime."),
            idee(1), idee(2), idee(3),
            para("<b>Et pour ceux qui ont déjà tout</b>, la carte cadeau Pack Jeu+ ou Pack Intégral, en PDF, prête à imprimer ou à envoyer :"),
            visuel_carte_cadeau(),
            bouton("Voir toutes les idées cadeaux", "[LIEN_NOEL]")])
mail(id="40-noel-derniere-livraison", cat=P_TEMPS, mailjet=True, quand="Le dernier jour de commande pour une livraison avant Noël (date à fixer avec la boutique), sauf à ceux qui ont commandé dans la semaine" + INFO_MJ,
     objet="Commandez aujourd'hui pour être livré avant Noël", pre="Dernier jour pour recevoir livres et échiquiers avant le 25 décembre. Ensuite, il reste la carte cadeau.", sur="Noël · dernier jour de livraison", titre="Livré avant Noël : | commandez aujourd'hui.",
     corps=[para("Bonjour, pour recevoir votre commande avant le 25 décembre, passez-la avant ce soir, <b>[DATE_LIMITE_LIVRAISON]</b>."),
            billet("Dernier jour pour être livré avant Noël", [("Commande", "avant ce soir, [HEURE_LIMITE]"), ("Livraison", "[CONDITIONS_LIVRAISON]")], jour="[JJ]", mois="déc."),
            bouton("Voir les idées cadeaux", "[LIEN_NOEL]"),
            para(petit("Passé cette date, la carte cadeau Pack Jeu+ ou Pack Intégral reste possible jusqu'au dernier moment : elle arrive en PDF, sans livraison."))])
mail(id="41-noel-carte-cadeau", cat=P_TEMPS, mailjet=True, quand="Du 22 au 24 décembre, une seule fois, sauf à ceux qui ont acheté une carte cadeau" + INFO_MJ,
     objet="Un cadeau d'échecs, même le 24 décembre", pre="La carte cadeau Europe Échecs arrive en PDF : prête à imprimer ou à envoyer, sans attendre la livraison.", sur="Noël · cadeau de dernière minute", titre="Trop tard pour la livraison ? | La carte cadeau.",
     corps=[para("Bonjour, il est trop tard pour une livraison avant Noël, mais pas pour faire plaisir à un joueur d'échecs."),
            visuel_carte_cadeau(),
            liste(["<b>Choisissez</b> le Pack Jeu+ ou le Pack Intégral", "<b>Téléchargez</b> la carte cadeau en PDF dans votre compte", "<b>Imprimez-la ou envoyez-la</b> : le code s'active sur europe-echecs.com/activer-mon-code-cadeau"]),
            bouton("Offrir une carte cadeau", "[LIEN_CARTE_CADEAU]"),
            para(petit(f'Le contenu de chaque Pack est détaillé sur notre <a href="{TARIFS}" style="color:#6b6b66">page des tarifs</a>.'))])

# Rendez-vous réguliers
def couverture():   # couverture de la revue et sommaire, côte à côte
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 22px"><tr>'
            f'<td width="150" valign="top" style="padding-right:18px"><a href="[LIEN_REVUE_EN_LIGNE]"><img src="[URL_COUVERTURE]" width="150" alt="Couverture du numéro [NUMERO_REVUE]" style="display:block;width:150px;height:auto;border:0;border-radius:6px;box-shadow:0 4px 14px rgba(0,0,0,.18)"></a></td>'
            f'<td valign="top"><div style="font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.1em;text-transform:uppercase;color:{C["em"]}">Au sommaire</div>'
            + "".join(f'<div style="margin-top:10px;font:15px/1.45 {SANS};color:{C["texte"]}">[SOMMAIRE_{i}]</div>' for i in (1, 2, 3, 4)) + '</td></tr></table>')
mail(id="42-revue-nouveau-numero", cat=P_RDV, mailjet=True, quand="À la sortie de chaque numéro de la revue, aux abonnés qui ont la revue en ligne (Pack Intégral) ou papier" + INFO_MJ,
     objet="Le numéro [NUMERO_REVUE] de la revue est en ligne", pre="[ACCROCHE_NUMERO]", sur="La revue · numéro [NUMERO_REVUE]", titre="Le nouveau numéro | est en ligne.",
     corps=[para("Bonjour, le numéro <b>[NUMERO_REVUE]</b> de la revue Europe Échecs vous attend. [ACCROCHE_NUMERO]"),
            couverture(),
            bouton("Lire le numéro", "[LIEN_REVUE_EN_LIGNE]"),
            para(petit("Les parties de la revue sont à rejouer en ligne, coup par coup."))],
     sign="Bonne lecture,<br><b>La rédaction d'Europe Échecs</b>")
mail(id="43-probleme-de-la-semaine", cat=P_RDV, mailjet=True, quand="Chaque semaine (jour à fixer, pas le même que la newsletter), aux comptes gratuits qui acceptent les e-mails d'information. Varier les niveaux d'une semaine à l'autre" + INFO_MJ,
     objet="Le problème de la semaine : [CONSIGNE_COURTE]", pre="Niveau [NIVEAU_PROBLEME]. Trouvez le coup, puis vérifiez la solution sur Europe Échecs.", sur="Le problème de la semaine", titre="À vous | de jouer !",
     corps=[image("[URL_IMAGE_POSITION]", "La position du problème de la semaine", "[LIEN_SOLUTION]"),
            infos([("Niveau", "[NIVEAU_PROBLEME]"), ("Consigne", "[CONSIGNE]")]),
            bouton("Voir la solution", "[LIEN_SOLUTION]"),
            para(petit("Envie d'autres exercices ? Le Pack Jeu+ ouvre la zone d'entraînement tactique en illimité, avec un mode challenge pour battre votre record."))])

for _src, _dst in (("assets/captures/ee/revue-779-couv.png", "revue-779-couv.png"), ("build/pack/images/00-emails/email-puzzle-1080x1080.jpg", "probleme-exemple.jpg"),
                   ("assets/captures/ee/boutique/cadeau-pack-steinitz.jpg", "cadeau-1.jpg"), ("assets/captures/ee/boutique/cadeau-revue-pack-jeu.jpg", "cadeau-2.jpg"), ("assets/captures/ee/boutique/cadeau-sweat-shirts.jpg", "cadeau-3.jpg")):
    _im = _I.open(ICI / _src).convert("RGB"); _im.thumbnail((1100, 1100)); _im.save(APER / f"img/{_dst.replace('.png', '.jpg')}", quality=86)
EXEMPLES.update({
    "URL_COUVERTURE": "img/revue-779-couv.jpg", "NUMERO_REVUE": "779",
    "ACCROCHE_NUMERO": "Étienne Bacrot et Sophie Milliet, seize titres de champion de France à eux deux, commentent leurs parties.",
    "SOMMAIRE_1": "<b>Le grand dossier</b> : Bacrot et Milliet reviennent sur leur nouveau sacre", "SOMMAIRE_2": "<b>Les analyses</b> de Wesley So, Vasyl Ivanchuk et Susan Polgar",
    "SOMMAIRE_3": "<b>Loïc Travadon et Marie Sebag</b>", "SOMMAIRE_4": "<b>Le cahier pédagogique</b> pour progresser",
    "URL_IMAGE_PRODUIT_1": "img/cadeau-1.jpg", "PROFIL_1": "Pour un passionné d'histoire", "PRODUIT_1": "Le Pack Steinitz : les deux tomes de Georges Bertola",
    "URL_IMAGE_PRODUIT_2": "img/cadeau-2.jpg", "PROFIL_2": "Pour un joueur de club", "PRODUIT_2": "La revue papier et le Pack Jeu+, pour 1 an",
    "URL_IMAGE_PRODUIT_3": "img/cadeau-3.jpg", "PROFIL_3": "Pour tous les fans", "PRODUIT_3": "Les sweat-shirts Europe Échecs",
    "URL_IMAGE_POSITION": "img/probleme-exemple.jpg", "NIVEAU_PROBLEME": "facile", "CONSIGNE": "Les Blancs jouent et font mat en un coup.", "CONSIGNE_COURTE": "les Blancs matent en un coup"})
for _k in ("JJ", "HEURE_LIMITE", "DATE_LIMITE_LIVRAISON", "CONDITIONS_LIVRAISON") + tuple(f"PRIX_PRODUIT_{i}" for i in (1, 2, 3)):
    EXEMPLES[_k] = "[" + _k + "]"   # aucun résultat, prix ni offre inventés

# ---------- 10. Propositions : vos chiffres, satisfaction et fidélité (envoyés par le site) ----------
# Ils demandent des données du site (parties, Elo, exercices, panier) : à créer si elles n'existent pas encore (liste dans DEVELOPPEURS-EE.md).
P_CHIFFRES, P_FIDELE = "Propositions · vos chiffres", "Propositions · satisfaction et fidélité"
INFO_DONNEES = " · proposition, à valider · données à créer côté site (voir DEVELOPPEURS-EE.md)"

mail(id="44-votre-mois", cat=P_CHIFFRES, quand="Le 1er de chaque mois, aux comptes qui ont joué au moins une partie dans le mois, s'ils acceptent les e-mails d'information" + INFO_DONNEES,
     objet="Votre mois de [MOIS_BILAN] sur Europe Échecs", pre="[NB_PARTIES] parties, [VARIATION_ELO] points Elo et [NB_EXERCICES] exercices réussis.", sur="Votre bilan · [MOIS_BILAN]", titre="Votre mois | en chiffres.",
     corps=[para("Bonjour [PSEUDO], voici votre mois de <b>[MOIS_BILAN]</b> sur Europe Échecs."),
            tuiles([("[NB_PARTIES]", "parties jouées"), ("[VARIATION_ELO]", "points Elo"), ("[NB_EXERCICES]", "exercices réussis")]),
            nouveautes("Votre meilleur moment", [("Plus belle victoire", "[MEILLEURE_VICTOIRE]"), ("Classement actuel", "[ELO_ACTUEL]")]),
            bouton("Jouer une partie", L("ZONE_DE_JEU")),
            para(petit("Pour recevoir ou non ce bilan, gérez vos e-mails dans « Mon compte »."))])
mail(id="45-cap-franchi", cat=P_CHIFFRES, quand="Quand un joueur franchit un cap : 100ᵉ partie, nouveau record Elo, record battu en mode challenge (un seul e-mail par semaine au plus)" + INFO_DONNEES,
     objet="Bravo [PSEUDO] : [CAP_FRANCHI]", pre="Félicitations, [DETAIL_CAP]. On continue sur cette lancée ?", sur="Cap franchi", titre="Bravo, | [CAP_FRANCHI] !",
     corps=[medaille(),
            para("Bonjour [PSEUDO], <b>[DETAIL_CAP]</b>. Félicitations !"),
            infos([("Votre record", "[RECORD]"), ("Le jour", "[DATE_CAP]")]),
            bouton("Viser le cap suivant", L("ZONE_DE_JEU"))])

mail(id="46-panier-abandonne", cat=P_FIDELE, quand="1 heure après avoir quitté la page de paiement d'un abonnement sans payer, une seule fois par semaine" + INFO_DONNEES,
     objet="Votre [SERVICE] vous attend", pre="Il ne reste qu'une étape pour retrouver vos vidéos, leçons et entraînements.", sur="Votre commande", titre="Il ne reste | qu'une étape.",
     corps=[para("Bonjour [PSEUDO], vous avez commencé à souscrire au <b>[SERVICE]</b> sans aller jusqu'au paiement. Votre sélection est gardée :"),
            infos([("Formule", "[SERVICE]"), ("Prix", "[PRIX]")]),
            bouton("Terminer ma commande", "[LIEN_PANIER]"),
            para(petit("Une question avant de vous décider ? Notre page d'aide répond aux plus fréquentes, et le support est joignable depuis votre compte."))])
mail(id="47-satisfaction-30j", cat=P_FIDELE, quand="30 jours après le début d'un abonnement payant, une seule fois" + INFO_DONNEES,
     objet="Un mois sur Europe Échecs : votre avis ?", pre="Une question, un clic : vous recommanderiez Europe Échecs à un ami ?", sur="Votre avis", titre="Votre avis | nous aide.",
     corps=[para("Bonjour [PSEUDO], cela fait un mois que vous êtes abonné au <b>[SERVICE]</b>. Une seule question :"),
            para("<b>Recommanderiez-vous Europe Échecs à un ami joueur d'échecs ?</b>"),
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:6px 0 10px"><tr>' + "".join(
                f'<td width="9%" align="center" style="padding:0 2px"><a href="[LIEN_AVIS]?note={n}" style="display:block;padding:11px 0;border-radius:8px;background:{("#fde2e1" if n <= 6 else "#fff1b8" if n <= 8 else "#d8f3dc")};font:bold 15px {SANS};color:{("#9b1c1c" if n <= 6 else "#7a5a00" if n <= 8 else "#1b6b34")};text-decoration:none">{n}</a></td>' for n in range(11)) + '</tr></table>',
            f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 20px"><tr><td style="font:12px {SANS};color:{C["gris"]}">Pas du tout</td><td align="right" style="font:12px {SANS};color:{C["gris"]}">Oui, sans hésiter</td></tr></table>',
            para(petit("Un clic suffit. Si vous voulez en dire plus, une page s'ouvre pour laisser un commentaire."))])
mail(id="48-anniversaire-abonnement", cat=P_FIDELE, quand="Au 1er anniversaire d'un abonnement (puis chaque année), 30 jours avant l'échéance pour les formules de 1 an" + INFO_DONNEES,
     objet="Un an avec vous, [PSEUDO] : merci !", pre="[NB_PARTIES_AN] parties, [NB_VIDEOS_AN] vidéos et [NB_EXERCICES_AN] exercices en un an.", sur="Votre anniversaire", titre="Un an | ensemble.",
     corps=[para("Bonjour [PSEUDO], vous êtes abonné au <b>[SERVICE]</b> depuis un an. Merci de votre fidélité ! Votre année en chiffres :"),
            tuiles([("[NB_PARTIES_AN]", "parties jouées"), ("[NB_VIDEOS_AN]", "vidéos vues"), ("[NB_EXERCICES_AN]", "exercices réussis")]),
            bouton("Continuer à progresser", L("ZONE_DE_JEU")),
            para(petit("Votre abonnement arrive à échéance le [DATE_FIN] : vous recevrez un rappel avant cette date."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="49-votre-annee", cat=P_CHIFFRES, quand="Début janvier, aux comptes qui ont joué dans l'année, s'ils acceptent les e-mails d'information" + INFO_DONNEES,
     objet="Votre année [ANNEE] sur Europe Échecs", pre="[NB_PARTIES_AN] parties, votre meilleur Elo à [ELO_MAX] et votre plus belle victoire.", sur="Votre année [ANNEE]", titre="Votre année | [ANNEE].",
     corps=[bandeau_annee(),
            para("Bonjour [PSEUDO], voici votre année <b>[ANNEE]</b> sur Europe Échecs."),
            tuiles([("[NB_PARTIES_AN]", "parties jouées"), ("[ELO_MAX]", "meilleur Elo"), ("[NB_EXERCICES_AN]", "exercices réussis")]),
            nouveautes("Vos moments forts", [("Plus belle victoire", "[MEILLEURE_VICTOIRE]"), ("Cadence préférée", "[CADENCE_PREFEREE]"), ("Mois le plus actif", "[MOIS_ACTIF]")]),
            bouton("Partager mon année", "[LIEN_PARTAGE_ANNEE]"),
            para('<a href="' + L("ZONE_DE_JEU") + '" style="color:#1f6fc0;font-weight:700">Commencer [ANNEE_SUIVANTE] par une partie</a>')])
mail(id="50-revue-papier-vers-web", cat=P_FIDELE, quand="Abonnés à la revue papier sans abonnement web, 2 mois après le début de l'abonnement, une seule fois" + INFO_DONNEES,
     objet="Votre revue, aussi en ligne et en vidéo", pre="Les parties de la revue à rejouer coup par coup, plus de 4 vidéos par semaine et la zone de jeu premium.", sur="Pack Intégral", titre="Votre revue, | en ligne aussi.",
     corps=[para("Bonjour [PSEUDO], vous recevez la revue Europe Échecs chez vous. Le Pack Intégral la prolonge sur le site :"),
            INTEGRAL,
            bouton("Découvrir le Pack Intégral", L("ABONNEMENTS")),
            para(petit(f'Toutes nos formules sont sur <a href="{TARIFS}" style="color:#6b6b66">la page des tarifs</a>.'))])

EXEMPLES.update({"MOIS_BILAN": "novembre", "ANNEE": "2026", "ANNEE_SUIVANTE": "2027", "PRIX": "11,90 € par mois"})
# Chiffres d'un joueur fictif (LéaDame), pour l'aperçu seulement : ce sont des données personnelles, pas des chiffres d'Europe Échecs
EXEMPLES.update({"NB_PARTIES": "42", "VARIATION_ELO": "+38", "NB_EXERCICES": "156", "MEILLEURE_VICTOIRE": "contre un joueur à 1720", "ELO_ACTUEL": "1612",
    "CAP_FRANCHI": "votre 100ᵉ partie", "CHIFFRE_CAP": "100", "UNITE_CAP": "parties", "DETAIL_CAP": "vous venez de jouer votre 100ᵉ partie sur Europe Échecs", "RECORD": "1612 Elo", "DATE_CAP": "24 novembre",
    "NB_PARTIES_AN": "318", "NB_VIDEOS_AN": "64", "NB_EXERCICES_AN": "1 240", "ELO_MAX": "1648", "CADENCE_PREFEREE": "blitz 5 min", "MOIS_ACTIF": "mars"})

# ---------- 11. Boutique : suivi de commande (boutique.echecs.com) ----------
P_COMMANDE = "Boutique · suivi de commande"
INFO_BOUTIQUE = " · proposition, à valider · envoyé par la boutique"

def suivi(etape):   # les étapes de la commande : commandée, expédiée, livrée ; les étapes passées en jaune
    noms = ["Commandée", "Expédiée", "Livrée"]
    cell = lambda i, n: (f'<td width="33%" align="center" valign="top" style="padding:0 4px">'
                         f'<div style="width:34px;height:34px;margin:0 auto;border-radius:50%;background:{C["jaune"] if i <= etape else C["fond"]};'
                         f'font:bold 15px/34px {SANS};color:{C["nuit"] if i <= etape else C["gris"]};text-align:center">{"&#10003;" if i < etape else i + 1}</div>'
                         f'<div style="margin-top:8px;font-family:{SANS};font-weight:{800 if i == min(etape, 2) else 600};font-size:13px;color:{C["texte"] if i <= etape else C["gris"]}">{n}</div></td>')
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:6px 0 24px"><tr>'
            + "".join(cell(i, n) for i, n in enumerate(noms)) + '</tr></table>')

def article_commande(n=1):   # une ligne de produit : vignette, nom, quantité, prix
    return (f'<!-- PRODUIT {n} : une ligne par produit -->' f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 10px"><tr>'
            f'<td width="72" valign="middle"><img src="[URL_IMAGE_ARTICLE_COMMANDE_{n}]" width="64" alt="" style="display:block;width:64px;height:auto;border:1px solid #e4e1d8;border-radius:8px"></td>'
            f'<td valign="middle" style="padding-left:12px;font:{GRAS} 15px/1.35 {SERIF};color:{C["texte"]}">[NOM_ARTICLE_{n}]<div style="margin-top:2px;font:13px {SANS};color:{C["gris"]}">Quantité : [QUANTITE_ARTICLE_{n}]</div></td>'
            f'<td align="right" valign="middle" style="font:bold 15px {SANS};color:{C["texte"]};white-space:nowrap">[PRIX_ARTICLE_{n}]</td></tr></table>')

mail(id="51-commande-confirmee", cat=P_COMMANDE, marketing=False, quand="Dès la commande payée sur la boutique" + INFO_BOUTIQUE,
     objet="Commande n° [NUMERO_COMMANDE] confirmée, merci !", pre="Nous préparons votre colis. Livraison prévue autour du [DATE_LIVRAISON_ESTIMEE].", sur="Votre commande", titre="Merci pour | votre commande !",
     corps=[suivi(0),
            para("Bonjour [PRENOM_CLIENT], votre commande <b>n° [NUMERO_COMMANDE]</b> est bien enregistrée. Nous la préparons, et vous recevrez un e-mail dès son expédition."),
            article_commande(1), article_commande(2),
            recu([("Sous-total", "[SOUS_TOTAL]"), ("Livraison ([MODE_LIVRAISON])", "[FRAIS_PORT]")], "Total TTC", "[TOTAL]"),
            infos([("Livraison à", "[ADRESSE_LIVRAISON]"), ("Livraison prévue", "[DATE_LIVRAISON_ESTIMEE]"), ("Paiement", "[MODE_PAIEMENT]")]),
            bouton("Voir ma commande", "[LIEN_COMMANDE]"),
            para(petit("Votre facture est disponible dans votre compte, rubrique « Mes commandes »."))],
     sign="Merci de votre confiance,<br><b>La boutique Europe Échecs</b>")
mail(id="52-commande-expediee", cat=P_COMMANDE, marketing=False, quand="Quand le colis est remis au transporteur, avec le numéro de suivi" + INFO_BOUTIQUE,
     objet="Votre commande n° [NUMERO_COMMANDE] est en route", pre="Colis remis à [TRANSPORTEUR] : suivez-le avec le numéro [NUMERO_SUIVI].", sur="Votre commande", titre="Votre colis | est en route !",
     corps=[suivi(1),
            para("Bonjour [PRENOM_CLIENT], bonne nouvelle : votre commande <b>n° [NUMERO_COMMANDE]</b> vient de partir."),
            infos([("Transporteur", "[TRANSPORTEUR]"), ("N° de suivi", "[NUMERO_SUIVI]"), ("Livraison prévue", "[DATE_LIVRAISON_ESTIMEE]")]),
            bouton("Suivre mon colis", "[LIEN_SUIVI]"),
            article_commande(1), article_commande(2)],
     sign="À très bientôt,<br><b>La boutique Europe Échecs</b>")
mail(id="53-commande-livree", cat=P_COMMANDE, marketing=False, quand="Quand le transporteur signale la livraison (ou 3 jours après l'expédition si le transporteur ne le signale pas)" + INFO_BOUTIQUE,
     objet="Votre commande n° [NUMERO_COMMANDE] est arrivée", pre="Tout est en ordre ? Un souci avec votre colis : nous sommes là pour vous aider.", sur="Votre commande", titre="Votre colis | est arrivé.",
     corps=[suivi(3),
            para("Bonjour [PRENOM_CLIENT], votre commande <b>n° [NUMERO_COMMANDE]</b> a été livrée. Nous espérons qu'elle vous plaira !"),
            encadre("<b>Vous avez choisi un livre ?</b> Beaucoup de nos auteurs sont aussi en vidéo sur Europe Échecs, chaque semaine. Toutes les vidéos sont incluses dans le Pack Intégral."),
            bouton("Voir les vidéos", L("VIDEOS")),
            para(petit('Un article manquant ou abîmé ? Écrivez-nous depuis <a href="[LIEN_AIDE]" style="color:#6b6b66">la page d\'aide</a> en indiquant votre numéro de commande.'))],
     sign="Bonne lecture et bonnes parties,<br><b>La boutique Europe Échecs</b>")
mail(id="54-avis-produit", cat=P_COMMANDE, quand="10 jours après la livraison, une seule fois par commande, s'il accepte les e-mails d'information" + INFO_BOUTIQUE,
     objet="[NOM_ARTICLE_1] : qu'en pensez-vous ?", pre="Votre avis aide les autres joueurs à choisir. Une note suffit, un commentaire si vous voulez.", sur="Votre avis", titre="Votre avis | compte !",
     corps=[para("Bonjour [PRENOM_CLIENT], vous avez reçu votre commande il y a une dizaine de jours. Que pensez-vous de cet article ?"),
            article_commande(1),
            '<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:8px auto 22px"><tr>' + "".join(
                f'<td style="padding:0 3px"><a href="[LIEN_AVIS_PRODUIT]?note={n}" style="display:block;width:46px;height:46px;border-radius:10px;background:{C["fond"]};font:30px/46px {SANS};color:{C["jaune"]};text-align:center;text-decoration:none">&#9733;</a></td>' for n in range(1, 6)) + '</tr></table>',
            para(petit("Touchez une étoile pour donner votre note : une page s'ouvre pour ajouter un commentaire si vous le souhaitez."))],
     sign="Merci pour votre aide,<br><b>La boutique Europe Échecs</b>")
mail(id="55-remboursement", cat=P_COMMANDE, marketing=False, quand="Quand un remboursement (total ou partiel) ou une annulation est validé" + INFO_BOUTIQUE,
     objet="Remboursement de votre commande n° [NUMERO_COMMANDE]", pre="[MONTANT_REMBOURSE] remboursés sur votre [MODE_PAIEMENT]. Ils apparaîtront sous quelques jours.", sur="Votre commande", titre="Votre remboursement | est en cours.",
     corps=[para("Bonjour [PRENOM_CLIENT], nous avons procédé au remboursement de votre commande <b>n° [NUMERO_COMMANDE]</b>."),
            recu([("Article(s)", "[ARTICLES_REMBOURSES]"), ("Moyen de paiement", "[MODE_PAIEMENT]")], "Remboursé", "[MONTANT_REMBOURSE]"),
            para("Le délai d'apparition sur votre compte dépend de votre banque, en général quelques jours ouvrés."),
            bouton("Voir ma commande", "[LIEN_COMMANDE]")],
     sign="La boutique Europe Échecs")
mail(id="56-retour-en-stock", cat=P_COMMANDE, quand="Quand un produit épuisé revient en stock, à ceux qui ont demandé à être prévenus (une seule fois)" + INFO_BOUTIQUE,
     objet="[NOM_ARTICLE_1] est de retour en stock", pre="Vous avez demandé à être prévenu : il est de nouveau disponible sur la boutique.", sur="La boutique", titre="De retour | en stock !",
     corps=[para("Bonjour, vous nous aviez demandé de vous prévenir : <b>[NOM_ARTICLE_1]</b> est de nouveau disponible."),
            '<a href="[LIEN_PRODUIT_1]"><img src="[URL_IMAGE_PRODUIT_STOCK]" width="260" alt="[NOM_ARTICLE_1]" style="display:block;width:260px;max-width:100%;height:auto;border:0;margin:0 auto 22px"></a>',
            bouton("Voir le produit", "[LIEN_PRODUIT_1]")],
     sign="La boutique Europe Échecs")
mail(id="57-panier-boutique", cat=P_COMMANDE, quand="2 heures après un panier laissé sur la boutique par un client connecté, une seule fois par panier" + INFO_BOUTIQUE,
     objet="Vous avez oublié quelque chose", pre="[NOM_ARTICLE_1] vous attend dans votre panier.", sur="Votre panier", titre="Votre panier | vous attend.",
     corps=[para("Bonjour [PRENOM_CLIENT], vous avez laissé des articles dans votre panier. Nous les gardons pour vous :"),
            article_commande(1),
            bouton("Retrouver mon panier", "[LIEN_PANIER_BOUTIQUE]"),
            para(petit('Une question sur un produit ? <a href="[LIEN_AIDE]" style="color:#6b6b66">La page d\'aide</a> est là pour vous.'))],
     sign="La boutique Europe Échecs")

EXEMPLES.update({"PRENOM_CLIENT": "Léa", "URL_IMAGE_ARTICLE_COMMANDE_1": "img/cadeau-1.jpg", "NOM_ARTICLE_1": "Pack Steinitz (2 tomes)", "QUANTITE_ARTICLE_1": "1",
    "URL_IMAGE_ARTICLE_COMMANDE_2": "img/cadeau-3.jpg", "NOM_ARTICLE_2": "Sweat-shirt Europe Échecs", "QUANTITE_ARTICLE_2": "1",
    "URL_IMAGE_PRODUIT_STOCK": "img/cadeau-1.jpg", "TRANSPORTEUR": "Colissimo", "MODE_LIVRAISON": "Colissimo", "MODE_PAIEMENT": "carte bancaire",
    "ADRESSE_LIVRAISON": "12 rue des Échecs, 75011 Paris", "ARTICLES_REMBOURSES": "Sweat-shirt Europe Échecs"})
# Gabarits d'affichage (largeur réelle, aucune valeur inventée) : prix, dates et numéro de suivi restent à remplir
EXEMPLES.update({k: "XX,XX €" for k in ("PRIX_ARTICLE_1", "PRIX_ARTICLE_2", "SOUS_TOTAL", "FRAIS_PORT", "TOTAL", "MONTANT_REMBOURSE")})
EXEMPLES.update({"DATE_LIVRAISON_ESTIMEE": "JJ/MM/AAAA", "NUMERO_SUIVI": "XXXXXXXXXXXXX"})

# ---------- 12. Propositions : bien démarrer, ne pas décrocher, d'un produit à l'autre ----------
P_DEMARRER, P_PONTS = "Propositions · bien démarrer", "Propositions · d'un produit à l'autre"

def etapes(items):   # étapes numérotées : pastille jaune, titre, texte
    return ('<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:6px 0 22px">' + "".join(
        f'<tr><td width="52" valign="top" style="padding:0 0 18px"><div style="width:38px;height:38px;border-radius:50%;background:{C["jaune"]};font:{GRAS} 18px/38px {SERIF};color:{C["nuit"]};text-align:center">{i}</div></td>'
        f'<td valign="top" style="padding:2px 0 18px"><div style="font:{GRAS} 17px/1.3 {SERIF};color:{C["texte"]}">{titre}</div><div style="margin-top:4px;font:15px/1.5 {SANS};color:{C["gris"]}">{texte}</div></td></tr>'
        for i, (titre, texte) in enumerate(items, 1)) + '</table>')

def sujet(icone, titre, texte, cle):   # une case à cocher du centre de préférences
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 10px;border:1px solid #e4e1d8;border-radius:12px"><tr>'
            f'<td width="44" align="center" valign="middle" style="padding:14px 0 14px 14px;font-size:24px;line-height:1">{icone}</td>'
            f'<td valign="middle" style="padding:14px 12px"><div style="font:{GRAS} 16px/1.3 {SERIF};color:{C["texte"]}">{titre}</div><div style="margin-top:2px;font:14px/1.4 {SANS};color:{C["gris"]}">{texte}</div></td>'
            f'<td width="96" align="right" valign="middle" style="padding:14px 14px 14px 0"><a href="[LIEN_PREFERENCES]?sujet={cle}" style="display:inline-block;padding:8px 14px;border-radius:999px;background:{C["fond"]};font:bold 14px {SANS};color:{C["nuit"]};text-decoration:none;white-space:nowrap">Je veux</a></td></tr></table>')

# Premiers pas des nouveaux abonnés : 3 e-mails, on sort de la série dès qu'on a utilisé le service présenté
mail(id="58-premiers-pas-tactique", cat=P_DEMARRER, quand="J+1 après la souscription d'un Pack Jeu+ ou d'un Pack Intégral, sauf s'il a déjà résolu un exercice" + INFO_PROPOSITION,
     objet="Votre premier défi tactique vous attend", pre="Des milliers d'exercices en illimité et un mode challenge : battez votre premier record aujourd'hui.", sur="Bien démarrer · 1/3", titre="Votre premier | défi tactique.",
     corps=[para("Bonjour [PSEUDO], votre <b>[SERVICE]</b> vous ouvre la zone d'entraînement tactique en illimité. Le meilleur moyen de commencer :"),
            etapes([("Ouvrez la zone d'entraînement", "Les exercices sont en illimité avec votre Pack : résolvez-en autant que vous voulez."),
                    ("Lancez le mode challenge", "Enchaînez les exercices et visez le meilleur score."),
                    ("Battez votre record", "Revenez demain pour faire mieux : quelques minutes par jour suffisent pour progresser.")]),
            bouton("Résoudre mon premier exercice", "https://www.europe-echecs.com/exercice-tactique")])
mail(id="59-premiers-pas-videos", cat=P_DEMARRER, quand="J+3 après la souscription d'un Pack Intégral, sauf s'il a déjà regardé une vidéo" + INFO_PROPOSITION,
     objet="Vos 4 rendez-vous vidéo de la semaine", pre="Stratégie le lundi, légendes le mardi, calcul le mercredi, finales le vendredi : tout est dans votre Pack Intégral.", sur="Bien démarrer · 2/3", titre="Vos rendez-vous | vidéo.",
     corps=[para("Bonjour [PSEUDO], chaque semaine, plus de 4 nouvelles vidéos vous attendent avec votre <b>Pack Intégral</b>. Voici les dernières :"),
            video_semaine(1, "La Minute Stratégie", "Lundi"), video_semaine(2, "Coup de Légende", "Mardi"),
            bouton("Voir toutes les vidéos", L("VIDEOS")),
            para(petit("Calcul Gagnant le mercredi et La Minute Finale le vendredi complètent la semaine. Toutes les anciennes vidéos restent disponibles à la demande."))])
mail(id="60-premiers-pas-revue", cat=P_DEMARRER, quand="J+7 après la souscription d'un Pack Intégral, sauf s'il a déjà ouvert la revue en ligne" + INFO_PROPOSITION,
     objet="Votre revue Europe Échecs est aussi en ligne", pre="Le dernier numéro est inclus dans votre Pack Intégral, avec ses parties à rejouer coup par coup.", sur="Bien démarrer · 3/3", titre="Votre revue, | en ligne.",
     corps=[para("Bonjour [PSEUDO], le saviez-vous ? La revue Europe Échecs est incluse dans votre <b>Pack Intégral</b>. Voici le numéro du mois :"),
            couverture(),
            bouton("Lire la revue", "[LIEN_REVUE_EN_LIGNE]"),
            para(petit("Les parties commentées sont à rejouer en ligne, coup par coup, sur l'échiquier."))],
     sign="Bonne lecture,<br><b>L'équipe d'Europe Échecs</b>")

# Abonné payant qui décroche
mail(id="61-abonne-inactif", cat=P_DEMARRER, quand="Abonnés payants sans aucune vidéo, exercice ni partie depuis 21 jours, une seule fois par période d'inactivité" + INFO_PROPOSITION,
     objet="Ce que vous avez manqué ces 3 semaines", pre="De nouvelles vidéos et de nouveaux exercices vous attendent dans votre [SERVICE].", sur="Votre abonnement", titre="Ça vous attend | depuis 3 semaines.",
     corps=[para("Bonjour [PSEUDO], depuis votre dernière visite, votre <b>[SERVICE]</b> s'est enrichi. Quelques minutes suffisent pour reprendre :"),
            video_semaine(3, "Calcul Gagnant", "Mercredi"), video_semaine(4, "La Minute Finale", "Vendredi"),
            bouton("Reprendre là où j'en étais", L("VIDEOS")),
            para(petit("Envie de jouer plutôt ? Une partie vous attend dans la zone de jeu, à la cadence de votre choix."))])

# D'un produit à l'autre
mail(id="62-livre-auteur-en-video", cat=P_PONTS, quand="15 jours après la livraison d'un livre dont l'auteur a des vidéos sur Europe Échecs, à ceux qui n'ont pas le Pack Intégral" + INFO_PROPOSITION,
     objet="[AUTEUR_LIVRE] vous attend aussi en vidéo", pre="L'auteur de votre livre présente [SERIE_AUTEUR] chaque semaine sur Europe Échecs.", sur="De la page à l'écran", titre="Votre auteur, | en vidéo.",
     corps=[para("Bonjour [PRENOM_CLIENT], vous lisez le livre de <b>[AUTEUR_LIVRE]</b> ? Il vous donne aussi rendez-vous chaque semaine sur Europe Échecs, en vidéo :"),
            coach("[AUTEUR_LIVRE]", "[TITRE_AUTEUR]", "[URL_PHOTO_AUTEUR]", "[SERIE_AUTEUR] chaque [JOUR_SERIE_AUTEUR]"),
            video_semaine(4, "La Minute Finale", "Vendredi"),
            bouton("Découvrir le Pack Intégral", L("ABONNEMENTS")),
            para(petit("Toutes ses vidéos, et celles de nos autres auteurs, sont incluses dans le Pack Intégral."))])
mail(id="63-choisir-ses-emails", cat=P_PONTS, quand="J+2 après la création d'un compte, une seule fois (et lien permanent dans le pied des e-mails d'information)" + INFO_PROPOSITION,
     objet="Choisissez ce que vous voulez recevoir", pre="Actualités, vidéos, problème de la semaine, boutique : cochez ce qui vous intéresse, rien de plus.", sur="Vos e-mails", titre="À vous | de choisir.",
     corps=[para("Bonjour [PSEUDO], pour ne recevoir que ce qui vous intéresse, choisissez vos sujets :"),
            sujet("📰", "L'actualité des échecs", "La newsletter : tournois, interviews, analyses", "actualites"),
            sujet("🎬", "Les vidéos de la semaine", "Le dimanche, le récapitulatif des nouvelles vidéos", "videos"),
            sujet("♟️", "Le problème de la semaine", "Une position à résoudre, la solution en un clic", "probleme"),
            sujet("📖", "La revue", "Le sommaire de chaque nouveau numéro", "revue"),
            sujet("🛍️", "La boutique", "Livres, échiquiers et offres du moment", "boutique"),
            para(petit("Vous pourrez changer d'avis à tout moment dans « Mon compte ». Les e-mails liés à votre compte et à vos commandes sont toujours envoyés."))])

_I.open(ICI / "assets/captures/ee/hd/auth-quenehen.jpg").convert("RGB").resize((200, 200)).save(APER / "img/auteur-exemple.jpg", quality=88)
EXEMPLES.update({"AUTEUR_LIVRE": "Marc Quenehen", "TITRE_AUTEUR": "Auteur", "URL_PHOTO_AUTEUR": "img/auteur-exemple.jpg", "SERIE_AUTEUR": "La Minute Finale", "JOUR_SERIE_AUTEUR": "vendredi",
    "TITRE_VIDEO_1": "Minute Stratégie #282", "TITRE_VIDEO_2": "Coup de Légende #148", "TITRE_VIDEO_3": "Calcul Gagnant #147", "TITRE_VIDEO_4": "Minute Finale #222"})

# Exemples des aperçus : vraies séries et vrais auteurs du catalogue vidéo ; jours, titres et prix restent à fournir
from PIL import Image as _I
for _n, _f in ((1, "p-minute-strategie"), (2, "p-coup-de-legende"), (3, "p-calcul-gagnant"), (4, "p-minute-finale")):
    _im = _I.open(ICI / f"assets/captures/ee/hd/{_f}.jpg").convert("RGB"); _im.thumbnail((1072, 603)); _im.save(APER / f"img/video-exemple-{_n}.jpg", quality=84)
EXEMPLES.update({"MOIS": "décembre 2026", "CARTE_4_CHIFFRES": "4242", "MOIS_EXPIRATION": "décembre", "DATE_PROCHAIN_PAIEMENT": "18/01/2027",
    "MOYEN_PAIEMENT": "Carte •••• 4242", "PRIX_MENSUEL": "11,90 € par mois", "PRIX_ANNUEL": "99,90 € pour 1 an", "PRIX_2ANS": "149,90 €", "ECONOMIE": "42,90 €", "MONTANT": "11,90 €", "NB_SEMAINES": "[NB_SEMAINES]", "DATE_ENVOI": "23 novembre",
    "AUTEUR_4": "Marc Quenehen", "URL_MINIATURE_4": "img/video-exemple-4.jpg", "AUTEUR_1": "Marc Quenehen", "URL_MINIATURE_1": "img/video-exemple-1.jpg",
    "AUTEUR_2": "Romuald De Labaca (MF)", "URL_MINIATURE_2": "img/video-exemple-2.jpg",
    "AUTEUR_3": "Sylvain Ravot (MF)", "URL_MINIATURE_3": "img/video-exemple-3.jpg"})
for _k in ("NOUVEAUTE_1", "NOUVEAUTE_2", "NOUVEAUTE_3"): EXEMPLES[_k] = "[" + _k + "]"   # aucune nouveauté inventée

for e in E:   # exemples propres à un e-mail
    if e["id"] == "09-paiement-recu": e["exemples"] = {"PRODUIT": "Pack Intégral · 1 an", "MONTANT": "99,90 €", "PRIX_LIGNE": "99,90 €", "TOTAL": "99,90 €"}
TITRES = {}
MASCOTTES = {}
ENTETES = {}
# Exemples des aperçus : seulement des valeurs neutres. Les prix et montants restent affichés comme variables (aucun tarif n'est inventé).
EXEMPLES.update({"PSEUDO": "LéaDame", "CODE_ACTIVATION": "7Q4K-29", "MOT_DE_PASSE": "••••••••", "GESTIONNAIRE": "CoachMarc", "SERVICES_MULTICOMPTE": "Pack Jeu+",
    "DATE_SUPPRESSION": "18/11/2026", "HEURE_SUPPRESSION": "14:32", "CODE_PROMO": "EE25-8XK2", "SERVICE": "Pack Intégral", "PACK": "Pack Intégral",
    "DATE_FIN": "18/12/2026", "NUMERO_COMMANDE": "245871", "PRODUIT": "Pack Jeu+", "QUANTITE": "1", "ECHEANCE": "janvier 2027", "NUMERO_ABONNE": "10427",
    "PRODUIT_CADEAU": "Pack Intégral", "CODE_CADEAU": "K7P2-9QX4", "EMAIL_CONTACT": "[EMAIL_CONTACT]"})

exec((ICI / "scripts/emails-contenu-ee-site.py").read_text())   # tous les autres modèles actuels du site (65 à 122)
# Logo décliné par rubrique (forme officielle, couleur seule changée) : on reconnaît le type d'e-mail d'un coup d'œil
LOGO_RUBRIQUE = {"Compte": "logo-blanc", "Découverte": "logo-jaune", "Abonnement": "logo", "Nouvelles formules": "logo-jaune", "Revue": "logo-blanc", "Cadeaux": "logo-jaune", P_PAIEMENT: "logo", P_FIDELITE: "logo-jaune", P_GRATUITS: "logo-jaune", P_NEWS: "logo-blanc", P_BOUTIQUE: "logo-jaune", P_TEMPS: "logo-jaune", P_RDV: "logo-blanc", P_CHIFFRES: "logo", P_FIDELE: "logo", P_COMMANDE: "logo-jaune", P_DEMARRER: "logo-blanc", P_PONTS: "logo-jaune"}
LOGO_RUBRIQUE.update(LOGO_SITE)
for e in E: e["logo"] = LOGO_RUBRIQUE[e["cat"]]
# Identité visuelle : damier sous l'en-tête, pièce en filigrane par rubrique, pied marine
DAMIER = PIED_NUIT = True
PIECE_RUBRIQUE = {"Compte": "K", "Découverte": "N", "Abonnement": "Q", "Nouvelles formules": "Q", "Revue": "R", "Cadeaux": "B",
                  P_PAIEMENT: "R", P_FIDELITE: "K", P_GRATUITS: "N", P_NEWS: "B", P_BOUTIQUE: "P", P_TEMPS: "N", P_RDV: "R", P_CHIFFRES: "K", P_FIDELE: "Q", P_COMMANDE: "P", P_DEMARRER: "N", P_PONTS: "B"}
PIECE_RUBRIQUE.update(PIECE_SITE)
