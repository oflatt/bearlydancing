
from DestructiveFrozenClass import DestructiveFrozenClass

class Ship(DestructiveFrozenClass):

    def __init__(self):
        self._freeze()

    def draw(self, screen, pos, pixelsize):
        screen.fill((0, 180, 0), (pos[0]*screen.get_height(), pos[1]*screen.get_height(), pixelsize*screen.get_height(), pixelsize*screen.get_height()))
