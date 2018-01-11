#!/usr/bin/python
#Oliver Flatt works on Classes
from Dancer import Dancer
import graphics, variables, enemies, copy, stathandeling

class Enemy(Dancer):

    def __init__(self, animationnum, rarity, name, beatmaprules):
        self.lv = 0
        self.animationnum = animationnum
        self.reset()
        self.rarity = rarity
        self.name = name
        self.beatmaprules = beatmaprules
        self.health = None

    def reset(self):
        self.animation = enemies.animations[self.animationnum]
        self.animation.reset()

    def sethealth(self):
        self.health = stathandeling.max_health(self.lv)
