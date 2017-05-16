import random
from Texture import Texture

def pointinbounds(point, bounds):
    p = point
    b = bounds
    return p[0] >= b[0] and p[0] < b[2] and p[1] >= b[1] and p[1] < b[3]

def texturepoint(surface, x, y, t, bounds):
    points = [[x, y]]

    while len(points) > 0:
        p = points.pop(0)
        if pointinbounds(p, bounds):
            pcolor = surface.get_at(p)
            acceptedcolorq = True
            if t.acceptedcolors != None:
                acceptedcolorq = pcolor in t.acceptedcolors
            
            # first check if the point is already colored, or if it is one of the colors not to paint
            if (pcolor != t.color) and (not pcolor in t.stopcolors) and acceptedcolorq:
                surface.set_at(p, t.color)
                #now decide which points to add
                if t.addupq:
                    if random.random() < t.ychance:
                        points.append([p[0], p[1]-1])
                if t.adddownq:
                    if random.random() < t.ychance:
                        points.append([p[0], p[1]+1])
                if t.addleftq:
                    if random.random() < t.xchance:
                        points.append([p[0]-1, p[1]])
                if t.addrightq:
                    if random.random() < t.xchance:
                        points.append([p[0]+1, p[1]])

def texturerow(surface, y, texture, b):
    for x in range(b[0], b[2]):
        if random.random() < texture.initialchance:
            texturepoint(surface, x, y, texture, b)

def get_bounds(surface, texture):
    b = [0, 0, surface.get_width(), surface.get_height()]
    for x in range(4):
        if not texture.bounds[x] == None:
            b[x] = texture.bounds[x]
    return b

#type is a string that refers to a set of textures and random patterns
def addtexture(surface, texture):
    b = get_bounds(surface, texture)
    for y in range(b[1], b[3]):
        texturerow(surface, y, texture, b)
