"""Bake the relief tile pyramid (see pyramid.py): warm parchment hypsometric tint + multi-scale hillshade + soft sea
depth, the same look as render.py, cut into 512-px WebP tiles (+1 px bleed) at images/terrain/<n>/<i>_<j>.webp,
and write the manifest data/terrain.json that js/app.js reads.
Needs: fetch_tiles.py (DEM cache) and rings.js (coast mask).  Usage: python3 build/terrain/render_tiles.py [levels...]"""
import json, math, os, sys
from multiprocessing import Pool
import numpy as np
from PIL import Image, ImageDraw, ImageChops
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyramid as PY
from render import blur, shade, ramp, LAND, SEA, ROOT, WORK
PAD = 32
EX = {0: 2.6, 1: 2.6, 2: 2.6, 3: 2.6, 4: 2.2, 5: 1.9, 6: 1.7, 7: 1.7, 8: 1.7}
Q = 78
RINGS = None
CACHE = os.environ.get('TLM_TERRAIN_CACHE', '/workspace/tlm-terrain/cache')
_dem = {}

def dem(z, x, y):
    x %= 2 ** z; y = min(max(y, 0), 2 ** z - 1); k = (z, x, y)
    if k not in _dem:
        if len(_dem) > 400: _dem.clear()
        a = np.asarray(Image.open(f'{CACHE}/{z}/{x}/{y}.png').convert('RGB'), np.float32)
        _dem[k] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
    return _dem[k]

def mosaic(z, lon, lat):
    """bilinear DEM sample (Terrarium web-mercator tiles at zoom z) at every lon/lat (wraps in lon, clamps at +-85 lat)"""
    X = (lon + 180) / 360 * 2**z * 256
    r = np.radians(np.clip(lat, -85, 85)); Y = (1 - np.log(np.tan(r) + 1 / np.cos(r)) / np.pi) / 2 * 2**z * 256
    tx0, tx1, ty0, ty1 = int(X.min() // 256), int(X.max() // 256), int(Y.min() // 256), int(Y.max() // 256)
    M = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256), np.float32)
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1): M[(y - ty0) * 256:(y - ty0 + 1) * 256, (x - tx0) * 256:(x - tx0 + 1) * 256] = dem(z, x, y)
    fx, fy = X - tx0 * 256 - .5, Y - ty0 * 256 - .5
    i0 = np.clip(np.floor(fx).astype(int), 0, M.shape[1] - 2); j0 = np.clip(np.floor(fy).astype(int), 0, M.shape[0] - 2)
    u, v = np.clip(fx - i0, 0, 1), np.clip(fy - j0, 0, 1)
    return (M[j0, i0] * (1 - u) * (1 - v) + M[j0, i0 + 1] * u * (1 - v) + M[j0 + 1, i0] * (1 - u) * v + M[j0 + 1, i0 + 1] * u * v)

def mask(n, i, j, N):
    """land coverage (0..1) of the N x N tile pixels (incl. bleed + pad), 2x supersampled"""
    S = PY.S0 / 2 ** n; m = 1 + PAD; px = S / PY.P
    x0, y0 = PY.X0 + i * S - m * px, PY.Y0 + j * S - m * px; x1, y1 = x0 + N * px, y0 + N * px
    SS = 2; out = None
    for key in ('near', 'outer'):
        im = Image.new('1', (N * SS, N * SS), 0)
        for r in RINGS[key]:
            a = np.asarray(r)
            if a[:, 0].max() < x0 or a[:, 0].min() > x1 or a[:, 1].max() < y0 or a[:, 1].min() > y1: continue
            t = Image.new('1', im.size, 0)
            ImageDraw.Draw(t).polygon([((x - x0) / px * SS, (y - y0) / px * SS) for x, y in a], fill=1); im = ImageChops.logical_xor(im, t)
        out = im if out is None else ImageChops.logical_or(out, im)
    return np.asarray(out.convert('L').resize((N, N), Image.LANCZOS), np.float32) / 255

def tile(args):
    n, i, j = args
    p = f'{ROOT}/images/terrain/{n}/{i}_{j}.webp'
    lon, lat = PY.tile_lonlat(n, i, j, PAD); N = lon.shape[0]
    E = mosaic(PY.LEVELS[n][0], lon, lat)
    mpp = np.hypot(np.gradient(lon, axis=1) * np.cos(np.radians(lat)) * 111320, np.gradient(lat, axis=1) * 110540)
    land = mask(n, i, j, N)
    near_sea = blur((land < .5).astype(np.float32), 4 if n <= 4 else 8) > .02
    E = np.where(near_sea & (land >= .5) & (E < 2), np.maximum(E, 2), E)
    ex = EX[n]; fine = .6 if n <= 4 else (.8 if n == 5 else 1.0)
    Es = blur(E, fine)
    sh = .55 * shade(Es, mpp, ex) + .3 * shade(blur(E, 6), mpp, ex * 2.2) + .15 * shade(Es, mpp, ex, az=0, alt=55)
    flat = math.sin(math.radians(42)) * .85 + math.sin(math.radians(55)) * .15
    m = np.clip(1 + 1.05 * (sh - flat), .5, 1.14)[..., None]
    cl = ramp(E, LAND) * m
    # sea depth from at most z7 (smooth bathymetry; the fine DEM zooms have flat blocks offshore)
    Ed = E if PY.LEVELS[n][0] <= 7 else mosaic(7, lon, lat)
    seaE = blur(np.clip(-Ed, 0, None), 5 if n <= 3 else 3)
    cs = ramp(seaE, SEA) * np.clip(1 + .35 * (shade(blur(Ed, 2), mpp, ex * .6) - .74), .85, 1.06)[..., None]
    rgb = cl * land[..., None] + cs * (1 - land[..., None])
    rgb = rgb[PAD:N - PAD, PAD:N - PAD]                      # 514 x 514: the tile + 1 px bleed
    os.makedirs(os.path.dirname(p), exist_ok=True)
    Image.fromarray(np.clip(rgb + .5, 0, 255).astype(np.uint8), 'RGB').save(p, 'WEBP', quality=Q, method=6)
    return n, os.path.getsize(p)

def init():
    global RINGS
    RINGS = json.load(open(f'{WORK}/rings_raw.json'))

if __name__ == '__main__':
    lv = [int(a) for a in sys.argv[1:]] or list(PY.LEVELS)
    jobs = [(n, i, j) for n in lv for i, j in sorted(PY.tiles(n))]
    sizes = {}
    with Pool(int(os.environ.get('JOBS', os.cpu_count() or 4)), initializer=init) as pool:
        for k, (n, s) in enumerate(pool.imap_unordered(tile, jobs, chunksize=2)):
            sizes.setdefault(n, []).append(s)
            if k % 25 == 0: print(k, '/', len(jobs), flush=True)
    for n in sorted(sizes): print('level', n, len(sizes[n]), 'tiles', sum(sizes[n]) // 1024, 'KB', 'avg', sum(sizes[n]) // len(sizes[n]) // 1024, 'KB')
    # manifest: every level's grid + tile list (as [i, j] pairs) and the lon/lat boxes it covers
    cfg = {'attribution': 'Relief: Terrain Tiles (AWS Open Data; SRTM, GMTED2010, ETOPO1) \u00b7 coast: Natural Earth',
           'grid': {'X0': PY.X0, 'Y0': PY.Y0, 'S0': PY.S0, 'P': PY.P, 'bleed': 1, 'parallels': list(PY.PAR), 'rotate': [PY.ROT, 0]},
           'src': 'images/terrain/{n}/{i}_{j}.webp',
           'levels': [{'n': n, 'dem': PY.LEVELS[n][0], 'boxes': PY.LEVELS[n][1],
                       'tiles': [[i, j] for i, j in sorted(PY.tiles(n)) if os.path.exists(f'{ROOT}/images/terrain/{n}/{i}_{j}.webp')]}
                      for n in PY.LEVELS]}
    s = json.dumps(cfg, separators=(',', ':'))
    open(f'{ROOT}/data/terrain.json', 'w').write(s + '\n'); print('manifest', len(s), 'B')
