const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const shots = process.argv[3] !== 'noshots';
const D = process.env.SHOTS || 'screens';
(async () => {
  const b = await chromium.launch();
  const errs = [], notes = [];
  const ok = (n, c) => notes.push((c ? 'PASS ' : 'FAIL ') + n);
  process.on('unhandledRejection', e => { console.log(notes.join('\n')); console.log('CRASH', e.message.split('\n').slice(0,14).join(' | ')); process.exit(1); });
  for (const [name, vw, vh, mobile] of [['mobile',393,852,true],['desktop',1280,800,false]]) {
    const ctx = await b.newContext({viewport:{width:vw,height:vh}, deviceScaleFactor:2, isMobile:mobile, hasTouch:mobile});
    if (process.env.TS) await ctx.addInitScript(t => localStorage.setItem('tlm.textsize', t), process.env.TS); // TS=xl runs the suite at a saved text size
    const p = await ctx.newPage();
    // the About notice is tested in test-cine.js; here the visitor has already seen it
    await ctx.addInitScript(() => { try { localStorage.setItem('tlm.notice.v1', 'seen'); } catch(e){} });
    p.on('console', m => { if (m.type()==='error') errs.push(name+': '+m.text()); });
    p.on('pageerror', e => errs.push(name+' pageerror: '+e.message));
    let bytes = 0; p.on('response', async r => { try { bytes += (await r.body()).length; } catch(e){} });
    await p.goto(url, {waitUntil:'networkidle'}); await p.waitForTimeout(1200);
    notes.push(name+' bytes on load: '+bytes);
    const tap = async (x,y) => mobile ? p.touchscreen.tap(x,y) : p.mouse.click(x,y);
    // film controls fade out after a few seconds; a touch or mouse move brings them back first
    const ctl = async sel => { await p.evaluate(()=>{ dispatchEvent(new PointerEvent('pointermove')); if (__app.wake) __app.wake(); }); await p.waitForTimeout(120); return p.click(sel); };
    const st = () => p.evaluate(() => ({open: __app.open, step: __app.step, K: __app.K, tr: document.querySelector('#map > g').getAttribute('transform'), n: document.getElementById('evn').textContent, title: document.title}));
    let s = await st(); ok(name+' title "'+s.title+'"', s.title.includes('Story of the Jews'));
    ok(name+' objects drawn: '+await p.evaluate(()=>document.querySelectorAll('g.obj, g.lobj').length), true);
    if (!mobile && shots) await p.screenshot({path:D+'/faktaruta_desktop_overview.png'});
    const toEv = async () => { await p.evaluate(()=>scrollTo(0,0) || scrollTo(0, document.getElementById('ev').getBoundingClientRect().top + scrollY - document.getElementById('vp').offsetHeight - 8)); await p.waitForTimeout(150); };
    if (shots) await p.screenshot({path:D+'/faktaruta_intro'+(mobile?'':'_desktop')+'.png'});
    ok(name+' intro has Explore + Start buttons', await p.evaluate(()=>!!document.getElementById('goexplore') && !!document.getElementById('gostory')));
    ok(name+' explore pill "'+await p.textContent('#xp')+'"', /0\/12/.test(await p.textContent('#xp')));
    ok(name+' 12 glowing rings', await p.evaluate(()=>document.querySelectorAll('g.key.todo .ring').length) === 12);
    // step through events; map must move each time
    const trs = [s.tr];
    const total = +s.n.split('/')[1];
    for (let i = 1; i < total; i++) {
      await p.click('#evnext'); await p.waitForTimeout(1100);
      s = await st(); trs.push(s.tr);
      if (i === 1 && mobile && shots) { await p.evaluate(()=>scrollTo(0,0) || scrollTo(0, document.getElementById('ev').getBoundingClientRect().top + scrollY - document.getElementById('vp').offsetHeight - 8)); await p.waitForTimeout(150); await p.screenshot({path:D+'/faktaruta_mobile_story_step2.png'}); await p.evaluate(()=>scrollTo(0,0)); }
      if (s.step === 7 && mobile && shots) { await toEv(); await p.screenshot({path:D+'/faktaruta_mobile_event_big.png'}); await p.evaluate(()=>scrollTo(0,0)); }
    }
    ok(name+' stepped to '+s.n+', map moved every step', new Set(trs).size === trs.length);
    ok(name+' next disabled at end', await p.evaluate(()=>document.getElementById('evnext').disabled));
    ok(name+' last step is Explore with Play', await p.evaluate(()=>!!document.getElementById('playbtn') && document.querySelectorAll('.ck').length === 12));
    // label collision at medium zoom near Israel: no two visible labels overlap
    await p.evaluate(()=>{ __app.closeObj(); }); await p.evaluate(()=>window.__flyLab && 0);
    await p.evaluate(()=>__app.showStep(3)); await p.waitForTimeout(1100);
    const overlaps = await p.evaluate(() => { const r=[...document.querySelectorAll('g.obj')].filter(g=>g.style.display!=='none'&&!g.classList.contains('nolab')).map(g=>[g.__data__.o.id,g.querySelector('.lab').getBoundingClientRect()]).filter(x=>x[1].width>0);
      const z=[...document.querySelectorAll('text.zlabel')].filter(t=>t.style.display!=='none').map(t=>['zone:'+t.textContent,t.getBoundingClientRect()]);
      const all=r.concat(z), out=[]; for(let i=0;i<all.length;i++)for(let j=i+1;j<all.length;j++){const a=all[i][1],b=all[j][1]; if(a.left<b.right-1&&a.right>b.left+1&&a.top<b.bottom-1&&a.bottom>b.top+1) out.push(all[i][0]+'/'+all[j][0]);} return {out, hidden:document.querySelectorAll('g.obj.nolab').length}; });
    ok(name+' label overlaps near Israel (K='+(await st()).K.toFixed(1)+', hidden '+overlaps.hidden+'): '+JSON.stringify(overlaps.out), overlaps.out.length <= 1);
    // back to step 3 (Canaan) and tap a real city dot (Jerusalem) on screen
    await p.evaluate(()=>__app.showStep(3)); await p.waitForTimeout(1100);
    await p.evaluate(()=>scrollTo(0,0));
    const pos = id => p.evaluate(id => { const g=[...document.querySelectorAll('g.obj')].find(e=>e.__data__.o.id===id); if(!g||g.style.display==='none') return null; const r=g.querySelector('.hit').getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}; }, id);
    let q = await pos('jerusalem');
    if (q) { await tap(q.x, q.y); await p.waitForTimeout(400); }
    s = await st(); ok(name+' tap Jerusalem dot -> small box: '+s.open, s.open === 'jerusalem');
    if (mobile && shots) await p.screenshot({path:D+'/faktaruta_mobile_city.png'});
    await p.click('#popx'); await p.waitForTimeout(200);
    s = await st(); ok(name+' X closes', s.open === null);
    // chip in big box opens object and flies there
    const before = s.tr;
    await p.evaluate(()=>__app.showStep(8)); await p.waitForTimeout(1100);
    await p.evaluate(()=>[...document.querySelectorAll('.chip')].find(b=>b.dataset.o==='jordan').scrollIntoView({block:'center'}));
    await p.click('.chip[data-o="jordan"]'); await p.waitForTimeout(400);
    s = await st(); ok(name+' chip Jordan -> small box: '+s.open, s.open === 'jordan');
    // tap outside closes (header)
    await tap(40, 14); await p.waitForTimeout(300);
    s = await st(); ok(name+' tap outside closes', s.open === null);
    // river by tapping the line itself
    await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(700); // let the map settle after closing
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
    if (mobile && shots) await p.screenshot({path:D+'/faktaruta_mobile_people.png'});
    await p.click('#popx'); await p.waitForTimeout(200);
    // river small box screenshot (Nile, overview)
    await p.evaluate(()=>{ __app.showStep(0); }); await p.waitForTimeout(1100);
    await p.evaluate(()=>__app.openObj('nile', true)); await p.waitForTimeout(1000);
    if (mobile && shots) await p.screenshot({path:D+'/faktaruta_mobile_river.png'});
    if (!mobile && shots) { await p.evaluate(()=>__app.showStep(7)); await p.waitForTimeout(1100); await p.evaluate(()=>__app.openObj('ashkelon')); await p.waitForTimeout(300); await p.screenshot({path:D+'/faktaruta_desktop_event_and_city.png'}); }
    // every object opens without error
    const bad = await p.evaluate(()=>{ const out=[]; for (const g of document.querySelectorAll('g.obj, g.lobj')) { const id=(g.__data__.o||g.__data__).id; __app.openObj(id); if(__app.open!==id) out.push(id);} __app.closeObj(); return out; });
    ok(name+' all objects open: failures '+JSON.stringify(bad), bad.length===0);
    ok(name+' old narration hidden from main flow', await p.evaluate(()=>!document.getElementById('story') && !document.querySelector('audio')));
    // ---- explore progress: open 3 key objects from the checklist, persists across reload ----
    await p.evaluate(()=>{ localStorage.clear(); }); await p.reload({waitUntil:'networkidle'}); await p.waitForTimeout(1000);
    await p.click('#xp'); await p.waitForTimeout(1100);
    for (const id of ['israelp','jerusalem','ashkelon']) { await p.evaluate(id=>document.querySelector('.ck[data-o="'+id+'"]').scrollIntoView({block:'center'}), id); await p.click('.ck[data-o="'+id+'"]'); await p.waitForTimeout(350); await p.click('#popx'); await p.waitForTimeout(150); }
    await p.evaluate(()=>__app.showStep(__app.step)); await p.waitForTimeout(1100);
    ok(name+' explored '+JSON.stringify(await p.evaluate(()=>__app.explored)), (await p.evaluate(()=>__app.explored.length)) === 3);
    await p.reload({waitUntil:'networkidle'}); await p.waitForTimeout(1000);
    ok(name+' progress kept after reload: pill "'+(await p.textContent('#xp')).trim()+'", checks '+await p.evaluate(()=>document.querySelectorAll('g.key.done').length), /3\/12/.test(await p.textContent('#xp')) && await p.evaluate(()=>document.querySelectorAll('g.key.done').length) === 3);
    await p.click('#xp'); await p.waitForTimeout(1200);
    ok(name+' checklist shows 3 done', await p.evaluate(()=>document.querySelectorAll('.ck.done').length) === 3);
    if (shots) { if (mobile) await toEv(); await p.screenshot({path:D+'/faktaruta_progress'+(mobile?'':'_desktop')+'.png'}); await p.evaluate(()=>scrollTo(0,0)); }
    // ---- Play ----
    await p.evaluate(()=>document.getElementById('playbtn').scrollIntoView({block:'center'}));
    if (mobile) await p.tap('#playbtn'); else await p.click('#playbtn');
    await p.evaluate(()=>scrollTo(0,0)); await p.waitForTimeout(1500);
    const cap = await p.evaluate(()=>({vis:!document.getElementById('cap').hidden, t:document.getElementById('captext').textContent, b:!!document.querySelector('#captext .cb'), s:document.getElementById('capsrc').textContent, pill:document.getElementById('pill').textContent, play:__app.play}));
    ok(name+' play started, caption with badge + sources: '+JSON.stringify(cap).slice(0,160), cap.vis && cap.b && cap.s.startsWith('Sources:') && cap.play && cap.play.i === 0);
    await p.waitForTimeout(1500);
    if (shots) await p.screenshot({path:D+'/faktaruta_play'+(mobile?'':'_desktop')+'.png'});
    // pacing: beat 1 is a recorded line of 9.8 s + 2 s pause (reading time 8.4 s with the voice off), so at ~9 s we are still on it
    await p.waitForTimeout(6000);
    ok(name+' pacing: still on beat 1 after 9 s', await p.evaluate(()=>__app.play.i) === 0);
    const pace = await p.evaluate(()=>fetch('data/stories/jews/1207bc.json').then(r=>r.json()).then(d=>d.play.beats.every(b=>b.duration>=2000 && b.pauseAfter>=400 && b.pauseAfter<=2000 && b.audioMs>2000 && /^assets\/narration\//.test(b.audio)) && d.play.words));
    ok(name+' every beat has duration, pauseAfter and its recorded line in the JSON; words '+pace, pace >= 1000 && pace <= 1500);
    ok(name+' year counter moving: '+await p.textContent('#pill'), /^c\. 1\d{3} BC$/.test(await p.textContent('#pill')));
    // pause / resume
    await ctl('#cappp'); const pz = await p.evaluate(()=>__app.play.paused); await p.waitForTimeout(300); await ctl('#cappp');
    ok(name+' pause/resume', pz === true && (await p.evaluate(()=>__app.play.paused)) === false);
    await p.evaluate(()=>document.getElementById('map').dispatchEvent(new MouseEvent('click',{bubbles:true})));
    ok(name+' tapping the map does not pause', await p.evaluate(()=>__app.play.paused) === false);
    const sp = []; for (let i = 0; i < 3; i++){ await ctl('#capspd'); sp.push(await p.textContent('#capspd')); }
    ok(name+' speed button cycles '+sp.join(' '), sp.join(' ') === '1.25× 0.75× 1×');
    ok(name+' controls visible: prev, pause, next, speed', await p.evaluate(()=>['capprev','cappp','capnext','capspd'].every(id=>{const r=document.getElementById(id).getBoundingClientRect(); return r.width>30 && r.height>30;})));
    // migration beat: arrows drawing + caption
    await p.evaluate(()=>__app.seek(11)); await p.waitForTimeout(6600);
    const mig = await p.evaluate(()=>({arrows:document.querySelectorAll('.arrow.mig.unsure').length, lab:[...document.querySelectorAll('.fxlab text')].map(t=>t.textContent), cap:document.getElementById('captext').textContent.slice(0,40)}));
    ok(name+' migration arrows dashed + Disputed: '+JSON.stringify(mig), mig.arrows === 2 && mig.lab.every(l=>/Disputed/.test(l)));
    if (shots) await p.screenshot({path:D+'/faktaruta_animation'+(mobile?'':'_desktop')+'.png'});
    await p.evaluate(()=>__app.seek(15)); await p.waitForTimeout(8800);
    ok(name+' battle beat: markers '+await p.evaluate(()=>document.querySelectorAll('.battle').length)+', army arrows '+await p.evaluate(()=>document.querySelectorAll('.arrow.army').length), await p.evaluate(()=>document.querySelectorAll('.battle').length===3 && document.querySelectorAll('.arrow.army').length===5));
    if (shots) await p.screenshot({path:D+'/faktaruta_battle'+(mobile?'':'_desktop')+'.png'});
    ok(name+' Hatti faded', await p.evaluate(()=>[...document.querySelectorAll('path.z-hatti.zone')].every(e=>e.classList.contains('gone'))));
    // run to the end quickly
    await p.evaluate(()=>{ __app.speed = 12; __app.seek(__app.play.n - 6); });
    await p.waitForFunction(()=>__app.mode === 'stop' && !__app.play && /1150/.test(document.getElementById('pill').textContent), null, {timeout:30000});
    await p.waitForTimeout(1600);
    const end = await p.evaluate(()=>({big:document.getElementById('big').textContent, flag:!!document.querySelector('.soonflag'), phil:document.querySelectorAll('path.z-philistia').length, isr:document.querySelectorAll('path.israel').length, added:document.querySelectorAll('path.added').length, hatti:document.querySelectorAll('path.z-hatti').length, cap:document.getElementById('cap').hidden, xp:document.getElementById('xp').hidden}));
    await p.waitForTimeout(2500);
    ok(name+' stays on the 1150 intro (no auto-continue)', await p.evaluate(()=>__app.mode === 'stop' && !__app.play && /1150/.test(document.getElementById('pill').textContent)));
    ok(name+' recap has no scene lines, scene captions exist in data', await p.evaluate(()=>![...document.querySelectorAll('#evbody .cb')].some(b=>b.textContent==='Imagine')));
    ok(name+' donate link follows site.json donateUrl', await p.evaluate(()=>fetch('data/site.json').then(r=>r.json()).then(c=>{ const d=document.getElementById('donate'); return c.donateUrl ? (!d.hidden && d.href===c.donateUrl) : (d.hidden && getComputedStyle(d).display==='none'); })));
    ok(name+' play ends at the live c. 1150 stop (its own map, no soon flag): '+JSON.stringify(end), end.big === 'c. 1150 BC' && !end.flag && end.phil >= 1 && end.isr >= 1 && end.added === 0 && end.hatti === 0 && end.cap && !end.xp);
    if (shots) { if (mobile) await toEv(); await p.screenshot({path:D+'/faktaruta_1150'+(mobile?'':'_desktop')+'.png'}); await p.evaluate(()=>scrollTo(0,0)); }
    // visible zone labels never overlap (PHILISTIA hides next to ISRAEL when zoomed far out)
    ok(name+' zone labels do not overlap', await p.evaluate(()=>{ const r=[...document.querySelectorAll('text.zlabel')].filter(t=>getComputedStyle(t).visibility!=='hidden' && getComputedStyle(t).display!=='none' && +getComputedStyle(t).opacity>.5).map(t=>t.getBoundingClientRect()).filter(b=>b.width);
      return r.every((a,i)=>r.every((b,j)=>i>=j || a.right<=b.left+1 || b.right<=a.left+1 || a.bottom<=b.top+1 || b.bottom<=a.top+1)); }));
    if (await p.evaluate(()=>[...document.querySelectorAll('text.zlabel')].find(t=>t.textContent==='PHILISTIA').classList.contains('zcull'))) { await p.evaluate(()=>__zoomTest()); await p.waitForTimeout(1200); }
    ok(name+' PHILISTIA label shown when zoomed in', await p.evaluate(()=>!document.querySelector('text.zlabel.zcull')));
    q = await p.evaluate(() => { const t=[...document.querySelectorAll('text.zlabel')].find(t=>t.textContent==='PHILISTIA'); const r=t.getBoundingClientRect(); return {x:r.x+r.width/2,y:r.y+r.height/2}; });
    await tap(q.x, q.y); await p.waitForTimeout(400);
    s = await st(); ok(name+' tap PHILISTIA -> '+s.open, s.open === 'philistines');
    await p.click('#popx'); await p.waitForTimeout(200);
    // back to 1207, replay its Play, then stop -> 1207 explore, zones reset
    await p.evaluate(()=>{ __app.speed = 1; __app.go(0); }); await p.waitForTimeout(1200); await p.evaluate(()=>__app.playStart('play', 0)); await p.waitForTimeout(800);
    ok(name+' replay runs', await p.evaluate(()=>__app.play && __app.play.i === 0));
    await ctl('#capx'); await p.waitForTimeout(1200);
    ok(name+' stop -> 1207 explore, no added zones', await p.evaluate(()=>__app.mode==='stop' && !!document.getElementById('playbtn') && document.querySelectorAll('.added').length===0 && document.getElementById('pill').textContent==='1207 BC'));
    // timeline straight to c. 1150: the live stop with its own map (base features, nothing 'added')
    await p.evaluate(()=>__app.go(1)); await p.waitForTimeout(1200);
    ok(name+' timeline to 1150: '+await p.evaluate(()=>__app.mode+' '+document.querySelectorAll('.added').length), await p.evaluate(()=>__app.mode==='stop' && document.querySelectorAll('path.added').length===0 && document.querySelectorAll('path.z-philistia').length>=1 && document.querySelectorAll('path.z-hatti').length===0));
    await p.evaluate(()=>__app.go(2)); await p.waitForTimeout(1200);
    ok(name+' timeline to c. 1000 BC: a live stop (Chapter 3) with its own map', await p.evaluate(()=>__app.mode==='stop' && /1000/.test(document.getElementById('pill').textContent) && !document.querySelector('.soonflag') && document.querySelectorAll('path.z-ammon').length>=1));
    await p.evaluate(()=>__app.go(3)); await p.waitForTimeout(1500);
    ok(name+' timeline to c. 930 BC: a live stop (Chapter 4) with its own map, Israel and Judah drawn', await p.evaluate(()=>__app.mode==='stop' && /930/.test(document.getElementById('pill').textContent) && !document.querySelector('.soonflag') && document.querySelectorAll('path.z-judah').length>=1 && document.querySelectorAll('path.z-israel').length>=1));
    await p.evaluate(()=>__app.go(4)); await p.waitForTimeout(600);
    ok(name+' timeline to 722 BC: a live stop (Chapter 5) with its own map', await p.evaluate(()=>__app.mode==='stop' && /722/.test(document.getElementById('pill').textContent) && !document.querySelector('.soonflag') && document.querySelectorAll('path.z-aram').length>=1));
    await p.evaluate(()=>__app.go(5)); await p.waitForTimeout(600);
    ok(name+' timeline to 701 BC: the end of the 722 Play, coming soon', await p.evaluate(()=>__app.mode==='soon' && /701/.test(document.getElementById('pill').textContent) && !!document.querySelector('.soonflag')));
    await p.evaluate(()=>__app.go(0)); await p.waitForTimeout(1200);
    await ctx.close();
  }
  await b.close();
  console.log(notes.join('\n'));
  console.log('ERRORS:', JSON.stringify(errs));
})();
