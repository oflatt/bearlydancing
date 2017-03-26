import pygame, variables, copy, random
from pygame import draw
from random import randint

TREEWIDTH = 100
TREEHEIGHT = 200
TREEFILLCOLOR = (33, 52, 27, 255)
TREEOUTLINECOLOR = (22, 40, 20)
TRUNKCOLOR = (39, 32, 32, 255)


def pointinbounds(p):
    return p[0] >= 0 and p[0] < TREEWIDTH and p[1] >= 0 and p[1] < TREEHEIGHT


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

    startingpoint = [middlebound, int((100 + yoffset - topy) / 2) + topy]
    insidecolorbefore = p.get_at(startingpoint)
    draw.polygon(p, TREEOUTLINECOLOR, rightpoints, 1)  # outline

    # fills a polygon with a point in the polygon
    def fillpolygon(s, firstpoint):
        pointlist = [firstpoint]

        while len(pointlist) != 0:
            point = pointlist.pop(0)
            s.set_at(point, TREEFILLCOLOR)
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
        # this is so that if it changes towards the center, it changes much less (prevents trees with empty regions
        if p[0] > midpoint:
            if changedir < 0:
                a = randint(1, 3) * changedir
            else:
                a = randint(3, 10) * changedir
        else:
            if changedir < 0:
                a = randint(3, 10) * changedir
            else:
                a = randint(1, 3) * changedir
        return a

    pl = addpoints(pl, 0, TREEWIDTH, 3)
    # variation- x positions first
    for x in range(len(pl)):
        if randint(1, 5) == 1:
            changedir = random.choice([-1, 1])
            pl[x][0] += changeamount(pl[x], changedir)
            a = 1
            while randint(1, 3) > 1:
                pl[(x + a) % len(pl)][0] += changeamount(pl[(x + a) % len(pl)], changedir)
                a += 1

    draw.polygon(surface, TRUNKCOLOR, pl)


#specialtextures is a list of colors to use instead of the normal ones
def texturepoint(surface, x, y, searchcolor, type, specialtextures):
    moss1 = (28, 61, 33)
    moss2 = (26, 47, 21)
    moss3 = (28, 63, 12)
    bark1 = (45, 32, 32)
    bark2 = (46, 35, 35)

    def patchoftexturechance(t, defaultchance, xcfactor, ycfactor):
        points = [[x, y]]
        while len(points) > 0:
            p = points.pop(0)
            if pointinbounds(p):
                if surface.get_at(p) == searchcolor:
                    chance = defaultchance
                    if p[0] != x:
                        chance *= xcfactor
                    if p[1] != y:
                        chance *= ycfactor

                    if random.random() <= 1/chance:
                        surface.set_at(p, t)
                        # then go again on the points to the side and the one below
                        points.extend([[p[0], p[1] + 1], [p[0] - 1, p[1]], [p[0] + 1, p[1]]])

    if surface.get_at([x, y]) == searchcolor:
        if type == "moss":
            if randint(1, 80) == 1:
                surface.set_at([x, y], moss1)
            elif randint(1, 10) == 1:
                patchoftexturechance(moss3, 7, 3, 1/4)
            else:
                if specialtextures != None:
                    patchoftexturechance(specialtextures[0], 7, 3, 1 / 4)
                else:
                    patchoftexturechance(moss2, 7, 3, 1/4)
        if type == "bark":
            if randint(1, 5) == 1:
                patchoftexturechance(bark1, 20, 8, 1/18)
            elif randint(1, 2) == 1:
                if specialtextures != None:
                    patchoftexturechance(specialtextures[0], 20, 8, 1/18)
                else:
                    patchoftexturechance(bark2, 20, 8, 1 / 18)

def texturerow(surface, y, searchcolor, type, specialtextures):
    for x in range(surface.get_width()):
        texturepoint(surface, x, y, searchcolor, type, specialtextures)

#type is a string that refers to a set of textures and random patterns
def addtexture(surface, searchcolor, type, specialtextures = None):
    for y in range(surface.get_height()):
        texturerow(surface, y, searchcolor, type, specialtextures)


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

    p.blit(l, [0, 0])
    p.blit(l2, [0, 0])
    p.blit(l3, [0, 0])
    p.blit(l4, [0, 0])

    #chance for special texture
    if randint(1, 3) == 1:
        addtexture(p, TREEFILLCOLOR, "moss", [(randint(22, 28), randint(45, 65), randint(10, 25))])
    else:
        addtexture(p, TREEFILLCOLOR, "moss")

    #chance to add a different special texture
    if randint(1, 10) == 1:
        addtexture(p, TRUNKCOLOR, "bark", [(randint(30, 45), randint(30, 45), randint(30, 45))])
    else:
        addtexture(p, TRUNKCOLOR, "bark")

    # chance to add moss to tree
    if randint(1, 9) == 1:
        addtexture(p, TRUNKCOLOR, "moss", [(randint(22, 28), randint(45, 65), randint(10, 25))])

    p = pygame.transform.scale(p, [TREEWIDTH * 4, TREEHEIGHT * 4])
    surface.blit(p, [0, 0])
