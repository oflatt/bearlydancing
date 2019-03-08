from DestructiveFrozenClass import DestructiveFrozenClass
from .Garden import Garden

from .shopplants import getplantbyname
from .Plant import Plant

class GrowGame(DestructiveFrozenClass):

    def __init__(self):

        self.state = 'play'
        self.scale = 12
        self.garden = Garden()
        self.garden.addplant(Plant(getplantbyname("rose").headnode))
        self._freeze()


    def draw(self, time, settings, screen):
        self.garden.draw(time, settings, screen, self.scale)
