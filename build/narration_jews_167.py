"""Narration for the 167 BC stop of the Story of the Jews ("Chapter 9", The Maccabees): the opening film
(transitionIn) and Play (from Alexander to the early Hasmoneans: the Hellenistic kingdoms, Antiochus IV,
the crisis of 167 BC, the revolt, the rededication of the Second Temple, and the rise of a ruling house).
Same format and rules as build/narration_jews_538.py: one beat = one spoken line = one mp3. Labels:
attested / disputed / tradition / scene ("Imagine ...", no sources) / frame (opening film only).
Spoken text has no digits or brackets; subtitles show digits through "display" (DIGITS below).
The books of the Maccabees and Josephus are labelled tradition; the Heliodorus stele and Greek historians
are attested. How far 167 was a royal persecution, and how far a civil conflict, is disputed.
The chapter ends on a teaser for Rome in 63 BC.
"""
import re
import narration_jews_1000 as N1000, narration_jews_538 as N538
A,D,T,S,F = "attested","disputed","tradition","scene","frame"
cap, fo, yr, B = N1000.cap, N1000.fo, N1000.yr, N1000.B

P = dict(N538.P, **{
    "modein":[35.017,31.933], "bethzur":[35.101,31.592], "bethhoron":[35.110,31.878],
    "emmaus":[34.989,31.839], "elasa":[35.16,31.90], "paneas":[35.695,33.249],
    "antioch":[36.162,36.201], "alexandria":[29.909,31.201], "joppa":[34.751,32.053],
    "akko":[35.082,32.928],
})
YEHUD = N538.YEHUD
YEHUD_STEP = N538.YEHUD_STEP  # already on the map at the start of this chapter

# modest early-Hasmonean core (the hills and the western approaches; not later Galilee or the far south)
JUDAEA = [[34.88,32.05],[35.36,32.05],[35.36,31.50],[34.88,31.50],[34.88,32.05]]
JUDAEA_STEP = {"type":"border","fade":[{"zone":"judah"}],"add":[
  {"zone":"judah","certainty":"people","label":"JUDAEA","labelAt":[35.18,31.72],"coords":JUDAEA}],"sfx":"border"}

PATH_ALEX = {"type":"migration","label":"Alexander moves south (332 BC)","cert":"attested",
             "path":[P["tyre"],[34.9,32.4],P["gaza"],[32.8,31.0],P["memphis"]],
             "sfx":"migration","sfxHold":2200}

# ---------------- opening film ----------------
OPENER = [
 B("The Long Map. The Story of the Jews. The Maccabees.", F,
   vis=[yr(-167), fo([35.2,31.8],6,["jerusalem"])], amb="desert",
   note="Title card."),
 B("Our last chapter ended in the Persian period. Some of Judah's people had come home, and a Second Temple stood in a small province called Yehud.", F,
   vis=[yr(-516), fo([35.2,31.7],7,["jerusalem"])], note="Picks up the end of Chapter 8."),
 B("Now it is one hundred and sixty seven BC. A Greek-speaking king, ruling from Syria, stands over this land, and the Temple is about to enter a crisis.", A, ["maccabees","schwartz2008","polybius"],
   vis=[yr(-167), fo([36.0,33.5],2.2,["antioch","jerusalem","paneas"])],
   claims=[["In 167 BC a Seleucid king rules this land, and Jewish books remember a crisis over the Temple.",A,["maccabees","schwartz2008","polybius"]]]),
 B("The Second Temple still stands. But the empire that first let the exiles return has passed away, and new kingdoms have taken its place.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo([33.0,32.5],1.4,["jerusalem","antioch","alexandria"])],
   claims=[["After Persia, Hellenistic kingdoms rule the land around the Second Temple.",A,["tcherikover1959","grabbe2008"]]]),
 B("How did a revolt begin in these hills? And how was the Temple dedicated again? To find out, we go back.", F,
   vis=[fo([35.2,31.8],5,["jerusalem","modein"])]),
 B("On the map, Yehud is still a small province around Jerusalem. To the west lies the sea, with Greek-speaking cities on the coast. Far to the north is Antioch, a new royal capital in Syria. To the south-west, Alexandria in Egypt.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo([33.5,32.8],1.5,["jerusalem","antioch","alexandria","tyre"])],
   claims=[["Yehud is a small province around Jerusalem, with Hellenistic royal cities to the north and south-west.",A,["tcherikover1959","grabbe2008","stern2001"]]]),
 B("In the books later called Maccabees, and in Josephus, this is the hour when Jewish law is forbidden, and an alien altar is set on the Temple mount. How far that was royal policy, and how far a fight inside Jerusalem, scholars still dispute.", D, ["maccabees","josephusant","bickerman1979","honigman2014"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["The books of the Maccabees and Josephus describe a ban on the law and an alien altar in 167 BC.",T,["maccabees","josephusant"]],
           ["How far this was royal policy, and how far a conflict inside Jerusalem, is disputed.",D,["bickerman1979","tcherikover1959","honigman2014","schwartz2008"]]]),
 B("That is the world of this chapter. Now the story begins.", F,
   vis=[fo([35.2,31.8],6,["jerusalem"])],
   note="Locked closer; Play follows with no choice in between."),
]
OPENER[0]["chapter"] = "The world of 167 BC"

# ---------------- Play ----------------
HELLENISM = [
 B("When the Second Temple was dedicated, Yehud was still a small Persian province. For generations, life went on under the great king, with a governor, a priest, and a tax.", A, ["stern2001","grabbe2004"],
   vis=[yr(-516), fo(P["jerusalem"],7,["jerusalem"])],
   claims=[["Yehud remained a small Persian province after the Temple was rebuilt.",A,["stern2001","grabbe2004"]]]),
 B("In three thirty two BC, Alexander of Macedon takes the Persian empire. The Greek historians record his long sieges of Tyre and of Gaza, on the road to Egypt.", A, ["arrian"],
   vis=[yr(-332), fo([34.6,32.2],3.5,["tyre","gaza"]), PATH_ALEX,
        {"type":"battle","at":P["tyre"],"label":"Tyre taken (332 BC)","cert":"attested","sfx":"battle","sfxHold":1600}],
   claims=[["In 332 BC Alexander takes Tyre and Gaza on his way to Egypt.",A,["arrian"]]]),
 B("The story that he visited Jerusalem and honoured the Temple is told by Josephus, writing centuries later. It is not in the Greek historians of Alexander.", T, ["josephusant","arrian"],
   vis=[fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["Josephus says Alexander visited Jerusalem and honoured the Temple.",T,["josephusant"]],
           ["The Greek historians of Alexander do not tell that visit.",A,["arrian","grabbe2008"]]]),
 B("When Alexander dies in three twenty three BC, his generals divide the lands. The old Persian world breaks into new kingdoms, Greek in language, eastern in reach.", A, ["arrian","grabbe2008"],
   vis=[fo([33.0,32.0],1.3,["alexandria","antioch","babylon","jerusalem"])],
   claims=[["After Alexander's death in 323 BC, his generals divide the empire into new kingdoms.",A,["arrian","grabbe2008"]]]),
 B("Judaea first lies under the Ptolemies, who rule from Alexandria in Egypt. For about a century the land is taxed from the Nile, not from the old Persian capitals.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo(P["alexandria"],5,["alexandria","memphis","jerusalem"])],
   claims=[["In the third century BC Judaea lies under the Ptolemies, ruling from Alexandria.",A,["tcherikover1959","grabbe2008"]]]),
 B("Tyre, already an old Phoenician city, and the new Alexandria, become great ports of this world. Jerusalem remains a hill city, inland, beside its Temple.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo([32.5,32.0],1.6,["tyre","alexandria","jerusalem"])],
   claims=[["Tyre and Alexandria are the great ports of this Hellenistic world; Jerusalem remains an inland hill city.",A,["tcherikover1959","grabbe2008"]]]),
 B("Jewish communities already live in Egypt, including in Alexandria. The books of this age remember a people not only in Judaea, but also by the Nile.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo(P["alexandria"],6,["alexandria","memphis"])],
   claims=[["Jewish communities in Egypt, including Alexandria, are known in this age.",A,["tcherikover1959","grabbe2008"]]]),
 B("Imagine the coast filling with Greek-speaking cities, and the hill country still living by older ways, with the Temple at its centre.", S,
   vis=[fo([34.7,32.2],3.2,["tyre","joppa","akko","jerusalem"])]),
 B("In about two hundred BC, after a battle at Paneas, under Mount Hermon, the land passes to the Seleucid kings, who rule from Antioch in Syria.", A, ["polybius","tcherikover1959"],
   vis=[yr(-200), fo(P["paneas"],6,["paneas","damascus","jerusalem"]),
        {"type":"battle","at":P["paneas"],"label":"Battle of Paneas (c. 200 BC)","cert":"attested","sfx":"battle","sfxHold":1600}],
   claims=[["After the battle of Paneas, c. 200 BC, the land passes from the Ptolemies to the Seleucids.",A,["polybius","tcherikover1959"]]]),
 B("For a time, Jewish life in Jerusalem goes on: a high priest, the Second Temple, a small people under a distant king.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["Under early Seleucid rule, Jerusalem still has a high priest and the Second Temple.",A,["tcherikover1959","grabbe2008"]]]),
 B("The new kings settle veterans, found cities, and ask the peoples of the land to live under their tax. Some join; some do not.", A, ["tcherikover1959","hengel1974"],
   vis=[fo([34.8,32.3],3.0,["akko","joppa","samaria","jerusalem"])],
   claims=[["The Seleucids settle veterans and found cities; some people of the land join this order, and some do not.",A,["tcherikover1959","hengel1974"]]]),
]

PRIESTS = [
 B("In one hundred and seventy five BC, the second book of the Maccabees says, a man called Jason, of the priestly house, obtains the high priesthood from Antiochus, and seeks to make Jerusalem more like a Greek city.", T, ["maccabees","tcherikover1959"],
   vis=[yr(-175), fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["2 Maccabees says Jason obtains the high priesthood in 175 BC and promotes Greek ways in Jerusalem.",T,["maccabees"]],
           ["A struggle over the high priesthood in these years is widely accepted; the details follow 2 Maccabees.",D,["tcherikover1959","hengel1974","schwartz2008"]]]),
 B("That book says a gymnasium is built, and that some priests take up Greek customs. The first book of the Maccabees, written later, also remembers a turning to Greek ways in the city.", T, ["maccabees","hengel1974"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["1 and 2 Maccabees describe a turn to Greek customs and a gymnasium in Jerusalem.",T,["maccabees"]]]),
 B("How far this was a culture war, and how far a fight among priestly families for power and tax, scholars do not agree.", D, ["bickerman1979","tcherikover1959","hengel1974","honigman2014"],
   vis=[fo([35.2,31.8],6,["jerusalem"])],
   claims=[["Scholars disagree on whether the conflict was mainly cultural, or a struggle among priestly families for power and revenue.",D,["bickerman1979","tcherikover1959","hengel1974","honigman2014"]]]),
 B("Not everyone in the land takes up these ways. In the country towns, older customs still hold.", A, ["hengel1974","tcherikover1959"],
   vis=[fo([35.1,31.85],5,["modein","jerusalem"])],
   claims=[["Hellenizing customs are associated with Jerusalem; country towns are described as holding older ways.",A,["hengel1974","tcherikover1959"]]]),
 B("Jason is later displaced, in the account of the second book, by Menelaus, who is not of the old high-priestly line.", T, ["maccabees","schwartz2008"],
   vis=[fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["2 Maccabees says Menelaus, not of the old high-priestly line, displaces Jason.",T,["maccabees"]]]),
 B("The city is then torn, in the second book, by fighting between these priestly factions, even before the great crisis is told.", T, ["maccabees","schwartz2008"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["2 Maccabees describes fighting in Jerusalem between priestly factions before the 167 crisis.",T,["maccabees","schwartz2008"]]]),
 B("A royal letter on stone, found in the south of the land, shows Seleucid officials already watching over temples and revenues in this region, in the years before the revolt.", A, ["cotton2007"],
   vis=[fo([34.89,31.63],8,["lachish","jerusalem"])],
   claims=[["The Heliodorus stele, from the years before the revolt, shows Seleucid oversight of temples and revenues in the region.",A,["cotton2007"]]]),
 B("Antiochus the Fourth, called Epiphanes, is a real king. His coins, and the Greek historian Polybius, show him campaigning in Egypt and displaying his power in Syria.", A, ["polybius"],
   vis=[fo(P["antioch"],4,["antioch","memphis","alexandria"]),
        {"type":"migration","label":"Antiochus IV in Egypt and Syria","cert":"attested",
         "path":[P["antioch"],[32.0,31.5],P["memphis"],[32.0,31.5],P["antioch"]],
         "sfx":"migration","sfxHold":1800}],
   claims=[["Antiochus IV is attested on coins and in Polybius, including campaigns in Egypt.",A,["polybius"]]]),
 B("The second book of the Maccabees says that, returning from Egypt, the king enters Jerusalem and loots the Temple. Polybius, who knew this king, does not record that sack.", D, ["maccabees","polybius","schwartz2008"],
   vis=[fo(P["jerusalem"],7,["jerusalem"])],
   claims=[["2 Maccabees says Antiochus loots the Temple on his return from Egypt.",T,["maccabees"]],
           ["Polybius, who knew Antiochus IV, does not record that sack.",A,["polybius","schwartz2008"]]]),
 B("Imagine a king coming back from Egypt, short of money, and a city already divided.", S,
   vis=[fo([33.0,31.8],2.0,["alexandria","jerusalem","antioch"])]),
]

CRISIS = [
 B("In one hundred and sixty seven BC, or in the Seleucid year usually reckoned so, the books of the Maccabees say a persecution begins in Judaea.", T, ["maccabees","schwartz2008"],
   vis=[yr(-167), fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["1 and 2 Maccabees date a persecution in Judaea to 167 BC, in the usual reckoning.",T,["maccabees","schwartz2008"]]]),
 B("The first book says the king forbids the law, and that scrolls of the law are torn and burned.", T, ["maccabees"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["1 Maccabees says the king forbids the law and that scrolls of the law are destroyed.",T,["maccabees"]]]),
 B("In some towns, the first book says, people of Judaea are forced to take part in rites that are not their own, or they flee.", T, ["maccabees"],
   vis=[fo([35.15,31.75],5,["jerusalem","modein"])],
   claims=[["1 Maccabees says people in some towns are forced into foreign rites, or flee.",T,["maccabees"]]]),
 B("The second book, and the book of Daniel, speak of a desolating sacrilege, and of an alien altar set upon the altar of the Lord.", T, ["maccabees","bible"],
   vis=[fo(P["jerusalem"],10,["jerusalem"])],
   ref="Daniel 11.31; Daniel 12.11",
   claims=[["2 Maccabees and Daniel describe a desolating sacrilege and an alien altar on the Temple altar.",T,["maccabees","bible"]]]),
 B("Many scholars read the last chapters of Daniel as a voice from these very years, written close to the crisis, in the language of vision.", D, ["bible","schwartz2008"],
   vis=[fo(P["jerusalem"],8,["jerusalem"])],
   ref="Daniel 11–12",
   claims=[["Many scholars date the last chapters of Daniel to the 160s BC, close to this crisis.",D,["bible","schwartz2008"]]]),
 B("Josephus, writing later, tells the same story in his own way: the Temple is profaned, and an altar to a Greek god is set there.", T, ["josephusant"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["Josephus says the Temple is profaned and an altar to a Greek god is set there.",T,["josephusant"]]]),
 B("What the stones of Jerusalem from these exact years can show is limited. No royal edict of persecution has been found on stone.", A, ["honigman2014","grabbe2008"],
   vis=[fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["No royal edict of persecution from 167 BC has been found on stone, and the archaeology of these exact years in Jerusalem is limited.",A,["honigman2014","grabbe2008"]]]),
 B("Some scholars read a royal attack on Jewish law. Others read a civil conflict in Jerusalem, later told as a persecution from outside.", D, ["bickerman1979","tcherikover1959","honigman2014","schwartz2008"],
   vis=[fo([35.2,31.8],6,["jerusalem"])],
   claims=[["Whether 167 BC was mainly a royal persecution or a civil conflict later told as one is disputed.",D,["bickerman1979","tcherikover1959","honigman2014","schwartz2008"]]]),
 B("What we can hold to is more modest. A crisis in these years was remembered, close to the time, in several Jewish books. The inner motives of the king, and the exact acts, are harder to fix.", A, ["schwartz2008","goldstein1976","honigman2014"],
   vis=[fo([35.2,31.8],6,["jerusalem"])],
   claims=[["A crisis in these years is remembered in several nearly contemporary Jewish books; the king's motives and the exact acts are harder to fix.",A,["schwartz2008","goldstein1976","honigman2014"]]]),
 B("Imagine the Temple mount, and an altar that is not the old altar, and fear in the streets.", S,
   vis=[fo(P["jerusalem"],11,["jerusalem"])]),
]

REVOLT = [
 B("The first book of the Maccabees says the revolt begins at Modein, a town in the western hills, when a priest called Mattathias refuses a royal command and flees to the hills with his sons.", T, ["maccabees","goldstein1976"],
   vis=[fo(P["modein"],9,["modein","jerusalem"]),
        {"type":"migration","label":"From Modein into the hills (tradition)","cert":"tradition",
         "path":[P["modein"],[35.05,31.85],P["bethhoron"]],
         "sfx":"migration","sfxHold":1600}],
   claims=[["1 Maccabees says the revolt begins at Modein, when Mattathias refuses a royal command.",T,["maccabees"]]]),
 B("The identification of Modein is not certain. Several ruins in those hills have been proposed, and none is agreed beyond dispute.", D, ["goldstein1976","barkochva1989"],
   vis=[fo(P["modein"],10,["modein"])],
   claims=[["The site of Modein is disputed; several ruins in the western hills have been proposed.",D,["goldstein1976","barkochva1989"]]]),
 B("His son Judah, later called Maccabee, becomes the military leader in that tradition.", T, ["maccabees","barkochva1989"],
   vis=[fo([35.05,31.88],8,["modein","bethhoron","jerusalem"])],
   claims=[["1 Maccabees makes Judah, called Maccabee, the military leader of the revolt.",T,["maccabees"]]]),
 B("The books tell of early fights in the hills, and of a victory on the road at Beth-horon.", T, ["maccabees","barkochva1989"],
   vis=[fo(P["bethhoron"],10,["bethhoron","modein"]),
        {"type":"battle","at":P["bethhoron"],"label":"Beth-horon (tradition)","cert":"tradition","sfx":"battle","sfxHold":1400}],
   claims=[["1 Maccabees tells of a victory at Beth-horon.",T,["maccabees"]]]),
 B("At Emmaus, the first book says, Judah surprises a royal camp, and the king's men flee.", T, ["maccabees","barkochva1989"],
   vis=[fo(P["emmaus"],9,["emmaus","jerusalem"]),
        {"type":"battle","at":P["emmaus"],"label":"Emmaus (tradition)","cert":"tradition","sfx":"battle","sfxHold":1400}],
   claims=[["1 Maccabees says Judah surprises a royal camp at Emmaus.",T,["maccabees"]],
           ["The identification of this Emmaus is not certain.",D,["barkochva1989","goldstein1976"]]]),
 B("How many men stood on each side, and how far these reports are later hero-story, is disputed. A hill war in this landscape is real enough.", D, ["barkochva1989","goldstein1976"],
   vis=[fo([35.05,31.85],6,["modein","bethhoron","emmaus","jerusalem"])],
   claims=[["Troop numbers and the heroic shape of the early battles in 1 Maccabees are disputed; a hill war in this landscape is plausible.",D,["barkochva1989","goldstein1976"]]]),
 B("Imagine paths in the limestone hills, and a small force that knows the land, and a royal army that does not.", S,
   vis=[fo([35.05,31.88],7,["modein","bethhoron"])]),
 B("Jerusalem is retaken in this tradition, and the Temple mount is cleared.", T, ["maccabees","josephusant"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["1 Maccabees and Josephus say Jerusalem is retaken and the Temple mount cleared.",T,["maccabees","josephusant"]]]),
 B("The first book also speaks of a citadel in the city, the Akra, held by a royal garrison. Its exact place in Jerusalem is disputed.", D, ["maccabees","goldstein1976"],
   vis=[fo(P["jerusalem"],10,["jerusalem"])],
   claims=[["1 Maccabees describes a Seleucid citadel, the Akra, in Jerusalem.",T,["maccabees"]],
           ["The exact location of the Akra is disputed.",D,["goldstein1976","barkochva1989"]]]),
]

TEMPLE = [
 B("In one hundred and sixty four BC, in the usual reckoning, the first book says the altar is rebuilt and the Temple dedicated again, for eight days.", T, ["maccabees","schwartz2008"],
   vis=[yr(-164), fo(P["jerusalem"],10,["jerusalem"])],
   claims=[["1 Maccabees dates a rededication of the Temple, for eight days, to 164 BC in the usual reckoning.",T,["maccabees","schwartz2008"]]]),
 B("The first book says the stones of the polluted altar are taken down, and a new altar is built in their place.", T, ["maccabees"],
   vis=[fo(P["jerusalem"],11,["jerusalem"])],
   claims=[["1 Maccabees says the polluted altar is taken down and a new altar is built in its place.",T,["maccabees"]]]),
 B("That memory will become the festival of Dedication, later called Hanukkah. The later festival is real. The exact calendar of the first dedication is a traditional reckoning.", T, ["maccabees","schwartz2008"],
   vis=[fo(P["jerusalem"],9,["jerusalem"])],
   claims=[["The festival of Dedication (Hanukkah) remembers this story; the exact calendar of the first dedication is a traditional reckoning.",T,["maccabees","schwartz2008"]]]),
 B("Of that restoration, as it first stood, no certain stone has been identified. A later king, Herod, would one day rebuild the mount on a far greater scale.", A, ["stern2001"],
   vis=[fo(P["jerusalem"],10,["jerusalem"])],
   claims=[["No certain remains of the 164 BC restoration have been identified on the Temple mount.",A,["stern2001"]]]),
 B("The war does not end with the dedication. The first book, and Josephus, take the story on through more campaigns, still under the shadow of Syria.", T, ["maccabees","josephusant","barkochva1989"],
   vis=[fo([35.15,31.7],5,["jerusalem","bethzur"])],
   claims=[["1 Maccabees and Josephus continue the war after the rededication.",T,["maccabees","josephusant"]]]),
 B("Antiochus himself dies in the east, in the usual telling, and the royal house in Syria begins to split. The war in the hills goes on.", A, ["polybius","maccabees"],
   vis=[fo(P["antioch"],3,["antioch","jerusalem"])],
   claims=[["Antiochus IV dies in the east; the Seleucid house then splits, while war continues in Judaea.",A,["polybius","maccabees"]]]),
 B("At Beth-zur, a fortress on the road south of Jerusalem, the books place a siege and a garrison.", T, ["maccabees","barkochva1989"],
   vis=[fo(P["bethzur"],10,["bethzur","jerusalem"]),
        {"type":"battle","at":P["bethzur"],"label":"Beth-zur (tradition)","cert":"tradition","sfx":"battle","sfxHold":1400}],
   claims=[["1 Maccabees places a siege and a garrison at Beth-zur.",T,["maccabees"]],
           ["Beth-zur is a real fortress site on the road south of Jerusalem.",A,["barkochva1989"]]]),
 B("On the road at Beth-zechariah, the first book tells of a battle in which one of Judah's brothers dies under an elephant of the royal army. That scene is later tradition's own.", T, ["maccabees","barkochva1989"],
   vis=[fo([35.11,31.66],9,["bethzur","jerusalem"]),
        {"type":"battle","at":[35.11,31.66],"label":"Beth-zechariah (tradition)","cert":"tradition","sfx":"battle","sfxHold":1400}],
   claims=[["1 Maccabees describes a battle at Beth-zechariah, including the death of Eleazar under an elephant.",T,["maccabees"]]]),
 B("Judah falls in battle, in this tradition, and his brothers Jonathan and Simon take up the lead.", T, ["maccabees","josephusant"],
   vis=[fo(P["elasa"],8,["elasa","bethhoron","jerusalem"]),
        {"type":"battle","at":P["elasa"],"label":"Death of Judah (tradition; site uncertain)","cert":"tradition","sfx":"battle","sfxHold":1400}],
   claims=[["1 Maccabees and Josephus say Judah falls in battle and that Jonathan and Simon take the lead.",T,["maccabees","josephusant"]]]),
 B("The first book also tells of a treaty with Rome. That embassy is not confirmed by a Roman record of the same years, and some scholars doubt its form.", D, ["maccabees","goldstein1976"],
   vis=[fo([35.2,31.8],5,["jerusalem"])],
   claims=[["1 Maccabees describes a treaty with Rome; it is not confirmed by a Roman record of those years, and its form is disputed.",D,["maccabees","goldstein1976"]]]),
]

HOUSE = [
 B("In time, Jonathan is recognised as high priest, and Simon after him. A family from the western hills becomes the ruling house, later called Hasmonean.", T, ["maccabees","josephusant"],
   vis=[fo([35.1,31.85],6,["modein","jerusalem"]), JUDAEA_STEP],
   claims=[["1 Maccabees and Josephus say Jonathan, then Simon, are recognised as high priest, and that their house later called Hasmonean rules.",T,["maccabees","josephusant"]]]),
 B("The first book says that in Simon's days the yoke of the nations is lifted, and that the people begin to write in their own year. That claim of independence is the book's own, in the mid one hundred and forty twos.", T, ["maccabees","goldstein1976"],
   vis=[fo([35.15,31.75],5,["jerusalem","modein","joppa"])],
   claims=[["1 Maccabees claims that in Simon's days, usually 142 BC, the yoke of the nations is lifted and a native year-count begins.",T,["maccabees","goldstein1976"]]]),
 B("The first book also says this house takes the port of Joppa, and so gains a door to the sea.", T, ["maccabees"],
   vis=[fo(P["joppa"],8,["joppa","jerusalem"]),
        {"type":"migration","label":"Joppa taken (tradition)","cert":"tradition",
         "path":[P["jerusalem"],P["joppa"]],
         "sfx":"migration","sfxHold":1400}],
   claims=[["1 Maccabees says the Hasmoneans take the port of Joppa.",T,["maccabees"]]]),
 B("This is no longer only a small Persian province. It is becoming a Jewish state in the hills, still in a world of greater kings.", A, ["tcherikover1959","grabbe2008"],
   vis=[fo([35.15,31.75],5,["jerusalem","modein","bethzur","joppa"])],
   claims=[["By the late second century BC a Jewish state is taking shape in the hills, still among greater kingdoms.",A,["tcherikover1959","grabbe2008"]]]),
 B("Later coins and later buildings will mark that house. The first coins that name it come after these opening years.", A, ["tcherikover1959"],
   vis=[fo(P["jerusalem"],8,["jerusalem"])],
   claims=[["Hasmonean coins appear after the opening years of the revolt, not at its very beginning.",A,["tcherikover1959"]]]),
 B("In the generations that follow, this house will grow in power, and will also make enemies. That later growth is another story.", A, ["josephusant","tcherikover1959"],
   vis=[fo([35.2,32.0],3.5,["jerusalem","samaria","joppa"])],
   claims=[["The later Hasmoneans expand their rule; that later growth lies beyond the opening of the house.",A,["josephusant","tcherikover1959"]]]),
 B("The empire that first took this land from Persia is itself coming apart. A new power is rising in the west, at Rome.", A, ["polybius"],
   vis=[fo([30.0,34.0],1.0,["antioch","alexandria","jerusalem"])],
   claims=[["In the second century BC the Hellenistic kingdoms weaken and Rome rises in the west.",A,["polybius"]]]),
 B("In time, a Roman general will stand in Jerusalem, and this Hasmonean house will lose its independence. That is where our next chapter begins.", A, ["josephusant"],
   vis=[yr(-63), fo(P["jerusalem"],7,["jerusalem"])],
   claims=[["In 63 BC a Roman general will take Jerusalem, and Hasmonean independence will end. That story belongs to the next chapter.",A,["josephusant"]]],
   note="Teaser for the next chapter (Rome arrives, 63 BC)."),
]
HOUSE[0]["chapter"] = "A ruling house"
HELLENISM[0]["chapter"] = "A new world"
PRIESTS[0]["chapter"] = "Priests in Jerusalem"
CRISIS[0]["chapter"] = "The crisis"
REVOLT[0]["chapter"] = "The revolt in the hills"
TEMPLE[0]["chapter"] = "The Temple rededicated"

PLAY = HELLENISM + PRIESTS + CRISIS + REVOLT + TEMPLE + HOUSE
INTRO_BEATS = OPENER

DIGITS = [
    ("one hundred and sixty seven BC", "167 BC"),
    ("one hundred and seventy five BC", "175 BC"),
    ("one hundred and sixty four BC", "164 BC"),
    ("three thirty two BC", "332 BC"),
    ("three twenty three BC", "323 BC"),
    ("about two hundred BC", "about 200 BC"),
    ("one hundred and forty twos", "140s"),
    ("eight days", "8 days"),
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
assert PLAY[-1]["steps"][-1]["text"].endswith("next chapter begins.")

speech, clean = N1000.speech, N1000.clean

import quick as _quick
QUICK, QUICK_FROM = _quick.build(__import__(__name__), "Chapter 9 in brief",
    ["pl00","pl01","pl08","pl17","pl21","pl29","pl31","pl40","pl42","pl50","pl52","pl57"],
    ("Chapter Nine, in two minutes.", [fo([35.2,32.0],2.0)]))
QUICK[-1]["pauseAfter"] = 2000
