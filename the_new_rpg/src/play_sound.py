import math
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
    if shapefactor<25:
        for a in range(shapefactor):
            k = a+1
            sval += ((-1)**k) * (sin(2*pi*k*f*t)/k)
    else:
        sval = 2 * ((t/p) - ((0.5 + (t/p))//1))

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


# a list of sounds from A3 to A6
# value of 0 corresponds to A4
# -12 is A3, then
all_tones = []
for x in range(36 + 1):
    s = make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), "sawtooth", 6)
    s.set_volume(variables.battle_volume)
    all_tones.append(s)

Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")
Drum_kick_heavy.set_volume(variables.battle_volume * 6)


def play_tone(t):
    # add because values are centered on 0
    all_tones[t + 12].play(loops=-1)


def play_sound(s):
    if s == "drum kick heavy":
        Drum_kick_heavy.play()


def stop_tone(t):
    all_tones[t + 12].stop()

# def speedx(snd_array, factor):
#     """ Speeds up / slows down a sound, by some factor. """
#     indices = np.round(np.arange(0, len(snd_array), factor))
#     indices = indices[indices < len(snd_array)].astype(int)
#     return snd_array[indices]
#
#
# def stretch(snd_array, factor, window_size, h):
#     """ Stretches/shortens a sound, by some factor. """
#     phase = np.zeros(window_size)
#     hanning_window = np.hanning(window_size)
#     result = np.zeros(len(snd_array) / factor + window_size)
#
#     for i in np.arange(0, len(snd_array) - (window_size + h), h*factor):
#         # Two potentially overlapping subarrays
#         a1 = snd_array[i: i + window_size]
#         a2 = snd_array[i + h: i + window_size + h]
#
#         # The spectra of these arrays
#         s1 = np.fft.fft(hanning_window * a1)
#         s2 = np.fft.fft(hanning_window * a2)
#
#         # Rephase all frequencies
#         phase = (phase + np.angle(s2/s1)) % 2*np.pi
#
#         a2_rephased = np.fft.ifft(np.abs(s2)*np.exp(1j*phase))
#         i2 = int(i/factor)
#         result[i2: i2 + window_size] += hanning_window*a2_rephased.real
#
#     # normalize (16bit)
#     result = ((2**(16-4)) * result/result.max())
#
#     return result.astype('int16')
#
#
# def pitchshift(snd_array, n, window_size=2**13, h=2**11):
#     """ Changes the pitch of a sound by ``n`` semitones. """
#     factor = 2**(1.0 * n / 12.0)
#     stretched = stretch(snd_array, 1.0/factor, window_size, h)
#     return speedx(stretched[window_size:], factor)
#
# def makesounds(soundfont, instumentnum):
#     global all_tones
#     all_tones = []
#     opensf = open(soundfont, "rb")
#     sf = Sf2File(opensf)
#     newpath = os.path.basename(soundfont) + "export"
#     sample = sf.samples[instumentnum]
#     sample.export(newpath)
#     opensf.close()
#
#     #cut the wav down to the looping size
#     win = wave.open(newpath, 'rb')
#     offset = 1000
#     s0, s1 = offset, offset+sample.end-sample.start #start and end of where to chop the wav file
#     win.readframes(s0)  # discard
#     frames = win.readframes(s1-s0)
#     params = win.getparams()
#     win.close()
#     os.remove(newpath) #get rid of the old file
#     wout = wave.open(newpath, 'wb')
#     wout.setparams(params)
#     wout.writeframes(frames)
#     wout.close()
#     all_tones.append(pygame.mixer.Sound(newpath))
#
#     # for x in range(36):
#     #     all_tones.append(pygame.mixer.Sound(newpath))
#
#     for x in range(36):
#         fps, array = wavfile.read(newpath)
#         transposed = pitchshift(array, x-12)
#         all_tones.append(pygame.mixer.Sound(transposed))
