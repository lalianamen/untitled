// Render a seekable HTML timeline to an H.264 MP4 by screenshotting every frame.
// usage: node render.mjs <html> <width> <height> <fps> <duration> <out.mp4>
import { createRequire } from 'node:module';
import { spawn } from 'node:child_process';
const require = createRequire(process.env.NODE_MODULES || '/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');

const [,, html, W, H, FPS, DUR, OUT] = process.argv;
const width = +W, height = +H, fps = +FPS, duration = +DUR;
const FF = process.env.FFMPEG || 'ffmpeg';

const ff = spawn(FF, ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-i', '-',
  '-c:v', 'libx264', '-preset', 'medium', '-crf', '18', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', OUT],
  { stdio: ['pipe', 'inherit', 'inherit'] });

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width, height }, deviceScaleFactor: 1 });
await page.goto('file://' + html);
await page.evaluate(() => document.fonts.ready);
await page.evaluate(() => window.seek(0));
await page.waitForTimeout(300);

const total = Math.round(duration * fps);
const t0 = Date.now();
for (let i = 0; i < total; i++) {
  const t = i / fps;
  await page.evaluate(t => window.seek(t), t);
  const buf = await page.screenshot({ type: 'png', animations: 'disabled', caret: 'hide' });
  if (!ff.stdin.write(buf)) await new Promise(r => ff.stdin.once('drain', r));
  if (i % (fps * 5) === 0) console.log(`frame ${i}/${total}  t=${t.toFixed(1)}s  ${((Date.now() - t0) / 1000).toFixed(0)}s elapsed`);
}
ff.stdin.end();
await new Promise(r => ff.on('close', r));
await browser.close();
console.log('done', OUT);
