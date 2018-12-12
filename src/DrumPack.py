import pygame, numpy

from FrozenClass import FrozenClass
from wavefunctions import make_wave
from volumebuffers import volbuffers, volumeenvelopes

class DrumPack(FrozenClass):

    def __init__(self, wavetype, shapefactor):
        # list of sounds with different frequencies used to generate them
        self.sounds = []

        self.make_soundpack(wavetype, shapefactor)

        self._freeze()

    def make_soundpack(self, wavetype, shapefactor):
        # generate every fifth note
        for i in range(int(37/5)):
            x = i * 5
            frequency = (440 * ((2 ** (1 / 12)) ** (x - 12)))
            loopbuf = make_wave(frequency, wavetype, shapefactor, addnoisep=True, sampleduration = (1/frequency) * 20)[0]

            volbuf = volbuffers["sharp"]

            buf = numpy.empty(loopbuf.shape, dtype=numpy.int16)
            volbuf = volbuf[0:loopbuf.shape[0]]

            numpy.multiply(volbuf, loopbuf, out=buf, casting='unsafe')
            sound = pygame.sndarray.make_sound(buf)
            self.sounds.append(sound)

    def getsound(self, index):
        i = int(index/5)
        return self.sounds[i]
