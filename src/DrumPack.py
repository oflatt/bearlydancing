import pygame, numpy, random, math

from FrozenClass import FrozenClass
from wavefunctions import make_wave
from volumebuffers import volbuffers, volumeenvelopes

def changingnoisefunction(t, sval):
    if t % 2 < 1:
        return sval
    else:
        return multiplynoisefunction(t, sval)

def additivenoisefunction(t, sval):
    noiselevel = 0.5
    return sval + numpy.random.normal(0, noiselevel)


def multiplynoisefunction(t, sval):
    noiselevel = 0.2
    sval = sval*numpy.random.normal(0.5, noiselevel)
    if random.random()<0.5:
        return -sval
    else:
        return sval

def wavenoisefunction(t, sval):
    wave = math.sin(2*math.pi * 440 * t)
    sval = sval * numpy.random.normal(0.5, 0.1)

    if random.random() < abs(wave)/2:
        return -sval*0.5
    else:
        return sval

class DrumPack(FrozenClass):

    def __init__(self, wavetype, shapefactor, volumeenvelopename, lowerfrequency, heigherfrequency, duration=None):
        # list of sounds with different frequencies used to generate them
        self.sounds = []

        self.make_soundpack(wavetype, shapefactor, volumeenvelopename, lowerfrequency, heigherfrequency, duration)

        self._freeze()

    def make_soundpack(self, wavetype, shapefactor, volumeenvelopename, low, high, duration):
        # generate only 8 notes
        moveby = int((high - low)/8)
        
        for i in range(8):
            x = i * moveby
            frequency = (440 * ((2 ** (1 / 12)) ** (x - 12 + low)))
            sampledur = duration
            if sampledur == None:
                sampledur = (1/440)*20
            sampledur = sampledur - sampledur%(1/frequency)
            loopbuf = make_wave(frequency, wavetype, shapefactor, sampleduration = sampledur)[0]

            volbuf = volbuffers[volumeenvelopename]

            buf = numpy.empty(loopbuf.shape, dtype=numpy.int16)
            volbuf = volbuf[0:loopbuf.shape[0]]

            numpy.multiply(volbuf, loopbuf, out=buf, casting='unsafe')
            sound = pygame.sndarray.make_sound(buf)
            self.sounds.append(sound)

    # a number from 0 to 7
    def getsound(self, index):
        return self.sounds[index]
