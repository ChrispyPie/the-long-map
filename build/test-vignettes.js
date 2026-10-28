// Vignettes (build/vignettes.py): data checks, then in the browser on a phone (390x844) and a desktop:
// the card comes in on its beat, sits beside the place in focus without covering it, the subtitles or
// the year, freezes with pause, re-places with the subtitle toggle, fades when the next beat moves the
// camera; a picture that fails to load is left out and the film goes on; reduced motion has no drift.
// Usage: node build/test-vignettes.js [url]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8852/';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const J = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
  const d1 = J('data/stories/jews/1207bc.json'), d2 = J('data/stories/jews/1150bc.json'), d3 = J('data/stories/jews/1000bc.json');
  const vs = (bs) => bs.map((b, i) => [i, b]).filter(([, b]) => b.vignette);
  const reels = {'1207 opener': d1.transitionIn.beats, '1207 play': d1.play.beats, '1150 opener': d2.transitionIn.beats, '1150 play': d2.play.beats, '1000 opener': d3.transitionIn.beats, '1000 play': d3.play.beats};
  let all = [];
  for (const [k, bs] of Object.entries(reels)) all = all.concat(vs(bs).flatMap(([i, b]) => (b.vignette.images || [b.vignette]).map(v => ({k, i, v}))));   // a pair counts as its two pictures
  ok('vignettes: ' + all.length + ' (' + Object.entries(reels).map(([k, bs]) => k + ' ' + vs(bs).length).join(', ') + ')', all.length >= 20);
  ok('every vignette has a small WebP and alt text', all.every(({v}) => /^images\/vignettes\/[a-z0-9-]+\.webp$/.test(v.src) && fs.existsSync(path.join(ROOT, v.src)) && fs.statSync(path.join(ROOT, v.src)).size < 150000 && v.alt && v.alt.length > 10));
  ok('no picture used twice', new Set(all.map(x => x.v.src)).size === all.length);
  ok('narration untouched: every beat still has its recording', Object.values(reels).every(bs => bs.every(b => b.audio && b.audioMs > 0)));
  const b = await chromium.launch();
  const V = p => p.evaluate(() => { const e = document.getElementById('vig'), r = e.getBoundingClientRect(), im = e.querySelector('img');
    const ct = document.getElementById('captext'), cr = ct.getBoundingClientRect(), cy = document.getElementById('cyear').getBoundingClientRect(), vp = document.getElementById('vp').getBoundingClientRect();
    return {shown: !e.hidden && e.classList.contains('in') && getComputedStyle(e).visibility !== 'hidden', hidden: e.hidden, src: im.getAttribute('src'), loaded: im.complete && im.naturalWidth > 0,
      r: [r.left, r.top, r.right, r.bottom].map(Math.round), cap: ct.offsetHeight ? [cr.left, cr.top, cr.right, cr.bottom].map(Math.round) : null, cy: [cy.left, cy.top, cy.right, cy.bottom].map(Math.round),
      vp: [vp.left, vp.top, vp.right, vp.bottom].map(Math.round), paused: e.classList.contains('paused'), photo: im.classList.contains('photo'), anim: getComputedStyle(im).animationName, play: getComputedStyle(im).animationPlayState,
      i: __app.play && __app.play.i }; });
  const hit = (a, c) => c && a[0] < c[2] && a[2] > c[0] && a[1] < c[3] && a[3] > c[1];
  const startAt = async (p, stopYear, reel, i) => {
    await p.evaluate(async ([y, r, i]) => { __app.setVoice(false); if (__app.play) await __app.playStop(false); const k = __app.parts ? null : null;
      const st = (await (await fetch('data/stories/jews/story.json')).json()).stops.findIndex(s => s.year === y); await __app.go(st); await __app.playStart(r, i); }, [stopYear, reel, i]);
  };
  for (const [name, vw, vh, mobile, reduced] of [['phone', 390, 844, true, false], ['desktop', 1280, 800, false, false], ['desktop-reduced', 1280, 800, false, true]]){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile, reducedMotion: reduced ? 'reduce' : 'no-preference'});
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.snd', 'off'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    await p.route(/images\/vignettes\/c1-terraces\.webp/, r => r.abort('failed'));   // one picture fails
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(600);
      const cases = reduced ? [[-1207, 'play', 34]] : [[-1207, 'intro', 14], [-1207, 'play', 34], [-1150, 'play', 2], [-1150, 'play', 50]];
      for (const [y, r, i] of cases){
        await startAt(p, y, r, i);
        await p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in'); }, null, {timeout: 8000}).catch(() => {});
        await p.waitForTimeout(800);
        const s = await V(p);
        const [cx, foc] = await p.evaluate(() => { const r = document.getElementById('vp').getBoundingClientRect(), f = __app.filmFree(); return [r.left + f.cx, r.top + f.cy]; });   // the middle of the free picture beside the card (js/app.js filmFree)
        const fbox = [cx - 14, foc - 14, cx + 14, foc + 14];
        ok(`${name} ${y} ${r} ${i}: card in, picture loaded ${s.src} ${JSON.stringify(s.r)}`, s.shown && s.loaded && s.i === i);
        ok(`${name} ${y} ${r} ${i}: inside the film, clear of the focus point, subtitles and year`, s.r[0] >= s.vp[0] && s.r[2] <= s.vp[2] && s.r[1] >= s.vp[1] && s.r[3] <= s.vp[3] && !hit(s.r, fbox) && !hit(s.r, s.cap) && !hit(s.r, s.cy) && (s.r[2] - s.r[0]) >= 130);
        if (reduced) ok(name + ' reduced motion: no Ken Burns drift (' + s.anim + ')', s.anim === 'none');
        else if (s.photo) ok(`${name} a museum-plate photo stays still (${s.anim})`, s.anim === 'none');
        else ok(`${name} Ken Burns runs (${s.anim})`, /^vigkb/.test(s.anim) && s.play === 'running');
      }
      if (!reduced){
        // pause freezes the drift, play resumes it; the card stays
        await p.evaluate(() => __app.playPause(true)); await p.waitForTimeout(300);
        let s = await V(p); ok(name + ' pause freezes the card', s.shown && s.paused && s.play === 'paused');
        await p.waitForTimeout(1500); const i0 = (await V(p)).i;
        await p.evaluate(() => __app.playPause(false)); await p.waitForTimeout(300);
        s = await V(p); ok(name + ' play resumes it, same beat', s.shown && !s.paused && s.play === 'running' && s.i === i0);
        // subtitles off and on: the card is re-placed and still clear of the subtitles
        await p.evaluate(() => __app.setCC(false)); await p.waitForTimeout(300); const off = await V(p);
        await p.evaluate(() => __app.setCC(true)); await p.waitForTimeout(300); const on = await V(p);
        ok(name + ' subtitle toggle keeps the card up and clear', off.shown && on.shown && !hit(on.r, on.cap));
        // the next beat that moves the camera fades it
        await startAt(p, -1207, 'play', 34);
        await p.waitForFunction(() => !document.getElementById('vig').hidden, null, {timeout: 8000}).catch(() => {});
        // a beat with no card of its own and none in the 3 lines before it
        const NOCARD = d1.play.beats.findIndex((x, k) => k > 0 && !d1.play.beats.slice(Math.max(0, k - 3), k + 1).some(y => y.vignette));
        const nextFocus = d1.play.beats.findIndex((x, k) => k > 34 && (x.vignette || x.steps.some(s => s.type === 'focus')));
        await p.evaluate(n => __app.seek(n), nextFocus); await p.waitForTimeout(150);
        await p.evaluate(n => __app.seek(n), NOCARD); await p.waitForTimeout(900);
        s = await V(p); ok(name + ' moving on to a beat without a card hides it', s.hidden);
        // the failed picture (c1-terraces, play 37): left out, the film goes on
        await startAt(p, -1207, 'play', 37); await p.waitForTimeout(3500);
        s = await V(p); const pl = await p.evaluate(() => __app.play);
        ok(name + ' a picture that fails is left out, the film goes on ' + JSON.stringify(pl), (s.hidden || !s.shown) && pl && !pl.paused && pl.i >= 37);
        // the natural run: card of play 33 (village ring) gives way to play 34's card
        await startAt(p, -1207, 'play', 33);
        await p.waitForFunction(() => __app.play && __app.play.i >= 34, null, {timeout: 20000}).catch(() => {});
        await p.waitForTimeout(2500); s = await V(p);
        ok(name + ' on its own the next card takes over: ' + s.src, s.shown && /c1-pillared-house/.test(s.src));
      }
      await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(900);
      ok(name + ' stopping the film removes the card', (await V(p)).hidden);
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
