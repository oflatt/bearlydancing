import pygame, variables, random, addtexture
from pygame import draw
from random import randint
from Texture import Texture

def makepatch(randomcolorsunsorted, width, height):
    def brightness(color):
        return color[0] + color[1] + color[2]
    randomcolors = sorted(randomcolorsunsorted, key=brightness)
    s = pygame.Surface([width, height], pygame.SRCALPHA)
    # randomcolors should be sorted in order of drawing
    texture1 = Texture(randomcolors[0], 1/15, 2/5, 2/5)
    texture2 = Texture(randomcolors[1], 1/30, 2/5, 2/5)
    texture3 = Texture(randomcolors[2], 1/60, 2/5, 2/5)
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
    numofpatches = randint(5, 10)

    pinkmodeonq = True

    def randompink():
        return (randint(140, 255), randint(0, 100), randint(150, 255))
    
    randomgreens = [randint(80, 170), randint(80, 170), randint(80, 170)]
    randomgreens = sorted(randomgreens, key=int)

    
    randomcolors = []
    if pinkmodeonq:
        randomcolors = [randompink(), randompink(), randompink()]
    else:
        for x in range(3):
            randomcolors.append((round(randomgreens[x]/3), randomgreens[x], 8))

    for x in range(numofpatches):
        patches.append(makepatch(randomcolors, patchwidth, patchheight))
    surface = pygame.Surface([width, height], pygame.SRCALPHA)
    if pinkmodeonq:
        backgroundcolor = (255, 119, 228)
    else:
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
