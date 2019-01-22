
from DestructiveFrozenClass import DestructiveFrozenClass

class SubGrid(DestructiveFrozenClass):

    # all measurements in rect are fractions of the screen- with of 1 is one screen width
    def __init__(self, rect, lavas):

        self.rect = rect
        self.lavas = lavas

        self._freeze()


    def draw(self, time, settings, screen):
        for l in self.lavas:
            l.draw(time, settings, screen, self.rect)
        
