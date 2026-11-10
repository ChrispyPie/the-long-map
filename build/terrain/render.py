"""The relief look shared by render_tiles.py: Gaussian blur, hillshade, colour ramps (warm parchment hypsometric tint
for land, soft blues for sea depth). DEM: Terrain Tiles on AWS Open Data (Terrarium encoding; SRTM, GMTED2010,
ETOPO1 etc.), see build/terrain/README.md."""
import json, math, os, sys
import numpy as np
ROOT = os.path.dirname(os.path.abspath(__file__)) + '/../..'
WORK = os.environ.get('TLM_TERRAIN_WORK', '/workspace/tlm-terrain/work')

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
