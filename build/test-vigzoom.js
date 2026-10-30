// Vignette pictures enlarge on a tap and shrink on the next one (or a tap beside them, or Esc) without
// touching the player: the controls stay as they were and the narration keeps going. An enlarged picture
// fits the free picture (below the year, above the subtitles); when its time is up it fades out like a card.
// Review mode: a tap on the review tag copies it ('Kopierat ✓'), with a fallback when navigator.clipboard
// is missing, and it neither brings up the controls nor pauses.
// Usage: node build/test-vigzoom.js [url]
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8852/';
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const b = await chromium.launch();
  for (const [name, vw, vh, mobile] of [['phone', 390, 844, true], ['phone-small', 360, 640, true], ['phone-landscape', 844, 390, true], ['desktop', 1280, 800, false]]){
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: mobile, hasTouch: mobile});
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], {origin: new URL(url).origin});
    await ctx.addInitScript(() => { localStorage.setItem('tlm.notice.v1', 'seen'); localStorage.setItem('tlm.snd', 'off'); localStorage.setItem('tlm.review', '1'); localStorage.setItem('tlm.ctlhint', '9'); });
    const p = await ctx.newPage();
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    // desktop: the mouse moving onto a spot brings the controls up by design, so a test click first moves there and
    // puts the controls back as they were; the click itself is what is checked
    const tap = async (x, y) => { if (mobile) return p.touchscreen.tap(x, y); const was = await p.evaluate(() => document.body.classList.contains('idle'));
      await p.mouse.move(x, y); await p.waitForTimeout(40); if (was) await p.evaluate(() => __app.ctlHide()); return p.mouse.click(x, y); };
    const R = sel => p.evaluate(s => { const e = document.querySelector(s); if (!e || !e.offsetHeight) return null; const r = e.getBoundingClientRect(); return [r.left, r.top, r.right, r.bottom].map(Math.round); }, sel);
    const st = () => p.evaluate(() => ({idle: document.body.classList.contains('idle'), paused: !!(__app.play && __app.play.paused), zoom: document.getElementById('vig').classList.contains('zoom'), hidden: document.getElementById('vig').hidden, i: __app.play && __app.play.i}));
    const mid = r => [(r[0] + r[2]) / 2, (r[1] + r[3]) / 2];
    const waitVig = () => p.waitForFunction(() => { const e = document.getElementById('vig'); return !e.hidden && e.classList.contains('in') && e.style.visibility !== 'hidden'; }, null, {timeout: 10000});
    try {
      await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(600);
      await p.evaluate(() => __app.showStep(0)); await p.waitForTimeout(400);
      await p.evaluate(() => document.getElementById('gostory').scrollIntoView({block: 'center'}));
      mobile ? await p.tap('#gostory') : await p.click('#gostory');
      await p.waitForFunction(() => __app.cine && __app.cine.full && document.getElementById('captext').offsetHeight > 0, null, {timeout: 8000});
      await p.evaluate(async () => { __app.setVoice(false); await __app.playStop(false); const s = (await (await fetch('data/stories/jews/story.json')).json()).stops.findIndex(s => s.year === -1207); await __app.go(s); await __app.playStart('play', 34); });
      await waitVig(); await p.waitForTimeout(800);
      if (!mobile){ await p.mouse.move(2, 2); await p.waitForTimeout(900); }
      await p.evaluate(() => __app.ctlHide());
      const card = await R('#vig'), beat = (await st()).i;
      // tap the picture: enlarged, controls untouched, still playing
      await tap(...mid(card)); await p.waitForTimeout(500);
      let s = await st(); const big = await R('#vig'), f = await p.evaluate(() => __app.filmFree(true)), vp = await R('#vp');
      ok(`${name} tap enlarges the picture (${card[2] - card[0]}x${card[3] - card[1]} -> ${big[2] - big[0]}x${big[3] - big[1]})`, s.zoom && (big[2] - big[0]) * (big[3] - big[1]) > 1.25 * (card[2] - card[0]) * (card[3] - card[1]));
      ok(name + ' enlarged picture fits the screen, clear of the year and the subtitles ' + JSON.stringify({big, vp, top: f.top|0, bot: f.bot|0}), big[0] >= vp[0] && big[2] <= vp[2] && big[1] - vp[1] >= f.top - 1 && big[3] - vp[1] <= f.bot + 1);
      ok(name + ' enlarged picture keeps the small card\'s top edge (' + card[1] + ' -> ' + big[1] + ')', Math.abs(big[1] - card[1]) <= 2);
      ok(name + ' enlarged picture uses the room below it: full width or down to the subtitles', big[2] - big[0] >= (vp[2] - vp[0]) - 16 || big[3] - vp[1] >= f.bot - 16);
      ok(name + ' tap on the picture leaves the controls hidden and keeps playing ' + JSON.stringify(s), (s.idle || !mobile) && !s.paused);
      const kb = await p.evaluate(() => getComputedStyle(document.querySelector('#vig img')).animationName);
      ok(name + ' no slow pan while enlarged (whole picture visible): ' + kb, kb === 'none');
      const subs = await R('#captext'); ok(name + ' subtitles still visible above the dimmed map', !!subs && await p.evaluate(() => { const t = document.getElementById('captext').getBoundingClientRect(), e = document.elementFromPoint(t.left + t.width / 2, t.top + t.height / 2); return !!(e && e.closest('#cap')); }));
      await p.screenshot({path: `/tmp/vz-${name}-zoom.png`});
      // tap again: back to the card
      await tap(...mid(big)); await p.waitForTimeout(500);
      s = await st(); const back = await R('#vig');
      ok(name + ' second tap shrinks it back to the card', !s.zoom && Math.abs((back[2] - back[0]) - (card[2] - card[0])) <= 3 && (s.idle || !mobile) && !s.paused);
      // with the controls up, tapping the picture still only zooms (controls stay up)
      await p.evaluate(() => __app.wake()); await tap(...mid(back)); await p.waitForTimeout(400);
      s = await st(); ok(name + ' with the controls up, a tap on the picture zooms and leaves them up', s.zoom && !s.idle);
      // a tap beside the enlarged picture shrinks it and leaves the controls alone
      const b2 = await R('#vig'); const beside = b2[1] - vp[1] > 30 ? [vp[0] + 12, b2[1] - 10] : [b2[0] > vp[0] + 30 ? b2[0] - 10 : b2[2] + 10, (b2[1] + b2[3]) / 2];
      await tap(...beside); await p.waitForTimeout(400);
      s = await st(); ok(name + ' tap beside the enlarged picture shrinks it, controls stay', !s.zoom && !s.idle && !s.paused);
      if (!mobile){ await tap(...mid(await R('#vig'))); await p.waitForTimeout(300); await p.keyboard.press('Escape'); await p.waitForTimeout(300); s = await st(); ok(name + ' Esc shrinks the picture and does not end the film', !s.zoom && (await p.evaluate(() => !!__app.play))); }
      // review mode adds no extra position tag above the subtitles any more (the time is in the player, the #line in the subtitle)
      ok(name + ' no review tag above the subtitles', !(await p.evaluate(() => document.getElementById('revtag'))));
      // the picture's time runs out while it is enlarged: it closes, and the next one (most lines have one now) is a normal card
      await p.evaluate(() => __app.seek(34)); await waitVig(); await p.waitForTimeout(700);
      await tap(...mid(await R('#vig'))); await p.waitForTimeout(400);
      const zi = (await st()).i;
      await p.evaluate(() => { __app.speed = 4; });
      await p.waitForFunction(zi => !document.getElementById('vig').classList.contains('zoom') && __app.play && __app.play.i !== zi, zi, {timeout: 60000});
      s = await st(); ok(`${name} enlarged picture closes by itself when its time is up (beat ${zi} -> ${s.i})`, !s.zoom && !(await p.evaluate(() => document.getElementById('vp').classList.contains('vigzoom'))) && !s.paused);
      await p.evaluate(() => { __app.speed = 1; __app.seek(34); }); await waitVig(); await p.waitForTimeout(700);
      ok(name + ' next picture comes as a normal card', !(await st()).zoom);
      // a jump (Scenes / next line) while enlarged closes it at once
      await tap(...mid(await R('#vig'))); await p.waitForTimeout(300);
      await p.evaluate(() => __app.seek(36)); await p.waitForTimeout(200);
      s = await st(); ok(name + ' a jump while enlarged closes it at once', !s.zoom && s.i === 36 && !(await p.evaluate(() => document.getElementById('vp').classList.contains('vigzoom'))));
    } catch(e){ errs.push(name + ': ' + e.message); }
    await ctx.close();
  }
  await b.close();
  for (const n of notes) console.log(n); for (const e of errs) console.log('ERROR ' + e);
  const f = notes.filter(n => n.startsWith('FAIL')).length + errs.length;
  console.log(f ? 'FAILED ' + f : 'ALL PASS ' + notes.filter(n => n.startsWith('PASS')).length); process.exit(f ? 1 : 0);
})();
