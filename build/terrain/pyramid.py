"""The relief tile pyramid: one grid in the map's own projection, shared by the renderer (render_tiles.py),
the DEM fetcher (fetch_tiles.py) and the site (js/app.js reads data/terrain.json).

Projection: d3.geoConicConformal().parallels([30, 40]).rotate([-38, 0]) at scale 1, translate [0, 0]
(the same as js/app.js; data/world.json). Raw units: x right, y down (d3's screen convention).
Tile (n, i, j) covers x in [X0 + i*S, X0 + (i+1)*S], y in [Y0 + j*S, ...] with S = S0 / 2**n; each tile is a
P-pixel WebP plus a 1-pixel bleed on every side (P + 2 px) so neighbours overlap and no seam shows.

Levels: each level covers a lon/lat box (the whole map at the coarse levels, then ever smaller boxes around the
places the story is told), so detail costs download only where it is used and only when that spot is on screen.
Add a region later (Europe, North Africa, Central Asia ...) by adding a box at the levels it needs."""
import math
import numpy as np

S0, P, X0, Y0 = 1.0, 512, -2.0, -2.0
PAR, ROT = (30.0, 40.0), -38.0
# n: (DEM zoom (Terrarium, web mercator), [lon0, lat0, lon1, lat1] boxes covered at this level)
LEVELS = {
    0: (4, [[-20, -2, 95, 66]]),
    1: (5, [[-20, -2, 95, 66]]),
    2: (6, [[-20, -2, 95, 66]]),                     # the whole world map (Europe, North Africa, Middle East, Central Asia)
    3: (7, [[-20, -2, 95, 66]]),                      # the whole world map again, sharper (Europe, Africa, Central Asia)
    4: (8, [[24, 26, 52, 40]]),                       # the core: Nile delta, Levant, Mesopotamia
    5: (9, [[30, 28, 46, 38]]),
    6: (10, [[32.6, 28.2, 38.8, 35.2]]),              # Levant (the old 'levant' image)
    7: (11, [[34.0, 29.6, 36.6, 33.6]]),              # Israel / Judah, Philistia, Transjordan
    8: (12, [[34.6, 31.0, 35.75, 32.7]]),             # the hill country, Jerusalem to Samaria, Lachish, the Dead Sea
}

_y0, _y1 = math.radians(PAR[0]), math.radians(PAR[1])
_f = lambda y: np.tan((math.pi / 2 + y) / 2)
_n = math.log(math.cos(_y0) / math.cos(_y1)) / math.log(_f(_y1) / _f(_y0))
_F = math.cos(_y0) * _f(_y0) ** _n / _n

def fwd(lon, lat):
    """lon/lat (deg, arrays ok) -> raw x, y (y down), as d3 does it"""
    l = np.radians((np.asarray(lon, np.float64) + ROT + 180) % 360 - 180); p = np.radians(np.asarray(lat, np.float64))
    p = np.clip(p, -math.pi / 2 + 1e-6, math.pi / 2 - 1e-6)
    r = _F / _f(p) ** _n
    return r * np.sin(_n * l), -(_F - r * np.cos(_n * l))

def inv(x, y):
    """raw x, y (y down) -> lon/lat (deg)"""
    x = np.asarray(x, np.float64); fy = _F + np.asarray(y, np.float64)   # F - (-y)
    r = np.sign(_n) * np.sqrt(x * x + fy * fy)
    l = np.arctan2(x, np.abs(fy)) * np.sign(fy)
    lat = 2 * np.arctan((_F / r) ** (1 / _n)) - math.pi / 2
    return np.degrees(l / _n) - ROT, np.degrees(lat)

def box_raw(b, steps=60):
    """raw bounding box of a lon/lat box (its edges are curves in the projection)"""
    a, c, e, d = b; t = np.linspace(0, 1, steps)
    lon = np.concatenate([a + (e - a) * t, a + (e - a) * t, np.full(steps, a), np.full(steps, e)])
    lat = np.concatenate([np.full(steps, c), np.full(steps, d), c + (d - c) * t, c + (d - c) * t])
    x, y = fwd(lon, lat); return x.min(), y.min(), x.max(), y.max()

def tiles(n):
    """the tiles of level n: a set of (i, j)"""
    S = S0 / 2 ** n; out = set()
    for b in LEVELS[n][1]:
        x0, y0, x1, y1 = box_raw(b)
        for i in range(math.floor((x0 - X0) / S), math.floor((x1 - X0) / S) + 1):
            for j in range(math.floor((y0 - Y0) / S), math.floor((y1 - Y0) / S) + 1): out.add((i, j))
    return out

def tile_lonlat(n, i, j, pad=0):
    """lon/lat of every pixel centre of tile (n, i, j) incl. the 1-px bleed and an extra pad (for blur context)"""
    S = S0 / 2 ** n; px = S / P; m = 1 + pad; N = P + 2 * m
    xs = X0 + i * S + (np.arange(N) - m + .5) * px; ys = Y0 + j * S + (np.arange(N) - m + .5) * px
    X, Y = np.meshgrid(xs, ys); return inv(X, Y)

if __name__ == '__main__':
    tot = 0
    for n in LEVELS: k = len(tiles(n)); tot += k; print('level', n, 'tiles', k, 'px/deg ~', round(P * 2 ** n / S0 / 57.2958))
    print('total', tot)
