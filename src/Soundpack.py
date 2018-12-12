import pygame, os, wave, math, numpy, variables, copy
import time as mtime
from math import sin
from math import pi
import random

from FrozenClass import FrozenClass
from VolumeEnvelope import VolumeEnvelope
from variables import sample_rate
from wavefunctions import make_wave
from variables import max_sample
from volumebuffers import volbuffers, volumeenvelopes
    
class Soundpack(FrozenClass):
    

    def __init__(self, wavetype, shapefactor):
        # list of buffers for different frequencies of notes
        # each buffer is a perfectly loopable sample of the wave, normalized
        # two dimensional array
        self.loopbuffers = []
        
        # how long in milliseconds the sound from each loopbuffer is
        self.loopbufferdurationmillis = []
        
        # finally, generate all the loopbuffers
        self.make_soundpack(wavetype, shapefactor)
        
        self._freeze()

    
    def make_soundpack(self, wavetype, shapefactor):
        for x in range(37):
            loopbuf = make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor)
            
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
        





