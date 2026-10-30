// Every vignette in chapters 1-4, phone (390x844) and desktop: the card comes in on its beat with all its
// pictures loaded, inside the film and clear of the subtitles and year. A pair sits side by side (never
// stacked) at one height, and enlarged it stays side by side, top edge in place, naming each picture's caption. The fx overlay sits on
// illustrations only and is gone with reduced motion. No page errors.
// Usage: node build/test-vignettes-all.js [url]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8941/';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const J = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
  const cases = [];
  for (const [y, f] of [[-1207, '1207bc'], [-1150, '1150bc'], [-1000, '1000bc'], [-930, '930bc']]){
    const d = J('data/stories/jews/' + f + '.json');
    for (const [reel, bs] of [['intro', d.transitionIn.beats], ['play', d.play.beats]])
      bs.forEach((b, i) => b.vignette && (!process.env.ONLY || String(y) === process.env.ONLY) && cases.push({y, reel, i, v: b.vignette}));   // ONLY=-1150 runs one chapter
  }
  const b = await chromium.launch();
  const V = p => p.evaluate(() => { const e = document.getElementById('vig'), r = e.getBoundingClientRect();
    const ims = [...e.querySelectorAll('img')].filter(im => getComputedStyle(im).display !== 'none');
    const ct = document.getElementById('captext'), cr = ct.getBoundingClientRect(), cy = document.getElementById('cyear').getBoundingClientRect(), vp = document.getElementById('vp').getBoundingClientRect();
    const fx = e.querySelector('.vigfx');
    return {shown: !e.hidden && e.classList.contains('in'), r: [r.left, r.top, r.right, r.bottom].map(Math.round),
      ims: ims.map(im => { const q = im.getBoundingClientRect(); return {src: im.getAttribute('src'), loaded: im.complete && im.naturalWidth > 0, r: [q.left, q.top, q.right, q.bottom].map(Math.round), photo: im.classList.contains('photo'), anim: getComputedStyle(im).animationName}; }),
      cap: ct.offsetHeight ? [cr.left, cr.top, cr.right, cr.bottom].map(Math.round) : null, cy: [cy.left, cy.top, cy.right, cy.bottom].map(Math.round),
      vp: [vp.left, vp.top, vp.right, vp.bottom].map(Math.round), i: __app.play && __app.play.i,
      fx: fx && getComputedStyle(fx).display !== 'none' ? fx.children.length : 0,
      vcap: (e.querySelector('.vigcap, figcaption') || {}).textContent || '' }; });
  const hit = (a, c) => c && a[0] < c[2] && a[2] > c[0] && a[1] < c[3] && a[3] > c[1];
  const startAt = (p, y, r, i) => p.evaluate(async ([y, r, i]) => { __app.setVoice(false); if (__app.play) await __app.playStop(false);
    const st = (await (await fetch('data/stories/jews/story.json')).json()).stops.findIndex(s => s.year === y); await __app.go(st); await __app.playStart(r, i); }, [y, r, i]);
  const views = [['phone', 390, 844, true, false], ['desktop', 1280, 800, false, false], ['phone-reduced', 390, 844, true, true]];
  for (const [name, vw, vh, mobile, reduced] of views){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile, reducedMotion: reduced ? 'reduce' : 'no-preference'});
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.snd', 'off'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(600);
    let bad = 0, n = 0, fxSeen = 0;
    const list = reduced ? cases.filter(c => c.v.fx || c.v.images) : cases;
    for (const c of list){
      await startAt(p, c.y, c.reel, c.i);
      await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000}).catch(() => {});
      await p.waitForTimeout(500);
      const s = await V(p); n++;
      const pics = c.v.images || [c.v];
      const why = [];
      if (!s.shown || s.i !== c.i) why.push('not shown');
      if (s.ims.length !== pics.length || !s.ims.every((im, k) => im.loaded && im.src.endsWith(pics[k].src))) why.push('pictures ' + JSON.stringify(s.ims.map(x => x.src)));
      if (!(s.r[0] >= s.vp[0] && s.r[2] <= s.vp[2] && s.r[1] >= s.vp[1] && s.r[3] <= s.vp[3])) why.push('outside film ' + s.r);
      if (hit(s.r, s.cap)) why.push('over subtitles'); if (hit(s.r, s.cy)) why.push('over year');
      if (pics.length === 2){ const [a, z] = s.ims.map(x => x.r);
        if (!(a && z && z[0] >= a[2] - 1 && Math.abs(a[1] - z[1]) <= 2 && Math.abs(a[3] - z[3]) <= 2)) why.push('pair not side by side ' + JSON.stringify([a, z])); }
      if (s.ims.some(x => x.photo && x.anim !== 'none')) why.push('photo moves');
      const wantFx = !reduced && pics.some(x => x.fx && !x.photo);
      if (wantFx && !s.fx) why.push('no fx'); if (!wantFx && s.fx) why.push('fx where none expected');
      if (s.fx) fxSeen++;
      if (why.length){ bad++; ok(`${name} ${c.y} ${c.reel} ${c.i}: ${why.join('; ')}`, false); }
      // pair: tapping either picture enlarges the pair, side by side, top edge in place, with each picture's caption; Esc closes
      if (pics.length === 2 && !reduced){
        for (const k of [0, 1]){
          await p.evaluate(k => __app.playPause(true), k);
          const top0 = await p.evaluate(() => document.getElementById('vig').getBoundingClientRect().top);
          await p.locator('#vig img').nth(k).click(); await p.waitForTimeout(500);
          const z = await p.evaluate(() => { const e = document.getElementById('vig'); const vis = [...e.querySelectorAll('.vigin img')].filter(im => getComputedStyle(im).display !== 'none').map(im => im.getBoundingClientRect());
            return {zoom: e.classList.contains('zoom'), n: vis.length, side: vis.length === 2 && Math.abs(vis[0].top - vis[1].top) <= 1 && vis[0].right <= vis[1].left + 1, top: e.getBoundingClientRect().top, text: e.textContent}; });
          ok(`${name} pair (tap ${k + 1}) enlarges side by side, top kept (${top0 | 0} -> ${z.top | 0}), both captions`, z.zoom && z.side && Math.abs(z.top - top0) <= 2 && pics.every(q => !q.caption || z.text.includes(q.caption)));
          await p.keyboard.press('Escape'); await p.waitForTimeout(400);
          const u = await p.evaluate(() => { const e = document.getElementById('vig'); return {zoom: e.classList.contains('zoom'), n: [...e.querySelectorAll('img')].filter(im => getComputedStyle(im).display !== 'none').length, text: e.textContent}; });
          ok(`${name} pair closes back to both pictures and the pair caption`, !u.zoom && u.n === 2 && (!c.v.caption || u.text.includes(c.v.caption)));
          await p.evaluate(() => __app.playPause(false));
        }
      }
    }
    ok(`${name}: ${n - bad}/${n} vignettes in place` + (reduced ? ' (reduced motion, no fx overlay)' : `, fx overlays seen ${fxSeen}`), bad === 0);
    await ctx.close();
  }
  await b.close();
  for (const e of errs) notes.push('FAIL ' + e);
  console.log(notes.join('\n')); const f = notes.filter(x => x.startsWith('FAIL')).length;
  console.log(f ? 'FAILED ' + f : 'ALL PASS'); process.exit(f ? 1 : 0);
})();
