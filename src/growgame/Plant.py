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
        self._freeze()

    def draw(self, time, settings, screen, scale, baseposition):
        pic = getpic(self.pic, scale)
        potsurface = getpic(self.potpic, scale)
        potpos = (baseposition[0], baseposition[1]-potsurface.get_height())

        plantpos = (-self.posoffset[0]*scale+potpos[0] + potsurface.get_width()/2, -self.posoffset[1]*scale+potpos[1] + potsurface.get_height()/4)
                  
        screen.blit(potsurface, potpos)
        screen.blit(pic, plantpos)
