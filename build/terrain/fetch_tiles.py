"""Download Terrarium elevation tiles (AWS Open Data 'Terrain Tiles', mostly SRTM/GMTED/ETOPO1 - open, attribution).
Usage: python3 build/terrain/fetch_tiles.py  -> cache in $TLM_TERRAIN_CACHE (default /workspace/tlm-terrain/cache)"""
import math, os, sys, urllib.request
from concurrent.futures import ThreadPoolExecutor
CACHE = os.environ.get('TLM_TERRAIN_CACHE', '/workspace/tlm-terrain/cache')
URL = 'https://s3.amazonaws.com/elevation-tiles-prod/terrarium/{z}/{x}/{y}.png'
# name: (zoom, lon0, lat0, lon1, lat1)
AREAS = {'region': (7, 2, 8, 76, 56), 'levant': (10, 32.6, 28.2, 38.8, 35.2)}
def tx(lon, z): return int((lon + 180) / 360 * 2**z)
def ty(lat, z): r = math.radians(lat); return int((1 - math.log(math.tan(r) + 1 / math.cos(r)) / math.pi) / 2 * 2**z)
def get(job):
    z, x, y = job; p = f'{CACHE}/{z}/{x}/{y}.png'
    if os.path.exists(p): return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    for _ in range(3):
        try: urllib.request.urlretrieve(URL.format(z=z, x=x, y=y), p); return
        except Exception as e: err = e
    print('fail', job, err, file=sys.stderr)
jobs = []
for z, a, b, c, d in AREAS.values():
    jobs += [(z, x, y) for x in range(tx(a, z), tx(c, z) + 1) for y in range(ty(d, z), ty(b, z) + 1)]
print(len(jobs), 'tiles')
with ThreadPoolExecutor(16) as ex: list(ex.map(get, jobs))
