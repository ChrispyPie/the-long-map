# Shaded relief: tile pyramid

Pre-baked relief tiles in the map's own projection (conic conformal 30/40, rotate -38), drawn as SVG `<image>`s in
`g.reliefs` at the bottom of `gLand`; coast, lakes, rivers, zones, labels and all animations stay vector on top.
The relief shows on every chapter and over the whole map. `?terrain=0` turns it off.

## Grid (build/terrain/pyramid.py, mirrored in data/terrain.json "grid")
Raw units = the projection at scale 1 / translate 0 (y down). Level n has square tiles of S = S0 / 2^n raw units
(S0 = 1), origin X0 = Y0 = -2; tile (n, i, j) covers x in [X0 + i·S, X0 + (i+1)·S]. Each tile is a 512-px WebP
rendered with a 1-px bleed (514 px) so neighbours overlap and no seam shows.

| level | DEM zoom | covers | ~px/deg |
|---|---|---|---|
| 0–2 | 4–6 | the whole world map, lon -20..95, lat -2..66 | 9–36 |
| 3 | 7 | Near East, lon 2..76, lat 8..56 | 71 |
| 4 | 8 | Nile delta, Levant, Mesopotamia | 143 |
| 5 | 9 | Egypt to the Euphrates | 286 |
| 6 | 10 | the Levant | 572 |
| 7 | 11 | Israel / Judah, Philistia, Transjordan | 1144 |
| 8 | 12 | the hill country: Samaria to Hebron, Lachish, the Dead Sea | 2288 |

To give a new region (e.g. Europe or Central Asia for a later book) detail, add its lon/lat box to the levels it
needs in `pyramid.py` and re-run the three steps below; the site picks the tiles up from the manifest.

## Site (js/app.js: reliefTiles / updateRelief)
On every zoom or pan (once per animation frame) the view's box in raw units decides the level the screen needs
(`ceil(log2(projScale · zoom · devicePixelRatio · 0.8 / P))`); the deepest level ≤ that which covers the whole view
is the floor, and the tiles of the floor up to the needed level that exist are drawn, coarse under fine. Tiles that
leave stay underneath until the new ones have loaded. So the first load is a handful of small tiles
(~20–160 KB depending on the chapter's view), and detail is fetched only where and when it is looked at.

## Build

    MAPSHAPER=node_modules/.bin/mapshaper build/world/build.sh   # outer land (coast mask outside the Near East)
    python3 build/terrain/fetch_tiles.py      # DEM tiles -> /workspace/tlm-terrain/cache (~330 MB, not in repo)
    node build/terrain/rings.js               # land rings in raw units -> /workspace/tlm-terrain/work/rings_raw.json
    python3 build/terrain/render_tiles.py     # -> images/terrain/<n>/<i>_<j>.webp + data/terrain.json (~1 min, 8 cores)

Look (render.py): warm parchment hypsometric tint, multi-scale hillshade (fine + broad + a soft north light),
soft sea depth (from at most DEM z7, smooth offshore). Coast mask: data/base.topo.json land (the coast the map
draws) plus Natural Earth 50m outside the Near East box, 2× supersampled.

DEM: "Terrain Tiles" on AWS Open Data (Terrarium encoding), a composite of SRTM (public domain, NASA/USGS),
GMTED2010 (USGS, public domain), ETOPO1 (NOAA, public domain) and others. Attribution on the site:
"Shaded relief: elevation from Terrain Tiles on AWS Open Data (SRTM, GMTED2010, ETOPO1; public domain)".
For a pure-public-domain chain, swap the source for SRTM 3" / Copernicus GLO-90 (free licence, attribution) — same pipeline.
