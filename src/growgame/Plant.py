import math

from DestructiveFrozenClass import DestructiveFrozenClass
from graphics import getpic, makeplant


from .growgraphics import randompotpic
from .drawplant import drawplant


class Plant(DestructiveFrozenClass):

    def __init__(self, headnode):
        self.headnode = headnode
        
        self.pic, self.posoffset = makeplant(self.headnode)
        self.potpic = randompotpic()

        self.plantbaseoffset = self.plantbaseoffset(1, (0,0))
        
        self._freeze()

    def plantbaseoffset(self, scale, baseposition):
        potsurface = getpic(self.potpic, scale)
        return ((self.posoffset[0]*scale - potsurface.get_width()/2),
                (self.posoffset[1]*scale - potsurface.get_height()/4))

    def draw(self, time, settings, screen, scale, position):
        pic = getpic(self.pic, scale)
        potsurface = getpic(self.potpic, scale)
                  
        screen.blit(potsurface, (position[0]+self.plantbaseoffset[0]*scale,
                                 position[1]+self.plantbaseoffset[1]*scale))
        screen.blit(pic, position)
