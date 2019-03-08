import math, random
from pygame import gfxdraw
from pygame import Surface, SRCALPHA

from rdraw.pointlist import rotatepointlist
from rdraw.rdrawsoil import dirtcolor
from variables import brighten


def shiftpointlist(pointlistin, shiftchance):
    l = pointlistin.copy()
    shiftamount = 0
    if len(l) % 2 != 0:
        raise Exception("polygonlist must be an even length, something went wrong")

    for i in range(int(len(l)/2)): 
        if random.random() < shiftchance + shiftchance*i/len(l):
            if random.random() < 0.5:
                shiftamount += 1
            else:
                shiftamount -= 1

        l[i] = (l[i][0], l[i][1]+shiftamount)
        l[-i-1] = (l[-i-1][0], l[-i-1][1]+shiftamount)

    return l


def plantshapelistdisplacement():
    pass

def drawplant(head_node):
    surface = Surface((40, 40), SRCALPHA)

    # the stack has the node, the currentx, and the currenty for each node in it
    stack = [head_node, surface.get_width()/2, surface.get_height()-1]
        
    callcount = 0

    while len(stack) != 0 and callcount < 1000:
        
        callcount += 1
        currenty = stack.pop()
        currentx = stack.pop()
        node = stack.pop()
        
        randomspacings = [0]
        spacingLength = 0
        for i in range(node.repeatnum-1):
            randomspacings.append(random.uniform(node.anglespace-node.anglevariance*node.anglespace, node.anglespace+node.anglevariance*node.anglespace))
            spacingLength += randomspacings[i+1]

        startspacing = random.uniform(node.anglespace-node.anglevariance*node.anglespace, node.anglespace+node.anglevariance*node.anglespace)/2 * random.choice((-1, 1))
        
        # start angle so that it points up on average
        angle = -math.pi/2 + startspacing - spacingLength/2 + node.angleoffset
        
        for i in range(node.repeatnum):
            # draw all the plantshapes at this angle
            angle += randomspacings[i]
            mainltranslated = None
            for shapei in range(len(node.plantshapelist)):
                shape = node.plantshapelist[shapei]
            

                
                # chance to shift along points in the list
                l = shiftpointlist(shape.polygonlist, node.shiftchance)
                
            
                l = rotatepointlist(l, angle, offsetresult = (currentx-node.anchor[0], currenty-node.anchor[1]))
                

                if mainltranslated == None:
                    mainltranslated = l


                gfxdraw.filled_polygon(surface, l, shape.fillcolor)
                gfxdraw.polygon(surface, l, shape.outlinecolor)

            # find the new currentx and currenty
            mainlistlen = len(node.plantshapelist[0].polygonlist)
            randindex = random.randint(int(mainlistlen/2 - mainlistlen*node.brancharea),
                                       int(mainlistlen/2 + mainlistlen*node.brancharea))
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
