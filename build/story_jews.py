import narration_jews_1207 as NAR
import narration_jews_1150 as NAR1150
import narration_jews_1000 as NAR1000
import narration_jews_930 as NAR930
import narration_jews_722 as NAR722
A,D,T = "attested","disputed","tradition"
STORY = {
 "id":"jews","title":"Story of the Jews","site":"The Long Map",
 "book":"Book One",
 "series":"A series of histories, each told from the perspective of a different people. Later books (Book Two: Story of the Arabs, then Story of the Persians) are coming later and not yet written.",
 "theme":{"accent":"#b8893a","accent-ink":"#7a5614","accent-soft":"#f0dfb4","accent-map":"#e2b45a","accent-foil":"#e0bd72"},
 "perspective":"Told from the perspective of Israel and the Jewish people. Other peoples appear as the world around them.",
 "intro":"This is the story of the Jewish people, told on a map. It begins with a name carved in stone. Around 1208 BC an Egyptian king listed his enemies in Canaan, and among them was a people called Israel. Jewish tradition remembers this early world through the Torah: the patriarchs, slavery in Egypt, the Exodus and the covenant at Sinai. Ancient inscriptions and archaeology add their own evidence. Here both are told side by side, and every line says whether it is attested, disputed, or tradition.",
 "from":-1400,"to":2030,
 "stops":[
  {"year":-1207,"label":"1207 BC","title":"Israel is named","era":"data/eras/1207bc.json","file":"data/stories/jews/1207bc.json",
   "years":"1207–c. 1150 BC","summary":"Around 1208 BC Pharaoh Merneptah names a people called Israel on a stone, the oldest known mention of the name. Then the palace world of the Late Bronze Age falls, the Sea Peoples arrive, and new villages spread across the hills of Canaan."},
  {"year":-1150,"label":"c. 1150 BC","title":"Villages in the hills","era":"data/eras/1150bc.json","file":"data/stories/jews/1150bc.json",
   "years":"c. 1150–1000 BC","summary":"The Philistines hold five cities on the coast while the hill villages of Israel grow. Jewish tradition tells of Shiloh, the Judges and Saul, the first king; the chapter ends with what can and cannot be known about David."},
  {"year":-1000,"label":"c. 1000 BC","title":"David and Solomon: tradition and evidence","era":"data/eras/1000bc.json","file":"data/stories/jews/1000bc.json",
   "years":"c. 1000–930 BC","summary":"The Bible tells of David's Jerusalem and Solomon's temple, and archaeologists still debate how large their kingdom was. Tradition and evidence are told side by side, until the kingdom divides into Israel and Judah."},
  {"year":-930,"label":"c. 930 BC","title":"Israel and Judah","era":"data/eras/930bc.json","file":"data/stories/jews/930bc.json",
   "years":"c. 930–841 BC","summary":"Israel and Judah live side by side among Aram, Moab and a rising Assyria. Omri makes Samaria a capital, and stones from Qarqar, Moab, Dan and Nimrud name Israel's kings, down to Jehu's tribute in 841 BC."},
  {"year":-722,"label":"722 BC","title":"Fall of Samaria","era":"data/eras/722bc.json","file":"data/stories/jews/722bc.json",
   "years":"c. 841–722 BC","summary":"Aram presses on Israel, then Assyria returns to stay. Jeroboam II's Israel prospers and Amos and Hosea speak out, until Tiglath-pileser III takes Galilee and Samaria falls. Its people are carried off, and Judah stands alone."},
  {"year":-701,"label":"701 BC","title":"Sennacherib at Jerusalem","years":"701 BC","summary":"Coming soon. Sennacherib of Assyria marches on Judah, takes Lachish and shuts Hezekiah up in Jerusalem.",
   # reached at the end of the 722 BC Play (Chapter 5 ends c. 720 BC with Judah alone, a vassal of Assyria)
   "soon":{"title":"Sennacherib at Jerusalem","text":"Next chapter coming soon. Samaria has fallen and Israel is an Assyrian province. In 701 BC a new king of Assyria, Sennacherib, marches on Judah. He takes Lachish and shuts Hezekiah up in Jerusalem, 'like a bird in a cage'. That is where the next chapter begins.",
     "hl":["jerusalem","lachish","nineveh","judah","assyria"],"focus":{"c":[39.0,33.6],"k":1.9}}},
  {"year":-586,"label":"586 BC","title":"The First Temple destroyed"},
  {"year":-538,"label":"538 BC","title":"Return under Persia"},
  {"year":-516,"label":"516 BC","title":"The Second Temple"},
  {"year":-167,"label":"167 BC","title":"The Maccabees"},
  {"year":-63,"label":"63 BC","title":"Rome arrives"},
  {"year":70,"label":"AD 70","title":"The Second Temple destroyed"},
  {"year":135,"label":"AD 135","title":"Bar Kokhba revolt ends"},
  {"year":638,"label":"AD 638","title":"Arab conquest of Jerusalem"},
  {"year":1948,"label":"1947–48","title":"Partition and war"},
  {"year":1979,"label":"1979","title":"Egypt–Israel peace"}]
}
STOP = {
 "story":"jews","year":-1207,"label":"1207 BC","title":"Israel is named",
 "keyObjects":["israelp","hills","jerusalem","shechem","ashkelon","gezer","yenoam","jordan"],
 # the opening film: a short opener that ends on a choice, then chapters 2 and 3 (see narration_jews_1207.py)
 "transitionIn":{"text":"The first chapter of the Jewish story on this map. Egypt, Hatti, Assyria and Babylon are the great powers. In the hills of Canaan lives a people called Israel.",
   "title":"The world of 1207 BC","ambient":"desert","beats":NAR.clean(NAR.INTRO_BEATS)},
 "transitionOut":{"to":-1150,"text":"Next: the hill villages grow over the following generations. In Jewish memory this is the time of the Judges, when the tribes lived without a king."},
 "events":[
  {"id":"kadesh","kicker":"Background","title":"A land between empires","date":"1274 BC","cert":A,
   "text":"At Kadesh in Syria, Ramesses II of Egypt fought the Hittite king Muwatalli II in one of the largest chariot battles of the ancient world. Both kings claimed victory. Afterwards the frontier settled: the Hittites kept Syria, and Egypt kept Canaan.",
   "why":"The land where Israel would soon appear lay on Egypt's side of this line. Again and again in Jewish history, life in this narrow land would be shaped by the great powers on either side.",
   "claims":[["Battle of Kadesh, year 5 of Ramesses II (1274 BC in the usual chronology).",A,["bryce","kuhrt"]],["Ramesses' own account of personal triumph is royal propaganda. Most historians see a stalemate.",D,["bryce","vdm"]]],
   "src":["bryce","kuhrt","vdm"],"objects":["kadesh","orontes","hatti","egypt","piramesses"],"focus":{"c":[36.0,33.8],"k":2.6},"hl":["kadesh","orontes"]},
  {"id":"treaty","kicker":"Background","title":"Peace between Egypt and Hatti","date":"c. 1259 BC","cert":A,
   "text":"In Ramesses II's 21st year, Egypt and the Hittite king Hattusili III made one of the oldest peace treaties known. It was written on silver tablets. Copies survive in hieroglyphs on temple walls at Karnak and the Ramesseum, and in Akkadian on clay tablets found at Hattusa.",
   "why":"The peace held for the rest of the century. Canaan stayed under Egyptian rule, with its roads, garrisons and tribute. This is the world in which Israel's name first enters writing.",
   "claims":[["Treaty of year 21 of Ramesses II with Hattusili III.",A,["bryce2006","beckman"]],["Egyptian copies at Karnak and the Ramesseum; Akkadian tablets at Hattusa.",A,["bryce2006","beckman"]]],
   "src":["bryce2006","beckman"],"objects":["hattusa","thebes","egypt","hatti","carchemish"],"focus":{"c":[34.5,34.0],"k":1.3},"hl":["hattusa","thebes"]},
  {"id":"canaan","kicker":"The land","title":"Canaan under Egypt","date":"13th century BC","cert":A,
   "text":"Canaan was a patchwork of small city-states, each with its own ruler and Egypt as overlord. Egyptian troops sat at Gaza and Beth-Shean, and a fortified road, the Ways of Horus, linked Egypt to Canaan. A century earlier, local rulers of Jerusalem, Shechem, Gezer and Megiddo wrote clay letters to Pharaoh, each asking for his favour.",
   "why":"Many of these names run through the Hebrew Bible: Jerusalem, Shechem, Hebron, Megiddo, Hazor, Gezer. They were already old towns long before Israel had kings. The great city of Hazor in the north had probably already been destroyed.",
   "claims":[["Egyptian garrisons at Gaza and Beth-Shean; forts along the Ways of Horus.",A,["morris"]],["Amarna letters from rulers of Jerusalem, Shechem, Gezer and Megiddo (14th century BC).",A,["moran"]],["Hazor was destroyed in the 13th century BC. Who destroyed it, and exactly when, is disputed.",D,["zuckerman","fink2005"]],["The Book of Joshua tells that Joshua conquered Hazor and burned it.",T,["bible"]]],
   "src":["morris","moran","killebrew","zuckerman"],"objects":["gaza","bethshean","megiddo","jerusalem","shechem","gezer","hazor","wayshorus","coastroad","canaanites"],"focus":{"c":[35.1,32.2],"k":5.5},"hl":["gaza","bethshean","jerusalem","shechem","megiddo"]},
  {"id":"exodus","kicker":"Jewish tradition","title":"The memory of Egypt","date":"Tradition, no fixed date","cert":T,
   "text":"The Hebrew Bible tells how the children of Israel, descendants of Abraham, Isaac and Jacob, went down to Egypt and were enslaved there. God brought them out under the leadership of Moses. At Mount Sinai they received the Torah, and after forty years in the wilderness they came to the land of Canaan.",
   "why":"For Jews, the Exodus is the founding memory: the story of becoming a free people bound by a covenant with God. It is retold every year at the Passover Seder, and it shapes prayer and law: 'you shall not wrong a stranger, for you were strangers in the land of Egypt' (Exodus 22:21).",
   "claims":[["The account of slavery, Exodus, Sinai and the wilderness is told in the Torah (Exodus to Deuteronomy).",T,["bible"]],["Exodus 1:11 names the store-cities Pithom and Raamses. Many scholars connect Raamses with Pi-Ramesses, the residence of Ramesses II.",D,["killebrew","pusch"]],["People from Canaan did live and work in New Kingdom Egypt, and Egypt ruled Canaan, so contact between the two lands was real.",A,["killebrew","morris"]],["No Egyptian text found so far mentions Moses or the Exodus. Scholars differ on how the memory relates to history, from a large historical exodus to the experience of a smaller group.",D,["killebrew","faust","finkelstein"]]],
   "src":["bible","killebrew","faust"],"objects":["piramesses","sinai","nile","egypt","israelp"],"focus":{"c":[32.6,30.2],"k":2.6},"hl":["piramesses","sinai"]},
  {"id":"assyria","kicker":"The wider world","title":"Assyria on the rise","date":"c. 1243–1207 BC","cert":A,
   "text":"Far to the east, Tukulti-Ninurta I of Assyria defeated the Hittites near Nihriya, captured the Babylonian king Kashtiliashu IV and plundered Babylon, carrying off the statue of the god Marduk. He built himself a new capital, Kar-Tukulti-Ninurta. Around 1207 BC he was killed there by one of his sons.",
   "why":"For now Assyria is far away. Five centuries later Assyria would conquer the kingdom of Israel and take Samaria (722 BC), one of the great turning points in Jewish history.",
   "claims":[["Reign c. 1243–1207 BC; capture of Kashtiliashu IV and of Babylon.",A,["grayson","chron","brinkman"]],["Killed by his son(s) in a revolt; Ashur-nadin-apli followed.",A,["chron","grayson"]],["His claim to have carried off '28,800 Hittites' is a royal boast; the number cannot be checked.",D,["riao"]]],
   "src":["grayson","chron","brinkman","during"],"objects":["assyria","assur","kartn","babylon","babylon_s","tigris","euphrates"],"focus":{"c":[43.8,34.3],"k":2.8},"hl":["assur","kartn","babylon"]},
  {"id":"year5","kicker":"Crisis","title":"Famine, war and the 'Sea Peoples'","date":"c. 1208 BC","cert":A,
   "text":"In Merneptah's fifth year, Libyans under their chief Meryey invaded Egypt with allies the Egyptians named Ekwesh, Teresh, Lukka, Sherden and Shekelesh, groups modern scholars call 'Sea Peoples'. Merneptah defeated them. In the same years he sent grain to the Hittites, as he says, 'to keep alive' the land of Hatti in a famine.",
   "why":"The old order was starting to break. Over the next decades, palaces fell from Greece to Syria. In the hills of Canaan, a new village society would grow in the gap that opened up, and among the later newcomers on the coast were the Philistines, well known from the Bible.",
   "claims":[["The Libyan war of year 5 and the named allies come from Merneptah's Great Karnak Inscription.",A,["kitchen4","cline"]],["Grain shipped to Hatti 'to keep alive' the land.",A,["kitchen4","cline"]],["The Bronze Age collapse had many causes, including drought, earthquakes, war and broken trade. How much each mattered is disputed.",D,["cline"]],["The Peleset (Philistines) appear under Ramesses III, a generation later.",A,["yasur","cline"]]],
   "src":["kitchen4","cline","yasur"],"objects":["seapeoples","libyans","medsea","ugarit","cyprus","hatti"],"focus":{"c":[30.5,33.0],"k":1.3},"hl":["seapeoples","libyans","ugarit"]},
  {"id":"stele","kicker":"The first mention","title":"'Israel' in stone","date":"c. 1208/1207 BC","cert":A,
   "text":"In the same year Merneptah set up a victory hymn in his temple at Thebes. Near its end come a few lines about Canaan: 'Canaan is plundered with every evil. Ashkelon is carried off, Gezer is seized, Yenoam is made non-existent. Israel is laid waste, its seed is not.' The cities are written with the sign for a foreign land. Israel is written with the sign for a people.",
   "why":"This is the oldest known mention of Israel outside the Bible. It shows that a group called Israel lived in Canaan around 1208 BC, distinct enough for Egypt to name it beside the old cities. Pharaoh's boast that Israel was finished did not come true: more than 3,200 years later the name of Israel lives on in the Jewish people.",
   "claims":[["Text of the Merneptah Stele, year 5. Quotation in standard translation.",A,["stele","kitchen4"]],["Israel is written with the determinative for a people, the cities with the sign for a foreign land.",A,["hasel"]],["Whether 'seed' means grain or descendants is debated.",D,["hasel"]],["The stele does not say where Israel lived. Most scholars place it in Canaan, many in the central hill country.",D,["hasel","fink2013"]],["Found by Flinders Petrie in 1896 in Merneptah's mortuary temple in western Thebes; the stone is a reused stele of Amenhotep III.",A,["petrie1897","stele"]]],
   "src":["stele","kitchen4","hasel","petrie1897"],"pic":{"src":"images/merneptah.jpg","cap":"The Merneptah Stele, Egyptian Museum, Cairo. Photograph by Onceinawhile, 2022. CC BY-SA 4.0."},
   "objects":["israelp","ashkelon","gezer","yenoam","thebes"],"focus":{"c":[35.0,31.95],"k":5.5},"hl":["israelp","ashkelon","gezer","yenoam"]},
  {"id":"villages","kicker":"The land of Israel","title":"New villages in the hills","date":"c. 1200–1000 BC","cert":D,
   "text":"Over the next two centuries, small farming villages spread across the central hill country, where few people had lived before. Surveys count about 30 sites there in the 13th century BC and about 250 by the end of the Iron Age I, around 1000 BC.",
   "why":"These hills, around Shechem, Shiloh, Jerusalem and Hebron, became the heartland of the later kingdoms of Israel and Judah. Jewish tradition remembers this as the time of the Judges: 'In those days there was no king in Israel' (Judges 21:25).",
   "claims":[["About 30 sites and 50 hectares in the 13th century BC; about 250 sites and 220 hectares in late Iron I.",A,["fink2013"]],["Population about 10,000 rising to about 45,000. These figures are calculated from built-up area, so they are rough.",D,["fink2013"]],["Many archaeologists identify these villagers with early Israel. Others caution that pottery and houses alone cannot show who people felt they were.",D,["faust","fink2013","killebrew"]],["Few or no pig bones are found at these hill sites, and some scholars link this to Israelite identity.",D,["faust"]],["The Book of Judges tells of tribes led by judges such as Deborah and Gideon.",T,["bible"]]],
   "src":["fink2013","finkelstein","faust"],"objects":["hills","izbetsartah","shechem","jerusalem","hebron","jordan","deadsea","jezreel"],"focus":{"c":[35.25,31.95],"k":6.5},"hl":["hills","izbetsartah","shechem","jerusalem","hebron"]}
 ]
}

# ---------- explore progress: the key objects of this stop ----------
STOP["explore"] = {
 "key":["israelp","hills","izbetsartah","jerusalem","shechem","jordan","gezer","ashkelon","yenoam","megiddo","egypt","seapeoples"],
 "text":"Open each key place or people on the map to read its fact box. Unexplored ones glow; explored ones get a check. Your progress is saved on this device. When you are ready, press Play to move on to c. 1150 BC."
}

# ---------- play: timed transition 1207 BC -> c. 1150 BC ----------
# A beat runs its steps together; beats run one after another.
# Step types: caption, focus, migration, border, battle, year (+ optional audio cue on any beat: "audio":"path.mp3").
# Every caption carries cert + sources. Uncertain movements are dashed and marked Disputed.
STOP["play"] = {
 "to":-1150, "title":"From 1207 BC to c. 1150 BC",
 "intro":"Plays full screen like a short narrated film, with subtitles (CC). Pause, step back or forward, or change speed at any time. Stop whenever you like: it remembers your chapter.",
 "zoneObjects":{"philistia":"philistines","highlands":"israelp"},
 # sound (js/app.js, assets/sfx/README.md): the scene's ambient loop; battle, migration, border and year
 # steps get a default effect; "sfx" overrides it (null = none) and "sfxHold" (ms) lets it play out
 "ambient":"desert",
 # the narrated beats, one recorded line each (build/narration_jews_1207.py, audio from build/narrate.py)
 "beats":NAR.clean(NAR.PLAY)
}


# ---------- c. 1150 BC: villages in the hills (opening film + Play to c. 1000 BC, build/narration_jews_1150.py) ----------
# No big fact boxes (events) yet: this stop is told by its two films. The map is the end state of the
# 1207 BC Play (data/eras/1150bc.json, built in make_data.py). David's kingdom gets no border.
STOP1150 = {
 "story":"jews","year":-1150,"label":"c. 1150 BC","title":"Villages in the hills",
 "keyObjects":["israelp","hills","shiloh","philistines","ashdod","ekron","gath","jerusalem","telqasile","dor"],
 "transitionIn":{"text":"About 1150 BC. Egypt's empire is gone from Canaan. Philistine cities lie on the coast, Israelite villages in the hills, and Jewish tradition remembers this as the age of the Judges.",
   "title":"c. 1150 BC: villages, judges and the first kings","ambient":"desert","beats":NAR1150.clean(NAR1150.INTRO_BEATS)},
 "transitionOut":{"to":-1000,"text":"Next: the Philistine cities, Shiloh and the Judges, Saul and David. Tradition and archaeology are told side by side, and where scholars disagree, each view is given."},
 "events":[],
 "explore":{
  "key":["israelp","hills","shiloh","philistines","ashdod","ashkelon","ekron","gath","gaza","telqasile","dor","jerusalem"],
  "text":"Open each key place or people on the map to read its fact box. Unexplored ones glow; explored ones get a check. Your progress is saved on this device. When you are ready, press Play to move on to c. 1000 BC."},
 "play":{
  "to":-1000, "title":"From c. 1150 BC to c. 1000 BC",
  "intro":"Plays full screen like a short narrated film, with subtitles (CC). Pause, step back or forward, or change speed at any time. Stop whenever you like: it remembers your chapter.",
  "zoneObjects":{"philistia":"philistines","israel":"israelp"},
  "ambient":"desert",
  "beats":NAR1150.clean(NAR1150.PLAY)}
}


# ---------- c. 1000 BC: David and Solomon (Chapter 3: opening film + Play to c. 930 BC, build/narration_jews_1000.py) ----------
# The map is the end state of the c. 1150 BC Play plus dashed Ammon, Moab and Edom (data/eras/1000bc.json, make_data.py).
# No border for David or Solomon. The Play draws the split of c. 930 BC (ISRAEL north, JUDAH south) and ends on a teaser.
STOP1000 = {
 "story":"jews","year":-1000,"label":"c. 1000 BC","title":"David and Solomon: tradition and evidence",
 "keyObjects":["jerusalem","hebron","gibeon","motza","gezer","megiddo","hazor","nahas","rabbah","tyre","israelp","philistines"],
 "transitionIn":{"text":"About 1000 BC. No empire rules the land. Philistine cities hold the coast, Tyre trades across the sea, and in the Hebrew Bible David is king in Jerusalem.",
   "title":"c. 1000 BC: David, Solomon and the split","ambient":"desert","beats":NAR1000.clean(NAR1000.INTRO_BEATS)},
 "transitionOut":{"to":-930,"text":"Next: David's Jerusalem, his wars and heirs, Solomon's temple and gates, and the split into Israel and Judah. Tradition and archaeology are told side by side, and where scholars disagree, each view is given."},
 "events":[
  {"id":"gates","kicker":"Archaeology","title":"The six-chambered gates","date":"10th–9th century BC","cert":D,
   "text":"The Bible says Solomon built Hazor, Megiddo and Gezer. In the 1950s Yigael Yadin found city gates of the same plan at all three, each with six chambers, and called them Solomon's gates. Israel Finkelstein later moved them about a century down, to the kings of the northern kingdom. At Gezer, radiocarbon dates published in 2023 put the level with the gate back in the 10th century BC.",
   "why":"Was Solomon a great builder, as the Bible says? The gates are one of the main tests. They show planned building in these years, but not who ordered it, and Hazor and Megiddo are still argued over.",
   "claims":[["'Solomon built Hazor, Megiddo and Gezer' (1 Kings 9:15).",T,["bible"]],["Yadin identified the six-chambered gates at Hazor, Megiddo and Gezer as Solomonic.",A,["yadin1958"]],["Finkelstein's 'low chronology' dates these levels to the 9th century BC.",D,["fink1996"]],["Radiocarbon dates for Gezer Stratum 8, with the gate: built c. 998–957 BC, destroyed c. 969–940 BC (68% ranges). Similar gates are also found elsewhere, so the plan alone does not prove a single builder.",D,["webster2023"]]],
   "src":["yadin1958","fink1996","webster2023","bible"],"objects":["gezer","megiddo","hazor"],"focus":{"c":[35.2,32.45],"k":4.2},"hl":["gezer","megiddo","hazor"]},
  {"id":"copper","kicker":"The neighbours","title":"The copper of Edom","date":"c. 1100–850 BC","cert":A,
   "text":"After Egypt left Canaan, copper smelting in the Arabah valley did not stop. At Khirbet en-Nahas in Faynan and at Timna, huge slag heaps and radiocarbon dates show production on a large scale in the 11th to 9th centuries BC, run by people who mostly lived in tents.",
   "why":"Archaeologists look for stone palaces to find kingdoms. Edom's copper shows that a strong, organised society can leave few buildings. Some scholars call this the 'architectural bias', and it matters for how we judge David's kingdom too.",
   "claims":[["Large-scale smelting at Khirbet en-Nahas and Timna in the 11th–9th centuries BC, dated by radiocarbon.",A,["levy2014","benyosef2019"]],["That this was run by an Edomite polity of largely nomadic people, and what that says about early kingdoms, is debated.",D,["benyosef2019"]],["The Bible says David put garrisons in Edom (2 Samuel 8:14).",T,["bible"]]],
   "src":["levy2014","benyosef2019"],"objects":["nahas","timna","edom","bozrah"],"focus":{"c":[35.3,30.4],"k":5},"hl":["nahas","timna","bozrah"]},
  {"id":"temple","kicker":"Jewish tradition","title":"The temple: text and parallels","date":"Tradition: 10th century BC","cert":T,
   "text":"The Book of Kings describes Solomon's temple in detail: a porch, a great hall and an inner room, the Holy of Holies, where the Ark of the Covenant stood. No trace of it has been found, because the Temple Mount is a holy place and cannot be excavated. But temples of the same three-part plan are known, most closely at Ain Dara in Syria, and a small temple of this age was found at Tel Motza, just outside Jerusalem.",
   "why":"The Temple in Jerusalem became the centre of Jewish worship. After it was destroyed, prayer took its place: Jews still face Jerusalem when they pray, as Solomon asks in his dedication prayer.",
   "claims":[["The building and dedication of the temple: 1 Kings 6–8.",T,["bible"]],["Ain Dara has a three-part plan like the one described in 1 Kings 6.",A,["monson2000"]],["Tel Motza: an Iron IIA temple with altar and courtyard, late 10th–early 9th century BC.",A,["kisilevitz2015"]],["A stone shrine model from Khirbet Qeiyafa has a recessed doorframe that some compare with 1 Kings 6:31.",D,["garfinkelmumcuoglu2016"]],["Facing Jerusalem in prayer, from 1 Kings 8.",T,["berakhot30a"]]],
   "src":["bible","monson2000","kisilevitz2015","garfinkelmumcuoglu2016","berakhot30a"],"objects":["jerusalem","motza","aindara","qeiyafa"],"focus":{"c":[35.2,31.8],"k":9},"hl":["jerusalem","motza"]},
  {"id":"monarchy","kicker":"The big question","title":"Was there a united monarchy?","date":"c. 1000–930 BC","cert":D,
   "text":"The Bible tells of one kingdom of all Israel under Saul, David and Solomon, which split in two after Solomon. Some historians, such as Israel Finkelstein, think the north and Judah were separate from the start, and that the 'united monarchy' is a later ideal. Others, such as Amihai Mazar, think a modest kingdom ruled from Jerusalem is the best reading of the evidence.",
   "why":"A 9th-century BC stele from Tel Dan names the 'House of David', so a dynasty named after David ruled Judah within about a century and a half. How large and how rich that kingdom was at the start is still open.",
   "claims":[["One kingdom under David and Solomon, split after Solomon: 2 Samuel to 1 Kings 12.",T,["bible"]],["The north and Judah were separate from the start; the united monarchy is a later ideal.",D,["finksilb2006","fink2013"]],["A modest united kingdom in the 10th century BC is the best reading of the evidence.",D,["mazar2010"]],["The Tel Dan stele names the 'House of David' (9th century BC).",A,["biran1993","biran1995"]]],
   "src":["finksilb2006","mazar2010","biran1995","bible"],"objects":["jerusalem","shechem","dan","israelp"],"focus":{"c":[35.3,32.3],"k":4},"hl":["jerusalem","shechem","dan"]},
  {"id":"mesha","kicker":"A neighbour's voice","title":"The Mesha stele","date":"c. 840 BC","cert":A,
   "text":"About a century after the split, Mesha, king of Moab, set up a stone at Dibon boasting that he had thrown off the rule of Israel's king Omri and his son. It was found in 1868 and is now in the Louvre. In a broken line near the end, André Lemaire proposed reading 'House of David'. Others read a king's name, Balak, instead.",
   "why":"It is Moab's own side of a story the Bible tells too (2 Kings 3). If the reading is right, it is a second 9th-century witness to a dynasty named after David.",
   "claims":[["Mesha of Moab's inscription from Dibon, naming Omri king of Israel.",A,["lemaire1994","langlois2019"]],["Line 31 reads 'House of David': hypothetical but the most probable reading.",D,["lemaire1994","langlois2019"]],["Line 31 cannot read 'House of David'; the name may be Balak.",D,["finknaamanromer2019"]],["Mesha's revolt against Israel: 2 Kings 3.",T,["bible"]]],
   "src":["lemaire1994","langlois2019","finknaamanromer2019","bible"],"objects":["dibon","moab"],"focus":{"c":[35.78,31.5],"k":8},"hl":["dibon"]}
 ],
 "explore":{
  "key":["jerusalem","hebron","gibeon","tyre","rabbah","nahas","gezer","megiddo","hazor","motza","philistines","israelp"],
  "text":"Open each key place or people on the map to read its fact box. Unexplored ones glow; explored ones get a check. Your progress is saved on this device. When you are ready, press Play to move on to c. 930 BC."},
 "play":{
  "to":-930, "title":"From c. 1000 BC to c. 930 BC",
  "intro":"Plays full screen like a short narrated film, with subtitles (CC). Pause, step back or forward, or change speed at any time. Stop whenever you like: it remembers your chapter.",
  "zoneObjects":{"philistia":"philistines","israel":"israelp","ammon":"ammon","moab":"moab","edom":"edom","judah":"judah"},
  "ambient":"desert",
  "beats":NAR1000.clean(NAR1000.PLAY)}
}

STOP930 = {
 "story":"jews","year":-930,"label":"c. 930 BC","title":"Israel and Judah",
 "keyObjects":["israelk","judah","samaria","jerusalem","jezreelcity","tirzah","dan","damascus","qarqar","dibon","kalhu","tyre"],
 "transitionIn":{"text":"About 930 BC. Two kingdoms share the hills: Israel in the north and Judah in the south, ruled from Jerusalem by the House of David. Egypt's Shoshenq has passed through, and Assyria is about to march west.",
   "title":"c. 930 BC: Israel and Judah","ambient":"desert","beats":NAR930.clean(NAR930.INTRO_BEATS)},
 "transitionOut":{"to":-722,"text":"Next: wars between the two kingdoms, the House of Omri and its capital Samaria, Elijah in tradition, Ahab at Qarqar, Mesha's revolt in Moab, and Jehu and Hazael. Here, for the first time, Israel's neighbours name its kings in their own inscriptions."},
 "events":[
  {"id":"shoshenq","kicker":"Egypt's side","title":"The pharaoh's list at Karnak","date":"c. 925 BC","cert":A,
   "text":"On the Bubastite Portal at Karnak, Shoshenq I, founder of Egypt's 22nd Dynasty, carved a long list of places in the land. Many names can be read: Megiddo, Taanach, Beth-shean, Gibeon, Mahanaim and Penuel across the Jordan, and many small places in the Negev. Jerusalem is not among the names that survive. A fragment of a stone with his name was found at Megiddo.",
   "why":"The Bible says Shishak came up against Jerusalem and took the temple treasures (1 Kings 14:25–26). Karnak is Egypt's own record of a campaign the Bible also tells, so the two can be read side by side.",
   "claims":[["Shoshenq I's list at Karnak names Megiddo, Taanach, Beth-shean, Gibeon and places east of the Jordan and in the Negev.",A,["wilson2005","kitchen1996"]],["Jerusalem is not among the names that survive; the list is partly damaged.",A,["wilson2005"]],["Rehoboam paid tribute and Jerusalem was spared.",D,["kitchen1996"]],["Shishak takes the treasures of the temple: 1 Kings 14:25–26.",T,["bible"]],["A Shoshenq fragment was found at Megiddo in 1925–26; perhaps from a building inscription rather than a stele.",A,["bendorfink2023"]]],
   "src":["wilson2005","kitchen1996","bendorfink2023","bible"],"objects":["thebes","megiddo","gibeon","bethshean","negev"],"focus":{"c":[34.0,29.5],"k":1.9},"hl":["thebes","megiddo","gibeon"]},
  {"id":"samaria","kicker":"Archaeology","title":"Samaria, Omri's capital","date":"c. 880–841 BC","cert":A,
   "text":"Omri moved Israel's capital from Tirzah to a new site, Samaria. On the summit, excavators found a royal compound with walls of finely cut stone and, nearby, carved ivories in Phoenician style. Jezreel, above the great valley, had a large enclosure with a moat. Israel Finkelstein groups these sites as 'Omride architecture'.",
   "why":"The Bible gives Omri only a few verses and judges him harshly. Archaeology and his neighbours show a strong king: Assyria called Israel 'the House of Omri', and Moab remembered his rule.",
   "claims":[["Omri bought the hill of Samaria from Shemer for two talents of silver: 1 Kings 16:24.",T,["bible"]],["The first palace on the summit (Building Period I) is Omride.",D,["franklin2004","fink2000"]],["Phoenician-style ivories from Samaria.",A,["crowfoot1938"]],["The royal enclosure at Jezreel: 9th century BC, short-lived.",A,["ussishkin1997"]],["Assyrian texts call Israel the House of Omri.",A,["grayson1996"]]],
   "src":["franklin2004","fink2000","crowfoot1938","ussishkin1997","grayson1996","bible"],"objects":["samaria","jezreelcity","tirzah","megiddo"],"focus":{"c":[35.27,32.42],"k":9},"hl":["samaria","jezreelcity","tirzah"]},
  {"id":"elijah","kicker":"Jewish tradition","title":"Elijah the prophet","date":"Tradition: 9th century BC","cert":T,
   "text":"In the Book of Kings, Elijah confronts Ahab and Jezebel. He calls the people to choose on Mount Carmel, hears a 'still small voice' at Horeb, condemns the killing of Naboth at Jezreel, and is taken to heaven in a chariot of fire. The prophet Malachi says God will send Elijah before the great day of the Lord.",
   "why":"Elijah lives on in Jewish practice: a cup of wine is poured for him at every Passover Seder, a chair is set for him at every circumcision, and the words of the people on Carmel, 'The Lord, He is God', close the Yom Kippur prayers. Many scholars think the stories took their present shape long after Ahab's time.",
   "claims":[["Elijah's stories: 1 Kings 17–19, 21 and 2 Kings 1–2; Malachi 3:23.",T,["bible"]],["The cup of Elijah at the Passover Seder.",A,["ejelijahcup"]],["The chair of Elijah at circumcision.",A,["jeelijahchair"]],["'The Lord, He is God' said seven times at the end of Yom Kippur.",A,["neilah623"]],["The Elijah–Elisha stories were added to Kings in the exilic and post-exilic periods.",D,["otto2003"]]],
   "src":["bible","ejelijahcup","jeelijahchair","neilah623","otto2003"],"objects":["carmel","zarephath","jezreelcity","samaria"],"focus":{"c":[35.2,32.9],"k":6},"hl":["carmel","zarephath","jezreelcity"]},
  {"id":"qarqar","kicker":"Assyria's side","title":"Qarqar, 853 BC: Ahab on an Assyrian stone","date":"853 BC","cert":A,
   "text":"Shalmaneser III of Assyria marched west and met a coalition of twelve kings at Qarqar on the Orontes. His Kurkh Monolith lists them: Hadad-ezer of Damascus, Irhuleni of Hamath, and 'Ahab the Israelite' with 2,000 chariots and 10,000 soldiers, as well as troops from Egypt and Byblos, and Gindibu the Arab with 1,000 camels. Shalmaneser claims a great victory, but he did not take Damascus or Hamath and fought the same alliance again in 849, 848 and 845 BC.",
   "why":"It is one of the earliest records outside the Bible to name a king of Israel, and it shows Israel as a major power of its day. The Bible does not mention the battle.",
   "claims":[["Kurkh Monolith: the coalition at Qarqar, with Ahab the Israelite, 2,000 chariots and 10,000 troops.",A,["grayson1996","bmkurkh"]],["The 2,000 chariots may be a scribal error, perhaps for 200.",D,["naaman1976"]],["Gindibu the Arab, the earliest mention of Arabs.",A,["ephal1982"]],["Qarqar was a check on Assyria; Shalmaneser came back in 849, 848 and 845 BC.",D,["yamada2000"]],["Ahab dies in battle at Ramoth-gilead: 1 Kings 22.",T,["bible"]]],
   "src":["grayson1996","bmkurkh","yamada2000","naaman1976","ephal1982","bible"],"objects":["qarqar","hamath","kurkh","damascus","byblos"],"focus":{"c":[37.5,35.6],"k":3.2},"hl":["qarqar","hamath","kurkh"]},
  {"id":"mesharevolt","kicker":"A neighbour's voice","title":"Mesha's revolt: Moab's side","date":"c. 850–840 BC","cert":A,
   "text":"Mesha of Moab wrote that Omri had oppressed Moab 'for many days' and that he himself had beaten Omri's son. He took Ataroth, where 'the men of Gad' had lived from of old, and Nebo, from where he carried off 'the vessels of Yahweh'. He also took Medeba and Yahaz. The Bible tells of a campaign by Israel, Judah and Edom against him, which ended when Mesha offered his eldest son on the wall.",
   "why":"It is one of the oldest mentions of the name of Israel's God outside the Bible, and a rare case where both sides of a war speak. Mesha boasts that 'Israel has perished forever'; it had not.",
   "claims":[["Omri, his son, Ataroth and the men of Gad, Nebo and the vessels of Yahweh, Medeba: the Mesha stele.",A,["dearman1989","louvremesha"]],["Which son of Omri is meant, and how Mesha's 40 years fit, is debated.",D,["dearman1989"]],["Mesha the sheep breeder, the campaign of three kings and the end on the wall: 2 Kings 3.",T,["bible"]],["Found at Dhiban in 1868; broken in 1869; restored from a squeeze.",A,["louvremesha","dearman1989"]]],
   "src":["dearman1989","louvremesha","bible"],"objects":["dibon","ataroth","nebo","medeba","moab"],"focus":{"c":[35.75,31.6],"k":8},"hl":["dibon","ataroth","nebo","medeba"]},
  {"id":"teldanjehu","kicker":"Aram's side","title":"Who killed the two kings?","date":"841 BC","cert":D,
   "text":"The Bible says the army commander Jehu killed Joram, king of Israel, and Ahaziah, king of Judah, at Jezreel, and ended the House of Omri. A broken Aramaic stele from Tel Dan, very likely set up by Hazael of Damascus, has its king claim that he killed '[Jo]ram son of [Ahab], king of Israel' and '[Ahaz]iah ... of the House of David'. The names are partly restored.",
   "why":"Two sources, two killers. William Schniedewind suggests both may be partly right: Jehu may have acted as Hazael's ally. Either way, the stele is the clearest early text naming the House of David.",
   "claims":[["Jehu kills Joram and Ahaziah: 2 Kings 9.",T,["bible"]],["The Tel Dan stele: a king of Aram claims to have killed the king of Israel and the king of the House of David.",A,["biran1995"]],["The names Joram and Ahaziah are restored.",D,["biran1995","schniedewind1996"]],["Hazael as author; Jehu as his agent.",D,["schniedewind1996"]]],
   "src":["biran1995","schniedewind1996","bible"],"objects":["dan","jezreelcity","damascus","aramdamascus"],"focus":{"c":[35.6,32.9],"k":6},"hl":["dan","jezreelcity","damascus"]},
  {"id":"blackobelisk","kicker":"Assyria's side","title":"The Black Obelisk: Jehu's tribute","date":"841 BC","cert":A,
   "text":"In 841 BC Shalmaneser III marched west again, shut Hazael up in Damascus, and took tribute from Tyre, Sidon and 'Jehu of the house of Omri'. On his Black Obelisk from Nimrud, a panel shows a man kneeling before the king, with the words 'tribute of Jehu ... silver, gold, a gold bowl ... tin ... spears'.",
   "why":"It shows Israel's new place in the world: a small kingdom paying a great empire. And Assyria still called Israel 'the house of Omri', though Jehu had just ended Omri's line.",
   "claims":[["Year 18 (841 BC): Hazael at Damascus, and tribute of Tyre, Sidon and Jehu.",A,["grayson1996"]],["The Black Obelisk epigraph of Jehu's tribute; now in the British Museum.",A,["grayson1996","bmblackobelisk"]],["Whether the kneeling man is Jehu himself or his envoy is not certain.",D,["bmblackobelisk"]],["Jehu's coup ends the House of Omri: 2 Kings 9–10.",T,["bible"]]],
   "src":["grayson1996","bmblackobelisk","bible"],"objects":["kalhu","samaria","damascus","tyre"],"focus":{"c":[39.5,34.5],"k":2.2},"hl":["kalhu","samaria","damascus"]},
  {"id":"ajrud","kicker":"Archaeology","title":"Yahweh and his Asherah","date":"c. 800 BC","cert":D,
   "text":"At Kuntillet Ajrud, a way station in the Sinai from about 800 BC, travellers left inscriptions on large jars and on plaster. Some bless 'by Yahweh of Samaria and his Asherah', others 'by Yahweh of Teman and his Asherah'.",
   "why":"They show that worship of Israel's God was more varied than the Bible's ideal, in the same century as Elijah and the prophets who fought against Baal. What 'his Asherah' meant, a goddess or a sacred symbol, is debated.",
   "claims":[["Blessings by 'Yahweh of Samaria and his Asherah' and 'Yahweh of Teman and his Asherah', c. 800 BC.",A,["meshel2012"]],["Whether Asherah here is a goddess or a cult object is debated.",D,["meshel2012","smith2002"]]],
   "src":["meshel2012","smith2002"],"objects":["ajrud","samaria"],"focus":{"c":[34.8,31.2],"k":3.4},"hl":["ajrud","samaria"]}
 ],
 "explore":{
  "key":["israelk","judah","samaria","jerusalem","jezreelcity","tirzah","dan","damascus","qarqar","dibon","kalhu","tyre"],
  "text":"Open each key place or people on the map to read its fact box. Unexplored ones glow; explored ones get a check. Your progress is saved on this device. When you are ready, press Play to follow the story to 841 BC."},
 "play":{
  "to":-722, "title":"From c. 930 BC to 841 BC",
  "intro":"Plays full screen like a short narrated film, with subtitles (CC). Pause, step back or forward, or change speed at any time. Stop whenever you like: it remembers your chapter.",
  "zoneObjects":{"philistia":"philistines","israel":"israelk","ammon":"ammon","moab":"moab","edom":"edom","judah":"judah","aram":"aramdamascus"},
  "ambient":"desert",
  "beats":NAR930.clean(NAR930.PLAY)}
}

STOP722 = {
 "story":"jews","year":-722,"label":"722 BC","title":"Fall of Samaria",
 "keyObjects":["israelk","judah","samaria","jerusalem","damascus","assyria","rimah","bethel","hazor","dursharrukin","gozan","gerizim"],
 "transitionIn":{"text":"722 BC. Samaria, the capital of Israel, is under Assyrian siege. To see how it came to this, the chapter goes back to 841 BC, where Chapter 4 ended.",
   "title":"722 BC: Fall of Samaria","ambient":"desert","beats":NAR722.clean(NAR722.INTRO_BEATS)},
 "transitionOut":{"to":-701,"text":"Next: Aram's pressure and Joash on an Assyrian stele, Jeroboam II's Israel and the prophets Amos and Hosea, Tiglath-pileser III, the fall of Damascus and Galilee, the siege and fall of Samaria, the exile of its people, and Judah left alone."},
 "events":[
  {"id":"rimahjoash","kicker":"Assyria's side","title":"Joash the Samarian","date":"c. 796 BC","cert":A,
   "text":"Around 796 BC Adad-nirari III of Assyria marched west and took a great tribute from the king of Damascus. A stele found at Tell al-Rimah in northern Iraq in 1967 lists another king who paid: 'Joash the Samarian'. He is Jehu's grandson, the king who, says the Bible, won back Israel's towns from Aram.",
   "why":"It ties a king of the Bible to an Assyrian text, and shows the pattern of the century: when Assyria struck Damascus, Israel could breathe again. Assyria now names Israel after its capital, Samaria.",
   "claims":[["Tribute of Joash (Iu'asu) the Samarian on the Tell al-Rimah stele of Adad-nirari III.",A,["page1968","grayson1996"]],["Hazael and his son oppress Israel; a 'deliverer'; Joash wins back the towns: 2 Kings 13.",T,["bible"]],["Assyria's campaigns against Damascus gave Israel room to recover.",D,["fink2013","grayson1996"]]],
   "src":["page1968","grayson1996","fink2013","bible"],"objects":["rimah","damascus","samaria","aramdamascus"],"focus":{"c":[39.0,34.6],"k":2.2},"hl":["rimah","damascus","samaria"]},
  {"id":"jeroboam2","kicker":"Archaeology","title":"Jeroboam II: oil, wine and a lion seal","date":"c. 788–747 BC","cert":D,
   "text":"The Bible gives Jeroboam II 41 years and a border from Lebo-hamath to the Dead Sea, in just a few verses. At Samaria, the Harvard expedition found over a hundred inscribed sherds, the Samaria Ostraca, recording wine and oil sent to the capital. At Megiddo in 1904, a jasper seal with a roaring lion was found, reading 'belonging to Shema, servant of Jeroboam'.",
   "why":"Israel Finkelstein sees these years as the peak of the northern kingdom. The ostraca's personal names, some built with Yahu and some with Baal, give a rare glimpse of ordinary faith.",
   "claims":[["Jeroboam II reigns 41 years and restores the border: 2 Kings 14:23–29.",T,["bible"]],["The Samaria Ostraca record deliveries of wine and oil; names with Yahu and Baal.",A,["reisner1924"]],["The ostraca date to the first half of the 8th century BC.",D,["fink2013","reisner1924"]],["The Shema seal, found in 1904, is lost and known from casts; its 'Jeroboam' is probably Jeroboam II.",D,["ussishkin1994"]],["The 8th century BC as the peak of the northern kingdom.",D,["fink2013"]]],
   "src":["reisner1924","ussishkin1994","fink2013","bible"],"objects":["samaria","megiddo","israelk"],"focus":{"c":[35.2,32.45],"k":10},"hl":["samaria","megiddo"]},
  {"id":"amoshosea","kicker":"Jewish tradition","title":"Amos and Hosea","date":"Tradition: c. 760–725 BC","cert":T,
   "text":"Amos, a herdsman from Tekoa in Judah, speaks at the royal shrine of Bethel against those who 'lie on beds of ivory' while the poor are crushed: 'Let justice roll down like waters'. Hosea, from the north, speaks of Israel as an unfaithful wife whom God still loves. Their books are among the oldest of the prophets.",
   "why":"Their words, against wealth without justice and faith without loyalty, became part of the Hebrew Bible and are still read in synagogues today. Ivory inlays like those Amos condemns were found at Samaria.",
   "claims":[["Amos at Bethel; beds of ivory; 'Let justice roll down': Amos 1:1; 5:24; 6:4–6; 7:10–15.",T,["bible"]],["Hosea's marriage and God's love: Hosea 1–3; 11.",T,["bible"]],["Ivory furniture inlays from Samaria.",A,["crowfoot1938"]],["Yadin linked a destruction at Hazor with the earthquake of Amos 1:1.",D,["yadin1972"]]],
   "src":["bible","crowfoot1938","yadin1972"],"objects":["bethel","tekoa","samaria","hazor"],"focus":{"c":[35.3,32.2],"k":7},"hl":["bethel","tekoa","samaria"]},
  {"id":"tiglath","kicker":"Assyria's side","title":"Tiglath-pileser III names three kings","date":"745–727 BC","cert":A,
   "text":"Tiglath-pileser III made the conquered lands into provinces and moved whole peoples. His annals and lists of tribute name Menahem of Samaria, Jehoahaz (Ahaz) of Judah, and Pekah, whom 'they overthrew', and Hoshea, whom 'I set as king over them'. In Babylon he ruled under the name Pulu, the 'Pul' of the Bible.",
   "why":"For the first time, Assyrian texts and the Book of Kings can be read almost year by year side by side. Each king of Israel and Judah had to choose between paying Assyria and resisting it.",
   "claims":[["Menahem of Samaria, Jehoahaz of Judah, Pekah and Hoshea in Tiglath-pileser III's inscriptions.",A,["tadmor2011"]],["Tiglath-pileser III's accession in 745 BC.",A,["millard1994","tadmor2011"]],["His policy of provinces and two-way deportations.",A,["tadmor2011","oded1979"]],["Menahem pays Pul a thousand talents; Ahaz: 'I am your servant and your son': 2 Kings 15:19–20; 16:7–8.",T,["bible"]],["Rezin and Pekah against Ahaz; the sign of Immanuel: Isaiah 7.",T,["bible"]]],
   "src":["tadmor2011","millard1994","oded1979","bible"],"objects":["kalhu","samaria","jerusalem","damascus"],"focus":{"c":[39.0,34.2],"k":2.1},"hl":["kalhu","samaria","jerusalem"]},
  {"id":"galilee732","kicker":"Archaeology","title":"732 BC: Damascus, Galilee and Hazor","date":"733–732 BC","cert":A,
   "text":"After campaigns 'to Damascus' in 733 and 732 BC, Tiglath-pileser took Damascus and made Aram a province. Israel lost Galilee and Gilead. At Hazor, the city of this time ended in fire under a thick layer of ash. The Bible names the towns taken, from Ijon to Hazor, and says their people were carried off to Assyria.",
   "why":"Within a few years the northern kingdom shrank to the hills around Samaria. It was the first great deportation of Israelites.",
   "claims":[["Campaigns 'to Damascus' in 733 and 732 BC.",A,["millard1994"]],["Damascus becomes an Assyrian province.",A,["tadmor2011"]],["Hazor Stratum V destroyed by fire, with a thick ash layer, in 732 BC.",A,["yadin1972"]],["Ijon, Abel-beth-maacah, Hazor, Gilead, Galilee and Naphtali taken and deported: 2 Kings 15:29.",T,["bible"]]],
   "src":["millard1994","tadmor2011","yadin1972","bible"],"objects":["damascus","hazor","aramdamascus","israelk"],"focus":{"c":[35.9,33.0],"k":5.5},"hl":["damascus","hazor"]},
  {"id":"samariafall","kicker":"Two kings, one city","title":"Who took Samaria?","date":"722–720 BC","cert":D,
   "text":"The Bible says Shalmaneser V besieged Samaria for three years and took it. A Babylonian chronicle says only that Shalmaneser 'ravaged Shamara'in'. His successor Sargon II claims the conquest for himself: '27,290 people' in his palace at Khorsabad, '27,280' and 200 chariots on a prism from Nimrud. In 720 BC Samaria joined a revolt led by Hamath, which Sargon crushed at Qarqar.",
   "why":"Hayim Tadmor proposed that Samaria was taken twice, by Shalmaneser in 722 and again by Sargon in 720 BC, and many follow him. On the summit itself, Ron Tappy found little sign of a great burning.",
   "claims":[["The siege of three years: 2 Kings 17:5–6; 18:9–10.",T,["bible"]],["'He ravaged Shamara'in': Babylonian Chronicle 1.",A,["grayson1975"]],["Sargon's Khorsabad inscriptions: Samaria conquered, 27,290 deported, 50 chariots.",A,["fuchs1994","frame2021"]],["The Nimrud Prism: 27,280 deported and 200 chariots; Samaria resettled 'greater than before'.",A,["gadd1954"]],["The revolt of 720 BC crushed at Qarqar.",A,["frame2021","naaman1990"]],["Two conquests, 722 and 720 BC.",D,["tadmor1958","becking1992"]],["No clear destruction layer on the summit.",D,["tappy2001"]]],
   "src":["grayson1975","fuchs1994","frame2021","gadd1954","tadmor1958","becking1992","naaman1990","tappy2001","bible"],"objects":["samaria","dursharrukin","kalhu","qarqar"],"focus":{"c":[39.0,34.6],"k":2.1},"hl":["samaria","dursharrukin","qarqar"]},
  {"id":"deportations","kicker":"Exile","title":"Carried off: Israel in Assyria","date":"732–c. 700 BC","cert":A,
   "text":"The Bible says Israel was settled 'in Halah, on the Habor, the river of Gozan, and in the cities of the Medes'. Assyrian documents bear it out: Israelite names, built with the name of Israel's God, appear in the following decades at Gozan, Kalhu and other cities, and a unit of Samarian charioteers served in the Assyrian army.",
   "why":"Scholars think many Israelites stayed on the land; Assyria's own figure covers only part of the population. But those who were taken away mostly vanish from history, and that became the tradition of the ten lost tribes.",
   "claims":[["Halah, Habor, Gozan and the cities of the Medes: 2 Kings 17:6.",T,["bible"]],["Israelite names in Assyrian documents after 720 BC.",A,["becking1992","younger1998","oded1979"]],["Samarian charioteers in the Nimrud Horse Lists.",A,["dalley1985"]],["The deportations were partial; many stayed.",D,["younger1998"]]],
   "src":["becking1992","younger1998","oded1979","dalley1985","bible"],"objects":["gozan","media","kalhu"],"focus":{"c":[42.0,35.6],"k":1.9},"hl":["gozan","media","kalhu"]},
  {"id":"samaritans","kicker":"Two traditions","title":"The Samaritans and the ten tribes","date":"After 720 BC","cert":T,
   "text":"The Bible says Assyria brought people from Babylon, Cuthah, Hamath and other places to Samaria, and that they learned to fear the God of the land from a priest at Bethel. Later Jewish writings call the Samaritans 'Kutim'. The Samaritans tell a different story: they are Israelites who never left, keepers of the Torah on Mount Gerizim. A small community still lives there today.",
   "why":"Jewish tradition remembers the exiles as the ten lost tribes. Rabbi Akiva taught in the Mishnah that they would not return; others hoped they would. The same events gave rise to two traditions that still live.",
   "claims":[["Settlers from Babylon, Cuthah, Avva, Hamath and Sepharvaim; the priest at Bethel: 2 Kings 17:24–28.",T,["bible"]],["Sargon settled conquered peoples, and later Arabs, in Samaria.",A,["frame2021"]],["Samaritan self-understanding; 'Kutim'; Mount Gerizim; the community today.",A,["pummer2016"]],["Rabbi Akiva: the ten tribes will not return (Mishnah Sanhedrin 10:3).",T,["mishnahsanh"]],["Traditions of the ten lost tribes.",T,["je1906lost"]]],
   "src":["pummer2016","frame2021","mishnahsanh","je1906lost","bible"],"objects":["gerizim","cuthah","bethel","samaria"],"focus":{"c":[39.5,33.0],"k":2.0},"hl":["gerizim","cuthah","samaria"]},
  {"id":"jerusalemgrows","kicker":"Archaeology","title":"Jerusalem grows","date":"Late 8th century BC","cert":D,
   "text":"In the late 8th century BC Jerusalem spread from the old City of David onto the western hill and grew several times over. Magen Broshi and Israel Finkelstein linked the growth with refugees from the fallen north. Nadav Na'aman argues it had other causes and began later.",
   "why":"Whatever its cause, Jerusalem became Judah's great city just as Israel disappeared, and the traditions of the north, carried south, became part of Judah's story.",
   "claims":[["Jerusalem's growth onto the western hill, late 8th century BC.",A,["broshi1992","naaman2007"]],["Refugees from the north as the cause.",D,["broshi1992"]],["Na'aman's doubts.",D,["naaman2007"]],["Hezekiah invites Ephraim and Manasseh to the Passover: 2 Chronicles 30.",T,["bible"]]],
   "src":["broshi1992","naaman2007","bible"],"objects":["jerusalem","judah"],"focus":{"c":[35.2,31.75],"k":12},"hl":["jerusalem"]}
 ],
 "explore":{
  "key":["israelk","judah","samaria","jerusalem","damascus","assyria","rimah","bethel","hazor","dursharrukin","gozan","gerizim"],
  "text":"Open each key place or people on the map to read its fact box. Unexplored ones glow; explored ones get a check. Your progress is saved on this device. When you are ready, press Play to follow the story from 841 BC to the fall of Samaria."},
 "play":{
  "to":-701, "title":"From 841 BC to 720 BC",
  "intro":"Plays full screen like a short narrated film, with subtitles (CC). Pause, step back or forward, or change speed at any time. Stop whenever you like: it remembers your chapter.",
  "zoneObjects":{"philistia":"philistines","israel":"israelk","ammon":"ammon","moab":"moab","edom":"edom","judah":"judah","aram":"aramdamascus","assyria":"assyria"},
  "ambient":"desert",
  "beats":NAR722.clean(NAR722.PLAY)}
}
