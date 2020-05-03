from pygame import gfxdraw, Rect

import devoptions
import variables
from DestructiveFrozenClass import DestructiveFrozenClass
from ChoiceButtons import ChoiceButtons
from .Garden import Garden
from pygame import Rect
from graphics import getpicbyheight, getTextPic

from .shopplants import make_shopplant_list
from .constants import potsperrow
from .Plant import Plant

class CursorState():
    def __init__(self, state = None, data = None):
        self.state = state
        self.data = data

class Game(DestructiveFrozenClass):

    def __init__(self):

        self.state = 'play'
        self.basescale = int(variables.height / 20 / 6)
        self.zoom = 1
        self.gardenlimit = 12

        self.shopplants = make_shopplant_list()
        self.gardens = [Garden()]

        # add all shop plants cheat
        #for p in self.shopplants:
         #   self.gardens[0].addplant(Plant(p.headnode))
          #  self.gardens[1].addplant(Plant(p.headnode))
        self.cursorstate = CursorState()

        # position of cursor on items
        self.cursorx = 0
        self.cursory = 0

        # how many items to scroll to keep things on screen
        self.lastcursoroffset = 0
        self.yscrolloffset = 0


        self.sun = 0
        if devoptions.devmode:
            self.sun = 2000

        
        buttonnames = ["breed (-10 Sun)", "sell (+5 Sun)"]
        self.specialbuttonslen = len(buttonnames)
        for p in self.shopplants:
            labelname = p.name + " (-" + str(p.cost) + " Sun)"
            buttonnames.append(labelname)
            

        self.shop = ChoiceButtons(buttonnames, 1/25)
        
        self._freeze()


    def buttonpressed(self, index):
        flowerindex = index-self.specialbuttonslen
        return self.addflower(self.shopplants[flowerindex])
        

    def addflower(self, shopplant):
        if self.sun >= shopplant.cost:
            self = self.destructiveset("sun", self.sun-shopplant.cost)
            added = False
            for garden in self.gardens:
                if len(garden.plants) < self.gardenlimit:
                    garden.addplant(Plant(shopplant.headnode))
                    added = True
            # otherwise all full
            if not added:
                self.gardens.append(Garden())
                self.gardens[-1].addplant(Plant(shopplant.headnode))
        return self
        
    def shopgetplantbyname(self, name):
        for p in self.shopplants:
            if p.name == name:
                return p
        raise Exception("No shopplant with name " + str(name))


    def scale(self):
        return self.basescale * (1/(1+self.zoom))

    def getgardenypositions(self, time, settings, screen):
        currenty = 0
        ylist = [0]
        for gardeni in range(len(self.gardens)):
            garden = self.gardens[gardeni]
            cursorpos, currenty = garden.draw(time, settings, screen, self.scale(), currenty = currenty, nodraw = True)
            ylist.append(currenty)
            
        return ylist

    def gardenindex(self):
        return max(self.cursory-1, 0)
    
    def draw(self, time, settings, screen):

        
        gardensareay = (self.shop.buttons[0].y*2) * screen.get_height() + self.shop.buttons[0].height()
        
        selectedgarden = self.gardens[self.gardenindex()]

        newcursoroffset = self.lastcursoroffset
        currentxscroll = 0
        if self.cursory != 0:
        
            while selectedgarden.get_xpos_end_of_cursor_plant(self.cursorx, self.scale(), newcursoroffset, screen) == None:
                newcursoroffset -= 1
            while selectedgarden.get_xpos_end_of_cursor_plant(self.cursorx, self.scale(), newcursoroffset, screen) > variables.width:
                newcursoroffset += 1

            # now to get how much it will scroll, calculate based upon a version without scrolling
            if newcursoroffset > 0:
                currentxscroll = selectedgarden.get_xpos_end_of_cursor_plant(newcursoroffset-1, self.scale(), 0, screen)
                

        

        gardenypositions = self.getgardenypositions(time, settings, screen)
        if gardenypositions[self.gardenindex()]+self.yscrolloffset < 0:
            self = self.destructiveset("yscrolloffset", -gardenypositions[self.gardenindex()])
        if gardenypositions[self.gardenindex()+1]+self.yscrolloffset > screen.get_height()-gardensareay:
            self = self.destructiveset("yscrolloffset", -(gardenypositions[self.gardenindex()+1]-screen.get_height() + gardensareay + 10*self.scale()))

        currenty = self.yscrolloffset + gardensareay
        
        for gardeni in range(len(self.gardens)):
            garden = self.gardens[gardeni]
            drawcursorindex =-1
            if gardeni == self.gardenindex() and self.cursory != 0:
                drawcursorindex = self.cursorx

            endscroll = garden.get_xpos_end_of_cursor_plant(len(garden.plants)-1, self.scale(), 0, screen)
            if endscroll == None:
                endscroll = 0
            highlightset = set()
            if self.cursorstate.state == "swap" and self.cursorstate.data[1] == gardeni:
                highlightset.add(self.cursorstate.data[0])
                
            cursorpos, currenty = garden.draw(time, settings, screen, self.scale(), currentxscroll = currentxscroll, cursoroffset = newcursoroffset, endscroll=endscroll, drawcursorindex = drawcursorindex, currenty = currenty, drawhighlighted = highlightset)

        self = self.destructiveset("lastcursoroffset", newcursoroffset)

        self.drawshop(screen, gardensareay)
        self.drawsun(screen)
        
        return self

    def drawshop(self, screen, gardensareay):
        screen.fill(variables.GREY, Rect(0, 0, screen.get_width(), gardensareay))
        
        self.shop.isselected = self.cursory == 0
        if self.cursory == 0:
            self.shop.currentoption = self.cursorx
        else:
            self.shop.currentoption = 0
        self.shop.draw()

    def drawsun(self, screen):
        sunh = screen.get_height()*1/15
        sunpic = getpicbyheight("sun3", sunh)
        texth = sunh * 2/3
        textpic = getTextPic(" " + str(self.sun) + " ", texth)
        boxrect = Rect(screen.get_width()-textpic.get_width()-sunpic.get_width()
                       ,screen.get_height()-sunh
                       ,textpic.get_width()+sunpic.get_width()
                       ,sunh)
        screen.fill(variables.GREY, boxrect)
        screen.blit(sunpic, boxrect)
        screen.blit(textpic, (boxrect.x + sunpic.get_width(), boxrect.y + (sunh-texth)/2))
        
        
        
        
        
        

    def current_row_length(self):
        if(self.cursory == 0):
            return len(self.shop.buttons)
        else:
            return len(self.gardens[self.gardenindex()].plants)

    def plantpressed(self):
        if self.cursorstate.state == None:
            self = self.destructiveset("cursorstate", CursorState("swap", (self.cursorx, self.gardenindex())))
        elif self.cursorstate.state == "swap":
            xpos, gardeni = self.cursorstate.data
            temp = self.gardens[gardeni].plants[xpos]
            self.gardens[gardeni].plants[xpos] = self.gardens[self.gardenindex()].plants[self.cursorx]
            self.gardens[self.gardenindex()].plants[self.cursorx] = temp
            self = self.destructiveset("cursorstate", CursorState(None, None))
        return self
            

    def onkeydown(self, key, settings):
        if settings.iskey("right", key):
            self = self.destructiveset("cursorx", (self.cursorx+1) % self.current_row_length())
        elif settings.iskey("left", key):
            self = self.destructiveset("cursorx", (self.cursorx-1)%self.current_row_length())
        elif settings.iskey("up", key):
            self = self.destructiveset("cursory", (self.cursory-1)%(len(self.gardens)+1))
            if self.cursory > 0 and len(self.gardens[self.gardenindex()].plants) == 0:
                self = self.destructiveset("cursory", (self.cursory-1)%(len(self.gardens)+1))
            
            if self.cursory == 0:
                self = self.destructiveset("cursorx", 0)
            else:
                self = self.destructiveset("cursorx", min(self.cursorx, self.current_row_length()-1))
            
        elif settings.iskey("down", key):
            self = self.destructiveset("cursory", (self.cursory+1)%(len(self.gardens)+1))
            if self.cursory > 0 and len(self.gardens[self.gardenindex()].plants) == 0:
                self = self.destructiveset("cursory", (self.cursory+1)%(len(self.gardens)+1))
                
            if self.cursory == 0:
                self = self.destructiveset("cursorx", 0)
            else:
                self = self.destructiveset("cursorx", min(self.cursorx, self.current_row_length()-1))
                
        elif settings.iskey("action", key):
            if self.cursory == 0:
                self = self.destructiveset("cursorstate", CursorState(None, None))
                self = self.buttonpressed(self.cursorx)
            else:
                self = self.plantpressed()
        elif settings.iskey("zoom", key):
            self =self.destructiveset("zoom", (self.zoom + 1)% 4)
            # also reset the offset for recalculation
            self = self.destructiveset("lastcursoroffset", 0)
        return self
