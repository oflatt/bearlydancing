#!/usr/bin/python
#Oliver Flatt works on Classes
from FrozenClass import FrozenClass
import graphics, variables, enemies, copy, stathandeling
from FrozenClass import FrozenClass

class Enemy(FrozenClass):

    def __init__(self, animationnum, rarity, name, beatmaprules):
        self.lv = 0
        self.animationnum = animationnum
        self.reset()
        self.rarity = rarity
        self.name = name
        self.beatmaprules = beatmaprules
        self.health = None
        self.storyeventsonwin = None
        self.storyeventsonlose = None
        self.storyeventsonflee = None
        self.specialscale = None
        
        self._freeze()

    def reset(self):
        self.animation = enemies.animations[self.animationnum]
        self.animation.reset()

    def sethealth(self):
        self.health = stathandeling.max_health(self.lv)
