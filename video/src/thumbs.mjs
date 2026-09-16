import { createRequire } from 'node:module';
const require = createRequire(process.env.NODE_MODULES || '/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const [,, html, outdir] = process.argv;
const jobs = [
  ['pain', 1080, 1920, 'shorts_thumb_A_pain'],
  ['benefit', 1080, 1920, 'shorts_thumb_B_benefit'],
  ['pain', 1280, 720, 'youtube_thumb_A_pain'],
  ['benefit', 1280, 720, 'youtube_thumb_B_benefit'],
];
const browser = await chromium.launch();
for (const [v, w, h, name] of jobs) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto('file://' + html + '?v=' + v);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  await page.screenshot({ path: `${outdir}/${name}.png` });
  await page.close();
  console.log('ok', name);
}
await browser.close();
