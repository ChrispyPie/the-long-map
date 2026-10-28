/* The Long Map: stories on a vector map.
   A story (data/stories/<id>/story.json) has stops. Each stop has events = big fact boxes, the narrative.
   Map objects come from a shared library (data/objects/*.json) = small fact boxes, reused by every story.
   Sources come from a shared registry (data/sources.json). */
const $ = id => document.getElementById(id);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const STORY_URL = 'data/stories/jews/story.json';
let STORY = null, STOP = null, ERA = null, SRC = {}, OBJ = {}, OBJS = [];
let cur = 0, step = 0, K = 1, openId = null, MODE = 'stop', SPEED = 1;
let ARRIVE = -1;   // the stop just reached by the end of the previous chapter's Play (shows "Continue to Chapter N")
const cache = {};
// frame = the film's own framing lines (title, how to read the labels, the choice): shown without a badge
const CERT = {attested:'Attested', disputed:'Disputed', tradition:'Tradition', scene:'Imagine', frame:''};
const badge = c => CERT[c] ? `<span class="cb cb-${c}">${CERT[c]}</span>` : '';
const TYPE = {city:'City', site:'Site', river:'River', lake:'Lake', sea:'Sea', region:'Region', route:'Route', people:'People', state:'Kingdom'};
const ICON = {
  city:'<circle cx="8" cy="8" r="4.5"/>', site:'<rect x="4" y="4" width="8" height="8" transform="rotate(45 8 8)"/>',
  river:'<path d="M1 6c3-3 4 3 7 0s4 3 7 0M1 11c3-3 4 3 7 0s4 3 7 0" fill="none" stroke-width="1.6"/>',
  lake:'<ellipse cx="8" cy="8" rx="6" ry="4"/>', sea:'<path d="M1 9c2-2 3 2 5 0s3 2 5 0 3 2 4 0" fill="none" stroke-width="1.8"/>',
  region:'<path d="M1 13 6 5l3 4 2-3 4 7z"/>', route:'<path d="M2 13 14 3" fill="none" stroke-width="2" stroke-dasharray="2 2"/>',
  people:'<circle cx="5.5" cy="5" r="2.4"/><circle cx="10.5" cy="5" r="2.4"/><path d="M1 14c0-4 9-4 9 0zM6 14c0-4 9-4 9 0z"/>',
  state:'<path d="M2 14V6l6-4 6 4v8z"/>'};
const icon = t => `<svg class="ic ic-${t}" viewBox="0 0 16 16" aria-hidden="true">${ICON[t]||ICON.city}</svg>`;

const svg = d3.select('#map');
const root = svg.append('g');
const gLand = root.append('g'), gZones = root.append('g'), gFx = root.append('g').attr('class','fx'), gLines = root.append('g'), gKey = root.append('g').attr('class','keys'), gPts = root.append('g'), gFxTop = root.append('g').attr('class','fx');
const projection = d3.geoConicConformal().parallels([30, 40]).rotate([-38, 0]);
const path = d3.geoPath(projection);
const VIEW = {type:'MultiPoint', coordinates:[[20,24],[57,24],[20,43],[57,43],[38,44.5]]};
const RIVERS = {}, LAKES = {};

function rewind(f){
  const g = f.geometry; if (!g) return f;
  const fix = poly => d3.geoArea({type:'Polygon', coordinates:poly}) > 2*Math.PI ? poly.map(r => r.slice().reverse()) : poly;
  if (g.type === 'Polygon') g.coordinates = fix(g.coordinates);
  if (g.type === 'MultiPolygon') g.coordinates = g.coordinates.map(fix);
  return f;
}
const rewindAll = fc => { (fc.features || [fc]).forEach(rewind); return fc; };
function size(){ const r = $('vp').getBoundingClientRect(); return [r.width, r.height]; }

function fit(){
  const [w,h] = size();
  projection.fitExtent([[6,6],[w-6,h-6]], VIEW);
  svg.attr('viewBox', `0 0 ${w} ${h}`);
  const a = projection([-12, 58]), b = projection([88, 58]), c = projection([-12, 2]), d = projection([88, 2]), m = projection([38, 2]);
  zoom.extent([[0,0],[w,h]]).translateExtent([[Math.max(a[0],c[0]), Math.min(a[1],b[1])], [Math.min(b[0],d[0]), m[1]]]);
  redraw();
}
function redraw(){
  root.selectAll('path:not(.nogeo)').attr('d', path);
  gPts.selectAll('g.obj').attr('transform', d => { const p = projection(d.pt); return `translate(${p[0]},${p[1]})`; });
  scaleMarks();
}
// rank 1 always, rank 2 from zoom 2, rank 3 from zoom 4.5; highlighted objects always
const showAt = (r, t) => r === 1 ? 0 : r === 2 ? 2 : (t === 'city' || t === 'site') ? 4.5 : 7;
function scaleMarks(){
  gPts.selectAll('g.obj')
    .style('display', d => (K >= showAt(d.o.rank, d.o.type) || d.hl) ? null : 'none')
    .each(function(){ d3.select(this).select('.inner').attr('transform', `scale(${1/K})`); });
  gZones.selectAll('text.zlabel').style('font-size', (10*TSM()/K) + 'px').style('stroke-width', (2/K) + 'px').style('display', K > 9 ? 'none' : null);
  // the soft edge is for a people without a border; the two kingdoms after the split (c. 930 BC) keep a sharp, dashed edge
  gZones.selectAll('.israel').attr('filter', function(){ return K < 3 || this.matches('.z-israel, .z-judah') ? null : 'url(#soft)'; });
  gKey.selectAll('g.key').attr('transform', d => { const p = projection(d.pt); return `translate(${p[0]},${p[1]}) scale(${1/K})`; });
  root.selectAll('g.fxm').attr('transform', d => { const p = projection(d.pt); return `translate(${p[0]},${p[1]}) scale(${1/K})`; });
  root.selectAll('g.tip').attr('transform', d => { const a = projection(d.a), b = projection(d.b); const ang = Math.atan2(b[1]-a[1], b[0]-a[0]) * 180 / Math.PI; return `translate(${b[0]},${b[1]}) rotate(${ang}) scale(${1/K})`; });
  cullLabels();
}
// ---------- label collision: greedy, on screen boxes; the dot stays, only the text hides ----------
// greedy label collision pass on real screen boxes (zone labels first, then by priority)
let cullRaf = 0;
function cullLabels(){ if (!cullRaf) cullRaf = requestAnimationFrame(() => { cullRaf = 0; cullNow(); }); }
function cullNow(){
  const boxes = [], pad = 1, hit = b => boxes.some(q => b.left < q.right - pad && b.right > q.left + pad && b.top < q.bottom - pad && b.bottom > q.top + pad);
  // in a film the places the narrator names always keep their labels: they claim their space first
  const first = new Set();
  if (PLAY) gPts.selectAll('g.obj.hl').each(function(){ if (this.style.display === 'none') return; const lab = this.querySelector('.lab'); const r = lab && lab.getBoundingClientRect();
    if (r && r.width && !hit(r)){ this.classList.remove('nolab'); boxes.push(r); first.add(this); } });
  // zone labels among themselves: the people label (ISRAEL) first; a zone label that would sit on top of
  // another one (PHILISTIA next to ISRAEL when zoomed far out) hides until there is room
  const zl = gZones.selectAll('text.zlabel').nodes().sort((a, b) => b.classList.contains('zl-people') - a.classList.contains('zl-people'));
  zl.forEach(t => {
    t.classList.remove('zcull');
    if (t.style.display === 'none' || +(getComputedStyle(t).opacity) < .5) return;
    const r = t.getBoundingClientRect(); if (!r.width) return;
    if (hit(r)) t.classList.add('zcull'); else boxes.push(r);
  });
  // transition labels (arrows, battles): newest first, they win over map labels
  [...document.querySelectorAll('#map .fxlab text, #map .battle .blab')].reverse().forEach(t => {
    t.classList.remove('nolabt'); const r = t.getBoundingClientRect(); if (!r.width) return;
    if (hit(r)) t.classList.add('nolabt'); else boxes.push(r);
  });
  const vis = [];
  gPts.selectAll('g.obj').each(function(d){ if (this.style.display !== 'none') vis.push([this, d]); });
  const pr = d => d.o.id === openId ? 0 : d.hl ? 1 : KEYSET.has(d.o.id) ? 2 : ((d.o.type === 'city' || d.o.type === 'site') ? 2.5 : 3) + d.o.rank;
  vis.sort((a, b) => pr(a[1]) - pr(b[1]));
  for (const [el, d] of vis){
    if (first.has(el)) continue;
    const lab = el.querySelector('.lab'); if (!lab) continue;
    const r = lab.getBoundingClientRect(); if (!r.width) continue;
    const clash = hit(r);
    el.classList.toggle('nolab', clash);
    if (!clash) boxes.push(r);
  }
}
let TR = {k:1, x:0, y:0};
const zoom = d3.zoom().scaleExtent([1, 160]).on('zoom', e => { TR = e.transform; K = e.transform.k; root.attr('transform', e.transform); scaleMarks(); });
svg.call(zoom).on('dblclick.zoom', null);
svg.append('defs').html('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.6"/></filter>');

async function getJSON(u){ if (!cache[u]) cache[u] = fetch(u).then(r => { if (!r.ok) throw new Error(u+' '+r.status); return r.json(); }); return cache[u]; }

function flyTo(c, k, ms = 900){
  const [w,h] = size(); const p = projection(c);
  // in the film the focus sits in the middle of the free picture: below the year, above the subtitles
  const f = filmFree();
  svg.transition().duration(ms).call(zoom.transform, d3.zoomIdentity.translate(w/2, f.cy).scale(k).translate(-p[0], -p[1]));
}
// the part of the film picture nothing covers: below the year bar and above the subtitle box (its source chip
// included). The player controls only show for a moment on a tap, so they do not count. Outside the film: all of it.
function filmFree(){
  const [w, h] = size();
  if (!(CINE && CINE.full)) return {top: 0, bot: h, cy: h / 2, w, h};
  const vb = $('vp').getBoundingClientRect(), cy = $('cyear'), cap = $('cap');
  const top = Math.min(h * .2, cy && cy.offsetHeight ? cy.getBoundingClientRect().bottom - vb.top + 6 : Math.min(h * .06, 46));
  let bot = h - 8;
  if (cap && !cap.hidden && cap.parentNode === $('vp')){
    for (const el of [$('captext'), $('capmeta')]){ if (el && el.offsetHeight) bot = Math.min(bot, el.getBoundingClientRect().top - vb.top - 6); }
  }
  bot = Math.max(bot, top + h * .45);   // a very long line never squeezes the picture below half the screen
  return {top, bot, cy: (top + bot) / 2, w, h};
}

// ---------- object geometry ----------
function midOf(feat){
  const g = feat.geometry; const lines = g.type === 'LineString' ? [g.coordinates] : g.coordinates;
  const L = lines.slice().sort((a,b) => b.length - a.length)[0]; return L[Math.floor(L.length/2)];
}
function placeObjects(){
  // where.at / where.line / where.river / where.lake / where.zone -> label point + geometry
  OBJS.forEach(o => {
    const w = o.where || {};
    if (w.at) o.pt = w.at;
    else if (w.line) { o.geo = {type:'Feature', geometry:{type:'LineString', coordinates:w.line}}; o.pt = w.line[Math.floor(w.line.length/2)]; }
    else if (w.river && RIVERS[w.river]) { o.geo = RIVERS[w.river]; o.pt = midOf(RIVERS[w.river][0]); }
    else if (w.lake && LAKES[w.lake]) { o.geo = LAKES[w.lake]; o.pt = d3.geoPath().centroid(LAKES[w.lake][0]); }
    else if (w.zone) o.zone = w.zone;
  });
}
// an object with "since" is drawn only from that stop's map on (e.g. sites added with c. 1150 BC)
const onMap = o => !o.since || (STOP && STOP.year >= o.since);
function drawObjects(){
  gLines.selectAll('*').remove(); gPts.selectAll('*').remove();
  // rivers and lakes: wide invisible hit path over the real line
  const lineObjs = OBJS.filter(o => o.geo && onMap(o));
  lineObjs.forEach(o => {
    const feats = Array.isArray(o.geo) ? o.geo : [o.geo];
    const g = gLines.append('g').attr('class', 'lobj t-' + o.type).datum(o);
    if (o.type === 'route') g.selectAll('path.route').data(feats).join('path').attr('class','route');
    g.selectAll('path.glow').data(feats).join('path').attr('class','glow');
    g.selectAll('path.lhit').data(feats).join('path').attr('class','lhit tap').on('click', (e) => { e.stopPropagation(); openObj(o.id); });
  });
  // area labels (regions, seas, peoples, rivers) underneath, so city and site dots always win the tap
  const top = t => (t === 'city' || t === 'site') ? 1 : 0;
  const pts = OBJS.filter(o => o.pt && onMap(o)).map(o => ({o, pt:o.pt})).sort((a,b) => top(a.o.type) - top(b.o.type));
  const g = gPts.selectAll('g.obj').data(pts, d => d.o.id).join('g').attr('class', d => `obj t-${d.o.type} r-${d.o.rank}`);
  const inner = g.append('g').attr('class','inner');
  const pointy = t => t === 'city' || t === 'site';
  inner.append('circle').attr('class','hit tap').attr('r', d => top(d.o.type) ? 15 : 12).on('click', (e, d) => { e.stopPropagation(); openObj(d.o.id); });
  // the film's highlight: a soft pulsing ring around the place the narrator names (shown only on .hl while a film plays)
  inner.filter(d => pointy(d.o.type)).append('circle').attr('class','ring').attr('r', 8);
  inner.filter(d => d.o.type === 'city').append('circle').attr('class','dot').attr('r', d => d.o.rank === 1 ? 3 : 2.4);
  inner.filter(d => d.o.type === 'site').append('rect').attr('class','dot').attr('x',-2.2).attr('y',-2.2).attr('width',4.4).attr('height',4.4).attr('transform','rotate(45)');
  inner.append('text').attr('class','lab').attr('x', d => pointy(d.o.type) ? 4.5 : 0).attr('y', d => pointy(d.o.type) ? 3.6 : 3.5)
    .attr('text-anchor', d => pointy(d.o.type) ? 'start' : 'middle').text(d => d.o.name);
  redraw();
}
function setHighlight(ids){
  const s = new Set(ids || []);
  gPts.selectAll('g.obj').each(d => d.hl = s.has(d.o.id)).classed('hl', d => d.hl);
  gLines.selectAll('g.lobj').classed('hl', o => s.has(o.id));
  const zs = new Set(OBJS.filter(o => s.has(o.id) && o.zone).map(o => o.zone));
  gZones.selectAll('path.zone, path.israel').classed('hl', f => zs.has(f.properties.zone));
  scaleMarks();
}

// ---------- zones (shared era layer) ----------
function centroidOf(features){
  const pick = features.slice().sort((a,b) => (b.properties.certainty==='sure') - (a.properties.certainty==='sure') || d3.geoPath().area(b) - d3.geoPath().area(a))[0];
  return d3.geoPath().centroid(pick);
}
function centroidLonLat(f){ const b = d3.geoBounds(f); return [(b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2]; }
const zoneObj = z => OBJ[ERA.zoneObjects[z]];
function drawZones(era){
  gZones.selectAll('*').remove();
  if (!era) return;
  const g = gZones.append('g');
  const feats = era.zones.features;
  const states = feats.filter(f => f.properties.certainty !== 'people');
  const people = feats.filter(f => f.properties.certainty === 'people');
  const open = (e, z) => { e.stopPropagation(); openObj(ERA.zoneObjects[z]); };
  g.selectAll('path.halo').data(states.filter(f => f.properties.certainty === 'unsure')).join('path').attr('class', f => 'halo z-' + f.properties.zone);
  g.selectAll('path.zone').data(states).join('path').attr('class', f => `zone tap ${f.properties.certainty} z-${f.properties.zone}`)
    .on('click', (e, f) => open(e, f.properties.zone));
  g.selectAll('path.israel').data(people).join('path').attr('class','israel tap').on('click', (e, f) => open(e, f.properties.zone));
  const ids = [...new Set(feats.map(f => f.properties.zone))];
  g.selectAll('text.zlabel').data(ids.map(id => ({id, c: (era.labelAt||{})[id] || centroidOf(feats.filter(f => f.properties.zone === id))}))).join('text')
    .attr('class', d => 'zlabel tap' + (d.id === 'israel' ? ' zl-people' : '')).text(d => (era.zoneLabels || {})[d.id] || zoneObj(d.id).name.replace(/ \(.*\)/,''))
    .attr('x', d => projection(d.c)[0]).attr('y', d => projection(d.c)[1])
    .on('click', (e, d) => open(e, d.id));
  // generous tap target for the small "people" area
  g.selectAll('circle.zhit').data(people.map(f => ({id:f.properties.zone, c:centroidLonLat(f)}))).join('circle').attr('class','zhit tap')
    .attr('r', 1).on('click', (e, d) => open(e, d.id));
  redrawZones();
}
// zone labels (ISRAEL in the hill country, PHILISTIA on the coast) sit among the sites; a tap on the word
// itself opens its zone even where a site's (larger) tap circle or another zone's tap area reaches under it
// (rivers and roads keep their own taps)
svg.node().addEventListener('click', e => {
  const c = e.target.classList; if (CINE || !c || !(c.contains('hit') || c.contains('zhit') || c.contains('israel') || c.contains('zone'))) return;
  for (const t of gZones.selectAll('text.zlabel').nodes()){
    const r = t.getBoundingClientRect(); if (!r.width || getComputedStyle(t).display === 'none' || +getComputedStyle(t).opacity === 0 || t.classList.contains('gone') || t.classList.contains('zcull')) continue;
    const z = t.__data__ && ERA.zoneObjects[t.__data__.id];
    if (z && e.clientX >= r.left && e.clientX <= r.right && e.clientY >= r.top && e.clientY <= r.bottom){ e.stopPropagation(); e.preventDefault(); openObj(z); return; }
  }
}, true);
function redrawZones(){
  gZones.selectAll('path').attr('d', path);
  gZones.selectAll('text.zlabel').attr('x', d => projection(d.c)[0]).attr('y', d => projection(d.c)[1]);
  gZones.selectAll('circle.zhit').attr('cx', d => projection(d.c)[0]).attr('cy', d => projection(d.c)[1]).attr('r', 12);
}

// ---------- small fact box ----------
const srcList = keys => '<ol>' + keys.map(k => { const s = SRC[k]; if (!s) return ''; const t = esc(s.t); return '<li>' + (s.url ? `<a href="${esc(s.url)}" target="_blank" rel="noopener">${t}</a>` : t) + (s.kind === 'tradition' ? ' ' + badge('tradition') : '') + '</li>'; }).join('') + '</ol>';
function openObj(id, fly){
  const o = OBJ[id]; if (!o) return;
  openId = id; markExplored(id); if (PLAY && !PLAY.paused) playPause();
  let zoneParts = '';
  if (o.zone && ERA){
    const lab = {sure:'Solid: core well documented', unsure:'Dashed: extent uncertain', people:'Gold: a people, no border'};
    zoneParts = '<div class="area">' + ERA.zones.features.concat(FXZ).filter(f => f.properties.zone === o.zone).map(f => `<span>${esc(lab[f.properties.certainty])} · ${esc(f.properties.part)}</span>`).join('') + '</div>';
  }
  const stats = [];
  if (o.people) stats.push(`<div class="row"><b>People</b><span>${esc(o.people)}</span></div>`);
  if (o.pop) stats.push(`<div class="row"><b>Population</b><span>${esc(o.pop.v)} ${badge(o.pop.cert)}</span></div>`);
  const allSrc = [...new Set([...(o.src||[]), ...((o.pop||{}).src||[]), ...(o.facts||[]).flatMap(f => f[2])])];
  $('popbody').innerHTML =
    `<div class="pk">${icon(o.type)}<span>${TYPE[o.type]||o.type}</span>${badge(o.cert)}</div>` +
    `<h3 id="pt">${esc(o.name)}</h3>` + (o.alt ? `<div class="alt">Also: ${esc(o.alt)}</div>` : '') +
    `<p class="desc">${esc(o.desc)}</p>` + stats.join('') +
    ((o.facts||[]).length ? '<ul class="claims">' + o.facts.map(f => `<li>${badge(f[1])} ${esc(f[0])}</li>`).join('') + '</ul>' : '') +
    zoneParts +
    `<details class="src"><summary>Sources (${allSrc.length})</summary>${srcList(allSrc)}${o.zone && ERA ? '<p class="cap">'+esc(ERA.note)+'</p>' : ''}</details>`;
  $('pop').hidden = false; $('pop').scrollTop = 0;
  document.body.classList.add('popopen');
  gPts.selectAll('g.obj').classed('sel', d => d.o.id === id);
  gLines.selectAll('g.lobj').classed('sel', d => d.id === id);
  if (fly && o.pt) flyTo(o.pt, Math.max(K, showAt(o.rank, o.type) + 1.5));
  scaleMarks();
}
function closeObj(){ const was = openId; openId = null; if (was) setTimeout(scaleMarks, 0); $('pop').hidden = true; document.body.classList.remove('popopen'); gPts.selectAll('g.obj').classed('sel', false); gLines.selectAll('g.lobj').classed('sel', false); }
$('popx').onclick = e => { e.stopPropagation(); closeObj(); };
document.addEventListener('click', e => {
  if ($('pop').hidden) return;
  if (e.target.closest('#pop') || e.target.closest('.tap') || e.target.closest('.chip')) return;
  closeObj();
});
addEventListener('keydown', e => { if (e.key === 'Escape') closeObj(); });

// ---------- explore progress: key objects per stop, saved on this device ----------
let KEYSET = new Set(), EXPLORED = new Set();
const xpKey = () => `tlm.explored.${STORY.id}.${STOP.year}`;
function loadExplored(){
  KEYSET = new Set(STOP && STOP.explore ? STOP.explore.key : []);
  try { EXPLORED = new Set(JSON.parse(localStorage.getItem(xpKey()) || '[]').filter(id => KEYSET.has(id))); } catch(e){ EXPLORED = new Set(); }
}
function saveExplored(){ try { localStorage.setItem(xpKey(), JSON.stringify([...EXPLORED])); } catch(e){} }
function markExplored(id){
  if (MODE !== 'stop' || !KEYSET.has(id) || EXPLORED.has(id)) return;
  EXPLORED.add(id); saveExplored(); drawKeys();
  if (steps()[step] && steps()[step].explore) renderChecklist();
}
function keyPt(id){
  const o = OBJ[id]; if (!o) return null;
  if (o.pt) return o.pt;
  if (o.zone && ERA){ const z = Object.keys(ERA.zoneObjects).find(k => ERA.zoneObjects[k] === id); if (z && ERA.labelAt && ERA.labelAt[z]) return ERA.labelAt[z]; }
  return null;
}
function drawKeys(){
  gKey.selectAll('*').remove();
  const show = MODE === 'stop' && !PLAY;
  $('xp').hidden = !show || !KEYSET.size;
  if (!show) return;
  const data = [...KEYSET].map(id => ({id, pt:keyPt(id), done:EXPLORED.has(id)})).filter(d => d.pt);
  const g = gKey.selectAll('g.key').data(data).join('g').attr('class', d => 'key ' + (d.done ? 'done' : 'todo'));
  g.filter(d => !d.done).append('circle').attr('class','ring').attr('r', 9);
  const c = g.filter(d => d.done).append('g').attr('transform','translate(7,-9)');
  c.append('circle').attr('class','chk').attr('r', 5);
  c.append('path').attr('class','chkm nogeo').attr('d','M-2.4 0.2 -0.6 2 2.6 -1.8');
  $('xpn').textContent = `${EXPLORED.size}/${KEYSET.size}`;
  $('xp').classList.toggle('all', EXPLORED.size === KEYSET.size);
  scaleMarks();
}
$('xp').onclick = e => { e.stopPropagation(); showStep(steps().length - 1); };
function renderChecklist(){
  const box = $('evbody').querySelector('.checklist'); if (!box) return;
  box.innerHTML = [...KEYSET].map(id => { const o = OBJ[id], d = EXPLORED.has(id);
    return `<li><button type="button" class="ck${d ? ' done' : ''}" data-o="${id}"><span class="box" aria-hidden="true">${d ? '✓' : ''}</span>${icon(o.type)}<span class="nm">${esc(o.name)}</span><span class="sr">${d ? 'explored' : 'not yet explored'}</span></button></li>`; }).join('');
  box.querySelectorAll('.ck').forEach(b => b.onclick = ev => { ev.stopPropagation(); openObj(b.dataset.o, true); });
  const n = $('evbody').querySelector('.xpcount'); if (n) n.textContent = `${EXPLORED.size}/${KEYSET.size} explored`;
}

// ---------- big fact box: intro -> events -> explore + Play ----------
function steps(){ return STOP ? [{intro:true}, ...STOP.events, {explore:true}] : []; }
const chips = ids => '<div class="chips">' + ids.map(id => OBJ[id] ? `<button type="button" class="chip" data-o="${id}">${icon(OBJ[id].type)}${esc(OBJ[id].name)}</button>` : '').join('') + '</div>';
function showStep(i, fly = true){
  if (MODE !== 'stop') return;
  const S = steps(); if (!S.length) return;
  step = Math.max(0, Math.min(S.length - 1, i));
  const e = S[step], last = step === S.length - 1;
  let h;
  if (e.intro){
    // just arrived here from the previous chapter's Play: one big button straight into this chapter
    const arr = ARRIVE === cur && chapNo(cur);
    h = `<div class="kicker">${esc(STORY.title)} · ${esc(STOP.label)}</div><h2>${esc(STOP.title)}</h2>` +
        (arr ? `<div class="cta arrive"><button type="button" class="play big" id="gonextch" data-part="${cur}" data-how="${posGet(STOP.year) ? 'resume' : 'over'}">Continue to Chapter ${arr} ▶</button></div>` : '') + partList() +
        `<p class="lead">${esc(STORY.intro)}</p><p>${esc(tinText())}</p>` +
        (tinBeats() ? `<div class="cta"><button type="button" class="play" id="gostory">▶ Watch the opening · ${minsOf(reelChapters('intro')[0].ms)}</button><button type="button" id="goexplore">Explore the map</button></div>` +
            resumeHere('goresume') + chapterList('intro') +
            (STOP.events.length ? `<p class="cap"><button type="button" class="linkish" id="goread">Or read it as fact boxes ›</button></p>` : '')
          : `<div class="cta"><button type="button" class="play" id="gostory">Start the story ›</button><button type="button" id="goexplore">Explore the map</button></div>`) +
        `<div class="sub">Key places and peoples</div>${chips(STOP.keyObjects)}` +
        `<div class="legend2">${badge('attested')} found in ancient evidence · ${badge('disputed')} scholars disagree · ${badge('tradition')} Jewish tradition and the Hebrew Bible</div>`;
  } else if (e.explore){
    const pl = STOP.play;
    h = `<div class="kicker">${esc(STOP.label)} · Explore</div><h2>Explore ${esc(STOP.label)}</h2>` +
        resumeHere('xpresume') + `<p>${esc(STOP.explore.text)}</p>` +
        `<div class="sub xpcount"></div><ul class="checklist"></ul>` +
        `<button type="button" class="linkish" id="xpreset">Reset progress</button>` +
        (pl ? `<div class="next"><div class="sub">Next</div><p>${esc(STOP.transitionOut.text)}</p>` +
              `<button type="button" class="play big" id="playbtn">▶ Play: ${esc(pl.title)}</button><p class="cap">About ${Math.max(1, Math.round(playTotal() / 60000))} minutes, in ${reelChapters('play').length} scenes. ${esc(pl.intro)}</p>` +
              chapterList('play') + '</div>' : '');
  } else {
    h = `<div class="kicker">${esc(e.kicker)} · ${esc(e.date)}</div><h2>${esc(e.title)} ${badge(e.cert)}</h2>` +
        `<p class="lead">${esc(e.text)}</p>` +
        `<div class="why"><div class="sub">What it meant for Israel</div><p>${esc(e.why)}</p></div>` +
        (e.pic ? `<img class="shot" alt="" src="${esc(e.pic.src)}"><p class="cap">${esc(e.pic.cap)}</p>` : '') +
        `<div class="sub">The evidence</div><ul class="claims">` + e.claims.map(c => `<li>${badge(c[1])} ${esc(c[0])}</li>`).join('') + '</ul>' +
        `<div class="sub">On the map</div>${chips(e.objects)}` +
        `<details class="src"><summary>Sources (${e.src.length})</summary>${srcList(e.src)}</details>`;
  }
  $('evbody').innerHTML = h; $('evbody').scrollTop = 0;
  $('evn').textContent = `${step + 1} / ${S.length}`;
  $('evprev').disabled = step === 0; $('evnext').disabled = last;
  $('evbody').querySelectorAll('.chip').forEach(b => b.onclick = ev => { ev.stopPropagation(); openObj(b.dataset.o, true); });
  if (e.intro){
    $('gostory').onclick = ev => { ev.stopPropagation(); tinBeats() ? playStart('intro') : showStep(1); };
    $('goexplore').onclick = () => showStep(S.length - 1);
    if ($('goread')) $('goread').onclick = () => showStep(1);
  }
  $('evbody').querySelectorAll('[data-reel]').forEach(b => b.onclick = ev => { ev.stopPropagation(); playStart(b.dataset.reel, +b.dataset.b); });
  $('evbody').querySelectorAll('[data-part]').forEach(b => b.onclick = ev => { ev.stopPropagation(); partStart(+b.dataset.part, b.dataset.how); });
  if (e.explore){
    renderChecklist();
    $('xpreset').onclick = ev => { ev.stopPropagation(); EXPLORED.clear(); saveExplored(); drawKeys(); renderChecklist(); };
    if ($('playbtn')) $('playbtn').onclick = ev => { ev.stopPropagation(); playStart(); };
  }
  closeObj();
  setHighlight(e.intro ? STOP.keyObjects : e.explore ? [] : e.hl);
  if (fly) { if (e.intro || e.explore) flyTo([35.6, 33.2], e.explore ? 3.2 : 1.6); else flyTo(e.focus.c, e.focus.k); }
}
$('evprev').onclick = () => showStep(step - 1);
$('evnext').onclick = () => showStep(step + 1);

// ---------- narrated films ("reels"): the opening film of a stop (transitionIn.beats) and Play ----------
// transitionIn is either a plain string (older stops) or {text, beats}; beats run like Play's.
const tinText = () => !STOP ? '' : typeof STOP.transitionIn === 'string' ? STOP.transitionIn : (STOP.transitionIn && STOP.transitionIn.text) || '';
const tinBeats = () => STOP && STOP.transitionIn && typeof STOP.transitionIn === 'object' && STOP.transitionIn.beats && STOP.transitionIn.beats.length ? STOP.transitionIn.beats : null;
const reelBeats = r => r === 'intro' ? tinBeats() : STOP && STOP.play ? STOP.play.beats : null;
const reelAmbient = r => r === 'intro' ? (STOP.transitionIn.ambient || null) : (STOP.play.ambient || null);
const minsOf = ms => ms < 90000 ? 'about ' + Math.max(1, Math.round(ms / 60000)) + ' minute' : 'about ' + Math.round(ms / 60000) + ' minutes';
// chapters: a beat with "chapter" opens one; each runs to the next. ms = planned length at 1x.
function reelChapters(r){
  const bs = reelBeats(r) || [], out = [];
  bs.forEach((b, i) => { if (b.chapter || !out.length) out.push({title: b.chapter || '', i, ms: 0}); out[out.length - 1].ms += beatPlan(b); });
  out.forEach((c, k) => { c.end = k + 1 < out.length ? out[k + 1].i : bs.length; c.n = k + 1; });
  return out;
}
const chapterAt = (r, i) => { const cs = reelChapters(r); let c = cs[0]; cs.forEach(x => { if (x.i <= i) c = x; }); return c; };
const mmss = ms => { const s = Math.round(ms / 1000); return Math.floor(s / 60) + ':' + String(s % 60).padStart(2, '0'); };
// resume: the line to come back to, per stop and film, on this device (tlm.resume.<story>.<year>.<reel> = beat index;
// older versions stored the first beat of the scene there, which still works)
const resumeKey = (r, y = STOP && STOP.year) => `tlm.resume.${STORY && STORY.id}.${y}.${r}`;
function resumeGet(r){ try { const v = +localStorage.getItem(resumeKey(r)); const bs = reelBeats(r); return v > 0 && bs && v < bs.length ? v : 0; } catch(e){ return 0; } }
function resumeSet(r, i){ try { i > 0 ? localStorage.setItem(resumeKey(r), String(i)) : localStorage.removeItem(resumeKey(r)); } catch(e){} }
// the place in a whole chapter (stop) to come back to: tlm.pos.<story>.<year> = {r: reel, i: line, t: ms into the chapter}.
// Saved at every line while a film plays (so leaving, pausing or closing the page keeps it), cleared when the chapter ends.
const posKey = y => `tlm.pos.${STORY && STORY.id}.${y}`;
function posGet(y){
  let p = null;
  try { p = JSON.parse(localStorage.getItem(posKey(y)) || 'null'); } catch(e){ p = null; }
  if (p && !((p.r === 'intro' || p.r === 'play') && Number.isInteger(p.i) && p.i >= 0 && p.t >= 0)) p = null;
  const here = STOP && STOP.year === y;
  if (p && here){ const bs = reelBeats(p.r); if (!bs || p.i >= bs.length) p = null; }
  // progress saved before tlm.pos existed: the old per-film keys
  if (!p && here){ const ip = resumeGet('play'), ii = resumeGet('intro'); if (ip) p = {r: 'play', i: ip, t: posMs('play', ip)}; else if (ii) p = {r: 'intro', i: ii, t: posMs('intro', ii)}; }
  return p;
}
const posMs = (r, i) => (r === 'play' && tinBeats() ? playTotal('intro') : 0) + (reelBeats(r) || []).slice(0, i).reduce((s, b) => s + beatPlan(b), 0);
function posSet(r, i){ if (!STOP) return; try { localStorage.setItem(posKey(STOP.year), JSON.stringify({r, i, t: Math.round(posMs(r, i))})); } catch(e){} }
function posClear(y){ try { localStorage.removeItem(posKey(y)); ['intro', 'play'].forEach(r => localStorage.removeItem(resumeKey(r, y))); } catch(e){} }
const chapNo = k => parts().findIndex(x => x.k === k) + 1;
// "Resume" near the top of the stop's panel (under Watch the opening, and on the Explore step), with a small Start over
function resumeHere(id){
  const p = STOP && posGet(STOP.year); if (!p) return '';
  const sc = chapterAt(p.r, p.i), n = chapNo(cur);
  return `<div class="resumebox"><button type="button" class="resume" id="${id}" data-part="${cur}" data-how="resume">▶ Resume${n ? ' Chapter ' + n : ''} at ${mmss(p.t)}${sc && sc.title ? ' · ' + esc(sc.title) : ''}</button>` +
    `<button type="button" class="linkish over" data-part="${cur}" data-how="over">Start over</button></div>`;
}
function chapterList(r){
  const cs = reelChapters(r); if (cs.length < 2) return '';
  return `<div class="sub">Scenes</div><ol class="chlist">` + cs.map(c => `<li><button type="button" class="chb" data-reel="${r}" data-b="${c.i}"><span class="cn">${c.n}</span><span class="ct">${esc(c.title)}</span><span class="cm">${mmss(c.ms)}</span></button></li>`).join('') + '</ol>';
}
// parts: every built stop is one chapter of the book (shown as Chapter 1 = 1207 BC, Chapter 2 = c. 1150 BC, ...;
// in the code they are still "parts", and the chapter strip inside a film shows "scenes").
// The intro step lists them, so a part can be started directly; a part counts as watched on this
// device once its opening film or its Play has run to the end (localStorage tlm.done.<story>.<year>).
const doneKey = y => `tlm.done.${STORY && STORY.id}.${y}`;
const partDone = y => { try { return localStorage.getItem(doneKey(y)) === '1'; } catch(e){ return false; } };
function partSet(){ try { if (STOP) localStorage.setItem(doneKey(STOP.year), '1'); } catch(e){} }
const parts = () => STORY.stops.map((s, k) => ({s, k})).filter(x => x.s.file);
function partList(){
  const ps = parts(); if (ps.length < 2) return '';
  const here = ps.findIndex(x => x.k === cur), nx = ps[here + 1];
  // the next part is preloaded, so a tap starts its film at once
  if (nx){ getJSON(nx.s.file).catch(() => {}); getJSON(nx.s.era).catch(() => {}); }
  return `<div class="sub">Chapters</div><ol class="plist parts">` + ps.map((x, n) => {
    const me = x.k === cur, pos = posGet(x.s.year), next = !pos && nx && x.k === nx.k && partDone(STOP.year);
    // a chapter that was started but not finished: Resume (with the time), and a small Start over under it
    const tag = pos ? `Resume ▶ (${mmss(pos.t)})` : me ? 'You are here' : next ? 'Continue ▶' : partDone(x.s.year) ? '✓ Watched' : 'Start ▶';
    return `<li><button type="button" class="chb part${me && !pos ? ' here' : ''}${next || pos ? ' gonext' : ''}" data-part="${x.k}"${pos ? ' data-how="resume"' : ''}${me ? ' aria-current="true"' : ''}>` +
      `<span class="cn">${n + 1}</span><span class="ct"><b>Chapter ${n + 1}</b> · ${esc(x.s.label)} · ${esc(x.s.title)}</span><span class="cm">${tag}</span></button>` +
      (pos ? `<button type="button" class="linkish over" data-part="${x.k}" data-how="over">Start over</button>` : '') + '</li>'; }).join('') + '</ol>';
}
// start a part's opening film; another part first opens its stop (inside the tap, so sound and full screen are allowed).
// how: 'resume' continues at the saved line (map rebuilt to that moment), 'over' forgets the saved place and starts again
async function partStart(k, how){
  const y = STORY.stops[k] && STORY.stops[k].year;
  if (how === 'over') posClear(y);
  const here = k === cur && MODE === 'stop';
  let p = how === 'resume' ? posGet(y) : null;
  if (here && !p && how !== 'over') return; // 'You are here'
  sndEnsure(); enterCine();
  if (!here){ await go(k); $('cyear').textContent = $('pill').textContent; if (how === 'resume') p = posGet(y); }
  if (MODE !== 'stop') return exitCine();
  if (p && reelBeats(p.r)) playStart(p.r, p.i);
  else if (tinBeats()) playStart('intro'); else exitCine();
}
// the narrator's voice has its own switch (default on, also with reduced motion); effects are separate
let VOICE = true;
try { VOICE = localStorage.getItem('tlm.voice') !== 'off'; } catch(e){}
const AUD = {};   // Audio objects by file, created during a film only (after the click), the next line preloaded
function audioFor(src){ let a = AUD[src]; if (!a){ a = AUD[src] = new Audio(); a.preload = 'auto'; a.src = src; } return a; }
function preload(b){ if (b && b.audio && VOICE) audioFor(b.audio); }

// ---------- Play: timed transition to the next stop ----------
// A beat runs its steps together (caption, focus, migration, border, battle, year); beats run in order.
let PLAY = null, FXZ = [], YEAR = null;
const shortSrc = k => { const s = SRC[k]; if (!s) return k; const m = s.t.match(/^([^,(.]+?)(?:,| et al\.| &)[^(]*\((\d{4})\)/); if (m) return m[1].trim() + (/ et al\./.test(s.t.slice(0, 40)) ? ' et al.' : '') + ' ' + m[2]; if (s.kind === 'tradition') return 'Hebrew Bible'; return s.t.split(/[.(]/)[0].trim().slice(0, 40); };
const yfmt = (y, c) => (c ? 'c. ' : '') + fmt(Math.round(y));
function setYear(y, approx){ YEAR = y; const t = yfmt(y, approx); $('big').textContent = t; $('pill').textContent = t; $('cyear').textContent = t; }
// ---------- review mode (temporary): ?review=1 turns it on (remembered), ?review=0 turns it off ----------
// a small 'Ch2 · #14 · 3:12' tag on the subtitle box so fixes can be reported by line and time; normal visitors never see it
const REVIEW = (() => { try { const q = new URLSearchParams(location.search).get('review');
  if (q === '1') localStorage.setItem('tlm.review', '1'); else if (q === '0') localStorage.removeItem('tlm.review');
  return localStorage.getItem('tlm.review') === '1'; } catch(e){ return false; } })();
const mss = ms => { const t = Math.max(0, Math.floor(ms / 1000)); return Math.floor(t / 60) + ':' + String(t % 60).padStart(2, '0'); };
function reviewTag(){
  if (!REVIEW || !PLAY || !STOP || !PLAY.beats) return;
  let e = $('revtag'); if (!e){ e = document.createElement('div'); e.id = 'revtag'; e.setAttribute('aria-hidden', 'true'); $('capmeta').appendChild(e); }
  // line = 1-based index in this reel's beats (the order in the narration data); time = elapsed in the chapter, opening included
  const t = posMs(PLAY.reel, PLAY.i) + Math.max(0, PLAY.clock - (PLAY.t0 || 0));
  const s = 'Ch' + chapNo(cur) + ' · ' + (PLAY.reel === 'intro' ? 'opening ' : '') + '#' + (PLAY.i + 1) + ' · ' + mss(t);
  if (e.textContent !== s) e.textContent = s;
}
// ---------- Play: one virtual clock, so pause, speed and step all stay in sync ----------
// Timing rules (see build/README.md): the caption line drives the beat. Camera first, then the
// visual events one at a time, then the line must have finished (reading time or audio), then pauseAfter.
const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
const ANIM = {year:2000, focus:2000, migration:3200, battle:3000, border:3000};
const GAP = 400;
const dur = x => x.duration || ANIM[x.type] || 0;
function anim(ms, fn){ if (!ms || !PLAY || !PLAY.clockOn){ fn(1); return; } const a = {t0:PLAY.clock, ms, fn}; PLAY.anims.push(a); fn(0); }
function at(t, fn){ PLAY.events.push({t, fn}); }
function tick(now){
  if (!PLAY) return;
  const dt = Math.min(100, now - (PLAY.last || now)); PLAY.last = now;
  if (!PLAY.paused && !PLAY.hold && !PLAY.wait) PLAY.clock += dt * SPEED;   // wait: the opener's choice
  audioWatch(now); reviewTag();
  const c = PLAY.clock;
  PLAY.anims = PLAY.anims.filter(a => { const f = Math.min(1, Math.max(0, (c - a.t0) / a.ms)); a.fn(ease(f)); return f < 1; });
  if (PLAY.anims.length) scaleMarks();
  for (;;){
    PLAY.events.sort((a, b) => a.t - b.t);
    if (!PLAY.events.length || PLAY.events[0].t > c) break;
    PLAY.events.shift().fn(); if (!PLAY) return;
  }
  if (PLAY.bEnd) $('capbar').style.width = Math.min(100, 100 * (PLAY.clock - PLAY.b0) / (PLAY.bEnd - PLAY.b0)) + '%';
  PLAY.raf = requestAnimationFrame(tick);
}
// watchdog for the narrator's clip: if its time does not move for STALL_MS while the film runs
// (stalled download, the phone paused it, a failed play()), retry once, then skip it
const STALL_MS = 2500;
function audioWatch(now){
  const w = PLAY && PLAY.aw; if (!w || PLAY.audio !== w.a) return;
  if (PLAY.paused || w.a.ended){ w.t = now; return; }
  if (w.a.currentTime !== w.last){ w.last = w.a.currentTime; w.t = now; return; }
  if (now - w.t > STALL_MS){ w.t = now; w.retry(); }
}
function tweenYear(to, ms){
  const from = YEAR == null ? STOP.year : YEAR;
  anim(ms, f => setYear(from + (to - from) * f, from !== to || to !== STOP.year));
}
// short hops on a regional map: planar lon/lat with a cos(lat) factor is accurate enough
const gDist = (a, b) => Math.hypot((b[0]-a[0]) * Math.cos((a[1]+b[1]) * Math.PI / 360), b[1]-a[1]);
const gLerp = (a, b) => t => [a[0] + (b[0]-a[0]) * t, a[1] + (b[1]-a[1]) * t];
function partial(coords, f){
  const d = []; let tot = 0;
  for (let i = 1; i < coords.length; i++){ d.push(gDist(coords[i-1], coords[i])); tot += d[i-1]; }
  let want = tot * f; const out = [coords[0]];
  for (let i = 1; i < coords.length; i++){
    if (want >= d[i-1]){ out.push(coords[i]); want -= d[i-1]; continue; }
    out.push(gLerp(coords[i-1], coords[i])(want / d[i-1])); break;
  }
  if (out.length < 2) out.push(gLerp(coords[0], coords[1])(0.001));
  return out;
}
const fade = (sel, to, ms) => { const from = +(sel.style('opacity') || 1); anim(ms, f => sel.style('opacity', from + (to - from) * f)); };
function arrow(layer, coords, cls, ms, label){
  const g = layer.append('g').attr('class', 'arrow ' + cls);
  const line = g.append('path').attr('class','shaft');
  const tip = g.append('g').attr('class','tip'); tip.append('path').attr('class','nogeo').attr('d','M-9 -5.5 L2 0 L-9 5.5 z');
  const set = f => { const c = partial(coords, Math.max(0.001, f)); line.datum({type:'Feature', geometry:{type:'LineString', coordinates:c}}).attr('d', path); tip.datum({a:c[c.length-2], b:c[c.length-1]}); };
  let lab = null;
  if (label){ lab = layer.append('g').attr('class','fxm fxlab ' + cls).datum({pt: coords[Math.floor(coords.length/2)]}); lab.append('text').attr('y', -7).text(label); }
  if (!ms){ set(1); return; }
  if (lab) lab.style('opacity', 0);
  anim(ms * 0.8, set);
  if (lab) at(PLAY.clock + ms * 0.8, () => fade(lab, 1, ms * 0.2));
}
// a narrated line about one place, or a few places close together, zooms in until they fill a good part of
// the screen: the k in the data is only a minimum. Lines about a whole land, a people, a river or a route keep
// their wide shot. The view always keeps some land around the place (SPAN, in degrees, by kind of place).
const SPAN = o => o.type === 'region' ? 1.3 : o.rank === 1 ? 2.2 : o.rank === 2 ? 1.4 : 0.5;
const placeLike = o => o && o.pt && o.where && o.where.at && (o.type === 'city' || o.type === 'site' || (o.type === 'region' && o.rank >= 3));
function focusView(x){
  const os = (x.hl || []).map(id => OBJ[id]);
  if (!os.length || !os.every(placeLike)) return {c: x.c, k: x.k};
  const [w, h] = size();
  // the free picture: in the film the subtitles cover the bottom and the year the top. The place and its SPAN
  // fill about half of the free height, so the bigger picture shows more of the land around it
  const f = filmFree();
  const aw = w * 0.72, ah = Math.max(120, (f.bot - f.top) * (CINE && CINE.full ? 0.5 : 0.62));
  const ps = os.map(o => projection(o.pt)), xs = ps.map(p => p[0]), ys = ps.map(p => p[1]);
  const deg = Math.abs(projection([36, 31.8])[0] - projection([35, 31.8])[0]);
  const m = Math.min(...os.map(SPAN)) * deg;
  const bw = Math.max(m, Math.max(...xs) - Math.min(...xs)), bh = Math.max(m, Math.max(...ys) - Math.min(...ys));
  // labels sit to the right of their dots: keep LABW screen pixels free on the right, and shift the picture to match
  const LABW = 84, k = Math.min(150, (aw - LABW) / bw, ah / bh);
  if (k <= x.k) return {c: x.c, k: x.k};
  return {c: projection.invert([(Math.max(...xs) + Math.min(...xs)) / 2 + LABW / 2 / k, (Math.max(...ys) + Math.min(...ys)) / 2]), k};
}
function flyFocus(x, ms){ const v = focusView(x); flyTo(v.c, v.k, ms); }
const CERTTXT = c => c === 'disputed' ? ' · Disputed' : '';
const STEP = {
  year: (x, ms) => tweenYear(x.to, ms),
  focus: (x, ms) => { setHighlight(x.hl || []); PLAY.lastFocus = x; if (ms) flyFocus(x, ms / SPEED); },
  migration: (x, ms) => arrow(gFx, x.path, 'mig' + (x.cert === 'disputed' ? ' unsure' : ''), ms, x.label + CERTTXT(x.cert)),
  battle: (x, ms) => {
    // the armies' arrows first, then the battle marker
    (x.arrows || []).forEach(a => arrow(gFx, a.path, 'army side-' + a.side + (a.cert === 'disputed' ? ' unsure' : ''), ms * 0.6));
    const mark = () => {
      const g = gFxTop.append('g').attr('class','fxm battle' + (x.cert === 'disputed' ? ' unsure' : '')).datum({pt:x.at});
      g.append('circle').attr('class','pulse').attr('r', 14); g.append('circle').attr('class','core').attr('r', 7);
      g.append('path').attr('class','swords nogeo').attr('d','M-4 -4 4 4 M4 -4 -4 4');
      g.append('text').attr('class','blab').attr('x', 11).attr('y', 4).text(x.label + CERTTXT(x.cert));
      scaleMarks(); if (ms){ g.style('opacity', 0); fade(g, 1, ms * 0.4); }
    };
    if (ms) at(PLAY.clock + ms * 0.6, mark); else mark();
  },
  border: (x, ms) => {
    // one crossfade: old shapes fade while new ones appear
    (x.fade || []).forEach(f => {
      const m = z => z.properties.zone === f.zone && (!f.certainty || z.properties.certainty === f.certainty);
      const els = gZones.selectAll('path.zone, path.israel, path.halo').filter(m).classed('gone', true).style('pointer-events','none');
      ms ? fade(els, .14, ms) : els.style('opacity', .14);
      if (!f.certainty){ const t = gZones.selectAll('text.zlabel').filter(z => z.id === f.zone).classed('gone', true).style('pointer-events','none'); ms ? fade(t, 0, ms) : t.style('opacity', 0); }
    });
    (x.add || []).forEach(a => {
      const feat = rewind({type:'Feature', properties:{zone:a.zone, certainty:a.certainty, part:`Drawn for ${playToLabel()}: extent uncertain`}, geometry:{type:'Polygon', coordinates:[a.coords]}});
      FXZ.push(feat);
      const g = gZones.select('g');
      const el = a.certainty === 'people' ? g.append('path').attr('class',`israel tap added z-${a.zone}`) : g.append('path').attr('class', `zone tap unsure added z-${a.zone}`);
      el.datum(feat).attr('d', path).on('click', e => { e.stopPropagation(); openObj(ERA.zoneObjects[a.zone]); });
      const t = g.append('text').datum({id:a.zone, c:a.labelAt}).attr('class', 'zlabel tap added' + (a.certainty === 'people' ? ' zl-people' : '')).text(a.label)
        .on('click', e => { e.stopPropagation(); openObj(ERA.zoneObjects[a.zone]); });
      if (ms){ el.style('opacity', 0); t.style('opacity', 0); fade(el, 1, ms); fade(t, 1, ms); }
      redrawZones(); scaleMarks();
    });
  },
  caption: (x, ms) => {
    if (!ms) return;
    // subtitles show digits ("display") while the voice reads the words ("text")
    $('captext').innerHTML = (badge(x.cert) ? badge(x.cert) + ' ' : '') + esc(x.display || x.text);
    $('capsrc').textContent = x.cert === 'scene' ? 'Scene-setting only: no new facts.' : x.cert === 'frame' ? '' : 'Sources: ' + x.src.map(shortSrc).join('; ') + (x.ref ? ' · ' + x.ref : '');
    $('cap').classList.toggle('frame', x.cert === 'frame');
    $('capsrc').title = x.src.map(k => SRC[k] ? SRC[k].t : k).join('\n');
    const c = $('cap'); c.classList.remove('in'); void c.offsetWidth; c.classList.add('in');
  }
};
const words = t => t.split(/\s+/).length;
// reading time ~2.5 words per second, at least 2 s (make_data.py writes this as beat.duration)
// with the voice on, a recorded line lasts as long as its audio (audioMs, measured when it was recorded)
const lineMs = b => { if (VOICE && b.audio && b.audioMs) return b.audioMs; const c = b.steps.find(x => x.type === 'caption'); return b.duration || Math.max(2000, Math.round(words(c ? c.text : '') / 2.5 * 1000)); };
const pauseMs = b => b.pauseAfter == null ? 600 : b.pauseAfter;
// the gap after a line: short and natural (pauseAfter, ~0.6 s); with sound on a battle or march may
// stretch it so its effect can swell (sfxHold), but no breathing moment is longer than BREATH_MAX
const BREATH_MAX = 2000;
const breathMs = b => { const h = holdMs(b); return h ? Math.min(BREATH_MAX, Math.max(pauseMs(b), h)) : pauseMs(b); };
const VISUAL = ['migration', 'battle', 'border'];
// planned length of one beat at 1x (without audio)
function beatPlan(b){
  let t = 0; const f = b.steps.find(x => x.type === 'focus'); if (f) t += dur(f) + GAP;
  b.steps.filter(x => VISUAL.includes(x.type)).forEach(x => { t += dur(x) + GAP; });
  return Math.max(lineMs(b), t) + breathMs(b);
}
const playTotal = (r = 'play') => (reelBeats(r) || []).reduce((s, b) => s + beatPlan(b), 0);
function clearFx(){ gFx.selectAll('*').interrupt().remove(); gFxTop.selectAll('*').remove(); FXZ = []; }
function resetMap(){ clearFx(); drawZones(ERA); drawObjects(); }
function applyInstant(i){ PLAY.beats[i].steps.forEach(x => { if (x.type !== 'caption') STEP[x.type](x, 0); }); }
function runBeat(i){
  if (i >= PLAY.beats.length) return PLAY.reel === 'intro' ? introEnd() : playEnd();
  const b = PLAY.beats[i], t0 = PLAY.clock;
  PLAY.i = i; PLAY.events = []; PLAY.hold = false; PLAY.wait = false; PLAY.sndUsed = new Set(); hideChoice();
  PLAY.tok = (PLAY.tok || 0) + 1;
  if (PLAY.audio){ PLAY.audio.onended = PLAY.audio.onerror = null; PLAY.audio.pause(); PLAY.audio = null; }
  PLAY.t0 = t0; reviewTag();
  const ch = chapterAt(PLAY.reel, i);
  if (b.chapter || i === PLAY.from){ showChapter(ch, PLAY.reel); }
  resumeSet(PLAY.reel, i); if (i > 0 || PLAY.reel === 'play') posSet(PLAY.reel, i); drawChapters();
  // sound: last beat's effects fade, the scene's ambient loop continues, everything ducks under the new line
  sndFadeShots(1.5); sndAmbient(ambAt(i)); sndLevel('voice');
  // earlier beats' arrows and markers step back so the new ones read clearly
  gFx.selectAll(':scope > g').classed('old', true); gFxTop.selectAll(':scope > g').classed('old', true);
  // 1) the line starts: caption (and audio), year counter runs alongside
  b.steps.filter(x => x.type === 'caption' || x.type === 'year').forEach(x => { STEP[x.type](x, dur(x) || 1); if (x.type === 'year') sndShot(sfxOf(x)); });
  let audioDone = true;
  if (b.audio && VOICE){ try {
    // tok: a play() aborted by a later seek must not release this line's hold (the same file can be reused)
    audioDone = false; const a = PLAY.audio = audioFor(b.audio), tok = PLAY.tok = (PLAY.tok || 0) + 1; a.currentTime = 0; a.playbackRate = SPEED;
    const done = () => { if (PLAY && PLAY.tok === tok && PLAY.audio === a){ audioDone = true; a.onended = a.onerror = null; PLAY.audio = null; PLAY.aw = null; PLAY.hold = false; sndLevel('fill'); } };
    // a clip that fails, stalls or is stopped by the phone (call, other app) never pauses the film:
    // it is retried once, then skipped and the film goes on with the subtitles on the beat timer
    const skip = () => { if (PLAY && PLAY.tok === tok && PLAY.audio === a){ try { a.pause(); } catch(e){} PLAY.audioSkips = (PLAY.audioSkips || 0) + 1; done(); } };
    const retry = () => { if (!PLAY || PLAY.tok !== tok || PLAY.audio !== a) return; if (PLAY.aw.tries++ >= 1) return skip(); PLAY.aw.t = performance.now();
      if (a.error){ const pos = a.currentTime; a.load(); try { a.currentTime = pos; } catch(e){} } if (!PLAY.paused) a.play().catch(err => { if (!err || err.name !== 'AbortError') skip(); }); };
    PLAY.aw = {a, tok, last: -1, t: performance.now(), tries: 0, retry};
    a.onended = done; a.onerror = retry;
    if (!PLAY.paused) a.play().catch(err => { if (!err || err.name !== 'AbortError') retry(); });
  } catch(e){ audioDone = true; } }
  preload(PLAY.beats[i + 1]);
  // 2) camera moves first, 3) then one visual event at a time
  let t = t0; const f = b.steps.find(x => x.type === 'focus');
  if (f){ STEP.focus(f, dur(f)); t += dur(f) + GAP; }
  vigBeat(i, b, f ? t0 + dur(f) * 0.75 : t0 + 250);
  b.steps.filter(x => VISUAL.includes(x.type)).forEach(x => { at(t, () => { STEP[x.type](x, dur(x)); sndShot(sfxOf(x)); }); t += dur(x) + GAP; });
  // 4) wait for the line to finish (reading time, or the audio), 5) then the pause
  const lineEnd = Math.max(t0 + lineMs(b), t);
  // in the pause the effects and ambient rise so the film can breathe; sfxHold lets a battle or march play out
  at(lineEnd, () => { if (!audioDone) PLAY.hold = true; else sndLevel('fill'); });
  // the opener's last line ends on a choice: the film waits until the viewer picks one
  at(lineEnd + 1, () => { if (b.choice && PLAY.reel === 'intro'){ PLAY.wait = true; sndLevel('fill'); showChoice(i); return; }
    const pz = breathMs(b); PLAY.b0 = t0; PLAY.bEnd = PLAY.clock + pz; at(PLAY.clock + pz, () => runBeat(i + 1)); });
  PLAY.b0 = t0; PLAY.bEnd = lineEnd + breathMs(b);
  $('capn').textContent = `${i + 1} / ${PLAY.beats.length}`;
  setPP(true);   // a new beat keeps the idle timer going but does not bring hidden controls back
}
function seek(i){
  // rebuild the state of beats 0..i-1 instantly, then play beat i
  if (!PLAY) return;
  i = Math.max(0, Math.min(PLAY.beats.length - 1, i));
  gZones.selectAll('*').interrupt(); svg.interrupt(); PLAY.anims = []; PLAY.events = [];
  resetMap(); YEAR = STOP.year; PLAY.lastFocus = null; vigHide(true);
  PLAY.clockOn = false; for (let j = 0; j < i; j++) applyInstant(j); PLAY.clockOn = true;
  if (!PLAY.beats[i].steps.some(x => x.type === 'focus') && PLAY.lastFocus){ const f = PLAY.lastFocus; setHighlight(f.hl || []); flyFocus(f, 600); }
  runBeat(i);
}
async function playStart(reel = 'play', from = 0){
  if (typeof reel !== 'string') reel = 'play';
  ARRIVE = -1; sndEnsure(); // inside the Play click: the browser allows audio from here on
  // the narrated part runs as a small film: the map grows to fill the screen first
  const film = enterCine();
  if (MODE !== 'stop') await go(liveBefore(cur));
  if (!STOP || !reelBeats(reel)){ exitCine(); return; }
  closeObj();
  await film; if (!CINE) return;
  if (reel === 'play') Object.assign(ERA.zoneObjects, STOP.play.zoneObjects);
  if (PLAY){ cancelAnimationFrame(PLAY.raf); if (PLAY.audio) PLAY.audio.pause(); }
  const beats = reelBeats(reel); from = Math.max(0, Math.min(beats.length - 1, +from || 0));
  PLAY = {reel, beats, from, i: 0, paused: false, clock: 0, clockOn: true, anims: [], events: []};
  vigHide(true); vigPreload(from);
  document.body.classList.toggle('reel-intro', reel === 'intro');
  document.body.classList.add('playing'); placeCap(); $('cap').hidden = false; drawKeys();
  if (NARROW()) scrollTo({top:0, behavior:'smooth'});
  $('ev').classList.add('dim');
  resetMap(); YEAR = STOP.year; setHighlight([]);
  buildChapters();
  if (from) seek(from); else runBeat(0);
  PLAY.raf = requestAnimationFrame(tick);
}
// the opener's choice, shown over the picture when its last line has been spoken
function showChoice(i){
  // while the choice is up the subtitle, source line, progress bar and chapter strip step aside;
  // the panel sits between the year and the controls, and scrolls if a screen is very short
  document.body.classList.add('choosing'); vigHide();
  const c = $('choice'); c.hidden = false; c.classList.remove('in'); void c.offsetWidth; c.classList.add('in'); wake(); placeChoice();
  const nxt = chapterAt('intro', i + 1);
  $('choicego').textContent = 'Continue the story ›';
  // an opener that ends on its choice (c. 1150 BC): Continue goes straight on into Play
  const intoPlay = i + 1 >= PLAY.beats.length && STOP.play;
  if (i + 1 >= PLAY.beats.length) partSet();
  $('choicesub').textContent = intoPlay ? `Play: ${STOP.play.title} · ${mmss(playTotal())}` : nxt && nxt.i === i + 1 ? `Scene ${nxt.n}: ${nxt.title} · ${mmss(reelChapters('intro').filter(x => x.n >= nxt.n).reduce((s, x) => s + x.ms, 0))}` : '';
  $('choicego').onclick = e => { e.stopPropagation(); if (!PLAY) return; hideChoice(); PLAY.wait = false; if (PLAY.paused) playPause(false);
    if (intoPlay){ resumeSet('intro', 0); playStart('play'); } else runBeat(i + 1); };
  $('choicemap').onclick = e => { e.stopPropagation(); if (!PLAY) return; const r = PLAY.reel; playStop(false); resumeSet(r, i + 1);
    // back to the map before the Play: Resume picks up at the Play's first line
    if (intoPlay) posSet('play', 0); else posSet(r, i + 1); };
  setTimeout(() => { if (!c.hidden) $('choicego').focus({preventScroll: true}); }, 50);
}
function hideChoice(){ const c = $('choice'); if (c) c.hidden = true; document.body.classList.remove('choosing'); }
function placeChoice(){
  const c = $('choice'); if (!c || c.hidden) return;
  const vb = $('vp').getBoundingClientRect(), cap = $('cap'), cy = $('cyear');
  const capTop = !cap.hidden && cap.offsetHeight ? cap.getBoundingClientRect().top : vb.bottom;
  const yb = cy && cy.offsetHeight ? cy.getBoundingClientRect().bottom : vb.top;
  c.style.setProperty('--choice-top', Math.max(8, Math.round(yb - vb.top) + 8) + 'px');
  c.style.setProperty('--choice-bottom', Math.max(8, Math.round(vb.bottom - capTop) + 8) + 'px');
}
// the opening film ends by handing over to the map: zoom out onto the Explore step
function introEnd(){ resumeSet('intro', 0); if (!STOP.play) posClear(STOP.year); else posSet('play', 0); partSet(); playStop(false); }
// a chapter card at the start of each chapter, and chapter segments above the film controls
let chapT = 0;
function showChapter(c, r){
  const el = $('chapcard'); if (!c || !c.title) return;
  const n = reelChapters(r).length;
  el.innerHTML = `<span class="k">Scene ${c.n} of ${n}</span><span class="t">${esc(c.title)}</span>`;
  el.hidden = false; el.classList.remove('in'); void el.offsetWidth; el.classList.add('in');
  clearTimeout(chapT); chapT = setTimeout(() => { el.hidden = true; }, 3600);
}
function buildChapters(){
  const box = $('capch'), cs = reelChapters(PLAY.reel), tot = cs.reduce((s, c) => s + c.ms, 0);
  box.hidden = cs.length < 2;
  box.innerHTML = cs.map(c => `<button type="button" class="chs" data-b="${c.i}" style="flex:${Math.max(1, Math.round(1000 * c.ms / tot))}" aria-label="Scene ${c.n}: ${esc(c.title)}" title="Scene ${c.n}: ${esc(c.title)} · ${mmss(c.ms)}"><i></i><span>${c.n} · ${esc(c.title)}</span></button>`).join('');
  box.querySelectorAll('.chs').forEach(b => b.onclick = e => { e.stopPropagation(); if (PLAY){ hideChoice(); seek(+b.dataset.b); } });
}
function drawChapters(){
  if (!PLAY) return;
  const cs = reelChapters(PLAY.reel), i = PLAY.i;
  $('capch').querySelectorAll('.chs').forEach((el, k) => { const c = cs[k]; const f = i >= c.end ? 1 : i < c.i ? 0 : (i - c.i) / (c.end - c.i);
    el.classList.toggle('cur', i >= c.i && i < c.end); el.classList.toggle('done', i >= c.end); el.querySelector('i').style.width = Math.round(100 * f) + '%'; });
}
// phones: subtitles sit next to the map so they never cover the animation
const NARROW = () => matchMedia('(max-width:899px)').matches;
function placeCap(){ const c = $('cap'), vp = $('vp'); if (NARROW() && !CINE){ if (c.parentNode === vp) vp.after(c); c.classList.add('below'); } else { if (c.parentNode !== vp) vp.append(c); c.classList.remove('below'); } }
addEventListener('resize', () => { if (PLAY) placeCap(); placeChoice(); });
// text size (js/textsize.js): map labels follow the gentler map scale; relabel and re-place the film panels
function TSM(){ const v = parseFloat(getComputedStyle(document.documentElement).getPropertyValue('--tsm')); return v > 0 ? v : 1; }
addEventListener('tlm:textsize', () => { scaleMarks(); placeChoice(); requestAnimationFrame(placeChoice); });
function setPP(quiet){ const p = PLAY && PLAY.paused; $('cappp').textContent = p ? '▶' : '❚❚'; $('cappp').setAttribute('aria-label', p ? 'Play' : 'Pause'); $('cap').classList.toggle('paused', !!p); $('vig').classList.toggle('paused', !!p); if (!quiet || (!idleT && !document.body.classList.contains('idle'))) wake(); }
function playPause(force){
  if (!PLAY) return;
  PLAY.paused = force === undefined ? !PLAY.paused : force;
  if (PLAY.audio){ PLAY.paused ? PLAY.audio.pause() : PLAY.audio.play().catch(() => {}); }
  if (SND.ctx){ PLAY.paused ? SND.ctx.suspend().catch(() => {}) : SND.on && SND.ctx.resume().catch(() => {}); }
  if (PLAY.paused) svg.interrupt();
  setPP();
}
const SPEEDS = [0.75, 1, 1.25];
function setSpeed(v){ SPEED = v; if (PLAY && PLAY.audio) PLAY.audio.playbackRate = v; $('capspd').textContent = (v === 1 ? '1' : String(v)) + '×'; $('capspd').setAttribute('aria-label', 'Speed ' + v + 'x'); }
function playStop(toEnd){
  if (!PLAY) return;
  cancelAnimationFrame(PLAY.raf); if (PLAY.audio) PLAY.audio.pause();
  if (SND.ctx && SND.ctx.state === 'suspended' && SND.on) SND.ctx.resume().catch(() => {});
  sndStop(0.8);
  PLAY = null; document.body.classList.remove('playing', 'reel-intro'); $('cap').hidden = true; $('ev').classList.remove('dim');
  hideChoice(); vigHide(true); $('chapcard').hidden = true; clearTimeout(chapT);
  const out = exitCine();
  if (!toEnd){ resetMap(); YEAR = null; $('big').textContent = STOP.label; $('pill').textContent = STOP.label; drawKeys(); out.then(() => { if (!PLAY) showStep(steps().length - 1); }); }
  return out;
}
const playToLabel = () => { const s = STOP && STOP.play && STORY.stops.find(s => s.year === STOP.play.to); return s ? s.label : ''; };
function playEnd(){
  // the transition ends on the new year's intro and stays there (no auto-continue)
  resumeSet('play', 0); posClear(STOP.year); partSet();
  const to = STOP.play.to;
  const k = STORY.stops.findIndex(s => s.year === to);
  // zoom back out to the explore view first, then land on the new year: its intro when the stop is built,
  // otherwise the 'coming soon' end state
  playStop(true).then(() => { if (PLAY) return; if (STORY.stops[k].file){ ARRIVE = k; go(k); } else arriveSoon(k, false); });
}
// ---------- vignettes: a picture card over the map while the narrator describes something ----------
// beat.vignette = {src, alt, caption?, beats?} comes from build/vignettes.py. The card appears once the
// camera has settled, beside the place in focus (never on it, never on the subtitles or the year), drifts
// slowly (Ken Burns, frozen while paused, none with reduced motion) and fades when a later beat moves the
// camera, brings its own card, or after `beats` lines (default 3). Pictures load two beats ahead; one that
// fails to load is simply left out, the film never waits for it.
const VIG = {img: {}, cur: null, n: 0, t: 0};
const VIG_BEATS = 3;
function vigLoad(v){
  let r = VIG.img[v.src];
  if (!r){ const im = new Image(); r = VIG.img[v.src] = {im, ok: null, cb: []}; im.decoding = 'async';
    im.onload = () => { r.ok = true; r.cb.splice(0).forEach(f => f()); }; im.onerror = () => { r.ok = false; r.cb = []; }; im.src = v.src; }
  return r;
}
function vigPreload(i){ if (!PLAY) return; for (let j = i; j <= i + 2; j++){ const b = PLAY.beats[j]; if (b && b.vignette) vigLoad(b.vignette); } }
function vigHide(now){
  const el = $('vig'); VIG.cur = null; clearTimeout(VIG.t); if (!el) return;
  el.classList.remove('in');
  if (now || el.hidden || REDUCED()){ el.hidden = true; el.classList.remove('out'); return; }
  el.classList.add('out'); VIG.t = setTimeout(() => { if (!VIG.cur){ el.hidden = true; el.classList.remove('out'); } }, 650);
}
// called when beat i starts; at = clock time the camera has (nearly) settled
function vigBeat(i, b, at_){
  const c = VIG.cur;
  if (c && (b.vignette || b.steps.some(x => x.type === 'focus') || i >= c.i + (c.v.beats || VIG_BEATS) || i < c.i)) vigHide();
  vigPreload(i + 1);
  const v = b.vignette; if (!v) return;
  const r = vigLoad(v); if (r.ok === false) return;
  at(at_, () => { if (!PLAY || PLAY.i !== i) return; const show = () => { if (PLAY && PLAY.i === i && r.ok) vigShow(v, i, r.im); }; r.ok ? show() : r.cb.push(show); });
}
function vigShow(v, i, im){
  const el = $('vig'); if (!el) return;
  clearTimeout(VIG.t); VIG.cur = {v, i}; VIG.n++;
  const img = el.querySelector('img'); img.src = im.src; img.alt = v.alt || '';
  img.style.setProperty('--ar', im.naturalWidth && im.naturalHeight ? im.naturalWidth / im.naturalHeight : 4 / 3);
  el.dataset.kb = String(VIG.n % 4);
  const cp = el.querySelector('figcaption'); cp.textContent = v.caption || ''; cp.hidden = !v.caption;
  el.classList.remove('in', 'out'); el.hidden = false; vigPlace(); void el.offsetWidth; el.classList.add('in');
  el.classList.toggle('paused', !!PLAY.paused);
}
// the largest card that fits to the right, left, above or below the focus point
function vigPlace(){
  const el = $('vig'); if (!el || el.hidden || !VIG.cur) return;
  const vp = $('vp').getBoundingClientRect(), W = vp.width, H = vp.height, narrow = W < 600;
  const cy = $('cyear'), cap = $('cap'), pad = 10, gap = narrow ? 34 : 48;
  // where flyTo puts the place in focus (the camera may still be landing when the card comes in)
  const f = filmFree(), px = W / 2, py = f.cy;
  let top = Math.max(pad, cy && cy.offsetHeight ? cy.getBoundingClientRect().bottom - vp.top + 8 : Math.min(H * .06, 46) + 8);
  let bot = H - pad;
  if (CINE && CINE.full) bot = Math.min(bot, f.bot - 4);   // the subtitles and source chip; the tap controls may cover it for a moment
  else if (cap && !cap.hidden && cap.offsetHeight && cap.parentNode === $('vp')){ const r = cap.getBoundingClientRect(); bot = Math.min(bot, r.top - vp.top - 8); }
  const ar = parseFloat(el.querySelector('img').style.getPropertyValue('--ar')) || 4 / 3;
  const maxW0 = narrow ? Math.min(W * .8, 330) : Math.min(Math.max(W * .3, 240), 400);
  // caption: one line, or two when it is long (it wraps instead of being cut off)
  const capL = c => !c ? 0 : c.length * 6.4 * TSM() > maxW0 - 16 ? 2 : 1;
  const capH = () => (VIG.cur.v.caption ? 6 + 16 * TSM() * capL(VIG.cur.v.caption) : 0) + 12;   // caption lines + frame padding
  const maxW = maxW0;
  const fit = (w, h) => Math.max(0, Math.min(maxW, w - 12, (h - capH()) * ar + 12));
  const cand = [
    {s: 'r', w: fit(W - pad - (px + gap), bot - top), x0: px + gap, y: 'mid'},
    {s: 'l', w: fit(px - gap - pad, bot - top), x1: px - gap, y: 'mid'},
    {s: 'a', w: fit(W - 2 * pad, py - gap - top), y1: py - gap},
    {s: 'b', w: fit(W - 2 * pad, bot - (py + gap)), y0: py + gap}
  ].sort((a, b) => b.w - a.w);
  const c = cand[0];
  if (c.w < 130){ el.style.visibility = 'hidden'; return; }   // no room on this screen: leave it out
  el.style.visibility = '';
  const w = Math.round(c.w), h = Math.round((w - 12) / ar + capH());
  const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
  let x, y;
  if (c.s === 'r' || c.s === 'l'){ x = c.s === 'r' ? c.x0 : c.x1 - w; y = clamp(py - h * .6, top, bot - h); }
  else { x = clamp(px - w / 2, pad, W - pad - w); y = c.s === 'a' ? c.y1 - h : c.y0; y = clamp(y, top, bot - h); }
  el.style.width = w + 'px'; el.style.left = Math.round(x) + 'px'; el.style.top = Math.round(y) + 'px'; el.dataset.side = c.s;
  // the real height (the caption may wrap differently from the estimate): keep the card inside the free picture
  const hr = el.offsetHeight;
  if (hr && hr !== h){ const y2 = clamp(c.s === 'a' ? Math.min(y, c.y1 - hr) : y, top, Math.max(top, bot - hr)); if (y2 !== y) el.style.top = Math.round(y2) + 'px'; }
}
addEventListener('resize', () => requestAnimationFrame(vigPlace));
addEventListener('tlm:textsize', () => requestAnimationFrame(vigPlace));
// ---------- cinematic mode: the narrated part as a small film ----------
// The map viewport grows from its place in the page to the full screen (Fullscreen API where it exists,
// otherwise a fixed full-viewport layer, e.g. iPhone Safari), the page chrome fades, subtitles (CC) sit
// at the bottom. When the part ends it shrinks back into the page.
const REDUCED = () => matchMedia('(prefers-reduced-motion: reduce)').matches;
const CINE_MS = 650, IDLE_MS = 3000;
let CINE = null, CC = true, idleT = 0;
try { CC = localStorage.getItem('tlm.cc') !== 'off'; } catch(e){}
function setCC(on){
  CC = !!on; try { localStorage.setItem('tlm.cc', CC ? 'on' : 'off'); } catch(e){}
  document.body.classList.toggle('cc-off', !CC); requestAnimationFrame(vigPlace);
  const b = $('capcc'); b.setAttribute('aria-pressed', String(CC)); b.setAttribute('aria-label', CC ? 'Subtitles on' : 'Subtitles off'); b.classList.toggle('on', CC);
}
setCC(CC);

// ---------- sound effects: a quiet bed under the narration that rises in the pauses ----------
// Clips live in assets/sfx (prompts and credits in assets/sfx/README.md). Web Audio starts only after a
// user gesture (BEGIN ADVENTURE, Play or the sound button); nothing is fetched before. While a line is
// being narrated the effects sit about 18 dB down; in the pause after it they rise to about -6 dB, then
// duck smoothly when the next line starts. Steps may set "sfx" (a clip name, or null for none) and
// "sfxHold" (ms the pause is stretched so the sound can play out; on the same virtual clock, so it
// follows the speed setting, and Skip cuts it).
const SFX_FILES = {battle:'battle', migration:'migration', border:'border', year:'year', desert:'amb-desert', river:'amb-river'};
const SFX_DEFAULT = {battle:'battle', migration:'migration', border:'border', year:'year'};
const DB = d => Math.pow(10, d / 20);
const SFX_LEVEL = {voice: DB(-18), fill: DB(-6), off: 0};
const AMB_GAIN = DB(-5);
let GESTURE = false;
['pointerdown', 'keydown', 'touchend', 'click'].forEach(t => addEventListener(t, e => { if (e.isTrusted) GESTURE = true; }, {capture: true, passive: true}));
const SND = {on: !REDUCED(), ctx: null, bus: null, buf: {}, loading: null, amb: null, ambName: null, shots: [], phase: 'off', target: 0};
try { const v = localStorage.getItem('tlm.snd'); if (v) SND.on = v === 'on'; } catch(e){}
const sfxOf = x => x.sfx === undefined ? SFX_DEFAULT[x.type] : x.sfx;
function sndEnsure(){
  if (!SND.on || !GESTURE) return null;
  if (!SND.ctx){
    const AC = window.AudioContext || window.webkitAudioContext; if (!AC) return null;
    try { SND.ctx = new AC(); } catch(e){ return null; }
    SND.bus = SND.ctx.createGain(); SND.bus.gain.value = 0; SND.bus.connect(SND.ctx.destination);
  }
  if (SND.ctx.state === 'suspended' && !(PLAY && PLAY.paused)) SND.ctx.resume().catch(() => {});
  if (!SND.loading) SND.loading = Promise.all(Object.entries(SFX_FILES).map(([k, f]) => fetch('assets/sfx/' + f + '.mp3')
    .then(r => r.arrayBuffer()).then(a => new Promise((ok, no) => SND.ctx.decodeAudioData(a, ok, no))).then(b => { SND.buf[k] = b; }).catch(() => {})));
  return SND.ctx;
}
function ramp(param, to, sec){ const t = SND.ctx.currentTime; param.cancelScheduledValues(t); param.setValueAtTime(param.value, t); param.linearRampToValueAtTime(to, t + sec); }
function sndLevel(phase){
  SND.phase = phase; SND.target = SND.on ? SFX_LEVEL[phase] : 0;
  if (SND.ctx) ramp(SND.bus.gain, SND.target, phase === 'fill' ? 1.4 : phase === 'voice' ? 0.6 : 0.5);
}
function sndShot(name){
  if (!name || !SND.on || !PLAY || !PLAY.clockOn || !sndEnsure()) return;
  if (PLAY.sndUsed){ if (PLAY.sndUsed.has(name)) return; PLAY.sndUsed.add(name); }
  const go = () => {
    const b = SND.buf[name]; if (!b || !PLAY || !SND.on) return;
    const c = SND.ctx, s = c.createBufferSource(), g = c.createGain(), t = c.currentTime;
    s.buffer = b; g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(1, t + 0.3);
    s.connect(g); g.connect(SND.bus); s.start(t);
    const o = {name, s, g}; SND.shots.push(o); s.onended = () => { SND.shots = SND.shots.filter(x => x !== o); };
  };
  SND.buf[name] ? go() : SND.loading.then(go);
}
function sndFadeShots(sec){
  if (SND.ctx) SND.shots.forEach(o => { try { ramp(o.g.gain, 0, sec); o.s.stop(SND.ctx.currentTime + sec + 0.05); } catch(e){} });
  SND.shots = [];
}
function sndAmbient(name){
  if (!SND.on) name = null;
  if (name === SND.ambName && (SND.amb || !name)) return;
  const old = SND.amb; SND.amb = null; SND.ambName = name;
  if (old && SND.ctx){ try { ramp(old.g.gain, 0, 2); old.s.stop(SND.ctx.currentTime + 2.1); } catch(e){} }
  if (!name || !sndEnsure()) return;
  const go = () => {
    const b = SND.buf[name]; if (!b || SND.ambName !== name || SND.amb || !PLAY) return;
    const c = SND.ctx, s = c.createBufferSource(), g = c.createGain(), t = c.currentTime;
    s.buffer = b; s.loop = true; g.gain.setValueAtTime(0, t); g.gain.linearRampToValueAtTime(AMB_GAIN, t + 2.5);
    s.connect(g); g.connect(SND.bus); s.start(t); SND.amb = {name, s, g};
  };
  SND.buf[name] ? go() : SND.loading.then(go);
}
function sndStop(sec){ sndFadeShots(sec); sndAmbient(null); sndLevel('off'); }
// the scene's ambient loop: the nearest earlier beat that names one, else the transition's default
const ambAt = i => { for (let j = i; j >= 0; j--) if (PLAY.beats[j].ambient) return PLAY.beats[j].ambient; return reelAmbient(PLAY.reel); };
// extra pause for steps whose sound should play out (only when sound is on)
const holdMs = b => SND.on ? Math.max(0, ...b.steps.filter(x => sfxOf(x)).map(x => +x.sfxHold || 0)) : 0;
function setSnd(on){
  SND.on = !!on; try { localStorage.setItem('tlm.snd', SND.on ? 'on' : 'off'); } catch(e){}
  const b = $('capsnd'); b.setAttribute('aria-pressed', String(SND.on)); b.setAttribute('aria-label', SND.on ? 'Sound on' : 'Sound off'); b.title = SND.on ? 'Sound on' : 'Sound off'; b.classList.toggle('on', SND.on);
  if (!SND.on){ sndStop(0.4); SND.phase = PLAY ? SND.phase : 'off'; return; }
  if (PLAY){ sndEnsure(); sndLevel(SND.phase === 'off' ? 'voice' : SND.phase); sndAmbient(ambAt(PLAY.i)); }
}
// keep the same picture on screen when the map viewport changes size
function refitKeep(){
  const vb = (svg.attr('viewBox') || '').split(/[ ,]+/).map(Number);
  const r = svg.node().getBoundingClientRect();
  if (vb.length < 4 || !vb[2] || !r.width){ fit(); redrawZones(); return; }
  const s = Math.min(r.width / vb[2], r.height / vb[3]), ox = (r.width - vb[2] * s) / 2, oy = (r.height - vb[3] * s) / 2;
  const g1 = [30, 30], g2 = [40, 36], a = projection(g1), b = projection(g2);
  fit();
  const a2 = projection(g1), b2 = projection(g2), q = (b2[0] - a2[0]) / (b[0] - a[0]);
  const cx = a2[0] - q * a[0], cy = a2[1] - q * a[1], k1 = s * TR.k / q;
  svg.interrupt(); svg.call(zoom.transform, d3.zoomIdentity.translate(ox + s * TR.x - k1 * cx, oy + s * TR.y - k1 * cy).scale(k1));
  redrawZones(); cullLabels();
}
const wait = ms => new Promise(r => setTimeout(r, ms));
function morph(vp, from, to){
  // animate the fixed viewport between two screen rectangles
  const ms = REDUCED() ? 0 : CINE_MS;
  const set = q => { vp.style.left = q.left + 'px'; vp.style.top = q.top + 'px'; vp.style.width = q.width + 'px'; vp.style.height = q.height + 'px'; };
  vp.classList.remove('cinefx'); set(from); void vp.offsetWidth;
  if (ms) vp.classList.add('cinefx'); set(to);
  return wait(ms + 30).then(() => vp.classList.remove('cinefx'));
}
function enterCine(){
  if (CINE) return CINE.ready;
  const vp = $('vp'), r = vp.getBoundingClientRect(), b = document.body;
  CINE = {full: false, fsOn: false};
  // Fullscreen API needs the user's click, so ask right away; iPhone Safari has none and keeps the fixed layer
  const el = document.documentElement, rq = el.requestFullscreen || el.webkitRequestFullscreen;
  if (rq && !document.fullscreenElement){ try { const p = rq.call(el); if (p && p.then) p.then(() => { if (CINE) CINE.fsOn = true; }).catch(() => {}); else CINE.fsOn = true; } catch(e){} }
  const ph = document.createElement('div'); ph.id = 'vpph'; ph.className = 'vpph'; ph.style.height = r.height + 'px'; vp.before(ph);
  vp.classList.add('cinefixed'); $('cyear').textContent = $('pill').textContent;
  b.classList.add('cine'); ctlHide(); ctlHint();
  placeCap();
  const c = CINE;
  c.ready = morph(vp, r, {left: 0, top: 0, width: innerWidth, height: innerHeight}).then(() => {
    if (CINE !== c) return;
    vp.style.cssText = ''; vp.classList.add('full'); c.full = true; refitKeep();
  });
  return c.ready;
}
function exitCine(){
  if (!CINE) return Promise.resolve();
  if (CINE.out) return CINE.out;
  const c = CINE, vp = $('vp'), b = document.body, ph = $('vpph');
  c.fsOn = false;
  if (document.fullscreenElement && document.exitFullscreen) document.exitFullscreen().catch(() => {});
  clearTimeout(idleT); idleT = null; b.classList.remove('idle');
  c.out = (c.ready || Promise.resolve()).then(() => {
    const from = vp.getBoundingClientRect();
    vp.classList.remove('full'); b.classList.remove('cine'); placeCap();
    const to = ph ? ph.getBoundingClientRect() : from;
    return morph(vp, from, {left: to.left, top: to.top, width: to.width, height: to.height});
  }).then(() => {
    vp.classList.remove('cinefixed'); vp.style.cssText = ''; if (ph) ph.remove();
    CINE = null; refitKeep(); placeCap();
  });
  return c.out;
}
// controls fade after a few quiet seconds and come back on any touch or mouse move
function wake(){
  const b = document.body; b.classList.remove('idle'); clearTimeout(idleT); idleT = null;
  if (CINE && PLAY && !PLAY.paused) idleT = setTimeout(() => { idleT = null; if (CINE && PLAY && !PLAY.paused && !CINE.out) b.classList.add('idle'); }, IDLE_MS);
}
// hide the controls now (a tap on the picture while they show, and the start of a film)
function ctlHide(){ clearTimeout(idleT); idleT = null; if (CINE) document.body.classList.add('idle'); }
// the first two films on this device say once how to get the controls
function ctlHint(){
  const el = $('ctlhint'); if (!el) return; let n = 0;
  try { n = +localStorage.getItem('tlm.ctlhint') || 0; if (n < 2) localStorage.setItem('tlm.ctlhint', String(n + 1)); } catch(e){}
  if (n >= 2){ el.hidden = true; return; }
  el.textContent = matchMedia('(hover: none)').matches ? 'Tap the screen for controls' : 'Move the mouse or click for controls';
  el.hidden = false; clearTimeout(ctlHint.t); ctlHint.t = setTimeout(() => { el.hidden = true; }, 3600);
}
// a touch or click on the picture itself is decided in the click handler below (show or hide); anything else wakes
const onPic = e => e.target && e.target.closest && e.target.closest('#vp') && !e.target.closest('.cap2, .choice, button, a');
// (a mouse that just moved onto the picture brought the controls up; a click right after keeps them up)
let movedUp = -1e9;
['pointermove', 'pointerdown', 'touchstart', 'keydown'].forEach(t => addEventListener(t, e => {
  if (!CINE || ((t === 'pointerdown' || t === 'touchstart') && onPic(e))) return;
  if (t === 'pointermove' && document.body.classList.contains('idle')) movedUp = performance.now();
  wake(); }, {passive: true}));
// in the film a tap (or click) on the picture shows the controls, and a tap while they show hides them again,
// like a video player; it never pauses or plays, which is too easy to do by accident. Play and pause: the
// button in the control bar, or Space. Taps on the controls keep them up. Objects are not opened mid-film.
$('vp').addEventListener('click', e => {
  if (!CINE || e.target.closest('.cap2, .choice, button, a')) return;
  e.stopPropagation(); e.preventDefault();
  if (document.body.classList.contains('idle') || performance.now() - movedUp < 800) wake(); else ctlHide();
}, true);
addEventListener('keydown', e => {
  if (!CINE || !PLAY) return;
  if (e.key === 'Escape'){ e.preventDefault(); playStop(false); }
  else if (e.key === ' ' && !(e.target.closest && e.target.closest('button'))){ e.preventDefault(); playPause(); }
  else if (e.key === 'ArrowRight') $('capnext').click();
  else if (e.key === 'ArrowLeft') $('capprev').click();
});
// leaving browser fullscreen (e.g. the Esc key) also ends the film
document.addEventListener('fullscreenchange', () => {
  if (document.fullscreenElement){ if (CINE) CINE.fsOn = true; return; }
  if (CINE && CINE.fsOn && !CINE.out && PLAY){ CINE.fsOn = false; playStop(false); }
});
$('cappp').onclick = e => { e.stopPropagation(); playPause(); };
$('capnext').onclick = e => { e.stopPropagation(); if (PLAY) seek(PLAY.i + 1 < PLAY.beats.length ? PLAY.i + 1 : PLAY.i) ; };
$('capprev').onclick = e => { e.stopPropagation(); if (PLAY) seek(PLAY.i - 1); };
$('capspd').onclick = e => { e.stopPropagation(); setSpeed(SPEEDS[(SPEEDS.indexOf(SPEED) + 1) % SPEEDS.length] || 1); };
$('capx').onclick = e => { e.stopPropagation(); playStop(false); };
$('capcc').onclick = e => { e.stopPropagation(); setCC(!CC); };
$('capsnd').onclick = e => { e.stopPropagation(); setSnd(!SND.on); };
setSnd(SND.on);
// voice off: the line in progress stops and the subtitles keep their reading time; on: from the next line
function setVoice(on){
  VOICE = !!on; try { localStorage.setItem('tlm.voice', VOICE ? 'on' : 'off'); } catch(e){}
  const b = $('capvoice'); b.setAttribute('aria-pressed', String(VOICE)); b.setAttribute('aria-label', VOICE ? 'Narrator on' : 'Narrator off'); b.title = VOICE ? 'Narrator on' : 'Narrator off'; b.classList.toggle('on', VOICE);
  if (!VOICE && PLAY && PLAY.audio){ const a = PLAY.audio; a.pause(); if (a.onended) a.onended(); }
}
$('capvoice').onclick = e => { e.stopPropagation(); setVoice(!VOICE); };
setVoice(VOICE);
$('capskip').onclick = e => { e.stopPropagation(); if (PLAY && PLAY.reel === 'intro'){ resumeSet('intro', 0); posClear(STOP.year); playStop(false); return; } if (PLAY){ svg.interrupt(); PLAY.anims = []; PLAY.events = []; resetMap(); YEAR = STOP.year; PLAY.clockOn = false; PLAY.beats.forEach((b, j) => applyInstant(j)); playEnd(); } };
// a tap on the map never pauses Play (too easy by accident); tapping an object opens its box, which pauses

// a stop that is not built yet, reached at the end of Play: the map keeps the end state
const liveBefore = k => { for (let j = k; j >= 0; j--) if (STORY.stops[j].file) return j; return 0; };
function arriveSoon(k, rebuild){
  const s = STORY.stops[k];
  cur = k; MODE = 'soon';
  if (rebuild){ resetMap(); Object.assign(ERA.zoneObjects, STOP.play.zoneObjects); PLAY = {beats: STOP.play.beats, clockOn: false, anims: [], events: []}; STOP.play.beats.forEach((b, j) => applyInstant(j)); PLAY = null; }
  setHighlight(s.soon.hl || []);
  // the end state keeps the new borders; arrows and battle markers belong to the transition only
  gFx.selectAll('*').interrupt().transition().duration(rebuild ? 0 : 700).style('opacity', 0).remove();
  gFxTop.selectAll('*').transition().duration(rebuild ? 0 : 700).style('opacity', 0).remove();
  const f = s.soon.focus || {c: [35.0, 31.95], k: 4.6};
  flyTo(f.c, f.k, rebuild ? 0 : 1400);
  timelineState(s);
  $('chapter').textContent = s.title; $('ev').hidden = false; $('soon').hidden = true;
  const recap = STOP.play.beats.map(b => b.steps.find(x => x.type === 'caption')).filter(c => c && c.cert !== 'scene' && c.cert !== 'frame');
  const all = [...new Set(recap.flatMap(c => c.src))];
  $('evbody').innerHTML = `<div class="kicker">${esc(STORY.title)} · ${esc(s.label)}</div><h2>${esc(s.soon.title)}</h2>` +
    `<div class="soonflag">Next chapter coming soon</div><p class="lead">${esc(s.soon.text)}</p>` +
    `<div class="cta"><button type="button" class="play" id="replay">↺ Replay transition</button><button type="button" id="back1207">‹ Back to ${esc(STOP.label)}</button></div>` +
    `<div class="sub">What changed, step by step</div><ul class="claims">` + recap.map(c => `<li>${badge(c.cert)} ${esc(c.display || c.text)}</li>`).join('') + '</ul>' +
    `<details class="src"><summary>Sources (${all.length})</summary>${srcList(all)}</details>`;
  $('evbody').scrollTop = 0;
  $('evn').textContent = '1 / 1'; $('evprev').disabled = true; $('evnext').disabled = true;
  $('replay').onclick = e => { e.stopPropagation(); MODE = 'stop'; cur = liveBefore(k); timelineState(STORY.stops[cur]); playStart('play'); };
  $('back1207').onclick = e => { e.stopPropagation(); go(liveBefore(k)); };
  drawKeys();
}

// ---------- timeline of stops ----------
const fmt = y => y < 0 ? (-y) + ' BC' : 'AD ' + y;
function buildTrack(){
  const tr = d3.select('#track');
  const pos = y => (100 * (y - STORY.from) / (STORY.to - STORY.from)) + '%';
  [-1000,-500,1,500,1000,1500,2000].forEach(y => tr.append('div').attr('class', y === 2000 ? 'tick tend' : 'tick').style('left', pos(y)).text(y === 1 ? 'AD 1' : fmt(y)));
  tr.selectAll('button.mk').data(STORY.stops).join('button')
    .attr('class', d => 'mk' + (d.file ? ' live' : d.soon ? ' half' : '')).attr('type','button')
    .attr('aria-label', d => d.label + (d.file ? '' : ', coming soon'))
    .style('left', d => pos(d.year)).on('click', (e, d) => go(STORY.stops.indexOf(d)));
}
function timelineState(s){
  $('big').textContent = s.label; $('big').classList.toggle('soon', !s.file);
  $('ttitle').textContent = s.title + (s.file ? '' : ' · coming soon');
  $('prev').disabled = cur === 0; $('next').disabled = cur === STORY.stops.length - 1;
  d3.selectAll('#track .mk').classed('cur', (d, j) => j === cur);
  $('pill').textContent = s.label; YEAR = null;
}
async function go(i){
  if (PLAY) playStop(true);
  cur = Math.max(0, Math.min(STORY.stops.length - 1, i));
  if (cur !== ARRIVE) ARRIVE = -1;
  const s = STORY.stops[cur];
  timelineState(s);
  $('soon').hidden = true; $('soont').textContent = s.label + ' · ' + s.title;
  closeObj();
  const L = liveBefore(cur), ls = STORY.stops[L];
  if (s.file || (s.soon && ls.file)){
    [STOP, ERA] = await Promise.all([getJSON(ls.file), getJSON(ls.era)]);
    if (!ERA._wound){ rewindAll(ERA.zones); ERA._wound = true; }
    clearFx(); drawZones(ERA); drawObjects(); loadExplored();
    if (s.file){ MODE = 'stop'; $('chapter').textContent = STOP.title; $('ev').hidden = false; drawKeys(); showStep(0); }
    else if (STOP.play && STOP.play.to === s.year) arriveSoon(cur, true);
    else { MODE = 'none'; drawKeys(); }
  } else {
    MODE = 'none'; STOP = null; ERA = null; $('chapter').textContent = 'Planned stop'; $('soon').hidden = false;
    clearFx(); drawZones(null); gPts.selectAll('*').remove(); gLines.selectAll('*').remove(); KEYSET = new Set(); drawKeys(); $('ev').hidden = true;
  }
}
$('prev').onclick = () => go(cur - 1);
$('next').onclick = () => go(cur + 1);

window.__zoomTest = () => flyTo([35.3, 32.0], 7, 600);
window.__app = { openObj, closeObj, showStep, go, playStart, playPause, playStop, seek: i => PLAY && seek(i),
  get step(){ return step; }, get K(){ return K; }, get open(){ return openId; }, get mode(){ return MODE; }, get cur(){ return cur; },
  get explored(){ return [...EXPLORED]; }, get keys(){ return [...KEYSET]; },
  get play(){ return PLAY ? {i: PLAY.i, n: PLAY.beats.length, paused: PLAY.paused, reel: PLAY.reel, hold: !!(PLAY.hold || PLAY.wait), chapter: chapterAt(PLAY.reel, PLAY.i).n, choice: !$('choice').hidden} : null; },
  get voice(){ return {on: VOICE, playing: !!(PLAY && PLAY.audio && !PLAY.audio.paused), src: PLAY && PLAY.audio ? PLAY.audio.src : null}; }, setVoice,
  parts: () => parts().map((x, n) => ({n: n + 1, k: x.k, year: x.s.year, done: partDone(x.s.year)})), partStart,
  chapters: r => reelChapters(r || 'play').map(c => ({n: c.n, title: c.title, i: c.i, end: c.end, ms: c.ms})), resume: r => resumeGet(r || 'play'), pos: y => posGet(y === undefined ? STOP && STOP.year : y),
  set speed(v){ setSpeed(v); }, projection,
  get cine(){ return CINE ? {full: !!CINE.full, fs: !!document.fullscreenElement, idle: document.body.classList.contains('idle')} : null; }, filmFree, wake, ctlHide,
  get cc(){ return CC; }, setCC, enterCine, exitCine, IDLE_MS,
  get snd(){ return {on: SND.on, ctx: SND.ctx ? SND.ctx.state : null, phase: SND.phase, target: SND.target, gain: SND.bus ? SND.bus.gain.value : null,
    amb: SND.amb ? SND.amb.name : null, shots: SND.shots.map(o => o.name), loaded: Object.keys(SND.buf).sort()}; }, setSnd,
  plan: i => PLAY ? beatPlan(PLAY.beats[i]) : null, gap: i => PLAY ? breathMs(PLAY.beats[i]) : null, get audioEl(){ return PLAY ? PLAY.audio : null; }, get audioSkips(){ return PLAY ? PLAY.audioSkips || 0 : 0; }, STALL_MS, get clock(){ return PLAY ? PLAY.clock : null; } };

// donations: hidden until data/site.json has a donateUrl (https only)
// "Report an error" works the same way with reportUrl
getJSON('data/site.json').then(c => { [['donateUrl', 'donate'], ['reportUrl', 'report']].forEach(([k, id]) => { const u = c && c[k]; if (typeof u === 'string' && /^https:\/\//.test(u)){ const a = $(id); a.href = u; a.hidden = false; } }); }).catch(() => {});
(async function init(){
  const [base, story, srcs, lib] = await Promise.all([getJSON('data/base.topo.json'), getJSON(STORY_URL), getJSON('data/sources.json'), getJSON('data/objects/near-east.json')]);
  STORY = story; SRC = srcs; OBJS = lib.objects; OBJS.forEach(o => OBJ[o.id] = o);
  document.title = `${STORY.site} · ${STORY.title}`; $('stitle').textContent = STORY.title;
  // each book in the series brings its own accent colours (story.json "theme"), on the shared leather-and-paper look
  Object.entries(STORY.theme || {}).forEach(([k, v]) => { if (/^[a-z-]+$/.test(k) && /^#[0-9a-f]{3,8}$/i.test(v)) document.documentElement.style.setProperty('--' + k, v); });
  if (STORY.book) $('sbook').textContent = STORY.book;
  const o = base.objects;
  gLand.append('path').datum(rewindAll(d3.feature(base, o.land))).attr('class','land');
  const lakes = rewindAll(d3.feature(base, o.lakes)).features;
  gLand.selectAll('path.lake').data(lakes).join('path').attr('class','lake');
  lakes.forEach(f => (LAKES[f.properties.name] = LAKES[f.properties.name] || []).push(f));
  const rivers = d3.feature(base, o.rivers).features;
  gLand.selectAll('path.river').data(rivers).join('path').attr('class', d => 'river' + (d.properties.src === 'approx' ? ' approx' : ''));
  rivers.forEach(f => (RIVERS[f.properties.name] = RIVERS[f.properties.name] || []).push(f));
  placeObjects();
  fit();
  buildTrack();
  await go(STORY.stops.findIndex(s => s.file));
})();
addEventListener('resize', () => { if (CINE){ if (CINE.full) refitKeep(); } else { fit(); redrawZones(); } });
