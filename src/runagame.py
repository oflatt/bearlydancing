import pygame

from polarinvaders.polarinvaders import creategame
import generategridgame.generategridgame

import pygame, ctypes, os, time

from Settings import Settings

# Setup
pygame.init()

#master clock
clock = pygame.time.Clock()

# Set the width and height of the screen [width,height]
modes = pygame.display.list_modes()

mode = modes[0]
height = mode[1]#displayinfo.current_h - 200
width = mode[0]
hh = height/2
flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
screen = pygame.display.set_mode(mode, flags)
running = True

fontlist = pygame.font.get_fonts()
fontname = "use default"
if "orangekidregular" in fontlist:
    fontname = "orangekidregular"
font = pygame.font.SysFont(fontname, 30)

game = generategridgame.generategridgame.creategame()

settings = Settings()

game.initfunction(settings, screen)

while running:
    time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            game.keydownfunction(time, settings, event.key)
        elif event.type == pygame.KEYUP:
            game.keyupfunction(time, settings, event.key)
        
    
    game.tickfunction(time, settings)
    game.drawfunction(time, settings, screen)
    
    pygame.display.flip()
    clock.tick(60)
