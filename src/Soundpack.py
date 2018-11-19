import pygame, os, wave, math, numpy, variables, copy
from math import sin
from math import pi
import random
from FrozenClass import FrozenClass
from VolumeEnvelope import VolumeEnvelope
from variables import sample_rate

max_sample = 2 ** (16 - 1) - 1

defaultvol = 0.5

# volume envelopes are lists of times and what volume it should be at that time
volumeenvelopes = {"bell" : VolumeEnvelope([[0, 0.05], [200, 1], [800, 0.3]], 200, 0.05),
                   "flat" : VolumeEnvelope([[0, defaultvol]], 1000, 0.1)}

# volbuffers are a pair containing the volume buffer of the beginning of the volume envelope and the volume buffer for the looped section
# each buffer is a 1d numpy array with float16
volbuffers = {}

for k in volumeenvelopes:
    envelope = volumeenvelopes[k]
    n_samples = int(round(envelope.timevollist[-1][0]*sample_rate/1000))
    firstbuf = numpy.zeros(n_samples, dtype=numpy.float16)
    for s in range(n_samples):
        t = float(s)/sample_rate
        firstbuf[s] = envelope.tone_volume(t*1000)

    n_samples2 = int(round(envelope.endoscilationrate/1000*sample_rate))
    secondbuf = numpy.zeros(n_samples2, dtype=numpy.float16)
    for s in range(n_samples2):
        t = float(s+n_samples)/sample_rate
        secondbuf[s] = envelope.tone_volume(t*1000)
        
    volbuffers[k] = (firstbuf, secondbuf)

    
class Soundpack(FrozenClass):
    

    def __init__(self, wavetype, shapefactor, resetq=False):
        # list of buffers for different frequencies of notes
        # each buffer is a perfectly loopable sample of the wave, normalized
        # one dimensional array
        self.loopbuffers = []

        # have the first ones precomputed for startup time
        # a dictionary of volenvelopes as keys and lists of 2d buffers as values
        self.firstbuffers = {}
        self.secondbuffers = {}

        # buffers to fill and pass along, 2d arrays
        self.tempbuffers = []

        # buffer to return when there are too many playing
        self.defaultbuffers = []
        
        # how long in milliseconds the sound from each loopbuffer is
        self.loopbufferdurationmillis = []
        
        # finally, generate all the loopbuffers
        self.make_soundpack(wavetype, shapefactor, resetq)
        
        self._freeze()


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
        buf = numpy.zeros(n_samples, dtype=numpy.int16)

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
            buf[s] = sval

        return (buf, duration)

    def make_soundpack(self, wavetype, shapefactor, resetq):
        for x in range(37):
            loopbuf = self.make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor)
            
            self.loopbuffers.append(loopbuf[0])

            defaultbuf = numpy.zeros((int(loopbuf[0].size), 2), dtype=numpy.int16)
            for i in range(loopbuf[0].size):
                defaultbuf[i][0] = loopbuf[0][i]*defaultvol
                defaultbuf[i][1] = defaultbuf[i][0]

            self.defaultbuffers.append(defaultbuf)
            
            self.tempbuffers.append(numpy.zeros((int(loopbuf[0].size), 2), dtype=numpy.int16))
            self.loopbufferdurationmillis.append(loopbuf[1]*1000)

            # add all the first buffers
            for k in volumeenvelopes:
                if not k in self.firstbuffers:
                    self.firstbuffers[k] = []
                    self.secondbuffers[k] = []
                    
                firstbuf = self.getbufferattime(x, 0, k, True)
                secondbuf = self.getbufferattime(x, self.loopbufferdurationmillis[x], k, True)
                self.firstbuffers[k].append(copy.deepcopy(firstbuf))
                self.secondbuffers[k].append(copy.deepcopy(secondbuf))


    # get the buffer with the volume envelope applied at time in milliseconds
    # index is which loopbuffer for the frequency to play
    # time is time in milliseconds since start of the note played
    def getbufferattime(self, index, time, volenvelope, applyvolenvelopep):
        
        if not applyvolenvelopep:
            # if we don't apply the envelope, just return the default
            return self.defaultbuffers[index]
    
        if time == 0 and len(self.firstbuffers[volenvelope])>index:
            return self.firstbuffers[volenvelope][index]
        elif time < self.loopbufferdurationmillis[index]+1 and len(self.secondbuffers[volenvelope])>index:
            return self.secondbuffers[volenvelope][index]
        
        obuf = self.loopbuffers[index]
        buf = self.tempbuffers[index]

        timeindex = int(time/1000 * sample_rate)
        voltuple = volbuffers[volenvelope]
        volbuf1 = voltuple[0]
        volbuf2 = voltuple[1]

        # use the first buffer until you get to the second
        i = 0
        buf1top = min(volbuf1.size - timeindex, obuf.size)
        while i < buf1top:
            buf[i][0] = obuf[i]*volbuf1[i+timeindex]
            buf[i][1] = buf[i][0]
            i += 1

        top2 = obuf.size
        vi = timeindex - volbuf1.size
        while i < top2:
            vi= vi % volbuf2.size
            buf[i][0] = obuf[i]*volbuf2[vi]
            buf[i][1] = buf[i][0]
            i += 1
            vi += 1

            
        return buf
