// Captures des e-mails (build/_emails_apercu/*.html) en largeur téléphone, pour la page de validation.
// Usage : node scripts/emails-apercus.mjs [abonnes|ccas]  → build/pack/emails[-ccas]/apercus/*.jpg
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const PROFIL = process.argv[2] || 'abonnes', SUF = PROFIL === 'abonnes' ? '' : '-' + PROFIL;
const src = path.join(here, `build/_emails${SUF}_apercu`), out = path.join(here, `build/pack/emails${SUF}/apercus`);
const SOMBRE = PROFIL === 'ccas' ? ['02-bienvenue', '09-cours-de-la-semaine', '13-resultats-tournoi'] : ['02-bienvenue-compte-gratuit', '07-confirmation-abonnement', '19-annonce-masterclass'];
const ORDI = PROFIL === 'ccas' ? ['02-bienvenue', '09-cours-de-la-semaine', '14-lettre-de-la-semaine'] : ['02-bienvenue-compte-gratuit', '19-annonce-masterclass', '26-lettre-plusieurs-nouvelles'];
fs.mkdirSync(path.join(out, 'sombre'), { recursive: true }); fs.mkdirSync(path.join(out, 'ordinateur'), { recursive: true });
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
for (const f of fs.readdirSync(src).filter(f => f.endsWith('.html')).sort()) {
  const p = await b.newPage({ viewport: { width: 420, height: 900 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(src, f)); await p.waitForLoadState('load');
  await p.screenshot({ path: path.join(out, f.replace('.html', '.jpg')), fullPage: true, type: 'jpeg', quality: 82 });
  await p.close(); console.log('aperçu', f);
}
// Quelques aperçus en mode sombre (Apple Mail, iOS…)
for (const f of SOMBRE) {
  const p = await b.newPage({ viewport: { width: 420, height: 900 }, deviceScaleFactor: 2, colorScheme: 'dark' });
  await p.goto('file://' + path.join(src, f + '.html')); await p.waitForLoadState('load');
  await p.screenshot({ path: path.join(out, 'sombre', f + '.jpg'), fullPage: true, type: 'jpeg', quality: 82 }); await p.close();
}
// Quelques aperçus sur ordinateur (fenêtre de messagerie de 1280 px)
for (const f of ORDI) {
  const p = await b.newPage({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
  await p.goto('file://' + path.join(src, f + '.html')); await p.waitForLoadState('load');
  await p.screenshot({ path: path.join(out, 'ordinateur', f + '.jpg'), fullPage: true, type: 'jpeg', quality: 82 }); await p.close();
}
await b.close();
