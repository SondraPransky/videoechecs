// Catalogue des visuels du pack réseaux sociaux (rendus par scripts/pack.mjs via src/visuels.html).
// Chaque visuel est décliné dans tous les formats de son groupe ; « theme » fixe l'ambiance de couleur.

// Formats de publication : [suffixe de fichier, largeur, hauteur, usage]
window.FORMATS = {
  posts: [
    ["carre-1080x1080", 1080, 1080, "Post carré Instagram, Facebook, LinkedIn"],
    ["portrait-1080x1350", 1080, 1350, "Post portrait 4:5 Instagram, Facebook"],
    ["story-1080x1920", 1080, 1920, "Story Instagram, Facebook, TikTok, couverture de Reel"],
    ["x-1600x900", 1600, 900, "Post X (Twitter)"],
    ["lien-1200x630", 1200, 630, "Lien partagé Facebook, LinkedIn, X"],
    ["pinterest-1000x1500", 1000, 1500, "Épingle Pinterest"],
  ],
};

const START = { a1: "wR", b1: "wN", c1: "wB", d1: "wQ", e1: "wK", f1: "wB", g1: "wN", h1: "wR", a8: "bR", b8: "bN", c8: "bB", d8: "bQ", e8: "bK", f8: "bB", g8: "bN", h8: "bR" };
"abcdefgh".split("").forEach(f => { START[f + "2"] = "wP"; START[f + "7"] = "bP"; });
const MAT1 = { g1: "wK", d1: "wR", f2: "wP", g2: "wP", h2: "wP", g8: "bK", f7: "bP", g7: "bP", h7: "bP", b2: "bQ", a7: "bP" };
const MAT1_OK = Object.assign({}, MAT1, { d8: "wR" }); delete MAT1_OK.d1;

const ICON = {
  lecons: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h6a2 2 0 0 1 2 2v12a2 2 0 0 0-2-2H4zM20 5h-6a2 2 0 0 0-2 2v12a2 2 0 0 1 2-2h6z"/></svg>',
  videos: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4l13 8-13 8z"/></svg>',
  masterclasses: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.5 3 3 6 3s6-1.5 6-3v-5"/><path d="M22 9v6"/></svg>',
  exercices: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1.5" fill="currentColor"/></svg>',
  tournois: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M7 4h10v5a5 5 0 0 1-10 0z"/><path d="M7 6H4a3 3 0 0 0 3 4M17 6h3a3 3 0 0 1-3 4M12 14v4M8 20h8"/></svg>',
  forum: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M4 5h16v10H9l-5 4z"/></svg>',
  revue: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"><path d="M6 2h9l5 5v15H6z"/><path d="M15 2v5h5M9 13h8M9 17h6"/></svg>',
  parties: '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M3 3h9v9H3zM12 12h9v9h-9z"/><path d="M12 3h9v9h-9zM3 12h9v9H3z" opacity=".35"/></svg>',
};

window.VISUELS = [
  // ---- Accroches : un visuel par pan de l'académie, avec une capture du motion
  { id: "01-progression", tpl: "accroche", theme: "nuit", k: "Ta progression", t: "Progresse", e: "à ton rythme.", s: "Du premier coup à plus de 2000.", shot: "progression", pose: "niveau-superieur" },
  { id: "02-valide-chaque-etape", tpl: "accroche", theme: "ciel", k: "Mesure tes progrès", t: "Valide", e: "chaque étape.", s: "Modules, étoiles et courbe Elo.", shot: "progres", pose: "serie-reussie" },
  { id: "03-lecons", tpl: "accroche", theme: "soleil", k: "Leçons interactives", t: "+200 leçons", e: "interactives.", s: "Vidéos, cours, exercices et quiz.", shot: "lecons", pose: "idee" },
  { id: "04-exercices", tpl: "accroche", theme: "craie", k: "Entraînement", t: "+2 000 exercices", e: "à ton niveau.", s: "Du mat en 1 aux finales de tours.", shot: "exercices", pose: "bonne-reponse" },
  { id: "05-videos", tpl: "accroche", theme: "nuit", k: "Europe Échecs · Vidéos", t: "Tout le catalogue", e: "vidéo inclus.", s: "Les séries d'Europe Échecs, en HD.", shot: "videos", pose: "regarde" },
  { id: "06-masterclasses", tpl: "accroche", theme: "rose", k: "Cours en direct", t: "Masterclasses", e: "avec des pros.", s: "MF et GMI en direct, chaque semaine.", shot: "masterclasses", pose: "lecon-terminee" },
  { id: "07-tes-parties", tpl: "accroche", theme: "menthe", k: "Tes parties", t: "Saisis, analyse,", e: "partage.", s: "Ton espace de parties, en PGN.", shot: "parties", pose: "reflexion" },
  { id: "08-revue", tpl: "accroche", theme: "nuit", k: "La revue Europe Échecs", t: "Toute la revue", e: "en PGN interactif.", s: "Chaque mois, le nouveau numéro.", shot: "revue", pose: "lecture" },
  { id: "09-forum", tpl: "accroche", theme: "ciel", k: "Le forum", t: "Rejoins", e: "la communauté.", s: "Pose tes questions, partage tes parties.", shot: "forum", pose: "serie-de-jours" },
  { id: "10-tournois", tpl: "accroche", theme: "soleil", k: "Tournois en ligne", t: "Mesure-toi", e: "aux autres joueurs.", s: "Ouvert à tous les niveaux.", shot: "tournois", pose: "victoire-tournoi" },

  // ---- Chiffres clés
  { id: "11-chiffre-200-lecons", tpl: "chiffre", theme: "soleil", k: "Leçons interactives", n: "+200", t: "leçons", e: "pour progresser.", pose: "hourra" },
  { id: "12-chiffre-2000-exercices", tpl: "chiffre", theme: "nuit", k: "Entraînement", n: "+2<b>&#8239;</b>000", t: "exercices", e: "et quiz.", pose: "bonne-reponse" },
  { id: "13-chiffre-4-formats", tpl: "chiffre", theme: "menthe", k: "Apprends comme tu veux", n: "4", t: "formats", e: "de leçon.", s: "Vidéo, cours écrit, exercice, quiz.", pose: "lit-assise" },

  // ---- Engagement : problème, solution, quiz
  { id: "14-probleme-mat-en-1", tpl: "puzzle", theme: "nuit", k: "Le problème du jour", t: "Mat en 1.", e: "À toi de jouer !", s: "Les Blancs jouent. Ta réponse en commentaire.", pos: MAT1, pose: "reflexion" },
  { id: "15-solution-mat-en-1", tpl: "puzzle", theme: "menthe", k: "La solution", t: "Td8#", e: "le mat du couloir.", s: "Le Roi noir est enfermé par ses propres pions.", pos: MAT1_OK, hl: ["d1", "d8"], arrow: ["d1", "d8"], pose: "hourra" },
  { id: "16-quiz-carlsbad", tpl: "quiz", theme: "craie", k: "Quiz · Objectif 1600", q: "Structure Carlsbad : quel est le plan typique des Blancs ?", opts: ["L'attaque de minorité", "Échanger toutes les pièces", "Pousser h4-h5 au plus vite"], s: "Réponds en commentaire : A, B ou C ?", pose: "haussement" },

  // ---- Portraits des coachs
  { id: "17-coach-sylvain-ravot", tpl: "coach", theme: "rose", k: "Nos coachs", t: "Sylvain Ravot", e: "Maître FIDE.", photo: "auth-ravot", titre: "MF" },
  { id: "18-coach-marc-quenehen", tpl: "coach", theme: "menthe", k: "Nos coachs", t: "Marc Quenehen", e: "Entraîneur.", photo: "auth-quenehen" },
  { id: "19-coach-fabien-libiszewski", tpl: "coach", theme: "ciel", k: "Nos coachs", t: "Fabien Libiszewski", e: "Grand Maître.", s: "En masterclass sur echecs.com.", photo: "auth-libiszewski", titre: "GMI" },
  { id: "20-coach-gata-kamsky", tpl: "coach", theme: "soleil", k: "Nos coachs", t: "Gata Kamsky", e: "Grand Maître.", s: "En masterclass sur echecs.com.", photo: "auth-kamsky", titre: "GMI" },

  // ---- Humeurs de la mascotte
  { id: "21-humeur-serie", tpl: "mascotte", theme: "nuit", k: "Ta série", t: "7 jours de suite.", e: "Ne lâche rien !", pose: "serie-de-jours" },
  { id: "22-humeur-lecon-terminee", tpl: "mascotte", theme: "soleil", k: "Bravo", t: "Leçon terminée.", e: "Au tour de la suivante !", pose: "reverence" },
  { id: "23-humeur-rate", tpl: "mascotte", theme: "ciel", k: "Pas grave", t: "Raté ?", e: "C'est comme ça qu'on apprend.", pose: "parapluie" },
  { id: "24-humeur-dodo", tpl: "mascotte", theme: "nuit", k: "Ce soir", t: "Une partie avant de dormir ?", e: "Juste une.", pose: "sieste" },
  { id: "25-humeur-victoire", tpl: "mascotte", theme: "rose", k: "Tournoi du week-end", t: "Premier du tournoi !", e: "Et toi, quand ?", pose: "champion" },
  { id: "26-humeur-idee", tpl: "mascotte", theme: "craie", k: "Astuce du jour", t: "Sors tes pièces", e: "avant ta dame.", pose: "montre-le-ciel" },

  // ---- Annonces
  { id: "27-revue-numero-779", tpl: "revue", theme: "nuit", k: "Nouveau numéro", t: "Le n°779", e: "est sorti !", s: "Milliet & Bacrot : 16 titres pour 2 légendes.", },
  { id: "28-tournois-chaque-semaine", tpl: "event", theme: "ciel", k: "Tournois en ligne", t: "Chaque semaine,", e: "un tournoi.", facts: ["Ouvert à tous les niveaux", "Classement en direct"], pose: "pendule" },

  // ---- Nouvelles mascottes
  { id: "29-newsletter", tpl: "mascotte", theme: "soleil", k: "Newsletter", t: "Ta lettre", e: "de la semaine.", pose: "message-recu" },
  { id: "30-bienvenue", tpl: "mascotte", theme: "ciel", k: "Nouveau membre", t: "Bienvenue", e: "dans l'académie !", pose: "coucou-autre-main" },
  { id: "31-pause-cafe", tpl: "mascotte", theme: "craie", k: "Pause", t: "Une leçon", e: "avec ton café ?", pose: "cafe" },
  { id: "32-forum-discussion", tpl: "mascotte", theme: "menthe", k: "Le forum", t: "Une question ?", e: "La communauté répond.", pose: "discute" },
  { id: "33-objectif-atteint", tpl: "mascotte", theme: "nuit", k: "Objectif atteint", t: "Module validé.", e: "Au suivant !", pose: "drapeau" },
  { id: "34-grande-nouvelle", tpl: "mascotte", theme: "rose", k: "Annonce", t: "Grande nouvelle !", e: "Bientôt sur l'académie.", pose: "pancarte" },
  { id: "35-blancs-ou-noirs", tpl: "mascotte", theme: "craie", k: "Sondage", t: "Blancs ou Noirs ?", e: "Tu joues quoi ?", pose: "blancs-ou-noirs" },
  { id: "36-respire", tpl: "mascotte", theme: "menthe", k: "Avant ta partie", t: "Respire.", e: "Et calcule.", pose: "etirement" },
  { id: "37-oups", tpl: "mascotte", theme: "ciel", k: "Ça arrive", t: "Une gaffe ?", e: "Même aux meilleurs.", pose: "haussement" },
  { id: "38-week-end", tpl: "mascotte", theme: "soleil", k: "C'est le week-end", t: "Une partie ?", e: "Ou deux, ou trois…", pose: "fete" },
  // Quiz supplémentaires (même gabarit que le 16) : la bonne réponse change de place d'un quiz à l'autre
  { id: "39-quiz-roque", tpl: "quiz", theme: "ciel", k: "Quiz · Initiation", q: "Peut-on roquer quand son roi est en échec ?", opts: ["Oui, toujours", "Non, jamais", "Seulement le petit roque"], s: "Réponds en commentaire : A, B ou C ?", pose: "menton" },
  { id: "40-quiz-clouage", tpl: "quiz", theme: "soleil", k: "Quiz · Objectif 1200", q: "Une pièce ne peut pas bouger sans exposer une pièce plus précieuse derrière elle. C'est…", opts: ["Une fourchette", "Une enfilade", "Un clouage"], s: "Réponds en commentaire : A, B ou C ?", pose: "menton" },
  { id: "41-quiz-espagnole", tpl: "quiz", theme: "menthe", k: "Quiz · Objectif 1400", q: "1.e4 e5 2.Cf3 Cc6 3.Fb5 : quelle est cette ouverture ?", opts: ["La partie italienne", "La partie espagnole", "La défense française"], s: "Réponds en commentaire : A, B ou C ?", pose: "reflexion" },
  { id: "42-quiz-colonne-ouverte", tpl: "quiz", theme: "rose", k: "Quiz · Objectif 1400", q: "Où une tour <span style=\"white-space:nowrap\">est-elle</span> la plus active ?", opts: ["Sur une colonne ouverte", "Dans un coin, bien protégée", "Devant ses propres pions"], s: "Réponds en commentaire : A, B ou C ?", pose: "idee" },
  { id: "43-quiz-regle-du-carre", tpl: "quiz", theme: "nuit", k: "Quiz · Objectif 1600", q: "Roi contre pion passé : comment savoir si le roi le rattrape ?", opts: ["La règle de l'opposition", "La règle du carré", "La règle des 50 coups"], s: "Réponds en commentaire : A, B ou C ?", pose: "loupe" },
  { id: "44-quiz-tarrasch", tpl: "quiz", theme: "craie", k: "Quiz · Objectif 1800", q: "Avec un pion passé, où placer ses tours selon la règle de Tarrasch ?", opts: ["Derrière le pion passé", "Devant le pion passé", "Sur la première rangée"], s: "Réponds en commentaire : A, B ou C ?", pose: "lit-assise" },
  { id: "45-quiz-champion-1972", tpl: "quiz", theme: "soleil", k: "Quiz · Culture échecs", q: "Qui fut champion du monde d'échecs de 1972 à 1975 ?", opts: ["Garry Kasparov", "Anatoli Karpov", "Bobby Fischer"], s: "Réponds en commentaire : A, B ou C ?", pose: "cherche" },
  // Quiz inspirés de l'académie : séries vidéo, coachs, leçons, revue
  { id: "46-quiz-minute-finale", tpl: "quiz", theme: "ciel", k: "Quiz · Vidéos", q: "Quelle série vidéo de Marc Quenehen est consacrée aux finales ?", opts: ["Flashback", "La Minute Finale", "Les ouvertures en vogue"], s: "Réponds en commentaire : A, B ou C ?", pose: "regarde" },
  { id: "47-quiz-calcul-gagnant", tpl: "quiz", theme: "rose", k: "Quiz · Nos coachs", q: "Qui présente la série Calcul Gagnant ?", opts: ["Igor Nataf", "Marc Quenehen", "Sylvain Ravot"], s: "Réponds en commentaire : A, B ou C ?", pose: "prof" },
  { id: "48-quiz-gambit-elephant", tpl: "quiz", theme: "menthe", k: "Quiz · Ouvertures", q: "Par quels coups commence le Gambit Éléphant ?", opts: ["1.e4 e5 2.Cf3 d5", "1.d4 d5 2.c4", "1.e4 c5 2.Cf3 d6"], s: "Réponds en commentaire : A, B ou C ?", pose: "reflexion" },
  { id: "49-quiz-herisson", tpl: "quiz", theme: "nuit", k: "Quiz · Stratégie", q: "Dans le Hérisson, où les Noirs placent-ils leurs pions ?", opts: ["a5, b5, d5, e5", "a6, b6, d6, e6", "c5, d5, e5"], s: "Réponds en commentaire : A, B ou C ?", pose: "loupe" },
  { id: "50-quiz-revue-779", tpl: "quiz", theme: "soleil", k: "Quiz · La revue n°779", q: "Milliet et Bacrot : combien de titres de champion de France à eux deux ?", opts: ["9", "12", "16"], s: "Réponds en commentaire : A, B ou C ?", pose: "lecture" },
  { id: "51-quiz-sicilienne", tpl: "quiz", theme: "craie", k: "Quiz · Ouvertures", q: "Par quel coup les Noirs <span style=\"white-space:nowrap\">jouent-ils</span> la défense sicilienne ?", opts: ["1.e4 e6", "1.e4 c5", "1.e4 c6"], s: "Réponds en commentaire : A, B ou C ?", pose: "idee" },
  { id: "52-quiz-mat-du-couloir", tpl: "quiz", theme: "rose", k: "Quiz · Exercices", q: "Le mat du couloir arrive souvent quand…", opts: ["le roi est enfermé par ses propres pions", "la dame est clouée", "les tours sont doublées"], s: "Réponds en commentaire : A, B ou C ?", pose: "menton" },
  { id: "53-quiz-gmi", tpl: "quiz", theme: "ciel", k: "Quiz · Masterclasses", q: "Gata Kamsky est GMI. Que veut dire ce titre ?", opts: ["Grand Maître Initié", "Gagnant Mondial Invaincu", "Grand Maître International"], s: "Réponds en commentaire : A, B ou C ?", pose: "menton" },
  { id: "54-quiz-pion-isole", tpl: "quiz", theme: "menthe", k: "Quiz · Stratégie", q: "Un pion isolé, c'est un pion…", opts: ["bloqué par une pièce adverse", "sans pion de son camp sur les colonnes voisines", "qui a avancé de deux cases"], s: "Réponds en commentaire : A, B ou C ?", pose: "haussement" },
  { id: "55-quiz-formats", tpl: "quiz", theme: "soleil", k: "Quiz · L'académie", q: "Combien de formats de leçon propose l'académie echecs.com ?", opts: ["2", "3", "4"], s: "Réponds en commentaire : A, B ou C ?", pose: "hourra" },
  // Quiz tirés des séries, de la revue et de l'espace de parties
  { id: "56-quiz-philidor", tpl: "quiz", theme: "craie", k: "Quiz · La revue n°778", q: "Le n°778 consacre un dossier de 33 pages à un grand nom français des échecs. Lequel ?", opts: ["Alexandre Alekhine", "François-André Philidor", "José Raúl Capablanca"], s: "Réponds en commentaire : A, B ou C ?", pose: "lecture" },
  { id: "57-quiz-citation", tpl: "quiz", theme: "nuit", k: "Quiz · Culture échecs", q: "« Les pions sont l'âme des échecs. » Qui l'a dit ?", opts: ["Garry Kasparov", "Magnus Carlsen", "François-André Philidor"], s: "Réponds en commentaire : A, B ou C ?", pose: "reflexion" },
  { id: "58-quiz-fourchette", tpl: "quiz", theme: "rose", k: "Quiz · Calcul Gagnant", q: "Une pièce attaque deux pièces adverses en même temps. C'est…", opts: ["une fourchette", "un coup intermédiaire", "une élimination du défenseur"], s: "Réponds en commentaire : A, B ou C ?", pose: "idee" },
  { id: "59-quiz-coup-intermediaire", tpl: "quiz", theme: "ciel", k: "Quiz · Calcul Gagnant", q: "Au lieu de reprendre tout de suite, on joue d'abord un coup plus fort. C'est…", opts: ["un roque", "une promotion", "un coup intermédiaire"], s: "Réponds en commentaire : A, B ou C ?", pose: "menton" },
  { id: "60-quiz-finales-778", tpl: "quiz", theme: "soleil", k: "Quiz · La revue n°778", q: "Dans le n°778, qui vous réconcilie avec les finales ?", opts: ["Vincent Moret", "Paul Velten", "Étienne Bacrot"], s: "Réponds en commentaire : A, B ou C ?", pose: "lecture" },
  { id: "61-quiz-repertoires", tpl: "quiz", theme: "menthe", k: "Quiz · Tes parties", q: "Dans ton espace de parties, où ranger les ouvertures que tu joues ?", opts: ["Dans Bases", "Dans Répertoires", "Dans Favoris"], s: "Réponds en commentaire : A, B ou C ?", pose: "cherche" },
  { id: "62-quiz-tata-steel", tpl: "quiz", theme: "ciel", k: "Quiz · Vidéos", q: "Dans quel pays se joue le tournoi Tata Steel Chess ?", opts: ["Aux Pays-Bas", "En Inde", "En Norvège"], s: "Réponds en commentaire : A, B ou C ?", pose: "regarde" },
  { id: "63-quiz-candidats", tpl: "quiz", theme: "nuit", k: "Quiz · Le Récap'", q: "Que désigne le Tournoi des candidats ?", opts: ["le champion d'Europe", "le meilleur jeune joueur", "le challenger du champion du monde"], s: "Réponds en commentaire : A, B ou C ?", pose: "menton" },
  { id: "64-quiz-karpov", tpl: "quiz", theme: "rose", k: "Quiz · Culture échecs", q: "Qui succède à Bobby Fischer comme champion du monde en 1975 ?", opts: ["Garry Kasparov", "Anatoli Karpov", "Boris Spassky"], s: "Réponds en commentaire : A, B ou C ?", pose: "prof" },

  // ---- Identité de profil (formats propres)
  { id: "id-avatar-nuit", tpl: "id-avatar", theme: "nuit", only: [["avatar-1080x1080", 1080, 1080, "Photo de profil (tous réseaux)"]] },
  { id: "id-avatar-soleil", tpl: "id-avatar", theme: "soleil", only: [["avatar-1080x1080", 1080, 1080, "Photo de profil (tous réseaux)"]] },
  { id: "id-banniere", tpl: "id-ban", theme: "nuit", pose: "prof", only: [
    ["x-1500x500", 1500, 500, "Bannière X", { sw: 1500, sh: 380, left: 260 }],
    ["linkedin-1584x396", 1584, 396, "Bannière LinkedIn (page)", { sw: 1584, sh: 300, left: 300 }],
    ["facebook-1640x624", 1640, 624, "Couverture Facebook", { sw: 1300, sh: 420 }],
    ["youtube-2560x1440", 2560, 1440, "Bannière YouTube (zone sûre 1546×423)", { sw: 1546, sh: 423 }],
  ] },
  { id: "id-banniere-soleil", tpl: "id-ban", theme: "soleil", pose: "hourra", only: [
    ["x-1500x500", 1500, 500, "Bannière X", { sw: 1500, sh: 380, left: 260 }],
    ["linkedin-1584x396", 1584, 396, "Bannière LinkedIn (page)", { sw: 1584, sh: 300, left: 300 }],
    ["facebook-1640x624", 1640, 624, "Couverture Facebook", { sw: 1300, sh: 420 }],
    ["youtube-2560x1440", 2560, 1440, "Bannière YouTube (zone sûre 1546×423)", { sw: 1546, sh: 423 }],
  ] },
  ...Object.entries({ lecons: "Leçons", videos: "Vidéos", masterclasses: "Masterclasses", exercices: "Exercices", tournois: "Tournois", forum: "Forum", revue: "Revue", parties: "Parties" })
    .map(([k, label]) => ({ id: "id-a-la-une-" + k, tpl: "id-hl", theme: "nuit", label, svg: ICON[k].replace(/currentColor/g, "#111"), only: [["story-a-la-une-1080x1920", 1080, 1920, "Couverture de story à la une Instagram"]] })),
];
