import { chromium } from 'playwright';
const [dir, out, ...ids] = process.argv.slice(2);
const b = await chromium.launch();
for (const id of ids) for (const [w, h] of [[1080, 1080], [1080, 1920], [1200, 630]]) {
  const p = await b.newPage({ viewport: { width: w, height: h } });
  p.on('pageerror', e => console.log('ERR', id, e.message));
  await p.goto(`file://${dir}/src/visuels.html?id=${id}&w=${w}&h=${h}`); await p.evaluate(() => window.ready);
  await p.screenshot({ path: `${out}/${id}-${w}x${h}.png` }); await p.close();
}
await b.close();
