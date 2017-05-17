import pygame, variables, random, addtexture
from pygame import draw
from random import randint
from Texture import Texture

def makepatch(randomgreens, width, height):
    s = pygame.Surface([width, height], pygame.SRCALPHA)
    center = [round(s.get_width()/2), round(s.get_height()/2)]
    gr = sorted(randomgreens, key=int)
    # draw the colors on from darkest to lightest
    texture1 = Texture((round(gr[0]/3), gr[0], 8), 1/15, 2/5, 2/5)
    texture2 = Texture((round(gr[1]/3), gr[1], 8), 1/30, 2/5, 2/5)
    texture3 = Texture((round(gr[2]/3), gr[2], 8), 1/60, 2/5, 2/5)
    textures = [texture1, texture2, texture3]
    for t in textures:
        t.xinvisiblechance = 1/2
        t.yinvisiblechance = 1/2
        addtexture.addtexture(s, t)
    return s

def makegrassland(width, height):
    patchwidth = randint(15, 30)
    patchheight = randint(15, 30)
    patches = []
    numofpatches = randint(3, 6)
    gr = [randint(80, 170), randint(80, 170), randint(80, 170)]
    for x in range(numofpatches):
        patches.append(makepatch(gr, patchwidth, patchheight))
    surface = pygame.Surface([width, height], pygame.SRCALPHA)
    backgroundcolor = (77, 112, 30)
    surface.fill(backgroundcolor)

    # now add the patches to the land
    spacingvariability = round(patchwidth/4)
    def addrow(ypos):
        xpos = 0
        while xpos < surface.get_width():
            surface.blit(random.choice(patches), [xpos, ypos])
            xpos += patchwidth + randint(-spacingvariability, 0)

    ypos = 0
    while ypos < surface.get_height():
        addrow(ypos)
        ypos += patchheight + randint(-spacingvariability, 0)

    return surface
