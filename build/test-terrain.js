// Shaded relief tile pyramid (data/terrain.json, images/terrain/<n>/<i>_<j>.webp; build/terrain/render_tiles.py).
// Data: every listed tile exists (514 px incl. the 1-px bleed), levels go from the whole world map down to the hill
// country. Browser (390x844 phone, DPR 2): relief on every chapter, only a handful of small tiles on first load,
// deeper levels load only when zoomed in (and only where they exist), the tiles on screen follow the view, the
// deepest level shows at Jerusalem at full zoom, the old tiles go once the new have loaded, ?terrain=0 is off.
// Usage: node build/test-terrain.js [url]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const ROOT = path.join(__dirname, '..');
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const T = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/terrain.json'), 'utf8'));
  const file = (n, i, j) => path.join(ROOT, T.src.replace('{n}', n).replace('{i}', i).replace('{j}', j));
  let missing = 0, bytes = 0, count = 0;
  T.levels.forEach(L => L.tiles.forEach(([i, j]) => { const f = file(L.n, i, j); if (!fs.existsSync(f)) missing++; else { bytes += fs.statSync(f).size; count++; } }));
  ok(`manifest: ${T.levels.length} levels, ${count} tiles, ${Math.round(bytes / 1024)} KB in all, none missing`, T.levels.length >= 9 && !missing && count > 300);
  ok('grid matches the map projection', T.grid.P === 512 && T.grid.bleed === 1 && JSON.stringify(T.grid.parallels) === '[30,40]' && T.grid.rotate[0] === -38);
  ok('coarse levels cover the whole world map, deep levels only the story lands', T.levels[0].boxes[0][0] <= -20 && T.levels[0].boxes[0][2] >= 95 && T.levels[8].tiles.length < 100);
  const extra = fs.readdirSync(path.join(ROOT, 'images/terrain')).filter(f => !/^\d+$/.test(f));
  ok('no stray images left in images/terrain ' + JSON.stringify(extra), !extra.length);

  const b = await chromium.launch();
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.recaps', 'off'); });
  const p = await ctx.newPage(); let tb = 0, tn = 0;
  p.on('pageerror', e => errs.push(String(e)));
  p.on('response', async r => { if (/images\/terrain\//.test(r.url())){ try { tb += (await r.body()).length; tn++; } catch(e){} } });
  await p.goto(url + '?ch=1', {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
  const st = () => p.evaluate(() => { const im = [...document.querySelectorAll('image.relief')]; return {on: document.body.classList.contains('terrain'), n: im.length, keys: __app.relief, lv: Math.max(...(__app.relief || []).map(k => +k.split('/')[0])), credit: !document.getElementById('tcredit').hidden}; });
  let s = await st();
  ok(`Chapter 1 shows the relief on load (${s.n} tiles, ${tn} requests, ${Math.round(tb / 1024)} KB) and the credit`, s.on && s.n >= 1 && s.credit);
  ok('first load stays small: under 300 KB and 40 tiles', tb < 300 * 1024 && tn <= 40);
  // every chapter
  const parts = await p.evaluate(() => __app.parts());
  for (const x of parts){ await p.evaluate(k => __app.go(k), x.k); await p.waitForTimeout(900); s = await st(); ok(`Chapter ${x.n} (${x.year}) relief on (${s.n} tiles)`, s.on && s.n >= 1); }
  // zoom in steps over Jerusalem: the level rises, few tiles on screen, the deepest at full zoom
  const J = [35.2, 31.8]; let last = -1, fine = true;
  for (const k of [1, 4, 12, 30, 70, 160]){
    await p.evaluate(([c, k]) => __app.fly(c, k), [J, k]); await p.waitForTimeout(1200);
    s = await st(); fine = fine && s.lv >= last && s.n <= 40; last = s.lv;
    const loaded = await p.evaluate(() => [...document.querySelectorAll('image.relief:not(.old)')].every(i => i.classList.contains('ok')));
    ok(`zoom ${k} at Jerusalem: level ${s.lv}, ${s.n} tiles, all loaded`, s.n >= 1 && s.n <= 40 && loaded);
  }
  ok('the level rises with the zoom and reaches the deepest (8) at full zoom', fine && last === 8);
  const before = tn;
  await p.evaluate(([c, k]) => __app.fly(c, k), [J, 160]); await p.waitForTimeout(500);
  ok('the same view loads nothing new', tn === before);
  // Babylon at deep zoom: no level-8 tiles exist there, so the best level there shows and nothing is blank
  await p.evaluate(([c, k]) => __app.fly(c, k), [[44.42, 32.54], 100]); await p.waitForTimeout(1500);
  s = await st(); ok(`Babylon at zoom 100: level ${s.lv} (no deep tiles outside the story lands), ${s.n} tiles`, s.n >= 1 && s.lv <= 5);
  await p.waitForTimeout(2600);
  ok('old tiles are gone once the new ones show', await p.evaluate(() => !document.querySelector('image.relief.old')));
  ok('no page errors ' + errs.join(' | '), !errs.length);
  // ?terrain=0
  const p2 = await ctx.newPage(); await p2.goto(url + '?ch=6&terrain=0', {waitUntil: 'networkidle'}); await p2.waitForTimeout(800);
  ok('?terrain=0: no relief', await p2.evaluate(() => !document.body.classList.contains('terrain') && !document.querySelector('image.relief')));
  await b.close();
  console.log(notes.join('\n'));
  const f = notes.filter(n => n.startsWith('FAIL')).length; console.log(f ? f + ' FAILED' : 'ALL PASS'); process.exit(f ? 1 : 0);
})();
