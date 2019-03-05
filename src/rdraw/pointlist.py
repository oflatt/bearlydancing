import math

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
