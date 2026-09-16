// usage: node stills.mjs <html> <w> <h> <outdir> t1 t2 t3 ...
import { createRequire } from 'node:module';
const require = createRequire(process.env.NODE_MODULES || '/opt/node22/lib/node_modules/');
const { chromium } = require('playwright');
const [,, html, W, H, outdir, ...times] = process.argv;
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: +W, height: +H } });
await page.goto('file://' + html);
await page.evaluate(() => document.fonts.ready);
for (const ts of times) {
  await page.evaluate(t => window.seek(t), +ts);
  await page.screenshot({ path: `${outdir}/still_${W}x${H}_${(+ts).toFixed(1)}.png` });
}
await browser.close();
console.log('stills ok');
