"""Musique originale générée par code (donc libre de droits) pour la vidéo echecs.com.

Électro douce / piano moderne, 100 BPM, ré mineur. Les repères de structure
suivent le découpage des scènes de src/index.html (voir TIMELINE dans ce fichier).
Sortie : audio/music.wav (stéréo, 48 kHz).
"""
import os
import wave

import numpy as np

SR = 48000
BPM = 100
BEAT = 60 / BPM
DURATION = 62.0
OUT = os.path.join(os.path.dirname(__file__), "music.wav")

# Repères (secondes)
T_ARP = 3.0       # arpèges de piano
T_BEAT = 14.5     # kick doux
T_HATS = 25.0     # charleston
T_BREAK = 50.6    # montée avant le plan final
T_DROP = 52.5     # impact sur le logo
T_END = 60.0      # extinction

rng = np.random.default_rng(1959)
n_total = int(SR * DURATION)
L = np.zeros(n_total)
R = np.zeros(n_total)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def add(buf, start, sig, gain=1.0):
    i = int(start * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * gain


def lowpass(x, cutoff):
    a = np.broadcast_to(np.exp(-2 * np.pi * np.asarray(cutoff, dtype=float) / SR), x.shape)
    y = np.empty_like(x)
    acc = 0.0
    for k in range(len(x)):
        acc = (1 - a[k]) * x[k] + a[k] * acc
        y[k] = acc
    return y


def env_adsr(n, a, d, s, r):
    t = np.arange(n) / SR
    dur = n / SR
    e = np.where(t < a, t / max(a, 1e-4), 1.0)
    e = np.where((t >= a) & (t < a + d), 1 - (1 - s) * (t - a) / max(d, 1e-4), e)
    e = np.where(t >= a + d, s, e)
    e = e * np.clip((dur - t) / max(r, 1e-4), 0, 1)
    return e


def pad_voice(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for det in (-0.12, 0.0, 0.11):
        f = freq * 2 ** (det / 12)
        for h in range(1, 7):
            sig += np.sin(2 * np.pi * f * h * t + rng.uniform(0, 6.28)) / (h ** 1.6)
    return sig * env_adsr(n, 1.2, 0.5, 0.8, 1.4)


def piano(freq, dur=1.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    sig = np.zeros(n)
    for h, amp in enumerate((1.0, 0.45, 0.22, 0.12, 0.06), start=1):
        sig += amp * np.sin(2 * np.pi * freq * h * t * (1 + 0.0004 * h * h)) * np.exp(-t * (2.2 + h * 0.9))
    sig *= np.minimum(1, t / 0.004)
    return sig


def kick():
    n = int(0.45 * SR)
    t = np.arange(n) / SR
    f = 42 + 90 * np.exp(-t * 28)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 7.5)


def hat():
    n = int(0.08 * SR)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    x = x - lowpass(x, 7000)
    return x * np.exp(-t * 60)


# Progression : Dm9 – Bbmaj7 – Fmaj7 – C6 (2 mesures chacun)
CHORDS = [
    (50, [62, 65, 69, 72, 76]),   # Dm9
    (46, [58, 62, 65, 69, 74]),   # Bbmaj7
    (41, [57, 60, 64, 65, 69]),   # Fmaj7
    (48, [60, 64, 67, 69, 72]),   # C6
]
BAR = 4 * BEAT
CHORD_LEN = 2 * BAR

# Pad + basse
t = 0.0
ci = 0
while t < T_END:
    root, notes = CHORDS[ci % 4]
    dur = CHORD_LEN + 1.2
    pad = sum(pad_voice(midi(nn - 12), dur) for nn in notes[:4]) * 0.035
    add(L, t, pad * 1.0)
    add(R, t, pad * 0.92)
    if t >= T_BEAT - 0.01:
        n = int(CHORD_LEN * SR)
        tt = np.arange(n) / SR
        bass = np.sin(2 * np.pi * midi(root - 12) * tt) * env_adsr(n, 0.02, 0.3, 0.7, 0.3) * 0.16
        add(L, t, bass)
        add(R, t, bass)
    t += CHORD_LEN
    ci += 1

# Arpèges de piano (croches), motif montant/descendant
pattern = [0, 2, 4, 3, 1, 3, 4, 2]
step = BEAT / 2
k = 0
t = T_ARP
while t < T_BREAK:
    ci = int(t // CHORD_LEN) % 4
    notes = CHORDS[ci][1]
    nn = notes[pattern[k % 8]] + (12 if (k // 16) % 2 and t > T_BEAT else 0)
    vel = 0.10 if k % 2 == 0 else 0.07
    pan = 0.5 + 0.35 * np.sin(k * 0.7)
    p = piano(midi(nn))
    add(L, t, p, vel * (1.2 - pan))
    add(R, t, p, vel * (0.2 + pan))
    t += step
    k += 1

# Kick (temps 1 et 3), puis tous les temps après 25 s
t = T_BEAT
b = 0
while t < T_BREAK:
    if b % 2 == 0 or t >= T_HATS:
        kk = kick() * 0.33
        add(L, t, kk)
        add(R, t, kk)
    t += BEAT
    b += 1

# Charleston sur les contretemps
t = T_HATS + BEAT / 2
while t < T_BREAK:
    h = hat() * 0.05
    add(L, t, h * 0.8)
    add(R, t, h)
    t += BEAT

# Montée (bruit filtré qui s'ouvre)
n = int((T_DROP - T_BREAK) * SR)
x = rng.standard_normal(n)
tt = np.linspace(0, 1, n)
riser = (x - lowpass(x, 400 + 6000 * tt ** 2)) * tt ** 2 * 0.06
add(L, T_BREAK, riser)
add(R, T_BREAK, riser)

# Impact final : accord de Ré mineur large + grosse caisse + queue de piano
imp = kick() * 0.5
add(L, T_DROP, imp)
add(R, T_DROP, imp)
for nn in (38, 50, 57, 62, 65, 69, 74, 77):
    p = piano(midi(nn), 7.0) * 0.08
    add(L, T_DROP, p)
    add(R, T_DROP + 0.004, p)
final_pad = sum(pad_voice(midi(nn), 9.0) for nn in (50, 57, 62, 65, 69)) * 0.03
add(L, T_DROP, final_pad)
add(R, T_DROP, final_pad)


def reverb(x):
    y = x.copy()
    for d, g in ((0.0297, 0.5), (0.0371, 0.45), (0.0411, 0.42), (0.0437, 0.4), (0.113, 0.3), (0.171, 0.22), (0.263, 0.15)):
        k = int(d * SR)
        z = np.zeros_like(x)
        z[k:] = x[:-k] * g
        y += z
    return y


L = 0.7 * L + 0.3 * reverb(L)
R = 0.7 * R + 0.3 * reverb(R)

# Fondu d'entrée / sortie et normalisation
fade_in = np.minimum(1, np.arange(n_total) / (SR * 1.5))
fade_out = np.clip((DURATION - np.arange(n_total) / SR) / 3.0, 0, 1)
L *= fade_in * fade_out
R *= fade_in * fade_out
peak = max(np.abs(L).max(), np.abs(R).max())
L, R = L / peak * 0.89, R / peak * 0.89

data = (np.stack([L, R], axis=1) * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("écrit", OUT, f"{DURATION:.1f}s")
