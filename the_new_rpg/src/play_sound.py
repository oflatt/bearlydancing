import math
import numpy
import pygame, variables

nessoundfont = "The_Nes_Soundfont.sf2"

def make_sound(frequency):
    duration = (1/frequency)*50          # in seconds
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

#a list of sounds from A3 to A6
#value of 0 corresponds to A4
#-12 is A3, then
all_tones = []
for x in range(36+1):
    s = make_sound((440*((2**(1/12))**(x-12))))
    s.set_volume(variables.battle_volume)
    all_tones.append(s)

Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")
Drum_kick_heavy.set_volume(variables.battle_volume*6)

def play_tone(t):
    #add because values are centered on 0
    all_tones[t+12].play(loops = -1)

def play_sound(s):
    if s == "drum kick heavy":
        Drum_kick_heavy.play()

def stop_tone(t):
    all_tones[t+12].stop()