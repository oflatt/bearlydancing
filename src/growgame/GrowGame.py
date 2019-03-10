
import variables
from DestructiveFrozenClass import DestructiveFrozenClass
from .Garden import Garden

from .shopplants import getplantbyname, getallplants
from .Plant import Plant

class GrowGame(DestructiveFrozenClass):

    def __init__(self):

        self.state = 'play'
        self.basescale = int(variables.height / 20 / 6)
        self.scale = self.basescale
        self.garden = Garden()

        # add all shop plants cheat
        for p in getallplants():
            self.garden.addplant(Plant(p.headnode))
        
        
        self._freeze()


    def draw(self, time, settings, screen):
        self.garden.draw(time, settings, screen, self.basescale)
