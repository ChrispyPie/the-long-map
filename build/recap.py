"""'The story so far': a short recap before Chapters 2-6 (reel jews-<year>-recap, recorded with build/narrate.py).

Very high level, no details: one or two lines per earlier chapter, so the recap grows with the book
(about 20 s before Chapter 2, about a minute before Chapter 5, about a minute and a half before Chapter 6). Newly written lines (not the chapters' own),
labelled and sourced like every other line; tradition stays tradition. Map moves only (no years, no borders),
so the map underneath stays the one the chapter starts on. It plays before the chapter's opening film or its
quick version, has its own Skip, and can be switched off (the ⚙ setting, or the checkbox on the Quick/Full card).
Each chapter's recap is its own recorded reel; no audio is shared between them.
"""
A, D, T, F = "attested", "disputed", "tradition", "frame"
def cap(text, cert, src=(), claims=None, ref=None, display=None):
    c = {"type": "caption", "text": text, "cert": cert, "src": list(src)}
    c["claims"] = claims if claims is not None else ([] if cert == F else [[text, cert, list(src)]])
    if ref: c["ref"] = ref
    if display: c["display"] = display
    return c
def fo(c, k): return {"type": "focus", "c": c, "k": k}
def B(text, cert, src=(), vis=(), **kw): return {"steps": list(vis) + [cap(text, cert, src, **kw)]}

OPEN = lambda: B("The story so far.", F, vis=[fo([35.4, 31.6], 2.4)])
# one block per finished chapter
CH1 = [B("In twelve oh seven BC, an Egyptian victory stone names a people called Israel, in Canaan. It is the oldest known mention of the name.",
         A, ["stele", "kitchen4", "hasel"], vis=[fo([33.2, 30.6], 2.3)],
         display="In 1207 BC, an Egyptian victory stone names a people called Israel, in Canaan. It is the oldest known mention of the name."),
       B("Canaan is ruled by Egypt then, in a world of great empires.", A, ["morris", "bryce2006"])]
CH2 = [B("Then the old world of the Bronze Age breaks down. Philistines settle on the coast, and small villages fill the hills.",
         A, ["cline", "killebrew", "fink2013"], vis=[fo([35.0, 31.9], 4.5)]),
       B("Jewish tradition remembers this as the time of the Judges, and of the first kings.", T, ["bible"], ref="Judges; 1 Samuel 8–10")]
CH3 = [B("The Bible tells of David and Solomon, ruling from Jerusalem, and of the temple Solomon built.", T, ["bible"], ref="2 Samuel 5; 1 Kings 6",
         vis=[fo([35.235, 31.777], 9)]),
       B("How large their kingdom was is debated. But by about nine thirty BC there are two kingdoms: Israel in the north, and Judah in the south.",
         D, ["mazar2010", "finksilb2006", "biran1995"], vis=[fo([35.3, 32.2], 5.0)],
         claims=[["How large their kingdom was is debated.", D, ["mazar2010", "finksilb2006"]],
                 ["By about 930 BC there are two kingdoms: Israel in the north, and Judah in the south.", A, ["biran1995", "mazar2010"]]],
         display="How large their kingdom was is debated. But by about 930 BC there are two kingdoms: Israel in the north, and Judah in the south.")]
CH4 = [B("Pharaoh Sheshonq, the Bible's Shishak, marches through the land, and lists the places he took on a temple wall at Karnak.",
         A, ["wilson2005", "kitchen1996"], vis=[fo([33.5, 31.0], 3.4)]),
       B("Israel grows strong under Omri and Ahab, with its capital at Samaria. Then Assyria arrives, and King Jehu pays it tribute.",
         A, ["franklin2004", "grayson1996", "bmblackobelisk"], vis=[fo([38.5, 33.6], 2.0)])]

CH5 = [B("Under Jeroboam the Second, Israel grows rich, and the prophets Amos and Hosea speak of justice and faithfulness.",
         T, ["bible", "fink2013"], ref="2 Kings 14:23–29; Amos; Hosea", vis=[fo([35.25, 32.25], 7.0)],
         claims=[["Under Jeroboam the Second, Israel grows rich.", D, ["fink2013", "reisner1924"]],
                 ["The prophets Amos and Hosea speak of justice and faithfulness.", T, ["bible"]]]),
       B("Then Assyria returns to stay. Tiglath-pileser the Third takes Damascus and Galilee, and in seven twenty two BC Samaria falls.",
         A, ["tadmor2011", "grayson1975", "frame2021"], vis=[fo([36.6, 33.4], 3.0)],
         display="Then Assyria returns to stay. Tiglath-pileser III takes Damascus and Galilee, and in 722 BC Samaria falls."),
       B("Many of Israel's people are carried off to Assyria. In the south, Judah survives, as a vassal of the empire.",
         A, ["younger1998", "frame2021"], vis=[fo([35.2, 31.7], 6.0)])]

def recap(n_done):
    """the recap before chapter n_done + 1"""
    beats = [OPEN()] + [b for blk in [CH1, CH2, CH3, CH4, CH5][:n_done] for b in blk]
    import copy; beats = copy.deepcopy(beats)
    beats[0]["chapter"] = "The story so far"; beats[0]["ambient"] = "desert"
    beats[-1]["pauseAfter"] = 1200
    return beats
RECAPS = {1150: recap(1), 1000: recap(2), 930: recap(3), 722: recap(4), 701: recap(5)}
speech = lambda b: b["steps"][-1]["text"]
for bs in RECAPS.values():
    for b in bs:
        c = b["steps"][-1]; import re
        assert not re.search(r"[()\d]", c["text"]), c["text"]
