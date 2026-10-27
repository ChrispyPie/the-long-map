/* The Long Map: stories on a vector map.
   A story (data/stories/<id>/story.json) has stops. Each stop has events = big fact boxes, the narrative.
   Map objects come from a shared library (data/objects/*.json) = small fact boxes, reused by every story.
   Sources come from a shared registry (data/sources.json). */
const $ = id => document.getElementById(id);
const esc = s => String(s == null ? '' : s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const STORY_URL = 'data/stories/jews/story.json';
let STORY = null, STOP = null, ERA = null, SRC = {}, OBJ = {}, OBJS = [];
let cur = 0, step = 0, K = 1, openId = null;
const cache = {};
const CERT = {attested:'Attested', disputed:'Disputed', tradition:'Tradition'};
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
const gLand = root.append('g'), gZones = root.append('g'), gLines = root.append('g'), gPts = root.append('g');
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
  root.selectAll('path').attr('d', path);
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
  openId = id;
  let zoneParts = '';
  if (o.zone && ERA){
    const lab = {sure:'Solid: core well documented', unsure:'Dashed: extent uncertain', people:'Gold: a people, no border'};
    zoneParts = '<div class="area">' + ERA.zones.features.filter(f => f.properties.zone === o.zone).map(f => `<span>${esc(lab[f.properties.certainty])} · ${esc(f.properties.part)}</span>`).join('') + '</div>';
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
}
function closeObj(){ openId = null; $('pop').hidden = true; document.body.classList.remove('popopen'); gPts.selectAll('g.obj').classed('sel', false); gLines.selectAll('g.lobj').classed('sel', false); }
$('popx').onclick = e => { e.stopPropagation(); closeObj(); };
document.addEventListener('click', e => {
  if ($('pop').hidden) return;
  if (e.target.closest('#pop') || e.target.closest('.tap') || e.target.closest('.chip')) return;
  closeObj();
});
addEventListener('keydown', e => { if (e.key === 'Escape') closeObj(); });

// ---------- big fact box: the narrative ----------
function steps(){ return STOP ? [{intro:true}, ...STOP.events] : []; }
function showStep(i, fly = true){
  const S = steps(); if (!S.length) return;
  step = Math.max(0, Math.min(S.length - 1, i));
  const e = S[step], last = step === S.length - 1;
  const chips = ids => '<div class="chips">' + ids.map(id => OBJ[id] ? `<button type="button" class="chip" data-o="${id}">${icon(OBJ[id].type)}${esc(OBJ[id].name)}</button>` : '').join('') + '</div>';
  let h;
  if (e.intro){
    h = `<div class="kicker">${esc(STORY.title)} · ${esc(STOP.label)}</div><h2>${esc(STOP.title)}</h2>` +
        `<p class="lead">${esc(STORY.intro)}</p><p>${esc(STOP.transitionIn)}</p>` +
        `<div class="sub">Key places and peoples</div>${chips(STOP.keyObjects)}` +
        `<div class="legend2">${badge('attested')} found in ancient evidence · ${badge('disputed')} scholars disagree · ${badge('tradition')} Jewish tradition and the Hebrew Bible</div>`;
  } else {
    h = `<div class="kicker">${esc(e.kicker)} · ${esc(e.date)}</div><h2>${esc(e.title)} ${badge(e.cert)}</h2>` +
        `<p class="lead">${esc(e.text)}</p>` +
        `<div class="why"><div class="sub">What it meant for Israel</div><p>${esc(e.why)}</p></div>` +
        (e.pic ? `<img class="shot" alt="" src="${esc(e.pic.src)}"><p class="cap">${esc(e.pic.cap)}</p>` : '') +
        (e.id === 'stele' && STOP.narration ? `<button class="play" type="button" onclick="openStory()">Listen: draft narration</button><p class="cap">${esc(STOP.narration.note)}</p>` : '') +
        `<div class="sub">The evidence</div><ul class="claims">` + e.claims.map(c => `<li>${badge(c[1])} ${esc(c[0])}</li>`).join('') + '</ul>' +
        `<div class="sub">On the map</div>${chips(e.objects)}` +
        `<details class="src"><summary>Sources (${e.src.length})</summary>${srcList(e.src)}</details>`;
    if (last && STOP.transitionOut) h += `<div class="next"><p>${esc(STOP.transitionOut.text)}</p></div>`;
  }
  $('evbody').innerHTML = h; $('evbody').scrollTop = 0;
  $('evn').textContent = `${step + 1} / ${S.length}`;
  $('evprev').disabled = step === 0; $('evnext').disabled = last;
  $('evbody').querySelectorAll('.chip').forEach(b => b.onclick = ev => { ev.stopPropagation(); openObj(b.dataset.o, true); });
  closeObj();
  setHighlight(e.intro ? STOP.keyObjects : e.hl);
  if (fly) { if (e.intro) flyTo([35.6, 33.2], 1.6); else flyTo(e.focus.c, e.focus.k); }
}
$('evprev').onclick = () => showStep(step - 1);
$('evnext').onclick = () => showStep(step + 1);

// ---------- timeline of stops ----------
const fmt = y => y < 0 ? (-y) + ' BC' : 'AD ' + y;
function buildTrack(){
  const tr = d3.select('#track');
  const pos = y => (100 * (y - STORY.from) / (STORY.to - STORY.from)) + '%';
  [-1000,-500,1,500,1000,1500,2000].forEach(y => tr.append('div').attr('class','tick').style('left', pos(y)).text(y === 1 ? 'AD 1' : fmt(y)));
  tr.selectAll('button.mk').data(STORY.stops).join('button')
    .attr('class', d => 'mk' + (d.file ? ' live' : '')).attr('type','button')
    .attr('aria-label', d => d.label + (d.file ? '' : ', coming soon'))
    .style('left', d => pos(d.year)).on('click', (e, d) => go(STORY.stops.indexOf(d)));
}
async function go(i){
  cur = Math.max(0, Math.min(STORY.stops.length - 1, i));
  const s = STORY.stops[cur];
  $('big').textContent = s.label; $('big').classList.toggle('soon', !s.file);
  $('ttitle').textContent = s.title + (s.file ? '' : ' · coming soon');
  $('prev').disabled = cur === 0; $('next').disabled = cur === STORY.stops.length - 1;
  d3.selectAll('#track .mk').classed('cur', (d, j) => j === cur);
  $('soon').hidden = !!s.file; $('soont').textContent = s.label + ' · ' + s.title;
  $('pill').textContent = s.label;
  closeObj();
  if (s.file){
    [STOP, ERA] = await Promise.all([getJSON(s.file), getJSON(s.era)]);
    if (!ERA._wound){ rewindAll(ERA.zones); ERA._wound = true; }
    $('chapter').textContent = STOP.title;
    drawZones(ERA); drawObjects(); $('ev').hidden = false; showStep(0);
  } else {
    STOP = null; ERA = null; $('chapter').textContent = 'Planned stop';
    drawZones(null); gPts.selectAll('*').remove(); gLines.selectAll('*').remove(); $('ev').hidden = true;
  }
}
$('prev').onclick = () => go(cur - 1);
$('next').onclick = () => go(cur + 1);

window.__zoomTest = () => flyTo([35.3, 32.0], 7, 600);
window.__app = { openObj, closeObj, showStep, get step(){ return step; }, get K(){ return K; }, get open(){ return openId; }, projection };

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

// ---------- draft narration (unchanged words; flagged as draft, not every line sourced) ----------
const TALE = "Down on the coast, Egypt still holds the cities. Gaza. Ashkelon. The roads, and the grain that moves along them. A king in the Nile valley can name those cities. He can send soldiers to their gates. Up in the hills, between Shechem and Hebron, there is no gate worth naming. Stone houses sit on the ridges. Terraces cut the slope into thin green steps. Flocks move in the last light. No king. No wall a pharaoh would bother to write down. Then Merneptah, king of Egypt, has a victory stone cut. He lists the cities he claims to have crushed. Ashkelon. Gezer. Yanoam. And then one line is different. Israel is laid waste. Its seed is not. The mark beside the name is not the mark for a city. It is the mark for a people. No capital. No border a scribe could draw. But the name is already in the stone. In the hills above the Egyptian road, a people is living who will one day be called by that name in every empire that follows. Tonight they are only villages. A fire on a ridge. And a word an Egyptian chisel was not supposed to make eternal.";
const words = TALE.split(/\s+/);
const weights = words.map(w => w.replace(/[^A-Za-z]/g,'').length + (/[.!?]/.test(w) ? 4 : 0) + 1);
const weightSum = weights.reduce((a,b)=>a+b,0);
const DURATION = 66.6;
let cursor = 0;
const times = weights.map(w => { const start = cursor; cursor += DURATION * w / weightSum; return start; });
const stoneAt = words.findIndex(w => w.startsWith('Then'));
const inner = $('reel-inner');
inner.innerHTML = words.map((w,i)=>`<span class="w" id="w${i}">${w}</span>`).join(' ');
// Before the stele: a made scene (labelled). From the stele on: the real photograph, with credit.
const STILLS = {
  scene: {src:'images/ridge.jpg', label:'Scene, not a photograph'},
  stele: {src:'images/merneptah.jpg', label:'Real photo: Merneptah Stele, Cairo. Onceinawhile, 2022, CC BY-SA 4.0'}
};
let still = 'scene';
function setStill(k){ if (k === still) return; still = k; $('still').src = STILLS[k].src; $('scene').textContent = STILLS[k].label; }
function openStory(){ $('story').classList.add('open'); const a = $('narr'); a.currentTime = 0; a.play().catch(()=>{}); }
function closeStory(){ $('narr').pause(); $('story').classList.remove('open'); }
function togglePlay(){ const a = $('narr'); if (a.paused) a.play().catch(()=>{}); else a.pause(); }
function skip(s){ const a = $('narr'); a.currentTime = Math.max(0, Math.min((a.duration||DURATION)-0.2, a.currentTime + s)); }
const narr = $('narr');
narr.addEventListener('play', () => $('pp').textContent = 'Pause');
narr.addEventListener('pause', () => $('pp').textContent = 'Play');
narr.addEventListener('timeupdate', () => {
  const t = narr.currentTime;
  let i = 0;
  while (i < times.length-1 && times[i+1] <= t) i++;
  document.querySelectorAll('.w.on').forEach(el => el.classList.remove('on'));
  const el = $('w'+i);
  if (el) el.classList.add('on');
  const reel = $('reel');
  inner.style.transform = `translateY(${-(el.offsetTop - reel.clientHeight * 0.62)}px)`;
  setStill(i >= stoneAt ? 'stele' : 'scene');
  const m = Math.floor(t/60), s = Math.floor(t%60);
  $('time').textContent = m + ':' + String(s).padStart(2,'0');
});
