import pygame, random
from pygame import Rect

from .pointlist import listarc
from variables import brighten

groundcolor = (140, 81, 35)

# a "pot" is just a lump on the ground to grow stuff in
def drawpot(potwidth):
    potheight = int(potwidth*1.5)
    
    surface = pygame.Surface((potwidth, potheight), pygame.SRCALPHA)
    midx = (potwidth/2)
    rimheight = potheight/3

    toparc = listarc(0, rimheight/2, potwidth, rimheight/2, int(potwidth))
    pygame.gfxdraw.polygon(surface, toparc, brighten(groundcolor, 40))

    return surface


