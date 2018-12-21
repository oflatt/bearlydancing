import pygame, numpy


from wavefunctions import make_wave, savesoundtofile
from volumebuffers import volbuffers


for x in range(37):
    frequency = (440 * ((2 ** (1 / 12)) ** (x - 12)))
    loopbuf = make_wave(frequency, "sine", 1, addnoisep=True, sampleduration = (1/frequency) * 20)[0]

    volbuf = volbuffers["sharp"]

    buf = numpy.empty(loopbuf.shape, dtype=numpy.int16)
    volbuf = volbuf[0:loopbuf.shape[0]]

    numpy.multiply(volbuf, loopbuf, out=buf, casting='unsafe')
    sound = pygame.sndarray.make_sound(buf)

    savesoundtofile("drum_" + str(x), sound)
