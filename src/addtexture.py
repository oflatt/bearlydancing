import random, pygame, time
from Texture import Texture
from pygame import Color

def reducergb(t):
    return (t[0], t[1], t[2])

def rgbsimple(l):
    if l == None:
        return l
    newl = []
    for i in range(len(l)):
        newl.append((l[i][0],l[i][1],l[i][2]))
    return newl


def setsarray(sarray, x, y, color):
    sarray[x][y][0] = color[0]
    sarray[x][y][1] = color[1]
    sarray[x][y][2] = color[2]


def comparenonalpha(c1, c2):
    return c1[0] == c2[0] and c1[1] == c2[1] and c1[2]==c2[2]

# fills a polygon with a point in the polygon
# s is the surface, firstpoint is the starting point, fillcolor is the color to fill
# checkcolors is a list of colors that will be overridden
# bounds is a list x y width height of where the points can color, inclusive
def fillpolygon(s, firstpoint, fillcolor, checkcolors = None, stopcolors = None, fillbounds = None):

    sarray = pygame.surfarray.pixels3d(s)
    sarrayalpha = pygame.surfarray.pixels_alpha(s)
    
    alphatoset = 255
    if len(fillcolor) > 3:
        alphatoset = fillcolor[3]
    
    firstpoint = [int(firstpoint[0]), int(firstpoint[1])]
    if fillbounds == None:
        bounds = [0, 0, s.get_width(), s.get_height()]
    else:
        bounds = fillbounds
    pointlist = [firstpoint]

    def paintoverp(c):
        c = reducergb(c)
        stopp = False
        if checkcolors != None:
            incolors = False
            for check in checkcolors:
                if comparenonalpha(check, c):
                    incolors = True
                    break

            if not incolors:
                stopp = True
                
        if stopcolors != None:
            for check in stopcolors:
                if comparenonalpha(check, c):
                    stopp = True
                    break

        if comparenonalpha(c,fillcolor):
            stopp = True
            
        return not stopp

    if not paintoverp(sarray[pointlist[0][0]][pointlist[0][1]]):
        pointlist = []

    point = None
    while len(pointlist) != 0:
        point = pointlist.pop(0)
        setsarray(sarray, point[0],point[1], fillcolor)
        sarrayalpha[point[0]][point[1]] = alphatoset
        
        #if there is still a point to the left in the bounds
        if point[0] > bounds[0]:
            if paintoverp(sarray[point[0] - 1][point[1]]):
                pointlist.insert(0, [point[0] - 1, point[1]])
        if point[0] < bounds[0]+bounds[2]-1:
            if paintoverp(sarray[point[0] + 1][point[1]]):
                pointlist.insert(0, [point[0] + 1, point[1]])
        if point[1] > bounds[1]:
            if paintoverp(sarray[point[0]][point[1] - 1]):
                pointlist.insert(0, [point[0], point[1] - 1])
        if point[1] < bounds[1]+bounds[3]-1:
            if paintoverp(sarray[point[0]][point[1] + 1]):
                pointlist.insert(0, [point[0], point[1] + 1])

def pointinbounds(point, bounds):
    p = point
    b = bounds
    return p[0] >= b[0] and p[0] < b[0] + b[2] and p[1] >= b[1] and p[1] < b[1] + b[3]

def texturepoint(surface, x, y, t, bounds, sarray, sarrayalpha):
    # each point is a list of xpos, ypos, invisibleq
    points = [[x, y, False]]
    pointcolor = t.color
    # vary it by the spawn variance
    pointcolor = (pointcolor[0]+random.randint(-t.redvarianceperspawn, t.redvarianceperspawn), pointcolor[1]+random.randint(-t.greenvarianceperspawn, t.greenvarianceperspawn), pointcolor[2]+random.randint(-t.bluevarianceperspawn, t.bluevarianceperspawn))

    while len(points) > 0:
        p = points.pop(0)
        if pointinbounds(p, bounds):
            pc = sarray[p[0]][p[1]]
            pcolorreduced = (pc[0], pc[1], pc[2])
            pcolor = (pcolorreduced[0], pcolorreduced[1], pcolorreduced[2], sarrayalpha[p[0]][p[1]])
            acceptedcolorq = True
            if t.acceptedcolors != None:
                acceptedcolorq = pcolor in t.acceptedcolors or pcolorreduced in t.acceptedcolors
            
            # first check if the point is already colored, or if it is one of the colors not to paint
            if (pcolor != pointcolor) and (not pcolor in t.stopcolors) and acceptedcolorq:
                if not p[2]:
                    setcolor = (pointcolor[0]+random.randint(-t.redvariancefactor, t.redvariancefactor), pointcolor[1]+random.randint(-t.greenvariancefactor, t.greenvariancefactor), pointcolor[2]+random.randint(-t.bluevariancefactor, t.bluevariancefactor))
                    setsarray(sarray,p[0],p[1],setcolor)
                    sarrayalpha[p[0]][p[1]] = 255
                    
                addup = False
                adddown = False
                addright = False
                addleft = False
                yprob = t.ychance
                xprob = t.xchance
                if t.distruibution == "geometric":
                    yprob = yprob ** (1+abs(y-p[1]))
                    xprob = xprob ** (1+abs(x-p[0]))
                
                #now decide which points to add
                if t.addupq and (t.backtrackmodeonq or p[1] <= y):
                    if t.yinvisiblechance == 0:
                        upinvisibleq = False
                    else:
                        upinvisibleq = random.random() < t.yinvisiblechance
                    if random.random() < yprob:
                        addup = True
                if t.adddownq and (t.backtrackmodeonq or p[1] >= y):
                    if t.yinvisiblechance == 0:
                        downinvisibleq = False
                    else:
                        downinvisibleq = random.random() < t.yinvisiblechance
                    if random.random() < yprob:
                        adddown = True
                if t.addleftq and (t.backtrackmodeonq or p[0] <= x):
                    if t.xinvisiblechance == 0:
                        leftinvisibleq = False
                    else:
                        leftinvisibleq = random.random() < t.xinvisiblechance
                    if random.random() < xprob:
                        addleft = True
                if t.addrightq and (t.backtrackmodeonq or p[0] >= x):
                    if t.xinvisiblechance == 0:
                        rightinvisibleq = False
                    else:
                        rightinvisibleq = random.random() < t.xinvisiblechance
                    if random.random() < xprob:
                        addright = True
                        
                addlist = [addleft, addright, adddown, addup]
                if t.pickonedirp:
                    trueindexes = []
                    for i in range(len(addlist)):
                        if addlist[i]:
                            trueindexes.append(i)
                    if len(trueindexes)>0:
                        directioni = random.choice(trueindexes)
                        for i in range(len(addlist)):
                            if i == directioni:
                                addlist[i] = True
                            else:
                                addlist[i] = False
                    
                if addlist[3]:
                    points.append([p[0], p[1]-1, upinvisibleq])
                if addlist[2]:
                    points.append([p[0], p[1]+1, downinvisibleq])
                if addlist[0]:
                    points.append([p[0]-1, p[1], leftinvisibleq])
                if addlist[1]:
                    points.append([p[0]+1, p[1], rightinvisibleq])

def get_bounds(surface, texture):
    b = [0, 0, surface.get_width(), surface.get_height()]
    for x in range(4):
        if not texture.bounds[x] == None:
            b[x] = texture.bounds[x]
    return b

def get_texturing_bounds(bounds, texturebounds):
    tbounds = []
    for x in range(4):
        if not texturebounds[x] == None:
            tbounds.append(texturebounds[x])
        else:
            tbounds.append(bounds[x])
    return tbounds

def texturerow(surface, y, texture, b, tbounds, sarray, sarrayalpha):
    for x in range(tbounds[0], tbounds[0]+tbounds[2]):
        if random.random() < texture.initialchance:
            texturepoint(surface, x, y, texture, b, sarray, sarrayalpha)

#type is a string that refers to a set of textures and random patterns
def addtexture(surface, texture, printp = False):
    b = get_bounds(surface, texture)
    tbounds = get_texturing_bounds(b, texture.texturingbounds)
    sarray = pygame.surfarray.pixels3d(surface)
    sarrayalpha = pygame.surfarray.pixels_alpha(surface)
    if printp:
        print(b)
    for y in range(tbounds[1], tbounds[1]+tbounds[3]):
        texturerow(surface, y, texture, b, tbounds, sarray, sarrayalpha)
