// Rend src/index.html image par image (timeline GSAP pilotée par seekTo) et encode en MP4.
// Usage : node render.mjs [sortie.mp4] [--from s] [--to s] [--fps n] [--frames t1,t2,...]
import { chromium } from 'playwright';
import { spawn, execSync } from 'child_process';
import path from 'path';
import fs from 'fs';

const args = process.argv.slice(2);
const opt = (k, d) => { const i = args.indexOf(k); return i >= 0 ? args[i + 1] : d; };
const out = args[0] && !args[0].startsWith('--') ? args[0] : 'build/video-muette.mp4';
const fps = +opt('--fps', 30);
const stills = opt('--frames', null);
const ffmpeg = execSync("python3 -c 'import imageio_ffmpeg as f;print(f.get_ffmpeg_exe())'").toString().trim();
const here = path.dirname(new URL(import.meta.url).pathname);

const browser = await chromium.launch({ executablePath: process.env.CHROMIUM || '/opt/pw-browsers/chromium', args: ['--allow-file-access-from-files'] });
const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
await page.goto('file://' + path.join(here, 'src/index.html'));
await page.evaluate(() => window.ready);
const total = await page.evaluate(() => window.TOTAL);
fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });

if (stills) {
  for (const t of stills.split(',').map(Number)) {
    await page.evaluate(t => window.seekTo(t), t);
    await page.screenshot({ path: `${out}-${String(t).padStart(5, '0')}.png` });
  }
  await browser.close();
  process.exit(0);
}

const from = +opt('--from', 0), to = +opt('--to', total);
const enc = spawn(ffmpeg, ['-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
  '-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', out], { stdio: ['pipe', 'ignore', 'inherit'] });
const n = Math.round((to - from) * fps);
for (let i = 0; i < n; i++) {
  await page.evaluate(t => window.seekTo(t), from + i / fps);
  const buf = await page.screenshot({ type: 'jpeg', quality: 95 });
  if (!enc.stdin.write(buf)) await new Promise(r => enc.stdin.once('drain', r));
  if (i % 150 === 0) console.log(`image ${i}/${n}`);
}
enc.stdin.end();
await new Promise(r => enc.on('close', r));
await browser.close();
console.log('écrit', out);
