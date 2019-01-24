
from DestructiveFrozenClass import DestructiveFrozenClass

class SubGrid(DestructiveFrozenClass):

    # all measurements in rect are fractions of the screen- with of 1 is one screen width
    def __init__(self, rect, lavas):

        self.rect = rect
        self.lavas = lavas

        self._freeze()


    def draw(self, time, settings, screen, offset):
        for l in self.lavas:
            l.draw(time, settings, screen, (self.rect[0] + offset[0], self.rect[1] + offset[1]))

    def collideswithshipp(self, time, settings, shippos, pixelsize):
        shippos = (shippos[0] - self.rect.x, shippos[1]-self.rect.y)
        for l in self.lavas:
            if l.collideswithshipp(time, settings, shippos, pixelsize):
                return True

        return False
