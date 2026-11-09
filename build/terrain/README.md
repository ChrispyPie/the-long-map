# Shaded relief (prototype, branch feat/terrain-proto)

Pre-baked relief images in the map's own projection (conic conformal 30/40, rotate -38), drawn as SVG `<image>`
at the bottom of `gLand`; coast, lakes, rivers, zones, labels and all animations stay vector on top.
`data/terrain.json` gives each image's box in the projection at scale 1 / translate 0, so `placeRelief()` maps it
onto the live projection with one scale + offset. `?terrain=0` turns it off.

    python3 build/terrain/fetch_tiles.py      # DEM tiles -> /workspace/tlm-terrain/cache (~60 MB, not in repo)
    node build/terrain/grid.js                # pixel lon/lat grids + Natural Earth land rings -> /workspace/tlm-terrain/work
    python3 build/terrain/render.py           # -> images/terrain/*.webp + data/terrain.json

Layers: `region` (3000 px wide, Terrarium z7, ~1.2 km/px source) and `levant` (2400 px, z10, ~150 m/px source),
feathered so the detail melts into the region image.

DEM: "Terrain Tiles" on AWS Open Data (Terrarium encoding), a composite of SRTM (public domain, NASA/USGS),
GMTED2010 (USGS, public domain), ETOPO1 (NOAA, public domain) and others. Attribution on the site:
"Relief: Terrain Tiles (AWS Open Data; SRTM, GMTED2010, ETOPO1) · Natural Earth".
For a pure-public-domain chain, swap the source for SRTM 3" / Copernicus GLO-90 (free licence, attribution) — same pipeline.
