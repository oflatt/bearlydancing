import pygame, os, pickle
from pygame import Rect
from Settings import Settings
from Properties import Properties
from sys import platform

os.environ['SDL_VIDEO_WINDOW_POS'] = "0,0"
# for export need the commented section
try:
    from pathtoself import pathtoself
except ImportError:
    try:
        from pathtoselfwindows import pathtoself
    except ImportError:
        from pathtoselfmac import pathtoself


testsmallp = False
devmode = True
skipsteve = True
newworldeachloadq = False
# this overrides the generation of a new set of graphics for a new game
newworldnever = False
# this is for not loading the maps from the save file, to test new map changes
dontloadmapsdict = False
# only loads first couple of maps
fasttestmodep = False
# adds to player level when loading
lvcheat = 0

# if None it does nothing, if it is a dictionary for "specs" it goes directly into a battle with those specs
testspecs = None#{'maxtime' : 20, 'lv' : 4, 'rules' : ["alternating"]}

devlosebattlekey = pygame.K_DELETE
devwinbattlekey = pygame.K_END
devengagebattlekey = pygame.K_END

# this is the mode for the finished product- it just turns off all other development modes
exportmode = False
if exportmode:
    testsmallp = False
    devmode = False
    newworldnever = False
    newworldeachloadq = False
    dontloadmapsdict = False
    fasttestmodep = False
    testspecs = None
    lvcheat = 0
    skipsteve = False

# Setup
pygame.mixer.pre_init(22050, -16, 2, 128)
pygame.mixer.init()
pygame.init()

# load icon
icon = pygame.image.load(os.path.join(pathtoself, "icon.png"))
pygame.display.set_icon(icon)

pygame.display.set_caption('Bearly Dancing')
pygame.mixer.set_num_channels(46)

modes = pygame.display.list_modes()
mode = modes[0]
ratio = mode[0]/mode[1]

if platform == 'win32':
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
elif platform == 'darwin':
    import AppKit
    AppKit.NSMenu.setMenuBarVisible_(False)
    for m in modes:
        if m[0]/m[1] == ratio:
            if m[0]<1800:
                mode = m
                break

#(ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
# Set the width and height of the screen [width,height]
height = mode[1]
width = mode[0]

if testsmallp:
    height = int(height/2)
    width = int(width/2)

savefolderpath = os.path.join(pathtoself, "save0/")
manualsavebackuppath = os.path.join(pathtoself, "savebackup/");
settingspath = os.path.join(savefolderpath, "bdsettings.txt")
savepath = os.path.join(savefolderpath, "bdsave.txt")
settings = Settings()
if (os.path.isfile(os.path.abspath(settingspath))):
        if os.path.getsize(os.path.abspath(settingspath)) > 0:
            with open(settingspath, "rb") as f:
                settings = pickle.load(f)
settings.menuonq = True


screen = None
def setscreen(windowmode):
    global screen
    if windowmode == "windowed":
        flags = pygame.NOFRAME | pygame.DOUBLEBUF | pygame.HWSURFACE
        screen = pygame.display.set_mode((width, height), flags)
    if windowmode == "fullscreen":
        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
        screen = pygame.display.set_mode((width, height), flags)

setscreen(settings.windowmode)

# this is used so that time does not continue durng the frame that it generates the beatmap
generatingbeatmapp = False

olddirtyrects = []
dirtyrects = []
#screen = pygame.Surface([height, width])

unrounded_displayscale = height*0.0025
# factor for the dimensions of a pixel on a given screen
displayscale = round(unrounded_displayscale+0.25)
# factor for scaling up a map to a screen
scaleoffset = 1
# the product of scaleoffset and displayscale
compscale = displayscale
compscaleunrounded = unrounded_displayscale

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)
LIGHTYELLOW = (235,227, 92)
LIGHTBLUE = (66, 206, 244)

# font
font = pygame.font.Font(os.path.join(pathtoself, 'orangekidregular.ttf'), 30)

# map stuff
# keys are filenames like randompinetree and values are the number generated
generatedgraphicsused = {}

def num_of_generated_graphics_used():
    s = 0
    for k in generatedgraphicsused.keys():
        s += generatedgraphicsused[k]
    return s

basemapsize = 360

snowcolor = (220, 220, 220)

TREEWIDTH = 100
TREEHEIGHT = 200
ROCKMAXRADIUS = 12
TREECOLLIDESECTION = [0, 18.5 / 20, 1, 1.5 / 20]
ROCKCOLLIDESECTION = [0, 1/10, 1, 9/10]
FLOWERCOLLIDESECTION = [0, 1, 0, 0]

# battle
healthanimationspeed = 2000# time in milliseconds for the health bar animation to go
expanimationspeed = 3000
numofrounds = 2

def getpadypos():
    return height*(13/16)

# lv and rules are added later
maxdifficulty = 200
generic_specs = {'maxtime' : 16, 'lv' : 0, 'rules' : []}
melodic_specs = {'maxtime' : 16, 'lv' : 0, 'rules' : ['melodic']}
maxvalue = 14
minvalue = -7

perfect_value = 1.75
good_value = 1
ok_value = 0.7
miss_value = 0

all_perfect_multiplier = 1.75
player_advantage_multiplier = 1.3

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
conversationnames = []

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
if devmode:
    playerspeed *= 2
accelpixelpermillisecond = 0.2359/1000
floatinessagainstreality = 0.6
accelpixelpermillisecond *= floatinessagainstreality
    
#encountering enemies
encounter_check_rate = 100 # rate of check in milliseconds
encounter_chance = 0.002 # chance per check

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
    text = pygame.transform.scale2x(font.render(string, 0, WHITE).convert())
    xpos = int((width / 2) - (text.get_width() / 2))
    ypos = int((height / 2) - text.get_height() - height/10)
    pygame.draw.rect(screen, BLACK, Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height()*2))
    screen.blit(text, [xpos, ypos])

def draw_loading_tips():
    text = pygame.transform.scale2x(font.render("tip: use the escape key to pause the game", 0, WHITE).convert())
    xpos = int((width / 2) - (text.get_width() / 2))
    ypos = int((height / 2) - text.get_height() - height/10) - text.get_height()*2.5
    pygame.draw.rect(screen, BLACK, Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height()))
    screen.blit(text, [xpos, ypos])

def draw_progress_bar():
    #clear all the events so it does not crash
    pygame.event.get()
    numused = num_of_generated_graphics_used()
    estimated = properties.num_of_generated_graphics

    draw_loading_tips()
    
    if numused == 1:
        draw_loading_text("generating world (2/2)")
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

def updatescreen():
    pygame.display.update(dirtyrects + olddirtyrects + [Rect(10,font.get_linesize(), font.get_linesize()*6, font.get_linesize()*6)])
