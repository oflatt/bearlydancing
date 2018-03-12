import pygame, os, wave, math, numpy
from math import sin
from math import pi

initialvolume = 1
max_sample = 2 ** (16 - 1) - 1
bellvolume = [[0, 0], [100, 1], [600, 0.15]]

class Soundpack():
    

    def __init__(self, wavetype, shapefactor, resetq=False):
        self.soundlist = []
        self.loopsoundlist = []
        self.loopbuffers = []
        self.volumelist = bellvolume
        self.make_soundpack(wavetype, shapefactor, resetq)

    #durationplayed in is milliseconds
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
            if (frequency * t) % 2 < 0.5:
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
            sval = (2 / p) * abs((t % p) - p / 2) - p / 4
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
    def make_wave(self, frequency, wavetype, shapefactor, loopq = False):
        loopduration = (1 / frequency) * 50  # in seconds
        duration = self.volumelist[-1][0]/1000 + loopduration
        if loopq:
            duration = loopduration
        sample_rate = 44100

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
            if loopq == False:
                volume = self.tone_volume(t * 1000)
            sval = (get_sval(t) / normalizevalue) * volume 
            buf[s][0] = sval # left
            buf[s][1] = sval # right

        if loopq:
            self.loopbuffers.append(buf)
            
        return pygame.sndarray.make_sound(buf)

    def make_soundpack(self, wavetype, shapefactor, resetq):
        l = []
        isexistingsounds = os.path.exists("sounds/" + wavetype + "0_" + str(shapefactor) + ".wav")
        if isexistingsounds and resetq == False:
            for x in range(37):
                l.append(pygame.mixer.Sound("sounds/" + wavetype + str(x) + "_" + str(shapefactor) + ".wav"))
                l[x].set_volume(initialvolume)
                loopwave = self.make_wave((440 * ((2 ** (1 / 12)) ** (x - 12))), wavetype, shapefactor, True)
                self.loopsoundlist.append(loopwave)
                self.loopsoundlist[x].set_volume(initialvolume)
        else:
            try:
                os.makedirs("sounds")
            except OSError:
                pass
            for x in range(36 + 1):
                currentfrequency = 440 * ((2 ** (1 / 12)) ** (x - 12))
                
                s = self.make_wave(currentfrequency, wavetype, shapefactor)
                s.set_volume(initialvolume)

                # save it for future loading
                sfile = wave.open("sounds/" + wavetype + str(x) + "_" + str(shapefactor) + ".wav", "w")
                sfile.setframerate(22050)
                sfile.setnchannels(2)
                sfile.setsampwidth(2)
                sfile.writeframesraw(s.get_raw())
                sfile.close()

                l.append(s)

                loopwave = self.make_wave(currentfrequency, wavetype, shapefactor, True)
                loopwave.set_volume(initialvolume)
                self.loopsoundlist.append(loopwave)
                
        self.soundlist = l
