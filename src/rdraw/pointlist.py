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
