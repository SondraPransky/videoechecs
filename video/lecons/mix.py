"""Mixage d'une leçon : voix off + bruitages (coups, prises, compte à rebours des quiz, transitions).

Usage : python3 lecons/mix.py <nom>   → build/lecons/<nom>/mix.wav
Les bruitages sont synthétisés ici, donc libres de droits.
"""
import json
import os
import subprocess
import sys
import wave

import imageio_ffmpeg
import numpy as np

SR = 48000
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = np.random.default_rng(7)


def env(n, attack, decay):
    t = np.arange(n) / SR
    return np.minimum(1, t / max(attack, 1e-4)) * np.exp(-t / decay)


def bandnoise(n, lo, hi):
    spec = np.fft.rfft(rng.standard_normal(n))
    f = np.fft.rfftfreq(n, 1 / SR)
    spec[(f < lo) | (f > hi)] = 0
    x = np.fft.irfft(spec, n)
    return x / (np.abs(x).max() + 1e-9)


def tone(n, freq, decay):
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * freq * t) * np.exp(-t / decay)


def click(level=1.0):
    """Pièce posée sur un échiquier en bois : attaque sèche + petit corps grave."""
    n = int(0.16 * SR)
    x = 0.55 * bandnoise(n, 1200, 5200) * env(n, 0.0005, 0.012) + 0.7 * tone(n, 190, 0.035) + 0.25 * tone(n, 420, 0.02)
    return level * 0.22 * x / np.abs(x).max()


SOUNDS = {
    "move": click(1.0),
    "capture": np.concatenate([click(0.8)[: int(0.05 * SR)], click(1.25)]),
    "tick": 0.09 * tone(int(0.09 * SR), 1320, 0.02),
    "reveal": 0.12 * np.concatenate([tone(int(0.12 * SR), 784, 0.08), tone(int(0.5 * SR), 1175, 0.18)]),
}
n = int(0.7 * SR)
sweep = bandnoise(n, 300, 6000) * np.sin(np.linspace(0, np.pi, n)) ** 2
SOUNDS["whoosh"] = 0.10 * sweep


def read_wav(path):
    with wave.open(path) as w:
        assert w.getframerate() == SR and w.getnchannels() == 1
        return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768


def main(name):
    base = os.path.join(ROOT, "build", "lecons", name)
    ev = json.load(open(os.path.join(base, "events.json")))
    durs = json.load(open(os.path.join(base, "voix", "durees.json")))
    total = int(ev["total"] * SR) + SR
    voice = np.zeros(total, np.float32)
    fx = np.zeros(total, np.float32)
    for v in ev["voice"]:
        x = read_wav(durs[v["id"]]["wav"])
        i = int(v["at"] * SR)
        voice[i:i + len(x)] += x[: total - i]
    for e in ev["events"]:
        x = SOUNDS[e["type"]]
        i = int(e["t"] * SR)
        fx[i:i + len(x)] += x[: total - i]
    mix = voice + fx
    tmp = os.path.join(base, "mix-brut.wav")
    with wave.open(tmp, "wb") as w:
        w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
        w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes())
    ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
    subprocess.run([ffmpeg, "-y", "-loglevel", "error", "-i", tmp,
                    "-af", "highpass=f=70,acompressor=threshold=-20dB:ratio=2.5:attack=5:release=150,loudnorm=I=-16:TP=-1.5:LRA=9",
                    "-ar", str(SR), "-ac", "2", "-t", str(ev["total"]), os.path.join(base, "mix.wav")], check=True)
    os.remove(tmp)
    print("écrit", os.path.join(base, "mix.wav"))


if __name__ == "__main__":
    main(sys.argv[1])
