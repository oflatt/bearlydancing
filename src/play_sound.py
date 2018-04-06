import pygame, variables, random
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

scales = {"C major" : [2, 2, 1, 2, 2, 2, 1],
          "C minor" : [2, 1, 2, 2, 1, 3, 1]}# list of offsets for the scale

onedrum = pygame.mixer.Sound("music/onedrum.wav")
menumusic = pygame.mixer.Sound("music/menu.wav")
bearhome = pygame.mixer.Sound("music/bearhome.wav")

channels = []
for x in range(37):
    channels.append(pygame.mixer.Channel(x))

musicchannel = pygame.mixer.Channel(37)
soundeffectchannel = pygame.mixer.Channel(38)

def play_tone(t):
    # add because values are centered on 0
    all_tones[variables.settings.soundpack].soundlist[t+12].set_volume(variables.settings.volume*(1/2)) # balance volume
    channels[t+12].play(all_tones[variables.settings.soundpack].soundlist[t + 12])

def update_tone(t):
    c = channels[t+12]
    all_tones[variables.settings.soundpack].loopsoundlist[t + 12].set_volume(variables.settings.volume*(1/2))
    if c.get_queue() == None:
        c.queue(all_tones[variables.settings.soundpack].loopsoundlist[t + 12])

def stop_tone(t):
    if not t == None:
        channels[t+12].stop()

def getsoundvar(s):
    g = globals()
    return g[s]
        
def play_effect(s):
    sound = getsoundvar(s)
    sound.set_volume(variables.settings.volume)
    soundeffectchannel.play(sound)

def play_music(s):
    sound = getsoundvar(s)
    sound.set_volume(variables.settings.volume)
    musicchannel.play(sound, loops=-1)

def stop_music():
    musicchannel.stop()


############################################ grassland music #########################################
grassmelodys = []
for x in range(13):
    grassmelodys.append(pygame.mixer.Sound("music/modmusicgrassland/melody" + str(x) + ".wav"))

grassdrums = []
for x in range(6):
    grassmelodys.append(pygame.mixer.Sound("music/modmusicgrassland/drum" + str(x) + ".wav"))
    
def nextgrasslandsound():
    return random.choice(grassmelodys)

def initiatemelody():
    sound = nextgrasslandsound()
    sound.set_volume(variables.settings.volume)
    musicchannel.play(sound)

def initiatedrums():
    sound = random.choice(grassdrums)
    sound.set_volume(variables.settings.volume)
    soundeffectchannel.play(sound)
    
def initiategrasslandmusic():
    initiatemelody()
    initiatedrums()

def grasslandmusictick():
    if not musicchannel.get_busy():
        initiatemelody()
    elif musicchannel.get_queue() == None:
        sound = nextgrasslandsound()
        sound.set_volume(variables.settings.volume)
        musicchannel.queue(sound)
