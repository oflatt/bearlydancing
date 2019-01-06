from pygame import Rect

import variables
from FrozenClass import FrozenClass

screenrect = Rect(0,0,variables.width,variables.height)

class WindShift(FrozenClass):

    def __init__(self, surface, xpos, ypos, endtime):
        self.scompscale = variables.compscale()
        self.surface = surface

        # map coordinates in pixels
        self.xpos = xpos
        self.ypos = ypos

        # when it expires
        self.endtime = endtime
        

        self._freeze()

    def draw(self, mapoffset):
        
        cmpscale = variables.compscale()
        # only draw if it was spawned at the correct scale and on screen
        if cmpscale == self.scompscale:
            drawrect = Rect(self.xpos*cmpscale + mapoffset[0],
                            self.ypos*cmpscale + mapoffset[1],
                            self.surface.get_width(),
                            self.surface.get_height())
            if screenrect.contains(drawrect):
                variables.screen.blit(self.surface, drawrect)
                variables.dirtyrects.append(drawrect)
        
