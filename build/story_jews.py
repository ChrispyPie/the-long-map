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
  {"year":-1207,"label":"1207 BC","title":"Israel is named","era":"data/eras/1207bc.json","file":"data/stories/jews/1207bc.json"},
  {"year":-1150,"label":"c. 1150 BC","title":"Villages in the hills",
   "soon":{"title":"Villages in the hills","text":"Next chapter coming soon. The transition you just watched brings the map to about 1150 BC: Egypt's empire in Canaan is ending, the Philistines have settled on the southern coast, and the hill villages of early Israel are growing."}},
  {"year":-1000,"label":"c. 1000 BC","title":"David and Solomon: tradition and evidence"},
  {"year":-930,"label":"c. 930 BC","title":"Israel and Judah"},
  {"year":-722,"label":"722 BC","title":"Assyria takes Samaria"},
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
 "transitionIn":"The first chapter of the Jewish story on this map. The great powers are Egypt, Hatti, Assyria and Babylon. Israel is small, and new.",
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
   "why":"For Jews, the Exodus is the founding memory: the story of becoming a free people bound by a covenant with God. It is retold every year at the Passover Seder, and it shapes prayer and law: 'you shall not wrong a stranger, for you were strangers in the land of Egypt' (Exodus 22:20).",
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
PHILISTIA = [[34.38,31.38],[34.52,31.66],[34.63,31.86],[34.92,31.86],[34.98,31.62],[34.6,31.28],[34.38,31.38]]
HIGHLANDS = [[34.98,32.55],[35.42,32.55],[35.55,32.15],[35.5,31.6],[35.25,31.35],[34.98,31.42],[34.92,31.9],[34.98,32.55]]
def cap(text, cert, src): return {"type":"caption","text":text,"cert":cert,"src":src}
# "scene" captions are scene-setting only: framed as "Imagine ...", they assert no new facts and carry no sources.
def scene(text): return {"type":"caption","text":text,"cert":"scene","src":[]}
STOP["play"] = {
 "to":-1150, "title":"From 1207 BC to c. 1150 BC",
 "intro":"Plays full screen like a short film, with subtitles (CC). Pause, step back or forward, change speed, or tap the picture to pause at any time.",
 "zoneObjects":{"philistia":"philistines","highlands":"israelp"},
 # sound (js/app.js, assets/sfx/README.md): the scene's ambient loop; battle, migration, border and year
 # steps get a default effect; "sfx" overrides it (null = none) and "sfxHold" (ms) lets it play out
 "ambient":"desert",
 "beats":[
  {"steps":[{"type":"year","to":-1200},{"type":"focus","c":[34.6,34.0],"k":1.5},
    cap("In the years after the Israel Stele, the world around Israel fell apart. Historians call it the Late Bronze Age collapse.",A,["cline","kuhrt"])]},
  {"steps":[{"type":"year","to":-1190},{"type":"focus","c":[35.9,35.3],"k":4.5,"hl":["ugarit"]},
    {"type":"battle","at":[35.78,35.60],"label":"Ugarit destroyed","cert":A,"sfxHold":2500,
     "arrows":[{"path":[[34.2,35.95],[35.0,35.75],[35.66,35.62]],"side":"enemy","cert":D}]},
    cap("Around 1190 BC Ugarit, a rich port on the Syrian coast, was destroyed. Its last letters tell of enemy ships off the coast.",A,["kaniewski","cline"])]},
  {"steps":[cap("The exact year and the attackers are debated; radiocarbon dates from nearby Tell Tweini point to about 1192–1190 BC.",D,["kaniewski"])]},
  {"steps":[{"type":"year","to":-1185},{"type":"focus","c":[35.0,38.0],"k":2.2,"hl":["carchemish"]},
    {"type":"border","fade":[{"zone":"hatti"}]},
    cap("Soon after, the Hittite court left Hattusa and the empire ended. Excavators found little sign of a final battle there. A branch of the royal family held on at Carchemish.",A,["seeher","bryce"])]},
  {"steps":[{"type":"year","to":-1180},{"type":"focus","c":[31.5,34.2],"k":1.35,"hl":["seapeoples"]},
    {"type":"migration","label":"By sea","cert":D,"sfxHold":2500,"path":[[25.8,37.2],[28.6,36.3],[31.6,36.0],[33.8,35.3],[35.2,34.9],[34.85,33.4],[34.35,32.1],[33.4,31.45],[32.2,31.55]]},
    {"type":"migration","label":"By land","cert":D,"path":[[28.2,38.4],[31.0,37.8],[34.0,37.1],[35.9,36.4],[36.2,34.7],[35.6,33.4]]},
    cap("'The foreign countries made a conspiracy in their islands … No land could stand before their arms, from Hatti … on.' So Ramesses III of Egypt had it written at Medinet Habu.",A,["edgerton","mhabu"])]},
  {"steps":[cap("Modern historians call them the 'Sea Peoples'. Their origins, numbers and part in the collapse are disputed; drought, earthquakes and broken trade also played a role.",D,["cline","kaniewski"])]},
  {"ambient":"river","steps":[{"type":"year","to":-1177},{"type":"focus","c":[33.2,31.9],"k":2.8},
    {"type":"battle","at":[35.25,33.1],"label":"Land battle in Djahy (place disputed)","cert":D,"sfxHold":3000,
     "arrows":[{"path":[[34.47,31.50],[34.75,32.3],[35.1,32.9]],"side":"egypt","cert":A},{"path":[[35.9,34.4],[35.5,33.7],[35.32,33.25]],"side":"enemy","cert":D}]},
    {"type":"battle","at":[31.95,31.42],"label":"Sea battle at the Nile mouths","cert":A,
     "arrows":[{"path":[[31.83,30.80],[31.9,31.25]],"side":"egypt","cert":A},{"path":[[33.0,31.75],[32.4,31.6],[32.05,31.48]],"side":"enemy","cert":D}]},
    cap("In his year 8 (c. 1177 BC in the usual dating), Ramesses III fought them on land in Djahy and at sea at the mouths of the Nile, and claimed victory. The Peleset, later called Philistines, were among them.",A,["edgerton","mhabu","cline"])]},
  {"steps":[cap("A later papyrus says he settled the defeated 'in strongholds'. Whether that means Egypt itself placed the Philistines in Canaan is disputed.",D,["harris","killebrew"])]},
  {"ambient":"desert","steps":[{"type":"year","to":-1170},{"type":"focus","c":[34.72,31.62],"k":7,"hl":["ashdod","ashkelon","ekron","gath","gaza"]},
    {"type":"border","add":[{"zone":"philistia","certainty":"unsure","label":"PHILISTIA","labelAt":[34.45,31.95],"coords":PHILISTIA}]},
    cap("On the southern coast, newcomers made Ashdod, Ashkelon, Ekron and Gath their own. Their pottery, cooking and weaving followed Aegean ways. Ancient DNA from Ashkelon shows people with southern European ancestry who soon mixed with locals.",A,["killebrew","yasur","feldman"])]},
  {"steps":[cap("When they arrived is debated: about 1175 BC in the usual view, or about 1135 BC in a lower dating.",D,["fink1995","yasur"])]},
  {"steps":[cap("The Hebrew Bible remembers the Philistines as coming from Caphtor (Amos 9:7), and as Israel's great rival in the days of the Judges, Samson and Saul.",T,["bible"])]},
  {"steps":[{"type":"year","to":-1160},{"type":"focus","c":[35.2,32.1],"k":4.2,"hl":["bethshean","gaza"]},
    {"type":"border","fade":[{"zone":"egypt","certainty":"unsure"}]},
    cap("Egypt kept garrisons in Canaan, such as Beth-Shean, for some decades more. Its rule there ended during the 12th century BC.",A,["weinstein","millek","morris"])]},
  {"steps":[cap("Whether the end came quickly or slowly, over 75 years or more, is debated.",D,["weinstein","millek"])]},
  {"steps":[{"type":"year","to":-1150},{"type":"focus","c":[35.2,31.95],"k":5.5,"hl":["hills","izbetsartah","shechem","jerusalem"]},
    {"type":"border","fade":[{"zone":"israel"}],"add":[{"zone":"highlands","certainty":"people","label":"ISRAEL","labelAt":[34.95,32.62],"coords":HIGHLANDS}]},
    cap("In the hills, small farming villages kept multiplying. Surveys count about 30 sites in the 13th century BC and about 250 by the end of Iron I, around 1000 BC.",A,["fink2013","faust"])]},
  {"steps":[scene("Imagine the hills at dawn: rock and scrub, smoke from cooking fires, flocks heading out to graze. Here is what excavations show.")]},
  {"steps":[{"type":"focus","c":[35.05,32.07],"k":9,"hl":["izbetsartah"]},
    cap("Most villages were small, often a few dozen households. Some of the earliest, such as Izbet Sartah, were laid out as a ring of houses around an open yard.",A,["finkelstein","faust"])]},
  {"steps":[cap("A typical home was a pillared house of three or four spaces around a central room. Animals and stores were probably kept on the ground floor, with living space above.",A,["faust","killebrew"])]},
  {"steps":[cap("Families stored grain in stone-lined pits and in large 'collared-rim' jars, and cut cisterns into the rock to keep winter rain for the dry summer. On steeper slopes, terraces held the soil.",A,["finkelstein","killebrew"])]},
  {"steps":[cap("They grew wheat and barley, tended olives and vines, and herded sheep and goats. Pig bones are rare at these hill sites.",A,["faust","fink2013"])]},
  {"steps":[{"type":"focus","c":[35.0,32.3],"k":4.4},
    cap("Down on the coast and the trade roads, the long-distance trade in copper, tin and fine goods that had fed the palaces had faltered.",A,["cline"])]},
  {"steps":[cap("For Israel, the world nearby had changed: the empire that named it in stone was withdrawing, the Philistines were new neighbours on the coast, and the hill villages kept growing.",A,["millek","killebrew","fink2013"])]},
  {"steps":[scene("Imagine a winter evening in one of these houses, rain on the roof and the animals shifting below. We do not know these villagers' names. Their houses, jars and terraces are what they left us.")]},
  {"steps":[cap("In Jewish tradition this is the age of the Judges, when 'there was no king in Israel' (Judges 21:25) and leaders rose tribe by tribe.",T,["bible"])]}
 ]
}
