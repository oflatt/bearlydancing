import pygame, os, pickle
from pygame import Rect
from Settings import Settings
from Properties import Properties

testsmallp = False
devmode = True
newworldeachloadq = False
# this overrides the generation of a new set of graphics for a new game
newworldnever = True
# this is for not loading the maps from the save file, to test new map changes
dontloadmapsdict = True
# only loads first couple of maps
fasttestmodep = False

# if None it does nothing, if it is a dictionary for "specs" it goes directly into a battle with those specs
testspecs = None #{'maxtime' : 20, 'lv' : 7, 'rules' : ["repeatvalues", "highrepeatchance", "cheapending"]}

devlosebattlekey = pygame.K_DELETE
devwinbattlekey = pygame.K_END

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

# Setup
pygame.mixer.pre_init(22050, -16, 2, 128)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(46)

if os.name == 'nt':
    import ctypes
    ctypes.windll.user32.SetProcessDPIAware()
    
modes = pygame.display.list_modes()
mode = modes[0]#(ctypes.windll.user32.GetSystemMetrics(0),ctypes.windll.user32.GetSystemMetrics(1))
# Set the width and height of the screen [width,height]
height = mode[1]
width = mode[0]

if testsmallp:
    height = int(height/2)
    width = int(width/2)
    

flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
screen = pygame.display.set_mode(mode, flags)
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
font = pygame.font.Font(os.path.realpath('orangekidregular.ttf'), 30)

# map stuff
# pinetreesused is used to keep track of how many random trees are used
pinetreesused = 0
grasslandsused = 0
greyrocksused = 0

def num_of_generated_graphics_used():
    return pinetreesused + grasslandsused + greyrocksused

basemapsize = 360

TREEWIDTH = 100
TREEHEIGHT = 200
ROCKMAXRADIUS = 12
TREECOLLIDESECTION = [0, 18.5 / 20, 1, 1.5 / 20]
ROCKCOLLIDESECTION = [0, 1/10, 1, 9/10]

# battle
healthanimationspeed = 2000# time in milliseconds for the health bar animation to go
expanimationspeed = 3000
def getpadypos():
    return height*(13/16)

# lv and rules are added later
maxdifficulty = 200
generic_specs = {'maxtime' : 20, 'lv' : 0, 'rules' : []}
melodic_specs = {'maxtime' : 20, 'lv' : 0, 'rules' : ['melodic']}
maxvalue = 14
minvalue = -7

perfect_value = 1.75
good_value = 1
ok_value = 0.7
miss_value = 0

all_perfect_multiplier = 1.7
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

def getmenutextyspace():
    return gettextsize() * 1.5
def getmenutextxoffset():
    return gettextsize()
def getdotwidth():
    return getmenutextxoffset() / 3

#world
playerspeed = 0.05
if devmode:
    playerspeed *= 2
accelpixelpermillisecond = 0.2359/1000
floatinessagainstreality = 0.6
accelpixelpermillisecond *= floatinessagainstreality
    
#encountering enemies
encounter_check_rate = 100 # rate of check in milliseconds
encounter_chance = 0.002 # chance per check

settings = Settings()
properties = Properties()
properties_filename = "properties.txt"

def load_properties():
    global properties
    if os.path.isfile(os.path.abspath(properties_filename)):
        if os.path.getsize(os.path.abspath(properties_filename)) > 0:
            f = open(properties_filename, "rb")
            properties = pickle.load(f)

def save_properties():
    properties.num_of_generated_graphics = num_of_generated_graphics_used()
    with open("properties.txt", "wb") as f:
        pickle.dump(properties, f)

def draw_loading_text(string):
    text = pygame.transform.scale2x(font.render(string, 0, WHITE).convert())
    xpos = int((width / 2) - (text.get_width() / 2))
    ypos = int((height / 2) - text.get_height() - height/10)
    pygame.draw.rect(screen, BLACK, Rect(xpos-text.get_width(), ypos, text.get_width()*3, text.get_height()*2))
    screen.blit(text, [xpos, ypos])

def draw_progress_bar():
    #clear all the events so it does not crash
    pygame.event.get()
    numused = num_of_generated_graphics_used()
    estimated = properties.num_of_generated_graphics
    
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
