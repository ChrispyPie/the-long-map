"""Narration for the 586 BC stop of the Story of the Jews ("Chapter 7", The First Temple destroyed): the opening film
(transitionIn) and Play (c. 687 BC to 586 BC, with an epilogue toward the exile and a teaser for Persia, 538 BC).
Same format and rules as build/narration_jews_701.py: one beat = one spoken line = one mp3 in assets/narration/
(recorded with build/narrate.py). Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame
(opening film only). Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
The opener starts at the end (586 BC: a Babylonian army at Jerusalem), then goes back to the years after 701 BC.
Told from the side of Judah; Babylon speaks in its own chronicles and ration tablets; the Bible is labelled tradition
where it is the only witness. The year of the fall (586 or 587 BC) is told as disputed. The chapter ends on a teaser
for the next one (Persia, 538 BC).
"""
import re
import narration_jews_1000 as N1000, narration_jews_701 as N701
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
cap, fo, yr, B = N1000.cap, N1000.fo, N1000.yr, N1000.B

P = dict(N701.P, **{"mizpah":[35.217,31.885], "riblah":[36.52,34.43], "arad":[35.146,31.281],
     "ketef":[35.226,31.768], "jericho":[35.444,31.855], "tahpanhes":[32.00,30.86],
     "hamath":[36.75,35.13], "babylon":[44.42,32.54], "alyahudu":[45.15,32.15],
     "media":[48.53,34.80]})

# smaller Judah as Chapter 6 left it; a remnant in Benjamin after 586 BC
JUDAH_AFTER = N701.JUDAH_AFTER
SHEPH = N701.SHEPH
BENJAMIN = [[35.26,31.96],[35.32,31.88],[35.28,31.78],[35.16,31.78],[35.14,31.90],[35.26,31.96]]
JUDAH_STEP = {"type":"border","fade":[{"zone":"judah"}],"add":[
  {"zone":"judah","certainty":"people","label":"JUDAH","labelAt":[35.2,31.55],"coords":JUDAH_AFTER}],"sfx":"border"}
LOSS_ALREADY = {"type":"border","fade":[],"add":[
  {"zone":"philistia","certainty":"unsure","label":"TO ASHDOD, EKRON, GAZA","labelAt":[34.86,31.6],"coords":SHEPH}],"sfx":None}
END_STEP = {"type":"border","fade":[{"zone":"judah"}],"add":[
  {"zone":"judah","certainty":"people","label":"THOSE WHO REMAINED","labelAt":[35.20,31.88],"coords":BENJAMIN}],"sfx":"border"}
PATH_WEST = {"type":"migration","label":"Nebuchadnezzar marches west (605–597 BC)","cert":"attested",
             "path":[P["babylon"],[43.5,34.2],[40.0,35.6],P["carchemish"] if False else [38.01,36.83]],"sfx":"migration","sfxHold":2000}
# carchemish is in N701? no, use literal
PATH_WEST["path"] = [P["babylon"],[43.5,34.2],[40.0,35.6],[38.01,36.83]]
PATH_597 = {"type":"migration","label":"Jehoiachin taken to Babylon (597 BC)","cert":"attested",
            "path":[P["jerusalem"],[35.5,32.4],[36.5,33.8],[38.01,36.83],[41.0,35.0],P["babylon"]],"sfx":"migration","sfxHold":2200}
PATH_586 = {"type":"migration","label":"Zedekiah taken to Riblah, then Babylon (586 BC)","cert":"tradition",
            "path":[P["jerusalem"],P["jericho"],[35.8,32.8],P["riblah"],[38.01,36.83],P["babylon"]],"sfx":"migration","sfxHold":2200}
PATH_EGYPT = {"type":"migration","label":"Flight to Egypt after Gedaliah's death","cert":"tradition",
              "path":[P["mizpah"],[34.8,31.5],[33.5,31.2],P["tahpanhes"]],"sfx":"migration","sfxHold":1800}

# ---------------- opening film (transitionIn) ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. The fall of Jerusalem, and the end of the First Temple.", F,
   vis=[yr(-586), fo([37.5,33.2],2.0,["jerusalem","babylon"])], amb="desert",
   note="Title card. Warm, no long silence after it."),
 B("Our last chapter ended in six eighty one BC. Sennacherib was dead, and Jerusalem had been spared.", F,
   vis=[yr(-681), fo([35.3,31.8],5.0,["jerusalem"])], note="Picks up the end of Chapter 6."),
 B("Now it is five eighty six BC. A Babylonian army is at Jerusalem, and the city is about to fall.", A, ["wiseman1956","lipschits2005","shiloh1984"],
   vis=[yr(-586), fo(P["jerusalem"],16,["jerusalem"])],
   claims=[["In 586 BC a Babylonian army is at Jerusalem, and the city is about to fall.",A,["wiseman1956","lipschits2005"]],
           ["The exact year, 586 or 587 BC, is disputed.",D,["galil1996","cogan1988"]]]),
 B("Inside the walls, the Temple that Jewish tradition says Solomon built still stands. It will not stand much longer.", T, ["bible"], ref="1 Kings 6; 2 Kings 25:9",
   vis=[fo(P["jerusalem"],20,["jerusalem"])],
   claims=[["The Temple that Jewish tradition says Solomon built still stands.",T,["bible"]],
           ["It will not stand much longer.",T,["bible"]]]),
 B("How did Judah, spared a century earlier, come to this? To find out, we go back.", F,
   vis=[yr(-687), fo([39.0,33.0],2.2,["jerusalem","babylon","nineveh"])]),
 B("On the map, a smaller Judah in the hills. The lowlands had been taken from it after Sennacherib's campaign. To the north, the old land of Israel is still an Assyrian province.", A, ["grayson2012","finknaaman2004"],
   vis=[fo([35.0,31.7],5.2,["judah","ekron","ashdod","samaria"]), JUDAH_STEP]),
 B("Far to the east, Assyria still looks supreme. But in Babylon, a new power is already stirring. And Egypt is never far away.", A, ["grayson1975","kitchen1996"],
   vis=[fo([38.0,32.5],1.6,["assyria","babylon","egypt"])]),
 B("That is the world of this chapter. Now the story begins.", F,
   vis=[fo([35.1,31.6],4.0)]),
]
OPENER[0]["chapter"] = "The world of 586 BC"

# ---------------- Play ----------------
MANASSEH = [
 B("After Hezekiah, his son Manasseh rules Judah for many years, as a vassal of Assyria.", A, ["leichty2011","novotny2018"],
   vis=[yr(-687), fo(P["jerusalem"],12,["jerusalem"])], amb="desert", note="Manasseh: ma-NASS-eh. Accession date debated; a long reign is agreed."),
 B("His name, Manasseh of Judah, is written on the inscriptions of Esarhaddon and of Ashurbanipal, among the western kings who brought them tribute.", A, ["leichty2011","novotny2018"],
   vis=[fo([40.0,34.0],2.0,["jerusalem","nineveh"])], note="Esarhaddon: ee-sar-HAD-on. Ashurbanipal: ash-ur-BAH-nee-pal."),
 B("In the lowlands, towns that Sennacherib had ruined begin to live again.", A, ["finknaaman2004"],
   vis=[fo([34.9,31.6],8,["lachish","azekah"])]),
 B("The Bible says Manasseh rebuilt the high places his father had torn down, and filled Jerusalem with innocent blood.", T, ["bible"], ref="2 Kings 21:1–16"),
 B("Chronicles adds that he was taken in chains to Babylon, and there he repented. The book of Kings says nothing of this.", T, ["bible"], ref="2 Chronicles 33:11–13",
   vis=[fo([39.5,32.8],2.0,["jerusalem","babylon"])],
   claims=[["Chronicles adds that he was taken in chains to Babylon, and there he repented.",T,["bible"]],
           ["The book of Kings says nothing of this.",A,["bible"]]]),
 B("In these years Assyria stands at its height. Esarhaddon takes Memphis. Ashurbanipal holds a world from Elam to the Nile.", A, ["leichty2011","novotny2018","kitchen1996"],
   vis=[fo([36.0,30.5],1.4,["assyria","memphis","elam","egypt"])]),
 B("Imagine a king of Judah sending gifts east, year after year, to keep the peace his father had bought so dearly.", S,
   vis=[fo(P["jerusalem"],10,["jerusalem"])]),
]
MANASSEH[0]["chapter"] = "Manasseh's Judah"

KETEF = [
 B("Just outside Jerusalem, in a family tomb at Ketef Hinnom, two tiny silver scrolls were found, rolled up as amulets.", A, ["barkay2004"],
   vis=[fo(P["ketef"],24,["ketefhinnom","jerusalem"])], note="Ketef Hinnom: keh-TEF hin-NOME."),
 B("Scratched into the silver is a blessing: the Lord bless you and keep you. It is the oldest known text of a passage that still stands in the Hebrew Bible.", A, ["barkay2004","bible"], ref="Numbers 6:24–26",
   claims=[["Scratched into the silver is a blessing: the Lord bless you and keep you.",A,["barkay2004"]],
           ["It is the oldest known text of a passage that still stands in the Hebrew Bible.",A,["barkay2004","bible"]]]),
 B("The tomb belongs to the late seventh century BC, in the last generations before the city fell.", A, ["barkay2004"]),
]
KETEF[0]["chapter"] = "A blessing in silver"

JOSIAH = [
 B("After a short reign, Josiah, a boy, is made king of Judah.", T, ["bible"], ref="2 Kings 22:1",
   vis=[yr(-640), fo(P["jerusalem"],12,["jerusalem"])], note="Josiah: jo-SY-a."),
 B("The Bible says that in his eighteenth year a book of the law was found in the Temple.", T, ["bible"], ref="2 Kings 22:3–10"),
 B("Josiah tears his clothes, and begins a reform. The high places are pulled down, and worship is gathered to Jerusalem.", T, ["bible"], ref="2 Kings 23:1–20"),
 B("It says he kept a passover in Jerusalem such as had not been kept since the days of the judges.", T, ["bible"], ref="2 Kings 23:21–23"),
 B("At Arad, in the south, a small temple in the fortress was carefully taken apart and buried. Some link it with Josiah's reform. Others date the burial earlier.", D, ["herzog2010","naaman1991"],
   vis=[fo(P["arad"],16,["arad"])],
   claims=[["At Arad, a small temple in the fortress was carefully taken apart and buried.",A,["herzog2010"]],
           ["Some link it with Josiah's reform. Others date the burial earlier.",D,["herzog2010","naaman1991"]]]),
 B("How much of the story of the lost book is memory, and how much is a later telling, is debated.", D, ["naaman1991"]),
]
JOSIAH[0]["chapter"] = "Josiah"

NINEVEH = [
 B("In the east, Assyria's grip begins to fail. In Babylon, a new dynasty rises under Nabopolassar.", A, ["wiseman1956","grayson1975"],
   vis=[yr(-626), fo(P["babylon"],6,["babylon","nineveh"])], note="Nabopolassar: nab-o-po-LASS-ar."),
 B("In six twelve BC, the Babylonians and the Medes take Nineveh, the great capital, and burn it.", A, ["wiseman1956","grayson1975"],
   vis=[yr(-612), fo(P["nineveh"],8,["nineveh"]),
        {"type":"battle","at":P["nineveh"],"label":"Nineveh falls (612 BC)","cert":"attested","sfx":"battle","sfxHold":1600}]),
 B("The last Assyrian king holds out a little longer, on the Euphrates, and looks to Egypt for help.", A, ["wiseman1956","kitchen1996"],
   vis=[fo([38.0,36.5],3.0,["carchemish","egypt"])]),
 B("Pharaoh Neco marches north. At Megiddo, the Bible says, Josiah goes out to meet him, and is killed.", T, ["bible"], ref="2 Kings 23:29",
   vis=[yr(-609), fo(P["megiddo"],12,["megiddo"]),
        {"type":"battle","at":P["megiddo"],"label":"Josiah's death at Megiddo (609 BC)","cert":"tradition","sfx":"battle","sfxHold":1400}],
   note="Neco: NEE-ko."),
 B("Neco's march is known from Egyptian and Greek writers. Josiah's death at Megiddo is told only in the Bible.", D, ["herodotusneco","kitchen1996","bible"],
   claims=[["Neco's march is known from Egyptian and Greek writers.",A,["herodotusneco","kitchen1996"]],
           ["Josiah's death at Megiddo is told only in the Bible.",T,["bible"]]]),
 B("The people of the land make Jehoahaz king. Neco removes him, and sets his brother Jehoiakim on the throne. Judah is now in Egypt's shadow.", T, ["bible"], ref="2 Kings 23:30–35",
   vis=[fo([33.5,31.5],2.2,["jerusalem","egypt"])], note="Jehoahaz: je-HO-a-haz. Jehoiakim: je-HOY-a-kim."),
]
NINEVEH[0]["chapter"] = "Nineveh falls"

CARCHEMISH = [
 B("In six oh five BC, at Carchemish on the Euphrates, the crown prince of Babylon, Nebuchadnezzar, meets the army of Egypt, and breaks it.", A, ["wiseman1956","grayson1975"],
   vis=[yr(-605), fo([38.01,36.83],8,["carchemish"]),
        {"type":"battle","at":[38.01,36.83],"label":"Carchemish (605 BC)","cert":"attested","sfx":"battle","sfxHold":1800}],
   note="Carchemish: KAR-ke-mish. Nebuchadnezzar: neb-u-kad-NEZ-ar."),
 B("A Babylonian chronicle records the battle, and that the remnant of the Egyptian army was destroyed in the district of Hamath.", A, ["wiseman1956","grayson1975"],
   vis=[fo(P["hamath"],5,["carchemish"])]),
 B("Nabopolassar dies, and Nebuchadnezzar becomes king. The west, including Judah, passes into Babylon's hand.", A, ["wiseman1956","grayson1975"],
   vis=[fo([40.0,33.5],1.8,["babylon","jerusalem"]), PATH_WEST]),
 B("In the next year the Babylonian army takes Ashkelon, and burns it.", A, ["wiseman1956","stager1996"],
   vis=[yr(-604), fo(P["ashkelon"],12,["ashkelon"]),
        {"type":"battle","at":P["ashkelon"],"label":"Ashkelon destroyed (604 BC)","cert":"attested","sfx":"battle","sfxHold":1400}]),
 B("For a few years Jehoiakim pays tribute to Babylon.", T, ["bible"], ref="2 Kings 24:1",
   vis=[fo(P["jerusalem"],10,["jerusalem"])]),
]
CARCHEMISH[0]["chapter"] = "Carchemish"

EXILE1 = [
 B("Then Jehoiakim rebels. The Bible says he dies in Jerusalem. How, it does not clearly say.", T, ["bible"], ref="2 Kings 24:1–6",
   vis=[yr(-598), fo(P["jerusalem"],12,["jerusalem"])]),
 B("His son Jehoiachin, a young man, is king for three months.", T, ["bible"], ref="2 Kings 24:8–12",
   note="Jehoiachin: je-HOY-a-kin."),
 B("In five ninety seven BC, in the seventh year of Nebuchadnezzar, a Babylonian chronicle says: he encamped against the city of Judah, and on the second day of the month of Adar he took the city and seized its king.", A, ["wiseman1956","grayson1975"],
   vis=[yr(-597), fo(P["jerusalem"],16,["jerusalem"])], note="Adar: AY-dar."),
 B("He appointed there a king of his own choosing, and took a heavy tribute back to Babylon.", A, ["wiseman1956","grayson1975"],
   vis=[fo([40.0,33.2],1.9,["jerusalem","babylon"]), PATH_597]),
 B("The Bible names the new king Zedekiah, uncle of Jehoiachin, and says the officers, the craftsmen, and the king himself were taken east.", T, ["bible"], ref="2 Kings 24:12–17",
   note="Zedekiah: zed-eh-KY-a."),
 B("Among them, it says, was a priest called Ezekiel, who would prophesy by a canal in Babylonia of a temple yet to come.", T, ["bible"], ref="Ezekiel 1:1–3",
   vis=[fo(P["babylon"],8,["babylon"])], note="Ezekiel: eh-ZEE-kee-el."),
 B("The Temple still stood. The vessels of the house of the Lord, the Bible says, were carried to Babylon.", T, ["bible"], ref="2 Kings 24:13"),
 B("Imagine the road down from the hills, and a young king leaving Jerusalem, not knowing if he would see it again.", S,
   vis=[fo([37.0,32.8],2.2,["jerusalem","babylon"])]),
]
EXILE1[0]["chapter"] = "The first exile"

SIEGE = [
 B("Zedekiah rules as Babylon's vassal. After some years he rebels, and looks to Egypt for help, as Hezekiah once looked to Kush.", T, ["bible"], ref="2 Kings 24:20; Ezekiel 17:15",
   vis=[yr(-589), fo([33.8,31.4],2.4,["jerusalem","egypt"])]),
 B("Jeremiah the prophet, the book that bears his name says, warns the king not to fight Babylon. He is not heard.", T, ["bible"], ref="Jeremiah 27; 37–38",
   vis=[fo(P["jerusalem"],14,["jerusalem"])], note="Jeremiah: jer-eh-MY-a."),
 B("Nebuchadnezzar comes west. The siege of Jerusalem begins.", A, ["lipschits2005","bible"], ref="2 Kings 25:1–2",
   vis=[yr(-588), fo(P["jerusalem"],16,["jerusalem"])],
   claims=[["Nebuchadnezzar comes west. The siege of Jerusalem begins.",A,["lipschits2005"]],
           ["The Bible dates the start of the siege to Zedekiah's ninth year.",T,["bible"]]]),
 B("In the lowlands, the Babylonian army takes the cities of Judah one by one.", A, ["ussishkin2004","lipschits2005"],
   vis=[fo([34.95,31.62],8,["lachish","azekah"])]),
 B("At Lachish, rebuilt after Sennacherib's siege, letters written in ink on broken pottery were found in the gatehouse.", A, ["torczyner1938","ahituv2008","ussishkin2004"],
   vis=[fo(P["lachish"],20,["lachish"])]),
 B("One officer writes to his lord: we are watching for the fire signals of Lachish, according to the signs you gave, for we cannot see Azekah.", A, ["torczyner1938","ahituv2008"],
   vis=[fo([34.89,31.63],12,["lachish","azekah"])]),
 B("Azekah, it seems, had already gone dark.", D, ["torczyner1938","ahituv2008"],
   claims=[["The letter says they cannot see Azekah.",A,["torczyner1938","ahituv2008"]],
           ["That Azekah had already fallen is the usual reading, though it is an inference.",D,["torczyner1938"]]]),
 B("Imagine a night on the wall at Lachish, and a signal that does not come.", S,
   vis=[fo(P["lachish"],18,["lachish"])]),
]
SIEGE[0]["chapter"] = "The siege"

FALL = [
 B("In five eighty six BC, or, as some scholars reckon, five eighty seven, Jerusalem falls.", D, ["galil1996","cogan1988","wiseman1956","lipschits2005"],
   vis=[yr(-586), fo(P["jerusalem"],16,["jerusalem"]),
        {"type":"battle","at":P["jerusalem"],"label":"Jerusalem falls (586 or 587 BC)","cert":"disputed","sfx":"battle","sfxHold":1800}],
   claims=[["Jerusalem falls.",A,["wiseman1956","lipschits2005","shiloh1984"]],
           ["The exact year, 586 or 587 BC, is disputed.",D,["galil1996","cogan1988"]]]),
 B("The Bible says the walls were broken through. Zedekiah fled by night toward the Jordan, and was caught on the plains of Jericho.", T, ["bible"], ref="2 Kings 25:4–5",
   vis=[fo(P["jericho"],10,["jerusalem"])]),
 B("They brought him to Riblah, to the king of Babylon. His sons were killed before his eyes, and then he was blinded, and taken in chains to Babylon.", T, ["bible"], ref="2 Kings 25:6–7",
   vis=[fo(P["riblah"],6,["riblah"]), PATH_586], note="Riblah: RIB-la."),
 B("In the fifth month, the Bible says, the house of the Lord was burned, and the king's house, and every great house in Jerusalem, and the walls were pulled down.", T, ["bible"], ref="2 Kings 25:8–10"),
 B("In the City of David, and in houses on the western hill, archaeologists have found rooms blackened by a great fire, arrowheads of a Babylonian type, and a layer of ash.", A, ["shiloh1984","lipschits2005"],
   vis=[fo(P["jerusalem"],22,["jerusalem"])]),
 B("The same fire is found at Lachish, in the level that follows the letters in the gate, and in other towns of Judah.", A, ["ussishkin2004","lipschits2005"],
   vis=[fo(P["lachish"],12,["lachish"])]),
 B("Of the Temple itself, no burnt stone has been found that we can point to and say, this was Solomon's house. The burning of the Temple is told in the Bible, and in a memory that never let it go.", D, ["bible","lipschits2005"],
   vis=[fo(P["jerusalem"],20,["jerusalem"])],
   claims=[["Of the Temple itself, no burnt stone has been found that we can point to and say, this was Solomon's house.",A,["lipschits2005"]],
           ["The burning of the Temple is told in the Bible, and in a memory that never let it go.",T,["bible"]]]),
 B("Imagine the smoke over the ridge, and the mount where the house of the Lord had stood, empty of its house.", S,
   vis=[fo(P["jerusalem"],18,["jerusalem"])]),
]
FALL[0]["chapter"] = "The city falls"

BABYLON = [
 B("Many of Judah's people were taken to Babylon. The Bible gives more than one number for those who went, and the numbers do not agree.", D, ["bible"], ref="2 Kings 24:14–16; Jeremiah 52:28–30",
   vis=[fo([40.0,33.0],1.9,["jerusalem","babylon"])],
   claims=[["Many of Judah's people were taken to Babylon.",A,["wiseman1956","weidner1939","bible"]],
           ["The Bible gives more than one number for those who went, and the numbers do not agree.",D,["bible"]]]),
 B("In Babylon, unbaked clay tablets list rations of oil for Yaukin, king of the land of Judah, and for his five sons.", A, ["weidner1939","alstola2020"],
   vis=[fo(P["babylon"],12,["babylon"])], note="Yaukin: YAH-oo-kin."),
 B("The tablets date from years after Jerusalem had fallen. A king of Judah was still being fed at the emperor's table, in exile.", A, ["weidner1939","alstola2020"]),
 B("Other tablets, found in the Babylonian countryside, name Judean families living in a town called Al-Yahudu, the city of Judah, digging canals and raising crops, a generation on.", A, ["pearce2014","alstola2020"],
   vis=[fo(P["alyahudu"],8,["alyahudu"])], note="Al-Yahudu: al-ya-HOO-doo."),
 B("A lament that later entered the Hebrew Bible begins: how lonely sits the city that was full of people.", T, ["bible"], ref="Lamentations 1:1",
   vis=[fo(P["jerusalem"],10,["jerusalem"])]),
]
BABYLON[0]["chapter"] = "In Babylon"

REMAIN = [
 B("Over those who remained in the land, the Babylonians appointed a governor, Gedaliah, of a family that had served Josiah. He sat at Mizpah, north of the ruins.", T, ["bible","lipschits2005"], ref="2 Kings 25:22–24",
   vis=[fo(P["mizpah"],14,["mizpah"]), END_STEP], note="Gedaliah: ged-a-LY-a. Mizpah: MIZ-pa.",
   claims=[["The Bible says the Babylonians appointed Gedaliah to govern those who remained, from Mizpah.",T,["bible"]],
           ["Archaeology finds Mizpah flourishing in the Babylonian period, which fits a centre of government there.",A,["lipschits2005"]]]),
 B("The Bible says he was murdered, by a man of the royal house, and that many then fled to Egypt, taking the prophet Jeremiah with them, against his will.", T, ["bible"], ref="2 Kings 25:25–26; Jeremiah 41–43",
   vis=[fo([33.5,31.3],2.4,["mizpah","egypt"]), PATH_EGYPT]),
 B("Jeremiah had lived to see the city fall. The book says his words were written on a scroll by his scribe, Baruch son of Neriah.", T, ["bible"], ref="Jeremiah 36",
   vis=[fo(P["jerusalem"],10,["jerusalem"])], note="Baruch: BAR-ook. Neriah: ne-RY-a."),
 B("A clay seal impression reading belonging to Berekyahu, son of Neriyahu, the scribe, has been published. Some take it for Baruch's seal. Others say that seals from the antiquities market cannot be trusted.", D, ["avigad1986","rollston2014"],
   claims=[["A clay seal impression reading belonging to Berekyahu, son of Neriyahu, the scribe, has been published.",A,["avigad1986"]],
           ["Some take it for Baruch's seal. Others say that seals from the antiquities market cannot be trusted.",D,["rollston2014","avigad1986"]]],
   note="Berekyahu: beh-reh-KYA-hu. Neriyahu: ne-ree-YAH-hu."),
 B("Did the land lie empty? The Bible speaks of a land left desolate, keeping a sabbath. Archaeology finds life going on in Benjamin, at Mizpah and at Bethel, under Babylonian rule.", D, ["bible","barstad1996","lipschits2005"], ref="2 Chronicles 36:20–21",
   vis=[fo([35.22,31.9],9,["mizpah","bethel"])],
   claims=[["The Bible speaks of a land left desolate, keeping a sabbath.",T,["bible"]],
           ["Archaeology finds life going on in Benjamin, at Mizpah and at Bethel, under Babylonian rule.",A,["barstad1996","lipschits2005"]]]),
 B("Imagine a pot of oil measured out in a storehouse of Babylon, for a king who no longer had a city.", S,
   vis=[fo(P["babylon"],12,["babylon"])]),
 B("In Jewish memory, this is the beginning of exile: a people that would learn to live, and to remember, far from Jerusalem, and still turn toward it.", T, ["bible"], ref="Psalm 137; Jeremiah 29",
   vis=[fo([39.5,32.8],1.9,["jerusalem","babylon"])]),
 B("By the rivers of Babylon, a later psalm says, we sat down and wept, when we remembered Zion.", T, ["bible"], ref="Psalm 137:1",
   vis=[fo(P["babylon"],8,["babylon"])]),
 B("A generation later, Babylon itself will fall, and a Persian king will let the exiles go home. That is where our next chapter begins.", A, ["cylinder"],
   vis=[yr(-538), fo([44.0,33.0],1.8,["babylon","jerusalem"])],
   note="Chapter hook. Slow down on the last sentence, then stop. The Cyrus Cylinder and the return are the next chapter."),
]
REMAIN[0]["chapter"] = "Those who remained"

PLAY = MANASSEH + KETEF + JOSIAH + NINEVEH + CARCHEMISH + EXILE1 + SIEGE + FALL + BABYLON + REMAIN
INTRO_BEATS = OPENER

DIGITS = [
  ("ended in six eighty one BC","ended in 681 BC"),
  ("it is five eighty six BC","it is 586 BC"),
  ("In six twelve BC","In 612 BC"),
  ("In six oh five BC","In 605 BC"),
  ("In five ninety seven BC","In 597 BC"),
  ("In five eighty six BC, or, as some scholars reckon, five eighty seven","In 586 BC, or, as some scholars reckon, 587"),
  ("the late seventh century BC","the late 7th century BC"),
  ("in his eighteenth year","in his 18th year"),
  ("king for three months","king for 3 months"),
  ("for his five sons","for his 5 sons"),
  ("on the second day of the month of Adar","on the 2nd day of the month of Adar"),
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
assert len(INTRO_BEATS) == 8 and len(PLAY) == 65, (len(INTRO_BEATS), len(PLAY))
assert PLAY[-1]["steps"][-1]["text"].endswith("next chapter begins.")

speech, clean = N1000.speech, N1000.clean

import quick as _quick
QUICK, QUICK_FROM = _quick.build(__import__(__name__), "Chapter 7 in brief",
    ["pl01","pl07","pl11","pl17","pl19","pl22","pl29","pl39","pl43","pl47","pl52","pl60","pl64"],
    ("Chapter Seven, in two minutes.", [fo([36.5,32.4],2.2)]),
    steps_map={"pl60": ["pl56"]})  # remnant border lives on pl56; show it with the Benjamin line
QUICK[-1]["pauseAfter"] = 2000
