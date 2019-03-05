import math, random
from pygame import gfxdraw
from pygame import Surface, SRCALPHA

from rdraw.pointlist import rotatepointlist


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


def drawplant(head_node):
    surface = Surface((20, 20), SRCALPHA)
    currentpos = (surface.get_width()/2, surface.get_height()-1)

    def drawnode(node):
        angle = node.anglespace*(node.repeatnum-1)/2 - math.pi/2
        
        for i in range(node.repeatnum):
            shape = node.plantshapelist[i]
            


            # chance to shift along points in the list
            l = shiftpointlist(shape.polygonlist, node.shiftchance)
                
            
            l = rotatepointlist(l, angle, offsetresult = (currentpos[0]-node.anchor[0], currentpos[1]-node.anchor[1]))


            gfxdraw.filled_polygon(surface, l, shape.fillcolor)
            gfxdraw.polygon(surface, l, shape.outlinecolor)

            
            
    drawnode(head_node)

    return surface
