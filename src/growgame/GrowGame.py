from pygame import gfxdraw, Rect


import variables
from DestructiveFrozenClass import DestructiveFrozenClass
from .Garden import Garden

from .shopplants import make_shopplant_list
from .constants import potsperrow
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
        

        # position of cursor on items
        self.cursorx = 0
        self.cursory = 0

        # for drawing- keeps track of the current scroll of the picture horizontally
        self.currentrowoffset = 0
            
        self._freeze()


    def shopgetplantbyname(self, name):
        for p in self.shopplants:
            if p.name == name:
                return p
        raise Exception("No shopplant with name " + str(name))



    def draw(self, time, settings, screen):
        initialy = variables.height/4

        initialxspacing = 20*self.basescale
        xspacing = 50*self.basescale

        def initialx():
            return initialxspacing + self.currentrowoffset

        def cursorx():
            return initialx() + self.cursorx*xspacing - xspacing/3

        while cursorx()+xspacing > screen.get_width():
            self = self.destructiveset("currentrowoffset", self.currentrowoffset - xspacing)
        while cursorx() < 0:
            self = self.destructiveset("currentrowoffset", self.currentrowoffset + xspacing)

        
        self.garden.draw(time, settings, screen, self.basescale, initialx(), xspacing)
        gfxdraw.box(screen, Rect(cursorx(), initialy, xspacing/15, xspacing/15), (211, 214, 64))

        return self

    def current_row_length(self):
        return len(self.garden.plants) - self.cursory * potsperrow

    def onkeydown(self, key, settings):
        if settings.iskey("right", key):
            if self.cursorx < self.current_row_length()-1:
                self = self.destructiveset("cursorx", (self.cursorx+1))
        elif settings.iskey("left", key):
            if self.cursorx > 0:
                self = self.destructiveset("cursorx", (self.cursorx-1)%self.current_row_length())
        return self
