import math, random

import variables
from pygame import Rect, gfxdraw
from DestructiveFrozenClass import DestructiveFrozenClass
from graphics import getpic, makeplant
from Animation import Animation


from .growgraphics import randompotpic
from .drawplant import drawplant

sunanimduration = 1000
sunanim = Animation(["sun0", "sun1", "sun2", "sun3"]
                    ,sunanimduration / 4.0
                    ,loopp = False)

class Plant(DestructiveFrozenClass):

    def __init__(self, headnode):
        self.headnode = headnode
        
        self.pic, self.posoffset = makeplant(self.headnode)
        self.potpic = randompotpic()

        potsurface = getpic(self.potpic, 1)
        self.plantbasexoffset =  (self.posoffset[0] - potsurface.get_width()/2)
                                 
        pic = getpic(self.pic, 1)
        self.plantwidth = pic.get_width()
        self.nextsuntime = 0
        self.sunanimtime = None
        
        self._freeze()


    def pot_pos(self, bottom_position, scale):
        potsurface = getpic(self.potpic, scale)
        return (bottom_position[0]+self.plantbasexoffset*scale, bottom_position[1]-potsurface.get_height())
        

    def draw(self, time, settings, screen, scale, position, highlighted = False, highlightcolor = (211, 214, 64)):
        pic = getpic(self.pic, scale)
        potsurface = getpic(self.potpic, scale)
        potpos = self.pot_pos(position, scale)
        
        screen.blit(potsurface, potpos)
        screen.blit(pic, (position[0],
                          -self.posoffset[1]*scale+ potpos[1] + 5*scale))
        if self.sunanimtime != None:
            timezerotoone = (time-self.sunanimtime)/sunanimduration
            sunypos = potpos[1] - (timezerotoone) * pic.get_height()*0.75
            sunxpos = potpos[0] + potsurface.get_width() * 0.75
            picname = sunanim.current_frame(begin_time = self.sunanimtime, current_time = time)
            sunpic = getpic(picname, scale)
            screen.blit(sunpic, (sunxpos, sunypos))
            

        if highlighted:
            xspace = variables.potxspace()
            cursordrawpos = Rect(potpos[0]-xspace, potpos[1]-xspace,
                                     xspace, xspace)
            gfxdraw.box(screen, cursordrawpos, highlightcolor)

    def tick(self, time):
        addsun = 0
        if time > self.nextsuntime:
            self = self.destructiveset("nextsuntime", time + random.randint(10000, 20000))
            self = self.destructiveset("sunanimtime", time)
            
        if self.sunanimtime != None:
            if self.sunanimtime+sunanimduration < time:
                self = self.destructiveset("sunanimtime", None)
                addsun = 1
        return self, addsun
