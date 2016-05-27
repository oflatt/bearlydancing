import pygame, ctypes

# Setup
pygame.init()

#master clock
current_time = 0

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()
ctypes.windll.user32.SetProcessDPIAware()
mode = modes[0]
height = mode[1]#displayinfo.current_h - 200
width = height #for not it is a square window
hh = height/2
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
wide_screen = pygame.display.set_mode(mode, pygame.FULLSCREEN)
screen = pygame.Surface([height, width])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 255, 0)

#state can be world, battle, or conversation
state = "world"

#general
scaleoffset = 1
fontlist = pygame.font.get_fonts()
fontname = "use default"
if "orangekidregular" in fontlist:
    fontname = "orangekidregular"
font = pygame.font.SysFont(fontname, 30)

#battle
healthanimationspeed = 2000#time in milliseconds for the health bar animation to go
expanimationspeed = 3000
dancespeed = height/8 * 0.001#factor for displaying notes
perfect_range = height/25
good_range = height/20
ok_range = height/15
miss_range = height/10
notes_colors = [ORANGE, BLUE, RED, GREEN, GREEN, RED, BLUE, ORANGE]

#conversation
textbox_height = height*1/4
photo_size = width/6

#world
playerspeed = height/800 * 0.15 #factor against time
#encountering enemies
encounter_check_rate = 100 #rate of check in milliseconds
encounter_chance = 0.0025#chance per check

#keybindings
enterkeys = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]
note1keys = [pygame.K_a]
note2keys = [pygame.K_s]
note3keys = [pygame.K_d]
note4keys = [pygame.K_f]
note5keys = [pygame.K_j]
note6keys = [pygame.K_k]
note7keys = [pygame.K_l]
note8keys = [pygame.K_SEMICOLON]