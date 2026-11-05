// Images « ordinateur » des e-mails CCAS, toutes au même format, pour les partager : l'e-mail tel qu'il s'ouvre dans une messagerie
// (bandeau expéditeur / objet en haut). Écrit build/apercus-emails-ccas/ordinateur-ecran/ (1920 × 1200, identiques) et ordinateur-complet/ (même largeur, e-mail entier).
// Usage : node scripts/apercus-ordinateur-ccas.mjs
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const src = path.join(here, 'build/_emails-ccas_apercu'), base = path.join(here, 'build/apercus-emails-ccas');
const tel = fs.readdirSync(path.join(base, 'telephone')).filter(f => f.endsWith('.jpg')).sort();   // ordre du parcours (01-…)
const ecran = path.join(base, 'ordinateur-ecran'), complet = path.join(base, 'ordinateur-complet');
for (const d of [ecran, complet]) { fs.rmSync(d, { recursive: true, force: true }); fs.mkdirSync(d, { recursive: true }); }
const files = fs.readdirSync(src).filter(f => f.endsWith('.html'));
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
for (const t of tel) {
  const slug = t.slice(3, -4), f = files.find(x => x.slice(3, -5) === slug); if (!f) continue;
  const p = await b.newPage({ viewport: { width: 1280, height: 800 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + path.join(src, f), { waitUntil: 'networkidle' }); await p.evaluate(() => document.fonts.ready);
  await p.evaluate(() => {
    const boite = document.body.firstElementChild; const objet = document.title;
    const exp = 'Europe Échecs · Activités Sociales';
    boite.remove();
    const h = document.createElement('div');
    h.style.cssText = 'background:#fff;border-bottom:1px solid #e4e1d8;padding:22px 40px;font-family:Signika,Arial,sans-serif;color:#1d1d1b';
    h.innerHTML = `<div style="font-size:24px;font-weight:600;margin-bottom:10px">${objet}</div>
      <div style="display:flex;align-items:center;gap:12px;font-size:15px;color:#6b6b66"><img src="img/favicon.png" style="width:36px;height:36px;border-radius:50%">
      <span><b style="color:#1d1d1b">${exp}</b><br>à moi</span></div>`;
    document.body.prepend(h);
  });
  await p.screenshot({ path: path.join(ecran, t), type: 'jpeg', quality: 85 });   // 1920 × 1200, même format pour tous
  await p.screenshot({ path: path.join(complet, t), fullPage: true, type: 'jpeg', quality: 82 });
  await p.close(); console.log('ordinateur', t);
}
await b.close();
