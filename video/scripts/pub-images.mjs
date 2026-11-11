// Images fixes des publicités (src/pub.html) : pour chaque question, 3 vues (question, réponse, appel final)
// utilisables seules ou en carrousel, dans les formats des réseaux, en thème nuit et soleil (fond jaune).
// Sortie : build/pack/images/00-publicites/pub-N/
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';

const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const OUT = path.join(here, 'build/pack/images/00-publicites');
const VUES = [['1-question', 3.5], ['2-reponse', 13.1], ['3-final', 16.8]];   // pubs de 17,2 s
// suffixe, fmt de la page, viewport, échelle (taille finale = viewport × échelle), thèmes
const FORMATS = [
  ['story-1080x1920', 'story', [1080, 1920], 1, ['nuit', 'soleil']],
  ['portrait-1080x1350', 'feed', [1080, 1350], 1, ['nuit', 'soleil']],
  ['carre-1080x1080', 'carre', [1080, 1080], 1, ['nuit', 'soleil']],
  ['x-1600x900', 'wide', [1920, 1080], 1600 / 1920, ['nuit']],
  ['lien-1200x628', 'wide', [1920, 1005], 1200 / 1920, ['nuit']],
];
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
let n = 0;
for (const q of (process.env.PUBS || "1 2 3 4 5").split(" ").map(Number)) {
  const dir = path.join(OUT, `pub-${q}`);
  fs.mkdirSync(dir, { recursive: true });
  for (const [suffix, fmt, [w, h], scale, themes] of FORMATS) {
    for (const theme of themes) {
      const page = await browser.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: scale });
      await page.goto('file://' + path.join(here, 'src/pub.html') + `?q=${q}&fmt=${fmt}&theme=${theme}&still=1`);
      await page.evaluate(() => window.ready);
      for (const [vue, t] of VUES) {
        await page.evaluate(t => window.seekTo(t), t);
        const file = path.join(dir, `pub-${q}-${vue}-${suffix}${theme === 'soleil' ? '-jaune' : ''}.jpg`);
        await page.screenshot({ path: file, type: 'jpeg', quality: 92 });
        n++;
      }
      await page.close();
    }
  }
  console.log(`pub ${q} : images écrites`);
}
await browser.close();
console.log(n, 'images');
