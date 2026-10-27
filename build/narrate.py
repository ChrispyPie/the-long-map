"""Records the narration: one mp3 per beat, in assets/narration/. Run from the repo root:
  ELEVENLABS_API_KEY=... python3 build/narrate.py            (records only lines that are new or changed)
The key is read from the environment only and is never written or printed.
Voice: Grant Gravitas (ElevenLabs VC6vCXhVaI8BZefRtXZV), eleven_multilingual_v2, the voice's own settings
but speed 1.0 for a calm pace. Mono mp3, 22.05 kHz, 32 kbit/s.
Continuity: each line is sent with the request ids of up to three lines before it (request stitching)
and the text of the next line, so the reel sounds like one read.
Writes assets/narration/index.json: file -> {ms, sha} (ms from ffprobe, sha of the spoken text);
make_data.py uses ms as the line's real length and refuses lines whose text no longer matches.
"""
import hashlib, json, os, subprocess, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(__file__))
import narration_jews_1207 as N
VOICE = "VC6vCXhVaI8BZefRtXZV"; MODEL = "eleven_multilingual_v2"; FMT = "mp3_22050_32"
SETTINGS = {"stability": 0.32, "similarity_boost": 0.75, "style": 0.47, "use_speaker_boost": True, "speed": 1.0}
OUT = "assets/narration"; IDX = f"{OUT}/index.json"
REELS = {"jews-1207-in": N.INTRO_BEATS, "jews-1207-play": N.PLAY}
def sha(t): return hashlib.sha1(t.encode()).hexdigest()[:12]
def ms(fp):
    r = subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",fp], capture_output=True, text=True, check=True)
    return round(float(r.stdout) * 1000)
def tts(text, prev_ids, next_text):
    body = {"text": text, "model_id": MODEL, "voice_settings": SETTINGS, "previous_request_ids": prev_ids[-3:]}
    if next_text: body["next_text"] = next_text
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE}?output_format={FMT}",
        data=json.dumps(body).encode(), method="POST",
        headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json", "Accept": "audio/mpeg"})
    for n in range(4):
        try:
            with urllib.request.urlopen(req, timeout=120) as r: return r.read(), r.headers.get("request-id")
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and n < 3: time.sleep(5 * (n + 1)); continue
            raise SystemExit(f"ElevenLabs error {e.code}: {e.read()[:300]!r}")
def file_of(reel, i): return f"{OUT}/{reel}-{i+1:02d}.mp3"
if __name__ == "__main__":
    if not os.environ.get("ELEVENLABS_API_KEY"): raise SystemExit("set ELEVENLABS_API_KEY")
    idx = json.load(open(IDX)) if os.path.exists(IDX) else {}
    rid = {}  # request ids of this run, for stitching (not stored)
    chars = 0
    for reel, beats in REELS.items():
        ids = []
        for i, b in enumerate(beats):
            fp, t = file_of(reel, i), N.speech(b)
            if idx.get(fp, {}).get("sha") == sha(t) and os.path.exists(fp): ids = []; continue
            nxt = N.speech(beats[i+1]) if i + 1 < len(beats) else None
            audio, r = tts(t, ids, nxt); chars += len(t)
            open(fp, "wb").write(audio); ids.append(r)
            idx[fp] = {"ms": ms(fp), "sha": sha(t)}
            print(fp, idx[fp]["ms"], "ms", flush=True)
            json.dump(idx, open(IDX, "w"), indent=0, sort_keys=True)
    print("characters sent", chars)
