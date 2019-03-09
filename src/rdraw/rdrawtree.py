import pygame, variables, copy, random, math
import pygame.gfxdraw
from .addtexture import addtexture
from .rdrawrock import addlump
from random import randint
from .Texture import Texture
from variables import TREEWIDTH, TREEHEIGHT

TREEFILLCOLOR = (33, 52, 27, 255)
TREEOUTLINECOLOR = (22, 40, 20)
TRUNKCOLOR = (39, 32, 32, 255)
TREECOLOR1 = (26, 47, 21)
TREECOLOR2 = (28, 63, 12)
TREECOLOR3 = (28, 61, 33)
TOPTREECOLORLIST = [TREEFILLCOLOR[:3], TREEOUTLINECOLOR, TREECOLOR1, TREECOLOR2, TREECOLOR3]

def addpoints(l, leftbound, rightbound, maxvariation):
    cl = copy.deepcopy(l)
    length = len(l)
    x = 0
    while x < length:
        p = cl[x]
        nextp = cl[(x + 1) % length]
        # chance to add a point in between two points
        if randint(1, 3) == 1:
            variationpoint = [p[0] + int((nextp[0] - p[0]) / 2), p[1] + int((nextp[1] - p[1]) / 2)]
            variationpoint[0] += randint(-maxvariation, maxvariation)
            variationpoint[1] += randint(-maxvariation, maxvariation)
            if (variationpoint[0] < leftbound):
                variationpoint[0] = leftbound
            if (variationpoint[0] >= rightbound):
                variationpoint[0] = rightbound - 1

            cl.insert(x + 1, variationpoint)
            # add one to x and length because the length changes
            x += 1
            length += 1

        x += 1

    return cl

def tuplenumberadd(t, number):
    l = [None,] * len(t)
    for a in range(len(t)):
        l[a] = t[a] + number
    return tuple(l)

def snowclump(surfacefinal, x, y, addrad = False, groundp = False):
    basecolor = variables.snowcolor
    if groundp:
        basecolor = (basecolor[0]-3, basecolor[1]-3, basecolor[2]-3)
    swidth = 76
    surface = pygame.Surface([swidth, swidth], pygame.SRCALPHA)
    fillcolor = (basecolor[0]-10, basecolor[1]-10, basecolor[2]-10)
    
    numofpoints = 15
    points = []
    radius = randint(4, 11)
    if groundp:
        radius = radius * 2
    for t in range(numofpoints):
        radians = (t/numofpoints)*2*math.pi
        xpos = (radius+1.5)*math.cos(radians)
        ypos = radius*math.sin(radians)
        points.append([xpos, ypos])

    # squish bottom
    addlump(points, int(numofpoints/2), numofpoints, randint(4, 5))
    
    numoflumps = randint(1, 3)
    for nonused in range(numoflumps):
        addtoy = True
        lumplength = randint(int(numofpoints/5), int(numofpoints/2))
        startpoint = randint(-1, int(numofpoints/2)+2-lumplength)
        if randint(0, 4) == 1:
            addtoy = False
            startpoint = randint(-int(numofpoints/5), int(numofpoints/2)+int(numofpoints/5)-lumplength)
        addlump(points, startpoint, startpoint + lumplength, randint(1, 4), addtoy)

    shadowthreshold = radius*2/3
    # get bottom points for the shadow
    shadowpoints = []
    for p in points:
        if p[1] > shadowthreshold:
            shadowpoints.append((p[0], p[1]))
    shadowcolor = (basecolor[0]-20, basecolor[1]-20, basecolor[2]-20)
    shadowfillcolor = tuplenumberadd(shadowcolor, -10)
    if groundp:
        shadowcolor = tuplenumberadd(fillcolor, 0)
        shadowfillcolor = tuplenumberadd(shadowcolor, 0)
    
        
    tallest = 1
    for p in points:
        if -p[1] > tallest:
            tallest = -p[1]
    primarys = shadowpoints.copy()
    if len(shadowpoints) > 0:
        shadowr = shadowpoints[0][0]
        for i in range(len(primarys)):
            radians = (i/len(primarys))*math.pi
            xpos = primarys[len(primarys)-1-i][0]
            ypos = -math.sin(radians)*(tallest*1/3) + shadowthreshold
            shadowpoints.append((xpos, ypos))

    pointstranslated = []
    if addrad:
        y = y + radius
    for p in points:
        newpx = min(p[0]+swidth/2, swidth-1)
        newpy = min(p[1]+swidth/2, swidth-1)
        pointstranslated.append((newpx, newpy))
    shadowpointstranslated = []
    for p in shadowpoints:
        shadowpointstranslated.append((p[0]+swidth/2, p[1]+swidth/2))
    
    
    fillpoint = (int(swidth/2),swidth-1)
    while surface.get_at(fillpoint)[3] == 0 and fillpoint[1] > 0:
        fillpoint = (fillpoint[0], fillpoint[1]-1)
    while surface.get_at(fillpoint)[3] != 0 and fillpoint[1] > 0:
        fillpoint = (fillpoint[0], fillpoint[1]-1)
    
    pygame.gfxdraw.filled_polygon(surface, pointstranslated, basecolor)

    if(len(shadowpoints)>1):
        
        pygame.gfxdraw.filled_polygon(surface, shadowpointstranslated, shadowfillcolor)
        pygame.gfxdraw.polygon(surface, shadowpointstranslated, shadowcolor)


    # draw outline of polygon
    pygame.gfxdraw.polygon(surface, pointstranslated, basecolor)
    surfacefinal.blit(surface, [x-swidth/2, y-swidth/2])
    

def drawlayer(p, yoffset, leftbound, rightbound, toplayerp=False, addsnowp = False):
    boundwidth = rightbound - leftbound
    bottomcurveamount = boundwidth/6
    halflen = int((rightbound - leftbound) / 2) - 1
    middlebound = halflen + leftbound
    spikelower = 108 + yoffset
    spikeupper = 92 + yoffset
    spikewmin = 4
    spikewmax = 8
    # highest point unless toplayerp is true
    topy = 65 + yoffset

    # add some dip to points closer to center
    def spikeyoffset(pointxpos):
        return int(yoffset + math.sin((pointxpos - leftbound)/boundwidth * math.pi) * bottomcurveamount - bottomcurveamount/2)

    # starts with a lower point
    rightpoints = [[middlebound, randint(100 + yoffset, spikelower)]]

    # add the spikes on the right side
    drawingspikesq = True
    spikex = middlebound
    while drawingspikesq:
        # add higher point- higher points cropped while lower points break
        spikex += randint(spikewmin, spikewmax)
        if (spikex >= rightbound):
            spikex = rightbound - 1
        rightpoints.append([spikex, randint(spikeupper+spikeyoffset(spikex)-yoffset, 100 + spikeyoffset(spikex))])

        # add lower point
        spikex += randint(spikewmin, spikewmax)
        if (spikex >= (rightbound - spikewmin - 1)):
            break
        rightpoints.append([spikex, randint(100 + spikeyoffset(spikex), spikelower+spikeyoffset(spikex)-yoffset)])

    # now add the top of the layer after the bottom is done
    fourth = int(boundwidth / 4)
    if toplayerp:
        # with the top layer, it's taller and has points in the middle
        rightpoints.extend(
            [[rightbound - fourth, 70 + yoffset],
             [middlebound + randint(0, fourth), randint(52, 65) + yoffset],
             [middlebound + randint(-fourth, 0), randint(52, 65) + yoffset],
             [leftbound + fourth, 70 + yoffset]])
    else:
        rightpoints.extend(
            [[rightbound - fourth, topy], [leftbound + int(boundwidth / 4), topy]])

    leftpoints = []
    # now the left side of the bottom spikey bit
    drawingspikesq = True
    spikex = middlebound
    while drawingspikesq:
        spikex -= randint(spikewmin, spikewmax)
        if (spikex < leftbound):
            spikex = leftbound
        leftpoints.append([spikex, randint(spikeupper+spikeyoffset(spikex)-yoffset, 100 + spikeyoffset(spikex))])

        spikex -= randint(spikewmin, spikewmax)
        if (spikex <= leftbound + spikewmin):
            break
        # add spikeyoffset but subtract yoffset because spikelower already had it added on
        leftpoints.append([spikex, randint(100 + spikeyoffset(spikex), spikelower+ spikeyoffset(spikex)-yoffset)])

    rightpoints.extend(leftpoints[::-1])
    # Then call a function that randomly adds new points for complexity
    rightpoints = addpoints(rightpoints, leftbound, rightbound, 4)
    rightpoints = addpoints(rightpoints, leftbound, rightbound, 2)

    startingpoint = [middlebound, int((100 + yoffset - topy) / 2) + topy]
    insidecolorbefore = p.get_at(startingpoint)
    
    
    pygame.gfxdraw.filled_polygon(p, rightpoints, TREEFILLCOLOR)
    pygame.gfxdraw.polygon(p, rightpoints, TREEOUTLINECOLOR)

    if addsnowp:
        for tpoint in rightpoints:
            if(tpoint[1] > 100+yoffset and tpoint[1]<spikelower and tpoint[0] > leftbound+fourth/2 and tpoint[0] < rightbound - fourth/2):
                if randint(0, 4) == 0:
                    snowclump(p, tpoint[0], tpoint[1])
        if toplayerp: # add snow cap sometimes
            if(randint(0, 2) < 2):
                snowclump(p, middlebound + randint(int(-fourth*2/3), int(fourth*2/3)), randint(52, 65)+yoffset+4, addrad = True)


def drawtrunk(surface):
    midpoint = int(TREEWIDTH / 2)
    halfh = int(TREEHEIGHT / 2)
    bottom = TREEHEIGHT - 1
    # if changechance is 4, it means each point has a 1 in 4 chance of being varied
    changechance = 4

    def changeamount(p, minimum = 2, maximum = 6):
        changedir = 1
        a = 0
        if len(p) == 2:
            a = randint(2, maximum+1)
        return a

    def changedir(p):
        dir = 1
        if p[0]<midpoint:
            dir = -1
        elif int(p[0]) == midpoint:
            dir = random.choice([-1,1])
        return dir
    
    pl = [[0, 0],
          [3, -1],
          [7, -2],
          [10, -4],
          [12, -8],
          [10, -12],
          [7, -15, "unchanging"], #unchanging tag means that changeamount returns 0
          [7, -halfh]]

    reversepl = copy.deepcopy(pl)

    # now alter the unchanging one, the top of the base
    def basechange(halflist, midoffset = 1):
        if randint(0, changechance) == 0:
            changea = changeamount([midpoint+midoffset, 0], maximum = 4)
            for x in range(len(pl)-1):
                halflist[x][0] += changea
                
    basechange(pl)
    basechange(reversepl, -1)

    reversepl = reversepl[::-1]
    for x in reversepl:
        x[0] = -x[0]
    pl.extend(reversepl)

    # center it at the right place
    for x in pl:
        x[0] += midpoint
        x[1] += bottom

    pl = addpoints(pl, 0, TREEWIDTH, 1)

    # variation
    for x in range(len(pl)):
        if randint(0, changechance) == 0:
            pullamount = changeamount(pl[x])
            pl[x][0] += pullamount * changedir(pl[x])
            a = 1
            while randint(0, 2) > 0:
                followpoint = pl[(x + a) % len(pl)]
                if not len(followpoint) > 2:
                    followpoint[0] += pullamount * changedir(followpoint)
                    a += 1

    for i in range(len(pl)):
        if len(pl[i]) > 2:
            pl[i] = pl[i][:2]
    pygame.gfxdraw.filled_polygon(surface,  pl,TRUNKCOLOR)

def maketree(snowp = False):
    p = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l2 = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l3 = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l4 = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    
    treeshortener = randint(0, 15)
    if randint(0, 5) < 1:
        treeshortener += randint(0, 10)
    
    drawtrunk(p)
    
    yoffset = randint(30, 40) + treeshortener
    if randint(0, 8) > 0:
        drawlayer(l, yoffset, 0, TREEWIDTH, addsnowp = False)
    yoffset += randint(-25, -15)
    drawlayer(l2, yoffset, 5, TREEWIDTH - 5, addsnowp = snowp)
    yoffset += randint(-25, -15)
    drawlayer(l3, yoffset, 10, TREEWIDTH - 10, addsnowp = snowp)
    yoffset += randint(-25, -15)
    drawlayer(l4, yoffset, 15, TREEWIDTH - 15, True, snowp)

    p.blit(l, [0, 0])
    p.blit(l2, [0, 0])
    p.blit(l3, [0, 0])
    p.blit(l4, [0, 0])
    
    # first texturize the green part of the tree
    moss1 = Texture(TREECOLOR1, 1/12, 1/21, 4/7, acceptedcolors = [TREEFILLCOLOR])
    moss2 = Texture(TREECOLOR2, 1/70, 1/21, 4/7, acceptedcolors = [TREEFILLCOLOR])
    moss3 = Texture(TREECOLOR3, 1/70, 0, 0, acceptedcolors = [TREEFILLCOLOR])

    if randint(1, 3) == 1:
        moss1.color = (randint(22, 28), randint(55, 65), randint(10, 25))
    addtexture(p, moss1)
    addtexture(p, moss2)
    addtexture(p, moss3)
    
    # then texture the bark
    bark1 = Texture((46, 35, 35), 1/40, 1/160, 18/20, acceptedcolors = [TRUNKCOLOR])
    bark2 = Texture((45, 32, 32), 1/100, 1/160, 18/20, acceptedcolors = [TRUNKCOLOR])
    bark1.xinvisiblechance = 1
    bark2.xinvisiblechance = 1

    if randint(1, 10) == 1:
        bark1.color = (randint(30, 45), randint(30, 45), randint(30, 45))
    addtexture(p, bark1)
    addtexture(p, bark2)

    # then chance to add moss to tree
    if randint(1, 9) == 1:
        moss1.color = (randint(22, 28), randint(45, 65), randint(10, 25))
        moss1.acceptedcolors = [TRUNKCOLOR]
        moss2.acceptedcolors = [TRUNKCOLOR]
        moss3.acceptedcolors = [TRUNKCOLOR]
        addtexture(p, moss1)
        addtexture(p, moss2)
        addtexture(p, moss3)

    return p


def makechristmastree(surface):
    christmascolors = [variables.LIGHTYELLOW, variables.GREEN, variables.RED, variables.LIGHTBLUE]
    if randint(0, 3) == 0:
        christmascolors = [random.choice(christmascolors)]
    w = surface.get_width()
    h = surface.get_height()
    lightxspacing = 5
    lightyspacing = 16
    curvedepth = 8
    numoflightsperrow = int(w/lightxspacing)
    numofrows = int(TREEHEIGHT/lightyspacing)-1

    def inboundsp(xpos, ypos):
        return xpos >= 0 and xpos< surface.get_width() and ypos>=0 and ypos<surface.get_height()
    
    def addpixel(xpos, ypos, color):
        if inboundsp(xpos, ypos):
            surface.set_at([xpos, ypos], color)
    
    def addlight(xpos, ypos):
        ypos += random.choice([0,-1,1])
        if inboundsp(xpos, ypos):
            if surface.get_at([xpos, ypos])[:3] in TOPTREECOLORLIST:
                rcolor = random.choice(christmascolors)
                #center pixel
                surface.set_at([xpos, ypos], rcolor)
                rcolor = (abs(rcolor[0]-10), abs(rcolor[1]-10), abs(rcolor[2]-10),150)
                addpixel(xpos-1, ypos, rcolor)
                addpixel(xpos+1, ypos, rcolor)
                addpixel(xpos, ypos+1, rcolor)
                addpixel(xpos, ypos-1, rcolor)

    def drawstring(yoffset):
        for lightindex in range(numoflightsperrow):
            xpos = lightindex * lightxspacing
            radians = math.pi * (lightindex/numoflightsperrow)
            curveoffset = math.sin(radians)
            curveoffset = curvedepth * curveoffset
            addlight(int(xpos), int(yoffset+curveoffset-lightindex))
    
    for y in range(numofrows):
        drawstring(y*lightyspacing)
