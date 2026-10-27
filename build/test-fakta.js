const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
(async () => {
  const b = await chromium.launch();
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  for (const [name, vw, vh, mobile] of [['mobile',393,852,true],['desktop',1280,800,false]]) {
    const ctx = await b.newContext({viewport:{width:vw,height:vh}, deviceScaleFactor:2, isMobile:mobile, hasTouch:mobile});
    const p = await ctx.newPage();
    p.on('console', m => { if (m.type()==='error') errs.push(name+': '+m.text()); });
    p.on('pageerror', e => errs.push(name+' pageerror: '+e.message));
    let bytes = 0; p.on('response', async r => { try { bytes += (await r.body()).length; } catch(e){} });
    await p.goto(url, {waitUntil:'networkidle'}); await p.waitForTimeout(1200);
    notes.push(name+' bytes on load: '+bytes);
    const tap = async (x,y) => mobile ? p.touchscreen.tap(x,y) : p.mouse.click(x,y);
    const st = () => p.evaluate(() => ({open: __app.open, step: __app.step, K: __app.K, tr: document.querySelector('#map > g').getAttribute('transform'), n: document.getElementById('evn').textContent, title: document.title}));
    let s = await st(); ok(name+' title "'+s.title+'"', s.title.includes('History of the Jews'));
    ok(name+' objects drawn: '+await p.evaluate(()=>document.querySelectorAll('g.obj, g.lobj').length), true);
    if (!mobile && shots) await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_desktop_overview.png'});
    // step through events; map must move each time
    const trs = [s.tr];
    const total = +s.n.split('/')[1];
    for (let i = 1; i < total; i++) {
      await p.click('#evnext'); await p.waitForTimeout(1100);
      s = await st(); trs.push(s.tr);
      if (i === 1 && mobile && shots) { await p.evaluate(()=>scrollTo(0,0) || scrollTo(0, document.getElementById('ev').getBoundingClientRect().top + scrollY - document.getElementById('vp').offsetHeight - 8)); await p.waitForTimeout(150); await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_mobile_story_step2.png'}); await p.evaluate(()=>scrollTo(0,0)); }
      if (s.step === 7 && mobile && shots) { // stele event: big box
        await p.evaluate(()=>scrollTo(0,0) || scrollTo(0, document.getElementById('ev').getBoundingClientRect().top + scrollY - document.getElementById('vp').offsetHeight - 8)); await p.waitForTimeout(150);
        await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_mobile_event_big.png'}); await p.evaluate(()=>scrollTo(0,0));
      }
    }
    ok(name+' stepped to '+s.n+', map moved every step', new Set(trs).size === trs.length);
    ok(name+' next disabled at end', await p.evaluate(()=>document.getElementById('evnext').disabled));
    // back to step 3 (Canaan) and tap a real city dot (Jerusalem) on screen
    await p.evaluate(()=>__app.showStep(3)); await p.waitForTimeout(1100);
    await p.evaluate(()=>scrollTo(0,0));
    const pos = id => p.evaluate(id => { const g=[...document.querySelectorAll('g.obj')].find(e=>e.__data__.o.id===id); if(!g||g.style.display==='none') return null; const r=g.querySelector('.hit').getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}; }, id);
    let q = await pos('jerusalem');
    if (q) { await tap(q.x, q.y); await p.waitForTimeout(400); }
    s = await st(); ok(name+' tap Jerusalem dot -> small box: '+s.open, s.open === 'jerusalem');
    if (mobile && shots) await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_mobile_city.png'});
    await p.click('#popx'); await p.waitForTimeout(200);
    s = await st(); ok(name+' X closes', s.open === null);
    // chip in big box opens object and flies there
    const before = s.tr;
    await p.evaluate(()=>__app.showStep(8)); await p.waitForTimeout(1100);
    await p.evaluate(()=>[...document.querySelectorAll('.chip')].find(b=>b.dataset.o==='jordan').scrollIntoView({block:'center'}));
    await p.click('.chip[data-o="jordan"]'); await p.waitForTimeout(400);
    s = await st(); ok(name+' chip Jordan -> small box: '+s.open, s.open === 'jordan');
    // tap outside closes (header)
    await tap(vw-120, 20); await p.waitForTimeout(300);
    s = await st(); ok(name+' tap outside closes', s.open === null);
    // river by tapping the line itself
    await p.evaluate(()=>scrollTo(0,0));
    q = await p.evaluate(() => { const g=[...document.querySelectorAll('g.lobj')].find(e=>e.__data__.id==='jordan');
      for (const pth of g.querySelectorAll('.lhit')) { const L=pth.getTotalLength(); const m=pth.getScreenCTM();
        for (let f=0.1; f<0.95; f+=0.05) { const pt=pth.getPointAtLength(L*f); const x=pt.x*m.a+m.e, y=pt.y*m.d+m.f;
          if (y < 60 || y > document.getElementById('vp').getBoundingClientRect().bottom - 30) continue;
          const el=document.elementFromPoint(x,y); if (el && el.closest('g.lobj') === g) return {x,y}; } } return {x:0,y:0}; });
    await tap(q.x, q.y); await p.waitForTimeout(400);
    s = await st(); ok(name+' tap Jordan line -> '+s.open, s.open === 'jordan');
    await p.click('#popx'); await p.waitForTimeout(200);
    // people: tap Israel zone
    await p.evaluate(()=>__app.showStep(7)); await p.waitForTimeout(1100); await p.evaluate(()=>scrollTo(0,0));
    q = await p.evaluate(() => { const r=document.querySelector('text.zl-people').getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}; });
    await tap(q.x, q.y); await p.waitForTimeout(400);
    s = await st(); ok(name+' tap ISRAEL label -> '+s.open, s.open === 'israelp');
    if (mobile && shots) await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_mobile_people.png'});
    await p.click('#popx'); await p.waitForTimeout(200);
    // river small box screenshot (Nile, overview)
    await p.evaluate(()=>{ __app.showStep(0); }); await p.waitForTimeout(1100);
    await p.evaluate(()=>__app.openObj('nile', true)); await p.waitForTimeout(1000);
    if (mobile && shots) await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_mobile_river.png'});
    if (!mobile && shots) { await p.evaluate(()=>__app.showStep(7)); await p.waitForTimeout(1100); await p.evaluate(()=>__app.openObj('ashkelon')); await p.waitForTimeout(300); await p.screenshot({path:(process.env.SHOTS||'screens')+'/faktaruta_desktop_event_and_city.png'}); }
    // every object opens without error
    const bad = await p.evaluate(()=>{ const out=[]; for (const g of document.querySelectorAll('g.obj, g.lobj')) { const id=(g.__data__.o||g.__data__).id; __app.openObj(id); if(__app.open!==id) out.push(id);} __app.closeObj(); return out; });
    ok(name+' all objects open: failures '+JSON.stringify(bad), bad.length===0);
    // narration still works
    await p.evaluate(()=>openStory()); await p.waitForTimeout(300); await p.evaluate(()=>closeStory());
    await ctx.close();
  }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS:', JSON.stringify(errs));
})();
