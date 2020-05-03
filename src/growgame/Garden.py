from pygame import Rect, gfxdraw, Surface

from graphics import getpic

import variables
from DestructiveFrozenClass import DestructiveFrozenClass

from .Plant import Plant

class Garden(DestructiveFrozenClass):

    def __init__(self):

        self.plants = []
        self._freeze()


    def drawwood(self, time, settings, screen, scale, bottomypos, currentxscroll, endscroll):
        shelfheight = 7*scale
        shelfdepth = 18*scale
        shelfdepthoffset = 7*scale
        shelfyoffset = 2*scale
        frontcolor = (127, 88, 26)
        left = 10 * scale - currentxscroll
        shelfwidth = max(endscroll - scale * 10, screen.get_width()/2)

        frontrect = Rect(left, bottomypos-shelfheight+shelfyoffset, shelfwidth, shelfheight)

        # draw depth
        depthplist = [(frontrect[0], frontrect[1]),
                      (frontrect[0]+shelfdepthoffset, frontrect[1]-shelfheight),
                      (frontrect[0]+frontrect.width+shelfdepthoffset,
                       frontrect[1]-shelfheight),
                      (frontrect[0]+frontrect.width, frontrect[1])]
        gfxdraw.filled_polygon(screen, depthplist, variables.brighten(frontcolor, 13))
        
        # draw front
        gfxdraw.box(screen, frontrect, frontcolor)

        # draw right side
        rsideplist = [depthplist[-2], depthplist[-1],
                      (frontrect[0]+frontrect.width, frontrect[1]+shelfheight),
                      (depthplist[-2][0], depthplist[-2][1]+shelfheight)]
        gfxdraw.filled_polygon(screen, rsideplist, variables.brighten(frontcolor, -3))


    def tallest_height(self, scale):
        if len(self.plants) == 0:
            return 40*scale
        else:
            def pich(plant):
                return getpic(plant.pic, scale).get_height() + getpic(plant.potpic, scale).get_height()
            return pich(max(self.plants, key= pich))
            
        
    # returns the x position at which the cursor was drawn
    def draw(self, time, settings, screen : Surface, scale, cursoroffset = 0, currentxscroll = 0, endscroll = 0, drawcursorindex = None, nodraw = False, currenty = 0):
        bottomypos = self.tallest_height(scale) + currenty
        # first draw wood
        if not nodraw:
            self.drawwood(time, settings, screen, scale, bottomypos, currentxscroll, endscroll)

        xspace = variables.potxspace()
        currentx = xspace
        endofhighlighted = None
        
        for i in range(cursoroffset, len(self.plants)):
            currentpos = (currentx, bottomypos)
            if not nodraw:
                self.plants[i].draw(time, settings, screen, scale,
                                    currentpos, highlighted = drawcursorindex == i)
            currentx += self.plants[i].plantwidth*scale + xspace
            if drawcursorindex == i:
                endofhighlighted = currentx
        
        return (endofhighlighted, bottomypos)

    # returns the x position of the end of the currently highlighted plant
    def get_xpos_end_of_cursor_plant(self, cursorx : int, scale : float, oldcursoroffset : float, screen : Surface) -> Rect:
        endofhighlighted, bottomypos = self.draw(0, None, screen, scale, cursoroffset = oldcursoroffset, drawcursorindex = cursorx, nodraw = True) 
        return endofhighlighted
            
    def addplant(self, newplant):
        self.plants.append(newplant)
