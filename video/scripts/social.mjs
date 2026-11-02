// Visuels pour les réseaux sociaux (src/social.html?fmt=...) et cadres des vidéos verticale et carrée.
// Usage : node scripts/social.mjs [dossier de sortie, par défaut build/reseaux]
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const out = process.argv[2] || path.join(here, 'build/reseaux');
fs.mkdirSync(out, { recursive: true });
// [fichier, format de social.html, largeur, hauteur]
const SHOTS = [
  ['instagram-post-1080x1080.jpg', 'post', 1080, 1080],
  ['story-reel-tiktok-1080x1920.jpg', 'story', 1080, 1920],
  ['banniere-x-linkedin-1500x500.jpg', 'banner', 1500, 500],
  ['cadre-vertical.png', 'frame-vertical', 1080, 1920],
  ['cadre-carre.png', 'frame-square', 1080, 1080],
];
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
for (const [file, fmt, w, h] of SHOTS) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto('file://' + path.join(here, 'src/social.html') + '?fmt=' + fmt);
  await page.evaluate(() => window.ready);
  const p = path.join(out, file);
  await page.screenshot(file.endsWith('.png') ? { path: p } : { path: p, type: 'jpeg', quality: 92 });
  await page.close();
  console.log('écrit', p);
}
await browser.close();
