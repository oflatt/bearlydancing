#!/usr/bin/python
#Oliver Flatt works on Classes
from Dancer import Dancer
import graphics, variables

class Enemy(Dancer):

    def __init__(self, animation, rarity, name, beatmaprules):
        self.animation = animation
        self.rarity = rarity
        self.name = name
        self.beatmaprules = beatmaprules

    def scalepure(self):
        for x in range(len(self.animation.pics)):
            self.animation.pics[x]["img"] = graphics.scale_pure(self.animation.pics[x]["img"], variables.width / 5)
