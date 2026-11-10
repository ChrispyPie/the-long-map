// Chapter 6 (c. 715 BC to 701 BC: Hezekiah, Ashdod's revolt, the great revolt, the tunnel, Lachish, Sennacherib at Jerusalem).
// Data: live stop, 8 opener + 65 Play lines, each with its recording, no digits or brackets in spoken text, every
// Bible ref cites the Bible, every vignette matches one line, the Play runs to 586 BC and ends on the teaser for the
// next chapter. Browser (390x844): the opener and the whole Play run start to finish (speed 8, voice on), every
// line's recording is requested, Samerina is on the map, Judah's lost lowlands are drawn, vignettes show, and the end
// is the 586 BC 'coming soon' state.
// Usage: node build/test-chapter6.js [url] [noshots]; SHOTS=dir for ch6_*.png screenshots.
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
  const story = J('data/stories/jews/story.json'), data = J('data/stories/jews/701bc.json');
  const IN = data.transitionIn.beats, PL = data.play.beats, all = IN.concat(PL);
  const caps = b => b.steps.filter(x => x.type === 'caption');
  const s701 = story.stops.find(s => s.year === -701), s586 = story.stops.find(s => s.year === -586);
  ok('701 is a live stop with its own map', s701 && s701.file === 'data/stories/jews/701bc.json' && s701.era === 'data/eras/701bc.json' && fs.existsSync(path.join(ROOT, s701.era)));
  ok('586 is the next, coming soon stop', s586 && !s586.file && s586.soon && data.play.to === -586);
  ok('every source cited in the chapter exists', (() => { const S = J('data/sources.json'), ids = new Set(Object.keys(S.sources || S)); return all.every(b => caps(b).every(c => (c.src || []).every(x => ids.has(x)))); })());
  ok('8 events, each claim sourced and labelled', data.events.length === 8 && data.events.every(e => (e.claims || []).length && e.claims.every(c => Array.isArray(c[2]) && c[2].length && ['attested', 'disputed', 'tradition'].includes(c[1]))));
  const vig = all.filter(b => b.vignette);
  ok('vignettes on ' + vig.length + ' lines, files present', vig.length >= 20 && vig.every(b => fs.existsSync(path.join(ROOT, b.vignette.src))));
  ok('8 opener lines, 65 Play lines', IN.length === 8 && PL.length === 65);
  const sizes = all.map(b => b.audio && fs.existsSync(path.join(ROOT, b.audio)) ? fs.statSync(path.join(ROOT, b.audio)).size : -1);
  ok('every line has its recording (' + Math.round(sizes.reduce((a, s) => a + s, 0) / 1024) + ' kB)', sizes.every(s => s > 4000 && s < 80000));
  ok('audioMs measured for every line', all.every(b => b.audioMs > 2000 && b.audioMs < 20000));
  ok('spoken text has no digits or brackets', all.every(b => caps(b).every(c => !/[()\d]/.test(c.text))));
  ok('every Bible ref cites the Bible', all.every(b => caps(b).every(c => !c.ref || (c.src || []).includes('bible'))));
  ok('no choice inside the films (it comes at the end of the chapter), the opener ends on a lead-in', IN.every(b => !b.choice) && PL.every(b => !b.choice) && /begin/.test(IN[IN.length - 1].steps.find(x => x.type === 'caption').text));
  ok('ends on the teaser for the next chapter', /next chapter begins\.$/.test(caps(PL[PL.length - 1])[0].text));
  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  const ctx = await b.newContext({viewport: {width: 390, height: 844}, deviceScaleFactor: 2, isMobile: true, hasTouch: true});
  await ctx.addInitScript(() => (localStorage.setItem('tlm.notice.v1', 'seen'), localStorage.setItem('tlm.recaps', 'off')));
  const p = await ctx.newPage();
  const name = 'mobile';
  try {
    const req = new Set();
    p.on('request', r => { const m = r.url().match(/(jews-701-(in|play)-\d+)\.mp3/); if (m) req.add(m[1]); });
    p.on('console', m => { if (m.type() === 'error' && !/favicon/.test(m.location().url || '')) errs.push(m.text()); });
    p.on('pageerror', e => errs.push('pageerror: ' + e.message));
    const shot = async n => { if (shots) await p.screenshot({path: D + '/ch6_' + n + '.png'}); };
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
    await p.evaluate(() => __app.go(5)); await p.waitForTimeout(1600);
    let s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, sam: document.querySelectorAll('path.z-samerina').length, aram: document.querySelectorAll('path.z-aram').length, parts: __app.parts().length}));
    ok(name + ' timeline to 701 BC: live stop, Chapter 6 ' + JSON.stringify(s), s.mode === 'stop' && /701/.test(s.pill) && s.sam >= 1 && !s.aram && s.parts === 6);
    await shot('intro');
    await p.tap('#gostory'); await p.waitForTimeout(300); if (await p.evaluate(() => !!__app.lenPick)) await p.click('#lpfull'); /* Quick or Full */ await p.waitForTimeout(2000);
    s = await p.evaluate(() => ({play: __app.play, voice: __app.voice}));
    ok(name + ' opener runs with voice ' + JSON.stringify(s.play), s.play && s.play.reel === 'intro' && s.play.n === 8 && /jews-701-in-01/.test(s.voice.src || ''));
    await p.evaluate(() => { __app.speed = 8; });
    // the opener runs straight on into Play (no choice in between)
    await p.waitForFunction(() => __app.play && __app.play.reel === 'play', null, {timeout: 120000});
    await p.waitForTimeout(300);
    s = await p.evaluate(() => __app.play);
    ok(name + ' the opener goes straight on into Play ' + JSON.stringify(s), s && s.reel === 'play' && s.n === 65);
    await p.evaluate(() => { __app.speed = 8; });
    let maxI = 0, provSeen = false, lastCap = '', vigSeen = new Set();
    for (let i = 0; i < 600 && await p.evaluate(() => !!__app.play && !__app.ended); i++){
      const t = await p.evaluate(() => ({i: __app.play ? __app.play.i : -1, n: __app.play ? __app.play.n : 0, prov: document.querySelectorAll('path.added.z-philistia').length, vig: ((document.querySelector('#vig img:not([hidden])') || {}).src || ''), cap: document.getElementById('cap').textContent}));
      maxI = Math.max(maxI, t.i); if (t.prov) provSeen = true; const vm = t.vig.match(/c6-[\w-]+\.webp/); if (vm) vigSeen.add(vm[0]); if (t.i === t.n - 1) lastCap = t.cap;
      if (t.i >= 36 && shots && !fs.existsSync(D + '/ch6_lachish.png')) await shot('lachish');
      await p.waitForTimeout(500);
    }
    ok(name + ' Play ran through every line (last index ' + maxI + ')', maxI === 64);
    ok(name + ' Judah\'s lost lowlands drawn on the map', provSeen);
    ok(name + ' last subtitle is the teaser ' + JSON.stringify(lastCap.slice(0, 60)), /next chapter begins/.test(lastCap));
    const miss = [...Array(8).keys()].map(i => 'jews-701-in-0' + (i + 1)).concat([...Array(65).keys()].map(i => 'jews-701-play-' + String(i + 1).padStart(2, '0'))).filter(f => !req.has(f));
    ok(name + ' every line\'s recording requested (' + req.size + ') missing ' + JSON.stringify(miss), miss.length === 0);
    ok(name + ' Chapter 6 vignettes shown during Play (' + vigSeen.size + ')', vigSeen.size >= 10);
    await p.waitForTimeout(1500);
    ok(name + ' the chapter ends on Stay with the story / Explore the map', await p.evaluate(() => __app.ended && !document.getElementById('choice').hidden && /Stay with the story/.test(document.getElementById('choicego').textContent)));
    await shot('endchoice');
    await p.tap('#choicego'); await p.waitForTimeout(800);
    await p.waitForTimeout(2000);
    s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, flag: !!document.querySelector('.soonflag')}));
    ok(name + ' Stay with the story after Chapter 6 → 586 BC coming soon ' + JSON.stringify(s), s.mode === 'soon' && /586/.test(s.pill) && s.flag);
    await shot('end586');
    ok(name + ' Chapter 6 counted as watched', await p.evaluate(() => __app.parts()[5].done));
  } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
  await ctx.close(); await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  const f = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(f ? f + ' FAILED' : 'ALL PASS ' + notes.length);
  process.exit(f || errs.length ? 1 : 0);
})();
