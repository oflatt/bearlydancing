import pygame, os, copy, sys
import platform
import dill as pickle
from pygame import Rect
from typing import List, Dict


from Settings import Settings
from Properties import Properties
from random import randint
from Game import Game

import devoptions
from devoptions import devprint


os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
# for export need the commented section
try:
    from pathtoself import pathtoself
except ImportError:
    try:
        from pathtoselfwindows import pathtoself
    except ImportError:
        from pathtoselfmac import pathtoself


pypyp = platform.python_implementation() == "PyPy"


# load settings
savefolderpath = os.path.join(pathtoself, "save0/")
graphicssavefolderpath = os.path.join(savefolderpath, "graphics/")
manualsavebackuppath = os.path.join(pathtoself, "savebackup/")
os.makedirs(savefolderpath, exist_ok=True)
os.makedirs(graphicssavefolderpath, exist_ok=True)
os.makedirs(manualsavebackuppath, exist_ok = True)

settingspath = os.path.join(savefolderpath, "bdsettings.txt")
savepath = os.path.join(savefolderpath, "bdsave.txt")
settings = Settings()
if not devoptions.args.restart and not devoptions.dontloadsettings:
    if (os.path.isfile(os.path.abspath(settingspath))):
        if os.path.getsize(os.path.abspath(settingspath)) > 0:
            with open(settingspath, "rb") as f:
                settings = pickle.load(f)
                print(settings.state)
settings.menuonq = True



# load games
def loadpolar():
    from polarinvaders.polarinvaders import creategame
    return creategame()


# go from being a function that loads a game to being a game object
games = {"polarinvaders":loadpolar}

def currentgame():
    return games[settings.currentgame]

    

# Setup
sample_rate = 22050
max_sample = 2 ** (16 - 1) - 1

pygame.mixer.pre_init(sample_rate, 16, 2, 512)

mainchannels = None
otherchannels = None


def soundinit():
    global otherchannels
    global mainchannels
    failed = False
    try:
        pygame.mixer.init()
        pygame.mixer.set_reserved(38)
        pygame.mixer.set_num_channels(46)
        mainchannels = []
        for x in range(37):
            mainchannels.append(pygame.mixer.Channel(x))
            otherchannels = [pygame.mixer.Channel(37), pygame.mixer.Channel(38)]
    except pygame.error:
         #if volume is 0, do not use the mixer, it is not initialized
        settings.volume = 0
        failed = True
    return not failed

soundinit()


pygame.init()

    
# load icon
icon = pygame.image.load(os.path.join(pathtoself, "icon.png"))

mode = None

if devoptions.args.novideomode:
    mode = (1200, 700)
else:
    pygame.display.set_icon(icon)


    pygame.display.set_caption('Bearly Dancing')


    modes = pygame.display.list_modes()
    mode = modes[0]
    if not mode is None:
        ratio = mode[0]/mode[1]

    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()
    elif sys.platform == 'darwin':
        import AppKit
        AppKit.NSMenu.setMenuBarVisible_(False)
        
        for m in modes:
            if m[0]/m[1] == ratio:
                if m[0]<1800:
                    mode = m
                    break

#(ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
# Set the width and height of the screen [width,height]
if not mode is None:
    height = mode[1]
    width = mode[0]

if devoptions.testsmallp:
    height = int(height/2)
    width = int(width/2)


screen = None
def setscreen(windowmode):
    global screen
    if windowmode == "windowed":
        flags = pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE
        screen = pygame.display.set_mode((width, height), flags, 32)
    if windowmode == "fullscreen":
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        screen = pygame.display.set_mode((width, height), flags, 32)

if not devoptions.args.novideomode:
    setscreen(settings.windowmode)

# this is used so that time does not continue durng the frame that it generates the beatmap
generatingbeatmapp = False

olddirtyrects : List[Rect] = []
# keep track of areas of the screen to update. Blitting is done regardless of dirty rects, but when a dirtyrect is appended to this list it is updated twice- this frame and next
dirtyrects : List[Rect] = []
#screen = pygame.Surface([height, width])

unrounded_displayscale = height*0.0025
# factor for the dimensions of a pixel on a given screen
displayscale = round(unrounded_displayscale+0.25)
# factor for scaling up a map to a screen
scaleoffset = 1
# the product of scaleoffset and displayscale
# this is used only for drawing the world
def compscale():
    return displayscale*scaleoffset+settings.zoomlevel
def compscaleunrounded():
    return unrounded_displayscale * scaleoffset + settings.zoomlevel

# Define some colors
BLACK = (0, 0, 0)
BLUEWHITE = (220, 220, 247)
BLUEGREY = (73, 73, 102)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)
LIGHTYELLOW = (235,227, 92)
LIGHTBLUE = (66, 206, 244)
PINK = (226, 40, 255)

def randomnicecolor():
    color = [randint(60, 255), randint(60, 255), randint(60, 255), 255]
    # set one of them to 60
    color[randint(0, 2)] = 60
    return color

def greenp(c):
    return c[1] > c[0]+10 and c[1] > c[2] + 10

def brighten(c, amount):
    if len(c) == 4:
        return (max(0, min(c[0]+amount, 255)),
                max(0, min(c[1]+amount, 255)),
                max(0, min(c[2]+amount, 255)),
                c[3])
    else:
        return (max(0, min(c[0]+amount, 255)),
                max(0, min(c[1]+amount, 255)),
                max(0, min(c[2]+amount, 255)))

def darken(c, amount):
    return brighten(c, -amount)

# font
font = pygame.font.Font(os.path.join(pathtoself, 'orangekidregular.ttf'), 30)

# map stuff
# keys are filenames like randompinetree and values are the number generated
generatedgraphicsused : Dict[str, int] = {}

def num_of_generated_graphics_used():
    s = 0
    for k in generatedgraphicsused.keys():
        s += generatedgraphicsused[k]
    return s

basemapsize = 360

snowcolor = (200, 200, 200)

TREEWIDTH = 100
TREEHEIGHT = 200
ROCKMAXRADIUS = 12
ROCKMINRADIUS = 5
TREECOLLIDESECTION = [0, 18.5 / 20, 1, 1.5 / 20]
ARCADECABINETCOLLIDESECTION = [0, 4/5.0, 1, 1/5.0]
ROCKCOLLIDESECTION = [0, 1/10, 1, 9/10]
FLOWERCOLLIDESECTION = [0, 1, 0, 0]

# battle
healthanimationspeed = 2000# time in milliseconds for the health bar animation to go
expanimationspeed = 3000
numofrounds = 2

accidentallvthreshhold=8

dancepadlevelincrease = 4

numberofoctopusheads = 3
octopusarmdraworder = [4, 3, 6, 2, 7, 1, 0, 5]
octopusarmtomultipartpart = []
for armnum in range(8):
    octopusarmtomultipartpart.append(octopusarmdraworder.index(armnum)+1) # add one because the body is drawn first
octopusarmtomultipartpart.reverse()

def getpadypos():
    return height*(13/16)

def getpadheight():
    return height / 80.0

def get_border_width():
    return max(1, int(getpadheight()/3))
    
def dancearrowwidth():
    return width/15

def notewidth():
    return width / 20

def noteendwidth():
    return notewidth()*1.25

def noteendwidthoffset():
    return (noteendwidth()-notewidth())/2

maxdifficulty = 200
# maxtime is changed in the code, the goal for how long the song should be
# lv is the level of the enemy
# rules are the rules for generating a beatmap
generic_specs = {'maxtime' : 16, 'lv' : 0, 'rules' : [], 'volumeenvelope': 'bell'}
melodic_specs = generic_specs.copy()
melodic_specs['rules'] = ["melodic"]
maxvalue = 14
minvalue = -7

perfect_value = 1.75
good_value = 1
ok_value = 0.7
miss_value = 0


all_perfect_multiplier = 1.3
player_advantage_multiplier = 1.2
# combo multiplier is calculated by  one plus the length of the max combo over the total number of notes, and then it is multiplied by this factor
player_combo_multiplier = 0.25

def getperfectrange():
    return height/100
def getgoodrange():
    return height/60
def getokrange():
    return height/25
def getmissrange():
    return height/15

notes_colors = [ORANGE, BLUE, RED, GREEN, GREEN, RED, BLUE, ORANGE]

# conversation
def gettextsize():
    return height/15
def gettextboxheight():
    return height/4
def getlinesinscreen():
    return int(gettextboxheight()/gettextsize())
def getphotosize():
    return width/6
def getbuttonpadding():
    return int(width/70)

# used to ensure that no duplicate names exist
conversationnames : List[str] = []

# menu
beginningprompttextcolor = BLUE
menuscrollspeed = 150 # in milliseconds
confirmduration = 11 # in seconds
maxbindings = 50
# keeps track of if we saved to display the symbol
saved = False

def getmenutextyspace():
    return gettextsize() * 1.5
def getmenutextxoffset():
    return gettextsize()
def getdotwidth():
    return getmenutextxoffset() / 3

#world
playerspeed = 0.07
if devoptions.devmode:
    playerspeed *= 2
accelpixelpermillisecond = 0.2359/1000
floatinessagainstreality = 0.6
accelpixelpermillisecond *= floatinessagainstreality
    
#encountering enemies
encounter_check_rate = 100 # rate of check in milliseconds
encounter_chance = 0.004 # chance per check

# wind
windcheckrate = 100
windchance = 0.05

properties = Properties()
properties_path = os.path.join(pathtoself, "properties.txt")

def load_properties():
    global properties
    if os.path.isfile(properties_path):
        if os.path.getsize(properties_path) > 0:
            f = open(properties_path, "rb")
            properties = pickle.load(f)

def save_properties():
    # overestimate
    properties.num_of_generated_graphics = int(num_of_generated_graphics_used() * 1.2)
    with open(properties_path, "wb") as f:
        pickle.dump(properties, f)

def draw_loading_text(string):
    if devoptions.args.novideomode:
        return
    text = pygame.transform.scale2x(font.render(string, 0, WHITE).convert())
    xpos = int((width / 2) - (text.get_width() / 2))
    ypos = int((height / 2) - text.get_height() - height/10)
    pygame.draw.rect(screen, BLACK, Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height()*2))
    screen.blit(text, [xpos, ypos])

def draw_loading_tips():
    if devoptions.args.novideomode:
        return
    text = pygame.transform.scale2x(font.render("tip: use the escape key to pause the game", 0, WHITE).convert())
    xpos = int((width / 2) - (text.get_width() / 2))
    ypos = int((height / 2) - text.get_height() - height/10) - text.get_height()*2.5
    pygame.draw.rect(screen, BLACK, Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height()))
    screen.blit(text, [xpos, ypos]) 

def draw_graphic_name(name):
    if not devoptions.args.novideomode:
        text = font.render(name, 0, WHITE).convert()
        xpos = int((width / 2) - (text.get_width() / 2))
        ypos = int((height -text.get_height() - height/20))
        textrect = Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height())
        pygame.draw.rect(screen, BLACK, textrect)
        screen.blit(text, [xpos, ypos])
        pygame.display.update(textrect)
    
def draw_progress_bar():
    if devoptions.args.novideomode:
        return
    #clear all the events so it does not crash
    pygame.event.get()
    numused = num_of_generated_graphics_used()
    estimated = properties.num_of_generated_graphics

    draw_loading_tips()
    
    if numused == 1:
        draw_loading_text("generating world (3/3)")
        if estimated == None:
            pygame.display.flip()
    
    if not estimated == None:
        if estimated <= 0:
            percent_complete = 1
        else:
            percent_complete = numused / estimated

        progresstext = pygame.transform.scale2x(font.render(str(numused) + "/" + str(estimated), 0, WHITE).convert())

        texty = int(height/2 + height/5)
        
        screen.fill(BLUE, Rect(0, int(height/2), width*percent_complete, height/10))
        
        screen.fill(BLACK, Rect(0, int(height/2 + height/10), width, int(height/2 + progresstext.get_height()*2)))
        
        screen.blit(progresstext, [int(width/2 - progresstext.get_width()/2), texty])
        pygame.display.flip()
        


def checkkey(name, key):
    if name == "enter":
        name = "action"
    return key in settings.keydict[name]

# returns a bigger rect that contains both of the rects
def combinerects(rect1, rect2):
    return rect1.union(rect2)


# wraps pygame transform.scale so that it checks width and height are not zero to avoid segfault
def transformscale(img, newdimensions):
    if img.get_width() == 0 or img.get_height() == 0:
        return img
    else:
        return pygame.transform.scale(img, newdimensions)

def transformrotozoom(img, angle, scale):
    if img.get_width() == 0 or img.get_height() == 0:
        return img
    else:
        return pygame.transform.rotozoom(img, angle, scale)

def transformrotate(img, degrees):
    if img.get_width() == 0 or img.get_height() == 0:
        return img
    else:
        return pygame.transform.rotate(img, degrees)

def dirtyupdateall():
    global dirtyrects
    dirtyrects = [Rect(0, 0, width, height)]

def updatescreen():
    if len(dirtyrects) > 0:
        if dirtyrects[0] == Rect(0,0,width,height):
            pygame.display.update(Rect(0,0,width, height))
        else:
            updaterects()
    elif len(olddirtyrects) > 0:
        if olddirtyrects[0] == Rect(0,0,width,height):
            pygame.display.update(Rect(0,0,width, height))
        else:
            updaterects()
    elif len(dirtyrects) == 0 and len(olddirtyrects) == 0:
        pygame.display.update(Rect(0,0,width,height))
    else:
        updaterects()

def updaterects():
    # update rects and the fps
    pygame.display.update(dirtyrects + olddirtyrects + [Rect(10,font.get_linesize(), font.get_linesize()*5, font.get_linesize()*3)])
        
sign = lambda x: (1, -1)[x < 0]

