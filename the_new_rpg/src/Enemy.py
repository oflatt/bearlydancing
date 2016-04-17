#!/usr/bin/python
#Oliver Flatt works on Classes
from Dancer import Dancer

class Enemy(Dancer):

    def __init__(self, pic, rarity, name):
        self.pic = pic
        self.rarity = rarity
        self.name = name
