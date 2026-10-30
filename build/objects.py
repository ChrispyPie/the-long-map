# Shared object library (small fact boxes). Reusable by every story.
# where: {"at":[lon,lat]} point | {"river":"Nile"} | {"lake":"Dead Sea"} | {"line":[[lon,lat],...]} | {"zone":"egypt"} | {} (no map position)
A,D,T = "attested","disputed","tradition"
O = []
def o(id,type,name,where,rank,desc,src,cert=A,people=None,pop=None,facts=(),alt=None,since=None):
    # since: first stop year on whose map the object is drawn (None = every stop)
    O.append(dict(id=id,type=type,name=name,alt=alt,where=where,rank=rank,desc=desc,people=people,pop=pop,facts=[list(f) for f in facts],src=src,cert=cert,since=since))

# ---------- Egypt ----------
o("thebes","city","Thebes",{"at":[32.64,25.70]},1,"Religious capital of New Kingdom Egypt, centre of the god Amun (Karnak, Luxor). The Merneptah Stele was found in Merneptah's mortuary temple on the west bank.",["petrie1897","kuhrt"],people="Egyptians",alt="Waset",
  facts=[("The Israel Stele was found here by Petrie in 1896.",A,["stele","petrie1897"]),("The Great Karnak Inscription of Merneptah (Libyan war, year 5) is carved at Karnak.",A,["kitchen4"])])
o("memphis","city","Memphis",{"at":[31.25,29.85]},1,"Old royal city at the head of the Nile Delta, a main administrative and military centre of Egypt.",["kuhrt","vdm"],people="Egyptians")
o("piramesses","city","Pi-Ramesses",{"at":[31.83,30.80]},2,"Royal residence founded by Ramesses II in the eastern Delta (modern Qantir), close to the roads to Canaan. Its size is debated, but it was very large.",["pusch","kuhrt"],people="Egyptians",
  facts=[("Starting point for armies going to Canaan along the Ways of Horus.",A,["morris"])])
o("napata","city","Napata",{"at":[31.83,18.53]},2,"Egyptian-controlled town at the 4th Nile cataract in Nubia, the far south of Egypt's reach.",["morris","kuhrt"])
# ---------- Canaan ----------
o("gaza","city","Gaza",{"at":[34.46,31.50]},3,"Egypt's main base at the end of the Ways of Horus.",["morris"],people="Canaanites; Egyptian officials and soldiers",
  facts=[("Major Egyptian logistical hub in the 13th century BC.",A,["morris"])])
o("ashkelon","city","Ashkelon",{"at":[34.55,31.66]},3,"Coastal Canaanite city. Named on the Merneptah Stele: 'Ashkelon has been carried off'.",["stele","kitchen4"],people="Canaanites",
  facts=[("Named on the Israel Stele next to Gezer, Yenoam and Israel.",A,["stele","hasel"]),("Whether Merneptah really campaigned here, or the hymn is boastful, is debated.",D,["hasel","kitchen4"])])
o("gezer","city","Gezer",{"at":[34.92,31.86]},3,"Canaanite city where the coastal plain meets the hills. Named on the Merneptah Stele: 'Gezer has been seized'.",["stele","kitchen4"],people="Canaanites",
  facts=[("Its king wrote letters to Pharaoh in the Amarna archive (14th century BC).",A,["moran"])])
o("yenoam","city","Yenoam",{"at":[35.475,32.72]},3,"Canaanite town named on the Merneptah Stele: 'Yenoam is made non-existent'. Where it was is not known for sure.",["stele","abbas"],cert=D,people="Canaanites",
  facts=[("Location disputed: Tel Yin'am, Tell el-'Ubeidiya and Tell esh-Shihab are proposed. Dot placed at Tel Yin'am.",D,["abbas"])])
o("megiddo","city","Megiddo",{"at":[35.185,32.585]},3,"Canaanite city guarding the pass from the coast into the Jezreel Valley, on the main road north.",["killebrew","morris"],people="Canaanites",
  facts=[("Its ruler appears in the Amarna letters as an Egyptian vassal.",A,["moran"])])
o("bethshean","city","Beth-Shean",{"at":[35.50,32.505]},3,"Egyptian garrison town in the Jordan valley, controlling river crossings. Egyptian-style buildings and inscriptions were found.",["morris","killebrew"],people="Egyptians and Canaanites",
  facts=[("Permanent Egyptian base in the Ramesside period.",A,["morris"])])
o("hazor","city","Hazor",{"at":[35.568,33.017]},3,"The largest Canaanite city of the Bronze Age, in upper Galilee. By 1207 BC it had probably already been destroyed by fire.",["zuckerman","fink2005"],people="Canaanites",
  facts=[("Destroyed violently in the 13th century BC.",A,["zuckerman"]),("Exact date and who destroyed it are disputed (Ben-Tor/Zuckerman vs. Finkelstein).",D,["zuckerman","fink2005"]),("The Book of Joshua says Joshua burned it.",T,["bible"])])
o("jerusalem","city","Jerusalem",{"at":[35.235,31.777]},3,"Small hill-country town. In the 14th century BC its ruler Abdi-Heba wrote to Pharaoh (Amarna letters EA 285–290).",["moran","finkelstein"],people="Canaanites (in 1207 BC)",
  facts=[("Abdi-Heba of Jerusalem was an Egyptian vassal.",A,["moran"]),("How large it was in the Late Bronze Age is disputed; little has been found.",D,["finkelstein"])])
o("shechem","city","Shechem",{"at":[35.28,32.21]},3,"Hill-country centre between Mount Ebal and Mount Gerizim. Its 14th-century ruler Lab'ayu appears in the Amarna letters.",["moran","finkelstein"],people="Canaanites",
  facts=[("Lab'ayu of Shechem expanded his power in the hills (14th century BC).",A,["moran"])])
o("hebron","city","Hebron",{"at":[35.10,31.53]},3,"Town in the southern hills. Settlement was thin in the Late Bronze Age.",["finkelstein"],cert=D,
  facts=[("Important in the Abraham stories of Genesis.",T,["bible"])])
o("lachish","city","Lachish",{"at":[34.849,31.565]},3,"Major Canaanite city in the Shephelah (low hills), with Egyptian contacts. Destroyed in the 12th century BC, after this stop.",["killebrew","vdm"],people="Canaanites")
o("izbetsartah","site","Izbet Sartah",{"at":[34.97,32.10]},3,"Small Iron I village on the hill-country edge. A pottery sherd with an early alphabet (abecedary) was found here.",["finkelstein","faust"],
  facts=[("Founded around the late 13th or 12th century BC (Iron I).",D,["finkelstein"])])
o("timna","site","Timna",{"at":[34.96,29.78]},3,"Copper mines in the Arava valley, worked under Egyptian control in the 13th–12th centuries BC.",["killebrew"],cert=D)
# ---------- added for the c. 1150 BC stop (coordinates: Wikipedia / openbible.info, noted per line) ----------
# since=-1150: drawn from the c. 1150 BC map on, so the 1207 BC map stays as it was
o("shiloh","site","Shiloh",{"at": [35.2895, 32.0556]},3,"Hill-country sanctuary town. In tradition the Ark was kept here (1 Samuel 1–4). Iron I settlement burned in the second half of the 11th century BC.",["finkshiloh1993", "finkpiasetzky2006"],alt="Khirbet Seilun / Tel Shiloh",since=-1150)  # Wikipedia 'Shiloh (biblical city)', 32.055556 N, 35.289528 E
o("gibeah","site","Gibeah (Tell el-Ful?)",{"at": [35.231, 31.823]},3,"Saul's home town in tradition. Long identified with Tell el-Ful; the identification is disputed.",["fink2011ful"],cert=D,alt="Tell el-Ful",since=-1150)  # openbible.info / Wikipedia 'Gibeah', c. 31.823 N, 35.231 E
o("qeiyafa","site","Khirbet Qeiyafa",{"at": [34.957, 31.696]},3,"Short-lived fortified town above the Valley of Elah, destroyed c. 1000 BC. Who built it is debated.",["garfinkel2012", "garfinkel2015", "finkfantalkin2012"],since=-1150)  # Wikipedia, 31.6964 N, 34.9572 E
o("dan","site","Dan",{"at": [35.652, 33.249]},3,"City in the far north. A 9th-century BC Aramaic victory stele found here names the 'House of David'.",["biran1993", "biran1995"],alt="Tel Dan",since=-1150)  # Wikipedia 'Dan (ancient city)', 33.249 N, 35.652 E
o("gilboa","region","Mount Gilboa",{"at": [35.414, 32.434]},3,"Ridge above the Jezreel and Jordan valleys. In tradition, where Saul and Jonathan fell (1 Samuel 31).",["bible"],since=-1150)  # Wikipedia, 32.4339 N, 35.4144 E
o("bethlehem","city","Bethlehem",{"at": [35.206, 31.704]},3,"Town south of Jerusalem. In tradition, David's home town (1 Samuel 16; Ruth).",["bible"],since=-1150)  # Wikipedia, 31.7044 N, 35.2064 E (modern town centre)
o("aphek","site","Aphek",{"at": [34.93, 32.105]},3,"Town at the springs of the Yarkon. In tradition, the Philistine camp before the battle where the Ark was taken (1 Samuel 4).",["bible"],alt="Tel Afek / Antipatris",since=-1150)  # Wikipedia 'Antipatris', 32.105 N, 34.9304 E
o("bethshemesh","site","Beth-Shemesh",{"at": [34.975, 31.751]},3,"Border town between the hills and Philistia. In tradition, where the Ark came back (1 Samuel 6).",["bible"],alt="Tel Beit Shemesh",since=-1150)  # Wikipedia, 31.7506 N, 34.975 E
o("kiriathjearim","site","Kiriath-jearim",{"at": [35.104, 31.809]},3,"Hilltop town west of Jerusalem. In tradition, where the Ark stayed for many years (1 Samuel 7).",["bible"],alt="Deir el-Azar",since=-1150)  # openbible.info 'Deir el Azar', 31.80896 N, 35.10378 E
o("telqasile","site","Tell Qasile",{"at": [34.794, 32.101]},3,"Philistine town on the Yarkon, now in Tel Aviv, with a temple rebuilt several times.",["mazar1980"],since=-1150)  # Wikipedia, 32.1014 N, 34.7941 E
o("dor","city","Dor",{"at": [34.9175, 32.6175]},3,"Harbour town on the Carmel coast. The Report of Wenamun calls it a town of the Tjeker.",["lichtheim1976"],alt="Tel Dor",since=-1150)  # Wikipedia 'Tel Dor', 32.6175 N, 34.9175 E
# ---------- Phoenician coast & Syria ----------
o("tyre","city","Tyre",{"at":[35.19,33.27]},3,"Island port city on the Levantine coast, known from the Amarna letters.",["moran","vdm"],people="Canaanites (later called Phoenicians)")
o("sidon","city","Sidon",{"at":[35.37,33.56]},3,"Coastal port city, rival of Tyre.",["moran","vdm"],people="Canaanites (later called Phoenicians)")
o("byblos","city","Byblos",{"at":[35.65,34.12]},2,"Old port with close ties to Egypt; source of cedar timber. Its ruler Rib-Hadda wrote many Amarna letters.",["moran","vdm"],people="Canaanites",alt="Gubla")
o("ugarit","city","Ugarit",{"at":[35.78,35.60]},2,"Rich port kingdom, vassal of the Hittites. Its tablets in an alphabetic script tell of grain shortage and enemy ships at the end. Abandoned c. 1190 BC, after this stop.",["gilibert","cline"],people="Ugaritians (West Semitic), Hurrians and foreign merchants",
  pop={"v":"City c. 6,000–8,000 (one estimate near 10,000); kingdom perhaps c. 25,000–35,000","cert":D,"src":["gilibert","garr"]},
  facts=[("City covered about 28 hectares.",A,["gilibert"])])
o("damascus","city","Damascus",{"at":[36.29,33.51]},2,"Oasis town at the edge of the desert; Egypt's northern frontier province (Upe) in the 13th century BC.",["morris","vdm"],people="Canaanites / Syrians")
o("kadesh","city","Kadesh",{"at":[36.52,34.56]},2,"City on the Orontes (Tell Nebi Mend). The great battle between Ramesses II and the Hittites was fought here in 1274 BC.",["bryce","vdm"],
  facts=[("Under Hittite control after the battle.",A,["bryce"])])
o("carchemish","city","Carchemish",{"at":[38.01,36.83]},2,"Hittite viceroy seat on the Euphrates, governing the Syrian vassals.",["bryce"],people="Hittites, Hurrians, Luwians")
o("emar","city","Emar",{"at":[38.11,35.99]},2,"Trading town on the middle Euphrates, under Hittite control. Its tablets are an important archive. Destroyed c. 1185 BC.",["cline","vdm"],cert=A)
# ---------- Anatolia & Aegean ----------
o("hattusa","city","Hattusa",{"at":[34.62,40.02]},1,"Capital of the Hittite kings in central Anatolia; huge royal archive of clay tablets, including the Akkadian copy of the treaty with Egypt.",["bryce","schachner2024","beckman"],people="Hittites",
  pop={"v":"No reliable count. One estimate is c. 10,000–12,000; newer work suggests much of the walled area was not housing","cert":D,"src":["schachner","schachner2024"]})
o("troy","city","Troy",{"at":[26.24,39.96]},2,"City at Hisarlik near the Dardanelles, probably Hittite 'Wilusa'. Level VIIa was destroyed around 1180 BC.",["bryce","cline"],cert=D,
  facts=[("Homer's Trojan War is a later epic tradition.",T,["cline"])])
o("mycenae","city","Mycenae",{"at":[22.76,37.73]},2,"Leading palace centre of Mycenaean Greece. Palace destructions in Greece came around 1200 BC.",["cline","vdm"],people="Mycenaean Greeks")
# ---------- Mesopotamia & Iran ----------
o("assur","city","Assur",{"at":[43.26,35.46]},1,"Old religious capital of Assyria on the Tigris, home of the god Ashur.",["during","grayson"],people="Assyrians")
o("kartn","city","Kar-Tukulti-Ninurta",{"at":[43.30,35.53]},3,"New capital built by Tukulti-Ninurta I just upstream from Assur. He was killed here.",["grayson","chron"],people="Assyrians")
o("nineveh","city","Nineveh",{"at":[43.15,36.36]},2,"Assyrian city on the Tigris with a temple of Ishtar; capital only centuries later.",["during","vdm"],people="Assyrians")
o("babylon","city","Babylon",{"at":[44.42,32.54]},1,"Capital of Babylonia, ruled by the Kassite dynasty. Tukulti-Ninurta I of Assyria captured it and its king in the 13th century BC.",["brinkman","chron"],people="Babylonians under Kassite kings")
o("nippur","city","Nippur",{"at":[45.23,32.13]},2,"Religious centre of the god Enlil in Babylonia; many Kassite-period texts.",["brinkman"])
o("durkurigalzu","city","Dur-Kurigalzu",{"at":[44.20,33.35]},3,"Kassite royal city with a large ziggurat (Aqar Quf, near Baghdad).",["brinkman","vdm"])
o("susa","city","Susa",{"at":[48.26,32.19]},1,"Lowland capital of Elam; temple of the god Inshushinak.",["potts"],people="Elamites")
o("anshan","city","Anshan",{"at":[52.41,30.01]},2,"Highland capital of Elam (Tal-i Malyan in Fars).",["potts"],people="Elamites")
o("choghazanbil","site","Chogha Zanbil",{"at":[48.52,32.01]},3,"Ziggurat and temple city built by the Elamite king Untash-Napirisha in the 13th century BC.",["potts"])
# ---------- Rivers, lakes ----------
o("nile","river","Nile",{"river":"Nile"},1,"The river that made Egypt possible. The yearly flood fed the grain fields of the valley and Delta.",["butzer"],
  facts=[("Egyptian population depended on the cultivable flood land.",A,["butzer"])])
o("jordan","river","Jordan",{"river":"Jordan"},2,"River running from the Sea of Galilee down to the Dead Sea; a natural boundary between the western hills and Transjordan.",["ne","finkelstein"])
o("euphrates","river","Euphrates",{"river":"Euphrates"},1,"Great river of Syria and Mesopotamia. In 1207 BC it roughly divided the Hittite sphere from Assyria.",["bryce","during"])
o("tigris","river","Tigris",{"river":"Tigris"},1,"River of the Assyrian heartland: Assur and Nineveh lie on it.",["during"])
o("orontes","river","Orontes",{"river":"Orontes"},2,"River of inland Syria flowing north. Kadesh lies on it. Drawn approximately on this map.",["bryce","ne"])
o("halys","river","Halys (Kızılırmak)",{"river":"Kızılırmak (Halys)"},2,"Longest river of Anatolia; it loops around the Hittite heartland and Hattusa.",["bryce"])
o("karkheh","river","Karkheh",{"river":"Karkheh"},3,"River of the Susa plain in Elam.",["potts"])
o("deadsea","lake","Dead Sea",{"lake":"Dead Sea"},2,"Salt lake at the lowest point on land, at the south end of the Jordan.",["ne"])
o("galilee","lake","Sea of Galilee",{"lake":"Sea of Galilee"},3,"Freshwater lake in the north, fed by the Jordan.",["ne"],alt="Lake Kinneret")
# ---------- Seas, regions, routes ----------
o("medsea","sea","Mediterranean Sea",{"at":[30.5,34.2]},1,"The sea linking Egypt, the Levant, Cyprus, Anatolia and Greece. Around 1200 BC, raiders and migrants called 'Sea Peoples' by modern scholars appear in Egyptian texts.",["cline"])
o("redsea","sea","Red Sea",{"at":[35.6,26.2]},2,"Sea between Egypt and Arabia.",["ne"])
o("gulf","sea","Persian Gulf",{"at":[50.6,27.6]},2,"Southern end of Mesopotamia; the 'Sealand' of Babylonian texts lay near its head.",["brinkman"])
o("aegean","sea","Aegean Sea",{"at":[25.0,38.6]},2,"Sea of the Mycenaean palaces and the islands.",["cline"])
o("cyprus","region","Cyprus (Alashiya)",{"at":[33.2,35.05]},2,"Copper-rich island, called Alashiya in Late Bronze Age letters to Egypt, Ugarit and Hatti.",["moran","cline"],
  facts=[("Identification of Alashiya with (part of) Cyprus is widely accepted.",A,["cline"])])
o("sinai","region","Sinai",{"at":[33.8,29.6]},2,"Desert peninsula between Egypt and Canaan. The main road ran along its north coast.",["morris"])
o("negev","region","Negev",{"at":[34.85,30.75]},3,"Dry south of Canaan; land of herders.",["finkelstein"])
o("hills","region","Central hill country",{"at":[35.22,31.98]},3,"Hills between Jezreel Valley and Beersheba. Around 1200 BC, many new small villages begin to appear here.",["finkelstein","fink2013","faust"],
  facts=[("13th century BC: c. 30 sites, c. 50 hectares built up.",A,["fink2013"]),("Late Iron I (c. 1000 BC): c. 250 sites, c. 220 hectares.",A,["fink2013"])],
  pop={"v":"13th century BC: about 10,000 (our arithmetic: 50 ha × 200 people/ha, Finkelstein's density). Late Iron I: c. 45,000","cert":D,"src":["fink2013"]})
o("jezreel","region","Jezreel Valley",{"at":[35.30,32.62]},3,"Fertile valley crossing the hills; Megiddo guards its western entrance.",["finkelstein"])
o("lebanon","region","Lebanon mountains",{"at":[35.95,34.05]},2,"Mountain range behind the coast; source of cedar wood.",["vdm"])
o("taurus","region","Taurus mountains",{"at":[33.6,37.35]},2,"Mountain wall of southern Anatolia between the Hittite land and Syria.",["bryce"])
o("zagros","region","Zagros mountains",{"at":[46.9,34.6]},2,"Mountains east of Mesopotamia, between Babylonia/Assyria and the Iranian plateau.",["potts"])
o("syriandesert","region","Syrian desert",{"at":[39.6,33.0]},2,"Steppe and desert between the Levant and the Euphrates.",["vdm"])
o("wayshorus","route","Ways of Horus",{"line":[[31.83,30.80],[32.33,30.92],[32.8,31.07],[33.5,31.12],[33.9,31.16],[34.25,31.30],[34.46,31.50]]},2,"Egypt's fortified military road along north Sinai to Gaza, with forts and wells. Shown in reliefs of Seti I at Karnak. Course drawn approximately.",["morris"],
  facts=[("Line on this map is approximate.",D,["morris"])])
o("coastroad","route","Coastal road north",{"line":[[34.46,31.50],[34.55,31.66],[34.75,31.95],[34.93,32.12],[35.05,32.45],[35.185,32.585],[35.50,32.85],[35.568,33.017],[35.85,33.25],[36.29,33.51]]},2,"The main road from Gaza through Megiddo and Hazor to Damascus. Often called 'Via Maris' today, but that Latin name is much later.",["morris","killebrew"],cert=D,
  facts=[("The name 'Via Maris' is medieval/modern, not from 1207 BC.",A,["killebrew"]),("Exact course is approximate.",D,["morris"])])
# ---------- Peoples ----------
o("israelp","people","Israel",{"zone":"israel"},1,"A people named Israel, the ancestors the Jewish people trace their name and heritage to. In 1207 BC it was a people, not a kingdom, and the Egyptians wrote its name with the sign for a people rather than a city.",["stele","hasel"],people="Israelites",
  facts=[("Named on the Merneptah Stele, c. 1208/1207 BC. This is the oldest known mention of the name outside the Bible.",A,["stele","hasel"]),
         ("Where exactly they lived and how they related to the new hill villages is still debated. Many scholars place them in the central hills.",D,["hasel","faust","fink2013"]),
         ("Worship: there is little direct evidence for 1207 BC. Later Israel worshipped Yahweh, and how early this began is debated.",D,["faust","soleb"]),
         ("In the Hebrew Bible, Israel is the name God gave to Jacob, and his twelve sons are the ancestors of the tribes of Israel (Genesis 32; 35).",T,["bible"])],
  pop={"v":"Unknown. The hill-country villages held perhaps c. 10,000–20,000 people around 1200 BC","cert":D,"src":["fink2013"]})
o("canaanites","people","Canaanites",{"at":[35.05,32.95]},2,"Name for the people of the city-states of Canaan, each with its own ruler under Egyptian overlordship.",["killebrew","moran"],people="Canaanites")
o("bullsite","site","Bull Site",{"at":[35.3236,32.4092]},3,"A small hilltop shrine of the early Iron Age in the northern hills, open to the sky. A bronze figurine of a bull was found there.",["mazar1982"])
o("shasu","people","Shasu",{"at":[35.65,30.45]},2,"Egyptian word for tent-dwelling herders, especially in Edom, the Negev and Transjordan.",["killebrew","soleb"],
  facts=[("A temple list at Soleb names a 'land of the Shasu, yhw'.",A,["soleb"]),("Whether yhw there is the god Yahweh is disputed.",D,["soleb"])])
# ---------- States (open when a coloured area is tapped) ----------
o("egypt","state","Egypt",{"zone":"egypt"},1,"Kingdom of the Nile under the pharaoh, the overlord of Canaan in 1207 BC.",["kuhrt","morris"],people="Egyptians; Canaanites in the vassal cities",
  pop={"v":"Egypt proper: c. 2.9 million (Butzer, for 1250 BC) to c. 2.9–4.5 million (O'Connor). Modern estimates","cert":D,"src":["butzer","oconnor"]},
  facts=[("Ruler: Merneptah, son of Ramesses II (reigned c. 1213–1203 BC; exact dates vary by a few years).",A,["kitchen4","kuhrt"]),("Held Canaan with garrisons at Gaza and Beth-Shean and the Ways of Horus road.",A,["morris"]),("Gods: Amun, Ra, Osiris and many more.",A,["kuhrt"])])
o("hatti","state","Hatti (Hittites)",{"zone":"hatti"},1,"Kingdom of the Hittites in central Anatolia, ruling north Syria through vassals. It collapsed soon after 1200 BC.",["bryce","cline"],people="Hittites, Luwians, Hurrians; Syrian vassals",
  pop={"v":"No reliable count","cert":D,"src":["bryce"]},
  facts=[("King around 1207 BC: Tudhaliya IV or his successors Arnuwanda III and Suppiluliuma II; exact reign dates are uncertain.",D,["bryce"]),("Asked Egypt for grain in a famine; Merneptah says he shipped grain 'to keep alive' Hatti.",A,["kitchen4","cline"])])
o("assyria","state","Assyria",{"zone":"assyria"},1,"Kingdom on the middle Tigris, expanding west and south in the 13th century BC.",["during","grayson"],people="Assyrians (Akkadian-speaking)",
  pop={"v":"No reliable count","cert":D,"src":["during"]},
  facts=[("Tukulti-Ninurta I (c. 1243–1207 BC) died around this time; his son Ashur-nadin-apli followed.",D,["grayson","chron"]),("Main god: Ashur.",A,["during"])])
o("babylon_s","state","Babylonia",{"zone":"babylon"},1,"Southern Mesopotamia under kings of the Kassite dynasty, recently humiliated by Assyria.",["brinkman","chron"],people="Babylonians under Kassite kings",
  pop={"v":"No reliable count","cert":D,"src":["brinkman"]},
  facts=[("Kassite kings ruled Babylonia for more than four centuries and adopted Babylonian language and gods.",A,["brinkman","vdm"]),("Chief god: Marduk of Babylon.",A,["vdm"])])
o("elam","state","Elam",{"zone":"elam"},1,"Kingdom of southwest Iran with two centres, Susa in the lowlands and Anshan in the highlands. Elamites spoke their own language; they were not Persians.",["potts"],people="Elamites",
  pop={"v":"No reliable count","cert":D,"src":["potts"]},
  facts=[("Main god at Susa: Inshushinak.",A,["potts"])])
o("mycenaeans","people","Mycenaeans",{"at":[22.2,37.2]},2,"Greek-speaking palace societies of the Aegean (Linear B script).",["cline"])
o("libyans","people","Libyans (Libu)",{"at":[25.6,30.9]},2,"Peoples west of Egypt. In Merneptah's year 5, the Libyan chief Meryey invaded Egypt with allies from the sea.",["kitchen4","cline"])
o("seapeoples","people","'Sea Peoples'",{"at":[28.5,33.0]},2,"Modern name for groups named in Egyptian texts: in Merneptah's year 5, Ekwesh, Teresh, Lukka, Sherden and Shekelesh fought with the Libyans.",["kitchen4","cline","yasur"],
  facts=[("Named in Merneptah's Great Karnak Inscription.",A,["kitchen4"]),("Where they came from and why they moved is disputed.",D,["cline","yasur"]),("Map position is symbolic only.",A,["cline"])])
o("arameans","people","Arameans",{"at":[40.6,35.3]},2,"Not yet named in 1207 BC. First clearly named c. 1112 BC by Tiglath-pileser I of Assyria. Shown as a reminder of who comes next.",["aram"],cert=D)

# ---------- added for the 1207 -> c. 1150 BC transition ----------
o("ashdod","city","Ashdod",{"at":[34.66,31.76]},3,"Coastal city. Canaanite in the Late Bronze Age; in the 12th century BC it became one of the main Philistine cities.",["killebrew","yasur"],people="Canaanites, later Philistines")
o("ekron","city","Ekron",{"at":[34.85,31.78]},3,"Tel Miqne. A small Canaanite town that grew into a large Philistine city in the 12th century BC.",["killebrew","yasur"],people="Canaanites, later Philistines",alt="Tel Miqne")
o("gath","city","Gath",{"at":[34.85,31.70]},3,"Tell es-Safi. Canaanite city, later one of the Philistine cities.",["killebrew"],people="Canaanites, later Philistines",alt="Tell es-Safi")
o("medinethabu","site","Medinet Habu",{"at":[32.60,25.72]},3,"Mortuary temple of Ramesses III in western Thebes. Its walls show his year 8 battles against the 'Sea Peoples' on land and at sea.",["mhabu","edgerton"],
  facts=[("The reliefs name the Peleset, Tjeker, Shekelesh, Denyen and Weshesh.",A,["edgerton"]),("Year 8 of Ramesses III is c. 1177 BC in the usual chronology; dates differ by a few years.",D,["cline"])])
o("philistines","people","Philistines",{"zone":"philistia"},2,"A people who settled on the southern coast of Canaan in the 12th century BC. Egyptian texts call them Peleset. Their pottery, cooking and weaving show Aegean links.",["killebrew","yasur","feldman"],
  people="Philistines (Egyptian Peleset)",
  facts=[("The Peleset are named among Ramesses III's enemies at Medinet Habu.",A,["edgerton"]),
         ("Aegean-style pottery appears at Ashdod, Ekron, Ashkelon and Gath.",A,["killebrew","yasur"]),
         ("Ancient DNA from Ashkelon shows newcomers with southern European ancestry in the early Iron Age, soon mixed with the local population.",A,["feldman"]),
         ("Whether they settled around 1175 BC or around 1135 BC is disputed.",D,["fink1995","yasur"]),
         ("The Hebrew Bible remembers the Philistines as coming from Caphtor (Amos 9:7; Jeremiah 47:4).",T,["bible"])])

# ---------- c. 1000 to c. 930 BC (Chapter 3). since=-1000: the earlier maps stay as they were ----------
# coordinates checked 28 Oct 2026 (Wikipedia / Wikidata, see comments)
o('gibeon','site','Gibeon',{'at': [35.186, 31.848]},3,'Hill town north-west of Jerusalem. In tradition, where Solomon dreamed and asked for wisdom (1 Kings 3).',['bible'],cert=A,alt='el-Jib',since=-1000)  # Wikipedia "Gibeon (ancient city)": 31.8475 N 35.1864 E (checked 28 Oct 2026)
o('motza','site','Tel Motza',{'at': [35.164, 31.794]},3,'Site 7 km north-west of ancient Jerusalem with an Iron IIA temple (late 10th–early 9th century BC).',['kisilevitz2015'],cert=A,alt='Mozah',since=-1000)  # Wikidata Q16056713 "Tel Motza temple": 31.7945 N 35.1638 E (checked 28 Oct 2026)
o('aindara','site','Ain Dara',{'at': [36.852, 36.459]},3,"Temple in north Syria with a three-part plan like the one described for Solomon's temple; giant carved footprints. Badly damaged in 2018.",['monson2000'],cert=A,since=-1000)  # Wikipedia "Ain Dara (archaeological site)": 36.4594 N 36.8521 E (checked 28 Oct 2026)
o('rabbah','city','Rabbah',{'at': [35.934, 31.955]},3,'Capital of Ammon, on the citadel hill of modern Amman.',['bible'],cert=A,alt='Rabbath-Ammon, Amman citadel',since=-1000)  # Wikidata Q3157009 "Amman Citadel": 31.9547 N 35.9343 E (checked 28 Oct 2026)
o('dibon','city','Dibon',{'at': [35.786, 31.499]},3,'Moabite town; the Mesha stele (9th century BC) was found here in 1868.',['bible'],cert=A,alt='Dhiban',since=-1000)  # Wikipedia "Dhiban, Jordan": 31.4989 N 35.7856 E (modern town beside the tell; checked 28 Oct 2026)
o('bozrah','city','Bozrah',{'at': [35.607, 30.739]},3,'Later capital of Edom, on the plateau above Faynan.',['benyosef2019'],cert=A,alt='Buseirah',since=-1000)  # Wikipedia "Busaira, Jordan": 30.7389 N 35.6072 E (checked 28 Oct 2026)
o('nahas','site','Khirbet en-Nahas',{'at': [35.436, 30.681]},3,'Huge copper-smelting site in Faynan, busiest c. 11th–9th centuries BC.',['levy2014', 'benyosef2019'],cert=A,alt='Faynan',since=-1000)  # Wikipedia "Khirbet en-Nahas": 30.6806 N 35.4361 E (checked 28 Oct 2026)
o('eziongeber','site','Ezion-geber (Tell el-Kheleifeh?)',{'at': [34.98, 29.547]},3,'Port at the head of the Gulf of Aqaba in tradition. The identification with Tell el-Kheleifeh is disputed, and no 10th-century remains are clear.',['bible'],cert=D,alt='Tell el-Kheleifeh',since=-1000)  # Wikipedia "Tell el-Kheleifeh": 29.5472 N 34.9803 E (checked 28 Oct 2026); the identification itself is disputed
o('tanis','city','Tanis',{'at': [31.88, 30.977]},2,"Capital of Egypt's 21st Dynasty in the north-east Delta; royal tombs with silver coffins.",['kitchen1996'],cert=A,alt='San el-Hagar',since=-1000)  # Wikipedia "Tanis": 30.9769 N 31.8800 E (checked 28 Oct 2026)
o('bethel','site','Bethel',{'at': [35.238, 31.928]},3,"Hill town north of Jerusalem. In tradition, one of Jeroboam's two royal shrines (1 Kings 12).",['bible'],cert=A,alt='Beitin',since=-1000)  # Wikipedia "Beitin": 31.9283 N 35.2383 E (village on ancient Bethel; Wikipedia "Bethel" gives 31.9226 N 35.245 E; checked 28 Oct 2026)
o('zobah','region','Aram-Zobah',{'at': [36.1, 33.9]},2,'Aramean kingdom of Hadadezer in tradition, probably in the Beqaa valley of Lebanon. Its extent and exact place are uncertain.',['bible', 'aram'],cert=D,since=-1000)  # approximate, Beqaa valley
o('sheba','city','Sheba (Marib)',{'at': [45.326, 15.463]},1,'Capital of the kingdom of Saba in Yemen. Its inscriptions begin in later centuries.',['simpson2002'],cert=A,alt='Saba',since=-1000)  # Wikidata Q335478 "Marib": 15.4625 N 45.3258 E (modern town; the ancient city lies just beside it; checked 28 Oct 2026). South of the map's default view (lat 24–44): optional, not highlighted in narration.
o('ammon','people','Ammon',{'zone': 'ammon'},2,'People east of the Jordan around Rabbah. A kingdom by the 9th century BC; how organised around 1000 BC is uncertain.',['bible', 'mazar2010'],cert=D)  # zone, dashed
o('moab','people','Moab',{'zone': 'moab'},2,"People on the plateau east of the Dead Sea. Ruth came from Moab in tradition; King Mesha's stele (9th century BC) is Moab's own voice.",['bible', 'mazar2010'],cert=D)  # zone, dashed
o('edom','people','Edom',{'zone': 'edom'},2,'People south-east of the Dead Sea and in the Arabah. Copper production at Faynan suggests strong organisation already in the 10th century BC; whether it was a kingdom is debated.',['benyosef2019', 'levy2014'],cert=D)  # zone, dashed
o('judah','people','Judah',{'zone': 'judah'},1,'Southern kingdom, ruled from Jerusalem by the House of David. Shown from the split (c. 930 BC).',['biran1995', 'mazar2010'],cert=A)  # zone: southern part of the existing 'israel' hill-country zone
# ---------- c. 930 to 841 BC (Chapter 4). since=-930: the earlier maps stay as they were ----------
o('israelk','people','Israel (northern kingdom)',{'zone': 'israel'},1,"The northern kingdom after the split (c. 930 BC), larger and richer than Judah. Capitals Shechem, Tirzah and, from Omri, Samaria. Assyrian texts call it the House of Omri.",['fink2013','grayson1996'],cert=A,
  facts=[("Ahab 'the Israelite' at Qarqar, 853 BC, on the Kurkh Monolith.",A,['grayson1996']),("Named 'Israel' by Mesha of Moab, c. 840 BC.",A,['dearman1989']),("Its kings from Jeroboam to Jehu: 1 Kings 12 to 2 Kings 10.",T,['bible'])])  # zone: northern part of the hill country, as drawn at the end of Chapter 3
o('samaria','city','Samaria',{'at': [35.195, 32.276]},2,"Capital of the kingdom of Israel, founded by Omri on a hill bought from Shemer (1 Kings 16:24). A royal compound of fine cut stone on the summit.",['franklin2004','fink2000','bible'],cert=A,alt='Shomron, Sebastia',since=-930,
  facts=[("First palace (Building Period I) dated to the Omride kings.",D,['franklin2004','fink2000']),("Carved ivory furniture inlays in Phoenician style were found here.",A,['crowfoot1938']),("Omri bought the hill for two talents of silver.",T,['bible']),("Inscriptions at Kuntillet Ajrud name 'Yahweh of Samaria'.",A,['meshel2012'])])  # Wikipedia "Samaria (ancient city)": 32.2764 N 35.1950 E (checked 30 Oct 2026)
o('tirzah','city','Tirzah',{'at': [35.338, 32.287]},3,"Early capital of the northern kingdom, before Samaria. Usually identified with Tell el-Far'ah (North), near the head of Wadi Far'ah.",['bible'],cert=A,alt="Tell el-Far'ah (North)",since=-930,
  facts=[("Zimri ruled here for seven days and burned the palace around himself.",T,['bible'])])  # Wikipedia "Tell el-Far'ah (North)": 32.2874 N 35.3378 E (checked 30 Oct 2026)
o('jezreelcity','site','Jezreel',{'at': [35.328, 32.558]},3,"Royal town of the Omride kings above the Jezreel Valley. A large enclosure with a casemate wall, towers and a moat, built in the 9th century BC and destroyed soon after.",['ussishkin1997','fink2000'],cert=A,alt='Tel Jezreel',since=-930,
  facts=[("Excavated by D. Ussishkin and J. Woodhead, 1990–1996.",A,['ussishkin1997']),("Naboth's vineyard; Jehu kills Joram and Jezebel here.",T,['bible'])])  # Wikipedia "Tel Jezreel": 32.5579 N 35.3279 E (checked 30 Oct 2026)
o('ramah','site','Ramah',{'at': [35.232, 31.85]},3,"Town of Benjamin on the road north of Jerusalem. In the Bible, Baasha of Israel fortified it against Judah (1 Kings 15:17).",['bible'],cert=A,alt='er-Ram',since=-930)  # Wikipedia "Ramah in Benjamin": 31.8500 N 35.2317 E (checked 30 Oct 2026)
o('carmel','region','Mount Carmel',{'at': [35.05, 32.733]},2,"Mountain ridge above the coast, by modern Haifa. In the Bible, where Elijah challenged the prophets of Baal (1 Kings 18).",['bible'],cert=T,since=-930,
  facts=[("'The Lord, He is God' (1 Kings 18:39) is said seven times at the end of Yom Kippur.",A,['neilah623'])])  # Wikipedia "Mount Carmel": 32°44' N 35°03' E (checked 30 Oct 2026)
o('zarephath','city','Zarephath',{'at': [35.296, 33.458]},3,"Phoenician coastal town between Tyre and Sidon. In the Bible, where a widow fed Elijah in the drought (1 Kings 17:9–16).",['bible'],cert=A,alt='Sarepta, Sarafand',since=-930)  # Wikipedia "Sarepta": 33°27'27" N 35°17'45" E (checked 30 Oct 2026)
o('ajrud','site','Kuntillet Ajrud',{'at': [34.428, 30.186]},3,"Way station in north-east Sinai, c. 800 BC, with inscriptions and drawings on large jars and plaster: blessings by 'Yahweh of Samaria and his Asherah' and 'Yahweh of Teman and his Asherah'.",['meshel2012'],cert=A,alt='Horvat Teman',since=-930,
  facts=[("What 'his Asherah' means, a goddess or a cult symbol, is debated.",D,['meshel2012','smith2002'])])  # Wikipedia "Kuntillet Ajrud": 30.1861 N 34.4281 E (checked 30 Oct 2026)
o('ramothgilead','city','Ramoth-gilead',{'at': [36.017, 32.5]},3,"Israelite town in Gilead, east of the Jordan, fought over with Aram. In the Bible, where Ahab fell in battle (1 Kings 22). Its exact site is disputed.",['bible'],cert=D,alt='Tell er-Rumeith?',since=-930)  # Wikipedia "Ramoth-Gilead": 32.5000 N 36.0167 E (checked 30 Oct 2026); identification disputed
o('qarqar','site','Qarqar',{'at': [36.33, 35.743]},2,"Town on the Orontes, where Shalmaneser III fought a coalition of twelve kings in 853 BC. Identified with Tell Qarqur.",['grayson1996','yamada2000'],cert=A,alt='Tell Qarqur',since=-930,
  facts=[("Ahab the Israelite brought 2,000 chariots and 10,000 troops, by the Assyrian count.",A,['grayson1996']),("The chariot number may be a scribal error.",D,['naaman1976']),("Gindibu the Arab brought 1,000 camels: the earliest mention of Arabs.",A,['grayson1996','ephal1982']),("Shalmaneser claims victory but fought the same alliance again in 849, 848 and 845 BC.",D,['yamada2000'])])  # Wikipedia "Tell Qarqur": 35.7431 N 36.3303 E (checked 30 Oct 2026)
o('hamath','city','Hamath',{'at': [36.75, 35.135]},2,"Capital of a kingdom on the Orontes in central Syria. Its king Irhuleni co-led the coalition at Qarqar.",['grayson1996'],cert=A,alt='Hama',since=-930,
  facts=[("Irhuleni the Hamathite: 700 chariots, 700 cavalry and 10,000 troops at Qarqar.",A,['grayson1996'])])  # Wikipedia "Hama": 35.1350 N 36.7500 E (checked 30 Oct 2026)
o('kurkh','site','Kurkh',{'at': [40.54, 37.825]},3,"Site on the upper Tigris where the Kurkh Monolith of Shalmaneser III was found in 1861. It tells of Qarqar and names Ahab.",['bmkurkh','grayson1996'],cert=A,alt='Üçtepe',since=-930,
  facts=[("Now in the British Museum (118884).",A,['bmkurkh']),("Carved in haste, with many scribal errors.",A,['grayson1996'])])  # Wikipedia "Üçtepe": 37.8250 N 40.5400 E (checked 30 Oct 2026)
o('kalhu','city','Kalhu (Nimrud)',{'at': [43.329, 36.098]},2,"Royal city of Assyria on the Tigris under Ashurnasirpal II and Shalmaneser III. The Black Obelisk, with the tribute of Jehu, was found here in 1846.",['bmblackobelisk','grayson1996'],cert=A,alt='Calah, Nimrud',since=-930,
  facts=[("Black Obelisk: 'tribute of Jehu of the house of Omri', 841 BC.",A,['grayson1996','bmblackobelisk'])])  # Wikipedia "Nimrud": 36.0981 N 43.3289 E (checked 30 Oct 2026)
o('ataroth','site','Ataroth',{'at': [35.665, 31.574]},3,"Town in Moab where, says Mesha, the men of Gad had lived from of old and the king of Israel had built for them. Usually identified with Khirbat Ataruz.",['dearman1989'],cert=A,alt='Khirbat Ataruz',since=-930)  # Wikipedia "Ataruz": 31.5744 N 35.6648 E (checked 30 Oct 2026)
o('nebo','site','Nebo',{'at': [35.725, 31.767]},3,"Town and mountain above the Dead Sea. Mesha took it from Israel and carried off 'the vessels of Yahweh'. In tradition, Moses saw the Promised Land from Mount Nebo.",['dearman1989','bible'],cert=A,since=-930,
  facts=[("Mesha: 'Go, take Nebo from Israel'.",A,['dearman1989']),("Moses dies on Mount Nebo (Deuteronomy 34).",T,['bible'])])  # Wikipedia "Mount Nebo": 31.7667 N 35.7250 E (checked 30 Oct 2026); the town's exact site is uncertain
o('medeba','city','Medeba',{'at': [35.80, 31.717]},3,"Town on the Moabite plateau. Mesha says Omri held it 'his days and half the days of his son, forty years'.",['dearman1989'],cert=A,alt='Madaba',since=-930)  # Wikipedia "Madaba": 31.7167 N 35.8000 E (checked 30 Oct 2026)
o('aramdamascus','state','Aram-Damascus',{'zone': 'aram'},2,"Aramean kingdom ruled from Damascus. Under Hazael (c. 842–800 BC) it pressed hard on Israel. Its borders are uncertain.",['grayson1996','biran1995','aram'],cert=D,
  facts=[("Shalmaneser III: 'Hazael, son of a nobody, took the throne'.",A,['grayson1996']),("The Tel Dan stele, very likely Hazael's, claims the deaths of the kings of Israel and of the House of David.",D,['biran1995','schniedewind1996']),("Hazael takes Gilead (2 Kings 10:32–33).",T,['bible'])])  # zone, dashed (border step in the Play)
