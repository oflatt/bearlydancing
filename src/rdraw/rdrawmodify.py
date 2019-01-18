import pygame, math, numpy, copy
from pygame import Rect

import variables
from Shadow import Shadow

def fillskipalpha(surface, color):
    array = pygame.surfarray.pixels2d(surface)
    colorcode = surface.map_rgb(color)
    checkcolors = (surface.map_rgb((0,0,0,0)), surface.map_rgb((255,255,255,0)))
    array[numpy.logical_and(array != checkcolors[0], array != checkcolors[1])] = colorcode
    del array


def findanchor(surface, checklist = [], greatestfrom = 1, xchangedir = -1):
    if greatestfrom < 1:
        greatestfrom = 1
    anchor = None
    array = pygame.surfarray.pixels2d(surface)
    checkcolors = (surface.map_rgb((0,0,0,0)), surface.map_rgb((255,255,255,0)))
    numberfound = 0

    if xchangedir < 0:
        start = array.shape[0]-1
        end = -1
    else:
        start = 0
        end = array.shape[0]
    
    for y in range(array.shape[1]-1, 0-1, -1):
        for x in range(start, end, xchangedir):
            
            if not array[x][y] in checkcolors and (len(checklist) == 0 or array[x][y] in checklist):
                if anchor == None:
                    anchor = (x, y)
                elif xchangedir > 0:
                    if x < anchor[0]:
                        anchor = (x, y)
                else:
                    if x > anchor[0]:
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


# rotate around the offset (relative to middle of surface)
def rotate(surface, angleradians, offset):
    angle = angleradians*180 / math.pi
    pivot = surface.get_rect().center
    rotated_image = pygame.transform.rotozoom(surface, -angle, 1)  # Rotate the image.
    rotated_offset = offset.rotate(angle)  # Rotate the offset vector.
    
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = rotated_image.get_rect(center=pivot-rotated_offset+offset)
    return rotated_image, rect  # Return the rotated image and shifted rect.

#rotates half of the way, then squishes the rest of the way
# all transformations are also applied to offset so that positioning can be done
def rotateandsquish(surface, angleradians, offset, rotateportion = 0.75, scaling = 1):
    
    rotated_offset = copy.deepcopy(offset)
    
    # scale height by scaling first
    firstscalingimage = pygame.transform.scale(surface, (surface.get_width(), int(surface.get_height()*scaling)))
    
    rotated_offset = pygame.Vector2(rotated_offset.x, rotated_offset.y * scaling)
    
    angledegrees = angleradians*180 / math.pi

    
    # rotate the image
    rotated_image = pygame.transform.rotozoom(firstscalingimage, -angledegrees*rotateportion, 1)
    
    
    # Rotate the offset vector.
    rotated_offset = rotated_offset.rotate(angledegrees*rotateportion)

    angleafterrotate = abs(math.pi/2 - angleradians*rotateportion)
    goalangleradians = abs(math.pi/2 - angleradians)
    goalovercurrent = numpy.sin(goalangleradians)/numpy.sin(angleafterrotate)
    newheight = firstscalingimage.get_height() * goalovercurrent

    
    # scale the rest of the way to the angle
    scaled_image = pygame.transform.scale(rotated_image, (rotated_image.get_width(), int(newheight)))

    # scale the vector the same way
    rotated_offset = pygame.Vector2(rotated_offset.x, rotated_offset.y * int(newheight)/rotated_image.get_height())


    pivot = surface.get_rect().center
    # Add the offset vector to the center/pivot point to shift the rect.
    rect = scaled_image.get_rect(center=pivot-rotated_offset+offset)
    return scaled_image, rect  # Return the rotated image and shifted rect.



# returns a surface that is a shadow of the surface given at an angle
def createshadow(surface, angle):
    # crop it for the shadow
    surface = surface.subsurface(Rect(0,0,surface.get_width(),int(surface.get_height() * 14/15)))

    rotatingfactor = ((abs(angle) % (math.pi/2)))/(math.pi/2) * 0.8 + 0.2
    scalingfactor = ((abs(angle) % (math.pi/2)))/(math.pi/2) * 0.5 + 0.5
    dirforanchor = -1
    if angle > 0:
        dirforanchor = 1
    # find the anchor point
    sanchor = findanchor(surface, greatestfrom = int(surface.get_height() / 15), xchangedir = dirforanchor)
    
    srect = surface.get_rect()

    # offset is a vector from the center to the anchor
    offset = pygame.math.Vector2(sanchor[0]-srect.center[0], sanchor[1]-srect.center[1])

    rotateportion = ((abs(angle) % (math.pi/2)))/(math.pi/2) * 0.9 + 0.1
    

    
    newsurface, newrect = rotateandsquish(surface, -angle, offset,
                                          rotateportion = rotatingfactor, scaling = scalingfactor)
    
    # convert to shadow color
    fillskipalpha(newsurface, (0,0,0,100))
    
    
    return Shadow(newsurface, newrect.left, newrect.top)


def rotatepoint(point, angle):
    newx = point[0] * math.cos(angle) - point[1] * math.sin(angle)
    newy = point[0] * math.sin(angle) + point[1] * math.cos(angle)
    return (newx, newy)
