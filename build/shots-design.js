// Screenshots of the visual design: notice, book cover, explore view, open fact box, film mode.
// node build/shots-design.js http://127.0.0.1:8793/  (SHOTS=dir, PREFIX=design2_)
const { chromium } = require('playwright');
const url = process.argv[2] || 'http://127.0.0.1:8793/';
const D = process.env.SHOTS || 'screens', P = process.env.PREFIX || 'design2_';
(async () => {
  const b = await chromium.launch(); const errs = [];
  for (const [name, vw, vh, mobile] of [['mobile',393,852,true],['desktop',1280,800,false]]) {
    const ctx = await b.newContext({viewport:{width:vw,height:vh}, deviceScaleFactor:2, isMobile:mobile, hasTouch:mobile});
    const p = await ctx.newPage(); const sfx = mobile ? '' : '_desktop';
    p.on('console', m => { if (m.type()==='error') errs.push(name+': '+m.text()); }); p.on('pageerror', e => errs.push(name+': '+e.message));
    const shot = f => p.screenshot({path:`${D}/${P}${f}${sfx}.png`});
    await p.goto(url, {waitUntil:'networkidle'}); await p.waitForTimeout(900);
    await shot('notice');
    await p.click('#begin'); await p.waitForTimeout(420); await shot('cover');
    await p.waitForTimeout(420); if (mobile) await shot('book_mid');
    await p.waitForTimeout(2980);
    await shot('explore');
    if (mobile){ await p.evaluate(()=>scrollTo(0, 700)); await p.waitForTimeout(300); await shot('story'); await p.evaluate(()=>scrollTo(0,0)); }
    await p.evaluate(()=>__app.openObj('jerusalem')); await p.waitForTimeout(900); await shot('factbox');
    await p.evaluate(()=>__app.closeObj()); await p.evaluate(()=>__app.showStep(9)); await p.waitForTimeout(1200);
    await p.evaluate(()=>document.getElementById('playbtn').scrollIntoView({block:'center'})); await p.click('#playbtn');
    await p.waitForTimeout(9000); await shot('film');
    await ctx.close();
  }
  await b.close(); console.log('ERRORS', JSON.stringify(errs));
})();
