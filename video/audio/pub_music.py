"""Musiques des publicités de 15 s (src/pub.html) : un style différent par question.

  1  électro-house 128 BPM, la mineur     (classement bloqué → ça décolle)
  2  funk-house 124 BPM, ré dorien        (« jouez moins, comprenez plus »)
  3  drum'n'bass liquide 174 BPM          (on stagne… puis on passe un cap)
  4  trap / phonk 150 BPM, do mineur      (« ne regardez plus, jouez ! »)
  5  pop dance 128 BPM, sol majeur        (« suivez le guide », optimiste)

Pas de mélodie aiguë : rythme, basse saturée, stabs d'accords en médium, crashs et toms.
Le rythme est là dès la première seconde, étouffé par un filtre qui s'ouvre pendant la question ;
roulement et drop sur « Nous avons la solution ! » (3,9 s), mélodie pendant la réponse, roulement et impact
sur l'appel final (11,6 s).
Usage : python3 audio/pub_music.py STYLE SORTIE.wav
"""
import sys
import wave

import numpy as np
from scipy.signal import butter, sosfilt

SR = 48000
STYLE = int(sys.argv[1])
OUT = sys.argv[2]
DURATION = 15.0
T_DROP, T_SOL, T_FINAL = 3.9, 5.4, 11.6
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


def reese(freq, dur, cut=600):
    n = int(dur * SR)
    x = saw(freq, n, rng.random()) + saw(freq * 1.006, n, rng.random()) + saw(freq * .994, n, rng.random())
    t = np.arange(n) / SR
    lfo = cut * (1 + .5 * np.sin(2 * np.pi * 1.5 * t))
    y = np.zeros(n)
    for i in range(0, n, 1024):
        y[i:i + 1024] = filt(x[i:i + 1024], "lowpass", lfo[i])
    return np.tanh(y * .9) * env(n, .005, .05, 1, .05)


def cowbell(freq, dur=.25):
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = np.sign(np.sin(2 * np.pi * freq * t)) + np.sign(np.sin(2 * np.pi * freq * 1.48 * t))
    return filt(x, "bandpass", [500, 4000]) * np.exp(-t * 12) * .5


def lead(freq, dur):
    n = int(dur * SR)
    t = np.arange(n) / SR
    vib = 1 + .004 * np.sin(2 * np.pi * 5.5 * t) * np.clip(t * 4, 0, 1)
    ph = np.cumsum(freq * vib) / SR
    x = sum((2 * ((ph * (1 + d) + r) % 1) - 1) for d, r in ((-.004, .1), (0, .5), (.004, .8)))
    return filt(x / 3, "lowpass", 4500) * env(n, .008, .08, .75, .06)


def drums_house(bpm, t0, t1, clap_g=.45, hat16=True):
    beat = 60 / bpm
    for t, k in grid(bpm, t0, t1, .25):
        if k % 4 == 0:
            st(t, kick(), .85)
        if k % 8 == 4:
            st(t, clap(), clap_g)
        if k % 4 == 2:
            st(t, hat(True), .13, .2)
        if hat16:
            st(t, hat(), .06 if k % 2 else .035, -.25 if k % 2 else .25)


def roll(bpm, t_end, beats=4, g=.35):
    """Roulement de caisse claire qui accélère jusqu'à t_end."""
    beat = 60 / bpm
    t = t_end - beats * beat
    k = 0
    while t < t_end - 1e-3:
        frac = 1 - (t_end - t) / (beats * beat)
        step = beat / 2 if frac < .5 else beat / 4 if frac < .8 else beat / 8
        st(t, snare(200 + 200 * frac), g * (.4 + .6 * frac), .15 * np.sin(k))
        t += step
        k += 1


def pump_bus(x, bpm, t0):
    """Effet « pompe » du sidechain sur un bus mélodique."""
    beat = 60 / bpm
    t = np.arange(len(x)) / SR
    ph = ((t - t0) % beat) / beat
    return x * (1 - .7 * np.exp(-ph * 9))


def melody(bpm, t0, t1, notes, rhythm, voice, g, pan=.0):
    """notes : hauteurs MIDI ; rhythm : durées en temps (cycliques). Coupé : les sons aigus gênaient."""
    return
    beat = 60 / bpm
    t, k = t0, 0
    while t < t1 - .05:
        d = rhythm[k % len(rhythm)] * beat
        nn = notes[k % len(notes)]
        if nn is not None:
            st(t, voice(midi(nn), d * .95), g, pan)
        t += d
        k += 1


def filtered_intro():
    """Tout ce qui précède le drop passe dans un passe-bas qui s'ouvre (300 → 2500 Hz)."""
    global L, R
    n = int(T_DROP * SR)
    for buf in (L, R):
        zi = None
        out = np.zeros(n)
        for i in range(0, n, 512):
            fc = 300 * (2500 / 300) ** ((i / n) ** 1.6)
            sos = butter(2, fc, "lowpass", fs=SR, output="sos")
            if zi is None:
                zi = np.zeros((sos.shape[0], 2))
            j = min(n, i + 512)
            out[i:j], zi = sosfilt(sos, buf[i:j], zi=zi)
        buf[:n] = out * .7


def crash(dur=1.6):
    n = int(dur * SR)
    t = np.arange(n) / SR
    return filt(noise(n), "highpass", 4000) * np.exp(-t * 2.8) * .6


def tom(freq):
    n = int(.3 * SR)
    t = np.arange(n) / SR
    return np.sin(2 * np.pi * np.cumsum(freq * (1 + .6 * np.exp(-t * 25))) / SR) * np.exp(-t * 11)


def energie(bpm, prog, low=-12):
    """Couche « pub » : crash à chaque mesure, stabs d'accords en médium qui pompent,
    basse saturée, claps doublés et roulements de toms avant les changements."""
    beat = 60 / bpm; bar = 4 * beat
    for t, k in grid(bpm, T_DROP, DURATION, 4):
        st(t, crash(), .22, .2 * (-1) ** k)
    stabs = np.zeros(N)
    for t, k in grid(bpm, T_DROP, T_FINAL + bar, .5):
        root, notes = chord_at(prog, t, bar)
        mid = sorted(((x - 60) % 12) + 55 for x in notes)[:4]
        if k % 8 in (0, 3, 6):
            add(stabs, t, supersaw(mid, beat * .4, 2400), .6)
    stabs = pump_bus(stabs, bpm, T_DROP)
    st(0, stabs, .7, -.15); st(.009, stabs, .55, .15)
    for t, k in grid(bpm, T_DROP, DURATION, 1):
        root, _ = chord_at(prog, t, bar)
        x = bass(midi(root + low), beat * .9, 1500)
        st(t, np.tanh(x * 3) * .5, .4)
        if k % 2:
            st(t + .012, clap(), .25, .3)
    for t_end in (T_DROP, T_SOL, T_FINAL):
        for i, f in enumerate((220, 180, 150, 120)):
            st(t_end - (4 - i) * beat / 4, tom(f), .35, .3 - .2 * i)


def common_transitions(bpm, final_notes, cut=5000):
    roll(bpm, T_DROP, 4, .4)
    st(T_DROP - 1.4, riser(1.4), .45)
    st(T_DROP, impact(), .7)
    st(T_SOL - .35, whoosh_(.35), .4)
    roll(bpm, T_FINAL, 2, .3)
    st(T_FINAL - .7, reverse_cymbal(.7), .3)
    st(T_FINAL, impact(), .7)
    for nn in final_notes:
        s = supersaw([nn], 3.4) * .9
        st(T_FINAL, filt(s, "lowpass", cut) * np.exp(-np.arange(len(s)) / SR * .8), .35)


def whoosh_(dur):
    n = int(dur * SR)
    tt = np.linspace(0, 1, n)
    y = np.zeros(n)
    x = noise(n)
    for i in range(0, n, 2048):
        fc = 500 + 7000 * tt[i] ** 2
        y[i:i + 2048] = filt(x[i:i + 2048], "bandpass", [fc * .6, min(fc * 1.6, 20000)], 1)
    return y * tt ** 2


def style1():   # électro-house 128 BPM, la mineur
    bpm = 128; beat = 60 / bpm; bar = 4 * beat
    prog = [(57, [69, 72, 76]), (53, [65, 69, 72]), (48, [67, 72, 76]), (55, [67, 71, 74])]
    drums_house(bpm, 0, DURATION)
    chords = np.zeros(N)
    for t, k in grid(bpm, 0, DURATION, .5):   # stabs sur les contretemps
        if k % 2:
            root, notes = chord_at(prog, t, bar)
            s = supersaw([x - 12 for x in notes] + notes, beat * .45, 4200)
            add(chords, t, s, .5)
    chords = pump_bus(chords, bpm, T_DROP)
    st(0, chords, .9, -.1); st(.011, chords, .7, .1)
    for t, k in grid(bpm, 0, DURATION, .5):   # basse house en contretemps
        root, _ = chord_at(prog, t, bar)
        if k % 2:
            st(t, bass(midi(root - 12), beat * .45, 900), .65)
    for t, k in grid(bpm, 0, DURATION, .25):
        root, notes = chord_at(prog, t, bar)
        tones = notes + [notes[0] + 12]
        st(t, pluck(midi(tones[[0, 2, 1, 3, 2, 1, 3, 2][k % 8]] - 12), .2, 1200), .05, .4 * np.sin(k))
    melody(bpm, T_SOL, T_FINAL, [81, 79, 76, 76, 77, 76, 72, 74, 76, None, 81, 83, 84, 83, 79, None],
           [.5, .5, 1, .5, .5, .5, .5, 1, 1, 1, .5, .5, 1, .5, .5, 1], lead, .22, .1)
    energie(bpm, prog)
    filtered_intro()
    common_transitions(bpm, [45, 57, 64, 69, 72, 76])


def style2():   # funk-house 124 BPM, ré dorien
    bpm = 124; beat = 60 / bpm; bar = 4 * beat
    prog = [(50, [62, 65, 69, 72]), (55, [62, 67, 71, 65]), (50, [62, 65, 69, 72]), (57, [64, 67, 69, 73])]
    drums_house(bpm, 0, DURATION, .5)
    for t, k in grid(bpm, 0, DURATION, .25):
        root, notes = chord_at(prog, t, bar)
        if [1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0, 1][k % 16]:
            oct_ = 12 if k % 16 in (3, 6, 11, 15) else 0
            st(t, slap(midi(root - 12 + oct_), beat / 4 * 1.1), .6)
        if k % 16 in (2, 6, 10, 13):
            st(t, supersaw(notes, beat * .28, 5000) * env(int(beat * .28 * SR), .004, .05, .6, .05), .6, .15)
        if k % 2 == 1:
            m = int(.04 * SR)
            st(t, filt(noise(m), "bandpass", [1500, 4000]) * np.exp(-np.arange(m) / SR * 80), .2, -.35)
    melody(bpm, T_SOL, T_FINAL, [74, 77, 79, 81, 79, 77, 74, None, 72, 74, 77, 74, None, 81, 79, 77],
           [.5, .5, .5, 1, .5, .5, .5, .5, .5, .5, .5, 1, .5, .5, .5, 1], lambda f, d: pluck(f, max(d, .2), 4000, 6), .3, -.15)
    for t, k in grid(bpm, T_SOL, DURATION, 4):
        root, notes = chord_at(prog, t + .01, bar)
        st(t, pad([x + 12 for x in notes], bar, 3500), .2)
    energie(bpm, prog)
    filtered_intro()
    common_transitions(bpm, [38, 50, 57, 62, 65, 69, 72])


def style3():   # drum'n'bass liquide 174 BPM
    bpm = 174; beat = 60 / bpm; bar = 4 * beat
    prog = [(53, [64, 69, 72, 76]), (52, [62, 67, 71, 74]), (50, [60, 65, 69, 72]), (48, [64, 67, 71, 74])]
    for t, k in grid(bpm, 0, DURATION, .25):   # breakbeat : kick 1 et 2.5, caisse 2 et 4
        kk = k % 16
        if kk in (0, 10):
            st(t, kick(150, 52, 12), .85)
        if kk in (4, 12):
            st(t, snare(230), .6)
            st(t, clap(), .25)
        if kk in (7, 15):
            st(t, snare(260), .12)
        st(t, hat(), .055 if k % 2 else .03, .25 * np.sin(k))
        if kk in (2, 14):
            st(t, hat(True), .08, .3)
    for t, k in grid(bpm, 0, DURATION, 4):
        root, notes = chord_at(prog, t + .01, bar)
        st(t, reese(midi(root - 24), bar * .98), .45)
        st(t, rhodes(notes, bar), .35)
        st(t, pad([x + 12 for x in notes], bar, 2500), .14)
    melody(bpm, T_SOL, T_FINAL, [76, 79, 81, 84, 81, 79, 76, 74, 72, 74, 76, 79],
           [1, 1, 1, 1.5, .5, 1, 1, 1, 1, 1, 1, 2], lambda f, d: marimba(f, max(d, .4)), .28, .25)
    energie(bpm, prog)
    filtered_intro()
    common_transitions(bpm, [41, 53, 64, 69, 72, 76])


def style4():   # trap / phonk 150 BPM, do mineur
    bpm = 150; beat = 60 / bpm; bar = 4 * beat
    prog = [(48, [60, 63, 67]), (44, [60, 63, 68]), (51, [58, 63, 67]), (46, [58, 62, 65])]
    for t, k in grid(bpm, 0, DURATION, .25):
        kk = k % 16
        root, notes = chord_at(prog, t, bar)
        if kk in (0, 3, 6, 10, 11):
            st(t, k808(midi(root - 24 + (12 if kk == 11 else 0)), beat * (.7 if kk in (0, 6) else .4)), .65)
            st(t, kick(180, 50, 14), .5)
        if kk in (4, 12):
            st(t, clap(), .55); st(t, snare(210), .3)
        if (k // 16) % 2 == 1 and kk >= 12:
            for r in range(2):
                st(t + r * beat / 8, hat(), .06)
        else:
            st(t, hat(), .07 if k % 2 == 0 else .04, .2 * np.sin(k))
        if [1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 0][kk]:   # cloche « phonk »
            st(t, cowbell(midi(notes[(k // 3) % 3] - 12)), .12, .3)
    for t, k in grid(bpm, 0, DURATION, 4):
        root, notes = chord_at(prog, t + .01, bar)
        st(t, pad([x - 12 for x in notes] + [notes[0]], bar, 2200), .3)
    melody(bpm, T_SOL, T_FINAL, [72, 75, 79, 77, 75, 74, 75, None, 72, 79, 80, 79, 75, 77, 74, None],
           [.5, .5, 1, .5, .5, .5, 1, .5, .5, .5, .5, 1, .5, .5, 1, .5], lead, .2, -.1)
    energie(bpm, prog)
    filtered_intro()
    common_transitions(bpm, [36, 48, 55, 60, 63, 67])


def style5():   # pop dance 128 BPM, sol majeur
    bpm = 128; beat = 60 / bpm; bar = 4 * beat
    prog = [(55, [55, 59, 62, 67, 71]), (52, [52, 59, 64, 67, 71]), (48, [48, 55, 60, 64, 67]), (50, [50, 57, 62, 66, 69])]
    drums_house(bpm, 0, DURATION, .5, hat16=False)
    for t, k in grid(bpm, 0, DURATION, .25):
        root, notes = chord_at(prog, t + .01, bar)
        if k % 8 in (0, 2, 3, 5, 6):
            strum(notes, t, .42 if k % 8 == 0 else .3, down=k % 2 == 0)
        st(t, shaker(), .11 if k % 2 else .06)
        if k % 2 == 0:
            st(t, bass(midi(root - 12 + (12 if k % 4 == 2 else 0)), beat / 2 * .9, 800), .55)
    melody(bpm, T_SOL, T_FINAL, [79, 83, 86, 83, 81, 79, 76, 79, 81, 83, 81, 79, 78, 79, 83, 86],
           [.5] * 16, lambda f, d: marimba(f, .5), .26, .3)
    melody(bpm, T_SOL, T_FINAL, [67, None, 71, None, 72, None, 74, None], [1] * 8, lambda f, d: pluck(f, .4, 3500, 8), .14, -.3)
    energie(bpm, prog)
    filtered_intro()
    common_transitions(bpm, [43, 55, 62, 67, 71, 74])

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
