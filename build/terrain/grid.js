// For each relief image: its box in the map's own projection (scale 1, translate 0), the lon/lat of every
// pixel (for sampling the DEM) and the Natural Earth land in pixel coords (for the coast mask).
// Usage: node build/terrain/grid.js OUTDIR
const fs = require('fs'), vm = require('vm');
global.window = global; global.self = global; global.document = {};
vm.runInThisContext(fs.readFileSync(__dirname + '/../../js/d3-lite.min.js', 'utf8'));
const out = process.argv[2] || '/workspace/tlm-terrain/work'; fs.mkdirSync(out, {recursive: true});
const P = () => d3.geoConicConformal().parallels([30, 40]).rotate([-38, 0]).scale(1).translate([0, 0]);
const IMAGES = {region: {box: [14, 18, 64, 48], w: 3000}, levant: {box: [33.6, 29.0, 37.8, 34.4], w: 2400}};
const base = JSON.parse(fs.readFileSync(__dirname + '/../../data/base.topo.json'));
const land = d3.feature(base, base.objects.land);
const fix = poly => d3.geoArea({type:'Polygon', coordinates:poly}) > 2*Math.PI ? poly.map(r => r.slice().reverse()) : poly;
(land.features || [land]).forEach(f => { const g = f.geometry; if (g.type === 'Polygon') g.coordinates = fix(g.coordinates); if (g.type === 'MultiPolygon') g.coordinates = g.coordinates.map(fix); });
for (const [name, im] of Object.entries(IMAGES)){
  const p = P(), [a, b, c, d] = im.box, ring = [];
  for (let t = 0; t <= 100; t++){ ring.push([a + (c - a) * t / 100, b], [a + (c - a) * t / 100, d], [a, b + (d - b) * t / 100], [c, b + (d - b) * t / 100]); }
  const xy = ring.map(q => p(q)), xs = xy.map(q => q[0]), ys = xy.map(q => q[1]);
  // the inner box (inside the curved lon/lat box) so the image is a plain rectangle of real data
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  const w = im.w, h = Math.round(w * (y1 - y0) / (x1 - x0));
  const lon = new Float32Array(w * h), lat = new Float32Array(w * h);
  for (let j = 0; j < h; j++) for (let i = 0; i < w; i++){
    const q = p.invert([x0 + (i + .5) * (x1 - x0) / w, y0 + (j + .5) * (y1 - y0) / h]); lon[j * w + i] = q[0]; lat[j * w + i] = q[1];
  }
  fs.writeFileSync(`${out}/${name}.lon.f32`, Buffer.from(lon.buffer)); fs.writeFileSync(`${out}/${name}.lat.f32`, Buffer.from(lat.buffer));
  // land rings in pixel coords
  const pp = P().scale(w / (x1 - x0)).translate([-x0 * w / (x1 - x0), -y0 * w / (x1 - x0)]);
  const rings = [];
  let cur = null; const end = () => { if (cur && cur.length > 2) rings.push(cur); cur = null; };
  d3.geoPath(pp, {moveTo(x, y){ end(); cur = [[x, y]]; }, lineTo(x, y){ cur.push([x, y]); }, closePath(){ end(); }, arc(){}})(land); end();
  fs.writeFileSync(`${out}/${name}.json`, JSON.stringify({raw: [x0, y0, x1, y1], w, h, rings}));
  console.log(name, w, h, rings.length);
}
