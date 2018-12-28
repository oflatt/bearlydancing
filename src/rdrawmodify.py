import pygame, math, numpy

from Shadow import Shadow

def fillskipalpha(surface, color):
    array = pygame.surfarray.pixels2d(surface)
    colorcode = surface.map_rgb(color)
    checkcolors = (surface.map_rgb((0,0,0,0)), surface.map_rgb((255,255,255,0)))
    array[numpy.logical_and(array != checkcolors[0], array != checkcolors[1])] = colorcode
    del array

def findanchor(surface):
    anchor = None
    array = pygame.surfarray.pixels2d(surface)
    checkcolors = (surface.map_rgb((0,0,0,0)), surface.map_rgb((255,255,255,0)))
    for y in range(len(array[0])-1, 0-1, -1):
        for x in range(len(array)-1, 0-1, -1):
            if not array[x][y] in checkcolors:
                anchor = (x, y)
                break

        if anchor != None:
            break
    if anchor == None:
        anchor = (len(array)-1, len(array[0])-1)
    return anchor
        

# returns a surface that is a shadow of the surface given at an angle
def createshadow(surface, angle):
    scalingfactor = 1#((math.pi/2)-(abs(angle) % (math.pi/2)))/(math.pi/2)

    newsurface = pygame.transform.scale(surface, (surface.get_width(), int(surface.get_height() * scalingfactor)))

    newsurface = pygame.transform.rotate(newsurface, angle*180 / (math.pi))

    # convert to shadow color
    fillskipalpha(newsurface, (0,0,0,100))

    # find the anchor point
    shadowanchor = findanchor(newsurface)
    
    
    return Shadow(newsurface, shadowanchor[0], shadowanchor[1])
