import pygame
from collections import OrderedDict
from FrozenClass import FrozenClass

class Settings(FrozenClass):

    def __init__(self):
        # keybindings
        self.keydict = OrderedDict()
        self.keydict["up"] =[pygame.K_UP, pygame.K_w]
        self.keydict["down"] = [pygame.K_DOWN, pygame.K_s]
        self.keydict["left"] = [pygame.K_LEFT, pygame.K_a]
        self.keydict["right"] = [pygame.K_RIGHT, pygame.K_d]
        self.keydict["action"] = [pygame.K_SPACE, pygame.K_RETURN, pygame.K_KP_ENTER]
        self.keydict["note1"] = [pygame.K_a]
        self.keydict["note2"] = [pygame.K_s]
        self.keydict["note3"] = [pygame.K_d]
        self.keydict["note4"] = [pygame.K_f]
        self.keydict["note5"] = [pygame.K_j]
        self.keydict["note6"] = [pygame.K_k]
        self.keydict["note7"] = [pygame.K_l]
        self.keydict["note8"] = [pygame.K_SEMICOLON]

        self.keydict["escape"] = [pygame.K_ESCAPE]

        # normal setting stuff
        self.windowmode = "windowed"
        self.volume = 0.5

        # state can be world, battle, or conversation
        self.state = "world"
        self.backgroundstate = "world"
        self.menuonq = True
        self.easymodeq = False

        #possible soundpacks can be seen by listing the keys in all_sounds in play_sound
        self.soundpack = "sine"

        # the index in the player.scales currently chosen
        self.scaleindex = 0
        
        # the number of (length 1) notes that can be shown on screen at once before the pad
        self.notes_per_screen = 6

        self.username = "Greg"
        self.bearname = "Honey"

        # master clock
        self.current_time = 0

        # this is an offset for all enemy levels
        self.difficulty = 0

        self._freeze()
