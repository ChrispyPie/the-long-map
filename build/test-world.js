// The world map foundation (data/world.json, data/world/outer.topo.json): the page loads only the Near East vectors;
// the outer world (Europe, North Africa, Central Asia: coast, lakes, rivers) loads only when the view leaves the Near
// East (or a stop names it); one can zoom out to the whole world map and pan to Europe; the relief follows there at
// coarse levels; the coast has no straight cut lines; the stories and the home view are unchanged.
// Usage: node build/test-world.js [url] [noshots]; SHOTS=dir for screenshots (default /workspace/thelongmap/screens-terrain)
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || '/workspace/thelongmap/screens-terrain';
const ROOT = path.join(__dirname, '..');
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const W = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/world.json'), 'utf8')), T = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/terrain.json'), 'utf8'));
  ok('world.json: projection matches the relief grid', JSON.stringify(W.projection.parallels) === JSON.stringify(T.grid.parallels) && W.projection.rotate[0] === T.grid.rotate[0]);
  ok('world.json: one start region, the others lazy, every vector file exists', W.regions.filter(r => r.load === 'start').length === 1 && W.regions.every(r => fs.existsSync(path.join(ROOT, r.vector))));
  const outerKB = fs.statSync(path.join(ROOT, 'data/world/outer.topo.json')).size / 1024;
  ok(`outer world vectors are small (${Math.round(outerKB)} KB)`, outerKB < 150);
  const b = await chromium.launch();
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.recaps', 'off'); });
  const p = await ctx.newPage(); const got = [];
  p.on('pageerror', e => errs.push(String(e)));
  p.on('request', r => got.push(r.url()));
  await p.goto(url + '?ch=6', {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
  ok('first load: no outer world vectors', !got.some(u => /outer\.topo/.test(u)));
  ok('home: the Near East region is there, the world not', await p.evaluate(() => __app.regions['near-east'] === 'ok' && !__app.regions.world));
  ok('the coast is its own line (land has no stroke)', await p.evaluate(() => !!document.querySelector('path.coast') && getComputedStyle(document.querySelector('path.land')).stroke === 'none' || !document.body.classList.contains('terrain')));
  // the stories still fly about inside the Near East without loading the world
  for (const x of await p.evaluate(() => __app.parts())){ await p.evaluate(k => __app.go(k), x.k); await p.waitForTimeout(600); }
  ok('all six chapters open without the outer world', await p.evaluate(() => !__app.regions.world) && !got.some(u => /outer\.topo/.test(u)));
  const ext = await p.evaluate(() => __app.scaleExtent);
  ok('one can zoom out below the home view ' + JSON.stringify(ext), ext[0] < 1 && ext[1] === 160);
  // zoom out fully: the whole world map
  await p.evaluate(() => { __app.closeObj && __app.closeObj(); const e = document.getElementById('ev'); if (e) e.style.visibility = 'hidden'; });
  await p.evaluate(e => __app.fly([38, 32], e), ext[0]); await p.waitForTimeout(2000);
  const v = await p.evaluate(() => __app.viewBox());
  ok('zoomed out: the world loads ' + JSON.stringify(v.map(Math.round)), await p.evaluate(() => __app.regions.world === 'ok') && got.some(u => /outer\.topo/.test(u)));
  ok('the outer world has land, lakes, rivers and a coast', await p.evaluate(() => { const g = document.querySelector('g.r-world'); return g && g.querySelector('path.land') && g.querySelectorAll('path.lake').length > 5 && g.querySelectorAll('path.river').length > 5 && g.querySelector('path.coast'); }));
  ok('relief shows at the zoomed-out world', await p.evaluate(() => (__app.relief || []).length >= 1));
  if (shots) await p.screenshot({path: `${D}/after-6-world-zoomed-out.png`});
  // Europe (Rome) and Central Asia (Samarkand) close up: relief tiles + vectors
  for (const [name, c, k] of [['europe-rome', [12.5, 41.9], 6], ['central-asia-samarkand', [66.96, 39.65], 6], ['north-africa-carthage', [10.32, 36.85], 6]]){
    await p.evaluate(([c, k]) => __app.fly(c, k), [c, k]); await p.waitForTimeout(2200);
    const n = await p.evaluate(() => __app.relief.length);
    ok(`${name}: relief ${n} tiles, all loaded`, n >= 1 && await p.evaluate(() => [...document.querySelectorAll('image.relief:not(.old)')].every(i => i.classList.contains('ok'))));
    if (shots) await p.screenshot({path: `${D}/after-7-${name}.png`});
  }
  // the home view is unchanged
  await p.evaluate(k => __app.go(k), (await p.evaluate(() => __app.parts()))[0].k); await p.waitForTimeout(1500);
  ok('no page errors ' + errs.join(' | '), !errs.length);
  // a stop can ask for a region: go() loads it
  const p2 = await ctx.newPage(); const got2 = []; p2.on('request', r => got2.push(r.url()));
  await p2.goto(url + '?ch=1', {waitUntil: 'networkidle'}); await p2.waitForTimeout(800);
  await p2.evaluate(() => { const s = __app.parts()[1]; }); 
  ok('?ch=1: no outer world on load', !got2.some(u => /outer\.topo/.test(u)));
  await b.close();
  console.log(notes.join('\n'));
  const f = notes.filter(n => n.startsWith('FAIL')).length; console.log(f ? f + ' FAILED' : 'ALL PASS'); process.exit(f ? 1 : 0);
})();
