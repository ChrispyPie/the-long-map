"""Builds the story data. Run from the repo root: python3 build/make_data.py
Outputs:
  data/sources.json              shared source registry (all stories)
  data/objects/near-east.json    shared object library = small fact boxes (all stories)
  data/eras/1207bc.json          shared era layer: zone geometry + which object each zone opens
  data/stories/jews/story.json   the 'Story of the Jews' story: title, intro, stops
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
for i in stop["explore"]["key"]: assert i in ids, f"unknown explore key {i}"
era = json.load(open("data/eras/1207bc.json"))
# play transition: every caption sourced and labelled, every id/zone known
TYPES = {"caption","focus","migration","border","battle","year"}
play = stop["play"]; zones_known = {f["properties"]["zone"] for f in era["zones"]["features"]} | set(play["zoneObjects"])
for v in play["zoneObjects"].values(): assert v in ids
assert any(x["type"]=="caption" for b in play["beats"] for x in b["steps"])
for n,b in enumerate(play["beats"]):
    assert any(x["type"]=="caption" for x in b["steps"]), f"beat {n} has no caption"
    for x in b["steps"]:
        assert x["type"] in TYPES, x["type"]
        if x["type"]=="caption":
            if x["cert"]=="scene":   # evocative framing only: no sources, must read as "Imagine ..."
                assert not x["src"] and x["text"].startswith("Imagine"), f"scene caption in beat {n} must start with 'Imagine'"
            else: chk(x["src"], f"play beat {n}"); assert x["cert"] in CERT
        if x["type"] in ("migration","battle"): assert x["cert"] in CERT
        for a in x.get("arrows",[]): assert a["cert"] in CERT and a["side"] in ("egypt","enemy")
        for i in x.get("hl",[]): assert i in ids, f"unknown hl {i} in play beat {n}"
        for f in x.get("fade",[]) + x.get("add",[]): assert f["zone"] in zones_known, f["zone"]
# pacing (see build/README.md): each beat gets duration = reading time of its line
# (~2.5 words/s, at least 4 s) and pauseAfter (default 2 s) unless set by hand
words = 0
for b in play["beats"]:
    c = next(x for x in b["steps"] if x["type"]=="caption"); wc = len(c["text"].split()); words += wc
    b.setdefault("duration", max(4000, round(wc / 2.5 * 10) * 100))
    b.setdefault("pauseAfter", 2000)
    assert 1500 <= b["pauseAfter"] <= 2500, f"pauseAfter out of range in beat"
play["words"] = words
# sound: known clips only, holds of a few seconds at most, small files
SFX = {"battle","migration","border","year"}; AMB = {"desert","river"}
FILES = {"battle":"battle","migration":"migration","border":"border","year":"year","desert":"amb-desert","river":"amb-river"}
for k,f in FILES.items():
    fp = f"assets/sfx/{f}.mp3"; assert os.path.exists(fp), fp; assert os.path.getsize(fp) < 130_000, f"{fp} too big"
assert play.get("ambient") in AMB
for b in play["beats"]:
    assert b.get("ambient", "desert") in AMB, b.get("ambient")
    for x in b["steps"]:
        if "sfx" in x: assert x["sfx"] is None or x["sfx"] in SFX, x["sfx"]
        if "sfxHold" in x: assert 0 <= x["sfxHold"] <= 4000 and x["type"] in ("battle","migration","border"), x
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
print("objects", len(objs), "events", len(stop["events"]), "sources", len(src), "play beats", len(play["beats"]), "words", words, "~min", round(sum(b["duration"]+b["pauseAfter"] for b in play["beats"])/60000, 1), "explore keys", len(stop["explore"]["key"]))
