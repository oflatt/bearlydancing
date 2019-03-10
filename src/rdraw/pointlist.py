import math
from pygame import Rect

# starts at startx and starty as the left side of the circle
def listarc(startx, starty, width, height, numofpoints):
    pointlist = []


    for t in range(numofpoints):
        radians = -(t/(numofpoints-1)) * math.pi + math.pi
        xpos = width/2 * math.cos(radians) + startx + width/2
        ypos = -height * math.sin(radians) + starty
        
        pointlist.append([xpos, ypos])

    return pointlist


# returns a new list with rotated points
def rotatepointlist(l, angle, offsetresult = (0,0)):
    newl = []
    for p in l:
        newl.append((p[0]*math.cos(angle)-p[1]*math.sin(angle) + offsetresult[0],
                     p[1]*math.cos(angle)+p[0]*math.sin(angle) + offsetresult[1]))

    return newl


def offsetpointlist(l, offset):
    newl = []
    for p in l:
        newl.append((p[0]+offset[0],
                     p[1]+offset[1]))
    return newl

# get a rect that is the bounding box of the polygon
def getlistbounds(polygonlist):
    bounds = [polygonlist[0][0], polygonlist[0][1], polygonlist[0][0], polygonlist[0][1]]
    for p in polygonlist:
        if p[0] < bounds[0]:
            bounds[0] = p[0]
        if p[0] > bounds[2]:
            bounds[2] = p[0]
        if p[1] < bounds[1]:
            bounds[1] = p[1]
        if p[1] > bounds[3]:
            bounds[3] = p[1]
            
    # add some offset for rounding in polygon drawing
    bounds[0] -= 1
    bounds[1] -= 1
    bounds[2] += 2
    bounds[3] += 2
    return Rect(bounds[0], bounds[1], bounds[2]-bounds[0], bounds[3]-bounds[1])

# find the angle tangent to the point at the index in the clockwise direction
# does this by taking the vector to the next point and rotating it
def listangleatindex(polygonlist, index):
    beforeindex = index-1
    afterindex = (index+1)%len(polygonlist)
    #v1 = (polygonlist[index][1]-polygonlist[beforeindex][1], polygonlist[index][0]-polygonlist[beforeindex][0])
    v2 = (polygonlist[index][1]-polygonlist[afterindex][1], polygonlist[index][0]-polygonlist[afterindex][0])
    #angle1 = math.atan2(v1[1], v1[0])
    angle2 = math.atan2(v2[1], v2[0])
    return angle2-(math.pi/2)
