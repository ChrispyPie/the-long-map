"""Builds the story data. Run from the repo root: python3 build/make_data.py
Outputs:
  data/sources.json              shared source registry (all stories)
  data/objects/near-east.json    shared object library = small fact boxes (all stories)
  data/eras/1207bc.json          shared era layer: zone geometry + which object each zone opens
  data/eras/1150bc.json          the same layer for c. 1150 BC (derived from 1207 + the 1207 Play's border steps)
  data/stories/jews/story.json   the 'Story of the Jews' story: title, intro, stops
  data/stories/jews/1207bc.json  events (big fact boxes) for the 1207 BC stop, told from Israel's perspective
  data/stories/jews/1150bc.json  the c. 1150 BC stop: opening film, explore keys and Play to c. 1000 BC
  data/eras/1000bc.json          c. 1000 BC: the c. 1150 BC layer + dashed Ammon, Moab and Edom
  data/stories/jews/1000bc.json  the c. 1000 BC stop ("Chapter 3"): opening film, fact boxes, explore keys and Play to c. 930 BC
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
import re
import sources, objects, story_jews, narrate
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
era1207 = json.load(open("data/eras/1207bc.json"))   # hand-drawn geometry (read, then rewritten with zoneObjects/labelAt)
# narrated films: the opening film (transitionIn.beats) and Play. Every caption sourced and labelled,
# every id/zone known. Labels: attested / disputed / tradition, "scene" (evocative only: no sources,
# must read as "Imagine ...") and, in the opening film only, "frame" (the film's own framing lines:
# no sources, no facts). Spoken text has no digits or brackets; "display" is the subtitle with digits.
TYPES = {"caption","focus","migration","border","battle","year"}
# pacing (see build/README.md): each beat gets duration = reading time of its line (~2.5 words/s, at
# least 2 s; used when the voice is off) and pauseAfter (0.6 s, 1.5 s before a new chapter) unless set by hand. With the voice
# on the recorded line sets the length: audio + audioMs come from assets/narration/index.json
# (build/narrate.py); a line whose text changed since it was recorded is refused.
NIDX = json.load(open(narrate.IDX)) if os.path.exists(narrate.IDX) else {}
SILENT_OK = os.environ.get("TLM_ALLOW_SILENT") == "1"   # build without the voice for lines not recorded yet
def check_stop(stop, era, reel_prefix):
    """checks one stop's events, keys and films against the era it is drawn on; adds pacing and audio"""
    for e in stop["events"]:
        chk(e["src"], e["id"]); assert e["cert"] in CERT
        for c in e["claims"]: chk(c[2], e["id"]); assert c[1] in CERT
        for i in e["objects"] + e["hl"]: assert i in ids, f"unknown object {i} in {e['id']}"
    for i in stop["keyObjects"]: assert i in ids
    for i in stop["explore"]["key"]: assert i in ids, f"unknown explore key {i}"
    play = stop["play"]; zones_known = {f["properties"]["zone"] for f in era["zones"]["features"]} | set(play["zoneObjects"])
    for v in play["zoneObjects"].values(): assert v in ids
    tin = stop["transitionIn"]
    assert isinstance(tin, str) or (isinstance(tin, dict) and isinstance(tin.get("text"), str)), "transitionIn: a string, or {text, beats}"
    reels = [("play", play["beats"], False)] + ([("intro", tin["beats"], True)] if isinstance(tin, dict) and tin.get("beats") else [])
    def check_reel(where, beats, frame_ok):
        where_ = f"{stop['label']} {where}"
        assert beats and "chapter" in beats[0], f"{where_}: the first beat opens a chapter"
        assert sum(1 for b in beats if b.get("choice")) == (1 if where == "intro" else 0), f"{where_}: choice beats"
        for n,b in enumerate(beats):
            caps = [x for x in b["steps"] if x["type"]=="caption"]
            assert len(caps) == 1, f"{where_} beat {n} needs exactly one caption"
            if "chapter" in b: assert isinstance(b["chapter"], str) and 2 < len(b["chapter"]) < 40, b["chapter"]
            for x in b["steps"]:
                assert x["type"] in TYPES, x["type"]
                if x["type"]=="caption":
                    assert not re.search(r"[()\d]", x["text"]), f"{where_} beat {n}: spoken text has digits or brackets"
                    if "display" in x: assert isinstance(x["display"], str) and x["display"] != x["text"], f"{where_} beat {n}: display"
                    if "ref" in x: assert isinstance(x["ref"], str) and "bible" in x["src"], f"{where_} beat {n}: ref needs the bible source"
                    if x["cert"]=="scene":
                        assert not x["src"] and x["text"].startswith("Imagine"), f"scene caption in {where_} beat {n} must start with 'Imagine'"
                    elif x["cert"]=="frame":
                        assert frame_ok and not x["src"] and not x.get("claims"), f"frame caption in {where_} beat {n}: opening film only, no sources"
                    else: chk(x["src"], f"{where_} beat {n}"); assert x["cert"] in CERT
                    for c in x.get("claims", []): chk(c[2], f"{where_} beat {n}"); assert c[1] in CERT
                if x["type"] in ("migration","battle"): assert x["cert"] in CERT
                for a in x.get("arrows",[]): assert a["cert"] in CERT and a["side"] in ("egypt","enemy")
                for i in x.get("hl",[]): assert i in ids, f"unknown hl {i} in {where_} beat {n}"
                for f in x.get("fade",[]) + x.get("add",[]): assert f["zone"] in zones_known, f["zone"]
    for where, beats, frame_ok in reels: check_reel(where, beats, frame_ok)
    reel_file = {"intro": reel_prefix + "-in", "play": reel_prefix + "-play"}
    for where, beats, _ in reels:
        words = 0
        for n,b in enumerate(beats):
            c = next(x for x in b["steps"] if x["type"]=="caption"); wc = len(c["text"].split()); words += wc
            b.setdefault("duration", max(2000, round(wc / 2.5 * 10) * 100))
            # short natural gap after a line; a longer breath only before a new chapter
            nxt = beats[n + 1] if n + 1 < len(beats) else None
            b.setdefault("pauseAfter", 1500 if nxt and nxt.get("chapter") else 600)
            assert 400 <= b["pauseAfter"] <= 2000, f"pauseAfter out of range in beat"
            fp = narrate.file_of(reel_file[where], n); e = NIDX.get(fp)
            if e and os.path.exists(fp) and e["sha"] == narrate.sha(c["text"]):
                assert os.path.getsize(fp) < 80_000, f"{fp} too big"
                b["audio"] = fp; b["audioMs"] = e["ms"]
            else:
                assert SILENT_OK, f"{stop['label']} {where} beat {n}: no recording for this text, run build/narrate.py (or TLM_ALLOW_SILENT=1)"
                print("warning: no voice for", stop["label"], where, "beat", n)
        (play if where == "play" else tin)["words"] = words
NOTE = "Outlines are approximate. Drawn by The Long Map from the sources in each fact box, not traced from one published map. Solid = core area well documented. Dashed = extent uncertain. Coastline and rivers are modern."
zmap = {"egypt":"egypt","hatti":"hatti","assyria":"assyria","babylon":"babylon_s","elam":"elam","israel":"israelp"}
labelAt = {k: c.get("labelAt") for k,c in era1207.get("cards",{}).items()} or era1207.get("labelAt")
# the people label "Israel" sits inside the central hill country (it used to hang out over the sea west of the coast)
labelAt["israel"] = story_jews.NAR.ISRAEL_LABEL
era = {"year":-1207,"label":"1207 BC","zones":era1207["zones"],"zoneObjects":zmap,"labelAt":labelAt,"note":NOTE}
# c. 1150 BC: the map where the 1207 BC Play ends, taken from that Play's own border steps:
# the Hittite empire gone, Egyptian-held Canaan gone, Israel's villages drawn over the central hill country,
# and Philistia (dashed) on the southern coast. Nothing else is redrawn.
def border_adds(beats):
    out = {}
    for b in beats:
        for x in b["steps"]:
            for a in x.get("add", []) if x["type"] == "border" else []: out[a["zone"]] = a
    return out
ADD = border_adds(story_jews.NAR.PLAY)
f1150 = []
for f in era1207["zones"]["features"]:
    z, c = f["properties"]["zone"], f["properties"]["certainty"]
    if z == "hatti" or (z == "egypt" and c == "unsure"): continue
    if z == "israel":
        h = ADD["highlands"]
        f = {"type":"Feature","properties":{"zone":"israel","certainty":"people","part":"Central hill country, Iron I villages (drawn for c. 1150 BC)"},
             "geometry":{"type":"Polygon","coordinates":[h["coords"]]}}
    f1150.append(f)
ph = ADD["philistia"]
f1150.append({"type":"Feature","properties":{"zone":"philistia","certainty":"unsure","part":"Philistine cities of the southern coast (drawn for c. 1150 BC; extent uncertain)"},
              "geometry":{"type":"Polygon","coordinates":[ph["coords"]]}})
z1150 = {k: v for k, v in zmap.items() if k != "hatti"}; z1150["philistia"] = "philistines"
l1150 = {k: v for k, v in labelAt.items() if k != "hatti"}; l1150["israel"] = ADD["highlands"]["labelAt"]; l1150["philistia"] = ph["labelAt"]
# the same words the Play wrote on the map, so the label does not change at the hand-over
zl1150 = {"israel": ADD["highlands"]["label"], "philistia": ph["label"]}
era1150 = {"year":-1150,"label":"c. 1150 BC","zones":{"type":"FeatureCollection","features":f1150},"zoneObjects":z1150,"labelAt":l1150,"zoneLabels":zl1150,"note":NOTE}
# c. 1000 BC: the c. 1150 BC map (no border for David or Solomon) plus the neighbours east of the Jordan,
# dashed because their extent around 1000 BC is uncertain. The Play draws the split of c. 930 BC itself.
NEIGH = {
 "ammon":([[35.62,32.30],[35.95,32.38],[36.25,32.18],[36.25,31.85],[36.0,31.72],[35.72,31.78],[35.6,32.0],[35.62,32.30]],"Ammon, around Rabbah (drawn for c. 1000 BC; extent uncertain)",[36.02,32.06],"AMMON"),
 "moab":([[35.6,31.7],[35.95,31.7],[36.12,31.4],[36.0,31.06],[35.62,31.06],[35.58,31.4],[35.6,31.7]],"Moab, the plateau east of the Dead Sea (drawn for c. 1000 BC; extent uncertain)",[35.86,31.33],"MOAB"),
 "edom":([[35.42,31.0],[35.9,30.98],[35.85,30.3],[35.45,29.95],[35.17,30.25],[35.25,30.75],[35.42,31.0]],"Edom, the highlands and Arabah south-east of the Dead Sea (drawn for c. 1000 BC; extent uncertain)",[35.58,30.5],"EDOM")}
f1000 = [dict(f) for f in f1150] + [{"type":"Feature","properties":{"zone":z,"certainty":"unsure","part":p},"geometry":{"type":"Polygon","coordinates":[c]}} for z,(c,p,_,_) in NEIGH.items()]
z1000 = dict(z1150, ammon="ammon", moab="moab", edom="edom")
l1000 = dict(l1150, **{z: v[2] for z, v in NEIGH.items()})
zl1000 = dict(zl1150, **{z: v[3] for z, v in NEIGH.items()})
era1000 = {"year":-1000,"label":"c. 1000 BC","zones":{"type":"FeatureCollection","features":f1000},"zoneObjects":z1000,"labelAt":l1000,"zoneLabels":zl1000,"note":NOTE}
stop = story_jews.STOP; stop1150 = story_jews.STOP1150; stop1000 = story_jews.STOP1000
check_stop(stop, era, "jews-1207")
check_stop(stop1150, era1150, "jews-1150")
check_stop(stop1000, era1000, "jews-1000")
def w(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    json.dump(d, open(p,"w"), ensure_ascii=False, separators=(",",":"))
    print(p, os.path.getsize(p))
w("data/sources.json", src)
w("data/objects/near-east.json", {"library":"near-east","note":"Shared by all stories. Each object is one small fact box.","objects":objs})
w("data/eras/1207bc.json", era)
w("data/eras/1150bc.json", era1150)
w("data/eras/1000bc.json", era1000)
w("data/stories/jews/story.json", story_jews.STORY)
w("data/stories/jews/1207bc.json", stop)
w("data/stories/jews/1150bc.json", stop1150)
w("data/stories/jews/1000bc.json", stop1000)
for st in (stop, stop1150, stop1000):
    play, tin = st["play"], st["transitionIn"]
    print(st["label"], "events", len(st["events"]), "play beats", len(play["beats"]), "words", play["words"], "voice min", round(sum(b.get("audioMs", b["duration"])+b["pauseAfter"] for b in play["beats"])/60000, 1),
          "opening beats", len(tin["beats"]) if isinstance(tin, dict) else 0, "explore keys", len(st["explore"]["key"]))
print("objects", len(objs), "sources", len(src))
