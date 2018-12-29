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



# returns a surface that is a shadow of the surface given at an angle
def createshadow(surface, angle):
    scalingfactor = 1#((math.pi/2)-(abs(angle) % (math.pi/2)))/(math.pi/2)

    newsurface = pygame.transform.scale(surface, (surface.get_width(), int(surface.get_height() * scalingfactor)))

    
    # find the anchor point
    sanchor = findanchor(newsurface, greatestfrom = int(newsurface.get_height() / 5))
    
    # fill the anchor
    newsurface.fill((255,0,0,255), Rect(sanchor[0]-1, sanchor[1]-1, 3, 3))
    pixels = pygame.surfarray.pixels2d(newsurface)
    
    
    # rotate
    newsurface = pygame.transform.rotate(newsurface, angle*180 / (math.pi))

    # find the anchor
    secondsanchor = findanchor(newsurface, checklist = [pixels[sanchor[0]][sanchor[1]]])

    # convert to shadow color
    fillskipalpha(newsurface, (0,0,0,100))

    
    return Shadow(newsurface, sanchor[0]-secondsanchor[0], sanchor[1]-secondsanchor[1])


def rotatepoint(point, angle):
    newx = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    newy = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return (newx, newy)
