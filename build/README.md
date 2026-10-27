# How the map data is made (not loaded by the site)

- `data/base.topo.json`: Natural Earth (public domain), https://github.com/nvkelso/natural-earth-vector
  - Land: ne_10m_land clipped to 16,11,64,46 and simplified 25 %, plus ne_50m_land outside that box (simplified 40 %).
  - Lakes: ne_10m_lakes, only natural lakes (Dead Sea, Sea of Galilee, Van, Urmia, Tuz, Sevan, Hammar, Beyşehir, Eğirdir, Tana, Aral). Modern dam lakes left out.
  - Rivers: ne_10m_rivers_lake_centerlines (Nile, Euphrates, Tigris, Jordan, Karkheh, Halys and others). Canals left out.
  - Orontes is NOT in Natural Earth 10m. It is drawn by hand through modern towns (Hermel, Homs, Hama, Jisr al-Shughur, Antakya), marked `src:"approx"` and shown dashed.
  - Tool: mapshaper (`-clip`, `-simplify`, `-o format=topojson quantization=30000`).
- `data/eras/1207bc.json` (was `data/stops/1207bc.json`): zone outlines from `build/zones-1207.py`, clipped to land with mapshaper. Outlines are approximate and based on the sources listed in the file. `make_data.py` adds `zoneObjects` (zone → fact box) and label positions.
- `js/d3-lite.min.js`: d3-geo, d3-zoom, d3-selection, d3-transition and topojson-client (ISC licence), bundled from `build/d3lite.js` with esbuild.

## Fact boxes and stories (`build/make_data.py`)

Run from the repo root: `python3 build/make_data.py`. It checks that every source key, label and object id exists, then writes:

- `data/sources.json`: shared source registry, from `build/sources.py`. Each entry has kind, full reference, link and how it was checked.
- `data/objects/near-east.json`: shared map objects (the small fact boxes: cities, sites, rivers, lakes, seas, regions, routes, states, peoples), from `build/objects.py`. Any story can reuse them.
- `data/eras/1207bc.json`: shared zones for the year (see above).
- `data/stories/jews/story.json` and `data/stories/jews/1207bc.json`: the story "History of the Jews" (intro, stops, the big event boxes and transitions), from `build/story_jews.py`.

A new perspective gets its own `build/story_<id>.py` and `data/stories/<id>/`, and reuses the shared objects, eras and sources.

Each claim is `[text, label, [source keys]]`. The label is `attested`, `disputed` or `tradition`.

### Story guidelines

- **The fairness test:** would a thoughtful member of this people recognise and accept the telling?
- Write with respect and warmth, from the people's own experience and self-understanding.
- Include the people's own tradition and memory where it is relevant, labelled Tradition and told with respect ("In Jewish tradition …", "The Hebrew Bible tells …"). Never call it "myth" or "fabricated".
- Show scholarly debate neutrally as Disputed, without sneering. Use no loaded or hostile words about any people.
- Never state an unsourced claim as fact. Give uncertain numbers as ranges, labelled Disputed, with a source.

## Test

`build/test-fakta.js` uses Playwright and headless Chromium. It tests 393 px with touch and 1280 px: stepping through the events, opening every object, tap outside, X, chips, and console errors. Run it with `node build/test-fakta.js http://127.0.0.1:8793/ noshots` against a local `python3 -m http.server 8793`. Playwright must be installed.
