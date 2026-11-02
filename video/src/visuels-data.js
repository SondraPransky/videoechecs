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
  { id: "10-tournois", tpl: "accroche", theme: "soleil", k: "Tournois en ligne", t: "Mesure-toi", e: "aux autres joueurs.", s: "Cadence 10' + 5\", tous niveaux.", shot: "tournois", pose: "victoire-tournoi" },

  // ---- Chiffres clés
  { id: "11-chiffre-200-lecons", tpl: "chiffre", theme: "soleil", k: "Leçons interactives", n: "+200", t: "leçons", e: "pour progresser.", pose: "idee" },
  { id: "12-chiffre-2000-exercices", tpl: "chiffre", theme: "nuit", k: "Entraînement", n: "+2<b>&#8239;</b>000", t: "exercices", e: "et quiz.", pose: "bonne-reponse" },
  { id: "13-chiffre-4-formats", tpl: "chiffre", theme: "menthe", k: "Apprends comme tu veux", n: "4", t: "formats", e: "de leçon.", s: "Vidéo, cours écrit, exercice, quiz.", pose: "lecture" },

  // ---- Engagement : problème, solution, quiz
  { id: "14-probleme-mat-en-1", tpl: "puzzle", theme: "nuit", k: "Le problème du jour", t: "Mat en 1.", e: "À toi de jouer !", s: "Les Blancs jouent. Ta réponse en commentaire.", pos: MAT1, pose: "reflexion" },
  { id: "15-solution-mat-en-1", tpl: "puzzle", theme: "menthe", k: "La solution", t: "Td8#", e: "le mat du couloir.", s: "Le roi noir est enfermé par ses propres pions.", pos: MAT1_OK, hl: ["d1", "d8"], arrow: ["d1", "d8"], pose: "bonne-reponse" },
  { id: "16-quiz-carlsbad", tpl: "quiz", theme: "craie", k: "Quiz · Objectif 1600", q: "Structure Carlsbad : quel est le plan typique des Blancs ?", opts: ["L'attaque de minorité", "Échanger toutes les pièces", "Pousser h4-h5 au plus vite"], s: "Réponds en commentaire : A, B ou C ?", pose: "idee" },

  // ---- Portraits des coachs
  { id: "17-coach-sylvain-ravot", tpl: "coach", theme: "rose", k: "Nos coachs", t: "Sylvain Ravot", e: "Maître FIDE.", s: "Calcul, tactique et masterclasses en direct.", photo: "auth-ravot", titre: "MF" },
  { id: "18-coach-marc-quenehen", tpl: "coach", theme: "menthe", k: "Nos coachs", t: "Marc Quenehen", e: "la Minute Finale.", s: "Les finales expliquées simplement.", photo: "auth-quenehen" },
  { id: "19-coach-fabien-libiszewski", tpl: "coach", theme: "ciel", k: "Nos coachs", t: "Fabien Libiszewski", e: "Grand Maître.", s: "En masterclass sur echecs.com.", photo: "auth-libiszewski", titre: "GMI" },
  { id: "20-coach-gata-kamsky", tpl: "coach", theme: "soleil", k: "Nos coachs", t: "Gata Kamsky", e: "Grand Maître.", s: "En masterclass sur echecs.com.", photo: "auth-kamsky", titre: "GMI" },

  // ---- Humeurs de la mascotte
  { id: "21-humeur-serie", tpl: "mascotte", theme: "nuit", k: "Ta série", t: "7 jours de suite.", e: "Ne lâche rien !", pose: "serie-de-jours" },
  { id: "22-humeur-lecon-terminee", tpl: "mascotte", theme: "soleil", k: "Bravo", t: "Leçon terminée.", e: "Au tour de la suivante !", pose: "lecon-terminee" },
  { id: "23-humeur-rate", tpl: "mascotte", theme: "ciel", k: "Pas grave", t: "Raté ?", e: "C'est comme ça qu'on apprend.", pose: "mauvaise-reponse" },
  { id: "24-humeur-dodo", tpl: "mascotte", theme: "nuit", k: "Ce soir", t: "Une partie avant de dormir ?", e: "Juste une.", pose: "dodo", white: true },
  { id: "25-humeur-victoire", tpl: "mascotte", theme: "rose", k: "Tournoi du week-end", t: "Premier du tournoi !", e: "Et toi, quand ?", pose: "victoire-tournoi" },
  { id: "26-humeur-idee", tpl: "mascotte", theme: "craie", k: "Astuce du jour", t: "Sors tes pièces", e: "avant ta dame.", pose: "idee" },

  // ---- Annonces
  { id: "27-revue-numero-779", tpl: "revue", theme: "nuit", k: "Nouveau numéro", t: "Le n°779", e: "est sorti !", s: "Milliet & Bacrot : 16 titres pour 2 légendes.", },
  { id: "28-tournois-chaque-semaine", tpl: "event", theme: "ciel", k: "Tournois en ligne", t: "Chaque semaine,", e: "un tournoi.", facts: ["Cadence 10' + 5\"", "Ouvert à tous les niveaux", "Classement en direct"], pose: "victoire-tournoi", white: true },

  // ---- Identité de profil (formats propres)
  { id: "id-avatar-nuit", tpl: "id-avatar", theme: "nuit", only: [["avatar-1080x1080", 1080, 1080, "Photo de profil (tous réseaux)"]] },
  { id: "id-avatar-soleil", tpl: "id-avatar", theme: "soleil", only: [["avatar-1080x1080", 1080, 1080, "Photo de profil (tous réseaux)"]] },
  { id: "id-banniere", tpl: "id-ban", theme: "nuit", pose: "lecon-terminee", only: [
    ["x-1500x500", 1500, 500, "Bannière X", { sw: 1500, sh: 380, left: 260 }],
    ["linkedin-1584x396", 1584, 396, "Bannière LinkedIn (page)", { sw: 1584, sh: 300, left: 300 }],
    ["facebook-1640x624", 1640, 624, "Couverture Facebook", { sw: 1300, sh: 420 }],
    ["youtube-2560x1440", 2560, 1440, "Bannière YouTube (zone sûre 1546×423)", { sw: 1546, sh: 423 }],
  ] },
  { id: "id-banniere-soleil", tpl: "id-ban", theme: "soleil", pose: "serie-reussie", only: [
    ["x-1500x500", 1500, 500, "Bannière X", { sw: 1500, sh: 380, left: 260 }],
    ["linkedin-1584x396", 1584, 396, "Bannière LinkedIn (page)", { sw: 1584, sh: 300, left: 300 }],
    ["facebook-1640x624", 1640, 624, "Couverture Facebook", { sw: 1300, sh: 420 }],
    ["youtube-2560x1440", 2560, 1440, "Bannière YouTube (zone sûre 1546×423)", { sw: 1546, sh: 423 }],
  ] },
  ...Object.entries({ lecons: "Leçons", videos: "Vidéos", masterclasses: "Masterclasses", exercices: "Exercices", tournois: "Tournois", forum: "Forum", revue: "Revue", parties: "Parties" })
    .map(([k, label]) => ({ id: "id-a-la-une-" + k, tpl: "id-hl", theme: "nuit", label, svg: ICON[k].replace(/currentColor/g, "#111"), only: [["story-a-la-une-1080x1920", 1080, 1920, "Couverture de story à la une Instagram"]] })),
];
