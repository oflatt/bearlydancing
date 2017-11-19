import pygame, variables, copy, random, rdrawland
from addtexture import addtexture, fillpolygon
from pygame import draw
from random import randint
from Texture import Texture
from variables import TREEWIDTH, TREEHEIGHT

TREEFILLCOLOR = (33, 52, 27, 255)
TREEOUTLINECOLOR = (22, 40, 20)
TRUNKCOLOR = (39, 32, 32, 255)

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


def drawlayer(p, yoffset, leftbound, rightbound, istoplayer=False):
    boundwidth = rightbound - leftbound
    halflen = int((rightbound - leftbound) / 2) - 1
    middlebound = halflen + leftbound
    spikelower = 108 + yoffset
    spikeupper = 92 + yoffset
    spikewmin = 4
    spikewmax = 8
    # highest point unless istoplayer is true
    topy = 65 + yoffset

    # starts with a lower point
    rightpoints = [[middlebound, randint(100 + yoffset, spikelower)]]

    drawingspikesq = True
    spikex = middlebound
    while drawingspikesq:
        spikex += randint(spikewmin, spikewmax)
        if (spikex >= rightbound):
            spikex = rightbound - 1
        rightpoints.append([spikex, randint(spikeupper, 100 + yoffset)])

        spikex += randint(spikewmin, spikewmax)
        if (spikex >= (rightbound - spikewmin - 1)):
            break
        rightpoints.append([spikex, randint(100 + yoffset, spikelower)])

    fourth = int(boundwidth / 4)
    if istoplayer:
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
    # now the lest
    drawingspikesq = True
    spikex = middlebound
    while drawingspikesq:
        spikex -= randint(spikewmin, spikewmax)
        if (spikex < leftbound):
            spikex = leftbound
        leftpoints.append([spikex, randint(spikeupper, 100 + yoffset)])

        spikex -= randint(spikewmin, spikewmax)
        if (spikex <= leftbound + spikewmin):
            break
        leftpoints.append([spikex, randint(100 + yoffset, spikelower)])

    rightpoints.extend(leftpoints[::-1])
    # Then call a function that randomly adds new points for complexity
    rightpoints = addpoints(rightpoints, leftbound, rightbound, 4)
    rightpoints = addpoints(rightpoints, leftbound, rightbound, 2)

    startingpoint = [middlebound, int((100 + yoffset - topy) / 2) + topy]
    insidecolorbefore = p.get_at(startingpoint)
    draw.polygon(p, TREEOUTLINECOLOR, rightpoints, 1)  # outline

    fillpolygon(p, startingpoint, TREEFILLCOLOR, [insidecolorbefore],
                fillbounds= [leftbound, 0, rightbound-leftbound, TREEHEIGHT])


def drawtrunk(surface):
    midpoint = int(TREEWIDTH / 2)
    halfh = int(TREEHEIGHT / 2)
    bottom = TREEHEIGHT - 1

    pl = [[0, 0],
          [3, -1],
          [7, -2],
          [10, -4],
          [12, -8],
          [10, -12],
          [7, -15],
          [7, -halfh]]

    reversepl = copy.deepcopy(pl)
    reversepl = reversepl[::-1]
    for x in reversepl:
        x[0] = -x[0]
    pl.extend(reversepl)

    # center it at the right place
    for x in pl:
        x[0] += midpoint
        x[1] += bottom

    def changeamount(p, changedir):
        # this is so that if it changes towards the center, it changes much less,prevents trees with empty regions
        if p[0] > midpoint:
            if changedir < 0:
                a = randint(1, 2) * changedir
            else:
                a = randint(3, 8) * changedir
        else:
            if changedir < 0:
                a = randint(3, 8) * changedir
            else:
                a = randint(1, 2) * changedir
        return a


    pl = addpoints(pl, 0, TREEWIDTH, 1)
    # variation- x positions first
    for x in range(len(pl)):
        if randint(1, 4) == 1:
            changedir = random.choice([-1, 1])
            pl[x][0] += changeamount(pl[x], changedir)
            a = 1
            while randint(1, 3) > 1:
                pl[(x + a) % len(pl)][0] += changeamount(pl[(x + a) % len(pl)], changedir)
                a += 1

    draw.polygon(surface, TRUNKCOLOR, pl)

def maketree():
    p = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l2 = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l3 = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    l4 = pygame.Surface([TREEWIDTH, TREEHEIGHT], pygame.SRCALPHA)
    p.fill([255, 255, 255, 0])
    l.fill([255, 255, 255, 0])
    l2.fill([255, 255, 255, 0])
    l3.fill([255, 255, 255, 0])
    l4.fill([255, 255, 255, 0])

    treeshortener = randint(0, 15)
    if randint(0, 5) < 1:
        treeshortener += randint(0, 10)
    
    drawtrunk(p)

    yoffset = randint(30, 40) + treeshortener
    if randint(0, 8) > 0:
        drawlayer(l, yoffset, 0, TREEWIDTH)
    yoffset += randint(-25, -15)
    drawlayer(l2, yoffset, 5, TREEWIDTH - 5)
    yoffset += randint(-25, -15)
    drawlayer(l3, yoffset, 10, TREEWIDTH - 10)
    yoffset += randint(-25, -15)
    drawlayer(l4, yoffset, 15, TREEWIDTH - 15, True)

    p.blit(l, [0, 0])
    p.blit(l2, [0, 0])
    p.blit(l3, [0, 0])
    p.blit(l4, [0, 0])

    # first texturize the green part of the tree
    moss1 = Texture((26, 47, 21), 1/12, 1/21, 4/7, acceptedcolors = [TREEFILLCOLOR])
    moss2 = Texture((28, 63, 12), 1/70, 1/21, 4/7, acceptedcolors = [TREEFILLCOLOR])
    moss3 = Texture((28, 61, 33), 1/70, 0, 0, acceptedcolors = [TREEFILLCOLOR])

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
