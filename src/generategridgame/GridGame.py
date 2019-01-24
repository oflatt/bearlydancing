import pygame


from DestructiveFrozenClass import DestructiveFrozenClass

class GridGame(DestructiveFrozenClass):

    def __init__(self, subgrids, ship):
        self.subgrids = subgrids
        self.ship = ship
        self.shippos = (0.2, 0)
        self._freeze()

    def draw(self, time, settings, screen, pixelsize):
        offset = (-self.getscroll(time, settings), 0)
        for s in self.subgrids:
            s.draw(time, settings, screen, offset)

        self.ship.draw(screen, (self.shippos[0] + offset[0], self.shippos[1]+offset[1]), pixelsize)

    def onkey(self, time, settings, event, pixelsize):
        if event.type == pygame.KEYDOWN:
            if settings.iskey("left", event.key):
                self = self.destructiveset("shippos", (self.shippos[0]-pixelsize, self.shippos[1]))
            elif settings.iskey("right", event.key):
                self = self.destructiveset("shippos", (self.shippos[0]+pixelsize, self.shippos[1]))
            elif settings.iskey("up", event.key):
                self = self.destructiveset("shippos", (self.shippos[0], self.shippos[1]-pixelsize))
            elif settings.iskey("down", event.key):
                self = self.destructiveset("shippos", (self.shippos[0], self.shippos[1]+pixelsize))
        
        
        return self

    def getscroll(self, time, settings):
        return time/1000 * 0.2

    def gameoverp(self, time, settings, pixelsize):

        # check if player is off screen
        if self.shippos[0] < self.getscroll(time, settings):
            return True
        elif self.shippos[1]+pixelsize > 1:
            return True
        elif self.shippos[1] < 0:
            return True
        
        for s in self.subgrids:
            # no hitboxes from grids further along
            if s.rect.x > self.shippos[0]+pixelsize:
                break

            # if it is not a grid from before the ship
            if not s.rect.x + s.rect.w < self.shippos[0]:
                if s.collideswithshipp(time, settings, self.shippos, pixelsize):
                    return True

        return False
