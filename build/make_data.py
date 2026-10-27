"""Builds the story data. Run from the repo root: python3 build/make_data.py
Outputs:
  data/sources.json              shared source registry (all stories)
  data/objects/near-east.json    shared object library = small fact boxes (all stories)
  data/eras/1207bc.json          shared era layer: zone geometry + which object each zone opens
  data/stories/jews/story.json   the 'History of the Jews' story: title, intro, stops
  data/stories/jews/1207bc.json  events (big fact boxes) for the 1207 BC stop, told from Israel's perspective
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import sources, objects, story_jews
src = sources.export()
objs = objects.O
ids = {o["id"] for o in objs}
assert len(ids) == len(objs), "duplicate object id"
CERT = {"attested","disputed","tradition"}
def chk(keys, where):
    for k in keys: assert k in src, f"unknown source {k} in {where}"
for o in objs:
    chk(o["src"], o["id"]); assert o["cert"] in CERT
    for f in o["facts"]: chk(f[2], o["id"]); assert f[1] in CERT
    if o["pop"]: chk(o["pop"]["src"], o["id"]); assert o["pop"]["cert"] in CERT
    for k in [k for k,v in o.items() if v is None]: del o[k]
    if not o["facts"]: del o["facts"]
stop = story_jews.STOP
for e in stop["events"]:
    chk(e["src"], e["id"]); assert e["cert"] in CERT
    for c in e["claims"]: chk(c[2], e["id"]); assert c[1] in CERT
    for i in e["objects"] + e["hl"]: assert i in ids, f"unknown object {i} in {e['id']}"
for i in stop["keyObjects"]: assert i in ids
era = json.load(open("data/eras/1207bc.json"))
zmap = {"egypt":"egypt","hatti":"hatti","assyria":"assyria","babylon":"babylon_s","elam":"elam","israel":"israelp"}
labelAt = {k: c.get("labelAt") for k,c in era.get("cards",{}).items()} or era.get("labelAt")
era = {"year":-1207,"label":"1207 BC","zones":era["zones"],"zoneObjects":zmap,"labelAt":labelAt,
       "note":"Outlines are approximate. Drawn by The Long Map from the sources in each fact box, not traced from one published map. Solid = core area well documented. Dashed = extent uncertain. Coastline and rivers are modern."}
def w(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p,"w"), ensure_ascii=False, separators=(",",":"))
    print(p, os.path.getsize(p))
w("data/sources.json", src)
w("data/objects/near-east.json", {"library":"near-east","note":"Shared by all stories. Each object is one small fact box.","objects":objs})
w("data/eras/1207bc.json", era)
w("data/stories/jews/story.json", story_jews.STORY)
w("data/stories/jews/1207bc.json", stop)
used = set()
for o in objs: used |= set(o["src"])
print("objects", len(objs), "events", len(stop["events"]), "sources", len(src))
