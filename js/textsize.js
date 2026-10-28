/* The Long Map: text size. Four steps (A−, A, A+, A++) in the header and above the About notice.
   The choice sets <html data-ts>, which sets the CSS variables --ts (reading text) and --tsm (map labels),
   and is remembered in localStorage tlm.textsize. The inline script in <head> applies it before the first paint. */
(function(){
  const KEY = 'tlm.textsize', SIZES = ['s', 'm', 'l', 'xl'];
  const root = document.documentElement;
  const get = () => SIZES.includes(root.getAttribute('data-ts')) ? root.getAttribute('data-ts') : 'm';
  function sync(){
    const cur = get();
    document.querySelectorAll('.ts button[data-ts]').forEach(b => b.setAttribute('aria-pressed', b.dataset.ts === cur ? 'true' : 'false'));
  }
  function set(v, save = true){
    if (!SIZES.includes(v)) v = 'm';
    if (v === 'm') root.removeAttribute('data-ts'); else root.setAttribute('data-ts', v);
    if (save) { try { localStorage.setItem(KEY, v); } catch(e){} }
    sync();
    // the map relabels and the film re-places its panels for the new size
    dispatchEvent(new CustomEvent('tlm:textsize', {detail: v}));
  }
  document.addEventListener('click', e => {
    const b = e.target.closest && e.target.closest('.ts button[data-ts]'); if (!b) return;
    e.stopPropagation(); set(b.dataset.ts);
  }, true);
  sync();
  window.__ts = { set, get value(){ return get(); }, KEY, SIZES };
})();
