# How the map data is made (not loaded by the site)

- `data/base.topo.json`: Natural Earth (public domain), https://github.com/nvkelso/natural-earth-vector
  - Land: ne_10m_land clipped to 16,11,64,46 and simplified 25 %, plus ne_50m_land outside that box (simplified 40 %).
  - Lakes: ne_10m_lakes, only natural lakes (Dead Sea, Sea of Galilee, Van, Urmia, Tuz, Sevan, Hammar, Beyşehir, Eğirdir, Tana, Aral). Modern dam lakes left out.
  - Rivers: ne_10m_rivers_lake_centerlines (Nile, Euphrates, Tigris, Jordan, Karkheh, Halys and others). Canals left out.
  - Orontes is NOT in Natural Earth 10m. It is drawn by hand through modern towns (Hermel, Homs, Hama, Jisr al-Shughur, Antakya), marked `src:"approx"` and shown dashed.
  - Tool: mapshaper (`-clip`, `-simplify`, `-o format=topojson quantization=30000`).
- `data/stops/1207bc.json`: zone outlines from `build/zones-1207.py`, clipped to land with mapshaper. Outlines are approximate and based on the sources listed in the file.
- `js/d3-lite.min.js`: d3-geo, d3-zoom, d3-selection, d3-transition and topojson-client (ISC licence), bundled from `build/d3lite.js` with esbuild.
