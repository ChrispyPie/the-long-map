// The chapter flow (all chapters 1-6): chapter start → (Quick/Full card, recap) → opening film → Play, with no stop on
// the map in between; at the end of the chapter (Full and Quick) the choice 'Stay with the story' / 'Explore the map'.
// Explore = the map as the chapter left it (end-of-Play zones), the Explore checklist, and Continue to the next
// chapter (which opens the next chapter's Quick/Full card). Stay with the story opens that card directly; after
// Chapter 6 it goes to the 586 BC 'coming soon' page. The opening films have no choice and no 'explore' line.
// Usage: node build/test-chapterend.js [url] [noshots]; SHOTS=dir for screenshots (default /workspace).
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
  const cap = b => b.steps.find(x => x.type === 'caption');
  const YS = ['1207', '1150', '1000', '930', '722', '701'];
  for (const [n, y] of YS.map((y, i) => [i + 1, y])){
    const d = J(`data/stories/jews/${y}bc.json`), I = d.transitionIn.beats;
    ok(`Ch${n} opening film: no choice, no 'explore' or 'press Play' line`, I.every(b => !b.choice && !/explore|press play|stay with the story/i.test(cap(b).text)));
    ok(`Ch${n} opening film's last line is a lead-in, recorded`, /begin/.test(cap(I[I.length - 1]).text) && cap(I[I.length - 1]).cert === 'frame' && I[I.length - 1].audio);
  }
  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await ctx.addInitScript(() => (localStorage.setItem('tlm.notice.v1', 'seen'), localStorage.setItem('tlm.recaps', 'off')));
  const p = await ctx.newPage();
  p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location().url || '')) errs.push(m.text()); });
  p.on('pageerror', e => errs.push('pageerror: ' + e.message));
  const st = () => p.evaluate(() => ({reel: __app.play && __app.play.reel, i: __app.play && __app.play.i, n: __app.play && __app.play.n, ended: __app.ended, cur: __app.cur, mode: __app.mode, xend: __app.xend,
    choice: !document.getElementById('choice').hidden && document.getElementById('choice').textContent.replace(/\s+/g, ' ').trim(), lp: __app.lenPick}));
  const toEnd = async () => { await p.evaluate(() => { __app.speed = 8; __app.seek(__app.play.n - 1); }); for (let i = 0; i < 80 && !(await p.evaluate(() => __app.ended)); i++) await p.waitForTimeout(400); await p.waitForTimeout(600); };
  try {
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1200);
    for (let k = 0; k < 6; k++){
      const n = k + 1, quick = k === 1 || k === 3 || k === 5;
      await p.evaluate(k => __app.go(k), k); await p.waitForTimeout(1500);
      await p.tap('#gostory'); await p.waitForTimeout(400);
      ok(`Ch${n} Play Chapter asks Quick or Full`, await p.evaluate(() => __app.lenPick));
      await p.evaluate(() => { __app.speed = 1; }); await p.tap(quick ? '#lpquick' : '#lpfull'); await p.waitForTimeout(1500);
      let s = await st();
      ok(`Ch${n} ${quick ? 'quick' : 'full'} starts ${JSON.stringify([s.reel, s.i])}`, s.reel === (quick ? 'quick' : 'intro') && s.i <= 1);
      if (!quick){
        // the opening film runs straight on into Play
        await p.evaluate(() => { __app.speed = 8; __app.seek(__app.play.n - 1); });
        for (let i = 0; i < 60 && (await st()).reel === 'intro'; i++) await p.waitForTimeout(400);
        await p.waitForTimeout(1200); s = await st();
        ok(`Ch${n} opening film → Play directly ${JSON.stringify([s.reel, s.i, s.mode])}`, s.reel === 'play' && s.i <= 1 && !s.choice);
      }
      await toEnd(); s = await st();
      ok(`Ch${n} ends on the choice ${JSON.stringify(s.choice)}`, s.ended && /End of Chapter \d/.test(s.choice || '') && /Stay with the story/.test(s.choice) && /Explore the map/.test(s.choice) && s.cur === k);
      ok(`Ch${n} counted as watched`, await p.evaluate(k => __app.parts()[k].done, k));
      if (k === 2 && shots){ await p.waitForTimeout(800); await p.screenshot({path: `${D}/chapter-end-choice-phone.png`}); }
      if (k % 2 === 0){
        // Explore: the map as the chapter left it, the checklist, Continue → the next chapter's card
        const zonesEnd = await p.evaluate(() => [...document.querySelectorAll('.zlabel')].map(t => t.textContent).sort().join('|'));
        await p.tap('#choicemap'); await p.waitForTimeout(1800);
        s = await st();
        const z2 = await p.evaluate(() => [...document.querySelectorAll('.zlabel')].map(t => t.textContent).sort().join('|'));
        ok(`Ch${n} Explore keeps the end-of-chapter map ${JSON.stringify({xend: s.xend, film: s.reel})}`, !s.reel && s.xend === k && z2 === zonesEnd && s.mode === 'stop');
        ok(`Ch${n} Explore step: checklist and Continue`, await p.evaluate(n => /end of Chapter/.test(document.getElementById('evbody').textContent) && document.querySelectorAll('#evbody .checklist li').length > 3 && !!document.getElementById('xpnext') && (n < 6 ? /Continue to Chapter/ : /coming soon/).test(document.getElementById('xpnext').textContent), n));
        if (k === 0 && shots) await p.screenshot({path: `${D}/chapter-end-explore-phone.png`});
        await p.tap('#xpnext'); await p.waitForTimeout(700);
      } else {
        await p.tap('#choicego'); await p.waitForTimeout(700);
      }
      s = await st();
      if (n < 6){
        ok(`Ch${n} → Chapter ${n + 1}'s Quick/Full card`, s.lp && await p.evaluate(m => document.getElementById('lenpick').textContent.includes('Chapter ' + m) && !!document.getElementById('lprecap'), n + 1));
        if (n === 1){ await p.tap('#lpx'); await p.waitForTimeout(300); ok('✕ on the card keeps the page', !(await st()).lp); continue; }
        await p.tap('#lpfull'); await p.waitForTimeout(2200); s = await st();
        ok(`Ch${n} → Chapter ${n + 1} starts ${JSON.stringify([s.reel, s.cur])}`, s.reel === 'intro' && s.cur === k + 1);
        await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(1000);
      } else {
        await p.waitForTimeout(1500); s = await st();
        ok(`Ch6 → 586 BC coming soon ${JSON.stringify([s.mode, s.cur])}`, s.mode === 'soon' && !s.reel);
      }
    }
    // ✕ at the end choice explores too; deep link ?ch=3 opens the chapter page
    await p.evaluate(() => __app.go(0)); await p.waitForTimeout(1200);
    await p.evaluate(() => __app.bookPlay(0, 'play', 0)); await p.waitForTimeout(1500); await toEnd();
    await p.evaluate(() => { __app.wake(); document.getElementById('capx').click(); }); await p.waitForTimeout(1600);
    let s = await st(); ok(`✕ at the end → Explore ${JSON.stringify([s.xend, s.reel])}`, s.xend === 0 && !s.reel);
    await p.goto(url + '?ch=3', {waitUntil: 'networkidle'}); await p.waitForTimeout(1800);
    s = await st(); ok(`?ch=3 opens the chapter page ${JSON.stringify([s.cur, s.reel])}`, s.cur === 2 && !s.reel && await p.evaluate(() => /Play Chapter 3/.test(document.getElementById('gostory').textContent) && document.getElementById('deep').hidden));
  } catch (e) { ok('ran: ' + e.message.split('\n')[0], false); }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  const f = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(f ? f + ' FAILED' : 'ALL PASS ' + notes.length);
  process.exit(f || errs.length ? 1 : 0);
})();
