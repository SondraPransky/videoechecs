// Poses de la mascotte en PNG transparent (jaune, traits clairs : pour fond sombre), pour les e-mails.
// Usage : node scripts/mascotte-png.mjs pose1,pose2…  → build/_mascotte/<pose>.png (520 px de haut, marge pour les accessoires)
import { chromium } from 'playwright';
import path from 'path';
import fs from 'fs';
const here = path.dirname(path.dirname(new URL(import.meta.url).pathname));
const out = path.join(here, 'build/_mascotte'); fs.mkdirSync(out, { recursive: true });
const poses = process.argv[2].split(',');
const b = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
const p = await b.newPage({ viewport: { width: 400, height: 520 } });
const tmp = path.join(out, '_page.html');
fs.writeFileSync(tmp, `<!doctype html><html><body style="margin:0;background:transparent"><div id="m" style="width:344px;height:420px;margin:90px auto 0"></div><script src="${path.join(here, 'assets/mascot/poses.js')}"></script></body></html>`);
await p.goto('file://' + tmp);
await p.waitForFunction(() => window.MASCOT_POSES);
for (const pose of poses) {
  await p.evaluate(pose => {
    const m = document.getElementById('m'); m.innerHTML = window.MASCOT_POSES[pose];
    const svg = m.querySelector('svg'); svg.style.width = '100%'; svg.style.height = '100%'; svg.style.overflow = 'visible';
    svg.style.setProperty('--mascot', '#fae361'); svg.style.setProperty('--line', '#f4f1ea');
    m.querySelectorAll('.shadow').forEach(s => s.style.display = 'none');
    document.getAnimations().forEach(a => { a.pause(); a.currentTime = 1100; });
  }, pose);
  await p.screenshot({ path: path.join(out, pose + '.png'), omitBackground: true });
  console.log('mascotte', pose);
}
await b.close();
