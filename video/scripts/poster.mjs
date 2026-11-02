// Rend l'affiche de la vidéo (src/poster.html) en JPEG 1920×1080.
// Usage : node scripts/poster.mjs [build/poster.jpg]
import { chromium } from 'playwright';
import path from 'path';

const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const out = process.argv[2] || path.join(here, 'build/poster.jpg');
const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto('file://' + path.join(here, 'src/poster.html'));
await page.evaluate(() => window.ready);
await page.screenshot({ path: out, type: 'jpeg', quality: 92 });
await browser.close();
console.log('écrit', out);
