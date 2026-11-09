"""Bake the shaded-relief images for the map (warm parchment hypsometric tint + multi-scale hillshade + soft sea depth).
Needs: fetch_tiles.py (DEM cache) and grid.js (pixel lon/lat + land rings). Writes images/terrain/<name>.webp + data/terrain.json.
DEM: Terrain Tiles on AWS Open Data (Terrarium encoding; SRTM, GMTED2010, ETOPO1 etc.), see build/terrain/README.md."""
import json, math, os, sys
import numpy as np
from PIL import Image, ImageDraw, ImageChops, ImageFilter
ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../..'
CACHE = os.environ.get('TLM_TERRAIN_CACHE', '/workspace/tlm-terrain/cache')
WORK = os.environ.get('TLM_TERRAIN_WORK', '/workspace/tlm-terrain/work')
SPEC = {'region': dict(z=7, ex=2.6, q=80), 'levant': dict(z=10, ex=1.7, q=82)}

def mosaic(z, lon, lat):
    X = (lon + 180) / 360 * 2**z * 256
    r = np.radians(lat); Y = (1 - np.log(np.tan(r) + 1 / np.cos(r)) / np.pi) / 2 * 2**z * 256
    tx0, tx1, ty0, ty1 = int(X.min() // 256), int(X.max() // 256), int(Y.min() // 256), int(Y.max() // 256)
    M = np.zeros(((ty1 - ty0 + 1) * 256, (tx1 - tx0 + 1) * 256), np.float32)
    for x in range(tx0, tx1 + 1):
        for y in range(ty0, ty1 + 1):
            a = np.asarray(Image.open(f'{CACHE}/{z}/{x}/{y}.png').convert('RGB'), np.float32)
            M[(y - ty0) * 256:(y - ty0 + 1) * 256, (x - tx0) * 256:(x - tx0 + 1) * 256] = a[..., 0] * 256 + a[..., 1] + a[..., 2] / 256 - 32768
    fx, fy = X - tx0 * 256 - .5, Y - ty0 * 256 - .5
    i0 = np.clip(np.floor(fx).astype(int), 0, M.shape[1] - 2); j0 = np.clip(np.floor(fy).astype(int), 0, M.shape[0] - 2)
    u, v = np.clip(fx - i0, 0, 1), np.clip(fy - j0, 0, 1)
    return (M[j0, i0] * (1 - u) * (1 - v) + M[j0, i0 + 1] * u * (1 - v) + M[j0 + 1, i0] * (1 - u) * v + M[j0 + 1, i0 + 1] * u * v)

def blur(a, r):
    n = max(1, int(r * 3)); k = np.exp(-np.arange(-n, n + 1) ** 2 / (2 * r * r)); k /= k.sum()
    a = np.pad(a.astype(np.float32), n, mode='edge')
    a = sum(k[i] * a[:, i:i + a.shape[1] - 2 * n] for i in range(2 * n + 1))
    return sum(k[i] * a[i:i + a.shape[0] - 2 * n, :] for i in range(2 * n + 1)).astype(np.float32)

def shade(E, mpp, ex, az=315, alt=42):
    gy, gx = np.gradient(E * ex / mpp)
    a, h = math.radians(az), math.radians(alt)
    L = np.array([math.cos(h) * math.sin(a), -math.cos(h) * math.cos(a), math.sin(h)])
    return (-gx * L[0] - gy * L[1] + L[2]) / np.sqrt(gx * gx + gy * gy + 1)

def ramp(v, stops):
    xs = [s[0] for s in stops]; cs = np.array([[int(s[1][i:i + 2], 16) for i in (1, 3, 5)] for s in stops], np.float32)
    return np.stack([np.interp(v, xs, cs[:, k]) for k in range(3)], -1)

LAND = [(-430, '#b4a676'), (-150, '#c6b98a'), (-1, '#dbcfa4'), (0, '#efe5c6'), (120, '#ebdfbb'), (400, '#e1cea2'), (800, '#d5bd8f'),
        (1500, '#c8ac80'), (2500, '#b99d77'), (3800, '#bcab92'), (5000, '#d6cbb8')]
SEA = [(0, '#bccfd3'), (60, '#b3c7ce'), (300, '#a9bec8'), (1500, '#9fb6c1'), (4000, '#97afbb')]

def render(name, z, ex, q):
    meta = json.load(open(f'{WORK}/{name}.json')); w, h = meta['w'], meta['h']
    lon = np.fromfile(f'{WORK}/{name}.lon.f32', np.float32).reshape(h, w); lat = np.fromfile(f'{WORK}/{name}.lat.f32', np.float32).reshape(h, w)
    E = mosaic(z, lon, lat)
    mpp = np.hypot(np.gradient(lon, axis=1) * np.cos(np.radians(lat)) * 111320, np.gradient(lat, axis=1) * 110540)
    # land mask from Natural Earth (the same coast as the vector map), 2x supersampled
    S = 2; mask = Image.new('1', (w * S, h * S), 0)
    for ring in meta['rings']:
        t = Image.new('1', mask.size, 0); ImageDraw.Draw(t).polygon([(x * S, y * S) for x, y in ring], fill=1); mask = ImageChops.logical_xor(mask, t)
    land = np.asarray(mask.convert('L').resize((w, h), Image.LANCZOS), np.float32)[..., None] / 255
    # where Natural Earth's coast and the DEM disagree by a pixel or two, a land pixel near the sea is never below
    # sea level (that is kept for real depressions inland: the Jordan rift, the Dead Sea, the Caspian shore)
    near_sea = blur((land[..., 0] < .5).astype(np.float32), 4 if name == 'region' else 8) > .02
    E = np.where(near_sea & (land[..., 0] >= .5) & (E < 2), np.maximum(E, 2), E)
    # multi-scale light: fine detail + broad forms + a softer second light from the north, so ridges read as 3D
    Es = blur(E, 1.0 if name == 'levant' else 0.6)
    sh = .55 * shade(Es, mpp, ex) + .3 * shade(blur(E, 6), mpp, ex * 2.2) + .15 * shade(Es, mpp, ex, az=0, alt=55)
    flat = math.sin(math.radians(42)) * .85 + math.sin(math.radians(55)) * .15
    m = np.clip(1 + 1.05 * (sh - flat), .5, 1.14)[..., None]
    cl = ramp(E, LAND) * m
    # rift / below-sea floor a touch warmer so the Jordan valley and Dead Sea basin read at once
    seaE = blur(np.clip(-E, 0, None), 5 if name == 'region' else 3)
    cs = ramp(seaE, SEA) * np.clip(1 + .35 * (shade(blur(E, 2), mpp, ex * .6) - .74), .85, 1.06)[..., None]
    rgb = cl * land + cs * (1 - land)
    # feathered edges so the image melts into the map's sea colour / the region image underneath
    f = 48 if name == 'region' else 70
    yy, xx = np.mgrid[0:h, 0:w]; d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy)).astype(np.float32)
    alpha = np.clip(d / f, 0, 1) ** 1.5 * 255
    out = np.dstack([np.clip(rgb, 0, 255), alpha]).astype(np.uint8)
    os.makedirs(f'{ROOT}/images/terrain', exist_ok=True)
    p = f'{ROOT}/images/terrain/{name}.webp'; Image.fromarray(out, 'RGBA').save(p, 'WEBP', quality=q, method=6)
    print(name, w, h, os.path.getsize(p) // 1024, 'KB'); return {'src': f'images/terrain/{name}.webp', 'raw': meta['raw'], 'w': w, 'h': h}

if __name__ == '__main__':
    names = sys.argv[1:] or list(SPEC)
    cfg = {'attribution': 'Relief: Terrain Tiles (AWS Open Data; SRTM, GMTED2010, ETOPO1) · coast: Natural Earth', 'layers': []}
    for n in SPEC:
        if n in names: cfg['layers'].append(dict(name=n, **render(n, **SPEC[n])))
    json.dump(cfg, open(f'{ROOT}/data/terrain.json', 'w'), indent=1)
