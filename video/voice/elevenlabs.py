"""Voix off ElevenLabs : une piste WAV par réplique de script.txt.

Usage :
  python3 voice/elevenlabs.py --list            # voix françaises masculines du catalogue
  python3 voice/elevenlabs.py [--voice ID]      # génère voice/out/NN.wav

La clé est lue dans ELEVENLABS_API_KEY. La voix par défaut peut être fixée
avec ELEVENLABS_VOICE_ID.
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request

import imageio_ffmpeg

HERE = os.path.dirname(os.path.abspath(__file__))
API = "https://api.elevenlabs.io/v1"
KEY = os.environ.get("ELEVENLABS_API_KEY")
MODEL = "eleven_multilingual_v2"
# Réglages « pub dynamique » : peu de stabilité = plus d'expressivité
SETTINGS = {"stability": 0.32, "similarity_boost": 0.8, "style": 0.55, "use_speaker_boost": True, "speed": 1.08}


def call(path, body=None, params=None):
    url = API + path + ("?" + urllib.parse.urlencode(params) if params else "")
    req = urllib.request.Request(url, data=json.dumps(body).encode() if body else None,
                                 headers={"xi-api-key": KEY, "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read()


def list_voices():
    data = json.loads(call("/shared-voices", params={"language": "fr", "gender": "male", "page_size": 40, "sort": "trending"}))
    for v in data.get("voices", []):
        print(f'{v["voice_id"]}  {v.get("name", "")[:28]:28}  âge={v.get("age", "")!s:12} accent={v.get("accent", "")!s:12} usage={v.get("use_case", "")!s:18} {v.get("descriptive", "")}')


def synth(voice_id):
    lines = [l.rstrip("\n").split("|", 1) for l in open(os.path.join(HERE, "script.txt"), encoding="utf-8") if l.strip()]
    os.makedirs(os.path.join(HERE, "out"), exist_ok=True)
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    for k, (id_, text) in enumerate(lines):
        body = {"text": text, "model_id": MODEL, "voice_settings": SETTINGS}
        if k > 0:
            body["previous_text"] = lines[k - 1][1]
        if k < len(lines) - 1:
            body["next_text"] = lines[k + 1][1]
        mp3 = call(f"/text-to-speech/{voice_id}", body, params={"output_format": "mp3_44100_192"})
        src = os.path.join(HERE, "out", f"{id_}.mp3")
        open(src, "wb").write(mp3)
        # WAV mono 48 kHz, silences de début/fin coupés
        subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", src, "-af",
                        "silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse",
                        "-ar", "48000", "-ac", "1", os.path.join(HERE, "out", f"{id_}.wav")], check=True)
        os.remove(src)
        print("ok", id_, text)


if __name__ == "__main__":
    if not KEY:
        sys.exit("ELEVENLABS_API_KEY absente de l'environnement.")
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--voice", default=os.environ.get("ELEVENLABS_VOICE_ID"))
    a = ap.parse_args()
    if a.list:
        list_voices()
    elif not a.voice:
        sys.exit("Choisir une voix : --voice ID (voir --list).")
    else:
        synth(a.voice)
