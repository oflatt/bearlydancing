import pygame, numpy


from wavefunctions import make_wave, savesoundtofile
from volumebuffers import volbuffers


# key 50 is a4
for x in range(88):
    frequency = (440 * ((2 ** (1 / 12)) ** (x - 49)))
    # shape factor doesn't matter
    loopbuf = make_wave(frequency, "sine", 1, sampleduration = (1/frequency) * 500)[0]

    volbuf = volbuffers["flat"]

    buf = numpy.empty(loopbuf.shape, dtype=numpy.int16)
    volbuf = volbuf[0:loopbuf.shape[0]]

    #numpy.multiply(volbuf, loopbuf, out=buf, casting='unsafe')
    sound = pygame.sndarray.make_sound(loopbuf)

    savesoundtofile("sine_" + str(int(frequency)), sound)
