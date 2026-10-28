// Film mode, phone (390x844) and desktop:
// 1) with a picture card up, the camera's target and the highlighted places lie in the free picture BETWEEN the
//    card (above; on a wide screen: beside it) and the subtitles, never under the card;
// 2) taps on the card (enlarge, shrink, pair) never show or hide the player; only a SHORT tap on the map does.
//    A long press, a drag (pan) or a pinch of the map leaves the player as it is.
// Usage: node build/test-focus-tap.js [url]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8941/';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const J = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
  // vignette beats that move the camera to highlighted places: about 6 per chapter, spread out, plus the Tel Dan pair
  const cases = [];
  for (const [y, f] of [[-1207, '1207bc'], [-1150, '1150bc'], [-1000, '1000bc']]){
    const bs = J('data/stories/jews/' + f + '.json').play.beats;
    const vb = bs.map((b, i) => [i, b]).filter(([, b]) => b.vignette && b.steps.some(x => x.type === 'focus' && (x.hl || []).length));
    const step = Math.max(1, Math.floor(vb.length / 6));
    vb.forEach(([i, b], k) => { if (k % step === 0 || b.vignette.images) cases.push([y, i]); });
  }
  const pairCase = cases.find(([y, i]) => { const f = {'-1207': '1207bc', '-1150': '1150bc', '-1000': '1000bc'}[y]; return J('data/stories/jews/' + f + '.json').play.beats[i].vignette.images; });
  if (process.env.TAPS_ONLY) cases.length = 0;
  const b = await chromium.launch();
  const startAt = (p, y, r, i) => p.evaluate(async ([y, r, i]) => { __app.setVoice(false); if (__app.play) await __app.playStop(false);
    const st = (await (await fetch('data/stories/jews/story.json')).json()).stops.findIndex(s => s.year === y); await __app.go(st); await __app.playStart(r, i); }, [y, r, i]);
  const box = (p, sel) => p.evaluate(s => { const e = document.querySelector(s); if (!e || !e.offsetHeight) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(Math.round); }, sel);
  const idle = p => p.evaluate(() => document.body.classList.contains('idle'));
  const inside = (pt, r, m = 0) => r && pt[0] > r[0] - m && pt[0] < r[2] + m && pt[1] > r[1] - m && pt[1] < r[3] + m;
  for (const [name, vw, vh, mobile] of [['phone', 390, 844, true], ['desktop', 1280, 800, false]]){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile});
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.snd', 'off'); localStorage.setItem('tlm.ctlhint', '9'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    const cdp = mobile ? await ctx.newCDPSession(p) : null;
    const touch = (type, pts) => cdp.send('Input.dispatchTouchEvent', {type, touchPoints: pts.map(([x, y], id) => ({x, y, id}))});
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(600);
      // 1) the place in focus sits beside the card
      let bad = 0;
      for (const [y, i] of cases){
        await startAt(p, y, 'play', i);
        await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000}).catch(() => {});
        await p.waitForTimeout(1600);   // the camera has landed
        const v = await box(p, '#vig'), sub = await box(p, '#captext'), vp = await box(p, '#vp');
        const s = await p.evaluate(() => ({t: __app.camTarget(), slot: __app.vigSlot(), i: __app.play && __app.play.i,
          hl: [...document.querySelectorAll('#map g.obj.hl circle.hit, #map g.obj.hl circle')].map(c => { const r = c.getBoundingClientRect(); return [(r.left + r.right) / 2, (r.top + r.bottom) / 2]; }).filter((q, k, a) => a.findIndex(z => Math.abs(z[0] - q[0]) < 2 && Math.abs(z[1] - q[1]) < 2) === k) }));
        const why = [];
        if (!v || s.i !== i) why.push('no card'); else {
          const t = s.t, side = s.slot && s.slot.side;
          if (!t) why.push('no camera target');
          else if (side === 'a'){ const mid = (v[3] + sub[1]) / 2;
            if (!(t[1] > v[3] && t[1] < sub[1])) why.push(`target y ${t[1] | 0} not between card bottom ${v[3]} and subtitles ${sub[1]}`);
            else if (Math.abs(t[1] - mid) > 12) why.push(`target y ${t[1] | 0} not centred (${mid | 0})`); }
          else if (side === 'r'){ if (!(t[0] < v[0] && t[1] < sub[1])) why.push(`target ${t.map(Math.round)} not left of the card ${v[0]}`); }
          else why.push('no room reserved for the card');
          for (const q of s.hl) if (inside(q, v, 4)) why.push(`highlighted place ${q.map(Math.round)} under the card ${v}`);
        }
        if (why.length){ bad++; ok(`${name} ${y} play ${i}: ${why.join('; ')}`, false); }
      }
      ok(`${name}: the place in focus is beside the card, never under it (${cases.length - bad}/${cases.length} beats)`, bad === 0);
      // 1b) the enlarged picture keeps the small card's top edge and grows down from it; a pair stays side by side;
      //     it stays on the screen and the map does not move
      for (const [y, i] of [[-1207, 34], pairCase].filter(Boolean)){
        await startAt(p, y, 'play', i);
        await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000});
        await p.waitForTimeout(1600);
        const v0 = await box(p, '#vig'), t0 = await p.evaluate(() => __app.camTarget());
        await p.evaluate(() => __app.vigZoom(true, 0)); await p.waitForTimeout(700);
        const v1 = await box(p, '#vig'), vp = await box(p, '#vp'), t1 = await p.evaluate(() => __app.camTarget());
        const imgs = await p.evaluate(() => [...document.querySelectorAll('#vig .vigin img')].filter(m => m.offsetWidth).map(m => { const r = m.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(Math.round); }));
        const pair = i !== 34;
        ok(`${name} ${y} play ${i}: enlarged top ${v1[1]} == small top ${v0[1]} (±2), bigger (${v0[2] - v0[0]}→${v1[2] - v1[0]} px wide), on screen`,
          Math.abs(v1[1] - v0[1]) <= 2 && v1[2] - v1[0] > v0[2] - v0[0] && v1[0] >= vp[0] && v1[2] <= vp[2] && v1[3] <= vp[3]);
        if (pair) ok(`${name} enlarged pair stays side by side (${imgs.length} pictures, tops ${imgs.map(r => r[1])})`, imgs.length === 2 && Math.abs(imgs[0][1] - imgs[1][1]) <= 1 && imgs[0][2] <= imgs[1][0] + 1);
        ok(`${name} ${y} play ${i}: enlarging does not move the map`, t0 && t1 && Math.hypot(t1[0] - t0[0], t1[1] - t0[1]) < 2);
        await p.evaluate(() => __app.vigZoom(false)); await p.waitForTimeout(700);
        const v2 = await box(p, '#vig');
        ok(`${name} ${y} play ${i}: shrinks back to where it was`, v2.every((q, k) => Math.abs(q - v0[k]) <= 2));
      }
      // 2) taps: the card never toggles the player; only a short tap on the map does
      await startAt(p, -1207, 'play', 34);
      await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000});
      await p.waitForTimeout(900); await p.evaluate(() => __app.ctlHide());
      const tapAt = async (x, y) => { if (mobile) await p.touchscreen.tap(x, y); else { await p.mouse.move(x, y); await p.mouse.down(); await p.mouse.up(); } await p.waitForTimeout(350); };
      const mid = r => [(r[0] + r[2]) / 2, (r[1] + r[3]) / 2];
      let v = await box(p, '#vig');
      await tapAt(...mid(v));
      let zoomed = await p.evaluate(() => document.getElementById('vig').classList.contains('zoom'));
      ok(`${name} tap on the picture enlarges it and leaves the player hidden`, zoomed && await idle(p));
      await tapAt(...mid(await box(p, '#vig')));
      zoomed = await p.evaluate(() => document.getElementById('vig').classList.contains('zoom'));
      ok(`${name} tap on the enlarged picture shrinks it and leaves the player hidden`, !zoomed && await idle(p));
      if (mobile){   // a real finger wobbles a few px during a tap: still only enlarges / shrinks the picture
        for (const want of [true, false]){ const c = mid(await box(p, '#vig'));
          await touch('touchStart', [c]); await touch('touchMove', [[c[0] + 3, c[1] + 2]]); await touch('touchMove', [[c[0] + 4, c[1] + 4]]); await touch('touchEnd', []); await p.waitForTimeout(350);
          zoomed = await p.evaluate(() => document.getElementById('vig').classList.contains('zoom'));
          ok(`${name} a wobbly finger tap on the picture ${want ? 'enlarges' : 'shrinks'} it and leaves the player hidden`, zoomed === want && await idle(p)); }
      }
      // a free spot on the map (in the free picture, off the card)
      const spot = await p.evaluate(() => { const f = __app.filmFree(), r = document.getElementById('vp').getBoundingClientRect(); return [r.left + (f.cx ?? r.width * .25), r.top + f.top + (f.bot - f.top) * .75]; });
      const spot2 = [spot[0] + 20, spot[1] - 30];
      // long press
      if (mobile){ await touch('touchStart', [spot]); await p.waitForTimeout(800); await touch('touchEnd', []); }
      else { await p.mouse.move(...spot); await p.evaluate(() => __app.ctlHide()); await p.mouse.down(); await p.waitForTimeout(800); await p.mouse.up(); }
      await p.waitForTimeout(350);
      ok(`${name} long press on the map leaves the player hidden`, await idle(p));
      // drag (pan)
      if (mobile){ await touch('touchStart', [spot]); for (let k = 1; k <= 6; k++){ await touch('touchMove', [[spot[0] + k * 12, spot[1] + k * 8]]); await p.waitForTimeout(16); } await touch('touchEnd', []); }
      else { await p.mouse.move(...spot); await p.evaluate(() => __app.ctlHide()); await p.mouse.down(); for (let k = 1; k <= 6; k++){ await p.mouse.move(spot[0] + k * 12, spot[1] + k * 8); await p.waitForTimeout(16); } await p.mouse.up(); }
      await p.waitForTimeout(350);
      ok(`${name} dragging the map leaves the player hidden`, await idle(p));
      if (mobile){   // pinch
        await touch('touchStart', [spot, spot2]); for (let k = 1; k <= 5; k++){ await touch('touchMove', [[spot[0] - k * 8, spot[1] + k * 8], [spot2[0] + k * 8, spot2[1] - k * 8]]); await p.waitForTimeout(16); } await touch('touchEnd', []);
        await p.waitForTimeout(350); ok(`${name} pinching the map leaves the player hidden`, await idle(p));
        // a quick two-finger tap is not a tap either
        await touch('touchStart', [spot, spot2]); await p.waitForTimeout(60); await touch('touchEnd', []); await p.waitForTimeout(350);
        ok(`${name} a two-finger tap leaves the player hidden`, await idle(p));
      }
      // short tap on the map shows it, a second short tap hides it again
      if (!mobile){ await p.mouse.move(...spot); await p.evaluate(() => __app.ctlHide()); }
      await tapAt(...spot);
      ok(`${name} short tap on the map shows the player`, !(await idle(p)) && !!(await box(p, '#cap .crow')));
      // with the player up, a tap on the picture leaves it up (and only enlarges the picture)
      // (the card has a time of its own: start its beat again so it is surely up)
      await startAt(p, -1207, 'play', 34);
      await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000});
      await p.waitForTimeout(900);
      v = await box(p, '#vig');
      if (v){ await p.evaluate(() => __app.wake()); await tapAt(...mid(v)); ok(`${name} with the player up, a tap on the picture leaves it up`, !(await idle(p)) && await p.evaluate(() => document.getElementById('vig').classList.contains('zoom')));
        await tapAt(...mid(await box(p, '#vig'))); }
      // with the player up its panel covers the lower map: tap a spot that is map (svg), not card or controls
      const spot3 = await p.evaluate(() => { const r = document.getElementById('vp').getBoundingClientRect(), f = __app.filmFree();
        for (let fy = .3; fy < .95; fy += .05) for (const fx of [.5, .3, .7, .15, .85]){ const x = r.left + (f.left ?? 0) + ((f.right ?? r.width) - (f.left ?? 0)) * fx, y = r.top + f.top + (f.bot - f.top) * fy, e = document.elementFromPoint(x, y);
          if (e && e.closest('svg') && !e.closest('g.obj') && !e.closest('#vig')) return [x, y]; } return null; });
      if (!mobile) await p.mouse.move(...spot3);
      await tapAt(...spot3);
      ok(`${name} a second short tap on the map hides it`, await idle(p));
      const pl = await p.evaluate(() => __app.play);
      ok(`${name} the film kept playing throughout`, pl && !pl.paused);
    } catch(e){ errs.push(name + ': ' + e.message); }
    await ctx.close();
  }
  await b.close();
  for (const e of errs) notes.push('FAIL ' + e);
  console.log(notes.join('\n')); const f = notes.filter(x => x.startsWith('FAIL')).length;
  console.log(f ? 'FAILED ' + f : 'ALL PASS ' + notes.length); process.exit(f ? 1 : 0);
})();
