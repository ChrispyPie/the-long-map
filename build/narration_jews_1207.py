"""Narration for the 1207 BC stop of the Story of the Jews: the opening film (transitionIn) and Play.

One beat = one spoken line = one mp3 in assets/narration/ (recorded with build/narrate.py).
Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (the film's own framing
lines: the title, how to read the labels, the choice, the hand-over to the map; shown in the subtitles
without a badge or sources).
Written for the ear: the spoken text has no digits or brackets. Subtitles show digits through the caption's
"display" field, made here from the DIGITS table. Bible references use English verse numbering; where the
Hebrew numbering differs it is given in the reference ("ref", shown with the sources).
"claims" split a line into sentences with their own label and sources (kept for review and tests).
"note" is a reading note for the narrator only and is not written to the data.
"""
import re
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
def cap(text, cert, src=(), claims=None, ref=None):
    c = {"type":"caption","text":text,"cert":cert,"src":list(src)}
    c["claims"] = claims if claims is not None else ([] if cert in (S,F) else [[text, cert, list(src)]])
    if ref: c["ref"] = ref
    return c
def fo(c,k,hl=None):
    x={"type":"focus","c":c,"k":k}
    if hl: x["hl"]=hl
    return x
def yr(y): return {"type":"year","to":y}
def B(text, cert, src=(), vis=(), amb=None, claims=None, note=None, ref=None):
    b={"steps":list(vis)+[cap(text,cert,src,claims,ref)]}
    if amb: b["ambient"]=amb
    if note: b["note"]=note
    return b

# ---------------- 1207 BC year intro (transitionIn) ----------------
INTRO = [
 B("This is The Long Map. Book One. The Story of the Jews.", F, vis=[fo([38.0,33.0],1.2)], amb="desert",
   note="Title card. Slow, warm. Leave a beat of silence before the next line."),
 B("We will follow one people across more than three thousand years. Every line tells you whether it is attested, disputed, or remembered in tradition.", F),
 B("The year is about twelve hundred and seven BC. Egypt is still a great empire, and its king is Merneptah, the thirteenth son of Ramesses the Second.", A, ["stele","kuhrt","morris"],
   vis=[yr(-1207), fo([31.5,28.5],2.0,["egypt","thebes","memphis"])], amb="river"),
 B("Egypt lived by its river. Each summer the Nile flooded, and left fresh black soil on the fields. From that soil came the wheat and barley that fed the land.", A, ["butzer"],
   vis=[fo([31.3,27.5],2.6,["nile"])], amb="river"),
 B("Scholars estimate that some three million people lived in Egypt then. Some think it was more. Nobody counted them for us.", D, ["butzer","oconnor"]),
 B("North-east of Egypt, along a desert road of forts called the Ways of Horus, lay Canaan. It was a land of small city-states, each with its own ruler, and Egypt was their overlord.", A, ["morris","killebrew"],
   vis=[fo([34.4,31.4],4.0,["wayshorus"])], amb="desert"),
 B("Egyptian soldiers kept watch at Gaza, on the coast, and at Beth-Shean, in the valley of the Jordan.", A, ["morris"],
   vis=[fo([35.0,31.9],5.5,["gaza","bethshean"])]),
 B("The Canaanites had long been at home here. A century earlier, the rulers of Jerusalem, Shechem, Gezer and Megiddo had written clay letters to Pharaoh, each asking for his favour.", A, ["moran","killebrew"],
   vis=[fo([35.1,32.2],5.5,["jerusalem","shechem","gezer","megiddo"])]),
 B("Their gods were old gods of the land. El was the father of the gods. Baal was the storm god, who brought the rain that the fields depended on.", A, ["smith2002","killebrew"]),
 B("Far to the north, the Hittites ruled from Hattusa, high in Anatolia. Two generations earlier, Egypt and Hatti had fought at Kadesh, and then made one of the oldest peace treaties we know.", A, ["bryce","bryce2006","beckman"],
   vis=[fo([35.0,37.5],1.6,["hattusa","kadesh"])]),
 B("To the east, beyond the Euphrates, Assyria had grown strong. Its king, Tukulti-Ninurta, had plundered Babylon. Around this very time he was killed in a revolt led by his own son.", A, ["grayson","chron","brinkman"],
   vis=[fo([43.8,34.3],2.8,["assur","babylon"])]),
 B("And in the hills of Canaan lived a people called Israel. We do not know how long they had been there. Most scholars place them in the central hill country.", D, ["hasel","fink2013"],
   vis=[fo([35.22,31.98],6.0,["hills"])], amb="desert",
   claims=[["And in the hills of Canaan lived a people called Israel.",A,["stele","hasel"]],
           ["We do not know how long they had been there.",D,["hasel"]],
           ["Most scholars place them in the central hill country.",D,["hasel","fink2013"]]]),
 B("Imagine those hills in the evening. Rock and scrub, a few small fields, and smoke rising where a family is cooking.", S),
 B("We know Israel's name because of a stone. In his fifth year, Merneptah set up a victory hymn in his temple at Thebes. It was carved on a slab of grey granite, more than three metres tall.", A, ["stele","kitchen4","petrie1897"],
   vis=[fo([32.64,25.7],4.0,["thebes"])], amb="river"),
 B("The stone was not new. His craftsmen carved the hymn on the back of an older stele of Amenhotep the Third. It runs to twenty-eight lines.", A, ["stele","petrie1897"]),
 B("Most of the hymn praises his victory over the Libyans. Only near the very end does it turn to Canaan.", A, ["stele","kitchen4"]),
 B("Canaan is plundered with every evil. Ashkelon is carried off. Gezer is seized. Yenoam is made non-existent. Israel is laid waste. Its seed is not.", A, ["stele","kitchen4"],
   vis=[fo([35.0,31.95],5.5,["ashkelon","gezer","yenoam","israelp"])],
   note="Quotation from the stele, standard translation. Read slower, with a small pause after each clause. No sound effect under it."),
 B("Ashkelon, Gezer and Yenoam are written with the sign for a foreign land. Israel is written with the sign for a people.", A, ["hasel"]),
 B("This is a royal hymn, made to praise the king. Historians debate how much of it describes real battles, and whether seed here means grain, or children.", D, ["hasel","kitchen4"]),
 B("On a wall at Karnak, battle scenes show the taking of Ashkelon. Some scholars think another scene there shows Israel. Others disagree.", D, ["yurco1990","rainey2001","abbas"],
   claims=[["On a wall at Karnak, battle scenes show the taking of Ashkelon.",A,["yurco1990","rainey2001"]],
           ["Some scholars think another scene there shows Israel. Others disagree.",D,["yurco1990","rainey2001"]]]),
 B("Either way, Merneptah's stone holds the oldest known mention of Israel outside the Bible.", A, ["stele","hasel"]),
 B("In Jewish tradition, the name is older still. The Torah tells how Jacob wrestled through the night, and was told, your name shall be Israel. His descendants became the children of Israel.", T, ["bible"],
   ref="Genesis 32:28 (32:29 in the Hebrew numbering)"),
 B("The Torah tells how they went down to Egypt and were enslaved there, how God brought them out under Moses, and how at Sinai they received the Torah before coming to Canaan.", T, ["bible"], ref="Exodus to Deuteronomy",
   vis=[fo([32.6,30.2],2.6,["piramesses","sinai"])], amb="desert"),
 B("No Egyptian text found so far names Moses or the Exodus. Scholars differ on how this memory relates to history.", D, ["killebrew","faust","finkelstein"]),
 B("For Jews, it is the founding memory, retold every year at Passover. It carries a lesson for every age. Do not wrong the stranger, for you were strangers in the land of Egypt.", T, ["bible"],
   ref="Exodus 22:21 (22:20 in the Hebrew numbering)"),
 B("Pharaoh's stone said that Israel was finished. More than three thousand two hundred years later, the name of Israel lives on in the Jewish people.", A, ["stele","hasel"],
   vis=[fo([35.0,31.95],5.5,["israelp"])]),
 B("Explore the map. When you are ready, press Play, and watch this old world begin to change.", F),
]

# ---------------- Play: 1207 BC to c. 1150 BC ----------------
SEA=[[25.8,37.2],[28.6,36.3],[31.6,36.0],[33.8,35.3],[35.2,34.9],[34.85,33.4],[34.35,32.1],[33.4,31.45],[32.2,31.55]]
LAND=[[28.2,38.4],[31.0,37.8],[34.0,37.1],[35.9,36.4],[36.2,34.7],[35.6,33.4]]
PHIL=[[34.38,31.38],[34.52,31.66],[34.63,31.86],[34.92,31.86],[34.98,31.62],[34.6,31.28],[34.38,31.38]]
HIGH=[[34.98,32.55],[35.42,32.55],[35.55,32.15],[35.5,31.6],[35.25,31.35],[34.98,31.42],[34.92,31.9],[34.98,32.55]]
PLAY = [
 B("In the years after Merneptah's stone, the old world of palaces began to fall. Historians call it the Late Bronze Age collapse.", A, ["cline","kuhrt"],
   vis=[yr(-1200), fo([34.6,34.0],1.5)], amb="desert"),
 B("It had no single cause. Drought, earthquakes, war and broken trade all played a part, and scholars still argue over which mattered most.", D, ["cline"]),
 B("Even before the worst came, there was hunger. Merneptah sent grain by ship to the Hittites, to keep their land alive in a famine.", A, ["kitchen4","cline"],
   vis=[fo([33.5,36.0],1.8,["hatti"])]),
 B("On the Syrian coast stood Ugarit, a rich trading port. Its scribes wrote in several languages, and in their own alphabet of thirty letters.", A, ["yon2006","cline"],
   vis=[yr(-1190), fo([35.9,35.3],4.5,["ugarit"])]),
 B("By modern estimates, several thousand people lived in the city itself, and many more in its villages.", D, ["garr"]),
 B("A letter from the king of Ugarit to the king of Cyprus survives. My father, behold, the enemy's ships came. My cities were burned, and they did evil things in my country.", A, ["cline"],
   note="Second half is a quotation from letter RS 20.238. Read as a quotation."),
 B("Around eleven ninety BC, Ugarit was destroyed. It was never rebuilt as a city.", A, ["kaniewski","cline","yon2006"],
   vis=[{"type":"battle","at":[35.78,35.6],"label":"Ugarit destroyed","cert":"attested",
         "arrows":[{"path":[[34.2,35.95],[35.0,35.75],[35.66,35.62]],"side":"enemy","cert":"disputed"}],
         "sfx":"battle","sfxHold":3000}],
   note="SFX: distant battle and fire, swells in the pause, then fades."),
 B("Radiocarbon dates from nearby Tell Tweini point to about eleven ninety-two to eleven ninety BC. Who the attackers were is still debated.", D, ["kaniewski"]),
 B("Far inland, the Hittite court left its capital, Hattusa, and the empire came to an end. Excavators found little sign of a final battle. The court seems to have taken its records and treasures with it.", A, ["seeher","bryce"],
   vis=[yr(-1185), fo([35.0,38.0],2.2,["hattusa"]), {"type":"border","fade":[{"zone":"hatti"}],"sfx":"border"}], amb="desert"),
 B("A branch of the royal family held on at Carchemish, beside the Euphrates.", A, ["bryce"],
   vis=[fo([37.5,36.6],3.0,["carchemish"])]),
 B("In Egypt, Ramesses the Third had these words carved at Medinet Habu. The foreign countries made a conspiracy in their islands. No land could stand before their arms.", A, ["edgerton","mhabu"],
   vis=[yr(-1180), fo([31.5,34.2],1.35,["seapeoples"]),
        {"type":"migration","label":"By sea","cert":"disputed","path":SEA,"sfx":"migration","sfxHold":2000}],
   note="Second and third sentences are a quotation from the year 8 inscription."),
 B("The same temple walls show people on the move by land, with ox-carts carrying women and children.", A, ["mhabu","yasur"],
   vis=[{"type":"migration","label":"By land","cert":"disputed","path":LAND,"sfx":"migration","sfxHold":2000}],
   note="SFX: caravan, carts creaking, livestock. This line matters for fairness: these were families, not only raiders."),
 B("Modern historians call them the Sea Peoples. Where they came from, how many they were, and how much they caused the collapse, are all debated. Many were probably looking for a new home.", D, ["cline","yasur","kaniewski"]),
 B("In his eighth year, around eleven seventy-seven BC, Ramesses the Third met them on land, in a region the Egyptians called Djahy.", A, ["edgerton","mhabu","cline"],
   vis=[yr(-1177), fo([33.2,31.9],2.8),
        {"type":"battle","at":[35.25,33.1],"label":"Land battle in Djahy (place disputed)","cert":"disputed",
         "arrows":[{"path":[[34.47,31.5],[34.75,32.3],[35.1,32.9]],"side":"egypt","cert":"attested"},
                   {"path":[[35.9,34.4],[35.5,33.7],[35.32,33.25]],"side":"enemy","cert":"disputed"}],
         "sfx":"battle","sfxHold":3000}]),
 B("Where exactly Djahy lay, and where the battle was fought, is debated.", D, ["cline","edgerton"]),
 B("Then he fought them at sea, at the mouths of the Nile. His temple walls show ships locked together, and Egyptian archers shooting from the shore.", A, ["mhabu","edgerton"],
   vis=[{"type":"battle","at":[31.95,31.42],"label":"Sea battle at the Nile mouths","cert":"attested",
         "arrows":[{"path":[[31.83,30.8],[31.9,31.25]],"side":"egypt","cert":"attested"},
                   {"path":[[33.0,31.75],[32.4,31.6],[32.05,31.48]],"side":"enemy","cert":"disputed"}],
         "sfx":"battle","sfxHold":3000}], amb="river"),
 B("Ramesses claimed a great victory, and Egypt itself was not overrun.", A, ["edgerton","cline"]),
 B("Among the enemies, the inscriptions name the Peleset. We know them better as the Philistines.", A, ["edgerton","yasur"]),
 B("A later papyrus says Ramesses settled the defeated in strongholds. Whether that means Egypt itself placed the Philistines in Canaan is debated.", D, ["harris","killebrew"],
   claims=[["A later papyrus says Ramesses settled the defeated in strongholds.",A,["harris"]],
           ["Whether that means Egypt itself placed the Philistines in Canaan is debated.",D,["killebrew","harris"]]]),
 B("On the southern coast of Canaan, newcomers made four towns their own. Ashdod, Ashkelon, Ekron and Gath.", A, ["killebrew","yasur"],
   vis=[yr(-1170), fo([34.72,31.62],7,["ashdod","ashkelon","ekron","gath"]),
        {"type":"border","add":[{"zone":"philistia","certainty":"unsure","label":"PHILISTIA","labelAt":[34.45,31.95],"coords":PHIL}],"sfx":"border"}]),
 B("They brought their own ways. Their painted pottery followed Aegean styles. They cooked on open hearths, and wove with loom weights shaped like spools.", A, ["yasur","killebrew"]),
 B("They also ate a good deal of pork, unlike the villagers in the hills.", A, ["faust","killebrew"]),
 B("Ancient DNA from Ashkelon shows that some of the early settlers had ancestry from southern Europe. Within about two centuries, their families had mixed with the people of the land.", A, ["feldman"]),
 B("When they arrived is debated. The usual view says about eleven seventy-five BC. A lower dating says about eleven thirty-five.", D, ["fink1995","yasur"]),
 B("The Hebrew Bible remembers the Philistines as coming from Caphtor, and as Israel's great rivals in the days of the Judges, of Samson, and of Saul.", T, ["bible"], ref="Amos 9:7; Judges 13–16; 1 Samuel"),
 B("Imagine the coast in those years. New houses going up, unfamiliar words in the market, and families learning a new land, as so many families have done since.", S),
 B("Egypt held on in Canaan for some decades more, with soldiers still at Beth-Shean. But during the twelfth century its rule there came to an end.", A, ["weinstein","millek","morris"],
   vis=[yr(-1160), fo([35.2,32.1],4.2,["bethshean","gaza"]), {"type":"border","fade":[{"zone":"egypt","certainty":"unsure"}],"sfx":"border"}]),
 B("Whether the end came quickly, or slowly over seventy-five years or more, is still debated.", D, ["weinstein","millek"]),
 B("And in the hills, something new was growing. Small farming villages spread across the central hill country, where few people had lived before.", A, ["fink2013","finkelstein"],
   vis=[yr(-1150), fo([35.2,31.95],5.5,["hills","izbetsartah","shechem","jerusalem"]),
        {"type":"border","fade":[{"zone":"israel"}],"add":[{"zone":"highlands","certainty":"people","label":"ISRAEL","labelAt":[34.95,32.62],"coords":HIGH}],"sfx":"border"}],
   amb="desert"),
 B("Surveys count about thirty sites there in the thirteenth century BC, and about two hundred and fifty by around one thousand BC.", A, ["fink2013"]),
 B("Many archaeologists see these villagers as early Israel. Others caution that houses and pottery alone cannot tell us what people called themselves.", D, ["faust","fink2013","killebrew"],
   note="Needed because the map draws the ISRAEL label on these hills."),
 B("Where they came from is debated too. Some scholars think they were herders of the region, settling down. Others think many came from the Canaanite towns of the lowlands.", D, ["finkelstein","faust","killebrew"]),
 B("Imagine the hills at dawn. Rock and scrub, smoke from cooking fires, and flocks heading out to graze. Here is what the excavations show.", S),
 B("Most villages were small, often a few dozen households. Some of the earliest, like Izbet Sartah, were a ring of houses around an open yard.", A, ["finkelstein","faust"],
   vis=[fo([35.05,32.07],9,["izbetsartah"])]),
 B("A typical home was a pillared house, with three or four spaces around a central room.", A, ["faust","killebrew","stager1985"]),
 B("Animals and stores were probably kept on the ground floor, with the family living above. Not every scholar agrees.", D, ["stager1985","faust"]),
 B("Families stored grain in pits lined with stone, and in large jars with a collar around the neck. They cut cisterns into the rock, to keep the winter rain for the dry summer.", A, ["finkelstein","killebrew"]),
 B("On steeper slopes, terraces held the soil. How early these terraces were built is debated.", D, ["finkelstein","faust"],
   claims=[["On steeper slopes, terraces held the soil.",A,["finkelstein"]],
           ["How early these terraces were built is debated.",D,["finkelstein","faust"]]]),
 B("They grew wheat and barley, tended olives and vines, and herded sheep and goats.", A, ["faust","fink2013","kingstager"]),
 B("Bread was the staple food. Grinding stones for flour are common finds in these houses, and grinding was hard daily work.", A, ["kingstager","meyers2013"]),
 B("Scholars think it was mostly women who did it, for hours each day.", D, ["meyers2013"]),
 B("The Torah would later praise this land as a land of wheat and barley, of vines and figs and pomegranates, a land of olive oil and honey.", T, ["bible"], ref="Deuteronomy 8:8"),
 B("Pig bones are rare at these hill sites. Some scholars link this to the later Jewish law against eating pork. Others think it was simply how hill farmers lived.", D, ["faust","fink2013"],
   claims=[["Pig bones are rare at these hill sites.",A,["faust","fink2013"]],
           ["Some scholars link this to the later Jewish law against eating pork. Others think it was simply how hill farmers lived.",D,["faust","fink2013"]]]),
 B("At Izbet Sartah, someone scratched an alphabet onto a piece of pottery, perhaps while learning to write. How old it is exactly is debated.", D, ["kochavi1977"],
   vis=[fo([34.97,32.1],9,["izbetsartah"])],
   claims=[["At Izbet Sartah, someone scratched an alphabet onto a piece of pottery, perhaps while learning to write.",A,["kochavi1977"]],
           ["How old it is exactly is debated.",D,["kochavi1977"]]]),
 B("On a hilltop in the north of these hills, archaeologists found a small open-air shrine, and a bronze figure of a bull. Who worshipped there, and which god, is debated.", D, ["mazar1982"],
   vis=[fo([35.32,32.41],8,["bullsite"])],
   claims=[["On a hilltop in the north of these hills, archaeologists found a small open-air shrine, and a bronze figure of a bull.",A,["mazar1982"]],
           ["Who worshipped there, and which god, is debated.",D,["mazar1982"]]]),
 B("The name Israel itself contains El, the old word for God across Canaan.", A, ["smith2002"]),
 B("An Egyptian list from more than a century earlier names a land of the Shasu, Yhw. Some read this as the name of Israel's God. Others doubt it.", D, ["soleb","smith2002"],
   vis=[fo([35.65,30.45],5.0,["shasu"])]),
 B("Down on the coast and along the trade roads, the long-distance trade in copper, tin and fine goods that had fed the palaces had faltered.", A, ["cline"],
   vis=[fo([35.0,32.3],4.4)]),
 B("For Israel, the world nearby had changed. The empire that named it in stone was withdrawing. The Philistines were new neighbours on the coast. And the hill villages kept growing.", A, ["millek","killebrew","fink2013"]),
 B("Imagine a winter evening in one of these houses. Rain on the roof, the animals shifting nearby. We do not know these villagers' names. Their houses, jars and terraces are what they left us.", S),
 B("In Jewish tradition, this is the age of the Judges. In those days, there was no king in Israel, and leaders rose tribe by tribe. Deborah. Gideon. And others.", T, ["bible"], ref="Judges 21:25; Judges 4–8"),
 B("Many scholars count the Song of Deborah, in the Book of Judges, among the oldest poems in the Hebrew Bible. It names tribes who came to fight, and some who stayed at home.", D, ["stager1988","bible"], ref="Judges 5",
   claims=[["Many scholars count the Song of Deborah, in the Book of Judges, among the oldest poems in the Hebrew Bible.",D,["stager1988"]],
           ["It names tribes who came to fight, and some who stayed at home.",T,["bible"]]]),
 B("There is no kingdom yet. For now, this is a people of villages, in a land shared with others. Their story has only begun.", A, ["fink2013","killebrew"],
   note="Closing line. Let it settle; the map then opens c. 1150 BC."),
]

# ---------- the opening film: a short opener that ends on a choice, then chapter 2 ----------
CHOICE = B("That is the world of this year. You can stay with the story, or explore the map on your own.", F)
OPEN_IX = (0, 1, 2, 5, 11, 12)
OPENER = [INTRO[i] for i in OPEN_IX] + [CHOICE]
REST = [b for i, b in enumerate(INTRO) if i not in OPEN_IX]
OPENER[0]["chapter"] = "The world of 1207 BC"
OPENER[-1]["choice"] = True
REST[0]["chapter"] = "Egypt and the great powers"
next(b for b in REST if b["steps"][-1]["text"].startswith("We know Israel's name"))["chapter"] = "Israel's name in stone"
INTRO_BEATS = OPENER + REST

# ---------- Play chapters: a marker every two to three minutes ----------
PLAY_CHAPTERS = {0: "The palaces fall", 10: "The Sea Peoples", 26: "Villages in the hills", 39: "Bread, faith and memory"}
for i, t in PLAY_CHAPTERS.items(): PLAY[i]["chapter"] = t

# ---------- subtitles: digits for the eye, words for the ear ----------
DIGITS = [
 ("twelve hundred and seven BC", "1207 BC"), ("more than three thousand years", "more than 3,000 years"),
 ("thirteenth son of Ramesses the Second", "13th son of Ramesses II"), ("some three million", "some 3 million"),
 ("more than three metres tall", "more than 3 metres tall"), ("Amenhotep the Third", "Amenhotep III"),
 ("twenty-eight lines", "28 lines"), ("More than three thousand two hundred years later", "More than 3,200 years later"),
 ("alphabet of thirty letters", "alphabet of 30 letters"), ("Around eleven ninety BC", "Around 1190 BC"),
 ("about eleven ninety-two to eleven ninety BC", "about 1192 to 1190 BC"), ("Ramesses the Third", "Ramesses III"),
 ("around eleven seventy-seven BC", "around 1177 BC"), ("about eleven seventy-five BC", "about 1175 BC"),
 ("about eleven thirty-five", "about 1135 BC"), ("the twelfth century", "the 12th century BC"),
 ("seventy-five years", "75 years"), ("about thirty sites there in the thirteenth century BC", "about 30 sites there in the 13th century BC"),
 ("about two hundred and fifty by around one thousand BC", "about 250 by around 1000 BC"),
]
def displayed(t):
    for a, b in DIGITS: t = t.replace(a, b)
    return t
for b in INTRO_BEATS + PLAY:
    c = b["steps"][-1]; assert c["type"] == "caption"
    assert not re.search(r"[()\d]", c["text"]), c["text"]
    d = displayed(c["text"])
    if d != c["text"]: c["display"] = d
for a, _ in DIGITS: assert any(a in b["steps"][-1]["text"] for b in INTRO_BEATS + PLAY), a

def speech(b): return b["steps"][-1]["text"]
def clean(beats):
    """beats as written to the data: reading notes stay here"""
    return [{k: v for k, v in b.items() if k != "note"} for b in beats]
