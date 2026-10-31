"""Narration for the 722 BC stop of the Story of the Jews ("Chapter 5", Fall of Samaria): the opening film
(transitionIn) and Play (841 BC to 720 BC). Same format and rules as build/narration_jews_930.py:
one beat = one spoken line = one mp3 in assets/narration/ (recorded with build/narrate.py).
Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film only).
Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
The opener starts at the end (Samaria under siege, 722 BC), then goes back to 841 BC, where Chapter 4 ended.
Told from the side of Israel and Judah; Assyria speaks in its own inscriptions, the Samaritans in their own
tradition. The ten tribes are told as tradition. The chapter ends on a teaser for the next one
(Sennacherib and Jerusalem, 701 BC).
"""
import re
import narration_jews_1000 as N1000, narration_jews_930 as N930
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
cap, fo, yr, B = N1000.cap, N1000.fo, N1000.yr, N1000.B

# coordinates [lon, lat]; existing repo objects keep repo values; new ones as in build/objects.py
P = dict(N930.P, **{"gath":[34.85,31.70], "hazor":[35.568,33.017], "tekoa":[35.22,31.633], "bethel":[35.238,31.928],
     "rimah":[42.449,36.257], "gozan":[40.04,36.827], "media":[48.5,34.8], "dursharrukin":[43.229,36.509],
     "cuthah":[44.613,32.76], "babylon":[44.42,32.54], "gerizim":[35.273,32.201], "galilee":[35.45,32.85]})

# ---------------- opening film (transitionIn) ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. The kingdom of Israel, and the empire that ended it.", F, vis=[yr(-722), fo([38.0,33.8],2.1,["samaria","assyria"])], amb="desert",
   note="Title card. Warm, no long silence after it."),
 B("Our last chapter ended in eight forty one BC, with tribute from Jehu of Israel laid before the king of Assyria.", F,
   vis=[yr(-841), fo(P["kalhu"],10,["kalhu"])], note="Picks up the end of Chapter 4."),
 B("Now we begin at the other end of the story. The year is seven twenty two BC, and Samaria, Israel's capital, is under siege.", A, ["grayson1975","tadmor1958"],
   vis=[yr(-722), fo(P["samaria"],18,["samaria"])]),
 B("The Bible says the Assyrian army has been outside its walls for three years.", T, ["bible"], ref="2 Kings 17:5"),
 B("The king of Assyria is Shalmaneser the Fifth. Within months he will be dead, and Sargon the Second will claim the victory as his own.", A, ["tadmor1958","becking1992","frame2021"],
   note="Shalmaneser: shal-man-EE-zer. Sargon: SAR-gon."),
 B("How did the House of Omri's proud kingdom come to this? To find out, we go back more than a century, to the years after Jehu.", F,
   vis=[yr(-841), fo([37.0,33.6],2.6,["samaria","damascus","kalhu"])]),
 B("On the map, Israel in the north, Judah in the south, and Aram-Damascus pressing on them both. Far to the east, Assyria.", A, ["fink2013","grayson1996","aram"],
   vis=[fo([38.0,33.6],2.0,["israelk","judah","aramdamascus","assyria"])]),
 B("By the end of this chapter, one of those kingdoms will be gone from the map.", A, ["tadmor2011","frame2021"],
   vis=[fo([35.6,32.4],5.0,["israelk","judah"])]),
 B("That is the world of this chapter. You can stay with the story, or explore the map on your own.", F,
   vis=[fo([35.6,32.6],3.6)]),
]
OPENER[0]["chapter"] = "The world of 722 BC"
OPENER[-1]["choice"] = True

# ---------------- Play: 841 BC to 720 BC ----------------
ARAM = [
 B("After Jehu, the Bible says, Hazael of Damascus kept Israel weak. Jehu's son was left with only fifty horsemen, ten chariots and ten thousand foot soldiers.", T, ["bible"], ref="2 Kings 13:3, 7",
   vis=[yr(-815), fo([35.9,32.9],5.0,["damascus","samaria","aramdamascus"])], amb="desert", note="Hazael: HAZ-ay-el."),
 B("Hazael even marched down the coast to Gath, and Joash of Judah paid him off with the treasures of the temple.", T, ["bible"], ref="2 Kings 12:18–19 (12:17–18 in many English Bibles)",
   vis=[fo([35.2,32.3],4.6,["gath","jerusalem","damascus"]),
        {"type":"migration","label":"Hazael marches on Gath (tradition)","cert":"tradition","path":[P["damascus"],[35.6,32.7],[35.0,32.2],P["gath"]],"sfx":"migration","sfxHold":2000}]),
 B("At Gath, archaeologists found a siege trench dug around the whole city, and a great destruction from the late ninth century BC. Aren Maeir links it with Hazael.", D, ["maeir2004"],
   claims=[["At Gath, archaeologists found a siege trench dug around the whole city, and a great destruction from the late ninth century BC.",A,["maeir2004"]],
           ["Aren Maeir links it with Hazael.",D,["maeir2004"]]],
   vis=[fo(P["gath"],18,["gath"])], note="Aren Maeir: AH-ren MY-er. Gath is Tell es-Safi."),
 B("Then Assyria returns. Adad-nirari the Third marches west, and the king of Damascus pays him a vast tribute.", A, ["grayson1996","page1968"],
   vis=[yr(-796), fo([39.5,35.0],2.2,["kalhu","damascus"]),
        {"type":"migration","label":"Adad-nirari III marches west (c. 796 BC)","cert":"attested","path":[P["kalhu"],[40.0,36.6],[37.3,35.6],[36.6,34.4],P["damascus"]],"sfx":"migration","sfxHold":2400}],
   note="Adad-nirari: AH-dad NEE-rah-ree."),
 B("On a stele found at Tell al-Rimah, he names another king who paid. Joash, the Samarian.", A, ["page1968","grayson1996"],
   vis=[fo(P["rimah"],12,["rimah"])], note="Joash of Israel, Jehu's grandson. In Akkadian, Iu'asu."),
 B("The Bible says God gave Israel a deliverer, and that Joash won back the towns Aram had taken.", T, ["bible"], ref="2 Kings 13:5, 25"),
 B("Many historians see Assyria's blows on Damascus as what gave Israel room to recover.", D, ["fink2013","grayson1996"]),
 B("Imagine a town in Gilead rebuilding its wall, after a whole generation of raids from the north.", S,
   vis=[fo([35.9,32.4],10,["ramothgilead"])]),
]
ARAM[0]["chapter"] = "Aram's long shadow"

JEROB = [
 B("Joash's son, Jeroboam the Second, rules for forty one years. The Bible says he restored Israel's border, from Lebo-hamath to the Sea of the Arabah.", T, ["bible"], ref="2 Kings 14:23–25",
   vis=[yr(-785), fo([35.8,33.0],3.6,["israelk","hamath","deadsea"])], amb="desert", note="Lebo-hamath: LEE-bo HAY-math, 'the entrance to Hamath'."),
 B("It gives him only a few verses, and still says he did evil in the eyes of the Lord.", T, ["bible"], ref="2 Kings 14:24–29"),
 B("At Samaria, excavators found dozens of pottery sherds written in ink. They record deliveries of wine and fine oil to the capital.", A, ["reisner1924"],
   vis=[fo(P["samaria"],24,["samaria"])], note="The Samaria Ostraca, found by the Harvard expedition in 1910."),
 B("Their date is debated. Many place them in the first half of the eighth century BC, close to Jeroboam's reign.", D, ["fink2013","reisner1924"]),
 B("The names on them say something about faith. Some are built with Yahu, the name of Israel's God, and some with Baal.", A, ["reisner1924"]),
 B("At Megiddo, a jasper seal was found in nineteen oh four, carved with a roaring lion. It reads: belonging to Shema, servant of Jeroboam.", A, ["ussishkin1994"],
   vis=[fo(P["megiddo"],24,["megiddo"])], note="Shema: sheh-MAH. 'Servant' means a royal official."),
 B("Most scholars think the king is Jeroboam the Second. The seal itself is lost, and is known today from casts and photographs.", D, ["ussishkin1994"],
   claims=[["Most scholars think the king is Jeroboam the Second.",D,["ussishkin1994"]],
           ["The seal itself is lost, and is known today from casts and photographs.",A,["ussishkin1994"]]]),
 B("Israel Finkelstein sees these years as the high point of the northern kingdom, in its size and its wealth.", D, ["fink2013"]),
 B("Imagine a jar of oil, sealed and marked in ink, carried up the hill to the king's storerooms.", S,
   vis=[fo(P["samaria"],18,["samaria"])]),
]
JEROB[0]["chapter"] = "Jeroboam II"

PROPH = [
 B("In these rich years, a herdsman from Tekoa in Judah comes north, to the king's shrine at Bethel. His name is Amos.", T, ["bible"], ref="Amos 1:1; 7:10–13",
   vis=[yr(-760), fo([35.22,31.8],14,["tekoa","bethel"]),
        {"type":"migration","label":"Amos goes north to Bethel (tradition)","cert":"tradition","path":[P["tekoa"],[35.24,31.78],P["bethel"]],"sfx":"migration","sfxHold":1400}],
   amb="desert", note="Tekoa: teh-KOH-a."),
 B("Those who lie on beds of ivory, he says, who drink wine from bowls, but do not grieve over the ruin of Joseph.", T, ["bible"], ref="Amos 6:4–6",
   note="Quotation. 'Joseph' is the northern kingdom."),
 B("Ivory inlays for furniture, like those he describes, were found in the palace ruins at Samaria.", A, ["crowfoot1938"],
   vis=[fo(P["samaria"],24,["samaria"])]),
 B("Let justice roll down like waters, and righteousness like an ever-flowing stream.", T, ["bible"], ref="Amos 5:24",
   note="The best-known line of Amos. Slow, clear."),
 B("The priest of Bethel tells him to go back to Judah. Amos answers. I am no prophet, nor a prophet's son. I am a herdsman, and a dresser of sycamore figs.", T, ["bible"], ref="Amos 7:12–14",
   vis=[fo(P["bethel"],18,["bethel"])]),
 B("The book dates his words to two years before the earthquake. At Hazor, Yigael Yadin found walls bent and fallen in a layer of this time, and linked them with it.", D, ["bible","yadin1972"], ref="Amos 1:1",
   claims=[["The book dates his words to two years before the earthquake.",T,["bible"]],
           ["At Hazor, Yigael Yadin found walls bent and fallen in a layer of this time, and linked them with it.",D,["yadin1972"]]],
   vis=[fo(P["hazor"],18,["hazor"])], note="Yigael Yadin: yig-AH-el yah-DEEN."),
 B("In Israel itself, the prophet Hosea speaks of his people as an unfaithful wife, and of a God who still calls her back. When Israel was a child, I loved him.", T, ["bible"], ref="Hosea 2; 11:1",
   note="Hosea: ho-ZAY-a. The last sentence is a quotation, tender."),
 B("Imagine the crowd at Bethel falling silent, as a stranger from the south begins to speak.", S),
]
PROPH[0]["chapter"] = "Amos and Hosea"

TIG = [
 B("In seven forty five BC, a new king seizes the throne of Assyria. Tiglath-pileser the Third.", A, ["tadmor2011","millard1994"],
   vis=[yr(-745), fo([41.5,35.5],2.6,["assyria","kalhu"])], amb="desert", note="Tiglath-pileser: TIG-lath pi-LEE-zer."),
 B("He does not just collect tribute. He turns conquered lands into provinces, and moves whole peoples from one end of the empire to the other.", A, ["tadmor2011","oded1979"]),
 B("In Israel, after Jeroboam, kings are murdered one after another. Zechariah rules six months. Shallum, one.", T, ["bible"], ref="2 Kings 15:8–14",
   vis=[fo(P["samaria"],14,["samaria"])]),
 B("Then Pul, king of Assyria, comes against the land, and Menahem pays him a thousand talents of silver, raised from every wealthy man.", T, ["bible"], ref="2 Kings 15:19–20",
   note="Menahem: MEN-a-hem. Pul is Tiglath-pileser's Babylonian name."),
 B("Tiglath-pileser's own annals list the tribute of Menahem of Samaria. Pul was the name he used as king of Babylon.", A, ["tadmor2011"],
   vis=[fo([39.5,34.2],2.2,["kalhu","samaria"])]),
 B("In Judah, Ahaz is king. Rezin of Damascus and Pekah of Israel march on Jerusalem, to put a king of their own choosing on its throne.", T, ["bible"], ref="2 Kings 16:5; Isaiah 7:1–6",
   vis=[yr(-734), fo([35.7,32.6],5.0,["jerusalem","damascus","samaria"]),
        {"type":"migration","label":"Rezin and Pekah march on Jerusalem (tradition)","cert":"tradition","path":[P["damascus"],[35.7,32.6],P["samaria"],P["jerusalem"]],"sfx":"migration","sfxHold":2000}],
   note="Rezin: REE-zin. Pekah: PEE-ka. Ahaz: AY-haz."),
 B("The prophet Isaiah tells Ahaz to stand firm, and gives him a sign. A young woman will bear a son, and call his name Immanuel. God is with us.", T, ["bible"], ref="Isaiah 7:4, 14",
   vis=[fo(P["jerusalem"],18,["jerusalem"])]),
 B("Instead, Ahaz sends silver and gold to Tiglath-pileser. I am your servant and your son. Come and save me.", T, ["bible"], ref="2 Kings 16:7–8"),
 B("And on Tiglath-pileser's list of kings who paid him there is Jehoahaz of Judah. It is Ahaz, with his full name.", A, ["tadmor2011"]),
 B("Assyria strikes. In seven thirty two BC, after a long siege, Damascus falls. The kingdom of Aram becomes an Assyrian province.", A, ["tadmor2011","millard1994"],
   vis=[yr(-732), fo(P["damascus"],8.0,["damascus","aramdamascus"]),
        {"type":"battle","at":P["damascus"],"label":"Damascus falls (732 BC)","cert":"attested","sfx":"battle","sfxHold":2400}]),
 B("Israel loses Galilee and Gilead. The Bible names the towns, from Ijon to Hazor and all the land of Naphtali, and says their people were carried off to Assyria.", T, ["bible"], ref="2 Kings 15:29",
   vis=[fo([35.7,32.9],6.0,["galilee","hazor","israelk"]),
        {"type":"migration","label":"Galilee deported to Assyria (732 BC)","cert":"attested","path":[P["hazor"],[36.3,34.2],[38.5,35.8],P["kalhu"]],"sfx":"migration","sfxHold":2400}],
   note="Ijon: EYE-jon. Naphtali: NAF-ta-lee."),
 B("At Hazor, the city of this time ended in fire, under a thick layer of ash.", A, ["yadin1972"],
   vis=[fo(P["hazor"],18,["hazor"])]),
 B("Tiglath-pileser writes: they overthrew Pekah their king, and I set Hoshea as king over them.", A, ["tadmor2011"],
   note="Hoshea: ho-SHAY-a. Quotation from the Assyrian king."),
 B("The Bible says Hoshea killed Pekah. Assyria says it put Hoshea on the throne. Both may be true.", D, ["bible","tadmor2011"], ref="2 Kings 15:30",
   claims=[["The Bible says Hoshea killed Pekah.",T,["bible"]],["Assyria says it put Hoshea on the throne.",A,["tadmor2011"]],["Both may be true.",D,["tadmor2011","becking1992"]]]),
 B("Imagine families from Galilee on the long road east, children on donkeys, looking back at the hills.", S,
   vis=[fo([36.5,33.6],4.0,["galilee"])]),
]
TIG[0]["chapter"] = "Tiglath-pileser III"

FALL = [
 B("For some years Hoshea pays. Then he stops, and sends messengers to So, king of Egypt.", T, ["bible"], ref="2 Kings 17:3–4",
   vis=[yr(-725), fo([33.5,31.0],2.8,["samaria","egypt"])], amb="desert"),
 B("Who So was is debated. Kenneth Kitchen thought of Osorkon the Fourth, a pharaoh in the Delta. Others read So as the city of Sais.", D, ["kitchen1996","becking1992"],
   note="Osorkon: o-SOR-kon. Sais: SAY-iss."),
 B("Shalmaneser the Fifth arrests Hoshea, and lays siege to Samaria.", T, ["bible"], ref="2 Kings 17:4–5",
   vis=[yr(-724), fo(P["samaria"],14,["samaria"]),
        {"type":"battle","at":P["samaria"],"label":"Siege of Samaria (c. 724–722 BC)","cert":"attested",
         "arrows":[{"path":[[35.5,32.45],[35.3,32.33],[35.21,32.28]],"side":"enemy","cert":"attested"}],"sfx":"battle","sfxHold":3000}]),
 B("A Babylonian chronicle gives Shalmaneser's reign one line of war. He ravaged Shamarain. Most scholars read the name as Samaria.", A, ["grayson1975","becking1992"],
   claims=[["A Babylonian chronicle gives Shalmaneser's reign one line of war. He ravaged Shamarain.",A,["grayson1975"]],
           ["Most scholars read the name as Samaria.",D,["becking1992","tadmor1958"]]],
   note="Shamarain: sha-ma-RAH-in."),
 B("Then Shalmaneser dies, and Sargon the Second takes the throne. On the walls of his new palace at Khorsabad, he writes: I besieged and conquered Samaria.", A, ["fuchs1994","frame2021"],
   vis=[yr(-722), fo(P["dursharrukin"],12,["dursharrukin"])], note="Khorsabad: KOR-sa-bad, Sargon's city Dur-Sharrukin."),
 B("I carried off twenty seven thousand two hundred and ninety people, and from them I formed a unit of fifty chariots.", A, ["fuchs1994","frame2021"],
   note="Sargon's numbers, quoted. Even, not dramatic."),
 B("On a prism found at Nimrud, the numbers differ. Twenty seven thousand two hundred and eighty people, and two hundred chariots.", A, ["gadd1954"],
   vis=[fo(P["kalhu"],12,["kalhu"])]),
 B("Hayim Tadmor argued that Samaria fell twice. Once to Shalmaneser, at the end of his reign, and once more to Sargon, after a revolt.", D, ["tadmor1958","becking1992"],
   note="Hayim Tadmor: HI-im tad-MOR."),
 B("In seven twenty BC, Hamath rose against Sargon, and Samaria and Damascus joined it. The battle was at Qarqar, where Ahab had stood a century and more before.", A, ["frame2021","naaman1990"],
   vis=[yr(-720), fo(P["qarqar"],10,["qarqar","hamath"]),
        {"type":"battle","at":P["qarqar"],"label":"Qarqar again (720 BC)","cert":"attested","sfx":"battle","sfxHold":2400}],
   note="A callback to Chapter 4."),
 B("Sargon says he resettled Samaria, made it greater than before, and set his own official over it as governor. Israel had become the Assyrian province of Samerina.", A, ["fuchs1994","frame2021","gadd1954"],
   vis=[fo(P["samaria"],9.0,["samaria","israelk"])], note="Samerina: sa-meh-REE-na."),
 B("On the summit of Samaria there is little sign of a great burning. Ron Tappy argues that the city was taken, not destroyed.", D, ["tappy2001"],
   vis=[fo(P["samaria"],24,["samaria"])], note="Ron Tappy: TAP-ee."),
 B("Imagine the gate of Samaria opening after three years, and the silence in the streets inside.", S),
]
FALL[0]["chapter"] = "The fall of Samaria"

EXILE = [
 B("The Bible says the king of Assyria carried Israel away, and placed them in Halah, on the Habor, the river of Gozan, and in the cities of the Medes.", T, ["bible"], ref="2 Kings 17:6",
   vis=[fo([41.5,34.8],1.9,["samaria","gozan","media"]),
        {"type":"migration","label":"Deported to Gozan (tradition and Assyrian texts)","cert":"attested","path":[P["samaria"],[36.4,34.5],[38.2,36.3],P["gozan"]],"sfx":"migration","sfxHold":2000},
        {"type":"migration","label":"Deported to Media (tradition)","cert":"tradition","path":[P["samaria"],[39.0,34.0],[44.5,35.2],P["media"]],"sfx":"migration","sfxHold":2000}],
   amb="desert", note="Halah: HAY-la. Habor: HAY-bor. Gozan: GO-zan, Tell Halaf in Syria."),
 B("Assyrian documents bear this out. Names built with the name of Israel's God turn up in the following years at Gozan, at Kalhu, and in other cities of Assyria.", A, ["oded1979","younger1998","becking1992"],
   vis=[fo(P["gozan"],10,["gozan","kalhu"])]),
 B("At Kalhu, lists of the royal army name a unit of Samarian charioteers, serving the king of Assyria.", A, ["dalley1985"],
   vis=[fo(P["kalhu"],12,["kalhu"])]),
 B("In their place, the Bible says, Assyria brought people from Babylon, Cuthah, Avva, Hamath and Sepharvaim, and settled them in the towns of Samaria.", T, ["bible"], ref="2 Kings 17:24",
   vis=[fo([40.0,33.6],1.9,["babylon","cuthah","samaria"]),
        {"type":"migration","label":"New settlers for Samaria (tradition and Assyrian texts)","cert":"attested","path":[P["cuthah"],[42.0,34.6],[38.5,35.0],[36.5,33.6],P["samaria"]],"sfx":"migration","sfxHold":2400}],
   note="Cuthah: KOO-tha. Sepharvaim: sef-ar-VAY-im."),
 B("Sargon's own words agree. He says he settled people from the lands he had conquered there, and later Arab tribes from the desert.", A, ["frame2021","fuchs1994"]),
 B("How many left? Assyria's own figure is only a part of the kingdom's people. K. Lawson Younger and others think many Israelites stayed on the land.", D, ["younger1998","gadd1954"],
   note="Lawson Younger: LAW-son YUNG-er."),
 B("The Bible explains the fall in a long sermon. Israel had served other gods, and would not listen to the prophets.", T, ["bible"], ref="2 Kings 17:7–23"),
 B("It tells how the new settlers feared the God of the land, and were taught by an Israelite priest sent back to Bethel.", T, ["bible"], ref="2 Kings 17:25–28",
   vis=[fo(P["bethel"],18,["bethel"])]),
 B("Later Jewish writings call the Samaritans Kutim, people from Cuthah. The Samaritans tell their own story. They descend, they say, from Israelites who never left, and their holy mountain is Gerizim.", A, ["pummer2016"],
   vis=[fo(P["gerizim"],18,["gerizim","samaria"])], note="Kutim: koo-TEEM. Gerizim: GEH-ri-zim. Their own account, told plainly."),
 B("A small Samaritan community still lives there today.", A, ["pummer2016"]),
 B("And Jewish tradition remembers the ten lost tribes, carried away and never seen again. Rabbi Akiva taught that they would not return.", T, ["mishnahsanh","je1906lost"],
   note="Akiva: a-KEE-va."),
 B("Imagine a family in Gozan, far from the hills of Samaria, giving their child a name with the name of Israel's God in it.", S,
   vis=[fo(P["gozan"],14,["gozan"])]),
]
EXILE[0]["chapter"] = "Exile"

JUDAH = [
 B("In the south, Judah survives, as a vassal of Assyria. Sargon calls himself the subduer of Judah, which lies far away.", A, ["frame2021"],
   vis=[fo([35.2,31.7],6.0,["judah","jerusalem"])], amb="desert", note="Quotation from Sargon's Nimrud inscription."),
 B("Jerusalem grows fast in these years, onto the western hill. Some archaeologists think refugees from the north came with it. Nadav Na'aman doubts it.", D, ["broshi1992","naaman2007"],
   vis=[fo(P["jerusalem"],24,["jerusalem"])], note="Nadav Na'aman: na-DAHV na-a-MAHN."),
 B("The Bible says Judah's next king, Hezekiah, sent letters to the north as well, inviting Ephraim and Manasseh to keep the Passover in Jerusalem.", T, ["bible"], ref="2 Chronicles 30:1–11",
   note="Hezekiah: hez-eh-KY-a."),
 B("But Assyria is not done with Judah. In seven oh one BC, a new king, Sennacherib, will march on Jerusalem. That is where our next chapter begins.", A, ["grayson2012"],
   claims=[["In seven oh one BC, a new king, Sennacherib, will march on Jerusalem.",A,["grayson2012"]]],
   vis=[yr(-720), fo([38.5,33.6],2.0,["assyria","jerusalem"])],
   note="Chapter hook. Sennacherib: sen-AK-er-ib. Slow down on the last sentence, then stop."),
]
JUDAH[0]["chapter"] = "Judah alone"
PLAY = ARAM + JEROB + PROPH + TIG + FALL + EXILE + JUDAH
INTRO_BEATS = OPENER

# ---------- the map: Assyrian provinces replace Aram (732 BC), then Israel itself (722–720 BC) ----------
# Galilee, the Jezreel valley and Gilead (the provinces of Megiddo and Gilead; dashed, extent uncertain)
NORTHPROV = [[34.98,32.55],[35.0,33.05],[35.25,33.3],[35.6,33.35],[35.8,33.0],[35.78,32.62],[36.05,32.5],[36.0,32.1],[35.6,32.1],[35.55,32.15],[35.42,32.55],[34.98,32.55]]
PROV_STEP = {"type":"border","fade":[{"zone":"aram"}],"add":[
  {"zone":"assyria","certainty":"unsure","label":"ASSYRIAN PROVINCES","labelAt":[35.55,32.85],"coords":NORTHPROV},
  {"zone":"assyria","certainty":"unsure","label":"DAMASCUS","labelAt":[36.65,33.55],"coords":N930.ARAM_RING}],"sfx":"border"}
SAMERINA_STEP = {"type":"border","fade":[{"zone":"israel"}],"add":[
  {"zone":"assyria","certainty":"unsure","label":"SAMERINA","labelAt":[35.24,32.22],"coords":N1000.NORTH}],"sfx":"border"}
def _at(start): return next(b for b in PLAY if b["steps"][-1]["text"].startswith(start))
_b = _at("Israel loses Galilee and Gilead"); _b["steps"].insert(len(_b["steps"]) - 1, PROV_STEP)
_b = _at("Sargon says he resettled Samaria"); _b["steps"].insert(len(_b["steps"]) - 1, SAMERINA_STEP)

# ---------- subtitles: digits for the eye, words for the ear ----------
DIGITS = [("in eight forty one BC","in 841 BC"), ("seven twenty two BC","722 BC"), ("Shalmaneser the Fifth","Shalmaneser V"),
  ("Sargon the Second","Sargon II"), ("fifty horsemen, ten chariots and ten thousand foot soldiers","50 horsemen, 10 chariots and 10,000 foot soldiers"),
  ("Adad-nirari the Third","Adad-nirari III"), ("Jeroboam the Second","Jeroboam II"), ("forty one years","41 years"),
  ("in nineteen oh four","in 1904"), ("In seven forty five BC","In 745 BC"), ("Tiglath-pileser the Third","Tiglath-pileser III"),
  ("a thousand talents","1,000 talents"), ("In seven thirty two BC","In 732 BC"), ("Osorkon the Fourth","Osorkon IV"),
  ("twenty seven thousand two hundred and ninety people","27,290 people"), ("a unit of fifty chariots","a unit of 50 chariots"),
  ("Twenty seven thousand two hundred and eighty people, and two hundred chariots","27,280 people, and 200 chariots"),
  ("In seven twenty BC","In 720 BC"), ("In seven oh one BC","In 701 BC")]
def displayed(t):
    for a, b in DIGITS: t = t.replace(a, b)
    return t
for b in INTRO_BEATS + PLAY:
    c = b["steps"][-1]; assert c["type"] == "caption"
    assert not re.search(r"[()\d]", c["text"]), c["text"]
    d = displayed(c["text"])
    if d != c["text"]: c["display"] = d
for a, _ in DIGITS: assert any(a in b["steps"][-1]["text"] for b in INTRO_BEATS + PLAY), a

speech, clean = N1000.speech, N1000.clean
