# Contenu des e-mails du site europe-echecs.com (Europe Échecs) : compte, abonnements, nouvelles formules, revue papier, cartes cadeaux.
# Réécrits à partir des modèles actuels du site (relevé du 22 novembre 2026, voir pack/EMAILS-EE.md) et des 4 textes des nouvelles formules
# (Pack Jeu+, Pack Intégral, fin du Pack Jeu et du Pack Progresser). Vouvoiement, comme sur le site.
# Rien n'est ajouté aux sources : ni prix, ni délai, ni service qui n'y figure pas. Les prix restent des variables.
# Exécuté par scripts/emails.py (python3 scripts/emails.py ee), qui fournit les composants et le design.

# ---------- Réglages de la série ----------
C["em"] = "#1f6fc0"                 # bleu d'action du site (surtitre, suite du titre)
C["nuit"] = "#191f38"               # marine du site (en-tête, bloc calendrier)
C["bouton"] = "#fae361"; C["bouton_texte"] = "#191f38"   # boutons : jaune Europe Échecs, texte marine
C["jaune"] = "#fae361"              # jaune Europe Échecs (#FAE361, celui des pages de la revue) : filets d'encadré
C["clair"] = "#fae361"              # jaune : surtitre et suite du titre sur le bandeau marine, filet sous l'en-tête, pastille du Pack Intégral
TITRE_SUR_NUIT = True                # surtitre et titre dans le bandeau marine, sous le logo
# Palette déclinée de la charte du site (marine #191F38, bleu de marque #58ACFF, bleu d'action #1F6FC0, gris-bleu #6C7497) :
# les teintes crème de l'Académie deviennent des gris-bleus froids, partout (styles et règles du mode sombre)
REMAP = {"#f1f0ea": "#edf1f8",   # fond de page, encadrés, tuiles, tableaux
         "#1d1d1b": "#1a2140",   # texte : marine
         "#6b6b66": "#5d6480",   # texte secondaire : gris-bleu du site
         "#e4e1d8": "#dfe4ee",   # filets
         "#f4f1ea": "#eef1f7"}   # texte en mode sombre
DARK = DARK.replace("</style>", """@media (prefers-color-scheme: dark) {
  [style*="background:#e6f1ff"] { background:#1b2a44 !important; }
  [style*="border:1px solid #2c3658"] { border-color:#3a4670 !important; }
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
MENTION = "Europe Échecs · [ADRESSE_POSTALE]"
DOC = ICI / "pack/EMAILS-EE.md"
TARIFS = "https://www.europe-echecs.com/abonnement.html#table-rates-title"
TARIFS_REVUE = "https://www.europe-echecs.com/abonnement.html#price-revue"
petit = lambda t: f'<span style="color:#6b6b66;font-size:14px">{t}</span>'

def formule(nom, accroche, texte, phare=False):   # une formule proposée (sans prix : ils restent sur la page des abonnements) ; phare : sur fond marine, avec sa pastille
    if phare:
        return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 12px;border-collapse:separate"><tr>'
                f'<td bgcolor="{C["nuit"]}" style="background:{C["nuit"]};border:1px solid #2c3658;border-radius:14px;padding:18px 20px">'
                f'<div style="display:inline-block;margin:0 0 10px;padding:4px 10px;border-radius:999px;background:{C["clair"]};font-family:{SANS};font-weight:800;font-size:12px;letter-spacing:.06em;text-transform:uppercase;color:#0d1430">{accroche}</div>'
                f'<div style="font-family:{SERIF};font-weight:{GRAS};font-size:20px;line-height:1.25;color:#ffffff">{nom}</div>'
                f'<div style="margin-top:6px;font:16px/1.55 {SANS};color:#d3d8e6">{texte}</div></td></tr></table>')
    return (f'<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:0 0 12px;border-collapse:separate"><tr>'
            f'<td bgcolor="#e6f1ff" style="background:#e6f1ff;border-left:5px solid #58acff;border-radius:14px;padding:18px 20px">'
            f'<div style="font-family:{SERIF};font-weight:{GRAS};font-size:20px;line-height:1.25;color:{C["texte"]}">{nom}'
            + (f' <span style="font-weight:400;color:{C["em"]}">· {accroche}</span>' if accroche else "") + '</div>'
            f'<div style="margin-top:6px;font:16px/1.55 {SANS};color:{C["texte"]}">{texte}</div></td></tr></table>')
JEU_PLUS = formule("Pack Jeu+", "", "Accédez à toutes les fonctionnalités premium de la zone de jeu et à la zone d'entraînement tactique en illimité. Idéal pour jouer et progresser chaque jour !")
INTEGRAL = formule("Pack Intégral", "Le choix des passionnés", "Débloquez l'ensemble de nos contenus : vidéos à la demande, leçons, revue en ligne… et plus de 4 nouvelles vidéos chaque semaine pour continuer votre progression.", phare=True)
def identifiants(): return infos([("Pseudo", "[PSEUDO]"), ("Mot de passe", "[MOT_DE_PASSE]")])

# ---------- 1. Compte ----------
mail(id="01-activation-compte", cat="Compte", marketing=False, quand="À la création du compte, si une activation est nécessaire (modèle account_confirmation)",
     objet="Bienvenue ! Activez votre compte Europe Échecs", pre="Un clic, et la partie peut commencer.", sur="Votre compte", titre="Plus qu'un clic, | [PSEUDO] !",
     corps=[para("Nous sommes ravis de vous compter parmi nous. Il ne reste qu'une étape : activer votre compte."), bouton("Activer mon compte", L("ACTIVATION")),
            para(petit("Code d'activation à fournir si demandé : <b style='white-space:nowrap'>[CODE_ACTIVATION]</b>")),
            para("Une fois votre compte activé, tout Europe Échecs vous attend :"),
            liste([f'<a href="{L("ZONE_DE_JEU")}" style="color:#1f6fc0;font-weight:700">La zone de jeu</a>, pour jouer et vous entraîner', f'<a href="{L("VIDEOS")}" style="color:#1f6fc0;font-weight:700">Nos vidéos</a>',
                   f'<a href="{L("REVUE")}" style="color:#1f6fc0;font-weight:700">Notre revue</a>', '<a href="https://boutique.echecs.com" style="color:#1f6fc0;font-weight:700">Nos livres</a>, sur boutique.echecs.com']),
            para(f'Une question ? <a href="{L("AIDE")}" style="color:#1f6fc0;font-weight:700">Contactez-nous</a>, nous vous répondrons avec plaisir.')])
mail(id="02-compte-multicompte", cat="Compte", marketing=False, quand="À la création d'un compte par le gestionnaire d'une offre multicompte (modèle account_confirmation, variante multicompte)",
     objet="Votre compte Europe Échecs est prêt", pre="Créé par [GESTIONNAIRE] : vos identifiants et vos services.", sur="Votre compte", titre="Bienvenue, | [PSEUDO] !",
     corps=[para("Votre compte a été créé par le gestionnaire <b>[GESTIONNAIRE]</b>, dans le cadre d'une offre multicompte dont il assure la gestion. Elle vous donne accès à : <b>[SERVICES_MULTICOMPTE]</b>."),
            para("Voici vos identifiants de connexion :"), identifiants(),
            bouton("Activer mon compte", L("ACTIVATION")),
            para(petit("Pour plus de sécurité, changez votre mot de passe dans la rubrique <a href=\"[LIEN_MON_COMPTE]\" style=\"color:#6b6b66\">« Mon compte »</a>."))])
mail(id="03-mot-de-passe", cat="Compte", marketing=False, quand="Sur demande de réinitialisation (modèle resetpass)",
     objet="Réinitialisez votre mot de passe Europe Échecs", pre="Ce lien est valable 1 heure.", sur="Votre compte", titre="Un nouveau | mot de passe.",
     corps=[para("À la suite de votre demande sur le site, voici un lien pour réinitialiser le mot de passe de votre pseudo <b>[PSEUDO]</b>."), bouton("Choisir mon mot de passe", L("MOT_DE_PASSE")),
            para(petit("Attention : ce lien n'est valable que pendant 1 heure. Si vous n'êtes pas à l'origine de cette demande, ignorez cet e-mail : votre mot de passe ne change pas."))])
mail(id="04-suppression-compte", cat="Compte", marketing=False, quand="Après la suppression du compte (modèle deletion_request_perform)",
     objet="Suppression de votre compte Europe Échecs", pre="Votre compte et ses données ont été supprimés.", sur="Votre compte", titre="Votre compte | est supprimé.",
     corps=[para("Votre compte <b>[PSEUDO]</b> a bien été supprimé, ainsi que les données qui lui sont associées."),
            infos([("Date", "[DATE_SUPPRESSION]"), ("Heure", "[HEURE_SUPPRESSION] (GMT)")])],
     sign="Cordialement,<br><b>L'équipe d'Europe Échecs</b>")

# ---------- 2. Découverte ----------
mail(id="05-decouverte-zone-de-jeu", cat="Découverte", quand="Après la première connexion à la zone de jeu SimpleChess (modèle welcome_directplay)",
     objet="Bienvenue sur la zone de jeu !", pre="Cadences, tournois, analyse : ce que vous pouvez y faire.", sur="Zone de jeu", titre="Bienvenue | dans la communauté.",
     corps=[para("Bonjour [PSEUDO] ! Vous avez effectué votre première connexion à notre zone de jeu SimpleChess : nous espérons que l'expérience vous a plu. Voici ce que vous pouvez y faire en tant que membre."),
            liste(["<b>Cadences et force de l'adversaire</b> : choisissez vos cadences et la force de votre adversaire. Gagner contre plus fort que vous rapporte plus de points.",
                   "<b>La discussion</b> : échangez en direct avec vos amis ou n'importe quel joueur, dans le respect de la charte de la zone de jeu.",
                   "<b>Vos listes de joueurs</b> : cliquez sur un pseudo pour l'ajouter à vos amis (vous êtes prévenu de son arrivée) ou à votre liste noire (il ne peut plus vous écrire ni vous défier).",
                   "<b>Les parties des plus forts</b> : observez les parties en cours, et retrouvez les 10 dernières parties de chaque joueur sur son profil.",
                   "<b>L'analyse</b> : à la fin de chaque partie, revoyez-la avec un regard critique ; vous pouvez aussi analyser celles que vous observez.",
                   "<b>Les tournois</b> : participez, ou créez votre petit tournoi et invitez vos amis.",
                   "<b>Votre connexion</b> : un rapport détaillé après chaque partie, si vous pensez avoir perdu à cause d'une coupure."]),
            bouton("Jouer une partie", L("ZONE_DE_JEU"))])
mail(id="06-offre-de-bienvenue", cat="Découverte", quand="Offre de bienvenue après l'inscription, valable 48 h (modèle welcome_subscription_48h)",
     objet="Votre offre de bienvenue : −25 % pendant 48 h", pre="Sur tous nos Packs Web 1 et 2 ans, avec votre code.", sur="Offre de bienvenue", titre="−25 % | pour bien commencer.",
     corps=[para("Bonjour [PSEUDO] ! Nous sommes heureux de vous compter parmi nos joueurs. Pour découvrir nos services, profitez d'un tarif avantageux :"),
            tuiles([("−25&nbsp;%", "sur tous nos Packs Web 1 et 2 ans"), ("48&nbsp;h", "pour en profiter")]),
            para("Saisissez ce code dans votre panier :"),
            infos([("Votre code", "[CODE_PROMO]")]),
            bouton("C'est parti !", TARIFS),
            para(petit("Offre valable jusqu'à 48 heures après la réception de cet e-mail. Besoin d'aide ? Parcourez nos <a href=\"[LIEN_FAQ]\" style=\"color:#6b6b66\">questions fréquentes</a> ou <a href=\"[LIEN_AIDE]\" style=\"color:#6b6b66\">contactez-nous</a>."))])

# ---------- 3. Abonnement ----------
mail(id="07-bienvenue-abonnement", cat="Abonnement", marketing=False, quand="À la création du compte lors d'un abonnement (modèle welcome_subscription)",
     objet="Bienvenue sur Europe Échecs !", pre="Vos identifiants, et par où commencer.", sur="Bienvenue", titre="Bienvenue | parmi nous !",
     corps=[para("Merci pour votre abonnement ! Voici vos identifiants de connexion :"), identifiants(),
            bouton("Me connecter", L("CONNEXION")),
            para(petit("Pour plus de sécurité, changez votre mot de passe dans la rubrique <a href=\"[LIEN_MON_COMPTE]\" style=\"color:#6b6b66\">« Mon compte »</a>. Besoin d'aide ? Parcourez nos <a href=\"[LIEN_FAQ]\" style=\"color:#6b6b66\">questions fréquentes</a> ou <a href=\"[LIEN_AIDE]\" style=\"color:#6b6b66\">contactez-nous</a>."))])
mail(id="08-abonnement-mis-en-place", cat="Abonnement", marketing=False, quand="À la mise en place d'un abonnement à paiement récurrent (modèle recurpmt_created)",
     objet="Mise en place de votre abonnement [SERVICE]", pre="Votre abonnement récurrent est en place.", sur="Votre abonnement", titre="Votre abonnement | est en place.",
     corps=[para("Votre abonnement récurrent <b>[SERVICE]</b> a été mis en place avec succès pour votre compte <b>[PSEUDO]</b>."),
            para("La prise en compte de votre première mensualité peut demander quelques heures."),
            bouton("Gérer mon abonnement", L("MES_SERVICES")),
            para(petit("Vous pouvez gérer votre abonnement à tout moment dans la rubrique « Mon compte »."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="09-paiement-recu", cat="Abonnement", marketing=False, quand="À la réception d'un paiement de commande (modèle cmdpmtreceived)",
     objet="Votre commande n° [NUMERO_COMMANDE]", pre="Paiement reçu : votre commande est traitée.", sur="Commande n° [NUMERO_COMMANDE]", titre="Paiement reçu, | merci !",
     corps=[para("Nous avons bien reçu votre paiement de <b>[MONTANT]</b> pour la commande n° [NUMERO_COMMANDE], et nous vous en remercions. Votre commande a été traitée : si vous avez souscrit des services, ils sont activés."),
            recu([("[PRODUIT] · Qté [QUANTITE]", "[PRIX_LIGNE]"), ("Participation aux frais de port et d'emballage", "[FRAIS_PORT]")], "Total TTC", "[TOTAL]"),
            para(petit("Une ligne par produit commandé. La ligne des frais de port n'apparaît que s'ils sont supérieurs à zéro."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")
mail(id="10-abonnement-echeance", cat="Abonnement", quand="Avant l'échéance d'un abonnement web, 1re et 2e relance (modèles relance1web et relance2web, identiques)",
     objet="Votre abonnement Europe Échecs arrive à échéance", pre="[PACK] : jusqu'au [DATE_FIN].", sur="Votre abonnement", titre="Continuez | sans interruption.",
     corps=[para("Votre abonnement arrive bientôt à échéance (compte <b>[PSEUDO]</b>). Renouvelez-le, et continuez de profiter de vos services sans interruption !"),
            infos([("Formule", "[PACK]"), ("Fin de l'abonnement", "[DATE_FIN]")]),
            bouton("Renouveler mon abonnement", L("ABONNEMENTS")),
            para(petit("Nouveau : vous pouvez aussi opter pour le paiement mensuel, plus souple et sans engagement."))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")
mail(id="11-abonnement-annule", cat="Abonnement", marketing=False, quand="À l'annulation d'un abonnement récurrent (modèle recurpmt_cancelled)",
     objet="Annulation de votre abonnement [SERVICE]", pre="Votre abonnement ne sera plus facturé.", sur="Votre abonnement", titre="Votre abonnement | est annulé.",
     corps=[para("Votre abonnement <b>[SERVICE]</b> a été annulé pour votre compte <b>[PSEUDO]</b>. À partir d'aujourd'hui, il ne fera plus l'objet d'aucune facturation."),
            para("Vous pouvez vous réabonner à tout moment depuis la page des tarifs, à l'année ou au mois."), bouton("Voir les tarifs", TARIFS),
            para(petit("Une remarque, une suggestion ? <a href=\"[LIEN_AIDE]\" style=\"color:#6b6b66\">Écrivez-nous</a> : votre avis nous aide."))],
     sign="Merci de votre confiance,<br><b>L'équipe d'Europe Échecs</b>")

# ---------- 4. Nouvelles formules ----------
mail(id="12-pack-jeu-devient-jeu-plus", cat="Nouvelles formules", marketing=False, quand="Une fois, aux abonnés du Pack Jeu en cours (passage gratuit au Pack Jeu+)",
     objet="Votre Pack Jeu devient gratuitement le Pack Jeu+", pre="L'entraînement tactique en illimité est inclus dès maintenant.", sur="Bonne nouvelle", titre="Votre Pack Jeu | devient le Pack Jeu+.",
     corps=[para("Bonjour [PSEUDO], bonne nouvelle : votre abonnement Pack Jeu évolue <b>gratuitement</b> vers le Pack Jeu+ !"),
            para("En plus de toutes les fonctionnalités premium de la zone de jeu, vous bénéficiez dès maintenant d'un accès illimité à notre module d'entraînement tactique :"),
            liste(["<b>Des milliers d'exercices</b>", "<b>Un mode challenge</b>, pour vous tester et tenter de battre votre record"]),
            bouton("Découvrir l'entraînement tactique", L("ENTRAINEMENT_TACTIQUE")),
            para("Le Pack Jeu+ remplace désormais le Pack Jeu, pour une expérience plus riche et plus complète. À la fin de votre abonnement, vous pourrez le prolonger à l'année, ou avec notre nouvelle formule mensuelle.")])
mail(id="13-pack-progresser-en-cours", cat="Nouvelles formules", marketing=False, quand="Une fois, aux abonnés du Pack Progresser en cours",
     objet="Votre Pack Progresser : ce qui change", pre="Et deux nouvelles formules pour la suite.", sur="Nouvelles formules", titre="Rien ne change | pour l'instant.",
     corps=[para("Bonjour [PSEUDO], merci pour votre fidélité ! Le Pack Progresser n'existe plus : il a été remplacé par d'autres offres, mieux adaptées aux besoins exprimés par les utilisateurs que nous avons interrogés."),
            para("Rassurez-vous : jusqu'à la fin de votre abonnement, rien ne change, et vous profitez des mêmes services. Ensuite, deux formules vous seront proposées :"),
            JEU_PLUS, INTEGRAL,
            encadre("<b>Nouveauté :</b> vous pourrez opter pour le paiement mensuel, plus souple et sans engagement."),
            bouton("Découvrir les deux formules", L("ABONNEMENTS"))])
mail(id="14-pack-progresser-expire", cat="Nouvelles formules", quand="À l'échéance d'un abonnement Pack Progresser",
     objet="Votre Pack Progresser est arrivé à échéance", pre="Pack Jeu+ ou Pack Intégral : à vous de choisir.", sur="Nouvelles formules", titre="Choisissez | votre nouvelle formule.",
     corps=[para("Bonjour [PSEUDO], votre abonnement au Pack Progresser est arrivé à échéance. Cette formule n'existe plus : elle a été remplacée par d'autres offres, mieux adaptées aux besoins exprimés par les utilisateurs que nous avons interrogés."),
            para("Pour continuer à vivre votre passion sur Europe Échecs, deux formules vous attendent :"),
            JEU_PLUS, INTEGRAL,
            encadre("<b>Nouveauté :</b> vous pouvez désormais opter pour le paiement mensuel, plus souple et sans engagement."),
            bouton("Choisir ma formule", L("ABONNEMENTS"))],
     sign="Merci de votre fidélité !<br><b>L'équipe d'Europe Échecs</b>")
mail(id="15-pack-jeu-expire", cat="Nouvelles formules", quand="À l'échéance d'un abonnement Pack Jeu",
     objet="Votre Pack Jeu est arrivé à échéance", pre="Pack Jeu+ ou Pack Intégral : à vous de choisir.", sur="Nouvelles formules", titre="Choisissez | votre nouvelle formule.",
     corps=[para("Bonjour [PSEUDO], votre abonnement au Pack Jeu est arrivé à échéance. Cette formule n'existe plus : elle a été remplacée par d'autres offres, mieux adaptées aux besoins exprimés par les utilisateurs que nous avons interrogés."),
            para("Pour continuer à vivre votre passion sur Europe Échecs, deux formules vous attendent :"),
            JEU_PLUS, INTEGRAL,
            encadre("<b>Nouveauté :</b> vous pouvez désormais opter pour le paiement mensuel, plus souple et sans engagement."),
            bouton("Choisir ma formule", L("ABONNEMENTS"))],
     sign="Merci de votre fidélité !<br><b>L'équipe d'Europe Échecs</b>")

# ---------- 5. Revue ----------
mail(id="16-revue-echeance", cat="Revue", quand="Avant la fin d'un abonnement à la revue papier, 1re et 2e relance (modèles relance1ee et relance2ee, identiques)",
     objet="Votre abonnement à la revue Europe Échecs se termine", pre="Réabonnez-vous pour ne manquer aucun numéro.", sur="La revue", titre="Votre dernier numéro | arrive en [ECHEANCE].",
     corps=[para("Bonjour [PSEUDO], votre abonnement à la revue <i>Europe Échecs</i> arrive à échéance en <b>[ECHEANCE]</b> : c'est ce mois-là que vous recevrez le dernier numéro de votre abonnement en cours."),
            para("Pour ne pas en interrompre l'envoi, réabonnez-vous dès maintenant :"),
            bouton("Me réabonner", TARIFS_REVUE),
            para(petit("Une question ? Écrivez-nous à <a href=\"mailto:[EMAIL_CONTACT]?subject=Abonnement%20Europe%20Echecs%20n%C2%B0%20[NUMERO_ABONNE]\" style=\"color:#6b6b66\">[EMAIL_CONTACT]</a>, en rappelant votre numéro d'abonné ([NUMERO_ABONNE]). Si ce message a croisé votre règlement, merci de ne pas en tenir compte."))],
     sign="Merci de votre fidélité,<br><b>Le service abonnement</b>")

# ---------- 6. Cadeaux ----------
mail(id="17-carte-cadeau", cat="Cadeaux", marketing=False, quand="Après l'achat d'un Pack cadeau (modèle gift_code)",
     objet="Votre commande cadeau", pre="Le code à offrir, et la carte cadeau à imprimer.", sur="Votre cadeau", titre="Votre cadeau | est prêt à offrir !",
     corps=[para("Bonjour [PSEUDO], merci d'avoir acheté l'un de nos Packs cadeaux. Voici votre code :"),
            infos([("[PRODUIT_CADEAU]", "[CODE_CADEAU]")]),
            bouton("Télécharger la carte cadeau", L("CARTE_CADEAU_PDF")),
            para("La carte cadeau au format PDF est prête à imprimer ou à envoyer. Pour la télécharger, connectez-vous avec le compte qui a servi à passer la commande."),
            para('Pour activer le code, rendez-vous sur <a href="https://www.europe-echecs.com/activer-mon-code-cadeau.html" style="color:#1f6fc0;font-weight:700">europe-echecs.com/activer-mon-code-cadeau</a>.'),
            para(petit(f'Plusieurs codes ? Ils sont listés un par un, et un bouton permet de les télécharger tous dans un seul PDF. Le contenu de chaque Pack est détaillé sur notre <a href="{TARIFS}" style="color:#6b6b66">page des tarifs</a>.'))])

TITRES = {}
MASCOTTES = {}
ENTETES = {}
# Exemples des aperçus : seulement des valeurs neutres. Les prix et montants restent affichés comme variables (aucun tarif n'est inventé).
EXEMPLES.update({"PSEUDO": "LéaDame", "CODE_ACTIVATION": "7Q4K-29", "MOT_DE_PASSE": "••••••••", "GESTIONNAIRE": "CoachMarc", "SERVICES_MULTICOMPTE": "Pack Jeu+",
    "DATE_SUPPRESSION": "18/11/2026", "HEURE_SUPPRESSION": "14:32", "CODE_PROMO": "EE25-8XK2", "SERVICE": "Pack Intégral", "PACK": "Pack Intégral",
    "DATE_FIN": "18/12/2026", "NUMERO_COMMANDE": "245871", "PRODUIT": "Pack Jeu+", "QUANTITE": "1", "ECHEANCE": "janvier 2027", "NUMERO_ABONNE": "10427",
    "PRODUIT_CADEAU": "Pack Intégral", "CODE_CADEAU": "K7P2-9QX4", "EMAIL_CONTACT": "[EMAIL_CONTACT]"})
