// The subtitle box and the sources popup. The source line sits inside the subtitle box at the bottom (no separate chip
// above it), the box keeps one height per chapter (tallest line + one spare line). A tap on the source line PAUSES the
// film at the exact spot and opens one shared popup ('Sources', that line's citations, optional description, links and
// pictures, scrolls). While it is open nothing moves on (no next line, no chapter end), and X, a tap outside or Esc
// closes it and the film plays on from the same spot if it was playing (stays paused if it was paused).
// Usage: node build/test-sourcepop.js [url] [shots-dir]
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8852/';
const shots = process.argv[3] || null;
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const b = await chromium.launch();
  for (const [name, vw, vh, mobile] of [['phone-360', 360, 740, true], ['phone-412', 412, 915, true], ['desktop', 1280, 800, false]]){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: shots ? 2 : 1, isMobile: mobile, hasTouch: mobile});
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.snd', 'off'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    // optional fields (description, links, images) are rendered when sources.json has them: add them to one source here
    await p.route('**/data/sources.json', async r => { const res = await r.fetch(); const j = await res.json();
      j.kitchen4 = Object.assign({}, j.kitchen4, {description: 'TEST description of the source.', links: [{url: 'https://example.org/a', label: 'TEST link'}],
        images: [{url: new URL('assets/og.jpg', url).href, credit: 'TEST credit', license: 'CC0'}]});
      await r.fulfill({response: res, json: j}); });
    const tap = async sel => { const r = await R(sel); const x = (r[0] + r[2]) / 2, y = (r[1] + r[3]) / 2; mobile ? await p.touchscreen.tap(x, y) : await p.mouse.click(x, y); };
    const tapAt = async (x, y) => mobile ? p.touchscreen.tap(x, y) : p.mouse.click(x, y);
    const R = sel => p.evaluate(s => { const e = document.querySelector(s); if (!e || !e.offsetHeight) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; }, sel);
    const st = () => p.evaluate(() => ({...__app.play, c: __app.clock, t: document.getElementById('captime').textContent, line: document.getElementById('captext').textContent, open: __app.srcIsOpen, cine: !!__app.cine, choice: !document.getElementById('choice').hidden, soon: !document.getElementById('soon').hidden}));
    const startAt = (y, r, i) => p.evaluate(async ([y, r, i]) => { __app.setVoice(false); if (__app.play) await __app.playStop(false); const st = (await (await fetch('data/stories/jews/story.json')).json()).stops.findIndex(s => s.year === y); await __app.go(st); await __app.playStart(r, i); }, [y, r, i]);
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(600);
      await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(300);
      await p.evaluate(() => document.getElementById('gostory').scrollIntoView({block: 'center'}));
      mobile ? await p.tap('#gostory') : await p.click('#gostory');
      await p.waitForFunction(() => __app.cine && __app.cine.full && document.getElementById('captext').offsetHeight > 0, null, {timeout: 8000});
      // 1) the box: source line inside, at the bottom; no chip above; one height for the chapter, one spare line
      await startAt(-1207, 'play', 6); await p.waitForTimeout(1200);
      const box = await R('#capbox'), tx = await R('#captext'), sr = await R('#capsrc');
      ok(name + ' source line is inside the subtitle box', box && sr && sr[1] >= box[1] && sr[3] <= box[3] + .5 && sr[0] >= box[0] && sr[2] <= box[2] + .5);
      ok(name + ' source line sits at the bottom of the box, below the text', sr && tx && sr[1] >= tx[3] - .5 && box[3] - sr[3] <= 10);
      ok(name + ' no separate source chip above the subtitles', await p.evaluate(() => document.getElementById('capmeta').closest('#capbox') !== null));
      ok(name + ' source line reads "Sources: …"', /^Sources: /.test(await p.textContent('#capsrc')));
      const vp = await R('#vp');
      ok(`${name} subtitle box at the bottom (${Math.round(vp[3] - box[3])} px)`, vp[3] - box[3] >= 4 && vp[3] - box[3] <= 16);
      const hs = [];
      for (const i of [2, 6, 10, 20, 34]){ await p.evaluate(i => { __app.seek(i); __app.playPause(true); }, i); await p.waitForTimeout(200); const r = await R('#capbox'); hs.push(Math.round(r[3] - r[1])); }
      ok(name + ' subtitle box keeps one height ' + JSON.stringify([...new Set(hs)]), Math.max(...hs) - Math.min(...hs) <= 1);
      const spare = await p.evaluate(() => { const lh = parseFloat(getComputedStyle(document.getElementById('captext')).lineHeight); const b = document.getElementById('capbox'), t = document.getElementById('captext'), m = document.getElementById('capmeta');
        return {lh, free: b.getBoundingClientRect().height - t.getBoundingClientRect().height - m.getBoundingClientRect().height}; });
      ok(`${name} at least one spare line in the box (${Math.round(spare.free)} px free, line ${spare.lh} px)`, spare.free >= spare.lh - 1);
      // 2) open while playing: pauses at the exact spot
      await startAt(-1207, 'play', 6); await p.waitForTimeout(2500);
      const s0 = await st();
      ok(name + ' playing before the tap', s0.paused === false);
      await tap('#capsrc'); await p.waitForTimeout(350);
      const s1 = await st();
      ok(name + ' tap on the source line opens the popup', s1.open && await p.isVisible('#srcwrap'));
      ok(name + ' popup heading "Sources"', (await p.textContent('#srch')).trim() === 'Sources');
      ok(name + ' story paused', s1.paused === true);
      ok(`${name} same spot after opening (line ${s0.i}→${s1.i}, ${s0.t}→${s1.t})`, s1.i === s0.i && s1.reel === s0.reel && s1.chapter === s0.chapter && s1.line === s0.line && s1.cine);
      const nk = await p.evaluate(() => { const b = document.getElementById('capsrc').dataset.k.split(' ').filter(Boolean); return {k: b.length, e: document.querySelectorAll('#srcbody .sre').length}; });
      ok(`${name} lists this line's sources (${nk.e} of ${nk.k})`, nk.k > 0 && nk.e === nk.k);
      // the X: 44px, 16px inside every edge, nothing overlaps it; the popup fits the screen
      const xb = await R('#srcx'), sb = await R('#srcbox'), hd = await p.evaluate(() => { const h = document.getElementById('srch'), rg = document.createRange(); rg.selectNodeContents(h); const r = rg.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom]; });
      ok(`${name} X is a 44px target (${Math.round(xb[2] - xb[0])}×${Math.round(xb[3] - xb[1])})`, xb[2] - xb[0] >= 43.5 && xb[3] - xb[1] >= 43.5);
      ok(`${name} X is 16px inside the edges (${Math.round(xb[0])}/${Math.round(xb[1])}/${Math.round(vw - xb[2])})`, xb[1] >= 16 && vw - xb[2] >= 16 && xb[0] >= 16);
      ok(name + ' heading and X do not overlap', hd[2] <= xb[0] || hd[3] <= xb[1]);
      ok(name + ' popup inside the screen', sb[0] >= 0 && sb[1] >= 0 && sb[2] <= vw && sb[3] <= vh);
      const top = await p.evaluate(([x, y]) => { const e = document.elementFromPoint(x, y); return e && e.id; }, [(xb[0] + xb[2]) / 2, (xb[1] + xb[3]) / 2]);
      ok(name + ' X is on top where it is tapped (' + top + ')', top === 'srcx');
      // 3) nothing moves on while it is open: 10 s, no next line, no chapter end
      await p.waitForTimeout(10000);
      const s2 = await st();
      ok(`${name} 10 s open: same line, time, clock and chapter (${s2.i}, ${s2.t}, clock ${Math.round(s1.c)}→${Math.round(s2.c)})`, s2.open && s2.paused && s2.i === s0.i && s2.t === s1.t && s2.c === s1.c && s2.chapter === s0.chapter && s2.line === s0.line);
      ok(name + ' 10 s open: no chapter end, choice or coming-soon', s2.cine && !s2.choice && !s2.soon && s2.n === s0.n);
      if (shots && name === 'phone-412') await p.screenshot({path: shots + '/sourcepop-412-popup.png'});
      // 4) X closes and the film plays on from the same spot
      await tap('#srcx'); await p.waitForTimeout(150);
      const s3 = await st();
      ok(`${name} X closes, film plays on from the same spot (line ${s3.i}, clock ${Math.round(s2.c)}→${Math.round(s3.c)} ms)`, !s3.open && s3.paused === false && s3.i === s0.i && s3.c >= s2.c && s3.c - s2.c < 600 && s3.line === s0.line);
      await p.waitForTimeout(1600);
      const s4 = await st();
      ok(`${name} the clock runs again (${s3.t} → ${s4.t})`, s4.t !== s3.t && s4.paused === false);
      // 5) a tap outside closes; Esc closes and does not leave the film
      await tap('#capsrc'); await p.waitForTimeout(300);
      await tapAt(Math.min(8, vw / 2), 8); await p.waitForTimeout(200);
      const s5 = await st();
      ok(name + ' tap outside closes and plays on', !s5.open && s5.paused === false && s5.cine);
      await tap('#capsrc'); await p.waitForTimeout(300);
      await p.keyboard.press('Escape'); await p.waitForTimeout(200);
      const s6 = await st();
      ok(name + ' Esc closes, the film stays and plays on', !s6.open && s6.cine && s6.paused === false && s6.i === s5.i);
      // 6) paused before: stays paused after
      await p.evaluate(() => __app.playPause(true));
      await tap('#capsrc'); await p.waitForTimeout(300); await tap('#srcx'); await p.waitForTimeout(300);
      ok(name + ' paused before: still paused after closing', (await st()).paused === true && !(await st()).open);
      // 7) long lists scroll; optional description, links and pictures show
      await p.evaluate(async () => { const j = await (await fetch('data/sources.json')).json(); __app.srcOpen(['kitchen4', ...Object.keys(j)]); }); await p.waitForTimeout(400);
      const sc = await p.evaluate(() => { const e = document.getElementById('srcbody'); const h = e.scrollHeight, c = e.clientHeight; e.scrollTop = 400; return {h, c, t: e.scrollTop, ov: getComputedStyle(e).overflowY}; });
      ok(`${name} long list scrolls (${sc.h} > ${sc.c}, scrolled ${sc.t})`, sc.h > sc.c && sc.t > 0 && sc.ov === 'auto');
      const sb2 = await R('#srcbox'), xb2 = await R('#srcx');
      ok(name + ' long list: popup still inside the screen, X still 16px inside', sb2[1] >= 0 && sb2[3] <= vh && xb2[1] >= 16 && vw - xb2[2] >= 16);
      if (mobile){ await p.evaluate(() => { document.getElementById('srcbody').scrollTop = 0; }); const r = await R('#srcbody');
        await p.touchscreen.tap((r[0] + r[2]) / 2, r[3] - 30); }   // a tap inside the page does not close it
      ok(name + ' a tap inside the popup does not close it', await p.evaluate(() => __app.srcIsOpen));
      const opt = await p.evaluate(() => { const e = document.querySelector('#srcbody .sre[data-k="kitchen4"]'); return e && {d: !!e.querySelector('.srd'), a: [...e.querySelectorAll('a')].map(a => a.textContent + '|' + a.target + '|' + a.rel), f: e.querySelector('figcaption') && e.querySelector('figcaption').textContent}; });
      ok(name + ' optional description, links and picture credit render ' + JSON.stringify(opt), opt && opt.d && opt.a.some(x => /TEST link/.test(x) && /_blank/.test(x) && /noopener/.test(x)) && /TEST credit/.test(opt.f) && /CC0/.test(opt.f));
      await p.evaluate(() => __app.srcClose());
      if (shots && name === 'phone-412'){ await startAt(-1207, 'play', 6); await p.waitForTimeout(1500); await p.evaluate(() => __app.playPause(true)); await p.waitForTimeout(200); await p.screenshot({path: shots + '/sourcepop-412-box.png'}); }
    } catch(e){ errs.push(name + ': ' + e.message); }
    await ctx.close();
  }
  await b.close();
  for (const n of notes) console.log(n); for (const e of errs) console.log('ERROR ' + e);
  const f = notes.filter(n => n.startsWith('FAIL')).length + errs.length;
  console.log(f ? 'FAILED ' + f : 'ALL PASS ' + notes.filter(n => n.startsWith('PASS')).length); process.exit(f ? 1 : 0);
})();
