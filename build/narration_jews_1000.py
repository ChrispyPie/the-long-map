"""Narration for the c. 1000 BC stop of the Story of the Jews ("Chapter 3"): the opening film (transitionIn)
and Play (c. 1000 BC to c. 930 BC). Same format and rules as build/narration_jews_1150.py:
one beat = one spoken line = one mp3 in assets/narration/ (recorded with build/narrate.py).
Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film only).
Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
Contested points stay balanced: David's and Solomon's kingdom gets no border; Ammon, Moab and Edom are
dashed; the split of c. 930 BC is drawn as two hill-country areas (ISRAEL, JUDAH) with a dashed edge.
Camera: written for the zoom fix (js/app.js focusView): a focus whose hl are all city/site objects
zooms until they fill the picture, k is only a minimum; lines about a land or a people keep a wide k.
"note" is for the narrator only. The chapter ends on a teaser for the next one (Shishak and Karnak).
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

# proposed coordinates [lon, lat]; existing repo objects keep repo values
P = {"jerusalem":[35.235,31.777], "hebron":[35.10,31.53], "gibeon":[35.186,31.848], "motza":[35.164,31.794],
     "gezer":[34.92,31.86], "megiddo":[35.185,32.585], "hazor":[35.568,33.017], "shechem":[35.28,32.21],
     "bethel":[35.238,31.928], "dan":[35.652,33.249], "tyre":[35.19,33.27], "rabbah":[35.934,31.955],
     "dibon":[35.786,31.499], "bozrah":[35.607,30.739], "nahas":[35.436,30.681], "eziongeber":[34.980,29.547]}
JER = [35.235,31.777]

# ---------------- opening film (transitionIn), scene 1 ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. David, Solomon, and a kingdom that splits in two.", F, vis=[fo([35.1,31.85],6,["jerusalem"])], amb="desert",
   note="Title card. Warm, no long silence after it."),
 B("It is about one thousand BC. Egypt is divided and weak. Assyria is busy with the Arameans. No empire rules this land.", A, ["kitchen1996","grayson1991"],
   vis=[yr(-1000), fo([36.5,31.5],2.0,["egypt","assyria"])]),
 B("On the coast, the Philistine cities are still strong. In the north, Tyre and Sidon trade across the sea.", A, ["killebrew","vdm"],
   vis=[fo([35.0,32.5],4.2,["gath","ashdod","tyre","sidon"])]),
 B("East of the Jordan live Ammon, Moab and Edom, and north-east, the Aramean kingdoms.", A, ["mazar2010","aram"],
   claims=[["East of the Jordan live Ammon, Moab and Edom, and north-east, the Aramean kingdoms.",D,["mazar2010","aram","benyosef2019"]]],
   vis=[fo([36.0,31.9],4.0,["ammon","moab","edom","arameans"])],
   note="Labelled Disputed as a whole: these peoples are real, but how organised they were around 1000 BC is debated (Ben-Yosef's 'architectural bias')."),
 B("In the hills, the Hebrew Bible tells of a king. David, son of Jesse, who rules from Hebron, and then from Jerusalem.", T, ["bible"], ref="2 Samuel 2–5",
   vis=[fo([35.17,31.65],10,["hebron","jerusalem"])]),
 B("How large his kingdom was, and how much of the story is history, is still debated. So the map draws no border for it.", D, ["mazar2010","finksilb2006"]),
 B("That is the world of this year. You can stay with the story, or explore the map on your own.", F),
]
OPENER[0]["chapter"] = "The world of 1000 BC"
OPENER[-1]["choice"] = True

# ---------------- Play: c. 1000 BC to c. 930 BC ----------------
CITY = [
 B("The Bible says Jerusalem belonged to the Jebusites, and that David's men took it, perhaps by climbing up the water shaft.", T, ["bible"], ref="2 Samuel 5:6–9",
   vis=[yr(-995), fo(JER,24,["jerusalem"])], amb="desert",
   note="'Water shaft' translates the obscure Hebrew word tsinnor."),
 B("Jerusalem lay on the border between the northern and southern tribes, and belonged to neither. A good place for a capital.", D, ["mazar2010","finksilb2006"],
   vis=[fo([35.22,31.85],12,["jerusalem","gibeah","bethlehem"])],
   note="Common scholarly explanation of the choice, not a fact in any ancient text."),
 B("Then David brings up the Ark of the Covenant from Kiriath-jearim, with music and shouting. And David danced before the Lord with all his might.", T, ["bible"], ref="2 Samuel 6:1–15",
   vis=[fo([35.17,31.79],22,["kiriathjearim","jerusalem"]),
        {"type":"migration","label":"The Ark comes to Jerusalem (tradition)","cert":"tradition","path":[[35.104,31.809],JER],"sfx":"migration","sfxHold":1500}],
   note="Last sentence is a quotation. Light, joyful."),
 B("On the slope of the City of David, the oldest part of Jerusalem, archaeologists have found a huge stepped stone structure, and a large building above it.", A, ["emazar2006","mazar2010"],
   vis=[fo(JER,24,["jerusalem"])]),
 B("When they were built is debated. Some date them to the time of David and Solomon. Others to a century or more later.", D, ["mazar2010","finkpalace2007"]),
 B("Most agree that tenth century Jerusalem was a small town. What they argue about is whether it was a modest capital, or a hill-country stronghold.", D, ["mazar2010","finksilb2006"],
   note="'Tenth century' = 10th century BC, David and Solomon's time in the usual reckoning."),
 B("Jewish tradition gives David the Book of Psalms. Many of them carry his name, and they are still sung and prayed every day.", T, ["bible"], ref="e.g. Psalm 23; Psalms 51–72",
   claims=[["Jewish tradition gives David the Book of Psalms. Many of them carry his name,",T,["bible"]],
           ["and they are still sung and prayed every day.",A,["berakhot4b"]]],
   note="Second claim = attested Jewish practice (Ashrei, Psalm 145, said three times a day; Talmud Berakhot 4b)."),
 B("Imagine Jerusalem on that day. A small walled town on a ridge, crowded with people, and drums echoing in the valley.", S,
   vis=[fo(JER,24,["jerusalem"])]),
]
CITY[0]["chapter"] = "David's Jerusalem"

NEIGH = [
 B("The Second Book of Samuel lists David's wars. He defeats the Philistines, then Moab, Edom, Ammon, and the Aramean king Hadadezer of Zobah.", T, ["bible"], ref="2 Samuel 5:17–25; 8; 10",
   vis=[yr(-985), fo([35.9,32.2],3.6,["philistines","moab","edom","ammon","zobah"])]),
 B("No text from these neighbours mentions David's wars. And this list may have grown in the telling.", D, ["finksilb2006","mazar2010"],
   claims=[["No text from these neighbours mentions David's wars.",A,["mazar2010"]],
           ["And this list may have grown in the telling.",D,["finksilb2006","mazar2010"]]]),
 B("In the story, the siege of Rabbah, the Ammonite capital, leads to David's worst deed.", T, ["bible"], ref="2 Samuel 11:1",
   vis=[fo(P["rabbah"],24,["rabbah"])], note="Rabbah = the citadel hill in Amman, Jordan."),
 B("He takes Bathsheba, the wife of his soldier Uriah, and sends Uriah to die at the front. The prophet Nathan tells him a story about a stolen lamb, and says: you are the man.", T, ["bible"], ref="2 Samuel 11–12",
   vis=[fo(JER,24,["jerusalem"])], note="'You are the man' quietly, with weight."),
 B("Few ancient kings are shown like this. The Bible lets its greatest king be judged.", D, ["dever2001","mazar2010"],
   note="Labelled Disputed: an interpretation many scholars share, not a fact."),
 B("South of the Dead Sea, in the Arabah valley, a copper industry was booming at this time. At Khirbet en-Nahas, slag heaps and radiocarbon dates show smelting on a huge scale.", A, ["levy2014","benyosef2019"],
   vis=[fo(P["nahas"],24,["nahas"])],
   note="Nahas: na-HAAS."),
 B("Many scholars think the people who ran it were early Edomites, living mostly in tents. Erez Ben-Yosef argues that a kingdom can be real without leaving palaces behind.", D, ["benyosef2019"],
   vis=[fo([35.52,30.71],18,["nahas","bozrah"])]),
 B("It cuts both ways. A people with few stone buildings could still be strong. That matters for Edom, and for David too.", D, ["benyosef2019"]),
 B("Far to the north, in Tyre, the Bible says king Hiram sent David cedar wood and builders for his house.", T, ["bible"], ref="2 Samuel 5:11",
   vis=[fo(P["tyre"],24,["tyre"])]),
 B("A Tyrian king list, quoted much later by the historian Josephus, also names a king Hiram, who ruled for more than thirty years.", D, ["josephusapion"],
   note="Josephus quotes Menander of Ephesus and Dius. Labelled Disputed: a late, second-hand source; how reliable its numbers are is debated."),
]
NEIGH[0]["chapter"] = "Neighbours and wars"

HEIR = [
 B("David's last years are troubled. His son Absalom rebels, and is killed. Then two sons, Adonijah and Solomon, both want the throne.", T, ["bible"], ref="2 Samuel 15–18; 1 Kings 1",
   vis=[yr(-970), fo(JER,24,["jerusalem"])]),
 B("Bathsheba and Nathan go to the old king, and he chooses Solomon. Solomon is anointed at the spring of Gihon, below the city, and the people shout: long live king Solomon.", T, ["bible"], ref="1 Kings 1:11–40",
   note="Gihon: GEE-hon. The last phrase is a shout of joy, not too loud."),
 B("Counting back from later kings, the usual reckoning puts Solomon's reign at about nine seventy to nine thirty BC. Some scholars put it a little later.", D, ["kitchen2003","mazar2010"],
   vis=[yr(-965)]),
 B("At Gibeon, the story says, God appears to Solomon in a dream. Ask what I shall give you. And Solomon asks for an understanding heart.", T, ["bible"], ref="1 Kings 3:4–9",
   vis=[fo(P["gibeon"],24,["gibeon"])]),
 B("Then comes the famous judgement. Two women claim one baby. Solomon calls for a sword to divide the child, and the true mother cries out to spare it.", T, ["bible"], ref="1 Kings 3:16–28",
   vis=[fo(JER,24,["jerusalem"])]),
 B("Tradition also gives Solomon the books of Proverbs, Ecclesiastes, and the Song of Songs. Modern scholars think they were written or gathered over many centuries.", D, ["bible","finksilb2006"],
   claims=[["Tradition also gives Solomon the books of Proverbs, Ecclesiastes, and the Song of Songs.",T,["bible"]],
           ["Modern scholars think they were written or gathered over many centuries.",D,["finksilb2006"]]],
   ref="Proverbs 1:1; Ecclesiastes 1:1; Song of Songs 1:1"),
]
HEIR[0]["chapter"] = "Solomon becomes king"

TEMPLE = [
 B("In the fourth year of his reign, the Bible says, Solomon begins to build a house for the Lord in Jerusalem.", T, ["bible"], ref="1 Kings 6:1",
   vis=[yr(-960), fo(JER,24,["jerusalem"])], amb="desert"),
 B("Hiram of Tyre sends cedar from Lebanon, floated down the coast on rafts. In return, Solomon pays in wheat and olive oil.", T, ["bible"], ref="1 Kings 5:1–11",
   vis=[fo([35.6,33.2],6.5,["tyre","lebanon","jerusalem"]),
        {"type":"migration","label":"Cedar from Lebanon (tradition)","cert":"tradition","path":[[35.95,34.05],[35.19,33.27],[34.75,32.08],JER],"sfx":"migration","sfxHold":2000}],
   note="Path: Lebanon mountains, Tyre, the coast near Joppa, up to Jerusalem (1 Kings 5:9; 2 Chronicles 2:16)."),
 B("The temple has three parts. A porch, a great hall, and the innermost room, the Holy of Holies, where the Ark is placed beneath two golden cherubim.", T, ["bible"], ref="1 Kings 6–8",
   vis=[fo(JER,24,["jerusalem"])]),
 B("Nothing of Solomon's temple has been excavated. The Temple Mount is a holy place, and it cannot be dug.", A, ["mazar2010"],
   claims=[["Nothing of Solomon's temple has been excavated.",A,["mazar2010"]],
           ["The Temple Mount is a holy place, and it cannot be dug.",A,["mazar2010"]]],
   note="Neutral wording on purpose: holy to Jews and Muslims, and excavation there is not permitted."),
 B("But temples with the same three-part plan stand elsewhere. The closest is at Ain Dara in Syria, with giant footprints carved at its entrance.", A, ["monson2000"],
   vis=[fo([36.852,36.459],24,["aindara"])], note="Ain Dara: ain DAH-ra."),
 B("And at Tel Motza, just outside Jerusalem, archaeologists found a temple from this time, with an altar, a courtyard, and clay figures.", A, ["kisilevitz2015"],
   vis=[fo(P["motza"],24,["motza"])], note="Motza: MO-tsa. Dated Iron IIA, late tenth to early ninth century BC."),
 B("At Khirbet Qeiyafa, a small stone model of a shrine has a door with three frames set one inside the other. Its excavators link this to puzzling words in the Bible's account of Solomon's buildings.", D, ["garfinkelmumcuoglu2016"],
   claims=[["At Khirbet Qeiyafa, a small stone model of a shrine has a door with three frames set one inside the other.",A,["garfinkelmumcuoglu2016"]],
           ["Its excavators link this to puzzling words in the Bible's account of Solomon's buildings.",D,["garfinkelmumcuoglu2016"]]],
   vis=[fo([34.957,31.696],24,["qeiyafa"])]),
 B("None of this proves the biblical temple. It shows that such a temple would fit its world.", D, ["mazar2010","monson2000"]),
 B("At the dedication, Solomon prays that when people far away turn toward this house and pray, God will hear them in heaven.", T, ["bible"], ref="1 Kings 8:41–49",
   vis=[fo(JER,24,["jerusalem"])]),
 B("To this day, Jews everywhere turn toward Jerusalem when they pray.", A, ["berakhot30a"],
   note="Attested as Jewish practice and law (Talmud Berakhot 30a; Shulchan Arukh OC 94), not as a claim about Solomon. Strictly: outside the Land one faces the Land of Israel, with the heart on Jerusalem and the Temple. Let it land."),
 B("Imagine the cedar beams arriving. The smell of fresh wood, the shouts of the carriers, and the stone walls slowly rising.", S),
]
TEMPLE[0]["chapter"] = "The temple"

GATES = [
 B("The Bible says Solomon also built up Hazor, Megiddo and Gezer.", T, ["bible"], ref="1 Kings 9:15",
   vis=[yr(-950), fo([35.25,32.45],7.5,["hazor","megiddo","gezer"])]),
 B("In the nineteen fifties, Yigael Yadin found similar gates at all three, each with six chambers. He called them Solomon's gates.", A, ["yadin1958"],
   vis=[fo([34.92,31.86],24,["gezer"])], note="Gezer first: that is where Yadin made the link from old excavation plans."),
 B("Then the dates were questioned. Israel Finkelstein moved them about a century later, to the northern kings of Israel.", D, ["fink1996"],
   vis=[fo([35.185,32.585],24,["megiddo"])]),
 B("Newer radiocarbon work at Gezer points back to the tenth century BC. At Megiddo and Hazor, the argument goes on.", D, ["webster2023","mazar2005"],
   vis=[fo([34.92,31.86],24,["gezer"])]),
 B("Gates of this kind are now known from many sites, so the style alone cannot name the king who built them.", A, ["webster2023"]),
 B("Gezer gave us something else, too. A small limestone tablet listing the farmer's year. Two months of gathering, two months of sowing, a month of barley harvest.", A, ["rollston2010"],
   claims=[["Gezer gave us something else, too. A small limestone tablet listing the farmer's year.",A,["rollston2010"]],
           ["Two months of gathering, two months of sowing, a month of barley harvest.",A,["rollston2010"]]],
   note="The Gezer Calendar, usually dated to the 10th century BC. Whether its script is Hebrew or Phoenician is debated: said in the next line."),
 B("Whether it is written in early Hebrew or in Phoenician is debated. Either way, the alphabet was spreading in these hills.", D, ["rollston2010"]),
 B("In the Bible, Gezer came to Solomon as a gift. A pharaoh burned it, and gave it to his daughter when she married Solomon.", T, ["bible"], ref="1 Kings 9:16",
   note="Which pharaoh is unknown; Siamun is sometimes suggested. Left out of the spoken text on purpose."),
 B("Egypt's kings of this time ruled from Tanis, in the Nile Delta. There, in nineteen forty, Pierre Montet found the untouched tomb of king Psusennes the First, with a silver coffin and a gold mask.", A, ["kitchen1996","montet1951"],
   vis=[fo([31.88,30.977],24,["tanis"])], amb="river",
   note="Psusennes: soo-SEN-eez. Intact tomb opened by Montet on 15 February 1940."),
 B("The Bible tells of ships, too. Solomon and Hiram send a fleet from Ezion-geber, on the Red Sea, to a land called Ophir, and it returns with gold.", T, ["bible"], ref="1 Kings 9:26–28",
   vis=[fo(P["eziongeber"],20,["eziongeber"])], amb="desert"),
 B("Where Ophir was, no one knows. Arabia, Africa and India have all been suggested.", D, ["kitchen2003"]),
 B("Then comes the queen of Sheba, with spices, gold and hard questions, to test Solomon's wisdom.", T, ["bible"], ref="1 Kings 10:1–13",
   vis=[fo([37.5,26.5],2.2,["redsea"])], note="Sheba itself (Yemen) lies south of the map, so the shot stays on the Red Sea heading south. No marker for Sheba."),
 B("Sheba was a real kingdom in Yemen, but its own inscriptions come from later centuries. In Ethiopia, a much later tradition says the queen bore Solomon a son, Menelik.", D, ["simpson2002","kebranagast"],
   claims=[["Sheba was a real kingdom in Yemen, but its own inscriptions come from later centuries.",A,["simpson2002"]],
           ["In Ethiopia, a much later tradition says the queen bore Solomon a son, Menelik.",T,["kebranagast"]]]),
]
GATES[0]["chapter"] = "Gates, ships and gold"

SPLIT = [
 B("The Bible does not hide the cost. Solomon's building needed forced labour, and heavy taxes from the tribes.", T, ["bible"], ref="1 Kings 5:13–18; 9:15–22; 12:4",
   vis=[yr(-940), fo([35.25,32.0],7.5,["jerusalem","shechem","gezer"])], amb="desert"),
 B("In his old age, it says, his many foreign wives turned his heart to other gods. And trouble rose. In Edom, in Damascus, and in his own court.", T, ["bible"], ref="1 Kings 11:1–25",
   vis=[fo([35.8,32.0],4.2,["edom","damascus","jerusalem"])]),
 B("An official named Jeroboam, from the north, rebels, and flees to Egypt, to a pharaoh called Shishak.", T, ["bible"], ref="1 Kings 11:26–40",
   vis=[fo([33.5,31.0],3.4,["tanis","jerusalem"]),
        {"type":"migration","label":"Jeroboam flees to Egypt (tradition)","cert":"tradition","path":[JER,[34.45,31.5],[31.88,30.977]],"sfx":"migration","sfxHold":1800}]),
 B("Then Solomon dies. His son Rehoboam goes to Shechem, where all Israel has come to make him king.", T, ["bible"], ref="1 Kings 11:43–12:1",
   vis=[yr(-930), fo(P["shechem"],24,["shechem"])]),
 B("The northern tribes ask him for a lighter load. He answers harshly. My father made your yoke heavy, but I will add to your yoke.", T, ["bible"], ref="1 Kings 12:4–14",
   note="Quotation. Hard and cold."),
 B("And the people answer. What portion have we in David? To your tents, O Israel.", T, ["bible"], ref="1 Kings 12:16",
   note="The turning point of the chapter. A short beat of silence after it is fine, but keep it under one second."),
 B("The north makes Jeroboam king of Israel. Rehoboam keeps Judah, and Jerusalem.", T, ["bible"], ref="1 Kings 12:17–20",
   vis=[fo([35.25,32.2],6.0,["shechem","jerusalem"])]),
 B("Jeroboam sets up golden calves at Bethel and at Dan, so that his people need not go to the temple in Jerusalem.", T, ["bible"], ref="1 Kings 12:26–30",
   vis=[fo([35.45,32.6],6.0,["bethel","dan"])]),
 B("Some historians doubt there ever was one kingdom to split. Israel Finkelstein sees the north and Judah as separate from the start, with the united monarchy a later ideal.", D, ["finksilb2006","fink2013"],
   vis=[fo([35.3,32.2],5.0,["hills"])]),
 B("Others, like Amihai Mazar, think a modest kingdom under David and Solomon is the best reading of the evidence.", D, ["mazar2010"]),
 B("Either way, from now on there are two kingdoms. Israel in the north, and Judah in the south, with the House of David in Jerusalem.", A, ["biran1995","mazar2010"],
   claims=[["Either way, from now on there are two kingdoms. Israel in the north, and Judah in the south,",A,["biran1995","mazar2010"]],
           ["with the House of David in Jerusalem.",A,["biran1995"]]],
   vis=[fo([35.3,32.2],5.0,["israelp","judah"])],
   note="Attested here = attested soon after: Assyrian, Moabite and Aramaic texts of the 9th century name both kingdoms; the Tel Dan stele names the House of David."),
 B("Then, in the fifth year of king Rehoboam, the Bible says, Shishak king of Egypt comes up against Jerusalem, and carries off the treasures of the temple.", T, ["bible"], ref="1 Kings 14:25–26",
   vis=[fo([33.5,31.0],3.4,["tanis","jerusalem"]),
        {"type":"migration","label":"Shishak marches north (tradition)","cert":"tradition","path":[[31.88,30.977],[34.45,31.5],JER],"sfx":"migration","sfxHold":1800}],
   note="Shishak = Shoshenq I, founder of Egypt's 22nd Dynasty; the identification is near-universal. Tension building, not loud."),
 B("And this time, Egypt tells its own side of the story. On a temple wall at Karnak, the pharaoh carved a long list of the places he conquered. Is Jerusalem on it? That is where our next chapter begins.", A, ["wilson2005"],
   claims=[["And this time, Egypt tells its own side of the story. On a temple wall at Karnak, the pharaoh carved a long list of the places he conquered.",A,["wilson2005"]]],
   vis=[fo([32.64,25.70],24,["thebes"])], amb="river",
   note="Chapter hook. The question is deliberate: Jerusalem's name is not found on the surviving list, which opens Chapter 4. Do not answer it here. Slow down on the last two sentences, then stop."),
]
SPLIT[0]["chapter"] = "The kingdom divides"
PLAY = CITY + NEIGH + HEIR + TEMPLE + GATES + SPLIT

INTRO_BEATS = OPENER

# the split of c. 930 BC: the hill-country area of Israel (data/eras/1000bc.json) is redrawn as two areas,
# a small gap between them just north of Jerusalem (and of Gibeon), dashed edges (index.html .z-judah)
def _split():
    import narration_jews_1207 as N1207   # the same ring the 1207 BC Play drew (data/eras/1150bc.json "israel")
    return next(a for b in N1207.PLAY for x in b["steps"] if x["type"] == "border" for a in x.get("add", []) if a["zone"] == "highlands")["coords"]
SPLIT_LAT_N, SPLIT_LAT_S = 31.885, 31.865   # Bethel (31.93) stays north, Gibeon (31.85) and Jerusalem south
def clip(ring, lat, keep_north):
    """the part of a polygon ring north (or south) of a line of latitude"""
    out = []; pts = ring[:-1] if ring[0] == ring[-1] else ring[:]
    ins = lambda p: p[1] >= lat if keep_north else p[1] <= lat
    for i, p in enumerate(pts):
        q = pts[(i + 1) % len(pts)]
        if ins(p): out.append([round(p[0], 4), round(p[1], 4)])
        if ins(p) != ins(q):
            t = (lat - p[1]) / (q[1] - p[1]); out.append([round(p[0] + t * (q[0] - p[0]), 4), lat])
    return out + [out[0]]
_R = _split()
NORTH, SOUTH = clip(_R, SPLIT_LAT_N, True), clip(_R, SPLIT_LAT_S, False)
SPLIT_STEP = {"type":"border","fade":[{"zone":"israel"}],"add":[
  {"zone":"israel","certainty":"people","label":"ISRAEL","labelAt":[35.24,32.22],"coords":NORTH},
  {"zone":"judah","certainty":"people","label":"JUDAH","labelAt":[35.13,31.62],"coords":SOUTH}],"sfx":"border"}
# the border step goes on the line that says the north makes Jeroboam king
_b = next(b for b in PLAY if b["steps"][-1]["text"].startswith("The north makes Jeroboam king"))
_b["steps"].insert(len(_b["steps"]) - 1, SPLIT_STEP)

# ---------- subtitles: digits for the eye, words for the ear ----------
DIGITS = [("about one thousand BC","about 1000 BC"), ("tenth century Jerusalem","10th-century Jerusalem"),
  ("about nine seventy to nine thirty BC","about 970 to 930 BC"), ("In the nineteen fifties","In the 1950s"),
  ("the tenth century BC","the 10th century BC"), ("in nineteen forty","in 1940"), ("Psusennes the First","Psusennes I"),
  ("more than thirty years","more than 30 years"), ("In the fourth year","In the 4th year")]
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
