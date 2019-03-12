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
        self.zoom = 0

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


    def scale(self):
        return self.basescale * (1/(1+self.zoom))

    def draw(self, time, settings, screen):
        initialy = variables.height/9

        initialxspacing = 20*self.scale()
        xspacing = 50*self.scale()

        def initialx():
            return initialxspacing + self.currentrowoffset

        def cursorx():
            return initialx() + self.cursorx*xspacing - xspacing/3

        while cursorx()+xspacing > screen.get_width():
            self = self.destructiveset("currentrowoffset", self.currentrowoffset - xspacing)
        while cursorx() < 0:
            self = self.destructiveset("currentrowoffset", self.currentrowoffset + xspacing)

        
        self.garden.draw(time, settings, screen, self.scale(), initialx(), xspacing)
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
        elif settings.iskey("zoom", key):
            self =self.destructiveset("zoom", (self.zoom + 1)% 3)
        return self
