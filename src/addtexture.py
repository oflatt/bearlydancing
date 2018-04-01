import random
from Texture import Texture

# fills a polygon with a point in the polygon
# s is the surface, firstpoint is the starting point, fillcolor is the color to fill
# checkcolors is a list of colors that will be overridden
# bounds is a list x y width height of where the points can color, inclusive
def fillpolygon(s, firstpoint, fillcolor, checkcolors = None, stopcolors = None, fillbounds = None):
    if fillbounds == None:
        bounds = [0, 0, s.get_width(), s.get_height()]
    else:
        bounds = fillbounds
    pointlist = [firstpoint]

    def paintoverp(c):
        stopp = False
        if checkcolors != None:
            if not c in checkcolors:
                stopp = True
        if stopcolors != None:
            if c in stopcolors:
                stopp = True
        if c == fillcolor:
            stopp = True
        return not stopp
    
    while len(pointlist) != 0:
        point = pointlist.pop(0)
        if point[0] >= 0 and point[0] < s.get_width() and point[1]>0 and point[1] < s.get_height():
            s.set_at(point, fillcolor)
        #if there is still a point to the left in the boudns
        if point[0] > bounds[0]:
            if paintoverp(s.get_at([point[0] - 1, point[1]])):
                pointlist.insert(0, [point[0] - 1, point[1]])
        if point[0] < bounds[0]+bounds[2]:
            if paintoverp(s.get_at([point[0] + 1, point[1]])):
                pointlist.insert(0, [point[0] + 1, point[1]])
        if point[1] > bounds[1]:
            if paintoverp(s.get_at([point[0], point[1] - 1])):
                pointlist.insert(0, [point[0], point[1] - 1])
        if point[1] < bounds[1]+bounds[3]:
            if paintoverp(s.get_at([point[0], point[1] + 1])):
                pointlist.insert(0, [point[0], point[1] + 1])

def pointinbounds(point, bounds):
    p = point
    b = bounds
    return p[0] >= b[0] and p[0] < b[0] + b[2] and p[1] >= b[1] and p[1] < b[1] + b[3]

def texturepoint(surface, x, y, t, bounds):
    # each point is a list of xpos, ypos, invisibleq
    points = [[x, y, False]]

    while len(points) > 0:
        p = points.pop(0)
        if pointinbounds(p, bounds):
            pcolor = surface.get_at(p[0:2])
            pcolorreduced = (pcolor[0], pcolor[1], pcolor[2])
            acceptedcolorq = True
            if t.acceptedcolors != None:
                acceptedcolorq = pcolor in t.acceptedcolors or pcolorreduced in t.acceptedcolors
            
            # first check if the point is already colored, or if it is one of the colors not to paint
            if (pcolor != t.color) and (not pcolor in t.stopcolors) and acceptedcolorq:
                if not p[2]:
                    setcolor = (t.color[0]+random.randint(-t.redvariancefactor, t.redvariancefactor), t.color[1]+random.randint(-t.greenvariancefactor, t.greenvariancefactor), t.color[2]+random.randint(-t.bluevariancefactor, t.bluevariancefactor))
                    
                    surface.set_at(p[0:2], setcolor)

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
                        invisibleq = False
                    else:
                        invisibleq = random.random() < t.yinvisiblechance
                    if random.random() < yprob:
                        addup = True
                if t.adddownq and (t.backtrackmodeonq or p[1] >= y):
                    if t.yinvisiblechance == 0:
                        invisibleq = False
                    else:
                        invisibleq = random.random() < t.yinvisiblechance
                    if random.random() < yprob:
                        adddown = True
                if t.addleftq and (t.backtrackmodeonq or p[0] <= x):
                    if t.xinvisiblechance == 0:
                        invisibleq = False
                    else:
                        invisibleq = random.random() < t.xinvisiblechance
                    if random.random() < xprob:
                        addleft = True
                if t.addrightq and (t.backtrackmodeonq or p[0] >= x):
                    if t.xinvisiblechance == 0:
                        invisibleq = False
                    else:
                        invisibleq = random.random() < t.xinvisiblechance
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
                    points.append([p[0], p[1]-1, invisibleq])
                if addlist[2]:
                    points.append([p[0], p[1]+1, invisibleq])
                if addlist[0]:
                    points.append([p[0]-1, p[1], invisibleq])
                if addlist[1]:
                    points.append([p[0]+1, p[1], invisibleq])

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

def texturerow(surface, y, texture, b, tbounds):
    for x in range(tbounds[0], tbounds[0]+tbounds[2]):
        if random.random() < texture.initialchance:
            texturepoint(surface, x, y, texture, b)

#type is a string that refers to a set of textures and random patterns
def addtexture(surface, texture, printp = False):
    b = get_bounds(surface, texture)
    tbounds = get_texturing_bounds(b, texture.texturingbounds)
    if printp:
        print(b)
    for y in range(tbounds[1], tbounds[1]+tbounds[3]):
        texturerow(surface, y, texture, b, tbounds)
