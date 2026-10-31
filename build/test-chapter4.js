// Chapter 4 (c. 930 BC to 841 BC: Israel and Judah, Omri, Ahab, Qarqar, Mesha, Tel Dan, Jehu). Data: live stop,
// 9 opener + 68 Play lines, each with its recording, no digits or brackets in spoken text, every Bible ref cites
// the Bible, every vignette matches one line, the Play runs to 722 BC and ends on the teaser for the next chapter.
// Browser (390x844): the opener and the whole Play run start to finish (speed 8, voice on), every line's recording
// is requested, Israel and Judah are drawn, vignettes show, and the end is the 722 BC intro (Chapter 5) with a 'Continue to Chapter 5' button.
// Usage: node build/test-chapter4.js [url] [noshots]; SHOTS=dir for ch4_*.png screenshots.
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
  const story = J('data/stories/jews/story.json'), data = J('data/stories/jews/930bc.json');
  const IN = data.transitionIn.beats, PL = data.play.beats, all = IN.concat(PL);
  const caps = b => b.steps.filter(x => x.type === 'caption');
  const s930 = story.stops.find(s => s.year === -930), s722 = story.stops.find(s => s.year === -722);
  ok('930 is a live stop with its own map', s930 && s930.file === 'data/stories/jews/930bc.json' && s930.era === 'data/eras/930bc.json' && fs.existsSync(path.join(ROOT, s930.era)));
  ok('722 is the next, live stop (Chapter 5)', s722 && s722.file === 'data/stories/jews/722bc.json' && !s722.soon && data.play.to === -722);
  ok('8 events, each claim sourced and labelled', data.events.length === 8 && data.events.every(e => (e.claims || []).length && e.claims.every(c => Array.isArray(c[2]) && c[2].length && ['attested', 'disputed', 'tradition'].includes(c[1]))));
  const vig = all.filter(b => b.vignette);
  ok('vignettes on ' + vig.length + ' lines, files present', vig.length >= 20 && vig.every(b => fs.existsSync(path.join(ROOT, b.vignette.src))));
  ok('9 opener lines, 68 Play lines', IN.length === 9 && PL.length === 68);
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
    p.on('request', r => { const m = r.url().match(/(jews-930-(in|play)-\d+)\.mp3/); if (m) req.add(m[1]); });
    p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location().url || '')) errs.push(m.text()); });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    const shot = async n => { if (shots) await p.screenshot({path: D + '/ch4_' + n + '.png'}); };
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
    await p.evaluate(() => __app.go(3)); await p.waitForTimeout(1600);
    let s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, judah: document.querySelectorAll('path.z-judah').length, parts: __app.parts().length}));
    ok(name + ' timeline to c. 930 BC: live stop, Chapter 4 ' + JSON.stringify(s), s.mode === 'stop' && /930/.test(s.pill) && s.judah >= 1 && s.parts === 5);
    await shot('intro');
    await p.tap('#gostory'); await p.waitForTimeout(2000);
    s = await p.evaluate(() => ({play: __app.play, voice: __app.voice}));
    ok(name + ' opener runs with voice ' + JSON.stringify(s.play), s.play && s.play.reel === 'intro' && s.play.n === 9 && /jews-930-in-01/.test(s.voice.src || ''));
    await p.evaluate(() => { __app.speed = 8; });
    await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 120000});
    await shot('choice');
    await p.evaluate(() => document.getElementById('choicego').scrollIntoView({block: 'center'}));
    await p.tap('#choicego'); await p.waitForTimeout(1500);
    s = await p.evaluate(() => __app.play);
    ok(name + ' Continue goes on into Play ' + JSON.stringify(s), s && s.reel === 'play' && s.n === 68);
    await p.evaluate(() => { __app.speed = 8; });
    let maxI = 0, splitSeen = false, lastCap = '', vigSeen = new Set();
    for (let i = 0; i < 600 && await p.evaluate(() => !!__app.play); i++){
      const t = await p.evaluate(() => ({i: __app.play ? __app.play.i : -1, n: __app.play ? __app.play.n : 0, judah: document.querySelectorAll('path.z-judah').length, vig: ((document.querySelector('#vig img:not([hidden])') || {}).src || ''), cap: document.getElementById('cap').textContent}));
      maxI = Math.max(maxI, t.i); if (t.judah) splitSeen = true; const vm = t.vig.match(/c4-[\w-]+\.webp/); if (vm) vigSeen.add(vm[0]); if (t.i === t.n - 1) lastCap = t.cap;
      if (t.i === 34 && shots && !fs.existsSync(D + '/ch4_qarqar.png')) await shot('qarqar');
      await p.waitForTimeout(500);
    }
    ok(name + ' Play ran through every line (last index ' + maxI + ')', maxI === 67);
    ok(name + ' Israel and Judah on the map', splitSeen);
    ok(name + ' last subtitle is the teaser ' + JSON.stringify(lastCap.slice(0, 60)), /next chapter begins/.test(lastCap));
    const miss = [...Array(9).keys()].map(i => 'jews-930-in-0' + (i + 1)).concat([...Array(68).keys()].map(i => 'jews-930-play-' + String(i + 1).padStart(2, '0'))).filter(f => !req.has(f));
    ok(name + ' every line\'s recording requested (' + req.size + ') missing ' + JSON.stringify(miss), miss.length === 0);
    ok(name + ' Chapter 4 vignettes shown during Play (' + vigSeen.size + ')', vigSeen.size >= 10);
    await p.waitForTimeout(2500);
    s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, flag: !!document.querySelector('.soonflag'), btn: (document.getElementById('gonextch') || {}).textContent}));
    ok(name + ' Play ends on the 722 BC intro with "Continue to Chapter 5" ' + JSON.stringify(s), s.mode === 'stop' && /722/.test(s.pill) && !s.flag && /Continue to Chapter 5/.test(s.btn || ''));
    await shot('end722');
    ok(name + ' Chapter 4 counted as watched', await p.evaluate(() => __app.parts()[3].done));
  } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
  await ctx.close(); await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  const f = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(f ? f + ' FAILED' : 'ALL PASS ' + notes.length);
  process.exit(f || errs.length ? 1 : 0);
})();
