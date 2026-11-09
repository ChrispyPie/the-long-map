// Quick version of Chapter 1 (reel jews-1207-quick, STOP.quick): the whole chapter in about two minutes.
// Data: every line recorded, sourced and labelled, ~250-320 words, vignettes reuse Chapter 1 pictures, and the reel
// ends on the same map as Play. Browser (390x844 touch, and 1280x800): Play Chapter 1 asks Quick or Full first
// (✕ / Esc cancel), Quick runs the quick reel with its own line markers (#q1) and links, a short tap on the map
// never pauses, the sources popup pauses and resumes, the reel runs to the end and lands on Chapter 2 ("Continue to
// Chapter 2") with Chapter 1 watched; Full still starts the opening film; Chapter 2 has no chooser; the book's
// Play chapter asks too; ?ch=1&quick=1 and ?ch=1&line=q5 open the quick version.
// Usage: node build/test-quick.js [url] [noshots]; SHOTS=dir for screenshots (default /workspace).
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || '/workspace';
const ROOT = path.join(__dirname, '..');
(async () => {
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const J = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
  const data = J('data/stories/jews/1207bc.json'), S = J('data/sources.json');
  const Q = (data.quick || {}).beats || [];
  const cap = b => b.steps.find(x => x.type === 'caption');
  ok('quick reel exists: ' + Q.length + ' lines', Q.length >= 12 && Q.length <= 22);
  const words = Q.reduce((s, b) => s + cap(b).text.split(/\s+/).length, 0);
  ok('about two minutes of words (' + words + ')', words >= 240 && words <= 330 && data.quick.words === words);
  const ms = Q.reduce((s, b) => s + b.audioMs + b.pauseAfter, 0);
  ok('voice length ' + Math.round(ms / 1000) + ' s', ms > 100000 && ms < 190000);
  ok('every line has its recording', Q.every((b, i) => b.audio === `assets/narration/jews-1207-quick-${String(i + 1).padStart(2, '0')}.mp3` && fs.existsSync(path.join(ROOT, b.audio)) && b.audioMs > 1500));
  ok('every factual line sourced and labelled', Q.every(b => { const c = cap(b); return c.cert === 'frame' ? !c.src.length : c.cert === 'scene' ? !c.src.length && /^Imagine/.test(c.text) : ['attested', 'disputed', 'tradition'].includes(c.cert) && c.src.length && c.src.every(k => S[k]) && c.claims.every(x => x[2].every(k => S[k])); }));
  ok('spoken text has no digits or brackets', Q.every(b => !/[()\d]/.test(cap(b).text)));
  ok('tradition lines are told as tradition', Q.filter(b => cap(b).cert === 'tradition').every(b => /tradition/i.test(cap(b).text) && cap(b).src.includes('bible')));
  ok('no "myth" or "fabricated"', Q.every(b => !/\bmyth|fabricat/i.test(cap(b).text)));
  ok('Exodus memory, stele, Sea Peoples and villages all present', ['Exodus', 'Israel is laid waste', 'Sea Peoples', 'villages'].every(w => Q.some(b => cap(b).text.includes(w))));
  const vig = Q.filter(b => b.vignette);
  ok('vignettes on ' + vig.length + ' lines, all existing Chapter 1 pictures', vig.length >= 8 && vig.every(b => /images\/vignettes\/c1-/.test(b.vignette.src) && fs.existsSync(path.join(ROOT, b.vignette.src))));
  const borders = r => { const out = {add: [], fade: []}; r.forEach(b => b.steps.forEach(x => { if (x.type === 'border'){ (x.add || []).forEach(a => out.add.push(a.zone)); (x.fade || []).forEach(f => out.fade.push(f.zone + (f.certainty || ''))); } })); return JSON.stringify([out.add.sort(), out.fade.sort()]); };
  ok('ends on the same map as Play ' + borders(Q), borders(Q) === borders(data.play.beats));
  ok('uses battle, migration and border steps', ['battle', 'migration', 'border', 'focus'].every(t => Q.some(b => b.steps.some(x => x.type === t))));

  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  for (const dev of [{name: 'phone', vp: {width: 390, height: 844}, mob: true}, {name: 'desktop', vp: {width: 1280, height: 800}, mob: false}]){
    const ctx = await b.newContext({viewport: dev.vp, deviceScaleFactor: 2, isMobile: dev.mob, hasTouch: dev.mob});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage(), name = dev.name;
    const tap = async sel => dev.mob ? p.tap(sel) : p.click(sel);
    const req = new Set();
    p.on('request', r => { const m = r.url().match(/(jews-1207-quick-\d+)\.mp3/); if (m) req.add(m[1]); });
    p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location().url || '')) errs.push(name + ': ' + m.text()); });
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
      ok(name + ' starts on Chapter 1', await p.evaluate(() => __app.mode === 'stop' && __app.cur === 0));
      await tap('#gostory'); await p.waitForTimeout(600);
      let s = await p.evaluate(() => ({lp: __app.lenPick, play: __app.play, q: (document.getElementById('lpquick') || {}).textContent, f: (document.getElementById('lpfull') || {}).textContent}));
      ok(name + ' Play Chapter 1 asks Quick or Full first ' + JSON.stringify(s), s.lp && !s.play && /Quick/.test(s.q) && /Full/.test(s.f));
      if (shots && dev.mob) await p.screenshot({path: D + '/quick-ch1-chooser-phone.png'});
      if (shots && !dev.mob) await p.screenshot({path: D + '/quick-ch1-chooser-desktop.png'});
      await p.keyboard.press('Escape'); await p.waitForTimeout(300);
      ok(name + ' Esc cancels, no film', await p.evaluate(() => !__app.lenPick && !__app.play));
      await tap('#gostory'); await p.waitForTimeout(400); await tap('#lpx'); await p.waitForTimeout(300);
      ok(name + ' ✕ cancels, no film', await p.evaluate(() => !__app.lenPick && !__app.play));
      await tap('#gostory'); await p.waitForTimeout(400); await tap('#lpquick'); await p.waitForTimeout(2500);
      s = await p.evaluate(() => ({play: __app.play, voice: __app.voice, cine: __app.cine, ln: (document.querySelector('#captext .lnum') || {}).textContent, time: __app.time, card: document.getElementById('chapcard').textContent}));
      ok(name + ' Quick plays the quick reel full screen ' + JSON.stringify(s.play), s.play && s.play.reel === 'quick' && s.play.n === Q.length && s.cine && /jews-1207-quick-01/.test(s.voice.src || ''));
      s.ter = await p.evaluate(() => ({on: document.body.classList.contains('terrain'), imgs: [...document.querySelectorAll('image.relief')].filter(i => i.style.display !== 'none').length}));
      ok(name + ' terrain relief shows under the quick film ' + JSON.stringify(s.ter), s.ter.on && s.ter.imgs >= 1 || /terrain=0/.test(url));
      ok(name + ' line marker #q1, quick time ' + JSON.stringify([s.ln, s.time, s.card]), s.ln === '#q1' && /\/ [12]:\d\d$/.test(s.time) && /Quick version/.test(s.card));
      s = await p.evaluate(() => ({l: __app.lineRef('q3'), t: __app.timeRef()}));
      ok(name + ' links: ' + JSON.stringify(s), /\(quick\), line #q3/.test(s.l) && /\?ch=1&line=q3$/.test(s.l) && /\?ch=1&quick=1&t=\d+$/.test(s.t));
      // a short tap on the map shows the controls and never pauses
      await p.evaluate(() => __app.ctlHide());
      const vb = await p.evaluate(() => { const r = document.getElementById('vp').getBoundingClientRect(); return {x: r.left + r.width * 0.15, y: r.top + r.height * 0.45}; });
      if (dev.mob) await p.touchscreen.tap(vb.x, vb.y); else await p.mouse.click(vb.x, vb.y);
      await p.waitForTimeout(300);
      s = await p.evaluate(() => ({paused: __app.play.paused, idle: __app.cine.idle}));
      ok(name + ' tap on the map shows controls, keeps playing ' + JSON.stringify(s), !s.paused && !s.idle);
      // sources popup pauses and resumes at the same line
      await p.evaluate(() => __app.seek(3)); await p.waitForTimeout(1200);
      const i0 = await p.evaluate(() => __app.play.i);
      await tap('#capsrc'); await p.waitForTimeout(500);
      s = await p.evaluate(() => ({open: __app.srcIsOpen, paused: __app.play.paused, n: document.querySelectorAll('#srcbody .sre').length}));
      ok(name + ' sources popup pauses ' + JSON.stringify(s), s.open && s.paused && s.n >= 1);
      await tap('#srcx'); await p.waitForTimeout(400);
      s = await p.evaluate(() => ({open: __app.srcIsOpen, paused: __app.play && __app.play.paused, i: __app.play && __app.play.i, reel: __app.play && __app.play.reel}));
      ok(name + ' closing resumes the same film ' + JSON.stringify(s), !s.open && s.paused === false && s.reel === 'quick' && s.i === i0);
      if (shots && dev.mob){ await p.evaluate(() => __app.seek(11)); await p.waitForTimeout(6500); await p.evaluate(() => __app.wake()); await p.waitForTimeout(200); await p.screenshot({path: D + '/quick-ch1-film-phone.png'}); }
      await p.evaluate(() => __app.seek(0)); await p.waitForTimeout(300);
      await p.evaluate(() => { __app.speed = 8; });
      let maxI = 0, phil = false, isr = false;
      for (let i = 0; i < 400 && await p.evaluate(() => !!__app.play); i++){
        const t = await p.evaluate(() => ({i: __app.play ? __app.play.i : -1, ph: document.querySelectorAll('path.added.z-philistia').length, is: document.querySelectorAll('path.added.z-highlands').length}));
        maxI = Math.max(maxI, t.i); if (t.ph) phil = true; if (t.is) isr = true;
        await p.waitForTimeout(400);
      }
      ok(name + ' ran every line (last ' + maxI + ')', maxI === Q.length - 1);
      ok(name + ' Philistia and Israel drawn', phil && isr);
      const miss = Q.map((_, i) => 'jews-1207-quick-' + String(i + 1).padStart(2, '0')).filter(f => !req.has(f));
      ok(name + ' every quick recording requested, missing ' + JSON.stringify(miss), !miss.length);
      await p.waitForTimeout(3000);
      s = await p.evaluate(() => ({mode: __app.mode, cur: __app.cur, btn: (document.getElementById('gonextch') || {}).textContent, done: __app.parts()[0].done, pos: __app.pos(-1207)}));
      ok(name + ' ends on Chapter 2 with Continue, Chapter 1 watched ' + JSON.stringify(s), s.mode === 'stop' && s.cur === 1 && /Continue to Chapter 2/.test(s.btn || '') && s.done && !s.pos);
      // Chapter 2 has no quick version: it starts as before
      await tap('#gonextch'); await p.waitForTimeout(800);
      s = await p.evaluate(() => ({lp: __app.lenPick, play: __app.play}));
      ok(name + ' Continue to Chapter 2 asks Quick or Full too ' + JSON.stringify(s), s.lp && !s.play);
      await tap('#lpfull'); await p.waitForTimeout(1500);
      s = await p.evaluate(() => ({lp: __app.lenPick, play: __app.play}));
      ok(name + ' Chapter 2 Full starts its opening film ' + JSON.stringify(s), !s.lp && s.play && s.play.reel === 'intro');
      await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1500);
      // back to Chapter 1: Full starts the opening film as before
      await p.evaluate(() => __app.go(0)); await p.waitForTimeout(1500);
      await tap('#gostory'); await p.waitForTimeout(400); await tap('#lpfull'); await p.waitForTimeout(1500);
      s = await p.evaluate(() => __app.play);
      ok(name + ' Full starts the opening film ' + JSON.stringify(s), s && s.reel === 'intro' && s.n === data.transitionIn.beats.length);
      await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1500);
      // the book's Play chapter asks too
      await p.evaluate(() => __app.bookOpen(1)); await p.waitForTimeout(1800);
      await tap('#bkpage [data-act="play"]'); await p.waitForTimeout(700);
      s = await p.evaluate(() => ({lp: __app.lenPick, book: __app.book.open}));
      ok(name + ' book Play chapter asks Quick or Full ' + JSON.stringify(s), s.lp && !s.book);
      await tap('#lpquick'); await p.waitForTimeout(1500);
      s = await p.evaluate(() => __app.play);
      ok(name + ' book Quick plays the quick reel', s && s.reel === 'quick');
      await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1200);
    } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
    // deep links
    try {
      await p.goto(url + '?ch=1&quick=1', {waitUntil: 'networkidle'}); await p.waitForTimeout(1800);
      let s = await p.evaluate(() => ({deep: !document.getElementById('deep').hidden, txt: document.getElementById('deep').textContent, d: __app.deep, href: location.search}));
      ok(name + ' ?ch=1&quick=1 offers the quick version ' + JSON.stringify([s.d, s.href]), s.deep && /Quick version/.test(s.txt) && s.d && s.d.r === 'quick' && s.d.i === 0 && s.href === '');
      await tap('#deepgo'); await p.waitForTimeout(2000);
      s = await p.evaluate(() => __app.play);
      ok(name + ' deep link plays the quick reel ' + JSON.stringify(s), s && s.reel === 'quick' && s.i === 0);
      await p.goto(url + '?ch=1&line=q5', {waitUntil: 'networkidle'}); await p.waitForTimeout(1800);
      s = await p.evaluate(() => __app.deep);
      ok(name + ' ?ch=1&line=q5 opens quick line 5 ' + JSON.stringify(s), s && s.r === 'quick' && s.i === 4);
      await p.goto(url + '?ch=1&line=12', {waitUntil: 'networkidle'}); await p.waitForTimeout(1800);
      s = await p.evaluate(() => __app.deep);
      ok(name + ' old links unchanged (?ch=1&line=12 is Play) ' + JSON.stringify(s), s && s.r === 'play' && s.i === 11);
    } catch (e) { ok(name + ' deep links ran: ' + e.message.split('\n')[0], false); }
    await ctx.close();
  }
  // ---------- Chapter 2 (c. 1150 BC): quick version, chooser, deep link, and the terrain relief (Ch1 and Ch2 only) ----------
  const d2 = J('data/stories/jews/1150bc.json'), Q2 = (d2.quick || {}).beats || [], T = J('data/terrain.json');
  const w2 = Q2.reduce((s, b) => s + cap(b).text.split(/\s+/).length, 0), ms2 = Q2.reduce((s, b) => s + b.audioMs + b.pauseAfter, 0);
  ok('Ch2 quick reel: ' + Q2.length + ' lines, ' + w2 + ' words, voice ' + Math.round(ms2 / 1000) + ' s', Q2.length >= 12 && w2 >= 240 && w2 <= 330 && ms2 > 100000 && ms2 < 190000);
  ok('Ch2 every line recorded', Q2.every((b, i) => b.audio === `assets/narration/jews-1150-quick-${String(i + 1).padStart(2, '0')}.mp3` && fs.existsSync(path.join(ROOT, b.audio))));
  ok('Ch2 every factual line sourced and labelled', Q2.every(b => { const c = cap(b); return c.cert === 'frame' ? !c.src.length : ['attested', 'disputed', 'tradition'].includes(c.cert) && c.src.length && c.src.every(k => S[k]) && c.claims.every(x => x[2].every(k => S[k])) && (!c.ref || c.src.includes('bible')); }));
  ok('Ch2 no digits, no myth', Q2.every(b => !/[()\d]/.test(cap(b).text) && !/\bmyth|fabricat/i.test(cap(b).text)));
  ok('Ch2 no border for David (no border steps)', Q2.every(b => b.steps.every(x => x.type !== 'border')));
  ok('Ch2 vignettes are c2 pictures (' + Q2.filter(b => b.vignette).length + ')', Q2.filter(b => b.vignette).length >= 8 && Q2.filter(b => b.vignette).every(b => /c2-/.test(b.vignette.src) && fs.existsSync(path.join(ROOT, b.vignette.src))));
  ok('terrain stops are Ch1 and Ch2 ' + JSON.stringify(T.stops), JSON.stringify(T.stops) === '[-1207,-1150]');
  for (const dev of [{name: 'phone2', vp: {width: 390, height: 844}, mob: true}, {name: 'desktop2', vp: {width: 1280, height: 800}, mob: false}]){
    const ctx = await b.newContext({viewport: dev.vp, deviceScaleFactor: 2, isMobile: dev.mob, hasTouch: dev.mob});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage(), name = dev.name, tap = async sel => dev.mob ? p.tap(sel) : p.click(sel);
    p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location().url || '')) errs.push(name + ': ' + m.text()); });
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    const ter = () => p.evaluate(() => document.body.classList.contains('terrain') && [...document.querySelectorAll('image.relief')].some(i => i.style.display !== 'none'));
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1200);
      await p.evaluate(() => __app.go(1)); await p.waitForTimeout(1800);
      ok(name + ' Ch2 page shows the terrain', await ter());
      await tap('#gostory'); await p.waitForTimeout(500);
      ok(name + ' Ch2 Play asks Quick or Full', await p.evaluate(() => __app.lenPick && /Chapter 2/.test(document.getElementById('lenpick').textContent)));
      await tap('#lpquick'); await p.waitForTimeout(2200);
      let s = await p.evaluate(() => ({play: __app.play, ln: (document.querySelector('#captext .lnum') || {}).textContent, src: __app.voice.src}));
      ok(name + ' Ch2 quick plays ' + JSON.stringify([s.play, s.ln]), s.play && s.play.reel === 'quick' && s.play.n === 18 && s.ln === '#q1' && /jews-1150-quick-01/.test(s.src || ''));
      ok(name + ' terrain under the Ch2 quick film', await ter());
      if (shots && dev.mob){ await p.evaluate(() => __app.seek(13)); await p.waitForTimeout(7000); await p.evaluate(() => __app.wake()); await p.waitForTimeout(200); await p.screenshot({path: D + '/quick-ch2-film-phone.png'}); }
      await p.evaluate(() => __app.seek(0)); await p.evaluate(() => { __app.speed = 8; });
      let maxI = 0;
      for (let i = 0; i < 400 && await p.evaluate(() => !!__app.play); i++){ maxI = Math.max(maxI, await p.evaluate(() => __app.play ? __app.play.i : -1)); await p.waitForTimeout(400); }
      ok(name + ' Ch2 quick ran every line (' + maxI + ')', maxI === 17);
      await p.waitForTimeout(3000);
      s = await p.evaluate(() => ({cur: __app.cur, btn: (document.getElementById('gonextch') || {}).textContent, done: __app.parts()[1].done}));
      ok(name + ' Ch2 quick ends on Chapter 3 ' + JSON.stringify(s), s.cur === 2 && /Continue to Chapter 3/.test(s.btn || '') && s.done);
      for (const k of [2, 3, 4]){ await p.evaluate(k => __app.go(k), k); await p.waitForTimeout(1500); ok(name + ' no terrain on Chapter ' + (k + 1), !(await ter())); }
      await p.evaluate(() => __app.bookPlay(1, 'intro', 1)); await p.waitForTimeout(2000);
      ok(name + ' terrain under the Ch2 opening film', (await p.evaluate(() => __app.play && __app.play.reel === 'intro')) && await ter());
      await p.evaluate(() => __app.bookPlay(1, 'play', 5)); await p.waitForTimeout(2000);
      ok(name + ' terrain under the Ch2 Play', (await p.evaluate(() => __app.play && __app.play.reel === 'play')) && await ter());
      await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1200);
      await p.goto(url + '?ch=2&quick=1', {waitUntil: 'networkidle'}); await p.waitForTimeout(1800);
      s = await p.evaluate(() => ({d: __app.deep, txt: document.getElementById('deep').textContent}));
      ok(name + ' ?ch=2&quick=1 offers the Ch2 quick version ' + JSON.stringify(s.d), s.d && s.d.k === 1 && s.d.r === 'quick' && /Quick version/.test(s.txt));
      await tap('#deepgo'); await p.waitForTimeout(2000);
      ok(name + ' Ch2 deep link plays the quick reel', await p.evaluate(() => __app.play && __app.play.reel === 'quick' && __app.cur === 1));
    } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
    await ctx.close();
  }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  const f = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(f ? f + ' FAILED' : 'ALL PASS ' + notes.length);
  process.exit(f || errs.length ? 1 : 0);
})();
