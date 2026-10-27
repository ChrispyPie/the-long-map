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
- `data/stories/jews/story.json` and `data/stories/jews/1207bc.json`: the story "Story of the Jews" (Book One) (intro, stops, the big event boxes and transitions), from `build/story_jews.py`.

A new perspective gets its own `build/story_<id>.py` and `data/stories/<id>/`, and reuses the shared objects, eras and sources.

Each claim is `[text, label, [source keys]]`. The label is `attested`, `disputed` or `tradition`.

### Story guidelines

- **The fairness test:** would a thoughtful member of this people recognise and accept the telling?
- Write with respect and warmth, from the people's own experience and self-understanding.
- Include the people's own tradition and memory where it is relevant, labelled Tradition and told with respect ("In Jewish tradition …", "The Hebrew Bible tells …"). Never call it "myth" or "fabricated".
- Show scholarly debate neutrally as Disputed, without sneering. Use no loaded or hostile words about any people.
- Never state an unsourced claim as fact. Give uncertain numbers as ranges, labelled Disputed, with a source.

## Explore progress (`STOP["explore"]`)

- `explore.key`: the curated key objects for a stop (ids from `objects.py`). They get a soft ring until opened, then a check.
- Progress is kept on the device in `localStorage` under `tlm.explored.<story>.<year>`. "Reset progress" clears it.
- Flow per year: intro box → free exploration (the "X/12 explored" pill opens the checklist) → Play.

## Play / transitions (`STOP["play"]`)

`play = {to, title, intro, zoneObjects, beats:[...]}`. Beats run one after another. Each beat has one `caption` step plus optional steps:

| step | fields | what it does |
|---|---|---|
| `caption` | `text`, `cert` (`attested`/`disputed`/`tradition`/`scene`), `src` | subtitle with badge and sources |
| `year` | `to` | the year counter tweens to this year |
| `focus` | `c` [lon,lat], `k` zoom, `hl` ids | camera move + highlights |
| `migration` | `path`, `label`, `cert` | animated arrow; dashed and "Disputed" when `cert` is disputed |
| `battle` | `at`, `label`, `cert`, `arrows:[{path, side: egypt/enemy, cert}]` | army arrows, then a pulsing marker |
| `border` | `fade:[{zone, certainty?}]`, `add:[{zone, certainty, label, labelAt, coords}]` | crossfade of zones |

Optional on a beat: `audio` (path to an mp3), `duration`, `pauseAfter`, `ambient` (`desert` or `river`, inherited by later beats; default `play.ambient`). Optional on a step: `duration` (ms); on battle, migration and border steps also `sfx` (clip name, or null for none) and `sfxHold` (ms, at most 4000).

### Pacing rules

1. The narration line drives timing. `make_data.py` writes `duration` = reading time (about 2.5 words per second, at least 2000 ms; used when the voice is off) and `pauseAfter` into every beat unless they are set by hand: 600 ms after a line, 1500 ms on the last beat before a new chapter (allowed range 400–2000). With `audio`, the beat waits for the audio to end, then the pause.
2. One main visual event at a time: the camera moves first (`focus`, 1600 ms), then each `migration` (3200 ms), `battle` (3000 ms) and `border` (3000 ms) runs on its own, one after another, with slow easing. The next beat starts only after max(line, visuals) + `pauseAfter`.
3. Sound (see `assets/sfx/README.md`): effects and the ambient loop sit about 18 dB down while a line is narrated, rise to about -6 dB in the pause, and duck again when the next line starts. With sound on, a step's `sfxHold` stretches the pause so the sound can play out, but no pause is longer than 2 s (`BREATH_MAX` in `js/app.js`). It runs on the same virtual clock, so it follows the speed setting, and Skip cuts it.
3. The controls are always shown: back one step, pause/play, forward one step, and speed 0.75× / 1× / 1.25×. Tapping the map pauses. All timing runs on one clock, so pause and speed affect everything.
4. At the end the map stays on the new year's intro. It does not continue by itself.
5. Captions must work without audio (narrator off, or a line not recorded yet). Long films are split into chapters of about 2–3 minutes (see Narration); the build prints the word count and the voiced length.

### Scene-setting captions

`cert: "scene"` (badge "Imagine") is for atmosphere only. The text must start with "Imagine", carry no sources, and assert no new facts. The build checks this. Scene lines are left out of the "What changed" recap. Any factual detail (houses, jars, cisterns, diet, trade) goes in a normal sourced caption.

## Site settings (`data/site.json`)

`donateUrl`: `null` hides the "Support this project" link in the footer. Set it to a full `https://` link to show it. No donation service has been chosen.

`reportUrl`: same idea for a "Report an error" link (a form or an issue tracker). `null` hides it. None is chosen yet.

## About notice and the opening book (`js/intro.js`)

On the first visit a short notice says what the site is (a source-based retelling of Jewish history from the perspective of the Jewish people; every claim has a source and a label; maps and borders are approximate) and what it is not (a religious text, political advocacy about modern conflicts, or the final word). **Begin adventure** opens a book: the leather cover ("The Long Map" / "Book One" / "Story of the Jews") turns and the page grows into the map. CSS only, no images or libraries.

- The choice is stored in `localStorage` as `tlm.notice.v1 = "seen"`; returning visitors go straight to the map. "About" in the header and "About this site" in the footer open the notice again.
- With `prefers-reduced-motion: reduce` there is no book; the notice simply closes.

## Cinematic mode (Play)

When a narrated part runs (Play, Replay), the map viewport grows from its place in the page to the whole screen, like a small film, and shrinks back when the part ends.

- Uses the Fullscreen API where it exists (requested on the Play click). iPhone Safari has no element fullscreen, so the same thing is done with a fixed full-viewport layer. Leaving browser fullscreen, Esc or × ends the film.
- Menus, the story panel, the timeline, the legend and the progress pill fade out. Subtle letterbox bars, the year at the top, subtitles at the bottom. Each subtitle keeps its label badge and a small source line.
- Floating controls: back, pause/play, forward, speed (0.75/1/1.25), **CC** (subtitles on/off, stored as `tlm.cc`), step count, Skip, × (exit). They hide after 3 s without input while playing and come back on any touch, mouse move or key. A tap on the picture shows them **and pauses**; objects are not opened mid-film. Keys: Space pause, ←/→ step, Esc exit.
- All pacing rules above are unchanged; the film only changes the frame. At the end the view zooms back out to the page and lands on the new year's intro (c. 1150 BC), with menus, texts and clickable objects back.
- With `prefers-reduced-motion: reduce` the grow/shrink and fades are instant.
- Both narrated films use it: the opening film of a year (`transitionIn.beats`) and Play. A **narrator** button (person with sound waves) next to the sound button switches the voice on or off (`tlm.voice`, default on, also with reduced motion); it is separate from the effects. With the voice off the subtitles keep their reading time.

## Narration (`build/narration_jews_1207.py`, `build/narrate.py`)

The script lives in `build/narration_jews_1207.py`, one recorded line per beat. `story_jews.py` takes its beats for `transitionIn.beats` (the opening film) and `play.beats`.

- **Labels.** As for fact boxes (`attested`, `disputed`, `tradition`, `scene`), plus `frame` for the film's own framing lines (the title, how to read the labels, the choice). Frame lines are allowed only in the opening film, carry no sources or facts, and show no badge or source line.
- **Written for the ear.** The spoken `text` has no digits and no brackets (the build refuses them). The subtitle can show digits through an optional `display` ("about 1207 BC" is read as "twelve hundred and seven BC"). Bible lines give the verse in `ref`, shown after the sources ("Sources: Hebrew Bible · Exodus 22:21 (22:20 in the Hebrew numbering)"): English verse numbering, Hebrew numbering in brackets where it differs.
- **Opening film and choice.** `transitionIn` stays backwards-compatible: a plain string, or `{text, ambient, beats}` where `text` is the fallback shown in the intro panel. The opener (chapter 1, about 75–90 s) ends on the one beat with `"choice": true`: the film waits, and the viewer picks **Continue the story** (chapter 2 onwards) or **Explore the map**. The intro panel offers "Watch the opening", "Explore the map" and "read it as fact boxes".
- **Chapters.** A beat with `"chapter": "Title"` opens a chapter; the first beat of each film must have one. Aim for 2–3 minutes per chapter. In the film a chapter card shows "Chapter N of M" and a strip of chapter segments above the controls jumps between chapters. The intro and Explore panels list the chapters with their length.
- **Resume.** The film stores the chapter in progress per stop and film (`tlm.resume.<story>.<year>.<intro|play>`) and the panels offer "Resume at chapter N". It is cleared when the film plays to its end or is skipped.
- **Playback.** In the film a tap or click on the picture never pauses or plays; it only shows the hidden controls (or keeps them up). Play and pause only with the button in the control bar, or Space. A narrator clip that fails, stalls for 2.5 s or is stopped by the phone is retried once and then skipped; the film goes on with the subtitles on the beat timer and never pauses by itself (`build/test-playback.js`).
- **Timing.** With the voice on a beat lasts as long as its recording (`audioMs`), then a short pause (`pauseAfter`, or `sfxHold` with sound on, at most 2 s); effects duck about 18 dB under the voice. Speed changes the voice's `playbackRate` and the virtual clock together.

**Recording.** `ELEVENLABS_API_KEY=… python3 build/narrate.py` records every line whose text changed (voice Grant Gravitas `VC6vCXhVaI8BZefRtXZV`, `eleven_multilingual_v2`, narrator settings at speed 1.0, mono 22.05 kHz 32 kbps), with request stitching (`previous_request_ids`, `next_text`) so the lines sound continuous. Files: `assets/narration/<reel>-NN.mp3` and `assets/narration/index.json` (`{file: {ms, sha}}`, `sha` = first 12 hex of the SHA-1 of the spoken text). The key is read from the environment only and is never written anywhere. `make_data.py` attaches `audio` and `audioMs` to each beat and refuses a line whose text no longer matches its recording; `TLM_ALLOW_SILENT=1` builds anyway, without the voice for those lines.

## Test

`build/test-fakta.js` uses Playwright and headless Chromium. It tests 393 px with touch and 1280 px: stepping through the events, opening every object, tap outside, X, chips, and console errors. It presets the About notice as seen. `build/test-cine.js` tests the notice, the book, cinematic mode, CC, auto-hide, tap-to-pause, the zoom-out and the reduced-motion path at 393 px (touch) and 1280 px. `build/test-sfx.js` tests the sound effects and `build/test-narration.js` the narration (recordings, opener length, the choice, chapters and the strip, resume, the narrator button, `display`, frame lines, Bible refs). Run each with `node build/test-<name>.js http://127.0.0.1:8793/ noshots` against a local `python3 -m http.server 8793`. Playwright must be installed.

## Design and series

*The Long Map* is a series. Each book tells history from the perspective of one people, on the same map and with the same rules for sources. This site is **Book One: Story of the Jews**. Book Two (Story of the Arabs) and the Story of the Persians are shown only as "coming later"; nothing about them is written yet. The series framing appears in the notice, on the book cover and in the footer.

The look is an old book: worn brown leather for the cover, header, frames and buttons (CSS gradients, a tiny inline SVG noise for grain and mottling, dashed "stitching"), and yellowed paper with torn edges for every text panel (class `paper`: grain, faint stains and an SVG `#torn` displacement filter on a `::before` layer, so text itself is never distorted). Browsers that ignore the filter show straight paper edges. No image files or libraries. Text is ink on paper, AA contrast or better; reduced motion turns off the book animation, pulses and rings.

Each book brings its own accent colours in `story.json` under `"theme"` (keys `accent`, `accent-ink`, `accent-soft`, `accent-map`, `accent-foil`, hex only); `js/app.js` sets them as CSS variables. The base palette deliberately belongs to no people or side (no flag colours, no dominant green).

`build/shots-design.js` takes the `design2_` screenshots (notice, cover, explore, fact box, film; mobile 393 px and desktop).
