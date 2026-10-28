// Notice, opening book and cinematic mode. Usage: node build/test-cine.js [url] [noshots]; TS=s|m|l|xl for a saved text size; SHOTS=dir for screenshots.
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
(async () => {
  const b = await chromium.launch();
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  for (const [name, vw, vh, mobile, rm] of [['mobile',393,852,true,false],['desktop',1280,800,false,false],['mobile-reduced',393,852,true,true]]) {
    const ctx = await b.newContext({viewport:{width:vw,height:vh}, deviceScaleFactor:2, isMobile:mobile, hasTouch:mobile, reducedMotion: rm ? 'reduce' : 'no-preference'});
    if (process.env.TS) await ctx.addInitScript(t => localStorage.setItem('tlm.textsize', t), process.env.TS); // TS=xl runs the suite at a saved text size
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type()==='error') errs.push(name+': '+m.text()); });
    p.on('pageerror', e => errs.push(name+' pageerror: '+e.message));
    const sfx = mobile ? '' : '_desktop', shot = async f => { if (shots && (!rm || f.includes('reduced'))) await p.screenshot({path:D+'/'+f+'.png'}); };
    const tap = async sel => mobile ? p.tap(sel) : p.click(sel);
    await p.goto(url, {waitUntil:'networkidle'}); await p.waitForTimeout(900);
    // 1) notice on first visit
    ok(name+' notice shown on first visit', await p.evaluate(()=>!document.getElementById('intro').hidden && __intro.state==='notice'));
    ok(name+' notice says what it is and is not', await p.evaluate(()=>{ const t=document.getElementById('notice').textContent; return /What this is/.test(t) && /What this is not/.test(t) && /source/.test(t) && /approximate/.test(t) && /religious text/.test(t) && /modern conflicts/.test(t) && /final word/.test(t); }));
    ok(name+' notice fits the screen', await p.evaluate(()=>{ const r=document.getElementById('begin').getBoundingClientRect(); return r.bottom <= innerHeight && r.top > 0; }));
    if (!rm) await shot('cine_notice'+sfx);
    // series framing, title and per-book theme
    ok(name+' notice: Book One of a series, later books coming later', await p.evaluate(()=>{ const t=document.getElementById('notice').textContent; return /Book One/.test(t) && /Story of the Jews/.test(t) && /Book Two · Story of the Arabs/.test(t) && /Story of the Persians/.test(t) && (t.match(/Coming later/g)||[]).length===2 && !/History of the/.test(t); }));
    ok(name+' cover reads The Long Map / Book One / Story of the Jews', await p.evaluate(()=>[...document.querySelectorAll('.cover .front .frame div')].filter(d=>!d.children.length).map(d=>d.textContent.trim()).join('/')==='The Long Map/Book One/Story of the Jews'));
    ok(name+' header, title and OG say Story of the Jews', await p.evaluate(()=>document.getElementById('stitle').textContent==='Story of the Jews' && document.getElementById('sbook').textContent==='Book One' && document.title==='The Long Map · Story of the Jews' && /Story of the Jews/.test(document.querySelector('meta[property="og:title"]').content) && /Book Two/.test(document.querySelector('footer .fseries').textContent)));
    ok(name+' per-book accent from story.json', await p.evaluate(()=>document.documentElement.style.getPropertyValue('--accent').trim()==='#b8893a'));
    ok(name+' paper panels and leather buttons', await p.evaluate(()=>document.getElementById('ev').classList.contains('paper') && document.getElementById('pop').classList.contains('paper') && !!document.getElementById('torn')));
    // 2) the book (on phones it must stay inside the screen at every frame, with no sideways scroll)
    await p.evaluate(()=>{ window.__bk=[]; const t0=performance.now(); const f=()=>{ const st=document.getElementById('intro').className; if(!/reveal/.test(st)) document.querySelectorAll('.book, .cover .front, .cover .back').forEach(e=>{ const q=e.getBoundingClientRect(); if(q.width) __bk.push([q.left,q.right]); }); __bk.push([0,0,document.documentElement.scrollWidth]); if(performance.now()-t0<3600) requestAnimationFrame(f); }; requestAnimationFrame(f); });
    await tap('#begin');
    if (!rm){
      await p.waitForTimeout(850); if (mobile) await shot('cine_book');
      ok(name+' book opening', await p.evaluate(()=>['opening','open'].includes(__intro.state) && document.getElementById('intro').classList.contains('open')));
      await p.waitForTimeout(800); if (mobile) await shot('cine_book_open');
      await p.waitForTimeout(1900);
      const bk = await p.evaluate(()=>{ const W=innerWidth; let l=1e9,r=-1e9,sw=0; __bk.forEach(([a,b,c])=>{ if(c) sw=Math.max(sw,c); else { l=Math.min(l,a); r=Math.max(r,b); } }); return {W,l:Math.round(l),r:Math.round(r),sw,n:__bk.length}; });
      ok(name+' book stays inside the screen while it opens '+JSON.stringify(bk), bk.l>=0 && bk.r<=bk.W && bk.sw<=bk.W);
    } else {
      await p.waitForTimeout(300);
      ok(name+' reduced motion: no book, notice gone at once', await p.evaluate(()=>__intro.state==='hidden' && !document.getElementById('intro').classList.contains('booking')));
    }
    ok(name+' map revealed after Begin', await p.evaluate(()=>document.getElementById('intro').hidden));
    ok(name+' choice remembered', await p.evaluate(()=>localStorage.getItem('tlm.notice.v1')==='seen'));
    await p.reload({waitUntil:'networkidle'}); await p.waitForTimeout(700);
    ok(name+' returning visitor skips notice', await p.evaluate(()=>document.getElementById('intro').hidden));
    await p.evaluate(()=>document.getElementById('about').scrollIntoView()); await tap('#about'); await p.waitForTimeout(200);
    ok(name+' About reopens the notice', await p.evaluate(()=>!document.getElementById('intro').hidden && __intro.state==='notice'));
    await tap('#begin'); await p.waitForTimeout(rm ? 300 : 3800);
    ok(name+' notice closes again', await p.evaluate(()=>document.getElementById('intro').hidden));
    // 3) cinematic mode
    await p.evaluate(()=>__app.showStep(9)); await p.waitForTimeout(1200);
    const rect0 = await p.evaluate(()=>{ const r=document.getElementById('vp').getBoundingClientRect(); return [r.width, r.height]; });
    await p.evaluate(()=>document.getElementById('playbtn').scrollIntoView({block:'center'}));
    await tap('#playbtn');
    await p.waitForTimeout(rm ? 150 : 300);
    const mid = await p.evaluate(()=>{ const r=document.getElementById('vp').getBoundingClientRect(); return [r.width, r.height]; });
    await p.waitForTimeout(1400);
    let c = await p.evaluate(()=>({cine: __app.cine, vp: (r=>[r.left,r.top,r.width,r.height])(document.getElementById('vp').getBoundingClientRect()), W: innerWidth, H: innerHeight,
      hdr: getComputedStyle(document.querySelector('header')).opacity, ev: getComputedStyle(document.getElementById('ev')).opacity, tl: getComputedStyle(document.querySelector('.timeline')).opacity,
      xp: getComputedStyle(document.getElementById('xp')).display, cap: !document.getElementById('cap').hidden && document.getElementById('cap').parentNode.id, play: __app.play, year: document.getElementById('cyear').textContent }));
    ok(name+' film: map fills the screen '+JSON.stringify(c.vp), c.cine && c.cine.full && Math.abs(c.vp[2]-c.W)<2 && Math.abs(c.vp[3]-c.H)<2 && c.vp[0]===0 && c.vp[1]===0);
    if (!rm) ok(name+' film: zoom grows smoothly (mid '+mid.map(Math.round)+' from '+rect0.map(Math.round)+')', mid[1] > rect0[1] && mid[1] < c.H - 1 || mid[0] > rect0[0] && mid[0] < c.W - 1);
    else ok(name+' reduced motion: fullscreen at once ('+mid.map(Math.round)+')', Math.abs(mid[1]-c.H) < 2);
    ok(name+' film: menus, panels and progress pill hidden', c.hdr==='0' && c.ev==='0' && c.tl==='0' && c.xp==='none');
    ok(name+' film: subtitles inside the picture with year '+c.year, c.cap==='vp' && /BC/.test(c.year));
    ok(name+' film: playing '+JSON.stringify(c.play), c.play && !c.play.paused);
    ok(name+' film: caption keeps its source badge', await p.evaluate(()=>!!document.querySelector('#captext .cb') && /Sources|Scene-setting/.test(document.getElementById('capsrc').textContent)));
    // wait into beat 2 (a migration) for the mid-transition picture
    await p.evaluate(()=>__app.seek(2)); await p.waitForTimeout(2600);
    if (mobile) await shot(rm ? 'cine_film_reduced' : 'cine_film'); else await shot('cine_film_desktop');
    // controls auto-hide
    await p.waitForTimeout(3300);
    c = await p.evaluate(()=>({idle: document.body.classList.contains('idle'), op: getComputedStyle(document.querySelector('#cap .crow')).opacity, paused: __app.play.paused}));
    ok(name+' controls auto-hide after a few seconds '+JSON.stringify(c), c.idle && !c.paused);
    if (!mobile){ await p.mouse.move(300, 300); await p.mouse.move(320, 310); await p.waitForTimeout(100);
      ok(name+' mouse move brings controls back, keeps playing', await p.evaluate(()=>!document.body.classList.contains('idle') && !__app.play.paused)); await p.waitForTimeout(3300); }
    // a tap only shows the controls, it never pauses; pause only with the button
    if (mobile) await p.touchscreen.tap(200, 300); else await p.mouse.click(640, 300);
    await p.waitForTimeout(250);
    c = await p.evaluate(()=>({idle: document.body.classList.contains('idle'), paused: __app.play.paused, open: __app.open}));
    ok(name+' tap shows controls and keeps playing '+JSON.stringify(c), !c.idle && !c.paused && c.open === null);
    await tap('#cappp'); await p.waitForTimeout(3400);
    ok(name+' paused: controls stay visible', await p.evaluate(()=>!document.body.classList.contains('idle')));
    // CC toggle, remembered
    await tap('#capcc'); await p.waitForTimeout(200);
    c = await p.evaluate(()=>({cc: __app.cc, ls: localStorage.getItem('tlm.cc'), txt: getComputedStyle(document.getElementById('captext')).display}));
    ok(name+' CC off hides subtitles '+JSON.stringify(c), c.cc===false && c.ls==='off' && c.txt==='none');
    if (mobile && !rm) await shot('cine_film_cc_off');
    await p.reload({waitUntil:'networkidle'}); await p.waitForTimeout(700);
    ok(name+' CC choice remembered after reload', await p.evaluate(()=>__app.cc===false && document.getElementById('capcc').getAttribute('aria-pressed')==='false'));
    // replay with CC on, skip to the end: zoom back out to the explore UI on the new year
    await p.evaluate(()=>__app.showStep(9)); await p.waitForTimeout(1200);
    await p.evaluate(()=>document.getElementById('playbtn').scrollIntoView({block:'center'}));
    await tap('#playbtn'); await p.waitForTimeout(1500);
    await tap('#capcc'); await p.waitForTimeout(100);
    ok(name+' CC back on', await p.evaluate(()=>__app.cc===true && getComputedStyle(document.getElementById('captext')).display!=='none'));
    await p.evaluate(()=>__app.seek(__app.play.n - 1)); await p.waitForTimeout(rm ? 300 : 500);
    // let the last beat finish by itself
    for (let i = 0; i < 40 && await p.evaluate(()=>!!__app.play); i++) await p.waitForTimeout(500);
    await p.waitForTimeout(rm ? 200 : 350);
    const zo = await p.evaluate(()=>({cine: !!__app.cine, vp: document.getElementById('vp').getBoundingClientRect().height}));
    await p.waitForTimeout(1600);
    c = await p.evaluate(()=>({mode: __app.mode, cine: __app.cine, hdr: getComputedStyle(document.querySelector('header')).opacity, ev: !document.getElementById('ev').hidden && getComputedStyle(document.getElementById('ev')).opacity,
      vp: document.getElementById('vp').getBoundingClientRect().height, H: innerHeight, pill: document.getElementById('pill').textContent, flag: !!document.querySelector('.soonflag'), ph: !!document.getElementById('vpph'), fs: !!document.fullscreenElement }));
    ok(name+' end: zoomed out to explore UI on '+c.pill+' '+JSON.stringify(c), c.mode==='soon' && c.cine===null && c.hdr==='1' && c.ev==='1' && c.vp < c.H - 50 && /1150/.test(c.pill) && c.flag && !c.ph && !c.fs);
    if (!rm) ok(name+' end: zoom-out is animated (mid height '+Math.round(zo.vp)+')', zo.vp < c.H);
    if (mobile && !rm) shot('cine_zoomout');
    await p.waitForTimeout(400); if (mobile && !rm) await shot('cine_zoomout');
    // objects clickable again
    ok(name+' end: map objects clickable again', await p.evaluate(()=>{ const g=[...document.querySelectorAll('g.obj')].find(e=>e.style.display!=='none'); if(!g) return false; g.querySelector('.hit').dispatchEvent(new MouseEvent('click',{bubbles:true})); return !!__app.open; }));
    await p.evaluate(()=>__app.closeObj());
    // exit button mid-film goes back to explore
    await p.evaluate(()=>document.getElementById('replay').scrollIntoView({block:'center'}));
    await tap('#replay'); await p.waitForTimeout(2200);
    ok(name+' replay enters the film again', await p.evaluate(()=>!!(__app.cine && __app.cine.full)));
    await p.evaluate(()=>document.body.classList.remove('idle'));
    await tap('#capx'); await p.waitForTimeout(1600);
    c = await p.evaluate(()=>({cine: __app.cine, mode: __app.mode, play: __app.play, hdr: getComputedStyle(document.querySelector('header')).opacity, pb: !!document.getElementById('playbtn')}));
    ok(name+' Exit leaves the film back to explore '+JSON.stringify(c), c.cine===null && c.play===null && c.mode==='stop' && c.hdr==='1' && c.pb);
    // Escape also exits
    if (!mobile){
      await p.evaluate(()=>document.getElementById('playbtn').scrollIntoView({block:'center'})); await p.click('#playbtn'); await p.waitForTimeout(1500);
      await p.keyboard.press('Escape'); await p.waitForTimeout(1600);
      ok(name+' Escape leaves the film', await p.evaluate(()=>__app.cine===null && __app.play===null));
    }
    await ctx.close();
  }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS', JSON.stringify(errs));
  console.log(notes.filter(n=>n.startsWith('FAIL')).length ? 'SOME FAILED' : 'ALL PASS', notes.length);
})();
