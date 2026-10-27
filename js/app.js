/* The Long Map: vector base map, zones as data, timeline. */
const $ = id => document.getElementById(id);
const esc = s => String(s).replace(/[&<>"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
let STOP = null;          // loaded stop data (zones, cards, sources, places)
let TL = null;            // timeline.json
let cur = 0;              // index of current stop
let K = 1;                // current zoom scale
const cache = {};

const svg = d3.select('#map');
const root = svg.append('g');
const gLand = root.append('g'), gZones = root.append('g'), gPlaces = root.append('g');
const projection = d3.geoConicConformal().parallels([30, 40]).rotate([-38, 0]);
const path = d3.geoPath(projection);
const VIEW = {type:'MultiPoint', coordinates:[[20,24],[57,24],[20,43],[57,43],[38,44.5]]};

// d3 wants clockwise outer rings; if a polygon covers more than half the globe, its rings are reversed.
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
  gLand.selectAll('path').attr('d', path);
  gZones.selectAll('path').attr('d', path);
  gZones.selectAll('circle.hit').each(function(d){ const p = projection(d.c); d3.select(this).attr('cx',p[0]).attr('cy',p[1]); });
  gZones.selectAll('text.zlabel').each(function(d){ const p = projection(d.c); d3.select(this).attr('x',p[0]).attr('y',p[1]); });
  gPlaces.selectAll('g.place').attr('transform', d => { const p = projection([d[1],d[2]]); return `translate(${p[0]},${p[1]})`; });
  scaleMarks();
}

// Keep dots and labels the same size on screen at any zoom, and show small towns only when zoomed in.
function scaleMarks(){
  gPlaces.selectAll('g.place')
    .style('display', d => (d[3] === 1 || (d[3] === 2 && K >= 2) || (d[3] === 3 && K >= 5)) ? null : 'none')
    .each(function(){ d3.select(this).select('.inner').attr('transform', `scale(${1/K})`); });
  gZones.selectAll('text.zlabel').style('font-size', (10/K) + 'px').style('stroke-width', (2/K) + 'px').style('display', K > 9 ? 'none' : null);
  gZones.selectAll('circle.hit').attr('r', 16/K);
  gZones.selectAll('.israel').attr('filter', K < 3 ? null : 'url(#soft)');
}

const zoom = d3.zoom().scaleExtent([1, 40]).on('zoom', e => {
  K = e.transform.k;
  root.attr('transform', e.transform);
  scaleMarks();
});
svg.call(zoom).on('dblclick.zoom', null);

// soft edge for the Israel "people" area
svg.append('defs').html('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="0.6"/></filter>');

async function getJSON(u){ if (!cache[u]) cache[u] = fetch(u).then(r => { if (!r.ok) throw new Error(u+' '+r.status); return r.json(); }); return cache[u]; }

function centroidOf(features){
  // largest "sure" part, else largest part
  const pick = features.slice().sort((a,b) => (b.properties.certainty==='sure') - (a.properties.certainty==='sure') || d3.geoPath().area(b) - d3.geoPath().area(a))[0];
  return d3.geoPath().centroid(pick);
}
function centroidLonLat(f){ const b = d3.geoBounds(f); return [(b[0][0]+b[1][0])/2, (b[0][1]+b[1][1])/2]; }

function drawZones(stop){
  const t = d3.transition().duration(350);
  gZones.selectAll('*').transition(t).style('opacity', 0).remove();
  if (!stop) { gPlaces.selectAll('*').remove(); return; }
  const g = gZones.append('g').style('opacity', 0);
  const feats = stop.zones.features;
  const states = feats.filter(f => f.properties.certainty !== 'people');
  const people = feats.filter(f => f.properties.certainty === 'people');
  g.selectAll('path.halo').data(states.filter(f => f.properties.certainty === 'unsure')).join('path')
    .attr('class', f => 'halo z-' + f.properties.zone).style('stroke', null);
  g.selectAll('path.zone').data(states).join('path')
    .attr('class', f => `zone ${f.properties.certainty} z-${f.properties.zone}`)
    .on('click', (e, f) => { e.stopPropagation(); openZ(f.properties.zone); })
    .append('title').text(f => stop.cards[f.properties.zone].name + ': ' + f.properties.part);
  const ids = [...new Set(feats.map(f => f.properties.zone))];
  g.selectAll('text.zlabel').data(ids.map(id => ({id, c: stop.cards[id].labelAt || centroidOf(feats.filter(f => f.properties.zone === id))}))).join('text')
    .attr('class', d => 'zlabel' + (d.id === 'israel' ? ' zl-people' : '')).text(d => stop.cards[d.id].name)
    .on('click', (e, d) => { e.stopPropagation(); openZ(d.id); });
  g.selectAll('path.israel').data(people).join('path').attr('class','israel')
    .on('click', (e, f) => { e.stopPropagation(); openZ(f.properties.zone); });
  // generous tap target for the small "people" areas
  g.selectAll('circle.hit').data(people.map(f => ({id:f.properties.zone, c:centroidLonLat(f)}))).join('circle').attr('class','hit')
    .on('click', (e, d) => { e.stopPropagation(); openZ(d.id); });
  g.transition(t).style('opacity', 1);
  gPlaces.selectAll('*').remove();
  const pl = gPlaces.selectAll('g.place').data(stop.places).join('g')
    .attr('class', d => 'place' + (['Shechem','Hebron'].includes(d[0]) ? ' israel-l' : ''));
  const inner = pl.append('g').attr('class','inner');
  inner.append('circle').attr('r', d => d[3] === 1 ? 2.8 : 2.2);
  inner.append('text').attr('x', 4).attr('y', 3.5).text(d => d[0]);
  redraw();
}

function openZ(id){
  if (!STOP || !STOP.cards[id]) return;
  const z = STOP.cards[id];
  const parts = STOP.zones.features.filter(f => f.properties.zone === id).map(f => f.properties);
  const lab = {sure:'Solid: core well documented', unsure:'Dashed: extent uncertain', people:'Gold: a people, no border'};
  $('kicker').textContent = STOP.label + ' · evidence';
  $('zt').textContent = z.name;
  $('facts').innerHTML = z.rows.map(r => '<div class="row"><b>'+esc(r[0])+'</b><span>'+esc(r[1])+'</span></div>').join('');
  $('area').innerHTML = parts.map(p => '<span>'+esc(lab[p.certainty])+' · '+esc(p.part)+'</span>').join('');
  $('pics').innerHTML = z.pics.map(p => '<img class="shot" alt="" src="'+esc(p.src)+'"><p class="cap">'+esc(p.cap)+'</p>').join('');
  $('src').innerHTML = '<b>Sources</b><ol>' + z.sources.map(k => '<li>'+esc(STOP.sources[k])+'</li>').join('') + '</ol><p class="cap">'+esc(STOP.note)+'</p>';
  $('play').hidden = !z.story;
  $('sheet').classList.add('open');
}
function closeZ(){ $('sheet').classList.remove('open'); }
$('sheet').addEventListener('click', e => { if (e.target.id === 'sheet') closeZ(); });

// ---------- timeline ----------
const fmt = y => y < 0 ? (-y) + ' BC' : 'AD ' + y;
function buildTrack(){
  const tr = d3.select('#track');
  const pos = y => (100 * (y - TL.from) / (TL.to - TL.from)) + '%';
  [-1000,-500,1,500,1000,1500,2000].forEach(y => tr.append('div').attr('class','tick').style('left', pos(y)).text(y === 1 ? 'AD 1' : fmt(y)));
  tr.selectAll('button.mk').data(TL.stops).join('button')
    .attr('class', d => 'mk' + (d.file ? ' live' : '')).attr('type','button')
    .attr('aria-label', d => d.label + (d.file ? '' : ', coming soon'))
    .style('left', d => pos(d.year))
    .on('click', (e, d) => go(TL.stops.indexOf(d)));
}
async function go(i){
  cur = Math.max(0, Math.min(TL.stops.length - 1, i));
  const s = TL.stops[cur];
  $('big').textContent = s.label; $('big').classList.toggle('soon', !s.file);
  $('ttitle').textContent = s.title + (s.file ? '' : ' · coming soon');
  $('prev').disabled = cur === 0; $('next').disabled = cur === TL.stops.length - 1;
  d3.selectAll('#track .mk').classed('cur', (d, j) => j === cur);
  $('soon').hidden = !!s.file; $('soont').textContent = s.label + ' · ' + s.title;
  $('pill').textContent = s.label;
  if (s.file){ STOP = await getJSON(s.file); if (!STOP._wound){ rewindAll(STOP.zones); STOP._wound = true; } $('chapter').textContent = STOP.title; drawZones(STOP); }
  else { STOP = null; $('chapter').textContent = 'Planned stop'; drawZones(null); }
}
$('prev').onclick = () => go(cur - 1);
$('next').onclick = () => go(cur + 1);

// test hook used by the screenshot script: zoom in on the southern Levant
window.__zoomTest = () => { const [w,h] = size(); const p = projection([35.3, 32.0]); svg.transition().duration(600).call(zoom.transform, d3.zoomIdentity.translate(w/2, h/2).scale(7).translate(-p[0], -p[1])); };

(async function init(){
  const [base, tl] = await Promise.all([getJSON('data/base.topo.json'), getJSON('data/timeline.json')]);
  TL = tl;
  const o = base.objects;
  gLand.append('path').datum(rewindAll(d3.feature(base, o.land))).attr('class','land');
  gLand.selectAll('path.lake').data(rewindAll(d3.feature(base, o.lakes)).features).join('path').attr('class','lake');
  gLand.selectAll('path.river').data(d3.feature(base, o.rivers).features).join('path')
    .attr('class', d => 'river' + (d.properties.src === 'approx' ? ' approx' : ''))
    .append('title').text(d => d.properties.name + (d.properties.src === 'approx' ? ' (drawn approximately)' : ''));
  fit();
  buildTrack();
  await go(TL.stops.findIndex(s => s.file));
})();
addEventListener('resize', fit);

// ---------- story (unchanged words, no made-up artefact image) ----------
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
