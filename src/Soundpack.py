import pygame, os, wave, math, numpy, variables, copy
import time as mtime
from math import sin
from math import pi
import random
from FrozenClass import FrozenClass
from VolumeEnvelope import VolumeEnvelope
from variables import sample_rate
from wavefunctions import sinesval, squaresval, trianglesval, sawtoothsval, randomicefunction, chooserandfunction, newrandomwavefunction

max_sample = 2 ** (16 - 1) - 1

defaultvol = 0.5

# volume envelopes are lists of times and what volume it should be at that time
volumeenvelopes = {"bell" : VolumeEnvelope([[0, 0.05], [200, 1], [800, 0.3]], 200, 0.05),
                   "flat" : VolumeEnvelope([[0, defaultvol], [400, defaultvol]], 1000, 0.1)}

# volbuffers are a pair containing the volume buffer of the beginning of the volume envelope and the volume buffer for the looped section
# each buffer is a 1d numpy array with float16
volbuffers = {}

for k in volumeenvelopes:
    envelope = volumeenvelopes[k]
    n_samples = int(round(envelope.timevollist[-1][0]*sample_rate/1000))

    # then put about a second worth of the oscilation part on to the end
    n_samples2 = int(round(envelope.endoscilationrate/1000*sample_rate))
    n_samples2 = n_samples2 * int(sample_rate/n_samples2)
    firstbuf = numpy.empty((n_samples+n_samples2, 2), dtype=numpy.float)
    
    for s in range(n_samples+n_samples2):
        t = float(s)/sample_rate
        firstbuf[s][0] = envelope.tone_volume(t*1000)
        firstbuf[s][1] = firstbuf[s][0]
        
    volbuffers[k] = firstbuf

    
class Soundpack(FrozenClass):
    

    def __init__(self, wavetype, shapefactor, resetq=False):
        # list of buffers for different frequencies of notes
        # each buffer is a perfectly loopable sample of the wave, normalized
        # one dimensional array
        self.loopbuffers = []
        
        # how long in milliseconds the sound from each loopbuffer is
        self.loopbufferdurationmillis = []
        
        # finally, generate all the loopbuffers
        self.make_soundpack(wavetype, shapefactor, resetq)
        
        self._freeze()

    # min refinement of 1 which means sine wave, and bigger numbers will take longer unless it is above 25 or so
    def make_wave(self, frequency, wavetype, shapefactor):
        loopduration = (1 / frequency) * 50  # in seconds
        duration = loopduration

        n_samples = int(round(duration * sample_rate))

        # setup our numpy array to handle  bit ints, which is what we set our mixer to expect with "bits"
        buf = numpy.zeros((n_samples, 2), dtype=numpy.int)

        randfunction = None
        if wavetype == "random":
            randfunction = newrandomwavefunction()

        def get_sval(t):
            sval = 0

            if wavetype == "sine":
                sval = sinesval(t, frequency)
            elif wavetype == "square":
                sval = squaresval(t, frequency, shapefactor)
            elif wavetype == "triangle":
                sval = trianglesval(t, frequency, shapefactor)
            elif wavetype == "sawtooth":
                sval = sawtoothsval(t, frequency, shapefactor)
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
            buf[s][0] = sval
            buf[s][1] = sval

        return (buf, duration)

    def make_soundpack(self, wavetype, shapefactor, resetq):
        for x in range(37):
            loopbuf = self.make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor)
            
            self.loopbuffers.append(loopbuf[0])

            self.loopbufferdurationmillis.append(loopbuf[1]*1000)

            

    # get the buffer with the volume envelope applied at time in milliseconds
    # index is which loopbuffer for the frequency to play
    # time is time in milliseconds since start of the note played
    def getbufferattime(self, index, time, volenvelope, applyvolenvelopep):
    
        obuf = self.loopbuffers[index]
        
        volbuf = volbuffers[volenvelope]
        # find the right slice of the volume buffer
        envelope = volumeenvelopes[volenvelope]
        n_samples = int(round(envelope.timevollist[-1][0]*sample_rate/1000))
        n_samples2 = int(round(envelope.endoscilationrate/1000*sample_rate))
        volindex = int(time/1000 * sample_rate)
        if volindex>n_samples:
            volindex = n_samples + (volindex-n_samples) % n_samples2
        
        buf = numpy.empty(obuf.shape, dtype=numpy.int16)
        volbuf = volbuf[volindex:volindex+obuf.shape[0]]
        
        numpy.multiply(volbuf, obuf, out=buf, casting='unsafe')
        
        return buf
        





