// Carrousels pédagogiques (Instagram et LinkedIn, 1080×1350) tirés des leçons de l'Académie.
// Une diapositive = un visuel « slide » ; toutes les diapositives d'un carrousel vont dans le même dossier (dir).
(() => {
  const S = (o => { const r = {}; for (const [k, v] of Object.entries(o)) for (const sq of v.split(" ")) r[sq] = k; return r; });
  const SQ = (cols, rows) => cols.split("").flatMap(c => rows.split("").map(r => c + r));

  // 1. Le mat du couloir
  const COULOIR = S({ wK: "g1", wR: "d1", wP: "f2 g2 h2", bK: "g8", bP: "f7 g7 h7 a7", bQ: "b2" });
  const COULOIR_MAT = S({ wK: "g1", wR: "d8", wP: "f2 g2 h2", bK: "g8", bP: "f7 g7 h7 a7", bQ: "b2" });
  const COULOIR_LUFT = S({ wK: "g1", wR: "d1", wP: "f2 g2 h2", bK: "g8", bP: "f7 g7 h6 a7", bQ: "b2" });
  const COULOIR_EXO = S({ wK: "g1", wR: "a1", wP: "f2 g2 h2", bK: "h8", bP: "g7 h7 b6" });
  // 2. La règle du carré
  const CARRE = S({ wK: "h1", wP: "b5", bK: "g5" });
  const CARRE_OK = S({ wK: "h1", wP: "b5", bK: "f6" });
  // 3. Le Fegatello
  const FEG1 = S({ wK: "e1", wQ: "d1", wR: "a1 h1", wB: "c1 c4", wN: "b1 f3", wP: "a2 b2 c2 d2 e4 f2 g2 h2",
    bK: "e8", bQ: "d8", bR: "a8 h8", bB: "c8 f8", bN: "c6 f6", bP: "a7 b7 c7 d7 e5 f7 g7 h7" });
  const FEG2 = S({ wK: "e1", wQ: "d1", wR: "a1 h1", wB: "c1 c4", wN: "b1 g5", wP: "a2 b2 c2 d2 f2 g2 h2",
    bK: "e8", bQ: "d8", bR: "a8 h8", bB: "c8 f8", bN: "c6 d5", bP: "a7 b7 c7 e5 f7 g7 h7" });
  const FEG3 = S({ wK: "e1", wQ: "d1", wR: "a1 h1", wB: "c1 c4", wN: "b1 f7", wP: "a2 b2 c2 d2 f2 g2 h2",
    bK: "e8", bQ: "d8", bR: "a8 h8", bB: "c8 f8", bN: "c6 d5", bP: "a7 b7 c7 e5 g7 h7" });
  const FEG4 = S({ wK: "e1", wQ: "f3", wR: "a1 h1", wB: "c1 c4", wN: "c3", wP: "a2 b2 c2 d2 f2 g2 h2",
    bK: "e6", bQ: "d8", bR: "a8 h8", bB: "c8 f8", bN: "c6 d5", bP: "a7 b7 c7 e5 g7 h7" });

  const C = [
    { dir: "carrousel-1-mat-du-couloir", theme: "rose", k: "Carrousel · Tactique", slides: [
      { t: "Le mat", e: "du couloir.", s: "L'erreur qui coûte la partie, même aux bons joueurs. En 6 diapositives.", pos: COULOIR, cover: true },
      { t: "Le décor", s: "Le Roi a roqué derrière trois pions intacts. Ils le protègent… mais l'enferment : aucune case de fuite.", pos: COULOIR, hl: ["f7", "g7", "h7"] },
      { t: "Le coup", s: "1.Td8# : la Tour arrive sur la dernière rangée. Le Roi est prisonnier de ses propres pions. Mat.", pos: COULOIR_MAT, arrow: ["d1", "d8"] },
      { t: "Comment l'éviter", s: "Ouvre une « fenêtre » : un coup de pion (h6 ou g6) donne une case de fuite au Roi. Ici, sur 1.Td8+, il file en h7.", pos: COULOIR_LUFT, hl: ["h7"] },
      { t: "À toi de jouer", s: "Les Blancs jouent et font mat en 1. Réponds en commentaire !", pos: COULOIR_EXO },
      { t: "1.Ta8# !", s: "Même idée : la Tour prend la dernière rangée, les pions g7 et h7 bouchent la sortie. Le mat du couloir revient dans des dizaines d'exercices de l'Académie.", pos: S({ wK: "g1", wR: "a8", wP: "f2 g2 h2", bK: "h8", bP: "g7 h7 b6" }), arrow: ["a1", "a8"] },
      { cta: true, t: "+2 000 exercices", e: "à ton niveau.", s: "Le mat du couloir, la fourchette, le clouage… Entraîne-toi chaque jour dans l'Académie echecs.com." },
    ] },
    { dir: "carrousel-2-regle-du-carre", theme: "ciel", k: "Carrousel · Finales", slides: [
      { t: "La règle", e: "du carré.", s: "Ton Roi rattrape-t-il ce pion ? La réponse en 2 secondes, sans calculer.", pos: CARRE, cover: true },
      { t: "Le problème", s: "Un pion passé file vers la promotion. Compter les coups un par un, c'est long… et on se trompe vite.", pos: CARRE },
      { t: "Trace le carré", s: "Du pion jusqu'à sa case de promotion : c'est le côté du carré. Ici, de b5 à b8, puis jusqu'à la colonne e.", pos: CARRE, hl: SQ("bcde", "5678") },
      { t: "La règle", s: "Si le Roi entre dans le carré (avec le trait), il rattrape le pion. Sinon, le pion passe. Ici, le Roi g5 n'y entre pas : le pion fait Dame.", pos: CARRE, hl: SQ("bcde", "5678") },
      { t: "Un pas de plus", s: "Roi en f6, trait aux Noirs : Re6 entre dans le carré. Le Roi rattrape le pion à temps.", pos: CARRE_OK, hl: SQ("bcde", "5678"), arrow: ["f6", "e6"] },
      { t: "Deux pièges", s: "• Un pion sur sa case de départ avance de deux cases : trace le carré depuis la 3e rangée.<br>• Si une pièce bloque la route du Roi, ou si le Roi adverse soutient le pion, la règle ne suffit plus : calcule." },
      { cta: true, t: "+200 leçons", e: "interactives.", s: "La règle du carré, l'opposition, la triangulation… Toutes les finales qui comptent, dans l'Académie echecs.com." },
    ] },
    { dir: "carrousel-3-fegatello", theme: "menthe", k: "Carrousel · Ouvertures", slides: [
      { t: "Le <i class=\"ei\">Fegatello.</i>", s: "Le sacrifice d'ouverture le plus célèbre. « Petit foie » en italien… et un Roi noir en danger.", pos: FEG3, cover: true, hl: ["f7"] },
      { t: "Le départ", s: "1.e4 e5 2.Cf3 Cc6 3.Fc4 Cf6 : la défense des deux Cavaliers. Le Fou c4 vise déjà f7.", pos: FEG1, hl: ["c4", "f7"] },
      { t: "L'erreur noire", s: "4.Cg5 d5 5.exd5 Cxd5 ? Les Noirs reprennent avec le Cavalier… et tout bascule.", pos: FEG2, hl: ["d5"] },
      { t: "Le sacrifice", s: "6.Cxf7 ! Le Cavalier se sacrifie pour arracher le Roi noir à son abri. Après 6...Rxf7 7.Df3+ Re6 8.Cc3, toutes les pièces blanches arrivent.", pos: FEG4, hl: ["e6"] },
      { t: "Avec les Noirs ?", s: "Prends : 6...Rxf7. Ton Roi va souffrir, mais tu as une pièce de plus. Mieux encore : évite le piège avec 5...Ca5, la ligne principale.", pos: FEG3, arrow: ["e8", "f7"] },
      { t: "À retenir", s: "• f7 n'est défendu que par le Roi : c'est la cible n° 1 en début de partie.<br>• Avant de reprendre au centre, regarde ce que vise l'adversaire." },
      { cta: true, t: "Les pièges", e: "d'ouverture.", s: "Le Fegatello, le gambit Roi, la Scandinave… Apprends-les dans les leçons Objectif 1400 et 1600 de l'Académie echecs.com." },
    ] },
  ];
  for (const c of C) c.slides.forEach((sl, i) => window.VISUELS.push({
    ...sl, id: `${c.dir}-${i + 1}`, dir: c.dir, tpl: "slide", theme: c.theme, k: c.k, n: i + 1, total: c.slides.length,
    only: [["portrait-1080x1350", 1080, 1350, "Diapositive de carrousel Instagram, LinkedIn, Facebook"]],
  }));
})();
