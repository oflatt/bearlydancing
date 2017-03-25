import pygame, variables, copy
from pygame import draw
from random import randint

TREEWIDTH = 100
TREEHEIGHT = 200


def addpoints(l, leftbound, rightbound):
    maxvariation = 4
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
            # add one to x and lengthbecause the length changes
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
    outlinecolor = [22, 40, 20]
    fillcolor = [33, 52, 27]
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
        #with the top layer, it's taller and has points in the middle
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
    rightpoints = addpoints(rightpoints, leftbound, rightbound)
    print(rightpoints)

    startingpoint = [middlebound, int((100+yoffset - topy) / 2) + topy]
    insidecolorbefore = p.get_at(startingpoint)
    draw.polygon(p, outlinecolor, rightpoints, 1)  # outline

    # fills a polygon with a point in the polygon
    def fillpolygon(s, firstpoint):
        pointlist = [firstpoint]

        while len(pointlist) != 0:
            point = pointlist.pop(0)
            s.set_at(point, fillcolor)
            if (point[0] > 0):
                if (s.get_at([point[0] - 1, point[1]]) == insidecolorbefore):
                    pointlist.insert(0, [point[0] - 1, point[1]])
            if (point[0] < rightbound - 1):
                if (s.get_at([point[0] + 1, point[1]]) == insidecolorbefore):
                    pointlist.insert(0, [point[0] + 1, point[1]])
            if (point[1] > 0):
                if (s.get_at([point[0], point[1] - 1]) == insidecolorbefore):
                    pointlist.insert(0, [point[0], point[1] - 1])
            if (point[1] < s.get_height() - 1):
                if (s.get_at([point[0], point[1] + 1]) == insidecolorbefore):
                    pointlist.insert(0, [point[0], point[1] + 1])

    fillpolygon(p, startingpoint)

def drawtrunk(surface):
    surface.fill([39, 32, 32, 255], [int(TREEWIDTH/2)-7, int(TREEHEIGHT/2), 14, int(TREEHEIGHT/2)])

def drawtree(surface):
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

    drawtrunk(p)

    yoffset = randint(30, 40)
    drawlayer(l, yoffset, 0, TREEWIDTH)
    yoffset += randint(-25, -15)
    drawlayer(l2, yoffset, 5, TREEWIDTH - 5)
    yoffset += randint(-25, -15)
    drawlayer(l3, yoffset, 10, TREEWIDTH - 10)
    yoffset += randint(-25, -15)
    drawlayer(l4, yoffset, 15, TREEWIDTH - 15, True)

    p.blit(l, [0,0])
    p.blit(l2, [0, 0])
    p.blit(l3, [0, 0])
    p.blit(l4, [0, 0])

    p = pygame.transform.scale(p, [TREEWIDTH * 4, TREEHEIGHT * 4])
    surface.blit(p, [0, 0])
