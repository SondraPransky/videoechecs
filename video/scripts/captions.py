"""Sous-titres WebVTT à partir de voice/script.txt et build/timing.json."""
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
timing = json.load(open(os.path.join(ROOT, "build", "timing.json")))
text = dict(l.rstrip("\n").split("|", 1) for l in open(os.path.join(ROOT, "voice", "script.txt"), encoding="utf-8") if l.strip())
fix = lambda s: s.replace("Échecs point com", "echecs.com").replace("échecs point com", "echecs.com")
ts = lambda t: f"00:{int(t // 60):02d}:{t % 60:06.3f}"
out = ["WEBVTT", ""]
for v in timing["vo"]:
    out += [f'{ts(v["at"])} --> {ts(v["at"] + v["dur"])}', fix(text[v["id"]]), ""]
open(os.path.join(ROOT, "build", "sous-titres.vtt"), "w", encoding="utf-8").write("\n".join(out))
