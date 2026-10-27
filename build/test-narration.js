// Narration: recorded lines drive the timing; the opening film ends on a choice; chapters, resume,
// the narrator switch, digits in subtitles ("display"), frame lines without a badge, Bible refs.
// Usage: node build/test-narration.js [url] [noshots]; SHOTS=dir for narr_*.png screenshots.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  // files: one small mono mp3 per line, all listed in the index
  const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/stories/jews/1207bc.json'), 'utf8'));
  const IN = data.transitionIn.beats, PL = data.play.beats, all = IN.concat(PL);
  const sizes = all.map(b => b.audio && fs.existsSync(path.join(ROOT, b.audio)) ? fs.statSync(path.join(ROOT, b.audio)).size : -1);
  ok('every line has its recording ('+all.length+' files, '+Math.round(sizes.reduce((a, s) => a + s, 0) / 1024)+' kB)', sizes.every(s => s > 4000 && s < 80000) && sizes.reduce((a, s) => a + s, 0) < 5e6);
  ok('audioMs measured for every line', all.every(b => b.audioMs > 2000 && b.audioMs < 20000));
  ok('transitionIn keeps its text fallback', typeof data.transitionIn.text === 'string' && data.transitionIn.text.length > 40);
  ok('spoken text has no digits or brackets', all.every(b => b.steps.filter(x => x.type === 'caption').every(c => !/[()\d]/.test(c.text))));
  ok('exactly one choice, at the end of the opener', IN.filter(b => b.choice).length === 1 && PL.every(b => !b.choice));
  const iChoice = IN.findIndex(b => b.choice), iDisp = IN.findIndex(b => b.steps.some(x => x.display && /\d/.test(x.display) && x.cert !== 'frame'));
  const iRef = PL.findIndex(b => b.steps.some(x => x.ref && /\d/.test(x.ref)));
  const b = await chromium.launch({args: ['--autoplay-policy=user-gesture-required']});
  for (const [name, vw, vh, mobile] of [['desktop',1280,800,false],['mobile',393,852,true]]) {
    const ctx = await b.newContext({viewport:{width:vw,height:vh}, deviceScaleFactor:2, isMobile:mobile, hasTouch:mobile});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage();
    try {
    p.on('console', m => { if (m.type()==='error') errs.push(name+': '+m.text()); });
    p.on('pageerror', e => errs.push(name+' pageerror: '+e.message));
    const req = []; p.on('request', r => { if (/assets\/narration\//.test(r.url())) req.push(r.url()); });
    const panelShot = async (sel, name) => {
      await p.evaluate(sel => { const e = document.querySelector(sel), v = document.getElementById('vp'), cs = getComputedStyle(v); const off = cs.position === 'sticky' ? (parseFloat(cs.top) || 0) + v.offsetHeight + 12 : innerHeight / 3; window.scrollTo({top: Math.max(0, e.getBoundingClientRect().top + scrollY - off), behavior: 'instant'}); }, sel);
      await p.waitForTimeout(300);
      await p.screenshot({path: D + '/' + name + (mobile ? '' : '_desktop') + '.png'});
    };
    const tap = async sel => { await p.evaluate(s => document.querySelector(s).scrollIntoView({block:'center'}), sel); return mobile ? p.tap(sel) : p.click(sel); };
    const P = () => p.evaluate(() => __app.play);
    const wake = async () => { await p.mouse.move(vw/2, vh/3); await p.mouse.move(vw/2 + 5, vh/3 + 3); await p.waitForTimeout(250); };
    await p.goto(url, {waitUntil:'networkidle'}); await p.waitForTimeout(900);
    ok(name+' no narration downloads before a click', req.length === 0);
    // the intro panel: watch the opening (about a minute), explore, or read
    await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(900);
    const ip = await p.evaluate(() => ({go: document.getElementById('gostory').textContent, map: !!document.getElementById('goexplore'), read: !!document.getElementById('goread'), ch: document.querySelectorAll('#evbody .chlist .chb').length}));
    ok(name+' intro panel: '+JSON.stringify(ip), /Watch the opening · about 1 minute/.test(ip.go) && ip.map && ip.read && ip.ch === 3);
    const chIn = await p.evaluate(() => __app.chapters('intro'));
    ok(name+' opener plan '+Math.round(chIn[0].ms/1000)+' s (75-90), chapters '+chIn.map(c => c.title+' '+Math.round(c.ms/1000)+'s').join(' | '), chIn.length === 3 && chIn[0].ms >= 75000 && chIn[0].ms <= 90000 && chIn[0].end === iChoice + 1);
    if (shots){ await p.evaluate(() => document.getElementById('gostory').scrollIntoView({block:'center'})); await p.waitForTimeout(300); }
    if (shots) await panelShot('#gostory', 'narr_intro_panel');
    await tap('#gostory'); await p.waitForTimeout(2200);
    let pl = await P(), v = await p.evaluate(() => __app.voice);
    ok(name+' opening film starts: '+JSON.stringify(pl), pl && pl.reel === 'intro' && pl.i === 0 && pl.chapter === 1);
    ok(name+' the narrator speaks line 1 '+(v.src || '').split('/').pop(), v.on && v.playing && /jews-1207-in-01\.mp3$/.test(v.src));
    ok(name+' no <audio> element in the page', await p.evaluate(() => document.querySelectorAll('audio').length === 0));
    const fr = await p.evaluate(() => ({b: !!document.querySelector('#captext .cb'), s: document.getElementById('capsrc').textContent, t: document.getElementById('captext').textContent, card: !document.getElementById('chapcard').hidden && document.getElementById('chapcard').textContent}));
    ok(name+' frame line: no badge, no sources, chapter card '+JSON.stringify(fr).slice(0, 140), !fr.b && fr.s === '' && fr.t.length > 10 && /Chapter 1 of 3/.test(fr.card));
    // timing follows the recording: plan = audio + pause, and the reading time when the voice is off
    const tm = await p.evaluate(() => { const a = __app.plan(0); __app.setVoice(false); const r = __app.plan(0); __app.setVoice(true); return {a, r}; });
    ok(name+' beat 1 plan follows the recording ('+tm.a+' ms with voice, '+tm.r+' ms without)', tm.a === IN[0].audioMs + IN[0].pauseAfter && tm.r === IN[0].duration + IN[0].pauseAfter);
    // display: digits in the subtitle, words in the voice
    await p.evaluate(i => __app.seek(i), iDisp); await p.waitForTimeout(500);
    const dp = await p.evaluate(() => document.getElementById('captext').textContent);
    const want = IN[iDisp].steps.find(x => x.display).display;
    ok(name+' subtitle shows digits: '+dp.slice(0, 70), dp.includes(want) && /\d/.test(dp) && !!(await p.$('#captext .cb')));
    // the voice switch: off stops the line, the film goes on, remembered
    await p.evaluate(() => __app.setVoice(false)); await p.waitForTimeout(300);
    v = await p.evaluate(() => ({v: __app.voice, ls: localStorage.getItem('tlm.voice'), pr: document.getElementById('capvoice').getAttribute('aria-pressed')}));
    ok(name+' narrator off: silent, remembered '+JSON.stringify(v), !v.v.on && !v.v.playing && v.ls === 'off' && v.pr === 'false');
    await wake(); await tap('#capvoice'); await p.waitForTimeout(200);
    ok(name+' narrator button turns it back on', await p.evaluate(() => __app.voice.on && localStorage.getItem('tlm.voice') === 'on'));
    // the choice: the opener's last line, then the film waits
    await p.evaluate(i => { __app.speed = 1.25; __app.seek(i); }, iChoice);
    await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 25000}).catch(() => {});
    await p.waitForTimeout(2500); pl = await P();
    const ch = await p.evaluate(() => { const r = id => { const e = document.getElementById(id).getBoundingClientRect(); return e.width > 80 && e.height >= 44 && e.bottom <= innerHeight && e.top >= 0; }; return {go: r('choicego'), map: r('choicemap'), q: document.querySelector('#choice .q').textContent, sub: document.getElementById('choicesub').textContent}; });
    ok(name+' choice shown and the film waits: '+JSON.stringify(pl)+' '+JSON.stringify(ch), pl.i === iChoice && pl.hold && pl.choice && ch.go && ch.map && /Chapter 2/.test(ch.sub));
    const row1 = await p.evaluate(() => { const bs = [...document.querySelectorAll('.cap2 .crow button')].map(e => e.getBoundingClientRect()); return {rows: new Set(bs.map(x => Math.round(x.top))).size, r: Math.max(...bs.map(x => x.right)), W: innerWidth}; });
    ok(name+' controls on one row at 1.25x too '+JSON.stringify(row1), row1.rows === 1 && row1.r <= row1.W);
    if (shots){ await wake(); await p.screenshot({path: D+'/narr_choice'+(mobile ? '' : '_desktop')+'.png'}); }
    await tap('#choicego'); await p.waitForTimeout(700); pl = await P();
    ok(name+' Continue the story: chapter 2 begins '+JSON.stringify(pl), pl.i === iChoice + 1 && pl.chapter === 2 && !pl.choice && /Chapter 2 of 3/.test(await p.textContent('#chapcard')));
    // chapter strip: one segment per chapter, a click jumps there
    await wake();
    const segs = await p.evaluate(() => [...document.querySelectorAll('#capch .chs')].map(e => ({t: e.textContent, w: Math.round(e.getBoundingClientRect().width), cur: e.classList.contains('cur')})));
    ok(name+' chapter strip '+JSON.stringify(segs), segs.length === 3 && segs[1].cur && segs.every(s => s.w > 20));
    await p.evaluate(() => document.querySelectorAll('#capch .chs')[2].click()); await p.waitForTimeout(600); pl = await P();
    ok(name+' strip jumps to chapter 3 '+JSON.stringify(pl), pl.i === chIn[2].i && pl.chapter === 3);
    // stop: the chapter is remembered and offered on the intro panel
    await p.evaluate(() => document.getElementById('capx').click()); await p.waitForTimeout(1800);
    ok(name+' resume saved at chapter 3', await p.evaluate(() => __app.resume('intro')) === chIn[2].i);
    await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(700);
    ok(name+' intro panel offers Resume at chapter 3', /Resume at chapter 3/.test(await p.evaluate(() => (document.getElementById('goresume') || {}).textContent || '')));
    await tap('#goresume'); await p.waitForTimeout(2200); pl = await P();
    ok(name+' resume plays from chapter 3 '+JSON.stringify(pl), pl && pl.reel === 'intro' && pl.i === chIn[2].i);
    // Skip in the opener goes to the map
    await wake(); await p.evaluate(() => document.getElementById('capskip').click()); await p.waitForTimeout(2200);
    ok(name+' Skip ends the opener on the map', await p.evaluate(() => __app.play === null && __app.step === 9 && __app.resume('intro') === 0));
    // Explore the map from the choice: lands on the map, chapter 2 offered later
    await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(600); await tap('#gostory'); await p.waitForTimeout(1500);
    await p.evaluate(i => { __app.speed = 1.25; __app.seek(i); }, iChoice);
    await p.waitForFunction(() => __app.play && __app.play.choice, null, {timeout: 25000}).catch(() => {});
    await tap('#choicemap'); await p.waitForTimeout(2200);
    ok(name+' Explore the map: film closed, Explore step, chapter 2 to resume', await p.evaluate(i => __app.play === null && __app.step === 9 && __app.resume('intro') === i, iChoice + 1));
    // Play: four chapters of about 2-3 minutes, markers, Bible reference after the sources
    const exp = await p.evaluate(() => ({btn: document.getElementById('playbtn') && document.querySelector('#playbtn + .cap').textContent, ch: document.querySelectorAll('#evbody .chlist .chb').length}));
    ok(name+' explore panel: '+JSON.stringify(exp).slice(0, 120), /in 4 chapters/.test(exp.btn) && exp.ch === 4);
    if (shots) await panelShot('#playbtn', 'narr_explore_panel');
    await p.evaluate(() => __app.speed = 1);
    await tap('#playbtn'); await p.waitForTimeout(2500);
    const chP = await p.evaluate(() => __app.chapters('play'));
    ok(name+' Play chapters '+chP.map(c => c.title+' '+Math.round(c.ms/1000)+'s').join(' | '), chP.length === 4 && chP.every(c => c.ms >= 100000 && c.ms <= 200000));
    ok(name+' Play voiced: '+((await p.evaluate(() => __app.voice.src)) || '').split('/').pop(), /jews-1207-play-01\.mp3$/.test(await p.evaluate(() => __app.voice.src)));
    await wake(); await p.evaluate(() => document.querySelectorAll('#capch .chs')[2].click()); await p.waitForTimeout(900);
    pl = await P();
    ok(name+' Play strip: chapter 3 '+JSON.stringify(pl)+' card '+await p.textContent('#chapcard'), pl.i === chP[2].i && pl.chapter === 3 && /Chapter 3 of 4/.test(await p.textContent('#chapcard')));
    if (shots){ await wake(); await p.waitForTimeout(400); await p.screenshot({path: D+'/narr_chapters'+(mobile ? '' : '_desktop')+'.png'}); }
    const row = await p.evaluate(() => { const bs = [...document.querySelectorAll('.cap2 .crow button')].map(e => e.getBoundingClientRect()); return {rows: new Set(bs.map(x => Math.round(x.top))).size, r: Math.max(...bs.map(x => x.right)), W: innerWidth}; });
    ok(name+' controls with the narrator button still on one row '+JSON.stringify(row), row.rows === 1 && row.r <= row.W);
    await p.evaluate(i => __app.seek(i), iRef); await p.waitForTimeout(500);
    const rs = await p.textContent('#capsrc'), wantRef = PL[iRef].steps.find(x => x.ref).ref;
    ok(name+' Bible reference after the sources: '+rs, rs.startsWith('Sources:') && rs.endsWith(' · ' + wantRef));
    await p.keyboard.press('Escape'); await p.waitForTimeout(1500);
    ok(name+' Escape keeps the Play chapter (2, where the Amos line is) for later', await p.evaluate(() => __app.play === null && __app.resume('play') === 10) && /Resume at chapter 2: The Sea Peoples/.test(await p.evaluate(() => (document.getElementById('playresume') || {}).textContent || '')));
    await p.reload({waitUntil:'networkidle'}); await p.waitForTimeout(800);
    ok(name+' resume survives a reload', await p.evaluate(() => __app.showStep(9) || true) && (await p.waitForTimeout(800), /Resume at chapter 2/.test(await p.evaluate(() => (document.getElementById('playresume') || {}).textContent || ''))));
    } catch(e){ ok(name+' crashed: '+e.message.split('\n')[0], false); }
    await ctx.close();
  }
  await b.close();
  notes.forEach(n => console.log(n)); console.log('ERRORS', JSON.stringify(errs));
  const fails = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(fails ? 'FAILED ' + fails : 'ALL PASS ' + notes.length);
  process.exit(fails ? 1 : 0);
})();
