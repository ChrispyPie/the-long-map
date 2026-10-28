"""Narration for the c. 1150 BC stop of the Story of the Jews: the opening film (transitionIn) and Play
(c. 1150 BC to c. 1000 BC). Same format and rules as build/narration_jews_1207.py:
one beat = one spoken line = one mp3 in assets/narration/ (recorded with build/narrate.py).
Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film only).
Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
Contested points stay balanced: David's kingdom gets no border; minimalist, maximalist and middle views
are given side by side. Battle steps at Aphek and Gilboa have no arrows on purpose (the arrow sides are
'egypt'/'enemy', and neither fits Israel and the Philistines). "note" is for the narrator only.
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

P = {  # verified coordinates [lon, lat]; existing repo objects reuse repo values
 "shiloh":[35.2895,32.0556], "aphek":[34.930,32.105], "ashdod":[34.66,31.76], "gath":[34.85,31.70],
 "ekron":[34.85,31.78], "bethshemesh":[34.975,31.751], "kiriathjearim":[35.104,31.809],
}
ARK = [P[k] for k in ("shiloh","aphek","ashdod","gath","ekron","bethshemesh","kiriathjearim")]

# ---------------- opening film (transitionIn), chapter 1 ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. Villages, judges, and the first kings.", F, vis=[fo([35.0,31.9],4.5)], amb="desert",
   note="Title card. Warm, unhurried, but no long silence after it."),
 B("It is about eleven hundred and fifty BC. Egypt's rule in Canaan is ending, and no great power holds the land.", A, ["millek","weinstein"],
   vis=[yr(-1150), fo([34.9,31.6],4.2,["gaza","bethshean"])]),
 B("On the southern coast, the Philistines are building up their cities.", A, ["killebrew","yasur","dothan2016"],
   vis=[fo([34.7,31.65],7,["ashdod","ashkelon","ekron","gath","gaza"])]),
 B("In the hill country, small farming villages keep spreading. Most scholars see in them the beginnings of Israel.", D, ["fink2013","faust"],
   vis=[fo([35.2,31.95],5.5,["hills"])],
   claims=[["In the hill country, small farming villages keep spreading.",A,["fink2013"]],
           ["Most scholars see in them the beginnings of Israel.",D,["faust","fink2013"]]]),
 B("Jewish tradition calls this the age of the Judges. In those days there was no king in Israel.", T, ["bible"], ref="Judges 21:25"),
 B("By about one thousand BC, the Bible tells of kings. First Saul, then David. How much of that story is history is one of the great debates in archaeology.", D, ["bible","mazar2010","finksilb2006"],
   claims=[["By about one thousand BC, the Bible tells of kings. First Saul, then David.",T,["bible"]],
           ["How much of that story is history is one of the great debates in archaeology.",D,["mazar2010","finksilb2006"]]],
   ref="1 Samuel 9 – 2 Samuel 5"),
 B("That is the world of this year. You can stay with the story, or explore the map on your own.", F),
]
OPENER[0]["chapter"] = "The world of 1150 BC"
OPENER[-1]["choice"] = True

# ---------------- Play: c. 1150 BC to c. 1000 BC ----------------
COAST = [
 B("The Bible speaks of five Philistine lords, ruling five cities. Gaza, Ashkelon and Ashdod near the sea. Ekron and Gath further inland.", T, ["bible"], ref="Joshua 13:3; 1 Samuel 6:17",
   vis=[yr(-1140), fo([34.68,31.65],7.5,["gaza","ashkelon","ashdod","ekron","gath"])], amb="desert"),
 B("Excavations at Ashkelon, Ashdod, Ekron and Gath show the newcomers' culture clearly. Ekron, at Tel Miqne, grew into a large planned city.", A, ["killebrew","yasur","dothan2016"],
   vis=[fo([34.85,31.78],9,["ekron"])]),
 B("Over time their pottery changed. Painted in red and black, it mixed Aegean, Canaanite and Egyptian styles. Archaeologists call it Bichrome ware.", A, ["yasur","killebrew"]),
 B("Further north, at Tell Qasile, in today's Tel Aviv, the Philistines built a temple, and rebuilt it larger more than once.", A, ["mazar1980"],
   vis=[fo([34.79,32.1],9,["telqasile"])]),
 B("Imagine the harbour towns in those years. Potters at their wheels, fishing boats pulled up on the sand, and many languages in the market.", S),
 B("Egypt's own strength kept fading. By about ten seventy BC, the line of the Ramesside kings had ended, and Egypt was split between rulers in the north and the priests of Amun at Thebes.", A, ["kitchen1996","kuhrt"],
   vis=[fo([31.6,28.5],2.4,["egypt","thebes"])], amb="river"),
 B("An Egyptian tale shows how far its fame had fallen. A temple official, Wenamun, sails to Byblos to buy cedar. At Dor, a harbour of a people called the Tjeker, he is robbed. In Byblos, the prince makes him wait for weeks.", A, ["lichtheim1976"],
   vis=[fo([35.2,33.2],4.0,["dor","byblos"])]),
 B("Whether Wenamun's story is a real report or a literary tale is debated. Either way, it pictures an Egypt that no longer commands its neighbours.", D, ["lichtheim1976"]),
 B("Far to the east, the Assyrian king Tiglath-pileser the First fought the Arameans again and again, and marched to the Mediterranean.", A, ["grayson1991","aram"],
   vis=[yr(-1110), fo([39.5,35.0],2.2,["arameans","assur"])], amb="desert"),
 B("In this world without an empire, small peoples had room to grow. On the coast, the Philistines. Inland, the Arameans. And in the hills, Israel.", A, ["killebrew","aram","fink2013"],
   vis=[fo([35.4,32.6],3.6,["philistines","arameans","hills"])]),
]
COAST[0]["chapter"] = "Five cities on the coast"

SHILOH = [
 B("The Book of Judges tells of leaders who rose in times of danger. Ehud, Deborah, Gideon, Jephthah and Samson. Each saves one tribe or a few. Then the people forget, and trouble returns.", T, ["bible"], ref="Judges 3–16",
   vis=[yr(-1100), fo([35.2,32.0],5.5,["hills"])]),
 B("Most scholars think the book was edited centuries later, as part of a longer history that runs from Deuteronomy to Kings.", D, ["noth1981","finksilb2001"]),
 B("Some of its stories may keep old memories of tribes and local heroes. How much, no one can say for sure.", D, ["stager1988","dever2001"]),
 B("What archaeology shows fits a land of villages. No palaces, few town walls, and no sign of a central government in the hills.", A, ["fink2013","faust"]),
 B("One place stands out in the tradition. Shiloh, in the hills north of Jerusalem. Here, the Bible says, the Ark of the Covenant was kept, in a sanctuary served by the priest Eli.", T, ["bible"], ref="Joshua 18:1; 1 Samuel 1–4",
   vis=[fo([35.29,32.05],9,["shiloh"])]),
 B("Here a woman named Hannah prayed for a child, so quietly that only her lips moved. Her son Samuel grew up at the sanctuary, and became a prophet.", T, ["bible"], ref="1 Samuel 1–3"),
 B("The rabbis of the Talmud took Hannah's silent prayer as a model for how to pray. Her story is read in synagogues on the Jewish New Year.", A, ["berakhot31a"],
   note="Attested here means: this is attested as Jewish practice and teaching (Talmud Berakhot 31a; haftarah for the first day of Rosh Hashanah), not as a claim about Hannah herself."),
 B("Excavations at Shiloh found a settlement of this time, with pillared buildings and storerooms full of large jars. Then it burned.", A, ["finkshiloh1993"]),
 B("Radiocarbon dates from charred grain in the burned rooms point to the second half of the eleventh century BC.", A, ["finkpiasetzky2006"],
   vis=[yr(-1050)]),
 B("The Bible tells how Israel lost a battle to the Philistines near Aphek, and how the Ark was captured. It was carried to Ashdod, then Gath, then Ekron, and in the end sent back.", T, ["bible"], ref="1 Samuel 4–6",
   vis=[fo([35.0,31.9],7.5,["aphek","ashdod","gath","ekron","bethshemesh","kiriathjearim"]),
        {"type":"battle","at":P["aphek"],"label":"Battle near Aphek (tradition)","cert":"tradition","arrows":[],"sfx":"battle","sfxHold":2500},
        {"type":"migration","label":"The Ark's journey (tradition)","cert":"tradition","path":ARK,"sfx":"migration","sfxHold":2000}],
   note="Battle step has no arrows on purpose: the arrow sides are 'egypt'/'enemy' and neither fits Israel v. Philistines. Check the engine accepts arrows: []."),
 B("The Bible never describes Shiloh's fall. But centuries later, the prophet Jeremiah warned: go to Shiloh, and see what I did to it.", T, ["bible"], ref="Jeremiah 7:12",
   vis=[fo([35.29,32.05],9,["shiloh"])]),
 B("Many scholars link the burnt settlement to these wars with the Philistines. Who set the fire, we do not know.", D, ["finkshiloh1993","finkpiasetzky2006"]),
 B("Imagine the news reaching a hill village. A runner on the path, and people gathering to hear.", S),
 B("In the story, Samuel now leads the people. But they ask him for something new. Give us a king, to judge us, like all the nations.", T, ["bible"], ref="1 Samuel 8:5",
   note="Chapter ending. Let the last phrase land."),
]
SHILOH[0]["chapter"] = "Shiloh and the Judges"

SAUL = [
 B("Samuel warns them. A king will take your sons for his chariots, and the best of your fields for his servants. But the people insist.", T, ["bible"], ref="1 Samuel 8:11–19",
   vis=[yr(-1025)]),
 B("So Samuel anoints Saul, a tall young man of the tribe of Benjamin, from Gibeah. His first victory, the story says, is to rescue the town of Jabesh-Gilead.", T, ["bible"], ref="1 Samuel 9–11",
   vis=[fo([35.23,31.85],8.5,["gibeah","jerusalem"])]),
 B("Where Gibeah lay is debated. It has long been placed at Tell el-Ful, just north of Jerusalem, but some scholars now look elsewhere.", D, ["fink2011ful"]),
 B("No inscription from the time names Saul. Still, many historians think a real highland ruler stands behind the story.", D, ["fink2006","fink2013"],
   claims=[["No inscription from the time names Saul.",A,["fink2006"]],
           ["Still, many historians think a real highland ruler stands behind the story.",D,["fink2006","fink2013"]]]),
 B("Israel Finkelstein, for one, argues that Saul led an early territorial kingdom, centred in the hills north of Jerusalem.", D, ["fink2006","fink2013"]),
 B("The Bible describes a troubled reign. War with the Philistines, quarrels with Samuel, and a dark mood that only music could calm.", T, ["bible"], ref="1 Samuel 13–16"),
 B("The music came from a young shepherd from Bethlehem. His name was David.", T, ["bible"], ref="1 Samuel 16",
   vis=[fo([35.2,31.7],9,["bethlehem"])]),
 B("David's own family story crosses borders. The Book of Ruth says his great-grandmother was Ruth, a woman from Moab, who chose to join Israel. Your people shall be my people.", T, ["bible"], ref="Ruth 1:16; 4:17",
   note="Last sentence is a quotation. Read it softly."),
 B("Saul's end came in battle on Mount Gilboa, against the Philistines. Saul and his son Jonathan fell, and their bodies were hung on the wall of Beth-Shean.", T, ["bible"], ref="1 Samuel 31",
   vis=[yr(-1010), fo([35.42,32.46],8,["gilboa","bethshean"]),
        {"type":"battle","at":[35.414,32.434],"label":"Mount Gilboa (tradition)","cert":"tradition","arrows":[],"sfx":"battle","sfxHold":3000}],
   note="Battle step without arrows, as at Aphek. Year step -1010 follows the traditional chronology only."),
 B("David's lament for them is one of the Bible's great poems. Saul and Jonathan, beloved and lovely, in life and in death they were not divided. How the mighty have fallen.", T, ["bible"], ref="2 Samuel 1:19–27",
   note="Quotation. Slow, with weight. Chapter ending."),
]
SAUL[0]["chapter"] = "Saul, the first king"

DAVID = [
 B("The Bible's David is a hero with flaws. He fells the Philistine giant Goliath in the Valley of Elah, flees from Saul, and for a time even serves Achish, king of Gath.", T, ["bible"], ref="1 Samuel 17; 21; 27",
   vis=[fo([34.92,31.7],9,["qeiyafa","gath"])]),
 B("After Saul's death, he is made king at Hebron. Later he takes Jerusalem, and makes it his capital.", T, ["bible"], ref="2 Samuel 2:4; 5:1–9",
   vis=[fo([35.17,31.65],8.5,["hebron","jerusalem"])]),
 B("Counting back from later kings, the usual reckoning places David around one thousand BC. The exact years are uncertain.", D, ["kitchen2003","mazar2010"],
   vis=[yr(-1000)]),
 B("Archaeology has added new evidence. Above the Valley of Elah stands Khirbet Qeiyafa, a fortified town of about two point three hectares, with a double wall and two gates.", A, ["garfinkel2012"],
   vis=[fo([34.957,31.696],10,["qeiyafa"])],
   note="Qeiyafa: kay-YAH-fah. 'Double wall' = casemate wall."),
 B("It was short-lived. Radiocarbon dates place its destruction around one thousand BC, give or take a few decades.", A, ["garfinkel2012","garfinkel2015"]),
 B("Among its finds were a pottery sherd with five lines of ink writing, and no pig bones.", A, ["misgav2009","garfinkelganor2009"]),
 B("The writing is hard to read. Some read it as early Hebrew. Others say neither the script nor the language can be pinned down.", D, ["misgav2009","rollston2011"]),
 B("Who built the town is debated too. Its excavator, Yosef Garfinkel, sees a stronghold of Judah in David's time. Israel Finkelstein and Alexander Fantalkin link it instead to an early kingdom in the north, perhaps Saul's.", D, ["garfinkel2012","garfinkel2015","finkfantalkin2012"]),
 B("At Gath, a sherd from about this time, or a little later, carries two names that were probably not Semitic. Its excavators note that they recall the name Goliath, but warn that this is not evidence for Goliath himself.", A, ["maeir2008"],
   vis=[fo([34.85,31.70],10,["gath"])]),
 B("The first mention of David outside the Bible comes more than a century later. In the ninth century BC, an Aramaean king set up a victory stone at Dan, in the far north.", A, ["biran1993","biran1995"],
   vis=[fo([35.4,32.6],5.0,["dan"])],
   note="This is later attestation; the map year stays at about 1000 BC."),
 B("He boasts of killing a king of Israel, and a king of the House of David. Most scholars read House of David as the name of Judah's royal line, called after its founder.", D, ["biran1993","biran1995","mazar2010"],
   claims=[["He boasts of killing a king of Israel, and a king of the House of David.",A,["biran1995"]],
           ["Most scholars read House of David as the name of Judah's royal line, called after its founder.",D,["biran1993","mazar2010"]]]),
 B("So how great was David's kingdom? Here scholars divide. Philip Davies and Thomas Thompson argued that the biblical David is mostly the creation of much later writers.", D, ["davies1992","thompson1999"],
   vis=[fo([35.1,31.75],6.5,["jerusalem","hebron","qeiyafa"])]),
 B("At the other end, Kenneth Kitchen held that the biblical account is broadly reliable.", D, ["kitchen2003"]),
 B("Many stand in between. William Dever and Amihai Mazar see a real David, ruling a modest early state. Israel Finkelstein sees a highland chief, ruling from a small Jerusalem.", D, ["dever2001","mazar2010","finksilb2006"]),
 B("Part of the argument is about dates. A shift of a few decades in dating pottery decides whether some large buildings belong to David's time, or to kings a century later.", D, ["fink1996","mazar2005"]),
 B("In Jerusalem, Eilat Mazar believed she had found David's palace. Other archaeologists dispute her dating of the walls.", D, ["emazar2006","finkpalace2007"],
   vis=[fo([35.235,31.777],10,["jerusalem"])]),
 B("Imagine the gate at Qeiyafa at dawn. Sentries looking down into the valley, and the smell of bread from the houses.", S,
   vis=[fo([34.957,31.696],10,["qeiyafa"])]),
 B("Large or small, in the Bible the House of David rules Jerusalem for about four hundred years. And in Jewish tradition, David's name became a lasting hope, of a future king who brings peace.", T, ["bible"], ref="2 Samuel 7:16; 2 Kings 25; Isaiah 11:1–9",
   vis=[fo([35.1,31.9],5.5,["jerusalem"])],
   note="Warm, hopeful, let it settle."),
 # teaser for the next chapter (added 28 Oct 2026; every chapter ends on a hook)
 B("But the story goes on. In the Bible, David's son Solomon builds a temple in Jerusalem, and after him the kingdom splits in two. That is our next chapter.", T, ["bible"], ref="1 Kings 6–8; 1 Kings 12",
   vis=[fo([35.25,32.0],5,["jerusalem","shechem"])],
   claims=[["In the Bible, David's son Solomon builds a temple in Jerusalem, and after him the kingdom splits in two.", T, ["bible"]]],
   note="Closing line of the chapter. A hook: lighter, a little forward-leaning, then let it settle."),
]
DAVID[0]["chapter"] = "David: tradition and evidence"
PLAY = COAST + SHILOH + SAUL + DAVID

INTRO_BEATS = OPENER

# ---------- subtitles: digits for the eye, words for the ear ----------
DIGITS = [
 ("about eleven hundred and fifty BC","about 1150 BC"), ("By about one thousand BC","By about 1000 BC"),
 ("about ten seventy BC","about 1070 BC"), ("Tiglath-pileser the First","Tiglath-pileser I"),
 ("the second half of the eleventh century BC","the second half of the 11th century BC"),
 ("around one thousand BC","around 1000 BC"), ("about two point three hectares","about 2.3 hectares"),
 ("five lines of ink writing","5 lines of ink writing"), ("the ninth century BC","the 9th century BC"),
 ("about four hundred years","about 400 years"),
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
