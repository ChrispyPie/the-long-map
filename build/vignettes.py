"""Vignettes: small illustrated cards that pop up over the map while the narrator describes something.

Each entry ties one picture to one narrated line. make_data.py finds the beat whose line starts with
"line" (it must match exactly one beat in that stop's reel) and writes beat["vignette"] = {src, alt, caption?, beats?, fx?, photo?}.
The film (js/app.js) shows the card when that beat starts, next to the place in focus, and fades it out when a
later beat moves the camera, brings its own vignette, or after "beats" lines (default 3), whichever comes first.

To add one: put a ~640px WebP (< 150 KB) in images/vignettes/ (warm sepia ink-and-watercolor on parchment,
no text, no modern things, no faces of named people) and add a line below. caption is optional (shown small under
the picture, wraps to 2 lines; keep it short); alt is read by screen readers.

Illustrations are the main thing. Real photos only very sparingly, for iconic finds, toned sepia and framed like a
museum plate so they sit in the same paper style (see README "Vignettes"); always credit them in the caption.

Optional keys:
  fx     "smoke" | "fire" | "waves" | "birds" | "dust" | "clouds", or a list of them: a subtle code-drawn animation
         layered on an illustration (never on photos; off under prefers-reduced-motion).
  photo  True for a real photograph (no Ken Burns drift, no fx).
  images [{src, alt, caption?, fx?, photo?}, {...}] instead of src/alt: two pictures side by side in one card
         (always side by side, scaled down to fit; each can be tapped to enlarge). The top-level caption names the pair.
"""

D = "images/vignettes/"
def _q(line, name): return {"line": line, "_name": name}

VIGNETTES = {
    # story-stop prefix (as in the narration file names) -> reel ("intro" = transitionIn, "play") -> list
    "jews-1207": {
        "intro": [
            {"line": "The year is about twelve hundred and seven BC", "src": D + "c1-egypt-temple.webp", "alt": "An Egyptian temple gateway with flagpoles, an obelisk and an avenue of sphinxes", "caption": "Egypt under Merneptah (impression)"},
            {"line": "North-east of Egypt, along a desert road", "src": D + "c1-ways-of-horus.webp", "alt": "A mud-brick fort with a water pool beside a desert road, donkeys passing", "caption": "A fort on the Ways of Horus", "fx": "dust"},
            {"line": "And in the hills of Canaan lived a people", "src": D + "c1-hill-village.webp", "alt": "A cluster of small stone houses and round pits on a wooded hilltop", "caption": "Hill country (impression)"},
            {"line": "Imagine those hills in the evening", "src": D + "c1-hills-evening.webp", "alt": "Evening in the hill country: a few small flat-roofed stone houses among rock and scrub, smoke rising from a cooking fire", "caption": "Hill country, evening (artist's impression)", "fx": "smoke"},
            {"line": "Egypt lived by its river", "src": D + "c1-nile-flood.webp", "alt": "The Nile in flood spreading over fields, palms and a village on higher ground", "caption": "The Nile flood (artist's impression)", "fx": "waves"},
            {"line": "Egyptian soldiers kept watch at Gaza", "src": D + "c1-egyptian-garrison.webp", "alt": "Egyptian soldiers with spears and a bow on a fort wall above a valley", "caption": "An Egyptian garrison (impression)"},
            {"line": "The Canaanites had long been at home here", "src": D + "c1-clay-letters.webp", "alt": "Clay tablets covered in wedge-shaped writing, a stylus and an oil lamp", "caption": "Clay letters to Pharaoh"},
            {"line": "Their gods were old gods of the land", "src": D + "c1-storm-god.webp", "alt": "A bronze figure of a striding god with a raised arm on a stone base, storm clouds behind", "caption": "Baal, the storm god (impression)", "fx": "clouds"},
            {"line": "Far to the north, the Hittites ruled from Hattusa", "src": D + "c1-hattusa-gate.webp", "alt": "A pointed stone gateway flanked by carved lions in a massive city wall", "caption": "Hattusa's Lion Gate (impression)"},
            {"line": "To the east, beyond the Euphrates, Assyria", "src": D + "c1-assur.webp", "alt": "A walled city with a stepped temple tower on a bluff above a river with boats", "caption": "Assur on the Tigris (impression)"},
            {"line": "We know Israel's name because of a stone", "src": D + "c1-merneptah-plate.webp", "photo": True, "alt": "Photograph of the Merneptah Stele in a museum: a tall dark granite slab with a rounded top, carved figures and rows of hieroglyphs", "caption": "The real Merneptah Stele · photo Onceinawhile, CC BY-SA 4.0"},
            {"line": "The stone was not new", "src": D + "c1-stele.webp", "alt": "A tall carved granite slab with a rounded top, covered in rows of carved signs", "caption": "A reused stele (impression)"},
            {"line": "Most of the hymn praises his victory over the Libyans", "src": D + "c1-libyan-war.webp", "alt": "Egyptian chariots with archers chasing warriors across a desert plain", "caption": "War with the Libyans (impression)", "fx": "dust"},
            {"line": "On a wall at Karnak, battle scenes", "src": D + "c1-karnak-relief.webp", "alt": "A carved temple relief of a king in a chariot before a walled town", "caption": "A Karnak battle relief (impression)"},
            {"line": "In Jewish tradition, the name is older still", "src": D + "c1-jacob-wrestling.webp", "alt": "Two figures wrestling at a river ford in a valley at dusk", "caption": "Jacob wrestles (impression)"},
            {"line": "The Torah tells how they went down to Egypt", "src": D + "c1-sinai.webp", "alt": "Tents camped below a rugged mountain wrapped in cloud", "caption": "At Sinai (impression)", "fx": "clouds"},
            {"line": "For Jews, it is the founding memory", "src": D + "c1-passover.webp", "alt": "A table with flat unleavened bread, a cup of wine, bitter herbs and a lamp", "caption": "Passover (impression)", "fx": "fire"},
        ],
        "play": [
            {"line": "In the years after Merneptah's stone", "src": D + "c1-palace-ruins.webp", "alt": "A collapsed palace with fallen beams, broken walls and spilled jars", "caption": "A fallen palace (impression)", "fx": "smoke"},
            {"line": "It had no single cause", "src": D + "c1-drought.webp", "alt": "Cracked dry ground, a thin cow and a man at a well, a village behind", "caption": "Drought (impression)", "fx": "dust"},
            {"line": "Even before the worst came, there was hunger", "src": D + "c1-grain-ship.webp", "alt": "Men carrying sacks and jars aboard a sailing ship at a riverbank", "caption": "Grain by ship (impression)", "fx": "waves"},
            {"line": "On the Syrian coast stood Ugarit", "src": D + "c1-ugarit-port.webp", "alt": "A walled port town on a bay with merchant ships at anchor and a scribe with clay tablets", "caption": "Ugarit, a trading port (artist's impression)", "fx": ["waves", "birds"]},
            {"line": "A letter from the king of Ugarit", "src": D + "c1-ugarit-letter.webp", "alt": "A hand writing on a clay tablet with a stylus, a ship seen through the window", "caption": "A letter on clay (impression)"},
            {"line": "Around eleven ninety BC, Ugarit was destroyed", "src": D + "c1-ugarit-burns.webp", "alt": "A coastal city burning, with ships offshore", "caption": "Ugarit burns (impression)", "fx": ["smoke", "fire"]},
            {"line": "Far inland, the Hittite court left", "src": D + "c1-hattusa-leaving.webp", "alt": "A line of ox-carts and people on foot leaving a walled hill city", "caption": "Leaving Hattusa (impression)", "fx": "dust"},
            {"line": "A branch of the royal family held on", "src": D + "c1-carchemish.webp", "alt": "A fortified city on a mound beside a wide river, a boat in front", "caption": "Carchemish (impression)"},
            {"line": "In Egypt, Ramesses the Third had these words", "src": D + "c1-medinet-habu.webp", "alt": "A great Egyptian temple gateway covered in carved scenes", "caption": "Medinet Habu (impression)"},
            {"line": "The same temple walls show people on the move", "src": D + "c1-ox-carts.webp", "alt": "Ox-drawn carts with women and children on a coastal road", "caption": "Families on the move (impression)", "fx": "dust"},
            {"line": "Modern historians call them the Sea Peoples", "src": D + "c1-sea-peoples.webp", "alt": "Ships with bird-head prows sailing toward a coast, gulls overhead", "caption": "The Sea Peoples (impression)", "fx": ["waves", "birds"]},
            {"line": "In his eighth year", "src": D + "c1-land-battle.webp", "alt": "Egyptian chariots and archers charging into warriors on a plain", "caption": "The land battle (impression)", "fx": "dust"},
            {"line": "Then he fought them at sea", "src": D + "c1-sea-battle.webp", "alt": "Ships locked together in battle near a river mouth while archers shoot from the shore", "caption": "After the temple reliefs at Medinet Habu (impression)", "fx": "waves"},
            {"line": "Among the enemies, the inscriptions name the Peleset", "src": D + "c1-peleset.webp", "alt": "A row of warriors with feathered headdresses, round shields and spears", "caption": "The Peleset (after the reliefs)"},
            {"line": "A later papyrus says", "src": D + "c1-papyrus.webp", "alt": "A papyrus scroll, a scribe's palette, a reed pen and an oil lamp", "caption": "A royal papyrus (impression)"},
            {"line": "On the southern coast of Canaan, newcomers", "src": D + "c1-ashkelon.webp", "alt": "A walled town on the shore, boats pulled up on the beach", "caption": "Ashkelon (impression)", "fx": "waves"},
            {"line": "They brought their own ways", "src": D + "c1-philistine-crafts.webp", "alt": "Painted Aegean-style pottery, an open hearth and a loom hung with spool-shaped weights", "caption": "Aegean-style pottery, hearth and spool loom weights"},
            {"line": "They also ate a good deal of pork", "src": D + "c1-pigs.webp", "alt": "A woman scattering food for pigs beside a clay oven", "caption": "Pigs in the yard (impression)"},
            {"line": "Imagine the coast in those years", "src": D + "c1-coast-market.webp", "alt": "A seaside market with fish, pots and a loom, ships offshore and gulls", "caption": "The coast (impression)", "fx": ["waves", "birds"]},
            {"line": "Egypt held on in Canaan", "src": D + "c1-beth-shean.webp", "alt": "A fort on a high mound above a green valley with palms", "caption": "Beth-Shean (impression)"},
            {"line": "Where they came from is debated too", "src": D + "c1-herders-settle.webp", "alt": "Herders' tents beside a sheep pen and new stone houses on a hillside", "caption": "Herders settling (impression)"},
            {"line": "Imagine the hills at dawn", "src": D + "c1-hills-dawn.webp", "alt": "Misty hills at dawn, a shepherd on a path below a village", "caption": "Hills at dawn (impression)", "fx": ["smoke", "birds"]},
            {"line": "Most villages were small", "src": D + "c1-village-ring.webp", "alt": "A small village seen from above: a ring of houses around an open yard", "caption": "A ring of houses around a yard, like Izbet Sartah (impression)"},
            {"line": "A typical home was a pillared house", "src": D + "c1-pillared-house.webp", "alt": "Cutaway drawing of a stone house with a row of pillars and rooms around a central space", "caption": "A pillared house (artist's impression)"},
            {"line": "Animals and stores were probably kept", "src": D + "c1-four-room-house.webp", "alt": "Cutaway of a two-storey house: animals and jars below, a family asleep above", "caption": "Animals below? (impression)"},
            {"line": "Families stored grain in pits", "src": D + "c1-jars-cistern.webp", "alt": "Large storage jars with collared necks beside a cistern cut into the rock", "caption": "Collared-rim jars and a rock-cut cistern"},
            {"line": "On steeper slopes, terraces held the soil", "src": D + "c1-terraces.webp", "alt": "Stone terrace walls stepping down a hillside, holding small fields", "caption": "Hillside terraces (artist's impression)"},
            {"line": "They grew wheat and barley", "src": D + "c1-farming.webp", "alt": "Farmers ploughing with oxen and reaping grain among olive trees", "caption": "Farming the hills (impression)"},
            {"line": "Bread was the staple food", "src": D + "c1-grinding.webp", "alt": "A stone grinding slab and hand stone with grain and flour, a bowl and loaves nearby", "caption": "Grinding grain into flour"},
            {"line": "The Torah would later praise this land", "src": D + "c1-seven-species.webp", "alt": "Wheat, barley, grapes, figs, pomegranates, olives and dates", "caption": "The seven species"},
            {"line": "At Izbet Sartah, someone scratched an alphabet", "src": D + "c1-abecedary.webp", "alt": "A broken potsherd scratched with rows of letters", "caption": "An alphabet sherd (impression)"},
            {"line": "On a hilltop in the north of these hills", "src": D + "c1-bronze-bull.webp", "alt": "A small bronze figurine of a bull on a hilltop, with a standing stone behind it", "caption": "The bronze bull figurine (setting is an impression)"},
            {"line": "An Egyptian list from more than a century earlier", "src": D + "c1-shasu.webp", "alt": "A line of nomads with donkeys and goats crossing dry hills", "caption": "Shasu nomads (impression)", "fx": "dust"},
            {"line": "Down on the coast and along the trade roads", "src": D + "c1-copper-trade.webp", "alt": "Ox-hide shaped copper ingots unloaded from a ship, donkeys waiting", "caption": "The copper trade (impression)", "fx": "waves"},
            {"line": "Imagine a winter evening", "src": D + "c1-winter-evening.webp", "alt": "A family around a fire inside a stone house at night, goats resting nearby", "caption": "A winter evening (impression)", "fx": "fire"},
            {"line": "In Jewish tradition, this is the age of the Judges", "src": D + "c1-judges-palm.webp", "alt": "A woman seated under a palm tree in the hills, people walking toward her", "caption": "Deborah's palm (impression)"},
        ],
        # Quick version (about two minutes): the same pictures as the full film, one per main line
        "quick": [
            _q("About twelve hundred and seven BC", "c1-hattusa-gate.webp"),
            _q("Between them lay Canaan", "c1-egyptian-garrison.webp"),
            _q("Pharaoh Merneptah carved a victory hymn", "c1-merneptah-plate.webp"),
            _q("In Jewish tradition, the story begins earlier", "c1-sinai.webp"),
            _q("Then the old world of palaces began to fall", "c1-palace-ruins.webp"),
            _q("The port of Ugarit was destroyed", "c1-ugarit-burns.webp"),
            _q("Egyptian temple walls show peoples on the move", "c1-ox-carts.webp"),
            _q("Around eleven seventy-seven BC", "c1-sea-battle.webp"),
            _q("Among them were the Philistines", "c1-ashkelon.webp"),
            _q("During the twelfth century", "c1-beth-shean.webp"),
            _q("In the hills, small farming villages spread", "c1-village-ring.webp"),
            _q("Many archaeologists see these villagers", "c1-pillared-house.webp"),
            _q("In Jewish tradition, this is the age of the Judges, when", "c1-judges-palm.webp"),
            _q("For now, this is a people of villages", "c1-hills-evening.webp"),
        ],
    },
    "jews-1150": {
        "intro": [
            {"line": "It is about eleven hundred and fifty", "src": D + "c2-empty-fort.webp", "alt": "An empty mud-brick fort with round towers and an open gate", "caption": "An empty Egyptian fort (impression)", "fx": "dust"},
            {"line": "On the southern coast, the Philistines are building", "src": D + "c2-philistine-building.webp", "alt": "Workers laying stone foundations and moulding bricks near the sea", "caption": "Building on the coast (impression)", "fx": "birds"},
            {"line": "In the hill country, small farming villages keep spreading", "src": D + "c2-villages-spread.webp", "alt": "Wooded hills with thin columns of smoke rising from scattered villages", "caption": "Villages spread (impression)", "fx": "smoke"},
        ],
        "play": [
            {"line": "The Bible speaks of five Philistine lords", "src": D + "c2-gaza.webp", "alt": "A walled town on a coastal hill above palms and the sea", "caption": "Gaza (impression)", "fx": "waves"},
            {"line": "Excavations at Ashkelon, Ashdod, Ekron and Gath", "src": D + "c2-philistine-city.webp", "alt": "Bird's-eye view of a walled city laid out in regular blocks", "caption": "A planned Philistine city (idealised impression)"},
            {"line": "Over time their pottery changed", "src": D + "c2-bichrome.webp", "alt": "Pottery painted in red and black bands, spirals and birds", "caption": "Bichrome ware"},
            {"line": "Further north, at Tell Qasile", "src": D + "c2-qasile-temple.webp", "alt": "Inside a small temple: two wooden pillars, benches along the walls and a raised platform", "caption": "The temple at Tell Qasile (artist's impression)"},
            {"line": "Imagine the harbour towns in those years", "src": D + "c2-harbour.webp", "alt": "A harbour town: a potter at the wheel, fishing boats on the sand and a busy market", "caption": "A harbour town (artist's impression)", "fx": "waves"},
            {"line": "Egypt's own strength kept fading", "src": D + "c2-thebes-priests.webp", "alt": "Priests in white carrying a sacred boat shrine between temple columns, incense smoke", "caption": "Priests at Thebes (impression)", "fx": "smoke"},
            {"line": "An Egyptian tale shows how far its fame had fallen", "src": D + "c2-byblos-cedar.webp", "alt": "Cedar logs stacked on the shore of a harbour, a ship waiting offshore", "caption": "Cedar at Byblos (artist's impression)", "fx": "waves"},
            {"line": "Far to the east, the Assyrian king", "src": D + "c2-assyrian-army.webp", "alt": "An army with chariots marching past a burning town by a river", "caption": "An Assyrian army (impression)", "fx": ["smoke", "dust"]},
            {"line": "The Book of Judges tells of leaders", "src": D + "c2-gideon.webp", "alt": "At night, men on a hill blow ram's horns and hold up torches above a camp", "caption": "Gideon's torches (impression)", "fx": "fire"},
            {"line": "One place stands out in the tradition", "src": D + "c2-shiloh.webp", "alt": "A tent sanctuary inside a fenced court on a hill, smoke rising from an altar", "caption": "Shiloh (impression)", "fx": "smoke"},
            {"line": "Here a woman named Hannah", "src": D + "c2-hannah.webp", "alt": "A woman in a head-cloth praying silently beside a tent curtain", "caption": "Hannah prays (impression)"},
            {"line": "Excavations at Shiloh found a settlement", "src": D + "c2-shiloh-storeroom.webp", "alt": "A storeroom with stone pillars and rows of large jars", "caption": "A storeroom full of jars (artist's impression)"},
            {"line": "Radiocarbon dates from charred grain", "src": D + "c2-charred-grain.webp", "alt": "Burnt grain spilled from broken jars below a scorched stone wall", "caption": "Charred grain (impression)"},
            {"line": "The Bible tells how Israel lost a battle", "src": D + "c2-ark-taken.webp", "alt": "Warriors carrying off a chest on poles across a battlefield", "caption": "The Ark is taken (impression)", "fx": "dust"},
            {"line": "The Bible never describes Shiloh's fall", "src": D + "c2-shiloh-ruins.webp", "alt": "Tumbled stone walls overgrown on a hill, a lone olive tree", "caption": "Shiloh in ruins (impression)", "fx": "birds"},
            {"line": "Imagine the news reaching a hill village", "src": D + "c2-runner.webp", "alt": "A small figure running along a hill path towards a village where people gather", "caption": "News reaches a village (artist's impression)"},
            {"line": "In the story, Samuel now leads the people", "src": D + "c2-elders.webp", "alt": "Bearded elders in robes speaking to an old man on a village path", "caption": "The elders ask (impression)"},
            {"line": "Samuel warns them", "src": D + "c2-kings-way.webp", "alt": "A chariot with officers, men hauling loads, people working the fields", "caption": "The way of a king (impression)", "fx": "dust"},
            {"line": "So Samuel anoints Saul", "src": D + "c2-anointing.webp", "alt": "An old man pouring oil from a horn over a young man's head at sunset", "caption": "Saul is anointed (impression)"},
            {"line": "Where Gibeah lay is debated", "src": D + "c2-gibeah.webp", "alt": "A hill with a small stone tower above terraced slopes", "caption": "Gibeah (impression)", "fx": "clouds"},
            {"line": "The Bible describes a troubled reign", "src": D + "c2-lyre.webp", "alt": "A brooding man seated by a hearth while a young man plays a lyre", "caption": "David plays for Saul (impression)", "fx": "fire"},
            {"line": "The music came from a young shepherd", "src": D + "c2-shepherd.webp", "alt": "A young shepherd with a staff sitting above grazing sheep, birds overhead", "caption": "A shepherd boy (impression)", "fx": "birds"},
            {"line": "David's own family story", "src": D + "c2-ruth.webp", "alt": "Women gathering sheaves of barley in a harvest field", "caption": "Ruth gleans (impression)"},
            {"line": "Saul's end came in battle on Mount Gilboa", "src": D + "c2-gilboa.webp", "alt": "A dusty battle on a mountain slope, a fallen shield, vultures circling", "caption": "Mount Gilboa (impression)", "fx": ["dust", "birds"]},
            {"line": "The Bible's David is a hero with flaws", "src": D + "c2-elah-valley.webp", "alt": "A broad valley between low hills, with a dry streambed and scattered trees", "caption": "The Valley of Elah (landscape impression)"},
            {"line": "After Saul's death, he is made king at Hebron", "src": D + "c2-hebron.webp", "alt": "A crowd gathering below a hill town among vineyards", "caption": "Hebron (impression)"},
            {"line": "Archaeology has added new evidence", "src": D + "c2-qeiyafa.webp", "alt": "A hilltop town ringed by a double stone wall with gates, above a valley", "caption": "Khirbet Qeiyafa (stylised impression)"},
            {"line": "Among its finds were a pottery sherd", "src": D + "c2-ostracon.webp", "alt": "A broken pottery sherd with faint lines of ink writing", "caption": "An inscribed sherd (impression, not the real text)"},
            {"line": "At Gath, a sherd from about this time", "src": D + "c2-gath-sherd.webp", "alt": "A broken sherd with two scratched words lying in the dirt", "caption": "Gath sherd (not the real text)"},
            {"line": "The first mention of David outside the Bible", "caption": "The Tel Dan Stele", "images": [{"src": D + "c2-dan-stele.webp", "alt": "A basalt victory stone with carved lines standing at a city gate", "caption": "A victory stone at Dan (impression; it was found broken)"}, {"src": D + "c2-dan-stele-plate.webp", "alt": "Sepia photograph of the real Tel Dan Stele: broken basalt fragments with Aramaic letters, in a museum", "caption": "Real fragments · photo Gary Todd, CC0", "photo": True}]},
            {"line": "Imagine the gate at Qeiyafa at dawn", "src": D + "c2-qeiyafa-dawn.webp", "alt": "A stone town gate at dawn, sentries on the wall looking over the valley, smoke from houses", "caption": "The gate at dawn (artist's impression)", "fx": "smoke"},
        ],
        "quick": [
            _q("It is about eleven hundred and fifty BC", "c2-empty-fort.webp"),
            _q("On the southern coast, the Philistines build up", "c2-philistine-city.webp"),
            _q("Without an empire, small peoples", "c2-villages-spread.webp"),
            _q("The Book of Judges tells of leaders", "c2-gideon.webp"),
            _q("At Shiloh, the Bible says", "c2-shiloh.webp"),
            _q("Excavations there found storerooms", "c2-shiloh-storeroom.webp"),
            _q("The Bible tells how the Philistines defeated Israel", "c2-ark-taken.webp"),
            _q("Then the people asked for a king", "c2-anointing.webp"),
            _q("Saul and his son Jonathan fell", "c2-gilboa.webp"),
            _q("David, a shepherd from Bethlehem", "c2-hebron.webp"),
            _q("Above the Valley of Elah", "c2-qeiyafa.webp"),
            _q("More than a century later, a victory stone", "c2-dan-stele.webp"),
            _q("In Jewish tradition, David's name", "c2-qeiyafa-dawn.webp"),
        ],
    },
    "jews-1000": {
        "intro": [
            {"line": "On the coast, the Philistine cities are still strong", "src": D + "c3-tyre.webp", "alt": "An island city with walls and ships with horse-head prows, gulls over the waves", "caption": "Tyre, island city (impression)", "fx": ["waves", "birds"]},
            {"line": "East of the Jordan live Ammon, Moab and Edom", "src": D + "c3-transjordan.webp", "alt": "High plateau land east of the Jordan with a town and flocks", "caption": "East of the Jordan (impression)", "fx": "clouds"},
        ],
        "play": [
            {"line": "The Bible says Jerusalem belonged to the Jebusites", "src": D + "c3-water-shaft.webp", "alt": "Men with an oil lamp climbing a dark rock-cut water shaft", "caption": "A water shaft (impression)", "fx": "fire"},
            {"line": "Jerusalem lay on the border", "src": D + "c3-jerusalem-ridge.webp", "alt": "A small walled town on a narrow ridge between deep valleys", "caption": "Jerusalem's ridge (impression)", "fx": "clouds"},
            {"line": "Then David brings up the Ark", "src": D + "c3-ark-procession.webp", "alt": "A procession with drums and lyres carrying a chest on poles up a hill path", "caption": "The Ark comes up (impression)", "fx": "dust"},
            {"line": "On the slope of the City of David", "src": D + "c3-stepped-structure.webp", "alt": "A huge stepped stone wall climbing a hill slope below houses", "caption": "Stepped Stone Structure (impr.)"},
            {"line": "Jewish tradition gives David the Book of Psalms", "src": D + "c3-psalms.webp", "alt": "Musicians with lyres and a drum singing at dusk", "caption": "Songs at dusk (impression)"},
            {"line": "Imagine Jerusalem on that day", "src": D + "c3-festival.webp", "alt": "A crowded hill town with banners, people celebrating on its slopes", "caption": "A day of celebration (impression)"},
            {"line": "The Second Book of Samuel lists David's wars", "src": D + "c3-wars.webp", "alt": "Lines of warriors marching through dusty hills", "caption": "David's wars (impression)", "fx": "dust"},
            {"line": "In the story, the siege of Rabbah", "src": D + "c3-rabbah.webp", "alt": "An army camped below a walled hilltop city, smoke rising", "caption": "The siege of Rabbah (impression)", "fx": "smoke"},
            {"line": "He takes Bathsheba", "src": D + "c3-ewe-lamb.webp", "alt": "A poor man holding a lamb in his arms at the door of a small house", "caption": "The poor man's lamb (parable)"},
            {"line": "South of the Dead Sea", "src": D + "c3-copper.webp", "alt": "Workers at small smelting furnaces in a desert valley, smoke and slag heaps", "caption": "Copper smelting (impression)", "fx": ["smoke", "fire"]},
            {"line": "Many scholars think the people who ran it", "src": D + "c3-edom-tents.webp", "alt": "A large black tent with donkeys in a rocky desert valley", "caption": "Living in tents (impression)", "fx": "dust"},
            {"line": "Far to the north, in Tyre", "src": D + "c3-cedars.webp", "alt": "Woodcutters felling huge cedars on a misty mountain, others hauling a log with ropes", "caption": "Cedars of Lebanon (impression)", "fx": "clouds"},
            {"line": "Bathsheba and Nathan go to the old king", "src": D + "c3-gihon.webp", "alt": "A crowd with a young man on a mule at a spring below a town, a horn blown", "caption": "At the Gihon spring (impression)"},
            {"line": "At Gibeon, the story says", "src": D + "c3-dream.webp", "alt": "A man asleep on a mat beside a stone altar under a starry sky", "caption": "Solomon's dream (impression)", "fx": "fire"},
            {"line": "Then comes the famous judgement", "src": D + "c3-judgement.webp", "alt": "A king on a wooden throne, two women before him, a guard with a sword and a woman holding a baby", "caption": "Solomon's judgement (impression)"},
            {"line": "In the fourth year of his reign", "src": D + "c3-temple-begins.webp", "alt": "Builders laying dressed stones for a large building, dust in the air", "caption": "The temple begun (impression)", "fx": "dust"},
            {"line": "Hiram of Tyre sends cedar", "src": D + "c3-rafts.webp", "alt": "Rafts of cedar logs poled along a rocky coast, towed by a sailing ship", "caption": "Cedar rafts (impression)", "fx": ["waves", "birds"]},
            {"line": "The temple has three parts", "src": D + "c3-temple-plan.webp", "alt": "Cutaway of a long temple: a porch with two bronze pillars, a great hall and a dark inner room; a basin and an altar in front", "caption": "Three-part temple (impression)", "fx": "smoke"},
            {"line": "But temples with the same three-part plan", "src": D + "c3-ain-dara.webp", "alt": "A ruined stone temple platform lined with carved lions and sphinxes, giant footprints on its threshold", "caption": "Ain Dara temple (impression)"},
            {"line": "And at Tel Motza", "src": D + "c3-motza.webp", "alt": "A small stone temple with a courtyard altar and pottery on a bench, terraced hills behind", "caption": "Tel Motza temple (impression)"},
            {"line": "At Khirbet Qeiyafa, a small stone model", "src": D + "c3-shrine-model.webp", "alt": "A small stone model of a shrine with a doorway of three recessed frames, in excavated earth", "caption": "Qeiyafa shrine model (impr.)"},
            {"line": "At the dedication, Solomon prays", "src": D + "c3-dedication.webp", "alt": "A figure with arms raised in prayer on a platform before a crowd, smoke from an altar", "caption": "The dedication (impression)", "fx": "smoke"},
            {"line": "Imagine the cedar beams arriving", "src": D + "c3-beams.webp", "alt": "Carriers shouldering cedar beams up a stone ramp to a rising building with scaffolding", "caption": "Cedar beams arrive (impression)", "fx": "dust"},
            {"line": "In the nineteen fifties, Yigael Yadin", "src": D + "c3-gate.webp", "alt": "Bird's-eye view of a city gate with three chambers on each side of the passage", "caption": "A six-chamber gate (impression)"},
            {"line": "Gezer gave us something else", "src": D + "c3-gezer.webp", "alt": "A small limestone tablet with lines of scratched letters beside a sickle, barley, grapes and an olive branch", "caption": "Gezer calendar (impression)"},
            {"line": "Egypt's kings of this time ruled from Tanis", "src": D + "c3-tanis.webp", "alt": "A silver coffin with a human face inside a stone sarcophagus in a lamp-lit tomb, a gold mask and jars beside it", "caption": "A royal tomb at Tanis (impression)", "fx": "fire"},
            {"line": "The Bible tells of ships, too", "src": D + "c3-ships.webp", "alt": "Two sailing ships with oars off a desert shore below red mountains, men loading jars", "caption": "Ships at Ezion-geber (impression)", "fx": "waves"},
            {"line": "Then comes the queen of Sheba", "src": D + "c3-sheba.webp", "alt": "A camel caravan crossing the desert, a woman riding under a fringed canopy", "caption": "The queen of Sheba (impression)", "fx": "dust"},
            {"line": "The Bible does not hide the cost", "src": D + "c3-labour.webp", "alt": "Labourers dragging a great stone block on a sledge up a hill, an overseer watching", "caption": "Forced labour (impression)", "fx": "dust"},
            {"line": "Then Solomon dies", "src": D + "c3-shechem.webp", "alt": "A crowd gathered in a valley between two hills, facing a young man on a rock", "caption": "The assembly at Shechem (impr.)"},
            {"line": "Jeroboam sets up golden calves", "src": D + "c3-dan.webp", "alt": "A raised stone platform among trees by a spring, a horned altar with smoke and a small golden calf", "caption": "A shrine at Dan (impression)", "fx": "smoke"},
            {"line": "Then, in the fifth year of king Rehoboam", "src": D + "c3-shoshenq.webp", "alt": "An Egyptian army with chariots, standards, archers and shield-bearers marching through hills", "caption": "Shishak's army (impression)", "fx": "dust"},
            {"line": "And this time, Egypt tells its own side", "src": D + "c3-karnak.webp", "alt": "A carved temple wall: a giant pharaoh smiting captives beside rows of name-rings topped by bound captives", "caption": "Shoshenq's list, Karnak (impression)"},
        ],
    },
    "jews-930": {
        "intro": [
            {"line": "At Megiddo itself, a broken piece of stone", "src": D + "c4-megiddo-fragment.webp", "alt": "A broken block of carved Egyptian stone with hieroglyphs and a royal name-ring in an excavation trench, a basket and a pick beside it", "caption": "A Shoshenq fragment (impression)"},
            {"line": "On the map, two kingdoms", "src": D + "c4-two-kingdoms.webp", "alt": "Terraced hills with olive trees and two walled hilltop towns on distant ridges, a road winding between them", "caption": "Two kingdoms in the hills (impr.)", "fx": "clouds"},
        ],
        "play": [
            {"line": "Baasha of Israel fortifies Ramah", "src": D + "c4-ramah.webp", "alt": "Workers carrying stones and timber to build a thick wall on a wooded hilltop", "caption": "Fortifying Ramah (impression)", "fx": "dust"},
            {"line": "Asa of Judah sends the silver and gold", "src": D + "c4-asa-gift.webp", "alt": "Robed men with staffs leading donkeys loaded with wooden chests along a dusty hill road", "caption": "A gift to Damascus (impression)", "fx": "dust"},
            {"line": "Imagine the smoke over Tirzah", "src": D + "c4-tirzah.webp", "alt": "A hilltop town with a palace on fire, smoke rising, soldiers with spears watching from the valley", "caption": "Tirzah burns (impression)", "fx": ["smoke", "fire"]},
            {"line": "Omri buys a hill from a man named Shemer", "src": D + "c4-samaria-hill.webp", "alt": "Builders laying cut stone blocks on the summit of a broad round hill among olive groves", "caption": "Samaria begun (impression)", "fx": "clouds"},
            {"line": "Carved ivories were found there too", "src": D + "c4-ivories.webp", "alt": "Carved ivory plaques of a winged sphinx, a palmette and a lotus set into a dark wooden panel", "caption": "Ivory inlays (impression)"},
            {"line": "At Jezreel, by the great valley", "src": D + "c4-jezreel.webp", "alt": "Bird's-eye view of a large walled rectangular enclosure with corner towers and a moat above a wide valley of fields", "caption": "Jezreel enclosure (impression)"},
            {"line": "In the drought, ravens bring him bread", "src": D + "c4-ravens.webp", "alt": "Ravens carrying bread fly down to a hooded figure sitting by a small brook in a dry ravine", "caption": "Ravens by the brook (story)", "fx": "birds"},
            {"line": "Fire falls on Elijah's altar", "src": D + "c4-carmel.webp", "alt": "Fire and smoke rising from a stone altar on a ridge above the sea, people bowing around it", "caption": "Mount Carmel (story)", "fx": ["fire", "waves"]},
            {"line": "Fleeing Jezebel, Elijah walks to Horeb", "src": D + "c4-horeb.webp", "alt": "A small robed figure at the mouth of a cave high on a jagged mountain, wind and cloud sweeping past", "caption": "At Horeb (story)", "fx": "clouds"},
            {"line": "At Jezreel, Ahab wants his neighbour Naboth's vineyard", "src": D + "c4-vineyard.webp", "alt": "A small terraced vineyard with a stone watchtower beside a walled compound of flat-roofed houses", "caption": "Naboth's vineyard (story)"},
            {"line": "Religion in Israel was more varied", "src": D + "c4-ajrud.webp", "alt": "A large storage jar painted with simple figures, a lyre player and a cow, in a desert way station", "caption": "A painted jar, Kuntillet Ajrud (impr.)", "fx": "dust"},
            {"line": "The Bible says Elijah did not die", "src": D + "c4-chariot-fire.webp", "alt": "A chariot and horses of fire rising in a whirlwind above a river valley, a figure watching from the bank", "caption": "The chariot of fire (story)", "fx": "fire"},
            {"line": "Imagine a door opened at the Seder", "src": D + "c4-seder-door.webp", "alt": "A table with matzah, cups of wine and small oil lamps, two children looking toward an open door and a starry night", "caption": "The cup of Elijah (impression)", "fx": "fire"},
            {"line": "Far to the east, Assyria is on the march again", "src": D + "c4-assyria-march.webp", "alt": "A long column of soldiers with conical helmets, horses and spears crossing a river on rafts and skins", "caption": "Assyria crosses the river (impr.)", "fx": ["dust", "waves"]},
            {"line": "Imagine the plain by the Orontes at dawn", "src": D + "c4-qarqar.webp", "alt": "Armies of chariots and soldiers on a plain at dawn, dust rising", "caption": "Qarqar, 853 BC (impression)", "fx": "dust"},
            {"line": "Also in the line are troops from Egypt and Byblos", "src": D + "c4-camels.webp", "alt": "Archers riding camels across a dusty steppe toward a camp of tents and chariots", "caption": "Camel riders (impression)", "fx": "dust"},
            {"line": "Mesha tells his own side", "src": D + "c4-mesha-stone.webp", "alt": "A tall black basalt stone with a rounded top and lines of small letters in a paved courtyard, the Dead Sea behind", "caption": "Mesha's stone (impression)"},
            {"line": "In Israel, a prophet's messenger anoints", "src": D + "c4-jehu.webp", "alt": "A chariot with two galloping horses racing along a valley road toward a walled town, dust behind", "caption": "Jehu drives to Jezreel (story)", "fx": "dust"},
            {"line": "But at Dan, an Aramean king tells another story", "src": D + "c4-teldan.webp", "alt": "Broken pieces of an inscribed stone slab lying before an old arched city gate by a stream", "caption": "Tel Dan fragments (impression)"},
            {"line": "On the Black Obelisk from Nimrud", "src": D + "c4-obelisk.webp", "alt": "A small black obelisk with a stepped top and rows of relief panels of tribute bearers, in a lamp-lit room", "caption": "The Black Obelisk (impression)", "fx": "fire"},
            {"line": "Imagine envoys from Samaria", "src": D + "c4-envoys.webp", "alt": "A row of kneeling envoys in a palace hall with carved wall reliefs, silver, gold bowls and spears laid on the floor", "caption": "Tribute to Assyria (impression)"},
        ],
    },
    "jews-722": {
        "intro": [
            {"line": "Now we begin at the other end", "src": D + "c5-siege.webp", "alt": "A walled city on a high hill at sunset, an army camp of tents and smoke in the valley below", "caption": "Samaria besieged (impression)", "fx": "smoke"},
            {"line": "On the map, Israel in the north", "src": D + "c5-hills.webp", "alt": "Terraced green hills with olive groves and a hilltop town, a snow-capped mountain far to the north", "caption": "The northern hills (impression)", "fx": "clouds"},
        ],
        "play": [
            {"line": "Hazael even marched down the coast", "src": D + "c5-gath-trench.webp", "alt": "A long siege trench curving around the foot of a walled hilltop city on a plain", "caption": "The siege trench at Gath (impr.)", "fx": "dust"},
            {"line": "On a stele found at Tell al-Rimah", "src": D + "c5-rimah-stele.webp", "alt": "A round-topped stone stele carved with a standing king and lines of writing, in an excavation trench with a pick and basket", "caption": "The Tell al-Rimah stele (impr.)"},
            {"line": "Imagine a town in Gilead rebuilding", "src": D + "c5-gilead-wall.webp", "alt": "Villagers rebuilding a stone wall with wooden scaffolding on a hillside, sheep and an old tree nearby", "caption": "Gilead rebuilds (impression)", "fx": "dust"},
            {"line": "At Samaria, excavators found dozens", "src": D + "c5-ostraca.webp", "alt": "Broken pottery pieces with lines of ink writing on a wooden table beside two tall jars and a small lamp", "caption": "The Samaria ostraca (impression)"},
            {"line": "At Megiddo, a jasper seal", "src": D + "c5-shema-seal.webp", "alt": "A round seal carved with a roaring lion beside its clay impression, lying on a cloth", "caption": "The seal of Shema (impression)"},
            {"line": "Imagine a jar of oil", "src": D + "c5-oil-jar.webp", "alt": "Men and a donkey carrying jars of oil up a winding path through olive groves toward a hilltop city", "caption": "Oil for Samaria (impression)", "fx": "clouds"},
            {"line": "In these rich years, a herdsman from Tekoa", "src": D + "c5-amos.webp", "alt": "A cloaked herdsman with a staff, seen from behind, leading sheep along a path in bare desert hills beside two trees", "caption": "A herdsman from Tekoa (impression)", "fx": "clouds"},
            {"line": "Those who lie on beds of ivory", "src": D + "c5-ivory-bed.webp", "alt": "A lamp-lit stone hall with guests reclining on couches inlaid with carved ivory sphinxes and palmettes, musicians playing lyres", "caption": "Beds of ivory (story)", "fx": "fire"},
            {"line": "The book dates his words", "src": D + "c5-earthquake.webp", "alt": "Rows of plain stone pillars, some fallen, among cracked and collapsed walls and broken jars, dust in the air", "caption": "After the earthquake (impression)", "fx": "dust"},
            {"line": "He does not just collect tribute", "src": D + "c5-deportees-relief.webp", "alt": "Two Assyrian scribes writing on a clay tablet and a scroll as a long column of families, ox carts and spearmen passes by", "caption": "Counting the deported (impression)", "fx": "dust"},
            {"line": "The prophet Isaiah tells Ahaz", "src": D + "c5-isaiah.webp", "alt": "A robed prophet and a boy speaking to a group of men beside a stone water channel and pool outside a walled city", "caption": "Isaiah meets Ahaz (story)"},
            {"line": "Assyria strikes. In seven thirty two", "src": D + "c5-damascus.webp", "alt": "An army with tall shields and a wheeled battering ram attacks a walled city among palm and fruit trees, smoke rising", "caption": "Damascus falls (impression)", "fx": ["smoke", "fire"]},
            {"line": "At Hazor, the city of this time ended in fire", "src": D + "c5-hazor-ash.webp", "alt": "A hilltop town burning under clouds of smoke, a line of soldiers with spears on the slope below", "caption": "Hazor burns (impression)", "fx": "smoke"},
            {"line": "Imagine families from Galilee", "src": D + "c5-galilee-road.webp", "alt": "A family with bundles, a child, a donkey with baskets and an old man walk a road by a lake, spearmen alongside", "caption": "Leaving Galilee (impression)", "fx": "dust"},
            {"line": "Shalmaneser the Fifth arrests Hoshea", "src": D + "c5-samaria-siege.webp", "alt": "A walled city on a high round hill, a battering ram on a ramp up the slope and an army camp of tents below", "caption": "The siege of Samaria (impression)", "fx": "dust"},
            {"line": "Then Shalmaneser dies, and Sargon", "src": D + "c5-khorsabad.webp", "alt": "A crowned king with attendants and a parasol walking through an arched gate between two huge winged human-headed bulls", "caption": "Sargon's gate (impression)"},
            {"line": "Imagine the gate of Samaria opening", "src": D + "c5-gate.webp", "alt": "Thin townspeople wait in shadow as a heavy wooden gate opens on soldiers with spears standing outside", "caption": "The gate opens (impression)"},
            {"line": "The Bible says the king of Assyria carried Israel away", "src": D + "c5-exile-road.webp", "alt": "A long column of families, donkeys and an ox cart walking across a wide dry plain toward a distant river, guards alongside", "caption": "The road east (impression)", "fx": "dust"},
            {"line": "At Kalhu, lists of the royal army", "src": D + "c5-charioteers.webp", "alt": "Two-horse chariots with drivers and archers parading before high mudbrick walls, horses with plumes and tassels", "caption": "Assyrian chariots (impression)", "fx": "dust"},
            {"line": "Later Jewish writings call the Samaritans Kutim", "src": D + "c5-gerizim.webp", "alt": "A line of robed pilgrims climbing a winding path up a green rocky mountain among olive trees", "caption": "Mount Gerizim (impression)", "fx": "clouds"},
            {"line": "Imagine a family in Gozan", "src": D + "c5-gozan.webp", "alt": "A mother kneading bread by a mudbrick house and a father mending a net by a river, a child watching the water, a mound in the distance", "caption": "By the Khabur (impression)", "fx": "waves"},
            {"line": "Jerusalem grows fast in these years", "src": D + "c5-jerusalem.webp", "alt": "Workers building a thick new stone wall around a crowded hillside town while people with bundles arrive on the road", "caption": "Jerusalem grows (impression)", "fx": "dust"},
        ],
    },
    "jews-701": {
        "intro": [
            {"line": "Now it is seven oh one BC", "src": D + "c6-lachish-camp.webp", "alt": "A large army camp of tents and campfires on a plain below a walled city on a high mound, at sunset", "caption": "The camp before Lachish (impression)", "fx": "smoke"},
            {"line": "On the map, Judah, from the hills", "src": D + "c6-judah-hills.webp", "alt": "Terraced hills with olive trees sloping down to wide lowlands, a small stone village in the foreground", "caption": "The hills of Judah (impression)", "fx": "clouds"},
        ],
        "play": [
            {"line": "At Beersheba, in the south", "src": D + "c6-storehouse.webp", "alt": "An excavated storehouse with stone pillars and large storage jars, a trowel and a basket in the foreground", "caption": "A storehouse at Beersheba (impression)"},
            {"line": "In two thousand and nine, in a rubbish heap", "src": D + "c6-bulla.webp", "alt": "A small round clay seal impression with a winged sun, lying on an open hand above a sieve of earth", "caption": "A king's seal (impression)"},
            {"line": "The Bible says that in that year the prophet Isaiah", "src": D + "c6-barefoot.webp", "alt": "A barefoot man in a simple wrap, seen from behind, walking down a stone street as townspeople watch from doorways", "caption": "Isaiah's sign (story)", "fx": "dust"},
            {"line": "Imagine the news reaching Jerusalem", "src": D + "c6-news.webp", "alt": "A tired, dusty horse outside a stone city gate, a group of robed elders coming out to meet it", "caption": "News from the coast (impression)", "fx": "dust"},
            {"line": "His son Sennacherib becomes king", "src": D + "c6-nineveh.webp", "alt": "Huge city walls and gates beside a wide river with boats, palaces on a high mound behind", "caption": "Nineveh on the Tigris (impression)", "fx": "waves"},
            {"line": "Hezekiah prepares for war", "src": D + "c6-broadwall.webp", "alt": "Workers on scaffolding build a very thick stone wall over ruined houses, smiths making shields in the foreground", "caption": "Walls and weapons (impression)", "fx": ["dust", "fire"]},
            {"line": "Under the City of David, a tunnel", "src": D + "c6-tunnel.webp", "alt": "A narrow tunnel cut through rock, water running along the floor, lit by a small clay oil lamp", "caption": "Inside the tunnel (impression)"},
            {"line": "Writing cut into its wall", "src": D + "c6-siloam-plate.webp", "photo": True, "alt": "Sepia photograph of the Siloam inscription: a pale slab of rock with faint carved lines of writing, in a museum case", "caption": "The real Siloam inscription · photo Oncenawhile, CC0"},
            {"line": "All over Judah, the handles", "src": D + "c6-lmlk.webp", "alt": "A row of large two-handled storage jars stamped with a round winged emblem, in a lamp-lit storeroom", "caption": "Jars for the king (impression)"},
            {"line": "Imagine the sound of picks", "src": D + "c6-picks.webp", "alt": "Two diggers with picks crouching in a narrow rock tunnel by a small oil lamp, listening", "caption": "Axe against axe (impression)"},
            {"line": "An army from Egypt and Kush", "src": D + "c6-eltekeh.webp", "alt": "Two armies clash on a dusty plain, chariots and shield-bearers on one side, archers with feathered headdresses on the other", "caption": "The battle of Eltekeh (impression)", "fx": "dust"},
            {"line": "Imagine the watchmen on Judah's hills", "src": D + "c6-watchmen.webp", "alt": "Two watchmen on a round stone tower on a hilltop look out over a plain where an army raises dust and smoke", "caption": "Dust on the plain (impression)", "fx": "smoke"},
            {"line": "At the south-west corner of the mound", "src": D + "c6-ramp.webp", "alt": "Shielded battering rams climbing a great stone ramp against a city wall, archers below, smoke rising", "caption": "The siege ramp (impression)", "fx": ["smoke", "fire"]},
            {"line": "In his palace at Nineveh", "src": D + "c6-lachish-relief-plate.webp", "photo": True, "alt": "Sepia photograph of a carved stone panel showing Assyrian archers shooting arrows, in the British Museum", "caption": "The Lachish reliefs, British Museum · photo Mike Peel, CC BY-SA 4.0"},
            {"line": "Imagine a family walking out of the gate", "src": D + "c6-lachish-exile.webp", "alt": "A family with an ox cart piled with bundles, a child on top, walk out of a burnt city gate past soldiers with shields", "caption": "Leaving Lachish (impression)", "fx": "smoke"},
            {"line": "Now Jerusalem. Sennacherib writes", "src": D + "c6-birdcage.webp", "alt": "A walled city on a ridge at dusk, small army camps with fires on the hills around it, one bird flying above", "caption": "Like a bird in a cage (impression)", "fx": "birds"},
            {"line": "Then Assyrian officers come to the wall", "src": D + "c6-rabshakeh.webp", "alt": "Officials in long robes and tall hats with soldiers below a city wall, one calling up to people crowding the top of the wall", "caption": "The Rabshakeh speaks (story)"},
            {"line": "The Bible tells what came next", "src": D + "c6-night-camp.webp", "alt": "A silent army camp of tents among dark hills at night, fires burned down, a beam of light falling from the clouds", "caption": "That night (story)", "fx": "clouds"},
            {"line": "Herodotus, writing about two and a half", "src": D + "c6-mice.webp", "alt": "Mice gnawing at a bowstring and quiver straps beside shields leaning on a tent, at night", "caption": "Herodotus' mice (story)"},
            {"line": "Imagine the first morning after", "src": D + "c6-morning.webp", "alt": "Early morning, townspeople walking out of a city gate onto an empty road through quiet hills, old campfire rings by the road", "caption": "The gates open (impression)", "fx": "dust"},
            {"line": "Jerusalem had been spared", "src": D + "c6-spared.webp", "alt": "A walled hill city of stone houses at sunset, dark storm clouds gathering on the far horizon", "caption": "Jerusalem spared (impression)", "fx": "clouds"},
        ],
    },
    "jews-586": {
        "intro": [
            {"line": "Now it is five eighty six BC", "src": D + "c7-siege-camp.webp", "alt": "A large army camp of tents and campfires on hills around a walled city on a ridge, at dusk", "caption": "Babylon at the gates (impression)", "fx": "smoke"},
            {"line": "On the map, a smaller Judah", "src": D + "c7-small-judah.webp", "alt": "Terraced limestone hills with olive trees and a small stone town, wide lowlands fading in the distance", "caption": "A smaller Judah (impression)", "fx": "clouds"},
        ],
        "play": [
            {"line": "His name, Manasseh of Judah", "src": D + "c7-tribute.webp", "alt": "A small caravan of pack animals with jars and ivory, on a long road toward a distant walled city by a river", "caption": "Tribute for Assyria (impression)", "fx": "dust"},
            {"line": "Just outside Jerusalem, in a family tomb", "src": D + "c7-tomb.webp", "alt": "A rock-cut tomb chamber with stone benches, a small silver scroll lying in the earth, a lamp", "caption": "The tomb at Ketef Hinnom (impression)"},
            {"line": "Scratched into the silver is a blessing", "src": D + "c7-scrolls.webp", "alt": "Two tiny unrolled silver strips with faint scratches, in an open palm, warm lamplight", "caption": "The silver scrolls (impression)"},
            {"line": "The Bible says that in his eighteenth year", "src": D + "c7-law-book.webp", "alt": "A scroll being opened by lamplight inside a stone temple chamber, dust in the air", "caption": "A book in the Temple (story)"},
            {"line": "At Arad, in the south", "src": D + "c7-arad.webp", "alt": "Inside a small fortress shrine, workers carefully lifting stone altars and stacking them, no fire", "caption": "The shrine at Arad (impression)", "fx": "dust"},
            {"line": "In six twelve BC, the Babylonians", "src": D + "c7-nineveh-fall.webp", "alt": "A great city on a river burning, walls broken, smoke over palaces and a temple tower", "caption": "Nineveh falls (impression)", "fx": ["smoke", "fire"]},
            {"line": "Pharaoh Neco marches north", "src": D + "c7-megiddo.webp", "alt": "Two forces meeting at a mountain pass, chariots and a hill fortress above the road", "caption": "The pass at Megiddo (story)", "fx": "dust"},
            {"line": "In six oh five BC, at Carchemish", "src": D + "c7-carchemish.webp", "alt": "A battle by a wide river under a fortress, chariots in the shallows, banners in the dust", "caption": "Carchemish (impression)", "fx": "dust"},
            {"line": "In the next year the Babylonian army takes Ashkelon", "src": D + "c7-ashkelon-fire.webp", "alt": "A coastal city burning, smoke over walls and ships in a harbour, evening light", "caption": "Ashkelon burns (impression)", "fx": ["smoke", "fire"]},
            {"line": "In five ninety seven BC, in the seventh year", "src": D + "c7-597.webp", "alt": "A column of people and pack animals leaving a city gate, soldiers alongside, hills behind", "caption": "The first exile (impression)", "fx": "dust"},
            {"line": "Imagine the road down from the hills", "src": D + "c7-road.webp", "alt": "A young man in a simple robe on a mule, looking back at a hill city as the road descends east", "caption": "Leaving Jerusalem (impression)", "fx": "dust"},
            {"line": "At Lachish, rebuilt after Sennacherib's siege", "src": D + "c7-ostraca.webp", "alt": "Ink letters on broken pottery lying on a stone bench in a gatehouse, an oil lamp beside them", "caption": "Letters in the gate (impression)"},
            {"line": "One officer writes to his lord", "src": D + "c7-signals.webp", "alt": "Watchmen on a city wall at night looking toward a distant dark hill, no fire there", "caption": "We cannot see Azekah (impression)", "fx": "clouds"},
            {"line": "Imagine a night on the wall at Lachish", "src": D + "c7-night-wall.webp", "alt": "A lone watchman on a fortress wall at night, empty dark hills, a cold wind, no signal fire", "caption": "A signal that does not come (impression)", "fx": "clouds"},
            {"line": "In five eighty six BC, or, as some scholars reckon", "src": D + "c7-fall.webp", "alt": "A hill city with a breach in its wall, fire in the houses, smoke rising at dawn", "caption": "Jerusalem falls (impression)", "fx": ["smoke", "fire"]},
            {"line": "In the City of David, and in houses", "src": D + "c7-ash.webp", "alt": "A burnt stone room, collapsed roof beams, a layer of ash and a few arrowheads on the floor", "caption": "The burnt rooms (impression)"},
            {"line": "Imagine the smoke over the ridge", "src": D + "c7-smoke-ridge.webp", "alt": "A bare rocky ridge under a column of smoke, an empty platform of stone, the city below in ruin", "caption": "The mount empty of its house (impression)", "fx": "smoke"},
            {"line": "In Babylon, unbaked clay tablets list rations", "src": D + "c7-rations.webp", "alt": "Clay tablets and small jars of oil on a storeroom shelf in a mudbrick palace, a scribe's stylus", "caption": "Rations for a king (impression)"},
            {"line": "Other tablets, found in the Babylonian countryside", "src": D + "c7-alyahudu.webp", "alt": "Families working irrigation canals and fields on a flat plain, mudbrick houses, a wide river far off", "caption": "The city of Judah, in exile (impression)", "fx": "waves"},
            {"line": "Over those who remained in the land", "src": D + "c7-mizpah.webp", "alt": "A modest walled town on a hill, the ruins of a larger city on the southern horizon", "caption": "Gedaliah at Mizpah (story)", "fx": "clouds"},
            {"line": "A clay seal impression reading belonging to Berekyahu", "src": D + "c7-bulla.webp", "alt": "A small round clay seal impression in an open palm, faint marks, no readable letters", "caption": "A scribe's seal? (impression)"},
            {"line": "Did the land lie empty", "src": D + "c7-benjamin.webp", "alt": "People harvesting grain and drawing water at a well in rolling hills, a small village, not a desert", "caption": "Life in Benjamin (impression)"},
            {"line": "Imagine a pot of oil measured out", "src": D + "c7-oil.webp", "alt": "A storekeeper pours oil from a jar into a smaller pot in a lamp-lit Babylonian storeroom", "caption": "A measure of oil (impression)"},
            {"line": "By the rivers of Babylon, a later psalm says", "src": D + "c7-rivers.webp", "alt": "People sitting under willows by a wide quiet river at evening, a great city on the far bank", "caption": "By the rivers (story)", "fx": "waves"},
            {"line": "A generation later, Babylon itself will fall", "src": D + "c7-horizon.webp", "alt": "Dawn over a great river city, a distant column of riders under a pale sky, the walls still standing", "caption": "A new power in the east (impression)", "fx": "clouds"},
        ],
    },
    "jews-538": {
        "intro": [
            {"line": "Now it is five thirty nine BC", "src": D + "c8-babylon-gates.webp", "alt": "The great walls and gated river front of Babylon on a flat plain, date palms, late afternoon light", "caption": "Babylon still stands (impression)", "fx": "clouds"},
            {"line": "On the map, a remnant still lives", "src": D + "c8-benjamin.webp", "alt": "People harvesting grain and drawing water at a well in rolling hills, a small village among terraces", "caption": "Those who remained (impression)"},
        ],
        "play": [
            {"line": "When Jerusalem fell, the king in Babylon", "src": D + "c8-nabonidus.webp", "alt": "A king in a long robe standing on a palace terrace above a great river city, evening light", "caption": "Nabonidus in Babylon (impression)"},
            {"line": "A Babylonian chronicle says that for years he left", "src": D + "c8-teima.webp", "alt": "An oasis town of mud-brick houses among palms, a desert road approaching, dry hills beyond", "caption": "Teima in Arabia (impression)", "fx": "dust"},
            {"line": "In the east, a Persian king was already taking land", "src": D + "c8-pasargadae.webp", "alt": "A stone palatial terrace and garden pavilions on a high Iranian plain, mountains far off", "caption": "The land of Cyrus (impression)", "fx": "clouds"},
            {"line": "The Babylonian chronicle says that Cyrus first made war on the Medes", "src": D + "c8-ecbatana.webp", "alt": "A walled royal city climbing a forested mountain slope, a caravan on the road below", "caption": "Ecbatana in Media (impression)"},
            {"line": "Greek writers later tell how he took Lydia", "src": D + "c8-sardis.webp", "alt": "A wealthy city on a steep acropolis above a river valley, walls and a camp of tents in the foreground", "caption": "Sardis (Greek tradition)", "fx": "clouds"},
            {"line": "In five thirty nine BC, Cyrus moves west", "src": D + "c8-opis.webp", "alt": "Two armies meeting on a river plain, dust and banners, a city in the distance", "caption": "The battle at Opis (impression)", "fx": "dust"},
            {"line": "Then Sippar was taken without a battle", "src": D + "c8-gates-open.webp", "alt": "The great gates of a river city standing open, a column of soldiers walking in, the walls unbreached", "caption": "Babylon entered without a battle (impression)"},
            {"line": "In the ruins of Babylon, more than two thousand years later, a clay cylinder", "src": D + "c8-cylinder-plate.webp", "photo": True, "alt": "Sepia photograph of the Cyrus Cylinder: a barrel-shaped baked clay object covered in cuneiform, in the British Museum", "caption": "The Cyrus Cylinder, British Museum · photo Daderot, CC0"},
            {"line": "He says he returned the gods to their cities", "src": D + "c8-gods-return.webp", "alt": "A procession of carts carrying small cult statues toward a walled Mesopotamian city among palms", "caption": "Gods and people sent home (impression)", "fx": "dust"},
            {"line": "The cylinder does not name Judah", "src": D + "c8-cylinder.webp", "alt": "A clay cylinder covered in wedge-shaped marks lying in lamplight, a stylus beside it", "caption": "A policy in the language of Babylon (impression)"},
            {"line": "The Hebrew Bible tells a more specific story", "src": D + "c8-ezra-scroll.webp", "alt": "An open parchment scroll with faint unreadable marks on a wooden table, lamp light, two figures in cloaks", "caption": "The decree in Ezra (tradition)"},
            {"line": "The Bible says that in the first year of Cyrus", "src": D + "c8-return-road.webp", "alt": "Families with donkeys and carts walking a long road toward distant hills, not a great army", "caption": "A column on the road (story)", "fx": "dust"},
            {"line": "Many families also stayed in Babylon", "src": D + "c8-alyahudu.webp", "alt": "A modest canal-side village of mud-brick houses among date palms, people and donkeys at work", "caption": "Judeans still in Babylonia (impression)", "fx": "waves"},
            {"line": "Jerusalem, when they reached it", "src": D + "c8-bare-mount.webp", "alt": "A reduced hill city with broken walls, a bare stone platform on the ridge, a few houses, morning light", "caption": "A bare mount (impression)", "fx": "clouds"},
            {"line": "The Bible says they settled in their towns", "src": D + "c8-altar.webp", "alt": "People gathered around a simple stone altar on a bare rocky platform, a modest offering fire, ruined walls behind", "caption": "An altar before the house (story)", "fx": "smoke"},
            {"line": "Persian rule in this land is real", "src": D + "c8-yehud.webp", "alt": "A modest hill town among terraced fields and olive trees, much smaller than an old royal city", "caption": "Yehud, a small province (impression)"},
            {"line": "For years, the Bible says, the work on the house of the Lord ceased", "src": D + "c8-halt.webp", "alt": "Unfinished foundation stones and a low incomplete platform on a rocky hill, weeds among idle blocks, empty of workers", "caption": "The work ceases (story)"},
            {"line": "After Cambyses, the empire shakes", "src": D + "c8-behistun.webp", "alt": "A huge cliff above a mountain road, a carved panel high on the rock, a caravan passing below", "caption": "Darius at Behistun (impression)", "fx": "clouds"},
            {"line": "The books of Haggai and Zechariah present themselves", "src": D + "c8-prophets.webp", "alt": "Figures speaking to a small crowd in a hill-town square, unfinished stone work behind them", "caption": "Finish the house (tradition)"},
            {"line": "In the sixth year of Darius", "src": D + "c8-temple-done.webp", "alt": "A modest rectangular stone house with a small courtyard on a hill, people bringing offerings, morning light", "caption": "The Second Temple (tradition)"},
            {"line": "Coins and seal impressions from a little later", "src": D + "c8-seals.webp", "alt": "Small clay seal impressions lying on a wooden table in lamplight, no readable letters", "caption": "Seals of the province (impression)"},
            {"line": "In Babylon, Judean families still live by the canals", "src": D + "c8-alyahudu.webp", "alt": "A modest canal-side village of mud-brick houses among date palms, people and donkeys at work", "caption": "A life in two places (impression)", "fx": "waves"},
            {"line": "Darius builds a new ceremonial city at Persepolis", "src": D + "c8-persepolis.webp", "alt": "A ceremonial stone terrace of tall columns and monumental stairways on a high dry plateau, mountains behind", "caption": "Persepolis (impression)", "fx": "clouds"},
            {"line": "In time, new empires will come to this land", "src": D + "c8-horizon.webp", "alt": "A wide quiet horizon over the Judean hills at dusk, a small distant town on a ridge, a long empty road", "caption": "The story is not finished (impression)", "fx": "clouds"},
        ],
    },
    "jews-167": {
        "intro": [
            {"line": "The Long Map. The Story of the Jews. The Maccabees.", "src": "images/vignettes/c9-title.webp", "alt": "A small Second Temple on a rocky hill, pale stone, quiet courtyards, Judean hills in warm evening light", "caption": "The Second Temple in Yehud (impression)", "fx": "clouds"},
            {"line": "Now it is one hundred and sixty seven BC", "src": "images/vignettes/c9-crisis-eve.webp", "alt": "Jerusalem on a ridge at dusk, a temple platform above tight streets, a tense stillness in the air", "caption": "A crisis is coming (impression)", "fx": "clouds"},
        ],
        "play": [
            {"line": "When the Second Temple was dedicated, Yehud was still a small Persian province", "src": "images/vignettes/c9-yehud.webp", "alt": "A modest walled hill city with a small temple, terraced slopes, a quiet provincial landscape", "caption": "Yehud, a small province (impression)"},
            {"line": "In three thirty two BC, Alexander of Macedon takes the Persian empire", "src": "images/vignettes/c9-tyre.webp", "alt": "An island harbour city under siege, causeway and ships, stone walls above a dark sea", "caption": "The siege of Tyre (impression)", "fx": "waves"},
            {"line": "When Alexander dies in three twenty three BC, his generals divide the lands", "src": "images/vignettes/c9-successors.webp", "alt": "A wide Hellenistic world of new cities and roads, two distant royal capitals under a pale sky", "caption": "The empire is divided (impression)", "fx": "clouds"},
            {"line": "Judaea first lies under the Ptolemies, who rule from Alexandria in Egypt", "src": "images/vignettes/c9-alexandria.webp", "alt": "A great harbour city on the Egyptian coast, a lighthouse on a spit of land, ships at anchor", "caption": "Alexandria, a new capital (impression)", "fx": "waves"},
            {"line": "In about two hundred BC, after a battle at Paneas, under Mount Hermon", "src": "images/vignettes/c9-paneas.webp", "alt": "A cave and spring at the foot of a snow-touched mountain, a small shrine, a valley opening south", "caption": "Paneas under Mount Hermon (impression)"},
            {"line": "In one hundred and seventy five BC, the second book of the Maccabees says, a man called Jason", "src": "images/vignettes/c9-gymnasium.webp", "alt": "An open palaestra courtyard in a hill city, columns and exercise grounds beside older stone houses, no faces close up", "caption": "A gymnasium in Jerusalem (impression)"},
            {"line": "A royal letter on stone, found in the south of the land", "src": "images/vignettes/c9-stele.webp", "alt": "A tall inscribed stone stele standing in a dusty courtyard, Greek letters suggested as marks, not readable", "caption": "A royal letter on stone (impression)"},
            {"line": "Antiochus the Fourth, called Epiphanes, is a real king", "src": "images/vignettes/c9-antiochus.webp", "alt": "A royal column on campaign in a wide river land, banners and dust, a distant city, no recognisable portrait", "caption": "A king in Egypt and Syria (impression)", "fx": "dust"},
            {"line": "In one hundred and sixty seven BC, or in the Seleucid year usually reckoned so", "src": "images/vignettes/c9-crisis.webp", "alt": "A tense street below a temple platform, shut doors, empty courts, smoke in the distance", "caption": "The crisis remembered (impression)", "fx": "smoke"},
            {"line": "The second book, and the book of Daniel, speak of a desolating sacrilege", "src": "images/vignettes/c9-altar.webp", "alt": "A temple court with an alien altar of strange shape set upon an older stone platform, no sacred text visible", "caption": "An alien altar, in the tradition (impression)"},
            {"line": "What we can hold to is more modest", "src": "images/vignettes/c9-hold.webp", "alt": "Quiet limestone hills and a small city on a ridge, open and undecided, morning light", "caption": "What the stones can show is limited (impression)"},
            {"line": "Imagine the Temple mount, and an altar that is not the old altar", "src": "images/vignettes/c9-imagine-mount.webp", "alt": "A high stone platform above a city, an unfamiliar altar in the court, fear suggested by empty streets", "caption": "Imagine the Temple mount (scene)", "fx": "smoke"},
            {"line": "The first book of the Maccabees says the revolt begins at Modein", "src": "images/vignettes/c9-modein.webp", "alt": "A small hill town of stone houses among olive terraces, paths leading into rougher hills", "caption": "Modein, in the tradition (impression)"},
            {"line": "The books tell of early fights in the hills, and of a victory on the road at Beth-horon", "src": "images/vignettes/c9-bethhoron.webp", "alt": "A steep winding road climbing from the coastal plain into limestone hills, dust on the ascent", "caption": "The ascent of Beth-horon (impression)", "fx": "dust"},
            {"line": "Imagine paths in the limestone hills, and a small force that knows the land", "src": "images/vignettes/c9-paths.webp", "alt": "Narrow goat paths through pale limestone hills, a small band seen only as distant figures, a wide royal road below", "caption": "Paths in the hills (scene)"},
            {"line": "Jerusalem is retaken in this tradition, and the Temple mount is cleared", "src": "images/vignettes/c9-retaken.webp", "alt": "Men clearing a stone court on a temple platform, old debris at the edge, morning light on pale walls", "caption": "The mount is cleared (impression)"},
            {"line": "In one hundred and sixty four BC, in the usual reckoning, the first book says the altar is rebuilt", "src": "images/vignettes/c9-dedication.webp", "alt": "A newly built stone altar in a modest temple court, simple offerings, people at a distance, no readable writing", "caption": "The Temple dedicated again (impression)"},
            {"line": "That memory will become the festival of Dedication, later called Hanukkah", "src": "images/vignettes/c9-dedication-lights.webp", "alt": "Small oil lamps glowing in a quiet stone court at night, a modest temple facade, warm lamp light", "caption": "The festival of Dedication (impression)"},
            {"line": "At Beth-zur, a fortress on the road south of Jerusalem", "src": "images/vignettes/c9-bethzur.webp", "alt": "A hill fortress of rough stone above a south road, terraces and a dry valley", "caption": "Beth-zur (impression)"},
            {"line": "In time, Jonathan is recognised as high priest, and Simon after him", "src": "images/vignettes/c9-hasmonean.webp", "alt": "A small hill state around Jerusalem, terraced slopes, a modest palace-like building and a temple on the ridge", "caption": "A ruling house in the hills (impression)"},
            {"line": "The first book also says this house takes the port of Joppa", "src": "images/vignettes/c9-joppa.webp", "alt": "A sandy harbour with small ships, a coastal town of pale houses, the sea opening west", "caption": "The port of Joppa (impression)", "fx": "waves"},
            {"line": "Later coins and later buildings will mark that house", "src": "images/vignettes/c9-coins.webp", "alt": "A few small ancient bronze coins on a cloth, pale designs suggested, no readable lettering or royal portraits", "caption": "Later coins of the house (impression)"},
            {"line": "The empire that first took this land from Persia is itself coming apart", "src": "images/vignettes/c9-rome-west.webp", "alt": "A wide western sea and a distant shore, a sense of a new power beyond the horizon, evening light", "caption": "A new power in the west (impression)", "fx": "clouds"},
            {"line": "In time, a Roman general will stand in Jerusalem, and this Hasmonean house will lose its independence", "src": "images/vignettes/c9-horizon.webp", "alt": "Jerusalem on its hills under a long quiet sky, a road leading west, the story unfinished", "caption": "The story is not finished (impression)", "fx": "clouds"},
        ],
    },
}


# the quick reel reuses the full film's pictures (same alt, caption and fx), looked up by file name
def _find(name):
    for reels in VIGNETTES.values():
        for where, vs in reels.items():
            if where == "quick": continue
            for v in vs:
                if v.get("src", "").endswith("/" + name): return v
                for im in v.get("images", []):
                    if im["src"].endswith("/" + name): return im
    raise KeyError(name)
for _reels in VIGNETTES.values():
    for _v in _reels.get("quick", []):
        _base = _find(_v.pop("_name")); _v.update({k: x for k, x in _base.items() if k != "line"})

# Chapters 3-5: the quick reels are made of the chapter's own lines (build/quick.py), so each quick line simply
# reuses the picture of the line it came from
def _auto_quick(prefix, M):
    reels = VIGNETTES.setdefault(prefix, {}); out = []
    for b, orig in zip(M.QUICK, M.QUICK_FROM):
        if not orig: continue
        hit = [v for where in ("intro", "play") for v in reels.get(where, []) if orig.startswith(v["line"])]
        if hit: out.append(dict(hit[0], line=M.speech(b)))
    reels["quick"] = out
import narration_jews_1000 as _n1000, narration_jews_930 as _n930, narration_jews_722 as _n722, narration_jews_701 as _n701, narration_jews_586 as _n586, narration_jews_538 as _n538, narration_jews_167 as _n167
_auto_quick("jews-1000", _n1000); _auto_quick("jews-930", _n930); _auto_quick("jews-722", _n722); _auto_quick("jews-701", _n701); _auto_quick("jews-586", _n586); _auto_quick("jews-538", _n538); _auto_quick("jews-167", _n167)
