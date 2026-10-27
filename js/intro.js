/* The Long Map: the "About" notice and the opening book.
   First visit: a short notice (what this site is and is not), then BEGIN ADVENTURE opens a book whose
   cover turns to reveal the map. The choice is remembered (localStorage tlm.notice.v1), so returning
   visitors go straight to the map. "About" in the header or footer opens the notice again.
   CSS only, no images. With prefers-reduced-motion the book is skipped and the notice simply fades. */
(function(){
  const KEY = 'tlm.notice.v1';
  const $ = id => document.getElementById(id);
  const intro = $('intro'), begin = $('begin');
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
  let timers = [], lastFocus = null, state = 'hidden';
  const later = (ms, fn) => timers.push(setTimeout(fn, ms));
  const seen = () => { try { return localStorage.getItem(KEY) === 'seen'; } catch(e){ return false; } };
  function show(){
    timers.forEach(clearTimeout); timers = [];
    lastFocus = document.activeElement;
    intro.className = 'intro'; intro.hidden = false; intro.style.opacity = '';
    document.body.classList.add('noticing'); state = 'notice';
    setTimeout(() => begin.focus(), 30);
  }
  function done(){
    intro.hidden = true; intro.className = 'intro'; document.body.classList.remove('noticing'); state = 'hidden';
    if (lastFocus && lastFocus.focus && lastFocus !== document.body) lastFocus.focus();
  }
  function start(){
    try { localStorage.setItem(KEY, 'seen'); } catch(e){}
    timers.forEach(clearTimeout); timers = [];
    if (reduced()){ state = 'closing'; intro.classList.add('reveal'); later(60, done); return; }
    // the book: appear, the cover turns, then the page grows into the map
    state = 'book'; intro.classList.add('booking');
    later(30, () => intro.classList.add('show'));
    later(550, () => { intro.classList.add('open'); state = 'opening'; });
    later(2050, () => { state = 'open'; });
    later(2600, () => { intro.classList.add('reveal'); state = 'reveal'; });
    later(3400, done);
  }
  begin.addEventListener('click', start);
  intro.addEventListener('keydown', e => { if (e.key === 'Tab' && state === 'notice'){ e.preventDefault(); begin.focus(); } });
  ['about', 'about2'].forEach(id => { const b = $(id); if (b) b.addEventListener('click', e => { e.stopPropagation(); show(); }); });
  if (!seen()) show();
  window.__intro = { show, start, get state(){ return state; }, KEY };
})();
