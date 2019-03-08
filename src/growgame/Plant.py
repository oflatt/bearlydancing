import math

from DestructiveFrozenClass import DestructiveFrozenClass
from graphics import getpic, makeplant


from .growgraphics import potpic
from .drawplant import drawplant


class Plant(DestructiveFrozenClass):

    def __init__(self, headnode):
        self.headnode = headnode
        
        self.pic = makeplant(self.headnode)
        self._freeze()

    def draw(self, time, settings, screen, scale):
        pic = getpic(self.pic, scale)
        
        screen.blit(getpic(potpic, scale), (10*scale,pic.get_height()-10*scale))
        screen.blit(getpic(self.pic, scale), (0,0))
