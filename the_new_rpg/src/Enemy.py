#!/usr/bin/python
#Oliver Flatt works on Classes

class Enemy():
    lv = 1
    health = 20

    def __init__(self, pic, rarity):
        self.pic = pic
        self.rarity = rarity
