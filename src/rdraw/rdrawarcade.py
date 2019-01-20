import pygame, random
from random import randint
from pygame import Surface

import variables

def makecabinet():
    width = 28
    height = 48
    # make it bigger in case cropped off
    surface = pygame.Surface((width+3, height), pygame.SRCALPHA)

    # the width of the front of the cabinet from the left edge to the right edge of the controls
    frontwidth = randint(int(width/2), int(width * 0.75))
    widthleft = width-frontwidth
    backwidth = min(frontwidth / 4, widthleft)

    cabinetheight = height*0.7

    topoffrontypos = height - cabinetheight

    topedgeoffset = frontwidth / 10
    topedgeheight = frontwidth / 4
    # right, left, bottom left, bottom right (counter-clockwise)
    topfront = ((backwidth+frontwidth+topedgeoffset, topoffrontypos),
                (backwidth+topedgeoffset, topoffrontypos),
                (backwidth, topoffrontypos+topedgeheight),
                (backwidth+frontwidth, topoffrontypos+topedgeheight))
    displayheight = int((height - topfront[-1][1]) / 2.3)
    buttonareaheight = displayheight/4
    coinareaheight = int((height - topfront[-1][1]) - displayheight - buttonareaheight)
    
    frontdisplayarea = (topfront[-1], topfront[-2],
                        (topfront[-2][0], topfront[-2][1]+displayheight),
                        (topfront[-1][0], topfront[-1][1]+displayheight))

    screenshrink = 2
    screenarea = ((frontdisplayarea[0][0]-screenshrink, frontdisplayarea[0][1]+screenshrink),
                  (frontdisplayarea[1][0]+screenshrink, frontdisplayarea[1][1]+screenshrink),
                  (frontdisplayarea[2][0]+screenshrink, frontdisplayarea[2][1]-screenshrink),
                  (frontdisplayarea[3][0]-screenshrink, frontdisplayarea[3][1]-screenshrink))

    coinslotxoffset = frontwidth/4

    
    
    buttonsarea = (frontdisplayarea[-1], frontdisplayarea[-2],
                   (frontdisplayarea[-2][0]+coinslotxoffset, frontdisplayarea[-2][1] + buttonareaheight),
                   (frontdisplayarea[-1][0]+coinslotxoffset, frontdisplayarea[-1][1] + buttonareaheight))

    coinslotarea = (buttonsarea[-1], buttonsarea[-2],
                    (buttonsarea[-2][0], buttonsarea[-2][1] + coinareaheight),
                    (buttonsarea[-1][0], buttonsarea[-1][1] + coinareaheight))

    yoffsetback = backwidth / 3
    backx = topfront[1][0]-backwidth
    sidearea = (topfront[1],
                (backx, topfront[1][1] - yoffsetback),
                (backx,  coinslotarea[-2][1]-yoffsetback*((coinslotarea[-2][0]-backx)/float(backwidth))),
                coinslotarea[-2])

    toparea = ((sidearea[1][0]+frontwidth, sidearea[1][1]),
               sidearea[1],
               sidearea[0],
               ((sidearea[0][0] + frontwidth), sidearea[0][1]))

    
    machinecolor = variables.randomnicecolor()

    pygame.gfxdraw.filled_polygon(surface, sidearea, machinecolor)
    
    screenbordercolor = variables.randomnicecolor()

    pygame.gfxdraw.filled_polygon(surface, toparea, variables.brighten(random.choice((machinecolor, screenbordercolor)), -20))
    
    pygame.gfxdraw.filled_polygon(surface, topfront, variables.brighten(random.choice((machinecolor, screenbordercolor)), -40))

    pygame.gfxdraw.filled_polygon(surface, frontdisplayarea, screenbordercolor)
    pygame.gfxdraw.filled_polygon(surface, screenarea, variables.BLACK)

    pygame.gfxdraw.filled_polygon(surface, buttonsarea, variables.brighten(screenbordercolor, -50))
    coinslotareacolor = variables.brighten(machinecolor, -30)
    pygame.gfxdraw.filled_polygon(surface, coinslotarea, coinslotareacolor)
    pygame.gfxdraw.polygon(surface, coinslotarea, variables.brighten(coinslotareacolor, -20))

    return surface
                        
                
