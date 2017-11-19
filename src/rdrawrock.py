import pygame, variables, random, math
from random import randint
from addtexture import addtexture, fillpolygon
from Texture import Texture

numofpoints = 15

#pointlist is a list of points centered around zero on the classical cartesian plane
# startpoint and endpoint are list indexes and are both inclusive
# it creates "lumps" by adding to the y values
def addlump(pointlist, startpoint, endpoint, radius, addtoy = True):
    lengthoflump = endpoint - startpoint + 1
    for t in range(startpoint, endpoint+1):
        radians = ((t-startpoint)/(2*lengthoflump)) * 2 * math.pi
        if addtoy:
            pointlist[t%numofpoints][1] += math.sin(radians) * radius
        else:
            pointlist[t%numofpoints][0] += math.sin(radians) * radius
        
def makerock():
    outlinecolor = (105, 105, 105)
    insidegrey = randint(115, 130)
    insidecolor = (insidegrey, insidegrey, insidegrey)
    texture1grey = randint(insidegrey-20, insidegrey-2)
    texture2grey = randint(insidegrey+2, insidegrey+20)
    texture1color = (texture1grey, texture1grey, texture1grey)
    texture2color = (texture2grey, texture2grey, texture2grey)

    pointlist = []
    radius = randint(9, 12)

    #chance for small rock
    if random.randint(0, 5) < 1:
        radius = randint(4, 9)
    
    for t in range(numofpoints):
        radians = (t/numofpoints) * 2 * math.pi
        xpos = radius * math.cos(radians) + 1.5 * math.cos(radians)
        ypos = radius * math.sin(radians)
        
        pointlist.append([xpos, ypos])

    # squish bottom of rock
    addlump(pointlist, int(numofpoints/2), numofpoints, 3)

    numoflumps = randint(1, 3)
    for x in range(numoflumps):
        addtoy = True
        lumplength = randint(int(numofpoints/5), int(numofpoints/2))
        startpoint = randint(-1, int(numofpoints/2)+2-lumplength)
        if randint(0, 4) == 1:
            addtoy = False
            startpoint = randint(-int(numofpoints/5), int(numofpoints/2)+int(numofpoints/5)-lumplength)
        addlump(pointlist, startpoint, startpoint + lumplength, randint(1, 4), addtoy)

    def getx(pos):
        return pos[0]
    def gety(pos):
        return pos[1]
    minx = min(pointlist, key=getx)[0]
    maxx = max(pointlist, key=getx)[0]
    miny = min(pointlist, key=gety)[1]
    maxy = max(pointlist, key=gety)[1]
    rockwidth = maxx-minx+1
    rockheight = maxy-miny+1
    for pos in pointlist:
        # flip because it was based on cartesian plane
        pos[1] = -pos[1]
        
        # center it
        pos[0] += abs(minx)
        pos[1] += abs(maxy)

    s = pygame.Surface([rockwidth, rockheight], pygame.SRCALPHA)

    pygame.draw.polygon(s, outlinecolor, pointlist, 1)
    fillpolygon(s, [5,5], insidecolor, stopcolors = [outlinecolor])
    texture1 = Texture(texture1color, 1/10, 1/20, 1/20, acceptedcolors=[insidecolor])
    texture1.addupq = True
    texture2 = Texture(texture2color, 1/10, 1/30, 1/30, acceptedcolors=[insidecolor])
    texture2.addupq = True
    addtexture(s, texture1)
    addtexture(s, texture2)

    return s
