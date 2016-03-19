#!/usr/bin/python
#Oliver Flatt works on Classes
import pygame, variables

class Map():
    def __init__(self, base, terrain):
        #base is a png
        self.base = base
        #terrain is a list of Rock
        self.terrain= terrain

    def draw(self):
        variables.screen.blit(self.base, [0, 0])
        #need to draw all Rock too