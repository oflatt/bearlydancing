from variables import mainchannels, otherchannels
import pygame, variables, random, os
from graphics import drawwave
from Soundpack import Soundpack
from DrumPack import DrumPack
from pygame import Rect

# nessoundfont = "soundfonts/The_Nes_Soundfont.sf2"


# each soundpack is a list of sounds from A3 to A6
# value of 0 corresponds to A4, -12 is A3
all_tones = {"sine": Soundpack("sine", 1), "square": Soundpack("square", 25),
             "triangle": Soundpack("triangle", 30), "sawtooth": Soundpack("sawtooth", 30),
             "noisy": Soundpack("noisysine", 25), # TODO: add noise to it, 0.5 normal with 0.1 st dev
             "random":Soundpack("random", 8)}

def currentsoundpack():
    return all_tones[variables.settings.soundpack]

drumpacks = {"normalnoise" : DrumPack("noisedrum", 30, "sharp", 0, 36),
             "deepnoise" : DrumPack("noisedrum", 30, "sharp", -24, 36),
             "chirp" : DrumPack("noisysine", 30, "chirp", 12, 48),
             # 40 milliseconds of transition, and make it very low
             "oomphwave" : DrumPack("oomphwave", 20, "sharp", -24-12, 6, duration=((1/440)*150))}

# all possible soundpacks
soundpackkeys = list(all_tones.keys())

scales = {"C major" : [2, 2, 1, 2, 2, 2, 1],
          "C minor" : [2, 1, 2, 2, 1, 3, 1],
          "chromatic" : [1, 1, 1, 6, 1, 1, 1]}# list of offsets for the scale

def loadmusic(filename):
    return pygame.mixer.Sound(os.path.join(variables.pathtoself, "music/", filename))


effects = {
    "menumusic":loadmusic("menu.wav"),
    "bearhome" :loadmusic("bearhome.wav"),
    "engagebattle" : loadmusic("encounterenemy.wav"),
    "onedrum" : drumpacks["normalnoise"].getsound(4)}


# stores time in milliseconds of the current end of the music queued on the channel
# none if not playing
channeltimes = [None]*37



def buffertosound(b):
    return pygame.sndarray.make_sound(b)

def play_tone(tonein, volenvelope, numofupdatetonessofar):
    if not variables.settings.soundonp():
        return
    t = tonein
    # make t always in range if out of range
    if t+12>=len(all_tones[variables.settings.soundpack].loopbuffers):
        t = len(all_tones[variables.settings.soundpack].loopbuffers)-1-12
    elif t+12 < 0:
        t = 0-12

    # add because values are centered on 0
    sp = all_tones[variables.settings.soundpack]
    mainchannels[t+12].set_volume(variables.settings.volume) # balance volume
    buf = sp.getbufferattime(t+12, 0, volenvelope, True)
    mainchannels[t+12].play(buffertosound(buf))
    displaywave(buf, t+12, numofupdatetonessofar)
 
    channeltimes[t+12] = sp.loopbufferdurationmillis[t+12]

# tonein is a index of the tone to play
# volenvelope is the name of the volenvelope to use
# numofupdatetonessofar is how many times we have called it so far
# this allows us to put a cap on the number of
# volumeenvelopes to apply, since it is expensive
def update_tone(tonein, volenvelope, numofupdatetonessofar):
    if not variables.settings.soundonp():
        return
    
    updatevolenvelopep = numofupdatetonessofar < variables.settings.maxvolumeenvelopesperframe
    
    t = tonein
    if t+12>=len(all_tones[variables.settings.soundpack].loopbuffers):
        t = len(all_tones[variables.settings.soundpack].loopbuffers)-1-12
    elif t+12 < 0:
        t = 0-12

    c = mainchannels[t+12]
    sp = all_tones[variables.settings.soundpack]

    if channeltimes[t+12] == None:
        channeltimes[t+12] = 0
    
    c.set_volume(variables.settings.volume)

    if c.get_queue() == None:
        buf = sp.getbufferattime(t+12, channeltimes[t+12], volenvelope, updatevolenvelopep)
        c.queue(buffertosound(buf))
        channeltimes[t+12] += sp.loopbufferdurationmillis[t+12]
        displaywave(buf, t+12, numofupdatetonessofar)
        firstbuf = sp.getbufferattime(t+12, 0, volenvelope, True)

def stop_tone(tonein):
    if not variables.settings.soundonp():
        return
    
    t = tonein
    if t+12>=len(all_tones[variables.settings.soundpack].loopbuffers):
        t = len(all_tones[variables.settings.soundpack].loopbuffers)-1-12
    elif t+12 < 0:
        t = 0-12
    if not t == None:
        mainchannels[t+12].stop()
        channeltimes[t+12] = None
        stopdisplaywave(t+12)

displaytuples = [None] * 37
furthestdisplaywavex = 0
nextdisplaywavey = 0
        
def displaywave(buf, channel, drawnsofar):
    if not variables.settings.soundonp():
        return
    
    global furthestdisplaywavex, nextdisplaywavey
    # make it so that each second crosses .2 of the width of the screen
    wavelen = (buf.size/2)/variables.sample_rate * 0.2 * variables.width
    t = displaytuples[channel]
    waveamp = variables.gettextsize() * 0.7
    if t == None:
        if nextdisplaywavey < waveamp:
            nextdisplaywavey = waveamp
            
        # init a new display tuple
        displaytuples[channel] = (furthestdisplaywavex-wavelen, nextdisplaywavey, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        
        nextdisplaywavey += waveamp*2
        if nextdisplaywavey > int(variables.getpadypos() -waveamp):
            nextdisplaywavey = waveamp
            
        t = displaytuples[channel]

    wavex = t[0]
    wavey = t[1]
    skiplen = len(buf)/wavelen
    drawwave(buf, skiplen, wavex, wavey, waveamp, wavelen, t[2], False)

    # now just update once and let it stay on screen
    pygame.display.update(Rect(wavex, wavey-waveamp, wavelen, waveamp*2))

    maxwavex = (variables.width*9/12)
    newwavex = wavex+wavelen
    if newwavex > maxwavex:
        newwavex = 0
        furthestdisplaywavex = newwavex
        variables.dirtyrects = [Rect(0,0,variables.width,variables.height)]
    
    displaytuples[channel] = (newwavex, wavey, t[2])
    if newwavex > furthestdisplaywavex:
        furthestdisplaywavex = newwavex    
        
        

def stopdisplaywave(channel):
    displaytuples[channel] = None

def getsoundvar(s):
    g = globals()
    return g[s]
        
def play_effect(s):
    if variables.settings.soundonp():
        sound = effects[s]
        otherchannels[0].set_volume(variables.settings.volume)
        otherchannels[0].play(sound)

def play_drum(index, drumpackname):
    if variables.settings.soundonp():
        otherchannels[0].set_volume(variables.settings.volume)
        otherchannels[0].play(drumpacks[drumpackname].getsound(index))
    
def play_music(s):
    if variables.settings.soundonp():
        sound = effects[s]
        otherchannels[1].set_volume(variables.settings.volume)
        otherchannels[1].play(sound, loops=-1)

def stop_music():
    if not variables.settings.soundonp():
        return
    otherchannels[1].stop()

def stop_effect():
    if not variables.settings.soundonp():
        return
    otherchannels[0].stop()

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
    if not variables.settings.soundonp():
        return
    sound = random.choice(grassdrums)
    otherchannels[0].set_volume(variables.settings.volume)
    otherchannels[0].play(sound)
    
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
    if not variables.settings.soundonp():
        return
    indexes_left = INDEXES.copy()
    sound = nextgrasslandsound()
    otherchannels[1].set_volume(variables.settings.volume)
    otherchannels[1].play(sound)
    
def initiategrasslandmusic():
    initiatemelody()
    initiatedrums()

def grasslandmusictick():
    if not variables.settings.soundonp():
        return
    if not otherchannels[1].get_busy():
        initiatemelody()
        initiatedrums()
    elif otherchannels[1].get_queue() == None:
        sound = nextgrasslandsound()
        otherchannels[1].set_volume(variables.settings.volume)
        otherchannels[1].queue(sound)

    if not otherchannels[0].get_busy():
        initiatedrums()
    elif otherchannels[0].get_queue() == None:
        sound = random.choice(grassdrums)
        otherchannels[0].set_volume(variables.settings.volume)
        otherchannels[0].queue(sound)

def setnewvolume():
    if not variables.settings.soundonp():
        return
    otherchannels[1].set_volume(variables.settings.volume)
    otherchannels[0].set_volume(variables.settings.volume)
        
