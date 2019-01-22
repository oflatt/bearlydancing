
from DestructiveFrozenClass import DestructiveFrozenClass

class GridGame(DestructiveFrozenClass):

    def __init__(self, subgrids):
        self.subgrids = subgrids
        self._freeze()

    def draw(self, time, settings, screen):
        for s in self.subgrids:
            s.draw(time, settings, screen)
