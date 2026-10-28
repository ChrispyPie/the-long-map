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

Tests: `node build/test-vignettes.js URL` and `node build/test-vignettes-all.js URL` (every vignette, phone and desktop).
