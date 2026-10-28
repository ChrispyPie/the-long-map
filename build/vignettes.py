"""Vignettes: small illustrated cards that pop up over the map while the narrator describes something.

Each entry ties one picture to one narrated line. make_data.py finds the beat whose line starts with
"line" (it must match exactly one beat in that stop's reel) and writes beat["vignette"] = {src, alt, caption?, beats?}.
The film (js/app.js) shows the card when that beat starts, next to the place in focus, and fades it out when a
later beat moves the camera, brings its own vignette, or after "beats" lines (default 3), whichever comes first.

To add one for a new chapter: put a ~640px WebP in images/vignettes/ (warm sepia ink-and-watercolor on parchment,
no text, no modern things, no faces of named people) and add a line below. caption is optional (shown small under
the picture); alt is read by screen readers.
"""

D = "images/vignettes/"

VIGNETTES = {
    # story-stop prefix (as in the narration file names) -> reel ("intro" = transitionIn, "play") -> list
    "jews-1207": {
        "intro": [
            {"line": "Imagine those hills in the evening", "src": D + "c1-hills-evening.webp",
             "alt": "Evening in the hill country: a few small flat-roofed stone houses among rock and scrub, smoke rising from a cooking fire",
             "caption": "Hill country, evening (artist's impression)"},
            {"line": "Egypt lived by its river", "src": D + "c1-nile-flood.webp",
             "alt": "The Nile in flood spreading over fields, palms and a village on higher ground",
             "caption": "The Nile flood (artist's impression)"},
            {"line": "We know Israel's name because of a stone", "src": D + "c1-stele.webp",
             "alt": "A tall carved granite slab with a rounded top, covered in rows of carved signs",
             "caption": "A victory stele like Merneptah's (impression, not the real text)"},
        ],
        "play": [
            {"line": "On the Syrian coast stood Ugarit", "src": D + "c1-ugarit-port.webp",
             "alt": "A walled port town on a bay with merchant ships at anchor and a scribe with clay tablets",
             "caption": "Ugarit, a trading port (artist's impression)"},
            {"line": "Then he fought them at sea", "src": D + "c1-sea-battle.webp",
             "alt": "Ships locked together in battle near a river mouth while archers shoot from the shore",
             "caption": "After the temple reliefs at Medinet Habu (impression)"},
            {"line": "They brought their own ways", "src": D + "c1-philistine-crafts.webp",
             "alt": "Painted Aegean-style pottery, an open hearth and a loom hung with spool-shaped weights",
             "caption": "Aegean-style pottery, hearth and spool loom weights"},
            {"line": "Most villages were small", "src": D + "c1-village-ring.webp",
             "alt": "A small village seen from above: a ring of houses around an open yard",
             "caption": "A ring of houses around a yard, like Izbet Sartah (impression)"},
            {"line": "A typical home was a pillared house", "src": D + "c1-pillared-house.webp",
             "alt": "Cutaway drawing of a stone house with a row of pillars and rooms around a central space",
             "caption": "A pillared house (artist's impression)"},
            {"line": "Families stored grain in pits", "src": D + "c1-jars-cistern.webp",
             "alt": "Large storage jars with collared necks beside a cistern cut into the rock",
             "caption": "Collared-rim jars and a rock-cut cistern"},
            {"line": "On steeper slopes, terraces held the soil", "src": D + "c1-terraces.webp",
             "alt": "Stone terrace walls stepping down a hillside, holding small fields",
             "caption": "Hillside terraces (artist's impression)"},
            {"line": "Bread was the staple food", "src": D + "c1-grinding.webp",
             "alt": "A stone grinding slab and hand stone with grain and flour, a bowl and loaves nearby",
             "caption": "Grinding grain into flour"},
            {"line": "On a hilltop in the north of these hills", "src": D + "c1-bronze-bull.webp",
             "alt": "A small bronze figurine of a bull on a hilltop, with a standing stone behind it",
             "caption": "The bronze bull figurine (setting is an impression)"},
        ],
    },
    "jews-1150": {
        "play": [
            {"line": "Excavations at Ashkelon, Ashdod, Ekron and Gath", "src": D + "c2-philistine-city.webp",
             "alt": "Bird's-eye view of a walled city laid out in regular blocks",
             "caption": "A planned Philistine city (idealised impression)"},
            {"line": "Over time their pottery changed", "src": D + "c2-bichrome.webp",
             "alt": "Pottery painted in red and black bands, spirals and birds",
             "caption": "Bichrome ware"},
            {"line": "Further north, at Tell Qasile", "src": D + "c2-qasile-temple.webp",
             "alt": "Inside a small temple: two wooden pillars, benches along the walls and a raised platform",
             "caption": "The temple at Tell Qasile (artist's impression)"},
            {"line": "Imagine the harbour towns in those years", "src": D + "c2-harbour.webp",
             "alt": "A harbour town: a potter at the wheel, fishing boats on the sand and a busy market",
             "caption": "A harbour town (artist's impression)"},
            {"line": "An Egyptian tale shows how far its fame had fallen", "src": D + "c2-byblos-cedar.webp",
             "alt": "Cedar logs stacked on the shore of a harbour, a ship waiting offshore",
             "caption": "Cedar at Byblos (artist's impression)"},
            {"line": "Excavations at Shiloh found a settlement", "src": D + "c2-shiloh-storeroom.webp",
             "alt": "A storeroom with stone pillars and rows of large jars",
             "caption": "A storeroom full of jars (artist's impression)"},
            {"line": "Imagine the news reaching a hill village", "src": D + "c2-runner.webp",
             "alt": "A small figure running along a hill path towards a village where people gather",
             "caption": "News reaches a village (artist's impression)"},
            {"line": "The Bible's David is a hero with flaws", "src": D + "c2-elah-valley.webp",
             "alt": "A broad valley between low hills, with a dry streambed and scattered trees",
             "caption": "The Valley of Elah (landscape impression)"},
            {"line": "Archaeology has added new evidence", "src": D + "c2-qeiyafa.webp",
             "alt": "A hilltop town ringed by a double stone wall with gates, above a valley",
             "caption": "Khirbet Qeiyafa (stylised impression)"},
            {"line": "Among its finds were a pottery sherd", "src": D + "c2-ostracon.webp",
             "alt": "A broken pottery sherd with faint lines of ink writing",
             "caption": "An inscribed sherd (impression, not the real text)"},
            {"line": "The first mention of David outside the Bible", "src": D + "c2-dan-stele.webp",
             "alt": "A basalt victory stone with carved lines standing at a city gate",
             "caption": "A victory stone at Dan (impression; it was found broken)"},
            {"line": "Imagine the gate at Qeiyafa at dawn", "src": D + "c2-qeiyafa-dawn.webp",
             "alt": "A stone town gate at dawn, sentries on the wall looking over the valley, smoke from houses",
             "caption": "The gate at dawn (artist's impression)"},
        ],
    },
}
