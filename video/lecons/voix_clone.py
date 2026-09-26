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
    parts = [p.strip() for p in re.findall(r"[^.!?…]+[.!?…]*", text) if p.strip()]
    # les fragments très courts (« Dame é trois ! ») font divaguer le modèle : on les regroupe
    merged = []
    for p in parts:
        if merged and (len(merged[-1]) < 70 or len(p) < 25) and len(merged[-1]) + len(p) < 200:
            merged[-1] += " " + p
        else:
            merged.append(p)
    out = []
    for p in merged:
        # phrases très longues : on coupe aux virgules
        while len(p) > 220 and "," in p[:220]:
            k = p[:220].rfind(",") + 1
            out.append(p[:k].strip()); p = p[k:].strip()
        out.append(p)
    return out


# Contrôle par reconnaissance vocale : une phrase mal lue (mots inventés, cases avalées)
# est régénérée avec une autre graine, et on garde la meilleure prise.
try:
    from faster_whisper import WhisperModel
    import difflib
    import numpy as np
    asr = WhisperModel("small", device="cpu", compute_type="int8", cpu_threads=4)
except ImportError:
    asr = None
DIGITS = dict(zip("12345678", ["un", "deux", "trois", "quatre", "cinq", "six", "sept", "huit"]))


def squash(t):
    t = re.sub(r"[1-8]", lambda m: " " + DIGITS[m.group()] + " ", t.lower())
    return re.sub(r"[^a-zàâçéèêëîïôûùüÿœ]", "", t)


def score(wav, sr, text):
    if asr is None:
        return 1.0
    import torchaudio.functional as F
    x = F.resample(wav, sr, 16000)[0].numpy().astype(np.float32)
    hyp = " ".join(s.text for s in asr.transcribe(x, language="fr", beam_size=1)[0])
    return difflib.SequenceMatcher(None, squash(text), squash(hyp)).ratio()


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
            best = None
            for seed in (1234, 7, 99):
                torch.manual_seed(seed)
                w = tts.generate(s, language_id="fr", audio_prompt_path=cfg["ref"],
                                 exaggeration=cfg.get("exaggeration", 0.35), cfg_weight=cfg.get("cfg", 0.3))
                q = score(w, tts.sr, s)
                if best is None or q > best[0]:
                    best = (q, w)
                if q >= 0.8:
                    break
            q, w = best
            if q < 0.8:
                print(f"  prise imparfaite ({q:.2f}) : {s[:70]}", flush=True)
            d = w.shape[-1] / tts.sr
            spans.append([s, round(t, 3), round(t + d, 3)])
            pieces += [w, torch.zeros(1, int(GAP * tts.sr))]
            t += d + GAP
        ta.save(job["out"], torch.cat(pieces[:-1], dim=-1), tts.sr)
    json.dump({"spans": spans}, open(job["out"] + ".json", "w"))
    print(f"{k + 1}/{len(cfg['jobs'])}", flush=True)
