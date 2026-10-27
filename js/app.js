/* The Long Map: stories on a vector map.
   A story (data/stories/<id>/story.json) has stops. Each stop has events = big fact boxes, the narrative.
   Map objects come from a shared library (data/objects/*.json) = small fact boxes, reused by every story.
   Sources come from a shared registry (data/sources.json). */
const $ = id => document.getElementById(id);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const STORY_URL = 'data/stories/jews/story.json';
let STORY = null, STOP = null, ERA = null, SRC = {}, OBJ = {}, OBJS = [];
let cur = 0, step = 0, K = 1, openId = null, MODE = 'stop', SPEED = 1;
const cache = {};
const CERT = {attested:'Attested', disputed:'Disputed', tradition:'Tradition', scene:'Imagine'};
const badge = c => `<span class="cb cb-${c}">${CERT[c]}</span>`;
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
  gZones.selectAll('text.zlabel').style('font-size', (10/K) + 'px').style('stroke-width', (2/K) + 'px').style('display', K > 9 ? 'none' : null);
  gZones.selectAll('.israel').attr('filter', K < 3 ? null : 'url(#soft)');
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
  gZones.selectAll('text.zlabel').each(function(){
    if (this.style.display === 'none' || +(getComputedStyle(this).opacity) < .5) return;
    const r = this.getBoundingClientRect(); if (r.width) boxes.push(r);
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
    const lab = el.querySelector('.lab'); if (!lab) continue;
    const r = lab.getBoundingClientRect(); if (!r.width) continue;
    const clash = hit(r);
    el.classList.toggle('nolab', clash);
    if (!clash) boxes.push(r);
  }
}
const zoom = d3.zoom().scaleExtent([1, 40]).on('zoom', e => { K = e.transform.k; root.attr('transform', e.transform); scaleMarks(); });
svg.call(zoom).on('dblclick.zoom', null);
svg.append('defs').html('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.6"/></filter>');

async function getJSON(u){ if (!cache[u]) cache[u] = fetch(u).then(r => { if (!r.ok) throw new Error(u+' '+r.status); return r.json(); }); return cache[u]; }

function flyTo(c, k, ms = 900){
  const [w,h] = size(); const p = projection(c);
  svg.transition().duration(ms).call(zoom.transform, d3.zoomIdentity.translate(w/2, h/2).scale(k).translate(-p[0], -p[1]));
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
function drawObjects(){
  gLines.selectAll('*').remove(); gPts.selectAll('*').remove();
  // rivers and lakes: wide invisible hit path over the real line
  const lineObjs = OBJS.filter(o => o.geo);
  lineObjs.forEach(o => {
    const feats = Array.isArray(o.geo) ? o.geo : [o.geo];
    const g = gLines.append('g').attr('class', 'lobj t-' + o.type).datum(o);
    if (o.type === 'route') g.selectAll('path.route').data(feats).join('path').attr('class','route');
    g.selectAll('path.glow').data(feats).join('path').attr('class','glow');
    g.selectAll('path.lhit').data(feats).join('path').attr('class','lhit tap').on('click', (e) => { e.stopPropagation(); openObj(o.id); });
  });
  // area labels (regions, seas, peoples, rivers) underneath, so city and site dots always win the tap
  const top = t => (t === 'city' || t === 'site') ? 1 : 0;
  const pts = OBJS.filter(o => o.pt).map(o => ({o, pt:o.pt})).sort((a,b) => top(a.o.type) - top(b.o.type));
  const g = gPts.selectAll('g.obj').data(pts, d => d.o.id).join('g').attr('class', d => `obj t-${d.o.type} r-${d.o.rank}`);
  const inner = g.append('g').attr('class','inner');
  inner.append('circle').attr('class','hit tap').attr('r', d => top(d.o.type) ? 15 : 12).on('click', (e, d) => { e.stopPropagation(); openObj(d.o.id); });
  inner.filter(d => d.o.type === 'city').append('circle').attr('class','dot').attr('r', d => d.o.rank === 1 ? 3 : 2.4);
  inner.filter(d => d.o.type === 'site').append('rect').attr('class','dot').attr('x',-2.2).attr('y',-2.2).attr('width',4.4).attr('height',4.4).attr('transform','rotate(45)');
  const pointy = t => t === 'city' || t === 'site';
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
    .attr('class', d => 'zlabel tap' + (d.id === 'israel' ? ' zl-people' : '')).text(d => zoneObj(d.id).name.replace(/ \(.*\)/,''))
    .attr('x', d => projection(d.c)[0]).attr('y', d => projection(d.c)[1])
    .on('click', (e, d) => open(e, d.id));
  // generous tap target for the small "people" area
  g.selectAll('circle.zhit').data(people.map(f => ({id:f.properties.zone, c:centroidLonLat(f)}))).join('circle').attr('class','zhit tap')
    .attr('r', 1).on('click', (e, d) => open(e, d.id));
  redrawZones();
}
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
    h = `<div class="kicker">${esc(STORY.title)} · ${esc(STOP.label)}</div><h2>${esc(STOP.title)}</h2>` +
        `<p class="lead">${esc(STORY.intro)}</p><p>${esc(STOP.transitionIn)}</p>` +
        `<div class="cta"><button type="button" class="play" id="gostory">Start the story ›</button><button type="button" id="goexplore">Explore the map</button></div>` +
        `<div class="sub">Key places and peoples</div>${chips(STOP.keyObjects)}` +
        `<div class="legend2">${badge('attested')} found in ancient evidence · ${badge('disputed')} scholars disagree · ${badge('tradition')} Jewish tradition and the Hebrew Bible</div>`;
  } else if (e.explore){
    const pl = STOP.play;
    h = `<div class="kicker">${esc(STOP.label)} · Explore</div><h2>Explore ${esc(STOP.label)}</h2>` +
        `<p>${esc(STOP.explore.text)}</p>` +
        `<div class="sub xpcount"></div><ul class="checklist"></ul>` +
        `<button type="button" class="linkish" id="xpreset">Reset progress</button>` +
        (pl ? `<div class="next"><div class="sub">Next</div><p>${esc(STOP.transitionOut.text)}</p>` +
              `<button type="button" class="play big" id="playbtn">▶ Play: ${esc(pl.title)}</button><p class="cap">About ${Math.max(1, Math.round(playTotal() / 60000))} minutes. ${esc(pl.intro)}</p></div>` : '');
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
  if (e.intro){ $('gostory').onclick = () => showStep(1); $('goexplore').onclick = () => showStep(S.length - 1); }
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

// ---------- Play: timed transition to the next stop ----------
// A beat runs its steps together (caption, focus, migration, border, battle, year); beats run in order.
let PLAY = null, FXZ = [], YEAR = null;
const shortSrc = k => { const s = SRC[k]; if (!s) return k; const m = s.t.match(/^([^,(.]+?)(?:,| et al\.| &)[^(]*\((\d{4})\)/); if (m) return m[1].trim() + (/ et al\./.test(s.t.slice(0, 40)) ? ' et al.' : '') + ' ' + m[2]; if (s.kind === 'tradition') return 'Hebrew Bible'; return s.t.split(/[.(]/)[0].trim().slice(0, 40); };
const yfmt = (y, c) => (c ? 'c. ' : '') + fmt(Math.round(y));
function setYear(y, approx){ YEAR = y; const t = yfmt(y, approx); $('big').textContent = t; $('pill').textContent = t; }
// ---------- Play: one virtual clock, so pause, speed and step all stay in sync ----------
// Timing rules (see build/README.md): the caption line drives the beat. Camera first, then the
// visual events one at a time, then the line must have finished (reading time or audio), then pauseAfter.
const ease = t => t < .5 ? 4*t*t*t : 1 - Math.pow(-2*t + 2, 3) / 2;
const ANIM = {year:2000, focus:1600, migration:3200, battle:3000, border:3000};
const GAP = 400;
const dur = x => x.duration || ANIM[x.type] || 0;
function anim(ms, fn){ if (!ms || !PLAY || !PLAY.clockOn){ fn(1); return; } const a = {t0:PLAY.clock, ms, fn}; PLAY.anims.push(a); fn(0); }
function at(t, fn){ PLAY.events.push({t, fn}); }
function tick(now){
  if (!PLAY) return;
  const dt = Math.min(100, now - (PLAY.last || now)); PLAY.last = now;
  if (!PLAY.paused && !PLAY.hold) PLAY.clock += dt * SPEED;
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
function tweenYear(to, ms){
  const from = YEAR == null ? STOP.year : YEAR;
  anim(ms, f => setYear(from + (to - from) * f, true));
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
const CERTTXT = c => c === 'disputed' ? ' · Disputed' : '';
const STEP = {
  year: (x, ms) => tweenYear(x.to, ms),
  focus: (x, ms) => { setHighlight(x.hl || []); PLAY.lastFocus = x; if (ms) flyTo(x.c, x.k, ms / SPEED); },
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
      const feat = rewind({type:'Feature', properties:{zone:a.zone, certainty:a.certainty, part:'Drawn for c. 1150 BC: extent uncertain'}, geometry:{type:'Polygon', coordinates:[a.coords]}});
      FXZ.push(feat);
      const g = gZones.select('g');
      const el = a.certainty === 'people' ? g.append('path').attr('class','israel tap added') : g.append('path').attr('class', `zone tap unsure added z-${a.zone}`);
      el.datum(feat).attr('d', path).on('click', e => { e.stopPropagation(); openObj(ERA.zoneObjects[a.zone]); });
      const t = g.append('text').datum({id:a.zone, c:a.labelAt}).attr('class', 'zlabel tap added' + (a.certainty === 'people' ? ' zl-people' : '')).text(a.label)
        .on('click', e => { e.stopPropagation(); openObj(ERA.zoneObjects[a.zone]); });
      if (ms){ el.style('opacity', 0); t.style('opacity', 0); fade(el, 1, ms); fade(t, 1, ms); }
      redrawZones(); scaleMarks();
    });
  },
  caption: (x, ms) => {
    if (!ms) return;
    $('captext').innerHTML = `${badge(x.cert)} ${esc(x.text)}`;
    $('capsrc').textContent = x.cert === 'scene' ? 'Scene-setting only: no new facts.' : 'Sources: ' + x.src.map(shortSrc).join('; ');
    $('capsrc').title = x.src.map(k => SRC[k] ? SRC[k].t : k).join('\n');
    const c = $('cap'); c.classList.remove('in'); void c.offsetWidth; c.classList.add('in');
  }
};
const words = t => t.split(/\s+/).length;
// reading time ~2.5 words per second, at least 4 s (make_data.py writes this as beat.duration)
const lineMs = b => { const c = b.steps.find(x => x.type === 'caption'); return b.duration || Math.max(4000, Math.round(words(c ? c.text : '') / 2.5 * 1000)); };
const pauseMs = b => b.pauseAfter == null ? 2000 : b.pauseAfter;
const VISUAL = ['migration', 'battle', 'border'];
// planned length of one beat at 1x (without audio)
function beatPlan(b){
  let t = 0; const f = b.steps.find(x => x.type === 'focus'); if (f) t += dur(f) + GAP;
  b.steps.filter(x => VISUAL.includes(x.type)).forEach(x => { t += dur(x) + GAP; });
  return Math.max(lineMs(b), t) + pauseMs(b);
}
const playTotal = () => STOP && STOP.play ? STOP.play.beats.reduce((s, b) => s + beatPlan(b), 0) : 0;
function clearFx(){ gFx.selectAll('*').interrupt().remove(); gFxTop.selectAll('*').remove(); FXZ = []; }
function resetMap(){ clearFx(); drawZones(ERA); drawObjects(); }
function applyInstant(i){ PLAY.beats[i].steps.forEach(x => { if (x.type !== 'caption') STEP[x.type](x, 0); }); }
function runBeat(i){
  if (i >= PLAY.beats.length) return playEnd();
  const b = PLAY.beats[i], t0 = PLAY.clock;
  PLAY.i = i; PLAY.events = []; PLAY.hold = false;
  if (PLAY.audio){ PLAY.audio.pause(); PLAY.audio = null; }
  // earlier beats' arrows and markers step back so the new ones read clearly
  gFx.selectAll(':scope > g').classed('old', true); gFxTop.selectAll(':scope > g').classed('old', true);
  // 1) the line starts: caption (and audio), year counter runs alongside
  b.steps.filter(x => x.type === 'caption' || x.type === 'year').forEach(x => STEP[x.type](x, dur(x) || 1));
  let audioDone = true;
  if (b.audio){ try { audioDone = false; const a = PLAY.audio = new Audio(b.audio); a.playbackRate = SPEED; a.onended = a.onerror = () => { audioDone = true; if (PLAY) PLAY.hold = false; }; a.play().catch(() => { audioDone = true; }); } catch(e){ audioDone = true; } }
  // 2) camera moves first, 3) then one visual event at a time
  let t = t0; const f = b.steps.find(x => x.type === 'focus');
  if (f){ STEP.focus(f, dur(f)); t += dur(f) + GAP; }
  b.steps.filter(x => VISUAL.includes(x.type)).forEach(x => { at(t, () => STEP[x.type](x, dur(x))); t += dur(x) + GAP; });
  // 4) wait for the line to finish (reading time, or the audio), 5) then the pause
  const lineEnd = Math.max(t0 + lineMs(b), t);
  at(lineEnd, () => { if (!audioDone) PLAY.hold = true; });
  at(lineEnd + 1, () => { PLAY.b0 = t0; PLAY.bEnd = lineEnd + pauseMs(b); at(PLAY.clock + pauseMs(b), () => runBeat(i + 1)); });
  PLAY.b0 = t0; PLAY.bEnd = lineEnd + pauseMs(b);
  $('capn').textContent = `${i + 1} / ${PLAY.beats.length}`;
  setPP();
}
function seek(i){
  // rebuild the state of beats 0..i-1 instantly, then play beat i
  if (!PLAY) return;
  i = Math.max(0, Math.min(PLAY.beats.length - 1, i));
  gZones.selectAll('*').interrupt(); svg.interrupt(); PLAY.anims = []; PLAY.events = [];
  resetMap(); YEAR = STOP.year; PLAY.lastFocus = null;
  PLAY.clockOn = false; for (let j = 0; j < i; j++) applyInstant(j); PLAY.clockOn = true;
  if (!PLAY.beats[i].steps.some(x => x.type === 'focus') && PLAY.lastFocus){ const f = PLAY.lastFocus; setHighlight(f.hl || []); flyTo(f.c, f.k, 600); }
  runBeat(i);
}
async function playStart(){
  if (MODE !== 'stop') await go(liveBefore(cur));
  if (!STOP || !STOP.play) return;
  closeObj();
  Object.assign(ERA.zoneObjects, STOP.play.zoneObjects);
  if (PLAY) cancelAnimationFrame(PLAY.raf);
  PLAY = {beats: STOP.play.beats, i: 0, paused: false, clock: 0, clockOn: true, anims: [], events: []};
  document.body.classList.add('playing'); placeCap(); $('cap').hidden = false; drawKeys();
  if (NARROW()) scrollTo({top:0, behavior:'smooth'});
  $('ev').classList.add('dim');
  resetMap(); YEAR = STOP.year; setHighlight([]);
  runBeat(0); PLAY.raf = requestAnimationFrame(tick);
}
// phones: subtitles sit next to the map so they never cover the animation
const NARROW = () => matchMedia('(max-width:899px)').matches;
function placeCap(){ const c = $('cap'), vp = $('vp'); if (NARROW()){ if (c.parentNode === vp) vp.after(c); c.classList.add('below'); } else { if (c.parentNode !== vp) vp.append(c); c.classList.remove('below'); } }
addEventListener('resize', () => { if (PLAY) placeCap(); });
function setPP(){ const p = PLAY && PLAY.paused; $('cappp').textContent = p ? '▶' : '❚❚'; $('cappp').setAttribute('aria-label', p ? 'Play' : 'Pause'); $('cap').classList.toggle('paused', !!p); }
function playPause(force){
  if (!PLAY) return;
  PLAY.paused = force === undefined ? !PLAY.paused : force;
  if (PLAY.audio){ PLAY.paused ? PLAY.audio.pause() : PLAY.audio.play().catch(() => {}); }
  if (PLAY.paused) svg.interrupt();
  setPP();
}
const SPEEDS = [0.75, 1, 1.25];
function setSpeed(v){ SPEED = v; if (PLAY && PLAY.audio) PLAY.audio.playbackRate = v; $('capspd').textContent = (v === 1 ? '1' : String(v)) + '×'; $('capspd').setAttribute('aria-label', 'Speed ' + v + 'x'); }
function playStop(toEnd){
  if (!PLAY) return;
  cancelAnimationFrame(PLAY.raf); if (PLAY.audio) PLAY.audio.pause();
  PLAY = null; document.body.classList.remove('playing'); $('cap').hidden = true; $('ev').classList.remove('dim');
  if (!toEnd){ resetMap(); YEAR = null; $('big').textContent = STOP.label; $('pill').textContent = STOP.label; drawKeys(); showStep(steps().length - 1); }
}
function playEnd(){
  // the transition ends on the new year's intro and stays there
  const to = STOP.play.to; playStop(true);
  const k = STORY.stops.findIndex(s => s.year === to);
  arriveSoon(k, false);
}
$('cappp').onclick = e => { e.stopPropagation(); playPause(); };
$('capnext').onclick = e => { e.stopPropagation(); if (PLAY) seek(PLAY.i + 1 < PLAY.beats.length ? PLAY.i + 1 : PLAY.i) ; };
$('capprev').onclick = e => { e.stopPropagation(); if (PLAY) seek(PLAY.i - 1); };
$('capspd').onclick = e => { e.stopPropagation(); setSpeed(SPEEDS[(SPEEDS.indexOf(SPEED) + 1) % SPEEDS.length] || 1); };
$('capx').onclick = e => { e.stopPropagation(); playStop(false); };
$('capskip').onclick = e => { e.stopPropagation(); if (PLAY){ svg.interrupt(); PLAY.anims = []; PLAY.events = []; resetMap(); YEAR = STOP.year; PLAY.clockOn = false; PLAY.beats.forEach((b, j) => applyInstant(j)); playEnd(); } };
// tapping the map pauses (tapping an object opens its box, which also pauses)
svg.on('click.play', () => { if (PLAY && !PLAY.paused) playPause(true); });

// a stop that is not built yet, reached at the end of Play: the map keeps the end state
const liveBefore = k => { for (let j = k; j >= 0; j--) if (STORY.stops[j].file) return j; return 0; };
function arriveSoon(k, rebuild){
  const s = STORY.stops[k];
  cur = k; MODE = 'soon';
  if (rebuild){ resetMap(); Object.assign(ERA.zoneObjects, STOP.play.zoneObjects); PLAY = {beats: STOP.play.beats, clockOn: false, anims: [], events: []}; STOP.play.beats.forEach((b, j) => applyInstant(j)); PLAY = null; }
  setHighlight(['hills','izbetsartah','philistines','ashdod','ashkelon','ekron','gath']);
  // the end state keeps the new borders; arrows and battle markers belong to the transition only
  gFx.selectAll('*').interrupt().transition().duration(rebuild ? 0 : 700).style('opacity', 0).remove();
  gFxTop.selectAll('*').transition().duration(rebuild ? 0 : 700).style('opacity', 0).remove();
  flyTo([35.0, 31.95], 4.6, rebuild ? 0 : 1400);
  timelineState(s);
  $('chapter').textContent = s.title; $('ev').hidden = false; $('soon').hidden = true;
  const recap = STOP.play.beats.map(b => b.steps.find(x => x.type === 'caption')).filter(c => c && c.cert !== 'scene');
  const all = [...new Set(recap.flatMap(c => c.src))];
  $('evbody').innerHTML = `<div class="kicker">${esc(STORY.title)} · ${esc(s.label)}</div><h2>${esc(s.soon.title)}</h2>` +
    `<div class="soonflag">Next chapter coming soon</div><p class="lead">${esc(s.soon.text)}</p>` +
    `<div class="cta"><button type="button" class="play" id="replay">↺ Replay transition</button><button type="button" id="back1207">‹ Back to ${esc(STOP.label)}</button></div>` +
    `<div class="sub">What changed, step by step</div><ul class="claims">` + recap.map(c => `<li>${badge(c.cert)} ${esc(c.text)}</li>`).join('') + '</ul>' +
    `<details class="src"><summary>Sources (${all.length})</summary>${srcList(all)}</details>`;
  $('evbody').scrollTop = 0;
  $('evn').textContent = '1 / 1'; $('evprev').disabled = true; $('evnext').disabled = true;
  $('replay').onclick = e => { e.stopPropagation(); MODE = 'stop'; cur = liveBefore(k); timelineState(STORY.stops[cur]); playStart(); };
  $('back1207').onclick = e => { e.stopPropagation(); go(liveBefore(k)); };
  drawKeys();
}

// ---------- timeline of stops ----------
const fmt = y => y < 0 ? (-y) + ' BC' : 'AD ' + y;
function buildTrack(){
  const tr = d3.select('#track');
  const pos = y => (100 * (y - STORY.from) / (STORY.to - STORY.from)) + '%';
  [-1000,-500,1,500,1000,1500,2000].forEach(y => tr.append('div').attr('class','tick').style('left', pos(y)).text(y === 1 ? 'AD 1' : fmt(y)));
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
  get play(){ return PLAY ? {i: PLAY.i, n: PLAY.beats.length, paused: PLAY.paused} : null; },
  set speed(v){ setSpeed(v); }, projection };

// donations: hidden until data/site.json has a donateUrl (https only)
getJSON('data/site.json').then(c => { const u = c && c.donateUrl; if (typeof u === 'string' && /^https:\/\//.test(u)){ const a = $('donate'); a.href = u; a.hidden = false; } }).catch(() => {});
(async function init(){
  const [base, story, srcs, lib] = await Promise.all([getJSON('data/base.topo.json'), getJSON(STORY_URL), getJSON('data/sources.json'), getJSON('data/objects/near-east.json')]);
  STORY = story; SRC = srcs; OBJS = lib.objects; OBJS.forEach(o => OBJ[o.id] = o);
  document.title = `${STORY.site} · ${STORY.title}`; $('stitle').textContent = STORY.title;
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
addEventListener('resize', () => { fit(); redrawZones(); });
