// The opener's choice ("The world is set. What next?") must be fully visible and tappable on every screen:
// both buttons inside the screen, not covered by the subtitle, chapter strip, controls, year or letterbox.
// Usage: node build/test-choice.js [url] [noshots]; TS=s|m|l|xl for a saved text size; SHOTS=dir for choice_<w>x<h>.png screenshots.
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
const VIEWS = [[360,640,1],[375,667,1],[390,844,1],[430,932,1],[458,1024,1],[640,360,1],[844,390,1],[932,430,1],[1280,800,0],[1920,1080,0]];
// ISRAEL (the people label) must sit inside the hill-country area, never out at sea
const israelCheck = p => p.evaluate(() => {
  const labs = [...document.querySelectorAll('#map text.zlabel')].filter(t => /^israel$/i.test(t.textContent.trim()) && getComputedStyle(t).display !== 'none' && +getComputedStyle(t).opacity > .3 && !t.classList.contains('gone'));
  const areas = [...document.querySelectorAll('#map path.israel')].filter(a => !a.classList.contains('gone'));
  return labs.map(t => { const q = t.getBoundingClientRect(), x = q.left + q.width / 2, y = q.top + q.height / 2;
    const inside = areas.some(a => { const m = a.getScreenCTM().inverse(), pt = a.ownerSVGElement.createSVGPoint(); pt.x = x; pt.y = y; return a.isPointInFill(pt.matrixTransform(m)); });
    return {at: [Math.round(x), Math.round(y)], inside}; });
});
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const b = await chromium.launch({args: ['--autoplay-policy=user-gesture-required']});
  for (const [vw, vh, mobile] of VIEWS){
    const name = vw + 'x' + vh;
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 2, isMobile: !!mobile, hasTouch: !!mobile});
    if (process.env.TS) await ctx.addInitScript(t => localStorage.setItem('tlm.textsize', t), process.env.TS); // TS=xl runs the suite at a saved text size
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.voice', 'off'); localStorage.setItem('tlm.snd', 'off'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    p.on('console', m => { if (m.type() === 'error') errs.push(name + ': ' + m.text()); });
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(800);
      await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(600);
      await p.evaluate(() => document.getElementById('gostory').scrollIntoView({block: 'center'}));
      mobile ? await p.tap('#gostory') : await p.click('#gostory');
      await p.waitForTimeout(1500);
      const iChoice = await p.evaluate(() => __app.chapters('intro')[0].end - 1);
      await p.evaluate(i => { __app.speed = 1.25; __app.seek(i); }, iChoice);
      await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 30000});
      await p.waitForTimeout(900);
      // wake the controls (the worst case: everything on screen at once)
      await p.mouse.move(vw / 2, vh / 3); await p.mouse.move(vw / 2 + 4, vh / 3 + 3); await p.waitForTimeout(500);
      const r = await p.evaluate(() => {
        const box = e => { const q = e.getBoundingClientRect(); return {l: q.left, t: q.top, r: q.right, b: q.bottom, w: q.width, h: q.height}; };
        const shown = e => { if (!e) return false; const cs = getComputedStyle(e); if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity < .05) return false; let a = e; while (a){ const c = getComputedStyle(a); if (c.display === 'none' || +c.opacity < .05) return false; a = a.parentElement; } const q = e.getBoundingClientRect(); return q.width > 0 && q.height > 0; };
        const vp = document.getElementById('vp'), vb = box(vp);
        const lb = parseFloat(getComputedStyle(vp, '::after').height) || 0;
        const others = ['#captext', '#capsrc', '.cap2 .bar', '#capch', '.cap2 .crow', '#cyear', '#chapcard']
          .map(s => [s, document.querySelector(s)]).filter(([, e]) => shown(e)).map(([s, e]) => [s, box(e)]);
        others.push(['letterbox top', {l: vb.l, r: vb.r, t: vb.t, b: vb.t + lb}], ['letterbox bottom', {l: vb.l, r: vb.r, t: vb.b - lb, b: vb.b}]);
        const out = {};
        for (const id of ['choicego', 'choicemap']){
          const e = document.getElementById(id), q = box(e);
          const hits = others.filter(([, o]) => q.l < o.r - .5 && q.r > o.l + .5 && q.t < o.b - .5 && q.b > o.t + .5).map(([s]) => s);
          const pts = [[.5, .5], [.1, .2], [.9, .2], [.1, .8], [.9, .8]].map(([fx, fy]) => { const x = q.l + q.w * fx, y = q.t + q.h * fy; const h = document.elementFromPoint(x, y); return !!h && (h === e || e.contains(h)); });
          out[id] = {box: [q.l, q.t, q.r, q.b].map(Math.round), inScreen: q.l >= 0 && q.t >= 0 && q.r <= innerWidth && q.b <= innerHeight, big: q.w >= 80 && q.h >= 44, hits, tappable: pts.every(Boolean)};
        }
        return out;
      });
      for (const id of ['choicego', 'choicemap']){
        const x = r[id];
        ok(name + ' ' + id + ' visible, not covered, tappable ' + JSON.stringify(x), x.inScreen && x.big && !x.hits.length && x.tappable);
      }
      const il = await israelCheck(p);
      ok(name + ' ISRAEL label inside the hill country (or hidden) ' + JSON.stringify(il), il.every(x => x.inside));
      if (shots) await p.screenshot({path: D + '/choice_' + name + '.png'});
      // after the choice the subtitles and controls come back
      mobile ? await p.tap('#choicego') : await p.click('#choicego'); await p.waitForTimeout(800);
      const after = await p.evaluate(() => ({choice: __app.play && __app.play.choice, i: __app.play && __app.play.i, choosing: document.body.classList.contains('choosing'), cap: getComputedStyle(document.getElementById('captext')).display}));
      ok(name + ' Continue works, subtitles back ' + JSON.stringify(after), after.choice === false && !after.choosing && after.cap !== 'none');
      // Play: the c. 1150 BC hill-country label (added by a border step)
      if (vw === 390 || vw === 1280 || vw === 844){
        await p.evaluate(() => __app.playStop && __app.playStop(false)); await p.waitForTimeout(800);
        await p.evaluate(() => __app.playStart('play', 0)); await p.waitForTimeout(2500);
        const ib = await p.evaluate(() => __app.chapters('play').length && 28);
        await p.evaluate(i => __app.seek(i + 1), ib); await p.waitForTimeout(4500);
        const il2 = await israelCheck(p);
        // the camera is close on Gibeah here, so the place labels may win the room and ISRAEL can be hidden
        ok(name + ' Play c. 1150 BC: ISRAEL label inside the hill country (or hidden) ' + JSON.stringify(il2), il2.every(x => x.inside));
        if (shots) await p.screenshot({path: D + '/israel_play_' + name + '.png'});
      }
    } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
    await ctx.close();
  }
  await b.close();
  notes.forEach(n => console.log(n));
  if (errs.length) console.log('ERRORS\n' + errs.join('\n'));
  const fail = notes.filter(n => n.startsWith('FAIL')).length + errs.length;
  console.log(fail ? 'FAILED ' + fail : 'ALL PASS ' + notes.length);
  process.exit(fail ? 1 : 0);
})();
