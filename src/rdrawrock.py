import pygame, variables, random, math
from random import randint
from addtexture import addtexture, fillpolygon
from Texture import Texture

numofpoints = 15

#pointlist is a list of points centered around zero on the classical cartesian plane
# startpoint and endpoint are list indexes and are both inclusive
# it creates "lumps" by adding to the y values
def addlump(pointlist, startpoint, endpoint, radius):
    lengthoflump = endpoint - startpoint + 1
    for t in range(startpoint, endpoint+1):
        radians = ((t-startpoint)/(2*lengthoflump)) * 2 * math.pi
        pointlist[t%numofpoints][1] += math.sin(radians) * radius

def makerock():
    outlinecolor = (105, 105, 105)
    insidecolor = (129, 122, 122)
    texture1color = (121, 115, 115)
    texture2color = (144, 138, 138)

    pointlist = []
    defaultradius = 10
    
    for t in range(numofpoints):
        radians = (t/numofpoints) * 2 * math.pi
        xpos = defaultradius * math.cos(radians) + 1.5 * math.cos(radians)
        ypos = defaultradius * math.sin(radians)
        
        pointlist.append([xpos, ypos])

    # squish bottom of rock
    addlump(pointlist, int(numofpoints/2), numofpoints, 3)

    numoflumps = randint(1, 3)
    for x in range(numoflumps):
        lumplength = randint(int(numofpoints/5), int(numofpoints/2))
        startpoint = randint(-1, int(numofpoints/2)+2-lumplength)
        addlump(pointlist, startpoint, startpoint + lumplength, randint(1, 4))

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
    

    return s
