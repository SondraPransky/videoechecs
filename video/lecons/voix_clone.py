"""Voix clonée avec Chatterbox (Resemble AI, licence MIT), sur processeur.

Appelé par voix.py dans l'environnement Python qui contient chatterbox-tts :
  python voix_clone.py jobs.json
jobs.json : {"ref": "voix.wav", "exaggeration": 0.35, "cfg": 0.3,
             "jobs": [{"text": ..., "out": ...wav, "vc_source": optionnel}]}

Chaque réplique est lue phrase par phrase (le modèle décroche au-delà de ~25 s),
puis les phrases sont recollées avec une courte pause. Avec vc_source, on ne
synthétise pas : on convertit une voix existante (ElevenLabs…) vers le timbre de ref.
"""
import json
import re
import sys
import warnings

import torch
import torchaudio as ta

warnings.filterwarnings("ignore")
torch.set_num_threads(4)

cfg = json.load(open(sys.argv[1], encoding="utf-8"))
tts = vc = None
GAP = 0.22


def sentences(text):
    parts = re.findall(r"[^.!?…]+[.!?…]*", text)
    out = []
    for p in (s.strip() for s in parts):
        if not p:
            continue
        # phrases très longues : on coupe aux virgules
        while len(p) > 220 and "," in p[:220]:
            k = p[:220].rfind(",") + 1
            out.append(p[:k].strip()); p = p[k:].strip()
        out.append(p)
    return out


for k, job in enumerate(cfg["jobs"]):
    if job.get("vc_source"):
        if vc is None:
            from chatterbox.vc import ChatterboxVC
            vc = ChatterboxVC.from_pretrained("cpu")
        wav = vc.generate(job["vc_source"], target_voice_path=cfg["ref"])
        ta.save(job["out"], wav, vc.sr)
        spans = None
    else:
        if tts is None:
            from chatterbox.mtl_tts import ChatterboxMultilingualTTS
            tts = ChatterboxMultilingualTTS.from_pretrained(device="cpu")
        pieces, spans, t = [], [], 0.0
        for s in sentences(job["text"]):
            torch.manual_seed(1234)
            w = tts.generate(s, language_id="fr", audio_prompt_path=cfg["ref"],
                             exaggeration=cfg.get("exaggeration", 0.35), cfg_weight=cfg.get("cfg", 0.3))
            d = w.shape[-1] / tts.sr
            spans.append([s, round(t, 3), round(t + d, 3)])
            pieces += [w, torch.zeros(1, int(GAP * tts.sr))]
            t += d + GAP
        ta.save(job["out"], torch.cat(pieces[:-1], dim=-1), tts.sr)
    json.dump({"spans": spans}, open(job["out"] + ".json", "w"))
    print(f"{k + 1}/{len(cfg['jobs'])}", flush=True)
