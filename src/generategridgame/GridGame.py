import pygame

from DestructiveFrozenClass import DestructiveFrozenClass


from .constants import keyrepeatspeed, scrollspeed

class GridGame(DestructiveFrozenClass):

    def __init__(self, subgrids, ship):
        self.subgrids = subgrids
        self.ship = ship
        self.shippospixels = (5, 5)
        # false or a number when being held that encodes the last time pos was updated
        self.leftpresstime = False
        self.rightpresstime = False
        self.uppresstime = False
        self.downpresstime = False

        
        self._freeze()

    def shippos(self, pixelsize):
        return (self.shippospixels[0]*pixelsize, self.shippospixels[1]*pixelsize)
        
    def draw(self, time, settings, screen, pixelsize):
        offset = (-self.getscroll(time, settings, pixelsize), 0)
        for s in self.subgrids:
            s.draw(time, settings, screen, offset)
        shippos = self.shippos(pixelsize)
        self.ship.draw(screen, (shippos[0] + offset[0], shippos[1]+offset[1]), pixelsize)

    def ontick(self, time, settings):

        
        if self.leftpresstime:
            if time-self.leftpresstime >= keyrepeatspeed:
                self = self.destructiveset("shippospixels", (self.shippospixels[0]-1, self.shippospixels[1]))
                self = self.destructiveset("leftpresstime", time)
        if self.rightpresstime:
            if time-self.rightpresstime >= keyrepeatspeed:
                self = self.destructiveset("shippospixels", (self.shippospixels[0]+1, self.shippospixels[1]))
                self = self.destructiveset("rightpresstime", time)
        if self.uppresstime:
            if time-self.uppresstime >= keyrepeatspeed:
                self = self.destructiveset("shippospixels", (self.shippospixels[0], self.shippospixels[1]-1))
                self = self.destructiveset("uppresstime", time)
        if self.downpresstime:
            if time-self.downpresstime >= keyrepeatspeed:
                self = self.destructiveset("shippospixels", (self.shippospixels[0], self.shippospixels[1]+1))
                self = self.destructiveset("downpresstime", time)
        return self

    def onkey(self, time, settings, event, pixelsize):

        
        if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
            keyreplace = False
            if event.type == pygame.KEYDOWN:
                keyreplace = time-keyrepeatspeed-1
                
            if settings.iskey("left", event.key):
                self = self.destructiveset("leftpresstime", keyreplace)
            elif settings.iskey("right", event.key):
                self = self.destructiveset("rightpresstime", keyreplace)
            elif settings.iskey("up", event.key):
                self = self.destructiveset("uppresstime",keyreplace)
            elif settings.iskey("down", event.key):
                self = self.destructiveset("downpresstime", keyreplace)
    
        return self

    def getscroll(self, time, settings, pixelsize):
        return time/1000 * scrollspeed * pixelsize

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
