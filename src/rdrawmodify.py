import pygame, math, numpy, unittest
from pygame import Rect

import variables
from Shadow import Shadow

def fillskipalpha(surface, color):
    array = pygame.surfarray.pixels2d(surface)
    colorcode = surface.map_rgb(color)
    checkcolors = (surface.map_rgb((0,0,0,0)), surface.map_rgb((255,255,255,0)))
    array[numpy.logical_and(array != checkcolors[0], array != checkcolors[1])] = colorcode
    del array


def findanchor(surface, checklist = [], greatestfrom = 1):
    anchor = None
    array = pygame.surfarray.pixels2d(surface)
    checkcolors = (surface.map_rgb((0,0,0,0)), surface.map_rgb((255,255,255,0)))
    numberfound = 0
    
    for y in range(array.shape[1]-1, 0-1, -1):
        for x in range(array.shape[0]-1, 0-1, -1):
            
            if not array[x][y] in checkcolors and (len(checklist) == 0 or array[x][y] in checklist):
                if anchor == None or x >= anchor[0]:
                    anchor = (x, y)
                numberfound += 1
                break
                

        if anchor != None:
            if numberfound >= greatestfrom:
                break
            
    if anchor == None:
        print("not found")
        anchor = (len(array)-1, len(array[0])-1)
    return anchor


def rotate(surface, angle, offset, scaling):
    """Rotate the surface around the pivot point.

    Args:
        surface (pygame.Surface): The surface that is to be rotated.
        angle (float): Rotate by this angle.
        pivot (tuple, list, pygame.math.Vector2): The pivot point.
    """
    pivot = surface.get_rect().center
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot-rotated_offset+offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.



# returns a surface that is a shadow of the surface given at an angle
def createshadow(surface, angle):
    scalingfactor = 1#((abs(angle) % (math.pi/2)))/(math.pi/2)
    # find the anchor point
    sanchor = findanchor(surface, greatestfrom = int(surface.get_height() / 8))
    srect = surface.get_rect()
    
    

    # offset is a vector from the center to the anchor
    offset = pygame.math.Vector2(sanchor[0]-srect.center[0], sanchor[1]-srect.center[1])
    
    # scale it down and rotate it
    newsurface, newrect = rotate(surface, -angle*180 / math.pi, offset, scalingfactor)
    
    # convert to shadow color
    fillskipalpha(newsurface, (0,0,0,100))
    
    
    return Shadow(newsurface, newrect.left, newrect.top)


def rotatepoint(point, angle):
    newx = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    newy = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return (newx, newy)
