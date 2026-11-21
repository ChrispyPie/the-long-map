"""Narration for the 538 BC stop of the Story of the Jews ("Chapter 8", Return under Persia): the opening film
(transitionIn) and Play (c. 556 BC to 516 BC: Cyrus, the fall of Babylon, the Cyrus Cylinder, the return to Zion,
and the building of the Second Temple). Same format and rules as build/narration_jews_586.py: one beat = one spoken
line = one mp3. Labels: attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film
only). Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
The opener starts at the gates of Babylon in 539 BC, then goes back. The biblical decree of return is labelled
tradition; the Cyrus Cylinder does not name Judah. The size of the return is disputed. The chapter ends on a teaser
for a later struggle over this Second Temple.
"""
import re
import narration_jews_1000 as N1000, narration_jews_586 as N586
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
cap, fo, yr, B = N1000.cap, N1000.fo, N1000.yr, N1000.B

P = dict(N586.P, **{
    "pasargadae":[53.17,30.20], "susa":[48.25,32.19], "ecbatana":[48.80,34.80],
    "persepolis":[52.89,29.93], "opis":[44.70,33.20], "sippar":[44.25,33.06],
    "sardis":[28.04,38.49], "teima":[38.61,27.63], "behistun":[47.44,34.39],
    "anshan":[52.61,30.01],
})
BENJAMIN = N586.BENJAMIN
END_STEP = N586.END_STEP  # remnant already on the map at the start of this chapter; kept for the opening

YEHUD = [[35.10,31.90],[35.32,31.90],[35.32,31.62],[35.10,31.62],[35.10,31.90]]
YEHUD_STEP = {"type":"border","fade":[{"zone":"judah"}],"add":[
  {"zone":"judah","certainty":"people","label":"YEHUD","labelAt":[35.22,31.72],"coords":YEHUD}],"sfx":"border"}

PATH_CYRUS = {"type":"migration","label":"Cyrus marches on Babylon (539 BC)","cert":"attested",
              "path":[P["pasargadae"],[50.0,32.8],[47.0,33.4],P["opis"],P["sippar"],P["babylon"]],
              "sfx":"migration","sfxHold":2200}
PATH_RETURN = {"type":"migration","label":"Return from Babylon to Zion (from 538 BC)","cert":"tradition",
               "path":[P["babylon"],[41.0,35.0],[38.01,36.83],[36.5,33.8],[35.5,32.4],P["jerusalem"]],
               "sfx":"migration","sfxHold":2200}

# ---------------- opening film ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. Cyrus, and the return to Zion.", F,
   vis=[yr(-539), fo([44.0,33.0],1.7,["babylon","jerusalem","pasargadae"])], amb="desert",
   note="Title card."),
 B("Our last chapter ended in five eighty six BC. Jerusalem had fallen, the Temple was gone, and many of Judah's people lived in Babylon.", F,
   vis=[yr(-586), fo([40.0,33.0],1.8,["jerusalem","babylon"])], note="Picks up the end of Chapter 7."),
 B("Now it is five thirty nine BC. A Persian king is moving on Babylon, and the city that took Jerusalem is about to fall in its turn.", A, ["abc7","briant2002"],
   vis=[yr(-539), fo([44.4,32.8],4.5,["babylon","opis"])],
   claims=[["In 539 BC a Persian king is moving on Babylon, and the city is about to fall.",A,["abc7","briant2002"]]]),
 B("In that city, and in towns around it, families from Judah have been living for a generation, farming and raising children by the canals.", A, ["pearce2014","alstola2020"],
   vis=[fo(P["alyahudu"],10,["alyahudu","babylon"])],
   claims=[["Judean families have been living in Babylonia for a generation, farming by the canals.",A,["pearce2014","alstola2020"]]]),
 B("How did some of the exiles come home? And how was a Second Temple built where the first had burned? To find out, we go back.", F,
   vis=[fo([40.0,33.0],1.8,["jerusalem","babylon","pasargadae"])]),
 B("On the map, a remnant still lives in the hills of Benjamin. To the east, Babylon still rules. Beyond Elam, a new power has risen in the land of the Persians.", A, ["abc7","lipschits2005","briant2002"],
   vis=[fo([42.0,32.8],1.5,["jerusalem","babylon","pasargadae"]), END_STEP],
   claims=[["A remnant still lives in the hills of Benjamin.",A,["lipschits2005","barstad1996"]],
           ["A new power has risen in the land of the Persians.",A,["abc7","briant2002"]]]),
 B("Its king is Cyrus. A clay cylinder later found in Babylon will claim that the great god of that city chose him, and that he sent captive people home.", A, ["cylinder","finkel2013"],
   vis=[fo(P["babylon"],14,["babylon"])],
   claims=[["Cyrus is king of the Persians.",A,["cylinder","abc7"]],
           ["A clay cylinder later found in Babylon claims that the god of that city chose him, and that he sent captive people home.",A,["cylinder","finkel2013"]]]),
 B("That is the world of this chapter. Now the story begins.", F,
   vis=[fo([42.0,32.8],1.6)]),
]
OPENER[0]["chapter"] = "The world of 539 BC"

# ---------------- Play ----------------
LASTKINGS = [
 B("When Jerusalem fell, the king in Babylon was already on the throne. His name was Nabonidus, and he was not of the old royal house of Nebuchadnezzar.", A, ["abc7","kuhrt2007"],
   vis=[yr(-556), fo(P["babylon"],10,["babylon"])],
   claims=[["Nabonidus, not of the old royal house of Nebuchadnezzar, was king in Babylon when Jerusalem fell and after.",A,["abc7","kuhrt2007"]]]),
 B("A Babylonian chronicle says that for years he left the city and dwelt at Teima, in Arabia, and that the New Year festival in Babylon was not held.", A, ["abc7","kuhrt2007"],
   vis=[fo([41.0,30.0],2.2,["teima","babylon"])],
   claims=[["Nabonidus spent years at Teima in Arabia, and the New Year festival in Babylon was not held.",A,["abc7","kuhrt2007"]]]),
 B("His son Belshazzar, named in Babylonian texts and later in the Bible, ruled in the city in his father's place.", A, ["abc7","kuhrt2007","bible"],
   vis=[fo(P["babylon"],12,["babylon"])],
   claims=[["Belshazzar, son of Nabonidus, is named in Babylonian texts and ruled in the city in his father's place.",A,["abc7","kuhrt2007"]],
           ["The book of Daniel also names Belshazzar, in a later story.",T,["bible"]]]),
 B("The book of Daniel tells of a feast in Babylon, and of writing on the wall. That story is later tradition, not a chronicle of the fall.", T, ["bible"], ref="Daniel 5",
   vis=[fo(P["babylon"],16,["babylon"])],
   claims=[["The feast and the writing on the wall in Daniel 5 are later tradition.",T,["bible"]]]),
 B("In the east, a Persian king was already taking land. In his own inscriptions he is Cyrus, king of Anshan, of the house called Achaemenid.", A, ["cylinder","kuhrt2007","briant2002"],
   vis=[yr(-550), fo(P["pasargadae"],6,["pasargadae","anshan"])],
   claims=[["Cyrus, king of Anshan, of the Achaemenid house, was taking land in the east.",A,["cylinder","kuhrt2007","briant2002"]]]),
]
LASTKINGS[0]["chapter"] = "The last kings of Babylon"

RISE = [
 B("The Babylonian chronicle says that Cyrus first made war on the Medes, and took their land, whose capital was at Ecbatana.", A, ["abc7","briant2002"],
   vis=[fo(P["ecbatana"],5,["ecbatana","pasargadae"])],
   claims=[["Cyrus made war on the Medes and took their land, whose capital was at Ecbatana.",A,["abc7","briant2002"]]]),
 B("Greek writers later tell how he took Lydia too, in the west, and its king Croesus, at Sardis. That western campaign is told as Greek tradition.", T, ["herodotuscyrus"],
   vis=[fo(P["sardis"],5,["sardis"])],
   claims=[["Cyrus's campaign against Lydia and Croesus is told as Greek tradition by Herodotus.",T,["herodotuscyrus"]]]),
 B("In Babylon, some of the priests of Marduk were unhappy. Nabonidus had favoured the moon god of Harran, and had stayed away from their city.", A, ["verseaccount","kuhrt2007"],
   vis=[fo(P["babylon"],8,["babylon"])],
   claims=[["Nabonidus favoured the moon god of Harran and stayed away from Babylon, to the anger of some of Marduk's priests.",A,["verseaccount","kuhrt2007"]]]),
 B("A Babylonian text written after the fall, the Verse Account of Nabonidus, accuses the king of neglect and heresy. It is a hostile source, composed under the new regime.", A, ["verseaccount","kuhrt2007"],
   vis=[fo(P["babylon"],10,["babylon"])],
   claims=[["The Verse Account of Nabonidus is a hostile Babylonian text, written after the fall, accusing the king of neglect and heresy.",A,["verseaccount","kuhrt2007"]]]),
 B("In five thirty nine BC, Cyrus moves west. At Opis on the Tigris, the chronicle says, he met the army of Akkad, and the people of Akkad retreated.", A, ["abc7","briant2002"],
   vis=[yr(-539), fo(P["opis"],8,["opis","babylon"]), PATH_CYRUS],
   claims=[["In 539 BC, at Opis on the Tigris, Cyrus met the army of Akkad, and the people of Akkad retreated.",A,["abc7"]]]),
 B("Then Sippar was taken without a battle. And in the month of Tashritu, Ugbaru, governor of Gutium, and the army of Cyrus entered Babylon, the chronicle says, without a battle.", A, ["abc7"],
   vis=[fo(P["babylon"],8,["sippar","babylon"])],
   claims=[["Sippar was taken without a battle, and in Tashritu Ugbaru and the army of Cyrus entered Babylon without a battle.",A,["abc7"]]]),
 B("Imagine the great gates opening, and a foreign army walking in, and the city still standing.", S,
   vis=[fo(P["babylon"],16,["babylon"])]),
 B("Cyrus himself entered the city a few days later, the chronicle says, and peace was imposed upon it.", A, ["abc7"],
   vis=[fo(P["babylon"],12,["babylon"])],
   claims=[["Cyrus entered Babylon a few days later, and peace was imposed upon the city.",A,["abc7"]]]),
 B("Herodotus, writing a century later, tells a different tale: that Cyrus diverted the river and came in by a dry bed. That is a Greek story, not what the chronicle says.", D, ["herodotusbabylon","abc7"],
   vis=[fo(P["babylon"],8,["babylon"])],
   claims=[["Herodotus says Cyrus diverted the river and took Babylon by a dry bed.",T,["herodotusbabylon"]],
           ["The Babylonian chronicle says the city was entered without a battle, and does not tell of a diverted river.",A,["abc7"]],
           ["The two accounts of how the city fell do not agree.",D,["herodotusbabylon","abc7"]]]),
]
RISE[0]["chapter"] = "Babylon falls"

CYLINDER = [
 B("In the ruins of Babylon, more than two thousand years later, a clay cylinder was found, inscribed in the name of Cyrus.", A, ["cylinder","finkel2013"],
   vis=[fo(P["babylon"],14,["babylon"])],
   claims=[["A clay cylinder inscribed in the name of Cyrus was found in the ruins of Babylon.",A,["cylinder","finkel2013"]]]),
 B("On it, Cyrus speaks as a Babylonian king. He says that Marduk, the great god of the city, searched the lands for a righteous ruler, chose him, and took him into Babylon without a fight.", A, ["cylinder","finkel2013"],
   vis=[fo(P["babylon"],18,["babylon"])],
   claims=[["On the cylinder, Cyrus says that Marduk chose him and took him into Babylon without a fight.",A,["cylinder","finkel2013"]]]),
 B("He says he returned the gods to their cities, and gathered people who had been settled far from home, and let them go back, and rebuild their temples.", A, ["cylinder","kuhrt1983"],
   vis=[fo([44.5,33.5],3.5,["babylon"])],
   claims=[["The cylinder says Cyrus returned cult images to their cities and allowed displaced people to go home and rebuild their temples.",A,["cylinder","kuhrt1983"]]]),
 B("The cylinder does not name Judah, or Jerusalem, or the god of Israel. What it records is a policy, told in the language of Babylon, for the cults of Mesopotamia.", A, ["cylinder","kuhrt1983","finkel2013"],
   vis=[fo(P["babylon"],10,["babylon"])],
   claims=[["The Cyrus Cylinder does not name Judah, Jerusalem, or the god of Israel.",A,["cylinder","kuhrt1983","finkel2013"]]]),
 B("The Hebrew Bible tells a more specific story. In the book of Ezra, and at the end of Chronicles, Cyrus issues a decree: the Lord, the god of heaven, has charged him to build a house in Jerusalem.", T, ["bible"], ref="Ezra 1:1–4; 2 Chronicles 36:22–23",
   vis=[fo([40.0,33.0],1.8,["babylon","jerusalem"])],
   claims=[["Ezra 1 and 2 Chronicles 36 say Cyrus issued a decree that the Lord charged him to build a house in Jerusalem.",T,["bible"]]]),
 B("Some scholars read that biblical decree as a later memory of the general policy, written in the language of Judah. Others think a specific permission for Jerusalem may have been given, and is now lost.", D, ["grabbe2004","bedford2001","kuhrt1983"],
   vis=[fo([40.0,33.0],1.8,["babylon","jerusalem"])],
   claims=[["Whether Ezra's decree is a later memory of a general policy, or a lost specific permission for Jerusalem, is disputed.",D,["grabbe2004","bedford2001","kuhrt1983"]]]),
 B("What we can say is this. The cylinder is a real inscription from the court of Cyrus. The decree in Ezra is a biblical tradition. Both speak of return, in different voices.", D, ["cylinder","bible","kuhrt1983"],
   vis=[fo(P["babylon"],8,["babylon"])],
   claims=[["The cylinder is a real inscription from the court of Cyrus.",A,["cylinder","finkel2013"]],
           ["The decree in Ezra is a biblical tradition.",T,["bible"]],
           ["How the two relate is disputed.",D,["kuhrt1983","grabbe2004","bedford2001"]]]),
]
CYLINDER[0]["chapter"] = "The Cyrus Cylinder"

RETURN = [
 B("The Bible says that in the first year of Cyrus the heads of the families of Judah and Benjamin rose up to go, and that Sheshbazzar, a prince of Judah, brought back the vessels of the Temple.", T, ["bible"], ref="Ezra 1:5–11",
   vis=[yr(-538), fo(P["babylon"],8,["babylon"])],
   claims=[["Ezra says that in the first year of Cyrus, families of Judah and Benjamin rose up to go, and Sheshbazzar brought back the Temple vessels.",T,["bible"]]]),
 B("It gives a great number of those who returned. Archaeology, in the land of Judah, does not show a sudden flood of people at this time. The province that appears under Persia is small, and poor.", D, ["bible","stern2001","lipschits2005","grabbe2004"], ref="Ezra 2",
   vis=[fo([35.2,31.7],6,["jerusalem","mizpah"])],
   claims=[["Ezra 2 gives a great number of those who returned.",T,["bible"]],
           ["Archaeology does not show a sudden flood of people in Judah at this time; the Persian province is small and poor.",A,["stern2001","lipschits2005","grabbe2004"]],
           ["The size of the first return is disputed.",D,["bible","grabbe2004","lipschits2005"]]]),
 B("Many families also stayed in Babylon. The tablets from Al-Yahudu go on for decades: Judeans farming, marrying, and paying taxes, under Persian rule as they had under Babylonian rule.", A, ["pearce2014","alstola2020"],
   vis=[fo(P["alyahudu"],10,["alyahudu","babylon"])],
   claims=[["Judean families stayed in Babylonia for decades, as the Al-Yahudu tablets show, under Persian as under Babylonian rule.",A,["pearce2014","alstola2020"]]]),
 B("Imagine a column on the road, not a nation on the march, but families, with donkeys and carts, walking back toward the hills they still called home.", S,
   vis=[fo([40.0,33.2],1.9,["babylon","jerusalem"]), PATH_RETURN]),
 B("Jerusalem, when they reached it, was not the city of Josiah or of Hezekiah. The walls were down. On the Temple mount, if the old platform could still be seen, it was bare.", A, ["lipschits2005","stern2001"],
   vis=[fo(P["jerusalem"],18,["jerusalem"])],
   claims=[["Jerusalem in the early Persian period was a much reduced city; the walls of the Iron Age city were down.",A,["lipschits2005","stern2001"]]]),
 B("The Bible says they settled in their towns, and that in the seventh month they gathered in Jerusalem, and built an altar, and offered burnt offerings, though the foundation of the Temple was not yet laid.", T, ["bible"], ref="Ezra 3:1–6",
   vis=[fo(P["jerusalem"],16,["jerusalem"])],
   claims=[["Ezra 3 says the returnees built an altar and offered burnt offerings before the Temple foundation was laid.",T,["bible"]]]),
 B("Persian rule in this land is real. Judah becomes a small province, later called Yehud, under a governor, paying tax to the great king.", A, ["stern2001","grabbe2004","lipschits2005"],
   vis=[fo([35.2,31.7],7,["jerusalem","mizpah"]), YEHUD_STEP],
   claims=[["Judah becomes a small Persian province, later called Yehud, under a governor, paying tax to the great king.",A,["stern2001","grabbe2004","lipschits2005"]]]),
]
RETURN[0]["chapter"] = "The return"

FOUNDATION = [
 B("The Bible names two leaders in these years: Sheshbazzar, who is said to have laid a foundation, and Zerubbabel, a grandson of King Jehoiachin, with the priest Jeshua.", T, ["bible"], ref="Ezra 3:8–10; 5:14–16",
   vis=[fo(P["jerusalem"],14,["jerusalem"])],
   claims=[["Ezra names Sheshbazzar, who is said to have laid a foundation, and Zerubbabel, a grandson of Jehoiachin, with the priest Jeshua.",T,["bible"]]]),
 B("How these two men relate to each other, and whether both belong to the first years of Cyrus, is disputed.", D, ["grabbe2004","bedford2001"],
   vis=[fo(P["jerusalem"],12,["jerusalem"])],
   claims=[["The relationship of Sheshbazzar and Zerubbabel, and whether both belong to the first years of Cyrus, is disputed.",D,["grabbe2004","bedford2001"]]]),
 B("The book of Ezra says that the people of the land, including some who claimed to worship the same god, offered to help, and were refused, and then worked to stop the building.", T, ["bible"], ref="Ezra 4:1–5",
   vis=[fo([35.2,32.1],6,["jerusalem","samaria"])],
   claims=[["Ezra 4 says neighbours offered to help, were refused, and then worked to stop the building.",T,["bible"]]]),
 B("That quarrel may remember real tension between those who returned and those who had remained, or between Jerusalem and Samaria. Scholars do not agree how much of Ezra's account is of this time, and how much was shaped later.", D, ["grabbe2004","bedford2001","lipschits2005"],
   vis=[fo([35.2,32.1],5.5,["jerusalem","samaria"])],
   claims=[["How much of Ezra 4 remembers real tension in this period, and how much was shaped later, is disputed.",D,["grabbe2004","bedford2001","lipschits2005"]]]),
 B("For years, the Bible says, the work on the house of the Lord ceased.", T, ["bible"], ref="Ezra 4:24",
   vis=[fo(P["jerusalem"],14,["jerusalem"])],
   claims=[["Ezra says the work on the house of the Lord ceased for years.",T,["bible"]]]),
]
FOUNDATION[0]["chapter"] = "A foundation, then a halt"

DARIUS = [
 B("Cyrus dies on campaign, in the north-east. His son Cambyses takes Egypt. The details of Cyrus's death are told in more than one way.", D, ["briant2002","herodotuscyrus"],
   vis=[yr(-530), fo([55.0,36.0],1.4,["pasargadae"])],
   claims=[["Cyrus dies on campaign in the north-east, and his son Cambyses takes Egypt.",A,["briant2002"]],
           ["The details of Cyrus's death are told in more than one way.",D,["briant2002","herodotuscyrus"]]]),
 B("After Cambyses, the empire shakes. Darius, a Persian of another branch of the royal house, takes the throne, and cuts a great inscription on the rock at Behistun, in three languages, to tell how he put down the revolts.", A, ["behistun","kuhrt2007","briant2002"],
   vis=[yr(-522), fo(P["behistun"],8,["behistun"])],
   claims=[["Darius takes the throne after a crisis, and cuts a trilingual inscription at Behistun telling how he put down the revolts.",A,["behistun","kuhrt2007","briant2002"]]]),
 B("The books of Haggai and Zechariah present themselves as words spoken in the second year of Darius, five twenty BC, urging Zerubbabel and the high priest to finish the house of the Lord.", T, ["bible"], ref="Haggai 1; Zechariah 1:1, 1:7",
   vis=[yr(-520), fo(P["jerusalem"],14,["jerusalem"])],
   claims=[["Haggai and Zechariah present themselves as words spoken in the second year of Darius, urging Zerubbabel and the high priest to finish the house.",T,["bible"]]]),
 B("Many scholars accept that setting as historical. The books are still, first of all, biblical texts, and the date is not independently confirmed on a Persian inscription.", D, ["bible","grabbe2004","bedford2001"],
   vis=[fo(P["jerusalem"],12,["jerusalem"])],
   claims=[["Many scholars accept a date in the second year of Darius as historical, but it is not independently confirmed on a Persian inscription.",D,["grabbe2004","bedford2001"]]]),
 B("The Bible says the work resumes, and that Tattenai, the Persian governor of the province Beyond the River, writes to Darius to ask whether a decree of Cyrus had in fact been issued.", T, ["bible"], ref="Ezra 5:3–17",
   vis=[fo([40.0,33.0],1.7,["jerusalem","babylon","ecbatana"])],
   claims=[["Ezra 5 says Tattenai, governor of Beyond the River, wrote to Darius to ask whether a decree of Cyrus had been issued.",T,["bible"]]]),
 B("A scroll is said to be found at Ecbatana, in Media, and Darius confirms the work. That official correspondence is told only in the book of Ezra.", T, ["bible"], ref="Ezra 6:1–12",
   vis=[fo(P["ecbatana"],8,["ecbatana"])],
   claims=[["Ezra 6 says a scroll was found at Ecbatana and that Darius confirmed the work; the correspondence is told only in Ezra.",T,["bible"]]]),
 B("In the sixth year of Darius, five sixteen BC in the usual reckoning, the Bible says the house was finished, and dedicated with joy.", T, ["bible"], ref="Ezra 6:15–18",
   vis=[yr(-516), fo(P["jerusalem"],16,["jerusalem"])],
   claims=[["Ezra 6 says the house was finished in the sixth year of Darius, usually reckoned as 516 BC, and dedicated with joy.",T,["bible"]]]),
 B("Of that Second Temple, as it first stood, no certain stone has been identified. Herod would one day rebuild the mount on a far greater scale, and what lies under it is not open to us.", A, ["stern2001","lipschits2005"],
   vis=[fo(P["jerusalem"],20,["jerusalem"])],
   claims=[["No certain remains of the first phase of the Second Temple have been identified; the mount was later rebuilt on a far greater scale under Herod.",A,["stern2001","lipschits2005"]]]),
 B("Imagine a modest house on the old hill, not the Temple of Solomon as tradition paints it, and not the great courts of later times, but a place where offerings began again.", S,
   vis=[fo(P["jerusalem"],18,["jerusalem"])]),
]
DARIUS[0]["chapter"] = "The Second Temple"

YEHUDLIFE = [
 B("This is not a new kingdom of David. It is Yehud, a small Persian province, with a governor, a priest, and a tax.", A, ["stern2001","grabbe2004"],
   vis=[fo([35.2,31.7],7,["jerusalem"])],
   claims=[["Yehud is a small Persian province, with a governor, a priest, and a tax, not a restored kingdom of David.",A,["stern2001","grabbe2004"]]]),
 B("Coins and seal impressions from a little later name the province and its governors. They do not restore a king.", A, ["stern2001","grabbe2004"],
   vis=[fo([35.2,31.7],8,["jerusalem"])],
   claims=[["Coins and seal impressions from a little later name the province Yehud and its governors; they do not restore a king.",A,["stern2001","grabbe2004"]]]),
 B("In Babylon, Judean families still live by the canals, and will for generations. The exile did not simply end. It became a life in two places.", A, ["pearce2014","alstola2020"],
   vis=[fo([40.0,33.0],1.8,["alyahudu","jerusalem"])],
   claims=[["Judean families continued to live in Babylonia for generations; Jewish life now existed in two places.",A,["pearce2014","alstola2020"]]]),
 B("The Bible will remember this as a return, a fulfilment of the word of the Lord through Jeremiah, seventy years after the land was left desolate.", T, ["bible"], ref="Jeremiah 25:11–12; 29:10; 2 Chronicles 36:21",
   vis=[fo(P["jerusalem"],10,["jerusalem"])],
   claims=[["The Bible remembers the return as a fulfilment of Jeremiah's word of seventy years.",T,["bible"]]]),
 B("Seventy years is a round number in that tradition, counted in more than one way. The archaeology of the land does not show an empty sabbath of seventy years.", D, ["bible","barstad1996","lipschits2005"],
   vis=[fo([35.2,31.7],5.5,["jerusalem","mizpah"])],
   claims=[["Seventy years is a round number in the biblical tradition, counted in more than one way.",T,["bible"]],
           ["Archaeology does not show an empty land for seventy years.",A,["barstad1996","lipschits2005"]]]),
 B("What we can hold to is more modest, and more lasting. A Persian king took Babylon. Some of Judah's people came home. A temple was built again in Jerusalem, under the eye of the empire.", A, ["abc7","cylinder","stern2001"],
   vis=[fo([40.0,33.0],1.8,["babylon","jerusalem"])],
   claims=[["A Persian king took Babylon.",A,["abc7","cylinder"]],
           ["Some of Judah's people came home.",A,["stern2001","lipschits2005"]],
           ["A temple was built again in Jerusalem under Persian rule: the biblical account of the dedication.",T,["bible"]]]),
 B("And from this small province, and from the families who stayed in the east, the next chapters of Jewish life will grow.", A, ["stern2001","alstola2020"],
   vis=[fo([40.0,33.0],1.8,["jerusalem","babylon"])],
   claims=[["Jewish life continued both in Yehud and among families who stayed in the east.",A,["stern2001","alstola2020"]]]),
 B("Darius builds a new ceremonial city at Persepolis, far to the east. The empire of which Yehud is a corner now stretches from the Aegean to the highlands of Iran.", A, ["briant2002","kuhrt2007"],
   vis=[fo([42.0,32.5],1.2,["persepolis","sardis","jerusalem"])],
   claims=[["Darius founds a ceremonial city at Persepolis; the empire stretches from the Aegean to the highlands of Iran.",A,["briant2002","kuhrt2007"]]]),
 B("In time, new empires will come to this land, and this Second Temple will stand at the centre of a later struggle. That is where our next chapter begins.", A, ["stern2001"],
   vis=[fo(P["jerusalem"],12,["jerusalem"])],
   claims=[["The Second Temple in Jerusalem will later stand at the centre of a struggle under new empires.",A,["stern2001"]]],
   note="Teaser for the next chapter (Maccabees / later Second Temple crisis)."),
]
YEHUDLIFE[0]["chapter"] = "A small province"

PLAY = LASTKINGS + RISE + CYLINDER + RETURN + FOUNDATION + DARIUS + YEHUDLIFE
INTRO_BEATS = OPENER

DIGITS = [
    ("five eighty six BC", "586 BC"),
    ("five thirty nine BC", "539 BC"),
    ("five twenty BC", "520 BC"),
    ("five sixteen BC", "516 BC"),
    ("more than two thousand years later", "more than 2,000 years later"),
    ("seventy years", "70 years"),
    ("an empty sabbath of seventy years", "an empty sabbath of 70 years"),
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
assert len(INTRO_BEATS) == 8, len(INTRO_BEATS)
assert len(PLAY) == 51, len(PLAY)
assert PLAY[-1]["steps"][-1]["text"].endswith("next chapter begins.")

speech, clean = N1000.speech, N1000.clean

import quick as _quick
QUICK, QUICK_FROM = _quick.build(__import__(__name__), "Chapter 8 in brief",
    ["pl00","pl09","pl10","pl14","pl16","pl17","pl21","pl27","pl35","pl39","pl44","pl50"],
    ("Chapter Eight, in two minutes.", [fo([42.0,32.8],1.6)]))
QUICK[-1]["pauseAfter"] = 2000
