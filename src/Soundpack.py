import pygame, os, wave, math, numpy, variables
from math import sin
from math import pi
import random
from FrozenClass import FrozenClass

max_sample = 2 ** (16 - 1) - 1
sample_rate = 22050

# volume envelopes are lists of times and what volume it should be at that time
volumeenvelopes = {"bell" : VolumeEnvelope([[0, 0.05], [200, 1], [800, 0.3]], 600, 0.1),
                   "flat" : VolumeEnvelope([[0, 0.5]], 300, 0.2)}

class Soundpack(FrozenClass):
    

    def __init__(self, wavetype, shapefactor, resetq=False):
        # list of buffers for different frequencies of notes
        # each buffer is a perfectly loopable sample of the wave, normalized
        self.loopbuffers = []
        self.tempbuffers = []

        # how long in milliseconds the sound from each loopbuffer is
        self.loopbufferdurationmillis = []
        
        # finally, generate all the loopbuffers
        self.make_soundpack(wavetype, shapefactor, resetq)

        
        self._freeze()

    # durationplayed is in milliseconds
    def tone_volume(self, durationplayed, volumeenvelopename):
        volen = volumeenvelopes[volumeenvelopename]
        volumelist = volumeenvelopes[volumeenvelopename].timevollist
        listplace = 0
        while True:
            if listplace + 1 >= len(volumelist):
                break
            elif durationplayed >= volumelist[listplace + 1][0]:
                listplace += 1
            else:
                break

        dt = durationplayed - volumelist[listplace][0]
        if listplace == len(volumelist)-1:
            volume = volumelist[listplace][1]
            timesinceend = durationplayed-volumelist[-1][0]
            volume = volume + math.sin(2*math.pi*timesinceend/volen.endoscilationrate)*volen.endoscilationvolume
        else:
            timebetween = (volumelist[listplace+1][0]-volumelist[listplace][0])
            ydifference = (volumelist[listplace+1][1]-volumelist[listplace][1])
            initial = volumelist[listplace][1]
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

    def randomicefunction(self):
        # how wound up the wave is
        dinterval = random.uniform(1, 4)
        # how dramatic the humps are, sharpness
        cpower = random.uniform(0.7, 1.5)
        # shifts humps in wave
        bshift = random.uniform(0, 2*math.pi)
        
        def sfunction(t, f, shapefactor):
            sval = 0

            for n in range(shapefactor):
                thissum = (dinterval*n + 1)
                coeff = math.pow(-1, n) / math.pow(thissum, cpower)
                sval += math.sin(2 * pi * f * t * thissum + bshift*n)*coeff
            return sval

        return sfunction

    def chooserandfunction(self):
        return random.choice([self.randomicefunction(), self.sawtoothsval, self.squaresval, self.trianglesval])
    
    # combine square, triangle, saw with different weights
    def newrandomwavefunction(self):
        rfunction = self.chooserandfunction()
        rfunction2 = self.chooserandfunction()
        rfunction3 = self.chooserandfunction()
        def sfunction(t, f, shapefactor):
            # add harmonics
            return rfunction(t,f,shapefactor) + (1/4)*rfunction2(2*t, f, shapefactor) + (1/8)*rfunction3(4*t, f, shapefactor)
        return sfunction

    # min refinement of 1 which means sine wave, and bigger numbers will take longer unless it is above 25 or so
    def make_wave(self, frequency, wavetype, shapefactor):
        loopduration = (1 / frequency) * 50  # in seconds
        duration = loopduration

        n_samples = int(round(duration * sample_rate))

        # setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits"
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int16)

        randfunction = None
        if wavetype == "random":
            randfunction = self.newrandomwavefunction()

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
            elif wavetype == "random":
                sval = randfunction(t, frequency, shapefactor)
            else:
                raise Exception("unknown wavetype " + wavetype)

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
            sval = (get_sval(t) / normalizevalue)
            buf[s][0] = sval # left
            buf[s][1] = sval # right

        return (buf, duration)

    def make_soundpack(self, wavetype, shapefactor, resetq):
        for x in range(37):
            loopbuf = self.make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor)
            
            self.loopbuffers.append(loopbuf[0])
            self.tempbuffers.append(numpy.zeros((int(loopbuf[0].size/2), 2), dtype=numpy.int16))
            self.loopbufferdurationmillis.append(loopbuf[1]*1000)


    # get the buffer with the volume envelope applied at time in milliseconds
    # index is which loopbuffer for the frequency to play
    # time is time in milliseconds since start of the note played
    def getbufferattime(self, index, time):
        obuf = self.loopbuffers[index]
        #buf = self.tempbuffers[index]
        #for i in range(int(obuf.size/2)):
        #    obuf[i][0] = buf[i][0]*0.5
        #    obuf[i][1] = buf[i][1]*0.5
        return obuf
