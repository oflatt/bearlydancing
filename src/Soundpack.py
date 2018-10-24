import pygame, os, wave, math, numpy, variables
from math import sin
from math import pi
from FrozenClass import FrozenClass

max_sample = 2 ** (16 - 1) - 1
bellvolume = [[0, 0], [100, 1], [600, 0.15]]
sample_rate = 44100

class Soundpack(FrozenClass):
    

    def __init__(self, wavetype, shapefactor, resetq=False):
        # list of buffers for different frequencies of notes
        # each buffer is a perfectly loopable sample of the wave, normalized
        self.loopbuffers = []

        # how long in milliseconds the sound from each loopbuffer is
        self.loopbufferdurationmillis = []
        # this volume envelope to use
        self.volumelist = bellvolume
        # finally, generate all the loopbuffers
        self.make_soundpack(wavetype, shapefactor, resetq)

        
        self._freeze()

    # durationplayed is in milliseconds
    def tone_volume(self, durationplayed):
        listplace = 0
        while True:
            if listplace + 1 >= len(self.volumelist):
                break
            elif durationplayed >= self.volumelist[listplace + 1][0]:
                listplace += 1
            else:
                break

        dt = durationplayed - self.volumelist[listplace][0]
        if listplace == len(self.volumelist)-1:
            volume = self.volumelist[listplace][1]
        else:
            timebetween = (self.volumelist[listplace+1][0]-self.volumelist[listplace][0])
            ydifference = (self.volumelist[listplace+1][1]-self.volumelist[listplace][1])
            initial = self.volumelist[listplace][1]
            volume = initial + ydifference * (dt/timebetween)

        return volume

    def sinesval(self, t, f):
        wave = math.sin(2 * math.pi * f * t)
        harmonic1 = (1 / 4) * math.sin(4 * math.pi * f * t)
        harmonic2 = (1 / 8) * math.sin(8 * math.pi * f * t)
        s = wave + harmonic1 + harmonic2
        return s

    def squaresval(self, t, frequency, squareness):
        sval = 0
        if squareness < 25:
            for x in range(squareness):
                sval += (1 / (x * 2 - 1)) * math.sin(math.pi * 2 * (2 * x - 1) * frequency * t)
        # max of 25 for "true" square wave
        elif squareness == 25:
            if (frequency * t) % 1 < 0.5:
                sval = 1
            else:
                sval = -1
        # muted version
        elif squareness > 25:
            sval = (frequency * t) % 2

        return sval

    def trianglesval(self, t, f, shapefactor):
        sval = 0
        if shapefactor < 25:
            for k in range(shapefactor):
                sval += (-1 ** k) * (sin(2 * pi * (2 * k + 1) * f * t) / ((2 * k + 1) ** 2))
        else:
            p = 1 / f
            sval = (2 / p) * 2* (abs((t % p) - p / 2) - p / 4)
        return sval

    # shapefactor is a factor used for additive synthesis
    def sawtoothsval(self, t, f, shapefactor):
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
    def make_wave(self, frequency, wavetype, shapefactor):
        loopduration = (1 / frequency) * 50  # in seconds
        duration = loopduration

        n_samples = int(round(duration * sample_rate))

        # setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits"
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)

        def get_sval(t):
            sval = 0

            if wavetype == "sine":
                sval = self.sinesval(t, frequency)
            elif wavetype == "square":
                sval = self.squaresval(t, frequency, shapefactor)
            elif wavetype == "triangle":
                sval = self.trianglesval(t, frequency, shapefactor)
            elif wavetype == "sawtooth":
                sval = self.sawtoothsval(t, frequency, shapefactor)

            return int(round(max_sample * sval))

        # find the maximum value to use to normalize it (make the max volume 1)
        normalizevalue = 1
        for s in range(int(round((1/frequency)*2*sample_rate))):
            t = float(s)/sample_rate
            sval = get_sval(t)
            if sval/max_sample > normalizevalue:
                normalizevalue = sval/max_sample

        for s in range(n_samples):
            t = float(s) / sample_rate  # time in seconds
            volume = self.volumelist[-1][1]
            sval = (get_sval(t) / normalizevalue) * volume 
            buf[s][0] = sval # left
            buf[s][1] = sval # right

        return (buf, duration)

    def make_soundpack(self, wavetype, shapefactor, resetq):
        for x in range(37):
            loopbuf = self.make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor)
            
            self.loopbuffers.append(loopbuf[0])
            self.loopbufferdurationmillis.append(loopbuf[1]*1000)


    # get the buffer with the volume envelope applied at time in milliseconds
    # index is which loopbuffer for the frequency to play
    # time is time in milliseconds since start of the note played
    def getbufferattime(self, index, time):
        return self.loopbuffers[index]
