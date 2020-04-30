from pygame import gfxdraw, Rect


import variables
from DestructiveFrozenClass import DestructiveFrozenClass
from .Garden import Garden

from .shopplants import make_shopplant_list
from .constants import potsperrow
from .Plant import Plant

class Game(DestructiveFrozenClass):

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

        # how many items to scroll to keep things on screen
        self.lastcursoroffset = 0

            
        self._freeze()


    def shopgetplantbyname(self, name):
        for p in self.shopplants:
            if p.name == name:
                return p
        raise Exception("No shopplant with name " + str(name))


    def scale(self):
        return self.basescale * (1/(1+self.zoom))

    def draw(self, time, settings, screen):
        newcursoroffset = self.lastcursoroffset
        while self.garden.get_xpos_end_of_cursor_plant(self.cursorx, self.scale(), newcursoroffset, screen) == None:
            newcursoroffset -= 1
        while self.garden.get_xpos_end_of_cursor_plant(self.cursorx, self.scale(), newcursoroffset, screen)[0] > variables.width:
            newcursoroffset += 1

        # now to get how much it will scroll, calculate based upon a version without scrolling
        if newcursoroffset > 0:
            currentxscroll = self.garden.get_xpos_end_of_cursor_plant(newcursoroffset-1, self.scale(), 0, screen)[0]
        else:
            currentxscroll = 0
            
        self.garden.draw(time, settings, screen, self.scale(), currentxscroll = currentxscroll, cursoroffset = newcursoroffset, drawcursorindex = self.cursorx)

        self = self.destructiveset("lastcursoroffset", newcursoroffset)

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
            # also reset the offset for recalculation
            self = self.destructiveset("lastcursoroffset", 0)
        return self
