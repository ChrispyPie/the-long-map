# Sound effects

Generated on 27 October 2026 with the ElevenLabs Sound Effects API
(`POST /v1/sound-generation`, model `eleven_text_to_sound_v2`, `prompt_influence` 0.45,
output `mp3_44100_64`). The API key is read from the environment only and is not stored in this repo.

Afterwards each clip was made mono at 48 kbit/s with ffmpeg. Effects were loudness-normalised to about -18 LUFS
(with a short fade-in); the two ambient loops were set to about -26 to -29 LUFS. The ambient clips were generated with `loop: true`
so they repeat without a seam.

| File | Length | Size | Credits (character-cost) | Prompt |
|---|---|---|---|---|
| `battle.mp3` | 10 s | 60 KB | 110 | Ancient Bronze Age battle in the distance: bronze swords clashing on wooden and leather shields, spears striking, men shouting far away, chariot wheels on dry earth. No music, no modern sounds, no gunfire. |
| `migration.mp3` | 12 s | 72 KB | 132 | A slow ancient caravan crossing dry land: many footsteps on dirt and gravel, a soft dry wind, sheep and goats bleating, wooden ox carts creaking, a donkey now and then. Calm, distant. No music, no modern sounds. |
| `border.mp3` | 4 s | 24 KB | 44 | A single low, soft frame drum hit with a gentle airy whoosh, subtle and calm, fading out. No music melody, no modern effects. |
| `year.mp3` | 3 s | 18 KB | 33 | A single old parchment page being turned slowly, soft and dry, close up, quiet room. |
| `amb-desert.mp3` | 15 s (loop) | 90 KB | 165 | Calm desert wind ambience, soft dry air moving over sand and rocks, very gentle and even, no birds, no voices, no music. |
| `amb-river.mp3` | 15 s (loop) | 90 KB | 165 | Gentle river water flowing slowly past reeds, calm and even, faint wind, no voices, no music, no modern sounds. |

Credits used: **649** in total, from the `character-cost` header of each request. The account's
`character_count` went from 880 to 1199 right after the run; that counter may update later.

## How they are used (js/app.js)

- **Defaults:** battle steps play `battle`, migration steps play `migration`, border changes play `border`, and year changes play `year` (a soft page turn).
  A step can set `"sfx"` to another clip name, or to `null` for none.
- **Ambient:** each scene has an ambient loop (`play.ambient`, or a beat's `"ambient"`): `desert` by default, and `river` at the Nile.
- **Levels:** while a line is narrated, all sound sits about 18 dB down. In the pause after the line it rises to about -6 dB over about 1.4 s, then ducks back when the next line starts.
- **`sfxHold` (ms, at most 4000):** on a battle, migration or border step, this stretches the pause so the sound can play out. The pause is capped at 2 s, so only a few scenes get a longer breath.
  It runs on the same clock as the rest of the film, so it follows the speed setting, and Skip cuts it. It applies only while sound is on.
- **When audio starts:** nothing loads or plays until a user gesture (BEGIN ADVENTURE, Play or the sound button).
  The sound button next to CC is remembered (`tlm.snd`). With reduced motion, sound is off by default.
- **Pausing:** pausing the film suspends the audio.
