// Prépare une leçon vidéo à partir de lecons/<nom>/lecon.mjs.
//   node lecons/build.mjs <nom> plan    → build/lecons/<nom>/plan.json (répliques à faire lire)
//   node lecons/build.mjs <nom> timing  → build/lecons/<nom>/data.js, events.json, sous-titres.vtt
// Entre les deux, lecons/voix.py produit les voix et build/lecons/<nom>/voix/durees.json.
import { Chess } from 'chess.js';
import fs from 'fs';
import path from 'path';
import crypto from 'crypto';

const here = path.dirname(new URL(import.meta.url).pathname);
const [name, step = 'plan'] = process.argv.slice(2);
if (!name) { console.error('usage : node lecons/build.mjs <nom> plan|timing'); process.exit(1); }
const out = path.join(here, '..', 'build', 'lecons', name);
fs.mkdirSync(out, { recursive: true });
const { beats, meta } = await import(path.join(here, name, 'lecon.mjs'));

const FR = { N: 'C', B: 'F', R: 'T', Q: 'D', K: 'R' };
const START = new Chess().fen();

// Texte : « ^ » = instant d'un coup, « # » = apparition des flèches. On garde la position
// (en caractères du texte nettoyé) de chaque repère.
function parseSay(raw) {
  let text = '', moves = [], arrows = null;
  for (const ch of raw || '') {
    if (ch === '^') moves.push(text.length);
    else if (ch === '#') arrows = text.length;
    else text += ch;
  }
  text = text.replace(/\s+/g, ' ').replace(/ ([,.])/g, '$1').trim();
  return { text, moves, arrows };
}

// ───────────── Étape 1 : simulation des coups ─────────────
const marks = { start: { fen: START, path: [] } };
let board = new Chess(), linePath = [], ch = '', line = '';
const plan = beats.map((b, i) => {
  if (b.from) {
    const m = marks[b.from];
    if (!m) throw new Error(`passage ${i} : position « ${b.from} » inconnue`);
    board = new Chess(m.fen); linePath = m.path.slice();
  }
  if (b.ch !== undefined) ch = b.ch;
  if (b.line !== undefined) line = b.line;
  const startFen = board.fen();
  const moves = [];
  for (const tok of (b.play || '').split(/\s+/).filter(Boolean)) {
    const ann = (tok.match(/[!?]+$/) || [''])[0];
    const san = tok.slice(0, tok.length - ann.length);
    const num = board.moveNumber(), color = board.turn();
    let mv;
    try { mv = board.move(san); } catch { throw new Error(`passage ${i} : coup illégal « ${tok} » dans ${board.fen()}`); }
    const m = { from: mv.from, to: mv.to, san: mv.san + ann, color, num, piece: mv.piece,
      fr: mv.san.replace(/[NBRQK]/g, c => FR[c]).replace(/=([CFTD])/, '=$1') + ann, fen: board.fen() };
    if (mv.isKingsideCastle()) m.rook = color === 'w' ? ['h1', 'f1'] : ['h8', 'f8'];
    if (mv.isQueensideCastle()) m.rook = color === 'w' ? ['a1', 'd1'] : ['a8', 'd8'];
    if (mv.isEnPassant()) m.ep = mv.to[0] + mv.from[1];
    if (mv.promotion) m.promo = mv.promotion;
    moves.push(m); linePath.push({ fr: m.fr, color, num, fig: mv.piece });
  }
  if (b.mark) marks[b.mark] = { fen: board.fen(), path: linePath.slice() };
  const say = parseSay(b.say);
  if (say.moves.length && say.moves.length !== moves.length)
    throw new Error(`passage ${i} : ${say.moves.length} repères ^ pour ${moves.length} coups`);
  const id = say.text ? crypto.createHash('sha1').update(say.text).digest('hex').slice(0, 12) : null;
  return { i, id, text: say.text, marks: say.moves, arrowMark: say.arrows, ch, line, startFen, endFen: board.fen(),
    moves, path: linePath.slice(), arrows: (b.arrows || '').split(/\s+/).filter(Boolean), sq: (b.sq || '').split(/\s+/).filter(Boolean),
    key: b.key || null, ev: b.ev || null, quiz: b.quiz || null, pause: b.pause || 5, card: b.card || null,
    fast: b.fast || null, game: b.game || null };
});

if (step === 'plan') {
  fs.writeFileSync(path.join(out, 'plan.json'), JSON.stringify({ meta, beats: plan }, null, 1));
  const chars = plan.reduce((s, b) => s + b.text.length, 0);
  // Script lisible, pour relecture avant d'enregistrer la voix
  let md = `# ${meta.title} — script de la voix off\n\n${meta.kicker}. ${meta.author}.\n\n`;
  for (const b of plan) {
    if (b.card) { md += `\n## ${b.card.k} — ${b.card.t}\n\n`; if (b.card.bullets) md += b.card.bullets.map((x, k) => `${k + 1}. ${x}`).join('\n') + '\n\n'; }
    const coups = b.moves.map((m, k) => (m.color === 'w' ? `${m.num}.` : k === 0 ? `${m.num}...` : '') + m.fr).join(' ');
    if (!b.text) continue;
    md += (coups ? `**${coups}**${b.line ? ` _(${b.line})_` : ''}${b.quiz ? ' — **QUIZ**' : ''}\n` : b.quiz ? '**QUIZ**\n' : '') + `> ${b.text}\n\n`;
  }
  fs.writeFileSync(path.join(here, name, 'script.md'), md);
  console.log(`${plan.length} passages, ${plan.reduce((s, b) => s + b.moves.length, 0)} coups, ${chars} caractères de voix off → ${out}/plan.json`);
  process.exit(0);
}

// ───────────── Étape 2 : chronologie calée sur la voix ─────────────
const durs = JSON.parse(fs.readFileSync(path.join(out, 'voix', 'durees.json'), 'utf8'));
const LEAD = 0.3, MORPH = 0.7, ANIM = 0.42;
let t = 0, prevEnd = START;
const events = [], subs = [];
// Instant (en s depuis le début de la réplique) où la voix atteint le caractère k
const charTime = (d, k) => {
  if (d.chars) { const c = d.chars[Math.min(k, d.chars.length - 1)]; return c ?? d.dur * k / d.len; }
  return d.dur * k / Math.max(1, d.len);
};
const timeline = plan.map(b => {
  const d = b.id ? durs[b.id] : null;
  if (b.id && !d) throw new Error(`voix manquante pour le passage ${b.i} (${b.id})`);
  const vdur = d ? d.dur : 0;
  const r = { ...b, t0: t, voice: d ? { at: t + LEAD, dur: vdur, id: b.id } : null };
  if (b.card) {
    r.dur = d ? LEAD + vdur + 0.9 : 2.6;
    // Points du bilan : chacun apparaît quand la voix dit « Un : », « Deux : »…
    if (b.card.bullets && d) {
      const re = /\b(Un|Deux|Trois|Quatre|Cinq)\s*:/gi, at = [];
      for (let m; (m = re.exec(b.text));) at.push(t + LEAD + charTime(d, m.index));
      r.bulletsAt = b.card.bullets.map((_, k) => at[k] ?? t + LEAD + vdur * (0.15 + 0.6 * k / b.card.bullets.length));
    }
    events.push({ t: t, type: 'whoosh' });
  } else {
    r.morph = b.startFen !== prevEnd ? prevEnd : null;
    const first = r.morph ? MORPH + 0.1 : 0.2;
    const n = b.moves.length;
    let times;
    if (b.fast) times = b.moves.map((_, k) => first + 0.6 + k * b.fast);
    else if (b.marks.length) times = b.marks.map(k => Math.max(first, LEAD + charTime(d, k) - 0.05));
    else if (n === 1) times = [Math.max(first, LEAD)];
    else times = b.moves.map((_, k) => first + k * Math.min(1.1, Math.max(0.55, (vdur * 0.8) / n)));
    for (let k = 1; k < times.length; k++) times[k] = Math.max(times[k], times[k - 1] + (b.fast ? b.fast * 0.9 : 0.5));
    const anim = b.fast ? Math.min(ANIM, b.fast * 0.75) : ANIM;
    r.moves = b.moves.map((m, k) => ({ ...m, t: t + times[k], a: anim }));
    const lastMove = n ? times[n - 1] + anim : 0;
    r.arrowsAt = t + (b.arrowMark !== null && d ? LEAD + charTime(d, b.arrowMark) : Math.max(lastMove + 0.15, first));
    r.keyAt = Math.max(r.arrowsAt, t + 0.4);
    for (const m of r.moves) events.push({ t: m.t + m.a, type: m.san.includes('x') ? 'capture' : 'move' });
    let dur = Math.max(LEAD + vdur + 0.55, lastMove + 0.9);
    if (b.quiz) { r.quizAt = t + LEAD + vdur + 0.2; dur = LEAD + vdur + 0.4 + b.pause + 0.3;
      for (let s = 0; s < b.pause; s++) events.push({ t: r.quizAt + s, type: 'tick' });
      events.push({ t: r.quizAt + b.pause, type: 'reveal' }); }
    r.dur = dur;
    prevEnd = b.endFen;
  }
  // Sous-titres : phrases découpées, durée proportionnelle à la position dans le texte
  if (d) {
    const parts = b.text.match(/[^.!?…:]+(?:[.!?…:]+|$)/g).map(s => s.trim()).filter(Boolean);
    const chunks = [];
    for (const p of parts) {
      if (p.length <= 95) { chunks.push(p); continue; }
      let cur = '';
      for (const w of p.split(/(?<=,) /)) { if ((cur + ' ' + w).length > 95 && cur) { chunks.push(cur); cur = w; } else cur = cur ? cur + ' ' + w : w; }
      if (cur) chunks.push(cur);
    }
    let k = 0;
    for (const c of chunks) {
      const i0 = b.text.indexOf(c, k); k = i0 + c.length;
      subs.push({ a: t + LEAD + charTime(d, i0), b: t + LEAD + charTime(d, k), text: c });
    }
  }
  t += r.dur;
  return r;
});
for (let i = 0; i < subs.length - 1; i++) subs[i].b = Math.min(subs[i].b + 0.25, subs[i + 1].a);

const total = +t.toFixed(3);
fs.writeFileSync(path.join(out, 'data.js'), `window.LESSON = ${JSON.stringify({ meta, total, beats: timeline, subs })};\n`);
fs.writeFileSync(path.join(out, 'events.json'), JSON.stringify({ total, events, voice: timeline.filter(b => b.voice).map(b => b.voice) }));
const ts = s => new Date(s * 1000).toISOString().slice(11, 23);
fs.writeFileSync(path.join(out, 'sous-titres.vtt'), 'WEBVTT\n\n' + subs.map(s => `${ts(s.a)} --> ${ts(s.b)}\n${s.text}\n`).join('\n'));
console.log(`durée ${Math.floor(total / 60)} min ${Math.round(total % 60)} s, ${timeline.length} passages → ${out}`);
