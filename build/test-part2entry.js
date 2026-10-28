// Parts: every built stop is a part of the book (Part 1 = 1207 BC, Part 2 = c. 1150 BC). The intro step lists
// them right under the title, so Part 2 can be started directly. Checks: the list is there and near the top,
// a tap on Part 2 opens c. 1150 BC and starts its opening film (with its own recordings and year), a tap on the
// picture only shows the controls, the part is remembered as watched, and once Part 1 is watched Part 2 says
// "Continue". "You are here" does nothing.
// Usage: node build/test-part2entry.js [url] [noshots]; SHOTS=dir for part2_*.png screenshots.
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
(async () => {
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  for (const [name, vw, vh, mobile] of [['mobile', 390, 844, true], ['desktop', 1280, 800, false]]) {
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 2, isMobile: mobile, hasTouch: mobile});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage();
    try {
      p.on('console', m => { if (m.type() === 'error') errs.push(name + ': ' + m.text()); });
      p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
      const tap = async sel => { await p.evaluate(s => document.querySelector(s).scrollIntoView({block: 'center'}), sel); mobile ? await p.tap(sel) : await p.click(sel); };
      const shot = async n => { if (shots) await p.screenshot({path: D + '/part2_' + n + (mobile ? '' : '_desktop') + '.png'}); };
      const list = () => p.evaluate(() => [...document.querySelectorAll('#evbody .parts .chb')].map(x => ({k: +x.dataset.part, t: x.textContent, here: x.classList.contains('here'), go: x.classList.contains('gonext')})));
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1200);
      let l = await list();
      ok(name + ' 1207 intro lists Part 1 (here) and Part 2 ' + JSON.stringify(l.map(x => x.t)), l.length === 2 && l[0].here && /Part 1.*1207/.test(l[0].t) && /Part 2.*1150.*Start/.test(l[1].t) && !l[1].go);
      const pos = await p.evaluate(() => { const ev = document.getElementById('evbody'), h2 = ev.querySelector('h2'), pt = ev.querySelector('.parts'), cta = document.getElementById('gostory');
        return {afterTitle: h2.compareDocumentPosition(pt) & 4, beforeCta: pt.compareDocumentPosition(cta) & 4, off: pt.getBoundingClientRect().top - ev.getBoundingClientRect().top}; });
      ok(name + ' parts sit under the title, before the opening button ' + JSON.stringify(pos), pos.afterTitle && pos.beforeCta && pos.off < 160);
      await p.evaluate(() => document.querySelector('.parts').scrollIntoView({block: 'center'})); await p.waitForTimeout(300); await shot('list');
      await tap('#evbody .parts .chb.here'); await p.waitForTimeout(600);
      ok(name + ' "You are here" does nothing', await p.evaluate(() => !__app.play && __app.cur === 0));
      await tap('#evbody .parts .chb[data-part="1"]');
      await p.waitForFunction(() => __app.play && __app.play.reel === 'intro', null, {timeout: 15000}); await p.waitForTimeout(2500);
      let s = await p.evaluate(() => ({cur: __app.cur, play: __app.play, cine: __app.cine, src: __app.voice.src, year: document.getElementById('cyear').textContent, chapter: document.getElementById('chapter').textContent}));
      ok(name + ' Part 2 starts the c. 1150 BC opening film ' + JSON.stringify(s), s.cur === 1 && s.play.n === 7 && !s.play.paused && s.cine && s.cine.full && /1150/.test(s.year) && /Villages/.test(s.chapter) && (!s.src || /jews-1150-in-0/.test(s.src)));
      await shot('playing');
      const vb = await p.evaluate(() => { const r = document.getElementById('vp').getBoundingClientRect(); return {x: r.left + r.width / 2, y: r.top + r.height * 0.4}; });
      mobile ? await p.touchscreen.tap(vb.x, vb.y) : await p.mouse.click(vb.x, vb.y); await p.waitForTimeout(500);
      ok(name + ' tap on the picture does not pause', await p.evaluate(() => __app.play && __app.play.paused === false));
      // to the opener's end: its choice marks Part 2 as watched, and Continue goes on into Play
      await p.evaluate(() => __app.seek(6));
      await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 40000});
      ok(name + ' Part 2 remembered as watched at its choice', await p.evaluate(() => localStorage.getItem('tlm.done.jews.-1150') === '1'));
      await tap('#choicego'); await p.waitForTimeout(1200);
      s = await p.evaluate(() => __app.play);
      ok(name + ' Continue goes on into the c. 1150 to c. 1000 BC Play ' + JSON.stringify(s), s && s.reel === 'play' && s.n === 52);
      await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1500);
      await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(400);
      l = await list();
      ok(name + ' 1150 intro lists Part 1 to go back, Part 2 here ' + JSON.stringify(l.map(x => x.t)), l.length === 2 && l[1].here && /Part 1.*Start/.test(l[0].t));
      // a fresh visit after Part 1 was watched: Part 2 says Continue
      await p.evaluate(() => { localStorage.setItem('tlm.done.jews.-1207', '1'); });
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1200);
      l = await list();
      ok(name + ' after Part 1, Part 2 is highlighted "Continue" ' + JSON.stringify(l.map(x => x.t)), l[1].go && /Continue/.test(l[1].t));
      await p.evaluate(() => document.querySelector('.parts').scrollIntoView({block: 'center'})); await p.waitForTimeout(300); await shot('continue');
      // Part 1's opener run to its end marks Part 1 as watched
      await p.evaluate(() => { localStorage.removeItem('tlm.done.jews.-1207'); });
      await tap('#gostory'); await p.waitForFunction(() => __app.play && __app.play.reel === 'intro', null, {timeout: 15000});
      const n = await p.evaluate(() => __app.play.n); await p.evaluate(n => __app.seek(n - 1), n);
      for (let i = 0; i < 80 && await p.evaluate(() => !!__app.play); i++){ if (await p.evaluate(() => __app.play && __app.play.choice)) await tap('#choicego'); await p.waitForTimeout(500); }
      ok(name + ' Part 1 opener to the end marks Part 1 watched', await p.evaluate(() => !__app.play && localStorage.getItem('tlm.done.jews.-1207') === '1'));
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
