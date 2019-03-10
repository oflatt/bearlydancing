import variables
from DestructiveFrozenClass import DestructiveFrozenClass

from .Plant import Plant

class Garden(DestructiveFrozenClass):

    def __init__(self):

        self.plants = []
        self._freeze()

    def draw(self, time, settings, screen, scale):
        initialx = 20*scale
        xspacing = 50*scale
        for i in range(len(self.plants)):
            self.plants[i].draw(time, settings, screen, scale,
                                (xspacing*i+initialx, variables.height*3/4))
            
    def addplant(self, newplant):
        self.plants.append(newplant)
