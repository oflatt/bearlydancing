import pygame
import math
import numpy
import variables

def make_sound(frequency):
    duration = 1.0          # in seconds
    sample_rate = 44100

    n_samples = int(round(duration*sample_rate))

    #setup our numpy array to handle 16 bit ints, which is what we set our mixer to expect with "bits" up above
    buf = numpy.zeros((n_samples, 2), dtype = numpy.int16)
    max_sample = 2**(16 - 1) - 1

    for s in range(n_samples):
        t = float(s)/sample_rate    # time in seconds

        #grab the x-coordinate of the sine wave at a given time, while constraining the sample to what our mixer is set to with "bits"
        buf[s][0] = int(round(max_sample*math.sin(2*math.pi*frequency*t)))        # left
        buf[s][1] = int(round(max_sample*0.5*math.sin(2*math.pi*frequency*t)))    # right

    return pygame.sndarray.make_sound(buf)

C = make_sound(523.25)
D = make_sound(587.33)
E = make_sound(659.26)
F = make_sound(698.76)
G = make_sound(783.99)
A = make_sound(880)
B = make_sound(987.77)
Chigh = make_sound(1046.5)
Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")
C.set_volume(variables.battle_volume)
D.set_volume(variables.battle_volume)
E.set_volume(variables.battle_volume)
F.set_volume(variables.battle_volume)
G.set_volume(variables.battle_volume)
A.set_volume(variables.battle_volume)
B.set_volume(variables.battle_volume)
Chigh.set_volume(variables.battle_volume)

def play_sound(s):
    if s == "C":
        C.play(loops = -1)
    elif s == "D":
        D.play(loops = -1)
    elif s == "E":
        E.play(loops = -1)
    elif s == "F":
        F.play(loops = -1)
    elif s == "G":
        G.play(loops = -1)
    elif s == "A":
        A.play(loops = -1)
    elif s == "B":
        B.play(loops = -1)
    elif s == "Chigh":
        Chigh.play(loops = -1)
    elif s == "drum kick heavy":
        Drum_kick_heavy.play()

def stop_sound(s):
    if s == "C":
        C.stop()
    elif s == "D":
        D.stop()
    elif s == "E":
        E.stop()
    elif s == "F":
        F.stop()
    elif s == "G":
        G.stop()
    elif s == "A":
        A.stop()
    elif s == "B":
        B.stop()
    elif s == "Chigh":
        Chigh.stop()