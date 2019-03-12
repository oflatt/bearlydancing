import variables
from DestructiveFrozenClass import DestructiveFrozenClass

from .Plant import Plant

class Garden(DestructiveFrozenClass):

    def __init__(self):

        self.plants = []
        self._freeze()

    def draw(self, time, settings, screen, scale, initialx, xspacing):
        for i in range(len(self.plants)):
            self.plants[i].draw(time, settings, screen, scale,
                                (xspacing*i+initialx, 0))
            
    def addplant(self, newplant):
        self.plants.append(newplant)
