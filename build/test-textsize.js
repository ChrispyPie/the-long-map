// Text-size selector (A− A A+ A++): shown on the first screen above the intro and in the header,
// remembered in localStorage 'tlm.textsize' and applied before first paint, scales reading text,
// and never makes the page wider than the screen. Film taps still only show the controls.
// Usage: node build/test-textsize.js [url] [noshots]; SHOTS=dir for textsize_*.png screenshots.
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
const VIEWS = [[320,568,1],[360,640,1],[390,844,1],[844,390,1],[1280,800,0],[1920,1080,0]];
const SIZES = {s: .9, m: 1, l: 1.2, xl: 1.4};
(async () => {
  const notes = [], errs = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  const b = await chromium.launch({args: ['--autoplay-policy=user-gesture-required']});
  const fit = p => p.evaluate(() => {
    const W = document.documentElement.clientWidth, sw = document.documentElement.scrollWidth;
    const wide = [...document.querySelectorAll('body *')].filter(e => { if (e.closest('svg')) return false; const q = e.getBoundingClientRect(); return q.width > 0 && q.right > W + .5 && getComputedStyle(e).position !== 'fixed'; }).slice(0, 3).map(e => e.tagName + '.' + e.className);
    return {W, sw, iw: innerWidth, wide};
  });
  // base sizes at "m" for the ratio checks
  let base = null;
  for (const [vw, vh, mobile] of VIEWS){
    const name = vw + 'x' + vh;
    for (const ts of Object.keys(SIZES)){
      const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 1, isMobile: !!mobile, hasTouch: !!mobile});
      await ctx.addInitScript(t => { if (!sessionStorage.getItem('tsinit')){ sessionStorage.setItem('tsinit', 1); localStorage.setItem('tlm.textsize', t); localStorage.setItem('tlm.voice', 'off'); localStorage.setItem('tlm.snd', 'off'); } }, ts);
      const p = await ctx.newPage();
      p.on('pageerror', e => errs.push(name + ' ' + ts + ' pageerror: ' + e.message));
      p.on('console', m => { if (m.type() === 'error') errs.push(name + ' ' + ts + ': ' + m.text()); });
      const tap = s => mobile ? p.tap(s) : p.click(s);
      try {
        await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForTimeout(700);
        const n = name + ' ' + ts;
        // the selector is on the first screen, above the intro notice, with the saved size pressed
        const sel = await p.evaluate(() => {
          const g = document.querySelector('#intro > .ts'), q = g.getBoundingClientRect(), nq = document.getElementById('notice').getBoundingClientRect(), bq = document.getElementById('begin').getBoundingClientRect();
          const btns = [...g.querySelectorAll('button')];
          return {ts: document.documentElement.getAttribute('data-ts') || 'm', box: [q.left, q.top, q.right, q.bottom].map(Math.round), above: q.bottom <= nq.top + 1, inScreen: q.top >= 0 && q.left >= 0 && q.right <= innerWidth,
            pressed: btns.filter(x => x.getAttribute('aria-pressed') === 'true').map(x => x.dataset.ts), labels: btns.every(x => /text/i.test(x.getAttribute('aria-label') || '')), big: btns.every(x => x.getBoundingClientRect().width >= 40 && x.getBoundingClientRect().height >= 40),
            group: g.getAttribute('role') === 'group' && !!g.getAttribute('aria-label'), begin: bq.top > 0 && bq.bottom <= innerHeight, intro: !document.getElementById('intro').hidden};
        });
        ok(n + ' selector above the intro, saved size applied ' + JSON.stringify(sel), sel.intro && sel.ts === ts && sel.above && sel.inScreen && sel.pressed.join() === ts && sel.labels && sel.big && sel.group);
        ok(n + ' Begin adventure fully on screen', sel.begin);
        let f = await fit(p);
        ok(n + ' intro: no sideways scroll ' + JSON.stringify(f), f.sw <= f.W && f.iw === vw && !f.wide.length);
        const fs = await p.evaluate(() => { const g = s => parseFloat(getComputedStyle(document.querySelector(s)).fontSize); return {nlead: g('.nlead'), nseries: g('.nseries p'), nsmall: g('.nsmall')}; });
        if (ts === 'm' && !base) base = {};
        if (ts === 'm') base[name] = fs;
        else if (base && base[name]) ok(n + ' intro text scaled x' + SIZES[ts] + ' ' + JSON.stringify(fs), Object.keys(fs).every(k => Math.abs(fs[k] / base[name][k] - SIZES[ts]) < .02));
        if (ts === 'm') ok(n + ' intro lead text at least 18px by default (' + fs.nlead + ')', fs.nlead >= 18);
        if (shots && vw === 390) await p.screenshot({path: D + '/textsize_intro_' + ts + '.png'});
        // into the map: header selector, no sideways scroll, fact box and labels scaled
        await tap('#begin'); await p.waitForTimeout(3800);
        f = await fit(p);
        ok(n + ' map page: no sideways scroll ' + JSON.stringify(f), f.sw <= f.W && f.iw === vw && !f.wide.length);
        const hs = await p.evaluate(() => { const g = document.querySelector('header > .ts'), q = g.getBoundingClientRect(); return {shown: q.width > 0 && q.top >= 0 && q.right <= innerWidth + .5, pressed: g.querySelector('[aria-pressed="true"]').dataset.ts,
          ev: parseFloat(getComputedStyle(document.querySelector('#ev p, #ev .txt, #ev')).fontSize)}; });
        ok(n + ' header selector shown, same size pressed ' + JSON.stringify(hs), hs.shown && hs.pressed === ts);
        // 3) change size from the header, persists across reload (only on one size per view to keep it quick)
        if (ts === 'm'){
          await p.evaluate(() => document.querySelector('header > .ts').scrollIntoView({block: 'center'}));
          await tap('header > .ts button[data-ts="l"]'); await p.waitForTimeout(200);
          const c = await p.evaluate(() => ({ts: document.documentElement.getAttribute('data-ts'), ls: localStorage.getItem('tlm.textsize'), both: [...document.querySelectorAll('.ts button[aria-pressed="true"]')].map(x => x.dataset.ts).join()}));
          ok(n + ' tapping A+ sets large, saved, both selectors in sync ' + JSON.stringify(c), c.ts === 'l' && c.ls === 'l' && c.both === 'l,l');
          await p.reload({waitUntil: 'networkidle'}); await p.waitForTimeout(500);
          ok(n + ' size remembered after reload', await p.evaluate(() => document.documentElement.getAttribute('data-ts') === 'l' && getComputedStyle(document.documentElement).getPropertyValue('--ts').trim() === '1.2'));
          await tap('header > .ts button[data-ts="m"]'); await p.waitForTimeout(150);
          ok(n + ' back to normal removes the attribute', await p.evaluate(() => !document.documentElement.hasAttribute('data-ts') && localStorage.getItem('tlm.textsize') === 'm'));
        }
        // 4) film at the largest size: subtitles bigger, inside the picture, not under the controls; tap does not pause
        if (ts === 'xl'){
          await p.evaluate(() => __app.showStep(9)); await p.waitForTimeout(1200);
          await p.evaluate(() => document.getElementById('playbtn').scrollIntoView({block: 'center'}));
          await tap('#playbtn'); await p.waitForTimeout(2200);
          await p.evaluate(() => __app.seek(2)); await p.waitForTimeout(2600);
          await p.evaluate(() => document.body.classList.remove('idle'));
          const c = await p.evaluate(() => { const t = document.getElementById('captext'), q = t.getBoundingClientRect(), r = document.querySelector('#cap .crow').getBoundingClientRect(), vp = document.getElementById('vp').getBoundingClientRect();
            const fs = parseFloat(getComputedStyle(t).fontSize); __ts.set('m'); const fm = parseFloat(getComputedStyle(t).fontSize); __ts.set('xl');
            return {fs, ratio: +(fs / fm).toFixed(3), box: [q.left, q.top, q.right, q.bottom].map(Math.round), crow: [r.left, r.top, r.right, r.bottom].map(Math.round),
              inside: q.left >= vp.left - .5 && q.right <= vp.right + .5 && q.top >= vp.top && q.bottom <= vp.bottom, overCrow: q.left < r.right && q.right > r.left && q.top < r.bottom && q.bottom > r.top,
              crowIn: r.left >= 0 && r.right <= innerWidth + .5 && r.bottom <= innerHeight + .5, half: q.height <= innerHeight * .5, sw: document.documentElement.scrollWidth, W: document.documentElement.clientWidth}; });
          ok(n + ' film: subtitles x1.4 (' + c.fs + 'px), inside the picture, clear of the controls ' + JSON.stringify(c), Math.abs(c.ratio - 1.4) < .02 && c.inside && !c.overCrow && c.crowIn && c.half && c.sw <= c.W);
          if (shots && vw === 390) await p.screenshot({path: D + '/textsize_film_xl.png'});
          if (mobile) await p.touchscreen.tap(Math.round(vw / 2), Math.round(vh * .35)); else await p.mouse.click(Math.round(vw / 2), Math.round(vh * .35));
          await p.waitForTimeout(250);
          const t = await p.evaluate(() => ({idle: document.body.classList.contains('idle'), paused: __app.play && __app.play.paused, open: __app.open}));
          ok(n + ' film: tap only shows the controls, keeps playing ' + JSON.stringify(t), !t.idle && t.paused === false && t.open === null);
        }
      } catch (e) { ok(name + ' ' + ts + ' run: ' + e.message.split('\n')[0], false); }
      await ctx.close();
    }
  }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  console.log(notes.filter(n => n.startsWith('FAIL')).length || errs.length ? 'SOME FAILED' : 'ALL PASS', notes.length);
})();
