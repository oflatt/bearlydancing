from DestructiveFrozenClass import DestructiveFrozenClass

from .Plant import Plant

class Garden(DestructiveFrozenClass):

    def __init__(self):

        self.plants = [Plant(None)]
        self._freeze()

    def draw(self, time, settings, screen, scale):
        for p in self.plants:
            p.draw(time, settings, screen, scale)
            
