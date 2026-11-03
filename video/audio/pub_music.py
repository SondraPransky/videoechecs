"""Musiques des publicités de 15 s (src/pub.html) : un style différent par question.

  1  électro-pop 124 BPM, la mineur        (classement bloqué → ça décolle)
  2  disco-funk 116 BPM, ré dorien         (« jouez moins, comprenez plus »)
  3  électro-pop de la vidéo longue, 120 BPM, ré mineur (on stagne… puis tout s'ouvre)
  4  trap cinématique 140 BPM, do mineur   (« passe à l'action ! »)
  5  électro-pop de la vidéo longue, 120 BPM, sol majeur (« suis le guide », lumineux)

Structure calée sur les scènes de la pub : question (0 → 3,9 s, ambiance qui retient son souffle),
« Nous avons la solution ! » (impact et départ du groove à 3,9 s), réponse, appel final (11,6 s).
Usage : python3 audio/pub_music.py STYLE SORTIE.wav
"""
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
STYLE = int(sys.argv[1])
OUT = sys.argv[2]
DURATION = 16.0
T_DROP, T_SOL, T_FINAL = 3.9, 6.4, 12.6
N = int(SR * (DURATION + .5))
L = np.zeros(N)
R = np.zeros(N)
rng = np.random.default_rng(100 + STYLE)


def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def add(buf, t, sig, g=1.0):
    i = int(t * SR)
    if i < 0:
        sig, i = sig[-i:], 0
    if i >= len(buf) or len(sig) == 0:
        return
    j = min(len(buf), i + len(sig))
    buf[i:j] += sig[: j - i] * g


def st(t, sig, g=1.0, pan=0.0):
    add(L, t, sig, g * (1 - max(0, pan)))
    add(R, t, sig, g * (1 + min(0, pan)))


def filt(x, kind, f, order=2):
    return sosfilt(butter(order, f, kind, fs=SR, output="sos"), x)


def saw(freq, n, phase=0.0):
    t = np.arange(n) / SR
    return 2 * ((freq * t + phase) % 1.0) - 1


def env(n, a, d, s, r):
    t = np.arange(n) / SR
    dur = n / SR
    return np.interp(t, [0, a, a + d, max(a + d, dur - r), dur], [0, 1, s, s, 0])


def noise(n):
    return rng.standard_normal(n)


# ------------------------------------------------------------------ instruments
def kick(punch=160, low=48, decay=9):
    n = int(.4 * SR)
    t = np.arange(n) / SR
    f = low + punch * np.exp(-t * 35)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * decay)
    return np.tanh((body + filt(noise(n), "highpass", 3000) * np.exp(-t * 400) * .3) * 1.6)


def k808(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = freq * (1 + 1.5 * np.exp(-t * 30))
    return np.tanh(np.sin(2 * np.pi * np.cumsum(f) / SR) * 2.2) * np.exp(-t * 1.6) * env(n, .002, .05, 1, .05)


def clap():
    n = int(.25 * SR)
    t = np.arange(n) / SR
    x = filt(noise(n), "bandpass", [900, 3500])
    e = sum(np.where(t >= dt, np.exp(-(t - dt) * (60 if k < 2 else 18)), 0) for k, dt in enumerate((0, .011, .022)))
    return x * e * .9


def snare(tone=190):
    n = int(.25 * SR)
    t = np.arange(n) / SR
    body = np.sin(2 * np.pi * tone * t) * np.exp(-t * 30)
    return body * .6 + filt(noise(n), "bandpass", [1500, 8000]) * np.exp(-t * 22)


def rim():
    n = int(.08 * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * 1700 * t) + .5 * filt(noise(n), "highpass", 2000)) * np.exp(-t * 90)


def hat(open_=False):
    n = int((.22 if open_ else .05) * SR)
    t = np.arange(n) / SR
    return filt(noise(n), "highpass", 8000) * np.exp(-t * (14 if open_ else 90))


def shaker():
    n = int(.09 * SR)
    t = np.arange(n) / SR
    return filt(noise(n), "bandpass", [4000, 11000]) * np.sin(np.pi * t / t[-1]) ** 2


def supersaw(notes, dur, cut=3200):
    n = int(dur * SR)
    x = np.zeros(n)
    for nn in notes:
        for det in (-.18, -.07, 0, .07, .18):
            x += saw(midi(nn) * 2 ** (det / 12), n, rng.random())
    return filt(x, "lowpass", cut) / (len(notes) * 5) * env(n, .01, .1, .8, .08)


def pad(notes, dur, cut=1800):
    n = int(dur * SR)
    x = np.zeros(n)
    for nn in notes:
        for det in (-.1, 0, .1):
            x += saw(midi(nn) * 2 ** (det / 12), n, rng.random())
    return filt(x, "lowpass", cut) / (len(notes) * 3) * env(n, .35, .2, .9, .4)


def rhodes(notes, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.zeros(n)
    for nn in notes:
        f = midi(nn)
        mod = np.sin(2 * np.pi * f * t) * 1.2 * np.exp(-t * 6)
        x += np.sin(2 * np.pi * f * t + mod) * np.exp(-t * 1.2)
    trem = 1 + .15 * np.sin(2 * np.pi * 4.5 * t)
    return x / len(notes) * trem * env(n, .005, .1, 1, .15)


def pluck(freq, dur=.25, bright=2500, dec=14):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return filt(saw(freq, n) * .6 + np.sin(2 * np.pi * freq * t), "lowpass", bright) * np.exp(-t * dec)


def marimba(freq, dur=.5):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return (np.sin(2 * np.pi * freq * t) + .35 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t * 30)) * np.exp(-t * 7)


def guitar(freq, dur=.6):
    """Corde pincée (Karplus-Strong)."""
    n = int(dur * SR)
    p = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, p)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % p]
        buf[i % p] = .5 * (buf[i % p] + buf[(i + 1) % p]) * .996
    return filt(out, "lowpass", 5000)


def strum(notes, t0, g=.5, down=True):
    for k, nn in enumerate(notes if down else notes[::-1]):
        st(t0 + k * .014, guitar(midi(nn), .9), g / len(notes) * 2.2, (k - len(notes) / 2) * .12)


def bass(freq, dur, cut=700):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return filt(np.sin(2 * np.pi * freq * t) + .35 * saw(freq, n), "lowpass", cut) * env(n, .005, .05, .85, .03)


def slap(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = saw(freq, n) * .5 + np.sin(2 * np.pi * freq * t)
    fc = 300 + 2500 * np.exp(-t * 25)
    y = np.zeros(n)
    for i in range(0, n, 1024):
        y[i:i + 1024] = filt(x[i:i + 1024], "lowpass", fc[i])
    return y * env(n, .003, .08, .7, .03)


def impact(g=1.0):
    n = int(1.6 * SR)
    t = np.arange(n) / SR
    boom = np.sin(2 * np.pi * np.cumsum(38 + 60 * np.exp(-t * 12)) / SR) * np.exp(-t * 3.5)
    return np.tanh((boom + filt(noise(n), "lowpass", 5000) * np.exp(-t * 6) * .35) * 1.4) * g


def riser(dur):
    n = int(dur * SR)
    x = noise(n)
    tt = np.linspace(0, 1, n)
    y = np.zeros(n)
    for i in range(0, n, 2048):
        y[i:i + 2048] = filt(x[i:i + 2048], "highpass", 300 + 6000 * tt[i] ** 2, 1)
    return y * tt ** 2


def reverse_cymbal(dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return (filt(noise(n), "highpass", 5000) * np.exp(-t * 3))[::-1]


def crackle(dur):
    n = int(dur * SR)
    x = np.zeros(n)
    idx = rng.integers(0, n, int(dur * 45))
    x[idx] = rng.uniform(-1, 1, len(idx))
    return filt(x, "bandpass", [1000, 6000]) * 2.5 + filt(noise(n), "lowpass", 400) * .03


def tick_tock(t0, t1, beat):
    """Horloge de l'accroche : le temps passe… sans progrès."""
    t, k = t0, 0
    while t < t1:
        st(t, rim(), .16 if k % 2 == 0 else .1, .3 if k % 2 else -.3)
        t += beat
        k += 1


# ------------------------------------------------------------------ styles
def grid(bpm, t0, t1, step):
    """Instants de la grille rythmique, calée pour que T_DROP tombe sur un temps."""
    beat = 60 / bpm
    k0 = int(np.floor((t0 - T_DROP) / (beat * step)))
    out = []
    k = k0
    while True:
        t = T_DROP + k * beat * step
        if t >= t1:
            break
        if t >= t0 - 1e-6:
            out.append((t, k))
        k += 1
    return out


def chord_at(prog, t, bar):
    return prog[int(np.floor((t - T_DROP) / bar + 1e-6)) % len(prog)]


def common_transitions(final_notes, cut=5000):
    st(T_DROP - 1.2, riser(1.2), .35)
    st(T_DROP - .9, reverse_cymbal(.9), .25)
    st(T_DROP, impact(), .55)
    st(T_SOL, impact(), .25)
    st(T_FINAL - .7, reverse_cymbal(.7), .2)
    st(T_FINAL, impact(), .7)
    for nn in final_notes:
        s = supersaw([nn], 3.4) * .9
        st(T_FINAL, filt(s, "lowpass", cut) * np.exp(-np.arange(len(s)) / SR * .8), .42)


def style1():   # électro-pop, la mineur
    bpm = 124; beat = 60 / bpm; bar = 4 * beat
    prog = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]
    tick_tock(.2, T_DROP - .3, beat)
    for t, k in grid(bpm, 0, DURATION, 4):
        root, notes = chord_at(prog, t + .01, bar)
        s = supersaw([x - 12 for x in notes] + [notes[0]], bar)
        st(t, filt(s, "lowpass", 700) if t < T_DROP else s, .35 if t < T_DROP else .5)
    for t, k in grid(bpm, T_DROP, DURATION, .5):
        root, _ = chord_at(prog, t, bar)
        st(t, bass(midi(root - 12 + (12 if k % 2 else 0)), beat / 2 * .9), .5)
    for t, k in grid(bpm, T_DROP, DURATION, .25):
        root, notes = chord_at(prog, t, bar)
        tones = notes + [notes[0] + 12]
        st(t, pluck(midi(tones[[0, 1, 2, 1, 2, 3, 2, 1][k % 8]] + (12 if t > T_SOL and (k // 8) % 2 else 0))), .12 if k % 4 == 0 else .08, .4 * np.sin(k))
    for t, k in grid(bpm, T_DROP, DURATION, 1):
        st(t, kick(), .75)
        if k % 2:
            st(t, clap(), .4)
        st(t + beat / 2, hat(True), .1, .2)
        st(t, hat(), .06, -.3)
    common_transitions([45, 57, 64, 69, 72, 76])


def style2():   # disco-funk, ré dorien
    bpm = 116; beat = 60 / bpm; bar = 4 * beat
    prog = [(50, [62, 65, 69, 72]), (55, [62, 67, 71, 65]), (50, [62, 65, 69, 72]), (57, [64, 67, 69, 73])]   # Dm7 G7 Dm7 A7
    for t, k in grid(bpm, .1, T_DROP, .5):   # basse funky étouffée
        root, _ = chord_at(prog, t, bar)
        st(t, filt(slap(midi(root - 12), beat / 2 * .7), "lowpass", 500), .3 if k % 2 == 0 else .15)
    for t, k in grid(bpm, T_DROP, DURATION, .25):
        root, notes = chord_at(prog, t, bar)
        pat = [1, 0, 1, 0, 0, 1, 1, 0, 1, 0, 0, 1, 0, 1, 1, 0]
        if pat[k % 16]:
            oct_ = 12 if k % 16 in (5, 13) else 0
            st(t, slap(midi(root - 12 + oct_), beat / 4 * 1.1), .55)
        if k % 16 in (2, 6, 10, 14):   # stabs de cuivres sur les contretemps
            st(t, supersaw(notes, beat * .3, 4500) * env(int(beat * .3 * SR), .005, .05, .6, .05), .55, .15)
        if k % 2 == 1:   # guitare « chicken scratch »
            st(t, filt(noise(int(.04 * SR)), "bandpass", [1500, 4000]) * np.exp(-np.arange(int(.04 * SR)) / SR * 80), .14, -.35)
    for t, k in grid(bpm, T_DROP, DURATION, 1):
        st(t, kick(140, 50, 11), .7)
        if k % 2:
            st(t, snare(210), .45)
        st(t + beat / 2, hat(True), .14, .25)
        st(t + beat / 4, hat(), .05)
        st(t + 3 * beat / 4, hat(), .05)
    for t, k in grid(bpm, T_SOL, DURATION, 4):   # nappe de cordes
        root, notes = chord_at(prog, t + .01, bar)
        st(t, pad([x + 12 for x in notes], bar, 3000), .18)
    common_transitions([38, 50, 57, 62, 65, 69, 72])


def longue(prog, final_notes):
    """Électro-pop de la vidéo longue (120 BPM) : intro filtrée, sidechain, basse à l'octave, arpège, montée finale."""
    bpm = 120; beat = 60 / bpm; bar = 4 * beat
    t_rise = T_FINAL - bar / 2
    # Sidechain : le kick « pompe » les accords et la basse, comme dans la vidéo longue
    pump = np.ones(N)
    seg = 1 - .75 * np.exp(-np.arange(int(beat * SR)) / SR * 11)
    for t, k in grid(bpm, T_DROP, DURATION, 1):
        i = int(t * SR); j = min(N, i + len(seg))
        pump[i:j] = np.minimum(pump[i:j], seg[: j - i])
    chords = np.zeros(N)
    bassline = np.zeros(N)
    for t, k in grid(bpm, 0, DURATION, 4):
        root, notes = chord_at(prog, t + .01, bar)
        add(chords, t, supersaw([x - 12 for x in notes] + [notes[0]], bar))
    for t, k in grid(bpm, T_DROP, DURATION, .5):   # basse en croches, octave sur les contretemps
        root, _ = chord_at(prog, t + .01, bar)
        add(bassline, t, bass(midi(root - 12 + (12 if k % 2 else 0)), beat / 2 * .9))
    # Intro : accords filtrés qui s'ouvrent peu à peu (on stagne…), puis tout s'ouvre au drop
    tt = np.arange(N) / SR
    intro = filt(chords, "lowpass", 900) * (.4 + .6 * np.clip(tt / T_DROP, 0, 1))
    mix = np.where(tt < T_DROP, intro, chords * pump)
    st(0, mix, .55, -.1)
    st(0, np.roll(mix, int(.012 * SR)), .45, .1)
    st(0, bassline * pump, .55)
    for t, k in grid(bpm, 0, T_DROP, 2):   # kick étouffé dans l'intro
        st(t, filt(kick(), "lowpass", 300), .45)
    for t, k in grid(bpm, T_DROP, DURATION, .25):   # arpège pluck, à l'octave après « la solution »
        root, notes = chord_at(prog, t + .01, bar)
        tones = notes + [notes[0] + 12]
        g = (.14 if k % 4 == 0 else .09) * (.5 if t_rise <= t < T_FINAL else 1)
        st(t, pluck(midi(tones[[0, 1, 2, 1, 2, 3, 2, 1][k % 8]] + (12 if t >= T_SOL and (k // 8) % 2 else 0))), g, .45 * np.sin(k * .9))
    for t, k in grid(bpm, T_DROP, DURATION, 1):   # batterie four-on-the-floor
        if not t_rise <= t < T_FINAL:
            st(t, kick(), .8)
            if k % 2:
                st(t, clap(), .42)
            st(t + beat / 2, hat(True), .1, .2)
        st(t, hat(), .07, -.3)
        st(t + beat / 4, hat(), .045, .3)
        st(t + beat * .75, hat(), .045, -.2)
    for i in range(16):   # roulement + montée avant l'appel final
        st(t_rise + (T_FINAL - t_rise) * i / 16, clap(), .12 + .3 * i / 16)
    st(t_rise, riser(T_FINAL - t_rise), .35)
    st(T_DROP - .45, riser(.45), .3)
    st(T_DROP, impact(), .32)
    st(T_SOL, impact(), .25)
    st(T_FINAL, impact(), .36)
    for nn in final_notes:   # accord final tenu
        s = supersaw([nn], 3.4) * .9
        st(T_FINAL, filt(s, "lowpass", 5000) * np.exp(-np.arange(len(s)) / SR * .9), .3)


def style3():   # électro-pop de la vidéo longue, ré mineur : Dm – B♭ – F – C (on stagne… puis tout s'ouvre)
    longue([(50, [62, 65, 69]), (46, [62, 65, 70]), (41, [60, 65, 69]), (48, [60, 64, 67])], (38, 50, 57, 62, 65, 69))


def style4():   # trap cinématique, do mineur
    bpm = 140; beat = 60 / bpm; bar = 4 * beat
    prog = [(48, [60, 63, 67]), (44, [60, 63, 68]), (51, [58, 63, 67]), (46, [58, 62, 65])]   # Cm Ab Eb Bb
    for t, k in grid(bpm, 0, DURATION, 4):
        root, notes = chord_at(prog, t + .01, bar)
        st(t, pad([x - 12 for x in notes] + [notes[0]], bar, 900 if t < T_DROP else 2200), .45)
    for t, k in grid(bpm, .2, T_DROP, 2):   # battement de cœur
        st(t, filt(kick(60, 40, 12), "lowpass", 200), .55)
        st(t + .22, filt(kick(60, 40, 12), "lowpass", 200), .35)
    for t, k in grid(bpm, T_DROP, DURATION, 4):
        root, _ = chord_at(prog, t + .01, bar)
        st(t, k808(midi(root - 24), bar * .55), .7)
        st(t + bar * .625, k808(midi(root - 24 + 7), bar * .3), .5)
    for t, k in grid(bpm, T_DROP, DURATION, 2):   # half-time : caisse sur le 3
        if k % 2 == 1:
            st(t, clap(), .5)
            st(t, snare(200), .35)
    for t, k in grid(bpm, T_DROP, DURATION, .25):   # charleston en rafales
        if (k // 16) % 2 == 1 and k % 16 >= 12:
            for r in range(3):
                st(t + r * beat / 12, hat(), .05)
        elif k % 2 == 0:
            st(t, hat(), .06, .2 * np.sin(k))
    for t, k in grid(bpm, T_SOL, DURATION, .5):   # cloche mélodique
        root, notes = chord_at(prog, t, bar)
        if [1, 0, 1, 1, 0, 1, 0, 0][k % 8]:
            st(t, pluck(midi(notes[k % 3] + 12), .4, 5000, 9), .12, .35)
    common_transitions([36, 48, 55, 60, 63, 67])


def style5():   # électro-pop de la vidéo longue, version lumineuse en sol majeur : G – D – Em – C
    bpm = 120; beat = 60 / bpm; bar = 4 * beat
    prog = [(43, [62, 67, 71]), (50, [62, 66, 69]), (52, [64, 67, 71]), (48, [64, 67, 72])]
    longue(prog, (43, 55, 62, 67, 71, 74))
    for t, k in grid(bpm, T_SOL, T_FINAL - bar / 2, .5):   # glockenspiel qui monte, étape par étape
        root, notes = chord_at(prog, t + .01, bar)
        st(t, marimba(midi(notes[k % 3] + 24 + (12 if k % 8 >= 6 else 0)), .5), .1, .4 * np.sin(k))


{1: style1, 2: style2, 3: style3, 4: style4, 5: style5}[STYLE]()


# ------------------------------------------------------------------ master
def room(x):
    y = x.copy()
    for d, g in ((.023, .35), (.031, .3), (.047, .25), (.089, .18), (.137, .12)):
        k = int(d * SR)
        y[k:] += x[:-k] * g
    return y


L = .8 * L + .2 * room(L)
R = .8 * R + .2 * room(R)
L, R = np.tanh(L * 1.3), np.tanh(R * 1.3)
nn = int(DURATION * SR)
L, R = L[:nn], R[:nn]
fade = np.clip((DURATION - np.arange(nn) / SR) / 1.2, 0, 1) * np.clip(np.arange(nn) / (SR * .05), 0, 1)
L, R = L * fade, R * fade
peak = max(np.abs(L).max(), np.abs(R).max())
data = (np.stack([L, R], 1) / peak * .9 * 32767).astype(np.int16)
with wave.open(OUT, "wb") as w:
    w.setnchannels(2)
    w.setsampwidth(2)
    w.setframerate(SR)
    w.writeframes(data.tobytes())
print("écrit", OUT, f"style {STYLE}")
