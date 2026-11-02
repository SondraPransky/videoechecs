// Images du pack réseaux sociaux : captures du motion, puis chaque visuel de src/visuels-data.js
// dans tous ses formats, et une page d'aperçu (build/pack/apercu.html) pour le community manager.
// Usage : node scripts/pack.mjs [--only id1,id2]   (les captures sont refaites à chaque fois)
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const PACK = path.join(here, 'build/pack');
const args = process.argv.slice(2);
const only = args.includes('--only') ? args[args.indexOf('--only') + 1].split(',') : null;
fs.mkdirSync(path.join(PACK, '_captures'), { recursive: true });
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });

// 1. Captures du motion (version longue), à un instant où chaque scène est complète
const SHOTS = { progression: ['s1', 5.4], progres: ['prog', 4.3], lecons: ['s3', 3.4], exercices: ['s6', 4.3], videos: ['videos', 4.6],
  masterclasses: ['s4', 4.0], parties: ['s5', 5.45], revue: ['revue', 4.2], forum: ['forum', 4.3], tournois: ['s7', 3.3] };
{
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  await page.goto('file://' + path.join(here, 'src/index.html'));
  await page.evaluate(() => window.ready);
  for (const [name, [scene, dt]] of Object.entries(SHOTS)) {
    const t = await page.evaluate(([s, d]) => window.TIMING.scenes.find(x => x.id === s).start + d, [scene, dt]);
    await page.evaluate(t => window.seekTo(t), t);
    await page.screenshot({ path: path.join(PACK, '_captures', name + '.png') });
  }
  await page.close();
}

// 2. Visuels dans tous les formats
const data = await (async () => {
  const page = await browser.newPage();
  await page.goto('file://' + path.join(here, 'src/visuels.html') + '?id=01-progression&w=100&h=100');
  const d = await page.evaluate(() => ({ items: window.VISUELS.map(v => ({ id: v.id, tpl: v.tpl, theme: v.theme, only: v.only || null, t: v.t, e: v.e })), posts: window.FORMATS.posts }));
  await page.close();
  return d;
})();
const index = [];
for (const it of data.items) {
  if (only && !only.includes(it.id)) continue;
  const dir = it.tpl.startsWith('id-') ? '00-identite' : it.id;
  fs.mkdirSync(path.join(PACK, 'images', dir), { recursive: true });
  for (const [suffix, w, h, usage, extra] of it.only || data.posts) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    const q = new URLSearchParams({ id: it.id, w, h, ...(extra || {}) });
    await page.goto('file://' + path.join(here, 'src/visuels.html') + '?' + q);
    await page.evaluate(() => window.ready);
    const file = path.join('images', dir, `${it.id.replace(/^id-/, '')}-${suffix}.jpg`);
    await page.screenshot({ path: path.join(PACK, file), type: 'jpeg', quality: 92 });
    await page.close();
    index.push({ file, usage, w, h, id: it.id, theme: it.theme, titre: it.t ? `${it.t} ${it.e}` : it.id });
    console.log('écrit', file);
  }
}
await browser.close();

// 3. Page d'aperçu
if (!only) {
  const groups = {};
  index.forEach(x => (groups[x.id] ||= []).push(x));
  const html = `<!doctype html><html lang="fr"><head><meta charset="utf-8"><title>Pack réseaux echecs.com</title>
<style>body{margin:0;padding:40px;background:#06080c;color:#f4f1ea;font:16px/1.4 system-ui,sans-serif}h1{font-size:34px;margin:0 0 8px}h2{margin:44px 0 6px;font-size:22px;color:#fae361}
p{color:#c9d1dc;margin:0 0 16px}.g{display:flex;flex-wrap:wrap;gap:18px;align-items:flex-end}figure{margin:0}img{display:block;height:260px;border-radius:10px;box-shadow:0 10px 30px rgba(0,0,0,.5)}
figcaption{margin-top:6px;font-size:13px;color:#93b9e2;max-width:360px}a{color:inherit}</style></head><body>
<h1>Pack réseaux sociaux — echecs.com Académie</h1><p>Cliquer sur une image pour l'ouvrir en taille réelle. Les vidéos sont dans le dossier <b>videos/</b>, les textes de publication dans <b>TEXTES-PUBLICATIONS.md</b>.</p>
${Object.entries(groups).map(([id, xs]) => `<h2>${id}</h2><p>${xs[0].titre} · ambiance ${xs[0].theme}</p><div class="g">${xs.map(x => `<figure><a href="${x.file}"><img src="${x.file}" loading="lazy"></a><figcaption>${x.w}×${x.h} — ${x.usage}</figcaption></figure>`).join('')}</div>`).join('\n')}
</body></html>`;
  fs.writeFileSync(path.join(PACK, 'apercu.html'), html);
  console.log(index.length, 'images');
}
