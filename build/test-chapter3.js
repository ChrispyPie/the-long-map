// Chapter 3 (c. 1000 BC: David, Solomon and the split). Data: live stop, 7 opener + 61 Play lines, each with its
// recording, no digits or brackets in spoken text, every Bible ref cites the Bible, the Play runs to c. 930 BC and
// ends on the teaser for the next chapter. Browser (390x844): the opener and the whole Play run start to finish
// (speed 8, voice on), every line's recording is requested, the split draws Israel and Judah, and the end is the
// c. 930 BC intro (Chapter 4) with a 'Continue to Chapter 4' button.
// Usage: node build/test-chapter3.js [url] [noshots]; SHOTS=dir for ch3_*.png screenshots.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8863/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
const ROOT = path.join(__dirname, '..');
(async () => {
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const J = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
  const story = J('data/stories/jews/story.json'), data = J('data/stories/jews/1000bc.json');
  const IN = data.transitionIn.beats, PL = data.play.beats, all = IN.concat(PL);
  const caps = b => b.steps.filter(x => x.type === 'caption');
  const s1000 = story.stops.find(s => s.year === -1000), s930 = story.stops.find(s => s.year === -930);
  ok('1000 is a live stop with its own map', s1000 && s1000.file === 'data/stories/jews/1000bc.json' && s1000.era === 'data/eras/1000bc.json' && fs.existsSync(path.join(ROOT, s1000.era)));
  ok('930 is the next, live stop (Chapter 4)', s930 && s930.file === 'data/stories/jews/930bc.json' && !s930.soon && data.play.to === -930);
  ok('7 opener lines, 61 Play lines', IN.length === 7 && PL.length === 61);
  const sizes = all.map(b => b.audio && fs.existsSync(path.join(ROOT, b.audio)) ? fs.statSync(path.join(ROOT, b.audio)).size : -1);
  ok('every line has its recording (' + Math.round(sizes.reduce((a, s) => a + s, 0) / 1024) + ' kB)', sizes.every(s => s > 4000 && s < 80000));
  ok('audioMs measured for every line', all.every(b => b.audioMs > 2000 && b.audioMs < 20000));
  ok('spoken text has no digits or brackets', all.every(b => caps(b).every(c => !/[()\d]/.test(c.text))));
  ok('every Bible ref cites the Bible', all.every(b => caps(b).every(c => !c.ref || (c.src || []).includes('bible'))));
  ok('exactly one choice, at the end of the opener', IN.filter(b => b.choice).length === 1 && IN[IN.length - 1].choice && PL.every(b => !b.choice));
  ok('ends on the teaser for the next chapter', /next chapter begins\.$/.test(caps(PL[PL.length - 1])[0].text));
  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
  const p = await ctx.newPage();
  const name = 'mobile';
  try {
    const req = new Set();
    p.on('request', r => { const m = r.url().match(/(jews-1000-(in|play)-\d+)\.mp3/); if (m) req.add(m[1]); });
    p.on('console', m => { if (m.type() === 'error') errs.push(m.text()); });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    const shot = async n => { if (shots) await p.screenshot({path: D + '/ch3_' + n + '.png'}); };
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
    await p.evaluate(() => __app.go(2)); await p.waitForTimeout(1600);
    let s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, ammon: document.querySelectorAll('path.z-ammon').length, parts: __app.parts().length}));
    ok(name + ' timeline to c. 1000 BC: live stop, Chapter 3 ' + JSON.stringify(s), s.mode === 'stop' && /1000/.test(s.pill) && s.ammon >= 1 && s.parts === 5);
    await shot('intro');
    await p.tap('#gostory'); await p.waitForTimeout(2000);
    s = await p.evaluate(() => ({play: __app.play, voice: __app.voice}));
    ok(name + ' opener runs with voice ' + JSON.stringify(s.play), s.play && s.play.reel === 'intro' && s.play.n === 7 && /jews-1000-in-01/.test(s.voice.src || ''));
    await p.evaluate(() => { __app.speed = 8; });
    await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 120000});
    await shot('choice');
    await p.evaluate(() => document.getElementById('choicego').scrollIntoView({block: 'center'}));
    await p.tap('#choicego'); await p.waitForTimeout(1500);
    s = await p.evaluate(() => __app.play);
    ok(name + ' Continue goes on into Play ' + JSON.stringify(s), s && s.reel === 'play' && s.n === 61);
    await p.evaluate(() => { __app.speed = 8; });
    let maxI = 0, splitSeen = false, lastCap = '';
    for (let i = 0; i < 600 && await p.evaluate(() => !!__app.play); i++){
      const t = await p.evaluate(() => ({i: __app.play ? __app.play.i : -1, n: __app.play ? __app.play.n : 0, judah: document.querySelectorAll('path.added.z-judah').length, cap: document.getElementById('cap').textContent}));
      maxI = Math.max(maxI, t.i); if (t.judah) splitSeen = true; if (t.i === t.n - 1) lastCap = t.cap;
      if (t.i === 56 && shots && !fs.existsSync(D + '/ch3_split.png')) await shot('split');
      await p.waitForTimeout(500);
    }
    ok(name + ' Play ran through every line (last index ' + maxI + ')', maxI === 60);
    ok(name + ' split drew Israel and Judah', splitSeen);
    ok(name + ' last subtitle is the teaser ' + JSON.stringify(lastCap.slice(0, 60)), /next chapter begins/.test(lastCap));
    const miss = [...Array(7).keys()].map(i => 'jews-1000-in-0' + (i + 1)).concat([...Array(61).keys()].map(i => 'jews-1000-play-' + String(i + 1).padStart(2, '0'))).filter(f => !req.has(f));
    ok(name + ' every line\'s recording requested (' + req.size + ') missing ' + JSON.stringify(miss), miss.length === 0);
    await p.waitForTimeout(2500);
    s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, flag: !!document.querySelector('.soonflag'), israel: document.querySelectorAll('path.z-israel').length, judah: document.querySelectorAll('path.z-judah').length, btn: (document.getElementById('gonextch') || {}).textContent}));
    ok(name + ' Play ends on the c. 930 BC intro with "Continue to Chapter 4", Israel and Judah on its map ' + JSON.stringify(s), s.mode === 'stop' && /930/.test(s.pill) && !s.flag && s.israel >= 1 && s.judah >= 1 && /Continue to Chapter 4/.test(s.btn || ''));
    await shot('end930');
    ok(name + ' Chapter 3 counted as watched', await p.evaluate(() => __app.parts()[2].done));
  } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
  await ctx.close(); await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  const f = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(f ? f + ' FAILED' : 'ALL PASS ' + notes.length);
  process.exit(f || errs.length ? 1 : 0);
})();
