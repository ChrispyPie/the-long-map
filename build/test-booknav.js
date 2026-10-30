// The book (chapters, scenes, index), the fixed subtitle box, the time / line references and shared links.
// Usage: node build/test-booknav.js [url] [noshots]; SHOTS=dir for screenshots.
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
(async () => {
  const b = await chromium.launch();
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  for (const [name, vw, vh, mobile] of [['mobile', 412, 915, true], ['desktop', 1280, 800, false]]) {
    const ctx = await b.newContext({viewport: {width: vw, height: vh}, deviceScaleFactor: 2, isMobile: mobile, hasTouch: mobile});
    await ctx.grantPermissions(['clipboard-read', 'clipboard-write'], {origin: new URL(url).origin});
    await ctx.addInitScript(() => localStorage.setItem('tlm.notice.v1', 'seen'));
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type() === 'error' && !/Failed to load resource/.test(m.text())) errs.push(name + ': ' + m.text()); });
    p.on('pageerror', e => errs.push(name + ' pageerror: ' + e.message));
    const shot = async f => { if (shots && mobile) await p.screenshot({path: D + '/' + f + '.png'}); };
    const tap = async sel => { await p.evaluate(s => { const e = document.querySelector(s); if (document.body.classList.contains('idle') && e && e.closest('#cap')) __app.wake(); }, sel); return mobile ? p.tap(sel) : p.click(sel); };
    const clip = () => p.evaluate(() => navigator.clipboard.readText().catch(() => null));
    try {
    await p.goto(url, {waitUntil: 'networkidle'}); await p.waitForFunction(() => window.__app && __app.mode === 'stop');
    const k4 = await p.evaluate(() => __app.parts()[3].k), k3 = await p.evaluate(() => __app.parts()[2].k);
    await p.evaluate(k => __app.go(k), k4); await p.waitForTimeout(1500);
    ok(name + ' intro button label', /^▶ Play Chapter 4 intro · \d+ min$/.test(await p.textContent('#gostory')));
    ok(name + ' book button on the chapter page', await p.isVisible('#gobook'));
    await tap('#gostory'); await p.waitForFunction(() => __app.play && __app.cine); await p.waitForTimeout(1500);
    await p.evaluate(() => __app.playPause(true));
    // 1) the controls stay put from line to line; the box is as tall as the tallest line
    const ys = [];
    for (const i of [0, 1, 2, 3, 4, 5, 6, 7, 8]) { await p.evaluate(i => { __app.seek(i); __app.playPause(true); __app.wake(); }, i); await p.waitForTimeout(250);
      ys.push(await p.evaluate(() => ({y: Math.round(document.querySelector('#cap .crow').getBoundingClientRect().top), h: Math.round(document.getElementById('capsub').getBoundingClientRect().height), H: Math.round(__app.capH)}))); }
    await p.evaluate(() => { __app.playStop(false); }); await p.waitForTimeout(900);
    await p.evaluate(k => __app.bookPlay(k, 'play', 30), k4); await p.waitForFunction(() => __app.play && __app.play.reel === 'play'); await p.waitForTimeout(900);
    for (const i of [30, 33, 40, 50, 56, 60, 67]) { await p.evaluate(i => { __app.seek(i); __app.playPause(true); __app.wake(); }, i); await p.waitForTimeout(250);
      ys.push(await p.evaluate(() => ({y: Math.round(document.querySelector('#cap .crow').getBoundingClientRect().top), h: Math.round(document.getElementById('capsub').getBoundingClientRect().height), H: Math.round(__app.capH)}))); }
    const yv = ys.map(o => o.y), hv = ys.map(o => o.h);
    ok(name + ' controls keep their y across lines ' + JSON.stringify([...new Set(yv)]), Math.max(...yv) - Math.min(...yv) <= 1);
    ok(name + ' subtitle box has one fixed height ' + JSON.stringify([...new Set(hv)]), Math.max(...hv) - Math.min(...hv) <= 1 && hv[0] > 20);
    ok(name + ' controls fit on one row', await p.evaluate(() => { const r = document.querySelector('#cap .crow'); return r.scrollWidth <= r.clientWidth + 1 && [...r.children].every(c => c.getBoundingClientRect().top - r.children[0].getBoundingClientRect().top < 6 || c.offsetParent === null); }));
    // 2) references: chapter time and line number
    ok(name + ' time counter reads m:ss / m:ss', /^\d+:\d\d \/ \d+:\d\d$/.test(await p.textContent('#captime')));
    await tap('#captime'); await p.waitForTimeout(200);
    const tr = await clip();
    ok(name + ' time copy text ' + tr, /^The Long Map – Chapter 4 at \d+:\d\d https:\/\/thelongmap\.com\/\?ch=4&t=\d+$/.test(tr || ''));
    ok(name + ' Copied ✓ toast', await p.evaluate(() => !document.getElementById('toast').hidden && /Copied ✓/.test(document.getElementById('toast').textContent)));
    ok(name + ' toast offers "Report an error here"', await p.evaluate(() => { const t = document.querySelector('#toast .tbtn'); return !!t && /Report an error here/.test(t.textContent); }));
    { const X = 'https://x.com/intent/post?in_reply_to=2116194386589397340&text=';
      const rl = await p.evaluate(() => __app.reportFor(68)), rt = await p.evaluate(() => __app.reportFor()), rf = await p.evaluate(() => __app.reportNow());
      const dec = h => h && h.startsWith(X) ? decodeURIComponent(h.slice(X.length)) : null;
      ok(name + ' report for a line replies to the pinned post: ' + dec(rl), dec(rl) === 'Correction for Chapter 4, #line 68: https://thelongmap.com/?ch=4&line=68');
      ok(name + ' report for the time: ' + dec(rt), /^Correction for Chapter 4 at \d+:\d\d: https:\/\/thelongmap\.com\/\?ch=4&t=\d+$/.test(dec(rt) || '') && dec(rt).length < 120);
      ok(name + ' footer report link follows the moment', /^Correction for Chapter 4 at /.test(dec(rf) || ''));
      ok(name + ' footer "Report an error" is shown', await p.evaluate(() => !document.getElementById('report').hidden)); }
    await p.evaluate(() => __app.wake());
    await (mobile ? p.tap('#captext .lnum') : p.click('#captext .lnum')); await p.waitForTimeout(200);
    const lr = await clip();
    ok(name + ' line copy text ' + lr, /^The Long Map – Chapter 4, line #68: ".+" https:\/\/thelongmap\.com\/\?ch=4&line=68$/.test(lr || ''));
    ok(name + ' line badge matches the line', await p.textContent('#captext .lnum') === '#68');
    await p.evaluate(() => __app.seek(56)); await p.waitForTimeout(300); await p.evaluate(() => { __app.playPause(true); __app.wake(); });
    await p.waitForTimeout(300); await shot('booknav_player');
    // 3) the book opens on this chapter, pauses the film, flips, index, back closes it
    await p.evaluate(() => __app.playPause(false));
    await tap('#capbook'); await p.waitForTimeout(1300);
    let bk = await p.evaluate(() => ({...__app.book, paused: __app.play && __app.play.paused}));
    ok(name + ' book opens on Chapter 4 ' + JSON.stringify(bk), bk.open && bk.type === 'ch' && bk.k === k4 && bk.paused);
    ok(name + ' chapter page has title, years, summary, buttons, scenes', await p.evaluate(() => { const t = document.getElementById('bkpage').textContent;
      return /Chapter 4/.test(t) && /Israel and Judah/.test(t) && /930–841 BC/.test(t) && /Omri/.test(t) && /▶ Play chapter/.test(t) && /Resume at/.test(t) && /Read as fact boxes/.test(t) && /Explore the map/.test(t) && document.querySelectorAll('#bkpage ol.sc li').length === 7; }));
    ok(name + ' the scene playing is marked', await p.evaluate(() => /Jehu and Hazael/.test((document.querySelector('#bkpage ol.sc li.now') || {}).textContent || '')));
    const sc = await p.evaluate(() => [...document.querySelectorAll('#bkpage ol.sc li')].map(li => ({seen: li.classList.contains('seen'), tick: li.querySelector('.ok').textContent, m: li.querySelector('.m').textContent, op: getComputedStyle(li.querySelector('button')).opacity, now: li.classList.contains('now')})));
    const sec = m => { const [a, b] = m.split(':'); return +a * 60 + +b; };
    ok(name + ' scene start times ' + sc.map(c => c.m).join(' '), sc[0].m === '0:00' && sc.every((c, j) => !j || sec(c.m) > sec(sc[j - 1].m)));
    ok(name + ' passed scenes have a ✓ and are not greyed ' + sc.map(c => c.seen ? '✓' : '·').join(''), sc.filter(c => c.seen).length >= 5 && sc.every(c => (c.tick === '✓') === c.seen && c.op === '1') && !sc.find(c => c.now).seen);
    ok(name + ' seen scenes are stored', await p.evaluate(() => { const k = Object.keys(localStorage).find(x => x.startsWith('tlm.seen.')); return !!k && JSON.parse(localStorage.getItem(k)).length >= 5; }));
    ok(name + ' no chapter tick before every scene is done', await p.evaluate(() => !document.querySelector('#bkpage h2 .cok')));
    await shot('booknav_chapter');
    await p.keyboard.press('ArrowRight'); await p.waitForTimeout(800);
    bk = await p.evaluate(() => __app.book); ok(name + ' arrow flips to the coming-soon page', bk.type === 'soon');
    await p.keyboard.press('ArrowLeft'); await p.waitForTimeout(800);
    bk = await p.evaluate(() => __app.book); ok(name + ' arrow flips back', bk.k === k4);
    const pb = await p.evaluate(() => { const r = document.getElementById('bkpage').getBoundingClientRect(); return {x: r.left + r.width / 2, y: r.top + r.height * 0.3}; });
    await p.mouse.move(pb.x + 110, pb.y); await p.mouse.down(); await p.mouse.move(pb.x - 40, pb.y + 8, {steps: 5}); await p.mouse.move(pb.x - 110, pb.y + 10, {steps: 3}); await p.mouse.up(); await p.waitForTimeout(800);
    bk = await p.evaluate(() => __app.book); ok(name + ' swipe left turns the page', bk.type === 'soon');
    await p.mouse.move(pb.x - 110, pb.y); await p.mouse.down(); await p.mouse.move(pb.x + 110, pb.y, {steps: 6}); await p.mouse.up(); await p.waitForTimeout(800);
    bk = await p.evaluate(() => __app.book); ok(name + ' swipe right turns back', bk.k === k4);
    await (mobile ? p.tap('#bkribbon') : p.click('#bkribbon')); await p.waitForTimeout(800);
    bk = await p.evaluate(() => __app.book); ok(name + ' ribbon opens the index', bk.type === 'index' && bk.page === 0);
    ok(name + ' index: Book One intro and every chapter', await p.evaluate(() => { const li = [...document.querySelectorAll('#bkpage ul.ix > li')]; return li[0].classList.contains('bkintro') && /Book One intro/.test(li[0].textContent) && li.length === 6 && li[5].classList.contains('soon'); }));
    await p.click('#bkpage button[data-x="' + k3 + '"]'); await p.waitForTimeout(200);
    ok(name + ' accordion opens a chapter\'s scenes', await p.evaluate(k => { const b = document.getElementById('bkacc' + k); return !b.hidden && b.querySelectorAll('li').length === 7 && document.querySelector('button[data-x="' + k + '"]').getAttribute('aria-expanded') === 'true'; }, k3));
    await shot('booknav_index');
    await p.click('#bkpage button[data-x="' + k3 + '"]'); await p.waitForTimeout(150);
    ok(name + ' accordion closes again', await p.evaluate(k => document.getElementById('bkacc' + k).hidden, k3));
    await p.click('#bkpage ul.ix > li:nth-child(4) .pg'); await p.waitForTimeout(250);
    ok(name + ' Page › turns the page visibly', await p.evaluate(() => !!document.querySelector('.bkturn') || __app.book.turning));
    await p.waitForTimeout(700);
    bk = await p.evaluate(() => __app.book); ok(name + ' Page › lands on Chapter 3', bk.k === k3 && !bk.turning);
    await p.goBack(); await p.waitForTimeout(500);
    bk = await p.evaluate(() => ({...__app.book, paused: __app.play && __app.play.paused})); ok(name + ' Back closes the book and the film goes on', !bk.open && bk.paused === false && await p.isHidden('#bkwrap'));
    // ✕ and a tap beside the book
    await tap('#capbook'); await p.waitForTimeout(1300); await p.click('#bkx'); await p.waitForTimeout(400);
    ok(name + ' ✕ closes', !(await p.evaluate(() => __app.book.open)) && await p.evaluate(() => !history.state || !history.state.tlmBook));
    await tap('#capbook'); await p.waitForTimeout(1300); await p.mouse.click(3, Math.round(vh * 0.5)); await p.waitForTimeout(400);
    ok(name + ' tap outside closes', !(await p.evaluate(() => __app.book.open)));
    // a scene from the book plays from that scene (Qarqar, 853 BC = line 34)
    await tap('#capbook'); await p.waitForTimeout(1300);
    await p.click('#bkpage ol.sc li:nth-child(5) button'); await p.waitForTimeout(1500);
    let pl = await p.evaluate(() => __app.play);
    ok(name + ' scene tap plays from that scene ' + JSON.stringify(pl), pl && pl.reel === 'play' && pl.i === 33 && !(await p.evaluate(() => __app.book.open)));
    // another chapter's scene from the index
    await tap('#capbook'); await p.waitForTimeout(1300); await p.click('#bkribbon'); await p.waitForTimeout(800);
    await p.click('#bkpage button[data-x="' + k3 + '"]'); await p.click('#bkacc' + k3 + ' ol.sc li:nth-child(3) button'); await p.waitForFunction(k => __app.play && __app.cur === k, k3, {timeout: 9000}); await p.waitForTimeout(600);
    pl = await p.evaluate(() => ({...__app.play, ch: __app.chapters('play')}));
    ok(name + ' index scene plays Chapter 3 from that scene', pl.reel === 'play' && pl.i === pl.ch[1].i);
    // skip chapter intros: the gear switch, remembered; Play chapter then starts at the first scene
    await tap('#capset'); await p.waitForTimeout(150);
    ok(name + ' settings menu opens', await p.isVisible('#capmenu'));
    await p.click('#capmenu input'); await p.waitForTimeout(100);
    ok(name + ' skip intros is remembered', await p.evaluate(() => __app.skipIntro && localStorage.getItem('tlm.skipintro') === 'on'));
    await tap('#capbook'); await p.waitForTimeout(1300);
    ok(name + ' skip switch shows in the book, checked', await p.evaluate(() => { const c = document.querySelector('#bkpage input[data-skipintro]'); return c && c.checked; }));
    await p.click('#bkpage button[data-act="play"]'); await p.waitForTimeout(1500);
    pl = await p.evaluate(() => __app.play); ok(name + ' Play chapter skips the intro', pl && pl.reel === 'play' && pl.i === 0);
    await tap('#capbook'); await p.waitForTimeout(1300); await p.click('#bkpage input[data-skipintro]'); await p.click('#bkpage button[data-act="play"]'); await p.waitForTimeout(1500);
    pl = await p.evaluate(() => __app.play); ok(name + ' skip off: Play chapter starts with the intro', pl && pl.reel === 'intro' && pl.i === 0 && await p.evaluate(() => localStorage.getItem('tlm.skipintro') !== 'on'));
    await p.evaluate(() => __app.playStop(false)); await p.waitForTimeout(900);
    // header book button, and Esc
    await p.click('#bookbtn'); await p.waitForTimeout(1300);
    ok(name + ' header button opens the book', await p.evaluate(() => __app.book.open));
    await p.keyboard.press('Escape'); await p.waitForTimeout(400);
    ok(name + ' Esc closes', !(await p.evaluate(() => __app.book.open)));
    // the chapter tick: every scene of Chapter 3 watched
    await p.evaluate(() => __app.bookOpen(0)); await p.waitForTimeout(1300);
    await p.evaluate(k => { const keys = [...document.querySelectorAll('#bkacc' + k + ' button[data-act=scene]')].map(b => b.dataset.r + ':' + b.dataset.i); localStorage.setItem(__app.seenKey(__app.parts()[2].year), JSON.stringify(keys)); }, k3);
    await p.evaluate(() => __app.bookClose()); await p.waitForTimeout(500); await p.evaluate(() => __app.bookOpen(0)); await p.waitForTimeout(1300);
    ok(name + ' chapter tick when all its scenes are done', await p.evaluate(() => { const li = document.querySelectorAll('#bkpage ul.ix > li'); return !!li[3].querySelector('.cok') && !li[4].querySelector('.cok'); }));
    await p.evaluate(() => __app.bookClose()); await p.waitForTimeout(500);
    // 4) shared links
    for (const [q, want] of [['?ch=4&line=57', {r: 'play', i: 56}], ['?ch=4&t=525', null], ['?ch=4&line=i3&review=1', {r: 'intro', i: 2}]]) {
      await p.goto(url + q, {waitUntil: 'networkidle'}); await p.waitForFunction(() => window.__app && __app.deep, null, {timeout: 15000}); await p.waitForTimeout(400);
      const dp = await p.evaluate(() => ({deep: __app.deep, cur: __app.cur, vis: !document.getElementById('deep').hidden, search: location.search, play: __app.play}));
      ok(name + ' ' + q + ' opens Chapter 4 paused with a play prompt ' + JSON.stringify(dp), dp.cur === k4 && dp.vis && !dp.play && !/ch=/.test(dp.search) && (!/review/.test(q) || /review=1/.test(dp.search)) && (!want || (dp.deep.r === want.r && dp.deep.i === want.i)));
      if (q === '?ch=4&line=57') await shot('booknav_deeplink');
      await (mobile ? p.tap('#deepgo') : p.click('#deepgo')); await p.waitForFunction(() => __app.play, null, {timeout: 9000}); await p.waitForTimeout(600);
      pl = await p.evaluate(() => ({...__app.play, time: __app.time}));
      if (want) ok(name + ' ' + q + ' plays from that line', pl.reel === want.r && pl.i === want.i);
      else { const [a] = pl.time.split(' / '); const [m, s] = a.split(':').map(Number); ok(name + ' ?t=525 starts at the beat holding 8:45 (' + pl.time + ')', m * 60 + s <= 526 && m * 60 + s > 525 - 40); }
      if (/review/.test(q)) ok(name + ' review tag still works', /^Ch4 · opening #3 · \d+:\d\d$/.test(await p.evaluate(() => (document.getElementById('revtag') || {}).textContent || '')));
    }
    } catch(e){ ok(name + ' stopped: ' + e.message.split('\n').slice(0, 12).join(' | '), false); await p.screenshot({path: '/tmp/booknav_fail_' + name + '.png'}).catch(() => {}); }
    await ctx.close();
  }
  await b.close();
  notes.forEach(n => console.log(n)); errs.forEach(e => console.log('ERR ' + e));
  const fails = notes.filter(n => n.startsWith('FAIL')).length;
  console.log(fails || errs.length ? `${fails} FAIL, ${errs.length} errors` : 'ALL PASS');
  process.exit(fails || errs.length ? 1 : 0);
})();
