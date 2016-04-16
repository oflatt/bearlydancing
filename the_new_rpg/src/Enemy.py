#!/usr/bin/python
#Oliver Flatt works on Classes

class Enemy():
    lv = 1
    health = 25

    def __init__(self, pic, rarity, name):
        self.pic = pic
        self.rarity = rarity
        self.name = name
