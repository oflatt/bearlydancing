import pygame
from pygame import Surface
from devoptions import args

import variables

def addsurfaceGR(GR, s, name, dimensions = None):
    if dimensions == None:
        dimensions = [s.get_width(), s.get_height()]
    if args.novideomode:
        GR[name] = {"img":s,"w":dimensions[0],"h":dimensions[1]}
    else:
        GR[name] = {"img":s.convert_alpha(),"w":dimensions[0],"h":dimensions[1]}


def adddancearrows(GR):
    # duplicate and rotate the left arrow
    leftdancearrow = GR["leftdancearrow"]["img"]
    rightdancearrow = variables.transformrotate(leftdancearrow,180)
    downdancearrow = variables.transformrotate(leftdancearrow,270)
    updancearrow = variables.transformrotate(leftdancearrow,90)

    leftdancearrowdark = leftdancearrow.copy()
    rightdancearrowdark = rightdancearrow.copy()
    updancearrowdark = updancearrow.copy()
    downdancearrowdark = downdancearrow.copy()

    pygame.PixelArray(leftdancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[0], -40))
    pygame.PixelArray(rightdancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[3], -40))
    pygame.PixelArray(updancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[2], -40))
    pygame.PixelArray(downdancearrow).replace((255,255,255), variables.brighten(variables.notes_colors[1], -40))

    pygame.PixelArray(leftdancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[0], -100))
    pygame.PixelArray(rightdancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[3], -100))
    pygame.PixelArray(updancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[2], -100))
    pygame.PixelArray(downdancearrowdark).replace((255,255,255), variables.brighten(variables.notes_colors[1], -100))

    pygame.PixelArray(leftdancearrow).replace((0,0,0), variables.notes_colors[0])
    pygame.PixelArray(rightdancearrow).replace((0,0,0), variables.notes_colors[3])
    pygame.PixelArray(updancearrow).replace((0,0,0), variables.notes_colors[2])
    pygame.PixelArray(downdancearrow).replace((0,0,0), variables.notes_colors[1])

    pygame.PixelArray(leftdancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[0], -50))
    pygame.PixelArray(rightdancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[3], -50))
    pygame.PixelArray(updancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[2], -50))
    pygame.PixelArray(downdancearrowdark).replace((0,0,0), variables.brighten(variables.notes_colors[1], -50))


    GR["leftdancearrow"]["img"] = leftdancearrow
    addsurfaceGR(GR, rightdancearrow, "rightdancearrow")
    addsurfaceGR(GR, updancearrow, "updancearrow")
    addsurfaceGR(GR, downdancearrow, "downdancearrow")

    addsurfaceGR(GR, leftdancearrowdark, "leftdancearrowdark")
    addsurfaceGR(GR, rightdancearrowdark, "rightdancearrowdark")
    addsurfaceGR(GR, updancearrowdark, "updancearrowdark")
    addsurfaceGR(GR, downdancearrowdark, "downdancearrowdark")
    
def load_special_graphics(GR):
    
    #add empty surface
    addsurfaceGR(GR, Surface((1,1), pygame.SRCALPHA), "empty")

    # down arrow used for conversations
    DOWNARROW = pygame.Surface([5, 8], pygame.SRCALPHA)
    pygame.draw.polygon(DOWNARROW, variables.WHITE, [[0, 4], [4, 4], [2, 7]])
    DOWNARROW.fill(variables.WHITE, pygame.Rect(1, 0, 3, 3))
    RIGHTARROW = variables.transformrotate(DOWNARROW, 90)
    addsurfaceGR(GR, DOWNARROW, "downarrow")
    addsurfaceGR(GR, RIGHTARROW, "rightarrow")

    adddancearrows(GR)

