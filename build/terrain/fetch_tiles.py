"""Download the Terrarium elevation tiles (AWS Open Data 'Terrain Tiles': SRTM, GMTED2010, ETOPO1 and others;
open, attribution) that the relief pyramid needs (build/terrain/pyramid.py: each level samples one DEM zoom).
Usage: python3 build/terrain/fetch_tiles.py [levels...]  -> cache in $TLM_TERRAIN_CACHE (default /workspace/tlm-terrain/cache)"""
import math, os, sys, urllib.request
import numpy as np
from concurrent.futures import ThreadPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pyramid as PY
CACHE = os.environ.get('TLM_TERRAIN_CACHE', '/workspace/tlm-terrain/cache')
URL = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
def need(n, pad=40):
    """every DEM tile in the lon/lat bounding rectangle of each relief tile (that is what render_tiles.mosaic reads)"""
    z = PY.LEVELS[n][0]; out = set()
    for i, j in PY.tiles(n):
        lon, lat = PY.tile_lonlat(n, i, j, pad)
        X = (lon + 180) / 360 * 2**z * 256; r = np.radians(np.clip(lat, -85, 85))
        Y = (1 - np.log(np.tan(r) + 1 / np.cos(r)) / np.pi) / 2 * 2**z * 256
        for x in range(int(X.min() // 256), int(X.max() // 256) + 1):
            for y in range(int(Y.min() // 256), int(Y.max() // 256) + 1): out.add((z, x % 2**z, min(max(y, 0), 2**z - 1)))
    return out
def get(job):
    z, x, y = job; p = f'{CACHE}/{z}/{x}/{y}.png'
    if os.path.exists(p) and os.path.getsize(p) > 0: return 0
    os.makedirs(os.path.dirname(p), exist_ok=True)
    for _ in range(4):
        try: urllib.request.urlretrieve(URL.format(z=z, x=x, y=y), p + '.part'); os.replace(p + '.part', p); return 1
        except Exception as e: err = e
    print('fail', job, err, file=sys.stderr); return 0
if __name__ == '__main__':
    lv = [int(a) for a in sys.argv[1:]] or list(PY.LEVELS)
    jobs = sorted(set().union(*[need(n) for n in lv]))
    print(len(jobs), 'DEM tiles needed', flush=True)
    with ThreadPoolExecutor(16) as ex: got = sum(ex.map(get, jobs))
    print('downloaded', got)
