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
stop = story_jews.STOP
for e in stop["events"]:
    chk(e["src"], e["id"]); assert e["cert"] in CERT
    for c in e["claims"]: chk(c[2], e["id"]); assert c[1] in CERT
    for i in e["objects"] + e["hl"]: assert i in ids, f"unknown object {i} in {e['id']}"
for i in stop["keyObjects"]: assert i in ids
for i in stop["explore"]["key"]: assert i in ids, f"unknown explore key {i}"
era = json.load(open("data/eras/1207bc.json"))
# narrated films: the opening film (transitionIn.beats) and Play. Every caption sourced and labelled,
# every id/zone known. Labels: attested / disputed / tradition, "scene" (evocative only: no sources,
# must read as "Imagine ...") and, in the opening film only, "frame" (the film's own framing lines:
# no sources, no facts). Spoken text has no digits or brackets; "display" is the subtitle with digits.
TYPES = {"caption","focus","migration","border","battle","year"}
play = stop["play"]; zones_known = {f["properties"]["zone"] for f in era["zones"]["features"]} | set(play["zoneObjects"])
for v in play["zoneObjects"].values(): assert v in ids
tin = stop["transitionIn"]
assert isinstance(tin, str) or (isinstance(tin, dict) and isinstance(tin.get("text"), str)), "transitionIn: a string, or {text, beats}"
REELS = [("play", play["beats"], False)] + ([("intro", tin["beats"], True)] if isinstance(tin, dict) and tin.get("beats") else [])
def check_reel(where, beats, frame_ok):
    assert beats and "chapter" in beats[0], f"{where}: the first beat opens a chapter"
    assert sum(1 for b in beats if b.get("choice")) == (1 if where == "intro" else 0), f"{where}: choice beats"
    for n,b in enumerate(beats):
        caps = [x for x in b["steps"] if x["type"]=="caption"]
        assert len(caps) == 1, f"{where} beat {n} needs exactly one caption"
        if "chapter" in b: assert isinstance(b["chapter"], str) and 2 < len(b["chapter"]) < 40, b["chapter"]
        for x in b["steps"]:
            assert x["type"] in TYPES, x["type"]
            if x["type"]=="caption":
                assert not re.search(r"[()\d]", x["text"]), f"{where} beat {n}: spoken text has digits or brackets"
                if "display" in x: assert isinstance(x["display"], str) and x["display"] != x["text"], f"{where} beat {n}: display"
                if "ref" in x: assert isinstance(x["ref"], str) and "bible" in x["src"], f"{where} beat {n}: ref needs the bible source"
                if x["cert"]=="scene":
                    assert not x["src"] and x["text"].startswith("Imagine"), f"scene caption in {where} beat {n} must start with 'Imagine'"
                elif x["cert"]=="frame":
                    assert frame_ok and not x["src"] and not x.get("claims"), f"frame caption in {where} beat {n}: opening film only, no sources"
                else: chk(x["src"], f"{where} beat {n}"); assert x["cert"] in CERT
                for c in x.get("claims", []): chk(c[2], f"{where} beat {n}"); assert c[1] in CERT
            if x["type"] in ("migration","battle"): assert x["cert"] in CERT
            for a in x.get("arrows",[]): assert a["cert"] in CERT and a["side"] in ("egypt","enemy")
            for i in x.get("hl",[]): assert i in ids, f"unknown hl {i} in {where} beat {n}"
            for f in x.get("fade",[]) + x.get("add",[]): assert f["zone"] in zones_known, f["zone"]
for where, beats, frame_ok in REELS: check_reel(where, beats, frame_ok)
# pacing (see build/README.md): each beat gets duration = reading time of its line (~2.5 words/s, at
# least 2 s; used when the voice is off) and pauseAfter (0.6 s, 1.5 s before a new chapter) unless set by hand. With the voice
# on the recorded line sets the length: audio + audioMs come from assets/narration/index.json
# (build/narrate.py); a line whose text changed since it was recorded is refused.
NIDX = json.load(open(narrate.IDX)) if os.path.exists(narrate.IDX) else {}
SILENT_OK = os.environ.get("TLM_ALLOW_SILENT") == "1"   # build without the voice for lines not recorded yet
REEL_FILE = {"intro":"jews-1207-in", "play":"jews-1207-play"}
for where, beats, _ in REELS:
    words = 0
    for n,b in enumerate(beats):
        c = next(x for x in b["steps"] if x["type"]=="caption"); wc = len(c["text"].split()); words += wc
        b.setdefault("duration", max(2000, round(wc / 2.5 * 10) * 100))
        # short natural gap after a line; a longer breath only before a new chapter
        nxt = beats[n + 1] if n + 1 < len(beats) else None
        b.setdefault("pauseAfter", 1500 if nxt and nxt.get("chapter") else 600)
        assert 400 <= b["pauseAfter"] <= 2000, f"pauseAfter out of range in beat"
        fp = narrate.file_of(REEL_FILE[where], n); e = NIDX.get(fp)
        if e and os.path.exists(fp) and e["sha"] == narrate.sha(c["text"]):
            assert os.path.getsize(fp) < 80_000, f"{fp} too big"
            b["audio"] = fp; b["audioMs"] = e["ms"]
        else:
            assert SILENT_OK, f"{where} beat {n}: no recording for this text, run build/narrate.py (or TLM_ALLOW_SILENT=1)"
            print("warning: no voice for", where, "beat", n)
    (play if where == "play" else tin)["words"] = words
zmap = {"egypt":"egypt","hatti":"hatti","assyria":"assyria","babylon":"babylon_s","elam":"elam","israel":"israelp"}
labelAt = {k: c.get("labelAt") for k,c in era.get("cards",{}).items()} or era.get("labelAt")
# the people label "Israel" sits inside the central hill country (it used to hang out over the sea west of the coast)
labelAt["israel"] = story_jews.NAR.ISRAEL_LABEL
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
print("objects", len(objs), "events", len(stop["events"]), "sources", len(src), "play beats", len(play["beats"]), "words", play["words"], "voice min", round(sum(b.get("audioMs", b["duration"])+b["pauseAfter"] for b in play["beats"])/60000, 1),
      "opening beats", len(tin["beats"]) if isinstance(tin, dict) else 0, "explore keys", len(stop["explore"]["key"]))
