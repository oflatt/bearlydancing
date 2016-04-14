import pygame

# Setup
pygame.init()

# Set the width and height of the screen [width,height]
displayinfo = pygame.display.Info()
height =800#displayinfo.current_h - 200
width = height #for not it is a square window
hh = height/2
screen = pygame.display.set_mode([height, height])
scaleoffset = 1
font = pygame.font.Font(None, 30)

playerspeed = height/800 * 3

#state can be world, battle, or conversation
state = "world"

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)