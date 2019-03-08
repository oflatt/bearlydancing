import math, random
from pygame import gfxdraw
from pygame import Surface, SRCALPHA

from rdraw.pointlist import rotatepointlist
from rdraw.rdrawsoil import dirtcolor
from variables import brighten

from .constants import potwidth


def shiftpointlist(pointlistin, shiftchance, widthscalar, heightscalar):
    l = pointlistin.copy()
    shiftamount = 0

    for i in range(int(len(l)/2)): 
        if random.random() < shiftchance + shiftchance*i/len(l):
            if random.random() < 0.5:
                shiftamount += 1
            else:
                shiftamount -= 1

        l[i] = (l[i][0]*widthscalar, l[i][1]*heightscalar+shiftamount)
        l[-i-1] = (l[-i-1][0]*widthscalar, l[-i-1][1]*heightscalar+shiftamount)

    return l


def shiftpointlists(plantshapelist, shiftchance, widthscalar, heightscalar):
    listofpolygons = []

    for plantshape in plantshapelist:
        listofpolygons.append(shiftpointlist(plantshape.polygonlist, shiftchance, widthscalar, heightscalar))

    for plist in listofpolygons:
        if len(plist) % 2 != 0:
            raise Exception("polygonlist must be an even length, something went wrong")
    return listofpolygons


def transformtopointlists(plantshapelist, shiftchance, angle, offset, widthscalar, heightscalar):
    listofpolygonlists = shiftpointlists(plantshapelist, shiftchance, widthscalar, heightscalar)

    for i in range(len(listofpolygonlists)):
        listofpolygonlists[i] = rotatepointlist(listofpolygonlists[i], angle, offsetresult=offset)
    
    return listofpolygonlists

def drawplant(head_node):
    surface = Surface((40, 40), SRCALPHA)
    
    
    
    # the stack has the node, the currentx, and the currenty for each node in it
    stack = []

    for i in range(head_node.repeatnumseparate):
        stack.append(head_node)
        firstx = potwidth * random.random() * head_node.brancharea + surface.get_width()/2
        stack.append(firstx)
        stack.append(surface.get_height()-1)
    
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

            widthscalar = 1 + random.random()*node.widthvariance
            heightscalar = 1 + random.random()*node.heightvariance
            pointliststransformed = transformtopointlists(node.plantshapelist, node.shiftchance, angle,
                                                          (currentx-node.anchor[0], currenty-node.anchor[1]),
                                                          widthscalar, heightscalar)


            for i in range(len(pointliststransformed)):
                if node.plantshapelist[i].fillcolor != None:
                    gfxdraw.filled_polygon(surface, pointliststransformed[i], node.plantshapelist[i].fillcolor)
                if node.plantshapelist[i].outlinecolor != None:
                    gfxdraw.polygon(surface, pointliststransformed[i], node.plantshapelist[i].outlinecolor)

            
            # find the new currentx and currenty
            mainlistlen = len(node.plantshapelist[0].polygonlist)
            mainltranslated = pointliststransformed[0]

            
            # add all the children at the current position
            for childnode in node.children:
                for i in range(childnode.repeatnumseparate):
                    
                    randindex = random.randint(int(mainlistlen/2 - mainlistlen*childnode.brancharea),
                                               int(mainlistlen/2 + mainlistlen*childnode.brancharea))
                    futurex = mainltranslated[randindex][0]
                    futurey = mainltranslated[randindex][1]
                    stack.append(childnode)
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
