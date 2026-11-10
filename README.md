# The Long Map

People moving through time. The map is the stage. The story is the product.

First chapter: about 1207 BC, from Greece to Persia. Israel is a people in the hills, named on Merneptah's stone, not a kingdom yet.

Domain, once pointed here: thelongmap.com

## Sound

The film has quiet sound effects: Bronze Age battle, a caravan on the move, a soft drum when a border changes, a page turn when the year changes, and desert-wind and river ambient loops.
They were made with the ElevenLabs Sound Effects API. The prompts and credits are in `assets/sfx/README.md`.

- Sound starts only after a tap (Begin adventure or Play).
- It sits low under the narration and rises a little in the pauses.
- The speaker button next to CC turns it on or off, and the choice is remembered.
- With reduced motion, sound is off by default.

## Vignettes

Small pictures that come in beside the map while the film plays, one for most narration lines in chapters 1–3 that show something you can see. Lines that are scholarly debate, dates or framing have none. They are listed in `build/vignettes.py` and copied into `data/stories/jews/*.json` by `python3 build/make_data.py`; don't edit the JSON by hand.

- Illustrations (`images/vignettes/*.webp`, sepia ink and watercolour, under 150 KB each) are the main thing. A caption says "(impression)" when a scene is reconstructed.
- `fx` adds a light CSS overlay (smoke, fire, waves, birds, dust, clouds) on the illustration only. It is turned off with reduced motion.
- `images: [a, b]` shows two pictures side by side at one height, never stacked. Tap one to enlarge it with its own caption.
- Real photos are used sparingly, toned sepia and framed like a museum plate (`photo: True`, no movement):
  - Merneptah Stele: photo by Onceinawhile, CC BY-SA 4.0, Wikimedia Commons.
  - Tel Dan Stele: "Aramaic Inscription on Basalt Monument, Dan, 9th Century BC" by Gary Todd, CC0, Wikimedia Commons.
  - Siloam inscription: photo by Oncenawhile, CC0, Wikimedia Commons (File:Siloam_inscription.jpg).
  - Lachish reliefs, British Museum (Assyrian archers): photo by Mike Peel (www.mikepeel.net), CC BY-SA 4.0, Wikimedia Commons (File:Lachish_Relief,_British_Museum_14.jpg). Also used, uncropped, in the Chapter 6 fact box "The siege of Lachish" (images/lachish-relief.webp).

Tests: `node build/test-vignettes.js URL` and `node build/test-vignettes-all.js URL` (every vignette, phone and desktop).

## World map

The map is built to grow with the story (Europe, North Africa, the Middle East, Central Asia, later the Americas)
without making the first visit heavier.

- `data/world.json`: the projection (conic conformal, parallels 30/40, rotated to 38°E), the home view, how far one
  can pan and zoom out (`bounds`, lon -20..95, lat -2..66), and the regions.
- Regions: `near-east` (`data/base.topo.json`, the coast/lakes/rivers the stories use) loads with the page; `world`
  (`data/world/outer.topo.json`, 83 KB, Natural Earth 50m outside the Near East box, made by `build/world/build.sh`)
  loads only when the view leaves the Near East, or when a stop names it (`"regions": ["world"]` in story.json).
  Each region draws its own coast line without the straight cuts where its data was clipped.
- Shaded relief: a tile pyramid in the same projection (`build/terrain/README.md`). Coarse levels cover the whole
  world map, deep levels only where the story is told (down to ~40 m per pixel over Judah), loaded tile by tile for
  what is on screen. A new region gets detail by adding its box to `build/terrain/pyramid.py` and re-rendering.
- The Americas need their own projection (and relief grid); the plan is a second map "world" in `world.json` that a
  stop switches to, not stretching this one.

Tests: `node build/test-terrain.js URL`, `node build/test-world.js URL`.
