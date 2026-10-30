"""Narration for the c. 930 BC stop of the Story of the Jews ("Chapter 4"): the opening film (transitionIn)
and Play (c. 930 BC to 841 BC). Same format and rules as build/narration_jews_1000.py:
one beat = one spoken line = one mp3 in assets/narration/ (recorded with build/narrate.py).
Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film only).
Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
Told from the side of Israel and Judah; the neighbours (Moab, Aram, Assyria, Tyre) speak in their own
words where their inscriptions survive. The Elijah stories are told as tradition, never as myth.
Camera: same zoom rules as Chapter 3 (js/app.js focusView). "note" is for the narrator only.
The chapter answers Chapter 3's hook (is Jerusalem on the Karnak list?) and ends on a teaser for
the next one (Assyria comes back; Samaria falls, c. 722 BC).
"""
import re
import narration_jews_1000 as N1000
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
cap, fo, yr, B = N1000.cap, N1000.fo, N1000.yr, N1000.B

# coordinates [lon, lat]; existing repo objects keep repo values; new ones as in build/objects.py
P = {"jerusalem":[35.235,31.777], "megiddo":[35.185,32.585], "thebes":[32.64,25.70], "gibeon":[35.186,31.848],
     "samaria":[35.195,32.276], "tirzah":[35.338,32.287], "jezreel":[35.328,32.558], "carmel":[35.05,32.733],
     "zarephath":[35.296,33.458], "ramah":[35.232,31.85], "dan":[35.652,33.249], "damascus":[36.29,33.51],
     "qarqar":[36.330,35.743], "hamath":[36.75,35.135], "kalhu":[43.329,36.098], "kurkh":[40.54,37.825],
     "dibon":[35.786,31.499], "ataroth":[35.665,31.574], "nebo":[35.725,31.767], "medeba":[35.80,31.717],
     "ajrud":[34.428,30.186], "ramothgilead":[36.017,32.5], "tyre":[35.19,33.27], "sidon":[35.37,33.56]}

# ---------------- opening film (transitionIn) ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. Two kingdoms, and the great powers around them.", F, vis=[yr(-930), fo([35.3,32.2],5.0,["israelk","judah"])], amb="desert",
   note="Title card. Warm, no long silence after it."),
 B("Our last chapter ended with a question. Is Jerusalem on the pharaoh's list at Karnak?", F,
   vis=[yr(-925), fo(P["thebes"],24,["thebes"])], amb="river", note="Picks up the hook of Chapter 3. Curious, not dramatic."),
 B("The list is long, and many names can still be read. Megiddo, Taanach, Beth-shean, Gibeon, and places across the Jordan.", A, ["wilson2005","kitchen1996"],
   vis=[fo([35.3,32.3],5.0,["megiddo","bethshean","gibeon"])]),
 B("Jerusalem is not among the names that survive. Many others are small places in the Negev.", A, ["wilson2005","finkpiasetzky2006"],
   vis=[fo([35.0,31.3],4.2,["jerusalem","negev"])]),
 B("Why? Some think Rehoboam paid the pharaoh, as the Bible says, and the city was spared. Others point out that parts of the list are broken, so it cannot settle the question.", D, ["kitchen1996","wilson2005"],
   claims=[["Why? Some think Rehoboam paid the pharaoh, as the Bible says, and the city was spared.",D,["kitchen1996","bible"]],
           ["Others point out that parts of the list are broken, so it cannot settle the question.",D,["wilson2005"]]],
   note="Two views, same weight. Rehoboam's payment: 1 Kings 14:25–26."),
 B("At Megiddo itself, a broken piece of stone with Shoshenq's name was found in the nineteen twenties. Egypt really did reach the valley.", A, ["bendorfink2023"],
   vis=[fo(P["megiddo"],24,["megiddo"])],
   note="Shoshenq: SHOW-shenk. The fragment was found in a dump by Fisher's team in 1925–26; whether it was a stele or a building inscription is debated."),
 B("Then Egypt turns inward again. The power that will come west instead is Assyria.", A, ["kitchen1996","grayson1996"],
   vis=[fo([38.5,33.0],1.9,["egypt","assyria"])]),
 B("On the map, two kingdoms. Israel in the north, larger and richer. Judah in the south, ruled from Jerusalem by the House of David.", A, ["fink2013","mazar2010","biran1995"],
   vis=[fo([35.3,32.2],5.0,["israelk","judah"])]),
 B("That is the world of this year. You can stay with the story, or explore the map on your own.", F,
   vis=[fo([35.6,32.4],3.6)]),
]
OPENER[0]["chapter"] = "The world of 930 BC"
OPENER[-1]["choice"] = True

# ---------------- Play: c. 930 BC to 841 BC ----------------
WAR = [
 B("For years, the Bible says, there is war between the two kingdoms. Rehoboam and Jeroboam, and then their heirs.", T, ["bible"], ref="1 Kings 14:30; 15:6–7, 16",
   vis=[yr(-910), fo([35.25,32.1],6.0,["israelk","judah"])], amb="desert"),
 B("Baasha of Israel fortifies Ramah, just north of Jerusalem, to close the road.", T, ["bible"], ref="1 Kings 15:16–17",
   vis=[fo(P["ramah"],24,["ramah","jerusalem"])]),
 B("Asa of Judah sends the silver and gold of the temple to the king of Aram in Damascus, and asks him to attack Israel from the north.", T, ["bible"], ref="1 Kings 15:18–19",
   vis=[fo([35.8,32.6],4.6,["jerusalem","damascus"]),
        {"type":"migration","label":"Asa's gift to Damascus (tradition)","cert":"tradition","path":[P["jerusalem"],[35.6,32.4],P["damascus"]],"sfx":"migration","sfxHold":1600}]),
 B("Ben-hadad of Damascus strikes the far north of Israel, at Dan and around the Sea of Galilee.", T, ["bible"], ref="1 Kings 15:20",
   vis=[fo([35.8,33.1],8.0,["dan","damascus","galilee"]),
        {"type":"migration","label":"Aram strikes the north (tradition)","cert":"tradition","path":[P["damascus"],[35.9,33.3],P["dan"]],"sfx":"migration","sfxHold":1400}]),
 B("Damascus is now the centre of a strong Aramean kingdom. It will shape this whole chapter.", A, ["aram","grayson1996"],
   vis=[fo(P["damascus"],8.0,["damascus","arameans"])]),
 B("In Israel, kings fall quickly. Baasha's son is murdered at Tirzah, the capital, and his killer, Zimri, rules for seven days.", T, ["bible"], ref="1 Kings 16:8–15",
   vis=[yr(-885), fo(P["tirzah"],24,["tirzah"])]),
 B("The army makes its commander king. His name is Omri. When Tirzah falls, Zimri sets the palace on fire around himself.", T, ["bible"], ref="1 Kings 16:16–18",
   note="Omri: OM-ree."),
 B("Imagine the smoke over Tirzah, and soldiers in the valley, wondering who their next king will be.", S,
   vis=[fo(P["tirzah"],18,["tirzah"])]),
]
WAR[0]["chapter"] = "Two kingdoms at war"

OMRI = [
 B("Omri buys a hill from a man named Shemer, for two talents of silver, and builds a new capital on it. He calls it Samaria.", T, ["bible"], ref="1 Kings 16:23–24",
   vis=[yr(-880), fo(P["samaria"],24,["samaria"])], amb="desert", note="Shemer: SHEH-mer. Samaria, in Hebrew Shomron."),
 B("On the summit, archaeologists found a royal compound, with walls of finely cut stone.", A, ["franklin2004","fink2000"]),
 B("Norma Franklin and Israel Finkelstein date its first building phase to Omri's dynasty. Details of the dating are still argued.", D, ["franklin2004","fink2000"]),
 B("Carved ivories were found there too, inlays for royal furniture in a Phoenician style. The Bible speaks of Ahab's house of ivory.", A, ["crowfoot1938","bible"],
   claims=[["Carved ivories were found there too, inlays for royal furniture in a Phoenician style.",A,["crowfoot1938"]],
           ["The Bible speaks of Ahab's house of ivory.",T,["bible"]]], ref="1 Kings 22:39; Amos 3:15",
   note="The ivories are dated 9th–8th century BC; which king owned them is open."),
 B("At Jezreel, by the great valley, a large walled enclosure with a moat was built in the same years, and destroyed not long after.", A, ["ussishkin1997"],
   vis=[fo(P["jezreel"],18,["jezreelcity","jezreel"])]),
 B("Finkelstein sees one style in these royal centres. Big platforms, walls with rooms inside them, and moats. He calls it Omride architecture.", D, ["fink2000"],
   vis=[fo([35.27,32.42],9.0,["samaria","jezreelcity","megiddo"])]),
 B("The Bible gives Omri only a few verses, and says he did evil in the eyes of the Lord, more than all before him.", T, ["bible"], ref="1 Kings 16:25–28"),
 B("Yet Assyria remembered him. Its scribes came to call Israel the House of Omri.", A, ["grayson1996"],
   vis=[fo([39.5,34.0],2.2,["samaria","assyria"])]),
 B("His son Ahab marries Jezebel, daughter of Ethbaal, king of the Sidonians, and builds a temple for Baal in Samaria.", T, ["bible"], ref="1 Kings 16:29–32",
   vis=[yr(-870), fo([35.25,32.9],7.0,["samaria","tyre","sidon"])], note="Jezebel: JEZ-eh-bel. Ethbaal: eth-BAAL."),
 B("Josephus, quoting a lost history of Tyre, names a king of Tyre called Ithobaal, a priest of Astarte. Many identify him with the Bible's Ethbaal.", A, ["josephusapion"],
   claims=[["Josephus, quoting a lost history of Tyre, names a king of Tyre called Ithobaal, a priest of Astarte.",A,["josephusapion"]],
           ["Many identify him with the Bible's Ethbaal.",D,["josephusapion"]]],
   vis=[fo(P["tyre"],18,["tyre"])], note="Against Apion 1.123. Ithobaal: ee-toh-BAAL."),
 B("Imagine the new capital on its hill. Cut stone glowing in the evening light, and the road west running down toward the sea.", S,
   vis=[fo(P["samaria"],18,["samaria"])]),
]
OMRI[0]["chapter"] = "The House of Omri"

ELIJAH = [
 B("Now the Bible turns to a prophet. Elijah the Tishbite, from Gilead, tells Ahab there will be no dew or rain, except by his word.", T, ["bible"], ref="1 Kings 17:1",
   vis=[yr(-865), fo([35.4,32.4],6.0,["samaria"])], amb="desert", note="Elijah: in Hebrew Eliyahu, 'my God is the Lord'. Tishbite: TISH-bite."),
 B("In the drought, ravens bring him bread and meat by a brook. Then a widow in Zarephath, near Sidon, shares her last flour and oil with him.", T, ["bible"], ref="1 Kings 17:2–16",
   vis=[fo(P["zarephath"],14,["zarephath","sidon"])], note="Zarephath: ZAR-eh-fath."),
 B("On Mount Carmel he calls the people to choose. How long will you waver between two opinions? If the Lord is God, follow him. If Baal, follow him.", T, ["bible"], ref="1 Kings 18:19–21",
   vis=[fo(P["carmel"],14,["carmel"])], note="Quotation. Direct, a challenge."),
 B("Fire falls on Elijah's altar, and the people fall on their faces. The Lord, he is God. The Lord, he is God.", T, ["bible"], ref="1 Kings 18:38–39",
   note="Slow on the repeated words."),
 B("Jews still say those words together, seven times, at the very end of Yom Kippur.", A, ["neilah623"],
   note="The close of Neilah, before the shofar."),
 B("Fleeing Jezebel, Elijah walks to Horeb, the mountain of God. There is wind, an earthquake and fire, but God is not in them. Then, a still, small voice.", T, ["bible"], ref="1 Kings 19:1–12",
   vis=[fo([34.5,30.5],3.6,["sinai"]),
        {"type":"migration","label":"Elijah walks to Horeb (tradition; place unknown)","cert":"tradition","path":[P["jezreel"],[34.80,31.24],[34.3,29.9]],"sfx":"migration","sfxHold":2000}],
   note="Quiet. The last three words almost a whisper."),
 B("At Jezreel, Ahab wants his neighbour Naboth's vineyard. Naboth will not sell the land of his fathers.", T, ["bible"], ref="1 Kings 21:1–3",
   vis=[fo(P["jezreel"],18,["jezreelcity"])], note="Naboth: NAY-both."),
 B("Jezebel has him falsely accused and stoned. And Elijah meets the king with a question. Have you murdered, and also taken possession?", T, ["bible"], ref="1 Kings 21:7–19"),
 B("Many scholars think the Elijah stories were shaped and written down long after Ahab's time, by later prophetic circles.", D, ["otto2003"]),
 B("Religion in Israel was more varied than the Bible's ideal. Inscriptions from Kuntillet Ajrud, in the Sinai, bless in the name of Yahweh of Samaria and his Asherah.", A, ["meshel2012"],
   claims=[["Religion in Israel was more varied than the Bible's ideal.",D,["meshel2012","smith2002"]],
           ["Inscriptions from Kuntillet Ajrud, in the Sinai, bless in the name of Yahweh of Samaria and his Asherah.",A,["meshel2012"]]],
   vis=[fo(P["ajrud"],10,["ajrud"])], note="From a little later, about 800 BC. Kuntillet Ajrud: koon-TILL-et ah-JROOD. What 'his Asherah' meant, a goddess or a sacred symbol, is debated."),
 B("The Bible says Elijah did not die. A chariot of fire took him up to heaven in a whirlwind.", T, ["bible"], ref="2 Kings 2:11",
   vis=[fo([35.55,31.9],8.0,["deadsea"])]),
 B("And the last of the prophets promises that God will send Elijah, before the great day of the Lord.", T, ["bible"], ref="Malachi 3:23 (4:5 in many English Bibles)"),
 B("So Elijah has a place at every Passover Seder, with a cup of wine poured for him, and a chair of his own at every circumcision.", A, ["ejelijahcup","jeelijahchair"]),
 B("Imagine a door opened at the Seder, and children watching, to see whether the prophet has come.", S),
]
ELIJAH[0]["chapter"] = "Elijah"

QARQAR = [
 B("Far to the east, Assyria is on the march again. Its new king, Shalmaneser the Third, crosses the Euphrates almost every year.", A, ["grayson1996","yamada2000"],
   vis=[yr(-858), fo([40.0,35.5],2.2,["assyria","kalhu","euphrates"])], amb="desert", note="Shalmaneser: shal-man-EE-zer."),
 B("In eight fifty three BC, he marches into Syria, toward Hamath.", A, ["grayson1996"],
   vis=[yr(-853), fo([39.5,35.6],2.4,["kalhu","hamath"]),
        {"type":"migration","label":"Shalmaneser III marches west (853 BC)","cert":"attested","path":[P["kalhu"],[40.0,36.6],[38.0,36.4],[37.15,36.2],P["qarqar"]],"sfx":"migration","sfxHold":2400}]),
 B("At Qarqar, on the Orontes river, twelve kings stand against him. They are led by Hadad-ezer of Damascus and Irhuleni of Hamath.", A, ["grayson1996","yamada2000"],
   vis=[fo(P["qarqar"],12,["qarqar","hamath","orontes"])], note="Qarqar: kar-KAR. Hadad-ezer: ha-dad-EH-zer. Irhuleni: ir-hoo-LEH-nee."),
 B("And the third king named is Ahab the Israelite, with two thousand chariots and ten thousand soldiers.", A, ["grayson1996","bmkurkh"],
   note="Ahab: AY-hab. The Kurkh Monolith, carved in 853 or 852 BC, now in the British Museum."),
 B("That is the biggest chariot force in the list. Nadav Na'aman thinks the number is a scribe's error, perhaps for two hundred.", D, ["naaman1976"]),
 B("Also in the line are troops from Egypt and Byblos, and a thousand camels of Gindibu the Arab. It is the first known mention of Arabs in any text.", A, ["grayson1996","ephal1982"],
   vis=[fo([36.2,34.6],5.0,["byblos","qarqar"])], note="Gindibu: gin-DEE-boo."),
 B("Shalmaneser claims a great victory. He says he dammed the Orontes with the bodies of his enemies.", A, ["grayson1996"],
   vis=[{"type":"battle","at":P["qarqar"],"label":"Battle of Qarqar (853 BC)","cert":"attested",
         "arrows":[{"path":[[36.9,35.95],[36.55,35.82],[36.38,35.76]],"side":"enemy","cert":"attested"}],"sfx":"battle","sfxHold":3000},
        fo(P["qarqar"],12,["qarqar"])], note="Assyrian boast, quoted. Not triumphant in the voice."),
 B("But he did not take Damascus or Hamath. He was back to fight the same alliance in eight forty nine, eight forty eight and eight forty five. Many historians see Qarqar as a check on Assyria, not a defeat for its enemies.", D, ["yamada2000","grayson1996"],
   claims=[["But he did not take Damascus or Hamath. He was back to fight the same alliance in eight forty nine, eight forty eight and eight forty five.",A,["grayson1996","yamada2000"]],
           ["Many historians see Qarqar as a check on Assyria, not a defeat for its enemies.",D,["yamada2000"]]]),
 B("The Bible does not mention Qarqar. It tells of Ahab's wars with Aram, and of his death in battle at Ramoth-gilead.", T, ["bible"], ref="1 Kings 20; 22:29–37",
   vis=[yr(-850), fo([35.7,32.5],6.0,["ramothgilead","samaria"])]),
 B("Some scholars think those war stories first belonged to later kings of Israel, and were set in Ahab's time when the books were put together.", D, ["miller1966"]),
 B("Imagine the plain by the Orontes at dawn. Dust from thousands of hooves, and kings from many lands, side by side, waiting.", S,
   vis=[fo(P["qarqar"],10,["qarqar"])]),
]
QARQAR[0]["chapter"] = "Qarqar, 853 BC"

MESHA = [
 B("East of the Dead Sea, Moab paid tribute to Israel. The Bible calls its king Mesha a sheep breeder, and says he rebelled after Ahab died.", T, ["bible"], ref="2 Kings 3:4–5",
   vis=[yr(-845), fo([35.75,31.6],7.0,["moab","dibon"])], amb="desert", note="Mesha: MAY-sha."),
 B("Mesha tells his own side, on a black stone at Dibon. Omri king of Israel oppressed Moab many days, for Chemosh was angry with his land.", A, ["dearman1989","louvremesha"],
   vis=[fo(P["dibon"],18,["dibon"])], note="Chemosh, Moab's god: KEE-mosh. Quotation from the stele, calm."),
 B("Omri's son, he says, also meant to oppress Moab. But I triumphed over him and his house, and Israel has perished forever.", A, ["dearman1989"],
   note="Mesha's boast. Israel, of course, did not perish; no comment needed, the next lines show it."),
 B("Who that son was, Ahab or a later king of the house, is debated. Mesha's numbers do not fit the Bible's dates neatly.", D, ["dearman1989"]),
 B("He writes that the men of Gad had lived at Ataroth from of old, and that the king of Israel built it for them. Mesha took it.", A, ["dearman1989"],
   vis=[fo(P["ataroth"],18,["ataroth"])], note="Gad: one of the tribes of Israel. Ataroth: AT-a-roth."),
 B("Then Chemosh said to him, Go, take Nebo from Israel. He took it, and dragged the vessels of Yahweh before Chemosh.", A, ["dearman1989"],
   vis=[fo(P["nebo"],18,["nebo","medeba"])], note="Yahweh is read here as written on the stele. Neutral, not shocked."),
 B("It is one of the oldest mentions of Israel's God, by that name, outside the Bible.", A, ["dearman1989","louvremesha"]),
 B("In the Bible, Israel, Judah and Edom march around the Dead Sea against Moab. Mesha offers his eldest son on the city wall, and Israel withdraws.", T, ["bible"], ref="2 Kings 3:6–27",
   vis=[fo([35.6,31.0],6.0,["moab","edom","deadsea"]),
        {"type":"migration","label":"Israel, Judah and Edom march on Moab (tradition)","cert":"tradition","path":[P["jerusalem"],[35.35,31.0],[35.5,30.95],[35.73,31.2]],"sfx":"migration","sfxHold":2000}],
   note="Hard line. Plain and quiet, no emphasis."),
 B("The stone was found in eighteen sixty eight. It was smashed soon after, but a paper squeeze taken before saved most of the text, and the pieces are now in the Louvre.", A, ["louvremesha","dearman1989"],
   vis=[fo(P["dibon"],18,["dibon"])], note="Squeeze: a wet paper impression of the letters."),
 B("Imagine a scholar in Jerusalem, smoothing out a torn paper copy, letter by letter.", S),
]
MESHA[0]["chapter"] = "Mesha of Moab"

JEHU = [
 B("In Damascus, Hadad-ezer dies. Shalmaneser writes: Hazael, son of a nobody, took the throne.", A, ["grayson1996"],
   vis=[yr(-842), fo(P["damascus"],12,["damascus"])], amb="desert", note="Hazael: HAZ-ay-el. 'Son of a nobody' is the Assyrian way to call him a usurper."),
 B("The Bible tells it from Israel's side. The prophet Elisha weeps as he foresees what Hazael will do to Israel, and Hazael kills his master.", T, ["bible"], ref="2 Kings 8:7–15",
   note="Elisha: eh-LIE-sha, Elijah's disciple."),
 B("In Israel, a prophet's messenger anoints an army commander, Jehu. He drives his chariot furiously to Jezreel.", T, ["bible"], ref="2 Kings 9:1–20",
   vis=[yr(-841), fo(P["jezreel"],18,["jezreelcity","ramothgilead"]),
        {"type":"migration","label":"Jehu rides to Jezreel (tradition)","cert":"tradition","path":[P["ramothgilead"],[35.6,32.52],P["jezreel"]],"sfx":"migration","sfxHold":1600}],
   note="Jehu: JAY-hoo. 'Furiously' with energy."),
 B("There he kills Joram, Ahab's son and king of Israel, and Ahaziah, king of Judah. Jezebel is thrown from a window.", T, ["bible"], ref="2 Kings 9:21–37",
   note="Joram: JOR-am. Ahaziah: a-ha-ZY-a."),
 B("Jehu ends the House of Omri, and tears down the temple of Baal in Samaria.", T, ["bible"], ref="2 Kings 10:1–28",
   vis=[fo(P["samaria"],18,["samaria"])]),
 B("But at Dan, an Aramean king tells another story. In broken lines, he says he killed the king of Israel and the king of the House of David.", A, ["biran1995"],
   vis=[fo(P["dan"],18,["dan"])]),
 B("The names are restored. Many read Joram son of Ahab, and Ahaziah. If so, the Aramean king, very likely Hazael, claims the deaths that the Bible gives to Jehu.", D, ["biran1995","schniedewind1996"]),
 B("William Schniedewind suggests both may be right in part. Jehu may have acted as Hazael's ally.", D, ["schniedewind1996"]),
 B("In the years after, the Bible says, Hazael takes Israel's lands east of the Jordan, all of Gilead.", T, ["bible"], ref="2 Kings 10:32–33",
   vis=[fo([36.2,33.0],4.4,["aramdamascus","damascus"])]),
 B("And in the same year, eight forty one, Shalmaneser comes back. Hazael is shut up in Damascus, and the kings of the coast bring tribute.", A, ["grayson1996"],
   vis=[fo([36.0,33.6],4.6,["damascus","tyre","sidon"]),
        {"type":"migration","label":"Shalmaneser III returns (841 BC)","cert":"attested","path":[P["kalhu"],[40.0,36.6],[37.3,35.6],[36.6,34.4],P["damascus"]],"sfx":"migration","sfxHold":2400}]),
 B("On the Black Obelisk from Nimrud, a man kneels before the Assyrian king. The words above him say: tribute of Jehu, of the House of Omri.", A, ["bmblackobelisk","grayson1996"],
   vis=[fo(P["kalhu"],10,["kalhu"])],
   note="Whether the kneeling man is Jehu himself or his envoy is not certain. 'Of the House of Omri', even though Jehu ended that house: to Assyria, Israel was still Omri's land."),
 B("Silver, gold, a golden bowl, golden vessels, tin, and spears. Israel now pays Assyria.", A, ["grayson1996"]),
 B("Imagine envoys from Samaria, kneeling in a palace far from home, their gifts laid out on the floor.", S),
 B("Assyria now knows the road west. When it comes back in force, Samaria itself will stand in its path. That is where our next chapter begins.", A, ["grayson1996"],
   claims=[["Assyria now knows the road west.",A,["grayson1996"]]],
   vis=[fo([39.5,34.2],2.0,["assyria","samaria"])],
   note="Chapter hook. Slow down on the last two sentences, then stop."),
]
JEHU[0]["chapter"] = "Jehu and Hazael"
PLAY = WAR + OMRI + ELIJAH + QARQAR + MESHA + JEHU
INTRO_BEATS = OPENER

# Aram-Damascus under Hazael: a dashed, uncertain area east of the Jordan (index.html .z-aram)
ARAM_RING = [[35.78,32.62],[35.82,33.45],[36.1,34.0],[36.6,34.4],[37.3,34.0],[37.25,33.1],[36.6,32.6],[36.05,32.5],[35.78,32.62]]
ARAM_STEP = {"type":"border","add":[{"zone":"aram","certainty":"unsure","label":"ARAM-DAMASCUS","labelAt":[36.65,33.55],"coords":ARAM_RING}],"sfx":"border"}
_b = next(b for b in PLAY if b["steps"][-1]["text"].startswith("In the years after, the Bible says, Hazael"))
_b["steps"].insert(len(_b["steps"]) - 1, ARAM_STEP)

# ---------- subtitles: digits for the eye, words for the ear ----------
DIGITS = [("in the nineteen twenties","in the 1920s"), ("Shalmaneser the Third","Shalmaneser III"),
  ("In eight fifty three BC","In 853 BC"), ("two thousand chariots and ten thousand soldiers","2,000 chariots and 10,000 soldiers"),
  ("perhaps for two hundred","perhaps for 200"), ("a thousand camels","1,000 camels"),
  ("in eight forty nine, eight forty eight and eight forty five","in 849, 848 and 845 BC"),
  ("in eighteen sixty eight","in 1868"), ("eight forty one","841 BC"), ("seven times","7 times")]
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
