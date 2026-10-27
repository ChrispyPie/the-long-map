// Playback: a tap on the film (touch or mouse) never pauses or plays, it only shows the controls; pause and
// play only with the control-bar button (or Space). A narrator clip that fails, stalls or is stopped by the phone never
// pauses the film. Pacing: short gaps after lines, a few longer breaths (2 s max).
// Usage: node build/test-playback.js [url]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const ROOT = process.env.ROOT || path.join(__dirname, '..');
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  // pacing, from the data
  const data = JSON.parse(fs.readFileSync(path.join(ROOT, 'data/stories/jews/1207bc.json'), 'utf8'));
  for (const [r, beats] of [['opener', data.transitionIn.beats], ['play', data.play.beats]]){
    const pa = beats.map(b => b.pauseAfter), long = pa.filter(x => x > 800);
    ok(r + ' gaps after lines are short (0.4-0.8 s) except a few chapter breaths <= 2 s: ' + JSON.stringify([...new Set(pa)]) + ', ' + long.length + ' long', pa.every(x => x >= 400 && x <= 2000) && long.length <= 4 && pa.filter(x => x <= 800).length >= beats.length - 4);
    ok(r + ' reading time when the voice is off is ~2.5 words/s, min 2 s', beats.every(b => { const c = b.steps.find(x => x.type === 'caption'); const w = c.text.split(/\s+/).length; return b.duration >= 2000 && Math.abs(b.duration - Math.max(2000, Math.round(w / 2.5 * 10) * 100)) <= 100; }));
  }
  const b = await chromium.launch({args: ['--autoplay-policy=user-gesture-required']});
  for (const [name, vw, vh, mobile] of [['mobile', 390, 844, true], ['desktop', 1280, 800, false]]){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    // narrator clips: play-03 fails (network error), play-04 stalls forever
    const hung = [];
    await p.route(/assets\/narration\/jews-1207-play-03\.mp3/, r => r.abort('failed'));
    await p.route(/assets\/narration\/jews-1207-play-04\.mp3/, r => { hung.push(r); });
    const tap = async (x, y) => mobile ? p.touchscreen.tap(x, y) : p.mouse.click(x, y);
    const tapSel = async sel => { const q = await p.evaluate(s => { const r = document.querySelector(s).getBoundingClientRect(); return [r.left + r.width / 2, r.top + r.height / 2]; }, sel); return tap(q[0], q[1]); };
    const P = () => p.evaluate(() => __app.play);
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(800);
      await p.evaluate(() => { const b = document.getElementById('playbtn') || document.querySelector('[data-play], #play'); });
      await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(500);
      await p.evaluate(() => document.getElementById('gostory').scrollIntoView({block: 'center'}));
      mobile ? await p.tap('#gostory') : await p.click('#gostory');
      await p.waitForTimeout(2500);
      // a spot on the picture away from the subtitles and controls
      const spot = await p.evaluate(() => { const v = document.getElementById('vp').getBoundingClientRect(); return [v.left + v.width * .5, v.top + v.height * .3]; });
      let pl = await P();
      ok(name + ' film runs ' + JSON.stringify(pl), pl && !pl.paused);
      // a tap on the film never pauses or plays; it only shows the controls
      for (let k = 0; k < 3; k++){ await tap(...spot); await p.waitForTimeout(250); }
      pl = await P();
      ok(name + ' taps on the film do not pause ' + JSON.stringify(pl), !pl.paused);
      await p.evaluate(() => new Promise(r => setTimeout(r, __app.IDLE_MS + 600)));
      const idle = await p.evaluate(() => document.body.classList.contains('idle'));
      await tap(...spot); await p.waitForTimeout(200);
      pl = await P();
      ok(name + ' with the controls hidden (' + idle + ') a tap shows them and keeps playing', idle && !pl.paused && !(await p.evaluate(() => document.body.classList.contains('idle'))));
      // paused with the button: a tap on the film does not resume
      await tapSel('#cappp'); await p.waitForTimeout(200);
      ok(name + ' the pause button pauses', (await P()).paused);
      await tap(...spot); await p.waitForTimeout(250); await tap(...spot); await p.waitForTimeout(250);
      ok(name + ' while paused, taps on the film do not resume', (await P()).paused);
      await tapSel('#cappp'); await p.waitForTimeout(200);
      ok(name + ' the button plays again', !(await P()).paused);
      if (!mobile){ await p.keyboard.press('Space'); await p.waitForTimeout(150); const a1 = (await P()).paused; await p.keyboard.press('Space'); await p.waitForTimeout(150);
        ok(name + ' Space pauses and plays', a1 && !(await P()).paused); }
      // a tap outside the film (inline map, if any) never pauses either: covered in test-cine
      // taps on subtitles and buttons do not toggle
      await p.mouse.move(vw / 2, vh / 3); await p.mouse.move(vw / 2 + 3, vh / 3 + 2); await p.waitForTimeout(300);
      await tapSel('#captext'); await p.waitForTimeout(200);
      ok(name + ' tap on the subtitle does not pause', !(await P()).paused);
      const cc0 = await p.evaluate(() => __app.cc);
      await tapSel('#capcc'); await p.waitForTimeout(200);
      ok(name + ' tap on CC toggles subtitles, not the film', !(await P()).paused && (await p.evaluate(() => __app.cc)) !== cc0);
      await tapSel('#capcc'); await p.waitForTimeout(200);
      // the phone stops the clip (call, other app): the film does not pause and the line finishes
      await p.evaluate(() => { __app.playStop(false); }); await p.waitForTimeout(1500);
      await p.evaluate(() => __app.playStart('play', 0)); await p.waitForTimeout(2500);
      await p.evaluate(() => __app.seek(1)); await p.waitForTimeout(1500);
      await p.evaluate(() => { const a = __app.audioEl; if (a) a.pause(); });
      await p.waitForFunction(() => __app.play && __app.play.i >= 2, null, {timeout: 30000}).catch(() => {});
      pl = await P();
      ok(name + ' clip paused by the system: the film goes on ' + JSON.stringify(pl), pl.i >= 2 && !pl.paused);
      // a failed clip (beat 4 = play-03) and a stalled one (beat 5 = play-04): skipped, the film goes on, never paused
      await p.evaluate(() => __app.seek(3)); 
      const t0 = Date.now();
      await p.waitForFunction(() => __app.play && __app.play.i >= 5, null, {timeout: 40000}).catch(() => {});
      pl = await P(); const sk = await p.evaluate(() => __app.audioSkips);
      ok(name + ' failed and stalled clips are skipped, not paused: ' + JSON.stringify(pl) + ' skips ' + sk + ' in ' + Math.round((Date.now() - t0) / 1000) + ' s', pl.i >= 5 && !pl.paused && sk >= 2);
    } catch (e) { ok(name + ' ran: ' + e.message.split('\n')[0], false); }
    hung.forEach(r => r.abort().catch(() => {}));
    await ctx.close();
  }
  await b.close();
  notes.forEach(n => console.log(n));
  if (errs.length) console.log('ERRORS\n' + errs.join('\n'));
  const fail = notes.filter(n => n.startsWith('FAIL')).length + errs.length;
  console.log(fail ? 'FAILED ' + fail : 'ALL PASS ' + notes.length);
  process.exit(fail ? 1 : 0);
})();
