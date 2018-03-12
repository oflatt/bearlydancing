import pygame, variables
from Soundpack import Soundpack

# nessoundfont = "soundfonts/The_Nes_Soundfont.sf2"


# each soundpack is a list of sounds from A3 to A6
# value of 0 corresponds to A4, -12 is A3
all_tones = {"sine": Soundpack("sine", 1), "square": Soundpack("square", 25),
             "triangle": Soundpack("triangle", 2),
             "triangleh": Soundpack("triangle", 30), "sawtooth": Soundpack("sawtooth", 4),
             "sawtoothh": Soundpack("sawtooth", 30)}

# all possible soundpacks
soundpackkeys = ["sine", 'square', 'triangle', 'triangleh', 'sawtooth', 'sawtoothh']

scales = {"C major" : [2, 2, 1, 2, 2, 2, 1]}  # list of offsets for the scale

Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")

channels = []
for x in range(37):
    channels.append(pygame.mixer.Channel(x))

def play_tone(t):
    # add because values are centered on 0
    all_tones[variables.settings.soundpack].soundlist[t+12].set_volume(variables.settings.volume)
    channels[t+12].play(all_tones[variables.settings.soundpack].soundlist[t + 12])

def update_tone(t):
    c = channels[t+12]
    all_tones[variables.settings.soundpack].loopsoundlist[t + 12].set_volume(variables.settings.volume)
    if c.get_queue() == None:
        c.queue(all_tones[variables.settings.soundpack].loopsoundlist[t + 12])

def play_sound(s):
    if s == "drum kick heavy":
        Drum_kick_heavy.set_volume(variables.settings.volume)
        Drum_kick_heavy.play()

def stop_tone(t):
    if not t == None:
        channels[t+12].stop()

