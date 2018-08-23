import pygame, variables, random
from pygame import draw
from random import randint
from Texture import Texture
from addtexture import addtexture
from pygame import Rect

dirtcolor = (70, 71, 14)
pathwidth = 16

def addroad(grasssurface, leftpath, rightpath, uppath, downpath):
    surface = grasssurface
    width = surface.get_width()
    height = surface.get_height()
    randcolor = (60, 61, randint(0, 50))
    randcolor2 = (randcolor[0]-10, randcolor[1]-10, randcolor[2])
    horizontaltop = int((height/2)-(pathwidth/2))
    verticalleft = int((width/2)-(pathwidth/2))

    fillrect = None
    if leftpath and rightpath:
        fillrect = pygame.Rect(0, horizontaltop, width, pathwidth)
    elif leftpath:
        fillrect = pygame.Rect(0, horizontaltop, int((width/2)+(pathwidth/2)), pathwidth)
    elif rightpath:
        fillrect = pygame.Rect(int((width/2)-(pathwidth/2)), horizontaltop, int((width/2)+(pathwidth/2)), pathwidth)

    if fillrect != None:
        surface.fill(dirtcolor, fillrect)
        
        extendingtexture = Texture(dirtcolor, 1/25, 0.8, 0.8)
        extendingtexture.bounds = [fillrect.x, horizontaltop-3, fillrect.width, 3]
        extendingtexture.texturingbounds = [fillrect.x, horizontaltop-1, fillrect.width, 1]
        addtexture(surface, extendingtexture)

        extendingtexture = Texture(dirtcolor, 1/25, 0.8, 1/30)
        extendingtexture.bounds = [fillrect.x, horizontaltop+pathwidth, fillrect.width, 3]
        extendingtexture.texturingbounds = [fillrect.x, horizontaltop+pathwidth, fillrect.width, 1]
        addtexture(surface, extendingtexture)
    
        horizontaltexture = Texture(randcolor, 1/15, 1/3, 1/5, acceptedcolors=[dirtcolor])
        horizontaltexture2 = Texture(randcolor2, 1/20, 1/40, 1/40, acceptedcolors=[dirtcolor])
        horizontaltexture.bounds = [fillrect.x, horizontaltop-1, fillrect.width, pathwidth+2]
        horizontaltexture2.bounds = horizontaltexture.bounds
        addtexture(surface, horizontaltexture)
        addtexture(surface, horizontaltexture2)

    fillrect = None
    if uppath and downpath:
        fillrect = Rect(verticalleft, 0, pathwidth, height)
    elif uppath:
        fillrect = Rect(verticalleft, 0, pathwidth, int(height/2))
    elif downpath:
        fillrect = Rect(verticalleft, int(height/2), pathwidth, int(height/2))

    if fillrect != None:
        surface.fill(dirtcolor, fillrect)
        
        extendingtexture = Texture(dirtcolor, 1/25, 1/30, 0.8)
        extendingtexture.bounds = [verticalleft-3, fillrect.y, 3, fillrect.height]
        extendingtexture.texturingbounds = [verticalleft-1, fillrect.y, 1, fillrect.height]
        addtexture(surface, extendingtexture)
        
        extendingtexture = Texture(dirtcolor, 1/25, 1/30, 0.8)
        extendingtexture.bounds = [verticalleft+pathwidth, fillrect.y, 3, fillrect.height]
        extendingtexture.texturingbounds = [verticalleft+pathwidth, fillrect.y, 1, fillrect.height]
        addtexture(surface, extendingtexture)
        
        verticaltexture = Texture(randcolor, 1/15, 1/5, 1/3, acceptedcolors=[dirtcolor])
        verticaltexture2 = Texture(randcolor2, 1/20, 1/40, 1/40, acceptedcolors=[dirtcolor])
        verticaltexture.bounds = [verticalleft-1, fillrect.y, pathwidth+2, fillrect.height]
        verticaltexture2.bounds = verticaltexture.bounds
        addtexture(surface, verticaltexture)
        addtexture(surface, verticaltexture2)
    
    return surface

def makepatch(randomcolorsunsorted, width, height):
    def brightness(color):
        return color[0] + color[1] + color[2]
    randomcolors = sorted(randomcolorsunsorted, key=brightness)
    s = pygame.Surface([width, height], pygame.SRCALPHA)
    # randomcolors should be sorted in order of drawing, brightest is texture 3
    texture1 = Texture(randomcolors[0], 1/13, 1/10, 9/20)
    texture2 = Texture(randomcolors[1], 1/13, 1/10, 9/20)
    texture3 = Texture(randomcolors[2], 1/9, 1/10, 9/20)
    textures = [texture1, texture2, texture3]
    for t in textures:
        t.greenvarianceperspawn = 8
        t.addupq = True
        t.adddownq = False
        t.pickonedirp = True
        # skip first couple pixels
        t.texturingbounds = [0, 2, width-2, height-2]
        t.distruibution = "geometric"
        t.xinvisiblechance = 1/4
        t.yinvisiblechance = 1/4
        addtexture(s, t)
    # blue rect for seeing where pathes are
    #pygame.draw.rect(s, variables.BLUE, Rect(0,0,width,height), 1)
    return s

def makegrassland(width, height, leftpath = True, rightpath = True, uppath = True, downpath = True):
    patchwidth = randint(15, 30)
    patchheight = randint(15, 30)
    patches = []
    numofpatches = randint(5, 10)

    pinkmodeonq = False
    if random.random() < 0.005:
        pinkmodeonq = True


    def randompink():
        return (randint(140, 255), randint(0, 100), randint(150, 255))
    
    randomgreens = [randint(75, 150), randint(75, 150), randint(75, 150)]
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
        ypos += patchheight + randint(-spacingvariability, -int(spacingvariability/3))

    surface = addroad(surface, leftpath, rightpath, uppath, downpath)
        
    return surface

def makesnowland(width, height):
    surface = pygame.Surface([width, height], pygame.SRCALPHA)
    surface.fill((210, 210, 210))
    return surface
