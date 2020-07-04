import pygame
from collections import OrderedDict
from FrozenClass import FrozenClass


class Settings(FrozenClass):

    def __init__(self):
        # keybinding
        self.keydict = OrderedDict()
        self.keydict["up"] =[pygame.K_UP, pygame.K_w, "joyaxis1-"]
        self.keydict["down"] = [pygame.K_DOWN, pygame.K_s, "joyaxis1+"]
        self.keydict["left"] = [pygame.K_LEFT, pygame.K_a, "joyaxis0-"]
        self.keydict["right"] = [pygame.K_RIGHT, pygame.K_d, "joyaxis0+"]
        self.keydict["action"] = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER, "joy0"]
        self.keydict["zoom"] = [pygame.K_z]
        self.keydict["note1"] = [pygame.K_a]
        self.keydict["note2"] = [pygame.K_s]
        self.keydict["note3"] = [pygame.K_d]
        self.keydict["note4"] = [pygame.K_f]
        self.keydict["note5"] = [pygame.K_j]
        self.keydict["note6"] = [pygame.K_k]
        self.keydict["note7"] = [pygame.K_l]
        self.keydict["note8"] = [pygame.K_SEMICOLON]
        self.keydict["notemodifier"] = [pygame.K_SPACE]
        self.keydict["note1modified"] = [pygame.K_w]
        self.keydict["note2modified"] = [pygame.K_e]
        self.keydict["note3modified"] = [pygame.K_r]
        self.keydict["note4modified"] = [pygame.K_t]
        self.keydict["note5modified"] = [pygame.K_i]
        self.keydict["note6modified"] = [pygame.K_o]
        self.keydict["note7modified"] = [pygame.K_p]
        self.keydict["note8modified"] = [pygame.K_LEFTBRACKET]
        
        self.keydict["escape"] = [pygame.K_ESCAPE, "joy7"]


        # normal setting stuff
        self.windowmode = "fullscreen"
        self.volume = 0.5
        self.autosavep = True

        # state can be world, battle, game, or conversation
        self.state = "world"
        self.backgroundstate = "world"
        self.menuonq = True

        # zoom level is for viewing the world- gets added to the display scale
        self.zoomlevel = 0

        #possible soundpacks can be seen by listing the keys in all_sounds in play_sound
        self.soundpack = "sine"

        # the index in the player.scales currently chosen
        self.scaleindex = 0
        
        # the number of (length 1) notes that can be shown on screen at once before the pad
        self.notes_per_screen = 6

        # maximum number of volume envelopes to apply per frame,
        # since it is expensive
        self.maxvolumeenvelopesperframe = 1

        self.username = "Greg" # the names should always end up overwritten
        self.bearname = "Honey"

        # master clock
        self.current_time = 0

        # this is an offset for all enemy levels
        self.difficulty = 0

        self.dancepadmodep = False

        # gamedata is a dict that can be populated by Game objects
        self.gamedata = {}
        self.currentgame = None

        self.lastslowtick = 0

        # used to keep track of the state of joystick, a set containing all joy stick axis that are pressed. Example: {"joyaxis0+"} is the x-axis to the right
        self.joyaxispressed = set()
        self.stickthreshhold = 0.2

        # money used in minigames
        self.money = 0
        
        self._freeze()

    def iskey(self,binding, pygamekey):
        return pygamekey in self.keydict[binding]

    def slowtickp(self):
        if self.current_time - self.lastslowtick >= 500:
            self.lastslowtick = self.current_time
            return True
        return False
        
    def soundonp(self):
        return self.volume != 0

    def updatezoom(self, displayscale):
        self.zoomlevel = self.zoomlevel+1
        if self.zoomlevel == 2:
            self.zoomlevel += 1
        elif self.zoomlevel > 2:
            self.zoomlevel = 0

    def setgamedata(self, gamename, gamedata):
        self.gamedata[gamename] = gamedata

    def getgamedata(self, gamename):
        try:
            return self.gamedata[gamename]
        except KeyError:
            return None

    def addmoney(self, amount):
        self.money += amount

    def getjoyeventname(self, event):
        eventname = "joyaxis" + str(event.axis)
        if event.value > 0:
            eventname = eventname + "+"
        else:
            eventname = eventname + "-"
        return eventname

    def joyaxistokeydown(self, event):
        presslist = []

        #joy = pygame.joystick.Joystick(i)
        
        if event.value > self.stickthreshhold or event.value < -self.stickthreshhold:
            eventname = self.getjoyeventname(event)
            
            if not eventname in self.joyaxispressed:
                self.joyaxispressed.add(eventname)
                return eventname

        return presslist

    def joyaxistokeyup(self, event):
        if event.value < self.stickthreshhold and event.value > -self.stickthreshhold:
            eventname = self.getjoyeventname(event)
            event.value = -event.value
            eventnameopposite = self.getjoyeventname(event)
            
            if eventname in self.joyaxispressed:
                self.joyaxispressed.remove(eventname)
                return eventname
            if eventnameopposite in self.joyaxispressed:
                self.joyaxispressed.remove(eventnameopposite)
                return eventnameopposite
        
