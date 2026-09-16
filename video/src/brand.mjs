import { createRequire } from 'node:module';
const require = createRequire(process.env.NODE_MODULES || '/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const [,, html, outdir] = process.argv;
const jobs = [
  ['banner_es', 2560, 1440], ['banner_en', 2560, 1440],
  ['avatar_mono', 800, 800], ['avatar_word', 800, 800],
];
const browser = await chromium.launch();
for (const [t, w, h] of jobs) {
  const page = await browser.newPage({ viewport: { width: w, height: h } });
  await page.goto('file://' + html + '?t=' + t);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(200);
  await page.screenshot({ path: `${outdir}/${t}.png` });
  await page.close();
  console.log('ok', t);
}
await browser.close();
