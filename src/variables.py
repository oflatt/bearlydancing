import pygame, ctypes
from Settings import Settings

# Setup
pygame.mixer.pre_init(22050, -16, 2, 64)
pygame.mixer.init()
pygame.init()
pygame.mixer.set_num_channels(46)

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()
ctypes.windll.user32.SetProcessDPIAware()
mode = modes[0]
height = mode[1]#displayinfo.current_h - 200
width = height #for not it is a square window
hh = height/2
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF | pygame.HWSURFACE
wide_screen = pygame.display.set_mode(mode, flags)
screen = pygame.Surface([height, width])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)

#general
scaleoffset = 1
fontlist = pygame.font.get_fonts()
fontname = "use default"
if "orangekidregular" in fontlist:
    fontname = "orangekidregular"
font = pygame.font.SysFont(fontname, 30)
newworldeachloadq = True

#pinetreesused is used to keep track of how many randomly generated trees have been made
pinetreesused = 0

#battle
healthanimationspeed = 2000#time in milliseconds for the health bar animation to go
expanimationspeed = 3000
dancespeed = height/8 * 0.001#factor for displaying notes
padypos = height*(13/16)

generic_specs = {'maxtime' : 20, 'lv' : 0, 'rules' : []}
melodic_specs = {'maxtime' : 20, 'lv' : 0, 'rules' : ['melodic']}
maxvalue = 14
minvalue = -7

perfect_value = 2
good_value = 1
ok_value = 0.6
miss_value = 0
perfect_range = height/100
good_range = height/60
ok_range = height/25
miss_range = height/15

battle_volume = 0.25

notes_colors = [ORANGE, BLUE, RED, GREEN, GREEN, RED, BLUE, ORANGE]

#conversation
textbox_height = height*1/4
photo_size = width/6

#world
playerspeed = height/800 * 0.1 #factor against time
#encountering enemies
encounter_check_rate = 100 #rate of check in milliseconds
encounter_chance = 0.0025#chance per check

settings = Settings()

#helpful functions
def smaller(a, b):
    if a<b:
        return a
    else:
        return b
