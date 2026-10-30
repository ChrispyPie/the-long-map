// Sound effects: gesture-only start, ducking under the line, rising in the pause, sfxHold, toggle.
// Usage: node build/test-sfx.js [url] [noshots]; SHOTS=dir for the control screenshot.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const b = await chromium.launch({args: ['--autoplay-policy=user-gesture-required']});
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  // files: all clips there and small
  const F = ['battle','migration','border','year','amb-desert','amb-river'].map(f => path.join(ROOT, 'assets/sfx', f + '.mp3'));
  const sizes = F.map(f => fs.existsSync(f) ? fs.statSync(f).size : -1);
  ok('sfx files exist and are small '+JSON.stringify(sizes), sizes.every(s => s > 5000 && s < 130000) && sizes.reduce((a, s) => a + s, 0) < 500000);
  ok('sfx prompts and credits documented', /character-cost|credits/i.test(fs.readFileSync(path.join(ROOT, 'assets/sfx/README.md'), 'utf8')));
  const near = (a, x, e) => Math.abs(a - x) < (e || 0.01);
  for (const [name, vw, vh, mobile, rm] of [['desktop',1280,800,false,false],['mobile',393,852,true,false],['mobile-reduced',393,852,true,true]]) {
    const ctx = await b.newContext({viewport:{width:vw,height:vh}, deviceScaleFactor:2, isMobile:mobile, hasTouch:mobile, reducedMotion: rm ? 'reduce' : 'no-preference'});
    await ctx.addInitScript(() => {
      localStorage.setItem('tlm.notice.v1', 'seen');
      window.__acN = 0; const A = window.AudioContext;
      window.AudioContext = class extends A { constructor(...a){ super(...a); window.__acN++; } };
    });
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type()==='error') errs.push(name+': '+m.text()); });
    p.on('pageerror', e => errs.push(name+' pageerror: '+e.message));
    const req = []; p.on('request', r => { if (/assets\/sfx\//.test(r.url())) req.push(r.url()); });
    const tap = async sel => { if (/^#cap/.test(sel)){ await p.evaluate(()=>dispatchEvent(new PointerEvent('pointermove'))); await p.waitForTimeout(80); } return mobile ? p.tap(sel) : p.click(sel); };
    const S = () => p.evaluate(() => __app.snd);
    await p.goto(url, {waitUntil:'networkidle'}); await p.waitForTimeout(900);
    ok(name+' no audio and no sfx downloads before a gesture', await p.evaluate(() => window.__acN === 0 && __app.snd.ctx === null) && req.length === 0);
    ok(name+' sound button sits next to CC', await p.evaluate(() => { const c = document.getElementById('capcc'), s = document.getElementById('capsnd'); return !!s && c.nextElementSibling === s && /Sound (on|off)/.test(s.getAttribute('aria-label')); }));
    const pressed = await p.evaluate(() => document.getElementById('capsnd').getAttribute('aria-pressed'));
    ok(name+' default: '+(rm ? 'off with reduced motion' : 'on')+' ('+pressed+')', pressed === (rm ? 'false' : 'true'));
    // start the film from the Play button (a real gesture)
    await p.evaluate(() => __app.showStep(9)); await p.waitForTimeout(1200);
    await p.evaluate(() => document.getElementById('playbtn').scrollIntoView({block:'center'}));
    await tap('#playbtn'); await p.waitForTimeout(2600);
    let s = await S();
    if (rm){
      ok(name+' reduced: playing silently, no audio context '+JSON.stringify(s), s.ctx === null && !s.on && s.target === 0);
      await tap('#capsnd'); await p.waitForTimeout(1500); s = await S();
      ok(name+' reduced: sound can still be switched on '+JSON.stringify(s), s.on && s.ctx === 'running' && s.amb === 'desert');
      await tap('#capsnd');
      await ctx.close(); continue;
    }
    ok(name+' audio starts with Play: one context, running '+JSON.stringify(s), await p.evaluate(() => window.__acN) === 1 && s.ctx === 'running');
    const row = await p.evaluate(() => { const bs = [...document.querySelectorAll('.cap2 .crow button')].map(e => e.getBoundingClientRect()); return {rows: new Set(bs.map(x => Math.round(x.top))).size, l: Math.min(...bs.map(x => x.left)), r: Math.max(...bs.map(x => x.right)), W: innerWidth}; });
    ok(name+' film controls fit on one row (two on a phone) '+JSON.stringify(row), row.rows === (row.W <= 640 ? 2 : 1) && row.l >= 0 && row.r <= row.W);
    ok(name+' all clips loaded '+s.loaded, s.loaded.join() === 'battle,border,desert,migration,river,year');
    ok(name+' ambient loop under the scene: '+s.amb, s.amb === 'desert');
    ok(name+' ducked about -18 dB under the line '+JSON.stringify(s), s.phase === 'voice' && near(s.target, Math.pow(10, -18/20)) && s.gain < 0.2);
    ok(name+' year change plays the page turn', s.shots.includes('year'));
    // beat 6: Ugarit battle with sfxHold 3000; the breath after the line is capped at 2 s (0.6 s pause + up to 1.4 s swell)
    const planOn = await p.evaluate(() => __app.plan(6));
    await p.evaluate(() => __app.seek(6));
    await p.waitForFunction(() => __app.snd.shots.includes('battle'), null, {timeout: 6000}).catch(() => {});
    ok(name+' battle step plays the battle clip', (await S()).shots.includes('battle'));
    const t0 = await p.evaluate(() => __app.clock);
    await p.waitForFunction(() => __app.snd.phase === 'fill', null, {timeout: 20000}).catch(() => {});
    await p.waitForTimeout(1100); s = await S();
    ok(name+' rises to about -6 dB in the pause '+JSON.stringify(s), s.phase === 'fill' && near(s.target, Math.pow(10, -6/20)) && s.gain > 0.4);
    // the hold: beat 6 lasts its plan (with the hold) on the virtual clock
    await p.waitForFunction(() => __app.play && __app.play.i === 7, null, {timeout: 25000}).catch(() => {});
    s = await S();
    const t1 = await p.evaluate(() => __app.clock);
    ok(name+' ducks again when the next line starts '+JSON.stringify(s), s.phase === 'voice' && s.target < 0.2);
    // sound off: the plan drops the hold, the choice is remembered
    await tap('#capsnd'); await p.waitForTimeout(700);
    const planOff = await p.evaluate(() => __app.plan(6)); s = await S();
    ok(name+' sfxHold stretches the gap to 2 s max, only with sound on ('+planOn+' vs '+planOff+', beat ran '+Math.round(t1 - t0)+' ms of clock)', planOn - planOff === 1400 && t1 - t0 > planOn - 1500 - 700);
    ok(name+' sound off: silent, remembered '+JSON.stringify(s), !s.on && s.target === 0 && s.amb === null && await p.evaluate(() => localStorage.getItem('tlm.snd') === 'off' && document.getElementById('capsnd').getAttribute('aria-pressed') === 'false'));
    await tap('#capsnd'); await p.waitForTimeout(1500); s = await S();
    ok(name+' sound back on: ambient again '+JSON.stringify(s), s.on && s.amb === 'desert' && s.ctx === 'running');
    if (shots){ await p.evaluate(() => { document.body.classList.remove('idle'); }); await p.mouse.move(vw/2, vh/2); await p.waitForTimeout(400);
      await p.screenshot({path: D+'/design2_sound_control'+(mobile ? '' : '_desktop')+'.png'});
      const r = await p.evaluate(() => { const e = document.querySelector('.cap2 .crow').getBoundingClientRect(); return {x: e.left - 8, y: e.top - 8, width: e.width + 16, height: e.height + 16}; });
      await p.screenshot({path: D+'/design2_sound_control_zoom'+(mobile ? '' : '_desktop')+'.png', clip: r}); }
    // speed: the hold is on the virtual clock, so 1.25x shortens it in real time
    await p.evaluate(() => { __app.speed = 1.25; __app.seek(10); });
    const r0 = Date.now();
    await p.waitForFunction(() => __app.play && __app.play.i === 11, null, {timeout: 30000}).catch(() => {});
    const real = Date.now() - r0, plan4 = await p.evaluate(() => __app.plan(10));
    ok(name+' migration hold follows speed 1.25x ('+real+' ms real for '+plan4+' ms plan)', real < plan4 / 1.25 + 900 && real > plan4 / 1.25 - 900);
    await p.evaluate(() => { __app.speed = 1; });
    // pause suspends the audio, play resumes it
    await p.evaluate(() => __app.playPause(true)); await p.waitForTimeout(400);
    const sp = (await S()).ctx;
    await p.evaluate(() => __app.playPause(false)); await p.waitForTimeout(400);
    ok(name+' pause suspends sound, play resumes ('+sp+' -> '+(await S()).ctx+')', sp === 'suspended' && (await S()).ctx === 'running');
    // Skip in the middle of a hold ends the sound with the film
    await p.evaluate(() => __app.seek(15));
    await p.waitForFunction(() => __app.snd.phase === 'fill', null, {timeout: 25000}).catch(() => {});
    ok(name+' river ambient at the Nile', (await S()).amb === 'river');
    await p.mouse.move(vw/2, vh/2 + 3); await p.waitForTimeout(150);
    await p.evaluate(() => document.getElementById('capskip').click()); await p.waitForTimeout(300);
    s = await S();
    ok(name+' Skip cuts the hold and fades sound out '+JSON.stringify(s), (await p.evaluate(() => __app.play)) === null && s.target === 0 && s.amb === null && s.shots.length === 0);
    await p.evaluate(() => __app.setSnd(false)); await p.reload({waitUntil:'networkidle'}); await p.waitForTimeout(800);
    ok(name+' sound choice remembered after reload', await p.evaluate(() => !__app.snd.on && document.getElementById('capsnd').getAttribute('aria-pressed') === 'false' && window.__acN === 0));
    await ctx.close();
  }
  await b.close();
  notes.forEach(n => console.log(n)); console.log('ERRORS', JSON.stringify(errs));
  const fails = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(fails ? 'FAILED ' + fails : 'ALL PASS ' + notes.length);
  process.exit(fails ? 1 : 0);
})();
