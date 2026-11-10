"""Narration for the 701 BC stop of the Story of the Jews ("Chapter 6", Sennacherib at Jerusalem): the opening film
(transitionIn) and Play (c. 715 BC to 701 BC, with an epilogue to 681 BC). Same format and rules as
build/narration_jews_722.py: one beat = one spoken line = one mp3 in assets/narration/ (recorded with build/narrate.py).
Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film only).
Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
The opener starts at the end (701 BC: Sennacherib at Lachish, Hezekiah in Jerusalem), then goes back to Hezekiah's
first years. Told from the side of Judah; Assyria speaks in its own inscriptions and reliefs, Egypt through
Herodotus. The two endings at Jerusalem (the Bible's and Sennacherib's) are told side by side. The chapter ends on
a teaser for the next one (Babylon, 586 BC).
"""
import re
import narration_jews_1000 as N1000, narration_jews_722 as N722
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
cap, fo, yr, B = N1000.cap, N1000.fo, N1000.yr, N1000.B

# coordinates [lon, lat]; existing repo objects keep repo values; new ones as in build/objects.py
P = dict(N722.P, **{"lachish":[34.849,31.565], "azekah":[34.936,31.700], "beersheba":[34.840,31.245], "siloam":[35.2357,31.7718],
     "nineveh":[43.15,36.36], "ekron":[34.85,31.78], "ashdod":[34.66,31.76], "ashkelon":[34.55,31.66], "gaza":[34.46,31.50],
     "byblos":[35.65,34.12], "eltekeh":[34.80,31.86], "memphis":[31.25,29.85], "napata":[31.83,18.53]})

# ---------- the map: Judah in the late 8th century BC (hills, lowlands and Negev), and what it lost in 701 BC ----------
JUDAH701 = [[35.5241,31.865],[35.5,31.6],[35.4,31.3],[35.1,31.1],[34.75,31.2],[34.80,31.33],[34.78,31.55],[34.85,31.75],[34.93,31.865],[35.5241,31.865]]
JUDAH_AFTER = [[35.5241,31.865],[35.5,31.6],[35.4,31.3],[35.1,31.1],[34.75,31.2],[34.80,31.33],[34.98,31.42],[34.9244,31.865],[35.5241,31.865]]
SHEPH = [[34.9244,31.865],[34.98,31.42],[34.80,31.33],[34.78,31.55],[34.85,31.75],[34.93,31.865],[34.9244,31.865]]
JUDAH_STEP = {"type":"border","fade":[{"zone":"judah"}],"add":[
  {"zone":"judah","certainty":"people","label":"JUDAH","labelAt":[35.13,31.5],"coords":JUDAH701}],"sfx":"border"}
LOSS_STEP = {"type":"border","fade":[{"zone":"judah"}],"add":[
  {"zone":"judah","certainty":"people","label":"JUDAH","labelAt":[35.2,31.55],"coords":JUDAH_AFTER},
  {"zone":"philistia","certainty":"unsure","label":"TO ASHDOD, EKRON, GAZA","labelAt":[34.86,31.6],"coords":SHEPH}],"sfx":"border"}

# ---------------- opening film (transitionIn) ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. Hezekiah of Judah, and the king of Assyria at his gates.", F, vis=[yr(-701), fo([37.5,33.6],2.0,["jerusalem","assyria"])], amb="desert",
   note="Title card. Warm, no long silence after it."),
 B("Our last chapter ended around seven twenty BC. Samaria had fallen, and Judah stood alone in the hills.", F,
   vis=[yr(-720), fo([35.3,32.0],5.0,["samaria","jerusalem"])], note="Picks up the end of Chapter 5."),
 B("Now it is seven oh one BC. An Assyrian army is in Judah, and its king, Sennacherib, has made his camp at Lachish.", A, ["grayson2012","bmlachish","ussishkin2004"],
   vis=[yr(-701), fo(P["lachish"],18,["lachish"])], note="Sennacherib: sen-AK-er-ib."),
 B("In Jerusalem, King Hezekiah is shut up behind his walls.", A, ["grayson2012"],
   vis=[fo(P["jerusalem"],18,["jerusalem"])], note="Hezekiah: hez-eh-KY-a."),
 B("How did a small kingdom in the hills come to defy the greatest empire of its time? To find out, we go back some fifteen years.", F,
   vis=[yr(-715), fo([37.0,33.4],2.4,["jerusalem","nineveh"])]),
 B("On the map, Judah, from the hills down to the lowlands and the Negev. On the coast, the Philistine cities. And where Israel was, the Assyrian province of Samerina.", A, ["finknaaman2004","ussishkin2004","frame2021"],
   vis=[fo([35.0,31.7],5.2,["judah","ekron","ashdod","samaria"]), JUDAH_STEP], note="Samerina: sa-meh-REE-na."),
 B("Far to the east lies Assyria. And in Egypt, kings from Kush, far up the Nile, now rule the whole country.", A, ["kitchen1996","grayson2012"],
   vis=[fo([36.0,31.0],1.5,["assyria","egypt","napata"])], note="Kush: KOOSH."),
 B("That is the world of this chapter. Now the story begins.", F,
   vis=[fo([35.1,31.6],4.0)]),
]
OPENER[0]["chapter"] = "The world of 701 BC"

# ---------------- Play: c. 715 BC to 701 BC (epilogue to 681 BC) ----------------
HEZ = [
 B("Hezekiah, son of Ahaz, becomes king of Judah. The Bible says he trusted in the Lord, the God of Israel, so that there was none like him among all the kings of Judah.", T, ["bible"], ref="2 Kings 18:1–5",
   vis=[yr(-715), fo(P["jerusalem"],14,["jerusalem"])], amb="desert", note="The date of his accession is debated; the Bible gives two systems."),
 B("It says he removed the high places, and broke in pieces the bronze serpent that Moses had made, because the people burned incense to it.", T, ["bible"], ref="2 Kings 18:4"),
 B("At Beersheba, in the south, archaeologists found the stones of a large horned altar, taken apart and built into the wall of a storehouse.", A, ["aharoni1974","herzog2010"],
   vis=[fo(P["beersheba"],16,["beersheba"])], note="Beersheba: beer-SHEE-ba."),
 B("Some link it with Hezekiah's reform. Nadav Na'aman and others doubt that a reform like the one in Kings ever took place.", D, ["herzog2010","naaman1995"],
   note="Nadav Na'aman: na-DAHV na-a-MAHN."),
 B("In two thousand and nine, in a rubbish heap at the foot of the Temple Mount, a tiny clay seal impression was found. It reads: belonging to Hezekiah, son of Ahaz, king of Judah.", A, ["mazar2015"],
   vis=[fo(P["jerusalem"],24,["jerusalem"])]),
 B("On the coast, Ashdod rebels against Sargon of Assyria, and looks to Egypt for help.", A, ["frame2021"],
   vis=[yr(-712), fo(P["ashdod"],10,["ashdod"])], note="Sargon: SAR-gon."),
 B("The Bible says that in that year the prophet Isaiah walked naked and barefoot for three years, as a sign. Whoever trusts in Egypt and Kush will be put to shame.", T, ["bible"], ref="Isaiah 20:1–5",
   note="Isaiah 20 is the only place in the Bible that names Sargon."),
 B("Sargon's army takes Ashdod. Its king, Yamani, flees to the land of Kush.", A, ["frame2021","frame1999"],
   vis=[fo([33.0,29.5],2.2,["ashdod","egypt"]),
        {"type":"migration","label":"Yamani flees to Kush (c. 711 BC)","cert":"attested","path":[P["ashdod"],[33.5,30.8],[31.6,29.6],[31.2,27.0]],"sfx":"migration","sfxHold":1800}],
   note="Yamani: ya-MAH-nee."),
 B("A rock inscription of Sargon, high in the mountains of Iran, tells the end. Shebitku, king of Kush, sent Yamani back to Assyria in chains.", A, ["frame1999"],
   note="Shebitku: sheh-BIT-koo."),
 B("Imagine the news reaching Jerusalem, of a rebel king sent back in chains by the very land he trusted.", S,
   vis=[fo(P["jerusalem"],10,["jerusalem"])]),
]
HEZ[0]["chapter"] = "Hezekiah's Judah"

REVOLT = [
 B("In seven oh five BC, Sargon is killed in battle, far away in the mountains of Anatolia. His body is never recovered.", A, ["frame2021"],
   vis=[yr(-705), fo([38.0,36.0],2.0,["assyria"])]),
 B("His son Sennacherib becomes king, and moves the capital to Nineveh. All over the empire, subject kings see their chance.", A, ["grayson2012"],
   vis=[fo(P["nineveh"],8,["nineveh"])]),
 B("In the west, Sidon, Ashkelon and Judah stop paying tribute to Assyria, and look to Egypt for help.", A, ["grayson2012"],
   vis=[yr(-703), fo([35.0,32.6],3.4,["sidon","ashkelon","jerusalem","egypt"])]),
 B("At Ekron, the nobles depose their king, Padi, who is loyal to Assyria, and hand him over to Hezekiah in chains.", A, ["grayson2012"],
   vis=[fo(P["ekron"],14,["ekron","jerusalem"]),
        {"type":"migration","label":"Padi of Ekron handed to Hezekiah","cert":"attested","path":[P["ekron"],[35.05,31.8],P["jerusalem"]],"sfx":"migration","sfxHold":1400}],
   note="Padi: PAH-dee."),
 B("Hezekiah prepares for war. The Bible says he rebuilt the broken walls, made weapons and shields in great numbers, and stopped up the springs outside the city.", T, ["bible"], ref="2 Chronicles 32:2–5",
   vis=[fo(P["jerusalem"],18,["jerusalem"])]),
 B("Why should the kings of Assyria come, and find much water?", T, ["bible"], ref="2 Chronicles 32:4", note="Quotation."),
 B("In the Jewish Quarter of Jerusalem, Nahman Avigad uncovered a city wall about seven metres thick, built over houses that had been torn down to make room for it.", A, ["avigad1983"],
   vis=[fo(P["jerusalem"],26,["jerusalem"])], note="Nahman Avigad: NAKH-man a-vee-GAD."),
 B("Avigad compared it with words of Isaiah. You counted the houses of Jerusalem, and broke down the houses to fortify the wall.", D, ["avigad1983","bible"], ref="Isaiah 22:10",
   claims=[["Avigad compared it with words of Isaiah.",D,["avigad1983"]],["You counted the houses of Jerusalem, and broke down the houses to fortify the wall.",T,["bible"]]]),
 B("Under the City of David, a tunnel more than five hundred metres long carries the water of the Gihon spring to a pool inside the walls.", A, ["frumkin2003","siloam"],
   vis=[fo(P["siloam"],28,["siloamtunnel","jerusalem"])], note="Gihon: GEE-hon."),
 B("Writing cut into its wall tells how two teams dug through the rock towards each other, axe against axe, until they met, and the water flowed.", A, ["siloam","ahituv2008"]),
 B("The Bible says Hezekiah made the pool and the conduit, and brought water into the city.", T, ["bible"], ref="2 Kings 20:20"),
 B("Radiocarbon dates from the tunnel's plaster point to about seven hundred BC. Ronny Reich and Eli Shukron argue that the work began earlier.", D, ["frumkin2003","reich2011"],
   claims=[["Radiocarbon dates from the tunnel's plaster point to about 700 BC.",A,["frumkin2003"]],["Ronny Reich and Eli Shukron argue that the work began earlier.",D,["reich2011"]]],
   note="Ronny Reich: RYKH. Eli Shukron: shoo-KRON."),
 B("All over Judah, the handles of large storage jars carry a royal stamp: belonging to the king, with the name of a place, such as Hebron.", A, ["lipschits2010","ahituv2008"],
   vis=[fo([35.0,31.5],7.0,["judah","hebron"])]),
 B("Many link the jars with Hezekiah's preparations for war. Oded Lipschits and others think the system began earlier, when Judah first paid tribute to Assyria.", D, ["lipschits2010"],
   note="Oded Lipschits: o-DED LIP-shits."),
 B("Imagine the sound of picks deep in the rock, and two teams of diggers listening for each other through the stone.", S,
   vis=[fo(P["siloam"],24,["siloamtunnel"])]),
]
REVOLT[0]["chapter"] = "The great revolt"

MARCH = [
 B("In seven oh one BC, Sennacherib marches west.", A, ["grayson2012"],
   vis=[yr(-701), fo([39.5,34.8],1.9,["nineveh","sidon"]),
        {"type":"migration","label":"Sennacherib marches west (701 BC)","cert":"attested","path":[P["nineveh"],[40.5,36.7],[37.5,36.3],[36.4,34.8],P["sidon"]],"sfx":"migration","sfxHold":2400}]),
 B("Luli, king of Sidon, flees across the sea, and the cities of the Phoenician coast submit.", A, ["grayson2012"],
   vis=[fo([34.5,34.0],4.0,["sidon","cyprus"])], note="Luli: LOO-lee."),
 B("An army from Egypt and Kush comes north to help Ekron. Sennacherib meets it on the plain of Eltekeh, and claims the victory.", A, ["grayson2012"],
   vis=[fo([34.8,31.8],9,["ekron"]),
        {"type":"battle","at":P["eltekeh"],"label":"Eltekeh (701 BC; site uncertain)","cert":"attested",
         "arrows":[{"path":[[34.55,31.45],[34.7,31.7],[34.78,31.84]],"side":"egypt","cert":"attested"},{"path":[[34.85,32.1],[34.81,31.9]],"side":"enemy","cert":"attested"}],"sfx":"battle","sfxHold":2400}],
   note="Eltekeh: el-TEK-eh."),
 B("The Bible remembers Tirhakah, king of Kush, coming out to fight him. Kenneth Kitchen thought he led the army as a young prince, and was named by his later title.", D, ["bible","kitchen1996"], ref="2 Kings 19:9",
   claims=[["The Bible remembers Tirhakah, king of Kush, coming out to fight him.",T,["bible"]],["Kenneth Kitchen thought he led the army as a young prince, and was named by his later title.",D,["kitchen1996"]]],
   note="Tirhakah: tir-HAH-ka (Taharqa)."),
 B("Sennacherib takes Ekron, punishes the nobles who rebelled, and puts Padi back on his throne.", A, ["grayson2012"],
   vis=[fo(P["ekron"],14,["ekron"])]),
 B("Imagine the watchmen on Judah's hills, seeing the dust of an army rising over the coastal plain.", S,
   vis=[fo([34.95,31.7],8,["azekah"])]),
]
MARCH[0]["chapter"] = "Sennacherib marches"

LACHISH = [
 B("Then he turns on Judah. Forty six of Hezekiah's walled cities, he writes, and small towns without number, I besieged and conquered.", A, ["grayson2012"],
   vis=[fo([35.0,31.55],6.0,["judah","lachish","azekah"])], note="Quotation from Sennacherib's annals."),
 B("He claims he carried off two hundred thousand one hundred and fifty people, young and old, with horses, mules, donkeys, camels, cattle and sheep beyond counting.", A, ["grayson2012"]),
 B("Many historians think the figure is far too high for the whole of Judah. It may count everyone and everything taken as booty, or it may simply be a boast.", D, ["grabbe2003","broshi1992"]),
 B("A broken Assyrian tablet tells of the siege of Azekah, a fortress high on a ridge above the Elah valley, taken with ramps and battering rams.", A, ["naaman1974"],
   vis=[fo(P["azekah"],18,["azekah"])], note="Azekah: a-ZAY-ka."),
 B("The greatest prize was Lachish, Judah's second city, guarding the road from the coast into the hills.", A, ["ussishkin2004"],
   vis=[fo(P["lachish"],16,["lachish"]),
        {"type":"battle","at":P["lachish"],"label":"Siege of Lachish (701 BC)","cert":"attested",
         "arrows":[{"path":[[34.75,31.48],[34.82,31.54],[34.845,31.562]],"side":"enemy","cert":"attested"}],"sfx":"battle","sfxHold":3000}],
   note="Lachish: LAY-kish."),
 B("The Bible says Sennacherib himself was at Lachish, and sent his officers from there to Jerusalem.", T, ["bible"], ref="2 Kings 18:14, 17"),
 B("At the south-west corner of the mound, archaeologists found the Assyrian siege ramp, a great slope of stones heaped against the wall. It is the oldest siege ramp known anywhere.", A, ["ussishkin2004","garfinkel2021"],
   vis=[fo(P["lachish"],26,["lachish"])]),
 B("Hundreds of iron arrowheads and sling stones were found on the slope, and the city of that time ended in fire.", A, ["ussishkin2004"]),
 B("In his palace at Nineveh, Sennacherib had the siege carved on the walls of one room, from the first assault to the end.", A, ["barnett1998","bmlachish"],
   vis=[fo(P["nineveh"],10,["nineveh"])]),
 B("Archers and slingers behind tall shields. Battering rams on the ramps. Defenders hurling torches from the towers. And families leaving through the gate, with carts and cattle, into exile.", A, ["barnett1998","bmlachish"]),
 B("The carvings also show prisoners being put to death before the king.", A, ["barnett1998"]),
 B("A caption above the throne reads: Sennacherib, king of the world, king of Assyria, sat on his throne, and the booty of Lachish passed before him.", A, ["barnett1998","bmlachish"],
   note="Quotation from the epigraph. Even, not grand."),
 B("Imagine a family walking out of the gate of Lachish with a cart, past the Assyrian archers, not looking back.", S,
   vis=[fo(P["lachish"],18,["lachish"])]),
]
LACHISH[0]["chapter"] = "Lachish"

JERUS = [
 B("Now Jerusalem. Sennacherib writes: Hezekiah himself I shut up in Jerusalem, his royal city, like a bird in a cage.", A, ["grayson2012"],
   vis=[fo(P["jerusalem"],14,["jerusalem"]),
        {"type":"migration","label":"Assyrian troops to Jerusalem","cert":"attested","path":[P["lachish"],[35.0,31.65],[35.15,31.72],P["jerusalem"]],"sfx":"migration","sfxHold":1800}],
   note="The most famous line of the annals. Slow."),
 B("I set up blockades against him, and made him dread leaving his city gate.", A, ["grayson2012"], note="Quotation."),
 B("The Bible tells that Hezekiah sent word to Lachish. I have done wrong. Withdraw from me, and whatever you lay on me, I will bear.", T, ["bible"], ref="2 Kings 18:14"),
 B("It says he paid three hundred talents of silver and thirty talents of gold, and stripped the gold from the doors of the temple.", T, ["bible"], ref="2 Kings 18:14–16"),
 B("Then Assyrian officers come to the wall of Jerusalem, and the Rabshakeh, the chief cupbearer, calls up to the people in their own language.", T, ["bible"], ref="2 Kings 18:17–28",
   vis=[fo(P["jerusalem"],22,["jerusalem"])], note="Rabshakeh: rab-SHAH-keh."),
 B("Hezekiah's officials beg him to speak Aramaic, so that the people on the wall will not understand. He shouts all the louder, in Judean.", T, ["bible"], ref="2 Kings 18:26–28"),
 B("Do not let Hezekiah deceive you. Has any of the gods of the nations saved its land from the hand of the king of Assyria?", T, ["bible"], ref="2 Kings 18:29, 33", note="Quotation, the Assyrian officer. Proud, not shouted."),
 B("Hezekiah tears his clothes and sends to the prophet Isaiah. Isaiah answers. He shall not come into this city, nor shoot an arrow there. For I will defend this city, to save it, for my own sake, and for my servant David's sake.", T, ["bible"], ref="2 Kings 19:1–2, 32–34",
   note="Quotation. Calm and certain."),
 B("Imagine the people on the wall, listening in silence, as the officer below shouts up at them.", S),
]
JERUS[0]["chapter"] = "A bird in a cage"

ENDS = [
 B("The Bible tells what came next. That night the angel of the Lord went out, and struck down a hundred and eighty five thousand in the camp of Assyria. And Sennacherib went home, and stayed at Nineveh.", T, ["bible"], ref="2 Kings 19:35–36",
   vis=[fo([35.2,31.75],10,["jerusalem"])]),
 B("Sennacherib tells it differently. After I left, he says, Hezekiah sent his tribute after me to Nineveh. Thirty talents of gold, eight hundred talents of silver, ivory couches, his own daughters, and singers, men and women.", A, ["grayson2012"],
   vis=[fo([39.5,34.6],1.9,["jerusalem","nineveh"]),
        {"type":"migration","label":"Hezekiah's tribute to Nineveh","cert":"attested","path":[P["jerusalem"],[36.5,33.6],[38.6,35.8],P["nineveh"]],"sfx":"migration","sfxHold":2000}]),
 B("On the gold, the two accounts agree. On the silver, they do not.", D, ["bible","grayson2012"],
   claims=[["Thirty talents of gold in both accounts.",A,["grayson2012","bible"]],["Three hundred talents of silver in the Bible, eight hundred in Sennacherib's annals.",A,["grayson2012","bible"]]]),
 B("And Sennacherib never says that he took Jerusalem.", A, ["grayson2012","grabbe2003"],
   vis=[fo(P["jerusalem"],16,["jerusalem"])]),
 B("Herodotus, writing about two and a half centuries later, heard a story from Egyptian priests. When Sennacherib marched against Egypt, mice came in the night and gnawed through his soldiers' bowstrings and shields.", T, ["herodotus"],
   vis=[fo([33.0,30.8],3.0,["egypt"])], note="Herodotus: heh-ROD-o-tus."),
 B("Why did Sennacherib leave Jerusalem standing? Some historians think of disease in his camp. Others think a vassal who paid was worth more to him than a ruined city.", D, ["grabbe2003","matty2016"]),
 B("Judah survived, but much smaller. Sennacherib says he cut off the towns he had taken, and gave them to the kings of Ashdod, Ekron and Gaza.", A, ["grayson2012"],
   vis=[fo([34.95,31.6],7.0,["judah","ashdod","ekron","gaza"]), LOSS_STEP]),
 B("Excavations show many towns of the lowlands destroyed in seven oh one, and only partly rebuilt in the decades that followed.", A, ["finknaaman2004"],
   vis=[fo(P["lachish"],12,["lachish","azekah"])]),
 B("Imagine the first morning after the army has gone, and the gates of Jerusalem opening again onto empty roads.", S,
   vis=[fo(P["jerusalem"],14,["jerusalem"])]),
]
ENDS[0]["chapter"] = "Two endings"

MEMORY = [
 B("Twenty years later, in six eighty one BC, Sennacherib was killed by his own son. A Babylonian chronicle records it, and the Bible tells it too: he was struck down while he worshipped in the house of his god.", A, ["grayson1975","bible"], ref="2 Kings 19:37",
   claims=[["Twenty years later, in 681 BC, Sennacherib was killed by his own son. A Babylonian chronicle records it.",A,["grayson1975"]],["He was struck down by his sons while he worshipped in the house of his god.",T,["bible"]]],
   vis=[yr(-681), fo(P["nineveh"],8,["nineveh"])]),
 B("In Jewish memory, the rescue of Jerusalem became a sign of God's care for his city. The Talmud even says that God wished to make Hezekiah the Messiah.", T, ["sanh94a"],
   vis=[fo(P["jerusalem"],12,["jerusalem"])], note="Talmud: TAL-mood."),
 B("Jerusalem had been spared. But a little more than a century later, a new power, Babylon, will come to its gates. That is where our next chapter begins.", A, ["grayson1975"],
   claims=[["A little more than a century later, Babylon will come to Jerusalem's gates.",A,["grayson1975"]]],
   vis=[yr(-681), fo([39.0,32.8],1.9,["jerusalem","babylon"])],
   note="Chapter hook. Slow down on the last sentence, then stop."),
]
MEMORY[0]["chapter"] = "Memory"
PLAY = HEZ + REVOLT + MARCH + LACHISH + JERUS + ENDS + MEMORY
INTRO_BEATS = OPENER

# ---------- subtitles: digits for the eye, words for the ear ----------
DIGITS = [("around seven twenty BC","around 720 BC"), ("it is seven oh one BC","it is 701 BC"), ("In two thousand and nine","In 2009"),
  ("In seven oh five BC","In 705 BC"), ("about seven metres thick","about 7 metres thick"), ("more than five hundred metres long","more than 500 metres long"),
  ("point to about seven hundred BC","point to about 700 BC"), ("In seven oh one BC","In 701 BC"), ("Forty six of Hezekiah's","46 of Hezekiah's"),
  ("two hundred thousand one hundred and fifty people","200,150 people"),
  ("three hundred talents of silver and thirty talents of gold","300 talents of silver and 30 talents of gold"),
  ("a hundred and eighty five thousand","185,000"), ("Thirty talents of gold, eight hundred talents of silver","30 talents of gold, 800 talents of silver"),
  ("destroyed in seven oh one","destroyed in 701 BC"), ("in six eighty one BC","in 681 BC"), ("some fifteen years","some 15 years")]
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

# ---------------- Quick version of Chapter 6 (about two and a half minutes; reel jews-701-quick), see build/quick.py ----------------
# Skeleton from the big fact boxes: Hezekiah, Ashdod and Yamani, the revolt, the wall and the tunnel, Lachish, the bird in a
# cage, the two endings, Judah made smaller (the Play's border step) and the closing line.
import quick as _quick
QUICK, QUICK_FROM = _quick.build(__import__(__name__), "Chapter 6 in brief",
    ["pl00","pl11","pl18","pl25","pl31","pl35","pl44","pl51","pl53","pl54","pl56","pl59","pl64"],
    ("Chapter Six, in two minutes.", [fo([35.6,32.0],2.4)]))
QUICK[-1]["pauseAfter"] = 2000  # the closing line (the Play's own last line) gets a longer breath before the map moves on
