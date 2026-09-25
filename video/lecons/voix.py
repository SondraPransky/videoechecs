"""Voix off d'une leçon : une piste WAV par réplique de build/lecons/<nom>/plan.json.

Usage :
  python3 lecons/voix.py <nom>                    # voix libre Piper (maquette)
  python3 lecons/voix.py <nom> --eleven [--voice ID] [--model eleven_flash_v2_5]
  python3 lecons/voix.py --voices                 # voix ElevenLabs disponibles sur le compte

Les pistes sont mises en cache par texte (build/lecons/<nom>/voix/<moteur>/<id>.wav) :
modifier une réplique ne refait que celle-là. Écrit voix/durees.json, et pour ElevenLabs
l'instant de chaque caractère, qui sert à caler les coups sur la voix.
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import urllib.request
import wave

import imageio_ffmpeg
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()
PIPER_MODEL = os.path.join(ROOT, "voice", "models", "fr_FR-tom-medium.onnx")
API = "https://api.elevenlabs.io/v1"
SETTINGS = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.35, "use_speaker_boost": True, "speed": 1.05}

# Prononciation : « e5 » doit se dire « é cinq », pas « euh cinq ». Remplacements de même
# longueur autant que possible, pour que les repères du texte restent alignés.
SAY = [
    (r"\be(?=[1-8]\b)", "é"),
    (r"\be prend\b", "é prend"),
    (r"\bKoneru\b", "Konérou"),
    (r"\bVidit\b", "Vidite"),
]


def spoken(text):
    for a, b in SAY:
        text = re.sub(a, b, text)
    return text


def to_wav(src, dst, trim=True):
    """Convertit en WAV mono 48 kHz ; renvoie le silence de tête retiré (s)."""
    raw = subprocess.run([FFMPEG, "-loglevel", "error", "-i", src, "-f", "s16le", "-ac", "1", "-ar", "48000", "-"],
                         capture_output=True, check=True).stdout
    x = np.frombuffer(raw, np.int16).astype(np.float32)
    lead = 0
    if trim:
        loud = np.nonzero(np.abs(x) > 32768 * 10 ** (-42 / 20))[0]
        if len(loud):
            lead = max(0, loud[0] - 480)
            x = x[lead:min(len(x), loud[-1] + 2400)]
    with wave.open(dst, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
        w.writeframes(x.astype(np.int16).tobytes())
    return lead / 48000, len(x) / 48000


def piper(text, dst):
    from piper import PiperVoice, SynthesisConfig
    global _voice
    if "_voice" not in globals():
        _voice = PiperVoice.load(PIPER_MODEL)
    tmp = dst + ".tmp.wav"
    with wave.open(tmp, "wb") as w:
        _voice.synthesize_wav(spoken(text), w, syn_config=SynthesisConfig(length_scale=0.9))
    _, dur = to_wav(tmp, dst)
    os.remove(tmp)
    return {"dur": round(dur, 3), "len": len(text)}


def eleven_call(path, body=None):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": os.environ["ELEVENLABS_API_KEY"], "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=180) as r:
        return json.loads(r.read())


def eleven(text, dst, voice, model, prev, nxt):
    say = spoken(text)
    body = {"text": say, "model_id": model, "voice_settings": SETTINGS, "language_code": "fr"}
    if prev: body["previous_text"] = spoken(prev)
    if nxt: body["next_text"] = spoken(nxt)
    r = eleven_call(f"/text-to-speech/{voice}/with-timestamps?output_format=mp3_44100_192", body)
    mp3 = dst + ".mp3"
    open(mp3, "wb").write(base64.b64decode(r["audio_base64"]))
    lead, dur = to_wav(mp3, dst)
    os.remove(mp3)
    al = r.get("alignment") or {}
    starts = al.get("character_start_times_seconds") or []
    # Instant de chaque caractère du texte affiché (les deux textes ont presque la même longueur)
    chars = [round(max(0.0, starts[min(len(starts) - 1, int(k * len(starts) / max(1, len(text))))] - lead), 3)
             for k in range(len(text) + 1)] if starts else None
    return {"dur": round(dur, 3), "len": len(text), "chars": chars}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("name", nargs="?")
    ap.add_argument("--eleven", action="store_true")
    ap.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    ap.add_argument("--model", default="eleven_flash_v2_5")
    ap.add_argument("--voices", action="store_true")
    a = ap.parse_args()
    if a.voices:
        for v in eleven_call("/voices")["voices"]:
            print(v["voice_id"], v["name"], v.get("category"), v.get("labels"))
        return
    base = os.path.join(ROOT, "build", "lecons", a.name)
    plan = json.load(open(os.path.join(base, "plan.json"), encoding="utf-8"))["beats"]
    engine = "eleven-" + a.voice if a.eleven else "piper"
    if a.eleven and not (os.environ.get("ELEVENLABS_API_KEY") and a.voice):
        sys.exit("ElevenLabs : il faut ELEVENLABS_API_KEY et --voice (ou ELEVENLABS_VOICE_ID).")
    cache = os.path.join(base, "voix", engine)
    os.makedirs(cache, exist_ok=True)
    index_path = os.path.join(cache, "index.json")
    index = json.load(open(index_path)) if os.path.exists(index_path) else {}
    lines = [b for b in plan if b["id"]]
    durs = {}
    for k, b in enumerate(lines):
        dst = os.path.join(cache, b["id"] + ".wav")
        if b["id"] not in index or not os.path.exists(dst):
            if a.eleven:
                index[b["id"]] = eleven(b["text"], dst, a.voice, a.model,
                                        lines[k - 1]["text"] if k else None, lines[k + 1]["text"] if k + 1 < len(lines) else None)
            else:
                index[b["id"]] = piper(b["text"], dst)
            json.dump(index, open(index_path, "w"))
            print(f"{k + 1}/{len(lines)} {index[b['id']]['dur']:.1f}s {b['text'][:70]}")
        durs[b["id"]] = {**index[b["id"]], "wav": dst}
    json.dump(durs, open(os.path.join(base, "voix", "durees.json"), "w"))
    print(f"{len(durs)} répliques, {sum(d['dur'] for d in durs.values()) / 60:.1f} min de voix ({engine})")


if __name__ == "__main__":
    main()
