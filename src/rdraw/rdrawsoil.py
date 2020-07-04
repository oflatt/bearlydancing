import pygame, random, math
from pygame import Rect

from .pointlist import listarc
from variables import brighten, randomnicecolor


dirtcolor = brighten((89, 55, 15), -10)
# a "pot" is just a lump on the ground to grow stuff in
def drawpot(potwidth):
    potcolor = brighten(randomnicecolor(), -100)
    
    potheight = int(potwidth*1.5)
    
    surface = pygame.Surface((potwidth+1, potheight+1), pygame.SRCALPHA)
    midx = (potwidth/2)
    rimheight = potheight/2

    toparc = listarc(0, rimheight/2, potwidth, rimheight/2, int(potwidth))
    toparclowered = []
    for i in range(len(toparc)):
        toparclowered.append(toparc[i].copy())
        toparclowered[i][1] += 2

    bottomarc = listarc(potwidth, rimheight/2, -potwidth, -rimheight/2, int(potwidth))

    #for i in range(len(bottomarc)):
    #    bottomarc[i][1] = math.ceil(bottomarc[i][1])
    
    rim = toparc + bottomarc

    for i in range(len(rim)):
        rim[i][0] = round(rim[i][0])



    basearc = listarc(potwidth/6, potheight-1-rimheight/2, potwidth-2*potwidth/6, -rimheight/6, int(potwidth))
    baselist = [bottomarc[2], bottomarc[-3]] + basearc
    # draw the base of the pot
    pygame.gfxdraw.filled_polygon(surface, baselist, brighten(potcolor, 20))

    # draw the inside of pot
    pygame.gfxdraw.filled_polygon(surface, rim, potcolor)
    # draw soil
    pygame.gfxdraw.filled_polygon(surface, toparclowered+bottomarc, dirtcolor)
    # draw rim of pot
    pygame.gfxdraw.polygon(surface, rim, brighten(potcolor, 30))

    return surface


