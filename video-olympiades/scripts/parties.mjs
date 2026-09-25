// Lit les PGN de data/ et écrit src/parties.js : pour chaque partie, ses
// métadonnées et la liste des demi-coups déjà résolus (case de départ, case
// d'arrivée, prise, roque, promotion) avec la position avant chacun.
// L'animation de l'échiquier n'a ainsi aucune règle du jeu à connaître.
import { Chess } from 'chess.js';
import fs from 'fs';
import path from 'path';

const here = path.dirname(new URL(import.meta.url).pathname);
const root = path.join(here, '..');

// clé → nom de famille du joueur qui sert de repère dans le PGN
const CLES = {
  mvl: ['france-chine-r9.pgn', 'Vachier-Lagrave'],
  lagarde: ['france-chine-r9.pgn', 'Lagarde'],
  maurizzi: ['france-chine-r9.pgn', 'Maurizzi'],
  moussard: ['france-chine-r9.pgn', 'Moussard'],
  gukesh: ['gukesh-r9.pgn', 'Gukesh'],
  ddc: ['france-serbie-r9.pgn', 'Daulyte-Cornette'],
};

const cache = {};
function parties(fichier) {
  if (!cache[fichier]) {
    const pgn = fs.readFileSync(path.join(root, 'data', fichier), 'utf8');
    cache[fichier] = pgn.split(/\n\n(?=\[Event)/).map(g => g.trim()).filter(Boolean);
  }
  return cache[fichier];
}

const tag = (g, k) => (g.match(new RegExp(`\\[${k} "([^"]*)"\\]`)) || [, ''])[1];
const nom = n => n.split(',')[0].trim(); // « Vachier-Lagrave, Maxime » → « Vachier-Lagrave »

const sortie = {};
for (const [cle, [fichier, joueur]] of Object.entries(CLES)) {
  const brut = parties(fichier).find(g => (tag(g, 'White') + tag(g, 'Black')).includes(joueur));
  if (!brut) throw new Error(`partie introuvable pour ${cle} (${joueur}) dans ${fichier}`);
  const chess = new Chess();
  // Les PGN de diffusion portent des commentaires de pendule ({[%clk …]}) et des
  // annotations que l'analyseur refuse : on ne garde que les coups.
  chess.loadPgn(brut.replace(/\{[^}]*\}/g, '').replace(/\$\d+/g, ''));
  sortie[cle] = {
    white: nom(tag(brut, 'White')), black: nom(tag(brut, 'Black')),
    whiteTeam: tag(brut, 'WhiteTeam'), blackTeam: tag(brut, 'BlackTeam'),
    whiteElo: tag(brut, 'WhiteElo'), blackElo: tag(brut, 'BlackElo'),
    result: tag(brut, 'Result'), eco: tag(brut, 'ECO'), opening: tag(brut, 'Opening'),
    moves: chess.history({ verbose: true }).map(m => ({
      san: m.san, from: m.from, to: m.to,
      piece: m.color + m.piece.toUpperCase(),
      color: m.color, flags: m.flags,
      captured: m.captured ? (m.color === 'w' ? 'b' : 'w') + m.captured.toUpperCase() : null,
      promotion: m.promotion ? m.color + m.promotion.toUpperCase() : null,
      before: m.before,
    })),
  };
}

fs.writeFileSync(path.join(root, 'src/parties.js'),
  '// Généré par scripts/parties.mjs — ne pas modifier à la main.\nwindow.PARTIES = '
  + JSON.stringify(sortie) + ';\n');

for (const [cle, g] of Object.entries(sortie)) {
  const n = Math.ceil(g.moves.length / 2);
  console.log(`${cle.padEnd(9)} ${g.white} (${g.whiteElo}) – ${g.black} (${g.blackElo})  ${g.result}  ${n} coups  ${g.eco}`);
}
