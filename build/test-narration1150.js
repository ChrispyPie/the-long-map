// c. 1150 BC stop: the second recorded stop. Data checks (recordings, chapters, no digits,
// no frame lines in Play, pig-bone wording, battles without arrows, no border for David),
// then in the browser: the 1150 opener ends on its choice and Continue goes on into Play,
// a tap only shows the controls (never pauses), sound gaps stay within 2 s, Play ends on the
// c. 1000 BC 'coming soon' state, and objects added for 1150 are not drawn on the 1207 map.
// Usage: node build/test-narration1150.js [url] [noshots]; SHOTS=dir for n1150_*.png screenshots.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const J = f => JSON.parse(fs.readFileSync(path.join(ROOT, f), 'utf8'));
  const story = J('data/stories/jews/story.json'), data = J('data/stories/jews/1150bc.json'), lib = J('data/objects/near-east.json');
  const IN = data.transitionIn.beats, PL = data.play.beats, all = IN.concat(PL);
  const caps = b => b.steps.filter(x => x.type === 'caption');
  const s1150 = story.stops.find(s => s.year === -1150), s1000 = story.stops.find(s => s.year === -1000);
  ok('1150 is a live stop with its own map', s1150 && s1150.file === 'data/stories/jews/1150bc.json' && s1150.era === 'data/eras/1150bc.json' && !s1150.soon && fs.existsSync(path.join(ROOT, s1150.era)));
  ok('1000 is the next, "coming soon" stop', s1000 && !s1000.file && s1000.soon && /David/.test(s1000.soon.title));
  ok('Play runs from c. 1150 to c. 1000 BC', data.play.to === -1000 && data.transitionOut && data.transitionOut.to === -1000);
  const sizes = all.map(b => b.audio && fs.existsSync(path.join(ROOT, b.audio)) ? fs.statSync(path.join(ROOT, b.audio)).size : -1);
  ok('every line has its recording (' + all.length + ' files, ' + Math.round(sizes.reduce((a, s) => a + s, 0) / 1024) + ' kB)', all.length === 59 && sizes.every(s => s > 4000 && s < 80000));
  const idx = J('assets/narration/index.json');
  ok('every recording listed in index.json', all.every(b => { const k = Object.keys(idx).find(k => b.audio.endsWith(k)); return k && idx[k].ms > 0; }));
  ok('audioMs measured for every line', all.every(b => b.audioMs > 2000 && b.audioMs < 20000));
  ok('spoken text has no digits or brackets', all.every(b => caps(b).every(c => !/[()\d]/.test(c.text))));
  ok('exactly one choice, at the end of the opener', IN.filter(b => b.choice).length === 1 && IN[IN.length - 1].choice && PL.every(b => !b.choice));
  const chIn = IN.filter(b => b.chapter).map(b => b.chapter), chPl = PL.filter(b => b.chapter).map(b => b.chapter);
  ok('chapters: ' + chIn.concat(chPl).join(' / '), JSON.stringify(chIn) === '["The world of 1150 BC"]' && JSON.stringify(chPl) === JSON.stringify(['Five cities on the coast', 'Shiloh and the Judges', 'Saul, the first king', 'David: tradition and evidence']));
  ok('no frame lines in Play', PL.every(b => caps(b).every(c => c.cert !== 'frame')));
  ok('scene lines start with "Imagine"', all.every(b => caps(b).every(c => c.cert !== 'scene' || /^Imagine/.test(c.text))));
  ok('every Bible ref cites the Bible', all.every(b => caps(b).every(c => !c.ref || (c.src || []).includes('bible'))));
  const srcIds = new Set(Object.keys(J('data/sources.json').sources || J('data/sources.json')));
  ok('every cited source exists', all.every(b => caps(b).every(c => (c.src || []).every(s => srcIds.has(s)))));
  const pig = PL.flatMap(caps).find(c => /pig bones/.test(c.text));
  ok('Qeiyafa: "no pig bones" (not "almost no"), sourced: ' + (pig && pig.text), pig && /and no pig bones/.test(pig.text) && !/almost no pig/.test(pig.text) && pig.src.includes('garfinkelganor2009'));
  const battles = PL.flatMap(b => b.steps.filter(x => x.type === 'battle'));
  ok('battles (' + battles.map(x => x.label).join(', ') + ') have no army arrows', battles.length === 2 && battles.every(x => Array.isArray(x.arrows) && x.arrows.length === 0));
  ok('no border step draws a kingdom for David', !PL.some(b => b.steps.some(x => /border|zone/.test(x.type) && /david|united|kingdom/i.test(JSON.stringify(x)))));
  const late = lib.objects.filter(o => o.since === -1150).map(o => o.id);
  ok('11 objects added for 1150 (since -1150): ' + late.join(','), late.length === 11 && late.includes('qeiyafa'));

  const b = await chromium.launch({args: ['--autoplay-policy=no-user-gesture-required']});
  for (const [name, vw, vh, mobile] of [['mobile', 390, 844, true], ['desktop', 1280, 800, false]]) {
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 2, isMobile: mobile, hasTouch: mobile});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage();
    try {
      p.on('console', m => { if (m.type() === 'error') errs.push(name + ': ' + m.text()); });
      p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
      const req = []; p.on('request', r => { if (/jews-1150-/.test(r.url())) req.push(r.url()); });
      const shot = async n => { if (shots) await p.screenshot({path: D + '/n1150_' + n + (mobile ? '' : '_desktop') + '.png'}); };
      const drawn = () => p.evaluate(() => [...document.querySelectorAll('g.obj, g.lobj')].map(g => (g.__data__.o || g.__data__).id));
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(1500);
      let ids = await drawn();
      const shown = late.filter(id => ids.includes(id));
      ok(name + ' 1207 map: none of the 1150 objects drawn ' + JSON.stringify(shown), ids.length > 20 && shown.length === 0);
      await p.evaluate(() => __app.go(1)); await p.waitForTimeout(1600);
      let s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, hatti: document.querySelectorAll('path.z-hatti').length, phil: document.querySelectorAll('path.z-philistia').length, added: document.querySelectorAll('path.added').length}));
      ok(name + ' timeline to c. 1150: live stop on its own map ' + JSON.stringify(s), s.mode === 'stop' && /1150/.test(s.pill) && s.hatti === 0 && s.phil >= 1 && s.added === 0);
      ids = await drawn();
      ok(name + ' 1150 map: Qeiyafa, Shiloh, Dor drawn', ['qeiyafa', 'shiloh', 'dor'].every(id => ids.includes(id)));
      await shot('intro');
      // opener
      await p.evaluate(() => __app.playStart('intro', 0)); await p.waitForTimeout(2500);
      s = await p.evaluate(() => ({play: __app.play, ch: __app.chapters('intro'), voice: __app.voice}));
      ok(name + ' opener runs with voice ' + JSON.stringify(s.play), s.play && s.play.reel === 'intro' && s.play.n === 7 && s.ch.length === 1 && /jews-1150-in-01/.test(s.voice.src || ''));
      // a tap on the picture shows the controls, never pauses
      const vb = await p.evaluate(() => { const r = document.getElementById('vp').getBoundingClientRect(); return {x: r.x + r.width / 2, y: r.y + r.height / 2}; });
      mobile ? await p.touchscreen.tap(vb.x, vb.y) : await p.mouse.click(vb.x, vb.y); await p.waitForTimeout(500);
      s = await p.evaluate(() => ({paused: __app.play.paused, idle: document.body.classList.contains('idle'), open: __app.open}));
      ok(name + ' tap on the picture does not pause ' + JSON.stringify(s), s.paused === false && !s.open);
      // to the choice, then Continue goes on into Play
      await p.evaluate(() => { __app.speed = 12; __app.seek(6); });
      await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 40000});
      const sub = await p.evaluate(() => document.getElementById('choice').textContent);
      ok(name + ' opener ends on its choice, offering the Play ' + JSON.stringify(sub.slice(0, 120)), /1150/.test(sub) && /1000/.test(sub));
      await shot('choice');
      await p.evaluate(() => document.getElementById('choicego').scrollIntoView({block: 'center'}));
      mobile ? await p.tap('#choicego') : await p.click('#choicego'); await p.waitForTimeout(1500);
      s = await p.evaluate(() => __app.play);
      ok(name + ' Continue goes on into Play ' + JSON.stringify(s), s && s.reel === 'play' && s.n === 52 && !s.choice);
      const ch = await p.evaluate(() => __app.chapters('play').map(c => c.title));
      ok(name + ' Play chapters ' + ch.join(' / '), ch.length === 4 && ch[3] === 'David: tradition and evidence');
      // tap in Play: still no pause
      await p.evaluate(() => { __app.speed = 1; }); await p.waitForTimeout(600);
      mobile ? await p.touchscreen.tap(vb.x, vb.y) : await p.mouse.click(vb.x, vb.y); await p.waitForTimeout(500);
      ok(name + ' tap in Play does not pause', await p.evaluate(() => __app.play && __app.play.paused === false));
      // battle beat (Aphek): marker, no army arrows, gap capped at 2 s
      await p.evaluate(() => __app.seek(19)); await p.waitForTimeout(5000);
      s = await p.evaluate(() => ({battle: document.querySelectorAll('.battle').length, army: document.querySelectorAll('.arrow.army').length, gap: __app.gap(19), gap2: __app.gap(32)}));
      ok(name + ' Aphek battle: marker, no army arrows, gaps <= 2 s ' + JSON.stringify(s), s.battle >= 1 && s.army === 0 && s.gap <= 2000 && s.gap2 <= 2000);
      await shot('film');
      ok(name + ' Play voice lines requested', req.some(u => /jews-1150-play-/.test(u)));
      // run to the end: c. 1000 BC coming soon, no border for David
      await p.evaluate(() => { __app.speed = 12; __app.seek(__app.play.n - 2); });
      for (let i = 0; i < 80 && await p.evaluate(() => !!__app.play); i++) await p.waitForTimeout(500);
      await p.waitForTimeout(2500);
      s = await p.evaluate(() => ({mode: __app.mode, pill: document.getElementById('pill').textContent, flag: !!document.querySelector('.soonflag'), added: document.querySelectorAll('path.added').length, body: document.getElementById('evbody').textContent.slice(0, 400)}));
      ok(name + ' Play ends on c. 1000 BC coming soon, no border drawn for David ' + JSON.stringify({mode: s.mode, pill: s.pill, flag: s.flag, added: s.added}), s.mode === 'soon' && /1000/.test(s.pill) && s.flag && s.added === 0 && /David/.test(s.body));
      await shot('soon1000');
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
