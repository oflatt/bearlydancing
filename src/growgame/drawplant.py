import math, random
from pygame import gfxdraw
from pygame import Surface, SRCALPHA

from rdraw.pointlist import rotatepointlist
from rdraw.rdrawsoil import dirtcolor
from variables import brighten

from .constants import potwidth


def shiftpointlist(pointlistin, shiftchance):
    l = pointlistin.copy()
    shiftamount = 0

    for i in range(int(len(l)/2)): 
        if random.random() < shiftchance + shiftchance*i/len(l):
            if random.random() < 0.5:
                shiftamount += 1
            else:
                shiftamount -= 1

        l[i] = (l[i][0], l[i][1]+shiftamount)
        l[-i-1] = (l[-i-1][0], l[-i-1][1]+shiftamount)

    return l


def shiftpointlists(plantshapelist, shiftchance):
    listofpolygons = []

    for plantshape in plantshapelist:
        listofpolygons.append(shiftpointlist(plantshape.polygonlist, shiftchance))

    for plist in listofpolygons:
        if len(plist) % 2 != 0:
            raise Exception("polygonlist must be an even length, something went wrong")
    return listofpolygons


def transformtopointlists(plantshapelist, shiftchance, angle, offset):
    listofpolygonlists = shiftpointlists(plantshapelist, shiftchance)

    for i in range(len(listofpolygonlists)):
        listofpolygonlists[i] = rotatepointlist(listofpolygonlists[i], angle, offsetresult=offset)
    
    return listofpolygonlists

def drawplant(head_node):
    surface = Surface((40, 40), SRCALPHA)

    firstx = potwidth * random.random() * head_node.brancharea + surface.get_width()/2
    
    # the stack has the node, the currentx, and the currenty for each node in it
    stack = [head_node, firstx, surface.get_height()-1]
    
    callcount = 0

    while len(stack) != 0 and callcount < 1000:
        
        callcount += 1
        currenty = stack.pop()
        currentx = stack.pop()
        node = stack.pop()
        
        randomspacings = [0]
        spacingLength = 0
        for i in range(node.repeatnumcircle-1):
            randomspacings.append(random.uniform(node.anglespace-node.anglevariance*node.anglespace, node.anglespace+node.anglevariance*node.anglespace))
            spacingLength += randomspacings[i+1]

        startspacing = random.uniform(node.anglespace-node.anglevariance*node.anglespace, node.anglespace+node.anglevariance*node.anglespace)/2 * random.choice((-1, 1))
        
        # start angle so that it points up on average
        angle = -math.pi/2 + startspacing - spacingLength/2 + node.angleoffset

        # update the random spacing to be final angles
        for i in range(len(randomspacings)):
            angle = angle + randomspacings[i]
            randomspacings[i] = angle

        for i in range(node.repeatnumcircle):
            # draw all the plantshapes at this angle
            # pick a random angle out of the list
            angle = randomspacings.pop(random.randint(0, len(randomspacings)-1))

            pointliststransformed = transformtopointlists(node.plantshapelist, node.shiftchance, angle, (currentx-node.anchor[0], currenty-node.anchor[1]))


            for i in range(len(pointliststransformed)):
                if node.plantshapelist[i].fillcolor != None:
                    gfxdraw.filled_polygon(surface, pointliststransformed[i], node.plantshapelist[i].fillcolor)
                if node.plantshapelist[i].outlinecolor != None:
                    gfxdraw.polygon(surface, pointliststransformed[i], node.plantshapelist[i].outlinecolor)

            
            # find the new currentx and currenty
            mainlistlen = len(node.plantshapelist[0].polygonlist)
            randindex = random.randint(int(mainlistlen/2 - mainlistlen*node.brancharea),
                                       int(mainlistlen/2 + mainlistlen*node.brancharea))
            mainltranslated = pointliststransformed[0]
            futurex = mainltranslated[randindex][0]
            futurey = mainltranslated[randindex][1]

            # add all the children at the current position
            for n in node.children:
                stack.append(n)
                stack.append(futurex)
                stack.append(futurey)

    # draw dirt clumps at bottom
    clumpscale = 0.1
    for i in range(3):
        gfxdraw.filled_circle(surface, int(surface.get_width()/2 - clumpscale + (2+i)*clumpscale),
                       int(surface.get_height()-1),
                       int(random.uniform(surface.get_width()*clumpscale/2,
                                          surface.get_width()*clumpscale)),
                        brighten(dirtcolor, -10))
        
    return surface
