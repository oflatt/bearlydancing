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

        potsurface = getpic(self.potpic, 1)
        self.plantbasexoffset =  (self.posoffset[0] - potsurface.get_width()/2)
                                 
        pic = getpic(self.pic, 1)
        self.plantwidth = pic.get_width()
        
        self._freeze()


    def pot_pos(self, bottom_position, scale):
        potsurface = getpic(self.potpic, scale)
        return (bottom_position[0]+self.plantbasexoffset*scale, bottom_position[1]-potsurface.get_height())
        

    def draw(self, time, settings, screen, scale, position):
        pic = getpic(self.pic, scale)
        potsurface = getpic(self.potpic, scale)
        potpos = self.pot_pos(position, scale)
        
        screen.blit(potsurface, potpos)
        screen.blit(pic, (position[0],
                          -self.posoffset[1]*scale+ potpos[1] + 5*scale))
