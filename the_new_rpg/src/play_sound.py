import math, os, wave
from math import sin
from math import pi
import numpy
import pygame, variables

# nessoundfont = "soundfonts/The_Nes_Soundfont.sf2"
max_sample = 2 ** (16 - 1) - 1

def sinesval(t, f):
    return math.sin(2 * math.pi * f * t)


def squaresval(t, frequency, squareness):
    sval = 0
    if squareness < 25:
        for x in range(squareness):
            sval += (1 / (x * 2 - 1)) * math.sin(math.pi * 2 * (2 * x - 1) * frequency * t)
    # max of 25 for "true" square wave
    elif squareness == 25:
        if (frequency * t) % 2 < 0.50000001:
            sval = 1
        else:
            sval = -1
    # muted version
    elif squareness > 25:
        sval = (frequency * t) % 2

    return sval


def trianglesval(t, f, shapefactor):
    sval = 0
    if shapefactor < 25:
        for k in range(shapefactor):
            sval += (-1 ** k) * (sin(2 * pi * (2 * k + 1) * f * t) / ((2 * k + 1) ** 2))
    else:
        p = 1 / f
        sval = (2 / p) * abs((t % p) - p / 2) - p / 4
    return sval


# shapefactor is a factor used for additive synthesis
def sawtoothsval(t, f, shapefactor):
    p = 1 / f
    sval = 0
    if shapefactor < 25:
        for a in range(shapefactor):
            k = a + 1
            sval += ((-1) ** k) * (sin(2 * pi * k * f * t) / k)
    else:
        sval = 2 * ((t / p) - ((0.5 + (t / p)) // 1))

    return sval


# min refinement of 1 which means sine wave, and bigger numbers will take longer unless it is above 25 or so
def make_wave(frequency, type, shapefactor):
    duration = (1 / frequency) * 10  # in seconds
    sample_rate = 44100

    n_samples = int(round(duration * sample_rate))

    # setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)

    for s in range(n_samples):
        t = float(s) / sample_rate  # time in seconds
        sval = 0

        if type == "sine":
            sval = sinesval(t, frequency)
        elif type == "square":
            sval = squaresval(t, frequency, shapefactor)
        elif type == "triangle":
            sval = trianglesval(t, frequency, shapefactor)
        elif type == "sawtooth":
            sval = sawtoothsval(t, frequency, shapefactor)

        # grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample * sval))  # left
        buf[s][1] = int(round(max_sample * sval))  # right

    return pygame.sndarray.make_sound(buf)


def make_soundpack(wavetype, shapefactor):
    l = []
    if os.path.exists("sounds/" + wavetype + "0.wav"):
        for x in range(37):
            l.append(pygame.mixer.Sound("sounds/" + wavetype + str(x) + ".wav"))
            l[x].set_volume(variables.battle_volume)
    else:
        try:
            os.makedirs("sounds")
        except OSError:
            pass
        for x in range(36 + 1):
            s = make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor)
            s.set_volume(variables.battle_volume)

            # save it for future loading
            sfile = wave.open("sounds/" + wavetype + str(x) + ".wav", "w")
            sfile.setframerate(22050)
            sfile.setnchannels(2)
            sfile.setsampwidth(2)
            sfile.writeframesraw(s.get_raw())
            sfile.close()

            l.append(s)
    return l


# each soundpack is a list of sounds from A3 to A6
# value of 0 corresponds to A4, -12 is A3
all_tones = {"sine": make_soundpack("sine", 1), "square": make_soundpack("square", 7),
             "squareh": make_soundpack("square", 25), "triangle": make_soundpack("triangle", 4),
             "triangleh": make_soundpack("triangle", 30), "sawtooth": make_soundpack("sawtooth", 4),
             "sawtoothh": make_soundpack("sawtooth", 30)}

# all possible soundpacks
soundpackkeys = ["sine", 'square', 'squareh', 'triangle', 'triangleh', 'sawtooth', 'sawtoothh']

Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")
Drum_kick_heavy.set_volume(variables.battle_volume * 6)


def play_tone(t):
    # add because values are centered on 0
    all_tones[variables.settings.soundpack][t + 12].play(loops=-1)


def play_sound(s):
    if s == "drum kick heavy":
        Drum_kick_heavy.play()


def stop_tone(t):
    all_tones[variables.settings.soundpack][t + 12].stop()
