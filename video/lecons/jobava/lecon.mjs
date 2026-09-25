// Leçon « Une petite idée contre le Jobava » — d'après le PGN commenté de Romuald De Labaca (12/11/2024).
//
// Chaque entrée est un passage : une réplique de la voix off (say) et ce qui se passe sur l'échiquier.
//   say     texte lu. « ^ » place le coup suivant de play à cet endroit de la phrase,
//           « # » fait apparaître flèches et cases à cet endroit (sinon après le dernier coup).
//   play    coups en notation anglaise (SAN), annotations !? ?! ! ? acceptées.
//   from    repart d'une position mémorisée (mark) ; « start » = position initiale.
//   mark    mémorise la position atteinte à la fin du passage.
//   arrows  flèches façon ChessBase : G/R/Y/B + départ + arrivée (ex. « Gc3b5 »).
//   sq      cases colorées : G/R/Y/B + case (ex. « Rc7 »).
//   key     idée clé affichée dans le panneau.       ev   évaluation (=+, ∞…).
//   ch      chapitre (reste affiché).                line  « Partie principale » ou nom de la variante.
//   quiz    question « À toi de jouer » : compte à rebours de pause secondes après la voix.
//   card    carte plein écran { k, t, s, pose, bullets }.
//   fast    secondes par coup pour dérouler une partie en accéléré.   game  bandeau de partie de référence.

export const meta = {
  title: 'Une petite idée contre le Jobava',
  kicker: 'Leçon d\'ouverture · Objectif 1600-1800',
  author: 'D\'après l\'analyse de Romuald De Labaca',
  orientation: 'black',   // leçon pour les Noirs : échiquier vu de leur côté
};

const MAIN = 'Partie principale';

export const beats = [
  { card: { k: 'Leçon d\'ouverture · Objectif 1600-1800', t: 'Une petite idée contre le Jobava', s: '1.d4 d5 2.Cc3 Cf6 3.Ff4', pose: 'idee' },
    say: 'Salut à toi ! Aujourd\'hui, on s\'attaque à une ouverture devenue incontournable : le système Jobava. Des joueurs de club jusqu\'à l\'élite mondiale, tout le monde s\'y met. Alors pour ne pas la subir, je vais te montrer une petite idée avec les Noirs : simple à retenir, logique, et qui pose de vrais problèmes aux Blancs.' },

  // ── Chapitre 1 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 1', t: 'Le système Jobava', pose: 'regarde' } },
  { ch: 'Le système Jobava', line: MAIN, from: 'start', play: 'd4 d5', mark: 'd5',
    say: 'Les Blancs ouvrent par ^d4, et on répond du tac au tac : ^d5.' },
  { play: 'Nc3', arrows: 'Yc2c4',
    say: 'Premier signal : Cavalier c3 ! Un coup peu courant dans les ouvertures du pion Dame, puisqu\'il bloque le pion c.' },
  { play: 'Nf6', mark: 'Nf6',
    say: 'On développe : Cavalier f6.' },
  { from: 'start', play: 'd4 Nf6 Nc3 d5', line: 'Transposition',
    say: 'Petite parenthèse : si tu préfères répondre à ^d4 par ^Cavalier f6, après ^Cavalier c3 et ^d5, on retombe exactement sur la même position. Ça transpose !' },
  { from: 'Nf6', line: MAIN, play: 'Bf4', sq: 'Rc7', arrows: 'Gc3b5 Gb5c7 Gf4c7', key: 'Le Fou vise c7, le Cavalier menace de bondir en b5.',
    say: 'Et voici le Jobava : Fou f4 ! Le Fou prend position sur cette belle diagonale, et il justifie le placement du Cavalier en c3. Regarde bien la case c7 : # le Fou la vise déjà, et le Cavalier peut sauter en b5 pour l\'attaquer une deuxième fois. Cavalier b5, c\'est une menace à prendre au sérieux dès maintenant !', mark: 'Bf4' },
  { quiz: 'Quel petit coup de pion règle le problème de Cb5 ?', pause: 5,
    say: 'Les Noirs ont plusieurs systèmes possibles. Moi, je te propose d\'aller vers quelque chose de simple. À toi de jouer : quel petit coup de pion règle définitivement la question du Cavalier b5 ?' },
  { play: 'a6!?', sq: 'Rb5', arrows: 'Ga6b5 Gb7b5', key: 'a6 : contrôle b5 et prépare la poussée ...b5.',
    say: 'Pion a6 ! D\'abord, # il contrôle la case b5 : fini le Cavalier en b5. Ensuite, il garde en réserve la poussée b5, pour gagner de l\'espace à l\'aile Dame plus tard. Deux idées pour le prix d\'un seul coup de pion.' },
  { play: 'e3', arrows: 'Gf1d3', mark: 'e3',
    say: 'Les Blancs jouent le coup normal : e3. Il ouvre la diagonale du Fou f1, qui va naturellement venir se placer en d3.' },

  // ── Chapitre 2 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 2', t: 'Le coup d\'attente ...h6 !?', pose: 'reflexion' } },
  { ch: 'Le coup d\'attente', play: 'h6!?', mark: 'h6', key: 'Coup d\'attente : on laisse les Blancs se dévoiler.', sq: 'Yg5',
    say: 'Et là, surprise : h6 ! Un petit coup d\'attente, utile et malin. Au passage, # il retire la case g5 aux pièces blanches. Mais surtout, il laisse les Blancs choisir leur développement en premier… pour qu\'on puisse s\'adapter ensuite.' },
  { from: 'e3', line: 'Variante : 4...e6', play: 'e6', arrows: 'Gf8e7 Ge8g8 Gc7c5',
    say: 'Mais pourquoi ne pas jouer e6 tout de suite ? C\'est d\'ailleurs le coup quasi exclusivement joué ici. Il est naturel : il libère le Fou f8, prépare le roque, et soutient l\'attaque du centre par c5. C\'est un système parfaitement viable… à condition de bien connaître la théorie. Car il existe un coup dangereux.' },
  { play: 'g4!', arrows: 'Gg4g5 Gd1g4', sq: 'Rf6', key: 'g4 ! : l\'attaque éclair, pion protégé par la Dame d1.',
    say: 'g4 ! Joué dans plusieurs parties de haut niveau. Le pion menace de monter en g5 pour chasser le Cavalier f6, et # il est protégé par la Dame d1 : impossible de le prendre. La position devient très tranchante, et avec les Noirs, il faut beaucoup de connaissances pour s\'en sortir. C\'est exactement ce qu\'on veut éviter !' },
  { from: 'h6', line: MAIN, key: 'Après ...h6, on réagit selon le coup blanc.',
    say: 'Revenons donc à h6. Maintenant, c\'est aux Blancs de se décider, et selon leur choix, on va réagir différemment. Trois coups principaux : Fou d3, h4, et Cavalier f3. On commence par le Fou.' },

  // ── Chapitre 3 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 3', t: 'Si 5.Fd3 : frappe au centre !', pose: 'regarde' } },
  { ch: 'Si 5.Fd3', line: 'Variante : 5.Fd3', from: 'h6', play: 'Bd3', mark: 'Bd3', arrows: 'Gd1g4',
    sq: 'Yg4', say: 'Fou d3 : c\'est la case naturelle du Fou. Et surtout, # la Dame d1 surveille toujours g4 : les Blancs gardent la possibilité de pousser g4 si on joue e6.' },
  { play: 'e6?! g4!', say: 'Donc ici, on évite ^e6 : les Blancs pousseraient aussitôt ^g4, et on retomberait dans ce type de position tranchante qu\'on voulait justement éviter.' },
  { from: 'Bd3', quiz: 'Si ce n\'est pas ...e6, quel coup pour les Noirs ?', pause: 5,
    say: 'À toi de jouer ! Si ce n\'est pas e6, quel est le bon coup pour les Noirs ? Un indice : pense au centre.' },
  { play: 'c5!', arrows: 'Rc5d4', mark: 'c5', key: '...c5 ! : l\'attaque naturelle du centre, sans enfermer le Fou c8.',
    say: 'c5 ! L\'attaque naturelle du centre. On frappe le pion d4 sans perdre de temps, et sans enfermer notre Fou c8, qui pourra encore sortir.' },
  { line: 'Variante : 6.Cf3', play: 'Nf3 c4!', arrows: 'Rc4d3', key: '...c4 ! gagne un temps sur le Fou d3.',
    say: 'Si les Blancs soutiennent le centre avec ^Cavalier f3, on pousse ^c4 ! # Le pion attaque le Fou d3, et on gagne un temps.' },
  { play: 'Be2 Bf5', ev: '=+', arrows: 'Ge7e6 Gf8d6 Ge8g8 Gb7b5', key: 'Le Fou c8 est sorti avant ...e6 : les Noirs sont confortables.',
    say: 'Le Fou recule en ^e2, et on sort notre Fou en ^f5. Regarde : on n\'a même pas joué e6, et notre Fou de cases blanches est déjà dehors ! # Ensuite, e6, Fou d6, le roque, et pourquoi pas b5. Les Noirs sont plus confortables.' },
  { from: 'c5', line: 'Variante : 5.Fd3', play: 'dxc5', mark: 'dxc5',
    say: 'Le plus souvent, les Blancs prennent : d prend c5. C\'est la réaction standard.' },
  { play: 'Nc6', mark: 'Nc6', arrows: 'Re5f4 Ge7e5 Gf8c5', key: 'On ignore c5 : ...e5 puis ...Fxc5 arrivent.',
    say: 'Et là, on ne se précipite pas pour reprendre ce pion. Cavalier c6 ! On développe, et # on menace e5, qui attaquera le Fou f4. Ensuite, le Fou f8 reprendra tranquillement en c5. Le pion ne va pas s\'envoler.' },
  { line: 'Variante : 7.Ca4', play: 'Na4', sq: 'Yc5 Yb6', arrows: 'Ga4c5 Ga4b6',
    say: 'Les Blancs peuvent essayer de garder le pion avec Cavalier a4. C\'est un coup fréquent quand les Noirs ont joué a6 : # le Cavalier défend c5, et il vise la case b6, affaiblie. Mais ici, c\'est inefficace.' },
  { play: 'e5', mark: 'Na4e5', arrows: 'Re5f4',
    say: 'Car e5 ! Le Fou f4 est attaqué.' },
  { play: 'Nb6 exf4 Nxa8 fxe3', sq: 'Ra8',
    say: 'Si les Blancs foncent avec ^Cavalier b6, on prend le Fou : ^e prend f4. ^Le Cavalier dévore la Tour a8… mais on continue avec ^f prend e3 ! Et le Cavalier a8, lui, est coincé dans le coin.' },
  { play: 'Qe2 Bxc5 fxe3 Bd7', ev: '−+', sq: 'Ra8',
    say: 'Par exemple : ^Dame e2, ^Fou prend c5, ^f prend e3, et ^Fou d7. Le Cavalier a8 ne ressortira pas vivant, et les Noirs auront deux pièces pour la Tour.' },
  { from: 'Na4e5', play: 'Bg3 Nd7', ev: '=+', arrows: 'Gd7b6 Gd7c5', sq: 'Yc5', key: '...Cd7 bouche le trou en b6 et vise c5.',
    say: 'Le plus raisonnable pour les Blancs, c\'est ^Fou g3. On répond ^Cavalier d7 : # on colmate le trou en b6, et on va se venger sur le pion c5. Les Noirs sont mieux.' },
  { from: 'Nc6', line: 'Variante : 5.Fd3', play: 'Nf3 Bg4', mark: 'Bg4', arrows: 'Ge7e5 Gf8c5', key: '...Fg4 puis ...e5 : jeu agréable et simple.',
    say: 'Revenons au coup naturel : ^Cavalier f3. Et là, ^Fou g4 ! # On menace toujours e5, puis de récupérer le pion c5, avec un jeu agréable et une position simple à jouer.' },
  { play: 'O-O e5 Bg3', quiz: 'Les Noirs ont un coup très fort. Cherche la fourchette !', pause: 6,
    say: 'Si les Blancs ^roquent, on joue ^e5, et le Fou recule en ^g3. Et maintenant, à toi : les Noirs ont un coup très fort. Cherche la fourchette !' },
  { play: 'e4!', arrows: 'Re4d3 Re4f3 Gg4f3', ev: '−+', key: 'Fourchette de pion ! Le Cavalier f3 est en plus cloué.',
    say: 'e4 ! Une fourchette de pion : # le Fou d3 et le Cavalier f3 sont attaqués en même temps. Et en plus, le Cavalier f3 est cloué par notre Fou g4. Les Blancs vont perdre une pièce.' },
  { from: 'Bg4', line: 'Variante : 8.h3', play: 'h3 Bxf3 Qxf3 e5 Bg3 e4!', arrows: 'Re4d3 Re4f3', ev: '−+',
    say: 'Même motif si les Blancs chassent le Fou avec ^h3 : on prend en ^f3, ^Dame prend f3, ^e5, ^Fou g3, et encore ^e4 ! # Cette fois, c\'est la Dame et le Fou qui sont fourchettés.' },
  { from: 'Bg4', line: 'Variante : 8.Fe2', play: 'Be2 Bxf3 Bxf3 e5 Bg3 e4 Be2 Bxc5', sq: 'Yd5', ev: '=+',
    say: 'Et après ^Fou e2 ? Même recette : on prend en ^f3, ^Fou prend f3, ^e5, ^Fou g3, puis ^e4 pour chasser le Fou, ^Fou e2, et on récupère le pion : ^Fou prend c5. Les Noirs sont très bien.' },

  // ── Chapitre 4 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 4', t: 'Si 5.h4 : l\'idée de Niemann', pose: 'lecture' } },
  { ch: 'Si 5.h4', line: 'Variante : 5.h4', from: 'h6', play: 'h4', arrows: 'Gh4h5',
    say: 'Autre option, défendue par le grand spécialiste du Jobava, Hans Niemann : h4. Les Blancs jouent un coup utile, et attendent eux aussi !' },
  { play: 'c5! dxc5 Nc6 Nf3 Bg4', arrows: 'Ge7e5 Gf8c5', key: 'Même principe : ...c5, ...Cc6, ...Fg4 et ...e5.',
    say: 'Et la recette ne change pas : ^c5, ^d prend c5, ^Cavalier c6 avec la menace e5, ^Cavalier f3, et ^Fou g4. Même principe !' },
  { play: 'Be2 Bxf3 Bxf3 e5', arrows: 'Re5f4',
    say: 'Après ^Fou e2, on prend le Cavalier : ^Fou prend f3, ^Fou prend f3, et on joue ^e5 pour s\'emparer du centre.' },
  { play: 'Bg3', sq: 'Rd5', arrows: 'Gc3d5 Gf3d5 Gd1d5',
    say: 'Fou g3. Mais attention : regarde le pion d5. # Le Cavalier c3, le Fou f3 et la Dame d1 le visent tous !' },
  { quiz: 'Comment se débarrasser de la pression sur d5 ?', pause: 5,
    say: 'À toi de jouer : comment les Noirs se débarrassent-ils de cette pression ?' },
  { play: 'e4! Be2 Bxc5', ev: '=+', mark: 'h4Bxc5', key: '...e4 ! chasse le Fou f3, puis ...Fxc5 : avantage noir.',
    say: '^e4 ! On chasse le Fou f3 et on coupe la pression sur d5. Le Fou recule en ^e2, et on récupère enfin le pion : ^Fou prend c5. Les Noirs ont un bon avantage, confirmé par les deux parties jouées au plus haut niveau dans cette position.' },
  { game: 'Niemann – Vidit · 2024 · 0-1', fast: 0.42, key: 'Partie de référence : ...d4, pièces actives, et l\'attaque noire l\'emporte.',
    play: 'Qd2 Qa5 O-O d4 exd4 Bxd4 Rad1 Rd8 Qf4 Bxc3 Rxd8+ Qxd8 bxc3 O-O Rb1 b5 Qe3 Qa5 Qc5 Qxa2 Re1 Nd8 Qb6 Ne6 Bf1 Re8 Be5 Ng4 Qc6 Rd8 Bg3 Qxc2 Rxe4 Rd1 Rxg4 Rxf1+ Kh2 Qd1 Qa8+ Nf8 Kh3 Rh1+ Bh2 Rxh2+ Kg3 Qd6+',
    say: 'Regarde la partie Niemann contre Vidit, en 2024. Les Noirs cassent le centre avec d4, activent toutes leurs pièces, gagnent le pion a2, puis le c2… et l\'attaque finit par tomber sur le Roi blanc. Victoire de Vidit ! Et dans Hou Yifan contre Koneru, la même année ? Encore une victoire noire.' },

  // ── Chapitre 5 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 5', t: 'La ligne principale : 5.Cf3', pose: 'regarde' } },
  { ch: 'La ligne principale 5.Cf3', line: MAIN, from: 'h6', play: 'Nf3', sq: 'Yg4',
    say: 'Passons au coup le plus naturel : Cavalier f3. Et là, l\'idée de h6 prend tout son sens !' },
  { quiz: 'Pourquoi ...e6 devient-il possible maintenant ?', pause: 4,
    say: 'Question : pourquoi peut-on maintenant jouer e6 sans craindre g4 ? Regarde bien la Dame d1.' },
  { play: 'e6', mark: 'e6', arrows: 'Rd1g4', sq: 'Gf3', key: 'Le Cf3 bouche la route de la Dame vers g4.',
    say: 'Réponse : # le Cavalier f3 bouche la route de la Dame vers g4. La poussée g4 ne tient plus debout, donc on joue e6 tranquillement, et on continue notre développement.' },
  { line: 'Variante : 6.g4?', play: 'g4? Nxg4', ev: '=+',
    say: 'Si les Blancs insistent quand même avec ^g4, on prend simplement : ^Cavalier prend g4. Un pion gratuit !' },
  { from: 'e6', line: MAIN, play: 'Bd3 c5', mark: 'c5main', arrows: 'Rc5d4',
    say: '^Fou d3, et on frappe le centre : ^c5. Position simple à jouer ! La position blanche est solide, mais on a du mal à imaginer que les Blancs puissent être très dangereux ici.' },
  { line: 'Variante : 7.O-O', play: 'O-O c4 Be2 b5', arrows: 'Gb8d7 Gf8e7 Gc8b7 Gb5b4',
    say: 'Si les Blancs ^roquent, on gagne un temps avec ^c4, le Fou recule en ^e2, et ^b5 ! # Les Noirs sont en avance à l\'aile Dame : Cavalier d7, Fou e7, Fou b7, le roque, puis l\'expansion avec b4.' },
  { from: 'c5main', line: MAIN, play: 'dxc5 Bxc5',
    say: 'Mais les Blancs prennent régulièrement : ^d prend c5, ^Fou prend c5. Notre Fou est actif, et on est prêts à roquer.' },
  { play: 'e4', arrows: 'Re4d5', key: 'e4 : structure de défense française, acceptable pour les Noirs.',
    say: 'e4 ! Les Blancs changent la structure centrale. C\'est une réaction typique qu\'il faut connaître avec les Noirs. La partie prend une tournure de défense française, tout à fait acceptable pour nous. Et si les Blancs roquent d\'abord avant de pousser e4, on revient au même.' },
  { play: 'Nc6 O-O O-O', mark: 'castle', key: 'Les Blancs doivent décider quoi faire au centre.',
    say: '^Cavalier c6, les deux camps ^roquent ^… et maintenant, les Blancs doivent décider ce qu\'ils vont faire au centre. Trois possibilités.' },

  // ── Chapitre 6 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 6', t: 'Trois plans pour les Blancs', pose: 'reflexion' } },
  { ch: 'Trois plans pour les Blancs', line: 'Plan 1 : 10.exd5', from: 'castle', play: 'exd5 Nxd5 Nxd5 exd5', sq: 'Rd5', ev: '∞',
    arrows: 'Gd8f6 Gc8g4 Ga8d8 Gf8e8', key: 'Pion isolé en d5, mais pièces noires très actives.',
    say: 'Premièrement : ^e prend d5. Ça soulage plutôt les Noirs. Après ^Cavalier prend d5, ^Cavalier prend d5, ^e prend d5, on hérite d\'un pion isolé… # mais regarde l\'activité ! La Dame va débouler en f6, où elle attaquera le Fou f4 et le pion b2. Le Fou c8 trouve une case naturelle en g4, et les Tours rejoignent vite le centre. L\'activité compense largement le pion isolé, qui prend même de l\'espace aux pièces blanches.' },
  { from: 'castle', line: 'Plan 2 : 10.Te1', play: 'Re1 b5', arrows: 'Gc8b7 Gd8b6 Gc5f2', sq: 'Rf2',
    say: 'Deuxièmement : ^Tour e1, pour garder la tension. On joue ^b5, et la position est facile à jouer : # Fou b7, sans doute Dame b6, avec une pression sur le pion f2.' },
  { from: 'castle', line: 'Plan 3 : 10.e5', play: 'e5', arrows: 'Rd3h7 Rf6d7',
    say: 'Troisièmement, le plus ambitieux : e5 ! Les Blancs ferment le centre, chassent le Cavalier f6, et # visent clairement notre Roi.' },
  { play: 'Nd7 Qd2', mark: 'Qd2', sq: 'Rh6', arrows: 'Gd2h6 Gf4h6', key: 'Dd2 : la Dame et le Fou visent h6. Sacrifice en vue !',
    say: '^Cavalier d7, et ^Dame d2. Officiellement, c\'est pour relier les Tours. Mais # regarde la case h6 : la Dame et le Fou la visent tous les deux. Un sacrifice se prépare !' },
  { line: 'Plan 3 : 11...b5?', play: 'b5? Bxh6 gxh6 Qxh6', arrows: 'Gf3g5 Gh6h7 Gd3h7', sq: 'Rh7', ev: '+−',
    say: 'Si les Noirs continuent tranquillement, avec ^b5 par exemple : ^Fou prend h6 ! Après ^g prend h6, ^Dame prend h6, # Cavalier g5 arrive, avec des menaces de mat en h7. Le Roi noir est en grand danger.' },
  { from: 'Qd2', line: 'Plan 3 : 10.e5', quiz: 'Quel coup réflexe pour éteindre l\'attaque ?', pause: 6,
    say: 'Alors à toi de jouer : quel est le coup réflexe pour éteindre l\'attaque blanche ? Un indice : il faut couper la diagonale du Fou d3.' },
  { play: 'f5!', mark: 'f5', arrows: 'Rd3h7 Gg7g5', sq: 'Gf5', key: '...f5 ! coupe la diagonale du Fou d3. À connaître par cœur !',
    say: 'f5 ! La réaction standard, à connaître par cœur. # On ferme la diagonale du Fou d3, et toute idée d\'attaque blanche disparaît. On garde même en réserve g5, pour chasser le Fou f4.' },
  { line: 'Variante : 12.Tfe1', play: 'Rfe1 Be7', arrows: 'Gg7g5 Gd7c5', ev: '=+',
    say: 'Si les Blancs ne prennent pas en passant, par exemple avec ^Tour e1, les Noirs ont une très bonne position : ^Fou e7 # renforce le Roi et prépare g5, ainsi que Cavalier c5. On pouvait même jouer g5 tout de suite.' },
  { from: 'f5', line: 'Plan 3 : 10.e5', play: 'exf6', mark: 'exf6',
    say: 'Les Blancs doivent donc absolument prendre en passant : e prend f6.' },
  { line: 'Variante : 12...Dxf6', play: 'Qxf6 Bg3 Nde5 Nxe5 Nxe5', sq: 'Rd3', arrows: 'Ge5d3 Gf6f1', ev: '=',
    say: 'On peut reprendre avec la ^Dame, pour mettre la pression sur la colonne f. Après ^Fou g3, ^Cavalier de e5, et les échanges ^en e5, ^… # notre Cavalier va prendre le Fou d3, puis Fou d7. Position active, aucun problème pour les Noirs !' },
  { from: 'exf6', line: 'Plan 3 : 10.e5', play: 'Nxf6', mark: 'Nxf6', arrows: 'Gc8d7 Ge6e5',
    say: 'Mais le plus simple, c\'est Cavalier prend f6. On obtient une bonne position de défense française, avec Fou d7 et la poussée e5 en ligne de mire.' },

  // ── Chapitre 7 ─────────────────────────────────────────────
  { card: { k: 'Chapitre 7', t: 'Pas peur du sacrifice !', pose: 'bonne-reponse' } },
  { ch: 'Pas peur du sacrifice', line: 'Variante : 13.Fxh6?', from: 'Nxf6', play: 'Bxh6? gxh6 Qxh6 Qe7', sq: 'Gg7', arrows: 'Ge7g7 Gf6h7', ev: '−+',
    key: 'Après ...f5 et ...Cxf6, le sacrifice en h6 ne marche plus.',
    say: 'Et le sacrifice en h6, maintenant ? ^Fou prend h6 n\'est pas bon. Il ne faut pas avoir peur ! Après ^g prend h6 et ^Dame prend h6, ^Dame e7 ! # La Dame vient colmater les trous en g7, et le Cavalier f6 défend h7. Les Noirs ont simplement une pièce de plus.' },
  { from: 'Nxf6', line: MAIN, play: 'Ne5 Nxe5 Bxe5 Bd7', sq: 'Re6', ev: '=',
    arrows: 'Ga8c8 Gd7e8 Ge8h5 Gf6g4', key: 'Idées : ...Cg4, ...Tc8, ...Fe8-h5. Surveiller e6.',
    say: 'Plus sérieux : ^Cavalier e5. On ^échange, ^Fou prend e5, puis ^Fou d7. Les Noirs ont un très bon jeu, typique de la défense française. # Les idées : Cavalier g4, Tour c8 sur la colonne c, et parfois Fou e8, puis h5, pour réactiver le Fou. Il faudra juste garder un œil sur le pion e6.' },

  // ── Bilan ─────────────────────────────────────────────────
  { card: { k: 'À retenir', t: 'Contre le Jobava', pose: 'lecon-terminee', bullets: [
      '...a6 empêche Cb5 et prépare ...b5',
      '...h6 : on attend. ...e6 seulement quand g4 n\'est plus possible',
      'Contre Fd3 ou h4 : ...c5 !, ...Cc6, ...Fg4, puis ...e5-e4',
      'Contre e5 et Dd2 : ...f5 ! et pas peur de Fxh6',
    ] },
    say: 'Récapitulons. Un : a6 empêche Cavalier b5 et prépare b5. Deux : h6, c\'est le coup d\'attente. On ne joue e6 que lorsque g4 n\'est plus possible, c\'est-à-dire après Cavalier f3. Trois : contre Fou d3 ou h4, c5 !, Cavalier c6, Fou g4, puis la poussée e5, puis e4. Et quatre : quand les Blancs poussent e5 et jouent Dame d2, f5 ! et pas peur du sacrifice en h6. Avec ça, tu as une arme simple et solide contre le Jobava. À toi de la tester dans tes parties !' },
];
