# Chapter 9 plan — 167 BC, The Maccabees

Unmerged branch `feat/chapter9-167`, worktree `/workspace/tlm-ch9`, started 21 Nov 2026 (Europe/Stockholm) after Chapter 8 went live (PR #47, `92da4c2`). Backup of main at the start: `backup/pre-ch9-20261121`. This file is a start, not a shippable chapter: no narration module, no audio, no tests yet. Do not hook it into `make_data.py` or `story_jews.py` until a full script exists.

## How it should ship
Same pattern as Chapter 8. The live coming-soon teaser already points at **167 BC, The Maccabees**. Keep that year. Events run from the Hellenistic succession after Alexander, through Antiochus IV, the crisis of 167, the revolt, the rededication (usually 164), and the early Hasmoneans — not a second 164 chapter. Next coming-soon after Ch9 should be **63 BC, Rome arrives**. 516 stays a title-only year.

- Intro last line exactly: `That is the world of this chapter. Now the story begins.`
- Play last line ends: `That is where our next chapter begins.` (`play.to = -63`)
- Quick: `pick()` from Play, last line = Play’s last line, `pauseAfter` 2000, `steps_map` if a border lives on an unpicked line
- Recap: new `CH8` block (no digits), `RECAPS[167] = recap(8)`, keep under the 200 s cap
- Labels: attested / disputed / tradition / scene; a source for every claim; `source_info` popups; `ref=` only with the bible source
- Era map = end of Ch8 Play (Yehud, a small Persian province, Second Temple). Play must then show the Hellenistic / Seleucid world and, later, Judaea under the revolt
- Tests: `test-chapter9.js`; extend test-chapterend / test-quick / test-recap / test-part2entry to 9 chapters; Ch8 Stay → Ch9 chooser; Ch9 Stay → 63 coming soon

## Story to tell (fairness first)
1. After Persia, Alexander takes the empire (332–323). Judaea passes, without a battle of its own that we can pin down here, into the world of the Successors.
2. Ptolemaic then Seleucid rule over the land; a Hellenistic city culture around it (places: Jerusalem, Samaria/Sebaste later, coastal cities, Antioch, Alexandria, Modein).
3. Onias, Jason, Menelaus — high-priesthood bought and sold in Greek sources and in 2 Maccabees (tradition / disputed detail).
4. Antiochus IV (attested on coins and in Greek historians). The crisis of 167: 1–2 Maccabees and Josephus describe a ban on Jewish law, a “desolating sacrilege” on the altar, and an altar to Zeus Olympios. How much is royal policy, how much a civil conflict inside Jerusalem, is disputed in modern scholarship (Bickerman, Tcherikover, Hengel, Schwartz, Honigman).
5. Revolt beginning at Modein; Judah Maccabee; guerrilla war in the hills; rededication of the Temple, usually dated 164 (Hanukkah) — the year and the later festival memory should be labelled carefully (biblical / traditional calendar vs attested Seleucid chronology).
6. The fight continues after 164: alliance language with Rome in 1 Maccabees (treat as tradition unless a supporting inscription is used carefully); death of Judah; Jonathan and Simon; the rise of a Hasmonean state.
7. Close on the threshold of Rome (63 BC), not a full Pompey chapter.

## Sources to add (verify before citing; do not invent)
Likely keys: `bible` (already; 1–2 Maccabees, Daniel), `josephusant`, `polybius`, `livy` or existing Greek historians, `antiochuscoins` / hoard catalogues, `1macc`/`2macc` if you split them, `bickerman1979` (or the exact edition you use), `tcherikover1959`, `hengel1974`, `schwartz2008` (2 Maccabees), `honigman2014`, maybe a Seleucid chronology handbook. Every new key needs a real publication and a `source_info` popup. Do not invent DOIs.

## Terrain / places
Jerusalem, Modein, Beth-zur, Beth-zechariah, Adasa, Antioch, Alexandria, the coastal cities, Samaria. Most of these sit inside existing L4 relief except perhaps some Syrian sites already covered by PR #41. No new pyramid required to start.

## Opener close and session notes
Intro must end on the locked sentence above. Play length target ~10–13 minutes, Quick ~2.5 minutes / under the 345-word cap. Fetch/merge `origin/main` before any PR (the other executor ships small PRs from `/workspace/tlm-fix`). Never print or commit `ELEVENLABS_API_KEY`.
