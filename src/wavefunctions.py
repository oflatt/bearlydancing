import math, random, numpy, random, os, wave, pygame
from math import sin
from math import pi

from variables import sample_rate
from variables import max_sample

def sinesval(t, f, shapefactorunused):
    wave = math.sin(2 * math.pi * f * t)
    harmonic1 = (1 / 4) * math.sin(4 * math.pi * f * t)
    harmonic2 = (1 / 8) * math.sin(8 * math.pi * f * t)
    s = wave + harmonic1 + harmonic2
    return s

def squaresval(t, frequency, squareness):
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

def trianglesval(t, f, shapefactor):
    sval = 0
    if shapefactor < 25:
        for k in range(shapefactor):
            sval += (-1 ** k) * (sin(2 * pi * (2 * k + 1) * f * t) / ((2 * k + 1) ** 2))
    else:
        p = 1 / f
        sval = (2 / p) * 2* (abs((t % p) - p / 2) - p / 4)
    return sval

# shapefactor is a factor used for additive synthesis
def sawtoothsval(t, f, shapefactor):
    p = 1 / f
    sval = 0
    if shapefactor < 25:
        for a in range(shapefactor):
            k = a + 1
            sval += ((-1) ** k) * (sin(2 * pi * k * f * t) / k)
    else:
        sval = 2 * ((t / p) - ((0.5 + (t / p)) // 1))

    return sval

def randomicefunction():
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

def chooserandfunction():
    return random.choice([randomicefunction(), sawtoothsval, squaresval, trianglesval])

# combine square, triangle, saw with different weights
def newrandomwavefunction():
    rfunction = chooserandfunction()
    rfunction2 = chooserandfunction()
    rfunction3 = chooserandfunction()
    def sfunction(t, f, shapefactor):
        # add harmonics
        return rfunction(t,f,shapefactor) + (1/4)*rfunction2(2*t, f, shapefactor) + (1/8)*rfunction3(4*t, f, shapefactor)
    return sfunction


def noisydrumsval(t, f, shapefactor):
    noiselevel = 0.2
    sval = sinesval(t,f,shapefactor)*numpy.random.normal(0.5, noiselevel)
    if random.random()<0.4:
        return -sval
    else:
        return sval

def noisysine(t, f, shapefactor):
    noiselevel = 0.1
    sval = sinesval(t,f,shapefactor)*numpy.random.normal(0.5, noiselevel)
    if random.random()<0.2:
        return -sval*0.5
    else:
        return sval

def lazerwave(t, f, shapefactor):
    t = t * 1000
    return math.sin(f*(math.pow(shapefactor, 2)/(t+1))*2*math.pi)

def oomphgong(t, f, shapefactor):
    t = t * 1000
    if t > shapefactor:
        secondt = math.pow(t, math.sin(t*2*0.2*math.pi)*0.05+1)
        secondt = (secondt-shapefactor)/1000
        return math.sin(2 * math.pi * f * secondt + f*(math.pow(shapefactor, 2)/(shapefactor+20))*2*math.pi)
    else:
        return math.sin(f*((math.pow(shapefactor, 2)/(t+1))/1000)*2*math.pi)
    
# changes the frequency over time to reach the target frequency, starting at triple the frequency
# shapefactor used for how long the transition takes- in milliseconds
def oomphwave(t, f, shapefactor):
    t = t * 1000
    if t > shapefactor:
        secondt = t
        secondt = (secondt-shapefactor)/1000
        return sawtoothsval(secondt + ((math.pow(shapefactor, 2)/(shapefactor+1))/1000), f, 6)
    else:
        return sawtoothsval((math.pow(shapefactor, 2)/(t+1))/1000, f, 6)

# new sval functions need to be added to the list
wavetypetofunction = {"sine":sinesval,
                      "square": squaresval,
                      "triangle": trianglesval,
                      "sawtooth": sawtoothsval,
                      "noisedrum":noisydrumsval,
                      "noisysine":noisysine,
                      "oomphwave":oomphwave}

# min refinement of 1 which means sine wave, and bigger numbers will take longer unless it is above 25 or so
# the default duration (None) is 1/frequency * 50
# processfunction is a function called on each of the values with the time and the value- it returns a new value
def make_wave(frequency, wavetype, shapefactor, sampleduration = None):
    if sampleduration == None:
        loopduration = (1 / frequency) * 100  # assume at least 8 frame/second
    else:
        loopduration = sampleduration
    duration = loopduration

    n_samples = int(round(duration * sample_rate))

    # setup our numpy array to handle  bit ints, which is what we set our mixer to expect with "bits"
    buf = numpy.zeros((n_samples, 2), dtype=int)

    randfunction = None
    if wavetype == "random":
        randfunction = newrandomwavefunction()

    svalfunction = None
    
    if wavetype == "random":
        svalfunction = randfunction
    elif wavetype in wavetypetofunction:
        svalfunction = wavetypetofunction[wavetype]
    else:
        raise Exception("unknown wavetype " + wavetype)

    def get_sval(t):
        
        return int(round(max_sample * svalfunction(t, frequency, shapefactor)))

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

    if wavetype == "replace to save a wavetype":
        savebuffertofile(wavetype + str(frequency), buf)

    return (buf, duration)


def savebuffertofile(name, buff):
    savesoundtofile(name, pygame.sndarray.make_sound(buff))

# saves a pygame sound to a wav file in sounds folder
def savesoundtofile(name, sound):
    try:
        os.makedirs("sounds")
    except OSError:
        pass

    sfile = wave.open("sounds/" + name + ".wav", "w")
    sfile.setframerate(sample_rate)
    sfile.setnchannels(2)
    sfile.setsampwidth(2)
    sfile.writeframesraw(sound.get_raw())
    sfile.close()

