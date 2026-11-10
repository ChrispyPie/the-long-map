// The land (coast mask) for the relief tiles, in the map's own projection at scale 1 / translate 0 (raw units, y down):
// the Near East land of data/base.topo.json (the coast the vector map draws) plus the land of the outer world layer
// (Natural Earth 50m outside the Near East box, unclipped: work/mask_outer.topo.json from build/world/build.sh). Two separate ring sets: render_tiles.py
// rasterises each with even-odd fill and ORs them.   Usage: node build/terrain/rings.js [OUT.json]
const fs = require('fs'), vm = require('vm');
global.window = global; global.self = global; global.document = {};
vm.runInThisContext(fs.readFileSync(__dirname + '/../../js/d3-lite.min.js', 'utf8'));
const out = process.argv[2] || '/workspace/tlm-terrain/work/rings_raw.json';
const p = d3.geoConicConformal().parallels([30, 40]).rotate([-38, 0]).scale(1).translate([0, 0]);
const fix = poly => d3.geoArea({type:'Polygon', coordinates:poly}) > 2*Math.PI ? poly.map(r => r.slice().reverse()) : poly;
function rings(file){
  if (!fs.existsSync(file)) return [];
  const topo = JSON.parse(fs.readFileSync(file)), land = d3.feature(topo, topo.objects.land), R = [];
  (land.features || [land]).forEach(f => { const g = f.geometry; if (!g) return; if (g.type === 'Polygon') g.coordinates = fix(g.coordinates); if (g.type === 'MultiPolygon') g.coordinates = g.coordinates.map(fix); });
  let cur = null; const end = () => { if (cur && cur.length > 2) R.push(cur.map(q => [+q[0].toFixed(7), +q[1].toFixed(7)])); cur = null; };
  d3.geoPath(p, {moveTo(x, y){ end(); cur = [[x, y]]; }, lineTo(x, y){ cur.push([x, y]); }, closePath(){ end(); }, arc(){}})(land); end();
  return R;
}
const res = {near: rings(__dirname + '/../../data/base.topo.json'), outer: rings(process.env.TLM_MASK || '/workspace/tlm-terrain/work/mask_outer.topo.json')};
fs.mkdirSync(require('path').dirname(out), {recursive: true}); fs.writeFileSync(out, JSON.stringify(res));
console.log('rings near', res.near.length, 'outer', res.outer.length);
