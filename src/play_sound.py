import pygame, variables, random, os
from Soundpack import Soundpack

# nessoundfont = "soundfonts/The_Nes_Soundfont.sf2"


# each soundpack is a list of sounds from A3 to A6
# value of 0 corresponds to A4, -12 is A3
all_tones = {"sine": Soundpack("sine", 1), "square": Soundpack("square", 25),
             "triangle": Soundpack("triangle", 30), "sawtooth": Soundpack("sawtooth", 30),
             "sawsoft": Soundpack("sawtooth", 4)}

def currentsoundpack():
    return all_tones[variables.settings.soundpack]

# all possible soundpacks
soundpackkeys = list(all_tones.keys())

scales = {"C major" : [2, 2, 1, 2, 2, 2, 1],
          "C minor" : [2, 1, 2, 2, 1, 3, 1],
          "chromatic" : [1, 1, 1, 6, 1, 1, 1]}# list of offsets for the scale

def loadmusic(filename):
    return pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/", filename))

onedrum = loadmusic("onedrum.wav")
menumusic = loadmusic("menu.wav")
bearhome = loadmusic("bearhome.wav")
engagebattle = loadmusic("encounterenemy.wav")

channels = []
for x in range(37):
    channels.append(pygame.mixer.Channel(x))

musicchannel = pygame.mixer.Channel(37)
soundeffectchannel = pygame.mixer.Channel(38)

def play_tone(tonein):
    t = tonein
    if t+12>=len(all_tones[variables.settings.soundpack].soundlist):
        t = len(all_tones[variables.settings.soundpack].soundlist)-1-12
    elif t+12 < 0:
        t = 0-12
    # add because values are centered on 0
    all_tones[variables.settings.soundpack].soundlist[t+12]
    channels[t+12].set_volume(variables.settings.volume*(1/3)) # balance volume
    channels[t+12].play(all_tones[variables.settings.soundpack].soundlist[t + 12])

def update_tone(t):
    c = channels[t+12]
    all_tones[variables.settings.soundpack].loopsoundlist[t + 12]
    c.set_volume(variables.settings.volume*(1/3))
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
    soundeffectchannel.set_volume(variables.settings.volume)
    soundeffectchannel.play(sound)

def play_music(s):
    sound = getsoundvar(s)
    musicchannel.set_volume(variables.settings.volume)
    musicchannel.play(sound, loops=-1)

def stop_music():
    musicchannel.stop()

def stop_effect():
    soundeffectchannel.stop()

############################################ grassland music #########################################
finalgrassmelody = pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/modmusicgrassland/melodyfinal.wav"))
grassmelodys = []
INDEXES = []
for x in range(13):
    grassmelodys.append(pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/modmusicgrassland/melody" + str(x) + ".wav")))
    INDEXES.append(x)
    
indexes_left = INDEXES.copy()

grassdrums = []
for x in range(6):
    grassdrums.append(pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/modmusicgrassland/drum" + str(x) + ".wav")))

def initiatedrums():
    sound = random.choice(grassdrums)
    soundeffectchannel.set_volume(variables.settings.volume)
    soundeffectchannel.play(sound)
    
def nextgrasslandsound():
    global indexes_left
    if len(indexes_left) > 0:
        index = random.choice(indexes_left)
        indexes_left.remove(index)
        return grassmelodys[index]
    else:
        indexes_left = INDEXES.copy()
        return finalgrassmelody

def initiatemelody():
    indexes_left = INDEXES.copy()
    sound = nextgrasslandsound()
    musicchannel.set_volume(variables.settings.volume)
    musicchannel.play(sound)
    
def initiategrasslandmusic():
    initiatemelody()
    initiatedrums()

def grasslandmusictick():
    if not musicchannel.get_busy():
        initiatemelody()
        initiatedrums()
    elif musicchannel.get_queue() == None:
        sound = nextgrasslandsound()
        musicchannel.set_volume(variables.settings.volume)
        musicchannel.queue(sound)

    if not soundeffectchannel.get_busy():
        initiatedrums()
    elif soundeffectchannel.get_queue() == None:
        sound = random.choice(grassdrums)
        soundeffectchannel.set_volume(variables.settings.volume)
        soundeffectchannel.queue(sound)

def setnewvolume():
    musicchannel.set_volume(variables.settings.volume)
    soundeffectchannel.set_volume(variables.settings.volume)
        
