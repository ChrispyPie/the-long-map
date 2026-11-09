"""Quick versions built from a chapter's own recorded script (Chapters 3-5).

A quick reel is a short list of the chapter's existing lines, picked along its big fact boxes, so every line keeps
its label, sources, claims, Bible ref, subtitle digits and map steps. pick() copies one line ("in07" = opening
film beat 7, "pl35" = Play beat 35); steps_from= adds another line's map steps (e.g. a border change from a line
that is left out, so the quick film ends on the same map as Play). QUICK_FROM keeps the source line of each quick
line, so build/vignettes.py can reuse that line's picture. Each picked line is recorded again in the quick reel.
"""
import copy
def pick(M, key, steps_from=(), types=("border",)):
    bs = M.INTRO_BEATS if key.startswith("in") else M.PLAY
    b = copy.deepcopy(bs[int(key[2:])])
    for k in ("chapter", "choice", "note", "ambient"): b.pop(k, None)
    extra = []
    for o in steps_from:
        ob = (M.INTRO_BEATS if o.startswith("in") else M.PLAY)[int(o[2:])]
        extra += [copy.deepcopy(x) for x in ob["steps"] if x["type"] in types]
    b["steps"] = b["steps"][:-1] + extra + b["steps"][-1:]
    return b
def frame(text, vis=()):
    return {"steps": list(vis) + [{"type": "caption", "text": text, "cert": "frame", "src": [], "claims": []}]}
def build(M, title, keys, opening, steps_map=None, amb="desert"):
    """keys: list of line keys; steps_map: key -> list of keys whose border steps it also runs"""
    steps_map = steps_map or {}
    Q = [frame(opening[0], opening[1])] + [pick(M, k, steps_map.get(k, ())) for k in keys]
    Q[0]["chapter"] = title; Q[0]["ambient"] = amb
    src = [None] + [M.speech((M.INTRO_BEATS if k.startswith("in") else M.PLAY)[int(k[2:])]) for k in keys]
    return Q, src
