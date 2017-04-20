import pygame, variables
from Soundpack import Soundpack

# nessoundfont = "soundfonts/The_Nes_Soundfont.sf2"


# each soundpack is a list of sounds from A3 to A6
# value of 0 corresponds to A4, -12 is A3
all_tones = {"sine": Soundpack("sine", 1), "square": Soundpack("square", 3),
             "squareh": Soundpack("square", 25), "triangle": Soundpack("triangle", 2),
             "triangleh": Soundpack("triangle", 30), "sawtooth": Soundpack("sawtooth", 2),
             "sawtoothh": Soundpack("sawtooth", 30)}

# all possible soundpacks
soundpackkeys = ["sine", 'square', 'squareh', 'triangle', 'triangleh', 'sawtooth', 'sawtoothh']

Drum_kick_heavy = pygame.mixer.Sound("drum_heavy_kick.wav")
Drum_kick_heavy.set_volume(variables.battle_volume * 6)

channels = []
for x in range(37):
    channels.append(pygame.mixer.Channel(x))

def play_tone(t):
    # add because values are centered on 0
    channels[t+12].play(all_tones[variables.settings.soundpack].soundlist[t + 12], loops=-1)

def play_sound(s):
    if s == "drum kick heavy":
        Drum_kick_heavy.play()

def stop_tone(t):
    if not t == None:
        channels[t+12].stop()

