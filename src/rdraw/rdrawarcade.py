import pygame
from random import randint
from pygame import Surface

import variables

def makecabinet(width, height):
    surface = pygame.Surface((width, height), pygame.SRCALPHA)

    # the width of the front of the cabinet from the left edge to the right edge of the controls
    frontwidth = randint(int(width/2), int(width * 0.75))
    widthleft = width-frontwidth
    backwidth = min(frontwidth / 4, widthleft)

    cabinetheight = randint(int(height*0.7), height)

    topoffrontypos = height - cabinetheight

    topedgeoffset = frontwidth / 10
    # right, left, bottom left, bottom right (counter-clockwise)
    topfront = ((backwidth+frontwidth+topedgeoffset, topoffrontypos),
                (backwidth+topedgeoffset, topoffrontypos),
                (backwidth, topoffrontypos+topedgeoffset),
                (backwidth+frontwidth, topoffrontypos+topedgeoffset))
    displayheight = int((height - topfront[-1][1]) / 3)
    buttonareaheight = displayheight/4
    coinareaheight = int((height - topfront[-1][1]) - displayheight - buttonareaheight)
    
    frontdisplayarea = (topfront[-1], topfront[-2],
                        (topfront[-2][0], topfront[-2][1]+displayheight),
                        (topfront[-1][0], topfront[-1][1]+displayheight))

    coinslotxoffset = int(width-topfront[-1][0])

    
    
    buttonsarea = (frontdisplayarea[-1], frontdisplayarea[-2],
                   (frontdisplayarea[-2][0]+coinslotxoffset, frontdisplayarea[-2][1] + buttonareaheight),
                   (frontdisplayarea[-1][0]+coinslotxoffset, frontdisplayarea[-1][1] + buttonareaheight))
                   

    pygame.gfxdraw.filled_polygon(surface, frontdisplayarea, variables.BLUE)
    pygame.gfxdraw.filled_polygon(surface, topfront, variables.BLACK)
    pygame.gfxdraw.filled_polygon(surface, buttonsarea, variables.BLUE)

    return surface
                        
                
