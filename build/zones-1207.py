import json
def F(zone,cert,part,coords): return {"type":"Feature","properties":{"zone":zone,"certainty":cert,"part":part},"geometry":{"type":"Polygon","coordinates":[coords+[coords[0]]]}}
# Nile valley: (lon,lat) along the river, south -> north
nile=[(31.83,18.40),(31.20,18.70),(30.48,19.17),(30.40,20.30),(30.90,21.20),(31.35,21.85),(32.20,22.70),(32.90,24.09),(32.64,25.70),(32.72,26.16),(31.80,26.60),(31.18,27.18),(30.75,28.10),(31.10,29.07),(31.25,30.00)]
w=[(x-0.45,y) for x,y in nile]; e=[(x+0.45,y) for x,y in reversed(nile)]
delta=[(30.20,30.50),(29.70,31.10),(29.90,31.70),(31.2,31.9),(32.40,31.60),(32.45,30.50),(31.9,30.0)]
egypt_core=w[:-1]+[(30.2,29.0)]+delta+e[1:]
F_=[
 F("egypt","sure","Nile valley and Delta, to Napata (4th cataract)",[list(p) for p in egypt_core]),
 F("egypt","unsure","Egyptian-held Canaan, Ways of Horus and Upe (Damascus)",
   [[32.40,31.60],[32.45,30.90],[33.6,30.9],[34.25,31.05],[34.85,31.15],[35.4,31.25],[35.75,32.1],[35.85,32.7],[36.4,32.6],[36.75,33.2],[36.75,33.75],[36.45,34.30],[35.95,34.35],[35.62,34.32],[35.2,33.5],[34.6,32.4],[34.1,31.4],[33.0,31.25]]),
 F("hatti","sure","Hittite core lands, Lower Land and Kizzuwatna (Cilicia)",
   [[31.8,40.6],[34.0,41.0],[36.5,40.9],[38.3,40.0],[38.6,38.6],[37.8,37.6],[36.3,36.7],[34.5,36.6],[33.0,37.2],[31.5,38.3],[31.0,39.5]]),
 F("hatti","unsure","Syrian vassals: Ugarit, Amurru, Aleppo, Carchemish, Emar, Kadesh",
   [[35.75,36.95],[36.7,37.15],[38.05,37.25],[38.5,36.6],[38.4,35.8],[38.0,35.3],[37.2,34.6],[36.55,34.42],[35.95,34.36],[35.62,34.32],[35.7,35.5],[35.6,36.3]]),
 F("hatti","unsure","Western Anatolian vassals (Seha, Mira, Wilusa). Loyalty uncertain by 1207 BC",
   [[26.0,40.4],[29.5,40.5],[31.0,39.8],[31.0,38.4],[29.8,37.0],[27.2,37.0],[26.2,38.2]]),
 F("assyria","sure","Assyrian heartland: Assur, Nineveh, Arbela",
   [[42.6,36.9],[43.9,37.05],[44.6,36.2],[43.9,35.2],[43.2,35.0],[42.7,35.6]]),
 F("assyria","unsure","Upper Mesopotamia (former Hanigalbat), Khabur, middle Euphrates",
   [[38.6,36.7],[38.8,37.3],[40.5,37.7],[42.6,37.4],[42.6,36.9],[42.7,35.6],[43.2,35.0],[42.0,34.6],[40.9,34.35],[39.9,35.2],[38.75,35.9]]),
 F("babylon","sure","Babylon, Kish, Nippur, Dur-Kurigalzu",
   [[43.9,33.5],[44.8,33.6],[45.6,32.4],[45.6,31.6],[44.9,31.3],[44.0,32.0]]),
 F("babylon","unsure","Kassite Babylonia, from the Diyala to the Sealand",
   [[42.4,33.4],[43.2,34.1],[44.0,34.45],[45.4,34.1],[46.4,33.1],[47.3,31.9],[48.0,30.6],[47.9,29.95],[46.5,30.25],[45.3,30.9],[44.2,31.4],[43.2,32.4]]),
 F("elam","sure","Susiana plain (Susa)",
   [[47.6,32.9],[49.0,32.9],[49.6,31.9],[48.9,30.8],[47.8,31.2]]),
 F("elam","sure","Anshan (Tal-i Malyan, Fars)",
   [[51.8,30.4],[52.9,30.3],[53.0,29.6],[52.0,29.5]]),
 F("elam","unsure","Elamite highlands between Susa and Anshan",
   [[46.8,33.8],[48.6,34.0],[50.5,32.8],[52.4,31.5],[53.8,30.3],[53.4,29.0],[51.5,28.9],[50.2,29.9],[49.0,30.2],[48.2,30.4],[47.2,31.6]]),
]
json.dump({"type":"FeatureCollection","features":F_},open("zones.json","w"))
israel={"type":"FeatureCollection","features":[{"type":"Feature","properties":{"zone":"israel","certainty":"people","part":"Central hill country, Iron I villages (no border)"},"geometry":{"type":"Polygon","coordinates":[[[35.0,32.45],[35.35,32.45],[35.5,32.1],[35.45,31.65],[35.25,31.45],[35.0,31.5],[34.95,31.9],[35.0,32.45]]]}}]}
json.dump(israel,open("israel.json","w"))
