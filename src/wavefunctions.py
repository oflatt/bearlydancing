import math, random
from math import sin
from math import pi

def sinesval(t, f):
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
