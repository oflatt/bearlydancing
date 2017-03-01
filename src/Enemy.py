#!/usr/bin/python
#Oliver Flatt works on Classes
from Dancer import Dancer
import graphics, variables, enemies, copy

class Enemy(Dancer):

    def __init__(self, animationnum, rarity, name, beatmaprules):
        self.animationnum = animationnum
        self.reset()
        self.rarity = rarity
        self.name = name
        self.beatmaprules = beatmaprules

    def scalepure(self):
        for x in range(len(self.animation.pics)):
            self.animation.pics[x]["img"] = graphics.scale_pure(self.animation.pics[x]["img"], variables.width / 5)

    def reset(self):
        self.animation = enemies.animations[self.animationnum]
        self.animation.reset()
        self.scalepure()