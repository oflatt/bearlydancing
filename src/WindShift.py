from pygame import Rect, Surface


import variables
from FrozenClass import FrozenClass
from Animation import Animation

screenrect = Rect(0,0,variables.width,variables.height)

class WindShift(FrozenClass):

    def __init__(self, surfaceoranimation, xpos, ypos, endtime):
        self.scompscale = variables.compscale()

        
        self.animation = surfaceoranimation
        if type(self.animation) == Surface:
            # frame rate does not matter if static image
            self.animation = Animation([self.animation], 10000, surfacelist = True)

        # map coordinates in pixels
        self.xpos = xpos
        self.ypos = ypos

        # when it expires
        self.endtime = endtime
        

        self._freeze()

    def draw(self, mapoffset, destination = variables.screen):
        
        cmpscale = variables.compscale()
        surf = self.animation.current_frame()
        offset = self.animation.current_offset()
        
        # only draw if it was spawned at the correct scale and on screen
        if cmpscale == self.scompscale:
            drawrect = Rect(self.xpos*cmpscale + mapoffset[0] + offset[0]*cmpscale,
                            self.ypos*cmpscale + mapoffset[1] + offset[1]*cmpscale,
                            surf.get_width(),
                            surf.get_height())
            if screenrect.contains(drawrect):
                destination.blit(surf, drawrect)
                variables.dirtyrects.append(drawrect)
                
