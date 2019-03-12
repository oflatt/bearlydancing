import math, numpy
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


# returns a new list with rotated points, counter clockwise
def rotatepointlist(l, angle, offsetresult = (0,0)):

    newl = []
    for p in l:
        newl.append((p[0]*math.cos(angle)-(-p[1])*math.sin(angle) + offsetresult[0],
                     -((-p[1])*math.cos(angle)+p[0]*math.sin(angle)) + offsetresult[1]))

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



def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / numpy.linalg.norm(vector)


def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)

    return numpy.arccos(numpy.clip(numpy.dot(v1_u, v2_u), -1.0, 1.0))

# returns the angle between the vectors in the clockwise direction
def counterclockwise_angle(v1, v2):
    dot = v1[0]*v2[0] + (v1[1])*(v2[1])      # dot product between [v1[0], (-v1[1])] and [v2[0], (-v2[1])]
    det = v1[0]*(v2[1]) - (v1[1])*v2[0]      # determinant
    return math.atan2(det, dot)  # atan2(y, x) or atan2(sin, cos)


def listangleatindex(polygonlist, index):
    beforeindex = index-1
    afterindex = (index+1)%len(polygonlist)
    tries = 0
    while tries != len(polygonlist):
        if polygonlist[beforeindex] == polygonlist[index]:
            beforeindex += -1
            tries += 1
        else:
            break

    while tries != len(polygonlist):
        if polygonlist[afterindex] == polygonlist[index]:
            afterindex += 1
            tries += 1
        else:
            break
    
    v1 = (polygonlist[beforeindex][0]-polygonlist[index][0],
          -(polygonlist[beforeindex][1]-polygonlist[index][1]))
    v2 = (polygonlist[afterindex][0]-polygonlist[index][0],
          -(polygonlist[afterindex][1]-polygonlist[index][1]))



    angleofv2 = math.atan2(v2[1], v2[0])
    angleofv1 = math.atan2(v1[1], v1[0])
    angle_between_directional = counterclockwise_angle(v1, v2)
        
    return float(angleofv2 + math.pi - abs(angle_between_directional)/2) % (math.pi*2)

