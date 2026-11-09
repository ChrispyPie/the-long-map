// "The story so far" (STOP.recap, Chapters 2-5): data and browser checks.
// Data: Ch1 has none; Ch2-5 each have a recap that grows (about 20 s before Ch2 up to about a minute before Ch5),
// newly recorded (own files jews-<year>-recap-NN.mp3), every line labelled and sourced, tradition as tradition,
// no digits or brackets spoken, only map moves (no years, no borders). Browser (390x844 touch): with recaps on,
// Play Chapter 3 → Full plays the recap first (Skip recap button visible), then the opening film; Skip recap
// jumps to it; Quick also gets the recap; the settings switch turns recaps off; a previous chapter finished less
// than a day ago leaves it out, an older one brings it back; Continue to Chapter N (after finishing) skips it.
// Usage: node build/test-recap.js [url] [noshots]; SHOTS=dir for screenshots (default /workspace).
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
  const S = J('data/sources.json'), cap = b => b.steps.find(x => x.type === 'caption');
  ok('Chapter 1 has no recap', !J('data/stories/jews/1207bc.json').recap);
  let prev = 0;
  const lens = {};
  for (const [n, y] of [[2, '1150'], [3, '1000'], [4, '930'], [5, '722']]){
    const R = (J(`data/stories/jews/${y}bc.json`).recap || {}).beats || [];
    const ms = R.reduce((s, b) => s + b.audioMs + b.pauseAfter, 0); lens[n] = ms;
    ok(`Ch${n} recap: ${R.length} lines, ${Math.round(ms / 1000)} s of voice`, R.length >= 2 && ms > prev && ms > 14000 && ms < 80000); prev = ms;
    ok(`Ch${n} recap newly recorded`, R.every((b, i) => b.audio === `assets/narration/jews-${y}-recap-${String(i + 1).padStart(2, '0')}.mp3` && fs.existsSync(path.join(ROOT, b.audio)) && b.audioMs > 900));
    ok(`Ch${n} recap sourced and labelled`, R.every(b => { const c = cap(b); return c.cert === 'frame' ? !c.src.length : ['attested', 'disputed', 'tradition'].includes(c.cert) && c.src.length && c.src.every(k => S[k]) && c.claims.every(x => x[2].every(k => S[k])) && (c.cert !== 'tradition' || c.src.includes('bible')); }));
    ok(`Ch${n} recap: no digits spoken, no "myth"`, R.every(b => !/[()\d]/.test(cap(b).text) && !/\bmyth/i.test(cap(b).text)));
    ok(`Ch${n} recap: map moves only`, R.every(b => b.steps.every(x => ['focus', 'caption'].includes(x.type))));
  }
  ok('recaps grow: about 20 s before Ch2, about a minute before Ch5', lens[2] < 26000 && lens[5] > 45000);

  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
  const p = await ctx.newPage(), name = 'phone';
  p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location().url || '')) errs.push(m.text()); });
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  const st = () => p.evaluate(() => ({reel: __app.play && __app.play.reel, n: __app.play && __app.play.n, cur: __app.cur, skip: (() => { const e = document.getElementById('recapskip'); const r = e.getBoundingClientRect(); return getComputedStyle(e).display !== 'none' && r.width > 30 && r.top >= 0 && r.bottom <= innerHeight; })()}));
  const startCh = async (k, w) => { await p.evaluate(k => __app.go(k), k); await p.waitForTimeout(1500); await p.tap('#gostory'); await p.waitForTimeout(400); if (await p.evaluate(() => __app.lenPick)) await p.tap(w === 'quick' ? '#lpquick' : '#lpfull'); await p.waitForTimeout(1800); };
  const stop = async () => { await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1200); };
  try {
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1200);
    ok(`${name} recaps on by default`, await p.evaluate(() => __app.recaps));
    // Chapter 3, Full: recap first
    await startCh(2, 'full');
    let s = await st();
    ok(`${name} Ch3 Full starts with the story so far ${JSON.stringify(s)}`, s.reel === 'recap' && s.skip);
    ok(`${name} recap line marker #r1 and chapter card`, await p.evaluate(() => /#r1/.test(document.getElementById('captext').textContent) && /story so far/i.test(document.getElementById('chapcard').textContent)));
    await p.waitForTimeout(5500); await p.evaluate(() => __app.wake && __app.wake()); await p.waitForTimeout(200);
    if (shots) await p.screenshot({path: `${D}/recap-ch3-phone.png`});
    await p.tap('#recapskip'); await p.waitForTimeout(1800);
    s = await st();
    ok(`${name} Skip recap → the opening film ${JSON.stringify(s)}`, s.reel === 'intro' && !s.skip && s.cur === 2);
    await stop();
    // runs to its end on its own, then the opening film
    await startCh(1, 'full'); s = await st();
    ok(`${name} Ch2 recap ${JSON.stringify(s)}`, s.reel === 'recap' && s.n === 3);
    await p.evaluate(() => __app.seek(__app.play.n - 1)); 
    for (let i = 0; i < 60 && (await st()).reel === 'recap'; i++) await p.waitForTimeout(500);
    await p.waitForTimeout(1500); s = await st();
    ok(`${name} after the recap the opening film plays ${JSON.stringify(s)}`, s.reel === 'intro' && s.cur === 1);
    await stop();
    // Quick also gets it, then the quick reel
    await startCh(4, 'quick'); s = await st();
    ok(`${name} Ch5 Quick starts with the recap ${JSON.stringify(s)}`, s.reel === 'recap' && s.n === 9);
    await p.tap('#capskip').catch(async () => { await p.evaluate(() => document.getElementById('capskip').click()); });
    await p.waitForTimeout(1800); s = await st();
    ok(`${name} controls' Skip in the recap → the quick version ${JSON.stringify(s)}`, s.reel === 'quick');
    await stop();
    // the previous chapter finished less than a day ago: no recap; more than a day ago: recap again
    await p.evaluate(() => localStorage.setItem('tlm.doneat.jews.-930', String(Date.now() - 3600e3)));
    await startCh(4, 'full'); s = await st();
    ok(`${name} Ch4 finished an hour ago → Ch5 without recap ${JSON.stringify(s)}`, s.reel && s.reel !== 'recap');
    await stop();
    await p.evaluate(() => localStorage.setItem('tlm.doneat.jews.-930', String(Date.now() - 30 * 3600e3)));
    await startCh(4, 'full'); s = await st();
    ok(`${name} Ch4 finished yesterday → recap again ${JSON.stringify(s)}`, s.reel === 'recap');
    // the settings switch in the film turns recaps off (remembered)
    await p.evaluate(() => __app.wake && __app.wake()); await p.waitForTimeout(200);
    await p.evaluate(() => __app.capMenu(true)); await p.waitForTimeout(200);
    ok(`${name} settings show the recap switch, on`, await p.evaluate(() => { const c = document.querySelector('#capmenu input[data-recaps]'); return c && c.checked && c.offsetParent !== null; }));
    await p.click('#capmenu input[data-recaps]'); await p.waitForTimeout(200);
    ok(`${name} switch turns recaps off and remembers`, await p.evaluate(() => !__app.recaps && localStorage.getItem('tlm.recaps') === 'off'));
    await stop();
    await startCh(3, 'full'); s = await st();
    ok(`${name} recaps off → Ch4 starts on its opening film ${JSON.stringify(s)}`, s.reel === 'intro');
    await stop();
    await p.evaluate(() => __app.setRecaps(true));
    // finishing a chapter records the time; Continue to the next chapter then skips the recap
    await startCh(2, 'quick'); await p.tap('#recapskip'); await p.waitForTimeout(1500);
    await p.evaluate(() => { __app.speed = 8; __app.seek(__app.play.n - 1); });
    for (let i = 0; i < 80 && await p.evaluate(() => !!__app.play); i++) await p.waitForTimeout(500);
    await p.waitForTimeout(3000);
    ok(`${name} finishing Ch3 records when`, await p.evaluate(() => Date.now() - (+localStorage.getItem('tlm.doneat.jews.-1000') || 0) < 120e3));
    const btn = await p.$('#gonextch');
    if (btn){ await btn.tap(); await p.waitForTimeout(500); if (await p.evaluate(() => __app.lenPick)) await p.tap('#lpfull'); await p.waitForTimeout(1800); }
    s = await st();
    ok(`${name} Continue to Chapter 4 right after → no recap ${JSON.stringify(s)}`, !!btn && s.reel === 'intro' && s.cur === 3);
    await stop();
  } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  const f = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(f ? f + ' FAILED' : 'ALL PASS ' + notes.length);
  process.exit(f || errs.length ? 1 : 0);
})();
