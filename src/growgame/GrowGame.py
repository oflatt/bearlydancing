
import variables
from DestructiveFrozenClass import DestructiveFrozenClass
from .Garden import Garden

from .shopplants import make_shopplant_list
from .Plant import Plant

class GrowGame(DestructiveFrozenClass):

    def __init__(self):

        self.state = 'play'
        self.basescale = int(variables.height / 20 / 6)
        self.scale = self.basescale

        self.shopplants = make_shopplant_list()
        self.garden = Garden()

        # add all shop plants cheat
        for p in self.shopplants:
            self.garden.addplant(Plant(p.headnode))
        
        
        self._freeze()


    def shopgetplantbyname(self, name):
        for p in self.shopplants:
            if p.name == name:
                return p
        raise Exception("No shopplant with name " + str(name))



    def draw(self, time, settings, screen):
        self.garden.draw(time, settings, screen, self.basescale)
