import pygame

# Setup
pygame.init()

# Set the width and height of the screen [width,height]
displayinfo = pygame.display.Info()
height = 800#displayinfo.current_h - 200
hh = height/2
screen = pygame.display.set_mode([height, height])

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)