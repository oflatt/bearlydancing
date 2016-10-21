import math

import numpy
import pygame

import variables


def make_sound(frequency):
    duration = 0.5          # in seconds
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

#a list of sounds from A2 to A6
all_tones = []
for x in range(49):
    s = make_sound((440*((2**(1/12))**(x-24))))
    s.set_volume(variables.battle_volume)
    all_tones.append(s)

Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")
Drum_kick_heavy.set_volume(variables.battle_volume*6)

def play_tone(t):
    #add 24 because values are centered on 0 and list is 48 long
    all_tones[t+24].play(loops = -1)

def play_sound(s):
    if s == "drum kick heavy":
        Drum_kick_heavy.play()

def stop_tone(t):
    all_tones[t+24].stop()