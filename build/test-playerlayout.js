// Player layout in the film: subtitles at the very bottom, no empty band reserved for the player; the controls
// are hidden at the start, a tap on the picture shows them above the subtitles, a second tap hides them, taps on
// the controls keep them up, and they hide by themselves after IDLE_MS. On a desktop a mouse move shows them and
// a click right after the move keeps them up. The map's focus sits in the middle of the free picture (below the
// year, above the subtitles), and vignette captions wrap instead of being cut off.
// Usage: node build/test-playerlayout.js [url]
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8852/';
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const b = await chromium.launch();
  for (const [name, vw, vh, mobile] of [['phone', 390, 844, true], ['phone-small', 360, 740, true], ['phone-412', 412, 915, true], ['desktop', 1280, 800, false]]){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile});
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.snd', 'off'); localStorage.setItem('tlm.review', '1'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    const tap = async (x, y) => mobile ? p.touchscreen.tap(x, y) : p.mouse.click(x, y);
    const R = sel => p.evaluate(s => { const e = document.querySelector(s); if (!e || !e.offsetHeight) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(Math.round); }, sel);
    const idle = () => p.evaluate(() => document.body.classList.contains('idle'));
    const startAt = (y, r, i) => p.evaluate(async ([y, r, i]) => { __app.setVoice(false); if (__app.play) await __app.playStop(false); const st = (await (await fetch('data/stories/jews/story.json')).json()).stops.findIndex(s => s.year === y); await __app.go(st); await __app.playStart(r, i); }, [y, r, i]);
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(600);
      await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(400);
      await p.evaluate(() => document.getElementById('gostory').scrollIntoView({block: 'center'}));
      mobile ? await p.tap('#gostory') : await p.click('#gostory');
      await p.waitForFunction(() => __app.cine && __app.cine.full && document.getElementById('captext').offsetHeight > 0, null, {timeout: 8000});
      await p.waitForTimeout(300);
      const vp = await R('#vp');
      ok(name + ' controls hidden at the start', (await idle()) && !(await R('#cap .crow')) && !(await R('#capbar')));
      ok(name + ' first-film hint shows', !!(await R('#ctlhint')));
      const ct = await R('#captext');
      ok(`${name} subtitles at the very bottom (${vp[3] - ct[3]} px from the edge)`, vp[3] - ct[3] <= 16 && vp[3] - ct[3] >= 4);
      const after = await p.evaluate(() => getComputedStyle(document.getElementById('vp'), '::after').height);
      ok(name + ' no band reserved at the bottom (' + after + ')', parseFloat(after) === 0 || after === 'auto');
      await p.waitForTimeout(1500);
      // one time counter (in the player) and one line marker (in the subtitle box): no extra 'Ch1 · #4 · 0:33' tag, review mode or not
      ok(name + ' no extra position tag above the subtitles (review mode on)', !(await p.evaluate(() => document.getElementById('revtag'))));
      ok(name + ' line marker sits inside the subtitle box', !!(await R('#captext .lnum')));
      const rt = null, cs = await R('#capsrc');
      if (cs) ok(name + ' source chip sits just above the subtitles', cs[3] <= ct[1] && ct[1] - cs[3] <= 30);
      const f = await p.evaluate(() => __app.filmFree()), cy = await R('#cyear');
      ok(`${name} free picture runs from the year (${f.top|0}) to the subtitles (${f.bot|0})`, f.top >= cy[3] - vp[1] && f.top <= cy[3] - vp[1] + 12 && Math.abs(f.bot - (Math.min(ct[1], cs ? cs[1] : 1e9, rt ? rt[1] : 1e9) - vp[1] - 6)) <= 2);
      ok(name + ' free picture is most of the screen (' + Math.round(100 * (f.bot - f.top) / vh) + '%)', (f.bot - f.top) / vh > 0.55);
      // a place in focus lands in the middle of the free picture
      await startAt(-1207, 'play', 6); await p.waitForTimeout(3600);
      const foc = await p.evaluate(() => { const k = document.querySelector('#map g.obj.hl circle'); if (!k) return null; const r = k.getBoundingClientRect(); return [(r.left + r.right) / 2, (r.top + r.bottom) / 2]; });
      const f2 = await p.evaluate(() => __app.filmFree()), vp2 = await R('#vp');
      if (foc) ok(`${name} focus point at y=${Math.round(foc[1] - vp2[1])}, middle of free picture ${Math.round(f2.cy)}`, Math.abs(foc[1] - vp2[1] - f2.cy) <= 30);
      else notes.push('INFO ' + name + ' no highlighted dot on this beat');
      if (!mobile){ await p.mouse.move(6, 6); await p.waitForTimeout(900); }
      await p.evaluate(() => __app.ctlHide());
      // a tap shows the controls above the subtitles
      // on the map, not on a picture card (a tap on that enlarges it instead)
      const vg = await R('#vig'), inV = ([x, y]) => vg && x >= vg[0] - 4 && x <= vg[2] + 4 && y >= vg[1] - 4 && y <= vg[3] + 4;
      // (the subtitle box keeps the height of the longest line, so the controls can sit higher: try spots above them first)
      const spot = [[.5, .35], [.5, .5], [.15, .5], [.85, .5], [.5, .2], [.5, .6], [.15, .6], [.85, .6]].map(([a, b]) => [vp2[0] + (vp2[2] - vp2[0]) * a, vp2[1] + (vp2[3] - vp2[1]) * b]).find(q => !inV(q));
      await tap(...spot); await p.waitForTimeout(350);
      const crow = await R('#cap .crow'), ct2 = await R('#captext');
      ok(name + ' tap shows the controls', !(await idle()) && !!crow);
      ok(name + ' controls sit above the subtitles, subtitles stay at the bottom', crow && ct2 && crow[3] <= ct2[1] && vp2[3] - ct2[3] <= 16);
      ok(name + ' tap does not pause', (await p.evaluate(() => __app.play && __app.play.paused)) === false);
      // the buttons: none overlaps another (Skip never covers the time), each is a 44px target on a phone, and the
      // close X sits at least 16px inside the screen edge (a phone case covers the edges)
      const bs = await p.evaluate(() => [...document.querySelectorAll('#cap .crow button')].filter(e => e.offsetWidth).map(e => { const r = e.getBoundingClientRect(); return {id: e.id, l: r.left, t: r.top, r: r.right, b: r.bottom}; }));
      const ov = []; for (let i = 0; i < bs.length; i++) for (let j = i + 1; j < bs.length; j++){ const a = bs[i], c = bs[j]; if (Math.min(a.r, c.r) - Math.max(a.l, c.l) > 0.5 && Math.min(a.b, c.b) - Math.max(a.t, c.t) > 0.5) ov.push(a.id + '/' + c.id); }
      ok(`${name} no two controls overlap (${bs.length} buttons${ov.length ? ': ' + ov.join(' ') : ''})`, bs.length >= 12 && !ov.length);
      const tm = bs.find(x => x.id === 'captime'), tw = await p.evaluate(() => { const e = document.getElementById('captime'); return e.scrollWidth - e.clientWidth; });
      ok(`${name} time counter is whole (${tm && Math.round(tm.r - tm.l)}px wide, ${tw}px cut)`, tm && tm.r - tm.l >= 60 && tw <= 0);
      const xb = bs.find(x => x.id === 'capx');
      ok(`${name} close X is inset from the edges (${Math.round(xb.l)} / ${Math.round(vw - xb.r)} px)`, xb.l >= 16 && vw - xb.r >= 16);
      ok(name + ' every control is inside the screen with 16px to spare', bs.every(x => x.l >= 16 && vw - x.r >= 16));
      if (mobile){
        const small = bs.filter(x => x.r - x.l < 43.5 || x.b - x.t < 43.5).map(x => x.id);
        ok(name + ' phone: every control is a 44px target' + (small.length ? ' (' + small.join(' ') + ')' : ''), !small.length);
        const rows = [...new Set(bs.map(x => Math.round(x.t)))];
        ok(`${name} phone: the buttons sit in 2 rows under the scene strip (${rows.length})`, rows.length === 2 && bs.find(x => x.id === 'capskip').t > tm.b - 1 && Math.abs(xb.t - bs.find(x => x.id === 'capskip').t) < 1);
        await p.screenshot({path: `/tmp/pl-${name}-controls.png`});
      } else ok(name + ' wide screen: one row of buttons', new Set(bs.map(x => Math.round(x.t))).size === 1);
      const sp = await R('#capspd'); await tap((sp[0] + sp[2]) / 2, (sp[1] + sp[3]) / 2); await p.waitForTimeout(250);
      ok(name + ' a tap on a control keeps them up', !(await idle()));
      await p.evaluate(() => { __app.speed = 1; });
      if (!mobile){ await p.mouse.move(...spot); await p.waitForTimeout(900); }
      await tap(...spot); await p.waitForTimeout(250);
      ok(name + ' second tap hides them at once', await idle());
      if (!mobile){
        await p.mouse.move(spot[0] + 40, spot[1] + 20); ok(name + ' mouse move shows the controls', !(await idle()));
        await p.mouse.click(spot[0] + 40, spot[1] + 20); await p.waitForTimeout(150); ok(name + ' click right after the move keeps them up', !(await idle()));
        await p.waitForTimeout(900); await p.mouse.click(spot[0] + 40, spot[1] + 20); await p.waitForTimeout(150); ok(name + ' a later click hides them', await idle());
      }
      await tap(...spot); await p.waitForTimeout(250);
      const IDLE = await p.evaluate(() => __app.IDLE_MS);
      await p.waitForTimeout(IDLE + 500);
      ok(name + ' controls hide by themselves after ' + IDLE + ' ms', await idle());
      await tap(...spot); await p.waitForTimeout(250);
      const pp = await R('#cappp'); await tap((pp[0] + pp[2]) / 2, (pp[1] + pp[3]) / 2); await p.waitForTimeout(IDLE + 500);
      ok(name + ' paused: controls stay up', !(await idle()) && (await p.evaluate(() => __app.play.paused)));
      await tap((pp[0] + pp[2]) / 2, (pp[1] + pp[3]) / 2); await p.waitForTimeout(200);
      await p.evaluate(() => __app.setCC(false)); await p.waitForTimeout(200);
      const f3 = await p.evaluate(() => __app.filmFree());
      ok(name + ' subtitles off: free picture grows (' + Math.round(f3.bot) + ')', f3.bot >= f2.bot && f3.bot >= f3.h - 60);
      await p.evaluate(() => __app.setCC(true));
      await startAt(-1207, 'play', 34);
      await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000}).catch(() => {});
      await p.waitForTimeout(700);
      const vc = await p.evaluate(() => { const fc = document.querySelector('#vig figcaption'); if (fc.hidden) return null; const s = getComputedStyle(fc); return {clip: fc.scrollHeight - fc.clientHeight, ws: s.whiteSpace, t: fc.textContent}; });
      if (vc) ok(name + ' vignette caption wraps, not cut off: ' + vc.t, vc.ws !== 'nowrap' && vc.clip <= 1);
      await p.screenshot({path: `/tmp/pl-${name}.png`});
    } catch(e){ errs.push(name + ': ' + e.message); }
    await ctx.close();
  }
  await b.close();
  for (const n of notes) console.log(n); for (const e of errs) console.log('ERROR ' + e);
  const f = notes.filter(n => n.startsWith('FAIL')).length + errs.length;
  console.log(f ? 'FAILED ' + f : 'ALL PASS ' + notes.filter(n => n.startsWith('PASS')).length); process.exit(f ? 1 : 0);
})();
