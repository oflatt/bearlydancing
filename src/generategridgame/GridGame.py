import pygame
from pygame import Rect

from DestructiveFrozenClass import DestructiveFrozenClass


from .constants import baseplayerspeed, basescrollspeed, basescrollgrowthrate

class GridGame(DestructiveFrozenClass):

    def __init__(self, subgrids, ship, scrollgrowthrate = basescrollgrowthrate):
        self.subgrids = subgrids
        # offset subgrids
        offset = 0
        for s in self.subgrids:
            s.rect.x += offset
            offset += s.rect.w
            
        self.ship = ship
        self.shippospixels = (5, 5)
        # false or a number when being held that encodes the last time pos was updated
        self.leftpresstime = False
        self.rightpresstime = False
        self.uppresstime = False
        self.downpresstime = False

        self.scrollgrowthrate = scrollgrowthrate
        
        self._freeze()

    def shippos(self, pixelsize):
        return (self.shippospixels[0]*pixelsize, self.shippospixels[1]*pixelsize)
        
    def draw(self, time, settings, screen, pixelsize):
        offset = (-self.getscroll(time, settings, pixelsize), 0)
        for s in self.subgrids:
            # don't draw if off the screen
            if offset[0] + s.rect[0] > screen.get_width()/screen.get_height():
                break
            s.draw(time, settings, screen, offset)
            
        shippos = self.shippos(pixelsize)
        self.ship.draw(screen, (shippos[0] + offset[0], shippos[1]+offset[1]), pixelsize)

        # draw edges of screen
        bwidth = max(1, pixelsize*screen.get_height()/8)
        pygame.gfxdraw.box(screen, Rect(0, 0, screen.get_width(), bwidth), (255, 0, 0))
        pygame.gfxdraw.box(screen, Rect(0, 0, bwidth, screen.get_height()), (255, 0, 0))
        pygame.gfxdraw.box(screen, Rect(0, screen.get_height()-bwidth, screen.get_width(), bwidth), (255, 0, 0))

        
        
    def ontick(self, time, settings, pixelsize):
    
        if self.leftpresstime != False:
            # subtract scroll speed to normalize movement
            newx = self.shippospixels[0]- ((self.getplayerspeed(time, pixelsize)-self.getscrollspeed(time, pixelsize))*(time-self.leftpresstime)/1000.0)
            self = self.destructiveset("shippospixels",
                                       (newx,
                                        self.shippospixels[1]))
            self = self.destructiveset("leftpresstime", time)
            
        if self.rightpresstime != False:
            newx = self.shippospixels[0]+(self.getplayerspeed(time, pixelsize)+self.getscrollspeed(time, pixelsize))*(time-self.rightpresstime)/1000.0
            self = self.destructiveset("shippospixels",
                                       (newx, self.shippospixels[1]))
            self = self.destructiveset("rightpresstime", time)
            
        if self.uppresstime != False:
            self = self.destructiveset("shippospixels",
                                       (self.shippospixels[0],
                                        self.shippospixels[1]-(self.getplayerspeed(time, pixelsize))*(time-self.uppresstime)/1000.0))
            self = self.destructiveset("uppresstime", time)
            
        if self.downpresstime != False:
            self = self.destructiveset("shippospixels",
                                       (self.shippospixels[0],
                                        self.shippospixels[1]+(self.getplayerspeed(time, pixelsize))*(time-self.downpresstime)/1000.0))
            self = self.destructiveset("downpresstime", time)

            
        return self


    
    def onkey(self, time, settings, key, pixelsize, keydownp):
        keyreplace = False
        if keydownp:
            keyreplace = time

        if settings.iskey("left", key):
            self = self.destructiveset("leftpresstime", keyreplace)
        elif settings.iskey("right", key):
            self = self.destructiveset("rightpresstime", keyreplace)
        elif settings.iskey("up", key):
            self = self.destructiveset("uppresstime",keyreplace)
        elif settings.iskey("down", key):
            self = self.destructiveset("downpresstime", keyreplace)
    
        return self

    def getscrollspeed(self, time, pixelsize):
        return basescrollspeed + (basescrollspeed*time/1000*self.scrollgrowthrate)

    def getscroll(self, time, settings, pixelsize):
        # double the scroll speed every two seconds
        return time/1000 * self.getscrollspeed(time, pixelsize) * pixelsize

    def getplayerspeed(self, time, pixelsize):
        return self.getscrollspeed(time, pixelsize)*2

    def gameoverp(self, time, settings, pixelsize, shippospixels = None):
        if shippospixels == None:
            shippos = self.shippos(pixelsize)
        else:
            shippos = (shippospixels[0]*pixelsize, shippospixels[1]*pixelsize)
        # check if player is off screen
        if shippos[0] < self.getscroll(time, settings, pixelsize):
            return True
        elif shippos[1]+pixelsize > 1:
            return True
        elif shippos[1] < 0:
            return True
        
        for s in self.subgrids:
            # no hitboxes from grids further along
            if s.rect.x > shippos[0]+pixelsize:
                break

            # if it is not a grid from before the ship
            if not s.rect.x + s.rect.w < shippos[0]:
                if s.collideswithshipp(time, settings, shippos, pixelsize):
                    return True

        return False
